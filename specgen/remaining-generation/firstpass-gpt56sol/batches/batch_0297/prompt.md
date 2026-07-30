For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::Shr::shr",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "shr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:5018",
        "kind": "trait",
        "name": "Shr",
        "path": [
          "core",
          "ops",
          "bit",
          "Shr"
        ]
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "qualified_path": {
            "args": null,
            "name": "Output",
            "self_type": {
              "generic": "Self"
            },
            "trait": {
              "args": null,
              "id": 5018,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "   583: )]\n   584: pub const trait Shr<Rhs = Self> {\n   585:     /// The resulting type after applying the `>>` operator.\n   586:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   587:     type Output;\n   588: \n   589:     /// Performs the `>>` operation.\n   590:     ///\n   591:     /// # Examples\n   592:     ///\n   593:     /// ```\n   594:     /// assert_eq!(5u8 >> 1, 2);\n   595:     /// assert_eq!(2u8 >> 1, 1);\n   596:     /// ```\n   597:     #[must_use]\n   598:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   599:     fn shr(self, rhs: Rhs) -> Self::Output;\n   600: }\n   601: \n   602: macro_rules! shr_impl {\n   603:     ($t:ty, $f:ty) => {\n   604:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   605:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   606:         impl const Shr<$f> for $t {\n   607:             type Output = $t;\n   608: \n   609:             #[inline]\n   610:             #[track_caller]\n   611:             #[rustc_inherit_overflow_checks]\n   612:             fn shr(self, other: $f) -> $t {\n   613:                 self >> other\n   614:             }\n   615:         }",
    "nanvix_source": "   589:     /// Performs the `>>` operation.\n   590:     ///\n   591:     /// # Examples\n   592:     ///\n   593:     /// ```\n   594:     /// assert_eq!(5u8 >> 1, 2);\n   595:     /// assert_eq!(2u8 >> 1, 1);\n   596:     /// ```\n   597:     #[must_use]\n   598:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   599:     fn shr(self, rhs: Rhs) -> Self::Output;\n   600: }\n   601: \n   602: macro_rules! shr_impl {\n   603:     ($t:ty, $f:ty) => {\n   604:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   605:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   606:         const impl Shr<$f> for $t {\n   607:             type Output = $t;\n   608: \n   609:             #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ShrAssign::shr_assign",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "shr_assign",
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
        "item_id": "core:5030",
        "kind": "trait",
        "name": "ShrAssign",
        "path": [
          "core",
          "ops",
          "bit",
          "ShrAssign"
        ]
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1023:     message = \"no implementation for `{Self} >>= {Rhs}`\",\n  1024:     label = \"no implementation for `{Self} >>= {Rhs}`\"\n  1025: )]\n  1026: pub const trait ShrAssign<Rhs = Self> {\n  1027:     /// Performs the `>>=` operation.\n  1028:     ///\n  1029:     /// # Examples\n  1030:     ///\n  1031:     /// ```\n  1032:     /// let mut x: u8 = 5;\n  1033:     /// x >>= 1;\n  1034:     /// assert_eq!(x, 2);\n  1035:     ///\n  1036:     /// let mut x: u8 = 2;\n  1037:     /// x >>= 1;\n  1038:     /// assert_eq!(x, 1);\n  1039:     /// ```\n  1040:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1041:     fn shr_assign(&mut self, rhs: Rhs);\n  1042: }\n  1043: \n  1044: macro_rules! shr_assign_impl {\n  1045:     ($t:ty, $f:ty) => {\n  1046:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1047:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n  1048:         impl const ShrAssign<$f> for $t {\n  1049:             #[inline]\n  1050:             #[track_caller]\n  1051:             #[rustc_inherit_overflow_checks]\n  1052:             fn shr_assign(&mut self, other: $f) {\n  1053:                 *self >>= other\n  1054:             }\n  1055:         }",
    "nanvix_source": "  1029:     /// # Examples\n  1030:     ///\n  1031:     /// ```\n  1032:     /// let mut x: u8 = 5;\n  1033:     /// x >>= 1;\n  1034:     /// assert_eq!(x, 2);\n  1035:     ///\n  1036:     /// let mut x: u8 = 2;\n  1037:     /// x >>= 1;\n  1038:     /// assert_eq!(x, 1);\n  1039:     /// ```\n  1040:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1041:     fn shr_assign(&mut self, rhs: Rhs);\n  1042: }\n  1043: \n  1044: macro_rules! shr_assign_impl {\n  1045:     ($t:ty, $f:ty) => {\n  1046:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1047:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n  1048:         const impl ShrAssign<$f> for $t {\n  1049:             #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::SubAssign::sub_assign",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "sub_assign",
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
        "item_id": "core:2644",
        "kind": "trait",
        "name": "SubAssign",
        "path": [
          "core",
          "ops",
          "arith",
          "SubAssign"
        ]
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   834:     message = \"cannot subtract-assign `{Rhs}` from `{Self}`\",\n   835:     label = \"no implementation for `{Self} -= {Rhs}`\"\n   836: )]\n   837: #[doc(alias = \"-\")]\n   838: #[doc(alias = \"-=\")]\n   839: pub const trait SubAssign<Rhs = Self> {\n   840:     /// Performs the `-=` operation.\n   841:     ///\n   842:     /// # Example\n   843:     ///\n   844:     /// ```\n   845:     /// let mut x: u32 = 12;\n   846:     /// x -= 1;\n   847:     /// assert_eq!(x, 11);\n   848:     /// ```\n   849:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   850:     fn sub_assign(&mut self, rhs: Rhs);\n   851: }\n   852: \n   853: macro_rules! sub_assign_impl {\n   854:     ($($t:ty)+) => ($(\n   855:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   856:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   857:         impl const SubAssign for $t {\n   858:             #[inline]\n   859:             #[track_caller]\n   860:             #[rustc_inherit_overflow_checks]\n   861:             fn sub_assign(&mut self, other: $t) { *self -= other }\n   862:         }\n   863: \n   864:         forward_ref_op_assign! { impl SubAssign, sub_assign for $t, $t,\n   865:         #[stable(feature = \"op_assign_builtins_by_ref\", since = \"1.22.0\")]\n   866:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }",
    "nanvix_source": "   840:     /// Performs the `-=` operation.\n   841:     ///\n   842:     /// # Example\n   843:     ///\n   844:     /// ```\n   845:     /// let mut x: u32 = 12;\n   846:     /// x -= 1;\n   847:     /// assert_eq!(x, 11);\n   848:     /// ```\n   849:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   850:     fn sub_assign(&mut self, rhs: Rhs);\n   851: }\n   852: \n   853: macro_rules! sub_assign_impl {\n   854:     ($($t:ty)+) => ($(\n   855:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   856:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   857:         const impl SubAssign for $t {\n   858:             #[inline]\n   859:             #[track_caller]\n   860:             #[rustc_inherit_overflow_checks]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::FromStr::from_str",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "from_str",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:941",
        "kind": "trait",
        "name": "FromStr",
        "path": [
          "core",
          "str",
          "traits",
          "FromStr"
        ]
      },
      "signature": {
        "inputs": [
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "Err",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 941,
                          "path": ""
                        }
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
    "verification_source": "   888:     /// Parses a string `s` to return a value of this type.\n   889:     ///\n   890:     /// If parsing succeeds, return the value inside [`Ok`], otherwise\n   891:     /// when the string is ill-formatted return an error specific to the\n   892:     /// inside [`Err`]. The error type is specific to the implementation of the trait.\n   893:     ///\n   894:     /// # Examples\n   895:     ///\n   896:     /// Basic usage with [`i32`], a type that implements `FromStr`:\n   897:     ///\n   898:     /// ```\n   899:     /// use std::str::FromStr;\n   900:     ///\n   901:     /// let s = \"5\";\n   902:     /// let x = i32::from_str(s).unwrap();\n   903:     ///\n   904:     /// assert_eq!(5, x);\n   905:     /// ```\n   906:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   907:     #[rustc_diagnostic_item = \"from_str_method\"]\n   908:     fn from_str(s: &str) -> Result<Self, Self::Err>;\n   909: }\n   910: \n   911: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   912: impl FromStr for bool {\n   913:     type Err = ParseBoolError;\n   914: \n   915:     /// Parse a `bool` from a string.\n   916:     ///\n   917:     /// The only accepted values are `\"true\"` and `\"false\"`. Any other input\n   918:     /// will return an error.\n   919:     ///\n   920:     /// # Examples",
    "nanvix_source": "   879:     /// # Examples\n   880:     ///\n   881:     /// Basic usage with [`i32`], a type that implements `FromStr`:\n   882:     ///\n   883:     /// ```\n   884:     /// use std::str::FromStr;\n   885:     ///\n   886:     /// let s = \"5\";\n   887:     /// let x = i32::from_str(s).unwrap();\n   888:     ///\n   889:     /// assert_eq!(5, x);\n   890:     /// ```\n   891:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   892:     #[rustc_diagnostic_item = \"from_str_method\"]\n   893:     fn from_str(s: &str) -> Result<Self, Self::Err>;\n   894: }\n   895: \n   896: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   897: impl FromStr for bool {\n   898:     type Err = ParseBoolError;\n   899: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::consume",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "consume",
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
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
        ]
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
            "amount",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2367: \n  2368:     /// Marks the given `amount` of additional bytes from the internal buffer as having been read.\n  2369:     /// Subsequent calls to `read` only return bytes that have not been marked as read.\n  2370:     ///\n  2371:     /// This is a lower-level method and is meant to be used together with [`fill_buf`],\n  2372:     /// which can be used to fill the internal buffer via `Read` methods.\n  2373:     ///\n  2374:     /// It is a logic error if `amount` exceeds the number of unread bytes in the internal buffer, which is returned by [`fill_buf`].\n  2375:     ///\n  2376:     /// # Examples\n  2377:     ///\n  2378:     /// Since `consume()` is meant to be used with [`fill_buf`],\n  2379:     /// that method's example includes an example of `consume()`.\n  2380:     ///\n  2381:     /// [`fill_buf`]: BufRead::fill_buf\n  2382:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2383:     fn consume(&mut self, amount: usize);\n  2384: \n  2385:     /// Checks if there is any data left to be `read`.\n  2386:     ///\n  2387:     /// This function may fill the buffer to check for data,\n  2388:     /// so this function returns `Result<bool>`, not `bool`.\n  2389:     ///\n  2390:     /// The default implementation calls `fill_buf` and checks that the\n  2391:     /// returned slice is empty (which means that there is no data left,\n  2392:     /// since EOF is reached).\n  2393:     ///\n  2394:     /// # Errors\n  2395:     ///\n  2396:     /// This function will return an I/O error if a `Read` method was called, but returned an error.\n  2397:     ///\n  2398:     /// Examples\n  2399:     ///",
    "nanvix_source": "  1909:     ///\n  1910:     /// It is a logic error if `amount` exceeds the number of unread bytes in the internal buffer, which is returned by [`fill_buf`].\n  1911:     ///\n  1912:     /// # Examples\n  1913:     ///\n  1914:     /// Since `consume()` is meant to be used with [`fill_buf`],\n  1915:     /// that method's example includes an example of `consume()`.\n  1916:     ///\n  1917:     /// [`fill_buf`]: BufRead::fill_buf\n  1918:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1919:     fn consume(&mut self, amount: usize);\n  1920: \n  1921:     /// Checks if there is any data left to be `read`.\n  1922:     ///\n  1923:     /// This function may fill the buffer to check for data,\n  1924:     /// so this function returns `Result<bool>`, not `bool`.\n  1925:     ///\n  1926:     /// The default implementation calls `fill_buf` and checks that the\n  1927:     /// returned slice is empty (which means that there is no data left,\n  1928:     /// since EOF is reached).\n  1929:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::fill_buf",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "fill_buf",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
        ]
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
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2350:     /// use std::io::prelude::*;\n  2351:     ///\n  2352:     /// let stdin = io::stdin();\n  2353:     /// let mut stdin = stdin.lock();\n  2354:     ///\n  2355:     /// let buffer = stdin.fill_buf()?;\n  2356:     ///\n  2357:     /// // work with buffer\n  2358:     /// println!(\"{buffer:?}\");\n  2359:     ///\n  2360:     /// // mark the bytes we worked with as read\n  2361:     /// let length = buffer.len();\n  2362:     /// stdin.consume(length);\n  2363:     /// # std::io::Result::Ok(())\n  2364:     /// ```\n  2365:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2366:     fn fill_buf(&mut self) -> Result<&[u8]>;\n  2367: \n  2368:     /// Marks the given `amount` of additional bytes from the internal buffer as having been read.\n  2369:     /// Subsequent calls to `read` only return bytes that have not been marked as read.\n  2370:     ///\n  2371:     /// This is a lower-level method and is meant to be used together with [`fill_buf`],\n  2372:     /// which can be used to fill the internal buffer via `Read` methods.\n  2373:     ///\n  2374:     /// It is a logic error if `amount` exceeds the number of unread bytes in the internal buffer, which is returned by [`fill_buf`].\n  2375:     ///\n  2376:     /// # Examples\n  2377:     ///\n  2378:     /// Since `consume()` is meant to be used with [`fill_buf`],\n  2379:     /// that method's example includes an example of `consume()`.\n  2380:     ///\n  2381:     /// [`fill_buf`]: BufRead::fill_buf\n  2382:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "  1892:     ///\n  1893:     /// // work with buffer\n  1894:     /// println!(\"{buffer:?}\");\n  1895:     ///\n  1896:     /// // mark the bytes we worked with as read\n  1897:     /// let length = buffer.len();\n  1898:     /// stdin.consume(length);\n  1899:     /// # std::io::Result::Ok(())\n  1900:     /// ```\n  1901:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1902:     fn fill_buf(&mut self) -> Result<&[u8]>;\n  1903: \n  1904:     /// Marks the given `amount` of additional bytes from the internal buffer as having been read.\n  1905:     /// Subsequent calls to `read` only return bytes that have not been marked as read.\n  1906:     ///\n  1907:     /// This is a lower-level method and is meant to be used together with [`fill_buf`],\n  1908:     /// which can be used to fill the internal buffer via `Read` methods.\n  1909:     ///\n  1910:     /// It is a logic error if `amount` exceeds the number of unread bytes in the internal buffer, which is returned by [`fill_buf`].\n  1911:     ///\n  1912:     /// # Examples",
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
