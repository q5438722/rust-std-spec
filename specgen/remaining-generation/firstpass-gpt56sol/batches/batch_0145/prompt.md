For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::saturating_add",
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
      "name": "saturating_add",
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
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   687:     /// Saturating `Duration` addition. Computes `self + other`, returning [`Duration::MAX`]\n   688:     /// if overflow occurred.\n   689:     ///\n   690:     /// # Examples\n   691:     ///\n   692:     /// ```\n   693:     /// use std::time::Duration;\n   694:     ///\n   695:     /// assert_eq!(Duration::new(0, 0).saturating_add(Duration::new(0, 1)), Duration::new(0, 1));\n   696:     /// assert_eq!(Duration::new(1, 0).saturating_add(Duration::new(u64::MAX, 0)), Duration::MAX);\n   697:     /// ```\n   698:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   699:     #[must_use = \"this returns the result of the operation, \\\n   700:                   without modifying the original\"]\n   701:     #[inline]\n   702:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   703:     pub const fn saturating_add(self, rhs: Duration) -> Duration {\n   704:         match self.checked_add(rhs) {\n   705:             Some(res) => res,\n   706:             None => Duration::MAX,\n   707:         }\n   708:     }\n   709: \n   710:     /// Checked `Duration` subtraction. Computes `self - other`, returning [`None`]\n   711:     /// if the result would be negative or if overflow occurred.\n   712:     ///\n   713:     /// # Examples\n   714:     ///\n   715:     /// ```\n   716:     /// use std::time::Duration;\n   717:     ///\n   718:     /// assert_eq!(Duration::new(0, 1).checked_sub(Duration::new(0, 0)), Some(Duration::new(0, 1)));\n   719:     /// assert_eq!(Duration::new(0, 0).checked_sub(Duration::new(0, 1)), None);",
    "nanvix_source": "   693:     /// use std::time::Duration;\n   694:     ///\n   695:     /// assert_eq!(Duration::new(0, 0).saturating_add(Duration::new(0, 1)), Duration::new(0, 1));\n   696:     /// assert_eq!(Duration::new(1, 0).saturating_add(Duration::new(u64::MAX, 0)), Duration::MAX);\n   697:     /// ```\n   698:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   699:     #[must_use = \"this returns the result of the operation, \\\n   700:                   without modifying the original\"]\n   701:     #[inline]\n   702:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   703:     pub const fn saturating_add(self, rhs: Duration) -> Duration {\n   704:         match self.checked_add(rhs) {\n   705:             Some(res) => res,\n   706:             None => Duration::MAX,\n   707:         }\n   708:     }\n   709: \n   710:     /// Checked `Duration` subtraction. Computes `self - other`, returning [`None`]\n   711:     /// if the result would be negative or if overflow occurred.\n   712:     ///\n   713:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::saturating_mul",
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
      "name": "saturating_mul",
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
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   797:     /// Saturating `Duration` multiplication. Computes `self * other`, returning\n   798:     /// [`Duration::MAX`] if overflow occurred.\n   799:     ///\n   800:     /// # Examples\n   801:     ///\n   802:     /// ```\n   803:     /// use std::time::Duration;\n   804:     ///\n   805:     /// assert_eq!(Duration::new(0, 500_000_001).saturating_mul(2), Duration::new(1, 2));\n   806:     /// assert_eq!(Duration::new(u64::MAX - 1, 0).saturating_mul(2), Duration::MAX);\n   807:     /// ```\n   808:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   809:     #[must_use = \"this returns the result of the operation, \\\n   810:                   without modifying the original\"]\n   811:     #[inline]\n   812:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   813:     pub const fn saturating_mul(self, rhs: u32) -> Duration {\n   814:         match self.checked_mul(rhs) {\n   815:             Some(res) => res,\n   816:             None => Duration::MAX,\n   817:         }\n   818:     }\n   819: \n   820:     /// Checked `Duration` division. Computes `self / other`, returning [`None`]\n   821:     /// if `other == 0`.\n   822:     ///\n   823:     /// # Examples\n   824:     ///\n   825:     /// ```\n   826:     /// use std::time::Duration;\n   827:     ///\n   828:     /// assert_eq!(Duration::new(2, 0).checked_div(2), Some(Duration::new(1, 0)));\n   829:     /// assert_eq!(Duration::new(1, 0).checked_div(2), Some(Duration::new(0, 500_000_000)));",
    "nanvix_source": "   803:     /// use std::time::Duration;\n   804:     ///\n   805:     /// assert_eq!(Duration::new(0, 500_000_001).saturating_mul(2), Duration::new(1, 2));\n   806:     /// assert_eq!(Duration::new(u64::MAX - 1, 0).saturating_mul(2), Duration::MAX);\n   807:     /// ```\n   808:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   809:     #[must_use = \"this returns the result of the operation, \\\n   810:                   without modifying the original\"]\n   811:     #[inline]\n   812:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   813:     pub const fn saturating_mul(self, rhs: u32) -> Duration {\n   814:         match self.checked_mul(rhs) {\n   815:             Some(res) => res,\n   816:             None => Duration::MAX,\n   817:         }\n   818:     }\n   819: \n   820:     /// Checked `Duration` division. Computes `self / other`, returning [`None`]\n   821:     /// if `other == 0`.\n   822:     ///\n   823:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::saturating_sub",
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
      "name": "saturating_sub",
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
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   743:     /// Saturating `Duration` subtraction. Computes `self - other`, returning [`Duration::ZERO`]\n   744:     /// if the result would be negative or if overflow occurred.\n   745:     ///\n   746:     /// # Examples\n   747:     ///\n   748:     /// ```\n   749:     /// use std::time::Duration;\n   750:     ///\n   751:     /// assert_eq!(Duration::new(0, 1).saturating_sub(Duration::new(0, 0)), Duration::new(0, 1));\n   752:     /// assert_eq!(Duration::new(0, 0).saturating_sub(Duration::new(0, 1)), Duration::ZERO);\n   753:     /// ```\n   754:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   755:     #[must_use = \"this returns the result of the operation, \\\n   756:                   without modifying the original\"]\n   757:     #[inline]\n   758:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   759:     pub const fn saturating_sub(self, rhs: Duration) -> Duration {\n   760:         match self.checked_sub(rhs) {\n   761:             Some(res) => res,\n   762:             None => Duration::ZERO,\n   763:         }\n   764:     }\n   765: \n   766:     /// Checked `Duration` multiplication. Computes `self * other`, returning\n   767:     /// [`None`] if overflow occurred.\n   768:     ///\n   769:     /// # Examples\n   770:     ///\n   771:     /// ```\n   772:     /// use std::time::Duration;\n   773:     ///\n   774:     /// assert_eq!(Duration::new(0, 500_000_001).checked_mul(2), Some(Duration::new(1, 2)));\n   775:     /// assert_eq!(Duration::new(u64::MAX - 1, 0).checked_mul(2), None);",
    "nanvix_source": "   749:     /// use std::time::Duration;\n   750:     ///\n   751:     /// assert_eq!(Duration::new(0, 1).saturating_sub(Duration::new(0, 0)), Duration::new(0, 1));\n   752:     /// assert_eq!(Duration::new(0, 0).saturating_sub(Duration::new(0, 1)), Duration::ZERO);\n   753:     /// ```\n   754:     #[stable(feature = \"duration_saturating_ops\", since = \"1.53.0\")]\n   755:     #[must_use = \"this returns the result of the operation, \\\n   756:                   without modifying the original\"]\n   757:     #[inline]\n   758:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   759:     pub const fn saturating_sub(self, rhs: Duration) -> Duration {\n   760:         match self.checked_sub(rhs) {\n   761:             Some(res) => res,\n   762:             None => Duration::ZERO,\n   763:         }\n   764:     }\n   765: \n   766:     /// Checked `Duration` multiplication. Computes `self * other`, returning\n   767:     /// [`None`] if overflow occurred.\n   768:     ///\n   769:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::subsec_micros",
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
      "name": "subsec_micros",
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   536:     /// represented by microseconds. The returned number always represents a\n   537:     /// fractional portion of a second (i.e., it is less than one million).\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```\n   542:     /// use std::time::Duration;\n   543:     ///\n   544:     /// let duration = Duration::from_micros(1_234_567);\n   545:     /// assert_eq!(duration.as_secs(), 1);\n   546:     /// assert_eq!(duration.subsec_micros(), 234_567);\n   547:     /// ```\n   548:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   549:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   550:     #[must_use]\n   551:     #[inline]\n   552:     pub const fn subsec_micros(&self) -> u32 {\n   553:         self.nanos.as_inner() / NANOS_PER_MICRO\n   554:     }\n   555: \n   556:     /// Returns the fractional part of this `Duration`, in nanoseconds.\n   557:     ///\n   558:     /// This method does **not** return the length of the duration when\n   559:     /// represented by nanoseconds. The returned number always represents a\n   560:     /// fractional portion of a second (i.e., it is less than one billion).\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// use std::time::Duration;\n   566:     ///\n   567:     /// let duration = Duration::from_millis(5_010);\n   568:     /// assert_eq!(duration.as_secs(), 5);",
    "nanvix_source": "   542:     /// use std::time::Duration;\n   543:     ///\n   544:     /// let duration = Duration::from_micros(1_234_567);\n   545:     /// assert_eq!(duration.as_secs(), 1);\n   546:     /// assert_eq!(duration.subsec_micros(), 234_567);\n   547:     /// ```\n   548:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   549:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   550:     #[must_use]\n   551:     #[inline]\n   552:     pub const fn subsec_micros(&self) -> u32 {\n   553:         self.nanos.as_inner() / NANOS_PER_MICRO\n   554:     }\n   555: \n   556:     /// Returns the fractional part of this `Duration`, in nanoseconds.\n   557:     ///\n   558:     /// This method does **not** return the length of the duration when\n   559:     /// represented by nanoseconds. The returned number always represents a\n   560:     /// fractional portion of a second (i.e., it is less than one billion).\n   561:     ///\n   562:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::subsec_millis",
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
      "name": "subsec_millis",
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   513:     /// represented by milliseconds. The returned number always represents a\n   514:     /// fractional portion of a second (i.e., it is less than one thousand).\n   515:     ///\n   516:     /// # Examples\n   517:     ///\n   518:     /// ```\n   519:     /// use std::time::Duration;\n   520:     ///\n   521:     /// let duration = Duration::from_millis(5_432);\n   522:     /// assert_eq!(duration.as_secs(), 5);\n   523:     /// assert_eq!(duration.subsec_millis(), 432);\n   524:     /// ```\n   525:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   526:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   527:     #[must_use]\n   528:     #[inline]\n   529:     pub const fn subsec_millis(&self) -> u32 {\n   530:         self.nanos.as_inner() / NANOS_PER_MILLI\n   531:     }\n   532: \n   533:     /// Returns the fractional part of this `Duration`, in whole microseconds.\n   534:     ///\n   535:     /// This method does **not** return the length of the duration when\n   536:     /// represented by microseconds. The returned number always represents a\n   537:     /// fractional portion of a second (i.e., it is less than one million).\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```\n   542:     /// use std::time::Duration;\n   543:     ///\n   544:     /// let duration = Duration::from_micros(1_234_567);\n   545:     /// assert_eq!(duration.as_secs(), 1);",
    "nanvix_source": "   519:     /// use std::time::Duration;\n   520:     ///\n   521:     /// let duration = Duration::from_millis(5_432);\n   522:     /// assert_eq!(duration.as_secs(), 5);\n   523:     /// assert_eq!(duration.subsec_millis(), 432);\n   524:     /// ```\n   525:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   526:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   527:     #[must_use]\n   528:     #[inline]\n   529:     pub const fn subsec_millis(&self) -> u32 {\n   530:         self.nanos.as_inner() / NANOS_PER_MILLI\n   531:     }\n   532: \n   533:     /// Returns the fractional part of this `Duration`, in whole microseconds.\n   534:     ///\n   535:     /// This method does **not** return the length of the duration when\n   536:     /// represented by microseconds. The returned number always represents a\n   537:     /// fractional portion of a second (i.e., it is less than one million).\n   538:     ///\n   539:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::subsec_nanos",
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
      "name": "subsec_nanos",
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   559:     /// represented by nanoseconds. The returned number always represents a\n   560:     /// fractional portion of a second (i.e., it is less than one billion).\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// use std::time::Duration;\n   566:     ///\n   567:     /// let duration = Duration::from_millis(5_010);\n   568:     /// assert_eq!(duration.as_secs(), 5);\n   569:     /// assert_eq!(duration.subsec_nanos(), 10_000_000);\n   570:     /// ```\n   571:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   572:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   573:     #[must_use]\n   574:     #[inline]\n   575:     pub const fn subsec_nanos(&self) -> u32 {\n   576:         self.nanos.as_inner()\n   577:     }\n   578: \n   579:     /// Returns the total number of whole milliseconds contained by this `Duration`.\n   580:     ///\n   581:     /// # Examples\n   582:     ///\n   583:     /// ```\n   584:     /// use std::time::Duration;\n   585:     ///\n   586:     /// let duration = Duration::new(5, 730_023_852);\n   587:     /// assert_eq!(duration.as_millis(), 5_730);\n   588:     /// ```\n   589:     #[stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   590:     #[rustc_const_stable(feature = \"duration_as_u128\", since = \"1.33.0\")]\n   591:     #[must_use]",
    "nanvix_source": "   565:     /// use std::time::Duration;\n   566:     ///\n   567:     /// let duration = Duration::from_millis(5_010);\n   568:     /// assert_eq!(duration.as_secs(), 5);\n   569:     /// assert_eq!(duration.subsec_nanos(), 10_000_000);\n   570:     /// ```\n   571:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   572:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   573:     #[must_use]\n   574:     #[inline]\n   575:     pub const fn subsec_nanos(&self) -> u32 {\n   576:         self.nanos.as_inner()\n   577:     }\n   578: \n   579:     /// Returns the total number of whole milliseconds contained by this `Duration`.\n   580:     ///\n   581:     /// # Examples\n   582:     ///\n   583:     /// ```\n   584:     /// use std::time::Duration;\n   585:     ///",
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
