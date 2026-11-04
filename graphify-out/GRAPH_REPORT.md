# Graph Report - sds-ax-practice  (2026-11-04)

## Corpus Check
- 117 files · ~97,429 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: .bin 4, (none) 3, .sqlite3 1)

## Summary
- 771 nodes · 1202 edges · 53 communities (35 shown, 18 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.86)
- Token cost: 345,221 input · 0 output

## Community Hubs (Navigation)
- Day5-6 가드레일·Supervisor 문서
- 교육 규약·Day1-4 미션 문서
- LangGraph 조건 분기 실습
- 채점 스크립트·Day5 starter
- sds_testkit 가짜 모델
- Day1 공개 테스트
- Day2 공개 테스트
- Day3 공개 테스트
- Day4 운영 도구 starter
- Day4 공개 테스트
- Day7 공개 테스트
- Day2 RAG starter
- Day7 계측·평가 starter
- Day5 공개 테스트
- Day3 에이전트 starter
- Day6 공개 테스트
- Day1-7 미션 맵
- Day1 분류 체인 starter
- Day2 청킹·검색 실습
- Day1 LCEL 실습
- 제출물 로더 fixture
- conftest·환경 점검
- CI 채점 단계
- LangGraph 순환 실습
- CI self-check 잡
- Day2 RAG 체인 실습
- 제출·채점 흐름도
- grade.yml 설정
- Day1 도구 호출 실습
- 체인 한계 실습
- 조건 분기 그래프 그림
- 멀티턴 대화 기록
- Day8 테스트 템플릿
- Day9 테스트 템플릿
- Day10 테스트 템플릿
- CI 수동 실행 입력
- Day4 MCP 서버
- ReAct 도구 정의
- CI 변경 Day 감지
- CI 트리거
- Hello 그래프 그림
- Day8 starter 템플릿
- Day9 starter 템플릿
- Day10 starter 템플릿
- CI 환경 변수
- 여행 사이트 검색 도구
- 재택근무 규정
- 출장 규정
- 코사인 유사도
- Day2 get_text
- Day3 get_text
- sds-ax-training 루트

## God Nodes (most connected - your core abstractions)
1. `need()` - 62 edges
2. `ScriptedChatModel` - 28 edges
3. `load_submission()` - 18 edges
4. `Day 5. 승인 게이트와 가드레일` - 13 edges
5. `Day 7. 계측과 누적 평가` - 12 edges
6. `Day 6. Supervisor 인시던트 대응팀` - 11 edges
7. `FakeVectorStore` - 10 edges
8. `load_eval_set()` - 9 edges
9. `_run()` - 9 edges
10. `Failing` - 9 edges

## Surprising Connections (you probably didn't know these)
- `연차 규정 (day2_practice)` --semantically_similar_to--> `연차 휴가 규정 (sds-ax-training)`  [INFERRED] [semantically similar]
  day2_practice/docs/leave_policy.md → sds-ax-training/day02/practice/docs/leave_policy.md
- `연차 이월 (5일, 6월 말까지)` --semantically_similar_to--> `연차 이월 (최대 5일, 6개월 이내)`  [INFERRED] [semantically similar]
  day2_practice/docs/leave_policy.md → sds-ax-training/day02/practice/docs/leave_policy.md
- `requirements.txt (practice root)` --semantically_similar_to--> `requirements.txt (sds-ax-training)`  [INFERRED] [semantically similar]
  requirements.txt → sds-ax-training/requirements.txt
- `dayNN-submit 태그 기반 제출` --semantically_similar_to--> `[제출] 커밋 메시지 규칙`  [AMBIGUOUS] [semantically similar]
  sds-ax-training/day05/README.md → sds-ax-training/docs/STUDENT_GUIDE.md
- `test_컨텍스트_주입()` --uses--> `ScriptedChatModel`  [INFERRED]
  sds-ax-training/day02/tests/test_submission.py → sds-ax-training/sds_testkit.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **LLM 위의 결정적 규칙 게이트 패턴 (Day1~4 심화)** — sds_ax_training_day01_readme_apply_severity_rules, sds_ax_training_day02_readme_assess_retrieval, sds_ax_training_day03_readme_should_stop, sds_ax_training_day04_readme_classify_failure [INFERRED 0.85]
