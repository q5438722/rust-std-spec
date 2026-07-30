# Organized Rust std verification suite

Contracts are grouped by their original vstd source file.

- Groups: **36**
- Strict-faithful local-surrogate proofs: **168**
- External-body fallbacks: **371**

Each group has `proved/` and/or `external_body/` subdirectories. Proved entries contain the copied proof, original contract, Rust source, and metadata. Fallback entries retain the original contract on a same-signature `#[verifier::external_body]` mirror.

The proved entries verify local surrogate functions. Artificial `source_*` prefixes are removed during export; helper proofs use descriptive names ending in `_proof`. These entries do not directly prove the original external Rust std symbols, and no machine-checked linkage theorem connects the two.

Run everything with:

```bash
./verify.sh
```

Conservative fidelity mode uses `source-verification/fidelity-verdicts.json`: alternate implementations, inadmissible proofs, wrong mappings, and unresolved source bodies are moved to `external_body/`.
