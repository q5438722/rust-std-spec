For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::array::each_mut",
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
      "name": "each_mut",
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
          "array": {
            "len": "N",
            "type": {
              "generic": "T"
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
        "impl_id": "core:51748",
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
          "array": {
            "len": "N",
            "type": {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "T"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   694:     /// Borrows each element mutably and returns an array of mutable references\n   695:     /// with the same size as `self`.\n   696:     ///\n   697:     ///\n   698:     /// # Example\n   699:     ///\n   700:     /// ```\n   701:     ///\n   702:     /// let mut floats = [3.1, 2.7, -1.0];\n   703:     /// let float_refs: [&mut f64; 3] = floats.each_mut();\n   704:     /// *float_refs[0] = 0.0;\n   705:     /// assert_eq!(float_refs, [&mut 0.0, &mut 2.7, &mut -1.0]);\n   706:     /// assert_eq!(floats, [0.0, 2.7, -1.0]);\n   707:     /// ```\n   708:     #[stable(feature = \"array_methods\", since = \"1.77.0\")]\n   709:     #[rustc_const_stable(feature = \"const_array_each_ref\", since = \"1.91.0\")]\n   710:     pub const fn each_mut(&mut self) -> [&mut T; N] {\n   711:         let mut buf = [null_mut::<T>(); N];\n   712: \n   713:         // FIXME(const_trait_impl): We would like to simply use iterators for this (as in the original implementation), but this is not allowed in constant expressions.\n   714:         let mut i = 0;\n   715:         while i < N {\n   716:             buf[i] = &raw mut self[i];\n   717: \n   718:             i += 1;\n   719:         }\n   720: \n   721:         // SAFETY: `*mut T` has the same layout as `&mut T`, and we've also initialised each pointer as a valid reference.\n   722:         unsafe { transmute_unchecked(buf) }\n   723:     }\n   724: \n   725:     /// Divides one array reference into two at an index.\n   726:     ///",
    "nanvix_source": "   709:     /// ```\n   710:     ///\n   711:     /// let mut floats = [3.1, 2.7, -1.0];\n   712:     /// let float_refs: [&mut f64; 3] = floats.each_mut();\n   713:     /// *float_refs[0] = 0.0;\n   714:     /// assert_eq!(float_refs, [&mut 0.0, &mut 2.7, &mut -1.0]);\n   715:     /// assert_eq!(floats, [0.0, 2.7, -1.0]);\n   716:     /// ```\n   717:     #[stable(feature = \"array_methods\", since = \"1.77.0\")]\n   718:     #[rustc_const_stable(feature = \"const_array_each_ref\", since = \"1.91.0\")]\n   719:     pub const fn each_mut(&mut self) -> [&mut T; N] {\n   720:         let mut buf = [null_mut::<T>(); N];\n   721: \n   722:         // FIXME(const_trait_impl): We would like to simply use iterators for this (as in the original implementation), but this is not allowed in constant expressions.\n   723:         let mut i = 0;\n   724:         while i < N {\n   725:             buf[i] = &raw mut self[i];\n   726: \n   727:             i += 1;\n   728:         }\n   729: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::from_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": false
      },
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "s"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "s",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "T"
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
              "array": {
                "len": "1",
                "type": {
                  "generic": "T"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   158:             try { unsafe { MaybeUninit::array_assume_init(array) } }\n   159:         }\n   160:     }\n   161: }\n   162: \n   163: /// Converts a reference to `T` into a reference to an array of length 1 (without copying).\n   164: #[stable(feature = \"array_from_ref\", since = \"1.53.0\")]\n   165: #[rustc_const_stable(feature = \"const_array_from_ref_shared\", since = \"1.63.0\")]\n   166: pub const fn from_ref<T>(s: &T) -> &[T; 1] {\n   167:     // SAFETY: Converting `&T` to `&[T; 1]` is sound.\n   168:     unsafe { &*(s as *const T).cast::<[T; 1]>() }\n   169: }\n   170: \n   171: /// Converts a mutable reference to `T` into a mutable reference to an array of length 1 (without copying).\n   172: #[stable(feature = \"array_from_ref\", since = \"1.53.0\")]\n   173: #[rustc_const_stable(feature = \"const_array_from_ref\", since = \"1.83.0\")]\n   174: pub const fn from_mut<T>(s: &mut T) -> &mut [T; 1] {\n   175:     // SAFETY: Converting `&mut T` to `&mut [T; 1]` is sound.\n   176:     unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }\n   177: }\n   178: \n   179: /// The error type returned when a conversion from a slice to an array fails.\n   180: #[stable(feature = \"try_from\", since = \"1.34.0\")]\n   181: #[derive(Debug, Copy, Clone)]\n   182: pub struct TryFromSliceError(());\n   183: \n   184: #[stable(feature = \"core_array\", since = \"1.35.0\")]\n   185: impl fmt::Display for TryFromSliceError {\n   186:     #[inline]\n   187:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   188:         \"could not convert slice to array\".fmt(f)\n   189:     }\n   190: }",
    "nanvix_source": "   165: #[stable(feature = \"array_from_ref\", since = \"1.53.0\")]\n   166: #[rustc_const_stable(feature = \"const_array_from_ref_shared\", since = \"1.63.0\")]\n   167: pub const fn from_ref<T>(s: &T) -> &[T; 1] {\n   168:     // SAFETY: Converting `&T` to `&[T; 1]` is sound.\n   169:     unsafe { &*(s as *const T).cast::<[T; 1]>() }\n   170: }\n   171: \n   172: /// Converts a mutable reference to `T` into a mutable reference to an array of length 1 (without copying).\n   173: #[stable(feature = \"array_from_ref\", since = \"1.53.0\")]\n   174: #[rustc_const_stable(feature = \"const_array_from_ref\", since = \"1.83.0\")]\n   175: pub const fn from_mut<T>(s: &mut T) -> &mut [T; 1] {\n   176:     // SAFETY: Converting `&mut T` to `&mut [T; 1]` is sound.\n   177:     unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }\n   178: }\n   179: \n   180: /// The error type returned when a conversion from a slice to an array fails.\n   181: #[stable(feature = \"try_from\", since = \"1.34.0\")]\n   182: #[derive(Debug, Copy, Clone)]\n   183: pub struct TryFromSliceError(());\n   184: \n   185: #[stable(feature = \"core_array\", since = \"1.35.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24750",
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
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   613:     ///\n   614:     /// [`borrow_mut`]: RefCell::borrow_mut()\n   615:     ///\n   616:     /// # Examples\n   617:     ///\n   618:     /// ```\n   619:     /// use std::cell::Cell;\n   620:     ///\n   621:     /// let mut c = Cell::new(5);\n   622:     /// *c.get_mut() += 1;\n   623:     ///\n   624:     /// assert_eq!(c.get(), 6);\n   625:     /// ```\n   626:     #[inline]\n   627:     #[stable(feature = \"cell_get_mut\", since = \"1.11.0\")]\n   628:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   629:     pub const fn get_mut(&mut self) -> &mut T {\n   630:         self.value.get_mut()\n   631:     }\n   632: \n   633:     /// Returns a `&Cell<T>` from a `&mut T`\n   634:     ///\n   635:     /// # Examples\n   636:     ///\n   637:     /// ```\n   638:     /// use std::cell::Cell;\n   639:     ///\n   640:     /// let slice: &mut [i32] = &mut [1, 2, 3];\n   641:     /// let cell_slice: &Cell<[i32]> = Cell::from_mut(slice);\n   642:     /// let slice_cell: &[Cell<i32>] = cell_slice.as_slice_of_cells();\n   643:     ///\n   644:     /// assert_eq!(slice_cell.len(), 3);\n   645:     /// ```",
    "nanvix_source": "   619:     /// use std::cell::Cell;\n   620:     ///\n   621:     /// let mut c = Cell::new(5);\n   622:     /// *c.get_mut() += 1;\n   623:     ///\n   624:     /// assert_eq!(c.get(), 6);\n   625:     /// ```\n   626:     #[inline]\n   627:     #[stable(feature = \"cell_get_mut\", since = \"1.11.0\")]\n   628:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   629:     pub const fn get_mut(&mut self) -> &mut T {\n   630:         self.value.get_mut()\n   631:     }\n   632: \n   633:     /// Returns a `&Cell<T>` from a `&mut T`\n   634:     ///\n   635:     /// # Examples\n   636:     ///\n   637:     /// ```\n   638:     /// use std::cell::Cell;\n   639:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::LazyCell::force_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
        "is_unsafe": false
      },
      "name": "force_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11932,
            "path": "LazyCell"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": {
                            "parenthesized": {
                              "inputs": [],
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
                  "is_synthetic": false
                }
              },
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24688",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11932",
        "resolved_owner_path": [
          "core",
          "cell",
          "lazy",
          "LazyCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
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
                              "generic": "F"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 11932,
                    "path": "LazyCell"
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
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   163:     /// [`force()`]: LazyCell::force\n   164:     ///\n   165:     /// # Examples\n   166:     ///\n   167:     /// ```\n   168:     /// use std::cell::LazyCell;\n   169:     ///\n   170:     /// let mut lazy = LazyCell::new(|| 92);\n   171:     ///\n   172:     /// let p = LazyCell::force_mut(&mut lazy);\n   173:     /// assert_eq!(*p, 92);\n   174:     /// *p = 44;\n   175:     /// assert_eq!(*lazy, 44);\n   176:     /// ```\n   177:     #[inline]\n   178:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   179:     pub fn force_mut(this: &mut LazyCell<T, F>) -> &mut T {\n   180:         #[cold]\n   181:         /// # Safety\n   182:         /// May only be called when the state is `Uninit`.\n   183:         unsafe fn really_init_mut<T, F: FnOnce() -> T>(state: &mut State<T, F>) -> &mut T {\n   184:             // INVARIANT: Always valid, but the value may not be dropped.\n   185:             struct PoisonOnPanic<T, F>(*mut State<T, F>);\n   186:             impl<T, F> Drop for PoisonOnPanic<T, F> {\n   187:                 #[inline]\n   188:                 fn drop(&mut self) {\n   189:                     // SAFETY: Invariant states it is valid, and we don't drop the old value.\n   190:                     unsafe {\n   191:                         self.0.write(State::Poisoned);\n   192:                     }\n   193:                 }\n   194:             }\n   195: ",
    "nanvix_source": "   169:     ///\n   170:     /// let mut lazy = LazyCell::new(|| 92);\n   171:     ///\n   172:     /// let p = LazyCell::force_mut(&mut lazy);\n   173:     /// assert_eq!(*p, 92);\n   174:     /// *p = 44;\n   175:     /// assert_eq!(*lazy, 44);\n   176:     /// ```\n   177:     #[inline]\n   178:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   179:     pub fn force_mut(this: &mut LazyCell<T, F>) -> &mut T {\n   180:         #[cold]\n   181:         /// # Safety\n   182:         /// May only be called when the state is `Uninit`.\n   183:         unsafe fn really_init_mut<T, F: FnOnce() -> T>(state: &mut State<T, F>) -> &mut T {\n   184:             // INVARIANT: Always valid, but the value may not be dropped.\n   185:             struct PoisonOnPanic<T, F>(*mut State<T, F>);\n   186:             impl<T, F> Drop for PoisonOnPanic<T, F> {\n   187:                 #[inline]\n   188:                 fn drop(&mut self) {\n   189:                     // SAFETY: Invariant states it is valid, and we don't drop the old value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::LazyCell::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
        "is_unsafe": false
      },
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11932,
            "path": "LazyCell"
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
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24691",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11932",
        "resolved_owner_path": [
          "core",
          "cell",
          "lazy",
          "LazyCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
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
                              "generic": "F"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 11932,
                    "path": "LazyCell"
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
                        "lifetime": null,
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
    "verification_source": "   261:     /// poisoned), returns `None`.\n   262:     ///\n   263:     /// # Examples\n   264:     ///\n   265:     /// ```\n   266:     /// use std::cell::LazyCell;\n   267:     ///\n   268:     /// let mut lazy = LazyCell::new(|| 92);\n   269:     ///\n   270:     /// assert_eq!(LazyCell::get_mut(&mut lazy), None);\n   271:     /// let _ = LazyCell::force(&lazy);\n   272:     /// *LazyCell::get_mut(&mut lazy).unwrap() = 44;\n   273:     /// assert_eq!(*lazy, 44);\n   274:     /// ```\n   275:     #[inline]\n   276:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   277:     pub fn get_mut(this: &mut LazyCell<T, F>) -> Option<&mut T> {\n   278:         let state = this.state.get_mut();\n   279:         match state {\n   280:             State::Init(data) => Some(data),\n   281:             _ => None,\n   282:         }\n   283:     }\n   284: \n   285:     /// Returns a reference to the value if initialized. Otherwise (if uninitialized or poisoned),\n   286:     /// returns `None`.\n   287:     ///\n   288:     /// # Examples\n   289:     ///\n   290:     /// ```\n   291:     /// use std::cell::LazyCell;\n   292:     ///\n   293:     /// let lazy = LazyCell::new(|| 92);",
    "nanvix_source": "   267:     ///\n   268:     /// let mut lazy = LazyCell::new(|| 92);\n   269:     ///\n   270:     /// assert_eq!(LazyCell::get_mut(&mut lazy), None);\n   271:     /// let _ = LazyCell::force(&lazy);\n   272:     /// *LazyCell::get_mut(&mut lazy).unwrap() = 44;\n   273:     /// assert_eq!(*lazy, 44);\n   274:     /// ```\n   275:     #[inline]\n   276:     #[stable(feature = \"lazy_get\", since = \"1.94.0\")]\n   277:     pub fn get_mut(this: &mut LazyCell<T, F>) -> Option<&mut T> {\n   278:         let state = this.state.get_mut();\n   279:         match state {\n   280:             State::Init(data) => Some(data),\n   281:             _ => None,\n   282:         }\n   283:     }\n   284: \n   285:     /// Returns a reference to the value if initialized. Otherwise (if uninitialized or poisoned),\n   286:     /// returns `None`.\n   287:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
            "id": 9782,
            "path": "OnceCell"
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
        "impl_id": "core:24718",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9782",
        "resolved_owner_path": [
          "core",
          "cell",
          "once",
          "OnceCell"
        ],
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
    "verification_source": "    49: \n    50:     /// Gets the reference to the underlying value.\n    51:     ///\n    52:     /// Returns `None` if the cell is uninitialized.\n    53:     #[inline]\n    54:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant\n    57:         unsafe { &*self.inner.get() }.as_ref()\n    58:     }\n    59: \n    60:     /// Gets the mutable reference to the underlying value.\n    61:     ///\n    62:     /// Returns `None` if the cell is uninitialized.\n    63:     #[inline]\n    64:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    65:     pub fn get_mut(&mut self) -> Option<&mut T> {\n    66:         self.inner.get_mut().as_mut()\n    67:     }\n    68: \n    69:     /// Initializes the contents of the cell to `value`.\n    70:     ///\n    71:     /// # Errors\n    72:     ///\n    73:     /// This method returns `Ok(())` if the cell was uninitialized\n    74:     /// and `Err(value)` if it was already initialized.\n    75:     ///\n    76:     /// # Examples\n    77:     ///\n    78:     /// ```\n    79:     /// use std::cell::OnceCell;\n    80:     ///\n    81:     /// let cell = OnceCell::new();",
    "nanvix_source": "    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant\n    57:         unsafe { &*self.inner.get() }.as_ref()\n    58:     }\n    59: \n    60:     /// Gets the mutable reference to the underlying value.\n    61:     ///\n    62:     /// Returns `None` if the cell is uninitialized.\n    63:     #[inline]\n    64:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    65:     pub fn get_mut(&mut self) -> Option<&mut T> {\n    66:         self.inner.get_mut().as_mut()\n    67:     }\n    68: \n    69:     /// Initializes the contents of the cell to `value`.\n    70:     ///\n    71:     /// # Errors\n    72:     ///\n    73:     /// This method returns `Ok(())` if the cell was uninitialized\n    74:     /// and `Err(value)` if it was already initialized.\n    75:     ///",
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
