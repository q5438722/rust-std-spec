For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::btree_map::Entry::and_modify",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "V"
                                }
                              }
                            }
                          ],
                          "output": null
                        }
                      },
                      "id": 441,
                      "path": "FnOnce"
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
      "name": "and_modify",
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
                    "lifetime": "'a"
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
            "id": 1269,
            "path": "Entry"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
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
                          "id": 176,
                          "path": "Ord"
                        }
                      }
                    }
                  ],
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:1276",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1269",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "Entry"
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
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   245:     /// ```\n   246:     /// use std::collections::BTreeMap;\n   247:     ///\n   248:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   249:     ///\n   250:     /// map.entry(\"poneyland\")\n   251:     ///    .and_modify(|e| { *e += 1 })\n   252:     ///    .or_insert(42);\n   253:     /// assert_eq!(map[\"poneyland\"], 42);\n   254:     ///\n   255:     /// map.entry(\"poneyland\")\n   256:     ///    .and_modify(|e| { *e += 1 })\n   257:     ///    .or_insert(42);\n   258:     /// assert_eq!(map[\"poneyland\"], 43);\n   259:     /// ```\n   260:     #[stable(feature = \"entry_and_modify\", since = \"1.26.0\")]\n   261:     pub fn and_modify<F>(self, f: F) -> Self\n   262:     where\n   263:         F: FnOnce(&mut V),\n   264:     {\n   265:         match self {\n   266:             Occupied(mut entry) => {\n   267:                 f(entry.get_mut());\n   268:                 Occupied(entry)\n   269:             }\n   270:             Vacant(entry) => Vacant(entry),\n   271:         }\n   272:     }\n   273: \n   274:     /// Sets the value of the entry, and returns an `OccupiedEntry`.\n   275:     ///\n   276:     /// # Examples\n   277:     ///",
    "nanvix_source": "   300:     ///    .and_modify(|e| { *e += 1 })\n   301:     ///    .or_insert(42);\n   302:     /// assert_eq!(map[\"poneyland\"], 42);\n   303:     ///\n   304:     /// map.entry(\"poneyland\")\n   305:     ///    .and_modify(|e| { *e += 1 })\n   306:     ///    .or_insert(42);\n   307:     /// assert_eq!(map[\"poneyland\"], 43);\n   308:     /// ```\n   309:     #[stable(feature = \"entry_and_modify\", since = \"1.26.0\")]\n   310:     pub fn and_modify<F>(self, f: F) -> Self\n   311:     where\n   312:         F: FnOnce(&mut V),\n   313:     {\n   314:         match self {\n   315:             Occupied(mut entry) => {\n   316:                 f(entry.get_mut());\n   317:                 Occupied(entry)\n   318:             }\n   319:             Vacant(entry) => Vacant(entry),\n   320:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::dedup_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": true,
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
                      "id": 534,
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
      "name": "dedup_by",
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
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "same_bucket",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2598:     /// The `same_bucket` function is passed references to two elements from the vector and\n  2599:     /// must determine if the elements compare equal. The elements are passed in opposite order\n  2600:     /// from their order in the slice, so if `same_bucket(a, b)` returns `true`, `a` is removed.\n  2601:     ///\n  2602:     /// If the vector is sorted, this removes all duplicates.\n  2603:     ///\n  2604:     /// # Examples\n  2605:     ///\n  2606:     /// ```\n  2607:     /// let mut vec = vec![\"foo\", \"bar\", \"Bar\", \"baz\", \"bar\"];\n  2608:     ///\n  2609:     /// vec.dedup_by(|a, b| a.eq_ignore_ascii_case(b));\n  2610:     ///\n  2611:     /// assert_eq!(vec, [\"foo\", \"bar\", \"baz\", \"bar\"]);\n  2612:     /// ```\n  2613:     #[stable(feature = \"dedup_by\", since = \"1.16.0\")]\n  2614:     pub fn dedup_by<F>(&mut self, mut same_bucket: F)\n  2615:     where\n  2616:         F: FnMut(&mut T, &mut T) -> bool,\n  2617:     {\n  2618:         let len = self.len();\n  2619:         if len <= 1 {\n  2620:             return;\n  2621:         }\n  2622: \n  2623:         // Check if we ever want to remove anything.\n  2624:         // This allows to use copy_non_overlapping in next cycle.\n  2625:         // And avoids any memory writes if we don't need to remove anything.\n  2626:         let mut first_duplicate_idx: usize = 1;\n  2627:         let start = self.as_mut_ptr();\n  2628:         while first_duplicate_idx != len {\n  2629:             let found_duplicate = unsafe {\n  2630:                 // SAFETY: first_duplicate always in range [1..len)",
    "nanvix_source": "  2641:     /// # Examples\n  2642:     ///\n  2643:     /// ```\n  2644:     /// let mut vec = vec![\"foo\", \"bar\", \"Bar\", \"baz\", \"bar\"];\n  2645:     ///\n  2646:     /// vec.dedup_by(|a, b| a.eq_ignore_ascii_case(b));\n  2647:     ///\n  2648:     /// assert_eq!(vec, [\"foo\", \"bar\", \"baz\", \"bar\"]);\n  2649:     /// ```\n  2650:     #[stable(feature = \"dedup_by\", since = \"1.16.0\")]\n  2651:     pub fn dedup_by<F>(&mut self, mut same_bucket: F)\n  2652:     where\n  2653:         F: FnMut(&mut T, &mut T) -> bool,\n  2654:     {\n  2655:         let len = self.len();\n  2656:         if len <= 1 {\n  2657:             return;\n  2658:         }\n  2659: \n  2660:         // Check if we ever want to remove anything.\n  2661:         // This allows to use copy_non_overlapping in next cycle.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::dedup_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "K"
                          }
                        }
                      },
                      "id": 534,
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
                      "id": 179,
                      "path": "PartialEq"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
      "name": "dedup_by_key",
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
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "key",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2571:     /// Removes all but the first of consecutive elements in the vector that resolve to the same\n  2572:     /// key.\n  2573:     ///\n  2574:     /// If the vector is sorted, this removes all duplicates.\n  2575:     ///\n  2576:     /// # Examples\n  2577:     ///\n  2578:     /// ```\n  2579:     /// let mut vec = vec![10, 20, 21, 30, 20];\n  2580:     ///\n  2581:     /// vec.dedup_by_key(|i| *i / 10);\n  2582:     ///\n  2583:     /// assert_eq!(vec, [10, 20, 30, 20]);\n  2584:     /// ```\n  2585:     #[stable(feature = \"dedup_by\", since = \"1.16.0\")]\n  2586:     #[inline]\n  2587:     pub fn dedup_by_key<F, K>(&mut self, mut key: F)\n  2588:     where\n  2589:         F: FnMut(&mut T) -> K,\n  2590:         K: PartialEq,\n  2591:     {\n  2592:         self.dedup_by(|a, b| key(a) == key(b))\n  2593:     }\n  2594: \n  2595:     /// Removes all but the first of consecutive elements in the vector satisfying a given equality\n  2596:     /// relation.\n  2597:     ///\n  2598:     /// The `same_bucket` function is passed references to two elements from the vector and\n  2599:     /// must determine if the elements compare equal. The elements are passed in opposite order\n  2600:     /// from their order in the slice, so if `same_bucket(a, b)` returns `true`, `a` is removed.\n  2601:     ///\n  2602:     /// If the vector is sorted, this removes all duplicates.\n  2603:     ///",
    "nanvix_source": "  2614:     ///\n  2615:     /// ```\n  2616:     /// let mut vec = vec![10, 20, 21, 30, 20];\n  2617:     ///\n  2618:     /// vec.dedup_by_key(|i| *i / 10);\n  2619:     ///\n  2620:     /// assert_eq!(vec, [10, 20, 30, 20]);\n  2621:     /// ```\n  2622:     #[stable(feature = \"dedup_by\", since = \"1.16.0\")]\n  2623:     #[inline]\n  2624:     pub fn dedup_by_key<F, K>(&mut self, mut key: F)\n  2625:     where\n  2626:         F: FnMut(&mut T) -> K,\n  2627:         K: PartialEq,\n  2628:     {\n  2629:         self.dedup_by(|a, b| key(a) == key(b))\n  2630:     }\n  2631: \n  2632:     /// Removes all but the first of consecutive elements in the vector satisfying a given equality\n  2633:     /// relation.\n  2634:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::pop_if",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
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
                                  "is_mutable": true,
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
                        "id": 441,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(&mut T) -> bool"
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
      "name": "pop_if",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "predicate"
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "predicate",
            {
              "impl_trait": [
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
                                "is_mutable": true,
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
                      "id": 441,
                      "path": "FnOnce"
                    }
                  }
                }
              ]
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2827: \n  2828:     /// Removes and returns the last element from a vector if the predicate\n  2829:     /// returns `true`, or [`None`] if the predicate returns false or the vector\n  2830:     /// is empty (the predicate will not be called in that case).\n  2831:     ///\n  2832:     /// # Examples\n  2833:     ///\n  2834:     /// ```\n  2835:     /// let mut vec = vec![1, 2, 3, 4];\n  2836:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2837:     ///\n  2838:     /// assert_eq!(vec.pop_if(pred), Some(4));\n  2839:     /// assert_eq!(vec, [1, 2, 3]);\n  2840:     /// assert_eq!(vec.pop_if(pred), None);\n  2841:     /// ```\n  2842:     #[stable(feature = \"vec_pop_if\", since = \"1.86.0\")]\n  2843:     pub fn pop_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2844:         let last = self.last_mut()?;\n  2845:         if predicate(last) { self.pop() } else { None }\n  2846:     }\n  2847: \n  2848:     /// Returns a mutable reference to the last item in the vector, or\n  2849:     /// `None` if it is empty.\n  2850:     ///\n  2851:     /// # Examples\n  2852:     ///\n  2853:     /// Basic usage:\n  2854:     ///\n  2855:     /// ```\n  2856:     /// #![feature(vec_peek_mut)]\n  2857:     /// let mut vec = Vec::new();\n  2858:     /// assert!(vec.peek_mut().is_none());\n  2859:     ///",
    "nanvix_source": "  2870:     ///\n  2871:     /// ```\n  2872:     /// let mut vec = vec![1, 2, 3, 4];\n  2873:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2874:     ///\n  2875:     /// assert_eq!(vec.pop_if(pred), Some(4));\n  2876:     /// assert_eq!(vec, [1, 2, 3]);\n  2877:     /// assert_eq!(vec.pop_if(pred), None);\n  2878:     /// ```\n  2879:     #[stable(feature = \"vec_pop_if\", since = \"1.86.0\")]\n  2880:     pub fn pop_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2881:         let last = self.last_mut()?;\n  2882:         if predicate(last) { self.pop() } else { None }\n  2883:     }\n  2884: \n  2885:     /// Returns a mutable reference to the last item in the vector, or\n  2886:     /// `None` if it is empty.\n  2887:     ///\n  2888:     /// # Examples\n  2889:     ///\n  2890:     /// Basic usage:",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::resize_with",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
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
                          "inputs": [],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 534,
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
      "name": "resize_with",
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
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "new_len",
            {
              "primitive": "usize"
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
    "verification_source": "  3125:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  3126:     ///\n  3127:     /// # Examples\n  3128:     ///\n  3129:     /// ```\n  3130:     /// let mut vec = vec![1, 2, 3];\n  3131:     /// vec.resize_with(5, Default::default);\n  3132:     /// assert_eq!(vec, [1, 2, 3, 0, 0]);\n  3133:     ///\n  3134:     /// let mut vec = vec![];\n  3135:     /// let mut p = 1;\n  3136:     /// vec.resize_with(4, || { p *= 2; p });\n  3137:     /// assert_eq!(vec, [2, 4, 8, 16]);\n  3138:     /// ```\n  3139:     #[cfg(not(no_global_oom_handling))]\n  3140:     #[stable(feature = \"vec_resize_with\", since = \"1.33.0\")]\n  3141:     pub fn resize_with<F>(&mut self, new_len: usize, f: F)\n  3142:     where\n  3143:         F: FnMut() -> T,\n  3144:     {\n  3145:         let len = self.len();\n  3146:         if new_len > len {\n  3147:             self.extend_trusted(iter::repeat_with(f).take(new_len - len));\n  3148:         } else {\n  3149:             self.truncate(new_len);\n  3150:         }\n  3151:     }\n  3152: \n  3153:     /// Consumes and leaks the `Vec`, returning a mutable reference to the contents,\n  3154:     /// `&'a mut [T]`.\n  3155:     ///\n  3156:     /// Note that the type `T` must outlive the chosen lifetime `'a`. If the type\n  3157:     /// has only static references, or none at all, then this may be chosen to be",
    "nanvix_source": "  3172:     /// vec.resize_with(5, Default::default);\n  3173:     /// assert_eq!(vec, [1, 2, 3, 0, 0]);\n  3174:     ///\n  3175:     /// let mut vec = vec![];\n  3176:     /// let mut p = 1;\n  3177:     /// vec.resize_with(4, || { p *= 2; p });\n  3178:     /// assert_eq!(vec, [2, 4, 8, 16]);\n  3179:     /// ```\n  3180:     #[cfg(not(no_global_oom_handling))]\n  3181:     #[stable(feature = \"vec_resize_with\", since = \"1.33.0\")]\n  3182:     pub fn resize_with<F>(&mut self, new_len: usize, f: F)\n  3183:     where\n  3184:         F: FnMut() -> T,\n  3185:     {\n  3186:         let len = self.len();\n  3187:         if new_len > len {\n  3188:             self.extend_trusted(iter::repeat_with(f).take(new_len - len));\n  3189:         } else {\n  3190:             self.truncate(new_len);\n  3191:         }\n  3192:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::from_fn",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
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
            "name": "T"
          },
          {
            "kind": {
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
          },
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "primitive": "usize"
                            }
                          ],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 22,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "from_fn",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "array": {
            "len": "N",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "    93: /// # // TBH `array::repeat` would be better for this, but it's not stable yet.\n    94: /// let my_string = String::from(\"Hello\");\n    95: /// let clones: [String; 42] = std::array::from_fn(|_| my_string.clone());\n    96: /// assert!(clones.iter().all(|x| *x == my_string));\n    97: /// ```\n    98: ///\n    99: /// The array is generated in ascending index order, starting from the front\n   100: /// and going towards the back, so you can use closures with mutable state:\n   101: /// ```\n   102: /// let mut state = 1;\n   103: /// let a = std::array::from_fn(|_| { let x = state; state *= 2; x });\n   104: /// assert_eq!(a, [1, 2, 4, 8, 16, 32]);\n   105: /// ```\n   106: #[inline]\n   107: #[stable(feature = \"array_from_fn\", since = \"1.63.0\")]\n   108: #[rustc_const_unstable(feature = \"const_array\", issue = \"147606\")]\n   109: pub const fn from_fn<T: [const] Destruct, const N: usize, F>(f: F) -> [T; N]\n   110: where\n   111:     F: [const] FnMut(usize) -> T + [const] Destruct,\n   112: {\n   113:     try_from_fn(NeverShortCircuit::wrap_mut_1(f)).0\n   114: }\n   115: \n   116: /// Creates an array `[T; N]` where each fallible array element `T` is returned by the `cb` call.\n   117: /// Unlike [`from_fn`], where the element creation can't fail, this version will return an error\n   118: /// if any element creation was unsuccessful.\n   119: ///\n   120: /// The return type of this function depends on the return type of the closure.\n   121: /// If you return `Result<T, E>` from the closure, you'll get a `Result<[T; N], E>`.\n   122: /// If you return `Option<T>` from the closure, you'll get an `Option<[T; N]>`.\n   123: ///\n   124: /// # Arguments\n   125: ///",
    "nanvix_source": "   100: /// The array is generated in ascending index order, starting from the front\n   101: /// and going towards the back, so you can use closures with mutable state:\n   102: /// ```\n   103: /// let mut state = 1;\n   104: /// let a = std::array::from_fn(|_| { let x = state; state *= 2; x });\n   105: /// assert_eq!(a, [1, 2, 4, 8, 16, 32]);\n   106: /// ```\n   107: #[inline]\n   108: #[stable(feature = \"array_from_fn\", since = \"1.63.0\")]\n   109: #[rustc_const_unstable(feature = \"const_array\", issue = \"147606\")]\n   110: pub const fn from_fn<T: [const] Destruct, const N: usize, F>(f: F) -> [T; N]\n   111: where\n   112:     F: [const] FnMut(usize) -> T + [const] Destruct,\n   113: {\n   114:     try_from_fn(NeverShortCircuit::wrap_mut_1(f)).0\n   115: }\n   116: \n   117: /// Creates an array `[T; N]` where each fallible array element `T` is returned by the `cb` call.\n   118: /// Unlike [`from_fn`], where the element creation can't fail, this version will return an error\n   119: /// if any element creation was unsuccessful.\n   120: ///",
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
