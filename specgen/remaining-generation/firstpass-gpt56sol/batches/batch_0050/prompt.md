For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::first_chunk_mut",
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
      "name": "first_chunk_mut",
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
    "verification_source": "   341:     /// # Examples\n   342:     ///\n   343:     /// ```\n   344:     /// let x = &mut [0, 1, 2];\n   345:     ///\n   346:     /// if let Some(first) = x.first_chunk_mut::<2>() {\n   347:     ///     first[0] = 5;\n   348:     ///     first[1] = 4;\n   349:     /// }\n   350:     /// assert_eq!(x, &[5, 4, 2]);\n   351:     ///\n   352:     /// assert_eq!(None, x.first_chunk_mut::<4>());\n   353:     /// ```\n   354:     #[inline]\n   355:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   356:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   357:     pub const fn first_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   358:         if self.len() < N {\n   359:             None\n   360:         } else {\n   361:             // SAFETY: We explicitly check for the correct number of elements,\n   362:             //   do not let the reference outlive the slice,\n   363:             //   and require exclusive access to the entire slice to mutate the chunk.\n   364:             Some(unsafe { &mut *(self.as_mut_ptr().cast_array()) })\n   365:         }\n   366:     }\n   367: \n   368:     /// Returns an array reference to the first `N` items in the slice and the remaining slice.\n   369:     ///\n   370:     /// If the slice is not at least `N` in length, this will return `None`.\n   371:     ///\n   372:     /// # Examples\n   373:     ///",
    "nanvix_source": "   347:     ///     first[0] = 5;\n   348:     ///     first[1] = 4;\n   349:     /// }\n   350:     /// assert_eq!(x, &[5, 4, 2]);\n   351:     ///\n   352:     /// assert_eq!(None, x.first_chunk_mut::<4>());\n   353:     /// ```\n   354:     #[inline]\n   355:     #[stable(feature = \"slice_first_last_chunk\", since = \"1.77.0\")]\n   356:     #[rustc_const_stable(feature = \"const_slice_first_last_chunk\", since = \"1.83.0\")]\n   357:     pub const fn first_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {\n   358:         if self.len() < N {\n   359:             None\n   360:         } else {\n   361:             // SAFETY: We explicitly check for the correct number of elements,\n   362:             //   do not let the reference outlive the slice,\n   363:             //   and require exclusive access to the entire slice to mutate the chunk.\n   364:             Some(unsafe { &mut *(self.as_mut_ptr().cast_array()) })\n   365:         }\n   366:     }\n   367: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::from_mut",
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
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "   195:     }\n   196: }\n   197: \n   198: /// Converts a reference to T into a slice of length 1 (without copying).\n   199: #[stable(feature = \"from_ref\", since = \"1.28.0\")]\n   200: #[rustc_const_stable(feature = \"const_slice_from_ref_shared\", since = \"1.63.0\")]\n   201: #[rustc_diagnostic_item = \"slice_from_ref\"]\n   202: #[must_use]\n   203: pub const fn from_ref<T>(s: &T) -> &[T] {\n   204:     array::from_ref(s)\n   205: }\n   206: \n   207: /// Converts a reference to T into a slice of length 1 (without copying).\n   208: #[stable(feature = \"from_ref\", since = \"1.28.0\")]\n   209: #[rustc_const_stable(feature = \"const_slice_from_ref\", since = \"1.83.0\")]\n   210: #[must_use]\n   211: pub const fn from_mut<T>(s: &mut T) -> &mut [T] {\n   212:     array::from_mut(s)\n   213: }\n   214: \n   215: /// Forms a slice from a pointer range.\n   216: ///\n   217: /// This function is useful for interacting with foreign interfaces which\n   218: /// use two pointers to refer to a range of elements in memory, as is\n   219: /// common in C++.\n   220: ///\n   221: /// # Safety\n   222: ///\n   223: /// Behavior is undefined if any of the following conditions are violated:\n   224: ///\n   225: /// * The `start` pointer of the range must be a non-null, [valid] and properly aligned pointer\n   226: ///   to the first element of a slice.\n   227: ///",
    "nanvix_source": "   201: #[rustc_diagnostic_item = \"slice_from_ref\"]\n   202: #[must_use]\n   203: pub const fn from_ref<T>(s: &T) -> &[T] {\n   204:     array::from_ref(s)\n   205: }\n   206: \n   207: /// Converts a reference to T into a slice of length 1 (without copying).\n   208: #[stable(feature = \"from_ref\", since = \"1.28.0\")]\n   209: #[rustc_const_stable(feature = \"const_slice_from_ref\", since = \"1.83.0\")]\n   210: #[must_use]\n   211: pub const fn from_mut<T>(s: &mut T) -> &mut [T] {\n   212:     array::from_mut(s)\n   213: }\n   214: \n   215: /// Forms a slice from a pointer range.\n   216: ///\n   217: /// This function is useful for interacting with foreign interfaces which\n   218: /// use two pointers to refer to a range of elements in memory, as is\n   219: /// common in C++.\n   220: ///\n   221: /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::from_raw_parts_mut",
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
      "name": "from_raw_parts_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "data",
            {
              "raw_pointer": {
                "is_mutable": true,
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
            "is_mutable": true,
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
    "verification_source": "   163: /// * The memory referenced by the returned slice must not be accessed through any other pointer\n   164: ///   (not derived from the return value) for the duration of lifetime `'a`.\n   165: ///   Both read and write accesses are forbidden.\n   166: ///\n   167: /// * The total size `len * size_of::<T>()` of the slice must be no larger than `isize::MAX`,\n   168: ///   and adding that size to `data` must not \"wrap around\" the address space.\n   169: ///   See the safety documentation of [`pointer::offset`].\n   170: ///\n   171: /// [valid]: ptr#safety\n   172: /// [`NonNull::dangling()`]: ptr::NonNull::dangling\n   173: #[inline]\n   174: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   175: #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n   176: #[must_use]\n   177: #[rustc_diagnostic_item = \"slice_from_raw_parts_mut\"]\n   178: #[track_caller]\n   179: pub const unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> &'a mut [T] {\n   180:     // SAFETY: the caller must uphold the safety contract for `from_raw_parts_mut`.\n   181:     unsafe {\n   182:         ub_checks::assert_unsafe_precondition!(\n   183:             check_language_ub,\n   184:             \"slice::from_raw_parts_mut requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`\",\n   185:             (\n   186:                 data: *mut () = data as *mut (),\n   187:                 size: usize = size_of::<T>(),\n   188:                 align: usize = align_of::<T>(),\n   189:                 len: usize = len,\n   190:             ) =>\n   191:             ub_checks::maybe_is_aligned_and_not_null(data, align, false)\n   192:                 && ub_checks::is_valid_allocation_size(size, len)\n   193:         );\n   194:         &mut *ptr::slice_from_raw_parts_mut(data, len)\n   195:     }",
    "nanvix_source": "   169: ///   See the safety documentation of [`pointer::offset`].\n   170: ///\n   171: /// [valid]: ptr#safety\n   172: /// [`NonNull::dangling()`]: ptr::NonNull::dangling\n   173: #[inline]\n   174: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   175: #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n   176: #[must_use]\n   177: #[rustc_diagnostic_item = \"slice_from_raw_parts_mut\"]\n   178: #[track_caller]\n   179: pub const unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> &'a mut [T] {\n   180:     // SAFETY: the caller must uphold the safety contract for `from_raw_parts_mut`.\n   181:     unsafe {\n   182:         ub_checks::assert_unsafe_precondition!(\n   183:             check_language_ub,\n   184:             \"slice::from_raw_parts_mut requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`\",\n   185:             (\n   186:                 data: *mut () = data as *mut (),\n   187:                 size: usize = size_of::<T>(),\n   188:                 align: usize = align_of::<T>(),\n   189:                 len: usize = len,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::get_disjoint_mut",
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
                      "id": 23745,
                      "path": "GetDisjointMutIndex"
                    }
                  }
                },
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "get_disjoint_mut",
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
            "indices",
            {
              "array": {
                "len": "N",
                "type": {
                  "generic": "I"
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
                      "array": {
                        "len": "N",
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
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10080,
                        "path": "GetDisjointMutError"
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
    "verification_source": "  5193:     /// if let Ok([a, b]) = v.get_disjoint_mut([0..1, 1..3]) {\n  5194:     ///     a[0] = 8;\n  5195:     ///     b[0] = 88;\n  5196:     ///     b[1] = 888;\n  5197:     /// }\n  5198:     /// assert_eq!(v, &[8, 88, 888]);\n  5199:     ///\n  5200:     /// if let Ok([a, b]) = v.get_disjoint_mut([1..=2, 0..=0]) {\n  5201:     ///     a[0] = 11;\n  5202:     ///     a[1] = 111;\n  5203:     ///     b[0] = 1;\n  5204:     /// }\n  5205:     /// assert_eq!(v, &[1, 11, 111]);\n  5206:     /// ```\n  5207:     #[stable(feature = \"get_many_mut\", since = \"1.86.0\")]\n  5208:     #[inline]\n  5209:     pub fn get_disjoint_mut<I, const N: usize>(\n  5210:         &mut self,\n  5211:         indices: [I; N],\n  5212:     ) -> Result<[&mut I::Output; N], GetDisjointMutError>\n  5213:     where\n  5214:         I: GetDisjointMutIndex + SliceIndex<Self>,\n  5215:     {\n  5216:         get_disjoint_check_valid(&indices, self.len())?;\n  5217:         // SAFETY: The `get_disjoint_check_valid()` call checked that all indices\n  5218:         // are disjunct and in bounds.\n  5219:         unsafe { Ok(self.get_disjoint_unchecked_mut(indices)) }\n  5220:     }\n  5221: \n  5222:     /// Returns the index that an element reference points to.\n  5223:     ///\n  5224:     /// Returns `None` if `element` does not point to the start of an element within the slice.\n  5225:     ///",
    "nanvix_source": "  5206:     ///\n  5207:     /// if let Ok([a, b]) = v.get_disjoint_mut([1..=2, 0..=0]) {\n  5208:     ///     a[0] = 11;\n  5209:     ///     a[1] = 111;\n  5210:     ///     b[0] = 1;\n  5211:     /// }\n  5212:     /// assert_eq!(v, &[1, 11, 111]);\n  5213:     /// ```\n  5214:     #[stable(feature = \"get_many_mut\", since = \"1.86.0\")]\n  5215:     #[inline]\n  5216:     pub fn get_disjoint_mut<I, const N: usize>(\n  5217:         &mut self,\n  5218:         indices: [I; N],\n  5219:     ) -> Result<[&mut I::Output; N], GetDisjointMutError>\n  5220:     where\n  5221:         I: GetDisjointMutIndex + SliceIndex<Self>,\n  5222:     {\n  5223:         get_disjoint_check_valid(&indices, self.len())?;\n  5224:         // SAFETY: The `get_disjoint_check_valid()` call checked that all indices\n  5225:         // are disjunct and in bounds.\n  5226:         unsafe { Ok(self.get_disjoint_unchecked_mut(indices)) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::get_disjoint_unchecked_mut",
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
                      "id": 23745,
                      "path": "GetDisjointMutIndex"
                    }
                  }
                },
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "get_disjoint_unchecked_mut",
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
            "indices",
            {
              "array": {
                "len": "N",
                "type": {
                  "generic": "I"
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
        }
      }
    },
    "verification_source": "  5126:     /// assert_eq!(x, &[8, 88, 888]);\n  5127:     ///\n  5128:     /// unsafe {\n  5129:     ///     let [a, b] = x.get_disjoint_unchecked_mut([1..=2, 0..=0]);\n  5130:     ///     a[0] = 11;\n  5131:     ///     a[1] = 111;\n  5132:     ///     b[0] = 1;\n  5133:     /// }\n  5134:     /// assert_eq!(x, &[1, 11, 111]);\n  5135:     /// ```\n  5136:     ///\n  5137:     /// [`get_disjoint_mut`]: slice::get_disjoint_mut\n  5138:     /// [undefined behavior]: https://doc.rust-lang.org/reference/behavior-considered-undefined.html\n  5139:     #[stable(feature = \"get_many_mut\", since = \"1.86.0\")]\n  5140:     #[inline]\n  5141:     #[track_caller]\n  5142:     pub unsafe fn get_disjoint_unchecked_mut<I, const N: usize>(\n  5143:         &mut self,\n  5144:         indices: [I; N],\n  5145:     ) -> [&mut I::Output; N]\n  5146:     where\n  5147:         I: GetDisjointMutIndex + SliceIndex<Self>,\n  5148:     {\n  5149:         // NB: This implementation is written as it is because any variation of\n  5150:         // `indices.map(|i| self.get_unchecked_mut(i))` would make miri unhappy,\n  5151:         // or generate worse code otherwise. This is also why we need to go\n  5152:         // through a raw pointer here.\n  5153:         let slice: *mut [T] = self;\n  5154:         let mut arr: MaybeUninit<[&mut I::Output; N]> = MaybeUninit::uninit();\n  5155:         let arr_ptr = arr.as_mut_ptr();\n  5156: \n  5157:         // SAFETY: We expect `indices` to contain disjunct values that are\n  5158:         // in bounds of `self`.",
    "nanvix_source": "  5139:     ///     b[0] = 1;\n  5140:     /// }\n  5141:     /// assert_eq!(x, &[1, 11, 111]);\n  5142:     /// ```\n  5143:     ///\n  5144:     /// [`get_disjoint_mut`]: slice::get_disjoint_mut\n  5145:     /// [undefined behavior]: https://doc.rust-lang.org/reference/behavior-considered-undefined.html\n  5146:     #[stable(feature = \"get_many_mut\", since = \"1.86.0\")]\n  5147:     #[inline]\n  5148:     #[track_caller]\n  5149:     pub unsafe fn get_disjoint_unchecked_mut<I, const N: usize>(\n  5150:         &mut self,\n  5151:         indices: [I; N],\n  5152:     ) -> [&mut I::Output; N]\n  5153:     where\n  5154:         I: GetDisjointMutIndex + SliceIndex<Self>,\n  5155:     {\n  5156:         // NB: This implementation is written as it is because any variation of\n  5157:         // `indices.map(|i| self.get_unchecked_mut(i))` would make miri unhappy,\n  5158:         // or generate worse code otherwise. This is also why we need to go\n  5159:         // through a raw pointer here.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::get_mut",
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
    "verification_source": "   583:     ///\n   584:     /// # Examples\n   585:     ///\n   586:     /// ```\n   587:     /// let x = &mut [0, 1, 2];\n   588:     ///\n   589:     /// if let Some(elem) = x.get_mut(1) {\n   590:     ///     *elem = 42;\n   591:     /// }\n   592:     /// assert_eq!(x, &[0, 42, 2]);\n   593:     /// ```\n   594:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   595:     #[rustc_no_implicit_autorefs]\n   596:     #[inline]\n   597:     #[must_use]\n   598:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   599:     pub const fn get_mut<I>(&mut self, index: I) -> Option<&mut I::Output>\n   600:     where\n   601:         I: [const] SliceIndex<Self>,\n   602:     {\n   603:         index.get_mut(self)\n   604:     }\n   605: \n   606:     /// Returns a reference to an element or subslice, without doing bounds\n   607:     /// checking.\n   608:     ///\n   609:     /// For a safe alternative see [`get`].\n   610:     ///\n   611:     /// # Safety\n   612:     ///\n   613:     /// Calling this method with an out-of-bounds index is *[undefined behavior]*\n   614:     /// even if the resulting reference is not used.\n   615:     ///",
    "nanvix_source": "   590:     ///     *elem = 42;\n   591:     /// }\n   592:     /// assert_eq!(x, &[0, 42, 2]);\n   593:     /// ```\n   594:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   595:     #[rustc_no_implicit_autorefs]\n   596:     #[inline]\n   597:     #[must_use]\n   598:     #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   599:     #[rustc_no_writable]\n   600:     pub const fn get_mut<I>(&mut self, index: I) -> Option<&mut I::Output>\n   601:     where\n   602:         I: [const] SliceIndex<Self>,\n   603:     {\n   604:         index.get_mut(self)\n   605:     }\n   606: \n   607:     /// Returns a reference to an element or subslice, without doing bounds\n   608:     /// checking.\n   609:     ///\n   610:     /// For a safe alternative see [`get`].",
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
