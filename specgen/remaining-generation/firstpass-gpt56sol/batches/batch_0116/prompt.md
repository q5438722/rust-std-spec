For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::Cell::get",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "get",
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
            "id": 9785,
            "path": "Cell"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 6,
                          "path": "Copy"
                        }
                      }
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
        "impl_id": "core:24745",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   536: impl<T: Copy> Cell<T> {\n   537:     /// Returns a copy of the contained value.\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```\n   542:     /// use std::cell::Cell;\n   543:     ///\n   544:     /// let c = Cell::new(5);\n   545:     ///\n   546:     /// let five = c.get();\n   547:     /// ```\n   548:     #[inline]\n   549:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   550:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   551:     #[rustc_should_not_be_called_on_const_items]\n   552:     pub const fn get(&self) -> T {\n   553:         // SAFETY: This can cause data races if called from a separate thread,\n   554:         // but `Cell` is `!Sync` so this won't happen.\n   555:         unsafe { *self.value.get() }\n   556:     }\n   557: \n   558:     /// Updates the contained value using a function.\n   559:     ///\n   560:     /// # Examples\n   561:     ///\n   562:     /// ```\n   563:     /// use std::cell::Cell;\n   564:     ///\n   565:     /// let c = Cell::new(5);\n   566:     /// c.update(|x| x + 1);\n   567:     /// assert_eq!(c.get(), 6);\n   568:     /// ```",
    "nanvix_source": "   542:     /// use std::cell::Cell;\n   543:     ///\n   544:     /// let c = Cell::new(5);\n   545:     ///\n   546:     /// let five = c.get();\n   547:     /// ```\n   548:     #[inline]\n   549:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   550:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   551:     #[rustc_should_not_be_called_on_const_items]\n   552:     pub const fn get(&self) -> T {\n   553:         // SAFETY: This can cause data races if called from a separate thread,\n   554:         // but `Cell` is `!Sync` so this won't happen.\n   555:         unsafe { *self.value.get() }\n   556:     }\n   557: \n   558:     /// Updates the contained value using a function.\n   559:     ///\n   560:     /// # Examples\n   561:     ///\n   562:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::into_inner",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "into_inner",
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
            "id": 9785,
            "path": "Cell"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24742",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   515: \n   516:     /// Unwraps the value, consuming the cell.\n   517:     ///\n   518:     /// # Examples\n   519:     ///\n   520:     /// ```\n   521:     /// use std::cell::Cell;\n   522:     ///\n   523:     /// let c = Cell::new(5);\n   524:     /// let five = c.into_inner();\n   525:     ///\n   526:     /// assert_eq!(five, 5);\n   527:     /// ```\n   528:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   529:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   530:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   531:     pub const fn into_inner(self) -> T {\n   532:         self.value.into_inner()\n   533:     }\n   534: }\n   535: \n   536: impl<T: Copy> Cell<T> {\n   537:     /// Returns a copy of the contained value.\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```\n   542:     /// use std::cell::Cell;\n   543:     ///\n   544:     /// let c = Cell::new(5);\n   545:     ///\n   546:     /// let five = c.get();\n   547:     /// ```",
    "nanvix_source": "   521:     /// use std::cell::Cell;\n   522:     ///\n   523:     /// let c = Cell::new(5);\n   524:     /// let five = c.into_inner();\n   525:     ///\n   526:     /// assert_eq!(five, 5);\n   527:     /// ```\n   528:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   529:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   530:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   531:     pub const fn into_inner(self) -> T {\n   532:         self.value.into_inner()\n   533:     }\n   534: }\n   535: \n   536: impl<T: Copy> Cell<T> {\n   537:     /// Returns a copy of the contained value.\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::new",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
            "id": 9785,
            "path": "Cell"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24742",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "value",
            {
              "generic": "T"
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
            "id": 9785,
            "path": "Cell"
          }
        }
      }
    },
    "verification_source": "   398:     }\n   399: }\n   400: \n   401: impl<T> Cell<T> {\n   402:     /// Creates a new `Cell` containing the given value.\n   403:     ///\n   404:     /// # Examples\n   405:     ///\n   406:     /// ```\n   407:     /// use std::cell::Cell;\n   408:     ///\n   409:     /// let c = Cell::new(5);\n   410:     /// ```\n   411:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   412:     #[rustc_const_stable(feature = \"const_cell_new\", since = \"1.24.0\")]\n   413:     #[inline]\n   414:     pub const fn new(value: T) -> Cell<T> {\n   415:         Cell { value: UnsafeCell::new(value) }\n   416:     }\n   417: \n   418:     /// Sets the contained value.\n   419:     ///\n   420:     /// # Examples\n   421:     ///\n   422:     /// ```\n   423:     /// use std::cell::Cell;\n   424:     ///\n   425:     /// let c = Cell::new(5);\n   426:     ///\n   427:     /// c.set(10);\n   428:     /// ```\n   429:     #[inline]\n   430:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   404:     /// # Examples\n   405:     ///\n   406:     /// ```\n   407:     /// use std::cell::Cell;\n   408:     ///\n   409:     /// let c = Cell::new(5);\n   410:     /// ```\n   411:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   412:     #[rustc_const_stable(feature = \"const_cell_new\", since = \"1.24.0\")]\n   413:     #[inline]\n   414:     pub const fn new(value: T) -> Cell<T> {\n   415:         Cell { value: UnsafeCell::new(value) }\n   416:     }\n   417: \n   418:     /// Sets the contained value.\n   419:     ///\n   420:     /// # Examples\n   421:     ///\n   422:     /// ```\n   423:     /// use std::cell::Cell;\n   424:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::replace",
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
        "is_const": true,
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9785,
            "path": "Cell"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24742",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          ],
          [
            "val",
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
    "verification_source": "   494:     ///\n   495:     /// # Examples\n   496:     ///\n   497:     /// ```\n   498:     /// use std::cell::Cell;\n   499:     ///\n   500:     /// let cell = Cell::new(5);\n   501:     /// assert_eq!(cell.get(), 5);\n   502:     /// assert_eq!(cell.replace(10), 5);\n   503:     /// assert_eq!(cell.get(), 10);\n   504:     /// ```\n   505:     #[inline]\n   506:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   507:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   508:     #[rustc_confusables(\"swap\")]\n   509:     #[rustc_should_not_be_called_on_const_items]\n   510:     pub const fn replace(&self, val: T) -> T {\n   511:         // SAFETY: This can cause data races if called from a separate thread,\n   512:         // but `Cell` is `!Sync` so this won't happen.\n   513:         mem::replace(unsafe { &mut *self.value.get() }, val)\n   514:     }\n   515: \n   516:     /// Unwraps the value, consuming the cell.\n   517:     ///\n   518:     /// # Examples\n   519:     ///\n   520:     /// ```\n   521:     /// use std::cell::Cell;\n   522:     ///\n   523:     /// let c = Cell::new(5);\n   524:     /// let five = c.into_inner();\n   525:     ///\n   526:     /// assert_eq!(five, 5);",
    "nanvix_source": "   500:     /// let cell = Cell::new(5);\n   501:     /// assert_eq!(cell.get(), 5);\n   502:     /// assert_eq!(cell.replace(10), 5);\n   503:     /// assert_eq!(cell.get(), 10);\n   504:     /// ```\n   505:     #[inline]\n   506:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   507:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   508:     #[rustc_confusables(\"swap\")]\n   509:     #[rustc_should_not_be_called_on_const_items]\n   510:     pub const fn replace(&self, val: T) -> T {\n   511:         // SAFETY: This can cause data races if called from a separate thread,\n   512:         // but `Cell` is `!Sync` so this won't happen.\n   513:         mem::replace(unsafe { &mut *self.value.get() }, val)\n   514:     }\n   515: \n   516:     /// Unwraps the value, consuming the cell.\n   517:     ///\n   518:     /// # Examples\n   519:     ///\n   520:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::take",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 70,
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
        "is_const": true,
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9785,
            "path": "Cell"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 70,
                          "path": "Default"
                        }
                      }
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
        "impl_id": "core:24752",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   655: impl<T: Default> Cell<T> {\n   656:     /// Takes the value of the cell, leaving `Default::default()` in its place.\n   657:     ///\n   658:     /// # Examples\n   659:     ///\n   660:     /// ```\n   661:     /// use std::cell::Cell;\n   662:     ///\n   663:     /// let c = Cell::new(5);\n   664:     /// let five = c.take();\n   665:     ///\n   666:     /// assert_eq!(five, 5);\n   667:     /// assert_eq!(c.into_inner(), 0);\n   668:     /// ```\n   669:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   670:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   671:     pub const fn take(&self) -> T\n   672:     where\n   673:         T: [const] Default,\n   674:     {\n   675:         self.replace(Default::default())\n   676:     }\n   677: }\n   678: \n   679: #[unstable(feature = \"coerce_unsized\", issue = \"18598\")]\n   680: impl<T: CoerceUnsized<U>, U> CoerceUnsized<Cell<U>> for Cell<T> {}\n   681: \n   682: // Allow types that wrap `Cell` to also implement `DispatchFromDyn`\n   683: // and become dyn-compatible method receivers.\n   684: // Note that currently `Cell` itself cannot be a method receiver\n   685: // because it does not implement Deref.\n   686: // In other words:\n   687: // `self: Cell<&Self>` won't work",
    "nanvix_source": "   661:     /// use std::cell::Cell;\n   662:     ///\n   663:     /// let c = Cell::new(5);\n   664:     /// let five = c.take();\n   665:     ///\n   666:     /// assert_eq!(five, 5);\n   667:     /// assert_eq!(c.into_inner(), 0);\n   668:     /// ```\n   669:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   670:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   671:     pub const fn take(&self) -> T\n   672:     where\n   673:         T: [const] Default,\n   674:     {\n   675:         self.replace(Default::default())\n   676:     }\n   677: }\n   678: \n   679: #[unstable(feature = \"coerce_unsized\", issue = \"18598\")]\n   680: impl<T: CoerceUnsized<U>, U> CoerceUnsized<Cell<U>> for Cell<T> {}\n   681: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::LazyCell::get",
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
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11932,
            "path": "LazyCell"
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
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24691",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11932",
        "resolved_owner_path": [
          "core",
          "cell",
          "lazy",
          "LazyCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
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
                              "generic": "F"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 11932,
                    "path": "LazyCell"
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
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
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   285:     /// Returns a reference to the value if initialized. Otherwise (if uninitialized or poisoned),\n   286:     /// returns `None`.\n   287:     ///\n   288:     /// # Examples\n   289:     ///\n   290:     /// ```\n   291:     /// use std::cell::LazyCell;\n   292:     ///\n   293:     /// let lazy = LazyCell::new(|| 92);\n   294:     ///\n   295:     /// assert_eq!(LazyCell::get(&lazy), None);\n   296:     /// let _ = LazyCell::force(&lazy);\n   297:     /// assert_eq!(LazyCell::get(&lazy), Some(&92));\n   298:     /// ```\n   299:     #[inline]\n   300:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   301:     pub fn get(this: &LazyCell<T, F>) -> Option<&T> {\n   302:         // SAFETY:\n   303:         // This is sound for the same reason as in `force`: once the state is\n   304:         // initialized, it will not be mutably accessed again, so this reference\n   305:         // will stay valid for the duration of the borrow to `self`.\n   306:         let state = unsafe { &*this.state.get() };\n   307:         match state {\n   308:             State::Init(data) => Some(data),\n   309:             _ => None,\n   310:         }\n   311:     }\n   312: }\n   313: \n   314: #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   315: impl<T, F: FnOnce() -> T> Deref for LazyCell<T, F> {\n   316:     type Target = T;\n   317: ",
    "nanvix_source": "   291:     /// use std::cell::LazyCell;\n   292:     ///\n   293:     /// let lazy = LazyCell::new(|| 92);\n   294:     ///\n   295:     /// assert_eq!(LazyCell::get(&lazy), None);\n   296:     /// let _ = LazyCell::force(&lazy);\n   297:     /// assert_eq!(LazyCell::get(&lazy), Some(&92));\n   298:     /// ```\n   299:     #[inline]\n   300:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   301:     pub fn get(this: &LazyCell<T, F>) -> Option<&T> {\n   302:         // SAFETY:\n   303:         // This is sound for the same reason as in `force`: once the state is\n   304:         // initialized, it will not be mutably accessed again, so this reference\n   305:         // will stay valid for the duration of the borrow to `self`.\n   306:         let state = unsafe { &*this.state.get() };\n   307:         match state {\n   308:             State::Init(data) => Some(data),\n   309:             _ => None,\n   310:         }\n   311:     }",
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
