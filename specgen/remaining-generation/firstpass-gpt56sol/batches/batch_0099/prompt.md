For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashSet::intersection",
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
      "name": "intersection",
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
            "id": 1381,
            "path": "Intersection"
          }
        }
      }
    },
    "verification_source": "   736:     /// ```\n   737:     /// use std::collections::HashSet;\n   738:     /// let a = HashSet::from([1, 2, 3]);\n   739:     /// let b = HashSet::from([4, 2, 3, 4]);\n   740:     ///\n   741:     /// // Print 2, 3 in arbitrary order.\n   742:     /// for x in a.intersection(&b) {\n   743:     ///     println!(\"{x}\");\n   744:     /// }\n   745:     ///\n   746:     /// let intersection: HashSet<_> = a.intersection(&b).collect();\n   747:     /// assert_eq!(intersection, [2, 3].iter().collect());\n   748:     /// ```\n   749:     #[inline]\n   750:     #[rustc_lint_query_instability]\n   751:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   752:     pub fn intersection<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Intersection<'a, T, S, A> {\n   753:         if self.len() <= other.len() {\n   754:             Intersection { iter: self.iter(), other }\n   755:         } else {\n   756:             Intersection { iter: other.iter(), other: self }\n   757:         }\n   758:     }\n   759: \n   760:     /// Visits the values representing the union,\n   761:     /// i.e., all the values in `self` or `other`, without duplicates.\n   762:     ///\n   763:     /// # Examples\n   764:     ///\n   765:     /// ```\n   766:     /// use std::collections::HashSet;\n   767:     /// let a = HashSet::from([1, 2, 3]);\n   768:     /// let b = HashSet::from([4, 2, 3, 4]);",
    "nanvix_source": "   742:     /// for x in a.intersection(&b) {\n   743:     ///     println!(\"{x}\");\n   744:     /// }\n   745:     ///\n   746:     /// let intersection: HashSet<_> = a.intersection(&b).collect();\n   747:     /// assert_eq!(intersection, [2, 3].iter().collect());\n   748:     /// ```\n   749:     #[inline]\n   750:     #[rustc_lint_query_instability]\n   751:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   752:     pub fn intersection<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Intersection<'a, T, S, A> {\n   753:         if self.len() <= other.len() {\n   754:             Intersection { iter: self.iter(), other }\n   755:         } else {\n   756:             Intersection { iter: other.iter(), other: self }\n   757:         }\n   758:     }\n   759: \n   760:     /// Visits the values representing the union,\n   761:     /// i.e., all the values in `self` or `other`, without duplicates.\n   762:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::retain",
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
    "verification_source": "   502:     /// # Examples\n   503:     ///\n   504:     /// ```\n   505:     /// use std::collections::HashSet;\n   506:     ///\n   507:     /// let mut set = HashSet::from([1, 2, 3, 4, 5, 6]);\n   508:     /// set.retain(|&k| k % 2 == 0);\n   509:     /// assert_eq!(set, HashSet::from([2, 4, 6]));\n   510:     /// ```\n   511:     ///\n   512:     /// # Performance\n   513:     ///\n   514:     /// In the current implementation, this operation takes O(capacity) time\n   515:     /// instead of O(len) because it internally visits empty buckets too.\n   516:     #[rustc_lint_query_instability]\n   517:     #[stable(feature = \"retain_hash_collection\", since = \"1.18.0\")]\n   518:     pub fn retain<F>(&mut self, f: F)\n   519:     where\n   520:         F: FnMut(&T) -> bool,\n   521:     {\n   522:         self.base.retain(f)\n   523:     }\n   524: \n   525:     /// Clears the set, removing all values.\n   526:     ///\n   527:     /// # Examples\n   528:     ///\n   529:     /// ```\n   530:     /// use std::collections::HashSet;\n   531:     ///\n   532:     /// let mut v = HashSet::new();\n   533:     /// v.insert(1);\n   534:     /// v.clear();",
    "nanvix_source": "   508:     /// set.retain(|&k| k % 2 == 0);\n   509:     /// assert_eq!(set, HashSet::from([2, 4, 6]));\n   510:     /// ```\n   511:     ///\n   512:     /// # Performance\n   513:     ///\n   514:     /// In the current implementation, this operation takes O(capacity) time\n   515:     /// instead of O(len) because it internally visits empty buckets too.\n   516:     #[rustc_lint_query_instability]\n   517:     #[stable(feature = \"retain_hash_collection\", since = \"1.18.0\")]\n   518:     pub fn retain<F>(&mut self, f: F)\n   519:     where\n   520:         F: FnMut(&T) -> bool,\n   521:     {\n   522:         self.base.retain(f)\n   523:     }\n   524: \n   525:     /// Clears the set, removing all values.\n   526:     ///\n   527:     /// # Examples\n   528:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::symmetric_difference",
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
      "name": "symmetric_difference",
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
            "id": 1379,
            "path": "SymmetricDifference"
          }
        }
      }
    },
    "verification_source": "   702:     /// let b = HashSet::from([4, 2, 3, 4]);\n   703:     ///\n   704:     /// // Print 1, 4 in arbitrary order.\n   705:     /// for x in a.symmetric_difference(&b) {\n   706:     ///     println!(\"{x}\");\n   707:     /// }\n   708:     ///\n   709:     /// let diff1: HashSet<_> = a.symmetric_difference(&b).collect();\n   710:     /// let diff2: HashSet<_> = b.symmetric_difference(&a).collect();\n   711:     ///\n   712:     /// assert_eq!(diff1, diff2);\n   713:     /// assert_eq!(diff1, [1, 4].iter().collect());\n   714:     /// ```\n   715:     #[inline]\n   716:     #[rustc_lint_query_instability]\n   717:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   718:     pub fn symmetric_difference<'a>(\n   719:         &'a self,\n   720:         other: &'a HashSet<T, S, A>,\n   721:     ) -> SymmetricDifference<'a, T, S, A> {\n   722:         SymmetricDifference { iter: self.difference(other).chain(other.difference(self)) }\n   723:     }\n   724: \n   725:     /// Visits the values representing the intersection,\n   726:     /// i.e., the values that are both in `self` and `other`.\n   727:     ///\n   728:     /// When an equal element is present in `self` and `other`\n   729:     /// then the resulting `Intersection` may yield references to\n   730:     /// one or the other. This can be relevant if `T` contains fields which\n   731:     /// are not compared by its `Eq` implementation, and may hold different\n   732:     /// value between the two equal copies of `T` in the two sets.\n   733:     ///\n   734:     /// # Examples",
    "nanvix_source": "   708:     ///\n   709:     /// let diff1: HashSet<_> = a.symmetric_difference(&b).collect();\n   710:     /// let diff2: HashSet<_> = b.symmetric_difference(&a).collect();\n   711:     ///\n   712:     /// assert_eq!(diff1, diff2);\n   713:     /// assert_eq!(diff1, [1, 4].iter().collect());\n   714:     /// ```\n   715:     #[inline]\n   716:     #[rustc_lint_query_instability]\n   717:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   718:     pub fn symmetric_difference<'a>(\n   719:         &'a self,\n   720:         other: &'a HashSet<T, S, A>,\n   721:     ) -> SymmetricDifference<'a, T, S, A> {\n   722:         SymmetricDifference { iter: self.difference(other).chain(other.difference(self)) }\n   723:     }\n   724: \n   725:     /// Visits the values representing the intersection,\n   726:     /// i.e., the values that are both in `self` and `other`.\n   727:     ///\n   728:     /// When an equal element is present in `self` and `other`",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::union",
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
      "name": "union",
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
            "id": 1383,
            "path": "Union"
          }
        }
      }
    },
    "verification_source": "   765:     /// ```\n   766:     /// use std::collections::HashSet;\n   767:     /// let a = HashSet::from([1, 2, 3]);\n   768:     /// let b = HashSet::from([4, 2, 3, 4]);\n   769:     ///\n   770:     /// // Print 1, 2, 3, 4 in arbitrary order.\n   771:     /// for x in a.union(&b) {\n   772:     ///     println!(\"{x}\");\n   773:     /// }\n   774:     ///\n   775:     /// let union: HashSet<_> = a.union(&b).collect();\n   776:     /// assert_eq!(union, [1, 2, 3, 4].iter().collect());\n   777:     /// ```\n   778:     #[inline]\n   779:     #[rustc_lint_query_instability]\n   780:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   781:     pub fn union<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Union<'a, T, S, A> {\n   782:         if self.len() >= other.len() {\n   783:             Union { iter: self.iter().chain(other.difference(self)) }\n   784:         } else {\n   785:             Union { iter: other.iter().chain(self.difference(other)) }\n   786:         }\n   787:     }\n   788: \n   789:     /// Returns `true` if the set contains a value.\n   790:     ///\n   791:     /// The value may be any borrowed form of the set's value type, but\n   792:     /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for\n   793:     /// the value type.\n   794:     ///\n   795:     /// # Examples\n   796:     ///\n   797:     /// ```",
    "nanvix_source": "   771:     /// for x in a.union(&b) {\n   772:     ///     println!(\"{x}\");\n   773:     /// }\n   774:     ///\n   775:     /// let union: HashSet<_> = a.union(&b).collect();\n   776:     /// assert_eq!(union, [1, 2, 3, 4].iter().collect());\n   777:     /// ```\n   778:     #[inline]\n   779:     #[rustc_lint_query_instability]\n   780:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   781:     pub fn union<'a>(&'a self, other: &'a HashSet<T, S, A>) -> Union<'a, T, S, A> {\n   782:         if self.len() >= other.len() {\n   783:             Union { iter: self.iter().chain(other.difference(self)) }\n   784:         } else {\n   785:             Union { iter: other.iter().chain(self.difference(other)) }\n   786:         }\n   787:     }\n   788: \n   789:     /// Returns `true` if the set contains a value.\n   790:     ///\n   791:     /// The value may be any borrowed form of the set's value type, but",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::iter",
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
      "name": "iter",
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
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
            "id": 2409,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  3233:     /// [`components`]: Path::components\n  3234:     ///\n  3235:     /// # Examples\n  3236:     ///\n  3237:     /// ```\n  3238:     /// use std::path::{self, Path};\n  3239:     /// use std::ffi::OsStr;\n  3240:     ///\n  3241:     /// let mut it = Path::new(\"/tmp/foo.txt\").iter();\n  3242:     /// assert_eq!(it.next(), Some(OsStr::new(&path::MAIN_SEPARATOR.to_string())));\n  3243:     /// assert_eq!(it.next(), Some(OsStr::new(\"tmp\")));\n  3244:     /// assert_eq!(it.next(), Some(OsStr::new(\"foo.txt\")));\n  3245:     /// assert_eq!(it.next(), None)\n  3246:     /// ```\n  3247:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3248:     #[inline]\n  3249:     pub fn iter(&self) -> Iter<'_> {\n  3250:         Iter { inner: self.components() }\n  3251:     }\n  3252: \n  3253:     /// Returns an object that implements [`Display`] for safely printing paths\n  3254:     /// that may contain non-Unicode data. This may perform lossy conversion,\n  3255:     /// depending on the platform.  If you would like an implementation which\n  3256:     /// escapes the path please use [`Debug`] instead.\n  3257:     ///\n  3258:     /// [`Display`]: fmt::Display\n  3259:     /// [`Debug`]: fmt::Debug\n  3260:     ///\n  3261:     /// # Examples\n  3262:     ///\n  3263:     /// ```\n  3264:     /// use std::path::Path;\n  3265:     ///",
    "nanvix_source": "  3269:     /// use std::ffi::OsStr;\n  3270:     ///\n  3271:     /// let mut it = Path::new(\"/tmp/foo.txt\").iter();\n  3272:     /// assert_eq!(it.next(), Some(OsStr::new(&path::MAIN_SEPARATOR.to_string())));\n  3273:     /// assert_eq!(it.next(), Some(OsStr::new(\"tmp\")));\n  3274:     /// assert_eq!(it.next(), Some(OsStr::new(\"foo.txt\")));\n  3275:     /// assert_eq!(it.next(), None)\n  3276:     /// ```\n  3277:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3278:     #[inline]\n  3279:     pub fn iter(&self) -> Iter<'_> {\n  3280:         Iter { inner: self.components() }\n  3281:     }\n  3282: \n  3283:     /// Returns an object that implements [`Display`] for safely printing paths\n  3284:     /// that may contain non-Unicode data. This may perform lossy conversion,\n  3285:     /// depending on the platform.  If you would like an implementation which\n  3286:     /// escapes the path please use [`Debug`] instead.\n  3287:     ///\n  3288:     /// [`Display`]: fmt::Display\n  3289:     /// [`Debug`]: fmt::Debug",
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
