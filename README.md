# Deep Writing

Deep Writing is a Codex skill for restructuring academic manuscripts while preserving the author's personal voice. It separates architecture work from sentence-level editing and uses a calibrated style profile, a feedback log, Elements of Style-inspired concision rules, and objective style-drift checks.

## Install

Requires Codex with the `skill-installer` system skill.

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo LujunShen/deep-writing \
  --path deep-writing
```

Or, if `CODEX_HOME` is unset:

```bash
python3 "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo LujunShen/deep-writing \
  --path deep-writing
```

After installation, invoke it in a new Codex turn:

```text
Use $deep-writing to restructure my manuscript while preserving my academic writing style.
```

## First Calibration

On first use, supply the materials listed in `deep-writing/references/material-intake.md`: original drafts, paired AI revisions, approved style anchors, rejected anti-anchors, and any hard vetoes. Codex will populate `references/style-profile.md` and can then perform style-sensitive architecture and language passes.

## What Is Not Included

The public repository does not include the full Elements of Style PDF or any author manuscripts. Keep personal drafts, calibration profiles, and feedback logs private; create a local copy or keep them outside the shared skill folder.
