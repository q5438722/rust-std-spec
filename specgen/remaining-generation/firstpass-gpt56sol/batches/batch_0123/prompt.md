For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::IpAddr::is_loopback",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
    "verification_source": "   309:     ///\n   310:     /// See the documentation for [`Ipv4Addr::is_loopback()`] and\n   311:     /// [`Ipv6Addr::is_loopback()`] for more details.\n   312:     ///\n   313:     /// # Examples\n   314:     ///\n   315:     /// ```\n   316:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   317:     ///\n   318:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)).is_loopback(), true);\n   319:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0x1)).is_loopback(), true);\n   320:     /// ```\n   321:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   322:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   323:     #[must_use]\n   324:     #[inline]\n   325:     pub const fn is_loopback(&self) -> bool {\n   326:         match self {\n   327:             IpAddr::V4(ip) => ip.is_loopback(),\n   328:             IpAddr::V6(ip) => ip.is_loopback(),\n   329:         }\n   330:     }\n   331: \n   332:     /// Returns [`true`] if the address appears to be globally routable.\n   333:     ///\n   334:     /// See the documentation for [`Ipv4Addr::is_global()`] and\n   335:     /// [`Ipv6Addr::is_global()`] for more details.\n   336:     ///\n   337:     /// # Examples\n   338:     ///\n   339:     /// ```\n   340:     /// #![feature(ip)]\n   341:     ///",
    "nanvix_source": "   315:     /// ```\n   316:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   317:     ///\n   318:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)).is_loopback(), true);\n   319:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0x1)).is_loopback(), true);\n   320:     /// ```\n   321:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   322:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   323:     #[must_use]\n   324:     #[inline]\n   325:     pub const fn is_loopback(&self) -> bool {\n   326:         match self {\n   327:             IpAddr::V4(ip) => ip.is_loopback(),\n   328:             IpAddr::V6(ip) => ip.is_loopback(),\n   329:         }\n   330:     }\n   331: \n   332:     /// Returns [`true`] if the address appears to be globally routable.\n   333:     ///\n   334:     /// See the documentation for [`Ipv4Addr::is_global()`] and\n   335:     /// [`Ipv6Addr::is_global()`] for more details.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::IpAddr::is_multicast",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
    "verification_source": "   358:     ///\n   359:     /// See the documentation for [`Ipv4Addr::is_multicast()`] and\n   360:     /// [`Ipv6Addr::is_multicast()`] for more details.\n   361:     ///\n   362:     /// # Examples\n   363:     ///\n   364:     /// ```\n   365:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   366:     ///\n   367:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(224, 254, 0, 0)).is_multicast(), true);\n   368:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0)).is_multicast(), true);\n   369:     /// ```\n   370:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   371:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   372:     #[must_use]\n   373:     #[inline]\n   374:     pub const fn is_multicast(&self) -> bool {\n   375:         match self {\n   376:             IpAddr::V4(ip) => ip.is_multicast(),\n   377:             IpAddr::V6(ip) => ip.is_multicast(),\n   378:         }\n   379:     }\n   380: \n   381:     /// Returns [`true`] if this address is in a range designated for documentation.\n   382:     ///\n   383:     /// See the documentation for [`Ipv4Addr::is_documentation()`] and\n   384:     /// [`Ipv6Addr::is_documentation()`] for more details.\n   385:     ///\n   386:     /// # Examples\n   387:     ///\n   388:     /// ```\n   389:     /// #![feature(ip)]\n   390:     ///",
    "nanvix_source": "   364:     /// ```\n   365:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   366:     ///\n   367:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(224, 254, 0, 0)).is_multicast(), true);\n   368:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0xff00, 0, 0, 0, 0, 0, 0, 0)).is_multicast(), true);\n   369:     /// ```\n   370:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   371:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   372:     #[must_use]\n   373:     #[inline]\n   374:     pub const fn is_multicast(&self) -> bool {\n   375:         match self {\n   376:             IpAddr::V4(ip) => ip.is_multicast(),\n   377:             IpAddr::V6(ip) => ip.is_multicast(),\n   378:         }\n   379:     }\n   380: \n   381:     /// Returns [`true`] if this address is in a range designated for documentation.\n   382:     ///\n   383:     /// See the documentation for [`Ipv4Addr::is_documentation()`] and\n   384:     /// [`Ipv6Addr::is_documentation()`] for more details.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::IpAddr::is_unspecified",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
    "verification_source": "   285:     ///\n   286:     /// See the documentation for [`Ipv4Addr::is_unspecified()`] and\n   287:     /// [`Ipv6Addr::is_unspecified()`] for more details.\n   288:     ///\n   289:     /// # Examples\n   290:     ///\n   291:     /// ```\n   292:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   293:     ///\n   294:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)).is_unspecified(), true);\n   295:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0)).is_unspecified(), true);\n   296:     /// ```\n   297:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   298:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   299:     #[must_use]\n   300:     #[inline]\n   301:     pub const fn is_unspecified(&self) -> bool {\n   302:         match self {\n   303:             IpAddr::V4(ip) => ip.is_unspecified(),\n   304:             IpAddr::V6(ip) => ip.is_unspecified(),\n   305:         }\n   306:     }\n   307: \n   308:     /// Returns [`true`] if this is a loopback address.\n   309:     ///\n   310:     /// See the documentation for [`Ipv4Addr::is_loopback()`] and\n   311:     /// [`Ipv6Addr::is_loopback()`] for more details.\n   312:     ///\n   313:     /// # Examples\n   314:     ///\n   315:     /// ```\n   316:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   317:     ///",
    "nanvix_source": "   291:     /// ```\n   292:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   293:     ///\n   294:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)).is_unspecified(), true);\n   295:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0, 0, 0)).is_unspecified(), true);\n   296:     /// ```\n   297:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   298:     #[stable(feature = \"ip_shared\", since = \"1.12.0\")]\n   299:     #[must_use]\n   300:     #[inline]\n   301:     pub const fn is_unspecified(&self) -> bool {\n   302:         match self {\n   303:             IpAddr::V4(ip) => ip.is_unspecified(),\n   304:             IpAddr::V6(ip) => ip.is_unspecified(),\n   305:         }\n   306:     }\n   307: \n   308:     /// Returns [`true`] if this is a loopback address.\n   309:     ///\n   310:     /// See the documentation for [`Ipv4Addr::is_loopback()`] and\n   311:     /// [`Ipv6Addr::is_loopback()`] for more details.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::IpAddr::to_canonical",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
    "verification_source": "   481:     /// ```\n   482:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   483:     ///\n   484:     /// let localhost_v4 = Ipv4Addr::new(127, 0, 0, 1);\n   485:     ///\n   486:     /// assert_eq!(IpAddr::V4(localhost_v4).to_canonical(), localhost_v4);\n   487:     /// assert_eq!(IpAddr::V6(localhost_v4.to_ipv6_mapped()).to_canonical(), localhost_v4);\n   488:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)).to_canonical().is_loopback(), true);\n   489:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1)).is_loopback(), false);\n   490:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1)).to_canonical().is_loopback(), true);\n   491:     /// ```\n   492:     #[inline]\n   493:     #[must_use = \"this returns the result of the operation, \\\n   494:                   without modifying the original\"]\n   495:     #[stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n   496:     #[rustc_const_stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n   497:     pub const fn to_canonical(&self) -> IpAddr {\n   498:         match self {\n   499:             IpAddr::V4(_) => *self,\n   500:             IpAddr::V6(v6) => v6.to_canonical(),\n   501:         }\n   502:     }\n   503: \n   504:     /// Returns the eight-bit integers this address consists of as a slice.\n   505:     ///\n   506:     /// # Examples\n   507:     ///\n   508:     /// ```\n   509:     /// #![feature(ip_as_octets)]\n   510:     ///\n   511:     /// use std::net::{Ipv4Addr, Ipv6Addr, IpAddr};\n   512:     ///\n   513:     /// assert_eq!(IpAddr::V4(Ipv4Addr::LOCALHOST).as_octets(), &[127, 0, 0, 1]);",
    "nanvix_source": "   487:     /// assert_eq!(IpAddr::V6(localhost_v4.to_ipv6_mapped()).to_canonical(), localhost_v4);\n   488:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)).to_canonical().is_loopback(), true);\n   489:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1)).is_loopback(), false);\n   490:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0, 0, 0, 0, 0, 0xffff, 0x7f00, 0x1)).to_canonical().is_loopback(), true);\n   491:     /// ```\n   492:     #[inline]\n   493:     #[must_use = \"this returns the result of the operation, \\\n   494:                   without modifying the original\"]\n   495:     #[stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n   496:     #[rustc_const_stable(feature = \"ip_to_canonical\", since = \"1.75.0\")]\n   497:     pub const fn to_canonical(&self) -> IpAddr {\n   498:         match self {\n   499:             IpAddr::V4(_) => *self,\n   500:             IpAddr::V6(v6) => v6.to_canonical(),\n   501:         }\n   502:     }\n   503: \n   504:     /// Returns the eight-bit integers this address consists of as a slice.\n   505:     ///\n   506:     /// # Examples\n   507:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::from_bits",
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
            "bits",
            {
              "primitive": "u32"
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
    "verification_source": "   592:     /// Converts a native byte order `u32` into an IPv4 address.\n   593:     ///\n   594:     /// See [`Ipv4Addr::to_bits`] for an explanation on endianness.\n   595:     ///\n   596:     /// # Examples\n   597:     ///\n   598:     /// ```\n   599:     /// use std::net::Ipv4Addr;\n   600:     ///\n   601:     /// let addr = Ipv4Addr::from_bits(0x12345678);\n   602:     /// assert_eq!(Ipv4Addr::new(0x12, 0x34, 0x56, 0x78), addr);\n   603:     /// ```\n   604:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   605:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   606:     #[must_use]\n   607:     #[inline]\n   608:     pub const fn from_bits(bits: u32) -> Ipv4Addr {\n   609:         Ipv4Addr { octets: bits.to_be_bytes() }\n   610:     }\n   611: \n   612:     /// An IPv4 address with the address pointing to localhost: `127.0.0.1`\n   613:     ///\n   614:     /// # Examples\n   615:     ///\n   616:     /// ```\n   617:     /// use std::net::Ipv4Addr;\n   618:     ///\n   619:     /// let addr = Ipv4Addr::LOCALHOST;\n   620:     /// assert_eq!(addr, Ipv4Addr::new(127, 0, 0, 1));\n   621:     /// ```\n   622:     #[stable(feature = \"ip_constructors\", since = \"1.30.0\")]\n   623:     pub const LOCALHOST: Self = Ipv4Addr::new(127, 0, 0, 1);\n   624: ",
    "nanvix_source": "   598:     /// ```\n   599:     /// use std::net::Ipv4Addr;\n   600:     ///\n   601:     /// let addr = Ipv4Addr::from_bits(0x12345678);\n   602:     /// assert_eq!(Ipv4Addr::new(0x12, 0x34, 0x56, 0x78), addr);\n   603:     /// ```\n   604:     #[rustc_const_stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   605:     #[stable(feature = \"ip_bits\", since = \"1.80.0\")]\n   606:     #[must_use]\n   607:     #[inline]\n   608:     pub const fn from_bits(bits: u32) -> Ipv4Addr {\n   609:         Ipv4Addr { octets: bits.to_be_bytes() }\n   610:     }\n   611: \n   612:     /// An IPv4 address with the address pointing to localhost: `127.0.0.1`\n   613:     ///\n   614:     /// # Examples\n   615:     ///\n   616:     /// ```\n   617:     /// use std::net::Ipv4Addr;\n   618:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::Ipv4Addr::from_octets",
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
            "octets",
            {
              "array": {
                "len": "4",
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
            "id": 9946,
            "path": "Ipv4Addr"
          }
        }
      }
    },
    "verification_source": "   670:     }\n   671: \n   672:     /// Creates an `Ipv4Addr` from a four element byte array.\n   673:     ///\n   674:     /// # Examples\n   675:     ///\n   676:     /// ```\n   677:     /// use std::net::Ipv4Addr;\n   678:     ///\n   679:     /// let addr = Ipv4Addr::from_octets([13u8, 12u8, 11u8, 10u8]);\n   680:     /// assert_eq!(Ipv4Addr::new(13, 12, 11, 10), addr);\n   681:     /// ```\n   682:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n   683:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n   684:     #[must_use]\n   685:     #[inline]\n   686:     pub const fn from_octets(octets: [u8; 4]) -> Ipv4Addr {\n   687:         Ipv4Addr { octets }\n   688:     }\n   689: \n   690:     /// Returns the four eight-bit integers that make up this address\n   691:     /// as a slice.\n   692:     ///\n   693:     /// # Examples\n   694:     ///\n   695:     /// ```\n   696:     /// #![feature(ip_as_octets)]\n   697:     ///\n   698:     /// use std::net::Ipv4Addr;\n   699:     ///\n   700:     /// let addr = Ipv4Addr::new(127, 0, 0, 1);\n   701:     /// assert_eq!(addr.as_octets(), &[127, 0, 0, 1]);\n   702:     /// ```",
    "nanvix_source": "   676:     /// ```\n   677:     /// use std::net::Ipv4Addr;\n   678:     ///\n   679:     /// let addr = Ipv4Addr::from_octets([13u8, 12u8, 11u8, 10u8]);\n   680:     /// assert_eq!(Ipv4Addr::new(13, 12, 11, 10), addr);\n   681:     /// ```\n   682:     #[stable(feature = \"ip_from\", since = \"1.91.0\")]\n   683:     #[rustc_const_stable(feature = \"ip_from\", since = \"1.91.0\")]\n   684:     #[must_use]\n   685:     #[inline]\n   686:     pub const fn from_octets(octets: [u8; 4]) -> Ipv4Addr {\n   687:         Ipv4Addr { octets }\n   688:     }\n   689: \n   690:     /// Returns the four eight-bit integers that make up this address\n   691:     /// as a slice.\n   692:     ///\n   693:     /// # Examples\n   694:     ///\n   695:     /// ```\n   696:     /// #![feature(ip_as_octets)]",
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
