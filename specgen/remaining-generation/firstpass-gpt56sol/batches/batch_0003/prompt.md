For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::trim_right_matches",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "lifetime": "'a"
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
                  "args": {
                    "angle_bracketed": {
                      "args": [
                        {
                          "lifetime": "'a"
                        }
                      ],
                      "constraints": []
                    }
                  },
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "trim_right_matches",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  2694:     ///\n  2695:     /// let x: &[_] = &['1', '2'];\n  2696:     /// assert_eq!(\"12foo1bar12\".trim_right_matches(x), \"12foo1bar\");\n  2697:     /// ```\n  2698:     ///\n  2699:     /// A more complex pattern, using a closure:\n  2700:     ///\n  2701:     /// ```\n  2702:     /// assert_eq!(\"1fooX\".trim_right_matches(|c| c == '1' || c == 'X'), \"1foo\");\n  2703:     /// ```\n  2704:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2705:     #[deprecated(\n  2706:         since = \"1.33.0\",\n  2707:         note = \"superseded by `trim_end_matches`\",\n  2708:         suggestion = \"trim_end_matches\"\n  2709:     )]\n  2710:     pub fn trim_right_matches<P: Pattern>(&self, pat: P) -> &str\n  2711:     where\n  2712:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2713:     {\n  2714:         self.trim_end_matches(pat)\n  2715:     }\n  2716: \n  2717:     /// Parses this string slice into another type.\n  2718:     ///\n  2719:     /// Because `parse` is so general, it can cause problems with type\n  2720:     /// inference. As such, `parse` is one of the few times you'll see\n  2721:     /// the syntax affectionately known as the 'turbofish': `::<>`. This\n  2722:     /// helps the inference algorithm understand specifically which type\n  2723:     /// you're trying to parse into.\n  2724:     ///\n  2725:     /// `parse` can parse into any type that implements the [`FromStr`] trait.\n  2726:     ///",
    "nanvix_source": "  2720:     ///\n  2721:     /// ```\n  2722:     /// assert_eq!(\"1fooX\".trim_right_matches(|c| c == '1' || c == 'X'), \"1foo\");\n  2723:     /// ```\n  2724:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2725:     #[deprecated(\n  2726:         since = \"1.33.0\",\n  2727:         note = \"superseded by `trim_end_matches`\",\n  2728:         suggestion = \"trim_end_matches\"\n  2729:     )]\n  2730:     pub fn trim_right_matches<P: Pattern>(&self, pat: P) -> &str\n  2731:     where\n  2732:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2733:     {\n  2734:         self.trim_end_matches(pat)\n  2735:     }\n  2736: \n  2737:     /// Parses this string slice into another type.\n  2738:     ///\n  2739:     /// Because `parse` is so general, it can cause problems with type\n  2740:     /// inference. As such, `parse` is one of the few times you'll see",
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
