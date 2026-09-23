# Original ASCII method calls do not bind to local source proofs

This is a source-proof limitation on unmodified Verus
`0.2026.09.20.aef82ed` and its matching vstd, hosted by Rust 1.98.1.
The semantic source remains Rust 1.96. No Rust implementation or
documentation defect is alleged. Independent review confirmed the limitation
and approved the six source-copy call rebindings below. They are now adopted,
and the affected source proofs compile and verify without new assumptions.
Independent replay of the repaired proofs remains pending. The original
external-method limitation is unchanged. No external issue has been filed.

## Shared split-off dependency: a separately reviewed call rebinding

The same missing-external-binding limitation also affects
`<[T]>::split_off_last`. This separate **implementation-change**
request is not an extension of the six ASCII permissions. No change to the
canonical Rust source, verifier, vstd or checker is requested.

Rust 1.96 `slice/mod.rs:4993-5015,5043-5065` documents removing a shared
endpoint, returning `None` on empty input. Both signatures are
`pub const fn split_off_{first,last}<'a>(self: &mut &'a Self) -> Option<&'a T>`.
Runtime calls are stable since 1.87.0; public const calls still require
`const_split_off_first_last`. The bodies first destructure the shared split,
return immediately on `None`, assign the remainder to `*self`, and then
return the endpoint. Only the reference slot changes; no element is moved,
written or dropped.

The selected whole-vstd search has no binding for either split-off method.
It does have `split_first` at `std_specs/slice.rs:547-552`, but no
`split_last`. The two new public split-off declarations are isolated in
[`specs/slice/split_off.rs`](../specs/slice/split_off.rs); neither source proof
imports them. Both use the same pure predicates in
[`split_off_post.rs`](../specs/slice/split_off_post.rs), with initial `Seq<T>`
and complete `(Option<T>, Seq<T>)` observations.

The unchanged receiver-lifted first body compiles with
`--crate-type lib --compile --no-cheating --num-threads 1`:
[`return-state/split_off_first/`](../logs/split-off-endpoints/return-state/split_off_first/).
Its count is one source target, no imported project proof functions.
The corresponding last attempt is rejected before verification:

```text
error: `core::slice::impl&%0::split_last` is not supported
  --> proofs/correctness/slice/split_off_last.rs:21:29
21 |     let Some((last, rem)) = slice.split_last() else { return None };
```

The exact source snapshot, command, exit code and full diagnostic are in
[`return-state/split_off_last/`](../logs/split-off-endpoints/return-state/split_off_last/).
The earlier ambiguous post-state annotation failures remain in
[`original/`](../logs/split-off-endpoints/original/).
They were resolved by the selected Verus spelling `(*final(slice))@`;
that spelling observes the outer reference slot when its call borrow ends.
There is no returned mutable borrow and no caller-final environment input.
The new aggregate compiles with two existing consistency lemmas, not two
split-off source proofs:
[`aggregate-return-state/`](../logs/split-off-endpoints/aggregate-return-state/).

The requested executable change in the formal last source is exactly:

```diff
 #[path = "../../../specs/slice/split_off_post.rs"]
 mod contracts;
+#[path = "split_last.rs"]
+mod split_dependency;
@@
-    let Some((last, rem)) = slice.split_last() else { return None };
+    let Some((last, rem)) = split_dependency::split_last(*slice) else { return None };
     *slice = rem;
     Some(last)
```

Before independent permission, exploration was confined to
[`proofs/correctness/slice/proposals/split_off_last.rs`](../proofs/correctness/slice/proposals/split_off_last.rs).
Its two relative imports account for the extra proposal directory. The
pre-adoption formal last source retained the original method call. The first
source requires no rebinding, and no first-source change is requested.

