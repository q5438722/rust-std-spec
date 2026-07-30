For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::mem::MaybeUninit::assume_init_read",
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
      "name": "assume_init_read",
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
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   777:     /// *Incorrect* usage of this method:\n   778:     ///\n   779:     /// ```rust,no_run\n   780:     /// use std::mem::MaybeUninit;\n   781:     ///\n   782:     /// let mut x = MaybeUninit::<Option<Vec<u32>>>::uninit();\n   783:     /// x.write(Some(vec![0, 1, 2]));\n   784:     /// let x1 = unsafe { x.assume_init_read() };\n   785:     /// let x2 = unsafe { x.assume_init_read() };\n   786:     /// // We now created two copies of the same vector, leading to a double-free \u26a0\ufe0f when\n   787:     /// // they both get dropped!\n   788:     /// ```\n   789:     #[stable(feature = \"maybe_uninit_extra\", since = \"1.60.0\")]\n   790:     #[rustc_const_stable(feature = \"const_maybe_uninit_assume_init_read\", since = \"1.75.0\")]\n   791:     #[inline(always)]\n   792:     #[track_caller]\n   793:     pub const unsafe fn assume_init_read(&self) -> T {\n   794:         // SAFETY: the caller must guarantee that `self` is initialized.\n   795:         // Reading from `self.as_ptr()` is safe since `self` should be initialized.\n   796:         unsafe {\n   797:             intrinsics::assert_inhabited::<T>();\n   798:             self.as_ptr().read()\n   799:         }\n   800:     }\n   801: \n   802:     /// Drops the contained value in place.\n   803:     ///\n   804:     /// If you have ownership of the `MaybeUninit`, you can also use\n   805:     /// [`assume_init`] as an alternative.\n   806:     ///\n   807:     /// # Safety\n   808:     ///\n   809:     /// It is up to the caller to guarantee that the `MaybeUninit<T>` really is",
    "nanvix_source": "   784:     /// x.write(Some(vec![0, 1, 2]));\n   785:     /// let x1 = unsafe { x.assume_init_read() };\n   786:     /// let x2 = unsafe { x.assume_init_read() };\n   787:     /// // We now created two copies of the same vector, leading to a double-free \u26a0\ufe0f when\n   788:     /// // they both get dropped!\n   789:     /// ```\n   790:     #[stable(feature = \"maybe_uninit_extra\", since = \"1.60.0\")]\n   791:     #[rustc_const_stable(feature = \"const_maybe_uninit_assume_init_read\", since = \"1.75.0\")]\n   792:     #[inline(always)]\n   793:     #[track_caller]\n   794:     pub const unsafe fn assume_init_read(&self) -> T {\n   795:         // SAFETY: the caller must guarantee that `self` is initialized.\n   796:         // Reading from `self.as_ptr()` is safe since `self` should be initialized.\n   797:         unsafe {\n   798:             intrinsics::assert_inhabited::<T>();\n   799:             self.as_ptr().read()\n   800:         }\n   801:     }\n   802: \n   803:     /// Drops the contained value in place.\n   804:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::transmute_copy",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
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
            "name": "Src"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Dst"
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
      "name": "transmute_copy",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "src",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Src"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Dst"
        }
      }
    },
    "verification_source": "  1056: ///     let mut foo_struct: Foo = mem::transmute_copy(&foo_array);\n  1057: ///     assert_eq!(foo_struct.bar, 10);\n  1058: ///\n  1059: ///     // Modify the copied data\n  1060: ///     foo_struct.bar = 20;\n  1061: ///     assert_eq!(foo_struct.bar, 20);\n  1062: /// }\n  1063: ///\n  1064: /// // The contents of 'foo_array' should not have changed\n  1065: /// assert_eq!(foo_array, [10]);\n  1066: /// ```\n  1067: #[inline]\n  1068: #[must_use]\n  1069: #[track_caller]\n  1070: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1071: #[rustc_const_stable(feature = \"const_transmute_copy\", since = \"1.74.0\")]\n  1072: pub const unsafe fn transmute_copy<Src, Dst>(src: &Src) -> Dst {\n  1073:     assert!(\n  1074:         size_of::<Src>() >= size_of::<Dst>(),\n  1075:         \"cannot transmute_copy if Dst is larger than Src\"\n  1076:     );\n  1077: \n  1078:     // If Dst has a higher alignment requirement, src might not be suitably aligned.\n  1079:     if align_of::<Dst>() > align_of::<Src>() {\n  1080:         // SAFETY: `src` is a reference which is guaranteed to be valid for reads.\n  1081:         // The caller must guarantee that the actual transmutation is safe.\n  1082:         unsafe { ptr::read_unaligned(src as *const Src as *const Dst) }\n  1083:     } else {\n  1084:         // SAFETY: `src` is a reference which is guaranteed to be valid for reads.\n  1085:         // We just checked that `src as *const Dst` was properly aligned.\n  1086:         // The caller must guarantee that the actual transmutation is safe.\n  1087:         unsafe { ptr::read(src as *const Src as *const Dst) }\n  1088:     }",
    "nanvix_source": "  1128: /// assert_eq!(\n  1129: ///     unsafe { mem::transmute_copy::<[u8], u32>(bytes) },\n  1130: ///     u32::from_ne_bytes(*bytes.first_chunk().unwrap()),\n  1131: /// );\n  1132: /// ```\n  1133: #[inline]\n  1134: #[must_use]\n  1135: #[track_caller]\n  1136: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1137: #[rustc_const_stable(feature = \"const_transmute_copy\", since = \"1.74.0\")]\n  1138: pub const unsafe fn transmute_copy<Src: ?Sized, Dst>(src: &Src) -> Dst {\n  1139:     // library UB because it's possible for the `Src` to be only a subset of the allocation\n  1140:     // and thus for a failure to not be immediate language UB\n  1141:     assert_unsafe_precondition!(\n  1142:         check_library_ub,\n  1143:         \"cannot transmute_copy if Dst is larger than Src\",\n  1144:         (\n  1145:             src_size: usize = size_of_val::<Src>(src),\n  1146:             dst_size: usize = Dst::SIZE,\n  1147:         ) => src_size >= dst_size\n  1148:     );",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::uninitialized",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "uninitialized",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   730: /// is special in that the compiler knows that it does not have a fixed value.\n   731: /// This makes it undefined behavior to have uninitialized data in a variable even\n   732: /// if that variable has an integer type.\n   733: ///\n   734: /// Therefore, it is immediate undefined behavior to call this function on nearly all types,\n   735: /// including integer types and arrays of integer types, and even if the result is unused.\n   736: ///\n   737: /// [uninit]: MaybeUninit::uninit\n   738: /// [assume_init]: MaybeUninit::assume_init\n   739: /// [inv]: MaybeUninit#initialization-invariant\n   740: #[inline(always)]\n   741: #[must_use]\n   742: #[deprecated(since = \"1.39.0\", note = \"use `mem::MaybeUninit` instead\")]\n   743: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   744: #[rustc_diagnostic_item = \"mem_uninitialized\"]\n   745: #[track_caller]\n   746: pub unsafe fn uninitialized<T>() -> T {\n   747:     // SAFETY: the caller must guarantee that an uninitialized value is valid for `T`.\n   748:     unsafe {\n   749:         intrinsics::assert_mem_uninitialized_valid::<T>();\n   750:         let mut val = MaybeUninit::<T>::uninit();\n   751: \n   752:         // Fill memory with 0x01, as an imperfect mitigation for old code that uses this function on\n   753:         // bool, nonnull, and noundef types. But don't do this if we actively want to detect UB.\n   754:         if !cfg!(any(miri, sanitize = \"memory\")) {\n   755:             val.as_mut_ptr().write_bytes(0x01, 1);\n   756:         }\n   757: \n   758:         val.assume_init()\n   759:     }\n   760: }\n   761: \n   762: /// Swaps the values at two mutable locations, without deinitializing either one.",
    "nanvix_source": "   775: ///\n   776: /// [uninit]: MaybeUninit::uninit\n   777: /// [assume_init]: MaybeUninit::assume_init\n   778: /// [inv]: MaybeUninit#initialization-invariant\n   779: #[inline(always)]\n   780: #[must_use]\n   781: #[deprecated(since = \"1.39.0\", note = \"use `mem::MaybeUninit` instead\")]\n   782: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   783: #[rustc_diagnostic_item = \"mem_uninitialized\"]\n   784: #[track_caller]\n   785: pub unsafe fn uninitialized<T>() -> T {\n   786:     // SAFETY: the caller must guarantee that an uninitialized value is valid for `T`.\n   787:     unsafe {\n   788:         intrinsics::assert_mem_uninitialized_valid::<T>();\n   789:         let mut val = MaybeUninit::<T>::uninit();\n   790: \n   791:         // Fill memory with 0x01, as an imperfect mitigation for old code that uses this function on\n   792:         // bool, nonnull, and noundef types. But don't do this if we actively want to detect UB.\n   793:         if !cfg!(any(miri, sanitize = \"memory\")) {\n   794:             val.as_mut_ptr().write_bytes(0x01, 1);\n   795:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::zeroed",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
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
      "name": "zeroed",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "   693: ///\n   694: /// *Incorrect* usage of this function: initializing a reference with zero.\n   695: ///\n   696: /// ```rust,no_run\n   697: /// # #![allow(invalid_value)]\n   698: /// use std::mem;\n   699: ///\n   700: /// let _x: &i32 = unsafe { mem::zeroed() }; // Undefined behavior!\n   701: /// let _y: fn() = unsafe { mem::zeroed() }; // And again!\n   702: /// ```\n   703: #[inline(always)]\n   704: #[must_use]\n   705: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   706: #[rustc_diagnostic_item = \"mem_zeroed\"]\n   707: #[track_caller]\n   708: #[rustc_const_stable(feature = \"const_mem_zeroed\", since = \"1.75.0\")]\n   709: pub const unsafe fn zeroed<T>() -> T {\n   710:     // SAFETY: the caller must guarantee that an all-zero value is valid for `T`.\n   711:     unsafe {\n   712:         intrinsics::assert_zero_valid::<T>();\n   713:         MaybeUninit::zeroed().assume_init()\n   714:     }\n   715: }\n   716: \n   717: /// Bypasses Rust's normal memory-initialization checks by pretending to\n   718: /// produce a value of type `T`, while doing nothing at all.\n   719: ///\n   720: /// **This function is deprecated.** Use [`MaybeUninit<T>`] instead.\n   721: /// It also might be slower than using `MaybeUninit<T>` due to mitigations that were put in place to\n   722: /// limit the potential harm caused by incorrect use of this function in legacy code.\n   723: ///\n   724: /// The reason for deprecation is that the function basically cannot be used\n   725: /// correctly: it has the same effect as [`MaybeUninit::uninit().assume_init()`][uninit].",
    "nanvix_source": "   738: ///\n   739: /// let _x: &i32 = unsafe { mem::zeroed() }; // Undefined behavior!\n   740: /// let _y: fn() = unsafe { mem::zeroed() }; // And again!\n   741: /// ```\n   742: #[inline(always)]\n   743: #[must_use]\n   744: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   745: #[rustc_diagnostic_item = \"mem_zeroed\"]\n   746: #[track_caller]\n   747: #[rustc_const_stable(feature = \"const_mem_zeroed\", since = \"1.75.0\")]\n   748: pub const unsafe fn zeroed<T>() -> T {\n   749:     // SAFETY: the caller must guarantee that an all-zero value is valid for `T`.\n   750:     unsafe {\n   751:         intrinsics::assert_zero_valid::<T>();\n   752:         MaybeUninit::zeroed().assume_init()\n   753:     }\n   754: }\n   755: \n   756: /// Bypasses Rust's normal memory-initialization checks by pretending to\n   757: /// produce a value of type `T`, while doing nothing at all.\n   758: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::copied",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
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
                      "id": 6,
                      "path": "Copy"
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
        "is_unsafe": false
      },
      "name": "copied",
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
                      "borrowed_ref": {
                        "is_mutable": false,
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28063",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
    "verification_source": "  2118: impl<T> Option<&T> {\n  2119:     /// Maps an `Option<&T>` to an `Option<T>` by copying the contents of the\n  2120:     /// option.\n  2121:     ///\n  2122:     /// # Examples\n  2123:     ///\n  2124:     /// ```\n  2125:     /// let x = 12;\n  2126:     /// let opt_x = Some(&x);\n  2127:     /// assert_eq!(opt_x, Some(&12));\n  2128:     /// let copied = opt_x.copied();\n  2129:     /// assert_eq!(copied, Some(12));\n  2130:     /// ```\n  2131:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2132:     #[stable(feature = \"copied\", since = \"1.35.0\")]\n  2133:     #[rustc_const_stable(feature = \"const_option\", since = \"1.83.0\")]\n  2134:     pub const fn copied(self) -> Option<T>\n  2135:     where\n  2136:         T: Copy,\n  2137:     {\n  2138:         // FIXME(const-hack): this implementation, which sidesteps using `Option::map` since it's not const\n  2139:         // ready yet, should be reverted when possible to avoid code repetition\n  2140:         match self {\n  2141:             Some(&v) => Some(v),\n  2142:             None => None,\n  2143:         }\n  2144:     }\n  2145: \n  2146:     /// Maps an `Option<&T>` to an `Option<T>` by cloning the contents of the\n  2147:     /// option.\n  2148:     ///\n  2149:     /// # Examples\n  2150:     ///",
    "nanvix_source": "  2124:     /// ```\n  2125:     /// let x = 12;\n  2126:     /// let opt_x = Some(&x);\n  2127:     /// assert_eq!(opt_x, Some(&12));\n  2128:     /// let copied = opt_x.copied();\n  2129:     /// assert_eq!(copied, Some(12));\n  2130:     /// ```\n  2131:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2132:     #[stable(feature = \"copied\", since = \"1.35.0\")]\n  2133:     #[rustc_const_stable(feature = \"const_option\", since = \"1.83.0\")]\n  2134:     pub const fn copied(self) -> Option<T>\n  2135:     where\n  2136:         T: Copy,\n  2137:     {\n  2138:         // FIXME(const-hack): this implementation, which sidesteps using `Option::map` since it's not const\n  2139:         // ready yet, should be reverted when possible to avoid code repetition\n  2140:         match self {\n  2141:             Some(&v) => Some(v),\n  2142:             None => None,\n  2143:         }\n  2144:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::unwrap_unchecked",
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
      "name": "unwrap_unchecked",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
    "verification_source": "  1112:     /// # Examples\n  1113:     ///\n  1114:     /// ```\n  1115:     /// let x = Some(\"air\");\n  1116:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, \"air\");\n  1117:     /// ```\n  1118:     ///\n  1119:     /// ```no_run\n  1120:     /// let x: Option<&str> = None;\n  1121:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, \"air\"); // Undefined behavior!\n  1122:     /// ```\n  1123:     #[inline]\n  1124:     #[track_caller]\n  1125:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1126:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1127:     #[rustc_const_stable(feature = \"const_option\", since = \"1.83.0\")]\n  1128:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1129:         match self {\n  1130:             Some(val) => val,\n  1131:             // SAFETY: the safety contract must be upheld by the caller.\n  1132:             None => unsafe { hint::unreachable_unchecked() },\n  1133:         }\n  1134:     }\n  1135: \n  1136:     /////////////////////////////////////////////////////////////////////////\n  1137:     // Transforming contained values\n  1138:     /////////////////////////////////////////////////////////////////////////\n  1139: \n  1140:     /// Maps an `Option<T>` to `Option<U>` by applying a function to a contained value (if `Some`) or returns `None` (if `None`).\n  1141:     ///\n  1142:     /// # Examples\n  1143:     ///\n  1144:     /// Calculates the length of an <code>Option<[String]></code> as an",
    "nanvix_source": "  1116:     ///\n  1117:     /// ```no_run\n  1118:     /// let x: Option<&str> = None;\n  1119:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, \"air\"); // Undefined behavior!\n  1120:     /// ```\n  1121:     #[inline]\n  1122:     #[track_caller]\n  1123:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1124:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1125:     #[rustc_const_stable(feature = \"const_option\", since = \"1.83.0\")]\n  1126:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1127:         match self {\n  1128:             Some(val) => val,\n  1129:             // SAFETY: the safety contract must be upheld by the caller.\n  1130:             None => unsafe { hint::unreachable_unchecked() },\n  1131:         }\n  1132:     }\n  1133: \n  1134:     /////////////////////////////////////////////////////////////////////////\n  1135:     // Transforming contained values\n  1136:     /////////////////////////////////////////////////////////////////////////",
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
