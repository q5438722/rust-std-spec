# Strict implementation-fidelity retry

| Result | Count |
|---|---:|
| Previously alternate-implementation records retried | 204 |
| Verus-passing retry artifacts | 20 |
| Blocked under exact-body policy | 184 |
| Accepted after independent fidelity review | **19** |
| Passing retry artifacts rejected by review | 1 |

## Blocker categories

| Category | Count |
|---|---:|
| `private_or_internal_operation_inaccessible` | 87 |
| `other_strict_fidelity_blocker` | 46 |
| `verus_or_compiler_operation_unavailable` | 33 |
| `exact_operation_is_target_or_circular` | 12 |
| `missing_lower_contract_or_model_bridge` | 6 |

## Newly accepted records

- `std_specs__core.rs__L165__core__intrinsics__likely` — The surrogate reproduces the exact if/else body and the exact empty cold_path body (419); only Verus contracts/attributes are added. No target axiom or cycle is used.
- `std_specs__duration.rs__L186__Duration__from_hours` — The overflow test, panic branch, multiplication order, and Duration::from_secs call are preserved; panic! is mechanically represented by vpanic! plus a proof-only unreachable assertion. Duration::from_secs is a smaller acyclic std contract.
- `std_specs__duration.rs__L193__Duration__from_mins` — The overflow test, panic branch, multiplication, and Duration::from_secs call are preserved; panic! is mechanically represented by vpanic! plus a proof-only unreachable assertion. Duration::from_secs is a smaller acyclic std contract.
- `std_specs__duration.rs__L250__Duration__abs_diff` — The checked_sub/else/reverse-checked_sub/unwrap executable body is exact. Duration::checked_sub and Option::unwrap are smaller acyclic std contracts; there is no target cycle or target-equivalent axiom.
- `std_specs__duration.rs__L350__Duration__from_secs_f32` — The try_from_secs_f32 match and Err panic are preserved exactly; only the panic macro is mechanically adapted for Verus. Duration::try_from_secs_f32 is a smaller acyclic std contract.
- `std_specs__layout_value.rs__L161__Layout__repeat` — The proof mechanically rewrites the two let-else constructs as matches while preserving every return, error branch, debug assertion, and call. pad_to_align, repeat_packed, extend_packed, size, and checked_sub are smaller acyclic contracts.
- `std_specs__net.rs__L288__Ipv6Addr__is_multicast` — The executable segments()[0] mask comparison is exact; the temporary and bit-vector/view facts are proof-only. The segments/view-length facts are smaller acyclic representation contracts, not the target result.
- `std_specs__net.rs__L293__Ipv6Addr__is_unique_local` — The executable segments()[0] mask comparison is exact after introducing a local; all arithmetic and bit-vector steps are proof-only. Ipv6Addr::segments and view facts are smaller acyclic contracts.
- `std_specs__net.rs__L298__Ipv6Addr__is_unicast_link_local` — The executable segments()[0] mask comparison is exact after introducing a local; all range/bit-vector reasoning is proof-only. Ipv6Addr::segments and view facts are smaller acyclic contracts.
- `std_specs__net.rs__L469__IpAddr__to_canonical` — The two match arms and the call to the original Ipv6Addr::to_canonical method are exact; the length fact is ghost-only. Ipv6Addr::to_canonical is a distinct smaller acyclic std contract, not a peer surrogate.
- `std_specs__net.rs__L522__Ipv6Addr__from_segments` — The array destructuring pattern is mechanically expanded to eight indexed locals, followed by the same Ipv6Addr::new call in the same order. Ipv6Addr::new is a smaller acyclic std contract.
- `std_specs__net.rs__L631__SocketAddr__set_ip` — The proof uses match ergonomics instead of explicit &mut/ref mut patterns but preserves the same three arms, same-family setters, and cross-family Self::new(new_ip, port()) assignment. Those called methods are smaller acyclic std contracts.
- `std_specs__option.rs__L160__Option__T__unwrap` — The Some/None match and call to a locally copied unwrap_failed helper are exact; the helper preserves the source panic text/body (2250-2252), with only Verus panic plumbing and proof preconditions added. No assumed target semantics are used.
- `std_specs__option.rs__L395__Option__insert` — The assignment and unsafe as_mut().unwrap_unchecked() return are exact. The explicit unwrap_unchecked specification is a smaller acyclic std contract and does not restate Option::insert.
- `std_specs__result.rs__L177__Result__T__E__unwrap` — The Ok/Err match, exact message, and unwrap_failed call are preserved; the source helper bodies (1869-1883) are copied with only mechanical panic-macro/Verus specification adaptation. No target axiom or cycle is present.
- `std_specs__result.rs__L196__Result__T__E__unwrap_err` — The Ok/Err match, exact message, and unwrap_failed call are preserved; both source helper configurations (1869-1883) are copied with only mechanical panic-macro/Verus specification adaptation. No target axiom or cycle is present.
- `std_specs__result.rs__L215__Result__T__E__expect` — The Ok/Err match and unwrap_failed(msg, &e) call are preserved; the applicable source helper (1869-1871) is copied with only mechanical panic-macro/Verus specification adaptation. No target axiom or cycle is present.
- `std_specs__slice.rs__L194__T__split_at` — The split_at_checked match, Some return, None panic, and panic text are preserved; only the panic macro is mechanically adapted. The explicit split_at_checked specification is a smaller acyclic std contract.
- `std_specs__slice.rs__L92__core__hint__unreachable_unchecked` — The proof mechanically expands assert_unsafe_precondition! using ub_checks.rs:53-81 and reproduces check_language_ub (96-108), then makes the same intrinsics::unreachable call. The intrinsic contract is a smaller acyclic std contract; ghost-only helper variants do not change reachable target behavior under requires false.
