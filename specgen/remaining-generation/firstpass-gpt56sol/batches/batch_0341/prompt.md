For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::as_ptr_range",
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
      "name": "as_ptr_range",
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
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "raw_pointer": {
                        "is_mutable": false,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9744,
            "path": "Range"
          }
        }
      }
    },
    "verification_source": "   777:     /// element of this slice:\n   778:     ///\n   779:     /// ```\n   780:     /// let a = [1, 2, 3];\n   781:     /// let x = &a[1] as *const _;\n   782:     /// let y = &5 as *const _;\n   783:     ///\n   784:     /// assert!(a.as_ptr_range().contains(&x));\n   785:     /// assert!(!a.as_ptr_range().contains(&y));\n   786:     /// ```\n   787:     ///\n   788:     /// [`as_ptr`]: slice::as_ptr\n   789:     #[stable(feature = \"slice_ptr_range\", since = \"1.48.0\")]\n   790:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   791:     #[inline]\n   792:     #[must_use]\n   793:     pub const fn as_ptr_range(&self) -> Range<*const T> {\n   794:         let start = self.as_ptr();\n   795:         // SAFETY: The `add` here is safe, because:\n   796:         //\n   797:         //   - Both pointers are part of the same object, as pointing directly\n   798:         //     past the object also counts.\n   799:         //\n   800:         //   - The size of the slice is never larger than `isize::MAX` bytes, as\n   801:         //     noted here:\n   802:         //       - https://github.com/rust-lang/unsafe-code-guidelines/issues/102#issuecomment-473340447\n   803:         //       - https://doc.rust-lang.org/reference/behavior-considered-undefined.html\n   804:         //       - https://doc.rust-lang.org/core/slice/fn.from_raw_parts.html#safety\n   805:         //     (This doesn't seem normative yet, but the very same assumption is\n   806:         //     made in many places, including the Index implementation of slices.)\n   807:         //\n   808:         //   - There is no wrapping around involved, as slices do not wrap past\n   809:         //     the end of the address space.",
    "nanvix_source": "   786:     ///\n   787:     /// assert!(a.as_ptr_range().contains(&x));\n   788:     /// assert!(!a.as_ptr_range().contains(&y));\n   789:     /// ```\n   790:     ///\n   791:     /// [`as_ptr`]: slice::as_ptr\n   792:     #[stable(feature = \"slice_ptr_range\", since = \"1.48.0\")]\n   793:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   794:     #[inline]\n   795:     #[must_use]\n   796:     pub const fn as_ptr_range(&self) -> Range<*const T> {\n   797:         let start = self.as_ptr();\n   798:         // SAFETY: The `add` here is safe, because:\n   799:         //\n   800:         //   - Both pointers are part of the same object, as pointing directly\n   801:         //     past the object also counts.\n   802:         //\n   803:         //   - The size of the slice is never larger than `isize::MAX` bytes, as\n   804:         //     noted here:\n   805:         //       - https://github.com/rust-lang/unsafe-code-guidelines/issues/102#issuecomment-473340447\n   806:         //       - https://doc.rust-lang.org/reference/behavior-considered-undefined.html",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::assume_init_drop",
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
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "assume_init_drop",
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
        "for": {
          "slice": {
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
              "id": 8278,
              "path": "MaybeUninit"
            }
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51771",
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
        "output": null
      }
    },
    "verification_source": "  1470:     ///\n  1471:     /// It is up to the caller to guarantee that every `MaybeUninit<T>` in the slice\n  1472:     /// really is in an initialized state. Calling this when the content is not yet\n  1473:     /// fully initialized causes undefined behavior.\n  1474:     ///\n  1475:     /// On top of that, all additional invariants of the type `T` must be\n  1476:     /// satisfied, as the `Drop` implementation of `T` (or its members) may\n  1477:     /// rely on this. For example, setting a `Vec<T>` to an invalid but\n  1478:     /// non-null address makes it initialized (under the current implementation;\n  1479:     /// this does not constitute a stable guarantee), because the only\n  1480:     /// requirement the compiler knows about it is that the data pointer must be\n  1481:     /// non-null. Dropping such a `Vec<T>` however will cause undefined\n  1482:     /// behaviour.\n  1483:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1484:     #[inline(always)]\n  1485:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1486:     pub const unsafe fn assume_init_drop(&mut self)\n  1487:     where\n  1488:         T: [const] Destruct,\n  1489:     {\n  1490:         if !self.is_empty() {\n  1491:             // SAFETY: the caller must guarantee that every element of `self`\n  1492:             // is initialized and satisfies all invariants of `T`.\n  1493:             // Dropping the value in place is safe if that is the case.\n  1494:             unsafe { ptr::drop_in_place(self as *mut [MaybeUninit<T>] as *mut [T]) }\n  1495:         }\n  1496:     }\n  1497: \n  1498:     /// Gets a shared reference to the contained value.\n  1499:     ///\n  1500:     /// # Safety\n  1501:     ///\n  1502:     /// Calling this when the content is not yet fully initialized causes undefined",
    "nanvix_source": "  1477:     /// satisfied, as the `Drop` implementation of `T` (or its members) may\n  1478:     /// rely on this. For example, setting a `Vec<T>` to an invalid but\n  1479:     /// non-null address makes it initialized (under the current implementation;\n  1480:     /// this does not constitute a stable guarantee), because the only\n  1481:     /// requirement the compiler knows about it is that the data pointer must be\n  1482:     /// non-null. Dropping such a `Vec<T>` however will cause undefined\n  1483:     /// behaviour.\n  1484:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1485:     #[inline(always)]\n  1486:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1487:     pub const unsafe fn assume_init_drop(&mut self)\n  1488:     where\n  1489:         T: [const] Destruct,\n  1490:     {\n  1491:         if !self.is_empty() {\n  1492:             // SAFETY: the caller must guarantee that every element of `self`\n  1493:             // is initialized and satisfies all invariants of `T`.\n  1494:             // Dropping the value in place is safe if that is the case.\n  1495:             unsafe { ptr::drop_in_place(self as *mut [MaybeUninit<T>] as *mut [T]) }\n  1496:         }\n  1497:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::assume_init_ref",
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "assume_init_ref",
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
          "slice": {
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
              "id": 8278,
              "path": "MaybeUninit"
            }
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51771",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1492:             // is initialized and satisfies all invariants of `T`.\n  1493:             // Dropping the value in place is safe if that is the case.\n  1494:             unsafe { ptr::drop_in_place(self as *mut [MaybeUninit<T>] as *mut [T]) }\n  1495:         }\n  1496:     }\n  1497: \n  1498:     /// Gets a shared reference to the contained value.\n  1499:     ///\n  1500:     /// # Safety\n  1501:     ///\n  1502:     /// Calling this when the content is not yet fully initialized causes undefined\n  1503:     /// behavior: it is up to the caller to guarantee that every `MaybeUninit<T>` in\n  1504:     /// the slice really is in an initialized state.\n  1505:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1506:     #[rustc_const_stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1507:     #[inline(always)]\n  1508:     pub const unsafe fn assume_init_ref(&self) -> &[T] {\n  1509:         // SAFETY: casting `slice` to a `*const [T]` is safe since the caller guarantees that\n  1510:         // `slice` is initialized, and `MaybeUninit` is guaranteed to have the same layout as `T`.\n  1511:         // The pointer obtained is valid since it refers to memory owned by `slice` which is a\n  1512:         // reference and thus guaranteed to be valid for reads.\n  1513:         unsafe { &*(self as *const Self as *const [T]) }\n  1514:     }\n  1515: \n  1516:     /// Gets a mutable (unique) reference to the contained value.\n  1517:     ///\n  1518:     /// # Safety\n  1519:     ///\n  1520:     /// Calling this when the content is not yet fully initialized causes undefined\n  1521:     /// behavior: it is up to the caller to guarantee that every `MaybeUninit<T>` in the\n  1522:     /// slice really is in an initialized state. For instance, `.assume_init_mut()` cannot\n  1523:     /// be used to initialize a `MaybeUninit` slice.\n  1524:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]",
    "nanvix_source": "  1499:     /// Gets a shared reference to the contained value.\n  1500:     ///\n  1501:     /// # Safety\n  1502:     ///\n  1503:     /// Calling this when the content is not yet fully initialized causes undefined\n  1504:     /// behavior: it is up to the caller to guarantee that every `MaybeUninit<T>` in\n  1505:     /// the slice really is in an initialized state.\n  1506:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1507:     #[rustc_const_stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1508:     #[inline(always)]\n  1509:     pub const unsafe fn assume_init_ref(&self) -> &[T] {\n  1510:         // SAFETY: casting `slice` to a `*const [T]` is safe since the caller guarantees that\n  1511:         // `slice` is initialized, and `MaybeUninit` is guaranteed to have the same layout as `T`.\n  1512:         // The pointer obtained is valid since it refers to memory owned by `slice` which is a\n  1513:         // reference and thus guaranteed to be valid for reads.\n  1514:         unsafe { &*(self as *const Self as *const [T]) }\n  1515:     }\n  1516: \n  1517:     /// Gets a mutable (unique) reference to the contained value.\n  1518:     ///\n  1519:     /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::from_raw_parts",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "from_raw_parts",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "data",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "len",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "   108: ///\n   109: /// // This could be the result of C++'s std::vector::data():\n   110: /// let ptr = std::ptr::null();\n   111: /// // And this could be std::vector::size():\n   112: /// let len = 0;\n   113: /// assert_eq!(unsafe { sum_slice(ptr, len) }, 0.0);\n   114: /// ```\n   115: ///\n   116: /// [valid]: ptr#safety\n   117: /// [`NonNull::dangling()`]: ptr::NonNull::dangling\n   118: #[inline]\n   119: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   120: #[rustc_const_stable(feature = \"const_slice_from_raw_parts\", since = \"1.64.0\")]\n   121: #[must_use]\n   122: #[rustc_diagnostic_item = \"slice_from_raw_parts\"]\n   123: #[track_caller]\n   124: pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T] {\n   125:     // SAFETY: the caller must uphold the safety contract for `from_raw_parts`.\n   126:     unsafe {\n   127:         ub_checks::assert_unsafe_precondition!(\n   128:             check_language_ub,\n   129:             \"slice::from_raw_parts requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`\",\n   130:             (\n   131:                 data: *mut () = data as *mut (),\n   132:                 size: usize = size_of::<T>(),\n   133:                 align: usize = align_of::<T>(),\n   134:                 len: usize = len,\n   135:             ) =>\n   136:             ub_checks::maybe_is_aligned_and_not_null(data, align, false)\n   137:                 && ub_checks::is_valid_allocation_size(size, len)\n   138:         );\n   139:         &*ptr::slice_from_raw_parts(data, len)\n   140:     }",
    "nanvix_source": "   114: /// ```\n   115: ///\n   116: /// [valid]: ptr#safety\n   117: /// [`NonNull::dangling()`]: ptr::NonNull::dangling\n   118: #[inline]\n   119: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   120: #[rustc_const_stable(feature = \"const_slice_from_raw_parts\", since = \"1.64.0\")]\n   121: #[must_use]\n   122: #[rustc_diagnostic_item = \"slice_from_raw_parts\"]\n   123: #[track_caller]\n   124: pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T] {\n   125:     // SAFETY: the caller must uphold the safety contract for `from_raw_parts`.\n   126:     unsafe {\n   127:         ub_checks::assert_unsafe_precondition!(\n   128:             check_language_ub,\n   129:             \"slice::from_raw_parts requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`\",\n   130:             (\n   131:                 data: *mut () = data as *mut (),\n   132:                 size: usize = size_of::<T>(),\n   133:                 align: usize = align_of::<T>(),\n   134:                 len: usize = len,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::get_unchecked",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
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
                                "generic": "Self"
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
              "generic_params": [],
              "type": {
                "generic": "I"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
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
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
            "index",
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
    "verification_source": "   623:     ///\n   624:     /// # Examples\n   625:     ///\n   626:     /// ```\n   627:     /// let x = &[1, 2, 4];\n   628:     ///\n   629:     /// unsafe {\n   630:     ///     assert_eq!(x.get_unchecked(1), &2);\n   631:     /// }\n   632:     /// ```\n   633:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   634:     #[rustc_no_implicit_autorefs]\n   635:     #[inline]\n   636:     #[must_use]\n   637:     #[track_caller]\n   638:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   639:     pub const unsafe fn get_unchecked<I>(&self, index: I) -> &I::Output\n   640:     where\n   641:         I: [const] SliceIndex<Self>,\n   642:     {\n   643:         // SAFETY: the caller must uphold most of the safety requirements for `get_unchecked`;\n   644:         // the slice is dereferenceable because `self` is a safe reference.\n   645:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   646:         unsafe { &*index.get_unchecked(self) }\n   647:     }\n   648: \n   649:     /// Returns a mutable reference to an element or subslice, without doing\n   650:     /// bounds checking.\n   651:     ///\n   652:     /// For a safe alternative see [`get_mut`].\n   653:     ///\n   654:     /// # Safety\n   655:     ///",
    "nanvix_source": "   630:     /// unsafe {\n   631:     ///     assert_eq!(x.get_unchecked(1), &2);\n   632:     /// }\n   633:     /// ```\n   634:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   635:     #[rustc_no_implicit_autorefs]\n   636:     #[inline]\n   637:     #[must_use]\n   638:     #[track_caller]\n   639:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   640:     pub const unsafe fn get_unchecked<I>(&self, index: I) -> &I::Output\n   641:     where\n   642:         I: [const] SliceIndex<Self>,\n   643:     {\n   644:         // SAFETY: the caller must uphold most of the safety requirements for `get_unchecked`;\n   645:         // the slice is dereferenceable because `self` is a safe reference.\n   646:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   647:         unsafe { &*index.get_unchecked(self) }\n   648:     }\n   649: \n   650:     /// Returns a mutable reference to an element or subslice, without doing",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_at_unchecked",
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "split_at_unchecked",
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
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            },
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            }
          ]
        }
      }
    },
    "verification_source": "  2022:     ///     let (left, right) = v.split_at_unchecked(2);\n  2023:     ///     assert_eq!(left, ['a', 'b']);\n  2024:     ///     assert_eq!(right, ['c']);\n  2025:     /// }\n  2026:     ///\n  2027:     /// unsafe {\n  2028:     ///     let (left, right) = v.split_at_unchecked(3);\n  2029:     ///     assert_eq!(left, ['a', 'b', 'c']);\n  2030:     ///     assert_eq!(right, []);\n  2031:     /// }\n  2032:     /// ```\n  2033:     #[stable(feature = \"slice_split_at_unchecked\", since = \"1.79.0\")]\n  2034:     #[rustc_const_stable(feature = \"const_slice_split_at_unchecked\", since = \"1.77.0\")]\n  2035:     #[inline]\n  2036:     #[must_use]\n  2037:     #[track_caller]\n  2038:     pub const unsafe fn split_at_unchecked(&self, mid: usize) -> (&[T], &[T]) {\n  2039:         // FIXME(const-hack): the const function `from_raw_parts` is used to make this\n  2040:         // function const; previously the implementation used\n  2041:         // `(self.get_unchecked(..mid), self.get_unchecked(mid..))`\n  2042: \n  2043:         let len = self.len();\n  2044:         let ptr = self.as_ptr();\n  2045: \n  2046:         assert_unsafe_precondition!(\n  2047:             check_library_ub,\n  2048:             \"slice::split_at_unchecked requires the index to be within the slice\",\n  2049:             (mid: usize = mid, len: usize = len) => mid <= len,\n  2050:         );\n  2051: \n  2052:         // SAFETY: Caller has to check that `0 <= mid <= self.len()`\n  2053:         unsafe { (from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))) }\n  2054:     }",
    "nanvix_source": "  2031:     ///     let (left, right) = v.split_at_unchecked(3);\n  2032:     ///     assert_eq!(left, ['a', 'b', 'c']);\n  2033:     ///     assert_eq!(right, []);\n  2034:     /// }\n  2035:     /// ```\n  2036:     #[stable(feature = \"slice_split_at_unchecked\", since = \"1.79.0\")]\n  2037:     #[rustc_const_stable(feature = \"const_slice_split_at_unchecked\", since = \"1.77.0\")]\n  2038:     #[inline]\n  2039:     #[must_use]\n  2040:     #[track_caller]\n  2041:     pub const unsafe fn split_at_unchecked(&self, mid: usize) -> (&[T], &[T]) {\n  2042:         // FIXME(const-hack): the const function `from_raw_parts` is used to make this\n  2043:         // function const; previously the implementation used\n  2044:         // `(self.get_unchecked(..mid), self.get_unchecked(mid..))`\n  2045: \n  2046:         let len = self.len();\n  2047:         let ptr = self.as_ptr();\n  2048: \n  2049:         assert_unsafe_precondition!(\n  2050:             check_library_ub,\n  2051:             \"slice::split_at_unchecked requires the index to be within the slice\",",
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
