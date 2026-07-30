For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::min_by",
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
      "name": "min_by",
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
    "verification_source": "  3392: \n  3393:     /// Returns the element that gives the minimum value with respect to the\n  3394:     /// specified comparison function.\n  3395:     ///\n  3396:     /// If several elements are equally minimum, the first element is\n  3397:     /// returned. If the iterator is empty, [`None`] is returned.\n  3398:     ///\n  3399:     /// # Examples\n  3400:     ///\n  3401:     /// ```\n  3402:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3403:     /// assert_eq!(a.into_iter().min_by(|x, y| x.cmp(y)).unwrap(), -10);\n  3404:     /// ```\n  3405:     #[inline]\n  3406:     #[stable(feature = \"iter_min_by\", since = \"1.15.0\")]\n  3407:     #[rustc_non_const_trait_method]\n  3408:     fn min_by<F>(self, compare: F) -> Option<Self::Item>\n  3409:     where\n  3410:         Self: Sized,\n  3411:         F: FnMut(&Self::Item, &Self::Item) -> Ordering,\n  3412:     {\n  3413:         #[inline]\n  3414:         fn fold<T>(mut compare: impl FnMut(&T, &T) -> Ordering) -> impl FnMut(T, T) -> T {\n  3415:             move |x, y| cmp::min_by(x, y, &mut compare)\n  3416:         }\n  3417: \n  3418:         self.reduce(fold(compare))\n  3419:     }\n  3420: \n  3421:     /// Reverses an iterator's direction.\n  3422:     ///\n  3423:     /// Usually, iterators iterate from left to right. After using `rev()`,\n  3424:     /// an iterator will instead iterate from right to left.",
    "nanvix_source": "  3396:     ///\n  3397:     /// # Examples\n  3398:     ///\n  3399:     /// ```\n  3400:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3401:     /// assert_eq!(a.into_iter().min_by(|x, y| x.cmp(y)).unwrap(), -10);\n  3402:     /// ```\n  3403:     #[inline]\n  3404:     #[stable(feature = \"iter_min_by\", since = \"1.15.0\")]\n  3405:     #[rustc_non_const_trait_method]\n  3406:     fn min_by<F>(self, compare: F) -> Option<Self::Item>\n  3407:     where\n  3408:         Self: Sized,\n  3409:         F: FnMut(&Self::Item, &Self::Item) -> Ordering,\n  3410:     {\n  3411:         #[inline]\n  3412:         fn fold<T>(mut compare: impl FnMut(&T, &T) -> Ordering) -> impl FnMut(T, T) -> T {\n  3413:             move |x, y| cmp::min_by(x, y, &mut compare)\n  3414:         }\n  3415: \n  3416:         self.reduce(fold(compare))",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::min_by_key",
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
      "name": "min_by_key",
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
    "verification_source": "  3358: \n  3359:     /// Returns the element that gives the minimum value from the\n  3360:     /// specified function.\n  3361:     ///\n  3362:     /// If several elements are equally minimum, the first element is\n  3363:     /// returned. If the iterator is empty, [`None`] is returned.\n  3364:     ///\n  3365:     /// # Examples\n  3366:     ///\n  3367:     /// ```\n  3368:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3369:     /// assert_eq!(a.into_iter().min_by_key(|x| x.abs()).unwrap(), 0);\n  3370:     /// ```\n  3371:     #[inline]\n  3372:     #[stable(feature = \"iter_cmp_by_key\", since = \"1.6.0\")]\n  3373:     #[rustc_non_const_trait_method]\n  3374:     fn min_by_key<B: Ord, F>(self, f: F) -> Option<Self::Item>\n  3375:     where\n  3376:         Self: Sized,\n  3377:         F: FnMut(&Self::Item) -> B,\n  3378:     {\n  3379:         #[inline]\n  3380:         fn key<T, B>(mut f: impl FnMut(&T) -> B) -> impl FnMut(T) -> (B, T) {\n  3381:             move |x| (f(&x), x)\n  3382:         }\n  3383: \n  3384:         #[inline]\n  3385:         fn compare<T, B: Ord>((x_p, _): &(B, T), (y_p, _): &(B, T)) -> Ordering {\n  3386:             x_p.cmp(y_p)\n  3387:         }\n  3388: \n  3389:         let (_, x) = self.map(key(f)).min_by(compare)?;\n  3390:         Some(x)",
    "nanvix_source": "  3362:     ///\n  3363:     /// # Examples\n  3364:     ///\n  3365:     /// ```\n  3366:     /// let a = [-3_i32, 0, 1, 5, -10];\n  3367:     /// assert_eq!(a.into_iter().min_by_key(|x| x.abs()).unwrap(), 0);\n  3368:     /// ```\n  3369:     #[inline]\n  3370:     #[stable(feature = \"iter_cmp_by_key\", since = \"1.6.0\")]\n  3371:     #[rustc_non_const_trait_method]\n  3372:     fn min_by_key<B: Ord, F>(self, f: F) -> Option<Self::Item>\n  3373:     where\n  3374:         Self: Sized,\n  3375:         F: FnMut(&Self::Item) -> B,\n  3376:     {\n  3377:         #[inline]\n  3378:         fn key<T, B>(mut f: impl FnMut(&T) -> B) -> impl FnMut(T) -> (B, T) {\n  3379:             move |x| (f(&x), x)\n  3380:         }\n  3381: \n  3382:         #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::ne",
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
            "name": "I"
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
                "generic": "I"
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
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
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
                      "id": 54,
                      "path": "PartialEq"
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
      "name": "ne",
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
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  3919:         }\n  3920: \n  3921:         SpecIterEq::spec_iter_eq(self, other.into_iter(), compare(eq))\n  3922:     }\n  3923: \n  3924:     /// Determines if the elements of this [`Iterator`] are not equal to those of\n  3925:     /// another.\n  3926:     ///\n  3927:     /// # Examples\n  3928:     ///\n  3929:     /// ```\n  3930:     /// assert_eq!([1].iter().ne([1].iter()), false);\n  3931:     /// assert_eq!([1].iter().ne([1, 2].iter()), true);\n  3932:     /// ```\n  3933:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3934:     #[rustc_non_const_trait_method]\n  3935:     fn ne<I>(self, other: I) -> bool\n  3936:     where\n  3937:         I: IntoIterator,\n  3938:         Self::Item: PartialEq<I::Item>,\n  3939:         Self: Sized,\n  3940:     {\n  3941:         !self.eq(other)\n  3942:     }\n  3943: \n  3944:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3945:     /// less than those of another.\n  3946:     ///\n  3947:     /// # Examples\n  3948:     ///\n  3949:     /// ```\n  3950:     /// assert_eq!([1].iter().lt([1].iter()), false);\n  3951:     /// assert_eq!([1].iter().lt([1, 2].iter()), true);",
    "nanvix_source": "  3923:     /// another.\n  3924:     ///\n  3925:     /// # Examples\n  3926:     ///\n  3927:     /// ```\n  3928:     /// assert_eq!([1].iter().ne([1].iter()), false);\n  3929:     /// assert_eq!([1].iter().ne([1, 2].iter()), true);\n  3930:     /// ```\n  3931:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3932:     #[rustc_non_const_trait_method]\n  3933:     fn ne<I>(self, other: I) -> bool\n  3934:     where\n  3935:         I: IntoIterator,\n  3936:         Self::Item: PartialEq<I::Item>,\n  3937:         Self: Sized,\n  3938:     {\n  3939:         !self.eq(other)\n  3940:     }\n  3941: \n  3942:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3943:     /// less than those of another.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::nth",
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
      "name": "nth",
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
    "verification_source": "   374:     ///\n   375:     /// let mut iter = a.into_iter();\n   376:     ///\n   377:     /// assert_eq!(iter.nth(1), Some(2));\n   378:     /// assert_eq!(iter.nth(1), None);\n   379:     /// ```\n   380:     ///\n   381:     /// Returning `None` if there are less than `n + 1` elements:\n   382:     ///\n   383:     /// ```\n   384:     /// let a = [1, 2, 3];\n   385:     /// assert_eq!(a.into_iter().nth(10), None);\n   386:     /// ```\n   387:     #[inline]\n   388:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   389:     #[rustc_non_const_trait_method]\n   390:     fn nth(&mut self, n: usize) -> Option<Self::Item> {\n   391:         self.advance_by(n).ok()?;\n   392:         self.next()\n   393:     }\n   394: \n   395:     /// Creates an iterator starting at the same point, but stepping by\n   396:     /// the given amount at each iteration.\n   397:     ///\n   398:     /// Note 1: The first element of the iterator will always be returned,\n   399:     /// regardless of the step given.\n   400:     ///\n   401:     /// Note 2: The time at which ignored elements are pulled is not fixed.\n   402:     /// `StepBy` behaves like the sequence `self.next()`, `self.nth(step-1)`,\n   403:     /// `self.nth(step-1)`, \u2026, but is also free to behave like the sequence\n   404:     /// `advance_n_and_return_first(&mut self, step)`,\n   405:     /// `advance_n_and_return_first(&mut self, step)`, \u2026\n   406:     /// Which way is used may change for some iterators for performance reasons.",
    "nanvix_source": "   378:     ///\n   379:     /// Returning `None` if there are less than `n + 1` elements:\n   380:     ///\n   381:     /// ```\n   382:     /// let a = [1, 2, 3];\n   383:     /// assert_eq!(a.into_iter().nth(10), None);\n   384:     /// ```\n   385:     #[inline]\n   386:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   387:     #[rustc_non_const_trait_method]\n   388:     fn nth(&mut self, n: usize) -> Option<Self::Item> {\n   389:         self.advance_by(n).ok()?;\n   390:         self.next()\n   391:     }\n   392: \n   393:     /// Creates an iterator starting at the same point, but stepping by\n   394:     /// the given amount at each iteration.\n   395:     ///\n   396:     /// Note 1: The first element of the iterator will always be returned,\n   397:     /// regardless of the step given.\n   398:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::partial_cmp",
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
            "name": "I"
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
                "generic": "I"
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
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
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
                      "id": 58,
                      "path": "PartialOrd"
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
      "name": "partial_cmp",
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
              "generic": "I"
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
                        "args": null,
                        "id": 1682,
                        "path": "Ordering"
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
    "verification_source": "  3794:     /// ```\n  3795:     /// assert_eq!([f64::NAN].iter().partial_cmp([1.].iter()), None);\n  3796:     /// ```\n  3797:     ///\n  3798:     /// The results are determined by the order of evaluation.\n  3799:     ///\n  3800:     /// ```\n  3801:     /// use std::cmp::Ordering;\n  3802:     ///\n  3803:     /// assert_eq!([1.0, f64::NAN].iter().partial_cmp([2.0, f64::NAN].iter()), Some(Ordering::Less));\n  3804:     /// assert_eq!([2.0, f64::NAN].iter().partial_cmp([1.0, f64::NAN].iter()), Some(Ordering::Greater));\n  3805:     /// assert_eq!([f64::NAN, 1.0].iter().partial_cmp([f64::NAN, 2.0].iter()), None);\n  3806:     /// ```\n  3807:     ///\n  3808:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3809:     #[rustc_non_const_trait_method]\n  3810:     fn partial_cmp<I>(self, other: I) -> Option<Ordering>\n  3811:     where\n  3812:         I: IntoIterator,\n  3813:         Self::Item: PartialOrd<I::Item>,\n  3814:         Self: Sized,\n  3815:     {\n  3816:         self.partial_cmp_by(other, |x, y| x.partial_cmp(&y))\n  3817:     }\n  3818: \n  3819:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3820:     /// of another with respect to the specified comparison function.\n  3821:     ///\n  3822:     /// # Examples\n  3823:     ///\n  3824:     /// ```\n  3825:     /// #![feature(iter_order_by)]\n  3826:     ///",
    "nanvix_source": "  3798:     /// ```\n  3799:     /// use std::cmp::Ordering;\n  3800:     ///\n  3801:     /// assert_eq!([1.0, f64::NAN].iter().partial_cmp([2.0, f64::NAN].iter()), Some(Ordering::Less));\n  3802:     /// assert_eq!([2.0, f64::NAN].iter().partial_cmp([1.0, f64::NAN].iter()), Some(Ordering::Greater));\n  3803:     /// assert_eq!([f64::NAN, 1.0].iter().partial_cmp([f64::NAN, 2.0].iter()), None);\n  3804:     /// ```\n  3805:     ///\n  3806:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3807:     #[rustc_non_const_trait_method]\n  3808:     fn partial_cmp<I>(self, other: I) -> Option<Ordering>\n  3809:     where\n  3810:         I: IntoIterator,\n  3811:         Self::Item: PartialOrd<I::Item>,\n  3812:         Self: Sized,\n  3813:     {\n  3814:         self.partial_cmp_by(other, |x, y| x.partial_cmp(&y))\n  3815:     }\n  3816: \n  3817:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3818:     /// of another with respect to the specified comparison function.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::partition",
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
                      "id": 78,
                      "path": "Extend"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "B"
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
      "name": "partition",
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
          "tuple": [
            {
              "generic": "B"
            },
            {
              "generic": "B"
            }
          ]
        }
      }
    },
    "verification_source": "  2257:     /// [`partition_in_place()`]: Iterator::partition_in_place\n  2258:     ///\n  2259:     /// # Examples\n  2260:     ///\n  2261:     /// ```\n  2262:     /// let a = [1, 2, 3];\n  2263:     ///\n  2264:     /// let (even, odd): (Vec<_>, Vec<_>) = a\n  2265:     ///     .into_iter()\n  2266:     ///     .partition(|n| n % 2 == 0);\n  2267:     ///\n  2268:     /// assert_eq!(even, [2]);\n  2269:     /// assert_eq!(odd, [1, 3]);\n  2270:     /// ```\n  2271:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2272:     #[rustc_non_const_trait_method]\n  2273:     fn partition<B, F>(self, f: F) -> (B, B)\n  2274:     where\n  2275:         Self: Sized,\n  2276:         B: Default + Extend<Self::Item>,\n  2277:         F: FnMut(&Self::Item) -> bool,\n  2278:     {\n  2279:         #[inline]\n  2280:         fn extend<'a, T, B: Extend<T>>(\n  2281:             mut f: impl FnMut(&T) -> bool + 'a,\n  2282:             left: &'a mut B,\n  2283:             right: &'a mut B,\n  2284:         ) -> impl FnMut((), T) + 'a {\n  2285:             move |(), x| {\n  2286:                 if f(&x) {\n  2287:                     left.extend_one(x);\n  2288:                 } else {\n  2289:                     right.extend_one(x);",
    "nanvix_source": "  2261:     ///\n  2262:     /// let (even, odd): (Vec<_>, Vec<_>) = a\n  2263:     ///     .into_iter()\n  2264:     ///     .partition(|n| n % 2 == 0);\n  2265:     ///\n  2266:     /// assert_eq!(even, [2]);\n  2267:     /// assert_eq!(odd, [1, 3]);\n  2268:     /// ```\n  2269:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2270:     #[rustc_non_const_trait_method]\n  2271:     fn partition<B, F>(self, f: F) -> (B, B)\n  2272:     where\n  2273:         Self: Sized,\n  2274:         B: Default + Extend<Self::Item>,\n  2275:         F: FnMut(&Self::Item) -> bool,\n  2276:     {\n  2277:         #[inline]\n  2278:         fn extend<'a, T, B: Extend<T>>(\n  2279:             mut f: impl FnMut(&T) -> bool + 'a,\n  2280:             left: &'a mut B,\n  2281:             right: &'a mut B,",
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
