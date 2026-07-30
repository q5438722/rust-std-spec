For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::BufReader::with_capacity",
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
            "capacity",
            {
              "primitive": "usize"
            }
          ],
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
    "verification_source": "    86:     ///\n    87:     /// # Examples\n    88:     ///\n    89:     /// Creating a buffer with ten bytes of capacity:\n    90:     ///\n    91:     /// ```no_run\n    92:     /// use std::io::BufReader;\n    93:     /// use std::fs::File;\n    94:     ///\n    95:     /// fn main() -> std::io::Result<()> {\n    96:     ///     let f = File::open(\"log.txt\")?;\n    97:     ///     let reader = BufReader::with_capacity(10, f);\n    98:     ///     Ok(())\n    99:     /// }\n   100:     /// ```\n   101:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   102:     pub fn with_capacity(capacity: usize, inner: R) -> BufReader<R> {\n   103:         BufReader { inner, buf: Buffer::with_capacity(capacity) }\n   104:     }\n   105: }\n   106: \n   107: impl<R: Read + ?Sized> BufReader<R> {\n   108:     /// Attempt to look ahead `n` bytes.\n   109:     ///\n   110:     /// `n` must be less than or equal to `capacity`.\n   111:     ///\n   112:     /// The returned slice may be less than `n` bytes long if\n   113:     /// end of file is reached.\n   114:     ///\n   115:     /// After calling this method, you may call [`consume`](BufRead::consume)\n   116:     /// with a value less than or equal to `n` to advance over some or all of\n   117:     /// the returned bytes.\n   118:     ///",
    "nanvix_source": "    93:     /// use std::io::BufReader;\n    94:     /// use std::fs::File;\n    95:     ///\n    96:     /// fn main() -> std::io::Result<()> {\n    97:     ///     let f = File::open(\"log.txt\")?;\n    98:     ///     let reader = BufReader::with_capacity(10, f);\n    99:     ///     Ok(())\n   100:     /// }\n   101:     /// ```\n   102:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   103:     pub fn with_capacity(capacity: usize, inner: R) -> BufReader<R> {\n   104:         BufReader { inner, buf: Buffer::with_capacity(capacity) }\n   105:     }\n   106: }\n   107: \n   108: impl<R: Read + ?Sized> BufReader<R> {\n   109:     /// Attempt to look ahead `n` bytes.\n   110:     ///\n   111:     /// `n` must be less than or equal to `capacity`.\n   112:     ///\n   113:     /// The returned slice may be less than `n` bytes long if",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::buffer",
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
      "name": "buffer",
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
        "impl_id": "std:3289",
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
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "   305:     }\n   306: \n   307:     /// Returns a reference to the internally buffered data.\n   308:     ///\n   309:     /// # Examples\n   310:     ///\n   311:     /// ```no_run\n   312:     /// use std::io::BufWriter;\n   313:     /// use std::net::TcpStream;\n   314:     ///\n   315:     /// let buf_writer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   316:     ///\n   317:     /// // See how many bytes are currently buffered\n   318:     /// let bytes_buffered = buf_writer.buffer().len();\n   319:     /// ```\n   320:     #[stable(feature = \"bufreader_buffer\", since = \"1.37.0\")]\n   321:     pub fn buffer(&self) -> &[u8] {\n   322:         &self.buf\n   323:     }\n   324: \n   325:     /// Returns a mutable reference to the internal buffer.\n   326:     ///\n   327:     /// This can be used to write data directly into the buffer without triggering writers\n   328:     /// to the underlying writer.\n   329:     ///\n   330:     /// That the buffer is a `Vec` is an implementation detail.\n   331:     /// Callers should not modify the capacity as there currently is no public API to do so\n   332:     /// and thus any capacity changes would be unexpected by the user.\n   333:     pub(in crate::io) fn buffer_mut(&mut self) -> &mut Vec<u8> {\n   334:         &mut self.buf\n   335:     }\n   336: \n   337:     /// Returns the number of bytes the internal buffer can hold without flushing.",
    "nanvix_source": "   324:     /// ```no_run\n   325:     /// use std::io::BufWriter;\n   326:     /// use std::net::TcpStream;\n   327:     ///\n   328:     /// let buf_writer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   329:     ///\n   330:     /// // See how many bytes are currently buffered\n   331:     /// let bytes_buffered = buf_writer.buffer().len();\n   332:     /// ```\n   333:     #[stable(feature = \"bufreader_buffer\", since = \"1.37.0\")]\n   334:     pub fn buffer(&self) -> &[u8] {\n   335:         &self.buf\n   336:     }\n   337: \n   338:     /// Returns a mutable reference to the internal buffer.\n   339:     ///\n   340:     /// This can be used to write data directly into the buffer without triggering writers\n   341:     /// to the underlying writer.\n   342:     ///\n   343:     /// That the buffer is a `Vec` is an implementation detail.\n   344:     /// Callers should not modify the capacity as there currently is no public API to do so",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::capacity",
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
        "impl_id": "std:3289",
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
    "verification_source": "   337:     /// Returns the number of bytes the internal buffer can hold without flushing.\n   338:     ///\n   339:     /// # Examples\n   340:     ///\n   341:     /// ```no_run\n   342:     /// use std::io::BufWriter;\n   343:     /// use std::net::TcpStream;\n   344:     ///\n   345:     /// let buf_writer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   346:     ///\n   347:     /// // Check the capacity of the inner buffer\n   348:     /// let capacity = buf_writer.capacity();\n   349:     /// // Calculate how many bytes can be written without flushing\n   350:     /// let without_flush = capacity - buf_writer.buffer().len();\n   351:     /// ```\n   352:     #[stable(feature = \"buffered_io_capacity\", since = \"1.46.0\")]\n   353:     pub fn capacity(&self) -> usize {\n   354:         self.buf.capacity()\n   355:     }\n   356: \n   357:     // Ensure this function does not get inlined into `write`, so that it\n   358:     // remains inlineable and its common path remains as short as possible.\n   359:     // If this function ends up being called frequently relative to `write`,\n   360:     // it's likely a sign that the client is using an improperly sized buffer\n   361:     // or their write patterns are somewhat pathological.\n   362:     #[cold]\n   363:     #[inline(never)]\n   364:     fn write_cold(&mut self, buf: &[u8]) -> io::Result<usize> {\n   365:         if buf.len() > self.spare_capacity() {\n   366:             self.flush_buf()?;\n   367:         }\n   368: \n   369:         // Why not len > capacity? To avoid a needless trip through the buffer when the input",
    "nanvix_source": "   356:     /// use std::net::TcpStream;\n   357:     ///\n   358:     /// let buf_writer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   359:     ///\n   360:     /// // Check the capacity of the inner buffer\n   361:     /// let capacity = buf_writer.capacity();\n   362:     /// // Calculate how many bytes can be written without flushing\n   363:     /// let without_flush = capacity - buf_writer.buffer().len();\n   364:     /// ```\n   365:     #[stable(feature = \"buffered_io_capacity\", since = \"1.46.0\")]\n   366:     pub fn capacity(&self) -> usize {\n   367:         self.buf.capacity()\n   368:     }\n   369: \n   370:     // Ensure this function does not get inlined into `write`, so that it\n   371:     // remains inlineable and its common path remains as short as possible.\n   372:     // If this function ends up being called frequently relative to `write`,\n   373:     // it's likely a sign that the client is using an improperly sized buffer\n   374:     // or their write patterns are somewhat pathological.\n   375:     #[cold]\n   376:     #[inline(never)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::get_mut",
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
        "impl_id": "std:3289",
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
    "verification_source": "   287:     /// Gets a mutable reference to the underlying writer.\n   288:     ///\n   289:     /// It is inadvisable to directly write to the underlying writer.\n   290:     ///\n   291:     /// # Examples\n   292:     ///\n   293:     /// ```no_run\n   294:     /// use std::io::BufWriter;\n   295:     /// use std::net::TcpStream;\n   296:     ///\n   297:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   298:     ///\n   299:     /// // we can use reference just like buffer\n   300:     /// let reference = buffer.get_mut();\n   301:     /// ```\n   302:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   303:     pub fn get_mut(&mut self) -> &mut W {\n   304:         &mut self.inner\n   305:     }\n   306: \n   307:     /// Returns a reference to the internally buffered data.\n   308:     ///\n   309:     /// # Examples\n   310:     ///\n   311:     /// ```no_run\n   312:     /// use std::io::BufWriter;\n   313:     /// use std::net::TcpStream;\n   314:     ///\n   315:     /// let buf_writer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   316:     ///\n   317:     /// // See how many bytes are currently buffered\n   318:     /// let bytes_buffered = buf_writer.buffer().len();\n   319:     /// ```",
    "nanvix_source": "   306:     /// ```no_run\n   307:     /// use std::io::BufWriter;\n   308:     /// use std::net::TcpStream;\n   309:     ///\n   310:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   311:     ///\n   312:     /// // we can use reference just like buffer\n   313:     /// let reference = buffer.get_mut();\n   314:     /// ```\n   315:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   316:     pub fn get_mut(&mut self) -> &mut W {\n   317:         &mut self.inner\n   318:     }\n   319: \n   320:     /// Returns a reference to the internally buffered data.\n   321:     ///\n   322:     /// # Examples\n   323:     ///\n   324:     /// ```no_run\n   325:     /// use std::io::BufWriter;\n   326:     /// use std::net::TcpStream;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::get_ref",
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
        "impl_id": "std:3289",
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
    "verification_source": "   267:     }\n   268: \n   269:     /// Gets a reference to the underlying writer.\n   270:     ///\n   271:     /// # Examples\n   272:     ///\n   273:     /// ```no_run\n   274:     /// use std::io::BufWriter;\n   275:     /// use std::net::TcpStream;\n   276:     ///\n   277:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   278:     ///\n   279:     /// // we can use reference just like buffer\n   280:     /// let reference = buffer.get_ref();\n   281:     /// ```\n   282:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   283:     pub fn get_ref(&self) -> &W {\n   284:         &self.inner\n   285:     }\n   286: \n   287:     /// Gets a mutable reference to the underlying writer.\n   288:     ///\n   289:     /// It is inadvisable to directly write to the underlying writer.\n   290:     ///\n   291:     /// # Examples\n   292:     ///\n   293:     /// ```no_run\n   294:     /// use std::io::BufWriter;\n   295:     /// use std::net::TcpStream;\n   296:     ///\n   297:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   298:     ///\n   299:     /// // we can use reference just like buffer",
    "nanvix_source": "   286:     /// ```no_run\n   287:     /// use std::io::BufWriter;\n   288:     /// use std::net::TcpStream;\n   289:     ///\n   290:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   291:     ///\n   292:     /// // we can use reference just like buffer\n   293:     /// let reference = buffer.get_ref();\n   294:     /// ```\n   295:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   296:     pub fn get_ref(&self) -> &W {\n   297:         &self.inner\n   298:     }\n   299: \n   300:     /// Gets a mutable reference to the underlying writer.\n   301:     ///\n   302:     /// It is inadvisable to directly write to the underlying writer.\n   303:     ///\n   304:     /// # Examples\n   305:     ///\n   306:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufWriter::into_inner",
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
                                    "id": 2553,
                                    "path": "BufWriter"
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
    "verification_source": "   129:     /// # Errors\n   130:     ///\n   131:     /// An [`Err`] will be returned if an error occurs while flushing the buffer.\n   132:     ///\n   133:     /// # Examples\n   134:     ///\n   135:     /// ```no_run\n   136:     /// use std::io::BufWriter;\n   137:     /// use std::net::TcpStream;\n   138:     ///\n   139:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   140:     ///\n   141:     /// // unwrap the TcpStream and flush the buffer\n   142:     /// let stream = buffer.into_inner().unwrap();\n   143:     /// ```\n   144:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   145:     pub fn into_inner(mut self) -> Result<W, IntoInnerError<BufWriter<W>>> {\n   146:         match self.flush_buf() {\n   147:             Err(e) => Err(IntoInnerError::new(self, e)),\n   148:             Ok(()) => Ok(self.into_parts().0),\n   149:         }\n   150:     }\n   151: \n   152:     /// Disassembles this `BufWriter<W>`, returning the underlying writer, and any buffered but\n   153:     /// unwritten data.\n   154:     ///\n   155:     /// If the underlying writer panicked, it is not known what portion of the data was written.\n   156:     /// In this case, we return `WriterPanicked` for the buffered data (from which the buffer\n   157:     /// contents can still be recovered).\n   158:     ///\n   159:     /// `into_parts` makes no attempt to flush data and cannot fail.\n   160:     ///\n   161:     /// # Examples",
    "nanvix_source": "   135:     /// ```no_run\n   136:     /// use std::io::BufWriter;\n   137:     /// use std::net::TcpStream;\n   138:     ///\n   139:     /// let mut buffer = BufWriter::new(TcpStream::connect(\"127.0.0.1:34254\").unwrap());\n   140:     ///\n   141:     /// // unwrap the TcpStream and flush the buffer\n   142:     /// let stream = buffer.into_inner().unwrap();\n   143:     /// ```\n   144:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   145:     pub fn into_inner(mut self) -> Result<W, IntoInnerError<BufWriter<W>>> {\n   146:         match self.flush_buf() {\n   147:             Err(e) => Err(IntoInnerError::new(self, e)),\n   148:             Ok(()) => Ok(self.into_parts().0),\n   149:         }\n   150:     }\n   151: \n   152:     /// Disassembles this `BufWriter<W>`, returning the underlying writer, and any buffered but\n   153:     /// unwritten data.\n   154:     ///\n   155:     /// If the underlying writer panicked, it is not known what portion of the data was written.",
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
