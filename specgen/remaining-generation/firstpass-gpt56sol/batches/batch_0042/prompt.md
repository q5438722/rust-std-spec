For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::string::String::as_mut_str",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
      "name": "as_mut_str",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  1059:     ///\n  1060:     /// # Examples\n  1061:     ///\n  1062:     /// ```\n  1063:     /// let mut s = String::from(\"foobar\");\n  1064:     /// let s_mut_str = s.as_mut_str();\n  1065:     ///\n  1066:     /// s_mut_str.make_ascii_uppercase();\n  1067:     ///\n  1068:     /// assert_eq!(\"FOOBAR\", s_mut_str);\n  1069:     /// ```\n  1070:     #[inline]\n  1071:     #[must_use]\n  1072:     #[stable(feature = \"string_as_str\", since = \"1.7.0\")]\n  1073:     #[rustc_diagnostic_item = \"string_as_mut_str\"]\n  1074:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1075:     pub const fn as_mut_str(&mut self) -> &mut str {\n  1076:         // SAFETY: String contents are stipulated to be valid UTF-8, invalid contents are an error\n  1077:         // at construction.\n  1078:         unsafe { str::from_utf8_unchecked_mut(self.vec.as_mut_slice()) }\n  1079:     }\n  1080: \n  1081:     /// Appends a given string slice onto the end of this `String`.\n  1082:     ///\n  1083:     /// # Panics\n  1084:     ///\n  1085:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1086:     ///\n  1087:     /// # Examples\n  1088:     ///\n  1089:     /// ```\n  1090:     /// let mut s = String::from(\"foo\");\n  1091:     ///",
    "nanvix_source": "  1070:     ///\n  1071:     /// s_mut_str.make_ascii_uppercase();\n  1072:     ///\n  1073:     /// assert_eq!(\"FOOBAR\", s_mut_str);\n  1074:     /// ```\n  1075:     #[inline]\n  1076:     #[must_use]\n  1077:     #[stable(feature = \"string_as_str\", since = \"1.7.0\")]\n  1078:     #[rustc_diagnostic_item = \"string_as_mut_str\"]\n  1079:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1080:     pub const fn as_mut_str(&mut self) -> &mut str {\n  1081:         // SAFETY: String contents are stipulated to be valid UTF-8, invalid contents are an error\n  1082:         // at construction.\n  1083:         unsafe { str::from_utf8_unchecked_mut(self.vec.as_mut_slice()) }\n  1084:     }\n  1085: \n  1086:     /// Appends a given string slice onto the end of this `String`.\n  1087:     ///\n  1088:     /// # Panics\n  1089:     ///\n  1090:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::as_mut_vec",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": true
      },
      "name": "as_mut_vec",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
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
          }
        }
      }
    },
    "verification_source": "  1820:     /// # Examples\n  1821:     ///\n  1822:     /// ```\n  1823:     /// let mut s = String::from(\"hello\");\n  1824:     ///\n  1825:     /// unsafe {\n  1826:     ///     let vec = s.as_mut_vec();\n  1827:     ///     assert_eq!(&[104, 101, 108, 108, 111][..], &vec[..]);\n  1828:     ///\n  1829:     ///     vec.reverse();\n  1830:     /// }\n  1831:     /// assert_eq!(s, \"olleh\");\n  1832:     /// ```\n  1833:     #[inline]\n  1834:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1835:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1836:     pub const unsafe fn as_mut_vec(&mut self) -> &mut Vec<u8> {\n  1837:         &mut self.vec\n  1838:     }\n  1839: \n  1840:     /// Returns the length of this `String`, in bytes, not [`char`]s or\n  1841:     /// graphemes. In other words, it might not be what a human considers the\n  1842:     /// length of the string.\n  1843:     ///\n  1844:     /// # Examples\n  1845:     ///\n  1846:     /// ```\n  1847:     /// let a = String::from(\"foo\");\n  1848:     /// assert_eq!(a.len(), 3);\n  1849:     ///\n  1850:     /// let fancy_f = String::from(\"\u0192oo\");\n  1851:     /// assert_eq!(fancy_f.len(), 4);\n  1852:     /// assert_eq!(fancy_f.chars().count(), 3);",
    "nanvix_source": "  1831:     ///     let vec = s.as_mut_vec();\n  1832:     ///     assert_eq!(&[104, 101, 108, 108, 111][..], &vec[..]);\n  1833:     ///\n  1834:     ///     vec.reverse();\n  1835:     /// }\n  1836:     /// assert_eq!(s, \"olleh\");\n  1837:     /// ```\n  1838:     #[inline]\n  1839:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1840:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1841:     pub const unsafe fn as_mut_vec(&mut self) -> &mut Vec<u8> {\n  1842:         &mut self.vec\n  1843:     }\n  1844: \n  1845:     /// Returns the length of this `String`, in bytes, not [`char`]s or\n  1846:     /// graphemes. In other words, it might not be what a human considers the\n  1847:     /// length of the string.\n  1848:     ///\n  1849:     /// # Examples\n  1850:     ///\n  1851:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::leak",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "leak",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  2189:     /// trimming the capacity may result in a reallocation and copy.\n  2190:     ///\n  2191:     /// [`into_boxed_str`]: Self::into_boxed_str\n  2192:     ///\n  2193:     /// # Examples\n  2194:     ///\n  2195:     /// ```\n  2196:     /// let x = String::from(\"bucket\");\n  2197:     /// let static_ref: &'static mut str = x.leak();\n  2198:     /// assert_eq!(static_ref, \"bucket\");\n  2199:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  2200:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  2201:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  2202:     /// ```\n  2203:     #[stable(feature = \"string_leak\", since = \"1.72.0\")]\n  2204:     #[inline]\n  2205:     pub fn leak<'a>(self) -> &'a mut str {\n  2206:         let slice = self.vec.leak();\n  2207:         unsafe { from_utf8_unchecked_mut(slice) }\n  2208:     }\n  2209: }\n  2210: \n  2211: impl FromUtf8Error {\n  2212:     /// Returns a slice of [`u8`]s bytes that were attempted to convert to a `String`.\n  2213:     ///\n  2214:     /// # Examples\n  2215:     ///\n  2216:     /// ```\n  2217:     /// // some invalid bytes, in a vector\n  2218:     /// let bytes = vec![0, 159];\n  2219:     ///\n  2220:     /// let value = String::from_utf8(bytes);\n  2221:     ///",
    "nanvix_source": "  2200:     /// ```\n  2201:     /// let x = String::from(\"bucket\");\n  2202:     /// let static_ref: &'static mut str = x.leak();\n  2203:     /// assert_eq!(static_ref, \"bucket\");\n  2204:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  2205:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  2206:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  2207:     /// ```\n  2208:     #[stable(feature = \"string_leak\", since = \"1.72.0\")]\n  2209:     #[inline]\n  2210:     pub fn leak<'a>(self) -> &'a mut str {\n  2211:         let slice = self.vec.leak();\n  2212:         unsafe { from_utf8_unchecked_mut(slice) }\n  2213:     }\n  2214: }\n  2215: \n  2216: impl FromUtf8Error {\n  2217:     /// Returns a slice of [`u8`]s bytes that were attempted to convert to a `String`.\n  2218:     ///\n  2219:     /// # Examples\n  2220:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
        "impl_id": "alloc:4423",
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
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2608:     /// [clone]: Clone::clone\n  2609:     ///\n  2610:     /// # Examples\n  2611:     ///\n  2612:     /// ```\n  2613:     /// use std::sync::Arc;\n  2614:     ///\n  2615:     /// let mut x = Arc::new(3);\n  2616:     /// *Arc::get_mut(&mut x).unwrap() = 4;\n  2617:     /// assert_eq!(*x, 4);\n  2618:     ///\n  2619:     /// let _y = Arc::clone(&x);\n  2620:     /// assert!(Arc::get_mut(&mut x).is_none());\n  2621:     /// ```\n  2622:     #[inline]\n  2623:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  2624:     pub fn get_mut(this: &mut Self) -> Option<&mut T> {\n  2625:         if Self::is_unique(this) {\n  2626:             // This unsafety is ok because we're guaranteed that the pointer\n  2627:             // returned is the *only* pointer that will ever be returned to T. Our\n  2628:             // reference count is guaranteed to be 1 at this point, and we required\n  2629:             // the Arc itself to be `mut`, so we're returning the only possible\n  2630:             // reference to the inner data.\n  2631:             unsafe { Some(Arc::get_mut_unchecked(this)) }\n  2632:         } else {\n  2633:             None\n  2634:         }\n  2635:     }\n  2636: \n  2637:     /// Returns a mutable reference into the given `Arc`,\n  2638:     /// without any check.\n  2639:     ///\n  2640:     /// See also [`get_mut`], which is safe and does appropriate checks.",
    "nanvix_source": "  2629:     ///\n  2630:     /// let mut x = Arc::new(3);\n  2631:     /// *Arc::get_mut(&mut x).unwrap() = 4;\n  2632:     /// assert_eq!(*x, 4);\n  2633:     ///\n  2634:     /// let _y = Arc::clone(&x);\n  2635:     /// assert!(Arc::get_mut(&mut x).is_none());\n  2636:     /// ```\n  2637:     #[inline]\n  2638:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  2639:     pub fn get_mut(this: &mut Self) -> Option<&mut T> {\n  2640:         if Self::is_unique(this) {\n  2641:             // This unsafety is ok because we're guaranteed that the pointer\n  2642:             // returned is the *only* pointer that will ever be returned to T. Our\n  2643:             // reference count is guaranteed to be 1 at this point, and we required\n  2644:             // the Arc itself to be `mut`, so we're returning the only possible\n  2645:             // reference to the inner data.\n  2646:             unsafe { Some(Arc::get_mut_unchecked(this)) }\n  2647:         } else {\n  2648:             None\n  2649:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::make_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
      "name": "make_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 36,
                          "path": "CloneToUninit"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:4418",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2484:     /// ```\n  2485:     /// use std::sync::Arc;\n  2486:     ///\n  2487:     /// let mut data = Arc::new(75);\n  2488:     /// let weak = Arc::downgrade(&data);\n  2489:     ///\n  2490:     /// assert!(75 == *data);\n  2491:     /// assert!(75 == *weak.upgrade().unwrap());\n  2492:     ///\n  2493:     /// *Arc::make_mut(&mut data) += 1;\n  2494:     ///\n  2495:     /// assert!(76 == *data);\n  2496:     /// assert!(weak.upgrade().is_none());\n  2497:     /// ```\n  2498:     #[inline]\n  2499:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  2500:     pub fn make_mut(this: &mut Self) -> &mut T {\n  2501:         let size_of_val = size_of_val::<T>(&**this);\n  2502: \n  2503:         // Note that we hold both a strong reference and a weak reference.\n  2504:         // Thus, releasing our strong reference only will not, by itself, cause\n  2505:         // the memory to be deallocated.\n  2506:         //\n  2507:         // Use Acquire to ensure that we see any writes to `weak` that happen\n  2508:         // before release writes (i.e., decrements) to `strong`. Since we hold a\n  2509:         // weak count, there's no chance the ArcInner itself could be\n  2510:         // deallocated.\n  2511:         if this.inner().strong.compare_exchange(1, 0, Acquire, Relaxed).is_err() {\n  2512:             // Another strong pointer exists, so we must clone.\n  2513:             *this = Arc::clone_from_ref_in(&**this, this.alloc.clone());\n  2514:         } else if this.inner().weak.load(Relaxed) != 1 {\n  2515:             // Relaxed suffices in the above because this is fundamentally an\n  2516:             // optimization: we are always racing with weak pointers being",
    "nanvix_source": "  2505:     /// assert!(75 == *data);\n  2506:     /// assert!(75 == *weak.upgrade().unwrap());\n  2507:     ///\n  2508:     /// *Arc::make_mut(&mut data) += 1;\n  2509:     ///\n  2510:     /// assert!(76 == *data);\n  2511:     /// assert!(weak.upgrade().is_none());\n  2512:     /// ```\n  2513:     #[inline]\n  2514:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  2515:     pub fn make_mut(this: &mut Self) -> &mut T {\n  2516:         let size_of_val = size_of_val::<T>(&**this);\n  2517: \n  2518:         // Note that we hold both a strong reference and a weak reference.\n  2519:         // Thus, releasing our strong reference only will not, by itself, cause\n  2520:         // the memory to be deallocated.\n  2521:         //\n  2522:         // Use Acquire to ensure that we see any writes to `weak` that happen\n  2523:         // before release writes (i.e., decrements) to `strong`. Since we hold a\n  2524:         // weak count, there's no chance the ArcInner itself could be\n  2525:         // deallocated.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::IntoIter::as_mut_slice",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
      "name": "as_mut_slice",
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
            "id": 605,
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
        "impl_id": "alloc:4782",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:605",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "into_iter",
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
    "verification_source": "    90:     }\n    91: \n    92:     /// Returns the remaining items of this iterator as a mutable slice.\n    93:     ///\n    94:     /// # Examples\n    95:     ///\n    96:     /// ```\n    97:     /// let vec = vec!['a', 'b', 'c'];\n    98:     /// let mut into_iter = vec.into_iter();\n    99:     /// assert_eq!(into_iter.as_slice(), &['a', 'b', 'c']);\n   100:     /// into_iter.as_mut_slice()[2] = 'z';\n   101:     /// assert_eq!(into_iter.next().unwrap(), 'a');\n   102:     /// assert_eq!(into_iter.next().unwrap(), 'b');\n   103:     /// assert_eq!(into_iter.next().unwrap(), 'z');\n   104:     /// ```\n   105:     #[stable(feature = \"vec_into_iter_as_slice\", since = \"1.15.0\")]\n   106:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   107:         unsafe { &mut *self.as_raw_mut_slice() }\n   108:     }\n   109: \n   110:     /// Returns a reference to the underlying allocator.\n   111:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   112:     #[inline]\n   113:     pub fn allocator(&self) -> &A {\n   114:         &self.alloc\n   115:     }\n   116: \n   117:     fn as_raw_mut_slice(&mut self) -> *mut [T] {\n   118:         ptr::slice_from_raw_parts_mut(self.ptr.as_ptr(), self.len())\n   119:     }\n   120: \n   121:     /// Drops remaining elements and relinquishes the backing allocation.\n   122:     ///",
    "nanvix_source": "    96:     /// ```\n    97:     /// let vec = vec!['a', 'b', 'c'];\n    98:     /// let mut into_iter = vec.into_iter();\n    99:     /// assert_eq!(into_iter.as_slice(), &['a', 'b', 'c']);\n   100:     /// into_iter.as_mut_slice()[2] = 'z';\n   101:     /// assert_eq!(into_iter.next().unwrap(), 'a');\n   102:     /// assert_eq!(into_iter.next().unwrap(), 'b');\n   103:     /// assert_eq!(into_iter.next().unwrap(), 'z');\n   104:     /// ```\n   105:     #[stable(feature = \"vec_into_iter_as_slice\", since = \"1.15.0\")]\n   106:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   107:         unsafe { &mut *self.as_raw_mut_slice() }\n   108:     }\n   109: \n   110:     /// Returns a reference to the underlying allocator.\n   111:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   112:     #[inline]\n   113:     pub fn allocator(&self) -> &A {\n   114:         &self.alloc\n   115:     }\n   116: ",
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
