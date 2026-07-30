For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::RefCell::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": false
      },
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1314:     /// [`forget()`]: mem::forget\n  1315:     /// [`undo_leak`]: RefCell::undo_leak()\n  1316:     ///\n  1317:     /// # Examples\n  1318:     ///\n  1319:     /// ```\n  1320:     /// use std::cell::RefCell;\n  1321:     ///\n  1322:     /// let mut c = RefCell::new(5);\n  1323:     /// *c.get_mut() += 1;\n  1324:     ///\n  1325:     /// assert_eq!(c, RefCell::new(6));\n  1326:     /// ```\n  1327:     #[inline]\n  1328:     #[stable(feature = \"cell_get_mut\", since = \"1.11.0\")]\n  1329:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1330:     pub const fn get_mut(&mut self) -> &mut T {\n  1331:         self.value.get_mut()\n  1332:     }\n  1333: \n  1334:     /// Undo the effect of leaked guards on the borrow state of the `RefCell`.\n  1335:     ///\n  1336:     /// This call is similar to [`get_mut`] but more specialized. It borrows `RefCell` mutably to\n  1337:     /// ensure no borrows exist and then resets the state tracking shared borrows. This is relevant\n  1338:     /// if some `Ref` or `RefMut` borrows have been leaked.\n  1339:     ///\n  1340:     /// [`get_mut`]: RefCell::get_mut()\n  1341:     ///\n  1342:     /// # Examples\n  1343:     ///\n  1344:     /// ```\n  1345:     /// #![feature(cell_leak)]\n  1346:     /// use std::cell::RefCell;",
    "nanvix_source": "  1320:     /// use std::cell::RefCell;\n  1321:     ///\n  1322:     /// let mut c = RefCell::new(5);\n  1323:     /// *c.get_mut() += 1;\n  1324:     ///\n  1325:     /// assert_eq!(c, RefCell::new(6));\n  1326:     /// ```\n  1327:     #[inline]\n  1328:     #[stable(feature = \"cell_get_mut\", since = \"1.11.0\")]\n  1329:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1330:     pub const fn get_mut(&mut self) -> &mut T {\n  1331:         self.value.get_mut()\n  1332:     }\n  1333: \n  1334:     /// Undo the effect of leaked guards on the borrow state of the `RefCell`.\n  1335:     ///\n  1336:     /// This call is similar to [`get_mut`] but more specialized. It borrows `RefCell` mutably to\n  1337:     /// ensure no borrows exist and then resets the state tracking shared borrows. This is relevant\n  1338:     /// if some `Ref` or `RefMut` borrows have been leaked.\n  1339:     ///\n  1340:     /// [`get_mut`]: RefCell::get_mut()",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::from_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": false
      },
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "value"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "value",
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
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
            }
          }
        }
      }
    },
    "verification_source": "  2401:     /// Converts from `&mut T` to `&mut UnsafeCell<T>`.\n  2402:     ///\n  2403:     /// # Examples\n  2404:     ///\n  2405:     /// ```\n  2406:     /// use std::cell::UnsafeCell;\n  2407:     ///\n  2408:     /// let mut val = 42;\n  2409:     /// let uc = UnsafeCell::from_mut(&mut val);\n  2410:     ///\n  2411:     /// *uc.get_mut() -= 1;\n  2412:     /// assert_eq!(*uc.get_mut(), 41);\n  2413:     /// ```\n  2414:     #[inline(always)]\n  2415:     #[stable(feature = \"unsafe_cell_from_mut\", since = \"1.84.0\")]\n  2416:     #[rustc_const_stable(feature = \"unsafe_cell_from_mut\", since = \"1.84.0\")]\n  2417:     pub const fn from_mut(value: &mut T) -> &mut UnsafeCell<T> {\n  2418:         // SAFETY: `UnsafeCell<T>` has the same memory layout as `T` due to #[repr(transparent)].\n  2419:         unsafe { &mut *(value as *mut T as *mut UnsafeCell<T>) }\n  2420:     }\n  2421: \n  2422:     /// Gets a mutable pointer to the wrapped value.\n  2423:     ///\n  2424:     /// This can be cast to a pointer of any kind. When creating references, you must uphold the\n  2425:     /// aliasing rules; see [the type-level docs][UnsafeCell#aliasing-rules] for more discussion and\n  2426:     /// caveats.\n  2427:     ///\n  2428:     /// # Examples\n  2429:     ///\n  2430:     /// ```\n  2431:     /// use std::cell::UnsafeCell;\n  2432:     ///\n  2433:     /// let uc = UnsafeCell::new(5);",
    "nanvix_source": "  2407:     ///\n  2408:     /// let mut val = 42;\n  2409:     /// let uc = UnsafeCell::from_mut(&mut val);\n  2410:     ///\n  2411:     /// *uc.get_mut() -= 1;\n  2412:     /// assert_eq!(*uc.get_mut(), 41);\n  2413:     /// ```\n  2414:     #[inline(always)]\n  2415:     #[stable(feature = \"unsafe_cell_from_mut\", since = \"1.84.0\")]\n  2416:     #[rustc_const_stable(feature = \"unsafe_cell_from_mut\", since = \"1.84.0\")]\n  2417:     pub const fn from_mut(value: &mut T) -> &mut UnsafeCell<T> {\n  2418:         // SAFETY: `UnsafeCell<T>` has the same memory layout as `T` due to #[repr(transparent)].\n  2419:         unsafe { &mut *(value as *mut T as *mut UnsafeCell<T>) }\n  2420:     }\n  2421: \n  2422:     /// Gets a mutable pointer to the wrapped value.\n  2423:     ///\n  2424:     /// This can be cast to a pointer of any kind. When creating (shared or mutable) references, you\n  2425:     /// must uphold the aliasing rules; see [the type-level docs][UnsafeCell#aliasing-rules] for\n  2426:     /// more discussion and caveats.\n  2427:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": false
      },
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2452:     /// This call borrows the `UnsafeCell` mutably (at compile-time) which\n  2453:     /// guarantees that we possess the only reference.\n  2454:     ///\n  2455:     /// # Examples\n  2456:     ///\n  2457:     /// ```\n  2458:     /// use std::cell::UnsafeCell;\n  2459:     ///\n  2460:     /// let mut c = UnsafeCell::new(5);\n  2461:     /// *c.get_mut() += 1;\n  2462:     ///\n  2463:     /// assert_eq!(*c.get_mut(), 6);\n  2464:     /// ```\n  2465:     #[inline(always)]\n  2466:     #[stable(feature = \"unsafe_cell_get_mut\", since = \"1.50.0\")]\n  2467:     #[rustc_const_stable(feature = \"const_unsafecell_get_mut\", since = \"1.83.0\")]\n  2468:     pub const fn get_mut(&mut self) -> &mut T {\n  2469:         &mut self.value\n  2470:     }\n  2471: \n  2472:     /// Gets a mutable pointer to the wrapped value.\n  2473:     /// The difference from [`get`] is that this function accepts a raw pointer,\n  2474:     /// which is useful to avoid the creation of temporary references.\n  2475:     ///\n  2476:     /// This can be cast to a pointer of any kind. When creating references, you must uphold the\n  2477:     /// aliasing rules; see [the type-level docs][UnsafeCell#aliasing-rules] for more discussion and\n  2478:     /// caveats.\n  2479:     ///\n  2480:     /// [`get`]: UnsafeCell::get()\n  2481:     ///\n  2482:     /// # Examples\n  2483:     ///\n  2484:     /// Gradual initialization of an `UnsafeCell` requires `raw_get`, as",
    "nanvix_source": "  2458:     /// use std::cell::UnsafeCell;\n  2459:     ///\n  2460:     /// let mut c = UnsafeCell::new(5);\n  2461:     /// *c.get_mut() += 1;\n  2462:     ///\n  2463:     /// assert_eq!(*c.get_mut(), 6);\n  2464:     /// ```\n  2465:     #[inline(always)]\n  2466:     #[stable(feature = \"unsafe_cell_get_mut\", since = \"1.50.0\")]\n  2467:     #[rustc_const_stable(feature = \"const_unsafecell_get_mut\", since = \"1.83.0\")]\n  2468:     pub const fn get_mut(&mut self) -> &mut T {\n  2469:         &mut self.value\n  2470:     }\n  2471: \n  2472:     /// Gets a mutable pointer to the wrapped value.\n  2473:     /// The difference from [`get`] is that this function accepts a raw pointer,\n  2474:     /// which is useful to avoid the creation of temporary references.\n  2475:     ///\n  2476:     /// This can be cast to a pointer of any kind. When creating (shared or mutable) references, you\n  2477:     /// must uphold the aliasing rules; see [the type-level docs][UnsafeCell#aliasing-rules] for\n  2478:     /// more discussion and caveats.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Peekable::peek_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "peek_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "I"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9889,
            "path": "Peekable"
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
                          "id": 82,
                          "path": "Iterator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "I"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:26006",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9889",
        "resolved_owner_path": [
          "core",
          "iter",
          "adapters",
          "peekable",
          "Peekable"
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Item",
                            "self_type": {
                              "generic": "I"
                            },
                            "trait": {
                              "args": null,
                              "id": 82,
                              "path": ""
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
    "verification_source": "   240:     /// // Like with `peek()`, we can see into the future without advancing the iterator.\n   241:     /// assert_eq!(iter.peek_mut(), Some(&mut &1));\n   242:     /// assert_eq!(iter.peek_mut(), Some(&mut &1));\n   243:     /// assert_eq!(iter.next(), Some(&1));\n   244:     ///\n   245:     /// // Peek into the iterator and set the value behind the mutable reference.\n   246:     /// if let Some(p) = iter.peek_mut() {\n   247:     ///     assert_eq!(*p, &2);\n   248:     ///     *p = &5;\n   249:     /// }\n   250:     ///\n   251:     /// // The value we put in reappears as the iterator continues.\n   252:     /// assert_eq!(iter.collect::<Vec<_>>(), vec![&5, &3]);\n   253:     /// ```\n   254:     #[inline]\n   255:     #[stable(feature = \"peekable_peek_mut\", since = \"1.53.0\")]\n   256:     pub fn peek_mut(&mut self) -> Option<&mut I::Item> {\n   257:         let iter = &mut self.iter;\n   258:         self.peeked.get_or_insert_with(|| iter.next()).as_mut()\n   259:     }\n   260: \n   261:     /// Consume and return the next value of this iterator if a condition is true.\n   262:     ///\n   263:     /// If `func` returns `true` for the next value of this iterator, consume and return it.\n   264:     /// Otherwise, return `None`.\n   265:     ///\n   266:     /// # Examples\n   267:     /// Consume a number if it's equal to 0.\n   268:     /// ```\n   269:     /// let mut iter = (0..5).peekable();\n   270:     /// // The first item of the iterator is 0; consume it.\n   271:     /// assert_eq!(iter.next_if(|&x| x == 0), Some(0));\n   272:     /// // The next item returned is now 1, so `next_if` will return `None`.",
    "nanvix_source": "   246:     /// if let Some(p) = iter.peek_mut() {\n   247:     ///     assert_eq!(*p, &2);\n   248:     ///     *p = &5;\n   249:     /// }\n   250:     ///\n   251:     /// // The value we put in reappears as the iterator continues.\n   252:     /// assert_eq!(iter.collect::<Vec<_>>(), vec![&5, &3]);\n   253:     /// ```\n   254:     #[inline]\n   255:     #[stable(feature = \"peekable_peek_mut\", since = \"1.53.0\")]\n   256:     pub fn peek_mut(&mut self) -> Option<&mut I::Item> {\n   257:         let iter = &mut self.iter;\n   258:         self.peeked.get_or_insert_with(|| iter.next()).as_mut()\n   259:     }\n   260: \n   261:     /// Consume and return the next value of this iterator if a condition is true.\n   262:     ///\n   263:     /// If `func` returns `true` for the next value of this iterator, consume and return it.\n   264:     /// Otherwise, return `None`.\n   265:     ///\n   266:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::MaybeUninit::write",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": false
      },
      "name": "write",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
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
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   557:     ///     pub fn capacity(&self) -> usize {\n   558:     ///         self.memory.len()\n   559:     ///     }\n   560:     ///     pub fn push(&mut self, val: T) -> Pin<&mut T> {\n   561:     ///         if self.len >= self.capacity() {\n   562:     ///             panic!(\"Attempted to push to a full pin arena!\");\n   563:     ///         }\n   564:     ///         let ref_ = self.memory[self.len].write(val);\n   565:     ///         self.len += 1;\n   566:     ///         unsafe { Pin::new_unchecked(ref_) }\n   567:     ///     }\n   568:     /// }\n   569:     /// ```\n   570:     #[inline(always)]\n   571:     #[stable(feature = \"maybe_uninit_write\", since = \"1.55.0\")]\n   572:     #[rustc_const_stable(feature = \"const_maybe_uninit_write\", since = \"1.85.0\")]\n   573:     pub const fn write(&mut self, val: T) -> &mut T {\n   574:         *self = MaybeUninit::new(val);\n   575:         // SAFETY: We just initialized this value.\n   576:         unsafe { self.assume_init_mut() }\n   577:     }\n   578: \n   579:     /// Gets a pointer to the contained value. Reading from this pointer or turning it\n   580:     /// into a reference is undefined behavior unless the `MaybeUninit<T>` is initialized.\n   581:     /// Writing to memory that this pointer (non-transitively) points to is undefined behavior\n   582:     /// (except inside an `UnsafeCell<T>`).\n   583:     ///\n   584:     /// # Examples\n   585:     ///\n   586:     /// Correct usage of this method:\n   587:     ///\n   588:     /// ```rust\n   589:     /// use std::mem::MaybeUninit;",
    "nanvix_source": "   564:     ///         }\n   565:     ///         let ref_ = self.memory[self.len].write(val);\n   566:     ///         self.len += 1;\n   567:     ///         unsafe { Pin::new_unchecked(ref_) }\n   568:     ///     }\n   569:     /// }\n   570:     /// ```\n   571:     #[inline(always)]\n   572:     #[stable(feature = \"maybe_uninit_write\", since = \"1.55.0\")]\n   573:     #[rustc_const_stable(feature = \"const_maybe_uninit_write\", since = \"1.85.0\")]\n   574:     pub const fn write(&mut self, val: T) -> &mut T {\n   575:         *self = MaybeUninit::new(val);\n   576:         // SAFETY: We just initialized this value.\n   577:         unsafe { self.assume_init_mut() }\n   578:     }\n   579: \n   580:     /// Gets a pointer to the contained value. Reading from this pointer or turning it\n   581:     /// into a reference is undefined behavior unless the `MaybeUninit<T>` is initialized.\n   582:     /// Writing to memory that this pointer (non-transitively) points to is undefined behavior\n   583:     /// (except inside an `UnsafeCell<T>`).\n   584:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::as_deref_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8650,
                      "path": "DerefMut"
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
      "name": "as_deref_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
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
    "verification_source": "  1398:     ///\n  1399:     /// Leaves the original `Option` in-place, creating a new one containing a mutable reference to\n  1400:     /// the inner type's [`Deref::Target`] type.\n  1401:     ///\n  1402:     /// # Examples\n  1403:     ///\n  1404:     /// ```\n  1405:     /// let mut x: Option<String> = Some(\"hey\".to_owned());\n  1406:     /// assert_eq!(x.as_deref_mut().map(|x| {\n  1407:     ///     x.make_ascii_uppercase();\n  1408:     ///     x\n  1409:     /// }), Some(\"HEY\".to_owned().as_mut_str()));\n  1410:     /// ```\n  1411:     #[inline]\n  1412:     #[stable(feature = \"option_deref\", since = \"1.40.0\")]\n  1413:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1414:     pub const fn as_deref_mut(&mut self) -> Option<&mut T::Target>\n  1415:     where\n  1416:         T: [const] DerefMut,\n  1417:     {\n  1418:         self.as_mut().map(DerefMut::deref_mut)\n  1419:     }\n  1420: \n  1421:     /////////////////////////////////////////////////////////////////////////\n  1422:     // Iterator constructors\n  1423:     /////////////////////////////////////////////////////////////////////////\n  1424: \n  1425:     /// Returns an iterator over the possibly contained value.\n  1426:     ///\n  1427:     /// # Examples\n  1428:     ///\n  1429:     /// ```\n  1430:     /// let x = Some(4);",
    "nanvix_source": "  1400:     /// ```\n  1401:     /// let mut x: Option<String> = Some(\"hey\".to_owned());\n  1402:     /// assert_eq!(x.as_deref_mut().map(|x| {\n  1403:     ///     x.make_ascii_uppercase();\n  1404:     ///     x\n  1405:     /// }), Some(\"HEY\".to_owned().as_mut_str()));\n  1406:     /// ```\n  1407:     #[inline]\n  1408:     #[stable(feature = \"option_deref\", since = \"1.40.0\")]\n  1409:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1410:     pub const fn as_deref_mut(&mut self) -> Option<&mut T::Target>\n  1411:     where\n  1412:         T: [const] DerefMut,\n  1413:     {\n  1414:         self.as_mut().map(DerefMut::deref_mut)\n  1415:     }\n  1416: \n  1417:     /////////////////////////////////////////////////////////////////////////\n  1418:     // Iterator constructors\n  1419:     /////////////////////////////////////////////////////////////////////////\n  1420: ",
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
