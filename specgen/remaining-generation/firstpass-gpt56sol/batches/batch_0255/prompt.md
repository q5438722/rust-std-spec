For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::LocalKey::with_borrow",
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
      "name": "with_borrow",
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
                        "id": 367,
                        "path": "crate::cell::RefCell"
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
        "impl_id": "std:385",
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
    "verification_source": "   653:     ///\n   654:     /// Panics if the key currently has its destructor running,\n   655:     /// and it **may** panic if the destructor has previously been run for this thread.\n   656:     ///\n   657:     /// # Examples\n   658:     ///\n   659:     /// ```\n   660:     /// use std::cell::RefCell;\n   661:     ///\n   662:     /// thread_local! {\n   663:     ///     static X: RefCell<Vec<i32>> = RefCell::new(Vec::new());\n   664:     /// }\n   665:     ///\n   666:     /// X.with_borrow(|v| assert!(v.is_empty()));\n   667:     /// ```\n   668:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   669:     pub fn with_borrow<F, R>(&'static self, f: F) -> R\n   670:     where\n   671:         F: FnOnce(&T) -> R,\n   672:     {\n   673:         self.with(|cell| f(&cell.borrow()))\n   674:     }\n   675: \n   676:     /// Acquires a mutable reference to the contained value.\n   677:     ///\n   678:     /// This will lazily initialize the value if this thread has not referenced\n   679:     /// this key yet.\n   680:     ///\n   681:     /// # Panics\n   682:     ///\n   683:     /// Panics if the value is currently borrowed.\n   684:     ///\n   685:     /// Panics if the key currently has its destructor running,",
    "nanvix_source": "   667:     /// ```\n   668:     /// use std::cell::RefCell;\n   669:     ///\n   670:     /// thread_local! {\n   671:     ///     static X: RefCell<Vec<i32>> = RefCell::new(Vec::new());\n   672:     /// }\n   673:     ///\n   674:     /// X.with_borrow(|v| assert!(v.is_empty()));\n   675:     /// ```\n   676:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   677:     pub fn with_borrow<F, R>(&'static self, f: F) -> R\n   678:     where\n   679:         F: FnOnce(&T) -> R,\n   680:     {\n   681:         self.with(|cell| f(&cell.borrow()))\n   682:     }\n   683: \n   684:     /// Acquires a mutable reference to the contained value.\n   685:     ///\n   686:     /// This will lazily initialize the value if this thread has not referenced\n   687:     /// this key yet.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::with_borrow_mut",
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
                                "is_mutable": true,
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
      "name": "with_borrow_mut",
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
                        "id": 367,
                        "path": "crate::cell::RefCell"
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
        "impl_id": "std:385",
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
    "verification_source": "   686:     /// and it **may** panic if the destructor has previously been run for this thread.\n   687:     ///\n   688:     /// # Examples\n   689:     ///\n   690:     /// ```\n   691:     /// use std::cell::RefCell;\n   692:     ///\n   693:     /// thread_local! {\n   694:     ///     static X: RefCell<Vec<i32>> = RefCell::new(Vec::new());\n   695:     /// }\n   696:     ///\n   697:     /// X.with_borrow_mut(|v| v.push(1));\n   698:     ///\n   699:     /// X.with_borrow(|v| assert_eq!(*v, vec![1]));\n   700:     /// ```\n   701:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   702:     pub fn with_borrow_mut<F, R>(&'static self, f: F) -> R\n   703:     where\n   704:         F: FnOnce(&mut T) -> R,\n   705:     {\n   706:         self.with(|cell| f(&mut cell.borrow_mut()))\n   707:     }\n   708: \n   709:     /// Sets or initializes the contained value.\n   710:     ///\n   711:     /// Unlike the other methods, this will *not* run the lazy initializer of\n   712:     /// the thread local. Instead, it will be directly initialized with the\n   713:     /// given value if it wasn't initialized yet.\n   714:     ///\n   715:     /// # Panics\n   716:     ///\n   717:     /// Panics if the value is currently borrowed.\n   718:     ///",
    "nanvix_source": "   700:     ///\n   701:     /// thread_local! {\n   702:     ///     static X: RefCell<Vec<i32>> = RefCell::new(Vec::new());\n   703:     /// }\n   704:     ///\n   705:     /// X.with_borrow_mut(|v| v.push(1));\n   706:     ///\n   707:     /// X.with_borrow(|v| assert_eq!(*v, vec![1]));\n   708:     /// ```\n   709:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   710:     pub fn with_borrow_mut<F, R>(&'static self, f: F) -> R\n   711:     where\n   712:         F: FnOnce(&mut T) -> R,\n   713:     {\n   714:         self.with(|cell| f(&mut cell.borrow_mut()))\n   715:     }\n   716: \n   717:     /// Sets or initializes the contained value.\n   718:     ///\n   719:     /// Unlike the other methods, this will *not* run the lazy initializer of\n   720:     /// the thread local. Instead, it will be directly initialized with the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Result::and",
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
            "name": "U"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "U"
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
      "name": "and",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
            "res",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "generic": "U"
                        }
                      },
                      {
                        "type": {
                          "generic": "E"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 90,
                "path": "Result"
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
                      "generic": "U"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1426:     ///\n  1427:     /// let x: Result<u32, &str> = Err(\"early error\");\n  1428:     /// let y: Result<&str, &str> = Ok(\"foo\");\n  1429:     /// assert_eq!(x.and(y), Err(\"early error\"));\n  1430:     ///\n  1431:     /// let x: Result<u32, &str> = Err(\"not a 2\");\n  1432:     /// let y: Result<&str, &str> = Err(\"late error\");\n  1433:     /// assert_eq!(x.and(y), Err(\"not a 2\"));\n  1434:     ///\n  1435:     /// let x: Result<u32, &str> = Ok(2);\n  1436:     /// let y: Result<&str, &str> = Ok(\"different result type\");\n  1437:     /// assert_eq!(x.and(y), Ok(\"different result type\"));\n  1438:     /// ```\n  1439:     #[inline]\n  1440:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1441:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1442:     pub const fn and<U>(self, res: Result<U, E>) -> Result<U, E>\n  1443:     where\n  1444:         T: [const] Destruct,\n  1445:         E: [const] Destruct,\n  1446:         U: [const] Destruct,\n  1447:     {\n  1448:         match self {\n  1449:             Ok(_) => res,\n  1450:             Err(e) => Err(e),\n  1451:         }\n  1452:     }\n  1453: \n  1454:     /// Calls `op` if the result is [`Ok`], otherwise returns the [`Err`] value of `self`.\n  1455:     ///\n  1456:     ///\n  1457:     /// This function can be used for control flow based on `Result` values.\n  1458:     ///",
    "nanvix_source": "  1430:     /// let y: Result<&str, &str> = Err(\"late error\");\n  1431:     /// assert_eq!(x.and(y), Err(\"not a 2\"));\n  1432:     ///\n  1433:     /// let x: Result<u32, &str> = Ok(2);\n  1434:     /// let y: Result<&str, &str> = Ok(\"different result type\");\n  1435:     /// assert_eq!(x.and(y), Ok(\"different result type\"));\n  1436:     /// ```\n  1437:     #[inline]\n  1438:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1439:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1440:     pub const fn and<U>(self, res: Result<U, E>) -> Result<U, E>\n  1441:     where\n  1442:         T: [const] Destruct,\n  1443:         E: [const] Destruct,\n  1444:         U: [const] Destruct,\n  1445:     {\n  1446:         match self {\n  1447:             Ok(_) => res,\n  1448:             Err(e) => Err(e),\n  1449:         }\n  1450:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Result::and_then",
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
            "name": "U"
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
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "generic": "U"
                                      }
                                    },
                                    {
                                      "type": {
                                        "generic": "E"
                                      }
                                    }
                                  ],
                                  "constraints": []
                                }
                              },
                              "id": 90,
                              "path": "Result"
                            }
                          }
                        }
                      },
                      "id": 24,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "and_then",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
            "op",
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
                      "generic": "U"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1472:     ///\n  1473:     /// ```\n  1474:     /// use std::{io::ErrorKind, path::Path};\n  1475:     ///\n  1476:     /// // Note: on Windows \"/\" maps to \"C:\\\"\n  1477:     /// let root_modified_time = Path::new(\"/\").metadata().and_then(|md| md.modified());\n  1478:     /// assert!(root_modified_time.is_ok());\n  1479:     ///\n  1480:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1481:     /// assert!(should_fail.is_err());\n  1482:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1483:     /// ```\n  1484:     #[inline]\n  1485:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1486:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1487:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1488:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1489:     where\n  1490:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1491:     {\n  1492:         match self {\n  1493:             Ok(t) => op(t),\n  1494:             Err(e) => Err(e),\n  1495:         }\n  1496:     }\n  1497: \n  1498:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.\n  1499:     ///\n  1500:     /// Arguments passed to `or` are eagerly evaluated; if you are passing the\n  1501:     /// result of a function call, it is recommended to use [`or_else`], which is\n  1502:     /// lazily evaluated.\n  1503:     ///\n  1504:     /// [`or_else`]: Result::or_else",
    "nanvix_source": "  1476:     /// assert!(root_modified_time.is_ok());\n  1477:     ///\n  1478:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1479:     /// assert!(should_fail.is_err());\n  1480:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1481:     /// ```\n  1482:     #[inline]\n  1483:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1484:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1485:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1486:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1487:     where\n  1488:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1489:     {\n  1490:         match self {\n  1491:             Ok(t) => op(t),\n  1492:             Err(e) => Err(e),\n  1493:         }\n  1494:     }\n  1495: \n  1496:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Result::as_deref",
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
      "reference_identity_vs_view"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8635,
                      "path": "Deref"
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
      "name": "as_deref",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1030:     /// and returns the new [`Result`].\n  1031:     ///\n  1032:     /// # Examples\n  1033:     ///\n  1034:     /// ```\n  1035:     /// let x: Result<String, u32> = Ok(\"hello\".to_string());\n  1036:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1037:     /// assert_eq!(x.as_deref(), y);\n  1038:     ///\n  1039:     /// let x: Result<String, u32> = Err(42);\n  1040:     /// let y: Result<&str, &u32> = Err(&42);\n  1041:     /// assert_eq!(x.as_deref(), y);\n  1042:     /// ```\n  1043:     #[inline]\n  1044:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1045:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1046:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1047:     where\n  1048:         T: [const] Deref,\n  1049:     {\n  1050:         self.as_ref().map(Deref::deref)\n  1051:     }\n  1052: \n  1053:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1054:     ///\n  1055:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1056:     /// and returns the new [`Result`].\n  1057:     ///\n  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());",
    "nanvix_source": "  1034:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1035:     /// assert_eq!(x.as_deref(), y);\n  1036:     ///\n  1037:     /// let x: Result<String, u32> = Err(42);\n  1038:     /// let y: Result<&str, &u32> = Err(&42);\n  1039:     /// assert_eq!(x.as_deref(), y);\n  1040:     /// ```\n  1041:     #[inline]\n  1042:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1043:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1044:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1045:     where\n  1046:         T: [const] Deref,\n  1047:     {\n  1048:         self.as_ref().map(Deref::deref)\n  1049:     }\n  1050: \n  1051:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1052:     ///\n  1053:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1054:     /// and returns the new [`Result`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Result::as_deref_mut",
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
      "reference_identity_vs_view"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8650,
                      "path": "DerefMut"
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
      "name": "as_deref_mut",
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
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());\n  1063:     /// let y: Result<&mut str, &mut u32> = Ok(&mut s);\n  1064:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1065:     ///\n  1066:     /// let mut i = 42;\n  1067:     /// let mut x: Result<String, u32> = Err(42);\n  1068:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1069:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1070:     /// ```\n  1071:     #[inline]\n  1072:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1073:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1074:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1075:     where\n  1076:         T: [const] DerefMut,\n  1077:     {\n  1078:         self.as_mut().map(DerefMut::deref_mut)\n  1079:     }\n  1080: \n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082:     // Iterator constructors\n  1083:     /////////////////////////////////////////////////////////////////////////\n  1084: \n  1085:     /// Returns an iterator over the possibly contained value.\n  1086:     ///\n  1087:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1088:     ///\n  1089:     /// # Examples\n  1090:     ///",
    "nanvix_source": "  1062:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1063:     ///\n  1064:     /// let mut i = 42;\n  1065:     /// let mut x: Result<String, u32> = Err(42);\n  1066:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1067:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1068:     /// ```\n  1069:     #[inline]\n  1070:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1071:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1072:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1073:     where\n  1074:         T: [const] DerefMut,\n  1075:     {\n  1076:         self.as_mut().map(DerefMut::deref_mut)\n  1077:     }\n  1078: \n  1079:     /////////////////////////////////////////////////////////////////////////\n  1080:     // Iterator constructors\n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082: ",
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
