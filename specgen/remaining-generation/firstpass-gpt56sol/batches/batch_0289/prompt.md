For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::map",
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
            "id": 9880,
            "path": "Map"
          }
        }
      }
    },
    "verification_source": "   817:     ///\n   818:     /// ```\n   819:     /// # #![allow(unused_must_use)]\n   820:     /// // don't do this:\n   821:     /// (0..5).map(|x| println!(\"{x}\"));\n   822:     ///\n   823:     /// // it won't even execute, as it is lazy. Rust will warn you about this.\n   824:     ///\n   825:     /// // Instead, use a for-loop:\n   826:     /// for x in 0..5 {\n   827:     ///     println!(\"{x}\");\n   828:     /// }\n   829:     /// ```\n   830:     #[rustc_diagnostic_item = \"IteratorMap\"]\n   831:     #[inline]\n   832:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   833:     fn map<B, F>(self, f: F) -> Map<Self, F>\n   834:     where\n   835:         Self: Sized,\n   836:         F: FnMut(Self::Item) -> B,\n   837:     {\n   838:         Map::new(self, f)\n   839:     }\n   840: \n   841:     /// Calls a closure on each element of an iterator.\n   842:     ///\n   843:     /// This is equivalent to using a [`for`] loop on the iterator, although\n   844:     /// `break` and `continue` are not possible from a closure. It's generally\n   845:     /// more idiomatic to use a `for` loop, but `for_each` may be more legible\n   846:     /// when processing items at the end of longer iterator chains. In some\n   847:     /// cases `for_each` may also be faster than a loop, because it will use\n   848:     /// internal iteration on adapters like `Chain`.\n   849:     ///",
    "nanvix_source": "   821:     /// // it won't even execute, as it is lazy. Rust will warn you about this.\n   822:     ///\n   823:     /// // Instead, use a for-loop:\n   824:     /// for x in 0..5 {\n   825:     ///     println!(\"{x}\");\n   826:     /// }\n   827:     /// ```\n   828:     #[rustc_diagnostic_item = \"IteratorMap\"]\n   829:     #[inline]\n   830:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   831:     fn map<B, F>(self, f: F) -> Map<Self, F>\n   832:     where\n   833:         Self: Sized,\n   834:         F: FnMut(Self::Item) -> B,\n   835:     {\n   836:         Map::new(self, f)\n   837:     }\n   838: \n   839:     /// Calls a closure on each element of an iterator.\n   840:     ///\n   841:     /// This is equivalent to using a [`for`] loop on the iterator, although",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::map_while",
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
      "name": "map_while",
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
            "id": 9883,
            "path": "MapWhile"
          }
        }
      }
    },
    "verification_source": "  1332:     ///\n  1333:     /// let result: Vec<i32> = iter.collect();\n  1334:     ///\n  1335:     /// assert_eq!(result, [4]);\n  1336:     /// ```\n  1337:     ///\n  1338:     /// The `-3` is no longer there, because it was consumed in order to see if\n  1339:     /// the iteration should stop, but wasn't placed back into the iterator.\n  1340:     ///\n  1341:     /// Note that unlike [`take_while`] this iterator is **not** fused.\n  1342:     /// It is also not specified what this iterator returns after the first [`None`] is returned.\n  1343:     /// If you need a fused iterator, use [`fuse`].\n  1344:     ///\n  1345:     /// [`fuse`]: Iterator::fuse\n  1346:     #[inline]\n  1347:     #[stable(feature = \"iter_map_while\", since = \"1.57.0\")]\n  1348:     fn map_while<B, P>(self, predicate: P) -> MapWhile<Self, P>\n  1349:     where\n  1350:         Self: Sized,\n  1351:         P: FnMut(Self::Item) -> Option<B>,\n  1352:     {\n  1353:         MapWhile::new(self, predicate)\n  1354:     }\n  1355: \n  1356:     /// Creates an iterator that skips the first `n` elements.\n  1357:     ///\n  1358:     /// `skip(n)` skips elements until `n` elements are skipped or the end of the\n  1359:     /// iterator is reached (whichever happens first). After that, all the remaining\n  1360:     /// elements are yielded. In particular, if the original iterator is too short,\n  1361:     /// then the returned iterator is empty.\n  1362:     ///\n  1363:     /// Rather than overriding this method directly, instead override the `nth` method.\n  1364:     ///",
    "nanvix_source": "  1336:     /// The `-3` is no longer there, because it was consumed in order to see if\n  1337:     /// the iteration should stop, but wasn't placed back into the iterator.\n  1338:     ///\n  1339:     /// Note that unlike [`take_while`] this iterator is **not** fused.\n  1340:     /// It is also not specified what this iterator returns after the first [`None`] is returned.\n  1341:     /// If you need a fused iterator, use [`fuse`].\n  1342:     ///\n  1343:     /// [`fuse`]: Iterator::fuse\n  1344:     #[inline]\n  1345:     #[stable(feature = \"iter_map_while\", since = \"1.57.0\")]\n  1346:     fn map_while<B, P>(self, predicate: P) -> MapWhile<Self, P>\n  1347:     where\n  1348:         Self: Sized,\n  1349:         P: FnMut(Self::Item) -> Option<B>,\n  1350:     {\n  1351:         MapWhile::new(self, predicate)\n  1352:     }\n  1353: \n  1354:     /// Creates an iterator that skips the first `n` elements.\n  1355:     ///\n  1356:     /// `skip(n)` skips elements until `n` elements are skipped or the end of the",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::max",
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
                      "id": 50,
                      "path": "Ord"
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
      "name": "max",
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
    "verification_source": "  3236:     ///     2.4\n  3237:     /// );\n  3238:     /// ```\n  3239:     ///\n  3240:     /// # Examples\n  3241:     ///\n  3242:     /// ```\n  3243:     /// let a = [1, 2, 3];\n  3244:     /// let b: [u32; 0] = [];\n  3245:     ///\n  3246:     /// assert_eq!(a.into_iter().max(), Some(3));\n  3247:     /// assert_eq!(b.into_iter().max(), None);\n  3248:     /// ```\n  3249:     #[inline]\n  3250:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3251:     #[rustc_non_const_trait_method]\n  3252:     fn max(self) -> Option<Self::Item>\n  3253:     where\n  3254:         Self: Sized,\n  3255:         Self::Item: Ord,\n  3256:     {\n  3257:         self.max_by(Ord::cmp)\n  3258:     }\n  3259: \n  3260:     /// Returns the minimum element of an iterator.\n  3261:     ///\n  3262:     /// If several elements are equally minimum, the first element is returned.\n  3263:     /// If the iterator is empty, [`None`] is returned.\n  3264:     ///\n  3265:     /// Note that [`f32`]/[`f64`] doesn't implement [`Ord`] due to NaN being\n  3266:     /// incomparable. You can work around this by using [`Iterator::reduce`]:\n  3267:     /// ```\n  3268:     /// assert_eq!(",
    "nanvix_source": "  3240:     /// ```\n  3241:     /// let a = [1, 2, 3];\n  3242:     /// let b: [u32; 0] = [];\n  3243:     ///\n  3244:     /// assert_eq!(a.into_iter().max(), Some(3));\n  3245:     /// assert_eq!(b.into_iter().max(), None);\n  3246:     /// ```\n  3247:     #[inline]\n  3248:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3249:     #[rustc_non_const_trait_method]\n  3250:     fn max(self) -> Option<Self::Item>\n  3251:     where\n  3252:         Self: Sized,\n  3253:         Self::Item: Ord,\n  3254:     {\n  3255:         self.max_by(Ord::cmp)\n  3256:     }\n  3257: \n  3258:     /// Returns the minimum element of an iterator.\n  3259:     ///\n  3260:     /// If several elements are equally minimum, the first element is returned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::max_by",
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
                            },
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
                            "resolved_path": {
                              "args": null,
                              "id": 1682,
                              "path": "Ordering"
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
      "name": "max_by",
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
            "compare",
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
    "verification_source": "  3330: \n  3331:     /// Returns the element that gives the maximum value with respect to the\n  3332:     /// specified comparison function.\n  3333:     ///\n  3334:     /// If several elements are equally maximum, the last element is\n  3335:     /// returned. If the iterator is empty, [`None`] is returned.\n  3336:     ///\n  3337:     /// # Examples\n  3338:     ///\n  3339:     /// ```\n  3340:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3341:     /// assert_eq!(a.into_iter().max_by(|x, y| x.cmp(y)).unwrap(), 5);\n  3342:     /// ```\n  3343:     #[inline]\n  3344:     #[stable(feature = \"iter_max_by\", since = \"1.15.0\")]\n  3345:     #[rustc_non_const_trait_method]\n  3346:     fn max_by<F>(self, compare: F) -> Option<Self::Item>\n  3347:     where\n  3348:         Self: Sized,\n  3349:         F: FnMut(&Self::Item, &Self::Item) -> Ordering,\n  3350:     {\n  3351:         #[inline]\n  3352:         fn fold<T>(mut compare: impl FnMut(&T, &T) -> Ordering) -> impl FnMut(T, T) -> T {\n  3353:             move |x, y| cmp::max_by(x, y, &mut compare)\n  3354:         }\n  3355: \n  3356:         self.reduce(fold(compare))\n  3357:     }\n  3358: \n  3359:     /// Returns the element that gives the minimum value from the\n  3360:     /// specified function.\n  3361:     ///\n  3362:     /// If several elements are equally minimum, the first element is",
    "nanvix_source": "  3334:     ///\n  3335:     /// # Examples\n  3336:     ///\n  3337:     /// ```\n  3338:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3339:     /// assert_eq!(a.into_iter().max_by(|x, y| x.cmp(y)).unwrap(), 5);\n  3340:     /// ```\n  3341:     #[inline]\n  3342:     #[stable(feature = \"iter_max_by\", since = \"1.15.0\")]\n  3343:     #[rustc_non_const_trait_method]\n  3344:     fn max_by<F>(self, compare: F) -> Option<Self::Item>\n  3345:     where\n  3346:         Self: Sized,\n  3347:         F: FnMut(&Self::Item, &Self::Item) -> Ordering,\n  3348:     {\n  3349:         #[inline]\n  3350:         fn fold<T>(mut compare: impl FnMut(&T, &T) -> Ordering) -> impl FnMut(T, T) -> T {\n  3351:             move |x, y| cmp::max_by(x, y, &mut compare)\n  3352:         }\n  3353: \n  3354:         self.reduce(fold(compare))",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::max_by_key",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 50,
                        "path": "Ord"
                      }
                    }
                  }
                ],
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
      "name": "max_by_key",
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
    "verification_source": "  3296: \n  3297:     /// Returns the element that gives the maximum value from the\n  3298:     /// specified function.\n  3299:     ///\n  3300:     /// If several elements are equally maximum, the last element is\n  3301:     /// returned. If the iterator is empty, [`None`] is returned.\n  3302:     ///\n  3303:     /// # Examples\n  3304:     ///\n  3305:     /// ```\n  3306:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3307:     /// assert_eq!(a.into_iter().max_by_key(|x| x.abs()).unwrap(), -10);\n  3308:     /// ```\n  3309:     #[inline]\n  3310:     #[stable(feature = \"iter_cmp_by_key\", since = \"1.6.0\")]\n  3311:     #[rustc_non_const_trait_method]\n  3312:     fn max_by_key<B: Ord, F>(self, f: F) -> Option<Self::Item>\n  3313:     where\n  3314:         Self: Sized,\n  3315:         F: FnMut(&Self::Item) -> B,\n  3316:     {\n  3317:         #[inline]\n  3318:         fn key<T, B>(mut f: impl FnMut(&T) -> B) -> impl FnMut(T) -> (B, T) {\n  3319:             move |x| (f(&x), x)\n  3320:         }\n  3321: \n  3322:         #[inline]\n  3323:         fn compare<T, B: Ord>((x_p, _): &(B, T), (y_p, _): &(B, T)) -> Ordering {\n  3324:             x_p.cmp(y_p)\n  3325:         }\n  3326: \n  3327:         let (_, x) = self.map(key(f)).max_by(compare)?;\n  3328:         Some(x)",
    "nanvix_source": "  3300:     ///\n  3301:     /// # Examples\n  3302:     ///\n  3303:     /// ```\n  3304:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3305:     /// assert_eq!(a.into_iter().max_by_key(|x| x.abs()).unwrap(), -10);\n  3306:     /// ```\n  3307:     #[inline]\n  3308:     #[stable(feature = \"iter_cmp_by_key\", since = \"1.6.0\")]\n  3309:     #[rustc_non_const_trait_method]\n  3310:     fn max_by_key<B: Ord, F>(self, f: F) -> Option<Self::Item>\n  3311:     where\n  3312:         Self: Sized,\n  3313:         F: FnMut(&Self::Item) -> B,\n  3314:     {\n  3315:         #[inline]\n  3316:         fn key<T, B>(mut f: impl FnMut(&T) -> B) -> impl FnMut(T) -> (B, T) {\n  3317:             move |x| (f(&x), x)\n  3318:         }\n  3319: \n  3320:         #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::min",
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
                      "id": 50,
                      "path": "Ord"
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
      "name": "min",
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
    "verification_source": "  3273:     ///     1.3\n  3274:     /// );\n  3275:     /// ```\n  3276:     ///\n  3277:     /// # Examples\n  3278:     ///\n  3279:     /// ```\n  3280:     /// let a = [1, 2, 3];\n  3281:     /// let b: [u32; 0] = [];\n  3282:     ///\n  3283:     /// assert_eq!(a.into_iter().min(), Some(1));\n  3284:     /// assert_eq!(b.into_iter().min(), None);\n  3285:     /// ```\n  3286:     #[inline]\n  3287:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3288:     #[rustc_non_const_trait_method]\n  3289:     fn min(self) -> Option<Self::Item>\n  3290:     where\n  3291:         Self: Sized,\n  3292:         Self::Item: Ord,\n  3293:     {\n  3294:         self.min_by(Ord::cmp)\n  3295:     }\n  3296: \n  3297:     /// Returns the element that gives the maximum value from the\n  3298:     /// specified function.\n  3299:     ///\n  3300:     /// If several elements are equally maximum, the last element is\n  3301:     /// returned. If the iterator is empty, [`None`] is returned.\n  3302:     ///\n  3303:     /// # Examples\n  3304:     ///\n  3305:     /// ```",
    "nanvix_source": "  3277:     /// ```\n  3278:     /// let a = [1, 2, 3];\n  3279:     /// let b: [u32; 0] = [];\n  3280:     ///\n  3281:     /// assert_eq!(a.into_iter().min(), Some(1));\n  3282:     /// assert_eq!(b.into_iter().min(), None);\n  3283:     /// ```\n  3284:     #[inline]\n  3285:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3286:     #[rustc_non_const_trait_method]\n  3287:     fn min(self) -> Option<Self::Item>\n  3288:     where\n  3289:         Self: Sized,\n  3290:         Self::Item: Ord,\n  3291:     {\n  3292:         self.min_by(Ord::cmp)\n  3293:     }\n  3294: \n  3295:     /// Returns the element that gives the maximum value from the\n  3296:     /// specified function.\n  3297:     ///",
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
