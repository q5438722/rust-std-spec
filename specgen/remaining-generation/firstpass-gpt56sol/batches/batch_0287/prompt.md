For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::fold",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "B"
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
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "B"
                            },
                            {
                              "qualified_path": {
                                "args": null,
                                "name": "Item",
                                "self_type": {
                                  "generic": "Self"
                                },
                                "trait": {
                                  "args": null,
                                  "id": 82,
                                  "path": ""
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "B"
                          }
                        }
                      },
                      "id": 22,
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
      "name": "fold",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
            "init",
            {
              "generic": "B"
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
        "output": {
          "generic": "B"
        }
      }
    },
    "verification_source": "  2650:     /// // for loop:\n  2651:     /// for i in &numbers {\n  2652:     ///     result = result + i;\n  2653:     /// }\n  2654:     ///\n  2655:     /// // fold:\n  2656:     /// let result2 = numbers.iter().fold(0, |acc, &x| acc + x);\n  2657:     ///\n  2658:     /// // they're the same\n  2659:     /// assert_eq!(result, result2);\n  2660:     /// ```\n  2661:     ///\n  2662:     /// [`reduce()`]: Iterator::reduce\n  2663:     #[doc(alias = \"inject\", alias = \"foldl\")]\n  2664:     #[inline]\n  2665:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2666:     fn fold<B, F>(mut self, init: B, mut f: F) -> B\n  2667:     where\n  2668:         Self: Sized + [const] Destruct,\n  2669:         F: [const] FnMut(B, Self::Item) -> B + [const] Destruct,\n  2670:     {\n  2671:         let mut accum = init;\n  2672:         while let Some(x) = self.next() {\n  2673:             accum = f(accum, x);\n  2674:         }\n  2675:         accum\n  2676:     }\n  2677: \n  2678:     /// Reduces the elements to a single one, by repeatedly applying a reducing\n  2679:     /// operation.\n  2680:     ///\n  2681:     /// If the iterator is empty, returns [`None`]; otherwise, returns the\n  2682:     /// result of the reduction.",
    "nanvix_source": "  2654:     /// let result2 = numbers.iter().fold(0, |acc, &x| acc + x);\n  2655:     ///\n  2656:     /// // they're the same\n  2657:     /// assert_eq!(result, result2);\n  2658:     /// ```\n  2659:     ///\n  2660:     /// [`reduce()`]: Iterator::reduce\n  2661:     #[doc(alias = \"inject\", alias = \"foldl\")]\n  2662:     #[inline]\n  2663:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2664:     fn fold<B, F>(mut self, init: B, mut f: F) -> B\n  2665:     where\n  2666:         Self: Sized + [const] Destruct,\n  2667:         F: [const] FnMut(B, Self::Item) -> B + [const] Destruct,\n  2668:     {\n  2669:         let mut accum = init;\n  2670:         while let Some(x) = self.next() {\n  2671:             accum = f(accum, x);\n  2672:         }\n  2673:         accum\n  2674:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::for_each",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
                              "qualified_path": {
                                "args": null,
                                "name": "Item",
                                "self_type": {
                                  "generic": "Self"
                                },
                                "trait": {
                                  "args": null,
                                  "id": 82,
                                  "path": ""
                                }
                              }
                            }
                          ],
                          "output": null
                        }
                      },
                      "id": 22,
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
      "name": "for_each",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
    "verification_source": "   863:     /// let v: Vec<_> = rx.iter().collect();\n   864:     /// assert_eq!(v, vec![1, 3, 5, 7, 9]);\n   865:     /// ```\n   866:     ///\n   867:     /// For such a small example, a `for` loop may be cleaner, but `for_each`\n   868:     /// might be preferable to keep a functional style with longer iterators:\n   869:     ///\n   870:     /// ```\n   871:     /// (0..5).flat_map(|x| (x * 100)..(x * 110))\n   872:     ///       .enumerate()\n   873:     ///       .filter(|&(i, x)| (i + x) % 3 == 0)\n   874:     ///       .for_each(|(i, x)| println!(\"{i}:{x}\"));\n   875:     /// ```\n   876:     #[inline]\n   877:     #[stable(feature = \"iterator_for_each\", since = \"1.21.0\")]\n   878:     #[rustc_non_const_trait_method]\n   879:     fn for_each<F>(self, f: F)\n   880:     where\n   881:         Self: Sized,\n   882:         F: FnMut(Self::Item),\n   883:     {\n   884:         #[inline]\n   885:         fn call<T>(mut f: impl FnMut(T)) -> impl FnMut((), T) {\n   886:             move |(), item| f(item)\n   887:         }\n   888: \n   889:         self.fold((), call(f));\n   890:     }\n   891: \n   892:     /// Creates an iterator which uses a closure to determine if an element\n   893:     /// should be yielded.\n   894:     ///\n   895:     /// Given an element the closure must return `true` or `false`. The returned",
    "nanvix_source": "   867:     ///\n   868:     /// ```\n   869:     /// (0..5).flat_map(|x| (x * 100)..(x * 110))\n   870:     ///       .enumerate()\n   871:     ///       .filter(|&(i, x)| (i + x) % 3 == 0)\n   872:     ///       .for_each(|(i, x)| println!(\"{i}:{x}\"));\n   873:     /// ```\n   874:     #[inline]\n   875:     #[stable(feature = \"iterator_for_each\", since = \"1.21.0\")]\n   876:     #[rustc_non_const_trait_method]\n   877:     fn for_each<F>(self, f: F)\n   878:     where\n   879:         Self: Sized,\n   880:         F: FnMut(Self::Item),\n   881:     {\n   882:         #[inline]\n   883:         fn call<T>(mut f: impl FnMut(T)) -> impl FnMut((), T) {\n   884:             move |(), item| f(item)\n   885:         }\n   886: \n   887:         self.fold((), call(f));",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::fuse",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                "generic": "Self"
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
      "name": "fuse",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9868,
            "path": "Fuse"
          }
        }
      }
    },
    "verification_source": "  1819:     /// assert_eq!(iter.next(), Some(2));\n  1820:     /// assert_eq!(iter.next(), None);\n  1821:     ///\n  1822:     /// // however, once we fuse it...\n  1823:     /// let mut iter = iter.fuse();\n  1824:     ///\n  1825:     /// assert_eq!(iter.next(), Some(4));\n  1826:     /// assert_eq!(iter.next(), None);\n  1827:     ///\n  1828:     /// // it will always return `None` after the first time.\n  1829:     /// assert_eq!(iter.next(), None);\n  1830:     /// assert_eq!(iter.next(), None);\n  1831:     /// assert_eq!(iter.next(), None);\n  1832:     /// ```\n  1833:     #[inline]\n  1834:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1835:     fn fuse(self) -> Fuse<Self>\n  1836:     where\n  1837:         Self: Sized,\n  1838:     {\n  1839:         Fuse::new(self)\n  1840:     }\n  1841: \n  1842:     /// Does something with each element of an iterator, passing the value on.\n  1843:     ///\n  1844:     /// When using iterators, you'll often chain several of them together.\n  1845:     /// While working on such code, you might want to check out what's\n  1846:     /// happening at various parts in the pipeline. To do that, insert\n  1847:     /// a call to `inspect()`.\n  1848:     ///\n  1849:     /// It's more common for `inspect()` to be used as a debugging tool than to\n  1850:     /// exist in your final code, but applications may find it useful in certain\n  1851:     /// situations when errors need to be logged before being discarded.",
    "nanvix_source": "  1823:     /// assert_eq!(iter.next(), Some(4));\n  1824:     /// assert_eq!(iter.next(), None);\n  1825:     ///\n  1826:     /// // it will always return `None` after the first time.\n  1827:     /// assert_eq!(iter.next(), None);\n  1828:     /// assert_eq!(iter.next(), None);\n  1829:     /// assert_eq!(iter.next(), None);\n  1830:     /// ```\n  1831:     #[inline]\n  1832:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1833:     fn fuse(self) -> Fuse<Self>\n  1834:     where\n  1835:         Self: Sized,\n  1836:     {\n  1837:         Fuse::new(self)\n  1838:     }\n  1839: \n  1840:     /// Does something with each element of an iterator, passing the value on.\n  1841:     ///\n  1842:     /// When using iterators, you'll often chain several of them together.\n  1843:     /// While working on such code, you might want to check out what's",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::ge",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "I"
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
                      "args": null,
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
                                  },
                                  "trait": {
                                    "args": null,
                                    "id": 80,
                                    "path": ""
                                  }
                                }
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
                    "path": ""
                  }
                }
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "ge",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
            "other",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4007:         self.partial_cmp(other) == Some(Ordering::Greater)\n  4008:     }\n  4009: \n  4010:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  4011:     /// greater than or equal to those of another.\n  4012:     ///\n  4013:     /// # Examples\n  4014:     ///\n  4015:     /// ```\n  4016:     /// assert_eq!([1].iter().ge([1].iter()), true);\n  4017:     /// assert_eq!([1].iter().ge([1, 2].iter()), false);\n  4018:     /// assert_eq!([1, 2].iter().ge([1].iter()), true);\n  4019:     /// assert_eq!([1, 2].iter().ge([1, 2].iter()), true);\n  4020:     /// ```\n  4021:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  4022:     #[rustc_non_const_trait_method]\n  4023:     fn ge<I>(self, other: I) -> bool\n  4024:     where\n  4025:         I: IntoIterator,\n  4026:         Self::Item: PartialOrd<I::Item>,\n  4027:         Self: Sized,\n  4028:     {\n  4029:         matches!(self.partial_cmp(other), Some(Ordering::Greater | Ordering::Equal))\n  4030:     }\n  4031: \n  4032:     /// Checks if the elements of this iterator are sorted.\n  4033:     ///\n  4034:     /// That is, for each element `a` and its following element `b`, `a <= b` must hold. If the\n  4035:     /// iterator yields exactly zero or one element, `true` is returned.\n  4036:     ///\n  4037:     /// Note that if `Self::Item` is only `PartialOrd`, but not `Ord`, the above definition\n  4038:     /// implies that this function returns `false` if any two consecutive items are not\n  4039:     /// comparable.",
    "nanvix_source": "  4011:     /// # Examples\n  4012:     ///\n  4013:     /// ```\n  4014:     /// assert_eq!([1].iter().ge([1].iter()), true);\n  4015:     /// assert_eq!([1].iter().ge([1, 2].iter()), false);\n  4016:     /// assert_eq!([1, 2].iter().ge([1].iter()), true);\n  4017:     /// assert_eq!([1, 2].iter().ge([1, 2].iter()), true);\n  4018:     /// ```\n  4019:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  4020:     #[rustc_non_const_trait_method]\n  4021:     fn ge<I>(self, other: I) -> bool\n  4022:     where\n  4023:         I: IntoIterator,\n  4024:         Self::Item: PartialOrd<I::Item>,\n  4025:         Self: Sized,\n  4026:     {\n  4027:         matches!(self.partial_cmp(other), Some(Ordering::Greater | Ordering::Equal))\n  4028:     }\n  4029: \n  4030:     /// Checks if the elements of this iterator are sorted.\n  4031:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::gt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "I"
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
                      "args": null,
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
                                  },
                                  "trait": {
                                    "args": null,
                                    "id": 80,
                                    "path": ""
                                  }
                                }
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
                    "path": ""
                  }
                }
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "gt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
            "other",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  3985:         matches!(self.partial_cmp(other), Some(Ordering::Less | Ordering::Equal))\n  3986:     }\n  3987: \n  3988:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3989:     /// greater than those of another.\n  3990:     ///\n  3991:     /// # Examples\n  3992:     ///\n  3993:     /// ```\n  3994:     /// assert_eq!([1].iter().gt([1].iter()), false);\n  3995:     /// assert_eq!([1].iter().gt([1, 2].iter()), false);\n  3996:     /// assert_eq!([1, 2].iter().gt([1].iter()), true);\n  3997:     /// assert_eq!([1, 2].iter().gt([1, 2].iter()), false);\n  3998:     /// ```\n  3999:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  4000:     #[rustc_non_const_trait_method]\n  4001:     fn gt<I>(self, other: I) -> bool\n  4002:     where\n  4003:         I: IntoIterator,\n  4004:         Self::Item: PartialOrd<I::Item>,\n  4005:         Self: Sized,\n  4006:     {\n  4007:         self.partial_cmp(other) == Some(Ordering::Greater)\n  4008:     }\n  4009: \n  4010:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  4011:     /// greater than or equal to those of another.\n  4012:     ///\n  4013:     /// # Examples\n  4014:     ///\n  4015:     /// ```\n  4016:     /// assert_eq!([1].iter().ge([1].iter()), true);\n  4017:     /// assert_eq!([1].iter().ge([1, 2].iter()), false);",
    "nanvix_source": "  3989:     /// # Examples\n  3990:     ///\n  3991:     /// ```\n  3992:     /// assert_eq!([1].iter().gt([1].iter()), false);\n  3993:     /// assert_eq!([1].iter().gt([1, 2].iter()), false);\n  3994:     /// assert_eq!([1, 2].iter().gt([1].iter()), true);\n  3995:     /// assert_eq!([1, 2].iter().gt([1, 2].iter()), false);\n  3996:     /// ```\n  3997:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3998:     #[rustc_non_const_trait_method]\n  3999:     fn gt<I>(self, other: I) -> bool\n  4000:     where\n  4001:         I: IntoIterator,\n  4002:         Self::Item: PartialOrd<I::Item>,\n  4003:         Self: Sized,\n  4004:     {\n  4005:         self.partial_cmp(other) == Some(Ordering::Greater)\n  4006:     }\n  4007: \n  4008:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  4009:     /// greater than or equal to those of another.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::inspect",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
                                  "qualified_path": {
                                    "args": null,
                                    "name": "Item",
                                    "self_type": {
                                      "generic": "Self"
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
                          ],
                          "output": null
                        }
                      },
                      "id": 22,
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
      "name": "inspect",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
            "f",
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
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9871,
            "path": "Inspect"
          }
        }
      }
    },
    "verification_source": "  1903:     ///         }\n  1904:     ///     })\n  1905:     ///     .filter_map(Result::ok)\n  1906:     ///     .sum();\n  1907:     ///\n  1908:     /// println!(\"Sum: {sum}\");\n  1909:     /// ```\n  1910:     ///\n  1911:     /// This will print:\n  1912:     ///\n  1913:     /// ```text\n  1914:     /// Parsing error: invalid digit found in string\n  1915:     /// Sum: 3\n  1916:     /// ```\n  1917:     #[inline]\n  1918:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1919:     fn inspect<F>(self, f: F) -> Inspect<Self, F>\n  1920:     where\n  1921:         Self: Sized,\n  1922:         F: FnMut(&Self::Item),\n  1923:     {\n  1924:         Inspect::new(self, f)\n  1925:     }\n  1926: \n  1927:     /// Creates a \"by reference\" adapter for this instance of `Iterator`.\n  1928:     ///\n  1929:     /// Consuming method calls (direct or indirect calls to `next`)\n  1930:     /// on the \"by reference\" adapter will consume the original iterator,\n  1931:     /// but ownership-taking methods (those with a `self` parameter)\n  1932:     /// only take ownership of the \"by reference\" iterator.\n  1933:     ///\n  1934:     /// This is useful for applying ownership-taking methods\n  1935:     /// (such as `take` in the example below)",
    "nanvix_source": "  1907:     /// ```\n  1908:     ///\n  1909:     /// This will print:\n  1910:     ///\n  1911:     /// ```text\n  1912:     /// Parsing error: invalid digit found in string\n  1913:     /// Sum: 3\n  1914:     /// ```\n  1915:     #[inline]\n  1916:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1917:     fn inspect<F>(self, f: F) -> Inspect<Self, F>\n  1918:     where\n  1919:         Self: Sized,\n  1920:         F: FnMut(&Self::Item),\n  1921:     {\n  1922:         Inspect::new(self, f)\n  1923:     }\n  1924: \n  1925:     /// Creates a \"by reference\" adapter for this instance of `Iterator`.\n  1926:     ///\n  1927:     /// Consuming method calls (direct or indirect calls to `next`)",
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
