For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::park",
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
      "name": "park",
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
    "verification_source": "   513: /// // happens first, `park` will return immediately.\n   514: /// // There is also no other `park` that could consume this token,\n   515: /// // since we waited until the other thread got queued.\n   516: /// // Hence there is no risk of a deadlock.\n   517: /// FLAG.store(true, Ordering::Release);\n   518: /// println!(\"Unpark the thread\");\n   519: /// parked_thread.thread().unpark();\n   520: ///\n   521: /// parked_thread.join().unwrap();\n   522: /// ```\n   523: ///\n   524: /// [`Thread`]: super::Thread\n   525: /// [`unpark`]: super::Thread::unpark\n   526: /// [`thread::park_timeout`]: park_timeout\n   527: /// [release sequence]: https://en.cppreference.com/w/cpp/atomic/memory_order#Release_sequence\n   528: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   529: pub fn park() {\n   530:     let guard = PanicGuard;\n   531:     // SAFETY: park_timeout is called on the parker owned by this thread.\n   532:     unsafe {\n   533:         current().park();\n   534:     }\n   535:     // No panic occurred, do not abort.\n   536:     forget(guard);\n   537: }\n   538: \n   539: /// Uses [`park_timeout`].\n   540: ///\n   541: /// Blocks unless or until the current thread's token is made available or\n   542: /// the specified duration has been reached (may wake spuriously).\n   543: ///\n   544: /// The semantics of this function are equivalent to [`park`] except\n   545: /// that the thread will be blocked for roughly no longer than `dur`. This",
    "nanvix_source": "   519: /// parked_thread.thread().unpark();\n   520: ///\n   521: /// parked_thread.join().unwrap();\n   522: /// ```\n   523: ///\n   524: /// [`Thread`]: super::Thread\n   525: /// [`unpark`]: super::Thread::unpark\n   526: /// [`thread::park_timeout`]: park_timeout\n   527: /// [release sequence]: https://en.cppreference.com/w/cpp/atomic/memory_order#Release_sequence\n   528: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   529: pub fn park() {\n   530:     let guard = PanicGuard;\n   531:     // SAFETY: park_timeout is called on the parker owned by this thread.\n   532:     unsafe {\n   533:         current().park();\n   534:     }\n   535:     // No panic occurred, do not abort.\n   536:     forget(guard);\n   537: }\n   538: \n   539: /// Uses [`park_timeout`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::park_timeout",
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
      "name": "park_timeout",
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
        "inputs": [
          [
            "dur",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "crate::time::Duration"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   580: ///\n   581: /// let timeout = Duration::from_secs(2);\n   582: /// let beginning_park = Instant::now();\n   583: ///\n   584: /// let mut timeout_remaining = timeout;\n   585: /// loop {\n   586: ///     park_timeout(timeout_remaining);\n   587: ///     let elapsed = beginning_park.elapsed();\n   588: ///     if elapsed >= timeout {\n   589: ///         break;\n   590: ///     }\n   591: ///     println!(\"restarting park_timeout after {elapsed:?}\");\n   592: ///     timeout_remaining = timeout - elapsed;\n   593: /// }\n   594: /// ```\n   595: #[stable(feature = \"park_timeout\", since = \"1.4.0\")]\n   596: pub fn park_timeout(dur: Duration) {\n   597:     let guard = PanicGuard;\n   598:     // SAFETY: park_timeout is called on a handle owned by this thread.\n   599:     unsafe {\n   600:         current().park_timeout(dur);\n   601:     }\n   602:     // No panic occurred, do not abort.\n   603:     forget(guard);\n   604: }\n   605: \n   606: /// Returns an estimate of the default amount of parallelism a program should use.\n   607: ///\n   608: /// Parallelism is a resource. A given machine provides a certain capacity for\n   609: /// parallelism, i.e., a bound on the number of computations it can perform\n   610: /// simultaneously. This number often corresponds to the amount of CPUs a\n   611: /// computer has, but it may diverge in various cases.\n   612: ///",
    "nanvix_source": "   586: ///     park_timeout(timeout_remaining);\n   587: ///     let elapsed = beginning_park.elapsed();\n   588: ///     if elapsed >= timeout {\n   589: ///         break;\n   590: ///     }\n   591: ///     println!(\"restarting park_timeout after {elapsed:?}\");\n   592: ///     timeout_remaining = timeout - elapsed;\n   593: /// }\n   594: /// ```\n   595: #[stable(feature = \"park_timeout\", since = \"1.4.0\")]\n   596: pub fn park_timeout(dur: Duration) {\n   597:     let guard = PanicGuard;\n   598:     // SAFETY: park_timeout is called on a handle owned by this thread.\n   599:     unsafe {\n   600:         current().park_timeout(dur);\n   601:     }\n   602:     // No panic occurred, do not abort.\n   603:     forget(guard);\n   604: }\n   605: \n   606: /// Returns an estimate of the default amount of parallelism a program should use.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::park_timeout_ms",
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
      "name": "park_timeout_ms",
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
        "inputs": [
          [
            "ms",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   537: }\n   538: \n   539: /// Uses [`park_timeout`].\n   540: ///\n   541: /// Blocks unless or until the current thread's token is made available or\n   542: /// the specified duration has been reached (may wake spuriously).\n   543: ///\n   544: /// The semantics of this function are equivalent to [`park`] except\n   545: /// that the thread will be blocked for roughly no longer than `dur`. This\n   546: /// method should not be used for precise timing due to anomalies such as\n   547: /// preemption or platform differences that might not cause the maximum\n   548: /// amount of time waited to be precisely `ms` long.\n   549: ///\n   550: /// See the [park documentation][`park`] for more detail.\n   551: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   552: #[deprecated(since = \"1.6.0\", note = \"replaced by `std::thread::park_timeout`\")]\n   553: pub fn park_timeout_ms(ms: u32) {\n   554:     park_timeout(Duration::from_millis(ms as u64))\n   555: }\n   556: \n   557: /// Blocks unless or until the current thread's token is made available or\n   558: /// the specified duration has been reached (may wake spuriously).\n   559: ///\n   560: /// The semantics of this function are equivalent to [`park`][park] except\n   561: /// that the thread will be blocked for roughly no longer than `dur`. This\n   562: /// method should not be used for precise timing due to anomalies such as\n   563: /// preemption or platform differences that might not cause the maximum\n   564: /// amount of time waited to be precisely `dur` long.\n   565: ///\n   566: /// See the [park documentation][park] for more details.\n   567: ///\n   568: /// # Platform-specific behavior\n   569: ///",
    "nanvix_source": "   543: ///\n   544: /// The semantics of this function are equivalent to [`park`] except\n   545: /// that the thread will be blocked for roughly no longer than `dur`. This\n   546: /// method should not be used for precise timing due to anomalies such as\n   547: /// preemption or platform differences that might not cause the maximum\n   548: /// amount of time waited to be precisely `ms` long.\n   549: ///\n   550: /// See the [park documentation][`park`] for more detail.\n   551: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   552: #[deprecated(since = \"1.6.0\", note = \"replaced by `std::thread::park_timeout`\")]\n   553: pub fn park_timeout_ms(ms: u32) {\n   554:     park_timeout(Duration::from_millis(ms as u64))\n   555: }\n   556: \n   557: /// Blocks unless or until the current thread's token is made available or\n   558: /// the specified duration has been reached (may wake spuriously).\n   559: ///\n   560: /// The semantics of this function are equivalent to [`park`][park] except\n   561: /// that the thread will be blocked for roughly no longer than `dur`. This\n   562: /// method should not be used for precise timing due to anomalies such as\n   563: /// preemption or platform differences that might not cause the maximum",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::scope",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'env"
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
                    "generic_params": [
                      {
                        "kind": {
                          "lifetime": {
                            "outlives": []
                          }
                        },
                        "name": "'scope"
                      }
                    ],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": "'scope",
                                "type": {
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
                                }
                              }
                            }
                          ],
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
      "name": "scope",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   125: ///\n   126: /// The `'scope` lifetime represents the lifetime of the scope itself.\n   127: /// That is: the time during which new scoped threads may be spawned,\n   128: /// and also the time during which they might still be running.\n   129: /// Once this lifetime ends, all scoped threads are joined.\n   130: /// This lifetime starts within the `scope` function, before `f` (the argument to `scope`) starts.\n   131: /// It ends after `f` returns and all scoped threads have been joined, but before `scope` returns.\n   132: ///\n   133: /// The `'env` lifetime represents the lifetime of whatever is borrowed by the scoped threads.\n   134: /// This lifetime must outlast the call to `scope`, and thus cannot be smaller than `'scope`.\n   135: /// It can be as small as the call to `scope`, meaning that anything that outlives this call,\n   136: /// such as local variables defined right before the scope, can be borrowed by the scoped threads.\n   137: ///\n   138: /// The `'env: 'scope` bound is part of the definition of the `Scope` type.\n   139: #[track_caller]\n   140: #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   141: pub fn scope<'env, F, T>(f: F) -> T\n   142: where\n   143:     F: for<'scope> FnOnce(&'scope Scope<'scope, 'env>) -> T,\n   144: {\n   145:     // We put the `ScopeData` into an `Arc` so that other threads can finish their\n   146:     // `decrement_num_running_threads` even after this function returns.\n   147:     let scope = Scope {\n   148:         data: Arc::new(ScopeData {\n   149:             num_running_threads: AtomicUsize::new(0),\n   150:             main_thread: current_or_unnamed(),\n   151:             a_thread_panicked: AtomicBool::new(false),\n   152:         }),\n   153:         env: PhantomData,\n   154:         scope: PhantomData,\n   155:     };\n   156: \n   157:     // Run `f`, but catch panics so we can make sure to wait for all the threads to join.",
    "nanvix_source": "   131: /// It ends after `f` returns and all scoped threads have been joined, but before `scope` returns.\n   132: ///\n   133: /// The `'env` lifetime represents the lifetime of whatever is borrowed by the scoped threads.\n   134: /// This lifetime must outlast the call to `scope`, and thus cannot be smaller than `'scope`.\n   135: /// It can be as small as the call to `scope`, meaning that anything that outlives this call,\n   136: /// such as local variables defined right before the scope, can be borrowed by the scoped threads.\n   137: ///\n   138: /// The `'env: 'scope` bound is part of the definition of the `Scope` type.\n   139: #[track_caller]\n   140: #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   141: pub fn scope<'env, F, T>(f: F) -> T\n   142: where\n   143:     F: for<'scope> FnOnce(&'scope Scope<'scope, 'env>) -> T,\n   144: {\n   145:     // We put the `ScopeData` into an `Arc` so that other threads can finish their\n   146:     // `decrement_num_running_threads` even after this function returns.\n   147:     let scope = Scope {\n   148:         data: Arc::new(ScopeData {\n   149:             num_running_threads: AtomicUsize::new(0),\n   150:             main_thread: current_or_unnamed(),\n   151:             a_thread_panicked: AtomicBool::new(false),",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::sleep",
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
      "name": "sleep",
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
        "inputs": [
          [
            "dur",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "crate::time::Duration"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   276: /// [`nanosleep`]: https://linux.die.net/man/2/nanosleep\n   277: /// [`Sleep`]: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleep\n   278: ///\n   279: /// # Examples\n   280: ///\n   281: /// ```no_run\n   282: /// use std::{thread, time};\n   283: ///\n   284: /// let ten_millis = time::Duration::from_millis(10);\n   285: /// let now = time::Instant::now();\n   286: ///\n   287: /// thread::sleep(ten_millis);\n   288: ///\n   289: /// assert!(now.elapsed() >= ten_millis);\n   290: /// ```\n   291: #[stable(feature = \"thread_sleep\", since = \"1.4.0\")]\n   292: pub fn sleep(dur: Duration) {\n   293:     imp::sleep(dur)\n   294: }\n   295: \n   296: /// Puts the current thread to sleep until the specified deadline has passed.\n   297: ///\n   298: /// The thread may still be asleep after the deadline specified due to\n   299: /// scheduling specifics or platform-dependent functionality. It will never\n   300: /// wake before.\n   301: ///\n   302: /// This function is blocking, and should not be used in `async` functions.\n   303: ///\n   304: /// # Platform-specific behavior\n   305: ///\n   306: /// In most cases this function will call an OS specific function. Where that\n   307: /// is not supported [`sleep`] is used. Those platforms are referred to as other\n   308: /// in the table below.",
    "nanvix_source": "   282: /// use std::{thread, time};\n   283: ///\n   284: /// let ten_millis = time::Duration::from_millis(10);\n   285: /// let now = time::Instant::now();\n   286: ///\n   287: /// thread::sleep(ten_millis);\n   288: ///\n   289: /// assert!(now.elapsed() >= ten_millis);\n   290: /// ```\n   291: #[stable(feature = \"thread_sleep\", since = \"1.4.0\")]\n   292: pub fn sleep(dur: Duration) {\n   293:     imp::sleep(dur)\n   294: }\n   295: \n   296: /// Puts the current thread to sleep until the specified deadline has passed.\n   297: ///\n   298: /// The thread may still be asleep after the deadline specified due to\n   299: /// scheduling specifics or platform-dependent functionality. It will never\n   300: /// wake before.\n   301: ///\n   302: /// This function is blocking, and should not be used in `async` functions.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::sleep_ms",
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
      "name": "sleep_ms",
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
        "inputs": [
          [
            "ms",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   234: ///\n   235: /// On Unix platforms, the underlying syscall may be interrupted by a\n   236: /// spurious wakeup or signal handler. To ensure the sleep occurs for at least\n   237: /// the specified duration, this function may invoke that system call multiple\n   238: /// times.\n   239: ///\n   240: /// # Examples\n   241: ///\n   242: /// ```no_run\n   243: /// use std::thread;\n   244: ///\n   245: /// // Let's sleep for 2 seconds:\n   246: /// thread::sleep_ms(2000);\n   247: /// ```\n   248: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   249: #[deprecated(since = \"1.6.0\", note = \"replaced by `std::thread::sleep`\")]\n   250: pub fn sleep_ms(ms: u32) {\n   251:     sleep(Duration::from_millis(ms as u64))\n   252: }\n   253: \n   254: /// Puts the current thread to sleep for at least the specified amount of time.\n   255: ///\n   256: /// The thread may sleep longer than the duration specified due to scheduling\n   257: /// specifics or platform-dependent functionality. It will never sleep less.\n   258: ///\n   259: /// This function is blocking, and should not be used in `async` functions.\n   260: ///\n   261: /// # Platform-specific behavior\n   262: ///\n   263: /// On Unix platforms, the underlying syscall may be interrupted by a\n   264: /// spurious wakeup or signal handler. To ensure the sleep occurs for at least\n   265: /// the specified duration, this function may invoke that system call multiple\n   266: /// times.",
    "nanvix_source": "   240: /// # Examples\n   241: ///\n   242: /// ```no_run\n   243: /// use std::thread;\n   244: ///\n   245: /// // Let's sleep for 2 seconds:\n   246: /// thread::sleep_ms(2000);\n   247: /// ```\n   248: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   249: #[deprecated(since = \"1.6.0\", note = \"replaced by `std::thread::sleep`\")]\n   250: pub fn sleep_ms(ms: u32) {\n   251:     sleep(Duration::from_millis(ms as u64))\n   252: }\n   253: \n   254: /// Puts the current thread to sleep for at least the specified amount of time.\n   255: ///\n   256: /// The thread may sleep longer than the duration specified due to scheduling\n   257: /// specifics or platform-dependent functionality. It will never sleep less.\n   258: ///\n   259: /// This function is blocking, and should not be used in `async` functions.\n   260: ///",
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
