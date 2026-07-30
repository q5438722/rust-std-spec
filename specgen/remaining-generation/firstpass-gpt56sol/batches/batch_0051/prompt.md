For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::get_unchecked_mut",
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
            "index",
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
    "verification_source": "   668:     ///\n   669:     /// ```\n   670:     /// let x = &mut [1, 2, 4];\n   671:     ///\n   672:     /// unsafe {\n   673:     ///     let elem = x.get_unchecked_mut(1);\n   674:     ///     *elem = 13;\n   675:     /// }\n   676:     /// assert_eq!(x, &[1, 13, 4]);\n   677:     /// ```\n   678:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   679:     #[rustc_no_implicit_autorefs]\n   680:     #[inline]\n   681:     #[must_use]\n   682:     #[track_caller]\n   683:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   684:     pub const unsafe fn get_unchecked_mut<I>(&mut self, index: I) -> &mut I::Output\n   685:     where\n   686:         I: [const] SliceIndex<Self>,\n   687:     {\n   688:         // SAFETY: the caller must uphold the safety requirements for `get_unchecked_mut`;\n   689:         // the slice is dereferenceable because `self` is a safe reference.\n   690:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   691:         unsafe { &mut *index.get_unchecked_mut(self) }\n   692:     }\n   693: \n   694:     /// Returns a raw pointer to the slice's buffer.\n   695:     ///\n   696:     /// The caller must ensure that the slice outlives the pointer this\n   697:     /// function returns, or else it will end up dangling.\n   698:     ///\n   699:     /// The caller must also ensure that the memory the pointer (non-transitively) points to\n   700:     /// is never written to (except inside an `UnsafeCell`) using this pointer or any pointer",
    "nanvix_source": "   676:     /// }\n   677:     /// assert_eq!(x, &[1, 13, 4]);\n   678:     /// ```\n   679:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   680:     #[rustc_no_implicit_autorefs]\n   681:     #[inline]\n   682:     #[must_use]\n   683:     #[track_caller]\n   684:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   685:     #[rustc_no_writable]\n   686:     pub const unsafe fn get_unchecked_mut<I>(&mut self, index: I) -> &mut I::Output\n   687:     where\n   688:         I: [const] SliceIndex<Self>,\n   689:     {\n   690:         // SAFETY: the caller must uphold the safety requirements for `get_unchecked_mut`;\n   691:         // the slice is dereferenceable because `self` is a safe reference.\n   692:         // The returned pointer is safe because impls of `SliceIndex` have to guarantee that it is.\n   693:         unsafe { &mut *index.get_unchecked_mut(self) }\n   694:     }\n   695: \n   696:     /// Returns a raw pointer to the slice's buffer.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::last_chunk_mut",
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
      "name": "last_chunk_mut",
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
    "verification_source": "   523:     /// # Examples\n   524:     ///\n   525:     /// ```\n   526:     /// let x = &mut [0, 1, 2];\n   527:     ///\n   528:     /// if let Some(last) = x.last_chunk_mut::<2>() {\n   529:     ///     last[0] = 10;\n   530:     ///     last[1] = 20;\n   531:     /// }\n   532:     /// assert_eq!(x, &[0, 10, 20]);\n   533:     ///\n   534:     /// assert_eq!(None, x.last_chunk_mut::<4>());\n   535:     /// ```\n   536:     #[inline]\n   537:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   538:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   539:     pub const fn last_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   540:         // FIXME(const-hack): Without const traits, we need this instead of `get`.\n   541:         let Some(index) = self.len().checked_sub(N) else { return None };\n   542:         let (_, last) = self.split_at_mut(index);\n   543: \n   544:         // SAFETY: We explicitly check for the correct number of elements,\n   545:         //   do not let the reference outlive the slice,\n   546:         //   and require exclusive access to the entire slice to mutate the chunk.\n   547:         Some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })\n   548:     }\n   549: \n   550:     /// Returns a reference to an element or subslice depending on the type of\n   551:     /// index.\n   552:     ///\n   553:     /// - If given a position, returns a reference to the element at that\n   554:     ///   position or `None` if out of bounds.\n   555:     /// - If given a range, returns the subslice corresponding to that range,",
    "nanvix_source": "   529:     ///     last[0] = 10;\n   530:     ///     last[1] = 20;\n   531:     /// }\n   532:     /// assert_eq!(x, &[0, 10, 20]);\n   533:     ///\n   534:     /// assert_eq!(None, x.last_chunk_mut::<4>());\n   535:     /// ```\n   536:     #[inline]\n   537:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   538:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   539:     pub const fn last_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   540:         // FIXME(const-hack): Without const traits, we need this instead of `get`.\n   541:         let Some(index) = self.len().checked_sub(N) else { return None };\n   542:         let (_, last) = self.split_at_mut(index);\n   543: \n   544:         // SAFETY: We explicitly check for the correct number of elements,\n   545:         //   do not let the reference outlive the slice,\n   546:         //   and require exclusive access to the entire slice to mutate the chunk.\n   547:         Some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })\n   548:     }\n   549: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::select_nth_unstable",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 50,
                      "path": "Ord"
                    }
                  }
                }
              ],
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "select_nth_unstable",
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
            "index",
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
    },
    "verification_source": "  3500:     /// assert!(lesser == [-3, -5] || lesser == [-5, -3]);\n  3501:     /// assert_eq!(median, &mut 1);\n  3502:     /// assert!(greater == [4, 2] || greater == [2, 4]);\n  3503:     ///\n  3504:     /// // We are only guaranteed the slice will be one of the following, based on the way we sort\n  3505:     /// // about the specified index.\n  3506:     /// assert!(v == [-3, -5, 1, 2, 4] ||\n  3507:     ///         v == [-5, -3, 1, 2, 4] ||\n  3508:     ///         v == [-3, -5, 1, 4, 2] ||\n  3509:     ///         v == [-5, -3, 1, 4, 2]);\n  3510:     /// ```\n  3511:     ///\n  3512:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3513:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3514:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3515:     #[inline]\n  3516:     pub fn select_nth_unstable(&mut self, index: usize) -> (&mut [T], &mut T, &mut [T])\n  3517:     where\n  3518:         T: Ord,\n  3519:     {\n  3520:         sort::select::partition_at_index(self, index, T::lt)\n  3521:     }\n  3522: \n  3523:     /// Reorders the slice with a comparator function such that the element at `index` is at a\n  3524:     /// sort-order position. All elements before `index` will be `<=` to this value, and all\n  3525:     /// elements after will be `>=` to it, according to the comparator function.\n  3526:     ///\n  3527:     /// This reordering is unstable (i.e. any element that compares equal to the nth element may end\n  3528:     /// up at that position), in-place (i.e.  does not allocate), and runs in *O*(*n*) time. This\n  3529:     /// function is also known as \"kth element\" in other libraries.\n  3530:     ///\n  3531:     /// Returns a triple partitioning the reordered slice:\n  3532:     ///",
    "nanvix_source": "  3512:     /// assert!(v == [-3, -5, 1, 2, 4] ||\n  3513:     ///         v == [-5, -3, 1, 2, 4] ||\n  3514:     ///         v == [-3, -5, 1, 4, 2] ||\n  3515:     ///         v == [-5, -3, 1, 4, 2]);\n  3516:     /// ```\n  3517:     ///\n  3518:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3519:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3520:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3521:     #[inline]\n  3522:     pub fn select_nth_unstable(&mut self, index: usize) -> (&mut [T], &mut T, &mut [T])\n  3523:     where\n  3524:         T: Ord,\n  3525:     {\n  3526:         sort::select::partition_at_index(self, index, T::lt)\n  3527:     }\n  3528: \n  3529:     /// Reorders the slice with a comparator function such that the element at `index` is at a\n  3530:     /// sort-order position. All elements before `index` will be `<=` to this value, and all\n  3531:     /// elements after will be `>=` to it, according to the comparator function.\n  3532:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::select_nth_unstable_by",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": null,
                              "id": 1682,
                              "path": "Ordering"
                            }
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
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
      "name": "select_nth_unstable_by",
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
            "index",
            {
              "primitive": "usize"
            }
          ],
          [
            "compare",
            {
              "generic": "F"
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
    },
    "verification_source": "  3565:     /// assert!(before == [4, 2] || before == [2, 4]);\n  3566:     /// assert_eq!(median, &mut 1);\n  3567:     /// assert!(after == [-3, -5] || after == [-5, -3]);\n  3568:     ///\n  3569:     /// // We are only guaranteed the slice will be one of the following, based on the way we sort\n  3570:     /// // about the specified index.\n  3571:     /// assert!(v == [2, 4, 1, -5, -3] ||\n  3572:     ///         v == [2, 4, 1, -3, -5] ||\n  3573:     ///         v == [4, 2, 1, -5, -3] ||\n  3574:     ///         v == [4, 2, 1, -3, -5]);\n  3575:     /// ```\n  3576:     ///\n  3577:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3578:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3579:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3580:     #[inline]\n  3581:     pub fn select_nth_unstable_by<F>(\n  3582:         &mut self,\n  3583:         index: usize,\n  3584:         mut compare: F,\n  3585:     ) -> (&mut [T], &mut T, &mut [T])\n  3586:     where\n  3587:         F: FnMut(&T, &T) -> Ordering,\n  3588:     {\n  3589:         sort::select::partition_at_index(self, index, |a: &T, b: &T| compare(a, b) == Less)\n  3590:     }\n  3591: \n  3592:     /// Reorders the slice with a key extraction function such that the element at `index` is at a\n  3593:     /// sort-order position. All elements before `index` will have keys `<=` to the key at `index`,\n  3594:     /// and all elements after will have keys `>=` to it.\n  3595:     ///\n  3596:     /// This reordering is unstable (i.e. any element that compares equal to the nth element may end\n  3597:     /// up at that position), in-place (i.e.  does not allocate), and runs in *O*(*n*) time. This",
    "nanvix_source": "  3577:     /// assert!(v == [2, 4, 1, -5, -3] ||\n  3578:     ///         v == [2, 4, 1, -3, -5] ||\n  3579:     ///         v == [4, 2, 1, -5, -3] ||\n  3580:     ///         v == [4, 2, 1, -3, -5]);\n  3581:     /// ```\n  3582:     ///\n  3583:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3584:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3585:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3586:     #[inline]\n  3587:     pub fn select_nth_unstable_by<F>(\n  3588:         &mut self,\n  3589:         index: usize,\n  3590:         mut compare: F,\n  3591:     ) -> (&mut [T], &mut T, &mut [T])\n  3592:     where\n  3593:         F: FnMut(&T, &T) -> Ordering,\n  3594:     {\n  3595:         sort::select::partition_at_index(self, index, |a: &T, b: &T| compare(a, b) == Less)\n  3596:     }\n  3597: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::select_nth_unstable_by_key",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "K"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 50,
                      "path": "Ord"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
      "name": "select_nth_unstable_by_key",
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
            "index",
            {
              "primitive": "usize"
            }
          ],
          [
            "f",
            {
              "generic": "F"
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
    },
    "verification_source": "  3632:     /// assert!(lesser == [1, 2] || lesser == [2, 1]);\n  3633:     /// assert_eq!(median, &mut -3);\n  3634:     /// assert!(greater == [4, -5] || greater == [-5, 4]);\n  3635:     ///\n  3636:     /// // We are only guaranteed the slice will be one of the following, based on the way we sort\n  3637:     /// // about the specified index.\n  3638:     /// assert!(v == [1, 2, -3, 4, -5] ||\n  3639:     ///         v == [1, 2, -3, -5, 4] ||\n  3640:     ///         v == [2, 1, -3, 4, -5] ||\n  3641:     ///         v == [2, 1, -3, -5, 4]);\n  3642:     /// ```\n  3643:     ///\n  3644:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3645:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3646:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3647:     #[inline]\n  3648:     pub fn select_nth_unstable_by_key<K, F>(\n  3649:         &mut self,\n  3650:         index: usize,\n  3651:         mut f: F,\n  3652:     ) -> (&mut [T], &mut T, &mut [T])\n  3653:     where\n  3654:         F: FnMut(&T) -> K,\n  3655:         K: Ord,\n  3656:     {\n  3657:         sort::select::partition_at_index(self, index, |a: &T, b: &T| f(a).lt(&f(b)))\n  3658:     }\n  3659: \n  3660:     /// Moves all consecutive repeated elements to the end of the slice according to the\n  3661:     /// [`PartialEq`] trait implementation.\n  3662:     ///\n  3663:     /// Returns two slices. The first contains no consecutive repeated elements.\n  3664:     /// The second contains all the duplicates in no specified order.",
    "nanvix_source": "  3644:     /// assert!(v == [1, 2, -3, 4, -5] ||\n  3645:     ///         v == [1, 2, -3, -5, 4] ||\n  3646:     ///         v == [2, 1, -3, 4, -5] ||\n  3647:     ///         v == [2, 1, -3, -5, 4]);\n  3648:     /// ```\n  3649:     ///\n  3650:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3651:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3652:     #[stable(feature = \"slice_select_nth_unstable\", since = \"1.49.0\")]\n  3653:     #[inline]\n  3654:     pub fn select_nth_unstable_by_key<K, F>(\n  3655:         &mut self,\n  3656:         index: usize,\n  3657:         mut f: F,\n  3658:     ) -> (&mut [T], &mut T, &mut [T])\n  3659:     where\n  3660:         F: FnMut(&T) -> K,\n  3661:         K: Ord,\n  3662:     {\n  3663:         sort::select::partition_at_index(self, index, |a: &T, b: &T| f(a).lt(&f(b)))\n  3664:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_at_mut_checked",
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
    "verification_source": "  2176:     /// let mut v = [1, 0, 3, 0, 5, 6];\n  2177:     ///\n  2178:     /// if let Some((left, right)) = v.split_at_mut_checked(2) {\n  2179:     ///     assert_eq!(left, [1, 0]);\n  2180:     ///     assert_eq!(right, [3, 0, 5, 6]);\n  2181:     ///     left[1] = 2;\n  2182:     ///     right[1] = 4;\n  2183:     /// }\n  2184:     /// assert_eq!(v, [1, 2, 3, 4, 5, 6]);\n  2185:     ///\n  2186:     /// assert_eq!(None, v.split_at_mut_checked(7));\n  2187:     /// ```\n  2188:     #[stable(feature = \"split_at_checked\", since = \"1.80.0\")]\n  2189:     #[rustc_const_stable(feature = \"const_slice_split_at_mut\", since = \"1.83.0\")]\n  2190:     #[inline]\n  2191:     #[must_use]\n  2192:     pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut [T], &mut [T])> {\n  2193:         if mid <= self.len() {\n  2194:             // SAFETY: `[ptr; mid]` and `[mid; len]` are inside `self`, which\n  2195:             // fulfills the requirements of `split_at_unchecked`.\n  2196:             Some(unsafe { self.split_at_mut_unchecked(mid) })\n  2197:         } else {\n  2198:             None\n  2199:         }\n  2200:     }\n  2201: \n  2202:     /// Returns an iterator over subslices separated by elements that match\n  2203:     /// `pred`. The matched element is not contained in the subslices.\n  2204:     ///\n  2205:     /// # Examples\n  2206:     ///\n  2207:     /// ```\n  2208:     /// let slice = [10, 40, 33, 20];",
    "nanvix_source": "  2185:     ///     right[1] = 4;\n  2186:     /// }\n  2187:     /// assert_eq!(v, [1, 2, 3, 4, 5, 6]);\n  2188:     ///\n  2189:     /// assert_eq!(None, v.split_at_mut_checked(7));\n  2190:     /// ```\n  2191:     #[stable(feature = \"split_at_checked\", since = \"1.80.0\")]\n  2192:     #[rustc_const_stable(feature = \"const_slice_split_at_mut\", since = \"1.83.0\")]\n  2193:     #[inline]\n  2194:     #[must_use]\n  2195:     pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut [T], &mut [T])> {\n  2196:         if mid <= self.len() {\n  2197:             // SAFETY: `[ptr; mid]` and `[mid; len]` are inside `self`, which\n  2198:             // fulfills the requirements of `split_at_unchecked`.\n  2199:             Some(unsafe { self.split_at_mut_unchecked(mid) })\n  2200:         } else {\n  2201:             None\n  2202:         }\n  2203:     }\n  2204: \n  2205:     /// Returns an iterator over subslices separated by elements that match",
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
