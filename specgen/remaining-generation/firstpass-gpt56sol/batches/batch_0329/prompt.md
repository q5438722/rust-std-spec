For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::write_volatile",
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "write_volatile",
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
    "verification_source": "  1164:         unsafe { ptr::write_bytes(self.as_ptr(), val, count) }\n  1165:     }\n  1166: \n  1167:     /// Performs a volatile write of a memory location with the given value without\n  1168:     /// reading or dropping the old value.\n  1169:     ///\n  1170:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1171:     /// to not be elided or reordered by the compiler across other volatile\n  1172:     /// operations.\n  1173:     ///\n  1174:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1175:     ///\n  1176:     /// [`ptr::write_volatile`]: crate::ptr::write_volatile()\n  1177:     #[inline(always)]\n  1178:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1179:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1180:     pub unsafe fn write_volatile(self, val: T)\n  1181:     where\n  1182:         T: Sized,\n  1183:     {\n  1184:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1185:         unsafe { ptr::write_volatile(self.as_ptr(), val) }\n  1186:     }\n  1187: \n  1188:     /// Overwrites a memory location with the given value without reading or\n  1189:     /// dropping the old value.\n  1190:     ///\n  1191:     /// Unlike `write`, the pointer may be unaligned.\n  1192:     ///\n  1193:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1194:     ///\n  1195:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1196:     #[inline(always)]",
    "nanvix_source": "  1103:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1104:     /// to not be elided or reordered by the compiler across other volatile\n  1105:     /// operations.\n  1106:     ///\n  1107:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1108:     ///\n  1109:     /// [`ptr::write_volatile`]: crate::ptr::write_volatile()\n  1110:     #[inline(always)]\n  1111:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1112:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1113:     pub unsafe fn write_volatile(self, val: T)\n  1114:     where\n  1115:         T: Sized,\n  1116:     {\n  1117:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1118:         unsafe { ptr::write_volatile(self.as_ptr(), val) }\n  1119:     }\n  1120: \n  1121:     /// Overwrites a memory location with the given value without reading or\n  1122:     /// dropping the old value.\n  1123:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::add",
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
      "name": "add",
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
    "verification_source": "   813:     /// # Examples\n   814:     ///\n   815:     /// ```\n   816:     /// let s: &str = \"123\";\n   817:     /// let ptr: *const u8 = s.as_ptr();\n   818:     ///\n   819:     /// unsafe {\n   820:     ///     assert_eq!(*ptr.add(1), b'2');\n   821:     ///     assert_eq!(*ptr.add(2), b'3');\n   822:     /// }\n   823:     /// ```\n   824:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n   825:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   826:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   827:     #[inline(always)]\n   828:     #[track_caller]\n   829:     pub const unsafe fn add(self, count: usize) -> Self\n   830:     where\n   831:         T: Sized,\n   832:     {\n   833:         #[cfg(debug_assertions)]\n   834:         #[inline]\n   835:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   836:         const fn runtime_add_nowrap(this: *const (), count: usize, size: usize) -> bool {\n   837:             const_eval_select!(\n   838:                 @capture { this: *const (), count: usize, size: usize } -> bool:\n   839:                 if const {\n   840:                     true\n   841:                 } else {\n   842:                     let Some(byte_offset) = count.checked_mul(size) else {\n   843:                         return false;\n   844:                     };\n   845:                     let (_, overflow) = this.addr().overflowing_add(byte_offset);",
    "nanvix_source": "   828:     /// unsafe {\n   829:     ///     assert_eq!(*ptr.add(1), b'2');\n   830:     ///     assert_eq!(*ptr.add(2), b'3');\n   831:     /// }\n   832:     /// ```\n   833:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n   834:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   835:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n   836:     #[inline(always)]\n   837:     #[track_caller]\n   838:     pub const unsafe fn add(self, count: usize) -> Self\n   839:     where\n   840:         T: Sized,\n   841:     {\n   842:         #[cfg(debug_assertions)]\n   843:         #[inline]\n   844:         #[rustc_allow_const_fn_unstable(const_eval_select)]\n   845:         const fn runtime_add_nowrap(this: *const (), count: usize, size: usize) -> bool {\n   846:             const_eval_select!(\n   847:                 @capture { this: *const (), count: usize, size: usize } -> bool:\n   848:                 if const {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::addr",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "addr",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   128:     ///\n   129:     /// [`cast_mut`]: pointer::cast_mut\n   130:     #[stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   131:     #[rustc_const_stable(feature = \"ptr_const_cast\", since = \"1.65.0\")]\n   132:     #[rustc_diagnostic_item = \"ptr_cast_const\"]\n   133:     #[inline(always)]\n   134:     pub const fn cast_const(self) -> *const T {\n   135:         self as _\n   136:     }\n   137: \n   138:     #[doc = include_str!(\"./docs/addr.md\")]\n   139:     ///\n   140:     /// [without_provenance]: without_provenance_mut\n   141:     #[must_use]\n   142:     #[inline(always)]\n   143:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   144:     pub fn addr(self) -> usize {\n   145:         // A pointer-to-integer transmute currently has exactly the right semantics: it returns the\n   146:         // address without exposing the provenance. Note that this is *not* a stable guarantee about\n   147:         // transmute semantics, it relies on sysroot crates having special status.\n   148:         // SAFETY: Pointer-to-integer transmutes are valid (if you are okay with losing the\n   149:         // provenance).\n   150:         unsafe { mem::transmute(self.cast::<()>()) }\n   151:     }\n   152: \n   153:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   154:     /// [`with_exposed_provenance_mut`] and returns the \"address\" portion.\n   155:     ///\n   156:     /// This is equivalent to `self as usize`, which semantically discards provenance information.\n   157:     /// Furthermore, this (like the `as` cast) has the implicit side-effect of marking the\n   158:     /// provenance as 'exposed', so on platforms that support it you can later call\n   159:     /// [`with_exposed_provenance_mut`] to reconstitute the original pointer including its provenance.\n   160:     ///",
    "nanvix_source": "   134:     pub const fn cast_const(self) -> *const T {\n   135:         self as _\n   136:     }\n   137: \n   138:     #[doc = include_str!(\"./docs/addr.md\")]\n   139:     ///\n   140:     /// [without_provenance]: without_provenance_mut\n   141:     #[must_use]\n   142:     #[inline(always)]\n   143:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   144:     pub fn addr(self) -> usize {\n   145:         // A pointer-to-integer transmute currently has exactly the right semantics: it returns the\n   146:         // address without exposing the provenance. Note that this is *not* a stable guarantee about\n   147:         // transmute semantics, it relies on sysroot crates having special status.\n   148:         // SAFETY: Pointer-to-integer transmutes are valid (if you are okay with losing the\n   149:         // provenance).\n   150:         unsafe { mem::transmute(self.cast::<()>()) }\n   151:     }\n   152: \n   153:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   154:     /// [`with_exposed_provenance_mut`] and returns the \"address\" portion.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::addr_eq",
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
            "name": "U"
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
      "name": "addr_eq",
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
            "p",
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
            "q",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "U"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2431: /// then this is the same as [`eq`].\n  2432: ///\n  2433: /// # Examples\n  2434: ///\n  2435: /// ```\n  2436: /// use std::ptr;\n  2437: ///\n  2438: /// let whole: &[i32; 3] = &[1, 2, 3];\n  2439: /// let first: &i32 = &whole[0];\n  2440: ///\n  2441: /// assert!(ptr::addr_eq(whole, first));\n  2442: /// assert!(!ptr::eq::<dyn std::fmt::Debug>(whole, first));\n  2443: /// ```\n  2444: #[stable(feature = \"ptr_addr_eq\", since = \"1.76.0\")]\n  2445: #[inline(always)]\n  2446: #[must_use = \"pointer comparison produces a value\"]\n  2447: pub fn addr_eq<T: PointeeSized, U: PointeeSized>(p: *const T, q: *const U) -> bool {\n  2448:     (p as *const ()) == (q as *const ())\n  2449: }\n  2450: \n  2451: /// Compares the *addresses* of the two function pointers for equality.\n  2452: ///\n  2453: /// This is the same as `f == g`, but using this function makes clear that the potentially\n  2454: /// surprising semantics of function pointer comparison are involved.\n  2455: ///\n  2456: /// There are **very few guarantees** about how functions are compiled and they have no intrinsic\n  2457: /// \u201cidentity\u201d; in particular, this comparison:\n  2458: ///\n  2459: /// * May return `true` unexpectedly, in cases where functions are equivalent.\n  2460: ///\n  2461: ///   For example, the following program is likely (but not guaranteed) to print `(true, true)`\n  2462: ///   when compiled with optimization:\n  2463: ///",
    "nanvix_source": "  2489: ///\n  2490: /// let whole: &[i32; 3] = &[1, 2, 3];\n  2491: /// let first: &i32 = &whole[0];\n  2492: ///\n  2493: /// assert!(ptr::addr_eq(whole, first));\n  2494: /// assert!(!ptr::eq::<dyn std::fmt::Debug>(whole, first));\n  2495: /// ```\n  2496: #[stable(feature = \"ptr_addr_eq\", since = \"1.76.0\")]\n  2497: #[inline(always)]\n  2498: #[must_use = \"pointer comparison produces a value\"]\n  2499: pub fn addr_eq<T: PointeeSized, U: PointeeSized>(p: *const T, q: *const U) -> bool {\n  2500:     (p as *const ()) == (q as *const ())\n  2501: }\n  2502: \n  2503: /// Compares the *addresses* of the two function pointers for equality.\n  2504: ///\n  2505: /// This is the same as `f == g`, but using this function makes clear that the potentially\n  2506: /// surprising semantics of function pointer comparison are involved.\n  2507: ///\n  2508: /// There are **very few guarantees** about how functions are compiled and they have no intrinsic\n  2509: /// \u201cidentity\u201d; in particular, this comparison:",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::align_offset",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "align_offset",
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
            "align",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1278:     /// let x = [5_u8, 6, 7, 8, 9];\n  1279:     /// let ptr = x.as_ptr();\n  1280:     /// let offset = ptr.align_offset(align_of::<u16>());\n  1281:     ///\n  1282:     /// if offset < x.len() - 1 {\n  1283:     ///     let u16_ptr = ptr.add(offset).cast::<u16>();\n  1284:     ///     assert!(*u16_ptr == u16::from_ne_bytes([5, 6]) || *u16_ptr == u16::from_ne_bytes([6, 7]));\n  1285:     /// } else {\n  1286:     ///     // while the pointer can be aligned via `offset`, it would point\n  1287:     ///     // outside the allocation\n  1288:     /// }\n  1289:     /// # }\n  1290:     /// ```\n  1291:     #[must_use]\n  1292:     #[inline]\n  1293:     #[stable(feature = \"align_offset\", since = \"1.36.0\")]\n  1294:     pub fn align_offset(self, align: usize) -> usize\n  1295:     where\n  1296:         T: Sized,\n  1297:     {\n  1298:         if !align.is_power_of_two() {\n  1299:             panic!(\"align_offset: align is not a power-of-two\");\n  1300:         }\n  1301: \n  1302:         // SAFETY: `align` has been checked to be a power of 2 above\n  1303:         let ret = unsafe { align_offset(self, align) };\n  1304: \n  1305:         // Inform Miri that we want to consider the resulting pointer to be suitably aligned.\n  1306:         #[cfg(miri)]\n  1307:         if ret != usize::MAX {\n  1308:             intrinsics::miri_promise_symbolic_alignment(self.wrapping_add(ret).cast(), align);\n  1309:         }\n  1310: ",
    "nanvix_source": "  1266:     ///     assert!(*u16_ptr == u16::from_ne_bytes([5, 6]) || *u16_ptr == u16::from_ne_bytes([6, 7]));\n  1267:     /// } else {\n  1268:     ///     // while the pointer can be aligned via `offset`, it would point\n  1269:     ///     // outside the allocation\n  1270:     /// }\n  1271:     /// # }\n  1272:     /// ```\n  1273:     #[must_use]\n  1274:     #[inline]\n  1275:     #[stable(feature = \"align_offset\", since = \"1.36.0\")]\n  1276:     pub fn align_offset(self, align: usize) -> usize\n  1277:     where\n  1278:         T: Sized,\n  1279:     {\n  1280:         if !align.is_power_of_two() {\n  1281:             panic!(\"align_offset: align is not a power-of-two\");\n  1282:         }\n  1283: \n  1284:         // SAFETY: `align` has been checked to be a power of 2 above\n  1285:         let ret = unsafe { align_offset(self, align) };\n  1286: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::as_array",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
      "name": "as_array",
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
            "is_mutable": false,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
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
        "impl_id": "core:51649",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "raw_pointer": {
                        "is_mutable": false,
                        "type": {
                          "array": {
                            "len": "N",
                            "type": {
                              "generic": "T"
                            }
                          }
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
    "verification_source": "  1490:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1491:     /// assert_eq!(slice.as_ptr(), ptr::null());\n  1492:     /// ```\n  1493:     #[inline]\n  1494:     #[unstable(feature = \"slice_ptr_get\", issue = \"74265\")]\n  1495:     pub const fn as_ptr(self) -> *const T {\n  1496:         self as *const T\n  1497:     }\n  1498: \n  1499:     /// Gets a raw pointer to the underlying array.\n  1500:     ///\n  1501:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n  1502:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1503:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1504:     #[inline]\n  1505:     #[must_use]\n  1506:     pub const fn as_array<const N: usize>(self) -> Option<*const [T; N]> {\n  1507:         if self.len() == N {\n  1508:             let me = self.as_ptr() as *const [T; N];\n  1509:             Some(me)\n  1510:         } else {\n  1511:             None\n  1512:         }\n  1513:     }\n  1514: \n  1515:     /// Returns a raw pointer to an element or subslice, without doing bounds\n  1516:     /// checking.\n  1517:     ///\n  1518:     /// Calling this method with an out-of-bounds index or when `self` is not dereferenceable\n  1519:     /// is *[undefined behavior]* even if the resulting pointer is not used.\n  1520:     ///\n  1521:     /// [undefined behavior]: https://doc.rust-lang.org/reference/behavior-considered-undefined.html\n  1522:     ///",
    "nanvix_source": "  1478:         self as *const T\n  1479:     }\n  1480: \n  1481:     /// Gets a raw pointer to the underlying array.\n  1482:     ///\n  1483:     /// If `N` is not exactly equal to the length of `self`, then this method returns `None`.\n  1484:     #[stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1485:     #[rustc_const_stable(feature = \"core_slice_as_array\", since = \"1.93.0\")]\n  1486:     #[inline]\n  1487:     #[must_use]\n  1488:     pub const fn as_array<const N: usize>(self) -> Option<*const [T; N]> {\n  1489:         if self.len() == N {\n  1490:             let me = self.as_ptr() as *const [T; N];\n  1491:             Some(me)\n  1492:         } else {\n  1493:             None\n  1494:         }\n  1495:     }\n  1496: \n  1497:     /// Returns a raw pointer to an element or subslice, without doing bounds\n  1498:     /// checking.",
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
