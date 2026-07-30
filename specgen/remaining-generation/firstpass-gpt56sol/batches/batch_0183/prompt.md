For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::swap",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "swap",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "a",
            {
              "primitive": "usize"
            }
          ],
          [
            "b",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   889:     ///\n   890:     /// # Panics\n   891:     ///\n   892:     /// Panics if `a` or `b` are out of bounds.\n   893:     ///\n   894:     /// # Examples\n   895:     ///\n   896:     /// ```\n   897:     /// let mut v = [\"a\", \"b\", \"c\", \"d\", \"e\"];\n   898:     /// v.swap(2, 4);\n   899:     /// assert!(v == [\"a\", \"b\", \"e\", \"d\", \"c\"]);\n   900:     /// ```\n   901:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   902:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n   903:     #[inline]\n   904:     #[track_caller]\n   905:     pub const fn swap(&mut self, a: usize, b: usize) {\n   906:         // FIXME: use swap_unchecked here (https://github.com/rust-lang/rust/pull/88540#issuecomment-944344343)\n   907:         // Can't take two mutable loans from one vector, so instead use raw pointers.\n   908:         let pa = &raw mut self[a];\n   909:         let pb = &raw mut self[b];\n   910:         // SAFETY: `pa` and `pb` have been created from safe mutable references and refer\n   911:         // to elements in the slice and therefore are guaranteed to be valid and aligned.\n   912:         // Note that accessing the elements behind `a` and `b` is checked and will\n   913:         // panic when out of bounds.\n   914:         unsafe {\n   915:             ptr::swap(pa, pb);\n   916:         }\n   917:     }\n   918: \n   919:     /// Swaps two elements in the slice, without doing bounds checking.\n   920:     ///\n   921:     /// For a safe alternative see [`swap`].",
    "nanvix_source": "   898:     ///\n   899:     /// ```\n   900:     /// let mut v = [\"a\", \"b\", \"c\", \"d\", \"e\"];\n   901:     /// v.swap(2, 4);\n   902:     /// assert!(v == [\"a\", \"b\", \"e\", \"d\", \"c\"]);\n   903:     /// ```\n   904:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   905:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n   906:     #[inline]\n   907:     #[track_caller]\n   908:     pub const fn swap(&mut self, a: usize, b: usize) {\n   909:         // FIXME: use swap_unchecked here (https://github.com/rust-lang/rust/pull/88540#issuecomment-944344343)\n   910:         // Can't take two mutable loans from one vector, so instead use raw pointers.\n   911:         let pa = &raw mut self[a];\n   912:         let pb = &raw mut self[b];\n   913:         // SAFETY: `pa` and `pb` have been created from safe mutable references and refer\n   914:         // to elements in the slice and therefore are guaranteed to be valid and aligned.\n   915:         // Note that accessing the elements behind `a` and `b` is checked and will\n   916:         // panic when out of bounds.\n   917:         unsafe {\n   918:             ptr::swap(pa, pb);",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut [T]` receiver. The determinism checker materializes that state as a by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable swap semantics while avoiding this limitation."
  },
  {
    "target": "core::slice::swap_with_slice",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "swap_with_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "other"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "other",
            {
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4406:     ///\n  4407:     /// ```\n  4408:     /// let mut slice = [1, 2, 3, 4, 5];\n  4409:     ///\n  4410:     /// {\n  4411:     ///     let (left, right) = slice.split_at_mut(2);\n  4412:     ///     left.swap_with_slice(&mut right[1..]);\n  4413:     /// }\n  4414:     ///\n  4415:     /// assert_eq!(slice, [4, 5, 3, 1, 2]);\n  4416:     /// ```\n  4417:     ///\n  4418:     /// [`split_at_mut`]: slice::split_at_mut\n  4419:     #[stable(feature = \"swap_with_slice\", since = \"1.27.0\")]\n  4420:     #[rustc_const_unstable(feature = \"const_swap_with_slice\", issue = \"142204\")]\n  4421:     #[track_caller]\n  4422:     pub const fn swap_with_slice(&mut self, other: &mut [T]) {\n  4423:         assert!(self.len() == other.len(), \"destination and source slices have different lengths\");\n  4424:         // SAFETY: `self` is valid for `self.len()` elements by definition, and `src` was\n  4425:         // checked to have the same length. The slices cannot overlap because\n  4426:         // mutable references are exclusive.\n  4427:         unsafe {\n  4428:             ptr::swap_nonoverlapping(self.as_mut_ptr(), other.as_mut_ptr(), self.len());\n  4429:         }\n  4430:     }\n  4431: \n  4432:     /// Function to calculate lengths of the middle and trailing slice for `align_to{,_mut}`.\n  4433:     fn align_to_offsets<U>(&self) -> (usize, usize) {\n  4434:         // What we gonna do about `rest` is figure out what multiple of `U`s we can put in a\n  4435:         // lowest number of `T`s. And how many `T`s we need for each such \"multiple\".\n  4436:         //\n  4437:         // Consider for example T=u8 U=u16. Then we can put 1 U in 2 Ts. Simple. Now, consider\n  4438:         // for example a case where size_of::<T> = 16, size_of::<U> = 24. We can put 2 Us in",
    "nanvix_source": "  4419:     ///     left.swap_with_slice(&mut right[1..]);\n  4420:     /// }\n  4421:     ///\n  4422:     /// assert_eq!(slice, [4, 5, 3, 1, 2]);\n  4423:     /// ```\n  4424:     ///\n  4425:     /// [`split_at_mut`]: slice::split_at_mut\n  4426:     #[stable(feature = \"swap_with_slice\", since = \"1.27.0\")]\n  4427:     #[rustc_const_unstable(feature = \"const_swap_with_slice\", issue = \"142204\")]\n  4428:     #[track_caller]\n  4429:     pub const fn swap_with_slice(&mut self, other: &mut [T]) {\n  4430:         assert!(self.len() == other.len(), \"destination and source slices have different lengths\");\n  4431:         // SAFETY: `self` is valid for `self.len()` elements by definition, and `src` was\n  4432:         // checked to have the same length. The slices cannot overlap because\n  4433:         // mutable references are exclusive.\n  4434:         unsafe {\n  4435:             ptr::swap_nonoverlapping(self.as_mut_ptr(), other.as_mut_ptr(), self.len());\n  4436:         }\n  4437:     }\n  4438: \n  4439:     /// Function to calculate lengths of the middle and trailing slice for `align_to{,_mut}`.",
    "previous_skip_rationale": "A useful contract must describe both mutable slice post-states. The determinism checker materializes each as a by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable swap semantics while avoiding this limitation."
  },
  {
    "target": "core::str::make_ascii_lowercase",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "make_ascii_lowercase",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
        "output": null
      }
    },
    "verification_source": "  2874:     /// [`to_ascii_lowercase()`].\n  2875:     ///\n  2876:     /// [`to_ascii_lowercase()`]: #method.to_ascii_lowercase\n  2877:     ///\n  2878:     /// # Examples\n  2879:     ///\n  2880:     /// ```\n  2881:     /// let mut s = String::from(\"GR\u00dc\u00dfE, J\u00dcRGEN \u2764\");\n  2882:     ///\n  2883:     /// s.make_ascii_lowercase();\n  2884:     ///\n  2885:     /// assert_eq!(\"gr\u00dc\u00dfe, j\u00dcrgen \u2764\", s);\n  2886:     /// ```\n  2887:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n  2888:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n  2889:     #[inline]\n  2890:     pub const fn make_ascii_lowercase(&mut self) {\n  2891:         // SAFETY: changing ASCII letters only does not invalidate UTF-8.\n  2892:         let me = unsafe { self.as_bytes_mut() };\n  2893:         me.make_ascii_lowercase()\n  2894:     }\n  2895: \n  2896:     /// Returns a string slice with leading ASCII whitespace removed.\n  2897:     ///\n  2898:     /// 'Whitespace' refers to the definition used by\n  2899:     /// [`u8::is_ascii_whitespace`].\n  2900:     ///\n  2901:     /// [`u8::is_ascii_whitespace`]: u8::is_ascii_whitespace\n  2902:     ///\n  2903:     /// # Examples\n  2904:     ///\n  2905:     /// ```\n  2906:     /// assert_eq!(\" \\t \\u{3000}hello world\\n\".trim_ascii_start(), \"\\u{3000}hello world\\n\");",
    "nanvix_source": "  2956:     /// ```\n  2957:     /// let mut s = String::from(\"GR\u00dc\u00dfE, J\u00dcRGEN \u2764\");\n  2958:     ///\n  2959:     /// s.make_ascii_lowercase();\n  2960:     ///\n  2961:     /// assert_eq!(\"gr\u00dc\u00dfe, j\u00dcrgen \u2764\", s);\n  2962:     /// ```\n  2963:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n  2964:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n  2965:     #[inline]\n  2966:     pub const fn make_ascii_lowercase(&mut self) {\n  2967:         // SAFETY: changing ASCII letters only does not invalidate UTF-8.\n  2968:         let me = unsafe { self.as_bytes_mut() };\n  2969:         me.make_ascii_lowercase()\n  2970:     }\n  2971: \n  2972:     /// Returns a string slice with leading ASCII whitespace removed.\n  2973:     ///\n  2974:     /// 'Whitespace' refers to the definition used by\n  2975:     /// [`u8::is_ascii_whitespace`]. Importantly, this definition excludes\n  2976:     /// the U+000B code point even though it has the Unicode [`White_Space`] property",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut str` receiver. The determinism checker currently materializes that state as by-value `str`, which is unsized and cannot typecheck. No contract-only revision can preserve the source signature and observable semantics while avoiding this limitation."
  },
  {
    "target": "core::str::make_ascii_uppercase",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "make_ascii_uppercase",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
        "output": null
      }
    },
    "verification_source": "  2846:     /// [`to_ascii_uppercase()`].\n  2847:     ///\n  2848:     /// [`to_ascii_uppercase()`]: #method.to_ascii_uppercase\n  2849:     ///\n  2850:     /// # Examples\n  2851:     ///\n  2852:     /// ```\n  2853:     /// let mut s = String::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  2854:     ///\n  2855:     /// s.make_ascii_uppercase();\n  2856:     ///\n  2857:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s);\n  2858:     /// ```\n  2859:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n  2860:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n  2861:     #[inline]\n  2862:     pub const fn make_ascii_uppercase(&mut self) {\n  2863:         // SAFETY: changing ASCII letters only does not invalidate UTF-8.\n  2864:         let me = unsafe { self.as_bytes_mut() };\n  2865:         me.make_ascii_uppercase()\n  2866:     }\n  2867: \n  2868:     /// Converts this string to its ASCII lower case equivalent in-place.\n  2869:     ///\n  2870:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n  2871:     /// but non-ASCII letters are unchanged.\n  2872:     ///\n  2873:     /// To return a new lowercased value without modifying the existing one, use\n  2874:     /// [`to_ascii_lowercase()`].\n  2875:     ///\n  2876:     /// [`to_ascii_lowercase()`]: #method.to_ascii_lowercase\n  2877:     ///\n  2878:     /// # Examples",
    "nanvix_source": "  2928:     /// ```\n  2929:     /// let mut s = String::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  2930:     ///\n  2931:     /// s.make_ascii_uppercase();\n  2932:     ///\n  2933:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s);\n  2934:     /// ```\n  2935:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n  2936:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n  2937:     #[inline]\n  2938:     pub const fn make_ascii_uppercase(&mut self) {\n  2939:         // SAFETY: changing ASCII letters only does not invalidate UTF-8.\n  2940:         let me = unsafe { self.as_bytes_mut() };\n  2941:         me.make_ascii_uppercase()\n  2942:     }\n  2943: \n  2944:     /// Converts this string to its ASCII lower case equivalent in-place.\n  2945:     ///\n  2946:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n  2947:     /// but non-ASCII letters are unchanged.\n  2948:     ///",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut str` receiver. The determinism checker materializes that state as by-value `str`, which is unsized and cannot typecheck. No contract-only revision can preserve the source signature and observable semantics while avoiding this limitation."
  },
  {
    "target": "core::str::substr_range",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "substr_range",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "substr",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
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
                        "id": 9993,
                        "path": "Range"
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
    "verification_source": "  3111:     ///\n  3112:     /// # Examples\n  3113:     /// ```\n  3114:     /// #![feature(substr_range)]\n  3115:     /// use core::range::Range;\n  3116:     ///\n  3117:     /// let data = \"a, b, b, a\";\n  3118:     /// let mut iter = data.split(\", \").map(|s| data.substr_range(s).unwrap());\n  3119:     ///\n  3120:     /// assert_eq!(iter.next(), Some(Range { start: 0, end: 1 }));\n  3121:     /// assert_eq!(iter.next(), Some(Range { start: 3, end: 4 }));\n  3122:     /// assert_eq!(iter.next(), Some(Range { start: 6, end: 7 }));\n  3123:     /// assert_eq!(iter.next(), Some(Range { start: 9, end: 10 }));\n  3124:     /// ```\n  3125:     #[must_use]\n  3126:     #[unstable(feature = \"substr_range\", issue = \"126769\")]\n  3127:     pub fn substr_range(&self, substr: &str) -> Option<Range<usize>> {\n  3128:         self.as_bytes().subslice_range(substr.as_bytes())\n  3129:     }\n  3130: \n  3131:     /// Returns the same string as a string slice `&str`.\n  3132:     ///\n  3133:     /// This method is redundant when used directly on `&str`, but\n  3134:     /// it helps dereferencing other string-like types to string slices,\n  3135:     /// for example references to `Box<str>` or `Arc<str>`.\n  3136:     #[inline]\n  3137:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]\n  3138:     pub const fn as_str(&self) -> &str {\n  3139:         self\n  3140:     }\n  3141: }\n  3142: \n  3143: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "  3201:     /// let data = \"a, b, b, a\";\n  3202:     /// let mut iter = data.split(\", \").map(|s| data.substr_range(s).unwrap());\n  3203:     ///\n  3204:     /// assert_eq!(iter.next(), Some(Range { start: 0, end: 1 }));\n  3205:     /// assert_eq!(iter.next(), Some(Range { start: 3, end: 4 }));\n  3206:     /// assert_eq!(iter.next(), Some(Range { start: 6, end: 7 }));\n  3207:     /// assert_eq!(iter.next(), Some(Range { start: 9, end: 10 }));\n  3208:     /// ```\n  3209:     #[must_use]\n  3210:     #[stable(feature = \"substr_range\", since = \"CURRENT_RUSTC_VERSION\")]\n  3211:     pub fn substr_range(&self, substr: &str) -> Option<Range<usize>> {\n  3212:         self.as_bytes().subslice_range(substr.as_bytes())\n  3213:     }\n  3214: \n  3215:     /// Returns the same string as a string slice `&str`.\n  3216:     ///\n  3217:     /// This method is redundant when used directly on `&str`, but\n  3218:     /// it helps dereferencing other string-like types to string slices,\n  3219:     /// for example references to `Box<str>` or `Arc<str>`.\n  3220:     #[inline]\n  3221:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]",
    "previous_skip_rationale": "The exact return type core::range::Range<usize> is not modeled by current vstd, so the declaration cannot typecheck without a separate external type specification. Moreover, None versus Some depends on pointer location, and the documented empty-string false positives prevent characterizing it from semantic string views."
  },
  {
    "target": "std::collections::HashMap::get_key_value",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
    ],
    "category": "other",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Q"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Q"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 399,
                      "path": "Borrow"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 554,
                      "path": "Hash"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 136,
                      "path": "Eq"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Q"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "get_key_value",
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
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "K"
                }
              }
            },
            {
              "bound_predicate": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
                }
              }
            },
            {
              "bound_predicate": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 834,
                        "path": "Allocator"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "A"
                }
              }
            }
          ]
        },
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          ],
          [
            "k",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "generic": "K"
                            }
                          }
                        },
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "generic": "V"
                            }
                          }
                        }
                      ]
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1072:     ///     }\n  1073:     /// }\n  1074:     ///\n  1075:     /// let j_a = S { id: 1, name: \"Jessica\" };\n  1076:     /// let j_b = S { id: 1, name: \"Jess\" };\n  1077:     /// let p = S { id: 2, name: \"Paul\" };\n  1078:     /// assert_eq!(j_a, j_b);\n  1079:     ///\n  1080:     /// let mut map = HashMap::new();\n  1081:     /// map.insert(j_a, \"Paris\");\n  1082:     /// assert_eq!(map.get_key_value(&j_a), Some((&j_a, &\"Paris\")));\n  1083:     /// assert_eq!(map.get_key_value(&j_b), Some((&j_a, &\"Paris\"))); // the notable case\n  1084:     /// assert_eq!(map.get_key_value(&p), None);\n  1085:     /// ```\n  1086:     #[inline]\n  1087:     #[stable(feature = \"map_get_key_value\", since = \"1.40.0\")]\n  1088:     pub fn get_key_value<Q: ?Sized>(&self, k: &Q) -> Option<(&K, &V)>\n  1089:     where\n  1090:         K: Borrow<Q>,\n  1091:         Q: Hash + Eq,\n  1092:     {\n  1093:         self.base.get_key_value(k)\n  1094:     }\n  1095: \n  1096:     /// Attempts to get mutable references to `N` values in the map at once.\n  1097:     ///\n  1098:     /// Returns an array of length `N` with the results of each query. For soundness, at most one\n  1099:     /// mutable reference will be returned to any value. `None` will be used if the key is missing.\n  1100:     ///\n  1101:     /// This method performs a check to ensure there are no duplicate keys, which currently has a time-complexity of O(n^2),\n  1102:     /// so be careful when passing many keys.\n  1103:     ///\n  1104:     /// # Panics",
    "nanvix_source": "  1083:     /// assert_eq!(j_a, j_b);\n  1084:     ///\n  1085:     /// let mut map = HashMap::new();\n  1086:     /// map.insert(j_a, \"Paris\");\n  1087:     /// assert_eq!(map.get_key_value(&j_a), Some((&j_a, &\"Paris\")));\n  1088:     /// assert_eq!(map.get_key_value(&j_b), Some((&j_a, &\"Paris\"))); // the notable case\n  1089:     /// assert_eq!(map.get_key_value(&p), None);\n  1090:     /// ```\n  1091:     #[inline]\n  1092:     #[stable(feature = \"map_get_key_value\", since = \"1.40.0\")]\n  1093:     pub fn get_key_value<Q: ?Sized>(&self, k: &Q) -> Option<(&K, &V)>\n  1094:     where\n  1095:         K: Borrow<Q>,\n  1096:         Q: Hash + Eq,\n  1097:     {\n  1098:         self.base.get_key_value(k)\n  1099:     }\n  1100: \n  1101:     /// Attempts to get mutable references to `N` values in the map at once.\n  1102:     ///\n  1103:     /// Returns an array of length `N` with the results of each query. For soundness, at most one",
    "previous_skip_rationale": "For generic Borrow<Q>, vstd's borrowed-key predicates are uninterpreted and provide no functionality law establishing a unique stored key. Thus the observable key-value pair cannot be determined without an ad hoc choice, uniqueness assertion, or unjustified precondition."
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
