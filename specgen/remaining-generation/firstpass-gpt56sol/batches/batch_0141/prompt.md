For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::as_secs",
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
      "name": "as_secs",
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   490:     /// use std::time::Duration;\n   491:     ///\n   492:     /// let duration = Duration::new(5, 730_023_852);\n   493:     /// assert_eq!(duration.as_secs(), 5);\n   494:     /// ```\n   495:     ///\n   496:     /// To determine the total number of seconds represented by the `Duration`\n   497:     /// including the fractional part, use [`as_secs_f64`] or [`as_secs_f32`]\n   498:     ///\n   499:     /// [`as_secs_f64`]: Duration::as_secs_f64\n   500:     /// [`as_secs_f32`]: Duration::as_secs_f32\n   501:     /// [`subsec_nanos`]: Duration::subsec_nanos\n   502:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   503:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   504:     #[must_use]\n   505:     #[inline]\n   506:     pub const fn as_secs(&self) -> u64 {\n   507:         self.secs\n   508:     }\n   509: \n   510:     /// Returns the fractional part of this `Duration`, in whole milliseconds.\n   511:     ///\n   512:     /// This method does **not** return the length of the duration when\n   513:     /// represented by milliseconds. The returned number always represents a\n   514:     /// fractional portion of a second (i.e., it is less than one thousand).\n   515:     ///\n   516:     /// # Examples\n   517:     ///\n   518:     /// ```\n   519:     /// use std::time::Duration;\n   520:     ///\n   521:     /// let duration = Duration::from_millis(5_432);\n   522:     /// assert_eq!(duration.as_secs(), 5);",
    "nanvix_source": "   496:     /// To determine the total number of seconds represented by the `Duration`\n   497:     /// including the fractional part, use [`as_secs_f64`] or [`as_secs_f32`]\n   498:     ///\n   499:     /// [`as_secs_f64`]: Duration::as_secs_f64\n   500:     /// [`as_secs_f32`]: Duration::as_secs_f32\n   501:     /// [`subsec_nanos`]: Duration::subsec_nanos\n   502:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   503:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   504:     #[must_use]\n   505:     #[inline]\n   506:     pub const fn as_secs(&self) -> u64 {\n   507:         self.secs\n   508:     }\n   509: \n   510:     /// Returns the fractional part of this `Duration`, in whole milliseconds.\n   511:     ///\n   512:     /// This method does **not** return the length of the duration when\n   513:     /// represented by milliseconds. The returned number always represents a\n   514:     /// fractional portion of a second (i.e., it is less than one thousand).\n   515:     ///\n   516:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::as_secs_f32",
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
      "name": "as_secs_f32",
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
          "primitive": "f32"
        }
      }
    },
    "verification_source": "   869: \n   870:     /// Returns the number of seconds contained by this `Duration` as `f32`.\n   871:     ///\n   872:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   873:     ///\n   874:     /// # Examples\n   875:     /// ```\n   876:     /// use std::time::Duration;\n   877:     ///\n   878:     /// let dur = Duration::new(2, 700_000_000);\n   879:     /// assert_eq!(dur.as_secs_f32(), 2.7);\n   880:     /// ```\n   881:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   882:     #[must_use]\n   883:     #[inline]\n   884:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n   885:     pub const fn as_secs_f32(&self) -> f32 {\n   886:         (self.secs as f32) + (self.nanos.as_inner() as f32) / (NANOS_PER_SEC as f32)\n   887:     }\n   888: \n   889:     /// Returns the number of milliseconds contained by this `Duration` as `f64`.\n   890:     ///\n   891:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   892:     ///\n   893:     /// # Examples\n   894:     /// ```\n   895:     /// #![feature(duration_millis_float)]\n   896:     /// use std::time::Duration;\n   897:     ///\n   898:     /// let dur = Duration::new(2, 345_678_000);\n   899:     /// assert_eq!(dur.as_millis_f64(), 2_345.678);\n   900:     /// ```\n   901:     #[unstable(feature = \"duration_millis_float\", issue = \"122451\")]",
    "nanvix_source": "   875:     /// ```\n   876:     /// use std::time::Duration;\n   877:     ///\n   878:     /// let dur = Duration::new(2, 700_000_000);\n   879:     /// assert_eq!(dur.as_secs_f32(), 2.7);\n   880:     /// ```\n   881:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   882:     #[must_use]\n   883:     #[inline]\n   884:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n   885:     pub const fn as_secs_f32(&self) -> f32 {\n   886:         (self.secs as f32) + (self.nanos.as_inner() as f32) / (NANOS_PER_SEC as f32)\n   887:     }\n   888: \n   889:     /// Returns the number of milliseconds contained by this `Duration` as `f64`.\n   890:     ///\n   891:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   892:     ///\n   893:     /// # Examples\n   894:     /// ```\n   895:     /// #![feature(duration_millis_float)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::as_secs_f64",
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
      "name": "as_secs_f64",
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
          "primitive": "f64"
        }
      }
    },
    "verification_source": "   850: \n   851:     /// Returns the number of seconds contained by this `Duration` as `f64`.\n   852:     ///\n   853:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   854:     ///\n   855:     /// # Examples\n   856:     /// ```\n   857:     /// use std::time::Duration;\n   858:     ///\n   859:     /// let dur = Duration::new(2, 700_000_000);\n   860:     /// assert_eq!(dur.as_secs_f64(), 2.7);\n   861:     /// ```\n   862:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   863:     #[must_use]\n   864:     #[inline]\n   865:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n   866:     pub const fn as_secs_f64(&self) -> f64 {\n   867:         (self.secs as f64) + (self.nanos.as_inner() as f64) / (NANOS_PER_SEC as f64)\n   868:     }\n   869: \n   870:     /// Returns the number of seconds contained by this `Duration` as `f32`.\n   871:     ///\n   872:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   873:     ///\n   874:     /// # Examples\n   875:     /// ```\n   876:     /// use std::time::Duration;\n   877:     ///\n   878:     /// let dur = Duration::new(2, 700_000_000);\n   879:     /// assert_eq!(dur.as_secs_f32(), 2.7);\n   880:     /// ```\n   881:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   882:     #[must_use]",
    "nanvix_source": "   856:     /// ```\n   857:     /// use std::time::Duration;\n   858:     ///\n   859:     /// let dur = Duration::new(2, 700_000_000);\n   860:     /// assert_eq!(dur.as_secs_f64(), 2.7);\n   861:     /// ```\n   862:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n   863:     #[must_use]\n   864:     #[inline]\n   865:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n   866:     pub const fn as_secs_f64(&self) -> f64 {\n   867:         (self.secs as f64) + (self.nanos.as_inner() as f64) / (NANOS_PER_SEC as f64)\n   868:     }\n   869: \n   870:     /// Returns the number of seconds contained by this `Duration` as `f32`.\n   871:     ///\n   872:     /// The returned value includes the fractional (nanosecond) part of the duration.\n   873:     ///\n   874:     /// # Examples\n   875:     /// ```\n   876:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::checked_add",
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
      "name": "checked_add",
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
    "verification_source": "   654:     /// Checked `Duration` addition. Computes `self + other`, returning [`None`]\n   655:     /// if overflow occurred.\n   656:     ///\n   657:     /// # Examples\n   658:     ///\n   659:     /// ```\n   660:     /// use std::time::Duration;\n   661:     ///\n   662:     /// assert_eq!(Duration::new(0, 0).checked_add(Duration::new(0, 1)), Some(Duration::new(0, 1)));\n   663:     /// assert_eq!(Duration::new(1, 0).checked_add(Duration::new(u64::MAX, 0)), None);\n   664:     /// ```\n   665:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   666:     #[must_use = \"this returns the result of the operation, \\\n   667:                   without modifying the original\"]\n   668:     #[inline]\n   669:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   670:     pub const fn checked_add(self, rhs: Duration) -> Option<Duration> {\n   671:         if let Some(mut secs) = self.secs.checked_add(rhs.secs) {\n   672:             let mut nanos = self.nanos.as_inner() + rhs.nanos.as_inner();\n   673:             if nanos >= NANOS_PER_SEC {\n   674:                 nanos -= NANOS_PER_SEC;\n   675:                 let Some(new_secs) = secs.checked_add(1) else {\n   676:                     return None;\n   677:                 };\n   678:                 secs = new_secs;\n   679:             }\n   680:             debug_assert!(nanos < NANOS_PER_SEC);\n   681:             Some(Duration::new(secs, nanos))\n   682:         } else {\n   683:             None\n   684:         }\n   685:     }\n   686: ",
    "nanvix_source": "   660:     /// use std::time::Duration;\n   661:     ///\n   662:     /// assert_eq!(Duration::new(0, 0).checked_add(Duration::new(0, 1)), Some(Duration::new(0, 1)));\n   663:     /// assert_eq!(Duration::new(1, 0).checked_add(Duration::new(u64::MAX, 0)), None);\n   664:     /// ```\n   665:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   666:     #[must_use = \"this returns the result of the operation, \\\n   667:                   without modifying the original\"]\n   668:     #[inline]\n   669:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   670:     pub const fn checked_add(self, rhs: Duration) -> Option<Duration> {\n   671:         if let Some(mut secs) = self.secs.checked_add(rhs.secs) {\n   672:             let mut nanos = self.nanos.as_inner() + rhs.nanos.as_inner();\n   673:             if nanos >= NANOS_PER_SEC {\n   674:                 nanos -= NANOS_PER_SEC;\n   675:                 let Some(new_secs) = secs.checked_add(1) else {\n   676:                     return None;\n   677:                 };\n   678:                 secs = new_secs;\n   679:             }\n   680:             debug_assert!(nanos < NANOS_PER_SEC);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::checked_div",
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
      "name": "checked_div",
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
              "primitive": "u32"
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
    "verification_source": "   821:     /// if `other == 0`.\n   822:     ///\n   823:     /// # Examples\n   824:     ///\n   825:     /// ```\n   826:     /// use std::time::Duration;\n   827:     ///\n   828:     /// assert_eq!(Duration::new(2, 0).checked_div(2), Some(Duration::new(1, 0)));\n   829:     /// assert_eq!(Duration::new(1, 0).checked_div(2), Some(Duration::new(0, 500_000_000)));\n   830:     /// assert_eq!(Duration::new(2, 0).checked_div(0), None);\n   831:     /// ```\n   832:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   833:     #[must_use = \"this returns the result of the operation, \\\n   834:                   without modifying the original\"]\n   835:     #[inline]\n   836:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   837:     pub const fn checked_div(self, rhs: u32) -> Option<Duration> {\n   838:         if rhs != 0 {\n   839:             let (secs, extra_secs) = (self.secs / (rhs as u64), self.secs % (rhs as u64));\n   840:             let (mut nanos, extra_nanos) =\n   841:                 (self.nanos.as_inner() / rhs, self.nanos.as_inner() % rhs);\n   842:             nanos +=\n   843:                 ((extra_secs * (NANOS_PER_SEC as u64) + extra_nanos as u64) / (rhs as u64)) as u32;\n   844:             debug_assert!(nanos < NANOS_PER_SEC);\n   845:             Some(Duration::new(secs, nanos))\n   846:         } else {\n   847:             None\n   848:         }\n   849:     }\n   850: \n   851:     /// Returns the number of seconds contained by this `Duration` as `f64`.\n   852:     ///\n   853:     /// The returned value includes the fractional (nanosecond) part of the duration.",
    "nanvix_source": "   827:     ///\n   828:     /// assert_eq!(Duration::new(2, 0).checked_div(2), Some(Duration::new(1, 0)));\n   829:     /// assert_eq!(Duration::new(1, 0).checked_div(2), Some(Duration::new(0, 500_000_000)));\n   830:     /// assert_eq!(Duration::new(2, 0).checked_div(0), None);\n   831:     /// ```\n   832:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   833:     #[must_use = \"this returns the result of the operation, \\\n   834:                   without modifying the original\"]\n   835:     #[inline]\n   836:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   837:     pub const fn checked_div(self, rhs: u32) -> Option<Duration> {\n   838:         if rhs != 0 {\n   839:             let (secs, extra_secs) = (self.secs / (rhs as u64), self.secs % (rhs as u64));\n   840:             let (mut nanos, extra_nanos) =\n   841:                 (self.nanos.as_inner() / rhs, self.nanos.as_inner() % rhs);\n   842:             nanos +=\n   843:                 ((extra_secs * (NANOS_PER_SEC as u64) + extra_nanos as u64) / (rhs as u64)) as u32;\n   844:             debug_assert!(nanos < NANOS_PER_SEC);\n   845:             Some(Duration::new(secs, nanos))\n   846:         } else {\n   847:             None",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::checked_mul",
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
      "name": "checked_mul",
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
              "primitive": "u32"
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
    "verification_source": "   766:     /// Checked `Duration` multiplication. Computes `self * other`, returning\n   767:     /// [`None`] if overflow occurred.\n   768:     ///\n   769:     /// # Examples\n   770:     ///\n   771:     /// ```\n   772:     /// use std::time::Duration;\n   773:     ///\n   774:     /// assert_eq!(Duration::new(0, 500_000_001).checked_mul(2), Some(Duration::new(1, 2)));\n   775:     /// assert_eq!(Duration::new(u64::MAX - 1, 0).checked_mul(2), None);\n   776:     /// ```\n   777:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   778:     #[must_use = \"this returns the result of the operation, \\\n   779:                   without modifying the original\"]\n   780:     #[inline]\n   781:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   782:     pub const fn checked_mul(self, rhs: u32) -> Option<Duration> {\n   783:         // Multiply nanoseconds as u64, because it cannot overflow that way.\n   784:         let total_nanos = self.nanos.as_inner() as u64 * rhs as u64;\n   785:         let extra_secs = total_nanos / (NANOS_PER_SEC as u64);\n   786:         let nanos = (total_nanos % (NANOS_PER_SEC as u64)) as u32;\n   787:         // FIXME(const-hack): use `and_then` once that is possible.\n   788:         if let Some(s) = self.secs.checked_mul(rhs as u64) {\n   789:             if let Some(secs) = s.checked_add(extra_secs) {\n   790:                 debug_assert!(nanos < NANOS_PER_SEC);\n   791:                 return Some(Duration::new(secs, nanos));\n   792:             }\n   793:         }\n   794:         None\n   795:     }\n   796: \n   797:     /// Saturating `Duration` multiplication. Computes `self * other`, returning\n   798:     /// [`Duration::MAX`] if overflow occurred.",
    "nanvix_source": "   772:     /// use std::time::Duration;\n   773:     ///\n   774:     /// assert_eq!(Duration::new(0, 500_000_001).checked_mul(2), Some(Duration::new(1, 2)));\n   775:     /// assert_eq!(Duration::new(u64::MAX - 1, 0).checked_mul(2), None);\n   776:     /// ```\n   777:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   778:     #[must_use = \"this returns the result of the operation, \\\n   779:                   without modifying the original\"]\n   780:     #[inline]\n   781:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   782:     pub const fn checked_mul(self, rhs: u32) -> Option<Duration> {\n   783:         // Multiply nanoseconds as u64, because it cannot overflow that way.\n   784:         let total_nanos = self.nanos.as_inner() as u64 * rhs as u64;\n   785:         let extra_secs = total_nanos / (NANOS_PER_SEC as u64);\n   786:         let nanos = (total_nanos % (NANOS_PER_SEC as u64)) as u32;\n   787:         // FIXME(const-hack): use `and_then` once that is possible.\n   788:         if let Some(s) = self.secs.checked_mul(rhs as u64) {\n   789:             if let Some(secs) = s.checked_add(extra_secs) {\n   790:                 debug_assert!(nanos < NANOS_PER_SEC);\n   791:                 return Some(Duration::new(secs, nanos));\n   792:             }",
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
