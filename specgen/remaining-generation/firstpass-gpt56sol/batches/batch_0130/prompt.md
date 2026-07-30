For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::SocketAddrV4::port",
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
            "id": 9961,
            "path": "SocketAddrV4"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27946",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9961",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV4"
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
    "verification_source": "   366:     }\n   367: \n   368:     /// Returns the port number associated with this socket address.\n   369:     ///\n   370:     /// # Examples\n   371:     ///\n   372:     /// ```\n   373:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   374:     ///\n   375:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   376:     /// assert_eq!(socket.port(), 8080);\n   377:     /// ```\n   378:     #[must_use]\n   379:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   380:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   381:     #[inline]\n   382:     pub const fn port(&self) -> u16 {\n   383:         self.port\n   384:     }\n   385: \n   386:     /// Changes the port number associated with this socket address.\n   387:     ///\n   388:     /// # Examples\n   389:     ///\n   390:     /// ```\n   391:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   392:     ///\n   393:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   394:     /// socket.set_port(4242);\n   395:     /// assert_eq!(socket.port(), 4242);\n   396:     /// ```\n   397:     #[inline]\n   398:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]",
    "nanvix_source": "   372:     /// ```\n   373:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   374:     ///\n   375:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   376:     /// assert_eq!(socket.port(), 8080);\n   377:     /// ```\n   378:     #[must_use]\n   379:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   380:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   381:     #[inline]\n   382:     pub const fn port(&self) -> u16 {\n   383:         self.port\n   384:     }\n   385: \n   386:     /// Changes the port number associated with this socket address.\n   387:     ///\n   388:     /// # Examples\n   389:     ///\n   390:     /// ```\n   391:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   392:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV4::set_ip",
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
            "id": 9961,
            "path": "SocketAddrV4"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27946",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9961",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV4"
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
                "id": 9946,
                "path": "Ipv4Addr"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   348:     }\n   349: \n   350:     /// Changes the IP address associated with this socket address.\n   351:     ///\n   352:     /// # Examples\n   353:     ///\n   354:     /// ```\n   355:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   356:     ///\n   357:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   358:     /// socket.set_ip(Ipv4Addr::new(192, 168, 0, 1));\n   359:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(192, 168, 0, 1));\n   360:     /// ```\n   361:     #[inline]\n   362:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   363:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   364:     pub const fn set_ip(&mut self, new_ip: Ipv4Addr) {\n   365:         self.ip = new_ip;\n   366:     }\n   367: \n   368:     /// Returns the port number associated with this socket address.\n   369:     ///\n   370:     /// # Examples\n   371:     ///\n   372:     /// ```\n   373:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   374:     ///\n   375:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   376:     /// assert_eq!(socket.port(), 8080);\n   377:     /// ```\n   378:     #[must_use]\n   379:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   380:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]",
    "nanvix_source": "   354:     /// ```\n   355:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   356:     ///\n   357:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   358:     /// socket.set_ip(Ipv4Addr::new(192, 168, 0, 1));\n   359:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(192, 168, 0, 1));\n   360:     /// ```\n   361:     #[inline]\n   362:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   363:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   364:     pub const fn set_ip(&mut self, new_ip: Ipv4Addr) {\n   365:         self.ip = new_ip;\n   366:     }\n   367: \n   368:     /// Returns the port number associated with this socket address.\n   369:     ///\n   370:     /// # Examples\n   371:     ///\n   372:     /// ```\n   373:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   374:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV4::set_port",
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
            "id": 9961,
            "path": "SocketAddrV4"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27946",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9961",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV4"
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
    "verification_source": "   384:     }\n   385: \n   386:     /// Changes the port number associated with this socket address.\n   387:     ///\n   388:     /// # Examples\n   389:     ///\n   390:     /// ```\n   391:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   392:     ///\n   393:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   394:     /// socket.set_port(4242);\n   395:     /// assert_eq!(socket.port(), 4242);\n   396:     /// ```\n   397:     #[inline]\n   398:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   399:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   400:     pub const fn set_port(&mut self, new_port: u16) {\n   401:         self.port = new_port;\n   402:     }\n   403: }\n   404: \n   405: impl SocketAddrV6 {\n   406:     /// Creates a new socket address from an [`IPv6` address], a 16-bit port number,\n   407:     /// and the `flowinfo` and `scope_id` fields.\n   408:     ///\n   409:     /// For more information on the meaning and layout of the `flowinfo` and `scope_id`\n   410:     /// parameters, see [IETF RFC 2553, Section 3.3].\n   411:     ///\n   412:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   413:     /// [`IPv6` address]: Ipv6Addr\n   414:     ///\n   415:     /// # Examples\n   416:     ///",
    "nanvix_source": "   390:     /// ```\n   391:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   392:     ///\n   393:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   394:     /// socket.set_port(4242);\n   395:     /// assert_eq!(socket.port(), 4242);\n   396:     /// ```\n   397:     #[inline]\n   398:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   399:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   400:     pub const fn set_port(&mut self, new_port: u16) {\n   401:         self.port = new_port;\n   402:     }\n   403: }\n   404: \n   405: impl SocketAddrV6 {\n   406:     /// Creates a new socket address from an [`IPv6` address], a 16-bit port number,\n   407:     /// and the `flowinfo` and `scope_id` fields.\n   408:     ///\n   409:     /// For more information on the meaning and layout of the `flowinfo` and `scope_id`\n   410:     /// parameters, see [IETF RFC 2553, Section 3.3].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::flowinfo",
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
      "name": "flowinfo",
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
    "verification_source": "   510:     /// [IETF RFC 2460]: https://tools.ietf.org/html/rfc2460\n   511:     /// [Section 6]: https://tools.ietf.org/html/rfc2460#section-6\n   512:     /// [Section 7]: https://tools.ietf.org/html/rfc2460#section-7\n   513:     ///\n   514:     /// # Examples\n   515:     ///\n   516:     /// ```\n   517:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   518:     ///\n   519:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 10, 0);\n   520:     /// assert_eq!(socket.flowinfo(), 10);\n   521:     /// ```\n   522:     #[must_use]\n   523:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   524:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   525:     #[inline]\n   526:     pub const fn flowinfo(&self) -> u32 {\n   527:         self.flowinfo\n   528:     }\n   529: \n   530:     /// Changes the flow information associated with this socket address.\n   531:     ///\n   532:     /// See [`SocketAddrV6::flowinfo`]'s documentation for more details.\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   538:     ///\n   539:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 10, 0);\n   540:     /// socket.set_flowinfo(56);\n   541:     /// assert_eq!(socket.flowinfo(), 56);\n   542:     /// ```",
    "nanvix_source": "   516:     /// ```\n   517:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   518:     ///\n   519:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 10, 0);\n   520:     /// assert_eq!(socket.flowinfo(), 10);\n   521:     /// ```\n   522:     #[must_use]\n   523:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   524:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   525:     #[inline]\n   526:     pub const fn flowinfo(&self) -> u32 {\n   527:         self.flowinfo\n   528:     }\n   529: \n   530:     /// Changes the flow information associated with this socket address.\n   531:     ///\n   532:     /// See [`SocketAddrV6::flowinfo`]'s documentation for more details.\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::ip",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "ip",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 9949,
                "path": "Ipv6Addr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   428:     }\n   429: \n   430:     /// Returns the IP address associated with this socket address.\n   431:     ///\n   432:     /// # Examples\n   433:     ///\n   434:     /// ```\n   435:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   436:     ///\n   437:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   438:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1));\n   439:     /// ```\n   440:     #[must_use]\n   441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   442:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   443:     #[inline]\n   444:     pub const fn ip(&self) -> &Ipv6Addr {\n   445:         &self.ip\n   446:     }\n   447: \n   448:     /// Changes the IP address associated with this socket address.\n   449:     ///\n   450:     /// # Examples\n   451:     ///\n   452:     /// ```\n   453:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   454:     ///\n   455:     /// let mut socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   456:     /// socket.set_ip(Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   457:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(76, 45, 0, 0, 0, 0, 0, 0));\n   458:     /// ```\n   459:     #[inline]\n   460:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]",
    "nanvix_source": "   434:     /// ```\n   435:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   436:     ///\n   437:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   438:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1));\n   439:     /// ```\n   440:     #[must_use]\n   441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   442:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   443:     #[inline]\n   444:     pub const fn ip(&self) -> &Ipv6Addr {\n   445:         &self.ip\n   446:     }\n   447: \n   448:     /// Changes the IP address associated with this socket address.\n   449:     ///\n   450:     /// # Examples\n   451:     ///\n   452:     /// ```\n   453:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   454:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV6::new",
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
      "name": "new",
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
            "ip",
            {
              "resolved_path": {
                "args": null,
                "id": 9949,
                "path": "Ipv6Addr"
              }
            }
          ],
          [
            "port",
            {
              "primitive": "u16"
            }
          ],
          [
            "flowinfo",
            {
              "primitive": "u32"
            }
          ],
          [
            "scope_id",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9964,
            "path": "SocketAddrV6"
          }
        }
      }
    },
    "verification_source": "   410:     /// parameters, see [IETF RFC 2553, Section 3.3].\n   411:     ///\n   412:     /// [IETF RFC 2553, Section 3.3]: https://tools.ietf.org/html/rfc2553#section-3.3\n   413:     /// [`IPv6` address]: Ipv6Addr\n   414:     ///\n   415:     /// # Examples\n   416:     ///\n   417:     /// ```\n   418:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   419:     ///\n   420:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   421:     /// ```\n   422:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   423:     #[must_use]\n   424:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   425:     #[inline]\n   426:     pub const fn new(ip: Ipv6Addr, port: u16, flowinfo: u32, scope_id: u32) -> SocketAddrV6 {\n   427:         SocketAddrV6 { ip, port, flowinfo, scope_id }\n   428:     }\n   429: \n   430:     /// Returns the IP address associated with this socket address.\n   431:     ///\n   432:     /// # Examples\n   433:     ///\n   434:     /// ```\n   435:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   436:     ///\n   437:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   438:     /// assert_eq!(socket.ip(), &Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1));\n   439:     /// ```\n   440:     #[must_use]\n   441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   442:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]",
    "nanvix_source": "   416:     ///\n   417:     /// ```\n   418:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   419:     ///\n   420:     /// let socket = SocketAddrV6::new(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1), 8080, 0, 0);\n   421:     /// ```\n   422:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   423:     #[must_use]\n   424:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   425:     #[inline]\n   426:     pub const fn new(ip: Ipv6Addr, port: u16, flowinfo: u32, scope_id: u32) -> SocketAddrV6 {\n   427:         SocketAddrV6 { ip, port, flowinfo, scope_id }\n   428:     }\n   429: \n   430:     /// Returns the IP address associated with this socket address.\n   431:     ///\n   432:     /// # Examples\n   433:     ///\n   434:     /// ```\n   435:     /// use std::net::{SocketAddrV6, Ipv6Addr};\n   436:     ///",
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
