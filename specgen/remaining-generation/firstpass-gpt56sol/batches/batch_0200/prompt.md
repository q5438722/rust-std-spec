For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::BufWriter::into_parts",
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
      "name": "into_parts",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2553,
            "path": "BufWriter"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 2630,
                          "path": "Write"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3284",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2553",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufwriter",
          "BufWriter"
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
          "tuple": [
            {
              "generic": "W"
            },
            {
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
                      },
                      {
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 3283,
                            "path": "WriterPanicked"
                          }
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
          ]
        }
      }
    },
    "verification_source": "   159:     /// `into_parts` makes no attempt to flush data and cannot fail.\n   160:     ///\n   161:     /// # Examples\n   162:     ///\n   163:     /// ```\n   164:     /// use std::io::{BufWriter, Write};\n   165:     ///\n   166:     /// let mut buffer = [0u8; 10];\n   167:     /// let mut stream = BufWriter::new(buffer.as_mut());\n   168:     /// write!(stream, \"too much data\").unwrap();\n   169:     /// stream.flush().expect_err(\"it doesn't fit\");\n   170:     /// let (recovered_writer, buffered_data) = stream.into_parts();\n   171:     /// assert_eq!(recovered_writer.len(), 0);\n   172:     /// assert_eq!(&buffered_data.unwrap(), b\"ata\");\n   173:     /// ```\n   174:     #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   175:     pub fn into_parts(self) -> (W, Result<Vec<u8>, WriterPanicked>) {\n   176:         let mut this = ManuallyDrop::new(self);\n   177:         let buf = mem::take(&mut this.buf);\n   178:         let buf = if !this.panicked { Ok(buf) } else { Err(WriterPanicked { buf }) };\n   179: \n   180:         // SAFETY: double-drops are prevented by putting `this` in a ManuallyDrop that is never dropped\n   181:         let inner = unsafe { ptr::read(&this.inner) };\n   182: \n   183:         (inner, buf)\n   184:     }\n   185: }\n   186: \n   187: impl<W: ?Sized + Write> BufWriter<W> {\n   188:     /// Send data in our local buffer into the inner writer, looping as\n   189:     /// necessary until either it's all been sent or an error occurs.\n   190:     ///\n   191:     /// Because all the data in the buffer has been reported to our owner as",
    "nanvix_source": "   165:     ///\n   166:     /// let mut buffer = [0u8; 10];\n   167:     /// let mut stream = BufWriter::new(buffer.as_mut());\n   168:     /// write!(stream, \"too much data\").unwrap();\n   169:     /// stream.flush().expect_err(\"it doesn't fit\");\n   170:     /// let (recovered_writer, buffered_data) = stream.into_parts();\n   171:     /// assert_eq!(recovered_writer.len(), 0);\n   172:     /// assert_eq!(&buffered_data.unwrap(), b\"ata\");\n   173:     /// ```\n   174:     #[stable(feature = \"bufwriter_into_parts\", since = \"1.56.0\")]\n   175:     pub fn into_parts(self) -> (W, Result<Vec<u8>, WriterPanicked>) {\n   176:         let mut this = ManuallyDrop::new(self);\n   177:         let buf = mem::take(&mut this.buf);\n   178:         let buf = if !this.panicked { Ok(buf) } else { Err(WriterPanicked { buf }) };\n   179: \n   180:         // SAFETY: double-drops are prevented by putting `this` in a ManuallyDrop that is never dropped\n   181:         let inner = unsafe { ptr::read(&this.inner) };\n   182: \n   183:         (inner, buf)\n   184:     }\n   185: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::new",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2553,
            "path": "BufWriter"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 2630,
                          "path": "Write"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3284",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2553",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufwriter",
          "BufWriter"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "inner",
            {
              "generic": "W"
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2553,
            "path": "BufWriter"
          }
        }
      }
    },
    "verification_source": "    77:     inner: W,\n    78: }\n    79: \n    80: impl<W: Write> BufWriter<W> {\n    81:     /// Creates a new `BufWriter<W>` with a default buffer capacity. The default is currently 8 KiB,\n    82:     /// but may change in the future.\n    83:     ///\n    84:     /// # Examples\n    85:     ///\n    86:     /// ```no_run\n    87:     /// use std::io::BufWriter;\n    88:     /// use std::net::TcpStream;\n    89:     ///\n    90:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n    91:     /// ```\n    92:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    93:     pub fn new(inner: W) -> BufWriter<W> {\n    94:         BufWriter::with_capacity(DEFAULT_BUF_SIZE, inner)\n    95:     }\n    96: \n    97:     pub(crate) fn try_new_buffer() -> io::Result<Vec<u8>> {\n    98:         Vec::try_with_capacity(DEFAULT_BUF_SIZE).map_err(|_| {\n    99:             io::const_error!(ErrorKind::OutOfMemory, \"failed to allocate write buffer\")\n   100:         })\n   101:     }\n   102: \n   103:     pub(crate) fn with_buffer(inner: W, buf: Vec<u8>) -> Self {\n   104:         Self { inner, buf, panicked: false }\n   105:     }\n   106: \n   107:     /// Creates a new `BufWriter<W>` with at least the specified buffer capacity.\n   108:     ///\n   109:     /// # Examples",
    "nanvix_source": "    83:     ///\n    84:     /// # Examples\n    85:     ///\n    86:     /// ```no_run\n    87:     /// use std::io::BufWriter;\n    88:     /// use std::net::TcpStream;\n    89:     ///\n    90:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n    91:     /// ```\n    92:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    93:     pub fn new(inner: W) -> BufWriter<W> {\n    94:         BufWriter::with_capacity(DEFAULT_BUF_SIZE, inner)\n    95:     }\n    96: \n    97:     pub(crate) fn try_new_buffer() -> io::Result<Vec<u8>> {\n    98:         Vec::try_with_capacity(DEFAULT_BUF_SIZE).map_err(|_| {\n    99:             io::const_error!(ErrorKind::OutOfMemory, \"failed to allocate write buffer\")\n   100:         })\n   101:     }\n   102: \n   103:     pub(crate) fn with_buffer(inner: W, buf: Vec<u8>) -> Self {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::with_capacity",
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
      "name": "with_capacity",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2553,
            "path": "BufWriter"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 2630,
                          "path": "Write"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3284",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2553",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufwriter",
          "BufWriter"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "capacity",
            {
              "primitive": "usize"
            }
          ],
          [
            "inner",
            {
              "generic": "W"
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2553,
            "path": "BufWriter"
          }
        }
      }
    },
    "verification_source": "   105:     }\n   106: \n   107:     /// Creates a new `BufWriter<W>` with at least the specified buffer capacity.\n   108:     ///\n   109:     /// # Examples\n   110:     ///\n   111:     /// Creating a buffer with a buffer of at least a hundred bytes.\n   112:     ///\n   113:     /// ```no_run\n   114:     /// use std::io::BufWriter;\n   115:     /// use std::net::TcpStream;\n   116:     ///\n   117:     /// let stream = TcpStream::connect(\"127.0.0.1:34254\").unwrap();\n   118:     /// let mut buffer = BufWriter::with_capacity(100, stream);\n   119:     /// ```\n   120:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   121:     pub fn with_capacity(capacity: usize, inner: W) -> BufWriter<W> {\n   122:         BufWriter { inner, buf: Vec::with_capacity(capacity), panicked: false }\n   123:     }\n   124: \n   125:     /// Unwraps this `BufWriter<W>`, returning the underlying writer.\n   126:     ///\n   127:     /// The buffer is written out before returning the writer.\n   128:     ///\n   129:     /// # Errors\n   130:     ///\n   131:     /// An [`Err`] will be returned if an error occurs while flushing the buffer.\n   132:     ///\n   133:     /// # Examples\n   134:     ///\n   135:     /// ```no_run\n   136:     /// use std::io::BufWriter;\n   137:     /// use std::net::TcpStream;",
    "nanvix_source": "   111:     /// Creating a buffer with a buffer of at least a hundred bytes.\n   112:     ///\n   113:     /// ```no_run\n   114:     /// use std::io::BufWriter;\n   115:     /// use std::net::TcpStream;\n   116:     ///\n   117:     /// let stream = TcpStream::connect(\"127.0.0.1:34254\").unwrap();\n   118:     /// let mut buffer = BufWriter::with_capacity(100, stream);\n   119:     /// ```\n   120:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   121:     pub fn with_capacity(capacity: usize, inner: W) -> BufWriter<W> {\n   122:         BufWriter { inner, buf: Vec::with_capacity(capacity), panicked: false }\n   123:     }\n   124: \n   125:     /// Unwraps this `BufWriter<W>`, returning the underlying writer.\n   126:     ///\n   127:     /// The buffer is written out before returning the writer.\n   128:     ///\n   129:     /// # Errors\n   130:     ///\n   131:     /// An [`Err`] will be returned if an error occurs while flushing the buffer.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::IntoInnerError::error",
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
      "name": "error",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3281,
            "path": "IntoInnerError"
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
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3385",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3281",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "IntoInnerError"
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
                "id": 2710,
                "path": "Error"
              }
            }
          }
        }
      }
    },
    "verification_source": "    75:     ///\n    76:     /// // we want to get our `TcpStream` back, so let's try:\n    77:     ///\n    78:     /// let stream = match stream.into_inner() {\n    79:     ///     Ok(s) => s,\n    80:     ///     Err(e) => {\n    81:     ///         // Here, e is an IntoInnerError, let's log the inner error.\n    82:     ///         //\n    83:     ///         // We'll just 'log' to stdout for this example.\n    84:     ///         println!(\"{}\", e.error());\n    85:     ///\n    86:     ///         panic!(\"An unexpected error occurred.\");\n    87:     ///     }\n    88:     /// };\n    89:     /// ```\n    90:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    91:     pub fn error(&self) -> &Error {\n    92:         &self.1\n    93:     }\n    94: \n    95:     /// Returns the buffered writer instance which generated the error.\n    96:     ///\n    97:     /// The returned object can be used for error recovery, such as\n    98:     /// re-inspecting the buffer.\n    99:     ///\n   100:     /// # Examples\n   101:     ///\n   102:     /// ```no_run\n   103:     /// use std::io::BufWriter;\n   104:     /// use std::net::TcpStream;\n   105:     ///\n   106:     /// let mut stream = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   107:     ///",
    "nanvix_source": "    81:     ///         // Here, e is an IntoInnerError, let's log the inner error.\n    82:     ///         //\n    83:     ///         // We'll just 'log' to stdout for this example.\n    84:     ///         println!(\"{}\", e.error());\n    85:     ///\n    86:     ///         panic!(\"An unexpected error occurred.\");\n    87:     ///     }\n    88:     /// };\n    89:     /// ```\n    90:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    91:     pub fn error(&self) -> &Error {\n    92:         &self.1\n    93:     }\n    94: \n    95:     /// Returns the buffered writer instance which generated the error.\n    96:     ///\n    97:     /// The returned object can be used for error recovery, such as\n    98:     /// re-inspecting the buffer.\n    99:     ///\n   100:     /// # Examples\n   101:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::IntoInnerError::into_error",
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
      "name": "into_error",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3281,
            "path": "IntoInnerError"
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
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3385",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3281",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "IntoInnerError"
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
            "args": null,
            "id": 2710,
            "path": "Error"
          }
        }
      }
    },
    "verification_source": "   129: \n   130:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   131:     /// [`BufWriter::into_inner()`] to fail.  Unlike `error`, this can be used to\n   132:     /// obtain ownership of the underlying error.\n   133:     ///\n   134:     /// # Example\n   135:     /// ```\n   136:     /// use std::io::{BufWriter, ErrorKind, Write};\n   137:     ///\n   138:     /// let mut not_enough_space = [0u8; 10];\n   139:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());\n   140:     /// write!(stream, \"this cannot be actually written\").unwrap();\n   141:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   142:     /// let err = into_inner_err.into_error();\n   143:     /// assert_eq!(err.kind(), ErrorKind::WriteZero);\n   144:     /// ```\n   145:     #[stable(feature = \"io_into_inner_error_parts\", since = \"1.55.0\")]\n   146:     pub fn into_error(self) -> Error {\n   147:         self.1\n   148:     }\n   149: \n   150:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   151:     /// [`BufWriter::into_inner()`] to fail, and the underlying writer.\n   152:     ///\n   153:     /// This can be used to simply obtain ownership of the underlying error; it can also be used for\n   154:     /// advanced error recovery.\n   155:     ///\n   156:     /// # Example\n   157:     /// ```\n   158:     /// use std::io::{BufWriter, ErrorKind, Write};\n   159:     ///\n   160:     /// let mut not_enough_space = [0u8; 10];\n   161:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());",
    "nanvix_source": "   135:     /// ```\n   136:     /// use std::io::{BufWriter, ErrorKind, Write};\n   137:     ///\n   138:     /// let mut not_enough_space = [0u8; 10];\n   139:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());\n   140:     /// write!(stream, \"this cannot be actually written\").unwrap();\n   141:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   142:     /// let err = into_inner_err.into_error();\n   143:     /// assert_eq!(err.kind(), ErrorKind::WriteZero);\n   144:     /// ```\n   145:     #[stable(feature = \"io_into_inner_error_parts\", since = \"1.55.0\")]\n   146:     pub fn into_error(self) -> Error {\n   147:         self.1\n   148:     }\n   149: \n   150:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   151:     /// [`BufWriter::into_inner()`] to fail, and the underlying writer.\n   152:     ///\n   153:     /// This can be used to simply obtain ownership of the underlying error; it can also be used for\n   154:     /// advanced error recovery.\n   155:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::IntoInnerError::into_inner",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3281,
            "path": "IntoInnerError"
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
              "name": "W"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:3385",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3281",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "IntoInnerError"
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
          "generic": "W"
        }
      }
    },
    "verification_source": "   110:     /// // we want to get our `TcpStream` back, so let's try:\n   111:     ///\n   112:     /// let stream = match stream.into_inner() {\n   113:     ///     Ok(s) => s,\n   114:     ///     Err(e) => {\n   115:     ///         // Here, e is an IntoInnerError, let's re-examine the buffer:\n   116:     ///         let buffer = e.into_inner();\n   117:     ///\n   118:     ///         // do stuff to try to recover\n   119:     ///\n   120:     ///         // afterwards, let's just return the stream\n   121:     ///         buffer.into_inner().unwrap()\n   122:     ///     }\n   123:     /// };\n   124:     /// ```\n   125:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   126:     pub fn into_inner(self) -> W {\n   127:         self.0\n   128:     }\n   129: \n   130:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   131:     /// [`BufWriter::into_inner()`] to fail.  Unlike `error`, this can be used to\n   132:     /// obtain ownership of the underlying error.\n   133:     ///\n   134:     /// # Example\n   135:     /// ```\n   136:     /// use std::io::{BufWriter, ErrorKind, Write};\n   137:     ///\n   138:     /// let mut not_enough_space = [0u8; 10];\n   139:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());\n   140:     /// write!(stream, \"this cannot be actually written\").unwrap();\n   141:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   142:     /// let err = into_inner_err.into_error();",
    "nanvix_source": "   116:     ///         let buffer = e.into_inner();\n   117:     ///\n   118:     ///         // do stuff to try to recover\n   119:     ///\n   120:     ///         // afterwards, let's just return the stream\n   121:     ///         buffer.into_inner().unwrap()\n   122:     ///     }\n   123:     /// };\n   124:     /// ```\n   125:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   126:     pub fn into_inner(self) -> W {\n   127:         self.0\n   128:     }\n   129: \n   130:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   131:     /// [`BufWriter::into_inner()`] to fail.  Unlike `error`, this can be used to\n   132:     /// obtain ownership of the underlying error.\n   133:     ///\n   134:     /// # Example\n   135:     /// ```\n   136:     /// use std::io::{BufWriter, ErrorKind, Write};",
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
