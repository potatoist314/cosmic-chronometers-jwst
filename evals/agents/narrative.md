| round | change (one line) | val (n=12) | test | train | correct (val) | pass (val) | s/run | tool calls | $/run (list) | spend (list) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | baseline (levers at 7354c90) | 0.683 ±0.081 | 0.608 ±0.118 (n=9) | 0.649 ±0.107 (n=9) | 1.00 | 1.00 | 126 | 10.8 | 1.17 | 39.36 |
| 1 | define "adjacent" in answering style | 0.689 ±0.083 | 0.561 ±0.185 (n=5) | - | 0.92 | 0.92 | 112 (0.9×) | 8.8 (0.8×) | 1.12 (1.0×) | 58.45 |

1 trial per case. ± is the 95% t interval over cases. Perf columns are means over the 17 cases both variants ran. No delta clears noise: v1 − baseline on val is +0.006 ±0.036 (paired, n=12), and on test it is −0.043 ±0.276 (paired, n=5).

Best: round 0 (baseline). Stopped at 09:20 BST on quota. The shared 5 h window fell below the merge swarm's 25% reserve at about 08:40 and resets at 12:50, after the 11:00 stop time.

**Recommended change:** none. v1 did not change what it targeted. Mean reply length is 186 words at baseline and 201 with v1 (paired word ratio 0.99). `direct` is 0 in all 17 paired cases in both variants, and replies that open with a process line are 5/26 at baseline and 4/17 with v1.

**Versus baseline:** on val, 0.683 → 0.689 (n=12). On test, 0.604 → 0.561 on the 5 cases both ran. `correct` lost one case (val st05). The judge's own reason calls that call borderline: it says the formula "actually agrees" with the key, but it failed the reply for missing the key's notebook and grid paths.

**Why trust this:** the judge fails 12/12 planted wrong or empty replies and agrees with hand labels on 52/60 items. The levers are wired: both variants run `sync_wiki_direction.py --read` on st06, a rule only AGENTS.md states, and the v1 skill text appears in the v1 traces.

**What else was tried:** nothing. The quota allowed one round.
