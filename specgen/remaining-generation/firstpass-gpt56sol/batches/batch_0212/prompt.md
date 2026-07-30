For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::send_to",
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
                        "args": null,
                        "id": 1888,
                        "path": "ToSocketAddrs"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "A"
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
            "addr",
            {
              "generic": "A"
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
    "verification_source": "   192:     /// This will return an error when the IP version of the local socket\n   193:     /// does not match that returned from [`ToSocketAddrs`].\n   194:     ///\n   195:     /// See [Issue #34202] for more details.\n   196:     ///\n   197:     /// # Examples\n   198:     ///\n   199:     /// ```no_run\n   200:     /// use std::net::UdpSocket;\n   201:     ///\n   202:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   203:     /// socket.send_to(&[0; 10], \"127.0.0.1:4242\").expect(\"couldn't send data\");\n   204:     /// ```\n   205:     ///\n   206:     /// [Issue #34202]: https://github.com/rust-lang/rust/issues/34202\n   207:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   208:     pub fn send_to<A: ToSocketAddrs>(&self, buf: &[u8], addr: A) -> io::Result<usize> {\n   209:         match addr.to_socket_addrs()?.next() {\n   210:             Some(addr) => self.0.send_to(buf, &addr),\n   211:             None => Err(io::const_error!(ErrorKind::InvalidInput, \"no addresses to send data to\")),\n   212:         }\n   213:     }\n   214: \n   215:     /// Returns the socket address of the remote peer this socket was connected to.\n   216:     ///\n   217:     /// # Examples\n   218:     ///\n   219:     /// ```no_run\n   220:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};\n   221:     ///\n   222:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   223:     /// socket.connect(\"192.168.0.1:41203\").expect(\"couldn't connect to address\");\n   224:     /// assert_eq!(socket.peer_addr().unwrap(),",
    "nanvix_source": "   198:     ///\n   199:     /// ```no_run\n   200:     /// use std::net::UdpSocket;\n   201:     ///\n   202:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   203:     /// socket.send_to(&[0; 10], \"127.0.0.1:4242\").expect(\"couldn't send data\");\n   204:     /// ```\n   205:     ///\n   206:     /// [Issue #34202]: https://github.com/rust-lang/rust/issues/34202\n   207:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   208:     pub fn send_to<A: ToSocketAddrs>(&self, buf: &[u8], addr: A) -> io::Result<usize> {\n   209:         match addr.to_socket_addrs()?.next() {\n   210:             Some(addr) => self.0.send_to(buf, &addr),\n   211:             None => Err(io::const_error!(ErrorKind::InvalidInput, \"no addresses to send data to\")),\n   212:         }\n   213:     }\n   214: \n   215:     /// Returns the socket address of the remote peer this socket was connected to.\n   216:     ///\n   217:     /// # Examples\n   218:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_broadcast",
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
      "name": "set_broadcast",
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
            "broadcast",
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
    "verification_source": "   403:     }\n   404: \n   405:     /// Sets the value of the `SO_BROADCAST` option for this socket.\n   406:     ///\n   407:     /// When enabled, this socket is allowed to send packets to a broadcast\n   408:     /// address.\n   409:     ///\n   410:     /// # Examples\n   411:     ///\n   412:     /// ```no_run\n   413:     /// use std::net::UdpSocket;\n   414:     ///\n   415:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   416:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   417:     /// ```\n   418:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   419:     pub fn set_broadcast(&self, broadcast: bool) -> io::Result<()> {\n   420:         self.0.set_broadcast(broadcast)\n   421:     }\n   422: \n   423:     /// Gets the value of the `SO_BROADCAST` option for this socket.\n   424:     ///\n   425:     /// For more information about this option, see [`UdpSocket::set_broadcast`].\n   426:     ///\n   427:     /// # Examples\n   428:     ///\n   429:     /// ```no_run\n   430:     /// use std::net::UdpSocket;\n   431:     ///\n   432:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   433:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   434:     /// assert_eq!(socket.broadcast().unwrap(), false);\n   435:     /// ```",
    "nanvix_source": "   409:     ///\n   410:     /// # Examples\n   411:     ///\n   412:     /// ```no_run\n   413:     /// use std::net::UdpSocket;\n   414:     ///\n   415:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   416:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   417:     /// ```\n   418:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   419:     pub fn set_broadcast(&self, broadcast: bool) -> io::Result<()> {\n   420:         self.0.set_broadcast(broadcast)\n   421:     }\n   422: \n   423:     /// Gets the value of the `SO_BROADCAST` option for this socket.\n   424:     ///\n   425:     /// For more information about this option, see [`UdpSocket::set_broadcast`].\n   426:     ///\n   427:     /// # Examples\n   428:     ///\n   429:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_multicast_loop_v4",
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
      "name": "set_multicast_loop_v4",
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
            "multicast_loop_v4",
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
    "verification_source": "   439:     }\n   440: \n   441:     /// Sets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   442:     ///\n   443:     /// If enabled, multicast packets will be looped back to the local socket.\n   444:     /// Note that this might not have any effect on IPv6 sockets.\n   445:     ///\n   446:     /// # Examples\n   447:     ///\n   448:     /// ```no_run\n   449:     /// use std::net::UdpSocket;\n   450:     ///\n   451:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   452:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   453:     /// ```\n   454:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   455:     pub fn set_multicast_loop_v4(&self, multicast_loop_v4: bool) -> io::Result<()> {\n   456:         self.0.set_multicast_loop_v4(multicast_loop_v4)\n   457:     }\n   458: \n   459:     /// Gets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   460:     ///\n   461:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v4`].\n   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```no_run\n   466:     /// use std::net::UdpSocket;\n   467:     ///\n   468:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   469:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   470:     /// assert_eq!(socket.multicast_loop_v4().unwrap(), false);\n   471:     /// ```",
    "nanvix_source": "   445:     ///\n   446:     /// # Examples\n   447:     ///\n   448:     /// ```no_run\n   449:     /// use std::net::UdpSocket;\n   450:     ///\n   451:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   452:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   453:     /// ```\n   454:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   455:     pub fn set_multicast_loop_v4(&self, multicast_loop_v4: bool) -> io::Result<()> {\n   456:         self.0.set_multicast_loop_v4(multicast_loop_v4)\n   457:     }\n   458: \n   459:     /// Gets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   460:     ///\n   461:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v4`].\n   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_multicast_loop_v6",
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
      "name": "set_multicast_loop_v6",
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
            "multicast_loop_v6",
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
    "verification_source": "   514:     }\n   515: \n   516:     /// Sets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   517:     ///\n   518:     /// Controls whether this socket sees the multicast packets it sends itself.\n   519:     /// Note that this might not have any affect on IPv4 sockets.\n   520:     ///\n   521:     /// # Examples\n   522:     ///\n   523:     /// ```no_run\n   524:     /// use std::net::UdpSocket;\n   525:     ///\n   526:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   527:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   528:     /// ```\n   529:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   530:     pub fn set_multicast_loop_v6(&self, multicast_loop_v6: bool) -> io::Result<()> {\n   531:         self.0.set_multicast_loop_v6(multicast_loop_v6)\n   532:     }\n   533: \n   534:     /// Gets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   535:     ///\n   536:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v6`].\n   537:     ///\n   538:     /// # Examples\n   539:     ///\n   540:     /// ```no_run\n   541:     /// use std::net::UdpSocket;\n   542:     ///\n   543:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   544:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   545:     /// assert_eq!(socket.multicast_loop_v6().unwrap(), false);\n   546:     /// ```",
    "nanvix_source": "   520:     ///\n   521:     /// # Examples\n   522:     ///\n   523:     /// ```no_run\n   524:     /// use std::net::UdpSocket;\n   525:     ///\n   526:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   527:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   528:     /// ```\n   529:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   530:     pub fn set_multicast_loop_v6(&self, multicast_loop_v6: bool) -> io::Result<()> {\n   531:         self.0.set_multicast_loop_v6(multicast_loop_v6)\n   532:     }\n   533: \n   534:     /// Gets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   535:     ///\n   536:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v6`].\n   537:     ///\n   538:     /// # Examples\n   539:     ///\n   540:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_multicast_ttl_v4",
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
      "name": "set_multicast_ttl_v4",
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
            "multicast_ttl_v4",
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
    "verification_source": "   478:     ///\n   479:     /// Indicates the time-to-live value of outgoing multicast packets for\n   480:     /// this socket. The default value is 1 which means that multicast packets\n   481:     /// don't leave the local network unless explicitly requested.\n   482:     ///\n   483:     /// Note that this might not have any effect on IPv6 sockets.\n   484:     ///\n   485:     /// # Examples\n   486:     ///\n   487:     /// ```no_run\n   488:     /// use std::net::UdpSocket;\n   489:     ///\n   490:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   491:     /// socket.set_multicast_ttl_v4(42).expect(\"set_multicast_ttl_v4 call failed\");\n   492:     /// ```\n   493:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   494:     pub fn set_multicast_ttl_v4(&self, multicast_ttl_v4: u32) -> io::Result<()> {\n   495:         self.0.set_multicast_ttl_v4(multicast_ttl_v4)\n   496:     }\n   497: \n   498:     /// Gets the value of the `IP_MULTICAST_TTL` option for this socket.\n   499:     ///\n   500:     /// For more information about this option, see [`UdpSocket::set_multicast_ttl_v4`].\n   501:     ///\n   502:     /// # Examples\n   503:     ///\n   504:     /// ```no_run\n   505:     /// use std::net::UdpSocket;\n   506:     ///\n   507:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   508:     /// socket.set_multicast_ttl_v4(42).expect(\"set_multicast_ttl_v4 call failed\");\n   509:     /// assert_eq!(socket.multicast_ttl_v4().unwrap(), 42);\n   510:     /// ```",
    "nanvix_source": "   484:     ///\n   485:     /// # Examples\n   486:     ///\n   487:     /// ```no_run\n   488:     /// use std::net::UdpSocket;\n   489:     ///\n   490:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   491:     /// socket.set_multicast_ttl_v4(42).expect(\"set_multicast_ttl_v4 call failed\");\n   492:     /// ```\n   493:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   494:     pub fn set_multicast_ttl_v4(&self, multicast_ttl_v4: u32) -> io::Result<()> {\n   495:         self.0.set_multicast_ttl_v4(multicast_ttl_v4)\n   496:     }\n   497: \n   498:     /// Gets the value of the `IP_MULTICAST_TTL` option for this socket.\n   499:     ///\n   500:     /// For more information about this option, see [`UdpSocket::set_multicast_ttl_v4`].\n   501:     ///\n   502:     /// # Examples\n   503:     ///\n   504:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::set_nonblocking",
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
    "verification_source": "   800:     /// use std::net::UdpSocket;\n   801:     ///\n   802:     /// let socket = UdpSocket::bind(\"127.0.0.1:7878\").unwrap();\n   803:     /// socket.set_nonblocking(true).unwrap();\n   804:     ///\n   805:     /// # fn wait_for_fd() { unimplemented!() }\n   806:     /// let mut buf = [0; 10];\n   807:     /// let (num_bytes_read, _) = loop {\n   808:     ///     match socket.recv_from(&mut buf) {\n   809:     ///         Ok(n) => break n,\n   810:     ///         Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {\n   811:     ///             // wait until network socket is ready, typically implemented\n   812:     ///             // via platform-specific APIs such as epoll or IOCP\n   813:     ///             wait_for_fd();\n   814:     ///         }\n   815:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n   816:     ///     }\n   817:     /// };\n   818:     /// println!(\"bytes: {:?}\", &buf[..num_bytes_read]);\n   819:     /// ```\n   820:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   821:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   822:         self.0.set_nonblocking(nonblocking)\n   823:     }\n   824: }\n   825: \n   826: // In addition to the `impl`s here, `UdpSocket` also has `impl`s for\n   827: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n   828: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n   829: // `AsSocket`/`From<OwnedSocket>`/`Into<OwnedSocket>` and\n   830: // `AsRawSocket`/`IntoRawSocket`/`FromRawSocket` on Windows.\n   831: \n   832: impl AsInner<net_imp::UdpSocket> for UdpSocket {",
    "nanvix_source": "   806:     /// let mut buf = [0; 10];\n   807:     /// let (num_bytes_read, _) = loop {\n   808:     ///     match socket.recv_from(&mut buf) {\n   809:     ///         Ok(n) => break n,\n   810:     ///         Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {\n   811:     ///             // wait until network socket is ready, typically implemented\n   812:     ///             // via platform-specific APIs such as epoll or IOCP\n   813:     ///             wait_for_fd();\n   814:     ///         }\n   815:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n   816:     ///     }\n   817:     /// };\n   818:     /// println!(\"bytes: {:?}\", &buf[..num_bytes_read]);\n   819:     /// ```\n   820:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   821:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   822:         self.0.set_nonblocking(nonblocking)\n   823:     }\n   824: }\n   825: \n   826: // In addition to the `impl`s here, `UdpSocket` also has `impl`s for",
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
