For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::string::String::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to_fit",
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
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
    "verification_source": "  1349:     /// Shrinks the capacity of this `String` to match its length.\n  1350:     ///\n  1351:     /// # Examples\n  1352:     ///\n  1353:     /// ```\n  1354:     /// let mut s = String::from(\"foo\");\n  1355:     ///\n  1356:     /// s.reserve(100);\n  1357:     /// assert!(s.capacity() >= 100);\n  1358:     ///\n  1359:     /// s.shrink_to_fit();\n  1360:     /// assert_eq!(3, s.capacity());\n  1361:     /// ```\n  1362:     #[cfg(not(no_global_oom_handling))]\n  1363:     #[inline]\n  1364:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1365:     pub fn shrink_to_fit(&mut self) {\n  1366:         self.vec.shrink_to_fit()\n  1367:     }\n  1368: \n  1369:     /// Shrinks the capacity of this `String` with a lower bound.\n  1370:     ///\n  1371:     /// The capacity will remain at least as large as both the length\n  1372:     /// and the supplied value.\n  1373:     ///\n  1374:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1375:     ///\n  1376:     /// # Examples\n  1377:     ///\n  1378:     /// ```\n  1379:     /// let mut s = String::from(\"foo\");\n  1380:     ///\n  1381:     /// s.reserve(100);",
    "nanvix_source": "  1360:     ///\n  1361:     /// s.reserve(100);\n  1362:     /// assert!(s.capacity() >= 100);\n  1363:     ///\n  1364:     /// s.shrink_to_fit();\n  1365:     /// assert_eq!(3, s.capacity());\n  1366:     /// ```\n  1367:     #[cfg(not(no_global_oom_handling))]\n  1368:     #[inline]\n  1369:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1370:     pub fn shrink_to_fit(&mut self) {\n  1371:         self.vec.shrink_to_fit()\n  1372:     }\n  1373: \n  1374:     /// Shrinks the capacity of this `String` with a lower bound.\n  1375:     ///\n  1376:     /// The capacity will remain at least as large as both the length\n  1377:     /// and the supplied value.\n  1378:     ///\n  1379:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1380:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_reserve",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
            "additional",
            {
              "primitive": "usize"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1288:     /// use std::collections::TryReserveError;\n  1289:     ///\n  1290:     /// fn process_data(data: &str) -> Result<String, TryReserveError> {\n  1291:     ///     let mut output = String::new();\n  1292:     ///\n  1293:     ///     // Pre-reserve the memory, exiting if we can't\n  1294:     ///     output.try_reserve(data.len())?;\n  1295:     ///\n  1296:     ///     // Now we know this can't OOM in the middle of our complex work\n  1297:     ///     output.push_str(data);\n  1298:     ///\n  1299:     ///     Ok(output)\n  1300:     /// }\n  1301:     /// # process_data(\"rust\").expect(\"why is the test harness OOMing on 4 bytes?\");\n  1302:     /// ```\n  1303:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1304:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1305:         self.vec.try_reserve(additional)\n  1306:     }\n  1307: \n  1308:     /// Tries to reserve the minimum capacity for at least `additional` bytes\n  1309:     /// more than the current length. Unlike [`try_reserve`], this will not\n  1310:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1311:     /// After calling `try_reserve_exact`, capacity will be greater than or\n  1312:     /// equal to `self.len() + additional` if it returns `Ok(())`.\n  1313:     /// Does nothing if the capacity is already sufficient.\n  1314:     ///\n  1315:     /// Note that the allocator may give the collection more space than it\n  1316:     /// requests. Therefore, capacity can not be relied upon to be precisely\n  1317:     /// minimal. Prefer [`try_reserve`] if future insertions are expected.\n  1318:     ///\n  1319:     /// [`try_reserve`]: String::try_reserve\n  1320:     ///",
    "nanvix_source": "  1299:     ///     output.try_reserve(data.len())?;\n  1300:     ///\n  1301:     ///     // Now we know this can't OOM in the middle of our complex work\n  1302:     ///     output.push_str(data);\n  1303:     ///\n  1304:     ///     Ok(output)\n  1305:     /// }\n  1306:     /// # process_data(\"rust\").expect(\"why is the test harness OOMing on 4 bytes?\");\n  1307:     /// ```\n  1308:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1309:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1310:         self.vec.try_reserve(additional)\n  1311:     }\n  1312: \n  1313:     /// Tries to reserve the minimum capacity for at least `additional` bytes\n  1314:     /// more than the current length. Unlike [`try_reserve`], this will not\n  1315:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1316:     /// After calling `try_reserve_exact`, capacity will be greater than or\n  1317:     /// equal to `self.len() + additional` if it returns `Ok(())`.\n  1318:     /// Does nothing if the capacity is already sufficient.\n  1319:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::try_reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_reserve_exact",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
            "additional",
            {
              "primitive": "usize"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1329:     /// use std::collections::TryReserveError;\n  1330:     ///\n  1331:     /// fn process_data(data: &str) -> Result<String, TryReserveError> {\n  1332:     ///     let mut output = String::new();\n  1333:     ///\n  1334:     ///     // Pre-reserve the memory, exiting if we can't\n  1335:     ///     output.try_reserve_exact(data.len())?;\n  1336:     ///\n  1337:     ///     // Now we know this can't OOM in the middle of our complex work\n  1338:     ///     output.push_str(data);\n  1339:     ///\n  1340:     ///     Ok(output)\n  1341:     /// }\n  1342:     /// # process_data(\"rust\").expect(\"why is the test harness OOMing on 4 bytes?\");\n  1343:     /// ```\n  1344:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1345:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1346:         self.vec.try_reserve_exact(additional)\n  1347:     }\n  1348: \n  1349:     /// Shrinks the capacity of this `String` to match its length.\n  1350:     ///\n  1351:     /// # Examples\n  1352:     ///\n  1353:     /// ```\n  1354:     /// let mut s = String::from(\"foo\");\n  1355:     ///\n  1356:     /// s.reserve(100);\n  1357:     /// assert!(s.capacity() >= 100);\n  1358:     ///\n  1359:     /// s.shrink_to_fit();\n  1360:     /// assert_eq!(3, s.capacity());\n  1361:     /// ```",
    "nanvix_source": "  1340:     ///     output.try_reserve_exact(data.len())?;\n  1341:     ///\n  1342:     ///     // Now we know this can't OOM in the middle of our complex work\n  1343:     ///     output.push_str(data);\n  1344:     ///\n  1345:     ///     Ok(output)\n  1346:     /// }\n  1347:     /// # process_data(\"rust\").expect(\"why is the test harness OOMing on 4 bytes?\");\n  1348:     /// ```\n  1349:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1350:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1351:         self.vec.try_reserve_exact(additional)\n  1352:     }\n  1353: \n  1354:     /// Shrinks the capacity of this `String` to match its length.\n  1355:     ///\n  1356:     /// # Examples\n  1357:     ///\n  1358:     /// ```\n  1359:     /// let mut s = String::from(\"foo\");\n  1360:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::with_capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "with_capacity",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   468:     ///\n   469:     /// // These are all done without reallocating...\n   470:     /// let cap = s.capacity();\n   471:     /// for _ in 0..10 {\n   472:     ///     s.push('a');\n   473:     /// }\n   474:     ///\n   475:     /// assert_eq!(s.capacity(), cap);\n   476:     ///\n   477:     /// // ...but this may make the string reallocate\n   478:     /// s.push('a');\n   479:     /// ```\n   480:     #[cfg(not(no_global_oom_handling))]\n   481:     #[inline]\n   482:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   483:     #[must_use]\n   484:     pub fn with_capacity(capacity: usize) -> String {\n   485:         String { vec: Vec::with_capacity(capacity) }\n   486:     }\n   487: \n   488:     /// Creates a new empty `String` with at least the specified capacity.\n   489:     ///\n   490:     /// # Errors\n   491:     ///\n   492:     /// Returns [`Err`] if the capacity exceeds `isize::MAX` bytes,\n   493:     /// or if the memory allocator reports failure.\n   494:     ///\n   495:     #[inline]\n   496:     #[unstable(feature = \"try_with_capacity\", issue = \"91913\")]\n   497:     pub fn try_with_capacity(capacity: usize) -> Result<String, TryReserveError> {\n   498:         Ok(String { vec: Vec::try_with_capacity(capacity)? })\n   499:     }\n   500: ",
    "nanvix_source": "   483:     ///\n   484:     /// assert_eq!(s.capacity(), cap);\n   485:     ///\n   486:     /// // ...but this may make the string reallocate\n   487:     /// s.push('a');\n   488:     /// ```\n   489:     #[cfg(not(no_global_oom_handling))]\n   490:     #[inline]\n   491:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   492:     #[must_use]\n   493:     pub fn with_capacity(capacity: usize) -> String {\n   494:         String { vec: Vec::with_capacity(capacity) }\n   495:     }\n   496: \n   497:     /// Creates a new empty `String` with at least the specified capacity.\n   498:     ///\n   499:     /// # Errors\n   500:     ///\n   501:     /// Returns [`Err`] if the capacity exceeds `isize::MAX` bytes,\n   502:     /// or if the memory allocator reports failure.\n   503:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_unsafe": false
      },
      "name": "capacity",
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
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1430:     ///\n  1431:     /// A vector with zero-sized elements will always have a capacity of usize::MAX:\n  1432:     ///\n  1433:     /// ```\n  1434:     /// #[derive(Clone)]\n  1435:     /// struct ZeroSized;\n  1436:     ///\n  1437:     /// fn main() {\n  1438:     ///     assert_eq!(std::mem::size_of::<ZeroSized>(), 0);\n  1439:     ///     let v = vec![ZeroSized; 0];\n  1440:     ///     assert_eq!(v.capacity(), usize::MAX);\n  1441:     /// }\n  1442:     /// ```\n  1443:     #[inline]\n  1444:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1445:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1446:     pub const fn capacity(&self) -> usize {\n  1447:         self.buf.capacity()\n  1448:     }\n  1449: \n  1450:     /// Reserves capacity for at least `additional` more elements to be inserted\n  1451:     /// in the given `Vec<T>`. The collection may reserve more space to\n  1452:     /// speculatively avoid frequent reallocations. After calling `reserve`,\n  1453:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1454:     /// Does nothing if capacity is already sufficient.\n  1455:     ///\n  1456:     /// # Panics\n  1457:     ///\n  1458:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1459:     ///\n  1460:     /// # Examples\n  1461:     ///\n  1462:     /// ```",
    "nanvix_source": "  1434:     ///\n  1435:     /// fn main() {\n  1436:     ///     assert_eq!(std::mem::size_of::<ZeroSized>(), 0);\n  1437:     ///     let v = vec![ZeroSized; 0];\n  1438:     ///     assert_eq!(v.capacity(), usize::MAX);\n  1439:     /// }\n  1440:     /// ```\n  1441:     #[inline]\n  1442:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1443:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1444:     pub const fn capacity(&self) -> usize {\n  1445:         self.buf.capacity()\n  1446:     }\n  1447: \n  1448:     /// Reserves capacity for at least `additional` more elements to be inserted\n  1449:     /// in the given `Vec<T>`. The collection may reserve more space to\n  1450:     /// speculatively avoid frequent reallocations. After calling `reserve`,\n  1451:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1452:     /// Does nothing if capacity is already sufficient.\n  1453:     ///\n  1454:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "reserve_exact",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
        ],
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1484:     ///\n  1485:     /// [`reserve`]: Vec::reserve\n  1486:     ///\n  1487:     /// # Panics\n  1488:     ///\n  1489:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1490:     ///\n  1491:     /// # Examples\n  1492:     ///\n  1493:     /// ```\n  1494:     /// let mut vec = vec![1];\n  1495:     /// vec.reserve_exact(10);\n  1496:     /// assert!(vec.capacity() >= 11);\n  1497:     /// ```\n  1498:     #[cfg(not(no_global_oom_handling))]\n  1499:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1500:     pub fn reserve_exact(&mut self, additional: usize) {\n  1501:         self.buf.reserve_exact(self.len, additional);\n  1502:     }\n  1503: \n  1504:     /// Tries to reserve capacity for at least `additional` more elements to be inserted\n  1505:     /// in the given `Vec<T>`. The collection may reserve more space to speculatively avoid\n  1506:     /// frequent reallocations. After calling `try_reserve`, capacity will be\n  1507:     /// greater than or equal to `self.len() + additional` if it returns\n  1508:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1509:     /// preserves the contents even if an error occurs.\n  1510:     ///\n  1511:     /// # Errors\n  1512:     ///\n  1513:     /// If the capacity overflows, or the allocator reports a failure, then an error\n  1514:     /// is returned.\n  1515:     ///\n  1516:     /// # Examples",
    "nanvix_source": "  1488:     ///\n  1489:     /// # Examples\n  1490:     ///\n  1491:     /// ```\n  1492:     /// let mut vec = vec![1];\n  1493:     /// vec.reserve_exact(10);\n  1494:     /// assert!(vec.capacity() >= 11);\n  1495:     /// ```\n  1496:     #[cfg(not(no_global_oom_handling))]\n  1497:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1498:     pub fn reserve_exact(&mut self, additional: usize) {\n  1499:         self.buf.reserve_exact(self.len, additional);\n  1500:     }\n  1501: \n  1502:     /// Tries to reserve capacity for at least `additional` more elements to be inserted\n  1503:     /// in the given `Vec<T>`. The collection may reserve more space to speculatively avoid\n  1504:     /// frequent reallocations. After calling `try_reserve`, capacity will be\n  1505:     /// greater than or equal to `self.len() + additional` if it returns\n  1506:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1507:     /// preserves the contents even if an error occurs.\n  1508:     ///",
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
