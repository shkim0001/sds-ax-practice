# Graph Report - day5_practice  (2026-11-06)

## Corpus Check
- Corpus is ~1,339 words - fits in a single context window. You may not need a graph.

## Summary
- 74 nodes · 105 edges · 9 communities (2 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Interrupt Approval Graph
- PII Masking Middleware
- Logging Middleware
- Middleware Order Tags
- Hook Trace Middleware
- Shared get_text Helpers
- Employee Search Tool A
- Employee Search Tool B

## God Nodes (most connected - your core abstractions)
1. `TagMiddleware` - 7 edges
2. `HookTraceMiddleware` - 6 edges
3. `LoggingMiddleware` - 6 edges
4. `State` - 5 edges
5. `mask_message_content()` - 4 edges
6. `MaskingMiddleware` - 4 edges
7. `search_employee()` - 3 edges
8. `get_text()` - 3 edges
9. `propose_action()` - 3 edges
10. `human_approval()` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (9 total, 7 thin omitted)

### Community 0 - "Interrupt Approval Graph"
Cohesion: 0.16
Nodes (6): execute(), get_text(), human_approval(), main(), propose_action(), State

### Community 2 - "PII Masking Middleware"
Cohesion: 0.25
Nodes (4): get_text(), mask_message_content(), mask_pii(), MaskingMiddleware

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TagMiddleware` connect `Middleware Order Tags` to `Agent Scripts & Imports`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `LoggingMiddleware` connect `Logging Middleware` to `Agent Scripts & Imports`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `HookTraceMiddleware` connect `Hook Trace Middleware` to `Agent Scripts & Imports`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._