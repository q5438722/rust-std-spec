For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::replace",
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
      "name": "replace",
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
            "src",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1474:     where\n  1475:         T: Sized,\n  1476:     {\n  1477:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1478:         unsafe { write_unaligned(self, val) }\n  1479:     }\n  1480: \n  1481:     /// Replaces the value at `self` with `src`, returning the old\n  1482:     /// value, without dropping either.\n  1483:     ///\n  1484:     /// See [`ptr::replace`] for safety concerns and examples.\n  1485:     ///\n  1486:     /// [`ptr::replace`]: crate::ptr::replace()\n  1487:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1488:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]\n  1489:     #[inline(always)]\n  1490:     pub const unsafe fn replace(self, src: T) -> T\n  1491:     where\n  1492:         T: Sized,\n  1493:     {\n  1494:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1495:         unsafe { replace(self, src) }\n  1496:     }\n  1497: \n  1498:     /// Swaps the values at two mutable locations of the same type, without\n  1499:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1500:     /// otherwise equivalent.\n  1501:     ///\n  1502:     /// See [`ptr::swap`] for safety concerns and examples.\n  1503:     ///\n  1504:     /// [`ptr::swap`]: crate::ptr::swap()\n  1505:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1506:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]",
    "nanvix_source": "  1462: \n  1463:     /// Replaces the value at `self` with `src`, returning the old\n  1464:     /// value, without dropping either.\n  1465:     ///\n  1466:     /// See [`ptr::replace`] for safety concerns and examples.\n  1467:     ///\n  1468:     /// [`ptr::replace`]: crate::ptr::replace()\n  1469:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1470:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]\n  1471:     #[inline(always)]\n  1472:     pub const unsafe fn replace(self, src: T) -> T\n  1473:     where\n  1474:         T: Sized,\n  1475:     {\n  1476:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1477:         unsafe { replace(self, src) }\n  1478:     }\n  1479: \n  1480:     /// Swaps the values at two mutable locations of the same type, without\n  1481:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1482:     /// otherwise equivalent.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::slice_from_raw_parts",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "slice_from_raw_parts",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "data",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "len",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1163: /// ```\n  1164: ///\n  1165: /// You must ensure that the pointer is valid and not null before dereferencing\n  1166: /// the raw slice. A slice reference must never have a null pointer, even if it's empty.\n  1167: ///\n  1168: /// ```rust,should_panic\n  1169: /// use std::ptr;\n  1170: /// let danger: *const [u8] = ptr::slice_from_raw_parts(ptr::null(), 0);\n  1171: /// unsafe {\n  1172: ///     danger.as_ref().expect(\"references must not be null\");\n  1173: /// }\n  1174: /// ```\n  1175: #[inline]\n  1176: #[stable(feature = \"slice_from_raw_parts\", since = \"1.42.0\")]\n  1177: #[rustc_const_stable(feature = \"const_slice_from_raw_parts\", since = \"1.64.0\")]\n  1178: #[rustc_diagnostic_item = \"ptr_slice_from_raw_parts\"]\n  1179: pub const fn slice_from_raw_parts<T>(data: *const T, len: usize) -> *const [T] {\n  1180:     from_raw_parts(data, len)\n  1181: }\n  1182: \n  1183: /// Forms a raw mutable slice from a pointer and a length.\n  1184: ///\n  1185: /// The `len` argument is the number of **elements**, not the number of bytes.\n  1186: ///\n  1187: /// Performs the same functionality as [`slice_from_raw_parts`], except that a\n  1188: /// raw mutable slice is returned, as opposed to a raw immutable slice.\n  1189: ///\n  1190: /// This function is safe, but actually using the return value is unsafe.\n  1191: /// See the documentation of [`slice::from_raw_parts_mut`] for slice safety requirements.\n  1192: ///\n  1193: /// [`slice::from_raw_parts_mut`]: crate::slice::from_raw_parts_mut\n  1194: ///\n  1195: /// # Examples",
    "nanvix_source": "  1179: /// use std::ptr;\n  1180: /// let danger: *const [u8] = ptr::slice_from_raw_parts(ptr::null(), 0);\n  1181: /// unsafe {\n  1182: ///     danger.as_ref().expect(\"references must not be null\");\n  1183: /// }\n  1184: /// ```\n  1185: #[inline]\n  1186: #[stable(feature = \"slice_from_raw_parts\", since = \"1.42.0\")]\n  1187: #[rustc_const_stable(feature = \"const_slice_from_raw_parts\", since = \"1.64.0\")]\n  1188: #[rustc_diagnostic_item = \"ptr_slice_from_raw_parts\"]\n  1189: pub const fn slice_from_raw_parts<T>(data: *const T, len: usize) -> *const [T] {\n  1190:     from_raw_parts(data, len)\n  1191: }\n  1192: \n  1193: /// Forms a raw mutable slice from a pointer and a length.\n  1194: ///\n  1195: /// The `len` argument is the number of **elements**, not the number of bytes.\n  1196: ///\n  1197: /// Performs the same functionality as [`slice_from_raw_parts`], except that a\n  1198: /// raw mutable slice is returned, as opposed to a raw immutable slice.\n  1199: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::slice_from_raw_parts_mut",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "slice_from_raw_parts_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "data",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "len",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1209: /// ```\n  1210: ///\n  1211: /// You must ensure that the pointer is valid and not null before dereferencing\n  1212: /// the raw slice. A slice reference must never have a null pointer, even if it's empty.\n  1213: ///\n  1214: /// ```rust,should_panic\n  1215: /// use std::ptr;\n  1216: /// let danger: *mut [u8] = ptr::slice_from_raw_parts_mut(ptr::null_mut(), 0);\n  1217: /// unsafe {\n  1218: ///     danger.as_mut().expect(\"references must not be null\");\n  1219: /// }\n  1220: /// ```\n  1221: #[inline]\n  1222: #[stable(feature = \"slice_from_raw_parts\", since = \"1.42.0\")]\n  1223: #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n  1224: #[rustc_diagnostic_item = \"ptr_slice_from_raw_parts_mut\"]\n  1225: pub const fn slice_from_raw_parts_mut<T>(data: *mut T, len: usize) -> *mut [T] {\n  1226:     from_raw_parts_mut(data, len)\n  1227: }\n  1228: \n  1229: /// Swaps the values at two mutable locations of the same type, without\n  1230: /// deinitializing either.\n  1231: ///\n  1232: /// But for the following exceptions, this function is semantically\n  1233: /// equivalent to [`mem::swap`]:\n  1234: ///\n  1235: /// * It operates on raw pointers instead of references. When references are\n  1236: ///   available, [`mem::swap`] should be preferred.\n  1237: ///\n  1238: /// * The two pointed-to values may overlap. If the values do overlap, then the\n  1239: ///   overlapping region of memory from `x` will be used. This is demonstrated\n  1240: ///   in the second example below.\n  1241: ///",
    "nanvix_source": "  1225: /// use std::ptr;\n  1226: /// let danger: *mut [u8] = ptr::slice_from_raw_parts_mut(ptr::null_mut(), 0);\n  1227: /// unsafe {\n  1228: ///     danger.as_mut().expect(\"references must not be null\");\n  1229: /// }\n  1230: /// ```\n  1231: #[inline]\n  1232: #[stable(feature = \"slice_from_raw_parts\", since = \"1.42.0\")]\n  1233: #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n  1234: #[rustc_diagnostic_item = \"ptr_slice_from_raw_parts_mut\"]\n  1235: pub const fn slice_from_raw_parts_mut<T>(data: *mut T, len: usize) -> *mut [T] {\n  1236:     from_raw_parts_mut(data, len)\n  1237: }\n  1238: \n  1239: /// Swaps the values at two mutable locations of the same type, without\n  1240: /// deinitializing either.\n  1241: ///\n  1242: /// But for the following exceptions, this function is semantically\n  1243: /// equivalent to [`mem::swap`]:\n  1244: ///\n  1245: /// * It operates on raw pointers instead of references. When references are",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::sub",
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
      "name": "sub",
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
    "verification_source": "   919:     /// # Examples\n   920:     ///\n   921:     /// ```\n   922:     /// let s: &str = \"123\";\n   923:     ///\n   924:     /// unsafe {\n   925:     ///     let end: *const u8 = s.as_ptr().add(3);\n   926:     ///     assert_eq!(*end.sub(1), b'3');\n   927:     ///     assert_eq!(*end.sub(2), b'2');\n   928:     /// }\n   929:     /// ```\n   930:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n   931:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   932:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   933:     #[inline(always)]\n   934:     #[track_caller]\n   935:     pub const unsafe fn sub(self, count: usize) -> Self\n   936:     where\n   937:         T: Sized,\n   938:     {\n   939:         #[cfg(debug_assertions)]\n   940:         #[inline]\n   941:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   942:         const fn runtime_sub_nowrap(this: *const (), count: usize, size: usize) -> bool {\n   943:             const_eval_select!(\n   944:                 @capture { this: *const (), count: usize, size: usize } -> bool:\n   945:                 if const {\n   946:                     true\n   947:                 } else {\n   948:                     let Some(byte_offset) = count.checked_mul(size) else {\n   949:                         return false;\n   950:                     };\n   951:                     byte_offset <= (isize::MAX as usize) && this.addr() >= byte_offset",
    "nanvix_source": "   907:     ///     let end: *const u8 = s.as_ptr().add(3);\n   908:     ///     assert_eq!(*end.sub(1), b'3');\n   909:     ///     assert_eq!(*end.sub(2), b'2');\n   910:     /// }\n   911:     /// ```\n   912:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n   913:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   914:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   915:     #[inline(always)]\n   916:     #[track_caller]\n   917:     pub const unsafe fn sub(self, count: usize) -> Self\n   918:     where\n   919:         T: Sized,\n   920:     {\n   921:         #[cfg(debug_assertions)]\n   922:         #[inline]\n   923:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   924:         const fn runtime_sub_nowrap(this: *const (), count: usize, size: usize) -> bool {\n   925:             const_eval_select!(\n   926:                 @capture { this: *const (), count: usize, size: usize } -> bool:\n   927:                 if const {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::swap",
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
      "name": "swap",
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
            "with",
            {
              "raw_pointer": {
                "is_mutable": true,
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
    "verification_source": "  1492:         T: Sized,\n  1493:     {\n  1494:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1495:         unsafe { replace(self, src) }\n  1496:     }\n  1497: \n  1498:     /// Swaps the values at two mutable locations of the same type, without\n  1499:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1500:     /// otherwise equivalent.\n  1501:     ///\n  1502:     /// See [`ptr::swap`] for safety concerns and examples.\n  1503:     ///\n  1504:     /// [`ptr::swap`]: crate::ptr::swap()\n  1505:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1506:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n  1507:     #[inline(always)]\n  1508:     pub const unsafe fn swap(self, with: *mut T)\n  1509:     where\n  1510:         T: Sized,\n  1511:     {\n  1512:         // SAFETY: the caller must uphold the safety contract for `swap`.\n  1513:         unsafe { swap(self, with) }\n  1514:     }\n  1515: \n  1516:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1517:     /// `align`.\n  1518:     ///\n  1519:     /// If it is not possible to align the pointer, the implementation returns\n  1520:     /// `usize::MAX`.\n  1521:     ///\n  1522:     /// The offset is expressed in number of `T` elements, and not bytes. The value returned can be\n  1523:     /// used with the `wrapping_add` method.\n  1524:     ///",
    "nanvix_source": "  1480:     /// Swaps the values at two mutable locations of the same type, without\n  1481:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1482:     /// otherwise equivalent.\n  1483:     ///\n  1484:     /// See [`ptr::swap`] for safety concerns and examples.\n  1485:     ///\n  1486:     /// [`ptr::swap`]: crate::ptr::swap()\n  1487:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1488:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n  1489:     #[inline(always)]\n  1490:     pub const unsafe fn swap(self, with: *mut T)\n  1491:     where\n  1492:         T: Sized,\n  1493:     {\n  1494:         // SAFETY: the caller must uphold the safety contract for `swap`.\n  1495:         unsafe { swap(self, with) }\n  1496:     }\n  1497: \n  1498:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1499:     /// `align`.\n  1500:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::swap_nonoverlapping",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
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
      "name": "swap_nonoverlapping",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "x",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "y",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
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
    "verification_source": "  1352: /// let mut x = [1, 2, 3, 4];\n  1353: /// let mut y = [7, 8, 9];\n  1354: ///\n  1355: /// unsafe {\n  1356: ///     ptr::swap_nonoverlapping(x.as_mut_ptr(), y.as_mut_ptr(), 2);\n  1357: /// }\n  1358: ///\n  1359: /// assert_eq!(x, [7, 8, 3, 4]);\n  1360: /// assert_eq!(y, [1, 2, 9]);\n  1361: /// ```\n  1362: #[inline]\n  1363: #[stable(feature = \"swap_nonoverlapping\", since = \"1.27.0\")]\n  1364: #[rustc_const_stable(feature = \"const_swap_nonoverlapping\", since = \"1.88.0\")]\n  1365: #[rustc_diagnostic_item = \"ptr_swap_nonoverlapping\"]\n  1366: #[rustc_allow_const_fn_unstable(const_eval_select)] // both implementations behave the same\n  1367: #[track_caller]\n  1368: pub const unsafe fn swap_nonoverlapping<T>(x: *mut T, y: *mut T, count: usize) {\n  1369:     ub_checks::assert_unsafe_precondition!(\n  1370:         check_library_ub,\n  1371:         \"ptr::swap_nonoverlapping requires that both pointer arguments are aligned and non-null \\\n  1372:         and the specified memory ranges do not overlap\",\n  1373:         (\n  1374:             x: *mut () = x as *mut (),\n  1375:             y: *mut () = y as *mut (),\n  1376:             size: usize = size_of::<T>(),\n  1377:             align: usize = align_of::<T>(),\n  1378:             count: usize = count,\n  1379:         ) => {\n  1380:             let zero_size = size == 0 || count == 0;\n  1381:             ub_checks::maybe_is_aligned_and_not_null(x, align, zero_size)\n  1382:                 && ub_checks::maybe_is_aligned_and_not_null(y, align, zero_size)\n  1383:                 && ub_checks::maybe_is_nonoverlapping(x, y, size, count)\n  1384:         }",
    "nanvix_source": "  1368: ///\n  1369: /// assert_eq!(x, [7, 8, 3, 4]);\n  1370: /// assert_eq!(y, [1, 2, 9]);\n  1371: /// ```\n  1372: #[inline]\n  1373: #[stable(feature = \"swap_nonoverlapping\", since = \"1.27.0\")]\n  1374: #[rustc_const_stable(feature = \"const_swap_nonoverlapping\", since = \"1.88.0\")]\n  1375: #[rustc_diagnostic_item = \"ptr_swap_nonoverlapping\"]\n  1376: #[rustc_allow_const_fn_unstable(const_eval_select)] // both implementations behave the same\n  1377: #[track_caller]\n  1378: pub const unsafe fn swap_nonoverlapping<T>(x: *mut T, y: *mut T, count: usize) {\n  1379:     ub_checks::assert_unsafe_precondition!(\n  1380:         check_library_ub,\n  1381:         \"ptr::swap_nonoverlapping requires that both pointer arguments are aligned and non-null \\\n  1382:         and the specified memory ranges do not overlap\",\n  1383:         (\n  1384:             x: *mut () = x as *mut (),\n  1385:             y: *mut () = y as *mut (),\n  1386:             size: usize = size_of::<T>(),\n  1387:             align: usize = align_of::<T>(),\n  1388:             count: usize = count,",
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
