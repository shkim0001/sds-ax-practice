# semiconductor_swarm.py - 반도체 전망을 따져보는 Network(Swarm) 3인 팀
#
#   news_collector  최신뉴스 수집가   : Google News RSS로 최근 기사 수집
#   process_expert  반도체 공정 전문가: 뉴스를 공정·기술 관점(미세화, 수율, HBM, 패키징)으로 해석
#   market_analyst  증시 분석가       : Yahoo Finance 시세로 주가 흐름을 확인하고 최종 전망 정리
#
# network_demo.py와 같은 Swarm 구조입니다. 관리자 노드 없이 각 Agent가 handoff 도구로 서로 넘깁니다.
# 기본 릴레이: news_collector → process_expert → market_analyst(최종 정리)
# 실제 외부 데이터를 쓰므로 인터넷 연결이 필요합니다. 투자 권유가 아닌 교육용 데모입니다.
from datetime import date
import xml.etree.ElementTree as ET

import httpx
from botocore.config import Config
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_handoff_tool, create_swarm

load_dotenv()
MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
TODAY = date.today().isoformat()
HEADERS = {"User-Agent": "Mozilla/5.0 (sds-ax-training demo)"}

def llm():
    # Agent 3명이 연달아 호출하므로 분당 요청 한도(ThrottlingException)에 걸리기 쉽습니다.
    # adaptive 모드는 한도에 걸리면 간격을 늘려 가며 자동으로 다시 시도합니다.
    return ChatBedrockConverse(
        model=MODEL, region_name="us-east-1", temperature=0,
        config=Config(retries={"max_attempts": 10, "mode": "adaptive"}),
    )

def get_text(message):
    """content가 블록 리스트면 text만 모아 반환합니다."""
    c = message.content
    return "".join(b.get("text", "") for b in c if isinstance(b, dict)) if isinstance(c, list) else (c or "")


# ---------- 도구: Agent마다 자기 도메인 도구만 가집니다 ----------
# 도구는 실패해도 예외를 던지지 않고, 무엇이 안 됐는지 문장으로 돌려줍니다.
# 데이터를 못 받으면 지어내지 말라고 모델에게 알려 주는 역할도 합니다.

@tool
def search_news(query: str, days: int = 14) -> str:
    """최근 반도체 관련 뉴스 기사 제목·날짜·언론사를 검색한다.
    query 예: '반도체 업황', 'HBM 수요', 'TSMC 2나노', '메모리 가격'. days는 최근 며칠 이내 기사인지."""
    try:
        r = httpx.get(
            "https://news.google.com/rss/search",
            params={"q": f"{query} when:{days}d", "hl": "ko", "gl": "KR", "ceid": "KR:ko"},
            headers=HEADERS, timeout=10, follow_redirects=True,
        )
        r.raise_for_status()
        items = list(ET.fromstring(r.text).iter("item"))[:6]
    except Exception as e:
        return f"뉴스 검색 실패({type(e).__name__}). 기사 없이 추측하지 말고 데이터 부족을 그대로 보고하라."
    if not items:
        return f"'{query}' 최근 {days}일 기사가 없습니다. 검색어를 바꿔 다시 시도하라."
    lines = []
    for it in items:
        source = it.findtext("source") or "출처 미상"
        lines.append(f"- {it.findtext('title')} ({source}, {it.findtext('pubDate', '')[:16]})")
    return f"[뉴스: {query}, 최근 {days}일]\n" + "\n".join(lines)


PROCESS_CHECKLIST = {
    "미세화": "선단 공정(3nm/2nm GAA) 전환 일정, 경쟁사 대비 양산 시점, EUV 장비 확보 수준",
    "수율": "신공정 초기 수율 이슈 보도 여부, 고객사 인증(퀄) 통과 여부",
    "HBM": "HBM 세대(HBM3E/HBM4) 양산·공급 비중, 주요 GPU 고객사 납품 여부, TSV·적층 수율",
    "패키징": "CoWoS 등 첨단 패키징 생산능력이 AI 칩 출하의 병목인지",
    "메모리 사이클": "DRAM/NAND 가격 추세, 재고 수준, 감산·증설 발표",
    "공급망": "장비·소재 수출 규제, 신규 팹 건설·가동 일정, 전력·용수 이슈",
}

