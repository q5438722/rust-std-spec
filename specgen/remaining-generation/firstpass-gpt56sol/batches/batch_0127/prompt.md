For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::Ipv6Addr::is_unique_local",
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
      "name": "is_unique_local",
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
    "verification_source": "  1690:     /// This property is defined in [IETF RFC 4193].\n  1691:     ///\n  1692:     /// [IETF RFC 4193]: https://tools.ietf.org/html/rfc4193\n  1693:     ///\n  1694:     /// # Examples\n  1695:     ///\n  1696:     /// ```\n  1697:     /// use std::net::Ipv6Addr;\n  1698:     ///\n  1699:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_unique_local(), false);\n  1700:     /// assert_eq!(Ipv6Addr::new(0xfc02, 0, 0, 0, 0, 0, 0, 0).is_unique_local(), true);\n  1701:     /// ```\n  1702:     #[must_use]\n  1703:     #[inline]\n  1704:     #[stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1705:     #[rustc_const_stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1706:     pub const fn is_unique_local(&self) -> bool {\n  1707:         (self.segments()[0] & 0xfe00) == 0xfc00\n  1708:     }\n  1709: \n  1710:     /// Returns [`true`] if this is a unicast address, as defined by [IETF RFC 4291].\n  1711:     /// Any address that is not a [multicast address] (`ff00::/8`) is unicast.\n  1712:     ///\n  1713:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1714:     /// [multicast address]: Ipv6Addr::is_multicast\n  1715:     ///\n  1716:     /// # Examples\n  1717:     ///\n  1718:     /// ```\n  1719:     /// #![feature(ip)]\n  1720:     ///\n  1721:     /// use std::net::Ipv6Addr;\n  1722:     ///",
    "nanvix_source": "  1696:     /// ```\n  1697:     /// use std::net::Ipv6Addr;\n  1698:     ///\n  1699:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_unique_local(), false);\n  1700:     /// assert_eq!(Ipv6Addr::new(0xfc02, 0, 0, 0, 0, 0, 0, 0).is_unique_local(), true);\n  1701:     /// ```\n  1702:     #[must_use]\n  1703:     #[inline]\n  1704:     #[stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1705:     #[rustc_const_stable(feature = \"ipv6_is_unique_local\", since = \"1.84.0\")]\n  1706:     pub const fn is_unique_local(&self) -> bool {\n  1707:         (self.segments()[0] & 0xfe00) == 0xfc00\n  1708:     }\n  1709: \n  1710:     /// Returns [`true`] if this is a unicast address, as defined by [IETF RFC 4291].\n  1711:     /// Any address that is not a [multicast address] (`ff00::/8`) is unicast.\n  1712:     ///\n  1713:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1714:     /// [multicast address]: Ipv6Addr::is_multicast\n  1715:     ///\n  1716:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::is_unspecified",
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
      "name": "is_unspecified",
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
    "verification_source": "  1542:     /// This property is defined in [IETF RFC 4291].\n  1543:     ///\n  1544:     /// [IETF RFC 4291]: https://tools.ietf.org/html/rfc4291\n  1545:     ///\n  1546:     /// # Examples\n  1547:     ///\n  1548:     /// ```\n  1549:     /// use std::net::Ipv6Addr;\n  1550:     ///\n  1551:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_unspecified(), false);\n  1552:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0).is_unspecified(), true);\n  1553:     /// ```\n  1554:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1555:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1556:     #[must_use]\n  1557:     #[inline]\n  1558:     pub const fn is_unspecified(&self) -> bool {\n  1559:         u128::from_be_bytes(self.octets()) == u128::from_be_bytes(Ipv6Addr::UNSPECIFIED.octets())\n  1560:     }\n  1561: \n  1562:     /// Returns [`true`] if this is the [loopback address] (`::1`),\n  1563:     /// as defined in [IETF RFC 4291 section 2.5.3].\n  1564:     ///\n  1565:     /// Contrary to IPv4, in IPv6 there is only one loopback address.\n  1566:     ///\n  1567:     /// [loopback address]: Ipv6Addr::LOCALHOST\n  1568:     /// [IETF RFC 4291 section 2.5.3]: https://tools.ietf.org/html/rfc4291#section-2.5.3\n  1569:     ///\n  1570:     /// # Examples\n  1571:     ///\n  1572:     /// ```\n  1573:     /// use std::net::Ipv6Addr;\n  1574:     ///",
    "nanvix_source": "  1548:     /// ```\n  1549:     /// use std::net::Ipv6Addr;\n  1550:     ///\n  1551:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).is_unspecified(), false);\n  1552:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0).is_unspecified(), true);\n  1553:     /// ```\n  1554:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1555:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1556:     #[must_use]\n  1557:     #[inline]\n  1558:     pub const fn is_unspecified(&self) -> bool {\n  1559:         u128::from_be_bytes(self.octets()) == u128::from_be_bytes(Ipv6Addr::UNSPECIFIED.octets())\n  1560:     }\n  1561: \n  1562:     /// Returns [`true`] if this is the [loopback address] (`::1`),\n  1563:     /// as defined in [IETF RFC 4291 section 2.5.3].\n  1564:     ///\n  1565:     /// Contrary to IPv4, in IPv6 there is only one loopback address.\n  1566:     ///\n  1567:     /// [loopback address]: Ipv6Addr::LOCALHOST\n  1568:     /// [IETF RFC 4291 section 2.5.3]: https://tools.ietf.org/html/rfc4291#section-2.5.3",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::new",
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
            "a",
            {
              "primitive": "u16"
            }
          ],
          [
            "b",
            {
              "primitive": "u16"
            }
          ],
          [
            "c",
            {
              "primitive": "u16"
            }
          ],
          [
            "d",
            {
              "primitive": "u16"
            }
          ],
          [
            "e",
            {
              "primitive": "u16"
            }
          ],
          [
            "f",
            {
              "primitive": "u16"
            }
          ],
          [
            "g",
            {
              "primitive": "u16"
            }
          ],
          [
            "h",
            {
              "primitive": "u16"
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
    "verification_source": "  1331: impl Ipv6Addr {\n  1332:     /// Creates a new IPv6 address from eight 16-bit segments.\n  1333:     ///\n  1334:     /// The result will represent the IP address `a:b:c:d:e:f:g:h`.\n  1335:     ///\n  1336:     /// # Examples\n  1337:     ///\n  1338:     /// ```\n  1339:     /// use std::net::Ipv6Addr;\n  1340:     ///\n  1341:     /// let addr = Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff);\n  1342:     /// ```\n  1343:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n  1344:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1345:     #[must_use]\n  1346:     #[inline]\n  1347:     pub const fn new(a: u16, b: u16, c: u16, d: u16, e: u16, f: u16, g: u16, h: u16) -> Ipv6Addr {\n  1348:         let addr16 = [\n  1349:             a.to_be(),\n  1350:             b.to_be(),\n  1351:             c.to_be(),\n  1352:             d.to_be(),\n  1353:             e.to_be(),\n  1354:             f.to_be(),\n  1355:             g.to_be(),\n  1356:             h.to_be(),\n  1357:         ];\n  1358:         Ipv6Addr {\n  1359:             // All elements in `addr16` are big endian.\n  1360:             // SAFETY: `[u16; 8]` is always safe to transmute to `[u8; 16]`.\n  1361:             octets: unsafe { transmute::<_, [u8; 16]>(addr16) },\n  1362:         }\n  1363:     }",
    "nanvix_source": "  1337:     ///\n  1338:     /// ```\n  1339:     /// use std::net::Ipv6Addr;\n  1340:     ///\n  1341:     /// let addr = Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff);\n  1342:     /// ```\n  1343:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n  1344:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1345:     #[must_use]\n  1346:     #[inline]\n  1347:     pub const fn new(a: u16, b: u16, c: u16, d: u16, e: u16, f: u16, g: u16, h: u16) -> Ipv6Addr {\n  1348:         let addr16 = [\n  1349:             a.to_be(),\n  1350:             b.to_be(),\n  1351:             c.to_be(),\n  1352:             d.to_be(),\n  1353:             e.to_be(),\n  1354:             f.to_be(),\n  1355:             g.to_be(),\n  1356:             h.to_be(),\n  1357:         ];",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::octets",
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
      "name": "octets",
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
          "array": {
            "len": "16",
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "  2066:         }\n  2067:         IpAddr::V6(*self)\n  2068:     }\n  2069: \n  2070:     /// Returns the sixteen eight-bit integers the IPv6 address consists of.\n  2071:     ///\n  2072:     /// ```\n  2073:     /// use std::net::Ipv6Addr;\n  2074:     ///\n  2075:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).octets(),\n  2076:     ///            [0xff, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);\n  2077:     /// ```\n  2078:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n  2079:     #[stable(feature = \"ipv6_to_octets\", since = \"1.12.0\")]\n  2080:     #[must_use]\n  2081:     #[inline]\n  2082:     pub const fn octets(&self) -> [u8; 16] {\n  2083:         self.octets\n  2084:     }\n  2085: \n  2086:     /// Creates an `Ipv6Addr` from a sixteen element byte array.\n  2087:     ///\n  2088:     /// # Examples\n  2089:     ///\n  2090:     /// ```\n  2091:     /// use std::net::Ipv6Addr;\n  2092:     ///\n  2093:     /// let addr = Ipv6Addr::from_octets([\n  2094:     ///     0x19u8, 0x18u8, 0x17u8, 0x16u8, 0x15u8, 0x14u8, 0x13u8, 0x12u8,\n  2095:     ///     0x11u8, 0x10u8, 0x0fu8, 0x0eu8, 0x0du8, 0x0cu8, 0x0bu8, 0x0au8,\n  2096:     /// ]);\n  2097:     /// assert_eq!(\n  2098:     ///     Ipv6Addr::new(",
    "nanvix_source": "  2072:     /// ```\n  2073:     /// use std::net::Ipv6Addr;\n  2074:     ///\n  2075:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).octets(),\n  2076:     ///            [0xff, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);\n  2077:     /// ```\n  2078:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n  2079:     #[stable(feature = \"ipv6_to_octets\", since = \"1.12.0\")]\n  2080:     #[must_use]\n  2081:     #[inline]\n  2082:     pub const fn octets(&self) -> [u8; 16] {\n  2083:         self.octets\n  2084:     }\n  2085: \n  2086:     /// Creates an `Ipv6Addr` from a sixteen element byte array.\n  2087:     ///\n  2088:     /// # Examples\n  2089:     ///\n  2090:     /// ```\n  2091:     /// use std::net::Ipv6Addr;\n  2092:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::segments",
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
      "name": "segments",
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
          "array": {
            "len": "8",
            "type": {
              "primitive": "u16"
            }
          }
        }
      }
    },
    "verification_source": "  1479:     pub const UNSPECIFIED: Self = Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0);\n  1480: \n  1481:     /// Returns the eight 16-bit segments that make up this address.\n  1482:     ///\n  1483:     /// # Examples\n  1484:     ///\n  1485:     /// ```\n  1486:     /// use std::net::Ipv6Addr;\n  1487:     ///\n  1488:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).segments(),\n  1489:     ///            [0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff]);\n  1490:     /// ```\n  1491:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1492:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1493:     #[must_use]\n  1494:     #[inline]\n  1495:     pub const fn segments(&self) -> [u16; 8] {\n  1496:         // All elements in `self.octets` must be big endian.\n  1497:         // SAFETY: `[u8; 16]` is always safe to transmute to `[u16; 8]`.\n  1498:         let [a, b, c, d, e, f, g, h] = unsafe { transmute::<_, [u16; 8]>(self.octets) };\n  1499:         // We want native endian u16\n  1500:         [\n  1501:             u16::from_be(a),\n  1502:             u16::from_be(b),\n  1503:             u16::from_be(c),\n  1504:             u16::from_be(d),\n  1505:             u16::from_be(e),\n  1506:             u16::from_be(f),\n  1507:             u16::from_be(g),\n  1508:             u16::from_be(h),\n  1509:         ]\n  1510:     }\n  1511: ",
    "nanvix_source": "  1485:     /// ```\n  1486:     /// use std::net::Ipv6Addr;\n  1487:     ///\n  1488:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).segments(),\n  1489:     ///            [0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff]);\n  1490:     /// ```\n  1491:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1492:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1493:     #[must_use]\n  1494:     #[inline]\n  1495:     pub const fn segments(&self) -> [u16; 8] {\n  1496:         // All elements in `self.octets` must be big endian.\n  1497:         // SAFETY: `[u8; 16]` is always safe to transmute to `[u16; 8]`.\n  1498:         let [a, b, c, d, e, f, g, h] = unsafe { transmute::<_, [u16; 8]>(self.octets) };\n  1499:         // We want native endian u16\n  1500:         [\n  1501:             u16::from_be(a),\n  1502:             u16::from_be(b),\n  1503:             u16::from_be(c),\n  1504:             u16::from_be(d),\n  1505:             u16::from_be(e),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::to_bits",
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
      "name": "to_bits",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "u128"
        }
      }
    },
    "verification_source": "  1401:     ///     0x1020, 0x3040, 0x5060, 0x7080,\n  1402:     ///     0x90A0, 0xB0C0, 0xD0E0, 0xF00D,\n  1403:     /// );\n  1404:     /// let addr_bits = addr.to_bits() & 0xffffffffffffffffffffffffffff0000_u128;\n  1405:     /// assert_eq!(\n  1406:     ///     Ipv6Addr::new(\n  1407:     ///         0x1020, 0x3040, 0x5060, 0x7080,\n  1408:     ///         0x90A0, 0xB0C0, 0xD0E0, 0x0000,\n  1409:     ///     ),\n  1410:     ///     Ipv6Addr::from_bits(addr_bits));\n  1411:     ///\n  1412:     /// ```\n  1413:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1414:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1415:     #[must_use]\n  1416:     #[inline]\n  1417:     pub const fn to_bits(self) -> u128 {\n  1418:         u128::from_be_bytes(self.octets)\n  1419:     }\n  1420: \n  1421:     /// Converts a native byte order `u128` into an IPv6 address.\n  1422:     ///\n  1423:     /// See [`Ipv6Addr::to_bits`] for an explanation on endianness.\n  1424:     ///\n  1425:     /// # Examples\n  1426:     ///\n  1427:     /// ```\n  1428:     /// use std::net::Ipv6Addr;\n  1429:     ///\n  1430:     /// let addr = Ipv6Addr::from_bits(0x102030405060708090A0B0C0D0E0F00D_u128);\n  1431:     /// assert_eq!(\n  1432:     ///     Ipv6Addr::new(\n  1433:     ///         0x1020, 0x3040, 0x5060, 0x7080,",
    "nanvix_source": "  1407:     ///         0x1020, 0x3040, 0x5060, 0x7080,\n  1408:     ///         0x90A0, 0xB0C0, 0xD0E0, 0x0000,\n  1409:     ///     ),\n  1410:     ///     Ipv6Addr::from_bits(addr_bits));\n  1411:     ///\n  1412:     /// ```\n  1413:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1414:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n  1415:     #[must_use]\n  1416:     #[inline]\n  1417:     pub const fn to_bits(self) -> u128 {\n  1418:         u128::from_be_bytes(self.octets)\n  1419:     }\n  1420: \n  1421:     /// Converts a native byte order `u128` into an IPv6 address.\n  1422:     ///\n  1423:     /// See [`Ipv6Addr::to_bits`] for an explanation on endianness.\n  1424:     ///\n  1425:     /// # Examples\n  1426:     ///\n  1427:     /// ```",
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
