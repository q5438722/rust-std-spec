For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::range",
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
      "name": "range",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 2977,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  1709:     ///\n  1710:     /// # Examples\n  1711:     ///\n  1712:     /// ```\n  1713:     /// use std::collections::VecDeque;\n  1714:     ///\n  1715:     /// let deque: VecDeque<_> = [1, 2, 3].into();\n  1716:     /// let range = deque.range(2..).copied().collect::<VecDeque<_>>();\n  1717:     /// assert_eq!(range, [3]);\n  1718:     ///\n  1719:     /// // A full range covers all contents\n  1720:     /// let all = deque.range(..);\n  1721:     /// assert_eq!(all.len(), 3);\n  1722:     /// ```\n  1723:     #[inline]\n  1724:     #[stable(feature = \"deque_range\", since = \"1.51.0\")]\n  1725:     pub fn range<R>(&self, range: R) -> Iter<'_, T>\n  1726:     where\n  1727:         R: RangeBounds<usize>,\n  1728:     {\n  1729:         let (a_range, b_range) = self.slice_ranges(range, self.len);\n  1730:         // SAFETY: The ranges returned by `slice_ranges`\n  1731:         // are valid ranges into the physical buffer, so\n  1732:         // it's ok to pass them to `buffer_range` and\n  1733:         // dereference the result.\n  1734:         let a = unsafe { &*self.buffer_range(a_range) };\n  1735:         let b = unsafe { &*self.buffer_range(b_range) };\n  1736:         Iter::new(a.iter(), b.iter())\n  1737:     }\n  1738: \n  1739:     /// Creates an iterator that covers the specified mutable range in the deque.\n  1740:     ///\n  1741:     /// # Panics",
    "nanvix_source": "  1779:     /// let deque: VecDeque<_> = [1, 2, 3].into();\n  1780:     /// let range = deque.range(2..).copied().collect::<VecDeque<_>>();\n  1781:     /// assert_eq!(range, [3]);\n  1782:     ///\n  1783:     /// // A full range covers all contents\n  1784:     /// let all = deque.range(..);\n  1785:     /// assert_eq!(all.len(), 3);\n  1786:     /// ```\n  1787:     #[inline]\n  1788:     #[stable(feature = \"deque_range\", since = \"1.51.0\")]\n  1789:     pub fn range<R>(&self, range: R) -> Iter<'_, T>\n  1790:     where\n  1791:         R: RangeBounds<usize>,\n  1792:     {\n  1793:         let (a_range, b_range) = self.slice_ranges(range, self.len);\n  1794:         // SAFETY: The ranges returned by `slice_ranges`\n  1795:         // are valid ranges into the physical buffer, so\n  1796:         // it's ok to pass them to `buffer_range` and\n  1797:         // dereference the result.\n  1798:         let a = unsafe { &*self.buffer_range(a_range) };\n  1799:         let b = unsafe { &*self.buffer_range(b_range) };",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::range_mut",
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
      "name": "range_mut",
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
    "verification_source": "  1749:     /// use std::collections::VecDeque;\n  1750:     ///\n  1751:     /// let mut deque: VecDeque<_> = [1, 2, 3].into();\n  1752:     /// for v in deque.range_mut(2..) {\n  1753:     ///   *v *= 2;\n  1754:     /// }\n  1755:     /// assert_eq!(deque, [1, 2, 6]);\n  1756:     ///\n  1757:     /// // A full range covers all contents\n  1758:     /// for v in deque.range_mut(..) {\n  1759:     ///   *v *= 2;\n  1760:     /// }\n  1761:     /// assert_eq!(deque, [2, 4, 12]);\n  1762:     /// ```\n  1763:     #[inline]\n  1764:     #[stable(feature = \"deque_range\", since = \"1.51.0\")]\n  1765:     pub fn range_mut<R>(&mut self, range: R) -> IterMut<'_, T>\n  1766:     where\n  1767:         R: RangeBounds<usize>,\n  1768:     {\n  1769:         let (a_range, b_range) = self.slice_ranges(range, self.len);\n  1770:         // SAFETY: The ranges returned by `slice_ranges`\n  1771:         // are valid ranges into the physical buffer, so\n  1772:         // it's ok to pass them to `buffer_range` and\n  1773:         // dereference the result.\n  1774:         let a = unsafe { &mut *self.buffer_range(a_range) };\n  1775:         let b = unsafe { &mut *self.buffer_range(b_range) };\n  1776:         IterMut::new(a.iter_mut(), b.iter_mut())\n  1777:     }\n  1778: \n  1779:     /// Removes the specified range from the deque in bulk, returning all\n  1780:     /// removed elements as an iterator. If the iterator is dropped before\n  1781:     /// being fully consumed, it drops the remaining removed elements.",
    "nanvix_source": "  1819:     /// assert_eq!(deque, [1, 2, 6]);\n  1820:     ///\n  1821:     /// // A full range covers all contents\n  1822:     /// for v in deque.range_mut(..) {\n  1823:     ///   *v *= 2;\n  1824:     /// }\n  1825:     /// assert_eq!(deque, [2, 4, 12]);\n  1826:     /// ```\n  1827:     #[inline]\n  1828:     #[stable(feature = \"deque_range\", since = \"1.51.0\")]\n  1829:     pub fn range_mut<R>(&mut self, range: R) -> IterMut<'_, T>\n  1830:     where\n  1831:         R: RangeBounds<usize>,\n  1832:     {\n  1833:         let (a_range, b_range) = self.slice_ranges(range, self.len);\n  1834:         // SAFETY: The ranges returned by `slice_ranges`\n  1835:         // are valid ranges into the physical buffer, so\n  1836:         // it's ok to pass them to `buffer_range` and\n  1837:         // dereference the result.\n  1838:         let a = unsafe { &mut *self.buffer_range(a_range) };\n  1839:         let b = unsafe { &mut *self.buffer_range(b_range) };",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::retain",
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
    "verification_source": "  2645:     ///\n  2646:     /// Because the elements are visited exactly once in the original order,\n  2647:     /// external state may be used to decide which elements to keep.\n  2648:     ///\n  2649:     /// ```\n  2650:     /// use std::collections::VecDeque;\n  2651:     ///\n  2652:     /// let mut buf = VecDeque::new();\n  2653:     /// buf.extend(1..6);\n  2654:     ///\n  2655:     /// let keep = [false, true, true, false, true];\n  2656:     /// let mut iter = keep.iter();\n  2657:     /// buf.retain(|_| *iter.next().unwrap());\n  2658:     /// assert_eq!(buf, [2, 3, 5]);\n  2659:     /// ```\n  2660:     #[stable(feature = \"vec_deque_retain\", since = \"1.4.0\")]\n  2661:     pub fn retain<F>(&mut self, mut f: F)\n  2662:     where\n  2663:         F: FnMut(&T) -> bool,\n  2664:     {\n  2665:         self.retain_mut(|elem| f(elem));\n  2666:     }\n  2667: \n  2668:     /// Retains only the elements specified by the predicate.\n  2669:     ///\n  2670:     /// In other words, remove all elements `e` for which `f(&mut e)` returns false.\n  2671:     /// This method operates in place, visiting each element exactly once in the\n  2672:     /// original order, and preserves the order of the retained elements.\n  2673:     ///\n  2674:     /// # Examples\n  2675:     ///\n  2676:     /// ```\n  2677:     /// use std::collections::VecDeque;",
    "nanvix_source": "  2715:     ///\n  2716:     /// let mut buf = VecDeque::new();\n  2717:     /// buf.extend(1..6);\n  2718:     ///\n  2719:     /// let keep = [false, true, true, false, true];\n  2720:     /// let mut iter = keep.iter();\n  2721:     /// buf.retain(|_| *iter.next().unwrap());\n  2722:     /// assert_eq!(buf, [2, 3, 5]);\n  2723:     /// ```\n  2724:     #[stable(feature = \"vec_deque_retain\", since = \"1.4.0\")]\n  2725:     pub fn retain<F>(&mut self, mut f: F)\n  2726:     where\n  2727:         F: FnMut(&T) -> bool,\n  2728:     {\n  2729:         self.retain_mut(|elem| f(elem));\n  2730:     }\n  2731: \n  2732:     /// Retains only the elements specified by the predicate.\n  2733:     ///\n  2734:     /// In other words, remove all elements `e` for which `f(&mut e)` returns false.\n  2735:     /// This method operates in place, visiting each element exactly once in the",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::retain_mut",
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
      "name": "retain_mut",
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
    "verification_source": "  2674:     /// # Examples\n  2675:     ///\n  2676:     /// ```\n  2677:     /// use std::collections::VecDeque;\n  2678:     ///\n  2679:     /// let mut buf = VecDeque::new();\n  2680:     /// buf.extend(1..5);\n  2681:     /// buf.retain_mut(|x| if *x % 2 == 0 {\n  2682:     ///     *x += 1;\n  2683:     ///     true\n  2684:     /// } else {\n  2685:     ///     false\n  2686:     /// });\n  2687:     /// assert_eq!(buf, [3, 5]);\n  2688:     /// ```\n  2689:     #[stable(feature = \"vec_retain_mut\", since = \"1.61.0\")]\n  2690:     pub fn retain_mut<F>(&mut self, mut f: F)\n  2691:     where\n  2692:         F: FnMut(&mut T) -> bool,\n  2693:     {\n  2694:         let len = self.len;\n  2695:         let mut idx = 0;\n  2696:         let mut cur = 0;\n  2697: \n  2698:         // Stage 1: All values are retained.\n  2699:         while cur < len {\n  2700:             if !f(&mut self[cur]) {\n  2701:                 cur += 1;\n  2702:                 break;\n  2703:             }\n  2704:             cur += 1;\n  2705:             idx += 1;\n  2706:         }",
    "nanvix_source": "  2744:     /// buf.extend(1..5);\n  2745:     /// buf.retain_mut(|x| if *x % 2 == 0 {\n  2746:     ///     *x += 1;\n  2747:     ///     true\n  2748:     /// } else {\n  2749:     ///     false\n  2750:     /// });\n  2751:     /// assert_eq!(buf, [3, 5]);\n  2752:     /// ```\n  2753:     #[stable(feature = \"vec_retain_mut\", since = \"1.61.0\")]\n  2754:     pub fn retain_mut<F>(&mut self, mut f: F)\n  2755:     where\n  2756:         F: FnMut(&mut T) -> bool,\n  2757:     {\n  2758:         let len = self.len;\n  2759:         let mut idx = 0;\n  2760:         let mut cur = 0;\n  2761: \n  2762:         // Stage 1: All values are retained.\n  2763:         while cur < len {\n  2764:             if !f(&mut self[cur]) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::drain",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 4066,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "  1959:     ///\n  1960:     /// ```\n  1961:     /// let mut s = String::from(\"\u03b1 is alpha, \u03b2 is beta\");\n  1962:     /// let beta_offset = s.find('\u03b2').unwrap_or(s.len());\n  1963:     ///\n  1964:     /// // Remove the range up until the \u03b2 from the string\n  1965:     /// let t: String = s.drain(..beta_offset).collect();\n  1966:     /// assert_eq!(t, \"\u03b1 is alpha, \");\n  1967:     /// assert_eq!(s, \"\u03b2 is beta\");\n  1968:     ///\n  1969:     /// // A full range clears the string, like `clear()` does\n  1970:     /// s.drain(..);\n  1971:     /// assert_eq!(s, \"\");\n  1972:     /// ```\n  1973:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1974:     #[track_caller]\n  1975:     pub fn drain<R>(&mut self, range: R) -> Drain<'_>\n  1976:     where\n  1977:         R: RangeBounds<usize>,\n  1978:     {\n  1979:         // Memory safety\n  1980:         //\n  1981:         // The String version of Drain does not have the memory safety issues\n  1982:         // of the vector version. The data is just plain bytes.\n  1983:         // Because the range removal happens in Drop, if the Drain iterator is leaked,\n  1984:         // the removal will not happen.\n  1985:         let Range { start, end } = slice::range(range, ..self.len());\n  1986:         assert!(self.is_char_boundary(start));\n  1987:         assert!(self.is_char_boundary(end));\n  1988: \n  1989:         // Take out two simultaneous borrows. The &mut String won't be accessed\n  1990:         // until iteration is over, in Drop.\n  1991:         let self_ptr = self as *mut _;",
    "nanvix_source": "  1970:     /// let t: String = s.drain(..beta_offset).collect();\n  1971:     /// assert_eq!(t, \"\u03b1 is alpha, \");\n  1972:     /// assert_eq!(s, \"\u03b2 is beta\");\n  1973:     ///\n  1974:     /// // A full range clears the string, like `clear()` does\n  1975:     /// s.drain(..);\n  1976:     /// assert_eq!(s, \"\");\n  1977:     /// ```\n  1978:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1979:     #[track_caller]\n  1980:     pub fn drain<R>(&mut self, range: R) -> Drain<'_>\n  1981:     where\n  1982:         R: RangeBounds<usize>,\n  1983:     {\n  1984:         // Memory safety\n  1985:         //\n  1986:         // The String version of Drain does not have the memory safety issues\n  1987:         // of the vector version. The data is just plain bytes.\n  1988:         // Because the range removal happens in Drop, if the Drain iterator is leaked,\n  1989:         // the removal will not happen.\n  1990:         let Range { start, end } = slice::range(range, ..self.len());",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::retain",
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
                              "primitive": "char"
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
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
    "verification_source": "  1628:     ///\n  1629:     /// assert_eq!(s, \"foobar\");\n  1630:     /// ```\n  1631:     ///\n  1632:     /// Because the elements are visited exactly once in the original order,\n  1633:     /// external state may be used to decide which elements to keep.\n  1634:     ///\n  1635:     /// ```\n  1636:     /// let mut s = String::from(\"abcde\");\n  1637:     /// let keep = [false, true, true, false, true];\n  1638:     /// let mut iter = keep.iter();\n  1639:     /// s.retain(|_| *iter.next().unwrap());\n  1640:     /// assert_eq!(s, \"bce\");\n  1641:     /// ```\n  1642:     #[inline]\n  1643:     #[stable(feature = \"string_retain\", since = \"1.26.0\")]\n  1644:     pub fn retain<F>(&mut self, mut f: F)\n  1645:     where\n  1646:         F: FnMut(char) -> bool,\n  1647:     {\n  1648:         struct SetLenOnDrop<'a> {\n  1649:             s: &'a mut String,\n  1650:             idx: usize,\n  1651:             del_bytes: usize,\n  1652:         }\n  1653: \n  1654:         impl<'a> Drop for SetLenOnDrop<'a> {\n  1655:             fn drop(&mut self) {\n  1656:                 let new_len = self.idx - self.del_bytes;\n  1657:                 debug_assert!(new_len <= self.s.len());\n  1658:                 unsafe { self.s.vec.set_len(new_len) };\n  1659:             }\n  1660:         }",
    "nanvix_source": "  1639:     ///\n  1640:     /// ```\n  1641:     /// let mut s = String::from(\"abcde\");\n  1642:     /// let keep = [false, true, true, false, true];\n  1643:     /// let mut iter = keep.iter();\n  1644:     /// s.retain(|_| *iter.next().unwrap());\n  1645:     /// assert_eq!(s, \"bce\");\n  1646:     /// ```\n  1647:     #[inline]\n  1648:     #[stable(feature = \"string_retain\", since = \"1.26.0\")]\n  1649:     pub fn retain<F>(&mut self, mut f: F)\n  1650:     where\n  1651:         F: FnMut(char) -> bool,\n  1652:     {\n  1653:         struct SetLenOnDrop<'a> {\n  1654:             s: &'a mut String,\n  1655:             idx: usize,\n  1656:             del_bytes: usize,\n  1657:         }\n  1658: \n  1659:         impl<'a> Drop for SetLenOnDrop<'a> {",
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
