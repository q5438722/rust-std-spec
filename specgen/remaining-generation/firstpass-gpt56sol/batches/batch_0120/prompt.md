For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cmp::Ordering::is_gt",
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
      "name": "is_gt",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   483: \n   484:     /// Returns `true` if the ordering is the `Greater` variant.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::cmp::Ordering;\n   490:     ///\n   491:     /// assert_eq!(Ordering::Less.is_gt(), false);\n   492:     /// assert_eq!(Ordering::Equal.is_gt(), false);\n   493:     /// assert_eq!(Ordering::Greater.is_gt(), true);\n   494:     /// ```\n   495:     #[inline]\n   496:     #[must_use]\n   497:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   498:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   499:     pub const fn is_gt(self) -> bool {\n   500:         self.as_raw() > 0\n   501:     }\n   502: \n   503:     /// Returns `true` if the ordering is either the `Less` or `Equal` variant.\n   504:     ///\n   505:     /// # Examples\n   506:     ///\n   507:     /// ```\n   508:     /// use std::cmp::Ordering;\n   509:     ///\n   510:     /// assert_eq!(Ordering::Less.is_le(), true);\n   511:     /// assert_eq!(Ordering::Equal.is_le(), true);\n   512:     /// assert_eq!(Ordering::Greater.is_le(), false);\n   513:     /// ```\n   514:     #[inline]\n   515:     #[must_use]",
    "nanvix_source": "   490:     /// use std::cmp::Ordering;\n   491:     ///\n   492:     /// assert_eq!(Ordering::Less.is_gt(), false);\n   493:     /// assert_eq!(Ordering::Equal.is_gt(), false);\n   494:     /// assert_eq!(Ordering::Greater.is_gt(), true);\n   495:     /// ```\n   496:     #[inline]\n   497:     #[must_use]\n   498:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   499:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   500:     pub const fn is_gt(self) -> bool {\n   501:         self.as_raw() > 0\n   502:     }\n   503: \n   504:     /// Returns `true` if the ordering is either the `Less` or `Equal` variant.\n   505:     ///\n   506:     /// # Examples\n   507:     ///\n   508:     /// ```\n   509:     /// use std::cmp::Ordering;\n   510:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::is_le",
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
      "name": "is_le",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   502: \n   503:     /// Returns `true` if the ordering is either the `Less` or `Equal` variant.\n   504:     ///\n   505:     /// # Examples\n   506:     ///\n   507:     /// ```\n   508:     /// use std::cmp::Ordering;\n   509:     ///\n   510:     /// assert_eq!(Ordering::Less.is_le(), true);\n   511:     /// assert_eq!(Ordering::Equal.is_le(), true);\n   512:     /// assert_eq!(Ordering::Greater.is_le(), false);\n   513:     /// ```\n   514:     #[inline]\n   515:     #[must_use]\n   516:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   517:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   518:     pub const fn is_le(self) -> bool {\n   519:         self.as_raw() <= 0\n   520:     }\n   521: \n   522:     /// Returns `true` if the ordering is either the `Greater` or `Equal` variant.\n   523:     ///\n   524:     /// # Examples\n   525:     ///\n   526:     /// ```\n   527:     /// use std::cmp::Ordering;\n   528:     ///\n   529:     /// assert_eq!(Ordering::Less.is_ge(), false);\n   530:     /// assert_eq!(Ordering::Equal.is_ge(), true);\n   531:     /// assert_eq!(Ordering::Greater.is_ge(), true);\n   532:     /// ```\n   533:     #[inline]\n   534:     #[must_use]",
    "nanvix_source": "   509:     /// use std::cmp::Ordering;\n   510:     ///\n   511:     /// assert_eq!(Ordering::Less.is_le(), true);\n   512:     /// assert_eq!(Ordering::Equal.is_le(), true);\n   513:     /// assert_eq!(Ordering::Greater.is_le(), false);\n   514:     /// ```\n   515:     #[inline]\n   516:     #[must_use]\n   517:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   518:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   519:     pub const fn is_le(self) -> bool {\n   520:         self.as_raw() <= 0\n   521:     }\n   522: \n   523:     /// Returns `true` if the ordering is either the `Greater` or `Equal` variant.\n   524:     ///\n   525:     /// # Examples\n   526:     ///\n   527:     /// ```\n   528:     /// use std::cmp::Ordering;\n   529:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::is_lt",
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
      "name": "is_lt",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   464: \n   465:     /// Returns `true` if the ordering is the `Less` variant.\n   466:     ///\n   467:     /// # Examples\n   468:     ///\n   469:     /// ```\n   470:     /// use std::cmp::Ordering;\n   471:     ///\n   472:     /// assert_eq!(Ordering::Less.is_lt(), true);\n   473:     /// assert_eq!(Ordering::Equal.is_lt(), false);\n   474:     /// assert_eq!(Ordering::Greater.is_lt(), false);\n   475:     /// ```\n   476:     #[inline]\n   477:     #[must_use]\n   478:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   479:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   480:     pub const fn is_lt(self) -> bool {\n   481:         self.as_raw() < 0\n   482:     }\n   483: \n   484:     /// Returns `true` if the ordering is the `Greater` variant.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::cmp::Ordering;\n   490:     ///\n   491:     /// assert_eq!(Ordering::Less.is_gt(), false);\n   492:     /// assert_eq!(Ordering::Equal.is_gt(), false);\n   493:     /// assert_eq!(Ordering::Greater.is_gt(), true);\n   494:     /// ```\n   495:     #[inline]\n   496:     #[must_use]",
    "nanvix_source": "   471:     /// use std::cmp::Ordering;\n   472:     ///\n   473:     /// assert_eq!(Ordering::Less.is_lt(), true);\n   474:     /// assert_eq!(Ordering::Equal.is_lt(), false);\n   475:     /// assert_eq!(Ordering::Greater.is_lt(), false);\n   476:     /// ```\n   477:     #[inline]\n   478:     #[must_use]\n   479:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   480:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   481:     pub const fn is_lt(self) -> bool {\n   482:         self.as_raw() < 0\n   483:     }\n   484: \n   485:     /// Returns `true` if the ordering is the `Greater` variant.\n   486:     ///\n   487:     /// # Examples\n   488:     ///\n   489:     /// ```\n   490:     /// use std::cmp::Ordering;\n   491:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::is_ne",
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
      "name": "is_ne",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   445: \n   446:     /// Returns `true` if the ordering is not the `Equal` variant.\n   447:     ///\n   448:     /// # Examples\n   449:     ///\n   450:     /// ```\n   451:     /// use std::cmp::Ordering;\n   452:     ///\n   453:     /// assert_eq!(Ordering::Less.is_ne(), true);\n   454:     /// assert_eq!(Ordering::Equal.is_ne(), false);\n   455:     /// assert_eq!(Ordering::Greater.is_ne(), true);\n   456:     /// ```\n   457:     #[inline]\n   458:     #[must_use]\n   459:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   460:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   461:     pub const fn is_ne(self) -> bool {\n   462:         self.as_raw() != 0\n   463:     }\n   464: \n   465:     /// Returns `true` if the ordering is the `Less` variant.\n   466:     ///\n   467:     /// # Examples\n   468:     ///\n   469:     /// ```\n   470:     /// use std::cmp::Ordering;\n   471:     ///\n   472:     /// assert_eq!(Ordering::Less.is_lt(), true);\n   473:     /// assert_eq!(Ordering::Equal.is_lt(), false);\n   474:     /// assert_eq!(Ordering::Greater.is_lt(), false);\n   475:     /// ```\n   476:     #[inline]\n   477:     #[must_use]",
    "nanvix_source": "   452:     /// use std::cmp::Ordering;\n   453:     ///\n   454:     /// assert_eq!(Ordering::Less.is_ne(), true);\n   455:     /// assert_eq!(Ordering::Equal.is_ne(), false);\n   456:     /// assert_eq!(Ordering::Greater.is_ne(), true);\n   457:     /// ```\n   458:     #[inline]\n   459:     #[must_use]\n   460:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   461:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   462:     pub const fn is_ne(self) -> bool {\n   463:         self.as_raw() != 0\n   464:     }\n   465: \n   466:     /// Returns `true` if the ordering is the `Less` variant.\n   467:     ///\n   468:     /// # Examples\n   469:     ///\n   470:     /// ```\n   471:     /// use std::cmp::Ordering;\n   472:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::reverse",
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
      "name": "reverse",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        }
      }
    },
    "verification_source": "   558:     ///\n   559:     /// This method can be used to reverse a comparison:\n   560:     ///\n   561:     /// ```\n   562:     /// let data: &mut [_] = &mut [2, 10, 5, 8];\n   563:     ///\n   564:     /// // sort the array from largest to smallest.\n   565:     /// data.sort_by(|a, b| a.cmp(b).reverse());\n   566:     ///\n   567:     /// let b: &mut [_] = &mut [10, 8, 5, 2];\n   568:     /// assert!(data == b);\n   569:     /// ```\n   570:     #[inline]\n   571:     #[must_use]\n   572:     #[rustc_const_stable(feature = \"const_ordering\", since = \"1.48.0\")]\n   573:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   574:     pub const fn reverse(self) -> Ordering {\n   575:         match self {\n   576:             Less => Greater,\n   577:             Equal => Equal,\n   578:             Greater => Less,\n   579:         }\n   580:     }\n   581: \n   582:     /// Chains two orderings.\n   583:     ///\n   584:     /// Returns `self` when it's not `Equal`. Otherwise returns `other`.\n   585:     ///\n   586:     /// # Examples\n   587:     ///\n   588:     /// ```\n   589:     /// use std::cmp::Ordering;\n   590:     ///",
    "nanvix_source": "   565:     /// // sort the array from largest to smallest.\n   566:     /// data.sort_by(|a, b| a.cmp(b).reverse());\n   567:     ///\n   568:     /// let b: &mut [_] = &mut [10, 8, 5, 2];\n   569:     /// assert!(data == b);\n   570:     /// ```\n   571:     #[inline]\n   572:     #[must_use]\n   573:     #[rustc_const_stable(feature = \"const_ordering\", since = \"1.48.0\")]\n   574:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   575:     pub const fn reverse(self) -> Ordering {\n   576:         match self {\n   577:             Less => Greater,\n   578:             Equal => Equal,\n   579:             Greater => Less,\n   580:         }\n   581:     }\n   582: \n   583:     /// Chains two orderings.\n   584:     ///\n   585:     /// Returns `self` when it's not `Equal`. Otherwise returns `other`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::then",
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
      "name": "then",
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
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
                "id": 1682,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        }
      }
    },
    "verification_source": "   597:     /// let result = Ordering::Less.then(Ordering::Greater);\n   598:     /// assert_eq!(result, Ordering::Less);\n   599:     ///\n   600:     /// let result = Ordering::Equal.then(Ordering::Equal);\n   601:     /// assert_eq!(result, Ordering::Equal);\n   602:     ///\n   603:     /// let x: (i64, i64, i64) = (1, 2, 7);\n   604:     /// let y: (i64, i64, i64) = (1, 5, 3);\n   605:     /// let result = x.0.cmp(&y.0).then(x.1.cmp(&y.1)).then(x.2.cmp(&y.2));\n   606:     ///\n   607:     /// assert_eq!(result, Ordering::Less);\n   608:     /// ```\n   609:     #[inline]\n   610:     #[must_use]\n   611:     #[rustc_const_stable(feature = \"const_ordering\", since = \"1.48.0\")]\n   612:     #[stable(feature = \"ordering_chaining\", since = \"1.17.0\")]\n   613:     pub const fn then(self, other: Ordering) -> Ordering {\n   614:         match self {\n   615:             Equal => other,\n   616:             _ => self,\n   617:         }\n   618:     }\n   619: \n   620:     /// Chains the ordering with the given function.\n   621:     ///\n   622:     /// Returns `self` when it's not `Equal`. Otherwise calls `f` and returns\n   623:     /// the result.\n   624:     ///\n   625:     /// # Examples\n   626:     ///\n   627:     /// ```\n   628:     /// use std::cmp::Ordering;\n   629:     ///",
    "nanvix_source": "   604:     /// let x: (i64, i64, i64) = (1, 2, 7);\n   605:     /// let y: (i64, i64, i64) = (1, 5, 3);\n   606:     /// let result = x.0.cmp(&y.0).then(x.1.cmp(&y.1)).then(x.2.cmp(&y.2));\n   607:     ///\n   608:     /// assert_eq!(result, Ordering::Less);\n   609:     /// ```\n   610:     #[inline]\n   611:     #[must_use]\n   612:     #[rustc_const_stable(feature = \"const_ordering\", since = \"1.48.0\")]\n   613:     #[stable(feature = \"ordering_chaining\", since = \"1.17.0\")]\n   614:     pub const fn then(self, other: Ordering) -> Ordering {\n   615:         match self {\n   616:             Equal => other,\n   617:             _ => self,\n   618:         }\n   619:     }\n   620: \n   621:     /// Chains the ordering with the given function.\n   622:     ///\n   623:     /// Returns `self` when it's not `Equal`. Otherwise calls `f` and returns\n   624:     /// the result.",
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
