| round | change (one line) | val | test | train | n (val/test/train) | $/run (list) | spend (list) |
|---|---|---|---|---|---|---|---|
| 0 | baseline (levers at 7354c90) | 0.652 (partial) | - | 0.649 (partial) | 4/0/9 | 1.50 | 19.46 |
| 1 | define "adjacent" in answering style | - | - | - | 0/0/0 | - | - |

Status 2026-10-11 03:50 BST: eval runs paused for the merge swarm's 25% reserve of the shared 5 h window (lead decision, 03:30). They resume after the 07:50 reset, with the baseline and v1 run side by side on val and test. Stop at 11:00 BST or at 40% weekly.

v1 targets the behaviour seen in all 11 baseline train replies: content next to the question (history, fit results, other runs, upstream comparisons, cost) and reports of the agent's own checks. `direct` fails in 10 of 11 and `no_commentary` in 8 of 11. The analyzer bounds the gain at about +0.24 on the train mean and expects +0.08 to +0.12.

"$/run" and "spend" are list-price equivalents reported by claude -p (`total_cost_usd`). Runs bill to the Claude subscription, not to an API key.
