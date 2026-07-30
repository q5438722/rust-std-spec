For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixDatagram::peer_addr",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                        "id": 5186,
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
    "verification_source": "   302:     /// [`connect`]: UnixDatagram::connect\n   303:     ///\n   304:     /// # Examples\n   305:     ///\n   306:     /// ```no_run\n   307:     /// use std::os::unix::net::UnixDatagram;\n   308:     ///\n   309:     /// fn main() -> std::io::Result<()> {\n   310:     ///     let sock = UnixDatagram::unbound()?;\n   311:     ///     sock.connect(\"/path/to/the/socket\")?;\n   312:     ///\n   313:     ///     let addr = sock.peer_addr().expect(\"Couldn't get peer address\");\n   314:     ///     Ok(())\n   315:     /// }\n   316:     /// ```\n   317:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   318:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   319:         SocketAddr::new(|addr, len| unsafe { libc::getpeername(self.as_raw_fd(), addr, len) })\n   320:     }\n   321: \n   322:     fn recv_from_flags(\n   323:         &self,\n   324:         buf: &mut [u8],\n   325:         flags: core::ffi::c_int,\n   326:     ) -> io::Result<(usize, SocketAddr)> {\n   327:         let mut count = 0;\n   328:         let addr = SocketAddr::new(|addr, len| unsafe {\n   329:             count = libc::recvfrom(\n   330:                 self.as_raw_fd(),\n   331:                 buf.as_mut_ptr() as *mut _,\n   332:                 buf.len(),\n   333:                 flags,\n   334:                 addr,",
    "nanvix_source": "   305:     ///\n   306:     /// fn main() -> std::io::Result<()> {\n   307:     ///     let sock = UnixDatagram::unbound()?;\n   308:     ///     sock.connect(\"/path/to/the/socket\")?;\n   309:     ///\n   310:     ///     let addr = sock.peer_addr().expect(\"Couldn't get peer address\");\n   311:     ///     Ok(())\n   312:     /// }\n   313:     /// ```\n   314:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   315:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   316:         SocketAddr::new(|addr, len| unsafe { libc::getpeername(self.as_raw_fd(), addr, len) })\n   317:     }\n   318: \n   319:     fn recv_from_flags(\n   320:         &self,\n   321:         buf: &mut [u8],\n   322:         flags: core::ffi::c_int,\n   323:     ) -> io::Result<(usize, SocketAddr)> {\n   324:         let mut count = 0;\n   325:         let addr = SocketAddr::new(|addr, len| unsafe {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::read_timeout",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
    "verification_source": "   780:     ///\n   781:     /// # Examples\n   782:     ///\n   783:     /// ```\n   784:     /// use std::os::unix::net::UnixDatagram;\n   785:     /// use std::time::Duration;\n   786:     ///\n   787:     /// fn main() -> std::io::Result<()> {\n   788:     ///     let sock = UnixDatagram::unbound()?;\n   789:     ///     sock.set_read_timeout(Some(Duration::new(1, 0)))\n   790:     ///         .expect(\"set_read_timeout function failed\");\n   791:     ///     assert_eq!(sock.read_timeout()?, Some(Duration::new(1, 0)));\n   792:     ///     Ok(())\n   793:     /// }\n   794:     /// ```\n   795:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   796:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   797:         self.0.timeout(libc::SO_RCVTIMEO)\n   798:     }\n   799: \n   800:     /// Returns the write timeout of this socket.\n   801:     ///\n   802:     /// # Examples\n   803:     ///\n   804:     /// ```\n   805:     /// use std::os::unix::net::UnixDatagram;\n   806:     /// use std::time::Duration;\n   807:     ///\n   808:     /// fn main() -> std::io::Result<()> {\n   809:     ///     let sock = UnixDatagram::unbound()?;\n   810:     ///     sock.set_write_timeout(Some(Duration::new(1, 0)))\n   811:     ///         .expect(\"set_write_timeout function failed\");\n   812:     ///     assert_eq!(sock.write_timeout()?, Some(Duration::new(1, 0)));",
    "nanvix_source": "   783:     ///\n   784:     /// fn main() -> std::io::Result<()> {\n   785:     ///     let sock = UnixDatagram::unbound()?;\n   786:     ///     sock.set_read_timeout(Some(Duration::new(1, 0)))\n   787:     ///         .expect(\"set_read_timeout function failed\");\n   788:     ///     assert_eq!(sock.read_timeout()?, Some(Duration::new(1, 0)));\n   789:     ///     Ok(())\n   790:     /// }\n   791:     /// ```\n   792:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   793:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   794:         self.0.timeout(libc::SO_RCVTIMEO)\n   795:     }\n   796: \n   797:     /// Returns the write timeout of this socket.\n   798:     ///\n   799:     /// # Examples\n   800:     ///\n   801:     /// ```\n   802:     /// use std::os::unix::net::UnixDatagram;\n   803:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::recv",
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
      "name": "recv",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                  "slice": {
                    "primitive": "u8"
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
    "verification_source": "   373:     ///\n   374:     /// On success, returns the number of bytes read.\n   375:     ///\n   376:     /// # Examples\n   377:     ///\n   378:     /// ```no_run\n   379:     /// use std::os::unix::net::UnixDatagram;\n   380:     ///\n   381:     /// fn main() -> std::io::Result<()> {\n   382:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   383:     ///     let mut buf = vec![0; 10];\n   384:     ///     sock.recv(buf.as_mut_slice()).expect(\"recv function failed\");\n   385:     ///     Ok(())\n   386:     /// }\n   387:     /// ```\n   388:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   389:     pub fn recv(&self, buf: &mut [u8]) -> io::Result<usize> {\n   390:         self.0.read(buf)\n   391:     }\n   392: \n   393:     /// Receives data and ancillary data from socket.\n   394:     ///\n   395:     /// On success, returns the number of bytes read, if the data was truncated and the address from whence the msg came.\n   396:     ///\n   397:     /// # Examples\n   398:     ///\n   399:     #[cfg_attr(\n   400:         any(target_os = \"android\", target_os = \"linux\", target_os = \"cygwin\"),\n   401:         doc = \"```no_run\"\n   402:     )]\n   403:     #[cfg_attr(\n   404:         not(any(target_os = \"android\", target_os = \"linux\", target_os = \"cygwin\")),\n   405:         doc = \"```ignore\"",
    "nanvix_source": "   376:     /// use std::os::unix::net::UnixDatagram;\n   377:     ///\n   378:     /// fn main() -> std::io::Result<()> {\n   379:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   380:     ///     let mut buf = vec![0; 10];\n   381:     ///     sock.recv(buf.as_mut_slice()).expect(\"recv function failed\");\n   382:     ///     Ok(())\n   383:     /// }\n   384:     /// ```\n   385:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   386:     pub fn recv(&self, buf: &mut [u8]) -> io::Result<usize> {\n   387:         self.0.read(buf)\n   388:     }\n   389: \n   390:     /// Receives data and ancillary data from socket.\n   391:     ///\n   392:     /// On success, returns the number of bytes read, if the data was truncated and the address from whence the msg came.\n   393:     ///\n   394:     /// # Examples\n   395:     ///\n   396:     #[cfg_attr(",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::recv_from",
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
      "name": "recv_from",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                  "slice": {
                    "primitive": "u8"
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
                      "tuple": [
                        {
                          "primitive": "usize"
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 5186,
                            "path": "SocketAddr"
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
    "verification_source": "   352:     /// whence the data came.\n   353:     ///\n   354:     /// # Examples\n   355:     ///\n   356:     /// ```no_run\n   357:     /// use std::os::unix::net::UnixDatagram;\n   358:     ///\n   359:     /// fn main() -> std::io::Result<()> {\n   360:     ///     let sock = UnixDatagram::unbound()?;\n   361:     ///     let mut buf = vec![0; 10];\n   362:     ///     let (size, sender) = sock.recv_from(buf.as_mut_slice())?;\n   363:     ///     println!(\"received {size} bytes from {sender:?}\");\n   364:     ///     Ok(())\n   365:     /// }\n   366:     /// ```\n   367:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   368:     pub fn recv_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   369:         self.recv_from_flags(buf, 0)\n   370:     }\n   371: \n   372:     /// Receives data from the socket.\n   373:     ///\n   374:     /// On success, returns the number of bytes read.\n   375:     ///\n   376:     /// # Examples\n   377:     ///\n   378:     /// ```no_run\n   379:     /// use std::os::unix::net::UnixDatagram;\n   380:     ///\n   381:     /// fn main() -> std::io::Result<()> {\n   382:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   383:     ///     let mut buf = vec![0; 10];\n   384:     ///     sock.recv(buf.as_mut_slice()).expect(\"recv function failed\");",
    "nanvix_source": "   355:     ///\n   356:     /// fn main() -> std::io::Result<()> {\n   357:     ///     let sock = UnixDatagram::unbound()?;\n   358:     ///     let mut buf = vec![0; 10];\n   359:     ///     let (size, sender) = sock.recv_from(buf.as_mut_slice())?;\n   360:     ///     println!(\"received {size} bytes from {sender:?}\");\n   361:     ///     Ok(())\n   362:     /// }\n   363:     /// ```\n   364:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   365:     pub fn recv_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   366:         self.recv_from_flags(buf, 0)\n   367:     }\n   368: \n   369:     /// Receives data from the socket.\n   370:     ///\n   371:     /// On success, returns the number of bytes read.\n   372:     ///\n   373:     /// # Examples\n   374:     ///\n   375:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::send",
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
      "name": "send",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
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
    "verification_source": "   576:     ///\n   577:     /// On success, returns the number of bytes written.\n   578:     ///\n   579:     /// # Examples\n   580:     ///\n   581:     /// ```no_run\n   582:     /// use std::os::unix::net::UnixDatagram;\n   583:     ///\n   584:     /// fn main() -> std::io::Result<()> {\n   585:     ///     let sock = UnixDatagram::unbound()?;\n   586:     ///     sock.connect(\"/some/sock\").expect(\"Couldn't connect\");\n   587:     ///     sock.send(b\"omelette au fromage\").expect(\"send_to function failed\");\n   588:     ///     Ok(())\n   589:     /// }\n   590:     /// ```\n   591:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   592:     pub fn send(&self, buf: &[u8]) -> io::Result<usize> {\n   593:         self.0.write(buf)\n   594:     }\n   595: \n   596:     /// Sends data and ancillary data on the socket to the specified address.\n   597:     ///\n   598:     /// On success, returns the number of bytes written.\n   599:     ///\n   600:     /// # Examples\n   601:     ///\n   602:     #[cfg_attr(\n   603:         any(target_os = \"android\", target_os = \"linux\", target_os = \"cygwin\"),\n   604:         doc = \"```no_run\"\n   605:     )]\n   606:     #[cfg_attr(\n   607:         not(any(target_os = \"android\", target_os = \"linux\", target_os = \"cygwin\")),\n   608:         doc = \"```ignore\"",
    "nanvix_source": "   579:     /// use std::os::unix::net::UnixDatagram;\n   580:     ///\n   581:     /// fn main() -> std::io::Result<()> {\n   582:     ///     let sock = UnixDatagram::unbound()?;\n   583:     ///     sock.connect(\"/some/sock\").expect(\"Couldn't connect\");\n   584:     ///     sock.send(b\"omelette au fromage\").expect(\"send_to function failed\");\n   585:     ///     Ok(())\n   586:     /// }\n   587:     /// ```\n   588:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   589:     pub fn send(&self, buf: &[u8]) -> io::Result<usize> {\n   590:         self.0.write(buf)\n   591:     }\n   592: \n   593:     /// Sends data and ancillary data on the socket to the specified address.\n   594:     ///\n   595:     /// On success, returns the number of bytes written.\n   596:     ///\n   597:     /// # Examples\n   598:     ///\n   599:     #[cfg_attr(",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::send_to",
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
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 1802,
                                    "path": "Path"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 40,
                        "path": "AsRef"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "send_to",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
                }
              }
            }
          ],
          [
            "path",
            {
              "generic": "P"
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
    "verification_source": "   505:     /// Sends data on the socket to the specified address.\n   506:     ///\n   507:     /// On success, returns the number of bytes written.\n   508:     ///\n   509:     /// # Examples\n   510:     ///\n   511:     /// ```no_run\n   512:     /// use std::os::unix::net::UnixDatagram;\n   513:     ///\n   514:     /// fn main() -> std::io::Result<()> {\n   515:     ///     let sock = UnixDatagram::unbound()?;\n   516:     ///     sock.send_to(b\"omelette au fromage\", \"/some/sock\").expect(\"send_to function failed\");\n   517:     ///     Ok(())\n   518:     /// }\n   519:     /// ```\n   520:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   521:     pub fn send_to<P: AsRef<Path>>(&self, buf: &[u8], path: P) -> io::Result<usize> {\n   522:         unsafe {\n   523:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   524: \n   525:             let count = cvt(libc::sendto(\n   526:                 self.as_raw_fd(),\n   527:                 buf.as_ptr() as *const _,\n   528:                 buf.len(),\n   529:                 MSG_NOSIGNAL,\n   530:                 (&raw const addr) as *const _,\n   531:                 len,\n   532:             ))?;\n   533:             Ok(count as usize)\n   534:         }\n   535:     }\n   536: \n   537:     /// Sends data on the socket to the specified [SocketAddr].",
    "nanvix_source": "   508:     /// ```no_run\n   509:     /// use std::os::unix::net::UnixDatagram;\n   510:     ///\n   511:     /// fn main() -> std::io::Result<()> {\n   512:     ///     let sock = UnixDatagram::unbound()?;\n   513:     ///     sock.send_to(b\"omelette au fromage\", \"/some/sock\").expect(\"send_to function failed\");\n   514:     ///     Ok(())\n   515:     /// }\n   516:     /// ```\n   517:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   518:     pub fn send_to<P: AsRef<Path>>(&self, buf: &[u8], path: P) -> io::Result<usize> {\n   519:         unsafe {\n   520:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   521: \n   522:             let count = cvt(libc::sendto(\n   523:                 self.as_raw_fd(),\n   524:                 buf.as_ptr() as *const _,\n   525:                 buf.len(),\n   526:                 MSG_NOSIGNAL,\n   527:                 (&raw const addr) as *const _,\n   528:                 len,",
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
