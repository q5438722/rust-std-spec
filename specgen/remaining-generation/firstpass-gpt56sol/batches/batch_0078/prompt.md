For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::result::Result::and_then",
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
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "generic": "U"
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
      "name": "and_then",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "U"
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
    },
    "verification_source": "  1472:     ///\n  1473:     /// ```\n  1474:     /// use std::{io::ErrorKind, path::Path};\n  1475:     ///\n  1476:     /// // Note: on Windows \"/\" maps to \"C:\\\"\n  1477:     /// let root_modified_time = Path::new(\"/\").metadata().and_then(|md| md.modified());\n  1478:     /// assert!(root_modified_time.is_ok());\n  1479:     ///\n  1480:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1481:     /// assert!(should_fail.is_err());\n  1482:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1483:     /// ```\n  1484:     #[inline]\n  1485:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1486:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1487:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1488:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1489:     where\n  1490:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1491:     {\n  1492:         match self {\n  1493:             Ok(t) => op(t),\n  1494:             Err(e) => Err(e),\n  1495:         }\n  1496:     }\n  1497: \n  1498:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.\n  1499:     ///\n  1500:     /// Arguments passed to `or` are eagerly evaluated; if you are passing the\n  1501:     /// result of a function call, it is recommended to use [`or_else`], which is\n  1502:     /// lazily evaluated.\n  1503:     ///\n  1504:     /// [`or_else`]: Result::or_else",
    "nanvix_source": "  1476:     /// assert!(root_modified_time.is_ok());\n  1477:     ///\n  1478:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1479:     /// assert!(should_fail.is_err());\n  1480:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1481:     /// ```\n  1482:     #[inline]\n  1483:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1484:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1485:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1486:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1487:     where\n  1488:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1489:     {\n  1490:         match self {\n  1491:             Ok(t) => op(t),\n  1492:             Err(e) => Err(e),\n  1493:         }\n  1494:     }\n  1495: \n  1496:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::inspect",
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": null
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
      "name": "inspect",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "   972:     /// Calls a function with a reference to the contained value if [`Ok`].\n   973:     ///\n   974:     /// Returns the original result.\n   975:     ///\n   976:     /// # Examples\n   977:     ///\n   978:     /// ```\n   979:     /// let x: u8 = \"4\"\n   980:     ///     .parse::<u8>()\n   981:     ///     .inspect(|x| println!(\"original: {x}\"))\n   982:     ///     .map(|x| x.pow(3))\n   983:     ///     .expect(\"failed to parse number\");\n   984:     /// ```\n   985:     #[inline]\n   986:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n   987:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   988:     pub const fn inspect<F>(self, f: F) -> Self\n   989:     where\n   990:         F: [const] FnOnce(&T) + [const] Destruct,\n   991:     {\n   992:         if let Ok(ref t) = self {\n   993:             f(t);\n   994:         }\n   995: \n   996:         self\n   997:     }\n   998: \n   999:     /// Calls a function with a reference to the contained value if [`Err`].\n  1000:     ///\n  1001:     /// Returns the original result.\n  1002:     ///\n  1003:     /// # Examples\n  1004:     ///",
    "nanvix_source": "   976:     /// ```\n   977:     /// let x: u8 = \"4\"\n   978:     ///     .parse::<u8>()\n   979:     ///     .inspect(|x| println!(\"original: {x}\"))\n   980:     ///     .map(|x| x.pow(3))\n   981:     ///     .expect(\"failed to parse number\");\n   982:     /// ```\n   983:     #[inline]\n   984:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n   985:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   986:     pub const fn inspect<F>(self, f: F) -> Self\n   987:     where\n   988:         F: [const] FnOnce(&T) + [const] Destruct,\n   989:     {\n   990:         if let Ok(ref t) = self {\n   991:             f(t);\n   992:         }\n   993: \n   994:         self\n   995:     }\n   996: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::inspect_err",
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "E"
                                }
                              }
                            }
                          ],
                          "output": null
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
      "name": "inspect_err",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1000:     ///\n  1001:     /// Returns the original result.\n  1002:     ///\n  1003:     /// # Examples\n  1004:     ///\n  1005:     /// ```\n  1006:     /// use std::{fs, io};\n  1007:     ///\n  1008:     /// fn read() -> io::Result<String> {\n  1009:     ///     fs::read_to_string(\"address.txt\")\n  1010:     ///         .inspect_err(|e| eprintln!(\"failed to read file: {e}\"))\n  1011:     /// }\n  1012:     /// ```\n  1013:     #[inline]\n  1014:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1015:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1016:     pub const fn inspect_err<F>(self, f: F) -> Self\n  1017:     where\n  1018:         F: [const] FnOnce(&E) + [const] Destruct,\n  1019:     {\n  1020:         if let Err(ref e) = self {\n  1021:             f(e);\n  1022:         }\n  1023: \n  1024:         self\n  1025:     }\n  1026: \n  1027:     /// Converts from `Result<T, E>` (or `&Result<T, E>`) to `Result<&<T as Deref>::Target, &E>`.\n  1028:     ///\n  1029:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`Deref`](crate::ops::Deref)\n  1030:     /// and returns the new [`Result`].\n  1031:     ///\n  1032:     /// # Examples",
    "nanvix_source": "  1004:     /// use std::{fs, io};\n  1005:     ///\n  1006:     /// fn read() -> io::Result<String> {\n  1007:     ///     fs::read_to_string(\"address.txt\")\n  1008:     ///         .inspect_err(|e| eprintln!(\"failed to read file: {e}\"))\n  1009:     /// }\n  1010:     /// ```\n  1011:     #[inline]\n  1012:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1013:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1014:     pub const fn inspect_err<F>(self, f: F) -> Self\n  1015:     where\n  1016:         F: [const] FnOnce(&E) + [const] Destruct,\n  1017:     {\n  1018:         if let Err(ref e) = self {\n  1019:             f(e);\n  1020:         }\n  1021: \n  1022:         self\n  1023:     }\n  1024: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::is_err_and",
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
                            "primitive": "bool"
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
                "generic": "T"
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
      "name": "is_err_and",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   658:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), true);\n   659:     ///\n   660:     /// let x: Result<u32, Error> = Err(Error::new(ErrorKind::PermissionDenied, \"!\"));\n   661:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   662:     ///\n   663:     /// let x: Result<u32, Error> = Ok(123);\n   664:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   665:     ///\n   666:     /// let x: Result<u32, String> = Err(\"ownership\".to_string());\n   667:     /// assert_eq!(x.as_ref().is_err_and(|x| x.len() > 1), true);\n   668:     /// println!(\"still alive {:?}\", x);\n   669:     /// ```\n   670:     #[must_use]\n   671:     #[inline]\n   672:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   673:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   674:     pub const fn is_err_and<F>(self, f: F) -> bool\n   675:     where\n   676:         F: [const] FnOnce(E) -> bool + [const] Destruct,\n   677:         E: [const] Destruct,\n   678:         T: [const] Destruct,\n   679:     {\n   680:         match self {\n   681:             Ok(_) => false,\n   682:             Err(e) => f(e),\n   683:         }\n   684:     }\n   685: \n   686:     /////////////////////////////////////////////////////////////////////////\n   687:     // Adapter for each variant\n   688:     /////////////////////////////////////////////////////////////////////////\n   689: \n   690:     /// Converts from `Result<T, E>` to [`Option<T>`].",
    "nanvix_source": "   664:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   665:     ///\n   666:     /// let x: Result<u32, String> = Err(\"ownership\".to_string());\n   667:     /// assert_eq!(x.as_ref().is_err_and(|x| x.len() > 1), true);\n   668:     /// println!(\"still alive {:?}\", x);\n   669:     /// ```\n   670:     #[must_use]\n   671:     #[inline]\n   672:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   673:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   674:     pub const fn is_err_and<F>(self, f: F) -> bool\n   675:     where\n   676:         F: [const] FnOnce(E) -> bool + [const] Destruct,\n   677:         E: [const] Destruct,\n   678:         T: [const] Destruct,\n   679:     {\n   680:         match self {\n   681:             Ok(_) => false,\n   682:             Err(e) => f(e),\n   683:         }\n   684:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::is_ok_and",
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
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
      "name": "is_ok_and",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   603:     /// assert_eq!(x.is_ok_and(|x| x > 1), true);\n   604:     ///\n   605:     /// let x: Result<u32, &str> = Ok(0);\n   606:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);\n   607:     ///\n   608:     /// let x: Result<u32, &str> = Err(\"hey\");\n   609:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);\n   610:     ///\n   611:     /// let x: Result<String, &str> = Ok(\"ownership\".to_string());\n   612:     /// assert_eq!(x.as_ref().is_ok_and(|x| x.len() > 1), true);\n   613:     /// println!(\"still alive {:?}\", x);\n   614:     /// ```\n   615:     #[must_use]\n   616:     #[inline]\n   617:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   618:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   619:     pub const fn is_ok_and<F>(self, f: F) -> bool\n   620:     where\n   621:         F: [const] FnOnce(T) -> bool + [const] Destruct,\n   622:         T: [const] Destruct,\n   623:         E: [const] Destruct,\n   624:     {\n   625:         match self {\n   626:             Err(_) => false,\n   627:             Ok(x) => f(x),\n   628:         }\n   629:     }\n   630: \n   631:     /// Returns `true` if the result is [`Err`].\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```",
    "nanvix_source": "   609:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);\n   610:     ///\n   611:     /// let x: Result<String, &str> = Ok(\"ownership\".to_string());\n   612:     /// assert_eq!(x.as_ref().is_ok_and(|x| x.len() > 1), true);\n   613:     /// println!(\"still alive {:?}\", x);\n   614:     /// ```\n   615:     #[must_use]\n   616:     #[inline]\n   617:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   618:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   619:     pub const fn is_ok_and<F>(self, f: F) -> bool\n   620:     where\n   621:         F: [const] FnOnce(T) -> bool + [const] Destruct,\n   622:         T: [const] Destruct,\n   623:         E: [const] Destruct,\n   624:     {\n   625:         match self {\n   626:             Err(_) => false,\n   627:             Ok(x) => f(x),\n   628:         }\n   629:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::map_or",
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
                "generic": "U"
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
      "name": "map_or",
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
              "generic": "U"
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
    "verification_source": "   847:     ///\n   848:     /// [`map_or_else`]: Result::map_or_else\n   849:     ///\n   850:     /// # Examples\n   851:     ///\n   852:     /// ```\n   853:     /// let x: Result<_, &str> = Ok(\"foo\");\n   854:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n   855:     ///\n   856:     /// let x: Result<&str, _> = Err(\"bar\");\n   857:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"result_map_or\", since = \"1.41.0\")]\n   861:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   862:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n   863:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n   864:     where\n   865:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   866:         T: [const] Destruct,\n   867:         E: [const] Destruct,\n   868:         U: [const] Destruct,\n   869:     {\n   870:         match self {\n   871:             Ok(t) => f(t),\n   872:             Err(_) => default,\n   873:         }\n   874:     }\n   875: \n   876:     /// Maps a `Result<T, E>` to `U` by applying fallback function `default` to\n   877:     /// a contained [`Err`] value, or function `f` to a contained [`Ok`] value.\n   878:     ///\n   879:     /// This function can be used to unpack a successful result",
    "nanvix_source": "   853:     /// let x: Result<_, &str> = Ok(\"foo\");\n   854:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n   855:     ///\n   856:     /// let x: Result<&str, _> = Err(\"bar\");\n   857:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"result_map_or\", since = \"1.41.0\")]\n   861:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   862:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n   863:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n   864:     where\n   865:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   866:         T: [const] Destruct,\n   867:         E: [const] Destruct,\n   868:         U: [const] Destruct,\n   869:     {\n   870:         match self {\n   871:             Ok(t) => f(t),\n   872:             Err(_) => default,\n   873:         }",
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
