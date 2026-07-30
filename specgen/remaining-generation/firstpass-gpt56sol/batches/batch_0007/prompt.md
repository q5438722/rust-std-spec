For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::strip_suffix",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "strip_suffix",
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
            "suffix",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "primitive": "str"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2451:     /// function or closure that determines if a character matches.\n  2452:     ///\n  2453:     /// [`char`]: prim@char\n  2454:     /// [pattern]: self::pattern\n  2455:     /// [`trim_end_matches`]: Self::trim_end_matches\n  2456:     ///\n  2457:     /// # Examples\n  2458:     ///\n  2459:     /// ```\n  2460:     /// assert_eq!(\"bar:foo\".strip_suffix(\":foo\"), Some(\"bar\"));\n  2461:     /// assert_eq!(\"bar:foo\".strip_suffix(\"bar\"), None);\n  2462:     /// assert_eq!(\"foofoo\".strip_suffix(\"foo\"), Some(\"foo\"));\n  2463:     /// ```\n  2464:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2465:                   without modifying the original\"]\n  2466:     #[stable(feature = \"str_strip\", since = \"1.45.0\")]\n  2467:     pub fn strip_suffix<P: Pattern>(&self, suffix: P) -> Option<&str>\n  2468:     where\n  2469:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2470:     {\n  2471:         suffix.strip_suffix_of(self)\n  2472:     }\n  2473: \n  2474:     /// Returns a string slice with the prefix and suffix removed.\n  2475:     ///\n  2476:     /// If the string starts with the pattern `prefix` and ends with the pattern `suffix`, returns\n  2477:     /// the substring after the prefix and before the suffix, wrapped in `Some`.\n  2478:     /// Unlike [`trim_start_matches`] and [`trim_end_matches`], this method removes both the prefix\n  2479:     /// and suffix exactly once.\n  2480:     ///\n  2481:     /// If the string does not start with `prefix` or does not end with `suffix`, returns `None`.\n  2482:     ///\n  2483:     /// Each [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
    "nanvix_source": "  2476:     /// # Examples\n  2477:     ///\n  2478:     /// ```\n  2479:     /// assert_eq!(\"bar:foo\".strip_suffix(\":foo\"), Some(\"bar\"));\n  2480:     /// assert_eq!(\"bar:foo\".strip_suffix(\"bar\"), None);\n  2481:     /// assert_eq!(\"foofoo\".strip_suffix(\"foo\"), Some(\"foo\"));\n  2482:     /// ```\n  2483:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2484:                   without modifying the original\"]\n  2485:     #[stable(feature = \"str_strip\", since = \"1.45.0\")]\n  2486:     pub fn strip_suffix<P: Pattern>(&self, suffix: P) -> Option<&str>\n  2487:     where\n  2488:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2489:     {\n  2490:         suffix.strip_suffix_of(self)\n  2491:     }\n  2492: \n  2493:     /// Returns a string slice with the prefix and suffix removed.\n  2494:     ///\n  2495:     /// If the string starts with the pattern `prefix` and ends with\n  2496:     /// the pattern `suffix`, and the prefix and suffix don't overlap, returns",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::trim_left_matches",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "trim_left_matches",
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
    "verification_source": "  2651:     ///\n  2652:     /// # Examples\n  2653:     ///\n  2654:     /// ```\n  2655:     /// assert_eq!(\"11foo1bar11\".trim_left_matches('1'), \"foo1bar11\");\n  2656:     /// assert_eq!(\"123foo1bar123\".trim_left_matches(char::is_numeric), \"foo1bar123\");\n  2657:     ///\n  2658:     /// let x: &[_] = &['1', '2'];\n  2659:     /// assert_eq!(\"12foo1bar12\".trim_left_matches(x), \"foo1bar12\");\n  2660:     /// ```\n  2661:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2662:     #[deprecated(\n  2663:         since = \"1.33.0\",\n  2664:         note = \"superseded by `trim_start_matches`\",\n  2665:         suggestion = \"trim_start_matches\"\n  2666:     )]\n  2667:     pub fn trim_left_matches<P: Pattern>(&self, pat: P) -> &str {\n  2668:         self.trim_start_matches(pat)\n  2669:     }\n  2670: \n  2671:     /// Returns a string slice with all suffixes that match a pattern\n  2672:     /// repeatedly removed.\n  2673:     ///\n  2674:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2675:     /// function or closure that determines if a character matches.\n  2676:     ///\n  2677:     /// [`char`]: prim@char\n  2678:     /// [pattern]: self::pattern\n  2679:     ///\n  2680:     /// # Text directionality\n  2681:     ///\n  2682:     /// A string is a sequence of bytes. 'Right' in this context means the last\n  2683:     /// position of that byte string; for a language like Arabic or Hebrew",
    "nanvix_source": "  2677:     ///\n  2678:     /// let x: &[_] = &['1', '2'];\n  2679:     /// assert_eq!(\"12foo1bar12\".trim_left_matches(x), \"foo1bar12\");\n  2680:     /// ```\n  2681:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2682:     #[deprecated(\n  2683:         since = \"1.33.0\",\n  2684:         note = \"superseded by `trim_start_matches`\",\n  2685:         suggestion = \"trim_start_matches\"\n  2686:     )]\n  2687:     pub fn trim_left_matches<P: Pattern>(&self, pat: P) -> &str {\n  2688:         self.trim_start_matches(pat)\n  2689:     }\n  2690: \n  2691:     /// Returns a string slice with all suffixes that match a pattern\n  2692:     /// repeatedly removed.\n  2693:     ///\n  2694:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2695:     /// function or closure that determines if a character matches.\n  2696:     ///\n  2697:     /// [`char`]: prim@char",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::trim_start_matches",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "trim_start_matches",
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
    "verification_source": "  2389:     /// position of that byte string; for a left-to-right language like English or\n  2390:     /// Russian, this will be left side, and for right-to-left languages like\n  2391:     /// Arabic or Hebrew, this will be the right side.\n  2392:     ///\n  2393:     /// # Examples\n  2394:     ///\n  2395:     /// ```\n  2396:     /// assert_eq!(\"11foo1bar11\".trim_start_matches('1'), \"foo1bar11\");\n  2397:     /// assert_eq!(\"123foo1bar123\".trim_start_matches(char::is_numeric), \"foo1bar123\");\n  2398:     ///\n  2399:     /// let x: &[_] = &['1', '2'];\n  2400:     /// assert_eq!(\"12foo1bar12\".trim_start_matches(x), \"foo1bar12\");\n  2401:     /// ```\n  2402:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2403:                   without modifying the original\"]\n  2404:     #[stable(feature = \"trim_direction\", since = \"1.30.0\")]\n  2405:     pub fn trim_start_matches<P: Pattern>(&self, pat: P) -> &str {\n  2406:         let mut i = self.len();\n  2407:         let mut matcher = pat.into_searcher(self);\n  2408:         if let Some((a, _)) = matcher.next_reject() {\n  2409:             i = a;\n  2410:         }\n  2411:         // SAFETY: `Searcher` is known to return valid indices.\n  2412:         unsafe { self.get_unchecked(i..self.len()) }\n  2413:     }\n  2414: \n  2415:     /// Returns a string slice with the prefix removed.\n  2416:     ///\n  2417:     /// If the string starts with the pattern `prefix`, returns the substring after the prefix,\n  2418:     /// wrapped in `Some`. Unlike [`trim_start_matches`], this method removes the prefix exactly once.\n  2419:     ///\n  2420:     /// If the string does not start with `prefix`, returns `None`.\n  2421:     ///",
    "nanvix_source": "  2414:     /// ```\n  2415:     /// assert_eq!(\"11foo1bar11\".trim_start_matches('1'), \"foo1bar11\");\n  2416:     /// assert_eq!(\"123foo1bar123\".trim_start_matches(char::is_numeric), \"foo1bar123\");\n  2417:     ///\n  2418:     /// let x: &[_] = &['1', '2'];\n  2419:     /// assert_eq!(\"12foo1bar12\".trim_start_matches(x), \"foo1bar12\");\n  2420:     /// ```\n  2421:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2422:                   without modifying the original\"]\n  2423:     #[stable(feature = \"trim_direction\", since = \"1.30.0\")]\n  2424:     pub fn trim_start_matches<P: Pattern>(&self, pat: P) -> &str {\n  2425:         let mut i = self.len();\n  2426:         let mut matcher = pat.into_searcher(self);\n  2427:         if let Some((a, _)) = matcher.next_reject() {\n  2428:             i = a;\n  2429:         }\n  2430:         // SAFETY: `Searcher` is known to return valid indices.\n  2431:         unsafe { self.get_unchecked(i..self.len()) }\n  2432:     }\n  2433: \n  2434:     /// Returns a string slice with the prefix removed.",
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
