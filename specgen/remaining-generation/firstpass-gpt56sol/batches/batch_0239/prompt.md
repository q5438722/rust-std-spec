For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::Mutex::is_poisoned",
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
            "id": 508,
            "path": "Mutex"
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
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
    "verification_source": "   556:     ///\n   557:     /// ```\n   558:     /// use std::sync::{Arc, Mutex};\n   559:     /// use std::thread;\n   560:     ///\n   561:     /// let mutex = Arc::new(Mutex::new(0));\n   562:     /// let c_mutex = Arc::clone(&mutex);\n   563:     ///\n   564:     /// let _ = thread::spawn(move || {\n   565:     ///     let _lock = c_mutex.lock().unwrap();\n   566:     ///     panic!(); // the mutex gets poisoned\n   567:     /// }).join();\n   568:     /// assert_eq!(mutex.is_poisoned(), true);\n   569:     /// ```\n   570:     #[inline]\n   571:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   572:     pub fn is_poisoned(&self) -> bool {\n   573:         self.poison.get()\n   574:     }\n   575: \n   576:     /// Clear the poisoned state from a mutex.\n   577:     ///\n   578:     /// If the mutex is poisoned, it will remain poisoned until this function is called. This\n   579:     /// allows recovering from a poisoned state and marking that it has recovered. For example, if\n   580:     /// the value is overwritten by a known-good value, then the mutex can be marked as\n   581:     /// un-poisoned. Or possibly, the value could be inspected to determine if it is in a\n   582:     /// consistent state, and if so the poison is removed.\n   583:     ///\n   584:     /// # Examples\n   585:     ///\n   586:     /// ```\n   587:     /// use std::sync::{Arc, Mutex};\n   588:     /// use std::thread;",
    "nanvix_source": "   562:     /// let c_mutex = Arc::clone(&mutex);\n   563:     ///\n   564:     /// let _ = thread::spawn(move || {\n   565:     ///     let _lock = c_mutex.lock().unwrap();\n   566:     ///     panic!(); // the mutex gets poisoned\n   567:     /// }).join();\n   568:     /// assert_eq!(mutex.is_poisoned(), true);\n   569:     /// ```\n   570:     #[inline]\n   571:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   572:     pub fn is_poisoned(&self) -> bool {\n   573:         self.poison.get()\n   574:     }\n   575: \n   576:     /// Clear the poisoned state from a mutex.\n   577:     ///\n   578:     /// If the mutex is poisoned, it will remain poisoned until this function is called. This\n   579:     /// allows recovering from a poisoned state and marking that it has recovered. For example, if\n   580:     /// the value is overwritten by a known-good value, then the mutex can be marked as\n   581:     /// un-poisoned. Or possibly, the value could be inspected to determine if it is in a\n   582:     /// consistent state, and if so the poison is removed.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::lock",
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
      "name": "lock",
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
            "id": 508,
            "path": "Mutex"
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
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
                        "id": 8488,
                        "path": "MutexGuard"
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
    "verification_source": "   474:     /// # Examples\n   475:     ///\n   476:     /// ```\n   477:     /// use std::sync::{Arc, Mutex};\n   478:     /// use std::thread;\n   479:     ///\n   480:     /// let mutex = Arc::new(Mutex::new(0));\n   481:     /// let c_mutex = Arc::clone(&mutex);\n   482:     ///\n   483:     /// thread::spawn(move || {\n   484:     ///     *c_mutex.lock().unwrap() = 10;\n   485:     /// }).join().expect(\"thread::spawn failed\");\n   486:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   487:     /// ```\n   488:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   489:     #[rustc_should_not_be_called_on_const_items]\n   490:     pub fn lock(&self) -> LockResult<MutexGuard<'_, T>> {\n   491:         unsafe {\n   492:             self.inner.lock();\n   493:             MutexGuard::new(self)\n   494:         }\n   495:     }\n   496: \n   497:     /// Attempts to acquire this lock.\n   498:     ///\n   499:     /// If the lock could not be acquired at this time, then [`Err`] is returned.\n   500:     /// Otherwise, an RAII guard is returned. The lock will be unlocked when the\n   501:     /// guard is dropped.\n   502:     ///\n   503:     /// This function does not block.\n   504:     ///\n   505:     /// # Errors\n   506:     ///",
    "nanvix_source": "   480:     /// let mutex = Arc::new(Mutex::new(0));\n   481:     /// let c_mutex = Arc::clone(&mutex);\n   482:     ///\n   483:     /// thread::spawn(move || {\n   484:     ///     *c_mutex.lock().unwrap() = 10;\n   485:     /// }).join().expect(\"thread::spawn failed\");\n   486:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   487:     /// ```\n   488:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   489:     #[rustc_should_not_be_called_on_const_items]\n   490:     pub fn lock(&self) -> LockResult<MutexGuard<'_, T>> {\n   491:         unsafe {\n   492:             self.inner.lock();\n   493:             MutexGuard::new(self)\n   494:         }\n   495:     }\n   496: \n   497:     /// Attempts to acquire this lock.\n   498:     ///\n   499:     /// If the lock could not be acquired at this time, then [`Err`] is returned.\n   500:     /// Otherwise, an RAII guard is returned. The lock will be unlocked when the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::new",
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
            "id": 508,
            "path": "Mutex"
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
        "impl_id": "std:8891",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
            "id": 508,
            "path": "Mutex"
          }
        }
      }
    },
    "verification_source": "   334: #[unstable(feature = \"mapped_lock_guards\", issue = \"117108\")]\n   335: unsafe impl<T: ?Sized + Sync> Sync for MappedMutexGuard<'_, T> {}\n   336: \n   337: impl<T> Mutex<T> {\n   338:     /// Creates a new mutex in an unlocked state ready for use.\n   339:     ///\n   340:     /// # Examples\n   341:     ///\n   342:     /// ```\n   343:     /// use std::sync::Mutex;\n   344:     ///\n   345:     /// let mutex = Mutex::new(0);\n   346:     /// ```\n   347:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   348:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n   349:     #[inline]\n   350:     pub const fn new(t: T) -> Mutex<T> {\n   351:         Mutex { inner: sys::Mutex::new(), poison: poison::Flag::new(), data: UnsafeCell::new(t) }\n   352:     }\n   353: \n   354:     /// Returns the contained value by cloning it.\n   355:     ///\n   356:     /// # Errors\n   357:     ///\n   358:     /// If another user of this mutex panicked while holding the mutex, then\n   359:     /// this call will return an error instead.\n   360:     ///\n   361:     /// # Examples\n   362:     ///\n   363:     /// ```\n   364:     /// #![feature(lock_value_accessors)]\n   365:     ///\n   366:     /// use std::sync::Mutex;",
    "nanvix_source": "   340:     /// # Examples\n   341:     ///\n   342:     /// ```\n   343:     /// use std::sync::Mutex;\n   344:     ///\n   345:     /// let mutex = Mutex::new(0);\n   346:     /// ```\n   347:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   348:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n   349:     #[inline]\n   350:     pub const fn new(t: T) -> Mutex<T> {\n   351:         Mutex { inner: sys::Mutex::new(), poison: poison::Flag::new(), data: UnsafeCell::new(t) }\n   352:     }\n   353: \n   354:     /// Returns the contained value by cloning it.\n   355:     ///\n   356:     /// # Errors\n   357:     ///\n   358:     /// If another user of this mutex panicked while holding the mutex, then\n   359:     /// this call will return an error instead.\n   360:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::try_lock",
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
      "name": "try_lock",
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
            "id": 508,
            "path": "Mutex"
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
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
                        "id": 8488,
                        "path": "MutexGuard"
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
    "verification_source": "   523:     ///\n   524:     /// let mutex = Arc::new(Mutex::new(0));\n   525:     /// let c_mutex = Arc::clone(&mutex);\n   526:     ///\n   527:     /// thread::spawn(move || {\n   528:     ///     let mut lock = c_mutex.try_lock();\n   529:     ///     if let Ok(ref mut mutex) = lock {\n   530:     ///         **mutex = 10;\n   531:     ///     } else {\n   532:     ///         println!(\"try_lock failed\");\n   533:     ///     }\n   534:     /// }).join().expect(\"thread::spawn failed\");\n   535:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   536:     /// ```\n   537:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   538:     #[rustc_should_not_be_called_on_const_items]\n   539:     pub fn try_lock(&self) -> TryLockResult<MutexGuard<'_, T>> {\n   540:         unsafe {\n   541:             if self.inner.try_lock() {\n   542:                 Ok(MutexGuard::new(self)?)\n   543:             } else {\n   544:                 Err(TryLockError::WouldBlock)\n   545:             }\n   546:         }\n   547:     }\n   548: \n   549:     /// Determines whether the mutex is poisoned.\n   550:     ///\n   551:     /// If another thread is active, the mutex can still become poisoned at any\n   552:     /// time. You should not trust a `false` value for program correctness\n   553:     /// without additional synchronization.\n   554:     ///\n   555:     /// # Examples",
    "nanvix_source": "   529:     ///     if let Ok(ref mut mutex) = lock {\n   530:     ///         **mutex = 10;\n   531:     ///     } else {\n   532:     ///         println!(\"try_lock failed\");\n   533:     ///     }\n   534:     /// }).join().expect(\"thread::spawn failed\");\n   535:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   536:     /// ```\n   537:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   538:     #[rustc_should_not_be_called_on_const_items]\n   539:     pub fn try_lock(&self) -> TryLockResult<MutexGuard<'_, T>> {\n   540:         unsafe {\n   541:             if self.inner.try_lock() {\n   542:                 Ok(MutexGuard::new(self)?)\n   543:             } else {\n   544:                 Err(TryLockError::WouldBlock)\n   545:             }\n   546:         }\n   547:     }\n   548: \n   549:     /// Determines whether the mutex is poisoned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Once::call_once",
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [],
                          "output": null
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
      "name": "call_once",
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
            "args": null,
            "id": 8273,
            "path": "Once"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8280",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8273",
        "resolved_owner_path": [
          "std",
          "sync",
          "once",
          "Once"
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   140:     ///\n   141:     /// # Panics\n   142:     ///\n   143:     /// The closure `f` will only be executed once even if this is called\n   144:     /// concurrently amongst many threads. If that closure panics, however, then\n   145:     /// it will *poison* this [`Once`] instance, causing all future invocations of\n   146:     /// `call_once` to also panic.\n   147:     ///\n   148:     /// This is similar to [poisoning with mutexes][poison], but this mechanism\n   149:     /// is guaranteed to never skip panics within `f`.\n   150:     ///\n   151:     /// [poison]: struct.Mutex.html#poisoning\n   152:     #[inline]\n   153:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   154:     #[track_caller]\n   155:     #[rustc_should_not_be_called_on_const_items]\n   156:     pub fn call_once<F>(&self, f: F)\n   157:     where\n   158:         F: FnOnce(),\n   159:     {\n   160:         // Fast path check\n   161:         if self.inner.is_completed() {\n   162:             return;\n   163:         }\n   164: \n   165:         let mut f = Some(f);\n   166:         self.inner.call(false, &mut |_| f.take().unwrap()());\n   167:     }\n   168: \n   169:     /// Performs the same function as [`call_once()`] except ignores poisoning.\n   170:     ///\n   171:     /// Unlike [`call_once()`], if this [`Once`] has been poisoned (i.e., a previous\n   172:     /// call to [`call_once()`] or [`call_once_force()`] caused a panic), calling",
    "nanvix_source": "   146:     /// `call_once` to also panic.\n   147:     ///\n   148:     /// This is similar to [poisoning with mutexes][poison], but this mechanism\n   149:     /// is guaranteed to never skip panics within `f`.\n   150:     ///\n   151:     /// [poison]: struct.Mutex.html#poisoning\n   152:     #[inline]\n   153:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   154:     #[track_caller]\n   155:     #[rustc_should_not_be_called_on_const_items]\n   156:     pub fn call_once<F>(&self, f: F)\n   157:     where\n   158:         F: FnOnce(),\n   159:     {\n   160:         // Fast path check\n   161:         if self.inner.is_completed() {\n   162:             return;\n   163:         }\n   164: \n   165:         let mut f = Some(f);\n   166:         self.inner.call(false, &mut |_| f.take().unwrap()());",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Once::call_once_force",
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
                                  "resolved_path": {
                                    "args": null,
                                    "id": 8276,
                                    "path": "OnceState"
                                  }
                                }
                              }
                            }
                          ],
                          "output": null
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
      "name": "call_once_force",
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
            "args": null,
            "id": 8273,
            "path": "Once"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8280",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8273",
        "resolved_owner_path": [
          "std",
          "sync",
          "once",
          "Once"
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   200:     /// let handle = thread::spawn(|| {\n   201:     ///     INIT.call_once(|| {});\n   202:     /// });\n   203:     /// assert!(handle.join().is_err());\n   204:     ///\n   205:     /// // call_once_force will still run and reset the poisoned state\n   206:     /// INIT.call_once_force(|state| {\n   207:     ///     assert!(state.is_poisoned());\n   208:     /// });\n   209:     ///\n   210:     /// // once any success happens, we stop propagating the poison\n   211:     /// INIT.call_once(|| {});\n   212:     /// ```\n   213:     #[inline]\n   214:     #[stable(feature = \"once_poison\", since = \"1.51.0\")]\n   215:     #[rustc_should_not_be_called_on_const_items]\n   216:     pub fn call_once_force<F>(&self, f: F)\n   217:     where\n   218:         F: FnOnce(&OnceState),\n   219:     {\n   220:         // Fast path check\n   221:         if self.inner.is_completed() {\n   222:             return;\n   223:         }\n   224: \n   225:         let mut f = Some(f);\n   226:         self.inner.call(true, &mut |p| f.take().unwrap()(p));\n   227:     }\n   228: \n   229:     /// Returns `true` if some [`call_once()`] call has completed\n   230:     /// successfully. Specifically, `is_completed` will return false in\n   231:     /// the following situations:\n   232:     ///   * [`call_once()`] was not called at all,",
    "nanvix_source": "   206:     /// INIT.call_once_force(|state| {\n   207:     ///     assert!(state.is_poisoned());\n   208:     /// });\n   209:     ///\n   210:     /// // once any success happens, we stop propagating the poison\n   211:     /// INIT.call_once(|| {});\n   212:     /// ```\n   213:     #[inline]\n   214:     #[stable(feature = \"once_poison\", since = \"1.51.0\")]\n   215:     #[rustc_should_not_be_called_on_const_items]\n   216:     pub fn call_once_force<F>(&self, f: F)\n   217:     where\n   218:         F: FnOnce(&OnceState),\n   219:     {\n   220:         // Fast path check\n   221:         if self.inner.is_completed() {\n   222:             return;\n   223:         }\n   224: \n   225:         let mut f = Some(f);\n   226:         self.inner.call(true, &mut |p| f.take().unwrap()(p));",
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
