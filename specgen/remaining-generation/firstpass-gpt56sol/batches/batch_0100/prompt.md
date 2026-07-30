For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::alloc::handle_alloc_error",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "handle_alloc_error",
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
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 70,
                "path": "Layout"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "never"
        }
      }
    },
    "verification_source": "   522: ///\n   523: /// The default behavior is:\n   524: ///\n   525: ///  * If the binary links against `std` (typically the case), then\n   526: ///   print a message to standard error and abort the process.\n   527: ///   This behavior can be replaced with [`set_alloc_error_hook`] and [`take_alloc_error_hook`].\n   528: ///   Future versions of Rust may panic by default instead.\n   529: ///\n   530: /// * If the binary does not link against `std` (all of its crates are marked\n   531: ///   [`#![no_std]`][no_std]), then call [`panic!`] with a message.\n   532: ///   [The panic handler] applies as to any panic.\n   533: ///\n   534: /// [`set_alloc_error_hook`]: ../../std/alloc/fn.set_alloc_error_hook.html\n   535: /// [`take_alloc_error_hook`]: ../../std/alloc/fn.take_alloc_error_hook.html\n   536: /// [The panic handler]: https://doc.rust-lang.org/reference/runtime.html#the-panic_handler-attribute\n   537: /// [no_std]: https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute\n   538: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   539: #[rustc_const_unstable(feature = \"const_alloc_error\", issue = \"92523\")]\n   540: #[cfg(not(no_global_oom_handling))]\n   541: #[cold]\n   542: #[optimize(size)]\n   543: pub const fn handle_alloc_error(layout: Layout) -> ! {\n   544:     const fn ct_error(_: Layout) -> ! {\n   545:         panic!(\"allocation failed\");\n   546:     }\n   547: \n   548:     #[inline]\n   549:     fn rt_error(layout: Layout) -> ! {\n   550:         unsafe {\n   551:             __rust_alloc_error_handler(layout.size(), layout.align());\n   552:         }\n   553:     }\n   554: ",
    "nanvix_source": "   528: ///   Future versions of Rust may panic by default instead.\n   529: ///\n   530: /// * If the binary does not link against `std` (all of its crates are marked\n   531: ///   [`#![no_std]`][no_std]), then call [`panic!`] with a message.\n   532: ///   [The panic handler] applies as to any panic.\n   533: ///\n   534: /// [`set_alloc_error_hook`]: ../../std/alloc/fn.set_alloc_error_hook.html\n   535: /// [`take_alloc_error_hook`]: ../../std/alloc/fn.take_alloc_error_hook.html\n   536: /// [The panic handler]: https://doc.rust-lang.org/reference/runtime.html#the-panic_handler-attribute\n   537: /// [no_std]: https://doc.rust-lang.org/reference/names/preludes.html#the-no_std-attribute\n   538: #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   539: #[rustc_const_unstable(feature = \"const_alloc_error\", issue = \"92523\")]\n   540: #[cfg(not(no_global_oom_handling))]\n   541: #[cold]\n   542: #[optimize(size)]\n   543: pub const fn handle_alloc_error(layout: Layout) -> ! {\n   544:     const fn ct_error(_: Layout) -> ! {\n   545:         panic!(\"allocation failed\");\n   546:     }\n   547: \n   548:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::append",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "append",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "other"
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
            "id": 979,
            "path": "BinaryHeap"
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
                          "id": 176,
                          "path": "Ord"
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
        "impl_id": "alloc:995",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "other",
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
    "verification_source": "   983:     /// # Examples\n   984:     ///\n   985:     /// Basic usage:\n   986:     ///\n   987:     /// ```\n   988:     /// use std::collections::BinaryHeap;\n   989:     ///\n   990:     /// let mut a = BinaryHeap::from([-10, 1, 2, 3, 3]);\n   991:     /// let mut b = BinaryHeap::from([-20, 5, 43]);\n   992:     ///\n   993:     /// a.append(&mut b);\n   994:     ///\n   995:     /// assert_eq!(a.into_sorted_vec(), [-20, -10, 1, 2, 3, 3, 5, 43]);\n   996:     /// assert!(b.is_empty());\n   997:     /// ```\n   998:     #[stable(feature = \"binary_heap_append\", since = \"1.11.0\")]\n   999:     pub fn append(&mut self, other: &mut Self) {\n  1000:         if self.len() < other.len() {\n  1001:             swap(self, other);\n  1002:         }\n  1003: \n  1004:         let start = self.data.len();\n  1005: \n  1006:         self.data.append(&mut other.data);\n  1007: \n  1008:         self.rebuild_tail(start);\n  1009:     }\n  1010: \n  1011:     /// Clears the binary heap, returning an iterator over the removed elements\n  1012:     /// in heap order. If the iterator is dropped before being fully consumed,\n  1013:     /// it drops the remaining elements in heap order.\n  1014:     ///\n  1015:     /// The returned iterator keeps a mutable borrow on the heap to optimize",
    "nanvix_source": "   989:     ///\n   990:     /// let mut a = BinaryHeap::from([-10, 1, 2, 3, 3]);\n   991:     /// let mut b = BinaryHeap::from([-20, 5, 43]);\n   992:     ///\n   993:     /// a.append(&mut b);\n   994:     ///\n   995:     /// assert_eq!(a.into_sorted_vec(), [-20, -10, 1, 2, 3, 3, 5, 43]);\n   996:     /// assert!(b.is_empty());\n   997:     /// ```\n   998:     #[stable(feature = \"binary_heap_append\", since = \"1.11.0\")]\n   999:     pub fn append(&mut self, other: &mut Self) {\n  1000:         if self.len() < other.len() {\n  1001:             swap(self, other);\n  1002:         }\n  1003: \n  1004:         let start = self.data.len();\n  1005: \n  1006:         self.data.append(&mut other.data);\n  1007: \n  1008:         self.rebuild_tail(start);\n  1009:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::as_slice",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_slice",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1347:     /// order.\n  1348:     ///\n  1349:     /// # Examples\n  1350:     ///\n  1351:     /// Basic usage:\n  1352:     ///\n  1353:     /// ```\n  1354:     /// use std::collections::BinaryHeap;\n  1355:     /// use std::io::{self, Write};\n  1356:     ///\n  1357:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5, 6, 7]);\n  1358:     ///\n  1359:     /// io::sink().write(heap.as_slice()).unwrap();\n  1360:     /// ```\n  1361:     #[must_use]\n  1362:     #[stable(feature = \"binary_heap_as_slice\", since = \"1.80.0\")]\n  1363:     pub fn as_slice(&self) -> &[T] {\n  1364:         self.data.as_slice()\n  1365:     }\n  1366: \n  1367:     /// Returns a mutable slice of all values in the underlying vector.\n  1368:     ///\n  1369:     /// # Safety\n  1370:     ///\n  1371:     /// The caller must ensure that the slice remains a max-heap, i.e. for all indices\n  1372:     /// `0 < i < slice.len()`, `slice[(i - 1) / 2] >= slice[i]`, before the borrow ends\n  1373:     /// and the binary heap is used.\n  1374:     ///\n  1375:     /// # Examples\n  1376:     ///\n  1377:     /// Basic usage:\n  1378:     ///\n  1379:     /// ```",
    "nanvix_source": "  1353:     /// ```\n  1354:     /// use std::collections::BinaryHeap;\n  1355:     /// use std::io::{self, Write};\n  1356:     ///\n  1357:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5, 6, 7]);\n  1358:     ///\n  1359:     /// io::sink().write(heap.as_slice()).unwrap();\n  1360:     /// ```\n  1361:     #[must_use]\n  1362:     #[stable(feature = \"binary_heap_as_slice\", since = \"1.80.0\")]\n  1363:     pub fn as_slice(&self) -> &[T] {\n  1364:         self.data.as_slice()\n  1365:     }\n  1366: \n  1367:     /// Returns a mutable slice of all values in the underlying vector.\n  1368:     ///\n  1369:     /// # Safety\n  1370:     ///\n  1371:     /// The caller must ensure that the slice remains a max-heap, i.e. for all indices\n  1372:     /// `0 < i < slice.len()`, `slice[(i - 1) / 2] >= slice[i]`, before the borrow ends\n  1373:     /// and the binary heap is used.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::clear",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "clear",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
    "verification_source": "  1501:     ///\n  1502:     /// # Examples\n  1503:     ///\n  1504:     /// Basic usage:\n  1505:     ///\n  1506:     /// ```\n  1507:     /// use std::collections::BinaryHeap;\n  1508:     /// let mut heap = BinaryHeap::from([1, 3]);\n  1509:     ///\n  1510:     /// assert!(!heap.is_empty());\n  1511:     ///\n  1512:     /// heap.clear();\n  1513:     ///\n  1514:     /// assert!(heap.is_empty());\n  1515:     /// ```\n  1516:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1517:     pub fn clear(&mut self) {\n  1518:         self.drain();\n  1519:     }\n  1520: }\n  1521: \n  1522: /// Hole represents a hole in a slice i.e., an index without valid value\n  1523: /// (because it was moved from or duplicated).\n  1524: /// In drop, `Hole` will restore the slice by filling the hole\n  1525: /// position with the value that was originally removed.\n  1526: struct Hole<'a, T: 'a> {\n  1527:     data: &'a mut [T],\n  1528:     elt: ManuallyDrop<T>,\n  1529:     pos: usize,\n  1530: }\n  1531: \n  1532: impl<'a, T> Hole<'a, T> {\n  1533:     /// Creates a new `Hole` at index `pos`.",
    "nanvix_source": "  1507:     /// use std::collections::BinaryHeap;\n  1508:     /// let mut heap = BinaryHeap::from([1, 3]);\n  1509:     ///\n  1510:     /// assert!(!heap.is_empty());\n  1511:     ///\n  1512:     /// heap.clear();\n  1513:     ///\n  1514:     /// assert!(heap.is_empty());\n  1515:     /// ```\n  1516:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1517:     pub fn clear(&mut self) {\n  1518:         self.drain();\n  1519:     }\n  1520: }\n  1521: \n  1522: /// Hole represents a hole in a slice i.e., an index without valid value\n  1523: /// (because it was moved from or duplicated).\n  1524: /// In drop, `Hole` will restore the slice by filling the hole\n  1525: /// position with the value that was originally removed.\n  1526: struct Hole<'a, T: 'a> {\n  1527:     data: &'a mut [T],",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::into_sorted_vec",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "into_sorted_vec",
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
            "id": 979,
            "path": "BinaryHeap"
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
                          "id": 176,
                          "path": "Ord"
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
        "impl_id": "alloc:995",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
        }
      }
    },
    "verification_source": "   758:     /// # Examples\n   759:     ///\n   760:     /// Basic usage:\n   761:     ///\n   762:     /// ```\n   763:     /// use std::collections::BinaryHeap;\n   764:     ///\n   765:     /// let mut heap = BinaryHeap::from([1, 2, 4, 5, 7]);\n   766:     /// heap.push(6);\n   767:     /// heap.push(3);\n   768:     ///\n   769:     /// let vec = heap.into_sorted_vec();\n   770:     /// assert_eq!(vec, [1, 2, 3, 4, 5, 6, 7]);\n   771:     /// ```\n   772:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   773:     #[stable(feature = \"binary_heap_extras_15\", since = \"1.5.0\")]\n   774:     pub fn into_sorted_vec(mut self) -> Vec<T, A> {\n   775:         let mut end = self.len();\n   776:         while end > 1 {\n   777:             end -= 1;\n   778:             // SAFETY: `end` goes from `self.len() - 1` to 1 (both included),\n   779:             //  so it's always a valid index to access.\n   780:             //  It is safe to access index 0 (i.e. `ptr`), because\n   781:             //  1 <= end < self.len(), which means self.len() >= 2.\n   782:             unsafe {\n   783:                 let ptr = self.data.as_mut_ptr();\n   784:                 ptr::swap(ptr, ptr.add(end));\n   785:             }\n   786:             // SAFETY: `end` goes from `self.len() - 1` to 1 (both included) so:\n   787:             //  0 < 1 <= end <= self.len() - 1 < self.len()\n   788:             //  Which means 0 < end and end < self.len().\n   789:             unsafe { self.sift_down_range(0, end) };\n   790:         }",
    "nanvix_source": "   764:     ///\n   765:     /// let mut heap = BinaryHeap::from([1, 2, 4, 5, 7]);\n   766:     /// heap.push(6);\n   767:     /// heap.push(3);\n   768:     ///\n   769:     /// let vec = heap.into_sorted_vec();\n   770:     /// assert_eq!(vec, [1, 2, 3, 4, 5, 6, 7]);\n   771:     /// ```\n   772:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   773:     #[stable(feature = \"binary_heap_extras_15\", since = \"1.5.0\")]\n   774:     pub fn into_sorted_vec(mut self) -> Vec<T, A> {\n   775:         let mut end = self.len();\n   776:         while end > 1 {\n   777:             end -= 1;\n   778:             // SAFETY: `end` goes from `self.len() - 1` to 1 (both included),\n   779:             //  so it's always a valid index to access.\n   780:             //  It is safe to access index 0 (i.e. `ptr`), because\n   781:             //  1 <= end < self.len(), which means self.len() >= 2.\n   782:             unsafe {\n   783:                 let ptr = self.data.as_mut_ptr();\n   784:                 ptr::swap(ptr, ptr.add(end));",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::into_vec",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "into_vec",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
        }
      }
    },
    "verification_source": "  1401:     /// # Examples\n  1402:     ///\n  1403:     /// Basic usage:\n  1404:     ///\n  1405:     /// ```\n  1406:     /// use std::collections::BinaryHeap;\n  1407:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5, 6, 7]);\n  1408:     /// let vec = heap.into_vec();\n  1409:     ///\n  1410:     /// // Will print in some order\n  1411:     /// for x in vec {\n  1412:     ///     println!(\"{x}\");\n  1413:     /// }\n  1414:     /// ```\n  1415:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1416:     #[stable(feature = \"binary_heap_extras_15\", since = \"1.5.0\")]\n  1417:     pub fn into_vec(self) -> Vec<T, A> {\n  1418:         self.into()\n  1419:     }\n  1420: \n  1421:     /// Returns a reference to the underlying allocator.\n  1422:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  1423:     #[inline]\n  1424:     pub fn allocator(&self) -> &A {\n  1425:         self.data.allocator()\n  1426:     }\n  1427: \n  1428:     /// Returns the length of the binary heap.\n  1429:     ///\n  1430:     /// # Examples\n  1431:     ///\n  1432:     /// Basic usage:\n  1433:     ///",
    "nanvix_source": "  1407:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5, 6, 7]);\n  1408:     /// let vec = heap.into_vec();\n  1409:     ///\n  1410:     /// // Will print in some order\n  1411:     /// for x in vec {\n  1412:     ///     println!(\"{x}\");\n  1413:     /// }\n  1414:     /// ```\n  1415:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1416:     #[stable(feature = \"binary_heap_extras_15\", since = \"1.5.0\")]\n  1417:     pub fn into_vec(self) -> Vec<T, A> {\n  1418:         self.into()\n  1419:     }\n  1420: \n  1421:     /// Returns a reference to the underlying allocator.\n  1422:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  1423:     #[inline]\n  1424:     pub fn allocator(&self) -> &A {\n  1425:         self.data.allocator()\n  1426:     }\n  1427: ",
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
