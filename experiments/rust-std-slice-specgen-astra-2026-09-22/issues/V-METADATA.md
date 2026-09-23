# The slice length source expression is rejected at pointer coercion

Independent review reproduced this Verus reference-conversion limitation and
the isolated metadata-call limitation described below.
The original Rust implementation is not alleged to be defective.

The source is Rust 1.96 `library/core/src/slice/mod.rs:101-118`.
Its complete executable body is `ptr::metadata(self)`. The delegated body at
`core/src/ptr/metadata.rs:101-103` calls `ptr_metadata`, whose intrinsic
declaration and MIR meaning appear at `core/src/intrinsics/mod.rs:2951-2958`.
The metadata docs at `ptr/metadata.rs:12-27` describe the slice element count.

On official unmodified Verus `0.2026.09.20.aef82ed`, matching vstd, host Rust
`1.98.1`, the source-derived proof
[`proofs/correctness/slice/len.rs`](../proofs/correctness/slice/len.rs)
is rejected before any source-body proof obligation is discharged:

```text
error: The verifier does not yet support the following Rust feature: dereferencing a pointer (here the dereference is implicit)
  --> proofs/correctness/slice/len.rs:13:19
   |
13 |     ptr::metadata(slice)
   |                   ^^^^^
```

The actual command and diagnostic are preserved by this command and
[`logs/foundation/correctness/len/verus.log`](../logs/foundation/correctness/len/verus.log):

```sh
toolchain/verus-x86-linux/verus proofs/correctness/slice/len.rs \
  --crate-type lib --crate-name slice_len_source --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/foundation/correctness/len/queries \
  -o target/foundation/libslice_len_source.rlib
```

The same candidate predicates compile in the root aggregate, with two checked
consistency lemmas. The Engineer's retained Rust 1.96 native probes compiled
and executed all six source expressions. Neither observation proves this
length body. Existing vstd `spec_slice_len` and `axiom_spec_len` are not a
source bridge for the metadata operation.

The initial isolated diagnostic proposal spelled the implicit coercion explicitly
as `ptr::metadata(slice as *const [T])`. This changes the proof copy's
executable syntax and was raised here **before** the exploratory copy was
written. It was not adopted. Any future adoption requires independent comparison of the original
implicit conversion with the proposed cast, the exact metadata operation,
legal inputs (including zero-sized and non-Copy elements), safety, constness,
lifetimes, and the value-view bridge. Passing that rewritten proof alone
would not establish the original source correspondence. No new metadata
axiom or target postcondition is permitted.

The isolated proposal
[`issues/repros/metadata_explicit_cast.rs`](repros/metadata_explicit_cast.rs)
was tested without adoption and produced the same coercion rejection; its
diagnostic is in
[`logs/foundation/metadata-cast/verus.log`](../logs/foundation/metadata-cast/verus.log).
Thus simply spelling the cast does not address the limitation.

To isolate the delegated operation, a second minimal reproduction,
[`issues/repros/metadata_raw.rs`](repros/metadata_raw.rs), takes an already-raw
`*const [T]` and asks for its existing `PtrData::metadata` value. It removes
reference conversion from the experiment, not from the candidate source.
The command is:

```sh
toolchain/verus-x86-linux/verus issues/repros/metadata_raw.rs \
  --crate-type lib --no-cheating --num-threads 1 --log-all \
  --log-dir logs/foundation/metadata-raw/queries
```

The actual diagnostic in
[`logs/foundation/metadata-raw/verus.log`](../logs/foundation/metadata-raw/verus.log)
is:

```text
error: `core::ptr::metadata::metadata` is not supported
  --> issues/repros/metadata_raw.rs:10:5
```

The compiler's suggestion to add `assume_specification` is **not adopted**:
assuming the missing operation's answer would not prove the original
metadata implementation or its connection to the slice view. The existing
pointer model at `toolchain/upstream/source/vstd/raw_ptr.rs:70-95` represents
metadata but does not supply that executable call's contract.

