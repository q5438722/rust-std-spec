For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashSet::capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "capacity",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   343:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   344:     pub fn with_capacity_and_hasher_in(capacity: usize, hasher: S, alloc: A) -> HashSet<T, S, A> {\n   345:         HashSet { base: base::HashSet::with_capacity_and_hasher_in(capacity, hasher, alloc) }\n   346:     }\n   347: \n   348:     /// Returns the number of elements the set can hold without reallocating.\n   349:     ///\n   350:     /// # Examples\n   351:     ///\n   352:     /// ```\n   353:     /// use std::collections::HashSet;\n   354:     /// let set: HashSet<i32> = HashSet::with_capacity(100);\n   355:     /// assert!(set.capacity() >= 100);\n   356:     /// ```\n   357:     #[inline]\n   358:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   359:     pub fn capacity(&self) -> usize {\n   360:         self.base.capacity()\n   361:     }\n   362: \n   363:     /// An iterator visiting all elements in arbitrary order.\n   364:     /// The iterator element type is `&'a T`.\n   365:     ///\n   366:     /// # Examples\n   367:     ///\n   368:     /// ```\n   369:     /// use std::collections::HashSet;\n   370:     /// let mut set = HashSet::new();\n   371:     /// set.insert(\"a\");\n   372:     /// set.insert(\"b\");\n   373:     ///\n   374:     /// // Will print in an arbitrary order.\n   375:     /// for x in set.iter() {",
    "nanvix_source": "   349:     ///\n   350:     /// # Examples\n   351:     ///\n   352:     /// ```\n   353:     /// use std::collections::HashSet;\n   354:     /// let set: HashSet<i32> = HashSet::with_capacity(100);\n   355:     /// assert!(set.capacity() >= 100);\n   356:     /// ```\n   357:     #[inline]\n   358:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   359:     pub fn capacity(&self) -> usize {\n   360:         self.base.capacity()\n   361:     }\n   362: \n   363:     /// An iterator visiting all elements in arbitrary order.\n   364:     /// The iterator element type is `&'a T`.\n   365:     ///\n   366:     /// # Examples\n   367:     ///\n   368:     /// ```\n   369:     /// use std::collections::HashSet;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "hasher",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "S"
            }
          }
        }
      }
    },
    "verification_source": "   541:     }\n   542: \n   543:     /// Returns a reference to the set's [`BuildHasher`].\n   544:     ///\n   545:     /// # Examples\n   546:     ///\n   547:     /// ```\n   548:     /// use std::collections::HashSet;\n   549:     /// use std::hash::RandomState;\n   550:     ///\n   551:     /// let hasher = RandomState::new();\n   552:     /// let set: HashSet<i32> = HashSet::with_hasher(hasher);\n   553:     /// let hasher: &RandomState = set.hasher();\n   554:     /// ```\n   555:     #[inline]\n   556:     #[stable(feature = \"hashmap_public_hasher\", since = \"1.9.0\")]\n   557:     pub fn hasher(&self) -> &S {\n   558:         self.base.hasher()\n   559:     }\n   560: }\n   561: \n   562: impl<T, S, A> HashSet<T, S, A>\n   563: where\n   564:     T: Eq + Hash,\n   565:     S: BuildHasher,\n   566:     A: Allocator,\n   567: {\n   568:     /// Reserves capacity for at least `additional` more elements to be inserted\n   569:     /// in the `HashSet`. The collection may reserve more space to speculatively\n   570:     /// avoid frequent reallocations. After calling `reserve`,\n   571:     /// capacity will be greater than or equal to `self.len() + additional`.\n   572:     /// Does nothing if capacity is already sufficient.\n   573:     ///",
    "nanvix_source": "   547:     /// ```\n   548:     /// use std::collections::HashSet;\n   549:     /// use std::hash::RandomState;\n   550:     ///\n   551:     /// let hasher = RandomState::new();\n   552:     /// let set: HashSet<i32> = HashSet::with_hasher(hasher);\n   553:     /// let hasher: &RandomState = set.hasher();\n   554:     /// ```\n   555:     #[inline]\n   556:     #[stable(feature = \"hashmap_public_hasher\", since = \"1.9.0\")]\n   557:     pub fn hasher(&self) -> &S {\n   558:         self.base.hasher()\n   559:     }\n   560: }\n   561: \n   562: impl<T, S, A> HashSet<T, S, A>\n   563: where\n   564:     T: Eq + Hash,\n   565:     S: BuildHasher,\n   566:     A: Allocator,\n   567: {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to",
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   644:     /// # Examples\n   645:     ///\n   646:     /// ```\n   647:     /// use std::collections::HashSet;\n   648:     ///\n   649:     /// let mut set = HashSet::with_capacity(100);\n   650:     /// set.insert(1);\n   651:     /// set.insert(2);\n   652:     /// assert!(set.capacity() >= 100);\n   653:     /// set.shrink_to(10);\n   654:     /// assert!(set.capacity() >= 10);\n   655:     /// set.shrink_to(0);\n   656:     /// assert!(set.capacity() >= 2);\n   657:     /// ```\n   658:     #[inline]\n   659:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   660:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   661:         self.base.shrink_to(min_capacity)\n   662:     }\n   663: \n   664:     /// Visits the values representing the difference,\n   665:     /// i.e., the values that are in `self` but not in `other`.\n   666:     ///\n   667:     /// # Examples\n   668:     ///\n   669:     /// ```\n   670:     /// use std::collections::HashSet;\n   671:     /// let a = HashSet::from([1, 2, 3]);\n   672:     /// let b = HashSet::from([4, 2, 3, 4]);\n   673:     ///\n   674:     /// // Can be seen as `a - b`.\n   675:     /// for x in a.difference(&b) {\n   676:     ///     println!(\"{x}\"); // Print 1",
    "nanvix_source": "   650:     /// set.insert(1);\n   651:     /// set.insert(2);\n   652:     /// assert!(set.capacity() >= 100);\n   653:     /// set.shrink_to(10);\n   654:     /// assert!(set.capacity() >= 10);\n   655:     /// set.shrink_to(0);\n   656:     /// assert!(set.capacity() >= 2);\n   657:     /// ```\n   658:     #[inline]\n   659:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   660:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   661:         self.base.shrink_to(min_capacity)\n   662:     }\n   663: \n   664:     /// Visits the values representing the difference,\n   665:     /// i.e., the values that are in `self` but not in `other`.\n   666:     ///\n   667:     /// # Examples\n   668:     ///\n   669:     /// ```\n   670:     /// use std::collections::HashSet;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to_fit",
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
        "output": null
      }
    },
    "verification_source": "   619:     /// and possibly leaving some space in accordance with the resize policy.\n   620:     ///\n   621:     /// # Examples\n   622:     ///\n   623:     /// ```\n   624:     /// use std::collections::HashSet;\n   625:     ///\n   626:     /// let mut set = HashSet::with_capacity(100);\n   627:     /// set.insert(1);\n   628:     /// set.insert(2);\n   629:     /// assert!(set.capacity() >= 100);\n   630:     /// set.shrink_to_fit();\n   631:     /// assert!(set.capacity() >= 2);\n   632:     /// ```\n   633:     #[inline]\n   634:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   635:     pub fn shrink_to_fit(&mut self) {\n   636:         self.base.shrink_to_fit()\n   637:     }\n   638: \n   639:     /// Shrinks the capacity of the set with a lower limit. It will drop\n   640:     /// down no lower than the supplied limit while maintaining the internal rules\n   641:     /// and possibly leaving some space in accordance with the resize policy.\n   642:     ///\n   643:     /// If the current capacity is less than the lower limit, this is a no-op.\n   644:     /// # Examples\n   645:     ///\n   646:     /// ```\n   647:     /// use std::collections::HashSet;\n   648:     ///\n   649:     /// let mut set = HashSet::with_capacity(100);\n   650:     /// set.insert(1);\n   651:     /// set.insert(2);",
    "nanvix_source": "   625:     ///\n   626:     /// let mut set = HashSet::with_capacity(100);\n   627:     /// set.insert(1);\n   628:     /// set.insert(2);\n   629:     /// assert!(set.capacity() >= 100);\n   630:     /// set.shrink_to_fit();\n   631:     /// assert!(set.capacity() >= 2);\n   632:     /// ```\n   633:     #[inline]\n   634:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   635:     pub fn shrink_to_fit(&mut self) {\n   636:         self.base.shrink_to_fit()\n   637:     }\n   638: \n   639:     /// Shrinks the capacity of the set with a lower limit. It will drop\n   640:     /// down no lower than the supplied limit while maintaining the internal rules\n   641:     /// and possibly leaving some space in accordance with the resize policy.\n   642:     ///\n   643:     /// If the current capacity is less than the lower limit, this is a no-op.\n   644:     /// # Examples\n   645:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "try_reserve",
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "additional",
            {
              "primitive": "usize"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 874,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   597:     /// Does nothing if capacity is already sufficient.\n   598:     ///\n   599:     /// # Errors\n   600:     ///\n   601:     /// If the capacity overflows, or the allocator reports a failure, then an error\n   602:     /// is returned.\n   603:     ///\n   604:     /// # Examples\n   605:     ///\n   606:     /// ```\n   607:     /// use std::collections::HashSet;\n   608:     /// let mut set: HashSet<i32> = HashSet::new();\n   609:     /// set.try_reserve(10).expect(\"why is the test harness OOMing on a handful of bytes?\");\n   610:     /// ```\n   611:     #[inline]\n   612:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n   613:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   614:         self.base.try_reserve(additional).map_err(map_try_reserve_error)\n   615:     }\n   616: \n   617:     /// Shrinks the capacity of the set as much as possible. It will drop\n   618:     /// down as much as possible while maintaining the internal rules\n   619:     /// and possibly leaving some space in accordance with the resize policy.\n   620:     ///\n   621:     /// # Examples\n   622:     ///\n   623:     /// ```\n   624:     /// use std::collections::HashSet;\n   625:     ///\n   626:     /// let mut set = HashSet::with_capacity(100);\n   627:     /// set.insert(1);\n   628:     /// set.insert(2);\n   629:     /// assert!(set.capacity() >= 100);",
    "nanvix_source": "   603:     ///\n   604:     /// # Examples\n   605:     ///\n   606:     /// ```\n   607:     /// use std::collections::HashSet;\n   608:     /// let mut set: HashSet<i32> = HashSet::new();\n   609:     /// set.try_reserve(10).expect(\"why is the test harness OOMing on a handful of bytes?\");\n   610:     /// ```\n   611:     #[inline]\n   612:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n   613:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   614:         self.base.try_reserve(additional).map_err(map_try_reserve_error)\n   615:     }\n   616: \n   617:     /// Shrinks the capacity of the set as much as possible. It will drop\n   618:     /// down as much as possible while maintaining the internal rules\n   619:     /// and possibly leaving some space in accordance with the resize policy.\n   620:     ///\n   621:     /// # Examples\n   622:     ///\n   623:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashSet::with_capacity_and_hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "with_capacity_and_hasher",
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:1356",
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
            "capacity",
            {
              "primitive": "usize"
            }
          ],
          [
            "hasher",
            {
              "generic": "S"
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
                  },
                  {
                    "type": {
                      "generic": "S"
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
    },
    "verification_source": "   262:     /// The `hash_builder` passed should implement the [`BuildHasher`] trait for\n   263:     /// the `HashSet` to be useful, see its documentation for details.\n   264:     ///\n   265:     /// # Examples\n   266:     ///\n   267:     /// ```\n   268:     /// use std::collections::HashSet;\n   269:     /// use std::hash::RandomState;\n   270:     ///\n   271:     /// let s = RandomState::new();\n   272:     /// let mut set = HashSet::with_capacity_and_hasher(10, s);\n   273:     /// set.insert(1);\n   274:     /// ```\n   275:     #[inline]\n   276:     #[must_use]\n   277:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   278:     pub fn with_capacity_and_hasher(capacity: usize, hasher: S) -> HashSet<T, S> {\n   279:         HashSet { base: base::HashSet::with_capacity_and_hasher(capacity, hasher) }\n   280:     }\n   281: }\n   282: \n   283: impl<T, S, A: Allocator> HashSet<T, S, A> {\n   284:     /// Creates a new empty hash set which will use the given hasher to hash\n   285:     /// keys and will allocate memory using the provided allocator.\n   286:     ///\n   287:     /// The hash set is also created with the default initial capacity.\n   288:     ///\n   289:     /// Warning: `hasher` is normally randomly generated, and\n   290:     /// is designed to allow `HashSet`s to be resistant to attacks that\n   291:     /// cause many collisions and very poor performance. Setting it\n   292:     /// manually using this function can expose a DoS attack vector.\n   293:     ///\n   294:     /// The `hash_builder` passed should implement the [`BuildHasher`] trait for",
    "nanvix_source": "   268:     /// use std::collections::HashSet;\n   269:     /// use std::hash::RandomState;\n   270:     ///\n   271:     /// let s = RandomState::new();\n   272:     /// let mut set = HashSet::with_capacity_and_hasher(10, s);\n   273:     /// set.insert(1);\n   274:     /// ```\n   275:     #[inline]\n   276:     #[must_use]\n   277:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   278:     pub fn with_capacity_and_hasher(capacity: usize, hasher: S) -> HashSet<T, S> {\n   279:         HashSet { base: base::HashSet::with_capacity_and_hasher(capacity, hasher) }\n   280:     }\n   281: }\n   282: \n   283: impl<T, S, A: Allocator> HashSet<T, S, A> {\n   284:     /// Creates a new empty hash set which will use the given hasher to hash\n   285:     /// keys and will allocate memory using the provided allocator.\n   286:     ///\n   287:     /// The hash set is also created with the default initial capacity.\n   288:     ///",
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
