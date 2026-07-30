For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::DebugSet::entries",
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
      "formatting_effect",
      "reference_identity_vs_view"
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
                      "id": 921,
                      "path": "fmt::Debug"
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
                                    "generic": "D"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "entries",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13421,
            "path": "DebugSet"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29814",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13421",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugSet"
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
          ],
          [
            "entries",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   574:     ///\n   575:     /// impl fmt::Debug for Foo {\n   576:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   577:     ///         fmt.debug_set()\n   578:     ///            .entries(self.0.iter()) // Adds the first \"entry\".\n   579:     ///            .entries(self.1.iter()) // Adds the second \"entry\".\n   580:     ///            .finish()\n   581:     ///     }\n   582:     /// }\n   583:     ///\n   584:     /// assert_eq!(\n   585:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   586:     ///     \"{10, 11, 12, 13}\",\n   587:     /// );\n   588:     /// ```\n   589:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   590:     pub fn entries<D, I>(&mut self, entries: I) -> &mut Self\n   591:     where\n   592:         D: fmt::Debug,\n   593:         I: IntoIterator<Item = D>,\n   594:     {\n   595:         for entry in entries {\n   596:             self.entry(&entry);\n   597:         }\n   598:         self\n   599:     }\n   600: \n   601:     /// Marks the set as non-exhaustive, indicating to the reader that there are some other\n   602:     /// elements that are not shown in the debug representation.\n   603:     ///\n   604:     /// # Examples\n   605:     ///\n   606:     /// ```",
    "nanvix_source": "   580:     ///            .finish()\n   581:     ///     }\n   582:     /// }\n   583:     ///\n   584:     /// assert_eq!(\n   585:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   586:     ///     \"{10, 11, 12, 13}\",\n   587:     /// );\n   588:     /// ```\n   589:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   590:     pub fn entries<D, I>(&mut self, entries: I) -> &mut Self\n   591:     where\n   592:         D: fmt::Debug,\n   593:         I: IntoIterator<Item = D>,\n   594:     {\n   595:         for entry in entries {\n   596:             self.entry(&entry);\n   597:         }\n   598:         self\n   599:     }\n   600: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugSet::entry",
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
      "formatting_effect",
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
      "name": "entry",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13421,
            "path": "DebugSet"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29814",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13421",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugSet"
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
          ],
          [
            "entry",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "dyn_trait": {
                    "lifetime": null,
                    "traits": [
                      {
                        "generic_params": [],
                        "trait": {
                          "args": null,
                          "id": 921,
                          "path": "fmt::Debug"
                        }
                      }
                    ]
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   532:     ///\n   533:     /// impl fmt::Debug for Foo {\n   534:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   535:     ///         fmt.debug_set()\n   536:     ///            .entry(&self.0) // Adds the first \"entry\".\n   537:     ///            .entry(&self.1) // Adds the second \"entry\".\n   538:     ///            .finish()\n   539:     ///     }\n   540:     /// }\n   541:     ///\n   542:     /// assert_eq!(\n   543:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   544:     ///     \"{[10, 11], [12, 13]}\",\n   545:     /// );\n   546:     /// ```\n   547:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   548:     pub fn entry(&mut self, entry: &dyn fmt::Debug) -> &mut Self {\n   549:         self.inner.entry_with(|f| entry.fmt(f));\n   550:         self\n   551:     }\n   552: \n   553:     /// Adds a new entry to the set output.\n   554:     ///\n   555:     /// This method is equivalent to [`DebugSet::entry`], but formats the\n   556:     /// entry using a provided closure rather than by calling [`Debug::fmt`].\n   557:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   558:     pub fn entry_with<F>(&mut self, entry_fmt: F) -> &mut Self\n   559:     where\n   560:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n   561:     {\n   562:         self.inner.entry_with(entry_fmt);\n   563:         self\n   564:     }",
    "nanvix_source": "   538:     ///            .finish()\n   539:     ///     }\n   540:     /// }\n   541:     ///\n   542:     /// assert_eq!(\n   543:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   544:     ///     \"{[10, 11], [12, 13]}\",\n   545:     /// );\n   546:     /// ```\n   547:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   548:     pub fn entry(&mut self, entry: &dyn fmt::Debug) -> &mut Self {\n   549:         self.inner.entry_with(|f| entry.fmt(f));\n   550:         self\n   551:     }\n   552: \n   553:     /// Adds a new entry to the set output.\n   554:     ///\n   555:     /// This method is equivalent to [`DebugSet::entry`], but formats the\n   556:     /// entry using a provided closure rather than by calling [`Debug::fmt`].\n   557:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   558:     pub fn entry_with<F>(&mut self, entry_fmt: F) -> &mut Self",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugSet::finish",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "finish",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13421,
            "path": "DebugSet"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29814",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13421",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugSet"
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
            "args": null,
            "id": 919,
            "path": "fmt::Result"
          }
        }
      }
    },
    "verification_source": "   656:     /// struct Foo(Vec<i32>);\n   657:     ///\n   658:     /// impl fmt::Debug for Foo {\n   659:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   660:     ///         fmt.debug_set()\n   661:     ///            .entries(self.0.iter())\n   662:     ///            .finish() // Ends the set formatting.\n   663:     ///     }\n   664:     /// }\n   665:     ///\n   666:     /// assert_eq!(\n   667:     ///     format!(\"{:?}\", Foo(vec![10, 11])),\n   668:     ///     \"{10, 11}\",\n   669:     /// );\n   670:     /// ```\n   671:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   672:     pub fn finish(&mut self) -> fmt::Result {\n   673:         self.inner.result = self.inner.result.and_then(|_| self.inner.fmt.write_str(\"}\"));\n   674:         self.inner.result\n   675:     }\n   676: }\n   677: \n   678: /// A struct to help with [`fmt::Debug`](Debug) implementations.\n   679: ///\n   680: /// This is useful when you wish to output a formatted list of items as a part\n   681: /// of your [`Debug::fmt`] implementation.\n   682: ///\n   683: /// This can be constructed by the [`Formatter::debug_list`] method.\n   684: ///\n   685: /// # Examples\n   686: ///\n   687: /// ```\n   688: /// use std::fmt;",
    "nanvix_source": "   662:     ///            .finish() // Ends the set formatting.\n   663:     ///     }\n   664:     /// }\n   665:     ///\n   666:     /// assert_eq!(\n   667:     ///     format!(\"{:?}\", Foo(vec![10, 11])),\n   668:     ///     \"{10, 11}\",\n   669:     /// );\n   670:     /// ```\n   671:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   672:     pub fn finish(&mut self) -> fmt::Result {\n   673:         self.inner.result = self.inner.result.and_then(|_| self.inner.fmt.write_str(\"}\"));\n   674:         self.inner.result\n   675:     }\n   676: }\n   677: \n   678: /// A struct to help with [`fmt::Debug`](Debug) implementations.\n   679: ///\n   680: /// This is useful when you wish to output a formatted list of items as a part\n   681: /// of your [`Debug::fmt`] implementation.\n   682: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugSet::finish_non_exhaustive",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "finish_non_exhaustive",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13421,
            "path": "DebugSet"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29814",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13421",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugSet"
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
            "args": null,
            "id": 919,
            "path": "fmt::Result"
          }
        }
      }
    },
    "verification_source": "   614:     ///         let mut f = fmt.debug_set();\n   615:     ///         let mut f = f.entries(self.0.iter().take(2));\n   616:     ///         if self.0.len() > 2 {\n   617:     ///             f.finish_non_exhaustive()\n   618:     ///         } else {\n   619:     ///             f.finish()\n   620:     ///         }\n   621:     ///     }\n   622:     /// }\n   623:     ///\n   624:     /// assert_eq!(\n   625:     ///     format!(\"{:?}\", Foo(vec![1, 2, 3, 4])),\n   626:     ///     \"{1, 2, ..}\",\n   627:     /// );\n   628:     /// ```\n   629:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   630:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   631:         self.inner.result = self.inner.result.and_then(|_| {\n   632:             if self.inner.has_fields {\n   633:                 if self.inner.is_pretty() {\n   634:                     let mut slot = None;\n   635:                     let mut state = Default::default();\n   636:                     let mut writer = PadAdapter::wrap(self.inner.fmt, &mut slot, &mut state);\n   637:                     writer.write_str(\"..\\n\")?;\n   638:                     self.inner.fmt.write_str(\"}\")\n   639:                 } else {\n   640:                     self.inner.fmt.write_str(\", ..}\")\n   641:                 }\n   642:             } else {\n   643:                 self.inner.fmt.write_str(\"..}\")\n   644:             }\n   645:         });\n   646:         self.inner.result",
    "nanvix_source": "   620:     ///         }\n   621:     ///     }\n   622:     /// }\n   623:     ///\n   624:     /// assert_eq!(\n   625:     ///     format!(\"{:?}\", Foo(vec![1, 2, 3, 4])),\n   626:     ///     \"{1, 2, ..}\",\n   627:     /// );\n   628:     /// ```\n   629:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   630:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   631:         self.inner.result = self.inner.result.and_then(|_| {\n   632:             if self.inner.has_fields {\n   633:                 if self.inner.is_pretty() {\n   634:                     let mut slot = None;\n   635:                     let mut state = Default::default();\n   636:                     let mut writer = PadAdapter::wrap(self.inner.fmt, &mut slot, &mut state);\n   637:                     writer.write_str(\"..\\n\")?;\n   638:                     self.inner.fmt.write_str(\"}\")\n   639:                 } else {\n   640:                     self.inner.fmt.write_str(\", ..}\")",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugStruct::field",
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
      "formatting_effect",
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
      "name": "field",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13417,
            "path": "DebugStruct"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29782",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13417",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugStruct"
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
          ],
          [
            "name",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ],
          [
            "value",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "dyn_trait": {
                    "lifetime": null,
                    "traits": [
                      {
                        "generic_params": [],
                        "trait": {
                          "args": null,
                          "id": 921,
                          "path": "fmt::Debug"
                        }
                      }
                    ]
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   116:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   117:     ///         fmt.debug_struct(\"Bar\")\n   118:     ///            .field(\"bar\", &self.bar) // We add `bar` field.\n   119:     ///            .field(\"another\", &self.another) // We add `another` field.\n   120:     ///            // We even add a field which doesn't exist (because why not?).\n   121:     ///            .field(\"nonexistent_field\", &1)\n   122:     ///            .finish() // We're good to go!\n   123:     ///     }\n   124:     /// }\n   125:     ///\n   126:     /// assert_eq!(\n   127:     ///     format!(\"{:?}\", Bar { bar: 10, another: \"Hello World\".to_string() }),\n   128:     ///     r#\"Bar { bar: 10, another: \"Hello World\", nonexistent_field: 1 }\"#,\n   129:     /// );\n   130:     /// ```\n   131:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   132:     pub fn field(&mut self, name: &str, value: &dyn fmt::Debug) -> &mut Self {\n   133:         self.field_with(name, |f| value.fmt(f))\n   134:     }\n   135: \n   136:     /// Adds a new field to the generated struct output.\n   137:     ///\n   138:     /// This method is equivalent to [`DebugStruct::field`], but formats the\n   139:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n   140:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   141:     pub fn field_with<F>(&mut self, name: &str, value_fmt: F) -> &mut Self\n   142:     where\n   143:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n   144:     {\n   145:         self.result = self.result.and_then(|_| {\n   146:             if self.is_pretty() {\n   147:                 if !self.has_fields {\n   148:                     self.fmt.write_str(\" {\\n\")?;",
    "nanvix_source": "   122:     ///            .finish() // We're good to go!\n   123:     ///     }\n   124:     /// }\n   125:     ///\n   126:     /// assert_eq!(\n   127:     ///     format!(\"{:?}\", Bar { bar: 10, another: \"Hello World\".to_string() }),\n   128:     ///     r#\"Bar { bar: 10, another: \"Hello World\", nonexistent_field: 1 }\"#,\n   129:     /// );\n   130:     /// ```\n   131:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   132:     pub fn field(&mut self, name: &str, value: &dyn fmt::Debug) -> &mut Self {\n   133:         self.field_with(name, |f| value.fmt(f))\n   134:     }\n   135: \n   136:     /// Adds a new field to the generated struct output.\n   137:     ///\n   138:     /// This method is equivalent to [`DebugStruct::field`], but formats the\n   139:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n   140:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   141:     pub fn field_with<F>(&mut self, name: &str, value_fmt: F) -> &mut Self\n   142:     where",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugStruct::finish",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "finish",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13417,
            "path": "DebugStruct"
          }
        },
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
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29782",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13417",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugStruct"
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
            "args": null,
            "id": 919,
            "path": "fmt::Result"
          }
        }
      }
    },
    "verification_source": "   228:     /// impl fmt::Debug for Bar {\n   229:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   230:     ///         fmt.debug_struct(\"Bar\")\n   231:     ///            .field(\"bar\", &self.bar)\n   232:     ///            .field(\"baz\", &self.baz)\n   233:     ///            .finish() // You need to call it to \"finish\" the\n   234:     ///                      // struct formatting.\n   235:     ///     }\n   236:     /// }\n   237:     ///\n   238:     /// assert_eq!(\n   239:     ///     format!(\"{:?}\", Bar { bar: 10, baz: \"Hello World\".to_string() }),\n   240:     ///     r#\"Bar { bar: 10, baz: \"Hello World\" }\"#,\n   241:     /// );\n   242:     /// ```\n   243:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   244:     pub fn finish(&mut self) -> fmt::Result {\n   245:         if self.has_fields {\n   246:             self.result = self.result.and_then(|_| {\n   247:                 if self.is_pretty() { self.fmt.write_str(\"}\") } else { self.fmt.write_str(\" }\") }\n   248:             });\n   249:         }\n   250:         self.result\n   251:     }\n   252: \n   253:     fn is_pretty(&self) -> bool {\n   254:         self.fmt.alternate()\n   255:     }\n   256: }\n   257: \n   258: /// A struct to help with [`fmt::Debug`](Debug) implementations.\n   259: ///\n   260: /// This is useful when you wish to output a formatted tuple as a part of your",
    "nanvix_source": "   234:     ///                      // struct formatting.\n   235:     ///     }\n   236:     /// }\n   237:     ///\n   238:     /// assert_eq!(\n   239:     ///     format!(\"{:?}\", Bar { bar: 10, baz: \"Hello World\".to_string() }),\n   240:     ///     r#\"Bar { bar: 10, baz: \"Hello World\" }\"#,\n   241:     /// );\n   242:     /// ```\n   243:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   244:     pub fn finish(&mut self) -> fmt::Result {\n   245:         if self.has_fields {\n   246:             self.result = self.result.and_then(|_| {\n   247:                 if self.is_pretty() { self.fmt.write_str(\"}\") } else { self.fmt.write_str(\" }\") }\n   248:             });\n   249:         }\n   250:         self.result\n   251:     }\n   252: \n   253:     fn is_pretty(&self) -> bool {\n   254:         self.fmt.alternate()",
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
