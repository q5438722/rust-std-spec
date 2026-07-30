For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::peekable",
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
      "name": "peekable",
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
            "id": 9889,
            "path": "Peekable"
          }
        }
      }
    },
    "verification_source": "  1101:     /// assert_eq!(iter.next(), Some(1));\n  1102:     ///\n  1103:     /// if let Some(p) = iter.peek_mut() {\n  1104:     ///     assert_eq!(*p, 2);\n  1105:     ///     // put a value into the iterator\n  1106:     ///     *p = 1000;\n  1107:     /// }\n  1108:     ///\n  1109:     /// // The value reappears as the iterator continues\n  1110:     /// assert_eq!(iter.collect::<Vec<_>>(), vec![1000, 3]);\n  1111:     /// ```\n  1112:     /// [`peek`]: Peekable::peek\n  1113:     /// [`peek_mut`]: Peekable::peek_mut\n  1114:     /// [`next`]: Iterator::next\n  1115:     #[inline]\n  1116:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1117:     fn peekable(self) -> Peekable<Self>\n  1118:     where\n  1119:         Self: Sized,\n  1120:     {\n  1121:         Peekable::new(self)\n  1122:     }\n  1123: \n  1124:     /// Creates an iterator that [`skip`]s elements based on a predicate.\n  1125:     ///\n  1126:     /// [`skip`]: Iterator::skip\n  1127:     ///\n  1128:     /// `skip_while()` takes a closure as an argument. It will call this\n  1129:     /// closure on each element of the iterator, and ignore elements\n  1130:     /// until it returns `false`.\n  1131:     ///\n  1132:     /// After `false` is returned, `skip_while()`'s job is over, and the\n  1133:     /// rest of the elements are yielded.",
    "nanvix_source": "  1105:     /// }\n  1106:     ///\n  1107:     /// // The value reappears as the iterator continues\n  1108:     /// assert_eq!(iter.collect::<Vec<_>>(), vec![1000, 3]);\n  1109:     /// ```\n  1110:     /// [`peek`]: Peekable::peek\n  1111:     /// [`peek_mut`]: Peekable::peek_mut\n  1112:     /// [`next`]: Iterator::next\n  1113:     #[inline]\n  1114:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1115:     fn peekable(self) -> Peekable<Self>\n  1116:     where\n  1117:         Self: Sized,\n  1118:     {\n  1119:         Peekable::new(self)\n  1120:     }\n  1121: \n  1122:     /// Creates an iterator that [`skip`]s elements based on a predicate.\n  1123:     ///\n  1124:     /// [`skip`]: Iterator::skip\n  1125:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::position",
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
            "name": "P"
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
                          "output": {
                            "primitive": "bool"
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
                "generic": "P"
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
      "name": "position",
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
            "predicate",
            {
              "generic": "P"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  3120:     /// let a = [1, 2, 3, 4];\n  3121:     ///\n  3122:     /// let mut iter = a.into_iter();\n  3123:     ///\n  3124:     /// assert_eq!(iter.position(|x| x >= 2), Some(1));\n  3125:     ///\n  3126:     /// // we can still use `iter`, as there are more elements.\n  3127:     /// assert_eq!(iter.next(), Some(3));\n  3128:     ///\n  3129:     /// // The returned index depends on iterator state\n  3130:     /// assert_eq!(iter.position(|x| x == 4), Some(0));\n  3131:     ///\n  3132:     /// ```\n  3133:     #[inline]\n  3134:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3135:     #[rustc_non_const_trait_method]\n  3136:     fn position<P>(&mut self, predicate: P) -> Option<usize>\n  3137:     where\n  3138:         Self: Sized,\n  3139:         P: FnMut(Self::Item) -> bool,\n  3140:     {\n  3141:         #[inline]\n  3142:         fn check<'a, T>(\n  3143:             mut predicate: impl FnMut(T) -> bool + 'a,\n  3144:             acc: &'a mut usize,\n  3145:         ) -> impl FnMut((), T) -> ControlFlow<usize, ()> + 'a {\n  3146:             #[rustc_inherit_overflow_checks]\n  3147:             move |_, x| {\n  3148:                 if predicate(x) {\n  3149:                     ControlFlow::Break(*acc)\n  3150:                 } else {\n  3151:                     *acc += 1;\n  3152:                     ControlFlow::Continue(())",
    "nanvix_source": "  3124:     /// // we can still use `iter`, as there are more elements.\n  3125:     /// assert_eq!(iter.next(), Some(3));\n  3126:     ///\n  3127:     /// // The returned index depends on iterator state\n  3128:     /// assert_eq!(iter.position(|x| x == 4), Some(0));\n  3129:     ///\n  3130:     /// ```\n  3131:     #[inline]\n  3132:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3133:     #[rustc_non_const_trait_method]\n  3134:     fn position<P>(&mut self, predicate: P) -> Option<usize>\n  3135:     where\n  3136:         Self: Sized,\n  3137:         P: FnMut(Self::Item) -> bool,\n  3138:     {\n  3139:         #[inline]\n  3140:         fn check<'a, T>(\n  3141:             mut predicate: impl FnMut(T) -> bool + 'a,\n  3142:             acc: &'a mut usize,\n  3143:         ) -> impl FnMut((), T) -> ControlFlow<usize, ()> + 'a {\n  3144:             #[rustc_inherit_overflow_checks]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::product",
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
            "name": "P"
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
                        "angle_bracketed": {
                          "args": [
                            {
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
                          ],
                          "constraints": []
                        }
                      },
                      "id": 4652,
                      "path": "Product"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "P"
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
      "name": "product",
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
          "generic": "P"
        }
      }
    },
    "verification_source": "  3687:     ///\n  3688:     /// When calling `product()` and a primitive integer type is being returned,\n  3689:     /// method will panic if the computation overflows and overflow checks are\n  3690:     /// enabled.\n  3691:     ///\n  3692:     /// # Examples\n  3693:     ///\n  3694:     /// ```\n  3695:     /// fn factorial(n: u32) -> u32 {\n  3696:     ///     (1..=n).product()\n  3697:     /// }\n  3698:     /// assert_eq!(factorial(0), 1);\n  3699:     /// assert_eq!(factorial(1), 1);\n  3700:     /// assert_eq!(factorial(5), 120);\n  3701:     /// ```\n  3702:     #[stable(feature = \"iter_arith\", since = \"1.11.0\")]\n  3703:     fn product<P>(self) -> P\n  3704:     where\n  3705:         Self: Sized,\n  3706:         P: [const] Product<Self::Item>,\n  3707:     {\n  3708:         Product::product(self)\n  3709:     }\n  3710: \n  3711:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3712:     /// of another.\n  3713:     ///\n  3714:     /// # Examples\n  3715:     ///\n  3716:     /// ```\n  3717:     /// use std::cmp::Ordering;\n  3718:     ///\n  3719:     /// assert_eq!([1].iter().cmp([1].iter()), Ordering::Equal);",
    "nanvix_source": "  3691:     ///\n  3692:     /// ```\n  3693:     /// fn factorial(n: u32) -> u32 {\n  3694:     ///     (1..=n).product()\n  3695:     /// }\n  3696:     /// assert_eq!(factorial(0), 1);\n  3697:     /// assert_eq!(factorial(1), 1);\n  3698:     /// assert_eq!(factorial(5), 120);\n  3699:     /// ```\n  3700:     #[stable(feature = \"iter_arith\", since = \"1.11.0\")]\n  3701:     fn product<P>(self) -> P\n  3702:     where\n  3703:         Self: Sized,\n  3704:         P: [const] Product<Self::Item>,\n  3705:     {\n  3706:         Product::product(self)\n  3707:     }\n  3708: \n  3709:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3710:     /// of another.\n  3711:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::reduce",
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
                    "modifier": "maybe_const",
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
      "name": "reduce",
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
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2687:     /// every subsequent element into it.\n  2688:     ///\n  2689:     /// [`fold()`]: Iterator::fold\n  2690:     ///\n  2691:     /// # Example\n  2692:     ///\n  2693:     /// ```\n  2694:     /// let reduced: i32 = (1..10).reduce(|acc, e| acc + e).unwrap_or(0);\n  2695:     /// assert_eq!(reduced, 45);\n  2696:     ///\n  2697:     /// // Which is equivalent to doing it with `fold`:\n  2698:     /// let folded: i32 = (1..10).fold(0, |acc, e| acc + e);\n  2699:     /// assert_eq!(reduced, folded);\n  2700:     /// ```\n  2701:     #[inline]\n  2702:     #[stable(feature = \"iterator_fold_self\", since = \"1.51.0\")]\n  2703:     fn reduce<F>(mut self, f: F) -> Option<Self::Item>\n  2704:     where\n  2705:         Self: Sized + [const] Destruct,\n  2706:         F: [const] FnMut(Self::Item, Self::Item) -> Self::Item + [const] Destruct,\n  2707:     {\n  2708:         let first = self.next()?;\n  2709:         Some(self.fold(first, f))\n  2710:     }\n  2711: \n  2712:     /// Reduces the elements to a single one by repeatedly applying a reducing operation. If the\n  2713:     /// closure returns a failure, the failure is propagated back to the caller immediately.\n  2714:     ///\n  2715:     /// The return type of this method depends on the return type of the closure. If the closure\n  2716:     /// returns `Result<Self::Item, E>`, then this function will return `Result<Option<Self::Item>,\n  2717:     /// E>`. If the closure returns `Option<Self::Item>`, then this function will return\n  2718:     /// `Option<Option<Self::Item>>`.\n  2719:     ///",
    "nanvix_source": "  2691:     /// ```\n  2692:     /// let reduced: i32 = (1..10).reduce(|acc, e| acc + e).unwrap_or(0);\n  2693:     /// assert_eq!(reduced, 45);\n  2694:     ///\n  2695:     /// // Which is equivalent to doing it with `fold`:\n  2696:     /// let folded: i32 = (1..10).fold(0, |acc, e| acc + e);\n  2697:     /// assert_eq!(reduced, folded);\n  2698:     /// ```\n  2699:     #[inline]\n  2700:     #[stable(feature = \"iterator_fold_self\", since = \"1.51.0\")]\n  2701:     fn reduce<F>(mut self, f: F) -> Option<Self::Item>\n  2702:     where\n  2703:         Self: Sized + [const] Destruct,\n  2704:         F: [const] FnMut(Self::Item, Self::Item) -> Self::Item + [const] Destruct,\n  2705:     {\n  2706:         let first = self.next()?;\n  2707:         Some(self.fold(first, f))\n  2708:     }\n  2709: \n  2710:     /// Reduces the elements to a single one by repeatedly applying a reducing operation. If the\n  2711:     /// closure returns a failure, the failure is propagated back to the caller immediately.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::rposition",
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
            "name": "P"
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
                            "primitive": "bool"
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
                "generic": "P"
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
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 76,
                      "path": "ExactSizeIterator"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 74,
                      "path": "DoubleEndedIterator"
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
      "name": "rposition",
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
            "predicate",
            {
              "generic": "P"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  3186:     /// Stopping at the first `true`:\n  3187:     ///\n  3188:     /// ```\n  3189:     /// let a = [-1, 2, 3, 4];\n  3190:     ///\n  3191:     /// let mut iter = a.into_iter();\n  3192:     ///\n  3193:     /// assert_eq!(iter.rposition(|x| x >= 2), Some(3));\n  3194:     ///\n  3195:     /// // we can still use `iter`, as there are more elements.\n  3196:     /// assert_eq!(iter.next(), Some(-1));\n  3197:     /// assert_eq!(iter.next_back(), Some(3));\n  3198:     /// ```\n  3199:     #[inline]\n  3200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3201:     #[rustc_non_const_trait_method]\n  3202:     fn rposition<P>(&mut self, predicate: P) -> Option<usize>\n  3203:     where\n  3204:         P: FnMut(Self::Item) -> bool,\n  3205:         Self: Sized + ExactSizeIterator + DoubleEndedIterator,\n  3206:     {\n  3207:         // No need for an overflow check here, because `ExactSizeIterator`\n  3208:         // implies that the number of elements fits into a `usize`.\n  3209:         #[inline]\n  3210:         fn check<T>(\n  3211:             mut predicate: impl FnMut(T) -> bool,\n  3212:         ) -> impl FnMut(usize, T) -> ControlFlow<usize, usize> {\n  3213:             move |i, x| {\n  3214:                 let i = i - 1;\n  3215:                 if predicate(x) { ControlFlow::Break(i) } else { ControlFlow::Continue(i) }\n  3216:             }\n  3217:         }\n  3218: ",
    "nanvix_source": "  3190:     ///\n  3191:     /// assert_eq!(iter.rposition(|x| x >= 2), Some(3));\n  3192:     ///\n  3193:     /// // we can still use `iter`, as there are more elements.\n  3194:     /// assert_eq!(iter.next(), Some(-1));\n  3195:     /// assert_eq!(iter.next_back(), Some(3));\n  3196:     /// ```\n  3197:     #[inline]\n  3198:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3199:     #[rustc_non_const_trait_method]\n  3200:     fn rposition<P>(&mut self, predicate: P) -> Option<usize>\n  3201:     where\n  3202:         P: FnMut(Self::Item) -> bool,\n  3203:         Self: Sized + ExactSizeIterator + DoubleEndedIterator,\n  3204:     {\n  3205:         // No need for an overflow check here, because `ExactSizeIterator`\n  3206:         // implies that the number of elements fits into a `usize`.\n  3207:         #[inline]\n  3208:         fn check<T>(\n  3209:             mut predicate: impl FnMut(T) -> bool,\n  3210:         ) -> impl FnMut(usize, T) -> ControlFlow<usize, usize> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::scan",
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
            "name": "St"
          },
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
                                  "generic": "St"
                                }
                              }
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
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "generic": "B"
                                      }
                                    }
                                  ],
                                  "constraints": []
                                }
                              },
                              "id": 84,
                              "path": "Option"
                            }
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
      "name": "scan",
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
            "initial_state",
            {
              "generic": "St"
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
                      "generic": "St"
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
            "id": 9895,
            "path": "Scan"
          }
        }
      }
    },
    "verification_source": "  1480:     ///\n  1481:     ///     // ... and terminate if the state exceeds 6\n  1482:     ///     if *state > 6 {\n  1483:     ///         return None;\n  1484:     ///     }\n  1485:     ///     // ... else yield the negation of the state\n  1486:     ///     Some(-*state)\n  1487:     /// });\n  1488:     ///\n  1489:     /// assert_eq!(iter.next(), Some(-1));\n  1490:     /// assert_eq!(iter.next(), Some(-2));\n  1491:     /// assert_eq!(iter.next(), Some(-6));\n  1492:     /// assert_eq!(iter.next(), None);\n  1493:     /// ```\n  1494:     #[inline]\n  1495:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1496:     fn scan<St, B, F>(self, initial_state: St, f: F) -> Scan<Self, St, F>\n  1497:     where\n  1498:         Self: Sized,\n  1499:         F: FnMut(&mut St, Self::Item) -> Option<B>,\n  1500:     {\n  1501:         Scan::new(self, initial_state, f)\n  1502:     }\n  1503: \n  1504:     /// Creates an iterator that works like map, but flattens nested structure.\n  1505:     ///\n  1506:     /// The [`map`] adapter is very useful, but only when the closure\n  1507:     /// argument produces values. If it produces an iterator instead, there's\n  1508:     /// an extra layer of indirection. `flat_map()` will remove this extra layer\n  1509:     /// on its own.\n  1510:     ///\n  1511:     /// You can think of `flat_map(f)` as the semantic equivalent\n  1512:     /// of [`map`]ping, and then [`flatten`]ing as in `map(f).flatten()`.",
    "nanvix_source": "  1484:     ///     Some(-*state)\n  1485:     /// });\n  1486:     ///\n  1487:     /// assert_eq!(iter.next(), Some(-1));\n  1488:     /// assert_eq!(iter.next(), Some(-2));\n  1489:     /// assert_eq!(iter.next(), Some(-6));\n  1490:     /// assert_eq!(iter.next(), None);\n  1491:     /// ```\n  1492:     #[inline]\n  1493:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1494:     fn scan<St, B, F>(self, initial_state: St, f: F) -> Scan<Self, St, F>\n  1495:     where\n  1496:         Self: Sized,\n  1497:         F: FnMut(&mut St, Self::Item) -> Option<B>,\n  1498:     {\n  1499:         Scan::new(self, initial_state, f)\n  1500:     }\n  1501: \n  1502:     /// Creates an iterator that works like map, but flattens nested structure.\n  1503:     ///\n  1504:     /// The [`map`] adapter is very useful, but only when the closure",
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
