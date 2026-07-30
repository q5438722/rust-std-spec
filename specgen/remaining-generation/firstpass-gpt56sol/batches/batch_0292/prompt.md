For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::size_hint",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "size_hint",
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
          "tuple": [
            {
              "primitive": "usize"
            },
            {
              "resolved_path": {
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
                "id": 84,
                "path": "Option"
              }
            }
          ]
        }
      }
    },
    "verification_source": "   173:     ///\n   174:     /// // now both bounds are increased by five\n   175:     /// assert_eq!((5, Some(15)), iter.size_hint());\n   176:     /// ```\n   177:     ///\n   178:     /// Returning `None` for an upper bound:\n   179:     ///\n   180:     /// ```\n   181:     /// // an infinite iterator has no upper bound\n   182:     /// // and the maximum possible lower bound\n   183:     /// let iter = 0..;\n   184:     ///\n   185:     /// assert_eq!((usize::MAX, None), iter.size_hint());\n   186:     /// ```\n   187:     #[inline]\n   188:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   189:     fn size_hint(&self) -> (usize, Option<usize>) {\n   190:         (0, None)\n   191:     }\n   192: \n   193:     /// Consumes the iterator, counting the number of iterations and returning it.\n   194:     ///\n   195:     /// This method will call [`next`] repeatedly until [`None`] is encountered,\n   196:     /// returning the number of times it saw [`Some`]. Note that [`next`] has to be\n   197:     /// called at least once even if the iterator does not have any elements.\n   198:     ///\n   199:     /// [`next`]: Iterator::next\n   200:     ///\n   201:     /// # Overflow Behavior\n   202:     ///\n   203:     /// The method does no guarding against overflows, so counting elements of\n   204:     /// an iterator with more than [`usize::MAX`] elements either produces the\n   205:     /// wrong result or panics. If overflow checks are enabled, a panic is",
    "nanvix_source": "   179:     ///\n   180:     /// ```\n   181:     /// // an infinite iterator has no upper bound\n   182:     /// // and the maximum possible lower bound\n   183:     /// let iter = 0..;\n   184:     ///\n   185:     /// assert_eq!((usize::MAX, None), iter.size_hint());\n   186:     /// ```\n   187:     #[inline]\n   188:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   189:     fn size_hint(&self) -> (usize, Option<usize>) {\n   190:         (0, None)\n   191:     }\n   192: \n   193:     /// Consumes the iterator, counting the number of iterations and returning it.\n   194:     ///\n   195:     /// This method will call [`next`] repeatedly until [`None`] is encountered,\n   196:     /// returning the number of times it saw [`Some`]. Note that [`next`] has to be\n   197:     /// called at least once even if the iterator does not have any elements.\n   198:     ///\n   199:     /// [`next`]: Iterator::next",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::skip",
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "skip",
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
            "n",
            {
              "primitive": "usize"
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
            "id": 9898,
            "path": "Skip"
          }
        }
      }
    },
    "verification_source": "  1361:     /// then the returned iterator is empty.\n  1362:     ///\n  1363:     /// Rather than overriding this method directly, instead override the `nth` method.\n  1364:     ///\n  1365:     /// # Examples\n  1366:     ///\n  1367:     /// ```\n  1368:     /// let a = [1, 2, 3];\n  1369:     ///\n  1370:     /// let mut iter = a.into_iter().skip(2);\n  1371:     ///\n  1372:     /// assert_eq!(iter.next(), Some(3));\n  1373:     /// assert_eq!(iter.next(), None);\n  1374:     /// ```\n  1375:     #[inline]\n  1376:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1377:     fn skip(self, n: usize) -> Skip<Self>\n  1378:     where\n  1379:         Self: Sized,\n  1380:     {\n  1381:         Skip::new(self, n)\n  1382:     }\n  1383: \n  1384:     /// Creates an iterator that yields the first `n` elements, or fewer\n  1385:     /// if the underlying iterator ends sooner.\n  1386:     ///\n  1387:     /// `take(n)` yields elements until `n` elements are yielded or the end of\n  1388:     /// the iterator is reached (whichever happens first).\n  1389:     /// The returned iterator is a prefix of length `n` if the original iterator\n  1390:     /// contains at least `n` elements, otherwise it contains all of the\n  1391:     /// (fewer than `n`) elements of the original iterator.\n  1392:     ///\n  1393:     /// # Examples",
    "nanvix_source": "  1365:     /// ```\n  1366:     /// let a = [1, 2, 3];\n  1367:     ///\n  1368:     /// let mut iter = a.into_iter().skip(2);\n  1369:     ///\n  1370:     /// assert_eq!(iter.next(), Some(3));\n  1371:     /// assert_eq!(iter.next(), None);\n  1372:     /// ```\n  1373:     #[inline]\n  1374:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1375:     fn skip(self, n: usize) -> Skip<Self>\n  1376:     where\n  1377:         Self: Sized,\n  1378:     {\n  1379:         Skip::new(self, n)\n  1380:     }\n  1381: \n  1382:     /// Creates an iterator that yields the first `n` elements, or fewer\n  1383:     /// if the underlying iterator ends sooner.\n  1384:     ///\n  1385:     /// `take(n)` yields elements until `n` elements are yielded or the end of",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::skip_while",
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
      "name": "skip_while",
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
            "id": 9901,
            "path": "SkipWhile"
          }
        }
      }
    },
    "verification_source": "  1166:     /// let a = [-1, 0, 1, -2];\n  1167:     ///\n  1168:     /// let mut iter = a.into_iter().skip_while(|&x| x < 0);\n  1169:     ///\n  1170:     /// assert_eq!(iter.next(), Some(0));\n  1171:     /// assert_eq!(iter.next(), Some(1));\n  1172:     ///\n  1173:     /// // while this would have been false, since we already got a false,\n  1174:     /// // skip_while() isn't used any more\n  1175:     /// assert_eq!(iter.next(), Some(-2));\n  1176:     ///\n  1177:     /// assert_eq!(iter.next(), None);\n  1178:     /// ```\n  1179:     #[inline]\n  1180:     #[doc(alias = \"drop_while\")]\n  1181:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1182:     fn skip_while<P>(self, predicate: P) -> SkipWhile<Self, P>\n  1183:     where\n  1184:         Self: Sized,\n  1185:         P: FnMut(&Self::Item) -> bool,\n  1186:     {\n  1187:         SkipWhile::new(self, predicate)\n  1188:     }\n  1189: \n  1190:     /// Creates an iterator that yields elements based on a predicate.\n  1191:     ///\n  1192:     /// `take_while()` takes a closure as an argument. It will call this\n  1193:     /// closure on each element of the iterator, and yield elements\n  1194:     /// while it returns `true`.\n  1195:     ///\n  1196:     /// After `false` is returned, `take_while()`'s job is over, and the\n  1197:     /// rest of the elements are ignored.\n  1198:     ///",
    "nanvix_source": "  1170:     ///\n  1171:     /// // while this would have been false, since we already got a false,\n  1172:     /// // skip_while() isn't used any more\n  1173:     /// assert_eq!(iter.next(), Some(-2));\n  1174:     ///\n  1175:     /// assert_eq!(iter.next(), None);\n  1176:     /// ```\n  1177:     #[inline]\n  1178:     #[doc(alias = \"drop_while\")]\n  1179:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1180:     fn skip_while<P>(self, predicate: P) -> SkipWhile<Self, P>\n  1181:     where\n  1182:         Self: Sized,\n  1183:         P: FnMut(&Self::Item) -> bool,\n  1184:     {\n  1185:         SkipWhile::new(self, predicate)\n  1186:     }\n  1187: \n  1188:     /// Creates an iterator that yields elements based on a predicate.\n  1189:     ///\n  1190:     /// `take_while()` takes a closure as an argument. It will call this",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::step_by",
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "step_by",
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
            "step",
            {
              "primitive": "usize"
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
            "id": 9904,
            "path": "StepBy"
          }
        }
      }
    },
    "verification_source": "   425:     /// The method will panic if the given step is `0`.\n   426:     ///\n   427:     /// # Examples\n   428:     ///\n   429:     /// ```\n   430:     /// let a = [0, 1, 2, 3, 4, 5];\n   431:     /// let mut iter = a.into_iter().step_by(2);\n   432:     ///\n   433:     /// assert_eq!(iter.next(), Some(0));\n   434:     /// assert_eq!(iter.next(), Some(2));\n   435:     /// assert_eq!(iter.next(), Some(4));\n   436:     /// assert_eq!(iter.next(), None);\n   437:     /// ```\n   438:     #[inline]\n   439:     #[stable(feature = \"iterator_step_by\", since = \"1.28.0\")]\n   440:     #[rustc_non_const_trait_method]\n   441:     fn step_by(self, step: usize) -> StepBy<Self>\n   442:     where\n   443:         Self: Sized,\n   444:     {\n   445:         StepBy::new(self, step)\n   446:     }\n   447: \n   448:     /// Takes two iterators and creates a new iterator over both in sequence.\n   449:     ///\n   450:     /// `chain()` will return a new iterator which will first iterate over\n   451:     /// values from the first iterator and then over values from the second\n   452:     /// iterator.\n   453:     ///\n   454:     /// In other words, it links two iterators together, in a chain. \ud83d\udd17\n   455:     ///\n   456:     /// [`once`] is commonly used to adapt a single value into a chain of\n   457:     /// other kinds of iteration.",
    "nanvix_source": "   429:     /// let mut iter = a.into_iter().step_by(2);\n   430:     ///\n   431:     /// assert_eq!(iter.next(), Some(0));\n   432:     /// assert_eq!(iter.next(), Some(2));\n   433:     /// assert_eq!(iter.next(), Some(4));\n   434:     /// assert_eq!(iter.next(), None);\n   435:     /// ```\n   436:     #[inline]\n   437:     #[stable(feature = \"iterator_step_by\", since = \"1.28.0\")]\n   438:     #[rustc_non_const_trait_method]\n   439:     fn step_by(self, step: usize) -> StepBy<Self>\n   440:     where\n   441:         Self: Sized,\n   442:     {\n   443:         StepBy::new(self, step)\n   444:     }\n   445: \n   446:     /// Takes two iterators and creates a new iterator over both in sequence.\n   447:     ///\n   448:     /// `chain()` will return a new iterator which will first iterate over\n   449:     /// values from the first iterator and then over values from the second",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::sum",
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
            "name": "S"
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
                      "id": 4649,
                      "path": "Sum"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "S"
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
      "name": "sum",
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
          "generic": "S"
        }
      }
    },
    "verification_source": "  3655:     /// method will panic if the computation overflows and overflow checks are\n  3656:     /// enabled.\n  3657:     ///\n  3658:     /// # Examples\n  3659:     ///\n  3660:     /// ```\n  3661:     /// let a = [1, 2, 3];\n  3662:     /// let sum: i32 = a.iter().sum();\n  3663:     ///\n  3664:     /// assert_eq!(sum, 6);\n  3665:     ///\n  3666:     /// let b: Vec<f32> = vec![];\n  3667:     /// let sum: f32 = b.iter().sum();\n  3668:     /// assert_eq!(sum, -0.0_f32);\n  3669:     /// ```\n  3670:     #[stable(feature = \"iter_arith\", since = \"1.11.0\")]\n  3671:     fn sum<S>(self) -> S\n  3672:     where\n  3673:         Self: Sized,\n  3674:         S: [const] Sum<Self::Item>,\n  3675:     {\n  3676:         Sum::sum(self)\n  3677:     }\n  3678: \n  3679:     /// Iterates over the entire iterator, multiplying all the elements\n  3680:     ///\n  3681:     /// An empty iterator returns the one value of the type.\n  3682:     ///\n  3683:     /// `product()` can be used to multiply any type implementing [`Product`][`core::iter::Product`],\n  3684:     /// including [`Option`][`Option::product`] and [`Result`][`Result::product`].\n  3685:     ///\n  3686:     /// # Panics\n  3687:     ///",
    "nanvix_source": "  3659:     /// let a = [1, 2, 3];\n  3660:     /// let sum: i32 = a.iter().sum();\n  3661:     ///\n  3662:     /// assert_eq!(sum, 6);\n  3663:     ///\n  3664:     /// let b: Vec<f32> = vec![];\n  3665:     /// let sum: f32 = b.iter().sum();\n  3666:     /// assert_eq!(sum, -0.0_f32);\n  3667:     /// ```\n  3668:     #[stable(feature = \"iter_arith\", since = \"1.11.0\")]\n  3669:     fn sum<S>(self) -> S\n  3670:     where\n  3671:         Self: Sized,\n  3672:         S: [const] Sum<Self::Item>,\n  3673:     {\n  3674:         Sum::sum(self)\n  3675:     }\n  3676: \n  3677:     /// Iterates over the entire iterator, multiplying all the elements.\n  3678:     ///\n  3679:     /// An empty iterator returns the one value of the type.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::take",
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "take",
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
            "n",
            {
              "primitive": "usize"
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
            "id": 9907,
            "path": "Take"
          }
        }
      }
    },
    "verification_source": "  1433:     /// let mut words = [\"hello\", \"world\", \"of\", \"Rust\"].into_iter();\n  1434:     ///\n  1435:     /// // Take the first two words.\n  1436:     /// let hello_world: Vec<_> = words.by_ref().take(2).collect();\n  1437:     /// assert_eq!(hello_world, vec![\"hello\", \"world\"]);\n  1438:     ///\n  1439:     /// // Collect the rest of the words.\n  1440:     /// // We can only do this because we used `by_ref` earlier.\n  1441:     /// let of_rust: Vec<_> = words.collect();\n  1442:     /// assert_eq!(of_rust, vec![\"of\", \"Rust\"]);\n  1443:     /// ```\n  1444:     ///\n  1445:     /// [`by_ref`]: Iterator::by_ref\n  1446:     #[doc(alias = \"limit\")]\n  1447:     #[inline]\n  1448:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1449:     fn take(self, n: usize) -> Take<Self>\n  1450:     where\n  1451:         Self: Sized,\n  1452:     {\n  1453:         Take::new(self, n)\n  1454:     }\n  1455: \n  1456:     /// An iterator adapter which, like [`fold`], holds internal state, but\n  1457:     /// unlike [`fold`], produces a new iterator.\n  1458:     ///\n  1459:     /// [`fold`]: Iterator::fold\n  1460:     ///\n  1461:     /// `scan()` takes two arguments: an initial value which seeds the internal\n  1462:     /// state, and a closure with two arguments, the first being a mutable\n  1463:     /// reference to the internal state and the second an iterator element.\n  1464:     /// The closure can assign to the internal state to share state between\n  1465:     /// iterations.",
    "nanvix_source": "  1437:     /// // Collect the rest of the words.\n  1438:     /// // We can only do this because we used `by_ref` earlier.\n  1439:     /// let of_rust: Vec<_> = words.collect();\n  1440:     /// assert_eq!(of_rust, vec![\"of\", \"Rust\"]);\n  1441:     /// ```\n  1442:     ///\n  1443:     /// [`by_ref`]: Iterator::by_ref\n  1444:     #[doc(alias = \"limit\")]\n  1445:     #[inline]\n  1446:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1447:     fn take(self, n: usize) -> Take<Self>\n  1448:     where\n  1449:         Self: Sized,\n  1450:     {\n  1451:         Take::new(self, n)\n  1452:     }\n  1453: \n  1454:     /// An iterator adapter which, like [`fold`], holds internal state, but\n  1455:     /// unlike [`fold`], produces a new iterator.\n  1456:     ///\n  1457:     /// [`fold`]: Iterator::fold",
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
