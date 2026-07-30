For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::split_at_mut_unchecked",
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
      "name": "split_at_mut_unchecked",
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
                    "generic": "T"
                  }
                }
              }
            }
          ]
        }
      }
    },
    "verification_source": "  2076:     /// let mut v = [1, 0, 3, 0, 5, 6];\n  2077:     /// // scoped to restrict the lifetime of the borrows\n  2078:     /// unsafe {\n  2079:     ///     let (left, right) = v.split_at_mut_unchecked(2);\n  2080:     ///     assert_eq!(left, [1, 0]);\n  2081:     ///     assert_eq!(right, [3, 0, 5, 6]);\n  2082:     ///     left[1] = 2;\n  2083:     ///     right[1] = 4;\n  2084:     /// }\n  2085:     /// assert_eq!(v, [1, 2, 3, 4, 5, 6]);\n  2086:     /// ```\n  2087:     #[stable(feature = \"slice_split_at_unchecked\", since = \"1.79.0\")]\n  2088:     #[rustc_const_stable(feature = \"const_slice_split_at_mut\", since = \"1.83.0\")]\n  2089:     #[inline]\n  2090:     #[must_use]\n  2091:     #[track_caller]\n  2092:     pub const unsafe fn split_at_mut_unchecked(&mut self, mid: usize) -> (&mut [T], &mut [T]) {\n  2093:         let len = self.len();\n  2094:         let ptr = self.as_mut_ptr();\n  2095: \n  2096:         assert_unsafe_precondition!(\n  2097:             check_library_ub,\n  2098:             \"slice::split_at_mut_unchecked requires the index to be within the slice\",\n  2099:             (mid: usize = mid, len: usize = len) => mid <= len,\n  2100:         );\n  2101: \n  2102:         // SAFETY: Caller has to check that `0 <= mid <= self.len()`.\n  2103:         //\n  2104:         // `[ptr; mid]` and `[mid; len]` are not overlapping, so returning a mutable reference\n  2105:         // is fine.\n  2106:         unsafe {\n  2107:             (\n  2108:                 from_raw_parts_mut(ptr, mid),",
    "nanvix_source": "  2085:     ///     left[1] = 2;\n  2086:     ///     right[1] = 4;\n  2087:     /// }\n  2088:     /// assert_eq!(v, [1, 2, 3, 4, 5, 6]);\n  2089:     /// ```\n  2090:     #[stable(feature = \"slice_split_at_unchecked\", since = \"1.79.0\")]\n  2091:     #[rustc_const_stable(feature = \"const_slice_split_at_mut\", since = \"1.83.0\")]\n  2092:     #[inline]\n  2093:     #[must_use]\n  2094:     #[track_caller]\n  2095:     pub const unsafe fn split_at_mut_unchecked(&mut self, mid: usize) -> (&mut [T], &mut [T]) {\n  2096:         let len = self.len();\n  2097:         let ptr = self.as_mut_ptr();\n  2098: \n  2099:         assert_unsafe_precondition!(\n  2100:             check_library_ub,\n  2101:             \"slice::split_at_mut_unchecked requires the index to be within the slice\",\n  2102:             (mid: usize = mid, len: usize = len) => mid <= len,\n  2103:         );\n  2104: \n  2105:         // SAFETY: Caller has to check that `0 <= mid <= self.len()`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_first_chunk_mut",
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
      "name": "split_first_chunk_mut",
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
                      "tuple": [
                        {
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
    "verification_source": "   401:     ///\n   402:     /// ```\n   403:     /// let x = &mut [0, 1, 2];\n   404:     ///\n   405:     /// if let Some((first, elements)) = x.split_first_chunk_mut::<2>() {\n   406:     ///     first[0] = 3;\n   407:     ///     first[1] = 4;\n   408:     ///     elements[0] = 5;\n   409:     /// }\n   410:     /// assert_eq!(x, &[3, 4, 5]);\n   411:     ///\n   412:     /// assert_eq!(None, x.split_first_chunk_mut::<4>());\n   413:     /// ```\n   414:     #[inline]\n   415:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   416:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   417:     pub const fn split_first_chunk_mut<const N: usize>(\n   418:         &mut self,\n   419:     ) -> Option<(&mut [T; N], &mut [T])> {\n   420:         let Some((first, tail)) = self.split_at_mut_checked(N) else { return None };\n   421: \n   422:         // SAFETY: We explicitly check for the correct number of elements,\n   423:         //   do not let the reference outlive the slice,\n   424:         //   and enforce exclusive mutability of the chunk by the split.\n   425:         Some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))\n   426:     }\n   427: \n   428:     /// Returns an array reference to the last `N` items in the slice and the remaining slice.\n   429:     ///\n   430:     /// If the slice is not at least `N` in length, this will return `None`.\n   431:     ///\n   432:     /// # Examples\n   433:     ///",
    "nanvix_source": "   407:     ///     first[1] = 4;\n   408:     ///     elements[0] = 5;\n   409:     /// }\n   410:     /// assert_eq!(x, &[3, 4, 5]);\n   411:     ///\n   412:     /// assert_eq!(None, x.split_first_chunk_mut::<4>());\n   413:     /// ```\n   414:     #[inline]\n   415:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   416:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   417:     pub const fn split_first_chunk_mut<const N: usize>(\n   418:         &mut self,\n   419:     ) -> Option<(&mut [T; N], &mut [T])> {\n   420:         let Some((first, tail)) = self.split_at_mut_checked(N) else { return None };\n   421: \n   422:         // SAFETY: We explicitly check for the correct number of elements,\n   423:         //   do not let the reference outlive the slice,\n   424:         //   and enforce exclusive mutability of the chunk by the split.\n   425:         Some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))\n   426:     }\n   427: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_first_mut",
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
      "name": "split_first_mut",
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "generic": "T"
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
    "verification_source": "   204:     /// # Examples\n   205:     ///\n   206:     /// ```\n   207:     /// let x = &mut [0, 1, 2];\n   208:     ///\n   209:     /// if let Some((first, elements)) = x.split_first_mut() {\n   210:     ///     *first = 3;\n   211:     ///     elements[0] = 4;\n   212:     ///     elements[1] = 5;\n   213:     /// }\n   214:     /// assert_eq!(x, &[3, 4, 5]);\n   215:     /// ```\n   216:     #[stable(feature = \"slice_splits\", since = \"1.5.0\")]\n   217:     #[rustc_const_stable(feature = \"const_slice_first_last\", since = \"1.83.0\")]\n   218:     #[inline]\n   219:     #[must_use]\n   220:     pub const fn split_first_mut(&mut self) -> Option<(&mut T, &mut [T])> {\n   221:         if let [first, tail @ ..] = self { Some((first, tail)) } else { None }\n   222:     }\n   223: \n   224:     /// Returns the last and all the rest of the elements of the slice, or `None` if it is empty.\n   225:     ///\n   226:     /// # Examples\n   227:     ///\n   228:     /// ```\n   229:     /// let x = &[0, 1, 2];\n   230:     ///\n   231:     /// if let Some((last, elements)) = x.split_last() {\n   232:     ///     assert_eq!(last, &2);\n   233:     ///     assert_eq!(elements, &[0, 1]);\n   234:     /// }\n   235:     /// ```\n   236:     #[stable(feature = \"slice_splits\", since = \"1.5.0\")]",
    "nanvix_source": "   210:     ///     *first = 3;\n   211:     ///     elements[0] = 4;\n   212:     ///     elements[1] = 5;\n   213:     /// }\n   214:     /// assert_eq!(x, &[3, 4, 5]);\n   215:     /// ```\n   216:     #[stable(feature = \"slice_splits\", since = \"1.5.0\")]\n   217:     #[rustc_const_stable(feature = \"const_slice_first_last\", since = \"1.83.0\")]\n   218:     #[inline]\n   219:     #[must_use]\n   220:     pub const fn split_first_mut(&mut self) -> Option<(&mut T, &mut [T])> {\n   221:         if let [first, tail @ ..] = self { Some((first, tail)) } else { None }\n   222:     }\n   223: \n   224:     /// Returns the last and all the rest of the elements of the slice, or `None` if it is empty.\n   225:     ///\n   226:     /// # Examples\n   227:     ///\n   228:     /// ```\n   229:     /// let x = &[0, 1, 2];\n   230:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_last_chunk_mut",
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
      "name": "split_last_chunk_mut",
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
                              "array": {
                                "len": "N",
                                "type": {
                                  "generic": "T"
                                }
                              }
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
    "verification_source": "   462:     ///\n   463:     /// ```\n   464:     /// let x = &mut [0, 1, 2];\n   465:     ///\n   466:     /// if let Some((elements, last)) = x.split_last_chunk_mut::<2>() {\n   467:     ///     last[0] = 3;\n   468:     ///     last[1] = 4;\n   469:     ///     elements[0] = 5;\n   470:     /// }\n   471:     /// assert_eq!(x, &[5, 3, 4]);\n   472:     ///\n   473:     /// assert_eq!(None, x.split_last_chunk_mut::<4>());\n   474:     /// ```\n   475:     #[inline]\n   476:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   477:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   478:     pub const fn split_last_chunk_mut<const N: usize>(\n   479:         &mut self,\n   480:     ) -> Option<(&mut [T], &mut [T; N])> {\n   481:         let Some(index) = self.len().checked_sub(N) else { return None };\n   482:         let (init, last) = self.split_at_mut(index);\n   483: \n   484:         // SAFETY: We explicitly check for the correct number of elements,\n   485:         //   do not let the reference outlive the slice,\n   486:         //   and enforce exclusive mutability of the chunk by the split.\n   487:         Some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))\n   488:     }\n   489: \n   490:     /// Returns an array reference to the last `N` items in the slice.\n   491:     ///\n   492:     /// If the slice is not at least `N` in length, this will return `None`.\n   493:     ///\n   494:     /// # Examples",
    "nanvix_source": "   468:     ///     last[1] = 4;\n   469:     ///     elements[0] = 5;\n   470:     /// }\n   471:     /// assert_eq!(x, &[5, 3, 4]);\n   472:     ///\n   473:     /// assert_eq!(None, x.split_last_chunk_mut::<4>());\n   474:     /// ```\n   475:     #[inline]\n   476:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   477:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   478:     pub const fn split_last_chunk_mut<const N: usize>(\n   479:         &mut self,\n   480:     ) -> Option<(&mut [T], &mut [T; N])> {\n   481:         let Some(index) = self.len().checked_sub(N) else { return None };\n   482:         let (init, last) = self.split_at_mut(index);\n   483: \n   484:         // SAFETY: We explicitly check for the correct number of elements,\n   485:         //   do not let the reference outlive the slice,\n   486:         //   and enforce exclusive mutability of the chunk by the split.\n   487:         Some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))\n   488:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_last_mut",
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
      "name": "split_last_mut",
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "generic": "T"
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
    "verification_source": "   246:     /// # Examples\n   247:     ///\n   248:     /// ```\n   249:     /// let x = &mut [0, 1, 2];\n   250:     ///\n   251:     /// if let Some((last, elements)) = x.split_last_mut() {\n   252:     ///     *last = 3;\n   253:     ///     elements[0] = 4;\n   254:     ///     elements[1] = 5;\n   255:     /// }\n   256:     /// assert_eq!(x, &[4, 5, 3]);\n   257:     /// ```\n   258:     #[stable(feature = \"slice_splits\", since = \"1.5.0\")]\n   259:     #[rustc_const_stable(feature = \"const_slice_first_last\", since = \"1.83.0\")]\n   260:     #[inline]\n   261:     #[must_use]\n   262:     pub const fn split_last_mut(&mut self) -> Option<(&mut T, &mut [T])> {\n   263:         if let [init @ .., last] = self { Some((last, init)) } else { None }\n   264:     }\n   265: \n   266:     /// Returns the last element of the slice, or `None` if it is empty.\n   267:     ///\n   268:     /// # Examples\n   269:     ///\n   270:     /// ```\n   271:     /// let v = [10, 40, 30];\n   272:     /// assert_eq!(Some(&30), v.last());\n   273:     ///\n   274:     /// let w: &[i32] = &[];\n   275:     /// assert_eq!(None, w.last());\n   276:     /// ```\n   277:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   278:     #[rustc_const_stable(feature = \"const_slice_first_last_not_mut\", since = \"1.56.0\")]",
    "nanvix_source": "   252:     ///     *last = 3;\n   253:     ///     elements[0] = 4;\n   254:     ///     elements[1] = 5;\n   255:     /// }\n   256:     /// assert_eq!(x, &[4, 5, 3]);\n   257:     /// ```\n   258:     #[stable(feature = \"slice_splits\", since = \"1.5.0\")]\n   259:     #[rustc_const_stable(feature = \"const_slice_first_last\", since = \"1.83.0\")]\n   260:     #[inline]\n   261:     #[must_use]\n   262:     pub const fn split_last_mut(&mut self) -> Option<(&mut T, &mut [T])> {\n   263:         if let [init @ .., last] = self { Some((last, init)) } else { None }\n   264:     }\n   265: \n   266:     /// Returns the last element of the slice, or `None` if it is empty.\n   267:     ///\n   268:     /// # Examples\n   269:     ///\n   270:     /// ```\n   271:     /// let v = [10, 40, 30];\n   272:     /// assert_eq!(Some(&30), v.last());",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_off_first_mut",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
      "name": "split_off_first_mut",
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
                  "borrowed_ref": {
                    "is_mutable": true,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
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
                        "is_mutable": true,
                        "lifetime": "'a",
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
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  5019:     ///\n  5020:     /// Returns `None` if the slice is empty.\n  5021:     ///\n  5022:     /// # Examples\n  5023:     ///\n  5024:     /// ```\n  5025:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5026:     /// let first = slice.split_off_first_mut().unwrap();\n  5027:     /// *first = 'd';\n  5028:     ///\n  5029:     /// assert_eq!(slice, &['b', 'c']);\n  5030:     /// assert_eq!(first, &'d');\n  5031:     /// ```\n  5032:     #[inline]\n  5033:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5034:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5035:     pub const fn split_off_first_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {\n  5036:         // FIXME(const-hack): Use `mem::take` and `?` when available in const.\n  5037:         // Original: `mem::take(self).split_first_mut()?`\n  5038:         let Some((first, rem)) = mem::replace(self, &mut []).split_first_mut() else { return None };\n  5039:         *self = rem;\n  5040:         Some(first)\n  5041:     }\n  5042: \n  5043:     /// Removes the last element of the slice and returns a reference\n  5044:     /// to it.\n  5045:     ///\n  5046:     /// Returns `None` if the slice is empty.\n  5047:     ///\n  5048:     /// # Examples\n  5049:     ///\n  5050:     /// ```\n  5051:     /// let mut slice: &[_] = &['a', 'b', 'c'];",
    "nanvix_source": "  5032:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5033:     /// let first = slice.split_off_first_mut().unwrap();\n  5034:     /// *first = 'd';\n  5035:     ///\n  5036:     /// assert_eq!(slice, &['b', 'c']);\n  5037:     /// assert_eq!(first, &'d');\n  5038:     /// ```\n  5039:     #[inline]\n  5040:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5041:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5042:     pub const fn split_off_first_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {\n  5043:         // FIXME(const-hack): Use `mem::take` and `?` when available in const.\n  5044:         // Original: `mem::take(self).split_first_mut()?`\n  5045:         let Some((first, rem)) = mem::replace(self, &mut []).split_first_mut() else { return None };\n  5046:         *self = rem;\n  5047:         Some(first)\n  5048:     }\n  5049: \n  5050:     /// Removes the last element of the slice and returns a reference\n  5051:     /// to it.\n  5052:     ///",
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