- **Day 2 RAG 실습 문서 코퍼스** — sds_ax_training_day02_practice_docs_incident_runbook, sds_ax_training_day02_practice_docs_leave_policy, sds_ax_training_day02_practice_docs_oncall_policy, sds_ax_training_day02_readme_build_chunks [INFERRED 0.85]
- **HR 규정 더미 문서 (인사 포털 양식 신청)** — day2_practice_docs_leave_policy, day2_practice_docs_remote_work_policy, day2_practice_docs_travel_policy [INFERRED 0.85]
- **차단-정제-검증-기록 미들웨어 파이프라인** — sds_ax_training_day05_readme_inputguardmiddleware, sds_ax_training_day05_readme_maskingmiddleware, sds_ax_training_day05_readme_outputcheckmiddleware, sds_ax_training_day05_readme_loggingmiddleware [EXTRACTED 1.00]
- **Supervisor 인시던트 대응팀** — sds_ax_training_day06_readme_build_supervisor, sds_ax_training_day06_readme_route_question, sds_ax_training_day06_readme_log_agent, sds_ax_training_day06_readme_metric_agent, sds_ax_training_day06_readme_runbook_agent, sds_ax_training_day06_readme_judge_output [EXTRACTED 1.00]
- **계측, 누적 평가, 회귀 비교 루프** — sds_ax_training_day07_readme_tracecollector, sds_ax_training_day07_readme_run_eval, sds_ax_training_day07_readme_compare_eval, sds_ax_training_docs_student_guide_eval_set_json, sds_ax_training_day07_growth [INFERRED 0.85]
- **Conditional branch flow from classify to end** — hello_conditionnal_graph_classify, hello_conditionnal_graph_answer_question, hello_conditionnal_graph_react_exclaim, hello_conditionnal_graph_end [EXTRACTED 1.00]
- **Linear LangGraph flow: start -> respond -> end** — hello_graph_start, hello_graph_respond, hello_graph_end [EXTRACTED 1.00]
- **Five-step submission and grading pipeline** — sds_ax_training_docs_assets_grading_flow_read_mission, sds_ax_training_docs_assets_grading_flow_fill_todo, sds_ax_training_docs_assets_grading_flow_self_check, sds_ax_training_docs_assets_grading_flow_commit_push, sds_ax_training_docs_assets_grading_flow_auto_grading [EXTRACTED 1.00]
- **Assignment score structure (7 basic + 3 advanced, 80-point completion)** — sds_ax_training_docs_assets_grading_flow_basic_part, sds_ax_training_docs_assets_grading_flow_advanced_part, sds_ax_training_docs_assets_grading_flow_completion_criteria [EXTRACTED 1.00]
- **Day 1-7 layered mission sequence building one system** — sds_ax_training_docs_assets_mission_map_day1_alarm_triage, sds_ax_training_docs_assets_mission_map_day2_runbook_rag, sds_ax_training_docs_assets_mission_map_day3_investigation_agent, sds_ax_training_docs_assets_mission_map_day4_mcp_server, sds_ax_training_docs_assets_mission_map_day5_approval_gate, sds_ax_training_docs_assets_mission_map_day6_supervisor, sds_ax_training_docs_assets_mission_map_day7_instrumentation_eval [EXTRACTED 1.00]
- **Advanced +3 tasks: deterministic verification of LLM judgment** — sds_ax_training_docs_assets_mission_map_adv_deterministic_rules, sds_ax_training_docs_assets_mission_map_adv_retrieval_quality_judgment, sds_ax_training_docs_assets_mission_map_adv_call_budget, sds_ax_training_docs_assets_mission_map_adv_error_classification, sds_ax_training_docs_assets_mission_map_adv_risk_policy, sds_ax_training_docs_assets_mission_map_adv_output_gating, sds_ax_training_docs_assets_mission_map_adv_regression_comparison, sds_ax_training_docs_assets_mission_map_deterministic_verification_principle [EXTRACTED 1.00]
- **Day 2 retrieval and Day 4 tools become Day 6 Supervisor tools** — sds_ax_training_docs_assets_mission_map_chroma_db, sds_ax_training_docs_assets_mission_map_mcp_server_py, sds_ax_training_docs_assets_mission_map_day6_supervisor [EXTRACTED 1.00]

## Communities (53 total, 18 thin omitted)

### Community 0 - "Day5-6 가드레일·Supervisor 문서"
Cohesion: 0.06
Nodes (51): Day 5 강의자료, 강의자료 권장 순서, Day 5. 승인 게이트와 가드레일, delete_asset, input_guard(text), InputGuardMiddleware, LoggingMiddleware, mask_pii(text) (+43 more)

### Community 1 - "교육 규약·Day1-4 미션 문서"
Cohesion: 0.06
Nodes (48): 연차 규정 (day2_practice), 연차 이월 (5일, 6월 말까지), 연차 신청서 양식 HR-103, requirements.txt (practice root), SDS AX 교육 저장소 작업 지침 (AGENTS.md), 배점 체계 (기초 7 + 심화 3, pass_score 7), submission.py 제출 진입점, 고정 기술 스택 (Bedrock Claude Sonnet 4.5, Titan Embed v2, Chroma, SqliteSaver) (+40 more)

