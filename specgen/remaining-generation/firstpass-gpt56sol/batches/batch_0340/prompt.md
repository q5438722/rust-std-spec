For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::result::Result::unwrap_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "unwrap_unchecked",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1634:     ///\n  1635:     /// # Examples\n  1636:     ///\n  1637:     /// ```\n  1638:     /// let x: Result<u32, &str> = Ok(2);\n  1639:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, 2);\n  1640:     /// ```\n  1641:     ///\n  1642:     /// ```no_run\n  1643:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1644:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1645:     /// ```\n  1646:     #[inline]\n  1647:     #[track_caller]\n  1648:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1649:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1650:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1651:         match self {\n  1652:             Ok(t) => t,\n  1653:             Err(e) => {\n  1654:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1655:                 super::mem::forget(e);\n  1656:                 // SAFETY: the safety contract must be upheld by the caller.\n  1657:                 unsafe { hint::unreachable_unchecked() }\n  1658:             }\n  1659:         }\n  1660:     }\n  1661: \n  1662:     /// Returns the contained [`Err`] value, consuming the `self` value,\n  1663:     /// without checking that the value is not an [`Ok`].\n  1664:     ///\n  1665:     /// # Safety\n  1666:     ///",
    "nanvix_source": "  1638:     /// ```\n  1639:     ///\n  1640:     /// ```no_run\n  1641:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1642:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1647:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1648:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1649:         match self {\n  1650:             Ok(t) => t,\n  1651:             Err(e) => {\n  1652:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1653:                 super::mem::forget(e);\n  1654:                 // SAFETY: the safety contract must be upheld by the caller.\n  1655:                 unsafe { hint::unreachable_unchecked() }\n  1656:             }\n  1657:         }\n  1658:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::align_to",
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
            "name": "U"
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
      "name": "align_to",
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
                    "generic": "U"
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
    "verification_source": "  4483:     ///\n  4484:     /// # Examples\n  4485:     ///\n  4486:     /// Basic usage:\n  4487:     ///\n  4488:     /// ```\n  4489:     /// unsafe {\n  4490:     ///     let bytes: [u8; 7] = [1, 2, 3, 4, 5, 6, 7];\n  4491:     ///     let (prefix, shorts, suffix) = bytes.align_to::<u16>();\n  4492:     ///     // less_efficient_algorithm_for_bytes(prefix);\n  4493:     ///     // more_efficient_algorithm_for_aligned_shorts(shorts);\n  4494:     ///     // less_efficient_algorithm_for_bytes(suffix);\n  4495:     /// }\n  4496:     /// ```\n  4497:     #[stable(feature = \"slice_align_to\", since = \"1.30.0\")]\n  4498:     #[must_use]\n  4499:     pub unsafe fn align_to<U>(&self) -> (&[T], &[U], &[T]) {\n  4500:         // Note that most of this function will be constant-evaluated,\n  4501:         if U::IS_ZST || T::IS_ZST {\n  4502:             // handle ZSTs specially, which is \u2013 don't handle them at all.\n  4503:             return (self, &[], &[]);\n  4504:         }\n  4505: \n  4506:         // First, find at what point do we split between the first and 2nd slice. Easy with\n  4507:         // ptr.align_offset.\n  4508:         let ptr = self.as_ptr();\n  4509:         // SAFETY: See the `align_to_mut` method for the detailed safety comment.\n  4510:         let offset = unsafe { crate::ptr::align_offset(ptr, align_of::<U>()) };\n  4511:         if offset > self.len() {\n  4512:             (self, &[], &[])\n  4513:         } else {\n  4514:             let (left, rest) = self.split_at(offset);\n  4515:             let (us_len, ts_len) = rest.align_to_offsets::<U>();",
    "nanvix_source": "  4496:     /// unsafe {\n  4497:     ///     let bytes: [u8; 7] = [1, 2, 3, 4, 5, 6, 7];\n  4498:     ///     let (prefix, shorts, suffix) = bytes.align_to::<u16>();\n  4499:     ///     // less_efficient_algorithm_for_bytes(prefix);\n  4500:     ///     // more_efficient_algorithm_for_aligned_shorts(shorts);\n  4501:     ///     // less_efficient_algorithm_for_bytes(suffix);\n  4502:     /// }\n  4503:     /// ```\n  4504:     #[stable(feature = \"slice_align_to\", since = \"1.30.0\")]\n  4505:     #[must_use]\n  4506:     pub unsafe fn align_to<U>(&self) -> (&[T], &[U], &[T]) {\n  4507:         // Note that most of this function will be constant-evaluated,\n  4508:         if U::IS_ZST || T::IS_ZST {\n  4509:             // handle ZSTs specially, which is \u2013 don't handle them at all.\n  4510:             return (self, &[], &[]);\n  4511:         }\n  4512: \n  4513:         // First, find at what point do we split between the first and 2nd slice. Easy with\n  4514:         // ptr.align_offset.\n  4515:         let ptr = self.as_ptr();\n  4516:         // SAFETY: See the `align_to_mut` method for the detailed safety comment.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_chunks_unchecked",
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
      "name": "as_chunks_unchecked",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
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
    "verification_source": "  1322:     ///     unsafe { slice.as_chunks_unchecked() };\n  1323:     /// assert_eq!(chunks, &[['l'], ['o'], ['r'], ['e'], ['m'], ['!']]);\n  1324:     /// let chunks: &[[char; 3]] =\n  1325:     ///     // SAFETY: The slice length (6) is a multiple of 3\n  1326:     ///     unsafe { slice.as_chunks_unchecked() };\n  1327:     /// assert_eq!(chunks, &[['l', 'o', 'r'], ['e', 'm', '!']]);\n  1328:     ///\n  1329:     /// // These would be unsound:\n  1330:     /// // let chunks: &[[_; 5]] = slice.as_chunks_unchecked() // The slice length is not a multiple of 5\n  1331:     /// // let chunks: &[[_; 0]] = slice.as_chunks_unchecked() // Zero-length chunks are never allowed\n  1332:     /// ```\n  1333:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1334:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1335:     #[inline]\n  1336:     #[must_use]\n  1337:     #[track_caller]\n  1338:     pub const unsafe fn as_chunks_unchecked<const N: usize>(&self) -> &[[T; N]] {\n  1339:         assert_unsafe_precondition!(\n  1340:             check_language_ub,\n  1341:             \"slice::as_chunks_unchecked requires `N != 0` and the slice to split exactly into `N`-element chunks\",\n  1342:             (n: usize = N, len: usize = self.len()) => n != 0 && len.is_multiple_of(n),\n  1343:         );\n  1344:         // SAFETY: Caller must guarantee that `N` is nonzero and exactly divides the slice length\n  1345:         let new_len = unsafe { exact_div(self.len(), N) };\n  1346:         // SAFETY: We cast a slice of `new_len * N` elements into\n  1347:         // a slice of `new_len` many `N` elements chunks.\n  1348:         unsafe { from_raw_parts(self.as_ptr().cast(), new_len) }\n  1349:     }\n  1350: \n  1351:     /// Splits the slice into a slice of `N`-element arrays,\n  1352:     /// starting at the beginning of the slice,\n  1353:     /// and a remainder slice with length strictly less than `N`.\n  1354:     ///",
    "nanvix_source": "  1331:     ///\n  1332:     /// // These would be unsound:\n  1333:     /// // let chunks: &[[_; 5]] = slice.as_chunks_unchecked() // The slice length is not a multiple of 5\n  1334:     /// // let chunks: &[[_; 0]] = slice.as_chunks_unchecked() // Zero-length chunks are never allowed\n  1335:     /// ```\n  1336:     #[stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1337:     #[rustc_const_stable(feature = \"slice_as_chunks\", since = \"1.88.0\")]\n  1338:     #[inline]\n  1339:     #[must_use]\n  1340:     #[track_caller]\n  1341:     pub const unsafe fn as_chunks_unchecked<const N: usize>(&self) -> &[[T; N]] {\n  1342:         assert_unsafe_precondition!(\n  1343:             check_language_ub,\n  1344:             \"slice::as_chunks_unchecked requires `N != 0` and the slice to split exactly into `N`-element chunks\",\n  1345:             (n: usize = N, len: usize = self.len()) => n != 0 && len.is_multiple_of(n),\n  1346:         );\n  1347:         // SAFETY: Caller must guarantee that `N` is nonzero and exactly divides the slice length\n  1348:         let new_len = unsafe { exact_div(self.len(), N) };\n  1349:         // SAFETY: We cast a slice of `new_len * N` elements into\n  1350:         // a slice of `new_len` many `N` elements chunks.\n  1351:         unsafe { from_raw_parts(self.as_ptr().cast(), new_len) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_mut_ptr",
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   741:     /// let x = &mut [1, 2, 4];\n   742:     /// let x_ptr = x.as_mut_ptr();\n   743:     ///\n   744:     /// unsafe {\n   745:     ///     for i in 0..x.len() {\n   746:     ///         *x_ptr.add(i) += 2;\n   747:     ///     }\n   748:     /// }\n   749:     /// assert_eq!(x, &[3, 4, 6]);\n   750:     /// ```\n   751:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   752:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   753:     #[rustc_never_returns_null_ptr]\n   754:     #[rustc_as_ptr]\n   755:     #[inline(always)]\n   756:     #[must_use]\n   757:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n   758:         self as *mut [T] as *mut T\n   759:     }\n   760: \n   761:     /// Returns the two raw pointers spanning the slice.\n   762:     ///\n   763:     /// The returned range is half-open, which means that the end pointer\n   764:     /// points *one past* the last element of the slice. This way, an empty\n   765:     /// slice is represented by two equal pointers, and the difference between\n   766:     /// the two pointers represents the size of the slice.\n   767:     ///\n   768:     /// See [`as_ptr`] for warnings on using these pointers. The end pointer\n   769:     /// requires extra caution, as it does not point to a valid element in the\n   770:     /// slice.\n   771:     ///\n   772:     /// This function is useful for interacting with foreign interfaces which\n   773:     /// use two pointers to refer to a range of elements in memory, as is",
    "nanvix_source": "   750:     /// }\n   751:     /// assert_eq!(x, &[3, 4, 6]);\n   752:     /// ```\n   753:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   754:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   755:     #[rustc_never_returns_null_ptr]\n   756:     #[rustc_as_ptr]\n   757:     #[inline(always)]\n   758:     #[must_use]\n   759:     #[rustc_no_writable]\n   760:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n   761:         self as *mut [T] as *mut T\n   762:     }\n   763: \n   764:     /// Returns the two raw pointers spanning the slice.\n   765:     ///\n   766:     /// The returned range is half-open, which means that the end pointer\n   767:     /// points *one past* the last element of the slice. This way, an empty\n   768:     /// slice is represented by two equal pointers, and the difference between\n   769:     /// the two pointers represents the size of the slice.\n   770:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_mut_ptr_range",
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
      "name": "as_mut_ptr_range",
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
                      "raw_pointer": {
                        "is_mutable": true,
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
    "verification_source": "   820:     /// slice is represented by two equal pointers, and the difference between\n   821:     /// the two pointers represents the size of the slice.\n   822:     ///\n   823:     /// See [`as_mut_ptr`] for warnings on using these pointers. The end\n   824:     /// pointer requires extra caution, as it does not point to a valid element\n   825:     /// in the slice.\n   826:     ///\n   827:     /// This function is useful for interacting with foreign interfaces which\n   828:     /// use two pointers to refer to a range of elements in memory, as is\n   829:     /// common in C++.\n   830:     ///\n   831:     /// [`as_mut_ptr`]: slice::as_mut_ptr\n   832:     #[stable(feature = \"slice_ptr_range\", since = \"1.48.0\")]\n   833:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   834:     #[inline]\n   835:     #[must_use]\n   836:     pub const fn as_mut_ptr_range(&mut self) -> Range<*mut T> {\n   837:         let start = self.as_mut_ptr();\n   838:         // SAFETY: See as_ptr_range() above for why `add` here is safe.\n   839:         let end = unsafe { start.add(self.len()) };\n   840:         start..end\n   841:     }\n   842: \n   843:     /// Gets a reference to the underlying array.\n   844:     ///\n   845:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n   846:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   847:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n   848:     #[inline]\n   849:     #[must_use]\n   850:     pub const fn as_array<const N: usize>(&self) -> Option<&[T; N]> {\n   851:         if self.len() == N {\n   852:             let ptr = self.as_ptr().cast_array();",
    "nanvix_source": "   829:     ///\n   830:     /// This function is useful for interacting with foreign interfaces which\n   831:     /// use two pointers to refer to a range of elements in memory, as is\n   832:     /// common in C++.\n   833:     ///\n   834:     /// [`as_mut_ptr`]: slice::as_mut_ptr\n   835:     #[stable(feature = \"slice_ptr_range\", since = \"1.48.0\")]\n   836:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   837:     #[inline]\n   838:     #[must_use]\n   839:     pub const fn as_mut_ptr_range(&mut self) -> Range<*mut T> {\n   840:         let start = self.as_mut_ptr();\n   841:         // SAFETY: See as_ptr_range() above for why `add` here is safe.\n   842:         let end = unsafe { start.add(self.len()) };\n   843:         start..end\n   844:     }\n   845: \n   846:     /// Gets a reference to the underlying array.\n   847:     ///\n   848:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n   849:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::as_ptr",
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   710:     /// let x_ptr = x.as_ptr();\n   711:     ///\n   712:     /// unsafe {\n   713:     ///     for i in 0..x.len() {\n   714:     ///         assert_eq!(x.get_unchecked(i), &*x_ptr.add(i));\n   715:     ///     }\n   716:     /// }\n   717:     /// ```\n   718:     ///\n   719:     /// [`as_mut_ptr`]: slice::as_mut_ptr\n   720:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   721:     #[rustc_const_stable(feature = \"const_slice_as_ptr\", since = \"1.32.0\")]\n   722:     #[rustc_never_returns_null_ptr]\n   723:     #[rustc_as_ptr]\n   724:     #[inline(always)]\n   725:     #[must_use]\n   726:     pub const fn as_ptr(&self) -> *const T {\n   727:         self as *const [T] as *const T\n   728:     }\n   729: \n   730:     /// Returns an unsafe mutable pointer to the slice's buffer.\n   731:     ///\n   732:     /// The caller must ensure that the slice outlives the pointer this\n   733:     /// function returns, or else it will end up dangling.\n   734:     ///\n   735:     /// Modifying the container referenced by this slice may cause its buffer\n   736:     /// to be reallocated, which would also make any pointers to it invalid.\n   737:     ///\n   738:     /// # Examples\n   739:     ///\n   740:     /// ```\n   741:     /// let x = &mut [1, 2, 4];\n   742:     /// let x_ptr = x.as_mut_ptr();",
    "nanvix_source": "   718:     /// }\n   719:     /// ```\n   720:     ///\n   721:     /// [`as_mut_ptr`]: slice::as_mut_ptr\n   722:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   723:     #[rustc_const_stable(feature = \"const_slice_as_ptr\", since = \"1.32.0\")]\n   724:     #[rustc_never_returns_null_ptr]\n   725:     #[rustc_as_ptr]\n   726:     #[inline(always)]\n   727:     #[must_use]\n   728:     pub const fn as_ptr(&self) -> *const T {\n   729:         self as *const [T] as *const T\n   730:     }\n   731: \n   732:     /// Returns an unsafe mutable pointer to the slice's buffer.\n   733:     ///\n   734:     /// The caller must ensure that the slice outlives the pointer this\n   735:     /// function returns, or else it will end up dangling.\n   736:     ///\n   737:     /// Modifying the container referenced by this slice may cause its buffer\n   738:     /// to be reallocated, which would also make any pointers to it invalid.",
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
