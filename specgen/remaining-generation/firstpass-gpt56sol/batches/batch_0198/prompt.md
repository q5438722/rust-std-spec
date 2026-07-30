For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::BufReader::capacity",
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
      "name": "capacity",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
        "impl_id": "std:3237",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   233:     ///\n   234:     /// ```no_run\n   235:     /// use std::io::{BufReader, BufRead};\n   236:     /// use std::fs::File;\n   237:     ///\n   238:     /// fn main() -> std::io::Result<()> {\n   239:     ///     let f = File::open(\"log.txt\")?;\n   240:     ///     let mut reader = BufReader::new(f);\n   241:     ///\n   242:     ///     let capacity = reader.capacity();\n   243:     ///     let buffer = reader.fill_buf()?;\n   244:     ///     assert!(buffer.len() <= capacity);\n   245:     ///     Ok(())\n   246:     /// }\n   247:     /// ```\n   248:     #[stable(feature = \"buffered_io_capacity\", since = \"1.46.0\")]\n   249:     pub fn capacity(&self) -> usize {\n   250:         self.buf.capacity()\n   251:     }\n   252: \n   253:     /// Unwraps this `BufReader<R>`, returning the underlying reader.\n   254:     ///\n   255:     /// Note that any leftover data in the internal buffer is lost. Therefore,\n   256:     /// a following read from the underlying reader may lead to data loss.\n   257:     ///\n   258:     /// # Examples\n   259:     ///\n   260:     /// ```no_run\n   261:     /// use std::io::BufReader;\n   262:     /// use std::fs::File;\n   263:     ///\n   264:     /// fn main() -> std::io::Result<()> {\n   265:     ///     let f1 = File::open(\"log.txt\")?;",
    "nanvix_source": "   240:     ///     let f = File::open(\"log.txt\")?;\n   241:     ///     let mut reader = BufReader::new(f);\n   242:     ///\n   243:     ///     let capacity = reader.capacity();\n   244:     ///     let buffer = reader.fill_buf()?;\n   245:     ///     assert!(buffer.len() <= capacity);\n   246:     ///     Ok(())\n   247:     /// }\n   248:     /// ```\n   249:     #[stable(feature = \"buffered_io_capacity\", since = \"1.46.0\")]\n   250:     pub fn capacity(&self) -> usize {\n   251:         self.buf.capacity()\n   252:     }\n   253: \n   254:     /// Unwraps this `BufReader<R>`, returning the underlying reader.\n   255:     ///\n   256:     /// Note that any leftover data in the internal buffer is lost. Therefore,\n   257:     /// a following read from the underlying reader may lead to data loss.\n   258:     ///\n   259:     /// # Examples\n   260:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::get_mut",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
        "impl_id": "std:3237",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
              "generic": "R"
            }
          }
        }
      }
    },
    "verification_source": "   182:     ///\n   183:     /// # Examples\n   184:     ///\n   185:     /// ```no_run\n   186:     /// use std::io::BufReader;\n   187:     /// use std::fs::File;\n   188:     ///\n   189:     /// fn main() -> std::io::Result<()> {\n   190:     ///     let f1 = File::open(\"log.txt\")?;\n   191:     ///     let mut reader = BufReader::new(f1);\n   192:     ///\n   193:     ///     let f2 = reader.get_mut();\n   194:     ///     Ok(())\n   195:     /// }\n   196:     /// ```\n   197:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   198:     pub fn get_mut(&mut self) -> &mut R {\n   199:         &mut self.inner\n   200:     }\n   201: \n   202:     /// Returns a reference to the internally buffered data.\n   203:     ///\n   204:     /// Unlike [`fill_buf`], this will not attempt to fill the buffer if it is empty.\n   205:     ///\n   206:     /// [`fill_buf`]: BufRead::fill_buf\n   207:     ///\n   208:     /// # Examples\n   209:     ///\n   210:     /// ```no_run\n   211:     /// use std::io::{BufReader, BufRead};\n   212:     /// use std::fs::File;\n   213:     ///\n   214:     /// fn main() -> std::io::Result<()> {",
    "nanvix_source": "   189:     ///\n   190:     /// fn main() -> std::io::Result<()> {\n   191:     ///     let f1 = File::open(\"log.txt\")?;\n   192:     ///     let mut reader = BufReader::new(f1);\n   193:     ///\n   194:     ///     let f2 = reader.get_mut();\n   195:     ///     Ok(())\n   196:     /// }\n   197:     /// ```\n   198:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   199:     pub fn get_mut(&mut self) -> &mut R {\n   200:         &mut self.inner\n   201:     }\n   202: \n   203:     /// Returns a reference to the internally buffered data.\n   204:     ///\n   205:     /// Unlike [`fill_buf`], this will not attempt to fill the buffer if it is empty.\n   206:     ///\n   207:     /// [`fill_buf`]: BufRead::fill_buf\n   208:     ///\n   209:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::get_ref",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
        "impl_id": "std:3237",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
              "generic": "R"
            }
          }
        }
      }
    },
    "verification_source": "   159:     ///\n   160:     /// # Examples\n   161:     ///\n   162:     /// ```no_run\n   163:     /// use std::io::BufReader;\n   164:     /// use std::fs::File;\n   165:     ///\n   166:     /// fn main() -> std::io::Result<()> {\n   167:     ///     let f1 = File::open(\"log.txt\")?;\n   168:     ///     let reader = BufReader::new(f1);\n   169:     ///\n   170:     ///     let f2 = reader.get_ref();\n   171:     ///     Ok(())\n   172:     /// }\n   173:     /// ```\n   174:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   175:     pub fn get_ref(&self) -> &R {\n   176:         &self.inner\n   177:     }\n   178: \n   179:     /// Gets a mutable reference to the underlying reader.\n   180:     ///\n   181:     /// It is inadvisable to directly read from the underlying reader.\n   182:     ///\n   183:     /// # Examples\n   184:     ///\n   185:     /// ```no_run\n   186:     /// use std::io::BufReader;\n   187:     /// use std::fs::File;\n   188:     ///\n   189:     /// fn main() -> std::io::Result<()> {\n   190:     ///     let f1 = File::open(\"log.txt\")?;\n   191:     ///     let mut reader = BufReader::new(f1);",
    "nanvix_source": "   166:     ///\n   167:     /// fn main() -> std::io::Result<()> {\n   168:     ///     let f1 = File::open(\"log.txt\")?;\n   169:     ///     let reader = BufReader::new(f1);\n   170:     ///\n   171:     ///     let f2 = reader.get_ref();\n   172:     ///     Ok(())\n   173:     /// }\n   174:     /// ```\n   175:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   176:     pub fn get_ref(&self) -> &R {\n   177:         &self.inner\n   178:     }\n   179: \n   180:     /// Gets a mutable reference to the underlying reader.\n   181:     ///\n   182:     /// It is inadvisable to directly read from the underlying reader.\n   183:     ///\n   184:     /// # Examples\n   185:     ///\n   186:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::into_inner",
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
          }
        ]
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
        "impl_id": "std:3237",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
          "generic": "R"
        }
      }
    },
    "verification_source": "   257:     ///\n   258:     /// # Examples\n   259:     ///\n   260:     /// ```no_run\n   261:     /// use std::io::BufReader;\n   262:     /// use std::fs::File;\n   263:     ///\n   264:     /// fn main() -> std::io::Result<()> {\n   265:     ///     let f1 = File::open(\"log.txt\")?;\n   266:     ///     let reader = BufReader::new(f1);\n   267:     ///\n   268:     ///     let f2 = reader.into_inner();\n   269:     ///     Ok(())\n   270:     /// }\n   271:     /// ```\n   272:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   273:     pub fn into_inner(self) -> R\n   274:     where\n   275:         R: Sized,\n   276:     {\n   277:         self.inner\n   278:     }\n   279: \n   280:     /// Invalidates all data in the internal buffer.\n   281:     #[inline]\n   282:     pub(in crate::io) fn discard_buffer(&mut self) {\n   283:         self.buf.discard_buffer()\n   284:     }\n   285: }\n   286: \n   287: // This is only used by a test which asserts that the initialization-tracking is correct.\n   288: #[cfg(test)]\n   289: impl<R: ?Sized> BufReader<R> {",
    "nanvix_source": "   264:     ///\n   265:     /// fn main() -> std::io::Result<()> {\n   266:     ///     let f1 = File::open(\"log.txt\")?;\n   267:     ///     let reader = BufReader::new(f1);\n   268:     ///\n   269:     ///     let f2 = reader.into_inner();\n   270:     ///     Ok(())\n   271:     /// }\n   272:     /// ```\n   273:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   274:     pub fn into_inner(self) -> R\n   275:     where\n   276:         R: Sized,\n   277:     {\n   278:         self.inner\n   279:     }\n   280: \n   281:     /// Invalidates all data in the internal buffer.\n   282:     #[inline]\n   283:     pub(in crate::io) fn discard_buffer(&mut self) {\n   284:         self.buf.discard_buffer()",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::new",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
        "impl_id": "std:3228",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "inner",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
          }
        }
      }
    },
    "verification_source": "    57:     /// Creates a new `BufReader<R>` with a default buffer capacity. The default is currently 8 KiB,\n    58:     /// but may change in the future.\n    59:     ///\n    60:     /// # Examples\n    61:     ///\n    62:     /// ```no_run\n    63:     /// use std::io::BufReader;\n    64:     /// use std::fs::File;\n    65:     ///\n    66:     /// fn main() -> std::io::Result<()> {\n    67:     ///     let f = File::open(\"log.txt\")?;\n    68:     ///     let reader = BufReader::new(f);\n    69:     ///     Ok(())\n    70:     /// }\n    71:     /// ```\n    72:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    73:     pub fn new(inner: R) -> BufReader<R> {\n    74:         BufReader::with_capacity(DEFAULT_BUF_SIZE, inner)\n    75:     }\n    76: \n    77:     pub(crate) fn try_new_buffer() -> io::Result<Buffer> {\n    78:         Buffer::try_with_capacity(DEFAULT_BUF_SIZE)\n    79:     }\n    80: \n    81:     pub(crate) fn with_buffer(inner: R, buf: Buffer) -> Self {\n    82:         Self { inner, buf }\n    83:     }\n    84: \n    85:     /// Creates a new `BufReader<R>` with the specified buffer capacity.\n    86:     ///\n    87:     /// # Examples\n    88:     ///\n    89:     /// Creating a buffer with ten bytes of capacity:",
    "nanvix_source": "    64:     /// use std::io::BufReader;\n    65:     /// use std::fs::File;\n    66:     ///\n    67:     /// fn main() -> std::io::Result<()> {\n    68:     ///     let f = File::open(\"log.txt\")?;\n    69:     ///     let reader = BufReader::new(f);\n    70:     ///     Ok(())\n    71:     /// }\n    72:     /// ```\n    73:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    74:     pub fn new(inner: R) -> BufReader<R> {\n    75:         BufReader::with_capacity(DEFAULT_BUF_SIZE, inner)\n    76:     }\n    77: \n    78:     pub(crate) fn try_new_buffer() -> io::Result<Buffer> {\n    79:         Buffer::try_with_capacity(DEFAULT_BUF_SIZE)\n    80:     }\n    81: \n    82:     pub(crate) fn with_buffer(inner: R, buf: Buffer) -> Self {\n    83:         Self { inner, buf }\n    84:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::seek_relative",
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
      "name": "seek_relative",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
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
                          "id": 2550,
                          "path": "Seek"
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
        "impl_id": "std:3239",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
          ],
          [
            "offset",
            {
              "primitive": "i64"
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
                      "tuple": []
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
    "verification_source": "   286: \n   287: // This is only used by a test which asserts that the initialization-tracking is correct.\n   288: #[cfg(test)]\n   289: impl<R: ?Sized> BufReader<R> {\n   290:     #[allow(missing_docs)]\n   291:     pub fn initialized(&self) -> bool {\n   292:         self.buf.initialized()\n   293:     }\n   294: }\n   295: \n   296: impl<R: ?Sized + Seek> BufReader<R> {\n   297:     /// Seeks relative to the current position. If the new position lies within the buffer,\n   298:     /// the buffer will not be flushed, allowing for more efficient seeks.\n   299:     /// This method does not return the location of the underlying reader, so the caller\n   300:     /// must track this information themselves if it is required.\n   301:     #[stable(feature = \"bufreader_seek_relative\", since = \"1.53.0\")]\n   302:     pub fn seek_relative(&mut self, offset: i64) -> io::Result<()> {\n   303:         let pos = self.buf.pos() as u64;\n   304:         if offset < 0 {\n   305:             if let Some(_) = pos.checked_sub((-offset) as u64) {\n   306:                 self.buf.unconsume((-offset) as usize);\n   307:                 return Ok(());\n   308:             }\n   309:         } else if let Some(new_pos) = pos.checked_add(offset as u64) {\n   310:             if new_pos <= self.buf.filled() as u64 {\n   311:                 self.buf.consume(offset as usize);\n   312:                 return Ok(());\n   313:             }\n   314:         }\n   315: \n   316:         self.seek(SeekFrom::Current(offset)).map(drop)\n   317:     }\n   318: }",
    "nanvix_source": "   293:         self.buf.initialized()\n   294:     }\n   295: }\n   296: \n   297: impl<R: ?Sized + Seek> BufReader<R> {\n   298:     /// Seeks relative to the current position. If the new position lies within the buffer,\n   299:     /// the buffer will not be flushed, allowing for more efficient seeks.\n   300:     /// This method does not return the location of the underlying reader, so the caller\n   301:     /// must track this information themselves if it is required.\n   302:     #[stable(feature = \"bufreader_seek_relative\", since = \"1.53.0\")]\n   303:     pub fn seek_relative(&mut self, offset: i64) -> io::Result<()> {\n   304:         let pos = self.buf.pos() as u64;\n   305:         if offset < 0 {\n   306:             if let Some(_) = pos.checked_sub((-offset) as u64) {\n   307:                 self.buf.unconsume((-offset) as usize);\n   308:                 return Ok(());\n   309:             }\n   310:         } else if let Some(new_pos) = pos.checked_add(offset as u64) {\n   311:             if new_pos <= self.buf.filled() as u64 {\n   312:                 self.buf.consume(offset as usize);\n   313:                 return Ok(());",
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
