# Metrics

Item definitions, pass conditions and the written rule behind each: `rubric.md`.
`score` = mean of a case's applicable items (headline). `pass` = every critical item passes (`correct`, plus `no_changes`, `scope`, `no_new_files`, `task_value`, `tests_pass` where they apply).

## Judge validation

- Negatives (`judge_negatives.json`): 12/12 empty, "I don't know" and wrong replies fail `correct`.
- Agreement with hand labels (`judge_agreement.json`, labels by agent-hillclimb on pilot and baseline train runs): 52/60 items.

| item | agree |
|---|---|
| `correct` | 13/13 |
| `direct` | 11/13 |
| `no_commentary` | 10/13 |
| `plain` | 11/12 |
| `mental_model` | 4/4 |
| `in_scope` | 1/1 |
| `sourced` | 2/4 |

Judge: claude -p Sonnet, tools off, JSON schema output. It reads the request, the answer key, the final reply and, for edits, the commit log and diff.
