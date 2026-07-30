For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Result::ok",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
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
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
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
      "name": "ok",
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
    "verification_source": "   692:     /// Converts `self` into an [`Option<T>`], consuming `self`,\n   693:     /// and converting the error to `None`, if any.\n   694:     ///\n   695:     /// # Examples\n   696:     ///\n   697:     /// ```\n   698:     /// let x: Result<u32, &str> = Ok(2);\n   699:     /// assert_eq!(x.ok(), Some(2));\n   700:     ///\n   701:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   702:     /// assert_eq!(x.ok(), None);\n   703:     /// ```\n   704:     #[inline]\n   705:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   706:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   707:     #[rustc_diagnostic_item = \"result_ok_method\"]\n   708:     pub const fn ok(self) -> Option<T>\n   709:     where\n   710:         T: [const] Destruct,\n   711:         E: [const] Destruct,\n   712:     {\n   713:         match self {\n   714:             Ok(x) => Some(x),\n   715:             Err(_) => None,\n   716:         }\n   717:     }\n   718: \n   719:     /// Converts from `Result<T, E>` to [`Option<E>`].\n   720:     ///\n   721:     /// Converts `self` into an [`Option<E>`], consuming `self`,\n   722:     /// and discarding the success value, if any.\n   723:     ///\n   724:     /// # Examples",
    "nanvix_source": "   698:     /// let x: Result<u32, &str> = Ok(2);\n   699:     /// assert_eq!(x.ok(), Some(2));\n   700:     ///\n   701:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   702:     /// assert_eq!(x.ok(), None);\n   703:     /// ```\n   704:     #[inline]\n   705:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   706:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   707:     #[rustc_diagnostic_item = \"result_ok_method\"]\n   708:     pub const fn ok(self) -> Option<T>\n   709:     where\n   710:         T: [const] Destruct,\n   711:         E: [const] Destruct,\n   712:     {\n   713:         match self {\n   714:             Ok(x) => Some(x),\n   715:             Err(_) => None,\n   716:         }\n   717:     }\n   718: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::or",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "or",
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
              "generic": "Self"
            }
          ],
          [
            "res",
            {
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
                "id": 90,
                "path": "Result"
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1512:     ///\n  1513:     /// let x: Result<u32, &str> = Err(\"early error\");\n  1514:     /// let y: Result<u32, &str> = Ok(2);\n  1515:     /// assert_eq!(x.or(y), Ok(2));\n  1516:     ///\n  1517:     /// let x: Result<u32, &str> = Err(\"not a 2\");\n  1518:     /// let y: Result<u32, &str> = Err(\"late error\");\n  1519:     /// assert_eq!(x.or(y), Err(\"late error\"));\n  1520:     ///\n  1521:     /// let x: Result<u32, &str> = Ok(2);\n  1522:     /// let y: Result<u32, &str> = Ok(100);\n  1523:     /// assert_eq!(x.or(y), Ok(2));\n  1524:     /// ```\n  1525:     #[inline]\n  1526:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1527:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1528:     pub const fn or<F>(self, res: Result<T, F>) -> Result<T, F>\n  1529:     where\n  1530:         T: [const] Destruct,\n  1531:         E: [const] Destruct,\n  1532:         F: [const] Destruct,\n  1533:     {\n  1534:         match self {\n  1535:             Ok(v) => Ok(v),\n  1536:             Err(_) => res,\n  1537:         }\n  1538:     }\n  1539: \n  1540:     /// Calls `op` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.\n  1541:     ///\n  1542:     /// This function can be used for control flow based on result values.\n  1543:     ///\n  1544:     ///",
    "nanvix_source": "  1516:     /// let y: Result<u32, &str> = Err(\"late error\");\n  1517:     /// assert_eq!(x.or(y), Err(\"late error\"));\n  1518:     ///\n  1519:     /// let x: Result<u32, &str> = Ok(2);\n  1520:     /// let y: Result<u32, &str> = Ok(100);\n  1521:     /// assert_eq!(x.or(y), Ok(2));\n  1522:     /// ```\n  1523:     #[inline]\n  1524:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1525:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1526:     pub const fn or<F>(self, res: Result<T, F>) -> Result<T, F>\n  1527:     where\n  1528:         T: [const] Destruct,\n  1529:         E: [const] Destruct,\n  1530:         F: [const] Destruct,\n  1531:     {\n  1532:         match self {\n  1533:             Ok(v) => Ok(v),\n  1534:             Err(_) => res,\n  1535:         }\n  1536:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::or_else",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "O"
          }
        ],
        "where_predicates": [
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
                              "generic": "E"
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
                              "id": 90,
                              "path": "Result"
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
              "generic_params": [],
              "type": {
                "generic": "O"
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
      "name": "or_else",
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
              "generic": "Self"
            }
          ],
          [
            "op",
            {
              "generic": "O"
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1543:     ///\n  1544:     ///\n  1545:     /// # Examples\n  1546:     ///\n  1547:     /// ```\n  1548:     /// fn sq(x: u32) -> Result<u32, u32> { Ok(x * x) }\n  1549:     /// fn err(x: u32) -> Result<u32, u32> { Err(x) }\n  1550:     ///\n  1551:     /// assert_eq!(Ok(2).or_else(sq).or_else(sq), Ok(2));\n  1552:     /// assert_eq!(Ok(2).or_else(err).or_else(sq), Ok(2));\n  1553:     /// assert_eq!(Err(3).or_else(sq).or_else(err), Ok(9));\n  1554:     /// assert_eq!(Err(3).or_else(err).or_else(err), Err(3));\n  1555:     /// ```\n  1556:     #[inline]\n  1557:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1558:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1559:     pub const fn or_else<F, O>(self, op: O) -> Result<T, F>\n  1560:     where\n  1561:         O: [const] FnOnce(E) -> Result<T, F> + [const] Destruct,\n  1562:     {\n  1563:         match self {\n  1564:             Ok(t) => Ok(t),\n  1565:             Err(e) => op(e),\n  1566:         }\n  1567:     }\n  1568: \n  1569:     /// Returns the contained [`Ok`] value or a provided default.\n  1570:     ///\n  1571:     /// Arguments passed to `unwrap_or` are eagerly evaluated; if you are passing\n  1572:     /// the result of a function call, it is recommended to use [`unwrap_or_else`],\n  1573:     /// which is lazily evaluated.\n  1574:     ///\n  1575:     /// [`unwrap_or_else`]: Result::unwrap_or_else",
    "nanvix_source": "  1547:     /// fn err(x: u32) -> Result<u32, u32> { Err(x) }\n  1548:     ///\n  1549:     /// assert_eq!(Ok(2).or_else(sq).or_else(sq), Ok(2));\n  1550:     /// assert_eq!(Ok(2).or_else(err).or_else(sq), Ok(2));\n  1551:     /// assert_eq!(Err(3).or_else(sq).or_else(err), Ok(9));\n  1552:     /// assert_eq!(Err(3).or_else(err).or_else(err), Err(3));\n  1553:     /// ```\n  1554:     #[inline]\n  1555:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1556:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1557:     pub const fn or_else<F, O>(self, op: O) -> Result<T, F>\n  1558:     where\n  1559:         O: [const] FnOnce(E) -> Result<T, F> + [const] Destruct,\n  1560:     {\n  1561:         match self {\n  1562:             Ok(t) => Ok(t),\n  1563:             Err(e) => op(e),\n  1564:         }\n  1565:     }\n  1566: \n  1567:     /// Returns the contained [`Ok`] value or a provided default.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::transpose",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
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
      "name": "transpose",
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
        "impl_id": "core:29318",
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
    "verification_source": "  1800:     /// `Ok(Some(_))` and `Err(_)` will be mapped to `Some(Ok(_))` and `Some(Err(_))`.\n  1801:     ///\n  1802:     /// # Examples\n  1803:     ///\n  1804:     /// ```\n  1805:     /// #[derive(Debug, Eq, PartialEq)]\n  1806:     /// struct SomeErr;\n  1807:     ///\n  1808:     /// let x: Result<Option<i32>, SomeErr> = Ok(Some(5));\n  1809:     /// let y: Option<Result<i32, SomeErr>> = Some(Ok(5));\n  1810:     /// assert_eq!(x.transpose(), y);\n  1811:     /// ```\n  1812:     #[inline]\n  1813:     #[stable(feature = \"transpose_result\", since = \"1.33.0\")]\n  1814:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1815:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1816:     pub const fn transpose(self) -> Option<Result<T, E>> {\n  1817:         match self {\n  1818:             Ok(Some(x)) => Some(Ok(x)),\n  1819:             Ok(None) => None,\n  1820:             Err(e) => Some(Err(e)),\n  1821:         }\n  1822:     }\n  1823: }\n  1824: \n  1825: impl<T, E> Result<Result<T, E>, E> {\n  1826:     /// Converts from `Result<Result<T, E>, E>` to `Result<T, E>`\n  1827:     ///\n  1828:     /// # Examples\n  1829:     ///\n  1830:     /// ```\n  1831:     /// let x: Result<Result<&'static str, u32>, u32> = Ok(Ok(\"hello\"));\n  1832:     /// assert_eq!(Ok(\"hello\"), x.flatten());",
    "nanvix_source": "  1809:     /// struct SomeErr;\n  1810:     ///\n  1811:     /// let x: Result<Option<i32>, SomeErr> = Ok(Some(5));\n  1812:     /// let y: Option<Result<i32, SomeErr>> = Some(Ok(5));\n  1813:     /// assert_eq!(x.transpose(), y);\n  1814:     /// ```\n  1815:     #[inline]\n  1816:     #[stable(feature = \"transpose_result\", since = \"1.33.0\")]\n  1817:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1818:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1819:     pub const fn transpose(self) -> Option<Result<T, E>> {\n  1820:         match self {\n  1821:             Ok(Some(x)) => Some(Ok(x)),\n  1822:             Ok(None) => None,\n  1823:             Err(e) => Some(Err(e)),\n  1824:         }\n  1825:     }\n  1826: }\n  1827: \n  1828: impl<T, E> Result<Result<T, E>, E> {\n  1829:     /// Converts from `Result<Result<T, E>, E>` to `Result<T, E>`",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::unwrap",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
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
                      "id": 921,
                      "path": "fmt::Debug"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "E"
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
      "name": "unwrap",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1211:     /// # Examples\n  1212:     ///\n  1213:     /// Basic usage:\n  1214:     ///\n  1215:     /// ```\n  1216:     /// let x: Result<u32, &str> = Ok(2);\n  1217:     /// assert_eq!(x.unwrap(), 2);\n  1218:     /// ```\n  1219:     ///\n  1220:     /// ```should_panic\n  1221:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1222:     /// x.unwrap(); // panics with `emergency failure`\n  1223:     /// ```\n  1224:     #[inline(always)]\n  1225:     #[track_caller]\n  1226:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1227:     pub fn unwrap(self) -> T\n  1228:     where\n  1229:         E: fmt::Debug,\n  1230:     {\n  1231:         match self {\n  1232:             Ok(t) => t,\n  1233:             Err(e) => unwrap_failed(\"called `Result::unwrap()` on an `Err` value\", &e),\n  1234:         }\n  1235:     }\n  1236: \n  1237:     /// Returns the contained [`Ok`] value or a default\n  1238:     ///\n  1239:     /// Consumes the `self` argument then, if [`Ok`], returns the contained\n  1240:     /// value, otherwise if [`Err`], returns the default value for that\n  1241:     /// type.\n  1242:     ///\n  1243:     /// # Examples",
    "nanvix_source": "  1215:     /// assert_eq!(x.unwrap(), 2);\n  1216:     /// ```\n  1217:     ///\n  1218:     /// ```should_panic\n  1219:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1220:     /// x.unwrap(); // panics with `emergency failure`\n  1221:     /// ```\n  1222:     #[inline(always)]\n  1223:     #[track_caller]\n  1224:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1225:     pub fn unwrap(self) -> T\n  1226:     where\n  1227:         E: fmt::Debug,\n  1228:     {\n  1229:         match self {\n  1230:             Ok(t) => t,\n  1231:             Err(e) => unwrap_failed(\"called `Result::unwrap()` on an `Err` value\", &e),\n  1232:         }\n  1233:     }\n  1234: \n  1235:     /// Returns the contained [`Ok`] value or a default",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::unwrap_err",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
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
                      "id": 921,
                      "path": "fmt::Debug"
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
      "name": "unwrap_err",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "E"
        }
      }
    },
    "verification_source": "  1308:     /// by the [`Ok`]'s value.\n  1309:     ///\n  1310:     /// # Examples\n  1311:     ///\n  1312:     /// ```should_panic\n  1313:     /// let x: Result<u32, &str> = Ok(2);\n  1314:     /// x.unwrap_err(); // panics with `2`\n  1315:     /// ```\n  1316:     ///\n  1317:     /// ```\n  1318:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1319:     /// assert_eq!(x.unwrap_err(), \"emergency failure\");\n  1320:     /// ```\n  1321:     #[inline]\n  1322:     #[track_caller]\n  1323:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1324:     pub fn unwrap_err(self) -> E\n  1325:     where\n  1326:         T: fmt::Debug,\n  1327:     {\n  1328:         match self {\n  1329:             Ok(t) => unwrap_failed(\"called `Result::unwrap_err()` on an `Ok` value\", &t),\n  1330:             Err(e) => e,\n  1331:         }\n  1332:     }\n  1333: \n  1334:     /// Returns the contained [`Ok`] value, but never panics.\n  1335:     ///\n  1336:     /// Unlike [`unwrap`], this method is known to never panic on the\n  1337:     /// result types it is implemented for. Therefore, it can be used\n  1338:     /// instead of `unwrap` as a maintainability safeguard that will fail\n  1339:     /// to compile if the error type of the `Result` is later changed\n  1340:     /// to an error that can actually occur.",
    "nanvix_source": "  1312:     /// x.unwrap_err(); // panics with `2`\n  1313:     /// ```\n  1314:     ///\n  1315:     /// ```\n  1316:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1317:     /// assert_eq!(x.unwrap_err(), \"emergency failure\");\n  1318:     /// ```\n  1319:     #[inline]\n  1320:     #[track_caller]\n  1321:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1322:     pub fn unwrap_err(self) -> E\n  1323:     where\n  1324:         T: fmt::Debug,\n  1325:     {\n  1326:         match self {\n  1327:             Ok(t) => unwrap_failed(\"called `Result::unwrap_err()` on an `Ok` value\", &t),\n  1328:             Err(e) => e,\n  1329:         }\n  1330:     }\n  1331: \n  1332:     /// Returns the contained [`Ok`] value, but never panics.",
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
