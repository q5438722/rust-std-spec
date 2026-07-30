For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicPtr::fetch_xor",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
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
      "name": "fetch_xor",
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
          ],
          [
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
    "verification_source": "  2443:     ///\n  2444:     /// ```\n  2445:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2446:     ///\n  2447:     /// let pointer = &mut 3i64 as *mut i64;\n  2448:     /// let atom = AtomicPtr::<i64>::new(pointer);\n  2449:     ///\n  2450:     /// // Toggle a tag bit on the pointer.\n  2451:     /// atom.fetch_xor(1, Ordering::Relaxed);\n  2452:     /// assert_eq!(atom.load(Ordering::Relaxed).addr() & 1, 1);\n  2453:     /// ```\n  2454:     #[inline]\n  2455:     #[cfg(target_has_atomic = \"ptr\")]\n  2456:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2457:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2458:     #[rustc_should_not_be_called_on_const_items]\n  2459:     pub fn fetch_xor(&self, val: usize, order: Ordering) -> *mut T {\n  2460:         // SAFETY: data races are prevented by atomic intrinsics.\n  2461:         unsafe { atomic_xor(self.as_ptr(), val, order).cast() }\n  2462:     }\n  2463: \n  2464:     /// Returns a mutable pointer to the underlying pointer.\n  2465:     ///\n  2466:     /// Doing non-atomic reads and writes on the resulting pointer can be a data race.\n  2467:     /// This method is mostly useful for FFI, where the function signature may use\n  2468:     /// `*mut *mut T` instead of `&AtomicPtr<T>`.\n  2469:     ///\n  2470:     /// Returning an `*mut` pointer from a shared reference to this atomic is safe because the\n  2471:     /// atomic types work with interior mutability. All modifications of an atomic change the value\n  2472:     /// through a shared reference, and can do so safely as long as they use atomic operations. Any\n  2473:     /// use of the returned raw pointer requires an `unsafe` block and still has to uphold the\n  2474:     /// requirements of the [memory model].\n  2475:     ///",
    "nanvix_source": "  2438:     ///\n  2439:     /// // Toggle a tag bit on the pointer.\n  2440:     /// atom.fetch_xor(1, Ordering::Relaxed);\n  2441:     /// assert_eq!(atom.load(Ordering::Relaxed).addr() & 1, 1);\n  2442:     /// ```\n  2443:     #[inline]\n  2444:     #[cfg(target_has_atomic = \"ptr\")]\n  2445:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2446:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2447:     #[rustc_should_not_be_called_on_const_items]\n  2448:     pub fn fetch_xor(&self, val: usize, order: Ordering) -> *mut T {\n  2449:         // SAFETY: data races are prevented by atomic intrinsics.\n  2450:         unsafe { atomic_xor(self.as_ptr(), val, order).cast() }\n  2451:     }\n  2452: \n  2453:     /// Returns a mutable pointer to the underlying pointer.\n  2454:     ///\n  2455:     /// Doing non-atomic reads and writes on the resulting pointer can be a data race.\n  2456:     /// This method is mostly useful for FFI, where the function signature may use\n  2457:     /// `*mut *mut T` instead of `&AtomicPtr<T>`.\n  2458:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::from_mut",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
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
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "raw_pointer": {
                    "is_mutable": true,
                    "type": {
                      "generic": "T"
                    }
                  }
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
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "  1582:     /// # Examples\n  1583:     ///\n  1584:     /// ```\n  1585:     /// #![feature(atomic_from_mut)]\n  1586:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1587:     ///\n  1588:     /// let mut data = 123;\n  1589:     /// let mut some_ptr = &mut data as *mut i32;\n  1590:     /// let a = AtomicPtr::from_mut(&mut some_ptr);\n  1591:     /// let mut other_data = 456;\n  1592:     /// a.store(&mut other_data, Ordering::Relaxed);\n  1593:     /// assert_eq!(unsafe { *some_ptr }, 456);\n  1594:     /// ```\n  1595:     #[inline]\n  1596:     #[cfg(target_has_atomic_equal_alignment = \"ptr\")]\n  1597:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n  1598:     pub fn from_mut(v: &mut *mut T) -> &mut Self {\n  1599:         let [] = [(); align_of::<AtomicPtr<()>>() - align_of::<*mut ()>()];\n  1600:         // SAFETY:\n  1601:         //  - the mutable reference guarantees unique ownership.\n  1602:         //  - the alignment of `*mut T` and `Self` is the same on all platforms\n  1603:         //    supported by rust, as verified above.\n  1604:         unsafe { &mut *(v as *mut *mut T as *mut Self) }\n  1605:     }\n  1606: \n  1607:     /// Gets non-atomic access to a `&mut [AtomicPtr]` slice.\n  1608:     ///\n  1609:     /// This is safe because the mutable reference guarantees that no other threads are\n  1610:     /// concurrently accessing the atomic data.\n  1611:     ///\n  1612:     /// # Examples\n  1613:     ///\n  1614:     /// ```ignore-wasm",
    "nanvix_source": "  1579:     /// let mut data = 123;\n  1580:     /// let mut some_ptr = &mut data as *mut i32;\n  1581:     /// let a = AtomicPtr::from_mut(&mut some_ptr);\n  1582:     /// let mut other_data = 456;\n  1583:     /// a.store(&mut other_data, Ordering::Relaxed);\n  1584:     /// assert_eq!(unsafe { *some_ptr }, 456);\n  1585:     /// ```\n  1586:     #[inline]\n  1587:     #[cfg(target_has_atomic_primitive_alignment = \"ptr\")]\n  1588:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n  1589:     pub fn from_mut(v: &mut *mut T) -> &mut Self {\n  1590:         let [] = [(); align_of::<AtomicPtr<()>>() - align_of::<*mut ()>()];\n  1591:         // SAFETY:\n  1592:         //  - the mutable reference guarantees unique ownership.\n  1593:         //  - the alignment of `*mut T` and `Self` is the same on all platforms\n  1594:         //    supported by rust, as verified above.\n  1595:         unsafe { &mut *(v as *mut *mut T as *mut Self) }\n  1596:     }\n  1597: \n  1598:     /// Gets non-atomic access to a `&mut [AtomicPtr]` slice.\n  1599:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::from_mut_slice",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
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
      "name": "from_mut_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "raw_pointer": {
                      "is_mutable": true,
                      "type": {
                        "generic": "T"
                      }
                    }
                  }
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
              "slice": {
                "generic": "Self"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1661:     ///     for i in 0..a.len() {\n  1662:     ///         s.spawn(move || {\n  1663:     ///             let name = Box::new(format!(\"thread{i}\"));\n  1664:     ///             a[i].store(Box::into_raw(name), Ordering::Relaxed);\n  1665:     ///         });\n  1666:     ///     }\n  1667:     /// });\n  1668:     /// for p in some_ptrs {\n  1669:     ///     assert!(!p.is_null());\n  1670:     ///     let name = unsafe { Box::from_raw(p) };\n  1671:     ///     println!(\"Hello, {name}!\");\n  1672:     /// }\n  1673:     /// ```\n  1674:     #[inline]\n  1675:     #[cfg(target_has_atomic_equal_alignment = \"ptr\")]\n  1676:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n  1677:     pub fn from_mut_slice(v: &mut [*mut T]) -> &mut [Self] {\n  1678:         // SAFETY:\n  1679:         //  - the mutable reference guarantees unique ownership.\n  1680:         //  - the alignment of `*mut T` and `Self` is the same on all platforms\n  1681:         //    supported by rust, as verified above.\n  1682:         unsafe { &mut *(v as *mut [*mut T] as *mut [Self]) }\n  1683:     }\n  1684: \n  1685:     /// Consumes the atomic and returns the contained value.\n  1686:     ///\n  1687:     /// This is safe because passing `self` by value guarantees that no other threads are\n  1688:     /// concurrently accessing the atomic data.\n  1689:     ///\n  1690:     /// # Examples\n  1691:     ///\n  1692:     /// ```\n  1693:     /// use std::sync::atomic::AtomicPtr;",
    "nanvix_source": "  1656:     /// });\n  1657:     /// for p in some_ptrs {\n  1658:     ///     assert!(!p.is_null());\n  1659:     ///     let name = unsafe { Box::from_raw(p) };\n  1660:     ///     println!(\"Hello, {name}!\");\n  1661:     /// }\n  1662:     /// ```\n  1663:     #[inline]\n  1664:     #[cfg(target_has_atomic_primitive_alignment = \"ptr\")]\n  1665:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n  1666:     pub fn from_mut_slice(v: &mut [*mut T]) -> &mut [Self] {\n  1667:         // SAFETY:\n  1668:         //  - the mutable reference guarantees unique ownership.\n  1669:         //  - the alignment of `*mut T` and `Self` is the same on all platforms\n  1670:         //    supported by rust, as verified above.\n  1671:         unsafe { &mut *(v as *mut [*mut T] as *mut [Self]) }\n  1672:     }\n  1673: \n  1674:     /// Consumes the atomic and returns the contained value.\n  1675:     ///\n  1676:     /// This is safe because passing `self` by value guarantees that no other threads are",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::from_ptr",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
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
      "name": "from_ptr",
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "raw_pointer": {
                    "is_mutable": true,
                    "type": {
                      "generic": "T"
                    }
                  }
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
                "id": 9623,
                "path": "AtomicPtr"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1515:     /// ```\n  1516:     ///\n  1517:     /// # Safety\n  1518:     ///\n  1519:     /// * `ptr` must be aligned to `align_of::<AtomicPtr<T>>()` (note that on some platforms this\n  1520:     ///   can be bigger than `align_of::<*mut T>()`).\n  1521:     /// * `ptr` must be [valid] for both reads and writes for the whole lifetime `'a`.\n  1522:     /// * You must adhere to the [Memory model for atomic accesses]. In particular, it is not\n  1523:     ///   allowed to mix conflicting atomic and non-atomic accesses, or atomic accesses of different\n  1524:     ///   sizes, without synchronization.\n  1525:     ///\n  1526:     /// [valid]: crate::ptr#safety\n  1527:     /// [Memory model for atomic accesses]: self#memory-model-for-atomic-accesses\n  1528:     #[inline]\n  1529:     #[stable(feature = \"atomic_from_ptr\", since = \"1.75.0\")]\n  1530:     #[rustc_const_stable(feature = \"const_atomic_from_ptr\", since = \"1.84.0\")]\n  1531:     pub const unsafe fn from_ptr<'a>(ptr: *mut *mut T) -> &'a AtomicPtr<T> {\n  1532:         // SAFETY: guaranteed by the caller\n  1533:         unsafe { &*ptr.cast() }\n  1534:     }\n  1535: \n  1536:     /// Creates a new `AtomicPtr` initialized with a null pointer.\n  1537:     ///\n  1538:     /// # Examples\n  1539:     ///\n  1540:     /// ```\n  1541:     /// #![feature(atomic_ptr_null)]\n  1542:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1543:     ///\n  1544:     /// let atomic_ptr = AtomicPtr::<()>::null();\n  1545:     /// assert!(atomic_ptr.load(Ordering::Relaxed).is_null());\n  1546:     /// ```\n  1547:     #[inline]",
    "nanvix_source": "  1513:     /// * `ptr` must be [valid] for both reads and writes for the whole lifetime `'a`.\n  1514:     /// * You must adhere to the [Memory model for atomic accesses]. In particular, it is not\n  1515:     ///   allowed to mix conflicting atomic and non-atomic accesses, or atomic accesses of different\n  1516:     ///   sizes, without synchronization.\n  1517:     ///\n  1518:     /// [valid]: crate::ptr#safety\n  1519:     /// [Memory model for atomic accesses]: self#memory-model-for-atomic-accesses\n  1520:     #[inline]\n  1521:     #[stable(feature = \"atomic_from_ptr\", since = \"1.75.0\")]\n  1522:     #[rustc_const_stable(feature = \"const_atomic_from_ptr\", since = \"1.84.0\")]\n  1523:     pub const unsafe fn from_ptr<'a>(ptr: *mut *mut T) -> &'a AtomicPtr<T> {\n  1524:         // SAFETY: guaranteed by the caller\n  1525:         unsafe { &*ptr.cast() }\n  1526:     }\n  1527: \n  1528:     /// Creates a new `AtomicPtr` initialized with a null pointer.\n  1529:     ///\n  1530:     /// # Examples\n  1531:     ///\n  1532:     /// ```\n  1533:     /// #![feature(atomic_ptr_null)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::get_mut",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "reference_identity_vs_view",
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
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "  1556:     /// This is safe because the mutable reference guarantees that no other threads are\n  1557:     /// concurrently accessing the atomic data.\n  1558:     ///\n  1559:     /// # Examples\n  1560:     ///\n  1561:     /// ```\n  1562:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1563:     ///\n  1564:     /// let mut data = 10;\n  1565:     /// let mut atomic_ptr = AtomicPtr::new(&mut data);\n  1566:     /// let mut other_data = 5;\n  1567:     /// *atomic_ptr.get_mut() = &mut other_data;\n  1568:     /// assert_eq!(unsafe { *atomic_ptr.load(Ordering::SeqCst) }, 5);\n  1569:     /// ```\n  1570:     #[inline]\n  1571:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n  1572:     pub fn get_mut(&mut self) -> &mut *mut T {\n  1573:         // SAFETY:\n  1574:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1575:         unsafe { &mut *self.as_ptr() }\n  1576:     }\n  1577: \n  1578:     /// Gets atomic access to a pointer.\n  1579:     ///\n  1580:     /// **Note:** This function is only available on targets where `AtomicPtr<T>` has the same alignment as `*const T`\n  1581:     ///\n  1582:     /// # Examples\n  1583:     ///\n  1584:     /// ```\n  1585:     /// #![feature(atomic_from_mut)]\n  1586:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1587:     ///\n  1588:     /// let mut data = 123;",
    "nanvix_source": "  1554:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1555:     ///\n  1556:     /// let mut data = 10;\n  1557:     /// let mut atomic_ptr = AtomicPtr::new(&mut data);\n  1558:     /// let mut other_data = 5;\n  1559:     /// *atomic_ptr.get_mut() = &mut other_data;\n  1560:     /// assert_eq!(unsafe { *atomic_ptr.load(Ordering::SeqCst) }, 5);\n  1561:     /// ```\n  1562:     #[inline]\n  1563:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n  1564:     pub fn get_mut(&mut self) -> &mut *mut T {\n  1565:         // SAFETY:\n  1566:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1567:         unsafe { &mut *self.as_ptr() }\n  1568:     }\n  1569: \n  1570:     /// Gets atomic access to a pointer.\n  1571:     ///\n  1572:     /// **Note:** This function is only available on targets where `AtomicPtr<T>` has the same alignment as `*const T`\n  1573:     ///\n  1574:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::get_mut_slice",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "reference_identity_vs_view",
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
      "name": "get_mut_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
        ],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "Self"
                  }
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
              "slice": {
                "raw_pointer": {
                  "is_mutable": true,
                  "type": {
                    "generic": "T"
                  }
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "  1626:     ///     .for_each(|(i, ptr)| *ptr = Box::into_raw(Box::new(format!(\"iteration#{i}\"))));\n  1627:     ///\n  1628:     /// std::thread::scope(|s| {\n  1629:     ///     for ptr in &some_ptrs {\n  1630:     ///         s.spawn(move || {\n  1631:     ///             let ptr = ptr.load(Ordering::Relaxed);\n  1632:     ///             assert!(!ptr.is_null());\n  1633:     ///\n  1634:     ///             let name = unsafe { Box::from_raw(ptr) };\n  1635:     ///             println!(\"Hello, {name}!\");\n  1636:     ///         });\n  1637:     ///     }\n  1638:     /// });\n  1639:     /// ```\n  1640:     #[inline]\n  1641:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n  1642:     pub fn get_mut_slice(this: &mut [Self]) -> &mut [*mut T] {\n  1643:         // SAFETY: the mutable reference guarantees unique ownership.\n  1644:         unsafe { &mut *(this as *mut [Self] as *mut [*mut T]) }\n  1645:     }\n  1646: \n  1647:     /// Gets atomic access to a slice of pointers.\n  1648:     ///\n  1649:     /// **Note:** This function is only available on targets where `AtomicPtr<T>` has the same alignment as `*const T`\n  1650:     ///\n  1651:     /// # Examples\n  1652:     ///\n  1653:     /// ```ignore-wasm\n  1654:     /// #![feature(atomic_from_mut)]\n  1655:     /// use std::ptr::null_mut;\n  1656:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1657:     ///\n  1658:     /// let mut some_ptrs = [null_mut::<String>(); 10];",
    "nanvix_source": "  1622:     ///             assert!(!ptr.is_null());\n  1623:     ///\n  1624:     ///             let name = unsafe { Box::from_raw(ptr) };\n  1625:     ///             println!(\"Hello, {name}!\");\n  1626:     ///         });\n  1627:     ///     }\n  1628:     /// });\n  1629:     /// ```\n  1630:     #[inline]\n  1631:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n  1632:     pub fn get_mut_slice(this: &mut [Self]) -> &mut [*mut T] {\n  1633:         // SAFETY: the mutable reference guarantees unique ownership.\n  1634:         unsafe { &mut *(this as *mut [Self] as *mut [*mut T]) }\n  1635:     }\n  1636: \n  1637:     /// Gets atomic access to a slice of pointers.\n  1638:     ///\n  1639:     /// **Note:** This function is only available on targets where `AtomicPtr<T>` has the same alignment as `*const T`\n  1640:     ///\n  1641:     /// # Examples\n  1642:     ///",
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
