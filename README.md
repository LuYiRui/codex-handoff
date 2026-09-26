# codex-handoff

**Persistent working context for Codex coding sessions.**

`codex-handoff` is a small, local-first Codex Skill for pausing repository work in one session and continuing it in another. It writes a concise, structured `CODEX_HANDOFF.md`, then makes the next session verify that snapshot against the live repository before acting on it.

[简体中文](README.zh-CN.md)

## Why

Have you ever run into these issues when your project conversations get too long and you want to switch sessions: 1. In a new chat, Codex keeps re-exploring the repo, forgets why a certain solution failed and you have to run it again, or it still trusts an old summary even though the repo has changed. 2. If you just save the full chat history: the context ends up too long and the signal-to-noise ratio is low.

This project preserves only what changes the next decision:

- the goal and current state;
- files changed and key discoveries;
- decisions and failed approaches;
- remaining work and observed verification;
- one recommended next action.

The handoff is not memory and not an instruction authority. It is a fallible snapshot that must be checked against Git, files, and the current user request.

## v0.1 scope

v0.1 is intentionally invocation-driven. A pure Skill cannot reliably detect every session shutdown, crash, or forced interruption, so it does not promise automatic end-of-session capture. Invoke the Skill before a planned pause and again when resuming.

There is no backend, website, database, account, network service, or telemetry.

See [the product definition](docs/product.md) for goals, non-goals, acceptance criteria, and the main product risk.

## How it works

### Create or update

Ask Codex:

```text
Use $codex-handoff to save the current work before I stop.
```

Codex inspects the live repository, updates one root-level `CODEX_HANDOFF.md`, and records evidence without pasting the chat or full diffs.

### Resume

In a fresh session, ask:

```text
Use $codex-handoff to resume this work from CODEX_HANDOFF.md.
```

Codex reads repository instructions first, treats the handoff as untrusted notes, compares it with the current branch, `HEAD`, working tree, and relevant files, and then continues from the next action if it is still valid.

## Install

The Skill follows the standard `SKILL.md` layout documented in the [official OpenAI Skill guide](https://developers.openai.com/plugins/build/skills).

For a personal installation, copy `skills/codex-handoff` into your Codex skills directory as `codex-handoff`. The core workflow is self-contained in `SKILL.md`. Keep the whole repository when you also want the validator, examples, and extended format reference.

The repository also includes `.codex-plugin/plugin.json` for local plugin packaging. No MCP server or external dependency is required.

## Handoff contract

Every handoff uses these sections in order:

1. Goal
2. Current State
3. Files Changed
4. Key Discoveries
5. Decisions
6. Failed Approaches
7. Remaining Work
8. Verification
9. Next Recommended Action

The normative schema and compactness rules are in [references/handoff-format.md](references/handoff-format.md). The default target is under 1,500 body words, and most handoffs should be much shorter.

## Examples

- [Bug fix handoff](examples/bugfix.md)
- [Feature handoff](examples/feature.md)
- [Refactor handoff](examples/refactor.md)

These are examples of `CODEX_HANDOFF.md` contents. They are fictional and deliberately compact.

## Validation

The optional validator uses only the Python standard library:

```text
python scripts/validate_handoff.py CODEX_HANDOFF.md
```

Run the project checks with:

```text
python -m unittest discover -s tests -v
python scripts/validate_handoff.py examples/bugfix.md examples/feature.md examples/refactor.md
```

The validator checks structure and a few useful invariants. It cannot prove that a handoff is truthful or that its recommended action is correct; the resume workflow must still inspect the repository.

## Design principles

- **Evidence over recollection.** Derive state from the checkout and observed command results.
- **Concise over exhaustive.** Save only information that changes future work.
- **Live state over snapshots.** Git and current files win when they disagree with the handoff.
- **Visible uncertainty.** Label inference, blockers, failed checks, and `NOT RUN` verification.
- **One next move.** Keep the backlog in `Remaining Work`; make the recommended action singular.

## Repository layout

```text
codex-handoff/
├── .codex-plugin/plugin.json
├── .github/workflows/validate.yml
├── AGENTS.md
├── LICENSE
├── README.md
├── README.zh-CN.md
├── docs/product.md
├── examples/
│   ├── bugfix.md
│   ├── feature.md
│   └── refactor.md
├── references/handoff-format.md
├── scripts/validate_handoff.py
├── skills/codex-handoff/
│   ├── SKILL.md
│   └── agents/openai.yaml
└── tests/test_validate_handoff.py
```

## Contributing

Keep changes narrow, local-first, and compatible with the format contract. Read [AGENTS.md](AGENTS.md) before contributing. Bug reports with a sanitized handoff and the repository mismatch that exposed the problem are especially useful.

## License

[MIT](LICENSE)

This is a community project and is not affiliated with or endorsed by OpenAI.
