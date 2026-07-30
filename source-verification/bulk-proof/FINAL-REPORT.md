# Final Rust std source-proof campaign

## Result

| Metric | Count |
|---|---:|
| Direct `assume_specification` records | 539 |
| Unique API paths | 447 |
| Previously proved/exported | 101 |
| Remaining records attempted | 438 |
| Newly proved | 305 |
| Total proved | **406** |
| Strict-faithful admissible local surrogates | **168** |
| Passing artifacts not retained | **238** |
| Blocked after attempts/retries | **133** |
| Total proof rate | **75.32%** |
| New-proof success rate | **69.63%** |

The accepting files verify local surrogate functions. No
original external Rust std symbol is directly proved, and one accepting
artifact has an incorrect target mapping.

At unique API-path level:

- fully proved: **324**;
- partially proved (multiple contract records): **5**;
- blocked-only: **118**.

All 406 copied proof files were independently rerun:

```text
406 passed, 0 failed
```

## Trust levels of strict retained local surrogates

| Level | Count | Meaning |
|---|---:|---|
| A | 54 | Body proof without another Rust external contract |
| B | 112 | Composition from smaller trusted contracts |
| C | 2 | Also needs a representation/compiler invariant |
| D | 0 | Also needs target/runtime semantic assumptions |
| E | 0 | Central equivalence remains represented by a large model axiom |

## Blocked categories

| Category | Count |
|---|---:|
| `private_or_opaque_representation` | 90 |
| `other` | 18 |
| `verus_tooling_gap` | 9 |
| `iterator_guard_or_lifetime` | 8 |
| `allocator_or_capacity` | 4 |
| `trait_or_higher_order_law` | 3 |
| `unsafe_pointer_or_provenance` | 1 |

Largest blocked source modules:

- `std_specs__hash.rs`: 37
- `std_specs__btree.rs`: 23
- `std_specs__ffi.rs`: 14
- `std_specs__capacity.rs`: 13
- `std_specs__collections_extra.rs`: 12
- `std_specs__net.rs`: 11
- `std_specs__layout_value.rs`: 3
- `std_specs__location.rs`: 3
- `std_specs__range.rs`: 3
- `string.rs`: 3
- `std_specs__duration.rs`: 2
- `std_specs__maybe_uninit.rs`: 2
- `std_specs__vecdeque.rs`: 2
- `slice.rs`: 1
- `std_specs__core.rs`: 1

## Proved API directory

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/proved-apis
```

Each child directory contains:

- `proof.rs` — passing Verus harness;
- `contract.rs` — original vstd contract;
- `rust_source.rs` — copied Rust 1.96 implementation when available;
- `api.json` — API and declaration metadata;
- `metadata.json` — trust level and proof provenance.

No copied proof contains `assume(...)`, `admit()`,
`#[verifier::external_body]`, `unimplemented!()`, or `todo!()`.

## Organized one-click suite

The conservative 539-item suite is grouped by original vstd file:

```text
/home/chentianyu/nanvix-rust-std-spec-survey/source-verification/organized-suite
```

Run:

```bash
cd /home/chentianyu/nanvix-rust-std-spec-survey/source-verification/organized-suite
./verify.sh
```

Latest result: **539 passed, 0 failed** (168 strict-faithful local-surrogate records across 141 unique proof artifacts + 371 external-body fallbacks).
