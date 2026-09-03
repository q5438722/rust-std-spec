# Independent Reviewer request

**Status:** pending independent review

Review only input orders 008 `core::slice::align_to` and 009
`core::slice::align_to_mut` against the independently accepted 60-target
baseline. Do not invoke a stage-transition writer. Record **ACCEPT** or
actionable findings.

- Confirm active contract SHAs
  `ecdec7dc102f8a00f610ae369191cf306fabe2a435b651d7cc69d2775d75e321`
  and
  `d3f3080fe88dd4be74e095f3d06df2b686c52dd000e8bba962feaa71695cd330`.
  Inspect both literal declarations, generated align vocabulary, canonical
  Slice source/docs, canonical `ptr::align_offset` source/docs, both frozen
  harnesses and all eight frozen manifests, and all 20 trust records by
  readable content.
- Confirm `TS-008-D004`/`TS-008-E005`/`TS-008-E006` and
  `TS-009-D004`/`TS-009-E003`/`TS-009-E004` remain excluded and are replaced,
  not relabeled. Reject the retained null-provenance length-as-address model,
  opaque `slice_align_to_domain`/`slice_aligned_middle`, complete branch
  bridges, or any returned/final observation in `Boundary_T`.
- Confirm the source transitions define Slice pointer extraction,
  element-stride `align_offset` with wrapping addresses and `usize::MAX`,
  ZST and `offset > len` branches, gcd/ts/us arithmetic, exact split ranges,
  pointer casts/addition, raw-slice construction, byte-derived typed middle
  values, returned reference identity/provenance, disjoint mutable borrows,
  and relational final T/U frames.
- Confirm every theorem has one shared valid `x` and one shared `b`.
  `Boundary_T` may contain only initialized input bytes, input Slice
  representation/allocation/provenance, T/U layout and platform limits,
  transmute validity, root-borrow/alias/liveness, and outside frame. It must
  exclude offset/branch/gcd answers, partitions, decoded middle values, final
  bytes/views, target truth, and traces.
- Inspect the ten source cases per target: empty, source and destination ZST,
  aligned byte reinterpretation, finite misalignment, offset equal to length,
  offset greater than length, `usize::MAX`, nontrivial size gcd, and nondefault
  allocation/provenance. Inspect all 43 invalid-domain, wrong-transition,
  wrong-field, final-frame, and answer-laundering probes.
- Replay target 008 exact-output and full-state and target 009 exact-output as
  clean UNSAT. Replay target 009 full state as SAT and its concrete
  fixed-input/fixed-boundary witness as SAT; the witness must vary one legal
  mutable byte while re-deriving all final T/U views and preserving backing
  identity and outside frame.
- Freshly compile the Python, run focused and complete tests, type-check and
  verify both trusted-free target-local Verus models with six verified items
  and zero errors each, directly replay all Z3 evidence, run the bounded
  runner, integrated validator, and complete acceptance driver.
- Confirm all 60 certified target-evidence trees and all 320 frozen files are
  byte-identical, only rows 008/009 result cells changed, and the ledger has
  exactly 62 classified and zero `not-run`. Target 008 must be
  `conditional-complete` for both projections; target 009 must be exact-output
  `conditional-complete` and full-state `conditional-incomplete`. Use
  `tools/run_align_to_pair.py`.

The preservation baseline is accepted in
`REVIEW_ACCEPTANCE_20260901T135004Z.md`.
