For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::Not::not",
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
      "name": "not",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:2716",
        "kind": "trait",
        "name": "Not",
        "path": [
          "core",
          "ops",
          "bit",
          "Not"
        ]
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
          "qualified_path": {
            "args": null,
            "name": "Output",
            "self_type": {
              "generic": "Self"
            },
            "trait": {
              "args": null,
              "id": 2716,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "    36:     /// The resulting type after applying the `!` operator.\n    37:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    38:     type Output;\n    39: \n    40:     /// Performs the unary `!` operation.\n    41:     ///\n    42:     /// # Examples\n    43:     ///\n    44:     /// ```\n    45:     /// assert_eq!(!true, false);\n    46:     /// assert_eq!(!false, true);\n    47:     /// assert_eq!(!1u8, 254);\n    48:     /// assert_eq!(!0u8, 255);\n    49:     /// ```\n    50:     #[must_use]\n    51:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    52:     fn not(self) -> Self::Output;\n    53: }\n    54: \n    55: macro_rules! not_impl {\n    56:     ($($t:ty)*) => ($(\n    57:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    58:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n    59:         impl const Not for $t {\n    60:             type Output = $t;\n    61: \n    62:             #[inline]\n    63:             fn not(self) -> $t { !self }\n    64:         }\n    65: \n    66:         forward_ref_unop! { impl Not, not for $t,\n    67:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    68:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }",
    "nanvix_source": "    42:     /// # Examples\n    43:     ///\n    44:     /// ```\n    45:     /// assert_eq!(!true, false);\n    46:     /// assert_eq!(!false, true);\n    47:     /// assert_eq!(!1u8, 254);\n    48:     /// assert_eq!(!0u8, 255);\n    49:     /// ```\n    50:     #[must_use]\n    51:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    52:     fn not(self) -> Self::Output;\n    53: }\n    54: \n    55: macro_rules! not_impl {\n    56:     ($($t:ty)*) => ($(\n    57:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    58:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n    59:         const impl Not for $t {\n    60:             type Output = $t;\n    61: \n    62:             #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::RangeBounds::contains",
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
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "U"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
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
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "contains",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:23612",
        "kind": "trait",
        "name": "RangeBounds",
        "path": [
          "core",
          "ops",
          "range",
          "RangeBounds"
        ]
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
            "item",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "U"
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
    "verification_source": "   852: \n   853:     /// Returns `true` if `item` is contained in the range.\n   854:     ///\n   855:     /// # Examples\n   856:     ///\n   857:     /// ```\n   858:     /// assert!( (3..5).contains(&4));\n   859:     /// assert!(!(3..5).contains(&2));\n   860:     ///\n   861:     /// assert!( (0.0..1.0).contains(&0.5));\n   862:     /// assert!(!(0.0..1.0).contains(&f32::NAN));\n   863:     /// assert!(!(0.0..f32::NAN).contains(&0.5));\n   864:     /// assert!(!(f32::NAN..1.0).contains(&0.5));\n   865:     /// ```\n   866:     #[inline]\n   867:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   868:     fn contains<U>(&self, item: &U) -> bool\n   869:     where\n   870:         T: [const] PartialOrd<U>,\n   871:         U: ?Sized + [const] PartialOrd<T>,\n   872:     {\n   873:         (match self.start_bound() {\n   874:             Included(start) => start <= item,\n   875:             Excluded(start) => start < item,\n   876:             Unbounded => true,\n   877:         }) && (match self.end_bound() {\n   878:             Included(end) => item <= end,\n   879:             Excluded(end) => item < end,\n   880:             Unbounded => true,\n   881:         })\n   882:     }\n   883: \n   884:     /// Returns `true` if the range contains no items.",
    "nanvix_source": "   858:     /// assert!( (3..5).contains(&4));\n   859:     /// assert!(!(3..5).contains(&2));\n   860:     ///\n   861:     /// assert!( (0.0..1.0).contains(&0.5));\n   862:     /// assert!(!(0.0..1.0).contains(&f32::NAN));\n   863:     /// assert!(!(0.0..f32::NAN).contains(&0.5));\n   864:     /// assert!(!(f32::NAN..1.0).contains(&0.5));\n   865:     /// ```\n   866:     #[inline]\n   867:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   868:     fn contains<U>(&self, item: &U) -> bool\n   869:     where\n   870:         T: [const] PartialOrd<U>,\n   871:         U: ?Sized + [const] PartialOrd<T>,\n   872:     {\n   873:         (match self.start_bound() {\n   874:             Included(start) => start <= item,\n   875:             Excluded(start) => start < item,\n   876:             Unbounded => true,\n   877:         }) && (match self.end_bound() {\n   878:             Included(end) => item <= end,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::Rem::rem",
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
      "name": "rem",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:1719",
        "kind": "trait",
        "name": "Rem",
        "path": [
          "core",
          "ops",
          "arith",
          "Rem"
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
              "id": 1719,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "   568: #[doc(alias = \"%\")]\n   569: pub const trait Rem<Rhs = Self> {\n   570:     /// The resulting type after applying the `%` operator.\n   571:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   572:     type Output;\n   573: \n   574:     /// Performs the `%` operation.\n   575:     ///\n   576:     /// # Example\n   577:     ///\n   578:     /// ```\n   579:     /// assert_eq!(12 % 10, 2);\n   580:     /// ```\n   581:     #[must_use = \"this returns the result of the operation, without modifying the original\"]\n   582:     #[rustc_diagnostic_item = \"rem\"]\n   583:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   584:     fn rem(self, rhs: Rhs) -> Self::Output;\n   585: }\n   586: \n   587: macro_rules! rem_impl_integer {\n   588:     ($(($($t:ty)*) => $panic:expr),*) => ($($(\n   589:         /// This operation satisfies `n % d == n - (n / d) * d`. The\n   590:         /// result has the same sign as the left operand.\n   591:         ///\n   592:         /// # Panics\n   593:         ///\n   594:         #[doc = $panic]\n   595:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   596:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   597:         impl const Rem for $t {\n   598:             type Output = $t;\n   599: \n   600:             #[inline]",
    "nanvix_source": "   574:     /// Performs the `%` operation.\n   575:     ///\n   576:     /// # Example\n   577:     ///\n   578:     /// ```\n   579:     /// assert_eq!(12 % 10, 2);\n   580:     /// ```\n   581:     #[must_use = \"this returns the result of the operation, without modifying the original\"]\n   582:     #[rustc_diagnostic_item = \"rem\"]\n   583:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   584:     fn rem(self, rhs: Rhs) -> Self::Output;\n   585: }\n   586: \n   587: macro_rules! rem_impl_integer {\n   588:     ($(($($t:ty)*) => $panic:expr),*) => ($($(\n   589:         /// This operation satisfies `n % d == n - (n / d) * d`. The\n   590:         /// result has the same sign as the left operand.\n   591:         ///\n   592:         /// # Panics\n   593:         ///\n   594:         #[doc = $panic]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::RemAssign::rem_assign",
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
      "name": "rem_assign",
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
        "item_id": "core:1722",
        "kind": "trait",
        "name": "RemAssign",
        "path": [
          "core",
          "ops",
          "arith",
          "RemAssign"
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
    "verification_source": "  1010: /// let mut jar = CookieJar { cookies: 31 };\n  1011: /// let piles = 4;\n  1012: ///\n  1013: /// println!(\"Splitting up {} cookies into {} even piles!\", jar.cookies, piles);\n  1014: ///\n  1015: /// jar %= piles;\n  1016: ///\n  1017: /// println!(\"{} cookies remain in the cookie jar!\", jar.cookies);\n  1018: /// ```\n  1019: #[lang = \"rem_assign\"]\n  1020: #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1021: #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n  1022: #[diagnostic::on_unimplemented(\n  1023:     message = \"cannot calculate and assign the remainder of `{Self}` divided by `{Rhs}`\",\n  1024:     label = \"no implementation for `{Self} %= {Rhs}`\"\n  1025: )]\n  1026: #[doc(alias = \"%\")]\n  1027: #[doc(alias = \"%=\")]\n  1028: pub const trait RemAssign<Rhs = Self> {\n  1029:     /// Performs the `%=` operation.\n  1030:     ///\n  1031:     /// # Example\n  1032:     ///\n  1033:     /// ```\n  1034:     /// let mut x: u32 = 12;\n  1035:     /// x %= 10;\n  1036:     /// assert_eq!(x, 2);\n  1037:     /// ```\n  1038:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1039:     fn rem_assign(&mut self, rhs: Rhs);\n  1040: }\n  1041: \n  1042: macro_rules! rem_assign_impl {",
    "nanvix_source": "  1016: ///\n  1017: /// println!(\"{} cookies remain in the cookie jar!\", jar.cookies);\n  1018: /// ```\n  1019: #[lang = \"rem_assign\"]\n  1020: #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n  1021: #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n  1022: #[diagnostic::on_unimplemented(\n  1023:     message = \"cannot calculate and assign the remainder of `{Self}` divided by `{Rhs}`\",\n  1024:     label = \"no implementation for `{Self} %= {Rhs}`\"\n  1025: )]\n  1026: #[doc(alias = \"%\")]\n  1027: #[doc(alias = \"%=\")]\n  1028: pub const trait RemAssign<Rhs = Self> {\n  1029:     /// Performs the `%=` operation.\n  1030:     ///\n  1031:     /// # Example\n  1032:     ///\n  1033:     /// ```\n  1034:     /// let mut x: u32 = 12;\n  1035:     /// x %= 10;\n  1036:     /// assert_eq!(x, 2);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::Shl::shl",
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
      "name": "shl",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:5000",
        "kind": "trait",
        "name": "Shl",
        "path": [
          "core",
          "ops",
          "bit",
          "Shl"
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
              "id": 5000,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "   460: )]\n   461: pub const trait Shl<Rhs = Self> {\n   462:     /// The resulting type after applying the `<<` operator.\n   463:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   464:     type Output;\n   465: \n   466:     /// Performs the `<<` operation.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// assert_eq!(5u8 << 1, 10);\n   472:     /// assert_eq!(1u8 << 1, 2);\n   473:     /// ```\n   474:     #[must_use]\n   475:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   476:     fn shl(self, rhs: Rhs) -> Self::Output;\n   477: }\n   478: \n   479: macro_rules! shl_impl {\n   480:     ($t:ty, $f:ty) => {\n   481:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   482:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   483:         impl const Shl<$f> for $t {\n   484:             type Output = $t;\n   485: \n   486:             #[inline]\n   487:             #[track_caller]\n   488:             #[rustc_inherit_overflow_checks]\n   489:             fn shl(self, other: $f) -> $t {\n   490:                 self << other\n   491:             }\n   492:         }",
    "nanvix_source": "   466:     /// Performs the `<<` operation.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// assert_eq!(5u8 << 1, 10);\n   472:     /// assert_eq!(1u8 << 1, 2);\n   473:     /// ```\n   474:     #[must_use]\n   475:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   476:     fn shl(self, rhs: Rhs) -> Self::Output;\n   477: }\n   478: \n   479: macro_rules! shl_impl {\n   480:     ($t:ty, $f:ty) => {\n   481:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   482:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   483:         const impl Shl<$f> for $t {\n   484:             type Output = $t;\n   485: \n   486:             #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ShlAssign::shl_assign",
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
      "name": "shl_assign",
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
        "item_id": "core:5012",
        "kind": "trait",
        "name": "ShlAssign",
        "path": [
          "core",
          "ops",
          "bit",
          "ShlAssign"
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
    "verification_source": "   938: )]\n   939: pub const trait ShlAssign<Rhs = Self> {\n   940:     /// Performs the `<<=` operation.\n   941:     ///\n   942:     /// # Examples\n   943:     ///\n   944:     /// ```\n   945:     /// let mut x: u8 = 5;\n   946:     /// x <<= 1;\n   947:     /// assert_eq!(x, 10);\n   948:     ///\n   949:     /// let mut x: u8 = 1;\n   950:     /// x <<= 1;\n   951:     /// assert_eq!(x, 2);\n   952:     /// ```\n   953:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   954:     fn shl_assign(&mut self, rhs: Rhs);\n   955: }\n   956: \n   957: macro_rules! shl_assign_impl {\n   958:     ($t:ty, $f:ty) => {\n   959:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   960:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   961:         impl const ShlAssign<$f> for $t {\n   962:             #[inline]\n   963:             #[track_caller]\n   964:             #[rustc_inherit_overflow_checks]\n   965:             fn shl_assign(&mut self, other: $f) {\n   966:                 *self <<= other\n   967:             }\n   968:         }\n   969: \n   970:         forward_ref_op_assign! { impl ShlAssign, shl_assign for $t, $f,",
    "nanvix_source": "   944:     /// ```\n   945:     /// let mut x: u8 = 5;\n   946:     /// x <<= 1;\n   947:     /// assert_eq!(x, 10);\n   948:     ///\n   949:     /// let mut x: u8 = 1;\n   950:     /// x <<= 1;\n   951:     /// assert_eq!(x, 2);\n   952:     /// ```\n   953:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   954:     fn shl_assign(&mut self, rhs: Rhs);\n   955: }\n   956: \n   957: macro_rules! shl_assign_impl {\n   958:     ($t:ty, $f:ty) => {\n   959:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   960:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   961:         const impl ShlAssign<$f> for $t {\n   962:             #[inline]\n   963:             #[track_caller]\n   964:             #[rustc_inherit_overflow_checks]",
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
