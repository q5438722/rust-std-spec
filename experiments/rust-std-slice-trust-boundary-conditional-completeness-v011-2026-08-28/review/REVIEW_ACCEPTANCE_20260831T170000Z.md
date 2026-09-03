# Independent Reviewer decision: pointer-cast cluster

**VERDICT: ACCEPT**

This decision covers input orders 019 `core::slice::as_mut_ptr`, 021
`core::slice::as_ptr`, and 020 `core::slice::as_mut_ptr_range`, in that
dependency order. The two blockers in
`REVIEW_FINDINGS_20260831T161008Z.md` are resolved.

## Boundary authority and replacement findings

Both generated obligations for each target use metadata schema v3. Direct
inspection of the generated metadata and boundary manifests established:

| Target | Admitted / excluded / context-only partition | Boundary backing | Exact replacement coverage |
|---|---|---|---|
| 019 | `∅` / `TS-019-D001` / `TS-019-D002` | All 11 fields use `SRC-019-CANONICAL-SLICE-TO-MUT-PTR`; no retained trust-site ID is used | `TS-019-D001` |
| 021 | `∅` / `TS-021-D001` / `TS-021-D002` | All 9 fields use `SRC-021-CANONICAL-SLICE-TO-CONST-PTR`; no retained trust-site ID is used | `TS-021-D001` |
| 020 | `TS-020-D002` / `TS-020-D003, TS-020-D004, TS-020-E001` / `TS-020-D001, TS-020-C001, TS-020-C002, TS-020-C003` | All 11 fields use only `TS-020-D002` | `TS-020-D003, TS-020-D004, TS-020-E001` |

Thus the replacement records globally cover exactly
`TS-019-D001`, `TS-021-D001`, `TS-020-D003`, `TS-020-D004`, and
`TS-020-E001`, without overlap or extras. Replacement IDs are distinct
`SRC-*` identities and do not relabel retained `TS-*` identities.

The schema-v3 checker requires duplicate-free ID lists, an exact disjoint
partition of all audited sites, complete and non-overlapping replacement
coverage of excluded sites, declared replacement IDs and source-transition
symbols, and nonempty per-field backing. Fresh mutations confirmed rejection
of excluded, undeclared, fabricated, duplicate, missing, and relabeled
backing; an incomplete partition and missing replacement coverage were also
rejected. Authority-preserving fabricated/relabel mutations that pass the
generic structural layer were rejected by the target-specific reviewed
translation binding. The local validator independently matched each audited
set to the crosswalk authority.

`TS-020-D002` is the sole admitted target-020 site. Its dependency descriptor
binds target 019's result, source model, and full exact obligation by path,
size, and current SHA-256. The dependency is expressly limited to the
source-backed transition. Every `Boundary` selector is an initial
allocation/address/provenance, layout/platform, mutable-identity, or frame
observation; no returned pointer/range/endpoint, final state, target truth,
answer encoding, or trace occurs in `Boundary_T`.

## Source and semantic binding

Fresh hash checks matched every packaged active declaration, Rust item and
documentation excerpt, retained harness, transformation manifest, dependency
manifest, source-body manifest, and canonical source excerpt to both its
manifest and authority row: 9/9 artifacts for 019, 9/9 for 021, and 11/11
for 020. The active/retained contract hashes are exactly:

- 019: `840c4efc8976016ca0b1c8728d1cabb13529c6e83939e8ca3cbc31232ba6a14a`
- 021: `52c2a91bc8c7e49cd77d4429bb2b2a6e50a788211f2abca511f4df650f1a5edc`
- 020: `0d55922a668ea2e52e07ca14a1146f6ff2d0c9a9d68d9369ff4171f9a6d574c1`

The canonical mutable and const slice casts preserve allocation, address, and
provenance. The target-020 source transition computes the endpoint with
mathematical `len * size_of::<T>()`, preserves allocation/provenance, and
enforces non-nullness, alignment, isize fit, address non-wrap, and
allocation/provenance plus one-past bounds for nonzero offsets. Zero-byte
empty-slice and ZST cases remain admitted, including dangling inputs, and all
modeled final-state observations are unchanged.

## Fresh direct verification

The full acceptance driver was not rerun. The Reviewer directly executed:

```text
/home/chentianyu/miniconda3/bin/z3 -smt2 <each obligation>
/home/chentianyu/miniconda3/bin/z3 -smt2 <each probe>
../../verus/source/target-verus/release/verus proofs/<target>.rs --crate-type=lib --no-verify
../../verus/source/target-verus/release/verus proofs/<target>.rs --crate-type=lib
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_authority_design.py
```

Results:

- All 6 full-exact/exact-output obligations returned exactly `unsat\n`, exit
  zero, with empty stderr.
- All 39 probes matched: 019 = 5 SAT/6 UNSAT, 021 = 5 SAT/5 UNSAT, and
  020 = 5 SAT/13 UNSAT, totaling exactly 15 SAT/24 UNSAT.
- All three source models byte-match their captured evidence copies. Each
  type-check exited zero with empty stderr; each verification reported
  `2 verified, 0 errors`. None of the three models contains `external_body`.
- Fresh local validation reported `validation=PASS`, 62 selected rows, six
  active-authority contract drifts, 28 admissible/narrower and 34
  inadmissible boundaries, zero unlinked sites, and 51 `not-run` rows.

## Supervised acceptance, replay, and preservation

The final supervised run
`logs/live/pointer-cluster-acceptance-final-20260831T165500Z` completed with
exit status zero. Its manifest, progress log, and result record agree on
22/22 successful commands; the unit-test step ran 181 tests and reported
`OK`. All eight files in the supervised source snapshot still match their
recorded hashes.

Step 21 invoked only the self-contained
`python3 tools/run_pointer_cast_cluster.py` entry point after steps 18–20 had
produced a fully delivered three-target state. Its initial and final cluster
results are all `conditional-complete`, its recorded order is 019, 021, 020,
and its stdout reports all target pipelines, solver replays, and Verus runs
passing. Independent recomputation matched each before/after tree digest:

| Preserved evidence tree | SHA-256 |
|---|---|
| 013 | `20fefa7c85c88315176f7d92b371a546417637b8006083a22f9ed0c82b825366` |
| 022 | `b3ad4c9f03a321be32779b76c9da8e787ff0e13c691df57368fb61cdb7fbd77e` |
| 029 | `576f475b49402fd8a224231d603b35ff68600dc2bea7f96598fb1f29b7124a52` |
| 051 | `b4d575b1fbaf6ed03a3336289d077e7afe37ea1b3856c368d3ea085e576d7373` |
| 052 | `d1192be6666f2c3a01511f8fad469a090ac0c66f4797998d8eac1cd93bbd9b0f` |
| 081 | `7028372ff01661b86c08a9213a5c62ca37b49021dd6e17b528b5f04465d814a6` |
| 106 | `9ff53ef33c84b2f8b485ba85e1ffdf3b82093a6d847760379b1aaab8b058a4db` |
| 120 | `0cd3791cfe3f84f2b7bd7c6e1bf8cfa58f8c783b460e09772c1153960533030f` |

The CSV and JSON crosswalks are identical and match the replay-recorded
hashes. They contain exactly 62 rows: 11 classified and 51 `not-run`.
An in-memory replay-reset comparison found exactly six changed cells—the two
result columns for each of rows 019, 020, and 021—and no other changed cell.

**No stage transition is authorized by this review.**
