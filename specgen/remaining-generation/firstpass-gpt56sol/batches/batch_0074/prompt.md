For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::Ref::map_split",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
          {
            "kind": {
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "V"
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
                            "tuple": [
                              {
                                "borrowed_ref": {
                                  "is_mutable": false,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "U"
                                  }
                                }
                              },
                              {
                                "borrowed_ref": {
                                  "is_mutable": false,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "V"
                                  }
                                }
                              }
                            ]
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
      "name": "map_split",
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
                    "lifetime": "'b"
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
            "id": 13316,
            "path": "Ref"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'b"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24842",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13316",
        "resolved_owner_path": [
          "core",
          "cell",
          "Ref"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13316,
                "path": "Ref"
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
          "tuple": [
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
                      },
                      {
                        "type": {
                          "generic": "U"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 13316,
                "path": "Ref"
              }
            },
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
                      },
                      {
                        "type": {
                          "generic": "V"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 13316,
                "path": "Ref"
              }
            }
          ]
        }
      }
    },
    "verification_source": "  1760:     /// `Ref::map_split(...)`. A method would interfere with methods of the same\n  1761:     /// name on the contents of a `RefCell` used through `Deref`.\n  1762:     ///\n  1763:     /// # Examples\n  1764:     ///\n  1765:     /// ```\n  1766:     /// use std::cell::{Ref, RefCell};\n  1767:     ///\n  1768:     /// let cell = RefCell::new([1, 2, 3, 4]);\n  1769:     /// let borrow = cell.borrow();\n  1770:     /// let (begin, end) = Ref::map_split(borrow, |slice| slice.split_at(2));\n  1771:     /// assert_eq!(*begin, [1, 2]);\n  1772:     /// assert_eq!(*end, [3, 4]);\n  1773:     /// ```\n  1774:     #[stable(feature = \"refcell_map_split\", since = \"1.35.0\")]\n  1775:     #[inline]\n  1776:     pub fn map_split<U: ?Sized, V: ?Sized, F>(orig: Ref<'b, T>, f: F) -> (Ref<'b, U>, Ref<'b, V>)\n  1777:     where\n  1778:         F: FnOnce(&T) -> (&U, &V),\n  1779:     {\n  1780:         let (a, b) = f(&*orig);\n  1781:         let borrow = orig.borrow.clone();\n  1782:         (\n  1783:             Ref { value: NonNull::from(a), borrow },\n  1784:             Ref { value: NonNull::from(b), borrow: orig.borrow },\n  1785:         )\n  1786:     }\n  1787: \n  1788:     /// Converts into a reference to the underlying data.\n  1789:     ///\n  1790:     /// The underlying `RefCell` can never be mutably borrowed from again and will always appear\n  1791:     /// already immutably borrowed. It is not a good idea to leak more than a constant number of\n  1792:     /// references. The `RefCell` can be immutably borrowed again if only a smaller number of leaks",
    "nanvix_source": "  1766:     /// use std::cell::{Ref, RefCell};\n  1767:     ///\n  1768:     /// let cell = RefCell::new([1, 2, 3, 4]);\n  1769:     /// let borrow = cell.borrow();\n  1770:     /// let (begin, end) = Ref::map_split(borrow, |slice| slice.split_at(2));\n  1771:     /// assert_eq!(*begin, [1, 2]);\n  1772:     /// assert_eq!(*end, [3, 4]);\n  1773:     /// ```\n  1774:     #[stable(feature = \"refcell_map_split\", since = \"1.35.0\")]\n  1775:     #[inline]\n  1776:     pub fn map_split<U: ?Sized, V: ?Sized, F>(orig: Ref<'b, T>, f: F) -> (Ref<'b, U>, Ref<'b, V>)\n  1777:     where\n  1778:         F: FnOnce(&T) -> (&U, &V),\n  1779:     {\n  1780:         let (a, b) = f(&*orig);\n  1781:         let borrow = orig.borrow.clone();\n  1782:         (\n  1783:             Ref { value: NonNull::from(a), borrow },\n  1784:             Ref { value: NonNull::from(b), borrow: orig.borrow },\n  1785:         )\n  1786:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::replace_with",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                              "generic": "T"
                            }
                          }
                        },
                        "id": 24,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "replace_with",
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
            "id": 9393,
            "path": "RefCell"
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
        "impl_id": "core:24784",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1033:     ///\n  1034:     /// Panics if the value is currently borrowed.\n  1035:     ///\n  1036:     /// # Examples\n  1037:     ///\n  1038:     /// ```\n  1039:     /// use std::cell::RefCell;\n  1040:     /// let cell = RefCell::new(5);\n  1041:     /// let old_value = cell.replace_with(|&mut old| old + 1);\n  1042:     /// assert_eq!(old_value, 5);\n  1043:     /// assert_eq!(cell, RefCell::new(6));\n  1044:     /// ```\n  1045:     #[inline]\n  1046:     #[stable(feature = \"refcell_replace_swap\", since = \"1.35.0\")]\n  1047:     #[track_caller]\n  1048:     #[rustc_should_not_be_called_on_const_items]\n  1049:     pub fn replace_with<F: FnOnce(&mut T) -> T>(&self, f: F) -> T {\n  1050:         let mut_borrow = &mut *self.borrow_mut();\n  1051:         let replacement = f(mut_borrow);\n  1052:         mem::replace(mut_borrow, replacement)\n  1053:     }\n  1054: \n  1055:     /// Swaps the wrapped value of `self` with the wrapped value of `other`,\n  1056:     /// without deinitializing either one.\n  1057:     ///\n  1058:     /// This function corresponds to [`std::mem::swap`](../mem/fn.swap.html).\n  1059:     ///\n  1060:     /// # Panics\n  1061:     ///\n  1062:     /// Panics if the value in either `RefCell` is currently borrowed, or\n  1063:     /// if `self` and `other` point to the same `RefCell`.\n  1064:     ///\n  1065:     /// # Examples",
    "nanvix_source": "  1039:     /// use std::cell::RefCell;\n  1040:     /// let cell = RefCell::new(5);\n  1041:     /// let old_value = cell.replace_with(|&mut old| old + 1);\n  1042:     /// assert_eq!(old_value, 5);\n  1043:     /// assert_eq!(cell, RefCell::new(6));\n  1044:     /// ```\n  1045:     #[inline]\n  1046:     #[stable(feature = \"refcell_replace_swap\", since = \"1.35.0\")]\n  1047:     #[track_caller]\n  1048:     #[rustc_should_not_be_called_on_const_items]\n  1049:     pub fn replace_with<F: FnOnce(&mut T) -> T>(&self, f: F) -> T {\n  1050:         let mut_borrow = &mut *self.borrow_mut();\n  1051:         let replacement = f(mut_borrow);\n  1052:         mem::replace(mut_borrow, replacement)\n  1053:     }\n  1054: \n  1055:     /// Swaps the wrapped value of `self` with the wrapped value of `other`,\n  1056:     /// without deinitializing either one.\n  1057:     ///\n  1058:     /// This function corresponds to [`std::mem::swap`](../mem/fn.swap.html).\n  1059:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefMut::filter_map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
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
                                            "generic": "U"
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
                      "id": 24,
                      "path": "FnOnce"
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
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'b"
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
            "id": 13318,
            "path": "RefMut"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'b"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24866",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13318",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefMut"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13318,
                "path": "RefMut"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'b"
                              },
                              {
                                "type": {
                                  "generic": "U"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 13318,
                        "path": "RefMut"
                      }
                    }
                  },
                  {
                    "type": {
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1883:     ///\n  1884:     /// let c = RefCell::new(vec![1, 2, 3]);\n  1885:     ///\n  1886:     /// {\n  1887:     ///     let b1: RefMut<'_, Vec<u32>> = c.borrow_mut();\n  1888:     ///     let mut b2: Result<RefMut<'_, u32>, _> = RefMut::filter_map(b1, |v| v.get_mut(1));\n  1889:     ///\n  1890:     ///     if let Ok(mut b2) = b2 {\n  1891:     ///         *b2 += 2;\n  1892:     ///     }\n  1893:     /// }\n  1894:     ///\n  1895:     /// assert_eq!(*c.borrow(), vec![1, 4, 3]);\n  1896:     /// ```\n  1897:     #[stable(feature = \"cell_filter_map\", since = \"1.63.0\")]\n  1898:     #[inline]\n  1899:     pub fn filter_map<U: ?Sized, F>(mut orig: RefMut<'b, T>, f: F) -> Result<RefMut<'b, U>, Self>\n  1900:     where\n  1901:         F: FnOnce(&mut T) -> Option<&mut U>,\n  1902:     {\n  1903:         // SAFETY: function holds onto an exclusive reference for the duration\n  1904:         // of its call through `orig`, and the pointer is only de-referenced\n  1905:         // inside of the function call never allowing the exclusive reference to\n  1906:         // escape.\n  1907:         match f(&mut *orig) {\n  1908:             Some(value) => {\n  1909:                 Ok(RefMut { value: NonNull::from(value), borrow: orig.borrow, marker: PhantomData })\n  1910:             }\n  1911:             None => Err(orig),\n  1912:         }\n  1913:     }\n  1914: \n  1915:     /// Tries to makes a new `RefMut` for a component of the borrowed data.",
    "nanvix_source": "  1889:     ///\n  1890:     ///     if let Ok(mut b2) = b2 {\n  1891:     ///         *b2 += 2;\n  1892:     ///     }\n  1893:     /// }\n  1894:     ///\n  1895:     /// assert_eq!(*c.borrow(), vec![1, 4, 3]);\n  1896:     /// ```\n  1897:     #[stable(feature = \"cell_filter_map\", since = \"1.63.0\")]\n  1898:     #[inline]\n  1899:     pub fn filter_map<U: ?Sized, F>(mut orig: RefMut<'b, T>, f: F) -> Result<RefMut<'b, U>, Self>\n  1900:     where\n  1901:         F: FnOnce(&mut T) -> Option<&mut U>,\n  1902:     {\n  1903:         // SAFETY: function holds onto an exclusive reference for the duration\n  1904:         // of its call through `orig`, and the pointer is only de-referenced\n  1905:         // inside of the function call never allowing the exclusive reference to\n  1906:         // escape.\n  1907:         match f(&mut *orig) {\n  1908:             Some(value) => {\n  1909:                 Ok(RefMut { value: NonNull::from(value), borrow: orig.borrow, marker: PhantomData })",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefMut::map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
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
                            "borrowed_ref": {
                              "is_mutable": true,
                              "lifetime": null,
                              "type": {
                                "generic": "U"
                              }
                            }
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
      "name": "map",
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
                    "lifetime": "'b"
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
            "id": 13318,
            "path": "RefMut"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'b"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24866",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13318",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefMut"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13318,
                "path": "RefMut"
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
                    "lifetime": "'b"
                  },
                  {
                    "type": {
                      "generic": "U"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13318,
            "path": "RefMut"
          }
        }
      }
    },
    "verification_source": "  1845:     /// # Examples\n  1846:     ///\n  1847:     /// ```\n  1848:     /// use std::cell::{RefCell, RefMut};\n  1849:     ///\n  1850:     /// let c = RefCell::new((5, 'b'));\n  1851:     /// {\n  1852:     ///     let b1: RefMut<'_, (u32, char)> = c.borrow_mut();\n  1853:     ///     let mut b2: RefMut<'_, u32> = RefMut::map(b1, |t| &mut t.0);\n  1854:     ///     assert_eq!(*b2, 5);\n  1855:     ///     *b2 = 42;\n  1856:     /// }\n  1857:     /// assert_eq!(*c.borrow(), (42, 'b'));\n  1858:     /// ```\n  1859:     #[stable(feature = \"cell_map\", since = \"1.8.0\")]\n  1860:     #[inline]\n  1861:     pub fn map<U: ?Sized, F>(mut orig: RefMut<'b, T>, f: F) -> RefMut<'b, U>\n  1862:     where\n  1863:         F: FnOnce(&mut T) -> &mut U,\n  1864:     {\n  1865:         let value = NonNull::from(f(&mut *orig));\n  1866:         RefMut { value, borrow: orig.borrow, marker: PhantomData }\n  1867:     }\n  1868: \n  1869:     /// Makes a new `RefMut` for an optional component of the borrowed data. The\n  1870:     /// original guard is returned as an `Err(..)` if the closure returns\n  1871:     /// `None`.\n  1872:     ///\n  1873:     /// The `RefCell` is already mutably borrowed, so this cannot fail.\n  1874:     ///\n  1875:     /// This is an associated function that needs to be used as\n  1876:     /// `RefMut::filter_map(...)`. A method would interfere with methods of the\n  1877:     /// same name on the contents of a `RefCell` used through `Deref`.",
    "nanvix_source": "  1851:     /// {\n  1852:     ///     let b1: RefMut<'_, (u32, char)> = c.borrow_mut();\n  1853:     ///     let mut b2: RefMut<'_, u32> = RefMut::map(b1, |t| &mut t.0);\n  1854:     ///     assert_eq!(*b2, 5);\n  1855:     ///     *b2 = 42;\n  1856:     /// }\n  1857:     /// assert_eq!(*c.borrow(), (42, 'b'));\n  1858:     /// ```\n  1859:     #[stable(feature = \"cell_map\", since = \"1.8.0\")]\n  1860:     #[inline]\n  1861:     pub fn map<U: ?Sized, F>(mut orig: RefMut<'b, T>, f: F) -> RefMut<'b, U>\n  1862:     where\n  1863:         F: FnOnce(&mut T) -> &mut U,\n  1864:     {\n  1865:         let value = NonNull::from(f(&mut *orig));\n  1866:         RefMut { value, borrow: orig.borrow, marker: PhantomData }\n  1867:     }\n  1868: \n  1869:     /// Makes a new `RefMut` for an optional component of the borrowed data. The\n  1870:     /// original guard is returned as an `Err(..)` if the closure returns\n  1871:     /// `None`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefMut::map_split",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
          {
            "kind": {
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "V"
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
                            "tuple": [
                              {
                                "borrowed_ref": {
                                  "is_mutable": true,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "U"
                                  }
                                }
                              },
                              {
                                "borrowed_ref": {
                                  "is_mutable": true,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "V"
                                  }
                                }
                              }
                            ]
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
      "name": "map_split",
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
                    "lifetime": "'b"
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
            "id": 13318,
            "path": "RefMut"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'b"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24866",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13318",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefMut"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13318,
                "path": "RefMut"
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
          "tuple": [
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
                      },
                      {
                        "type": {
                          "generic": "U"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 13318,
                "path": "RefMut"
              }
            },
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
                      },
                      {
                        "type": {
                          "generic": "V"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 13318,
                "path": "RefMut"
              }
            }
          ]
        }
      }
    },
    "verification_source": "  1978:     ///\n  1979:     /// # Examples\n  1980:     ///\n  1981:     /// ```\n  1982:     /// use std::cell::{RefCell, RefMut};\n  1983:     ///\n  1984:     /// let cell = RefCell::new([1, 2, 3, 4]);\n  1985:     /// let borrow = cell.borrow_mut();\n  1986:     /// let (mut begin, mut end) = RefMut::map_split(borrow, |slice| slice.split_at_mut(2));\n  1987:     /// assert_eq!(*begin, [1, 2]);\n  1988:     /// assert_eq!(*end, [3, 4]);\n  1989:     /// begin.copy_from_slice(&[4, 3]);\n  1990:     /// end.copy_from_slice(&[2, 1]);\n  1991:     /// ```\n  1992:     #[stable(feature = \"refcell_map_split\", since = \"1.35.0\")]\n  1993:     #[inline]\n  1994:     pub fn map_split<U: ?Sized, V: ?Sized, F>(\n  1995:         mut orig: RefMut<'b, T>,\n  1996:         f: F,\n  1997:     ) -> (RefMut<'b, U>, RefMut<'b, V>)\n  1998:     where\n  1999:         F: FnOnce(&mut T) -> (&mut U, &mut V),\n  2000:     {\n  2001:         let borrow = orig.borrow.clone();\n  2002:         let (a, b) = f(&mut *orig);\n  2003:         (\n  2004:             RefMut { value: NonNull::from(a), borrow, marker: PhantomData },\n  2005:             RefMut { value: NonNull::from(b), borrow: orig.borrow, marker: PhantomData },\n  2006:         )\n  2007:     }\n  2008: \n  2009:     /// Converts into a mutable reference to the underlying data.\n  2010:     ///",
    "nanvix_source": "  1984:     /// let cell = RefCell::new([1, 2, 3, 4]);\n  1985:     /// let borrow = cell.borrow_mut();\n  1986:     /// let (mut begin, mut end) = RefMut::map_split(borrow, |slice| slice.split_at_mut(2));\n  1987:     /// assert_eq!(*begin, [1, 2]);\n  1988:     /// assert_eq!(*end, [3, 4]);\n  1989:     /// begin.copy_from_slice(&[4, 3]);\n  1990:     /// end.copy_from_slice(&[2, 1]);\n  1991:     /// ```\n  1992:     #[stable(feature = \"refcell_map_split\", since = \"1.35.0\")]\n  1993:     #[inline]\n  1994:     pub fn map_split<U: ?Sized, V: ?Sized, F>(\n  1995:         mut orig: RefMut<'b, T>,\n  1996:         f: F,\n  1997:     ) -> (RefMut<'b, U>, RefMut<'b, V>)\n  1998:     where\n  1999:         F: FnOnce(&mut T) -> (&mut U, &mut V),\n  2000:     {\n  2001:         let borrow = orig.borrow.clone();\n  2002:         let (a, b) = f(&mut *orig);\n  2003:         (\n  2004:             RefMut { value: NonNull::from(a), borrow, marker: PhantomData },",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::then_with",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [],
                          "output": {
                            "resolved_path": {
                              "args": null,
                              "id": 1682,
                              "path": "Ordering"
                            }
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "then_with",
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
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        }
      }
    },
    "verification_source": "   636:     /// let result = Ordering::Less.then_with(|| Ordering::Greater);\n   637:     /// assert_eq!(result, Ordering::Less);\n   638:     ///\n   639:     /// let result = Ordering::Equal.then_with(|| Ordering::Equal);\n   640:     /// assert_eq!(result, Ordering::Equal);\n   641:     ///\n   642:     /// let x: (i64, i64, i64) = (1, 2, 7);\n   643:     /// let y: (i64, i64, i64) = (1, 5, 3);\n   644:     /// let result = x.0.cmp(&y.0).then_with(|| x.1.cmp(&y.1)).then_with(|| x.2.cmp(&y.2));\n   645:     ///\n   646:     /// assert_eq!(result, Ordering::Less);\n   647:     /// ```\n   648:     #[inline]\n   649:     #[must_use]\n   650:     #[stable(feature = \"ordering_chaining\", since = \"1.17.0\")]\n   651:     #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n   652:     pub const fn then_with<F>(self, f: F) -> Ordering\n   653:     where\n   654:         F: [const] FnOnce() -> Ordering + [const] Destruct,\n   655:     {\n   656:         match self {\n   657:             Equal => f(),\n   658:             _ => self,\n   659:         }\n   660:     }\n   661: }\n   662: \n   663: /// A helper struct for reverse ordering.\n   664: ///\n   665: /// This struct is a helper to be used with functions like [`Vec::sort_by_key`] and\n   666: /// can be used to reverse order a part of a key.\n   667: ///\n   668: /// [`Vec::sort_by_key`]: ../../std/vec/struct.Vec.html#method.sort_by_key",
    "nanvix_source": "   643:     /// let x: (i64, i64, i64) = (1, 2, 7);\n   644:     /// let y: (i64, i64, i64) = (1, 5, 3);\n   645:     /// let result = x.0.cmp(&y.0).then_with(|| x.1.cmp(&y.1)).then_with(|| x.2.cmp(&y.2));\n   646:     ///\n   647:     /// assert_eq!(result, Ordering::Less);\n   648:     /// ```\n   649:     #[inline]\n   650:     #[must_use]\n   651:     #[stable(feature = \"ordering_chaining\", since = \"1.17.0\")]\n   652:     #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n   653:     pub const fn then_with<F>(self, f: F) -> Ordering\n   654:     where\n   655:         F: [const] FnOnce() -> Ordering + [const] Destruct,\n   656:     {\n   657:         match self {\n   658:             Equal => f(),\n   659:             _ => self,\n   660:         }\n   661:     }\n   662: }\n   663: ",
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
