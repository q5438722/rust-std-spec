---
title: ASCII case mutation and its scalar source boundary
description: Complete final-sequence observations cover all bytes; reviewed local call rebindings connect slice and scalar source proofs without new assumptions.
---

# ASCII case mutation and its scalar source boundary

Rust 1.96 `slice/ascii.rs:161-181,183-203` documents and implements
`<[u8]>::make_ascii_uppercase` and `make_ascii_lowercase`. Both take only
`&mut self`, return unit, and are stable const functions since Rust 1.84.
The authoritative source root is recorded in
[toolchain/BASELINE.md](../../../../../toolchain/BASELINE.md).

[The public bindings](../../../../../specs/slice/ascii.rs) and
[their predicates](../../../../../specs/slice/ascii_post.rs) reuse `Seq<u8>`.
The full final sequence equals the initial sequence mapped bytewise.
Uppercase conversion subtracts 32 on 97 through 122; lowercase conversion
adds 32 on 65 through 90. Every other byte is unchanged. Full sequence
equality also determines length and order, so separate clauses for those
facts would be redundant. No ASCII, UTF-8 or nonempty precondition is needed.

## The final sequence is an output, not an environment input

These methods return no borrow. Unlike the
[mutable singleton constructor](singleton-source-bridge.md), there is no
caller-owned returned slice whose subsequent writes must be represented as
an environment input. The casing relation takes only `old(slice)@` as input
and observes all of `final(slice)@` as output at the call boundary.

[The state lemmas](../../../../../proofs/completeness/slice/ascii_state.rs)
prove the candidate relation is the full sequence map, construct
length-preserving witnesses for every initial sequence, and relate slice
value equality to full view equality. The analysis functions use
`Ghost<Seq<u8>>` carriers for initial and final contents without changing the
public mutable-receiver/unit-return signature.

The actual generated comparisons in
[uppercase](../../../../../proofs/completeness/slice/make_ascii_uppercase.rs)
and [lowercase](../../../../../proofs/completeness/slice/make_ascii_lowercase.rs)
use `((r1)@ =~= (r2)@)`. The retained original queries disable all 55 generated
search guards. These are complete value-observation results, not source
implementation proofs or claims about allocation addresses.

## Source support on Verus 0.2026.09.20.aef82ed

The scalar call chain is mutation, conversion, then ASCII classification.
Rust 1.96 defines those bodies at `num/mod.rs:716-718,742-744`,
`639-642,664-667`, and `812-814,846-848`, respectively.
The conversion expressions use XOR or OR with `ASCII_CASE_MASK = 32`,
whose definition is at `num/mod.rs:539`.

Both original classification bodies verify after only lifting their receivers
to free-function parameters. An
[isolated indexed assignment](../../../../../issues/repros/ascii_mutable_index.rs)
also verifies the full slice-update relation using the selected upstream
indexing model. Neither result registers a binding for an external `u8`
method.

The original conversion, mutation and slice proof copies were rejected at
those external calls before verification. A
[contract-free reproduction](../../../../../issues/repros/u8_ascii_method_binding.rs)
has the same six rejections. New assumed declarations are not permitted by
the required `--no-cheating` source runs. The exact commands, diagnostics,
source correspondence and reviewed call-rebinding substitutions are in
[V-ASCII-CALL-BINDING](../../../../../issues/V-ASCII-CALL-BINDING.md).
This support boundary is specific to the selected release and these calls;
it is not a Rust defect or a claim about every possible verification method.

## Source-copy correspondence and successful proofs

Six reviewed substitutions bind the slice mutations to local scalar mutations,
the scalar mutations to local conversions, and the conversions to local
classifiers. The concrete `u8` receivers, const signatures, shared reads,
assignment order and indexed exclusive reborrows are preserved. No borrow
escapes the unit-returning mutation. The original XOR/OR expressions, mask,
loop and increment are unchanged.

Four ghost bit-vector assertions establish the equivalence of the original
bitwise expressions to the arithmetic specification on the relevant letter
intervals, and the identity for each zero mask. These assertions are proved,
not assumed. The original converted-prefix/unchanged-suffix loop invariant
proves the complete final sequence, including empty inputs and all 256 byte
values.

With `--compile --no-cheating --num-threads 1`, the
[scalar input](../../../../../proofs/correctness/num/u8_ascii.rs) verifies
11 obligations: six source functions, one constant and four bit-vector
assertions. Each
[uppercase](../../../../../proofs/correctness/slice/make_ascii_uppercase.rs)
or [lowercase](../../../../../proofs/correctness/slice/make_ascii_lowercase.rs)
input verifies 13: those eleven plus the slice body and its loop obligation.
The source copies and their dependencies are retained alongside the successful
[commands, queries and compiler outputs](../../../../../logs/ascii-case/rebinding/).
This is a source-derived proof on the selected upstream length/indexing basis,
not a new external-method binding or a proof of Rust 1.96 metadata internals.

The public candidates, full-state analysis inputs and checker configuration
are unchanged. The
[exporter](../../../../../scripts/export_completeness.py) checks the current
source-proof bytes against the successful compile's snapshot as well as the
existing completeness snapshots. It refuses failed, incomplete or stale
source results and records one slice source target per API.

[Native checks](native-output-locations.md#ascii-case-source-checks) exercise
all byte values, stable const calls, exact signatures and subslice frames.
They complement, rather than replace, either formal proof dimension. The
upstream `len` and indexing models do not establish the Rust 1.96
implementations of those dependencies.
