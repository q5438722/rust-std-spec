For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::result::Result::map_or_default",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
            "name": "U"
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
                    "modifier": "maybe_const",
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
                      "id": 70,
                      "path": "Default"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          },
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
      "name": "map_or_default",
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "U"
        }
      }
    },
    "verification_source": "   912:     /// # Examples\n   913:     ///\n   914:     /// ```\n   915:     /// #![feature(result_option_map_or_default)]\n   916:     ///\n   917:     /// let x: Result<_, &str> = Ok(\"foo\");\n   918:     /// let y: Result<&str, _> = Err(\"bar\");\n   919:     ///\n   920:     /// assert_eq!(x.map_or_default(|x| x.len()), 3);\n   921:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n   922:     /// ```\n   923:     ///\n   924:     /// [default value]: Default::default\n   925:     #[inline]\n   926:     #[unstable(feature = \"result_option_map_or_default\", issue = \"138099\")]\n   927:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   928:     pub const fn map_or_default<U, F>(self, f: F) -> U\n   929:     where\n   930:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   931:         U: [const] Default,\n   932:         T: [const] Destruct,\n   933:         E: [const] Destruct,\n   934:     {\n   935:         match self {\n   936:             Ok(t) => f(t),\n   937:             Err(_) => U::default(),\n   938:         }\n   939:     }\n   940: \n   941:     /// Maps a `Result<T, E>` to `Result<T, F>` by applying a function to a\n   942:     /// contained [`Err`] value, leaving an [`Ok`] value untouched.\n   943:     ///\n   944:     /// This function can be used to pass through a successful result while handling",
    "nanvix_source": "   916:     /// let y: Result<&str, _> = Err(\"bar\");\n   917:     ///\n   918:     /// assert_eq!(x.map_or_default(|x| x.len()), 3);\n   919:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n   920:     /// ```\n   921:     ///\n   922:     /// [default value]: Default::default\n   923:     #[inline]\n   924:     #[stable(feature = \"result_option_map_or_default\", since = \"CURRENT_RUSTC_VERSION\")]\n   925:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   926:     pub const fn map_or_default<U, F>(self, f: F) -> U\n   927:     where\n   928:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   929:         U: [const] Default,\n   930:         T: [const] Destruct,\n   931:         E: [const] Destruct,\n   932:     {\n   933:         match self {\n   934:             Ok(t) => f(t),\n   935:             Err(_) => U::default(),\n   936:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::map_or_else",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
            "name": "U"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "D"
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
              "generic_params": [],
              "type": {
                "generic": "D"
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
      "name": "map_or_else",
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
            "default",
            {
              "generic": "D"
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
          "generic": "U"
        }
      }
    },
    "verification_source": "   881:     ///\n   882:     ///\n   883:     /// # Examples\n   884:     ///\n   885:     /// ```\n   886:     /// let k = 21;\n   887:     ///\n   888:     /// let x : Result<_, &str> = Ok(\"foo\");\n   889:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);\n   890:     ///\n   891:     /// let x : Result<&str, _> = Err(\"bar\");\n   892:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);\n   893:     /// ```\n   894:     #[inline]\n   895:     #[stable(feature = \"result_map_or_else\", since = \"1.41.0\")]\n   896:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   897:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n   898:     where\n   899:         D: [const] FnOnce(E) -> U + [const] Destruct,\n   900:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   901:     {\n   902:         match self {\n   903:             Ok(t) => f(t),\n   904:             Err(e) => default(e),\n   905:         }\n   906:     }\n   907: \n   908:     /// Maps a `Result<T, E>` to a `U` by applying function `f` to the contained\n   909:     /// value if the result is [`Ok`], otherwise if [`Err`], returns the\n   910:     /// [default value] for the type `U`.\n   911:     ///\n   912:     /// # Examples\n   913:     ///",
    "nanvix_source": "   887:     ///\n   888:     /// let x : Result<_, &str> = Ok(\"foo\");\n   889:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);\n   890:     ///\n   891:     /// let x : Result<&str, _> = Err(\"bar\");\n   892:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);\n   893:     /// ```\n   894:     #[inline]\n   895:     #[stable(feature = \"result_map_or_else\", since = \"1.41.0\")]\n   896:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   897:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n   898:     where\n   899:         D: [const] FnOnce(E) -> U + [const] Destruct,\n   900:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   901:     {\n   902:         match self {\n   903:             Ok(t) => f(t),\n   904:             Err(e) => default(e),\n   905:         }\n   906:     }\n   907: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::or_else",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
    "target": "core::result::Result::unwrap_or_else",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                            "generic": "T"
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
      "name": "unwrap_or_else",
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
    "verification_source": "  1600: \n  1601:     /// Returns the contained [`Ok`] value or computes it from a closure.\n  1602:     ///\n  1603:     ///\n  1604:     /// # Examples\n  1605:     ///\n  1606:     /// ```\n  1607:     /// fn count(x: &str) -> usize { x.len() }\n  1608:     ///\n  1609:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1610:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1611:     /// ```\n  1612:     #[inline]\n  1613:     #[track_caller]\n  1614:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1615:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1616:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1617:     where\n  1618:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1619:     {\n  1620:         match self {\n  1621:             Ok(t) => t,\n  1622:             Err(e) => op(e),\n  1623:         }\n  1624:     }\n  1625: \n  1626:     /// Returns the contained [`Ok`] value, consuming the `self` value,\n  1627:     /// without checking that the value is not an [`Err`].\n  1628:     ///\n  1629:     /// # Safety\n  1630:     ///\n  1631:     /// Calling this method on an [`Err`] is *[undefined behavior]*.\n  1632:     ///",
    "nanvix_source": "  1604:     /// ```\n  1605:     /// fn count(x: &str) -> usize { x.len() }\n  1606:     ///\n  1607:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1608:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1609:     /// ```\n  1610:     #[inline]\n  1611:     #[track_caller]\n  1612:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1613:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1614:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1615:     where\n  1616:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1617:     {\n  1618:         match self {\n  1619:             Ok(t) => t,\n  1620:             Err(e) => op(e),\n  1621:         }\n  1622:     }\n  1623: \n  1624:     /// Returns the contained [`Ok`] value, consuming the `self` value,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::binary_search_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                                "lifetime": "'a",
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
      "name": "binary_search_by",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
                      "primitive": "usize"
                    }
                  },
                  {
                    "type": {
                      "primitive": "usize"
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
    "verification_source": "  2954:     ///\n  2955:     /// ```\n  2956:     /// let s = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55];\n  2957:     ///\n  2958:     /// let seek = 13;\n  2959:     /// assert_eq!(s.binary_search_by(|probe| probe.cmp(&seek)), Ok(9));\n  2960:     /// let seek = 4;\n  2961:     /// assert_eq!(s.binary_search_by(|probe| probe.cmp(&seek)), Err(7));\n  2962:     /// let seek = 100;\n  2963:     /// assert_eq!(s.binary_search_by(|probe| probe.cmp(&seek)), Err(13));\n  2964:     /// let seek = 1;\n  2965:     /// let r = s.binary_search_by(|probe| probe.cmp(&seek));\n  2966:     /// assert!(match r { Ok(1..=4) => true, _ => false, });\n  2967:     /// ```\n  2968:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2969:     #[inline]\n  2970:     pub fn binary_search_by<'a, F>(&'a self, mut f: F) -> Result<usize, usize>\n  2971:     where\n  2972:         F: FnMut(&'a T) -> Ordering,\n  2973:     {\n  2974:         let mut size = self.len();\n  2975:         if size == 0 {\n  2976:             return Err(0);\n  2977:         }\n  2978:         let mut base = 0usize;\n  2979: \n  2980:         // This loop intentionally doesn't have an early exit if the comparison\n  2981:         // returns Equal. We want the number of loop iterations to depend *only*\n  2982:         // on the size of the input slice so that the CPU can reliably predict\n  2983:         // the loop count.\n  2984:         while size > 1 {\n  2985:             let half = size / 2;\n  2986:             let mid = base + half;",
    "nanvix_source": "  2966:     /// let seek = 4;\n  2967:     /// assert_eq!(s.binary_search_by(|probe| probe.cmp(&seek)), Err(7));\n  2968:     /// let seek = 100;\n  2969:     /// assert_eq!(s.binary_search_by(|probe| probe.cmp(&seek)), Err(13));\n  2970:     /// let seek = 1;\n  2971:     /// let r = s.binary_search_by(|probe| probe.cmp(&seek));\n  2972:     /// assert!(match r { Ok(1..=4) => true, _ => false, });\n  2973:     /// ```\n  2974:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2975:     #[inline]\n  2976:     pub fn binary_search_by<'a, F>(&'a self, mut f: F) -> Result<usize, usize>\n  2977:     where\n  2978:         F: FnMut(&'a T) -> Ordering,\n  2979:     {\n  2980:         let mut size = self.len();\n  2981:         if size == 0 {\n  2982:             return Err(0);\n  2983:         }\n  2984:         let mut base = 0usize;\n  2985: \n  2986:         // This loop intentionally doesn't have an early exit if the comparison",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::binary_search_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
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
      "name": "binary_search_by_key",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
            "b",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "B"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  },
                  {
                    "type": {
                      "primitive": "usize"
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
    "verification_source": "  3055:     ///          (1, 2), (2, 3), (4, 5), (5, 8), (3, 13),\n  3056:     ///          (1, 21), (2, 34), (4, 55)];\n  3057:     ///\n  3058:     /// assert_eq!(s.binary_search_by_key(&13, |&(a, b)| b),  Ok(9));\n  3059:     /// assert_eq!(s.binary_search_by_key(&4, |&(a, b)| b),   Err(7));\n  3060:     /// assert_eq!(s.binary_search_by_key(&100, |&(a, b)| b), Err(13));\n  3061:     /// let r = s.binary_search_by_key(&1, |&(a, b)| b);\n  3062:     /// assert!(match r { Ok(1..=4) => true, _ => false, });\n  3063:     /// ```\n  3064:     // Lint rustdoc::broken_intra_doc_links is allowed as `slice::sort_by_key` is\n  3065:     // in crate `alloc`, and as such doesn't exists yet when building `core`: #74481.\n  3066:     // This breaks links when slice is displayed in core, but changing it to use relative links\n  3067:     // would break when the item is re-exported. So allow the core links to be broken for now.\n  3068:     #[allow(rustdoc::broken_intra_doc_links)]\n  3069:     #[stable(feature = \"slice_binary_search_by_key\", since = \"1.10.0\")]\n  3070:     #[inline]\n  3071:     pub fn binary_search_by_key<'a, B, F>(&'a self, b: &B, mut f: F) -> Result<usize, usize>\n  3072:     where\n  3073:         F: FnMut(&'a T) -> B,\n  3074:         B: Ord,\n  3075:     {\n  3076:         self.binary_search_by(|k| f(k).cmp(b))\n  3077:     }\n  3078: \n  3079:     /// Sorts the slice in ascending order **without** preserving the initial order of equal elements.\n  3080:     ///\n  3081:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not\n  3082:     /// allocate), and *O*(*n* \\* log(*n*)) worst-case.\n  3083:     ///\n  3084:     /// If the implementation of [`Ord`] for `T` does not implement a [total order], the function\n  3085:     /// may panic; even if the function exits normally, the resulting order of elements in the slice\n  3086:     /// is unspecified. See also the note on panicking below.\n  3087:     ///",
    "nanvix_source": "  3067:     /// let r = s.binary_search_by_key(&1, |&(a, b)| b);\n  3068:     /// assert!(match r { Ok(1..=4) => true, _ => false, });\n  3069:     /// ```\n  3070:     // Lint rustdoc::broken_intra_doc_links is allowed as `slice::sort_by_key` is\n  3071:     // in crate `alloc`, and as such doesn't exists yet when building `core`: #74481.\n  3072:     // This breaks links when slice is displayed in core, but changing it to use relative links\n  3073:     // would break when the item is re-exported. So allow the core links to be broken for now.\n  3074:     #[allow(rustdoc::broken_intra_doc_links)]\n  3075:     #[stable(feature = \"slice_binary_search_by_key\", since = \"1.10.0\")]\n  3076:     #[inline]\n  3077:     pub fn binary_search_by_key<'a, B, F>(&'a self, b: &B, mut f: F) -> Result<usize, usize>\n  3078:     where\n  3079:         F: FnMut(&'a T) -> B,\n  3080:         B: Ord,\n  3081:     {\n  3082:         self.binary_search_by(|k| f(k).cmp(b))\n  3083:     }\n  3084: \n  3085:     /// Sorts the slice in ascending order **without** preserving the initial order of equal elements.\n  3086:     ///\n  3087:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not",
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
