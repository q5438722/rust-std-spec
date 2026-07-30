For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::LinkedList::push_front",
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
      "name": "push_front",
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
            "elt",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   830:     /// This operation should compute in *O*(1) time.\n   831:     ///\n   832:     /// # Examples\n   833:     ///\n   834:     /// ```\n   835:     /// use std::collections::LinkedList;\n   836:     ///\n   837:     /// let mut dl = LinkedList::new();\n   838:     ///\n   839:     /// dl.push_front(2);\n   840:     /// assert_eq!(dl.front().unwrap(), &2);\n   841:     ///\n   842:     /// dl.push_front(1);\n   843:     /// assert_eq!(dl.front().unwrap(), &1);\n   844:     /// ```\n   845:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   846:     pub fn push_front(&mut self, elt: T) {\n   847:         let _ = self.push_front_mut(elt);\n   848:     }\n   849: \n   850:     /// Adds an element to the front of the list, returning a reference to it.\n   851:     ///\n   852:     /// This operation should compute in *O*(1) time.\n   853:     ///\n   854:     /// # Examples\n   855:     ///\n   856:     /// ```\n   857:     /// use std::collections::LinkedList;\n   858:     ///\n   859:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   860:     ///\n   861:     /// let ptr = dl.push_front_mut(2);\n   862:     /// *ptr += 4;",
    "nanvix_source": "   836:     ///\n   837:     /// let mut dl = LinkedList::new();\n   838:     ///\n   839:     /// dl.push_front(2);\n   840:     /// assert_eq!(dl.front().unwrap(), &2);\n   841:     ///\n   842:     /// dl.push_front(1);\n   843:     /// assert_eq!(dl.front().unwrap(), &1);\n   844:     /// ```\n   845:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   846:     pub fn push_front(&mut self, elt: T) {\n   847:         let _ = self.push_front_mut(elt);\n   848:     }\n   849: \n   850:     /// Adds an element to the front of the list, returning a reference to it.\n   851:     ///\n   852:     /// This operation should compute in *O*(1) time.\n   853:     ///\n   854:     /// # Examples\n   855:     ///\n   856:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::split_off",
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
                      "id": 25,
                      "path": "Clone"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "A"
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
      "name": "split_off",
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
            "at",
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
        }
      }
    },
    "verification_source": "   979:     ///\n   980:     /// ```\n   981:     /// use std::collections::LinkedList;\n   982:     ///\n   983:     /// let mut d = LinkedList::new();\n   984:     ///\n   985:     /// d.push_front(1);\n   986:     /// d.push_front(2);\n   987:     /// d.push_front(3);\n   988:     ///\n   989:     /// let mut split = d.split_off(2);\n   990:     ///\n   991:     /// assert_eq!(split.pop_front(), Some(1));\n   992:     /// assert_eq!(split.pop_front(), None);\n   993:     /// ```\n   994:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   995:     pub fn split_off(&mut self, at: usize) -> LinkedList<T, A>\n   996:     where\n   997:         A: Clone,\n   998:     {\n   999:         let len = self.len();\n  1000:         assert!(at <= len, \"Cannot split off at a nonexistent index\");\n  1001:         if at == 0 {\n  1002:             return mem::replace(self, Self::new_in(self.alloc.clone()));\n  1003:         } else if at == len {\n  1004:             return Self::new_in(self.alloc.clone());\n  1005:         }\n  1006: \n  1007:         // Below, we iterate towards the `i-1`th node, either from the start or the end,\n  1008:         // depending on which would be faster.\n  1009:         let split_node = if at - 1 <= len - 1 - (at - 1) {\n  1010:             let mut iter = self.iter_mut();\n  1011:             // instead of skipping using .skip() (which creates a new struct),",
    "nanvix_source": "   985:     /// d.push_front(1);\n   986:     /// d.push_front(2);\n   987:     /// d.push_front(3);\n   988:     ///\n   989:     /// let mut split = d.split_off(2);\n   990:     ///\n   991:     /// assert_eq!(split.pop_front(), Some(1));\n   992:     /// assert_eq!(split.pop_front(), None);\n   993:     /// ```\n   994:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   995:     pub fn split_off(&mut self, at: usize) -> LinkedList<T, A>\n   996:     where\n   997:         A: Clone,\n   998:     {\n   999:         let len = self.len();\n  1000:         assert!(at <= len, \"Cannot split off at a nonexistent index\");\n  1001:         if at == 0 {\n  1002:             return mem::replace(self, Self::new_in(self.alloc.clone()));\n  1003:         } else if at == len {\n  1004:             return Self::new_in(self.alloc.clone());\n  1005:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::as_slices",
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
      "name": "as_slices",
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
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            },
            {
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
          ]
        }
      }
    },
    "verification_source": "  1553:     ///\n  1554:     /// let expected = [0, 1, 2];\n  1555:     /// let (front, back) = deque.as_slices();\n  1556:     /// assert_eq!(&expected[..front.len()], front);\n  1557:     /// assert_eq!(&expected[front.len()..], back);\n  1558:     ///\n  1559:     /// deque.push_front(10);\n  1560:     /// deque.push_front(9);\n  1561:     ///\n  1562:     /// let expected = [9, 10, 0, 1, 2];\n  1563:     /// let (front, back) = deque.as_slices();\n  1564:     /// assert_eq!(&expected[..front.len()], front);\n  1565:     /// assert_eq!(&expected[front.len()..], back);\n  1566:     /// ```\n  1567:     #[inline]\n  1568:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1569:     pub fn as_slices(&self) -> (&[T], &[T]) {\n  1570:         let (a_range, b_range) = self.slice_ranges(.., self.len);\n  1571:         // SAFETY: `slice_ranges` always returns valid ranges into\n  1572:         // the physical buffer.\n  1573:         unsafe { (&*self.buffer_range(a_range), &*self.buffer_range(b_range)) }\n  1574:     }\n  1575: \n  1576:     /// Returns a pair of slices which contain, in order, the contents of the\n  1577:     /// deque.\n  1578:     ///\n  1579:     /// If [`make_contiguous`] was previously called, all elements of the\n  1580:     /// deque will be in the first slice and the second slice will be empty.\n  1581:     /// Otherwise, the exact split point depends on implementation details\n  1582:     /// and is not guaranteed.\n  1583:     ///\n  1584:     /// [`make_contiguous`]: VecDeque::make_contiguous\n  1585:     ///",
    "nanvix_source": "  1623:     /// deque.push_front(10);\n  1624:     /// deque.push_front(9);\n  1625:     ///\n  1626:     /// let expected = [9, 10, 0, 1, 2];\n  1627:     /// let (front, back) = deque.as_slices();\n  1628:     /// assert_eq!(&expected[..front.len()], front);\n  1629:     /// assert_eq!(&expected[front.len()..], back);\n  1630:     /// ```\n  1631:     #[inline]\n  1632:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1633:     pub fn as_slices(&self) -> (&[T], &[T]) {\n  1634:         let (a_range, b_range) = self.slice_ranges(.., self.len);\n  1635:         // SAFETY: `slice_ranges` always returns valid ranges into\n  1636:         // the physical buffer.\n  1637:         unsafe { (&*self.buffer_range(a_range), &*self.buffer_range(b_range)) }\n  1638:     }\n  1639: \n  1640:     /// Returns a pair of slices which contain, in order, the contents of the\n  1641:     /// deque.\n  1642:     ///\n  1643:     /// If [`make_contiguous`] was previously called, all elements of the",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::back",
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
      "name": "back",
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
    "verification_source": "  2009:     /// empty.\n  2010:     ///\n  2011:     /// # Examples\n  2012:     ///\n  2013:     /// ```\n  2014:     /// use std::collections::VecDeque;\n  2015:     ///\n  2016:     /// let mut d = VecDeque::new();\n  2017:     /// assert_eq!(d.back(), None);\n  2018:     ///\n  2019:     /// d.push_back(1);\n  2020:     /// d.push_back(2);\n  2021:     /// assert_eq!(d.back(), Some(&2));\n  2022:     /// ```\n  2023:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2024:     #[rustc_confusables(\"last\")]\n  2025:     pub fn back(&self) -> Option<&T> {\n  2026:         self.get(self.len.wrapping_sub(1))\n  2027:     }\n  2028: \n  2029:     /// Provides a mutable reference to the back element, or `None` if the\n  2030:     /// deque is empty.\n  2031:     ///\n  2032:     /// # Examples\n  2033:     ///\n  2034:     /// ```\n  2035:     /// use std::collections::VecDeque;\n  2036:     ///\n  2037:     /// let mut d = VecDeque::new();\n  2038:     /// assert_eq!(d.back(), None);\n  2039:     ///\n  2040:     /// d.push_back(1);\n  2041:     /// d.push_back(2);",
    "nanvix_source": "  2079:     ///\n  2080:     /// let mut d = VecDeque::new();\n  2081:     /// assert_eq!(d.back(), None);\n  2082:     ///\n  2083:     /// d.push_back(1);\n  2084:     /// d.push_back(2);\n  2085:     /// assert_eq!(d.back(), Some(&2));\n  2086:     /// ```\n  2087:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2088:     #[rustc_confusables(\"last\")]\n  2089:     pub fn back(&self) -> Option<&T> {\n  2090:         self.get(self.len.wrapping_sub(1))\n  2091:     }\n  2092: \n  2093:     /// Provides a mutable reference to the back element, or `None` if the\n  2094:     /// deque is empty.\n  2095:     ///\n  2096:     /// # Examples\n  2097:     ///\n  2098:     /// ```\n  2099:     /// use std::collections::VecDeque;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::binary_search",
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
                      "id": 176,
                      "path": "Ord"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "binary_search",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "x",
            {
              "borrowed_ref": {
                "is_mutable": false,
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  },
                  {
                    "type": {
                      "primitive": "usize"
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
    "verification_source": "  3103:     /// sort order, consider using [`partition_point`]:\n  3104:     ///\n  3105:     /// ```\n  3106:     /// use std::collections::VecDeque;\n  3107:     ///\n  3108:     /// let mut deque: VecDeque<_> = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55].into();\n  3109:     /// let num = 42;\n  3110:     /// let idx = deque.partition_point(|&x| x <= num);\n  3111:     /// // If `num` is unique, `s.partition_point(|&x| x < num)` (with `<`) is equivalent to\n  3112:     /// // `s.binary_search(&num).unwrap_or_else(|x| x)`, but using `<=` may allow `insert`\n  3113:     /// // to shift less elements.\n  3114:     /// deque.insert(idx, num);\n  3115:     /// assert_eq!(deque, &[0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  3116:     /// ```\n  3117:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3118:     #[inline]\n  3119:     pub fn binary_search(&self, x: &T) -> Result<usize, usize>\n  3120:     where\n  3121:         T: Ord,\n  3122:     {\n  3123:         self.binary_search_by(|e| e.cmp(x))\n  3124:     }\n  3125: \n  3126:     /// Binary searches this `VecDeque` with a comparator function.\n  3127:     ///\n  3128:     /// The comparator function should return an order code that indicates\n  3129:     /// whether its argument is `Less`, `Equal` or `Greater` the desired\n  3130:     /// target.\n  3131:     /// If the `VecDeque` is not sorted or if the comparator function does not\n  3132:     /// implement an order consistent with the sort order of the underlying\n  3133:     /// `VecDeque`, the returned result is unspecified and meaningless.\n  3134:     ///\n  3135:     /// If the value is found then [`Result::Ok`] is returned, containing the",
    "nanvix_source": "  3191:     /// let num = 42;\n  3192:     /// let idx = deque.partition_point(|&x| x <= num);\n  3193:     /// // If `num` is unique, `s.partition_point(|&x| x < num)` (with `<`) is equivalent to\n  3194:     /// // `s.binary_search(&num).unwrap_or_else(|x| x)`, but using `<=` may allow `insert`\n  3195:     /// // to shift less elements.\n  3196:     /// deque.insert(idx, num);\n  3197:     /// assert_eq!(deque, &[0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  3198:     /// ```\n  3199:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3200:     #[inline]\n  3201:     pub fn binary_search(&self, x: &T) -> Result<usize, usize>\n  3202:     where\n  3203:         T: Ord,\n  3204:     {\n  3205:         self.binary_search_by(|e| e.cmp(x))\n  3206:     }\n  3207: \n  3208:     /// Binary searches this `VecDeque` with a comparator function.\n  3209:     ///\n  3210:     /// The comparator function should return an order code that indicates\n  3211:     /// whether its argument is `Less`, `Equal` or `Greater` the desired",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::contains",
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
                                "generic": "T"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 179,
                      "path": "PartialEq"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "contains",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "x",
            {
              "borrowed_ref": {
                "is_mutable": false,
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1939:     /// [`binary_search`]: VecDeque::binary_search\n  1940:     ///\n  1941:     /// # Examples\n  1942:     ///\n  1943:     /// ```\n  1944:     /// use std::collections::VecDeque;\n  1945:     ///\n  1946:     /// let mut deque: VecDeque<u32> = VecDeque::new();\n  1947:     ///\n  1948:     /// deque.push_back(0);\n  1949:     /// deque.push_back(1);\n  1950:     ///\n  1951:     /// assert_eq!(deque.contains(&1), true);\n  1952:     /// assert_eq!(deque.contains(&10), false);\n  1953:     /// ```\n  1954:     #[stable(feature = \"vec_deque_contains\", since = \"1.12.0\")]\n  1955:     pub fn contains(&self, x: &T) -> bool\n  1956:     where\n  1957:         T: PartialEq<T>,\n  1958:     {\n  1959:         let (a, b) = self.as_slices();\n  1960:         a.contains(x) || b.contains(x)\n  1961:     }\n  1962: \n  1963:     /// Provides a reference to the front element, or `None` if the deque is\n  1964:     /// empty.\n  1965:     ///\n  1966:     /// # Examples\n  1967:     ///\n  1968:     /// ```\n  1969:     /// use std::collections::VecDeque;\n  1970:     ///\n  1971:     /// let mut d = VecDeque::new();",
    "nanvix_source": "  2009:     ///\n  2010:     /// let mut deque: VecDeque<u32> = VecDeque::new();\n  2011:     ///\n  2012:     /// deque.push_back(0);\n  2013:     /// deque.push_back(1);\n  2014:     ///\n  2015:     /// assert_eq!(deque.contains(&1), true);\n  2016:     /// assert_eq!(deque.contains(&10), false);\n  2017:     /// ```\n  2018:     #[stable(feature = \"vec_deque_contains\", since = \"1.12.0\")]\n  2019:     pub fn contains(&self, x: &T) -> bool\n  2020:     where\n  2021:         T: PartialEq<T>,\n  2022:     {\n  2023:         let (a, b) = self.as_slices();\n  2024:         a.contains(x) || b.contains(x)\n  2025:     }\n  2026: \n  2027:     /// Provides a reference to the front element, or `None` if the deque is\n  2028:     /// empty.\n  2029:     ///",
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
