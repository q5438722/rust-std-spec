For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::byte_add",
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
    "verification_source": "   661: \n   662:     /// Calculates the offset from a pointer in bytes (convenience for `.byte_offset(count as isize)`).\n   663:     ///\n   664:     /// `count` is in units of bytes.\n   665:     ///\n   666:     /// This is purely a convenience for casting to a `u8` pointer and\n   667:     /// using [`add`][NonNull::add] on it. See that method for documentation\n   668:     /// and safety requirements.\n   669:     ///\n   670:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   671:     /// leaving the metadata untouched.\n   672:     #[must_use]\n   673:     #[inline(always)]\n   674:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   675:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   676:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   677:     pub const unsafe fn byte_add(self, count: usize) -> Self {\n   678:         // SAFETY: the caller must uphold the safety contract for `add` and `byte_add` has the same\n   679:         // safety contract.\n   680:         // Additionally safety contract of `add` guarantees that the resulting pointer is pointing\n   681:         // to an allocation, there can't be an allocation at null, thus it's safe to construct\n   682:         // `NonNull`.\n   683:         unsafe { transmute(self.as_ptr().byte_add(count)) }\n   684:     }\n   685: \n   686:     /// Subtracts an offset from a pointer (convenience for\n   687:     /// `.offset((count as isize).wrapping_neg())`).\n   688:     ///\n   689:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   690:     /// offset of `3 * size_of::<T>()` bytes.\n   691:     ///\n   692:     /// # Safety\n   693:     ///",
    "nanvix_source": "   622:     /// using [`add`][NonNull::add] on it. See that method for documentation\n   623:     /// and safety requirements.\n   624:     ///\n   625:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   626:     /// leaving the metadata untouched.\n   627:     #[must_use]\n   628:     #[inline(always)]\n   629:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   630:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   631:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   632:     pub const unsafe fn byte_add(self, count: usize) -> Self {\n   633:         // SAFETY: the caller must uphold the safety contract for `add` and `byte_add` has the same\n   634:         // safety contract.\n   635:         // Additionally safety contract of `add` guarantees that the resulting pointer is pointing\n   636:         // to an allocation, there can't be an allocation at null, thus it's safe to construct\n   637:         // `NonNull`.\n   638:         unsafe { transmute(self.as_ptr().byte_add(count)) }\n   639:     }\n   640: \n   641:     #[doc = include_str!(\"./docs/sub.md\")]\n   642:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::byte_offset",
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
    "verification_source": "   585: \n   586:     /// Calculates the offset from a pointer in bytes.\n   587:     ///\n   588:     /// `count` is in units of **bytes**.\n   589:     ///\n   590:     /// This is purely a convenience for casting to a `u8` pointer and\n   591:     /// using [offset][pointer::offset] on it. See that method for documentation\n   592:     /// and safety requirements.\n   593:     ///\n   594:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   595:     /// leaving the metadata untouched.\n   596:     #[must_use]\n   597:     #[inline(always)]\n   598:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   599:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   600:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   601:     pub const unsafe fn byte_offset(self, count: isize) -> Self {\n   602:         // SAFETY: the caller must uphold the safety contract for `offset` and `byte_offset` has\n   603:         // the same safety contract.\n   604:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   605:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   606:         // construct `NonNull`.\n   607:         unsafe { transmute(self.as_ptr().byte_offset(count)) }\n   608:     }\n   609: \n   610:     /// Adds an offset to a pointer (convenience for `.offset(count as isize)`).\n   611:     ///\n   612:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n   613:     /// offset of `3 * size_of::<T>()` bytes.\n   614:     ///\n   615:     /// # Safety\n   616:     ///\n   617:     /// If any of the following conditions are violated, the result is Undefined Behavior:",
    "nanvix_source": "   567:     /// using [offset][pointer::offset] on it. See that method for documentation\n   568:     /// and safety requirements.\n   569:     ///\n   570:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   571:     /// leaving the metadata untouched.\n   572:     #[must_use]\n   573:     #[inline(always)]\n   574:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   575:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   576:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   577:     pub const unsafe fn byte_offset(self, count: isize) -> Self {\n   578:         // SAFETY: the caller must uphold the safety contract for `offset` and `byte_offset` has\n   579:         // the same safety contract.\n   580:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   581:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   582:         // construct `NonNull`.\n   583:         unsafe { transmute(self.as_ptr().byte_offset(count)) }\n   584:     }\n   585: \n   586:     #[doc = include_str!(\"./docs/add.md\")]\n   587:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::byte_offset_from",
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
                          "generic": "U"
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
    "verification_source": "   862:         unsafe { self.as_ptr().offset_from(origin.as_ptr()) }\n   863:     }\n   864: \n   865:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   866:     /// units of **bytes**.\n   867:     ///\n   868:     /// This is purely a convenience for casting to a `u8` pointer and\n   869:     /// using [`offset_from`][NonNull::offset_from] on it. See that method for\n   870:     /// documentation and safety requirements.\n   871:     ///\n   872:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   873:     /// ignoring the metadata.\n   874:     #[inline(always)]\n   875:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   876:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   877:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   878:     pub const unsafe fn byte_offset_from<U: ?Sized>(self, origin: NonNull<U>) -> isize {\n   879:         // SAFETY: the caller must uphold the safety contract for `byte_offset_from`.\n   880:         unsafe { self.as_ptr().byte_offset_from(origin.as_ptr()) }\n   881:     }\n   882: \n   883:     // N.B. `wrapping_offset``, `wrapping_add`, etc are not implemented because they can wrap to null\n   884: \n   885:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   886:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   887:     /// units of T: the distance in bytes is divided by `size_of::<T>()`.\n   888:     ///\n   889:     /// This computes the same value that [`offset_from`](#method.offset_from)\n   890:     /// would compute, but with the added precondition that the offset is\n   891:     /// guaranteed to be non-negative.  This method is equivalent to\n   892:     /// `usize::try_from(self.offset_from(origin)).unwrap_unchecked()`,\n   893:     /// but it provides slightly more information to the optimizer, which can\n   894:     /// sometimes allow it to optimize slightly better with some backends.",
    "nanvix_source": "   801:     /// This is purely a convenience for casting to a `u8` pointer and\n   802:     /// using [`offset_from`][NonNull::offset_from] on it. See that method for\n   803:     /// documentation and safety requirements.\n   804:     ///\n   805:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   806:     /// ignoring the metadata.\n   807:     #[inline(always)]\n   808:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   809:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   810:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   811:     pub const unsafe fn byte_offset_from<U: ?Sized>(self, origin: NonNull<U>) -> isize {\n   812:         // SAFETY: the caller must uphold the safety contract for `byte_offset_from`.\n   813:         unsafe { self.as_ptr().byte_offset_from(origin.as_ptr()) }\n   814:     }\n   815: \n   816:     // N.B. `wrapping_offset``, `wrapping_add`, etc are not implemented because they can wrap to null\n   817: \n   818:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   819:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   820:     /// units of T: the distance in bytes is divided by `size_of::<T>()`.\n   821:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::byte_offset_from_unsigned",
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
                          "generic": "U"
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
    "verification_source": "   954:     }\n   955: \n   956:     /// Calculates the distance between two pointers within the same allocation, *where it's known that\n   957:     /// `self` is equal to or greater than `origin`*. The returned value is in\n   958:     /// units of **bytes**.\n   959:     ///\n   960:     /// This is purely a convenience for casting to a `u8` pointer and\n   961:     /// using [`offset_from_unsigned`][NonNull::offset_from_unsigned] on it.\n   962:     /// See that method for documentation and safety requirements.\n   963:     ///\n   964:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   965:     /// ignoring the metadata.\n   966:     #[inline(always)]\n   967:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   968:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   969:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   970:     pub const unsafe fn byte_offset_from_unsigned<U: ?Sized>(self, origin: NonNull<U>) -> usize {\n   971:         // SAFETY: the caller must uphold the safety contract for `byte_offset_from_unsigned`.\n   972:         unsafe { self.as_ptr().byte_offset_from_unsigned(origin.as_ptr()) }\n   973:     }\n   974: \n   975:     /// Reads the value from `self` without moving it. This leaves the\n   976:     /// memory in `self` unchanged.\n   977:     ///\n   978:     /// See [`ptr::read`] for safety concerns and examples.\n   979:     ///\n   980:     /// [`ptr::read`]: crate::ptr::read()\n   981:     #[inline]\n   982:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   983:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   984:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   985:     pub const unsafe fn read(self) -> T\n   986:     where",
    "nanvix_source": "   893:     /// This is purely a convenience for casting to a `u8` pointer and\n   894:     /// using [`offset_from_unsigned`][NonNull::offset_from_unsigned] on it.\n   895:     /// See that method for documentation and safety requirements.\n   896:     ///\n   897:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   898:     /// ignoring the metadata.\n   899:     #[inline(always)]\n   900:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   901:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   902:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   903:     pub const unsafe fn byte_offset_from_unsigned<U: ?Sized>(self, origin: NonNull<U>) -> usize {\n   904:         // SAFETY: the caller must uphold the safety contract for `byte_offset_from_unsigned`.\n   905:         unsafe { self.as_ptr().byte_offset_from_unsigned(origin.as_ptr()) }\n   906:     }\n   907: \n   908:     /// Reads the value from `self` without moving it. This leaves the\n   909:     /// memory in `self` unchanged.\n   910:     ///\n   911:     /// See [`ptr::read`] for safety concerns and examples.\n   912:     ///\n   913:     /// [`ptr::read`]: crate::ptr::read()",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::byte_sub",
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
    "verification_source": "   743:     /// Calculates the offset from a pointer in bytes (convenience for\n   744:     /// `.byte_offset((count as isize).wrapping_neg())`).\n   745:     ///\n   746:     /// `count` is in units of bytes.\n   747:     ///\n   748:     /// This is purely a convenience for casting to a `u8` pointer and\n   749:     /// using [`sub`][NonNull::sub] on it. See that method for documentation\n   750:     /// and safety requirements.\n   751:     ///\n   752:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   753:     /// leaving the metadata untouched.\n   754:     #[must_use]\n   755:     #[inline(always)]\n   756:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   757:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   758:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   759:     pub const unsafe fn byte_sub(self, count: usize) -> Self {\n   760:         // SAFETY: the caller must uphold the safety contract for `sub` and `byte_sub` has the same\n   761:         // safety contract.\n   762:         // Additionally safety contract of `sub` guarantees that the resulting pointer is pointing\n   763:         // to an allocation, there can't be an allocation at null, thus it's safe to construct\n   764:         // `NonNull`.\n   765:         unsafe { transmute(self.as_ptr().byte_sub(count)) }\n   766:     }\n   767: \n   768:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   769:     /// units of T: the distance in bytes divided by `size_of::<T>()`.\n   770:     ///\n   771:     /// This is equivalent to `(self as isize - origin as isize) / (size_of::<T>() as isize)`,\n   772:     /// except that it has a lot more opportunities for UB, in exchange for the compiler\n   773:     /// better understanding what you are doing.\n   774:     ///\n   775:     /// The primary motivation of this method is for computing the `len` of an array/slice",
    "nanvix_source": "   682:     /// using [`sub`][NonNull::sub] on it. See that method for documentation\n   683:     /// and safety requirements.\n   684:     ///\n   685:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   686:     /// leaving the metadata untouched.\n   687:     #[must_use]\n   688:     #[inline(always)]\n   689:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   690:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   691:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   692:     pub const unsafe fn byte_sub(self, count: usize) -> Self {\n   693:         // SAFETY: the caller must uphold the safety contract for `sub` and `byte_sub` has the same\n   694:         // safety contract.\n   695:         // Additionally safety contract of `sub` guarantees that the resulting pointer is pointing\n   696:         // to an allocation, there can't be an allocation at null, thus it's safe to construct\n   697:         // `NonNull`.\n   698:         unsafe { transmute(self.as_ptr().byte_sub(count)) }\n   699:     }\n   700: \n   701:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   702:     /// units of T: the distance in bytes divided by `size_of::<T>()`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::copy_from",
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
      "unsafe_or_ownership_sensitive",
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
      "name": "copy_from",
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
            "src",
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
    "verification_source": "  1070:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1071:         unsafe { ptr::copy_nonoverlapping(self.as_ptr(), dest.as_ptr(), count) }\n  1072:     }\n  1073: \n  1074:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1075:     /// and destination may overlap.\n  1076:     ///\n  1077:     /// NOTE: this has the *opposite* argument order of [`ptr::copy`].\n  1078:     ///\n  1079:     /// See [`ptr::copy`] for safety concerns and examples.\n  1080:     ///\n  1081:     /// [`ptr::copy`]: crate::ptr::copy()\n  1082:     #[inline(always)]\n  1083:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1084:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1085:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1086:     pub const unsafe fn copy_from(self, src: NonNull<T>, count: usize)\n  1087:     where\n  1088:         T: Sized,\n  1089:     {\n  1090:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1091:         unsafe { ptr::copy(src.as_ptr(), self.as_ptr(), count) }\n  1092:     }\n  1093: \n  1094:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1095:     /// and destination may *not* overlap.\n  1096:     ///\n  1097:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1098:     ///\n  1099:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1100:     ///\n  1101:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1102:     #[inline(always)]",
    "nanvix_source": "  1009:     ///\n  1010:     /// NOTE: this has the *opposite* argument order of [`ptr::copy`].\n  1011:     ///\n  1012:     /// See [`ptr::copy`] for safety concerns and examples.\n  1013:     ///\n  1014:     /// [`ptr::copy`]: crate::ptr::copy()\n  1015:     #[inline(always)]\n  1016:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1017:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1018:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1019:     pub const unsafe fn copy_from(self, src: NonNull<T>, count: usize)\n  1020:     where\n  1021:         T: Sized,\n  1022:     {\n  1023:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1024:         unsafe { ptr::copy(src.as_ptr(), self.as_ptr(), count) }\n  1025:     }\n  1026: \n  1027:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1028:     /// and destination may *not* overlap.\n  1029:     ///",
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
