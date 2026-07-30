For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::TcpStream::set_write_timeout",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
            "dur",
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
    "verification_source": "   338:     /// ```\n   339:     ///\n   340:     /// An [`Err`] is returned if the zero [`Duration`] is passed to this\n   341:     /// method:\n   342:     ///\n   343:     /// ```no_run\n   344:     /// use std::io;\n   345:     /// use std::net::TcpStream;\n   346:     /// use std::time::Duration;\n   347:     ///\n   348:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\").unwrap();\n   349:     /// let result = stream.set_write_timeout(Some(Duration::new(0, 0)));\n   350:     /// let err = result.unwrap_err();\n   351:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   352:     /// ```\n   353:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   354:     pub fn set_write_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   355:         self.0.set_write_timeout(dur)\n   356:     }\n   357: \n   358:     /// Returns the read timeout of this socket.\n   359:     ///\n   360:     /// If the timeout is [`None`], then [`read`] calls will block indefinitely.\n   361:     ///\n   362:     /// # Platform-specific behavior\n   363:     ///\n   364:     /// Some platforms do not provide access to the current timeout.\n   365:     ///\n   366:     /// [`read`]: Read::read\n   367:     ///\n   368:     /// # Examples\n   369:     ///\n   370:     /// ```no_run",
    "nanvix_source": "   344:     /// use std::io;\n   345:     /// use std::net::TcpStream;\n   346:     /// use std::time::Duration;\n   347:     ///\n   348:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\").unwrap();\n   349:     /// let result = stream.set_write_timeout(Some(Duration::new(0, 0)));\n   350:     /// let err = result.unwrap_err();\n   351:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   352:     /// ```\n   353:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   354:     pub fn set_write_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   355:         self.0.set_write_timeout(dur)\n   356:     }\n   357: \n   358:     /// Returns the read timeout of this socket.\n   359:     ///\n   360:     /// If the timeout is [`None`], then [`read`] calls will block indefinitely.\n   361:     ///\n   362:     /// # Platform-specific behavior\n   363:     ///\n   364:     /// Some platforms do not provide access to the current timeout.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::shutdown",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
    "verification_source": "   229:     ///\n   230:     /// Calling this function multiple times may result in different behavior,\n   231:     /// depending on the operating system. On Linux, the second call will\n   232:     /// return `Ok(())`, but on macOS, it will return `ErrorKind::NotConnected`.\n   233:     /// This may change in the future.\n   234:     ///\n   235:     /// # Examples\n   236:     ///\n   237:     /// ```no_run\n   238:     /// use std::net::{Shutdown, TcpStream};\n   239:     ///\n   240:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   241:     ///                        .expect(\"Couldn't connect to the server...\");\n   242:     /// stream.shutdown(Shutdown::Both).expect(\"shutdown call failed\");\n   243:     /// ```\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   246:         self.0.shutdown(how)\n   247:     }\n   248: \n   249:     /// Creates a new independently owned handle to the underlying socket.\n   250:     ///\n   251:     /// The returned `TcpStream` is a reference to the same stream that this\n   252:     /// object references. Both handles will read and write the same stream of\n   253:     /// data, and options set on one stream will be propagated to the other\n   254:     /// stream.\n   255:     ///\n   256:     /// # Examples\n   257:     ///\n   258:     /// ```no_run\n   259:     /// use std::net::TcpStream;\n   260:     ///\n   261:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")",
    "nanvix_source": "   235:     /// # Examples\n   236:     ///\n   237:     /// ```no_run\n   238:     /// use std::net::{Shutdown, TcpStream};\n   239:     ///\n   240:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   241:     ///                        .expect(\"Couldn't connect to the server...\");\n   242:     /// stream.shutdown(Shutdown::Both).expect(\"shutdown call failed\");\n   243:     /// ```\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   246:         self.0.shutdown(how)\n   247:     }\n   248: \n   249:     /// Creates a new independently owned handle to the underlying socket.\n   250:     ///\n   251:     /// The returned `TcpStream` is a reference to the same stream that this\n   252:     /// object references. Both handles will read and write the same stream of\n   253:     /// data, and options set on one stream will be propagated to the other\n   254:     /// stream.\n   255:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::take_error",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
    "verification_source": "   556:     /// Gets the value of the `SO_ERROR` option on this socket.\n   557:     ///\n   558:     /// This will retrieve the stored error in the underlying socket, clearing\n   559:     /// the field in the process. This can be useful for checking errors between\n   560:     /// calls.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```no_run\n   565:     /// use std::net::TcpStream;\n   566:     ///\n   567:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   568:     ///                        .expect(\"Couldn't connect to the server...\");\n   569:     /// stream.take_error().expect(\"No error was expected...\");\n   570:     /// ```\n   571:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   572:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   573:         self.0.take_error()\n   574:     }\n   575: \n   576:     /// Moves this TCP stream into or out of nonblocking mode.\n   577:     ///\n   578:     /// This will result in `read`, `write`, `recv` and `send` system operations\n   579:     /// becoming nonblocking, i.e., immediately returning from their calls.\n   580:     /// If the IO operation is successful, `Ok` is returned and no further\n   581:     /// action is required. If the IO operation could not be completed and needs\n   582:     /// to be retried, an error with kind [`io::ErrorKind::WouldBlock`] is\n   583:     /// returned.\n   584:     ///\n   585:     /// On Unix platforms, calling this method corresponds to calling `fcntl`\n   586:     /// `FIONBIO`. On Windows calling this method corresponds to calling\n   587:     /// `ioctlsocket` `FIONBIO`.\n   588:     ///",
    "nanvix_source": "   613:     /// # Examples\n   614:     ///\n   615:     /// ```no_run\n   616:     /// use std::net::TcpStream;\n   617:     ///\n   618:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   619:     ///                        .expect(\"Couldn't connect to the server...\");\n   620:     /// stream.take_error().expect(\"No error was expected...\");\n   621:     /// ```\n   622:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   623:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   624:         self.0.take_error()\n   625:     }\n   626: \n   627:     /// Moves this TCP stream into or out of nonblocking mode.\n   628:     ///\n   629:     /// This will result in `read`, `write`, `recv` and `send` system operations\n   630:     /// becoming nonblocking, i.e., immediately returning from their calls.\n   631:     /// If the IO operation is successful, `Ok` is returned and no further\n   632:     /// action is required. If the IO operation could not be completed and needs\n   633:     /// to be retried, an error with kind [`io::ErrorKind::WouldBlock`] is",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::try_clone",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
                        "id": 3224,
                        "path": "TcpStream"
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
    "verification_source": "   250:     ///\n   251:     /// The returned `TcpStream` is a reference to the same stream that this\n   252:     /// object references. Both handles will read and write the same stream of\n   253:     /// data, and options set on one stream will be propagated to the other\n   254:     /// stream.\n   255:     ///\n   256:     /// # Examples\n   257:     ///\n   258:     /// ```no_run\n   259:     /// use std::net::TcpStream;\n   260:     ///\n   261:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   262:     ///                        .expect(\"Couldn't connect to the server...\");\n   263:     /// let stream_clone = stream.try_clone().expect(\"clone failed...\");\n   264:     /// ```\n   265:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   266:     pub fn try_clone(&self) -> io::Result<TcpStream> {\n   267:         self.0.duplicate().map(TcpStream)\n   268:     }\n   269: \n   270:     /// Sets the read timeout to the timeout specified.\n   271:     ///\n   272:     /// If the value specified is [`None`], then [`read`] calls will block\n   273:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   274:     /// passed to this method.\n   275:     ///\n   276:     /// # Platform-specific behavior\n   277:     ///\n   278:     /// Platforms may return a different error code whenever a read times out as\n   279:     /// a result of setting this option. For example Unix typically returns an\n   280:     /// error of the kind [`WouldBlock`], but Windows may return [`TimedOut`].\n   281:     ///\n   282:     /// [`read`]: Read::read",
    "nanvix_source": "   256:     /// # Examples\n   257:     ///\n   258:     /// ```no_run\n   259:     /// use std::net::TcpStream;\n   260:     ///\n   261:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   262:     ///                        .expect(\"Couldn't connect to the server...\");\n   263:     /// let stream_clone = stream.try_clone().expect(\"clone failed...\");\n   264:     /// ```\n   265:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   266:     pub fn try_clone(&self) -> io::Result<TcpStream> {\n   267:         self.0.duplicate().map(TcpStream)\n   268:     }\n   269: \n   270:     /// Sets the read timeout to the timeout specified.\n   271:     ///\n   272:     /// If the value specified is [`None`], then [`read`] calls will block\n   273:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   274:     /// passed to this method.\n   275:     ///\n   276:     /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::ttl",
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
      "name": "ttl",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
                      "primitive": "u32"
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
    "verification_source": "   536: \n   537:     /// Gets the value of the `IP_TTL` option for this socket.\n   538:     ///\n   539:     /// For more information about this option, see [`TcpStream::set_ttl`].\n   540:     ///\n   541:     /// # Examples\n   542:     ///\n   543:     /// ```no_run\n   544:     /// use std::net::TcpStream;\n   545:     ///\n   546:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   547:     ///                        .expect(\"Couldn't connect to the server...\");\n   548:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");\n   549:     /// assert_eq!(stream.ttl().unwrap_or(0), 100);\n   550:     /// ```\n   551:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   552:     pub fn ttl(&self) -> io::Result<u32> {\n   553:         self.0.ttl()\n   554:     }\n   555: \n   556:     /// Gets the value of the `SO_ERROR` option on this socket.\n   557:     ///\n   558:     /// This will retrieve the stored error in the underlying socket, clearing\n   559:     /// the field in the process. This can be useful for checking errors between\n   560:     /// calls.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```no_run\n   565:     /// use std::net::TcpStream;\n   566:     ///\n   567:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   568:     ///                        .expect(\"Couldn't connect to the server...\");",
    "nanvix_source": "   593:     ///\n   594:     /// ```no_run\n   595:     /// use std::net::TcpStream;\n   596:     ///\n   597:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   598:     ///                        .expect(\"Couldn't connect to the server...\");\n   599:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");\n   600:     /// assert_eq!(stream.ttl().unwrap_or(0), 100);\n   601:     /// ```\n   602:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   603:     pub fn ttl(&self) -> io::Result<u32> {\n   604:         self.0.ttl()\n   605:     }\n   606: \n   607:     /// Gets the value of the `SO_ERROR` option on this socket.\n   608:     ///\n   609:     /// This will retrieve the stored error in the underlying socket, clearing\n   610:     /// the field in the process. This can be useful for checking errors between\n   611:     /// calls.\n   612:     ///\n   613:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::write_timeout",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
    "verification_source": "   388:     ///\n   389:     /// Some platforms do not provide access to the current timeout.\n   390:     ///\n   391:     /// [`write`]: Write::write\n   392:     ///\n   393:     /// # Examples\n   394:     ///\n   395:     /// ```no_run\n   396:     /// use std::net::TcpStream;\n   397:     ///\n   398:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   399:     ///                        .expect(\"Couldn't connect to the server...\");\n   400:     /// stream.set_write_timeout(None).expect(\"set_write_timeout call failed\");\n   401:     /// assert_eq!(stream.write_timeout().unwrap(), None);\n   402:     /// ```\n   403:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   404:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   405:         self.0.write_timeout()\n   406:     }\n   407: \n   408:     /// Receives data on the socket from the remote address to which it is\n   409:     /// connected, without removing that data from the queue. On success,\n   410:     /// returns the number of bytes peeked.\n   411:     ///\n   412:     /// Successive calls return the same data. This is accomplished by passing\n   413:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   414:     ///\n   415:     /// # Examples\n   416:     ///\n   417:     /// ```no_run\n   418:     /// use std::net::TcpStream;\n   419:     ///\n   420:     /// let stream = TcpStream::connect(\"127.0.0.1:8000\")",
    "nanvix_source": "   394:     ///\n   395:     /// ```no_run\n   396:     /// use std::net::TcpStream;\n   397:     ///\n   398:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   399:     ///                        .expect(\"Couldn't connect to the server...\");\n   400:     /// stream.set_write_timeout(None).expect(\"set_write_timeout call failed\");\n   401:     /// assert_eq!(stream.write_timeout().unwrap(), None);\n   402:     /// ```\n   403:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   404:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   405:         self.0.write_timeout()\n   406:     }\n   407: \n   408:     /// Receives data on the socket from the remote address to which it is\n   409:     /// connected, without removing that data from the queue. On success,\n   410:     /// returns the number of bytes peeked.\n   411:     ///\n   412:     /// Successive calls return the same data. This is accomplished by passing\n   413:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   414:     ///",
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
