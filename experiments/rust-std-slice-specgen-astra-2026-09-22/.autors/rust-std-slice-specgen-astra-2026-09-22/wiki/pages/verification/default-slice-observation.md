---
title: Default slice observation
description: The mutable Default analysis preserves the empty-slice predicate through full-view equality, without changing the actual mutable return type.
---

# Default slice observation

The shared and mutable slice Default contracts use
`default_post(result)`, defined as `result@ =~= Seq::<T>::empty()` in
[specs/slice/default_post.rs](../../../../../specs/slice/default_post.rs).
It describes the full sequence, not pointer identity. The source proof copies
retain the original Rust 1.96 bodies `&[]` and `&mut []`, with no arguments or
additional element bounds.

The mutable analysis input reborrows a mutable slice as a shared slice:

```rust
fn observe<'a, T>(value: &'a mut [T]) -> (result: &'a [T])
    ensures
        result@ == old(value)@,
{
    &*value
}
```

Full-view equality entails
`default_post(result) <==> default_post(old(value))` by substituting equal
sequences in the predicate definition. Keeping that equivalence as a second
postcondition adds no semantic information. The relation concerns the
observer's initial value and its returned view; it does not remove or imply a
separate `final` writeback condition for other APIs.

The executable reborrow, constructor composition, and comparison between
returned slice values and complete sequence views are checked together in
[the mutable analysis input](../../../../../proofs/completeness/slice/inputs/default_mut.rs).
The reduced input compiles with `--no-cheating` and verifies four functions;
the command and output are retained in
[logs/defaults-redundancy/adapter](../../../../../logs/defaults-redundancy/adapter/).

This is an analysis adaptation, not a change to the public API's
`&'a mut [T]` return type. Direct mutable-reference return extraction remains
unsupported by the selected specdet version, as documented in
[issues/S-MUT-RETURN.md](../../../../../issues/S-MUT-RETURN.md).
The adapter proof and the generated determinism check answer different
questions and must both hold for the current candidate.

## Checker target identity

For this project's mutable Default configuration and specdet 0.3.0, target
discovery reports a project-relative file, function name and declaration line.
The corresponding project-relative selector is recognized; an absolute-path
selector with the same name and line is not. This is a discovery constraint,
not a failure to prove the contract.

The compared source snapshots are byte-for-byte identical in the input,
source proof, predicate and configuration. The effective configurations differ
only in their selectors. The comparison is recorded in
[selector-comparison.log](../../../../../logs/defaults-redundancy/selector-comparison.log);
the [discovery result](../../../../../logs/defaults-redundancy/completeness/default_mut/discover.json)
provides the recognized identity.
The [unrecognized selection](../../../../../logs/defaults-redundancy/completeness/default_mut/analyze.json)
contains no proof results, whereas the
[recognized selection](../../../../../logs/defaults-redundancy/completeness/default_mut/selected/analyze.json)
and its
[reexecution](../../../../../logs/defaults-redundancy/completeness/default_mut/selected/replay.json)
each check one determinism goal with an UNSAT original query.
