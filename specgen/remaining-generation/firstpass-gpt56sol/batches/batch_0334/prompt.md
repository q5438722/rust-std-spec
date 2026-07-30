For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::hash",
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
                        "id": 1003,
                        "path": "hash::Hasher"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "S"
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
      "name": "hash",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "into"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "hashee",
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
            "into",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "S"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2514: /// use std::ptr;\n  2515: ///\n  2516: /// let five = 5;\n  2517: /// let five_ref = &five;\n  2518: ///\n  2519: /// let mut hasher = DefaultHasher::new();\n  2520: /// ptr::hash(five_ref, &mut hasher);\n  2521: /// let actual = hasher.finish();\n  2522: ///\n  2523: /// let mut hasher = DefaultHasher::new();\n  2524: /// (five_ref as *const i32).hash(&mut hasher);\n  2525: /// let expected = hasher.finish();\n  2526: ///\n  2527: /// assert_eq!(actual, expected);\n  2528: /// ```\n  2529: #[stable(feature = \"ptr_hash\", since = \"1.35.0\")]\n  2530: pub fn hash<T: PointeeSized, S: hash::Hasher>(hashee: *const T, into: &mut S) {\n  2531:     use crate::hash::Hash;\n  2532:     hashee.hash(into);\n  2533: }\n  2534: \n  2535: #[stable(feature = \"fnptr_impls\", since = \"1.4.0\")]\n  2536: #[diagnostic::on_const(\n  2537:     message = \"pointers cannot be reliably compared during const eval\",\n  2538:     note = \"see issue #53020 <https://github.com/rust-lang/rust/issues/53020> for more information\"\n  2539: )]\n  2540: impl<F: FnPtr> PartialEq for F {\n  2541:     #[inline]\n  2542:     fn eq(&self, other: &Self) -> bool {\n  2543:         self.addr() == other.addr()\n  2544:     }\n  2545: }\n  2546: #[stable(feature = \"fnptr_impls\", since = \"1.4.0\")]",
    "nanvix_source": "  2572: /// ptr::hash(five_ref, &mut hasher);\n  2573: /// let actual = hasher.finish();\n  2574: ///\n  2575: /// let mut hasher = DefaultHasher::new();\n  2576: /// (five_ref as *const i32).hash(&mut hasher);\n  2577: /// let expected = hasher.finish();\n  2578: ///\n  2579: /// assert_eq!(actual, expected);\n  2580: /// ```\n  2581: #[stable(feature = \"ptr_hash\", since = \"1.35.0\")]\n  2582: pub fn hash<T: PointeeSized, S: hash::Hasher>(hashee: *const T, into: &mut S) {\n  2583:     use crate::hash::Hash;\n  2584:     hashee.hash(into);\n  2585: }\n  2586: \n  2587: #[stable(feature = \"fnptr_impls\", since = \"1.4.0\")]\n  2588: #[diagnostic::on_const(\n  2589:     message = \"pointers cannot be reliably compared during const eval\",\n  2590:     note = \"see issue #53020 <https://github.com/rust-lang/rust/issues/53020> for more information\"\n  2591: )]\n  2592: impl<F: FnPtr> PartialEq for F {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::is_aligned",
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
      "name": "is_aligned",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1316:     /// # Examples\n  1317:     ///\n  1318:     /// ```\n  1319:     /// // On some platforms, the alignment of i32 is less than 4.\n  1320:     /// #[repr(align(4))]\n  1321:     /// struct AlignedI32(i32);\n  1322:     ///\n  1323:     /// let data = AlignedI32(42);\n  1324:     /// let ptr = &data as *const AlignedI32;\n  1325:     ///\n  1326:     /// assert!(ptr.is_aligned());\n  1327:     /// assert!(!ptr.wrapping_byte_add(1).is_aligned());\n  1328:     /// ```\n  1329:     #[must_use]\n  1330:     #[inline]\n  1331:     #[stable(feature = \"pointer_is_aligned\", since = \"1.79.0\")]\n  1332:     pub fn is_aligned(self) -> bool\n  1333:     where\n  1334:         T: Sized,\n  1335:     {\n  1336:         self.is_aligned_to(align_of::<T>())\n  1337:     }\n  1338: \n  1339:     /// Returns whether the pointer is aligned to `align`.\n  1340:     ///\n  1341:     /// For non-`Sized` pointees this operation considers only the data pointer,\n  1342:     /// ignoring the metadata.\n  1343:     ///\n  1344:     /// # Panics\n  1345:     ///\n  1346:     /// The function panics if `align` is not a power-of-two (this includes 0).\n  1347:     ///\n  1348:     /// # Examples",
    "nanvix_source": "  1304:     ///\n  1305:     /// let data = AlignedI32(42);\n  1306:     /// let ptr = &data as *const AlignedI32;\n  1307:     ///\n  1308:     /// assert!(ptr.is_aligned());\n  1309:     /// assert!(!ptr.wrapping_byte_add(1).is_aligned());\n  1310:     /// ```\n  1311:     #[must_use]\n  1312:     #[inline]\n  1313:     #[stable(feature = \"pointer_is_aligned\", since = \"1.79.0\")]\n  1314:     pub fn is_aligned(self) -> bool\n  1315:     where\n  1316:         T: Sized,\n  1317:     {\n  1318:         self.is_aligned_to(align_of::<T>())\n  1319:     }\n  1320: \n  1321:     /// Returns whether the pointer is aligned to `align`.\n  1322:     ///\n  1323:     /// For non-`Sized` pointees this operation considers only the data pointer,\n  1324:     /// ignoring the metadata.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::is_empty",
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
      "name": "is_empty",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1460:         metadata(self)\n  1461:     }\n  1462: \n  1463:     /// Returns `true` if the raw slice has a length of 0.\n  1464:     ///\n  1465:     /// # Examples\n  1466:     ///\n  1467:     /// ```\n  1468:     /// use std::ptr;\n  1469:     ///\n  1470:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1471:     /// assert!(!slice.is_empty());\n  1472:     /// ```\n  1473:     #[inline(always)]\n  1474:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1475:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]\n  1476:     pub const fn is_empty(self) -> bool {\n  1477:         self.len() == 0\n  1478:     }\n  1479: \n  1480:     /// Returns a raw pointer to the slice's buffer.\n  1481:     ///\n  1482:     /// This is equivalent to casting `self` to `*const T`, but more type-safe.\n  1483:     ///\n  1484:     /// # Examples\n  1485:     ///\n  1486:     /// ```rust\n  1487:     /// #![feature(slice_ptr_get)]\n  1488:     /// use std::ptr;\n  1489:     ///\n  1490:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1491:     /// assert_eq!(slice.as_ptr(), ptr::null());\n  1492:     /// ```",
    "nanvix_source": "  1448:     ///\n  1449:     /// ```\n  1450:     /// use std::ptr;\n  1451:     ///\n  1452:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1453:     /// assert!(!slice.is_empty());\n  1454:     /// ```\n  1455:     #[inline(always)]\n  1456:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1457:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]\n  1458:     pub const fn is_empty(self) -> bool {\n  1459:         self.len() == 0\n  1460:     }\n  1461: \n  1462:     /// Returns a raw pointer to the slice's buffer.\n  1463:     ///\n  1464:     /// This is equivalent to casting `self` to `*const T`, but more type-safe.\n  1465:     ///\n  1466:     /// # Examples\n  1467:     ///\n  1468:     /// ```rust",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::is_null",
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
      "name": "is_null",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "    18:     #[rustc_const_stable(feature = \"const_ptr_is_null\", since = \"1.84.0\")]\n    19:     #[rustc_diagnostic_item = \"ptr_const_is_null\"]\n    20:     #[inline]\n    21:     #[rustc_allow_const_fn_unstable(const_eval_select)]\n    22:     pub const fn is_null(self) -> bool {\n    23:         // Compare via a cast to a thin pointer, so fat pointers are only\n    24:         // considering their \"data\" part for null-ness.\n    25:         let ptr = self as *const u8;\n    26:         const_eval_select!(\n    27:             @capture { ptr: *const u8 } -> bool:\n    28:             // This use of `const_raw_ptr_comparison` has been explicitly blessed by t-lang.\n    29:             if const #[rustc_allow_const_fn_unstable(const_raw_ptr_comparison)] {\n    30:                 match (ptr).guaranteed_eq(null_mut()) {\n    31:                     Some(res) => res,\n    32:                     // To remain maximally conservative, we stop execution when we don't\n    33:                     // know whether the pointer is null or not.\n    34:                     // We can *not* return `false` here, that would be unsound in `NonNull::new`!\n    35:                     None => panic!(\"null-ness of this pointer cannot be determined in const context\"),\n    36:                 }\n    37:             } else {\n    38:                 ptr.addr() == 0\n    39:             }\n    40:         )\n    41:     }\n    42: \n    43:     /// Casts to a pointer of another type.\n    44:     #[stable(feature = \"ptr_cast\", since = \"1.38.0\")]\n    45:     #[rustc_const_stable(feature = \"const_ptr_cast\", since = \"1.38.0\")]\n    46:     #[rustc_diagnostic_item = \"const_ptr_cast\"]\n    47:     #[inline(always)]\n    48:     pub const fn cast<U>(self) -> *const U {\n    49:         self as _\n    50:     }",
    "nanvix_source": "    24:         // considering their \"data\" part for null-ness.\n    25:         let ptr = self as *const u8;\n    26:         const_eval_select!(\n    27:             @capture { ptr: *const u8 } -> bool:\n    28:             // This use of `const_raw_ptr_comparison` has been explicitly blessed by t-lang.\n    29:             if const #[rustc_allow_const_fn_unstable(const_raw_ptr_comparison)] {\n    30:                 match (ptr).guaranteed_eq(null_mut()) {\n    31:                     Some(res) => res,\n    32:                     // To remain maximally conservative, we stop execution when we don't\n    33:                     // know whether the pointer is null or not.\n    34:                     // We can *not* return `false` here, that would be unsound in `NonNull::new`!\n    35:                     None => panic!(\"null-ness of this pointer cannot be determined in const context\"),\n    36:                 }\n    37:             } else {\n    38:                 ptr.addr() == 0\n    39:             }\n    40:         )\n    41:     }\n    42: \n    43:     /// Casts to a pointer of another type.\n    44:     #[stable(feature = \"ptr_cast\", since = \"1.38.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::len",
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
      "name": "len",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1443:     /// The returned value is the number of **elements**, not the number of bytes.\n  1444:     ///\n  1445:     /// This function is safe, even when the raw slice cannot be cast to a slice\n  1446:     /// reference because the pointer is null or unaligned.\n  1447:     ///\n  1448:     /// # Examples\n  1449:     ///\n  1450:     /// ```rust\n  1451:     /// use std::ptr;\n  1452:     ///\n  1453:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1454:     /// assert_eq!(slice.len(), 3);\n  1455:     /// ```\n  1456:     #[inline]\n  1457:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1458:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]\n  1459:     pub const fn len(self) -> usize {\n  1460:         metadata(self)\n  1461:     }\n  1462: \n  1463:     /// Returns `true` if the raw slice has a length of 0.\n  1464:     ///\n  1465:     /// # Examples\n  1466:     ///\n  1467:     /// ```\n  1468:     /// use std::ptr;\n  1469:     ///\n  1470:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1471:     /// assert!(!slice.is_empty());\n  1472:     /// ```\n  1473:     #[inline(always)]\n  1474:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1475:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]",
    "nanvix_source": "  1431:     ///\n  1432:     /// ```rust\n  1433:     /// use std::ptr;\n  1434:     ///\n  1435:     /// let slice: *const [i8] = ptr::slice_from_raw_parts(ptr::null(), 3);\n  1436:     /// assert_eq!(slice.len(), 3);\n  1437:     /// ```\n  1438:     #[inline]\n  1439:     #[stable(feature = \"slice_ptr_len\", since = \"1.79.0\")]\n  1440:     #[rustc_const_stable(feature = \"const_slice_ptr_len\", since = \"1.79.0\")]\n  1441:     pub const fn len(self) -> usize {\n  1442:         metadata(self)\n  1443:     }\n  1444: \n  1445:     /// Returns `true` if the raw slice has a length of 0.\n  1446:     ///\n  1447:     /// # Examples\n  1448:     ///\n  1449:     /// ```\n  1450:     /// use std::ptr;\n  1451:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::map_addr",
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
                        "args": {
                          "parenthesized": {
                            "inputs": [
                              {
                                "primitive": "usize"
                              }
                            ],
                            "output": {
                              "primitive": "usize"
                            }
                          }
                        },
                        "id": 24,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(usize) -> usize"
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
      "name": "map_addr",
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
            "f",
            {
              "impl_trait": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "primitive": "usize"
                            }
                          ],
                          "output": {
                            "primitive": "usize"
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   198:         // provenance.\n   199:         let self_addr = self.addr() as isize;\n   200:         let dest_addr = addr as isize;\n   201:         let offset = dest_addr.wrapping_sub(self_addr);\n   202:         self.wrapping_byte_offset(offset)\n   203:     }\n   204: \n   205:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the original\n   206:     /// pointer's [provenance][crate::ptr#provenance].\n   207:     ///\n   208:     /// This is a convenience for [`with_addr`][pointer::with_addr], see that method for details.\n   209:     ///\n   210:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   211:     #[must_use]\n   212:     #[inline]\n   213:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   214:     pub fn map_addr(self, f: impl FnOnce(usize) -> usize) -> Self {\n   215:         self.with_addr(f(self.addr()))\n   216:     }\n   217: \n   218:     /// Decompose a (possibly wide) pointer into its data pointer and metadata components.\n   219:     ///\n   220:     /// The pointer can be later reconstructed with [`from_raw_parts_mut`].\n   221:     #[unstable(feature = \"ptr_metadata\", issue = \"81513\")]\n   222:     #[inline]\n   223:     pub const fn to_raw_parts(self) -> (*mut (), <T as super::Pointee>::Metadata) {\n   224:         (self.cast(), super::metadata(self))\n   225:     }\n   226: \n   227:     #[doc = include_str!(\"./docs/as_ref.md\")]\n   228:     ///\n   229:     /// ```\n   230:     /// let ptr: *mut u8 = &mut 10u8 as *mut u8;",
    "nanvix_source": "   205: \n   206:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the original\n   207:     /// pointer's [provenance][crate::ptr#provenance].\n   208:     ///\n   209:     /// This is a convenience for [`with_addr`][pointer::with_addr], see that method for details.\n   210:     ///\n   211:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   212:     #[must_use]\n   213:     #[inline]\n   214:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   215:     pub fn map_addr(self, f: impl FnOnce(usize) -> usize) -> Self {\n   216:         self.with_addr(f(self.addr()))\n   217:     }\n   218: \n   219:     /// Decompose a (possibly wide) pointer into its data pointer and metadata components.\n   220:     ///\n   221:     /// The pointer can be later reconstructed with [`from_raw_parts_mut`].\n   222:     #[unstable(feature = \"ptr_metadata\", issue = \"81513\")]\n   223:     #[inline]\n   224:     pub const fn to_raw_parts(self) -> (*mut (), <T as super::Pointee>::Metadata) {\n   225:         (self.cast(), super::metadata(self))",
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
