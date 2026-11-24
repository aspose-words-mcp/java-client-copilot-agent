# Showcase run metrics

| Check | Status |
| --- | --- |
| Runtime behavior | Not checked |

| Metric | Count |
| --- | ---: |
| Selected questions | 99 |
| Attempted questions | 99 |
| Completed answers | 99 |
| Failed/incomplete generations | 0 |
| Remaining questions | 0 |
| Generated answers completed without repair | 83 |
| Compilation passed on first attempt | 74 |
| Compilation passed after repair | 16 |
| Repair requests | 16 |
| Generation retries | 1 |
| Saved-answer replays | 0 |
| Distinct known models | 2 |

Question outcomes, model counts, and repair counts describe the latest attempt per question; duration includes all saved sessions.

Run interrupted: no.
Total duration: 4786.20 seconds. Average per attempted question: 48.35 seconds.

## Compilation

| Status | Questions |
| --- | ---: |
| passed | 90 |
| failed | 0 |
| no_code | 9 |
| not_run | 0 |
| unavailable | 0 |
| timeout | 0 |
| incomplete | 0 |

No-code and unchecked answers are not compilation successes.

## Models

Counts are distinct questions per model and role; one question can use multiple models. Unknown identities are not counted as known models.

| Model | Generation questions | Repair questions |
| --- | ---: | ---: |
| gpt-6-luna | 70 | 15 |
| mai-code-2-flash | 29 | 1 |

## Exceptions

None.
