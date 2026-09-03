---
title: Target 082 key-sort operational boundary and v8 preservation
description: Source-backed key extraction, Ord, temporary destruction, callback destruction, unstable-sort composition, and additive preservation for sort_unstable_by_key.
---

# Target 082 key-sort operational boundary

The source transition for `core::slice::sort_unstable_by_key` evaluates
`f(left)` before `f(right)`, evaluates `K::lt` only after both owned keys
exist, destroys the right key before the left key, and destroys the owned
`F` after the private sort returns or while its panic unwinds. A panic from
temporary destruction during an existing unwind aborts immediately. A panic
from `F` destruction during an existing unwind likewise aborts. Ordinary
callback panic reaches the accepted private-sort unwind guards before `F`
is destroyed.

Each owned key has a source-derived identity containing its comparator
invocation, left/right slot, creation state, source element identity, and
abstract key identity. Equal abstract keys therefore remain distinct owned
values with independently observable destruction. Callback scalar state and
the complete externally observable element-interior state transition at key
extraction, `Ord::lt`, key destruction, and `F` destruction, including before
panic becomes observable.

The admitted boundary contains only total key, `Ord::lt`, key-`Drop`, and
`F`-`Drop` transition functions and the state-independent contract key/order
projection. It excludes realized comparison schedules, temporary lifetimes,
pivots, partitions, swaps, writes, outputs, final state, and traces. Those
observations are derived from the Rust adapter and the independently accepted
target-080 private unstable-sort transition. The boundary is strictly
narrower than the public target.

The additive operational theorem uses exact terminal status, unit return,
final sequence, callback state, and complete observable element state.
Separately, the certified public-contract result remains exact-output
`conditional-incomplete` because equal-key identities may reorder, and
reviewed-equivalence `conditional-complete` only under the documented
state-independent total-order projection.

# Abort-preserving private-sort composition

The target-082-specific SMT projection transports the adapter's NORMAL,
PANIC, or ABORT status in the accepted target-080 transition's integer
callback-state carrier. The target-080 transition itself is unchanged.
Target 082 decodes the carrier into the original callback state and terminal
status before public cleanup, while the decoded callback state selects the
source-backed element-interior observation.

An adapter ABORT therefore reaches the public result as status 2 with the
exact private abort-prefix sequence, callback state, and observable interior
state, and skips `F` destruction. Ordinary adapter panic still invokes `F`
destruction while unwinding, and normal completion invokes ordinary `F`
destruction. Independent solver regressions retain a satisfiable valid ABORT
branch and make the former ABORT-to-PANIC plus `F`-drop outcome unsatisfiable.

# Preservation successor

`path_policy_v8` byte-binds the unchanged accepted `path_policy_v7`. Any
v6-registered live file changed to integrate target 082 is resolved only by
an explicit logical-record-to-project-local-archive mapping. Unmapped,
duplicate, traversing, missing, or altered archive content fails closed.
The certified interactive Argus capture is likewise retained only through an
explicit historical mapping, while fresh authority generation records the
noninteractive `python -m argus_skill --version` command.
Target 082 remains review-pending; an independent decision belongs only in
the separate `path_policy_v9` lane.
