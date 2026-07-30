For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::mpsc::channel",
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
      "concurrency_or_hidden_state"
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
      "name": "channel",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "tuple": [
            {
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
                "id": 7867,
                "path": "Sender"
              }
            },
            {
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
                "id": 7865,
                "path": "Receiver"
              }
            }
          ]
        }
      }
    },
    "verification_source": "   503: ///\n   504: /// let (sender, receiver) = channel();\n   505: ///\n   506: /// // Spawn off an expensive computation\n   507: /// thread::spawn(move || {\n   508: /// #   fn expensive_computation() {}\n   509: ///     sender.send(expensive_computation()).unwrap();\n   510: /// });\n   511: ///\n   512: /// // Do some useful work for a while\n   513: ///\n   514: /// // Let's see what that answer was\n   515: /// println!(\"{:?}\", receiver.recv().unwrap());\n   516: /// ```\n   517: #[must_use]\n   518: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   519: pub fn channel<T>() -> (Sender<T>, Receiver<T>) {\n   520:     let (tx, rx) = mpmc::channel();\n   521:     (Sender { inner: tx }, Receiver { inner: rx })\n   522: }\n   523: \n   524: /// Creates a new synchronous, bounded channel.\n   525: ///\n   526: /// All data sent on the [`SyncSender`] will become available on the [`Receiver`]\n   527: /// in the same order as it was sent. Like asynchronous [`channel`]s, the\n   528: /// [`Receiver`] will block until a message becomes available. `sync_channel`\n   529: /// differs greatly in the semantics of the sender, however.\n   530: ///\n   531: /// This channel has an internal buffer on which messages will be queued.\n   532: /// `bound` specifies the buffer size. When the internal buffer becomes full,\n   533: /// future sends will *block* waiting for the buffer to open up. Note that a\n   534: /// buffer size of 0 is valid, in which case this becomes \"rendezvous channel\"\n   535: /// where each [`send`] will not return until a [`recv`] is paired with it.",
    "nanvix_source": "   516: ///     sender.send(expensive_computation()).unwrap();\n   517: /// });\n   518: ///\n   519: /// // Do some useful work for a while\n   520: ///\n   521: /// // Let's see what that answer was\n   522: /// println!(\"{:?}\", receiver.recv().unwrap());\n   523: /// ```\n   524: #[must_use]\n   525: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   526: pub fn channel<T>() -> (Sender<T>, Receiver<T>) {\n   527:     let (tx, rx) = mpmc::channel();\n   528:     (Sender { inner: tx }, Receiver { inner: rx })\n   529: }\n   530: \n   531: /// Creates a new synchronous, bounded channel.\n   532: ///\n   533: /// All data sent on the [`SyncSender`] will become available on the [`Receiver`]\n   534: /// in the same order as it was sent. Like asynchronous [`channel`]s, the\n   535: /// [`Receiver`] will block until a message becomes available. `sync_channel`\n   536: /// differs greatly in the semantics of the sender, however.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::sync_channel",
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
      "concurrency_or_hidden_state"
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
      "name": "sync_channel",
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
            "bound",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "tuple": [
            {
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
                "id": 7868,
                "path": "SyncSender"
              }
            },
            {
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
                "id": 7865,
                "path": "Receiver"
              }
            }
          ]
        }
      }
    },
    "verification_source": "   553: ///\n   554: /// let (sender, receiver) = sync_channel(1);\n   555: ///\n   556: /// // this returns immediately\n   557: /// sender.send(1).unwrap();\n   558: ///\n   559: /// thread::spawn(move || {\n   560: ///     // this will block until the previous message has been received\n   561: ///     sender.send(2).unwrap();\n   562: /// });\n   563: ///\n   564: /// assert_eq!(receiver.recv().unwrap(), 1);\n   565: /// assert_eq!(receiver.recv().unwrap(), 2);\n   566: /// ```\n   567: #[must_use]\n   568: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   569: pub fn sync_channel<T>(bound: usize) -> (SyncSender<T>, Receiver<T>) {\n   570:     let (tx, rx) = mpmc::sync_channel(bound);\n   571:     (SyncSender { inner: tx }, Receiver { inner: rx })\n   572: }\n   573: \n   574: ////////////////////////////////////////////////////////////////////////////////\n   575: // Sender\n   576: ////////////////////////////////////////////////////////////////////////////////\n   577: \n   578: impl<T> Sender<T> {\n   579:     /// Attempts to send a value on this channel, returning it back if it could\n   580:     /// not be sent.\n   581:     ///\n   582:     /// A successful send occurs when it is determined that the other end of\n   583:     /// the channel has not hung up already. An unsuccessful send would be one\n   584:     /// where the corresponding receiver has already been deallocated. Note\n   585:     /// that a return value of [`Err`] means that the data will never be",
    "nanvix_source": "   566: /// thread::spawn(move || {\n   567: ///     // this will block until the previous message has been received\n   568: ///     sender.send(2).unwrap();\n   569: /// });\n   570: ///\n   571: /// assert_eq!(receiver.recv().unwrap(), 1);\n   572: /// assert_eq!(receiver.recv().unwrap(), 2);\n   573: /// ```\n   574: #[must_use]\n   575: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   576: pub fn sync_channel<T>(bound: usize) -> (SyncSender<T>, Receiver<T>) {\n   577:     let (tx, rx) = mpmc::sync_channel(bound);\n   578:     (SyncSender { inner: tx }, Receiver { inner: rx })\n   579: }\n   580: \n   581: ////////////////////////////////////////////////////////////////////////////////\n   582: // Sender\n   583: ////////////////////////////////////////////////////////////////////////////////\n   584: \n   585: impl<T> Sender<T> {\n   586:     /// Attempts to send a value on this channel, returning it back if it could",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Builder::name",
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
      "name": "name",
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
            "name",
            {
              "resolved_path": {
                "args": null,
                "id": 218,
                "path": "String"
              }
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
    "verification_source": "    91:     ///\n    92:     /// ```\n    93:     /// use std::thread;\n    94:     ///\n    95:     /// let builder = thread::Builder::new()\n    96:     ///     .name(\"foo\".into());\n    97:     ///\n    98:     /// let handler = builder.spawn(|| {\n    99:     ///     assert_eq!(thread::current().name(), Some(\"foo\"))\n   100:     /// }).unwrap();\n   101:     ///\n   102:     /// handler.join().unwrap();\n   103:     /// ```\n   104:     ///\n   105:     /// [naming-threads]: ./index.html#naming-threads\n   106:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   107:     pub fn name(mut self, name: String) -> Builder {\n   108:         self.name = Some(name);\n   109:         self\n   110:     }\n   111: \n   112:     /// Sets the size of the stack (in bytes) for the new thread.\n   113:     ///\n   114:     /// The actual stack size may be greater than this value if\n   115:     /// the platform specifies a minimal stack size.\n   116:     ///\n   117:     /// For more information about the stack size for threads, see\n   118:     /// [this module-level documentation][stack-size].\n   119:     ///\n   120:     /// # Examples\n   121:     ///\n   122:     /// ```\n   123:     /// use std::thread;",
    "nanvix_source": "    97:     ///\n    98:     /// let handler = builder.spawn(|| {\n    99:     ///     assert_eq!(thread::current().name(), Some(\"foo\"))\n   100:     /// }).unwrap();\n   101:     ///\n   102:     /// handler.join().unwrap();\n   103:     /// ```\n   104:     ///\n   105:     /// [naming-threads]: ./index.html#naming-threads\n   106:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   107:     pub fn name(mut self, name: String) -> Builder {\n   108:         self.name = Some(name);\n   109:         self\n   110:     }\n   111: \n   112:     /// Sets the size of the stack (in bytes) for the new thread.\n   113:     ///\n   114:     /// The actual stack size may be greater than this value if\n   115:     /// the platform specifies a minimal stack size.\n   116:     ///\n   117:     /// For more information about the stack size for threads, see",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Builder::new",
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
        "inputs": [],
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
    "verification_source": "    62:     /// # Examples\n    63:     ///\n    64:     /// ```\n    65:     /// use std::thread;\n    66:     ///\n    67:     /// let builder = thread::Builder::new()\n    68:     ///                               .name(\"foo\".into())\n    69:     ///                               .stack_size(32 * 1024);\n    70:     ///\n    71:     /// let handler = builder.spawn(|| {\n    72:     ///     // thread code\n    73:     /// }).unwrap();\n    74:     ///\n    75:     /// handler.join().unwrap();\n    76:     /// ```\n    77:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    78:     pub fn new() -> Builder {\n    79:         Builder { name: None, stack_size: None, no_hooks: false }\n    80:     }\n    81: \n    82:     /// Names the thread-to-be. Currently the name is used for identification\n    83:     /// only in panic messages.\n    84:     ///\n    85:     /// The name must not contain null bytes (`\\0`).\n    86:     ///\n    87:     /// For more information about named threads, see\n    88:     /// [this module-level documentation][naming-threads].\n    89:     ///\n    90:     /// # Examples\n    91:     ///\n    92:     /// ```\n    93:     /// use std::thread;\n    94:     ///",
    "nanvix_source": "    68:     ///                               .name(\"foo\".into())\n    69:     ///                               .stack_size(32 * 1024);\n    70:     ///\n    71:     /// let handler = builder.spawn(|| {\n    72:     ///     // thread code\n    73:     /// }).unwrap();\n    74:     ///\n    75:     /// handler.join().unwrap();\n    76:     /// ```\n    77:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    78:     pub fn new() -> Builder {\n    79:         Builder { name: None, stack_size: None, no_hooks: false }\n    80:     }\n    81: \n    82:     /// Names the thread-to-be. Currently the name is used for identification\n    83:     /// only in panic messages.\n    84:     ///\n    85:     /// The name must not contain null bytes (`\\0`).\n    86:     ///\n    87:     /// For more information about named threads, see\n    88:     /// [this module-level documentation][naming-threads].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Builder::spawn",
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
    "verification_source": "   169:     /// ```\n   170:     /// use std::thread;\n   171:     ///\n   172:     /// let builder = thread::Builder::new();\n   173:     ///\n   174:     /// let handler = builder.spawn(|| {\n   175:     ///     // thread code\n   176:     /// }).unwrap();\n   177:     ///\n   178:     /// handler.join().unwrap();\n   179:     /// ```\n   180:     ///\n   181:     /// [`thread::spawn`]: super::spawn\n   182:     /// [`spawn`]: super::spawn\n   183:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   184:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   185:     pub fn spawn<F, T>(self, f: F) -> io::Result<JoinHandle<T>>\n   186:     where\n   187:         F: FnOnce() -> T,\n   188:         F: Send + 'static,\n   189:         T: Send + 'static,\n   190:     {\n   191:         unsafe { self.spawn_unchecked(f) }\n   192:     }\n   193: \n   194:     /// Spawns a new thread without any lifetime restrictions by taking ownership\n   195:     /// of the `Builder`, and returns an [`io::Result`] to its [`JoinHandle`].\n   196:     ///\n   197:     /// The spawned thread may outlive the caller (unless the caller thread\n   198:     /// is the main thread; the whole process is terminated when the main\n   199:     /// thread finishes). The join handle can be used to block on\n   200:     /// termination of the spawned thread, including recovering its panics.\n   201:     ///",
    "nanvix_source": "   175:     ///     // thread code\n   176:     /// }).unwrap();\n   177:     ///\n   178:     /// handler.join().unwrap();\n   179:     /// ```\n   180:     ///\n   181:     /// [`thread::spawn`]: super::spawn\n   182:     /// [`spawn`]: super::spawn\n   183:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   184:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   185:     pub fn spawn<F, T>(self, f: F) -> io::Result<JoinHandle<T>>\n   186:     where\n   187:         F: FnOnce() -> T,\n   188:         F: Send + 'static,\n   189:         T: Send + 'static,\n   190:     {\n   191:         unsafe { self.spawn_unchecked(f) }\n   192:     }\n   193: \n   194:     /// Spawns a new thread without any lifetime restrictions by taking ownership\n   195:     /// of the `Builder`, and returns an [`io::Result`] to its [`JoinHandle`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Builder::spawn_scoped",
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
      "name": "spawn_scoped",
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
            "path": "super::builder::Builder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:482",
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
            "scope",
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
    "verification_source": "   240:     ///         .spawn_scoped(s, ||\n   241:     ///     {\n   242:     ///         println!(\"hello from the {:?} scoped thread\", thread::current().name());\n   243:     ///         // We can even mutably borrow `x` here,\n   244:     ///         // because no other threads are using it.\n   245:     ///         x += a[0] + a[2];\n   246:     ///     })\n   247:     ///     .unwrap();\n   248:     ///     println!(\"hello from the main thread\");\n   249:     /// });\n   250:     ///\n   251:     /// // After the scope, we can modify and access our variables again:\n   252:     /// a.push(4);\n   253:     /// assert_eq!(x, a.len());\n   254:     /// ```\n   255:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   256:     pub fn spawn_scoped<'scope, 'env, F, T>(\n   257:         self,\n   258:         scope: &'scope Scope<'scope, 'env>,\n   259:         f: F,\n   260:     ) -> io::Result<ScopedJoinHandle<'scope, T>>\n   261:     where\n   262:         F: FnOnce() -> T + Send + 'scope,\n   263:         T: Send + 'scope,\n   264:     {\n   265:         let Builder { name, stack_size, no_hooks } = self;\n   266:         Ok(ScopedJoinHandle(unsafe {\n   267:             spawn_unchecked(name, stack_size, no_hooks, Some(scope.data.clone()), f)\n   268:         }?))\n   269:     }\n   270: }\n   271: \n   272: impl<'scope, T> ScopedJoinHandle<'scope, T> {",
    "nanvix_source": "   246:     ///     })\n   247:     ///     .unwrap();\n   248:     ///     println!(\"hello from the main thread\");\n   249:     /// });\n   250:     ///\n   251:     /// // After the scope, we can modify and access our variables again:\n   252:     /// a.push(4);\n   253:     /// assert_eq!(x, a.len());\n   254:     /// ```\n   255:     #[stable(feature = \"scoped_threads\", since = \"1.63.0\")]\n   256:     pub fn spawn_scoped<'scope, 'env, F, T>(\n   257:         self,\n   258:         scope: &'scope Scope<'scope, 'env>,\n   259:         f: F,\n   260:     ) -> io::Result<ScopedJoinHandle<'scope, T>>\n   261:     where\n   262:         F: FnOnce() -> T + Send + 'scope,\n   263:         T: Send + 'scope,\n   264:     {\n   265:         let Builder { name, stack_size, no_hooks } = self;\n   266:         Ok(ScopedJoinHandle(unsafe {",
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
