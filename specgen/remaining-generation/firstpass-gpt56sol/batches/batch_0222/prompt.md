For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixStream::set_read_timeout",
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
      "name": "set_read_timeout",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
            "timeout",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 513,
                            "path": "Duration"
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
    "verification_source": "   292:     /// method:\n   293:     ///\n   294:     /// ```no_run\n   295:     /// use std::io;\n   296:     /// use std::os::unix::net::UnixStream;\n   297:     /// use std::time::Duration;\n   298:     ///\n   299:     /// fn main() -> std::io::Result<()> {\n   300:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   301:     ///     let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   302:     ///     let err = result.unwrap_err();\n   303:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   304:     ///     Ok(())\n   305:     /// }\n   306:     /// ```\n   307:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   308:     pub fn set_read_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   309:         self.0.set_timeout(timeout, libc::SO_RCVTIMEO)\n   310:     }\n   311: \n   312:     /// Sets the write timeout for the socket.\n   313:     ///\n   314:     /// If the provided value is [`None`], then [`write`] calls will block\n   315:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   316:     /// passed to this method.\n   317:     ///\n   318:     /// [`read`]: io::Read::read\n   319:     ///\n   320:     /// # Examples\n   321:     ///\n   322:     /// ```no_run\n   323:     /// use std::os::unix::net::UnixStream;\n   324:     /// use std::time::Duration;",
    "nanvix_source": "   295:     ///\n   296:     /// fn main() -> std::io::Result<()> {\n   297:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   298:     ///     let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   299:     ///     let err = result.unwrap_err();\n   300:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   301:     ///     Ok(())\n   302:     /// }\n   303:     /// ```\n   304:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   305:     pub fn set_read_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   306:         self.0.set_timeout(timeout, libc::SO_RCVTIMEO)\n   307:     }\n   308: \n   309:     /// Sets the write timeout for the socket.\n   310:     ///\n   311:     /// If the provided value is [`None`], then [`write`] calls will block\n   312:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   313:     /// passed to this method.\n   314:     ///\n   315:     /// [`read`]: io::Read::read",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::set_write_timeout",
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
      "name": "set_write_timeout",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
            "timeout",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 513,
                            "path": "Duration"
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
    "verification_source": "   335:     /// method:\n   336:     ///\n   337:     /// ```no_run\n   338:     /// use std::io;\n   339:     /// use std::os::unix::net::UnixStream;\n   340:     /// use std::time::Duration;\n   341:     ///\n   342:     /// fn main() -> std::io::Result<()> {\n   343:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   344:     ///     let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   345:     ///     let err = result.unwrap_err();\n   346:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   347:     ///     Ok(())\n   348:     /// }\n   349:     /// ```\n   350:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   351:     pub fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   352:         self.0.set_timeout(timeout, libc::SO_SNDTIMEO)\n   353:     }\n   354: \n   355:     /// Returns the read timeout of this socket.\n   356:     ///\n   357:     /// # Examples\n   358:     ///\n   359:     /// ```no_run\n   360:     /// use std::os::unix::net::UnixStream;\n   361:     /// use std::time::Duration;\n   362:     ///\n   363:     /// fn main() -> std::io::Result<()> {\n   364:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   365:     ///     socket.set_read_timeout(Some(Duration::new(1, 0))).expect(\"Couldn't set read timeout\");\n   366:     ///     assert_eq!(socket.read_timeout()?, Some(Duration::new(1, 0)));\n   367:     ///     Ok(())",
    "nanvix_source": "   338:     ///\n   339:     /// fn main() -> std::io::Result<()> {\n   340:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   341:     ///     let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   342:     ///     let err = result.unwrap_err();\n   343:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   344:     ///     Ok(())\n   345:     /// }\n   346:     /// ```\n   347:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   348:     pub fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   349:         self.0.set_timeout(timeout, libc::SO_SNDTIMEO)\n   350:     }\n   351: \n   352:     /// Returns the read timeout of this socket.\n   353:     ///\n   354:     /// # Examples\n   355:     ///\n   356:     /// ```no_run\n   357:     /// use std::os::unix::net::UnixStream;\n   358:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::shutdown",
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
      "name": "shutdown",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
            "how",
            {
              "resolved_path": {
                "args": null,
                "id": 4727,
                "path": "Shutdown"
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
    "verification_source": "   465:     /// specified portions to immediately return with an appropriate value\n   466:     /// (see the documentation of [`Shutdown`]).\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```no_run\n   471:     /// use std::os::unix::net::UnixStream;\n   472:     /// use std::net::Shutdown;\n   473:     ///\n   474:     /// fn main() -> std::io::Result<()> {\n   475:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   476:     ///     socket.shutdown(Shutdown::Both).expect(\"shutdown function failed\");\n   477:     ///     Ok(())\n   478:     /// }\n   479:     /// ```\n   480:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   481:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   482:         self.0.shutdown(how)\n   483:     }\n   484: \n   485:     /// Receives data on the socket from the remote address to which it is\n   486:     /// connected, without removing that data from the queue. On success,\n   487:     /// returns the number of bytes peeked.\n   488:     ///\n   489:     /// Successive calls return the same data. This is accomplished by passing\n   490:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   491:     ///\n   492:     /// # Examples\n   493:     ///\n   494:     /// ```no_run\n   495:     /// #![feature(unix_socket_peek)]\n   496:     ///\n   497:     /// use std::os::unix::net::UnixStream;",
    "nanvix_source": "   468:     /// use std::os::unix::net::UnixStream;\n   469:     /// use std::net::Shutdown;\n   470:     ///\n   471:     /// fn main() -> std::io::Result<()> {\n   472:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   473:     ///     socket.shutdown(Shutdown::Both).expect(\"shutdown function failed\");\n   474:     ///     Ok(())\n   475:     /// }\n   476:     /// ```\n   477:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   478:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   479:         self.0.shutdown(how)\n   480:     }\n   481: \n   482:     /// Receives data on the socket from the remote address to which it is\n   483:     /// connected, without removing that data from the queue. On success,\n   484:     /// returns the number of bytes peeked.\n   485:     ///\n   486:     /// Successive calls return the same data. This is accomplished by passing\n   487:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   488:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::take_error",
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
      "name": "take_error",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 2710,
                                    "path": "io::Error"
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
    "verification_source": "   442:     ///\n   443:     /// ```no_run\n   444:     /// use std::os::unix::net::UnixStream;\n   445:     ///\n   446:     /// fn main() -> std::io::Result<()> {\n   447:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   448:     ///     if let Ok(Some(err)) = socket.take_error() {\n   449:     ///         println!(\"Got error: {err:?}\");\n   450:     ///     }\n   451:     ///     Ok(())\n   452:     /// }\n   453:     /// ```\n   454:     ///\n   455:     /// # Platform specific\n   456:     /// On Redox this always returns `None`.\n   457:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   458:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   459:         self.0.take_error()\n   460:     }\n   461: \n   462:     /// Shuts down the read, write, or both halves of this connection.\n   463:     ///\n   464:     /// This function will cause all pending and future I/O calls on the\n   465:     /// specified portions to immediately return with an appropriate value\n   466:     /// (see the documentation of [`Shutdown`]).\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```no_run\n   471:     /// use std::os::unix::net::UnixStream;\n   472:     /// use std::net::Shutdown;\n   473:     ///\n   474:     /// fn main() -> std::io::Result<()> {",
    "nanvix_source": "   445:     ///     if let Ok(Some(err)) = socket.take_error() {\n   446:     ///         println!(\"Got error: {err:?}\");\n   447:     ///     }\n   448:     ///     Ok(())\n   449:     /// }\n   450:     /// ```\n   451:     ///\n   452:     /// # Platform specific\n   453:     /// On Redox this always returns `None`.\n   454:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   455:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   456:         self.0.take_error()\n   457:     }\n   458: \n   459:     /// Shuts down the read, write, or both halves of this connection.\n   460:     ///\n   461:     /// This function will cause all pending and future I/O calls on the\n   462:     /// specified portions to immediately return with an appropriate value\n   463:     /// (see the documentation of [`Shutdown`]).\n   464:     ///\n   465:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::try_clone",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                      "resolved_path": {
                        "args": null,
                        "id": 4284,
                        "path": "UnixStream"
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
    "verification_source": "   184:     /// object references. Both handles will read and write the same stream of\n   185:     /// data, and options set on one stream will be propagated to the other\n   186:     /// stream.\n   187:     ///\n   188:     /// # Examples\n   189:     ///\n   190:     /// ```no_run\n   191:     /// use std::os::unix::net::UnixStream;\n   192:     ///\n   193:     /// fn main() -> std::io::Result<()> {\n   194:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   195:     ///     let sock_copy = socket.try_clone().expect(\"Couldn't clone socket\");\n   196:     ///     Ok(())\n   197:     /// }\n   198:     /// ```\n   199:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   200:     pub fn try_clone(&self) -> io::Result<UnixStream> {\n   201:         self.0.duplicate().map(UnixStream)\n   202:     }\n   203: \n   204:     /// Returns the socket address of the local half of this connection.\n   205:     ///\n   206:     /// # Examples\n   207:     ///\n   208:     /// ```no_run\n   209:     /// use std::os::unix::net::UnixStream;\n   210:     ///\n   211:     /// fn main() -> std::io::Result<()> {\n   212:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   213:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   214:     ///     Ok(())\n   215:     /// }\n   216:     /// ```",
    "nanvix_source": "   186:     /// ```no_run\n   187:     /// use std::os::unix::net::UnixStream;\n   188:     ///\n   189:     /// fn main() -> std::io::Result<()> {\n   190:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   191:     ///     let sock_copy = socket.try_clone().expect(\"Couldn't clone socket\");\n   192:     ///     Ok(())\n   193:     /// }\n   194:     /// ```\n   195:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   196:     pub fn try_clone(&self) -> io::Result<UnixStream> {\n   197:         self.0.duplicate().map(UnixStream)\n   198:     }\n   199: \n   200:     /// Returns the socket address of the local half of this connection.\n   201:     ///\n   202:     /// # Examples\n   203:     ///\n   204:     /// ```no_run\n   205:     /// use std::os::unix::net::UnixStream;\n   206:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::write_timeout",
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
      "name": "write_timeout",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 513,
                                    "path": "Duration"
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
    "verification_source": "   376:     ///\n   377:     /// # Examples\n   378:     ///\n   379:     /// ```no_run\n   380:     /// use std::os::unix::net::UnixStream;\n   381:     /// use std::time::Duration;\n   382:     ///\n   383:     /// fn main() -> std::io::Result<()> {\n   384:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   385:     ///     socket.set_write_timeout(Some(Duration::new(1, 0)))\n   386:     ///         .expect(\"Couldn't set write timeout\");\n   387:     ///     assert_eq!(socket.write_timeout()?, Some(Duration::new(1, 0)));\n   388:     ///     Ok(())\n   389:     /// }\n   390:     /// ```\n   391:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   392:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   393:         self.0.timeout(libc::SO_SNDTIMEO)\n   394:     }\n   395: \n   396:     /// Moves the socket into or out of nonblocking mode.\n   397:     ///\n   398:     /// # Examples\n   399:     ///\n   400:     /// ```no_run\n   401:     /// use std::os::unix::net::UnixStream;\n   402:     ///\n   403:     /// fn main() -> std::io::Result<()> {\n   404:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   405:     ///     socket.set_nonblocking(true).expect(\"Couldn't set nonblocking\");\n   406:     ///     Ok(())\n   407:     /// }\n   408:     /// ```",
    "nanvix_source": "   379:     ///\n   380:     /// fn main() -> std::io::Result<()> {\n   381:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   382:     ///     socket.set_write_timeout(Some(Duration::new(1, 0)))\n   383:     ///         .expect(\"Couldn't set write timeout\");\n   384:     ///     assert_eq!(socket.write_timeout()?, Some(Duration::new(1, 0)));\n   385:     ///     Ok(())\n   386:     /// }\n   387:     /// ```\n   388:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   389:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   390:         self.0.timeout(libc::SO_SNDTIMEO)\n   391:     }\n   392: \n   393:     /// Moves the socket into or out of nonblocking mode.\n   394:     ///\n   395:     /// # Examples\n   396:     ///\n   397:     /// ```no_run\n   398:     /// use std::os::unix::net::UnixStream;\n   399:     ///",
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
