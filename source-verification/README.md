# Source-level contract verification

These harnesses copy or source-faithfully desugar Rust 1.96 standard-library
implementations into ordinary Verus functions. The functions carry the same
postconditions as the generated `assume_specification` declarations, so Verus
checks the body rather than trusting the target method's contract.

Run all harnesses with:

```bash
cd /home/chentianyu/nanvix-rust-std-spec-survey/source-verification
./verify_all.py
```

The verification is deliberately stratified:

- **A:** self-contained enum/control-flow proof;
- **B:** composition from smaller trusted std contracts;
- **C:** composition plus a trusted external-type invariant;
- **D:** composition plus explicit target floating-point semantics.
- **E:** source control flow is copied, but the central mathematical/error
  equivalence is still represented by a large trusted model axiom.

The main remaining blockers are:

- private standard-library representation with no public operation exposing the
  required state (`Location::file_as_c_str`);
- guard/drop protocols (`BinaryHeap::peek_mut`);
- generic conversion laws (`CString::new`);
- intentionally representation-dependent results such as
  `VecDeque::binary_search` with duplicate elements.

`Duration::try_from_secs_f32/f64` now have source-faithful bit-level control
flow, but they remain Level E. Two arithmetic-model axioms encode the complete
shift/round-to-even equivalence, and a local mirror stands in for the private
error representation. They therefore should not be counted as fully derived
numerical proofs.

`duration_float.rs` is conditional on
`duration_float_ieee_semantics()`. This is necessary because vstd intentionally
models executable Rust float operators relationally: RFC 3514 permits
non-deterministic NaN payloads, and some non-conforming legacy targets can also
have excess-precision differences.

## All-contract campaign

The bulk campaign covers all **539** direct vstd `assume_specification`
records. Initially, 406 harnesses mechanically passed Verus. A strict
source/implementation audit then retained only **190** as faithful and
downgraded **216** alternate/circular/target-axiom proofs. Together with the
original 133 blockers, this yields **349** external-body fallbacks.

The successful APIs are copied per contract record under:

```text
source-verification/proved-apis/
```

The final report is:

```text
source-verification/bulk-proof/FINAL-REPORT.md
```

The complete grouped suite is:

```text
source-verification/organized-suite/
```

It contains 168 strict-faithful local surrogate records across 141 unique
proof artifacts and 371 same-signature `#[verifier::external_body]`
fallbacks, grouped by original vstd file. These are not direct proofs of the
external Rust std symbols. Run all 539 entries with:

```bash
cd source-verification/organized-suite
./verify.sh
```

Latest result: **539 passed, 0 failed**.