@tool
def process_checklist(topic: str = "") -> str:
    """반도체 공정·기술 관점의 점검 항목을 돌려준다. topic: 미세화, 수율, HBM, 패키징, 메모리 사이클, 공급망 (빈 값이면 전체)."""
    if topic and topic in PROCESS_CHECKLIST:
        return f"[공정 점검: {topic}] {PROCESS_CHECKLIST[topic]}"
    return "[공정 점검 항목]\n" + "\n".join(f"- {k}: {v}" for k, v in PROCESS_CHECKLIST.items())


TICKER_NAMES = {
    "005930.KS": "삼성전자", "000660.KS": "SK하이닉스", "NVDA": "엔비디아",
    "TSM": "TSMC(ADR)", "MU": "마이크론", "ASML": "ASML", "SOXX": "필라델피아 반도체 ETF(SOXX)",
}

@tool
def get_stock_trend(ticker: str, period: str = "3mo") -> str:
    """종목의 기간 주가 흐름(시작가·현재가·등락률·최고·최저)을 조회한다.
    ticker 예: 005930.KS(삼성전자), 000660.KS(SK하이닉스), NVDA, TSM, MU, ASML, SOXX. period: 1mo, 3mo, 6mo, 1y."""
    try:
        r = httpx.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
            params={"range": period, "interval": "1d"}, headers=HEADERS, timeout=10,
        )
        r.raise_for_status()
        res = r.json()["chart"]["result"][0]
        closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
    except Exception as e:
        return f"{ticker} 시세 조회 실패({type(e).__name__}). 시세를 추측하지 말고 조회 실패를 보고하라."
    if len(closes) < 2:
        return f"{ticker} 시세 데이터가 부족합니다."
    cur = res["meta"].get("currency", "")
    first, last = closes[0], closes[-1]
    name = TICKER_NAMES.get(ticker, ticker)
    return (f"[시세: {name} {ticker}, 최근 {period}] 시작 {first:,.1f} → 현재 {last:,.1f} {cur} "
            f"({(last / first - 1) * 100:+.1f}%), 기간 최고 {max(closes):,.1f}, 최저 {min(closes):,.1f}")


# ---------- handoff 도구: 누구에게 넘길 수 있는지를 각 Agent가 직접 들고 있습니다 ----------
to_news = create_handoff_tool(agent_name="news_collector",
                              description="최신 뉴스·기사 근거가 더 필요하면 news_collector에게 넘긴다.")
to_process = create_handoff_tool(agent_name="process_expert",
                                 description="공정·기술(미세화, 수율, HBM, 패키징) 해석이 필요하면 process_expert에게 넘긴다.")
to_market = create_handoff_tool(agent_name="market_analyst",
                                description="주가·증시 분석이나 최종 전망 정리가 필요하면 market_analyst에게 넘긴다.")

COMMON = (f"오늘은 {TODAY}다. 학습 지식이 아니라 도구 결과와 앞 담당자의 보고만 근거로 쓴다.\n"
          "자기 도구 목록에 없는 도구는 호출하지 말고, 필요하면 해당 담당자에게 넘겨라.\n"
          "transfer_to_* 도구는 다른 도구와 같은 턴에 섞지 말고, 결과를 다 받은 뒤 단독으로 호출하라.\n")


# ---------- 결과 없는 tool_use 보정 미들웨어 ----------
# 모델이 한 턴에 [search_news, transfer_to_process_expert]처럼 일반 도구와 handoff를 같이 부르면,
# handoff가 Command(graph=PARENT)로 즉시 Agent를 바꾸면서 자기 ToolMessage만 기록에 남깁니다.
# 같은 턴의 다른 도구 결과는 사라지고, Bedrock은 짝이 없는 tool_use를 보면
#   ValidationException: Expected toolResult blocks at messages.N.content ...
# 를 냅니다. 모델을 부르기 직전에 빠진 결과를 채워 넣어 기록의 짝을 맞춥니다. (저장된 상태는 바꾸지 않음)
@wrap_model_call
def repair_orphan_tool_calls(request, handler):
    answered = {m.tool_call_id for m in request.messages if isinstance(m, ToolMessage)}
    fixed, pending = [], []

    def flush():
        # 빠진 결과는 그 AIMessage 뒤에 이어지는 ToolMessage들의 끝에 넣어야 순서가 맞습니다
        for tc in pending:
            fixed.append(ToolMessage(
                content=f"{tc['name']} 결과가 담당자 전환(handoff)으로 전달되지 않았습니다. 필요하면 다시 호출하세요.",
                tool_call_id=tc["id"], name=tc["name"]))
        pending.clear()

    for m in request.messages:
        if not isinstance(m, ToolMessage):
            flush()
        fixed.append(m)
        if isinstance(m, AIMessage) and m.tool_calls:
            pending.extend(tc for tc in m.tool_calls if tc["id"] not in answered)
    flush()

    if len(fixed) != len(request.messages):
        request = request.override(messages=fixed)
    return handler(request)


