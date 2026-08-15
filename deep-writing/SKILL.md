---
name: deep-writing
description: >-
  Restructure academic reviews, manuscripts, proposals, and thesis chapters while preserving the author's personal writing voice. Use when the user asks for Deep Writing, wants Codex to improve architecture without rewriting their sentences, provides original and AI-edited draft pairs for style calibration, asks for style-sensitive copyediting that does not flatten critical language, or wants Elements of Style-inspired concision without losing stance and logical continuity. Supports Markdown, DOCX, LaTeX, and plain-text drafts.
---

# Deep Writing

## Core Contract

- Treat Codex as a structural consultant first and a constrained copyeditor second. Do not act as a co-author unless the user explicitly asks.
- Preserve the author's sentence rhythm, critical tone, first-person stance, hedging, vocabulary, and paragraph logic.
- Separate structural revision from sentence-level revision. Never perform both in one pass.
- If `references/style-profile.md` is incomplete, run calibration before editing a manuscript.
- Apply the concision gate from `references/elements-of-style.md` before shortening prose.

## Quick Workflow

1. Confirm the artifact, target document type, and requested mode: architecture only, language only, or both.
2. Check `references/style-profile.md`. If it has not been calibrated or may be stale, follow `references/material-intake.md`.
3. When a baseline draft and candidate draft are available, run `scripts/style_compare.py BASELINE CANDIDATE` to quantify style drift before manual review.
4. Produce an architecture pass first: a section/paragraph map, diagnosis, and move plan. Do not rewrite sentences in this pass.
5. After the author approves the structure, run a language pass. Report each sentence-level change as original, proposed, reason, and style risk.
6. Update `references/feedback-log.md` and `references/style-profile.md` after the author reviews the result.

## Non-Negotiable Rules

- Never silently rewrite a full draft or replace the author's critical phrasing with generic academic filler.
- Never shorten a sentence by deleting its claim, evidence, condition, evaluation, or link to the next argument.
- Treat neutral wording as a style failure: concise text must retain the author's point of view and logical continuity.
- Preserve the original argument unless there is an explicit instruction to change it.
- Preserve tense, person, hedging strength, and first-person stance unless the journal or author requires a change.
- Mark every newly created bridge or transition sentence as new text, not as a mere copyedit.
- If a change may alter meaning or tone, ask first instead of assuming.
- Do not let structure advice leak into sentence style; keep the two output layers visibly separate.

## Modes

- **Architecture**: Review section order, paragraph flow, claim placement, redundancy, and subsection boundaries. Output an edit plan with block-level move instructions.
- **Language**: Fix spelling, grammar, punctuation, terminology consistency, and obvious redundancy. Use the style profile as a constraint, not as a template for wholesale rewording.
- **Full**: Run Architecture, get approval if feasible, then run Language. If the user asks for a one-shot edit, still show the structural plan and language diff separately.
- **Calibrate**: Extract and update the personal style profile from supplied drafts and judgments.

## Resource Routing

- `references/material-intake.md`: Required materials and how to collect them.
- `references/workflow-protocol.md`: Detailed phase-by-phase operating instructions.
- `references/style-profile.md`: Persistent author-voice profile; update after calibration and feedback.
- `references/feedback-log.md`: Chronological record of accepted and rejected edits.
- `references/elements-of-style.md`: Concision and composition constraints distilled from the author's preferred style guide.
- `assets/style-audit-questionnaire.md`: Optional questionnaire for the author.
- `assets/elements-of-style-strunk.pdf`: Full source style guide, kept outside the default context.
- `scripts/style_compare.py`: Deterministic metrics for comparing baseline and revised text.
