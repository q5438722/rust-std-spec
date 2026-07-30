For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::LinkedList::push_front_mut",
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
      "name": "push_front_mut",
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
    "verification_source": "   851:     ///\n   852:     /// This operation should compute in *O*(1) time.\n   853:     ///\n   854:     /// # Examples\n   855:     ///\n   856:     /// ```\n   857:     /// use std::collections::LinkedList;\n   858:     ///\n   859:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   860:     ///\n   861:     /// let ptr = dl.push_front_mut(2);\n   862:     /// *ptr += 4;\n   863:     /// assert_eq!(dl.front().unwrap(), &6);\n   864:     /// ```\n   865:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n   866:     #[must_use = \"if you don't need a reference to the value, use `LinkedList::push_front` instead\"]\n   867:     pub fn push_front_mut(&mut self, elt: T) -> &mut T {\n   868:         let mut node =\n   869:             Box::into_non_null_with_allocator(Box::new_in(Node::new(elt), &self.alloc)).0;\n   870:         // SAFETY: node is a unique pointer to a node in self.alloc\n   871:         unsafe {\n   872:             self.push_front_node(node);\n   873:             &mut node.as_mut().element\n   874:         }\n   875:     }\n   876: \n   877:     /// Removes the first element and returns it, or `None` if the list is\n   878:     /// empty.\n   879:     ///\n   880:     /// This operation should compute in *O*(1) time.\n   881:     ///\n   882:     /// # Examples\n   883:     ///",
    "nanvix_source": "   857:     /// use std::collections::LinkedList;\n   858:     ///\n   859:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   860:     ///\n   861:     /// let ptr = dl.push_front_mut(2);\n   862:     /// *ptr += 4;\n   863:     /// assert_eq!(dl.front().unwrap(), &6);\n   864:     /// ```\n   865:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n   866:     #[must_use = \"if you don't need a reference to the value, use `LinkedList::push_front` instead\"]\n   867:     pub fn push_front_mut(&mut self, elt: T) -> &mut T {\n   868:         let mut node =\n   869:             Box::into_non_null_with_allocator(Box::new_in(Node::new(elt), &self.alloc)).0;\n   870:         // SAFETY: node is a unique pointer to a node in self.alloc\n   871:         unsafe {\n   872:             self.push_front_node(node);\n   873:             &mut node.as_mut().element\n   874:         }\n   875:     }\n   876: \n   877:     /// Removes the first element and returns it, or `None` if the list is",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::as_mut_slices",
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
      "name": "as_mut_slices",
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
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": true,
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
                "is_mutable": true,
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
    "verification_source": "  1602:     ///     let (front, back) = deque.as_mut_slices();\n  1603:     ///     if index > front.len() - 1 {\n  1604:     ///         back[index - front.len()] = val;\n  1605:     ///     } else {\n  1606:     ///         front[index] = val;\n  1607:     ///     }\n  1608:     /// };\n  1609:     ///\n  1610:     /// update_nth(0, 42);\n  1611:     /// update_nth(2, 24);\n  1612:     ///\n  1613:     /// let v: Vec<_> = deque.into();\n  1614:     /// assert_eq!(v, [42, 10, 24, 1]);\n  1615:     /// ```\n  1616:     #[inline]\n  1617:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1618:     pub fn as_mut_slices(&mut self) -> (&mut [T], &mut [T]) {\n  1619:         let (a_range, b_range) = self.slice_ranges(.., self.len);\n  1620:         // SAFETY: `slice_ranges` always returns valid ranges into\n  1621:         // the physical buffer.\n  1622:         unsafe { (&mut *self.buffer_range(a_range), &mut *self.buffer_range(b_range)) }\n  1623:     }\n  1624: \n  1625:     /// Returns the number of elements in the deque.\n  1626:     ///\n  1627:     /// # Examples\n  1628:     ///\n  1629:     /// ```\n  1630:     /// use std::collections::VecDeque;\n  1631:     ///\n  1632:     /// let mut deque = VecDeque::new();\n  1633:     /// assert_eq!(deque.len(), 0);\n  1634:     /// deque.push_back(1);",
    "nanvix_source": "  1672:     /// };\n  1673:     ///\n  1674:     /// update_nth(0, 42);\n  1675:     /// update_nth(2, 24);\n  1676:     ///\n  1677:     /// let v: Vec<_> = deque.into();\n  1678:     /// assert_eq!(v, [42, 10, 24, 1]);\n  1679:     /// ```\n  1680:     #[inline]\n  1681:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1682:     pub fn as_mut_slices(&mut self) -> (&mut [T], &mut [T]) {\n  1683:         let (a_range, b_range) = self.slice_ranges(.., self.len);\n  1684:         // SAFETY: `slice_ranges` always returns valid ranges into\n  1685:         // the physical buffer.\n  1686:         unsafe { (&mut *self.buffer_range(a_range), &mut *self.buffer_range(b_range)) }\n  1687:     }\n  1688: \n  1689:     /// Returns the number of elements in the deque.\n  1690:     ///\n  1691:     /// # Examples\n  1692:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::back_mut",
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
      "name": "back_mut",
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
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
    "verification_source": "  2033:     ///\n  2034:     /// ```\n  2035:     /// use std::collections::VecDeque;\n  2036:     ///\n  2037:     /// let mut d = VecDeque::new();\n  2038:     /// assert_eq!(d.back(), None);\n  2039:     ///\n  2040:     /// d.push_back(1);\n  2041:     /// d.push_back(2);\n  2042:     /// match d.back_mut() {\n  2043:     ///     Some(x) => *x = 9,\n  2044:     ///     None => (),\n  2045:     /// }\n  2046:     /// assert_eq!(d.back(), Some(&9));\n  2047:     /// ```\n  2048:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2049:     pub fn back_mut(&mut self) -> Option<&mut T> {\n  2050:         self.get_mut(self.len.wrapping_sub(1))\n  2051:     }\n  2052: \n  2053:     /// Removes the first element and returns it, or `None` if the deque is\n  2054:     /// empty.\n  2055:     ///\n  2056:     /// # Examples\n  2057:     ///\n  2058:     /// ```\n  2059:     /// use std::collections::VecDeque;\n  2060:     ///\n  2061:     /// let mut d = VecDeque::new();\n  2062:     /// d.push_back(1);\n  2063:     /// d.push_back(2);\n  2064:     ///\n  2065:     /// assert_eq!(d.pop_front(), Some(1));",
    "nanvix_source": "  2103:     ///\n  2104:     /// d.push_back(1);\n  2105:     /// d.push_back(2);\n  2106:     /// match d.back_mut() {\n  2107:     ///     Some(x) => *x = 9,\n  2108:     ///     None => (),\n  2109:     /// }\n  2110:     /// assert_eq!(d.back(), Some(&9));\n  2111:     /// ```\n  2112:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2113:     pub fn back_mut(&mut self) -> Option<&mut T> {\n  2114:         self.get_mut(self.len.wrapping_sub(1))\n  2115:     }\n  2116: \n  2117:     /// Removes the first element and returns it, or `None` if the deque is\n  2118:     /// empty.\n  2119:     ///\n  2120:     /// # Examples\n  2121:     ///\n  2122:     /// ```\n  2123:     /// use std::collections::VecDeque;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::front_mut",
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
      "name": "front_mut",
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
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
    "verification_source": "  1988:     ///\n  1989:     /// ```\n  1990:     /// use std::collections::VecDeque;\n  1991:     ///\n  1992:     /// let mut d = VecDeque::new();\n  1993:     /// assert_eq!(d.front_mut(), None);\n  1994:     ///\n  1995:     /// d.push_back(1);\n  1996:     /// d.push_back(2);\n  1997:     /// match d.front_mut() {\n  1998:     ///     Some(x) => *x = 9,\n  1999:     ///     None => (),\n  2000:     /// }\n  2001:     /// assert_eq!(d.front(), Some(&9));\n  2002:     /// ```\n  2003:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2004:     pub fn front_mut(&mut self) -> Option<&mut T> {\n  2005:         self.get_mut(0)\n  2006:     }\n  2007: \n  2008:     /// Provides a reference to the back element, or `None` if the deque is\n  2009:     /// empty.\n  2010:     ///\n  2011:     /// # Examples\n  2012:     ///\n  2013:     /// ```\n  2014:     /// use std::collections::VecDeque;\n  2015:     ///\n  2016:     /// let mut d = VecDeque::new();\n  2017:     /// assert_eq!(d.back(), None);\n  2018:     ///\n  2019:     /// d.push_back(1);\n  2020:     /// d.push_back(2);",
    "nanvix_source": "  2058:     ///\n  2059:     /// d.push_back(1);\n  2060:     /// d.push_back(2);\n  2061:     /// match d.front_mut() {\n  2062:     ///     Some(x) => *x = 9,\n  2063:     ///     None => (),\n  2064:     /// }\n  2065:     /// assert_eq!(d.front(), Some(&9));\n  2066:     /// ```\n  2067:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2068:     pub fn front_mut(&mut self) -> Option<&mut T> {\n  2069:         self.get_mut(0)\n  2070:     }\n  2071: \n  2072:     /// Provides a reference to the back element, or `None` if the deque is\n  2073:     /// empty.\n  2074:     ///\n  2075:     /// # Examples\n  2076:     ///\n  2077:     /// ```\n  2078:     /// use std::collections::VecDeque;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::get_mut",
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
            "index",
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
                      "borrowed_ref": {
                        "is_mutable": true,
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
    "verification_source": "   927:     ///\n   928:     /// ```\n   929:     /// use std::collections::VecDeque;\n   930:     ///\n   931:     /// let mut buf = VecDeque::new();\n   932:     /// buf.push_back(3);\n   933:     /// buf.push_back(4);\n   934:     /// buf.push_back(5);\n   935:     /// buf.push_back(6);\n   936:     /// assert_eq!(buf[1], 4);\n   937:     /// if let Some(elem) = buf.get_mut(1) {\n   938:     ///     *elem = 7;\n   939:     /// }\n   940:     /// assert_eq!(buf[1], 7);\n   941:     /// ```\n   942:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   943:     pub fn get_mut(&mut self, index: usize) -> Option<&mut T> {\n   944:         if index < self.len {\n   945:             let idx = self.to_physical_idx(index);\n   946:             unsafe { Some(&mut *self.ptr().add(idx)) }\n   947:         } else {\n   948:             None\n   949:         }\n   950:     }\n   951: \n   952:     /// Swaps elements at indices `i` and `j`.\n   953:     ///\n   954:     /// `i` and `j` may be equal.\n   955:     ///\n   956:     /// Element at index 0 is the front of the queue.\n   957:     ///\n   958:     /// # Panics\n   959:     ///",
    "nanvix_source": "   986:     /// buf.push_back(4);\n   987:     /// buf.push_back(5);\n   988:     /// buf.push_back(6);\n   989:     /// assert_eq!(buf[1], 4);\n   990:     /// if let Some(elem) = buf.get_mut(1) {\n   991:     ///     *elem = 7;\n   992:     /// }\n   993:     /// assert_eq!(buf[1], 7);\n   994:     /// ```\n   995:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   996:     pub fn get_mut(&mut self, index: usize) -> Option<&mut T> {\n   997:         if index < self.len {\n   998:             let idx = self.to_wrapped_index(index);\n   999:             unsafe { Some(&mut *self.ptr().add(idx.as_index())) }\n  1000:         } else {\n  1001:             None\n  1002:         }\n  1003:     }\n  1004: \n  1005:     /// Swaps elements at indices `i` and `j`.\n  1006:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::insert_mut",
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
      "name": "insert_mut",
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
            "index",
            {
              "primitive": "usize"
            }
          ],
          [
            "value",
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
    "verification_source": "  2420:     ///\n  2421:     /// Panics if `index` is strictly greater than the deque's length.\n  2422:     ///\n  2423:     /// # Examples\n  2424:     ///\n  2425:     /// ```\n  2426:     /// use std::collections::VecDeque;\n  2427:     ///\n  2428:     /// let mut vec_deque = VecDeque::from([1, 2, 3]);\n  2429:     ///\n  2430:     /// let x = vec_deque.insert_mut(1, 5);\n  2431:     /// *x += 7;\n  2432:     /// assert_eq!(vec_deque, &[1, 12, 2, 3]);\n  2433:     /// ```\n  2434:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2435:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::insert` instead\"]\n  2436:     pub fn insert_mut(&mut self, index: usize, value: T) -> &mut T {\n  2437:         assert!(index <= self.len(), \"index out of bounds\");\n  2438: \n  2439:         if self.is_full() {\n  2440:             self.grow();\n  2441:         }\n  2442: \n  2443:         let k = self.len - index;\n  2444:         if k < index {\n  2445:             // `index + 1` can't overflow, because if index was usize::MAX, then either the\n  2446:             // assert would've failed, or the deque would've tried to grow past usize::MAX\n  2447:             // and panicked.\n  2448:             unsafe {\n  2449:                 // see `remove()` for explanation why this wrap_copy() call is safe.\n  2450:                 self.wrap_copy(self.to_physical_idx(index), self.to_physical_idx(index + 1), k);\n  2451:                 self.len += 1;\n  2452:                 self.buffer_write(self.to_physical_idx(index), value)",
    "nanvix_source": "  2490:     /// use std::collections::VecDeque;\n  2491:     ///\n  2492:     /// let mut vec_deque = VecDeque::from([1, 2, 3]);\n  2493:     ///\n  2494:     /// let x = vec_deque.insert_mut(1, 5);\n  2495:     /// *x += 7;\n  2496:     /// assert_eq!(vec_deque, &[1, 12, 2, 3]);\n  2497:     /// ```\n  2498:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2499:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::insert` instead\"]\n  2500:     pub fn insert_mut(&mut self, index: usize, value: T) -> &mut T {\n  2501:         assert!(index <= self.len(), \"index out of bounds\");\n  2502: \n  2503:         if self.is_full() {\n  2504:             self.grow();\n  2505:         }\n  2506: \n  2507:         let k = self.len - index;\n  2508:         if k < index {\n  2509:             // `index + 1` can't overflow, because if index was usize::MAX, then either the\n  2510:             // assert would've failed, or the deque would've tried to grow past usize::MAX",
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
