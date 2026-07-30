For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Peekable::next_if_eq",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
                    "modifier": "maybe",
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
                    "generic": "I"
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
      "name": "next_if_eq",
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
                      "generic": "I"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9889,
            "path": "Peekable"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": "Iterator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "I"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:26006",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9889",
        "resolved_owner_path": [
          "core",
          "iter",
          "adapters",
          "peekable",
          "Peekable"
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
            "expected",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "T"
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
                      "qualified_path": {
                        "args": null,
                        "name": "Item",
                        "self_type": {
                          "generic": "I"
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
    "verification_source": "   297:     }\n   298: \n   299:     /// Consume and return the next item if it is equal to `expected`.\n   300:     ///\n   301:     /// # Example\n   302:     /// Consume a number if it's equal to 0.\n   303:     /// ```\n   304:     /// let mut iter = (0..5).peekable();\n   305:     /// // The first item of the iterator is 0; consume it.\n   306:     /// assert_eq!(iter.next_if_eq(&0), Some(0));\n   307:     /// // The next item returned is now 1, so `next_if_eq` will return `None`.\n   308:     /// assert_eq!(iter.next_if_eq(&0), None);\n   309:     /// // `next_if_eq` retains the next item if it was not equal to `expected`.\n   310:     /// assert_eq!(iter.next(), Some(1));\n   311:     /// ```\n   312:     #[stable(feature = \"peekable_next_if\", since = \"1.51.0\")]\n   313:     pub fn next_if_eq<T>(&mut self, expected: &T) -> Option<I::Item>\n   314:     where\n   315:         T: ?Sized,\n   316:         I::Item: PartialEq<T>,\n   317:     {\n   318:         self.next_if(|next| next == expected)\n   319:     }\n   320: \n   321:     /// Consumes the next value of this iterator and applies a function `f` on it,\n   322:     /// returning the result if the closure returns `Ok`.\n   323:     ///\n   324:     /// Otherwise if the closure returns `Err` the value is put back for the next iteration.\n   325:     ///\n   326:     /// The content of the `Err` variant is typically the original value of the closure,\n   327:     /// but this is not required. If a different value is returned,\n   328:     /// the next `peek()` or `next()` call will result in this new value.\n   329:     /// This is similar to modifying the output of `peek_mut()`.",
    "nanvix_source": "   303:     /// ```\n   304:     /// let mut iter = (0..5).peekable();\n   305:     /// // The first item of the iterator is 0; consume it.\n   306:     /// assert_eq!(iter.next_if_eq(&0), Some(0));\n   307:     /// // The next item returned is now 1, so `next_if_eq` will return `None`.\n   308:     /// assert_eq!(iter.next_if_eq(&0), None);\n   309:     /// // `next_if_eq` retains the next item if it was not equal to `expected`.\n   310:     /// assert_eq!(iter.next(), Some(1));\n   311:     /// ```\n   312:     #[stable(feature = \"peekable_next_if\", since = \"1.51.0\")]\n   313:     pub fn next_if_eq<T>(&mut self, expected: &T) -> Option<I::Item>\n   314:     where\n   315:         T: ?Sized,\n   316:         I::Item: PartialEq<T>,\n   317:     {\n   318:         self.next_if(|next| next == expected)\n   319:     }\n   320: \n   321:     /// Consumes the next value of this iterator and applies a function `f` on it,\n   322:     /// returning the result if the closure returns `Ok`.\n   323:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Peekable::next_if_map",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
            "name": "R"
          },
          {
            "kind": {
              "type": {
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
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
                                  },
                                  "trait": {
                                    "args": null,
                                    "id": 82,
                                    "path": ""
                                  }
                                }
                              }
                            ],
                            "output": {
                              "resolved_path": {
                                "args": {
                                  "angle_bracketed": {
                                    "args": [
                                      {
                                        "type": {
                                          "generic": "R"
                                        }
                                      },
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
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(I::Item) -> Result<R, I::Item>"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "next_if_map",
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
                      "generic": "I"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9889,
            "path": "Peekable"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": "Iterator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "I"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:26006",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9889",
        "resolved_owner_path": [
          "core",
          "iter",
          "adapters",
          "peekable",
          "Peekable"
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
            "f",
            {
              "impl_trait": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "qualified_path": {
                                "args": null,
                                "name": "Item",
                                "self_type": {
                                  "generic": "I"
                                },
                                "trait": {
                                  "args": null,
                                  "id": 82,
                                  "path": ""
                                }
                              }
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "generic": "R"
                                      }
                                    },
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
              ]
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
                      "generic": "R"
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
    "verification_source": "   394:     ///#         Node::Comment(\"Over\".to_owned()),\n   395:     ///#         Node::Blue(\"The\".to_owned()),\n   396:     ///#         Node::Comment(\"Lazy\".to_owned()),\n   397:     ///#         Node::Comment(\"Dog\".to_owned()),\n   398:     ///#     ]),\n   399:     ///#     vec![\n   400:     ///#         Node::Comment(\"TheQuickBrown\".to_owned()),\n   401:     ///#         Node::Red(\"Fox\".to_owned()),\n   402:     ///#         Node::Green(\"Jumped\".to_owned()),\n   403:     ///#         Node::Comment(\"Over\".to_owned()),\n   404:     ///#         Node::Blue(\"The\".to_owned()),\n   405:     ///#         Node::Comment(\"LazyDog\".to_owned()),\n   406:     ///#     ],\n   407:     ///# )\n   408:     /// ```\n   409:     #[stable(feature = \"peekable_next_if_map\", since = \"1.94.0\")]\n   410:     pub fn next_if_map<R>(&mut self, f: impl FnOnce(I::Item) -> Result<R, I::Item>) -> Option<R> {\n   411:         let unpeek = if let Some(item) = self.next() {\n   412:             match f(item) {\n   413:                 Ok(result) => return Some(result),\n   414:                 Err(item) => Some(item),\n   415:             }\n   416:         } else {\n   417:             None\n   418:         };\n   419:         self.peeked = Some(unpeek);\n   420:         None\n   421:     }\n   422: \n   423:     /// Gives a mutable reference to the next value of the iterator and applies a function `f` to it,\n   424:     /// returning the result and advancing the iterator if `f` returns `Some`.\n   425:     ///\n   426:     /// Otherwise, if `f` returns `None`, the next value is kept for the next iteration.",
    "nanvix_source": "   400:     ///#         Node::Comment(\"TheQuickBrown\".to_owned()),\n   401:     ///#         Node::Red(\"Fox\".to_owned()),\n   402:     ///#         Node::Green(\"Jumped\".to_owned()),\n   403:     ///#         Node::Comment(\"Over\".to_owned()),\n   404:     ///#         Node::Blue(\"The\".to_owned()),\n   405:     ///#         Node::Comment(\"LazyDog\".to_owned()),\n   406:     ///#     ],\n   407:     ///# )\n   408:     /// ```\n   409:     #[stable(feature = \"peekable_next_if_map\", since = \"1.94.0\")]\n   410:     pub fn next_if_map<R>(&mut self, f: impl FnOnce(I::Item) -> Result<R, I::Item>) -> Option<R> {\n   411:         let unpeek = if let Some(item) = self.next() {\n   412:             match f(item) {\n   413:                 Ok(result) => return Some(result),\n   414:                 Err(item) => Some(item),\n   415:             }\n   416:         } else {\n   417:             None\n   418:         };\n   419:         self.peeked = Some(unpeek);\n   420:         None",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Peekable::next_if_map_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
            "name": "R"
          },
          {
            "kind": {
              "type": {
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
                                  "is_mutable": true,
                                  "lifetime": null,
                                  "type": {
                                    "qualified_path": {
                                      "args": null,
                                      "name": "Item",
                                      "self_type": {
                                        "generic": "I"
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
                                "args": {
                                  "angle_bracketed": {
                                    "args": [
                                      {
                                        "type": {
                                          "generic": "R"
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
            "name": "impl FnOnce(&mut I::Item) -> Option<R>"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "next_if_map_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "f"
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
                      "generic": "I"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9889,
            "path": "Peekable"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": "Iterator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "I"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:26006",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9889",
        "resolved_owner_path": [
          "core",
          "iter",
          "adapters",
          "peekable",
          "Peekable"
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
            "f",
            {
              "impl_trait": [
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "qualified_path": {
                                    "args": null,
                                    "name": "Item",
                                    "self_type": {
                                      "generic": "I"
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
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "generic": "R"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "R"
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
    "verification_source": "   423:     /// Gives a mutable reference to the next value of the iterator and applies a function `f` to it,\n   424:     /// returning the result and advancing the iterator if `f` returns `Some`.\n   425:     ///\n   426:     /// Otherwise, if `f` returns `None`, the next value is kept for the next iteration.\n   427:     ///\n   428:     /// If `f` panics, the item that is consumed from the iterator as if `Some` was returned from `f`.\n   429:     /// The value will be dropped.\n   430:     ///\n   431:     /// This is similar to [`next_if_map`](Self::next_if_map), except ownership of the item is not given to `f`.\n   432:     /// This can be preferable if `f` would copy the item anyway.\n   433:     ///\n   434:     /// # Examples\n   435:     ///\n   436:     /// Parse the leading decimal number from an iterator of characters.\n   437:     /// ```\n   438:     /// let mut iter = \"125 GOTO 10\".chars().peekable();\n   439:     /// let mut line_num = 0_u32;\n   440:     /// while let Some(digit) = iter.next_if_map_mut(|c| c.to_digit(10)) {\n   441:     ///     line_num = line_num * 10 + digit;\n   442:     /// }\n   443:     /// assert_eq!(line_num, 125);\n   444:     /// assert_eq!(iter.collect::<String>(), \" GOTO 10\");\n   445:     /// ```\n   446:     #[stable(feature = \"peekable_next_if_map\", since = \"1.94.0\")]\n   447:     pub fn next_if_map_mut<R>(&mut self, f: impl FnOnce(&mut I::Item) -> Option<R>) -> Option<R> {\n   448:         let unpeek = if let Some(mut item) = self.next() {\n   449:             match f(&mut item) {\n   450:                 Some(result) => return Some(result),\n   451:                 None => Some(item),\n   452:             }\n   453:         } else {\n   454:             None\n   455:         };",
    "nanvix_source": "   429:     /// The value will be dropped.\n   430:     ///\n   431:     /// This is similar to [`next_if_map`](Self::next_if_map), except ownership of the item is not given to `f`.\n   432:     /// This can be preferable if `f` would copy the item anyway.\n   433:     ///\n   434:     /// # Examples\n   435:     ///\n   436:     /// Parse the leading decimal number from an iterator of characters.\n   437:     /// ```\n   438:     /// let mut iter = \"125 GOTO 10\".chars().peekable();\n   439:     /// let mut line_num = 0_u32;\n   440:     /// while let Some(digit) = iter.next_if_map_mut(|c| c.to_digit(10)) {\n   441:     ///     line_num = line_num * 10 + digit;\n   442:     /// }\n   443:     /// assert_eq!(line_num, 125);\n   444:     /// assert_eq!(iter.collect::<String>(), \" GOTO 10\");\n   445:     /// ```\n   446:     #[stable(feature = \"peekable_next_if_map\", since = \"1.94.0\")]\n   447:     pub fn next_if_map_mut<R>(&mut self, f: impl FnOnce(&mut I::Item) -> Option<R>) -> Option<R> {\n   448:         let unpeek = if let Some(mut item) = self.next() {\n   449:             match f(&mut item) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Peekable::peek",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "peek",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
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
                      "generic": "I"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9889,
            "path": "Peekable"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": "Iterator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "I"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:26006",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9889",
        "resolved_owner_path": [
          "core",
          "iter",
          "adapters",
          "peekable",
          "Peekable"
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
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Item",
                            "self_type": {
                              "generic": "I"
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
    "verification_source": "   200:     /// assert_eq!(iter.next(), Some(&1));\n   201:     ///\n   202:     /// assert_eq!(iter.next(), Some(&2));\n   203:     ///\n   204:     /// // The iterator does not advance even if we `peek` multiple times\n   205:     /// assert_eq!(iter.peek(), Some(&&3));\n   206:     /// assert_eq!(iter.peek(), Some(&&3));\n   207:     ///\n   208:     /// assert_eq!(iter.next(), Some(&3));\n   209:     ///\n   210:     /// // After the iterator is finished, so is `peek()`\n   211:     /// assert_eq!(iter.peek(), None);\n   212:     /// assert_eq!(iter.next(), None);\n   213:     /// ```\n   214:     #[inline]\n   215:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   216:     pub fn peek(&mut self) -> Option<&I::Item> {\n   217:         let iter = &mut self.iter;\n   218:         self.peeked.get_or_insert_with(|| iter.next()).as_ref()\n   219:     }\n   220: \n   221:     /// Returns a mutable reference to the next() value without advancing the iterator.\n   222:     ///\n   223:     /// Like [`next`], if there is a value, it is wrapped in a `Some(T)`.\n   224:     /// But if the iteration is over, `None` is returned.\n   225:     ///\n   226:     /// Because `peek_mut()` returns a reference, and many iterators iterate over\n   227:     /// references, there can be a possibly confusing situation where the\n   228:     /// return value is a double reference. You can see this effect in the examples\n   229:     /// below.\n   230:     ///\n   231:     /// [`next`]: Iterator::next\n   232:     ///",
    "nanvix_source": "   206:     /// assert_eq!(iter.peek(), Some(&&3));\n   207:     ///\n   208:     /// assert_eq!(iter.next(), Some(&3));\n   209:     ///\n   210:     /// // After the iterator is finished, so is `peek()`\n   211:     /// assert_eq!(iter.peek(), None);\n   212:     /// assert_eq!(iter.next(), None);\n   213:     /// ```\n   214:     #[inline]\n   215:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   216:     pub fn peek(&mut self) -> Option<&I::Item> {\n   217:         let iter = &mut self.iter;\n   218:         self.peeked.get_or_insert_with(|| iter.next()).as_ref()\n   219:     }\n   220: \n   221:     /// Returns a mutable reference to the next() value without advancing the iterator.\n   222:     ///\n   223:     /// Like [`next`], if there is a value, it is wrapped in a `Some(T)`.\n   224:     /// But if the iteration is over, `None` is returned.\n   225:     ///\n   226:     /// Because `peek_mut()` returns a reference, and many iterators iterate over",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::chain",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
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
            "name": "A"
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
                "generic": "A"
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
                                    "qualified_path": {
                                      "args": null,
                                      "name": "Item",
                                      "self_type": {
                                        "generic": "A"
                                      },
                                      "trait": {
                                        "args": null,
                                        "id": 80,
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
      "name": "chain",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "a",
            {
              "generic": "A"
            }
          ],
          [
            "b",
            {
              "generic": "B"
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
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "A"
                        },
                        "trait": {
                          "args": null,
                          "id": 80,
                          "path": ""
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "B"
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
            "id": 9841,
            "path": "Chain"
          }
        }
      }
    },
    "verification_source": "    48: /// use std::iter::chain;\n    49: ///\n    50: /// let a = [1, 2, 3];\n    51: /// let b = [4, 5, 6];\n    52: ///\n    53: /// let mut iter = chain(a, b);\n    54: ///\n    55: /// assert_eq!(iter.next(), Some(1));\n    56: /// assert_eq!(iter.next(), Some(2));\n    57: /// assert_eq!(iter.next(), Some(3));\n    58: /// assert_eq!(iter.next(), Some(4));\n    59: /// assert_eq!(iter.next(), Some(5));\n    60: /// assert_eq!(iter.next(), Some(6));\n    61: /// assert_eq!(iter.next(), None);\n    62: /// ```\n    63: #[stable(feature = \"iter_chain\", since = \"1.91.0\")]\n    64: pub fn chain<A, B>(a: A, b: B) -> Chain<A::IntoIter, B::IntoIter>\n    65: where\n    66:     A: IntoIterator,\n    67:     B: IntoIterator<Item = A::Item>,\n    68: {\n    69:     Chain::new(a.into_iter(), b.into_iter())\n    70: }\n    71: \n    72: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    73: impl<A, B> Iterator for Chain<A, B>\n    74: where\n    75:     A: Iterator,\n    76:     B: Iterator<Item = A::Item>,\n    77: {\n    78:     type Item = A::Item;\n    79: \n    80:     #[inline]",
    "nanvix_source": "    54: ///\n    55: /// assert_eq!(iter.next(), Some(1));\n    56: /// assert_eq!(iter.next(), Some(2));\n    57: /// assert_eq!(iter.next(), Some(3));\n    58: /// assert_eq!(iter.next(), Some(4));\n    59: /// assert_eq!(iter.next(), Some(5));\n    60: /// assert_eq!(iter.next(), Some(6));\n    61: /// assert_eq!(iter.next(), None);\n    62: /// ```\n    63: #[stable(feature = \"iter_chain\", since = \"1.91.0\")]\n    64: pub fn chain<A, B>(a: A, b: B) -> Chain<A::IntoIter, B::IntoIter>\n    65: where\n    66:     A: IntoIterator,\n    67:     B: IntoIterator<Item = A::Item>,\n    68: {\n    69:     Chain::new(a.into_iter(), b.into_iter())\n    70: }\n    71: \n    72: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    73: impl<A, B> Iterator for Chain<A, B>\n    74: where",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::empty",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
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
      "name": "empty",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
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
            "id": 9916,
            "path": "Empty"
          }
        }
      }
    },
    "verification_source": "    17: /// ```\n    18: #[stable(feature = \"iter_empty\", since = \"1.2.0\")]\n    19: #[rustc_const_stable(feature = \"const_iter_empty\", since = \"1.32.0\")]\n    20: pub const fn empty<T>() -> Empty<T> {\n    21:     Empty(marker::PhantomData)\n    22: }\n    23: \n    24: /// An iterator that yields nothing.\n    25: ///\n    26: /// This `struct` is created by the [`empty()`] function. See its documentation for more.\n    27: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n    28: #[stable(feature = \"iter_empty\", since = \"1.2.0\")]\n    29: #[rustc_diagnostic_item = \"IterEmpty\"]\n    30: pub struct Empty<T>(marker::PhantomData<fn() -> T>);\n    31: \n    32: #[stable(feature = \"core_impl_debug\", since = \"1.9.0\")]\n    33: impl<T> fmt::Debug for Empty<T> {\n    34:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n    35:         f.debug_struct(\"Empty\").finish()\n    36:     }\n    37: }\n    38: \n    39: #[stable(feature = \"iter_empty\", since = \"1.2.0\")]\n    40: impl<T> Iterator for Empty<T> {\n    41:     type Item = T;\n    42: \n    43:     fn next(&mut self) -> Option<T> {\n    44:         None\n    45:     }\n    46: \n    47:     fn size_hint(&self) -> (usize, Option<usize>) {\n    48:         (0, Some(0))\n    49:     }",
    "nanvix_source": "    23: \n    24: /// An iterator that yields nothing.\n    25: ///\n    26: /// This `struct` is created by the [`empty()`] function. See its documentation for more.\n    27: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n    28: #[stable(feature = \"iter_empty\", since = \"1.2.0\")]\n    29: #[rustc_diagnostic_item = \"IterEmpty\"]\n    30: pub struct Empty<T>(marker::PhantomData<fn() -> T>);\n    31: \n    32: #[stable(feature = \"core_impl_debug\", since = \"1.9.0\")]\n    33: impl<T> fmt::Debug for Empty<T> {\n    34:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n    35:         f.debug_struct(\"Empty\").finish()\n    36:     }\n    37: }\n    38: \n    39: #[stable(feature = \"iter_empty\", since = \"1.2.0\")]\n    40: impl<T> Iterator for Empty<T> {\n    41:     type Item = T;\n    42: \n    43:     fn next(&mut self) -> Option<T> {",
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
