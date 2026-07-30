For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::offset",
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   336:     /// # Examples\n   337:     ///\n   338:     /// ```\n   339:     /// let mut s = [1, 2, 3];\n   340:     /// let ptr: *mut u32 = s.as_mut_ptr();\n   341:     ///\n   342:     /// unsafe {\n   343:     ///     assert_eq!(2, *ptr.offset(1));\n   344:     ///     assert_eq!(3, *ptr.offset(2));\n   345:     /// }\n   346:     /// ```\n   347:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   348:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   349:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   350:     #[inline(always)]\n   351:     #[track_caller]\n   352:     pub const unsafe fn offset(self, count: isize) -> *mut T\n   353:     where\n   354:         T: Sized,\n   355:     {\n   356:         #[inline]\n   357:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   358:         const fn runtime_offset_nowrap(this: *const (), count: isize, size: usize) -> bool {\n   359:             // We can use const_eval_select here because this is only for UB checks.\n   360:             const_eval_select!(\n   361:                 @capture { this: *const (), count: isize, size: usize } -> bool:\n   362:                 if const {\n   363:                     true\n   364:                 } else {\n   365:                     // `size` is the size of a Rust type, so we know that\n   366:                     // `size <= isize::MAX` and thus `as` cast here is not lossy.\n   367:                     let Some(byte_offset) = count.checked_mul(size as isize) else {\n   368:                         return false;",
    "nanvix_source": "   347:     /// unsafe {\n   348:     ///     assert_eq!(2, *ptr.offset(1));\n   349:     ///     assert_eq!(3, *ptr.offset(2));\n   350:     /// }\n   351:     /// ```\n   352:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   353:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   354:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   355:     #[inline(always)]\n   356:     #[track_caller]\n   357:     pub const unsafe fn offset(self, count: isize) -> *mut T\n   358:     where\n   359:         T: Sized,\n   360:     {\n   361:         #[inline]\n   362:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   363:         const fn runtime_offset_nowrap(this: *const (), count: isize, size: usize) -> bool {\n   364:             // We can use const_eval_select here because this is only for UB checks.\n   365:             const_eval_select!(\n   366:                 @capture { this: *const (), count: isize, size: usize } -> bool:\n   367:                 if const {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::offset_from",
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
          ],
          [
            "origin",
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
        "output": {
          "primitive": "isize"
        }
      }
    },
    "verification_source": "   777:     /// let ptr2 = Box::into_raw(Box::new(1u8));\n   778:     /// let diff = (ptr2 as isize).wrapping_sub(ptr1 as isize);\n   779:     /// // Make ptr2_other an \"alias\" of ptr2.add(1), but derived from ptr1.\n   780:     /// let ptr2_other = (ptr1 as *mut u8).wrapping_offset(diff).wrapping_offset(1);\n   781:     /// assert_eq!(ptr2 as usize, ptr2_other as usize);\n   782:     /// // Since ptr2_other and ptr2 are derived from pointers to different objects,\n   783:     /// // computing their offset is undefined behavior, even though\n   784:     /// // they point to addresses that are in-bounds of the same object!\n   785:     /// unsafe {\n   786:     ///     let one = ptr2_other.offset_from(ptr2); // Undefined Behavior! \u26a0\ufe0f\n   787:     /// }\n   788:     /// ```\n   789:     #[stable(feature = \"ptr_offset_from\", since = \"1.47.0\")]\n   790:     #[rustc_const_stable(feature = \"const_ptr_offset_from\", since = \"1.65.0\")]\n   791:     #[inline(always)]\n   792:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   793:     pub const unsafe fn offset_from(self, origin: *const T) -> isize\n   794:     where\n   795:         T: Sized,\n   796:     {\n   797:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   798:         unsafe { (self as *const T).offset_from(origin) }\n   799:     }\n   800: \n   801:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   802:     /// units of **bytes**.\n   803:     ///\n   804:     /// This is purely a convenience for casting to a `u8` pointer and\n   805:     /// using [`offset_from`][pointer::offset_from] on it. See that method for\n   806:     /// documentation and safety requirements.\n   807:     ///\n   808:     /// For non-`Sized` pointees this operation considers only the data pointers,\n   809:     /// ignoring the metadata.",
    "nanvix_source": "   788:     /// // computing their offset is undefined behavior, even though\n   789:     /// // they point to addresses that are in-bounds of the same object!\n   790:     /// unsafe {\n   791:     ///     let one = ptr2_other.offset_from(ptr2); // Undefined Behavior! \u26a0\ufe0f\n   792:     /// }\n   793:     /// ```\n   794:     #[stable(feature = \"ptr_offset_from\", since = \"1.47.0\")]\n   795:     #[rustc_const_stable(feature = \"const_ptr_offset_from\", since = \"1.65.0\")]\n   796:     #[inline(always)]\n   797:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   798:     pub const unsafe fn offset_from(self, origin: *const T) -> isize\n   799:     where\n   800:         T: Sized,\n   801:     {\n   802:         // SAFETY: the caller must uphold the safety contract for `offset_from`.\n   803:         unsafe { (self as *const T).offset_from(origin) }\n   804:     }\n   805: \n   806:     /// Calculates the distance between two pointers within the same allocation. The returned value is in\n   807:     /// units of **bytes**.\n   808:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::offset_from_unsigned",
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
                  "generic": "T"
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
    "verification_source": "   685:     /// let ptr1: *const i32 = &a[1];\n   686:     /// let ptr2: *const i32 = &a[3];\n   687:     /// unsafe {\n   688:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr1), 2);\n   689:     ///     assert_eq!(ptr1.add(2), ptr2);\n   690:     ///     assert_eq!(ptr2.sub(2), ptr1);\n   691:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr2), 0);\n   692:     /// }\n   693:     ///\n   694:     /// // This would be incorrect, as the pointers are not correctly ordered:\n   695:     /// // ptr1.offset_from_unsigned(ptr2)\n   696:     /// ```\n   697:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   698:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   699:     #[inline]\n   700:     #[track_caller]\n   701:     pub const unsafe fn offset_from_unsigned(self, origin: *const T) -> usize\n   702:     where\n   703:         T: Sized,\n   704:     {\n   705:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   706:         const fn runtime_ptr_ge(this: *const (), origin: *const ()) -> bool {\n   707:             const_eval_select!(\n   708:                 @capture { this: *const (), origin: *const () } -> bool:\n   709:                 if const {\n   710:                     true\n   711:                 } else {\n   712:                     this >= origin\n   713:                 }\n   714:             )\n   715:         }\n   716: \n   717:         ub_checks::assert_unsafe_precondition!(",
    "nanvix_source": "   696:     ///     assert_eq!(ptr2.offset_from_unsigned(ptr2), 0);\n   697:     /// }\n   698:     ///\n   699:     /// // This would be incorrect, as the pointers are not correctly ordered:\n   700:     /// // ptr1.offset_from_unsigned(ptr2)\n   701:     /// ```\n   702:     #[stable(feature = \"ptr_sub_ptr\", since = \"1.87.0\")]\n   703:     #[rustc_const_stable(feature = \"const_ptr_sub_ptr\", since = \"1.87.0\")]\n   704:     #[inline]\n   705:     #[track_caller]\n   706:     pub const unsafe fn offset_from_unsigned(self, origin: *const T) -> usize\n   707:     where\n   708:         T: Sized,\n   709:     {\n   710:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   711:         const fn runtime_ptr_ge(this: *const (), origin: *const ()) -> bool {\n   712:             const_eval_select!(\n   713:                 @capture { this: *const (), origin: *const () } -> bool:\n   714:                 if const {\n   715:                     true\n   716:                 } else {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::read",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1150:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n  1151:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n  1152:     pub const fn wrapping_byte_sub(self, count: usize) -> Self {\n  1153:         self.cast::<u8>().wrapping_sub(count).with_metadata_of(self)\n  1154:     }\n  1155: \n  1156:     /// Reads the value from `self` without moving it. This leaves the\n  1157:     /// memory in `self` unchanged.\n  1158:     ///\n  1159:     /// See [`ptr::read`] for safety concerns and examples.\n  1160:     ///\n  1161:     /// [`ptr::read`]: crate::ptr::read()\n  1162:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1163:     #[rustc_const_stable(feature = \"const_ptr_read\", since = \"1.71.0\")]\n  1164:     #[inline]\n  1165:     #[track_caller]\n  1166:     pub const unsafe fn read(self) -> T\n  1167:     where\n  1168:         T: Sized,\n  1169:     {\n  1170:         // SAFETY: the caller must uphold the safety contract for `read`.\n  1171:         unsafe { read(self) }\n  1172:     }\n  1173: \n  1174:     /// Performs a volatile read of the value from `self` without moving it. This\n  1175:     /// leaves the memory in `self` unchanged.\n  1176:     ///\n  1177:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1178:     /// to not be elided or reordered by the compiler across other volatile\n  1179:     /// operations.\n  1180:     ///\n  1181:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n  1182:     ///",
    "nanvix_source": "  1138:     /// Reads the value from `self` without moving it. This leaves the\n  1139:     /// memory in `self` unchanged.\n  1140:     ///\n  1141:     /// See [`ptr::read`] for safety concerns and examples.\n  1142:     ///\n  1143:     /// [`ptr::read`]: crate::ptr::read()\n  1144:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1145:     #[rustc_const_stable(feature = \"const_ptr_read\", since = \"1.71.0\")]\n  1146:     #[inline]\n  1147:     #[track_caller]\n  1148:     pub const unsafe fn read(self) -> T\n  1149:     where\n  1150:         T: Sized,\n  1151:     {\n  1152:         // SAFETY: the caller must uphold the safety contract for `read`.\n  1153:         unsafe { read(self) }\n  1154:     }\n  1155: \n  1156:     /// Performs a volatile read of the value from `self` without moving it. This\n  1157:     /// leaves the memory in `self` unchanged.\n  1158:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::read_unaligned",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1191:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n  1192:         unsafe { read_volatile(self) }\n  1193:     }\n  1194: \n  1195:     /// Reads the value from `self` without moving it. This leaves the\n  1196:     /// memory in `self` unchanged.\n  1197:     ///\n  1198:     /// Unlike `read`, the pointer may be unaligned.\n  1199:     ///\n  1200:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n  1201:     ///\n  1202:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n  1203:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1204:     #[rustc_const_stable(feature = \"const_ptr_read\", since = \"1.71.0\")]\n  1205:     #[inline]\n  1206:     #[track_caller]\n  1207:     pub const unsafe fn read_unaligned(self) -> T\n  1208:     where\n  1209:         T: Sized,\n  1210:     {\n  1211:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n  1212:         unsafe { read_unaligned(self) }\n  1213:     }\n  1214: \n  1215:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1216:     /// and destination may overlap.\n  1217:     ///\n  1218:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n  1219:     ///\n  1220:     /// See [`ptr::copy`] for safety concerns and examples.\n  1221:     ///\n  1222:     /// [`ptr::copy`]: crate::ptr::copy()\n  1223:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]",
    "nanvix_source": "  1179:     ///\n  1180:     /// Unlike `read`, the pointer may be unaligned.\n  1181:     ///\n  1182:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n  1183:     ///\n  1184:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n  1185:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1186:     #[rustc_const_stable(feature = \"const_ptr_read\", since = \"1.71.0\")]\n  1187:     #[inline]\n  1188:     #[track_caller]\n  1189:     pub const unsafe fn read_unaligned(self) -> T\n  1190:     where\n  1191:         T: Sized,\n  1192:     {\n  1193:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n  1194:         unsafe { read_unaligned(self) }\n  1195:     }\n  1196: \n  1197:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1198:     /// and destination may overlap.\n  1199:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::read_volatile",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1171:         unsafe { read(self) }\n  1172:     }\n  1173: \n  1174:     /// Performs a volatile read of the value from `self` without moving it. This\n  1175:     /// leaves the memory in `self` unchanged.\n  1176:     ///\n  1177:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1178:     /// to not be elided or reordered by the compiler across other volatile\n  1179:     /// operations.\n  1180:     ///\n  1181:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n  1182:     ///\n  1183:     /// [`ptr::read_volatile`]: crate::ptr::read_volatile()\n  1184:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1185:     #[inline]\n  1186:     #[track_caller]\n  1187:     pub unsafe fn read_volatile(self) -> T\n  1188:     where\n  1189:         T: Sized,\n  1190:     {\n  1191:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n  1192:         unsafe { read_volatile(self) }\n  1193:     }\n  1194: \n  1195:     /// Reads the value from `self` without moving it. This leaves the\n  1196:     /// memory in `self` unchanged.\n  1197:     ///\n  1198:     /// Unlike `read`, the pointer may be unaligned.\n  1199:     ///\n  1200:     /// See [`ptr::read_unaligned`] for safety concerns and examples.\n  1201:     ///\n  1202:     /// [`ptr::read_unaligned`]: crate::ptr::read_unaligned()\n  1203:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]",
    "nanvix_source": "  1159:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1160:     /// to not be elided or reordered by the compiler across other volatile\n  1161:     /// operations.\n  1162:     ///\n  1163:     /// See [`ptr::read_volatile`] for safety concerns and examples.\n  1164:     ///\n  1165:     /// [`ptr::read_volatile`]: crate::ptr::read_volatile()\n  1166:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1167:     #[inline]\n  1168:     #[track_caller]\n  1169:     pub unsafe fn read_volatile(self) -> T\n  1170:     where\n  1171:         T: Sized,\n  1172:     {\n  1173:         // SAFETY: the caller must uphold the safety contract for `read_volatile`.\n  1174:         unsafe { read_volatile(self) }\n  1175:     }\n  1176: \n  1177:     /// Reads the value from `self` without moving it. This leaves the\n  1178:     /// memory in `self` unchanged.\n  1179:     ///",
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
