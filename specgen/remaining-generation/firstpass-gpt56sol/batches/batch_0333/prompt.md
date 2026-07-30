For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::dangling_mut",
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
      "name": "dangling_mut",
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
        "inputs": [],
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
    "verification_source": "   935:     unsafe { mem::transmute(addr) }\n   936: }\n   937: \n   938: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   939: ///\n   940: /// This is useful for initializing types which lazily allocate, like\n   941: /// `Vec::new` does.\n   942: ///\n   943: /// Note that the address of the returned pointer may potentially\n   944: /// be that of a valid pointer, which means this must not be used\n   945: /// as a \"not yet initialized\" sentinel value.\n   946: /// Types that lazily allocate must track initialization by some other means.\n   947: #[inline(always)]\n   948: #[must_use]\n   949: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   950: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   951: pub const fn dangling_mut<T>() -> *mut T {\n   952:     NonNull::dangling().as_ptr()\n   953: }\n   954: \n   955: /// Converts an address back to a pointer, picking up some previously 'exposed'\n   956: /// [provenance][crate::ptr#provenance].\n   957: ///\n   958: /// This is fully equivalent to `addr as *const T`. The provenance of the returned pointer is that\n   959: /// of *some* pointer that was previously exposed by passing it to\n   960: /// [`expose_provenance`][pointer::expose_provenance], or a `ptr as usize` cast. In addition, memory\n   961: /// which is outside the control of the Rust abstract machine (MMIO registers, for example) is\n   962: /// always considered to be accessible with an exposed provenance, so long as this memory is disjoint\n   963: /// from memory that will be used by the abstract machine such as the stack, heap, and statics.\n   964: ///\n   965: /// The exact provenance that gets picked is not specified. The compiler will do its best to pick\n   966: /// the \"right\" provenance for you (whatever that may be), but currently we cannot provide any\n   967: /// guarantees about which provenance the resulting pointer will have -- and therefore there",
    "nanvix_source": "   951: /// `Vec::new` does.\n   952: ///\n   953: /// Note that the address of the returned pointer may potentially\n   954: /// be that of a valid pointer, which means this must not be used\n   955: /// as a \"not yet initialized\" sentinel value.\n   956: /// Types that lazily allocate must track initialization by some other means.\n   957: #[inline(always)]\n   958: #[must_use]\n   959: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   960: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   961: pub const fn dangling_mut<T>() -> *mut T {\n   962:     NonNull::dangling().as_ptr()\n   963: }\n   964: \n   965: /// Converts an address back to a pointer, picking up some previously 'exposed'\n   966: /// [provenance][crate::ptr#provenance].\n   967: ///\n   968: /// This is fully equivalent to `addr as *const T`. The provenance of the returned pointer is that\n   969: /// of *some* pointer that was previously exposed by passing it to\n   970: /// [`expose_provenance`][pointer::expose_provenance], or a `ptr as usize` cast. In addition, memory\n   971: /// which is outside the control of the Rust abstract machine (MMIO registers, for example) is",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::drop_in_place",
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
              "bounds": [],
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
      "name": "drop_in_place",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1379:     pub const unsafe fn copy_from_nonoverlapping(self, src: *const T, count: usize)\n  1380:     where\n  1381:         T: Sized,\n  1382:     {\n  1383:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1384:         unsafe { copy_nonoverlapping(src, self, count) }\n  1385:     }\n  1386: \n  1387:     /// Executes the destructor (if any) of the pointed-to value.\n  1388:     ///\n  1389:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1390:     ///\n  1391:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1392:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1393:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1394:     #[inline(always)]\n  1395:     pub const unsafe fn drop_in_place(self)\n  1396:     where\n  1397:         T: [const] Destruct,\n  1398:     {\n  1399:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1400:         unsafe { drop_in_place(self) }\n  1401:     }\n  1402: \n  1403:     /// Overwrites a memory location with the given value without reading or\n  1404:     /// dropping the old value.\n  1405:     ///\n  1406:     /// See [`ptr::write`] for safety concerns and examples.\n  1407:     ///\n  1408:     /// [`ptr::write`]: crate::ptr::write()\n  1409:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1410:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1411:     #[inline(always)]",
    "nanvix_source": "  1367:     }\n  1368: \n  1369:     /// Executes the destructor (if any) of the pointed-to value.\n  1370:     ///\n  1371:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1372:     ///\n  1373:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1374:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1375:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1376:     #[inline(always)]\n  1377:     pub const unsafe fn drop_in_place(self)\n  1378:     where\n  1379:         T: [const] Destruct,\n  1380:     {\n  1381:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1382:         unsafe { drop_in_place(self) }\n  1383:     }\n  1384: \n  1385:     /// Overwrites a memory location with the given value without reading or\n  1386:     /// dropping the old value.\n  1387:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::eq",
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
      "name": "eq",
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
            "a",
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
            "b",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2407: /// assert!(!ptr::eq(five_ref, other_five_ref));\n  2408: /// ```\n  2409: ///\n  2410: /// Slices are also compared by their length (fat pointers):\n  2411: ///\n  2412: /// ```\n  2413: /// let a = [1, 2, 3];\n  2414: /// assert!(std::ptr::eq(&a[..3], &a[..3]));\n  2415: /// assert!(!std::ptr::eq(&a[..2], &a[..3]));\n  2416: /// assert!(!std::ptr::eq(&a[0..2], &a[1..3]));\n  2417: /// ```\n  2418: #[stable(feature = \"ptr_eq\", since = \"1.17.0\")]\n  2419: #[inline(always)]\n  2420: #[must_use = \"pointer comparison produces a value\"]\n  2421: #[rustc_diagnostic_item = \"ptr_eq\"]\n  2422: #[allow(ambiguous_wide_pointer_comparisons)] // it's actually clear here\n  2423: pub fn eq<T: PointeeSized>(a: *const T, b: *const T) -> bool {\n  2424:     a == b\n  2425: }\n  2426: \n  2427: /// Compares the *addresses* of the two pointers for equality,\n  2428: /// ignoring any metadata in fat pointers.\n  2429: ///\n  2430: /// If the arguments are thin pointers of the same type,\n  2431: /// then this is the same as [`eq`].\n  2432: ///\n  2433: /// # Examples\n  2434: ///\n  2435: /// ```\n  2436: /// use std::ptr;\n  2437: ///\n  2438: /// let whole: &[i32; 3] = &[1, 2, 3];\n  2439: /// let first: &i32 = &whole[0];",
    "nanvix_source": "  2465: /// let a = [1, 2, 3];\n  2466: /// assert!(std::ptr::eq(&a[..3], &a[..3]));\n  2467: /// assert!(!std::ptr::eq(&a[..2], &a[..3]));\n  2468: /// assert!(!std::ptr::eq(&a[0..2], &a[1..3]));\n  2469: /// ```\n  2470: #[stable(feature = \"ptr_eq\", since = \"1.17.0\")]\n  2471: #[inline(always)]\n  2472: #[must_use = \"pointer comparison produces a value\"]\n  2473: #[rustc_diagnostic_item = \"ptr_eq\"]\n  2474: #[allow(ambiguous_wide_pointer_comparisons)] // it's actually clear here\n  2475: pub fn eq<T: PointeeSized>(a: *const T, b: *const T) -> bool {\n  2476:     a == b\n  2477: }\n  2478: \n  2479: /// Compares the *addresses* of the two pointers for equality,\n  2480: /// ignoring any metadata in fat pointers.\n  2481: ///\n  2482: /// If the arguments are thin pointers of the same type,\n  2483: /// then this is the same as [`eq`].\n  2484: ///\n  2485: /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::expose_provenance",
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
      "name": "expose_provenance",
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
    "verification_source": "   161:     /// Due to its inherent ambiguity, [`with_exposed_provenance_mut`] may not be supported by tools\n   162:     /// that help you to stay conformant with the Rust memory model. It is recommended to use\n   163:     /// [Strict Provenance][crate::ptr#strict-provenance] APIs such as [`with_addr`][pointer::with_addr]\n   164:     /// wherever possible, in which case [`addr`][pointer::addr] should be used instead of `expose_provenance`.\n   165:     ///\n   166:     /// On most platforms this will produce a value with the same bytes as the original pointer,\n   167:     /// because all the bytes are dedicated to describing the address. Platforms which need to store\n   168:     /// additional information in the pointer may not support this operation, since the 'expose'\n   169:     /// side-effect which is required for [`with_exposed_provenance_mut`] to work is typically not\n   170:     /// available.\n   171:     ///\n   172:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   173:     ///\n   174:     /// [`with_exposed_provenance_mut`]: with_exposed_provenance_mut\n   175:     #[inline(always)]\n   176:     #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n   177:     pub fn expose_provenance(self) -> usize {\n   178:         self.cast::<()>() as usize\n   179:     }\n   180: \n   181:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   182:     /// `self`.\n   183:     ///\n   184:     /// This is similar to a `addr as *mut T` cast, but copies\n   185:     /// the *provenance* of `self` to the new pointer.\n   186:     /// This avoids the inherent ambiguity of the unary cast.\n   187:     ///\n   188:     /// This is equivalent to using [`wrapping_offset`][pointer::wrapping_offset] to offset\n   189:     /// `self` to the given address, and therefore has all the same capabilities and restrictions.\n   190:     ///\n   191:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   192:     #[must_use]\n   193:     #[inline]",
    "nanvix_source": "   168:     /// additional information in the pointer may not support this operation, since the 'expose'\n   169:     /// side-effect which is required for [`with_exposed_provenance_mut`] to work is typically not\n   170:     /// available.\n   171:     ///\n   172:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   173:     ///\n   174:     /// [`with_exposed_provenance_mut`]: with_exposed_provenance_mut\n   175:     #[inline(always)]\n   176:     #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n   177:     #[expect(implicit_provenance_casts, reason = \"this *is* the replacement\")]\n   178:     pub fn expose_provenance(self) -> usize {\n   179:         self.cast::<()>() as usize\n   180:     }\n   181: \n   182:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   183:     /// `self`.\n   184:     ///\n   185:     /// This is similar to a `addr as *mut T` cast, but copies\n   186:     /// the *provenance* of `self` to the new pointer.\n   187:     /// This avoids the inherent ambiguity of the unary cast.\n   188:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::from_mut",
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "r"
        ],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "r",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "T"
                }
              }
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
    "verification_source": "  1124: /// ```\n  1125: /// The recommended way to write this code is to avoid relying on lifetime extension\n  1126: /// when raw pointers are involved:\n  1127: /// ```rust\n  1128: /// # use std::ptr;\n  1129: /// # type T = i32;\n  1130: /// # fn foo() -> T { 42 }\n  1131: /// let mut x = foo();\n  1132: /// let p = ptr::from_mut(&mut x);\n  1133: /// unsafe { p.write(T::default()) };\n  1134: /// ```\n  1135: #[inline(always)]\n  1136: #[must_use]\n  1137: #[stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1138: #[rustc_const_stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1139: #[rustc_never_returns_null_ptr]\n  1140: pub const fn from_mut<T: PointeeSized>(r: &mut T) -> *mut T {\n  1141:     r\n  1142: }\n  1143: \n  1144: /// Forms a raw slice from a pointer and a length.\n  1145: ///\n  1146: /// The `len` argument is the number of **elements**, not the number of bytes.\n  1147: ///\n  1148: /// This function is safe, but actually using the return value is unsafe.\n  1149: /// See the documentation of [`slice::from_raw_parts`] for slice safety requirements.\n  1150: ///\n  1151: /// [`slice::from_raw_parts`]: crate::slice::from_raw_parts\n  1152: ///\n  1153: /// # Examples\n  1154: ///\n  1155: /// ```rust\n  1156: /// use std::ptr;",
    "nanvix_source": "  1140: /// # fn foo() -> T { 42 }\n  1141: /// let mut x = foo();\n  1142: /// let p = ptr::from_mut(&mut x);\n  1143: /// unsafe { p.write(T::default()) };\n  1144: /// ```\n  1145: #[inline(always)]\n  1146: #[must_use]\n  1147: #[stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1148: #[rustc_const_stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1149: #[rustc_never_returns_null_ptr]\n  1150: pub const fn from_mut<T: PointeeSized>(r: &mut T) -> *mut T {\n  1151:     r\n  1152: }\n  1153: \n  1154: /// Forms a raw slice from a pointer and a length.\n  1155: ///\n  1156: /// The `len` argument is the number of **elements**, not the number of bytes.\n  1157: ///\n  1158: /// This function is safe, but actually using the return value is unsafe.\n  1159: /// See the documentation of [`slice::from_raw_parts`] for slice safety requirements.\n  1160: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::from_ref",
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "from_ref",
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
            "r",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "T"
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
    "verification_source": "  1074: /// The recommended way to write this code is to avoid relying on lifetime extension\n  1075: /// when raw pointers are involved:\n  1076: /// ```rust\n  1077: /// # use std::ptr;\n  1078: /// # type T = i32;\n  1079: /// # fn foo() -> T { 42 }\n  1080: /// let x = foo();\n  1081: /// let p = ptr::from_ref(&x);\n  1082: /// unsafe { p.read() };\n  1083: /// ```\n  1084: #[inline(always)]\n  1085: #[must_use]\n  1086: #[stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1087: #[rustc_const_stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1088: #[rustc_never_returns_null_ptr]\n  1089: #[rustc_diagnostic_item = \"ptr_from_ref\"]\n  1090: pub const fn from_ref<T: PointeeSized>(r: &T) -> *const T {\n  1091:     r\n  1092: }\n  1093: \n  1094: /// Converts a mutable reference to a raw pointer.\n  1095: ///\n  1096: /// For `r: &mut T`, `from_mut(r)` is equivalent to `r as *mut T` (except for the caveat noted\n  1097: /// below), but is a bit safer since it will never silently change type or mutability, in particular\n  1098: /// if the code is refactored.\n  1099: ///\n  1100: /// The caller must ensure that the pointee outlives the pointer this function returns, or else it\n  1101: /// will end up dangling.\n  1102: ///\n  1103: /// ## Interaction with lifetime extension\n  1104: ///\n  1105: /// Note that this has subtle interactions with the rules for lifetime extension of temporaries in\n  1106: /// tail expressions. This code is valid, albeit in a non-obvious way:",
    "nanvix_source": "  1090: /// let x = foo();\n  1091: /// let p = ptr::from_ref(&x);\n  1092: /// unsafe { p.read() };\n  1093: /// ```\n  1094: #[inline(always)]\n  1095: #[must_use]\n  1096: #[stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1097: #[rustc_const_stable(feature = \"ptr_from_ref\", since = \"1.76.0\")]\n  1098: #[rustc_never_returns_null_ptr]\n  1099: #[rustc_diagnostic_item = \"ptr_from_ref\"]\n  1100: pub const fn from_ref<T: PointeeSized>(r: &T) -> *const T {\n  1101:     r\n  1102: }\n  1103: \n  1104: /// Converts a mutable reference to a raw pointer.\n  1105: ///\n  1106: /// For `r: &mut T`, `from_mut(r)` is equivalent to `r as *mut T` (except for the caveat noted\n  1107: /// below), but is a bit safer since it will never silently change type or mutability, in particular\n  1108: /// if the code is refactored.\n  1109: ///\n  1110: /// The caller must ensure that the pointee outlives the pointer this function returns, or else it",
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
