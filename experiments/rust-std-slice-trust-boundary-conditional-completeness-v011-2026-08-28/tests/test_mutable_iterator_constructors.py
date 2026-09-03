#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from checker_guards import GuardError, validate_obligation
import campaign_common as common
import mutable_iterator_constructors as constructors
import run_mutable_iterator_constructors as runner
import validate_authority_design as authority_validator


def omit_call(text: str, symbol: str) -> str:
    target_start = text.index("(define-fun TargetDefinition_T")
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


def source_anchor_inputs(
    config: constructors.ConstructorTarget,
) -> tuple[str, dict[str, str]]:
    row = next(
        row
        for row in common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        if (row["target"], row["input_order"])
        == (config.target, config.input_order)
    )
    canonical = (
        common.RUST_LIBRARY / constructors.CANONICAL_ITER_PATH
    ).read_text().splitlines(keepends=True)
    private = {
        source.name: "".join(canonical[source.start - 1 : source.end])
        for source in config.private_sources
    }
    return row["source_item_text"], private


class MutableIteratorConstructorGuardTests(unittest.TestCase):
    def test_active_contracts_match_the_live_crosswalk(self) -> None:
        rows = {
            (row["target"], row["input_order"]): row
            for row in common.read_csv(
                ROOT / "crosswalk/target_to_proof_boundary.csv"
            )
        }
        for config in constructors.TARGETS:
            row = rows[(config.target, config.input_order)]
            with self.subTest(target=config.target):
                self.assertEqual(
                    config.active_contract_sha256,
                    row["active_contract_sha256"],
                )
                self.assertEqual(
                    config.active_contract_text, row["active_contract_text"]
                )
                self.assertEqual(
                    set(config.all_trust_site_ids),
                    set(row["all_trust_site_ids"].split(";")),
                )

    def test_literal_theorems_are_checker_valid(self) -> None:
        for config in constructors.TARGETS:
            for purpose in constructors.PURPOSES:
                with self.subTest(target=config.target, purpose=purpose):
                    text, metadata = constructors.obligation(config, purpose)
                    validate_obligation(text, metadata)
                    constructors.validate_target_obligation(
                        config, text, metadata
                    )

    def test_every_active_conjunct_is_live_and_fail_closed(self) -> None:
        for config in constructors.TARGETS:
            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            target = text[text.index("(define-fun TargetDefinition_T") :]
            for conjunct in config.active_conjuncts:
                with self.subTest(target=config.target, conjunct=conjunct):
                    self.assertIn(f"({conjunct}", target)
                    with self.assertRaises(GuardError):
                        constructors.validate_target_obligation(
                            config, omit_call(text, conjunct), metadata
                        )

    def test_every_source_transition_is_live_and_fail_closed(self) -> None:
        for config in constructors.TARGETS:
            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            target_start = text.index("(define-fun TargetDefinition_T")
            for transition in config.source_transitions:
                with self.subTest(target=config.target, transition=transition):
                    self.assertIn(f"(define-fun {transition}", text)
                    self.assertIn(
                        f"({transition}",
                        text[
                            min(
                                text.index(f"(define-fun {transition}"),
                                target_start,
                            ) :
                        ],
                    )
            changed = text.replace(
                f"({config.top_transition} x y)", "true", 1
            )
            with self.assertRaises(GuardError):
                constructors.validate_target_obligation(
                    config, changed, metadata
                )

    def test_boundary_excludes_answers_callbacks_and_traces(self) -> None:
        forbidden = (
            "returned",
            "selected",
            "result",
            "final",
            "trace",
            "callback_result",
            "direction",
            "finished",
            "count",
            "chunk_size",
        )
        for config in constructors.TARGETS:
            metadata = constructors.obligation_metadata(
                config, constructors.PRIMARY
            )
            selectors = [
                field["selector"] for field in metadata["boundary_fields"]
            ]
            with self.subTest(target=config.target):
                self.assertTrue(metadata["boundary_scope"]["narrower_than_target"])
                for selector in selectors:
                    self.assertFalse(
                        any(token in selector for token in forbidden), selector
                    )
                self.assertEqual(
                    constructors.boundary_manifest(config)[
                        "deterministic_source_transition"
                    ]["constructor_callback_invocations"],
                    0,
                )

    def test_opaque_whole_target_relation_is_rejected(self) -> None:
        config = constructors.TARGETS[0]
        text, metadata = constructors.obligation(
            config, constructors.PRIMARY
        )
        text = text.replace(
            "(declare-const x Input)",
            "(declare-fun WholeTarget (Input Boundary Output State) Bool)\n"
            "(declare-const x Input)",
        )
        start = text.index("(define-fun TargetDefinition_T")
        end = text.index("(define-fun Spec_T", start)
        text = (
            text[:start]
            + """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (WholeTarget x b y s))
"""
            + text[end:]
        )
        metadata = copy.deepcopy(metadata)
        metadata["declared_functions"] = [
            {
                "symbol": "WholeTarget",
                "role": "source_transition",
                "source_citations": [config.source_reference],
            }
        ]
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_boundary_output_laundering_is_rejected(self) -> None:
        config = constructors.TARGETS[0]
        text, metadata = constructors.obligation(
            config, constructors.PRIMARY
        )
        old = "      (b_predicate_identity Int))))"
        self.assertIn(old, text)
        text = text.replace(
            old,
            "      (b_predicate_identity Int)\n"
            "      (b_returned_chunk_size Int))))",
            1,
        ).replace(
            "       (InputIdentityObserved x b)))",
            "       (InputIdentityObserved x b)\n"
            "       (>= (b_returned_chunk_size b) 0)))",
            1,
        ).replace(
            f"       ({config.top_transition} x y)",
            f"       ({config.top_transition} x y)\n"
            "       (= (y_chunk_size y) (b_returned_chunk_size b))",
            1,
        )
        metadata = copy.deepcopy(metadata)
        metadata["boundary_fields"].append(
            {
                "selector": "b_returned_chunk_size",
                "role": "selected_output",
                "source_citations": [config.source_reference],
                "trust_site_ids": [config.dependency_trust_site_ids[0]],
            }
        )
        with self.assertRaises(GuardError):
            validate_obligation(text, metadata)

    def test_nonzero_chunk_domain_and_raw_pointer_identity_fail_closed(
        self,
    ) -> None:
        for config in constructors.TARGETS:
            if config.family != "chunks":
                continue
            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            mutations = {
                "zero-domain": text.replace(
                    "(define-fun ActiveChunkDomainConjunct ((x Input)) Bool\n"
                    "  (> (x_parameter x) 0))",
                    "(define-fun ActiveChunkDomainConjunct ((x Input)) Bool\n"
                    "  (>= (x_parameter x) 0))",
                ),
                "raw-address": text.replace(
                    "(= (y_raw_address y) (x_address x))",
                    "(= (y_raw_address y) (+ (x_address x) 1))",
                ),
                "raw-provenance": text.replace(
                    "(= (y_raw_provenance y) (x_provenance x))",
                    "(= (y_raw_provenance y) (x_allocation x))",
                ),
                "chunk-size": text.replace(
                    "(= (y_chunk_size y) (x_parameter x))",
                    "(= (y_chunk_size y) (+ (x_parameter x) 1))",
                    1,
                ),
                "direction": text.replace(
                    f"(= (y_reverse y) {'true' if config.reverse else 'false'})",
                    f"(= (y_reverse y) {'false' if config.reverse else 'true'})",
                    1,
                ),
            }
            for name, changed in mutations.items():
                with self.subTest(target=config.target, mutation=name):
                    self.assertNotEqual(changed, text)
                    with self.assertRaises(GuardError):
                        constructors.validate_target_obligation(
                            config, changed, metadata
                        )

    def test_callback_constructor_defaults_fail_closed(self) -> None:
        for config in constructors.TARGETS:
            if not config.callback:
                continue
            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            mutations = [
                text.replace(
                    "(= (y_callback_calls y) 0)",
                    "(= (y_callback_calls y) 1)",
                    1,
                ),
                text.replace(
                    "(= (y_predicate_state y) (x_predicate_state x))",
                    "(= (y_predicate_state y) (+ (x_predicate_state x) 1))",
                    1,
                ),
            ]
            if config.family == "predicate":
                mutations.extend(
                    (
                        text.replace(
                            f"(= (y_reverse y) "
                            f"{'true' if config.reverse else 'false'})",
                            f"(= (y_reverse y) "
                            f"{'false' if config.reverse else 'true'})",
                            1,
                        ),
                        text.replace(
                            f"(= (y_inclusive y) "
                            f"{'true' if config.inclusive else 'false'})",
                            f"(= (y_inclusive y) "
                            f"{'false' if config.inclusive else 'true'})",
                            1,
                        ),
                    )
                )
            for index, changed in enumerate(mutations):
                with self.subTest(target=config.target, mutation=index):
                    self.assertNotEqual(changed, text)
                    with self.assertRaises(GuardError):
                        constructors.validate_target_obligation(
                            config, changed, metadata
                        )

    def test_source_anchored_finished_false_defaults_fail_closed(self) -> None:
        for artifact_id in (
            "074_core_slice_rsplit_mut",
            "076_core_slice_rsplitn_mut",
            "098_core_slice_split_mut",
        ):
            config = constructors.TARGET_BY_ARTIFACT[artifact_id]
            public, private = source_anchor_inputs(config)
            constructors.validate_source_anchors(config, public, private)

            changed_private = dict(private)
            split = changed_private["SplitMut::new"]
            changed_private["SplitMut::new"] = split.replace(
                "finished: false",
                "finished: true",
                1,
            )
            self.assertNotEqual(changed_private["SplitMut::new"], split)
            with self.subTest(target=config.target, mutation="source-finished"):
                with self.assertRaises(GuardError):
                    constructors.validate_source_anchors(
                        config, public, changed_private
                    )

            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            changed_text = text.replace(
                "(= (y_finished y) false)",
                "(= (y_finished y) true)",
                1,
            )
            self.assertNotEqual(changed_text, text)
            with self.subTest(target=config.target, mutation="smt-finished"):
                validate_obligation(changed_text, metadata)
                with self.assertRaises(GuardError):
                    constructors.validate_target_obligation(
                        config, changed_text, metadata
                    )

    def test_source_anchored_count_default_fails_closed(self) -> None:
        config = constructors.TARGET_BY_ARTIFACT[
            "076_core_slice_rsplitn_mut"
        ]
        public, private = source_anchor_inputs(config)
        constructors.validate_source_anchors(config, public, private)
        changed_private = dict(private)
        counted = changed_private["RSplitNMut::new"]
        changed_private["RSplitNMut::new"] = counted.replace(
            "count: n",
            "count: n + 1",
            1,
        )
        self.assertNotEqual(changed_private["RSplitNMut::new"], counted)
        with self.assertRaises(GuardError):
            constructors.validate_source_anchors(
                config, public, changed_private
            )

        text, metadata = constructors.obligation(
            config, constructors.PRIMARY
        )
        changed_text = text.replace(
            "(= (y_count y) (x_parameter x))",
            "(= (y_count y) (+ (x_parameter x) 1))",
            1,
        )
        self.assertNotEqual(changed_text, text)
        validate_obligation(changed_text, metadata)
        with self.assertRaises(GuardError):
            constructors.validate_target_obligation(
                config, changed_text, metadata
            )

    def test_nested_reverse_constructor_order_is_explicit(self) -> None:
        rsplit = constructors.TARGET_BY_ARTIFACT[
            "074_core_slice_rsplit_mut"
        ]
        rsplit_text = constructors.obligation_text(
            rsplit, constructors.PRIMARY
        )
        self.assertIn(
            "(and (SplitMutNewStorageTransition x y)",
            rsplit_text,
        )
        rsplitn = constructors.TARGET_BY_ARTIFACT[
            "076_core_slice_rsplitn_mut"
        ]
        text = constructors.obligation_text(rsplitn, constructors.PRIMARY)
        split = text.index("(define-fun SplitMutNewStorageTransition")
        reverse = text.index("(define-fun RSplitMutNewStorageTransition")
        counted = text.index("(define-fun RSplitNMutNewTransition")
        self.assertLess(split, reverse)
        self.assertLess(reverse, counted)
        self.assertIn(
            "(and (RSplitMutNewStorageTransition x y)", text[counted:]
        )
        self.assertIn("(= (y_count y) (x_parameter x))", text[counted:])
        for config, transition, replacement in (
            (
                rsplit,
                "(and (SplitMutNewStorageTransition x y)",
                "(and (StoredSliceTransition x y)",
            ),
            (
                rsplitn,
                "(and (RSplitMutNewStorageTransition x y)",
                "(and (SplitMutNewStorageTransition x y)",
            ),
        ):
            original, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            changed = original.replace(transition, replacement, 1)
            self.assertNotEqual(changed, original)
            with self.subTest(target=config.target, mutation="smt-order"):
                validate_obligation(changed, metadata)
                with self.assertRaises(GuardError):
                    constructors.validate_target_obligation(
                        config, changed, metadata
                    )

            public, private = source_anchor_inputs(config)
            changed_config = replace(
                config,
                constructor_chain=tuple(reversed(config.constructor_chain)),
            )
            with self.subTest(target=config.target, mutation="source-order"):
                with self.assertRaises(GuardError):
                    constructors.validate_source_anchors(
                        changed_config, public, private
                    )

    def test_nested_reverse_verus_models_flat_projection(self) -> None:
        rsplit = constructors.verus_text(
            constructors.TARGET_BY_ARTIFACT[
                "074_core_slice_rsplit_mut"
            ]
        )
        self.assertIn("pub ghost struct SplitMutStorage", rsplit)
        self.assertIn("pub ghost struct RSplitMutStorage", rsplit)
        self.assertIn("inner: split_mut_new(input)", rsplit)
        self.assertIn("pub proof fn rsplit_mut_flat_projection", rsplit)
        self.assertIn(
            "let ret = project_rsplit_mut(rsplit_mut_new(input));",
            rsplit,
        )

        rsplitn = constructors.verus_text(
            constructors.TARGET_BY_ARTIFACT[
                "076_core_slice_rsplitn_mut"
            ]
        )
        self.assertIn("pub ghost struct GenericSplitNStorage", rsplitn)
        self.assertIn("pub ghost struct RSplitNMutStorage", rsplitn)
        self.assertIn("iter: rsplit_mut_new(input)", rsplitn)
        self.assertIn("count: input.n", rsplitn)
        self.assertIn("pub proof fn rsplitn_mut_flat_projection", rsplitn)
        self.assertIn(
            "let ret = project_rsplitn_mut(rsplitn_mut_new(input));",
            rsplitn,
        )

    def test_local_validator_reports_56_classified_and_6_not_run(
        self,
    ) -> None:
        rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        self.assertEqual(
            authority_validator.target_result_counts(rows),
            (62, 0),
        )
        self.assertEqual(
            len(authority_validator.TARGET_RESULT_LABELS),
            62,
        )
        summary = authority_validator.target_results_summary(rows)
        for order in ("032", "036", "069", "074", "076", "093", "098"):
            self.assertIn(f"{order}_conditional-complete", summary)
        for order in ("091", "097", "101", "103"):
            self.assertIn(f"{order}_conditional-complete", summary)
        for order in ("037", "043"):
            self.assertIn(f"{order}_conditional-complete", summary)
        for order in ("035", "068"):
            self.assertIn(f"{order}_conditional-complete", summary)
        self.assertTrue(summary.endswith(",0_not-run"))
        self.assertEqual(
            authority_validator.target_result_count_summary(rows),
            "target_result_counts=62_classified,0_not-run",
        )


    def test_split_inclusive_finished_default_handles_empty_and_nonempty(
        self,
    ) -> None:
        config = constructors.TARGET_BY_ARTIFACT[
            "093_core_slice_split_inclusive_mut"
        ]
        text = constructors.obligation_text(config, constructors.PRIMARY)
        self.assertIn("(= (y_finished y) (= (x_length x) 0))", text)
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for length, impossible in ((0, "(not (y_finished y1))"), (3, "(y_finished y1)")):
            process = subprocess.run(
                [str(z3), "-in", "-smt2"],
                input=constructors.source_instance_text(
                    config,
                    length=length,
                    element_size=8,
                    extra_assertions=(impossible,),
                ),
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stdout, "unsat\n")
            self.assertEqual(process.stderr, "")

    def test_empty_nonempty_and_zst_source_instances_are_sat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        cases = ((0, 8), (5, 8), (5, 0))
        for config in constructors.TARGETS:
            for length, element_size in cases:
                with self.subTest(
                    target=config.target,
                    length=length,
                    element_size=element_size,
                ):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=constructors.source_instance_text(
                            config,
                            length=length,
                            element_size=element_size,
                        ),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "sat\n")
                    self.assertEqual(process.stderr, "")

    def test_both_exact_theorems_are_unsat(self) -> None:
        z3 = shutil.which("z3")
        self.assertIsNotNone(z3)
        for config in constructors.TARGETS:
            for purpose in constructors.PURPOSES:
                with self.subTest(target=config.target, purpose=purpose):
                    process = subprocess.run(
                        [str(z3), "-in", "-smt2"],
                        input=constructors.obligation_text(config, purpose),
                        text=True,
                        capture_output=True,
                        timeout=10,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(process.stdout, "unsat\n")
                    self.assertEqual(process.stderr, "")

    def test_omitting_any_exact_observation_fails_closed(self) -> None:
        for config in constructors.TARGETS:
            text, metadata = constructors.obligation(
                config, constructors.PRIMARY
            )
            selectors = (
                selector for selector, _ in config.output_fields + config.state_fields
            )
            for selector in selectors:
                left = "y1" if selector.startswith("y_") else "s1"
                right = "y2" if selector.startswith("y_") else "s2"
                equality = f"(= ({selector} {left}) ({selector} {right}))"
                with self.subTest(target=config.target, selector=selector):
                    self.assertIn(equality, text)
                    with self.assertRaises(GuardError):
                        constructors.validate_target_obligation(
                            config, text.replace(equality, "true"), metadata
                        )

    def test_stale_rsplitn_citation_is_reconciled_not_overwritten(self) -> None:
        config = constructors.TARGET_BY_ARTIFACT[
            "076_core_slice_rsplitn_mut"
        ]
        self.assertEqual(
            config.private_sources[-1].citation,
            "core/src/slice/iter.rs:1289-1293",
        )
        rows = common.read_csv(ROOT / "crosswalk/trust_site_inventory.csv")
        record = next(
            row for row in rows if row["record_id"] == "TS-076-C003"
        )
        self.assertEqual(
            record["source_lines"], "core/src/slice/iter.rs:1223-1225"
        )
        self.assertIn('"signature_start_line":1223', record["raw_record_json"])

    def test_out_of_scope_ledger_mutation_is_rejected(self) -> None:
        csv_rows = common.read_csv(
            ROOT / "crosswalk/target_to_proof_boundary.csv"
        )
        json_rows = json.loads(
            (ROOT / "crosswalk/target_to_proof_boundary.json").read_text()
        )
        other_key = next(
            (row["target"], row["input_order"])
            for row in csv_rows
            if (row["target"], row["input_order"])
            not in set(runner.BASELINE_RESULTS)
            | set(constructors.TARGET_KEYS)
        )
        for rows in (csv_rows, json_rows):
            row = next(
                item
                for item in rows
                if (item["target"], item["input_order"]) == other_key
            )
            row.update(runner.COMPLETE)
        with self.assertRaises(ValueError):
            runner.prepare_crosswalk_reset(csv_rows, json_rows)

    def test_generated_verus_is_target_specific_and_has_no_external_body(
        self,
    ) -> None:
        for config in constructors.TARGETS:
            text = constructors.verus_text(config)
            function = config.target.rsplit("::", 1)[-1]
            with self.subTest(target=config.target):
                self.assertNotIn("external_body", text)
                self.assertIn(f"{function}_constructor", text)
                self.assertIn(f"conditional_complete_{function}", text)
                self.assertIn("target_transition", text)
                self.assertIn("exact_equivalent", text)


if __name__ == "__main__":
    unittest.main()
