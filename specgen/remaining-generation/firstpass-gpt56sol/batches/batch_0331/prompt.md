For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::byte_offset_from_unsigned",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "multiple_rust_declarations_share_path"
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
            "name": "U"
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
      "name": "byte_offset_from_unsigned",
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
          "raw_pointer": {
            "is_mutable": false,
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:51637",
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
              "generic": "Self"
            }
          ],
          [
            "origin",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "U"
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
    "verification_source": "   730:     }\n   731: \n   732:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   733:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   734:     /// units of **bytes**.\n   735:     ///\n   736:     /// This is purely a convenience for casting to a `u8` pointer and\n   737:     /// using [`offset_from_unsigned`][pointer::offset_from_unsigned] on it.\n   738:     /// See that method for documentation and safety requirements.\n   739:     ///\n   740:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   741:     /// ignoring the metadata.\n   742:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   743:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   744:     #[inline]\n   745:     #[track_caller]\n   746:     pub const unsafe fn byte_offset_from_unsigned<U: ?Sized>(self, origin: *const U) -> usize {\n   747:         // SAFETY: the caller must uphold the safety contract for `offset_from_unsigned`.\n   748:         unsafe { self.cast::<u8>().offset_from_unsigned(origin.cast::<u8>()) }\n   749:     }\n   750: \n   751:     /// Returns whether two pointers are guaranteed to be equal.\n   752:     ///\n   753:     /// At runtime this function behaves like `Some(self == other)`.\n   754:     /// However, in some contexts (e.g., compile-time evaluation),\n   755:     /// it is not always possible to determine equality of two pointers, so this function may\n   756:     /// spuriously return `None` for pointers that later actually turn out to have its equality known.\n   757:     /// But when it returns `Some`, the pointers' equality is guaranteed to be known.\n   758:     ///\n   759:     /// The return value may change from `Some` to `None` and vice versa depending on the compiler\n   760:     /// version and unsafe code must not\n   761:     /// rely on the result of this function for soundness. It is suggested to only use this function\n   762:     /// for performance optimizations where spurious `None` return values by this function do not",
    "nanvix_source": "   741:     /// This is purely a convenience for casting to a `u8` pointer and\n   742:     /// using [`offset_from_unsigned`][pointer::offset_from_unsigned] on it.\n   743:     /// See that method for documentation and safety requirements.\n   744:     ///\n   745:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   746:     /// ignoring the metadata.\n   747:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   748:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   749:     #[inline]\n   750:     #[track_caller]\n   751:     pub const unsafe fn byte_offset_from_unsigned<U: ?Sized>(self, origin: *const U) -> usize {\n   752:         // SAFETY: the caller must uphold the safety contract for `offset_from_unsigned`.\n   753:         unsafe { self.cast::<u8>().offset_from_unsigned(origin.cast::<u8>()) }\n   754:     }\n   755: \n   756:     /// Returns whether two pointers are guaranteed to be equal.\n   757:     ///\n   758:     /// At runtime this function behaves like `Some(self == other)`.\n   759:     /// However, in some contexts (e.g., compile-time evaluation),\n   760:     /// it is not always possible to determine equality of two pointers, so this function may\n   761:     /// spuriously return `None` for pointers that later actually turn out to have its equality known.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::byte_sub",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "multiple_rust_declarations_share_path"
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
      "name": "byte_sub",
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
          "raw_pointer": {
            "is_mutable": false,
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:51637",
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
              "generic": "Self"
            }
          ],
          [
            "count",
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
    "verification_source": "   977: \n   978:     /// Subtracts an unsigned offset in bytes from a pointer.\n   979:     ///\n   980:     /// `count` is in units of bytes.\n   981:     ///\n   982:     /// This is purely a convenience for casting to a `u8` pointer and\n   983:     /// using [sub][pointer::sub] on it. See that method for documentation\n   984:     /// and safety requirements.\n   985:     ///\n   986:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   987:     /// leaving the metadata untouched.\n   988:     #[must_use]\n   989:     #[inline(always)]\n   990:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   991:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   992:     #[track_caller]\n   993:     pub const unsafe fn byte_sub(self, count: usize) -> Self {\n   994:         // SAFETY: the caller must uphold the safety contract for `sub`.\n   995:         unsafe { self.cast::<u8>().sub(count).with_metadata_of(self) }\n   996:     }\n   997: \n   998:     /// Adds an unsigned offset to a pointer using wrapping arithmetic.\n   999:     ///\n  1000:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n  1001:     /// offset of `3 * size_of::<T>()` bytes.\n  1002:     ///\n  1003:     /// # Safety\n  1004:     ///\n  1005:     /// This operation itself is always safe, but using the resulting pointer is not.\n  1006:     ///\n  1007:     /// The resulting pointer \"remembers\" the [allocation] that `self` points to; it must not\n  1008:     /// be used to read or write other allocations.\n  1009:     ///",
    "nanvix_source": "   965:     /// using [sub][pointer::sub] on it. See that method for documentation\n   966:     /// and safety requirements.\n   967:     ///\n   968:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   969:     /// leaving the metadata untouched.\n   970:     #[must_use]\n   971:     #[inline(always)]\n   972:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   973:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   974:     #[track_caller]\n   975:     pub const unsafe fn byte_sub(self, count: usize) -> Self {\n   976:         // SAFETY: the caller must uphold the safety contract for `sub`.\n   977:         unsafe { self.cast::<u8>().sub(count).with_metadata_of(self) }\n   978:     }\n   979: \n   980:     /// Adds an unsigned offset to a pointer using wrapping arithmetic.\n   981:     ///\n   982:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   983:     /// offset of `3 * size_of::<T>()` bytes.\n   984:     ///\n   985:     /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::cast",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "cast",
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
          "raw_pointer": {
            "is_mutable": false,
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:51637",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "U"
            }
          }
        }
      }
    },
    "verification_source": "    32:                     // To remain maximally conservative, we stop execution when we don't\n    33:                     // know whether the pointer is null or not.\n    34:                     // We can *not* return `false` here, that would be unsound in `NonNull::new`!\n    35:                     None => panic!(\"null-ness of this pointer cannot be determined in const context\"),\n    36:                 }\n    37:             } else {\n    38:                 ptr.addr() == 0\n    39:             }\n    40:         )\n    41:     }\n    42: \n    43:     /// Casts to a pointer of another type.\n    44:     #[stable(feature = \"ptr_cast\", since = \"1.38.0\")]\n    45:     #[rustc_const_stable(feature = \"const_ptr_cast\", since = \"1.38.0\")]\n    46:     #[rustc_diagnostic_item = \"const_ptr_cast\"]\n    47:     #[inline(always)]\n    48:     pub const fn cast<U>(self) -> *const U {\n    49:         self as _\n    50:     }\n    51: \n    52:     /// Try to cast to a pointer of another type by checking alignment.\n    53:     ///\n    54:     /// If the pointer is properly aligned to the target type, it will be\n    55:     /// cast to the target type. Otherwise, `None` is returned.\n    56:     ///\n    57:     /// # Examples\n    58:     ///\n    59:     /// ```rust\n    60:     /// #![feature(pointer_try_cast_aligned)]\n    61:     ///\n    62:     /// let x = 0u64;\n    63:     ///\n    64:     /// let aligned: *const u64 = &x;",
    "nanvix_source": "    38:                 ptr.addr() == 0\n    39:             }\n    40:         )\n    41:     }\n    42: \n    43:     /// Casts to a pointer of another type.\n    44:     #[stable(feature = \"ptr_cast\", since = \"1.38.0\")]\n    45:     #[rustc_const_stable(feature = \"const_ptr_cast\", since = \"1.38.0\")]\n    46:     #[rustc_diagnostic_item = \"const_ptr_cast\"]\n    47:     #[inline(always)]\n    48:     pub const fn cast<U>(self) -> *const U {\n    49:         self as _\n    50:     }\n    51: \n    52:     /// Try to cast to a pointer of another type by checking alignment.\n    53:     ///\n    54:     /// If the pointer is properly aligned to the target type, it will be\n    55:     /// cast to the target type. Otherwise, `None` is returned.\n    56:     ///\n    57:     /// # Examples\n    58:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::cast_const",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "cast_const",
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
          "raw_pointer": {
            "is_mutable": true,
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:51704",
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
              "generic": "Self"
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
    "verification_source": "   118:     }\n   119: \n   120:     /// Changes constness without changing the type.\n   121:     ///\n   122:     /// This is a bit safer than `as` because it wouldn't silently change the type if the code is\n   123:     /// refactored.\n   124:     ///\n   125:     /// While not strictly required (`*mut T` coerces to `*const T`), this is provided for symmetry\n   126:     /// with [`cast_mut`] on `*const T` and may have documentation value if used instead of implicit\n   127:     /// coercion.\n   128:     ///\n   129:     /// [`cast_mut`]: pointer::cast_mut\n   130:     #[stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   131:     #[rustc_const_stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   132:     #[rustc_diagnostic_item = \"ptr_cast_const\"]\n   133:     #[inline(always)]\n   134:     pub const fn cast_const(self) -> *const T {\n   135:         self as _\n   136:     }\n   137: \n   138:     #[doc = include_str!(\"./docs/addr.md\")]\n   139:     ///\n   140:     /// [without_provenance]: without_provenance_mut\n   141:     #[must_use]\n   142:     #[inline(always)]\n   143:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   144:     pub fn addr(self) -> usize {\n   145:         // A pointer-to-integer transmute currently has exactly the right semantics: it returns the\n   146:         // address without exposing the provenance. Note that this is *not* a stable guarantee about\n   147:         // transmute semantics, it relies on sysroot crates having special status.\n   148:         // SAFETY: Pointer-to-integer transmutes are valid (if you are okay with losing the\n   149:         // provenance).\n   150:         unsafe { mem::transmute(self.cast::<()>()) }",
    "nanvix_source": "   124:     ///\n   125:     /// While not strictly required (`*mut T` coerces to `*const T`), this is provided for symmetry\n   126:     /// with [`cast_mut`] on `*const T` and may have documentation value if used instead of implicit\n   127:     /// coercion.\n   128:     ///\n   129:     /// [`cast_mut`]: pointer::cast_mut\n   130:     #[stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   131:     #[rustc_const_stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   132:     #[rustc_diagnostic_item = \"ptr_cast_const\"]\n   133:     #[inline(always)]\n   134:     pub const fn cast_const(self) -> *const T {\n   135:         self as _\n   136:     }\n   137: \n   138:     #[doc = include_str!(\"./docs/addr.md\")]\n   139:     ///\n   140:     /// [without_provenance]: without_provenance_mut\n   141:     #[must_use]\n   142:     #[inline(always)]\n   143:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   144:     pub fn addr(self) -> usize {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::cast_mut",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "cast_mut",
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
          "raw_pointer": {
            "is_mutable": false,
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:51637",
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
              "generic": "Self"
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
    "verification_source": "   129:     #[inline]\n   130:     pub const fn with_metadata_of<U>(self, meta: *const U) -> *const U\n   131:     where\n   132:         U: PointeeSized,\n   133:     {\n   134:         from_raw_parts::<U>(self as *const (), metadata(meta))\n   135:     }\n   136: \n   137:     /// Changes constness without changing the type.\n   138:     ///\n   139:     /// This is a bit safer than `as` because it wouldn't silently change the type if the code is\n   140:     /// refactored.\n   141:     #[stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   142:     #[rustc_const_stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   143:     #[rustc_diagnostic_item = \"ptr_cast_mut\"]\n   144:     #[inline(always)]\n   145:     pub const fn cast_mut(self) -> *mut T {\n   146:         self as _\n   147:     }\n   148: \n   149:     #[doc = include_str!(\"./docs/addr.md\")]\n   150:     #[must_use]\n   151:     #[inline(always)]\n   152:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   153:     pub fn addr(self) -> usize {\n   154:         // A pointer-to-integer transmute currently has exactly the right semantics: it returns the\n   155:         // address without exposing the provenance. Note that this is *not* a stable guarantee about\n   156:         // transmute semantics, it relies on sysroot crates having special status.\n   157:         // SAFETY: Pointer-to-integer transmutes are valid (if you are okay with losing the\n   158:         // provenance).\n   159:         unsafe { mem::transmute(self.cast::<()>()) }\n   160:     }\n   161: ",
    "nanvix_source": "   135:     }\n   136: \n   137:     /// Changes constness without changing the type.\n   138:     ///\n   139:     /// This is a bit safer than `as` because it wouldn't silently change the type if the code is\n   140:     /// refactored.\n   141:     #[stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   142:     #[rustc_const_stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   143:     #[rustc_diagnostic_item = \"ptr_cast_mut\"]\n   144:     #[inline(always)]\n   145:     pub const fn cast_mut(self) -> *mut T {\n   146:         self as _\n   147:     }\n   148: \n   149:     #[doc = include_str!(\"./docs/addr.md\")]\n   150:     #[must_use]\n   151:     #[inline(always)]\n   152:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   153:     pub fn addr(self) -> usize {\n   154:         // A pointer-to-integer transmute currently has exactly the right semantics: it returns the\n   155:         // address without exposing the provenance. Note that this is *not* a stable guarantee about",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::copy",
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
        "is_unsafe": true
      },
      "name": "copy",
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
            "src",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "dst",
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
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   612: ///     // SAFETY: Our precondition ensures the source is aligned and valid,\n   613: ///     // and `Vec::with_capacity` ensures that we have usable space to write them.\n   614: ///     unsafe { ptr::copy(ptr, dst.as_mut_ptr(), elts); }\n   615: ///\n   616: ///     // SAFETY: We created it with this much capacity earlier,\n   617: ///     // and the previous `copy` has initialized these elements.\n   618: ///     unsafe { dst.set_len(elts); }\n   619: ///     dst\n   620: /// }\n   621: /// ```\n   622: #[doc(alias = \"memmove\")]\n   623: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   624: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   625: #[inline(always)]\n   626: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   627: #[rustc_diagnostic_item = \"ptr_copy\"]\n   628: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize) {\n   629:     // SAFETY: the safety contract for `copy` must be upheld by the caller.\n   630:     unsafe {\n   631:         ub_checks::assert_unsafe_precondition!(\n   632:             check_language_ub,\n   633:             \"ptr::copy requires that both pointer arguments are aligned and non-null\",\n   634:             (\n   635:                 src: *const () = src as *const (),\n   636:                 dst: *mut () = dst as *mut (),\n   637:                 align: usize = align_of::<T>(),\n   638:                 zero_size: bool = T::IS_ZST || count == 0,\n   639:             ) =>\n   640:             ub_checks::maybe_is_aligned_and_not_null(src, align, zero_size)\n   641:                 && ub_checks::maybe_is_aligned_and_not_null(dst, align, zero_size)\n   642:         );\n   643:         crate::intrinsics::copy(src, dst, count)\n   644:     }",
    "nanvix_source": "   615: ///     unsafe { dst.set_len(elts); }\n   616: ///     dst\n   617: /// }\n   618: /// ```\n   619: #[doc(alias = \"memmove\")]\n   620: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   621: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   622: #[inline(always)]\n   623: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   624: #[rustc_diagnostic_item = \"ptr_copy\"]\n   625: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize) {\n   626:     // SAFETY: the safety contract for `copy` must be upheld by the caller.\n   627:     unsafe {\n   628:         ub_checks::assert_unsafe_precondition!(\n   629:             check_language_ub,\n   630:             \"ptr::copy requires that both pointer arguments are aligned and non-null\",\n   631:             (\n   632:                 src: *const () = src as *const (),\n   633:                 dst: *mut () = dst as *mut (),\n   634:                 align: usize = align_of::<T>(),\n   635:                 zero_size: bool = T::IS_ZST || count == 0,",
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
