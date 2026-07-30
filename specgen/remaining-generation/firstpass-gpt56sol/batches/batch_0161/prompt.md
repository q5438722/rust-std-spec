For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::Cell::set",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
        "is_unsafe": false
      },
      "name": "set",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9785,
            "path": "Cell"
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
        "impl_id": "core:24742",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          ],
          [
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   417: \n   418:     /// Sets the contained value.\n   419:     ///\n   420:     /// # Examples\n   421:     ///\n   422:     /// ```\n   423:     /// use std::cell::Cell;\n   424:     ///\n   425:     /// let c = Cell::new(5);\n   426:     ///\n   427:     /// c.set(10);\n   428:     /// ```\n   429:     #[inline]\n   430:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   431:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   432:     #[rustc_should_not_be_called_on_const_items]\n   433:     pub const fn set(&self, val: T)\n   434:     where\n   435:         T: [const] Destruct,\n   436:     {\n   437:         self.replace(val);\n   438:     }\n   439: \n   440:     /// Swaps the values of two `Cell`s.\n   441:     ///\n   442:     /// The difference with `std::mem::swap` is that this function doesn't\n   443:     /// require a `&mut` reference.\n   444:     ///\n   445:     /// # Panics\n   446:     ///\n   447:     /// This function will panic if `self` and `other` are different `Cell`s that partially overlap.\n   448:     /// (Using just standard library methods, it is impossible to create such partially overlapping `Cell`s.\n   449:     /// However, unsafe code is allowed to e.g. create two `&Cell<[i32; 2]>` that partially overlap.)",
    "nanvix_source": "   423:     /// use std::cell::Cell;\n   424:     ///\n   425:     /// let c = Cell::new(5);\n   426:     ///\n   427:     /// c.set(10);\n   428:     /// ```\n   429:     #[inline]\n   430:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   431:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   432:     #[rustc_should_not_be_called_on_const_items]\n   433:     pub const fn set(&self, val: T)\n   434:     where\n   435:         T: [const] Destruct,\n   436:     {\n   437:         self.replace(val);\n   438:     }\n   439: \n   440:     /// Swaps the values of two `Cell`s.\n   441:     ///\n   442:     /// The difference with `std::mem::swap` is that this function doesn't\n   443:     /// require a `&mut` reference.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::swap",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_unsafe": false
      },
      "name": "swap",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9785,
            "path": "Cell"
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
        "impl_id": "core:24742",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          ],
          [
            "other",
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
        "output": null
      }
    },
    "verification_source": "   449:     /// However, unsafe code is allowed to e.g. create two `&Cell<[i32; 2]>` that partially overlap.)\n   450:     ///\n   451:     /// # Examples\n   452:     ///\n   453:     /// ```\n   454:     /// use std::cell::Cell;\n   455:     ///\n   456:     /// let c1 = Cell::new(5i32);\n   457:     /// let c2 = Cell::new(10i32);\n   458:     /// c1.swap(&c2);\n   459:     /// assert_eq!(10, c1.get());\n   460:     /// assert_eq!(5, c2.get());\n   461:     /// ```\n   462:     #[inline]\n   463:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   464:     #[rustc_should_not_be_called_on_const_items]\n   465:     pub fn swap(&self, other: &Self) {\n   466:         // This function documents that it *will* panic, and intrinsics::is_nonoverlapping doesn't\n   467:         // do the check in const, so trying to use it here would be inviting unnecessary fragility.\n   468:         fn is_nonoverlapping<T>(src: *const T, dst: *const T) -> bool {\n   469:             let src_usize = src.addr();\n   470:             let dst_usize = dst.addr();\n   471:             let diff = src_usize.abs_diff(dst_usize);\n   472:             diff >= size_of::<T>()\n   473:         }\n   474: \n   475:         if ptr::eq(self, other) {\n   476:             // Swapping wouldn't change anything.\n   477:             return;\n   478:         }\n   479:         if !is_nonoverlapping(self, other) {\n   480:             // See <https://github.com/rust-lang/rust/issues/80778> for why we need to stop here.\n   481:             panic!(\"`Cell::swap` on overlapping non-identical `Cell`s\");",
    "nanvix_source": "   455:     ///\n   456:     /// let c1 = Cell::new(5i32);\n   457:     /// let c2 = Cell::new(10i32);\n   458:     /// c1.swap(&c2);\n   459:     /// assert_eq!(10, c1.get());\n   460:     /// assert_eq!(5, c2.get());\n   461:     /// ```\n   462:     #[inline]\n   463:     #[stable(feature = \"move_cell\", since = \"1.17.0\")]\n   464:     #[rustc_should_not_be_called_on_const_items]\n   465:     pub fn swap(&self, other: &Self) {\n   466:         // This function documents that it *will* panic, and intrinsics::is_nonoverlapping doesn't\n   467:         // do the check in const, so trying to use it here would be inviting unnecessary fragility.\n   468:         fn is_nonoverlapping<T>(src: *const T, dst: *const T) -> bool {\n   469:             let src_usize = src.addr();\n   470:             let dst_usize = dst.addr();\n   471:             let diff = src_usize.abs_diff(dst_usize);\n   472:             diff >= size_of::<T>()\n   473:         }\n   474: \n   475:         if ptr::eq(self, other) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::update",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
                          "parenthesized": {
                            "inputs": [
                              {
                                "generic": "T"
                              }
                            ],
                            "output": {
                              "generic": "T"
                            }
                          }
                        },
                        "id": 24,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl [const] FnOnce(T) -> T"
          }
        ],
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
        "is_unsafe": false
      },
      "name": "update",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9785,
            "path": "Cell"
          }
        },
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
                          "args": null,
                          "id": 6,
                          "path": "Copy"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24745",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          ],
          [
            "f",
            {
              "impl_trait": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   557: \n   558:     /// Updates the contained value using a function.\n   559:     ///\n   560:     /// # Examples\n   561:     ///\n   562:     /// ```\n   563:     /// use std::cell::Cell;\n   564:     ///\n   565:     /// let c = Cell::new(5);\n   566:     /// c.update(|x| x + 1);\n   567:     /// assert_eq!(c.get(), 6);\n   568:     /// ```\n   569:     #[inline]\n   570:     #[stable(feature = \"cell_update\", since = \"1.88.0\")]\n   571:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   572:     #[rustc_should_not_be_called_on_const_items]\n   573:     pub const fn update(&self, f: impl [const] FnOnce(T) -> T)\n   574:     where\n   575:         // FIXME(const-hack): `Copy` should imply `const Destruct`\n   576:         T: [const] Destruct,\n   577:     {\n   578:         let old = self.get();\n   579:         self.set(f(old));\n   580:     }\n   581: }\n   582: \n   583: impl<T: ?Sized> Cell<T> {\n   584:     /// Returns a raw pointer to the underlying data in this cell.\n   585:     ///\n   586:     /// # Examples\n   587:     ///\n   588:     /// ```\n   589:     /// use std::cell::Cell;",
    "nanvix_source": "   563:     /// use std::cell::Cell;\n   564:     ///\n   565:     /// let c = Cell::new(5);\n   566:     /// c.update(|x| x + 1);\n   567:     /// assert_eq!(c.get(), 6);\n   568:     /// ```\n   569:     #[inline]\n   570:     #[stable(feature = \"cell_update\", since = \"1.88.0\")]\n   571:     #[rustc_const_unstable(feature = \"const_cell_traits\", issue = \"147787\")]\n   572:     #[rustc_should_not_be_called_on_const_items]\n   573:     pub const fn update(&self, f: impl [const] FnOnce(T) -> T)\n   574:     where\n   575:         // FIXME(const-hack): `Copy` should imply `const Destruct`\n   576:         T: [const] Destruct,\n   577:     {\n   578:         let old = self.get();\n   579:         self.set(f(old));\n   580:     }\n   581: }\n   582: \n   583: impl<T: ?Sized> Cell<T> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::swap",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
      "name": "swap",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9393,
            "path": "RefCell"
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
        "impl_id": "core:24784",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
          ],
          [
            "other",
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
        "output": null
      }
    },
    "verification_source": "  1063:     /// if `self` and `other` point to the same `RefCell`.\n  1064:     ///\n  1065:     /// # Examples\n  1066:     ///\n  1067:     /// ```\n  1068:     /// use std::cell::RefCell;\n  1069:     /// let c = RefCell::new(5);\n  1070:     /// let d = RefCell::new(6);\n  1071:     /// c.swap(&d);\n  1072:     /// assert_eq!(c, RefCell::new(6));\n  1073:     /// assert_eq!(d, RefCell::new(5));\n  1074:     /// ```\n  1075:     #[inline]\n  1076:     #[stable(feature = \"refcell_swap\", since = \"1.24.0\")]\n  1077:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1078:     #[rustc_should_not_be_called_on_const_items]\n  1079:     pub const fn swap(&self, other: &Self) {\n  1080:         mem::swap(&mut *self.borrow_mut(), &mut *other.borrow_mut())\n  1081:     }\n  1082: }\n  1083: \n  1084: impl<T: ?Sized> RefCell<T> {\n  1085:     /// Immutably borrows the wrapped value.\n  1086:     ///\n  1087:     /// The borrow lasts until the returned `Ref` exits scope. Multiple\n  1088:     /// immutable borrows can be taken out at the same time.\n  1089:     ///\n  1090:     /// # Panics\n  1091:     ///\n  1092:     /// Panics if the value is currently mutably borrowed. For a non-panicking variant, use\n  1093:     /// [`try_borrow`](#method.try_borrow).\n  1094:     ///\n  1095:     /// # Examples",
    "nanvix_source": "  1069:     /// let c = RefCell::new(5);\n  1070:     /// let d = RefCell::new(6);\n  1071:     /// c.swap(&d);\n  1072:     /// assert_eq!(c, RefCell::new(6));\n  1073:     /// assert_eq!(d, RefCell::new(5));\n  1074:     /// ```\n  1075:     #[inline]\n  1076:     #[stable(feature = \"refcell_swap\", since = \"1.24.0\")]\n  1077:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1078:     #[rustc_should_not_be_called_on_const_items]\n  1079:     pub const fn swap(&self, other: &Self) {\n  1080:         mem::swap(&mut *self.borrow_mut(), &mut *other.borrow_mut())\n  1081:     }\n  1082: }\n  1083: \n  1084: impl<T: ?Sized> RefCell<T> {\n  1085:     /// Immutably borrows the wrapped value.\n  1086:     ///\n  1087:     /// The borrow lasts until the returned `Ref` exits scope. Multiple\n  1088:     /// immutable borrows can be taken out at the same time.\n  1089:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::hint::cold_path",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
      "name": "cold_path",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   765: ///         cold_path();\n   766: ///     }\n   767: ///     b\n   768: /// }\n   769: ///\n   770: /// fn foo(x: i32) {\n   771: ///     if likely(x > 0) {\n   772: ///         println!(\"this branch is likely to be taken\");\n   773: ///     } else {\n   774: ///         println!(\"this branch is unlikely to be taken\");\n   775: ///     }\n   776: /// }\n   777: /// ```\n   778: #[stable(feature = \"cold_path\", since = \"1.95.0\")]\n   779: #[rustc_const_stable(feature = \"cold_path\", since = \"1.95.0\")]\n   780: #[inline(always)]\n   781: pub const fn cold_path() {\n   782:     crate::intrinsics::cold_path()\n   783: }\n   784: \n   785: /// Returns either `true_val` or `false_val` depending on the value of\n   786: /// `condition`, with a hint to the compiler that `condition` is unlikely to be\n   787: /// correctly predicted by a CPU\u2019s branch predictor.\n   788: ///\n   789: /// This method is functionally equivalent to\n   790: /// ```ignore (this is just for illustrative purposes)\n   791: /// fn select_unpredictable<T>(b: bool, true_val: T, false_val: T) -> T {\n   792: ///     if b { true_val } else { false_val }\n   793: /// }\n   794: /// ```\n   795: /// but might generate different assembly. In particular, on platforms with\n   796: /// a conditional move or select instruction (like `cmov` on x86 or `csel`\n   797: /// on ARM) the optimizer might use these instructions to avoid branches,",
    "nanvix_source": "   774: ///         println!(\"this branch is unlikely to be taken\");\n   775: ///     }\n   776: /// }\n   777: /// ```\n   778: #[stable(feature = \"cold_path\", since = \"1.95.0\")]\n   779: #[rustc_const_stable(feature = \"cold_path\", since = \"1.95.0\")]\n   780: #[inline(always)]\n   781: // Even if for some reason the cold_path intrinsic is not visible to codegen, the coldness will\n   782: // ensure that branches this is in are still known to be cold.\n   783: #[cold]\n   784: pub const fn cold_path() {\n   785:     crate::intrinsics::cold_path()\n   786: }\n   787: \n   788: /// Returns either `true_val` or `false_val` depending on the value of\n   789: /// `condition`, with a hint to the compiler that `condition` is unlikely to be\n   790: /// correctly predicted by a CPU\u2019s branch predictor.\n   791: ///\n   792: /// This method is functionally equivalent to\n   793: /// ```ignore (this is just for illustrative purposes)\n   794: /// fn select_unpredictable<T>(b: bool, true_val: T, false_val: T) -> T {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::hint::spin_loop",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
        "is_unsafe": false
      },
      "name": "spin_loop",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   254: /// while !live.load(Ordering::Acquire) {\n   255: ///     // The spin loop is a hint to the CPU that we're waiting, but probably\n   256: ///     // not for very long\n   257: ///     hint::spin_loop();\n   258: /// }\n   259: ///\n   260: /// // The value is now set\n   261: /// # fn do_some_work() {}\n   262: /// do_some_work();\n   263: /// bg_work.join()?;\n   264: /// # Ok::<(), Box<dyn core::any::Any + Send + 'static>>(())\n   265: /// ```\n   266: ///\n   267: /// [`thread::yield_now`]: ../../std/thread/fn.yield_now.html\n   268: #[inline(always)]\n   269: #[stable(feature = \"renamed_spin_loop\", since = \"1.49.0\")]\n   270: pub fn spin_loop() {\n   271:     crate::cfg_select! {\n   272:         miri => {\n   273:             unsafe extern \"Rust\" {\n   274:                 safe fn miri_spin_loop();\n   275:             }\n   276: \n   277:             // Miri does support some of the intrinsics that are called below, but to guarantee\n   278:             // consistent behavior across targets, this custom function is used.\n   279:             miri_spin_loop();\n   280:         }\n   281:         target_arch = \"x86\" => {\n   282:             // SAFETY: the `cfg` attr ensures that we only execute this on x86 targets.\n   283:             crate::arch::x86::_mm_pause()\n   284:         }\n   285:         target_arch = \"x86_64\" => {\n   286:             // SAFETY: the `cfg` attr ensures that we only execute this on x86_64 targets.",
    "nanvix_source": "   260: /// // The value is now set\n   261: /// # fn do_some_work() {}\n   262: /// do_some_work();\n   263: /// bg_work.join()?;\n   264: /// # Ok::<(), Box<dyn core::any::Any + Send + 'static>>(())\n   265: /// ```\n   266: ///\n   267: /// [`thread::yield_now`]: ../../std/thread/fn.yield_now.html\n   268: #[inline(always)]\n   269: #[stable(feature = \"renamed_spin_loop\", since = \"1.49.0\")]\n   270: pub fn spin_loop() {\n   271:     crate::cfg_select! {\n   272:         miri => {\n   273:             unsafe extern \"Rust\" {\n   274:                 safe fn miri_spin_loop();\n   275:             }\n   276: \n   277:             // Miri does support some of the intrinsics that are called below, but to guarantee\n   278:             // consistent behavior across targets, this custom function is used.\n   279:             miri_spin_loop();\n   280:         }",
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
