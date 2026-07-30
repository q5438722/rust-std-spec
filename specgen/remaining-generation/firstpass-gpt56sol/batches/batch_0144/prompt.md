For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::from_secs_f32",
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
      "name": "from_secs_f32",
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
            "secs",
            {
              "primitive": "f32"
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
    "verification_source": "   980:     /// let res = Duration::from_secs_f32(4.2e-7);\n   981:     /// assert_eq!(res, Duration::new(0, 420));\n   982:     /// let res = Duration::from_secs_f32(2.7);\n   983:     /// assert_eq!(res, Duration::new(2, 700_000_048));\n   984:     /// let res = Duration::from_secs_f32(3e10);\n   985:     /// assert_eq!(res, Duration::new(30_000_001_024, 0));\n   986:     /// // subnormal float\n   987:     /// let res = Duration::from_secs_f32(f32::from_bits(1));\n   988:     /// assert_eq!(res, Duration::new(0, 0));\n   989:     /// // conversion uses rounding\n   990:     /// let res = Duration::from_secs_f32(0.999e-9);\n   991:     /// assert_eq!(res, Duration::new(0, 1));\n   992:     /// ```\n   993:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   994:     #[must_use]\n   995:     #[inline]\n   996:     pub fn from_secs_f32(secs: f32) -> Duration {\n   997:         match Duration::try_from_secs_f32(secs) {\n   998:             Ok(v) => v,\n   999:             Err(e) => panic!(\"{e}\"),\n  1000:         }\n  1001:     }\n  1002: \n  1003:     /// Multiplies `Duration` by `f64`.\n  1004:     ///\n  1005:     /// # Panics\n  1006:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1007:     ///\n  1008:     /// # Examples\n  1009:     /// ```\n  1010:     /// use std::time::Duration;\n  1011:     ///\n  1012:     /// let dur = Duration::new(2, 700_000_000);",
    "nanvix_source": "   986:     /// // subnormal float\n   987:     /// let res = Duration::from_secs_f32(f32::from_bits(1));\n   988:     /// assert_eq!(res, Duration::new(0, 0));\n   989:     /// // conversion uses rounding\n   990:     /// let res = Duration::from_secs_f32(0.999e-9);\n   991:     /// assert_eq!(res, Duration::new(0, 1));\n   992:     /// ```\n   993:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   994:     #[must_use]\n   995:     #[inline]\n   996:     pub fn from_secs_f32(secs: f32) -> Duration {\n   997:         match Duration::try_from_secs_f32(secs) {\n   998:             Ok(v) => v,\n   999:             Err(e) => panic!(\"{e}\"),\n  1000:         }\n  1001:     }\n  1002: \n  1003:     /// Multiplies `Duration` by `f64`.\n  1004:     ///\n  1005:     /// # Panics\n  1006:     /// This method will panic if result is negative, overflows `Duration` or not finite.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_secs_f64",
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
      "name": "from_secs_f64",
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
            "secs",
            {
              "primitive": "f64"
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
    "verification_source": "   943:     /// let res = Duration::from_secs_f64(4.2e-7);\n   944:     /// assert_eq!(res, Duration::new(0, 420));\n   945:     /// let res = Duration::from_secs_f64(2.7);\n   946:     /// assert_eq!(res, Duration::new(2, 700_000_000));\n   947:     /// let res = Duration::from_secs_f64(3e10);\n   948:     /// assert_eq!(res, Duration::new(30_000_000_000, 0));\n   949:     /// // subnormal float\n   950:     /// let res = Duration::from_secs_f64(f64::from_bits(1));\n   951:     /// assert_eq!(res, Duration::new(0, 0));\n   952:     /// // conversion uses rounding\n   953:     /// let res = Duration::from_secs_f64(0.999e-9);\n   954:     /// assert_eq!(res, Duration::new(0, 1));\n   955:     /// ```\n   956:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   957:     #[must_use]\n   958:     #[inline]\n   959:     pub fn from_secs_f64(secs: f64) -> Duration {\n   960:         match Duration::try_from_secs_f64(secs) {\n   961:             Ok(v) => v,\n   962:             Err(e) => panic!(\"{e}\"),\n   963:         }\n   964:     }\n   965: \n   966:     /// Creates a new `Duration` from the specified number of seconds represented\n   967:     /// as `f32`.\n   968:     ///\n   969:     /// # Panics\n   970:     /// This constructor will panic if `secs` is negative, overflows `Duration` or not finite.\n   971:     ///\n   972:     /// # Examples\n   973:     /// ```\n   974:     /// use std::time::Duration;\n   975:     ///",
    "nanvix_source": "   949:     /// // subnormal float\n   950:     /// let res = Duration::from_secs_f64(f64::from_bits(1));\n   951:     /// assert_eq!(res, Duration::new(0, 0));\n   952:     /// // conversion uses rounding\n   953:     /// let res = Duration::from_secs_f64(0.999e-9);\n   954:     /// assert_eq!(res, Duration::new(0, 1));\n   955:     /// ```\n   956:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   957:     #[must_use]\n   958:     #[inline]\n   959:     pub fn from_secs_f64(secs: f64) -> Duration {\n   960:         match Duration::try_from_secs_f64(secs) {\n   961:             Ok(v) => v,\n   962:             Err(e) => panic!(\"{e}\"),\n   963:         }\n   964:     }\n   965: \n   966:     /// Creates a new `Duration` from the specified number of seconds represented\n   967:     /// as `f32`.\n   968:     ///\n   969:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::is_zero",
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
      "name": "is_zero",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   462:     /// ```\n   463:     /// use std::time::Duration;\n   464:     ///\n   465:     /// assert!(Duration::ZERO.is_zero());\n   466:     /// assert!(Duration::new(0, 0).is_zero());\n   467:     /// assert!(Duration::from_nanos(0).is_zero());\n   468:     /// assert!(Duration::from_secs(0).is_zero());\n   469:     ///\n   470:     /// assert!(!Duration::new(1, 1).is_zero());\n   471:     /// assert!(!Duration::from_nanos(1).is_zero());\n   472:     /// assert!(!Duration::from_secs(1).is_zero());\n   473:     /// ```\n   474:     #[must_use]\n   475:     #[stable(feature = \"duration_zero\", since = \"1.53.0\")]\n   476:     #[rustc_const_stable(feature = \"duration_zero\", since = \"1.53.0\")]\n   477:     #[inline]\n   478:     pub const fn is_zero(&self) -> bool {\n   479:         self.secs == 0 && self.nanos.as_inner() == 0\n   480:     }\n   481: \n   482:     /// Returns the number of _whole_ seconds contained by this `Duration`.\n   483:     ///\n   484:     /// The returned value does not include the fractional (nanosecond) part of the\n   485:     /// duration, which can be obtained using [`subsec_nanos`].\n   486:     ///\n   487:     /// # Examples\n   488:     ///\n   489:     /// ```\n   490:     /// use std::time::Duration;\n   491:     ///\n   492:     /// let duration = Duration::new(5, 730_023_852);\n   493:     /// assert_eq!(duration.as_secs(), 5);\n   494:     /// ```",
    "nanvix_source": "   468:     /// assert!(Duration::from_secs(0).is_zero());\n   469:     ///\n   470:     /// assert!(!Duration::new(1, 1).is_zero());\n   471:     /// assert!(!Duration::from_nanos(1).is_zero());\n   472:     /// assert!(!Duration::from_secs(1).is_zero());\n   473:     /// ```\n   474:     #[must_use]\n   475:     #[stable(feature = \"duration_zero\", since = \"1.53.0\")]\n   476:     #[rustc_const_stable(feature = \"duration_zero\", since = \"1.53.0\")]\n   477:     #[inline]\n   478:     pub const fn is_zero(&self) -> bool {\n   479:         self.secs == 0 && self.nanos.as_inner() == 0\n   480:     }\n   481: \n   482:     /// Returns the number of _whole_ seconds contained by this `Duration`.\n   483:     ///\n   484:     /// The returned value does not include the fractional (nanosecond) part of the\n   485:     /// duration, which can be obtained using [`subsec_nanos`].\n   486:     ///\n   487:     /// # Examples\n   488:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::mul_f32",
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
      "name": "mul_f32",
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
            "rhs",
            {
              "primitive": "f32"
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
    "verification_source": "  1025:     ///\n  1026:     /// # Panics\n  1027:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1028:     ///\n  1029:     /// # Examples\n  1030:     /// ```\n  1031:     /// use std::time::Duration;\n  1032:     ///\n  1033:     /// let dur = Duration::new(2, 700_000_000);\n  1034:     /// assert_eq!(dur.mul_f32(3.14), Duration::new(8, 478_000_641));\n  1035:     /// assert_eq!(dur.mul_f32(3.14e5), Duration::new(847_800, 0));\n  1036:     /// ```\n  1037:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1038:     #[must_use = \"this returns the result of the operation, \\\n  1039:                   without modifying the original\"]\n  1040:     #[inline]\n  1041:     pub fn mul_f32(self, rhs: f32) -> Duration {\n  1042:         Duration::from_secs_f32(rhs * self.as_secs_f32())\n  1043:     }\n  1044: \n  1045:     /// Divides `Duration` by `f64`.\n  1046:     ///\n  1047:     /// # Panics\n  1048:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1049:     ///\n  1050:     /// # Examples\n  1051:     /// ```\n  1052:     /// use std::time::Duration;\n  1053:     ///\n  1054:     /// let dur = Duration::new(2, 700_000_000);\n  1055:     /// assert_eq!(dur.div_f64(3.14), Duration::new(0, 859_872_611));\n  1056:     /// assert_eq!(dur.div_f64(3.14e5), Duration::new(0, 8_599));\n  1057:     /// ```",
    "nanvix_source": "  1070:     /// // Note that this `3.14_f32` argument already has more floating-point\n  1071:     /// // representation error than a direct `3.14_f64` would, so the result\n  1072:     /// // is slightly different from the ideal 8.478s.\n  1073:     /// assert_eq!(dur.mul_f32(3.14), Duration::new(8, 478_000_283));\n  1074:     /// assert_eq!(dur.mul_f32(3.14e5), Duration::new(847_800, 0));\n  1075:     /// ```\n  1076:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1077:     #[must_use = \"this returns the result of the operation, \\\n  1078:                   without modifying the original\"]\n  1079:     #[inline]\n  1080:     pub fn mul_f32(self, rhs: f32) -> Duration {\n  1081:         self.mul_f64(rhs.into())\n  1082:     }\n  1083: \n  1084:     /// Divides `Duration` by `f64`.\n  1085:     ///\n  1086:     /// # Panics\n  1087:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1088:     ///\n  1089:     /// # Examples\n  1090:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::mul_f64",
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
      "name": "mul_f64",
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
            "rhs",
            {
              "primitive": "f64"
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
    "verification_source": "  1004:     ///\n  1005:     /// # Panics\n  1006:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1007:     ///\n  1008:     /// # Examples\n  1009:     /// ```\n  1010:     /// use std::time::Duration;\n  1011:     ///\n  1012:     /// let dur = Duration::new(2, 700_000_000);\n  1013:     /// assert_eq!(dur.mul_f64(3.14), Duration::new(8, 478_000_000));\n  1014:     /// assert_eq!(dur.mul_f64(3.14e5), Duration::new(847_800, 0));\n  1015:     /// ```\n  1016:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1017:     #[must_use = \"this returns the result of the operation, \\\n  1018:                   without modifying the original\"]\n  1019:     #[inline]\n  1020:     pub fn mul_f64(self, rhs: f64) -> Duration {\n  1021:         Duration::from_secs_f64(rhs * self.as_secs_f64())\n  1022:     }\n  1023: \n  1024:     /// Multiplies `Duration` by `f32`.\n  1025:     ///\n  1026:     /// # Panics\n  1027:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1028:     ///\n  1029:     /// # Examples\n  1030:     /// ```\n  1031:     /// use std::time::Duration;\n  1032:     ///\n  1033:     /// let dur = Duration::new(2, 700_000_000);\n  1034:     /// assert_eq!(dur.mul_f32(3.14), Duration::new(8, 478_000_641));\n  1035:     /// assert_eq!(dur.mul_f32(3.14e5), Duration::new(847_800, 0));\n  1036:     /// ```",
    "nanvix_source": "  1042:     ///\n  1043:     /// ```should_panic\n  1044:     /// # use std::time::Duration;\n  1045:     /// // In the extreme, rounding can even overflow `Duration`, which panics.\n  1046:     /// let _ = Duration::from_secs(u64::MAX).mul_f64(1.0);\n  1047:     /// ```\n  1048:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1049:     #[must_use = \"this returns the result of the operation, \\\n  1050:                   without modifying the original\"]\n  1051:     #[inline]\n  1052:     pub fn mul_f64(self, rhs: f64) -> Duration {\n  1053:         Duration::from_secs_f64(rhs * self.as_secs_f64())\n  1054:     }\n  1055: \n  1056:     /// Multiplies `Duration` by `f32`.\n  1057:     ///\n  1058:     /// Since the significand of `f32` is quite limited compared to the range of `Duration`\n  1059:     /// -- only about 16.8ms of exact nanosecond precision -- this method currently forwards\n  1060:     /// to [`mul_f64`][Self::mul_f64] for greater accuracy.\n  1061:     ///\n  1062:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::new",
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
            "secs",
            {
              "primitive": "u64"
            }
          ],
          [
            "nanos",
            {
              "primitive": "u32"
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
    "verification_source": "   178:     /// # Panics\n   179:     ///\n   180:     /// This constructor will panic if the carry from the nanoseconds overflows\n   181:     /// the seconds counter.\n   182:     ///\n   183:     /// # Examples\n   184:     ///\n   185:     /// ```\n   186:     /// use std::time::Duration;\n   187:     ///\n   188:     /// let five_seconds = Duration::new(5, 0);\n   189:     /// ```\n   190:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   191:     #[inline]\n   192:     #[must_use]\n   193:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   194:     pub const fn new(secs: u64, nanos: u32) -> Duration {\n   195:         if nanos < NANOS_PER_SEC {\n   196:             // SAFETY: nanos < NANOS_PER_SEC, therefore nanos is within the valid range\n   197:             Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }\n   198:         } else {\n   199:             let secs = secs\n   200:                 .checked_add((nanos / NANOS_PER_SEC) as u64)\n   201:                 .expect(\"overflow in Duration::new\");\n   202:             let nanos = nanos % NANOS_PER_SEC;\n   203:             // SAFETY: nanos % NANOS_PER_SEC < NANOS_PER_SEC, therefore nanos is within the valid range\n   204:             Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }\n   205:         }\n   206:     }\n   207: \n   208:     /// Creates a new `Duration` from the specified number of whole seconds.\n   209:     ///\n   210:     /// # Examples",
    "nanvix_source": "   184:     ///\n   185:     /// ```\n   186:     /// use std::time::Duration;\n   187:     ///\n   188:     /// let five_seconds = Duration::new(5, 0);\n   189:     /// ```\n   190:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   191:     #[inline]\n   192:     #[must_use]\n   193:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   194:     pub const fn new(secs: u64, nanos: u32) -> Duration {\n   195:         if nanos < NANOS_PER_SEC {\n   196:             // SAFETY: nanos < NANOS_PER_SEC, therefore nanos is within the valid range\n   197:             Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }\n   198:         } else {\n   199:             let secs = secs\n   200:                 .checked_add((nanos / NANOS_PER_SEC) as u64)\n   201:                 .expect(\"overflow in Duration::new\");\n   202:             let nanos = nanos % NANOS_PER_SEC;\n   203:             // SAFETY: nanos % NANOS_PER_SEC < NANOS_PER_SEC, therefore nanos is within the valid range\n   204:             Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }",
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
