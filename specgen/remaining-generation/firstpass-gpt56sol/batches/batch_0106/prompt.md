For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::swap_remove_back",
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
      "name": "swap_remove_back",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "index",
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
    "verification_source": "  2356:     /// # Examples\n  2357:     ///\n  2358:     /// ```\n  2359:     /// use std::collections::VecDeque;\n  2360:     ///\n  2361:     /// let mut buf = VecDeque::new();\n  2362:     /// assert_eq!(buf.swap_remove_back(0), None);\n  2363:     /// buf.push_back(1);\n  2364:     /// buf.push_back(2);\n  2365:     /// buf.push_back(3);\n  2366:     /// assert_eq!(buf, [1, 2, 3]);\n  2367:     ///\n  2368:     /// assert_eq!(buf.swap_remove_back(0), Some(1));\n  2369:     /// assert_eq!(buf, [3, 2]);\n  2370:     /// ```\n  2371:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  2372:     pub fn swap_remove_back(&mut self, index: usize) -> Option<T> {\n  2373:         let length = self.len;\n  2374:         if length > 0 && index < length - 1 {\n  2375:             self.swap(index, length - 1);\n  2376:         } else if index >= length {\n  2377:             return None;\n  2378:         }\n  2379:         self.pop_back()\n  2380:     }\n  2381: \n  2382:     /// Inserts an element at `index` within the deque, shifting all elements\n  2383:     /// with indices greater than or equal to `index` towards the back.\n  2384:     ///\n  2385:     /// Element at index 0 is the front of the queue.\n  2386:     ///\n  2387:     /// # Panics\n  2388:     ///",
    "nanvix_source": "  2426:     /// assert_eq!(buf.swap_remove_back(0), None);\n  2427:     /// buf.push_back(1);\n  2428:     /// buf.push_back(2);\n  2429:     /// buf.push_back(3);\n  2430:     /// assert_eq!(buf, [1, 2, 3]);\n  2431:     ///\n  2432:     /// assert_eq!(buf.swap_remove_back(0), Some(1));\n  2433:     /// assert_eq!(buf, [3, 2]);\n  2434:     /// ```\n  2435:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  2436:     pub fn swap_remove_back(&mut self, index: usize) -> Option<T> {\n  2437:         let length = self.len;\n  2438:         if length > 0 && index < length - 1 {\n  2439:             self.swap(index, length - 1);\n  2440:         } else if index >= length {\n  2441:             return None;\n  2442:         }\n  2443:         self.pop_back()\n  2444:     }\n  2445: \n  2446:     /// Inserts an element at `index` within the deque, shifting all elements",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::swap_remove_front",
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
      "name": "swap_remove_front",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "index",
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
    "verification_source": "  2321:     /// # Examples\n  2322:     ///\n  2323:     /// ```\n  2324:     /// use std::collections::VecDeque;\n  2325:     ///\n  2326:     /// let mut buf = VecDeque::new();\n  2327:     /// assert_eq!(buf.swap_remove_front(0), None);\n  2328:     /// buf.push_back(1);\n  2329:     /// buf.push_back(2);\n  2330:     /// buf.push_back(3);\n  2331:     /// assert_eq!(buf, [1, 2, 3]);\n  2332:     ///\n  2333:     /// assert_eq!(buf.swap_remove_front(2), Some(3));\n  2334:     /// assert_eq!(buf, [2, 1]);\n  2335:     /// ```\n  2336:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  2337:     pub fn swap_remove_front(&mut self, index: usize) -> Option<T> {\n  2338:         let length = self.len;\n  2339:         if index < length && index != 0 {\n  2340:             self.swap(index, 0);\n  2341:         } else if index >= length {\n  2342:             return None;\n  2343:         }\n  2344:         self.pop_front()\n  2345:     }\n  2346: \n  2347:     /// Removes an element from anywhere in the deque and returns it,\n  2348:     /// replacing it with the last element.\n  2349:     ///\n  2350:     /// This does not preserve ordering, but is *O*(1).\n  2351:     ///\n  2352:     /// Returns `None` if `index` is out of bounds.\n  2353:     ///",
    "nanvix_source": "  2391:     /// assert_eq!(buf.swap_remove_front(0), None);\n  2392:     /// buf.push_back(1);\n  2393:     /// buf.push_back(2);\n  2394:     /// buf.push_back(3);\n  2395:     /// assert_eq!(buf, [1, 2, 3]);\n  2396:     ///\n  2397:     /// assert_eq!(buf.swap_remove_front(2), Some(3));\n  2398:     /// assert_eq!(buf, [2, 1]);\n  2399:     /// ```\n  2400:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  2401:     pub fn swap_remove_front(&mut self, index: usize) -> Option<T> {\n  2402:         let length = self.len;\n  2403:         if index < length && index != 0 {\n  2404:             self.swap(index, 0);\n  2405:         } else if index >= length {\n  2406:             return None;\n  2407:         }\n  2408:         self.pop_front()\n  2409:     }\n  2410: \n  2411:     /// Removes an element from anywhere in the deque and returns it,",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::Entry::insert_entry",
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
    "verification_source": "   272:     }\n   273: \n   274:     /// Sets the value of the entry, and returns an `OccupiedEntry`.\n   275:     ///\n   276:     /// # Examples\n   277:     ///\n   278:     /// ```\n   279:     /// use std::collections::BTreeMap;\n   280:     ///\n   281:     /// let mut map: BTreeMap<&str, String> = BTreeMap::new();\n   282:     /// let entry = map.entry(\"poneyland\").insert_entry(\"hoho\".to_string());\n   283:     ///\n   284:     /// assert_eq!(entry.key(), &\"poneyland\");\n   285:     /// ```\n   286:     #[inline]\n   287:     #[stable(feature = \"btree_entry_insert\", since = \"1.92.0\")]\n   288:     pub fn insert_entry(self, value: V) -> OccupiedEntry<'a, K, V, A> {\n   289:         match self {\n   290:             Occupied(mut entry) => {\n   291:                 entry.insert(value);\n   292:                 entry\n   293:             }\n   294:             Vacant(entry) => entry.insert_entry(value),\n   295:         }\n   296:     }\n   297: }\n   298: \n   299: impl<'a, K: Ord, V: Default, A: Allocator + Clone> Entry<'a, K, V, A> {\n   300:     #[stable(feature = \"entry_or_default\", since = \"1.28.0\")]\n   301:     /// Ensures a value is in the entry by inserting the default value if empty,\n   302:     /// and returns a mutable reference to the value in the entry.\n   303:     ///\n   304:     /// # Examples",
    "nanvix_source": "   327:     /// ```\n   328:     /// use std::collections::BTreeMap;\n   329:     ///\n   330:     /// let mut map: BTreeMap<&str, String> = BTreeMap::new();\n   331:     /// let entry = map.entry(\"poneyland\").insert_entry(\"hoho\".to_string());\n   332:     ///\n   333:     /// assert_eq!(entry.key(), &\"poneyland\");\n   334:     /// ```\n   335:     #[inline]\n   336:     #[stable(feature = \"btree_entry_insert\", since = \"1.92.0\")]\n   337:     pub fn insert_entry(self, value: V) -> OccupiedEntry<'a, K, V, A> {\n   338:         match self {\n   339:             Occupied(mut entry) => {\n   340:                 entry.insert(value);\n   341:                 entry\n   342:             }\n   343:             Vacant(entry) => entry.insert_entry(value),\n   344:         }\n   345:     }\n   346: }\n   347: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::Entry::key",
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
    "verification_source": "   217:                 entry.insert(value)\n   218:             }\n   219:         }\n   220:     }\n   221: \n   222:     /// Returns a reference to this entry's key.\n   223:     ///\n   224:     /// # Examples\n   225:     ///\n   226:     /// ```\n   227:     /// use std::collections::BTreeMap;\n   228:     ///\n   229:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   230:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   231:     /// ```\n   232:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   233:     pub fn key(&self) -> &K {\n   234:         match *self {\n   235:             Occupied(ref entry) => entry.key(),\n   236:             Vacant(ref entry) => entry.key(),\n   237:         }\n   238:     }\n   239: \n   240:     /// Provides in-place mutable access to an occupied entry before any\n   241:     /// potential inserts into the map.\n   242:     ///\n   243:     /// # Examples\n   244:     ///\n   245:     /// ```\n   246:     /// use std::collections::BTreeMap;\n   247:     ///\n   248:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   249:     ///",
    "nanvix_source": "   272:     ///\n   273:     /// # Examples\n   274:     ///\n   275:     /// ```\n   276:     /// use std::collections::BTreeMap;\n   277:     ///\n   278:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   279:     /// assert_eq!(map.entry(\"poneyland\").key(), &\"poneyland\");\n   280:     /// ```\n   281:     #[stable(feature = \"map_entry_keys\", since = \"1.10.0\")]\n   282:     pub fn key(&self) -> &K {\n   283:         match *self {\n   284:             Occupied(ref entry) => entry.key(),\n   285:             Vacant(ref entry) => entry.key(),\n   286:         }\n   287:     }\n   288: \n   289:     /// Provides in-place mutable access to an occupied entry before any\n   290:     /// potential inserts into the map.\n   291:     ///\n   292:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::get",
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
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   481:     ///\n   482:     /// # Examples\n   483:     ///\n   484:     /// ```\n   485:     /// use std::collections::BTreeMap;\n   486:     /// use std::collections::btree_map::Entry;\n   487:     ///\n   488:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   489:     /// map.entry(\"poneyland\").or_insert(12);\n   490:     ///\n   491:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   492:     ///     assert_eq!(o.get(), &12);\n   493:     /// }\n   494:     /// ```\n   495:     #[must_use]\n   496:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   497:     pub fn get(&self) -> &V {\n   498:         self.handle.reborrow().into_kv().1\n   499:     }\n   500: \n   501:     /// Gets a mutable reference to the value in the entry.\n   502:     ///\n   503:     /// If you need a reference to the `OccupiedEntry` that may outlive the\n   504:     /// destruction of the `Entry` value, see [`into_mut`].\n   505:     ///\n   506:     /// [`into_mut`]: OccupiedEntry::into_mut\n   507:     ///\n   508:     /// # Examples\n   509:     ///\n   510:     /// ```\n   511:     /// use std::collections::BTreeMap;\n   512:     /// use std::collections::btree_map::Entry;\n   513:     ///",
    "nanvix_source": "   536:     ///\n   537:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   538:     /// map.entry(\"poneyland\").or_insert(12);\n   539:     ///\n   540:     /// if let Entry::Occupied(o) = map.entry(\"poneyland\") {\n   541:     ///     assert_eq!(o.get(), &12);\n   542:     /// }\n   543:     /// ```\n   544:     #[must_use]\n   545:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   546:     pub fn get(&self) -> &V {\n   547:         self.handle.reborrow().into_kv().1\n   548:     }\n   549: \n   550:     /// Gets a mutable reference to the value in the entry.\n   551:     ///\n   552:     /// If you need a reference to the `OccupiedEntry` that may outlive the\n   553:     /// destruction of the `Entry` value, see [`into_mut`].\n   554:     ///\n   555:     /// [`into_mut`]: OccupiedEntry::into_mut\n   556:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::OccupiedEntry::insert",
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
      "name": "insert",
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
          "generic": "V"
        }
      }
    },
    "verification_source": "   560:     /// and returns the entry's old value.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// use std::collections::BTreeMap;\n   566:     /// use std::collections::btree_map::Entry;\n   567:     ///\n   568:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   569:     /// map.entry(\"poneyland\").or_insert(12);\n   570:     ///\n   571:     /// if let Entry::Occupied(mut o) = map.entry(\"poneyland\") {\n   572:     ///     assert_eq!(o.insert(15), 12);\n   573:     /// }\n   574:     /// assert_eq!(map[\"poneyland\"], 15);\n   575:     /// ```\n   576:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   577:     #[rustc_confusables(\"push\", \"put\")]\n   578:     pub fn insert(&mut self, value: V) -> V {\n   579:         mem::replace(self.get_mut(), value)\n   580:     }\n   581: \n   582:     /// Takes the value of the entry out of the map, and returns it.\n   583:     ///\n   584:     /// # Examples\n   585:     ///\n   586:     /// ```\n   587:     /// use std::collections::BTreeMap;\n   588:     /// use std::collections::btree_map::Entry;\n   589:     ///\n   590:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   591:     /// map.entry(\"poneyland\").or_insert(12);\n   592:     ///",
    "nanvix_source": "   615:     /// use std::collections::btree_map::Entry;\n   616:     ///\n   617:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   618:     /// map.entry(\"poneyland\").or_insert(12);\n   619:     ///\n   620:     /// if let Entry::Occupied(mut o) = map.entry(\"poneyland\") {\n   621:     ///     assert_eq!(o.insert(15), 12);\n   622:     /// }\n   623:     /// assert_eq!(map[\"poneyland\"], 15);\n   624:     /// ```\n   625:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   626:     #[rustc_confusables(\"push\", \"put\")]\n   627:     pub fn insert(&mut self, value: V) -> V {\n   628:         mem::replace(self.get_mut(), value)\n   629:     }\n   630: \n   631:     /// Takes the value of the entry out of the map, and returns it.\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```",
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
