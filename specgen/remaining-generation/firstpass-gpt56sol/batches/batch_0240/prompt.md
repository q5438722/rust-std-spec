For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::Once::is_completed",
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
      "name": "is_completed",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   256:     ///\n   257:     /// ```\n   258:     /// use std::sync::Once;\n   259:     /// use std::thread;\n   260:     ///\n   261:     /// static INIT: Once = Once::new();\n   262:     ///\n   263:     /// assert_eq!(INIT.is_completed(), false);\n   264:     /// let handle = thread::spawn(|| {\n   265:     ///     INIT.call_once(|| panic!());\n   266:     /// });\n   267:     /// assert!(handle.join().is_err());\n   268:     /// assert_eq!(INIT.is_completed(), false);\n   269:     /// ```\n   270:     #[stable(feature = \"once_is_completed\", since = \"1.43.0\")]\n   271:     #[inline]\n   272:     pub fn is_completed(&self) -> bool {\n   273:         self.inner.is_completed()\n   274:     }\n   275: \n   276:     /// Blocks the current thread until initialization has completed.\n   277:     ///\n   278:     /// # Example\n   279:     ///\n   280:     /// ```rust\n   281:     /// use std::sync::Once;\n   282:     /// use std::thread;\n   283:     ///\n   284:     /// static READY: Once = Once::new();\n   285:     ///\n   286:     /// let thread = thread::spawn(|| {\n   287:     ///     READY.wait();\n   288:     ///     println!(\"everything is ready\");",
    "nanvix_source": "   262:     ///\n   263:     /// assert_eq!(INIT.is_completed(), false);\n   264:     /// let handle = thread::spawn(|| {\n   265:     ///     INIT.call_once(|| panic!());\n   266:     /// });\n   267:     /// assert!(handle.join().is_err());\n   268:     /// assert_eq!(INIT.is_completed(), false);\n   269:     /// ```\n   270:     #[stable(feature = \"once_is_completed\", since = \"1.43.0\")]\n   271:     #[inline]\n   272:     pub fn is_completed(&self) -> bool {\n   273:         self.inner.is_completed()\n   274:     }\n   275: \n   276:     /// Blocks the current thread until initialization has completed.\n   277:     ///\n   278:     /// # Example\n   279:     ///\n   280:     /// ```rust\n   281:     /// use std::sync::Once;\n   282:     /// use std::thread;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Once::new",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 8273,
            "path": "Once"
          }
        }
      }
    },
    "verification_source": "    67: /// static START: Once = ONCE_INIT;\n    68: /// ```\n    69: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    70: #[deprecated(\n    71:     since = \"1.38.0\",\n    72:     note = \"the `Once::new()` function is now preferred\",\n    73:     suggestion = \"Once::new()\"\n    74: )]\n    75: pub const ONCE_INIT: Once = Once::new();\n    76: \n    77: impl Once {\n    78:     /// Creates a new `Once` value.\n    79:     #[inline]\n    80:     #[stable(feature = \"once_new\", since = \"1.2.0\")]\n    81:     #[rustc_const_stable(feature = \"const_once_new\", since = \"1.32.0\")]\n    82:     #[must_use]\n    83:     pub const fn new() -> Once {\n    84:         Once { inner: sys::Once::new() }\n    85:     }\n    86: \n    87:     /// Creates a new `Once` value that starts already completed.\n    88:     #[inline]\n    89:     #[must_use]\n    90:     pub(crate) const fn new_complete() -> Once {\n    91:         Once { inner: sys::Once::new_complete() }\n    92:     }\n    93: \n    94:     /// Performs an initialization routine once and only once. The given closure\n    95:     /// will be executed if this is the first time `call_once` has been called,\n    96:     /// and otherwise the routine will *not* be invoked.\n    97:     ///\n    98:     /// This method will block the calling thread if another initialization\n    99:     /// routine is currently running.",
    "nanvix_source": "    73:     suggestion = \"Once::new()\"\n    74: )]\n    75: pub const ONCE_INIT: Once = Once::new();\n    76: \n    77: impl Once {\n    78:     /// Creates a new `Once` value.\n    79:     #[inline]\n    80:     #[stable(feature = \"once_new\", since = \"1.2.0\")]\n    81:     #[rustc_const_stable(feature = \"const_once_new\", since = \"1.32.0\")]\n    82:     #[must_use]\n    83:     pub const fn new() -> Once {\n    84:         Once { inner: sys::Once::new() }\n    85:     }\n    86: \n    87:     /// Creates a new `Once` value that starts already completed.\n    88:     #[inline]\n    89:     #[must_use]\n    90:     pub(crate) const fn new_complete() -> Once {\n    91:         Once { inner: sys::Once::new_complete() }\n    92:     }\n    93: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Once::wait",
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
      "name": "wait",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   285:     ///\n   286:     /// let thread = thread::spawn(|| {\n   287:     ///     READY.wait();\n   288:     ///     println!(\"everything is ready\");\n   289:     /// });\n   290:     ///\n   291:     /// READY.call_once(|| println!(\"performing setup\"));\n   292:     /// ```\n   293:     ///\n   294:     /// # Panics\n   295:     ///\n   296:     /// If this [`Once`] has been poisoned because an initialization closure has\n   297:     /// panicked, this method will also panic. Use [`wait_force`](Self::wait_force)\n   298:     /// if this behavior is not desired.\n   299:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   300:     #[rustc_should_not_be_called_on_const_items]\n   301:     pub fn wait(&self) {\n   302:         if !self.inner.is_completed() {\n   303:             self.inner.wait(false);\n   304:         }\n   305:     }\n   306: \n   307:     /// Blocks the current thread until initialization has completed, ignoring\n   308:     /// poisoning.\n   309:     ///\n   310:     /// If this [`Once`] has been poisoned, this function blocks until it\n   311:     /// becomes completed, unlike [`Once::wait()`], which panics in this case.\n   312:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   313:     #[rustc_should_not_be_called_on_const_items]\n   314:     pub fn wait_force(&self) {\n   315:         if !self.inner.is_completed() {\n   316:             self.inner.wait(true);\n   317:         }",
    "nanvix_source": "   291:     /// READY.call_once(|| println!(\"performing setup\"));\n   292:     /// ```\n   293:     ///\n   294:     /// # Panics\n   295:     ///\n   296:     /// If this [`Once`] has been poisoned because an initialization closure has\n   297:     /// panicked, this method will also panic. Use [`wait_force`](Self::wait_force)\n   298:     /// if this behavior is not desired.\n   299:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   300:     #[rustc_should_not_be_called_on_const_items]\n   301:     pub fn wait(&self) {\n   302:         if !self.inner.is_completed() {\n   303:             self.inner.wait(false);\n   304:         }\n   305:     }\n   306: \n   307:     /// Blocks the current thread until initialization has completed, ignoring\n   308:     /// poisoning.\n   309:     ///\n   310:     /// If this [`Once`] has been poisoned, this function blocks until it\n   311:     /// becomes completed, unlike [`Once::wait()`], which panics in this case.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Once::wait_force",
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
      "name": "wait_force",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   298:     /// if this behavior is not desired.\n   299:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   300:     #[rustc_should_not_be_called_on_const_items]\n   301:     pub fn wait(&self) {\n   302:         if !self.inner.is_completed() {\n   303:             self.inner.wait(false);\n   304:         }\n   305:     }\n   306: \n   307:     /// Blocks the current thread until initialization has completed, ignoring\n   308:     /// poisoning.\n   309:     ///\n   310:     /// If this [`Once`] has been poisoned, this function blocks until it\n   311:     /// becomes completed, unlike [`Once::wait()`], which panics in this case.\n   312:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   313:     #[rustc_should_not_be_called_on_const_items]\n   314:     pub fn wait_force(&self) {\n   315:         if !self.inner.is_completed() {\n   316:             self.inner.wait(true);\n   317:         }\n   318:     }\n   319: \n   320:     /// Returns the current state of the `Once` instance.\n   321:     ///\n   322:     /// Since this takes a mutable reference, no initialization can currently\n   323:     /// be running, so the state must be either \"incomplete\", \"poisoned\" or\n   324:     /// \"complete\".\n   325:     #[inline]\n   326:     pub(crate) fn state(&mut self) -> OnceExclusiveState {\n   327:         self.inner.state()\n   328:     }\n   329: \n   330:     /// Sets current state of the `Once` instance.",
    "nanvix_source": "   304:         }\n   305:     }\n   306: \n   307:     /// Blocks the current thread until initialization has completed, ignoring\n   308:     /// poisoning.\n   309:     ///\n   310:     /// If this [`Once`] has been poisoned, this function blocks until it\n   311:     /// becomes completed, unlike [`Once::wait()`], which panics in this case.\n   312:     #[stable(feature = \"once_wait\", since = \"1.86.0\")]\n   313:     #[rustc_should_not_be_called_on_const_items]\n   314:     pub fn wait_force(&self) {\n   315:         if !self.inner.is_completed() {\n   316:             self.inner.wait(true);\n   317:         }\n   318:     }\n   319: \n   320:     /// Returns the current state of the `Once` instance.\n   321:     ///\n   322:     /// Since this takes a mutable reference, no initialization can currently\n   323:     /// be running, so the state must be either \"incomplete\", \"poisoned\" or\n   324:     /// \"complete\".",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::get",
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
    "verification_source": "   139:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n   140:     pub const fn new() -> OnceLock<T> {\n   141:         OnceLock {\n   142:             once: Once::new(),\n   143:             value: UnsafeCell::new(MaybeUninit::uninit()),\n   144:             _marker: PhantomData,\n   145:         }\n   146:     }\n   147: \n   148:     /// Gets the reference to the underlying value.\n   149:     ///\n   150:     /// Returns `None` if the cell is uninitialized, or being initialized.\n   151:     /// This method never blocks.\n   152:     #[inline]\n   153:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   154:     #[rustc_should_not_be_called_on_const_items]\n   155:     pub fn get(&self) -> Option<&T> {\n   156:         if self.initialized() {\n   157:             // Safe b/c checked initialized\n   158:             Some(unsafe { self.get_unchecked() })\n   159:         } else {\n   160:             None\n   161:         }\n   162:     }\n   163: \n   164:     /// Gets the mutable reference to the underlying value.\n   165:     ///\n   166:     /// Returns `None` if the cell is uninitialized.\n   167:     ///\n   168:     /// This method never blocks. Since it borrows the `OnceLock` mutably,\n   169:     /// it is statically guaranteed that no active borrows to the `OnceLock`\n   170:     /// exist, including from other threads.\n   171:     #[inline]",
    "nanvix_source": "   145:         }\n   146:     }\n   147: \n   148:     /// Gets the reference to the underlying value.\n   149:     ///\n   150:     /// Returns `None` if the cell is uninitialized, or being initialized.\n   151:     /// This method never blocks.\n   152:     #[inline]\n   153:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   154:     #[rustc_should_not_be_called_on_const_items]\n   155:     pub fn get(&self) -> Option<&T> {\n   156:         if self.initialized() {\n   157:             // Safe b/c checked initialized\n   158:             Some(unsafe { self.get_unchecked() })\n   159:         } else {\n   160:             None\n   161:         }\n   162:     }\n   163: \n   164:     /// Gets the mutable reference to the underlying value.\n   165:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::OnceLock::get_mut",
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
    "verification_source": "   157:             // Safe b/c checked initialized\n   158:             Some(unsafe { self.get_unchecked() })\n   159:         } else {\n   160:             None\n   161:         }\n   162:     }\n   163: \n   164:     /// Gets the mutable reference to the underlying value.\n   165:     ///\n   166:     /// Returns `None` if the cell is uninitialized.\n   167:     ///\n   168:     /// This method never blocks. Since it borrows the `OnceLock` mutably,\n   169:     /// it is statically guaranteed that no active borrows to the `OnceLock`\n   170:     /// exist, including from other threads.\n   171:     #[inline]\n   172:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   173:     pub fn get_mut(&mut self) -> Option<&mut T> {\n   174:         if self.initialized_mut() {\n   175:             // Safe b/c checked initialized and we have a unique access\n   176:             Some(unsafe { self.get_unchecked_mut() })\n   177:         } else {\n   178:             None\n   179:         }\n   180:     }\n   181: \n   182:     /// Blocks the current thread until the cell is initialized.\n   183:     ///\n   184:     /// # Example\n   185:     ///\n   186:     /// Waiting for a computation on another thread to finish:\n   187:     /// ```rust\n   188:     /// use std::thread;\n   189:     /// use std::sync::OnceLock;",
    "nanvix_source": "   163: \n   164:     /// Gets the mutable reference to the underlying value.\n   165:     ///\n   166:     /// Returns `None` if the cell is uninitialized.\n   167:     ///\n   168:     /// This method never blocks. Since it borrows the `OnceLock` mutably,\n   169:     /// it is statically guaranteed that no active borrows to the `OnceLock`\n   170:     /// exist, including from other threads.\n   171:     #[inline]\n   172:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   173:     pub fn get_mut(&mut self) -> Option<&mut T> {\n   174:         if self.initialized_mut() {\n   175:             // Safe b/c checked initialized and we have a unique access\n   176:             Some(unsafe { self.get_unchecked_mut() })\n   177:         } else {\n   178:             None\n   179:         }\n   180:     }\n   181: \n   182:     /// Blocks the current thread until the cell is initialized.\n   183:     ///",
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
