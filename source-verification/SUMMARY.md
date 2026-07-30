# Source-level verification of generated Rust std contracts

- Derived contracts: **101**
- Without `duration_float_ieee_semantics()`: **93**
- Conditional on the float target axiom: **8**
- All harnesses passed: **True**

| Harness | Contracts | Level | Verus result | Trusted basis |
|---|---:|---|---|---|
| `pure_control_flow.rs` | 16 | A | 16 verified, 0 errors | Copied enum matches; no lower external contract is needed. |
| `residual.rs` | 2 | C | 3 verified, 0 errors | Copied FromResidual bodies using FromSpec plus one trusted axiom that core::convert::Infallible is uninhabited. |
| `vecdeque.rs` | 2 | B | 2 verified, 0 errors | Copied control flow, using trusted len/swap/pop_front/pop_back contracts. |
| `collections.rs` | 6 | B | 6 verified, 0 errors | Copied one-line compositions using trusted len/get/new contracts. |
| `capacity_composed.rs` | 4 | B | 4 verified, 0 errors | Source-equivalent constructor compositions using trusted new/reserve and capacity contracts. |
| `net.rs` | 15 | B | 19 verified, 0 errors | Copied/desugared address operations using trusted octets/constructor contracts. |
| `net_enums.rs` | 7 | B | 7 verified, 0 errors | Copied IpAddr enum matches using the structural enum View and lower IPv4/IPv6 contracts. |
| `socket_addr.rs` | 7 | B | 11 verified, 0 errors | Copied SocketAddr enum matches using the structural enum View and lower SocketAddrV4/V6 contracts. |
| `ffi.rs` | 4 | B | 4 verified, 0 errors | Copied public compositions using trusted CStr/CString view-producing methods. |
| `layout.rs` | 7 | C | 9 verified, 0 errors | Public-API copies plus trusted Layout view validity and two rounding lemmas; private Alignment internals are inaccessible downstream. |
| `duration_integer.rs` | 19 | C | 19 verified, 0 errors | Integer/public-API copies plus the trusted invariant duration@ <= Duration::MAX. |
| `duration_from_secs.rs` | 2 | B | 2 verified, 0 errors | Copied panic wrappers using the lower try_from_secs_f32/f64 contracts; the error branch is proved unreachable from the validity precondition. |
| `duration_try_from.rs` | 2 | E | 12 verified, 0 errors | Source-faithful f32/f64 control flow, but the complete rounding/overflow equivalence remains in two trusted arithmetic-model axioms; the private error representation is only modeled by a local mirror. |
| `duration_float.rs` | 8 | D | 10 verified, 0 errors | Copied float bodies under duration_float_ieee_semantics() and explicit RFC 3514 bridges from relational executable float specs to IEEE spec operators. |

## Levels

- **A:** copied body proves the contract without another Rust external contract.
- **B:** copied body is verified compositionally from smaller trusted std contracts.
- **C:** additionally depends on a trusted representation/type invariant.
- **D:** additionally depends on an explicit target-semantics axiom.
- **E:** source control flow is copied, but the central numerical/error
  equivalence is still captured by a large trusted model axiom.

A successful harness removes trust from the target contract only relative to its
listed lower-level assumptions. It does not prove the Rust compiler or private
standard-library representation itself.

## Nanvix floating-point target assessment

- `x86-user.json`: `['target_feature="x87"']`
  `duration_float_ieee_semantics()` is not established because SSE2 is not
  enabled in the effective cfg; RFC 3514 documents finite-result excess-
  precision deviations on 32-bit x86 without SSE2.
- `x86-kernel.json`: `['target_feature="x87"']`
  the target requests soft-float, but the compiler-builtins path still needs
  a separate conformance audit before the predicate can be assumed.
