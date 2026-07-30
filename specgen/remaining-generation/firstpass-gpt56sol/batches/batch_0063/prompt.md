For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Formatter::sign_plus",
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
      "name": "sign_plus",
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
    "verification_source": "  2299:     ///             write!(formatter,\n  2300:     ///                    \"Foo({}{})\",\n  2301:     ///                    if self.0 < 0 { '-' } else { '+' },\n  2302:     ///                    self.0.abs())\n  2303:     ///         } else {\n  2304:     ///             write!(formatter, \"Foo({})\", self.0)\n  2305:     ///         }\n  2306:     ///     }\n  2307:     /// }\n  2308:     ///\n  2309:     /// assert_eq!(format!(\"{:+}\", Foo(23)), \"Foo(+23)\");\n  2310:     /// assert_eq!(format!(\"{:+}\", Foo(-23)), \"Foo(-23)\");\n  2311:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2312:     /// ```\n  2313:     #[must_use]\n  2314:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2315:     pub fn sign_plus(&self) -> bool {\n  2316:         self.options.flags & flags::SIGN_PLUS_FLAG != 0\n  2317:     }\n  2318: \n  2319:     /// Determines if the `-` flag was specified.\n  2320:     ///\n  2321:     /// # Examples\n  2322:     ///\n  2323:     /// ```\n  2324:     /// use std::fmt;\n  2325:     ///\n  2326:     /// struct Foo(i32);\n  2327:     ///\n  2328:     /// impl fmt::Display for Foo {\n  2329:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2330:     ///         if formatter.sign_minus() {\n  2331:     ///             // You want a minus sign? Have one!",
    "nanvix_source": "  2305:     ///         }\n  2306:     ///     }\n  2307:     /// }\n  2308:     ///\n  2309:     /// assert_eq!(format!(\"{:+}\", Foo(23)), \"Foo(+23)\");\n  2310:     /// assert_eq!(format!(\"{:+}\", Foo(-23)), \"Foo(-23)\");\n  2311:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2312:     /// ```\n  2313:     #[must_use]\n  2314:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2315:     pub fn sign_plus(&self) -> bool {\n  2316:         self.options.flags & flags::SIGN_PLUS_FLAG != 0\n  2317:     }\n  2318: \n  2319:     /// Determines if the `-` flag was specified.\n  2320:     ///\n  2321:     /// # Examples\n  2322:     ///\n  2323:     /// ```\n  2324:     /// use std::fmt;\n  2325:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::width",
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
      "name": "width",
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
    "verification_source": "  2228:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2229:     ///         if let Some(width) = formatter.width() {\n  2230:     ///             // If we received a width, we use it\n  2231:     ///             write!(formatter, \"{:width$}\", format!(\"Foo({})\", self.0), width = width)\n  2232:     ///         } else {\n  2233:     ///             // Otherwise we do nothing special\n  2234:     ///             write!(formatter, \"Foo({})\", self.0)\n  2235:     ///         }\n  2236:     ///     }\n  2237:     /// }\n  2238:     ///\n  2239:     /// assert_eq!(format!(\"{:10}\", Foo(23)), \"Foo(23)   \");\n  2240:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2241:     /// ```\n  2242:     #[must_use]\n  2243:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2244:     pub fn width(&self) -> Option<usize> {\n  2245:         if self.options.flags & flags::WIDTH_FLAG == 0 {\n  2246:             None\n  2247:         } else {\n  2248:             Some(self.options.width as usize)\n  2249:         }\n  2250:     }\n  2251: \n  2252:     /// Returns the optionally specified precision for numeric types.\n  2253:     /// Alternatively, the maximum width for string types.\n  2254:     ///\n  2255:     /// # Examples\n  2256:     ///\n  2257:     /// ```\n  2258:     /// use std::fmt;\n  2259:     ///\n  2260:     /// struct Foo(f32);",
    "nanvix_source": "  2234:     ///             write!(formatter, \"Foo({})\", self.0)\n  2235:     ///         }\n  2236:     ///     }\n  2237:     /// }\n  2238:     ///\n  2239:     /// assert_eq!(format!(\"{:10}\", Foo(23)), \"Foo(23)   \");\n  2240:     /// assert_eq!(format!(\"{}\", Foo(23)), \"Foo(23)\");\n  2241:     /// ```\n  2242:     #[must_use]\n  2243:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2244:     pub fn width(&self) -> Option<usize> {\n  2245:         if self.options.flags & flags::WIDTH_FLAG == 0 {\n  2246:             None\n  2247:         } else {\n  2248:             Some(self.options.width as usize)\n  2249:         }\n  2250:     }\n  2251: \n  2252:     /// Returns the optionally specified precision for numeric types.\n  2253:     /// Alternatively, the maximum width for string types.\n  2254:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::write_fmt",
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
      "name": "write_fmt",
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
            "fmt",
            {
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
                "id": 10035,
                "path": "Arguments"
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
    "verification_source": "  2112:     /// ```\n  2113:     /// use std::fmt;\n  2114:     ///\n  2115:     /// struct Foo(i32);\n  2116:     ///\n  2117:     /// impl fmt::Display for Foo {\n  2118:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2119:     ///         formatter.write_fmt(format_args!(\"Foo {}\", self.0))\n  2120:     ///     }\n  2121:     /// }\n  2122:     ///\n  2123:     /// assert_eq!(format!(\"{}\", Foo(-1)), \"Foo -1\");\n  2124:     /// assert_eq!(format!(\"{:0>8}\", Foo(2)), \"Foo 2\");\n  2125:     /// ```\n  2126:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2127:     #[inline]\n  2128:     pub fn write_fmt(&mut self, fmt: Arguments<'_>) -> Result {\n  2129:         if let Some(s) = fmt.as_statically_known_str() {\n  2130:             self.buf.write_str(s)\n  2131:         } else {\n  2132:             write(self.buf, fmt)\n  2133:         }\n  2134:     }\n  2135: \n  2136:     /// Returns flags for formatting.\n  2137:     #[must_use]\n  2138:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2139:     #[deprecated(\n  2140:         since = \"1.24.0\",\n  2141:         note = \"use the `sign_plus`, `sign_minus`, `alternate`, \\\n  2142:                 or `sign_aware_zero_pad` methods instead\"\n  2143:     )]\n  2144:     pub fn flags(&self) -> u32 {",
    "nanvix_source": "  2118:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2119:     ///         formatter.write_fmt(format_args!(\"Foo {}\", self.0))\n  2120:     ///     }\n  2121:     /// }\n  2122:     ///\n  2123:     /// assert_eq!(format!(\"{}\", Foo(-1)), \"Foo -1\");\n  2124:     /// assert_eq!(format!(\"{:0>8}\", Foo(2)), \"Foo 2\");\n  2125:     /// ```\n  2126:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2127:     #[inline]\n  2128:     pub fn write_fmt(&mut self, fmt: Arguments<'_>) -> Result {\n  2129:         if let Some(s) = fmt.as_statically_known_str() {\n  2130:             self.buf.write_str(s)\n  2131:         } else {\n  2132:             write(self.buf, fmt)\n  2133:         }\n  2134:     }\n  2135: \n  2136:     /// Returns flags for formatting.\n  2137:     #[must_use]\n  2138:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::write_str",
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
      "name": "write_str",
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
            "data",
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
    "verification_source": "  2083:     /// use std::fmt;\n  2084:     ///\n  2085:     /// struct Foo;\n  2086:     ///\n  2087:     /// impl fmt::Display for Foo {\n  2088:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2089:     ///         formatter.write_str(\"Foo\")\n  2090:     ///         // This is equivalent to:\n  2091:     ///         // write!(formatter, \"Foo\")\n  2092:     ///     }\n  2093:     /// }\n  2094:     ///\n  2095:     /// assert_eq!(format!(\"{Foo}\"), \"Foo\");\n  2096:     /// assert_eq!(format!(\"{Foo:0>8}\"), \"Foo\");\n  2097:     /// ```\n  2098:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2099:     pub fn write_str(&mut self, data: &str) -> Result {\n  2100:         self.buf.write_str(data)\n  2101:     }\n  2102: \n  2103:     /// Glue for usage of the [`write!`] macro with implementors of this trait.\n  2104:     ///\n  2105:     /// This method should generally not be invoked manually, but rather through\n  2106:     /// the [`write!`] macro itself.\n  2107:     ///\n  2108:     /// Writes some formatted information into this instance.\n  2109:     ///\n  2110:     /// # Examples\n  2111:     ///\n  2112:     /// ```\n  2113:     /// use std::fmt;\n  2114:     ///\n  2115:     /// struct Foo(i32);",
    "nanvix_source": "  2089:     ///         formatter.write_str(\"Foo\")\n  2090:     ///         // This is equivalent to:\n  2091:     ///         // write!(formatter, \"Foo\")\n  2092:     ///     }\n  2093:     /// }\n  2094:     ///\n  2095:     /// assert_eq!(format!(\"{Foo}\"), \"Foo\");\n  2096:     /// assert_eq!(format!(\"{Foo:0>8}\"), \"Foo\");\n  2097:     /// ```\n  2098:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2099:     pub fn write_str(&mut self, data: &str) -> Result {\n  2100:         self.buf.write_str(data)\n  2101:     }\n  2102: \n  2103:     /// Glue for usage of the [`write!`] macro with implementors of this trait.\n  2104:     ///\n  2105:     /// This method should generally not be invoked manually, but rather through\n  2106:     /// the [`write!`] macro itself.\n  2107:     ///\n  2108:     /// Writes some formatted information into this instance.\n  2109:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::NumBuffer::new",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13429,
            "path": "NumBuffer"
          }
        },
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
                          "args": null,
                          "id": 29877,
                          "path": "NumBufferTrait"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29906",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13429",
        "resolved_owner_path": [
          "core",
          "fmt",
          "num_buffer",
          "NumBuffer"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "    17:             }\n    18:             #[unstable(feature = \"int_format_into\", issue = \"138215\")]\n    19:             impl NumBufferTrait for $unsigned {\n    20:                 const BUF_SIZE: usize = $unsigned::MAX.ilog(10) as usize + 1;\n    21:             }\n    22:         )*\n    23:     }\n    24: }\n    25: \n    26: impl_NumBufferTrait! {\n    27:     i8, u8,\n    28:     i16, u16,\n    29:     i32, u32,\n    30:     i64, u64,\n    31:     isize, usize,\n    32:     i128, u128,\n    33: }\n    34: \n    35: /// A buffer wrapper of which the internal size is based on the maximum\n    36: /// number of digits the associated integer can have.\n    37: #[unstable(feature = \"int_format_into\", issue = \"138215\")]\n    38: #[derive(Debug)]\n    39: pub struct NumBuffer<T: NumBufferTrait> {\n    40:     // FIXME: Once const generics feature is working, use `T::BUF_SIZE` instead of 40.\n    41:     pub(crate) buf: [MaybeUninit<u8>; 40],\n    42:     // FIXME: Remove this field once we can actually use `T`.\n    43:     phantom: core::marker::PhantomData<T>,\n    44: }\n    45: \n    46: #[unstable(feature = \"int_format_into\", issue = \"138215\")]\n    47: impl<T: NumBufferTrait> NumBuffer<T> {\n    48:     /// Initializes internal buffer.\n    49:     #[unstable(feature = \"int_format_into\", issue = \"138215\")]",
    "nanvix_source": "    45: ///\n    46: /// ```\n    47: /// use core::fmt::NumBuffer;\n    48: ///\n    49: /// let mut buf = NumBuffer::new();\n    50: /// let n1 = 1972u32;\n    51: /// assert_eq!(n1.format_into(&mut buf), \"1972\");\n    52: ///\n    53: /// // Formatting a negative integer includes the sign.\n    54: /// let mut buf = NumBuffer::new();\n    55: /// let n2 = -1972i32;\n    56: /// assert_eq!(n2.format_into(&mut buf), \"-1972\");\n    57: /// ```\n    58: #[stable(feature = \"int_format_into\", since = \"CURRENT_RUSTC_VERSION\")]\n    59: pub struct NumBuffer<T: NumBufferTrait> {\n    60:     pub(crate) buf: T::Buf,\n    61:     phantom: core::marker::PhantomData<T>,\n    62: }\n    63: \n    64: #[stable(feature = \"int_format_into\", since = \"CURRENT_RUSTC_VERSION\")]\n    65: impl<T: NumBufferTrait> core::fmt::Debug for NumBuffer<T> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::and",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "and",
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
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "res",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "generic": "U"
                        }
                      },
                      {
                        "type": {
                          "generic": "E"
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
                      "generic": "U"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
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
    "verification_source": "  1426:     ///\n  1427:     /// let x: Result<u32, &str> = Err(\"early error\");\n  1428:     /// let y: Result<&str, &str> = Ok(\"foo\");\n  1429:     /// assert_eq!(x.and(y), Err(\"early error\"));\n  1430:     ///\n  1431:     /// let x: Result<u32, &str> = Err(\"not a 2\");\n  1432:     /// let y: Result<&str, &str> = Err(\"late error\");\n  1433:     /// assert_eq!(x.and(y), Err(\"not a 2\"));\n  1434:     ///\n  1435:     /// let x: Result<u32, &str> = Ok(2);\n  1436:     /// let y: Result<&str, &str> = Ok(\"different result type\");\n  1437:     /// assert_eq!(x.and(y), Ok(\"different result type\"));\n  1438:     /// ```\n  1439:     #[inline]\n  1440:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1441:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1442:     pub const fn and<U>(self, res: Result<U, E>) -> Result<U, E>\n  1443:     where\n  1444:         T: [const] Destruct,\n  1445:         E: [const] Destruct,\n  1446:         U: [const] Destruct,\n  1447:     {\n  1448:         match self {\n  1449:             Ok(_) => res,\n  1450:             Err(e) => Err(e),\n  1451:         }\n  1452:     }\n  1453: \n  1454:     /// Calls `op` if the result is [`Ok`], otherwise returns the [`Err`] value of `self`.\n  1455:     ///\n  1456:     ///\n  1457:     /// This function can be used for control flow based on `Result` values.\n  1458:     ///",
    "nanvix_source": "  1430:     /// let y: Result<&str, &str> = Err(\"late error\");\n  1431:     /// assert_eq!(x.and(y), Err(\"not a 2\"));\n  1432:     ///\n  1433:     /// let x: Result<u32, &str> = Ok(2);\n  1434:     /// let y: Result<&str, &str> = Ok(\"different result type\");\n  1435:     /// assert_eq!(x.and(y), Ok(\"different result type\"));\n  1436:     /// ```\n  1437:     #[inline]\n  1438:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1439:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1440:     pub const fn and<U>(self, res: Result<U, E>) -> Result<U, E>\n  1441:     where\n  1442:         T: [const] Destruct,\n  1443:         E: [const] Destruct,\n  1444:         U: [const] Destruct,\n  1445:     {\n  1446:         match self {\n  1447:             Ok(_) => res,\n  1448:             Err(e) => Err(e),\n  1449:         }\n  1450:     }",
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
