For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::alloc::alloc",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "alloc",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 70,
                "path": "Layout"
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
    "verification_source": "    79: ///     let layout = Layout::new::<u16>();\n    80: ///     let ptr = alloc(layout);\n    81: ///     if ptr.is_null() {\n    82: ///         handle_alloc_error(layout);\n    83: ///     }\n    84: ///\n    85: ///     *(ptr as *mut u16) = 42;\n    86: ///     assert_eq!(*(ptr as *mut u16), 42);\n    87: ///\n    88: ///     dealloc(ptr, layout);\n    89: /// }\n    90: /// ```\n    91: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n    92: #[must_use = \"losing the pointer will leak memory\"]\n    93: #[inline]\n    94: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n    95: pub unsafe fn alloc(layout: Layout) -> *mut u8 {\n    96:     unsafe {\n    97:         // Make sure we don't accidentally allow omitting the allocator shim in\n    98:         // stable code until it is actually stabilized.\n    99:         __rust_no_alloc_shim_is_unstable_v2();\n   100: \n   101:         __rust_alloc(layout.size(), layout.alignment())\n   102:     }\n   103: }\n   104: \n   105: /// Deallocates memory with the global allocator.\n   106: ///\n   107: /// This function forwards calls to the [`GlobalAlloc::dealloc`] method\n   108: /// of the allocator registered with the `#[global_allocator]` attribute\n   109: /// if there is one, or the `std` crate\u2019s default.\n   110: ///\n   111: /// This function is expected to be deprecated in favor of the `deallocate` method",
    "nanvix_source": "    85: ///     *(ptr as *mut u16) = 42;\n    86: ///     assert_eq!(*(ptr as *mut u16), 42);\n    87: ///\n    88: ///     dealloc(ptr, layout);\n    89: /// }\n    90: /// ```\n    91: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n    92: #[must_use = \"losing the pointer will leak memory\"]\n    93: #[inline]\n    94: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n    95: pub unsafe fn alloc(layout: Layout) -> *mut u8 {\n    96:     unsafe {\n    97:         // Make sure we don't accidentally allow omitting the allocator shim in\n    98:         // stable code until it is actually stabilized.\n    99:         __rust_no_alloc_shim_is_unstable_v2();\n   100: \n   101:         __rust_alloc(layout.size(), layout.alignment())\n   102:     }\n   103: }\n   104: \n   105: /// Deallocates memory with the global allocator.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::alloc::alloc_zeroed",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "alloc_zeroed",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 70,
                "path": "Layout"
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
    "verification_source": "   176: /// unsafe {\n   177: ///     let layout = Layout::new::<u16>();\n   178: ///     let ptr = alloc_zeroed(layout);\n   179: ///     if ptr.is_null() {\n   180: ///         handle_alloc_error(layout);\n   181: ///     }\n   182: ///\n   183: ///     assert_eq!(*(ptr as *mut u16), 0);\n   184: ///\n   185: ///     dealloc(ptr, layout);\n   186: /// }\n   187: /// ```\n   188: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   189: #[must_use = \"losing the pointer will leak memory\"]\n   190: #[inline]\n   191: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   192: pub unsafe fn alloc_zeroed(layout: Layout) -> *mut u8 {\n   193:     unsafe {\n   194:         // Make sure we don't accidentally allow omitting the allocator shim in\n   195:         // stable code until it is actually stabilized.\n   196:         __rust_no_alloc_shim_is_unstable_v2();\n   197: \n   198:         __rust_alloc_zeroed(layout.size(), layout.alignment())\n   199:     }\n   200: }\n   201: \n   202: impl Global {\n   203:     #[inline]\n   204:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   205:     fn alloc_impl_runtime(layout: Layout, zeroed: bool) -> Result<NonNull<[u8]>, AllocError> {\n   206:         match layout.size() {\n   207:             0 => Ok(NonNull::slice_from_raw_parts(layout.dangling_ptr(), 0)),\n   208:             // SAFETY: `layout` is non-zero in size,",
    "nanvix_source": "   182: ///\n   183: ///     assert_eq!(*(ptr as *mut u16), 0);\n   184: ///\n   185: ///     dealloc(ptr, layout);\n   186: /// }\n   187: /// ```\n   188: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   189: #[must_use = \"losing the pointer will leak memory\"]\n   190: #[inline]\n   191: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   192: pub unsafe fn alloc_zeroed(layout: Layout) -> *mut u8 {\n   193:     unsafe {\n   194:         // Make sure we don't accidentally allow omitting the allocator shim in\n   195:         // stable code until it is actually stabilized.\n   196:         __rust_no_alloc_shim_is_unstable_v2();\n   197: \n   198:         __rust_alloc_zeroed(layout.size(), layout.alignment())\n   199:     }\n   200: }\n   201: \n   202: impl Global {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::alloc::dealloc",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
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
        "is_unsafe": true
      },
      "name": "dealloc",
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
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "u8"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 70,
                "path": "Layout"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   104: \n   105: /// Deallocates memory with the global allocator.\n   106: ///\n   107: /// This function forwards calls to the [`GlobalAlloc::dealloc`] method\n   108: /// of the allocator registered with the `#[global_allocator]` attribute\n   109: /// if there is one, or the `std` crate\u2019s default.\n   110: ///\n   111: /// This function is expected to be deprecated in favor of the `deallocate` method\n   112: /// of the [`Global`] type when it and the [`Allocator`] trait become stable.\n   113: ///\n   114: /// # Safety\n   115: ///\n   116: /// See [`GlobalAlloc::dealloc`].\n   117: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   118: #[inline]\n   119: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   120: pub unsafe fn dealloc(ptr: *mut u8, layout: Layout) {\n   121:     unsafe { dealloc_nonnull(NonNull::new_unchecked(ptr), layout) }\n   122: }\n   123: \n   124: /// Same as [`dealloc`] but when you already have a non-null pointer\n   125: #[inline]\n   126: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   127: unsafe fn dealloc_nonnull(ptr: NonNull<u8>, layout: Layout) {\n   128:     unsafe { __rust_dealloc(ptr, layout.size(), layout.alignment()) }\n   129: }\n   130: \n   131: /// Reallocates memory with the global allocator.\n   132: ///\n   133: /// This function forwards calls to the [`GlobalAlloc::realloc`] method\n   134: /// of the allocator registered with the `#[global_allocator]` attribute\n   135: /// if there is one, or the `std` crate\u2019s default.\n   136: ///",
    "nanvix_source": "   110: ///\n   111: /// This function is expected to be deprecated in favor of the `deallocate` method\n   112: /// of the [`Global`] type when it and the [`Allocator`] trait become stable.\n   113: ///\n   114: /// # Safety\n   115: ///\n   116: /// See [`GlobalAlloc::dealloc`].\n   117: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   118: #[inline]\n   119: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   120: pub unsafe fn dealloc(ptr: *mut u8, layout: Layout) {\n   121:     unsafe { dealloc_nonnull(NonNull::new_unchecked(ptr), layout) }\n   122: }\n   123: \n   124: /// Same as [`dealloc`] but when you already have a non-null pointer\n   125: #[inline]\n   126: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   127: unsafe fn dealloc_nonnull(ptr: NonNull<u8>, layout: Layout) {\n   128:     unsafe { __rust_dealloc(ptr, layout.size(), layout.alignment()) }\n   129: }\n   130: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::alloc::realloc",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "realloc",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "u8"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 70,
                "path": "Layout"
              }
            }
          ],
          [
            "new_size",
            {
              "primitive": "usize"
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
    "verification_source": "   131: /// Reallocates memory with the global allocator.\n   132: ///\n   133: /// This function forwards calls to the [`GlobalAlloc::realloc`] method\n   134: /// of the allocator registered with the `#[global_allocator]` attribute\n   135: /// if there is one, or the `std` crate\u2019s default.\n   136: ///\n   137: /// This function is expected to be deprecated in favor of the `grow` and `shrink` methods\n   138: /// of the [`Global`] type when it and the [`Allocator`] trait become stable.\n   139: ///\n   140: /// # Safety\n   141: ///\n   142: /// See [`GlobalAlloc::realloc`].\n   143: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   144: #[must_use = \"losing the pointer will leak memory\"]\n   145: #[inline]\n   146: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   147: pub unsafe fn realloc(ptr: *mut u8, layout: Layout, new_size: usize) -> *mut u8 {\n   148:     unsafe { realloc_nonnull(NonNull::new_unchecked(ptr), layout, new_size) }\n   149: }\n   150: \n   151: /// Same as [`realloc`] but when you already have a non-null pointer\n   152: #[inline]\n   153: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   154: unsafe fn realloc_nonnull(ptr: NonNull<u8>, layout: Layout, new_size: usize) -> *mut u8 {\n   155:     unsafe { __rust_realloc(ptr, layout.size(), layout.alignment(), new_size) }\n   156: }\n   157: \n   158: /// Allocates zero-initialized memory with the global allocator.\n   159: ///\n   160: /// This function forwards calls to the [`GlobalAlloc::alloc_zeroed`] method\n   161: /// of the allocator registered with the `#[global_allocator]` attribute\n   162: /// if there is one, or the `std` crate\u2019s default.\n   163: ///",
    "nanvix_source": "   137: /// This function is expected to be deprecated in favor of the `grow` and `shrink` methods\n   138: /// of the [`Global`] type when it and the [`Allocator`] trait become stable.\n   139: ///\n   140: /// # Safety\n   141: ///\n   142: /// See [`GlobalAlloc::realloc`].\n   143: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   144: #[must_use = \"losing the pointer will leak memory\"]\n   145: #[inline]\n   146: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   147: pub unsafe fn realloc(ptr: *mut u8, layout: Layout, new_size: usize) -> *mut u8 {\n   148:     unsafe { realloc_nonnull(NonNull::new_unchecked(ptr), layout, new_size) }\n   149: }\n   150: \n   151: /// Same as [`realloc`] but when you already have a non-null pointer\n   152: #[inline]\n   153: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   154: unsafe fn realloc_nonnull(ptr: NonNull<u8>, layout: Layout, new_size: usize) -> *mut u8 {\n   155:     unsafe { __rust_realloc(ptr, layout.size(), layout.alignment(), new_size) }\n   156: }\n   157: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::as_mut_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_mut_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "b"
        ],
        "return_is_raw_pointer": true,
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "Box"
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
                          "id": 29,
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:494",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "b",
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
    "verification_source": "  1741:     ///     let mut b = Box::new(0);\n  1742:     ///     let ptr1 = Box::as_mut_ptr(&mut b);\n  1743:     ///     ptr1.write(1);\n  1744:     ///     let ptr2 = Box::as_mut_ptr(&mut b);\n  1745:     ///     ptr2.write(2);\n  1746:     ///     // Notably, the write to `ptr2` did *not* invalidate `ptr1`:\n  1747:     ///     ptr1.write(3);\n  1748:     /// }\n  1749:     /// ```\n  1750:     ///\n  1751:     /// [`as_mut_ptr`]: Self::as_mut_ptr\n  1752:     /// [`as_ptr`]: Self::as_ptr\n  1753:     #[unstable(feature = \"box_as_ptr\", issue = \"129090\")]\n  1754:     #[rustc_never_returns_null_ptr]\n  1755:     #[rustc_as_ptr]\n  1756:     #[inline]\n  1757:     pub fn as_mut_ptr(b: &mut Self) -> *mut T {\n  1758:         // This is a primitive deref, not going through `DerefMut`, and therefore not materializing\n  1759:         // any references.\n  1760:         &raw mut **b\n  1761:     }\n  1762: \n  1763:     /// Returns a raw pointer to the `Box`'s contents.\n  1764:     ///\n  1765:     /// The caller must ensure that the `Box` outlives the pointer this\n  1766:     /// function returns, or else it will end up dangling.\n  1767:     ///\n  1768:     /// The caller must also ensure that the memory the pointer (non-transitively) points to\n  1769:     /// is never written to (except inside an `UnsafeCell`) using this pointer or any pointer\n  1770:     /// derived from it. If you need to mutate the contents of the `Box`, use [`as_mut_ptr`].\n  1771:     ///\n  1772:     /// This method guarantees that for the purpose of the aliasing model, this method\n  1773:     /// does not materialize a reference to the underlying memory, and thus the returned pointer",
    "nanvix_source": "  1777:     /// ```\n  1778:     ///\n  1779:     /// [`as_mut_ptr`]: Self::as_mut_ptr\n  1780:     /// [`as_ptr`]: Self::as_ptr\n  1781:     /// [`as_non_null`]: Self::as_non_null\n  1782:     #[must_use]\n  1783:     #[stable(feature = \"box_as_ptr\", since = \"CURRENT_RUSTC_VERSION\")]\n  1784:     #[rustc_never_returns_null_ptr]\n  1785:     #[rustc_as_ptr]\n  1786:     #[inline]\n  1787:     pub fn as_mut_ptr(b: &mut Self) -> *mut T {\n  1788:         // This is a primitive deref, not going through `DerefMut`, and therefore not materializing\n  1789:         // any references.\n  1790:         &raw mut **b\n  1791:     }\n  1792: \n  1793:     /// Returns a raw pointer to the `Box`'s contents.\n  1794:     ///\n  1795:     /// The caller must ensure that the `Box` outlives the pointer this\n  1796:     /// function returns, or else it will end up dangling.\n  1797:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
        "is_const": false,
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "Box"
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
                          "id": 29,
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:494",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "b",
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
    "verification_source": "  1790:     ///     let _val = ptr2.read();\n  1791:     ///     // No write to this memory has happened yet, so `ptr1` is still valid.\n  1792:     ///     let _val = ptr1.read();\n  1793:     ///     // However, once we do a write...\n  1794:     ///     ptr2.write(1);\n  1795:     ///     // ... `ptr1` is no longer valid.\n  1796:     ///     // This would be UB: let _val = ptr1.read();\n  1797:     /// }\n  1798:     /// ```\n  1799:     ///\n  1800:     /// [`as_mut_ptr`]: Self::as_mut_ptr\n  1801:     /// [`as_ptr`]: Self::as_ptr\n  1802:     #[unstable(feature = \"box_as_ptr\", issue = \"129090\")]\n  1803:     #[rustc_never_returns_null_ptr]\n  1804:     #[rustc_as_ptr]\n  1805:     #[inline]\n  1806:     pub fn as_ptr(b: &Self) -> *const T {\n  1807:         // This is a primitive deref, not going through `DerefMut`, and therefore not materializing\n  1808:         // any references.\n  1809:         &raw const **b\n  1810:     }\n  1811: \n  1812:     /// Returns a reference to the underlying allocator.\n  1813:     ///\n  1814:     /// Note: this is an associated function, which means that you have\n  1815:     /// to call it as `Box::allocator(&b)` instead of `b.allocator()`. This\n  1816:     /// is so that there is no conflict with a method on the inner type.\n  1817:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  1818:     #[inline]\n  1819:     pub fn allocator(b: &Self) -> &A {\n  1820:         &b.1\n  1821:     }\n  1822: ",
    "nanvix_source": "  1826:     /// ```\n  1827:     ///\n  1828:     /// [`as_mut_ptr`]: Self::as_mut_ptr\n  1829:     /// [`as_ptr`]: Self::as_ptr\n  1830:     /// [`as_non_null`]: Self::as_non_null\n  1831:     #[must_use]\n  1832:     #[stable(feature = \"box_as_ptr\", since = \"CURRENT_RUSTC_VERSION\")]\n  1833:     #[rustc_never_returns_null_ptr]\n  1834:     #[rustc_as_ptr]\n  1835:     #[inline]\n  1836:     pub fn as_ptr(b: &Self) -> *const T {\n  1837:         // This is a primitive deref, not going through `DerefMut`, and therefore not materializing\n  1838:         // any references.\n  1839:         &raw const **b\n  1840:     }\n  1841: \n  1842:     /// Returns a `NonNull` pointer to the `Box`'s contents.\n  1843:     ///\n  1844:     /// The caller must ensure that the `Box` outlives the pointer this\n  1845:     /// function returns, or else it will end up dangling.\n  1846:     ///",
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
