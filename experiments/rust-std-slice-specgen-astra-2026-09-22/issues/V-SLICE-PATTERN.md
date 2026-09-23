# The selected verifier rejects the original slice patterns

Independent review has now authorized exactly the two `first`/`last`
source-proof conversions recorded below. The original slice-pattern
limitation remains; this permission neither changes Rust nor covers the two
split methods. Adoption and current-source validation have now completed in
new runs, not by inheriting the isolated results, as recorded in
[the adopted results](#adopted-current-source-results); final independent
review remains pending.

The separate [split conversion proposal](#proposed-conversion-of-split_first-and-split_last)
now has its own [independent permission](#independent-split-permission-before-adoption)
for exactly the two documented bodies. This permission is recorded before
adoption; [new current-source results](#adopted-split-source-results) now cover
the adopted files and their integration. Final independent review is still
required. The permission is not an extension of endpoint or ASCII permission.

## Proposed mutable split conversions

This `implementation-change` proposal was raised before creating either
isolated replacement for `split_first_mut` or `split_last_mut`. The separate
[independent permission](#independent-mutable-split-permission-before-adoption)
now covers exactly the two current proposal bodies and their existing
borrow-length proof blocks. The shared split and mutable endpoint permissions
below are not the authority for this change. Canonical Rust, Verus, vstd,
specdet and Argus remain unchanged; external filing is not authorized.

The authority is
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice/mod.rs`.
The documentation and body at 202-222 specify the first element and the
entire remainder, and demonstrate independent writes producing `[3, 4, 5]`.
Those at 244-264 specify `(last, init)` and demonstrate `[4, 5, 3]`.
Both return `None` exactly for an empty slice. The methods belong to the
unconstrained `impl<T> [T]` at 101, have a single mutable receiver and result
`Option<(&mut T, &mut [T])>`, and are const-stable since 1.83.0. The lifted
proof functions retain `pub const fn`, unrestricted `T`, and both output
lifetimes bound to the input. Only the following executable changes are
proposed:

```diff
--- proofs/correctness/slice/split_first_mut.rs
+++ proofs/correctness/slice/proposals/split_first_mut.rs
@@
-    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }
+    if slice.len() == 0 {
+        None
+    } else {
+        let (head, tail) = slice.split_at_mut(1);
+        Some((&mut head[0], tail))
+    }
--- proofs/correctness/slice/split_last_mut.rs
+++ proofs/correctness/slice/proposals/split_last_mut.rs
@@
-    if let [init @ .., last] = slice { Some((last, init)) } else { None }
+    if slice.len() == 0 {
+        None
+    } else {
+        let i = slice.len() - 1;
+        let (init, last) = slice.split_at_mut(i);
+        Some((&mut last[0], init))
+    }
```

Ordinary ghost assertions or calls to existing proved/borrow-length lemmas
may accompany these bodies, but may not change their executable operations.
The proposed files are separate inputs, not adopted source proofs.

### Independent mutable split permission before adoption

The independent Reviewer decision in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/c0b2f8f17fdf/round-0002.json`
permits only the current executable code in
`proofs/correctness/slice/proposals/{split_first_mut,split_last_mut}.rs`,
including their respective ghost calls to the existing
`vstd::slice::mut_ref_slice_len_eq(&tail)` and `(&init)`. This permission is
recorded before either formal original is replaced. It is not API completion
and does not authorize any canonical Rust or tool/trusted-basis change.

Reviewer directly checked the authoritative methods and split delegates,
raw construction, pointer offsets and versioned pattern/borrow/lifetime
rules for all legal lengths. The decision separately covers disjoint
element ranges, one-element indexing, safe subtraction before the mutable
split, both returned lifetimes, singleton empty remainders, const behavior
and zero-sized provenance. It does not infer those facts from value or
address equality. The unchanged pure candidates, exact first-contract
correspondence and isolated missing last binding were also checked.

Through the restricted read-only command path, Reviewer independently
compiled both isolated sources, the seven state lemmas, both adapters,
state regressions, aggregate and public-binding clients; ran discovery
and both selected analyze/reexecute pairs; and executed the 19 native
tests with 216 exact compiler rejections. All four main checker results
retain the full comparison and disable all 19 guards. The selected 31
Python tests passed; a review-script count assertion incorrectly expected
39 and is explicitly not a project defect. Eight separately compiled
`u8` witnesses do not change the supplementary searches' UNKNOWN outcomes.
No repetition of those searches is required.

Reviewer found no candidate clause to remove under the temporary redundancy
criterion: complete initial content and final writeback remain independent,
and the remainder's cross-state length relation remains necessary.
The adopted formal files and actual current-source native results must now
be compiled again. Selective export and its real rejection tests, followed
by final independent review, remain required. Original proof inputs,
isolated proposals, candidates and previous records have been preserved in
[`logs/mutable-splits/adoption-before/`](../logs/mutable-splits/adoption-before/)
before this adoption.

### Mutable split source correspondence submitted for review

Let `n` be the element count of any legal `&'a mut [T]`. The versioned Rust
1.96 [binding rules at 252-274](../.argus/sources/74d2d8be6f6312a91e3caccc.txt)
give both identifiers `ref mut` binding mode. Its
[slice patterns at 742-774](../.argus/sources/74d2d8be6f6312a91e3caccc.txt)
and [MIR projections at 1225-1267](../.argus/sources/d30066527f26d75ae5d1fd58.txt)
identify the first pattern's element zero and range `[1,n)`, and the last
pattern's element `n-1` and range `[0,n-1)`. Each pattern matches precisely
when `n >= 1`. The complementary unsigned test `n == 0` therefore preserves
both complete branch domains, including empty uninhabited-element slices.

The authoritative `split_at_mut` documentation and body at 1959-1991 give
ordered ranges `[0,mid)` and `[mid,n)`, panicking only when `mid > n`.
Its const-stable body delegates to `split_at_mut_checked` at 2192-2200,
which checks `mid <= n`, and then to `split_at_mut_unchecked` at 2092-2112.
The latter derives `ptr` from the same slice with `as_mut_ptr`, then returns
`from_raw_parts_mut(ptr, mid)` and
`from_raw_parts_mut(ptr.add(mid), unchecked_sub(n, mid))`. The relevant
pointer origin is in `slice/mod.rs:730-759`; element-unit pointer offsets
and their extent requirements are in `core/src/ptr/docs/add.md:1-24`.
The validity and exclusive-lifetime requirements and construction are in
`slice/raw.rs:143-195`. All three split methods and the mutable raw
constructor are const-callable on the required Rust 1.96 baseline.

For the first proposal, the nonempty branch permits `mid = 1`. The left
slice has exactly one element and the right slice is exactly `[1,n)`.
Index zero of the left slice is the same original element zero. For the
last proposal, `i = n-1` is computed before either returned mutable borrow;
subtraction cannot underflow and `0 <= i < n`. The left slice is `[0,n-1)`
and the right slice has one element at original position `n-1`; indexing
its zero position is valid. The return order is still `(last, init)`.
Neither branch reaches a bounds panic, underflow or invalid pointer offset.

These pairs partition the original element extent into disjoint ranges.
The inner one-element reborrow is wholly within its split region and is
disjoint from the other returned slice. It introduces no overlapping
escaping mutable reference. The versioned
[borrow rules at 63-73](../.argus/sources/df6d9bcc218b2f61bf5e45cc.txt) and
[lifetime rules at 29-35](../.argus/sources/3710179701fb89b97071de07.txt)
retain both output lifetimes within the input borrow and suspend conflicting
access through the original reference. At borrow end, both regions return
their own independently chosen final contents to that same input extent.
This concerns borrow resolution, not a requirement that a destructor run.

At length one, the first empty remainder starts at the original one-past
position; the last empty remainder starts at the original start. The same
ordered element extents apply to zero-sized types, even when addresses
coincide, and to legal lengths up to `usize::MAX` for such types. Neither
value equality nor a zero-sized address comparison proves this provenance.
The transformation does not move, copy, compare, clone, allocate or drop an
element. It introduces no trait bound, inhabitation requirement, callback
or extra element destructor. Both returned references may remain live
together and receive separate, repeated and interleaved legal writes.
For a receiver that is a subslice, all operations stay within that subslice;
its surrounding elements are not accessed or replaced.

### Mutable split contract and trusted dependencies

The selected existing `View for [T]` is `Seq<T>`
(`toolchain/upstream/source/vstd/slice.rs:13-17`). Its length, mutable-index
writeback and borrow-length contracts remain upstream dependencies, not new
proofs of Rust metadata or indexing. The selected `split_at_mut` contract
at `std_specs/slice.rs:526-535` states both initial subranges and
`final(slice)@ == final(ret.0)@ + final(ret.1)@`.

The selected vstd already registers `split_first_mut` at
`std_specs/slice.rs:554-564`. It includes the initial element, full initial
tail, equal initial/final tail lengths and final reconstruction in
element-then-tail order. Do not register that method again. The current
whole-vstd search finds no `split_last_mut` declaration; only that missing
public binding may be added, separately from the source-proof imports.

The pure candidates relate initial `Seq<T>` and caller-final
`Option<(T, Seq<T>)>` to initial `Option<(T, Seq<T>)>` and the entire final
input sequence. `None` must correspond exactly to empty input and require
no value of `T`. A nonempty caller choice permits any final element and
any final remainder with the original remainder's length. Its shape/length
domain must follow from the candidate, the initial subrange and the existing
`mut_ref_slice_len_eq` borrowing fact at `vstd/slice.rs:218-221`.
The final owner must not be an input. Reconstruction is
`seq![written_element] + written_remainder` for the first method and
`written_remainder + seq![written_element]` for the last.

The whole initial remainder is independent of both the initial element and
the final owner. The cross-state remainder-length relation is necessary
when adapting references to freely supplied sequences; equality to the
initial subrange alone does not constrain that final sequence. In contrast,
separate same-state remainder-length or final-owner-length clauses follow
from the full sequence relations and should not be duplicated. The existing
[temporary redundancy criterion](../review-criteria-temporary.txt) remains
applicable to this proposal and subsequent independent reviews.

Both original failures, isolated proof results, actual checker inputs
and comparisons, and native metadata/MIR and behavioral results are
retained separately. None supplies adoption permission. Final current-source
proofs, selective result export and independent review remain necessary
after an explicit permission for these two bodies.

### Retained isolated mutable split results

Before adoption, the formal files
`proofs/correctness/slice/{split_first_mut,split_last_mut}.rs` contained
their exact original patterns. Actual Verus invocations with
`--crate-type lib --compile --no-cheating --num-threads 1` reject each
pattern before checking any source function. Inputs, commands and diagnostics
are retained in
[`logs/mutable-splits-proposal/correctness/initial/original/`](../logs/mutable-splits-proposal/correctness/initial/original/).
This reproduces the selected verifier limitation for these two actual APIs,
not merely the earlier endpoints.

The isolated executable bodies are exactly the proposed differences above.
After `split_at_mut`, each now has one ghost block invoking the existing
`vstd::slice::mut_ref_slice_len_eq(&tail)` or `(&init)` before returning
that reference. This supplies the remainder's cross-state length relation
without freezing its contents or introducing an axiom. Both isolated files
compile with `--no-cheating`, each checking **one source function, no imported
proof functions and zero errors**:
[`correctness/borrow-length/`](../logs/mutable-splits-proposal/correctness/borrow-length/).
The earlier failed proposal runs without that ghost fact remain in
`correctness/initial/proposal/`. Their candidate and executable operations
are identical to the successful inputs; no observation was removed.

The pure candidates are in
[`specs/slice/mutable_splits_post.rs`](../specs/slice/mutable_splits_post.rs).
Only [`mutable_splits.rs`](../specs/slice/mutable_splits.rs) declares the
missing public `split_last_mut` binding; no `split_first_mut` declaration
is added. Source proofs import only the pure file. The aggregate appends
that single binding module without changing its earlier modules and compiled
with `--compile --num-threads 1`, checking its two pre-existing consistency
lemmas. This is not another source proof.

The proved state relation and direct checker limitation are detailed in
[S-MUT-RETURN](S-MUT-RETURN.md#two-simultaneously-live-mutable-regions).
The state file checks seven lemmas with `--compile --no-cheating`;
each analysis adapter adds one function. The actual analyze and reexecute
runs each prove one generated comparison for the selected API, with original
query UNSAT and all 19 search guards disabled. Both generated source files
were also compiled with ordinary `--compile`, each checking **nine functions**:
one comparison, one adapter and seven imported state lemmas.
[`compiled-comparisons/comparison-checks.json`](../logs/mutable-splits-proposal/compiled-comparisons/comparison-checks.json)
records current input/dependency equality, full comparison and guard checks
for all four checker executions. These results do not authorize adoption.

The pre-adoption native group was `mutable-splits-proposal`. Its retained
[`native-borrow-length/`](../logs/mutable-splits-proposal/native-borrow-length/logs/mutable-splits-proposal/native/)
run compiled Rust 1.96 metadata and runtime/const MIR, linked and executed
**19 tests**, and required **216 exact compiler rejection diagnostics**.
It compares the original patterns, isolated proposals and public methods,
not an adopted substitute. The extractor requires the exact pure predicates,
signatures, original/proposed bodies and length-proof blocks, and erases
only those exact ghost calls for native compilation. Earlier native runs and
the test failure caused by the newly added annotation remain separate.

The generic MIR records original nonempty tests and the projections
`[0 of 1]` with `[1:]`, and `[:-1]` with `[-1 of 1]`. The first proposal
calls `split_at_mut(1)` and indexes the left one-element slice. The last
computes `SubWithOverflow(n, 1)` before `split_at_mut`, indexes the right
one-element slice, then returns it before the left remainder. These actual
forms support, but do not replace, the arbitrary-length/source argument.
The tests keep both borrows live for independent and interleaved writes,
observe the complete input and outer subslice frame, and include const,
non-Copy, non-static, zero-sized, maximum-length unit and empty uninhabited
cases. Invalid arguments, both lifetimes, conflicting receiver accesses
and illegal aliases are checked by compiler rejection, never by executing UB.

[`tests/mutable_split_state.rs`](../tests/mutable_split_state.rs) compiles
with `--no-cheating`: ten new regression lemmas and seven imported state
lemmas pass. Its empty witness has no element parameter. The two public
binding clients in
[`mutable_split_contract_clients.rs`](../tests/mutable_split_contract_clients.rs)
also compile and verify interleaved replacements of unrestricted `T`; these
are explicitly clients, not source proofs. Current extraction/binding tests
passed 39 tests in
[`python-current/unittest.log`](../logs/mutable-splits-proposal/python-current/unittest.log).
The earlier native group's 73-test Python run is retained, not presented as
a new run of the annotated inputs.

These pre-adoption runs did not permit a source replacement or export.
The subsequent separate permission and current-source work are recorded
above and below; the original inputs and all these results remain intact.

### Adopted mutable split source results

After the separate permission above was recorded, both current source files
received only their permitted executable body and existing borrow-length
proof block. Their signatures, comments, imports and ensures clauses are
otherwise byte-identical to
[`adoption-before/`](../logs/mutable-splits/adoption-before/).
The pure candidates, missing-method binding, state lemmas, checker inputs,
aggregate, isolated proposals and direct-extraction failures are unchanged.
No canonical source, selected tool or trusted dependency was modified.

New actual Verus invocations in
[`logs/mutable-splits/correctness/`](../logs/mutable-splits/correctness/)
compile each formal file with
`--crate-type lib --compile --no-cheating --num-threads 1`, checking
**one source target, zero imported proof functions and zero errors** each.
Their command records, exact inputs, libraries and source queries are
retained. These new results replace neither the original failures nor the
earlier isolated runs.

The current native route is now `--group mutable-splits`, reading only
`proofs/correctness/slice/{split_first_mut,split_last_mut}.rs`. It replaces
the proposal route; the old source copies and logs remain historical.
The current extractor rejects any difference from the permitted source and
the exact pure contract, erasing only the two known ghost blocks for Rust.
The behavior file was renamed to
[`mutable_split_behavior.rs`](../tests/mutable_split_behavior.rs) with only
its source identifier and implementation labels changed. The fresh run in
[`current-native/`](../logs/mutable-splits/current-native/logs/mutable-splits/native/)
compiled Rust 1.96 metadata and runtime/const MIR, linked, executed all
**19 tests**, and checked all **216 specified compiler rejections**.
The failed early multi-diagnostic alias probe remains in its original
`native-initial` directory; it is not a current failure or a reason to rerun
an unchanged probe.

The newly selected
`scripts/export_completeness.py --mutable-splits [split_first_mut split_last_mut]`
validates all selected current source evidence before changing either row.
It also validates the unchanged state/adapter and real checker evidence by
content, including both selected runs, their exact relative selectors,
reexecute linkage, full nested comparison and 19 disabled original-query
guards. The previously independently reviewed main analyses are reused, not
presented as fresh checker executions after adoption.

The actual selective command wrote only two rows in
[`inventory/coverage.tsv`](../inventory/coverage.tsv) and the two generated
[`split_first_mut.rs`](../proofs/completeness/slice/split_first_mut.rs) /
[`split_last_mut.rs`](../proofs/completeness/slice/split_last_mut.rs)
comparison files. Apart from three provenance comments and relocating the
state import, each file is exactly the checker-generated source.
New `--compile --num-threads 1` invocations of those exported files check
**nine functions each: one comparison, one adapter and seven imported
state lemmas**, with zero errors. They are in
[`export-compile/`](../logs/mutable-splits/export-compile/);
[`export-correspondence.json`](../logs/mutable-splits/export-correspondence.json)
records the source equality. They are not nine API source targets.

The new real CLI tests passed 16 test methods and 324 invocations, including
305 rejected invocations that leave every existing file unchanged:
[`export-tests/focused/unittest.log`](../logs/mutable-splits/export-tests/focused/unittest.log).
They cover separate, joint, reordered and repeated selection, default-route
preservation, invalid/duplicate selections, failed/UNKNOWN/zero-goal results,
stale dependencies, invalid source/binding, missing outputs, altered
comparison or caller writes, enabled guards and wrong reexecution linkage.
The preceding combined test run retained a test-log filename collision;
after that test-only correction, the new module passed. Its 39 unaffected
existing export test methods had already passed in the retained combined
run and were not repeated. Current native-extractor and binding tests pass
33 methods in
[`python-current/unittest.log`](../logs/mutable-splits/python-current/unittest.log);
Python imports compile the changed code in those real test runs.

Content comparison in
[`preservation.json`](../logs/mutable-splits/preservation.json)
confirms the 329 unselected raw records, header/order, and all 18 existing
top-level completeness files are unchanged. In total 111 saved inputs and
historical files match their pre-adoption copies. Only the two selected
source-result rows and two new top-level comparisons are added to the
existing results. Current-file final independent review is still required;
the temporary redundancy criterion and all original limitations remain.

## Proposed mutable endpoint conversions

The independent review recorded in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/02036b1aebf8/round-0002.json`
now permits exactly the two executable replacements below. This permission
is recorded before adoption. It applies only to the two source-proof bodies,
not canonical Rust, Verus, vstd, other APIs or public contract registrations.
The proposal history and original failures below remain unchanged.

This separate `implementation-change` proposal concerns only `first_mut` and
`last_mut`. It was raised before writing the isolated replacements. Neither
the shared endpoint permission nor the split permission authorizes mutable
borrowing. The separate mutable permission above is required before either
current source-proof body may be replaced. No change to canonical Rust, Verus, vstd,
the checker or the runtime is proposed; external filing remains unauthorized.

The authority is
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice/mod.rs`.
The documentation at 159-173 requires a mutable reference to the first element
or `None` on empty input, and demonstrates changing `[0, 1, 2]` to `[5, 1, 2]`.
The documentation at 285-299 requires the last element and demonstrates
`[0, 1, 10]`. The unchanged implementations at 178-180 and 304-306 are:

```rust
pub const fn first_mut(&mut self) -> Option<&mut T> {
    if let [first, ..] = self { Some(first) } else { None }
}

pub const fn last_mut(&mut self) -> Option<&mut T> {
    if let [.., last] = self { Some(last) } else { None }
}
```

Both methods are in the unconstrained `impl<T> [T]`, stable since 1.0.0 and
const-stable since 1.83.0. The lifted proof signatures remain
`pub const fn first_mut<T>(slice: &mut [T]) -> Option<&mut T>` and the
corresponding `last_mut` signature. Their elided return lifetime is the input
lifetime. Only these executable differences are proposed:

```diff
--- proofs/correctness/slice/first_mut.rs
+++ proofs/correctness/slice/first_mut.rs
@@
-    if let [first, ..] = slice { Some(first) } else { None }
+    if slice.len() == 0 { None } else { Some(&mut slice[0]) }
--- proofs/correctness/slice/last_mut.rs
+++ proofs/correctness/slice/last_mut.rs
@@
-    if let [.., last] = slice { Some(last) } else { None }
+    if slice.len() == 0 {
+        None
+    } else {
+        let i = slice.len() - 1;
+        Some(&mut slice[i])
+    }
```

### Mutable source correspondence submitted for review

Let `n` be the element count of an arbitrary legal `&'a mut [T]`.
All legal lengths and element types remain in scope.

| Obligation | Original and isolated proposed bodies |
|---|---|
| Complete branch domain | Each slice pattern has one element and a rest pattern, so it matches precisely when `n >= 1`. The proposed unsigned `n == 0` condition selects exactly the complementary branch. |
| Exclusive borrowed place | Match ergonomics on this mutable reference binds `first` or `last` by `ref mut`, at element position zero or `n - 1`. The proposal takes one mutable reborrow of that same place, not a different equal-valued element. |
| Index and subtraction | On the nonempty branch `1 <= n <= usize::MAX`; zero and `n - 1` are valid indices and subtraction cannot underflow. Neither expression is evaluated on empty input. `last_mut` computes `i` before beginning the exclusive element borrow. |
| Borrow duration and return | Both forms return `Option<&'a mut T>` from the same input, with no owned temporary or second escaping borrow. While the returned borrow is live, the caller cannot independently access the original slice through the suspended mutable reference. At the end of that reborrow, its final pointee value is the selected element's value in the returned slice. This is a borrow-end relation, not an assertion about running a destructor. |
| Complete returned input | The call changes no element. Subsequent legal caller writes through the returned reference may replace exactly the selected element. The final slice is the initial sequence updated at that position; every other element is unchanged. An empty slice returns `None` and remains empty, without requiring any value of `T`. |
| Effects and safety | Added operations read slice metadata, compare/subtract machine integers, and form a built-in indexed borrow. They introduce no callback, allocation, clone, copy, element comparison, move or additional element destructor. Their bounds failures are unreachable on legal inputs. |
| Type and position scope | `T` has no additional trait or lifetime bounds. Non-Copy and non-static elements are borrowed, not duplicated. Zero-sized elements are distinguished by element positions, not addresses, including legal maximal-length slices. Empty uninhabited-element slices need no fabricated inhabitant. |
| Stable const | Both bodies retain `pub const fn`; the new operations must compile under stable Rust 1.96 with bootstrap removed, including real const calls and writes through the returned references. |

The versioned pattern rules already retained in
[`.argus/sources/74d2d8be6f6312a91e3caccc.txt`](../.argus/sources/74d2d8be6f6312a91e3caccc.txt)
at 252-274 specifically make the binding mode `ref mut` for a mutable
reference; 351-362 and 742-774 describe rest and slice patterns. The
[indexing rules at 78-103](../.argus/sources/62a6f833b4275b9bc1651123.txt)
and [MIR projections at 1225-1251](../.argus/sources/d30066527f26d75ae5d1fd58.txt)
identify the same zero-based and end-relative element positions. Generic
Rust 1.96 metadata/MIR and native original/proposal/public comparisons are
supplementary checks, not a universal proof of source correspondence.

The versioned [place-expression rules at 137-155](../.argus/sources/9f5f534ec42f485af1d6a3fe.txt)
classify both slice indexing and the pattern scrutinee as places rather than
owned element values. The [borrow rules at 63-73](../.argus/sources/df6d9bcc218b2f61bf5e45cc.txt),
fetched from the Rust 1.96 Reference with `argus.tools.web_source`, specify
that `&mut` borrows that location exclusively until the borrow expires.
The [lifetime-elision rules at 29-35](../.argus/sources/3710179701fb89b97071de07.txt)
tie the returned reference to the input for both the original method and
its lifted one-parameter proof function.

### Candidate and existing trusted boundary

The selected vstd already registers the exact public methods at
`toolchain/upstream/source/vstd/std_specs/slice.rs:498-513`. They must not be
registered again. On an empty initial view those contracts require `None`
and `final(slice)@ == seq![]`. Otherwise they require `Some`, its initial
pointee equal to position zero or the last initial element, and
`final(slice)@ == old(slice)@.update(index, *final(result.unwrap()))`.
The candidate must express the same complete relation and allow a final
element value different from its initial value.

The existing `View for [T] = Seq<T>`, slice length correspondence and
`usize` mutable-index contract are dependencies, not new proofs of Rust's
metadata or indexing implementation. In particular,
`toolchain/upstream/source/vstd/std_specs/slice.rs:17-35` defines
`index_mut_postcondition` by both initial pointee equality and the entire
final slice update. Source proofs may import only pure candidate predicates,
not a local assumed target binding, and may not call the target methods.
The nonempty premise is necessary for the selected index; an unconstrained
out-of-range spec index does not imply it. The full update clause already
implies the unborrowed frame and length and should not be accompanied by
redundant independent postconditions.

If direct checker extraction cannot observe `Option<&mut T>` completely,
the value-state representation must use only the initial `Seq<T>` and the
caller's final `Option<T>` as inputs. Its compared outputs are the initial
`Option<T>` observation and the entire final `Seq<T>`. Shape must follow the
original return branch, every legal replacement must be representable, and
the empty branch must not need a `T`. Neither final original slice nor a
frame assumption may be placed in the inputs. This analysis does not grant
permission to adopt either source conversion.

No mutable endpoint is marked complete by the proposal alone. Original
patterns, isolated proposed files and later adopted current files remain
distinct. The project-only
[temporary redundancy criterion](../review-criteria-temporary.txt) applies
to these two candidates and their subsequent reviews.

### Isolated mutable source and native results

The two current original proof files were actually compiled with
`--crate-type lib --compile --no-cheating --num-threads 1`. Each is rejected
at its own slice pattern before checking a source obligation. The commands
and diagnostics are in
[`logs/mutable-endpoints-proposal/correctness/original/`](../logs/mutable-endpoints-proposal/correctness/original/).
At that stage both files still contained the original patterns. Their full
pre-adoption contents are now preserved under `logs/mutable-endpoints/adoption-before/`;
the later permitted substitutions and new runs are recorded below.

The isolated files under `proofs/correctness/slice/proposals/` now compile
with the same flags, each reporting **one verified source function, no
imported proof functions and zero errors**. The successful commands,
libraries and full queries are in
[`logs/mutable-endpoints-proposal/extensional-empty/{first_mut,last_mut}/`](../logs/mutable-endpoints-proposal/extensional-empty/).
Their only local import is the pure
[`mutable_endpoints.rs`](../specs/slice/mutable_endpoints.rs).
No target call, target assumption, new axiom or trusted body is introduced.
The generated source queries explicitly check the nonempty index bounds,
and `last_mut` also checks subtraction. Mutable-index lowering uses the
existing `spec_slice_index`, `spec_slice_update` and their view
correspondence; the returned reference's final value is propagated through
the latter to the whole slice. This is the same value relation as the
existing `usize::index_mut_postcondition`, not a separately proved Rust
index implementation.

The first isolated attempt used ordinary sequence equality for the empty
final slice inside an opaque-to-extensionality helper. Its postcondition
proof failed; the original candidate text and queries remain in
[`correctness/proposal/`](../logs/mutable-endpoints-proposal/correctness/proposal/).
The current helper exposes extensional equality for that empty sequence.
The two `*_candidate_correspondence` lemmas prove equivalence to the exact
unchanged vstd postconditions, including their ordinary `== seq![]`.
No observation or caller write was removed. The aggregate compiled with
`--compile --num-threads 1`, without `--no-cheating` because of the older
public declarations, and checked the same two imported consistency lemmas.
Its result is not another API proof.

The native group is `mutable-endpoints-proposal`, with `--output-root`
and the existing project-local linker. Its earlier Rust 1.96 run retained
metadata and generic runtime/const MIR, actually linked and executed
**17 tests**, and checked **96 expected compiler rejections**:
[`pre-adoption-3/logs/mutable-endpoints-proposal/native/`](../logs/mutable-endpoints-proposal/pre-adoption-3/logs/mutable-endpoints-proposal/native/).
That run used the earlier empty-sequence expression, before the candidate
changed from `==` to `=~=`. It is retained as historical evidence, not as
a native replay of the current candidate.
The authority MIR tests `n >= 1` and borrows `[0 of 1]` or `[-1 of 1]`.
The proposal MIR tests `n == 0`, then checks the index; the last method
computes `SubWithOverflow(n, 1)` before starting its mutable element borrow.
These generated forms agree with the generic place/length argument above.

All three implementations are exercised with actual changed values and
whole-slice/subslice-frame observations. The cases include empty,
singleton, ordered and repeated elements, non-Copy and non-static elements,
zero-sized elements, maximum-length legal unit slices and legal empty
uninhabited slices. Exact higher-ranked mutable signatures, stable const
writes, wrong arguments and return types, lifetime escapes and both shared
and mutable conflicting accesses are checked. A returned borrow is kept
live in the conflicting-access probes. Address equality is not used to
infer zero-sized element positions.

The earlier native runner's focused Python tests, including its affected
groups, passed **75 tests**, of which 20 cover this new group:
[`python-tests-3.log`](../logs/mutable-endpoints-proposal/python-tests-3.log).
Those results also precede the candidate's extensional-empty change.
Earlier const-probe and MIR-printing failures remain recorded. The successful
maximum-length unit case uses safe `vec![(); usize::MAX]` rather than a giant
unit array constant that made the Rust 1.96 MIR printer fail; this is a
test-input representation change, not an API/source conversion.
None of these engineering runs grants independent permission or changes a
coverage result for an adopted source body.

### Synchronizing the native check with the current candidate

Independent review ran the native command through the restricted read-only
path and received `Mutable endpoint pure contract drift` before any Rust
compiler invocation. The exact-predicate text in `scripts/check_native.py`
still expected `observations.1 == seq![]`, whereas the proved candidate
uses `observations.1 =~= seq![]`. The corresponding mutation case in
`tests/test_native_mutable_endpoints.py` also retained the old string and
failed its `assertIn` check. The earlier successful runs above therefore
could not count as current independent native execution. Review withheld
both mutable conversion permissions; no environment repair was requested.

The repair changes only the runner's expected empty clause and the matching
mutation input to `=~=`. A further mutation restores `==` and must still be
rejected, preserving exact text correspondence rather than accepting both
spellings. The full-string comparison, all other rejection conditions, the
candidate, both original source bodies and both isolated proposals remain
unchanged.

The affected Python modules compile during their actual imports by unittest.
The native-runner, mutable-binding and existing contract-binding modules
passed **42 tests** in
[`current-contract-python/unittest.log`](../logs/mutable-endpoints-proposal/current-contract-python/unittest.log).
The retained command uses the complete project rather than an incomplete
temporary source copy. This run does not repeat the unchanged formal
proofs or checker analyses that independent review already verified.

The repaired runner then completed a fresh actual Rust 1.96 execution under
[`current-contract/logs/mutable-endpoints-proposal/native/`](../logs/mutable-endpoints-proposal/current-contract/logs/mutable-endpoints-proposal/native/).
Its source record contains the unchanged current candidate, including both
`=~=` empty clauses. The 100 command records include successful metadata/MIR
compilation, linking and execution of all **17 runtime tests**, followed by
**96 compiler rejections with the expected diagnostics**. Temporary binaries
were removed; source inputs, metadata, MIR and logs remain. The exact command
uses the same project-local linker and explicit `RUSTUP_HOME` as the existing
review guidance. The durable execution record is
[`.argus_subagents/slice-mutable-endpoints-native-current-contract.json`](../.argus_subagents/slice-mutable-endpoints-native-current-contract.json).

This is fresh engineering evidence for the current files, not an independent
replay. The current result link in
[`runtime-review-readiness.json`](../runtime-review-readiness.json) now points
to that run, while the earlier output directories and failed review account
remain preserved. Independent review must resume the restricted native run
and decide the two conversion permissions before any adoption. The original
proof bodies, candidates, state lemmas, checker inputs/configuration,
coverage TSV and all previous exports were not changed by this repair.

### Independent mutable permission before adoption

The second review independently reran the repaired native group through
`run_review_command`/`get_review_command`, using the project-local linker,
explicit `RUSTUP_HOME` and scratch-only outputs. Rust 1.96 metadata/MIR,
actual linking and execution completed: **17 runtime tests and 96 expected
compiler rejections passed**. The review also independently compiled the
Python files and ran the native/mutable binding tests in a content-matched
temporary project: **25 tests passed**. Its durable account is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/02036b1aebf8/round-0002.json`.
The earlier native mismatch and all preceding records remain preserved.

The permission explicitly covers only:

```rust
if slice.len() == 0 { None } else { Some(&mut slice[0]) }
```

and

```rust
if slice.len() == 0 {
    None
} else {
    let i = slice.len() - 1;
    Some(&mut slice[i])
}
```

The review matched the original `n >= 1` pattern projections with these
complementary branches, checked that subtraction and index bounds precede
the mutable element borrow, and confirmed the same exclusive place,
input-bound lifetime and borrow-end writeback for all legal lengths.
It combined versioned language rules with generic MIR rather than treating
finite native examples as universal equivalence. The unchanged candidate,
seven state lemmas, regression proofs and two full-observation checker
analyses/reexecutions retain the first review's independent support;
the second review did not repeat unchanged formal work.

There is no remaining request for conversion permission. Adoption must now
preserve the original files and isolated proposals, change only the two
current bodies, and produce new current-source compilations and native
comparisons. Selective export and its real CLI failure/preservation tests
are still required. The adopted files and exported results need final
independent review; the permission itself does not complete either API.

### Adopted mutable source results

After recording the independent permission above, the two current files
received only the approved body substitutions. The complete originals,
isolated proposals, candidate, state/analysis inputs, former native runner
and prior coverage are preserved in
[`logs/mutable-endpoints/adoption-before/`](../logs/mutable-endpoints/adoption-before/).
The current candidates, public registrations, signatures, const capability
and input-bound lifetimes did not change. Original failure diagnostics and
the separate proposal files remain available.

Both adopted source proofs were newly compiled with
`--crate-type lib --compile --no-cheating --num-threads 1`. Each verifies
**one current source target and zero imported proof functions**:
[`correctness/first_mut/`](../logs/mutable-endpoints/correctness/first_mut/) and
[`correctness/last_mut/`](../logs/mutable-endpoints/correctness/last_mut/).
Each directory retains the exact command, return code, compiled library,
source/predicate input copies and solver transcript. The only root
`Function-Def` is the intended endpoint, with UNSAT; the pure contracts
module contains no proof function. This is new current-source execution,
not reuse of the isolated source compilation.

The state lemmas, both analysis adapters, candidate, slice type-source and
configuration are unchanged. Their previously executed and independently
reviewed discovery, analyze and reexecution results remain under
[`logs/mutable-endpoints-proposal/completeness/`](../logs/mutable-endpoints-proposal/completeness/).
They were not rerun merely because an unrelated executable proof body moved
from proposal to current. The exporter checks all current analysis inputs
against both frozen runs and native proof worktrees, the selected `@8`
identities, exact commands including `--reexecute` without configuration
override, full Option/element/final-sequence comparison, and all 13 disabled
search guards. It also requires the separately compiled seven state lemmas.
The unchanged aggregate's two consistency obligations likewise retain their
earlier compilation and independent review; they are not new API targets.

The current native route is now `--group mutable-endpoints`. It extracts
the two adopted bodies from the actual current proof files and compares
them with authority patterns and real public methods. The former
`mutable-endpoints-proposal` route was removed, not left as a parallel
execution path; the isolated files can be absent or changed without affecting
the current comparison. New Rust 1.96 metadata/MIR compilation, linking and
execution passed **17 tests and 96 exact compiler rejections** in
[`current-native/logs/mutable-endpoints/native/`](../logs/mutable-endpoints/current-native/logs/mutable-endpoints/native/).
The 31 affected native/binding Python tests passed in
[`python-tests.log`](../logs/mutable-endpoints/python-tests.log).
The behavior input differs from the original suite only in implementation
labels and file names; its writeback and rejection checks were not relaxed.
The restricted independent argv now uses `mutable-endpoints` and remains in
[`runtime-review-readiness.json`](../runtime-review-readiness.json).

The real
`scripts/export_completeness.py --mutable-endpoints`
invocation then wrote only the two selected result rows and added
[`proofs/completeness/slice/first_mut.rs`](../proofs/completeness/slice/first_mut.rs)
and [`last_mut.rs`](../proofs/completeness/slice/last_mut.rs).
These are the actual generated checker sources with only the relative state
import relocated; they were not replaced by handwritten comparisons.
Both exported files were newly compiled with `--compile --num-threads 1`,
each reporting **nine verified obligations**: one generated comparison,
one value-state adapter and seven imported lemmas. Their generated search
assumptions require the ordinary compile mode; the original-query checks
above separately establish that all guards are disabled. The exports are
not source implementation proofs.
Commands, queries and compiled libraries are in
[`exported-compile/`](../logs/mutable-endpoints/exported-compile/).

The exporter validates both selected APIs completely before writing either
result, preserves raw unselected TSV records, and refuses a conflicting
existing output proof. **39 Python tests passed**, including **170 mutable,
119 shared-endpoint and 135 split actual CLI cases**. The mutable cases
include failed/zero/partial source proofs, wrong targets or commands,
missing state obligations, stale candidates and dependencies, UNKNOWN,
wrong replay parents, configuration overrides, missing Option/element/
writeback comparison and every enabled search guard. Each rejected mutable
invocation leaves every existing file byte-identical. Results are in
[`export-tests/`](../logs/mutable-endpoints/export-tests/) and
[the durable test log](../.argus_subagents/slice-mutable-endpoints-export-tests_logs/stderr.log).

The actual project export's
[`preservation.json`](../logs/mutable-endpoints/export-current/preservation.json)
confirms **329 unselected records**, all **15 preexisting top-level
completeness Rust files**, five original observer failure logs and the
mutable original failures/direct inputs/isolated proposals remain
byte-identical. Only the two new API results and their two comparison files
were added. The issue references and pending final independent review remain
explicit in both selected rows.

This completes adoption and engineering integration, not final independent
review of the adopted files. No metadata, indexing, singleton or other API
implementation proof is claimed. The candidate is unchanged, so the prior
independent redundancy judgment still applies; no new semantic clause or
public assumption was introduced.

## Retained original failures

Independent review reproduced the Verus slice-pattern translation rejections
for all four APIs in this report.
No Rust implementation or documentation defect is alleged.

Rust 1.96 uses slice patterns for all four reference-returning APIs:

| API | Source body | Original pattern |
|---|---|---|
| `first` | `core/src/slice/mod.rs:155-157` | `[first, ..]` |
| `split_first` | `core/src/slice/mod.rs:198-200` | `[first, tail @ ..]` |
| `split_last` | `core/src/slice/mod.rs:240-242` | `[init @ .., last]` |
| `last` | `core/src/slice/mod.rs:281-283` | `[.., last]` |

The immediately preceding docstrings require `None` for the empty slice and
the corresponding element and ordered remainder otherwise. In particular,
`split_last` returns `(last, init)`, not `(init, last)`.

On official unmodified Verus `0.2026.09.20.aef82ed`, matching vstd and host
Rust `1.98.1`, the first exact source proof gives:

```text
error: The verifier does not yet support the following Rust feature: slice patterns
  --> proofs/correctness/slice/first.rs:11:12
   |
11 |     if let [first, ..] = slice { Some(first) } else { None }
   |            ^^^^^^^^^^^
```

The native compiler diagnostic is retained in
[`logs/foundation/correctness/first/verus.log`](../logs/foundation/correctness/first/verus.log).
The corresponding selected upstream frontend at
`toolchain/upstream/source/rust_verify/src/rust_to_vir_expr.rs:926` contains
`PatKind::Slice(..) => unsupported_err!(pat.span, "slice patterns", pat)`.
This is an actual syntax-support limitation, not an inconclusive solver
result. The source proof checks zero relevant obligations.

```sh
toolchain/verus-x86-linux/verus proofs/correctness/slice/first.rs \
  --crate-type lib --crate-name slice_first_source --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/foundation/correctness/first/queries \
  -o target/foundation/libslice_first_source.rlib
```

The other three source inputs were each run and produced the same explicit
slice-pattern rejection. Their own inputs and diagnostics remain in
`proofs/correctness/slice/<api>.rs` and
`logs/foundation/correctness/<api>/verus.log`; no result is inherited from
`first`. The actual per-API commands and native completeness queries are
joined in [`inventory/coverage.tsv`](../inventory/coverage.tsv).
All four corresponding files under `proofs/completeness/slice/<api>.rs`
contain exported native specdet harnesses, with deterministic results.
Those results do not discharge these implementation proofs.

The original report proposed testing the length, indexing the appropriate
element and forming the corresponding range. It raised that executable
desugaring **before adoption**; no body was replaced at that stage.
Any such proposal must preserve empty and singleton behavior,
lifetimes, tuple order, zero-sized elements, unconstrained non-Copy elements,
panic/safety behavior and constness. It needs a checked source bridge and
strict independent review; proofs that merely use vstd's assumed `first`
or `split_first` contract do not supply that bridge.

The Engineer's retained native Rust behavior probes confirm the source
expressions' expected examples and signatures, but are not Verus
implementation proofs. Reviewer's native runtime rerun stopped for missing
`cc` before behavior tests; independent runtime reproduction is not claimed.
The independent review confirmed all four translation rejections, not the
missing source proofs; see the
[review account](../inventory/COVERAGE.md#independent-review-and-redundancy-repair).
The APIs remained incomplete at that stage. No upstream issue is filed and
external filing awaits separate authorization.

## Proposed conversion of `first` and `last`

This `implementation-change` proposal was raised within the existing
`verus-limitation` issue before adoption. At that point it had no independent
permission and `proofs/correctness/slice/first.rs` and `last.rs` still contained
their original slice patterns. The independent permission recorded below now
covers these two exact conversions. The prior ASCII call-rebinding permission
does not cover this proposal. Neither split method is included.

The authority is
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice/mod.rs`.
Lines 140-150 say, "Returns the first element of the slice, or `None` if it
is empty," and demonstrate `[10, 40, 30]` and an empty slice. Lines 266-276
make the corresponding statement and examples for the last element. The
unaltered bodies at 155-157 and 281-283 are:

```rust
pub const fn first(&self) -> Option<&T> {
    if let [first, ..] = self { Some(first) } else { None }
}

pub const fn last(&self) -> Option<&T> {
    if let [.., last] = self { Some(last) } else { None }
}
```

The surrounding `impl<T> [T]` is unconstrained. Both methods are stable
since Rust 1.0 and const-stable since Rust 1.56. Only the following executable
changes are proposed for the already lifted, source-derived proof functions:

```diff
--- proofs/correctness/slice/first.rs
+++ proofs/correctness/slice/first.rs
@@
-    if let [first, ..] = slice { Some(first) } else { None }
+    if slice.len() == 0 { None } else { Some(&slice[0]) }
--- proofs/correctness/slice/last.rs
+++ proofs/correctness/slice/last.rs
@@
-    if let [.., last] = slice { Some(last) } else { None }
+    if slice.len() == 0 { None } else { Some(&slice[slice.len() - 1]) }
```

There is no change to authoritative Rust, `first_post`, `last_post`, the
selected upstream slice view, the public bindings, or either proof signature.
An experiment may use copies under
`proofs/correctness/slice/proposals/`; their different relative module path
only imports the same existing contract file. A successful experiment is
not a successful current source proof and must not update coverage or exports.

### Source correspondence to be independently checked

Let `n` be the element count of an arbitrary legal `&'a [T]`. This is a
machine `usize`, not a byte count; no nonempty, `Copy`, `Eq`, or `'static`
premise is introduced.

| Obligation | Original pattern and proposed expression |
|---|---|
| Branch condition on every input | Each pattern contains exactly one element subpattern and a rest pattern. It matches exactly when `n >= 1`. The proposed `n == 0` test chooses `None` exactly on its complement because `n` is unsigned. |
| First borrowed place | `[first, ..]` binds a shared reference to element zero of the matched slice. In the nonempty branch `&slice[0]` borrows that same place; `0 < n` proves its index valid. |
| Last borrowed place | `[.., last]` binds a shared reference to the final element, at index `n - 1`. The proposed branch borrows precisely `&slice[n - 1]`, not an element with merely equal contents. |
| Subtraction and indexing safety | On the last branch, `1 <= n <= usize::MAX`, so `n - 1` is representable and `0 <= n - 1 < n`. On the empty branch no indexing or subtraction is evaluated. Neither new failure path is reachable, including at the largest legal zero-sized slice lengths. |
| Evaluation and observable effects | The scrutinee and proposed receiver are the same local shared slice reference. The proposal reads its length before branching, and `last` reads the same length again only on the nonempty branch. Slice metadata is unchanged by either expression; no user callback, element comparison, move, clone, write, allocation, or destructor runs. Taking a shared element reference does not read or copy the value of `T`. |
| Borrowing and lifetime | Matching the shared slice uses shared-reference binding. Shared indexing borrows from that same slice, within the same allocation/provenance and input lifetime. Elision still means `for<'a> fn(&'a [T]) -> Option<&'a T>`. Neither expression creates an owned temporary element, a mutable borrow, nor an escaping reference. |
| Zero-sized and uninhabited elements | Indices are element positions, even when distinct positions have identical addresses. No `size_of::<T>()` or pointer-offset calculation is introduced. Legal empty slices of an uninhabited `T` follow the empty branch without constructing a `T`; the correspondence quantifies over legal references rather than manufacturing invalid nonempty slices. |
| Stable const behavior | The proof signatures remain `pub const fn`. The added operations are slice length, integer comparison/subtraction, shared built-in slice indexing, and `Option` construction. Rust 1.96 must compile both original and proposed generic functions and actual const invocations with bootstrap disabled. |

The ordinary Rust argument concerns the borrowed place as well as its
contents. In contrast, the existing candidates observe the `Option` variant
and full value `*result`, not reference-address equality. Proving both bodies
satisfy those candidates, or testing pointer equality, would not by itself
establish this source correspondence. In particular, address equality cannot
distinguish different zero-sized element positions.

The native comparison must compile the original patterns extracted from the
authority and the exact two isolated expressions with Rust 1.96, retain MIR
showing the length branches and borrowed projections, and compare both with
the real public methods. Empty, singleton, ordered multi-element, zero-sized,
non-Copy, non-static and empty-uninhabited inputs are relevant. Signature,
const, wrong-argument, return-mutability and lifetime-escape probes are
additional checks, not a replacement for the argument above.

The versioned primary language sources supporting this argument were fetched
with the authorized Argus web-source command and retained locally:

| Primary source | Retained text and relevant rules |
|---|---|
| [Rust 1.96 patterns](https://doc.rust-lang.org/1.96.0/reference/patterns.html) | [`.argus/sources/74d2d8be6f6312a91e3caccc.txt`](../.argus/sources/74d2d8be6f6312a91e3caccc.txt), lines 252-274, 351-362, 742-774: automatic shared-reference binding, the rest pattern matching zero or more remaining elements, and dynamic slice patterns |
| [Rust 1.96 indexing](https://doc.rust-lang.org/1.96.0/reference/expressions/array-expr.html) | [`.argus/sources/62a6f833b4275b9bc1651123.txt`](../.argus/sources/62a6f833b4275b9bc1651123.txt), lines 78-103: built-in `usize` indexing of slices, zero-based positions and bounds checks |
| [Rust 1.96 MIR syntax](https://raw.githubusercontent.com/rust-lang/rust/1.96.0/compiler/rustc_middle/src/mir/syntax.rs) | [`.argus/sources/d30066527f26d75ae5d1fd58.txt`](../.argus/sources/d30066527f26d75ae5d1fd58.txt), lines 1225-1251: slice-pattern `ConstantIndex`, zero-based start offsets, one-based end offsets and minimum lengths |

The canonical `slice/index.rs:269-272` explicitly uses intrinsic indexing for
`usize`. This proposal uses built-in slice index expressions, not an explicit
const call to the still const-unstable `Index` or `SliceIndex` trait methods.
Stable const compilation below checks that distinction on Rust 1.96.

### Existing trusted dependencies and limits

Rust's `len` documentation and body at `slice/mod.rs:102-118` specify the
element count and use `ptr::metadata`. On the selected unmodified vstd,
`toolchain/upstream/source/vstd/slice.rs:13-17` supplies `View for [T]`;
lines 71-87 supply `spec_slice_len`, `axiom_spec_len` and the existing
`<[T]>::len` specification. The executable shared-index bridge is
`slice_index_get` at lines 59-69: it requires an in-range index and relates
the borrowed value to `slice@.index(i as int)`. The existing spec-index
correspondence is at lines 186-193. These are upstream trusted declarations,
not proofs supplied by this conversion.

The actual isolated queries use Verus's built-in slice-index lowering:
an explicit in-bounds obligation followed by `spec_slice_index`, related to
the existing view by `axiom_spec_slice_index`. They do not call the
`slice_index_get` helper. That helper describes the same upstream shared-index
boundary but is not an additional executed or verified dependency here.

The proposed source proof must discharge its branch, subtraction and index
obligations and the unchanged endpoint postcondition using those existing
dependencies. It must not call the target `first` or `last`, import their
assumed contracts as a proof, introduce an axiom or `external_body`, or modify
Rust, vstd, Verus, or the checker. Neither this argument nor an experiment
proves the Rust metadata implementation. No conclusion extends to
`split_first`, `split_last`, singleton constructors, or general slice-pattern
support.

Independent review must decide this exact two-body conversion before adoption.
After permission, only the two current proof copies may receive it, followed
by their actual source compilation, aggregate compilation, the two current
specdet analyses and reexecutions, narrowly scoped source-binding/native/export
checks, and final independent review. Original patterns and failure logs remain
part of this issue throughout. The project-only redundancy criterion in
[`review-criteria-temporary.txt`](../review-criteria-temporary.txt) continues
to apply; these proposals do not alter either candidate.

### Isolated results, without adoption

This section records the experiments before permission. The later adoption
and its new runs are recorded separately below.

Both isolated files compiled with the selected unmodified Verus. Each checked
**one proposed endpoint function and two imported consistency lemmas**
(`contracts::scalar_domain`, `contracts::empty_results`), reporting
`3 verified, 0 errors`. These are not three API proofs, and the current
pattern-based source proofs remain incomplete. The actual commands were:

```sh
RUSTUP_HOME=/home/chentianyu/.rustup \
  toolchain/verus-x86-linux/verus proofs/correctness/slice/proposals/first.rs \
  --crate-type lib --crate-name slice_first_proposal --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/endpoints-proposal/correctness/first/queries \
  -o target/endpoints-proposal/libslice_first_proposal.rlib
RUSTUP_HOME=/home/chentianyu/.rustup \
  toolchain/verus-x86-linux/verus proofs/correctness/slice/proposals/last.rs \
  --crate-type lib --crate-name slice_last_proposal --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/endpoints-proposal/correctness/last/queries \
  -o target/endpoints-proposal/libslice_last_proposal.rlib
```

The compiler/verifier logs are
[`logs/endpoints-proposal/correctness/first/verus.log`](../logs/endpoints-proposal/correctness/first/verus.log)
and
[`logs/endpoints-proposal/correctness/last/verus.log`](../logs/endpoints-proposal/correctness/last/verus.log).
The corresponding `queries/root-final.air` files contain the actual target
obligations at lines 3055-3114 and 3055-3125, respectively. The first query
checks index zero in the nonempty branch; the last additionally checks the
machine subtraction before its index bound. Both check the original endpoint
postcondition without a new input precondition. This is symbolic coverage of
the legal length domain, not an extrapolation from the native examples.

The native group was run as:

```sh
RUSTUP_HOME=/home/chentianyu/.rustup \
  /home/chentianyu/Argus/.venv/bin/python -B scripts/check_native.py \
  --group endpoints-proposal --output-root logs/endpoints-proposal/pre-adoption
```

It compiled with Rust 1.96, bootstrap removed, overflow checks enabled and
optimization disabled; executed **14 tests**; and checked **60 expected
compiler rejections** against their relevant diagnostics. It compares
authoritative patterns, exact isolated bodies and the public methods, including
the documented values, non-ZST reference positions, non-Copy/non-static values,
interior-mutability/drop observations, empty uninhabited slices and a legal
`usize::MAX`-length unit slice. It also compiles the exact higher-ranked shared
signatures and actual empty/singleton/multiple-element const calls.

All 63 native command exits, source mappings, retained source, runtime output
and rejection diagnostics are under
[`logs/endpoints-proposal/pre-adoption/logs/endpoints-proposal/native/`](../logs/endpoints-proposal/pre-adoption/logs/endpoints-proposal/native/).
`results.json` records the 14 executed tests and all 60 rejected cases;
`commands.json` records the compiler, bootstrap removal and command exits;
`source-spans.json` retains the authoritative docs, attributes and bodies and
both current and proposed proof inputs. Only temporary binaries and rejection
source files were removed.

The generic compiler output in that directory,
`endpoint_proposal_behavior.mir`, supports the following more specific
comparison. The interpretation of its constant projections follows the
versioned MIR source above, not address-based tests:

| Function and MIR lines | Branch and returned place |
|---|---|
| `original::first`, 4-34 | `PtrMetadata(_1) >= 1`; the successful branch returns a shared `&(*_1)[0 of 1]`, a start offset of zero with minimum length one |
| `original::last`, 79-109 | The same length test; a shared `&(*_1)[-1 of 1]`, an end offset of one with minimum length one, therefore position `n - 1` |
| `proposal::first`, 154-191 | The zero-length branch returns `None`; the other branch checks `0 < n` and returns a shared `&(*_1)[0]` |
| `proposal::last`, 254-299 | The zero-length branch returns `None`; the other branch computes checked `n - 1`, checks it below `n`, and returns a shared borrow at that index |

The additional panic successors in the proposed MIR are real compiler
checks, not silently omitted behavior. Under the nonempty branch they are
unreachable by the arithmetic argument above, whose obligations are also
discharged in the isolated Verus queries. The original MIR's pattern
projections and the proposed MIR's indices use the same `_1` slice place.
The const-evaluation MIR at lines 37-77, 112-152, 194-252 and 302-378 preserves
the same division into empty and nonempty branches and the same shared
projections. None of this claims an independently completed source bridge.

The changed native runner and existing exact binding tests also passed
**48 Python tests**. The actual invocation, exit code and output are retained
in `logs/endpoints-proposal/python-unit-command-2.json` and
`python-unit-2.log`. The original exact-body and exact-analysis comparisons
were not relaxed. Earlier experimental failures remain in `python-unit.log`
and `logs/endpoints-proposal/native/`: the early native launch had no proposal
files yet and executed zero tests. It is not included in the successful counts.

No current correctness file, candidate, analysis input, completeness export,
coverage row or historical source-failure log was replaced. The unchanged
aggregate and checker analyses were not rerun at this pre-adoption stage.
After permission, the actual affected checker selectors remain
`proofs/completeness/slice/inputs/first.rs:first@13` and
`proofs/completeness/slice/inputs/last.rs:last@13`; fresh analyze/reexecute
results and source/export integration are still required. Reviewer should
first decide the two precise conversions above using the existing
`run_review_command` / `get_review_command` route with all outputs in
`{scratch}` and explicit `RUSTUP_HOME` as needed.

### Independent permission before adoption

The independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/6c2571b94578/round-0001.json`
explicitly authorizes only the two exact diff expressions above in the
current source-proof copies. This decision was recorded here before changing
either body. Authoritative Rust, candidates, public signatures, the upstream
view and both split methods are outside that permission. Final independent
review after integration is still required.

Reviewer directly compared the Rust 1.96 docs and original bodies, current
proofs, isolated copies, the retained language Reference and MIR projection
definitions. The correspondence covers every legal length: the original
patterns match exactly at `n >= 1`; the explicit empty branch is its
complement; the shared projections are the same elements of the same slice.
The `0 < n` and `0 <= n - 1 < n` obligations exclude all newly introduced
index/subtraction failures. The argument uses no element move, copy or
comparison, no new bound, and no address-equality inference for zero-sized
positions.

Through the restricted read-only command route, Reviewer compiled and
verified both isolated files with
`--crate-type lib --compile --no-cheating --num-threads 1`: each exited zero
and checked one endpoint plus `scalar_domain` and `empty_results`, reporting
`3 verified, 0 errors`. The generated obligations included index bounds and
the last-element subtraction. Rust 1.96 metadata and MIR compilation without
bootstrap and with overflow checks also succeeded; the independent review
checked runtime and const-evaluation shared projections, all 60 expected
compiler rejections, and 21 Python runner/binding tests.

The independent native runtime attempt did **not** complete. The sandbox
could not use the Argus Python path; using the authorized miniconda Python
then reached a linker failure because `cc` was absent. Reviewer compared the
retained inputs with current source and inspected the Engineer's 14 successful
runtime tests, but did not independently execute them. Metadata compilation
does not replace those runtime tests. This limitation is retained, not treated
as an environment or API success. It does not invalidate the explicit
source-correspondence permission grounded in language semantics, all-length
safety, actual Verus proofs and independent MIR comparison.

The temporary redundancy review found no removable clause. In each Some
branch, the element equality alone cannot establish nonemptiness: a sequence
index outside its bounds does not supply that fact. Both the existing
nonempty condition and the complete element-value equality remain unchanged.
The required next work is adoption, current-source and aggregate compilation,
the two actual checker analyses/reexecutions, exact binding/native comparisons
and source-only export integration; no further wait for conversion permission
is necessary.

### Adopted current-source results

After recording the independent permission, only the two executable lines
shown in the diff were replaced in `proofs/correctness/slice/first.rs` and
`last.rs`. Exact pre-adoption copies are retained in
`logs/endpoints/adoption-before/proofs/correctness/slice/`. The original
analysis bodies, candidates, public signatures and upstream dependencies
remain unchanged; the split methods still have their original failures.

The current source files, not proposal files, were each compiled with
`--crate-type lib --compile --no-cheating --num-threads 1 --log-all`.
Their actual command arrays, exits, stdout/stderr, source/contract snapshots,
queries and compiled libraries are under
`logs/endpoints/correctness/first/` and `last/`.

| Current input | Actual compiled result | Scope |
|---|---|---|
| `proofs/correctness/slice/first.rs` | Exit 0; 3 verified, 0 errors | One endpoint and two imported consistency lemmas; index bound and unchanged `first_post` |
| `proofs/correctness/slice/last.rs` | Exit 0; 3 verified, 0 errors | One endpoint and two imported consistency lemmas; subtraction safety, index bound and unchanged `last_post` |
| `specs/mod.rs` | Exit 0; 2 verified, 0 errors | Specification aggregate and its two consistency lemmas, not two additional API proofs |

The aggregate's successful command and compiled library are under
`logs/endpoints/correctness/aggregate_current/`. As in the existing aggregate
workflow, it uses `--compile` without `--no-cheating` because it imports the
already existing specification declarations. The two executable source
proofs retain `--no-cheating`. The failed aggregate invocation with
`--no-cheating` is preserved in `correctness/aggregate/`; a subsequent command
with an invalid hyphenated crate name is preserved in `aggregate-bindings/`.
Neither is counted as a proof, and neither failure caused a source or
specification change.

Fresh actual `specdet analyze` and `replay --reexecute` runs used exactly
`proofs/completeness/slice/inputs/first.rs:first@13` and
`proofs/completeness/slice/inputs/last.rs:last@13`. The four commands and reports
are in `logs/endpoints/completeness/{first,last}/`, named
`{analyze,replay}-command.txt`, `{analyze,replay}-execution.json` and
`{analyze,replay}.json`. Each invocation exited zero, selected only its one
endpoint, verified one native determinism goal, and reported the original
query UNSAT. Reexecution restores the selected run without a `--config`
override, preserving its original target selector.

The actual generated comparison in all four runs is
`((r1 is Some) == (r2 is Some)) && ((r1 is Some) ==> (r1->Some_0 == r2->Some_0))`.
This observes the variant and complete referent value using Verus logical
equality, not Rust `PartialEq` or an allocation-address observation. The two
premises call the unchanged endpoint predicate on the same slice. Every
original query disables all seven guards: two slice-length guards, both
variants for each output, and `g_neq_tuple`. There is no search restriction,
new input premise, ignored value component or model-assisted proposal.
Current analysis/contract/config bytes were compared with both frozen
workspaces and the actual native worktrees; the analysis and replay harnesses
and original queries are identical. The other four observer analyses were
not rerun.

The native command is now
`scripts/check_native.py --group endpoints --output-root DIR`. Its sole
endpoint execution path extracts the **current adopted proofs**, the exact
authoritative patterns and the real public calls. Historical proposal
inputs/logs remain, but are not executed by this group. Source-binding tests
permit only the two approved substitutions; the other four original bodies
and all six analysis declarations are still compared exactly.
The actual Rust 1.96 run passed 14 runtime tests and 60 diagnostic-checked
rejections, with all 63 command exits retained under
`logs/endpoints/adopted-native-root/logs/endpoints/native/`. Source mappings,
the current inputs and runtime/const MIR are retained there. This engineering
run does not change the independent sandbox linking limitation recorded above.

`scripts/export_completeness.py --endpoints` validates the actual source
execution, nonempty compiled output, one successful target query plus the two
imported queries, both checker executions and all input snapshots before
writing. It rejects failed/zero/partial proofs, stale snapshots, mismatched
commands, changed observations, enabled search guards and a replay of the
wrong run. It updates source-result cells only; the default export path also
uses this checked endpoint evidence instead of restoring the old failures.
The 11 focused export tests passed **117 real CLI cases**, including rejected
inputs; their records are in `logs/endpoints/export-tests/current-reports/`.
An additional real-CLI test verifies that the test runner honors `TMPDIR` for
all temporary project copies, so independent review can keep writes in
`{scratch}`; its passing result is in
`logs/endpoints/export-tests/readonly-scratch/`. This adds one executed test
and CLI case without rerunning the unchanged proof tracks.

The real project export exited zero. Its before/after comparison in
`logs/endpoints/export-current/results.json` confirms exactly four changed
source-result cells in each endpoint row, **329 unrelated rows byte-identical**,
**14 existing completeness files byte-identical**, and **five historical
source-failure logs byte-identical**. Existing completeness cells and file
paths are unchanged; the fresh checker reports above are additional evidence,
not replacements for old results.

The adopted native runner and bindings passed 62 Python tests before export.
After export, one coverage assertion still expected the old zero endpoint
count; that failure is retained in `logs/endpoints/post-export-bindings/`.
The assertion now distinguishes `is_empty`, `first` and `last` from the three
remaining blocked original observers, and its actual rerun passed in
`post-export-bindings/revised/`. No candidate was changed to satisfy a test.
Final independent review of the adopted inputs and export remains pending;
the pre-adoption permission is not presented as that final review.

## Proposed conversion of `split_first` and `split_last`

This is a new `implementation-change` proposal within the existing
`verus-limitation` issue, raised before creating the isolated proof copies.
It is awaiting strict independent review, not an adopted change. The current
`proofs/correctness/slice/{split_first,split_last}.rs`, both candidates, both
analysis declarations, coverage and completeness exports remain unchanged.
All original failures and earlier experiments remain available.

The authority is
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/slice/mod.rs`.
The documentation at 182-193 says, "Returns the first and all the rest of the
elements of the slice, or `None` if it is empty," and shows the element `0`
followed by `[1, 2]` for `[0, 1, 2]`. Lines 224-235 state the last-element
counterpart and show `2` followed by `[0, 1]`. The exact original functions at
198-200 and 240-242 are:

```rust
pub const fn split_first(&self) -> Option<(&T, &[T])> {
    if let [first, tail @ ..] = self { Some((first, tail)) } else { None }
}

pub const fn split_last(&self) -> Option<(&T, &[T])> {
    if let [init @ .., last] = self { Some((last, init)) } else { None }
}
```

The surrounding `impl<T> [T]` at line 101 has no bound on `T`. Both methods
are stable since 1.5.0 and const-stable since 1.56.0. The shared receiver,
exact `Option<(&T, &[T])>` return, const signature and input-bound lifetimes
are unchanged. The proposed executable differences in the lifted proof
copies are exactly:

```diff
--- proofs/correctness/slice/split_first.rs
+++ proofs/correctness/slice/split_first.rs
@@
-    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }
+    if slice.len() == 0 {
+        None
+    } else {
+        Some((&slice[0], slice.split_at(1).1))
+    }
--- proofs/correctness/slice/split_last.rs
+++ proofs/correctness/slice/split_last.rs
@@
-    if let [init @ .., last] = slice { Some((last, init)) } else { None }
+    if slice.len() == 0 {
+        None
+    } else {
+        let i = slice.len() - 1;
+        Some((&slice[i], slice.split_at(i).0))
+    }
```

Only isolated files under `proofs/correctness/slice/proposals/` may contain
these expressions before permission. Their relative import points to the same
unchanged `specs/slice/mod.rs`; they do not import the target methods'
`assume_specification` declarations as implementation proofs.

### The delegated `split_at` operation

The canonical documentation at `slice/mod.rs:1913-1945` specifies the complete
ordered ranges `[0, mid)` and `[mid, len)`, with a panic only for `mid > len`.
The method at 1952-1957 calls `split_at_checked(mid)` and returns its `Some`
pair, otherwise panicking. Its attributes at 1946-1951 make it const-stable
since **1.71.0**, so it is a stable const dependency on the required Rust 1.96
baseline. This does not claim that the proposed bodies compile on 1.56-1.70.

`split_at_checked`, documented at 2114-2148 and implemented at 2153-2161,
tests `mid <= self.len()` and only then calls `split_at_unchecked(mid)`.
It is const-stable since 1.80.0. The unchecked method at 2038-2054 obtains
`len = self.len()` and `ptr = self.as_ptr()`, checks `mid <= len`, and constructs
exactly
`(from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid)))`.
The corresponding docs at 1993-2032 include the same ranges and require
`0 <= mid <= self.len()`. It is a const function, const-stable since 1.77.0.

The pointer is derived directly from the same shared slice by `as_ptr`
(`slice/mod.rs:694-728`), not reconstructed from an integer address.
`ptr.add(mid)` advances in units of `T`; the two slice lengths are `mid` and
`len - mid`. `slice/raw.rs:124-140` constructs shared references using those
pointer/length pairs. This source trace, together with the range docs,
establishes the origin and extent that are not expressed by a value-only
`split_at` contract. It is not a new Verus source proof of `split_at` or its
pointer dependencies.

The checked pointer safety rules are in `ptr/docs/add.md:7-25` and
`slice/raw.rs:6-40` beneath the same canonical `core/src` directory. A pointer
offset is measured in elements, with its mathematical byte offset bounded by
`isize::MAX`; a nonzero offset must stay within the originating allocation.
A shared raw slice requires a non-null aligned pointer, initialized consecutive
elements, one allocation and a valid shared lifetime. Each proposed split is
a subrange of the original legal slice, and zero-sized offsets are zero bytes.
The caller supplies none of these raw operations: the existing safe,
input-lifetime-bound `split_at` encapsulates them.

### Full source correspondence submitted for review

Let `slice: &'a [T]` be any legal input, let `n` be its element count and let
`p` be its element-zero base place. The claim is about borrowed places and
ordered ranges, not just equality of returned values.

| Obligation | Original patterns and proposed expressions |
|---|---|
| Every legal length | Each original pattern has one element and one rest pattern, so it matches exactly when `n >= 1`. Because `n` is unsigned, the proposed `n == 0` branch is exactly the complement. At zero it returns `None` without evaluating any element index, subtraction or `split_at`. |
| First element and remainder | The pattern uses `ConstantIndex { offset: 0, min_length: 1, from_end: false }` and `Subslice { from: 1, to: 0, from_end: true }`: element zero and `[1, n)`. The proposal borrows element zero, then takes component 1 of `split_at(1)`, whose base is the same input's position 1 and whose length is `n - 1`. For every `0 <= j < n - 1`, its position `j` is the original input's position `1 + j`. |
| Last element and remainder | The pattern uses `ConstantIndex { offset: 1, min_length: 1, from_end: true }` and `Subslice { from: 0, to: 1, from_end: true }`: element `n - 1` and `[0, n - 1)`. The proposal computes `i = n - 1`, borrows element `i`, then takes component 0 of `split_at(i)`, with base `p` and length `n - 1`. Every remainder position `j` is input position `j`. |
| Tuple order and complete sequence | Both results remain `(element, remainder)`, including `(last, init)` for `split_last`. The remainder maps above are increasing bijections onto the specified half-open input ranges. They therefore omit no required element, duplicate none, add none and reorder none, even when input values repeat. |
| Singleton empty remainders | At `n = 1`, the first remainder has length zero and begins at input position 1, the one-past position; the last remainder has length zero and begins at input position 0. The original `Subslice` projections and the delegated raw pointer/length construction agree on these distinct extents, not merely on the empty value sequence. |
| All machine arithmetic and checks | On either nonempty branch, `1 <= n <= usize::MAX`. Thus `0 < n`, `1 <= n`, and `0 <= n - 1 < n`. `n - 1` is representable, both element indices are in range, and both split indices satisfy `0 <= mid <= n`. Within `split_at`, `n - mid` cannot underflow. No `n + 1`, byte-count growth or unchecked operation is added by the proposal. |
| Actual evaluation | The first proposal tests the length, borrows element zero, then evaluates `split_at(1)` and selects its right slice. The last tests the length, computes `i` once, borrows element `i`, then evaluates `split_at(i)` and selects its left slice. Tuple operands evaluate left to right. The last original pattern binds the initial slice before the last element; these shared-borrow constructions have no user-visible effects, so that difference does not call user code or alter values. The extra panic successors are unreachable by the bounds above, not ignored. |
| Borrow validity and origin | Both original bindings borrow through the same `&'a [T]`. The proposal's built-in shared index and inherent shared `split_at` reborrow that input; neither reference originates in a temporary element or another allocation. Each returned lifetime is `'a` by the one-input/receiver elision rules. The discarded other `split_at` half is only a shared slice reference; it neither drops elements nor changes permissions. Additional shared references may overlap and do not invalidate the returned references. |
| Element behavior and domain | No operation moves, copies, compares, clones, drops or writes a `T`, and no user callback runs. `T` remains unconstrained: no `Copy`, `Eq`, `'static`, nonempty or length-limit premise. Interior mutability remains available to lawful callers but is not used by either body. Empty slices of an uninhabited type return `None` without creating a value. |
| Zero-sized elements and extent safety | Positions are element indices, not distinct byte addresses. For zero-sized `T`, `mid * size_of::<T>()` is zero even at maximal legal lengths; the length metadata still distinguishes the two remainder extents. For nonzero-sized `T`, each delegated range lies within the original legal slice allocation, so its byte extent cannot exceed the original one. An end position is used only for a zero-length remainder. No test of address equality is used to establish this generic correspondence. |
| Rust 1.96 const behavior | Both exact generic functions, their original patterns and real const invocations must compile with Rust 1.96 and `RUSTC_BOOTSTRAP` removed. Shared built-in slice indexing is used, not an explicit call to a const-unstable `Index` trait method. Length, integer comparison/subtraction, `Option` construction and the delegated inherent `split_at` are const-callable on this baseline. |

The retained Rust 1.96 primary sources are the same patterns, indexing and
MIR files linked above. In particular,
[`.argus/sources/d30066527f26d75ae5d1fd58.txt:1225-1267`](../.argus/sources/d30066527f26d75ae5d1fd58.txt)
defines both `ConstantIndex` and `Subslice`: the latter denotes
`slice[from..slice.len() - to]` when `from_end` is true.
The versioned
[expression rules](../.argus/sources/9f5f534ec42f485af1d6a3fe.txt)
at 97-120, 137-154 specify operand evaluation and borrowed places; the
[lifetime-elision rules](../.argus/sources/3710179701fb89b97071de07.txt)
at 29-35 assign both returned lifetimes to the input. The two additional
Reference pages were fetched through `argus.tools.web_source`, not inferred
from a different Rust release. Actual generic runtime/const MIR and native
results must be recorded separately; this argument is still submitted for
independent judgment.

### Explicit existing trusted dependencies

The proposed Verus proofs use the selected unmodified vstd, not new
assumptions, a local wrapper with an assumed body, or a contract for either
target method:

| Dependency | Selected declaration and scope |
|---|---|
| Slice sequence view | `toolchain/upstream/source/vstd/slice.rs:13-17`: `View for [T]` is `Seq<T>`. The unchanged candidates compare the full element value and full remainder sequence. |
| Length | The same file at 71-87 supplies `spec_slice_len`, `axiom_spec_len` and the existing `len` declaration. This relates the machine element count to the sequence length, including its machine bound; it does not prove Rust's metadata implementation. |
| Shared element indexing | The same file at 186-193 supplies `spec_slice_index` and `axiom_spec_slice_index`, after the source proof discharges its in-range obligation. The `slice_index_get` helper at 59-69 describes the same value relation but need not be called by built-in indexing. The actual generated queries determine which lowering is used. |
| Shared splitting | `toolchain/upstream/source/vstd/std_specs/slice.rs:516-523` is the existing `assume_specification<T>[<[T]>::split_at]`: requires `0 <= mid <= slice.len()`, ensures `ret.0@ == slice@[..mid]` and `ret.1@ == slice@[mid..]`, and `no_unwind`. The two source proofs must establish this precondition themselves. This trusted declaration supplies full ordered subranges, not pointer-origin equality and not a source proof of `split_at`. |

No candidate or legal input domain changes. In particular, the existing Some
clauses retain nonemptiness, the endpoint value and the entire ordered
remainder. The nonempty clause is not implied by equalities to an out-of-range
spec index or subrange; those expressions do not establish their own bounds.
The element clause cannot determine an arbitrary remainder, nor can the
remainder clause determine the excluded element. The project-only temporary
redundancy criterion remains readable in
[`review-criteria-temporary.txt`](../review-criteria-temporary.txt); Reviewer
must recheck this reasoning rather than inherit the endpoint judgment.

The required next independent decision is limited to these two exact
conversions and their full source correspondence. Use `run_review_command`
and `get_review_command`, write all outputs to `{scratch}`, and set
`RUSTUP_HOME=/home/chentianyu/.rustup` when needed. A successful isolated
experiment does not authorize adoption. After explicit permission, the current
source proofs, aggregate, discovery and the actual two analyses/reexecutions,
adopted native comparisons, exact binding and real export selection still
need to run, followed by final independent review. The analysis declarations
remain at `proofs/completeness/slice/inputs/split_first.rs:13` and
`proofs/completeness/slice/inputs/split_last.rs:13`; current discovery must
confirm those selectors. No endpoint, ASCII, Default or singleton review is
reopened, and no metadata or singleton source gap is closed by this proposal.

### Isolated split results, without adoption

Both isolated proposals compiled and verified on the selected unmodified
Verus. Each returned exit 0 with **3 verified, 0 errors**: one proposed split
function and the two unchanged imported lemmas `contracts::scalar_domain`
and `contracts::empty_results`. Neither result is a proof of the current
pattern-based file, and neither proves `split_at`.

```sh
RUSTUP_HOME=/home/chentianyu/.rustup \
  toolchain/verus-x86-linux/verus proofs/correctness/slice/proposals/split_first.rs \
  --crate-type lib --crate-name slice_split_first_proposal --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/splits-proposal/correctness/split_first/queries \
  -o target/splits-proposal/libslice_split_first_proposal.rlib
RUSTUP_HOME=/home/chentianyu/.rustup \
  toolchain/verus-x86-linux/verus proofs/correctness/slice/proposals/split_last.rs \
  --crate-type lib --crate-name slice_split_last_proposal --compile --no-cheating \
  --num-threads 1 --log-all \
  --log-dir logs/splits-proposal/correctness/split_last/queries \
  -o target/splits-proposal/libslice_split_last_proposal.rlib
```

The actual outputs are
[`logs/splits-proposal/correctness/split_first/verus.log`](../logs/splits-proposal/correctness/split_first/verus.log)
and
[`logs/splits-proposal/correctness/split_last/verus.log`](../logs/splits-proposal/correctness/split_last/verus.log).
Both compiled libraries are present and nonempty. In each directory,
`queries/root-final.air:4096` begins the one actual split function obligation;
`contracts-final.air` separately contains the two imported lemma obligations.
The first target checks index zero, the `split_at(1)` precondition, selection
of tuple component 1, and `split_first_post`. The last checks machine
subtraction, the resulting index, the `split_at(i)` precondition, component 0,
and `split_last_post`. The lowered index uses `spec_slice_index`, not a call
to `slice_index_get` or the target API. No executable proof-body annotation,
extra precondition, axiom, external body or target-contract assumption was
needed.

The native comparison was actually executed as:

```sh
RUSTUP_HOME=/home/chentianyu/.rustup \
  /home/chentianyu/Argus/.venv/bin/python -B scripts/check_native.py \
  --group splits-proposal --output-root logs/splits-proposal/pre-adoption
```

Rust **1.96.0**, without bootstrap and with overflow checks enabled, compiled
the generic original/proposed functions and their const invocations. The
binary executed **15 tests** comparing the authority patterns, exact isolated
proposals and real public methods. All **120 compiler rejection probes**
returned the expected single relevant diagnostic, separately checking both
tuple components' mutability and lifetime escape, including singleton empty
remainders, and rejecting wrong receivers, arguments and result shapes.
The run linked and executed successfully; this is an engineering result,
not a claim that Reviewer's environment can link or has replayed it.

The source mappings, current and isolated proof text, canonical docs, relevant
`split_at` dependency spans, generated Rust inputs, generic MIR, version,
commands, compiler diagnostics and results are retained under
[`logs/splits-proposal/pre-adoption/logs/splits-proposal/native/`](../logs/splits-proposal/pre-adoption/logs/splits-proposal/native/).
`commands.json` contains 123 command exits: the version, compile and behavior
commands succeeded; the 120 diagnostic-checked invalid programs were rejected.
`results.json` identifies the scope as unadopted and records every probe's
input and diagnostic. The retained source spans and behavior input were
compared with the current files after execution and still match exactly.
Temporary executables and rejection inputs were removed, not the retained
sources or logs.

The actual `split_proposal_behavior.mir` supports these correspondences:

| Generic function; runtime and CTFE starting lines | Actual branch, projections and result |
|---|---|
| `original::split_first`; 4, 42 | `n >= 1`; shared `[0 of 1]` and `[1:]` projections on the same `_1`; returns element then full tail |
| `original::split_last`; 97, 135 | `n >= 1`; shared `[:-1]` and `[-1 of 1]` projections on `_1`; returns last element before the initial slice |
| `proposal::split_first`; 190, 239 | Empty branch returns `None`; checks index zero, borrows `_1[0]`, calls inherent `split_at` on that input at 1 and selects component 1 |
| `proposal::split_last`; 321, 381 | Empty branch returns `None`; checked subtraction produces `i`, an index check precedes `_1[i]`, and inherent `split_at` on the same input at `i` supplies component 0 |

Runtime and CTFE MIR agree on the origins, range choices and tuple order.
MIR call successors include unwind paths; the complete legal-length argument
and actual Verus bounds obligations establish why the introduced checks cannot
fail on a legal input. The native `usize::MAX` unit-slice test is an additional
extreme example, not an enumeration proof. Zero-sized position correspondence
continues to depend on the generic projections and delegated range source,
not identical addresses.

The new runner reuses the existing output-root, diagnostic and command/MIR
execution structure. It rejects changes to either original body, exact
proposal, const/shared/generic signature, contract import or ensures clause.
It does not widen the current-source binding exception: only the previously
approved endpoint bodies are permitted by that existing test. Its new tests
also honor `TMPDIR`, so independent runs can keep temporary files in scratch.
The following affected Python execution passed **30 tests**, including the
existing endpoint runner tests because their command-recording implementation
is shared, and the four exact observer binding tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tests \
  TMPDIR="$PWD/logs/splits-proposal/python-tmp" \
  /home/chentianyu/Argus/.venv/bin/python -B -m unittest -v \
  test_native_split_proposals test_native_endpoints test_contract_bindings.ContractBindings
```

Its output is
[`logs/splits-proposal/python-unit.log`](../logs/splits-proposal/python-unit.log).
The test imports compiled the affected Python modules; no unrelated native
group or existing API proof was rerun. The unchanged aggregate, specdet
analyses, completeness files, exporter and coverage were not rerun or updated
at this pre-adoption stage.

Independent permission for the two split conversions is still required.
Reviewer can replay the commands above through the existing restricted
interface with all `--log-dir`, `-o`, `--output-root` and `TMPDIR` locations
under `{scratch}`. The native runner needs a linker; a link failure must be
recorded as an unexecuted runtime comparison, not a pass. Generic metadata/MIR
compilation and expected type/lifetime rejections remain distinct from runtime
execution. After permission, fresh checks must use the current adopted source
files, not these isolated libraries, and complete both actual checker runs
and export integration before the final independent review.

For Python-only replay, the new split suite can run directly with
`PYTHONPATH=.:tests`, `TMPDIR={scratch}/tmp` and
`python -B -m unittest -v test_native_split_proposals` after creating that
scratch directory. The existing endpoint mock suite instead creates fixtures
under its imported project root. Replaying that suite in the restricted
environment therefore needs byte-identical scratch copies of its input
files; do not write fixtures into the reviewed project or relax the
read-only command policy. This is a test-output constraint, not permission
to reopen or change the endpoint source proofs.

### Independent split permission before adoption

The independent review in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/1afe25aa17b0/round-0001.json`
explicitly authorizes the two exact split conversions above. This permission
is recorded before changing either current source-proof file. It preserves
`pub const fn`, shared input, `Option<(&T, &[T])>`, both input-bound output
lifetimes and unconstrained `T`. It does not authorize candidate, canonical
Rust, vstd or verifier changes, nor claim const compatibility with Rust
1.56-1.70. The overall API repair is not yet complete.

Reviewer directly checked the two source/doc spans and the full
`split_at -> split_at_checked -> split_at_unchecked` trace, the retained
versioned Reference and MIR definitions, and actual runtime/CTFE MIR. The
accepted correspondence covers element zero with `[1, n)`, element `n - 1`
with `[0, n - 1)`, element-first tuple order, the distinct singleton empty
remainder origins, legal zero-sized slices and all machine lengths.
Nonemptiness establishes the subtraction, indexing and split bounds; the
empty branch evaluates none of those operations. Shared borrowing neither
moves nor drops elements and calls no user code. The trusted dependencies
remain the existing view, length, indexing and `split_at` contracts, not a
source proof of `split_at`.

Through the restricted read-only command route, Reviewer independently ran
both isolated files with
`--crate-type lib --compile --no-cheating --num-threads 1`. Each succeeded
with `3 verified, 0 errors`, consisting of the one split target and
`scalar_domain` and `empty_results`. The independently inspected queries
contain both index/split preconditions and the last-element machine
subtraction, followed by the unchanged candidate postcondition.

Independent Rust 1.96 object/MIR compilation without bootstrap and with
overflow checks succeeded, covering exact generics and real const calls.
All 120 expected type, shape, mutability and lifetime rejection probes
matched their diagnostics. Thirty affected Python tests and Python
compilation also passed. The endpoint mock tests covered shared runner code
only; endpoint API verification was not reopened.

The independent native execution did **not** pass: the actual runner stopped
at `linker cc not found`, so the 15 runtime tests were not independently
executed. Reviewer checked the engineering runtime results and exact retained
inputs but did not relabel them independent. The restricted environment also
lacked the engineering Argus Python mount; standard-library scripts used the
already authorized Miniconda Python. An initial object compilation wrote a
temporary file to the read-only working directory and failed; compilation
from the review scratch directory then succeeded. Those failures remain
recorded in the independent review; object compilation is not linking or
runtime execution. Native independent replay still needs a usable linker
through the existing authorized environment path, not a changed
implementation or a weakened test.

The independent temporary redundancy review found no removable clause.
Neither out-of-domain spec indexing nor subrange equality implies
nonemptiness; the excluded element value and complete remainder also cannot
determine one another. Both unchanged candidates therefore remain intact.

The next engineering work is now adoption, not another wait for permission:
compile and verify both current source files, compile the aggregate using
its existing declaration mode, run discovery and each actual analyze/reexecute,
then compare authority/current/public native inputs and integrate exact
binding and source-only export selection. Final independent review remains
necessary. The pre-adoption originals and unchanged baseline files have been
preserved byte-for-byte under `logs/splits/adoption-before/`.

### Adopted split source results

After recording the independent permission, the two current files received
only the executable differences shown above. Exact original copies are in
`logs/splits/adoption-before/proofs/correctness/slice/`; the isolated proposals
and all original failure logs remain in their original locations. Neither
candidate, public binding, analysis declaration, configuration, canonical
Rust nor selected verifier/vstd was changed.

`logs/splits/run_checks.py` reuses the existing command-recording and proof
execution functions from `logs/endpoints/run_checks.py` without changing that
historical runner. It writes only new split results. The actual current
compilations, their complete command arrays, exits, source/contract snapshots,
SMT transcripts and nonempty libraries are under:

| Input | Directory | Actual result |
|---|---|---|
| `proofs/correctness/slice/split_first.rs` | `logs/splits/correctness/split_first/` | Exit 0; 3 verified, 0 errors: one split target and two imported consistency lemmas |
| `proofs/correctness/slice/split_last.rs` | `logs/splits/correctness/split_last/` | Exit 0; 3 verified, 0 errors: one split target and two imported consistency lemmas |
| `specs/mod.rs` | `logs/splits/correctness/aggregate_current/` | Exit 0; 2 verified, 0 errors: the aggregate's consistency lemmas, not additional API proofs |

Each actual split command uses
`--crate-type lib --compile --no-cheating --num-threads 1 --log-all`;
the aggregate uses its existing `--compile --num-threads 1` declaration
workflow, without `--no-cheating`. The actual target queries begin at
`split_first/queries/root-final.air:4092` and
`split_last/queries/root-final.air:4093`. Both check indexing and the existing
`split_at` precondition; the last also checks machine subtraction before
indexing. Each concludes its unchanged candidate. The imported
`scalar_domain` and `empty_results` queries are separate.

Actual discovery is retained in
`logs/splits/completeness/discovery/discover.json`. It lists an original
function at line 6 and a contract declaration at line 13 for each split.
The initial orchestration check incorrectly required uniqueness by file/name
alone and stopped before analysis. Its diagnostic remains in
`discovery/selection-failure.txt`. Filtering by the actual
`contract_declaration` kind resolved that distinction without rerunning
discovery or changing inputs.

The subsequent four actual checker commands succeeded:

| Selected declaration | Analyze and reexecution |
|---|---|
| `proofs/completeness/slice/inputs/split_first.rs:split_first@13` | `logs/splits/completeness/split_first/{analyze,replay}.json` |
| `proofs/completeness/slice/inputs/split_last.rs:split_last@13` | `logs/splits/completeness/split_last/{analyze,replay}.json` |

Each exited zero, selected exactly its one intended declaration, verified
one native goal and reported original-query UNSAT. Reexecution uses
`replay --run ANALYZED_DIRECTORY --reexecute` without a `--config` override.
The actual effective selectors, parent-run relations, frozen inputs,
dependencies, generated native worktrees and commands were checked; each
replay's generated comparison and original query match its analyzed run.
The comparison is:

```rust
((r1 is Some) == (r2 is Some))
    && ((r1 is Some) ==>
        ((r1->Some_0.0 == r2->Some_0.0) && (r1->Some_0.1 =~= r2->Some_0.1)))
```

Thus it observes the Option variant, element in tuple position 0 and
complete ordered slice in position 1. Existing slice extensional equality
relates the latter to equal lengths and every corresponding element
(`vstd/slice.rs:170-174`); it is not address equality or a length-only
comparison. Both candidate premises take the same unrestricted input.

There are **eleven**, not seven, search guards for these tuple-returning
declarations: two input-length guards, two Option-variant guards per result,
two remainder-length guards per result, and `g_neq_tuple`. Every guard is
disabled in each actual original query. The first exporter adaptation
correctly refused the unfamiliar generated harness because its template still
described the seven endpoint guards. That failed export test run remains in
`.argus_subagents/slice-splits-adopted-export-tests_logs/` and
`logs/splits/export-tests/{endpoints,splits}/`. The exporter now checks the
exact eleven-guard split form, including all four remainder-length guards,
without weakening the input or the comparison. No proof was rerun to repair
this output-shape validation mistake.

The sole current native route is now:

```sh
RUSTUP_HOME=/home/chentianyu/.rustup \
  /home/chentianyu/Argus/.venv/bin/python -B scripts/check_native.py \
  --group splits --output-root logs/splits/adopted-native-root
```

It extracts the **current adopted** split files, not the isolated proposals.
Rust 1.96 compilation, linking and all 15 runtime tests succeeded; all 120
invalid programs produced the expected diagnostic. All 123 command exits,
authority/current mappings, retained inputs, runtime/CTFE MIR and diagnostics
are in
`logs/splits/adopted-native-root/logs/splits/native/`.
The exact source-binding test permits only the new two approved differences
in addition to the prior two endpoint differences, and still compares all
six analysis declarations with the original source. The old proposal route
is rejected by CLI parsing, rather than left alongside the adopted route.
The original test and runner inputs are preserved in
`logs/splits/adoption-before/` and `logs/splits-proposal/`.

The adopted runner and exact binding tests passed 32 tests in
`logs/splits/python-bindings.log`. After the exporter learned the actual
eleven-guard shape, its 25 tests passed in
`logs/splits/python-export-eleven-guards.log`, exercising **119 endpoint and
135 split real CLI cases** recorded under
`logs/splits/export-tests/eleven-guards/`. The endpoint cases test the shared
export implementation, not a rerun or reopening of endpoint API proofs.
The split cases reject omitted/reordered tuple components, length-only
remainder comparisons, enabled individual guards, failed/zero/partial source
proofs, stale input/dependencies, wrong targets and wrong reexecutions.
Every rejected invocation preserves all outputs. Python compilation occurred
through these actual module imports and CLI executions; the run scripts
were also executed with the confirmed Argus Python.

The real `scripts/export_completeness.py --splits` invocation exited zero.
`logs/splits/export-current/` retains its command and result comparison:
exactly four source-result cells changed in each selected row, **329
unselected rows are byte-identical**, all **14 completeness files** and all
**five historical failure logs** are byte-identical. All old completeness
cells remain unchanged; the new analyze/reexecute records are additional
evidence. Candidates, analysis inputs and configuration also match the
pre-adoption copies. The updated coverage assertion passed separately in
`logs/splits/python-post-export-coverage.log`. The default exporter now also
uses the checked split source records rather than restoring their old
frontend failures.

These are engineering results. Final independent current-source proof,
checker and integration review remains required, and the separately recorded
native linker limitation must not be represented as independent runtime
success. Metadata and both singleton source gaps remain open; no
`split_at` implementation proof or module-wide completion is claimed.

### A usable native linker within the existing read-only scope

The independent `cc` failure was an actual missing dependency in the configured
`ubuntu:24.04` image. The existing approved mounts include the project,
Rustup and Miniconda `bin`/`lib`, but neither a host system compiler tree nor
the Argus Python checkout. No image, mount permission or runtime implementation
was changed to address it.

After that missing-tool failure, five pinned packages from the configured
Ubuntu archive were downloaded and extracted only beneath
`toolchain/review-native/sysroot/`: `gcc-13-x86-64-linux-gnu` and
`libgcc-13-dev` at `13.3.0-6ubuntu2~24.04.1`, `libc6` and `libc6-dev` at
`2.39-0ubuntu8.9`, and `libgcc-s1` at `14.2.0-4ubuntu2~24.04.1`.
These match the installed host package versions. There was no system
installation, package-index update or global environment change.
Package archives remain in `toolchain/review-native/packages/`, with their
actual package-manager download record in
`.argus_subagents/slice-splits-native-linker-packages_logs/` and extraction
commands/metadata in `logs/splits/native-linker-setup/`.

`toolchain/review-native/bin/cc` is a small launcher for that packaged GCC
driver, passing its local sysroot and helper/library locations and forwarding
the original linker arguments. It has no retry, alternate compiler or
test-success substitution. Rust 1.96, its flags, the native runner, the source
inputs and the 15 tests/120 rejection expectations are unchanged.

The Engineer then executed the actual `--group splits` runner through the
unchanged restricted-command implementation in `/home/chentianyu/Argus`,
using exactly the configured image/read roots and scratch-only outputs.
The mounted Miniconda Python ran the standard-library native script; the
project-local compiler directory was first on `PATH`. This invocation really
linked and executed all **15 runtime tests** and checked all **120 expected
compiler rejections**, with exit 0 and successful container removal. The
retained source spans and behavior input still match the current files.

This is an **engineering restricted execution**, not an independent review.
Its exact command and full result are in
`logs/splits/native-readonly-engineering/result.json`; that record links the
runtime's original command receipt and all scratch-native outputs.
`runtime-review-readiness.json` now includes the exact argv for Reviewer to
use through `run_review_command` / `get_review_command`. It retains the
explicit false API/module permission flag and the old failure records.
The native linker obstacle has an exercised project-local solution; Reviewer
must still run it independently during final review. Neither a probe nor this
engineering execution is relabeled an independent API result.