# ---------- 동등한 Agent 3개 (위아래 없음) ----------
news_collector = create_agent(
    llm(), tools=[search_news, to_process, to_market], name="news_collector",
    middleware=[repair_orphan_tool_calls],
    system_prompt=(COMMON +
        "너는 최신뉴스 수집가다. search_news를 2~3번(업황·메모리/HBM·파운드리 등) 돌려 핵심 기사만 골라라.\n"
        "기사마다 한 줄 요약과 날짜·언론사를 남기고, 해석은 하지 말고 process_expert에게 넘겨라."),
)
process_expert = create_agent(
    llm(), tools=[process_checklist, to_news, to_market], name="process_expert",
    middleware=[repair_orphan_tool_calls],
    system_prompt=(COMMON +
        "너는 반도체 공정 전문가다. process_checklist 항목으로 수집된 뉴스를 기술 관점에서 평가하라.\n"
        "기술적 강점·리스크를 근거 기사와 함께 정리하고, 뉴스가 부족할 때만 news_collector에게 되묻는다.\n"
        "정리가 끝나면 market_analyst에게 넘겨라. 주가 전망은 직접 하지 않는다."),
)
market_analyst = create_agent(
    llm(), tools=[get_stock_trend, to_news, to_process], name="market_analyst",
    middleware=[repair_orphan_tool_calls],
    system_prompt=(COMMON +
        "너는 증시 분석가이자 최종 정리 담당이다. get_stock_trend로 주요 종목 흐름을 확인하라.\n"
        "뉴스·공정 평가와 주가 흐름이 서로 맞는지 따져 보고, 낙관/기본/비관 시나리오를 '어떤 조건이면' 형태로 제시하라.\n"
        "확률·목표가·PER·배당률·매수 비중처럼 도구 결과에 없는 숫자와 매매 권유는 쓰지 말고, 1페이지 분량으로 정리하라.\n"
        "앞 담당자 분석이 이미 있으면 다시 넘기지 말고 직접 최종 답을 써라. 투자 권유가 아님을 밝힌다."),
)

# ---------- Swarm 조립: 관리자 없이 처음 받을 Agent만 정합니다 ----------
app = create_swarm(
    [news_collector, process_expert, market_analyst],
    default_active_agent="news_collector",
).compile(checkpointer=InMemorySaver())


printed_ids = set()   # Agent 노드는 대화 전체를 업데이트로 돌려주므로, 이미 출력한 메시지는 건너뜁니다

def chat(question, config):
    print(f"\n[사용자] {question}")
    final = ""
    for ns, chunk in app.stream({"messages": [("user", question)]}, config,
                                stream_mode="updates", subgraphs=True):
        for node, update in chunk.items():
            who = ns[0].split(":")[0] if ns else node
            for m in (update or {}).get("messages", []):
                key = (bool(ns), m.id)
                if m.id and key in printed_ids:
                    continue
                printed_ids.add(key)
                if ns:
                    for tc in getattr(m, "tool_calls", None) or []:
                        print(f"  [{who}] 도구: {tc['name']}({tc.get('args', {})})")
                elif m.type == "ai" and get_text(m):
                    final = f"[{who}] {get_text(m)}"
                    print(f"  [{who}] {get_text(m)[:150]}...")
    print(f"\n===== 최종 답변 =====\n{final}")
    print(f"\n  => 지금 대화 중인 Agent: {app.get_state(config).values.get('active_agent')}")

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "semi-001"}, "recursion_limit": 40}
    chat("앞으로 6~12개월 반도체 업황과 삼성전자·SK하이닉스 주가 전망을 따져봐줘. 근거와 리스크도 같이. 주가 차트 데이트도 다 가져와", config)
    # 두 번째 질문은 마지막 Agent(보통 market_analyst)가 먼저 받고, 공정 질문이라 process_expert로 넘깁니다
    # chat("HBM 공정 쪽 리스크만 좀 더 자세히 봐줘.", config)
