For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::pin::Pin::into_inner_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
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
        "is_unsafe": true
      },
      "name": "into_inner_unchecked",
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
                      "generic": "Ptr"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
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
                          "id": 8635,
                          "path": "Deref"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29040",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "pin",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "generic": "Ptr"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 9981,
                "path": "Pin"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Ptr"
        }
      }
    },
    "verification_source": "  1496:     /// the invariants on the `Pin` type can be upheld. If the code using the\n  1497:     /// resulting `Ptr` does not continue to maintain the pinning invariants that\n  1498:     /// is a violation of the API contract and may lead to undefined behavior in\n  1499:     /// later (safe) operations.\n  1500:     ///\n  1501:     /// Note that you must be able to guarantee that the data pointed to by `Ptr`\n  1502:     /// will be treated as pinned all the way until its `drop` handler is complete!\n  1503:     ///\n  1504:     /// *For more information, see the [`pin` module docs][self]*\n  1505:     ///\n  1506:     /// If the underlying data is [`Unpin`], [`Pin::into_inner`] should be used\n  1507:     /// instead.\n  1508:     #[inline(always)]\n  1509:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1510:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1511:     #[stable(feature = \"pin_into_inner\", since = \"1.39.0\")]\n  1512:     pub const unsafe fn into_inner_unchecked(pin: Pin<Ptr>) -> Ptr {\n  1513:         pin.pointer\n  1514:     }\n  1515: }\n  1516: \n  1517: impl<'a, T: ?Sized> Pin<&'a T> {\n  1518:     /// Constructs a new pin by mapping the interior value.\n  1519:     ///\n  1520:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1521:     /// you could use this to get access to that field in one line of code.\n  1522:     /// However, there are several gotchas with these \"pinning projections\";\n  1523:     /// see the [`pin` module] documentation for further details on that topic.\n  1524:     ///\n  1525:     /// # Safety\n  1526:     ///\n  1527:     /// This function is unsafe. You must guarantee that the data you return\n  1528:     /// will not move so long as the argument value does not move (for example,",
    "nanvix_source": "  1502:     /// will be treated as pinned all the way until its `drop` handler is complete!\n  1503:     ///\n  1504:     /// *For more information, see the [`pin` module docs][self]*\n  1505:     ///\n  1506:     /// If the underlying data is [`Unpin`], [`Pin::into_inner`] should be used\n  1507:     /// instead.\n  1508:     #[inline(always)]\n  1509:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1510:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1511:     #[stable(feature = \"pin_into_inner\", since = \"1.39.0\")]\n  1512:     pub const unsafe fn into_inner_unchecked(pin: Pin<Ptr>) -> Ptr {\n  1513:         pin.pointer\n  1514:     }\n  1515: }\n  1516: \n  1517: impl<'a, T: ?Sized> Pin<&'a T> {\n  1518:     /// Constructs a new pin by mapping the interior value.\n  1519:     ///\n  1520:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1521:     /// you could use this to get access to that field in one line of code.\n  1522:     /// However, there are several gotchas with these \"pinning projections\";",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::map_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
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
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          },
          {
            "bound_predicate": {
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "borrowed_ref": {
                              "is_mutable": false,
                              "lifetime": null,
                              "type": {
                                "generic": "U"
                              }
                            }
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
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
      "name": "map_unchecked",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": "'a",
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            },
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
        "impl_id": "core:29043",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
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
            "func",
            {
              "generic": "F"
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
                        "lifetime": "'a",
                        "type": {
                          "generic": "U"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "  1518:     /// Constructs a new pin by mapping the interior value.\n  1519:     ///\n  1520:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1521:     /// you could use this to get access to that field in one line of code.\n  1522:     /// However, there are several gotchas with these \"pinning projections\";\n  1523:     /// see the [`pin` module] documentation for further details on that topic.\n  1524:     ///\n  1525:     /// # Safety\n  1526:     ///\n  1527:     /// This function is unsafe. You must guarantee that the data you return\n  1528:     /// will not move so long as the argument value does not move (for example,\n  1529:     /// because it is one of the fields of that value), and also that you do\n  1530:     /// not move out of the argument you receive to the interior function.\n  1531:     ///\n  1532:     /// [`pin` module]: self#projections-and-structural-pinning\n  1533:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1534:     pub unsafe fn map_unchecked<U, F>(self, func: F) -> Pin<&'a U>\n  1535:     where\n  1536:         U: ?Sized,\n  1537:         F: FnOnce(&T) -> &U,\n  1538:     {\n  1539:         let pointer = &*self.pointer;\n  1540:         let new_pointer = func(pointer);\n  1541: \n  1542:         // SAFETY: the safety contract for `new_unchecked` must be\n  1543:         // upheld by the caller.\n  1544:         unsafe { Pin::new_unchecked(new_pointer) }\n  1545:     }\n  1546: \n  1547:     /// Gets a shared reference out of a pin.\n  1548:     ///\n  1549:     /// This is safe because it is not possible to move out of a shared reference.\n  1550:     /// It may seem like there is an issue here with interior mutability: in fact,",
    "nanvix_source": "  1524:     ///\n  1525:     /// # Safety\n  1526:     ///\n  1527:     /// This function is unsafe. You must guarantee that the data you return\n  1528:     /// will not move so long as the argument value does not move (for example,\n  1529:     /// because it is one of the fields of that value), and also that you do\n  1530:     /// not move out of the argument you receive to the interior function.\n  1531:     ///\n  1532:     /// [`pin` module]: self#projections-and-structural-pinning\n  1533:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1534:     pub unsafe fn map_unchecked<U, F>(self, func: F) -> Pin<&'a U>\n  1535:     where\n  1536:         U: ?Sized,\n  1537:         F: FnOnce(&T) -> &U,\n  1538:     {\n  1539:         let pointer = &*self.pointer;\n  1540:         let new_pointer = func(pointer);\n  1541: \n  1542:         // SAFETY: the safety contract for `new_unchecked` must be\n  1543:         // upheld by the caller.\n  1544:         unsafe { Pin::new_unchecked(new_pointer) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::new_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
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
        "is_unsafe": true
      },
      "name": "new_unchecked",
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
                      "generic": "Ptr"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
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
                          "id": 8635,
                          "path": "Deref"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29034",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "pointer",
            {
              "generic": "Ptr"
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
                      "generic": "Ptr"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "  1331:     ///     // Call the closure, so the future can assume it has been pinned.\n  1332:     ///     closure();\n  1333:     ///     // Move the closure somewhere else.\n  1334:     ///     let mut moved = closure;\n  1335:     ///     // Calling it again here is fine (except that we might be polling a future that already\n  1336:     ///     // returned `Poll::Ready`, but that is a separate problem).\n  1337:     ///     moved();\n  1338:     /// }\n  1339:     /// ```\n  1340:     ///\n  1341:     /// [`mem::swap`]: crate::mem::swap\n  1342:     /// [`pin` module docs]: self\n  1343:     #[lang = \"new_unchecked\"]\n  1344:     #[inline(always)]\n  1345:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1346:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1347:     pub const unsafe fn new_unchecked(pointer: Ptr) -> Pin<Ptr> {\n  1348:         Pin { pointer }\n  1349:     }\n  1350: \n  1351:     /// Gets a shared reference to the pinned value this [`Pin`] points to.\n  1352:     ///\n  1353:     /// This is a generic method to go from `&Pin<Pointer<T>>` to `Pin<&T>`.\n  1354:     /// It is safe because, as part of the contract of `Pin::new_unchecked`,\n  1355:     /// the pointee cannot move after `Pin<Pointer<T>>` got created.\n  1356:     /// \"Malicious\" implementations of `Pointer::Deref` are likewise\n  1357:     /// ruled out by the contract of `Pin::new_unchecked`.\n  1358:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1359:     #[inline(always)]\n  1360:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1361:     pub const fn as_ref(&self) -> Pin<&Ptr::Target>\n  1362:     where\n  1363:         Ptr: [const] Deref,",
    "nanvix_source": "  1337:     ///     moved();\n  1338:     /// }\n  1339:     /// ```\n  1340:     ///\n  1341:     /// [`mem::swap`]: crate::mem::swap\n  1342:     /// [`pin` module docs]: self\n  1343:     #[lang = \"new_unchecked\"]\n  1344:     #[inline(always)]\n  1345:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1346:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1347:     pub const unsafe fn new_unchecked(pointer: Ptr) -> Pin<Ptr> {\n  1348:         Pin { pointer }\n  1349:     }\n  1350: \n  1351:     /// Gets a shared reference to the pinned value this [`Pin`] points to.\n  1352:     ///\n  1353:     /// This is a generic method to go from `&Pin<Pointer<T>>` to `Pin<&T>`.\n  1354:     /// It is safe because, as part of the contract of `Pin::new_unchecked`,\n  1355:     /// the pointee cannot move after `Pin<Pointer<T>>` got created.\n  1356:     /// \"Malicious\" implementations of `Pointer::Deref` are likewise\n  1357:     /// ruled out by the contract of `Pin::new_unchecked`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::add",
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
    "verification_source": "   635:     /// ```\n   636:     /// use std::ptr::NonNull;\n   637:     ///\n   638:     /// let s: &str = \"123\";\n   639:     /// let ptr: NonNull<u8> = NonNull::new(s.as_ptr().cast_mut()).unwrap();\n   640:     ///\n   641:     /// unsafe {\n   642:     ///     println!(\"{}\", ptr.add(1).read() as char);\n   643:     ///     println!(\"{}\", ptr.add(2).read() as char);\n   644:     /// }\n   645:     /// ```\n   646:     #[inline(always)]\n   647:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   648:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   649:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   650:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   651:     pub const unsafe fn add(self, count: usize) -> Self\n   652:     where\n   653:         T: Sized,\n   654:     {\n   655:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   656:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   657:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   658:         // construct `NonNull`.\n   659:         unsafe { transmute(intrinsics::offset(self.as_ptr(), count)) }\n   660:     }\n   661: \n   662:     /// Calculates the offset from a pointer in bytes (convenience for `.byte_offset(count as isize)`).\n   663:     ///\n   664:     /// `count` is in units of bytes.\n   665:     ///\n   666:     /// This is purely a convenience for casting to a `u8` pointer and\n   667:     /// using [`add`][NonNull::add] on it. See that method for documentation",
    "nanvix_source": "   596:     /// unsafe {\n   597:     ///     println!(\"{}\", ptr.add(1).read() as char);\n   598:     ///     println!(\"{}\", ptr.add(2).read() as char);\n   599:     /// }\n   600:     /// ```\n   601:     #[inline(always)]\n   602:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   603:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   604:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   605:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   606:     pub const unsafe fn add(self, count: usize) -> Self\n   607:     where\n   608:         T: Sized,\n   609:     {\n   610:         // SAFETY: the caller must uphold the safety contract for `offset`.\n   611:         // Additionally safety contract of `offset` guarantees that the resulting pointer is\n   612:         // pointing to an allocation, there can't be an allocation at null, thus it's safe to\n   613:         // construct `NonNull`.\n   614:         unsafe { transmute(intrinsics::offset(self.as_ptr(), count)) }\n   615:     }\n   616: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   385:     ///\n   386:     /// let mut x = 0u32;\n   387:     /// let ptr = NonNull::new(&mut x).expect(\"ptr is null!\");\n   388:     ///\n   389:     /// let x_value = unsafe { *ptr.as_ptr() };\n   390:     /// assert_eq!(x_value, 0);\n   391:     ///\n   392:     /// unsafe { *ptr.as_ptr() += 2; }\n   393:     /// let x_value = unsafe { *ptr.as_ptr() };\n   394:     /// assert_eq!(x_value, 2);\n   395:     /// ```\n   396:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   397:     #[rustc_const_stable(feature = \"const_nonnull_as_ptr\", since = \"1.32.0\")]\n   398:     #[rustc_never_returns_null_ptr]\n   399:     #[must_use]\n   400:     #[inline(always)]\n   401:     pub const fn as_ptr(self) -> *mut T {\n   402:         // This is a transmute for the same reasons as `NonZero::get`.\n   403: \n   404:         // SAFETY: `NonNull` is `transparent` over a `*const T`, and `*const T`\n   405:         // and `*mut T` have the same layout, so transitively we can transmute\n   406:         // our `NonNull` to a `*mut T` directly.\n   407:         unsafe { mem::transmute::<Self, *mut T>(self) }\n   408:     }\n   409: \n   410:     /// Returns a shared reference to the value. If the value may be uninitialized, [`as_uninit_ref`]\n   411:     /// must be used instead.\n   412:     ///\n   413:     /// For the mutable counterpart see [`as_mut`].\n   414:     ///\n   415:     /// [`as_uninit_ref`]: NonNull::as_uninit_ref\n   416:     /// [`as_mut`]: NonNull::as_mut\n   417:     ///",
    "nanvix_source": "   388:     ///\n   389:     /// unsafe { *ptr.as_ptr() += 2; }\n   390:     /// let x_value = unsafe { *ptr.as_ptr() };\n   391:     /// assert_eq!(x_value, 2);\n   392:     /// ```\n   393:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   394:     #[rustc_const_stable(feature = \"const_nonnull_as_ptr\", since = \"1.32.0\")]\n   395:     #[rustc_never_returns_null_ptr]\n   396:     #[must_use]\n   397:     #[inline(always)]\n   398:     pub const fn as_ptr(self) -> *mut T {\n   399:         // This is a transmute for the same reasons as `NonZero::get`.\n   400: \n   401:         // SAFETY: `NonNull` is `transparent` over a `*const T`, and `*const T`\n   402:         // and `*mut T` have the same layout, so transitively we can transmute\n   403:         // our `NonNull` to a `*mut T` directly.\n   404:         unsafe { mem::transmute::<Self, *mut T>(self) }\n   405:     }\n   406: \n   407:     /// Returns a shared reference to the value. If the value may be uninitialized, [`as_uninit_ref`]\n   408:     /// must be used instead.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::as_ref",
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
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
      "name": "as_ref",
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   424:     ///\n   425:     /// ```\n   426:     /// use std::ptr::NonNull;\n   427:     ///\n   428:     /// let mut x = 0u32;\n   429:     /// let ptr = NonNull::new(&mut x as *mut _).expect(\"ptr is null!\");\n   430:     ///\n   431:     /// let ref_x = unsafe { ptr.as_ref() };\n   432:     /// println!(\"{ref_x}\");\n   433:     /// ```\n   434:     ///\n   435:     /// [the module documentation]: crate::ptr#safety\n   436:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   437:     #[rustc_const_stable(feature = \"const_nonnull_as_ref\", since = \"1.73.0\")]\n   438:     #[must_use]\n   439:     #[inline(always)]\n   440:     pub const unsafe fn as_ref<'a>(&self) -> &'a T {\n   441:         // SAFETY: the caller must guarantee that `self` meets all the\n   442:         // requirements for a reference.\n   443:         // `cast_const` avoids a mutable raw pointer deref.\n   444:         unsafe { &*self.as_ptr().cast_const() }\n   445:     }\n   446: \n   447:     /// Returns a unique reference to the value. If the value may be uninitialized, [`as_uninit_mut`]\n   448:     /// must be used instead.\n   449:     ///\n   450:     /// For the shared counterpart see [`as_ref`].\n   451:     ///\n   452:     /// [`as_uninit_mut`]: NonNull::as_uninit_mut\n   453:     /// [`as_ref`]: NonNull::as_ref\n   454:     ///\n   455:     /// # Safety\n   456:     ///",
    "nanvix_source": "   427:     ///\n   428:     /// let ref_x = unsafe { ptr.as_ref() };\n   429:     /// println!(\"{ref_x}\");\n   430:     /// ```\n   431:     ///\n   432:     /// [the module documentation]: crate::ptr#safety\n   433:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   434:     #[rustc_const_stable(feature = \"const_nonnull_as_ref\", since = \"1.73.0\")]\n   435:     #[must_use]\n   436:     #[inline(always)]\n   437:     pub const unsafe fn as_ref<'a>(&self) -> &'a T {\n   438:         // SAFETY: the caller must guarantee that `self` meets all the\n   439:         // requirements for a reference.\n   440:         // `cast_const` avoids a mutable raw pointer deref.\n   441:         unsafe { &*self.as_ptr().cast_const() }\n   442:     }\n   443: \n   444:     /// Returns a unique reference to the value. If the value may be uninitialized, [`as_uninit_mut`]\n   445:     /// must be used instead.\n   446:     ///\n   447:     /// For the shared counterpart see [`as_ref`].",
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
