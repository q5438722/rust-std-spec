For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::OnceLock::get_or_init",
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
      "name": "get_or_init",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
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
    "verification_source": "   301:     /// this may be changed to a panic in the future.\n   302:     ///\n   303:     /// # Examples\n   304:     ///\n   305:     /// ```\n   306:     /// use std::sync::OnceLock;\n   307:     ///\n   308:     /// let cell = OnceLock::new();\n   309:     /// let value = cell.get_or_init(|| 92);\n   310:     /// assert_eq!(value, &92);\n   311:     /// let value = cell.get_or_init(|| unreachable!());\n   312:     /// assert_eq!(value, &92);\n   313:     /// ```\n   314:     #[inline]\n   315:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   316:     #[rustc_should_not_be_called_on_const_items]\n   317:     pub fn get_or_init<F>(&self, f: F) -> &T\n   318:     where\n   319:         F: FnOnce() -> T,\n   320:     {\n   321:         match self.get_or_try_init(|| Ok::<T, !>(f())) {\n   322:             Ok(val) => val,\n   323:         }\n   324:     }\n   325: \n   326:     /// Gets the mutable reference of the contents of the cell, initializing\n   327:     /// it to `f()` if the cell was uninitialized.\n   328:     ///\n   329:     /// This method never blocks. Since it borrows the `OnceLock` mutably,\n   330:     /// it is statically guaranteed that no active borrows to the `OnceLock`\n   331:     /// exist, including from other threads.\n   332:     ///\n   333:     /// # Panics",
    "nanvix_source": "   307:     ///\n   308:     /// let cell = OnceLock::new();\n   309:     /// let value = cell.get_or_init(|| 92);\n   310:     /// assert_eq!(value, &92);\n   311:     /// let value = cell.get_or_init(|| unreachable!());\n   312:     /// assert_eq!(value, &92);\n   313:     /// ```\n   314:     #[inline]\n   315:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   316:     #[rustc_should_not_be_called_on_const_items]\n   317:     pub fn get_or_init<F>(&self, f: F) -> &T\n   318:     where\n   319:         F: FnOnce() -> T,\n   320:     {\n   321:         match self.get_or_try_init(|| Ok::<T, !>(f())) {\n   322:             Ok(val) => val,\n   323:         }\n   324:     }\n   325: \n   326:     /// Gets the mutable reference of the contents of the cell, initializing\n   327:     /// it to `f()` if the cell was uninitialized.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::into_inner",
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
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
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
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   462:     /// `None` if the cell was uninitialized.\n   463:     ///\n   464:     /// # Examples\n   465:     ///\n   466:     /// ```\n   467:     /// use std::sync::OnceLock;\n   468:     ///\n   469:     /// let cell: OnceLock<String> = OnceLock::new();\n   470:     /// assert_eq!(cell.into_inner(), None);\n   471:     ///\n   472:     /// let cell = OnceLock::new();\n   473:     /// cell.set(\"hello\".to_string()).unwrap();\n   474:     /// assert_eq!(cell.into_inner(), Some(\"hello\".to_string()));\n   475:     /// ```\n   476:     #[inline]\n   477:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   478:     pub fn into_inner(mut self) -> Option<T> {\n   479:         self.take()\n   480:     }\n   481: \n   482:     /// Takes the value out of this `OnceLock`, moving it back to an uninitialized state.\n   483:     ///\n   484:     /// Has no effect and returns `None` if the `OnceLock` was uninitialized.\n   485:     ///\n   486:     /// Since this method borrows the `OnceLock` mutably, it is statically guaranteed that\n   487:     /// no active borrows to the `OnceLock` exist, including from other threads.\n   488:     ///\n   489:     /// # Examples\n   490:     ///\n   491:     /// ```\n   492:     /// use std::sync::OnceLock;\n   493:     ///\n   494:     /// let mut cell: OnceLock<String> = OnceLock::new();",
    "nanvix_source": "   468:     ///\n   469:     /// let cell: OnceLock<String> = OnceLock::new();\n   470:     /// assert_eq!(cell.into_inner(), None);\n   471:     ///\n   472:     /// let cell = OnceLock::new();\n   473:     /// cell.set(\"hello\".to_string()).unwrap();\n   474:     /// assert_eq!(cell.into_inner(), Some(\"hello\".to_string()));\n   475:     /// ```\n   476:     #[inline]\n   477:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   478:     pub fn into_inner(mut self) -> Option<T> {\n   479:         self.take()\n   480:     }\n   481: \n   482:     /// Takes the value out of this `OnceLock`, moving it back to an uninitialized state.\n   483:     ///\n   484:     /// Has no effect and returns `None` if the `OnceLock` was uninitialized.\n   485:     ///\n   486:     /// Since this method borrows the `OnceLock` mutably, it is statically guaranteed that\n   487:     /// no active borrows to the `OnceLock` exist, including from other threads.\n   488:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::new",
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
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
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
            "id": 8271,
            "path": "OnceLock"
          }
        }
      }
    },
    "verification_source": "   124:     ///\n   125:     /// let cell = OnceLock::new();\n   126:     /// {\n   127:     ///     let s = String::new();\n   128:     ///     let _ = cell.set(A(&s));\n   129:     /// }\n   130:     /// ```\n   131:     _marker: PhantomData<T>,\n   132: }\n   133: \n   134: impl<T> OnceLock<T> {\n   135:     /// Creates a new uninitialized cell.\n   136:     #[inline]\n   137:     #[must_use]\n   138:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   139:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n   140:     pub const fn new() -> OnceLock<T> {\n   141:         OnceLock {\n   142:             once: Once::new(),\n   143:             value: UnsafeCell::new(MaybeUninit::uninit()),\n   144:             _marker: PhantomData,\n   145:         }\n   146:     }\n   147: \n   148:     /// Gets the reference to the underlying value.\n   149:     ///\n   150:     /// Returns `None` if the cell is uninitialized, or being initialized.\n   151:     /// This method never blocks.\n   152:     #[inline]\n   153:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   154:     #[rustc_should_not_be_called_on_const_items]\n   155:     pub fn get(&self) -> Option<&T> {\n   156:         if self.initialized() {",
    "nanvix_source": "   130:     /// ```\n   131:     _marker: PhantomData<T>,\n   132: }\n   133: \n   134: impl<T> OnceLock<T> {\n   135:     /// Creates a new uninitialized cell.\n   136:     #[inline]\n   137:     #[must_use]\n   138:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   139:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n   140:     pub const fn new() -> OnceLock<T> {\n   141:         OnceLock {\n   142:             once: Once::new(),\n   143:             value: UnsafeCell::new(MaybeUninit::uninit()),\n   144:             _marker: PhantomData,\n   145:         }\n   146:     }\n   147: \n   148:     /// Gets the reference to the underlying value.\n   149:     ///\n   150:     /// Returns `None` if the cell is uninitialized, or being initialized.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::set",
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
      "name": "set",
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
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
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
                      "tuple": []
                    }
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
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   222:     /// static CELL: OnceLock<i32> = OnceLock::new();\n   223:     ///\n   224:     /// fn main() {\n   225:     ///     assert!(CELL.get().is_none());\n   226:     ///\n   227:     ///     std::thread::spawn(|| {\n   228:     ///         assert_eq!(CELL.set(92), Ok(()));\n   229:     ///     }).join().unwrap();\n   230:     ///\n   231:     ///     assert_eq!(CELL.set(62), Err(62));\n   232:     ///     assert_eq!(CELL.get(), Some(&92));\n   233:     /// }\n   234:     /// ```\n   235:     #[inline]\n   236:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   237:     #[rustc_should_not_be_called_on_const_items]\n   238:     pub fn set(&self, value: T) -> Result<(), T> {\n   239:         match self.try_insert(value) {\n   240:             Ok(_) => Ok(()),\n   241:             Err((_, value)) => Err(value),\n   242:         }\n   243:     }\n   244: \n   245:     /// Initializes the contents of the cell to `value` if the cell was uninitialized,\n   246:     /// then returns a reference to it.\n   247:     ///\n   248:     /// May block if another thread is currently attempting to initialize the cell. The cell is\n   249:     /// guaranteed to contain a value when `try_insert` returns, though not necessarily the\n   250:     /// one provided.\n   251:     ///\n   252:     /// Returns `Ok(&value)` if the cell was uninitialized and\n   253:     /// `Err((&current_value, value))` if it was already initialized.\n   254:     ///",
    "nanvix_source": "   228:     ///         assert_eq!(CELL.set(92), Ok(()));\n   229:     ///     }).join().unwrap();\n   230:     ///\n   231:     ///     assert_eq!(CELL.set(62), Err(62));\n   232:     ///     assert_eq!(CELL.get(), Some(&92));\n   233:     /// }\n   234:     /// ```\n   235:     #[inline]\n   236:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   237:     #[rustc_should_not_be_called_on_const_items]\n   238:     pub fn set(&self, value: T) -> Result<(), T> {\n   239:         match self.try_insert(value) {\n   240:             Ok(_) => Ok(()),\n   241:             Err((_, value)) => Err(value),\n   242:         }\n   243:     }\n   244: \n   245:     /// Initializes the contents of the cell to `value` if the cell was uninitialized,\n   246:     /// then returns a reference to it.\n   247:     ///\n   248:     /// May block if another thread is currently attempting to initialize the cell. The cell is",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::take",
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
      "name": "take",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
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
                      "generic": "T"
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
    "verification_source": "   488:     ///\n   489:     /// # Examples\n   490:     ///\n   491:     /// ```\n   492:     /// use std::sync::OnceLock;\n   493:     ///\n   494:     /// let mut cell: OnceLock<String> = OnceLock::new();\n   495:     /// assert_eq!(cell.take(), None);\n   496:     ///\n   497:     /// let mut cell = OnceLock::new();\n   498:     /// cell.set(\"hello\".to_string()).unwrap();\n   499:     /// assert_eq!(cell.take(), Some(\"hello\".to_string()));\n   500:     /// assert_eq!(cell.get(), None);\n   501:     /// ```\n   502:     #[inline]\n   503:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   504:     pub fn take(&mut self) -> Option<T> {\n   505:         if self.initialized_mut() {\n   506:             self.once = Once::new();\n   507:             // SAFETY: `self.value` is initialized and contains a valid `T`.\n   508:             // `self.once` is reset, so `initialized()` will be false again\n   509:             // which prevents the value from being read twice.\n   510:             unsafe { Some(self.value.get_mut().assume_init_read()) }\n   511:         } else {\n   512:             None\n   513:         }\n   514:     }\n   515: \n   516:     #[inline]\n   517:     fn initialized(&self) -> bool {\n   518:         self.once.is_completed()\n   519:     }\n   520: ",
    "nanvix_source": "   494:     /// let mut cell: OnceLock<String> = OnceLock::new();\n   495:     /// assert_eq!(cell.take(), None);\n   496:     ///\n   497:     /// let mut cell = OnceLock::new();\n   498:     /// cell.set(\"hello\".to_string()).unwrap();\n   499:     /// assert_eq!(cell.take(), Some(\"hello\".to_string()));\n   500:     /// assert_eq!(cell.get(), None);\n   501:     /// ```\n   502:     #[inline]\n   503:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   504:     pub fn take(&mut self) -> Option<T> {\n   505:         if self.initialized_mut() {\n   506:             self.once = Once::new();\n   507:             // SAFETY: `self.value` is initialized and contains a valid `T`.\n   508:             // `self.once` is reset, so `initialized()` will be false again\n   509:             // which prevents the value from being read twice.\n   510:             unsafe { Some(self.value.get_mut().assume_init_read()) }\n   511:         } else {\n   512:             None\n   513:         }\n   514:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::wait",
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
      "name": "wait",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8271,
            "path": "OnceLock"
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
        "impl_id": "std:8421",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8271",
        "resolved_owner_path": [
          "std",
          "sync",
          "once_lock",
          "OnceLock"
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
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   187:     /// ```rust\n   188:     /// use std::thread;\n   189:     /// use std::sync::OnceLock;\n   190:     ///\n   191:     /// let value = OnceLock::new();\n   192:     ///\n   193:     /// thread::scope(|s| {\n   194:     ///     s.spawn(|| value.set(1 + 1));\n   195:     ///\n   196:     ///     let result = value.wait();\n   197:     ///     assert_eq!(result, &2);\n   198:     /// })\n   199:     /// ```\n   200:     #[inline]\n   201:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   202:     #[rustc_should_not_be_called_on_const_items]\n   203:     pub fn wait(&self) -> &T {\n   204:         self.once.wait_force();\n   205: \n   206:         unsafe { self.get_unchecked() }\n   207:     }\n   208: \n   209:     /// Initializes the contents of the cell to `value`.\n   210:     ///\n   211:     /// May block if another thread is currently attempting to initialize the cell. The cell is\n   212:     /// guaranteed to contain a value when `set` returns, though not necessarily the one provided.\n   213:     ///\n   214:     /// Returns `Ok(())` if the cell was uninitialized and\n   215:     /// `Err(value)` if the cell was already initialized.\n   216:     ///\n   217:     /// # Examples\n   218:     ///\n   219:     /// ```",
    "nanvix_source": "   193:     /// thread::scope(|s| {\n   194:     ///     s.spawn(|| value.set(1 + 1));\n   195:     ///\n   196:     ///     let result = value.wait();\n   197:     ///     assert_eq!(result, &2);\n   198:     /// })\n   199:     /// ```\n   200:     #[inline]\n   201:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   202:     #[rustc_should_not_be_called_on_const_items]\n   203:     pub fn wait(&self) -> &T {\n   204:         self.once.wait_force();\n   205: \n   206:         unsafe { self.get_unchecked() }\n   207:     }\n   208: \n   209:     /// Initializes the contents of the cell to `value`.\n   210:     ///\n   211:     /// May block if another thread is currently attempting to initialize the cell. The cell is\n   212:     /// guaranteed to contain a value when `set` returns, though not necessarily the one provided.\n   213:     ///",
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
