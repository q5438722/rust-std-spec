For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::btree_map::Entry::or_insert_with_key",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
                                  "is_mutable": false,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "K"
                                  }
                                }
                              }
                            ],
                            "output": {
                              "generic": "V"
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
      "name": "or_insert_with_key",
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
            "default",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   196:     /// The reference to the moved key is provided so that cloning or copying the key is\n   197:     /// unnecessary, unlike with `.or_insert_with(|| ... )`.\n   198:     ///\n   199:     /// # Examples\n   200:     ///\n   201:     /// ```\n   202:     /// use std::collections::BTreeMap;\n   203:     ///\n   204:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   205:     ///\n   206:     /// map.entry(\"poneyland\").or_insert_with_key(|key| key.chars().count());\n   207:     ///\n   208:     /// assert_eq!(map[\"poneyland\"], 9);\n   209:     /// ```\n   210:     #[inline]\n   211:     #[stable(feature = \"or_insert_with_key\", since = \"1.50.0\")]\n   212:     pub fn or_insert_with_key<F: FnOnce(&K) -> V>(self, default: F) -> &'a mut V {\n   213:         match self {\n   214:             Occupied(entry) => entry.into_mut(),\n   215:             Vacant(entry) => {\n   216:                 let value = default(entry.key());\n   217:                 entry.insert(value)\n   218:             }\n   219:         }\n   220:     }\n   221: \n   222:     /// Returns a reference to this entry's key.\n   223:     ///\n   224:     /// # Examples\n   225:     ///\n   226:     /// ```\n   227:     /// use std::collections::BTreeMap;\n   228:     ///",
    "nanvix_source": "   218:     /// use std::collections::BTreeMap;\n   219:     ///\n   220:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   221:     ///\n   222:     /// map.entry(\"poneyland\").or_insert_with_key(|key| key.chars().count());\n   223:     ///\n   224:     /// assert_eq!(map[\"poneyland\"], 9);\n   225:     /// ```\n   226:     #[inline]\n   227:     #[stable(feature = \"or_insert_with_key\", since = \"1.50.0\")]\n   228:     pub fn or_insert_with_key<F: FnOnce(&K) -> V>(self, default: F) -> &'a mut V {\n   229:         self.or_try_insert_with_key(|k| Result::<_, !>::Ok(default(k))).into_ok()\n   230:     }\n   231: \n   232:     /// Ensures a value is in the entry by inserting, if empty, the result of the default function.\n   233:     /// This method allows for generating key-derived values for insertion by providing the default\n   234:     /// function a reference to the key that was moved during the `entry(key)` method call.\n   235:     ///\n   236:     /// This method works identically to [`or_insert_with_key`] except that the default function\n   237:     /// should return a `Result` and, in the case of an error, the error is propagated.\n   238:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 1265,
            "path": "OccupiedEntry"
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
        "impl_id": "alloc:1332",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1265",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "OccupiedEntry"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   512:     /// use std::collections::btree_map::Entry;\n   513:     ///\n   514:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   515:     /// map.entry(\"poneyland\").or_insert(12);\n   516:     ///\n   517:     /// assert_eq!(map[\"poneyland\"], 12);\n   518:     /// if let Entry::Occupied(mut o) = map.entry(\"poneyland\") {\n   519:     ///     *o.get_mut() += 10;\n   520:     ///     assert_eq!(*o.get(), 22);\n   521:     ///\n   522:     ///     // We can use the same Entry multiple times.\n   523:     ///     *o.get_mut() += 2;\n   524:     /// }\n   525:     /// assert_eq!(map[\"poneyland\"], 24);\n   526:     /// ```\n   527:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   528:     pub fn get_mut(&mut self) -> &mut V {\n   529:         self.handle.kv_mut().1\n   530:     }\n   531: \n   532:     /// Converts the entry into a mutable reference to its value.\n   533:     ///\n   534:     /// If you need multiple references to the `OccupiedEntry`, see [`get_mut`].\n   535:     ///\n   536:     /// [`get_mut`]: OccupiedEntry::get_mut\n   537:     ///\n   538:     /// # Examples\n   539:     ///\n   540:     /// ```\n   541:     /// use std::collections::BTreeMap;\n   542:     /// use std::collections::btree_map::Entry;\n   543:     ///\n   544:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();",
    "nanvix_source": "   567:     /// if let Entry::Occupied(mut o) = map.entry(\"poneyland\") {\n   568:     ///     *o.get_mut() += 10;\n   569:     ///     assert_eq!(*o.get(), 22);\n   570:     ///\n   571:     ///     // We can use the same Entry multiple times.\n   572:     ///     *o.get_mut() += 2;\n   573:     /// }\n   574:     /// assert_eq!(map[\"poneyland\"], 24);\n   575:     /// ```\n   576:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   577:     pub fn get_mut(&mut self) -> &mut V {\n   578:         self.handle.kv_mut().1\n   579:     }\n   580: \n   581:     /// Converts the entry into a mutable reference to its value.\n   582:     ///\n   583:     /// If you need multiple references to the `OccupiedEntry`, see [`get_mut`].\n   584:     ///\n   585:     /// [`get_mut`]: OccupiedEntry::get_mut\n   586:     ///\n   587:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::into_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "into_mut",
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
            "id": 1265,
            "path": "OccupiedEntry"
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
        "impl_id": "alloc:1332",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1265",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "OccupiedEntry"
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
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   539:     ///\n   540:     /// ```\n   541:     /// use std::collections::BTreeMap;\n   542:     /// use std::collections::btree_map::Entry;\n   543:     ///\n   544:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   545:     /// map.entry(\"poneyland\").or_insert(12);\n   546:     ///\n   547:     /// assert_eq!(map[\"poneyland\"], 12);\n   548:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   549:     ///     *o.into_mut() += 10;\n   550:     /// }\n   551:     /// assert_eq!(map[\"poneyland\"], 22);\n   552:     /// ```\n   553:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   554:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   555:     pub fn into_mut(self) -> &'a mut V {\n   556:         self.handle.into_val_mut()\n   557:     }\n   558: \n   559:     /// Sets the value of the entry with the `OccupiedEntry`'s key,\n   560:     /// and returns the entry's old value.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// use std::collections::BTreeMap;\n   566:     /// use std::collections::btree_map::Entry;\n   567:     ///\n   568:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   569:     /// map.entry(\"poneyland\").or_insert(12);\n   570:     ///\n   571:     /// if let Entry::Occupied(mut o) = map.entry(\"poneyland\") {",
    "nanvix_source": "   594:     /// map.entry(\"poneyland\").or_insert(12);\n   595:     ///\n   596:     /// assert_eq!(map[\"poneyland\"], 12);\n   597:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   598:     ///     *o.into_mut() += 10;\n   599:     /// }\n   600:     /// assert_eq!(map[\"poneyland\"], 22);\n   601:     /// ```\n   602:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   603:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   604:     pub fn into_mut(self) -> &'a mut V {\n   605:         self.handle.into_val_mut()\n   606:     }\n   607: \n   608:     /// Sets the value of the entry with the `OccupiedEntry`'s key,\n   609:     /// and returns the entry's old value.\n   610:     ///\n   611:     /// # Examples\n   612:     ///\n   613:     /// ```\n   614:     /// use std::collections::BTreeMap;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::VacantEntry::insert",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "insert",
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
            "id": 1262,
            "path": "VacantEntry"
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
        "impl_id": "alloc:1304",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1262",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "VacantEntry"
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
            "value",
            {
              "generic": "V"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   360:     ///\n   361:     /// # Examples\n   362:     ///\n   363:     /// ```\n   364:     /// use std::collections::BTreeMap;\n   365:     /// use std::collections::btree_map::Entry;\n   366:     ///\n   367:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   368:     ///\n   369:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   370:     ///     o.insert(37);\n   371:     /// }\n   372:     /// assert_eq!(map[\"poneyland\"], 37);\n   373:     /// ```\n   374:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   375:     #[rustc_confusables(\"push\", \"put\")]\n   376:     pub fn insert(self, value: V) -> &'a mut V {\n   377:         self.insert_entry(value).into_mut()\n   378:     }\n   379: \n   380:     /// Sets the value of the entry with the `VacantEntry`'s key,\n   381:     /// and returns an `OccupiedEntry`.\n   382:     ///\n   383:     /// # Examples\n   384:     ///\n   385:     /// ```\n   386:     /// use std::collections::BTreeMap;\n   387:     /// use std::collections::btree_map::Entry;\n   388:     ///\n   389:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   390:     ///\n   391:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   392:     ///     let entry = o.insert_entry(37);",
    "nanvix_source": "   415:     ///\n   416:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   417:     ///\n   418:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   419:     ///     o.insert(37);\n   420:     /// }\n   421:     /// assert_eq!(map[\"poneyland\"], 37);\n   422:     /// ```\n   423:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   424:     #[rustc_confusables(\"push\", \"put\")]\n   425:     pub fn insert(self, value: V) -> &'a mut V {\n   426:         self.insert_entry(value).into_mut()\n   427:     }\n   428: \n   429:     /// Sets the value of the entry with the `VacantEntry`'s key,\n   430:     /// and returns an `OccupiedEntry`.\n   431:     ///\n   432:     /// # Examples\n   433:     ///\n   434:     /// ```\n   435:     /// use std::collections::BTreeMap;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 302,
            "path": "Rc"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 29,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
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
        "impl_id": "alloc:3610",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
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
    "verification_source": "  1914:     /// [clone]: Clone::clone\n  1915:     ///\n  1916:     /// # Examples\n  1917:     ///\n  1918:     /// ```\n  1919:     /// use std::rc::Rc;\n  1920:     ///\n  1921:     /// let mut x = Rc::new(3);\n  1922:     /// *Rc::get_mut(&mut x).unwrap() = 4;\n  1923:     /// assert_eq!(*x, 4);\n  1924:     ///\n  1925:     /// let _y = Rc::clone(&x);\n  1926:     /// assert!(Rc::get_mut(&mut x).is_none());\n  1927:     /// ```\n  1928:     #[inline]\n  1929:     #[stable(feature = \"rc_unique\", since = \"1.4.0\")]\n  1930:     pub fn get_mut(this: &mut Self) -> Option<&mut T> {\n  1931:         if Rc::is_unique(this) { unsafe { Some(Rc::get_mut_unchecked(this)) } } else { None }\n  1932:     }\n  1933: \n  1934:     /// Returns a mutable reference into the given `Rc`,\n  1935:     /// without any check.\n  1936:     ///\n  1937:     /// See also [`get_mut`], which is safe and does appropriate checks.\n  1938:     ///\n  1939:     /// [`get_mut`]: Rc::get_mut\n  1940:     ///\n  1941:     /// # Safety\n  1942:     ///\n  1943:     /// If any other `Rc` or [`Weak`] pointers to the same allocation exist, then\n  1944:     /// they must not be dereferenced or have active borrows for the duration\n  1945:     /// of the returned borrow, and their inner type must be exactly the same as the\n  1946:     /// inner type of this Rc (including lifetimes). This is trivially the case if no",
    "nanvix_source": "  1926:     ///\n  1927:     /// let mut x = Rc::new(3);\n  1928:     /// *Rc::get_mut(&mut x).unwrap() = 4;\n  1929:     /// assert_eq!(*x, 4);\n  1930:     ///\n  1931:     /// let _y = Rc::clone(&x);\n  1932:     /// assert!(Rc::get_mut(&mut x).is_none());\n  1933:     /// ```\n  1934:     #[inline]\n  1935:     #[stable(feature = \"rc_unique\", since = \"1.4.0\")]\n  1936:     pub fn get_mut(this: &mut Self) -> Option<&mut T> {\n  1937:         if Rc::is_unique(this) { unsafe { Some(Rc::get_mut_unchecked(this)) } } else { None }\n  1938:     }\n  1939: \n  1940:     /// Returns a mutable reference into the given `Rc`,\n  1941:     /// without any check.\n  1942:     ///\n  1943:     /// See also [`get_mut`], which is safe and does appropriate checks.\n  1944:     ///\n  1945:     /// [`get_mut`]: Rc::get_mut\n  1946:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::make_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "make_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 302,
            "path": "Rc"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 29,
                          "path": "Sized"
                        }
                      }
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 36,
                          "path": "CloneToUninit"
                        }
                      }
                    }
                  ],
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
        "impl_id": "alloc:3611",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2062:     /// ```\n  2063:     /// use std::rc::Rc;\n  2064:     ///\n  2065:     /// let mut data = Rc::new(75);\n  2066:     /// let weak = Rc::downgrade(&data);\n  2067:     ///\n  2068:     /// assert!(75 == *data);\n  2069:     /// assert!(75 == *weak.upgrade().unwrap());\n  2070:     ///\n  2071:     /// *Rc::make_mut(&mut data) += 1;\n  2072:     ///\n  2073:     /// assert!(76 == *data);\n  2074:     /// assert!(weak.upgrade().is_none());\n  2075:     /// ```\n  2076:     #[inline]\n  2077:     #[stable(feature = \"rc_unique\", since = \"1.4.0\")]\n  2078:     pub fn make_mut(this: &mut Self) -> &mut T {\n  2079:         let size_of_val = size_of_val::<T>(&**this);\n  2080: \n  2081:         if Rc::strong_count(this) != 1 {\n  2082:             // Gotta clone the data, there are other Rcs.\n  2083:             *this = Rc::clone_from_ref_in(&**this, this.alloc.clone());\n  2084:         } else if Rc::weak_count(this) != 0 {\n  2085:             // Can just steal the data, all that's left is Weaks\n  2086: \n  2087:             // We don't need panic-protection like the above branch does, but we might as well\n  2088:             // use the same mechanism.\n  2089:             let mut in_progress: UniqueRcUninit<T, A> =\n  2090:                 UniqueRcUninit::new(&**this, this.alloc.clone());\n  2091:             unsafe {\n  2092:                 // Initialize `in_progress` with move of **this.\n  2093:                 // We have to express this in terms of bytes because `T: ?Sized`; there is no\n  2094:                 // operation that just copies a value based on its `size_of_val()`.",
    "nanvix_source": "  2074:     /// assert!(75 == *data);\n  2075:     /// assert!(75 == *weak.upgrade().unwrap());\n  2076:     ///\n  2077:     /// *Rc::make_mut(&mut data) += 1;\n  2078:     ///\n  2079:     /// assert!(76 == *data);\n  2080:     /// assert!(weak.upgrade().is_none());\n  2081:     /// ```\n  2082:     #[inline]\n  2083:     #[stable(feature = \"rc_unique\", since = \"1.4.0\")]\n  2084:     pub fn make_mut(this: &mut Self) -> &mut T {\n  2085:         let size_of_val = size_of_val::<T>(&**this);\n  2086: \n  2087:         if Rc::strong_count(this) != 1 {\n  2088:             // Gotta clone the data, there are other Rcs.\n  2089:             *this = Rc::clone_from_ref_in(&**this, this.alloc.clone());\n  2090:         } else if Rc::weak_count(this) != 0 {\n  2091:             // Can just steal the data, all that's left is Weaks\n  2092: \n  2093:             // We don't need panic-protection like the above branch does, but we might as well\n  2094:             // use the same mechanism.",
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
