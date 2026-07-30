For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::split_whitespace",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "split_whitespace",
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
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10135,
            "path": "SplitWhitespace"
          }
        }
      }
    },
    "verification_source": "  1178:     /// assert_eq!(Some(\"little\"), iter.next());\n  1179:     /// assert_eq!(Some(\"lamb\"), iter.next());\n  1180:     ///\n  1181:     /// assert_eq!(None, iter.next());\n  1182:     /// ```\n  1183:     ///\n  1184:     /// If the string is empty or all whitespace, the iterator yields no string slices:\n  1185:     /// ```\n  1186:     /// assert_eq!(\"\".split_whitespace().next(), None);\n  1187:     /// assert_eq!(\"   \".split_whitespace().next(), None);\n  1188:     /// ```\n  1189:     #[must_use = \"this returns the split string as an iterator, \\\n  1190:                   without modifying the original\"]\n  1191:     #[stable(feature = \"split_whitespace\", since = \"1.1.0\")]\n  1192:     #[rustc_diagnostic_item = \"str_split_whitespace\"]\n  1193:     #[inline]\n  1194:     pub fn split_whitespace(&self) -> SplitWhitespace<'_> {\n  1195:         SplitWhitespace { inner: self.split(IsWhitespace).filter(IsNotEmpty) }\n  1196:     }\n  1197: \n  1198:     /// Splits a string slice by ASCII whitespace.\n  1199:     ///\n  1200:     /// The iterator returned will return string slices that are sub-slices of\n  1201:     /// the original string slice, separated by any amount of ASCII whitespace.\n  1202:     ///\n  1203:     /// This uses the same definition as [`char::is_ascii_whitespace`].\n  1204:     /// To split by Unicode `Whitespace` instead, use [`split_whitespace`].\n  1205:     ///\n  1206:     /// [`split_whitespace`]: str::split_whitespace\n  1207:     ///\n  1208:     /// # Examples\n  1209:     ///\n  1210:     /// Basic usage:",
    "nanvix_source": "  1200:     /// If the string is empty or all whitespace, the iterator yields no string slices:\n  1201:     /// ```\n  1202:     /// assert_eq!(\"\".split_whitespace().next(), None);\n  1203:     /// assert_eq!(\"   \".split_whitespace().next(), None);\n  1204:     /// ```\n  1205:     #[must_use = \"this returns the split string as an iterator, \\\n  1206:                   without modifying the original\"]\n  1207:     #[stable(feature = \"split_whitespace\", since = \"1.1.0\")]\n  1208:     #[rustc_diagnostic_item = \"str_split_whitespace\"]\n  1209:     #[inline]\n  1210:     pub fn split_whitespace(&self) -> SplitWhitespace<'_> {\n  1211:         SplitWhitespace { inner: self.split(IsWhitespace).filter(IsNotEmpty) }\n  1212:     }\n  1213: \n  1214:     /// Splits a string slice by ASCII whitespace.\n  1215:     ///\n  1216:     /// The iterator returned will return string slices that are sub-slices of\n  1217:     /// the original string slice, separated by any amount of ASCII whitespace.\n  1218:     ///\n  1219:     /// This uses the same definition as [`char::is_ascii_whitespace`].\n  1220:     /// To split by Unicode `Whitespace` instead, use [`split_whitespace`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::splitn",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "splitn",
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
            "n",
            {
              "primitive": "usize"
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
            "id": 10112,
            "path": "SplitN"
          }
        }
      }
    },
    "verification_source": "  1881:     ///\n  1882:     /// let v: Vec<&str> = \"abcXdef\".splitn(1, 'X').collect();\n  1883:     /// assert_eq!(v, [\"abcXdef\"]);\n  1884:     ///\n  1885:     /// let v: Vec<&str> = \"\".splitn(1, 'X').collect();\n  1886:     /// assert_eq!(v, [\"\"]);\n  1887:     /// ```\n  1888:     ///\n  1889:     /// A more complex pattern, using a closure:\n  1890:     ///\n  1891:     /// ```\n  1892:     /// let v: Vec<&str> = \"abc1defXghi\".splitn(2, |c| c == '1' || c == 'X').collect();\n  1893:     /// assert_eq!(v, [\"abc\", \"defXghi\"]);\n  1894:     /// ```\n  1895:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1896:     #[inline]\n  1897:     pub fn splitn<P: Pattern>(&self, n: usize, pat: P) -> SplitN<'_, P> {\n  1898:         SplitN(SplitNInternal { iter: self.split(pat).0, count: n })\n  1899:     }\n  1900: \n  1901:     /// Returns an iterator over substrings of this string slice, separated by a\n  1902:     /// pattern, starting from the end of the string, restricted to returning at\n  1903:     /// most `n` items.\n  1904:     ///\n  1905:     /// If `n` substrings are returned, the last substring (the `n`th substring)\n  1906:     /// will contain the remainder of the string.\n  1907:     ///\n  1908:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1909:     /// function or closure that determines if a character matches.\n  1910:     ///\n  1911:     /// [`char`]: prim@char\n  1912:     /// [pattern]: self::pattern\n  1913:     ///",
    "nanvix_source": "  1906:     /// ```\n  1907:     ///\n  1908:     /// A more complex pattern, using a closure:\n  1909:     ///\n  1910:     /// ```\n  1911:     /// let v: Vec<&str> = \"abc1defXghi\".splitn(2, |c| c == '1' || c == 'X').collect();\n  1912:     /// assert_eq!(v, [\"abc\", \"defXghi\"]);\n  1913:     /// ```\n  1914:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1915:     #[inline]\n  1916:     pub fn splitn<P: Pattern>(&self, n: usize, pat: P) -> SplitN<'_, P> {\n  1917:         SplitN(SplitNInternal { iter: self.split(pat).0, count: n })\n  1918:     }\n  1919: \n  1920:     /// Returns an iterator over substrings of this string slice, separated by a\n  1921:     /// pattern, starting from the end of the string, restricted to returning at\n  1922:     /// most `n` items.\n  1923:     ///\n  1924:     /// If `n` substrings are returned, the last substring (the `n`th substring)\n  1925:     /// will contain the remainder of the string.\n  1926:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::drain",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "is_unsafe": false
      },
      "name": "drain",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
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
                          "id": 834,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 864,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "   755:     /// use std::collections::HashMap;\n   756:     ///\n   757:     /// let mut a = HashMap::new();\n   758:     /// a.insert(1, \"a\");\n   759:     /// a.insert(2, \"b\");\n   760:     ///\n   761:     /// for (k, v) in a.drain().take(1) {\n   762:     ///     assert!(k == 1 || k == 2);\n   763:     ///     assert!(v == \"a\" || v == \"b\");\n   764:     /// }\n   765:     ///\n   766:     /// assert!(a.is_empty());\n   767:     /// ```\n   768:     #[inline]\n   769:     #[rustc_lint_query_instability]\n   770:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n   771:     pub fn drain(&mut self) -> Drain<'_, K, V, A> {\n   772:         Drain { base: self.base.drain() }\n   773:     }\n   774: \n   775:     /// Creates an iterator which uses a closure to determine if an element (key-value pair) should be removed.\n   776:     ///\n   777:     /// If the closure returns `true`, the element is removed from the map and\n   778:     /// yielded. If the closure returns `false`, or panics, the element remains\n   779:     /// in the map and will not be yielded.\n   780:     ///\n   781:     /// The iterator also lets you mutate the value of each element in the\n   782:     /// closure, regardless of whether you choose to keep or remove it.\n   783:     ///\n   784:     /// If the returned `ExtractIf` is not exhausted, e.g. because it is dropped without iterating\n   785:     /// or the iteration short-circuits, then the remaining elements will be retained.\n   786:     /// Use [`retain`] with a negated predicate if you do not need the returned iterator.\n   787:     ///",
    "nanvix_source": "   766:     /// for (k, v) in a.drain().take(1) {\n   767:     ///     assert!(k == 1 || k == 2);\n   768:     ///     assert!(v == \"a\" || v == \"b\");\n   769:     /// }\n   770:     ///\n   771:     /// assert!(a.is_empty());\n   772:     /// ```\n   773:     #[inline]\n   774:     #[rustc_lint_query_instability]\n   775:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n   776:     pub fn drain(&mut self) -> Drain<'_, K, V, A> {\n   777:         Drain { base: self.base.drain() }\n   778:     }\n   779: \n   780:     /// Creates an iterator which uses a closure to determine if an element (key-value pair) should be removed.\n   781:     ///\n   782:     /// If the closure returns `true`, the element is removed from the map and\n   783:     /// yielded. If the closure returns `false`, or panics, the element remains\n   784:     /// in the map and will not be yielded.\n   785:     ///\n   786:     /// The iterator also lets you mutate the value of each element in the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::extract_if",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
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
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "K"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "V"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 18,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
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
      "name": "extract_if",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
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
                          "id": 834,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pred",
            {
              "generic": "F"
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
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 867,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "   795:     /// use std::collections::HashMap;\n   796:     ///\n   797:     /// let mut map: HashMap<i32, i32> = (0..8).map(|x| (x, x)).collect();\n   798:     /// let extracted: HashMap<i32, i32> = map.extract_if(|k, _v| k % 2 == 0).collect();\n   799:     ///\n   800:     /// let mut evens = extracted.keys().copied().collect::<Vec<_>>();\n   801:     /// let mut odds = map.keys().copied().collect::<Vec<_>>();\n   802:     /// evens.sort();\n   803:     /// odds.sort();\n   804:     ///\n   805:     /// assert_eq!(evens, vec![0, 2, 4, 6]);\n   806:     /// assert_eq!(odds, vec![1, 3, 5, 7]);\n   807:     /// ```\n   808:     #[inline]\n   809:     #[rustc_lint_query_instability]\n   810:     #[stable(feature = \"hash_extract_if\", since = \"1.88.0\")]\n   811:     pub fn extract_if<F>(&mut self, pred: F) -> ExtractIf<'_, K, V, F, A>\n   812:     where\n   813:         F: FnMut(&K, &mut V) -> bool,\n   814:     {\n   815:         ExtractIf { base: self.base.extract_if(pred) }\n   816:     }\n   817: \n   818:     /// Retains only the elements specified by the predicate.\n   819:     ///\n   820:     /// In other words, remove all pairs `(k, v)` for which `f(&k, &mut v)` returns `false`.\n   821:     /// The elements are visited in unsorted (and unspecified) order.\n   822:     ///\n   823:     /// # Examples\n   824:     ///\n   825:     /// ```\n   826:     /// use std::collections::HashMap;\n   827:     ///",
    "nanvix_source": "   806:     /// let mut odds = map.keys().copied().collect::<Vec<_>>();\n   807:     /// evens.sort();\n   808:     /// odds.sort();\n   809:     ///\n   810:     /// assert_eq!(evens, vec![0, 2, 4, 6]);\n   811:     /// assert_eq!(odds, vec![1, 3, 5, 7]);\n   812:     /// ```\n   813:     #[inline]\n   814:     #[rustc_lint_query_instability]\n   815:     #[stable(feature = \"hash_extract_if\", since = \"1.88.0\")]\n   816:     pub fn extract_if<F>(&mut self, pred: F) -> ExtractIf<'_, K, V, F, A>\n   817:     where\n   818:         F: FnMut(&K, &mut V) -> bool,\n   819:     {\n   820:         ExtractIf { base: self.base.extract_if(pred) }\n   821:     }\n   822: \n   823:     /// Retains only the elements specified by the predicate.\n   824:     ///\n   825:     /// In other words, remove all pairs `(k, v)` for which `f(&k, &mut v)` returns `false`.\n   826:     /// The elements are visited in unsorted (and unspecified) order.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::into_keys",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "is_unsafe": false
      },
      "name": "into_keys",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
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
                          "id": 834,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 850,
            "path": "IntoKeys"
          }
        }
      }
    },
    "verification_source": "   531:     /// ]);\n   532:     ///\n   533:     /// let mut vec: Vec<&str> = map.into_keys().collect();\n   534:     /// // The `IntoKeys` iterator produces keys in arbitrary order, so the\n   535:     /// // keys must be sorted to test them against a sorted array.\n   536:     /// vec.sort_unstable();\n   537:     /// assert_eq!(vec, [\"a\", \"b\", \"c\"]);\n   538:     /// ```\n   539:     ///\n   540:     /// # Performance\n   541:     ///\n   542:     /// In the current implementation, iterating over keys takes O(capacity) time\n   543:     /// instead of O(len) because it internally visits empty buckets too.\n   544:     #[inline]\n   545:     #[rustc_lint_query_instability]\n   546:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n   547:     pub fn into_keys(self) -> IntoKeys<K, V, A> {\n   548:         IntoKeys { inner: self.into_iter() }\n   549:     }\n   550: \n   551:     /// An iterator visiting all values in arbitrary order.\n   552:     /// The iterator element type is `&'a V`.\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```\n   557:     /// use std::collections::HashMap;\n   558:     ///\n   559:     /// let map = HashMap::from([\n   560:     ///     (\"a\", 1),\n   561:     ///     (\"b\", 2),\n   562:     ///     (\"c\", 3),\n   563:     /// ]);",
    "nanvix_source": "   537:     /// assert_eq!(vec, [\"a\", \"b\", \"c\"]);\n   538:     /// ```\n   539:     ///\n   540:     /// # Performance\n   541:     ///\n   542:     /// In the current implementation, iterating over keys takes O(capacity) time\n   543:     /// instead of O(len) because it internally visits empty buckets too.\n   544:     #[inline]\n   545:     #[rustc_lint_query_instability]\n   546:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n   547:     pub fn into_keys(self) -> IntoKeys<K, V, A> {\n   548:         IntoKeys { inner: self.into_iter() }\n   549:     }\n   550: \n   551:     /// An iterator visiting all values in arbitrary order.\n   552:     /// The iterator element type is `&'a V`.\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```\n   557:     /// use std::collections::HashMap;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::into_values",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "is_unsafe": false
      },
      "name": "into_values",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
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
                          "id": 834,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 856,
            "path": "IntoValues"
          }
        }
      }
    },
    "verification_source": "   626:     /// ]);\n   627:     ///\n   628:     /// let mut vec: Vec<i32> = map.into_values().collect();\n   629:     /// // The `IntoValues` iterator produces values in arbitrary order, so\n   630:     /// // the values must be sorted to test them against a sorted array.\n   631:     /// vec.sort_unstable();\n   632:     /// assert_eq!(vec, [1, 2, 3]);\n   633:     /// ```\n   634:     ///\n   635:     /// # Performance\n   636:     ///\n   637:     /// In the current implementation, iterating over values takes O(capacity) time\n   638:     /// instead of O(len) because it internally visits empty buckets too.\n   639:     #[inline]\n   640:     #[rustc_lint_query_instability]\n   641:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n   642:     pub fn into_values(self) -> IntoValues<K, V, A> {\n   643:         IntoValues { inner: self.into_iter() }\n   644:     }\n   645: \n   646:     /// An iterator visiting all key-value pairs in arbitrary order.\n   647:     /// The iterator element type is `(&'a K, &'a V)`.\n   648:     ///\n   649:     /// # Examples\n   650:     ///\n   651:     /// ```\n   652:     /// use std::collections::HashMap;\n   653:     ///\n   654:     /// let map = HashMap::from([\n   655:     ///     (\"a\", 1),\n   656:     ///     (\"b\", 2),\n   657:     ///     (\"c\", 3),\n   658:     /// ]);",
    "nanvix_source": "   633:     /// assert_eq!(vec, [1, 2, 3]);\n   634:     /// ```\n   635:     ///\n   636:     /// # Performance\n   637:     ///\n   638:     /// In the current implementation, iterating over values takes O(capacity) time\n   639:     /// instead of O(len) because it internally visits empty buckets too.\n   640:     #[inline]\n   641:     #[rustc_lint_query_instability]\n   642:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n   643:     pub fn into_values(self) -> IntoValues<K, V, A> {\n   644:         IntoValues { inner: self.into_iter() }\n   645:     }\n   646: \n   647:     /// An iterator visiting all key-value pairs in arbitrary order.\n   648:     /// The iterator element type is `(&'a K, &'a V)`.\n   649:     ///\n   650:     /// # Examples\n   651:     ///\n   652:     /// ```\n   653:     /// use std::collections::HashMap;",
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
