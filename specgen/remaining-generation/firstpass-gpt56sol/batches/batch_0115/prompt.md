For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::alloc::Layout::size",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "size",
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
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   159:             \"Layout::from_size_alignment_unchecked requires \\\n   160:             that the rounded-up allocation size does not exceed isize::MAX\",\n   161:             (\n   162:                 size: usize = size,\n   163:                 alignment: Alignment = alignment,\n   164:             ) => Layout::is_size_alignment_valid(size, alignment)\n   165:         );\n   166:         // SAFETY: the caller is required to uphold the preconditions.\n   167:         Layout { size, align: alignment }\n   168:     }\n   169: \n   170:     /// The minimum size in bytes for a memory block of this layout.\n   171:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   172:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   173:     #[must_use]\n   174:     #[inline]\n   175:     pub const fn size(&self) -> usize {\n   176:         self.size\n   177:     }\n   178: \n   179:     /// The minimum byte alignment for a memory block of this layout.\n   180:     ///\n   181:     /// The returned alignment is guaranteed to be a power of two.\n   182:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   183:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   184:     #[must_use = \"this returns the minimum alignment, \\\n   185:                   without modifying the layout\"]\n   186:     #[inline]\n   187:     pub const fn align(&self) -> usize {\n   188:         self.align.as_usize()\n   189:     }\n   190: \n   191:     /// The minimum byte alignment for a memory block of this layout.",
    "nanvix_source": "   165:         );\n   166:         // SAFETY: the caller is required to uphold the preconditions.\n   167:         Layout { size, align: alignment }\n   168:     }\n   169: \n   170:     /// The minimum size in bytes for a memory block of this layout.\n   171:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   172:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   173:     #[must_use]\n   174:     #[inline]\n   175:     pub const fn size(&self) -> usize {\n   176:         self.size\n   177:     }\n   178: \n   179:     /// The minimum byte alignment for a memory block of this layout.\n   180:     ///\n   181:     /// The returned alignment is guaranteed to be a power of two.\n   182:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   183:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   184:     #[must_use = \"this returns the minimum alignment, \\\n   185:                   without modifying the layout\"]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::IntoIter::as_slice",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_slice",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "const": {
                      "expr": "N",
                      "is_literal": false,
                      "value": null
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9764,
            "path": "IntoIter"
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
        "impl_id": "core:24280",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9764",
        "resolved_owner_path": [
          "core",
          "array",
          "iter",
          "IntoIter"
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
    "verification_source": "   199:     /// }\n   200:     ///\n   201:     /// assert_eq!(get_bytes(true).collect::<Vec<_>>(), vec![1, 2, 3, 4]);\n   202:     /// assert_eq!(get_bytes(false).collect::<Vec<_>>(), vec![]);\n   203:     /// ```\n   204:     #[unstable(feature = \"array_into_iter_constructors\", issue = \"91583\")]\n   205:     #[inline]\n   206:     pub const fn empty() -> Self {\n   207:         let inner = InnerSized::empty();\n   208:         IntoIter { inner: ManuallyDrop::new(inner) }\n   209:     }\n   210: \n   211:     /// Returns an immutable slice of all elements that have not been yielded\n   212:     /// yet.\n   213:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   214:     #[inline]\n   215:     pub fn as_slice(&self) -> &[T] {\n   216:         self.unsize().as_slice()\n   217:     }\n   218: \n   219:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   220:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   221:     #[inline]\n   222:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   223:         self.unsize_mut().as_mut_slice()\n   224:     }\n   225: }\n   226: \n   227: #[stable(feature = \"array_value_iter_default\", since = \"1.89.0\")]\n   228: impl<T, const N: usize> Default for IntoIter<T, N> {\n   229:     fn default() -> Self {\n   230:         IntoIter::empty()\n   231:     }",
    "nanvix_source": "   210:     #[inline]\n   211:     pub const fn empty() -> Self {\n   212:         let inner = InnerSized::empty();\n   213:         IntoIter { inner: ManuallyDrop::new(inner) }\n   214:     }\n   215: \n   216:     /// Returns an immutable slice of all elements that have not been yielded\n   217:     /// yet.\n   218:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   219:     #[inline]\n   220:     pub fn as_slice(&self) -> &[T] {\n   221:         self.unsize().as_slice()\n   222:     }\n   223: \n   224:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   225:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   226:     #[inline]\n   227:     #[rustc_const_unstable(feature = \"const_iter\", issue = \"92476\")]\n   228:     pub const fn as_mut_slice(&mut self) -> &mut [T] {\n   229:         self.unsize_mut().as_mut_slice()\n   230:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::IntoIter::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "new",
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
                    "const": {
                      "expr": "N",
                      "is_literal": false,
                      "value": null
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9764,
            "path": "IntoIter"
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
        "impl_id": "core:24280",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9764",
        "resolved_owner_path": [
          "core",
          "array",
          "iter",
          "IntoIter"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "array",
            {
              "array": {
                "len": "N",
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "    64:         // With that, this initialization satisfies the invariants.\n    65:         //\n    66:         // FIXME: If normal `transmute` ever gets smart enough to allow this\n    67:         // directly, use it instead of `transmute_unchecked`.\n    68:         let data: [MaybeUninit<T>; N] = unsafe { transmute_unchecked(self) };\n    69:         // SAFETY: The original array was entirely initialized and the alive\n    70:         // range we're passing here represents that fact.\n    71:         let inner = unsafe { InnerSized::new_unchecked(IndexRange::zero_to(N), data) };\n    72:         IntoIter { inner: ManuallyDrop::new(inner) }\n    73:     }\n    74: }\n    75: \n    76: impl<T, const N: usize> IntoIter<T, N> {\n    77:     /// Creates a new iterator over the given `array`.\n    78:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n    79:     #[deprecated(since = \"1.59.0\", note = \"use `IntoIterator::into_iter` instead\")]\n    80:     pub fn new(array: [T; N]) -> Self {\n    81:         IntoIterator::into_iter(array)\n    82:     }\n    83: \n    84:     /// Creates an iterator over the elements in a partially-initialized buffer.\n    85:     ///\n    86:     /// If you have a fully-initialized array, then use [`IntoIterator`].\n    87:     /// But this is useful for returning partial results from unsafe code.\n    88:     ///\n    89:     /// # Safety\n    90:     ///\n    91:     /// - The `buffer[initialized]` elements must all be initialized.\n    92:     /// - The range must be canonical, with `initialized.start <= initialized.end`.\n    93:     /// - The range must be in-bounds for the buffer, with `initialized.end <= N`.\n    94:     ///   (Like how indexing `[0][100..100]` fails despite the range being empty.)\n    95:     ///\n    96:     /// It's sound to have more elements initialized than mentioned, though that",
    "nanvix_source": "    75:         // range we're passing here represents that fact.\n    76:         let inner = unsafe { InnerSized::new_unchecked(IndexRange::zero_to(N), data) };\n    77:         IntoIter { inner: ManuallyDrop::new(inner) }\n    78:     }\n    79: }\n    80: \n    81: impl<T, const N: usize> IntoIter<T, N> {\n    82:     /// Creates a new iterator over the given `array`.\n    83:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n    84:     #[deprecated(since = \"1.59.0\", note = \"use `IntoIterator::into_iter` instead\")]\n    85:     pub fn new(array: [T; N]) -> Self {\n    86:         IntoIterator::into_iter(array)\n    87:     }\n    88: \n    89:     /// Creates an iterator over the elements in a partially-initialized buffer.\n    90:     ///\n    91:     /// If you have a fully-initialized array, then use [`IntoIterator`].\n    92:     /// But this is useful for returning partial results from unsafe code.\n    93:     ///\n    94:     /// # Safety\n    95:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::as_array_of_cells",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_array_of_cells",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "array": {
                        "len": "N",
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
        "impl_id": "core:24756",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "array": {
                "len": "N",
                "type": {
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
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   736: }\n   737: \n   738: impl<T, const N: usize> Cell<[T; N]> {\n   739:     /// Returns a `&[Cell<T>; N]` from a `&Cell<[T; N]>`\n   740:     ///\n   741:     /// # Examples\n   742:     ///\n   743:     /// ```\n   744:     /// use std::cell::Cell;\n   745:     ///\n   746:     /// let mut array: [i32; 3] = [1, 2, 3];\n   747:     /// let cell_array: &Cell<[i32; 3]> = Cell::from_mut(&mut array);\n   748:     /// let array_cell: &[Cell<i32>; 3] = cell_array.as_array_of_cells();\n   749:     /// ```\n   750:     #[stable(feature = \"as_array_of_cells\", since = \"1.91.0\")]\n   751:     #[rustc_const_stable(feature = \"as_array_of_cells\", since = \"1.91.0\")]\n   752:     pub const fn as_array_of_cells(&self) -> &[Cell<T>; N] {\n   753:         // SAFETY: `Cell<T>` has the same memory layout as `T`.\n   754:         unsafe { &*(self as *const Cell<[T; N]> as *const [Cell<T>; N]) }\n   755:     }\n   756: }\n   757: \n   758: /// Types for which cloning `Cell<Self>` is sound.\n   759: ///\n   760: /// # Safety\n   761: ///\n   762: /// Implementing this trait for a type is sound if and only if the following code is sound for T =\n   763: /// that type.\n   764: ///\n   765: /// ```\n   766: /// #![feature(cell_get_cloned)]\n   767: /// # use std::cell::{CloneFromCell, Cell};\n   768: /// fn clone_from_cell<T: CloneFromCell>(cell: &Cell<T>) -> T {",
    "nanvix_source": "   742:     ///\n   743:     /// ```\n   744:     /// use std::cell::Cell;\n   745:     ///\n   746:     /// let mut array: [i32; 3] = [1, 2, 3];\n   747:     /// let cell_array: &Cell<[i32; 3]> = Cell::from_mut(&mut array);\n   748:     /// let array_cell: &[Cell<i32>; 3] = cell_array.as_array_of_cells();\n   749:     /// ```\n   750:     #[stable(feature = \"as_array_of_cells\", since = \"1.91.0\")]\n   751:     #[rustc_const_stable(feature = \"as_array_of_cells\", since = \"1.91.0\")]\n   752:     pub const fn as_array_of_cells(&self) -> &[Cell<T>; N] {\n   753:         // SAFETY: `Cell<T>` has the same memory layout as `T`.\n   754:         unsafe { &*(self as *const Cell<[T; N]> as *const [Cell<T>; N]) }\n   755:     }\n   756: }\n   757: \n   758: /// Types for which cloning `Cell<Self>` is sound.\n   759: ///\n   760: /// # Safety\n   761: ///\n   762: /// Implementing this trait for a type is sound if and only if the following code is sound for T =",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::as_slice_of_cells",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_slice_of_cells",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "slice": {
                        "generic": "T"
                      }
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
        "impl_id": "core:24754",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
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
                  "id": 9785,
                  "path": "Cell"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   716: impl<T> Cell<[T]> {\n   717:     /// Returns a `&[Cell<T>]` from a `&Cell<[T]>`\n   718:     ///\n   719:     /// # Examples\n   720:     ///\n   721:     /// ```\n   722:     /// use std::cell::Cell;\n   723:     ///\n   724:     /// let slice: &mut [i32] = &mut [1, 2, 3];\n   725:     /// let cell_slice: &Cell<[i32]> = Cell::from_mut(slice);\n   726:     /// let slice_cell: &[Cell<i32>] = cell_slice.as_slice_of_cells();\n   727:     ///\n   728:     /// assert_eq!(slice_cell.len(), 3);\n   729:     /// ```\n   730:     #[stable(feature = \"as_cell\", since = \"1.37.0\")]\n   731:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   732:     pub const fn as_slice_of_cells(&self) -> &[Cell<T>] {\n   733:         // SAFETY: `Cell<T>` has the same memory layout as `T`.\n   734:         unsafe { &*(self as *const Cell<[T]> as *const [Cell<T>]) }\n   735:     }\n   736: }\n   737: \n   738: impl<T, const N: usize> Cell<[T; N]> {\n   739:     /// Returns a `&[Cell<T>; N]` from a `&Cell<[T; N]>`\n   740:     ///\n   741:     /// # Examples\n   742:     ///\n   743:     /// ```\n   744:     /// use std::cell::Cell;\n   745:     ///\n   746:     /// let mut array: [i32; 3] = [1, 2, 3];\n   747:     /// let cell_array: &Cell<[i32; 3]> = Cell::from_mut(&mut array);\n   748:     /// let array_cell: &[Cell<i32>; 3] = cell_array.as_array_of_cells();",
    "nanvix_source": "   722:     /// use std::cell::Cell;\n   723:     ///\n   724:     /// let slice: &mut [i32] = &mut [1, 2, 3];\n   725:     /// let cell_slice: &Cell<[i32]> = Cell::from_mut(slice);\n   726:     /// let slice_cell: &[Cell<i32>] = cell_slice.as_slice_of_cells();\n   727:     ///\n   728:     /// assert_eq!(slice_cell.len(), 3);\n   729:     /// ```\n   730:     #[stable(feature = \"as_cell\", since = \"1.37.0\")]\n   731:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   732:     pub const fn as_slice_of_cells(&self) -> &[Cell<T>] {\n   733:         // SAFETY: `Cell<T>` has the same memory layout as `T`.\n   734:         unsafe { &*(self as *const Cell<[T]> as *const [Cell<T>]) }\n   735:     }\n   736: }\n   737: \n   738: impl<T, const N: usize> Cell<[T; N]> {\n   739:     /// Returns a `&[Cell<T>; N]` from a `&Cell<[T; N]>`\n   740:     ///\n   741:     /// # Examples\n   742:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Cell::from_mut",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "t"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
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
            "t",
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
            "is_mutable": false,
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
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 9785,
                "path": "Cell"
              }
            }
          }
        }
      }
    },
    "verification_source": "   633:     /// Returns a `&Cell<T>` from a `&mut T`\n   634:     ///\n   635:     /// # Examples\n   636:     ///\n   637:     /// ```\n   638:     /// use std::cell::Cell;\n   639:     ///\n   640:     /// let slice: &mut [i32] = &mut [1, 2, 3];\n   641:     /// let cell_slice: &Cell<[i32]> = Cell::from_mut(slice);\n   642:     /// let slice_cell: &[Cell<i32>] = cell_slice.as_slice_of_cells();\n   643:     ///\n   644:     /// assert_eq!(slice_cell.len(), 3);\n   645:     /// ```\n   646:     #[inline]\n   647:     #[stable(feature = \"as_cell\", since = \"1.37.0\")]\n   648:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   649:     pub const fn from_mut(t: &mut T) -> &Cell<T> {\n   650:         // SAFETY: `&mut` ensures unique access.\n   651:         unsafe { &*(t as *mut T as *const Cell<T>) }\n   652:     }\n   653: }\n   654: \n   655: impl<T: Default> Cell<T> {\n   656:     /// Takes the value of the cell, leaving `Default::default()` in its place.\n   657:     ///\n   658:     /// # Examples\n   659:     ///\n   660:     /// ```\n   661:     /// use std::cell::Cell;\n   662:     ///\n   663:     /// let c = Cell::new(5);\n   664:     /// let five = c.take();\n   665:     ///",
    "nanvix_source": "   639:     ///\n   640:     /// let slice: &mut [i32] = &mut [1, 2, 3];\n   641:     /// let cell_slice: &Cell<[i32]> = Cell::from_mut(slice);\n   642:     /// let slice_cell: &[Cell<i32>] = cell_slice.as_slice_of_cells();\n   643:     ///\n   644:     /// assert_eq!(slice_cell.len(), 3);\n   645:     /// ```\n   646:     #[inline]\n   647:     #[stable(feature = \"as_cell\", since = \"1.37.0\")]\n   648:     #[rustc_const_stable(feature = \"const_cell\", since = \"1.88.0\")]\n   649:     pub const fn from_mut(t: &mut T) -> &Cell<T> {\n   650:         // SAFETY: `&mut` ensures unique access.\n   651:         unsafe { &*(t as *mut T as *const Cell<T>) }\n   652:     }\n   653: }\n   654: \n   655: impl<T: Default> Cell<T> {\n   656:     /// Takes the value of the cell, leaving `Default::default()` in its place.\n   657:     ///\n   658:     /// # Examples\n   659:     ///",
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
