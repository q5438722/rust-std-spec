# Proved Rust std API contracts

Each child directory represents one direct vstd `assume_specification` record with a passing Verus source-level proof harness:

- `proof.rs`: passing Verus proof harness;
- `contract.rs`: original vstd contract;
- `rust_source.rs`: copied Rust 1.96 implementation when available;
- `api.json`: API/declaration metadata;
- `metadata.json`: proof provenance and trust classification.

Current directories: **406**.
