For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::IntoInnerError::into_parts",
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
          "tuple": [
            {
              "resolved_path": {
                "args": null,
                "id": 2710,
                "path": "Error"
              }
            },
            {
              "generic": "W"
            }
          ]
        }
      }
    },
    "verification_source": "   141:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   142:     /// let err = into_inner_err.into_error();\n   143:     /// assert_eq!(err.kind(), ErrorKind::WriteZero);\n   144:     /// ```\n   145:     #[stable(feature = \"io_into_inner_error_parts\", since = \"1.55.0\")]\n   146:     pub fn into_error(self) -> Error {\n   147:         self.1\n   148:     }\n   149: \n   150:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   151:     /// [`BufWriter::into_inner()`] to fail, and the underlying writer.\n   152:     ///\n   153:     /// This can be used to simply obtain ownership of the underlying error; it can also be used for\n   154:     /// advanced error recovery.\n   155:     ///\n   156:     /// # Example\n   157:     /// ```\n   158:     /// use std::io::{BufWriter, ErrorKind, Write};\n   159:     ///\n   160:     /// let mut not_enough_space = [0u8; 10];\n   161:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());\n   162:     /// write!(stream, \"this cannot be actually written\").unwrap();\n   163:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   164:     /// let (err, recovered_writer) = into_inner_err.into_parts();\n   165:     /// assert_eq!(err.kind(), ErrorKind::WriteZero);\n   166:     /// assert_eq!(recovered_writer.buffer(), b\"t be actually written\");\n   167:     /// ```\n   168:     #[stable(feature = \"io_into_inner_error_parts\", since = \"1.55.0\")]\n   169:     pub fn into_parts(self) -> (Error, W) {\n   170:         (self.1, self.0)\n   171:     }\n   172: }\n   173: ",
    "nanvix_source": "   147:         self.1\n   148:     }\n   149: \n   150:     /// Consumes the [`IntoInnerError`] and returns the error which caused the call to\n   151:     /// [`BufWriter::into_inner()`] to fail, and the underlying writer.\n   152:     ///\n   153:     /// This can be used to simply obtain ownership of the underlying error; it can also be used for\n   154:     /// advanced error recovery.\n   155:     ///\n   156:     /// # Example\n   157:     /// ```\n   158:     /// use std::io::{BufWriter, ErrorKind, Write};\n   159:     ///\n   160:     /// let mut not_enough_space = [0u8; 10];\n   161:     /// let mut stream = BufWriter::new(not_enough_space.as_mut());\n   162:     /// write!(stream, \"this cannot be actually written\").unwrap();\n   163:     /// let into_inner_err = stream.into_inner().expect_err(\"now we discover it's too small\");\n   164:     /// let (err, recovered_writer) = into_inner_err.into_parts();\n   165:     /// assert_eq!(err.kind(), ErrorKind::WriteZero);\n   166:     /// assert_eq!(recovered_writer.buffer(), b\"t be actually written\");\n   167:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::LineWriter::get_mut",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3340,
            "path": "LineWriter"
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
        "impl_id": "std:3345",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3340",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "linewriter",
          "LineWriter"
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
              "generic": "W"
            }
          }
        }
      }
    },
    "verification_source": "   118:     /// # Examples\n   119:     ///\n   120:     /// ```no_run\n   121:     /// use std::fs::File;\n   122:     /// use std::io::LineWriter;\n   123:     ///\n   124:     /// fn main() -> std::io::Result<()> {\n   125:     ///     let file = File::create(\"poem.txt\")?;\n   126:     ///     let mut file = LineWriter::new(file);\n   127:     ///\n   128:     ///     // we can use reference just like file\n   129:     ///     let reference = file.get_mut();\n   130:     ///     Ok(())\n   131:     /// }\n   132:     /// ```\n   133:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   134:     pub fn get_mut(&mut self) -> &mut W {\n   135:         self.inner.get_mut()\n   136:     }\n   137: \n   138:     /// Unwraps this `LineWriter`, returning the underlying writer.\n   139:     ///\n   140:     /// The internal buffer is written out before returning the writer.\n   141:     ///\n   142:     /// # Errors\n   143:     ///\n   144:     /// An [`Err`] will be returned if an error occurs while flushing the buffer.\n   145:     ///\n   146:     /// # Examples\n   147:     ///\n   148:     /// ```no_run\n   149:     /// use std::fs::File;\n   150:     /// use std::io::LineWriter;",
    "nanvix_source": "   124:     /// fn main() -> std::io::Result<()> {\n   125:     ///     let file = File::create(\"poem.txt\")?;\n   126:     ///     let mut file = LineWriter::new(file);\n   127:     ///\n   128:     ///     // we can use reference just like file\n   129:     ///     let reference = file.get_mut();\n   130:     ///     Ok(())\n   131:     /// }\n   132:     /// ```\n   133:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   134:     pub fn get_mut(&mut self) -> &mut W {\n   135:         self.inner.get_mut()\n   136:     }\n   137: \n   138:     /// Unwraps this `LineWriter`, returning the underlying writer.\n   139:     ///\n   140:     /// The internal buffer is written out before returning the writer.\n   141:     ///\n   142:     /// # Errors\n   143:     ///\n   144:     /// An [`Err`] will be returned if an error occurs while flushing the buffer.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::LineWriter::get_ref",
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
                      "generic": "W"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3340,
            "path": "LineWriter"
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
                    },
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
        "impl_id": "std:3347",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3340",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "linewriter",
          "LineWriter"
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
              "generic": "W"
            }
          }
        }
      }
    },
    "verification_source": "   169:     ///\n   170:     /// # Examples\n   171:     ///\n   172:     /// ```no_run\n   173:     /// use std::fs::File;\n   174:     /// use std::io::LineWriter;\n   175:     ///\n   176:     /// fn main() -> std::io::Result<()> {\n   177:     ///     let file = File::create(\"poem.txt\")?;\n   178:     ///     let file = LineWriter::new(file);\n   179:     ///\n   180:     ///     let reference = file.get_ref();\n   181:     ///     Ok(())\n   182:     /// }\n   183:     /// ```\n   184:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   185:     pub fn get_ref(&self) -> &W {\n   186:         self.inner.get_ref()\n   187:     }\n   188: }\n   189: \n   190: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   191: impl<W: ?Sized + Write> Write for LineWriter<W> {\n   192:     fn write(&mut self, buf: &[u8]) -> io::Result<usize> {\n   193:         LineWriterShim::new(&mut self.inner).write(buf)\n   194:     }\n   195: \n   196:     fn flush(&mut self) -> io::Result<()> {\n   197:         self.inner.flush()\n   198:     }\n   199: \n   200:     fn write_vectored(&mut self, bufs: &[IoSlice<'_>]) -> io::Result<usize> {\n   201:         LineWriterShim::new(&mut self.inner).write_vectored(bufs)",
    "nanvix_source": "   175:     ///\n   176:     /// fn main() -> std::io::Result<()> {\n   177:     ///     let file = File::create(\"poem.txt\")?;\n   178:     ///     let file = LineWriter::new(file);\n   179:     ///\n   180:     ///     let reference = file.get_ref();\n   181:     ///     Ok(())\n   182:     /// }\n   183:     /// ```\n   184:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   185:     pub fn get_ref(&self) -> &W {\n   186:         self.inner.get_ref()\n   187:     }\n   188: }\n   189: \n   190: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   191: impl<W: ?Sized + Write> Write for LineWriter<W> {\n   192:     fn write(&mut self, buf: &[u8]) -> io::Result<usize> {\n   193:         LineWriterShim::new(&mut self.inner).write(buf)\n   194:     }\n   195: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::LineWriter::into_inner",
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
            "id": 3340,
            "path": "LineWriter"
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
        "impl_id": "std:3345",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3340",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "linewriter",
          "LineWriter"
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
                      "generic": "W"
                    }
                  },
                  {
                    "type": {
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
                                              "generic": "W"
                                            }
                                          }
                                        ],
                                        "constraints": []
                                      }
                                    },
                                    "id": 3340,
                                    "path": "LineWriter"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 3281,
                        "path": "IntoInnerError"
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
      }
    },
    "verification_source": "   146:     /// # Examples\n   147:     ///\n   148:     /// ```no_run\n   149:     /// use std::fs::File;\n   150:     /// use std::io::LineWriter;\n   151:     ///\n   152:     /// fn main() -> std::io::Result<()> {\n   153:     ///     let file = File::create(\"poem.txt\")?;\n   154:     ///\n   155:     ///     let writer: LineWriter<File> = LineWriter::new(file);\n   156:     ///\n   157:     ///     let file: File = writer.into_inner()?;\n   158:     ///     Ok(())\n   159:     /// }\n   160:     /// ```\n   161:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   162:     pub fn into_inner(self) -> Result<W, IntoInnerError<LineWriter<W>>> {\n   163:         self.inner.into_inner().map_err(|err| err.new_wrapped(|inner| LineWriter { inner }))\n   164:     }\n   165: }\n   166: \n   167: impl<W: ?Sized + Write> LineWriter<W> {\n   168:     /// Gets a reference to the underlying writer.\n   169:     ///\n   170:     /// # Examples\n   171:     ///\n   172:     /// ```no_run\n   173:     /// use std::fs::File;\n   174:     /// use std::io::LineWriter;\n   175:     ///\n   176:     /// fn main() -> std::io::Result<()> {\n   177:     ///     let file = File::create(\"poem.txt\")?;\n   178:     ///     let file = LineWriter::new(file);",
    "nanvix_source": "   152:     /// fn main() -> std::io::Result<()> {\n   153:     ///     let file = File::create(\"poem.txt\")?;\n   154:     ///\n   155:     ///     let writer: LineWriter<File> = LineWriter::new(file);\n   156:     ///\n   157:     ///     let file: File = writer.into_inner()?;\n   158:     ///     Ok(())\n   159:     /// }\n   160:     /// ```\n   161:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   162:     pub fn into_inner(self) -> Result<W, IntoInnerError<LineWriter<W>>> {\n   163:         self.inner.into_inner().map_err(|err| err.new_wrapped(|inner| LineWriter { inner }))\n   164:     }\n   165: }\n   166: \n   167: impl<W: ?Sized + Write> LineWriter<W> {\n   168:     /// Gets a reference to the underlying writer.\n   169:     ///\n   170:     /// # Examples\n   171:     ///\n   172:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::LineWriter::new",
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
            "id": 3340,
            "path": "LineWriter"
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
        "impl_id": "std:3345",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3340",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "linewriter",
          "LineWriter"
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
            "id": 3340,
            "path": "LineWriter"
          }
        }
      }
    },
    "verification_source": "    72: impl<W: Write> LineWriter<W> {\n    73:     /// Creates a new `LineWriter`.\n    74:     ///\n    75:     /// # Examples\n    76:     ///\n    77:     /// ```no_run\n    78:     /// use std::fs::File;\n    79:     /// use std::io::LineWriter;\n    80:     ///\n    81:     /// fn main() -> std::io::Result<()> {\n    82:     ///     let file = File::create(\"poem.txt\")?;\n    83:     ///     let file = LineWriter::new(file);\n    84:     ///     Ok(())\n    85:     /// }\n    86:     /// ```\n    87:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    88:     pub fn new(inner: W) -> LineWriter<W> {\n    89:         // Lines typically aren't that long, don't use a giant buffer\n    90:         LineWriter::with_capacity(1024, inner)\n    91:     }\n    92: \n    93:     /// Creates a new `LineWriter` with at least the specified capacity for the\n    94:     /// internal buffer.\n    95:     ///\n    96:     /// # Examples\n    97:     ///\n    98:     /// ```no_run\n    99:     /// use std::fs::File;\n   100:     /// use std::io::LineWriter;\n   101:     ///\n   102:     /// fn main() -> std::io::Result<()> {\n   103:     ///     let file = File::create(\"poem.txt\")?;\n   104:     ///     let file = LineWriter::with_capacity(100, file);",
    "nanvix_source": "    78:     /// use std::fs::File;\n    79:     /// use std::io::LineWriter;\n    80:     ///\n    81:     /// fn main() -> std::io::Result<()> {\n    82:     ///     let file = File::create(\"poem.txt\")?;\n    83:     ///     let file = LineWriter::new(file);\n    84:     ///     Ok(())\n    85:     /// }\n    86:     /// ```\n    87:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    88:     pub fn new(inner: W) -> LineWriter<W> {\n    89:         // Lines typically aren't that long, don't use a giant buffer\n    90:         LineWriter::with_capacity(1024, inner)\n    91:     }\n    92: \n    93:     /// Creates a new `LineWriter` with at least the specified capacity for the\n    94:     /// internal buffer.\n    95:     ///\n    96:     /// # Examples\n    97:     ///\n    98:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::LineWriter::with_capacity",
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
            "id": 3340,
            "path": "LineWriter"
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
        "impl_id": "std:3345",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3340",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "linewriter",
          "LineWriter"
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
            "id": 3340,
            "path": "LineWriter"
          }
        }
      }
    },
    "verification_source": "    93:     /// Creates a new `LineWriter` with at least the specified capacity for the\n    94:     /// internal buffer.\n    95:     ///\n    96:     /// # Examples\n    97:     ///\n    98:     /// ```no_run\n    99:     /// use std::fs::File;\n   100:     /// use std::io::LineWriter;\n   101:     ///\n   102:     /// fn main() -> std::io::Result<()> {\n   103:     ///     let file = File::create(\"poem.txt\")?;\n   104:     ///     let file = LineWriter::with_capacity(100, file);\n   105:     ///     Ok(())\n   106:     /// }\n   107:     /// ```\n   108:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   109:     pub fn with_capacity(capacity: usize, inner: W) -> LineWriter<W> {\n   110:         LineWriter { inner: BufWriter::with_capacity(capacity, inner) }\n   111:     }\n   112: \n   113:     /// Gets a mutable reference to the underlying writer.\n   114:     ///\n   115:     /// Caution must be taken when calling methods on the mutable reference\n   116:     /// returned as extra writes could corrupt the output stream.\n   117:     ///\n   118:     /// # Examples\n   119:     ///\n   120:     /// ```no_run\n   121:     /// use std::fs::File;\n   122:     /// use std::io::LineWriter;\n   123:     ///\n   124:     /// fn main() -> std::io::Result<()> {\n   125:     ///     let file = File::create(\"poem.txt\")?;",
    "nanvix_source": "    99:     /// use std::fs::File;\n   100:     /// use std::io::LineWriter;\n   101:     ///\n   102:     /// fn main() -> std::io::Result<()> {\n   103:     ///     let file = File::create(\"poem.txt\")?;\n   104:     ///     let file = LineWriter::with_capacity(100, file);\n   105:     ///     Ok(())\n   106:     /// }\n   107:     /// ```\n   108:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   109:     pub fn with_capacity(capacity: usize, inner: W) -> LineWriter<W> {\n   110:         LineWriter { inner: BufWriter::with_capacity(capacity, inner) }\n   111:     }\n   112: \n   113:     /// Gets a mutable reference to the underlying writer.\n   114:     ///\n   115:     /// Caution must be taken when calling methods on the mutable reference\n   116:     /// returned as extra writes could corrupt the output stream.\n   117:     ///\n   118:     /// # Examples\n   119:     ///",
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
