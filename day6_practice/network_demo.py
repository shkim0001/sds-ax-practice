# network_demo.py - 관리자 없이 Agent끼리 직접 넘기는 Network(Swarm) 구조
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_handoff_tool, create_swarm

load_dotenv()
MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

def llm():
    return ChatBedrockConverse(model=MODEL, region_name="us-east-1", temperature=0)

def get_text(message):
    """content가 블록 리스트면 text만 모아 반환합니다."""
    c = message.content
    return "".join(b.get("text", "") for b in c if isinstance(b, dict)) if isinstance(c, list) else (c or "")

# 교육용 더미 도구입니다
@tool
def reset_vpn(user: str) -> str:
    """사용자의 VPN 계정을 초기화한다."""
    return f"[IT] {user}님의 VPN 계정을 초기화했습니다. 10분 뒤 다시 접속하세요."

@tool
def check_leave(user: str) -> str:
    """사용자의 남은 연차 일수를 조회한다."""
    return f"[HR] {user}님의 남은 연차는 7일입니다."

@tool
def apply_remote_work(user: str, date: str) -> str:
    """재택근무를 신청한다. date는 YYYY-MM-DD."""
    return f"[HR] {user}님의 {date} 재택근무 신청이 접수됐습니다."

# 1) handoff 도구: 누구에게 넘길 수 있는지를 각 Agent가 직접 들고 있습니다
to_it = create_handoff_tool(agent_name="it_agent",
                            description="VPN, 노트북, 계정 등 IT 문제는 it_agent에게 넘긴다.")
to_hr = create_handoff_tool(agent_name="hr_agent",
                            description="연차, 재택근무, 인사 규정 질문은 hr_agent에게 넘긴다.")

# 2) 동등한 Agent 3개 (위아래 없음)
reception = create_agent(
    llm(), tools=[to_it, to_hr], name="reception",
    system_prompt=("너는 사내 헬프데스크 접수 담당이다. 직접 처리하지 말고\n"
                   "IT 문제는 it_agent, 인사 문제는 hr_agent에게 넘겨라."),
)
it_agent = create_agent(
    llm(), tools=[reset_vpn, to_hr], name="it_agent",
    system_prompt=("너는 IT 헬프데스크 담당이다. IT 문제만 도구로 처리하라.\n"
                   "인사 관련 요청이 나오면 직접 답하지 말고 hr_agent에게 넘겨라."),
)
hr_agent = create_agent(
    llm(), tools=[check_leave, apply_remote_work, to_it], name="hr_agent",
    system_prompt=("너는 인사 담당이다. 연차와 재택근무만 도구로 처리하라.\n"
                   "IT 관련 요청이 나오면 직접 답하지 말고 it_agent에게 넘겨라."),
)

# 3) Swarm 조립: 관리자 노드 없이, 처음 받을 Agent만 정합니다
#    checkpointer가 '지금 대화 중인 Agent(active_agent)'를 기억합니다
app = create_swarm(
    [reception, it_agent, hr_agent],
    default_active_agent="reception",
).compile(checkpointer=InMemorySaver())

printed_ids = set()   # 이미 출력한 메시지 id. Agent 노드는 대화 전체를 업데이트로 돌려주므로 중복 출력을 막습니다

def chat(question, config):
    print(f"\n[사용자] {question}")
    for ns, chunk in app.stream({"messages": [("user", question)]}, config,
                                stream_mode="updates", subgraphs=True):
        for node, update in chunk.items():
            who = ns[0].split(":")[0] if ns else node   # 서브그래프 안이면 경로에서 Agent 이름을 꺼냅니다
            for m in (update or {}).get("messages", []):
                key = (bool(ns), m.id)                  # 서브그래프(도구 호출)와 상위(답변) 출력은 따로 셉니다
                if m.id and key in printed_ids:
                    continue
                printed_ids.add(key)
                if ns:
                    for tc in getattr(m, "tool_calls", None) or []:
                        print(f"  [{who}] 도구: {tc['name']}")
                elif m.type == "ai" and get_text(m):
                    print(f"  [{who}] {get_text(m)[:120]}")
    print(f"  => 지금 대화 중인 Agent: {app.get_state(config).values.get('active_agent')}")

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "emp-001"}, "recursion_limit": 25}
    chat("김하늘인데 VPN이 안 붙어요.", config)                 # reception → it_agent
    chat("그리고 남은 연차도 알려주세요.", config)               # it_agent → hr_agent (직접)
    chat("그럼 2026-11-20 재택근무도 신청해 주세요.", config)     # hr_agent가 바로 처리