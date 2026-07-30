For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::cloned",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          },
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
                      "id": 42,
                      "path": "Clone"
                    }
                  }
                },
                {
                  "outlives": "'a"
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
                                    "borrowed_ref": {
                                      "is_mutable": false,
                                      "lifetime": "'a",
                                      "type": {
                                        "generic": "T"
                                      }
                                    }
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
      "name": "cloned",
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9844,
            "path": "Cloned"
          }
        }
      }
    },
    "verification_source": "  3545:     /// assert_eq!(v_map, [1, 2, 3]);\n  3546:     /// ```\n  3547:     ///\n  3548:     /// To get the best performance, try to clone late:\n  3549:     ///\n  3550:     /// ```\n  3551:     /// let a = [vec![0_u8, 1, 2], vec![3, 4], vec![23]];\n  3552:     /// // don't do this:\n  3553:     /// let slower: Vec<_> = a.iter().cloned().filter(|s| s.len() == 1).collect();\n  3554:     /// assert_eq!(&[vec![23]], &slower[..]);\n  3555:     /// // instead call `cloned` late\n  3556:     /// let faster: Vec<_> = a.iter().filter(|s| s.len() == 1).cloned().collect();\n  3557:     /// assert_eq!(&[vec![23]], &faster[..]);\n  3558:     /// ```\n  3559:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3560:     #[rustc_diagnostic_item = \"iter_cloned\"]\n  3561:     fn cloned<'a, T>(self) -> Cloned<Self>\n  3562:     where\n  3563:         T: Clone + 'a,\n  3564:         Self: Sized + Iterator<Item = &'a T>,\n  3565:     {\n  3566:         Cloned::new(self)\n  3567:     }\n  3568: \n  3569:     /// Repeats an iterator endlessly.\n  3570:     ///\n  3571:     /// Instead of stopping at [`None`], the iterator will instead start again,\n  3572:     /// from the beginning. After iterating again, it will start at the\n  3573:     /// beginning again. And again. And again. Forever. Note that in case the\n  3574:     /// original iterator is empty, the resulting iterator will also be empty.\n  3575:     ///\n  3576:     /// # Examples\n  3577:     ///",
    "nanvix_source": "  3549:     /// let a = [vec![0_u8, 1, 2], vec![3, 4], vec![23]];\n  3550:     /// // don't do this:\n  3551:     /// let slower: Vec<_> = a.iter().cloned().filter(|s| s.len() == 1).collect();\n  3552:     /// assert_eq!(&[vec![23]], &slower[..]);\n  3553:     /// // instead call `cloned` late\n  3554:     /// let faster: Vec<_> = a.iter().filter(|s| s.len() == 1).cloned().collect();\n  3555:     /// assert_eq!(&[vec![23]], &faster[..]);\n  3556:     /// ```\n  3557:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3558:     #[rustc_diagnostic_item = \"iter_cloned\"]\n  3559:     fn cloned<'a, T>(self) -> Cloned<Self>\n  3560:     where\n  3561:         T: Clone + 'a,\n  3562:         Self: Sized + Iterator<Item = &'a T>,\n  3563:     {\n  3564:         Cloned::new(self)\n  3565:     }\n  3566: \n  3567:     /// Repeats an iterator endlessly.\n  3568:     ///\n  3569:     /// Instead of stopping at [`None`], the iterator will instead start again,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::cmp",
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
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
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
                              "name": "Item"
                            }
                          ]
                        }
                      },
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
      "name": "cmp",
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
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        }
      }
    },
    "verification_source": "  3709:     }\n  3710: \n  3711:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3712:     /// of another.\n  3713:     ///\n  3714:     /// # Examples\n  3715:     ///\n  3716:     /// ```\n  3717:     /// use std::cmp::Ordering;\n  3718:     ///\n  3719:     /// assert_eq!([1].iter().cmp([1].iter()), Ordering::Equal);\n  3720:     /// assert_eq!([1].iter().cmp([1, 2].iter()), Ordering::Less);\n  3721:     /// assert_eq!([1, 2].iter().cmp([1].iter()), Ordering::Greater);\n  3722:     /// ```\n  3723:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3724:     #[rustc_non_const_trait_method]\n  3725:     fn cmp<I>(self, other: I) -> Ordering\n  3726:     where\n  3727:         I: IntoIterator<Item = Self::Item>,\n  3728:         Self::Item: Ord,\n  3729:         Self: Sized,\n  3730:     {\n  3731:         self.cmp_by(other, |x, y| x.cmp(&y))\n  3732:     }\n  3733: \n  3734:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3735:     /// of another with respect to the specified comparison function.\n  3736:     ///\n  3737:     /// # Examples\n  3738:     ///\n  3739:     /// ```\n  3740:     /// #![feature(iter_order_by)]\n  3741:     ///",
    "nanvix_source": "  3713:     ///\n  3714:     /// ```\n  3715:     /// use std::cmp::Ordering;\n  3716:     ///\n  3717:     /// assert_eq!([1].iter().cmp([1].iter()), Ordering::Equal);\n  3718:     /// assert_eq!([1].iter().cmp([1, 2].iter()), Ordering::Less);\n  3719:     /// assert_eq!([1, 2].iter().cmp([1].iter()), Ordering::Greater);\n  3720:     /// ```\n  3721:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3722:     #[rustc_non_const_trait_method]\n  3723:     fn cmp<I>(self, other: I) -> Ordering\n  3724:     where\n  3725:         I: IntoIterator<Item = Self::Item>,\n  3726:         Self::Item: Ord,\n  3727:         Self: Sized,\n  3728:     {\n  3729:         self.cmp_by(other, |x, y| x.cmp(&y))\n  3730:     }\n  3731: \n  3732:     /// [Lexicographically](Ord#lexicographical-comparison) compares the elements of this [`Iterator`] with those\n  3733:     /// of another with respect to the specified comparison function.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::copied",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          },
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
                      "id": 6,
                      "path": "Copy"
                    }
                  }
                },
                {
                  "outlives": "'a"
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
                                    "borrowed_ref": {
                                      "is_mutable": false,
                                      "lifetime": "'a",
                                      "type": {
                                        "generic": "T"
                                      }
                                    }
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
      "name": "copied",
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9847,
            "path": "Copied"
          }
        }
      }
    },
    "verification_source": "  3497:     ///\n  3498:     /// # Examples\n  3499:     ///\n  3500:     /// ```\n  3501:     /// let a = [1, 2, 3];\n  3502:     ///\n  3503:     /// let v_copied: Vec<_> = a.iter().copied().collect();\n  3504:     ///\n  3505:     /// // copied is the same as .map(|&x| x)\n  3506:     /// let v_map: Vec<_> = a.iter().map(|&x| x).collect();\n  3507:     ///\n  3508:     /// assert_eq!(v_copied, [1, 2, 3]);\n  3509:     /// assert_eq!(v_map, [1, 2, 3]);\n  3510:     /// ```\n  3511:     #[stable(feature = \"iter_copied\", since = \"1.36.0\")]\n  3512:     #[rustc_diagnostic_item = \"iter_copied\"]\n  3513:     fn copied<'a, T>(self) -> Copied<Self>\n  3514:     where\n  3515:         T: Copy + 'a,\n  3516:         Self: Sized + Iterator<Item = &'a T>,\n  3517:     {\n  3518:         Copied::new(self)\n  3519:     }\n  3520: \n  3521:     /// Creates an iterator which [`clone`]s all of its elements.\n  3522:     ///\n  3523:     /// This is useful when you have an iterator over `&T`, but you need an\n  3524:     /// iterator over `T`.\n  3525:     ///\n  3526:     /// There is no guarantee whatsoever about the `clone` method actually\n  3527:     /// being called *or* optimized away. So code should not depend on\n  3528:     /// either.\n  3529:     ///",
    "nanvix_source": "  3501:     /// let v_copied: Vec<_> = a.iter().copied().collect();\n  3502:     ///\n  3503:     /// // copied is the same as .map(|&x| x)\n  3504:     /// let v_map: Vec<_> = a.iter().map(|&x| x).collect();\n  3505:     ///\n  3506:     /// assert_eq!(v_copied, [1, 2, 3]);\n  3507:     /// assert_eq!(v_map, [1, 2, 3]);\n  3508:     /// ```\n  3509:     #[stable(feature = \"iter_copied\", since = \"1.36.0\")]\n  3510:     #[rustc_diagnostic_item = \"iter_copied\"]\n  3511:     fn copied<'a, T>(self) -> Copied<Self>\n  3512:     where\n  3513:         T: Copy + 'a,\n  3514:         Self: Sized + Iterator<Item = &'a T>,\n  3515:     {\n  3516:         Copied::new(self)\n  3517:     }\n  3518: \n  3519:     /// Creates an iterator which [`clone`]s all of its elements.\n  3520:     ///\n  3521:     /// This is useful when you have an iterator over `&T`, but you need an",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::count",
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
              "bounds": [],
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
      "name": "count",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   208:     /// # Panics\n   209:     ///\n   210:     /// This function might panic if the iterator has more than [`usize::MAX`]\n   211:     /// elements.\n   212:     ///\n   213:     /// # Examples\n   214:     ///\n   215:     /// ```\n   216:     /// let a = [1, 2, 3];\n   217:     /// assert_eq!(a.iter().count(), 3);\n   218:     ///\n   219:     /// let a = [1, 2, 3, 4, 5];\n   220:     /// assert_eq!(a.iter().count(), 5);\n   221:     /// ```\n   222:     #[inline]\n   223:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   224:     fn count(self) -> usize\n   225:     where\n   226:         Self: Sized + [const] Destruct,\n   227:         Self::Item: [const] Destruct,\n   228:     {\n   229:         // FIXME(const-hack): revert this to a const closure\n   230:         #[rustc_const_unstable(feature = \"const_iter\", issue = \"92476\")]\n   231:         #[rustc_inherit_overflow_checks]\n   232:         const fn plus_one<T: [const] Destruct>(accum: usize, _elem: T) -> usize {\n   233:             accum + 1\n   234:         }\n   235:         self.fold(0, plus_one)\n   236:     }\n   237: \n   238:     /// Consumes the iterator, returning the last element.\n   239:     ///\n   240:     /// This method will evaluate the iterator until it returns [`None`]. While",
    "nanvix_source": "   214:     ///\n   215:     /// ```\n   216:     /// let a = [1, 2, 3];\n   217:     /// assert_eq!(a.iter().count(), 3);\n   218:     ///\n   219:     /// let a = [1, 2, 3, 4, 5];\n   220:     /// assert_eq!(a.iter().count(), 5);\n   221:     /// ```\n   222:     #[inline]\n   223:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   224:     fn count(self) -> usize\n   225:     where\n   226:         Self: Sized + [const] Destruct,\n   227:         Self::Item: [const] Destruct,\n   228:     {\n   229:         self.fold(\n   230:             0,\n   231:             #[rustc_inherit_overflow_checks]\n   232:             const |accum, _elem| accum + 1,\n   233:         )\n   234:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::cycle",
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
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 42,
                      "path": "Clone"
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
      "name": "cycle",
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9850,
            "path": "Cycle"
          }
        }
      }
    },
    "verification_source": "  3576:     /// # Examples\n  3577:     ///\n  3578:     /// ```\n  3579:     /// let a = [1, 2, 3];\n  3580:     ///\n  3581:     /// let mut iter = a.into_iter().cycle();\n  3582:     ///\n  3583:     /// loop {\n  3584:     ///     assert_eq!(iter.next(), Some(1));\n  3585:     ///     assert_eq!(iter.next(), Some(2));\n  3586:     ///     assert_eq!(iter.next(), Some(3));\n  3587:     /// #   break;\n  3588:     /// }\n  3589:     /// ```\n  3590:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3591:     #[inline]\n  3592:     fn cycle(self) -> Cycle<Self>\n  3593:     where\n  3594:         Self: Sized + [const] Clone,\n  3595:     {\n  3596:         Cycle::new(self)\n  3597:     }\n  3598: \n  3599:     /// Returns an iterator over `N` elements of the iterator at a time.\n  3600:     ///\n  3601:     /// The chunks do not overlap. If `N` does not divide the length of the\n  3602:     /// iterator, then the last up to `N-1` elements will be omitted and can be\n  3603:     /// retrieved from the [`.into_remainder()`][ArrayChunks::into_remainder]\n  3604:     /// function of the iterator.\n  3605:     ///\n  3606:     /// # Panics\n  3607:     ///\n  3608:     /// Panics if `N` is zero.",
    "nanvix_source": "  3580:     ///\n  3581:     /// loop {\n  3582:     ///     assert_eq!(iter.next(), Some(1));\n  3583:     ///     assert_eq!(iter.next(), Some(2));\n  3584:     ///     assert_eq!(iter.next(), Some(3));\n  3585:     /// #   break;\n  3586:     /// }\n  3587:     /// ```\n  3588:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3589:     #[inline]\n  3590:     fn cycle(self) -> Cycle<Self>\n  3591:     where\n  3592:         Self: Sized + [const] Clone,\n  3593:     {\n  3594:         Cycle::new(self)\n  3595:     }\n  3596: \n  3597:     /// Returns an iterator over `N` elements of the iterator at a time.\n  3598:     ///\n  3599:     /// The chunks do not overlap. If `N` does not divide the length of the\n  3600:     /// iterator, then the last up to `N-1` elements will be omitted and can be",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::enumerate",
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
      "name": "enumerate",
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9853,
            "path": "Enumerate"
          }
        }
      }
    },
    "verification_source": "  1030:     ///\n  1031:     /// # Examples\n  1032:     ///\n  1033:     /// ```\n  1034:     /// let a = ['a', 'b', 'c'];\n  1035:     ///\n  1036:     /// let mut iter = a.into_iter().enumerate();\n  1037:     ///\n  1038:     /// assert_eq!(iter.next(), Some((0, 'a')));\n  1039:     /// assert_eq!(iter.next(), Some((1, 'b')));\n  1040:     /// assert_eq!(iter.next(), Some((2, 'c')));\n  1041:     /// assert_eq!(iter.next(), None);\n  1042:     /// ```\n  1043:     #[inline]\n  1044:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1045:     #[rustc_diagnostic_item = \"enumerate_method\"]\n  1046:     fn enumerate(self) -> Enumerate<Self>\n  1047:     where\n  1048:         Self: Sized,\n  1049:     {\n  1050:         Enumerate::new(self)\n  1051:     }\n  1052: \n  1053:     /// Creates an iterator which can use the [`peek`] and [`peek_mut`] methods\n  1054:     /// to look at the next element of the iterator without consuming it. See\n  1055:     /// their documentation for more information.\n  1056:     ///\n  1057:     /// Note that the underlying iterator is still advanced when [`peek`] or\n  1058:     /// [`peek_mut`] are called for the first time: In order to retrieve the\n  1059:     /// next element, [`next`] is called on the underlying iterator, hence any\n  1060:     /// side effects (i.e. anything other than fetching the next value) of\n  1061:     /// the [`next`] method will occur.\n  1062:     ///",
    "nanvix_source": "  1034:     /// let mut iter = a.into_iter().enumerate();\n  1035:     ///\n  1036:     /// assert_eq!(iter.next(), Some((0, 'a')));\n  1037:     /// assert_eq!(iter.next(), Some((1, 'b')));\n  1038:     /// assert_eq!(iter.next(), Some((2, 'c')));\n  1039:     /// assert_eq!(iter.next(), None);\n  1040:     /// ```\n  1041:     #[inline]\n  1042:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1043:     #[rustc_diagnostic_item = \"enumerate_method\"]\n  1044:     fn enumerate(self) -> Enumerate<Self>\n  1045:     where\n  1046:         Self: Sized,\n  1047:     {\n  1048:         Enumerate::new(self)\n  1049:     }\n  1050: \n  1051:     /// Creates an iterator which can use the [`peek`] and [`peek_mut`] methods\n  1052:     /// to look at the next element of the iterator without consuming it. See\n  1053:     /// their documentation for more information.\n  1054:     ///",
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
