For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BTreeSet::range",
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
            "name": "K"
          },
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
                      "args": null,
                      "id": 176,
                      "path": "Ord"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 29,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
                                "generic": "K"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 30,
                      "path": "Borrow"
                    }
                  }
                },
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
                                "generic": "K"
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
            "id": 1996,
            "path": "BTreeSet"
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
                    },
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
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:2109",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1996",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "set",
          "BTreeSet"
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
            "id": 2070,
            "path": "Range"
          }
        }
      }
    },
    "verification_source": "   382:     /// # Examples\n   383:     ///\n   384:     /// ```\n   385:     /// use std::collections::BTreeSet;\n   386:     /// use std::ops::Bound::Included;\n   387:     ///\n   388:     /// let mut set = BTreeSet::new();\n   389:     /// set.insert(3);\n   390:     /// set.insert(5);\n   391:     /// set.insert(8);\n   392:     /// for &elem in set.range((Included(&4), Included(&8))) {\n   393:     ///     println!(\"{elem}\");\n   394:     /// }\n   395:     /// assert_eq!(Some(&5), set.range(4..).next());\n   396:     /// ```\n   397:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n   398:     pub fn range<K: ?Sized, R>(&self, range: R) -> Range<'_, T>\n   399:     where\n   400:         K: Ord,\n   401:         T: Borrow<K> + Ord,\n   402:         R: RangeBounds<K>,\n   403:     {\n   404:         Range { iter: self.map.range(range) }\n   405:     }\n   406: \n   407:     /// Visits the elements representing the difference,\n   408:     /// i.e., the elements that are in `self` but not in `other`,\n   409:     /// in ascending order.\n   410:     ///\n   411:     /// # Examples\n   412:     ///\n   413:     /// ```\n   414:     /// use std::collections::BTreeSet;",
    "nanvix_source": "   388:     /// let mut set = BTreeSet::new();\n   389:     /// set.insert(3);\n   390:     /// set.insert(5);\n   391:     /// set.insert(8);\n   392:     /// for &elem in set.range((Included(&4), Included(&8))) {\n   393:     ///     println!(\"{elem}\");\n   394:     /// }\n   395:     /// assert_eq!(Some(&5), set.range(4..).next());\n   396:     /// ```\n   397:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n   398:     pub fn range<K: ?Sized, R>(&self, range: R) -> Range<'_, T>\n   399:     where\n   400:         K: Ord,\n   401:         T: Borrow<K> + Ord,\n   402:         R: RangeBounds<K>,\n   403:     {\n   404:         Range { iter: self.map.range(range) }\n   405:     }\n   406: \n   407:     /// Visits the elements representing the difference,\n   408:     /// i.e., the elements that are in `self` but not in `other`,",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::retain",
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
            "id": 1996,
            "path": "BTreeSet"
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
                    },
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
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:2109",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1996",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "set",
          "BTreeSet"
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
    "verification_source": "  1086:     /// Retains only the elements specified by the predicate.\n  1087:     ///\n  1088:     /// In other words, remove all elements `e` for which `f(&e)` returns `false`.\n  1089:     /// The elements are visited in ascending order.\n  1090:     ///\n  1091:     /// # Examples\n  1092:     ///\n  1093:     /// ```\n  1094:     /// use std::collections::BTreeSet;\n  1095:     ///\n  1096:     /// let mut set = BTreeSet::from([1, 2, 3, 4, 5, 6]);\n  1097:     /// // Keep only the even numbers.\n  1098:     /// set.retain(|&k| k % 2 == 0);\n  1099:     /// assert!(set.iter().eq([2, 4, 6].iter()));\n  1100:     /// ```\n  1101:     #[stable(feature = \"btree_retain\", since = \"1.53.0\")]\n  1102:     pub fn retain<F>(&mut self, mut f: F)\n  1103:     where\n  1104:         T: Ord,\n  1105:         F: FnMut(&T) -> bool,\n  1106:     {\n  1107:         self.extract_if(.., |v| !f(v)).for_each(drop);\n  1108:     }\n  1109: \n  1110:     /// Moves all elements from `other` into `self`, leaving `other` empty.\n  1111:     ///\n  1112:     /// # Examples\n  1113:     ///\n  1114:     /// ```\n  1115:     /// use std::collections::BTreeSet;\n  1116:     ///\n  1117:     /// let mut a = BTreeSet::new();\n  1118:     /// a.insert(1);",
    "nanvix_source": "  1092:     ///\n  1093:     /// ```\n  1094:     /// use std::collections::BTreeSet;\n  1095:     ///\n  1096:     /// let mut set = BTreeSet::from([1, 2, 3, 4, 5, 6]);\n  1097:     /// // Keep only the even numbers.\n  1098:     /// set.retain(|&k| k % 2 == 0);\n  1099:     /// assert!(set.iter().eq([2, 4, 6].iter()));\n  1100:     /// ```\n  1101:     #[stable(feature = \"btree_retain\", since = \"1.53.0\")]\n  1102:     pub fn retain<F>(&mut self, mut f: F)\n  1103:     where\n  1104:         T: Ord,\n  1105:         F: FnMut(&T) -> bool,\n  1106:     {\n  1107:         self.extract_if(.., |v| !f(v)).for_each(drop);\n  1108:     }\n  1109: \n  1110:     /// Moves all elements from `other` into `self`, leaving `other` empty.\n  1111:     ///\n  1112:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::symmetric_difference",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
      "name": "symmetric_difference",
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
            "id": 1996,
            "path": "BTreeSet"
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
                    },
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
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:2109",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1996",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "set",
          "BTreeSet"
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
                "lifetime": "'a",
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
                "is_mutable": false,
                "lifetime": "'a",
                "type": {
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
                    "id": 1996,
                    "path": "BTreeSet"
                  }
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
                    "lifetime": "'a"
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
            "id": 2074,
            "path": "SymmetricDifference"
          }
        }
      }
    },
    "verification_source": "   469:     ///\n   470:     /// ```\n   471:     /// use std::collections::BTreeSet;\n   472:     ///\n   473:     /// let mut a = BTreeSet::new();\n   474:     /// a.insert(1);\n   475:     /// a.insert(2);\n   476:     ///\n   477:     /// let mut b = BTreeSet::new();\n   478:     /// b.insert(2);\n   479:     /// b.insert(3);\n   480:     ///\n   481:     /// let sym_diff: Vec<_> = a.symmetric_difference(&b).cloned().collect();\n   482:     /// assert_eq!(sym_diff, [1, 3]);\n   483:     /// ```\n   484:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   485:     pub fn symmetric_difference<'a>(\n   486:         &'a self,\n   487:         other: &'a BTreeSet<T, A>,\n   488:     ) -> SymmetricDifference<'a, T>\n   489:     where\n   490:         T: Ord,\n   491:     {\n   492:         SymmetricDifference(MergeIterInner::new(self.iter(), other.iter()))\n   493:     }\n   494: \n   495:     /// Visits the elements representing the intersection,\n   496:     /// i.e., the elements that are both in `self` and `other`,\n   497:     /// in ascending order.\n   498:     ///\n   499:     /// # Examples\n   500:     ///\n   501:     /// ```",
    "nanvix_source": "   475:     /// a.insert(2);\n   476:     ///\n   477:     /// let mut b = BTreeSet::new();\n   478:     /// b.insert(2);\n   479:     /// b.insert(3);\n   480:     ///\n   481:     /// let sym_diff: Vec<_> = a.symmetric_difference(&b).cloned().collect();\n   482:     /// assert_eq!(sym_diff, [1, 3]);\n   483:     /// ```\n   484:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   485:     pub fn symmetric_difference<'a>(\n   486:         &'a self,\n   487:         other: &'a BTreeSet<T, A>,\n   488:     ) -> SymmetricDifference<'a, T>\n   489:     where\n   490:         T: Ord,\n   491:     {\n   492:         SymmetricDifference(MergeIterInner::new(self.iter(), other.iter()))\n   493:     }\n   494: \n   495:     /// Visits the elements representing the intersection,",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::union",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
      "name": "union",
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
            "id": 1996,
            "path": "BTreeSet"
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
                    },
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
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:2109",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1996",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "set",
          "BTreeSet"
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
                "lifetime": "'a",
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
                "is_mutable": false,
                "lifetime": "'a",
                "type": {
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
                    "id": 1996,
                    "path": "BTreeSet"
                  }
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
                    "lifetime": "'a"
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
            "id": 2078,
            "path": "Union"
          }
        }
      }
    },
    "verification_source": "   547:     ///\n   548:     /// # Examples\n   549:     ///\n   550:     /// ```\n   551:     /// use std::collections::BTreeSet;\n   552:     ///\n   553:     /// let mut a = BTreeSet::new();\n   554:     /// a.insert(1);\n   555:     ///\n   556:     /// let mut b = BTreeSet::new();\n   557:     /// b.insert(2);\n   558:     ///\n   559:     /// let union: Vec<_> = a.union(&b).cloned().collect();\n   560:     /// assert_eq!(union, [1, 2]);\n   561:     /// ```\n   562:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   563:     pub fn union<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Union<'a, T>\n   564:     where\n   565:         T: Ord,\n   566:     {\n   567:         Union(MergeIterInner::new(self.iter(), other.iter()))\n   568:     }\n   569: \n   570:     /// Clears the set, removing all elements.\n   571:     ///\n   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// use std::collections::BTreeSet;\n   576:     ///\n   577:     /// let mut v = BTreeSet::new();\n   578:     /// v.insert(1);\n   579:     /// v.clear();",
    "nanvix_source": "   553:     /// let mut a = BTreeSet::new();\n   554:     /// a.insert(1);\n   555:     ///\n   556:     /// let mut b = BTreeSet::new();\n   557:     /// b.insert(2);\n   558:     ///\n   559:     /// let union: Vec<_> = a.union(&b).cloned().collect();\n   560:     /// assert_eq!(union, [1, 2]);\n   561:     /// ```\n   562:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   563:     pub fn union<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Union<'a, T>\n   564:     where\n   565:         T: Ord,\n   566:     {\n   567:         Union(MergeIterInner::new(self.iter(), other.iter()))\n   568:     }\n   569: \n   570:     /// Clears the set, removing all elements.\n   571:     ///\n   572:     /// # Examples\n   573:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::drain",
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
            "id": 1016,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "  1480:     /// Basic usage:\n  1481:     ///\n  1482:     /// ```\n  1483:     /// use std::collections::BinaryHeap;\n  1484:     /// let mut heap = BinaryHeap::from([1, 3]);\n  1485:     ///\n  1486:     /// assert!(!heap.is_empty());\n  1487:     ///\n  1488:     /// for x in heap.drain() {\n  1489:     ///     println!(\"{x}\");\n  1490:     /// }\n  1491:     ///\n  1492:     /// assert!(heap.is_empty());\n  1493:     /// ```\n  1494:     #[inline]\n  1495:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1496:     pub fn drain(&mut self) -> Drain<'_, T, A> {\n  1497:         Drain { iter: self.data.drain(..) }\n  1498:     }\n  1499: \n  1500:     /// Drops all items from the binary heap.\n  1501:     ///\n  1502:     /// # Examples\n  1503:     ///\n  1504:     /// Basic usage:\n  1505:     ///\n  1506:     /// ```\n  1507:     /// use std::collections::BinaryHeap;\n  1508:     /// let mut heap = BinaryHeap::from([1, 3]);\n  1509:     ///\n  1510:     /// assert!(!heap.is_empty());\n  1511:     ///\n  1512:     /// heap.clear();",
    "nanvix_source": "  1486:     /// assert!(!heap.is_empty());\n  1487:     ///\n  1488:     /// for x in heap.drain() {\n  1489:     ///     println!(\"{x}\");\n  1490:     /// }\n  1491:     ///\n  1492:     /// assert!(heap.is_empty());\n  1493:     /// ```\n  1494:     #[inline]\n  1495:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  1496:     pub fn drain(&mut self) -> Drain<'_, T, A> {\n  1497:         Drain { iter: self.data.drain(..) }\n  1498:     }\n  1499: \n  1500:     /// Drops all items from the binary heap.\n  1501:     ///\n  1502:     /// # Examples\n  1503:     ///\n  1504:     /// Basic usage:\n  1505:     ///\n  1506:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::iter",
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
            "id": 997,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  1084:     ///\n  1085:     /// # Examples\n  1086:     ///\n  1087:     /// Basic usage:\n  1088:     ///\n  1089:     /// ```\n  1090:     /// use std::collections::BinaryHeap;\n  1091:     /// let heap = BinaryHeap::from([1, 2, 3, 4]);\n  1092:     ///\n  1093:     /// // Print 1, 2, 3, 4 in arbitrary order\n  1094:     /// for x in heap.iter() {\n  1095:     ///     println!(\"{x}\");\n  1096:     /// }\n  1097:     /// ```\n  1098:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1099:     #[cfg_attr(not(test), rustc_diagnostic_item = \"binaryheap_iter\")]\n  1100:     pub fn iter(&self) -> Iter<'_, T> {\n  1101:         Iter { iter: self.data.iter() }\n  1102:     }\n  1103: \n  1104:     /// Returns an iterator which retrieves elements in heap order.\n  1105:     ///\n  1106:     /// This method consumes the original heap.\n  1107:     ///\n  1108:     /// # Examples\n  1109:     ///\n  1110:     /// Basic usage:\n  1111:     ///\n  1112:     /// ```\n  1113:     /// #![feature(binary_heap_into_iter_sorted)]\n  1114:     /// use std::collections::BinaryHeap;\n  1115:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5]);\n  1116:     ///",
    "nanvix_source": "  1090:     /// use std::collections::BinaryHeap;\n  1091:     /// let heap = BinaryHeap::from([1, 2, 3, 4]);\n  1092:     ///\n  1093:     /// // Print 1, 2, 3, 4 in arbitrary order\n  1094:     /// for x in heap.iter() {\n  1095:     ///     println!(\"{x}\");\n  1096:     /// }\n  1097:     /// ```\n  1098:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1099:     #[cfg_attr(not(test), rustc_diagnostic_item = \"binaryheap_iter\")]\n  1100:     pub fn iter(&self) -> Iter<'_, T> {\n  1101:         Iter { iter: self.data.iter() }\n  1102:     }\n  1103: \n  1104:     /// Returns an iterator which retrieves elements in heap order.\n  1105:     ///\n  1106:     /// This method consumes the original heap.\n  1107:     ///\n  1108:     /// # Examples\n  1109:     ///\n  1110:     /// Basic usage:",
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
