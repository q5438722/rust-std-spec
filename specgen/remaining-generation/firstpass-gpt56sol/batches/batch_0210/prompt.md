For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::leave_multicast_v6",
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
      "name": "leave_multicast_v6",
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
            "multiaddr",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 4667,
                    "path": "Ipv6Addr"
                  }
                }
              }
            }
          ],
          [
            "interface",
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
    "verification_source": "   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }\n   617: \n   618:     /// Executes an operation of the `IPV6_DROP_MEMBERSHIP` type.\n   619:     ///\n   620:     /// For more information about this option, see [`UdpSocket::join_multicast_v6`].\n   621:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   622:     pub fn leave_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   623:         self.0.leave_multicast_v6(multiaddr, interface)\n   624:     }\n   625: \n   626:     /// Gets the value of the `SO_ERROR` option on this socket.\n   627:     ///\n   628:     /// This will retrieve the stored error in the underlying socket, clearing\n   629:     /// the field in the process. This can be useful for checking errors between\n   630:     /// calls.\n   631:     ///\n   632:     /// # Examples\n   633:     ///\n   634:     /// ```no_run\n   635:     /// use std::net::UdpSocket;\n   636:     ///\n   637:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   638:     /// match socket.take_error() {",
    "nanvix_source": "   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }\n   617: \n   618:     /// Executes an operation of the `IPV6_DROP_MEMBERSHIP` type.\n   619:     ///\n   620:     /// For more information about this option, see [`UdpSocket::join_multicast_v6`].\n   621:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   622:     pub fn leave_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   623:         self.0.leave_multicast_v6(multiaddr, interface)\n   624:     }\n   625: \n   626:     /// Gets the value of the `SO_ERROR` option on this socket.\n   627:     ///\n   628:     /// This will retrieve the stored error in the underlying socket, clearing\n   629:     /// the field in the process. This can be useful for checking errors between\n   630:     /// calls.\n   631:     ///\n   632:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::local_addr",
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
      "name": "local_addr",
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
    "verification_source": "   240:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   241:         self.0.peer_addr()\n   242:     }\n   243: \n   244:     /// Returns the socket address that this socket was created from.\n   245:     ///\n   246:     /// # Examples\n   247:     ///\n   248:     /// ```no_run\n   249:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};\n   250:     ///\n   251:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   252:     /// assert_eq!(socket.local_addr().unwrap(),\n   253:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 34254)));\n   254:     /// ```\n   255:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   256:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   257:         self.0.socket_addr()\n   258:     }\n   259: \n   260:     /// Creates a new independently owned handle to the underlying socket.\n   261:     ///\n   262:     /// The returned `UdpSocket` is a reference to the same socket that this\n   263:     /// object references. Both handles will read and write the same port, and\n   264:     /// options set on one socket will be propagated to the other.\n   265:     ///\n   266:     /// # Examples\n   267:     ///\n   268:     /// ```no_run\n   269:     /// use std::net::UdpSocket;\n   270:     ///\n   271:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   272:     /// let socket_clone = socket.try_clone().expect(\"couldn't clone the socket\");",
    "nanvix_source": "   246:     /// # Examples\n   247:     ///\n   248:     /// ```no_run\n   249:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};\n   250:     ///\n   251:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   252:     /// assert_eq!(socket.local_addr().unwrap(),\n   253:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 34254)));\n   254:     /// ```\n   255:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   256:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   257:         self.0.socket_addr()\n   258:     }\n   259: \n   260:     /// Creates a new independently owned handle to the underlying socket.\n   261:     ///\n   262:     /// The returned `UdpSocket` is a reference to the same socket that this\n   263:     /// object references. Both handles will read and write the same port, and\n   264:     /// options set on one socket will be propagated to the other.\n   265:     ///\n   266:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::multicast_loop_v4",
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
      "name": "multicast_loop_v4",
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
                      "primitive": "bool"
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
    "verification_source": "   457:     }\n   458: \n   459:     /// Gets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   460:     ///\n   461:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v4`].\n   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```no_run\n   466:     /// use std::net::UdpSocket;\n   467:     ///\n   468:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   469:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   470:     /// assert_eq!(socket.multicast_loop_v4().unwrap(), false);\n   471:     /// ```\n   472:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   473:     pub fn multicast_loop_v4(&self) -> io::Result<bool> {\n   474:         self.0.multicast_loop_v4()\n   475:     }\n   476: \n   477:     /// Sets the value of the `IP_MULTICAST_TTL` option for this socket.\n   478:     ///\n   479:     /// Indicates the time-to-live value of outgoing multicast packets for\n   480:     /// this socket. The default value is 1 which means that multicast packets\n   481:     /// don't leave the local network unless explicitly requested.\n   482:     ///\n   483:     /// Note that this might not have any effect on IPv6 sockets.\n   484:     ///\n   485:     /// # Examples\n   486:     ///\n   487:     /// ```no_run\n   488:     /// use std::net::UdpSocket;\n   489:     ///",
    "nanvix_source": "   463:     /// # Examples\n   464:     ///\n   465:     /// ```no_run\n   466:     /// use std::net::UdpSocket;\n   467:     ///\n   468:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   469:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   470:     /// assert_eq!(socket.multicast_loop_v4().unwrap(), false);\n   471:     /// ```\n   472:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   473:     pub fn multicast_loop_v4(&self) -> io::Result<bool> {\n   474:         self.0.multicast_loop_v4()\n   475:     }\n   476: \n   477:     /// Sets the value of the `IP_MULTICAST_TTL` option for this socket.\n   478:     ///\n   479:     /// Indicates the time-to-live value of outgoing multicast packets for\n   480:     /// this socket. The default value is 1 which means that multicast packets\n   481:     /// don't leave the local network unless explicitly requested.\n   482:     ///\n   483:     /// Note that this might not have any effect on IPv6 sockets.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::multicast_loop_v6",
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
      "name": "multicast_loop_v6",
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
                      "primitive": "bool"
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
    "verification_source": "   532:     }\n   533: \n   534:     /// Gets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   535:     ///\n   536:     /// For more information about this option, see [`UdpSocket::set_multicast_loop_v6`].\n   537:     ///\n   538:     /// # Examples\n   539:     ///\n   540:     /// ```no_run\n   541:     /// use std::net::UdpSocket;\n   542:     ///\n   543:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   544:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   545:     /// assert_eq!(socket.multicast_loop_v6().unwrap(), false);\n   546:     /// ```\n   547:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   548:     pub fn multicast_loop_v6(&self) -> io::Result<bool> {\n   549:         self.0.multicast_loop_v6()\n   550:     }\n   551: \n   552:     /// Sets the value for the `IP_TTL` option on this socket.\n   553:     ///\n   554:     /// This value sets the time-to-live field that is used in every packet sent\n   555:     /// from this socket.\n   556:     ///\n   557:     /// # Examples\n   558:     ///\n   559:     /// ```no_run\n   560:     /// use std::net::UdpSocket;\n   561:     ///\n   562:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   563:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   564:     /// ```",
    "nanvix_source": "   538:     /// # Examples\n   539:     ///\n   540:     /// ```no_run\n   541:     /// use std::net::UdpSocket;\n   542:     ///\n   543:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   544:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   545:     /// assert_eq!(socket.multicast_loop_v6().unwrap(), false);\n   546:     /// ```\n   547:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   548:     pub fn multicast_loop_v6(&self) -> io::Result<bool> {\n   549:         self.0.multicast_loop_v6()\n   550:     }\n   551: \n   552:     /// Sets the value for the `IP_TTL` option on this socket.\n   553:     ///\n   554:     /// This value sets the time-to-live field that is used in every packet sent\n   555:     /// from this socket.\n   556:     ///\n   557:     /// # Examples\n   558:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::multicast_ttl_v4",
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
      "name": "multicast_ttl_v4",
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
    "verification_source": "   496:     }\n   497: \n   498:     /// Gets the value of the `IP_MULTICAST_TTL` option for this socket.\n   499:     ///\n   500:     /// For more information about this option, see [`UdpSocket::set_multicast_ttl_v4`].\n   501:     ///\n   502:     /// # Examples\n   503:     ///\n   504:     /// ```no_run\n   505:     /// use std::net::UdpSocket;\n   506:     ///\n   507:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   508:     /// socket.set_multicast_ttl_v4(42).expect(\"set_multicast_ttl_v4 call failed\");\n   509:     /// assert_eq!(socket.multicast_ttl_v4().unwrap(), 42);\n   510:     /// ```\n   511:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   512:     pub fn multicast_ttl_v4(&self) -> io::Result<u32> {\n   513:         self.0.multicast_ttl_v4()\n   514:     }\n   515: \n   516:     /// Sets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   517:     ///\n   518:     /// Controls whether this socket sees the multicast packets it sends itself.\n   519:     /// Note that this might not have any affect on IPv4 sockets.\n   520:     ///\n   521:     /// # Examples\n   522:     ///\n   523:     /// ```no_run\n   524:     /// use std::net::UdpSocket;\n   525:     ///\n   526:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   527:     /// socket.set_multicast_loop_v6(false).expect(\"set_multicast_loop_v6 call failed\");\n   528:     /// ```",
    "nanvix_source": "   502:     /// # Examples\n   503:     ///\n   504:     /// ```no_run\n   505:     /// use std::net::UdpSocket;\n   506:     ///\n   507:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   508:     /// socket.set_multicast_ttl_v4(42).expect(\"set_multicast_ttl_v4 call failed\");\n   509:     /// assert_eq!(socket.multicast_ttl_v4().unwrap(), 42);\n   510:     /// ```\n   511:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   512:     pub fn multicast_ttl_v4(&self) -> io::Result<u32> {\n   513:         self.0.multicast_ttl_v4()\n   514:     }\n   515: \n   516:     /// Sets the value of the `IPV6_MULTICAST_LOOP` option for this socket.\n   517:     ///\n   518:     /// Controls whether this socket sees the multicast packets it sends itself.\n   519:     /// Note that this might not have any affect on IPv4 sockets.\n   520:     ///\n   521:     /// # Examples\n   522:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::peek",
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
      "name": "peek",
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
    "verification_source": "   760:     /// will connect this socket to a remote address.\n   761:     ///\n   762:     /// # Examples\n   763:     ///\n   764:     /// ```no_run\n   765:     /// use std::net::UdpSocket;\n   766:     ///\n   767:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   768:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   769:     /// let mut buf = [0; 10];\n   770:     /// match socket.peek(&mut buf) {\n   771:     ///     Ok(received) => println!(\"received {received} bytes\"),\n   772:     ///     Err(e) => println!(\"peek function failed: {e:?}\"),\n   773:     /// }\n   774:     /// ```\n   775:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   776:     pub fn peek(&self, buf: &mut [u8]) -> io::Result<usize> {\n   777:         self.0.peek(buf)\n   778:     }\n   779: \n   780:     /// Moves this UDP socket into or out of nonblocking mode.\n   781:     ///\n   782:     /// This will result in `recv`, `recv_from`, `send`, and `send_to` system\n   783:     /// operations becoming nonblocking, i.e., immediately returning from their\n   784:     /// calls. If the IO operation is successful, `Ok` is returned and no\n   785:     /// further action is required. If the IO operation could not be completed\n   786:     /// and needs to be retried, an error with kind\n   787:     /// [`io::ErrorKind::WouldBlock`] is returned.\n   788:     ///\n   789:     /// On Unix platforms, calling this method corresponds to calling `fcntl`\n   790:     /// `FIONBIO`. On Windows calling this method corresponds to calling\n   791:     /// `ioctlsocket` `FIONBIO`.\n   792:     ///",
    "nanvix_source": "   766:     ///\n   767:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   768:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   769:     /// let mut buf = [0; 10];\n   770:     /// match socket.peek(&mut buf) {\n   771:     ///     Ok(received) => println!(\"received {received} bytes\"),\n   772:     ///     Err(e) => println!(\"peek function failed: {e:?}\"),\n   773:     /// }\n   774:     /// ```\n   775:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   776:     pub fn peek(&self, buf: &mut [u8]) -> io::Result<usize> {\n   777:         self.0.peek(buf)\n   778:     }\n   779: \n   780:     /// Moves this UDP socket into or out of nonblocking mode.\n   781:     ///\n   782:     /// This will result in `recv`, `recv_from`, `send`, and `send_to` system\n   783:     /// operations becoming nonblocking, i.e., immediately returning from their\n   784:     /// calls. If the IO operation is successful, `Ok` is returned and no\n   785:     /// further action is required. If the IO operation could not be completed\n   786:     /// and needs to be retried, an error with kind",
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
