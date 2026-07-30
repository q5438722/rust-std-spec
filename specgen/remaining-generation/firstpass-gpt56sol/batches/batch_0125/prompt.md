For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::Ipv4Addr::is_unspecified",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
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
    "verification_source": "   712:     /// W. Richard Stevens, p. 891; see also [ip7].\n   713:     ///\n   714:     /// [ip7]: https://man7.org/linux/man-pages/man7/ip.7.html\n   715:     ///\n   716:     /// # Examples\n   717:     ///\n   718:     /// ```\n   719:     /// use std::net::Ipv4Addr;\n   720:     ///\n   721:     /// assert_eq!(Ipv4Addr::new(0, 0, 0, 0).is_unspecified(), true);\n   722:     /// assert_eq!(Ipv4Addr::new(45, 22, 13, 197).is_unspecified(), false);\n   723:     /// ```\n   724:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n   725:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   726:     #[must_use]\n   727:     #[inline]\n   728:     pub const fn is_unspecified(&self) -> bool {\n   729:         u32::from_be_bytes(self.octets) == 0\n   730:     }\n   731: \n   732:     /// Returns [`true`] if this is a loopback address (`127.0.0.0/8`).\n   733:     ///\n   734:     /// This property is defined by [IETF RFC 1122].\n   735:     ///\n   736:     /// [IETF RFC 1122]: https://tools.ietf.org/html/rfc1122\n   737:     ///\n   738:     /// # Examples\n   739:     ///\n   740:     /// ```\n   741:     /// use std::net::Ipv4Addr;\n   742:     ///\n   743:     /// assert_eq!(Ipv4Addr::new(127, 0, 0, 1).is_loopback(), true);\n   744:     /// assert_eq!(Ipv4Addr::new(45, 22, 13, 197).is_loopback(), false);",
    "nanvix_source": "   718:     /// ```\n   719:     /// use std::net::Ipv4Addr;\n   720:     ///\n   721:     /// assert_eq!(Ipv4Addr::new(0, 0, 0, 0).is_unspecified(), true);\n   722:     /// assert_eq!(Ipv4Addr::new(45, 22, 13, 197).is_unspecified(), false);\n   723:     /// ```\n   724:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n   725:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   726:     #[must_use]\n   727:     #[inline]\n   728:     pub const fn is_unspecified(&self) -> bool {\n   729:         u32::from_be_bytes(self.octets) == 0\n   730:     }\n   731: \n   732:     /// Returns [`true`] if this is a loopback address (`127.0.0.0/8`).\n   733:     ///\n   734:     /// This property is defined by [IETF RFC 1122].\n   735:     ///\n   736:     /// [IETF RFC 1122]: https://tools.ietf.org/html/rfc1122\n   737:     ///\n   738:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::new",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "a",
            {
              "primitive": "u8"
            }
          ],
          [
            "b",
            {
              "primitive": "u8"
            }
          ],
          [
            "c",
            {
              "primitive": "u8"
            }
          ],
          [
            "d",
            {
              "primitive": "u8"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9946,
            "path": "Ipv4Addr"
          }
        }
      }
    },
    "verification_source": "   527: impl Ipv4Addr {\n   528:     /// Creates a new IPv4 address from four eight-bit octets.\n   529:     ///\n   530:     /// The result will represent the IP address `a`.`b`.`c`.`d`.\n   531:     ///\n   532:     /// # Examples\n   533:     ///\n   534:     /// ```\n   535:     /// use std::net::Ipv4Addr;\n   536:     ///\n   537:     /// let addr = Ipv4Addr::new(127, 0, 0, 1);\n   538:     /// ```\n   539:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n   540:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   541:     #[must_use]\n   542:     #[inline]\n   543:     pub const fn new(a: u8, b: u8, c: u8, d: u8) -> Ipv4Addr {\n   544:         Ipv4Addr { octets: [a, b, c, d] }\n   545:     }\n   546: \n   547:     /// The size of an IPv4 address in bits.\n   548:     ///\n   549:     /// # Examples\n   550:     ///\n   551:     /// ```\n   552:     /// use std::net::Ipv4Addr;\n   553:     ///\n   554:     /// assert_eq!(Ipv4Addr::BITS, 32);\n   555:     /// ```\n   556:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   557:     pub const BITS: u32 = 32;\n   558: \n   559:     /// Converts an IPv4 address into a `u32` representation using native byte order.",
    "nanvix_source": "   533:     ///\n   534:     /// ```\n   535:     /// use std::net::Ipv4Addr;\n   536:     ///\n   537:     /// let addr = Ipv4Addr::new(127, 0, 0, 1);\n   538:     /// ```\n   539:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n   540:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   541:     #[must_use]\n   542:     #[inline]\n   543:     pub const fn new(a: u8, b: u8, c: u8, d: u8) -> Ipv4Addr {\n   544:         Ipv4Addr { octets: [a, b, c, d] }\n   545:     }\n   546: \n   547:     /// The size of an IPv4 address in bits.\n   548:     ///\n   549:     /// # Examples\n   550:     ///\n   551:     /// ```\n   552:     /// use std::net::Ipv4Addr;\n   553:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::octets",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
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
            "len": "4",
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   652:     pub const BROADCAST: Self = Ipv4Addr::new(255, 255, 255, 255);\n   653: \n   654:     /// Returns the four eight-bit integers that make up this address.\n   655:     ///\n   656:     /// # Examples\n   657:     ///\n   658:     /// ```\n   659:     /// use std::net::Ipv4Addr;\n   660:     ///\n   661:     /// let addr = Ipv4Addr::new(127, 0, 0, 1);\n   662:     /// assert_eq!(addr.octets(), [127, 0, 0, 1]);\n   663:     /// ```\n   664:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   665:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   666:     #[must_use]\n   667:     #[inline]\n   668:     pub const fn octets(&self) -> [u8; 4] {\n   669:         self.octets\n   670:     }\n   671: \n   672:     /// Creates an `Ipv4Addr` from a four element byte array.\n   673:     ///\n   674:     /// # Examples\n   675:     ///\n   676:     /// ```\n   677:     /// use std::net::Ipv4Addr;\n   678:     ///\n   679:     /// let addr = Ipv4Addr::from_octets([13u8, 12u8, 11u8, 10u8]);\n   680:     /// assert_eq!(Ipv4Addr::new(13, 12, 11, 10), addr);\n   681:     /// ```\n   682:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n   683:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n   684:     #[must_use]",
    "nanvix_source": "   658:     /// ```\n   659:     /// use std::net::Ipv4Addr;\n   660:     ///\n   661:     /// let addr = Ipv4Addr::new(127, 0, 0, 1);\n   662:     /// assert_eq!(addr.octets(), [127, 0, 0, 1]);\n   663:     /// ```\n   664:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   665:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   666:     #[must_use]\n   667:     #[inline]\n   668:     pub const fn octets(&self) -> [u8; 4] {\n   669:         self.octets\n   670:     }\n   671: \n   672:     /// Creates an `Ipv4Addr` from a four element byte array.\n   673:     ///\n   674:     /// # Examples\n   675:     ///\n   676:     /// ```\n   677:     /// use std::net::Ipv4Addr;\n   678:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::to_bits",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   572:     /// let addr = Ipv4Addr::new(0x12, 0x34, 0x56, 0x78);\n   573:     /// assert_eq!(0x12345678, addr.to_bits());\n   574:     /// ```\n   575:     ///\n   576:     /// ```\n   577:     /// use std::net::Ipv4Addr;\n   578:     ///\n   579:     /// let addr = Ipv4Addr::new(0x12, 0x34, 0x56, 0x78);\n   580:     /// let addr_bits = addr.to_bits() & 0xffffff00;\n   581:     /// assert_eq!(Ipv4Addr::new(0x12, 0x34, 0x56, 0x00), Ipv4Addr::from_bits(addr_bits));\n   582:     ///\n   583:     /// ```\n   584:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   585:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   586:     #[must_use]\n   587:     #[inline]\n   588:     pub const fn to_bits(self) -> u32 {\n   589:         u32::from_be_bytes(self.octets)\n   590:     }\n   591: \n   592:     /// Converts a native byte order `u32` into an IPv4 address.\n   593:     ///\n   594:     /// See [`Ipv4Addr::to_bits`] for an explanation on endianness.\n   595:     ///\n   596:     /// # Examples\n   597:     ///\n   598:     /// ```\n   599:     /// use std::net::Ipv4Addr;\n   600:     ///\n   601:     /// let addr = Ipv4Addr::from_bits(0x12345678);\n   602:     /// assert_eq!(Ipv4Addr::new(0x12, 0x34, 0x56, 0x78), addr);\n   603:     /// ```\n   604:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]",
    "nanvix_source": "   578:     ///\n   579:     /// let addr = Ipv4Addr::new(0x12, 0x34, 0x56, 0x78);\n   580:     /// let addr_bits = addr.to_bits() & 0xffffff00;\n   581:     /// assert_eq!(Ipv4Addr::new(0x12, 0x34, 0x56, 0x00), Ipv4Addr::from_bits(addr_bits));\n   582:     ///\n   583:     /// ```\n   584:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   585:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   586:     #[must_use]\n   587:     #[inline]\n   588:     pub const fn to_bits(self) -> u32 {\n   589:         u32::from_be_bytes(self.octets)\n   590:     }\n   591: \n   592:     /// Converts a native byte order `u32` into an IPv4 address.\n   593:     ///\n   594:     /// See [`Ipv4Addr::to_bits`] for an explanation on endianness.\n   595:     ///\n   596:     /// # Examples\n   597:     ///\n   598:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::to_ipv6_compatible",
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
      "name": "to_ipv6_compatible",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
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
            "args": null,
            "id": 9949,
            "path": "Ipv6Addr"
          }
        }
      }
    },
    "verification_source": "  1073:     ///\n  1074:     /// # Examples\n  1075:     ///\n  1076:     /// ```\n  1077:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1078:     ///\n  1079:     /// assert_eq!(\n  1080:     ///     Ipv4Addr::new(192, 0, 2, 255).to_ipv6_compatible(),\n  1081:     ///     Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0xc000, 0x2ff)\n  1082:     /// );\n  1083:     /// ```\n  1084:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1085:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1086:     #[must_use = \"this returns the result of the operation, \\\n  1087:                   without modifying the original\"]\n  1088:     #[inline]\n  1089:     pub const fn to_ipv6_compatible(&self) -> Ipv6Addr {\n  1090:         let [a, b, c, d] = self.octets();\n  1091:         Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, b, c, d] }\n  1092:     }\n  1093: \n  1094:     /// Converts this address to an [IPv4-mapped] [`IPv6` address].\n  1095:     ///\n  1096:     /// `a.b.c.d` becomes `::ffff:a.b.c.d`\n  1097:     ///\n  1098:     /// [IPv4-mapped]: Ipv6Addr#ipv4-mapped-ipv6-addresses\n  1099:     /// [`IPv6` address]: Ipv6Addr\n  1100:     ///\n  1101:     /// # Examples\n  1102:     ///\n  1103:     /// ```\n  1104:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1105:     ///",
    "nanvix_source": "  1079:     /// assert_eq!(\n  1080:     ///     Ipv4Addr::new(192, 0, 2, 255).to_ipv6_compatible(),\n  1081:     ///     Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0xc000, 0x2ff)\n  1082:     /// );\n  1083:     /// ```\n  1084:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1085:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1086:     #[must_use = \"this returns the result of the operation, \\\n  1087:                   without modifying the original\"]\n  1088:     #[inline]\n  1089:     pub const fn to_ipv6_compatible(&self) -> Ipv6Addr {\n  1090:         let [a, b, c, d] = self.octets();\n  1091:         Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, b, c, d] }\n  1092:     }\n  1093: \n  1094:     /// Converts this address to an [IPv4-mapped] [`IPv6` address].\n  1095:     ///\n  1096:     /// `a.b.c.d` becomes `::ffff:a.b.c.d`\n  1097:     ///\n  1098:     /// [IPv4-mapped]: Ipv6Addr#ipv4-mapped-ipv6-addresses\n  1099:     /// [`IPv6` address]: Ipv6Addr",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::to_ipv6_mapped",
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
      "name": "to_ipv6_mapped",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27796",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9946",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "Ipv4Addr"
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
            "args": null,
            "id": 9949,
            "path": "Ipv6Addr"
          }
        }
      }
    },
    "verification_source": "  1098:     /// [IPv4-mapped]: Ipv6Addr#ipv4-mapped-ipv6-addresses\n  1099:     /// [`IPv6` address]: Ipv6Addr\n  1100:     ///\n  1101:     /// # Examples\n  1102:     ///\n  1103:     /// ```\n  1104:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1105:     ///\n  1106:     /// assert_eq!(Ipv4Addr::new(192, 0, 2, 255).to_ipv6_mapped(),\n  1107:     ///            Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc000, 0x2ff));\n  1108:     /// ```\n  1109:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1110:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1111:     #[must_use = \"this returns the result of the operation, \\\n  1112:                   without modifying the original\"]\n  1113:     #[inline]\n  1114:     pub const fn to_ipv6_mapped(&self) -> Ipv6Addr {\n  1115:         let [a, b, c, d] = self.octets();\n  1116:         Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xFF, 0xFF, a, b, c, d] }\n  1117:     }\n  1118: }\n  1119: \n  1120: #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n  1121: impl fmt::Display for IpAddr {\n  1122:     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1123:         match self {\n  1124:             IpAddr::V4(ip) => ip.fmt(fmt),\n  1125:             IpAddr::V6(ip) => ip.fmt(fmt),\n  1126:         }\n  1127:     }\n  1128: }\n  1129: \n  1130: #[stable(feature = \"ip_addr\", since = \"1.7.0\")]",
    "nanvix_source": "  1104:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1105:     ///\n  1106:     /// assert_eq!(Ipv4Addr::new(192, 0, 2, 255).to_ipv6_mapped(),\n  1107:     ///            Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc000, 0x2ff));\n  1108:     /// ```\n  1109:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1110:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1111:     #[must_use = \"this returns the result of the operation, \\\n  1112:                   without modifying the original\"]\n  1113:     #[inline]\n  1114:     pub const fn to_ipv6_mapped(&self) -> Ipv6Addr {\n  1115:         let [a, b, c, d] = self.octets();\n  1116:         Ipv6Addr { octets: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xFF, 0xFF, a, b, c, d] }\n  1117:     }\n  1118: }\n  1119: \n  1120: #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n  1121: impl fmt::Display for IpAddr {\n  1122:     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1123:         match self {\n  1124:             IpAddr::V4(ip) => ip.fmt(fmt),",
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
