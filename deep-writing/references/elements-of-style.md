# Elements Of Style Constraints

Use these distilled principles from the author's preferred style reference. The full source is in `assets/elements-of-style-strunk.pdf`; load that PDF only when an exact rule or example is needed.

## Purpose

Apply the book's concision without turning the text into neutral summary. Concision is a by-product of vigor, not a mandate to remove the author's position, evidence, or logical links.

## Concision Gate

Before shortening or deleting any sentence, identify and preserve these four elements:

1. **Claim**: What does this sentence assert or conclude?
2. **Reason**: What evidence, condition, mechanism, or logical connection supports the claim?
3. **Stance**: What judgment, tension, emphasis, or critical position does the author add?
4. **Move**: How does this sentence connect to the next paragraph or argument?

Reject an edit if it removes any of these merely to reduce word count.

## Operational Rules

1. Omit needless words, but never omit needful claims, conditions, or evaluations.
2. Prefer the active voice when it makes agency visible. Preserve passive voice when the subject is unknown, unimportant, or deliberately backgrounded.
3. Make definite assertions. Replace vague negative wording when the author's intended meaning is recoverable.
4. Prefer definite, specific, and concrete terms over abstractions. Add or retain representative examples rather than deleting them.
5. Keep the paragraph a single unit of thought. Move or split paragraphs to repair topic drift, not merely to shorten blocks.
6. Use parallel construction for coordinate ideas.
7. Keep related words together and put the new or emphatic idea near the end.
8. Write with nouns and verbs. Avoid leaning on adverbs and qualifiers that weaken the point.
9. Avoid overstatement and excessive qualifiers. Do not replace the author's calibrated hedging with either certainty or vague doubt.
10. Prefer clarity. Do not take shortcuts that force the reader to reconstruct the missing step.
11. Preserve argument-driven judgment, but remove gratuitous opinion that is not supported by the manuscript's claim.
12. Revision is expected. Keep a reversible record so the author can recover any deleted nuance.

## Anti-Laziness Examples

Reject this kind of edit:

```text
ORIGINAL:
A model that is well calibrated today may become quietly misleading under distribution shift.

BAD CONCISION:
Models may become misleading.
```

The bad version deletes the condition, the timing, and the tension. Prefer:

```text
GOOD CONCISION:
Models calibrated under one distribution can become misleading when that distribution shifts.
```

Reject shortening that removes a sentence whose job is evaluation:

```text
ORIGINAL:
This tension is not incidental; it follows from treating missing labels as evidence.

BAD DELETION:
This tension follows from treating missing labels as evidence.
```

The word `incidental` carries the author's critical judgment.

## Precedence

- The author's calibrated `style-profile.md` takes precedence over this reference.
- Academic conventions take precedence over Strunk and White examples intended for literary prose.
- When concision conflicts with stance or logical continuity, preserve stance and continuity and offer an alternative.
