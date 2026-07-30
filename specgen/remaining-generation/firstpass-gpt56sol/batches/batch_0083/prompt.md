For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BTreeMap::entry",
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "entry",
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
              "generic": "K"
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
            "id": 1269,
            "path": "Entry"
          }
        }
      }
    },
    "verification_source": "  1464:     ///\n  1465:     /// ```\n  1466:     /// use std::collections::BTreeMap;\n  1467:     ///\n  1468:     /// let mut count: BTreeMap<&str, usize> = BTreeMap::new();\n  1469:     ///\n  1470:     /// // count the number of occurrences of letters in the vec\n  1471:     /// for x in [\"a\", \"b\", \"a\", \"c\", \"a\", \"b\"] {\n  1472:     ///     count.entry(x).and_modify(|curr| *curr += 1).or_insert(1);\n  1473:     /// }\n  1474:     ///\n  1475:     /// assert_eq!(count[\"a\"], 3);\n  1476:     /// assert_eq!(count[\"b\"], 2);\n  1477:     /// assert_eq!(count[\"c\"], 1);\n  1478:     /// ```\n  1479:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1480:     pub fn entry(&mut self, key: K) -> Entry<'_, K, V, A>\n  1481:     where\n  1482:         K: Ord,\n  1483:     {\n  1484:         let (map, dormant_map) = DormantMutRef::new(self);\n  1485:         match map.root {\n  1486:             None => Vacant(VacantEntry {\n  1487:                 key,\n  1488:                 handle: None,\n  1489:                 dormant_map,\n  1490:                 alloc: (*map.alloc).clone(),\n  1491:                 _marker: PhantomData,\n  1492:             }),\n  1493:             Some(ref mut root) => match root.borrow_mut().search_tree(&key) {\n  1494:                 Found(handle) => Occupied(OccupiedEntry {\n  1495:                     handle,\n  1496:                     dormant_map,",
    "nanvix_source": "  1491:     /// // count the number of occurrences of letters in the vec\n  1492:     /// for x in [\"a\", \"b\", \"a\", \"c\", \"a\", \"b\"] {\n  1493:     ///     count.entry(x).and_modify(|curr| *curr += 1).or_insert(1);\n  1494:     /// }\n  1495:     ///\n  1496:     /// assert_eq!(count[\"a\"], 3);\n  1497:     /// assert_eq!(count[\"b\"], 2);\n  1498:     /// assert_eq!(count[\"c\"], 1);\n  1499:     /// ```\n  1500:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1501:     pub fn entry(&mut self, key: K) -> Entry<'_, K, V, A>\n  1502:     where\n  1503:         K: Ord,\n  1504:     {\n  1505:         let (map, dormant_map) = DormantMutRef::new(self);\n  1506:         match map.root {\n  1507:             None => Vacant(VacantEntry {\n  1508:                 key,\n  1509:                 handle: None,\n  1510:                 dormant_map,\n  1511:                 alloc: (*map.alloc).clone(),",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::extract_if",
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
            "id": 1414,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "  1587:     ///\n  1588:     /// // Splitting a map into even and odd keys, reusing the original map:\n  1589:     /// let mut map: BTreeMap<i32, i32> = (0..8).map(|x| (x, x)).collect();\n  1590:     /// let evens: BTreeMap<_, _> = map.extract_if(.., |k, _v| k % 2 == 0).collect();\n  1591:     /// let odds = map;\n  1592:     /// assert_eq!(evens.keys().copied().collect::<Vec<_>>(), [0, 2, 4, 6]);\n  1593:     /// assert_eq!(odds.keys().copied().collect::<Vec<_>>(), [1, 3, 5, 7]);\n  1594:     ///\n  1595:     /// // Splitting a map into low and high halves, reusing the original map:\n  1596:     /// let mut map: BTreeMap<i32, i32> = (0..8).map(|x| (x, x)).collect();\n  1597:     /// let low: BTreeMap<_, _> = map.extract_if(0..4, |_k, _v| true).collect();\n  1598:     /// let high = map;\n  1599:     /// assert_eq!(low.keys().copied().collect::<Vec<_>>(), [0, 1, 2, 3]);\n  1600:     /// assert_eq!(high.keys().copied().collect::<Vec<_>>(), [4, 5, 6, 7]);\n  1601:     /// ```\n  1602:     #[stable(feature = \"btree_extract_if\", since = \"1.91.0\")]\n  1603:     pub fn extract_if<F, R>(&mut self, range: R, pred: F) -> ExtractIf<'_, K, V, R, F, A>\n  1604:     where\n  1605:         K: Ord,\n  1606:         R: RangeBounds<K>,\n  1607:         F: FnMut(&K, &mut V) -> bool,\n  1608:     {\n  1609:         let (inner, alloc) = self.extract_if_inner(range);\n  1610:         ExtractIf { pred, inner, alloc }\n  1611:     }\n  1612: \n  1613:     pub(super) fn extract_if_inner<R>(&mut self, range: R) -> (ExtractIfInner<'_, K, V, R>, A)\n  1614:     where\n  1615:         K: Ord,\n  1616:         R: RangeBounds<K>,\n  1617:     {\n  1618:         if let Some(root) = self.root.as_mut() {\n  1619:             let (root, dormant_root) = DormantMutRef::new(root);",
    "nanvix_source": "  1614:     /// assert_eq!(odds.keys().copied().collect::<Vec<_>>(), [1, 3, 5, 7]);\n  1615:     ///\n  1616:     /// // Splitting a map into low and high halves, reusing the original map:\n  1617:     /// let mut map: BTreeMap<i32, i32> = (0..8).map(|x| (x, x)).collect();\n  1618:     /// let low: BTreeMap<_, _> = map.extract_if(0..4, |_k, _v| true).collect();\n  1619:     /// let high = map;\n  1620:     /// assert_eq!(low.keys().copied().collect::<Vec<_>>(), [0, 1, 2, 3]);\n  1621:     /// assert_eq!(high.keys().copied().collect::<Vec<_>>(), [4, 5, 6, 7]);\n  1622:     /// ```\n  1623:     #[stable(feature = \"btree_extract_if\", since = \"1.91.0\")]\n  1624:     pub fn extract_if<F, R>(&mut self, range: R, pred: F) -> ExtractIf<'_, K, V, R, F, A>\n  1625:     where\n  1626:         K: Ord,\n  1627:         R: RangeBounds<K>,\n  1628:         F: FnMut(&K, &mut V) -> bool,\n  1629:     {\n  1630:         let (inner, alloc) = self.extract_if_inner(range);\n  1631:         ExtractIf { pred, inner, alloc }\n  1632:     }\n  1633: \n  1634:     pub(super) fn extract_if_inner<R>(&mut self, range: R) -> (ExtractIfInner<'_, K, V, R>, A)",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::into_keys",
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
      "name": "into_keys",
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
            "id": 1416,
            "path": "IntoKeys"
          }
        }
      }
    },
    "verification_source": "  1645:     /// The iterator element type is `K`.\n  1646:     ///\n  1647:     /// # Examples\n  1648:     ///\n  1649:     /// ```\n  1650:     /// use std::collections::BTreeMap;\n  1651:     ///\n  1652:     /// let mut a = BTreeMap::new();\n  1653:     /// a.insert(2, \"b\");\n  1654:     /// a.insert(1, \"a\");\n  1655:     ///\n  1656:     /// let keys: Vec<i32> = a.into_keys().collect();\n  1657:     /// assert_eq!(keys, [1, 2]);\n  1658:     /// ```\n  1659:     #[inline]\n  1660:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n  1661:     pub fn into_keys(self) -> IntoKeys<K, V, A> {\n  1662:         IntoKeys { inner: self.into_iter() }\n  1663:     }\n  1664: \n  1665:     /// Creates a consuming iterator visiting all the values, in order by key.\n  1666:     /// The map cannot be used after calling this.\n  1667:     /// The iterator element type is `V`.\n  1668:     ///\n  1669:     /// # Examples\n  1670:     ///\n  1671:     /// ```\n  1672:     /// use std::collections::BTreeMap;\n  1673:     ///\n  1674:     /// let mut a = BTreeMap::new();\n  1675:     /// a.insert(1, \"hello\");\n  1676:     /// a.insert(2, \"goodbye\");\n  1677:     ///",
    "nanvix_source": "  1672:     ///\n  1673:     /// let mut a = BTreeMap::new();\n  1674:     /// a.insert(2, \"b\");\n  1675:     /// a.insert(1, \"a\");\n  1676:     ///\n  1677:     /// let keys: Vec<i32> = a.into_keys().collect();\n  1678:     /// assert_eq!(keys, [1, 2]);\n  1679:     /// ```\n  1680:     #[inline]\n  1681:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n  1682:     pub fn into_keys(self) -> IntoKeys<K, V, A> {\n  1683:         IntoKeys { inner: self.into_iter() }\n  1684:     }\n  1685: \n  1686:     /// Creates a consuming iterator visiting all the values, in order by key.\n  1687:     /// The map cannot be used after calling this.\n  1688:     /// The iterator element type is `V`.\n  1689:     ///\n  1690:     /// # Examples\n  1691:     ///\n  1692:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::into_values",
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
      "name": "into_values",
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
            "id": 1418,
            "path": "IntoValues"
          }
        }
      }
    },
    "verification_source": "  1667:     /// The iterator element type is `V`.\n  1668:     ///\n  1669:     /// # Examples\n  1670:     ///\n  1671:     /// ```\n  1672:     /// use std::collections::BTreeMap;\n  1673:     ///\n  1674:     /// let mut a = BTreeMap::new();\n  1675:     /// a.insert(1, \"hello\");\n  1676:     /// a.insert(2, \"goodbye\");\n  1677:     ///\n  1678:     /// let values: Vec<&str> = a.into_values().collect();\n  1679:     /// assert_eq!(values, [\"hello\", \"goodbye\"]);\n  1680:     /// ```\n  1681:     #[inline]\n  1682:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n  1683:     pub fn into_values(self) -> IntoValues<K, V, A> {\n  1684:         IntoValues { inner: self.into_iter() }\n  1685:     }\n  1686: \n  1687:     /// Makes a `BTreeMap` from a sorted iterator.\n  1688:     pub(crate) fn bulk_build_from_sorted_iter<I>(iter: I, alloc: A) -> Self\n  1689:     where\n  1690:         K: Ord,\n  1691:         I: IntoIterator<Item = (K, V)>,\n  1692:     {\n  1693:         let mut root = Root::new(alloc.clone());\n  1694:         let mut length = 0;\n  1695:         root.bulk_push(DedupSortedIter::new(iter.into_iter()), &mut length, alloc.clone());\n  1696:         BTreeMap { root: Some(root), length, alloc: ManuallyDrop::new(alloc), _marker: PhantomData }\n  1697:     }\n  1698: }\n  1699: ",
    "nanvix_source": "  1694:     ///\n  1695:     /// let mut a = BTreeMap::new();\n  1696:     /// a.insert(1, \"hello\");\n  1697:     /// a.insert(2, \"goodbye\");\n  1698:     ///\n  1699:     /// let values: Vec<&str> = a.into_values().collect();\n  1700:     /// assert_eq!(values, [\"hello\", \"goodbye\"]);\n  1701:     /// ```\n  1702:     #[inline]\n  1703:     #[stable(feature = \"map_into_keys_values\", since = \"1.54.0\")]\n  1704:     pub fn into_values(self) -> IntoValues<K, V, A> {\n  1705:         IntoValues { inner: self.into_iter() }\n  1706:     }\n  1707: \n  1708:     /// Makes a `BTreeMap` from a sorted iterator.\n  1709:     pub(crate) fn bulk_build_from_sorted_iter<I>(iter: I, alloc: A) -> Self\n  1710:     where\n  1711:         K: Ord,\n  1712:         I: IntoIterator<Item = (K, V)>,\n  1713:     {\n  1714:         let mut root = Root::new(alloc.clone());",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::iter_mut",
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
      "name": "iter_mut",
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
            "id": 1422,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  2696:     /// use std::collections::BTreeMap;\n  2697:     ///\n  2698:     /// let mut map = BTreeMap::from([\n  2699:     ///    (\"a\", 1),\n  2700:     ///    (\"b\", 2),\n  2701:     ///    (\"c\", 3),\n  2702:     /// ]);\n  2703:     ///\n  2704:     /// // add 10 to the value if the key isn't \"a\"\n  2705:     /// for (key, value) in map.iter_mut() {\n  2706:     ///     if key != &\"a\" {\n  2707:     ///         *value += 10;\n  2708:     ///     }\n  2709:     /// }\n  2710:     /// ```\n  2711:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2712:     pub fn iter_mut(&mut self) -> IterMut<'_, K, V> {\n  2713:         if let Some(root) = &mut self.root {\n  2714:             let full_range = root.borrow_valmut().full_range();\n  2715: \n  2716:             IterMut { range: full_range, length: self.length, _marker: PhantomData }\n  2717:         } else {\n  2718:             IterMut { range: LazyLeafRange::none(), length: 0, _marker: PhantomData }\n  2719:         }\n  2720:     }\n  2721: \n  2722:     /// Gets an iterator over the keys of the map, in sorted order.\n  2723:     ///\n  2724:     /// # Examples\n  2725:     ///\n  2726:     /// ```\n  2727:     /// use std::collections::BTreeMap;\n  2728:     ///",
    "nanvix_source": "  2724:     /// ]);\n  2725:     ///\n  2726:     /// // add 10 to the value if the key isn't \"a\"\n  2727:     /// for (key, value) in map.iter_mut() {\n  2728:     ///     if key != &\"a\" {\n  2729:     ///         *value += 10;\n  2730:     ///     }\n  2731:     /// }\n  2732:     /// ```\n  2733:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2734:     pub fn iter_mut(&mut self) -> IterMut<'_, K, V> {\n  2735:         if let Some(root) = &mut self.root {\n  2736:             let full_range = root.borrow_valmut().full_range();\n  2737: \n  2738:             IterMut { range: full_range, length: self.length, _marker: PhantomData }\n  2739:         } else {\n  2740:             IterMut { range: LazyLeafRange::none(), length: 0, _marker: PhantomData }\n  2741:         }\n  2742:     }\n  2743: \n  2744:     /// Gets an iterator over the keys of the map, in sorted order.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::range",
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
            "id": 1408,
            "path": "Range"
          }
        }
      }
    },
    "verification_source": "  1392:     /// # Examples\n  1393:     ///\n  1394:     /// ```\n  1395:     /// use std::collections::BTreeMap;\n  1396:     /// use std::ops::Bound::Included;\n  1397:     ///\n  1398:     /// let mut map = BTreeMap::new();\n  1399:     /// map.insert(3, \"a\");\n  1400:     /// map.insert(5, \"b\");\n  1401:     /// map.insert(8, \"c\");\n  1402:     /// for (&key, &value) in map.range((Included(&4), Included(&8))) {\n  1403:     ///     println!(\"{key}: {value}\");\n  1404:     /// }\n  1405:     /// assert_eq!(Some((&5, &\"b\")), map.range(4..).next());\n  1406:     /// ```\n  1407:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n  1408:     pub fn range<T: ?Sized, R>(&self, range: R) -> Range<'_, K, V>\n  1409:     where\n  1410:         T: Ord,\n  1411:         K: Borrow<T> + Ord,\n  1412:         R: RangeBounds<T>,\n  1413:     {\n  1414:         if let Some(root) = &self.root {\n  1415:             Range { inner: root.reborrow().range_search(range) }\n  1416:         } else {\n  1417:             Range { inner: LeafRange::none() }\n  1418:         }\n  1419:     }\n  1420: \n  1421:     /// Constructs a mutable double-ended iterator over a sub-range of elements in the map.\n  1422:     /// The simplest way is to use the range syntax `min..max`, thus `range(min..max)` will\n  1423:     /// yield elements from min (inclusive) to max (exclusive).\n  1424:     /// The range may also be entered as `(Bound<T>, Bound<T>)`, so for example",
    "nanvix_source": "  1419:     /// let mut map = BTreeMap::new();\n  1420:     /// map.insert(3, \"a\");\n  1421:     /// map.insert(5, \"b\");\n  1422:     /// map.insert(8, \"c\");\n  1423:     /// for (&key, &value) in map.range((Included(&4), Included(&8))) {\n  1424:     ///     println!(\"{key}: {value}\");\n  1425:     /// }\n  1426:     /// assert_eq!(Some((&5, &\"b\")), map.range(4..).next());\n  1427:     /// ```\n  1428:     #[stable(feature = \"btree_range\", since = \"1.17.0\")]\n  1429:     pub fn range<T: ?Sized, R>(&self, range: R) -> Range<'_, K, V>\n  1430:     where\n  1431:         T: Ord,\n  1432:         K: Borrow<T> + Ord,\n  1433:         R: RangeBounds<T>,\n  1434:     {\n  1435:         if let Some(root) = &self.root {\n  1436:             Range { inner: root.reborrow().range_search(range) }\n  1437:         } else {\n  1438:             Range { inner: LeafRange::none() }\n  1439:         }",
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
