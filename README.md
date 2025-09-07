# Laeda EFM++ Prompt Pack · Public Highlights

**TL;DR.** A tiny, practical pack of system prompts, checklists, and examples built around the EFM++ discipline (Emotion · Fact · Narrative · Meta + honesty + DecisionLog + token budget). Goal: faster first-usable answers with explicit acceptance criteria and traceable changes.

## Why this repo exists
People waste time on vague prompts and undocumented iterations. This pack shows how to structure LLM work so the **first** generation is often shippable, and every change is auditable.

## What’s inside
- **/prompts/** — battle-tested system/working prompts (Markdown or JSON).
- **/checklists/** — short SOPs for setup, review, and acceptance tests.
- **/examples/** — sanitized inputs/outputs that illustrate expected quality.
- **/docs/** — lightweight screenshots/diagrams (no private data).

## Core ideas (EFM++)
- **Role + Output format + Constraints + Acceptance tests** in every prompt.
- **s metric** = share of tasks where the first answer is directly used.
- **Δ time/tokens** vs baseline to estimate practical savings.
- **DecisionLog**: record why a change was made, not just what changed.
- **Token discipline**: keep prompts under strict budgets when possible.

## Quickstart
1. Pick a prompt from `/prompts/` and paste your real task text into the slot marked `INPUT`.
2. Run the **acceptance checklist** from `/checklists/` before you ask for a redo.
3. Log changes in `DecisionLog:` at the end of each prompt or PR.
4. Compare against `/examples/` to calibrate tone, structure, and depth.

## Contributing
- Open an issue with a minimal repro or a concrete before/after.
- PRs: add tests or examples; keep prompts readable and measured.
- No private code, secrets, or client data. Ever.

## License
MIT (see `LICENSE`). Texts and screenshots are provided “as is” without warranties. You are responsible for compliance with your org’s policies.

## Contact
Telegram: **@koregarequiemdaaa** · Email: **arielperseny@gmail.com**
