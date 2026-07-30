For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::as_chunks_mut",
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
      "name": "as_chunks_mut",
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
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "array": {
                      "len": "N",
                      "type": {
                        "generic": "T"
                      }
                    }
                  }
                }
              }
            },
            {
              "borrowed_ref": {
                "is_mutable": true,
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
    "verification_source": "  1536:     /// let v = &mut [0, 0, 0, 0, 0];\n  1537:     /// let mut count = 1;\n  1538:     ///\n  1539:     /// let (chunks, remainder) = v.as_chunks_mut();\n  1540:     /// remainder[0] = 9;\n  1541:     /// for chunk in chunks {\n  1542:     ///     *chunk = [count; 2];\n  1543:     ///     count += 1;\n  1544:     /// }\n  1545:     /// assert_eq!(v, &[1, 1, 2, 2, 9]);\n  1546:     /// ```\n  1547:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1548:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1549:     #[inline]\n  1550:     #[track_caller]\n  1551:     #[must_use]\n  1552:     pub const fn as_chunks_mut<const N: usize>(&mut self) -> (&mut [[T; N]], &mut [T]) {\n  1553:         assert!(N != 0, \"chunk size must be non-zero\");\n  1554:         let len_rounded_down = self.len() / N * N;\n  1555:         // SAFETY: The rounded-down value is always the same or smaller than the\n  1556:         // original length, and thus must be in-bounds of the slice.\n  1557:         let (multiple_of_n, remainder) = unsafe { self.split_at_mut_unchecked(len_rounded_down) };\n  1558:         // SAFETY: We already panicked for zero, and ensured by construction\n  1559:         // that the length of the subslice is a multiple of N.\n  1560:         let array_slice = unsafe { multiple_of_n.as_chunks_unchecked_mut() };\n  1561:         (array_slice, remainder)\n  1562:     }\n  1563: \n  1564:     /// Splits the slice into a slice of `N`-element arrays,\n  1565:     /// starting at the end of the slice,\n  1566:     /// and a remainder slice with length strictly less than `N`.\n  1567:     ///\n  1568:     /// The remainder is meaningful in the division sense.  Given",
    "nanvix_source": "  1545:     ///     *chunk = [count; 2];\n  1546:     ///     count += 1;\n  1547:     /// }\n  1548:     /// assert_eq!(v, &[1, 1, 2, 2, 9]);\n  1549:     /// ```\n  1550:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1551:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1552:     #[inline]\n  1553:     #[track_caller]\n  1554:     #[must_use]\n  1555:     pub const fn as_chunks_mut<const N: usize>(&mut self) -> (&mut [[T; N]], &mut [T]) {\n  1556:         assert!(N != 0, \"chunk size must be non-zero\");\n  1557:         let len_rounded_down = self.len() / N * N;\n  1558:         // SAFETY: The rounded-down value is always the same or smaller than the\n  1559:         // original length, and thus must be in-bounds of the slice.\n  1560:         let (multiple_of_n, remainder) = unsafe { self.split_at_mut_unchecked(len_rounded_down) };\n  1561:         // SAFETY: We already panicked for zero, and ensured by construction\n  1562:         // that the length of the subslice is a multiple of N.\n  1563:         let array_slice = unsafe { multiple_of_n.as_chunks_unchecked_mut() };\n  1564:         (array_slice, remainder)\n  1565:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_chunks_unchecked_mut",
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
      "name": "as_chunks_unchecked_mut",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "array": {
                  "len": "N",
                  "type": {
                    "generic": "T"
                  }
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "  1482:     /// assert_eq!(chunks, &[['L'], ['o'], ['r'], ['e'], ['m'], ['!']]);\n  1483:     /// let chunks: &mut [[char; 3]] =\n  1484:     ///     // SAFETY: The slice length (6) is a multiple of 3\n  1485:     ///     unsafe { slice.as_chunks_unchecked_mut() };\n  1486:     /// chunks[1] = ['a', 'x', '?'];\n  1487:     /// assert_eq!(slice, &['L', 'o', 'r', 'a', 'x', '?']);\n  1488:     ///\n  1489:     /// // These would be unsound:\n  1490:     /// // let chunks: &[[_; 5]] = slice.as_chunks_unchecked_mut() // The slice length is not a multiple of 5\n  1491:     /// // let chunks: &[[_; 0]] = slice.as_chunks_unchecked_mut() // Zero-length chunks are never allowed\n  1492:     /// ```\n  1493:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1494:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1495:     #[inline]\n  1496:     #[must_use]\n  1497:     #[track_caller]\n  1498:     pub const unsafe fn as_chunks_unchecked_mut<const N: usize>(&mut self) -> &mut [[T; N]] {\n  1499:         assert_unsafe_precondition!(\n  1500:             check_language_ub,\n  1501:             \"slice::as_chunks_unchecked requires `N != 0` and the slice to split exactly into `N`-element chunks\",\n  1502:             (n: usize = N, len: usize = self.len()) => n != 0 && len.is_multiple_of(n)\n  1503:         );\n  1504:         // SAFETY: Caller must guarantee that `N` is nonzero and exactly divides the slice length\n  1505:         let new_len = unsafe { exact_div(self.len(), N) };\n  1506:         // SAFETY: We cast a slice of `new_len * N` elements into\n  1507:         // a slice of `new_len` many `N` elements chunks.\n  1508:         unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), new_len) }\n  1509:     }\n  1510: \n  1511:     /// Splits the slice into a slice of `N`-element arrays,\n  1512:     /// starting at the beginning of the slice,\n  1513:     /// and a remainder slice with length strictly less than `N`.\n  1514:     ///",
    "nanvix_source": "  1491:     ///\n  1492:     /// // These would be unsound:\n  1493:     /// // let chunks: &[[_; 5]] = slice.as_chunks_unchecked_mut() // The slice length is not a multiple of 5\n  1494:     /// // let chunks: &[[_; 0]] = slice.as_chunks_unchecked_mut() // Zero-length chunks are never allowed\n  1495:     /// ```\n  1496:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1497:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1498:     #[inline]\n  1499:     #[must_use]\n  1500:     #[track_caller]\n  1501:     pub const unsafe fn as_chunks_unchecked_mut<const N: usize>(&mut self) -> &mut [[T; N]] {\n  1502:         assert_unsafe_precondition!(\n  1503:             check_language_ub,\n  1504:             \"slice::as_chunks_unchecked requires `N != 0` and the slice to split exactly into `N`-element chunks\",\n  1505:             (n: usize = N, len: usize = self.len()) => n != 0 && len.is_multiple_of(n)\n  1506:         );\n  1507:         // SAFETY: Caller must guarantee that `N` is nonzero and exactly divides the slice length\n  1508:         let new_len = unsafe { exact_div(self.len(), N) };\n  1509:         // SAFETY: We cast a slice of `new_len * N` elements into\n  1510:         // a slice of `new_len` many `N` elements chunks.\n  1511:         unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), new_len) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_flattened_mut",
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
      "name": "as_flattened_mut",
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
          "slice": {
            "array": {
              "len": "N",
              "type": {
                "generic": "T"
              }
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
            },
            {
              "kind": {
                "const": {
                  "default": null,
                  "type": {
                    "primitive": "usize"
                  }
                }
              },
              "name": "N"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51880",
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
          "borrowed_ref": {
            "is_mutable": true,
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
    "verification_source": "  5471:     ///\n  5472:     /// # Examples\n  5473:     ///\n  5474:     /// ```\n  5475:     /// fn add_5_to_all(slice: &mut [i32]) {\n  5476:     ///     for i in slice {\n  5477:     ///         *i += 5;\n  5478:     ///     }\n  5479:     /// }\n  5480:     ///\n  5481:     /// let mut array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];\n  5482:     /// add_5_to_all(array.as_flattened_mut());\n  5483:     /// assert_eq!(array, [[6, 7, 8], [9, 10, 11], [12, 13, 14]]);\n  5484:     /// ```\n  5485:     #[stable(feature = \"slice_flatten\", since = \"1.80.0\")]\n  5486:     #[rustc_const_stable(feature = \"const_slice_flatten\", since = \"1.87.0\")]\n  5487:     pub const fn as_flattened_mut(&mut self) -> &mut [T] {\n  5488:         let len = if T::IS_ZST {\n  5489:             self.len().checked_mul(N).expect(\"slice len overflow\")\n  5490:         } else {\n  5491:             // SAFETY: `self.len() * N` cannot overflow because `self` is\n  5492:             // already in the address space.\n  5493:             unsafe { self.len().unchecked_mul(N) }\n  5494:         };\n  5495:         // SAFETY: `[T]` is layout-identical to `[T; N]`\n  5496:         unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), len) }\n  5497:     }\n  5498: }\n  5499: \n  5500: impl [f32] {\n  5501:     /// Sorts the slice of floats.\n  5502:     ///\n  5503:     /// This sort is in-place (i.e. does not allocate), *O*(*n* \\* log(*n*)) worst-case, and uses",
    "nanvix_source": "  5483:     ///         *i += 5;\n  5484:     ///     }\n  5485:     /// }\n  5486:     ///\n  5487:     /// let mut array = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];\n  5488:     /// add_5_to_all(array.as_flattened_mut());\n  5489:     /// assert_eq!(array, [[6, 7, 8], [9, 10, 11], [12, 13, 14]]);\n  5490:     /// ```\n  5491:     #[stable(feature = \"slice_flatten\", since = \"1.80.0\")]\n  5492:     #[rustc_const_stable(feature = \"const_slice_flatten\", since = \"1.87.0\")]\n  5493:     pub const fn as_flattened_mut(&mut self) -> &mut [T] {\n  5494:         let len = if T::IS_ZST {\n  5495:             self.len().checked_mul(N).expect(\"slice len overflow\")\n  5496:         } else {\n  5497:             // SAFETY: `self.len() * N` cannot overflow because `self` is\n  5498:             // already in the address space.\n  5499:             unsafe { self.len().unchecked_mul(N) }\n  5500:         };\n  5501:         // SAFETY: `[T]` is layout-identical to `[T; N]`\n  5502:         unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), len) }\n  5503:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_mut_array",
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
      "name": "as_mut_array",
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
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "array": {
                            "len": "N",
                            "type": {
                              "generic": "T"
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
    "verification_source": "   853: \n   854:             // SAFETY: The underlying array of a slice can be reinterpreted as an actual array `[T; N]` if `N` is not greater than the slice's length.\n   855:             let me = unsafe { &*ptr };\n   856:             Some(me)\n   857:         } else {\n   858:             None\n   859:         }\n   860:     }\n   861: \n   862:     /// Gets a mutable reference to the slice's underlying array.\n   863:     ///\n   864:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n   865:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   866:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   867:     #[inline]\n   868:     #[must_use]\n   869:     pub const fn as_mut_array<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   870:         if self.len() == N {\n   871:             let ptr = self.as_mut_ptr().cast_array();\n   872: \n   873:             // SAFETY: The underlying array of a slice can be reinterpreted as an actual array `[T; N]` if `N` is not greater than the slice's length.\n   874:             let me = unsafe { &mut *ptr };\n   875:             Some(me)\n   876:         } else {\n   877:             None\n   878:         }\n   879:     }\n   880: \n   881:     /// Swaps two elements in the slice.\n   882:     ///\n   883:     /// If `a` equals to `b`, it's guaranteed that elements won't change value.\n   884:     ///\n   885:     /// # Arguments",
    "nanvix_source": "   862:         }\n   863:     }\n   864: \n   865:     /// Gets a mutable reference to the slice's underlying array.\n   866:     ///\n   867:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n   868:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   869:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   870:     #[inline]\n   871:     #[must_use]\n   872:     pub const fn as_mut_array<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   873:         if self.len() == N {\n   874:             let ptr = self.as_mut_ptr().cast_array();\n   875: \n   876:             // SAFETY: The underlying array of a slice can be reinterpreted as an actual array `[T; N]` if `N` is not greater than the slice's length.\n   877:             let me = unsafe { &mut *ptr };\n   878:             Some(me)\n   879:         } else {\n   880:             None\n   881:         }\n   882:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_rchunks_mut",
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
      "name": "as_rchunks_mut",
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
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": true,
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "array": {
                      "len": "N",
                      "type": {
                        "generic": "T"
                      }
                    }
                  }
                }
              }
            }
          ]
        }
      }
    },
    "verification_source": "  1589:     /// let v = &mut [0, 0, 0, 0, 0];\n  1590:     /// let mut count = 1;\n  1591:     ///\n  1592:     /// let (remainder, chunks) = v.as_rchunks_mut();\n  1593:     /// remainder[0] = 9;\n  1594:     /// for chunk in chunks {\n  1595:     ///     *chunk = [count; 2];\n  1596:     ///     count += 1;\n  1597:     /// }\n  1598:     /// assert_eq!(v, &[9, 1, 1, 2, 2]);\n  1599:     /// ```\n  1600:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1601:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1602:     #[inline]\n  1603:     #[track_caller]\n  1604:     #[must_use]\n  1605:     pub const fn as_rchunks_mut<const N: usize>(&mut self) -> (&mut [T], &mut [[T; N]]) {\n  1606:         assert!(N != 0, \"chunk size must be non-zero\");\n  1607:         let len = self.len() / N;\n  1608:         let (remainder, multiple_of_n) = self.split_at_mut(self.len() - len * N);\n  1609:         // SAFETY: We already panicked for zero, and ensured by construction\n  1610:         // that the length of the subslice is a multiple of N.\n  1611:         let array_slice = unsafe { multiple_of_n.as_chunks_unchecked_mut() };\n  1612:         (remainder, array_slice)\n  1613:     }\n  1614: \n  1615:     /// Returns an iterator over overlapping windows of `N` elements of a slice,\n  1616:     /// starting at the beginning of the slice.\n  1617:     ///\n  1618:     /// This is the const generic equivalent of [`windows`].\n  1619:     ///\n  1620:     /// If `N` is greater than the size of the slice, it will return no windows.\n  1621:     ///",
    "nanvix_source": "  1598:     ///     *chunk = [count; 2];\n  1599:     ///     count += 1;\n  1600:     /// }\n  1601:     /// assert_eq!(v, &[9, 1, 1, 2, 2]);\n  1602:     /// ```\n  1603:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1604:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1605:     #[inline]\n  1606:     #[track_caller]\n  1607:     #[must_use]\n  1608:     pub const fn as_rchunks_mut<const N: usize>(&mut self) -> (&mut [T], &mut [[T; N]]) {\n  1609:         assert!(N != 0, \"chunk size must be non-zero\");\n  1610:         let len = self.len() / N;\n  1611:         let (remainder, multiple_of_n) = self.split_at_mut(self.len() - len * N);\n  1612:         // SAFETY: We already panicked for zero, and ensured by construction\n  1613:         // that the length of the subslice is a multiple of N.\n  1614:         let array_slice = unsafe { multiple_of_n.as_chunks_unchecked_mut() };\n  1615:         (remainder, array_slice)\n  1616:     }\n  1617: \n  1618:     /// Returns an iterator over overlapping windows of `N` elements of a slice,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::assume_init_mut",
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
        "is_unsafe": true
      },
      "name": "assume_init_mut",
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
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
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
    "verification_source": "  1511:         // The pointer obtained is valid since it refers to memory owned by `slice` which is a\n  1512:         // reference and thus guaranteed to be valid for reads.\n  1513:         unsafe { &*(self as *const Self as *const [T]) }\n  1514:     }\n  1515: \n  1516:     /// Gets a mutable (unique) reference to the contained value.\n  1517:     ///\n  1518:     /// # Safety\n  1519:     ///\n  1520:     /// Calling this when the content is not yet fully initialized causes undefined\n  1521:     /// behavior: it is up to the caller to guarantee that every `MaybeUninit<T>` in the\n  1522:     /// slice really is in an initialized state. For instance, `.assume_init_mut()` cannot\n  1523:     /// be used to initialize a `MaybeUninit` slice.\n  1524:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1525:     #[rustc_const_stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1526:     #[inline(always)]\n  1527:     pub const unsafe fn assume_init_mut(&mut self) -> &mut [T] {\n  1528:         // SAFETY: similar to safety notes for `slice_get_ref`, but we have a\n  1529:         // mutable reference which is also guaranteed to be valid for writes.\n  1530:         unsafe { &mut *(self as *mut Self as *mut [T]) }\n  1531:     }\n  1532: }\n  1533: \n  1534: impl<T, const N: usize> MaybeUninit<[T; N]> {\n  1535:     /// Transposes a `MaybeUninit<[T; N]>` into a `[MaybeUninit<T>; N]`.\n  1536:     ///\n  1537:     /// # Examples\n  1538:     ///\n  1539:     /// ```\n  1540:     /// #![feature(maybe_uninit_uninit_array_transpose)]\n  1541:     /// # use std::mem::MaybeUninit;\n  1542:     ///\n  1543:     /// let data: [MaybeUninit<u8>; 1000] = MaybeUninit::uninit().transpose();",
    "nanvix_source": "  1518:     ///\n  1519:     /// # Safety\n  1520:     ///\n  1521:     /// Calling this when the content is not yet fully initialized causes undefined\n  1522:     /// behavior: it is up to the caller to guarantee that every `MaybeUninit<T>` in the\n  1523:     /// slice really is in an initialized state. For instance, `.assume_init_mut()` cannot\n  1524:     /// be used to initialize a `MaybeUninit` slice.\n  1525:     #[stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1526:     #[rustc_const_stable(feature = \"maybe_uninit_slice\", since = \"1.93.0\")]\n  1527:     #[inline(always)]\n  1528:     pub const unsafe fn assume_init_mut(&mut self) -> &mut [T] {\n  1529:         // SAFETY: similar to safety notes for `slice_get_ref`, but we have a\n  1530:         // mutable reference which is also guaranteed to be valid for writes.\n  1531:         unsafe { &mut *(self as *mut Self as *mut [T]) }\n  1532:     }\n  1533: }\n  1534: \n  1535: impl<T, const N: usize> MaybeUninit<[T; N]> {\n  1536:     /// Transposes a `MaybeUninit<[T; N]>` into a `[MaybeUninit<T>; N]`.\n  1537:     ///\n  1538:     /// # Examples",
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
