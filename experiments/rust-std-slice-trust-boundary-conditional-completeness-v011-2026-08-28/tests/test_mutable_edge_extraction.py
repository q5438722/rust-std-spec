#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import campaign_common as common
from checker_guards import GuardError, validate_obligation
import mutable_edge_extraction as edge
import replay_mutable_edge_extraction as replay
import run_mutable_edge_extraction as runner
import target_pipeline


def replace_call(text: str, symbol: str) -> str:
    target_start = text.index("(define-fun TargetSourceTransition")
    start = text.index(f"({symbol}", target_start)
    balance = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            balance += 1
        elif text[end] == ")":
            balance -= 1
            if balance == 0:
                return text[:start] + "true" + text[end + 1 :]
    raise AssertionError(f"unterminated call to {symbol}")


def definition_span(text: str, symbol: str) -> tuple[int, int]:
    start = text.index(f"(define-fun {symbol}")
    balance = 0
    for end in range(start, len(text)):
        if text[end] == "(":
            balance += 1
        elif text[end] == ")":
            balance -= 1
            if balance == 0:
                return start, end + 1
    raise AssertionError(f"unterminated definition {symbol}")


def run_z3(text: str) -> subprocess.CompletedProcess[str]:
    z3 = shutil.which("z3")
    if not z3:
        raise AssertionError("z3 is unavailable")
    return subprocess.run(
        [z3, "-in", "-smt2"],
        input=text,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


class MutableEdgeExtractionTests(unittest.TestCase):
    def test_active_contracts_and_all_trust_records_match_authority(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        trust = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        for config in edge.TARGETS:
            row = rows[(config.target, config.input_order)]
            records = {
                item["record_id"]: item
                for item in trust
                if (item["target"], item["input_order"])
                == (config.target, config.input_order)
            }
            with self.subTest(target=config.target):
                self.assertEqual(
                    config.active_contract_sha256,
                    row["active_contract_sha256"],
                )
                self.assertEqual(
                    config.active_contract_text,
                    row["active_contract_text"],
                )
                self.assertEqual(
                    config.generated_declaration_sha256,
                    row["generated_declaration_sha256"],
                )
                self.assertEqual(
                    config.source_item_sha256,
                    row["source_item_sha256"],
                )
                self.assertEqual(
                    set(records),
                    set(config.all_trust_site_ids),
                )
                self.assertTrue(
                    all(
                        item["semantic_disposition"]
                        == "admissible-source-backed-support"
                        and item["target_postcondition_coverage"]
                        == "partial-or-lower-level"
                        for item in records.values()
                    )
                )

    def test_canonical_source_and_vocabulary_anchors_fail_closed(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        vocabulary = (
            ROOT
            / "provenance/frozen/specgen/specs/slice_shared_vocabulary.rs"
        ).read_text().splitlines(keepends=True)
        excerpt = "\n".join(
            "".join(vocabulary[start - 1 : end])
            for start, end in edge.VOCABULARY_RANGES
        )
        for config in edge.TARGETS:
            source = rows[(config.target, config.input_order)][
                "source_item_text"
            ]
            edge.validate_source_anchors(config, source, excerpt)
            mutation = (
                source.replace("Some((first, tail))", "Some((tail, first))")
                if config.target.endswith("split_first_mut")
                else source.replace(
                    "Some((last, init))", "Some((init, last))"
                )
                if config.target.endswith("split_last_mut")
                else source.replace("*self = rem;", "Some(first);")
                if config.edge == "first"
                else source.replace("*self = rem;", "Some(last);")
            )
            with self.subTest(target=config.target):
                with self.assertRaises(GuardError):
                    edge.validate_source_anchors(config, mutation, excerpt)
                if config.wrapper:
                    with self.assertRaises(GuardError):
                        edge.validate_source_anchors(
                            config,
                            source,
                            excerpt.replace("remaining ==", "remaining !="),
                        )

    def test_literal_shared_x_shared_b_theorems_are_valid(self) -> None:
        for config in edge.TARGETS:
            for purpose in edge.PURPOSES:
                text, metadata = edge.obligation(config, purpose)
                with self.subTest(target=config.target, purpose=purpose):
                    validate_obligation(text, metadata)
                    edge.validate_target_obligation(config, text, metadata)
                    self.assertIn(
                        """(and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))""",
                        text,
                    )

    def test_boundary_excludes_answers_final_state_and_traces(self) -> None:
        forbidden = (
            "result",
            "selected",
            "range",
            "returned",
            "final",
            "receiver",
            "storage",
            "answer",
            "trace",
        )
        for config in edge.TARGETS:
            metadata = edge.obligation_metadata(config, edge.PRIMARY)
            selectors = [
                item["selector"] for item in metadata["boundary_fields"]
            ]
            with self.subTest(target=config.target):
                self.assertTrue(metadata["boundary_scope"]["narrower_than_target"])
                self.assertTrue(
                    all(
                        not any(token in selector for token in forbidden)
                        for selector in selectors
                    )
                )
                self.assertEqual(
                    set(metadata["boundary_scope"]["admitted_trust_site_ids"]),
                    set(config.all_trust_site_ids),
                )
                empty_fields = {
                    selector for selector in selectors if "empty" in selector
                }
                self.assertEqual(bool(empty_fields), config.wrapper)

    def test_every_active_definition_equality_is_fail_closed(self) -> None:
        for config in edge.TARGETS:
            text, metadata = edge.obligation(config, edge.PRIMARY)
            for symbol in config.active_conjuncts:
                start, end = definition_span(text, symbol)
                definition = text[start:end]
                equality_offsets: list[int] = []
                cursor = 0
                while True:
                    cursor = definition.find("(=", cursor)
                    if cursor < 0:
                        break
                    equality_offsets.append(cursor)
                    cursor += 2
                self.assertTrue(equality_offsets, symbol)
                for offset in equality_offsets:
                    mutated = (
                        text[: start + offset]
                        + "(distinct"
                        + text[start + offset + 2 :]
                    )
                    with self.subTest(
                        target=config.target,
                        symbol=symbol,
                        equality=offset,
                    ):
                        with self.assertRaises(GuardError):
                            edge.validate_target_obligation(
                                config,
                                mutated,
                                metadata,
                            )

    def test_omitted_contract_composition_and_disjointness_fail_closed(
        self,
    ) -> None:
        for config in edge.TARGETS:
            text, metadata = edge.obligation(config, edge.PRIMARY)
            for symbol in config.active_conjuncts:
                with self.subTest(target=config.target, symbol=symbol):
                    with self.assertRaises(GuardError):
                        edge.validate_target_obligation(
                            config,
                            replace_call(text, symbol),
                            metadata,
                        )
            self.assertIn("ActiveDisjointnessConjunct", text)
            with self.assertRaises(GuardError):
                edge.validate_target_obligation(
                    config,
                    text.replace("(<= (+", "(< (+", 1),
                    metadata,
                )

    def test_first_last_indices_ranges_and_tuple_order_fail_closed(self) -> None:
        for config in edge.TARGETS:
            text, metadata = edge.obligation(config, edge.PRIMARY)
            if config.wrapper:
                expected_index = (
                    "(= (p_selected_index p) 0)"
                    if config.edge == "first"
                    else (
                        "(= (p_selected_index p) "
                        "(- (r_held_length r) 1))"
                    )
                )
                range_source = "(seq.extract (r_held_source r)"
            else:
                expected_index = (
                    "(= (y_selected_index y) 0)"
                    if config.edge == "first"
                    else (
                        "(= (y_selected_index y) "
                        "(- (x_length x) 1))"
                    )
                )
                range_source = "(seq.extract (x_source x)"
            self.assertIn(expected_index, text)
            mutations = [
                text.replace(
                    expected_index,
                    (
                        "(= (p_selected_index p) 7)"
                        if config.wrapper
                        else "(= (y_selected_index y) 7)"
                    ),
                    1,
                ),
                text.replace(
                    f"{range_source} {config.remainder_offset}",
                    f"{range_source} 7",
                    1,
                ),
            ]
            if not config.wrapper:
                self.assertIn("(= (y_tuple_selected_first y) true)", text)
                mutations.append(
                    text.replace(
                        "(= (y_tuple_selected_first y) true)",
                        "(= (y_tuple_selected_first y) false)",
                        1,
                    )
                )
            for index, mutated in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    with self.assertRaises(GuardError):
                        edge.validate_target_obligation(
                            config,
                            mutated,
                            metadata,
                        )

    def test_wrapper_replace_split_assignment_order_and_empty_identity(
        self,
    ) -> None:
        for config in (item for item in edge.TARGETS if item.wrapper):
            text, metadata = edge.obligation(config, edge.PRIMARY)
            split = (
                "SplitFirstTransition"
                if config.edge == "first"
                else "SplitLastTransition"
            )
            calls = [
                "(ReplaceWithEmptyTransition x b r)",
                f"({split} r p)",
                "(ReceiverAssignmentTransition x b p y s)",
            ]
            positions = [text.index(call) for call in calls]
            self.assertEqual(positions, sorted(positions))
            reordered = text.replace(
                calls[0] + "\n         " + calls[1],
                calls[1] + "\n         " + calls[0],
                1,
            )
            with self.subTest(target=config.target, mutation="order"):
                with self.assertRaises(GuardError):
                    edge.validate_target_obligation(
                        config,
                        reordered,
                        metadata,
                    )
            empty_identity = edge.source_instance_text(
                config,
                length=0,
                element_size=8,
                extra_assertions=(
                    "(not (= (s_receiver_address s1) "
                    "(b_empty_address b)))",
                ),
            )
            process = run_z3(empty_identity)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stdout, "unsat\n")
            self.assertEqual(process.stderr, "")

    def test_zst_aliasing_is_address_equal_but_range_disjoint(self) -> None:
        for config in edge.TARGETS:
            if config.wrapper:
                address_equality = (
                    "(= (y_selected_address y1) (s_receiver_address s1))"
                )
            else:
                address_equality = (
                    "(= (y_selected_address y1) (y_remainder_address y1))"
                )
            text = edge.source_instance_text(
                config,
                length=5,
                element_size=0,
                extra_assertions=(address_equality,),
            )
            process = run_z3(text)
            with self.subTest(target=config.target):
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stdout, "sat\n")
                self.assertEqual(process.stderr, "")

    def test_empty_singleton_longer_zst_and_non_zst_instances_are_sat(
        self,
    ) -> None:
        for config in edge.TARGETS:
            for name, (length, element_size) in replay.SOURCE_INSTANCES.items():
                process = run_z3(
                    edge.source_instance_text(
                        config,
                        length=length,
                        element_size=element_size,
                    )
                )
                with self.subTest(target=config.target, case=name):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "sat\n")
                    self.assertEqual(process.stderr, "")

    def test_both_exact_theorems_are_unsat(self) -> None:
        for config in edge.TARGETS:
            for purpose in edge.PURPOSES:
                process = run_z3(edge.obligation_text(config, purpose))
                with self.subTest(target=config.target, purpose=purpose):
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_omitting_any_exact_observation_fails_closed(self) -> None:
        for config in edge.TARGETS:
            for purpose in edge.PURPOSES:
                text, metadata = edge.obligation(config, purpose)
                observations = (
                    config.output_fields
                    if purpose == edge.EXACT_OUTPUT
                    else config.output_fields + config.state_fields
                )
                for selector, _ in observations:
                    left = "y1" if selector.startswith("y_") else "s1"
                    right = "y2" if selector.startswith("y_") else "s2"
                    equality = (
                        f"(= ({selector} {left}) ({selector} {right}))"
                    )
                    self.assertIn(equality, text)
                    with self.subTest(
                        target=config.target,
                        purpose=purpose,
                        selector=selector,
                    ):
                        with self.assertRaises(GuardError):
                            edge.validate_target_obligation(
                                config,
                                text.replace(equality, "true", 1),
                                metadata,
                            )

    def test_opaque_relation_and_boundary_laundering_are_rejected(self) -> None:
        config = edge.TARGETS[0]
        text, metadata = edge.obligation(config, edge.PRIMARY)
        opaque = text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
            1,
        )
        start, end = definition_span(opaque, "TargetDefinition_T")
        opaque = (
            opaque[:start]
            + """(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeTarget x b y s))"""
            + opaque[end:]
        )
        opaque_metadata = copy.deepcopy(metadata)
        opaque_metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": [config.source_reference],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(opaque, opaque_metadata)

        old = "      (b_element_size Int))))"
        self.assertIn(old, text)
        laundered = text.replace(
            old,
            "      (b_element_size Int)\n"
            "      (b_selected_index Int))))",
            1,
        ).replace(
            "(InputBoundaryObserved x b)))",
            "(InputBoundaryObserved x b)\n"
            "       (= (y_selected_index y) (b_selected_index b))))",
            1,
        )
        laundering_metadata = copy.deepcopy(metadata)
        laundering_metadata["boundary_fields"].append(
            {
                "selector": "b_selected_index",
                "role": "selected_output",
                "meaning": "laundered answer",
                "source_citations": [config.source_reference],
                "trust_site_ids": list(config.all_trust_site_ids),
                "source_backed_replacement_ids": [],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(laundered, laundering_metadata)

    def test_out_of_scope_ledger_mutation_is_rejected(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        other = next(
            (row["target"], row["input_order"])
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS) | set(edge.TARGET_KEYS)
        )
        for rows in (csv_rows, json_rows):
            row = next(
                item
                for item in rows
                if (item["target"], item["input_order"]) == other
            )
            row.update(runner.COMPLETE)
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_generated_verus_is_target_specific_ordered_and_trusted_free(
        self,
    ) -> None:
        for config in edge.TARGETS:
            text = edge.verus_text(config)
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn(
                    f"conditional_complete_{config.function_name}",
                    text,
                )
                self.assertIn("source_transition", text)
                self.assertIn("exact_equivalent", text)
                self.assertIn(
                    "ordered_wrapper_transition"
                    if config.wrapper
                    else "pattern_split_transition",
                    text,
                )
                if config.wrapper:
                    self.assertLess(
                        text.index("replace_with_empty_transition"),
                        text.index(f"split_{config.edge}_transition"),
                    )
                    self.assertLess(
                        text.index(f"split_{config.edge}_transition"),
                        text.index("receiver_assignment_transition"),
                    )


if __name__ == "__main__":
    unittest.main()
