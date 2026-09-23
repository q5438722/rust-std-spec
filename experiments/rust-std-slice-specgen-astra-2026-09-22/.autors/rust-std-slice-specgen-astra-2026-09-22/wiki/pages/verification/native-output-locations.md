---
title: Native validation output locations
description: The native Rust checks can write beneath a separate directory while reading the unchanged project and authoritative source.
---

# Native validation output locations

`scripts/check_native.py --output-root DIR` writes temporary Rust inputs and
binaries beneath `DIR/target/defaults/native`, and retains compiler diagnostics,
test output and command records beneath `DIR/logs/defaults/native`. Without
the option, both paths remain beneath the project root. Relative output roots
are resolved from the invocation directory.

Only output placement changes. The authoritative source path, source spans,
project test files, Rust 1.96 toolchain selection and negative-test expectations
remain the same. The compiler still runs with the project as its working
directory. Temporary generated files are removed on exit, while command logs
are retained even when a compiler invocation fails.

Independent review uses `run_review_command` and supplies
`--output-root {scratch}/native`; output redirection alone does not enforce
read-only execution. These native checks supplement, rather than replace,
Verus source correctness and specdet completeness.

The implementation is
[scripts/check_native.py](../../../../../scripts/check_native.py).
`NativeCheckOutputPaths` in
[tests/test_contract_bindings.py](../../../../../tests/test_contract_bindings.py)
covers default and redirected locations, unchanged compiler working directory,
cleanup, and failure-log retention. The command and toolchain are documented in
[toolchain/BASELINE.md](../../../../../toolchain/BASELINE.md).

## Singleton source checks

`--group singleton` selects only `core::slice::from_ref`, `from_mut` and their
array delegates. Generated source and binaries use
`DIR/target/singleton/native`; logs use `DIR/logs/singleton/native`. This
group removes `RUSTC_BOOTSTRAP` from its compiler environment, so the native
checks exercise stable Rust 1.96, including both const calls.

The source-copy spans are `slice/raw.rs:203-205,211-213` and
`array/mod.rs:166-169,174-177`. `source-spans.json` preserves the exact copied
text, while `commands.json` and `results.json` retain compiler return codes
and each expected negative diagnostic. Temporary source copies, binaries and
negative probes are removed; existing unrelated output files are preserved.
The original group and its `defaults` paths are unchanged.

[tests/test_native_singleton.py](../../../../../tests/test_native_singleton.py)
covers selection, output redirection, span drift, exact rejection diagnostics,
and cleanup on success or failure. Native behavior and compile-time rejection
do not establish the missing
[singleton source bridge](singleton-source-bridge.md).

## ASCII case source checks

`--group ascii-case` selects only the two `[u8]` in-place case conversions.
Generated Rust files and binaries use `DIR/target/ascii-case/native`; retained
commands and diagnostics use `DIR/logs/ascii-case/native`. The runner removes
`RUSTC_BOOTSTRAP` and checks stable Rust 1.96. Source copies are extracted
from `slice/ascii.rs:173-181,195-203`, with their exact text and spans retained
in `source-spans.json`.

The group executes 17 tests against both source copies and real public APIs,
including all 256 single-byte inputs, ordered mixed slices, non-ASCII values,
repeat conversions, stable const calls and subslice frame preservation.
Expected mappings use numeric ASCII intervals and offsets rather than the
tested methods. Sixteen compile-time probes reject shared receivers, wrong
element types, wrong returns and extra arguments. Linking failures, zero
tests or an irrelevant diagnostic cannot count as successful checks.

