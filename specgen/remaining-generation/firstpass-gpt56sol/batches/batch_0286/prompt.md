For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::eq",
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
                      "id": 54,
                      "path": "PartialEq"
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
      "name": "eq",
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
    "verification_source": "  3865:             ControlFlow::Continue(ord) => Some(ord),\n  3866:             ControlFlow::Break(ord) => ord,\n  3867:         }\n  3868:     }\n  3869: \n  3870:     /// Determines if the elements of this [`Iterator`] are equal to those of\n  3871:     /// another.\n  3872:     ///\n  3873:     /// # Examples\n  3874:     ///\n  3875:     /// ```\n  3876:     /// assert_eq!([1].iter().eq([1].iter()), true);\n  3877:     /// assert_eq!([1].iter().eq([1, 2].iter()), false);\n  3878:     /// ```\n  3879:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3880:     #[rustc_non_const_trait_method]\n  3881:     fn eq<I>(self, other: I) -> bool\n  3882:     where\n  3883:         I: IntoIterator,\n  3884:         Self::Item: PartialEq<I::Item>,\n  3885:         Self: Sized,\n  3886:     {\n  3887:         self.eq_by(other, |x, y| x == y)\n  3888:     }\n  3889: \n  3890:     /// Determines if the elements of this [`Iterator`] are equal to those of\n  3891:     /// another with respect to the specified equality function.\n  3892:     ///\n  3893:     /// # Examples\n  3894:     ///\n  3895:     /// ```\n  3896:     /// #![feature(iter_order_by)]\n  3897:     ///",
    "nanvix_source": "  3869:     /// another.\n  3870:     ///\n  3871:     /// # Examples\n  3872:     ///\n  3873:     /// ```\n  3874:     /// assert_eq!([1].iter().eq([1].iter()), true);\n  3875:     /// assert_eq!([1].iter().eq([1, 2].iter()), false);\n  3876:     /// ```\n  3877:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3878:     #[rustc_non_const_trait_method]\n  3879:     fn eq<I>(self, other: I) -> bool\n  3880:     where\n  3881:         I: IntoIterator,\n  3882:         Self::Item: PartialEq<I::Item>,\n  3883:         Self: Sized,\n  3884:     {\n  3885:         self.eq_by(other, |x, y| x == y)\n  3886:     }\n  3887: \n  3888:     /// Determines if the elements of this [`Iterator`] are equal to those of\n  3889:     /// another with respect to the specified equality function.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::filter",
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
      "name": "filter",
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
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9856,
            "path": "Filter"
          }
        }
      }
    },
    "verification_source": "   938:     ///\n   939:     /// ```\n   940:     /// let s = &[0, 1, 2];\n   941:     ///\n   942:     /// let mut iter = s.iter().filter(|&&x| x > 1); // two &s\n   943:     ///\n   944:     /// assert_eq!(iter.next(), Some(&2));\n   945:     /// assert_eq!(iter.next(), None);\n   946:     /// ```\n   947:     ///\n   948:     /// of these layers.\n   949:     ///\n   950:     /// Note that `iter.filter(f).next()` is equivalent to `iter.find(f)`.\n   951:     #[inline]\n   952:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   953:     #[rustc_diagnostic_item = \"iter_filter\"]\n   954:     fn filter<P>(self, predicate: P) -> Filter<Self, P>\n   955:     where\n   956:         Self: Sized,\n   957:         P: FnMut(&Self::Item) -> bool,\n   958:     {\n   959:         Filter::new(self, predicate)\n   960:     }\n   961: \n   962:     /// Creates an iterator that both filters and maps.\n   963:     ///\n   964:     /// The returned iterator yields only the `value`s for which the supplied\n   965:     /// closure returns `Some(value)`.\n   966:     ///\n   967:     /// `filter_map` can be used to make chains of [`filter`] and [`map`] more\n   968:     /// concise. The example below shows how a `map().filter().map()` can be\n   969:     /// shortened to a single call to `filter_map`.\n   970:     ///",
    "nanvix_source": "   942:     /// assert_eq!(iter.next(), Some(&2));\n   943:     /// assert_eq!(iter.next(), None);\n   944:     /// ```\n   945:     ///\n   946:     /// of these layers.\n   947:     ///\n   948:     /// Note that `iter.filter(f).next()` is equivalent to `iter.find(f)`.\n   949:     #[inline]\n   950:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   951:     #[rustc_diagnostic_item = \"iter_filter\"]\n   952:     fn filter<P>(self, predicate: P) -> Filter<Self, P>\n   953:     where\n   954:         Self: Sized,\n   955:         P: FnMut(&Self::Item) -> bool,\n   956:     {\n   957:         Filter::new(self, predicate)\n   958:     }\n   959: \n   960:     /// Creates an iterator that both filters and maps.\n   961:     ///\n   962:     /// The returned iterator yields only the `value`s for which the supplied",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::filter_map",
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
      "name": "filter_map",
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
            "id": 9859,
            "path": "FilterMap"
          }
        }
      }
    },
    "verification_source": "   983:     /// assert_eq!(iter.next(), Some(1));\n   984:     /// assert_eq!(iter.next(), Some(5));\n   985:     /// assert_eq!(iter.next(), None);\n   986:     /// ```\n   987:     ///\n   988:     /// Here's the same example, but with [`filter`] and [`map`]:\n   989:     ///\n   990:     /// ```\n   991:     /// let a = [\"1\", \"two\", \"NaN\", \"four\", \"5\"];\n   992:     /// let mut iter = a.iter().map(|s| s.parse()).filter(|s| s.is_ok()).map(|s| s.unwrap());\n   993:     /// assert_eq!(iter.next(), Some(1));\n   994:     /// assert_eq!(iter.next(), Some(5));\n   995:     /// assert_eq!(iter.next(), None);\n   996:     /// ```\n   997:     #[inline]\n   998:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   999:     fn filter_map<B, F>(self, f: F) -> FilterMap<Self, F>\n  1000:     where\n  1001:         Self: Sized,\n  1002:         F: FnMut(Self::Item) -> Option<B>,\n  1003:     {\n  1004:         FilterMap::new(self, f)\n  1005:     }\n  1006: \n  1007:     /// Creates an iterator which gives the current iteration count as well as\n  1008:     /// the next value.\n  1009:     ///\n  1010:     /// The iterator returned yields pairs `(i, val)`, where `i` is the\n  1011:     /// current index of iteration and `val` is the value returned by the\n  1012:     /// iterator.\n  1013:     ///\n  1014:     /// `enumerate()` keeps its count as a [`usize`]. If you want to count by a\n  1015:     /// different sized integer, the [`zip`] function provides similar",
    "nanvix_source": "   987:     ///\n   988:     /// ```\n   989:     /// let a = [\"1\", \"two\", \"NaN\", \"four\", \"5\"];\n   990:     /// let mut iter = a.iter().map(|s| s.parse()).filter(|s| s.is_ok()).map(|s| s.unwrap());\n   991:     /// assert_eq!(iter.next(), Some(1));\n   992:     /// assert_eq!(iter.next(), Some(5));\n   993:     /// assert_eq!(iter.next(), None);\n   994:     /// ```\n   995:     #[inline]\n   996:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   997:     fn filter_map<B, F>(self, f: F) -> FilterMap<Self, F>\n   998:     where\n   999:         Self: Sized,\n  1000:         F: FnMut(Self::Item) -> Option<B>,\n  1001:     {\n  1002:         FilterMap::new(self, f)\n  1003:     }\n  1004: \n  1005:     /// Creates an iterator which gives the current iteration count as well as\n  1006:     /// the next value.\n  1007:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::find_map",
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
      "name": "find_map",
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
    "verification_source": "  2977:     /// the first non-none result.\n  2978:     ///\n  2979:     /// `iter.find_map(f)` is equivalent to `iter.filter_map(f).next()`.\n  2980:     ///\n  2981:     /// # Examples\n  2982:     ///\n  2983:     /// ```\n  2984:     /// let a = [\"lol\", \"NaN\", \"2\", \"5\"];\n  2985:     ///\n  2986:     /// let first_number = a.iter().find_map(|s| s.parse().ok());\n  2987:     ///\n  2988:     /// assert_eq!(first_number, Some(2));\n  2989:     /// ```\n  2990:     #[inline]\n  2991:     #[stable(feature = \"iterator_find_map\", since = \"1.30.0\")]\n  2992:     #[rustc_non_const_trait_method]\n  2993:     fn find_map<B, F>(&mut self, f: F) -> Option<B>\n  2994:     where\n  2995:         Self: Sized,\n  2996:         F: FnMut(Self::Item) -> Option<B>,\n  2997:     {\n  2998:         #[inline]\n  2999:         fn check<T, B>(mut f: impl FnMut(T) -> Option<B>) -> impl FnMut((), T) -> ControlFlow<B> {\n  3000:             move |(), x| match f(x) {\n  3001:                 Some(x) => ControlFlow::Break(x),\n  3002:                 None => ControlFlow::Continue(()),\n  3003:             }\n  3004:         }\n  3005: \n  3006:         self.try_fold((), check(f)).break_value()\n  3007:     }\n  3008: \n  3009:     /// Applies function to the elements of iterator and returns",
    "nanvix_source": "  2981:     /// ```\n  2982:     /// let a = [\"lol\", \"NaN\", \"2\", \"5\"];\n  2983:     ///\n  2984:     /// let first_number = a.iter().find_map(|s| s.parse().ok());\n  2985:     ///\n  2986:     /// assert_eq!(first_number, Some(2));\n  2987:     /// ```\n  2988:     #[inline]\n  2989:     #[stable(feature = \"iterator_find_map\", since = \"1.30.0\")]\n  2990:     #[rustc_non_const_trait_method]\n  2991:     fn find_map<B, F>(&mut self, f: F) -> Option<B>\n  2992:     where\n  2993:         Self: Sized,\n  2994:         F: FnMut(Self::Item) -> Option<B>,\n  2995:     {\n  2996:         #[inline]\n  2997:         fn check<T, B>(mut f: impl FnMut(T) -> Option<B>) -> impl FnMut((), T) -> ControlFlow<B> {\n  2998:             move |(), x| match f(x) {\n  2999:                 Some(x) => ControlFlow::Break(x),\n  3000:                 None => ControlFlow::Continue(()),\n  3001:             }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::flat_map",
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
            "name": "U"
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
                      "args": null,
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
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
                            "generic": "U"
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
      "name": "flat_map",
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
                      "generic": "U"
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
            "id": 9863,
            "path": "FlatMap"
          }
        }
      }
    },
    "verification_source": "  1519:     /// [`flatten`]: Iterator::flatten\n  1520:     ///\n  1521:     /// # Examples\n  1522:     ///\n  1523:     /// ```\n  1524:     /// let words = [\"alpha\", \"beta\", \"gamma\"];\n  1525:     ///\n  1526:     /// // chars() returns an iterator\n  1527:     /// let merged: String = words.iter()\n  1528:     ///                           .flat_map(|s| s.chars())\n  1529:     ///                           .collect();\n  1530:     /// assert_eq!(merged, \"alphabetagamma\");\n  1531:     /// ```\n  1532:     #[inline]\n  1533:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1534:     #[rustc_non_const_trait_method]\n  1535:     fn flat_map<U, F>(self, f: F) -> FlatMap<Self, U, F>\n  1536:     where\n  1537:         Self: Sized,\n  1538:         U: IntoIterator,\n  1539:         F: FnMut(Self::Item) -> U,\n  1540:     {\n  1541:         FlatMap::new(self, f)\n  1542:     }\n  1543: \n  1544:     /// Creates an iterator that flattens nested structure.\n  1545:     ///\n  1546:     /// This is useful when you have an iterator of iterators or an iterator of\n  1547:     /// things that can be turned into iterators and you want to remove one\n  1548:     /// level of indirection.\n  1549:     ///\n  1550:     /// # Examples\n  1551:     ///",
    "nanvix_source": "  1523:     ///\n  1524:     /// // chars() returns an iterator\n  1525:     /// let merged: String = words.iter()\n  1526:     ///                           .flat_map(|s| s.chars())\n  1527:     ///                           .collect();\n  1528:     /// assert_eq!(merged, \"alphabetagamma\");\n  1529:     /// ```\n  1530:     #[inline]\n  1531:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1532:     #[rustc_non_const_trait_method]\n  1533:     fn flat_map<U, F>(self, f: F) -> FlatMap<Self, U, F>\n  1534:     where\n  1535:         Self: Sized,\n  1536:         U: IntoIterator,\n  1537:         F: FnMut(Self::Item) -> U,\n  1538:     {\n  1539:         FlatMap::new(self, f)\n  1540:     }\n  1541: \n  1542:     /// Creates an iterator that flattens nested structure.\n  1543:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::flatten",
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
                      "id": 80,
                      "path": "IntoIterator"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "flatten",
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
            "id": 9866,
            "path": "Flatten"
          }
        }
      }
    },
    "verification_source": "  1603:     /// let d2: Vec<_> = d3.into_iter().flatten().collect();\n  1604:     /// assert_eq!(d2, [[1, 2], [3, 4], [5, 6], [7, 8]]);\n  1605:     ///\n  1606:     /// let d1: Vec<_> = d3.into_iter().flatten().flatten().collect();\n  1607:     /// assert_eq!(d1, [1, 2, 3, 4, 5, 6, 7, 8]);\n  1608:     /// ```\n  1609:     ///\n  1610:     /// Here we see that `flatten()` does not perform a \"deep\" flatten.\n  1611:     /// Instead, only one level of nesting is removed. That is, if you\n  1612:     /// `flatten()` a three-dimensional array, the result will be\n  1613:     /// two-dimensional and not one-dimensional. To get a one-dimensional\n  1614:     /// structure, you have to `flatten()` again.\n  1615:     ///\n  1616:     /// [`flat_map()`]: Iterator::flat_map\n  1617:     #[inline]\n  1618:     #[stable(feature = \"iterator_flatten\", since = \"1.29.0\")]\n  1619:     fn flatten(self) -> Flatten<Self>\n  1620:     where\n  1621:         Self: Sized,\n  1622:         Self::Item: IntoIterator,\n  1623:     {\n  1624:         Flatten::new(self)\n  1625:     }\n  1626: \n  1627:     /// Calls the given function `f` for each contiguous window of size `N` over\n  1628:     /// `self` and returns an iterator over the outputs of `f`. Like [`slice::windows()`],\n  1629:     /// the windows during mapping overlap as well.\n  1630:     ///\n  1631:     /// In the following example, the closure is called three times with the\n  1632:     /// arguments `&['a', 'b']`, `&['b', 'c']` and `&['c', 'd']` respectively.\n  1633:     ///\n  1634:     /// ```\n  1635:     /// #![feature(iter_map_windows)]",
    "nanvix_source": "  1607:     ///\n  1608:     /// Here we see that `flatten()` does not perform a \"deep\" flatten.\n  1609:     /// Instead, only one level of nesting is removed. That is, if you\n  1610:     /// `flatten()` a three-dimensional array, the result will be\n  1611:     /// two-dimensional and not one-dimensional. To get a one-dimensional\n  1612:     /// structure, you have to `flatten()` again.\n  1613:     ///\n  1614:     /// [`flat_map()`]: Iterator::flat_map\n  1615:     #[inline]\n  1616:     #[stable(feature = \"iterator_flatten\", since = \"1.29.0\")]\n  1617:     fn flatten(self) -> Flatten<Self>\n  1618:     where\n  1619:         Self: Sized,\n  1620:         Self::Item: IntoIterator,\n  1621:     {\n  1622:         Flatten::new(self)\n  1623:     }\n  1624: \n  1625:     /// Calls the given function `f` for each contiguous window of size `N` over\n  1626:     /// `self` and returns an iterator over the outputs of `f`. Like [`slice::windows()`],\n  1627:     /// the windows during mapping overlap as well.",
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
