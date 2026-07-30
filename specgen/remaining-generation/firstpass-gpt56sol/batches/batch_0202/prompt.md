For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::PipeReader::try_clone",
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
      "name": "try_clone",
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
            "id": 3617,
            "path": "PipeReader"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3622",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3617",
        "resolved_owner_path": [
          "std",
          "io",
          "pipe",
          "PipeReader"
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
                      "generic": "Self"
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
    "verification_source": "   161:     ///     );\n   162:     /// }\n   163:     ///\n   164:     /// // Wait for all jobs to finish.\n   165:     /// for mut job in jobs {\n   166:     ///     job.wait()?;\n   167:     /// }\n   168:     ///\n   169:     /// // Check our work and clean up.\n   170:     /// let xs = fs::read_to_string(OUTPUT)?;\n   171:     /// fs::remove_file(OUTPUT)?;\n   172:     /// assert_eq!(xs, \"x\".repeat(NUM_PROC.into()));\n   173:     /// # Ok(())\n   174:     /// # }\n   175:     /// ```\n   176:     #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   177:     pub fn try_clone(&self) -> io::Result<Self> {\n   178:         self.0.try_clone().map(Self)\n   179:     }\n   180: }\n   181: \n   182: impl PipeWriter {\n   183:     /// Creates a new [`PipeWriter`] instance that shares the same underlying file description.\n   184:     ///\n   185:     /// # Examples\n   186:     ///\n   187:     /// ```no_run\n   188:     /// # #[cfg(miri)] fn main() {}\n   189:     /// # #[cfg(not(miri))]\n   190:     /// # fn main() -> std::io::Result<()> {\n   191:     /// use std::process::Command;\n   192:     /// use std::io::{pipe, Read};\n   193:     /// let (mut reader, writer) = pipe()?;",
    "nanvix_source": "   163:     /// }\n   164:     ///\n   165:     /// // Check our work and clean up.\n   166:     /// let xs = fs::read_to_string(OUTPUT)?;\n   167:     /// fs::remove_file(OUTPUT)?;\n   168:     /// assert_eq!(xs, \"x\".repeat(NUM_PROC.into()));\n   169:     /// # Ok(())\n   170:     /// # }\n   171:     /// ```\n   172:     #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   173:     pub fn try_clone(&self) -> io::Result<Self> {\n   174:         self.0.try_clone().map(Self)\n   175:     }\n   176: }\n   177: \n   178: impl PipeWriter {\n   179:     /// Creates a new [`PipeWriter`] instance that shares the same underlying file description.\n   180:     ///\n   181:     /// # Examples\n   182:     ///\n   183:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::PipeWriter::try_clone",
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
      "name": "try_clone",
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
            "id": 3618,
            "path": "PipeWriter"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3679",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3618",
        "resolved_owner_path": [
          "std",
          "io",
          "pipe",
          "PipeWriter"
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
                      "generic": "Self"
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
    "verification_source": "   200:     ///          echo -n bar >&2\"\n   201:     ///     ])\n   202:     ///     .stdout(writer.try_clone()?)\n   203:     ///     .stderr(writer)\n   204:     ///     .spawn()?;\n   205:     ///\n   206:     /// // Read and check the result.\n   207:     /// let mut msg = String::new();\n   208:     /// reader.read_to_string(&mut msg)?;\n   209:     /// assert_eq!(&msg, \"foobar\");\n   210:     ///\n   211:     /// peer.wait()?;\n   212:     /// # Ok(())\n   213:     /// # }\n   214:     /// ```\n   215:     #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   216:     pub fn try_clone(&self) -> io::Result<Self> {\n   217:         self.0.try_clone().map(Self)\n   218:     }\n   219: }\n   220: \n   221: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   222: impl io::Read for &PipeReader {\n   223:     fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {\n   224:         self.0.read(buf)\n   225:     }\n   226:     fn read_vectored(&mut self, bufs: &mut [io::IoSliceMut<'_>]) -> io::Result<usize> {\n   227:         self.0.read_vectored(bufs)\n   228:     }\n   229:     #[inline]\n   230:     fn is_read_vectored(&self) -> bool {\n   231:         self.0.is_read_vectored()\n   232:     }",
    "nanvix_source": "   200:     /// // Read and check the result.\n   201:     /// let mut msg = String::new();\n   202:     /// reader.read_to_string(&mut msg)?;\n   203:     /// assert_eq!(&msg, \"foobar\");\n   204:     ///\n   205:     /// peer.wait()?;\n   206:     /// # Ok(())\n   207:     /// # }\n   208:     /// ```\n   209:     #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   210:     pub fn try_clone(&self) -> io::Result<Self> {\n   211:         self.0.try_clone().map(Self)\n   212:     }\n   213: }\n   214: \n   215: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n   216: impl io::Read for &PipeReader {\n   217:     fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {\n   218:         self.0.read(buf)\n   219:     }\n   220:     fn read_vectored(&mut self, bufs: &mut [io::IoSliceMut<'_>]) -> io::Result<usize> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Stderr::lock",
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
      "name": "lock",
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
            "id": 3937,
            "path": "Stderr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3940",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3937",
        "resolved_owner_path": [
          "std",
          "io",
          "stdio",
          "Stderr"
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
                    "lifetime": "'static"
                  }
                ],
                "constraints": []
              }
            },
            "id": 3939,
            "path": "StderrLock"
          }
        }
      }
    },
    "verification_source": "   981:     ///\n   982:     /// # Examples\n   983:     ///\n   984:     /// ```\n   985:     /// use std::io::{self, Write};\n   986:     ///\n   987:     /// fn foo() -> io::Result<()> {\n   988:     ///     let stderr = io::stderr();\n   989:     ///     let mut handle = stderr.lock();\n   990:     ///\n   991:     ///     handle.write_all(b\"hello world\")?;\n   992:     ///\n   993:     ///     Ok(())\n   994:     /// }\n   995:     /// ```\n   996:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   997:     pub fn lock(&self) -> StderrLock<'static> {\n   998:         // Locks this handle with 'static lifetime. This depends on the\n   999:         // implementation detail that the underlying `ReentrantMutex` is\n  1000:         // static.\n  1001:         StderrLock { inner: self.inner.lock() }\n  1002:     }\n  1003: }\n  1004: \n  1005: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n  1006: impl UnwindSafe for Stderr {}\n  1007: \n  1008: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n  1009: impl RefUnwindSafe for Stderr {}\n  1010: \n  1011: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n  1012: impl fmt::Debug for Stderr {\n  1013:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "nanvix_source": "   988:     /// fn foo() -> io::Result<()> {\n   989:     ///     let stderr = io::stderr();\n   990:     ///     let mut handle = stderr.lock();\n   991:     ///\n   992:     ///     handle.write_all(b\"hello world\")?;\n   993:     ///\n   994:     ///     Ok(())\n   995:     /// }\n   996:     /// ```\n   997:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   998:     pub fn lock(&self) -> StderrLock<'static> {\n   999:         // Locks this handle with 'static lifetime. This depends on the\n  1000:         // implementation detail that the underlying `ReentrantMutex` is\n  1001:         // static.\n  1002:         StderrLock { inner: self.inner.lock() }\n  1003:     }\n  1004: }\n  1005: \n  1006: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n  1007: impl UnwindSafe for Stderr {}\n  1008: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Stdin::lines",
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
      "name": "lines",
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
            "id": 3739,
            "path": "Stdin"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3748",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3739",
        "resolved_owner_path": [
          "std",
          "io",
          "stdio",
          "Stdin"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'static"
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 3741,
                        "path": "StdinLock"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3747,
            "path": "Lines"
          }
        }
      }
    },
    "verification_source": "   416:     ///\n   417:     /// For detailed semantics of this method, see the documentation on\n   418:     /// [`BufRead::lines`].\n   419:     ///\n   420:     /// # Examples\n   421:     ///\n   422:     /// ```no_run\n   423:     /// use std::io;\n   424:     ///\n   425:     /// let lines = io::stdin().lines();\n   426:     /// for line in lines {\n   427:     ///     println!(\"got a line: {}\", line.unwrap());\n   428:     /// }\n   429:     /// ```\n   430:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   431:     #[stable(feature = \"stdin_forwarders\", since = \"1.62.0\")]\n   432:     pub fn lines(self) -> Lines<StdinLock<'static>> {\n   433:         self.lock().lines()\n   434:     }\n   435: }\n   436: \n   437: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   438: impl fmt::Debug for Stdin {\n   439:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   440:         f.debug_struct(\"Stdin\").finish_non_exhaustive()\n   441:     }\n   442: }\n   443: \n   444: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   445: impl Read for Stdin {\n   446:     fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {\n   447:         self.lock().read(buf)\n   448:     }",
    "nanvix_source": "   423:     /// ```no_run\n   424:     /// use std::io;\n   425:     ///\n   426:     /// let lines = io::stdin().lines();\n   427:     /// for line in lines {\n   428:     ///     println!(\"got a line: {}\", line.unwrap());\n   429:     /// }\n   430:     /// ```\n   431:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   432:     #[stable(feature = \"stdin_forwarders\", since = \"1.62.0\")]\n   433:     pub fn lines(self) -> Lines<StdinLock<'static>> {\n   434:         self.lock().lines()\n   435:     }\n   436: }\n   437: \n   438: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   439: impl fmt::Debug for Stdin {\n   440:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   441:         f.debug_struct(\"Stdin\").finish_non_exhaustive()\n   442:     }\n   443: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Stdin::lock",
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
      "name": "lock",
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
            "id": 3739,
            "path": "Stdin"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3748",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3739",
        "resolved_owner_path": [
          "std",
          "io",
          "stdio",
          "Stdin"
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
                    "lifetime": "'static"
                  }
                ],
                "constraints": []
              }
            },
            "id": 3741,
            "path": "StdinLock"
          }
        }
      }
    },
    "verification_source": "   356:     ///\n   357:     /// # Examples\n   358:     ///\n   359:     /// ```no_run\n   360:     /// use std::io::{self, BufRead};\n   361:     ///\n   362:     /// fn main() -> io::Result<()> {\n   363:     ///     let mut buffer = String::new();\n   364:     ///     let stdin = io::stdin();\n   365:     ///     let mut handle = stdin.lock();\n   366:     ///\n   367:     ///     handle.read_line(&mut buffer)?;\n   368:     ///     Ok(())\n   369:     /// }\n   370:     /// ```\n   371:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   372:     pub fn lock(&self) -> StdinLock<'static> {\n   373:         // Locks this handle with 'static lifetime. This depends on the\n   374:         // implementation detail that the underlying `Mutex` is static.\n   375:         StdinLock { inner: self.inner.lock().unwrap_or_else(|e| e.into_inner()) }\n   376:     }\n   377: \n   378:     /// Locks this handle and reads a line of input, appending it to the specified buffer.\n   379:     ///\n   380:     /// For detailed semantics of this method, see the documentation on\n   381:     /// [`BufRead::read_line`]. In particular:\n   382:     /// * Previous content of the buffer will be preserved. To avoid appending\n   383:     ///   to the buffer, you need to [`clear`] it first.\n   384:     /// * The trailing newline character, if any, is included in the buffer.\n   385:     ///\n   386:     /// [`clear`]: String::clear\n   387:     ///\n   388:     /// # Examples",
    "nanvix_source": "   363:     /// fn main() -> io::Result<()> {\n   364:     ///     let mut buffer = String::new();\n   365:     ///     let stdin = io::stdin();\n   366:     ///     let mut handle = stdin.lock();\n   367:     ///\n   368:     ///     handle.read_line(&mut buffer)?;\n   369:     ///     Ok(())\n   370:     /// }\n   371:     /// ```\n   372:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   373:     pub fn lock(&self) -> StdinLock<'static> {\n   374:         // Locks this handle with 'static lifetime. This depends on the\n   375:         // implementation detail that the underlying `Mutex` is static.\n   376:         StdinLock { inner: self.inner.lock().unwrap_or_else(|e| e.into_inner()) }\n   377:     }\n   378: \n   379:     /// Locks this handle and reads a line of input, appending it to the specified buffer.\n   380:     ///\n   381:     /// For detailed semantics of this method, see the documentation on\n   382:     /// [`BufRead::read_line`]. In particular:\n   383:     /// * Previous content of the buffer will be preserved. To avoid appending",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Stdin::read_line",
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
      "name": "read_line",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "buf"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 3739,
            "path": "Stdin"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3748",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3739",
        "resolved_owner_path": [
          "std",
          "io",
          "stdio",
          "Stdin"
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
            "buf",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 218,
                    "path": "String"
                  }
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
                      "primitive": "usize"
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
    "verification_source": "   395:     ///     Ok(n) => {\n   396:     ///         println!(\"{n} bytes read\");\n   397:     ///         println!(\"{input}\");\n   398:     ///     }\n   399:     ///     Err(error) => println!(\"error: {error}\"),\n   400:     /// }\n   401:     /// ```\n   402:     ///\n   403:     /// You can run the example one of two ways:\n   404:     ///\n   405:     /// - Pipe some text to it, e.g., `printf foo | path/to/executable`\n   406:     /// - Give it text interactively by running the executable directly,\n   407:     ///   in which case it will wait for the Enter key to be pressed before\n   408:     ///   continuing\n   409:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   410:     #[rustc_confusables(\"get_line\")]\n   411:     pub fn read_line(&self, buf: &mut String) -> io::Result<usize> {\n   412:         self.lock().read_line(buf)\n   413:     }\n   414: \n   415:     /// Consumes this handle and returns an iterator over input lines.\n   416:     ///\n   417:     /// For detailed semantics of this method, see the documentation on\n   418:     /// [`BufRead::lines`].\n   419:     ///\n   420:     /// # Examples\n   421:     ///\n   422:     /// ```no_run\n   423:     /// use std::io;\n   424:     ///\n   425:     /// let lines = io::stdin().lines();\n   426:     /// for line in lines {\n   427:     ///     println!(\"got a line: {}\", line.unwrap());",
    "nanvix_source": "   402:     /// ```\n   403:     ///\n   404:     /// You can run the example one of two ways:\n   405:     ///\n   406:     /// - Pipe some text to it, e.g., `printf foo | path/to/executable`\n   407:     /// - Give it text interactively by running the executable directly,\n   408:     ///   in which case it will wait for the Enter key to be pressed before\n   409:     ///   continuing\n   410:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   411:     #[rustc_confusables(\"get_line\")]\n   412:     pub fn read_line(&self, buf: &mut String) -> io::Result<usize> {\n   413:         self.lock().read_line(buf)\n   414:     }\n   415: \n   416:     /// Consumes this handle and returns an iterator over input lines.\n   417:     ///\n   418:     /// For detailed semantics of this method, see the documentation on\n   419:     /// [`BufRead::lines`].\n   420:     ///\n   421:     /// # Examples\n   422:     ///",
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