Only the current temporary files are removed; older groups and unrelated
outputs are preserved. Independent review can use
`scripts/check_native.py --group ascii-case --output-root {scratch}/native-ascii`
through the existing restricted command interface.
The checks and their focused Python tests are
[ascii_case_behavior.rs](../../../../../tests/ascii_case_behavior.rs) and
[test_native_ascii_case.py](../../../../../tests/test_native_ascii_case.py).
They do not establish the
[scalar call correspondence](ascii-case-mutation.md#source-copy-correspondence-and-successful-proofs);
that relation and its formal proofs are separate.

## Adopted endpoint comparisons

`--group endpoints` compares only `first` and `last`. It reads the authoritative
Rust 1.96 spans `slice/mod.rs:140-157,266-283` and the actual current proof bodies
under `proofs/correctness/slice/`, after their two approved conversions. It rejects
drift in the docs, signatures, original bodies, import paths, postcondition
bindings or the two exact approved expressions. The analysis declarations and
other four original observer bodies remain subject to exact comparison.
Existing native groups retain their behavior.

With `--output-root DIR`, outputs use `DIR/target/endpoints/native`
and `DIR/logs/endpoints/native`. The latter retains source spans,
source mappings, generated Rust inputs, Rust 1.96 generic MIR, commands,
diagnostics and test results. Bootstrap is removed and overflow checks remain
enabled. Existing files at those output paths cause an explicit error; a fresh
output root preserves earlier results. Temporary binaries and individual
rejection inputs are removed, but the source inputs underlying the MIR remain.

The group compares the patterns, adopted bodies and real public methods. Its
behavior tests include non-Copy/non-static elements, legal empty uninhabited
slices, zero-sized slices including the largest `usize` length, shared-reference
positions and stable const calls. Compiler rejection probes cover invalid
arguments, wrong return types, attempted mutation and lifetime escapes.
Pointer equality cannot distinguish zero-sized element positions; source
correspondence remains a separate obligation.

Independent execution uses the same restricted command interface:
`scripts/check_native.py --group endpoints --output-root {scratch}/endpoints`.
The code and focused tests are
[check_native.py](../../../../../scripts/check_native.py),
[endpoint_proposal_behavior.rs](../../../../../tests/endpoint_proposal_behavior.rs)
and [test_native_endpoints.py](../../../../../tests/test_native_endpoints.py).
The two conversions and their source argument are confined to
[the endpoint correspondence](endpoint-source-correspondence.md).
Native compilation, MIR and examples do not replace either required proof
track. The earlier `endpoints-proposal` execution path was replaced, not kept
alongside the adopted path. Its retained inputs and logs remain readable in
`logs/endpoints-proposal/`; the current group does not use them as source.

## Adopted split comparisons

`--group splits` selects only `split_first` and `split_last`.
It reads the original Rust 1.96 spans `slice/mod.rs:182-200,224-242` and
extracts the two exact approved current proof bodies from
`proofs/correctness/slice/`. No proof copy, candidate, completeness file or
coverage row is written. Both executable differences must match the
separately permitted split conversions; endpoint permission is not reused.

With `--output-root DIR`, generated inputs and retained command logs, source
spans, mappings, diagnostics and generic runtime/const MIR use
`DIR/logs/splits/native`. Temporary executables and rejection probes
use `DIR/target/splits/native` and are removed on exit. Existing named
outputs cause an explicit error rather than being replaced.

The tests compare the authority patterns, current adopted bodies and public APIs
using exact higher-ranked shared signatures. Both tuple components, complete
ordered remainders, singleton empty-remainder origins, non-Copy/non-static
elements, empty uninhabited slices, zero-sized slices and const invocations
are represented. Separate rejection probes check both references'
mutability and input-bound lifetimes. Non-ZST address comparisons supplement
but do not establish the
[full source correspondence](split-source-dependencies.md).

Independent execution uses
`scripts/check_native.py --group splits --output-root {scratch}/splits`
through the existing restricted command interface. The runner requires
successful compilation, linking and execution; missing `cc` is a runtime
check failure, not a pass. The focused tests in
[`tests/test_native_splits.py`](../../../../../tests/test_native_splits.py)
honor `TMPDIR` for scratch-only temporary files.

The former `splits-proposal` route was replaced, not retained as a parallel
execution path. Its original inputs and results remain in
`logs/splits-proposal/` and `logs/splits/adoption-before/`; current comparisons
do not read the isolated proposals.

## Adopted mutable split comparisons

`--group mutable-splits` compares the authoritative Rust 1.96
`split_first_mut`/`split_last_mut` patterns, their adopted current proof
bodies and the actual public methods. Only the current formal source files
under `proofs/correctness/slice/` are native inputs; historical proposal
files can be absent or changed without affecting this comparison.

The extractor checks complete documentation, const/mutable signatures,
unconstrained generics, pure predicates, source bindings and exact executable
bodies. Each source's sole ghost block calls the existing borrowed-slice
length fact on `tail` or `init`. Only that exact block is erased for native
compilation; altered or additional ghost code is rejected.

With `--output-root DIR`, retained source inputs, metadata, runtime/const MIR,
commands, results and rejection diagnostics are under
`DIR/logs/mutable-splits/native`. Temporary executables and partial
compiler outputs are under `DIR/target/mutable-splits/native` and
are removed. Existing named outputs are not overwritten. The focused Python
tests use `TMPDIR` when provided.

The behavior tests keep both outputs live while replacing their contents
separately, repeatedly and in interleaved orders. They observe the complete
initial remainder, final input and outside-subrange frame. Const execution,
exact higher-ranked signatures, both output lifetimes and conflicting
receiver/alias rejection are included. Non-Copy/non-static values, singleton
empty-remainder origins, zero-sized extents and empty uninhabited slices
remain legal. Pointer equality is not used to establish zero-sized provenance.

Independent execution uses `run_review_command`/`get_review_command`, the
project-local linker, explicit `RUSTUP_HOME` and scratch output. The exact
argv is in `runtime-review-readiness.json` under
`native_mutable_splits_replay`. The runner and tests are
[`check_native.py`](../../../../../scripts/check_native.py),
[`mutable_split_behavior.rs`](../../../../../tests/mutable_split_behavior.rs)
and [`test_native_mutable_splits.py`](../../../../../tests/test_native_mutable_splits.py).
The [state observation](mutable-split-observations.md) and the independently
reviewed source correspondence remain separate obligations.

The former `mutable-splits-proposal` execution route was replaced rather
than kept as a second current path. Its original inputs and results remain
under `logs/mutable-splits-proposal/`, and the pre-adoption files and replay
guidance are preserved in `logs/mutable-splits/adoption-before/`.
The exact permission is confined to
[the two mutable split conversions](../../../../../issues/V-SLICE-PATTERN.md#independent-mutable-split-permission-before-adoption).

## Adopted mutable endpoint comparisons

`--group mutable-endpoints` reads the authoritative `first_mut` and
`last_mut` documentation/signatures/bodies at `slice/mod.rs:159-180,285-306`,
reads the two independently permitted current proof files under
`proofs/correctness/slice/`. Isolated proposal files are not execution
inputs; removing or changing them cannot affect this native comparison.
Source, pure-postcondition bindings, const/mutable signatures and the two
precise approved bodies are checked before compiling. The independent
permission is confined to
[these two conversions](../../../../../issues/V-SLICE-PATTERN.md#independent-mutable-permission-before-adoption).

The pure-predicate comparison is exact, including
`observations.1 =~= seq![]` in both empty branches. The mutation tests reject
both removing that relation and reverting it to `==`; a proved equivalent
earlier predicate spelling is not a match for the current source text.
Changing a predicate without synchronizing this comparison stops the runner
before Rust compilation and cannot supply current native evidence.

With `--output-root DIR`, generated source, metadata, runtime/const MIR,
commands, diagnostic results and test logs remain under
`DIR/logs/mutable-endpoints/native`. Temporary binaries use
`DIR/target/mutable-endpoints/native` and are removed on exit.
Existing named outputs cause an error rather than being overwritten.
Rust 1.96 runs with bootstrap removed and overflow checking enabled.

The comparison actually links and executes writes through the returned
references, then checks the whole input and outside-subrange frame against
the original pattern, adopted current body and public method. It covers empty,
singleton, ordered/repeated, non-Copy/non-static, zero-sized and empty
uninhabited slices. A safe maximum-length unit `Vec` avoids materializing a
giant array constant in Rust 1.96's MIR printer. This changes the test input
representation, not any of the three implementations.

The group also checks exact higher-ranked mutable signatures, stable const
writes and compiler rejections for wrong types/arguments, lifetime escape
and conflicting accesses while the returned borrow is still used.
Zero-sized positions are not inferred from equal addresses. The tests and
runner are
[`mutable_endpoint_behavior.rs`](../../../../../tests/mutable_endpoint_behavior.rs),
[`test_native_mutable_endpoints.py`](../../../../../tests/test_native_mutable_endpoints.py)
and [`check_native.py`](../../../../../scripts/check_native.py).

Independent execution uses the existing restricted command interface and
project-local linker, with output in scratch. The exact argv is under
`native_mutable_endpoints_replay` in
[`runtime-review-readiness.json`](../../../../../runtime-review-readiness.json).
The [optional mutable observation description](mutable-endpoint-observations.md)
states the separate source and checker boundaries.

The former `mutable-endpoints-proposal` route is no longer executable.
Its source inputs and logs remain under `logs/mutable-endpoints-proposal/`,
and the exact pre-adoption files are preserved under
`logs/mutable-endpoints/adoption-before/`. The current behavior tests differ
only in the implementation labels and source file names, not their checks.

## Shared split-off comparisons before a call rebinding

`--group split-off-endpoints-proposal` reads Rust 1.96
`slice/mod.rs:4993-5015,5043-5065`, both actual formal split-off source
files, the isolated last proposal and its actual local shared `split_last`
dependency. It compares authority originals, current formal bodies, that
last proposal and real public APIs. No first proposal is required or read.
This route is explicitly not an adopted-source route.

The extractor checks the complete docs, attributes, unconstrained inner
lifetimes, control flow, pure predicates, public-declaration isolation and
slot-assignment order. It erases only the checked proof syntax. Generated
source, metadata, generic/runtime MIR, command records, results and negative
Rust inputs remain under
`DIR/logs/split-off-endpoints-proposal/native`. Only named transient compiler
outputs under `DIR/target/split-off-endpoints-proposal/native` are removed.
The focused Python tests use `TMPDIR` when it is provided.

The suite tests repeated first, repeated last, alternating and exhausted
calls, keeping previous returned references live throughout. It also
reassigns the slot to an unrelated slice, checks unchanged owners and
subslice frames, distinguishes singleton empty-remainder origins for non-ZST
elements, and retains non-Copy, non-static, ZST and empty uninhabited cases.
The exact higher-ranked signature keeps the return tied to the inner
slice rather than the outer slot borrow.

Two diagnostic-checked negative probes call the real public methods in
const contexts without a feature. They must fail on Rust 1.96; compiling
the local const source copies cannot establish stable public const support.
Other rejected cases include wrong receivers, arguments, mutable returns
and owner-lifetime escapes. No native undefined behavior is executed.

The actual Rust 1.96 MIR prints the unique local dependency as
`fn split_last`, without its module path; the checked source and recorded
dependency path still determine which function that is. The five split-off
function names remain qualified by their original/current/proposal modules.
Both runtime and const MIR versions may be printed for a const function.
The runner recognizes the six generic source signatures rather than
counting textual `fn` occurrences.

Use the existing read-only command actions and project-local linker with
`--output-root {scratch}/native-split-off`. The exact argv is in
`runtime-review-readiness.json` under
`native_split_off_endpoints_proposal_replay`. The
[reference-slot description](split-off-reference-state.md) explains the
separate source and direct-comparison boundaries.

## Native linking in the configured Ubuntu read-only environment

The configured `ubuntu:24.04` image has no `cc`. The existing read roots
include this project, Rustup and Miniconda `bin`/`lib`, but not the host
compiler installation or the engineering Argus Python checkout.
`toolchain/review-native/bin/cc` supplies a project-local GCC 13.3.0 driver
with its pinned Ubuntu link dependencies in a local sysroot. It was extracted
from packages without system installation, image changes or broader mounts.
Package versions and actual extraction commands are in
[`logs/splits/native-linker-setup/`](../../../../../logs/splits/native-linker-setup/).

For native replay, put that directory first on `PATH`, retain the existing
Rustup/Cargo paths, explicitly set `RUSTUP_HOME`, and use the already mounted
`/home/chentianyu/miniconda3/bin/python` for the standard-library runner.
The exact argv is in
[`runtime-review-readiness.json`](../../../../../runtime-review-readiness.json),
under `native_split_replay`. Execute it through the restricted command tool,
not an unsandboxed replacement, with `--output-root {scratch}/native-splits`.
The compiler does not change the API, candidate or native test inputs.

With those paths, the actual adopted split native suite linked and ran
15 tests plus 120 diagnostic-checked rejections in one engineering invocation
of the unchanged restricted environment. The command record is
[`logs/splits/native-readonly-engineering/result.json`](../../../../../logs/splits/native-readonly-engineering/result.json).
This is scoped evidence that the linker is usable there, not a claim of
independent replay, general container reliability or API correctness.
