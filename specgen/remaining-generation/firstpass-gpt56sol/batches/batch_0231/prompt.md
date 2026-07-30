For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::Condvar::wait_timeout",
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
      "name": "wait_timeout",
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
          ],
          [
            "dur",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
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
                      "tuple": [
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
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 8524,
                            "path": "WaitTimeoutResult"
                          }
                        }
                      ]
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
    "verification_source": "   307:     /// // wait for the thread to start up\n   308:     /// let (lock, cvar) = &*pair;\n   309:     /// let mut started = lock.lock().unwrap();\n   310:     /// // as long as the value inside the `Mutex<bool>` is `false`, we wait\n   311:     /// loop {\n   312:     ///     let result = cvar.wait_timeout(started, Duration::from_millis(10)).unwrap();\n   313:     ///     // 10 milliseconds have passed, or maybe the value changed!\n   314:     ///     started = result.0;\n   315:     ///     if *started == true {\n   316:     ///         // We received the notification and the value has been updated, we can leave.\n   317:     ///         break\n   318:     ///     }\n   319:     /// }\n   320:     /// ```\n   321:     #[stable(feature = \"wait_timeout\", since = \"1.5.0\")]\n   322:     #[rustc_should_not_be_called_on_const_items]\n   323:     pub fn wait_timeout<'a, T>(\n   324:         &self,\n   325:         guard: MutexGuard<'a, T>,\n   326:         dur: Duration,\n   327:     ) -> LockResult<(MutexGuard<'a, T>, WaitTimeoutResult)> {\n   328:         let (poisoned, result) = unsafe {\n   329:             let lock = mutex::guard_lock(&guard);\n   330:             let success = self.inner.wait_timeout(lock, dur);\n   331:             (mutex::guard_poison(&guard).get(), WaitTimeoutResult(!success))\n   332:         };\n   333:         if poisoned { Err(PoisonError::new((guard, result))) } else { Ok((guard, result)) }\n   334:     }\n   335: \n   336:     /// Waits on this condition variable for a notification, timing out after a\n   337:     /// specified duration.\n   338:     ///\n   339:     /// The semantics of this function are equivalent to [`wait_while`] except",
    "nanvix_source": "   313:     ///     // 10 milliseconds have passed, or maybe the value changed!\n   314:     ///     started = result.0;\n   315:     ///     if *started == true {\n   316:     ///         // We received the notification and the value has been updated, we can leave.\n   317:     ///         break\n   318:     ///     }\n   319:     /// }\n   320:     /// ```\n   321:     #[stable(feature = \"wait_timeout\", since = \"1.5.0\")]\n   322:     #[rustc_should_not_be_called_on_const_items]\n   323:     pub fn wait_timeout<'a, T>(\n   324:         &self,\n   325:         guard: MutexGuard<'a, T>,\n   326:         dur: Duration,\n   327:     ) -> LockResult<(MutexGuard<'a, T>, WaitTimeoutResult)> {\n   328:         let (poisoned, result) = unsafe {\n   329:             let lock = mutex::guard_lock(&guard);\n   330:             let success = self.inner.wait_timeout(lock, dur);\n   331:             (mutex::guard_poison(&guard).get(), WaitTimeoutResult(!success))\n   332:         };\n   333:         if poisoned { Err(PoisonError::new((guard, result))) } else { Ok((guard, result)) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::wait_timeout_ms",
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
      "name": "wait_timeout_ms",
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
          ],
          [
            "ms",
            {
              "primitive": "u32"
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
                      "tuple": [
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
                        },
                        {
                          "primitive": "bool"
                        }
                      ]
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
    "verification_source": "   236:     /// let (lock, cvar) = &*pair;\n   237:     /// let mut started = lock.lock().unwrap();\n   238:     /// // As long as the value inside the `Mutex<bool>` is `false`, we wait.\n   239:     /// loop {\n   240:     ///     let result = cvar.wait_timeout_ms(started, 10).unwrap();\n   241:     ///     // 10 milliseconds have passed, or maybe the value changed!\n   242:     ///     started = result.0;\n   243:     ///     if *started == true {\n   244:     ///         // We received the notification and the value has been updated, we can leave.\n   245:     ///         break\n   246:     ///     }\n   247:     /// }\n   248:     /// ```\n   249:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   250:     #[rustc_should_not_be_called_on_const_items]\n   251:     #[deprecated(since = \"1.6.0\", note = \"replaced by `std::sync::Condvar::wait_timeout`\")]\n   252:     pub fn wait_timeout_ms<'a, T>(\n   253:         &self,\n   254:         guard: MutexGuard<'a, T>,\n   255:         ms: u32,\n   256:     ) -> LockResult<(MutexGuard<'a, T>, bool)> {\n   257:         let res = self.wait_timeout(guard, Duration::from_millis(ms as u64));\n   258:         poison::map_result(res, |(a, b)| (a, !b.timed_out()))\n   259:     }\n   260: \n   261:     /// Waits on this condition variable for a notification, timing out after a\n   262:     /// specified duration.\n   263:     ///\n   264:     /// The semantics of this function are equivalent to [`wait`] except that\n   265:     /// the thread will be blocked for roughly no longer than `dur`. This\n   266:     /// method should not be used for precise timing due to anomalies such as\n   267:     /// preemption or platform differences that might not cause the maximum\n   268:     /// amount of time waited to be precisely `dur`.",
    "nanvix_source": "   242:     ///     started = result.0;\n   243:     ///     if *started == true {\n   244:     ///         // We received the notification and the value has been updated, we can leave.\n   245:     ///         break\n   246:     ///     }\n   247:     /// }\n   248:     /// ```\n   249:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   250:     #[rustc_should_not_be_called_on_const_items]\n   251:     #[deprecated(since = \"1.6.0\", note = \"replaced by `std::sync::Condvar::wait_timeout`\")]\n   252:     pub fn wait_timeout_ms<'a, T>(\n   253:         &self,\n   254:         guard: MutexGuard<'a, T>,\n   255:         ms: u32,\n   256:     ) -> LockResult<(MutexGuard<'a, T>, bool)> {\n   257:         let res = self.wait_timeout(guard, Duration::from_millis(ms as u64));\n   258:         poison::map_result(res, |(a, b)| (a, !b.timed_out()))\n   259:     }\n   260: \n   261:     /// Waits on this condition variable for a notification, timing out after a\n   262:     /// specified duration.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::wait_timeout_while",
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
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 18,
                      "path": "FnMut"
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
      "name": "wait_timeout_while",
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
          ],
          [
            "dur",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
              }
            }
          ],
          [
            "condition",
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
                      "tuple": [
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
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 8524,
                            "path": "WaitTimeoutResult"
                          }
                        }
                      ]
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
    "verification_source": "   374:     /// });\n   375:     ///\n   376:     /// // wait for the thread to start up\n   377:     /// let (lock, cvar) = &*pair;\n   378:     /// let result = cvar.wait_timeout_while(\n   379:     ///     lock.lock().unwrap(),\n   380:     ///     Duration::from_millis(100),\n   381:     ///     |&mut pending| pending,\n   382:     /// ).unwrap();\n   383:     /// if result.1.timed_out() {\n   384:     ///     // timed-out without the condition ever evaluating to false.\n   385:     /// }\n   386:     /// // access the locked mutex via result.0\n   387:     /// ```\n   388:     #[stable(feature = \"wait_timeout_until\", since = \"1.42.0\")]\n   389:     #[rustc_should_not_be_called_on_const_items]\n   390:     pub fn wait_timeout_while<'a, T, F>(\n   391:         &self,\n   392:         mut guard: MutexGuard<'a, T>,\n   393:         dur: Duration,\n   394:         mut condition: F,\n   395:     ) -> LockResult<(MutexGuard<'a, T>, WaitTimeoutResult)>\n   396:     where\n   397:         F: FnMut(&mut T) -> bool,\n   398:     {\n   399:         let start = Instant::now();\n   400:         loop {\n   401:             if !condition(&mut *guard) {\n   402:                 return Ok((guard, WaitTimeoutResult(false)));\n   403:             }\n   404:             let timeout = match dur.checked_sub(start.elapsed()) {\n   405:                 Some(timeout) => timeout,\n   406:                 None => return Ok((guard, WaitTimeoutResult(true))),",
    "nanvix_source": "   380:     ///     Duration::from_millis(100),\n   381:     ///     |&mut pending| pending,\n   382:     /// ).unwrap();\n   383:     /// if result.1.timed_out() {\n   384:     ///     // timed-out without the condition ever evaluating to false.\n   385:     /// }\n   386:     /// // access the locked mutex via result.0\n   387:     /// ```\n   388:     #[stable(feature = \"wait_timeout_until\", since = \"1.42.0\")]\n   389:     #[rustc_should_not_be_called_on_const_items]\n   390:     pub fn wait_timeout_while<'a, T, F>(\n   391:         &self,\n   392:         mut guard: MutexGuard<'a, T>,\n   393:         dur: Duration,\n   394:         mut condition: F,\n   395:     ) -> LockResult<(MutexGuard<'a, T>, WaitTimeoutResult)>\n   396:     where\n   397:         F: FnMut(&mut T) -> bool,\n   398:     {\n   399:         let start = Instant::now();\n   400:         loop {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Condvar::wait_while",
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
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 18,
                      "path": "FnMut"
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
      "name": "wait_while",
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
          ],
          [
            "condition",
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
    "verification_source": "   166:     ///\n   167:     /// thread::spawn(move || {\n   168:     ///     let (lock, cvar) = &*pair2;\n   169:     ///     let mut pending = lock.lock().unwrap();\n   170:     ///     *pending = false;\n   171:     ///     // We notify the condvar that the value has changed.\n   172:     ///     cvar.notify_one();\n   173:     /// });\n   174:     ///\n   175:     /// // Wait for the thread to start up.\n   176:     /// let (lock, cvar) = &*pair;\n   177:     /// // As long as the value inside the `Mutex<bool>` is `true`, we wait.\n   178:     /// let _guard = cvar.wait_while(lock.lock().unwrap(), |pending| { *pending }).unwrap();\n   179:     /// ```\n   180:     #[stable(feature = \"wait_until\", since = \"1.42.0\")]\n   181:     #[rustc_should_not_be_called_on_const_items]\n   182:     pub fn wait_while<'a, T, F>(\n   183:         &self,\n   184:         mut guard: MutexGuard<'a, T>,\n   185:         mut condition: F,\n   186:     ) -> LockResult<MutexGuard<'a, T>>\n   187:     where\n   188:         F: FnMut(&mut T) -> bool,\n   189:     {\n   190:         while condition(&mut *guard) {\n   191:             guard = self.wait(guard)?;\n   192:         }\n   193:         Ok(guard)\n   194:     }\n   195: \n   196:     /// Waits on this condition variable for a notification, timing out after a\n   197:     /// specified duration.\n   198:     ///",
    "nanvix_source": "   172:     ///     cvar.notify_one();\n   173:     /// });\n   174:     ///\n   175:     /// // Wait for the thread to start up.\n   176:     /// let (lock, cvar) = &*pair;\n   177:     /// // As long as the value inside the `Mutex<bool>` is `true`, we wait.\n   178:     /// let _guard = cvar.wait_while(lock.lock().unwrap(), |pending| { *pending }).unwrap();\n   179:     /// ```\n   180:     #[stable(feature = \"wait_until\", since = \"1.42.0\")]\n   181:     #[rustc_should_not_be_called_on_const_items]\n   182:     pub fn wait_while<'a, T, F>(\n   183:         &self,\n   184:         mut guard: MutexGuard<'a, T>,\n   185:         mut condition: F,\n   186:     ) -> LockResult<MutexGuard<'a, T>>\n   187:     where\n   188:         F: FnMut(&mut T) -> bool,\n   189:     {\n   190:         while condition(&mut *guard) {\n   191:             guard = self.wait(guard)?;\n   192:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LazyLock::force",
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
      "name": "force",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   225:     /// [`new()`]: LazyLock::new\n   226:     /// [`force()`]: LazyLock::force\n   227:     ///\n   228:     /// # Examples\n   229:     ///\n   230:     /// ```\n   231:     /// use std::sync::LazyLock;\n   232:     ///\n   233:     /// let lazy = LazyLock::new(|| 92);\n   234:     ///\n   235:     /// assert_eq!(LazyLock::force(&lazy), &92);\n   236:     /// assert_eq!(&*lazy, &92);\n   237:     /// ```\n   238:     #[inline]\n   239:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   240:     #[rustc_should_not_be_called_on_const_items]\n   241:     pub fn force(this: &LazyLock<T, F>) -> &T {\n   242:         this.once.call_once_force(|state| {\n   243:             if state.is_poisoned() {\n   244:                 panic_poisoned();\n   245:             }\n   246: \n   247:             // SAFETY: `call_once` only runs this closure once, ever.\n   248:             let data = unsafe { &mut *this.data.get() };\n   249:             let f = unsafe { ManuallyDrop::take(&mut data.f) };\n   250:             let value = f();\n   251:             data.value = ManuallyDrop::new(value);\n   252:         });\n   253: \n   254:         // SAFETY:\n   255:         // There are four possible scenarios:\n   256:         // * the closure was called and initialized `value`.\n   257:         // * the closure was called and panicked, so this point is never reached.",
    "nanvix_source": "   231:     /// use std::sync::LazyLock;\n   232:     ///\n   233:     /// let lazy = LazyLock::new(|| 92);\n   234:     ///\n   235:     /// assert_eq!(LazyLock::force(&lazy), &92);\n   236:     /// assert_eq!(&*lazy, &92);\n   237:     /// ```\n   238:     #[inline]\n   239:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   240:     #[rustc_should_not_be_called_on_const_items]\n   241:     pub fn force(this: &LazyLock<T, F>) -> &T {\n   242:         this.once.call_once_force(|state| {\n   243:             if state.is_poisoned() {\n   244:                 panic_poisoned();\n   245:             }\n   246: \n   247:             // SAFETY: `call_once` only runs this closure once, ever.\n   248:             let data = unsafe { &mut *this.data.get() };\n   249:             let f = unsafe { ManuallyDrop::take(&mut data.f) };\n   250:             let value = f();\n   251:             data.value = ManuallyDrop::new(value);",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LazyLock::force_mut",
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
      "name": "force_mut",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   161:     /// [`force()`]: LazyLock::force\n   162:     ///\n   163:     /// # Examples\n   164:     ///\n   165:     /// ```\n   166:     /// use std::sync::LazyLock;\n   167:     ///\n   168:     /// let mut lazy = LazyLock::new(|| 92);\n   169:     ///\n   170:     /// let p = LazyLock::force_mut(&mut lazy);\n   171:     /// assert_eq!(*p, 92);\n   172:     /// *p = 44;\n   173:     /// assert_eq!(*lazy, 44);\n   174:     /// ```\n   175:     #[inline]\n   176:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   177:     pub fn force_mut(this: &mut LazyLock<T, F>) -> &mut T {\n   178:         #[cold]\n   179:         /// # Safety\n   180:         /// May only be called when the state is `Incomplete`.\n   181:         unsafe fn really_init_mut<T, F: FnOnce() -> T>(this: &mut LazyLock<T, F>) -> &mut T {\n   182:             struct PoisonOnPanic<'a, T, F>(&'a mut LazyLock<T, F>);\n   183:             impl<T, F> Drop for PoisonOnPanic<'_, T, F> {\n   184:                 #[inline]\n   185:                 fn drop(&mut self) {\n   186:                     self.0.once.set_state(OnceExclusiveState::Poisoned);\n   187:                 }\n   188:             }\n   189: \n   190:             // SAFETY: We always poison if the initializer panics (then we never check the data),\n   191:             // or set the data on success.\n   192:             let f = unsafe { ManuallyDrop::take(&mut this.data.get_mut().f) };\n   193:             // INVARIANT: Initiated from mutable reference, don't drop because we read it.",
    "nanvix_source": "   167:     ///\n   168:     /// let mut lazy = LazyLock::new(|| 92);\n   169:     ///\n   170:     /// let p = LazyLock::force_mut(&mut lazy);\n   171:     /// assert_eq!(*p, 92);\n   172:     /// *p = 44;\n   173:     /// assert_eq!(*lazy, 44);\n   174:     /// ```\n   175:     #[inline]\n   176:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   177:     pub fn force_mut(this: &mut LazyLock<T, F>) -> &mut T {\n   178:         #[cold]\n   179:         /// # Safety\n   180:         /// May only be called when the state is `Incomplete`.\n   181:         unsafe fn really_init_mut<T, F: FnOnce() -> T>(this: &mut LazyLock<T, F>) -> &mut T {\n   182:             struct PoisonOnPanic<'a, T, F>(&'a mut LazyLock<T, F>);\n   183:             impl<T, F> Drop for PoisonOnPanic<'_, T, F> {\n   184:                 #[inline]\n   185:                 fn drop(&mut self) {\n   186:                     self.0.once.set_state(OnceExclusiveState::Poisoned);\n   187:                 }",
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
