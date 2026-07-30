For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::Ipv6Addr::to_canonical",
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
      "name": "to_canonical",
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
          "resolved_path": {
            "args": null,
            "id": 9943,
            "path": "IpAddr"
          }
        }
      }
    },
    "verification_source": "  2047:     /// Converts this address to an `IpAddr::V4` if it is an IPv4-mapped address,\n  2048:     /// otherwise returns self wrapped in an `IpAddr::V6`.\n  2049:     ///\n  2050:     /// # Examples\n  2051:     ///\n  2052:     /// ```\n  2053:     /// use std::net::Ipv6Addr;\n  2054:     ///\n  2055:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1).is_loopback(), false);\n  2056:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1).to_canonical().is_loopback(), true);\n  2057:     /// ```\n  2058:     #[inline]\n  2059:     #[must_use = \"this returns the result of the operation, \\\n  2060:                   without modifying the original\"]\n  2061:     #[stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n  2062:     #[rustc_const_stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n  2063:     pub const fn to_canonical(&self) -> IpAddr {\n  2064:         if let Some(mapped) = self.to_ipv4_mapped() {\n  2065:             return IpAddr::V4(mapped);\n  2066:         }\n  2067:         IpAddr::V6(*self)\n  2068:     }\n  2069: \n  2070:     /// Returns the sixteen eight-bit integers the IPv6 address consists of.\n  2071:     ///\n  2072:     /// ```\n  2073:     /// use std::net::Ipv6Addr;\n  2074:     ///\n  2075:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).octets(),\n  2076:     ///            [0xff, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);\n  2077:     /// ```\n  2078:     #[rustc_const_stable(feature = \"const_ip_32\", since = \"1.32.0\")]\n  2079:     #[stable(feature = \"ipv6_to_octets\", since = \"1.12.0\")]",
    "nanvix_source": "  2053:     /// use std::net::Ipv6Addr;\n  2054:     ///\n  2055:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1).is_loopback(), false);\n  2056:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1).to_canonical().is_loopback(), true);\n  2057:     /// ```\n  2058:     #[inline]\n  2059:     #[must_use = \"this returns the result of the operation, \\\n  2060:                   without modifying the original\"]\n  2061:     #[stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n  2062:     #[rustc_const_stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n  2063:     pub const fn to_canonical(&self) -> IpAddr {\n  2064:         if let Some(mapped) = self.to_ipv4_mapped() {\n  2065:             return IpAddr::V4(mapped);\n  2066:         }\n  2067:         IpAddr::V6(*self)\n  2068:     }\n  2069: \n  2070:     /// Returns the sixteen eight-bit integers the IPv6 address consists of.\n  2071:     ///\n  2072:     /// ```\n  2073:     /// use std::net::Ipv6Addr;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::to_ipv4",
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
      "name": "to_ipv4",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 9946,
                        "path": "Ipv4Addr"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2021:     /// # Examples\n  2022:     ///\n  2023:     /// ```\n  2024:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  2025:     ///\n  2026:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).to_ipv4(), None);\n  2027:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).to_ipv4(),\n  2028:     ///            Some(Ipv4Addr::new(192, 10, 2, 255)));\n  2029:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1).to_ipv4(),\n  2030:     ///            Some(Ipv4Addr::new(0, 0, 0, 1)));\n  2031:     /// ```\n  2032:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  2033:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2034:     #[must_use = \"this returns the result of the operation, \\\n  2035:                   without modifying the original\"]\n  2036:     #[inline]\n  2037:     pub const fn to_ipv4(&self) -> Option<Ipv4Addr> {\n  2038:         if let [0, 0, 0, 0, 0, 0 | 0xffff, ab, cd] = self.segments() {\n  2039:             let [a, b] = ab.to_be_bytes();\n  2040:             let [c, d] = cd.to_be_bytes();\n  2041:             Some(Ipv4Addr::new(a, b, c, d))\n  2042:         } else {\n  2043:             None\n  2044:         }\n  2045:     }\n  2046: \n  2047:     /// Converts this address to an `IpAddr::V4` if it is an IPv4-mapped address,\n  2048:     /// otherwise returns self wrapped in an `IpAddr::V6`.\n  2049:     ///\n  2050:     /// # Examples\n  2051:     ///\n  2052:     /// ```\n  2053:     /// use std::net::Ipv6Addr;",
    "nanvix_source": "  2027:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).to_ipv4(),\n  2028:     ///            Some(Ipv4Addr::new(192, 10, 2, 255)));\n  2029:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1).to_ipv4(),\n  2030:     ///            Some(Ipv4Addr::new(0, 0, 0, 1)));\n  2031:     /// ```\n  2032:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n  2033:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2034:     #[must_use = \"this returns the result of the operation, \\\n  2035:                   without modifying the original\"]\n  2036:     #[inline]\n  2037:     pub const fn to_ipv4(&self) -> Option<Ipv4Addr> {\n  2038:         if let [0, 0, 0, 0, 0, 0 | 0xffff, ab, cd] = self.segments() {\n  2039:             let [a, b] = ab.to_be_bytes();\n  2040:             let [c, d] = cd.to_be_bytes();\n  2041:             Some(Ipv4Addr::new(a, b, c, d))\n  2042:         } else {\n  2043:             None\n  2044:         }\n  2045:     }\n  2046: \n  2047:     /// Converts this address to an `IpAddr::V4` if it is an IPv4-mapped address,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv6Addr::to_ipv4_mapped",
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
      "name": "to_ipv4_mapped",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 9946,
                        "path": "Ipv4Addr"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1979:     ///\n  1980:     /// # Examples\n  1981:     ///\n  1982:     /// ```\n  1983:     /// use std::net::{Ipv4Addr, Ipv6Addr};\n  1984:     ///\n  1985:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).to_ipv4_mapped(), None);\n  1986:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).to_ipv4_mapped(),\n  1987:     ///            Some(Ipv4Addr::new(192, 10, 2, 255)));\n  1988:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1).to_ipv4_mapped(), None);\n  1989:     /// ```\n  1990:     #[inline]\n  1991:     #[must_use = \"this returns the result of the operation, \\\n  1992:                   without modifying the original\"]\n  1993:     #[stable(feature = \"ipv6_to_ipv4_mapped\", since = \"1.63.0\")]\n  1994:     #[rustc_const_stable(feature = \"const_ipv6_to_ipv4_mapped\", since = \"1.75.0\")]\n  1995:     pub const fn to_ipv4_mapped(&self) -> Option<Ipv4Addr> {\n  1996:         match self.octets() {\n  1997:             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, a, b, c, d] => {\n  1998:                 Some(Ipv4Addr::new(a, b, c, d))\n  1999:             }\n  2000:             _ => None,\n  2001:         }\n  2002:     }\n  2003: \n  2004:     /// Converts this address to an [`IPv4` address] if it is either\n  2005:     /// an [IPv4-compatible] address as defined in [IETF RFC 4291 section 2.5.5.1],\n  2006:     /// or an [IPv4-mapped] address as defined in [IETF RFC 4291 section 2.5.5.2],\n  2007:     /// otherwise returns [`None`].\n  2008:     ///\n  2009:     /// Note that this will return an [`IPv4` address] for the IPv6 loopback address `::1`. Use\n  2010:     /// [`Ipv6Addr::to_ipv4_mapped`] to avoid this.\n  2011:     ///",
    "nanvix_source": "  1985:     /// assert_eq!(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0).to_ipv4_mapped(), None);\n  1986:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0xc00a, 0x2ff).to_ipv4_mapped(),\n  1987:     ///            Some(Ipv4Addr::new(192, 10, 2, 255)));\n  1988:     /// assert_eq!(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 1).to_ipv4_mapped(), None);\n  1989:     /// ```\n  1990:     #[inline]\n  1991:     #[must_use = \"this returns the result of the operation, \\\n  1992:                   without modifying the original\"]\n  1993:     #[stable(feature = \"ipv6_to_ipv4_mapped\", since = \"1.63.0\")]\n  1994:     #[rustc_const_stable(feature = \"const_ipv6_to_ipv4_mapped\", since = \"1.75.0\")]\n  1995:     pub const fn to_ipv4_mapped(&self) -> Option<Ipv4Addr> {\n  1996:         match self.octets() {\n  1997:             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, a, b, c, d] => {\n  1998:                 Some(Ipv4Addr::new(a, b, c, d))\n  1999:             }\n  2000:             _ => None,\n  2001:         }\n  2002:     }\n  2003: \n  2004:     /// Converts this address to an [`IPv4` address] if it is either\n  2005:     /// an [IPv4-compatible] address as defined in [IETF RFC 4291 section 2.5.5.1],",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::ip",
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
      "name": "ip",
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
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
            "id": 9943,
            "path": "IpAddr"
          }
        }
      }
    },
    "verification_source": "   177:     }\n   178: \n   179:     /// Returns the IP address associated with this socket address.\n   180:     ///\n   181:     /// # Examples\n   182:     ///\n   183:     /// ```\n   184:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   185:     ///\n   186:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   187:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   188:     /// ```\n   189:     #[must_use]\n   190:     #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n   191:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   192:     #[inline]\n   193:     pub const fn ip(&self) -> IpAddr {\n   194:         match *self {\n   195:             SocketAddr::V4(ref a) => IpAddr::V4(*a.ip()),\n   196:             SocketAddr::V6(ref a) => IpAddr::V6(*a.ip()),\n   197:         }\n   198:     }\n   199: \n   200:     /// Changes the IP address associated with this socket address.\n   201:     ///\n   202:     /// # Examples\n   203:     ///\n   204:     /// ```\n   205:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   206:     ///\n   207:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   208:     /// socket.set_ip(IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));\n   209:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));",
    "nanvix_source": "   183:     /// ```\n   184:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   185:     ///\n   186:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   187:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   188:     /// ```\n   189:     #[must_use]\n   190:     #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n   191:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   192:     #[inline]\n   193:     pub const fn ip(&self) -> IpAddr {\n   194:         match *self {\n   195:             SocketAddr::V4(ref a) => IpAddr::V4(*a.ip()),\n   196:             SocketAddr::V6(ref a) => IpAddr::V6(*a.ip()),\n   197:         }\n   198:     }\n   199: \n   200:     /// Changes the IP address associated with this socket address.\n   201:     ///\n   202:     /// # Examples\n   203:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::is_ipv4",
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
      "name": "is_ipv4",
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
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
    "verification_source": "   268:     /// [IP address]: IpAddr\n   269:     /// [`IPv4` address]: IpAddr::V4\n   270:     ///\n   271:     /// # Examples\n   272:     ///\n   273:     /// ```\n   274:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   275:     ///\n   276:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   277:     /// assert_eq!(socket.is_ipv4(), true);\n   278:     /// assert_eq!(socket.is_ipv6(), false);\n   279:     /// ```\n   280:     #[must_use]\n   281:     #[stable(feature = \"sockaddr_checker\", since = \"1.16.0\")]\n   282:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   283:     #[inline]\n   284:     pub const fn is_ipv4(&self) -> bool {\n   285:         matches!(*self, SocketAddr::V4(_))\n   286:     }\n   287: \n   288:     /// Returns [`true`] if the [IP address] in this `SocketAddr` is an\n   289:     /// [`IPv6` address], and [`false`] otherwise.\n   290:     ///\n   291:     /// [IP address]: IpAddr\n   292:     /// [`IPv6` address]: IpAddr::V6\n   293:     ///\n   294:     /// # Examples\n   295:     ///\n   296:     /// ```\n   297:     /// use std::net::{IpAddr, Ipv6Addr, SocketAddr};\n   298:     ///\n   299:     /// let socket = SocketAddr::new(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 65535, 0, 1)), 8080);\n   300:     /// assert_eq!(socket.is_ipv4(), false);",
    "nanvix_source": "   274:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   275:     ///\n   276:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   277:     /// assert_eq!(socket.is_ipv4(), true);\n   278:     /// assert_eq!(socket.is_ipv6(), false);\n   279:     /// ```\n   280:     #[must_use]\n   281:     #[stable(feature = \"sockaddr_checker\", since = \"1.16.0\")]\n   282:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   283:     #[inline]\n   284:     pub const fn is_ipv4(&self) -> bool {\n   285:         matches!(*self, SocketAddr::V4(_))\n   286:     }\n   287: \n   288:     /// Returns [`true`] if the [IP address] in this `SocketAddr` is an\n   289:     /// [`IPv6` address], and [`false`] otherwise.\n   290:     ///\n   291:     /// [IP address]: IpAddr\n   292:     /// [`IPv6` address]: IpAddr::V6\n   293:     ///\n   294:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::is_ipv6",
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
      "name": "is_ipv6",
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
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
    "verification_source": "   291:     /// [IP address]: IpAddr\n   292:     /// [`IPv6` address]: IpAddr::V6\n   293:     ///\n   294:     /// # Examples\n   295:     ///\n   296:     /// ```\n   297:     /// use std::net::{IpAddr, Ipv6Addr, SocketAddr};\n   298:     ///\n   299:     /// let socket = SocketAddr::new(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 65535, 0, 1)), 8080);\n   300:     /// assert_eq!(socket.is_ipv4(), false);\n   301:     /// assert_eq!(socket.is_ipv6(), true);\n   302:     /// ```\n   303:     #[must_use]\n   304:     #[stable(feature = \"sockaddr_checker\", since = \"1.16.0\")]\n   305:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   306:     #[inline]\n   307:     pub const fn is_ipv6(&self) -> bool {\n   308:         matches!(*self, SocketAddr::V6(_))\n   309:     }\n   310: }\n   311: \n   312: impl SocketAddrV4 {\n   313:     /// Creates a new socket address from an [`IPv4` address] and a port number.\n   314:     ///\n   315:     /// [`IPv4` address]: Ipv4Addr\n   316:     ///\n   317:     /// # Examples\n   318:     ///\n   319:     /// ```\n   320:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   321:     ///\n   322:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   323:     /// ```",
    "nanvix_source": "   297:     /// use std::net::{IpAddr, Ipv6Addr, SocketAddr};\n   298:     ///\n   299:     /// let socket = SocketAddr::new(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 65535, 0, 1)), 8080);\n   300:     /// assert_eq!(socket.is_ipv4(), false);\n   301:     /// assert_eq!(socket.is_ipv6(), true);\n   302:     /// ```\n   303:     #[must_use]\n   304:     #[stable(feature = \"sockaddr_checker\", since = \"1.16.0\")]\n   305:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   306:     #[inline]\n   307:     pub const fn is_ipv6(&self) -> bool {\n   308:         matches!(*self, SocketAddr::V6(_))\n   309:     }\n   310: }\n   311: \n   312: impl SocketAddrV4 {\n   313:     /// Creates a new socket address from an [`IPv4` address] and a port number.\n   314:     ///\n   315:     /// [`IPv4` address]: Ipv4Addr\n   316:     ///\n   317:     /// # Examples",
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
