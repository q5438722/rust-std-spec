For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::with_addr",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "with_addr",
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
            "id": 9475,
            "path": "NonNull"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
          ],
          [
            "addr",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "usize"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 1039,
                "path": "NonZero"
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
    "verification_source": "   345:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   346:     pub fn expose_provenance(self) -> NonZero<usize> {\n   347:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   348:         // meaning that the address will be non-zero.\n   349:         unsafe { NonZero::new_unchecked(self.as_ptr().expose_provenance()) }\n   350:     }\n   351: \n   352:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   353:     /// `self`.\n   354:     ///\n   355:     /// For more details, see the equivalent method on a raw pointer, [`pointer::with_addr`].\n   356:     ///\n   357:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   358:     #[must_use]\n   359:     #[inline]\n   360:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   361:     pub fn with_addr(self, addr: NonZero<usize>) -> Self {\n   362:         // SAFETY: The result of `ptr::from::with_addr` is non-null because `addr` is guaranteed to be non-zero.\n   363:         unsafe { NonNull::new_unchecked(self.as_ptr().with_addr(addr.get()) as *mut _) }\n   364:     }\n   365: \n   366:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the\n   367:     /// [provenance][crate::ptr#provenance] of `self`.\n   368:     ///\n   369:     /// For more details, see the equivalent method on a raw pointer, [`pointer::map_addr`].\n   370:     ///\n   371:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   372:     #[must_use]\n   373:     #[inline]\n   374:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   375:     pub fn map_addr(self, f: impl FnOnce(NonZero<usize>) -> NonZero<usize>) -> Self {\n   376:         self.with_addr(f(self.addr()))\n   377:     }",
    "nanvix_source": "   348: \n   349:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   350:     /// `self`.\n   351:     ///\n   352:     /// For more details, see the equivalent method on a raw pointer, [`pointer::with_addr`].\n   353:     ///\n   354:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   355:     #[must_use]\n   356:     #[inline]\n   357:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   358:     pub fn with_addr(self, addr: NonZero<usize>) -> Self {\n   359:         // SAFETY: The result of `ptr::from::with_addr` is non-null because `addr` is guaranteed to be non-zero.\n   360:         unsafe { NonNull::new_unchecked(self.as_ptr().with_addr(addr.get()) as *mut _) }\n   361:     }\n   362: \n   363:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the\n   364:     /// [provenance][crate::ptr#provenance] of `self`.\n   365:     ///\n   366:     /// For more details, see the equivalent method on a raw pointer, [`pointer::map_addr`].\n   367:     ///\n   368:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::with_exposed_provenance",
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
      "name": "with_exposed_provenance",
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
            "id": 9475,
            "path": "NonNull"
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
        "impl_id": "core:9486",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "usize"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 1039,
                "path": "NonZero"
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
    "verification_source": "   127:     #[must_use]\n   128:     #[inline]\n   129:     pub const fn dangling() -> Self {\n   130:         let align = crate::mem::Alignment::of::<T>();\n   131:         NonNull::without_provenance(align.as_nonzero_usize())\n   132:     }\n   133: \n   134:     /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n   135:     /// [provenance][crate::ptr#provenance].\n   136:     ///\n   137:     /// For more details, see the equivalent method on a raw pointer, [`ptr::with_exposed_provenance_mut`].\n   138:     ///\n   139:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   140:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   141:     #[rustc_const_unstable(feature = \"const_nonnull_with_exposed_provenance\", issue = \"154215\")]\n   142:     #[inline]\n   143:     pub const fn with_exposed_provenance(addr: NonZero<usize>) -> Self {\n   144:         // SAFETY: we know `addr` is non-zero.\n   145:         unsafe {\n   146:             let ptr = crate::ptr::with_exposed_provenance_mut(addr.get());\n   147:             NonNull::new_unchecked(ptr)\n   148:         }\n   149:     }\n   150: \n   151:     /// Returns a shared references to the value. In contrast to [`as_ref`], this does not require\n   152:     /// that the value has to be initialized.\n   153:     ///\n   154:     /// For the mutable counterpart see [`as_uninit_mut`].\n   155:     ///\n   156:     /// [`as_ref`]: NonNull::as_ref\n   157:     /// [`as_uninit_mut`]: NonNull::as_uninit_mut\n   158:     ///\n   159:     /// # Safety",
    "nanvix_source": "   130: \n   131:     /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n   132:     /// [provenance][crate::ptr#provenance].\n   133:     ///\n   134:     /// For more details, see the equivalent method on a raw pointer, [`ptr::with_exposed_provenance_mut`].\n   135:     ///\n   136:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   137:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   138:     #[rustc_const_unstable(feature = \"const_nonnull_with_exposed_provenance\", issue = \"154215\")]\n   139:     #[inline]\n   140:     pub const fn with_exposed_provenance(addr: NonZero<usize>) -> Self {\n   141:         // SAFETY: we know `addr` is non-zero.\n   142:         unsafe {\n   143:             let ptr = crate::ptr::with_exposed_provenance_mut(addr.get());\n   144:             NonNull::new_unchecked(ptr)\n   145:         }\n   146:     }\n   147: \n   148:     /// Returns a shared references to the value. In contrast to [`as_ref`], this does not require\n   149:     /// that the value has to be initialized.\n   150:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::without_provenance",
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
      "name": "without_provenance",
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
            "id": 9475,
            "path": "NonNull"
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
        "impl_id": "core:9486",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "usize"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 1039,
                "path": "NonZero"
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
    "verification_source": "    85: \n    86: /// `NonNull` pointers are not `Sync` because the data they reference may be aliased.\n    87: // N.B., this impl is unnecessary, but should provide better error messages.\n    88: #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n    89: impl<T: PointeeSized> !Sync for NonNull<T> {}\n    90: \n    91: impl<T: Sized> NonNull<T> {\n    92:     /// Creates a pointer with the given address and no [provenance][crate::ptr#provenance].\n    93:     ///\n    94:     /// For more details, see the equivalent method on a raw pointer, [`ptr::without_provenance_mut`].\n    95:     ///\n    96:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n    97:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n    98:     #[rustc_const_stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n    99:     #[must_use]\n   100:     #[inline]\n   101:     pub const fn without_provenance(addr: NonZero<usize>) -> Self {\n   102:         // SAFETY: we know `addr` is non-zero and all nonzero integers are valid raw pointers.\n   103:         unsafe { transmute(addr) }\n   104:     }\n   105: \n   106:     /// Creates a new `NonNull` that is dangling, but well-aligned.\n   107:     ///\n   108:     /// This is useful for initializing types which lazily allocate, like\n   109:     /// `Vec::new` does.\n   110:     ///\n   111:     /// Note that the address of the returned pointer may potentially\n   112:     /// be that of a valid pointer, which means this must not be used\n   113:     /// as a \"not yet initialized\" sentinel value.\n   114:     /// Types that lazily allocate must track initialization by some other means.\n   115:     ///\n   116:     /// # Examples\n   117:     ///",
    "nanvix_source": "    88: impl<T: Sized> NonNull<T> {\n    89:     /// Creates a pointer with the given address and no [provenance][crate::ptr#provenance].\n    90:     ///\n    91:     /// For more details, see the equivalent method on a raw pointer, [`ptr::without_provenance_mut`].\n    92:     ///\n    93:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n    94:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n    95:     #[rustc_const_stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n    96:     #[must_use]\n    97:     #[inline]\n    98:     pub const fn without_provenance(addr: NonZero<usize>) -> Self {\n    99:         // SAFETY: we know `addr` is non-zero and all nonzero integers are valid raw pointers.\n   100:         unsafe { transmute(addr) }\n   101:     }\n   102: \n   103:     /// Creates a new `NonNull` that is dangling, but well-aligned.\n   104:     ///\n   105:     /// This is useful for initializing types which lazily allocate, like\n   106:     /// `Vec::new` does.\n   107:     ///\n   108:     /// Note that the address of the returned pointer may potentially",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::ChunksExact::remainder",
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
      "name": "remainder",
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
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10066,
            "path": "ChunksExact"
          }
        },
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
        "impl_id": "core:31500",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10066",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "ChunksExact"
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
    "verification_source": "  1862:     ///\n  1863:     /// # Example\n  1864:     ///\n  1865:     /// ```\n  1866:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1867:     /// let mut iter = slice.chunks_exact(2);\n  1868:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1869:     /// assert_eq!(iter.next(), Some(&['l', 'o'][..]));\n  1870:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1871:     /// assert_eq!(iter.next(), Some(&['r', 'e'][..]));\n  1872:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1873:     /// assert_eq!(iter.next(), None);\n  1874:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1875:     /// ```\n  1876:     #[must_use]\n  1877:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1878:     pub fn remainder(&self) -> &'a [T] {\n  1879:         self.rem\n  1880:     }\n  1881: }\n  1882: \n  1883: // FIXME(#26925) Remove in favor of `#[derive(Clone)]`\n  1884: #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1885: impl<T> Clone for ChunksExact<'_, T> {\n  1886:     fn clone(&self) -> Self {\n  1887:         ChunksExact { v: self.v, rem: self.rem, chunk_size: self.chunk_size }\n  1888:     }\n  1889: }\n  1890: \n  1891: #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1892: impl<'a, T> Iterator for ChunksExact<'a, T> {\n  1893:     type Item = &'a [T];\n  1894: ",
    "nanvix_source": "  1866:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1867:     /// assert_eq!(iter.next(), Some(&['l', 'o'][..]));\n  1868:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1869:     /// assert_eq!(iter.next(), Some(&['r', 'e'][..]));\n  1870:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1871:     /// assert_eq!(iter.next(), None);\n  1872:     /// assert_eq!(iter.remainder(), &['m'][..]);\n  1873:     /// ```\n  1874:     #[must_use]\n  1875:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1876:     pub fn remainder(&self) -> &'a [T] {\n  1877:         self.rem\n  1878:     }\n  1879: }\n  1880: \n  1881: // FIXME(#26925) Remove in favor of `#[derive(Clone)]`\n  1882: #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1883: impl<T> Clone for ChunksExact<'_, T> {\n  1884:     fn clone(&self) -> Self {\n  1885:         ChunksExact { v: self.v, rem: self.rem, chunk_size: self.chunk_size }\n  1886:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::Iter::as_slice",
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
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10048,
            "path": "Iter"
          }
        },
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
        "impl_id": "core:31321",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10048",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "Iter"
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
    "verification_source": "   121:     /// println!(\"{:?}\", iter.as_slice());\n   122:     ///\n   123:     /// // Now, we call the `next` method to remove the first element from the iterator:\n   124:     /// iter.next();\n   125:     /// // Here the iterator does not contain the first element of the slice any more,\n   126:     /// // so `as_slice` only returns the last two elements of the slice,\n   127:     /// // and so this prints \"[2, 3]\":\n   128:     /// println!(\"{:?}\", iter.as_slice());\n   129:     ///\n   130:     /// // The underlying slice has not been modified and still contains three elements,\n   131:     /// // so this prints \"[1, 2, 3]\":\n   132:     /// println!(\"{:?}\", slice);\n   133:     /// ```\n   134:     #[must_use]\n   135:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   136:     #[inline]\n   137:     pub fn as_slice(&self) -> &'a [T] {\n   138:         self.make_slice()\n   139:     }\n   140: }\n   141: \n   142: iterator! {struct Iter -> *const T, &'a T, const, {/* no mut */}, as_ref, each_ref, {\n   143:     fn is_sorted_by<F>(self, mut compare: F) -> bool\n   144:     where\n   145:         Self: Sized,\n   146:         F: FnMut(&Self::Item, &Self::Item) -> bool,\n   147:     {\n   148:         self.as_slice().is_sorted_by(|a, b| compare(&a, &b))\n   149:     }\n   150: }}\n   151: \n   152: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   153: impl<T> Clone for Iter<'_, T> {",
    "nanvix_source": "   125:     /// // and so this prints \"[2, 3]\":\n   126:     /// println!(\"{:?}\", iter.as_slice());\n   127:     ///\n   128:     /// // The underlying slice has not been modified and still contains three elements,\n   129:     /// // so this prints \"[1, 2, 3]\":\n   130:     /// println!(\"{:?}\", slice);\n   131:     /// ```\n   132:     #[must_use]\n   133:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   134:     #[inline]\n   135:     pub fn as_slice(&self) -> &'a [T] {\n   136:         self.make_slice()\n   137:     }\n   138: }\n   139: \n   140: iterator! {struct Iter -> *const T, &'a T, const, {/* no mut */}, as_ref, each_ref, {\n   141:     fn is_sorted_by<F>(self, mut compare: F) -> bool\n   142:     where\n   143:         Self: Sized,\n   144:         F: FnMut(&Self::Item, &Self::Item) -> bool,\n   145:     {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::IterMut::as_slice",
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
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11725,
            "path": "IterMut"
          }
        },
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
        "impl_id": "core:31338",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11725",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "IterMut"
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
    "verification_source": "   297:     ///\n   298:     /// // Now, we call the `next` method to remove the first element from the iterator\n   299:     /// // and increment its value:\n   300:     /// *iter.next().unwrap() += 1;\n   301:     /// // Here the iterator does not contain the first element of the slice any more,\n   302:     /// // so `as_slice` only returns the last two elements of the slice,\n   303:     /// // and so this prints \"[2, 3]\":\n   304:     /// println!(\"{:?}\", iter.as_slice());\n   305:     ///\n   306:     /// // The underlying slice still contains three elements, but its first element\n   307:     /// // was increased by 1, so this prints \"[2, 2, 3]\":\n   308:     /// println!(\"{:?}\", slice);\n   309:     /// ```\n   310:     #[must_use]\n   311:     #[stable(feature = \"slice_iter_mut_as_slice\", since = \"1.53.0\")]\n   312:     #[inline]\n   313:     pub fn as_slice(&self) -> &[T] {\n   314:         self.make_slice()\n   315:     }\n   316: \n   317:     /// Views the underlying data as a mutable subslice of the original data.\n   318:     ///\n   319:     /// # Examples\n   320:     ///\n   321:     /// Basic usage:\n   322:     ///\n   323:     /// ```\n   324:     /// #![feature(slice_iter_mut_as_mut_slice)]\n   325:     ///\n   326:     /// let mut slice: &mut [usize] = &mut [1, 2, 3];\n   327:     ///\n   328:     /// // First, we get the iterator:\n   329:     /// let mut iter = slice.iter_mut();",
    "nanvix_source": "   301:     /// // and so this prints \"[2, 3]\":\n   302:     /// println!(\"{:?}\", iter.as_slice());\n   303:     ///\n   304:     /// // The underlying slice still contains three elements, but its first element\n   305:     /// // was increased by 1, so this prints \"[2, 2, 3]\":\n   306:     /// println!(\"{:?}\", slice);\n   307:     /// ```\n   308:     #[must_use]\n   309:     #[stable(feature = \"slice_iter_mut_as_slice\", since = \"1.53.0\")]\n   310:     #[inline]\n   311:     pub fn as_slice(&self) -> &[T] {\n   312:         self.make_slice()\n   313:     }\n   314: \n   315:     /// Views the underlying data as a mutable subslice of the original data.\n   316:     ///\n   317:     /// # Examples\n   318:     ///\n   319:     /// Basic usage:\n   320:     ///\n   321:     /// ```",
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
