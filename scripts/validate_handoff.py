#!/usr/bin/env python3
"""Validate the structural contract of one or more CODEX_HANDOFF.md files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REQUIRED_SECTIONS = (
    "Goal",
    "Current State",
    "Files Changed",
    "Key Discoveries",
    "Decisions",
    "Failed Approaches",
    "Remaining Work",
    "Verification",
    "Next Recommended Action",
)

REQUIRED_METADATA = ("Generated", "Repository", "Branch", "HEAD", "Working tree")
MAX_WORDS = 1_500


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _visible_lines(text: str) -> list[str]:
    """Return Markdown lines outside fenced code blocks."""
    visible: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        if not in_fence and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence = True
            fence_marker = stripped[:3]
            continue
        if in_fence and stripped.startswith(fence_marker):
            in_fence = False
            fence_marker = ""
            continue
        if not in_fence:
            visible.append(line)
    return visible


def _section_map(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    headings: list[str] = []
    sections: dict[str, list[str]] = {}
    active: str | None = None
    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*#*\s*$", line)
        if match:
            active = match.group(1).strip()
            headings.append(active)
            sections.setdefault(active, [])
        elif active is not None:
            sections[active].append(line)
    return headings, sections


def _meaningful_lines(lines: Iterable[str]) -> list[str]:
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("<!--")
    ]


def validate_text(text: str) -> ValidationResult:
    result = ValidationResult()
    lines = _visible_lines(text)
    nonempty = [line.strip() for line in lines if line.strip()]

    if not nonempty or nonempty[0] != "# CODEX_HANDOFF":
        result.errors.append("the first non-empty line must be '# CODEX_HANDOFF'")

    headings, sections = _section_map(lines)
    for name in REQUIRED_SECTIONS:
        count = headings.count(name)
        if count == 0:
            result.errors.append(f"missing required section: {name}")
        elif count > 1:
            result.errors.append(f"duplicate required section: {name}")

    present_required = [name for name in headings if name in REQUIRED_SECTIONS]
    expected_present = [name for name in REQUIRED_SECTIONS if name in present_required]
    if present_required != expected_present:
        result.errors.append("required sections are out of order")

    for name in REQUIRED_SECTIONS:
        if name in sections and not _meaningful_lines(sections[name]):
            result.errors.append(f"section is empty: {name}; use 'None — reason' when needed")

    first_section_index = next(
        (index for index, line in enumerate(lines) if line.startswith("## ")),
        len(lines),
    )
    metadata_text = "\n".join(lines[:first_section_index])
    for field_name in REQUIRED_METADATA:
        if not re.search(rf"^>\s*{re.escape(field_name)}:\s*\S.+$", metadata_text, re.MULTILINE):
            result.errors.append(f"missing or empty metadata field: {field_name}")

    verification = "\n".join(sections.get("Verification", []))
    if verification and not re.search(r"\b(?:PASS|FAIL|NOT RUN)\b", verification):
        result.errors.append("Verification must record at least one PASS, FAIL, or NOT RUN result")

    next_lines = _meaningful_lines(sections.get("Next Recommended Action", []))
    list_items = [
        line
        for line in next_lines
        if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line)
    ]
    if len(list_items) > 1:
        result.errors.append("Next Recommended Action must contain exactly one action, not a list")
    else:
        paragraphs = 0
        in_paragraph = False
        for line in sections.get("Next Recommended Action", []):
            if line.strip():
                if not in_paragraph:
                    paragraphs += 1
                    in_paragraph = True
            else:
                in_paragraph = False
        if paragraphs > 1:
            result.errors.append("Next Recommended Action must contain one paragraph")

    body_text = "\n".join(
        line
        for name in REQUIRED_SECTIONS
        for line in sections.get(name, [])
    )
    word_count = len(re.findall(r"\b[\w'-]+\b", body_text, re.UNICODE))
    has_override = bool(re.search(r"^>\s*Compactness override:\s*\S.+$", text, re.MULTILINE))
    if word_count > MAX_WORDS and not has_override:
        result.errors.append(
            f"handoff has {word_count} words; limit is {MAX_WORDS} unless a Compactness override is documented"
        )
    elif word_count > MAX_WORDS:
        result.warnings.append(f"handoff exceeds the default compactness target ({word_count} words)")

    if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", text):
        result.errors.append("possible private key material detected")

    return result


def validate_file(path: Path) -> ValidationResult:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return ValidationResult(errors=[f"cannot read file: {exc}"])
    return validate_text(text)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate CODEX_HANDOFF.md structure and compactness."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="handoff Markdown files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failed = False
    for path in args.paths:
        result = validate_file(path)
        if result.ok:
            print(f"[OK] {path}")
        else:
            failed = True
            print(f"[FAIL] {path}")
        for warning in result.warnings:
            print(f"  warning: {warning}")
        for error in result.errors:
            print(f"  error: {error}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
