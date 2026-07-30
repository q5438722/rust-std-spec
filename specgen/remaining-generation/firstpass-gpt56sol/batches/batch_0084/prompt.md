For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BTreeMap::range_mut",
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
            "name": "T"
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
                                "generic": "T"
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
                      "generic": "K"
                    }
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
            "id": 1411,
            "path": "RangeMut"
          }
        }
      }
    },
    "verification_source": "  1432:     ///\n  1433:     /// # Examples\n  1434:     ///\n  1435:     /// ```\n  1436:     /// use std::collections::BTreeMap;\n  1437:     ///\n  1438:     /// let mut map: BTreeMap<&str, i32> =\n  1439:     ///     [(\"Alice\", 0), (\"Bob\", 0), (\"Carol\", 0), (\"Cheryl\", 0)].into();\n  1440:     /// for (_, balance) in map.range_mut(\"B\"..\"Cheryl\") {\n  1441:     ///     *balance += 100;\n  1442:     /// }\n  1443:     /// for (name, balance) in &map {\n  1444:     ///     println!(\"{name} => {balance}\");\n  1445:     /// }\n  1446:     /// ```\n  1447:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n  1448:     pub fn range_mut<T: ?Sized, R>(&mut self, range: R) -> RangeMut<'_, K, V>\n  1449:     where\n  1450:         T: Ord,\n  1451:         K: Borrow<T> + Ord,\n  1452:         R: RangeBounds<T>,\n  1453:     {\n  1454:         if let Some(root) = &mut self.root {\n  1455:             RangeMut { inner: root.borrow_valmut().range_search(range), _marker: PhantomData }\n  1456:         } else {\n  1457:             RangeMut { inner: LeafRange::none(), _marker: PhantomData }\n  1458:         }\n  1459:     }\n  1460: \n  1461:     /// Gets the given key's corresponding entry in the map for in-place manipulation.\n  1462:     ///\n  1463:     /// # Examples\n  1464:     ///",
    "nanvix_source": "  1459:     /// let mut map: BTreeMap<&str, i32> =\n  1460:     ///     [(\"Alice\", 0), (\"Bob\", 0), (\"Carol\", 0), (\"Cheryl\", 0)].into();\n  1461:     /// for (_, balance) in map.range_mut(\"B\"..\"Cheryl\") {\n  1462:     ///     *balance += 100;\n  1463:     /// }\n  1464:     /// for (name, balance) in &map {\n  1465:     ///     println!(\"{name} => {balance}\");\n  1466:     /// }\n  1467:     /// ```\n  1468:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n  1469:     pub fn range_mut<T: ?Sized, R>(&mut self, range: R) -> RangeMut<'_, K, V>\n  1470:     where\n  1471:         T: Ord,\n  1472:         K: Borrow<T> + Ord,\n  1473:         R: RangeBounds<T>,\n  1474:     {\n  1475:         if let Some(root) = &mut self.root {\n  1476:             RangeMut { inner: root.borrow_valmut().range_search(range), _marker: PhantomData }\n  1477:         } else {\n  1478:             RangeMut { inner: LeafRange::none(), _marker: PhantomData }\n  1479:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::retain",
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
                        "parenthesized": {
                          "inputs": [
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "V"
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
    "verification_source": "  1155:     ///\n  1156:     /// In other words, remove all pairs `(k, v)` for which `f(&k, &mut v)` returns `false`.\n  1157:     /// The elements are visited in ascending key order.\n  1158:     ///\n  1159:     /// # Examples\n  1160:     ///\n  1161:     /// ```\n  1162:     /// use std::collections::BTreeMap;\n  1163:     ///\n  1164:     /// let mut map: BTreeMap<i32, i32> = (0..8).map(|x| (x, x*10)).collect();\n  1165:     /// // Keep only the elements with even-numbered keys.\n  1166:     /// map.retain(|&k, _| k % 2 == 0);\n  1167:     /// assert!(map.into_iter().eq(vec![(0, 0), (2, 20), (4, 40), (6, 60)]));\n  1168:     /// ```\n  1169:     #[inline]\n  1170:     #[stable(feature = \"btree_retain\", since = \"1.53.0\")]\n  1171:     pub fn retain<F>(&mut self, mut f: F)\n  1172:     where\n  1173:         K: Ord,\n  1174:         F: FnMut(&K, &mut V) -> bool,\n  1175:     {\n  1176:         self.extract_if(.., |k, v| !f(k, v)).for_each(drop);\n  1177:     }\n  1178: \n  1179:     /// Moves all elements from `other` into `self`, leaving `other` empty.\n  1180:     ///\n  1181:     /// If a key from `other` is already present in `self`, the respective\n  1182:     /// value from `self` will be overwritten with the respective value from `other`.\n  1183:     /// Similar to [`insert`], though, the key is not overwritten,\n  1184:     /// which matters for types that can be `==` without being identical.\n  1185:     ///\n  1186:     /// [`insert`]: BTreeMap::insert\n  1187:     ///",
    "nanvix_source": "  1182:     /// ```\n  1183:     /// use std::collections::BTreeMap;\n  1184:     ///\n  1185:     /// let mut map: BTreeMap<i32, i32> = (0..8).map(|x| (x, x*10)).collect();\n  1186:     /// // Keep only the elements with even-numbered keys.\n  1187:     /// map.retain(|&k, _| k % 2 == 0);\n  1188:     /// assert!(map.into_iter().eq(vec![(0, 0), (2, 20), (4, 40), (6, 60)]));\n  1189:     /// ```\n  1190:     #[inline]\n  1191:     #[stable(feature = \"btree_retain\", since = \"1.53.0\")]\n  1192:     pub fn retain<F>(&mut self, mut f: F)\n  1193:     where\n  1194:         K: Ord,\n  1195:         F: FnMut(&K, &mut V) -> bool,\n  1196:     {\n  1197:         self.extract_if(.., |k, v| !f(k, v)).for_each(drop);\n  1198:     }\n  1199: \n  1200:     /// Moves all elements from `other` into `self`, leaving `other` empty.\n  1201:     ///\n  1202:     /// If a key from `other` is already present in `self`, the respective",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::values_mut",
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
      "name": "values_mut",
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
        "impl_id": "alloc:1436",
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
                      "generic": "K"
                    }
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
            "id": 1426,
            "path": "ValuesMut"
          }
        }
      }
    },
    "verification_source": "  2764:     /// ```\n  2765:     /// use std::collections::BTreeMap;\n  2766:     ///\n  2767:     /// let mut a = BTreeMap::new();\n  2768:     /// a.insert(1, String::from(\"hello\"));\n  2769:     /// a.insert(2, String::from(\"goodbye\"));\n  2770:     ///\n  2771:     /// for value in a.values_mut() {\n  2772:     ///     value.push_str(\"!\");\n  2773:     /// }\n  2774:     ///\n  2775:     /// let values: Vec<String> = a.values().cloned().collect();\n  2776:     /// assert_eq!(values, [String::from(\"hello!\"),\n  2777:     ///                     String::from(\"goodbye!\")]);\n  2778:     /// ```\n  2779:     #[stable(feature = \"map_values_mut\", since = \"1.10.0\")]\n  2780:     pub fn values_mut(&mut self) -> ValuesMut<'_, K, V> {\n  2781:         ValuesMut { inner: self.iter_mut() }\n  2782:     }\n  2783: \n  2784:     /// Returns the number of elements in the map.\n  2785:     ///\n  2786:     /// # Examples\n  2787:     ///\n  2788:     /// ```\n  2789:     /// use std::collections::BTreeMap;\n  2790:     ///\n  2791:     /// let mut a = BTreeMap::new();\n  2792:     /// assert_eq!(a.len(), 0);\n  2793:     /// a.insert(1, \"a\");\n  2794:     /// assert_eq!(a.len(), 1);\n  2795:     /// ```\n  2796:     #[must_use]",
    "nanvix_source": "  2792:     ///\n  2793:     /// for value in a.values_mut() {\n  2794:     ///     value.push_str(\"!\");\n  2795:     /// }\n  2796:     ///\n  2797:     /// let values: Vec<String> = a.values().cloned().collect();\n  2798:     /// assert_eq!(values, [String::from(\"hello!\"),\n  2799:     ///                     String::from(\"goodbye!\")]);\n  2800:     /// ```\n  2801:     #[stable(feature = \"map_values_mut\", since = \"1.10.0\")]\n  2802:     pub fn values_mut(&mut self) -> ValuesMut<'_, K, V> {\n  2803:         ValuesMut { inner: self.iter_mut() }\n  2804:     }\n  2805: \n  2806:     /// Returns the number of elements in the map.\n  2807:     ///\n  2808:     /// # Examples\n  2809:     ///\n  2810:     /// ```\n  2811:     /// use std::collections::BTreeMap;\n  2812:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::difference",
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
      "name": "difference",
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
            "id": 2072,
            "path": "Difference"
          }
        }
      }
    },
    "verification_source": "   412:     ///\n   413:     /// ```\n   414:     /// use std::collections::BTreeSet;\n   415:     ///\n   416:     /// let mut a = BTreeSet::new();\n   417:     /// a.insert(1);\n   418:     /// a.insert(2);\n   419:     ///\n   420:     /// let mut b = BTreeSet::new();\n   421:     /// b.insert(2);\n   422:     /// b.insert(3);\n   423:     ///\n   424:     /// let diff: Vec<_> = a.difference(&b).cloned().collect();\n   425:     /// assert_eq!(diff, [1]);\n   426:     /// ```\n   427:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   428:     pub fn difference<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Difference<'a, T, A>\n   429:     where\n   430:         T: Ord,\n   431:     {\n   432:         if let Some(self_min) = self.first()\n   433:             && let Some(self_max) = self.last()\n   434:             && let Some(other_min) = other.first()\n   435:             && let Some(other_max) = other.last()\n   436:         {\n   437:             Difference {\n   438:                 inner: match (self_min.cmp(other_max), self_max.cmp(other_min)) {\n   439:                     (Greater, _) | (_, Less) => DifferenceInner::Iterate(self.iter()),\n   440:                     (Equal, _) => {\n   441:                         let mut self_iter = self.iter();\n   442:                         self_iter.next();\n   443:                         DifferenceInner::Iterate(self_iter)\n   444:                     }",
    "nanvix_source": "   418:     /// a.insert(2);\n   419:     ///\n   420:     /// let mut b = BTreeSet::new();\n   421:     /// b.insert(2);\n   422:     /// b.insert(3);\n   423:     ///\n   424:     /// let diff: Vec<_> = a.difference(&b).cloned().collect();\n   425:     /// assert_eq!(diff, [1]);\n   426:     /// ```\n   427:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   428:     pub fn difference<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Difference<'a, T, A>\n   429:     where\n   430:         T: Ord,\n   431:     {\n   432:         if let Some(self_min) = self.first()\n   433:             && let Some(self_max) = self.last()\n   434:             && let Some(other_min) = other.first()\n   435:             && let Some(other_max) = other.last()\n   436:         {\n   437:             Difference {\n   438:                 inner: match (self_min.cmp(other_max), self_max.cmp(other_min)) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::extract_if",
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
                                "generic": "T"
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
            "range",
            {
              "generic": "R"
            }
          ],
          [
            "pred",
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
                      "generic": "R"
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
            "id": 2099,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "  1202:     ///\n  1203:     /// // Splitting a set into even and odd values, reusing the original set:\n  1204:     /// let mut set: BTreeSet<i32> = (0..8).collect();\n  1205:     /// let evens: BTreeSet<_> = set.extract_if(.., |v| v % 2 == 0).collect();\n  1206:     /// let odds = set;\n  1207:     /// assert_eq!(evens.into_iter().collect::<Vec<_>>(), vec![0, 2, 4, 6]);\n  1208:     /// assert_eq!(odds.into_iter().collect::<Vec<_>>(), vec![1, 3, 5, 7]);\n  1209:     ///\n  1210:     /// // Splitting a set into low and high halves, reusing the original set:\n  1211:     /// let mut set: BTreeSet<i32> = (0..8).collect();\n  1212:     /// let low: BTreeSet<_> = set.extract_if(0..4, |_v| true).collect();\n  1213:     /// let high = set;\n  1214:     /// assert_eq!(low.into_iter().collect::<Vec<_>>(), [0, 1, 2, 3]);\n  1215:     /// assert_eq!(high.into_iter().collect::<Vec<_>>(), [4, 5, 6, 7]);\n  1216:     /// ```\n  1217:     #[stable(feature = \"btree_extract_if\", since = \"1.91.0\")]\n  1218:     pub fn extract_if<F, R>(&mut self, range: R, pred: F) -> ExtractIf<'_, T, R, F, A>\n  1219:     where\n  1220:         T: Ord,\n  1221:         R: RangeBounds<T>,\n  1222:         F: FnMut(&T) -> bool,\n  1223:     {\n  1224:         let (inner, alloc) = self.map.extract_if_inner(range);\n  1225:         ExtractIf { pred, inner, alloc }\n  1226:     }\n  1227: \n  1228:     /// Gets an iterator that visits the elements in the `BTreeSet` in ascending\n  1229:     /// order.\n  1230:     ///\n  1231:     /// # Examples\n  1232:     ///\n  1233:     /// ```\n  1234:     /// use std::collections::BTreeSet;",
    "nanvix_source": "  1208:     /// assert_eq!(odds.into_iter().collect::<Vec<_>>(), vec![1, 3, 5, 7]);\n  1209:     ///\n  1210:     /// // Splitting a set into low and high halves, reusing the original set:\n  1211:     /// let mut set: BTreeSet<i32> = (0..8).collect();\n  1212:     /// let low: BTreeSet<_> = set.extract_if(0..4, |_v| true).collect();\n  1213:     /// let high = set;\n  1214:     /// assert_eq!(low.into_iter().collect::<Vec<_>>(), [0, 1, 2, 3]);\n  1215:     /// assert_eq!(high.into_iter().collect::<Vec<_>>(), [4, 5, 6, 7]);\n  1216:     /// ```\n  1217:     #[stable(feature = \"btree_extract_if\", since = \"1.91.0\")]\n  1218:     pub fn extract_if<F, R>(&mut self, range: R, pred: F) -> ExtractIf<'_, T, R, F, A>\n  1219:     where\n  1220:         T: Ord,\n  1221:         R: RangeBounds<T>,\n  1222:         F: FnMut(&T) -> bool,\n  1223:     {\n  1224:         let (inner, alloc) = self.map.extract_if_inner(range);\n  1225:         ExtractIf { pred, inner, alloc }\n  1226:     }\n  1227: \n  1228:     /// Gets an iterator that visits the elements in the `BTreeSet` in ascending",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeSet::intersection",
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
      "name": "intersection",
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
            "id": 2076,
            "path": "Intersection"
          }
        }
      }
    },
    "verification_source": "   500:     ///\n   501:     /// ```\n   502:     /// use std::collections::BTreeSet;\n   503:     ///\n   504:     /// let mut a = BTreeSet::new();\n   505:     /// a.insert(1);\n   506:     /// a.insert(2);\n   507:     ///\n   508:     /// let mut b = BTreeSet::new();\n   509:     /// b.insert(2);\n   510:     /// b.insert(3);\n   511:     ///\n   512:     /// let intersection: Vec<_> = a.intersection(&b).cloned().collect();\n   513:     /// assert_eq!(intersection, [2]);\n   514:     /// ```\n   515:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   516:     pub fn intersection<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Intersection<'a, T, A>\n   517:     where\n   518:         T: Ord,\n   519:     {\n   520:         if let Some(self_min) = self.first()\n   521:             && let Some(self_max) = self.last()\n   522:             && let Some(other_min) = other.first()\n   523:             && let Some(other_max) = other.last()\n   524:         {\n   525:             Intersection {\n   526:                 inner: match (self_min.cmp(other_max), self_max.cmp(other_min)) {\n   527:                     (Greater, _) | (_, Less) => IntersectionInner::Answer(None),\n   528:                     (Equal, _) => IntersectionInner::Answer(Some(self_min)),\n   529:                     (_, Equal) => IntersectionInner::Answer(Some(self_max)),\n   530:                     _ if self.len() <= other.len() / ITER_PERFORMANCE_TIPPING_SIZE_DIFF => {\n   531:                         IntersectionInner::Search { small_iter: self.iter(), large_set: other }\n   532:                     }",
    "nanvix_source": "   506:     /// a.insert(2);\n   507:     ///\n   508:     /// let mut b = BTreeSet::new();\n   509:     /// b.insert(2);\n   510:     /// b.insert(3);\n   511:     ///\n   512:     /// let intersection: Vec<_> = a.intersection(&b).cloned().collect();\n   513:     /// assert_eq!(intersection, [2]);\n   514:     /// ```\n   515:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   516:     pub fn intersection<'a>(&'a self, other: &'a BTreeSet<T, A>) -> Intersection<'a, T, A>\n   517:     where\n   518:         T: Ord,\n   519:     {\n   520:         if let Some(self_min) = self.first()\n   521:             && let Some(self_max) = self.last()\n   522:             && let Some(other_min) = other.first()\n   523:             && let Some(other_max) = other.last()\n   524:         {\n   525:             Intersection {\n   526:                 inner: match (self_min.cmp(other_max), self_max.cmp(other_min)) {",
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
