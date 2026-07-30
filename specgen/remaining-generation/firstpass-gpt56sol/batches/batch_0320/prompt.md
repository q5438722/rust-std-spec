For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::Cell::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_ptr",
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
            "id": 9785,
            "path": "Cell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24750",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9785",
        "resolved_owner_path": [
          "core",
          "cell",
          "Cell"
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   584:     /// Returns a raw pointer to the underlying data in this cell.\n   585:     ///\n   586:     /// # Examples\n   587:     ///\n   588:     /// ```\n   589:     /// use std::cell::Cell;\n   590:     ///\n   591:     /// let c = Cell::new(5);\n   592:     ///\n   593:     /// let ptr = c.as_ptr();\n   594:     /// ```\n   595:     #[inline]\n   596:     #[stable(feature = \"cell_as_ptr\", since = \"1.12.0\")]\n   597:     #[rustc_const_stable(feature = \"const_cell_as_ptr\", since = \"1.32.0\")]\n   598:     #[rustc_as_ptr]\n   599:     #[rustc_never_returns_null_ptr]\n   600:     pub const fn as_ptr(&self) -> *mut T {\n   601:         self.value.get()\n   602:     }\n   603: \n   604:     /// Returns a mutable reference to the underlying data.\n   605:     ///\n   606:     /// This call borrows `Cell` mutably (at compile-time) which guarantees\n   607:     /// that we possess the only reference.\n   608:     ///\n   609:     /// However be cautious: this method expects `self` to be mutable, which is\n   610:     /// generally not the case when using a `Cell`. If you require interior\n   611:     /// mutability by reference, consider using `RefCell` which provides\n   612:     /// run-time checked mutable borrows through its [`borrow_mut`] method.\n   613:     ///\n   614:     /// [`borrow_mut`]: RefCell::borrow_mut()\n   615:     ///\n   616:     /// # Examples",
    "nanvix_source": "   590:     ///\n   591:     /// let c = Cell::new(5);\n   592:     ///\n   593:     /// let ptr = c.as_ptr();\n   594:     /// ```\n   595:     #[inline]\n   596:     #[stable(feature = \"cell_as_ptr\", since = \"1.12.0\")]\n   597:     #[rustc_const_stable(feature = \"const_cell_as_ptr\", since = \"1.32.0\")]\n   598:     #[rustc_as_ptr]\n   599:     #[rustc_never_returns_null_ptr]\n   600:     pub const fn as_ptr(&self) -> *mut T {\n   601:         self.value.get()\n   602:     }\n   603: \n   604:     /// Returns a mutable reference to the underlying data.\n   605:     ///\n   606:     /// This call borrows `Cell` mutably (at compile-time) which guarantees\n   607:     /// that we possess the only reference.\n   608:     ///\n   609:     /// However be cautious: this method expects `self` to be mutable, which is\n   610:     /// generally not the case when using a `Cell`. If you require interior",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_ptr",
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
            "id": 9393,
            "path": "RefCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1276:     /// Returns a raw pointer to the underlying data in this cell.\n  1277:     ///\n  1278:     /// # Examples\n  1279:     ///\n  1280:     /// ```\n  1281:     /// use std::cell::RefCell;\n  1282:     ///\n  1283:     /// let c = RefCell::new(5);\n  1284:     ///\n  1285:     /// let ptr = c.as_ptr();\n  1286:     /// ```\n  1287:     #[inline]\n  1288:     #[stable(feature = \"cell_as_ptr\", since = \"1.12.0\")]\n  1289:     #[rustc_as_ptr]\n  1290:     #[rustc_never_returns_null_ptr]\n  1291:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1292:     pub const fn as_ptr(&self) -> *mut T {\n  1293:         self.value.get()\n  1294:     }\n  1295: \n  1296:     /// Returns a mutable reference to the underlying data.\n  1297:     ///\n  1298:     /// Since this method borrows `RefCell` mutably, it is statically guaranteed\n  1299:     /// that no borrows to the underlying data exist. The dynamic checks inherent\n  1300:     /// in [`borrow_mut`] and most other methods of `RefCell` are therefore\n  1301:     /// unnecessary. Note that this method does not reset the borrowing state if borrows were previously leaked\n  1302:     /// (e.g., via [`forget()`] on a [`Ref`] or [`RefMut`]). For that purpose,\n  1303:     /// consider using the unstable [`undo_leak`] method.\n  1304:     ///\n  1305:     /// This method can only be called if `RefCell` can be mutably borrowed,\n  1306:     /// which in general is only the case directly after the `RefCell` has\n  1307:     /// been created. In these situations, skipping the aforementioned dynamic\n  1308:     /// borrowing checks may yield better ergonomics and runtime-performance.",
    "nanvix_source": "  1282:     ///\n  1283:     /// let c = RefCell::new(5);\n  1284:     ///\n  1285:     /// let ptr = c.as_ptr();\n  1286:     /// ```\n  1287:     #[inline]\n  1288:     #[stable(feature = \"cell_as_ptr\", since = \"1.12.0\")]\n  1289:     #[rustc_as_ptr]\n  1290:     #[rustc_never_returns_null_ptr]\n  1291:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1292:     pub const fn as_ptr(&self) -> *mut T {\n  1293:         self.value.get()\n  1294:     }\n  1295: \n  1296:     /// Returns a mutable reference to the underlying data.\n  1297:     ///\n  1298:     /// Since this method borrows `RefCell` mutably, it is statically guaranteed\n  1299:     /// that no borrows to the underlying data exist. The dynamic checks inherent\n  1300:     /// in [`borrow_mut`] and most other methods of `RefCell` are therefore\n  1301:     /// unnecessary. Note that this method does not reset the borrowing state if borrows were previously leaked\n  1302:     /// (e.g., via [`forget()`] on a [`Ref`] or [`RefMut`]). For that purpose,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::try_borrow_unguarded",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
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
        "is_unsafe": true
      },
      "name": "try_borrow_unguarded",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
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
            "id": 9393,
            "path": "RefCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 12904,
                        "path": "BorrowError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1376:     ///\n  1377:     /// let c = RefCell::new(5);\n  1378:     ///\n  1379:     /// {\n  1380:     ///     let m = c.borrow_mut();\n  1381:     ///     assert!(unsafe { c.try_borrow_unguarded() }.is_err());\n  1382:     /// }\n  1383:     ///\n  1384:     /// {\n  1385:     ///     let m = c.borrow();\n  1386:     ///     assert!(unsafe { c.try_borrow_unguarded() }.is_ok());\n  1387:     /// }\n  1388:     /// ```\n  1389:     #[stable(feature = \"borrow_state\", since = \"1.37.0\")]\n  1390:     #[inline]\n  1391:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1392:     pub const unsafe fn try_borrow_unguarded(&self) -> Result<&T, BorrowError> {\n  1393:         if !is_writing(self.borrow.get()) {\n  1394:             // SAFETY: We check that nobody is actively writing now, but it is\n  1395:             // the caller's responsibility to ensure that nobody writes until\n  1396:             // the returned reference is no longer in use.\n  1397:             // Also, `self.value.get()` refers to the value owned by `self`\n  1398:             // and is thus guaranteed to be valid for the lifetime of `self`.\n  1399:             Ok(unsafe { &*self.value.get() })\n  1400:         } else {\n  1401:             Err(BorrowError {\n  1402:                 // If a borrow occurred, then we must already have an outstanding borrow,\n  1403:                 // so `borrowed_at` will be `Some`\n  1404:                 #[cfg(feature = \"debug_refcell\")]\n  1405:                 location: self.borrowed_at.get().unwrap(),\n  1406:             })\n  1407:         }\n  1408:     }",
    "nanvix_source": "  1382:     /// }\n  1383:     ///\n  1384:     /// {\n  1385:     ///     let m = c.borrow();\n  1386:     ///     assert!(unsafe { c.try_borrow_unguarded() }.is_ok());\n  1387:     /// }\n  1388:     /// ```\n  1389:     #[stable(feature = \"borrow_state\", since = \"1.37.0\")]\n  1390:     #[inline]\n  1391:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1392:     pub const unsafe fn try_borrow_unguarded(&self) -> Result<&T, BorrowError> {\n  1393:         if !is_writing(self.borrow.get()) {\n  1394:             // SAFETY: We check that nobody is actively writing now, but it is\n  1395:             // the caller's responsibility to ensure that nobody writes until\n  1396:             // the returned reference is no longer in use.\n  1397:             // Also, `self.value.get()` refers to the value owned by `self`\n  1398:             // and is thus guaranteed to be valid for the lifetime of `self`.\n  1399:             Ok(unsafe { &*self.value.get() })\n  1400:         } else {\n  1401:             Err(BorrowError {\n  1402:                 // If a borrow occurred, then we must already have an outstanding borrow,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::get",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "get",
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
            "id": 9473,
            "path": "UnsafeCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24893",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9473",
        "resolved_owner_path": [
          "core",
          "cell",
          "UnsafeCell"
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2427:     ///\n  2428:     /// # Examples\n  2429:     ///\n  2430:     /// ```\n  2431:     /// use std::cell::UnsafeCell;\n  2432:     ///\n  2433:     /// let uc = UnsafeCell::new(5);\n  2434:     ///\n  2435:     /// let five = uc.get();\n  2436:     /// ```\n  2437:     #[inline(always)]\n  2438:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2439:     #[rustc_const_stable(feature = \"const_unsafecell_get\", since = \"1.32.0\")]\n  2440:     #[rustc_as_ptr]\n  2441:     #[rustc_never_returns_null_ptr]\n  2442:     #[rustc_should_not_be_called_on_const_items]\n  2443:     pub const fn get(&self) -> *mut T {\n  2444:         // We can just cast the pointer from `UnsafeCell<T>` to `T` because of\n  2445:         // #[repr(transparent)]. This exploits std's special status, there is\n  2446:         // no guarantee for user code that this will work in future versions of the compiler!\n  2447:         self as *const UnsafeCell<T> as *const T as *mut T\n  2448:     }\n  2449: \n  2450:     /// Returns a mutable reference to the underlying data.\n  2451:     ///\n  2452:     /// This call borrows the `UnsafeCell` mutably (at compile-time) which\n  2453:     /// guarantees that we possess the only reference.\n  2454:     ///\n  2455:     /// # Examples\n  2456:     ///\n  2457:     /// ```\n  2458:     /// use std::cell::UnsafeCell;\n  2459:     ///",
    "nanvix_source": "  2433:     /// let uc = UnsafeCell::new(5);\n  2434:     ///\n  2435:     /// let five = uc.get();\n  2436:     /// ```\n  2437:     #[inline(always)]\n  2438:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2439:     #[rustc_const_stable(feature = \"const_unsafecell_get\", since = \"1.32.0\")]\n  2440:     #[rustc_as_ptr]\n  2441:     #[rustc_never_returns_null_ptr]\n  2442:     #[rustc_should_not_be_called_on_const_items]\n  2443:     pub const fn get(&self) -> *mut T {\n  2444:         // We can just cast the pointer from `UnsafeCell<T>` to `T` because of\n  2445:         // #[repr(transparent)]. This exploits std's special status, there is\n  2446:         // no guarantee for user code that this will work in future versions of the compiler!\n  2447:         self as *const UnsafeCell<T> as *const T as *mut T\n  2448:     }\n  2449: \n  2450:     /// Returns a mutable reference to the underlying data.\n  2451:     ///\n  2452:     /// This call borrows the `UnsafeCell` mutably (at compile-time) which\n  2453:     /// guarantees that we possess the only reference.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::raw_get",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "raw_get",
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
            "id": 9473,
            "path": "UnsafeCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:24893",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9473",
        "resolved_owner_path": [
          "core",
          "cell",
          "UnsafeCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "Self"
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
    "verification_source": "  2487:     /// ```\n  2488:     /// use std::cell::UnsafeCell;\n  2489:     /// use std::mem::MaybeUninit;\n  2490:     ///\n  2491:     /// let m = MaybeUninit::<UnsafeCell<i32>>::uninit();\n  2492:     /// unsafe { UnsafeCell::raw_get(m.as_ptr()).write(5); }\n  2493:     /// // avoid below which references to uninitialized data\n  2494:     /// // unsafe { UnsafeCell::get(&*m.as_ptr()).write(5); }\n  2495:     /// let uc = unsafe { m.assume_init() };\n  2496:     ///\n  2497:     /// assert_eq!(uc.into_inner(), 5);\n  2498:     /// ```\n  2499:     #[inline(always)]\n  2500:     #[stable(feature = \"unsafe_cell_raw_get\", since = \"1.56.0\")]\n  2501:     #[rustc_const_stable(feature = \"unsafe_cell_raw_get\", since = \"1.56.0\")]\n  2502:     #[rustc_diagnostic_item = \"unsafe_cell_raw_get\"]\n  2503:     pub const fn raw_get(this: *const Self) -> *mut T {\n  2504:         // We can just cast the pointer from `UnsafeCell<T>` to `T` because of\n  2505:         // #[repr(transparent)]. This exploits std's special status, there is\n  2506:         // no guarantee for user code that this will work in future versions of the compiler!\n  2507:         this as *const T as *mut T\n  2508:     }\n  2509: \n  2510:     /// Get a shared reference to the value within the `UnsafeCell`.\n  2511:     ///\n  2512:     /// # Safety\n  2513:     ///\n  2514:     /// - It is Undefined Behavior to call this while any mutable\n  2515:     ///   reference to the wrapped value is alive.\n  2516:     /// - Mutating the wrapped value while the returned\n  2517:     ///   reference is alive is Undefined Behavior.\n  2518:     ///\n  2519:     /// # Examples",
    "nanvix_source": "  2493:     /// // avoid below which references to uninitialized data\n  2494:     /// // unsafe { UnsafeCell::get(&*m.as_ptr()).write(5); }\n  2495:     /// let uc = unsafe { m.assume_init() };\n  2496:     ///\n  2497:     /// assert_eq!(uc.into_inner(), 5);\n  2498:     /// ```\n  2499:     #[inline(always)]\n  2500:     #[stable(feature = \"unsafe_cell_raw_get\", since = \"1.56.0\")]\n  2501:     #[rustc_const_stable(feature = \"unsafe_cell_raw_get\", since = \"1.56.0\")]\n  2502:     #[rustc_diagnostic_item = \"unsafe_cell_raw_get\"]\n  2503:     pub const fn raw_get(this: *const Self) -> *mut T {\n  2504:         // We can just cast the pointer from `UnsafeCell<T>` to `T` because of\n  2505:         // #[repr(transparent)]. This exploits std's special status, there is\n  2506:         // no guarantee for user code that this will work in future versions of the compiler!\n  2507:         this as *const T as *mut T\n  2508:     }\n  2509: \n  2510:     /// Get a shared reference to the value within the `UnsafeCell`.\n  2511:     ///\n  2512:     /// # Safety\n  2513:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_ptr",
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
          "resolved_path": {
            "args": null,
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 25237,
                "path": "c_char"
              }
            }
          }
        }
      }
    },
    "verification_source": "   467:     /// To fix the problem, bind the `CString` to a local variable:\n   468:     ///\n   469:     /// ```\n   470:     /// use std::ffi::{CStr, CString};\n   471:     ///\n   472:     /// let c_str = CString::new(\"Hi!\".to_uppercase()).unwrap();\n   473:     /// let ptr = c_str.as_ptr();\n   474:     ///\n   475:     /// assert_eq!(unsafe { CStr::from_ptr(ptr) }, c\"HI!\");\n   476:     /// ```\n   477:     #[inline]\n   478:     #[must_use]\n   479:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   480:     #[rustc_const_stable(feature = \"const_str_as_ptr\", since = \"1.32.0\")]\n   481:     #[rustc_as_ptr]\n   482:     #[rustc_never_returns_null_ptr]\n   483:     pub const fn as_ptr(&self) -> *const c_char {\n   484:         self.inner.as_ptr()\n   485:     }\n   486: \n   487:     /// We could eventually expose this publicly, if we wanted.\n   488:     #[inline]\n   489:     #[must_use]\n   490:     const fn as_non_null_ptr(&self) -> NonNull<c_char> {\n   491:         // FIXME(const_trait_impl) replace with `NonNull::from`\n   492:         // SAFETY: a reference is never null\n   493:         unsafe { NonNull::new_unchecked(&self.inner as *const [c_char] as *mut [c_char]) }\n   494:             .as_non_null_ptr()\n   495:     }\n   496: \n   497:     /// Returns the length of `self`. Like C's `strlen`, this does not include the nul terminator.\n   498:     ///\n   499:     /// > **Note**: This method is currently implemented as a constant-time",
    "nanvix_source": "   474:     /// let ptr = c_str.as_ptr();\n   475:     ///\n   476:     /// assert_eq!(unsafe { CStr::from_ptr(ptr) }, c\"HI!\");\n   477:     /// ```\n   478:     #[inline]\n   479:     #[must_use]\n   480:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   481:     #[rustc_const_stable(feature = \"const_str_as_ptr\", since = \"1.32.0\")]\n   482:     #[rustc_as_ptr]\n   483:     #[rustc_never_returns_null_ptr]\n   484:     pub const fn as_ptr(&self) -> *const c_char {\n   485:         self.inner.as_ptr()\n   486:     }\n   487: \n   488:     /// We could eventually expose this publicly, if we wanted.\n   489:     #[inline]\n   490:     #[must_use]\n   491:     const fn as_non_null_ptr(&self) -> NonNull<c_char> {\n   492:         // FIXME(const_trait_impl) replace with `NonNull::from`\n   493:         // SAFETY: a reference is never null\n   494:         unsafe { NonNull::new_unchecked(&self.inner as *const [c_char] as *mut [c_char]) }",
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
