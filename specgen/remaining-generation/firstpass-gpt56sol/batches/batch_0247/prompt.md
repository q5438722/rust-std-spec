For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::TryLockResult::is_err_and",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
    "target": "std::sync::TryLockResult::is_ok",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "is_ok",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   577: \n   578:     /// Returns `true` if the result is [`Ok`].\n   579:     ///\n   580:     /// # Examples\n   581:     ///\n   582:     /// ```\n   583:     /// let x: Result<i32, &str> = Ok(-3);\n   584:     /// assert_eq!(x.is_ok(), true);\n   585:     ///\n   586:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   587:     /// assert_eq!(x.is_ok(), false);\n   588:     /// ```\n   589:     #[must_use = \"if you intended to assert that this is ok, consider `.unwrap()` instead\"]\n   590:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   591:     #[inline]\n   592:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   593:     pub const fn is_ok(&self) -> bool {\n   594:         matches!(*self, Ok(_))\n   595:     }\n   596: \n   597:     /// Returns `true` if the result is [`Ok`] and the value inside of it matches a predicate.\n   598:     ///\n   599:     /// # Examples\n   600:     ///\n   601:     /// ```\n   602:     /// let x: Result<u32, &str> = Ok(2);\n   603:     /// assert_eq!(x.is_ok_and(|x| x > 1), true);\n   604:     ///\n   605:     /// let x: Result<u32, &str> = Ok(0);\n   606:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);\n   607:     ///\n   608:     /// let x: Result<u32, &str> = Err(\"hey\");\n   609:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);",
    "nanvix_source": "   583:     /// let x: Result<i32, &str> = Ok(-3);\n   584:     /// assert_eq!(x.is_ok(), true);\n   585:     ///\n   586:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   587:     /// assert_eq!(x.is_ok(), false);\n   588:     /// ```\n   589:     #[must_use = \"if you intended to assert that this is ok, consider `.unwrap()` instead\"]\n   590:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   591:     #[inline]\n   592:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   593:     pub const fn is_ok(&self) -> bool {\n   594:         matches!(*self, Ok(_))\n   595:     }\n   596: \n   597:     /// Returns `true` if the result is [`Ok`] and the value inside of it matches a predicate.\n   598:     ///\n   599:     /// # Examples\n   600:     ///\n   601:     /// ```\n   602:     /// let x: Result<u32, &str> = Ok(2);\n   603:     /// assert_eq!(x.is_ok_and(|x| x > 1), true);",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::TryLockResult::is_ok_and",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
    "target": "std::sync::TryLockResult::iter",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
    "target": "std::sync::TryLockResult::iter_mut",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
  },
  {
    "target": "std::sync::TryLockResult::map",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
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
    "verification_source": "   815:     ///\n   816:     /// Print the numbers on each line of a string multiplied by two.\n   817:     ///\n   818:     /// ```\n   819:     /// let line = \"1\\n2\\n3\\n4\\n\";\n   820:     ///\n   821:     /// for num in line.lines() {\n   822:     ///     match num.parse::<i32>().map(|i| i * 2) {\n   823:     ///         Ok(n) => println!(\"{n}\"),\n   824:     ///         Err(..) => {}\n   825:     ///     }\n   826:     /// }\n   827:     /// ```\n   828:     #[inline]\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   831:     pub const fn map<U, F>(self, op: F) -> Result<U, E>\n   832:     where\n   833:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   834:     {\n   835:         match self {\n   836:             Ok(t) => Ok(op(t)),\n   837:             Err(e) => Err(e),\n   838:         }\n   839:     }\n   840: \n   841:     /// Returns the provided default (if [`Err`]), or\n   842:     /// applies a function to the contained value (if [`Ok`]).\n   843:     ///\n   844:     /// Arguments passed to `map_or` are eagerly evaluated; if you are passing\n   845:     /// the result of a function call, it is recommended to use [`map_or_else`],\n   846:     /// which is lazily evaluated.\n   847:     ///",
    "nanvix_source": "   821:     /// for num in line.lines() {\n   822:     ///     match num.parse::<i32>().map(|i| i * 2) {\n   823:     ///         Ok(n) => println!(\"{n}\"),\n   824:     ///         Err(..) => {}\n   825:     ///     }\n   826:     /// }\n   827:     /// ```\n   828:     #[inline]\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   831:     pub const fn map<U, F>(self, op: F) -> Result<U, E>\n   832:     where\n   833:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   834:     {\n   835:         match self {\n   836:             Ok(t) => Ok(op(t)),\n   837:             Err(e) => Err(e),\n   838:         }\n   839:     }\n   840: \n   841:     /// Returns the provided default (if [`Err`]), or",
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