The expected result is a checked source connection from the actual pointer
metadata operation to the existing slice value view. There are two observed
obstacles: reference conversion and the unsupported delegated function.
No tested encoding on this baseline has discharged them.
The API remains incomplete. Independent review confirmed both limitations,
not a Rust std defect or a completed source proof; see the
[review account](../inventory/COVERAGE.md#independent-review-and-redundancy-repair).
No external issue has been filed; filing awaits separate authorization.

The candidate and both proof tracks are joined in
[`inventory/coverage.tsv`](../inventory/coverage.tsv). The completeness proof
[`proofs/completeness/slice/len.rs`](../proofs/completeness/slice/len.rs)
has a real deterministic specdet result, but that does not discharge the
metadata implementation proof.

During the slice-default constructor integration, the unchanged
[`is_empty.rs`](../proofs/correctness/slice/is_empty.rs) source proof was
compiled with `--no-cheating` again. That integration's
[`command`](../logs/defaults/correctness/is_empty/command.txt) and
[`output`](../logs/defaults/correctness/is_empty/verus.log) record one
verified target function and two imported consistency lemmas. This is a
proof of `slice.len() == 0` using the selected vstd's existing `len`
contract, not a proof of the Rust metadata chain above. The new constructor
clients exercise that exact bounded result. No failed metadata attempt was
rerun or changed in that original integration. The later independent review
reproduced both metadata blockers and confirmed the bounded `is_empty`
result, still conditional on existing vstd `len`. Reviewer's native runtime
rerun stopped for missing `cc` before behavior tests, so the retained
Engineer native-test results are not independently reproduced results.

## Singleton array delegation on the same baseline

The same reference-conversion diagnostic now occurs in the unchanged
Rust 1.96 array delegates used by `core::slice::from_ref` and
`core::slice::from_mut`. Independent review has now reproduced this scope;
the earlier independent findings above remain unchanged.

The slice docstrings and bodies are `slice/raw.rs:198,203-205` and
`slice/raw.rs:207,211-213`. They delegate to the array docstrings and bodies
at `array/mod.rs:163-169,171-177`. In
[`array/singleton.rs`](../proofs/correctness/array/singleton.rs), the original
expressions remain:

```rust
unsafe { &*(s as *const T).cast::<[T; 1]>() }
unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }
```

The actual array-only `--compile --no-cheating` run returns exit code 1:

```text
error: The verifier does not yet support the following Rust feature: dereferencing a pointer (here the dereference is implicit)
  --> proofs/correctness/array/singleton.rs:14:17
   |
14 |     unsafe { &*(s as *const T).cast::<[T; 1]>() }
   |                 ^

error: The verifier does not yet support the following Rust feature: dereferencing a pointer (here the dereference is implicit)
  --> proofs/correctness/array/singleton.rs:24:21
   |
24 |     unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }
   |                     ^
```

The command and full output are in
[`logs/singletons/correctness/array/`](../logs/singletons/correctness/array/).
The two slice source files import and jointly check these delegates, rather
than assuming their missing contracts; their separate attempted compilations
are recorded in
[`correctness/from_ref/`](../logs/singletons/correctness/from_ref/) and
[`correctness/from_mut/`](../logs/singletons/correctness/from_mut/).
No target or imported dependency function was verified in these runs.

The minimal
[`singleton_reference_casts.rs`](repros/singleton_reference_casts.rs)
contains only the two reference-to-pointer conversions, with no candidate
predicate, postcondition or array dereference. It produces the same two
diagnostics:
[`command`](../logs/singletons/reference-cast-repro/command.txt),
[`output`](../logs/singletons/reference-cast-repro/stderr.log).
This isolates the observed rejection to those conversions. It does not
establish whether the later pointer cast and dereference could be verified
after that obstacle was removed.

The independent record is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/d67769d288a6/round-0001.json`.
Reviewer ran the array file and both slice files with
`--compile --no-cheating`, reproduced the two array diagnostics at lines
14 and 24, and reproduced the contract-free casts. Each slice run verified
zero target functions and zero imported dependency functions; the array run
verified neither of its two targets. Reviewer also located the explicit
rejection in the selected upstream
`toolchain/upstream/source/rust_verify/src/rust_to_vir_expr.rs:1688-1693`,
in the `AutoBorrow::RawPtr` branch. This is a frontend failure before
source proof generation, not an unproved postcondition that a stronger
candidate would repair.

The existing vstd array view and array-to-slice coercion contracts do not
prove that either Rust array constructor satisfies its singleton predicate.
Adding assumed array contracts would therefore not close this issue.
No executable replacement is proposed or adopted here. Any later change
to these bodies or to the verifier requires a separate implementation-change
proposal, strict independent review and the applicable authorization.

The aggregate and supplemental candidate clients compile. Native Rust 1.96
also compiles and executes the exact source copies; retained results are in
[`native-singleton-20260922-111038/logs/singleton/native/`](../native-singleton-20260922-111038/logs/singleton/native/).
The independently replayed shared completeness check and the new
four-state mutable completeness check do not use these array bodies.
Direct mutable extraction remains separately blocked by
[S-MUT-RETURN](S-MUT-RETURN.md#singleton-borrows-with-caller-owned-state);
its proved value-state adaptation still requires independent review.
None of these results is a source bridge. Both APIs remain incomplete;
their current rows and proof paths are in
[`coverage.tsv`](../inventory/coverage.tsv).
