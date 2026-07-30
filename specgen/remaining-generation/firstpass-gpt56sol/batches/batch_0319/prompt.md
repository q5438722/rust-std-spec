For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::vec::Vec::as_mut_ptr",
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
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2006:     /// let capacity = v.capacity();\n  2007:     /// let slice_ptr: *mut [MaybeUninit<i32>] =\n  2008:     ///     std::ptr::slice_from_raw_parts_mut(ptr.cast(), capacity);\n  2009:     /// drop(unsafe { Box::from_raw(slice_ptr) });\n  2010:     /// ```\n  2011:     ///\n  2012:     /// [`as_mut_ptr`]: Vec::as_mut_ptr\n  2013:     /// [`as_ptr`]: Vec::as_ptr\n  2014:     /// [`as_non_null`]: Vec::as_non_null\n  2015:     /// [`dealloc`]: crate::alloc::GlobalAlloc::dealloc\n  2016:     /// [`ManuallyDrop`]: core::mem::ManuallyDrop\n  2017:     #[stable(feature = \"vec_as_ptr\", since = \"1.37.0\")]\n  2018:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  2019:     #[rustc_never_returns_null_ptr]\n  2020:     #[rustc_as_ptr]\n  2021:     #[inline]\n  2022:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n  2023:         // We shadow the slice method of the same name to avoid going through\n  2024:         // `deref_mut`, which creates an intermediate reference.\n  2025:         self.buf.ptr()\n  2026:     }\n  2027: \n  2028:     /// Returns a `NonNull` pointer to the vector's buffer, or a dangling\n  2029:     /// `NonNull` pointer valid for zero sized reads if the vector didn't allocate.\n  2030:     ///\n  2031:     /// The caller must ensure that the vector outlives the pointer this\n  2032:     /// function returns, or else it will end up dangling.\n  2033:     /// Modifying the vector may cause its buffer to be reallocated,\n  2034:     /// which would also make any pointers to it invalid.\n  2035:     ///\n  2036:     /// This method guarantees that for the purpose of the aliasing model, this method\n  2037:     /// does not materialize a reference to the underlying slice, and thus the returned pointer\n  2038:     /// will remain valid when mixed with other calls to [`as_ptr`], [`as_mut_ptr`],",
    "nanvix_source": "  2048:     /// [`as_mut_ptr`]: Vec::as_mut_ptr\n  2049:     /// [`as_ptr`]: Vec::as_ptr\n  2050:     /// [`as_non_null`]: Vec::as_non_null\n  2051:     /// [`dealloc`]: crate::alloc::GlobalAlloc::dealloc\n  2052:     /// [`ManuallyDrop`]: core::mem::ManuallyDrop\n  2053:     #[stable(feature = \"vec_as_ptr\", since = \"1.37.0\")]\n  2054:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  2055:     #[rustc_never_returns_null_ptr]\n  2056:     #[rustc_as_ptr]\n  2057:     #[inline]\n  2058:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n  2059:         // We shadow the slice method of the same name to avoid going through\n  2060:         // `deref_mut`, which creates an intermediate reference.\n  2061:         self.buf.ptr()\n  2062:     }\n  2063: \n  2064:     /// Returns a `NonNull` pointer to the vector's buffer, or a dangling\n  2065:     /// `NonNull` pointer valid for zero sized reads if the vector didn't allocate.\n  2066:     ///\n  2067:     /// The caller must ensure that the vector outlives the pointer this\n  2068:     /// function returns, or else it will end up dangling.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::as_ptr",
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
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1922:     ///     let ptr2 = v.as_mut_ptr().offset(2);\n  1923:     ///     ptr2.write(2);\n  1924:     ///     // Notably, the write to `ptr2` did *not* invalidate `ptr1`\n  1925:     ///     // because it mutated a different element:\n  1926:     ///     let _ = ptr1.read();\n  1927:     /// }\n  1928:     /// ```\n  1929:     ///\n  1930:     /// [`as_mut_ptr`]: Vec::as_mut_ptr\n  1931:     /// [`as_ptr`]: Vec::as_ptr\n  1932:     /// [`as_non_null`]: Vec::as_non_null\n  1933:     #[stable(feature = \"vec_as_ptr\", since = \"1.37.0\")]\n  1934:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1935:     #[rustc_never_returns_null_ptr]\n  1936:     #[rustc_as_ptr]\n  1937:     #[inline]\n  1938:     pub const fn as_ptr(&self) -> *const T {\n  1939:         // We shadow the slice method of the same name to avoid going through\n  1940:         // `deref`, which creates an intermediate reference.\n  1941:         self.buf.ptr()\n  1942:     }\n  1943: \n  1944:     /// Returns a raw mutable pointer to the vector's buffer, or a dangling\n  1945:     /// raw pointer valid for zero sized reads if the vector didn't allocate.\n  1946:     ///\n  1947:     /// The caller must ensure that the vector outlives the pointer this\n  1948:     /// function returns, or else it will end up dangling.\n  1949:     /// Modifying the vector may cause its buffer to be reallocated,\n  1950:     /// which would also make any pointers to it invalid.\n  1951:     ///\n  1952:     /// This method guarantees that for the purpose of the aliasing model, this method\n  1953:     /// does not materialize a reference to the underlying slice, and thus the returned pointer\n  1954:     /// will remain valid when mixed with other calls to [`as_ptr`], [`as_mut_ptr`],",
    "nanvix_source": "  1964:     /// ```\n  1965:     ///\n  1966:     /// [`as_mut_ptr`]: Vec::as_mut_ptr\n  1967:     /// [`as_ptr`]: Vec::as_ptr\n  1968:     /// [`as_non_null`]: Vec::as_non_null\n  1969:     #[stable(feature = \"vec_as_ptr\", since = \"1.37.0\")]\n  1970:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1971:     #[rustc_never_returns_null_ptr]\n  1972:     #[rustc_as_ptr]\n  1973:     #[inline]\n  1974:     pub const fn as_ptr(&self) -> *const T {\n  1975:         // We shadow the slice method of the same name to avoid going through\n  1976:         // `deref`, which creates an intermediate reference.\n  1977:         self.buf.ptr()\n  1978:     }\n  1979: \n  1980:     /// Returns a raw mutable pointer to the vector's buffer, or a dangling\n  1981:     /// raw pointer valid for zero sized reads if the vector didn't allocate.\n  1982:     ///\n  1983:     /// The caller must ensure that the vector outlives the pointer this\n  1984:     /// function returns, or else it will end up dangling.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::from_raw_parts",
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
      "name": "from_raw_parts",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4892",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
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
            "length",
            {
              "primitive": "usize"
            }
          ],
          [
            "capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   628:     ///         if mem.is_null() {\n   629:     ///             return;\n   630:     ///         }\n   631:     ///\n   632:     ///         mem.write(1_000_000);\n   633:     ///\n   634:     ///         Vec::from_raw_parts(mem, 1, 16)\n   635:     ///     };\n   636:     ///\n   637:     ///     assert_eq!(vec, &[1_000_000]);\n   638:     ///     assert_eq!(vec.capacity(), 16);\n   639:     /// }\n   640:     /// ```\n   641:     #[inline]\n   642:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   643:     #[rustc_const_unstable(feature = \"const_heap\", issue = \"79597\")]\n   644:     pub const unsafe fn from_raw_parts(ptr: *mut T, length: usize, capacity: usize) -> Self {\n   645:         unsafe { Self::from_raw_parts_in(ptr, length, capacity, Global) }\n   646:     }\n   647: \n   648:     #[doc(alias = \"from_non_null_parts\")]\n   649:     /// Creates a `Vec<T>` directly from a `NonNull` pointer, a length, and a capacity.\n   650:     ///\n   651:     /// # Safety\n   652:     ///\n   653:     /// This is highly unsafe, due to the number of invariants that aren't\n   654:     /// checked:\n   655:     ///\n   656:     /// * `ptr` must have been allocated using the global allocator, such as via\n   657:     ///   the [`alloc::alloc`] function.\n   658:     /// * `T` needs to have the same alignment as what `ptr` was allocated with.\n   659:     ///   (`T` having a less strict alignment is not sufficient, the alignment really\n   660:     ///   needs to be equal to satisfy the [`dealloc`] requirement that memory must be",
    "nanvix_source": "   632:     ///         Vec::from_raw_parts(mem, 1, 16)\n   633:     ///     };\n   634:     ///\n   635:     ///     assert_eq!(vec, &[1_000_000]);\n   636:     ///     assert_eq!(vec.capacity(), 16);\n   637:     /// }\n   638:     /// ```\n   639:     #[inline]\n   640:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   641:     #[rustc_const_unstable(feature = \"const_heap\", issue = \"79597\")]\n   642:     pub const unsafe fn from_raw_parts(ptr: *mut T, length: usize, capacity: usize) -> Self {\n   643:         unsafe { Self::from_raw_parts_in(ptr, length, capacity, Global) }\n   644:     }\n   645: \n   646:     #[doc(alias = \"from_non_null_parts\")]\n   647:     /// Creates a `Vec<T>` directly from a `NonNull` pointer, a length, and a capacity.\n   648:     ///\n   649:     /// # Safety\n   650:     ///\n   651:     /// This is highly unsafe, due to the number of invariants that aren't\n   652:     /// checked:",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::into_raw_parts",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "into_raw_parts",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4892",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
          "tuple": [
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            },
            {
              "primitive": "usize"
            },
            {
              "primitive": "usize"
            }
          ]
        }
      }
    },
    "verification_source": "   826:     /// let v: Vec<i32> = vec![-1, 0, 1];\n   827:     ///\n   828:     /// let (ptr, len, cap) = v.into_raw_parts();\n   829:     ///\n   830:     /// let rebuilt = unsafe {\n   831:     ///     // We can now make changes to the components, such as\n   832:     ///     // transmuting the raw pointer to a compatible type.\n   833:     ///     let ptr = ptr as *mut u32;\n   834:     ///\n   835:     ///     Vec::from_raw_parts(ptr, len, cap)\n   836:     /// };\n   837:     /// assert_eq!(rebuilt, [4294967295, 0, 1]);\n   838:     /// ```\n   839:     #[must_use = \"losing the pointer will leak memory\"]\n   840:     #[stable(feature = \"vec_into_raw_parts\", since = \"1.93.0\")]\n   841:     #[rustc_const_unstable(feature = \"const_heap\", issue = \"79597\")]\n   842:     pub const fn into_raw_parts(self) -> (*mut T, usize, usize) {\n   843:         let mut me = ManuallyDrop::new(self);\n   844:         (me.as_mut_ptr(), me.len(), me.capacity())\n   845:     }\n   846: \n   847:     #[doc(alias = \"into_non_null_parts\")]\n   848:     /// Decomposes a `Vec<T>` into its raw components: `(NonNull pointer, length, capacity)`.\n   849:     ///\n   850:     /// Returns the `NonNull` pointer to the underlying data, the length of\n   851:     /// the vector (in elements), and the allocated capacity of the\n   852:     /// data (in elements). These are the same arguments in the same\n   853:     /// order as the arguments to [`from_parts`].\n   854:     ///\n   855:     /// After calling this function, the caller is responsible for the\n   856:     /// memory previously managed by the `Vec`. The only way to do\n   857:     /// this is to convert the `NonNull` pointer, length, and capacity back\n   858:     /// into a `Vec` with the [`from_parts`] function, allowing",
    "nanvix_source": "   830:     ///     // transmuting the raw pointer to a compatible type.\n   831:     ///     let ptr = ptr as *mut u32;\n   832:     ///\n   833:     ///     Vec::from_raw_parts(ptr, len, cap)\n   834:     /// };\n   835:     /// assert_eq!(rebuilt, [4294967295, 0, 1]);\n   836:     /// ```\n   837:     #[must_use = \"losing the pointer will leak memory\"]\n   838:     #[stable(feature = \"vec_into_raw_parts\", since = \"1.93.0\")]\n   839:     #[rustc_const_unstable(feature = \"const_heap\", issue = \"79597\")]\n   840:     pub const fn into_raw_parts(self) -> (*mut T, usize, usize) {\n   841:         let mut me = ManuallyDrop::new(self);\n   842:         (me.as_mut_ptr(), me.len(), me.capacity())\n   843:     }\n   844: \n   845:     #[doc(alias = \"into_non_null_parts\")]\n   846:     /// Decomposes a `Vec<T>` into its raw components: `(NonNull pointer, length, capacity)`.\n   847:     ///\n   848:     /// Returns the `NonNull` pointer to the underlying data, the length of\n   849:     /// the vector (in elements), and the allocated capacity of the\n   850:     /// data (in elements). These are the same arguments in the same",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::set_len",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "set_len",
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
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
          ],
          [
            "new_len",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2171:     /// // 1. `old_len..0` is empty so no elements need to be initialized.\n  2172:     /// // 2. `0 <= capacity` always holds whatever `capacity` is.\n  2173:     /// unsafe {\n  2174:     ///     vec.set_len(0);\n  2175:     /// #   // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  2176:     /// #   // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  2177:     /// #   vec.set_len(3);\n  2178:     /// }\n  2179:     /// ```\n  2180:     ///\n  2181:     /// Normally, here, one would use [`clear`] instead to correctly drop\n  2182:     /// the contents and thus not leak memory.\n  2183:     ///\n  2184:     /// [`spare_capacity_mut()`]: Vec::spare_capacity_mut\n  2185:     #[inline]\n  2186:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2187:     pub unsafe fn set_len(&mut self, new_len: usize) {\n  2188:         ub_checks::assert_unsafe_precondition!(\n  2189:             check_library_ub,\n  2190:             \"Vec::set_len requires that new_len <= capacity()\",\n  2191:             (new_len: usize = new_len, capacity: usize = self.capacity()) => new_len <= capacity\n  2192:         );\n  2193: \n  2194:         self.len = new_len;\n  2195:     }\n  2196: \n  2197:     /// Removes an element from the vector and returns it.\n  2198:     ///\n  2199:     /// The removed element is replaced by the last element of the vector.\n  2200:     ///\n  2201:     /// This does not preserve ordering of the remaining elements, but is *O*(1).\n  2202:     /// If you need to preserve the element order, use [`remove`] instead.\n  2203:     ///",
    "nanvix_source": "  2214:     /// }\n  2215:     /// ```\n  2216:     ///\n  2217:     /// Normally, here, one would use [`clear`] instead to correctly drop\n  2218:     /// the contents and thus not leak memory.\n  2219:     ///\n  2220:     /// [`spare_capacity_mut()`]: Vec::spare_capacity_mut\n  2221:     #[inline]\n  2222:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2223:     #[rustc_const_unstable(feature = \"const_heap\", issue = \"79597\")]\n  2224:     pub const unsafe fn set_len(&mut self, new_len: usize) {\n  2225:         ub_checks::assert_unsafe_precondition!(\n  2226:             check_library_ub,\n  2227:             \"Vec::set_len requires that new_len <= capacity()\",\n  2228:             (new_len: usize = new_len, capacity: usize = self.capacity()) => new_len <= capacity\n  2229:         );\n  2230: \n  2231:         self.len = new_len;\n  2232:     }\n  2233: \n  2234:     /// Removes an element from the vector and returns it.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::from_size_align_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "from_size_align_unchecked",
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
            "size",
            {
              "primitive": "usize"
            }
          ],
          [
            "align",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   116:         } else {\n   117:             Err(LayoutError)\n   118:         }\n   119:     }\n   120: \n   121:     /// Creates a layout, bypassing all checks.\n   122:     ///\n   123:     /// # Safety\n   124:     ///\n   125:     /// This function is unsafe as it does not verify the preconditions from\n   126:     /// [`Layout::from_size_align`].\n   127:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   128:     #[rustc_const_stable(feature = \"const_alloc_layout_unchecked\", since = \"1.36.0\")]\n   129:     #[must_use]\n   130:     #[inline]\n   131:     #[track_caller]\n   132:     pub const unsafe fn from_size_align_unchecked(size: usize, align: usize) -> Self {\n   133:         assert_unsafe_precondition!(\n   134:             check_library_ub,\n   135:             \"Layout::from_size_align_unchecked requires that align is a power of 2 \\\n   136:             and the rounded-up allocation size does not exceed isize::MAX\",\n   137:             (\n   138:                 size: usize = size,\n   139:                 align: usize = align,\n   140:             ) => Layout::is_size_align_valid(size, align)\n   141:         );\n   142:         // SAFETY: the caller is required to uphold the preconditions.\n   143:         unsafe { Layout { size, align: mem::transmute(align) } }\n   144:     }\n   145: \n   146:     /// Creates a layout, bypassing all checks.\n   147:     ///\n   148:     /// # Safety",
    "nanvix_source": "   122:     ///\n   123:     /// # Safety\n   124:     ///\n   125:     /// This function is unsafe as it does not verify the preconditions from\n   126:     /// [`Layout::from_size_align`].\n   127:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   128:     #[rustc_const_stable(feature = \"const_alloc_layout_unchecked\", since = \"1.36.0\")]\n   129:     #[must_use]\n   130:     #[inline]\n   131:     #[track_caller]\n   132:     pub const unsafe fn from_size_align_unchecked(size: usize, align: usize) -> Self {\n   133:         assert_unsafe_precondition!(\n   134:             check_library_ub,\n   135:             \"Layout::from_size_align_unchecked requires that align is a power of 2 \\\n   136:             and the rounded-up allocation size does not exceed isize::MAX\",\n   137:             (\n   138:                 size: usize = size,\n   139:                 align: usize = align,\n   140:             ) => Layout::is_size_align_valid(size, align)\n   141:         );\n   142:         // SAFETY: the caller is required to uphold the preconditions.",
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
