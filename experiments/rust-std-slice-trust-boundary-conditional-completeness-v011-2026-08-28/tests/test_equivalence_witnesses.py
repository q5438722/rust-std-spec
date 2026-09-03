#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_authority_design import unstable_sort_witness


class UnstableSortWitnessTests(unittest.TestCase):
    def test_relation_requires_exact_element_multiset(self) -> None:
        text = unstable_sort_witness(True)
        self.assertIn("(SameElementMultiset left right)", text)
        self.assertIn("(ElementMultiplicity left (select right 2))", text)
        self.assertIn("(ElementMultiplicity right (select left 0))", text)

    def test_positive_witness_only_reorders_equal_key_identities(self) -> None:
        text = unstable_sort_witness(True)
        self.assertIn("(store (store (store base 0 11) 1 10) 2 20)", text)
        self.assertIn("(assert (EqualKeyEquivalent output1 output2))", text)

    def test_negative_witness_rejects_foreign_same_key_identity(self) -> None:
        text = unstable_sort_witness(False)
        self.assertIn("(store (store (store base 0 12) 1 10) 2 20)", text)
        self.assertIn("(assert (not (EqualKeyEquivalent output1 output2)))", text)
        self.assertIn("(ite (= identity 20) 2 1)", text)


if __name__ == "__main__":
    unittest.main()