### Community 2 - "LangGraph 조건 분기 실습"
Cohesion: 0.06
Nodes (15): answer_question(), classify(), ClassifyState, get_text(), react_exclaim(), route_by_intent(), respond(), State (+7 more)

### Community 3 - "채점 스크립트·Day5 starter"
Cohesion: 0.07
Nodes (10): input_guard(), load_public_sets(), mask_pii(), needs_approval(), append_step_summary(), grade(), GradePlugin, load_config() (+2 more)

### Community 4 - "sds_testkit 가짜 모델"
Cohesion: 0.07
Nodes (5): as_json(), CallCounter, FakeRetriever, make_docs(), tool_results_in()

### Community 5 - "Day1 공개 테스트"
Cohesion: 0.10
Nodes (9): test_병렬_조립(), test_스키마_계약(), test_심화_규칙의_결정성(), test_심화_깨진_출력_복구(), test_심화_파이프라인_연결(), test_역할_지정(), test_형식_지침_주입(), test_확장_검사_게이트() (+1 more)

### Community 6 - "Day2 공개 테스트"
Cohesion: 0.11
Nodes (13): load_eval_set(), _chain(), chunks(), sub(), test_메타데이터_상속(), test_심화_거절_경로(), test_심화_파이프라인_연결(), test_심화_판정의_결정성() (+5 more)

### Community 7 - "Day3 공개 테스트"
Cohesion: 0.13
Nodes (10): _run(), test_그래프_위상(), test_도구_정의_품질(), test_루프_완주(), test_심화_예산_준수(), test_심화_조기_종료(), test_심화_판정의_결정성(), test_연쇄() (+2 more)

### Community 8 - "Day4 운영 도구 starter"
Cohesion: 0.08
Nodes (6): classify_failure(), _default_fetch(), get_asset_status(), get_asset_status_backup(), get_service_owner(), query_recent_incidents()

### Community 9 - "Day4 공개 테스트"
Cohesion: 0.11
Nodes (9): Failing, test_도구_명세(), test_심화_fatal은_즉시_폴백(), test_심화_retryable은_재시도(), test_심화_분류의_결정성(), test_장애_복구(), test_재시도_실행(), test_호출_동작() (+1 more)

### Community 10 - "Day7 공개 테스트"
Cohesion: 0.13
Nodes (10): answer_ok(), sub(), test_계측(), test_심화_비교의_결정성(), test_심화_회귀_없음(), test_심화_회귀_탐지(), test_예외_격리(), test_집계_형식() (+2 more)

### Community 11 - "Day2 RAG starter"
Cohesion: 0.11
Nodes (10): _appears(), assess_retrieval(), build_chunks(), build_rag_chain(), _run(), build_retriever(), _default_llm(), format_docs() (+2 more)

### Community 12 - "Day7 계측·평가 starter"
Cohesion: 0.10
Nodes (3): compare_eval(), run_eval(), TraceCollector

### Community 13 - "Day5 공개 테스트"
Cohesion: 0.16
Nodes (9): need(), test_공격_차단(), test_마스킹(), test_미들웨어_순서(), test_심화_과차단_방지(), test_심화_이중_확인(), test_심화_정책의_결정성(), test_오탐_없음() (+1 more)

### Community 14 - "Day3 에이전트 starter"
Cohesion: 0.11
Nodes (5): build_agent(), _default_llm(), DeployArgs, get_deploy_history(), should_stop()

### Community 15 - "Day6 공개 테스트"
Cohesion: 0.15
Nodes (8): test_구성(), test_도구_격리(), test_라우팅_정확도(), test_라우팅_테스트셋(), test_심화_게이팅_결정성(), test_심화_저가치_억제(), test_심화_파이프라인_연결(), test_확장_검사_게이트()

### Community 16 - "Day1-7 미션 맵"
Cohesion: 0.14
Nodes (19): SDS AX Day 1~7 Mission Map (diagram), Advanced (Day 3): Call Budget, Advanced (Day 1): Deterministic Rules, Advanced (Day 4): Error Classification, Advanced (Day 6): Output Gating, Advanced (Day 7): Regression Comparison, Advanced (Day 2): Retrieval Quality Judgment, Advanced (Day 5): Risk Policy (+11 more)

### Community 18 - "Day1 분류 체인 starter"
Cohesion: 0.14
Nodes (8): apply_severity_rules(), build_full_chain(), safe_triage(), build_notice_chain(), build_triage_chain(), _default_llm(), get_text(), TriageResult

### Community 20 - "Day1 LCEL 실습"
Cohesion: 0.18
Nodes (3): Routing, tap(), InquiryAnalysis

