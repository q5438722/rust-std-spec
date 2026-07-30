For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::Barrier::wait",
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
      "name": "wait",
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
            "args": null,
            "id": 8321,
            "path": "Barrier"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8326",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8321",
        "resolved_owner_path": [
          "std",
          "sync",
          "barrier",
          "Barrier"
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
            "args": null,
            "id": 8324,
            "path": "BarrierWaitResult"
          }
        }
      }
    },
    "verification_source": "   107:     ///\n   108:     /// let n = 10;\n   109:     /// let barrier = Barrier::new(n);\n   110:     /// thread::scope(|s| {\n   111:     ///     for _ in 0..n {\n   112:     ///         // The same messages will be printed together.\n   113:     ///         // You will NOT see any interleaving.\n   114:     ///         s.spawn(|| {\n   115:     ///             println!(\"before wait\");\n   116:     ///             barrier.wait();\n   117:     ///             println!(\"after wait\");\n   118:     ///         });\n   119:     ///     }\n   120:     /// });\n   121:     /// ```\n   122:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   123:     pub fn wait(&self) -> BarrierWaitResult {\n   124:         let mut lock = self.lock.lock();\n   125:         let local_gen = lock.generation_id;\n   126:         lock.count += 1;\n   127:         if lock.count < self.num_threads {\n   128:             self.cvar.wait_while(&mut lock, |state| local_gen == state.generation_id);\n   129:             BarrierWaitResult(false)\n   130:         } else {\n   131:             lock.count = 0;\n   132:             lock.generation_id = lock.generation_id.wrapping_add(1);\n   133:             self.cvar.notify_all();\n   134:             BarrierWaitResult(true)\n   135:         }\n   136:     }\n   137: }\n   138: \n   139: #[stable(feature = \"std_debug\", since = \"1.16.0\")]",
    "nanvix_source": "   113:     ///         // You will NOT see any interleaving.\n   114:     ///         s.spawn(|| {\n   115:     ///             println!(\"before wait\");\n   116:     ///             barrier.wait();\n   117:     ///             println!(\"after wait\");\n   118:     ///         });\n   119:     ///     }\n   120:     /// });\n   121:     /// ```\n   122:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   123:     pub fn wait(&self) -> BarrierWaitResult {\n   124:         let mut lock = self.lock.lock();\n   125:         let local_gen = lock.generation_id;\n   126:         lock.count += 1;\n   127:         if lock.count < self.num_threads {\n   128:             self.cvar.wait_while(&mut lock, |state| local_gen == state.generation_id);\n   129:             BarrierWaitResult(false)\n   130:         } else {\n   131:             lock.count = 0;\n   132:             lock.generation_id = lock.generation_id.wrapping_add(1);\n   133:             self.cvar.notify_all();",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::BarrierWaitResult::is_leader",
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
      "name": "is_leader",
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
            "args": null,
            "id": 8324,
            "path": "BarrierWaitResult"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8344",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8324",
        "resolved_owner_path": [
          "std",
          "sync",
          "barrier",
          "BarrierWaitResult"
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
    "verification_source": "   127:         if lock.count < self.num_threads {\n   128:             self.cvar.wait_while(&mut lock, |state| local_gen == state.generation_id);\n   129:             BarrierWaitResult(false)\n   130:         } else {\n   131:             lock.count = 0;\n   132:             lock.generation_id = lock.generation_id.wrapping_add(1);\n   133:             self.cvar.notify_all();\n   134:             BarrierWaitResult(true)\n   135:         }\n   136:     }\n   137: }\n   138: \n   139: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   140: impl fmt::Debug for BarrierWaitResult {\n   141:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   142:         f.debug_struct(\"BarrierWaitResult\").field(\"is_leader\", &self.is_leader()).finish()\n   143:     }\n   144: }\n   145: \n   146: impl BarrierWaitResult {\n   147:     /// Returns `true` if this thread is the \"leader thread\" for the call to\n   148:     /// [`Barrier::wait()`].\n   149:     ///\n   150:     /// Only one thread will have `true` returned from their result, all other\n   151:     /// threads will have `false` returned.\n   152:     ///\n   153:     /// # Examples\n   154:     ///\n   155:     /// ```\n   156:     /// use std::sync::Barrier;\n   157:     ///\n   158:     /// let barrier = Barrier::new(1);\n   159:     /// let barrier_wait_result = barrier.wait();",
    "nanvix_source": "   133:             self.cvar.notify_all();\n   134:             BarrierWaitResult(true)\n   135:         }\n   136:     }\n   137: }\n   138: \n   139: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   140: impl fmt::Debug for BarrierWaitResult {\n   141:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   142:         f.debug_struct(\"BarrierWaitResult\").field(\"is_leader\", &self.is_leader()).finish()\n   143:     }\n   144: }\n   145: \n   146: impl BarrierWaitResult {\n   147:     /// Returns `true` if this thread is the \"leader thread\" for the call to\n   148:     /// [`Barrier::wait()`].\n   149:     ///\n   150:     /// Only one thread will have `true` returned from their result, all other\n   151:     /// threads will have `false` returned.\n   152:     ///\n   153:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::new",
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
            "args": null,
            "id": 507,
            "path": "Condvar"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8860",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:507",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "condvar",
          "Condvar"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 507,
            "path": "Condvar"
          }
        }
      }
    },
    "verification_source": "    48: \n    49: impl Condvar {\n    50:     /// Creates a new condition variable which is ready to be waited on and\n    51:     /// notified.\n    52:     ///\n    53:     /// # Examples\n    54:     ///\n    55:     /// ```\n    56:     /// use std::sync::Condvar;\n    57:     ///\n    58:     /// let condvar = Condvar::new();\n    59:     /// ```\n    60:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    61:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n    62:     #[must_use]\n    63:     #[inline]\n    64:     pub const fn new() -> Condvar {\n    65:         Condvar { inner: sys::Condvar::new() }\n    66:     }\n    67: \n    68:     /// Blocks the current thread until this condition variable receives a\n    69:     /// notification.\n    70:     ///\n    71:     /// This function will atomically unlock the mutex specified (represented by\n    72:     /// `guard`) and block the current thread. This means that any calls\n    73:     /// to [`notify_one`] or [`notify_all`] which happen logically after the\n    74:     /// mutex is unlocked are candidates to wake this thread up. When this\n    75:     /// function call returns, the lock specified will have been re-acquired.\n    76:     ///\n    77:     /// Note that this function is susceptible to spurious wakeups. Condition\n    78:     /// variables normally have a boolean predicate associated with them, and\n    79:     /// the predicate must always be checked each time this function returns to\n    80:     /// protect against spurious wakeups.",
    "nanvix_source": "    54:     ///\n    55:     /// ```\n    56:     /// use std::sync::Condvar;\n    57:     ///\n    58:     /// let condvar = Condvar::new();\n    59:     /// ```\n    60:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    61:     #[rustc_const_stable(feature = \"const_locks\", since = \"1.63.0\")]\n    62:     #[must_use]\n    63:     #[inline]\n    64:     pub const fn new() -> Condvar {\n    65:         Condvar { inner: sys::Condvar::new() }\n    66:     }\n    67: \n    68:     /// Blocks the current thread until this condition variable receives a\n    69:     /// notification.\n    70:     ///\n    71:     /// This function will atomically unlock the mutex specified (represented by\n    72:     /// `guard`) and block the current thread. This means that any calls\n    73:     /// to [`notify_one`] or [`notify_all`] which happen logically after the\n    74:     /// mutex is unlocked are candidates to wake this thread up. When this",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::notify_all",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "notify_all",
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
            "id": 507,
            "path": "Condvar"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8860",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:507",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "condvar",
          "Condvar"
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
        "output": null
      }
    },
    "verification_source": "   463:     /// [`notify_one`]: Self::notify_one\n   464:     ///\n   465:     /// # Examples\n   466:     ///\n   467:     /// ```\n   468:     /// use std::sync::{Arc, Mutex, Condvar};\n   469:     /// use std::thread;\n   470:     ///\n   471:     /// let pair = Arc::new((Mutex::new(false), Condvar::new()));\n   472:     /// let pair2 = Arc::clone(&pair);\n   473:     ///\n   474:     /// thread::spawn(move || {\n   475:     ///     let (lock, cvar) = &*pair2;\n   476:     ///     let mut started = lock.lock().unwrap();\n   477:     ///     *started = true;\n   478:     ///     // We notify the condvar that the value has changed.\n   479:     ///     cvar.notify_all();\n   480:     /// });\n   481:     ///\n   482:     /// // Wait for the thread to start up.\n   483:     /// let (lock, cvar) = &*pair;\n   484:     /// let mut started = lock.lock().unwrap();\n   485:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   486:     /// while !*started {\n   487:     ///     started = cvar.wait(started).unwrap();\n   488:     /// }\n   489:     /// ```\n   490:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   491:     #[rustc_should_not_be_called_on_const_items]\n   492:     pub fn notify_all(&self) {\n   493:         self.inner.notify_all()\n   494:     }\n   495: }",
    "nanvix_source": "   469:     /// use std::thread;\n   470:     ///\n   471:     /// let pair = Arc::new((Mutex::new(false), Condvar::new()));\n   472:     /// let pair2 = Arc::clone(&pair);\n   473:     ///\n   474:     /// thread::spawn(move || {\n   475:     ///     let (lock, cvar) = &*pair2;\n   476:     ///     let mut started = lock.lock().unwrap();\n   477:     ///     *started = true;\n   478:     ///     // We notify the condvar that the value has changed.\n   479:     ///     cvar.notify_all();\n   480:     /// });\n   481:     ///\n   482:     /// // Wait for the thread to start up.\n   483:     /// let (lock, cvar) = &*pair;\n   484:     /// let mut started = lock.lock().unwrap();\n   485:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   486:     /// while !*started {\n   487:     ///     started = cvar.wait(started).unwrap();\n   488:     /// }\n   489:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::notify_one",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "notify_one",
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
            "id": 507,
            "path": "Condvar"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8860",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:507",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "condvar",
          "Condvar"
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
        "output": null
      }
    },
    "verification_source": "   435:     ///     let mut started = lock.lock().unwrap();\n   436:     ///     *started = true;\n   437:     ///     // We notify the condvar that the value has changed.\n   438:     ///     cvar.notify_one();\n   439:     /// });\n   440:     ///\n   441:     /// // Wait for the thread to start up.\n   442:     /// let (lock, cvar) = &*pair;\n   443:     /// let mut started = lock.lock().unwrap();\n   444:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   445:     /// while !*started {\n   446:     ///     started = cvar.wait(started).unwrap();\n   447:     /// }\n   448:     /// ```\n   449:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   450:     #[rustc_should_not_be_called_on_const_items]\n   451:     pub fn notify_one(&self) {\n   452:         self.inner.notify_one()\n   453:     }\n   454: \n   455:     /// Wakes up all blocked threads on this condvar.\n   456:     ///\n   457:     /// This method will ensure that any current waiters on the condition\n   458:     /// variable are awoken. Calls to `notify_all()` are not buffered in any\n   459:     /// way.\n   460:     ///\n   461:     /// To wake up only one thread, see [`notify_one`].\n   462:     ///\n   463:     /// [`notify_one`]: Self::notify_one\n   464:     ///\n   465:     /// # Examples\n   466:     ///\n   467:     /// ```",
    "nanvix_source": "   441:     /// // Wait for the thread to start up.\n   442:     /// let (lock, cvar) = &*pair;\n   443:     /// let mut started = lock.lock().unwrap();\n   444:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   445:     /// while !*started {\n   446:     ///     started = cvar.wait(started).unwrap();\n   447:     /// }\n   448:     /// ```\n   449:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   450:     #[rustc_should_not_be_called_on_const_items]\n   451:     pub fn notify_one(&self) {\n   452:         self.inner.notify_one()\n   453:     }\n   454: \n   455:     /// Wakes up all blocked threads on this condvar.\n   456:     ///\n   457:     /// This method will ensure that any current waiters on the condition\n   458:     /// variable are awoken. Calls to `notify_all()` are not buffered in any\n   459:     /// way.\n   460:     ///\n   461:     /// To wake up only one thread, see [`notify_one`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::wait",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          },
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "wait",
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
            "args": null,
            "id": 507,
            "path": "Condvar"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8860",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:507",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "condvar",
          "Condvar"
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
            "guard",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'a"
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
                                "lifetime": "'a"
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
    "verification_source": "   109:     ///     let mut started = lock.lock().unwrap();\n   110:     ///     *started = true;\n   111:     ///     // We notify the condvar that the value has changed.\n   112:     ///     cvar.notify_one();\n   113:     /// });\n   114:     ///\n   115:     /// // Wait for the thread to start up.\n   116:     /// let (lock, cvar) = &*pair;\n   117:     /// let mut started = lock.lock().unwrap();\n   118:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   119:     /// while !*started {\n   120:     ///     started = cvar.wait(started).unwrap();\n   121:     /// }\n   122:     /// ```\n   123:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124:     #[rustc_should_not_be_called_on_const_items]\n   125:     pub fn wait<'a, T>(&self, guard: MutexGuard<'a, T>) -> LockResult<MutexGuard<'a, T>> {\n   126:         let poisoned = unsafe {\n   127:             let lock = mutex::guard_lock(&guard);\n   128:             self.inner.wait(lock);\n   129:             mutex::guard_poison(&guard).get()\n   130:         };\n   131:         if poisoned { Err(PoisonError::new(guard)) } else { Ok(guard) }\n   132:     }\n   133: \n   134:     /// Blocks the current thread until the provided condition becomes false.\n   135:     ///\n   136:     /// `condition` is checked immediately; if not met (returns `true`), this\n   137:     /// will [`wait`] for the next notification then check again. This repeats\n   138:     /// until `condition` returns `false`, in which case this function returns.\n   139:     ///\n   140:     /// This function will atomically unlock the mutex specified (represented by\n   141:     /// `guard`) and block the current thread. This means that any calls",
    "nanvix_source": "   115:     /// // Wait for the thread to start up.\n   116:     /// let (lock, cvar) = &*pair;\n   117:     /// let mut started = lock.lock().unwrap();\n   118:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   119:     /// while !*started {\n   120:     ///     started = cvar.wait(started).unwrap();\n   121:     /// }\n   122:     /// ```\n   123:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124:     #[rustc_should_not_be_called_on_const_items]\n   125:     pub fn wait<'a, T>(&self, guard: MutexGuard<'a, T>) -> LockResult<MutexGuard<'a, T>> {\n   126:         let poisoned = unsafe {\n   127:             let lock = mutex::guard_lock(&guard);\n   128:             self.inner.wait(lock);\n   129:             mutex::guard_poison(&guard).get()\n   130:         };\n   131:         if poisoned { Err(PoisonError::new(guard)) } else { Ok(guard) }\n   132:     }\n   133: \n   134:     /// Blocks the current thread until the provided condition becomes false.\n   135:     ///",
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
