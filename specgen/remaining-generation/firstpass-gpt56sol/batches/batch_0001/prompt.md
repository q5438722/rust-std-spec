For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::get",
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
                      "modifier": "maybe_const",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "primitive": "str"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9549,
                        "path": "SliceIndex"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "get",
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
            "i",
            {
              "generic": "I"
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
                          "qualified_path": {
                            "args": null,
                            "name": "Output",
                            "self_type": {
                              "generic": "I"
                            },
                            "trait": {
                              "args": null,
                              "id": 9549,
                              "path": ""
                            }
                          }
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
    "verification_source": "   602:     ///\n   603:     /// ```\n   604:     /// let v = String::from(\"\ud83d\uddfb\u2208\ud83c\udf0f\");\n   605:     ///\n   606:     /// assert_eq!(Some(\"\ud83d\uddfb\"), v.get(0..4));\n   607:     ///\n   608:     /// // indices not on UTF-8 sequence boundaries\n   609:     /// assert!(v.get(1..).is_none());\n   610:     /// assert!(v.get(..8).is_none());\n   611:     ///\n   612:     /// // out of bounds\n   613:     /// assert!(v.get(..42).is_none());\n   614:     /// ```\n   615:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   616:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   617:     #[inline]\n   618:     pub const fn get<I: [const] SliceIndex<str>>(&self, i: I) -> Option<&I::Output> {\n   619:         i.get(self)\n   620:     }\n   621: \n   622:     /// Returns a mutable subslice of `str`.\n   623:     ///\n   624:     /// This is the non-panicking alternative to indexing the `str`. Returns\n   625:     /// [`None`] whenever equivalent indexing operation would panic.\n   626:     ///\n   627:     /// # Examples\n   628:     ///\n   629:     /// ```\n   630:     /// let mut v = String::from(\"hello\");\n   631:     /// // correct length\n   632:     /// assert!(v.get_mut(0..5).is_some());\n   633:     /// // out of bounds\n   634:     /// assert!(v.get_mut(..42).is_none());",
    "nanvix_source": "   624:     /// // indices not on UTF-8 sequence boundaries\n   625:     /// assert!(v.get(1..).is_none());\n   626:     /// assert!(v.get(..8).is_none());\n   627:     ///\n   628:     /// // out of bounds\n   629:     /// assert!(v.get(..42).is_none());\n   630:     /// ```\n   631:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   632:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   633:     #[inline]\n   634:     pub const fn get<I: [const] SliceIndex<str>>(&self, i: I) -> Option<&I::Output> {\n   635:         i.get(self)\n   636:     }\n   637: \n   638:     /// Returns a mutable subslice of `str`.\n   639:     ///\n   640:     /// This is the non-panicking alternative to indexing the `str`. Returns\n   641:     /// [`None`] whenever equivalent indexing operation would panic.\n   642:     ///\n   643:     /// # Examples\n   644:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::parse",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
                        "id": 941,
                        "path": "FromStr"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
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
      "name": "parse",
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
                      "generic": "F"
                    }
                  },
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "Err",
                        "self_type": {
                          "generic": "F"
                        },
                        "trait": {
                          "args": null,
                          "id": 941,
                          "path": ""
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2745:     ///\n  2746:     /// ```\n  2747:     /// let four = \"4\".parse::<u32>();\n  2748:     ///\n  2749:     /// assert_eq!(Ok(4), four);\n  2750:     /// ```\n  2751:     ///\n  2752:     /// Failing to parse:\n  2753:     ///\n  2754:     /// ```\n  2755:     /// let nope = \"j\".parse::<u32>();\n  2756:     ///\n  2757:     /// assert!(nope.is_err());\n  2758:     /// ```\n  2759:     #[inline]\n  2760:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2761:     pub fn parse<F: FromStr>(&self) -> Result<F, F::Err> {\n  2762:         FromStr::from_str(self)\n  2763:     }\n  2764: \n  2765:     /// Checks if all characters in this string are within the ASCII range.\n  2766:     ///\n  2767:     /// An empty string returns `true`.\n  2768:     ///\n  2769:     /// # Examples\n  2770:     ///\n  2771:     /// ```\n  2772:     /// let ascii = \"hello!\\n\";\n  2773:     /// let non_ascii = \"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\";\n  2774:     ///\n  2775:     /// assert!(ascii.is_ascii());\n  2776:     /// assert!(!non_ascii.is_ascii());\n  2777:     /// ```",
    "nanvix_source": "  2771:     ///\n  2772:     /// Failing to parse:\n  2773:     ///\n  2774:     /// ```\n  2775:     /// let nope = \"j\".parse::<u32>();\n  2776:     ///\n  2777:     /// assert!(nope.is_err());\n  2778:     /// ```\n  2779:     #[inline]\n  2780:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2781:     pub fn parse<F: FromStr>(&self) -> Result<F, F::Err> {\n  2782:         FromStr::from_str(self)\n  2783:     }\n  2784: \n  2785:     /// Checks if all characters in this string are within the ASCII range.\n  2786:     ///\n  2787:     /// An empty string returns `true`.\n  2788:     ///\n  2789:     /// # Examples\n  2790:     ///\n  2791:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rfind",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
      "name": "rfind",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
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
    "verification_source": "  1507:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n  1508:     ///\n  1509:     /// assert_eq!(s.rfind(char::is_whitespace), Some(12));\n  1510:     /// assert_eq!(s.rfind(char::is_lowercase), Some(20));\n  1511:     /// ```\n  1512:     ///\n  1513:     /// Not finding the pattern:\n  1514:     ///\n  1515:     /// ```\n  1516:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n  1517:     /// let x: &[_] = &['1', '2'];\n  1518:     ///\n  1519:     /// assert_eq!(s.rfind(x), None);\n  1520:     /// ```\n  1521:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1522:     #[inline]\n  1523:     pub fn rfind<P: Pattern>(&self, pat: P) -> Option<usize>\n  1524:     where\n  1525:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1526:     {\n  1527:         pat.into_searcher(self).next_match_back().map(|(i, _)| i)\n  1528:     }\n  1529: \n  1530:     /// Returns an iterator over substrings of this string slice, separated by\n  1531:     /// characters matched by a pattern.\n  1532:     ///\n  1533:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1534:     /// function or closure that determines if a character matches.\n  1535:     ///\n  1536:     /// If there are no matches the full string slice is returned as the only\n  1537:     /// item in the iterator.\n  1538:     ///\n  1539:     /// [`char`]: prim@char",
    "nanvix_source": "  1532:     /// Not finding the pattern:\n  1533:     ///\n  1534:     /// ```\n  1535:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n  1536:     /// let x: &[_] = &['1', '2'];\n  1537:     ///\n  1538:     /// assert_eq!(s.rfind(x), None);\n  1539:     /// ```\n  1540:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1541:     #[inline]\n  1542:     pub fn rfind<P: Pattern>(&self, pat: P) -> Option<usize>\n  1543:     where\n  1544:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1545:     {\n  1546:         pat.into_searcher(self).next_match_back().map(|(i, _)| i)\n  1547:     }\n  1548: \n  1549:     /// Returns an iterator over substrings of this string slice, separated by\n  1550:     /// characters matched by a pattern.\n  1551:     ///\n  1552:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rmatch_indices",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
      "name": "rmatch_indices",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10121,
            "path": "RMatchIndices"
          }
        }
      }
    },
    "verification_source": "  2127:     /// [`match_indices`]: str::match_indices\n  2128:     ///\n  2129:     /// # Examples\n  2130:     ///\n  2131:     /// ```\n  2132:     /// let v: Vec<_> = \"abcXXXabcYYYabc\".rmatch_indices(\"abc\").collect();\n  2133:     /// assert_eq!(v, [(12, \"abc\"), (6, \"abc\"), (0, \"abc\")]);\n  2134:     ///\n  2135:     /// let v: Vec<_> = \"1abcabc2\".rmatch_indices(\"abc\").collect();\n  2136:     /// assert_eq!(v, [(4, \"abc\"), (1, \"abc\")]);\n  2137:     ///\n  2138:     /// let v: Vec<_> = \"ababa\".rmatch_indices(\"aba\").collect();\n  2139:     /// assert_eq!(v, [(2, \"aba\")]); // only the last `aba`\n  2140:     /// ```\n  2141:     #[stable(feature = \"str_match_indices\", since = \"1.5.0\")]\n  2142:     #[inline]\n  2143:     pub fn rmatch_indices<P: Pattern>(&self, pat: P) -> RMatchIndices<'_, P>\n  2144:     where\n  2145:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2146:     {\n  2147:         RMatchIndices(self.match_indices(pat).0)\n  2148:     }\n  2149: \n  2150:     /// Returns a string slice with leading and trailing whitespace removed.\n  2151:     ///\n  2152:     /// 'Whitespace' is defined according to the terms of the Unicode Derived\n  2153:     /// Core Property `White_Space`, which includes newlines.\n  2154:     ///\n  2155:     /// # Examples\n  2156:     ///\n  2157:     /// ```\n  2158:     /// let s = \"\\n Hello\\tworld\\t\\n\";\n  2159:     ///",
    "nanvix_source": "  2152:     /// assert_eq!(v, [(12, \"abc\"), (6, \"abc\"), (0, \"abc\")]);\n  2153:     ///\n  2154:     /// let v: Vec<_> = \"1abcabc2\".rmatch_indices(\"abc\").collect();\n  2155:     /// assert_eq!(v, [(4, \"abc\"), (1, \"abc\")]);\n  2156:     ///\n  2157:     /// let v: Vec<_> = \"ababa\".rmatch_indices(\"aba\").collect();\n  2158:     /// assert_eq!(v, [(2, \"aba\")]); // only the last `aba`\n  2159:     /// ```\n  2160:     #[stable(feature = \"str_match_indices\", since = \"1.5.0\")]\n  2161:     #[inline]\n  2162:     pub fn rmatch_indices<P: Pattern>(&self, pat: P) -> RMatchIndices<'_, P>\n  2163:     where\n  2164:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2165:     {\n  2166:         RMatchIndices(self.match_indices(pat).0)\n  2167:     }\n  2168: \n  2169:     /// Returns a string slice with leading and trailing whitespace removed.\n  2170:     ///\n  2171:     /// 'Whitespace' is defined according to the terms of the Unicode Derived\n  2172:     /// Core Property `White_Space`, which includes newlines.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rmatches",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
      "name": "rmatches",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10127,
            "path": "RMatches"
          }
        }
      }
    },
    "verification_source": "  2043:     ///\n  2044:     /// For iterating from the front, the [`matches`] method can be used.\n  2045:     ///\n  2046:     /// [`matches`]: str::matches\n  2047:     ///\n  2048:     /// # Examples\n  2049:     ///\n  2050:     /// ```\n  2051:     /// let v: Vec<&str> = \"abcXXXabcYYYabc\".rmatches(\"abc\").collect();\n  2052:     /// assert_eq!(v, [\"abc\", \"abc\", \"abc\"]);\n  2053:     ///\n  2054:     /// let v: Vec<&str> = \"1abc2abc3\".rmatches(char::is_numeric).collect();\n  2055:     /// assert_eq!(v, [\"3\", \"2\", \"1\"]);\n  2056:     /// ```\n  2057:     #[stable(feature = \"str_matches\", since = \"1.2.0\")]\n  2058:     #[inline]\n  2059:     pub fn rmatches<P: Pattern>(&self, pat: P) -> RMatches<'_, P>\n  2060:     where\n  2061:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2062:     {\n  2063:         RMatches(self.matches(pat).0)\n  2064:     }\n  2065: \n  2066:     /// Returns an iterator over the disjoint matches of a pattern within this string\n  2067:     /// slice as well as the index that the match starts at.\n  2068:     ///\n  2069:     /// For matches of `pat` within `self` that overlap, only the indices\n  2070:     /// corresponding to the first match are returned.\n  2071:     ///\n  2072:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2073:     /// function or closure that determines if a character matches.\n  2074:     ///\n  2075:     /// [`char`]: prim@char",
    "nanvix_source": "  2068:     ///\n  2069:     /// ```\n  2070:     /// let v: Vec<&str> = \"abcXXXabcYYYabc\".rmatches(\"abc\").collect();\n  2071:     /// assert_eq!(v, [\"abc\", \"abc\", \"abc\"]);\n  2072:     ///\n  2073:     /// let v: Vec<&str> = \"1abc2abc3\".rmatches(char::is_numeric).collect();\n  2074:     /// assert_eq!(v, [\"3\", \"2\", \"1\"]);\n  2075:     /// ```\n  2076:     #[stable(feature = \"str_matches\", since = \"1.2.0\")]\n  2077:     #[inline]\n  2078:     pub fn rmatches<P: Pattern>(&self, pat: P) -> RMatches<'_, P>\n  2079:     where\n  2080:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2081:     {\n  2082:         RMatches(self.matches(pat).0)\n  2083:     }\n  2084: \n  2085:     /// Returns an iterator over the disjoint matches of a pattern within this string\n  2086:     /// slice as well as the index that the match starts at.\n  2087:     ///\n  2088:     /// For matches of `pat` within `self` that overlap, only the indices",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rsplit",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
      "name": "rsplit",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10103,
            "path": "RSplit"
          }
        }
      }
    },
    "verification_source": "  1731:     ///\n  1732:     /// let v: Vec<&str> = \"lionXXtigerXleopard\".rsplit('X').collect();\n  1733:     /// assert_eq!(v, [\"leopard\", \"tiger\", \"\", \"lion\"]);\n  1734:     ///\n  1735:     /// let v: Vec<&str> = \"lion::tiger::leopard\".rsplit(\"::\").collect();\n  1736:     /// assert_eq!(v, [\"leopard\", \"tiger\", \"lion\"]);\n  1737:     /// ```\n  1738:     ///\n  1739:     /// A more complex pattern, using a closure:\n  1740:     ///\n  1741:     /// ```\n  1742:     /// let v: Vec<&str> = \"abc1defXghi\".rsplit(|c| c == '1' || c == 'X').collect();\n  1743:     /// assert_eq!(v, [\"ghi\", \"def\", \"abc\"]);\n  1744:     /// ```\n  1745:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1746:     #[inline]\n  1747:     pub fn rsplit<P: Pattern>(&self, pat: P) -> RSplit<'_, P>\n  1748:     where\n  1749:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1750:     {\n  1751:         RSplit(self.split(pat).0)\n  1752:     }\n  1753: \n  1754:     /// Returns an iterator over substrings of the given string slice, separated\n  1755:     /// by characters matched by a pattern.\n  1756:     ///\n  1757:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1758:     /// function or closure that determines if a character matches.\n  1759:     ///\n  1760:     /// [`char`]: prim@char\n  1761:     /// [pattern]: self::pattern\n  1762:     ///\n  1763:     /// Equivalent to [`split`], except that the trailing substring",
    "nanvix_source": "  1756:     /// ```\n  1757:     ///\n  1758:     /// A more complex pattern, using a closure:\n  1759:     ///\n  1760:     /// ```\n  1761:     /// let v: Vec<&str> = \"abc1defXghi\".rsplit(|c| c == '1' || c == 'X').collect();\n  1762:     /// assert_eq!(v, [\"ghi\", \"def\", \"abc\"]);\n  1763:     /// ```\n  1764:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1765:     #[inline]\n  1766:     pub fn rsplit<P: Pattern>(&self, pat: P) -> RSplit<'_, P>\n  1767:     where\n  1768:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1769:     {\n  1770:         RSplit(self.split(pat).0)\n  1771:     }\n  1772: \n  1773:     /// Returns an iterator over substrings of the given string slice, separated\n  1774:     /// by characters matched by a pattern.\n  1775:     ///\n  1776:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
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
