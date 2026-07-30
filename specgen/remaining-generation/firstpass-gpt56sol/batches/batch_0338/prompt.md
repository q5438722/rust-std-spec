For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::wrapping_byte_add",
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
        "is_unsafe": false
      },
      "name": "wrapping_byte_add",
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
    "verification_source": "  1057:         self.wrapping_offset(count as isize)\n  1058:     }\n  1059: \n  1060:     /// Adds an unsigned offset in bytes to a pointer using wrapping arithmetic.\n  1061:     ///\n  1062:     /// `count` is in units of bytes.\n  1063:     ///\n  1064:     /// This is purely a convenience for casting to a `u8` pointer and\n  1065:     /// using [wrapping_add][pointer::wrapping_add] on it. See that method for documentation.\n  1066:     ///\n  1067:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1068:     /// leaving the metadata untouched.\n  1069:     #[must_use]\n  1070:     #[inline(always)]\n  1071:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n  1072:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n  1073:     pub const fn wrapping_byte_add(self, count: usize) -> Self {\n  1074:         self.cast::<u8>().wrapping_add(count).with_metadata_of(self)\n  1075:     }\n  1076: \n  1077:     /// Subtracts an unsigned offset from a pointer using wrapping arithmetic.\n  1078:     ///\n  1079:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n  1080:     /// offset of `3 * size_of::<T>()` bytes.\n  1081:     ///\n  1082:     /// # Safety\n  1083:     ///\n  1084:     /// This operation itself is always safe, but using the resulting pointer is not.\n  1085:     ///\n  1086:     /// The resulting pointer \"remembers\" the [allocation] that `self` points to; it must not\n  1087:     /// be used to read or write other allocations.\n  1088:     ///\n  1089:     /// In other words, `let z = x.wrapping_sub((x as usize) - (y as usize))` does *not* make `z`",
    "nanvix_source": "  1045:     ///\n  1046:     /// This is purely a convenience for casting to a `u8` pointer and\n  1047:     /// using [wrapping_add][pointer::wrapping_add] on it. See that method for documentation.\n  1048:     ///\n  1049:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1050:     /// leaving the metadata untouched.\n  1051:     #[must_use]\n  1052:     #[inline(always)]\n  1053:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n  1054:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n  1055:     pub const fn wrapping_byte_add(self, count: usize) -> Self {\n  1056:         self.cast::<u8>().wrapping_add(count).with_metadata_of(self)\n  1057:     }\n  1058: \n  1059:     /// Subtracts an unsigned offset from a pointer using wrapping arithmetic.\n  1060:     ///\n  1061:     /// `count` is in units of T; e.g., a `count` of 3 represents a pointer\n  1062:     /// offset of `3 * size_of::<T>()` bytes.\n  1063:     ///\n  1064:     /// # Safety\n  1065:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::wrapping_byte_offset",
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
        "is_unsafe": false
      },
      "name": "wrapping_byte_offset",
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
    "verification_source": "   469:     }\n   470: \n   471:     /// Adds a signed offset in bytes to a pointer using wrapping arithmetic.\n   472:     ///\n   473:     /// `count` is in units of **bytes**.\n   474:     ///\n   475:     /// This is purely a convenience for casting to a `u8` pointer and\n   476:     /// using [wrapping_offset][pointer::wrapping_offset] on it. See that method\n   477:     /// for documentation.\n   478:     ///\n   479:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   480:     /// leaving the metadata untouched.\n   481:     #[must_use]\n   482:     #[inline(always)]\n   483:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   484:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   485:     pub const fn wrapping_byte_offset(self, count: isize) -> Self {\n   486:         self.cast::<u8>().wrapping_offset(count).with_metadata_of(self)\n   487:     }\n   488: \n   489:     /// Masks out bits of the pointer according to a mask.\n   490:     ///\n   491:     /// This is convenience for `ptr.map_addr(|a| a & mask)`.\n   492:     ///\n   493:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   494:     /// leaving the metadata untouched.\n   495:     ///\n   496:     /// ## Examples\n   497:     ///\n   498:     /// ```\n   499:     /// #![feature(ptr_mask)]\n   500:     /// let v = 17_u32;\n   501:     /// let ptr: *const u32 = &v;",
    "nanvix_source": "   480:     /// This is purely a convenience for casting to a `u8` pointer and\n   481:     /// using [wrapping_offset][pointer::wrapping_offset] on it. See that method\n   482:     /// for documentation.\n   483:     ///\n   484:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   485:     /// leaving the metadata untouched.\n   486:     #[must_use]\n   487:     #[inline(always)]\n   488:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n   489:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n   490:     pub const fn wrapping_byte_offset(self, count: isize) -> Self {\n   491:         self.cast::<u8>().wrapping_offset(count).with_metadata_of(self)\n   492:     }\n   493: \n   494:     /// Masks out bits of the pointer according to a mask.\n   495:     ///\n   496:     /// This is convenience for `ptr.map_addr(|a| a & mask)`.\n   497:     ///\n   498:     /// For non-`Sized` pointees this operation changes only the data pointer,\n   499:     /// leaving the metadata untouched.\n   500:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::wrapping_byte_sub",
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
        "is_unsafe": false
      },
      "name": "wrapping_byte_sub",
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
    "verification_source": "  1136:         self.wrapping_offset((count as isize).wrapping_neg())\n  1137:     }\n  1138: \n  1139:     /// Subtracts an unsigned offset in bytes from a pointer using wrapping arithmetic.\n  1140:     ///\n  1141:     /// `count` is in units of bytes.\n  1142:     ///\n  1143:     /// This is purely a convenience for casting to a `u8` pointer and\n  1144:     /// using [wrapping_sub][pointer::wrapping_sub] on it. See that method for documentation.\n  1145:     ///\n  1146:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1147:     /// leaving the metadata untouched.\n  1148:     #[must_use]\n  1149:     #[inline(always)]\n  1150:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n  1151:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n  1152:     pub const fn wrapping_byte_sub(self, count: usize) -> Self {\n  1153:         self.cast::<u8>().wrapping_sub(count).with_metadata_of(self)\n  1154:     }\n  1155: \n  1156:     /// Reads the value from `self` without moving it. This leaves the\n  1157:     /// memory in `self` unchanged.\n  1158:     ///\n  1159:     /// See [`ptr::read`] for safety concerns and examples.\n  1160:     ///\n  1161:     /// [`ptr::read`]: crate::ptr::read()\n  1162:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1163:     #[rustc_const_stable(feature = \"const_ptr_read\", since = \"1.71.0\")]\n  1164:     #[inline]\n  1165:     #[track_caller]\n  1166:     pub const unsafe fn read(self) -> T\n  1167:     where\n  1168:         T: Sized,",
    "nanvix_source": "  1124:     ///\n  1125:     /// This is purely a convenience for casting to a `u8` pointer and\n  1126:     /// using [wrapping_sub][pointer::wrapping_sub] on it. See that method for documentation.\n  1127:     ///\n  1128:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1129:     /// leaving the metadata untouched.\n  1130:     #[must_use]\n  1131:     #[inline(always)]\n  1132:     #[stable(feature = \"pointer_byte_offsets\", since = \"1.75.0\")]\n  1133:     #[rustc_const_stable(feature = \"const_pointer_byte_offsets\", since = \"1.75.0\")]\n  1134:     pub const fn wrapping_byte_sub(self, count: usize) -> Self {\n  1135:         self.cast::<u8>().wrapping_sub(count).with_metadata_of(self)\n  1136:     }\n  1137: \n  1138:     /// Reads the value from `self` without moving it. This leaves the\n  1139:     /// memory in `self` unchanged.\n  1140:     ///\n  1141:     /// See [`ptr::read`] for safety concerns and examples.\n  1142:     ///\n  1143:     /// [`ptr::read`]: crate::ptr::read()\n  1144:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::wrapping_offset",
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
        "is_unsafe": false
      },
      "name": "wrapping_offset",
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
    "verification_source": "   449:     /// let mut ptr: *mut u8 = data.as_mut_ptr();\n   450:     /// let step = 2;\n   451:     /// let end_rounded_up = ptr.wrapping_offset(6);\n   452:     ///\n   453:     /// while ptr != end_rounded_up {\n   454:     ///     unsafe {\n   455:     ///         *ptr = 0;\n   456:     ///     }\n   457:     ///     ptr = ptr.wrapping_offset(step);\n   458:     /// }\n   459:     /// assert_eq!(&data, &[0, 2, 0, 4, 0]);\n   460:     /// ```\n   461:     #[stable(feature = \"ptr_wrapping_offset\", since = \"1.16.0\")]\n   462:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   463:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   464:     #[inline(always)]\n   465:     pub const fn wrapping_offset(self, count: isize) -> *mut T\n   466:     where\n   467:         T: Sized,\n   468:     {\n   469:         // SAFETY: the `arith_offset` intrinsic has no prerequisites to be called.\n   470:         unsafe { intrinsics::arith_offset(self, count) as *mut T }\n   471:     }\n   472: \n   473:     /// Adds a signed offset in bytes to a pointer using wrapping arithmetic.\n   474:     ///\n   475:     /// `count` is in units of **bytes**.\n   476:     ///\n   477:     /// This is purely a convenience for casting to a `u8` pointer and\n   478:     /// using [wrapping_offset][pointer::wrapping_offset] on it. See that method\n   479:     /// for documentation.\n   480:     ///\n   481:     /// For non-`Sized` pointees this operation changes only the data pointer,",
    "nanvix_source": "   460:     ///         *ptr = 0;\n   461:     ///     }\n   462:     ///     ptr = ptr.wrapping_offset(step);\n   463:     /// }\n   464:     /// assert_eq!(&data, &[0, 2, 0, 4, 0]);\n   465:     /// ```\n   466:     #[stable(feature = \"ptr_wrapping_offset\", since = \"1.16.0\")]\n   467:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   468:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   469:     #[inline(always)]\n   470:     pub const fn wrapping_offset(self, count: isize) -> *mut T\n   471:     where\n   472:         T: Sized,\n   473:     {\n   474:         // SAFETY: the `arith_offset` intrinsic has no prerequisites to be called.\n   475:         unsafe { intrinsics::arith_offset(self, count) as *mut T }\n   476:     }\n   477: \n   478:     /// Adds a signed offset in bytes to a pointer using wrapping arithmetic.\n   479:     ///\n   480:     /// `count` is in units of **bytes**.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::wrapping_sub",
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
        "is_unsafe": false
      },
      "name": "wrapping_sub",
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
    "verification_source": "  1116:     /// ptr = ptr.wrapping_add(4);\n  1117:     /// let step = 2;\n  1118:     /// let mut out = String::new();\n  1119:     /// while ptr != start_rounded_down {\n  1120:     ///     unsafe {\n  1121:     ///         write!(&mut out, \"{}, \", *ptr)?;\n  1122:     ///     }\n  1123:     ///     ptr = ptr.wrapping_sub(step);\n  1124:     /// }\n  1125:     /// assert_eq!(out, \"5, 3, 1, \");\n  1126:     /// # std::fmt::Result::Ok(())\n  1127:     /// ```\n  1128:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1129:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n  1130:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n  1131:     #[inline(always)]\n  1132:     pub const fn wrapping_sub(self, count: usize) -> Self\n  1133:     where\n  1134:         T: Sized,\n  1135:     {\n  1136:         self.wrapping_offset((count as isize).wrapping_neg())\n  1137:     }\n  1138: \n  1139:     /// Subtracts an unsigned offset in bytes from a pointer using wrapping arithmetic.\n  1140:     ///\n  1141:     /// `count` is in units of bytes.\n  1142:     ///\n  1143:     /// This is purely a convenience for casting to a `u8` pointer and\n  1144:     /// using [wrapping_sub][pointer::wrapping_sub] on it. See that method for documentation.\n  1145:     ///\n  1146:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1147:     /// leaving the metadata untouched.\n  1148:     #[must_use]",
    "nanvix_source": "  1104:     ///     }\n  1105:     ///     ptr = ptr.wrapping_sub(step);\n  1106:     /// }\n  1107:     /// assert_eq!(out, \"5, 3, 1, \");\n  1108:     /// # std::fmt::Result::Ok(())\n  1109:     /// ```\n  1110:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1111:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n  1112:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n  1113:     #[inline(always)]\n  1114:     pub const fn wrapping_sub(self, count: usize) -> Self\n  1115:     where\n  1116:         T: Sized,\n  1117:     {\n  1118:         self.wrapping_offset((count as isize).wrapping_neg())\n  1119:     }\n  1120: \n  1121:     /// Subtracts an unsigned offset in bytes from a pointer using wrapping arithmetic.\n  1122:     ///\n  1123:     /// `count` is in units of bytes.\n  1124:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::write",
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
      "unit_return_variant",
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
      "name": "write",
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
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1397:         T: [const] Destruct,\n  1398:     {\n  1399:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1400:         unsafe { drop_in_place(self) }\n  1401:     }\n  1402: \n  1403:     /// Overwrites a memory location with the given value without reading or\n  1404:     /// dropping the old value.\n  1405:     ///\n  1406:     /// See [`ptr::write`] for safety concerns and examples.\n  1407:     ///\n  1408:     /// [`ptr::write`]: crate::ptr::write()\n  1409:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1410:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1411:     #[inline(always)]\n  1412:     #[track_caller]\n  1413:     pub const unsafe fn write(self, val: T)\n  1414:     where\n  1415:         T: Sized,\n  1416:     {\n  1417:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1418:         unsafe { write(self, val) }\n  1419:     }\n  1420: \n  1421:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1422:     /// bytes of memory starting at `self` to `val`.\n  1423:     ///\n  1424:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1425:     ///\n  1426:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1427:     #[doc(alias = \"memset\")]\n  1428:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1429:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]",
    "nanvix_source": "  1385:     /// Overwrites a memory location with the given value without reading or\n  1386:     /// dropping the old value.\n  1387:     ///\n  1388:     /// See [`ptr::write`] for safety concerns and examples.\n  1389:     ///\n  1390:     /// [`ptr::write`]: crate::ptr::write()\n  1391:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1392:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1393:     #[inline(always)]\n  1394:     #[track_caller]\n  1395:     pub const unsafe fn write(self, val: T)\n  1396:     where\n  1397:         T: Sized,\n  1398:     {\n  1399:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1400:         unsafe { write(self, val) }\n  1401:     }\n  1402: \n  1403:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1404:     /// bytes of memory starting at `self` to `val`.\n  1405:     ///",
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
