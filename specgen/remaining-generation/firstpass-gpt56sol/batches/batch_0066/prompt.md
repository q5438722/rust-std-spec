For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Result::inspect_err",
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
    "target": "core::fmt::Result::is_err",
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
      "name": "is_err",
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
    "verification_source": "   630: \n   631:     /// Returns `true` if the result is [`Err`].\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```\n   636:     /// let x: Result<i32, &str> = Ok(-3);\n   637:     /// assert_eq!(x.is_err(), false);\n   638:     ///\n   639:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   640:     /// assert_eq!(x.is_err(), true);\n   641:     /// ```\n   642:     #[must_use = \"if you intended to assert that this is err, consider `.unwrap_err()` instead\"]\n   643:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   644:     #[inline]\n   645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   646:     pub const fn is_err(&self) -> bool {\n   647:         !self.is_ok()\n   648:     }\n   649: \n   650:     /// Returns `true` if the result is [`Err`] and the value inside of it matches a predicate.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::io::{Error, ErrorKind};\n   656:     ///\n   657:     /// let x: Result<u32, Error> = Err(Error::new(ErrorKind::NotFound, \"!\"));\n   658:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), true);\n   659:     ///\n   660:     /// let x: Result<u32, Error> = Err(Error::new(ErrorKind::PermissionDenied, \"!\"));\n   661:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   662:     ///",
    "nanvix_source": "   636:     /// let x: Result<i32, &str> = Ok(-3);\n   637:     /// assert_eq!(x.is_err(), false);\n   638:     ///\n   639:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   640:     /// assert_eq!(x.is_err(), true);\n   641:     /// ```\n   642:     #[must_use = \"if you intended to assert that this is err, consider `.unwrap_err()` instead\"]\n   643:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   644:     #[inline]\n   645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   646:     pub const fn is_err(&self) -> bool {\n   647:         !self.is_ok()\n   648:     }\n   649: \n   650:     /// Returns `true` if the result is [`Err`] and the value inside of it matches a predicate.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::io::{Error, ErrorKind};\n   656:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::is_err_and",
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
    "target": "core::fmt::Result::is_ok",
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
    "target": "core::fmt::Result::is_ok_and",
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
    "target": "core::fmt::Result::iter",
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
