# tool_decision.py - 모델의 도구 호출 "결정" 확인
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_aws import ChatBedrockConverse

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """두 정수 a와 b를 입력받아 곱을 반환한다. 정확한 산술 계산이 필요할 때 사용."""
    return a * b

@tool
def search_employee(name: str) -> str:
    """삼성SDS 임직원 디렉터리에서 이름으로 직원 정보를 조회한다."""
    # 교육용 더미 데이터입니다
    fake_db = {
        "김하늘": "김하늘 / 클라우드운영팀 / haneul.kim@samsungsds.example.com",
        "박도윤": "박도윤 / 물류플랫폼팀 / doyun.park@samsungsds.example.com",
    }
    return fake_db.get(name, f"{name}을(를) 찾을 수 없습니다.")

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
    return "\n".join(
        f"- {s['name']} ({s['category']}, 평점 {s['rating']}) {s['url']} : {s['feature']}"
        for s in results
    )

# bind_tools: 모델에게 "이런 도구들이 있다"고 알려줍니다
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)
llm_with_tools = llm.bind_tools([multiply, search_employee, search_travel_sites])

queries = [
    "1234567 곱하기 8901234 계산해줘.",              # 단일 도구
    "김하늘 찾아서 이메일 알려주고 15 곱하기 25도.",  # 복합 (도구 2개)
    "일본 여행 항공권이랑 숙소 사이트 찾아줘.",       # 같은 도구 2번 호출
    "그냥 안녕이라고만 인사해줘.",                    # 도구 불필요
]

# 모델이 고른 도구 이름으로 실제 함수를 찾기 위한 표
tools_by_name = {t.name: t for t in [multiply, search_employee, search_travel_sites]}

for q in queries:
    print(f"[질문] {q}")
    messages = [HumanMessage(q)]

    # 1단계: 모델이 호출할 도구를 "결정" (아직 실행 전)
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print(f"  -> 직접 응답: {response.content}\n")
        continue

    # 2단계: 우리 코드가 도구를 실제로 "실행"하고 결과를 ToolMessage로 붙임
    for call in response.tool_calls:
        print(f"  -> 호출 결정: {call['name']}({call['args']})")
        tool_message = tools_by_name[call["name"]].invoke(call)
        print(f"     실행 결과: {tool_message.content}")
        messages.append(tool_message)

    # 3단계: 도구 실행 결과를 보고 모델이 최종 답변 작성
    final = llm_with_tools.invoke(messages)
    print(f"  -> 최종 답변: {final.content}\n")