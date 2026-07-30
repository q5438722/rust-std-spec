For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashMap::iter_mut",
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
      "name": "iter_mut",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 860,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "   690:     /// // Update all values\n   691:     /// for (_, val) in map.iter_mut() {\n   692:     ///     *val *= 2;\n   693:     /// }\n   694:     ///\n   695:     /// for (key, val) in &map {\n   696:     ///     println!(\"key: {key} val: {val}\");\n   697:     /// }\n   698:     /// ```\n   699:     ///\n   700:     /// # Performance\n   701:     ///\n   702:     /// In the current implementation, iterating over map takes O(capacity) time\n   703:     /// instead of O(len) because it internally visits empty buckets too.\n   704:     #[rustc_lint_query_instability]\n   705:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   706:     pub fn iter_mut(&mut self) -> IterMut<'_, K, V> {\n   707:         IterMut { base: self.base.iter_mut() }\n   708:     }\n   709: \n   710:     /// Returns the number of elements in the map.\n   711:     ///\n   712:     /// # Examples\n   713:     ///\n   714:     /// ```\n   715:     /// use std::collections::HashMap;\n   716:     ///\n   717:     /// let mut a = HashMap::new();\n   718:     /// assert_eq!(a.len(), 0);\n   719:     /// a.insert(1, \"a\");\n   720:     /// assert_eq!(a.len(), 1);\n   721:     /// ```\n   722:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   701:     /// assert_eq!(map.get(\"b\"), Some(&4));\n   702:     /// assert_eq!(map.get(\"c\"), Some(&6));\n   703:     /// ```\n   704:     ///\n   705:     /// # Performance\n   706:     ///\n   707:     /// In the current implementation, iterating over map takes O(capacity) time\n   708:     /// instead of O(len) because it internally visits empty buckets too.\n   709:     #[rustc_lint_query_instability]\n   710:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   711:     pub fn iter_mut(&mut self) -> IterMut<'_, K, V> {\n   712:         IterMut { base: self.base.iter_mut() }\n   713:     }\n   714: \n   715:     /// Returns the number of elements in the map.\n   716:     ///\n   717:     /// # Examples\n   718:     ///\n   719:     /// ```\n   720:     /// use std::collections::HashMap;\n   721:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::retain",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
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
      "name": "retain",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   824:     ///\n   825:     /// ```\n   826:     /// use std::collections::HashMap;\n   827:     ///\n   828:     /// let mut map: HashMap<i32, i32> = (0..8).map(|x| (x, x*10)).collect();\n   829:     /// map.retain(|&k, _| k % 2 == 0);\n   830:     /// assert_eq!(map.len(), 4);\n   831:     /// ```\n   832:     ///\n   833:     /// # Performance\n   834:     ///\n   835:     /// In the current implementation, this operation takes O(capacity) time\n   836:     /// instead of O(len) because it internally visits empty buckets too.\n   837:     #[inline]\n   838:     #[rustc_lint_query_instability]\n   839:     #[stable(feature = \"retain_hash_collection\", since = \"1.18.0\")]\n   840:     pub fn retain<F>(&mut self, f: F)\n   841:     where\n   842:         F: FnMut(&K, &mut V) -> bool,\n   843:     {\n   844:         self.base.retain(f)\n   845:     }\n   846: \n   847:     /// Clears the map, removing all key-value pairs. Keeps the allocated memory\n   848:     /// for reuse.\n   849:     ///\n   850:     /// # Examples\n   851:     ///\n   852:     /// ```\n   853:     /// use std::collections::HashMap;\n   854:     ///\n   855:     /// let mut a = HashMap::new();\n   856:     /// a.insert(1, \"a\");",
    "nanvix_source": "   835:     /// assert_eq!(map.len(), 4);\n   836:     /// ```\n   837:     ///\n   838:     /// # Performance\n   839:     ///\n   840:     /// In the current implementation, this operation takes O(capacity) time\n   841:     /// instead of O(len) because it internally visits empty buckets too.\n   842:     #[inline]\n   843:     #[rustc_lint_query_instability]\n   844:     #[stable(feature = \"retain_hash_collection\", since = \"1.18.0\")]\n   845:     pub fn retain<F>(&mut self, f: F)\n   846:     where\n   847:         F: FnMut(&K, &mut V) -> bool,\n   848:     {\n   849:         self.base.retain(f)\n   850:     }\n   851: \n   852:     /// Clears the map, removing all key-value pairs. Keeps the allocated memory\n   853:     /// for reuse.\n   854:     ///\n   855:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::values_mut",
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
      "name": "values_mut",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 854,
            "path": "ValuesMut"
          }
        }
      }
    },
    "verification_source": "   593:     ///\n   594:     /// for val in map.values_mut() {\n   595:     ///     *val = *val + 10;\n   596:     /// }\n   597:     ///\n   598:     /// for val in map.values() {\n   599:     ///     println!(\"{val}\");\n   600:     /// }\n   601:     /// ```\n   602:     ///\n   603:     /// # Performance\n   604:     ///\n   605:     /// In the current implementation, iterating over values takes O(capacity) time\n   606:     /// instead of O(len) because it internally visits empty buckets too.\n   607:     #[rustc_lint_query_instability]\n   608:     #[stable(feature = \"map_values_mut\", since = \"1.10.0\")]\n   609:     pub fn values_mut(&mut self) -> ValuesMut<'_, K, V> {\n   610:         ValuesMut { inner: self.iter_mut() }\n   611:     }\n   612: \n   613:     /// Creates a consuming iterator visiting all the values in arbitrary order.\n   614:     /// The map cannot be used after calling this.\n   615:     /// The iterator element type is `V`.\n   616:     ///\n   617:     /// # Examples\n   618:     ///\n   619:     /// ```\n   620:     /// use std::collections::HashMap;\n   621:     ///\n   622:     /// let map = HashMap::from([\n   623:     ///     (\"a\", 1),\n   624:     ///     (\"b\", 2),\n   625:     ///     (\"c\", 3),",
    "nanvix_source": "   600:     /// assert_eq!(map.get(\"b\"), Some(&12));\n   601:     /// assert_eq!(map.get(\"c\"), Some(&13));\n   602:     /// ```\n   603:     ///\n   604:     /// # Performance\n   605:     ///\n   606:     /// In the current implementation, iterating over values takes O(capacity) time\n   607:     /// instead of O(len) because it internally visits empty buckets too.\n   608:     #[rustc_lint_query_instability]\n   609:     #[stable(feature = \"map_values_mut\", since = \"1.10.0\")]\n   610:     pub fn values_mut(&mut self) -> ValuesMut<'_, K, V> {\n   611:         ValuesMut { inner: self.iter_mut() }\n   612:     }\n   613: \n   614:     /// Creates a consuming iterator visiting all the values in arbitrary order.\n   615:     /// The map cannot be used after calling this.\n   616:     /// The iterator element type is `V`.\n   617:     ///\n   618:     /// # Examples\n   619:     ///\n   620:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::difference",
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
      "name": "difference",
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
                      "generic": "T"
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
            "id": 1347,
            "path": "HashSet"
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
              "name": "T"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "args": null,
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "T"
                }
              }
            },
            {
              "bound_predicate": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
                }
              }
            },
            {
              "bound_predicate": {
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
                "generic_params": [],
                "type": {
                  "generic": "A"
                }
              }
            }
          ]
        },
        "impl_id": "std:1397",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1347",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "set",
          "HashSet"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": "'a",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "other",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": "'a",
                "type": {
                  "resolved_path": {
                    "args": {
                      "angle_bracketed": {
                        "args": [
                          {
                            "type": {
                              "generic": "T"
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
                    "id": 1347,
                    "path": "HashSet"
                  }
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
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
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
            "id": 1377,
            "path": "Difference"
          }
        }
      }
    },
    "verification_source": "   674:     /// // Can be seen as `a - b`.\n   675:     /// for x in a.difference(&b) {\n   676:     ///     println!(\"{x}\"); // Print 1\n   677:     /// }\n   678:     ///\n   679:     /// let diff: HashSet<_> = a.difference(&b).collect();\n   680:     /// assert_eq!(diff, [1].iter().collect());\n   681:     ///\n   682:     /// // Note that difference is not symmetric,\n   683:     /// // and `b - a` means something else:\n   684:     /// let diff: HashSet<_> = b.difference(&a).collect();\n   685:     /// assert_eq!(diff, [4].iter().collect());\n   686:     /// ```\n   687:     #[inline]\n   688:     #[rustc_lint_query_instability]\n   689:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   690:     pub fn difference<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Difference<'a, T, S, A> {\n   691:         Difference { iter: self.iter(), other }\n   692:     }\n   693: \n   694:     /// Visits the values representing the symmetric difference,\n   695:     /// i.e., the values that are in `self` or in `other` but not in both.\n   696:     ///\n   697:     /// # Examples\n   698:     ///\n   699:     /// ```\n   700:     /// use std::collections::HashSet;\n   701:     /// let a = HashSet::from([1, 2, 3]);\n   702:     /// let b = HashSet::from([4, 2, 3, 4]);\n   703:     ///\n   704:     /// // Print 1, 4 in arbitrary order.\n   705:     /// for x in a.symmetric_difference(&b) {\n   706:     ///     println!(\"{x}\");",
    "nanvix_source": "   680:     /// assert_eq!(diff, [1].iter().collect());\n   681:     ///\n   682:     /// // Note that difference is not symmetric,\n   683:     /// // and `b - a` means something else:\n   684:     /// let diff: HashSet<_> = b.difference(&a).collect();\n   685:     /// assert_eq!(diff, [4].iter().collect());\n   686:     /// ```\n   687:     #[inline]\n   688:     #[rustc_lint_query_instability]\n   689:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   690:     pub fn difference<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Difference<'a, T, S, A> {\n   691:         Difference { iter: self.iter(), other }\n   692:     }\n   693: \n   694:     /// Visits the values representing the symmetric difference,\n   695:     /// i.e., the values that are in `self` or in `other` but not in both.\n   696:     ///\n   697:     /// # Examples\n   698:     ///\n   699:     /// ```\n   700:     /// use std::collections::HashSet;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::drain",
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
                      "generic": "T"
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
            "id": 1347,
            "path": "HashSet"
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
              "name": "T"
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
        "impl_id": "std:1371",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1347",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "set",
          "HashSet"
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
                      "generic": "T"
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
            "id": 1365,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "   437:     /// ```\n   438:     /// use std::collections::HashSet;\n   439:     ///\n   440:     /// let mut set = HashSet::from([1, 2, 3]);\n   441:     /// assert!(!set.is_empty());\n   442:     ///\n   443:     /// // print 1, 2, 3 in an arbitrary order\n   444:     /// for i in set.drain() {\n   445:     ///     println!(\"{i}\");\n   446:     /// }\n   447:     ///\n   448:     /// assert!(set.is_empty());\n   449:     /// ```\n   450:     #[inline]\n   451:     #[rustc_lint_query_instability]\n   452:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n   453:     pub fn drain(&mut self) -> Drain<'_, T, A> {\n   454:         Drain { base: self.base.drain() }\n   455:     }\n   456: \n   457:     /// Creates an iterator which uses a closure to determine if an element should be removed.\n   458:     ///\n   459:     /// If the closure returns `true`, the element is removed from the set and\n   460:     /// yielded. If the closure returns `false`, or panics, the element remains\n   461:     /// in the set and will not be yielded.\n   462:     ///\n   463:     /// If the returned `ExtractIf` is not exhausted, e.g. because it is dropped without iterating\n   464:     /// or the iteration short-circuits, then the remaining elements will be retained.\n   465:     /// Use [`retain`] with a negated predicate if you do not need the returned iterator.\n   466:     ///\n   467:     /// [`retain`]: HashSet::retain\n   468:     ///\n   469:     /// # Examples",
    "nanvix_source": "   443:     /// // print 1, 2, 3 in an arbitrary order\n   444:     /// for i in set.drain() {\n   445:     ///     println!(\"{i}\");\n   446:     /// }\n   447:     ///\n   448:     /// assert!(set.is_empty());\n   449:     /// ```\n   450:     #[inline]\n   451:     #[rustc_lint_query_instability]\n   452:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n   453:     pub fn drain(&mut self) -> Drain<'_, T, A> {\n   454:         Drain { base: self.base.drain() }\n   455:     }\n   456: \n   457:     /// Creates an iterator which uses a closure to determine if an element should be removed.\n   458:     ///\n   459:     /// If the closure returns `true`, the element is removed from the set and\n   460:     /// yielded. If the closure returns `false`, or panics, the element remains\n   461:     /// in the set and will not be yielded.\n   462:     ///\n   463:     /// If the returned `ExtractIf` is not exhausted, e.g. because it is dropped without iterating",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::extract_if",
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
                                  "generic": "T"
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
                      "generic": "T"
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
            "id": 1347,
            "path": "HashSet"
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
              "name": "T"
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
        "impl_id": "std:1371",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1347",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "set",
          "HashSet"
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
                      "generic": "T"
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
            "id": 1368,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "   474:     /// use std::collections::HashSet;\n   475:     ///\n   476:     /// let mut set: HashSet<i32> = (0..8).collect();\n   477:     /// let extracted: HashSet<i32> = set.extract_if(|v| v % 2 == 0).collect();\n   478:     ///\n   479:     /// let mut evens = extracted.into_iter().collect::<Vec<_>>();\n   480:     /// let mut odds = set.into_iter().collect::<Vec<_>>();\n   481:     /// evens.sort();\n   482:     /// odds.sort();\n   483:     ///\n   484:     /// assert_eq!(evens, vec![0, 2, 4, 6]);\n   485:     /// assert_eq!(odds, vec![1, 3, 5, 7]);\n   486:     /// ```\n   487:     #[inline]\n   488:     #[rustc_lint_query_instability]\n   489:     #[stable(feature = \"hash_extract_if\", since = \"1.88.0\")]\n   490:     pub fn extract_if<F>(&mut self, pred: F) -> ExtractIf<'_, T, F, A>\n   491:     where\n   492:         F: FnMut(&T) -> bool,\n   493:     {\n   494:         ExtractIf { base: self.base.extract_if(pred) }\n   495:     }\n   496: \n   497:     /// Retains only the elements specified by the predicate.\n   498:     ///\n   499:     /// In other words, remove all elements `e` for which `f(&e)` returns `false`.\n   500:     /// The elements are visited in unsorted (and unspecified) order.\n   501:     ///\n   502:     /// # Examples\n   503:     ///\n   504:     /// ```\n   505:     /// use std::collections::HashSet;\n   506:     ///",
    "nanvix_source": "   480:     /// let mut odds = set.into_iter().collect::<Vec<_>>();\n   481:     /// evens.sort();\n   482:     /// odds.sort();\n   483:     ///\n   484:     /// assert_eq!(evens, vec![0, 2, 4, 6]);\n   485:     /// assert_eq!(odds, vec![1, 3, 5, 7]);\n   486:     /// ```\n   487:     #[inline]\n   488:     #[rustc_lint_query_instability]\n   489:     #[stable(feature = \"hash_extract_if\", since = \"1.88.0\")]\n   490:     pub fn extract_if<F>(&mut self, pred: F) -> ExtractIf<'_, T, F, A>\n   491:     where\n   492:         F: FnMut(&T) -> bool,\n   493:     {\n   494:         ExtractIf { base: self.base.extract_if(pred) }\n   495:     }\n   496: \n   497:     /// Retains only the elements specified by the predicate.\n   498:     ///\n   499:     /// In other words, remove all elements `e` for which `f(&e)` returns `false`.\n   500:     /// The elements are visited in unsorted (and unspecified) order.",
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
