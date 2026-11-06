# Day 4: 자산 조회 도구는 장애를 어떻게 견디나? {#day04-recovery}

`get_asset_status`는 예외를 던지지 않습니다. 실패를 세 종류로 갈라 백엔드를 **최대 3번**까지만 부르고, 그래도 안 되면 `get_asset_status_backup` 캐시 값으로 답합니다.

- 타임아웃은 다시 물으면 답이 달라질 수 있어서 짧게 재시도합니다.[](source:readme)
- 스키마 오류나 없는 자원은 몇 번을 물어도 같아서 1번 만에 대체 경로로 넘어갑니다.
- 대체 경로로 답할 때는 반환 문자열에 `get_asset_status_backup` 이름과 실패 분류를 남깁니다.
- 반환값과 로그에 나가는 모든 문자열은 `_redact`를 거쳐 토큰이 지워집니다.[](source:submission)

@answer scope="day04 starter/submission.py 현재 작업본 · 로컬 채점 10/10 · eval_set.json 문항은 아직 없음"
@meta locale=ko
@source readme title="day04 README: 과제 요구사항과 채점 기준" path=sds-ax-training/day04/README.md
@source submission title="day04 submission.py 구현" path=sds-ax-training/day04/practice/starter/submission.py
@source tests title="day04 공개 테스트" path=sds-ax-training/day04/tests/test_submission.py

## 호출 한 번은 어떤 길을 지나나? {#flow}

@diagram workflow id=recovery-flow source=asset-status.workflow.json title="get_asset_status 재시도·폴백 흐름"

@steps id=flow-steps
| s-validate | asset_id 검증 | 빈 ID면 백엔드를 부르지 않고 등록된 ID 목록을 안내합니다. | recovery-flow | validate |
| s-fetch | fetch(asset_id) | 외부 백엔드를 부릅니다. 첫 시도와 재시도를 합쳐 3번을 넘지 않습니다. | recovery-flow | fetch |
| s-classify | classify_failure | 예외 타입과 메시지로 retryable, backoff, fatal 중 하나를 고릅니다. | recovery-flow | classify |
| s-wait | 대기 후 재시도 | retryable은 0.05초, backoff는 0.2초 다음 0.4초를 쉬고 다시 부릅니다. | recovery-flow | wait |
| s-backup | get_asset_status_backup | fatal이거나 3번을 다 쓰면 캐시에서 값을 꺼냅니다. | recovery-flow | backup |
| s-fbreply | 폴백 안내 문자열 | 경로 이름, 분류, 호출 횟수, 캐시라는 경고를 함께 돌려줍니다. | recovery-flow | fbreply |
| s-ok | 정상 응답 | 재시도 끝에 성공하면 되살아난 응답을 그대로 씁니다. | recovery-flow | ok |

## 실패 종류마다 무엇이 달라지나? {#classes}

| 분류 | 판정 근거 | 대응 | 백엔드 호출 |
| --- | --- | --- | --- |
| retryable | `TimeoutError`, `ConnectionError`, 판정이 안 되는 오류 | 0.05초 쉬고 재시도 | 3번 {good:채점 2~3번} |
| backoff | 메시지에 429, rate limit, too many requests | 0.2초, 0.4초로 간격을 늘려 재시도 | 3번 |
| fatal | `LookupError`, `ValueError`, 권한·스키마·not found | 재시도 없이 즉시 대체 경로 | 1번 {good:채점 1번 이하} |

@callout level=note title="판정 순서"
backoff 키워드를 가장 먼저 봅니다. 429 메시지를 담은 `RuntimeError`가 retryable로 새지 않게 하려는 순서입니다.
그다음 예외 타입으로 fatal과 retryable을 가르고, 타입으로 모르면 메시지 키워드를 봅니다.

## 실제로 어떤 문자열이 돌아오나? {#outputs}

```text title="정상 조회: get_asset_status('SRV-001')"
[자산 SRV-001] name: payment-api-prod-01, status: running, owner: pay-be
```

```text title="1번 타임아웃 후 성공 (백엔드 2번 호출)"
[자산 SRV-001] name: recovered, status: running, owner: x (재시도 1회 후 성공)
```

```text title="계속 타임아웃 (백엔드 3번 호출)"
기본 조회 경로가 실패했어요 (분류: retryable, 호출 3회, 마지막 오류 TimeoutError: timed out). 대체 경로 get_asset_status_backup 결과로 답합니다. 캐시 값이라 현재 상태와 다를 수 있어요.
[get_asset_status_backup · 캐시] 자산 SRV-001: name: payment-api-prod-01, status: running, owner: pay-be
```

```text title="스키마 오류 (백엔드 1번 호출)"
기본 조회 경로가 실패했어요 (분류: fatal, 호출 1회, 마지막 오류 ValueError: schema validation failed: field 'status' missing). 대체 경로 get_asset_status_backup 결과로 답합니다. 캐시 값이라 현재 상태와 다를 수 있어요.
[get_asset_status_backup · 캐시] 자산 SRV-002: name: auth-service-prod-01, status: degraded, owner: iam
```

토큰이 든 오류 메시지를 넣어 보면 반환값과 로그 모두 `Bearer [REDACTED]`로 바뀝니다.

## MCP로 내보내는 세 도구는 언제 쓰나? {#tools}

| 도구 | 쓸 때 | 쓰지 말 때 | 인자 |
| --- | --- | --- | --- |
| `search_runbook` | 무엇부터 확인해야 하나 | 담당자, 과거 장애, 자산 상태 | `symptom`: 5xx, oom, cert |
| `get_service_owner` | 누구에게 연락하나 | 원인이나 대응 절차 찾기 | `service`: payment-api 등 |
| `query_recent_incidents` | 비슷한 장애가 있었나 | 현재 상태나 담당자 | `service`: payment-api 등 |

없는 값을 넣으면 예외 대신 쓸 수 있는 값을 알려 줍니다. 예: `등록되지 않은 증상 키워드예요: 'disk'. 쓸 수 있는 값: 5xx, cert, oom`

## 채점 결과는? {#grade}

@facts
| 기초 파트 | 7 / 7 (도구 명세, 호출 동작, 장애 복구, 재시도, 확장 검사) |
| 심화 파트 | 3 / 3 (분류 결정성, fatal 즉시 폴백, retryable 재시도) |
| 공개 테스트 | 8개 모두 통과[](source:tests) |
| 확인 명령 | `python scripts/grade.py --day 4` |

## 제출 전에 무엇이 남았나? {#todo}

- [ ] 저장소 루트 `eval_set.json`에 `tool_recovery` 유형 문항을 `d4-01`, `d4-02`로 2개 이상 추가
- [ ] `day04/mcp_server.py`가 인자 설명까지 넘기도록 보강할지 결정
- [ ] `submission.py`와 `mcp_server.py`를 커밋에 포함
- [ ] `git tag day04-submit` 후 태그까지 push
