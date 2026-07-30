# Determinism-feedback comparison

Both columns use the same **2,121 targets**. `With feedback` means using spec determinism as feedback.

## Pure determinism-feedback status table
We generate specs for 268 functions. and 1853 are classified as no spec

| Status | No feedback | With feedback | Delta |
|---|---:|---:|---:|
| `complete` | 150 | 225 | +75 |
| `unknown` | 68 | 40 | -28 |
| `trivial_equality` | 19 | 3 | -16 |
| `incomplete (sat reported by Z3)` | 0 | 0 | +0 |
| `no_spec` | 1884 | 1853 | -31 |


## Why no specification was produced

| Reason                                       | Meaning                                                                       | With feedback | With-feedback share |
| -------------------------------------------- | ----------------------------------------------------------------------------- | ------------: | ------------------: |
| `runtime_or_hidden_state`                    | Result depends on OS/runtime/process state not exposed by a stable pure view. |           456 |              24.61% |
| `needs_new_vstd_abstraction`                 | Required semantic vocabulary or owner/module model is absent from vstd.       |           346 |              18.67% |
| `trait_contract_integration`                 | Requires editing or composing an external trait specification.                |           201 |              10.85% |
| `concurrency_or_hidden_state`                | Atomic/concurrent state is not represented by an ordinary deterministic view. |           179 |               9.66% |
| `unsafe_or_representation_sensitive`         | Raw pointer, provenance, unsafe, or representation-sensitive behavior.        |           150 |               8.09% |
| `determinism_checker_unsupported`            | Current checker cannot encode the exact output or mutable post-state.         |           124 |               6.69% |
| `iterator_or_adapter_result`                 | Iterator/guard/adapter result needs a prophetic or state-transition model.    |           101 |               5.45% |
| `toolchain_unavailable`                      | API is unavailable in the Verus Rust 1.96 toolchain.                          |            70 |               3.78% |
| `formatting_effect`                          | Formatting state and emitted effects are not modeled.                         |            67 |               3.62% |
| `representation_or_allocator`                | Allocator or private representation state is absent from the public view.     |            40 |               2.16% |
| `higher_order_contract`                      | Closure/callback semantics require call-ensures or a higher-order model.      |            39 |               2.10% |
| `ownership_or_uninitialized_model`           | Linear ownership, initialization, or MaybeUninit state is not modeled.        |            25 |               1.35% |
| `complex_result_or_pattern_model`            | Result discriminant/pattern semantics need an additional model.               |            20 |               1.08% |
| `associated_type_or_projection`              | Associated-type/projection signature requires manual integration.             |            17 |               0.92% |
| `no_modeled_observable_output`               | No return value or mutable output is represented by the checker.              |             9 |               0.49% |
| `needs_borrowed_key_or_ordering_model`       | Borrow<Q> functionality or cross-type ordering is missing.                    |             4 |               0.22% |
| `needs_pointer_identity_or_provenance_model` | Semantic views erase location, identity, address, or provenance.              |             3 |               0.16% |
| `needs_functional_trait_semantics`           | Clone/Default is only relational and do_                                      |      2         |          0.11%           |
