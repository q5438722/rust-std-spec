For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::ControlFlow::map_break",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
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
                              "generic": "B"
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
      "name": "map_break",
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
                      "generic": "B"
                    }
                  },
                  {
                    "type": {
                      "generic": "C"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9735,
            "path": "ControlFlow"
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
              "name": "C"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23404",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9735",
        "resolved_owner_path": [
          "core",
          "ops",
          "control_flow",
          "ControlFlow"
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
                      "generic": "C"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9735,
            "path": "ControlFlow"
          }
        }
      }
    },
    "verification_source": "   263:     #[inline]\n   264:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   265:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   266:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   267:     pub const fn break_ok(self) -> Result<B, C> {\n   268:         match self {\n   269:             ControlFlow::Continue(c) => Err(c),\n   270:             ControlFlow::Break(b) => Ok(b),\n   271:         }\n   272:     }\n   273: \n   274:     /// Maps `ControlFlow<B, C>` to `ControlFlow<T, C>` by applying a function\n   275:     /// to the break value in case it exists.\n   276:     #[inline]\n   277:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   278:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   279:     pub const fn map_break<T, F>(self, f: F) -> ControlFlow<T, C>\n   280:     where\n   281:         F: [const] FnOnce(B) -> T + [const] Destruct,\n   282:     {\n   283:         match self {\n   284:             ControlFlow::Continue(x) => ControlFlow::Continue(x),\n   285:             ControlFlow::Break(x) => ControlFlow::Break(f(x)),\n   286:         }\n   287:     }\n   288: \n   289:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the\n   290:     /// `ControlFlow` was `Continue` and `None` otherwise.\n   291:     ///\n   292:     /// # Examples\n   293:     ///\n   294:     /// ```\n   295:     /// use std::ops::ControlFlow;",
    "nanvix_source": "   270:             ControlFlow::Continue(c) => Err(c),\n   271:             ControlFlow::Break(b) => Ok(b),\n   272:         }\n   273:     }\n   274: \n   275:     /// Maps `ControlFlow<B, C>` to `ControlFlow<T, C>` by applying a function\n   276:     /// to the break value in case it exists.\n   277:     #[inline]\n   278:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   279:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   280:     pub const fn map_break<T, F>(self, f: F) -> ControlFlow<T, C>\n   281:     where\n   282:         F: [const] FnOnce(B) -> T + [const] Destruct,\n   283:     {\n   284:         match self {\n   285:             ControlFlow::Continue(x) => ControlFlow::Continue(x),\n   286:             ControlFlow::Break(x) => ControlFlow::Break(f(x)),\n   287:         }\n   288:     }\n   289: \n   290:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::map_continue",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
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
                              "generic": "C"
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
      "name": "map_continue",
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
                      "generic": "B"
                    }
                  },
                  {
                    "type": {
                      "generic": "C"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9735,
            "path": "ControlFlow"
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
              "name": "C"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23404",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9735",
        "resolved_owner_path": [
          "core",
          "ops",
          "control_flow",
          "ControlFlow"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "B"
                    }
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
            "id": 9735,
            "path": "ControlFlow"
          }
        }
      }
    },
    "verification_source": "   375:     #[inline]\n   376:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   377:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   378:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   379:     pub const fn continue_ok(self) -> Result<C, B> {\n   380:         match self {\n   381:             ControlFlow::Continue(c) => Ok(c),\n   382:             ControlFlow::Break(b) => Err(b),\n   383:         }\n   384:     }\n   385: \n   386:     /// Maps `ControlFlow<B, C>` to `ControlFlow<B, T>` by applying a function\n   387:     /// to the continue value in case it exists.\n   388:     #[inline]\n   389:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   390:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   391:     pub const fn map_continue<T, F>(self, f: F) -> ControlFlow<B, T>\n   392:     where\n   393:         F: [const] FnOnce(C) -> T + [const] Destruct,\n   394:     {\n   395:         match self {\n   396:             ControlFlow::Continue(x) => ControlFlow::Continue(f(x)),\n   397:             ControlFlow::Break(x) => ControlFlow::Break(x),\n   398:         }\n   399:     }\n   400: }\n   401: \n   402: impl<T> ControlFlow<T, T> {\n   403:     /// Extracts the value `T` that is wrapped by `ControlFlow<T, T>`.\n   404:     ///\n   405:     /// # Examples\n   406:     ///\n   407:     /// ```",
    "nanvix_source": "   382:             ControlFlow::Continue(c) => Ok(c),\n   383:             ControlFlow::Break(b) => Err(b),\n   384:         }\n   385:     }\n   386: \n   387:     /// Maps `ControlFlow<B, C>` to `ControlFlow<B, T>` by applying a function\n   388:     /// to the continue value in case it exists.\n   389:     #[inline]\n   390:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   391:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   392:     pub const fn map_continue<T, F>(self, f: F) -> ControlFlow<B, T>\n   393:     where\n   394:         F: [const] FnOnce(C) -> T + [const] Destruct,\n   395:     {\n   396:         match self {\n   397:             ControlFlow::Continue(x) => ControlFlow::Continue(f(x)),\n   398:             ControlFlow::Break(x) => ControlFlow::Break(x),\n   399:         }\n   400:     }\n   401: }\n   402: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::filter",
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
                "generic": "P"
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
      "name": "filter",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "predicate",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1562:     /// # Examples\n  1563:     ///\n  1564:     /// ```rust\n  1565:     /// fn is_even(n: &i32) -> bool {\n  1566:     ///     n % 2 == 0\n  1567:     /// }\n  1568:     ///\n  1569:     /// assert_eq!(None.filter(is_even), None);\n  1570:     /// assert_eq!(Some(3).filter(is_even), None);\n  1571:     /// assert_eq!(Some(4).filter(is_even), Some(4));\n  1572:     /// ```\n  1573:     ///\n  1574:     /// [`Some(t)`]: Some\n  1575:     #[inline]\n  1576:     #[stable(feature = \"option_filter\", since = \"1.27.0\")]\n  1577:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1578:     pub const fn filter<P>(self, predicate: P) -> Self\n  1579:     where\n  1580:         P: [const] FnOnce(&T) -> bool + [const] Destruct,\n  1581:         T: [const] Destruct,\n  1582:     {\n  1583:         if let Some(x) = self {\n  1584:             if predicate(&x) {\n  1585:                 return Some(x);\n  1586:             }\n  1587:         }\n  1588:         None\n  1589:     }\n  1590: \n  1591:     /// Returns the option if it contains a value, otherwise returns `optb`.\n  1592:     ///\n  1593:     /// Arguments passed to `or` are eagerly evaluated; if you are passing the\n  1594:     /// result of a function call, it is recommended to use [`or_else`], which is",
    "nanvix_source": "  1564:     ///\n  1565:     /// assert_eq!(None.filter(is_even), None);\n  1566:     /// assert_eq!(Some(3).filter(is_even), None);\n  1567:     /// assert_eq!(Some(4).filter(is_even), Some(4));\n  1568:     /// ```\n  1569:     ///\n  1570:     /// [`Some(t)`]: Some\n  1571:     #[inline]\n  1572:     #[stable(feature = \"option_filter\", since = \"1.27.0\")]\n  1573:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1574:     pub const fn filter<P>(self, predicate: P) -> Self\n  1575:     where\n  1576:         P: [const] FnOnce(&T) -> bool + [const] Destruct,\n  1577:         T: [const] Destruct,\n  1578:     {\n  1579:         if let Some(x) = self {\n  1580:             if predicate(&x) {\n  1581:                 return Some(x);\n  1582:             }\n  1583:         }\n  1584:         None",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::inspect",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
    "verification_source": "  1175:     ///\n  1176:     /// ```\n  1177:     /// let list = vec![1, 2, 3];\n  1178:     ///\n  1179:     /// // prints \"got: 2\"\n  1180:     /// let x = list\n  1181:     ///     .get(1)\n  1182:     ///     .inspect(|x| println!(\"got: {x}\"))\n  1183:     ///     .expect(\"list should be long enough\");\n  1184:     ///\n  1185:     /// // prints nothing\n  1186:     /// list.get(5).inspect(|x| println!(\"got: {x}\"));\n  1187:     /// ```\n  1188:     #[inline]\n  1189:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1190:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1191:     pub const fn inspect<F>(self, f: F) -> Self\n  1192:     where\n  1193:         F: [const] FnOnce(&T) + [const] Destruct,\n  1194:     {\n  1195:         if let Some(ref x) = self {\n  1196:             f(x);\n  1197:         }\n  1198: \n  1199:         self\n  1200:     }\n  1201: \n  1202:     /// Returns the provided default result (if none),\n  1203:     /// or applies a function to the contained value (if any).\n  1204:     ///\n  1205:     /// Arguments passed to `map_or` are eagerly evaluated; if you are passing\n  1206:     /// the result of a function call, it is recommended to use [`map_or_else`],\n  1207:     /// which is lazily evaluated.",
    "nanvix_source": "  1179:     ///     .get(1)\n  1180:     ///     .inspect(|x| println!(\"got: {x}\"))\n  1181:     ///     .expect(\"list should be long enough\");\n  1182:     ///\n  1183:     /// // prints nothing\n  1184:     /// list.get(5).inspect(|x| println!(\"got: {x}\"));\n  1185:     /// ```\n  1186:     #[inline]\n  1187:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1188:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1189:     pub const fn inspect<F>(self, f: F) -> Self\n  1190:     where\n  1191:         F: [const] FnOnce(&T) + [const] Destruct,\n  1192:     {\n  1193:         if let Some(ref x) = self {\n  1194:             f(x);\n  1195:         }\n  1196: \n  1197:         self\n  1198:     }\n  1199: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::is_none_or",
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
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl [const] FnOnce(T) -> bool + [const] Destruct"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "is_none_or",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
              "impl_trait": [
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
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   694:     /// assert_eq!(x.is_none_or(|x| x > 1), true);\n   695:     ///\n   696:     /// let x: Option<u32> = Some(0);\n   697:     /// assert_eq!(x.is_none_or(|x| x > 1), false);\n   698:     ///\n   699:     /// let x: Option<u32> = None;\n   700:     /// assert_eq!(x.is_none_or(|x| x > 1), true);\n   701:     ///\n   702:     /// let x: Option<String> = Some(\"ownership\".to_string());\n   703:     /// assert_eq!(x.as_ref().is_none_or(|x| x.len() > 1), true);\n   704:     /// println!(\"still alive {:?}\", x);\n   705:     /// ```\n   706:     #[must_use]\n   707:     #[inline]\n   708:     #[stable(feature = \"is_none_or\", since = \"1.82.0\")]\n   709:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n   710:     pub const fn is_none_or(self, f: impl [const] FnOnce(T) -> bool + [const] Destruct) -> bool {\n   711:         match self {\n   712:             None => true,\n   713:             Some(x) => f(x),\n   714:         }\n   715:     }\n   716: \n   717:     /////////////////////////////////////////////////////////////////////////\n   718:     // Adapter for working with references\n   719:     /////////////////////////////////////////////////////////////////////////\n   720: \n   721:     /// Converts from `&Option<T>` to `Option<&T>`.\n   722:     ///\n   723:     /// # Examples\n   724:     ///\n   725:     /// Calculates the length of an <code>Option<[String]></code> as an <code>Option<[usize]></code>\n   726:     /// without moving the [`String`]. The [`map`] method takes the `self` argument by value,",
    "nanvix_source": "   698:     /// assert_eq!(x.is_none_or(|x| x > 1), true);\n   699:     ///\n   700:     /// let x: Option<String> = Some(\"ownership\".to_string());\n   701:     /// assert_eq!(x.as_ref().is_none_or(|x| x.len() > 1), true);\n   702:     /// println!(\"still alive {:?}\", x);\n   703:     /// ```\n   704:     #[must_use]\n   705:     #[inline]\n   706:     #[stable(feature = \"is_none_or\", since = \"1.82.0\")]\n   707:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n   708:     pub const fn is_none_or(self, f: impl [const] FnOnce(T) -> bool + [const] Destruct) -> bool {\n   709:         match self {\n   710:             None => true,\n   711:             Some(x) => f(x),\n   712:         }\n   713:     }\n   714: \n   715:     /////////////////////////////////////////////////////////////////////////\n   716:     // Adapter for working with references\n   717:     /////////////////////////////////////////////////////////////////////////\n   718: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::is_some_and",
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
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl [const] FnOnce(T) -> bool + [const] Destruct"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "is_some_and",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
              "impl_trait": [
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
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   645:     /// assert_eq!(x.is_some_and(|x| x > 1), true);\n   646:     ///\n   647:     /// let x: Option<u32> = Some(0);\n   648:     /// assert_eq!(x.is_some_and(|x| x > 1), false);\n   649:     ///\n   650:     /// let x: Option<u32> = None;\n   651:     /// assert_eq!(x.is_some_and(|x| x > 1), false);\n   652:     ///\n   653:     /// let x: Option<String> = Some(\"ownership\".to_string());\n   654:     /// assert_eq!(x.as_ref().is_some_and(|x| x.len() > 1), true);\n   655:     /// println!(\"still alive {:?}\", x);\n   656:     /// ```\n   657:     #[must_use]\n   658:     #[inline]\n   659:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   660:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n   661:     pub const fn is_some_and(self, f: impl [const] FnOnce(T) -> bool + [const] Destruct) -> bool {\n   662:         match self {\n   663:             None => false,\n   664:             Some(x) => f(x),\n   665:         }\n   666:     }\n   667: \n   668:     /// Returns `true` if the option is a [`None`] value.\n   669:     ///\n   670:     /// # Examples\n   671:     ///\n   672:     /// ```\n   673:     /// let x: Option<u32> = Some(2);\n   674:     /// assert_eq!(x.is_none(), false);\n   675:     ///\n   676:     /// let x: Option<u32> = None;\n   677:     /// assert_eq!(x.is_none(), true);",
    "nanvix_source": "   649:     /// assert_eq!(x.is_some_and(|x| x > 1), false);\n   650:     ///\n   651:     /// let x: Option<String> = Some(\"ownership\".to_string());\n   652:     /// assert_eq!(x.as_ref().is_some_and(|x| x.len() > 1), true);\n   653:     /// println!(\"still alive {:?}\", x);\n   654:     /// ```\n   655:     #[must_use]\n   656:     #[inline]\n   657:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   658:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n   659:     pub const fn is_some_and(self, f: impl [const] FnOnce(T) -> bool + [const] Destruct) -> bool {\n   660:         match self {\n   661:             None => false,\n   662:             Some(x) => f(x),\n   663:         }\n   664:     }\n   665: \n   666:     /// Returns `true` if the option is a [`None`] value.\n   667:     ///\n   668:     /// # Examples\n   669:     ///",
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
