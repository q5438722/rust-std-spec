For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::Utf8Error::error_len",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
      "name": "error_len",
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
            "id": 10083,
            "path": "Utf8Error"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:31700",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10083",
        "resolved_owner_path": [
          "core",
          "str",
          "error",
          "Utf8Error"
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
    "verification_source": "    85:     /// * `None`: the end of the input was reached unexpectedly.\n    86:     ///   `self.valid_up_to()` is 1 to 3 bytes from the end of the input.\n    87:     ///   If a byte stream (such as a file or a network socket) is being decoded incrementally,\n    88:     ///   this could be a valid `char` whose UTF-8 byte sequence is spanning multiple chunks.\n    89:     ///\n    90:     /// * `Some(len)`: an unexpected byte was encountered.\n    91:     ///   The length provided is that of the invalid byte sequence\n    92:     ///   that starts at the index given by `valid_up_to()`.\n    93:     ///   Decoding should resume after that sequence\n    94:     ///   (after inserting a [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD]) in case of\n    95:     ///   lossy decoding.\n    96:     ///\n    97:     /// [U+FFFD]: ../../std/char/constant.REPLACEMENT_CHARACTER.html\n    98:     #[stable(feature = \"utf8_error_error_len\", since = \"1.20.0\")]\n    99:     #[rustc_const_stable(feature = \"const_str_from_utf8_shared\", since = \"1.63.0\")]\n   100:     #[must_use]\n   101:     #[inline]\n   102:     pub const fn error_len(&self) -> Option<usize> {\n   103:         // FIXME(const-hack): This should become `map` again, once it's `const`\n   104:         match self.error_len {\n   105:             Some(len) => Some(len as usize),\n   106:             None => None,\n   107:         }\n   108:     }\n   109: }\n   110: \n   111: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   112: impl fmt::Display for Utf8Error {\n   113:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   114:         if let Some(error_len) = self.error_len {\n   115:             write!(\n   116:                 f,\n   117:                 \"invalid utf-8 sequence of {} bytes from index {}\",",
    "nanvix_source": "    91:     ///   The length provided is that of the invalid byte sequence\n    92:     ///   that starts at the index given by `valid_up_to()`.\n    93:     ///   Decoding should resume after that sequence\n    94:     ///   (after inserting a [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD]) in case of\n    95:     ///   lossy decoding.\n    96:     ///\n    97:     /// [U+FFFD]: ../../std/char/constant.REPLACEMENT_CHARACTER.html\n    98:     #[stable(feature = \"utf8_error_error_len\", since = \"1.20.0\")]\n    99:     #[rustc_const_stable(feature = \"const_str_from_utf8_shared\", since = \"1.63.0\")]\n   100:     #[must_use]\n   101:     #[inline]\n   102:     pub const fn error_len(&self) -> Option<usize> {\n   103:         // FIXME(const-hack): This should become `map` again, once it's `const`\n   104:         match self.error_len {\n   105:             Some(len) => Some(len as usize),\n   106:             None => None,\n   107:         }\n   108:     }\n   109: }\n   110: \n   111: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::Utf8Error::valid_up_to",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
      "name": "valid_up_to",
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
            "id": 10083,
            "path": "Utf8Error"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:31700",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10083",
        "resolved_owner_path": [
          "core",
          "str",
          "error",
          "Utf8Error"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "    63:     /// ```\n    64:     /// use std::str;\n    65:     ///\n    66:     /// // some invalid bytes, in a vector\n    67:     /// let sparkle_heart = vec![0, 159, 146, 150];\n    68:     ///\n    69:     /// // std::str::from_utf8 returns a Utf8Error\n    70:     /// let error = str::from_utf8(&sparkle_heart).unwrap_err();\n    71:     ///\n    72:     /// // the second byte is invalid here\n    73:     /// assert_eq!(1, error.valid_up_to());\n    74:     /// ```\n    75:     #[stable(feature = \"utf8_error\", since = \"1.5.0\")]\n    76:     #[rustc_const_stable(feature = \"const_str_from_utf8_shared\", since = \"1.63.0\")]\n    77:     #[must_use]\n    78:     #[inline]\n    79:     pub const fn valid_up_to(&self) -> usize {\n    80:         self.valid_up_to\n    81:     }\n    82: \n    83:     /// Provides more information about the failure:\n    84:     ///\n    85:     /// * `None`: the end of the input was reached unexpectedly.\n    86:     ///   `self.valid_up_to()` is 1 to 3 bytes from the end of the input.\n    87:     ///   If a byte stream (such as a file or a network socket) is being decoded incrementally,\n    88:     ///   this could be a valid `char` whose UTF-8 byte sequence is spanning multiple chunks.\n    89:     ///\n    90:     /// * `Some(len)`: an unexpected byte was encountered.\n    91:     ///   The length provided is that of the invalid byte sequence\n    92:     ///   that starts at the index given by `valid_up_to()`.\n    93:     ///   Decoding should resume after that sequence\n    94:     ///   (after inserting a [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD]) in case of\n    95:     ///   lossy decoding.",
    "nanvix_source": "    69:     /// // std::str::from_utf8 returns a Utf8Error\n    70:     /// let error = str::from_utf8(&sparkle_heart).unwrap_err();\n    71:     ///\n    72:     /// // the second byte is invalid here\n    73:     /// assert_eq!(1, error.valid_up_to());\n    74:     /// ```\n    75:     #[stable(feature = \"utf8_error\", since = \"1.5.0\")]\n    76:     #[rustc_const_stable(feature = \"const_str_from_utf8_shared\", since = \"1.63.0\")]\n    77:     #[must_use]\n    78:     #[inline]\n    79:     pub const fn valid_up_to(&self) -> usize {\n    80:         self.valid_up_to\n    81:     }\n    82: \n    83:     /// Provides more information about the failure:\n    84:     ///\n    85:     /// * `None`: the end of the input was reached unexpectedly.\n    86:     ///   `self.valid_up_to()` is 1 to 3 bytes from the end of the input.\n    87:     ///   If a byte stream (such as a file or a network socket) is being decoded incrementally,\n    88:     ///   this could be a valid `char` whose UTF-8 byte sequence is spanning multiple chunks.\n    89:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::abs_diff",
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
      "name": "abs_diff",
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
        "impl_id": "core:32378",
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
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "other",
            {
              "resolved_path": {
                "args": null,
                "id": 10186,
                "path": "Duration"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   634: \n   635:     /// Computes the absolute difference between `self` and `other`.\n   636:     ///\n   637:     /// # Examples\n   638:     ///\n   639:     /// ```\n   640:     /// use std::time::Duration;\n   641:     ///\n   642:     /// assert_eq!(Duration::new(100, 0).abs_diff(Duration::new(80, 0)), Duration::new(20, 0));\n   643:     /// assert_eq!(Duration::new(100, 400_000_000).abs_diff(Duration::new(110, 0)), Duration::new(9, 600_000_000));\n   644:     /// ```\n   645:     #[stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   646:     #[rustc_const_stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   647:     #[must_use = \"this returns the result of the operation, \\\n   648:                   without modifying the original\"]\n   649:     #[inline]\n   650:     pub const fn abs_diff(self, other: Duration) -> Duration {\n   651:         if let Some(res) = self.checked_sub(other) { res } else { other.checked_sub(self).unwrap() }\n   652:     }\n   653: \n   654:     /// Checked `Duration` addition. Computes `self + other`, returning [`None`]\n   655:     /// if overflow occurred.\n   656:     ///\n   657:     /// # Examples\n   658:     ///\n   659:     /// ```\n   660:     /// use std::time::Duration;\n   661:     ///\n   662:     /// assert_eq!(Duration::new(0, 0).checked_add(Duration::new(0, 1)), Some(Duration::new(0, 1)));\n   663:     /// assert_eq!(Duration::new(1, 0).checked_add(Duration::new(u64::MAX, 0)), None);\n   664:     /// ```\n   665:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   666:     #[must_use = \"this returns the result of the operation, \\",
    "nanvix_source": "   640:     /// use std::time::Duration;\n   641:     ///\n   642:     /// assert_eq!(Duration::new(100, 0).abs_diff(Duration::new(80, 0)), Duration::new(20, 0));\n   643:     /// assert_eq!(Duration::new(100, 400_000_000).abs_diff(Duration::new(110, 0)), Duration::new(9, 600_000_000));\n   644:     /// ```\n   645:     #[stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   646:     #[rustc_const_stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   647:     #[must_use = \"this returns the result of the operation, \\\n   648:                   without modifying the original\"]\n   649:     #[inline]\n   650:     pub const fn abs_diff(self, other: Duration) -> Duration {\n   651:         if let Some(res) = self.checked_sub(other) { res } else { other.checked_sub(self).unwrap() }\n   652:     }\n   653: \n   654:     /// Checked `Duration` addition. Computes `self + other`, returning [`None`]\n   655:     /// if overflow occurred.\n   656:     ///\n   657:     /// # Examples\n   658:     ///\n   659:     /// ```\n   660:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::as_micros",
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
      "name": "as_micros",
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
        "impl_id": "core:32378",
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
          "primitive": "u128"
        }
      }
    },
    "verification_source": "   596:     }\n   597: \n   598:     /// Returns the total number of whole microseconds contained by this `Duration`.\n   599:     ///\n   600:     /// # Examples\n   601:     ///\n   602:     /// ```\n   603:     /// use std::time::Duration;\n   604:     ///\n   605:     /// let duration = Duration::new(5, 730_023_852);\n   606:     /// assert_eq!(duration.as_micros(), 5_730_023);\n   607:     /// ```\n   608:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   609:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   610:     #[must_use]\n   611:     #[inline]\n   612:     pub const fn as_micros(&self) -> u128 {\n   613:         self.secs as u128 * MICROS_PER_SEC as u128\n   614:             + (self.nanos.as_inner() / NANOS_PER_MICRO) as u128\n   615:     }\n   616: \n   617:     /// Returns the total number of nanoseconds contained by this `Duration`.\n   618:     ///\n   619:     /// # Examples\n   620:     ///\n   621:     /// ```\n   622:     /// use std::time::Duration;\n   623:     ///\n   624:     /// let duration = Duration::new(5, 730_023_852);\n   625:     /// assert_eq!(duration.as_nanos(), 5_730_023_852);\n   626:     /// ```\n   627:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   628:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]",
    "nanvix_source": "   602:     /// ```\n   603:     /// use std::time::Duration;\n   604:     ///\n   605:     /// let duration = Duration::new(5, 730_023_852);\n   606:     /// assert_eq!(duration.as_micros(), 5_730_023);\n   607:     /// ```\n   608:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   609:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   610:     #[must_use]\n   611:     #[inline]\n   612:     pub const fn as_micros(&self) -> u128 {\n   613:         self.secs as u128 * MICROS_PER_SEC as u128\n   614:             + (self.nanos.as_inner() / NANOS_PER_MICRO) as u128\n   615:     }\n   616: \n   617:     /// Returns the total number of nanoseconds contained by this `Duration`.\n   618:     ///\n   619:     /// # Examples\n   620:     ///\n   621:     /// ```\n   622:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::as_millis",
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
      "name": "as_millis",
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
        "impl_id": "core:32378",
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
          "primitive": "u128"
        }
      }
    },
    "verification_source": "   577:     }\n   578: \n   579:     /// Returns the total number of whole milliseconds contained by this `Duration`.\n   580:     ///\n   581:     /// # Examples\n   582:     ///\n   583:     /// ```\n   584:     /// use std::time::Duration;\n   585:     ///\n   586:     /// let duration = Duration::new(5, 730_023_852);\n   587:     /// assert_eq!(duration.as_millis(), 5_730);\n   588:     /// ```\n   589:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   590:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   591:     #[must_use]\n   592:     #[inline]\n   593:     pub const fn as_millis(&self) -> u128 {\n   594:         self.secs as u128 * MILLIS_PER_SEC as u128\n   595:             + (self.nanos.as_inner() / NANOS_PER_MILLI) as u128\n   596:     }\n   597: \n   598:     /// Returns the total number of whole microseconds contained by this `Duration`.\n   599:     ///\n   600:     /// # Examples\n   601:     ///\n   602:     /// ```\n   603:     /// use std::time::Duration;\n   604:     ///\n   605:     /// let duration = Duration::new(5, 730_023_852);\n   606:     /// assert_eq!(duration.as_micros(), 5_730_023);\n   607:     /// ```\n   608:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   609:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]",
    "nanvix_source": "   583:     /// ```\n   584:     /// use std::time::Duration;\n   585:     ///\n   586:     /// let duration = Duration::new(5, 730_023_852);\n   587:     /// assert_eq!(duration.as_millis(), 5_730);\n   588:     /// ```\n   589:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   590:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   591:     #[must_use]\n   592:     #[inline]\n   593:     pub const fn as_millis(&self) -> u128 {\n   594:         self.secs as u128 * MILLIS_PER_SEC as u128\n   595:             + (self.nanos.as_inner() / NANOS_PER_MILLI) as u128\n   596:     }\n   597: \n   598:     /// Returns the total number of whole microseconds contained by this `Duration`.\n   599:     ///\n   600:     /// # Examples\n   601:     ///\n   602:     /// ```\n   603:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::as_nanos",
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
      "name": "as_nanos",
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
        "impl_id": "core:32378",
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
          "primitive": "u128"
        }
      }
    },
    "verification_source": "   615:     }\n   616: \n   617:     /// Returns the total number of nanoseconds contained by this `Duration`.\n   618:     ///\n   619:     /// # Examples\n   620:     ///\n   621:     /// ```\n   622:     /// use std::time::Duration;\n   623:     ///\n   624:     /// let duration = Duration::new(5, 730_023_852);\n   625:     /// assert_eq!(duration.as_nanos(), 5_730_023_852);\n   626:     /// ```\n   627:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   628:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   629:     #[must_use]\n   630:     #[inline]\n   631:     pub const fn as_nanos(&self) -> u128 {\n   632:         self.secs as u128 * NANOS_PER_SEC as u128 + self.nanos.as_inner() as u128\n   633:     }\n   634: \n   635:     /// Computes the absolute difference between `self` and `other`.\n   636:     ///\n   637:     /// # Examples\n   638:     ///\n   639:     /// ```\n   640:     /// use std::time::Duration;\n   641:     ///\n   642:     /// assert_eq!(Duration::new(100, 0).abs_diff(Duration::new(80, 0)), Duration::new(20, 0));\n   643:     /// assert_eq!(Duration::new(100, 400_000_000).abs_diff(Duration::new(110, 0)), Duration::new(9, 600_000_000));\n   644:     /// ```\n   645:     #[stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   646:     #[rustc_const_stable(feature = \"duration_abs_diff\", since = \"1.81.0\")]\n   647:     #[must_use = \"this returns the result of the operation, \\",
    "nanvix_source": "   621:     /// ```\n   622:     /// use std::time::Duration;\n   623:     ///\n   624:     /// let duration = Duration::new(5, 730_023_852);\n   625:     /// assert_eq!(duration.as_nanos(), 5_730_023_852);\n   626:     /// ```\n   627:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   628:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   629:     #[must_use]\n   630:     #[inline]\n   631:     pub const fn as_nanos(&self) -> u128 {\n   632:         self.secs as u128 * NANOS_PER_SEC as u128 + self.nanos.as_inner() as u128\n   633:     }\n   634: \n   635:     /// Computes the absolute difference between `self` and `other`.\n   636:     ///\n   637:     /// # Examples\n   638:     ///\n   639:     /// ```\n   640:     /// use std::time::Duration;\n   641:     ///",
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