### Community 21 - "제출물 로더 fixture"
Cohesion: 0.15
Nodes (6): load_submission(), sub(), sub(), sub(), sub(), sub()

### Community 23 - "CI 채점 단계"
Cohesion: 0.21
Nodes (12): steps, steps, id, if, name, run, shell, uses (+4 more)

### Community 24 - "LangGraph 순환 실습"
Cohesion: 0.25
Nodes (5): check_quality(), generate(), get_text(), QualityState, route_quality()

### Community 25 - "CI self-check 잡"
Cohesion: 0.20
Nodes (10): self-check, day, continue-on-error, if, name, needs, runs-on, strategy (+2 more)

### Community 27 - "제출·채점 흐름도"
Cohesion: 0.44
Nodes (8): Submission & Grading Flow Diagram (제출과 채점), Advanced Part (3 points), Step 5: Automatic Grading (hidden items + variant inputs), Basic Part (7 points, pass line), Step 4: Commit & Push ([제출] DayN), Step 2: Fill TODO (starter/submission.py), Step 1: Read Mission (dayNN/README.md), Step 3: Self-check (python grade.py --day N)

### Community 28 - "grade.yml 설정"
Cohesion: 0.25
Nodes (7): concurrency, cancel-in-progress, group, jobs, name, permissions, contents

### Community 29 - "Day1 도구 호출 실습"
Cohesion: 0.29
Nodes (3): multiply(), search_employee(), search_travel_sites()

### Community 30 - "체인 한계 실습"
Cohesion: 0.29
Nodes (3): build_prompt(), generate(), retrieve()

### Community 31 - "조건 분기 그래프 그림"
Cohesion: 0.33
Nodes (7): Hello Conditional Graph Diagram, answer_question node, classify node, Conditional Edge Routing, __end__ node, react_exclaim node, __start__ node

### Community 36 - "CI 수동 실행 입력"
Cohesion: 0.33
Nodes (6): default, description, options, required, type, day

### Community 39 - "CI 변경 Day 감지"
Cohesion: 0.40
Nodes (5): name, outputs, runs-on, detect-days, days

### Community 40 - "CI 트리거"
Cohesion: 0.40
Nodes (5): on, push, workflow_dispatch, branches, inputs

### Community 41 - "Hello 그래프 그림"
Cohesion: 0.83
Nodes (4): Hello Graph (LangGraph diagram), __end__ node, respond node, __start__ node

### Community 45 - "CI 환경 변수"
Cohesion: 0.50
Nodes (4): BEFORE_SHA, EVENT_NAME, SELECTED_DAY, env

### Community 47 - "재택근무 규정"
Cohesion: 0.67
Nodes (3): 재택근무 규정, 재택근무 신청서 양식 RW-201, 재택근무 보안 수칙 (VPN 필수)

### Community 48 - "출장 규정"
Cohesion: 0.67
Nodes (3): 출장 규정, 출장 경비 한도 및 정산, 출장 신청서 양식 TR-102

## Ambiguous Edges - Review These
- `[제출] 커밋 메시지 규칙` → `dayNN-submit 태그 기반 제출`  [AMBIGUOUS]
  sds-ax-training/day05/README.md · relation: semantically_similar_to

## Knowledge Gaps
- **26 isolated node(s):** `sds-ax-training`, `연차 신청서 양식 HR-103`, `재택근무 신청서 양식 RW-201`, `재택근무 보안 수칙 (VPN 필수)`, `출장 신청서 양식 TR-102` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 331 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `need()` connect `Day5 공개 테스트` to `Day1 공개 테스트`, `Day2 공개 테스트`, `Day3 공개 테스트`, `Day4 공개 테스트`, `Day7 공개 테스트`, `Day6 공개 테스트`, `제출물 로더 fixture`, `conftest·환경 점검`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `ScriptedChatModel` (e.g. with `test_병렬_조립()` and `test_심화_깨진_출력_복구()`) actually correct?**
  _`ScriptedChatModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `sds-ax-training`, `연차 신청서 양식 HR-103`, `재택근무 신청서 양식 RW-201` to the rest of the system?**
  _26 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Day5-6 가드레일·Supervisor 문서` be split into smaller, more focused modules?**
  _Cohesion score 0.05552617662612375 - nodes in this community are weakly interconnected._
- **Why does `ScriptedChatModel` connect `Day1 공개 테스트` to `Day6 공개 테스트`, `sds_testkit 가짜 모델`, `Day2 공개 테스트`, `Day3 공개 테스트`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `교육 규약·Day1-4 미션 문서` be split into smaller, more focused modules?**
  _Cohesion score 0.05957767722473605 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `[제출] 커밋 메시지 규칙` and `dayNN-submit 태그 기반 제출`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._