For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::successors",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
      "name": "successors",
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
            "first",
            {
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
                "id": 84,
                "path": "Option"
              }
            }
          ],
          [
            "succ",
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
                      "generic": "T"
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
            "id": 9940,
            "path": "Successors"
          }
        }
      }
    },
    "verification_source": "    18: /// let powers_of_10 = successors(Some(1_u16), |n| n.checked_mul(10));\n    19: /// assert_eq!(powers_of_10.collect::<Vec<_>>(), &[1, 10, 100, 1_000, 10_000]);\n    20: /// ```\n    21: #[stable(feature = \"iter_successors\", since = \"1.34.0\")]\n    22: pub fn successors<T, F>(first: Option<T>, succ: F) -> Successors<T, F>\n    23: where\n    24:     F: FnMut(&T) -> Option<T>,\n    25: {\n    26:     // If this function returned `impl Iterator<Item=T>`\n    27:     // it could be based on `from_fn` and not need a dedicated type.\n    28:     // However having a named `Successors<T, F>` type allows it to be `Clone` when `T` and `F` are.\n    29:     Successors { next: first, succ }\n    30: }\n    31: \n    32: /// An iterator which, starting from an initial item,\n    33: /// computes each successive item from the preceding one.\n    34: ///\n    35: /// This `struct` is created by the [`iter::successors()`] function.\n    36: /// See its documentation for more.\n    37: ///\n    38: /// [`iter::successors()`]: successors\n    39: #[derive(Clone)]\n    40: #[stable(feature = \"iter_successors\", since = \"1.34.0\")]\n    41: pub struct Successors<T, F> {\n    42:     next: Option<T>,\n    43:     succ: F,\n    44: }\n    45: \n    46: #[stable(feature = \"iter_successors\", since = \"1.34.0\")]\n    47: impl<T, F> Iterator for Successors<T, F>\n    48: where\n    49:     F: FnMut(&T) -> Option<T>,\n    50: {",
    "nanvix_source": "    24:     F: FnMut(&T) -> Option<T>,\n    25: {\n    26:     // If this function returned `impl Iterator<Item=T>`\n    27:     // it could be based on `from_fn` and not need a dedicated type.\n    28:     // However having a named `Successors<T, F>` type allows it to be `Clone` when `T` and `F` are.\n    29:     Successors { next: first, succ }\n    30: }\n    31: \n    32: /// An iterator which, starting from an initial item,\n    33: /// computes each successive item from the preceding one.\n    34: ///\n    35: /// This `struct` is created by the [`iter::successors()`] function.\n    36: /// See its documentation for more.\n    37: ///\n    38: /// [`iter::successors()`]: successors\n    39: #[derive(Clone)]\n    40: #[stable(feature = \"iter_successors\", since = \"1.34.0\")]\n    41: pub struct Successors<T, F> {\n    42:     next: Option<T>,\n    43:     succ: F,\n    44: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::zip",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
            "name": "A"
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
                "generic": "A"
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
                "generic": "B"
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
      "name": "zip",
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
            "a",
            {
              "generic": "A"
            }
          ],
          [
            "b",
            {
              "generic": "B"
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
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "A"
                        },
                        "trait": {
                          "args": null,
                          "id": 80,
                          "path": ""
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "B"
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
            "id": 9913,
            "path": "Zip"
          }
        }
      }
    },
    "verification_source": "    51: /// assert_eq!(iter.next().unwrap(), (1, 4));\n    52: /// assert_eq!(iter.next().unwrap(), (2, 5));\n    53: /// assert_eq!(iter.next().unwrap(), (3, 6));\n    54: /// assert!(iter.next().is_none());\n    55: ///\n    56: /// // Nested zips are also possible:\n    57: /// let zs = [7, 8, 9];\n    58: ///\n    59: /// let mut iter = zip(zip(xs, ys), zs);\n    60: ///\n    61: /// assert_eq!(iter.next().unwrap(), ((1, 4), 7));\n    62: /// assert_eq!(iter.next().unwrap(), ((2, 5), 8));\n    63: /// assert_eq!(iter.next().unwrap(), ((3, 6), 9));\n    64: /// assert!(iter.next().is_none());\n    65: /// ```\n    66: #[stable(feature = \"iter_zip\", since = \"1.59.0\")]\n    67: pub fn zip<A, B>(a: A, b: B) -> Zip<A::IntoIter, B::IntoIter>\n    68: where\n    69:     A: IntoIterator,\n    70:     B: IntoIterator,\n    71: {\n    72:     ZipImpl::new(a.into_iter(), b.into_iter())\n    73: }\n    74: \n    75: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    76: impl<A, B> Iterator for Zip<A, B>\n    77: where\n    78:     A: Iterator,\n    79:     B: Iterator,\n    80: {\n    81:     type Item = (A::Item, B::Item);\n    82: \n    83:     #[inline]",
    "nanvix_source": "    55: /// let zs = [7, 8, 9];\n    56: ///\n    57: /// let mut iter = zip(zip(xs, ys), zs);\n    58: ///\n    59: /// assert_eq!(iter.next().unwrap(), ((1, 4), 7));\n    60: /// assert_eq!(iter.next().unwrap(), ((2, 5), 8));\n    61: /// assert_eq!(iter.next().unwrap(), ((3, 6), 9));\n    62: /// assert!(iter.next().is_none());\n    63: /// ```\n    64: #[stable(feature = \"iter_zip\", since = \"1.59.0\")]\n    65: pub fn zip<A, B>(a: A, b: B) -> Zip<A::IntoIter, B::IntoIter>\n    66: where\n    67:     A: IntoIterator,\n    68:     B: IntoIterator,\n    69: {\n    70:     ZipImpl::new(a.into_iter(), b.into_iter())\n    71: }\n    72: \n    73: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    74: impl<A, B> Iterator for Zip<A, B>\n    75: where",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::iter",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "id": 9971,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  1422:     // Iterator constructors\n  1423:     /////////////////////////////////////////////////////////////////////////\n  1424: \n  1425:     /// Returns an iterator over the possibly contained value.\n  1426:     ///\n  1427:     /// # Examples\n  1428:     ///\n  1429:     /// ```\n  1430:     /// let x = Some(4);\n  1431:     /// assert_eq!(x.iter().next(), Some(&4));\n  1432:     ///\n  1433:     /// let x: Option<u32> = None;\n  1434:     /// assert_eq!(x.iter().next(), None);\n  1435:     /// ```\n  1436:     #[inline]\n  1437:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1438:     pub fn iter(&self) -> Iter<'_, T> {\n  1439:         Iter { inner: Item { opt: self.as_ref() } }\n  1440:     }\n  1441: \n  1442:     /// Returns a mutable iterator over the possibly contained value.\n  1443:     ///\n  1444:     /// # Examples\n  1445:     ///\n  1446:     /// ```\n  1447:     /// let mut x = Some(4);\n  1448:     /// match x.iter_mut().next() {\n  1449:     ///     Some(v) => *v = 42,\n  1450:     ///     None => {},\n  1451:     /// }\n  1452:     /// assert_eq!(x, Some(42));\n  1453:     ///\n  1454:     /// let mut x: Option<u32> = None;",
    "nanvix_source": "  1424:     ///\n  1425:     /// ```\n  1426:     /// let x = Some(4);\n  1427:     /// assert_eq!(x.iter().next(), Some(&4));\n  1428:     ///\n  1429:     /// let x: Option<u32> = None;\n  1430:     /// assert_eq!(x.iter().next(), None);\n  1431:     /// ```\n  1432:     #[inline]\n  1433:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1434:     pub fn iter(&self) -> Iter<'_, T> {\n  1435:         Iter { inner: Item { opt: self.as_ref() } }\n  1436:     }\n  1437: \n  1438:     /// Returns a mutable iterator over the possibly contained value.\n  1439:     ///\n  1440:     /// # Examples\n  1441:     ///\n  1442:     /// ```\n  1443:     /// let mut x = Some(4);\n  1444:     /// match x.iter_mut().next() {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::iter_mut",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 13389,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  1443:     ///\n  1444:     /// # Examples\n  1445:     ///\n  1446:     /// ```\n  1447:     /// let mut x = Some(4);\n  1448:     /// match x.iter_mut().next() {\n  1449:     ///     Some(v) => *v = 42,\n  1450:     ///     None => {},\n  1451:     /// }\n  1452:     /// assert_eq!(x, Some(42));\n  1453:     ///\n  1454:     /// let mut x: Option<u32> = None;\n  1455:     /// assert_eq!(x.iter_mut().next(), None);\n  1456:     /// ```\n  1457:     #[inline]\n  1458:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1459:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1460:         IterMut { inner: Item { opt: self.as_mut() } }\n  1461:     }\n  1462: \n  1463:     /////////////////////////////////////////////////////////////////////////\n  1464:     // Boolean operations on the values, eager and lazy\n  1465:     /////////////////////////////////////////////////////////////////////////\n  1466: \n  1467:     /// Returns [`None`] if the option is [`None`], otherwise returns `optb`.\n  1468:     ///\n  1469:     /// Arguments passed to `and` are eagerly evaluated; if you are passing the\n  1470:     /// result of a function call, it is recommended to use [`and_then`], which is\n  1471:     /// lazily evaluated.\n  1472:     ///\n  1473:     /// [`and_then`]: Option::and_then\n  1474:     ///\n  1475:     /// # Examples",
    "nanvix_source": "  1445:     ///     Some(v) => *v = 42,\n  1446:     ///     None => {},\n  1447:     /// }\n  1448:     /// assert_eq!(x, Some(42));\n  1449:     ///\n  1450:     /// let mut x: Option<u32> = None;\n  1451:     /// assert_eq!(x.iter_mut().next(), None);\n  1452:     /// ```\n  1453:     #[inline]\n  1454:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1455:     pub fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1456:         IterMut { inner: Item { opt: self.as_mut() } }\n  1457:     }\n  1458: \n  1459:     /////////////////////////////////////////////////////////////////////////\n  1460:     // Boolean operations on the values, eager and lazy\n  1461:     /////////////////////////////////////////////////////////////////////////\n  1462: \n  1463:     /// Returns [`None`] if the option is [`None`], otherwise returns `optb`.\n  1464:     ///\n  1465:     /// Arguments passed to `and` are eagerly evaluated; if you are passing the",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::iter",
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
        "is_const": true,
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
            "id": 10009,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  1085:     /// Returns an iterator over the possibly contained value.\n  1086:     ///\n  1087:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1088:     ///\n  1089:     /// # Examples\n  1090:     ///\n  1091:     /// ```\n  1092:     /// let x: Result<u32, &str> = Ok(7);\n  1093:     /// assert_eq!(x.iter().next(), Some(&7));\n  1094:     ///\n  1095:     /// let x: Result<u32, &str> = Err(\"nothing!\");\n  1096:     /// assert_eq!(x.iter().next(), None);\n  1097:     /// ```\n  1098:     #[inline]\n  1099:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1100:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1101:     pub const fn iter(&self) -> Iter<'_, T> {\n  1102:         Iter { inner: self.as_ref().ok() }\n  1103:     }\n  1104: \n  1105:     /// Returns a mutable iterator over the possibly contained value.\n  1106:     ///\n  1107:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1108:     ///\n  1109:     /// # Examples\n  1110:     ///\n  1111:     /// ```\n  1112:     /// let mut x: Result<u32, &str> = Ok(7);\n  1113:     /// match x.iter_mut().next() {\n  1114:     ///     Some(v) => *v = 40,\n  1115:     ///     None => {},\n  1116:     /// }\n  1117:     /// assert_eq!(x, Ok(40));",
    "nanvix_source": "  1089:     /// ```\n  1090:     /// let x: Result<u32, &str> = Ok(7);\n  1091:     /// assert_eq!(x.iter().next(), Some(&7));\n  1092:     ///\n  1093:     /// let x: Result<u32, &str> = Err(\"nothing!\");\n  1094:     /// assert_eq!(x.iter().next(), None);\n  1095:     /// ```\n  1096:     #[inline]\n  1097:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1098:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1099:     pub const fn iter(&self) -> Iter<'_, T> {\n  1100:         Iter { inner: self.as_ref().ok() }\n  1101:     }\n  1102: \n  1103:     /// Returns a mutable iterator over the possibly contained value.\n  1104:     ///\n  1105:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1106:     ///\n  1107:     /// # Examples\n  1108:     ///\n  1109:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::iter_mut",
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
        "is_const": true,
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
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 13412,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  1109:     /// # Examples\n  1110:     ///\n  1111:     /// ```\n  1112:     /// let mut x: Result<u32, &str> = Ok(7);\n  1113:     /// match x.iter_mut().next() {\n  1114:     ///     Some(v) => *v = 40,\n  1115:     ///     None => {},\n  1116:     /// }\n  1117:     /// assert_eq!(x, Ok(40));\n  1118:     ///\n  1119:     /// let mut x: Result<u32, &str> = Err(\"nothing!\");\n  1120:     /// assert_eq!(x.iter_mut().next(), None);\n  1121:     /// ```\n  1122:     #[inline]\n  1123:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1124:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1125:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1126:         IterMut { inner: self.as_mut().ok() }\n  1127:     }\n  1128: \n  1129:     /////////////////////////////////////////////////////////////////////////\n  1130:     // Extract a value\n  1131:     /////////////////////////////////////////////////////////////////////////\n  1132: \n  1133:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1134:     ///\n  1135:     /// Because this function may panic, its use is generally discouraged.\n  1136:     /// Instead, prefer to use pattern matching and handle the [`Err`]\n  1137:     /// case explicitly, or call [`unwrap_or`], [`unwrap_or_else`], or\n  1138:     /// [`unwrap_or_default`].\n  1139:     ///\n  1140:     /// [`unwrap_or`]: Result::unwrap_or\n  1141:     /// [`unwrap_or_else`]: Result::unwrap_or_else",
    "nanvix_source": "  1113:     ///     None => {},\n  1114:     /// }\n  1115:     /// assert_eq!(x, Ok(40));\n  1116:     ///\n  1117:     /// let mut x: Result<u32, &str> = Err(\"nothing!\");\n  1118:     /// assert_eq!(x.iter_mut().next(), None);\n  1119:     /// ```\n  1120:     #[inline]\n  1121:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1122:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1123:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1124:         IterMut { inner: self.as_mut().ok() }\n  1125:     }\n  1126: \n  1127:     /////////////////////////////////////////////////////////////////////////\n  1128:     // Extract a value\n  1129:     /////////////////////////////////////////////////////////////////////////\n  1130: \n  1131:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1132:     ///\n  1133:     /// Because this function may panic, its use is generally discouraged.",
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
