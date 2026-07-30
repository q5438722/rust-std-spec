For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::LocalKey::replace",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "multiple_rust_declarations_share_path"
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
      "name": "replace",
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
                        "id": 363,
                        "path": "crate::cell::Cell"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:379",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "value",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   600:     /// and it **may** panic if the destructor has previously been run for this thread.\n   601:     ///\n   602:     /// # Examples\n   603:     ///\n   604:     /// ```\n   605:     /// use std::cell::Cell;\n   606:     ///\n   607:     /// thread_local! {\n   608:     ///     static X: Cell<i32> = const { Cell::new(1) };\n   609:     /// }\n   610:     ///\n   611:     /// assert_eq!(X.replace(2), 1);\n   612:     /// assert_eq!(X.replace(3), 2);\n   613:     /// ```\n   614:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   615:     #[rustc_confusables(\"swap\")]\n   616:     pub fn replace(&'static self, value: T) -> T {\n   617:         self.with(|cell| cell.replace(value))\n   618:     }\n   619: \n   620:     /// Updates the contained value using a function.\n   621:     ///\n   622:     /// # Examples\n   623:     ///\n   624:     /// ```\n   625:     /// #![feature(local_key_cell_update)]\n   626:     /// use std::cell::Cell;\n   627:     ///\n   628:     /// thread_local! {\n   629:     ///     static X: Cell<i32> = const { Cell::new(5) };\n   630:     /// }\n   631:     ///\n   632:     /// X.update(|x| x + 1);",
    "nanvix_source": "   607:     ///\n   608:     /// thread_local! {\n   609:     ///     static X: Cell<i32> = const { Cell::new(1) };\n   610:     /// }\n   611:     ///\n   612:     /// assert_eq!(X.replace(2), 1);\n   613:     /// assert_eq!(X.replace(3), 2);\n   614:     /// ```\n   615:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   616:     #[rustc_confusables(\"swap\")]\n   617:     pub fn replace(&'static self, value: T) -> T {\n   618:         self.with(|cell| cell.replace(value))\n   619:     }\n   620: \n   621:     /// Updates the contained value using a function.\n   622:     ///\n   623:     /// This will lazily initialize the value if this thread has not referenced\n   624:     /// this key yet.\n   625:     ///\n   626:     /// # Panics\n   627:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::set",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "unit_return_variant",
      "multiple_rust_declarations_share_path"
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
      "name": "set",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
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
                        "id": 363,
                        "path": "crate::cell::Cell"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:379",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "value",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   506:     /// # Examples\n   507:     ///\n   508:     /// ```\n   509:     /// use std::cell::Cell;\n   510:     ///\n   511:     /// thread_local! {\n   512:     ///     static X: Cell<i32> = panic!(\"!\");\n   513:     /// }\n   514:     ///\n   515:     /// // Calling X.get() here would result in a panic.\n   516:     ///\n   517:     /// X.set(123); // But X.set() is fine, as it skips the initializer above.\n   518:     ///\n   519:     /// assert_eq!(X.get(), 123);\n   520:     /// ```\n   521:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   522:     pub fn set(&'static self, value: T) {\n   523:         self.initialize_with(Cell::new(value), |value, cell| {\n   524:             if let Some(value) = value {\n   525:                 // The cell was already initialized, so `value` wasn't used to\n   526:                 // initialize it. So we overwrite the current value with the\n   527:                 // new one instead.\n   528:                 cell.set(value.into_inner());\n   529:             }\n   530:         });\n   531:     }\n   532: \n   533:     /// Returns a copy of the contained value.\n   534:     ///\n   535:     /// This will lazily initialize the value if this thread has not referenced\n   536:     /// this key yet.\n   537:     ///\n   538:     /// # Panics",
    "nanvix_source": "   513:     ///     static X: Cell<i32> = panic!(\"!\");\n   514:     /// }\n   515:     ///\n   516:     /// // Calling X.get() here would result in a panic.\n   517:     ///\n   518:     /// X.set(123); // But X.set() is fine, as it skips the initializer above.\n   519:     ///\n   520:     /// assert_eq!(X.get(), 123);\n   521:     /// ```\n   522:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   523:     pub fn set(&'static self, value: T) {\n   524:         self.initialize_with(Cell::new(value), |value, cell| {\n   525:             if let Some(value) = value {\n   526:                 // The cell was already initialized, so `value` wasn't used to\n   527:                 // initialize it. So we overwrite the current value with the\n   528:                 // new one instead.\n   529:                 cell.set(value.into_inner());\n   530:             }\n   531:         });\n   532:     }\n   533: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::take",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "multiple_rust_declarations_share_path"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
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
                      "id": 132,
                      "path": "Default"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
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
      "name": "take",
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
                        "id": 363,
                        "path": "crate::cell::Cell"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:379",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   569:     /// Panics if the key currently has its destructor running,\n   570:     /// and it **may** panic if the destructor has previously been run for this thread.\n   571:     ///\n   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// use std::cell::Cell;\n   576:     ///\n   577:     /// thread_local! {\n   578:     ///     static X: Cell<Option<i32>> = const { Cell::new(Some(1)) };\n   579:     /// }\n   580:     ///\n   581:     /// assert_eq!(X.take(), Some(1));\n   582:     /// assert_eq!(X.take(), None);\n   583:     /// ```\n   584:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   585:     pub fn take(&'static self) -> T\n   586:     where\n   587:         T: Default,\n   588:     {\n   589:         self.with(Cell::take)\n   590:     }\n   591: \n   592:     /// Replaces the contained value, returning the old value.\n   593:     ///\n   594:     /// This will lazily initialize the value if this thread has not referenced\n   595:     /// this key yet.\n   596:     ///\n   597:     /// # Panics\n   598:     ///\n   599:     /// Panics if the key currently has its destructor running,\n   600:     /// and it **may** panic if the destructor has previously been run for this thread.\n   601:     ///",
    "nanvix_source": "   576:     /// use std::cell::Cell;\n   577:     ///\n   578:     /// thread_local! {\n   579:     ///     static X: Cell<Option<i32>> = const { Cell::new(Some(1)) };\n   580:     /// }\n   581:     ///\n   582:     /// assert_eq!(X.take(), Some(1));\n   583:     /// assert_eq!(X.take(), None);\n   584:     /// ```\n   585:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   586:     pub fn take(&'static self) -> T\n   587:     where\n   588:         T: Default,\n   589:     {\n   590:         self.with(Cell::take)\n   591:     }\n   592: \n   593:     /// Replaces the contained value, returning the old value.\n   594:     ///\n   595:     /// This will lazily initialize the value if this thread has not referenced\n   596:     /// this key yet.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::try_with",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
            "name": "R"
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
                            "generic": "R"
                          }
                        }
                      },
                      "id": 20,
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
      "name": "try_with",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:373",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "R"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 371,
                        "path": "AccessError"
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
    "verification_source": "   441:     /// key's initializer panics.\n   442:     ///\n   443:     /// # Examples\n   444:     ///\n   445:     /// ```\n   446:     /// thread_local! {\n   447:     ///     pub static STATIC: String = String::from(\"I am\");\n   448:     /// }\n   449:     ///\n   450:     /// assert_eq!(\n   451:     ///     STATIC.try_with(|original_value| format!(\"{original_value} initialized\")),\n   452:     ///     Ok(String::from(\"I am initialized\")),\n   453:     /// );\n   454:     /// ```\n   455:     #[stable(feature = \"thread_local_try_with\", since = \"1.26.0\")]\n   456:     #[inline]\n   457:     pub fn try_with<F, R>(&'static self, f: F) -> Result<R, AccessError>\n   458:     where\n   459:         F: FnOnce(&T) -> R,\n   460:     {\n   461:         let thread_local = unsafe { (self.inner)(None).as_ref().ok_or(AccessError)? };\n   462:         Ok(f(thread_local))\n   463:     }\n   464: \n   465:     /// Acquires a reference to the value in this TLS key, initializing it with\n   466:     /// `init` if it wasn't already initialized on this thread.\n   467:     ///\n   468:     /// If `init` was used to initialize the thread local variable, `None` is\n   469:     /// passed as the first argument to `f`. If it was already initialized,\n   470:     /// `Some(init)` is passed to `f`.\n   471:     ///\n   472:     /// # Panics\n   473:     ///",
    "nanvix_source": "   448:     ///     pub static STATIC: String = String::from(\"I am\");\n   449:     /// }\n   450:     ///\n   451:     /// assert_eq!(\n   452:     ///     STATIC.try_with(|original_value| format!(\"{original_value} initialized\")),\n   453:     ///     Ok(String::from(\"I am initialized\")),\n   454:     /// );\n   455:     /// ```\n   456:     #[stable(feature = \"thread_local_try_with\", since = \"1.26.0\")]\n   457:     #[inline]\n   458:     pub fn try_with<F, R>(&'static self, f: F) -> Result<R, AccessError>\n   459:     where\n   460:         F: FnOnce(&T) -> R,\n   461:     {\n   462:         let thread_local = unsafe { (self.inner)(None).as_ref().ok_or(AccessError)? };\n   463:         Ok(f(thread_local))\n   464:     }\n   465: \n   466:     /// Acquires a reference to the value in this TLS key, initializing it with\n   467:     /// `init` if it wasn't already initialized on this thread.\n   468:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::update",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
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
                                "generic": "T"
                              }
                            ],
                            "output": {
                              "generic": "T"
                            }
                          }
                        },
                        "id": 20,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(T) -> T"
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
                      "id": 126,
                      "path": "Copy"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
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
      "name": "update",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
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
                        "id": 363,
                        "path": "crate::cell::Cell"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:379",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "f",
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
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 20,
                      "path": "FnOnce"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   620:     /// Updates the contained value using a function.\n   621:     ///\n   622:     /// # Examples\n   623:     ///\n   624:     /// ```\n   625:     /// #![feature(local_key_cell_update)]\n   626:     /// use std::cell::Cell;\n   627:     ///\n   628:     /// thread_local! {\n   629:     ///     static X: Cell<i32> = const { Cell::new(5) };\n   630:     /// }\n   631:     ///\n   632:     /// X.update(|x| x + 1);\n   633:     /// assert_eq!(X.get(), 6);\n   634:     /// ```\n   635:     #[unstable(feature = \"local_key_cell_update\", issue = \"143989\")]\n   636:     pub fn update(&'static self, f: impl FnOnce(T) -> T)\n   637:     where\n   638:         T: Copy,\n   639:     {\n   640:         self.with(|cell| cell.update(f))\n   641:     }\n   642: }\n   643: \n   644: impl<T: 'static> LocalKey<RefCell<T>> {\n   645:     /// Acquires a reference to the contained value.\n   646:     ///\n   647:     /// This will lazily initialize the value if this thread has not referenced\n   648:     /// this key yet.\n   649:     ///\n   650:     /// # Panics\n   651:     ///\n   652:     /// Panics if the value is currently mutably borrowed.",
    "nanvix_source": "   634:     /// use std::cell::Cell;\n   635:     ///\n   636:     /// thread_local! {\n   637:     ///     static X: Cell<i32> = const { Cell::new(5) };\n   638:     /// }\n   639:     ///\n   640:     /// X.update(|x| x + 1);\n   641:     /// assert_eq!(X.get(), 6);\n   642:     /// ```\n   643:     #[stable(feature = \"local_key_cell_update\", since = \"CURRENT_RUSTC_VERSION\")]\n   644:     pub fn update(&'static self, f: impl FnOnce(T) -> T)\n   645:     where\n   646:         T: Copy,\n   647:     {\n   648:         self.with(|cell| cell.update(f))\n   649:     }\n   650: }\n   651: \n   652: impl<T: 'static> LocalKey<RefCell<T>> {\n   653:     /// Acquires a reference to the contained value.\n   654:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::with",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
            "name": "R"
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
                            "generic": "R"
                          }
                        }
                      },
                      "id": 20,
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
      "name": "with",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:373",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
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
        "output": {
          "generic": "R"
        }
      }
    },
    "verification_source": "   406:     /// destructor running, and it **may** panic if the destructor has\n   407:     /// previously been run for this thread.\n   408:     ///\n   409:     /// # Examples\n   410:     ///\n   411:     /// ```\n   412:     /// thread_local! {\n   413:     ///     pub static STATIC: String = String::from(\"I am\");\n   414:     /// }\n   415:     ///\n   416:     /// assert_eq!(\n   417:     ///     STATIC.with(|original_value| format!(\"{original_value} initialized\")),\n   418:     ///     \"I am initialized\",\n   419:     /// );\n   420:     /// ```\n   421:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   422:     pub fn with<F, R>(&'static self, f: F) -> R\n   423:     where\n   424:         F: FnOnce(&T) -> R,\n   425:     {\n   426:         match self.try_with(f) {\n   427:             Ok(r) => r,\n   428:             Err(err) => panic_access_error(err),\n   429:         }\n   430:     }\n   431: \n   432:     /// Acquires a reference to the value in this TLS key.\n   433:     ///\n   434:     /// This will lazily initialize the value if this thread has not referenced\n   435:     /// this key yet. If the key has been destroyed (which may happen if this is called\n   436:     /// in a destructor), this function will return an [`AccessError`].\n   437:     ///\n   438:     /// # Panics",
    "nanvix_source": "   413:     /// thread_local! {\n   414:     ///     pub static STATIC: String = String::from(\"I am\");\n   415:     /// }\n   416:     ///\n   417:     /// assert_eq!(\n   418:     ///     STATIC.with(|original_value| format!(\"{original_value} initialized\")),\n   419:     ///     \"I am initialized\",\n   420:     /// );\n   421:     /// ```\n   422:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   423:     pub fn with<F, R>(&'static self, f: F) -> R\n   424:     where\n   425:         F: FnOnce(&T) -> R,\n   426:     {\n   427:         match self.try_with(f) {\n   428:             Ok(r) => r,\n   429:             Err(err) => panic_access_error(err),\n   430:         }\n   431:     }\n   432: \n   433:     /// Acquires a reference to the value in this TLS key.",
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
