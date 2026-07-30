For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::Ipv6Addr::from_bits",
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
      "name": "from_bits",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bits",
            {
              "primitive": "u128"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9949,
            "path": "Ipv6Addr"
          }
        }
      }
    },
    "verification_source": "  1426:     ///\n  1427:     /// ```\n  1428:     /// use std::net::Ipv6Addr;\n  1429:     ///\n  1430:     /// let addr = Ipv6Addr::from_bits(0x102030405060708090A0B0C0D0E0F00D_u128);\n  1431:     /// assert_eq!(\n  1432:     ///     Ipv6Addr::new(\n  1433:     ///         0x1020, 0x3040, 0x5060, 0x7080,\n  1434:     ///         0x90A0, 0xB0C0, 0xD0E0, 0xF00D,\n  1435:     ///     ),\n  1436:     ///     addr);\n  1437:     /// ```\n  1438:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1439:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1440:     #[must_use]\n  1441:     #[inline]\n  1442:     pub const fn from_bits(bits: u128) -> Ipv6Addr {\n  1443:         Ipv6Addr { octets: bits.to_be_bytes() }\n  1444:     }\n  1445: \n  1446:     /// An IPv6 address representing localhost: `::1`.\n  1447:     ///\n  1448:     /// This corresponds to constant `IN6ADDR_LOOPBACK_INIT` or `in6addr_loopback` in other\n  1449:     /// languages.\n  1450:     ///\n  1451:     /// # Examples\n  1452:     ///\n  1453:     /// ```\n  1454:     /// use std::net::Ipv6Addr;\n  1455:     ///\n  1456:     /// let addr = Ipv6Addr::LOCALHOST;\n  1457:     /// assert_eq!(addr, Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1));\n  1458:     /// ```",
    "nanvix_source": "  1432:     ///     Ipv6Addr::new(\n  1433:     ///         0x1020, 0x3040, 0x5060, 0x7080,\n  1434:     ///         0x90A0, 0xB0C0, 0xD0E0, 0xF00D,\n  1435:     ///     ),\n  1436:     ///     addr);\n  1437:     /// ```\n  1438:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1439:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1440:     #[must_use]\n  1441:     #[inline]\n  1442:     pub const fn from_bits(bits: u128) -> Ipv6Addr {\n  1443:         Ipv6Addr { octets: bits.to_be_bytes() }\n  1444:     }\n  1445: \n  1446:     /// An IPv6 address representing localhost: `::1`.\n  1447:     ///\n  1448:     /// This corresponds to constant `IN6ADDR_LOOPBACK_INIT` or `in6addr_loopback` in other\n  1449:     /// languages.\n  1450:     ///\n  1451:     /// # Examples\n  1452:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::from_octets",
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
      "name": "from_octets",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "octets",
            {
              "array": {
                "len": "16",
                "type": {
                  "primitive": "u8"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9949,
            "path": "Ipv6Addr"
          }
        }
      }
    },
    "verification_source": "  2093:     /// let addr = Ipv6Addr::from_octets([\n  2094:     ///     0x19u8, 0x18u8, 0x17u8, 0x16u8, 0x15u8, 0x14u8, 0x13u8, 0x12u8,\n  2095:     ///     0x11u8, 0x10u8, 0x0fu8, 0x0eu8, 0x0du8, 0x0cu8, 0x0bu8, 0x0au8,\n  2096:     /// ]);\n  2097:     /// assert_eq!(\n  2098:     ///     Ipv6Addr::new(\n  2099:     ///         0x1918, 0x1716, 0x1514, 0x1312,\n  2100:     ///         0x1110, 0x0f0e, 0x0d0c, 0x0b0a,\n  2101:     ///     ),\n  2102:     ///     addr\n  2103:     /// );\n  2104:     /// ```\n  2105:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n  2106:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n  2107:     #[must_use]\n  2108:     #[inline]\n  2109:     pub const fn from_octets(octets: [u8; 16]) -> Ipv6Addr {\n  2110:         Ipv6Addr { octets }\n  2111:     }\n  2112: \n  2113:     /// Returns the sixteen eight-bit integers the IPv6 address consists of\n  2114:     /// as a slice.\n  2115:     ///\n  2116:     /// # Examples\n  2117:     ///\n  2118:     /// ```\n  2119:     /// #![feature(ip_as_octets)]\n  2120:     ///\n  2121:     /// use std::net::Ipv6Addr;\n  2122:     ///\n  2123:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).as_octets(),\n  2124:     ///            &[255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])\n  2125:     /// ```",
    "nanvix_source": "  2099:     ///         0x1918, 0x1716, 0x1514, 0x1312,\n  2100:     ///         0x1110, 0x0f0e, 0x0d0c, 0x0b0a,\n  2101:     ///     ),\n  2102:     ///     addr\n  2103:     /// );\n  2104:     /// ```\n  2105:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n  2106:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n  2107:     #[must_use]\n  2108:     #[inline]\n  2109:     pub const fn from_octets(octets: [u8; 16]) -> Ipv6Addr {\n  2110:         Ipv6Addr { octets }\n  2111:     }\n  2112: \n  2113:     /// Returns the sixteen eight-bit integers the IPv6 address consists of\n  2114:     /// as a slice.\n  2115:     ///\n  2116:     /// # Examples\n  2117:     ///\n  2118:     /// ```\n  2119:     /// #![feature(ip_as_octets)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::from_segments",
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
      "name": "from_segments",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "segments",
            {
              "array": {
                "len": "8",
                "type": {
                  "primitive": "u16"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9949,
            "path": "Ipv6Addr"
          }
        }
      }
    },
    "verification_source": "  1519:     /// let addr = Ipv6Addr::from_segments([\n  1520:     ///     0x20du16, 0x20cu16, 0x20bu16, 0x20au16,\n  1521:     ///     0x209u16, 0x208u16, 0x207u16, 0x206u16,\n  1522:     /// ]);\n  1523:     /// assert_eq!(\n  1524:     ///     Ipv6Addr::new(\n  1525:     ///         0x20d, 0x20c, 0x20b, 0x20a,\n  1526:     ///         0x209, 0x208, 0x207, 0x206,\n  1527:     ///     ),\n  1528:     ///     addr\n  1529:     /// );\n  1530:     /// ```\n  1531:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n  1532:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n  1533:     #[must_use]\n  1534:     #[inline]\n  1535:     pub const fn from_segments(segments: [u16; 8]) -> Ipv6Addr {\n  1536:         let [a, b, c, d, e, f, g, h] = segments;\n  1537:         Ipv6Addr::new(a, b, c, d, e, f, g, h)\n  1538:     }\n  1539: \n  1540:     /// Returns [`true`] for the special 'unspecified' address (`::`).\n  1541:     ///\n  1542:     /// This property is defined in [IETF RFC 4291].\n  1543:     ///\n  1544:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1545:     ///\n  1546:     /// # Examples\n  1547:     ///\n  1548:     /// ```\n  1549:     /// use std::net::Ipv6Addr;\n  1550:     ///\n  1551:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_unspecified(), false);",
    "nanvix_source": "  1525:     ///         0x20d, 0x20c, 0x20b, 0x20a,\n  1526:     ///         0x209, 0x208, 0x207, 0x206,\n  1527:     ///     ),\n  1528:     ///     addr\n  1529:     /// );\n  1530:     /// ```\n  1531:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n  1532:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n  1533:     #[must_use]\n  1534:     #[inline]\n  1535:     pub const fn from_segments(segments: [u16; 8]) -> Ipv6Addr {\n  1536:         let [a, b, c, d, e, f, g, h] = segments;\n  1537:         Ipv6Addr::new(a, b, c, d, e, f, g, h)\n  1538:     }\n  1539: \n  1540:     /// Returns [`true`] for the special 'unspecified' address (`::`).\n  1541:     ///\n  1542:     /// This property is defined in [IETF RFC 4291].\n  1543:     ///\n  1544:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1545:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::is_loopback",
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
      "name": "is_loopback",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1566:     ///\n  1567:     /// [loopback address]: Ipv6Addr::LOCALHOST\n  1568:     /// [IETF RFC 4291 section 2.5.3]: https://tools.ietf.org/html/rfc4291#section-2.5.3\n  1569:     ///\n  1570:     /// # Examples\n  1571:     ///\n  1572:     /// ```\n  1573:     /// use std::net::Ipv6Addr;\n  1574:     ///\n  1575:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_loopback(), false);\n  1576:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0x1).is_loopback(), true);\n  1577:     /// ```\n  1578:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1579:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1580:     #[must_use]\n  1581:     #[inline]\n  1582:     pub const fn is_loopback(&self) -> bool {\n  1583:         u128::from_be_bytes(self.octets()) == u128::from_be_bytes(Ipv6Addr::LOCALHOST.octets())\n  1584:     }\n  1585: \n  1586:     /// Returns [`true`] if the address appears to be globally reachable\n  1587:     /// as specified by the [IANA IPv6 Special-Purpose Address Registry].\n  1588:     ///\n  1589:     /// Whether or not an address is practically reachable will depend on your\n  1590:     /// network configuration. Most IPv6 addresses are globally reachable, unless\n  1591:     /// they are specifically defined as *not* globally reachable.\n  1592:     ///\n  1593:     /// Non-exhaustive list of notable addresses that are not globally reachable:\n  1594:     /// - The [unspecified address] ([`is_unspecified`](Ipv6Addr::is_unspecified))\n  1595:     /// - The [loopback address] ([`is_loopback`](Ipv6Addr::is_loopback))\n  1596:     /// - IPv4-mapped addresses\n  1597:     /// - Addresses reserved for benchmarking ([`is_benchmarking`](Ipv6Addr::is_benchmarking))\n  1598:     /// - Addresses reserved for documentation ([`is_documentation`](Ipv6Addr::is_documentation))",
    "nanvix_source": "  1572:     /// ```\n  1573:     /// use std::net::Ipv6Addr;\n  1574:     ///\n  1575:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_loopback(), false);\n  1576:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0x1).is_loopback(), true);\n  1577:     /// ```\n  1578:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1579:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1580:     #[must_use]\n  1581:     #[inline]\n  1582:     pub const fn is_loopback(&self) -> bool {\n  1583:         u128::from_be_bytes(self.octets()) == u128::from_be_bytes(Ipv6Addr::LOCALHOST.octets())\n  1584:     }\n  1585: \n  1586:     /// Returns [`true`] if the address appears to be globally reachable\n  1587:     /// as specified by the [IANA IPv6 Special-Purpose Address Registry].\n  1588:     ///\n  1589:     /// Whether or not an address is practically reachable will depend on your\n  1590:     /// network configuration. Most IPv6 addresses are globally reachable, unless\n  1591:     /// they are specifically defined as *not* globally reachable.\n  1592:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::is_multicast",
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
      "name": "is_multicast",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1926:     /// This property is defined by [IETF RFC 4291].\n  1927:     ///\n  1928:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1929:     ///\n  1930:     /// # Examples\n  1931:     ///\n  1932:     /// ```\n  1933:     /// use std::net::Ipv6Addr;\n  1934:     ///\n  1935:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).is_multicast(), true);\n  1936:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_multicast(), false);\n  1937:     /// ```\n  1938:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1939:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1940:     #[must_use]\n  1941:     #[inline]\n  1942:     pub const fn is_multicast(&self) -> bool {\n  1943:         (self.segments()[0] & 0xff00) == 0xff00\n  1944:     }\n  1945: \n  1946:     /// Returns [`true`] if the address is an IPv4-mapped address (`::ffff:0:0/96`).\n  1947:     ///\n  1948:     /// IPv4-mapped addresses can be converted to their canonical IPv4 address with\n  1949:     /// [`to_ipv4_mapped`](Ipv6Addr::to_ipv4_mapped).\n  1950:     ///\n  1951:     /// # Examples\n  1952:     /// ```\n  1953:     /// #![feature(ip)]\n  1954:     ///\n  1955:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1956:     ///\n  1957:     /// let ipv4_mapped = Ipv4Addr::new(192, 0, 2, 255).to_ipv6_mapped();\n  1958:     /// assert_eq!(ipv4_mapped.is_ipv4_mapped(), true);",
    "nanvix_source": "  1932:     /// ```\n  1933:     /// use std::net::Ipv6Addr;\n  1934:     ///\n  1935:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).is_multicast(), true);\n  1936:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_multicast(), false);\n  1937:     /// ```\n  1938:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1939:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1940:     #[must_use]\n  1941:     #[inline]\n  1942:     pub const fn is_multicast(&self) -> bool {\n  1943:         (self.segments()[0] & 0xff00) == 0xff00\n  1944:     }\n  1945: \n  1946:     /// Returns [`true`] if the address is an IPv4-mapped address (`::ffff:0:0/96`).\n  1947:     ///\n  1948:     /// IPv4-mapped addresses can be converted to their canonical IPv4 address with\n  1949:     /// [`to_ipv4_mapped`](Ipv6Addr::to_ipv4_mapped).\n  1950:     ///\n  1951:     /// # Examples\n  1952:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::is_unicast_link_local",
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
      "name": "is_unicast_link_local",
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
            "id": 9949,
            "path": "Ipv6Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27837",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9949",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv6Addr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1768:     ///\n  1769:     /// // The loopback address (`::1`) does not actually have link-local scope.\n  1770:     /// assert_eq!(Ipv6Addr::LOCALHOST.is_unicast_link_local(), false);\n  1771:     ///\n  1772:     /// // Only addresses in `fe80::/10` have link-local scope.\n  1773:     /// assert_eq!(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0).is_unicast_link_local(), false);\n  1774:     /// assert_eq!(Ipv6Addr::new(0xfe80, 0, 0, 0, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1775:     ///\n  1776:     /// // Addresses outside the stricter `fe80::/64` also have link-local scope.\n  1777:     /// assert_eq!(Ipv6Addr::new(0xfe80, 0, 0, 1, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1778:     /// assert_eq!(Ipv6Addr::new(0xfe81, 0, 0, 0, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1779:     /// ```\n  1780:     #[must_use]\n  1781:     #[inline]\n  1782:     #[stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1783:     #[rustc_const_stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1784:     pub const fn is_unicast_link_local(&self) -> bool {\n  1785:         (self.segments()[0] & 0xffc0) == 0xfe80\n  1786:     }\n  1787: \n  1788:     /// Returns [`true`] if this is an address reserved for documentation\n  1789:     /// (`2001:db8::/32` and `3fff::/20`).\n  1790:     ///\n  1791:     /// This property is defined by [IETF RFC 3849] and [IETF RFC 9637].\n  1792:     ///\n  1793:     /// [IETF RFC 3849]: https://tools.ietf.org/html/rfc3849\n  1794:     /// [IETF RFC 9637]: https://tools.ietf.org/html/rfc9637\n  1795:     ///\n  1796:     /// # Examples\n  1797:     ///\n  1798:     /// ```\n  1799:     /// #![feature(ip)]\n  1800:     ///",
    "nanvix_source": "  1774:     /// assert_eq!(Ipv6Addr::new(0xfe80, 0, 0, 0, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1775:     ///\n  1776:     /// // Addresses outside the stricter `fe80::/64` also have link-local scope.\n  1777:     /// assert_eq!(Ipv6Addr::new(0xfe80, 0, 0, 1, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1778:     /// assert_eq!(Ipv6Addr::new(0xfe81, 0, 0, 0, 0, 0, 0, 0).is_unicast_link_local(), true);\n  1779:     /// ```\n  1780:     #[must_use]\n  1781:     #[inline]\n  1782:     #[stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1783:     #[rustc_const_stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1784:     pub const fn is_unicast_link_local(&self) -> bool {\n  1785:         (self.segments()[0] & 0xffc0) == 0xfe80\n  1786:     }\n  1787: \n  1788:     /// Returns [`true`] if this is an address reserved for documentation\n  1789:     /// (`2001:db8::/32` and `3fff::/20`).\n  1790:     ///\n  1791:     /// This property is defined by [IETF RFC 3849] and [IETF RFC 9637].\n  1792:     ///\n  1793:     /// [IETF RFC 3849]: https://tools.ietf.org/html/rfc3849\n  1794:     /// [IETF RFC 9637]: https://tools.ietf.org/html/rfc9637",
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
