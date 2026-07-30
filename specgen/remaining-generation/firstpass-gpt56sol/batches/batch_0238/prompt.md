For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::LockResult::unwrap_or_default",
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
        "where_predicates": [
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
      "name": "unwrap_or_default",
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
    "verification_source": "  1249:     ///\n  1250:     /// ```\n  1251:     /// let good_year_from_input = \"1909\";\n  1252:     /// let bad_year_from_input = \"190blarg\";\n  1253:     /// let good_year = good_year_from_input.parse().unwrap_or_default();\n  1254:     /// let bad_year = bad_year_from_input.parse().unwrap_or_default();\n  1255:     ///\n  1256:     /// assert_eq!(1909, good_year);\n  1257:     /// assert_eq!(0, bad_year);\n  1258:     /// ```\n  1259:     ///\n  1260:     /// [`parse`]: str::parse\n  1261:     /// [`FromStr`]: crate::str::FromStr\n  1262:     #[inline]\n  1263:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1264:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1265:     pub const fn unwrap_or_default(self) -> T\n  1266:     where\n  1267:         T: [const] Default + [const] Destruct,\n  1268:         E: [const] Destruct,\n  1269:     {\n  1270:         match self {\n  1271:             Ok(x) => x,\n  1272:             Err(_) => Default::default(),\n  1273:         }\n  1274:     }\n  1275: \n  1276:     /// Returns the contained [`Err`] value, consuming the `self` value.\n  1277:     ///\n  1278:     /// # Panics\n  1279:     ///\n  1280:     /// Panics if the value is an [`Ok`], with a panic message including the\n  1281:     /// passed message, and the content of the [`Ok`].",
    "nanvix_source": "  1253:     ///\n  1254:     /// assert_eq!(1909, good_year);\n  1255:     /// assert_eq!(0, bad_year);\n  1256:     /// ```\n  1257:     ///\n  1258:     /// [`parse`]: str::parse\n  1259:     /// [`FromStr`]: crate::str::FromStr\n  1260:     #[inline]\n  1261:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1262:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1263:     pub const fn unwrap_or_default(self) -> T\n  1264:     where\n  1265:         T: [const] Default + [const] Destruct,\n  1266:         E: [const] Destruct,\n  1267:     {\n  1268:         match self {\n  1269:             Ok(x) => x,\n  1270:             Err(_) => Default::default(),\n  1271:         }\n  1272:     }\n  1273: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::unwrap_or_else",
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
    "target": "std::sync::LockResult::unwrap_unchecked",
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
        "is_unsafe": true
      },
      "name": "unwrap_unchecked",
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
    "verification_source": "  1634:     ///\n  1635:     /// # Examples\n  1636:     ///\n  1637:     /// ```\n  1638:     /// let x: Result<u32, &str> = Ok(2);\n  1639:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, 2);\n  1640:     /// ```\n  1641:     ///\n  1642:     /// ```no_run\n  1643:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1644:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1645:     /// ```\n  1646:     #[inline]\n  1647:     #[track_caller]\n  1648:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1649:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1650:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1651:         match self {\n  1652:             Ok(t) => t,\n  1653:             Err(e) => {\n  1654:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1655:                 super::mem::forget(e);\n  1656:                 // SAFETY: the safety contract must be upheld by the caller.\n  1657:                 unsafe { hint::unreachable_unchecked() }\n  1658:             }\n  1659:         }\n  1660:     }\n  1661: \n  1662:     /// Returns the contained [`Err`] value, consuming the `self` value,\n  1663:     /// without checking that the value is not an [`Ok`].\n  1664:     ///\n  1665:     /// # Safety\n  1666:     ///",
    "nanvix_source": "  1638:     /// ```\n  1639:     ///\n  1640:     /// ```no_run\n  1641:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1642:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1647:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1648:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1649:         match self {\n  1650:             Ok(t) => t,\n  1651:             Err(e) => {\n  1652:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1653:                 super::mem::forget(e);\n  1654:                 // SAFETY: the safety contract must be upheld by the caller.\n  1655:                 unsafe { hint::unreachable_unchecked() }\n  1656:             }\n  1657:         }\n  1658:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::clear_poison",
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
      "concurrency_or_hidden_state",
      "unit_return_variant"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "clear_poison",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 508,
            "path": "Mutex"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 8,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
        "output": null
      }
    },
    "verification_source": "   594:     ///     let _lock = c_mutex.lock().unwrap();\n   595:     ///     panic!(); // the mutex gets poisoned\n   596:     /// }).join();\n   597:     ///\n   598:     /// assert_eq!(mutex.is_poisoned(), true);\n   599:     /// let x = mutex.lock().unwrap_or_else(|mut e| {\n   600:     ///     **e.get_mut() = 1;\n   601:     ///     mutex.clear_poison();\n   602:     ///     e.into_inner()\n   603:     /// });\n   604:     /// assert_eq!(mutex.is_poisoned(), false);\n   605:     /// assert_eq!(*x, 1);\n   606:     /// ```\n   607:     #[inline]\n   608:     #[stable(feature = \"mutex_unpoison\", since = \"1.77.0\")]\n   609:     #[rustc_should_not_be_called_on_const_items]\n   610:     pub fn clear_poison(&self) {\n   611:         self.poison.clear();\n   612:     }\n   613: \n   614:     /// Consumes this mutex, returning the underlying data.\n   615:     ///\n   616:     /// # Errors\n   617:     ///\n   618:     /// If another user of this mutex panicked while holding the mutex, then\n   619:     /// this call will return an error containing the underlying data\n   620:     /// instead.\n   621:     ///\n   622:     /// # Examples\n   623:     ///\n   624:     /// ```\n   625:     /// use std::sync::Mutex;\n   626:     ///",
    "nanvix_source": "   600:     ///     **e.get_mut() = 1;\n   601:     ///     mutex.clear_poison();\n   602:     ///     e.into_inner()\n   603:     /// });\n   604:     /// assert_eq!(mutex.is_poisoned(), false);\n   605:     /// assert_eq!(*x, 1);\n   606:     /// ```\n   607:     #[inline]\n   608:     #[stable(feature = \"mutex_unpoison\", since = \"1.77.0\")]\n   609:     #[rustc_should_not_be_called_on_const_items]\n   610:     pub fn clear_poison(&self) {\n   611:         self.poison.clear();\n   612:     }\n   613: \n   614:     /// Consumes this mutex, returning the underlying data.\n   615:     ///\n   616:     /// # Errors\n   617:     ///\n   618:     /// If another user of this mutex panicked while holding the mutex, then\n   619:     /// this call will return an error containing the underlying data\n   620:     /// instead.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::get_mut",
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
      "concurrency_or_hidden_state",
      "reference_identity_vs_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "get_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 508,
            "path": "Mutex"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 8,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 8855,
            "path": "LockResult"
          }
        }
      }
    },
    "verification_source": "   648:     /// If another user of this mutex panicked while holding the mutex, then\n   649:     /// this call will return an error containing a mutable reference to the\n   650:     /// underlying data instead.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::sync::Mutex;\n   656:     ///\n   657:     /// let mut mutex = Mutex::new(0);\n   658:     /// *mutex.get_mut().unwrap() = 10;\n   659:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   660:     /// ```\n   661:     ///\n   662:     /// [`forget()`]: mem::forget\n   663:     #[stable(feature = \"mutex_get_mut\", since = \"1.6.0\")]\n   664:     pub fn get_mut(&mut self) -> LockResult<&mut T> {\n   665:         let data = self.data.get_mut();\n   666:         poison::map_result(self.poison.borrow(), |()| data)\n   667:     }\n   668: \n   669:     /// Returns a raw pointer to the underlying data.\n   670:     ///\n   671:     /// The returned pointer is always non-null and properly aligned, but it is\n   672:     /// the user's responsibility to ensure that any reads and writes through it\n   673:     /// are properly synchronized to avoid data races, and that it is not read\n   674:     /// or written through after the mutex is dropped.\n   675:     #[unstable(feature = \"mutex_data_ptr\", issue = \"140368\")]\n   676:     pub const fn data_ptr(&self) -> *mut T {\n   677:         self.data.get()\n   678:     }\n   679: }\n   680: ",
    "nanvix_source": "   654:     /// ```\n   655:     /// use std::sync::Mutex;\n   656:     ///\n   657:     /// let mut mutex = Mutex::new(0);\n   658:     /// *mutex.get_mut().unwrap() = 10;\n   659:     /// assert_eq!(*mutex.lock().unwrap(), 10);\n   660:     /// ```\n   661:     ///\n   662:     /// [`forget()`]: mem::forget\n   663:     #[stable(feature = \"mutex_get_mut\", since = \"1.6.0\")]\n   664:     pub fn get_mut(&mut self) -> LockResult<&mut T> {\n   665:         let data = self.data.get_mut();\n   666:         poison::map_result(self.poison.borrow(), |()| data)\n   667:     }\n   668: \n   669:     /// Returns a raw pointer to the underlying data.\n   670:     ///\n   671:     /// The returned pointer is always non-null and properly aligned, but it is\n   672:     /// the user's responsibility to ensure that any reads and writes through it\n   673:     /// are properly synchronized to avoid data races, and that it is not read\n   674:     /// or written through after the mutex is dropped.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Mutex::into_inner",
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
                      "id": 8,
                      "path": "Sized"
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
      "name": "into_inner",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 508,
            "path": "Mutex"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 8,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:8900",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:508",
        "resolved_owner_path": [
          "std",
          "sync",
          "poison",
          "mutex",
          "Mutex"
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
            "id": 8855,
            "path": "LockResult"
          }
        }
      }
    },
    "verification_source": "   615:     ///\n   616:     /// # Errors\n   617:     ///\n   618:     /// If another user of this mutex panicked while holding the mutex, then\n   619:     /// this call will return an error containing the underlying data\n   620:     /// instead.\n   621:     ///\n   622:     /// # Examples\n   623:     ///\n   624:     /// ```\n   625:     /// use std::sync::Mutex;\n   626:     ///\n   627:     /// let mutex = Mutex::new(0);\n   628:     /// assert_eq!(mutex.into_inner().unwrap(), 0);\n   629:     /// ```\n   630:     #[stable(feature = \"mutex_into_inner\", since = \"1.6.0\")]\n   631:     pub fn into_inner(self) -> LockResult<T>\n   632:     where\n   633:         T: Sized,\n   634:     {\n   635:         let data = self.data.into_inner();\n   636:         poison::map_result(self.poison.borrow(), |()| data)\n   637:     }\n   638: \n   639:     /// Returns a mutable reference to the underlying data.\n   640:     ///\n   641:     /// Since this call borrows the `Mutex` mutably, no actual locking needs to\n   642:     /// take place -- the mutable borrow statically guarantees no new locks can be acquired\n   643:     /// while this reference exists. Note that this method does not clear any previous abandoned locks\n   644:     /// (e.g., via [`forget()`] on a [`MutexGuard`]).\n   645:     ///\n   646:     /// # Errors\n   647:     ///",
    "nanvix_source": "   621:     ///\n   622:     /// # Examples\n   623:     ///\n   624:     /// ```\n   625:     /// use std::sync::Mutex;\n   626:     ///\n   627:     /// let mutex = Mutex::new(0);\n   628:     /// assert_eq!(mutex.into_inner().unwrap(), 0);\n   629:     /// ```\n   630:     #[stable(feature = \"mutex_into_inner\", since = \"1.6.0\")]\n   631:     pub fn into_inner(self) -> LockResult<T>\n   632:     where\n   633:         T: Sized,\n   634:     {\n   635:         let data = self.data.into_inner();\n   636:         poison::map_result(self.poison.borrow(), |()| data)\n   637:     }\n   638: \n   639:     /// Returns a mutable reference to the underlying data.\n   640:     ///\n   641:     /// Since this call borrows the `Mutex` mutably, no actual locking needs to",
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
