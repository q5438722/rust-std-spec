For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::take_while",
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
      "name": "take_while",
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
            "id": 9910,
            "path": "TakeWhile"
          }
        }
      }
    },
    "verification_source": "  1244:     /// let a = [1, 2, 3, 4];\n  1245:     /// let mut iter = a.into_iter();\n  1246:     ///\n  1247:     /// let result: Vec<i32> = iter.by_ref().take_while(|&n| n != 3).collect();\n  1248:     ///\n  1249:     /// assert_eq!(result, [1, 2]);\n  1250:     ///\n  1251:     /// let result: Vec<i32> = iter.collect();\n  1252:     ///\n  1253:     /// assert_eq!(result, [4]);\n  1254:     /// ```\n  1255:     ///\n  1256:     /// The `3` is no longer there, because it was consumed in order to see if\n  1257:     /// the iteration should stop, but wasn't placed back into the iterator.\n  1258:     #[inline]\n  1259:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1260:     fn take_while<P>(self, predicate: P) -> TakeWhile<Self, P>\n  1261:     where\n  1262:         Self: Sized,\n  1263:         P: FnMut(&Self::Item) -> bool,\n  1264:     {\n  1265:         TakeWhile::new(self, predicate)\n  1266:     }\n  1267: \n  1268:     /// Creates an iterator that both yields elements based on a predicate and maps.\n  1269:     ///\n  1270:     /// `map_while()` takes a closure as an argument. It will call this\n  1271:     /// closure on each element of the iterator, and yield elements\n  1272:     /// while it returns [`Some(_)`][`Some`].\n  1273:     ///\n  1274:     /// # Examples\n  1275:     ///\n  1276:     /// Basic usage:",
    "nanvix_source": "  1248:     ///\n  1249:     /// let result: Vec<i32> = iter.collect();\n  1250:     ///\n  1251:     /// assert_eq!(result, [4]);\n  1252:     /// ```\n  1253:     ///\n  1254:     /// The `3` is no longer there, because it was consumed in order to see if\n  1255:     /// the iteration should stop, but wasn't placed back into the iterator.\n  1256:     #[inline]\n  1257:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1258:     fn take_while<P>(self, predicate: P) -> TakeWhile<Self, P>\n  1259:     where\n  1260:         Self: Sized,\n  1261:         P: FnMut(&Self::Item) -> bool,\n  1262:     {\n  1263:         TakeWhile::new(self, predicate)\n  1264:     }\n  1265: \n  1266:     /// Creates an iterator that both yields elements based on a predicate and maps.\n  1267:     ///\n  1268:     /// `map_while()` takes a closure as an argument. It will call this",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::try_fold",
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
                              "generic": "B"
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
                            "generic": "R"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "B"
                                  }
                                }
                              },
                              "name": "Output"
                            }
                          ]
                        }
                      },
                      "id": 12972,
                      "path": "Try"
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
      "name": "try_fold",
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
            "init",
            {
              "generic": "B"
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
          "generic": "R"
        }
      }
    },
    "verification_source": "  2472:     ///         ControlFlow::Break(prev)\n  2473:     ///     }\n  2474:     /// });\n  2475:     /// assert_eq!(triangular, ControlFlow::Break(120));\n  2476:     ///\n  2477:     /// let triangular = (1..30).try_fold(0_u64, |prev, x| {\n  2478:     ///     if let Some(next) = prev.checked_add(x) {\n  2479:     ///         ControlFlow::Continue(next)\n  2480:     ///     } else {\n  2481:     ///         ControlFlow::Break(prev)\n  2482:     ///     }\n  2483:     /// });\n  2484:     /// assert_eq!(triangular, ControlFlow::Continue(435));\n  2485:     /// ```\n  2486:     #[inline]\n  2487:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n  2488:     fn try_fold<B, F, R>(&mut self, init: B, mut f: F) -> R\n  2489:     where\n  2490:         Self: Sized,\n  2491:         F: [const] FnMut(B, Self::Item) -> R + [const] Destruct,\n  2492:         R: [const] Try<Output = B>,\n  2493:     {\n  2494:         let mut accum = init;\n  2495:         while let Some(x) = self.next() {\n  2496:             accum = f(accum, x)?;\n  2497:         }\n  2498:         try { accum }\n  2499:     }\n  2500: \n  2501:     /// An iterator method that applies a fallible function to each item in the\n  2502:     /// iterator, stopping at the first error and returning that error.\n  2503:     ///\n  2504:     /// This can also be thought of as the fallible form of [`for_each()`]",
    "nanvix_source": "  2476:     ///     if let Some(next) = prev.checked_add(x) {\n  2477:     ///         ControlFlow::Continue(next)\n  2478:     ///     } else {\n  2479:     ///         ControlFlow::Break(prev)\n  2480:     ///     }\n  2481:     /// });\n  2482:     /// assert_eq!(triangular, ControlFlow::Continue(435));\n  2483:     /// ```\n  2484:     #[inline]\n  2485:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n  2486:     fn try_fold<B, F, R>(&mut self, init: B, mut f: F) -> R\n  2487:     where\n  2488:         Self: Sized,\n  2489:         F: [const] FnMut(B, Self::Item) -> R + [const] Destruct,\n  2490:         R: [const] Try<Output = B>,\n  2491:     {\n  2492:         let mut accum = init;\n  2493:         while let Some(x) = self.next() {\n  2494:             accum = f(accum, x)?;\n  2495:         }\n  2496:         try { accum }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::try_for_each",
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
                            "generic": "R"
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "tuple": []
                                  }
                                }
                              },
                              "name": "Output"
                            }
                          ]
                        }
                      },
                      "id": 12972,
                      "path": "Try"
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
      "name": "try_for_each",
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
          "generic": "R"
        }
      }
    },
    "verification_source": "  2531:     ///\n  2532:     /// ```\n  2533:     /// use std::ops::ControlFlow;\n  2534:     ///\n  2535:     /// let r = (2..100).try_for_each(|x| {\n  2536:     ///     if 323 % x == 0 {\n  2537:     ///         return ControlFlow::Break(x)\n  2538:     ///     }\n  2539:     ///\n  2540:     ///     ControlFlow::Continue(())\n  2541:     /// });\n  2542:     /// assert_eq!(r, ControlFlow::Break(17));\n  2543:     /// ```\n  2544:     #[inline]\n  2545:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n  2546:     #[rustc_non_const_trait_method]\n  2547:     fn try_for_each<F, R>(&mut self, f: F) -> R\n  2548:     where\n  2549:         Self: Sized,\n  2550:         F: FnMut(Self::Item) -> R,\n  2551:         R: Try<Output = ()>,\n  2552:     {\n  2553:         #[inline]\n  2554:         fn call<T, R>(mut f: impl FnMut(T) -> R) -> impl FnMut((), T) -> R {\n  2555:             move |(), x| f(x)\n  2556:         }\n  2557: \n  2558:         self.try_fold((), call(f))\n  2559:     }\n  2560: \n  2561:     /// Folds every element into an accumulator by applying an operation,\n  2562:     /// returning the final result.\n  2563:     ///",
    "nanvix_source": "  2535:     ///         return ControlFlow::Break(x)\n  2536:     ///     }\n  2537:     ///\n  2538:     ///     ControlFlow::Continue(())\n  2539:     /// });\n  2540:     /// assert_eq!(r, ControlFlow::Break(17));\n  2541:     /// ```\n  2542:     #[inline]\n  2543:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n  2544:     #[rustc_non_const_trait_method]\n  2545:     fn try_for_each<F, R>(&mut self, f: F) -> R\n  2546:     where\n  2547:         Self: Sized,\n  2548:         F: FnMut(Self::Item) -> R,\n  2549:         R: Try<Output = ()>,\n  2550:     {\n  2551:         #[inline]\n  2552:         fn call<T, R>(mut f: impl FnMut(T) -> R) -> impl FnMut((), T) -> R {\n  2553:             move |(), x| f(x)\n  2554:         }\n  2555: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::unzip",
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "FromA"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "FromB"
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
                      "id": 70,
                      "path": "Default"
                    }
                  }
                },
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
                                "generic": "A"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 78,
                      "path": "Extend"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "FromA"
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
                      "id": 70,
                      "path": "Default"
                    }
                  }
                },
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
                                "generic": "B"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 78,
                      "path": "Extend"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "FromB"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "tuple": [
                                      {
                                        "generic": "A"
                                      },
                                      {
                                        "generic": "B"
                                      }
                                    ]
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 82,
                      "path": "Iterator"
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
      "name": "unzip",
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
          "tuple": [
            {
              "generic": "FromA"
            },
            {
              "generic": "FromB"
            }
          ]
        }
      }
    },
    "verification_source": "  3466:     ///\n  3467:     /// let (left, right): (Vec<_>, Vec<_>) = a.into_iter().unzip();\n  3468:     ///\n  3469:     /// assert_eq!(left, [1, 3, 5]);\n  3470:     /// assert_eq!(right, [2, 4, 6]);\n  3471:     ///\n  3472:     /// // you can also unzip multiple nested tuples at once\n  3473:     /// let a = [(1, (2, 3)), (4, (5, 6))];\n  3474:     ///\n  3475:     /// let (x, (y, z)): (Vec<_>, (Vec<_>, Vec<_>)) = a.into_iter().unzip();\n  3476:     /// assert_eq!(x, [1, 4]);\n  3477:     /// assert_eq!(y, [2, 5]);\n  3478:     /// assert_eq!(z, [3, 6]);\n  3479:     /// ```\n  3480:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3481:     #[rustc_non_const_trait_method]\n  3482:     fn unzip<A, B, FromA, FromB>(self) -> (FromA, FromB)\n  3483:     where\n  3484:         FromA: Default + Extend<A>,\n  3485:         FromB: Default + Extend<B>,\n  3486:         Self: Sized + Iterator<Item = (A, B)>,\n  3487:     {\n  3488:         let mut unzipped: (FromA, FromB) = Default::default();\n  3489:         unzipped.extend(self);\n  3490:         unzipped\n  3491:     }\n  3492: \n  3493:     /// Creates an iterator which copies all of its elements.\n  3494:     ///\n  3495:     /// This is useful when you have an iterator over `&T`, but you need an\n  3496:     /// iterator over `T`.\n  3497:     ///\n  3498:     /// # Examples",
    "nanvix_source": "  3470:     /// // you can also unzip multiple nested tuples at once\n  3471:     /// let a = [(1, (2, 3)), (4, (5, 6))];\n  3472:     ///\n  3473:     /// let (x, (y, z)): (Vec<_>, (Vec<_>, Vec<_>)) = a.into_iter().unzip();\n  3474:     /// assert_eq!(x, [1, 4]);\n  3475:     /// assert_eq!(y, [2, 5]);\n  3476:     /// assert_eq!(z, [3, 6]);\n  3477:     /// ```\n  3478:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3479:     #[rustc_non_const_trait_method]\n  3480:     fn unzip<A, B, FromA, FromB>(self) -> (FromA, FromB)\n  3481:     where\n  3482:         FromA: Default + Extend<A>,\n  3483:         FromB: Default + Extend<B>,\n  3484:         Self: Sized + Iterator<Item = (A, B)>,\n  3485:     {\n  3486:         let mut unzipped: (FromA, FromB) = Default::default();\n  3487:         unzipped.extend(self);\n  3488:         unzipped\n  3489:     }\n  3490: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::zip",
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
              "generic": "U"
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
                      "qualified_path": {
                        "args": null,
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "U"
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
    "verification_source": "   615:     ///     .into_iter()\n   616:     ///     .map(|x| x * 2)\n   617:     ///     .skip(1)\n   618:     ///     .zip(b.into_iter().map(|x| x * 2).skip(1));\n   619:     /// #\n   620:     /// # assert_eq!(zipped.next(), Some((4, 6)));\n   621:     /// # assert_eq!(zipped.next(), Some((6, 8)));\n   622:     /// # assert_eq!(zipped.next(), None);\n   623:     /// ```\n   624:     ///\n   625:     /// [`enumerate`]: Iterator::enumerate\n   626:     /// [`next`]: Iterator::next\n   627:     /// [`zip`]: crate::iter::zip\n   628:     #[inline]\n   629:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   630:     #[rustc_non_const_trait_method]\n   631:     fn zip<U>(self, other: U) -> Zip<Self, U::IntoIter>\n   632:     where\n   633:         Self: Sized,\n   634:         U: IntoIterator,\n   635:     {\n   636:         Zip::new(self, other.into_iter())\n   637:     }\n   638: \n   639:     /// Creates a new iterator which places a copy of `separator` between items\n   640:     /// of the original iterator.\n   641:     ///\n   642:     /// Specifically on fused iterators, it is guaranteed that the new iterator\n   643:     /// places a copy of `separator` between *adjacent* `Some(_)` items. For non-fused iterators,\n   644:     /// it is guaranteed that [`intersperse`] will create a new iterator that places a copy\n   645:     /// of `separator` between `Some(_)` items, particularly just right before the subsequent\n   646:     /// `Some(_)` item.\n   647:     ///",
    "nanvix_source": "   619:     /// # assert_eq!(zipped.next(), Some((6, 8)));\n   620:     /// # assert_eq!(zipped.next(), None);\n   621:     /// ```\n   622:     ///\n   623:     /// [`enumerate`]: Iterator::enumerate\n   624:     /// [`next`]: Iterator::next\n   625:     /// [`zip`]: crate::iter::zip\n   626:     #[inline]\n   627:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   628:     #[rustc_non_const_trait_method]\n   629:     fn zip<U>(self, other: U) -> Zip<Self, U::IntoIter>\n   630:     where\n   631:         Self: Sized,\n   632:         U: IntoIterator,\n   633:     {\n   634:         Zip::new(self, other.into_iter())\n   635:     }\n   636: \n   637:     /// Creates a new iterator which places a copy of `separator` between items\n   638:     /// of the original iterator.\n   639:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Product::product",
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
                        "args": {
                          "angle_bracketed": {
                            "args": [],
                            "constraints": [
                              {
                                "args": null,
                                "binding": {
                                  "equality": {
                                    "type": {
                                      "generic": "A"
                                    }
                                  }
                                },
                                "name": "Item"
                              }
                            ]
                          }
                        },
                        "id": 82,
                        "path": "Iterator"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
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
        "item_id": "core:4652",
        "kind": "trait",
        "name": "Product",
        "path": [
          "core",
          "iter",
          "traits",
          "accum",
          "Product"
        ]
      },
      "signature": {
        "inputs": [
          [
            "iter",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "    29: /// this trait can be generated by using the [`product()`] method on an iterator.\n    30: /// Like [`FromIterator`], this trait should rarely be called directly.\n    31: ///\n    32: /// [`product()`]: Iterator::product\n    33: /// [`FromIterator`]: iter::FromIterator\n    34: #[stable(feature = \"iter_arith_traits\", since = \"1.12.0\")]\n    35: #[rustc_const_unstable(feature = \"const_iter\", issue = \"92476\")]\n    36: #[diagnostic::on_unimplemented(\n    37:     message = \"a value of type `{Self}` cannot be made by multiplying all elements of type `{A}` from an iterator\",\n    38:     label = \"value of type `{Self}` cannot be made by multiplying all elements from a `std::iter::Iterator<Item={A}>`\"\n    39: )]\n    40: pub const trait Product<A = Self>: Sized {\n    41:     /// Takes an iterator and generates `Self` from the elements by multiplying\n    42:     /// the items.\n    43:     #[stable(feature = \"iter_arith_traits\", since = \"1.12.0\")]\n    44:     fn product<I: Iterator<Item = A>>(iter: I) -> Self;\n    45: }\n    46: \n    47: macro_rules! integer_sum_product {\n    48:     (@impls $zero:expr, $one:expr, #[$attr:meta], $($a:ty)*) => ($(\n    49:         #[$attr]\n    50:         impl Sum for $a {\n    51:             fn sum<I: Iterator<Item=Self>>(iter: I) -> Self {\n    52:                 iter.fold(\n    53:                     $zero,\n    54:                     #[rustc_inherit_overflow_checks]\n    55:                     |a, b| a + b,\n    56:                 )\n    57:             }\n    58:         }\n    59: \n    60:         #[$attr]\n    61:         impl Product for $a {",
    "nanvix_source": "    35: #[rustc_const_unstable(feature = \"const_iter\", issue = \"92476\")]\n    36: #[diagnostic::on_unimplemented(\n    37:     message = \"a value of type `{Self}` cannot be made by multiplying all elements of type `{A}` from an iterator\",\n    38:     label = \"value of type `{Self}` cannot be made by multiplying all elements from a `std::iter::Iterator<Item={A}>`\"\n    39: )]\n    40: pub const trait Product<A = Self>: Sized {\n    41:     /// Takes an iterator and generates `Self` from the elements by multiplying\n    42:     /// the items.\n    43:     #[stable(feature = \"iter_arith_traits\", since = \"1.12.0\")]\n    44:     fn product<I: Iterator<Item = A>>(iter: I) -> Self;\n    45: }\n    46: \n    47: macro_rules! integer_sum_product {\n    48:     (@impls $zero:expr, $one:expr, #[$attr:meta], $($a:ty)*) => ($(\n    49:         #[$attr]\n    50:         impl Sum for $a {\n    51:             fn sum<I: Iterator<Item=Self>>(iter: I) -> Self {\n    52:                 iter.fold(\n    53:                     $zero,\n    54:                     #[rustc_inherit_overflow_checks]\n    55:                     |a, b| a + b,",
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
