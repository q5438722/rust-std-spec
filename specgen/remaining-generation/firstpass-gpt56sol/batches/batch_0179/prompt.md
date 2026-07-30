For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BTreeMap::get_key_value",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Q"
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
                                "generic": "Q"
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
                "generic": "Q"
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
      "name": "get_key_value",
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
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
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
            "id": 1268,
            "path": "BTreeMap"
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
              "name": "V"
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
        "impl_id": "alloc:1419",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1268",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "BTreeMap"
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
            "k",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "generic": "K"
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
    "verification_source": "   767:     ///         self.id.cmp(&other.id)\n   768:     ///     }\n   769:     /// }\n   770:     ///\n   771:     /// let j_a = S { id: 1, name: \"Jessica\" };\n   772:     /// let j_b = S { id: 1, name: \"Jess\" };\n   773:     /// let p = S { id: 2, name: \"Paul\" };\n   774:     /// assert_eq!(j_a, j_b);\n   775:     ///\n   776:     /// let mut map = BTreeMap::new();\n   777:     /// map.insert(j_a, \"Paris\");\n   778:     /// assert_eq!(map.get_key_value(&j_a), Some((&j_a, &\"Paris\")));\n   779:     /// assert_eq!(map.get_key_value(&j_b), Some((&j_a, &\"Paris\"))); // the notable case\n   780:     /// assert_eq!(map.get_key_value(&p), None);\n   781:     /// ```\n   782:     #[stable(feature = \"map_get_key_value\", since = \"1.40.0\")]\n   783:     pub fn get_key_value<Q: ?Sized>(&self, k: &Q) -> Option<(&K, &V)>\n   784:     where\n   785:         K: Borrow<Q> + Ord,\n   786:         Q: Ord,\n   787:     {\n   788:         let root_node = self.root.as_ref()?.reborrow();\n   789:         match root_node.search_tree(k) {\n   790:             Found(handle) => Some(handle.into_kv()),\n   791:             GoDown(_) => None,\n   792:         }\n   793:     }\n   794: \n   795:     /// Returns the first key-value pair in the map.\n   796:     /// The key in this pair is the minimum key in the map.\n   797:     ///\n   798:     /// # Examples\n   799:     ///",
    "nanvix_source": "   773:     /// let p = S { id: 2, name: \"Paul\" };\n   774:     /// assert_eq!(j_a, j_b);\n   775:     ///\n   776:     /// let mut map = BTreeMap::new();\n   777:     /// map.insert(j_a, \"Paris\");\n   778:     /// assert_eq!(map.get_key_value(&j_a), Some((&j_a, &\"Paris\")));\n   779:     /// assert_eq!(map.get_key_value(&j_b), Some((&j_a, &\"Paris\"))); // the notable case\n   780:     /// assert_eq!(map.get_key_value(&p), None);\n   781:     /// ```\n   782:     #[stable(feature = \"map_get_key_value\", since = \"1.40.0\")]\n   783:     pub fn get_key_value<Q: ?Sized>(&self, k: &Q) -> Option<(&K, &V)>\n   784:     where\n   785:         K: Borrow<Q> + Ord,\n   786:         Q: Ord,\n   787:     {\n   788:         let root_node = self.root.as_ref()?.reborrow();\n   789:         match root_node.search_tree(k) {\n   790:             Found(handle) => Some(handle.into_kv()),\n   791:             GoDown(_) => None,\n   792:         }\n   793:     }",
    "previous_skip_rationale": "For generic Borrow<Q>, existing vstd borrowed-key relations are opaque and provide neither a cross-type ordering compatibility law nor a functional map/query-to-stored-key relation. Therefore the observable returned key-value pair cannot be determined without an unjustified precondition or ad hoc choice."
  },
  {
    "target": "alloc::collections::BTreeMap::split_off",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
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
                        "id": 29,
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
            "name": "Q"
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
                                "generic": "Q"
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
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
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
            "id": 1268,
            "path": "BTreeMap"
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
              "name": "V"
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
        "impl_id": "alloc:1419",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1268",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "BTreeMap"
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
            "key",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1524:     /// a.insert(17, \"d\");\n  1525:     /// a.insert(41, \"e\");\n  1526:     ///\n  1527:     /// let b = a.split_off(&3);\n  1528:     ///\n  1529:     /// assert_eq!(a.len(), 2);\n  1530:     /// assert_eq!(b.len(), 3);\n  1531:     ///\n  1532:     /// assert_eq!(a[&1], \"a\");\n  1533:     /// assert_eq!(a[&2], \"b\");\n  1534:     ///\n  1535:     /// assert_eq!(b[&3], \"c\");\n  1536:     /// assert_eq!(b[&17], \"d\");\n  1537:     /// assert_eq!(b[&41], \"e\");\n  1538:     /// ```\n  1539:     #[stable(feature = \"btree_split_off\", since = \"1.11.0\")]\n  1540:     pub fn split_off<Q: ?Sized + Ord>(&mut self, key: &Q) -> Self\n  1541:     where\n  1542:         K: Borrow<Q> + Ord,\n  1543:         A: Clone,\n  1544:     {\n  1545:         if self.is_empty() {\n  1546:             return Self::new_in((*self.alloc).clone());\n  1547:         }\n  1548: \n  1549:         let total_num = self.len();\n  1550:         let left_root = self.root.as_mut().unwrap(); // unwrap succeeds because not empty\n  1551: \n  1552:         let right_root = left_root.split_off(key, (*self.alloc).clone());\n  1553: \n  1554:         let (new_left_len, right_len) = Root::calc_split_length(total_num, &left_root, &right_root);\n  1555:         self.length = new_left_len;\n  1556: ",
    "nanvix_source": "  1551:     /// assert_eq!(b.len(), 3);\n  1552:     ///\n  1553:     /// assert_eq!(a[&1], \"a\");\n  1554:     /// assert_eq!(a[&2], \"b\");\n  1555:     ///\n  1556:     /// assert_eq!(b[&3], \"c\");\n  1557:     /// assert_eq!(b[&17], \"d\");\n  1558:     /// assert_eq!(b[&41], \"e\");\n  1559:     /// ```\n  1560:     #[stable(feature = \"btree_split_off\", since = \"1.11.0\")]\n  1561:     pub fn split_off<Q: ?Sized + Ord>(&mut self, key: &Q) -> Self\n  1562:     where\n  1563:         K: Borrow<Q> + Ord,\n  1564:         A: Clone,\n  1565:     {\n  1566:         if self.is_empty() {\n  1567:             return Self::new_in((*self.alloc).clone());\n  1568:         }\n  1569: \n  1570:         let total_num = self.len();\n  1571:         let left_root = self.root.as_mut().unwrap(); // unwrap succeeds because not empty",
    "previous_skip_rationale": "The split boundary depends on ordering the borrowed Q key against stored keys. Existing vstd vocabulary models only borrowed-key containment, not Borrow::borrow or cross-type ordering. Consequently, the structural partition clauses admit multiple prefix/suffix splits, especially when the queried key is absent."
  },
  {
    "target": "alloc::collections::BTreeSet::split_off",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
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
                        "id": 29,
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
            "name": "Q"
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
                                "generic": "Q"
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
            "value",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1161:     /// a.insert(17);\n  1162:     /// a.insert(41);\n  1163:     ///\n  1164:     /// let b = a.split_off(&3);\n  1165:     ///\n  1166:     /// assert_eq!(a.len(), 2);\n  1167:     /// assert_eq!(b.len(), 3);\n  1168:     ///\n  1169:     /// assert!(a.contains(&1));\n  1170:     /// assert!(a.contains(&2));\n  1171:     ///\n  1172:     /// assert!(b.contains(&3));\n  1173:     /// assert!(b.contains(&17));\n  1174:     /// assert!(b.contains(&41));\n  1175:     /// ```\n  1176:     #[stable(feature = \"btree_split_off\", since = \"1.11.0\")]\n  1177:     pub fn split_off<Q: ?Sized + Ord>(&mut self, value: &Q) -> Self\n  1178:     where\n  1179:         T: Borrow<Q> + Ord,\n  1180:         A: Clone,\n  1181:     {\n  1182:         BTreeSet { map: self.map.split_off(value) }\n  1183:     }\n  1184: \n  1185:     /// Creates an iterator that visits elements in the specified range in ascending order and\n  1186:     /// uses a closure to determine if an element should be removed.\n  1187:     ///\n  1188:     /// If the closure returns `true`, the element is removed from the set and\n  1189:     /// yielded. If the closure returns `false`, or panics, the element remains\n  1190:     /// in the set and will not be yielded.\n  1191:     ///\n  1192:     /// If the returned `ExtractIf` is not exhausted, e.g. because it is dropped without iterating\n  1193:     /// or the iteration short-circuits, then the remaining elements will be retained.",
    "nanvix_source": "  1167:     /// assert_eq!(b.len(), 3);\n  1168:     ///\n  1169:     /// assert!(a.contains(&1));\n  1170:     /// assert!(a.contains(&2));\n  1171:     ///\n  1172:     /// assert!(b.contains(&3));\n  1173:     /// assert!(b.contains(&17));\n  1174:     /// assert!(b.contains(&41));\n  1175:     /// ```\n  1176:     #[stable(feature = \"btree_split_off\", since = \"1.11.0\")]\n  1177:     pub fn split_off<Q: ?Sized + Ord>(&mut self, value: &Q) -> Self\n  1178:     where\n  1179:         T: Borrow<Q> + Ord,\n  1180:         A: Clone,\n  1181:     {\n  1182:         BTreeSet { map: self.map.split_off(value) }\n  1183:     }\n  1184: \n  1185:     /// Creates an iterator that visits elements in the specified range in ascending order and\n  1186:     /// uses a closure to determine if an element should be removed.\n  1187:     ///",
    "previous_skip_rationale": "The split boundary depends on ordering the borrowed Q value against stored keys. Existing vstd vocabulary models borrowed-key containment, but not Borrow::borrow or cross-type ordering. The proposed structural clauses therefore admit multiple prefix/suffix partitions when the queried value is absent."
  },
  {
    "target": "alloc::string::String::replace_range",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
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
      "name": "replace_range",
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
            "range",
            {
              "generic": "R"
            }
          ],
          [
            "replace_with",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2059:     /// Panics if the range has `start_bound > end_bound`, or, if the range is\n  2060:     /// bounded on either end and does not lie on a [`char`] boundary.\n  2061:     ///\n  2062:     /// # Examples\n  2063:     ///\n  2064:     /// ```\n  2065:     /// let mut s = String::from(\"\u03b1 is alpha, \u03b2 is beta\");\n  2066:     /// let beta_offset = s.find('\u03b2').unwrap_or(s.len());\n  2067:     ///\n  2068:     /// // Replace the range up until the \u03b2 from the string\n  2069:     /// s.replace_range(..beta_offset, \"\u0391 is capital alpha; \");\n  2070:     /// assert_eq!(s, \"\u0391 is capital alpha; \u03b2 is beta\");\n  2071:     /// ```\n  2072:     #[cfg(not(no_global_oom_handling))]\n  2073:     #[stable(feature = \"splice\", since = \"1.27.0\")]\n  2074:     #[track_caller]\n  2075:     pub fn replace_range<R>(&mut self, range: R, replace_with: &str)\n  2076:     where\n  2077:         R: RangeBounds<usize>,\n  2078:     {\n  2079:         // We avoid #81138 (nondeterministic RangeBounds impls) because we only use `range` once, here.\n  2080:         let checked_range = slice::range(range, ..self.len());\n  2081: \n  2082:         assert!(\n  2083:             self.is_char_boundary(checked_range.start),\n  2084:             \"start of range should be a character boundary\"\n  2085:         );\n  2086:         assert!(\n  2087:             self.is_char_boundary(checked_range.end),\n  2088:             \"end of range should be a character boundary\"\n  2089:         );\n  2090: \n  2091:         unsafe { self.as_mut_vec() }.splice(checked_range, replace_with.bytes());",
    "nanvix_source": "  2070:     /// let mut s = String::from(\"\u03b1 is alpha, \u03b2 is beta\");\n  2071:     /// let beta_offset = s.find('\u03b2').unwrap_or(s.len());\n  2072:     ///\n  2073:     /// // Replace the range up until the \u03b2 from the string\n  2074:     /// s.replace_range(..beta_offset, \"\u0391 is capital alpha; \");\n  2075:     /// assert_eq!(s, \"\u0391 is capital alpha; \u03b2 is beta\");\n  2076:     /// ```\n  2077:     #[cfg(not(no_global_oom_handling))]\n  2078:     #[stable(feature = \"splice\", since = \"1.27.0\")]\n  2079:     #[track_caller]\n  2080:     pub fn replace_range<R>(&mut self, range: R, replace_with: &str)\n  2081:     where\n  2082:         R: RangeBounds<usize>,\n  2083:     {\n  2084:         // We avoid #81138 (nondeterministic RangeBounds impls) because we only use `range` once, here.\n  2085:         let checked_range = slice::range(range, ..self.len());\n  2086: \n  2087:         assert!(\n  2088:             self.is_char_boundary(checked_range.start),\n  2089:             \"start of range should be a character boundary\"\n  2090:         );",
    "previous_skip_rationale": "The generic RangeBounds implementation may be stateful or nondeterministic; the source only queries it once. No existing law connects those observed bounds to a stable Verus model, so a post-state relation or no-panic precondition would be an unjustified trusted assumption."
  },
  {
    "target": "alloc::vec::Vec::extend_from_within",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
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
      "name": "extend_from_within",
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
            "id": 114,
            "path": "Vec"
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
        "impl_id": "alloc:4949",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "src",
            {
              "generic": "R"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3540:     ///\n  3541:     /// ```\n  3542:     /// let mut characters = vec!['a', 'b', 'c', 'd', 'e'];\n  3543:     /// characters.extend_from_within(2..);\n  3544:     /// assert_eq!(characters, ['a', 'b', 'c', 'd', 'e', 'c', 'd', 'e']);\n  3545:     ///\n  3546:     /// let mut numbers = vec![0, 1, 2, 3, 4];\n  3547:     /// numbers.extend_from_within(..2);\n  3548:     /// assert_eq!(numbers, [0, 1, 2, 3, 4, 0, 1]);\n  3549:     ///\n  3550:     /// let mut strings = vec![String::from(\"hello\"), String::from(\"world\"), String::from(\"!\")];\n  3551:     /// strings.extend_from_within(1..=2);\n  3552:     /// assert_eq!(strings, [\"hello\", \"world\", \"!\", \"world\", \"!\"]);\n  3553:     /// ```\n  3554:     #[cfg(not(no_global_oom_handling))]\n  3555:     #[stable(feature = \"vec_extend_from_within\", since = \"1.53.0\")]\n  3556:     pub fn extend_from_within<R>(&mut self, src: R)\n  3557:     where\n  3558:         R: RangeBounds<usize>,\n  3559:     {\n  3560:         let range = slice::range(src, ..self.len());\n  3561:         self.reserve(range.len());\n  3562: \n  3563:         // SAFETY:\n  3564:         // - `slice::range` guarantees that the given range is valid for indexing self\n  3565:         unsafe {\n  3566:             self.spec_extend_from_within(range);\n  3567:         }\n  3568:     }\n  3569: }\n  3570: \n  3571: impl<T, A: Allocator, const N: usize> Vec<[T; N], A> {\n  3572:     /// Takes a `Vec<[T; N]>` and flattens it into a `Vec<T>`.",
    "nanvix_source": "  3587:     /// let mut numbers = vec![0, 1, 2, 3, 4];\n  3588:     /// numbers.extend_from_within(..2);\n  3589:     /// assert_eq!(numbers, [0, 1, 2, 3, 4, 0, 1]);\n  3590:     ///\n  3591:     /// let mut strings = vec![String::from(\"hello\"), String::from(\"world\"), String::from(\"!\")];\n  3592:     /// strings.extend_from_within(1..=2);\n  3593:     /// assert_eq!(strings, [\"hello\", \"world\", \"!\", \"world\", \"!\"]);\n  3594:     /// ```\n  3595:     #[cfg(not(no_global_oom_handling))]\n  3596:     #[stable(feature = \"vec_extend_from_within\", since = \"1.53.0\")]\n  3597:     pub fn extend_from_within<R>(&mut self, src: R)\n  3598:     where\n  3599:         R: RangeBounds<usize>,\n  3600:     {\n  3601:         let range = slice::range(src, ..self.len());\n  3602:         self.reserve(range.len());\n  3603: \n  3604:         // SAFETY:\n  3605:         // - `slice::range` guarantees that the given range is valid for indexing self\n  3606:         unsafe {\n  3607:             self.spec_extend_from_within(range);",
    "previous_skip_rationale": "For arbitrary T: Clone, the source justifies only that appended elements satisfy vstd's relational cloned predicate. That predicate does not uniquely determine Vec@, while equating clones with their sources or requiring clone uniqueness would impose an unsupported domain restriction."
  },
  {
    "target": "core::mem::discriminant",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "free_function"
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
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "discriminant",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "v",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9396,
            "path": "Discriminant"
          }
        }
      }
    },
    "verification_source": "  1215: /// }\n  1216: ///\n  1217: /// let unit_like = Enum::Unit;\n  1218: /// let tuple_like = Enum::Tuple(true);\n  1219: /// let struct_like = Enum::Struct { a: false };\n  1220: /// assert_eq!(0, unit_like.discriminant());\n  1221: /// assert_eq!(1, tuple_like.discriminant());\n  1222: /// assert_eq!(2, struct_like.discriminant());\n  1223: ///\n  1224: /// // \u26a0\ufe0f This is undefined behavior. Don't do this. \u26a0\ufe0f\n  1225: /// // assert_eq!(0, unsafe { std::mem::transmute::<_, u8>(std::mem::discriminant(&unit_like)) });\n  1226: /// ```\n  1227: #[stable(feature = \"discriminant_value\", since = \"1.21.0\")]\n  1228: #[rustc_const_stable(feature = \"const_discriminant\", since = \"1.75.0\")]\n  1229: #[rustc_diagnostic_item = \"mem_discriminant\"]\n  1230: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1231: pub const fn discriminant<T>(v: &T) -> Discriminant<T> {\n  1232:     Discriminant(intrinsics::discriminant_value(v))\n  1233: }\n  1234: \n  1235: /// Returns the number of variants in the enum type `T`.\n  1236: ///\n  1237: /// If `T` is not an enum, calling this function will not result in undefined behavior, but the\n  1238: /// return value is unspecified. Equally, if `T` is an enum with more variants than `usize::MAX`\n  1239: /// the return value is unspecified. Uninhabited variants will be counted.\n  1240: ///\n  1241: /// Note that an enum may be expanded with additional variants in the future\n  1242: /// as a non-breaking change, for example if it is marked `#[non_exhaustive]`,\n  1243: /// which will change the result of this function.\n  1244: ///\n  1245: /// # Examples\n  1246: ///\n  1247: /// ```",
    "nanvix_source": "  1394: /// assert_eq!(1, tuple_like.discriminant());\n  1395: /// assert_eq!(2, struct_like.discriminant());\n  1396: ///\n  1397: /// // \u26a0\ufe0f This is undefined behavior. Don't do this. \u26a0\ufe0f\n  1398: /// // assert_eq!(0, unsafe { std::mem::transmute::<_, u8>(std::mem::discriminant(&unit_like)) });\n  1399: /// ```\n  1400: #[stable(feature = \"discriminant_value\", since = \"1.21.0\")]\n  1401: #[rustc_const_stable(feature = \"const_discriminant\", since = \"1.75.0\")]\n  1402: #[rustc_diagnostic_item = \"mem_discriminant\"]\n  1403: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1404: pub const fn discriminant<T>(v: &T) -> Discriminant<T> {\n  1405:     Discriminant(intrinsics::discriminant_value(v))\n  1406: }\n  1407: \n  1408: /// Returns the number of variants in the enum type `T`.\n  1409: ///\n  1410: /// If `T` is not an enum, calling this function will not result in undefined behavior, but the\n  1411: /// return value is unspecified. Equally, if `T` is an enum with more variants than `usize::MAX`\n  1412: /// the return value is unspecified. Uninhabited variants will be counted.\n  1413: ///\n  1414: /// Note that an enum may be expanded with additional variants in the future",
    "previous_skip_rationale": "Discriminant<T> is opaque, and public vstd has no generic active-variant model for T. A no_unwind-only contract would not usefully relate the result to v; doing so otherwise requires an unjustified model or private representation access."
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
