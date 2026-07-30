For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::key",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "key",
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
              "generic": "K"
            }
          }
        }
      }
    },
    "verification_source": "   431: }\n   432: \n   433: impl<'a, K: Ord, V, A: Allocator + Clone> OccupiedEntry<'a, K, V, A> {\n   434:     /// Gets a reference to the key in the entry.\n   435:     ///\n   436:     /// # Examples\n   437:     ///\n   438:     /// ```\n   439:     /// use std::collections::BTreeMap;\n   440:     ///\n   441:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   442:     /// map.entry(\"poneyland\").or_insert(12);\n   443:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   444:     /// ```\n   445:     #[must_use]\n   446:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   447:     pub fn key(&self) -> &K {\n   448:         self.handle.reborrow().into_kv().0\n   449:     }\n   450: \n   451:     /// Converts the entry into a reference to its key.\n   452:     pub(crate) fn into_key(self) -> &'a K {\n   453:         self.handle.into_kv_mut().0\n   454:     }\n   455: \n   456:     /// Take ownership of the key and value from the map.\n   457:     ///\n   458:     /// # Examples\n   459:     ///\n   460:     /// ```\n   461:     /// use std::collections::BTreeMap;\n   462:     /// use std::collections::btree_map::Entry;\n   463:     ///",
    "nanvix_source": "   486:     ///\n   487:     /// ```\n   488:     /// use std::collections::BTreeMap;\n   489:     ///\n   490:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   491:     /// map.entry(\"poneyland\").or_insert(12);\n   492:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   493:     /// ```\n   494:     #[must_use]\n   495:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   496:     pub fn key(&self) -> &K {\n   497:         self.handle.reborrow().into_kv().0\n   498:     }\n   499: \n   500:     /// Converts the entry into a reference to its key.\n   501:     pub(crate) fn into_key(self) -> &'a K {\n   502:         self.handle.into_kv_mut().0\n   503:     }\n   504: \n   505:     /// Take ownership of the key and value from the map.\n   506:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::remove",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "remove",
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
          "generic": "V"
        }
      }
    },
    "verification_source": "   572:     ///     assert_eq!(o.insert(15), 12);\n   573:     /// }\n   574:     /// assert_eq!(map[\"poneyland\"], 15);\n   575:     /// ```\n   576:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   577:     #[rustc_confusables(\"push\", \"put\")]\n   578:     pub fn insert(&mut self, value: V) -> V {\n   579:         mem::replace(self.get_mut(), value)\n   580:     }\n   581: \n   582:     /// Takes the value of the entry out of the map, and returns it.\n   583:     ///\n   584:     /// # Examples\n   585:     ///\n   586:     /// ```\n   587:     /// use std::collections::BTreeMap;\n   588:     /// use std::collections::btree_map::Entry;\n   589:     ///\n   590:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   591:     /// map.entry(\"poneyland\").or_insert(12);\n   592:     ///\n   593:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   594:     ///     assert_eq!(o.remove(), 12);\n   595:     /// }\n   596:     /// // If we try to get \"poneyland\"'s value, it'll panic:\n   597:     /// // println!(\"{}\", map[\"poneyland\"]);\n   598:     /// ```\n   599:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   600:     #[rustc_confusables(\"delete\", \"take\")]\n   601:     pub fn remove(self) -> V {\n   602:         self.remove_kv().1\n   603:     }\n   604: ",
    "nanvix_source": "   627:     pub fn insert(&mut self, value: V) -> V {\n   628:         mem::replace(self.get_mut(), value)\n   629:     }\n   630: \n   631:     /// Takes the value of the entry out of the map, and returns it.\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```\n   636:     /// use std::collections::BTreeMap;\n   637:     /// use std::collections::btree_map::Entry;\n   638:     ///\n   639:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   640:     /// map.entry(\"poneyland\").or_insert(12);\n   641:     ///\n   642:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   643:     ///     assert_eq!(o.remove(), 12);\n   644:     /// }\n   645:     /// // If we try to get \"poneyland\"'s value, it'll panic:\n   646:     /// // println!(\"{}\", map[\"poneyland\"]);\n   647:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::remove_entry",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "remove_entry",
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
          "tuple": [
            {
              "generic": "K"
            },
            {
              "generic": "V"
            }
          ]
        }
      }
    },
    "verification_source": "   460:     /// ```\n   461:     /// use std::collections::BTreeMap;\n   462:     /// use std::collections::btree_map::Entry;\n   463:     ///\n   464:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   465:     /// map.entry(\"poneyland\").or_insert(12);\n   466:     ///\n   467:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   468:     ///     // We delete the entry from the map.\n   469:     ///     o.remove_entry();\n   470:     /// }\n   471:     ///\n   472:     /// // If now try to get the value, it will panic:\n   473:     /// // println!(\"{}\", map[\"poneyland\"]);\n   474:     /// ```\n   475:     #[stable(feature = \"map_entry_recover_keys2\", since = \"1.12.0\")]\n   476:     pub fn remove_entry(self) -> (K, V) {\n   477:         self.remove_kv()\n   478:     }\n   479: \n   480:     /// Gets a reference to the value in the entry.\n   481:     ///\n   482:     /// # Examples\n   483:     ///\n   484:     /// ```\n   485:     /// use std::collections::BTreeMap;\n   486:     /// use std::collections::btree_map::Entry;\n   487:     ///\n   488:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   489:     /// map.entry(\"poneyland\").or_insert(12);\n   490:     ///\n   491:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   492:     ///     assert_eq!(o.get(), &12);",
    "nanvix_source": "   515:     ///\n   516:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   517:     ///     // We delete the entry from the map.\n   518:     ///     o.remove_entry();\n   519:     /// }\n   520:     ///\n   521:     /// // If now try to get the value, it will panic:\n   522:     /// // println!(\"{}\", map[\"poneyland\"]);\n   523:     /// ```\n   524:     #[stable(feature = \"map_entry_recover_keys2\", since = \"1.12.0\")]\n   525:     pub fn remove_entry(self) -> (K, V) {\n   526:         self.remove_kv()\n   527:     }\n   528: \n   529:     /// Gets a reference to the value in the entry.\n   530:     ///\n   531:     /// # Examples\n   532:     ///\n   533:     /// ```\n   534:     /// use std::collections::BTreeMap;\n   535:     /// use std::collections::btree_map::Entry;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::VacantEntry::insert_entry",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "insert_entry",
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
        }
      }
    },
    "verification_source": "   382:     ///\n   383:     /// # Examples\n   384:     ///\n   385:     /// ```\n   386:     /// use std::collections::BTreeMap;\n   387:     /// use std::collections::btree_map::Entry;\n   388:     ///\n   389:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   390:     ///\n   391:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   392:     ///     let entry = o.insert_entry(37);\n   393:     ///     assert_eq!(entry.get(), &37);\n   394:     /// }\n   395:     /// assert_eq!(map[\"poneyland\"], 37);\n   396:     /// ```\n   397:     #[stable(feature = \"btree_entry_insert\", since = \"1.92.0\")]\n   398:     pub fn insert_entry(mut self, value: V) -> OccupiedEntry<'a, K, V, A> {\n   399:         let handle = match self.handle {\n   400:             None => {\n   401:                 // SAFETY: There is no tree yet so no reference to it exists.\n   402:                 let map = unsafe { self.dormant_map.reborrow() };\n   403:                 let root = map.root.insert(NodeRef::new_leaf(self.alloc.clone()).forget_type());\n   404:                 // SAFETY: We *just* created the root as a leaf, and we're\n   405:                 // stacking the new handle on the original borrow lifetime.\n   406:                 unsafe {\n   407:                     let mut leaf = root.borrow_mut().cast_to_leaf_unchecked();\n   408:                     leaf.push_with_handle(self.key, value)\n   409:                 }\n   410:             }\n   411:             Some(handle) => handle.insert_recursing(self.key, value, self.alloc.clone(), |ins| {\n   412:                 drop(ins.left);\n   413:                 // SAFETY: Pushing a new root node doesn't invalidate\n   414:                 // handles to existing nodes.",
    "nanvix_source": "   437:     ///\n   438:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   439:     ///\n   440:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   441:     ///     let entry = o.insert_entry(37);\n   442:     ///     assert_eq!(entry.get(), &37);\n   443:     /// }\n   444:     /// assert_eq!(map[\"poneyland\"], 37);\n   445:     /// ```\n   446:     #[stable(feature = \"btree_entry_insert\", since = \"1.92.0\")]\n   447:     pub fn insert_entry(mut self, value: V) -> OccupiedEntry<'a, K, V, A> {\n   448:         let handle = match self.handle {\n   449:             None => {\n   450:                 // SAFETY: There is no tree yet so no reference to it exists.\n   451:                 let map = unsafe { self.dormant_map.reborrow() };\n   452:                 let root = map.root.insert(NodeRef::new_leaf(self.alloc.clone()).forget_type());\n   453:                 // SAFETY: We *just* created the root as a leaf, and we're\n   454:                 // stacking the new handle on the original borrow lifetime.\n   455:                 unsafe {\n   456:                     let mut leaf = root.borrow_mut().cast_to_leaf_unchecked();\n   457:                     leaf.push_with_handle(self.key, value)",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::VacantEntry::into_key",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "into_key",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "K"
        }
      }
    },
    "verification_source": "   338: \n   339:     /// Take ownership of the key.\n   340:     ///\n   341:     /// # Examples\n   342:     ///\n   343:     /// ```\n   344:     /// use std::collections::BTreeMap;\n   345:     /// use std::collections::btree_map::Entry;\n   346:     ///\n   347:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   348:     ///\n   349:     /// if let Entry::Vacant(v) = map.entry(\"poneyland\") {\n   350:     ///     v.into_key();\n   351:     /// }\n   352:     /// ```\n   353:     #[stable(feature = \"map_entry_recover_keys2\", since = \"1.12.0\")]\n   354:     pub fn into_key(self) -> K {\n   355:         self.key\n   356:     }\n   357: \n   358:     /// Sets the value of the entry with the `VacantEntry`'s key,\n   359:     /// and returns a mutable reference to it.\n   360:     ///\n   361:     /// # Examples\n   362:     ///\n   363:     /// ```\n   364:     /// use std::collections::BTreeMap;\n   365:     /// use std::collections::btree_map::Entry;\n   366:     ///\n   367:     /// let mut map: BTreeMap<&str, u32> = BTreeMap::new();\n   368:     ///\n   369:     /// if let Entry::Vacant(o) = map.entry(\"poneyland\") {\n   370:     ///     o.insert(37);",
    "nanvix_source": "   393:     /// use std::collections::BTreeMap;\n   394:     /// use std::collections::btree_map::Entry;\n   395:     ///\n   396:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   397:     ///\n   398:     /// if let Entry::Vacant(v) = map.entry(\"poneyland\") {\n   399:     ///     v.into_key();\n   400:     /// }\n   401:     /// ```\n   402:     #[stable(feature = \"map_entry_recover_keys2\", since = \"1.12.0\")]\n   403:     pub fn into_key(self) -> K {\n   404:         self.key\n   405:     }\n   406: \n   407:     /// Sets the value of the entry with the `VacantEntry`'s key,\n   408:     /// and returns a mutable reference to it.\n   409:     ///\n   410:     /// # Examples\n   411:     ///\n   412:     /// ```\n   413:     /// use std::collections::BTreeMap;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::VacantEntry::key",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "key",
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
              "generic": "K"
            }
          }
        }
      }
    },
    "verification_source": "   319:     }\n   320: }\n   321: \n   322: impl<'a, K: Ord, V, A: Allocator + Clone> VacantEntry<'a, K, V, A> {\n   323:     /// Gets a reference to the key that would be used when inserting a value\n   324:     /// through the VacantEntry.\n   325:     ///\n   326:     /// # Examples\n   327:     ///\n   328:     /// ```\n   329:     /// use std::collections::BTreeMap;\n   330:     ///\n   331:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   332:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   333:     /// ```\n   334:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   335:     pub fn key(&self) -> &K {\n   336:         &self.key\n   337:     }\n   338: \n   339:     /// Take ownership of the key.\n   340:     ///\n   341:     /// # Examples\n   342:     ///\n   343:     /// ```\n   344:     /// use std::collections::BTreeMap;\n   345:     /// use std::collections::btree_map::Entry;\n   346:     ///\n   347:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   348:     ///\n   349:     /// if let Entry::Vacant(v) = map.entry(\"poneyland\") {\n   350:     ///     v.into_key();\n   351:     /// }",
    "nanvix_source": "   374:     ///\n   375:     /// # Examples\n   376:     ///\n   377:     /// ```\n   378:     /// use std::collections::BTreeMap;\n   379:     ///\n   380:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   381:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   382:     /// ```\n   383:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   384:     pub fn key(&self) -> &K {\n   385:         &self.key\n   386:     }\n   387: \n   388:     /// Take ownership of the key.\n   389:     ///\n   390:     /// # Examples\n   391:     ///\n   392:     /// ```\n   393:     /// use std::collections::BTreeMap;\n   394:     /// use std::collections::btree_map::Entry;",
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
