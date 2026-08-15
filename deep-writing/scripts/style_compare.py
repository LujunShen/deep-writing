#!/usr/bin/env python3
"""Compare objective writing-style metrics between two plain-text drafts."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
PASSIVE_RE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being)\s+"
    r"(?:not\s+)?(?:\w+\s+){0,2}\w+(?:ed|en|ified)\b",
    re.IGNORECASE,
)
NOMINALIZATION_SUFFIXES = (
    "tion",
    "ment",
    "ity",
    "ness",
    "ance",
    "ence",
    "ization",
    "ism",
)

TRANSITIONS = {
    "however",
    "therefore",
    "thus",
    "moreover",
    "furthermore",
    "nevertheless",
    "consequently",
    "accordingly",
    "in contrast",
    "by contrast",
    "conversely",
    "in addition",
    "for example",
    "for instance",
    "in particular",
    "notably",
    "critically",
    "subsequently",
    "alternatively",
    "meanwhile",
}

HEDGES = {
    "may",
    "might",
    "could",
    "perhaps",
    "possibly",
    "probably",
    "likely",
    "suggests",
    "suggested",
    "appears",
    "appeared",
    "tends",
    "often",
    "generally",
    "usually",
    "typically",
    "potentially",
    "arguably",
    "seems",
    "seemed",
    "in part",
    "to some extent",
    "may be",
}

BOOSTERS = {
    "notably",
    "critically",
    "importantly",
    "indeed",
    "striking",
    "strikingly",
    "fundamentally",
    "essentially",
    "clearly",
    "especially",
    "in particular",
    "key",
    "central",
    "crucial",
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", text.lower())


def split_sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text)
    return [part.strip() for part in SENTENCE_END_RE.split(flat) if part.strip()]


def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round(q * (len(ordered) - 1)))]


def count_terms(tokens: list[str], terms: Iterable[str]) -> int:
    normalized = " " + " ".join(tokens) + " "
    return sum(normalized.count(" " + term + " ") for term in terms)


def top_openers(sentences: list[str], limit: int = 5) -> list[tuple[str, int]]:
    openers = Counter()
    for sentence in sentences:
        words = tokenize(sentence)
        if words:
            openers[words[0]] += 1
    return openers.most_common(limit)


def read_lexicon(path: Path) -> tuple[list[str], list[str]]:
    approved: list[str] = []
    banned: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().lower()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            banned.append(line[1:].strip())
        elif line.startswith("+"):
            approved.append(line[1:].strip())
        else:
            approved.append(line)
    return approved, banned


def analyze(text: str, approved_terms: list[str], banned_terms: list[str]) -> dict:
    tokens = tokenize(text)
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)
    sentence_word_counts = [len(tokenize(sentence)) for sentence in sentences]
    paragraph_word_counts = [len(tokenize(paragraph)) for paragraph in paragraphs]
    total_words = len(tokens)
    unique_tokens = set(tokens)

    passive_sentences = sum(bool(PASSIVE_RE.search(sentence)) for sentence in sentences)
    first_singular = count_terms(tokens, {"i", "my", "mine", "myself"})
    first_plural = count_terms(tokens, {"we", "our", "ours", "ourselves"})
    transitions = count_terms(tokens, TRANSITIONS)
    hedges = count_terms(tokens, HEDGES)
    boosters = count_terms(tokens, BOOSTERS)
    approved = count_terms(tokens, approved_terms)
    banned = count_terms(tokens, banned_terms)
    nominalizations = sum(token.endswith(NOMINALIZATION_SUFFIXES) for token in tokens)
    word_lengths = [len(token) for token in tokens]

    return {
        "counts": {
            "characters": len(text),
            "words": total_words,
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
        },
        "sentence": {
            "words_mean": mean([float(x) for x in sentence_word_counts]),
            "words_median": median([float(x) for x in sentence_word_counts]),
            "words_p90": quantile([float(x) for x in sentence_word_counts], 0.9),
            "short_under_10_ratio": (
                sum(x < 10 for x in sentence_word_counts) / len(sentence_word_counts)
                if sentence_word_counts
                else 0.0
            ),
            "long_over_30_ratio": (
                sum(x > 30 for x in sentence_word_counts) / len(sentence_word_counts)
                if sentence_word_counts
                else 0.0
            ),
            "comma_ratio": text.count(",") / len(sentences) if sentences else 0.0,
            "semicolon_ratio": text.count(";") / len(sentences) if sentences else 0.0,
            "colon_ratio": text.count(":") / len(sentences) if sentences else 0.0,
            "dash_ratio": (text.count(" - ") + text.count("--")) / len(sentences)
            if sentences
            else 0.0,
            "parenthesis_ratio": (text.count("(") + text.count(")"))
            / len(sentences)
            if sentences
            else 0.0,
            "top_openers": top_openers(sentences),
        },
        "voice": {
            "passive_sentence_ratio": passive_sentences / len(sentences)
            if sentences
            else 0.0,
            "first_singular_per_1000": first_singular / total_words * 1000
            if total_words
            else 0.0,
            "first_plural_per_1000": first_plural / total_words * 1000
            if total_words
            else 0.0,
            "hedges_per_1000": hedges / total_words * 1000 if total_words else 0.0,
            "boosters_per_1000": boosters / total_words * 1000
            if total_words
            else 0.0,
            "transitions_per_1000": transitions / total_words * 1000
            if total_words
            else 0.0,
            "nominalizations_per_1000": nominalizations / total_words * 1000
            if total_words
            else 0.0,
            "mean_word_length": mean([float(x) for x in word_lengths]),
        },
        "vocabulary": {
            "type_token_ratio": len(unique_tokens) / total_words if total_words else 0.0,
            "approved_term_count": approved,
            "banned_term_count": banned,
        },
        "paragraph": {
            "words_mean": mean([float(x) for x in paragraph_word_counts]),
            "words_median": median([float(x) for x in paragraph_word_counts]),
        },
    }


def flatten_metrics(metrics: dict, prefix: str = "") -> dict[str, float]:
    flat: dict[str, float] = {}
    for key, value in metrics.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_metrics(value, path))
        elif isinstance(value, (int, float)):
            flat[path] = float(value)
    return flat


def compare(
    baseline: dict, candidate: dict, max_delta: float
) -> tuple[list[dict], list[dict[str, float]]]:
    base_flat = flatten_metrics(baseline)
    candidate_flat = flatten_metrics(candidate)
    drift: list[dict] = []
    rows: list[dict[str, float]] = []
    for metric in sorted(set(base_flat) | set(candidate_flat)):
        base_value = base_flat.get(metric, 0.0)
        candidate_value = candidate_flat.get(metric, 0.0)
        if base_value == 0.0 and candidate_value == 0.0:
            continue
        delta = (
            (candidate_value - base_value) / base_value
            if base_value != 0.0
            else (1.0 if candidate_value != 0.0 else 0.0)
        )
        row = {
            "metric": metric,
            "baseline": base_value,
            "candidate": candidate_value,
            "delta": delta,
        }
        rows.append(row)
        if abs(delta) >= max_delta:
            drift.append(row)
    return drift, rows


def print_report(
    baseline: dict,
    candidate: dict,
    drift: list[dict],
    rows: list[dict[str, float]],
) -> None:
    print("Style comparison")
    print(f"{'Metric':38} {'Baseline':>12} {'Candidate':>12} {'Delta':>10}")
    print("-" * 76)
    for row in rows:
        marker = " *" if row in drift else ""
        print(
            f"{row['metric']:38} "
            f"{row['baseline']:12.3f} "
            f"{row['candidate']:12.3f} "
            f"{row['delta'] * 100:9.1f}%{marker}"
        )
    print("-" * 76)
    print(f"Drift metrics: {len(drift)}")
    if drift:
        print("Review metrics marked with * before deciding whether the drift is intentional.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare objective writing-style metrics between an author's "
            "baseline draft and an edited candidate."
        )
    )
    parser.add_argument("baseline", type=Path, help="author-approved original text")
    parser.add_argument("candidate", type=Path, help="edited or AI-revised text")
    parser.add_argument(
        "--lexicon",
        type=Path,
        help="optional term list; prefix approved terms with + and banned terms with -",
    )
    parser.add_argument(
        "--max-delta",
        type=float,
        default=0.25,
        help="relative change threshold for flagging drift (default: 0.25)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON output")
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="exit with status 2 if any metric exceeds max-delta",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.baseline.is_file():
        print(f"Baseline file not found: {args.baseline}", file=sys.stderr)
        return 1
    if not args.candidate.is_file():
        print(f"Candidate file not found: {args.candidate}", file=sys.stderr)
        return 1

    approved_terms: list[str] = []
    banned_terms: list[str] = []
    if args.lexicon:
        if not args.lexicon.is_file():
            print(f"Lexicon file not found: {args.lexicon}", file=sys.stderr)
            return 1
        approved_terms, banned_terms = read_lexicon(args.lexicon)

    baseline_text = args.baseline.read_text(encoding="utf-8")
    candidate_text = args.candidate.read_text(encoding="utf-8")
    baseline = analyze(baseline_text, approved_terms, banned_terms)
    candidate = analyze(candidate_text, approved_terms, banned_terms)
    drift, rows = compare(baseline, candidate, args.max_delta)

    if args.json:
        print(
            json.dumps(
                {
                    "baseline": baseline,
                    "candidate": candidate,
                    "drift": drift,
                    "drift_count": len(drift),
                },
                indent=2,
            )
        )
    else:
        print_report(baseline, candidate, drift, rows)

    return 2 if args.fail_on_drift and drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
