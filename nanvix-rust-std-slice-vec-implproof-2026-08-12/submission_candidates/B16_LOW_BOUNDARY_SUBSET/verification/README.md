# B16 specification verification

`typecheck_b16_specs.rs` loads the merged submission specs. Run:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus \
  typecheck_b16_specs.rs --no-verify
```

`check_source_subset.py` compares all 16 contracts and 20 selected helper items
against the active module-first Slice artifacts after removing whitespace.
Recorded results are under `evidence/`.
