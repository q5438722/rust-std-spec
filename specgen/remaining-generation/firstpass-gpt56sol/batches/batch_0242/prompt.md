For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::OnceState::is_poisoned",
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
            "args": null,
            "id": 8276,
            "path": "OnceState"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8299",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8276",
        "resolved_owner_path": [
          "std",
          "sync",
          "once",
          "OnceState"
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
    "verification_source": "   355:     ///\n   356:     /// ```\n   357:     /// use std::sync::Once;\n   358:     /// use std::thread;\n   359:     ///\n   360:     /// static INIT: Once = Once::new();\n   361:     ///\n   362:     /// // poison the once\n   363:     /// let handle = thread::spawn(|| {\n   364:     ///     INIT.call_once(|| panic!());\n   365:     /// });\n   366:     /// assert!(handle.join().is_err());\n   367:     ///\n   368:     /// INIT.call_once_force(|state| {\n   369:     ///     assert!(state.is_poisoned());\n   370:     /// });\n   371:     /// ```\n   372:     ///\n   373:     /// An unpoisoned [`Once`]:\n   374:     ///\n   375:     /// ```\n   376:     /// use std::sync::Once;\n   377:     ///\n   378:     /// static INIT: Once = Once::new();\n   379:     ///\n   380:     /// INIT.call_once_force(|state| {\n   381:     ///     assert!(!state.is_poisoned());\n   382:     /// });\n   383:     #[stable(feature = \"once_poison\", since = \"1.51.0\")]\n   384:     #[inline]\n   385:     pub fn is_poisoned(&self) -> bool {\n   386:         self.inner.is_poisoned()\n   387:     }",
    "nanvix_source": "   361:     ///\n   362:     /// // poison the once\n   363:     /// let handle = thread::spawn(|| {\n   364:     ///     INIT.call_once(|| panic!());\n   365:     /// });\n   366:     /// assert!(handle.join().is_err());\n   367:     ///\n   368:     /// INIT.call_once_force(|state| {\n   369:     ///     assert!(state.is_poisoned());\n   370:     /// });\n   371:     /// ```\n   372:     ///\n   373:     /// An unpoisoned [`Once`]:\n   374:     ///\n   375:     /// ```\n   376:     /// use std::sync::Once;\n   377:     ///\n   378:     /// static INIT: Once = Once::new();\n   379:     ///\n   380:     /// INIT.call_once_force(|state| {\n   381:     ///     assert!(!state.is_poisoned());",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::PoisonError::get_mut",
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
            "id": 8886,
            "path": "PoisonError"
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
        "impl_id": "std:9176",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8886",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "PoisonError"
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
    "verification_source": "   311:     /// ```\n   312:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   313:     pub fn into_inner(self) -> T {\n   314:         self.data\n   315:     }\n   316: \n   317:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   318:     /// reference to the associated data.\n   319:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   320:     pub fn get_ref(&self) -> &T {\n   321:         &self.data\n   322:     }\n   323: \n   324:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   325:     /// mutable reference to the associated data.\n   326:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   327:     pub fn get_mut(&mut self) -> &mut T {\n   328:         &mut self.data\n   329:     }\n   330: }\n   331: \n   332: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   333: impl<T> From<PoisonError<T>> for TryLockError<T> {\n   334:     fn from(err: PoisonError<T>) -> TryLockError<T> {\n   335:         TryLockError::Poisoned(err)\n   336:     }\n   337: }\n   338: \n   339: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   340: impl<T> fmt::Debug for TryLockError<T> {\n   341:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   342:         match *self {\n   343:             #[cfg(panic = \"unwind\")]",
    "nanvix_source": "   314:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   315:     /// reference to the associated data.\n   316:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   317:     pub fn get_ref(&self) -> &T {\n   318:         &self.data\n   319:     }\n   320: \n   321:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   322:     /// mutable reference to the associated data.\n   323:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   324:     pub fn get_mut(&mut self) -> &mut T {\n   325:         &mut self.data\n   326:     }\n   327: }\n   328: \n   329: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   330: impl<T> From<PoisonError<T>> for TryLockError<T> {\n   331:     fn from(err: PoisonError<T>) -> TryLockError<T> {\n   332:         TryLockError::Poisoned(err)\n   333:     }\n   334: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::PoisonError::get_ref",
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
      "name": "get_ref",
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
            "id": 8886,
            "path": "PoisonError"
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
        "impl_id": "std:9176",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8886",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "PoisonError"
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
    "verification_source": "   304:     ///     data.insert(10);\n   305:     ///     panic!();\n   306:     /// }).join();\n   307:     ///\n   308:     /// let p_err = mutex.lock().unwrap_err();\n   309:     /// let data = p_err.into_inner();\n   310:     /// println!(\"recovered {} items\", data.len());\n   311:     /// ```\n   312:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   313:     pub fn into_inner(self) -> T {\n   314:         self.data\n   315:     }\n   316: \n   317:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   318:     /// reference to the associated data.\n   319:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   320:     pub fn get_ref(&self) -> &T {\n   321:         &self.data\n   322:     }\n   323: \n   324:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   325:     /// mutable reference to the associated data.\n   326:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   327:     pub fn get_mut(&mut self) -> &mut T {\n   328:         &mut self.data\n   329:     }\n   330: }\n   331: \n   332: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   333: impl<T> From<PoisonError<T>> for TryLockError<T> {\n   334:     fn from(err: PoisonError<T>) -> TryLockError<T> {\n   335:         TryLockError::Poisoned(err)\n   336:     }",
    "nanvix_source": "   307:     /// println!(\"recovered {} items\", data.len());\n   308:     /// ```\n   309:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   310:     pub fn into_inner(self) -> T {\n   311:         self.data\n   312:     }\n   313: \n   314:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   315:     /// reference to the associated data.\n   316:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   317:     pub fn get_ref(&self) -> &T {\n   318:         &self.data\n   319:     }\n   320: \n   321:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   322:     /// mutable reference to the associated data.\n   323:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   324:     pub fn get_mut(&mut self) -> &mut T {\n   325:         &mut self.data\n   326:     }\n   327: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::PoisonError::into_inner",
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
            "id": 8886,
            "path": "PoisonError"
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
        "impl_id": "std:9176",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8886",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "PoisonError"
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
    "verification_source": "   297:     ///\n   298:     /// let mutex = Arc::new(Mutex::new(HashSet::new()));\n   299:     ///\n   300:     /// // poison the mutex\n   301:     /// let c_mutex = Arc::clone(&mutex);\n   302:     /// let _ = thread::spawn(move || {\n   303:     ///     let mut data = c_mutex.lock().unwrap();\n   304:     ///     data.insert(10);\n   305:     ///     panic!();\n   306:     /// }).join();\n   307:     ///\n   308:     /// let p_err = mutex.lock().unwrap_err();\n   309:     /// let data = p_err.into_inner();\n   310:     /// println!(\"recovered {} items\", data.len());\n   311:     /// ```\n   312:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   313:     pub fn into_inner(self) -> T {\n   314:         self.data\n   315:     }\n   316: \n   317:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   318:     /// reference to the associated data.\n   319:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   320:     pub fn get_ref(&self) -> &T {\n   321:         &self.data\n   322:     }\n   323: \n   324:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   325:     /// mutable reference to the associated data.\n   326:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   327:     pub fn get_mut(&mut self) -> &mut T {\n   328:         &mut self.data\n   329:     }",
    "nanvix_source": "   300:     ///     let mut data = c_mutex.lock().unwrap();\n   301:     ///     data.insert(10);\n   302:     ///     panic!();\n   303:     /// }).join();\n   304:     ///\n   305:     /// let p_err = mutex.lock().unwrap_err();\n   306:     /// let data = p_err.into_inner();\n   307:     /// println!(\"recovered {} items\", data.len());\n   308:     /// ```\n   309:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   310:     pub fn into_inner(self) -> T {\n   311:         self.data\n   312:     }\n   313: \n   314:     /// Reaches into this error indicating that a lock is poisoned, returning a\n   315:     /// reference to the associated data.\n   316:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   317:     pub fn get_ref(&self) -> &T {\n   318:         &self.data\n   319:     }\n   320: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::PoisonError::new",
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
            "id": 8886,
            "path": "PoisonError"
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
        "impl_id": "std:9176",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8886",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "PoisonError"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "data",
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
            "id": 8886,
            "path": "PoisonError"
          }
        }
      }
    },
    "verification_source": "   255:         \"poisoned lock: another task failed inside\".fmt(f)\n   256:     }\n   257: }\n   258: \n   259: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   260: impl<T> Error for PoisonError<T> {}\n   261: \n   262: impl<T> PoisonError<T> {\n   263:     /// Creates a `PoisonError`.\n   264:     ///\n   265:     /// This is generally created by methods like [`Mutex::lock`](crate::sync::Mutex::lock)\n   266:     /// or [`RwLock::read`](crate::sync::RwLock::read).\n   267:     ///\n   268:     /// This method may panic if std was built with `panic=\"abort\"`.\n   269:     #[cfg(panic = \"unwind\")]\n   270:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   271:     pub fn new(data: T) -> PoisonError<T> {\n   272:         PoisonError { data }\n   273:     }\n   274: \n   275:     /// Creates a `PoisonError`.\n   276:     ///\n   277:     /// This is generally created by methods like [`Mutex::lock`](crate::sync::Mutex::lock)\n   278:     /// or [`RwLock::read`](crate::sync::RwLock::read).\n   279:     ///\n   280:     /// This method may panic if std was built with `panic=\"abort\"`.\n   281:     #[cfg(not(panic = \"unwind\"))]\n   282:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   283:     #[track_caller]\n   284:     pub fn new(_data: T) -> PoisonError<T> {\n   285:         panic!(\"PoisonError created in a libstd built with panic=\\\"abort\\\"\")\n   286:     }\n   287: ",
    "nanvix_source": "   258: \n   259: impl<T> PoisonError<T> {\n   260:     /// Creates a `PoisonError`.\n   261:     ///\n   262:     /// This is generally created by methods like [`Mutex::lock`](crate::sync::Mutex::lock)\n   263:     /// or [`RwLock::read`](crate::sync::RwLock::read).\n   264:     ///\n   265:     /// This method may panic if std was built with `panic=\"abort\"`.\n   266:     #[cfg(panic = \"unwind\")]\n   267:     #[stable(feature = \"sync_poison\", since = \"1.2.0\")]\n   268:     pub fn new(data: T) -> PoisonError<T> {\n   269:         PoisonError { data }\n   270:     }\n   271: \n   272:     /// Creates a `PoisonError`.\n   273:     ///\n   274:     /// This is generally created by methods like [`Mutex::lock`](crate::sync::Mutex::lock)\n   275:     /// or [`RwLock::read`](crate::sync::RwLock::read).\n   276:     ///\n   277:     /// This method may panic if std was built with `panic=\"abort\"`.\n   278:     #[cfg(not(panic = \"unwind\"))]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::RwLock::clear_poison",
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
      "name": "clear_poison",
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
        "output": null
      }
    },
    "verification_source": "   603:     /// let _ = thread::spawn(move || {\n   604:     ///     let _lock = c_lock.write().unwrap();\n   605:     ///     panic!(); // the lock gets poisoned\n   606:     /// }).join();\n   607:     ///\n   608:     /// assert_eq!(lock.is_poisoned(), true);\n   609:     /// let guard = lock.write().unwrap_or_else(|mut e| {\n   610:     ///     **e.get_mut() = 1;\n   611:     ///     lock.clear_poison();\n   612:     ///     e.into_inner()\n   613:     /// });\n   614:     /// assert_eq!(lock.is_poisoned(), false);\n   615:     /// assert_eq!(*guard, 1);\n   616:     /// ```\n   617:     #[inline]\n   618:     #[stable(feature = \"mutex_unpoison\", since = \"1.77.0\")]\n   619:     pub fn clear_poison(&self) {\n   620:         self.poison.clear();\n   621:     }\n   622: \n   623:     /// Consumes this `RwLock`, returning the underlying data.\n   624:     ///\n   625:     /// # Errors\n   626:     ///\n   627:     /// This function will return an error containing the underlying data if\n   628:     /// the `RwLock` is poisoned. An `RwLock` is poisoned whenever a writer\n   629:     /// panics while holding an exclusive lock. An error will only be returned\n   630:     /// if the lock would have otherwise been acquired.\n   631:     ///\n   632:     /// # Examples\n   633:     ///\n   634:     /// ```\n   635:     /// use std::sync::RwLock;",
    "nanvix_source": "   609:     /// let guard = lock.write().unwrap_or_else(|mut e| {\n   610:     ///     **e.get_mut() = 1;\n   611:     ///     lock.clear_poison();\n   612:     ///     e.into_inner()\n   613:     /// });\n   614:     /// assert_eq!(lock.is_poisoned(), false);\n   615:     /// assert_eq!(*guard, 1);\n   616:     /// ```\n   617:     #[inline]\n   618:     #[stable(feature = \"mutex_unpoison\", since = \"1.77.0\")]\n   619:     pub fn clear_poison(&self) {\n   620:         self.poison.clear();\n   621:     }\n   622: \n   623:     /// Consumes this `RwLock`, returning the underlying data.\n   624:     ///\n   625:     /// # Errors\n   626:     ///\n   627:     /// This function will return an error containing the underlying data if\n   628:     /// the `RwLock` is poisoned. An `RwLock` is poisoned whenever a writer\n   629:     /// panics while holding an exclusive lock. An error will only be returned",
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
