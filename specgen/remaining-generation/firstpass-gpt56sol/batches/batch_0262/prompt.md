For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::thread::Thread::id",
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
      "name": "id",
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
            "id": 504,
            "path": "Thread"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:650",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:504",
        "resolved_owner_path": [
          "std",
          "thread",
          "thread",
          "Thread"
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
            "id": 502,
            "path": "ThreadId"
          }
        }
      }
    },
    "verification_source": "   187:     /// Gets the thread's unique identifier.\n   188:     ///\n   189:     /// # Examples\n   190:     ///\n   191:     /// ```\n   192:     /// use std::thread;\n   193:     ///\n   194:     /// let other_thread = thread::spawn(|| {\n   195:     ///     thread::current().id()\n   196:     /// });\n   197:     ///\n   198:     /// let other_thread_id = other_thread.join().unwrap();\n   199:     /// assert!(thread::current().id() != other_thread_id);\n   200:     /// ```\n   201:     #[stable(feature = \"thread_id\", since = \"1.19.0\")]\n   202:     #[must_use]\n   203:     pub fn id(&self) -> ThreadId {\n   204:         self.inner.id\n   205:     }\n   206: \n   207:     /// Gets the thread's name.\n   208:     ///\n   209:     /// For more information about named threads, see\n   210:     /// [this module-level documentation][naming-threads].\n   211:     ///\n   212:     /// # Examples\n   213:     ///\n   214:     /// Threads by default have no name specified:\n   215:     ///\n   216:     /// ```\n   217:     /// use std::thread;\n   218:     ///\n   219:     /// let builder = thread::Builder::new();",
    "nanvix_source": "   193:     ///\n   194:     /// let other_thread = thread::spawn(|| {\n   195:     ///     thread::current().id()\n   196:     /// });\n   197:     ///\n   198:     /// let other_thread_id = other_thread.join().unwrap();\n   199:     /// assert!(thread::current().id() != other_thread_id);\n   200:     /// ```\n   201:     #[stable(feature = \"thread_id\", since = \"1.19.0\")]\n   202:     #[must_use]\n   203:     pub fn id(&self) -> ThreadId {\n   204:         self.inner.id\n   205:     }\n   206: \n   207:     /// Gets the thread's name.\n   208:     ///\n   209:     /// For more information about named threads, see\n   210:     /// [this module-level documentation][naming-threads].\n   211:     ///\n   212:     /// # Examples\n   213:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Thread::name",
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
      "name": "name",
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
            "args": null,
            "id": 504,
            "path": "Thread"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:650",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:504",
        "resolved_owner_path": [
          "std",
          "thread",
          "thread",
          "Thread"
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
                          "primitive": "str"
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
    "verification_source": "   230:     /// ```\n   231:     /// use std::thread;\n   232:     ///\n   233:     /// let builder = thread::Builder::new()\n   234:     ///     .name(\"foo\".into());\n   235:     ///\n   236:     /// let handler = builder.spawn(|| {\n   237:     ///     assert_eq!(thread::current().name(), Some(\"foo\"))\n   238:     /// }).unwrap();\n   239:     ///\n   240:     /// handler.join().unwrap();\n   241:     /// ```\n   242:     ///\n   243:     /// [naming-threads]: ./index.html#naming-threads\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     #[must_use]\n   246:     pub fn name(&self) -> Option<&str> {\n   247:         if let Some(name) = &self.inner.name {\n   248:             Some(name.as_str())\n   249:         } else if main_thread::get() == Some(self.inner.id) {\n   250:             Some(\"main\")\n   251:         } else {\n   252:             None\n   253:         }\n   254:     }\n   255: \n   256:     /// Consumes the `Thread`, returning a raw pointer.\n   257:     ///\n   258:     /// To avoid a memory leak the pointer must be converted\n   259:     /// back into a `Thread` using [`Thread::from_raw`]. The pointer is\n   260:     /// guaranteed to be aligned to at least 8 bytes.\n   261:     ///\n   262:     /// # Examples",
    "nanvix_source": "   236:     /// let handler = builder.spawn(|| {\n   237:     ///     assert_eq!(thread::current().name(), Some(\"foo\"))\n   238:     /// }).unwrap();\n   239:     ///\n   240:     /// handler.join().unwrap();\n   241:     /// ```\n   242:     ///\n   243:     /// [naming-threads]: ./index.html#naming-threads\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     #[must_use]\n   246:     pub fn name(&self) -> Option<&str> {\n   247:         if let Some(name) = &self.inner.name {\n   248:             Some(name.as_str())\n   249:         } else if main_thread::get() == Some(self.inner.id) {\n   250:             Some(\"main\")\n   251:         } else {\n   252:             None\n   253:         }\n   254:     }\n   255: \n   256:     /// Consumes the `Thread`, returning a raw pointer.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::Thread::unpark",
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
      "name": "unpark",
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
            "id": 504,
            "path": "Thread"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:650",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:504",
        "resolved_owner_path": [
          "std",
          "thread",
          "thread",
          "Thread"
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
    "verification_source": "   167:     /// while !QUEUED.load(Ordering::Acquire) {\n   168:     ///     // Spinning is of course inefficient; in practice, this would more likely be\n   169:     ///     // a dequeue where we have no work to do if there's nobody queued.\n   170:     ///     std::hint::spin_loop();\n   171:     /// }\n   172:     ///\n   173:     /// println!(\"Unpark the thread\");\n   174:     /// parked_thread.thread().unpark();\n   175:     ///\n   176:     /// parked_thread.join().unwrap();\n   177:     /// ```\n   178:     ///\n   179:     /// [`park`]: super::park\n   180:     /// [park documentation]: super::park\n   181:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   182:     #[inline]\n   183:     pub fn unpark(&self) {\n   184:         self.inner.as_ref().parker().unpark();\n   185:     }\n   186: \n   187:     /// Gets the thread's unique identifier.\n   188:     ///\n   189:     /// # Examples\n   190:     ///\n   191:     /// ```\n   192:     /// use std::thread;\n   193:     ///\n   194:     /// let other_thread = thread::spawn(|| {\n   195:     ///     thread::current().id()\n   196:     /// });\n   197:     ///\n   198:     /// let other_thread_id = other_thread.join().unwrap();\n   199:     /// assert!(thread::current().id() != other_thread_id);",
    "nanvix_source": "   173:     /// println!(\"Unpark the thread\");\n   174:     /// parked_thread.thread().unpark();\n   175:     ///\n   176:     /// parked_thread.join().unwrap();\n   177:     /// ```\n   178:     ///\n   179:     /// [`park`]: super::park\n   180:     /// [park documentation]: super::park\n   181:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   182:     #[inline]\n   183:     pub fn unpark(&self) {\n   184:         self.inner.as_ref().parker().unpark();\n   185:     }\n   186: \n   187:     /// Gets the thread's unique identifier.\n   188:     ///\n   189:     /// # Examples\n   190:     ///\n   191:     /// ```\n   192:     /// use std::thread;\n   193:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::available_parallelism",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "available_parallelism",
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
                                  "primitive": "usize"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 522,
                        "path": "crate::num::NonZero"
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
    "verification_source": "   657: ///   scan mountpoints to find the corresponding cgroup v1 controller,\n   658: ///   which may take time on systems with large numbers of mountpoints.\n   659: ///   (This does not apply to cgroup v2, or to processes not in a\n   660: ///   cgroup.)\n   661: /// - It does not attempt to take `ulimit` into account. If there is a limit set on the number of\n   662: ///   threads, `available_parallelism` cannot know how much of that limit a Rust program should\n   663: ///   take, or know in a reliable and race-free way how much of that limit is already taken.\n   664: ///\n   665: /// On all targets:\n   666: /// - It may overcount the amount of parallelism available when running in a VM\n   667: /// with CPU usage limits (e.g. an overcommitted host).\n   668: ///\n   669: /// # Errors\n   670: ///\n   671: /// This function will, but is not limited to, return errors in the following\n   672: /// cases:\n   673: ///\n   674: /// - If the amount of parallelism is not known for the target platform.\n   675: /// - If the program lacks permission to query the amount of parallelism made\n   676: ///   available to it.\n   677: ///\n   678: /// # Examples\n   679: ///\n   680: /// ```\n   681: /// # #![allow(dead_code)]\n   682: /// use std::{io, thread};\n   683: ///\n   684: /// fn main() -> io::Result<()> {\n   685: ///     let count = thread::available_parallelism()?.get();\n   686: ///     assert!(count >= 1_usize);\n   687: ///     Ok(())\n   688: /// }\n   689: /// ```",
    "nanvix_source": "   663: ///   take, or know in a reliable and race-free way how much of that limit is already taken.\n   664: ///\n   665: /// On all targets:\n   666: /// - It may overcount the amount of parallelism available when running in a VM\n   667: /// with CPU usage limits (e.g. an overcommitted host).\n   668: ///\n   669: /// # Errors\n   670: ///\n   671: /// This function will, but is not limited to, return errors in the following\n   672: /// cases:\n   673: ///\n   674: /// - If the amount of parallelism is not known for the target platform.\n   675: /// - If the program lacks permission to query the amount of parallelism made\n   676: ///   available to it.\n   677: ///\n   678: /// # Examples\n   679: ///\n   680: /// ```\n   681: /// # #![allow(dead_code)]\n   682: /// use std::{io, thread};\n   683: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::current",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "current",
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
          "resolved_path": {
            "args": null,
            "id": 504,
            "path": "super::thread::Thread"
          }
        }
      }
    },
    "verification_source": "   260: ///\n   261: /// ```\n   262: /// use std::thread;\n   263: ///\n   264: /// let handler = thread::Builder::new()\n   265: ///     .name(\"named thread\".into())\n   266: ///     .spawn(|| {\n   267: ///         let handle = thread::current();\n   268: ///         assert_eq!(handle.name(), Some(\"named thread\"));\n   269: ///     })\n   270: ///     .unwrap();\n   271: ///\n   272: /// handler.join().unwrap();\n   273: /// ```\n   274: #[must_use]\n   275: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   276: pub fn current() -> Thread {\n   277:     let current = CURRENT.get();\n   278:     if current > DESTROYED {\n   279:         unsafe {\n   280:             let current = ManuallyDrop::new(Thread::from_raw(current));\n   281:             (*current).clone()\n   282:         }\n   283:     } else {\n   284:         init_current(current)\n   285:     }\n   286: }\n   287: \n   288: #[cold]\n   289: fn init_current(current: *mut ()) -> Thread {\n   290:     if current == NONE {\n   291:         CURRENT.set(BUSY);\n   292:         // If the thread ID was initialized already, use it.",
    "nanvix_source": "   266: ///     .spawn(|| {\n   267: ///         let handle = thread::current();\n   268: ///         assert_eq!(handle.name(), Some(\"named thread\"));\n   269: ///     })\n   270: ///     .unwrap();\n   271: ///\n   272: /// handler.join().unwrap();\n   273: /// ```\n   274: #[must_use]\n   275: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   276: pub fn current() -> Thread {\n   277:     let current = CURRENT.get();\n   278:     if current > DESTROYED {\n   279:         unsafe {\n   280:             let current = ManuallyDrop::new(Thread::from_raw(current));\n   281:             (*current).clone()\n   282:         }\n   283:     } else {\n   284:         init_current(current)\n   285:     }\n   286: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::thread::panicking",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "panicking",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   204: /// {\n   205: ///     print!(\"a: \");\n   206: ///     let a = SomeStruct;\n   207: /// }\n   208: ///\n   209: /// {\n   210: ///     print!(\"b: \");\n   211: ///     let b = SomeStruct;\n   212: ///     panic!()\n   213: /// }\n   214: /// ```\n   215: ///\n   216: /// [Mutex]: crate::sync::Mutex\n   217: #[inline]\n   218: #[must_use]\n   219: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   220: pub fn panicking() -> bool {\n   221:     panicking::panicking()\n   222: }\n   223: \n   224: /// Uses [`sleep`].\n   225: ///\n   226: /// Puts the current thread to sleep for at least the specified amount of time.\n   227: ///\n   228: /// The thread may sleep longer than the duration specified due to scheduling\n   229: /// specifics or platform-dependent functionality. It will never sleep less.\n   230: ///\n   231: /// This function is blocking, and should not be used in `async` functions.\n   232: ///\n   233: /// # Platform-specific behavior\n   234: ///\n   235: /// On Unix platforms, the underlying syscall may be interrupted by a\n   236: /// spurious wakeup or signal handler. To ensure the sleep occurs for at least",
    "nanvix_source": "   210: ///     print!(\"b: \");\n   211: ///     let b = SomeStruct;\n   212: ///     panic!()\n   213: /// }\n   214: /// ```\n   215: ///\n   216: /// [Mutex]: crate::sync::Mutex\n   217: #[inline]\n   218: #[must_use]\n   219: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   220: pub fn panicking() -> bool {\n   221:     panicking::panicking()\n   222: }\n   223: \n   224: /// Uses [`sleep`].\n   225: ///\n   226: /// Puts the current thread to sleep for at least the specified amount of time.\n   227: ///\n   228: /// The thread may sleep longer than the duration specified due to scheduling\n   229: /// specifics or platform-dependent functionality. It will never sleep less.\n   230: ///",
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
