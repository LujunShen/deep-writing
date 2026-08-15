# Workflow Protocol

## Phase 0: Calibrate The Voice

1. Read `material-intake.md` and identify which Tier A materials are present.
2. If the profile is incomplete, do not edit prose. Ask for the missing evidence or proceed only when the task is purely structural and the author explicitly accepts a provisional profile.
3. Extract the following dimensions from the originals, not from AI revisions:
   - median and range of sentence length;
   - punctuation habits: commas, semicolons, colons, dashes, parentheses;
   - sentence openers and paragraph openers;
   - active/passive balance by section type;
   - first-person stance and where it appears;
   - hedging and direct-evaluation patterns;
   - preferred transitions and repeated verbs;
   - claim-first versus evidence-first argumentation.
4. Run `scripts/style_compare.py BASELINE CANDIDATE` on representative original passages to record objective baselines. Add a local `--lexicon` file only when the author supplies approved and rejected terms.
5. Write the dimensions into `style-profile.md`, with at most twenty representative anchors and at most twenty anti-anchors.
6. Record calibration date, source files, and confidence. If the corpus is small, mark confidence as partial and be more conservative during editing.

## Phase 1: Architecture Pass

1. Read only what is needed to model the argument: title, abstract, headings, first and last sentence of each paragraph, and explicit claims.
2. Produce a current map:

```text
Section -> Subsection -> Paragraph -> Claim/function -> Links before/after
```

3. Diagnose only structural problems:
   - claim order or logic gap;
   - duplicate sections or paragraphs;
   - section doing multiple jobs;
   - evidence not adjacent to its claim;
   - weak transition between major moves;
   - mislabeled headings.
4. Produce a block-level plan:
   - keep, move, split, merge, delete, or relabel;
   - exact source and destination for each move;
   - any missing section as a description, not drafted prose.
5. Do not rewrite the author's sentences in this phase. A newly required bridge can be proposed as a separate labeled item and only inserted after approval.

## Phase 2: Apply Structure

1. Apply only approved block moves. Preserve block text verbatim except for mechanical changes forced by the move.
2. Keep citations, equations, tables, and figure references attached to the correct block.
3. Produce a structural diff summary:
   - what moved;
   - what was split or merged;
   - what new bridge text was added.
4. If a move depends on a new transition sentence, show it separately and mark it as `[NEW BRIDGE]`.

## Phase 3: Language Pass

1. Allow only:
   - spelling, typography, grammar, and punctuation fixes;
   - consistency of terminology, numbers, acronyms, and citation style;
   - removal of exact duplication;
   - split or merge of a sentence only when it is grammatically broken.
2. For each sentence-level change, show:

```text
ORIGINAL: ...
PROPOSED: ...
REASON: ...
STYLE RISK: low/medium/high and why
```

3. Apply the concision gate from `elements-of-style.md` before shortening or deleting text:
   - state the claim;
   - state the reason or condition;
   - state the author's evaluation or tension;
   - state the link to the next paragraph.
4. Compare the proposal against `style-profile.md` and the same gate. Reject edits that:
   - flatten a critical claim;
   - shorten a sentence by removing its condition, consequence, or evidence link;
   - convert the author's point of view into neutral summary;
   - remove hedging or insert hedging the author did not choose;
   - replace an approved transition or evaluative verb with a generic one;
   - convert active to passive or passive to active without author approval;
   - regularize sentence length or punctuation rhythm.
5. After editing, run `scripts/style_compare.py ORIGINAL REVISION` between the approved original and revision. Investigate large metric shifts even if individual edits looked harmless.
6. If a requested change conflicts with the profile or the concision gate, say so and offer alternatives instead of silently obeying.

## Phase 4: Close The Loop

1. Ask the author to review structural suggestions and language edits separately.
2. Add accepted edits to the profile when they reveal a new style preference.
3. Add rejected edits to the feedback log with the exact reason.
4. Update anchors and anti-anchors only with short verbatim examples, not whole documents.
5. Record the date, manuscript, and calibration version in `style-profile.md`.

## Output Contract

Never return only a rewritten document. Always include:

- the mode used;
- the architecture plan or structural diff;
- the language diff;
- items flagged for author decision;
- a note on any edits not made because they would violate the style profile.
