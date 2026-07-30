For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::as_mut_array",
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
      "name": "as_mut_array",
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
              "slice": {
                "generic": "T"
              }
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51719",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "raw_pointer": {
                        "is_mutable": true,
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
    "verification_source": "  1748:     /// assert!(!slice.is_empty());\n  1749:     /// ```\n  1750:     #[inline(always)]\n  1751:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1752:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]\n  1753:     pub const fn is_empty(self) -> bool {\n  1754:         self.len() == 0\n  1755:     }\n  1756: \n  1757:     /// Gets a raw, mutable pointer to the underlying array.\n  1758:     ///\n  1759:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n  1760:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1761:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1762:     #[inline]\n  1763:     #[must_use]\n  1764:     pub const fn as_mut_array<const N: usize>(self) -> Option<*mut [T; N]> {\n  1765:         if self.len() == N {\n  1766:             let me = self.as_mut_ptr() as *mut [T; N];\n  1767:             Some(me)\n  1768:         } else {\n  1769:             None\n  1770:         }\n  1771:     }\n  1772: \n  1773:     /// Divides one mutable raw slice into two at an index.\n  1774:     ///\n  1775:     /// The first will contain all indices from `[0, mid)` (excluding\n  1776:     /// the index `mid` itself) and the second will contain all\n  1777:     /// indices from `[mid, len)` (excluding the index `len` itself).\n  1778:     ///\n  1779:     /// # Panics\n  1780:     ///",
    "nanvix_source": "  1737:         self.len() == 0\n  1738:     }\n  1739: \n  1740:     /// Gets a raw, mutable pointer to the underlying array.\n  1741:     ///\n  1742:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n  1743:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1744:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1745:     #[inline]\n  1746:     #[must_use]\n  1747:     pub const fn as_mut_array<const N: usize>(self) -> Option<*mut [T; N]> {\n  1748:         if self.len() == N {\n  1749:             let me = self.as_mut_ptr() as *mut [T; N];\n  1750:             Some(me)\n  1751:         } else {\n  1752:             None\n  1753:         }\n  1754:     }\n  1755: \n  1756:     /// Divides one mutable raw slice into two at an index.\n  1757:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::as_ref",
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
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
        "is_unsafe": true
      },
      "name": "as_ref",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
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
    "verification_source": "   250:     /// let ptr: *const u8 = &10u8 as *const u8;\n   251:     ///\n   252:     /// unsafe {\n   253:     ///     if let Some(val_back) = ptr.as_ref() {\n   254:     ///         assert_eq!(val_back, &10);\n   255:     ///     }\n   256:     /// }\n   257:     /// ```\n   258:     ///\n   259:     ///\n   260:     /// [`is_null`]: #method.is_null\n   261:     /// [`as_uninit_ref`]: #method.as_uninit_ref\n   262:     /// [`as_ref_unchecked`]: #method.as_ref_unchecked\n   263:     #[stable(feature = \"ptr_as_ref\", since = \"1.9.0\")]\n   264:     #[rustc_const_stable(feature = \"const_ptr_is_null\", since = \"1.84.0\")]\n   265:     #[inline]\n   266:     pub const unsafe fn as_ref<'a>(self) -> Option<&'a T> {\n   267:         // SAFETY: the caller must guarantee that `self` is valid\n   268:         // for a reference if it isn't null.\n   269:         if self.is_null() { None } else { unsafe { Some(&*self) } }\n   270:     }\n   271: \n   272:     /// Returns a shared reference to the value behind the pointer.\n   273:     /// If the pointer may be null or the value may be uninitialized, [`as_uninit_ref`] must be used instead.\n   274:     /// If the pointer may be null, but the value is known to have been initialized, [`as_ref`] must be used instead.\n   275:     ///\n   276:     /// [`as_ref`]: #method.as_ref\n   277:     /// [`as_uninit_ref`]: #method.as_uninit_ref\n   278:     ///\n   279:     /// # Safety\n   280:     ///\n   281:     /// When calling this method, you have to ensure that\n   282:     /// the pointer is [convertible to a reference](crate::ptr#pointer-to-reference-conversion).",
    "nanvix_source": "   257:     /// }\n   258:     /// ```\n   259:     ///\n   260:     ///\n   261:     /// [`is_null`]: #method.is_null\n   262:     /// [`as_uninit_ref`]: #method.as_uninit_ref\n   263:     /// [`as_ref_unchecked`]: #method.as_ref_unchecked\n   264:     #[stable(feature = \"ptr_as_ref\", since = \"1.9.0\")]\n   265:     #[rustc_const_stable(feature = \"const_ptr_is_null\", since = \"1.84.0\")]\n   266:     #[inline]\n   267:     pub const unsafe fn as_ref<'a>(self) -> Option<&'a T> {\n   268:         // SAFETY: the caller must guarantee that `self` is valid\n   269:         // for a reference if it isn't null.\n   270:         if self.is_null() { None } else { unsafe { Some(&*self) } }\n   271:     }\n   272: \n   273:     /// Returns a shared reference to the value behind the pointer.\n   274:     /// If the pointer may be null or the value may be uninitialized, [`as_uninit_ref`] must be used instead.\n   275:     /// If the pointer may be null, but the value is known to have been initialized, [`as_ref`] must be used instead.\n   276:     ///\n   277:     /// [`as_ref`]: #method.as_ref",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::as_ref_unchecked",
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
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
        "is_unsafe": true
      },
      "name": "as_ref_unchecked",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   281:     /// When calling this method, you have to ensure that\n   282:     /// the pointer is [convertible to a reference](crate::ptr#pointer-to-reference-conversion).\n   283:     ///\n   284:     /// # Examples\n   285:     ///\n   286:     /// ```\n   287:     /// let ptr: *const u8 = &10u8 as *const u8;\n   288:     ///\n   289:     /// unsafe {\n   290:     ///     assert_eq!(ptr.as_ref_unchecked(), &10);\n   291:     /// }\n   292:     /// ```\n   293:     #[stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   294:     #[rustc_const_stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   295:     #[inline]\n   296:     #[must_use]\n   297:     pub const unsafe fn as_ref_unchecked<'a>(self) -> &'a T {\n   298:         // SAFETY: the caller must guarantee that `self` is valid for a reference\n   299:         unsafe { &*self }\n   300:     }\n   301: \n   302:     #[doc = include_str!(\"./docs/as_uninit_ref.md\")]\n   303:     ///\n   304:     /// [`is_null`]: #method.is_null\n   305:     /// [`as_ref`]: #method.as_ref\n   306:     ///\n   307:     /// # Examples\n   308:     ///\n   309:     /// ```\n   310:     /// #![feature(ptr_as_uninit)]\n   311:     ///\n   312:     /// let ptr: *const u8 = &10u8 as *const u8;\n   313:     ///",
    "nanvix_source": "   288:     /// let ptr: *const u8 = &10u8 as *const u8;\n   289:     ///\n   290:     /// unsafe {\n   291:     ///     assert_eq!(ptr.as_ref_unchecked(), &10);\n   292:     /// }\n   293:     /// ```\n   294:     #[stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   295:     #[rustc_const_stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   296:     #[inline]\n   297:     #[must_use]\n   298:     pub const unsafe fn as_ref_unchecked<'a>(self) -> &'a T {\n   299:         // SAFETY: the caller must guarantee that `self` is valid for a reference\n   300:         unsafe { &*self }\n   301:     }\n   302: \n   303:     #[doc = include_str!(\"./docs/as_uninit_ref.md\")]\n   304:     ///\n   305:     /// [`is_null`]: #method.is_null\n   306:     /// [`as_ref`]: #method.as_ref\n   307:     ///\n   308:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::byte_add",
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
      "name": "byte_add",
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
    "verification_source": "   865: \n   866:     /// Adds an unsigned offset in bytes to a pointer.\n   867:     ///\n   868:     /// `count` is in units of bytes.\n   869:     ///\n   870:     /// This is purely a convenience for casting to a `u8` pointer and\n   871:     /// using [add][pointer::add] on it. See that method for documentation\n   872:     /// and safety requirements.\n   873:     ///\n   874:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   875:     /// leaving the metadata untouched.\n   876:     #[must_use]\n   877:     #[inline(always)]\n   878:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   879:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   880:     #[track_caller]\n   881:     pub const unsafe fn byte_add(self, count: usize) -> Self {\n   882:         // SAFETY: the caller must uphold the safety contract for `add`.\n   883:         unsafe { self.cast::<u8>().add(count).with_metadata_of(self) }\n   884:     }\n   885: \n   886:     /// Subtracts an unsigned offset from a pointer.\n   887:     ///\n   888:     /// This can only move the pointer backward (or not move it). If you need to move forward or\n   889:     /// backward depending on the value, then you might want [`offset`](#method.offset) instead\n   890:     /// which takes a signed offset.\n   891:     ///\n   892:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   893:     /// offset of `3 * size_of::<T>()` bytes.\n   894:     ///\n   895:     /// # Safety\n   896:     ///\n   897:     /// If any of the following conditions are violated, the result is Undefined Behavior:",
    "nanvix_source": "   880:     /// using [add][pointer::add] on it. See that method for documentation\n   881:     /// and safety requirements.\n   882:     ///\n   883:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   884:     /// leaving the metadata untouched.\n   885:     #[must_use]\n   886:     #[inline(always)]\n   887:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   888:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   889:     #[track_caller]\n   890:     pub const unsafe fn byte_add(self, count: usize) -> Self {\n   891:         // SAFETY: the caller must uphold the safety contract for `add`.\n   892:         unsafe { self.cast::<u8>().add(count).with_metadata_of(self) }\n   893:     }\n   894: \n   895:     #[doc = include_str!(\"./docs/sub.md\")]\n   896:     ///\n   897:     /// Consider using [`wrapping_sub`](#method.wrapping_sub) instead if these constraints are\n   898:     /// difficult to satisfy. The only advantage of this method is that it\n   899:     /// enables more aggressive compiler optimizations.\n   900:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::byte_offset",
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
      "name": "byte_offset",
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
              "primitive": "isize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   386: \n   387:     /// Adds a signed offset in bytes to a pointer.\n   388:     ///\n   389:     /// `count` is in units of **bytes**.\n   390:     ///\n   391:     /// This is purely a convenience for casting to a `u8` pointer and\n   392:     /// using [offset][pointer::offset] on it. See that method for documentation\n   393:     /// and safety requirements.\n   394:     ///\n   395:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   396:     /// leaving the metadata untouched.\n   397:     #[must_use]\n   398:     #[inline(always)]\n   399:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   400:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   401:     #[track_caller]\n   402:     pub const unsafe fn byte_offset(self, count: isize) -> Self {\n   403:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   404:         unsafe { self.cast::<u8>().offset(count).with_metadata_of(self) }\n   405:     }\n   406: \n   407:     /// Adds a signed offset to a pointer using wrapping arithmetic.\n   408:     ///\n   409:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   410:     /// offset of `3 * size_of::<T>()` bytes.\n   411:     ///\n   412:     /// # Safety\n   413:     ///\n   414:     /// This operation itself is always safe, but using the resulting pointer is not.\n   415:     ///\n   416:     /// The resulting pointer \"remembers\" the [allocation] that `self` points to\n   417:     /// (this is called \"[Provenance](ptr/index.html#provenance)\").\n   418:     /// The pointer must not be used to read or write other allocations.",
    "nanvix_source": "   397:     /// using [offset][pointer::offset] on it. See that method for documentation\n   398:     /// and safety requirements.\n   399:     ///\n   400:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   401:     /// leaving the metadata untouched.\n   402:     #[must_use]\n   403:     #[inline(always)]\n   404:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   405:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   406:     #[track_caller]\n   407:     pub const unsafe fn byte_offset(self, count: isize) -> Self {\n   408:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   409:         unsafe { self.cast::<u8>().offset(count).with_metadata_of(self) }\n   410:     }\n   411: \n   412:     /// Adds a signed offset to a pointer using wrapping arithmetic.\n   413:     ///\n   414:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   415:     /// offset of `3 * size_of::<T>()` bytes.\n   416:     ///\n   417:     /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::byte_offset_from",
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
      "name": "byte_offset_from",
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
          "primitive": "isize"
        }
      }
    },
    "verification_source": "   619:         unsafe { intrinsics::ptr_offset_from(self, origin) }\n   620:     }\n   621: \n   622:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   623:     /// units of **bytes**.\n   624:     ///\n   625:     /// This is purely a convenience for casting to a `u8` pointer and\n   626:     /// using [`offset_from`][pointer::offset_from] on it. See that method for\n   627:     /// documentation and safety requirements.\n   628:     ///\n   629:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   630:     /// ignoring the metadata.\n   631:     #[inline(always)]\n   632:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   633:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   634:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   635:     pub const unsafe fn byte_offset_from<U: ?Sized>(self, origin: *const U) -> isize {\n   636:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   637:         unsafe { self.cast::<u8>().offset_from(origin.cast::<u8>()) }\n   638:     }\n   639: \n   640:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   641:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   642:     /// units of T: the distance in bytes is divided by `size_of::<T>()`.\n   643:     ///\n   644:     /// This computes the same value that [`offset_from`](#method.offset_from)\n   645:     /// would compute, but with the added precondition that the offset is\n   646:     /// guaranteed to be non-negative.  This method is equivalent to\n   647:     /// `usize::try_from(self.offset_from(origin)).unwrap_unchecked()`,\n   648:     /// but it provides slightly more information to the optimizer, which can\n   649:     /// sometimes allow it to optimize slightly better with some backends.\n   650:     ///\n   651:     /// This method can be thought of as recovering the `count` that was passed",
    "nanvix_source": "   630:     /// This is purely a convenience for casting to a `u8` pointer and\n   631:     /// using [`offset_from`][pointer::offset_from] on it. See that method for\n   632:     /// documentation and safety requirements.\n   633:     ///\n   634:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   635:     /// ignoring the metadata.\n   636:     #[inline(always)]\n   637:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   638:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   639:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   640:     pub const unsafe fn byte_offset_from<U: ?Sized>(self, origin: *const U) -> isize {\n   641:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   642:         unsafe { self.cast::<u8>().offset_from(origin.cast::<u8>()) }\n   643:     }\n   644: \n   645:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   646:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   647:     /// units of T: the distance in bytes is divided by `size_of::<T>()`.\n   648:     ///\n   649:     /// This computes the same value that [`offset_from`](#method.offset_from)\n   650:     /// would compute, but with the added precondition that the offset is",
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
