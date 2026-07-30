For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::TcpStream::peer_addr",
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
      "name": "peer_addr",
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
                        "id": 4670,
                        "path": "SocketAddr"
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
    "verification_source": "   185:         net_imp::TcpStream::connect_timeout(addr, timeout).map(TcpStream)\n   186:     }\n   187: \n   188:     /// Returns the socket address of the remote peer of this TCP connection.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```no_run\n   193:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpStream};\n   194:     ///\n   195:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   196:     ///                        .expect(\"Couldn't connect to the server...\");\n   197:     /// assert_eq!(stream.peer_addr().unwrap(),\n   198:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   199:     /// ```\n   200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   201:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   202:         self.0.peer_addr()\n   203:     }\n   204: \n   205:     /// Returns the socket address of the local half of this TCP connection.\n   206:     ///\n   207:     /// # Examples\n   208:     ///\n   209:     /// ```no_run\n   210:     /// use std::net::{IpAddr, Ipv4Addr, TcpStream};\n   211:     ///\n   212:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   213:     ///                        .expect(\"Couldn't connect to the server...\");\n   214:     /// assert_eq!(stream.local_addr().unwrap().ip(),\n   215:     ///            IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   216:     /// ```\n   217:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   191:     ///\n   192:     /// ```no_run\n   193:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpStream};\n   194:     ///\n   195:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   196:     ///                        .expect(\"Couldn't connect to the server...\");\n   197:     /// assert_eq!(stream.peer_addr().unwrap(),\n   198:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   199:     /// ```\n   200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   201:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   202:         self.0.peer_addr()\n   203:     }\n   204: \n   205:     /// Returns the socket address of the local half of this TCP connection.\n   206:     ///\n   207:     /// # Examples\n   208:     ///\n   209:     /// ```no_run\n   210:     /// use std::net::{IpAddr, Ipv4Addr, TcpStream};\n   211:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::read_timeout",
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
      "name": "read_timeout",
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
    "verification_source": "   363:     ///\n   364:     /// Some platforms do not provide access to the current timeout.\n   365:     ///\n   366:     /// [`read`]: Read::read\n   367:     ///\n   368:     /// # Examples\n   369:     ///\n   370:     /// ```no_run\n   371:     /// use std::net::TcpStream;\n   372:     ///\n   373:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   374:     ///                        .expect(\"Couldn't connect to the server...\");\n   375:     /// stream.set_read_timeout(None).expect(\"set_read_timeout call failed\");\n   376:     /// assert_eq!(stream.read_timeout().unwrap(), None);\n   377:     /// ```\n   378:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   379:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   380:         self.0.read_timeout()\n   381:     }\n   382: \n   383:     /// Returns the write timeout of this socket.\n   384:     ///\n   385:     /// If the timeout is [`None`], then [`write`] calls will block indefinitely.\n   386:     ///\n   387:     /// # Platform-specific behavior\n   388:     ///\n   389:     /// Some platforms do not provide access to the current timeout.\n   390:     ///\n   391:     /// [`write`]: Write::write\n   392:     ///\n   393:     /// # Examples\n   394:     ///\n   395:     /// ```no_run",
    "nanvix_source": "   369:     ///\n   370:     /// ```no_run\n   371:     /// use std::net::TcpStream;\n   372:     ///\n   373:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   374:     ///                        .expect(\"Couldn't connect to the server...\");\n   375:     /// stream.set_read_timeout(None).expect(\"set_read_timeout call failed\");\n   376:     /// assert_eq!(stream.read_timeout().unwrap(), None);\n   377:     /// ```\n   378:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   379:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   380:         self.0.read_timeout()\n   381:     }\n   382: \n   383:     /// Returns the write timeout of this socket.\n   384:     ///\n   385:     /// If the timeout is [`None`], then [`write`] calls will block indefinitely.\n   386:     ///\n   387:     /// # Platform-specific behavior\n   388:     ///\n   389:     /// Some platforms do not provide access to the current timeout.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::set_nodelay",
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
      "name": "set_nodelay",
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
            "nodelay",
            {
              "primitive": "bool"
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
    "verification_source": "   479:     /// If set, this option disables the Nagle algorithm. This means that\n   480:     /// segments are always sent as soon as possible, even if there is only a\n   481:     /// small amount of data. When not set, data is buffered until there is a\n   482:     /// sufficient amount to send out, thereby avoiding the frequent sending of\n   483:     /// small packets.\n   484:     ///\n   485:     /// # Examples\n   486:     ///\n   487:     /// ```no_run\n   488:     /// use std::net::TcpStream;\n   489:     ///\n   490:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   491:     ///                        .expect(\"Couldn't connect to the server...\");\n   492:     /// stream.set_nodelay(true).expect(\"set_nodelay call failed\");\n   493:     /// ```\n   494:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   495:     pub fn set_nodelay(&self, nodelay: bool) -> io::Result<()> {\n   496:         self.0.set_nodelay(nodelay)\n   497:     }\n   498: \n   499:     /// Gets the value of the `TCP_NODELAY` option on this socket.\n   500:     ///\n   501:     /// For more information about this option, see [`TcpStream::set_nodelay`].\n   502:     ///\n   503:     /// # Examples\n   504:     ///\n   505:     /// ```no_run\n   506:     /// use std::net::TcpStream;\n   507:     ///\n   508:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   509:     ///                        .expect(\"Couldn't connect to the server...\");\n   510:     /// stream.set_nodelay(true).expect(\"set_nodelay call failed\");\n   511:     /// assert_eq!(stream.nodelay().unwrap_or(false), true);",
    "nanvix_source": "   536:     /// # Examples\n   537:     ///\n   538:     /// ```no_run\n   539:     /// use std::net::TcpStream;\n   540:     ///\n   541:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   542:     ///                        .expect(\"Couldn't connect to the server...\");\n   543:     /// stream.set_nodelay(true).expect(\"set_nodelay call failed\");\n   544:     /// ```\n   545:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   546:     pub fn set_nodelay(&self, nodelay: bool) -> io::Result<()> {\n   547:         self.0.set_nodelay(nodelay)\n   548:     }\n   549: \n   550:     /// Gets the value of the `TCP_NODELAY` option on this socket.\n   551:     ///\n   552:     /// For more information about this option, see [`TcpStream::set_nodelay`].\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::set_nonblocking",
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
      "name": "set_nonblocking",
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
            "nonblocking",
            {
              "primitive": "bool"
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
    "verification_source": "   601:     /// # fn wait_for_fd() { unimplemented!() }\n   602:     /// let mut buf = vec![];\n   603:     /// loop {\n   604:     ///     match stream.read_to_end(&mut buf) {\n   605:     ///         Ok(_) => break,\n   606:     ///         Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {\n   607:     ///             // wait until network socket is ready, typically implemented\n   608:     ///             // via platform-specific APIs such as epoll or IOCP\n   609:     ///             wait_for_fd();\n   610:     ///         }\n   611:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n   612:     ///     };\n   613:     /// };\n   614:     /// println!(\"bytes: {buf:?}\");\n   615:     /// ```\n   616:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   617:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   618:         self.0.set_nonblocking(nonblocking)\n   619:     }\n   620: }\n   621: \n   622: // In addition to the `impl`s here, `TcpStream` also has `impl`s for\n   623: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n   624: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n   625: // `AsSocket`/`From<OwnedSocket>`/`Into<OwnedSocket>` and\n   626: // `AsRawSocket`/`IntoRawSocket`/`FromRawSocket` on Windows.\n   627: \n   628: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   629: impl Read for TcpStream {\n   630:     fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {\n   631:         self.0.read(buf)\n   632:     }\n   633: ",
    "nanvix_source": "   658:     ///             // wait until network socket is ready, typically implemented\n   659:     ///             // via platform-specific APIs such as epoll or IOCP\n   660:     ///             wait_for_fd();\n   661:     ///         }\n   662:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n   663:     ///     };\n   664:     /// };\n   665:     /// println!(\"bytes: {buf:?}\");\n   666:     /// ```\n   667:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   668:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   669:         self.0.set_nonblocking(nonblocking)\n   670:     }\n   671: }\n   672: \n   673: // In addition to the `impl`s here, `TcpStream` also has `impl`s for\n   674: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n   675: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n   676: // `AsSocket`/`From<OwnedSocket>`/`Into<OwnedSocket>` and\n   677: // `AsRawSocket`/`IntoRawSocket`/`FromRawSocket` on Windows.\n   678: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::set_read_timeout",
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
    "verification_source": "   294:     /// ```\n   295:     ///\n   296:     /// An [`Err`] is returned if the zero [`Duration`] is passed to this\n   297:     /// method:\n   298:     ///\n   299:     /// ```no_run\n   300:     /// use std::io;\n   301:     /// use std::net::TcpStream;\n   302:     /// use std::time::Duration;\n   303:     ///\n   304:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\").unwrap();\n   305:     /// let result = stream.set_read_timeout(Some(Duration::new(0, 0)));\n   306:     /// let err = result.unwrap_err();\n   307:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   308:     /// ```\n   309:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   310:     pub fn set_read_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   311:         self.0.set_read_timeout(dur)\n   312:     }\n   313: \n   314:     /// Sets the write timeout to the timeout specified.\n   315:     ///\n   316:     /// If the value specified is [`None`], then [`write`] calls will block\n   317:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   318:     /// passed to this method.\n   319:     ///\n   320:     /// # Platform-specific behavior\n   321:     ///\n   322:     /// Platforms may return a different error code whenever a write times out\n   323:     /// as a result of setting this option. For example Unix typically returns\n   324:     /// an error of the kind [`WouldBlock`], but Windows may return [`TimedOut`].\n   325:     ///\n   326:     /// [`write`]: Write::write",
    "nanvix_source": "   300:     /// use std::io;\n   301:     /// use std::net::TcpStream;\n   302:     /// use std::time::Duration;\n   303:     ///\n   304:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\").unwrap();\n   305:     /// let result = stream.set_read_timeout(Some(Duration::new(0, 0)));\n   306:     /// let err = result.unwrap_err();\n   307:     /// assert_eq!(err.kind(), io::ErrorKind::InvalidInput)\n   308:     /// ```\n   309:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   310:     pub fn set_read_timeout(&self, dur: Option<Duration>) -> io::Result<()> {\n   311:         self.0.set_read_timeout(dur)\n   312:     }\n   313: \n   314:     /// Sets the write timeout to the timeout specified.\n   315:     ///\n   316:     /// If the value specified is [`None`], then [`write`] calls will block\n   317:     /// indefinitely. An [`Err`] is returned if the zero [`Duration`] is\n   318:     /// passed to this method.\n   319:     ///\n   320:     /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::set_ttl",
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
    "verification_source": "   517: \n   518:     /// Sets the value for the `IP_TTL` option on this socket.\n   519:     ///\n   520:     /// This value sets the time-to-live field that is used in every packet sent\n   521:     /// from this socket.\n   522:     ///\n   523:     /// # Examples\n   524:     ///\n   525:     /// ```no_run\n   526:     /// use std::net::TcpStream;\n   527:     ///\n   528:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   529:     ///                        .expect(\"Couldn't connect to the server...\");\n   530:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");\n   531:     /// ```\n   532:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   533:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n   534:         self.0.set_ttl(ttl)\n   535:     }\n   536: \n   537:     /// Gets the value of the `IP_TTL` option for this socket.\n   538:     ///\n   539:     /// For more information about this option, see [`TcpStream::set_ttl`].\n   540:     ///\n   541:     /// # Examples\n   542:     ///\n   543:     /// ```no_run\n   544:     /// use std::net::TcpStream;\n   545:     ///\n   546:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   547:     ///                        .expect(\"Couldn't connect to the server...\");\n   548:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");\n   549:     /// assert_eq!(stream.ttl().unwrap_or(0), 100);",
    "nanvix_source": "   574:     /// # Examples\n   575:     ///\n   576:     /// ```no_run\n   577:     /// use std::net::TcpStream;\n   578:     ///\n   579:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   580:     ///                        .expect(\"Couldn't connect to the server...\");\n   581:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");\n   582:     /// ```\n   583:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   584:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n   585:         self.0.set_ttl(ttl)\n   586:     }\n   587: \n   588:     /// Gets the value of the `IP_TTL` option for this socket.\n   589:     ///\n   590:     /// For more information about this option, see [`TcpStream::set_ttl`].\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```no_run",
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
