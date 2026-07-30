For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::RwLock::try_write",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_write",
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
            "id": 8652,
            "path": "RwLock"
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
                          "id": 8,
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:9010",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8652",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "rwlock",
          "RwLock"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'_"
                              },
                              {
                                "type": {
                                  "generic": "T"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9003,
                        "path": "RwLockWriteGuard"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 8894,
            "path": "TryLockResult"
          }
        }
      }
    },
    "verification_source": "   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::sync::RwLock;\n   538:     ///\n   539:     /// let lock = RwLock::new(1);\n   540:     ///\n   541:     /// let n = lock.read().unwrap();\n   542:     /// assert_eq!(*n, 1);\n   543:     ///\n   544:     /// assert!(lock.try_write().is_err());\n   545:     /// ```\n   546:     #[inline]\n   547:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   548:     #[rustc_should_not_be_called_on_const_items]\n   549:     pub fn try_write(&self) -> TryLockResult<RwLockWriteGuard<'_, T>> {\n   550:         unsafe {\n   551:             if self.inner.try_write() {\n   552:                 Ok(RwLockWriteGuard::new(self)?)\n   553:             } else {\n   554:                 Err(TryLockError::WouldBlock)\n   555:             }\n   556:         }\n   557:     }\n   558: \n   559:     /// Determines whether the lock is poisoned.\n   560:     ///\n   561:     /// If another thread is active, the lock can still become poisoned at any\n   562:     /// time. You should not trust a `false` value for program correctness\n   563:     /// without additional synchronization.\n   564:     ///\n   565:     /// # Examples",
    "nanvix_source": "   539:     /// let lock = RwLock::new(1);\n   540:     ///\n   541:     /// let n = lock.read().unwrap();\n   542:     /// assert_eq!(*n, 1);\n   543:     ///\n   544:     /// assert!(lock.try_write().is_err());\n   545:     /// ```\n   546:     #[inline]\n   547:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   548:     #[rustc_should_not_be_called_on_const_items]\n   549:     pub fn try_write(&self) -> TryLockResult<RwLockWriteGuard<'_, T>> {\n   550:         unsafe {\n   551:             if self.inner.try_write() {\n   552:                 Ok(RwLockWriteGuard::new(self)?)\n   553:             } else {\n   554:                 Err(TryLockError::WouldBlock)\n   555:             }\n   556:         }\n   557:     }\n   558: \n   559:     /// Determines whether the lock is poisoned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::write",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "write",
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
            "id": 8652,
            "path": "RwLock"
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
                          "id": 8,
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:9010",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8652",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "rwlock",
          "RwLock"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'_"
                              },
                              {
                                "type": {
                                  "generic": "T"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9003,
                        "path": "RwLockWriteGuard"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 8855,
            "path": "LockResult"
          }
        }
      }
    },
    "verification_source": "   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::sync::RwLock;\n   490:     ///\n   491:     /// let lock = RwLock::new(1);\n   492:     ///\n   493:     /// let mut n = lock.write().unwrap();\n   494:     /// *n = 2;\n   495:     ///\n   496:     /// assert!(lock.try_read().is_err());\n   497:     /// ```\n   498:     #[inline]\n   499:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   500:     #[rustc_should_not_be_called_on_const_items]\n   501:     pub fn write(&self) -> LockResult<RwLockWriteGuard<'_, T>> {\n   502:         unsafe {\n   503:             self.inner.write();\n   504:             RwLockWriteGuard::new(self)\n   505:         }\n   506:     }\n   507: \n   508:     /// Attempts to lock this `RwLock` with exclusive write access.\n   509:     ///\n   510:     /// If the lock could not be acquired at this time, then `Err` is returned.\n   511:     /// Otherwise, an RAII guard is returned which will release the lock when\n   512:     /// it is dropped.\n   513:     ///\n   514:     /// This function does not block.\n   515:     ///\n   516:     /// This function does not provide any guarantees with respect to the ordering\n   517:     /// of whether contentious readers or writers will acquire the lock first.",
    "nanvix_source": "   491:     /// let lock = RwLock::new(1);\n   492:     ///\n   493:     /// let mut n = lock.write().unwrap();\n   494:     /// *n = 2;\n   495:     ///\n   496:     /// assert!(lock.try_read().is_err());\n   497:     /// ```\n   498:     #[inline]\n   499:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   500:     #[rustc_should_not_be_called_on_const_items]\n   501:     pub fn write(&self) -> LockResult<RwLockWriteGuard<'_, T>> {\n   502:         unsafe {\n   503:             self.inner.write();\n   504:             RwLockWriteGuard::new(self)\n   505:         }\n   506:     }\n   507: \n   508:     /// Attempts to lock this `RwLock` with exclusive write access.\n   509:     ///\n   510:     /// If the lock could not be acquired at this time, then `Err` is returned.\n   511:     /// Otherwise, an RAII guard is returned which will release the lock when",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLockWriteGuard::downgrade",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "downgrade",
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
                    "lifetime": "'rwlock"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9003,
            "path": "RwLockWriteGuard"
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
              "name": "'rwlock"
            },
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
                          "id": 8,
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:9069",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:9003",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "rwlock",
          "RwLockWriteGuard"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "s",
            {
              "generic": "Self"
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
                    "lifetime": "'rwlock"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9000,
            "path": "RwLockReadGuard"
          }
        }
      }
    },
    "verification_source": "   867:     ///\n   868:     /// *main_write_guard = 2;\n   869:     ///\n   870:     /// // Atomically downgrade the write guard into a read guard.\n   871:     /// let main_read_guard = RwLockWriteGuard::downgrade(main_write_guard);\n   872:     ///\n   873:     /// // Since `downgrade` is atomic, the writer thread cannot have changed the protected data.\n   874:     /// assert_eq!(*main_read_guard, 2, \"`downgrade` was not atomic\");\n   875:     /// #\n   876:     /// # drop(main_read_guard);\n   877:     /// # evil_handle.join().unwrap();\n   878:     /// #\n   879:     /// # let final_check = rw.read().unwrap();\n   880:     /// # assert_eq!(*final_check, 3);\n   881:     /// ```\n   882:     #[stable(feature = \"rwlock_downgrade\", since = \"1.92.0\")]\n   883:     pub fn downgrade(s: Self) -> RwLockReadGuard<'rwlock, T> {\n   884:         let lock = s.lock;\n   885: \n   886:         // We don't want to call the destructor since that calls `write_unlock`.\n   887:         forget(s);\n   888: \n   889:         // SAFETY: We take ownership of a write guard, so we must already have the `RwLock` in write\n   890:         // mode, satisfying the `downgrade` contract.\n   891:         unsafe { lock.inner.downgrade() };\n   892: \n   893:         // SAFETY: We have just successfully called `downgrade`, so we fulfill the safety contract.\n   894:         unsafe { RwLockReadGuard::new(lock).unwrap_or_else(PoisonError::into_inner) }\n   895:     }\n   896: \n   897:     /// Makes a [`MappedRwLockWriteGuard`] for a component of the borrowed data, e.g.\n   898:     /// an enum variant.\n   899:     ///",
    "nanvix_source": "   873:     /// // Since `downgrade` is atomic, the writer thread cannot have changed the protected data.\n   874:     /// assert_eq!(*main_read_guard, 2, \"`downgrade` was not atomic\");\n   875:     /// #\n   876:     /// # drop(main_read_guard);\n   877:     /// # evil_handle.join().unwrap();\n   878:     /// #\n   879:     /// # let final_check = rw.read().unwrap();\n   880:     /// # assert_eq!(*final_check, 3);\n   881:     /// ```\n   882:     #[stable(feature = \"rwlock_downgrade\", since = \"1.92.0\")]\n   883:     pub fn downgrade(s: Self) -> RwLockReadGuard<'rwlock, T> {\n   884:         let lock = s.lock;\n   885: \n   886:         // We don't want to call the destructor since that calls `write_unlock`.\n   887:         forget(s);\n   888: \n   889:         // SAFETY: We take ownership of a write guard, so we must already have the `RwLock` in write\n   890:         // mode, satisfying the `downgrade` contract.\n   891:         unsafe { lock.inner.downgrade() };\n   892: \n   893:         // SAFETY: We have just successfully called `downgrade`, so we fulfill the safety contract.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::TryLockResult::and",
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
    "target": "std::sync::TryLockResult::and_then",
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
    "target": "std::sync::TryLockResult::as_deref",
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
