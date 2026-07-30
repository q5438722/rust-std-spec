For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::SocketAddrV6::port",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "port",
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
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
          "primitive": "u16"
        }
      }
    },
    "verification_source": "   464:     }\n   465: \n   466:     /// Returns the port number associated with this socket address.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   472:     ///\n   473:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   474:     /// assert_eq!(socket.port(), 8080);\n   475:     /// ```\n   476:     #[must_use]\n   477:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   478:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   479:     #[inline]\n   480:     pub const fn port(&self) -> u16 {\n   481:         self.port\n   482:     }\n   483: \n   484:     /// Changes the port number associated with this socket address.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   490:     ///\n   491:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   492:     /// socket.set_port(4242);\n   493:     /// assert_eq!(socket.port(), 4242);\n   494:     /// ```\n   495:     #[inline]\n   496:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]",
    "nanvix_source": "   470:     /// ```\n   471:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   472:     ///\n   473:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   474:     /// assert_eq!(socket.port(), 8080);\n   475:     /// ```\n   476:     #[must_use]\n   477:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   478:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   479:     #[inline]\n   480:     pub const fn port(&self) -> u16 {\n   481:         self.port\n   482:     }\n   483: \n   484:     /// Changes the port number associated with this socket address.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   490:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::scope_id",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "scope_id",
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
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   553:     /// as specified in [IETF RFC 2553, Section 3.3].\n   554:     ///\n   555:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   556:     ///\n   557:     /// # Examples\n   558:     ///\n   559:     /// ```\n   560:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   561:     ///\n   562:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);\n   563:     /// assert_eq!(socket.scope_id(), 78);\n   564:     /// ```\n   565:     #[must_use]\n   566:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   567:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   568:     #[inline]\n   569:     pub const fn scope_id(&self) -> u32 {\n   570:         self.scope_id\n   571:     }\n   572: \n   573:     /// Changes the scope ID associated with this socket address.\n   574:     ///\n   575:     /// See [`SocketAddrV6::scope_id`]'s documentation for more details.\n   576:     ///\n   577:     /// # Examples\n   578:     ///\n   579:     /// ```\n   580:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   581:     ///\n   582:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);\n   583:     /// socket.set_scope_id(42);\n   584:     /// assert_eq!(socket.scope_id(), 42);\n   585:     /// ```",
    "nanvix_source": "   559:     /// ```\n   560:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   561:     ///\n   562:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);\n   563:     /// assert_eq!(socket.scope_id(), 78);\n   564:     /// ```\n   565:     #[must_use]\n   566:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   567:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   568:     #[inline]\n   569:     pub const fn scope_id(&self) -> u32 {\n   570:         self.scope_id\n   571:     }\n   572: \n   573:     /// Changes the scope ID associated with this socket address.\n   574:     ///\n   575:     /// See [`SocketAddrV6::scope_id`]'s documentation for more details.\n   576:     ///\n   577:     /// # Examples\n   578:     ///\n   579:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::set_flowinfo",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_flowinfo",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
            "new_flowinfo",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   530:     /// Changes the flow information associated with this socket address.\n   531:     ///\n   532:     /// See [`SocketAddrV6::flowinfo`]'s documentation for more details.\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   538:     ///\n   539:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 10, 0);\n   540:     /// socket.set_flowinfo(56);\n   541:     /// assert_eq!(socket.flowinfo(), 56);\n   542:     /// ```\n   543:     #[inline]\n   544:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   545:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   546:     pub const fn set_flowinfo(&mut self, new_flowinfo: u32) {\n   547:         self.flowinfo = new_flowinfo;\n   548:     }\n   549: \n   550:     /// Returns the scope ID associated with this address.\n   551:     ///\n   552:     /// This information corresponds to the `sin6_scope_id` field in C's `netinet/in.h`,\n   553:     /// as specified in [IETF RFC 2553, Section 3.3].\n   554:     ///\n   555:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   556:     ///\n   557:     /// # Examples\n   558:     ///\n   559:     /// ```\n   560:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   561:     ///\n   562:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);",
    "nanvix_source": "   536:     /// ```\n   537:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   538:     ///\n   539:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 10, 0);\n   540:     /// socket.set_flowinfo(56);\n   541:     /// assert_eq!(socket.flowinfo(), 56);\n   542:     /// ```\n   543:     #[inline]\n   544:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   545:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   546:     pub const fn set_flowinfo(&mut self, new_flowinfo: u32) {\n   547:         self.flowinfo = new_flowinfo;\n   548:     }\n   549: \n   550:     /// Returns the scope ID associated with this address.\n   551:     ///\n   552:     /// This information corresponds to the `sin6_scope_id` field in C's `netinet/in.h`,\n   553:     /// as specified in [IETF RFC 2553, Section 3.3].\n   554:     ///\n   555:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   556:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::set_ip",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_ip",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
            "new_ip",
            {
              "resolved_path": {
                "args": null,
                "id": 9949,
                "path": "Ipv6Addr"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   446:     }\n   447: \n   448:     /// Changes the IP address associated with this socket address.\n   449:     ///\n   450:     /// # Examples\n   451:     ///\n   452:     /// ```\n   453:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   454:     ///\n   455:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   456:     /// socket.set_ip(Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   457:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   458:     /// ```\n   459:     #[inline]\n   460:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   461:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   462:     pub const fn set_ip(&mut self, new_ip: Ipv6Addr) {\n   463:         self.ip = new_ip;\n   464:     }\n   465: \n   466:     /// Returns the port number associated with this socket address.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   472:     ///\n   473:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   474:     /// assert_eq!(socket.port(), 8080);\n   475:     /// ```\n   476:     #[must_use]\n   477:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   478:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]",
    "nanvix_source": "   452:     /// ```\n   453:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   454:     ///\n   455:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   456:     /// socket.set_ip(Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   457:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   458:     /// ```\n   459:     #[inline]\n   460:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   461:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   462:     pub const fn set_ip(&mut self, new_ip: Ipv6Addr) {\n   463:         self.ip = new_ip;\n   464:     }\n   465: \n   466:     /// Returns the port number associated with this socket address.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   472:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::set_port",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_port",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
            "new_port",
            {
              "primitive": "u16"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   482:     }\n   483: \n   484:     /// Changes the port number associated with this socket address.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   490:     ///\n   491:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   492:     /// socket.set_port(4242);\n   493:     /// assert_eq!(socket.port(), 4242);\n   494:     /// ```\n   495:     #[inline]\n   496:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   497:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   498:     pub const fn set_port(&mut self, new_port: u16) {\n   499:         self.port = new_port;\n   500:     }\n   501: \n   502:     /// Returns the flow information associated with this address.\n   503:     ///\n   504:     /// This information corresponds to the `sin6_flowinfo` field in C's `netinet/in.h`,\n   505:     /// as specified in [IETF RFC 2553, Section 3.3].\n   506:     /// It combines information about the flow label and the traffic class as specified\n   507:     /// in [IETF RFC 2460], respectively [Section 6] and [Section 7].\n   508:     ///\n   509:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   510:     /// [IETF RFC 2460]: https://tools.ietf.org/html/rfc2460\n   511:     /// [Section 6]: https://tools.ietf.org/html/rfc2460#section-6\n   512:     /// [Section 7]: https://tools.ietf.org/html/rfc2460#section-7\n   513:     ///\n   514:     /// # Examples",
    "nanvix_source": "   488:     /// ```\n   489:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   490:     ///\n   491:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   492:     /// socket.set_port(4242);\n   493:     /// assert_eq!(socket.port(), 4242);\n   494:     /// ```\n   495:     #[inline]\n   496:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   497:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   498:     pub const fn set_port(&mut self, new_port: u16) {\n   499:         self.port = new_port;\n   500:     }\n   501: \n   502:     /// Returns the flow information associated with this address.\n   503:     ///\n   504:     /// This information corresponds to the `sin6_flowinfo` field in C's `netinet/in.h`,\n   505:     /// as specified in [IETF RFC 2553, Section 3.3].\n   506:     /// It combines information about the flow label and the traffic class as specified\n   507:     /// in [IETF RFC 2460], respectively [Section 6] and [Section 7].\n   508:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::set_scope_id",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_scope_id",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 9964,
            "path": "SocketAddrV6"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27981",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9964",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV6"
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
            "new_scope_id",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   573:     /// Changes the scope ID associated with this socket address.\n   574:     ///\n   575:     /// See [`SocketAddrV6::scope_id`]'s documentation for more details.\n   576:     ///\n   577:     /// # Examples\n   578:     ///\n   579:     /// ```\n   580:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   581:     ///\n   582:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);\n   583:     /// socket.set_scope_id(42);\n   584:     /// assert_eq!(socket.scope_id(), 42);\n   585:     /// ```\n   586:     #[inline]\n   587:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   588:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   589:     pub const fn set_scope_id(&mut self, new_scope_id: u32) {\n   590:         self.scope_id = new_scope_id;\n   591:     }\n   592: }\n   593: \n   594: #[stable(feature = \"ip_from_ip\", since = \"1.16.0\")]\n   595: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   596: impl const From<SocketAddrV4> for SocketAddr {\n   597:     /// Converts a [`SocketAddrV4`] into a [`SocketAddr::V4`].\n   598:     #[inline]\n   599:     fn from(sock4: SocketAddrV4) -> SocketAddr {\n   600:         SocketAddr::V4(sock4)\n   601:     }\n   602: }\n   603: \n   604: #[stable(feature = \"ip_from_ip\", since = \"1.16.0\")]\n   605: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]",
    "nanvix_source": "   579:     /// ```\n   580:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   581:     ///\n   582:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 78);\n   583:     /// socket.set_scope_id(42);\n   584:     /// assert_eq!(socket.scope_id(), 42);\n   585:     /// ```\n   586:     #[inline]\n   587:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   588:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   589:     pub const fn set_scope_id(&mut self, new_scope_id: u32) {\n   590:         self.scope_id = new_scope_id;\n   591:     }\n   592: }\n   593: \n   594: #[stable(feature = \"ip_from_ip\", since = \"1.16.0\")]\n   595: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   596: const impl From<SocketAddrV4> for SocketAddr {\n   597:     /// Converts a [`SocketAddrV4`] into a [`SocketAddr::V4`].\n   598:     #[inline]\n   599:     fn from(sock4: SocketAddrV4) -> SocketAddr {",
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
