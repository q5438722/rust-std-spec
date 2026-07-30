For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::as_mut_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_mut_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   576:     }\n   577: \n   578:     /// Converts a mutable string slice to a raw pointer.\n   579:     ///\n   580:     /// As string slices are a slice of bytes, the raw pointer points to a\n   581:     /// [`u8`]. This pointer will be pointing to the first byte of the string\n   582:     /// slice.\n   583:     ///\n   584:     /// It is your responsibility to make sure that the string slice only gets\n   585:     /// modified in a way that it remains valid UTF-8.\n   586:     #[stable(feature = \"str_as_mut_ptr\", since = \"1.36.0\")]\n   587:     #[rustc_const_stable(feature = \"const_str_as_mut\", since = \"1.83.0\")]\n   588:     #[rustc_never_returns_null_ptr]\n   589:     #[rustc_as_ptr]\n   590:     #[must_use]\n   591:     #[inline(always)]\n   592:     pub const fn as_mut_ptr(&mut self) -> *mut u8 {\n   593:         self as *mut str as *mut u8\n   594:     }\n   595: \n   596:     /// Returns a subslice of `str`.\n   597:     ///\n   598:     /// This is the non-panicking alternative to indexing the `str`. Returns\n   599:     /// [`None`] whenever equivalent indexing operation would panic.\n   600:     ///\n   601:     /// # Examples\n   602:     ///\n   603:     /// ```\n   604:     /// let v = String::from(\"\ud83d\uddfb\u2208\ud83c\udf0f\");\n   605:     ///\n   606:     /// assert_eq!(Some(\"\ud83d\uddfb\"), v.get(0..4));\n   607:     ///\n   608:     /// // indices not on UTF-8 sequence boundaries",
    "nanvix_source": "   598:     ///\n   599:     /// It is your responsibility to make sure that the string slice only gets\n   600:     /// modified in a way that it remains valid UTF-8.\n   601:     #[stable(feature = \"str_as_mut_ptr\", since = \"1.36.0\")]\n   602:     #[rustc_const_stable(feature = \"const_str_as_mut\", since = \"1.83.0\")]\n   603:     #[rustc_never_returns_null_ptr]\n   604:     #[rustc_as_ptr]\n   605:     #[must_use]\n   606:     #[inline(always)]\n   607:     #[rustc_no_writable]\n   608:     pub const fn as_mut_ptr(&mut self) -> *mut u8 {\n   609:         self as *mut str as *mut u8\n   610:     }\n   611: \n   612:     /// Returns a subslice of `str`.\n   613:     ///\n   614:     /// This is the non-panicking alternative to indexing the `str`. Returns\n   615:     /// [`None`] whenever equivalent indexing operation would panic.\n   616:     ///\n   617:     /// # Examples\n   618:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   558:     /// If you need to mutate the contents of the string slice, use [`as_mut_ptr`].\n   559:     ///\n   560:     /// [`as_mut_ptr`]: str::as_mut_ptr\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// let s = \"Hello\";\n   566:     /// let ptr = s.as_ptr();\n   567:     /// ```\n   568:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   569:     #[rustc_const_stable(feature = \"rustc_str_as_ptr\", since = \"1.32.0\")]\n   570:     #[rustc_never_returns_null_ptr]\n   571:     #[rustc_as_ptr]\n   572:     #[must_use]\n   573:     #[inline(always)]\n   574:     pub const fn as_ptr(&self) -> *const u8 {\n   575:         self as *const str as *const u8\n   576:     }\n   577: \n   578:     /// Converts a mutable string slice to a raw pointer.\n   579:     ///\n   580:     /// As string slices are a slice of bytes, the raw pointer points to a\n   581:     /// [`u8`]. This pointer will be pointing to the first byte of the string\n   582:     /// slice.\n   583:     ///\n   584:     /// It is your responsibility to make sure that the string slice only gets\n   585:     /// modified in a way that it remains valid UTF-8.\n   586:     #[stable(feature = \"str_as_mut_ptr\", since = \"1.36.0\")]\n   587:     #[rustc_const_stable(feature = \"const_str_as_mut\", since = \"1.83.0\")]\n   588:     #[rustc_never_returns_null_ptr]\n   589:     #[rustc_as_ptr]\n   590:     #[must_use]",
    "nanvix_source": "   579:     /// ```\n   580:     /// let s = \"Hello\";\n   581:     /// let ptr = s.as_ptr();\n   582:     /// ```\n   583:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   584:     #[rustc_const_stable(feature = \"rustc_str_as_ptr\", since = \"1.32.0\")]\n   585:     #[rustc_never_returns_null_ptr]\n   586:     #[rustc_as_ptr]\n   587:     #[must_use]\n   588:     #[inline(always)]\n   589:     pub const fn as_ptr(&self) -> *const u8 {\n   590:         self as *const str as *const u8\n   591:     }\n   592: \n   593:     /// Converts a mutable string slice to a raw pointer.\n   594:     ///\n   595:     /// As string slices are a slice of bytes, the raw pointer points to a\n   596:     /// [`u8`]. This pointer will be pointing to the first byte of the string\n   597:     /// slice.\n   598:     ///\n   599:     /// It is your responsibility to make sure that the string slice only gets",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::from_utf8",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "multiple_rust_declarations_share_path"
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
        "is_unsafe": false
      },
      "name": "from_utf8",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
                "is_mutable": false,
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
                          "primitive": "str"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10083,
                        "path": "Utf8Error"
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
    "verification_source": "   235:     /// errors that can be returned.\n   236:     ///\n   237:     /// A \"stack allocated string\":\n   238:     ///\n   239:     /// ```\n   240:     /// // some bytes, in a stack-allocated array\n   241:     /// let sparkle_heart = [240, 159, 146, 150];\n   242:     ///\n   243:     /// // We know these bytes are valid, so just use `unwrap()`.\n   244:     /// let sparkle_heart: &str = str::from_utf8(&sparkle_heart).unwrap();\n   245:     ///\n   246:     /// assert_eq!(\"\ud83d\udc96\", sparkle_heart);\n   247:     /// ```\n   248:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   249:     #[rustc_const_stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   250:     #[rustc_diagnostic_item = \"str_inherent_from_utf8\"]\n   251:     pub const fn from_utf8(v: &[u8]) -> Result<&str, Utf8Error> {\n   252:         converts::from_utf8(v)\n   253:     }\n   254: \n   255:     /// Converts a mutable slice of bytes to a mutable string slice.\n   256:     ///\n   257:     /// # Examples\n   258:     ///\n   259:     /// Basic usage:\n   260:     ///\n   261:     /// ```\n   262:     /// // \"Hello, Rust!\" as a mutable vector\n   263:     /// let mut hellorust = vec![72, 101, 108, 108, 111, 44, 32, 82, 117, 115, 116, 33];\n   264:     ///\n   265:     /// // As we know these bytes are valid, we can use `unwrap()`\n   266:     /// let outstr = str::from_utf8_mut(&mut hellorust).unwrap();\n   267:     ///",
    "nanvix_source": "   242:     /// let sparkle_heart = [240, 159, 146, 150];\n   243:     ///\n   244:     /// // We know these bytes are valid, so just use `unwrap()`.\n   245:     /// let sparkle_heart: &str = str::from_utf8(&sparkle_heart).unwrap();\n   246:     ///\n   247:     /// assert_eq!(\"\ud83d\udc96\", sparkle_heart);\n   248:     /// ```\n   249:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   250:     #[rustc_const_stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   251:     #[rustc_diagnostic_item = \"str_inherent_from_utf8\"]\n   252:     pub const fn from_utf8(v: &[u8]) -> Result<&str, Utf8Error> {\n   253:         converts::from_utf8(v)\n   254:     }\n   255: \n   256:     /// Converts a mutable slice of bytes to a mutable string slice.\n   257:     ///\n   258:     /// # Examples\n   259:     ///\n   260:     /// Basic usage:\n   261:     ///\n   262:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::get_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
      "name": "get_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
                "is_mutable": false,
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
            "is_mutable": false,
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
    "verification_source": "   667:     ///\n   668:     /// Failing that, the returned string slice may reference invalid memory or\n   669:     /// violate the invariants communicated by the `str` type.\n   670:     ///\n   671:     /// # Examples\n   672:     ///\n   673:     /// ```\n   674:     /// let v = \"\ud83d\uddfb\u2208\ud83c\udf0f\";\n   675:     /// unsafe {\n   676:     ///     assert_eq!(\"\ud83d\uddfb\", v.get_unchecked(0..4));\n   677:     ///     assert_eq!(\"\u2208\", v.get_unchecked(4..7));\n   678:     ///     assert_eq!(\"\ud83c\udf0f\", v.get_unchecked(7..11));\n   679:     /// }\n   680:     /// ```\n   681:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   682:     #[inline]\n   683:     pub unsafe fn get_unchecked<I: SliceIndex<str>>(&self, i: I) -> &I::Output {\n   684:         // SAFETY: the caller must uphold the safety contract for `get_unchecked`;\n   685:         // the slice is dereferenceable because `self` is a safe reference.\n   686:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   687:         unsafe { &*i.get_unchecked(self) }\n   688:     }\n   689: \n   690:     /// Returns a mutable, unchecked subslice of `str`.\n   691:     ///\n   692:     /// This is the unchecked alternative to indexing the `str`.\n   693:     ///\n   694:     /// # Safety\n   695:     ///\n   696:     /// Callers of this function are responsible that these preconditions are\n   697:     /// satisfied:\n   698:     ///\n   699:     /// * The starting index must not exceed the ending index;",
    "nanvix_source": "   689:     /// ```\n   690:     /// let v = \"\ud83d\uddfb\u2208\ud83c\udf0f\";\n   691:     /// unsafe {\n   692:     ///     assert_eq!(\"\ud83d\uddfb\", v.get_unchecked(0..4));\n   693:     ///     assert_eq!(\"\u2208\", v.get_unchecked(4..7));\n   694:     ///     assert_eq!(\"\ud83c\udf0f\", v.get_unchecked(7..11));\n   695:     /// }\n   696:     /// ```\n   697:     #[stable(feature = \"str_checked_slicing\", since = \"1.20.0\")]\n   698:     #[inline]\n   699:     pub unsafe fn get_unchecked<I: SliceIndex<str>>(&self, i: I) -> &I::Output {\n   700:         // SAFETY: the caller must uphold the safety contract for `get_unchecked`;\n   701:         // the slice is dereferenceable because `self` is a safe reference.\n   702:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   703:         unsafe { &*i.get_unchecked(self) }\n   704:     }\n   705: \n   706:     /// Returns a mutable, unchecked subslice of `str`.\n   707:     ///\n   708:     /// This is the unchecked alternative to indexing the `str`.\n   709:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::slice_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
      "name": "slice_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
                "is_mutable": false,
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
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   753:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n   754:     ///\n   755:     /// unsafe {\n   756:     ///     assert_eq!(\"L\u00f6we \u8001\u864e L\u00e9opard\", s.slice_unchecked(0, 21));\n   757:     /// }\n   758:     ///\n   759:     /// let s = \"Hello, world!\";\n   760:     ///\n   761:     /// unsafe {\n   762:     ///     assert_eq!(\"world\", s.slice_unchecked(7, 12));\n   763:     /// }\n   764:     /// ```\n   765:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   766:     #[deprecated(since = \"1.29.0\", note = \"use `get_unchecked(begin..end)` instead\")]\n   767:     #[must_use]\n   768:     #[inline]\n   769:     pub unsafe fn slice_unchecked(&self, begin: usize, end: usize) -> &str {\n   770:         // SAFETY: the caller must uphold the safety contract for `get_unchecked`;\n   771:         // the slice is dereferenceable because `self` is a safe reference.\n   772:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   773:         unsafe { &*(begin..end).get_unchecked(self) }\n   774:     }\n   775: \n   776:     /// Creates a string slice from another string slice, bypassing safety\n   777:     /// checks.\n   778:     ///\n   779:     /// This is generally not recommended, use with caution! For a safe\n   780:     /// alternative see [`str`] and [`IndexMut`].\n   781:     ///\n   782:     /// [`IndexMut`]: crate::ops::IndexMut\n   783:     ///\n   784:     /// This new slice goes from `begin` to `end`, including `begin` but\n   785:     /// excluding `end`.",
    "nanvix_source": "   775:     /// let s = \"Hello, world!\";\n   776:     ///\n   777:     /// unsafe {\n   778:     ///     assert_eq!(\"world\", s.slice_unchecked(7, 12));\n   779:     /// }\n   780:     /// ```\n   781:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   782:     #[deprecated(since = \"1.29.0\", note = \"use `get_unchecked(begin..end)` instead\")]\n   783:     #[must_use]\n   784:     #[inline]\n   785:     pub unsafe fn slice_unchecked(&self, begin: usize, end: usize) -> &str {\n   786:         // SAFETY: the caller must uphold the safety contract for `get_unchecked`;\n   787:         // the slice is dereferenceable because `self` is a safe reference.\n   788:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   789:         unsafe { &*(begin..end).get_unchecked(self) }\n   790:     }\n   791: \n   792:     /// Creates a string slice from another string slice, bypassing safety\n   793:     /// checks.\n   794:     ///\n   795:     /// This is generally not recommended, use with caution! For a safe",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::from_encoded_bytes_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
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
      "name": "from_encoded_bytes_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   865:     /// use std::ffi::OsStr;\n   866:     ///\n   867:     /// let os_str = OsStr::new(\"Mary had a little lamb\");\n   868:     /// let bytes = os_str.as_encoded_bytes();\n   869:     /// let words = bytes.split(|b| *b == b' ');\n   870:     /// let words: Vec<&OsStr> = words.map(|word| {\n   871:     ///     // SAFETY:\n   872:     ///     // - Each `word` only contains content that originated from `OsStr::as_encoded_bytes`\n   873:     ///     // - Only split with ASCII whitespace which is a non-empty UTF-8 substring\n   874:     ///     unsafe { OsStr::from_encoded_bytes_unchecked(word) }\n   875:     /// }).collect();\n   876:     /// ```\n   877:     ///\n   878:     /// [conversions]: super#conversions\n   879:     #[inline]\n   880:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   881:     pub unsafe fn from_encoded_bytes_unchecked(bytes: &[u8]) -> &Self {\n   882:         Self::from_inner(unsafe { Slice::from_encoded_bytes_unchecked(bytes) })\n   883:     }\n   884: \n   885:     #[inline]\n   886:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   887:     const fn from_inner(inner: &Slice) -> &OsStr {\n   888:         // SAFETY: OsStr is just a wrapper of Slice,\n   889:         // therefore converting &Slice to &OsStr is safe.\n   890:         unsafe { &*(inner as *const Slice as *const OsStr) }\n   891:     }\n   892: \n   893:     #[inline]\n   894:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   895:     const fn from_inner_mut(inner: &mut Slice) -> &mut OsStr {\n   896:         // SAFETY: OsStr is just a wrapper of Slice,\n   897:         // therefore converting &mut Slice to &mut OsStr is safe.",
    "nanvix_source": "   863:     ///     // SAFETY:\n   864:     ///     // - Each `word` only contains content that originated from `OsStr::as_encoded_bytes`\n   865:     ///     // - Only split with ASCII whitespace which is a non-empty UTF-8 substring\n   866:     ///     unsafe { OsStr::from_encoded_bytes_unchecked(word) }\n   867:     /// }).collect();\n   868:     /// ```\n   869:     ///\n   870:     /// [conversions]: super#conversions\n   871:     #[inline]\n   872:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   873:     pub unsafe fn from_encoded_bytes_unchecked(bytes: &[u8]) -> &Self {\n   874:         Self::from_inner(unsafe { Slice::from_encoded_bytes_unchecked(bytes) })\n   875:     }\n   876: \n   877:     #[inline]\n   878:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   879:     const fn from_inner(inner: &Slice) -> &OsStr {\n   880:         // SAFETY: OsStr is just a wrapper of Slice,\n   881:         // therefore converting &Slice to &OsStr is safe.\n   882:         unsafe { &*(inner as *const Slice as *const OsStr) }\n   883:     }",
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
