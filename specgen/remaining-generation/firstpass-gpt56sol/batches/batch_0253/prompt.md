For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::Builder::spawn_unchecked",
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
        "is_unsafe": true
      },
      "name": "spawn_unchecked",
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
            "id": 471,
            "path": "Builder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:477",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:471",
        "resolved_owner_path": [
          "std",
          "thread",
          "builder",
          "Builder"
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
                        "path": "JoinHandle"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "   220:     /// This can be guaranteed in two ways:\n   221:     ///\n   222:     /// - ensure that [`join`][`JoinHandle::join`] is called before any referenced\n   223:     /// data is dropped\n   224:     /// - use only types with `'static` lifetime bounds, i.e., those with no or only\n   225:     /// `'static` references (both [`thread::Builder::spawn`][`Builder::spawn`]\n   226:     /// and [`thread::spawn`] enforce this property statically)\n   227:     ///\n   228:     /// # Examples\n   229:     ///\n   230:     /// ```\n   231:     /// use std::thread;\n   232:     ///\n   233:     /// let builder = thread::Builder::new();\n   234:     ///\n   235:     /// let x = 1;\n   236:     /// let thread_x = &x;\n   237:     ///\n   238:     /// let handler = unsafe {\n   239:     ///     builder.spawn_unchecked(move || {\n   240:     ///         println!(\"x = {}\", *thread_x);\n   241:     ///     }).unwrap()\n   242:     /// };\n   243:     ///\n   244:     /// // caller has to ensure `join()` is called, otherwise\n   245:     /// // it is possible to access freed memory if `x` gets\n   246:     /// // dropped before the thread closure is executed!\n   247:     /// handler.join().unwrap();\n   248:     /// ```\n   249:     ///\n   250:     /// [`thread::spawn`]: super::spawn\n   251:     /// [`spawn`]: super::spawn\n   252:     #[stable(feature = \"thread_spawn_unchecked\", since = \"1.82.0\")]",
    "nanvix_source": "   226:     /// and [`thread::spawn`] enforce this property statically)\n   227:     ///\n   228:     /// # Examples\n   229:     ///\n   230:     /// ```\n   231:     /// use std::thread;\n   232:     ///\n   233:     /// let builder = thread::Builder::new();\n   234:     ///\n   235:     /// let x = 1;\n   236:     /// let thread_x = &x;\n   237:     ///\n   238:     /// let handler = unsafe {\n   239:     ///     builder.spawn_unchecked(move || {\n   240:     ///         println!(\"x = {}\", *thread_x);\n   241:     ///     }).unwrap()\n   242:     /// };\n   243:     ///\n   244:     /// // caller has to ensure `join()` is called, otherwise\n   245:     /// // it is possible to access freed memory if `x` gets\n   246:     /// // dropped before the thread closure is executed!",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Builder::stack_size",
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
      "name": "stack_size",
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
            "id": 471,
            "path": "Builder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:477",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:471",
        "resolved_owner_path": [
          "std",
          "thread",
          "builder",
          "Builder"
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
            "size",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 471,
            "path": "Builder"
          }
        }
      }
    },
    "verification_source": "   114:     /// The actual stack size may be greater than this value if\n   115:     /// the platform specifies a minimal stack size.\n   116:     ///\n   117:     /// For more information about the stack size for threads, see\n   118:     /// [this module-level documentation][stack-size].\n   119:     ///\n   120:     /// # Examples\n   121:     ///\n   122:     /// ```\n   123:     /// use std::thread;\n   124:     ///\n   125:     /// let builder = thread::Builder::new().stack_size(32 * 1024);\n   126:     /// ```\n   127:     ///\n   128:     /// [stack-size]: ./index.html#stack-size\n   129:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   130:     pub fn stack_size(mut self, size: usize) -> Builder {\n   131:         self.stack_size = Some(size);\n   132:         self\n   133:     }\n   134: \n   135:     /// Disables running and inheriting [spawn hooks].\n   136:     ///\n   137:     /// Use this if the parent thread is in no way relevant for the child thread.\n   138:     /// For example, when lazily spawning threads for a thread pool.\n   139:     ///\n   140:     /// [spawn hooks]: super::add_spawn_hook\n   141:     #[unstable(feature = \"thread_spawn_hook\", issue = \"132951\")]\n   142:     pub fn no_hooks(mut self) -> Builder {\n   143:         self.no_hooks = true;\n   144:         self\n   145:     }\n   146: ",
    "nanvix_source": "   120:     /// # Examples\n   121:     ///\n   122:     /// ```\n   123:     /// use std::thread;\n   124:     ///\n   125:     /// let builder = thread::Builder::new().stack_size(32 * 1024);\n   126:     /// ```\n   127:     ///\n   128:     /// [stack-size]: ./index.html#stack-size\n   129:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   130:     pub fn stack_size(mut self, size: usize) -> Builder {\n   131:         self.stack_size = Some(size);\n   132:         self\n   133:     }\n   134: \n   135:     /// Disables running and inheriting [spawn hooks].\n   136:     ///\n   137:     /// Use this if the parent thread is in no way relevant for the child thread.\n   138:     /// For example, when lazily spawning threads for a thread pool.\n   139:     ///\n   140:     /// [spawn hooks]: super::add_spawn_hook",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::JoinHandle::is_finished",
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
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 475,
            "path": "JoinHandle"
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
        "impl_id": "std:563",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:475",
        "resolved_owner_path": [
          "std",
          "thread",
          "join_handle",
          "JoinHandle"
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
    "verification_source": "   137:     /// # Notes\n   138:     ///\n   139:     /// If a \"foreign\" unwinding operation (e.g. an exception thrown from C++\n   140:     /// code, or a `panic!` in Rust code compiled or linked with a different\n   141:     /// runtime) unwinds all the way to the thread root, the process may be\n   142:     /// aborted; see the Notes on [`thread::spawn`]. If the process is not\n   143:     /// aborted, this function will return a `Result::Err` containing an opaque\n   144:     /// type.\n   145:     ///\n   146:     /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   147:     /// [`thread::spawn`]: super::spawn\n   148:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   149:     pub fn join(self) -> Result<T> {\n   150:         self.0.join()\n   151:     }\n   152: \n   153:     /// Checks if the associated thread has finished running its main function.\n   154:     ///\n   155:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   156:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   157:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   158:     ///\n   159:     /// This might return `true` for a brief moment after the thread's main\n   160:     /// function has returned, but before the thread itself has stopped running.\n   161:     /// However, once this returns `true`, [`join`][Self::join] can be expected\n   162:     /// to return quickly, without blocking for any significant amount of time.\n   163:     #[stable(feature = \"thread_is_running\", since = \"1.61.0\")]\n   164:     pub fn is_finished(&self) -> bool {\n   165:         self.0.is_finished()\n   166:     }\n   167: }\n   168: \n   169: impl<T> AsInner<imp::Thread> for JoinHandle<T> {",
    "nanvix_source": "   143:     /// aborted, this function will return a `Result::Err` containing an opaque\n   144:     /// type.\n   145:     ///\n   146:     /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   147:     /// [`thread::spawn`]: super::spawn\n   148:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   149:     pub fn join(self) -> Result<T> {\n   150:         self.0.join()\n   151:     }\n   152: \n   153:     /// Checks if the associated thread has finished running its main function.\n   154:     ///\n   155:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   156:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   157:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   158:     ///\n   159:     /// This might return `true` for a brief moment after the thread's main\n   160:     /// function has returned, but before the thread itself has stopped running.\n   161:     /// However, once this returns `true`, [`join`][Self::join] can be expected\n   162:     /// to return quickly, without blocking for any significant amount of time.\n   163:     #[stable(feature = \"thread_is_running\", since = \"1.61.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::JoinHandle::join",
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
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 475,
            "path": "JoinHandle"
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
        "impl_id": "std:563",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:475",
        "resolved_owner_path": [
          "std",
          "thread",
          "join_handle",
          "JoinHandle"
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
    "verification_source": "   129:     /// let builder = thread::Builder::new();\n   130:     ///\n   131:     /// let join_handle: thread::JoinHandle<_> = builder.spawn(|| {\n   132:     ///     // some work here\n   133:     /// }).unwrap();\n   134:     /// join_handle.join().expect(\"Couldn't join on the associated thread\");\n   135:     /// ```\n   136:     ///\n   137:     /// # Notes\n   138:     ///\n   139:     /// If a \"foreign\" unwinding operation (e.g. an exception thrown from C++\n   140:     /// code, or a `panic!` in Rust code compiled or linked with a different\n   141:     /// runtime) unwinds all the way to the thread root, the process may be\n   142:     /// aborted; see the Notes on [`thread::spawn`]. If the process is not\n   143:     /// aborted, this function will return a `Result::Err` containing an opaque\n   144:     /// type.\n   145:     ///\n   146:     /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   147:     /// [`thread::spawn`]: super::spawn\n   148:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   149:     pub fn join(self) -> Result<T> {\n   150:         self.0.join()\n   151:     }\n   152: \n   153:     /// Checks if the associated thread has finished running its main function.\n   154:     ///\n   155:     /// `is_finished` supports implementing a non-blocking join operation, by checking\n   156:     /// `is_finished`, and calling `join` if it returns `true`. This function does not block. To\n   157:     /// block while waiting on the thread to finish, use [`join`][Self::join].\n   158:     ///\n   159:     /// This might return `true` for a brief moment after the thread's main\n   160:     /// function has returned, but before the thread itself has stopped running.\n   161:     /// However, once this returns `true`, [`join`][Self::join] can be expected",
    "nanvix_source": "   135:     /// ```\n   136:     ///\n   137:     /// # Notes\n   138:     ///\n   139:     /// If a \"foreign\" unwinding operation (e.g. an exception thrown from C++\n   140:     /// code, or a `panic!` in Rust code compiled or linked with a different\n   141:     /// runtime) unwinds all the way to the thread root, the process may be\n   142:     /// aborted; see the Notes on [`thread::spawn`]. If the process is not\n   143:     /// aborted, this function will return a `Result::Err` containing an opaque\n   144:     /// type.\n   145:     ///\n   146:     /// [`catch_unwind`]: ../../std/panic/fn.catch_unwind.html\n   147:     /// [`thread::spawn`]: super::spawn\n   148:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   149:     pub fn join(self) -> Result<T> {\n   150:         self.0.join()\n   151:     }\n   152: \n   153:     /// Checks if the associated thread has finished running its main function.\n   154:     ///\n   155:     /// `is_finished` supports implementing a non-blocking join operation, by checking",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::JoinHandle::thread",
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
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 475,
            "path": "JoinHandle"
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
        "impl_id": "std:563",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:475",
        "resolved_owner_path": [
          "std",
          "thread",
          "join_handle",
          "JoinHandle"
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
    "verification_source": "    81:     /// # Examples\n    82:     ///\n    83:     /// ```\n    84:     /// use std::thread;\n    85:     ///\n    86:     /// let builder = thread::Builder::new();\n    87:     ///\n    88:     /// let join_handle: thread::JoinHandle<_> = builder.spawn(|| {\n    89:     ///     // some work here\n    90:     /// }).unwrap();\n    91:     ///\n    92:     /// let thread = join_handle.thread();\n    93:     /// println!(\"thread id: {:?}\", thread.id());\n    94:     /// ```\n    95:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    96:     #[must_use]\n    97:     pub fn thread(&self) -> &Thread {\n    98:         self.0.thread()\n    99:     }\n   100: \n   101:     /// Waits for the associated thread to finish.\n   102:     ///\n   103:     /// This function will return immediately if the associated thread has already finished.\n   104:     /// Otherwise, it fully waits for the thread to finish, including all destructors\n   105:     /// for thread-local variables that might be running after the main function of the thread.\n   106:     ///\n   107:     /// In terms of [atomic memory orderings],  the completion of the associated\n   108:     /// thread synchronizes with this function returning. In other words, all\n   109:     /// operations performed by that thread [happen\n   110:     /// before](https://doc.rust-lang.org/nomicon/atomics.html#data-accesses) all\n   111:     /// operations that happen after `join` returns.\n   112:     ///\n   113:     /// If the associated thread panics, [`Err`] is returned with the parameter given",
    "nanvix_source": "    87:     ///\n    88:     /// let join_handle: thread::JoinHandle<_> = builder.spawn(|| {\n    89:     ///     // some work here\n    90:     /// }).unwrap();\n    91:     ///\n    92:     /// let thread = join_handle.thread();\n    93:     /// println!(\"thread id: {:?}\", thread.id());\n    94:     /// ```\n    95:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    96:     #[must_use]\n    97:     pub fn thread(&self) -> &Thread {\n    98:         self.0.thread()\n    99:     }\n   100: \n   101:     /// Waits for the associated thread to finish.\n   102:     ///\n   103:     /// This function will return immediately if the associated thread has already finished.\n   104:     /// Otherwise, it fully waits for the thread to finish, including all destructors\n   105:     /// for thread-local variables that might be running after the main function of the thread.\n   106:     ///\n   107:     /// In terms of [atomic memory orderings],  the completion of the associated",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::LocalKey::get",
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
                      "id": 126,
                      "path": "Copy"
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
      "name": "get",
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
                        "id": 363,
                        "path": "crate::cell::Cell"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 370,
            "path": "LocalKey"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "outlives": "'static"
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
        "impl_id": "std:379",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:370",
        "resolved_owner_path": [
          "std",
          "thread",
          "local",
          "LocalKey"
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
                "lifetime": "'static",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   539:     ///\n   540:     /// Panics if the key currently has its destructor running,\n   541:     /// and it **may** panic if the destructor has previously been run for this thread.\n   542:     ///\n   543:     /// # Examples\n   544:     ///\n   545:     /// ```\n   546:     /// use std::cell::Cell;\n   547:     ///\n   548:     /// thread_local! {\n   549:     ///     static X: Cell<i32> = const { Cell::new(1) };\n   550:     /// }\n   551:     ///\n   552:     /// assert_eq!(X.get(), 1);\n   553:     /// ```\n   554:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   555:     pub fn get(&'static self) -> T\n   556:     where\n   557:         T: Copy,\n   558:     {\n   559:         self.with(Cell::get)\n   560:     }\n   561: \n   562:     /// Takes the contained value, leaving `Default::default()` in its place.\n   563:     ///\n   564:     /// This will lazily initialize the value if this thread has not referenced\n   565:     /// this key yet.\n   566:     ///\n   567:     /// # Panics\n   568:     ///\n   569:     /// Panics if the key currently has its destructor running,\n   570:     /// and it **may** panic if the destructor has previously been run for this thread.\n   571:     ///",
    "nanvix_source": "   546:     /// ```\n   547:     /// use std::cell::Cell;\n   548:     ///\n   549:     /// thread_local! {\n   550:     ///     static X: Cell<i32> = const { Cell::new(1) };\n   551:     /// }\n   552:     ///\n   553:     /// assert_eq!(X.get(), 1);\n   554:     /// ```\n   555:     #[stable(feature = \"local_key_cell_methods\", since = \"1.73.0\")]\n   556:     pub fn get(&'static self) -> T\n   557:     where\n   558:         T: Copy,\n   559:     {\n   560:         self.with(Cell::get)\n   561:     }\n   562: \n   563:     /// Takes the contained value, leaving `Default::default()` in its place.\n   564:     ///\n   565:     /// This will lazily initialize the value if this thread has not referenced\n   566:     /// this key yet.",
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
