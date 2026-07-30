For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::make_ascii_lowercase",
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
          "slice": {
            "primitive": "u8"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51785",
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
    "verification_source": "   179:             i += 1;\n   180:         }\n   181:     }\n   182: \n   183:     /// Converts this slice to its ASCII lower case equivalent in-place.\n   184:     ///\n   185:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n   186:     /// but non-ASCII letters are unchanged.\n   187:     ///\n   188:     /// To return a new lowercased value without modifying the existing one, use\n   189:     /// [`to_ascii_lowercase`].\n   190:     ///\n   191:     /// [`to_ascii_lowercase`]: #method.to_ascii_lowercase\n   192:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n   193:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n   194:     #[inline]\n   195:     pub const fn make_ascii_lowercase(&mut self) {\n   196:         // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.\n   197:         let mut i = 0;\n   198:         while i < self.len() {\n   199:             let byte = &mut self[i];\n   200:             byte.make_ascii_lowercase();\n   201:             i += 1;\n   202:         }\n   203:     }\n   204: \n   205:     /// Returns an iterator that produces an escaped version of this slice,\n   206:     /// treating it as an ASCII string.\n   207:     ///\n   208:     /// # Examples\n   209:     ///\n   210:     /// ```\n   211:     /// let s = b\"0\\t\\r\\n'\\\"\\\\\\x9d\";",
    "nanvix_source": "   185:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n   186:     /// but non-ASCII letters are unchanged.\n   187:     ///\n   188:     /// To return a new lowercased value without modifying the existing one, use\n   189:     /// [`to_ascii_lowercase`].\n   190:     ///\n   191:     /// [`to_ascii_lowercase`]: #method.to_ascii_lowercase\n   192:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n   193:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n   194:     #[inline]\n   195:     pub const fn make_ascii_lowercase(&mut self) {\n   196:         // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.\n   197:         let mut i = 0;\n   198:         while i < self.len() {\n   199:             let byte = &mut self[i];\n   200:             byte.make_ascii_lowercase();\n   201:             i += 1;\n   202:         }\n   203:     }\n   204: \n   205:     /// Returns an iterator that produces an escaped version of this slice,",
    "previous_skip_rationale": "A useful contract must model the final `&mut [u8]` contents. Although reversing the comparison operands avoids the terminator-parser crash, the determinism checker then materializes the mutable slice as unsized by-value `[u8]`, which cannot use vstd's Sized-only extensional equality."
  },
  {
    "target": "core::slice::make_ascii_uppercase",
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
          "slice": {
            "primitive": "u8"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51785",
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
    "verification_source": "   157: \n   158:         true\n   159:     }\n   160: \n   161:     /// Converts this slice to its ASCII upper case equivalent in-place.\n   162:     ///\n   163:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n   164:     /// but non-ASCII letters are unchanged.\n   165:     ///\n   166:     /// To return a new uppercased value without modifying the existing one, use\n   167:     /// [`to_ascii_uppercase`].\n   168:     ///\n   169:     /// [`to_ascii_uppercase`]: #method.to_ascii_uppercase\n   170:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n   171:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n   172:     #[inline]\n   173:     pub const fn make_ascii_uppercase(&mut self) {\n   174:         // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.\n   175:         let mut i = 0;\n   176:         while i < self.len() {\n   177:             let byte = &mut self[i];\n   178:             byte.make_ascii_uppercase();\n   179:             i += 1;\n   180:         }\n   181:     }\n   182: \n   183:     /// Converts this slice to its ASCII lower case equivalent in-place.\n   184:     ///\n   185:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n   186:     /// but non-ASCII letters are unchanged.\n   187:     ///\n   188:     /// To return a new lowercased value without modifying the existing one, use\n   189:     /// [`to_ascii_lowercase`].",
    "nanvix_source": "   163:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n   164:     /// but non-ASCII letters are unchanged.\n   165:     ///\n   166:     /// To return a new uppercased value without modifying the existing one, use\n   167:     /// [`to_ascii_uppercase`].\n   168:     ///\n   169:     /// [`to_ascii_uppercase`]: #method.to_ascii_uppercase\n   170:     #[stable(feature = \"ascii_methods_on_intrinsics\", since = \"1.23.0\")]\n   171:     #[rustc_const_stable(feature = \"const_make_ascii\", since = \"1.84.0\")]\n   172:     #[inline]\n   173:     pub const fn make_ascii_uppercase(&mut self) {\n   174:         // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.\n   175:         let mut i = 0;\n   176:         while i < self.len() {\n   177:             let byte = &mut self[i];\n   178:             byte.make_ascii_uppercase();\n   179:             i += 1;\n   180:         }\n   181:     }\n   182: \n   183:     /// Converts this slice to its ASCII lower case equivalent in-place.",
    "previous_skip_rationale": "Numeric u8 constants fix the byte-literal typecheck error, but any useful contract must model the final `&mut [u8]` state. The determinism checker materializes this state as unsized by-value `[u8]`, which cannot be compared by its Sized-only extensional equality."
  },
  {
    "target": "core::slice::reverse",
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
      "name": "reverse",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   962:             ptr::swap(ptr.add(a), ptr.add(b));\n   963:         }\n   964:     }\n   965: \n   966:     /// Reverses the order of elements in the slice, in place.\n   967:     ///\n   968:     /// # Examples\n   969:     ///\n   970:     /// ```\n   971:     /// let mut v = [1, 2, 3];\n   972:     /// v.reverse();\n   973:     /// assert!(v == [3, 2, 1]);\n   974:     /// ```\n   975:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   976:     #[rustc_const_stable(feature = \"const_slice_reverse\", since = \"1.90.0\")]\n   977:     #[inline]\n   978:     pub const fn reverse(&mut self) {\n   979:         let half_len = self.len() / 2;\n   980:         let Range { start, end } = self.as_mut_ptr_range();\n   981: \n   982:         // These slices will skip the middle item for an odd length,\n   983:         // since that one doesn't need to move.\n   984:         let (front_half, back_half) =\n   985:             // SAFETY: Both are subparts of the original slice, so the memory\n   986:             // range is valid, and they don't overlap because they're each only\n   987:             // half (or less) of the original slice.\n   988:             unsafe {\n   989:                 (\n   990:                     slice::from_raw_parts_mut(start, half_len),\n   991:                     slice::from_raw_parts_mut(end.sub(half_len), half_len),\n   992:                 )\n   993:             };\n   994: ",
    "nanvix_source": "   971:     /// # Examples\n   972:     ///\n   973:     /// ```\n   974:     /// let mut v = [1, 2, 3];\n   975:     /// v.reverse();\n   976:     /// assert!(v == [3, 2, 1]);\n   977:     /// ```\n   978:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   979:     #[rustc_const_stable(feature = \"const_slice_reverse\", since = \"1.90.0\")]\n   980:     #[inline]\n   981:     pub const fn reverse(&mut self) {\n   982:         let half_len = self.len() / 2;\n   983:         let Range { start, end } = self.as_mut_ptr_range();\n   984: \n   985:         // These slices will skip the middle item for an odd length,\n   986:         // since that one doesn't need to move.\n   987:         let (front_half, back_half) =\n   988:             // SAFETY: Both are subparts of the original slice, so the memory\n   989:             // range is valid, and they don't overlap because they're each only\n   990:             // half (or less) of the original slice.\n   991:             unsafe {",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut [T]` receiver. The determinism checker materializes that state as by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable reversal semantics while avoiding this limitation."
  },
  {
    "target": "core::slice::rotate_left",
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
      "name": "rotate_left",
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
            "mid",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3868:     ///\n  3869:     /// ```\n  3870:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3871:     /// a.rotate_left(2);\n  3872:     /// assert_eq!(a, ['c', 'd', 'e', 'f', 'a', 'b']);\n  3873:     /// ```\n  3874:     ///\n  3875:     /// Rotating a subslice:\n  3876:     ///\n  3877:     /// ```\n  3878:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3879:     /// a[1..5].rotate_left(1);\n  3880:     /// assert_eq!(a, ['a', 'c', 'd', 'e', 'b', 'f']);\n  3881:     /// ```\n  3882:     #[stable(feature = \"slice_rotate\", since = \"1.26.0\")]\n  3883:     #[rustc_const_stable(feature = \"const_slice_rotate\", since = \"1.92.0\")]\n  3884:     pub const fn rotate_left(&mut self, mid: usize) {\n  3885:         assert!(mid <= self.len());\n  3886:         let k = self.len() - mid;\n  3887:         let p = self.as_mut_ptr();\n  3888: \n  3889:         // SAFETY: The range `[p.add(mid) - mid, p.add(mid) + k)` is trivially\n  3890:         // valid for reading and writing, as required by `ptr_rotate`.\n  3891:         unsafe {\n  3892:             rotate::ptr_rotate(mid, p.add(mid), k);\n  3893:         }\n  3894:     }\n  3895: \n  3896:     /// Rotates the slice in-place such that the first `self.len() - k`\n  3897:     /// elements of the slice move to the end while the last `k` elements move\n  3898:     /// to the front.\n  3899:     ///\n  3900:     /// After calling `rotate_right`, the element previously at index",
    "nanvix_source": "  3880:     ///\n  3881:     /// Rotating a subslice:\n  3882:     ///\n  3883:     /// ```\n  3884:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3885:     /// a[1..5].rotate_left(1);\n  3886:     /// assert_eq!(a, ['a', 'c', 'd', 'e', 'b', 'f']);\n  3887:     /// ```\n  3888:     #[stable(feature = \"slice_rotate\", since = \"1.26.0\")]\n  3889:     #[rustc_const_stable(feature = \"const_slice_rotate\", since = \"1.92.0\")]\n  3890:     pub const fn rotate_left(&mut self, mid: usize) {\n  3891:         assert!(mid <= self.len());\n  3892:         let k = self.len() - mid;\n  3893:         let p = self.as_mut_ptr();\n  3894: \n  3895:         // SAFETY: The range `[p.add(mid) - mid, p.add(mid) + k)` is trivially\n  3896:         // valid for reading and writing, as required by `ptr_rotate`.\n  3897:         unsafe {\n  3898:             rotate::ptr_rotate(mid, p.add(mid), k);\n  3899:         }\n  3900:     }",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut [T]` receiver. The determinism checker materializes that state as by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable rotation semantics while avoiding this limitation."
  },
  {
    "target": "core::slice::rotate_right",
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
      "name": "rotate_right",
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
            "k",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3914:     ///\n  3915:     /// ```\n  3916:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3917:     /// a.rotate_right(2);\n  3918:     /// assert_eq!(a, ['e', 'f', 'a', 'b', 'c', 'd']);\n  3919:     /// ```\n  3920:     ///\n  3921:     /// Rotating a subslice:\n  3922:     ///\n  3923:     /// ```\n  3924:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3925:     /// a[1..5].rotate_right(1);\n  3926:     /// assert_eq!(a, ['a', 'e', 'b', 'c', 'd', 'f']);\n  3927:     /// ```\n  3928:     #[stable(feature = \"slice_rotate\", since = \"1.26.0\")]\n  3929:     #[rustc_const_stable(feature = \"const_slice_rotate\", since = \"1.92.0\")]\n  3930:     pub const fn rotate_right(&mut self, k: usize) {\n  3931:         assert!(k <= self.len());\n  3932:         let mid = self.len() - k;\n  3933:         let p = self.as_mut_ptr();\n  3934: \n  3935:         // SAFETY: The range `[p.add(mid) - mid, p.add(mid) + k)` is trivially\n  3936:         // valid for reading and writing, as required by `ptr_rotate`.\n  3937:         unsafe {\n  3938:             rotate::ptr_rotate(mid, p.add(mid), k);\n  3939:         }\n  3940:     }\n  3941: \n  3942:     /// Moves the elements of this slice `N` places to the left, returning the ones\n  3943:     /// that \"fall off\" the front, and putting `inserted` at the end.\n  3944:     ///\n  3945:     /// Equivalently, you can think of concatenating `self` and `inserted` into one\n  3946:     /// long sequence, then returning the left-most `N` items and the rest into `self`:",
    "nanvix_source": "  3926:     ///\n  3927:     /// Rotating a subslice:\n  3928:     ///\n  3929:     /// ```\n  3930:     /// let mut a = ['a', 'b', 'c', 'd', 'e', 'f'];\n  3931:     /// a[1..5].rotate_right(1);\n  3932:     /// assert_eq!(a, ['a', 'e', 'b', 'c', 'd', 'f']);\n  3933:     /// ```\n  3934:     #[stable(feature = \"slice_rotate\", since = \"1.26.0\")]\n  3935:     #[rustc_const_stable(feature = \"const_slice_rotate\", since = \"1.92.0\")]\n  3936:     pub const fn rotate_right(&mut self, k: usize) {\n  3937:         assert!(k <= self.len());\n  3938:         let mid = self.len() - k;\n  3939:         let p = self.as_mut_ptr();\n  3940: \n  3941:         // SAFETY: The range `[p.add(mid) - mid, p.add(mid) + k)` is trivially\n  3942:         // valid for reading and writing, as required by `ptr_rotate`.\n  3943:         unsafe {\n  3944:             rotate::ptr_rotate(mid, p.add(mid), k);\n  3945:         }\n  3946:     }",
    "previous_skip_rationale": "A useful contract must describe the rotated post-state of the exact `&mut [T]` receiver. The determinism checker materializes that state as by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable rotation semantics while avoiding this limitation."
  },
  {
    "target": "core::slice::split_off",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                        "id": 23782,
                        "path": "OneSidedRange"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
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
      "name": "split_off",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
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
                  "borrowed_ref": {
                    "is_mutable": false,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
                  }
                }
              }
            }
          ],
          [
            "range",
            {
              "generic": "R"
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
                          "generic": "Self"
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
    "verification_source": "  4890:     /// ```\n  4891:     ///\n  4892:     /// Getting `None` when `range` is out of bounds:\n  4893:     ///\n  4894:     /// ```\n  4895:     /// let mut slice: &[_] = &['a', 'b', 'c', 'd'];\n  4896:     ///\n  4897:     /// assert_eq!(None, slice.split_off(5..));\n  4898:     /// assert_eq!(None, slice.split_off(..5));\n  4899:     /// assert_eq!(None, slice.split_off(..=4));\n  4900:     /// let expected: &[char] = &['a', 'b', 'c', 'd'];\n  4901:     /// assert_eq!(Some(expected), slice.split_off(..4));\n  4902:     /// ```\n  4903:     #[inline]\n  4904:     #[must_use = \"method does not modify the slice if the range is out of bounds\"]\n  4905:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  4906:     pub fn split_off<'a, R: OneSidedRange<usize>>(\n  4907:         self: &mut &'a Self,\n  4908:         range: R,\n  4909:     ) -> Option<&'a Self> {\n  4910:         let (direction, split_index) = split_point_of(range)?;\n  4911:         if split_index > self.len() {\n  4912:             return None;\n  4913:         }\n  4914:         let (front, back) = self.split_at(split_index);\n  4915:         match direction {\n  4916:             Direction::Front => {\n  4917:                 *self = back;\n  4918:                 Some(front)\n  4919:             }\n  4920:             Direction::Back => {\n  4921:                 *self = front;\n  4922:                 Some(back)",
    "nanvix_source": "  4903:     ///\n  4904:     /// assert_eq!(None, slice.split_off(5..));\n  4905:     /// assert_eq!(None, slice.split_off(..5));\n  4906:     /// assert_eq!(None, slice.split_off(..=4));\n  4907:     /// let expected: &[char] = &['a', 'b', 'c', 'd'];\n  4908:     /// assert_eq!(Some(expected), slice.split_off(..4));\n  4909:     /// ```\n  4910:     #[inline]\n  4911:     #[must_use = \"method does not modify the slice if the range is out of bounds\"]\n  4912:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  4913:     pub fn split_off<'a, R: OneSidedRange<usize>>(\n  4914:         self: &mut &'a Self,\n  4915:         range: R,\n  4916:     ) -> Option<&'a Self> {\n  4917:         let (direction, split_index) = split_point_of(range)?;\n  4918:         if split_index > self.len() {\n  4919:             return None;\n  4920:         }\n  4921:         let (front, back) = self.split_at(split_index);\n  4922:         match direction {\n  4923:             Direction::Front => {",
    "previous_skip_rationale": "A useful deterministic contract must model both the mutated nested slice reference and how R selects the split direction and index. The checker materializes the slice post-state as unsized by-value `[T]`, while existing vstd vocabulary has no declared semantic model for OneSidedRange::bound. The previous prefix-or-suffix disjunction therefore remains nondeterministic, and no source-justified ordinary contract-only revision avoids both limitations."
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
