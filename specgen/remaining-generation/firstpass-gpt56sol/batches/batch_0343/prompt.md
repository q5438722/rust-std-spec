For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::ffi::OsString::from_encoded_bytes_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "from_encoded_bytes_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u8"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 222,
                "path": "Vec"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   168:     /// use std::ffi::OsStr;\n   169:     ///\n   170:     /// let os_str = OsStr::new(\"Mary had a little lamb\");\n   171:     /// let bytes = os_str.as_encoded_bytes();\n   172:     /// let words = bytes.split(|b| *b == b' ');\n   173:     /// let words: Vec<&OsStr> = words.map(|word| {\n   174:     ///     // SAFETY:\n   175:     ///     // - Each `word` only contains content that originated from `OsStr::as_encoded_bytes`\n   176:     ///     // - Only split with ASCII whitespace which is a non-empty UTF-8 substring\n   177:     ///     unsafe { OsStr::from_encoded_bytes_unchecked(word) }\n   178:     /// }).collect();\n   179:     /// ```\n   180:     ///\n   181:     /// [conversions]: super#conversions\n   182:     #[inline]\n   183:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   184:     pub unsafe fn from_encoded_bytes_unchecked(bytes: Vec<u8>) -> Self {\n   185:         OsString { inner: unsafe { Buf::from_encoded_bytes_unchecked(bytes) } }\n   186:     }\n   187: \n   188:     /// Converts to an [`OsStr`] slice.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```\n   193:     /// use std::ffi::{OsString, OsStr};\n   194:     ///\n   195:     /// let os_string = OsString::from(\"foo\");\n   196:     /// let os_str = OsStr::new(\"foo\");\n   197:     /// assert_eq!(os_string.as_os_str(), os_str);\n   198:     /// ```\n   199:     #[cfg_attr(not(test), rustc_diagnostic_item = \"os_string_as_os_str\")]\n   200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   166:     ///     // SAFETY:\n   167:     ///     // - Each `word` only contains content that originated from `OsStr::as_encoded_bytes`\n   168:     ///     // - Only split with ASCII whitespace which is a non-empty UTF-8 substring\n   169:     ///     unsafe { OsStr::from_encoded_bytes_unchecked(word) }\n   170:     /// }).collect();\n   171:     /// ```\n   172:     ///\n   173:     /// [conversions]: super#conversions\n   174:     #[inline]\n   175:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   176:     pub unsafe fn from_encoded_bytes_unchecked(bytes: Vec<u8>) -> Self {\n   177:         OsString { inner: unsafe { Buf::from_encoded_bytes_unchecked(bytes) } }\n   178:     }\n   179: \n   180:     /// Converts to an [`OsStr`] slice.\n   181:     ///\n   182:     /// # Examples\n   183:     ///\n   184:     /// ```\n   185:     /// use std::ffi::{OsString, OsStr};\n   186:     ///",
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
