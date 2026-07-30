For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::LazyLock::get",
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
      "concurrency_or_hidden_state",
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
            "id": 831,
            "path": "LazyLock"
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
        "impl_id": "std:8374",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:831",
        "resolved_owner_path": [
          "std",
          "sync",
          "lazy_lock",
          "LazyLock"
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
                    "id": 831,
                    "path": "LazyLock"
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
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   295:     /// returns `None`.\n   296:     ///\n   297:     /// # Examples\n   298:     ///\n   299:     /// ```\n   300:     /// use std::sync::LazyLock;\n   301:     ///\n   302:     /// let lazy = LazyLock::new(|| 92);\n   303:     ///\n   304:     /// assert_eq!(LazyLock::get(&lazy), None);\n   305:     /// let _ = LazyLock::force(&lazy);\n   306:     /// assert_eq!(LazyLock::get(&lazy), Some(&92));\n   307:     /// ```\n   308:     #[inline]\n   309:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   310:     #[rustc_should_not_be_called_on_const_items]\n   311:     pub fn get(this: &LazyLock<T, F>) -> Option<&T> {\n   312:         if this.once.is_completed() {\n   313:             // SAFETY:\n   314:             // The closure has been run successfully, so `value` has been initialized\n   315:             // and will not be modified again.\n   316:             Some(unsafe { &(*this.data.get()).value })\n   317:         } else {\n   318:             None\n   319:         }\n   320:     }\n   321: }\n   322: \n   323: #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   324: impl<T, F> Drop for LazyLock<T, F> {\n   325:     fn drop(&mut self) {\n   326:         match self.once.state() {\n   327:             OnceExclusiveState::Incomplete => unsafe {",
    "nanvix_source": "   301:     ///\n   302:     /// let lazy = LazyLock::new(|| 92);\n   303:     ///\n   304:     /// assert_eq!(LazyLock::get(&lazy), None);\n   305:     /// let _ = LazyLock::force(&lazy);\n   306:     /// assert_eq!(LazyLock::get(&lazy), Some(&92));\n   307:     /// ```\n   308:     #[inline]\n   309:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   310:     #[rustc_should_not_be_called_on_const_items]\n   311:     pub fn get(this: &LazyLock<T, F>) -> Option<&T> {\n   312:         if this.once.is_completed() {\n   313:             // SAFETY:\n   314:             // The closure has been run successfully, so `value` has been initialized\n   315:             // and will not be modified again.\n   316:             Some(unsafe { &(*this.data.get()).value })\n   317:         } else {\n   318:             None\n   319:         }\n   320:     }\n   321: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LazyLock::get_mut",
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
      "concurrency_or_hidden_state",
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 831,
            "path": "LazyLock"
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
        "impl_id": "std:8374",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:831",
        "resolved_owner_path": [
          "std",
          "sync",
          "lazy_lock",
          "LazyLock"
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
                    "id": 831,
                    "path": "LazyLock"
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
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   267:     /// poisoned), returns `None`.\n   268:     ///\n   269:     /// # Examples\n   270:     ///\n   271:     /// ```\n   272:     /// use std::sync::LazyLock;\n   273:     ///\n   274:     /// let mut lazy = LazyLock::new(|| 92);\n   275:     ///\n   276:     /// assert_eq!(LazyLock::get_mut(&mut lazy), None);\n   277:     /// let _ = LazyLock::force(&lazy);\n   278:     /// *LazyLock::get_mut(&mut lazy).unwrap() = 44;\n   279:     /// assert_eq!(*lazy, 44);\n   280:     /// ```\n   281:     #[inline]\n   282:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   283:     pub fn get_mut(this: &mut LazyLock<T, F>) -> Option<&mut T> {\n   284:         // `state()` does not perform an atomic load, so prefer it over `is_complete()`.\n   285:         let state = this.once.state();\n   286:         match state {\n   287:             // SAFETY:\n   288:             // The closure has been run successfully, so `value` has been initialized.\n   289:             OnceExclusiveState::Complete => Some(unsafe { &mut this.data.get_mut().value }),\n   290:             _ => None,\n   291:         }\n   292:     }\n   293: \n   294:     /// Returns a reference to the value if initialized. Otherwise (if uninitialized or poisoned),\n   295:     /// returns `None`.\n   296:     ///\n   297:     /// # Examples\n   298:     ///\n   299:     /// ```",
    "nanvix_source": "   273:     ///\n   274:     /// let mut lazy = LazyLock::new(|| 92);\n   275:     ///\n   276:     /// assert_eq!(LazyLock::get_mut(&mut lazy), None);\n   277:     /// let _ = LazyLock::force(&lazy);\n   278:     /// *LazyLock::get_mut(&mut lazy).unwrap() = 44;\n   279:     /// assert_eq!(*lazy, 44);\n   280:     /// ```\n   281:     #[inline]\n   282:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   283:     pub fn get_mut(this: &mut LazyLock<T, F>) -> Option<&mut T> {\n   284:         // `state()` does not perform an atomic load, so prefer it over `is_complete()`.\n   285:         let state = this.once.state();\n   286:         match state {\n   287:             // SAFETY:\n   288:             // The closure has been run successfully, so `value` has been initialized.\n   289:             OnceExclusiveState::Complete => Some(unsafe { &mut this.data.get_mut().value }),\n   290:             _ => None,\n   291:         }\n   292:     }\n   293: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LazyLock::new",
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
      "concurrency_or_hidden_state"
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
            "id": 831,
            "path": "LazyLock"
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
                          "args": {
                            "parenthesized": {
                              "inputs": [],
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
                  "is_synthetic": false
                }
              },
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:8371",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:831",
        "resolved_owner_path": [
          "std",
          "sync",
          "lazy_lock",
          "LazyLock"
        ],
        "trait": null
      },
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
            "id": 831,
            "path": "LazyLock"
          }
        }
      }
    },
    "verification_source": "    88:     /// Creates a new lazy value with the given initializing function.\n    89:     ///\n    90:     /// # Examples\n    91:     ///\n    92:     /// ```\n    93:     /// use std::sync::LazyLock;\n    94:     ///\n    95:     /// let hello = \"Hello, World!\".to_string();\n    96:     ///\n    97:     /// let lazy = LazyLock::new(|| hello.to_uppercase());\n    98:     ///\n    99:     /// assert_eq!(&*lazy, \"HELLO, WORLD!\");\n   100:     /// ```\n   101:     #[inline]\n   102:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   103:     #[rustc_const_stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   104:     pub const fn new(f: F) -> LazyLock<T, F> {\n   105:         LazyLock { once: Once::new(), data: UnsafeCell::new(Data { f: ManuallyDrop::new(f) }) }\n   106:     }\n   107: \n   108:     /// Consumes this `LazyLock` returning the stored value.\n   109:     ///\n   110:     /// Returns `Ok(value)` if `Lazy` is initialized and `Err(f)` otherwise.\n   111:     ///\n   112:     /// # Panics\n   113:     ///\n   114:     /// Panics if the lock is poisoned.\n   115:     ///\n   116:     /// # Examples\n   117:     ///\n   118:     /// ```\n   119:     /// #![feature(lazy_cell_into_inner)]\n   120:     ///",
    "nanvix_source": "    94:     ///\n    95:     /// let hello = \"Hello, World!\".to_string();\n    96:     ///\n    97:     /// let lazy = LazyLock::new(|| hello.to_uppercase());\n    98:     ///\n    99:     /// assert_eq!(&*lazy, \"HELLO, WORLD!\");\n   100:     /// ```\n   101:     #[inline]\n   102:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   103:     #[rustc_const_stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   104:     pub const fn new(f: F) -> LazyLock<T, F> {\n   105:         LazyLock { once: Once::new(), data: UnsafeCell::new(Data { f: ManuallyDrop::new(f) }) }\n   106:     }\n   107: \n   108:     /// Consumes this `LazyLock` returning the stored value.\n   109:     ///\n   110:     /// Returns `Ok(value)` if `Lazy` is initialized and `Err(f)` otherwise.\n   111:     ///\n   112:     /// # Panics\n   113:     ///\n   114:     /// Panics if the lock is poisoned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::and",
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
      "concurrency_or_hidden_state"
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
    "target": "std::sync::LockResult::and_then",
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
      "concurrency_or_hidden_state"
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
    "target": "std::sync::LockResult::as_deref",
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
      "concurrency_or_hidden_state",
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
