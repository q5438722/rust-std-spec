For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::PathBuf::leak",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "leak",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "resolved_path": {
                "args": null,
                "id": 1802,
                "path": "Path"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1278: \n  1279:     /// Consumes and leaks the `PathBuf`, returning a mutable reference to the contents,\n  1280:     /// `&'a mut Path`.\n  1281:     ///\n  1282:     /// The caller has free choice over the returned lifetime, including 'static.\n  1283:     /// Indeed, this function is ideally used for data that lives for the remainder of\n  1284:     /// the program's life, as dropping the returned reference will cause a memory leak.\n  1285:     ///\n  1286:     /// It does not reallocate or shrink the `PathBuf`, so the leaked allocation may include\n  1287:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n  1288:     /// capacity, call [`into_boxed_path`], and then [`Box::leak`] instead.\n  1289:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n  1290:     ///\n  1291:     /// [`into_boxed_path`]: Self::into_boxed_path\n  1292:     #[stable(feature = \"os_string_pathbuf_leak\", since = \"1.89.0\")]\n  1293:     #[inline]\n  1294:     pub fn leak<'a>(self) -> &'a mut Path {\n  1295:         Path::from_inner_mut(self.inner.leak())\n  1296:     }\n  1297: \n  1298:     /// Extends `self` with `path`.\n  1299:     ///\n  1300:     /// If `path` is absolute, it replaces the current path.\n  1301:     ///\n  1302:     /// On Windows:\n  1303:     ///\n  1304:     /// * if `path` has a root but no prefix (e.g., `\\windows`), it\n  1305:     ///   replaces everything except for the prefix (if any) of `self`.\n  1306:     /// * if `path` has a prefix but no root, it replaces `self`.\n  1307:     /// * if `self` has a verbatim prefix (e.g. `\\\\?\\C:\\windows`)\n  1308:     ///   and `path` is not empty, the new path is normalized: all references\n  1309:     ///   to `.` and `..` are removed.\n  1310:     ///",
    "nanvix_source": "  1284:     /// the program's life, as dropping the returned reference will cause a memory leak.\n  1285:     ///\n  1286:     /// It does not reallocate or shrink the `PathBuf`, so the leaked allocation may include\n  1287:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n  1288:     /// capacity, call [`into_boxed_path`], and then [`Box::leak`] instead.\n  1289:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n  1290:     ///\n  1291:     /// [`into_boxed_path`]: Self::into_boxed_path\n  1292:     #[stable(feature = \"os_string_pathbuf_leak\", since = \"1.89.0\")]\n  1293:     #[inline]\n  1294:     pub fn leak<'a>(self) -> &'a mut Path {\n  1295:         Path::from_inner_mut(self.inner.leak())\n  1296:     }\n  1297: \n  1298:     /// Extends `self` with `path`.\n  1299:     ///\n  1300:     /// If `path` is absolute, it replaces the current path.\n  1301:     ///\n  1302:     /// On Windows:\n  1303:     ///\n  1304:     /// * if `path` has a root but no prefix (e.g., `\\windows`), it",
    "previous_skip_rationale": ""
  }
]
```

Return JSON only:
{
  "candidates": [
    {
      "target": "exact target string",
      "decision": "add_spec" | "skip",
      "contract_form": "assume_specification" | "external_trait_specification",
      "contract_code": "complete Verus declaration(s), without verus! wrapper",
      "requires": ["..."],
      "ensures": ["..."],
      "feature_gates": ["..."],
      "imports": ["..."],
      "useful": true | false,
      "rationale": "short source-grounded explanation",
      "risks": ["..."]
    }
  ]
}

Rules:
- Return exactly one candidate for every target, in the same order.
- Do not edit files.
- External contracts are trusted; do not invent private fields, hidden state, or
  stronger behavior than the supplied signature/source supports.
- Respect each target's classification and reasons. A `skip` decision is the
  expected result for runtime effects, hidden state, formatting, concurrency,
  unavailable toolchain APIs, unsupported mutable-reference returns, and APIs
  that need a missing abstraction.
- Use `add_spec` only when a concrete useful relation can be written in existing
  public vstd vocabulary.
- For `add_spec`, use the exact Rust 1.96 signature metadata. Bind non-unit
  results by name. Use `old(x)`/`final(x)` for mutable references.
- Do not add cfg/cfg_attr attributes.
- Do not use `true`, `false`, `arbitrary()`, `assume`, `requires false`, or
  source-unjustified preconditions to force determinism.
- Prefer `skip` over a deterministic but semantically unsupported contract.
