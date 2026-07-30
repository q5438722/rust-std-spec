For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Formatter::flags",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "flags",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
    "verification_source": "  2128:     pub fn write_fmt(&mut self, fmt: Arguments<'_>) -> Result {\n  2129:         if let Some(s) = fmt.as_statically_known_str() {\n  2130:             self.buf.write_str(s)\n  2131:         } else {\n  2132:             write(self.buf, fmt)\n  2133:         }\n  2134:     }\n  2135: \n  2136:     /// Returns flags for formatting.\n  2137:     #[must_use]\n  2138:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2139:     #[deprecated(\n  2140:         since = \"1.24.0\",\n  2141:         note = \"use the `sign_plus`, `sign_minus`, `alternate`, \\\n  2142:                 or `sign_aware_zero_pad` methods instead\"\n  2143:     )]\n  2144:     pub fn flags(&self) -> u32 {\n  2145:         // Extract the debug upper/lower hex, zero pad, alternate, and plus/minus flags\n  2146:         // to stay compatible with older versions of Rust.\n  2147:         self.options.flags >> 21 & 0x3F\n  2148:     }\n  2149: \n  2150:     /// Returns the character used as 'fill' whenever there is alignment.\n  2151:     ///\n  2152:     /// # Examples\n  2153:     ///\n  2154:     /// ```\n  2155:     /// use std::fmt;\n  2156:     ///\n  2157:     /// struct Foo;\n  2158:     ///\n  2159:     /// impl fmt::Display for Foo {\n  2160:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "nanvix_source": "  2134:     }\n  2135: \n  2136:     /// Returns flags for formatting.\n  2137:     #[must_use]\n  2138:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2139:     #[deprecated(\n  2140:         since = \"1.24.0\",\n  2141:         note = \"use the `sign_plus`, `sign_minus`, `alternate`, \\\n  2142:                 or `sign_aware_zero_pad` methods instead\"\n  2143:     )]\n  2144:     pub fn flags(&self) -> u32 {\n  2145:         // Extract the debug upper/lower hex, zero pad, alternate, and plus/minus flags\n  2146:         // to stay compatible with older versions of Rust.\n  2147:         self.options.flags >> 21 & 0x3F\n  2148:     }\n  2149: \n  2150:     /// Returns the character used as 'fill' whenever there is alignment.\n  2151:     ///\n  2152:     /// # Examples\n  2153:     ///\n  2154:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::pad",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "pad",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
            "s",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 919,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1894:     ///\n  1895:     /// ```\n  1896:     /// use std::fmt;\n  1897:     ///\n  1898:     /// struct Foo;\n  1899:     ///\n  1900:     /// impl fmt::Display for Foo {\n  1901:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1902:     ///         formatter.pad(\"Foo\")\n  1903:     ///     }\n  1904:     /// }\n  1905:     ///\n  1906:     /// assert_eq!(format!(\"{Foo:<4}\"), \"Foo \");\n  1907:     /// assert_eq!(format!(\"{Foo:0>4}\"), \"0Foo\");\n  1908:     /// ```\n  1909:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1910:     pub fn pad(&mut self, s: &str) -> Result {\n  1911:         // Make sure there's a fast path up front.\n  1912:         if self.options.flags & (flags::WIDTH_FLAG | flags::PRECISION_FLAG) == 0 {\n  1913:             return self.buf.write_str(s);\n  1914:         }\n  1915: \n  1916:         // The `precision` field can be interpreted as a maximum width for the\n  1917:         // string being formatted.\n  1918:         let (s, char_count) = if let Some(max_char_count) = self.options.get_precision() {\n  1919:             let mut iter = s.char_indices();\n  1920:             let remaining = match iter.advance_by(usize::from(max_char_count)) {\n  1921:                 Ok(()) => 0,\n  1922:                 Err(remaining) => remaining.get(),\n  1923:             };\n  1924:             // SAFETY: The offset of `.char_indices()` is guaranteed to be\n  1925:             // in-bounds and between character boundaries.\n  1926:             let truncated = unsafe { s.get_unchecked(..iter.offset()) };",
    "nanvix_source": "  1900:     /// impl fmt::Display for Foo {\n  1901:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1902:     ///         formatter.pad(\"Foo\")\n  1903:     ///     }\n  1904:     /// }\n  1905:     ///\n  1906:     /// assert_eq!(format!(\"{Foo:<4}\"), \"Foo \");\n  1907:     /// assert_eq!(format!(\"{Foo:0>4}\"), \"0Foo\");\n  1908:     /// ```\n  1909:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1910:     pub fn pad(&mut self, s: &str) -> Result {\n  1911:         // Make sure there's a fast path up front.\n  1912:         if self.options.flags & (flags::WIDTH_FLAG | flags::PRECISION_FLAG) == 0 {\n  1913:             return self.buf.write_str(s);\n  1914:         }\n  1915: \n  1916:         // The `precision` field can be interpreted as a maximum width for the\n  1917:         // string being formatted.\n  1918:         let (s, char_count) = if let Some(max_char_count) = self.options.get_precision() {\n  1919:             let mut iter = s.char_indices();\n  1920:             let remaining = match iter.advance_by(usize::from(max_char_count)) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::pad_integral",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "pad_integral",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
            "is_nonnegative",
            {
              "primitive": "bool"
            }
          ],
          [
            "prefix",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ],
          [
            "buf",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 919,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1810:     /// impl fmt::Display for Foo {\n  1811:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1812:     ///         // We need to remove \"-\" from the number output.\n  1813:     ///         let tmp = self.nb.abs().to_string();\n  1814:     ///\n  1815:     ///         formatter.pad_integral(self.nb >= 0, \"Foo \", &tmp)\n  1816:     ///     }\n  1817:     /// }\n  1818:     ///\n  1819:     /// assert_eq!(format!(\"{}\", Foo::new(2)), \"2\");\n  1820:     /// assert_eq!(format!(\"{}\", Foo::new(-1)), \"-1\");\n  1821:     /// assert_eq!(format!(\"{}\", Foo::new(0)), \"0\");\n  1822:     /// assert_eq!(format!(\"{:#}\", Foo::new(-1)), \"-Foo 1\");\n  1823:     /// assert_eq!(format!(\"{:0>#8}\", Foo::new(-1)), \"00-Foo 1\");\n  1824:     /// ```\n  1825:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1826:     pub fn pad_integral(&mut self, is_nonnegative: bool, prefix: &str, buf: &str) -> Result {\n  1827:         let mut width = buf.len();\n  1828: \n  1829:         let mut sign = None;\n  1830:         if !is_nonnegative {\n  1831:             sign = Some('-');\n  1832:             width += 1;\n  1833:         } else if self.sign_plus() {\n  1834:             sign = Some('+');\n  1835:             width += 1;\n  1836:         }\n  1837: \n  1838:         let prefix = if self.alternate() {\n  1839:             width += prefix.chars().count();\n  1840:             Some(prefix)\n  1841:         } else {\n  1842:             None",
    "nanvix_source": "  1816:     ///     }\n  1817:     /// }\n  1818:     ///\n  1819:     /// assert_eq!(format!(\"{}\", Foo::new(2)), \"2\");\n  1820:     /// assert_eq!(format!(\"{}\", Foo::new(-1)), \"-1\");\n  1821:     /// assert_eq!(format!(\"{}\", Foo::new(0)), \"0\");\n  1822:     /// assert_eq!(format!(\"{:#}\", Foo::new(-1)), \"-Foo 1\");\n  1823:     /// assert_eq!(format!(\"{:0>#8}\", Foo::new(-1)), \"00-Foo 1\");\n  1824:     /// ```\n  1825:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1826:     pub fn pad_integral(&mut self, is_nonnegative: bool, prefix: &str, buf: &str) -> Result {\n  1827:         let mut width = buf.len();\n  1828: \n  1829:         let mut sign = None;\n  1830:         if !is_nonnegative {\n  1831:             sign = Some('-');\n  1832:             width += 1;\n  1833:         } else if self.sign_plus() {\n  1834:             sign = Some('+');\n  1835:             width += 1;\n  1836:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::precision",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "precision",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                      "primitive": "usize"
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
    "verification_source": "  2263:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2264:     ///         if let Some(precision) = formatter.precision() {\n  2265:     ///             // If we received a precision, we use it.\n  2266:     ///             write!(formatter, \"Foo({1:.*})\", precision, self.0)\n  2267:     ///         } else {\n  2268:     ///             // Otherwise we default to 2.\n  2269:     ///             write!(formatter, \"Foo({:.2})\", self.0)\n  2270:     ///         }\n  2271:     ///     }\n  2272:     /// }\n  2273:     ///\n  2274:     /// assert_eq!(format!(\"{:.4}\", Foo(23.2)), \"Foo(23.2000)\");\n  2275:     /// assert_eq!(format!(\"{}\", Foo(23.2)), \"Foo(23.20)\");\n  2276:     /// ```\n  2277:     #[must_use]\n  2278:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2279:     pub fn precision(&self) -> Option<usize> {\n  2280:         if self.options.flags & flags::PRECISION_FLAG == 0 {\n  2281:             None\n  2282:         } else {\n  2283:             Some(self.options.precision as usize)\n  2284:         }\n  2285:     }\n  2286: \n  2287:     /// Determines if the `+` flag was specified.\n  2288:     ///\n  2289:     /// # Examples\n  2290:     ///\n  2291:     /// ```\n  2292:     /// use std::fmt;\n  2293:     ///\n  2294:     /// struct Foo(i32);\n  2295:     ///",
    "nanvix_source": "  2269:     ///             write!(formatter, \"Foo({:.2})\", self.0)\n  2270:     ///         }\n  2271:     ///     }\n  2272:     /// }\n  2273:     ///\n  2274:     /// assert_eq!(format!(\"{:.4}\", Foo(23.2)), \"Foo(23.2000)\");\n  2275:     /// assert_eq!(format!(\"{}\", Foo(23.2)), \"Foo(23.20)\");\n  2276:     /// ```\n  2277:     #[must_use]\n  2278:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2279:     pub fn precision(&self) -> Option<usize> {\n  2280:         if self.options.flags & flags::PRECISION_FLAG == 0 {\n  2281:             None\n  2282:         } else {\n  2283:             Some(self.options.precision as usize)\n  2284:         }\n  2285:     }\n  2286: \n  2287:     /// Determines if the `+` flag was specified.\n  2288:     ///\n  2289:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::sign_aware_zero_pad",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "sign_aware_zero_pad",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
    "verification_source": "  2382:     ///\n  2383:     /// struct Foo(i32);\n  2384:     ///\n  2385:     /// impl fmt::Display for Foo {\n  2386:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2387:     ///         assert!(formatter.sign_aware_zero_pad());\n  2388:     ///         assert_eq!(formatter.width(), Some(4));\n  2389:     ///         // We ignore the formatter's options.\n  2390:     ///         write!(formatter, \"{}\", self.0)\n  2391:     ///     }\n  2392:     /// }\n  2393:     ///\n  2394:     /// assert_eq!(format!(\"{:04}\", Foo(23)), \"23\");\n  2395:     /// ```\n  2396:     #[must_use]\n  2397:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2398:     pub fn sign_aware_zero_pad(&self) -> bool {\n  2399:         self.options.flags & flags::SIGN_AWARE_ZERO_PAD_FLAG != 0\n  2400:     }\n  2401: \n  2402:     // FIXME: Decide what public API we want for these two flags.\n  2403:     // https://github.com/rust-lang/rust/issues/48584\n  2404:     fn debug_lower_hex(&self) -> bool {\n  2405:         self.options.flags & flags::DEBUG_LOWER_HEX_FLAG != 0\n  2406:     }\n  2407:     fn debug_upper_hex(&self) -> bool {\n  2408:         self.options.flags & flags::DEBUG_UPPER_HEX_FLAG != 0\n  2409:     }\n  2410: \n  2411:     /// Creates a [`DebugStruct`] builder designed to assist with creation of\n  2412:     /// [`fmt::Debug`] implementations for structs.\n  2413:     ///\n  2414:     /// [`fmt::Debug`]: self::Debug",
    "nanvix_source": "  2388:     ///         assert_eq!(formatter.width(), Some(4));\n  2389:     ///         // We ignore the formatter's options.\n  2390:     ///         write!(formatter, \"{}\", self.0)\n  2391:     ///     }\n  2392:     /// }\n  2393:     ///\n  2394:     /// assert_eq!(format!(\"{:04}\", Foo(23)), \"23\");\n  2395:     /// ```\n  2396:     #[must_use]\n  2397:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2398:     pub fn sign_aware_zero_pad(&self) -> bool {\n  2399:         self.options.flags & flags::SIGN_AWARE_ZERO_PAD_FLAG != 0\n  2400:     }\n  2401: \n  2402:     // FIXME: Decide what public API we want for these two flags.\n  2403:     // https://github.com/rust-lang/rust/issues/48584\n  2404:     fn debug_lower_hex(&self) -> bool {\n  2405:         self.options.flags & flags::DEBUG_LOWER_HEX_FLAG != 0\n  2406:     }\n  2407:     fn debug_upper_hex(&self) -> bool {\n  2408:         self.options.flags & flags::DEBUG_UPPER_HEX_FLAG != 0",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::sign_minus",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "sign_minus",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
    "verification_source": "  2328:     /// impl fmt::Display for Foo {\n  2329:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2330:     ///         if formatter.sign_minus() {\n  2331:     ///             // You want a minus sign? Have one!\n  2332:     ///             write!(formatter, \"-Foo({})\", self.0)\n  2333:     ///         } else {\n  2334:     ///             write!(formatter, \"Foo({})\", self.0)\n  2335:     ///         }\n  2336:     ///     }\n  2337:     /// }\n  2338:     ///\n  2339:     /// assert_eq!(format!(\"{:-}\", Foo(23)), \"-Foo(23)\");\n  2340:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2341:     /// ```\n  2342:     #[must_use]\n  2343:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2344:     pub fn sign_minus(&self) -> bool {\n  2345:         self.options.flags & flags::SIGN_MINUS_FLAG != 0\n  2346:     }\n  2347: \n  2348:     /// Determines if the `#` flag was specified.\n  2349:     ///\n  2350:     /// # Examples\n  2351:     ///\n  2352:     /// ```\n  2353:     /// use std::fmt;\n  2354:     ///\n  2355:     /// struct Foo(i32);\n  2356:     ///\n  2357:     /// impl fmt::Display for Foo {\n  2358:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2359:     ///         if formatter.alternate() {\n  2360:     ///             write!(formatter, \"Foo({})\", self.0)",
    "nanvix_source": "  2334:     ///             write!(formatter, \"Foo({})\", self.0)\n  2335:     ///         }\n  2336:     ///     }\n  2337:     /// }\n  2338:     ///\n  2339:     /// assert_eq!(format!(\"{:-}\", Foo(23)), \"-Foo(23)\");\n  2340:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2341:     /// ```\n  2342:     #[must_use]\n  2343:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2344:     pub fn sign_minus(&self) -> bool {\n  2345:         self.options.flags & flags::SIGN_MINUS_FLAG != 0\n  2346:     }\n  2347: \n  2348:     /// Determines if the `#` flag was specified.\n  2349:     ///\n  2350:     /// # Examples\n  2351:     ///\n  2352:     /// ```\n  2353:     /// use std::fmt;\n  2354:     ///",
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
