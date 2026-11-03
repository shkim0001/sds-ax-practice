# travel_tool.py - 여행 사이트 검색 mock 도구
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_aws import ChatBedrockConverse

load_dotenv()

# 교육용 더미 데이터입니다. 실제 사이트가 아닙니다.
FAKE_TRAVEL_SITES = [
    {"name": "하늘길항공권", "url": "https://skyroad.example.com", "category": "항공권",
     "regions": ["일본", "동남아", "유럽"], "rating": 4.5, "feature": "특가 항공권 알림"},
    {"name": "바다호텔스", "url": "https://seahotels.example.com", "category": "숙소",
     "regions": ["제주", "일본", "동남아"], "rating": 4.3, "feature": "무료 취소 객실 다수"},
    {"name": "온누리패키지", "url": "https://onnuri-tour.example.com", "category": "패키지",
     "regions": ["유럽", "동남아"], "rating": 4.1, "feature": "가이드 동행 패키지"},
    {"name": "제주한바퀴", "url": "https://jeju-round.example.com", "category": "렌터카",
     "regions": ["제주"], "rating": 4.6, "feature": "완전자차 보험 포함"},
    {"name": "도쿄마실", "url": "https://tokyo-masil.example.com", "category": "투어",
     "regions": ["일본"], "rating": 4.4, "feature": "현지 일일 투어 예약"},
]


@tool
def search_travel_sites(destination: str, category: str = "전체") -> str:
    """여행지와 분류로 여행 예약 사이트를 검색한다.

    destination: 여행지. 예: '제주', '일본', '동남아', '유럽'
    category: '항공권', '숙소', '패키지', '렌터카', '투어', '전체' 중 하나
    """
    results = [
        site for site in FAKE_TRAVEL_SITES
        if destination in site["regions"]
        and (category == "전체" or site["category"] == category)
    ]
    if not results:
        return f"'{destination}' / '{category}' 조건에 맞는 여행 사이트를 찾지 못했습니다."

    results.sort(key=lambda s: s["rating"], reverse=True)
    lines = [
        f"- {s['name']} ({s['category']}, 평점 {s['rating']}) {s['url']} : {s['feature']}"
        for s in results
    ]
    return "\n".join(lines)


tools = {"search_travel_sites": search_travel_sites}

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0,
)
llm_with_tools = llm.bind_tools(list(tools.values()))

queries = [
    "제주도 렌터카 예약할 만한 사이트 알려줘.",
    "일본 여행 가는데 항공권이랑 숙소 사이트 둘 다 추천해줘.",
    "여행 가기 좋은 계절이 언제야?",  # 도구 불필요
]

for q in queries:
    print(f"[질문] {q}")
    messages = [HumanMessage(q)]

    # 1단계: 모델이 도구 호출을 "결정"
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print(f"  -> 직접 응답: {response.content}\n")
        continue

    # 2단계: 우리 코드가 도구를 "실행"하고 결과를 ToolMessage로 돌려줌
    for call in response.tool_calls:
        print(f"  -> 호출 결정: {call['name']}({call['args']})")
        tool_message = tools[call["name"]].invoke(call)
        print(f"     실행 결과:\n{tool_message.content}")
        messages.append(tool_message)

    # 3단계: 도구 결과를 보고 모델이 최종 답변 작성
    final = llm_with_tools.invoke(messages)
    print(f"  -> 최종 답변: {final.content}\n")
