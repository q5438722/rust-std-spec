# alloc::vec module-first workspace

This isolated workspace freezes the first `alloc::vec` module-first inputs after the reviewed `core::slice::select_nth_unstable*` mission completed.

Protected trees are read-only inputs for this workspace: `/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96`, `/home/chentianyu/nanvix-rust-std-spec-survey/verus`, `/home/chentianyu/nanvix-rust-std-spec-survey/results`, and the completed slice workspace.

Initial artifacts:

- `rust-alloc-vec/vec/**`: complete Rust 1.96 `library/alloc/src/vec/**` source copy.
- `rust-alloc-adjacent/`: directly required adjacent alloc sources for raw allocation/capacity, `TryReserveError`, allocator traits, and boxed-slice conversions.
- `vstd-baseline/std_specs/{vec,capacity}.rs`: copied vstd baselines used by the 24 exact existing-vstd rows.
- `results/{modules,coverage}.csv`: local frozen authority snapshots.
- `inventory/vec_exec_fn_inventory.*`: 49 stable unique executable API inventory.
- `inventory/vec_existing_vstd_exact_match_audit.*`: exact target/signature-shape audit for the 24 stable vstd-covered rows.
- `inventory/vec_unstable_exclusions.*`: 28 excluded unstable alloc::vec rows.
- `specs/{existing_vstd_vec_specs.rs,generated_vec_specs.rs,all_vec_specs.rs,vec_shared_vocabulary.rs}`: integrated exact-vstd rows, generated executable rows, merged markers, and shared Vec vocabulary.
- `catalog/vec_spec_catalog.*`: 49-row catalog with 24 exact-vstd rows, 24 generated executable rows, and one source-backed justified no-spec record for `Vec::splice`.
- `verification/`: module-first validators, helper audit, Verus no-verify evidence, and supervised feedback determinism runner/wrapper.

Decisive bootstrap verifier:

```sh
python3 verification/check_inventory.py --modules-csv results/modules.csv --inventory inventory/vec_exec_fn_inventory.csv --expect-total 49 --expect-existing-vstd 24 --expect-unstable 28
```

The local Verus typecheck harness intentionally includes only
`specs/generated_vec_specs.rs`: the 24 exact existing-vstd contracts are already
loaded by vstd and would be duplicate declarations if redeclared in the harness.
`Vec::splice` is recorded in `catalog/vec_justified_no_spec_records.*` because
the exact stable signature requires `Splice<'_, I::IntoIter, A>`, and Verus does
not currently expose the `IntoIterator::IntoIter` associated type for that
external trait without narrowing the API shape.
