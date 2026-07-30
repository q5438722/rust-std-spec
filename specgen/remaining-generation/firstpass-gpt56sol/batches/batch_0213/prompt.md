For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::set_read_timeout",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   302:     /// ```\n   303:     ///\n   304:     /// An [`Err`] is returned if the zero [`Duration`] is passed to this\n   305:     /// method:\n   306:     ///\n   307:     /// ```no_run\n   308:     /// use std::io;\n   309:     /// use std::net::UdpSocket;\n   310:     /// use std::time::Duration;\n   311:     ///\n   312:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").unwrap();\n   313:     /// let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   314:     /// let err = result.unwrap_err();\n   315:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   316:     /// ```\n   317:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   318:     pub fn set_read_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   319:         self.0.set_read_timeout(dur)\n   320:     }\n   321: \n   322:     /// Sets the write timeout to the timeout specified.\n   323:     ///\n   324:     /// If the value specified is [`None`], then [`write`] calls will block\n   325:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   326:     /// passed to this method.\n   327:     ///\n   328:     /// # Platform-specific behavior\n   329:     ///\n   330:     /// Platforms may return a different error code whenever a write times out\n   331:     /// as a result of setting this option. For example Unix typically returns\n   332:     /// an error of the kind [`WouldBlock`], but Windows may return [`TimedOut`].\n   333:     ///\n   334:     /// [`write`]: io::Write::write",
    "nanvix_source": "   308:     /// use std::io;\n   309:     /// use std::net::UdpSocket;\n   310:     /// use std::time::Duration;\n   311:     ///\n   312:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").unwrap();\n   313:     /// let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   314:     /// let err = result.unwrap_err();\n   315:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   316:     /// ```\n   317:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   318:     pub fn set_read_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   319:         self.0.set_read_timeout(dur)\n   320:     }\n   321: \n   322:     /// Sets the write timeout to the timeout specified.\n   323:     ///\n   324:     /// If the value specified is [`None`], then [`write`] calls will block\n   325:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   326:     /// passed to this method.\n   327:     ///\n   328:     /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_ttl",
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
      "name": "set_ttl",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
            "ttl",
            {
              "primitive": "u32"
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
    "verification_source": "   550:     }\n   551: \n   552:     /// Sets the value for the `IP_TTL` option on this socket.\n   553:     ///\n   554:     /// This value sets the time-to-live field that is used in every packet sent\n   555:     /// from this socket.\n   556:     ///\n   557:     /// # Examples\n   558:     ///\n   559:     /// ```no_run\n   560:     /// use std::net::UdpSocket;\n   561:     ///\n   562:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   563:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   564:     /// ```\n   565:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   566:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n   567:         self.0.set_ttl(ttl)\n   568:     }\n   569: \n   570:     /// Gets the value of the `IP_TTL` option for this socket.\n   571:     ///\n   572:     /// For more information about this option, see [`UdpSocket::set_ttl`].\n   573:     ///\n   574:     /// # Examples\n   575:     ///\n   576:     /// ```no_run\n   577:     /// use std::net::UdpSocket;\n   578:     ///\n   579:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   580:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   581:     /// assert_eq!(socket.ttl().unwrap(), 42);\n   582:     /// ```",
    "nanvix_source": "   556:     ///\n   557:     /// # Examples\n   558:     ///\n   559:     /// ```no_run\n   560:     /// use std::net::UdpSocket;\n   561:     ///\n   562:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   563:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   564:     /// ```\n   565:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   566:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n   567:         self.0.set_ttl(ttl)\n   568:     }\n   569: \n   570:     /// Gets the value of the `IP_TTL` option for this socket.\n   571:     ///\n   572:     /// For more information about this option, see [`UdpSocket::set_ttl`].\n   573:     ///\n   574:     /// # Examples\n   575:     ///\n   576:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_write_timeout",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   345:     /// ```\n   346:     ///\n   347:     /// An [`Err`] is returned if the zero [`Duration`] is passed to this\n   348:     /// method:\n   349:     ///\n   350:     /// ```no_run\n   351:     /// use std::io;\n   352:     /// use std::net::UdpSocket;\n   353:     /// use std::time::Duration;\n   354:     ///\n   355:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").unwrap();\n   356:     /// let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   357:     /// let err = result.unwrap_err();\n   358:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   359:     /// ```\n   360:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   361:     pub fn set_write_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   362:         self.0.set_write_timeout(dur)\n   363:     }\n   364: \n   365:     /// Returns the read timeout of this socket.\n   366:     ///\n   367:     /// If the timeout is [`None`], then [`read`] calls will block indefinitely.\n   368:     ///\n   369:     /// [`read`]: io::Read::read\n   370:     ///\n   371:     /// # Examples\n   372:     ///\n   373:     /// ```no_run\n   374:     /// use std::net::UdpSocket;\n   375:     ///\n   376:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   377:     /// socket.set_read_timeout(None).expect(\"set_read_timeout call failed\");",
    "nanvix_source": "   351:     /// use std::io;\n   352:     /// use std::net::UdpSocket;\n   353:     /// use std::time::Duration;\n   354:     ///\n   355:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").unwrap();\n   356:     /// let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   357:     /// let err = result.unwrap_err();\n   358:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   359:     /// ```\n   360:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   361:     pub fn set_write_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   362:         self.0.set_write_timeout(dur)\n   363:     }\n   364: \n   365:     /// Returns the read timeout of this socket.\n   366:     ///\n   367:     /// If the timeout is [`None`], then [`read`] calls will block indefinitely.\n   368:     ///\n   369:     /// [`read`]: io::Read::read\n   370:     ///\n   371:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::take_error",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   629:     /// the field in the process. This can be useful for checking errors between\n   630:     /// calls.\n   631:     ///\n   632:     /// # Examples\n   633:     ///\n   634:     /// ```no_run\n   635:     /// use std::net::UdpSocket;\n   636:     ///\n   637:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   638:     /// match socket.take_error() {\n   639:     ///     Ok(Some(error)) => println!(\"UdpSocket error: {error:?}\"),\n   640:     ///     Ok(None) => println!(\"No error\"),\n   641:     ///     Err(error) => println!(\"UdpSocket.take_error failed: {error:?}\"),\n   642:     /// }\n   643:     /// ```\n   644:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   645:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   646:         self.0.take_error()\n   647:     }\n   648: \n   649:     /// Connects this UDP socket to a remote address, allowing the `send` and\n   650:     /// `recv` syscalls to be used to send data and also applies filters to only\n   651:     /// receive data from the specified address.\n   652:     ///\n   653:     /// If `addr` yields multiple addresses, `connect` will be attempted with\n   654:     /// each of the addresses until the underlying OS function returns no\n   655:     /// error. Note that usually, a successful `connect` call does not specify\n   656:     /// that there is a remote server listening on the port, rather, such an\n   657:     /// error would only be detected after the first send. If the OS returns an\n   658:     /// error for each of the specified addresses, the error returned from the\n   659:     /// last connection attempt (the last address) is returned.\n   660:     ///\n   661:     /// # Examples",
    "nanvix_source": "   635:     /// use std::net::UdpSocket;\n   636:     ///\n   637:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   638:     /// match socket.take_error() {\n   639:     ///     Ok(Some(error)) => println!(\"UdpSocket error: {error:?}\"),\n   640:     ///     Ok(None) => println!(\"No error\"),\n   641:     ///     Err(error) => println!(\"UdpSocket.take_error failed: {error:?}\"),\n   642:     /// }\n   643:     /// ```\n   644:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   645:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   646:         self.0.take_error()\n   647:     }\n   648: \n   649:     /// Connects this UDP socket to a remote address, allowing the `send` and\n   650:     /// `recv` syscalls to be used to send data and also applies filters to only\n   651:     /// receive data from the specified address.\n   652:     ///\n   653:     /// If `addr` yields multiple addresses, `connect` will be attempted with\n   654:     /// each of the addresses until the underlying OS function returns no\n   655:     /// error. Note that usually, a successful `connect` call does not specify",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::try_clone",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
                        "id": 4677,
                        "path": "UdpSocket"
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
    "verification_source": "   259: \n   260:     /// Creates a new independently owned handle to the underlying socket.\n   261:     ///\n   262:     /// The returned `UdpSocket` is a reference to the same socket that this\n   263:     /// object references. Both handles will read and write the same port, and\n   264:     /// options set on one socket will be propagated to the other.\n   265:     ///\n   266:     /// # Examples\n   267:     ///\n   268:     /// ```no_run\n   269:     /// use std::net::UdpSocket;\n   270:     ///\n   271:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   272:     /// let socket_clone = socket.try_clone().expect(\"couldn't clone the socket\");\n   273:     /// ```\n   274:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   275:     pub fn try_clone(&self) -> io::Result<UdpSocket> {\n   276:         self.0.duplicate().map(UdpSocket)\n   277:     }\n   278: \n   279:     /// Sets the read timeout to the timeout specified.\n   280:     ///\n   281:     /// If the value specified is [`None`], then [`read`] calls will block\n   282:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   283:     /// passed to this method.\n   284:     ///\n   285:     /// # Platform-specific behavior\n   286:     ///\n   287:     /// Platforms may return a different error code whenever a read times out as\n   288:     /// a result of setting this option. For example Unix typically returns an\n   289:     /// error of the kind [`WouldBlock`], but Windows may return [`TimedOut`].\n   290:     ///\n   291:     /// [`read`]: io::Read::read",
    "nanvix_source": "   265:     ///\n   266:     /// # Examples\n   267:     ///\n   268:     /// ```no_run\n   269:     /// use std::net::UdpSocket;\n   270:     ///\n   271:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   272:     /// let socket_clone = socket.try_clone().expect(\"couldn't clone the socket\");\n   273:     /// ```\n   274:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   275:     pub fn try_clone(&self) -> io::Result<UdpSocket> {\n   276:         self.0.duplicate().map(UdpSocket)\n   277:     }\n   278: \n   279:     /// Sets the read timeout to the timeout specified.\n   280:     ///\n   281:     /// If the value specified is [`None`], then [`read`] calls will block\n   282:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   283:     /// passed to this method.\n   284:     ///\n   285:     /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::ttl",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   568:     }\n   569: \n   570:     /// Gets the value of the `IP_TTL` option for this socket.\n   571:     ///\n   572:     /// For more information about this option, see [`UdpSocket::set_ttl`].\n   573:     ///\n   574:     /// # Examples\n   575:     ///\n   576:     /// ```no_run\n   577:     /// use std::net::UdpSocket;\n   578:     ///\n   579:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   580:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   581:     /// assert_eq!(socket.ttl().unwrap(), 42);\n   582:     /// ```\n   583:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   584:     pub fn ttl(&self) -> io::Result<u32> {\n   585:         self.0.ttl()\n   586:     }\n   587: \n   588:     /// Executes an operation of the `IP_ADD_MEMBERSHIP` type.\n   589:     ///\n   590:     /// This function specifies a new multicast group for this socket to join.\n   591:     /// The address must be a valid multicast address, and `interface` is the\n   592:     /// address of the local interface with which the system should join the\n   593:     /// multicast group. If it's equal to [`UNSPECIFIED`](Ipv4Addr::UNSPECIFIED)\n   594:     /// then an appropriate interface is chosen by the system.\n   595:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   596:     pub fn join_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   597:         self.0.join_multicast_v4(multiaddr, interface)\n   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.",
    "nanvix_source": "   574:     /// # Examples\n   575:     ///\n   576:     /// ```no_run\n   577:     /// use std::net::UdpSocket;\n   578:     ///\n   579:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   580:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   581:     /// assert_eq!(socket.ttl().unwrap(), 42);\n   582:     /// ```\n   583:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   584:     pub fn ttl(&self) -> io::Result<u32> {\n   585:         self.0.ttl()\n   586:     }\n   587: \n   588:     /// Executes an operation of the `IP_ADD_MEMBERSHIP` type.\n   589:     ///\n   590:     /// This function specifies a new multicast group for this socket to join.\n   591:     /// The address must be a valid multicast address, and `interface` is the\n   592:     /// address of the local interface with which the system should join the\n   593:     /// multicast group. If it's equal to [`UNSPECIFIED`](Ipv4Addr::UNSPECIFIED)\n   594:     /// then an appropriate interface is chosen by the system.",
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
