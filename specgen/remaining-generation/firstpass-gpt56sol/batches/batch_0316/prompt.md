For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::rc::Rc::increment_strong_count",
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
        "is_unsafe": true
      },
      "name": "increment_strong_count",
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
            "id": 302,
            "path": "Rc"
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
                          "id": 29,
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
        "impl_id": "alloc:3598",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
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
        "output": null
      }
    },
    "verification_source": "  1547:     /// use std::rc::Rc;\n  1548:     ///\n  1549:     /// let five = Rc::new(5);\n  1550:     ///\n  1551:     /// unsafe {\n  1552:     ///     let ptr = Rc::into_raw(five);\n  1553:     ///     Rc::increment_strong_count(ptr);\n  1554:     ///\n  1555:     ///     let five = Rc::from_raw(ptr);\n  1556:     ///     assert_eq!(2, Rc::strong_count(&five));\n  1557:     /// #   // Prevent leaks for Miri.\n  1558:     /// #   Rc::decrement_strong_count(ptr);\n  1559:     /// }\n  1560:     /// ```\n  1561:     #[inline]\n  1562:     #[stable(feature = \"rc_mutate_strong_count\", since = \"1.53.0\")]\n  1563:     pub unsafe fn increment_strong_count(ptr: *const T) {\n  1564:         unsafe { Self::increment_strong_count_in(ptr, Global) }\n  1565:     }\n  1566: \n  1567:     /// Decrements the strong reference count on the `Rc<T>` associated with the\n  1568:     /// provided pointer by one.\n  1569:     ///\n  1570:     /// # Safety\n  1571:     ///\n  1572:     /// The pointer must have been obtained through `Rc::into_raw`and must satisfy the\n  1573:     /// same layout requirements specified in [`Rc::from_raw_in`][from_raw_in].\n  1574:     /// The associated `Rc` instance must be valid (i.e. the strong count must be at\n  1575:     /// least 1) when invoking this method, and `ptr` must point to a block of memory\n  1576:     /// allocated by the global allocator. This method can be used to release the final `Rc` and\n  1577:     /// backing storage, but **should not** be called after the final `Rc` has been released.\n  1578:     ///\n  1579:     /// [from_raw_in]: Rc::from_raw_in",
    "nanvix_source": "  1559:     ///     Rc::increment_strong_count(ptr);\n  1560:     ///\n  1561:     ///     let five = Rc::from_raw(ptr);\n  1562:     ///     assert_eq!(2, Rc::strong_count(&five));\n  1563:     /// #   // Prevent leaks for Miri.\n  1564:     /// #   Rc::decrement_strong_count(ptr);\n  1565:     /// }\n  1566:     /// ```\n  1567:     #[inline]\n  1568:     #[stable(feature = \"rc_mutate_strong_count\", since = \"1.53.0\")]\n  1569:     pub unsafe fn increment_strong_count(ptr: *const T) {\n  1570:         unsafe { Self::increment_strong_count_in(ptr, Global) }\n  1571:     }\n  1572: \n  1573:     /// Decrements the strong reference count on the `Rc<T>` associated with the\n  1574:     /// provided pointer by one.\n  1575:     ///\n  1576:     /// # Safety\n  1577:     ///\n  1578:     /// The pointer must have been obtained through `Rc::into_raw` and must satisfy the\n  1579:     /// same layout requirements specified in [`Rc::from_raw_in`][from_raw_in].",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::into_raw",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "into_raw",
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
            "id": 302,
            "path": "Rc"
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
                          "id": 29,
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
        "impl_id": "alloc:3598",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "generic": "Self"
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
    "verification_source": "  1510:     /// [`Rc::from_raw`].\n  1511:     ///\n  1512:     /// # Examples\n  1513:     ///\n  1514:     /// ```\n  1515:     /// use std::rc::Rc;\n  1516:     ///\n  1517:     /// let x = Rc::new(\"hello\".to_owned());\n  1518:     /// let x_ptr = Rc::into_raw(x);\n  1519:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1520:     /// # // Prevent leaks for Miri.\n  1521:     /// # drop(unsafe { Rc::from_raw(x_ptr) });\n  1522:     /// ```\n  1523:     #[must_use = \"losing the pointer will leak memory\"]\n  1524:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1525:     #[rustc_never_returns_null_ptr]\n  1526:     pub fn into_raw(this: Self) -> *const T {\n  1527:         let this = ManuallyDrop::new(this);\n  1528:         Self::as_ptr(&*this)\n  1529:     }\n  1530: \n  1531:     /// Increments the strong reference count on the `Rc<T>` associated with the\n  1532:     /// provided pointer by one.\n  1533:     ///\n  1534:     /// # Safety\n  1535:     ///\n  1536:     /// The pointer must have been obtained through `Rc::into_raw` and must satisfy the\n  1537:     /// same layout requirements specified in [`Rc::from_raw_in`][from_raw_in].\n  1538:     /// The associated `Rc` instance must be valid (i.e. the strong count must be at\n  1539:     /// least 1) for the duration of this method, and `ptr` must point to a block of memory\n  1540:     /// allocated by the global allocator.\n  1541:     ///\n  1542:     /// [from_raw_in]: Rc::from_raw_in",
    "nanvix_source": "  1524:     ///\n  1525:     /// let x = Rc::new(\"hello\".to_owned());\n  1526:     /// let x_ptr = Rc::into_raw(x);\n  1527:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1528:     /// # // Prevent leaks for Miri.\n  1529:     /// # drop(unsafe { Rc::from_raw(x_ptr) });\n  1530:     /// ```\n  1531:     #[must_use = \"losing the pointer will leak memory\"]\n  1532:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1533:     #[rustc_never_returns_null_ptr]\n  1534:     pub fn into_raw(this: Self) -> *const T {\n  1535:         let this = ManuallyDrop::new(this);\n  1536:         Self::as_ptr(&*this)\n  1537:     }\n  1538: \n  1539:     /// Increments the strong reference count on the `Rc<T>` associated with the\n  1540:     /// provided pointer by one.\n  1541:     ///\n  1542:     /// # Safety\n  1543:     ///\n  1544:     /// The pointer must have been obtained through [`Rc::into_raw`] and must satisfy the",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::as_ptr",
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
        "is_const": false,
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
            "id": 3551,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:3747",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  3367:     /// let strong = Rc::new(\"hello\".to_owned());\n  3368:     /// let weak = Rc::downgrade(&strong);\n  3369:     /// // Both point to the same object\n  3370:     /// assert!(ptr::eq(&*strong, weak.as_ptr()));\n  3371:     /// // The strong here keeps it alive, so we can still access the object.\n  3372:     /// assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3373:     ///\n  3374:     /// drop(strong);\n  3375:     /// // But not any more. We can do weak.as_ptr(), but accessing the pointer would lead to\n  3376:     /// // undefined behavior.\n  3377:     /// // assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3378:     /// ```\n  3379:     ///\n  3380:     /// [`null`]: ptr::null\n  3381:     #[must_use]\n  3382:     #[stable(feature = \"rc_as_ptr\", since = \"1.45.0\")]\n  3383:     pub fn as_ptr(&self) -> *const T {\n  3384:         let ptr: *mut RcInner<T> = NonNull::as_ptr(self.ptr);\n  3385: \n  3386:         if is_dangling(ptr) {\n  3387:             // If the pointer is dangling, we return the sentinel directly. This cannot be\n  3388:             // a valid payload address, as the payload is at least as aligned as RcInner (usize).\n  3389:             ptr as *const T\n  3390:         } else {\n  3391:             // SAFETY: if is_dangling returns false, then the pointer is dereferenceable.\n  3392:             // The payload may be dropped at this point, and we have to maintain provenance,\n  3393:             // so use raw pointer manipulation.\n  3394:             unsafe { &raw mut (*ptr).value }\n  3395:         }\n  3396:     }\n  3397: \n  3398:     /// Consumes the `Weak<T>`, returning the wrapped pointer and allocator.\n  3399:     ///",
    "nanvix_source": "  3382:     ///\n  3383:     /// drop(strong);\n  3384:     /// // But not any more. We can do weak.as_ptr(), but accessing the pointer would lead to\n  3385:     /// // undefined behavior.\n  3386:     /// // assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3387:     /// ```\n  3388:     ///\n  3389:     /// [`null`]: ptr::null\n  3390:     #[must_use]\n  3391:     #[stable(feature = \"rc_as_ptr\", since = \"1.45.0\")]\n  3392:     pub fn as_ptr(&self) -> *const T {\n  3393:         let ptr: *mut RcInner<T> = NonNull::as_ptr(self.ptr);\n  3394: \n  3395:         if is_dangling(ptr) {\n  3396:             // If the pointer is dangling, we return the sentinel directly. This cannot be\n  3397:             // a valid payload address, as the payload is at least as aligned as RcInner (usize).\n  3398:             ptr as *const T\n  3399:         } else {\n  3400:             // SAFETY: if is_dangling returns false, then the pointer is dereferenceable.\n  3401:             // The payload may be dropped at this point, and we have to maintain provenance,\n  3402:             // so use raw pointer manipulation.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::from_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "from_raw",
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
            "id": 3551,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:3739",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "  3294:     /// assert_eq!(2, Rc::weak_count(&strong));\n  3295:     ///\n  3296:     /// assert_eq!(\"hello\", &*unsafe { Weak::from_raw(raw_1) }.upgrade().unwrap());\n  3297:     /// assert_eq!(1, Rc::weak_count(&strong));\n  3298:     ///\n  3299:     /// drop(strong);\n  3300:     ///\n  3301:     /// // Decrement the last weak count.\n  3302:     /// assert!(unsafe { Weak::from_raw(raw_2) }.upgrade().is_none());\n  3303:     /// ```\n  3304:     ///\n  3305:     /// [`into_raw`]: Weak::into_raw\n  3306:     /// [`upgrade`]: Weak::upgrade\n  3307:     /// [`new`]: Weak::new\n  3308:     #[inline]\n  3309:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3310:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  3311:         unsafe { Self::from_raw_in(ptr, Global) }\n  3312:     }\n  3313: \n  3314:     /// Consumes the `Weak<T>` and turns it into a raw pointer.\n  3315:     ///\n  3316:     /// This converts the weak pointer into a raw pointer, while still preserving the ownership of\n  3317:     /// one weak reference (the weak count is not modified by this operation). It can be turned\n  3318:     /// back into the `Weak<T>` with [`from_raw`].\n  3319:     ///\n  3320:     /// The same restrictions of accessing the target of the pointer as with\n  3321:     /// [`as_ptr`] apply.\n  3322:     ///\n  3323:     /// # Examples\n  3324:     ///\n  3325:     /// ```\n  3326:     /// use std::rc::{Rc, Weak};",
    "nanvix_source": "  3309:     ///\n  3310:     /// // Decrement the last weak count.\n  3311:     /// assert!(unsafe { Weak::from_raw(raw_2) }.upgrade().is_none());\n  3312:     /// ```\n  3313:     ///\n  3314:     /// [`into_raw`]: Weak::into_raw\n  3315:     /// [`upgrade`]: Weak::upgrade\n  3316:     /// [`new`]: Weak::new\n  3317:     #[inline]\n  3318:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3319:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  3320:         unsafe { Self::from_raw_in(ptr, Global) }\n  3321:     }\n  3322: \n  3323:     /// Consumes the `Weak<T>` and turns it into a raw pointer.\n  3324:     ///\n  3325:     /// This converts the weak pointer into a raw pointer, while still preserving the ownership of\n  3326:     /// one weak reference (the weak count is not modified by this operation). It can be turned\n  3327:     /// back into the `Weak<T>` with [`from_raw`].\n  3328:     ///\n  3329:     /// The same restrictions of accessing the target of the pointer as with",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::into_raw",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "into_raw",
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
            "id": 3551,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:3739",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  3327:     ///\n  3328:     /// let strong = Rc::new(\"hello\".to_owned());\n  3329:     /// let weak = Rc::downgrade(&strong);\n  3330:     /// let raw = weak.into_raw();\n  3331:     ///\n  3332:     /// assert_eq!(1, Rc::weak_count(&strong));\n  3333:     /// assert_eq!(\"hello\", unsafe { &*raw });\n  3334:     ///\n  3335:     /// drop(unsafe { Weak::from_raw(raw) });\n  3336:     /// assert_eq!(0, Rc::weak_count(&strong));\n  3337:     /// ```\n  3338:     ///\n  3339:     /// [`from_raw`]: Weak::from_raw\n  3340:     /// [`as_ptr`]: Weak::as_ptr\n  3341:     #[must_use = \"losing the pointer will leak memory\"]\n  3342:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3343:     pub fn into_raw(self) -> *const T {\n  3344:         mem::ManuallyDrop::new(self).as_ptr()\n  3345:     }\n  3346: }\n  3347: \n  3348: impl<T: ?Sized, A: Allocator> Weak<T, A> {\n  3349:     /// Returns a reference to the underlying allocator.\n  3350:     #[inline]\n  3351:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  3352:     pub fn allocator(&self) -> &A {\n  3353:         &self.alloc\n  3354:     }\n  3355: \n  3356:     /// Returns a raw pointer to the object `T` pointed to by this `Weak<T>`.\n  3357:     ///\n  3358:     /// The pointer is valid only if there are some strong references. The pointer may be dangling,\n  3359:     /// unaligned or even [`null`] otherwise.",
    "nanvix_source": "  3342:     /// assert_eq!(\"hello\", unsafe { &*raw });\n  3343:     ///\n  3344:     /// drop(unsafe { Weak::from_raw(raw) });\n  3345:     /// assert_eq!(0, Rc::weak_count(&strong));\n  3346:     /// ```\n  3347:     ///\n  3348:     /// [`from_raw`]: Weak::from_raw\n  3349:     /// [`as_ptr`]: Weak::as_ptr\n  3350:     #[must_use = \"losing the pointer will leak memory\"]\n  3351:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3352:     pub fn into_raw(self) -> *const T {\n  3353:         mem::ManuallyDrop::new(self).as_ptr()\n  3354:     }\n  3355: }\n  3356: \n  3357: impl<T: ?Sized, A: Allocator> Weak<T, A> {\n  3358:     /// Returns a reference to the underlying allocator.\n  3359:     #[inline]\n  3360:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  3361:     pub fn allocator(&self) -> &A {\n  3362:         &self.alloc",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::str::from_boxed_utf8_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "free_function"
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
        "is_unsafe": true
      },
      "name": "from_boxed_utf8_unchecked",
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
            "v",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "slice": {
                            "primitive": "u8"
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 82,
                "path": "crate::boxed::Box"
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
                      "primitive": "str"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "crate::boxed::Box"
          }
        }
      }
    },
    "verification_source": "   600: ///\n   601: /// # Safety\n   602: ///\n   603: /// * The provided bytes must contain a valid UTF-8 sequence.\n   604: ///\n   605: /// # Examples\n   606: ///\n   607: /// ```\n   608: /// let smile_utf8 = Box::new([226, 152, 186]);\n   609: /// let smile = unsafe { std::str::from_boxed_utf8_unchecked(smile_utf8) };\n   610: ///\n   611: /// assert_eq!(\"\u263a\", &*smile);\n   612: /// ```\n   613: #[stable(feature = \"str_box_extras\", since = \"1.20.0\")]\n   614: #[must_use]\n   615: #[inline]\n   616: pub unsafe fn from_boxed_utf8_unchecked(v: Box<[u8]>) -> Box<str> {\n   617:     unsafe { Box::from_raw(Box::into_raw(v) as *mut str) }\n   618: }\n   619: \n   620: /// Converts leading ascii bytes in `s` by calling the `convert` function.\n   621: ///\n   622: /// For better average performance, this happens in chunks of `2*size_of::<usize>()`.\n   623: ///\n   624: /// Returns a tuple of the converted prefix and the remainder starting from\n   625: /// the first non-ascii character.\n   626: ///\n   627: /// This function is only public so that it can be verified in a codegen test,\n   628: /// see `issue-123712-str-to-lower-autovectorization.rs`.\n   629: #[unstable(feature = \"str_internals\", issue = \"none\")]\n   630: #[doc(hidden)]\n   631: #[inline]\n   632: #[cfg(not(no_global_oom_handling))]",
    "nanvix_source": "   885: ///\n   886: /// ```\n   887: /// let smile_utf8 = Box::new([226, 152, 186]);\n   888: /// let smile = unsafe { std::str::from_boxed_utf8_unchecked(smile_utf8) };\n   889: ///\n   890: /// assert_eq!(\"\u263a\", &*smile);\n   891: /// ```\n   892: #[stable(feature = \"str_box_extras\", since = \"1.20.0\")]\n   893: #[must_use]\n   894: #[inline]\n   895: pub unsafe fn from_boxed_utf8_unchecked(v: Box<[u8]>) -> Box<str> {\n   896:     unsafe { Box::from_raw(Box::into_raw(v) as *mut str) }\n   897: }\n   898: \n   899: /// Converts leading ascii bytes in `s` by calling the `convert` function.\n   900: ///\n   901: /// For better average performance, this happens in chunks of `2*size_of::<usize>()`.\n   902: ///\n   903: /// Returns a tuple of the converted prefix and the remainder starting from\n   904: /// the first non-ascii character.\n   905: ///",
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
