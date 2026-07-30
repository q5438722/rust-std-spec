For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::copy_from",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "copy_from",
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
            "src",
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
    "verification_source": "  1343:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1344:         unsafe { copy_nonoverlapping(self, dest, count) }\n  1345:     }\n  1346: \n  1347:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1348:     /// and destination may overlap.\n  1349:     ///\n  1350:     /// NOTE: this has the *opposite* argument order of [`ptr::copy`].\n  1351:     ///\n  1352:     /// See [`ptr::copy`] for safety concerns and examples.\n  1353:     ///\n  1354:     /// [`ptr::copy`]: crate::ptr::copy()\n  1355:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1356:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1357:     #[inline(always)]\n  1358:     #[track_caller]\n  1359:     pub const unsafe fn copy_from(self, src: *const T, count: usize)\n  1360:     where\n  1361:         T: Sized,\n  1362:     {\n  1363:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1364:         unsafe { copy(src, self, count) }\n  1365:     }\n  1366: \n  1367:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1368:     /// and destination may *not* overlap.\n  1369:     ///\n  1370:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1371:     ///\n  1372:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1373:     ///\n  1374:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1375:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]",
    "nanvix_source": "  1331:     ///\n  1332:     /// NOTE: this has the *opposite* argument order of [`ptr::copy`].\n  1333:     ///\n  1334:     /// See [`ptr::copy`] for safety concerns and examples.\n  1335:     ///\n  1336:     /// [`ptr::copy`]: crate::ptr::copy()\n  1337:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1338:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1339:     #[inline(always)]\n  1340:     #[track_caller]\n  1341:     pub const unsafe fn copy_from(self, src: *const T, count: usize)\n  1342:     where\n  1343:         T: Sized,\n  1344:     {\n  1345:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1346:         unsafe { copy(src, self, count) }\n  1347:     }\n  1348: \n  1349:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1350:     /// and destination may *not* overlap.\n  1351:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::copy_from_nonoverlapping",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "copy_from_nonoverlapping",
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
            "src",
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
    "verification_source": "  1363:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1364:         unsafe { copy(src, self, count) }\n  1365:     }\n  1366: \n  1367:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1368:     /// and destination may *not* overlap.\n  1369:     ///\n  1370:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1371:     ///\n  1372:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1373:     ///\n  1374:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1375:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1376:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1377:     #[inline(always)]\n  1378:     #[track_caller]\n  1379:     pub const unsafe fn copy_from_nonoverlapping(self, src: *const T, count: usize)\n  1380:     where\n  1381:         T: Sized,\n  1382:     {\n  1383:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1384:         unsafe { copy_nonoverlapping(src, self, count) }\n  1385:     }\n  1386: \n  1387:     /// Executes the destructor (if any) of the pointed-to value.\n  1388:     ///\n  1389:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1390:     ///\n  1391:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1392:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1393:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1394:     #[inline(always)]\n  1395:     pub const unsafe fn drop_in_place(self)",
    "nanvix_source": "  1351:     ///\n  1352:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1353:     ///\n  1354:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1355:     ///\n  1356:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1357:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1358:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1359:     #[inline(always)]\n  1360:     #[track_caller]\n  1361:     pub const unsafe fn copy_from_nonoverlapping(self, src: *const T, count: usize)\n  1362:     where\n  1363:         T: Sized,\n  1364:     {\n  1365:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1366:         unsafe { copy_nonoverlapping(src, self, count) }\n  1367:     }\n  1368: \n  1369:     /// Executes the destructor (if any) of the pointed-to value.\n  1370:     ///\n  1371:     /// See [`ptr::drop_in_place`] for safety concerns and examples.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::copy_nonoverlapping",
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
      "name": "copy_nonoverlapping",
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
            "src",
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
            "dst",
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
    "verification_source": "   515: /// let mut a = vec!['r'];\n   516: /// let mut b = vec!['u', 's', 't'];\n   517: ///\n   518: /// append(&mut a, &mut b);\n   519: ///\n   520: /// assert_eq!(a, &['r', 'u', 's', 't']);\n   521: /// assert!(b.is_empty());\n   522: /// ```\n   523: ///\n   524: /// [`Vec::append`]: ../../std/vec/struct.Vec.html#method.append\n   525: #[doc(alias = \"memcpy\")]\n   526: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   527: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   528: #[inline(always)]\n   529: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   530: #[rustc_diagnostic_item = \"ptr_copy_nonoverlapping\"]\n   531: pub const unsafe fn copy_nonoverlapping<T>(src: *const T, dst: *mut T, count: usize) {\n   532:     ub_checks::assert_unsafe_precondition!(\n   533:         check_language_ub,\n   534:         \"ptr::copy_nonoverlapping requires that both pointer arguments are aligned and non-null \\\n   535:         and the specified memory ranges do not overlap\",\n   536:         (\n   537:             src: *const () = src as *const (),\n   538:             dst: *mut () = dst as *mut (),\n   539:             size: usize = size_of::<T>(),\n   540:             align: usize = align_of::<T>(),\n   541:             count: usize = count,\n   542:         ) => {\n   543:             let zero_size = count == 0 || size == 0;\n   544:             ub_checks::maybe_is_aligned_and_not_null(src, align, zero_size)\n   545:                 && ub_checks::maybe_is_aligned_and_not_null(dst, align, zero_size)\n   546:                 && ub_checks::maybe_is_nonoverlapping(src, dst, size, count)\n   547:         }",
    "nanvix_source": "   518: /// assert!(b.is_empty());\n   519: /// ```\n   520: ///\n   521: /// [`Vec::append`]: ../../std/vec/struct.Vec.html#method.append\n   522: #[doc(alias = \"memcpy\")]\n   523: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   524: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   525: #[inline(always)]\n   526: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   527: #[rustc_diagnostic_item = \"ptr_copy_nonoverlapping\"]\n   528: pub const unsafe fn copy_nonoverlapping<T>(src: *const T, dst: *mut T, count: usize) {\n   529:     ub_checks::assert_unsafe_precondition!(\n   530:         check_language_ub,\n   531:         \"ptr::copy_nonoverlapping requires that both pointer arguments are aligned and non-null \\\n   532:         and the specified memory ranges do not overlap\",\n   533:         (\n   534:             src: *const () = src as *const (),\n   535:             dst: *mut () = dst as *mut (),\n   536:             size: usize = size_of::<T>(),\n   537:             align: usize = align_of::<T>(),\n   538:             count: usize = count,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::copy_to",
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
      "name": "copy_to",
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
            "dest",
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
    "verification_source": "  1211:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n  1212:         unsafe { read_unaligned(self) }\n  1213:     }\n  1214: \n  1215:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1216:     /// and destination may overlap.\n  1217:     ///\n  1218:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n  1219:     ///\n  1220:     /// See [`ptr::copy`] for safety concerns and examples.\n  1221:     ///\n  1222:     /// [`ptr::copy`]: crate::ptr::copy()\n  1223:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1224:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1225:     #[inline]\n  1226:     #[track_caller]\n  1227:     pub const unsafe fn copy_to(self, dest: *mut T, count: usize)\n  1228:     where\n  1229:         T: Sized,\n  1230:     {\n  1231:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1232:         unsafe { copy(self, dest, count) }\n  1233:     }\n  1234: \n  1235:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1236:     /// and destination may *not* overlap.\n  1237:     ///\n  1238:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n  1239:     ///\n  1240:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1241:     ///\n  1242:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1243:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]",
    "nanvix_source": "  1199:     ///\n  1200:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n  1201:     ///\n  1202:     /// See [`ptr::copy`] for safety concerns and examples.\n  1203:     ///\n  1204:     /// [`ptr::copy`]: crate::ptr::copy()\n  1205:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1206:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1207:     #[inline]\n  1208:     #[track_caller]\n  1209:     pub const unsafe fn copy_to(self, dest: *mut T, count: usize)\n  1210:     where\n  1211:         T: Sized,\n  1212:     {\n  1213:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1214:         unsafe { copy(self, dest, count) }\n  1215:     }\n  1216: \n  1217:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1218:     /// and destination may *not* overlap.\n  1219:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::copy_to_nonoverlapping",
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
      "name": "copy_to_nonoverlapping",
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
            "dest",
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
    "verification_source": "  1231:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1232:         unsafe { copy(self, dest, count) }\n  1233:     }\n  1234: \n  1235:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1236:     /// and destination may *not* overlap.\n  1237:     ///\n  1238:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n  1239:     ///\n  1240:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1241:     ///\n  1242:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1243:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1244:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1245:     #[inline]\n  1246:     #[track_caller]\n  1247:     pub const unsafe fn copy_to_nonoverlapping(self, dest: *mut T, count: usize)\n  1248:     where\n  1249:         T: Sized,\n  1250:     {\n  1251:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1252:         unsafe { copy_nonoverlapping(self, dest, count) }\n  1253:     }\n  1254: \n  1255:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1256:     /// `align`.\n  1257:     ///\n  1258:     /// If it is not possible to align the pointer, the implementation returns\n  1259:     /// `usize::MAX`.\n  1260:     ///\n  1261:     /// The offset is expressed in number of `T` elements, and not bytes. The value returned can be\n  1262:     /// used with the `wrapping_add` method.\n  1263:     ///",
    "nanvix_source": "  1219:     ///\n  1220:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n  1221:     ///\n  1222:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1223:     ///\n  1224:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1225:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1226:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1227:     #[inline]\n  1228:     #[track_caller]\n  1229:     pub const unsafe fn copy_to_nonoverlapping(self, dest: *mut T, count: usize)\n  1230:     where\n  1231:         T: Sized,\n  1232:     {\n  1233:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1234:         unsafe { copy_nonoverlapping(self, dest, count) }\n  1235:     }\n  1236: \n  1237:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1238:     /// `align`.\n  1239:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::dangling",
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
      "name": "dangling",
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
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   890:     without_provenance_mut(addr)\n   891: }\n   892: \n   893: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   894: ///\n   895: /// This is useful for initializing types which lazily allocate, like\n   896: /// `Vec::new` does.\n   897: ///\n   898: /// Note that the address of the returned pointer may potentially\n   899: /// be that of a valid pointer, which means this must not be used\n   900: /// as a \"not yet initialized\" sentinel value.\n   901: /// Types that lazily allocate must track initialization by some other means.\n   902: #[inline(always)]\n   903: #[must_use]\n   904: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   905: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   906: pub const fn dangling<T>() -> *const T {\n   907:     dangling_mut()\n   908: }\n   909: \n   910: /// Creates a pointer with the given address and no [provenance][crate::ptr#provenance].\n   911: ///\n   912: /// This is equivalent to `ptr::null_mut().with_addr(addr)`.\n   913: ///\n   914: /// Without provenance, this pointer is not associated with any actual allocation. Such a\n   915: /// no-provenance pointer may be used for zero-sized memory accesses (if suitably aligned), but\n   916: /// non-zero-sized memory accesses with a no-provenance pointer are UB. No-provenance pointers are\n   917: /// little more than a `usize` address in disguise.\n   918: ///\n   919: /// This is different from `addr as *mut T`, which creates a pointer that picks up a previously\n   920: /// exposed provenance. See [`with_exposed_provenance_mut`] for more details on that operation.\n   921: ///\n   922: /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.",
    "nanvix_source": "   906: /// `Vec::new` does.\n   907: ///\n   908: /// Note that the address of the returned pointer may potentially\n   909: /// be that of a valid pointer, which means this must not be used\n   910: /// as a \"not yet initialized\" sentinel value.\n   911: /// Types that lazily allocate must track initialization by some other means.\n   912: #[inline(always)]\n   913: #[must_use]\n   914: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   915: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   916: pub const fn dangling<T>() -> *const T {\n   917:     dangling_mut()\n   918: }\n   919: \n   920: /// Creates a pointer with the given address and no [provenance][crate::ptr#provenance].\n   921: ///\n   922: /// This is equivalent to `ptr::null_mut().with_addr(addr)`.\n   923: ///\n   924: /// Without provenance, this pointer is not associated with any actual allocation. Such a\n   925: /// no-provenance pointer may be used for zero-sized memory accesses (if suitably aligned), but\n   926: /// non-zero-sized memory accesses with a no-provenance pointer are UB. No-provenance pointers are",
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
