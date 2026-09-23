import copy
import json
from pathlib import Path
import unittest

from scripts import check_singleton_writeback


ROOT = Path(__file__).resolve().parents[1]


class WritebackCounterexamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads(
            (ROOT / "logs/singleton-writeback/weakening-ghost-inputs/results.json").read_text()
        )

    def test_real_counterexamples_preserve_the_other_observation(self):
        check_singleton_writeback.check_results(self.results)

    def test_unproved_witness_is_not_a_counterexample(self):
        results = copy.deepcopy(self.results)
        results["missing-initial"]["counterexample"]["verified_goals"] = 0
        with self.assertRaises(AssertionError):
            check_singleton_writeback.check_results(results)

    def test_bindings_must_match_the_verified_certificate(self):
        results = copy.deepcopy(self.results)
        results["missing-return"]["counterexample"]["bindings"]["r2"]["value"]["items"][1] = False
        with self.assertRaises(AssertionError):
            check_singleton_writeback.check_results(results)


if __name__ == "__main__":
    unittest.main()
