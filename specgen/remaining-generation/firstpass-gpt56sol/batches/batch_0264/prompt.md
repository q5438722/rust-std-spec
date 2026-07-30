For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::spawn",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
                  "outlives": "'static"
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
                  "outlives": "'static"
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
      "owner": null,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 475,
            "path": "super::join_handle::JoinHandle"
          }
        }
      }
    },
    "verification_source": "   109: /// This function has the same minimal guarantee regarding \"foreign\" unwinding operations (e.g.\n   110: /// an exception thrown from C++ code, or a `panic!` in Rust code compiled or linked with a\n   111: /// different runtime) as [`catch_unwind`]; namely, if the thread created with `thread::spawn`\n   112: /// unwinds all the way to the root with such an exception, one of two behaviors are possible,\n   113: /// and it is unspecified which will occur:\n   114: ///\n   115: /// * The process aborts.\n   116: /// * The process does not abort, and [`join`] will return a `Result::Err`\n   117: ///   containing an opaque type.\n   118: ///\n   119: /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   120: /// [`channels`]: crate::sync::mpsc\n   121: /// [`join`]: JoinHandle::join\n   122: /// [`Err`]: crate::result::Result::Err\n   123: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   125: pub fn spawn<F, T>(f: F) -> JoinHandle<T>\n   126: where\n   127:     F: FnOnce() -> T,\n   128:     F: Send + 'static,\n   129:     T: Send + 'static,\n   130: {\n   131:     Builder::new().spawn(f).expect(\"failed to spawn thread\")\n   132: }\n   133: \n   134: /// Cooperatively gives up a timeslice to the OS scheduler.\n   135: ///\n   136: /// This calls the underlying OS scheduler's yield primitive, signaling\n   137: /// that the calling thread is willing to give up its remaining timeslice\n   138: /// so that the OS may schedule other threads on the CPU.\n   139: ///\n   140: /// A drawback of yielding in a loop is that if the OS does not have any\n   141: /// other ready threads to run on the current CPU, the thread will effectively",
    "nanvix_source": "   115: /// * The process aborts.\n   116: /// * The process does not abort, and [`join`] will return a `Result::Err`\n   117: ///   containing an opaque type.\n   118: ///\n   119: /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   120: /// [`channels`]: crate::sync::mpsc\n   121: /// [`join`]: JoinHandle::join\n   122: /// [`Err`]: crate::result::Result::Err\n   123: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   125: pub fn spawn<F, T>(f: F) -> JoinHandle<T>\n   126: where\n   127:     F: FnOnce() -> T,\n   128:     F: Send + 'static,\n   129:     T: Send + 'static,\n   130: {\n   131:     Builder::new().spawn(f).expect(\"failed to spawn thread\")\n   132: }\n   133: \n   134: /// Cooperatively gives up a timeslice to the OS scheduler.\n   135: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::yield_now",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
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
      "name": "yield_now",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   151: /// repeated polling is required because there is no other suitable way to\n   152: /// learn when an event of interest has occurred.\n   153: ///\n   154: /// # Examples\n   155: ///\n   156: /// ```\n   157: /// use std::thread;\n   158: ///\n   159: /// thread::yield_now();\n   160: /// ```\n   161: ///\n   162: /// [`channel`]: crate::sync::mpsc\n   163: /// [`join`]: JoinHandle::join\n   164: /// [`Condvar`]: crate::sync::Condvar\n   165: /// [`Mutex`]: crate::sync::Mutex\n   166: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   167: pub fn yield_now() {\n   168:     imp::yield_now()\n   169: }\n   170: \n   171: /// Determines whether the current thread is panicking.\n   172: ///\n   173: /// This returns `true` both when the thread is unwinding due to a panic,\n   174: /// or executing a panic hook. Note that the latter case will still happen\n   175: /// when `panic=abort` is set.\n   176: ///\n   177: /// A common use of this feature is to poison shared resources when writing\n   178: /// unsafe code, by checking `panicking` when the `drop` is called.\n   179: ///\n   180: /// This is usually not needed when writing safe code, as [`Mutex`es][Mutex]\n   181: /// already poison themselves when a thread panics while holding the lock.\n   182: ///\n   183: /// This can also be used in multithreaded applications, in order to send a",
    "nanvix_source": "   157: /// use std::thread;\n   158: ///\n   159: /// thread::yield_now();\n   160: /// ```\n   161: ///\n   162: /// [`channel`]: crate::sync::mpsc\n   163: /// [`join`]: JoinHandle::join\n   164: /// [`Condvar`]: crate::sync::Condvar\n   165: /// [`Mutex`]: crate::sync::Mutex\n   166: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   167: pub fn yield_now() {\n   168:     imp::yield_now()\n   169: }\n   170: \n   171: /// Determines whether the current thread is panicking.\n   172: ///\n   173: /// This returns `true` both when the thread is unwinding due to a panic,\n   174: /// or executing a panic hook. Note that the latter case will still happen\n   175: /// when `panic=abort` is set.\n   176: ///\n   177: /// A common use of this feature is to poison shared resources when writing",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::checked_add",
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
      "name": "checked_add",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "duration",
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
                      "resolved_path": {
                        "args": null,
                        "id": 516,
                        "path": "Instant"
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
    "verification_source": "   382:     ///\n   383:     /// let instant = Instant::now();\n   384:     /// let three_secs = Duration::from_secs(3);\n   385:     /// sleep(three_secs);\n   386:     /// assert!(instant.elapsed() >= three_secs);\n   387:     /// ```\n   388:     #[must_use]\n   389:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   390:     pub fn elapsed(&self) -> Duration {\n   391:         Instant::now() - *self\n   392:     }\n   393: \n   394:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   395:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   396:     /// otherwise.\n   397:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   398:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   399:         self.0.checked_add_duration(&duration).map(Instant)\n   400:     }\n   401: \n   402:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   403:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   404:     /// otherwise.\n   405:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   406:     pub fn checked_sub(&self, duration: Duration) -> Option<Instant> {\n   407:         self.0.checked_sub_duration(&duration).map(Instant)\n   408:     }\n   409: \n   410:     // Used by platform specific `sleep_until` implementations such as the one used on Linux.\n   411:     #[cfg_attr(\n   412:         not(target_os = \"linux\"),\n   413:         allow(unused, reason = \"not every platform has a specific `sleep_until`\")\n   414:     )]",
    "nanvix_source": "   386:     #[must_use]\n   387:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   388:     pub fn elapsed(&self) -> Duration {\n   389:         Instant::now() - *self\n   390:     }\n   391: \n   392:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   393:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   394:     /// otherwise.\n   395:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   396:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   397:         self.0.checked_add_duration(&duration).map(Instant)\n   398:     }\n   399: \n   400:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   401:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   402:     /// otherwise.\n   403:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   404:     pub fn checked_sub(&self, duration: Duration) -> Option<Instant> {\n   405:         self.0.checked_sub_duration(&duration).map(Instant)\n   406:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::checked_duration_since",
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
      "name": "checked_duration_since",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "earlier",
            {
              "resolved_path": {
                "args": null,
                "id": 516,
                "path": "Instant"
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
                        "args": null,
                        "id": 513,
                        "path": "Duration"
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
    "verification_source": "   326:     /// [monotonicity bugs]: Instant#monotonicity\n   327:     ///\n   328:     /// # Examples\n   329:     ///\n   330:     /// ```no_run\n   331:     /// use std::time::{Duration, Instant};\n   332:     /// use std::thread::sleep;\n   333:     ///\n   334:     /// let now = Instant::now();\n   335:     /// sleep(Duration::new(1, 0));\n   336:     /// let new_now = Instant::now();\n   337:     /// println!(\"{:?}\", new_now.checked_duration_since(now));\n   338:     /// println!(\"{:?}\", now.checked_duration_since(new_now)); // None\n   339:     /// ```\n   340:     #[must_use]\n   341:     #[stable(feature = \"checked_duration_since\", since = \"1.39.0\")]\n   342:     pub fn checked_duration_since(&self, earlier: Instant) -> Option<Duration> {\n   343:         self.0.checked_sub_instant(&earlier.0)\n   344:     }\n   345: \n   346:     /// Returns the amount of time elapsed from another instant to this one,\n   347:     /// or zero duration if that instant is later than this one.\n   348:     ///\n   349:     /// # Examples\n   350:     ///\n   351:     /// ```no_run\n   352:     /// use std::time::{Duration, Instant};\n   353:     /// use std::thread::sleep;\n   354:     ///\n   355:     /// let now = Instant::now();\n   356:     /// sleep(Duration::new(1, 0));\n   357:     /// let new_now = Instant::now();\n   358:     /// println!(\"{:?}\", new_now.saturating_duration_since(now));",
    "nanvix_source": "   330:     /// use std::thread::sleep;\n   331:     ///\n   332:     /// let now = Instant::now();\n   333:     /// sleep(Duration::new(1, 0));\n   334:     /// let new_now = Instant::now();\n   335:     /// println!(\"{:?}\", new_now.checked_duration_since(now));\n   336:     /// println!(\"{:?}\", now.checked_duration_since(new_now)); // None\n   337:     /// ```\n   338:     #[must_use]\n   339:     #[stable(feature = \"checked_duration_since\", since = \"1.39.0\")]\n   340:     pub fn checked_duration_since(&self, earlier: Instant) -> Option<Duration> {\n   341:         self.0.checked_sub_instant(&earlier.0)\n   342:     }\n   343: \n   344:     /// Returns the amount of time elapsed from another instant to this one,\n   345:     /// or zero duration if that instant is later than this one.\n   346:     ///\n   347:     /// # Examples\n   348:     ///\n   349:     /// ```no_run\n   350:     /// use std::time::{Duration, Instant};",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::checked_sub",
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
      "name": "checked_sub",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "duration",
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
                      "resolved_path": {
                        "args": null,
                        "id": 516,
                        "path": "Instant"
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
    "verification_source": "   390:     pub fn elapsed(&self) -> Duration {\n   391:         Instant::now() - *self\n   392:     }\n   393: \n   394:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   395:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   396:     /// otherwise.\n   397:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   398:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   399:         self.0.checked_add_duration(&duration).map(Instant)\n   400:     }\n   401: \n   402:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   403:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   404:     /// otherwise.\n   405:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   406:     pub fn checked_sub(&self, duration: Duration) -> Option<Instant> {\n   407:         self.0.checked_sub_duration(&duration).map(Instant)\n   408:     }\n   409: \n   410:     // Used by platform specific `sleep_until` implementations such as the one used on Linux.\n   411:     #[cfg_attr(\n   412:         not(target_os = \"linux\"),\n   413:         allow(unused, reason = \"not every platform has a specific `sleep_until`\")\n   414:     )]\n   415:     pub(crate) fn into_inner(self) -> time::Instant {\n   416:         self.0\n   417:     }\n   418: }\n   419: \n   420: #[stable(feature = \"time2\", since = \"1.8.0\")]\n   421: impl Add<Duration> for Instant {\n   422:     type Output = Instant;",
    "nanvix_source": "   394:     /// otherwise.\n   395:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   396:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   397:         self.0.checked_add_duration(&duration).map(Instant)\n   398:     }\n   399: \n   400:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   401:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   402:     /// otherwise.\n   403:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   404:     pub fn checked_sub(&self, duration: Duration) -> Option<Instant> {\n   405:         self.0.checked_sub_duration(&duration).map(Instant)\n   406:     }\n   407: \n   408:     // Used by platform specific `sleep_until` implementations such as the one used on Linux.\n   409:     #[cfg_attr(\n   410:         not(target_os = \"linux\"),\n   411:         allow(unused, reason = \"not every platform has a specific `sleep_until`\")\n   412:     )]\n   413:     pub(crate) fn into_inner(self) -> time::Instant {\n   414:         self.0",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::duration_since",
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
      "name": "duration_since",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "earlier",
            {
              "resolved_path": {
                "args": null,
                "id": 516,
                "path": "Instant"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 513,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   300:     /// [Monotonicity]: Instant#monotonicity\n   301:     ///\n   302:     /// # Examples\n   303:     ///\n   304:     /// ```no_run\n   305:     /// use std::time::{Duration, Instant};\n   306:     /// use std::thread::sleep;\n   307:     ///\n   308:     /// let now = Instant::now();\n   309:     /// sleep(Duration::new(1, 0));\n   310:     /// let new_now = Instant::now();\n   311:     /// println!(\"{:?}\", new_now.duration_since(now));\n   312:     /// println!(\"{:?}\", now.duration_since(new_now)); // 0ns\n   313:     /// ```\n   314:     #[must_use]\n   315:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   316:     pub fn duration_since(&self, earlier: Instant) -> Duration {\n   317:         self.checked_duration_since(earlier).unwrap_or_default()\n   318:     }\n   319: \n   320:     /// Returns the amount of time elapsed from another instant to this one,\n   321:     /// or None if that instant is later than this one.\n   322:     ///\n   323:     /// Due to [monotonicity bugs], even under correct logical ordering of the passed `Instant`s,\n   324:     /// this method can return `None`.\n   325:     ///\n   326:     /// [monotonicity bugs]: Instant#monotonicity\n   327:     ///\n   328:     /// # Examples\n   329:     ///\n   330:     /// ```no_run\n   331:     /// use std::time::{Duration, Instant};\n   332:     /// use std::thread::sleep;",
    "nanvix_source": "   304:     /// use std::thread::sleep;\n   305:     ///\n   306:     /// let now = Instant::now();\n   307:     /// sleep(Duration::new(1, 0));\n   308:     /// let new_now = Instant::now();\n   309:     /// println!(\"{:?}\", new_now.duration_since(now));\n   310:     /// println!(\"{:?}\", now.duration_since(new_now)); // 0ns\n   311:     /// ```\n   312:     #[must_use]\n   313:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   314:     pub fn duration_since(&self, earlier: Instant) -> Duration {\n   315:         self.checked_duration_since(earlier).unwrap_or_default()\n   316:     }\n   317: \n   318:     /// Returns the amount of time elapsed from another instant to this one,\n   319:     /// or None if that instant is later than this one.\n   320:     ///\n   321:     /// Due to [monotonicity bugs], even under correct logical ordering of the passed `Instant`s,\n   322:     /// this method can return `None`.\n   323:     ///\n   324:     /// [monotonicity bugs]: Instant#monotonicity",
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
