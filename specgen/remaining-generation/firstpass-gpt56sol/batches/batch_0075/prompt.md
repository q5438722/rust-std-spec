For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cmp::max_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
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
          },
          {
            "kind": {
              "type": {
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
                                "borrowed_ref": {
                                  "is_mutable": false,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              },
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "max_by",
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
            "v1",
            {
              "generic": "T"
            }
          ],
          [
            "v2",
            {
              "generic": "T"
            }
          ],
          [
            "compare",
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
    "verification_source": "  1695: ///\n  1696: /// let abs_cmp = |x: &i32, y: &i32| x.abs().cmp(&y.abs());\n  1697: ///\n  1698: /// let result = cmp::max_by(3, -2, abs_cmp) ;\n  1699: /// assert_eq!(result, 3);\n  1700: ///\n  1701: /// let result = cmp::max_by(1, -2, abs_cmp);\n  1702: /// assert_eq!(result, -2);\n  1703: ///\n  1704: /// let result = cmp::max_by(1, -1, abs_cmp);\n  1705: /// assert_eq!(result, -1);\n  1706: /// ```\n  1707: #[inline]\n  1708: #[must_use]\n  1709: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1710: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1711: pub const fn max_by<T: [const] Destruct, F: [const] FnOnce(&T, &T) -> Ordering>(\n  1712:     v1: T,\n  1713:     v2: T,\n  1714:     compare: F,\n  1715: ) -> T {\n  1716:     if compare(&v1, &v2).is_gt() { v1 } else { v2 }\n  1717: }\n  1718: \n  1719: /// Returns the element that gives the maximum value from the specified function.\n  1720: ///\n  1721: /// Returns the second argument if the comparison determines them to be equal.\n  1722: ///\n  1723: /// # Examples\n  1724: ///\n  1725: /// ```\n  1726: /// use std::cmp;\n  1727: ///",
    "nanvix_source": "  1702: /// let result = cmp::max_by(1, -2, abs_cmp);\n  1703: /// assert_eq!(result, -2);\n  1704: ///\n  1705: /// let result = cmp::max_by(1, -1, abs_cmp);\n  1706: /// assert_eq!(result, -1);\n  1707: /// ```\n  1708: #[inline]\n  1709: #[must_use]\n  1710: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1711: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1712: pub const fn max_by<T: [const] Destruct, F: [const] FnOnce(&T, &T) -> Ordering>(\n  1713:     v1: T,\n  1714:     v2: T,\n  1715:     compare: F,\n  1716: ) -> T {\n  1717:     if compare(&v1, &v2).is_gt() { v1 } else { v2 }\n  1718: }\n  1719: \n  1720: /// Returns the element that gives the maximum value from the specified function.\n  1721: ///\n  1722: /// Returns the second argument if the comparison determines them to be equal.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::max_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
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
                    "modifier": "maybe_const",
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
                            "generic": "K"
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
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 50,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "max_by_key",
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
            "v1",
            {
              "generic": "T"
            }
          ],
          [
            "v2",
            {
              "generic": "T"
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
    "verification_source": "  1725: /// ```\n  1726: /// use std::cmp;\n  1727: ///\n  1728: /// let result = cmp::max_by_key(3, -2, |x: &i32| x.abs());\n  1729: /// assert_eq!(result, 3);\n  1730: ///\n  1731: /// let result = cmp::max_by_key(1, -2, |x: &i32| x.abs());\n  1732: /// assert_eq!(result, -2);\n  1733: ///\n  1734: /// let result = cmp::max_by_key(1, -1, |x: &i32| x.abs());\n  1735: /// assert_eq!(result, -1);\n  1736: /// ```\n  1737: #[inline]\n  1738: #[must_use]\n  1739: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1740: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1741: pub const fn max_by_key<T, F, K>(v1: T, v2: T, mut f: F) -> T\n  1742: where\n  1743:     T: [const] Destruct,\n  1744:     F: [const] FnMut(&T) -> K + [const] Destruct,\n  1745:     K: [const] Ord + [const] Destruct,\n  1746: {\n  1747:     if f(&v2) < f(&v1) { v1 } else { v2 }\n  1748: }\n  1749: \n  1750: /// Compares and sorts two values, returning minimum and maximum.\n  1751: ///\n  1752: /// Returns `[v1, v2]` if the comparison determines them to be equal.\n  1753: ///\n  1754: /// # Examples\n  1755: ///\n  1756: /// ```\n  1757: /// #![feature(cmp_minmax)]",
    "nanvix_source": "  1732: /// let result = cmp::max_by_key(1, -2, |x: &i32| x.abs());\n  1733: /// assert_eq!(result, -2);\n  1734: ///\n  1735: /// let result = cmp::max_by_key(1, -1, |x: &i32| x.abs());\n  1736: /// assert_eq!(result, -1);\n  1737: /// ```\n  1738: #[inline]\n  1739: #[must_use]\n  1740: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1741: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1742: pub const fn max_by_key<T, F, K>(v1: T, v2: T, mut f: F) -> T\n  1743: where\n  1744:     T: [const] Destruct,\n  1745:     F: [const] FnMut(&T) -> K + [const] Destruct,\n  1746:     K: [const] Ord + [const] Destruct,\n  1747: {\n  1748:     if f(&v2) < f(&v1) { v1 } else { v2 }\n  1749: }\n  1750: \n  1751: /// Compares and sorts two values, returning minimum and maximum.\n  1752: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::min_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
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
          },
          {
            "kind": {
              "type": {
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
                                "borrowed_ref": {
                                  "is_mutable": false,
                                  "lifetime": null,
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              },
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "min_by",
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
            "v1",
            {
              "generic": "T"
            }
          ],
          [
            "v2",
            {
              "generic": "T"
            }
          ],
          [
            "compare",
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
    "verification_source": "  1588: ///\n  1589: /// let abs_cmp = |x: &i32, y: &i32| x.abs().cmp(&y.abs());\n  1590: ///\n  1591: /// let result = cmp::min_by(2, -1, abs_cmp);\n  1592: /// assert_eq!(result, -1);\n  1593: ///\n  1594: /// let result = cmp::min_by(2, -3, abs_cmp);\n  1595: /// assert_eq!(result, 2);\n  1596: ///\n  1597: /// let result = cmp::min_by(1, -1, abs_cmp);\n  1598: /// assert_eq!(result, 1);\n  1599: /// ```\n  1600: #[inline]\n  1601: #[must_use]\n  1602: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1603: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1604: pub const fn min_by<T: [const] Destruct, F: [const] FnOnce(&T, &T) -> Ordering>(\n  1605:     v1: T,\n  1606:     v2: T,\n  1607:     compare: F,\n  1608: ) -> T {\n  1609:     if compare(&v1, &v2).is_le() { v1 } else { v2 }\n  1610: }\n  1611: \n  1612: /// Returns the element that gives the minimum value from the specified function.\n  1613: ///\n  1614: /// Returns the first argument if the comparison determines them to be equal.\n  1615: ///\n  1616: /// # Examples\n  1617: ///\n  1618: /// ```\n  1619: /// use std::cmp;\n  1620: ///",
    "nanvix_source": "  1595: /// let result = cmp::min_by(2, -3, abs_cmp);\n  1596: /// assert_eq!(result, 2);\n  1597: ///\n  1598: /// let result = cmp::min_by(1, -1, abs_cmp);\n  1599: /// assert_eq!(result, 1);\n  1600: /// ```\n  1601: #[inline]\n  1602: #[must_use]\n  1603: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1604: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1605: pub const fn min_by<T: [const] Destruct, F: [const] FnOnce(&T, &T) -> Ordering>(\n  1606:     v1: T,\n  1607:     v2: T,\n  1608:     compare: F,\n  1609: ) -> T {\n  1610:     if compare(&v1, &v2).is_le() { v1 } else { v2 }\n  1611: }\n  1612: \n  1613: /// Returns the element that gives the minimum value from the specified function.\n  1614: ///\n  1615: /// Returns the first argument if the comparison determines them to be equal.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::min_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
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
                    "modifier": "maybe_const",
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
                            "generic": "K"
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
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 50,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "min_by_key",
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
            "v1",
            {
              "generic": "T"
            }
          ],
          [
            "v2",
            {
              "generic": "T"
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
    "verification_source": "  1618: /// ```\n  1619: /// use std::cmp;\n  1620: ///\n  1621: /// let result = cmp::min_by_key(2, -1, |x: &i32| x.abs());\n  1622: /// assert_eq!(result, -1);\n  1623: ///\n  1624: /// let result = cmp::min_by_key(2, -3, |x: &i32| x.abs());\n  1625: /// assert_eq!(result, 2);\n  1626: ///\n  1627: /// let result = cmp::min_by_key(1, -1, |x: &i32| x.abs());\n  1628: /// assert_eq!(result, 1);\n  1629: /// ```\n  1630: #[inline]\n  1631: #[must_use]\n  1632: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1633: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1634: pub const fn min_by_key<T, F, K>(v1: T, v2: T, mut f: F) -> T\n  1635: where\n  1636:     T: [const] Destruct,\n  1637:     F: [const] FnMut(&T) -> K + [const] Destruct,\n  1638:     K: [const] Ord + [const] Destruct,\n  1639: {\n  1640:     if f(&v2) < f(&v1) { v2 } else { v1 }\n  1641: }\n  1642: \n  1643: /// Compares and returns the maximum of two values.\n  1644: ///\n  1645: /// Returns the second argument if the comparison determines them to be equal.\n  1646: ///\n  1647: /// Internally uses an alias to [`Ord::max`].\n  1648: ///\n  1649: /// # Examples\n  1650: ///",
    "nanvix_source": "  1625: /// let result = cmp::min_by_key(2, -3, |x: &i32| x.abs());\n  1626: /// assert_eq!(result, 2);\n  1627: ///\n  1628: /// let result = cmp::min_by_key(1, -1, |x: &i32| x.abs());\n  1629: /// assert_eq!(result, 1);\n  1630: /// ```\n  1631: #[inline]\n  1632: #[must_use]\n  1633: #[stable(feature = \"cmp_min_max_by\", since = \"1.53.0\")]\n  1634: #[rustc_const_unstable(feature = \"const_cmp\", issue = \"143800\")]\n  1635: pub const fn min_by_key<T, F, K>(v1: T, v2: T, mut f: F) -> T\n  1636: where\n  1637:     T: [const] Destruct,\n  1638:     F: [const] FnMut(&T) -> K + [const] Destruct,\n  1639:     K: [const] Ord + [const] Destruct,\n  1640: {\n  1641:     if f(&v2) < f(&v1) { v2 } else { v1 }\n  1642: }\n  1643: \n  1644: /// Compares and returns the maximum of two values.\n  1645: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::poll_fn",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
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
                                    "id": 13510,
                                    "path": "crate::task::Context"
                                  }
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
                                        "generic": "T"
                                      }
                                    }
                                  ],
                                  "constraints": []
                                }
                              },
                              "id": 10198,
                              "path": "crate::task::Poll"
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
      "name": "poll_fn",
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13504,
            "path": "PollFn"
          }
        }
      }
    },
    "verification_source": "    96: ///                 Poll::Pending\n    97: ///             }\n    98: ///         }).await\n    99: ///     }\n   100: /// }\n   101: ///\n   102: /// let a = async { 42 };\n   103: /// let b = future::pending();\n   104: /// let v = naive_select(a, b).await;\n   105: /// assert_eq!(v, 42);\n   106: /// # }\n   107: /// ```\n   108: ///\n   109: ///   - Notice how, by virtue of being in an `async` context, we have been able to make the [`pin!`]\n   110: ///     macro work, thereby avoiding any need for the `unsafe`\n   111: ///     <code>[Pin::new_unchecked](&mut fut)</code> constructor.\n   112: ///\n   113: /// [`pin!`]: crate::pin::pin!\n   114: #[stable(feature = \"future_poll_fn\", since = \"1.64.0\")]\n   115: pub fn poll_fn<T, F>(f: F) -> PollFn<F>\n   116: where\n   117:     F: FnMut(&mut Context<'_>) -> Poll<T>,\n   118: {\n   119:     PollFn { f }\n   120: }\n   121: \n   122: /// A Future that wraps a function returning [`Poll`].\n   123: ///\n   124: /// This `struct` is created by [`poll_fn()`]. See its\n   125: /// documentation for more.\n   126: #[must_use = \"futures do nothing unless you `.await` or poll them\"]\n   127: #[stable(feature = \"future_poll_fn\", since = \"1.64.0\")]\n   128: pub struct PollFn<F> {",
    "nanvix_source": "   102: /// let a = async { 42 };\n   103: /// let b = future::pending();\n   104: /// let v = naive_select(a, b).await;\n   105: /// assert_eq!(v, 42);\n   106: /// # }\n   107: /// ```\n   108: ///\n   109: ///   - Notice how, by virtue of being in an `async` context, we have been able to make the [`pin!`]\n   110: ///     macro work, thereby avoiding any need for the `unsafe`\n   111: ///     <code>[Pin::new_unchecked](&mut fut)</code> constructor.\n   112: ///\n   113: /// [`pin!`]: crate::pin::pin!\n   114: #[stable(feature = \"future_poll_fn\", since = \"1.64.0\")]\n   115: pub fn poll_fn<T, F>(f: F) -> PollFn<F>\n   116: where\n   117:     F: FnMut(&mut Context<'_>) -> Poll<T>,\n   118: {\n   119:     PollFn { f }\n   120: }\n   121: \n   122: /// A Future that wraps a function returning [`Poll`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::Bound::map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
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
            "name": "U"
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
                        "args": {
                          "parenthesized": {
                            "inputs": [
                              {
                                "generic": "T"
                              }
                            ],
                            "output": {
                              "generic": "U"
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
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9759,
            "path": "Bound"
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
        "impl_id": "core:24011",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9759",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "Bound"
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "U"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9759,
            "path": "Bound"
          }
        }
      }
    },
    "verification_source": "   735:     ///\n   736:     /// let bound_string = Included(\"Hello, World!\");\n   737:     ///\n   738:     /// assert_eq!(bound_string.map(|s| s.len()), Included(13));\n   739:     /// ```\n   740:     ///\n   741:     /// ```\n   742:     /// use std::ops::Bound;\n   743:     /// use Bound::*;\n   744:     ///\n   745:     /// let unbounded_string: Bound<String> = Unbounded;\n   746:     ///\n   747:     /// assert_eq!(unbounded_string.map(|s| s.len()), Unbounded);\n   748:     /// ```\n   749:     #[inline]\n   750:     #[stable(feature = \"bound_map\", since = \"1.77.0\")]\n   751:     pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> Bound<U> {\n   752:         match self {\n   753:             Unbounded => Unbounded,\n   754:             Included(x) => Included(f(x)),\n   755:             Excluded(x) => Excluded(f(x)),\n   756:         }\n   757:     }\n   758: }\n   759: \n   760: impl<T: Copy> Bound<&T> {\n   761:     /// Map a `Bound<&T>` to a `Bound<T>` by copying the contents of the bound.\n   762:     ///\n   763:     /// # Examples\n   764:     ///\n   765:     /// ```\n   766:     /// #![feature(bound_copied)]\n   767:     ///",
    "nanvix_source": "   741:     /// ```\n   742:     /// use std::ops::Bound;\n   743:     /// use Bound::*;\n   744:     ///\n   745:     /// let unbounded_string: Bound<String> = Unbounded;\n   746:     ///\n   747:     /// assert_eq!(unbounded_string.map(|s| s.len()), Unbounded);\n   748:     /// ```\n   749:     #[inline]\n   750:     #[stable(feature = \"bound_map\", since = \"1.77.0\")]\n   751:     pub fn map<U, F: FnOnce(T) -> U>(self, f: F) -> Bound<U> {\n   752:         match self {\n   753:             Unbounded => Unbounded,\n   754:             Included(x) => Included(f(x)),\n   755:             Excluded(x) => Excluded(f(x)),\n   756:         }\n   757:     }\n   758: }\n   759: \n   760: impl<T: Copy> Bound<&T> {\n   761:     /// Map a `Bound<&T>` to a `Bound<T>` by copying the contents of the bound.",
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
