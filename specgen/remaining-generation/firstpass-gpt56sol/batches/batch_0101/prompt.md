For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BinaryHeap::is_empty",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1451:     /// Basic usage:\n  1452:     ///\n  1453:     /// ```\n  1454:     /// use std::collections::BinaryHeap;\n  1455:     /// let mut heap = BinaryHeap::new();\n  1456:     ///\n  1457:     /// assert!(heap.is_empty());\n  1458:     ///\n  1459:     /// heap.push(3);\n  1460:     /// heap.push(5);\n  1461:     /// heap.push(1);\n  1462:     ///\n  1463:     /// assert!(!heap.is_empty());\n  1464:     /// ```\n  1465:     #[must_use]\n  1466:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1467:     pub fn is_empty(&self) -> bool {\n  1468:         self.len() == 0\n  1469:     }\n  1470: \n  1471:     /// Clears the binary heap, returning an iterator over the removed elements\n  1472:     /// in arbitrary order. If the iterator is dropped before being fully\n  1473:     /// consumed, it drops the remaining elements in arbitrary order.\n  1474:     ///\n  1475:     /// The returned iterator keeps a mutable borrow on the heap to optimize\n  1476:     /// its implementation.\n  1477:     ///\n  1478:     /// # Examples\n  1479:     ///\n  1480:     /// Basic usage:\n  1481:     ///\n  1482:     /// ```\n  1483:     /// use std::collections::BinaryHeap;",
    "nanvix_source": "  1457:     /// assert!(heap.is_empty());\n  1458:     ///\n  1459:     /// heap.push(3);\n  1460:     /// heap.push(5);\n  1461:     /// heap.push(1);\n  1462:     ///\n  1463:     /// assert!(!heap.is_empty());\n  1464:     /// ```\n  1465:     #[must_use]\n  1466:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1467:     pub fn is_empty(&self) -> bool {\n  1468:         self.len() == 0\n  1469:     }\n  1470: \n  1471:     /// Clears the binary heap, returning an iterator over the removed elements\n  1472:     /// in arbitrary order. If the iterator is dropped before being fully\n  1473:     /// consumed, it drops the remaining elements in arbitrary order.\n  1474:     ///\n  1475:     /// The returned iterator keeps a mutable borrow on the heap to optimize\n  1476:     /// its implementation.\n  1477:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::len",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1427: \n  1428:     /// Returns the length of the binary heap.\n  1429:     ///\n  1430:     /// # Examples\n  1431:     ///\n  1432:     /// Basic usage:\n  1433:     ///\n  1434:     /// ```\n  1435:     /// use std::collections::BinaryHeap;\n  1436:     /// let heap = BinaryHeap::from([1, 3]);\n  1437:     ///\n  1438:     /// assert_eq!(heap.len(), 2);\n  1439:     /// ```\n  1440:     #[must_use]\n  1441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1442:     #[rustc_confusables(\"length\", \"size\")]\n  1443:     pub fn len(&self) -> usize {\n  1444:         self.data.len()\n  1445:     }\n  1446: \n  1447:     /// Checks if the binary heap is empty.\n  1448:     ///\n  1449:     /// # Examples\n  1450:     ///\n  1451:     /// Basic usage:\n  1452:     ///\n  1453:     /// ```\n  1454:     /// use std::collections::BinaryHeap;\n  1455:     /// let mut heap = BinaryHeap::new();\n  1456:     ///\n  1457:     /// assert!(heap.is_empty());\n  1458:     ///\n  1459:     /// heap.push(3);",
    "nanvix_source": "  1433:     ///\n  1434:     /// ```\n  1435:     /// use std::collections::BinaryHeap;\n  1436:     /// let heap = BinaryHeap::from([1, 3]);\n  1437:     ///\n  1438:     /// assert_eq!(heap.len(), 2);\n  1439:     /// ```\n  1440:     #[must_use]\n  1441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1442:     #[rustc_confusables(\"length\", \"size\")]\n  1443:     pub fn len(&self) -> usize {\n  1444:         self.data.len()\n  1445:     }\n  1446: \n  1447:     /// Checks if the binary heap is empty.\n  1448:     ///\n  1449:     /// # Examples\n  1450:     ///\n  1451:     /// Basic usage:\n  1452:     ///\n  1453:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::new",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:982",
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
        "inputs": [],
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 979,
            "path": "BinaryHeap"
          }
        }
      }
    },
    "verification_source": "   498: \n   499: impl<T> BinaryHeap<T> {\n   500:     /// Creates an empty `BinaryHeap` as a max-heap.\n   501:     ///\n   502:     /// # Examples\n   503:     ///\n   504:     /// Basic usage:\n   505:     ///\n   506:     /// ```\n   507:     /// use std::collections::BinaryHeap;\n   508:     /// let mut heap = BinaryHeap::new();\n   509:     /// heap.push(4);\n   510:     /// ```\n   511:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   512:     #[rustc_const_stable(feature = \"const_binary_heap_constructor\", since = \"1.80.0\")]\n   513:     #[must_use]\n   514:     pub const fn new() -> BinaryHeap<T> {\n   515:         BinaryHeap { data: vec![] }\n   516:     }\n   517: \n   518:     /// Creates an empty `BinaryHeap` with at least the specified capacity.\n   519:     ///\n   520:     /// The binary heap will be able to hold at least `capacity` elements without\n   521:     /// reallocating. This method is allowed to allocate for more elements than\n   522:     /// `capacity`. If `capacity` is zero, the binary heap will not allocate.\n   523:     ///\n   524:     /// # Examples\n   525:     ///\n   526:     /// Basic usage:\n   527:     ///\n   528:     /// ```\n   529:     /// use std::collections::BinaryHeap;\n   530:     /// let mut heap = BinaryHeap::with_capacity(10);",
    "nanvix_source": "   504:     /// Basic usage:\n   505:     ///\n   506:     /// ```\n   507:     /// use std::collections::BinaryHeap;\n   508:     /// let mut heap = BinaryHeap::new();\n   509:     /// heap.push(4);\n   510:     /// ```\n   511:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   512:     #[rustc_const_stable(feature = \"const_binary_heap_constructor\", since = \"1.80.0\")]\n   513:     #[must_use]\n   514:     pub const fn new() -> BinaryHeap<T> {\n   515:         BinaryHeap { data: vec![] }\n   516:     }\n   517: \n   518:     /// Creates an empty `BinaryHeap` with at least the specified capacity.\n   519:     ///\n   520:     /// The binary heap will be able to hold at least `capacity` elements without\n   521:     /// reallocating. This method is allowed to allocate for more elements than\n   522:     /// `capacity`. If `capacity` is zero, the binary heap will not allocate.\n   523:     ///\n   524:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::peek",
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
      "name": "peek",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1131:     /// use std::collections::BinaryHeap;\n  1132:     /// let mut heap = BinaryHeap::new();\n  1133:     /// assert_eq!(heap.peek(), None);\n  1134:     ///\n  1135:     /// heap.push(1);\n  1136:     /// heap.push(5);\n  1137:     /// heap.push(2);\n  1138:     /// assert_eq!(heap.peek(), Some(&5));\n  1139:     ///\n  1140:     /// ```\n  1141:     ///\n  1142:     /// # Time complexity\n  1143:     ///\n  1144:     /// Cost is *O*(1) in the worst case.\n  1145:     #[must_use]\n  1146:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1147:     pub fn peek(&self) -> Option<&T> {\n  1148:         self.data.get(0)\n  1149:     }\n  1150: \n  1151:     /// Returns the number of elements the binary heap can hold without reallocating.\n  1152:     ///\n  1153:     /// # Examples\n  1154:     ///\n  1155:     /// Basic usage:\n  1156:     ///\n  1157:     /// ```\n  1158:     /// use std::collections::BinaryHeap;\n  1159:     /// let mut heap = BinaryHeap::with_capacity(100);\n  1160:     /// assert!(heap.capacity() >= 100);\n  1161:     /// heap.push(4);\n  1162:     /// ```\n  1163:     #[must_use]",
    "nanvix_source": "  1137:     /// heap.push(2);\n  1138:     /// assert_eq!(heap.peek(), Some(&5));\n  1139:     ///\n  1140:     /// ```\n  1141:     ///\n  1142:     /// # Time complexity\n  1143:     ///\n  1144:     /// Cost is *O*(1) in the worst case.\n  1145:     #[must_use]\n  1146:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1147:     pub fn peek(&self) -> Option<&T> {\n  1148:         self.data.get(0)\n  1149:     }\n  1150: \n  1151:     /// Returns the number of elements the binary heap can hold without reallocating.\n  1152:     ///\n  1153:     /// # Examples\n  1154:     ///\n  1155:     /// Basic usage:\n  1156:     ///\n  1157:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::peek_mut",
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
      "name": "peek_mut",
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'_"
                              },
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
                        "id": 987,
                        "path": "PeekMut"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   635:     /// assert!(heap.peek_mut().is_none());\n   636:     ///\n   637:     /// heap.push(1);\n   638:     /// heap.push(5);\n   639:     /// heap.push(2);\n   640:     /// if let Some(mut val) = heap.peek_mut() {\n   641:     ///     *val = 0;\n   642:     /// }\n   643:     /// assert_eq!(heap.peek(), Some(&2));\n   644:     /// ```\n   645:     ///\n   646:     /// # Time complexity\n   647:     ///\n   648:     /// If the item is modified then the worst case time complexity is *O*(log(*n*)),\n   649:     /// otherwise it's *O*(1).\n   650:     #[stable(feature = \"binary_heap_peek_mut\", since = \"1.12.0\")]\n   651:     pub fn peek_mut(&mut self) -> Option<PeekMut<'_, T, A>> {\n   652:         if self.is_empty() { None } else { Some(PeekMut { heap: self, original_len: None }) }\n   653:     }\n   654: \n   655:     /// Removes the greatest item from the binary heap and returns it, or `None` if it\n   656:     /// is empty.\n   657:     ///\n   658:     /// # Examples\n   659:     ///\n   660:     /// Basic usage:\n   661:     ///\n   662:     /// ```\n   663:     /// use std::collections::BinaryHeap;\n   664:     /// let mut heap = BinaryHeap::from([1, 3]);\n   665:     ///\n   666:     /// assert_eq!(heap.pop(), Some(3));\n   667:     /// assert_eq!(heap.pop(), Some(1));",
    "nanvix_source": "   641:     ///     *val = 0;\n   642:     /// }\n   643:     /// assert_eq!(heap.peek(), Some(&2));\n   644:     /// ```\n   645:     ///\n   646:     /// # Time complexity\n   647:     ///\n   648:     /// If the item is modified then the worst case time complexity is *O*(log(*n*)),\n   649:     /// otherwise it's *O*(1).\n   650:     #[stable(feature = \"binary_heap_peek_mut\", since = \"1.12.0\")]\n   651:     pub fn peek_mut(&mut self) -> Option<PeekMut<'_, T, A>> {\n   652:         if self.is_empty() { None } else { Some(PeekMut { heap: self, original_len: None }) }\n   653:     }\n   654: \n   655:     /// Removes the greatest item from the binary heap and returns it, or `None` if it\n   656:     /// is empty.\n   657:     ///\n   658:     /// # Examples\n   659:     ///\n   660:     /// Basic usage:\n   661:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::pop",
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
      "name": "pop",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   659:     ///\n   660:     /// Basic usage:\n   661:     ///\n   662:     /// ```\n   663:     /// use std::collections::BinaryHeap;\n   664:     /// let mut heap = BinaryHeap::from([1, 3]);\n   665:     ///\n   666:     /// assert_eq!(heap.pop(), Some(3));\n   667:     /// assert_eq!(heap.pop(), Some(1));\n   668:     /// assert_eq!(heap.pop(), None);\n   669:     /// ```\n   670:     ///\n   671:     /// # Time complexity\n   672:     ///\n   673:     /// The worst case cost of `pop` on a heap containing *n* elements is *O*(log(*n*)).\n   674:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   675:     pub fn pop(&mut self) -> Option<T> {\n   676:         self.data.pop().map(|mut item| {\n   677:             if !self.is_empty() {\n   678:                 swap(&mut item, &mut self.data[0]);\n   679:                 // SAFETY: !self.is_empty() means that self.len() > 0\n   680:                 unsafe { self.sift_down_to_bottom(0) };\n   681:             }\n   682:             item\n   683:         })\n   684:     }\n   685: \n   686:     /// Removes and returns the greatest item from the binary heap if the predicate\n   687:     /// returns `true`, or [`None`] if the predicate returns false or the heap\n   688:     /// is empty (the predicate will not be called in that case).\n   689:     ///\n   690:     /// # Examples\n   691:     ///",
    "nanvix_source": "   665:     ///\n   666:     /// assert_eq!(heap.pop(), Some(3));\n   667:     /// assert_eq!(heap.pop(), Some(1));\n   668:     /// assert_eq!(heap.pop(), None);\n   669:     /// ```\n   670:     ///\n   671:     /// # Time complexity\n   672:     ///\n   673:     /// The worst case cost of `pop` on a heap containing *n* elements is *O*(log(*n*)).\n   674:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   675:     pub fn pop(&mut self) -> Option<T> {\n   676:         self.data.pop().map(|mut item| {\n   677:             if !self.is_empty() {\n   678:                 swap(&mut item, &mut self.data[0]);\n   679:                 // SAFETY: !self.is_empty() means that self.len() > 0\n   680:                 unsafe { self.sift_down_to_bottom(0) };\n   681:             }\n   682:             item\n   683:         })\n   684:     }\n   685: ",
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
