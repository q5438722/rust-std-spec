For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BinaryHeap::retain",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [
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
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 534,
                      "path": "FnMut"
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
        "is_unsafe": false
      },
      "name": "retain",
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1045:     /// `false`. The elements are visited in unsorted (and unspecified) order.\n  1046:     ///\n  1047:     /// # Examples\n  1048:     ///\n  1049:     /// Basic usage:\n  1050:     ///\n  1051:     /// ```\n  1052:     /// use std::collections::BinaryHeap;\n  1053:     ///\n  1054:     /// let mut heap = BinaryHeap::from([-10, -5, 1, 2, 4, 13]);\n  1055:     ///\n  1056:     /// heap.retain(|x| x % 2 == 0); // only keep even numbers\n  1057:     ///\n  1058:     /// assert_eq!(heap.into_sorted_vec(), [-10, 2, 4])\n  1059:     /// ```\n  1060:     #[stable(feature = \"binary_heap_retain\", since = \"1.70.0\")]\n  1061:     pub fn retain<F>(&mut self, mut f: F)\n  1062:     where\n  1063:         F: FnMut(&T) -> bool,\n  1064:     {\n  1065:         // rebuild_start will be updated to the first touched element below, and the rebuild will\n  1066:         // only be done for the tail.\n  1067:         let mut guard = RebuildOnDrop { rebuild_from: self.len(), heap: self };\n  1068:         let mut i = 0;\n  1069: \n  1070:         guard.heap.data.retain(|e| {\n  1071:             let keep = f(e);\n  1072:             if !keep && i < guard.rebuild_from {\n  1073:                 guard.rebuild_from = i;\n  1074:             }\n  1075:             i += 1;\n  1076:             keep\n  1077:         });",
    "nanvix_source": "  1051:     /// ```\n  1052:     /// use std::collections::BinaryHeap;\n  1053:     ///\n  1054:     /// let mut heap = BinaryHeap::from([-10, -5, 1, 2, 4, 13]);\n  1055:     ///\n  1056:     /// heap.retain(|x| x % 2 == 0); // only keep even numbers\n  1057:     ///\n  1058:     /// assert_eq!(heap.into_sorted_vec(), [-10, 2, 4])\n  1059:     /// ```\n  1060:     #[stable(feature = \"binary_heap_retain\", since = \"1.70.0\")]\n  1061:     pub fn retain<F>(&mut self, mut f: F)\n  1062:     where\n  1063:         F: FnMut(&T) -> bool,\n  1064:     {\n  1065:         // rebuild_start will be updated to the first touched element below, and the rebuild will\n  1066:         // only be done for the tail.\n  1067:         let mut guard = RebuildOnDrop { rebuild_from: self.len(), heap: self };\n  1068:         let mut i = 0;\n  1069: \n  1070:         guard.heap.data.retain(|e| {\n  1071:             let keep = f(e);",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::extract_if",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 534,
                      "path": "FnMut"
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
        "is_unsafe": false
      },
      "name": "extract_if",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
            "filter",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
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
            "id": 2545,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "  1148:     ///\n  1149:     /// Splitting a list into even and odd values, reusing the original list:\n  1150:     ///\n  1151:     /// ```\n  1152:     /// use std::collections::LinkedList;\n  1153:     ///\n  1154:     /// let mut numbers: LinkedList<u32> = LinkedList::new();\n  1155:     /// numbers.extend(&[1, 2, 3, 4, 5, 6, 8, 9, 11, 13, 14, 15]);\n  1156:     ///\n  1157:     /// let evens = numbers.extract_if(|x| *x % 2 == 0).collect::<LinkedList<_>>();\n  1158:     /// let odds = numbers;\n  1159:     ///\n  1160:     /// assert_eq!(evens.into_iter().collect::<Vec<_>>(), vec![2, 4, 6, 8, 14]);\n  1161:     /// assert_eq!(odds.into_iter().collect::<Vec<_>>(), vec![1, 3, 5, 9, 11, 13, 15]);\n  1162:     /// ```\n  1163:     #[stable(feature = \"extract_if\", since = \"1.87.0\")]\n  1164:     pub fn extract_if<F>(&mut self, filter: F) -> ExtractIf<'_, T, F, A>\n  1165:     where\n  1166:         F: FnMut(&mut T) -> bool,\n  1167:     {\n  1168:         // avoid borrow issues.\n  1169:         let it = self.head;\n  1170:         let old_len = self.len;\n  1171: \n  1172:         ExtractIf { list: self, it, pred: filter, idx: 0, old_len }\n  1173:     }\n  1174: }\n  1175: \n  1176: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1177: unsafe impl<#[may_dangle] T, A: Allocator> Drop for LinkedList<T, A> {\n  1178:     fn drop(&mut self) {\n  1179:         struct DropGuard<'a, T, A: Allocator>(&'a mut LinkedList<T, A>);\n  1180: ",
    "nanvix_source": "  1154:     /// let mut numbers: LinkedList<u32> = LinkedList::new();\n  1155:     /// numbers.extend(&[1, 2, 3, 4, 5, 6, 8, 9, 11, 13, 14, 15]);\n  1156:     ///\n  1157:     /// let evens = numbers.extract_if(|x| *x % 2 == 0).collect::<LinkedList<_>>();\n  1158:     /// let odds = numbers;\n  1159:     ///\n  1160:     /// assert_eq!(evens.into_iter().collect::<Vec<_>>(), vec![2, 4, 6, 8, 14]);\n  1161:     /// assert_eq!(odds.into_iter().collect::<Vec<_>>(), vec![1, 3, 5, 9, 11, 13, 15]);\n  1162:     /// ```\n  1163:     #[stable(feature = \"extract_if\", since = \"1.87.0\")]\n  1164:     pub fn extract_if<F>(&mut self, filter: F) -> ExtractIf<'_, T, F, A>\n  1165:     where\n  1166:         F: FnMut(&mut T) -> bool,\n  1167:     {\n  1168:         // avoid borrow issues.\n  1169:         let it = self.head;\n  1170:         let old_len = self.len;\n  1171: \n  1172:         ExtractIf { list: self, it, pred: filter, idx: 0, old_len }\n  1173:     }\n  1174: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::iter",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
      "name": "iter",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2518,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "   524:     /// use std::collections::LinkedList;\n   525:     ///\n   526:     /// let mut list: LinkedList<u32> = LinkedList::new();\n   527:     ///\n   528:     /// list.push_back(0);\n   529:     /// list.push_back(1);\n   530:     /// list.push_back(2);\n   531:     ///\n   532:     /// let mut iter = list.iter();\n   533:     /// assert_eq!(iter.next(), Some(&0));\n   534:     /// assert_eq!(iter.next(), Some(&1));\n   535:     /// assert_eq!(iter.next(), Some(&2));\n   536:     /// assert_eq!(iter.next(), None);\n   537:     /// ```\n   538:     #[inline]\n   539:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   540:     pub fn iter(&self) -> Iter<'_, T> {\n   541:         Iter { head: self.head, tail: self.tail, len: self.len, marker: PhantomData }\n   542:     }\n   543: \n   544:     /// Provides a forward iterator with mutable references.\n   545:     ///\n   546:     /// # Examples\n   547:     ///\n   548:     /// ```\n   549:     /// use std::collections::LinkedList;\n   550:     ///\n   551:     /// let mut list: LinkedList<u32> = LinkedList::new();\n   552:     ///\n   553:     /// list.push_back(0);\n   554:     /// list.push_back(1);\n   555:     /// list.push_back(2);\n   556:     ///",
    "nanvix_source": "   530:     /// list.push_back(2);\n   531:     ///\n   532:     /// let mut iter = list.iter();\n   533:     /// assert_eq!(iter.next(), Some(&0));\n   534:     /// assert_eq!(iter.next(), Some(&1));\n   535:     /// assert_eq!(iter.next(), Some(&2));\n   536:     /// assert_eq!(iter.next(), None);\n   537:     /// ```\n   538:     #[inline]\n   539:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   540:     pub fn iter(&self) -> Iter<'_, T> {\n   541:         Iter { head: self.head, tail: self.tail, len: self.len, marker: PhantomData }\n   542:     }\n   543: \n   544:     /// Provides a forward iterator with mutable references.\n   545:     ///\n   546:     /// # Examples\n   547:     ///\n   548:     /// ```\n   549:     /// use std::collections::LinkedList;\n   550:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::iter_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
      "name": "iter_mut",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2520,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "   553:     /// list.push_back(0);\n   554:     /// list.push_back(1);\n   555:     /// list.push_back(2);\n   556:     ///\n   557:     /// for element in list.iter_mut() {\n   558:     ///     *element += 10;\n   559:     /// }\n   560:     ///\n   561:     /// let mut iter = list.iter();\n   562:     /// assert_eq!(iter.next(), Some(&10));\n   563:     /// assert_eq!(iter.next(), Some(&11));\n   564:     /// assert_eq!(iter.next(), Some(&12));\n   565:     /// assert_eq!(iter.next(), None);\n   566:     /// ```\n   567:     #[inline]\n   568:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   569:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n   570:         IterMut { head: self.head, tail: self.tail, len: self.len, marker: PhantomData }\n   571:     }\n   572: \n   573:     /// Provides a cursor at the front element.\n   574:     ///\n   575:     /// The cursor is pointing to the \"ghost\" non-element if the list is empty.\n   576:     #[inline]\n   577:     #[must_use]\n   578:     #[unstable(feature = \"linked_list_cursors\", issue = \"58533\")]\n   579:     pub fn cursor_front(&self) -> Cursor<'_, T, A> {\n   580:         Cursor { index: 0, current: self.head, list: self }\n   581:     }\n   582: \n   583:     /// Provides a cursor with editing operations at the front element.\n   584:     ///\n   585:     /// The cursor is pointing to the \"ghost\" non-element if the list is empty.",
    "nanvix_source": "   559:     /// }\n   560:     ///\n   561:     /// let mut iter = list.iter();\n   562:     /// assert_eq!(iter.next(), Some(&10));\n   563:     /// assert_eq!(iter.next(), Some(&11));\n   564:     /// assert_eq!(iter.next(), Some(&12));\n   565:     /// assert_eq!(iter.next(), None);\n   566:     /// ```\n   567:     #[inline]\n   568:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   569:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n   570:         IterMut { head: self.head, tail: self.tail, len: self.len, marker: PhantomData }\n   571:     }\n   572: \n   573:     /// Provides a cursor at the front element.\n   574:     ///\n   575:     /// The cursor is pointing to the \"ghost\" non-element if the list is empty.\n   576:     #[inline]\n   577:     #[must_use]\n   578:     #[unstable(feature = \"linked_list_cursors\", issue = \"58533\")]\n   579:     pub fn cursor_front(&self) -> Cursor<'_, T, A> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::drain",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "primitive": "usize"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 1409,
                      "path": "RangeBounds"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "R"
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
      "name": "drain",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "range",
            {
              "generic": "R"
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
            "id": 2819,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "  1798:     /// # Examples\n  1799:     ///\n  1800:     /// ```\n  1801:     /// use std::collections::VecDeque;\n  1802:     ///\n  1803:     /// let mut deque: VecDeque<_> = [1, 2, 3].into();\n  1804:     /// let drained = deque.drain(2..).collect::<VecDeque<_>>();\n  1805:     /// assert_eq!(drained, [3]);\n  1806:     /// assert_eq!(deque, [1, 2]);\n  1807:     ///\n  1808:     /// // A full range clears all contents, like `clear()` does\n  1809:     /// deque.drain(..);\n  1810:     /// assert!(deque.is_empty());\n  1811:     /// ```\n  1812:     #[inline]\n  1813:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1814:     pub fn drain<R>(&mut self, range: R) -> Drain<'_, T, A>\n  1815:     where\n  1816:         R: RangeBounds<usize>,\n  1817:     {\n  1818:         // Memory safety\n  1819:         //\n  1820:         // When the Drain is first created, the source deque is shortened to\n  1821:         // make sure no uninitialized or moved-from elements are accessible at\n  1822:         // all if the Drain's destructor never gets to run.\n  1823:         //\n  1824:         // Drain will ptr::read out the values to remove.\n  1825:         // When finished, the remaining data will be copied back to cover the hole,\n  1826:         // and the head/tail values will be restored correctly.\n  1827:         //\n  1828:         let Range { start, end } = slice::range(range, ..self.len);\n  1829:         let drain_start = start;\n  1830:         let drain_len = end - start;",
    "nanvix_source": "  1868:     /// let drained = deque.drain(2..).collect::<VecDeque<_>>();\n  1869:     /// assert_eq!(drained, [3]);\n  1870:     /// assert_eq!(deque, [1, 2]);\n  1871:     ///\n  1872:     /// // A full range clears all contents, like `clear()` does\n  1873:     /// deque.drain(..);\n  1874:     /// assert!(deque.is_empty());\n  1875:     /// ```\n  1876:     #[inline]\n  1877:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1878:     pub fn drain<R>(&mut self, range: R) -> Drain<'_, T, A>\n  1879:     where\n  1880:         R: RangeBounds<usize>,\n  1881:     {\n  1882:         // Memory safety\n  1883:         //\n  1884:         // When the Drain is first created, the source deque is shortened to\n  1885:         // make sure no uninitialized or moved-from elements are accessible at\n  1886:         // all if the Drain's destructor never gets to run.\n  1887:         //\n  1888:         // Drain will ptr::read out the values to remove.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::iter_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
      "name": "iter_mut",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2885,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  1512:     /// # Examples\n  1513:     ///\n  1514:     /// ```\n  1515:     /// use std::collections::VecDeque;\n  1516:     ///\n  1517:     /// let mut buf = VecDeque::new();\n  1518:     /// buf.push_back(5);\n  1519:     /// buf.push_back(3);\n  1520:     /// buf.push_back(4);\n  1521:     /// for num in buf.iter_mut() {\n  1522:     ///     *num = *num - 2;\n  1523:     /// }\n  1524:     /// let b: &[_] = &[&mut 3, &mut 1, &mut 2];\n  1525:     /// assert_eq!(&buf.iter_mut().collect::<Vec<&mut i32>>()[..], b);\n  1526:     /// ```\n  1527:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1528:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1529:         let (a, b) = self.as_mut_slices();\n  1530:         IterMut::new(a.iter_mut(), b.iter_mut())\n  1531:     }\n  1532: \n  1533:     /// Returns a pair of slices which contain, in order, the contents of the\n  1534:     /// deque.\n  1535:     ///\n  1536:     /// If [`make_contiguous`] was previously called, all elements of the\n  1537:     /// deque will be in the first slice and the second slice will be empty.\n  1538:     /// Otherwise, the exact split point depends on implementation details\n  1539:     /// and is not guaranteed.\n  1540:     ///\n  1541:     /// [`make_contiguous`]: VecDeque::make_contiguous\n  1542:     ///\n  1543:     /// # Examples\n  1544:     ///",
    "nanvix_source": "  1582:     /// buf.push_back(5);\n  1583:     /// buf.push_back(3);\n  1584:     /// buf.push_back(4);\n  1585:     /// for num in buf.iter_mut() {\n  1586:     ///     *num = *num - 2;\n  1587:     /// }\n  1588:     /// let b: &[_] = &[&mut 3, &mut 1, &mut 2];\n  1589:     /// assert_eq!(&buf.iter_mut().collect::<Vec<&mut i32>>()[..], b);\n  1590:     /// ```\n  1591:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1592:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1593:         let (a, b) = self.as_mut_slices();\n  1594:         IterMut::new(a.iter_mut(), b.iter_mut())\n  1595:     }\n  1596: \n  1597:     /// Returns a pair of slices which contain, in order, the contents of the\n  1598:     /// deque.\n  1599:     ///\n  1600:     /// If [`make_contiguous`] was previously called, all elements of the\n  1601:     /// deque will be in the first slice and the second slice will be empty.\n  1602:     /// Otherwise, the exact split point depends on implementation details",
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
