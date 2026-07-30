For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::from_utf8_unchecked_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function",
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
        "is_unsafe": true
      },
      "name": "from_utf8_unchecked_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   325:     ///\n   326:     /// # Examples\n   327:     ///\n   328:     /// Basic usage:\n   329:     ///\n   330:     /// ```\n   331:     /// let mut heart = vec![240, 159, 146, 150];\n   332:     /// let heart = unsafe { str::from_utf8_unchecked_mut(&mut heart) };\n   333:     ///\n   334:     /// assert_eq!(\"\ud83d\udc96\", heart);\n   335:     /// ```\n   336:     #[inline]\n   337:     #[must_use]\n   338:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   339:     #[rustc_const_stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   340:     #[rustc_diagnostic_item = \"str_inherent_from_utf8_unchecked_mut\"]\n   341:     pub const unsafe fn from_utf8_unchecked_mut(v: &mut [u8]) -> &mut str {\n   342:         // SAFETY: converts::from_utf8_unchecked_mut has the same safety requirements as this function.\n   343:         unsafe { converts::from_utf8_unchecked_mut(v) }\n   344:     }\n   345: \n   346:     /// Checks that `index`-th byte is the first byte in a UTF-8 code point\n   347:     /// sequence or the end of the string.\n   348:     ///\n   349:     /// The start and end of the string (when `index == self.len()`) are\n   350:     /// considered to be boundaries.\n   351:     ///\n   352:     /// Returns `false` if `index` is greater than `self.len()`.\n   353:     ///\n   354:     /// # Examples\n   355:     ///\n   356:     /// ```\n   357:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";",
    "nanvix_source": "   332:     /// let mut heart = vec![240, 159, 146, 150];\n   333:     /// let heart = unsafe { str::from_utf8_unchecked_mut(&mut heart) };\n   334:     ///\n   335:     /// assert_eq!(\"\ud83d\udc96\", heart);\n   336:     /// ```\n   337:     #[inline]\n   338:     #[must_use]\n   339:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   340:     #[rustc_const_stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   341:     #[rustc_diagnostic_item = \"str_inherent_from_utf8_unchecked_mut\"]\n   342:     pub const unsafe fn from_utf8_unchecked_mut(v: &mut [u8]) -> &mut str {\n   343:         // SAFETY: converts::from_utf8_unchecked_mut has the same safety requirements as this function.\n   344:         unsafe { converts::from_utf8_unchecked_mut(v) }\n   345:     }\n   346: \n   347:     /// Checks that `index`-th byte is the first byte in a UTF-8 code point\n   348:     /// sequence or the end of the string.\n   349:     ///\n   350:     /// The start and end of the string (when `index == self.len()`) are\n   351:     /// considered to be boundaries.\n   352:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
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
                      "modifier": "maybe_const",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "primitive": "str"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9549,
                        "path": "SliceIndex"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "i",
            {
              "generic": "I"
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
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Output",
                            "self_type": {
                              "generic": "I"
                            },
                            "trait": {
                              "args": null,
                              "id": 9549,
                              "path": ""
                            }
                          }
                        }
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
    "verification_source": "   635:     /// assert_eq!(Some(\"he\"), v.get_mut(0..2).map(|v| &*v));\n   636:     ///\n   637:     /// assert_eq!(\"hello\", v);\n   638:     /// {\n   639:     ///     let s = v.get_mut(0..2);\n   640:     ///     let s = s.map(|s| {\n   641:     ///         s.make_ascii_uppercase();\n   642:     ///         &*s\n   643:     ///     });\n   644:     ///     assert_eq!(Some(\"HE\"), s);\n   645:     /// }\n   646:     /// assert_eq!(\"HEllo\", v);\n   647:     /// ```\n   648:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   649:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   650:     #[inline]\n   651:     pub const fn get_mut<I: [const] SliceIndex<str>>(&mut self, i: I) -> Option<&mut I::Output> {\n   652:         i.get_mut(self)\n   653:     }\n   654: \n   655:     /// Returns an unchecked subslice of `str`.\n   656:     ///\n   657:     /// This is the unchecked alternative to indexing the `str`.\n   658:     ///\n   659:     /// # Safety\n   660:     ///\n   661:     /// Callers of this function are responsible that these preconditions are\n   662:     /// satisfied:\n   663:     ///\n   664:     /// * The starting index must not exceed the ending index;\n   665:     /// * Indexes must be within bounds of the original slice;\n   666:     /// * Indexes must lie on UTF-8 sequence boundaries.\n   667:     ///",
    "nanvix_source": "   657:     ///         s.make_ascii_uppercase();\n   658:     ///         &*s\n   659:     ///     });\n   660:     ///     assert_eq!(Some(\"HE\"), s);\n   661:     /// }\n   662:     /// assert_eq!(\"HEllo\", v);\n   663:     /// ```\n   664:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   665:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   666:     #[inline]\n   667:     pub const fn get_mut<I: [const] SliceIndex<str>>(&mut self, i: I) -> Option<&mut I::Output> {\n   668:         i.get_mut(self)\n   669:     }\n   670: \n   671:     /// Returns an unchecked subslice of `str`.\n   672:     ///\n   673:     /// This is the unchecked alternative to indexing the `str`.\n   674:     ///\n   675:     /// # Safety\n   676:     ///\n   677:     /// Callers of this function are responsible that these preconditions are",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::get_unchecked_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
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
                                  "primitive": "str"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9549,
                        "path": "SliceIndex"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "get_unchecked_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "i",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "qualified_path": {
                "args": null,
                "name": "Output",
                "self_type": {
                  "generic": "I"
                },
                "trait": {
                  "args": null,
                  "id": 9549,
                  "path": ""
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   702:     ///\n   703:     /// Failing that, the returned string slice may reference invalid memory or\n   704:     /// violate the invariants communicated by the `str` type.\n   705:     ///\n   706:     /// # Examples\n   707:     ///\n   708:     /// ```\n   709:     /// let mut v = String::from(\"\ud83d\uddfb\u2208\ud83c\udf0f\");\n   710:     /// unsafe {\n   711:     ///     assert_eq!(\"\ud83d\uddfb\", v.get_unchecked_mut(0..4));\n   712:     ///     assert_eq!(\"\u2208\", v.get_unchecked_mut(4..7));\n   713:     ///     assert_eq!(\"\ud83c\udf0f\", v.get_unchecked_mut(7..11));\n   714:     /// }\n   715:     /// ```\n   716:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   717:     #[inline]\n   718:     pub unsafe fn get_unchecked_mut<I: SliceIndex<str>>(&mut self, i: I) -> &mut I::Output {\n   719:         // SAFETY: the caller must uphold the safety contract for `get_unchecked_mut`;\n   720:         // the slice is dereferenceable because `self` is a safe reference.\n   721:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   722:         unsafe { &mut *i.get_unchecked_mut(self) }\n   723:     }\n   724: \n   725:     /// Creates a string slice from another string slice, bypassing safety\n   726:     /// checks.\n   727:     ///\n   728:     /// This is generally not recommended, use with caution! For a safe\n   729:     /// alternative see [`str`] and [`Index`].\n   730:     ///\n   731:     /// [`Index`]: crate::ops::Index\n   732:     ///\n   733:     /// This new slice goes from `begin` to `end`, including `begin` but\n   734:     /// excluding `end`.",
    "nanvix_source": "   724:     /// ```\n   725:     /// let mut v = String::from(\"\ud83d\uddfb\u2208\ud83c\udf0f\");\n   726:     /// unsafe {\n   727:     ///     assert_eq!(\"\ud83d\uddfb\", v.get_unchecked_mut(0..4));\n   728:     ///     assert_eq!(\"\u2208\", v.get_unchecked_mut(4..7));\n   729:     ///     assert_eq!(\"\ud83c\udf0f\", v.get_unchecked_mut(7..11));\n   730:     /// }\n   731:     /// ```\n   732:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   733:     #[inline]\n   734:     pub unsafe fn get_unchecked_mut<I: SliceIndex<str>>(&mut self, i: I) -> &mut I::Output {\n   735:         // SAFETY: the caller must uphold the safety contract for `get_unchecked_mut`;\n   736:         // the slice is dereferenceable because `self` is a safe reference.\n   737:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   738:         unsafe { &mut *i.get_unchecked_mut(self) }\n   739:     }\n   740: \n   741:     /// Creates a string slice from another string slice, bypassing safety\n   742:     /// checks.\n   743:     ///\n   744:     /// This is generally not recommended, use with caution! For a safe",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::slice_mut_unchecked",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_unsafe": true
      },
      "name": "slice_mut_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "begin",
            {
              "primitive": "usize"
            }
          ],
          [
            "end",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   787:     /// To get an immutable string slice instead, see the\n   788:     /// [`slice_unchecked`] method.\n   789:     ///\n   790:     /// [`slice_unchecked`]: str::slice_unchecked\n   791:     ///\n   792:     /// # Safety\n   793:     ///\n   794:     /// Callers of this function are responsible that three preconditions are\n   795:     /// satisfied:\n   796:     ///\n   797:     /// * `begin` must not exceed `end`.\n   798:     /// * `begin` and `end` must be byte positions within the string slice.\n   799:     /// * `begin` and `end` must lie on UTF-8 sequence boundaries.\n   800:     #[stable(feature = \"str_slice_mut\", since = \"1.5.0\")]\n   801:     #[deprecated(since = \"1.29.0\", note = \"use `get_unchecked_mut(begin..end)` instead\")]\n   802:     #[inline]\n   803:     pub unsafe fn slice_mut_unchecked(&mut self, begin: usize, end: usize) -> &mut str {\n   804:         // SAFETY: the caller must uphold the safety contract for `get_unchecked_mut`;\n   805:         // the slice is dereferenceable because `self` is a safe reference.\n   806:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   807:         unsafe { &mut *(begin..end).get_unchecked_mut(self) }\n   808:     }\n   809: \n   810:     /// Divides one string slice into two at an index.\n   811:     ///\n   812:     /// The argument, `mid`, should be a byte offset from the start of the\n   813:     /// string. It must also be on the boundary of a UTF-8 code point.\n   814:     ///\n   815:     /// The two slices returned go from the start of the string slice to `mid`,\n   816:     /// and from `mid` to the end of the string slice.\n   817:     ///\n   818:     /// To get mutable string slices instead, see the [`split_at_mut`]\n   819:     /// method.",
    "nanvix_source": "   809:     ///\n   810:     /// Callers of this function are responsible that three preconditions are\n   811:     /// satisfied:\n   812:     ///\n   813:     /// * `begin` must not exceed `end`.\n   814:     /// * `begin` and `end` must be byte positions within the string slice.\n   815:     /// * `begin` and `end` must lie on UTF-8 sequence boundaries.\n   816:     #[stable(feature = \"str_slice_mut\", since = \"1.5.0\")]\n   817:     #[deprecated(since = \"1.29.0\", note = \"use `get_unchecked_mut(begin..end)` instead\")]\n   818:     #[inline]\n   819:     pub unsafe fn slice_mut_unchecked(&mut self, begin: usize, end: usize) -> &mut str {\n   820:         // SAFETY: the caller must uphold the safety contract for `get_unchecked_mut`;\n   821:         // the slice is dereferenceable because `self` is a safe reference.\n   822:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   823:         unsafe { &mut *(begin..end).get_unchecked_mut(self) }\n   824:     }\n   825: \n   826:     /// Divides one string slice into two at an index.\n   827:     ///\n   828:     /// The argument, `mid`, should be a byte offset from the start of the\n   829:     /// string. It must also be on the boundary of a UTF-8 code point.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_at_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "split_at_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "mid",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            },
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ]
        }
      }
    },
    "verification_source": "   868:     /// # Examples\n   869:     ///\n   870:     /// ```\n   871:     /// let mut s = \"Per Martin-L\u00f6f\".to_string();\n   872:     /// {\n   873:     ///     let (first, last) = s.split_at_mut(3);\n   874:     ///     first.make_ascii_uppercase();\n   875:     ///     assert_eq!(\"PER\", first);\n   876:     ///     assert_eq!(\" Martin-L\u00f6f\", last);\n   877:     /// }\n   878:     /// assert_eq!(\"PER Martin-L\u00f6f\", s);\n   879:     /// ```\n   880:     #[inline]\n   881:     #[must_use]\n   882:     #[stable(feature = \"str_split_at\", since = \"1.4.0\")]\n   883:     #[rustc_const_stable(feature = \"const_str_split_at\", since = \"1.86.0\")]\n   884:     pub const fn split_at_mut(&mut self, mid: usize) -> (&mut str, &mut str) {\n   885:         // is_char_boundary checks that the index is in [0, .len()]\n   886:         if self.is_char_boundary(mid) {\n   887:             // SAFETY: just checked that `mid` is on a char boundary.\n   888:             unsafe { self.split_at_mut_unchecked(mid) }\n   889:         } else {\n   890:             slice_error_fail(self, 0, mid)\n   891:         }\n   892:     }\n   893: \n   894:     /// Divides one string slice into two at an index.\n   895:     ///\n   896:     /// The argument, `mid`, should be a valid byte offset from the start of the\n   897:     /// string. It must also be on the boundary of a UTF-8 code point. The\n   898:     /// method returns `None` if that\u2019s not the case.\n   899:     ///\n   900:     /// The two slices returned go from the start of the string slice to `mid`,",
    "nanvix_source": "   890:     ///     first.make_ascii_uppercase();\n   891:     ///     assert_eq!(\"PER\", first);\n   892:     ///     assert_eq!(\" Martin-L\u00f6f\", last);\n   893:     /// }\n   894:     /// assert_eq!(\"PER Martin-L\u00f6f\", s);\n   895:     /// ```\n   896:     #[inline]\n   897:     #[must_use]\n   898:     #[stable(feature = \"str_split_at\", since = \"1.4.0\")]\n   899:     #[rustc_const_stable(feature = \"const_str_split_at\", since = \"1.86.0\")]\n   900:     pub const fn split_at_mut(&mut self, mid: usize) -> (&mut str, &mut str) {\n   901:         // is_char_boundary checks that the index is in [0, .len()]\n   902:         if self.is_char_boundary(mid) {\n   903:             // SAFETY: just checked that `mid` is on a char boundary.\n   904:             unsafe { self.split_at_mut_unchecked(mid) }\n   905:         } else {\n   906:             slice_error_fail(self, 0, mid)\n   907:         }\n   908:     }\n   909: \n   910:     /// Divides one string slice into two at an index.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_at_mut_checked",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "split_at_mut_checked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "mid",
            {
              "primitive": "usize"
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "primitive": "str"
                            }
                          }
                        },
                        {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "primitive": "str"
                            }
                          }
                        }
                      ]
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
    "verification_source": "   949:     /// ```\n   950:     /// let mut s = \"Per Martin-L\u00f6f\".to_string();\n   951:     /// if let Some((first, last)) = s.split_at_mut_checked(3) {\n   952:     ///     first.make_ascii_uppercase();\n   953:     ///     assert_eq!(\"PER\", first);\n   954:     ///     assert_eq!(\" Martin-L\u00f6f\", last);\n   955:     /// }\n   956:     /// assert_eq!(\"PER Martin-L\u00f6f\", s);\n   957:     ///\n   958:     /// assert_eq!(None, s.split_at_mut_checked(13));  // Inside \u201c\u00f6\u201d\n   959:     /// assert_eq!(None, s.split_at_mut_checked(16));  // Beyond the string length\n   960:     /// ```\n   961:     #[inline]\n   962:     #[must_use]\n   963:     #[stable(feature = \"split_at_checked\", since = \"1.80.0\")]\n   964:     #[rustc_const_stable(feature = \"const_str_split_at\", since = \"1.86.0\")]\n   965:     pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut str, &mut str)> {\n   966:         // is_char_boundary checks that the index is in [0, .len()]\n   967:         if self.is_char_boundary(mid) {\n   968:             // SAFETY: just checked that `mid` is on a char boundary.\n   969:             Some(unsafe { self.split_at_mut_unchecked(mid) })\n   970:         } else {\n   971:             None\n   972:         }\n   973:     }\n   974: \n   975:     /// Divides one string slice into two at an index.\n   976:     ///\n   977:     /// # Safety\n   978:     ///\n   979:     /// The caller must ensure that `mid` is a valid byte offset from the start\n   980:     /// of the string and falls on the boundary of a UTF-8 code point.\n   981:     #[inline]",
    "nanvix_source": "   971:     /// }\n   972:     /// assert_eq!(\"PER Martin-L\u00f6f\", s);\n   973:     ///\n   974:     /// assert_eq!(None, s.split_at_mut_checked(13));  // Inside \u201c\u00f6\u201d\n   975:     /// assert_eq!(None, s.split_at_mut_checked(16));  // Beyond the string length\n   976:     /// ```\n   977:     #[inline]\n   978:     #[must_use]\n   979:     #[stable(feature = \"split_at_checked\", since = \"1.80.0\")]\n   980:     #[rustc_const_stable(feature = \"const_str_split_at\", since = \"1.86.0\")]\n   981:     pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut str, &mut str)> {\n   982:         // is_char_boundary checks that the index is in [0, .len()]\n   983:         if self.is_char_boundary(mid) {\n   984:             // SAFETY: just checked that `mid` is on a char boundary.\n   985:             Some(unsafe { self.split_at_mut_unchecked(mid) })\n   986:         } else {\n   987:             None\n   988:         }\n   989:     }\n   990: \n   991:     /// Divides one string slice into two at an index.",
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
