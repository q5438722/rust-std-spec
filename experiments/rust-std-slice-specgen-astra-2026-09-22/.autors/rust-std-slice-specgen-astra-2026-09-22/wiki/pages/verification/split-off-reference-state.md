---
title: Shared slice reference consumption
description: Call-return reference-slot state, the independent inner lifetime, direct full-state comparisons and Rust 1.96 const restrictions.
---

# Shared slice reference consumption

Rust 1.96 `slice/mod.rs:4993-5015,5043-5065` defines `split_off_first`
and `split_off_last` in the unconstrained `impl<T> [T]`. Their receiver is
`self: &mut &'a Self` and their return is `Option<&'a T>`. Runtime use is
stable since 1.87.0. The `pub const fn` spelling does not make public const
calls stable: both carry `rustc_const_unstable` for
`const_split_off_first_last`.

Each body destructures a shared split, returns `None` immediately on empty
input, assigns the remainder to `*self`, and returns the endpoint. It changes
the outer reference slot, not any underlying element. For nonempty input
of length `n`, the first method returns element zero and retains `[1,n)`;
the last returns element `n-1` and retains `[0,n-1)`. The empty branch leaves
the slot unchanged. A singleton first remainder begins one past the element;
a singleton last remainder begins at its start. Equal zero-sized addresses
do not establish equal element positions.

The shared dependencies and their source/provenance boundaries are described
in [Split remainder source dependencies](split-source-dependencies.md).
The versioned method lookup rules are retained in
[`.argus/sources/641618b79489a25d70283127.txt:32-42`](../../../../../.argus/sources/641618b79489a25d70283127.txt).
For the concrete nested slice receiver, auto-dereferencing selects the inherent
shared split. The assignment rules at
[`.argus/sources/df6d9bcc218b2f61bf5e45cc.txt:770-796`](../../../../../.argus/sources/df6d9bcc218b2f61bf5e45cc.txt)
evaluate the remainder before writing the reference slot. No owned `T`,
extra element destruction or mutable element reference is introduced.

## The slot is observed when this call returns

The pure predicates are in
[`specs/slice/split_off_post.rs`](../../../../../specs/slice/split_off_post.rs).
Their input is only the original `Seq<T>`; the full observation is
`(Option<T>, Seq<T>)`, containing the returned logical element value and the
entire ordered remaining slice. They have no input precondition, trait bound
or caller-final environment.

The public declarations use `(*old(slice))@` for the original sequence and
`(*final(slice))@` for the updated slot. Here `final` applies to the outer
mutable reference, not to the shared element or underlying owner. No borrow
of that slot is returned, so the slot's call borrow can end immediately.
The caller may retain the result, consume again, reassign the slot to an
unrelated slice, or let the local slot cease to exist. The returned reference
still cannot outlive its underlying owner.

This use of `old` and `final` follows the selected verifier's
[`migration-mut-ref.md:78-89`](../../../../../toolchain/upstream/source/docs/migration-mut-ref.md)
and
[`mutable-references.md:40-59`](../../../../../toolchain/upstream/source/docs/guide/src/mutable-references.md).
The compiled public clients in
[`tests/split_off_contract_clients.rs`](../../../../../tests/split_off_contract_clients.rs)
exercise both repeated calls and subsequent arbitrary slot reassignment.
They are clients of the declarations, not implementation proofs.

The six lemmas in
[`split_off_state.rs`](../../../../../proofs/completeness/slice/split_off_state.rs)
establish candidate correspondence, an observation for every initial
sequence, ordered reconstruction, and equivalence of the complete value
comparison. Empty input needs no inhabitant of `T`. Full sequence equality
already entails remaining length and all positions; those are not extra
candidate clauses. The nonempty input condition is still needed because a
spec `subrange` expression's recommended domain is not a premise.

## Direct checker extraction retains the slot update

For these nested shared-reference receivers, the selected specdet 0.3.0
already generates separate `pre_slice`, `post1_slice`, and `post2_slice`
parameters. Its direct comparison is:

```rust
(((r1 is Some) == (r2 is Some))
    && ((r1 is Some) ==> (r1->Some_0 == r2->Some_0)))
    && (post1_slice =~= post2_slice)
```

Both candidate instances share only the pre-state. Their post-state slices
are independent observations, not a single supplied answer. The comparison
includes the Option variant, complete logical element value and every
remaining element. `complete_comparison` proves the corresponding
`(Option<T>, Seq<T>)` value equality. No additional adapter or arbitrary
caller-final state is necessary for this shape.

The current direct selectors are
`proofs/completeness/slice/inputs/split_off_first.rs:split_off_first@15`
and the analogous `split_off_last` selector at line 15. Line 6 is the
unannotated source copy, not the declaration to analyze. The actual generated
comparisons and analyzed-directory reexecutions are retained in
[`logs/split-off-endpoints/direct/`](../../../../../logs/split-off-endpoints/direct/).
Each original query disables all eleven guards: two pre-slice length
guards, four Option guards, four independent post-slice length guards and
the output-inequality guard. This is a different set from the eleven
[shared split tuple guards](split-source-dependencies.md#complete-tuple-observations-introduce-four-additional-search-guards).

## The missing dependency binding is separate from the candidate

The selected vstd has neither split-off binding. Both declarations are
isolated in [`split_off.rs`](../../../../../specs/slice/split_off.rs), outside
the source-proof imports. Its existing `split_first` declaration at
`std_specs/slice.rs:547-552` supports the original first delegation.
There is no corresponding external `split_last` binding.

A proved local shared `split_last` does not automatically specify that
external method. The contract-free reproduction and the separate, narrowly
scoped call-rebinding request are in
[V-ASCII-CALL-BINDING](../../../../../issues/V-ASCII-CALL-BINDING.md#shared-split-off-dependency-a-separate-unapproved-call-rebinding).
Earlier ASCII or pattern-conversion permissions do not grant permission for
this distinct executable change. Neither the complete direct checker
comparison nor native examples resolve that source-proof boundary.
