# Session plans

This folder is the durable record of individual research and coding sessions.
It lets a new session resume from verified project state rather than relying on
chat history or memory.

`PROJECT_ROADMAP.md` holds the longer-term stages. It is a deliberately rough
working draft, not a committed schedule: stages stay bare placeholders until
they are worked out through discussion and explicitly agreed. Consult it when
choosing a session goal, but do not treat an unagreed stage as a decision, and
do not add detail to it outside a discussion. The rules are in the root
`AGENTS.md`, under *Roadmap discipline*.

Records here are where the reasoning, evidence, and task detail live. The
roadmap only records which stages are settled.

## Coverage

Dated records begin on 2026-07-27. Sessions before that date were not recorded
here; for that earlier period the git history and the notebooks are the only
record. Do not read this folder as a complete history of the project.

## File naming

Create one file for each distinct desk session:

```text
YYYY-MM-DD-short-goal-slug.md
```

For example:

```text
2026-07-22-reproduce-borghi-hz-bin.md
2026-07-22-trace-covariance-components-2.md
```

The slug describes the intended main outcome. If the session changes direction,
keep the filename stable and record the actual outcome in the close-out. Use
`-2`, `-3`, and so on only for separate sessions on the same date.

## Workflow

1. Copy `TEMPLATE.md` to a dated filename before substantive work begins.
2. Write one observable session goal and a concrete definition of done.
3. Fill in the starting state using inspected files, outputs, or calculations.
4. Plan a small number of substantive tasks in dependency order. Include the
   expected artifact and the scientific or computational check for each task.
5. Update statuses after meaningful milestones, decisions, or blockers rather
   than after every minor action.
6. At the end, reconcile all tasks and complete the close-out so the next
   session has an exact starting point.

Use only these statuses: `planned`, `in progress`, `completed`, `partial`,
`blocked`, and `deferred`. A completion claim needs recorded evidence. Note
whether evidence was inspected directly or only reported by the user.

The detailed rules for how Codex should create, use, and close these records are
in the root `AGENTS.md`.
