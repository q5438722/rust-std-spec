import unittest

import test_endpoint_export_cli


class SplitExportCLI(test_endpoint_export_cli.EndpointExportCLI):
    GROUP = "splits"
    APIS = ("split_first", "split_last")
    INVALID_API = "first"
    LOG_ENV = "SPLIT_EXPORT_TEST_LOG_DIR"
    GUARDS = (
        "g_slice_leneq", "g_slice_lenrng",
        "g_r1_is_Some", "g_r1__Some_0_1_leneq", "g_r1__Some_0_1_lenrng", "g_r1_is_None",
        "g_r2_is_Some", "g_r2__Some_0_1_leneq", "g_r2__Some_0_1_lenrng", "g_r2_is_None",
        "g_neq_tuple",
    )

    def test_element_remainder_and_order_cannot_be_dropped_from_comparison(self):
        native = ["results", 0, "proofs", 0, "native", "det_spec"]
        for phase in ("analyze", "replay"):
            for case, before, after in (
                ("element-only",
                 "((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1))",
                 "(r1->Some_0.0 == r2->Some_0.0)"),
                ("remainder-only",
                 "((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1))",
                 "(r1->Some_0.1 =~= r2->Some_0.1)"),
                ("remainder-length",
                 "(r1->Some_0.1 =~= r2->Some_0.1)",
                 "(r1->Some_0.1.len() == r2->Some_0.1.len())"),
                ("swapped-components",
                 "((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1))",
                 "((r1->Some_0.1 == r2->Some_0.1) && (r1->Some_0.0 =~= r2->Some_0.0))"),
            ):
                with self.subTest(phase=phase, case=case):
                    def change(project, p=phase, before=before, after=after):
                        _, report = self.report(project, p)
                        equal = report["results"][0]["proofs"][0]["native"]["det_spec"]["equal_fn_def"]
                        self.assertIn(before, equal)
                        self.alter_report(project, native + ["equal_fn_def"], equal.replace(before, after), p)
                    self.check_case(f"{phase}-{case}", change)


if __name__ == "__main__":
    unittest.main()
