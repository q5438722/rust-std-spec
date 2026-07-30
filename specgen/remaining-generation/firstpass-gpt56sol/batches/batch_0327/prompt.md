For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::offset",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "offset",
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
    "verification_source": "   559:     /// ```\n   560:     /// use std::ptr::NonNull;\n   561:     ///\n   562:     /// let mut s = [1, 2, 3];\n   563:     /// let ptr: NonNull<u32> = NonNull::new(s.as_mut_ptr()).unwrap();\n   564:     ///\n   565:     /// unsafe {\n   566:     ///     println!(\"{}\", ptr.offset(1).read());\n   567:     ///     println!(\"{}\", ptr.offset(2).read());\n   568:     /// }\n   569:     /// ```\n   570:     #[inline(always)]\n   571:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   572:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   573:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   574:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   575:     pub const unsafe fn offset(self, count: isize) -> Self\n   576:     where\n   577:         T: Sized,\n   578:     {\n   579:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   580:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   581:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   582:         // construct `NonNull`.\n   583:         unsafe { transmute(intrinsics::offset(self.as_ptr(), count)) }\n   584:     }\n   585: \n   586:     /// Calculates the offset from a pointer in bytes.\n   587:     ///\n   588:     /// `count` is in units of **bytes**.\n   589:     ///\n   590:     /// This is purely a convenience for casting to a `u8` pointer and\n   591:     /// using [offset][pointer::offset] on it. See that method for documentation",
    "nanvix_source": "   541:     /// unsafe {\n   542:     ///     println!(\"{}\", ptr.offset(1).read());\n   543:     ///     println!(\"{}\", ptr.offset(2).read());\n   544:     /// }\n   545:     /// ```\n   546:     #[inline(always)]\n   547:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   548:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   549:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   550:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   551:     pub const unsafe fn offset(self, count: isize) -> Self\n   552:     where\n   553:         T: Sized,\n   554:     {\n   555:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   556:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   557:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   558:         // construct `NonNull`.\n   559:         unsafe { transmute(intrinsics::offset(self.as_ptr(), count)) }\n   560:     }\n   561: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::offset_from",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "offset_from",
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
            "origin",
            {
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
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "isize"
        }
      }
    },
    "verification_source": "   841:     /// let ptr2 = NonNull::new(Box::into_raw(Box::new(1u8))).unwrap();\n   842:     /// let diff = (ptr2.addr().get() as isize).wrapping_sub(ptr1.addr().get() as isize);\n   843:     /// // Make ptr2_other an \"alias\" of ptr2.add(1), but derived from ptr1.\n   844:     /// let diff_plus_1 = diff.wrapping_add(1);\n   845:     /// let ptr2_other = NonNull::new(ptr1.as_ptr().wrapping_byte_offset(diff_plus_1)).unwrap();\n   846:     /// assert_eq!(ptr2.addr(), ptr2_other.addr());\n   847:     /// // Since ptr2_other and ptr2 are derived from pointers to different objects,\n   848:     /// // computing their offset is undefined behavior, even though\n   849:     /// // they point to addresses that are in-bounds of the same object!\n   850:     ///\n   851:     /// let one = unsafe { ptr2_other.offset_from(ptr2) }; // Undefined Behavior! \u26a0\ufe0f\n   852:     /// ```\n   853:     #[inline]\n   854:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   855:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   856:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   857:     pub const unsafe fn offset_from(self, origin: NonNull<T>) -> isize\n   858:     where\n   859:         T: Sized,\n   860:     {\n   861:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   862:         unsafe { self.as_ptr().offset_from(origin.as_ptr()) }\n   863:     }\n   864: \n   865:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   866:     /// units of **bytes**.\n   867:     ///\n   868:     /// This is purely a convenience for casting to a `u8` pointer and\n   869:     /// using [`offset_from`][NonNull::offset_from] on it. See that method for\n   870:     /// documentation and safety requirements.\n   871:     ///\n   872:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   873:     /// ignoring the metadata.",
    "nanvix_source": "   780:     /// // Since ptr2_other and ptr2 are derived from pointers to different objects,\n   781:     /// // computing their offset is undefined behavior, even though\n   782:     /// // they point to addresses that are in-bounds of the same object!\n   783:     ///\n   784:     /// let one = unsafe { ptr2_other.offset_from(ptr2) }; // Undefined Behavior! \u26a0\ufe0f\n   785:     /// ```\n   786:     #[inline]\n   787:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   788:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   789:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   790:     pub const unsafe fn offset_from(self, origin: NonNull<T>) -> isize\n   791:     where\n   792:         T: Sized,\n   793:     {\n   794:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   795:         unsafe { self.as_ptr().offset_from(origin.as_ptr()) }\n   796:     }\n   797: \n   798:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   799:     /// units of **bytes**.\n   800:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::offset_from_unsigned",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "offset_from_unsigned",
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
            "subtracted",
            {
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
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   932:     /// let ptr1: NonNull<u32> = NonNull::from(&a[1]);\n   933:     /// let ptr2: NonNull<u32> = NonNull::from(&a[3]);\n   934:     /// unsafe {\n   935:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr1), 2);\n   936:     ///     assert_eq!(ptr1.add(2), ptr2);\n   937:     ///     assert_eq!(ptr2.sub(2), ptr1);\n   938:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr2), 0);\n   939:     /// }\n   940:     ///\n   941:     /// // This would be incorrect, as the pointers are not correctly ordered:\n   942:     /// // ptr1.offset_from_unsigned(ptr2)\n   943:     /// ```\n   944:     #[inline]\n   945:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   946:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   947:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   948:     pub const unsafe fn offset_from_unsigned(self, subtracted: NonNull<T>) -> usize\n   949:     where\n   950:         T: Sized,\n   951:     {\n   952:         // SAFETY: the caller must uphold the safety contract for `offset_from_unsigned`.\n   953:         unsafe { self.as_ptr().offset_from_unsigned(subtracted.as_ptr()) }\n   954:     }\n   955: \n   956:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   957:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   958:     /// units of **bytes**.\n   959:     ///\n   960:     /// This is purely a convenience for casting to a `u8` pointer and\n   961:     /// using [`offset_from_unsigned`][NonNull::offset_from_unsigned] on it.\n   962:     /// See that method for documentation and safety requirements.\n   963:     ///\n   964:     /// For non-`Sized` pointees this operation considers only the data pointers,",
    "nanvix_source": "   871:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr2), 0);\n   872:     /// }\n   873:     ///\n   874:     /// // This would be incorrect, as the pointers are not correctly ordered:\n   875:     /// // ptr1.offset_from_unsigned(ptr2)\n   876:     /// ```\n   877:     #[inline]\n   878:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   879:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   880:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   881:     pub const unsafe fn offset_from_unsigned(self, subtracted: NonNull<T>) -> usize\n   882:     where\n   883:         T: Sized,\n   884:     {\n   885:         // SAFETY: the caller must uphold the safety contract for `offset_from_unsigned`.\n   886:         unsafe { self.as_ptr().offset_from_unsigned(subtracted.as_ptr()) }\n   887:     }\n   888: \n   889:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   890:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   891:     /// units of **bytes**.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::read",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "read",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   969:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   970:     pub const unsafe fn byte_offset_from_unsigned<U: ?Sized>(self, origin: NonNull<U>) -> usize {\n   971:         // SAFETY: the caller must uphold the safety contract for `byte_offset_from_unsigned`.\n   972:         unsafe { self.as_ptr().byte_offset_from_unsigned(origin.as_ptr()) }\n   973:     }\n   974: \n   975:     /// Reads the value from `self` without moving it. This leaves the\n   976:     /// memory in `self` unchanged.\n   977:     ///\n   978:     /// See [`ptr::read`] for safety concerns and examples.\n   979:     ///\n   980:     /// [`ptr::read`]: crate::ptr::read()\n   981:     #[inline]\n   982:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   983:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   984:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   985:     pub const unsafe fn read(self) -> T\n   986:     where\n   987:         T: Sized,\n   988:     {\n   989:         // SAFETY: the caller must uphold the safety contract for `read`.\n   990:         unsafe { ptr::read(self.as_ptr()) }\n   991:     }\n   992: \n   993:     /// Performs a volatile read of the value from `self` without moving it. This\n   994:     /// leaves the memory in `self` unchanged.\n   995:     ///\n   996:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n   997:     /// to not be elided or reordered by the compiler across other volatile\n   998:     /// operations.\n   999:     ///\n  1000:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n  1001:     ///",
    "nanvix_source": "   908:     /// Reads the value from `self` without moving it. This leaves the\n   909:     /// memory in `self` unchanged.\n   910:     ///\n   911:     /// See [`ptr::read`] for safety concerns and examples.\n   912:     ///\n   913:     /// [`ptr::read`]: crate::ptr::read()\n   914:     #[inline]\n   915:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   916:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   917:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   918:     pub const unsafe fn read(self) -> T\n   919:     where\n   920:         T: Sized,\n   921:     {\n   922:         // SAFETY: the caller must uphold the safety contract for `read`.\n   923:         unsafe { ptr::read(self.as_ptr()) }\n   924:     }\n   925: \n   926:     /// Performs a volatile read of the value from `self` without moving it. This\n   927:     /// leaves the memory in `self` unchanged.\n   928:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::read_unaligned",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "read_unaligned",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1010:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n  1011:         unsafe { ptr::read_volatile(self.as_ptr()) }\n  1012:     }\n  1013: \n  1014:     /// Reads the value from `self` without moving it. This leaves the\n  1015:     /// memory in `self` unchanged.\n  1016:     ///\n  1017:     /// Unlike `read`, the pointer may be unaligned.\n  1018:     ///\n  1019:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n  1020:     ///\n  1021:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n  1022:     #[inline]\n  1023:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1024:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1025:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1026:     pub const unsafe fn read_unaligned(self) -> T\n  1027:     where\n  1028:         T: Sized,\n  1029:     {\n  1030:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n  1031:         unsafe { ptr::read_unaligned(self.as_ptr()) }\n  1032:     }\n  1033: \n  1034:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1035:     /// and destination may overlap.\n  1036:     ///\n  1037:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n  1038:     ///\n  1039:     /// See [`ptr::copy`] for safety concerns and examples.\n  1040:     ///\n  1041:     /// [`ptr::copy`]: crate::ptr::copy()\n  1042:     #[inline(always)]",
    "nanvix_source": "   949:     ///\n   950:     /// Unlike `read`, the pointer may be unaligned.\n   951:     ///\n   952:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n   953:     ///\n   954:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n   955:     #[inline]\n   956:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   957:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   958:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   959:     pub const unsafe fn read_unaligned(self) -> T\n   960:     where\n   961:         T: Sized,\n   962:     {\n   963:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n   964:         unsafe { ptr::read_unaligned(self.as_ptr()) }\n   965:     }\n   966: \n   967:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n   968:     /// and destination may overlap.\n   969:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::read_volatile",
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
                      "id": 12,
                      "path": "Sized"
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
        "is_unsafe": true
      },
      "name": "read_volatile",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   990:         unsafe { ptr::read(self.as_ptr()) }\n   991:     }\n   992: \n   993:     /// Performs a volatile read of the value from `self` without moving it. This\n   994:     /// leaves the memory in `self` unchanged.\n   995:     ///\n   996:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n   997:     /// to not be elided or reordered by the compiler across other volatile\n   998:     /// operations.\n   999:     ///\n  1000:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n  1001:     ///\n  1002:     /// [`ptr::read_volatile`]: crate::ptr::read_volatile()\n  1003:     #[inline]\n  1004:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1005:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1006:     pub unsafe fn read_volatile(self) -> T\n  1007:     where\n  1008:         T: Sized,\n  1009:     {\n  1010:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n  1011:         unsafe { ptr::read_volatile(self.as_ptr()) }\n  1012:     }\n  1013: \n  1014:     /// Reads the value from `self` without moving it. This leaves the\n  1015:     /// memory in `self` unchanged.\n  1016:     ///\n  1017:     /// Unlike `read`, the pointer may be unaligned.\n  1018:     ///\n  1019:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n  1020:     ///\n  1021:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n  1022:     #[inline]",
    "nanvix_source": "   929:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n   930:     /// to not be elided or reordered by the compiler across other volatile\n   931:     /// operations.\n   932:     ///\n   933:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n   934:     ///\n   935:     /// [`ptr::read_volatile`]: crate::ptr::read_volatile()\n   936:     #[inline]\n   937:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   938:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   939:     pub unsafe fn read_volatile(self) -> T\n   940:     where\n   941:         T: Sized,\n   942:     {\n   943:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n   944:         unsafe { ptr::read_volatile(self.as_ptr()) }\n   945:     }\n   946: \n   947:     /// Reads the value from `self` without moving it. This leaves the\n   948:     /// memory in `self` unchanged.\n   949:     ///",
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
