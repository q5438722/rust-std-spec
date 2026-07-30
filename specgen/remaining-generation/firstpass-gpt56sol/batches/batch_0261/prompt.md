For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::Result::unwrap_or_else",
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
                              "generic": "E"
                            }
                          ],
                          "output": {
                            "generic": "T"
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
      "name": "unwrap_or_else",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1600: \n  1601:     /// Returns the contained [`Ok`] value or computes it from a closure.\n  1602:     ///\n  1603:     ///\n  1604:     /// # Examples\n  1605:     ///\n  1606:     /// ```\n  1607:     /// fn count(x: &str) -> usize { x.len() }\n  1608:     ///\n  1609:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1610:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1611:     /// ```\n  1612:     #[inline]\n  1613:     #[track_caller]\n  1614:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1615:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1616:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1617:     where\n  1618:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1619:     {\n  1620:         match self {\n  1621:             Ok(t) => t,\n  1622:             Err(e) => op(e),\n  1623:         }\n  1624:     }\n  1625: \n  1626:     /// Returns the contained [`Ok`] value, consuming the `self` value,\n  1627:     /// without checking that the value is not an [`Err`].\n  1628:     ///\n  1629:     /// # Safety\n  1630:     ///\n  1631:     /// Calling this method on an [`Err`] is *[undefined behavior]*.\n  1632:     ///",
    "nanvix_source": "  1604:     /// ```\n  1605:     /// fn count(x: &str) -> usize { x.len() }\n  1606:     ///\n  1607:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1608:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1609:     /// ```\n  1610:     #[inline]\n  1611:     #[track_caller]\n  1612:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1613:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1614:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1615:     where\n  1616:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1617:     {\n  1618:         match self {\n  1619:             Ok(t) => t,\n  1620:             Err(e) => op(e),\n  1621:         }\n  1622:     }\n  1623: \n  1624:     /// Returns the contained [`Ok`] value, consuming the `self` value,",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Result::unwrap_unchecked",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "unwrap_unchecked",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1634:     ///\n  1635:     /// # Examples\n  1636:     ///\n  1637:     /// ```\n  1638:     /// let x: Result<u32, &str> = Ok(2);\n  1639:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, 2);\n  1640:     /// ```\n  1641:     ///\n  1642:     /// ```no_run\n  1643:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1644:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1645:     /// ```\n  1646:     #[inline]\n  1647:     #[track_caller]\n  1648:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1649:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1650:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1651:         match self {\n  1652:             Ok(t) => t,\n  1653:             Err(e) => {\n  1654:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1655:                 super::mem::forget(e);\n  1656:                 // SAFETY: the safety contract must be upheld by the caller.\n  1657:                 unsafe { hint::unreachable_unchecked() }\n  1658:             }\n  1659:         }\n  1660:     }\n  1661: \n  1662:     /// Returns the contained [`Err`] value, consuming the `self` value,\n  1663:     /// without checking that the value is not an [`Ok`].\n  1664:     ///\n  1665:     /// # Safety\n  1666:     ///",
    "nanvix_source": "  1638:     /// ```\n  1639:     ///\n  1640:     /// ```no_run\n  1641:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1642:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1647:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1648:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1649:         match self {\n  1650:             Ok(t) => t,\n  1651:             Err(e) => {\n  1652:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1653:                 super::mem::forget(e);\n  1654:                 // SAFETY: the safety contract must be upheld by the caller.\n  1655:                 unsafe { hint::unreachable_unchecked() }\n  1656:             }\n  1657:         }\n  1658:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Scope::spawn",
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
            "name": "T"
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
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 20,
                      "path": "FnOnce"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 6,
                      "path": "Send"
                    }
                  }
                },
                {
                  "outlives": "'scope"
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 6,
                      "path": "Send"
                    }
                  }
                },
                {
                  "outlives": "'scope"
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
      "name": "spawn",
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
                    "lifetime": "'scope"
                  },
                  {
                    "lifetime": "'env"
                  }
                ],
                "constraints": []
              }
            },
            "id": 480,
            "path": "Scope"
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
              "name": "'scope"
            },
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'env"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:606",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:480",
        "resolved_owner_path": [
          "std",
          "thread",
          "scoped",
          "Scope"
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
                "lifetime": "'scope",
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
                    "lifetime": "'scope"
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
            "id": 481,
            "path": "ScopedJoinHandle"
          }
        }
      }
    },
    "verification_source": "   185:     /// the panic payload.\n   186:     ///\n   187:     /// If the join handle is dropped, the spawned thread will be implicitly joined at the\n   188:     /// end of the scope. In that case, if the spawned thread panics, [`scope`] will\n   189:     /// panic after all threads are joined.\n   190:     ///\n   191:     /// This function creates a thread with the default parameters of [`Builder`].\n   192:     /// To specify the new thread's stack size or the name, use [`Builder::spawn_scoped`].\n   193:     ///\n   194:     /// # Panics\n   195:     ///\n   196:     /// Panics if the OS fails to create a thread; use [`Builder::spawn_scoped`]\n   197:     /// to recover from such errors.\n   198:     ///\n   199:     /// [`join`]: ScopedJoinHandle::join\n   200:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   201:     pub fn spawn<F, T>(&'scope self, f: F) -> ScopedJoinHandle<'scope, T>\n   202:     where\n   203:         F: FnOnce() -> T + Send + 'scope,\n   204:         T: Send + 'scope,\n   205:     {\n   206:         Builder::new().spawn_scoped(self, f).expect(\"failed to spawn thread\")\n   207:     }\n   208: }\n   209: \n   210: impl Builder {\n   211:     /// Spawns a new scoped thread using the settings set through this `Builder`.\n   212:     ///\n   213:     /// Unlike [`Scope::spawn`], this method yields an [`io::Result`] to\n   214:     /// capture any failure to create the thread at the OS level.\n   215:     ///\n   216:     /// # Panics\n   217:     ///",
    "nanvix_source": "   191:     /// This function creates a thread with the default parameters of [`Builder`].\n   192:     /// To specify the new thread's stack size or the name, use [`Builder::spawn_scoped`].\n   193:     ///\n   194:     /// # Panics\n   195:     ///\n   196:     /// Panics if the OS fails to create a thread; use [`Builder::spawn_scoped`]\n   197:     /// to recover from such errors.\n   198:     ///\n   199:     /// [`join`]: ScopedJoinHandle::join\n   200:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   201:     pub fn spawn<F, T>(&'scope self, f: F) -> ScopedJoinHandle<'scope, T>\n   202:     where\n   203:         F: FnOnce() -> T + Send + 'scope,\n   204:         T: Send + 'scope,\n   205:     {\n   206:         Builder::new().spawn_scoped(self, f).expect(\"failed to spawn thread\")\n   207:     }\n   208: }\n   209: \n   210: impl Builder {\n   211:     /// Spawns a new scoped thread using the settings set through this `Builder`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::ScopedJoinHandle::is_finished",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "is_finished",
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
                    "lifetime": "'scope"
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
            "id": 481,
            "path": "ScopedJoinHandle"
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
              "name": "'scope"
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
        "impl_id": "std:626",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:481",
        "resolved_owner_path": [
          "std",
          "thread",
          "scoped",
          "ScopedJoinHandle"
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
    "verification_source": "   309:     /// # Examples\n   310:     ///\n   311:     /// ```\n   312:     /// use std::thread;\n   313:     ///\n   314:     /// thread::scope(|s| {\n   315:     ///     let t = s.spawn(|| {\n   316:     ///         panic!(\"oh no\");\n   317:     ///     });\n   318:     ///     assert!(t.join().is_err());\n   319:     /// });\n   320:     /// ```\n   321:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   322:     pub fn join(self) -> Result<T> {\n   323:         self.0.join()\n   324:     }\n   325: \n   326:     /// Checks if the associated thread has finished running its main function.\n   327:     ///\n   328:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   329:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   330:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   331:     ///\n   332:     /// This might return `true` for a brief moment after the thread's main\n   333:     /// function has returned, but before the thread itself has stopped running.\n   334:     /// However, once this returns `true`, [`join`][Self::join] can be expected\n   335:     /// to return quickly, without blocking for any significant amount of time.\n   336:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   337:     pub fn is_finished(&self) -> bool {\n   338:         self.0.is_finished()\n   339:     }\n   340: }\n   341: ",
    "nanvix_source": "   315:     ///     let t = s.spawn(|| {\n   316:     ///         panic!(\"oh no\");\n   317:     ///     });\n   318:     ///     assert!(t.join().is_err());\n   319:     /// });\n   320:     /// ```\n   321:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   322:     pub fn join(self) -> Result<T> {\n   323:         self.0.join()\n   324:     }\n   325: \n   326:     /// Checks if the associated thread has finished running its main function.\n   327:     ///\n   328:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   329:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   330:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   331:     ///\n   332:     /// This might return `true` for a brief moment after the thread's main\n   333:     /// function has returned, but before the thread itself has stopped running.\n   334:     /// However, once this returns `true`, [`join`][Self::join] can be expected\n   335:     /// to return quickly, without blocking for any significant amount of time.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::ScopedJoinHandle::join",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "join",
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
                    "lifetime": "'scope"
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
            "id": 481,
            "path": "ScopedJoinHandle"
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
              "name": "'scope"
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
        "impl_id": "std:626",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:481",
        "resolved_owner_path": [
          "std",
          "thread",
          "scoped",
          "ScopedJoinHandle"
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
            "id": 561,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   302:     /// [happen before](https://doc.rust-lang.org/nomicon/atomics.html#data-accesses)\n   303:     /// all operations that happen after `join` returns.\n   304:     ///\n   305:     /// If the associated thread panics, [`Err`] is returned with the panic payload.\n   306:     ///\n   307:     /// [atomic memory orderings]: crate::sync::atomic\n   308:     ///\n   309:     /// # Examples\n   310:     ///\n   311:     /// ```\n   312:     /// use std::thread;\n   313:     ///\n   314:     /// thread::scope(|s| {\n   315:     ///     let t = s.spawn(|| {\n   316:     ///         panic!(\"oh no\");\n   317:     ///     });\n   318:     ///     assert!(t.join().is_err());\n   319:     /// });\n   320:     /// ```\n   321:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   322:     pub fn join(self) -> Result<T> {\n   323:         self.0.join()\n   324:     }\n   325: \n   326:     /// Checks if the associated thread has finished running its main function.\n   327:     ///\n   328:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   329:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   330:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   331:     ///\n   332:     /// This might return `true` for a brief moment after the thread's main\n   333:     /// function has returned, but before the thread itself has stopped running.\n   334:     /// However, once this returns `true`, [`join`][Self::join] can be expected",
    "nanvix_source": "   308:     ///\n   309:     /// # Examples\n   310:     ///\n   311:     /// ```\n   312:     /// use std::thread;\n   313:     ///\n   314:     /// thread::scope(|s| {\n   315:     ///     let t = s.spawn(|| {\n   316:     ///         panic!(\"oh no\");\n   317:     ///     });\n   318:     ///     assert!(t.join().is_err());\n   319:     /// });\n   320:     /// ```\n   321:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   322:     pub fn join(self) -> Result<T> {\n   323:         self.0.join()\n   324:     }\n   325: \n   326:     /// Checks if the associated thread has finished running its main function.\n   327:     ///\n   328:     /// `is_finished` supports implementing a non-blocking join operation, by checking",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::ScopedJoinHandle::thread",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "thread",
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
                    "lifetime": "'scope"
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
            "id": 481,
            "path": "ScopedJoinHandle"
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
              "name": "'scope"
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
        "impl_id": "std:626",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:481",
        "resolved_owner_path": [
          "std",
          "thread",
          "scoped",
          "ScopedJoinHandle"
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
              "resolved_path": {
                "args": null,
                "id": 504,
                "path": "Thread"
              }
            }
          }
        }
      }
    },
    "verification_source": "   273:     /// Extracts a handle to the underlying thread.\n   274:     ///\n   275:     /// # Examples\n   276:     ///\n   277:     /// ```\n   278:     /// use std::thread;\n   279:     ///\n   280:     /// thread::scope(|s| {\n   281:     ///     let t = s.spawn(|| {\n   282:     ///         println!(\"hello\");\n   283:     ///     });\n   284:     ///     println!(\"thread id: {:?}\", t.thread().id());\n   285:     /// });\n   286:     /// ```\n   287:     #[must_use]\n   288:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   289:     pub fn thread(&self) -> &Thread {\n   290:         self.0.thread()\n   291:     }\n   292: \n   293:     /// Waits for the associated thread to finish.\n   294:     ///\n   295:     /// This function will return immediately if the associated thread has already finished.\n   296:     /// Otherwise, it fully waits for the thread to finish, including all destructors\n   297:     /// for thread-local variables that might be running after the main function of the thread.\n   298:     ///\n   299:     /// In terms of [atomic memory orderings], the completion of the associated\n   300:     /// thread synchronizes with this function returning.\n   301:     /// In other words, all operations performed by that thread\n   302:     /// [happen before](https://doc.rust-lang.org/nomicon/atomics.html#data-accesses)\n   303:     /// all operations that happen after `join` returns.\n   304:     ///\n   305:     /// If the associated thread panics, [`Err`] is returned with the panic payload.",
    "nanvix_source": "   279:     ///\n   280:     /// thread::scope(|s| {\n   281:     ///     let t = s.spawn(|| {\n   282:     ///         println!(\"hello\");\n   283:     ///     });\n   284:     ///     println!(\"thread id: {:?}\", t.thread().id());\n   285:     /// });\n   286:     /// ```\n   287:     #[must_use]\n   288:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   289:     pub fn thread(&self) -> &Thread {\n   290:         self.0.thread()\n   291:     }\n   292: \n   293:     /// Waits for the associated thread to finish.\n   294:     ///\n   295:     /// This function will return immediately if the associated thread has already finished.\n   296:     /// Otherwise, it fully waits for the thread to finish, including all destructors\n   297:     /// for thread-local variables that might be running after the main function of the thread.\n   298:     ///\n   299:     /// In terms of [atomic memory orderings], the completion of the associated",
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
