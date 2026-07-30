For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::Ipv4Addr::is_broadcast",
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
      "name": "is_broadcast",
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
    "verification_source": "  1016:     /// A broadcast address has all octets set to `255` as defined in [IETF RFC 919].\n  1017:     ///\n  1018:     /// [IETF RFC 919]: https://tools.ietf.org/html/rfc919\n  1019:     ///\n  1020:     /// # Examples\n  1021:     ///\n  1022:     /// ```\n  1023:     /// use std::net::Ipv4Addr;\n  1024:     ///\n  1025:     /// assert_eq!(Ipv4Addr::new(255, 255, 255, 255).is_broadcast(), true);\n  1026:     /// assert_eq!(Ipv4Addr::new(236, 168, 10, 65).is_broadcast(), false);\n  1027:     /// ```\n  1028:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1029:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1030:     #[must_use]\n  1031:     #[inline]\n  1032:     pub const fn is_broadcast(&self) -> bool {\n  1033:         u32::from_be_bytes(self.octets()) == u32::from_be_bytes(Self::BROADCAST.octets())\n  1034:     }\n  1035: \n  1036:     /// Returns [`true`] if this address is in a range designated for documentation.\n  1037:     ///\n  1038:     /// This is defined in [IETF RFC 5737]:\n  1039:     ///\n  1040:     /// - `192.0.2.0/24` (TEST-NET-1)\n  1041:     /// - `198.51.100.0/24` (TEST-NET-2)\n  1042:     /// - `203.0.113.0/24` (TEST-NET-3)\n  1043:     ///\n  1044:     /// [IETF RFC 5737]: https://tools.ietf.org/html/rfc5737\n  1045:     ///\n  1046:     /// # Examples\n  1047:     ///\n  1048:     /// ```",
    "nanvix_source": "  1022:     /// ```\n  1023:     /// use std::net::Ipv4Addr;\n  1024:     ///\n  1025:     /// assert_eq!(Ipv4Addr::new(255, 255, 255, 255).is_broadcast(), true);\n  1026:     /// assert_eq!(Ipv4Addr::new(236, 168, 10, 65).is_broadcast(), false);\n  1027:     /// ```\n  1028:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1029:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1030:     #[must_use]\n  1031:     #[inline]\n  1032:     pub const fn is_broadcast(&self) -> bool {\n  1033:         u32::from_be_bytes(self.octets()) == u32::from_be_bytes(Self::BROADCAST.octets())\n  1034:     }\n  1035: \n  1036:     /// Returns [`true`] if this address is in a range designated for documentation.\n  1037:     ///\n  1038:     /// This is defined in [IETF RFC 5737]:\n  1039:     ///\n  1040:     /// - `192.0.2.0/24` (TEST-NET-1)\n  1041:     /// - `198.51.100.0/24` (TEST-NET-2)\n  1042:     /// - `203.0.113.0/24` (TEST-NET-3)",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::is_documentation",
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
      "name": "is_documentation",
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
    "verification_source": "  1044:     /// [IETF RFC 5737]: https://tools.ietf.org/html/rfc5737\n  1045:     ///\n  1046:     /// # Examples\n  1047:     ///\n  1048:     /// ```\n  1049:     /// use std::net::Ipv4Addr;\n  1050:     ///\n  1051:     /// assert_eq!(Ipv4Addr::new(192, 0, 2, 255).is_documentation(), true);\n  1052:     /// assert_eq!(Ipv4Addr::new(198, 51, 100, 65).is_documentation(), true);\n  1053:     /// assert_eq!(Ipv4Addr::new(203, 0, 113, 6).is_documentation(), true);\n  1054:     /// assert_eq!(Ipv4Addr::new(193, 34, 17, 19).is_documentation(), false);\n  1055:     /// ```\n  1056:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1057:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1058:     #[must_use]\n  1059:     #[inline]\n  1060:     pub const fn is_documentation(&self) -> bool {\n  1061:         matches!(self.octets(), [192, 0, 2, _] | [198, 51, 100, _] | [203, 0, 113, _])\n  1062:     }\n  1063: \n  1064:     /// Converts this address to an [IPv4-compatible] [`IPv6` address].\n  1065:     ///\n  1066:     /// `a.b.c.d` becomes `::a.b.c.d`\n  1067:     ///\n  1068:     /// Note that IPv4-compatible addresses have been officially deprecated.\n  1069:     /// If you don't explicitly need an IPv4-compatible address for legacy reasons, consider using `to_ipv6_mapped` instead.\n  1070:     ///\n  1071:     /// [IPv4-compatible]: Ipv6Addr#ipv4-compatible-ipv6-addresses\n  1072:     /// [`IPv6` address]: Ipv6Addr\n  1073:     ///\n  1074:     /// # Examples\n  1075:     ///\n  1076:     /// ```",
    "nanvix_source": "  1050:     ///\n  1051:     /// assert_eq!(Ipv4Addr::new(192, 0, 2, 255).is_documentation(), true);\n  1052:     /// assert_eq!(Ipv4Addr::new(198, 51, 100, 65).is_documentation(), true);\n  1053:     /// assert_eq!(Ipv4Addr::new(203, 0, 113, 6).is_documentation(), true);\n  1054:     /// assert_eq!(Ipv4Addr::new(193, 34, 17, 19).is_documentation(), false);\n  1055:     /// ```\n  1056:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1057:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1058:     #[must_use]\n  1059:     #[inline]\n  1060:     pub const fn is_documentation(&self) -> bool {\n  1061:         matches!(self.octets(), [192, 0, 2, _] | [198, 51, 100, _] | [203, 0, 113, _])\n  1062:     }\n  1063: \n  1064:     /// Converts this address to an [IPv4-compatible] [`IPv6` address].\n  1065:     ///\n  1066:     /// `a.b.c.d` becomes `::a.b.c.d`\n  1067:     ///\n  1068:     /// Note that IPv4-compatible addresses have been officially deprecated.\n  1069:     /// If you don't explicitly need an IPv4-compatible address for legacy reasons, consider using `to_ipv6_mapped` instead.\n  1070:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::is_link_local",
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
      "name": "is_link_local",
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
    "verification_source": "   793:     ///\n   794:     /// [IETF RFC 3927]: https://tools.ietf.org/html/rfc3927\n   795:     ///\n   796:     /// # Examples\n   797:     ///\n   798:     /// ```\n   799:     /// use std::net::Ipv4Addr;\n   800:     ///\n   801:     /// assert_eq!(Ipv4Addr::new(169, 254, 0, 0).is_link_local(), true);\n   802:     /// assert_eq!(Ipv4Addr::new(169, 254, 10, 65).is_link_local(), true);\n   803:     /// assert_eq!(Ipv4Addr::new(16, 89, 10, 65).is_link_local(), false);\n   804:     /// ```\n   805:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   806:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   807:     #[must_use]\n   808:     #[inline]\n   809:     pub const fn is_link_local(&self) -> bool {\n   810:         matches!(self.octets(), [169, 254, ..])\n   811:     }\n   812: \n   813:     /// Returns [`true`] if the address appears to be globally reachable\n   814:     /// as specified by the [IANA IPv4 Special-Purpose Address Registry].\n   815:     ///\n   816:     /// Whether or not an address is practically reachable will depend on your\n   817:     /// network configuration. Most IPv4 addresses are globally reachable, unless\n   818:     /// they are specifically defined as *not* globally reachable.\n   819:     ///\n   820:     /// Non-exhaustive list of notable addresses that are not globally reachable:\n   821:     ///\n   822:     /// - The [unspecified address] ([`is_unspecified`](Ipv4Addr::is_unspecified))\n   823:     /// - Addresses reserved for private use ([`is_private`](Ipv4Addr::is_private))\n   824:     /// - Addresses in the shared address space ([`is_shared`](Ipv4Addr::is_shared))\n   825:     /// - Loopback addresses ([`is_loopback`](Ipv4Addr::is_loopback))",
    "nanvix_source": "   799:     /// use std::net::Ipv4Addr;\n   800:     ///\n   801:     /// assert_eq!(Ipv4Addr::new(169, 254, 0, 0).is_link_local(), true);\n   802:     /// assert_eq!(Ipv4Addr::new(169, 254, 10, 65).is_link_local(), true);\n   803:     /// assert_eq!(Ipv4Addr::new(16, 89, 10, 65).is_link_local(), false);\n   804:     /// ```\n   805:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   806:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   807:     #[must_use]\n   808:     #[inline]\n   809:     pub const fn is_link_local(&self) -> bool {\n   810:         matches!(self.octets(), [169, 254, ..])\n   811:     }\n   812: \n   813:     /// Returns [`true`] if the address appears to be globally reachable\n   814:     /// as specified by the [IANA IPv4 Special-Purpose Address Registry].\n   815:     ///\n   816:     /// Whether or not an address is practically reachable will depend on your\n   817:     /// network configuration. Most IPv4 addresses are globally reachable, unless\n   818:     /// they are specifically defined as *not* globally reachable.\n   819:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::is_loopback",
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
    "verification_source": "   734:     /// This property is defined by [IETF RFC 1122].\n   735:     ///\n   736:     /// [IETF RFC 1122]: https://tools.ietf.org/html/rfc1122\n   737:     ///\n   738:     /// # Examples\n   739:     ///\n   740:     /// ```\n   741:     /// use std::net::Ipv4Addr;\n   742:     ///\n   743:     /// assert_eq!(Ipv4Addr::new(127, 0, 0, 1).is_loopback(), true);\n   744:     /// assert_eq!(Ipv4Addr::new(45, 22, 13, 197).is_loopback(), false);\n   745:     /// ```\n   746:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   747:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   748:     #[must_use]\n   749:     #[inline]\n   750:     pub const fn is_loopback(&self) -> bool {\n   751:         self.octets()[0] == 127\n   752:     }\n   753: \n   754:     /// Returns [`true`] if this is a private address.\n   755:     ///\n   756:     /// The private address ranges are defined in [IETF RFC 1918] and include:\n   757:     ///\n   758:     ///  - `10.0.0.0/8`\n   759:     ///  - `172.16.0.0/12`\n   760:     ///  - `192.168.0.0/16`\n   761:     ///\n   762:     /// [IETF RFC 1918]: https://tools.ietf.org/html/rfc1918\n   763:     ///\n   764:     /// # Examples\n   765:     ///\n   766:     /// ```",
    "nanvix_source": "   740:     /// ```\n   741:     /// use std::net::Ipv4Addr;\n   742:     ///\n   743:     /// assert_eq!(Ipv4Addr::new(127, 0, 0, 1).is_loopback(), true);\n   744:     /// assert_eq!(Ipv4Addr::new(45, 22, 13, 197).is_loopback(), false);\n   745:     /// ```\n   746:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   747:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   748:     #[must_use]\n   749:     #[inline]\n   750:     pub const fn is_loopback(&self) -> bool {\n   751:         self.octets()[0] == 127\n   752:     }\n   753: \n   754:     /// Returns [`true`] if this is a private address.\n   755:     ///\n   756:     /// The private address ranges are defined in [IETF RFC 1918] and include:\n   757:     ///\n   758:     ///  - `10.0.0.0/8`\n   759:     ///  - `172.16.0.0/12`\n   760:     ///  - `192.168.0.0/16`",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::is_multicast",
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
    "verification_source": "   994:     ///\n   995:     /// [IETF RFC 5771]: https://tools.ietf.org/html/rfc5771\n   996:     ///\n   997:     /// # Examples\n   998:     ///\n   999:     /// ```\n  1000:     /// use std::net::Ipv4Addr;\n  1001:     ///\n  1002:     /// assert_eq!(Ipv4Addr::new(224, 254, 0, 0).is_multicast(), true);\n  1003:     /// assert_eq!(Ipv4Addr::new(236, 168, 10, 65).is_multicast(), true);\n  1004:     /// assert_eq!(Ipv4Addr::new(172, 16, 10, 65).is_multicast(), false);\n  1005:     /// ```\n  1006:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1007:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1008:     #[must_use]\n  1009:     #[inline]\n  1010:     pub const fn is_multicast(&self) -> bool {\n  1011:         self.octets()[0] >= 224 && self.octets()[0] <= 239\n  1012:     }\n  1013: \n  1014:     /// Returns [`true`] if this is a broadcast address (`255.255.255.255`).\n  1015:     ///\n  1016:     /// A broadcast address has all octets set to `255` as defined in [IETF RFC 919].\n  1017:     ///\n  1018:     /// [IETF RFC 919]: https://tools.ietf.org/html/rfc919\n  1019:     ///\n  1020:     /// # Examples\n  1021:     ///\n  1022:     /// ```\n  1023:     /// use std::net::Ipv4Addr;\n  1024:     ///\n  1025:     /// assert_eq!(Ipv4Addr::new(255, 255, 255, 255).is_broadcast(), true);\n  1026:     /// assert_eq!(Ipv4Addr::new(236, 168, 10, 65).is_broadcast(), false);",
    "nanvix_source": "  1000:     /// use std::net::Ipv4Addr;\n  1001:     ///\n  1002:     /// assert_eq!(Ipv4Addr::new(224, 254, 0, 0).is_multicast(), true);\n  1003:     /// assert_eq!(Ipv4Addr::new(236, 168, 10, 65).is_multicast(), true);\n  1004:     /// assert_eq!(Ipv4Addr::new(172, 16, 10, 65).is_multicast(), false);\n  1005:     /// ```\n  1006:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  1007:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n  1008:     #[must_use]\n  1009:     #[inline]\n  1010:     pub const fn is_multicast(&self) -> bool {\n  1011:         self.octets()[0] >= 224 && self.octets()[0] <= 239\n  1012:     }\n  1013: \n  1014:     /// Returns [`true`] if this is a broadcast address (`255.255.255.255`).\n  1015:     ///\n  1016:     /// A broadcast address has all octets set to `255` as defined in [IETF RFC 919].\n  1017:     ///\n  1018:     /// [IETF RFC 919]: https://tools.ietf.org/html/rfc919\n  1019:     ///\n  1020:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::is_private",
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
      "name": "is_private",
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
    "verification_source": "   765:     ///\n   766:     /// ```\n   767:     /// use std::net::Ipv4Addr;\n   768:     ///\n   769:     /// assert_eq!(Ipv4Addr::new(10, 0, 0, 1).is_private(), true);\n   770:     /// assert_eq!(Ipv4Addr::new(10, 10, 10, 10).is_private(), true);\n   771:     /// assert_eq!(Ipv4Addr::new(172, 16, 10, 10).is_private(), true);\n   772:     /// assert_eq!(Ipv4Addr::new(172, 29, 45, 14).is_private(), true);\n   773:     /// assert_eq!(Ipv4Addr::new(172, 32, 0, 2).is_private(), false);\n   774:     /// assert_eq!(Ipv4Addr::new(192, 168, 0, 2).is_private(), true);\n   775:     /// assert_eq!(Ipv4Addr::new(192, 169, 0, 2).is_private(), false);\n   776:     /// ```\n   777:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   778:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   779:     #[must_use]\n   780:     #[inline]\n   781:     pub const fn is_private(&self) -> bool {\n   782:         match self.octets() {\n   783:             [10, ..] => true,\n   784:             [172, b, ..] if b >= 16 && b <= 31 => true,\n   785:             [192, 168, ..] => true,\n   786:             _ => false,\n   787:         }\n   788:     }\n   789: \n   790:     /// Returns [`true`] if the address is link-local (`169.254.0.0/16`).\n   791:     ///\n   792:     /// This property is defined by [IETF RFC 3927].\n   793:     ///\n   794:     /// [IETF RFC 3927]: https://tools.ietf.org/html/rfc3927\n   795:     ///\n   796:     /// # Examples\n   797:     ///",
    "nanvix_source": "   771:     /// assert_eq!(Ipv4Addr::new(172, 16, 10, 10).is_private(), true);\n   772:     /// assert_eq!(Ipv4Addr::new(172, 29, 45, 14).is_private(), true);\n   773:     /// assert_eq!(Ipv4Addr::new(172, 32, 0, 2).is_private(), false);\n   774:     /// assert_eq!(Ipv4Addr::new(192, 168, 0, 2).is_private(), true);\n   775:     /// assert_eq!(Ipv4Addr::new(192, 169, 0, 2).is_private(), false);\n   776:     /// ```\n   777:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   778:     #[stable(since = \"1.7.0\", feature = \"ip_17\")]\n   779:     #[must_use]\n   780:     #[inline]\n   781:     pub const fn is_private(&self) -> bool {\n   782:         match self.octets() {\n   783:             [10, ..] => true,\n   784:             [172, b, ..] if b >= 16 && b <= 31 => true,\n   785:             [192, 168, ..] => true,\n   786:             _ => false,\n   787:         }\n   788:     }\n   789: \n   790:     /// Returns [`true`] if the address is link-local (`169.254.0.0/16`).\n   791:     ///",
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
