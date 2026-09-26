from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_handoff import REQUIRED_SECTIONS, validate_text  # noqa: E402


def minimal_handoff() -> str:
    sections = {
        "Goal": "Continue the scoped task.",
        "Current State": "- Verified: repository state was inspected.",
        "Files Changed": "None — working tree unchanged.",
        "Key Discoveries": "None — no durable discovery yet.",
        "Decisions": "None — no decision made yet.",
        "Failed Approaches": "None — no failed approach worth preserving.",
        "Remaining Work": "- [ ] Inspect the target file.",
        "Verification": "| Check | Result | When |\n| --- | --- | --- |\n| Repository inspection | PASS | current session |",
        "Next Recommended Action": "Inspect `src/example.ts`.",
    }
    metadata = (
        "# CODEX_HANDOFF\n\n"
        "> Generated: 2026-09-26T00:00:00Z\n"
        "> Repository: example\n"
        "> Branch: main\n"
        "> HEAD: abc1234\n"
        "> Working tree: clean\n"
    )
    body = "\n".join(f"\n## {name}\n\n{sections[name]}\n" for name in REQUIRED_SECTIONS)
    return metadata + body


class BundledExamplesTest(unittest.TestCase):
    def test_all_examples_are_valid(self) -> None:
        for path in sorted((ROOT / "examples").glob("*.md")):
            with self.subTest(path=path.name):
                result = validate_text(path.read_text(encoding="utf-8"))
                self.assertEqual([], result.errors)


class ContractTest(unittest.TestCase):
    def test_minimal_handoff_is_valid(self) -> None:
        self.assertTrue(validate_text(minimal_handoff()).ok)

    def test_missing_section_is_rejected(self) -> None:
        text = minimal_handoff().replace(
            "\n## Failed Approaches\n\nNone — no failed approach worth preserving.\n", "\n"
        )
        result = validate_text(text)
        self.assertIn("missing required section: Failed Approaches", result.errors)

    def test_out_of_order_sections_are_rejected(self) -> None:
        text = minimal_handoff()
        text = text.replace("## Goal", "## __TEMP__", 1)
        text = text.replace("## Current State", "## Goal", 1)
        text = text.replace("## __TEMP__", "## Current State", 1)
        result = validate_text(text)
        self.assertIn("required sections are out of order", result.errors)

    def test_multiple_next_actions_are_rejected(self) -> None:
        text = minimal_handoff().replace(
            "Inspect `src/example.ts`.",
            "- Inspect `src/example.ts`.\n- Run the complete test suite.",
        )
        result = validate_text(text)
        self.assertIn(
            "Next Recommended Action must contain exactly one action, not a list",
            result.errors,
        )

    def test_private_key_material_is_rejected(self) -> None:
        text = minimal_handoff().replace(
            "None — no durable discovery yet.",
            "-----BEGIN PRIVATE KEY-----",
        )
        result = validate_text(text)
        self.assertIn("possible private key material detected", result.errors)


if __name__ == "__main__":
    unittest.main()
