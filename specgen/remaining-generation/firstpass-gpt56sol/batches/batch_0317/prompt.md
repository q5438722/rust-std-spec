For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::string::String::from_raw_parts",
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
        "is_const": false,
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "buf",
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
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   964:     /// # Examples\n   965:     ///\n   966:     /// ```\n   967:     /// unsafe {\n   968:     ///     let s = String::from(\"hello\");\n   969:     ///\n   970:     ///     // Deconstruct the String into parts.\n   971:     ///     let (ptr, len, capacity) = s.into_raw_parts();\n   972:     ///\n   973:     ///     let s = String::from_raw_parts(ptr, len, capacity);\n   974:     ///\n   975:     ///     assert_eq!(String::from(\"hello\"), s);\n   976:     /// }\n   977:     /// ```\n   978:     #[inline]\n   979:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   980:     pub unsafe fn from_raw_parts(buf: *mut u8, length: usize, capacity: usize) -> String {\n   981:         unsafe { String { vec: Vec::from_raw_parts(buf, length, capacity) } }\n   982:     }\n   983: \n   984:     /// Converts a vector of bytes to a `String` without checking that the\n   985:     /// string contains valid UTF-8.\n   986:     ///\n   987:     /// See the safe version, [`from_utf8`], for more details.\n   988:     ///\n   989:     /// [`from_utf8`]: String::from_utf8\n   990:     ///\n   991:     /// # Safety\n   992:     ///\n   993:     /// This function is unsafe because it does not check that the bytes passed\n   994:     /// to it are valid UTF-8. If this constraint is violated, it may cause\n   995:     /// memory unsafety issues with future users of the `String`, as the rest of\n   996:     /// the standard library assumes that `String`s are valid UTF-8.",
    "nanvix_source": "   975:     ///     // Deconstruct the String into parts.\n   976:     ///     let (ptr, len, capacity) = s.into_raw_parts();\n   977:     ///\n   978:     ///     let s = String::from_raw_parts(ptr, len, capacity);\n   979:     ///\n   980:     ///     assert_eq!(String::from(\"hello\"), s);\n   981:     /// }\n   982:     /// ```\n   983:     #[inline]\n   984:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   985:     pub unsafe fn from_raw_parts(buf: *mut u8, length: usize, capacity: usize) -> String {\n   986:         unsafe { String { vec: Vec::from_raw_parts(buf, length, capacity) } }\n   987:     }\n   988: \n   989:     /// Converts a vector of bytes to a `String` without checking that the\n   990:     /// string contains valid UTF-8.\n   991:     ///\n   992:     /// See the safe version, [`from_utf8`], for more details.\n   993:     ///\n   994:     /// [`from_utf8`]: String::from_utf8\n   995:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf8_unchecked",
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "from_utf8_unchecked",
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
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u8"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 114,
                "path": "Vec"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   997:     ///\n   998:     /// # Examples\n   999:     ///\n  1000:     /// ```\n  1001:     /// // some bytes, in a vector\n  1002:     /// let sparkle_heart = vec![240, 159, 146, 150];\n  1003:     ///\n  1004:     /// let sparkle_heart = unsafe {\n  1005:     ///     String::from_utf8_unchecked(sparkle_heart)\n  1006:     /// };\n  1007:     ///\n  1008:     /// assert_eq!(\"\ud83d\udc96\", sparkle_heart);\n  1009:     /// ```\n  1010:     #[inline]\n  1011:     #[must_use]\n  1012:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1013:     pub unsafe fn from_utf8_unchecked(bytes: Vec<u8>) -> String {\n  1014:         String { vec: bytes }\n  1015:     }\n  1016: \n  1017:     /// Converts a `String` into a byte vector.\n  1018:     ///\n  1019:     /// This consumes the `String`, so we do not need to copy its contents.\n  1020:     ///\n  1021:     /// # Examples\n  1022:     ///\n  1023:     /// ```\n  1024:     /// let s = String::from(\"hello\");\n  1025:     /// let bytes = s.into_bytes();\n  1026:     ///\n  1027:     /// assert_eq!(&[104, 101, 108, 108, 111][..], &bytes[..]);\n  1028:     /// ```\n  1029:     #[inline]",
    "nanvix_source": "  1008:     ///\n  1009:     /// let sparkle_heart = unsafe {\n  1010:     ///     String::from_utf8_unchecked(sparkle_heart)\n  1011:     /// };\n  1012:     ///\n  1013:     /// assert_eq!(\"\ud83d\udc96\", sparkle_heart);\n  1014:     /// ```\n  1015:     #[inline]\n  1016:     #[must_use]\n  1017:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1018:     pub unsafe fn from_utf8_unchecked(bytes: Vec<u8>) -> String {\n  1019:         String { vec: bytes }\n  1020:     }\n  1021: \n  1022:     /// Converts a `String` into a byte vector.\n  1023:     ///\n  1024:     /// This consumes the `String`, so we do not need to copy its contents.\n  1025:     ///\n  1026:     /// # Examples\n  1027:     ///\n  1028:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::into_raw_parts",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
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
                  "primitive": "u8"
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
    "verification_source": "   922:     /// the destructor to perform the cleanup.\n   923:     ///\n   924:     /// [`from_raw_parts`]: String::from_raw_parts\n   925:     ///\n   926:     /// # Examples\n   927:     ///\n   928:     /// ```\n   929:     /// let s = String::from(\"hello\");\n   930:     ///\n   931:     /// let (ptr, len, cap) = s.into_raw_parts();\n   932:     ///\n   933:     /// let rebuilt = unsafe { String::from_raw_parts(ptr, len, cap) };\n   934:     /// assert_eq!(rebuilt, \"hello\");\n   935:     /// ```\n   936:     #[must_use = \"losing the pointer will leak memory\"]\n   937:     #[stable(feature = \"vec_into_raw_parts\", since = \"1.93.0\")]\n   938:     pub fn into_raw_parts(self) -> (*mut u8, usize, usize) {\n   939:         self.vec.into_raw_parts()\n   940:     }\n   941: \n   942:     /// Creates a new `String` from a pointer, a length and a capacity.\n   943:     ///\n   944:     /// # Safety\n   945:     ///\n   946:     /// This is highly unsafe, due to the number of invariants that aren't\n   947:     /// checked:\n   948:     ///\n   949:     /// * all safety requirements for [`Vec::<u8>::from_raw_parts`].\n   950:     /// * all safety requirements for [`String::from_utf8_unchecked`].\n   951:     ///\n   952:     /// Violating these may cause problems like corrupting the allocator's\n   953:     /// internal data structures. For example, it is normally **not** safe to\n   954:     /// build a `String` from a pointer to a C `char` array containing UTF-8",
    "nanvix_source": "   933:     /// ```\n   934:     /// let s = String::from(\"hello\");\n   935:     ///\n   936:     /// let (ptr, len, cap) = s.into_raw_parts();\n   937:     ///\n   938:     /// let rebuilt = unsafe { String::from_raw_parts(ptr, len, cap) };\n   939:     /// assert_eq!(rebuilt, \"hello\");\n   940:     /// ```\n   941:     #[must_use = \"losing the pointer will leak memory\"]\n   942:     #[stable(feature = \"vec_into_raw_parts\", since = \"1.93.0\")]\n   943:     pub fn into_raw_parts(self) -> (*mut u8, usize, usize) {\n   944:         self.vec.into_raw_parts()\n   945:     }\n   946: \n   947:     /// Creates a new `String` from a pointer, a length and a capacity.\n   948:     ///\n   949:     /// # Safety\n   950:     ///\n   951:     /// This is highly unsafe, due to the number of invariants that aren't\n   952:     /// checked:\n   953:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::as_ptr",
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4417",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:346",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Arc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
    "verification_source": "  1802:     /// as long as there are strong counts in the `Arc`.\n  1803:     ///\n  1804:     /// # Examples\n  1805:     ///\n  1806:     /// ```\n  1807:     /// use std::sync::Arc;\n  1808:     ///\n  1809:     /// let x = Arc::new(\"hello\".to_owned());\n  1810:     /// let y = Arc::clone(&x);\n  1811:     /// let x_ptr = Arc::as_ptr(&x);\n  1812:     /// assert_eq!(x_ptr, Arc::as_ptr(&y));\n  1813:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1814:     /// ```\n  1815:     #[must_use]\n  1816:     #[stable(feature = \"rc_as_ptr\", since = \"1.45.0\")]\n  1817:     #[rustc_never_returns_null_ptr]\n  1818:     pub fn as_ptr(this: &Self) -> *const T {\n  1819:         let ptr: *mut ArcInner<T> = NonNull::as_ptr(this.ptr);\n  1820: \n  1821:         // SAFETY: This cannot go through Deref::deref or ArcInnerPtr::inner because\n  1822:         // this is required to retain raw/mut provenance such that e.g. `get_mut` can\n  1823:         // write through the pointer after the Arc is recovered through `from_raw`.\n  1824:         unsafe { &raw mut (*ptr).data }\n  1825:     }\n  1826: \n  1827:     /// Constructs an `Arc<T, A>` from a raw pointer.\n  1828:     ///\n  1829:     /// The raw pointer must have been previously returned by a call to [`Arc<U,\n  1830:     /// A>::into_raw`][into_raw] or [`Arc<U, A>::into_raw_with_allocator`][into_raw_with_allocator].\n  1831:     ///\n  1832:     /// # Safety\n  1833:     ///\n  1834:     /// * Creating a `Arc<T, A>` from a pointer other than one returned from",
    "nanvix_source": "  1820:     ///\n  1821:     /// let x = Arc::new(\"hello\".to_owned());\n  1822:     /// let y = Arc::clone(&x);\n  1823:     /// let x_ptr = Arc::as_ptr(&x);\n  1824:     /// assert_eq!(x_ptr, Arc::as_ptr(&y));\n  1825:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1826:     /// ```\n  1827:     #[must_use]\n  1828:     #[stable(feature = \"rc_as_ptr\", since = \"1.45.0\")]\n  1829:     #[rustc_never_returns_null_ptr]\n  1830:     pub fn as_ptr(this: &Self) -> *const T {\n  1831:         let ptr: *mut ArcInner<T> = NonNull::as_ptr(this.ptr);\n  1832: \n  1833:         // SAFETY: This cannot go through Deref::deref or ArcInnerPtr::inner because\n  1834:         // this is required to retain raw/mut provenance such that e.g. `get_mut` can\n  1835:         // write through the pointer after the Arc is recovered through `from_raw`.\n  1836:         unsafe { &raw mut (*ptr).data }\n  1837:     }\n  1838: \n  1839:     /// Constructs an `Arc<T, A>` from a raw pointer.\n  1840:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::assume_init",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "assume_init",
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
                        "id": 431,
                        "path": "mem::MaybeUninit"
                      }
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4394",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:346",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Arc"
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
            "id": 346,
            "path": "Arc"
          }
        }
      }
    },
    "verification_source": "  1426:     ///\n  1427:     /// ```\n  1428:     /// use std::sync::Arc;\n  1429:     ///\n  1430:     /// let mut five = Arc::<u32>::new_uninit();\n  1431:     ///\n  1432:     /// // Deferred initialization:\n  1433:     /// Arc::get_mut(&mut five).unwrap().write(5);\n  1434:     ///\n  1435:     /// let five = unsafe { five.assume_init() };\n  1436:     ///\n  1437:     /// assert_eq!(*five, 5)\n  1438:     /// ```\n  1439:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1440:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1441:     #[inline]\n  1442:     pub unsafe fn assume_init(self) -> Arc<T, A> {\n  1443:         let (ptr, alloc) = Arc::into_inner_with_allocator(self);\n  1444:         unsafe { Arc::from_inner_in(ptr.cast(), alloc) }\n  1445:     }\n  1446: }\n  1447: \n  1448: impl<T: ?Sized + CloneToUninit> Arc<T> {\n  1449:     /// Constructs a new `Arc<T>` with a clone of `value`.\n  1450:     ///\n  1451:     /// # Examples\n  1452:     ///\n  1453:     /// ```\n  1454:     /// #![feature(clone_from_ref)]\n  1455:     /// use std::sync::Arc;\n  1456:     ///\n  1457:     /// let hello: Arc<str> = Arc::clone_from_ref(\"hello\");\n  1458:     /// ```",
    "nanvix_source": "  1444:     /// // Deferred initialization:\n  1445:     /// Arc::get_mut(&mut five).unwrap().write(5);\n  1446:     ///\n  1447:     /// let five = unsafe { five.assume_init() };\n  1448:     ///\n  1449:     /// assert_eq!(*five, 5)\n  1450:     /// ```\n  1451:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1452:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1453:     #[inline]\n  1454:     pub unsafe fn assume_init(self) -> Arc<T, A> {\n  1455:         let (ptr, alloc) = Arc::into_inner_with_allocator(self);\n  1456:         unsafe { Arc::from_inner_in(ptr.cast(), alloc) }\n  1457:     }\n  1458: }\n  1459: \n  1460: impl<T: ?Sized + CloneToUninit> Arc<T> {\n  1461:     /// Constructs a new `Arc<T>` with a clone of `value`.\n  1462:     ///\n  1463:     /// # Examples\n  1464:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::decrement_strong_count",
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
      "name": "decrement_strong_count",
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
            "id": 346,
            "path": "Arc"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4409",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:346",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Arc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1738:     /// let five = Arc::new(5);\n  1739:     ///\n  1740:     /// unsafe {\n  1741:     ///     let ptr = Arc::into_raw(five);\n  1742:     ///     Arc::increment_strong_count(ptr);\n  1743:     ///\n  1744:     ///     // Those assertions are deterministic because we haven't shared\n  1745:     ///     // the `Arc` between threads.\n  1746:     ///     let five = Arc::from_raw(ptr);\n  1747:     ///     assert_eq!(2, Arc::strong_count(&five));\n  1748:     ///     Arc::decrement_strong_count(ptr);\n  1749:     ///     assert_eq!(1, Arc::strong_count(&five));\n  1750:     /// }\n  1751:     /// ```\n  1752:     #[inline]\n  1753:     #[stable(feature = \"arc_mutate_strong_count\", since = \"1.51.0\")]\n  1754:     pub unsafe fn decrement_strong_count(ptr: *const T) {\n  1755:         unsafe { Arc::decrement_strong_count_in(ptr, Global) }\n  1756:     }\n  1757: }\n  1758: \n  1759: impl<T: ?Sized, A: Allocator> Arc<T, A> {\n  1760:     /// Returns a reference to the underlying allocator.\n  1761:     ///\n  1762:     /// Note: this is an associated function, which means that you have\n  1763:     /// to call it as `Arc::allocator(&a)` instead of `a.allocator()`. This\n  1764:     /// is so that there is no conflict with a method on the inner type.\n  1765:     #[inline]\n  1766:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  1767:     pub fn allocator(this: &Self) -> &A {\n  1768:         &this.alloc\n  1769:     }\n  1770: ",
    "nanvix_source": "  1756:     ///     // Those assertions are deterministic because we haven't shared\n  1757:     ///     // the `Arc` between threads.\n  1758:     ///     let five = Arc::from_raw(ptr);\n  1759:     ///     assert_eq!(2, Arc::strong_count(&five));\n  1760:     ///     Arc::decrement_strong_count(ptr);\n  1761:     ///     assert_eq!(1, Arc::strong_count(&five));\n  1762:     /// }\n  1763:     /// ```\n  1764:     #[inline]\n  1765:     #[stable(feature = \"arc_mutate_strong_count\", since = \"1.51.0\")]\n  1766:     pub unsafe fn decrement_strong_count(ptr: *const T) {\n  1767:         unsafe { Arc::decrement_strong_count_in(ptr, Global) }\n  1768:     }\n  1769: }\n  1770: \n  1771: impl<T: ?Sized, A: Allocator> Arc<T, A> {\n  1772:     /// Returns a reference to the underlying allocator.\n  1773:     ///\n  1774:     /// Note: this is an associated function, which means that you have\n  1775:     /// to call it as `Arc::allocator(&a)` instead of `a.allocator()`. This\n  1776:     /// is so that there is no conflict with a method on the inner type.",
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
