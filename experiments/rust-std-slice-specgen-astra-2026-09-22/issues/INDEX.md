# Current local issues

The reports concern the selected upstream Verus release, specdet 0.3.0 and
the Rust 1.96 source. None is a confirmed Rust implementation or documentation defect.
Independent source/semantic checks and dual-track reruns completed for the
original inputs; see the
[review account](../inventory/COVERAGE.md#independent-review-and-redundancy-repair).
The revised mutable Default adapter passes its affected engineering proof and checker
runs, and its follow-up independent review is now complete. The authoritative
second-round record is
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/8b6d043ccde7/round-0002.json`
(`review.status: done`). Both `Default` constructors are independently
reviewed in full `Seq<T>` value observation, not allocation-address determinism.
No external issue has been filed;
external filing and changes to the canonical source or trusted basis are not
authorized.

| Issue | Affected APIs | Current evidence |
|---|---|---|
| [V-METADATA](V-METADATA.md) | `len`; metadata foundation; `from_ref` / `from_mut` array delegates | Independent review reproduced both the original limitations and the singleton array/cast failures. Both singleton source counts remain zero |
| [V-SLICE-PATTERN](V-SLICE-PATTERN.md) | `first`, `split_first`, `split_last`, `last`; `first_mut`, `last_mut`; `split_first_mut`, `split_last_mut` | Earlier failures and permissions are retained. Independent review separately permitted the two exact mutable split conversions. Both adopted current files now compile with one source target each; current native comparisons and selective exports pass. Final adopted-file review remains required |
| [S-MUT-RETURN](S-MUT-RETURN.md) | `Default` for `&mut [T]`; `core::slice::from_mut`; `first_mut`, `last_mut`; `split_first_mut`, `split_last_mut` | Direct extraction failures remain. The mutable split state relation and analyze/reexecutions were independently checked, retaining both complete initial components, final input and all 19 guards off. The two new exported comparisons compile. Supplementary negative searches remain explicitly UNKNOWN, with separately proved concrete witnesses |
| [V-ASCII-CALL-BINDING](V-ASCII-CALL-BINDING.md) | `<[u8]>::make_ascii_uppercase`, `<[u8]>::make_ascii_lowercase` and their scalar dependencies; `<[T]>::split_off_last` | Earlier ASCII permissions and failures remain unchanged. Independent review separately permitted the single last split-off call rebinding. The adopted formal last source compiles with one target, one dependency and two consistency lemmas; original first and full direct analyses are unchanged. Current native comparisons and selective exports pass; final adopted-source/integration review remains required |

The singleton source bridges remain incomplete; shared determinism does not
prove them. The current mutable adaptation retains both the entire initial
sequence and the input's final return value; it is not a Default-style
initial-only shared observation. See the
[singleton account](../inventory/COVERAGE.md#singleton-reference-constructors).
The completed Default review is not reopened.

The mutable singleton state adaptation was independently completed in
`/home/chentianyu/.argus-slice-specgen-astra-20260922/projects/s-74553d43/handoffs/63ed051184d5/round-0001.json`.
This is a recorded result, not a new replay in the ASCII work. The original
direct-extraction failure and both missing array source proofs remain open.

The original constructor integration also recompiled the unchanged
`is_empty` source proof with one target function and two imported
consistency lemmas; see
[`logs/defaults/correctness/is_empty/`](../logs/defaults/correctness/is_empty/).
Its trusted `len` boundary remains exactly as described in V-METADATA.
Neither the two empty-array constructor proofs nor their completeness
results resolve pointer metadata or slice-pattern translation. The five
old failed inputs and their diagnostics were not replaced or rerun during
that integration. Reviewer's later independent checks reproduced the two
metadata limitations and four slice-pattern rejections; all five source
proofs remained incomplete at that review. The later, explicitly approved
`first`/`last` conversions now have compiled source proofs and fresh checker
results as recorded in V-SLICE-PATTERN. They do not resolve metadata or either
split method.

The separately permitted split conversions have now been adopted, as recorded
in [their current-source results](V-SLICE-PATTERN.md#adopted-split-source-results).
They depend on the existing upstream `split_at` value contract and do not
prove `split_at` itself. The original pattern diagnostics and both original
split proof inputs remain preserved, and final independent review of the
adopted split inputs is still required.
