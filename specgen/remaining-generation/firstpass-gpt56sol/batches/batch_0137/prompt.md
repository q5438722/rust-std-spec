For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::from_mut",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "r"
        ],
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "   275:         }\n   276:     }\n   277: \n   278:     /// Converts a reference to a `NonNull` pointer.\n   279:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   280:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   281:     #[inline]\n   282:     pub const fn from_ref(r: &T) -> Self {\n   283:         // SAFETY: A reference cannot be null.\n   284:         unsafe { transmute(r as *const T) }\n   285:     }\n   286: \n   287:     /// Converts a mutable reference to a `NonNull` pointer.\n   288:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   289:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   290:     #[inline]\n   291:     pub const fn from_mut(r: &mut T) -> Self {\n   292:         // SAFETY: A mutable reference cannot be null.\n   293:         unsafe { transmute(r as *mut T) }\n   294:     }\n   295: \n   296:     /// Performs the same functionality as [`std::ptr::from_raw_parts`], except that a\n   297:     /// `NonNull` pointer is returned, as opposed to a raw `*const` pointer.\n   298:     ///\n   299:     /// See the documentation of [`std::ptr::from_raw_parts`] for more details.\n   300:     ///\n   301:     /// [`std::ptr::from_raw_parts`]: crate::ptr::from_raw_parts\n   302:     #[unstable(feature = \"ptr_metadata\", issue = \"81513\")]\n   303:     #[inline]\n   304:     pub const fn from_raw_parts(\n   305:         data_pointer: NonNull<impl super::Thin>,\n   306:         metadata: <T as super::Pointee>::Metadata,\n   307:     ) -> NonNull<T> {",
    "nanvix_source": "   278:     #[inline]\n   279:     pub const fn from_ref(r: &T) -> Self {\n   280:         // SAFETY: A reference cannot be null.\n   281:         unsafe { transmute(r as *const T) }\n   282:     }\n   283: \n   284:     /// Converts a mutable reference to a `NonNull` pointer.\n   285:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   286:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   287:     #[inline]\n   288:     pub const fn from_mut(r: &mut T) -> Self {\n   289:         // SAFETY: A mutable reference cannot be null.\n   290:         unsafe { transmute(r as *mut T) }\n   291:     }\n   292: \n   293:     /// Performs the same functionality as [`std::ptr::from_raw_parts`], except that a\n   294:     /// `NonNull` pointer is returned, as opposed to a raw `*const` pointer.\n   295:     ///\n   296:     /// See the documentation of [`std::ptr::from_raw_parts`] for more details.\n   297:     ///\n   298:     /// [`std::ptr::from_raw_parts`]: crate::ptr::from_raw_parts",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::from_ref",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "from_ref",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "   266:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   267:     #[rustc_const_stable(feature = \"const_nonnull_new\", since = \"1.85.0\")]\n   268:     #[inline]\n   269:     pub const fn new(ptr: *mut T) -> Option<Self> {\n   270:         if !ptr.is_null() {\n   271:             // SAFETY: The pointer is already checked and is not null\n   272:             Some(unsafe { Self::new_unchecked(ptr) })\n   273:         } else {\n   274:             None\n   275:         }\n   276:     }\n   277: \n   278:     /// Converts a reference to a `NonNull` pointer.\n   279:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   280:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   281:     #[inline]\n   282:     pub const fn from_ref(r: &T) -> Self {\n   283:         // SAFETY: A reference cannot be null.\n   284:         unsafe { transmute(r as *const T) }\n   285:     }\n   286: \n   287:     /// Converts a mutable reference to a `NonNull` pointer.\n   288:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   289:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   290:     #[inline]\n   291:     pub const fn from_mut(r: &mut T) -> Self {\n   292:         // SAFETY: A mutable reference cannot be null.\n   293:         unsafe { transmute(r as *mut T) }\n   294:     }\n   295: \n   296:     /// Performs the same functionality as [`std::ptr::from_raw_parts`], except that a\n   297:     /// `NonNull` pointer is returned, as opposed to a raw `*const` pointer.\n   298:     ///",
    "nanvix_source": "   269:             Some(unsafe { Self::new_unchecked(ptr) })\n   270:         } else {\n   271:             None\n   272:         }\n   273:     }\n   274: \n   275:     /// Converts a reference to a `NonNull` pointer.\n   276:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   277:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   278:     #[inline]\n   279:     pub const fn from_ref(r: &T) -> Self {\n   280:         // SAFETY: A reference cannot be null.\n   281:         unsafe { transmute(r as *const T) }\n   282:     }\n   283: \n   284:     /// Converts a mutable reference to a `NonNull` pointer.\n   285:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   286:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   287:     #[inline]\n   288:     pub const fn from_mut(r: &mut T) -> Self {\n   289:         // SAFETY: A mutable reference cannot be null.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::is_aligned",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1310:     /// ```\n  1311:     /// use std::ptr::NonNull;\n  1312:     ///\n  1313:     /// // On some platforms, the alignment of i32 is less than 4.\n  1314:     /// #[repr(align(4))]\n  1315:     /// struct AlignedI32(i32);\n  1316:     ///\n  1317:     /// let data = AlignedI32(42);\n  1318:     /// let ptr = NonNull::<AlignedI32>::from(&data);\n  1319:     ///\n  1320:     /// assert!(ptr.is_aligned());\n  1321:     /// assert!(!NonNull::new(ptr.as_ptr().wrapping_byte_add(1)).unwrap().is_aligned());\n  1322:     /// ```\n  1323:     #[inline]\n  1324:     #[must_use]\n  1325:     #[stable(feature = \"pointer_is_aligned\", since = \"1.79.0\")]\n  1326:     pub fn is_aligned(self) -> bool\n  1327:     where\n  1328:         T: Sized,\n  1329:     {\n  1330:         self.as_ptr().is_aligned()\n  1331:     }\n  1332: \n  1333:     /// Returns whether the pointer is aligned to `align`.\n  1334:     ///\n  1335:     /// For non-`Sized` pointees this operation considers only the data pointer,\n  1336:     /// ignoring the metadata.\n  1337:     ///\n  1338:     /// # Panics\n  1339:     ///\n  1340:     /// The function panics if `align` is not a power-of-two (this includes 0).\n  1341:     ///\n  1342:     /// # Examples",
    "nanvix_source": "  1249:     ///\n  1250:     /// let data = AlignedI32(42);\n  1251:     /// let ptr = NonNull::<AlignedI32>::from(&data);\n  1252:     ///\n  1253:     /// assert!(ptr.is_aligned());\n  1254:     /// assert!(!NonNull::new(ptr.as_ptr().wrapping_byte_add(1)).unwrap().is_aligned());\n  1255:     /// ```\n  1256:     #[inline]\n  1257:     #[must_use]\n  1258:     #[stable(feature = \"pointer_is_aligned\", since = \"1.79.0\")]\n  1259:     pub fn is_aligned(self) -> bool\n  1260:     where\n  1261:         T: Sized,\n  1262:     {\n  1263:         self.as_ptr().is_aligned()\n  1264:     }\n  1265: \n  1266:     /// Returns whether the pointer is aligned to `align`.\n  1267:     ///\n  1268:     /// For non-`Sized` pointees this operation considers only the data pointer,\n  1269:     /// ignoring the metadata.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::is_empty",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "slice": {
                        "generic": "T"
                      }
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
        "impl_id": "core:9550",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1474:     }\n  1475: \n  1476:     /// Returns `true` if the non-null raw slice has a length of 0.\n  1477:     ///\n  1478:     /// # Examples\n  1479:     ///\n  1480:     /// ```rust\n  1481:     /// use std::ptr::NonNull;\n  1482:     ///\n  1483:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1484:     /// assert!(!slice.is_empty());\n  1485:     /// ```\n  1486:     #[stable(feature = \"slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1487:     #[rustc_const_stable(feature = \"const_slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1488:     #[must_use]\n  1489:     #[inline]\n  1490:     pub const fn is_empty(self) -> bool {\n  1491:         self.len() == 0\n  1492:     }\n  1493: \n  1494:     /// Returns a non-null pointer to the slice's buffer.\n  1495:     ///\n  1496:     /// # Examples\n  1497:     ///\n  1498:     /// ```rust\n  1499:     /// #![feature(slice_ptr_get)]\n  1500:     /// use std::ptr::NonNull;\n  1501:     ///\n  1502:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1503:     /// assert_eq!(slice.as_non_null_ptr(), NonNull::<i8>::dangling());\n  1504:     /// ```\n  1505:     #[inline]\n  1506:     #[must_use]",
    "nanvix_source": "  1413:     /// ```rust\n  1414:     /// use std::ptr::NonNull;\n  1415:     ///\n  1416:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1417:     /// assert!(!slice.is_empty());\n  1418:     /// ```\n  1419:     #[stable(feature = \"slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1420:     #[rustc_const_stable(feature = \"const_slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1421:     #[must_use]\n  1422:     #[inline]\n  1423:     pub const fn is_empty(self) -> bool {\n  1424:         self.len() == 0\n  1425:     }\n  1426: \n  1427:     /// Returns a non-null pointer to the slice's buffer.\n  1428:     ///\n  1429:     /// # Examples\n  1430:     ///\n  1431:     /// ```rust\n  1432:     /// #![feature(slice_ptr_get)]\n  1433:     /// use std::ptr::NonNull;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::len",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "slice": {
                        "generic": "T"
                      }
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
        "impl_id": "core:9550",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1456:     ///\n  1457:     /// This function is safe, even when the non-null raw slice cannot be dereferenced to a slice\n  1458:     /// because the pointer does not have a valid address.\n  1459:     ///\n  1460:     /// # Examples\n  1461:     ///\n  1462:     /// ```rust\n  1463:     /// use std::ptr::NonNull;\n  1464:     ///\n  1465:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1466:     /// assert_eq!(slice.len(), 3);\n  1467:     /// ```\n  1468:     #[stable(feature = \"slice_ptr_len_nonnull\", since = \"1.63.0\")]\n  1469:     #[rustc_const_stable(feature = \"const_slice_ptr_len_nonnull\", since = \"1.63.0\")]\n  1470:     #[must_use]\n  1471:     #[inline]\n  1472:     pub const fn len(self) -> usize {\n  1473:         self.as_ptr().len()\n  1474:     }\n  1475: \n  1476:     /// Returns `true` if the non-null raw slice has a length of 0.\n  1477:     ///\n  1478:     /// # Examples\n  1479:     ///\n  1480:     /// ```rust\n  1481:     /// use std::ptr::NonNull;\n  1482:     ///\n  1483:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1484:     /// assert!(!slice.is_empty());\n  1485:     /// ```\n  1486:     #[stable(feature = \"slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1487:     #[rustc_const_stable(feature = \"const_slice_ptr_is_empty_nonnull\", since = \"1.79.0\")]\n  1488:     #[must_use]",
    "nanvix_source": "  1395:     /// ```rust\n  1396:     /// use std::ptr::NonNull;\n  1397:     ///\n  1398:     /// let slice: NonNull<[i8]> = NonNull::slice_from_raw_parts(NonNull::dangling(), 3);\n  1399:     /// assert_eq!(slice.len(), 3);\n  1400:     /// ```\n  1401:     #[stable(feature = \"slice_ptr_len_nonnull\", since = \"1.63.0\")]\n  1402:     #[rustc_const_stable(feature = \"const_slice_ptr_len_nonnull\", since = \"1.63.0\")]\n  1403:     #[must_use]\n  1404:     #[inline]\n  1405:     pub const fn len(self) -> usize {\n  1406:         self.as_ptr().len()\n  1407:     }\n  1408: \n  1409:     /// Returns `true` if the non-null raw slice has a length of 0.\n  1410:     ///\n  1411:     /// # Examples\n  1412:     ///\n  1413:     /// ```rust\n  1414:     /// use std::ptr::NonNull;\n  1415:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::slice_from_raw_parts",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "slice_from_raw_parts",
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
                      "slice": {
                        "generic": "T"
                      }
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
        "impl_id": "core:9550",
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
            "data",
            {
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1432:     /// ```rust\n  1433:     /// use std::ptr::NonNull;\n  1434:     ///\n  1435:     /// // create a slice pointer when starting out with a pointer to the first element\n  1436:     /// let mut x = [5, 6, 7];\n  1437:     /// let nonnull_pointer = NonNull::new(x.as_mut_ptr()).unwrap();\n  1438:     /// let slice = NonNull::slice_from_raw_parts(nonnull_pointer, 3);\n  1439:     /// assert_eq!(unsafe { slice.as_ref()[2] }, 7);\n  1440:     /// ```\n  1441:     ///\n  1442:     /// (Note that this example artificially demonstrates a use of this method,\n  1443:     /// but `let slice = NonNull::from(&x[..]);` would be a better way to write code like this.)\n  1444:     #[stable(feature = \"nonnull_slice_from_raw_parts\", since = \"1.70.0\")]\n  1445:     #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n  1446:     #[must_use]\n  1447:     #[inline]\n  1448:     pub const fn slice_from_raw_parts(data: NonNull<T>, len: usize) -> Self {\n  1449:         // SAFETY: `data` is a `NonNull` pointer which is necessarily non-null\n  1450:         unsafe { Self::new_unchecked(super::slice_from_raw_parts_mut(data.as_ptr(), len)) }\n  1451:     }\n  1452: \n  1453:     /// Returns the length of a non-null raw slice.\n  1454:     ///\n  1455:     /// The returned value is the number of **elements**, not the number of bytes.\n  1456:     ///\n  1457:     /// This function is safe, even when the non-null raw slice cannot be dereferenced to a slice\n  1458:     /// because the pointer does not have a valid address.\n  1459:     ///\n  1460:     /// # Examples\n  1461:     ///\n  1462:     /// ```rust\n  1463:     /// use std::ptr::NonNull;\n  1464:     ///",
    "nanvix_source": "  1371:     /// let slice = NonNull::slice_from_raw_parts(nonnull_pointer, 3);\n  1372:     /// assert_eq!(unsafe { slice.as_ref()[2] }, 7);\n  1373:     /// ```\n  1374:     ///\n  1375:     /// (Note that this example artificially demonstrates a use of this method,\n  1376:     /// but `let slice = NonNull::from(&x[..]);` would be a better way to write code like this.)\n  1377:     #[stable(feature = \"nonnull_slice_from_raw_parts\", since = \"1.70.0\")]\n  1378:     #[rustc_const_stable(feature = \"const_slice_from_raw_parts_mut\", since = \"1.83.0\")]\n  1379:     #[must_use]\n  1380:     #[inline]\n  1381:     pub const fn slice_from_raw_parts(data: NonNull<T>, len: usize) -> Self {\n  1382:         // SAFETY: `data` is a `NonNull` pointer which is necessarily non-null\n  1383:         unsafe { Self::new_unchecked(data.as_ptr().cast_slice(len)) }\n  1384:     }\n  1385: \n  1386:     /// Returns the length of a non-null raw slice.\n  1387:     ///\n  1388:     /// The returned value is the number of **elements**, not the number of bytes.\n  1389:     ///\n  1390:     /// This function is safe, even when the non-null raw slice cannot be dereferenced to a slice\n  1391:     /// because the pointer does not have a valid address.",
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
