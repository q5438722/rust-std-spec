For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::Stdout::lock",
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
            "id": 3846,
            "path": "Stdout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3848",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3846",
        "resolved_owner_path": [
          "std",
          "io",
          "stdio",
          "Stdout"
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
            "id": 3847,
            "path": "StdoutLock"
          }
        }
      }
    },
    "verification_source": "   749:     /// returned guard also implements the `Write` trait for writing data.\n   750:     ///\n   751:     /// # Examples\n   752:     ///\n   753:     /// ```no_run\n   754:     /// use std::io::{self, Write};\n   755:     ///\n   756:     /// fn main() -> io::Result<()> {\n   757:     ///     let mut stdout = io::stdout().lock();\n   758:     ///\n   759:     ///     stdout.write_all(b\"hello world\")?;\n   760:     ///\n   761:     ///     Ok(())\n   762:     /// }\n   763:     /// ```\n   764:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   765:     pub fn lock(&self) -> StdoutLock<'static> {\n   766:         // Locks this handle with 'static lifetime. This depends on the\n   767:         // implementation detail that the underlying `ReentrantMutex` is\n   768:         // static.\n   769:         StdoutLock { inner: self.inner.lock() }\n   770:     }\n   771: }\n   772: \n   773: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   774: impl UnwindSafe for Stdout {}\n   775: \n   776: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   777: impl RefUnwindSafe for Stdout {}\n   778: \n   779: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   780: impl fmt::Debug for Stdout {\n   781:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "nanvix_source": "   756:     ///\n   757:     /// fn main() -> io::Result<()> {\n   758:     ///     let mut stdout = io::stdout().lock();\n   759:     ///\n   760:     ///     stdout.write_all(b\"hello world\")?;\n   761:     ///\n   762:     ///     Ok(())\n   763:     /// }\n   764:     /// ```\n   765:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   766:     pub fn lock(&self) -> StdoutLock<'static> {\n   767:         // Locks this handle with 'static lifetime. This depends on the\n   768:         // implementation detail that the underlying `ReentrantMutex` is\n   769:         // static.\n   770:         StdoutLock { inner: self.inner.lock() }\n   771:     }\n   772: }\n   773: \n   774: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   775: impl UnwindSafe for Stdout {}\n   776: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::WriterPanicked::into_inner",
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
            "args": null,
            "id": 3283,
            "path": "WriterPanicked"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3317",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3283",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufwriter",
          "WriterPanicked"
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
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 222,
            "path": "Vec"
          }
        }
      }
    },
    "verification_source": "   476: ///     stream.flush().unwrap()\n   477: /// }));\n   478: /// assert!(result.is_err());\n   479: /// let (recovered_writer, buffered_data) = stream.into_parts();\n   480: /// assert!(matches!(recovered_writer, PanickingWriter));\n   481: /// assert_eq!(buffered_data.unwrap_err().into_inner(), b\"some data\");\n   482: /// ```\n   483: pub struct WriterPanicked {\n   484:     buf: Vec<u8>,\n   485: }\n   486: \n   487: impl WriterPanicked {\n   488:     /// Returns the perhaps-unwritten data.  Some of this data may have been written by the\n   489:     /// panicking call(s) to the underlying writer, so simply writing it again is not a good idea.\n   490:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   491:     #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   492:     pub fn into_inner(self) -> Vec<u8> {\n   493:         self.buf\n   494:     }\n   495: }\n   496: \n   497: #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   498: impl error::Error for WriterPanicked {}\n   499: \n   500: #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   501: impl fmt::Display for WriterPanicked {\n   502:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   503:         \"BufWriter inner writer panicked, what data remains unwritten is not known\".fmt(f)\n   504:     }\n   505: }\n   506: \n   507: #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   508: impl fmt::Debug for WriterPanicked {",
    "nanvix_source": "   495: /// ```\n   496: pub struct WriterPanicked {\n   497:     buf: Vec<u8>,\n   498: }\n   499: \n   500: impl WriterPanicked {\n   501:     /// Returns the perhaps-unwritten data.  Some of this data may have been written by the\n   502:     /// panicking call(s) to the underlying writer, so simply writing it again is not a good idea.\n   503:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   504:     #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   505:     pub fn into_inner(self) -> Vec<u8> {\n   506:         self.buf\n   507:     }\n   508: }\n   509: \n   510: #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   511: impl error::Error for WriterPanicked {}\n   512: \n   513: #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   514: impl fmt::Display for WriterPanicked {\n   515:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::copy",
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
            "name": "R"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "W"
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
                      "args": null,
                      "id": 2620,
                      "path": "Read"
                    }
                  }
                },
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
              "generic_params": [],
              "type": {
                "generic": "R"
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
                      "id": 2630,
                      "path": "Write"
                    }
                  }
                },
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
              "generic_params": [],
              "type": {
                "generic": "W"
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
      "name": "copy",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "reader",
          "writer"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "reader",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "R"
                }
              }
            }
          ],
          [
            "writer",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "W"
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
                      "primitive": "u64"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "super::Result"
          }
        }
      }
    },
    "verification_source": "    46: ///\n    47: ///     assert_eq!(&b\"hello\"[..], &writer[..]);\n    48: ///     Ok(())\n    49: /// }\n    50: /// ```\n    51: ///\n    52: /// # Platform-specific behavior\n    53: ///\n    54: /// On Linux (including Android), this function uses `copy_file_range(2)`,\n    55: /// `sendfile(2)` or `splice(2)` syscalls to move data directly between file\n    56: /// descriptors if possible.\n    57: ///\n    58: /// Note that platform-specific behavior [may change in the future][changes].\n    59: ///\n    60: /// [changes]: crate::io#platform-specific-behavior\n    61: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    62: pub fn copy<R: ?Sized, W: ?Sized>(reader: &mut R, writer: &mut W) -> Result<u64>\n    63: where\n    64:     R: Read,\n    65:     W: Write,\n    66: {\n    67:     match kernel_copy(reader, writer)? {\n    68:         CopyState::Ended(copied) => Ok(copied),\n    69:         CopyState::Fallback(copied) => {\n    70:             generic_copy(reader, writer).map(|additional| copied + additional)\n    71:         }\n    72:     }\n    73: }\n    74: \n    75: /// The userspace read-write-loop implementation of `io::copy` that is used when\n    76: /// OS-specific specializations for copy offloading are not available or not applicable.\n    77: fn generic_copy<R: ?Sized, W: ?Sized>(reader: &mut R, writer: &mut W) -> Result<u64>\n    78: where",
    "nanvix_source": "    52: /// # Platform-specific behavior\n    53: ///\n    54: /// On Linux (including Android), this function uses `copy_file_range(2)`,\n    55: /// `sendfile(2)` or `splice(2)` syscalls to move data directly between file\n    56: /// descriptors if possible.\n    57: ///\n    58: /// Note that platform-specific behavior [may change in the future][changes].\n    59: ///\n    60: /// [changes]: crate::io#platform-specific-behavior\n    61: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    62: pub fn copy<R: ?Sized, W: ?Sized>(reader: &mut R, writer: &mut W) -> Result<u64>\n    63: where\n    64:     R: Read,\n    65:     W: Write,\n    66: {\n    67:     match kernel_copy(reader, writer)? {\n    68:         CopyState::Ended(copied) => Ok(copied),\n    69:         CopyState::Fallback(copied) => {\n    70:             generic_copy(reader, writer).map(|additional| copied + additional)\n    71:         }\n    72:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::pipe",
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
      "name": "pipe",
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
                      "tuple": [
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 3617,
                            "path": "PipeReader"
                          }
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 3618,
                            "path": "PipeWriter"
                          }
                        }
                      ]
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
    "verification_source": "    69: /// drop(echo_command);\n    70: ///\n    71: /// let mut buf = String::new();\n    72: /// // Block until `cat` closes its stdout (a pong writer).\n    73: /// pong_reader.read_to_string(&mut buf)?;\n    74: /// assert_eq!(&buf, \"hello\");\n    75: ///\n    76: /// // At this point we know `cat` has exited, but we still need to wait to clean up the \"zombie\".\n    77: /// echo_child.wait()?;\n    78: /// # Ok(())\n    79: /// # }\n    80: /// ```\n    81: /// [changes]: io#platform-specific-behavior\n    82: /// [man page]: https://man7.org/linux/man-pages/man7/pipe.7.html\n    83: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n    84: #[inline]\n    85: pub fn pipe() -> io::Result<(PipeReader, PipeWriter)> {\n    86:     imp::pipe().map(|(reader, writer)| (PipeReader(reader), PipeWriter(writer)))\n    87: }\n    88: \n    89: /// Read end of an anonymous pipe.\n    90: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n    91: #[derive(Debug)]\n    92: pub struct PipeReader(pub(crate) imp::Pipe);\n    93: \n    94: /// Write end of an anonymous pipe.\n    95: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n    96: #[derive(Debug)]\n    97: pub struct PipeWriter(pub(crate) imp::Pipe);\n    98: \n    99: impl FromInner<imp::Pipe> for PipeReader {\n   100:     fn from_inner(inner: imp::Pipe) -> Self {\n   101:         Self(inner)",
    "nanvix_source": "    73: ///\n    74: /// // At this point we know `cat` has exited, but we still need to wait to clean up the \"zombie\".\n    75: /// echo_child.wait()?;\n    76: /// # Ok(())\n    77: /// # }\n    78: /// ```\n    79: /// [changes]: io#platform-specific-behavior\n    80: /// [man page]: https://man7.org/linux/man-pages/man7/pipe.7.html\n    81: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n    82: #[inline]\n    83: pub fn pipe() -> io::Result<(PipeReader, PipeWriter)> {\n    84:     imp::pipe().map(|(reader, writer)| (PipeReader(reader), PipeWriter(writer)))\n    85: }\n    86: \n    87: /// Read end of an anonymous pipe.\n    88: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]\n    89: #[derive(Debug)]\n    90: pub struct PipeReader(pub(crate) imp::Pipe);\n    91: \n    92: /// Write end of an anonymous pipe.\n    93: #[stable(feature = \"anonymous_pipe\", since = \"1.87.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::read_to_string",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 2620,
                        "path": "Read"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
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
      "name": "read_to_string",
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
            "reader",
            {
              "generic": "R"
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
                        "id": 218,
                        "path": "String"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1312: /// ```\n  1313: ///\n  1314: /// # Usage Notes\n  1315: ///\n  1316: /// `read_to_string` attempts to read a source until EOF, but many sources are continuous streams\n  1317: /// that do not send EOF. In these cases, `read_to_string` will block indefinitely. Standard input\n  1318: /// is one such stream which may be finite if piped, but is typically continuous. For example,\n  1319: /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n  1320: /// Reading user input or running programs that remain open indefinitely will never terminate\n  1321: /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n  1322: ///\n  1323: /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n  1324: ///\n  1325: ///[`read`]: Read::read\n  1326: ///\n  1327: #[stable(feature = \"io_read_to_string\", since = \"1.65.0\")]\n  1328: pub fn read_to_string<R: Read>(mut reader: R) -> Result<String> {\n  1329:     let mut buf = String::new();\n  1330:     reader.read_to_string(&mut buf)?;\n  1331:     Ok(buf)\n  1332: }\n  1333: \n  1334: /// A buffer type used with `Read::read_vectored`.\n  1335: ///\n  1336: /// It is semantically a wrapper around a `&mut [u8]`, but is guaranteed to be\n  1337: /// ABI compatible with the `iovec` type on Unix platforms and `WSABUF` on\n  1338: /// Windows.\n  1339: #[stable(feature = \"iovec\", since = \"1.36.0\")]\n  1340: #[repr(transparent)]\n  1341: pub struct IoSliceMut<'a>(sys::io::IoSliceMut<'a>);\n  1342: \n  1343: #[stable(feature = \"iovec_send_sync\", since = \"1.44.0\")]\n  1344: unsafe impl<'a> Send for IoSliceMut<'a> {}",
    "nanvix_source": "  1390: /// is one such stream which may be finite if piped, but is typically continuous. For example,\n  1391: /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n  1392: /// Reading user input or running programs that remain open indefinitely will never terminate\n  1393: /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n  1394: ///\n  1395: /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n  1396: ///\n  1397: ///[`read`]: Read::read\n  1398: ///\n  1399: #[stable(feature = \"io_read_to_string\", since = \"1.65.0\")]\n  1400: pub fn read_to_string<R: Read>(mut reader: R) -> Result<String> {\n  1401:     let mut buf = String::new();\n  1402:     reader.read_to_string(&mut buf)?;\n  1403:     Ok(buf)\n  1404: }\n  1405: \n  1406: /// A trait for objects which are byte-oriented sinks.\n  1407: ///\n  1408: /// Implementors of the `Write` trait are sometimes called 'writers'.\n  1409: ///\n  1410: /// Writers are defined by two required methods, [`write`] and [`flush`]:",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::stderr",
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
      "name": "stderr",
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
            "id": 3937,
            "path": "Stderr"
          }
        }
      }
    },
    "verification_source": "   949: ///\n   950: /// ```no_run\n   951: /// use std::io::{self, Write};\n   952: ///\n   953: /// fn main() -> io::Result<()> {\n   954: ///     let stderr = io::stderr();\n   955: ///     let mut handle = stderr.lock();\n   956: ///\n   957: ///     handle.write_all(b\"hello world\")?;\n   958: ///\n   959: ///     Ok(())\n   960: /// }\n   961: /// ```\n   962: #[must_use]\n   963: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   964: #[cfg_attr(not(test), rustc_diagnostic_item = \"io_stderr\")]\n   965: pub fn stderr() -> Stderr {\n   966:     // Note that unlike `stdout()` we don't use `at_exit` here to register a\n   967:     // destructor. Stderr is not buffered, so there's no need to run a\n   968:     // destructor for flushing the buffer\n   969:     static INSTANCE: ReentrantLock<RefCell<StderrRaw>> =\n   970:         ReentrantLock::new(RefCell::new(stderr_raw()));\n   971: \n   972:     Stderr { inner: &INSTANCE }\n   973: }\n   974: \n   975: impl Stderr {\n   976:     /// Locks this handle to the standard error stream, returning a writable\n   977:     /// guard.\n   978:     ///\n   979:     /// The lock is released when the returned lock goes out of scope. The\n   980:     /// returned guard also implements the [`Write`] trait for writing data.\n   981:     ///",
    "nanvix_source": "   956: ///     let mut handle = stderr.lock();\n   957: ///\n   958: ///     handle.write_all(b\"hello world\")?;\n   959: ///\n   960: ///     Ok(())\n   961: /// }\n   962: /// ```\n   963: #[must_use]\n   964: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   965: #[cfg_attr(not(test), rustc_diagnostic_item = \"io_stderr\")]\n   966: pub fn stderr() -> Stderr {\n   967:     // Note that unlike `stdout()` we don't use `at_exit` here to register a\n   968:     // destructor. Stderr is not buffered, so there's no need to run a\n   969:     // destructor for flushing the buffer\n   970:     static INSTANCE: ReentrantLock<RefCell<StderrRaw>> =\n   971:         ReentrantLock::new(RefCell::new(stderr_raw()));\n   972: \n   973:     Stderr { inner: &INSTANCE }\n   974: }\n   975: \n   976: impl Stderr {",
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