The proposed call copies the same inner shared `&'a [T]` from the slot
and passes it to the previously proved local shared `split_last`, whose
unconstrained, const signature ties both outputs to that input. The local
dependency remains unchanged and relies on its separately reviewed
split/index correspondence in
[V-SLICE-PATTERN](V-SLICE-PATTERN.md#independent-split-permission-before-adoption).
The `let-else`, early return, assignment and returned binding remain in
their original order. No assumption for either target method or for
external `split_last` is introduced. Equal sequences alone do not prove
reference provenance; source correspondence, the actual Rust 1.96 MIR,
lifetime probes and independent review remain necessary.

The proposal originally awaited independent permission; its passing compile
was not itself permission to adopt it. The separate permission below now
allows the exact change. All previous failures and other permissions in this
issue retain their scope.

### Independent split-off permission before adoption

Independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/ef0fcbf89597/round-0001.json`
permits only the `split_off_last` import and delegated-call difference
shown above. It does not permit changing `split_off_first`, either pure
candidate, the public signatures, branch/assignment/return order, canonical
Rust, vstd, Verus or specdet. No further external approval is needed for
this exact source-copy change.

Reviewer directly checked the Rust 1.96 docs, attributes and original
bodies, the existing shared `split_last`, and the original/proposed MIR.
Both last bodies copy the same inner shared slice, inspect the delegated
Option, write `rem` only in the `Some` branch, and return the same element
binding. The local dependency preserves the complete prefix and endpoint
origin; its nonempty branch establishes the bounds for subtraction, indexing
and `split_at`. It does not move, write or destroy `T`. Permission is based
on this source correspondence, not merely on successful verification.

In the restricted read-only environment, Reviewer independently compiled
the original first target, isolated last proposal, six state lemmas, state
regressions, seven public clients and aggregate. Both direct declarations
were analyzed and each analyzed directory reexecuted, with one selected
comparison, original UNSAT and all eleven guards off per run. Both generated
comparisons compiled separately. Native execution passed 20 tests and
128 diagnostic-matched rejections; the affected Python checks also passed.
Reviewer found no candidate clause requiring removal under the temporary
redundancy criterion. These unchanged inputs and results may be reused.

The formal last source still failed at the external call during that
review. Adoption must therefore be followed by its current-source compile,
an updated native route reading formal files rather than the isolated
proposal, selective export and real CLI rejection/preservation tests.
Final independent review of those changes remains required. The complete
pre-adoption files are preserved in
[`logs/split-off-endpoints/adoption-before/`](../logs/split-off-endpoints/adoption-before/).

### The isolated last proof and complete direct observations

The isolated last proposal now compiles with
`--crate-type lib --compile --no-cheating --num-threads 1`:
[`split-off-endpoints-proposal/correctness/split_off_last/`](../logs/split-off-endpoints-proposal/correctness/split_off_last/).
Its four verified functions are one split-off target, the unchanged local
shared `split_last`, and that dependency's two existing consistency lemmas.
The retained query transcripts distinguish all four. The contract-free
original call also reproduces the missing binding:
[`method-binding/`](../logs/split-off-endpoints/method-binding/).
Neither run changes the original formal last source.

The actual checker supports this receiver shape without an adapter. Both
direct declarations at line 15 were discovered and analyzed, then each
analyzed directory was executed by `replay --run ... --reexecute` without
a configuration override. Each of the four executions selected one target,
proved one goal and returned original-query UNSAT. Their full comparisons
use independent `post1_slice` and `post2_slice` observations:

```rust
(((r1 is Some) == (r2 is Some))
    && ((r1 is Some) ==> (r1->Some_0 == r2->Some_0)))
    && (post1_slice =~= post2_slice)
```

All eleven actual `check-sat-assuming` guards are off. Both generated files
also compile separately, with one comparison each. Inputs, pure predicates,
the configured view source and configuration match the frozen analyzed and
reexecuted workspaces. Reports, comparisons and unrestricted queries remain in
[`direct/`](../logs/split-off-endpoints/direct/); the independent generated
compilations are in
[`compiled-comparisons/`](../logs/split-off-endpoints/compiled-comparisons/).
This checks completeness, not the unsupported formal last source.

[`split_off_state.rs`](../proofs/completeness/slice/split_off_state.rs)
compiles with six proof lemmas and `--no-cheating`. It proves the reference
candidate correspondence, totality from only the initial `Seq<T>`, ordered
reconstruction, and complete comparison equivalence. The empty witness
does not construct a `T`. Five additional state regressions compile with
those six lemmas, eleven functions in total. The separate public-binding
clients compile with seven functions, including consecutive and alternating
consumption, retained earlier references, local-slot destruction and arbitrary
subsequent slot reassignment. These are not additional source targets.
Their records are in
[`value-state/`](../logs/split-off-endpoints/value-state/) and
[`contract-clients/`](../logs/split-off-endpoints/contract-clients/).

Under the temporary redundancy criterion, full remaining-sequence equality
already implies remaining length and each ordered position; no duplicate
length or pointwise clauses are present. The Option branch, endpoint value
and full remaining content are distinct observations. The nonempty guard
is not supplied by the recommended domain of a spec `subrange`. The empty
branch must still constrain the slot, not just the returned Option.

### Actual native comparison of the pending call change

The `split-off-endpoints-proposal` group reads both actual formal sources
and only the isolated last proposal, including the unchanged local
`split_last` dependency. It compares those with the authoritative bodies
and real public APIs. Through the unchanged `run_review_command` /
`get_review_command` path, Rust 1.96 metadata and MIR compilation, actual
linking, 20 runtime tests and 128 diagnostic-checked compiler rejections
passed. The read-only command completed with exit zero and its container
was removed:
[`native-readonly-mir-spelling/result.json`](../logs/split-off-endpoints-proposal/native-readonly-mir-spelling/result.json).
The retained source, MIR, exact commands, native results and negative inputs
are in [`native/`](../logs/split-off-endpoints-proposal/native/).
This was engineering execution, not independent review or adoption.

The actual generic MIR for the original and proposed last methods differs
only in the delegated callee. Both copy `(*_1)` into the same temporary
shared slice, branch on the returned Option, assign the remainder to
`(*_1)` only on `Some`, and return the same endpoint binding. See
[`split_off_endpoints.mir:112-156,607-651`](../logs/split-off-endpoints-proposal/native/split_off_endpoints.mir).
The native sequence/frame tests include empty and singleton inputs, ordered
and repeated values, non-Copy/non-static values, ZST extents, empty
uninhabited slices, repeated and alternating consumption, and retained
earlier results across later calls or arbitrary slot reassignment.

The exact higher-ranked shared signature compiles. Both owner-lifetime
escapes and mutable-return attempts are rejected, while references
outliving the short slot borrow compile and run. The two
`public-*-const-without-feature` probes reject actual public const calls;
const source-copy compilation is not substituted for that check.

The initial native run had compiled metadata/MIR but stopped before the
runtime suite because its MIR-name check expected a fully qualified local
dependency. Rust 1.96 prints that unique function as `fn split_last`,
although the source has the checked module path. The check and its mock
were corrected to the actual pinned compiler spelling, without changing
any Rust body. The initial failure is preserved in
[`native-readonly-engineering/`](../logs/split-off-endpoints-proposal/native-readonly-engineering/).
Current native-runner and binding tests pass 35 methods in
[`python-native-bindings/`](../logs/split-off-endpoints/python-native-bindings/).
The older mutable-split preservation assertions were updated only for the
new aggregate module suffix; their eleven methods also passed. Earlier
Python invocation/comment-matching failures remain under
[`python-bindings/`](../logs/split-off-endpoints/python-bindings/).

### Adopted split-off source and selective export

After recording the separate permission, the formal
[`split_off_last.rs`](../proofs/correctness/slice/split_off_last.rs)
was changed only by the module import and delegated-call replacement.
The original first source, both pure predicates and declarations, shared
dependency, state lemmas, checker inputs and configuration remain identical
to the preserved pre-adoption files. No old source failure was overwritten.

The changed formal last file now compiles with
`--crate-type lib --compile --no-cheating --num-threads 1`, verifying
one target, one shared `split_last` dependency and two existing consistency
lemmas. Exact command, inputs, compiled library and queries are in
[`correctness/split_off_last/`](../logs/split-off-endpoints/correctness/split_off_last/).
The independently checked first source and unchanged state/analyze/reexecute
results are reused by content, not rerun or promoted from an environment
probe. Their inputs remain the same as those used in the prior independent
review.

The active native route is now
`scripts/check_native.py --group split-off-endpoints --output-root DIR`.
It extracts only the actual formal sources and actual shared dependency,
not the isolated proposal. The proposal execution route was removed;
the proposal file, original tests and all earlier results remain in their
historical locations or the pre-adoption directory. A new restricted
read-only invocation compiled Rust 1.96 metadata/MIR, linked and passed
20 runtime tests and 110 exact compiler rejections, including both real
public const calls without the feature. The reduction from 128 rejections
and six generic functions to 110 and five removes only the redundant
isolated-last implementation. All twenty behavior cases and rejection
categories remain. The command completed with container removal:
[`current-native-readonly/result.json`](../logs/split-off-endpoints/current-native-readonly/result.json);
its retained native files are in
[`current-native/`](../logs/split-off-endpoints/current-native/).

`scripts/export_completeness.py --split-off-endpoints [split_off_first split_off_last]`
now checks each selected current-source compilation, exact permitted source
text, the reviewed state and declaration files, both actual checker runs,
the complete generated comparison and all eleven original-query guards
before writing anything. Failed, UNKNOWN, zero-goal, stale, wrong-selection
or missing-remainder observations cannot become successful exports.
All selected methods are validated before any proof or coverage file is
written, so failure of the second method does not partially export the first.

The two actual exported files are
[`split_off_first.rs`](../proofs/completeness/slice/split_off_first.rs) and
[`split_off_last.rs`](../proofs/completeness/slice/split_off_last.rs).
Only three provenance comments and the relative pure-predicate import
differ from the real generated comparisons. Each final file was compiled
with ordinary `--compile --num-threads 1`, verifying one comparison:
[`exported-comparisons/`](../logs/split-off-endpoints/exported-comparisons/).
These functions are not implementation targets.

Five affected Python files compile. The current native-runner, binding and
real export CLI tests pass 47 methods, including 137 actual CLI invocations
for independent/joint/repeated selection, invalid selection and content or
proof failures. Commands and outputs are in
[`adopted-python-native/`](../logs/split-off-endpoints/adopted-python-native/) and
[`export-tests/`](../logs/split-off-endpoints/export-tests/).
The actual project export updated only the two intended rows; 329 unselected
raw records, the table header/order and all 21 previous top-level
completeness/state files remained byte-identical:
[`export/preservation.json`](../logs/split-off-endpoints/export/preservation.json).
Final independent review of the adopted source and integration remains
required; the whole slice module is still incomplete.

## The actual dependency chain

All source paths below are relative to
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src`.

| Operation | Source body | Original delegated call |
|---|---|---|
| Slice uppercase mutation | `slice/ascii.rs:173-181` | `byte.make_ascii_uppercase()` |
| Slice lowercase mutation | `slice/ascii.rs:195-203` | `byte.make_ascii_lowercase()` |
| Scalar uppercase mutation | `num/mod.rs:716-718` | `self.to_ascii_uppercase()` |
| Scalar lowercase mutation | `num/mod.rs:742-744` | `self.to_ascii_lowercase()` |
| Scalar uppercase conversion | `num/mod.rs:639-642` | `self.is_ascii_lowercase()` |
| Scalar lowercase conversion | `num/mod.rs:664-667` | `self.is_ascii_uppercase()` |
| Uppercase classification | `num/mod.rs:812-814` | `matches!(*self, b'A'..=b'Z')` |
| Lowercase classification | `num/mod.rs:846-848` | `matches!(*self, b'a'..=b'z')` |

The slice documentation at `slice/ascii.rs:161-169,183-191` and the scalar
docstrings immediately preceding these bodies agree: only the corresponding
ASCII letter interval changes. `ASCII_CASE_MASK` is `0b0010_0000` at
`num/mod.rs:539`. Uppercase conversion uses XOR; lowercase conversion uses OR.
Neither branch can be replaced by a different arithmetic implementation
without the required source correspondence.

The two exact classification bodies, with only `self` lifted to a free
function parameter, compile with `--no-cheating` and verify **two dependency
functions, no lemmas**:
[`u8_ascii_classify.rs`](../proofs/correctness/num/u8_ascii_classify.rs),
[`command and output`](../logs/ascii-case/correctness/classify/).
These functions do not register a contract for the distinct external
`core::num::<impl u8>` methods.

Before rebinding, the four scalar bodies in
[`u8_ascii.rs`](../proofs/correctness/num/u8_ascii.rs) retained their original
method-call expressions. Their original compile run rejected all four external
calls before verification. Its first diagnostic was:

```text
error: `core::num::impl&%6::is_ascii_lowercase` is not supported
  --> proofs/correctness/num/u8_ascii.rs:16:15
16 |     *byte ^ ((byte.is_ascii_lowercase() as u8) * ASCII_CASE_MASK)
```

The compiler suggests `assume_specification`, but that suggestion is not a
source proof. The selected verifier explicitly rejects new
`external_body` / `assume_specification` declarations under `--no-cheating`;
see `toolchain/upstream/source/vir/src/well_formed.rs:1566-1578`.
No declaration or external import has been used to bypass this restriction.
That original attempt therefore verified **zero scalar conversion/mutation
functions**. Its complete command, return code and diagnostics remain in
[`correctness/scalar/`](../logs/ascii-case/correctness/scalar/).

The original slice attempts retained the loop, indexed reborrow, scalar method
call, increment and const signature. Each was separately rejected
at its `byte.make_ascii_*case()` call, before any target obligation:
[`uppercase`](../logs/ascii-case/correctness/make_ascii_uppercase/) and
[`lowercase`](../logs/ascii-case/correctness/make_ascii_lowercase/).
Each original source count was **zero**; neither imported an assumed scalar
contract. These failed runs have not been overwritten.

## Contract-free reproduction and the borrowing boundary

[`u8_ascii_method_binding.rs`](repros/u8_ascii_method_binding.rs) calls each
of the six scalar methods without any precondition, postcondition or imported
project contract. The
[`retained run`](../logs/ascii-case/method-binding-repro/)
rejects all six external calls with the same diagnostic. This distinguishes
the missing bindings from a failure of the proposed sequence postconditions.

The separate
[`indexed assignment`](repros/ascii_mutable_index.rs) compiles and verifies
one function with `--no-cheating`, using the original
`let byte = &mut slice[i];` operation followed by scalar assignment. Its
postcondition is the full `old(slice)@.update(i, value)` relation, including
all other elements. The
[`actual output`](../logs/ascii-case/mutable-index/) establishes this operation
on the selected upstream indexing basis, not the casing loop or Rust 1.96
indexing/length implementations. The missing scalar bindings remain the
observed source-proof obstruction.

## Reviewed source-copy call rebinding

This **implementation-change** issue was raised before any executable edit.
Independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/d52fae2975c8/round-0001.json`
approved only these substitutions and their module imports in the source-derived
proof copies. Canonical Rust, the public API declarations, Verus, vstd and
specdet remain unchanged:

```diff
--- proofs/correctness/num/u8_ascii.rs
+++ proposed source-copy calls
-    *byte ^ ((byte.is_ascii_lowercase() as u8) * ASCII_CASE_MASK)
+    *byte ^ ((classify::is_ascii_lowercase(byte) as u8) * ASCII_CASE_MASK)
-    *byte | (byte.is_ascii_uppercase() as u8 * ASCII_CASE_MASK)
+    *byte | (classify::is_ascii_uppercase(byte) as u8 * ASCII_CASE_MASK)
-    *byte = byte.to_ascii_uppercase();
+    *byte = to_ascii_uppercase(byte);
-    *byte = byte.to_ascii_lowercase();
+    *byte = to_ascii_lowercase(byte);
--- proofs/correctness/slice/make_ascii_uppercase.rs
+++ proposed source-copy call
-        byte.make_ascii_uppercase();
+        u8_ascii::make_ascii_uppercase(byte);
--- proofs/correctness/slice/make_ascii_lowercase.rs
+++ proposed source-copy call
-        byte.make_ascii_lowercase();
+        u8_ascii::make_ascii_lowercase(byte);
```

The local module imports select the retained Rust 1.96 source copies.
Review confirmed that every receiver is concrete `u8` and every original
call resolves to the corresponding inherent method. The lifted functions
preserve constness, parameter and return types. Classification and conversion
perform the same shared reads; scalar assignment occurs after its right-hand
side is evaluated. The slice call receives the same indexed exclusive
reborrow, returns unit, and returns no borrow. XOR, OR, the mask, assignment,
indexing, loop and increment remain unchanged. No additional input restriction
or assumed dependency contract is authorized.

### Actual proof results after rebinding

The first rebound scalar compile reached the two conversion postconditions
and failed there, rather than at an external method. That output is retained
in [`scalar-initial/`](../logs/ascii-case/rebinding/scalar-initial/).
Four ghost `bit_vector` assertions now establish XOR-with-32 as subtraction
on lowercase ASCII, OR-with-32 as addition on uppercase ASCII, and the two
zero-mask identities. They leave the executable expressions unchanged.
No new lemma precondition, API requirement, assumed contract or trusted
function was introduced.

The actual `--compile --no-cheating --num-threads 1` results are:

| Source input | Exit code | Verified obligations | Source functions covered |
|---|---:|---:|---|
| `proofs/correctness/num/u8_ascii.rs` | 0 | 11 | Six scalar bodies: two classifiers, two conversions and two mutations |
| `proofs/correctness/slice/make_ascii_uppercase.rs` | 0 | 13 | One slice body and the six scalar bodies |
| `proofs/correctness/slice/make_ascii_lowercase.rs` | 0 | 13 | One slice body and the six scalar bodies |

The scalar total includes one constant and four bit-vector assertions. Each
slice total also includes its loop obligation; it is not a count of 13 API
functions. Commands, compiled libraries, query inputs, outputs and unchanged
source snapshots are retained in
[`correctness/scalar/`](../logs/ascii-case/rebinding/correctness/scalar/),
[`uppercase-initial/`](../logs/ascii-case/rebinding/uppercase-initial/) and
[`lowercase-initial/`](../logs/ascii-case/rebinding/lowercase-initial/).
The existing prefix-converted/suffix-unchanged loop invariants suffice without
alteration. Length and indexing still use the selected upstream models, not
new proofs of Rust 1.96 metadata.

[`test_ascii_contracts.py`](../tests/test_ascii_contracts.py) compares all
eight bodies with the authoritative source after exactly the six reviewed
substitutions and receiver lifting, removing only ghost annotations. It
also checks the const signatures, concrete types, original mask and required
module imports. The five source/specification tests and five real export CLI
tests passed in [`python-tests/`](../logs/ascii-case/rebinding/python-tests/).

The public contracts, state correspondence, analysis inputs and checker
configuration are unchanged. The independent review cited above analyzed both
targets at line 9, obtaining one verified full-sequence comparison and original
query UNSAT per API with all 55 search guards disabled. Its command outputs are
in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/reviewer-checks/d232fd622cd944c0b04c5efb18703a3b/b7d332f888b54f34ae237c034f5059b1/scratch/`.
The retained original analyses and reexecutions remain applicable; they were
not rerun merely because executable proof-copy calls changed.

The ASCII exporter now requires successful source compilation and all 13
obligations, and compares each source input and dependency with the successful
run's saved bytes. It records one target source function rather than the old
zero. Failed, empty, incomplete or stale source results are rejected.
[`export/isolation.json`](../logs/ascii-case/rebinding/export/isolation.json)
records that only the two ASCII coverage rows changed; all 329 other rows and
all 14 completeness proof/state files are byte-identical. The prior two
coverage rows are retained beside that file. Independent review of these
repaired source proofs and writeback changes is still required.
