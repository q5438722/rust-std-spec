# Rust std spec generation with determinism feedback

## 1. Experiment scope

The starting point was the 2,121 stable Rust APIs used by Nanvix whose
canonical API paths were not covered by the current Verus vstd inventory.

The experiment first classified all targets, then ran generation only on the
high-confidence first-run subset.

Source/toolchain snapshot:

- Nanvix: `bac7075214a385b0088145eb0738cc0c4f121feb`
- Nanvix Rust: `nightly-2026-07-09`
- Rust source: `14cae681329a63c622a6e1fbe1d30f9374bc51d8`
- Verus/vstd: `1beb0fad337b8f8a224cf8684162cb02d0c2fc01`
- Verus Rust toolchain: `1.96.0`
- Model: `gpt-5.6-sol`
- Feedback rounds: at most 2

## 2. Classification

| Classification | Count |
|---|---:|
| Runtime, OS, I/O, or hidden state | 495 |
| Needs a new vstd abstraction | 361 |
| Trait-contract integration | 201 |
| Unsafe or representation-sensitive | 181 |
| Atomic/concurrent hidden state | 179 |
| **Suitable for the first run** | **133** |
| Determinism checker does not support the return shape | 109 |
| Iterator/adapter result requires a prophetic model | 101 |
| Formatting effect | 79 |
| Higher-order contract | 71 |
| Not present in Verus's Rust 1.96 toolchain | 70 |
| Representation or allocator state | 59 |
| Ownership or uninitialized-memory model | 33 |
| Complex result or pattern model | 21 |
| Associated-type/projection integration | 19 |
| No modeled observable output | 9 |
| **Total** | **2,121** |

The 133 selected targets were primarily APIs on `String`, `Vec`, `Option`,
`Result`, slices, strings, arrays, ranges, and modeled map/set types.

## 3. Generation and feedback result

| Metric | Count |
|---|---:|
| Targets run | 133 |
| Initial `add_spec` decisions | 129 |
| Initial `skip` decisions | 4 |
| Final `add_spec` decisions | 103 |
| Final `skip` decisions | 30 |
| Typechecked final contracts | 103 |
| Determinism checks with `R0 = unsat` | 103 |
| Raw determinism reward | 103 |
| Guarded determinism reward | 103 |
| Semantic-gated reward | 94 |
| Final `sat` or `unknown` checks | 0 |
| LLM errors after retries | 0 |

Feedback changed 26 initial `add_spec` proposals into final `skip` decisions.
The remaining 103 add-spec candidates all typechecked and uniquely determined
the modeled outputs after final rechecking.

No generated candidate is automatically eligible for upstream application.
`assume_specification` is trusted, so typechecking and determinism do not prove
that a contract is sound.

## 4. Representative successful candidates

### `alloc::string::String::clear`

```rust
ensures
    final(s)@ == Seq::<char>::empty(),
```

This directly captures the observable content effect while intentionally
ignoring capacity.

### `core::mem::replace`

```rust
ensures
    res == *old(dest),
    *final(dest) == src,
```

This matches the implementation's read-old/write-new behavior.

### `core::option::Option::replace`

```rust
ensures
    res == *old(option),
    *final(option) == Some(value),
```

### `core::slice::as_chunks`

The generated contract used the nonzero chunk-size precondition and specified
the array-chunk prefix and exact remainder through sequence views. The final
contract typechecked and had `R0 = unsat`.

## 5. Final skip examples

### `alloc::string::String::replace_range`

The model skipped this API because the generic `RangeBounds` implementation can
be stateful, while no existing vstd law connects its observed bounds to a stable
logical range.

### `core::slice::reverse`

The model skipped this API because the current determinism pipeline cannot
materialize the exact unsized mutable-slice post-state needed by the generated
check.

### `core::mem::needs_drop`

The model found no existing public vstd vocabulary that exposes the compiler's
type-level destructor property.

## 6. Why determinism reward still needs semantic gates

A manual semantic audit of the 24 guarded-deterministic pilot candidates found:

- 18 likely sound;
- 6 likely unsound.

The main failure modes were:

1. using raw `Map`/`Set` algebra for `BTreeMap`/`BTreeSet`, even though runtime
   key conflicts are determined by `Ord` equivalence rather than Rust equality;
2. adding source-unjustified preconditions to force determinism;
3. modeling trait-calling mutations, such as `Vec::dedup`, as pure transforms of
   the old sequence.

Four narrow postprocessing gates reproduced all six pilot findings:

- raw BTree view algebra;
- borrowed-key domain strengthening;
- clone-behavior domain strengthening;
- pure old-sequence modeling for `Vec::dedup`.

Across the full 133-target run:

- 103 candidates passed guarded determinism;
- 94 also passed these semantic postprocessing gates;
- 9 were flagged for semantic review.

The semantic-gated count is still a triage result, not a soundness proof.

## 7. Semantic audit of the full result

A second owner-stratified audit sampled 30 of the 76 semantic-gated candidates
that were not part of the original pilot audit:

- 27 were likely sound;
- 3 were uncertain;
- 0 were clearly unsound.

The resulting semantic-precision estimate for the 94-candidate set is roughly
90–95%, with a point estimate near 92%.

The three uncertain cases exposed additional patterns:

1. `core::slice::binary_search` followed the current implementation's duplicate
   selection policy even though the public API permits any matching index;
2. `RangeInclusive::start`/`end` specified stored fields even after exhaustion,
   where the public API documents those values as unspecified;
3. `HashSet::replace` depends on whether the logical set view already quotients
   keys by the hash/equality model.

These are implementation-detail and abstraction-boundary risks, not
determinism failures.

## 8. Artifacts

- `CLASSIFICATION.md`: complete classification summary and selected target list.
- `classification.csv`: one classification row per original target.
- `classified-manifest.json`: all 2,121 enriched targets.
- `suitable-manifest.json`: the 133 selected targets.
- `suitable-pilot-gpt56sol-v2/`: 32-target pilot artifacts.
- `suitable-remaining-gpt56sol-v1/`: remaining 101 target artifacts.
- `suitable-combined-gpt56sol/ANALYSIS.md`: combined per-target results.
- `suitable-combined-gpt56sol/final_candidates.csv`: final candidate table.
- `ALL-2121-SPECGEN-RESULTS-2026-07-23.md`: follow-up experiment covering
  every remaining API.
