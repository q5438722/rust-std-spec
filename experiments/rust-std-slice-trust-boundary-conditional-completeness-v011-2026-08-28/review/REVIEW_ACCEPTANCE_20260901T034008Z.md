# Independent Reviewer decision: mutable edge extraction

**VERDICT: ACCEPT**

**Timestamp:** 2026-09-01T03:40:08Z

This decision covers only input orders 091
`core::slice::split_first_mut`, 097 `core::slice::split_last_mut`, 101
`core::slice::split_off_first_mut`, and 103
`core::slice::split_off_last_mut`. It does not authorize a Manager stage
transition.

## Semantic review

The four active declarations, canonical source items and public docs, shared
split-off vocabulary, frozen harnesses, source-body/transformation/dependency
manifests, and all eight trust records are bound by direct content. The
catalog's public-doc text is the cited Rust source text with rustdoc comment
markers removed.

The direct models follow the canonical empty/nonempty first-tail and
init-last pattern splits. The wrapper models compose replacement with the
source-created empty literal, splitting of the held original slice, receiver
reassignment on the nonempty path, and return in source order. The empty path
retains the replacement literal identity; the nonempty path derives the
receiver from the source remainder.

`Boundary_T` contains only initial address, allocation, provenance,
mutable-borrow identity, element layout, and the wrapper-only pre-result
empty-literal identity. It excludes result tags, selected indices and ranges,
returned references, final receiver/storage, answer encodings, and traces.
The obligations use one shared valid input and one shared boundary and compare
every principal return/reference identity and immediate final-state
observation exactly. Range disjointness remains explicit when ZST references
have equal addresses.

## Independent execution

- Python compilation and 15 focused mutable-edge tests passed.
- All four generated Verus files type-checked and verified with one verified
  proof and zero errors each; none contains `external_body`.
- A 62-case source-derived probe passed concrete and negative checks for tags,
  first/last indices and ranges, tuple order, reference identity, final-frame
  reconstruction, empty replacement identity, singleton and longer inputs,
  ZST aliasing, invalid lengths/layouts, and mismatched boundaries.
- The complete acceptance driver passed all 33 commands. Its full repository
  test run passed 323 tests, and the target runner replayed eight clean UNSAT
  theorem obligations and 24 SAT source instances.
- The ledger contains 38 classified rows and 24 `not-run` rows. A direct
  pre/post semantic-content comparison covered 3,267 evidence, frozen-input,
  and crosswalk files without relying on integrity-only fields and found no
  changes.

