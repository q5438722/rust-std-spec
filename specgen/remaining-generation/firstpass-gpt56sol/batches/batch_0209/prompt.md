For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::bind",
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
      "name": "bind",
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
    "verification_source": "   105:     /// ```no_run\n   106:     /// use std::net::UdpSocket;\n   107:     ///\n   108:     /// let socket = UdpSocket::bind(\"127.0.0.1:0\").unwrap();\n   109:     /// ```\n   110:     ///\n   111:     /// Note that `bind` declares the scope of your network connection.\n   112:     /// You can only receive datagrams from and send datagrams to\n   113:     /// participants in that view of the network.\n   114:     /// For instance, binding to a loopback address as in the example\n   115:     /// above will prevent you from sending datagrams to another device\n   116:     /// in your local network.\n   117:     ///\n   118:     /// In order to limit your view of the network the least, `bind` to\n   119:     /// [`Ipv4Addr::UNSPECIFIED`] or [`Ipv6Addr::UNSPECIFIED`].\n   120:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   121:     pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<UdpSocket> {\n   122:         net_imp::UdpSocket::bind(addr).map(UdpSocket)\n   123:     }\n   124: \n   125:     /// Receives a single datagram message on the socket. On success, returns the number\n   126:     /// of bytes read and the origin.\n   127:     ///\n   128:     /// The function must be called with valid byte array `buf` of sufficient size to\n   129:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   130:     /// excess bytes may be discarded.\n   131:     ///\n   132:     /// Refer to the platform-specific documentation on this function; it is considered\n   133:     /// correct for its behavior to differ from [`UdpSocket::recv`] if the underlying system\n   134:     /// call does so.\n   135:     ///\n   136:     /// # Examples\n   137:     ///",
    "nanvix_source": "   111:     /// Note that `bind` declares the scope of your network connection.\n   112:     /// You can only receive datagrams from and send datagrams to\n   113:     /// participants in that view of the network.\n   114:     /// For instance, binding to a loopback address as in the example\n   115:     /// above will prevent you from sending datagrams to another device\n   116:     /// in your local network.\n   117:     ///\n   118:     /// In order to limit your view of the network the least, `bind` to\n   119:     /// [`Ipv4Addr::UNSPECIFIED`] or [`Ipv6Addr::UNSPECIFIED`].\n   120:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   121:     pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<UdpSocket> {\n   122:         net_imp::UdpSocket::bind(addr).map(UdpSocket)\n   123:     }\n   124: \n   125:     /// Receives a single datagram message on the socket. On success, returns the number\n   126:     /// of bytes read and the origin.\n   127:     ///\n   128:     /// The function must be called with valid byte array `buf` of sufficient size to\n   129:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   130:     /// excess bytes may be discarded.\n   131:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::broadcast",
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
      "name": "broadcast",
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
    "verification_source": "   421:     }\n   422: \n   423:     /// Gets the value of the `SO_BROADCAST` option for this socket.\n   424:     ///\n   425:     /// For more information about this option, see [`UdpSocket::set_broadcast`].\n   426:     ///\n   427:     /// # Examples\n   428:     ///\n   429:     /// ```no_run\n   430:     /// use std::net::UdpSocket;\n   431:     ///\n   432:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   433:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   434:     /// assert_eq!(socket.broadcast().unwrap(), false);\n   435:     /// ```\n   436:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   437:     pub fn broadcast(&self) -> io::Result<bool> {\n   438:         self.0.broadcast()\n   439:     }\n   440: \n   441:     /// Sets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   442:     ///\n   443:     /// If enabled, multicast packets will be looped back to the local socket.\n   444:     /// Note that this might not have any effect on IPv6 sockets.\n   445:     ///\n   446:     /// # Examples\n   447:     ///\n   448:     /// ```no_run\n   449:     /// use std::net::UdpSocket;\n   450:     ///\n   451:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   452:     /// socket.set_multicast_loop_v4(false).expect(\"set_multicast_loop_v4 call failed\");\n   453:     /// ```",
    "nanvix_source": "   427:     /// # Examples\n   428:     ///\n   429:     /// ```no_run\n   430:     /// use std::net::UdpSocket;\n   431:     ///\n   432:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   433:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   434:     /// assert_eq!(socket.broadcast().unwrap(), false);\n   435:     /// ```\n   436:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   437:     pub fn broadcast(&self) -> io::Result<bool> {\n   438:         self.0.broadcast()\n   439:     }\n   440: \n   441:     /// Sets the value of the `IP_MULTICAST_LOOP` option for this socket.\n   442:     ///\n   443:     /// If enabled, multicast packets will be looped back to the local socket.\n   444:     /// Note that this might not have any effect on IPv6 sockets.\n   445:     ///\n   446:     /// # Examples\n   447:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::connect",
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
      "name": "connect",
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
    "verification_source": "   666:     /// ```no_run\n   667:     /// use std::net::UdpSocket;\n   668:     ///\n   669:     /// let socket = UdpSocket::bind(\"127.0.0.1:3400\").expect(\"couldn't bind to address\");\n   670:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   671:     /// ```\n   672:     ///\n   673:     /// Unlike in the TCP case, passing an array of addresses to the `connect`\n   674:     /// function of a UDP socket is not a useful thing to do: The OS will be\n   675:     /// unable to determine whether something is listening on the remote\n   676:     /// address without the application sending data.\n   677:     ///\n   678:     /// If your first `connect` is to a loopback address, subsequent\n   679:     /// `connect`s to non-loopback addresses might fail, depending\n   680:     /// on the platform.\n   681:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   682:     pub fn connect<A: ToSocketAddrs>(&self, addr: A) -> io::Result<()> {\n   683:         self.0.connect(addr)\n   684:     }\n   685: \n   686:     /// Sends data on the socket to the remote address to which it is connected.\n   687:     /// On success, returns the number of bytes written. Note that the operating\n   688:     /// system may refuse buffers larger than 65507. However, partial writes are\n   689:     /// not possible until buffer sizes above `i32::MAX`.\n   690:     ///\n   691:     /// [`UdpSocket::connect`] will connect this socket to a remote address. This\n   692:     /// method will fail if the socket is not connected.\n   693:     ///\n   694:     /// # Examples\n   695:     ///\n   696:     /// ```no_run\n   697:     /// use std::net::UdpSocket;\n   698:     ///",
    "nanvix_source": "   672:     ///\n   673:     /// Unlike in the TCP case, passing an array of addresses to the `connect`\n   674:     /// function of a UDP socket is not a useful thing to do: The OS will be\n   675:     /// unable to determine whether something is listening on the remote\n   676:     /// address without the application sending data.\n   677:     ///\n   678:     /// If your first `connect` is to a loopback address, subsequent\n   679:     /// `connect`s to non-loopback addresses might fail, depending\n   680:     /// on the platform.\n   681:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   682:     pub fn connect<A: ToSocketAddrs>(&self, addr: A) -> io::Result<()> {\n   683:         self.0.connect(addr)\n   684:     }\n   685: \n   686:     /// Sends data on the socket to the remote address to which it is connected.\n   687:     /// On success, returns the number of bytes written. Note that the operating\n   688:     /// system may refuse buffers larger than 65507. However, partial writes are\n   689:     /// not possible until buffer sizes above `i32::MAX`.\n   690:     ///\n   691:     /// [`UdpSocket::connect`] will connect this socket to a remote address. This\n   692:     /// method will fail if the socket is not connected.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::join_multicast_v4",
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
      "name": "join_multicast_v4",
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
                    "id": 4665,
                    "path": "Ipv4Addr"
                  }
                }
              }
            }
          ],
          [
            "interface",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 4665,
                    "path": "Ipv4Addr"
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
    "verification_source": "   580:     /// socket.set_ttl(42).expect(\"set_ttl call failed\");\n   581:     /// assert_eq!(socket.ttl().unwrap(), 42);\n   582:     /// ```\n   583:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   584:     pub fn ttl(&self) -> io::Result<u32> {\n   585:         self.0.ttl()\n   586:     }\n   587: \n   588:     /// Executes an operation of the `IP_ADD_MEMBERSHIP` type.\n   589:     ///\n   590:     /// This function specifies a new multicast group for this socket to join.\n   591:     /// The address must be a valid multicast address, and `interface` is the\n   592:     /// address of the local interface with which the system should join the\n   593:     /// multicast group. If it's equal to [`UNSPECIFIED`](Ipv4Addr::UNSPECIFIED)\n   594:     /// then an appropriate interface is chosen by the system.\n   595:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   596:     pub fn join_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   597:         self.0.join_multicast_v4(multiaddr, interface)\n   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.\n   601:     ///\n   602:     /// This function specifies a new multicast group for this socket to join.\n   603:     /// The address must be a valid multicast address, and `interface` is the\n   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].",
    "nanvix_source": "   586:     }\n   587: \n   588:     /// Executes an operation of the `IP_ADD_MEMBERSHIP` type.\n   589:     ///\n   590:     /// This function specifies a new multicast group for this socket to join.\n   591:     /// The address must be a valid multicast address, and `interface` is the\n   592:     /// address of the local interface with which the system should join the\n   593:     /// multicast group. If it's equal to [`UNSPECIFIED`](Ipv4Addr::UNSPECIFIED)\n   594:     /// then an appropriate interface is chosen by the system.\n   595:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   596:     pub fn join_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   597:         self.0.join_multicast_v4(multiaddr, interface)\n   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.\n   601:     ///\n   602:     /// This function specifies a new multicast group for this socket to join.\n   603:     /// The address must be a valid multicast address, and `interface` is the\n   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::join_multicast_v6",
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
      "name": "join_multicast_v6",
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
    "verification_source": "   590:     /// This function specifies a new multicast group for this socket to join.\n   591:     /// The address must be a valid multicast address, and `interface` is the\n   592:     /// address of the local interface with which the system should join the\n   593:     /// multicast group. If it's equal to [`UNSPECIFIED`](Ipv4Addr::UNSPECIFIED)\n   594:     /// then an appropriate interface is chosen by the system.\n   595:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   596:     pub fn join_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   597:         self.0.join_multicast_v4(multiaddr, interface)\n   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.\n   601:     ///\n   602:     /// This function specifies a new multicast group for this socket to join.\n   603:     /// The address must be a valid multicast address, and `interface` is the\n   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }\n   617: \n   618:     /// Executes an operation of the `IPV6_DROP_MEMBERSHIP` type.\n   619:     ///\n   620:     /// For more information about this option, see [`UdpSocket::join_multicast_v6`].\n   621:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   622:     pub fn leave_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {",
    "nanvix_source": "   596:     pub fn join_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   597:         self.0.join_multicast_v4(multiaddr, interface)\n   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.\n   601:     ///\n   602:     /// This function specifies a new multicast group for this socket to join.\n   603:     /// The address must be a valid multicast address, and `interface` is the\n   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::leave_multicast_v4",
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
      "name": "leave_multicast_v4",
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
                    "id": 4665,
                    "path": "Ipv4Addr"
                  }
                }
              }
            }
          ],
          [
            "interface",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 4665,
                    "path": "Ipv4Addr"
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
    "verification_source": "   598:     }\n   599: \n   600:     /// Executes an operation of the `IPV6_ADD_MEMBERSHIP` type.\n   601:     ///\n   602:     /// This function specifies a new multicast group for this socket to join.\n   603:     /// The address must be a valid multicast address, and `interface` is the\n   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }\n   617: \n   618:     /// Executes an operation of the `IPV6_DROP_MEMBERSHIP` type.\n   619:     ///\n   620:     /// For more information about this option, see [`UdpSocket::join_multicast_v6`].\n   621:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   622:     pub fn leave_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   623:         self.0.leave_multicast_v6(multiaddr, interface)\n   624:     }\n   625: \n   626:     /// Gets the value of the `SO_ERROR` option on this socket.\n   627:     ///\n   628:     /// This will retrieve the stored error in the underlying socket, clearing\n   629:     /// the field in the process. This can be useful for checking errors between\n   630:     /// calls.",
    "nanvix_source": "   604:     /// index of the interface to join/leave (or 0 to indicate any interface).\n   605:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   606:     pub fn join_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   607:         self.0.join_multicast_v6(multiaddr, interface)\n   608:     }\n   609: \n   610:     /// Executes an operation of the `IP_DROP_MEMBERSHIP` type.\n   611:     ///\n   612:     /// For more information about this option, see [`UdpSocket::join_multicast_v4`].\n   613:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   614:     pub fn leave_multicast_v4(&self, multiaddr: &Ipv4Addr, interface: &Ipv4Addr) -> io::Result<()> {\n   615:         self.0.leave_multicast_v4(multiaddr, interface)\n   616:     }\n   617: \n   618:     /// Executes an operation of the `IPV6_DROP_MEMBERSHIP` type.\n   619:     ///\n   620:     /// For more information about this option, see [`UdpSocket::join_multicast_v6`].\n   621:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   622:     pub fn leave_multicast_v6(&self, multiaddr: &Ipv6Addr, interface: u32) -> io::Result<()> {\n   623:         self.0.leave_multicast_v6(multiaddr, interface)\n   624:     }",
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
