# Strict proof/source fidelity audit

| Metric | Count |
|---|---:|
| Mechanically passing proof harnesses before audit | 406 |
| Retained strict-faithful admissible local surrogates | **168** |
| Passing artifacts not retained | **238** |

No original Rust std symbol is directly proved. The conservative policy
retains only local `source_*` surrogates whose executable bodies are exact
copies or mechanical desugarings and whose proof artifacts are admissible.
Alternate algorithms, target-critical axioms, wrong mappings, unresolved
source bodies, and blocked records use external-body fallback.

## Retained trust levels

| Level | Count |
|---|---:|
| B | 112 |
| A | 54 |
| C | 2 |

## Largest not-retained groups

- `std_specs/duration.rs`: 30
- `std_specs/vecdeque.rs`: 24
- `std_specs/vec.rs`: 21
- `std_specs/net.rs`: 21
- `std_specs/cmp.rs`: 14
- `std_specs/ffi.rs`: 11
- `std_specs/capacity.rs`: 11
- `std_specs/ops.rs`: 10
- `std_specs/layout_value.rs`: 9
- `std_specs/collections_extra.rs`: 8
- `std_specs/smart_ptrs.rs`: 8
- `std_specs/bits.rs`: 8
- `std_specs/slice.rs`: 8
- `string.rs`: 8
- `std_specs/hash.rs`: 6
- `std_specs/ordering.rs`: 6
- `layout.rs`: 4
- `std_specs/option.rs`: 4
- `std_specs/nonzero.rs`: 3
- `std_specs/maybe_uninit.rs`: 3

## Strict organized suite

- Strict-faithful local-surrogate proofs: **168**
- External-body fallbacks: **371**
- Full run: **539 passed, 0 failed**
