For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::try_from_secs_f32",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_from_secs_f32",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32381",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "secs",
            {
              "primitive": "f32"
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
                        "id": 10186,
                        "path": "Duration"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10189,
                        "path": "TryFromFloatSecsError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1680:     /// let val = f32::from_bits(0x3B40_0000);\n  1681:     /// let res = Duration::try_from_secs_f32(val);\n  1682:     /// assert_eq!(res, Ok(Duration::new(0, 2_929_688)));\n  1683:     ///\n  1684:     /// // this float represents exactly 1.000_976_562_5\n  1685:     /// let val = f32::from_bits(0x3F802000);\n  1686:     /// let res = Duration::try_from_secs_f32(val);\n  1687:     /// assert_eq!(res, Ok(Duration::new(1, 976_562)));\n  1688:     ///\n  1689:     /// // this float represents exactly 1.002_929_687_5\n  1690:     /// let val = f32::from_bits(0x3F806000);\n  1691:     /// let res = Duration::try_from_secs_f32(val);\n  1692:     /// assert_eq!(res, Ok(Duration::new(1, 2_929_688)));\n  1693:     /// ```\n  1694:     #[stable(feature = \"duration_checked_float\", since = \"1.66.0\")]\n  1695:     #[inline]\n  1696:     pub fn try_from_secs_f32(secs: f32) -> Result<Duration, TryFromFloatSecsError> {\n  1697:         try_from_secs!(\n  1698:             secs = secs,\n  1699:             mantissa_bits = 23,\n  1700:             exponent_bits = 8,\n  1701:             offset = 41,\n  1702:             bits_ty = u32,\n  1703:             double_ty = u64,\n  1704:         )\n  1705:     }\n  1706: \n  1707:     /// The checked version of [`from_secs_f64`].\n  1708:     ///\n  1709:     /// [`from_secs_f64`]: Duration::from_secs_f64\n  1710:     ///\n  1711:     /// This constructor will return an `Err` if `secs` is negative, overflows `Duration` or not finite.\n  1712:     ///",
    "nanvix_source": "  1762:     /// let res = Duration::try_from_secs_f32(val);\n  1763:     /// assert_eq!(res, Ok(Duration::new(1, 976_562)));\n  1764:     ///\n  1765:     /// // this float represents exactly 1.002_929_687_5\n  1766:     /// let val = f32::from_bits(0x3F806000);\n  1767:     /// let res = Duration::try_from_secs_f32(val);\n  1768:     /// assert_eq!(res, Ok(Duration::new(1, 2_929_688)));\n  1769:     /// ```\n  1770:     #[stable(feature = \"duration_checked_float\", since = \"1.66.0\")]\n  1771:     #[inline]\n  1772:     pub fn try_from_secs_f32(secs: f32) -> Result<Duration, TryFromFloatSecsError> {\n  1773:         try_from_secs!(\n  1774:             secs = secs,\n  1775:             mantissa_bits = 23,\n  1776:             exponent_bits = 8,\n  1777:             offset = 41,\n  1778:             bits_ty = u32,\n  1779:             double_ty = u64,\n  1780:         )\n  1781:     }\n  1782: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::try_from_secs_f64",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_from_secs_f64",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32381",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "secs",
            {
              "primitive": "f64"
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
                        "id": 10186,
                        "path": "Duration"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10189,
                        "path": "TryFromFloatSecsError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1739:     /// let res = Duration::try_from_secs_f64(0.999e-9);\n  1740:     /// assert_eq!(res, Ok(Duration::new(0, 1)));\n  1741:     /// let res = Duration::try_from_secs_f64(0.999_999_999_499);\n  1742:     /// assert_eq!(res, Ok(Duration::new(0, 999_999_999)));\n  1743:     /// let res = Duration::try_from_secs_f64(0.999_999_999_501);\n  1744:     /// assert_eq!(res, Ok(Duration::new(1, 0)));\n  1745:     /// let res = Duration::try_from_secs_f64(42.999_999_999_499);\n  1746:     /// assert_eq!(res, Ok(Duration::new(42, 999_999_999)));\n  1747:     /// let res = Duration::try_from_secs_f64(42.999_999_999_501);\n  1748:     /// assert_eq!(res, Ok(Duration::new(43, 0)));\n  1749:     ///\n  1750:     /// // this float represents exactly 976562.5e-9\n  1751:     /// let val = f64::from_bits(0x3F50_0000_0000_0000);\n  1752:     /// let res = Duration::try_from_secs_f64(val);\n  1753:     /// assert_eq!(res, Ok(Duration::new(0, 976_562)));\n  1754:     ///\n  1755:     /// // this float represents exactly 2929687.5e-9\n  1756:     /// let val = f64::from_bits(0x3F68_0000_0000_0000);\n  1757:     /// let res = Duration::try_from_secs_f64(val);\n  1758:     /// assert_eq!(res, Ok(Duration::new(0, 2_929_688)));\n  1759:     ///\n  1760:     /// // this float represents exactly 1.000_976_562_5\n  1761:     /// let val = f64::from_bits(0x3FF0_0400_0000_0000);\n  1762:     /// let res = Duration::try_from_secs_f64(val);\n  1763:     /// assert_eq!(res, Ok(Duration::new(1, 976_562)));\n  1764:     ///\n  1765:     /// // this float represents exactly 1.002_929_687_5\n  1766:     /// let val = f64::from_bits(0x3_FF00_C000_0000_000);\n  1767:     /// let res = Duration::try_from_secs_f64(val);\n  1768:     /// assert_eq!(res, Ok(Duration::new(1, 2_929_688)));\n  1769:     /// ```\n  1770:     #[stable(feature = \"duration_checked_float\", since = \"1.66.0\")]\n  1771:     #[inline]",
    "nanvix_source": "  1821:     /// let res = Duration::try_from_secs_f64(42.999_999_999_499);\n  1822:     /// assert_eq!(res, Ok(Duration::new(42, 999_999_999)));\n  1823:     /// let res = Duration::try_from_secs_f64(42.999_999_999_501);\n  1824:     /// assert_eq!(res, Ok(Duration::new(43, 0)));\n  1825:     ///\n  1826:     /// // this float represents exactly 976562.5e-9\n  1827:     /// let val = f64::from_bits(0x3F50_0000_0000_0000);\n  1828:     /// let res = Duration::try_from_secs_f64(val);\n  1829:     /// assert_eq!(res, Ok(Duration::new(0, 976_562)));\n  1830:     ///\n  1831:     /// // this float represents exactly 2929687.5e-9\n  1832:     /// let val = f64::from_bits(0x3F68_0000_0000_0000);\n  1833:     /// let res = Duration::try_from_secs_f64(val);\n  1834:     /// assert_eq!(res, Ok(Duration::new(0, 2_929_688)));\n  1835:     ///\n  1836:     /// // this float represents exactly 1.000_976_562_5\n  1837:     /// let val = f64::from_bits(0x3FF0_0400_0000_0000);\n  1838:     /// let res = Duration::try_from_secs_f64(val);\n  1839:     /// assert_eq!(res, Ok(Duration::new(1, 976_562)));\n  1840:     ///\n  1841:     /// // this float represents exactly 1.002_929_687_5",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::as_encoded_bytes",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_encoded_bytes",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1058:     /// Converts an OS string slice to a byte slice.  To convert the byte slice back into an OS\n  1059:     /// string slice, use the [`OsStr::from_encoded_bytes_unchecked`] function.\n  1060:     ///\n  1061:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n  1062:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n  1063:     /// ASCII.\n  1064:     ///\n  1065:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n  1066:     /// be treated as opaque and only comparable within the same Rust version built for the same\n  1067:     /// target platform.  For example, sending the slice over the network or storing it in a file\n  1068:     /// will likely result in incompatible byte slices.  See [`OsString`] for more encoding details\n  1069:     /// and [`std::ffi`] for platform-specific, specified conversions.\n  1070:     ///\n  1071:     /// [`std::ffi`]: crate::ffi\n  1072:     #[inline]\n  1073:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n  1074:     pub fn as_encoded_bytes(&self) -> &[u8] {\n  1075:         self.inner.as_encoded_bytes()\n  1076:     }\n  1077: \n  1078:     /// Takes a substring based on a range that corresponds to the return value of\n  1079:     /// [`OsStr::as_encoded_bytes`].\n  1080:     ///\n  1081:     /// The range's start and end must lie on valid `OsStr` boundaries.\n  1082:     /// A valid `OsStr` boundary is one of:\n  1083:     /// - The start of the string\n  1084:     /// - The end of the string\n  1085:     /// - Immediately before a valid non-empty UTF-8 substring\n  1086:     /// - Immediately after a valid non-empty UTF-8 substring\n  1087:     ///\n  1088:     /// # Panics\n  1089:     ///\n  1090:     /// Panics if `range` does not lie on valid `OsStr` boundaries or if it",
    "nanvix_source": "  1111:     ///\n  1112:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n  1113:     /// be treated as opaque and only comparable within the same Rust version built for the same\n  1114:     /// target platform.  For example, sending the slice over the network or storing it in a file\n  1115:     /// will likely result in incompatible byte slices.  See [`OsString`] for more encoding details\n  1116:     /// and [`std::ffi`] for platform-specific, specified conversions.\n  1117:     ///\n  1118:     /// [`std::ffi`]: crate::ffi\n  1119:     #[inline]\n  1120:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n  1121:     pub fn as_encoded_bytes(&self) -> &[u8] {\n  1122:         self.inner.as_encoded_bytes()\n  1123:     }\n  1124: \n  1125:     /// Takes a substring based on a range that corresponds to the return value of\n  1126:     /// [`OsStr::as_encoded_bytes`].\n  1127:     ///\n  1128:     /// The range's start and end must lie on valid `OsStr` boundaries.\n  1129:     /// A valid `OsStr` boundary is one of:\n  1130:     /// - The start of the string\n  1131:     /// - The end of the string",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::display",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "display",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 2296,
            "path": "Display"
          }
        }
      }
    },
    "verification_source": "  1268:     ///\n  1269:     /// [`Display`]: fmt::Display\n  1270:     /// [`Debug`]: fmt::Debug\n  1271:     ///\n  1272:     /// # Examples\n  1273:     ///\n  1274:     /// ```\n  1275:     /// use std::ffi::OsStr;\n  1276:     ///\n  1277:     /// let s = OsStr::new(\"Hello, world!\");\n  1278:     /// println!(\"{}\", s.display());\n  1279:     /// ```\n  1280:     #[stable(feature = \"os_str_display\", since = \"1.87.0\")]\n  1281:     #[must_use = \"this does not display the `OsStr`; \\\n  1282:                   it returns an object that can be displayed\"]\n  1283:     #[inline]\n  1284:     pub fn display(&self) -> Display<'_> {\n  1285:         Display { os_str: self }\n  1286:     }\n  1287: \n  1288:     /// Returns the same string as a string slice `&OsStr`.\n  1289:     ///\n  1290:     /// This method is redundant when used directly on `&OsStr`, but\n  1291:     /// it helps dereferencing other string-like types to string slices,\n  1292:     /// for example references to `Box<OsStr>` or `Arc<OsStr>`.\n  1293:     #[inline]\n  1294:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]\n  1295:     pub const fn as_os_str(&self) -> &OsStr {\n  1296:         self\n  1297:     }\n  1298: }\n  1299: \n  1300: #[stable(feature = \"box_from_os_str\", since = \"1.17.0\")]",
    "nanvix_source": "  1321:     /// ```\n  1322:     /// use std::ffi::OsStr;\n  1323:     ///\n  1324:     /// let s = OsStr::new(\"Hello, world!\");\n  1325:     /// println!(\"{}\", s.display());\n  1326:     /// ```\n  1327:     #[stable(feature = \"os_str_display\", since = \"1.87.0\")]\n  1328:     #[must_use = \"this does not display the `OsStr`; \\\n  1329:                   it returns an object that can be displayed\"]\n  1330:     #[inline]\n  1331:     pub fn display(&self) -> Display<'_> {\n  1332:         Display { os_str: self }\n  1333:     }\n  1334: \n  1335:     /// Returns the same string as a string slice `&OsStr`.\n  1336:     ///\n  1337:     /// This method is redundant when used directly on `&OsStr`, but\n  1338:     /// it helps dereferencing other string-like types to string slices,\n  1339:     /// for example references to `Box<OsStr>` or `Arc<OsStr>`.\n  1340:     #[inline]\n  1341:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::eq_ignore_ascii_case",
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
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 1857,
                                    "path": "OsStr"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 40,
                        "path": "AsRef"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "S"
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
      "name": "eq_ignore_ascii_case",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
            "other",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1243: \n  1244:     /// Checks that two strings are an ASCII case-insensitive match.\n  1245:     ///\n  1246:     /// Same as `to_ascii_lowercase(a) == to_ascii_lowercase(b)`,\n  1247:     /// but without allocating and copying temporaries.\n  1248:     ///\n  1249:     /// # Examples\n  1250:     ///\n  1251:     /// ```\n  1252:     /// use std::ffi::OsString;\n  1253:     ///\n  1254:     /// assert!(OsString::from(\"Ferris\").eq_ignore_ascii_case(\"FERRIS\"));\n  1255:     /// assert!(OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00f6S\"));\n  1256:     /// assert!(!OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00d6S\"));\n  1257:     /// ```\n  1258:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1259:     pub fn eq_ignore_ascii_case<S: AsRef<OsStr>>(&self, other: S) -> bool {\n  1260:         self.inner.eq_ignore_ascii_case(&other.as_ref().inner)\n  1261:     }\n  1262: \n  1263:     /// Returns an object that implements [`Display`] for safely printing an\n  1264:     /// [`OsStr`] that may contain non-Unicode data. This may perform lossy\n  1265:     /// conversion, depending on the platform.  If you would like an\n  1266:     /// implementation which escapes the [`OsStr`] please use [`Debug`]\n  1267:     /// instead.\n  1268:     ///\n  1269:     /// [`Display`]: fmt::Display\n  1270:     /// [`Debug`]: fmt::Debug\n  1271:     ///\n  1272:     /// # Examples\n  1273:     ///\n  1274:     /// ```\n  1275:     /// use std::ffi::OsStr;",
    "nanvix_source": "  1296:     /// # Examples\n  1297:     ///\n  1298:     /// ```\n  1299:     /// use std::ffi::OsString;\n  1300:     ///\n  1301:     /// assert!(OsString::from(\"Ferris\").eq_ignore_ascii_case(\"FERRIS\"));\n  1302:     /// assert!(OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00f6S\"));\n  1303:     /// assert!(!OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00d6S\"));\n  1304:     /// ```\n  1305:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1306:     pub fn eq_ignore_ascii_case<S: AsRef<OsStr>>(&self, other: S) -> bool {\n  1307:         self.inner.eq_ignore_ascii_case(&other.as_ref().inner)\n  1308:     }\n  1309: \n  1310:     /// Returns an object that implements [`Display`] for safely printing an\n  1311:     /// [`OsStr`] that may contain non-Unicode data. This may perform lossy\n  1312:     /// conversion, depending on the platform.  If you would like an\n  1313:     /// implementation which escapes the [`OsStr`] please use [`Debug`]\n  1314:     /// instead.\n  1315:     ///\n  1316:     /// [`Display`]: fmt::Display",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::into_os_string",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "into_os_string",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "generic": "Self"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 216,
                "path": "Box"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "  1037:     /// let os_str = OsStr::new(\"\");\n  1038:     /// assert_eq!(os_str.len(), 0);\n  1039:     ///\n  1040:     /// let os_str = OsStr::new(\"foo\");\n  1041:     /// assert_eq!(os_str.len(), 3);\n  1042:     /// ```\n  1043:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1044:     #[must_use]\n  1045:     #[inline]\n  1046:     pub fn len(&self) -> usize {\n  1047:         self.inner.inner.len()\n  1048:     }\n  1049: \n  1050:     /// Converts a <code>[Box]<[OsStr]></code> into an [`OsString`] without copying or allocating.\n  1051:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n  1052:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1053:     pub fn into_os_string(self: Box<Self>) -> OsString {\n  1054:         let boxed = unsafe { Box::from_raw(Box::into_raw(self) as *mut Slice) };\n  1055:         OsString { inner: Buf::from_box(boxed) }\n  1056:     }\n  1057: \n  1058:     /// Converts an OS string slice to a byte slice.  To convert the byte slice back into an OS\n  1059:     /// string slice, use the [`OsStr::from_encoded_bytes_unchecked`] function.\n  1060:     ///\n  1061:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n  1062:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n  1063:     /// ASCII.\n  1064:     ///\n  1065:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n  1066:     /// be treated as opaque and only comparable within the same Rust version built for the same\n  1067:     /// target platform.  For example, sending the slice over the network or storing it in a file\n  1068:     /// will likely result in incompatible byte slices.  See [`OsString`] for more encoding details\n  1069:     /// and [`std::ffi`] for platform-specific, specified conversions.",
    "nanvix_source": "  1035:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1036:     #[must_use]\n  1037:     #[inline]\n  1038:     pub fn len(&self) -> usize {\n  1039:         self.inner.inner.len()\n  1040:     }\n  1041: \n  1042:     /// Converts a <code>[Box]<[OsStr]></code> into an [`OsString`] without copying or allocating.\n  1043:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n  1044:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1045:     pub fn into_os_string(self: Box<Self>) -> OsString {\n  1046:         let boxed = unsafe { Box::from_raw(Box::into_raw(self) as *mut Slice) };\n  1047:         OsString { inner: Buf::from_box(boxed) }\n  1048:     }\n  1049: \n  1050:     /// Divides one string slice into two at an index.\n  1051:     ///\n  1052:     /// The two slices returned go from the start of the string slice to `mid`, and from `mid` to the end of the string slice.\n  1053:     ///\n  1054:     /// The argument, `mid`, should be a byte offset from the start of the string.\n  1055:     /// It must also be on a valid `OsStr` boundary.",
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
