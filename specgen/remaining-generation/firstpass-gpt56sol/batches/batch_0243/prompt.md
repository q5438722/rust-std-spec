For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::RwLock::get_mut",
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
            "id": 8855,
            "path": "LockResult"
          }
        }
      }
    },
    "verification_source": "   662:     /// This function will return an error containing a mutable reference to\n   663:     /// the underlying data if the `RwLock` is poisoned. An `RwLock` is\n   664:     /// poisoned whenever a writer panics while holding an exclusive lock.\n   665:     /// An error will only be returned if the lock would have otherwise been\n   666:     /// acquired.\n   667:     ///\n   668:     /// # Examples\n   669:     ///\n   670:     /// ```\n   671:     /// use std::sync::RwLock;\n   672:     ///\n   673:     /// let mut lock = RwLock::new(0);\n   674:     /// *lock.get_mut().unwrap() = 10;\n   675:     /// assert_eq!(*lock.read().unwrap(), 10);\n   676:     /// ```\n   677:     #[stable(feature = \"rwlock_get_mut\", since = \"1.6.0\")]\n   678:     pub fn get_mut(&mut self) -> LockResult<&mut T> {\n   679:         let data = self.data.get_mut();\n   680:         poison::map_result(self.poison.borrow(), |()| data)\n   681:     }\n   682: \n   683:     /// Returns a raw pointer to the underlying data.\n   684:     ///\n   685:     /// The returned pointer is always non-null and properly aligned, but it is\n   686:     /// the user's responsibility to ensure that any reads and writes through it\n   687:     /// are properly synchronized to avoid data races, and that it is not read\n   688:     /// or written through after the lock is dropped.\n   689:     #[unstable(feature = \"rwlock_data_ptr\", issue = \"140368\")]\n   690:     pub const fn data_ptr(&self) -> *mut T {\n   691:         self.data.get()\n   692:     }\n   693: }\n   694: ",
    "nanvix_source": "   668:     /// # Examples\n   669:     ///\n   670:     /// ```\n   671:     /// use std::sync::RwLock;\n   672:     ///\n   673:     /// let mut lock = RwLock::new(0);\n   674:     /// *lock.get_mut().unwrap() = 10;\n   675:     /// assert_eq!(*lock.read().unwrap(), 10);\n   676:     /// ```\n   677:     #[stable(feature = \"rwlock_get_mut\", since = \"1.6.0\")]\n   678:     pub fn get_mut(&mut self) -> LockResult<&mut T> {\n   679:         let data = self.data.get_mut();\n   680:         poison::map_result(self.poison.borrow(), |()| data)\n   681:     }\n   682: \n   683:     /// Returns a raw pointer to the underlying data.\n   684:     ///\n   685:     /// The returned pointer is always non-null and properly aligned, but it is\n   686:     /// the user's responsibility to ensure that any reads and writes through it\n   687:     /// are properly synchronized to avoid data races, and that it is not read\n   688:     /// or written through after the lock is dropped.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::into_inner",
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
                      "id": 8,
                      "path": "Sized"
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
                    "type": {
                      "generic": "T"
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
    "verification_source": "   629:     /// panics while holding an exclusive lock. An error will only be returned\n   630:     /// if the lock would have otherwise been acquired.\n   631:     ///\n   632:     /// # Examples\n   633:     ///\n   634:     /// ```\n   635:     /// use std::sync::RwLock;\n   636:     ///\n   637:     /// let lock = RwLock::new(String::new());\n   638:     /// {\n   639:     ///     let mut s = lock.write().unwrap();\n   640:     ///     *s = \"modified\".to_owned();\n   641:     /// }\n   642:     /// assert_eq!(lock.into_inner().unwrap(), \"modified\");\n   643:     /// ```\n   644:     #[stable(feature = \"rwlock_into_inner\", since = \"1.6.0\")]\n   645:     pub fn into_inner(self) -> LockResult<T>\n   646:     where\n   647:         T: Sized,\n   648:     {\n   649:         let data = self.data.into_inner();\n   650:         poison::map_result(self.poison.borrow(), |()| data)\n   651:     }\n   652: \n   653:     /// Returns a mutable reference to the underlying data.\n   654:     ///\n   655:     /// Since this call borrows the `RwLock` mutably, no actual locking needs to\n   656:     /// take place -- the mutable borrow statically guarantees no new locks can be acquired\n   657:     /// while this reference exists. Note that this method does not clear any previously abandoned\n   658:     /// locks (e.g., via [`forget()`] on a [`RwLockReadGuard`] or [`RwLockWriteGuard`]).\n   659:     ///\n   660:     /// # Errors\n   661:     ///",
    "nanvix_source": "   635:     /// use std::sync::RwLock;\n   636:     ///\n   637:     /// let lock = RwLock::new(String::new());\n   638:     /// {\n   639:     ///     let mut s = lock.write().unwrap();\n   640:     ///     *s = \"modified\".to_owned();\n   641:     /// }\n   642:     /// assert_eq!(lock.into_inner().unwrap(), \"modified\");\n   643:     /// ```\n   644:     #[stable(feature = \"rwlock_into_inner\", since = \"1.6.0\")]\n   645:     pub fn into_inner(self) -> LockResult<T>\n   646:     where\n   647:         T: Sized,\n   648:     {\n   649:         let data = self.data.into_inner();\n   650:         poison::map_result(self.poison.borrow(), |()| data)\n   651:     }\n   652: \n   653:     /// Returns a mutable reference to the underlying data.\n   654:     ///\n   655:     /// Since this call borrows the `RwLock` mutably, no actual locking needs to",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::is_poisoned",
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
      "name": "is_poisoned",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   566:     ///\n   567:     /// ```\n   568:     /// use std::sync::{Arc, RwLock};\n   569:     /// use std::thread;\n   570:     ///\n   571:     /// let lock = Arc::new(RwLock::new(0));\n   572:     /// let c_lock = Arc::clone(&lock);\n   573:     ///\n   574:     /// let _ = thread::spawn(move || {\n   575:     ///     let _lock = c_lock.write().unwrap();\n   576:     ///     panic!(); // the lock gets poisoned\n   577:     /// }).join();\n   578:     /// assert_eq!(lock.is_poisoned(), true);\n   579:     /// ```\n   580:     #[inline]\n   581:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   582:     pub fn is_poisoned(&self) -> bool {\n   583:         self.poison.get()\n   584:     }\n   585: \n   586:     /// Clear the poisoned state from a lock.\n   587:     ///\n   588:     /// If the lock is poisoned, it will remain poisoned until this function is called. This allows\n   589:     /// recovering from a poisoned state and marking that it has recovered. For example, if the\n   590:     /// value is overwritten by a known-good value, then the lock can be marked as un-poisoned. Or\n   591:     /// possibly, the value could be inspected to determine if it is in a consistent state, and if\n   592:     /// so the poison is removed.\n   593:     ///\n   594:     /// # Examples\n   595:     ///\n   596:     /// ```\n   597:     /// use std::sync::{Arc, RwLock};\n   598:     /// use std::thread;",
    "nanvix_source": "   572:     /// let c_lock = Arc::clone(&lock);\n   573:     ///\n   574:     /// let _ = thread::spawn(move || {\n   575:     ///     let _lock = c_lock.write().unwrap();\n   576:     ///     panic!(); // the lock gets poisoned\n   577:     /// }).join();\n   578:     /// assert_eq!(lock.is_poisoned(), true);\n   579:     /// ```\n   580:     #[inline]\n   581:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   582:     pub fn is_poisoned(&self) -> bool {\n   583:         self.poison.get()\n   584:     }\n   585: \n   586:     /// Clear the poisoned state from a lock.\n   587:     ///\n   588:     /// If the lock is poisoned, it will remain poisoned until this function is called. This allows\n   589:     /// recovering from a poisoned state and marking that it has recovered. For example, if the\n   590:     /// value is overwritten by a known-good value, then the lock can be marked as un-poisoned. Or\n   591:     /// possibly, the value could be inspected to determine if it is in a consistent state, and if\n   592:     /// so the poison is removed.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::new",
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
        "impl_id": "std:8998",
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
            "t",
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
            "id": 8652,
            "path": "RwLock"
          }
        }
      }
    },
    "verification_source": "   242: // Implementations\n   243: ////////////////////////////////////////////////////////////////////////////////////////////////////\n   244: \n   245: impl<T> RwLock<T> {\n   246:     /// Creates a new instance of an `RwLock<T>` which is unlocked.\n   247:     ///\n   248:     /// # Examples\n   249:     ///\n   250:     /// ```\n   251:     /// use std::sync::RwLock;\n   252:     ///\n   253:     /// let lock = RwLock::new(5);\n   254:     /// ```\n   255:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   256:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n   257:     #[inline]\n   258:     pub const fn new(t: T) -> RwLock<T> {\n   259:         RwLock { inner: sys::RwLock::new(), poison: poison::Flag::new(), data: UnsafeCell::new(t) }\n   260:     }\n   261: \n   262:     /// Returns the contained value by cloning it.\n   263:     ///\n   264:     /// # Errors\n   265:     ///\n   266:     /// This function will return an error if the `RwLock` is poisoned. An\n   267:     /// `RwLock` is poisoned whenever a writer panics while holding an exclusive\n   268:     /// lock.\n   269:     ///\n   270:     /// # Examples\n   271:     ///\n   272:     /// ```\n   273:     /// #![feature(lock_value_accessors)]\n   274:     ///",
    "nanvix_source": "   248:     /// # Examples\n   249:     ///\n   250:     /// ```\n   251:     /// use std::sync::RwLock;\n   252:     ///\n   253:     /// let lock = RwLock::new(5);\n   254:     /// ```\n   255:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   256:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n   257:     #[inline]\n   258:     pub const fn new(t: T) -> RwLock<T> {\n   259:         RwLock { inner: sys::RwLock::new(), poison: poison::Flag::new(), data: UnsafeCell::new(t) }\n   260:     }\n   261: \n   262:     /// Returns the contained value by cloning it.\n   263:     ///\n   264:     /// # Errors\n   265:     ///\n   266:     /// This function will return an error if the `RwLock` is poisoned. An\n   267:     /// `RwLock` is poisoned whenever a writer panics while holding an exclusive\n   268:     /// lock.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::read",
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
      "name": "read",
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
                        "id": 9000,
                        "path": "RwLockReadGuard"
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
    "verification_source": "   392:     /// use std::thread;\n   393:     ///\n   394:     /// let lock = Arc::new(RwLock::new(1));\n   395:     /// let c_lock = Arc::clone(&lock);\n   396:     ///\n   397:     /// let n = lock.read().unwrap();\n   398:     /// assert_eq!(*n, 1);\n   399:     ///\n   400:     /// thread::spawn(move || {\n   401:     ///     let r = c_lock.read();\n   402:     ///     assert!(r.is_ok());\n   403:     /// }).join().unwrap();\n   404:     /// ```\n   405:     #[inline]\n   406:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   407:     #[rustc_should_not_be_called_on_const_items]\n   408:     pub fn read(&self) -> LockResult<RwLockReadGuard<'_, T>> {\n   409:         unsafe {\n   410:             self.inner.read();\n   411:             RwLockReadGuard::new(self)\n   412:         }\n   413:     }\n   414: \n   415:     /// Attempts to acquire this `RwLock` with shared read access.\n   416:     ///\n   417:     /// If the access could not be granted at this time, then `Err` is returned.\n   418:     /// Otherwise, an RAII guard is returned which will release the shared access\n   419:     /// when it is dropped.\n   420:     ///\n   421:     /// This function does not block.\n   422:     ///\n   423:     /// This function does not provide any guarantees with respect to the ordering\n   424:     /// of whether contentious readers or writers will acquire the lock first.",
    "nanvix_source": "   398:     /// assert_eq!(*n, 1);\n   399:     ///\n   400:     /// thread::spawn(move || {\n   401:     ///     let r = c_lock.read();\n   402:     ///     assert!(r.is_ok());\n   403:     /// }).join().unwrap();\n   404:     /// ```\n   405:     #[inline]\n   406:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   407:     #[rustc_should_not_be_called_on_const_items]\n   408:     pub fn read(&self) -> LockResult<RwLockReadGuard<'_, T>> {\n   409:         unsafe {\n   410:             self.inner.read();\n   411:             RwLockReadGuard::new(self)\n   412:         }\n   413:     }\n   414: \n   415:     /// Attempts to acquire this `RwLock` with shared read access.\n   416:     ///\n   417:     /// If the access could not be granted at this time, then `Err` is returned.\n   418:     /// Otherwise, an RAII guard is returned which will release the shared access",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::try_read",
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
      "name": "try_read",
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
                        "id": 9000,
                        "path": "RwLockReadGuard"
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
    "verification_source": "   439:     ///\n   440:     /// # Examples\n   441:     ///\n   442:     /// ```\n   443:     /// use std::sync::RwLock;\n   444:     ///\n   445:     /// let lock = RwLock::new(1);\n   446:     ///\n   447:     /// match lock.try_read() {\n   448:     ///     Ok(n) => assert_eq!(*n, 1),\n   449:     ///     Err(_) => unreachable!(),\n   450:     /// };\n   451:     /// ```\n   452:     #[inline]\n   453:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   454:     #[rustc_should_not_be_called_on_const_items]\n   455:     pub fn try_read(&self) -> TryLockResult<RwLockReadGuard<'_, T>> {\n   456:         unsafe {\n   457:             if self.inner.try_read() {\n   458:                 Ok(RwLockReadGuard::new(self)?)\n   459:             } else {\n   460:                 Err(TryLockError::WouldBlock)\n   461:             }\n   462:         }\n   463:     }\n   464: \n   465:     /// Locks this `RwLock` with exclusive write access, blocking the current\n   466:     /// thread until it can be acquired.\n   467:     ///\n   468:     /// This function will not return while other writers or other readers\n   469:     /// currently have access to the lock.\n   470:     ///\n   471:     /// Returns an RAII guard which will drop the write access of this `RwLock`",
    "nanvix_source": "   445:     /// let lock = RwLock::new(1);\n   446:     ///\n   447:     /// match lock.try_read() {\n   448:     ///     Ok(n) => assert_eq!(*n, 1),\n   449:     ///     Err(_) => unreachable!(),\n   450:     /// };\n   451:     /// ```\n   452:     #[inline]\n   453:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   454:     #[rustc_should_not_be_called_on_const_items]\n   455:     pub fn try_read(&self) -> TryLockResult<RwLockReadGuard<'_, T>> {\n   456:         unsafe {\n   457:             if self.inner.try_read() {\n   458:                 Ok(RwLockReadGuard::new(self)?)\n   459:             } else {\n   460:                 Err(TryLockError::WouldBlock)\n   461:             }\n   462:         }\n   463:     }\n   464: \n   465:     /// Locks this `RwLock` with exclusive write access, blocking the current",
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
