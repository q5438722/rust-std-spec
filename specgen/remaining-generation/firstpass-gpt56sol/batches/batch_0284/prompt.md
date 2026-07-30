For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::DoubleEndedIterator::rfold",
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
                            },
                            {
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "rfold",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:74",
        "kind": "trait",
        "name": "DoubleEndedIterator",
        "path": [
          "core",
          "iter",
          "traits",
          "double_ended",
          "DoubleEndedIterator"
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
            "init",
            {
              "generic": "B"
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
          "generic": "B"
        }
      }
    },
    "verification_source": "   289:     /// and continuing with each element from the back until the front:\n   290:     ///\n   291:     /// ```\n   292:     /// let numbers = [1, 2, 3, 4, 5];\n   293:     ///\n   294:     /// let zero = \"0\".to_string();\n   295:     ///\n   296:     /// let result = numbers.iter().rfold(zero, |acc, &x| {\n   297:     ///     format!(\"({x} + {acc})\")\n   298:     /// });\n   299:     ///\n   300:     /// assert_eq!(result, \"(1 + (2 + (3 + (4 + (5 + 0)))))\");\n   301:     /// ```\n   302:     #[doc(alias = \"foldr\")]\n   303:     #[inline]\n   304:     #[stable(feature = \"iter_rfold\", since = \"1.27.0\")]\n   305:     fn rfold<B, F>(mut self, init: B, mut f: F) -> B\n   306:     where\n   307:         Self: Sized + [const] Destruct,\n   308:         F: [const] FnMut(B, Self::Item) -> B + [const] Destruct,\n   309:     {\n   310:         let mut accum = init;\n   311:         while let Some(x) = self.next_back() {\n   312:             accum = f(accum, x);\n   313:         }\n   314:         accum\n   315:     }\n   316: \n   317:     /// Searches for an element of an iterator from the back that satisfies a predicate.\n   318:     ///\n   319:     /// `rfind()` takes a closure that returns `true` or `false`. It applies\n   320:     /// this closure to each element of the iterator, starting at the end, and if any\n   321:     /// of them return `true`, then `rfind()` returns [`Some(element)`]. If they all return",
    "nanvix_source": "   343:     ///\n   344:     /// let result = numbers.iter().rfold(zero, |acc, &x| {\n   345:     ///     format!(\"({x} + {acc})\")\n   346:     /// });\n   347:     ///\n   348:     /// assert_eq!(result, \"(1 + (2 + (3 + (4 + (5 + 0)))))\");\n   349:     /// ```\n   350:     #[doc(alias = \"foldr\")]\n   351:     #[inline]\n   352:     #[stable(feature = \"iter_rfold\", since = \"1.27.0\")]\n   353:     fn rfold<B, F>(mut self, init: B, mut f: F) -> B\n   354:     where\n   355:         Self: Sized + [const] Destruct,\n   356:         F: [const] FnMut(B, Self::Item) -> B + [const] Destruct,\n   357:     {\n   358:         let mut accum = init;\n   359:         while let Some(x) = self.next_back() {\n   360:             accum = f(accum, x);\n   361:         }\n   362:         accum\n   363:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::DoubleEndedIterator::try_rfold",
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
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
                            },
                            {
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
                          ],
                          "output": {
                            "generic": "R"
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
                    "modifier": "maybe_const",
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
                                    "generic": "B"
                                  }
                                }
                              },
                              "name": "Output"
                            }
                          ]
                        }
                      },
                      "id": 12972,
                      "path": "Try"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "R"
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
      "name": "try_rfold",
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
        "item_id": "core:74",
        "kind": "trait",
        "name": "DoubleEndedIterator",
        "path": [
          "core",
          "iter",
          "traits",
          "double_ended",
          "DoubleEndedIterator"
        ]
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
            "init",
            {
              "generic": "B"
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
          "generic": "R"
        }
      }
    },
    "verification_source": "   218:     ///\n   219:     /// ```\n   220:     /// let a = [\"1\", \"rust\", \"3\"];\n   221:     /// let mut it = a.iter();\n   222:     /// let sum = it\n   223:     ///     .by_ref()\n   224:     ///     .map(|&s| s.parse::<i32>())\n   225:     ///     .try_rfold(0, |acc, x| x.and_then(|y| Ok(acc + y)));\n   226:     /// assert!(sum.is_err());\n   227:     ///\n   228:     /// // Because it short-circuited, the remaining elements are still\n   229:     /// // available through the iterator.\n   230:     /// assert_eq!(it.next_back(), Some(&\"1\"));\n   231:     /// ```\n   232:     #[inline]\n   233:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n   234:     fn try_rfold<B, F, R>(&mut self, init: B, mut f: F) -> R\n   235:     where\n   236:         Self: Sized,\n   237:         F: [const] FnMut(B, Self::Item) -> R + [const] Destruct,\n   238:         R: [const] Try<Output = B>,\n   239:     {\n   240:         let mut accum = init;\n   241:         while let Some(x) = self.next_back() {\n   242:             accum = f(accum, x)?;\n   243:         }\n   244:         try { accum }\n   245:     }\n   246: \n   247:     /// An iterator method that reduces the iterator's elements to a single,\n   248:     /// final value, starting from the back.\n   249:     ///\n   250:     /// This is the reverse version of [`Iterator::fold()`]: it takes elements",
    "nanvix_source": "   272:     ///     .map(|&s| s.parse::<i32>())\n   273:     ///     .try_rfold(0, |acc, x| x.and_then(|y| Ok(acc + y)));\n   274:     /// assert!(sum.is_err());\n   275:     ///\n   276:     /// // Because it short-circuited, the remaining elements are still\n   277:     /// // available through the iterator.\n   278:     /// assert_eq!(it.next_back(), Some(&\"1\"));\n   279:     /// ```\n   280:     #[inline]\n   281:     #[stable(feature = \"iterator_try_fold\", since = \"1.27.0\")]\n   282:     fn try_rfold<B, F, R>(&mut self, init: B, mut f: F) -> R\n   283:     where\n   284:         Self: Sized,\n   285:         F: [const] FnMut(B, Self::Item) -> R + [const] Destruct,\n   286:         R: [const] Try<Output = B>,\n   287:     {\n   288:         let mut accum = init;\n   289:         while let Some(x) = self.next_back() {\n   290:             accum = f(accum, x)?;\n   291:         }\n   292:         try { accum }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::ExactSizeIterator::len",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "len",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:76",
        "kind": "trait",
        "name": "ExactSizeIterator",
        "path": [
          "core",
          "iter",
          "traits",
          "exact_size",
          "ExactSizeIterator"
        ]
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   100:     /// [`Some(T)`]: Some\n   101:     ///\n   102:     /// # Examples\n   103:     ///\n   104:     /// Basic usage:\n   105:     ///\n   106:     /// ```\n   107:     /// // a finite range knows exactly how many times it will iterate\n   108:     /// let mut range = 0..5;\n   109:     ///\n   110:     /// assert_eq!(5, range.len());\n   111:     /// let _ = range.next();\n   112:     /// assert_eq!(4, range.len());\n   113:     /// ```\n   114:     #[inline]\n   115:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   116:     fn len(&self) -> usize {\n   117:         let (lower, upper) = self.size_hint();\n   118:         // Note: This assertion is overly defensive, but it checks the invariant\n   119:         // guaranteed by the trait. If this trait were rust-internal,\n   120:         // we could use debug_assert!; assert_eq! will check all Rust user\n   121:         // implementations too.\n   122:         assert_eq!(upper, Some(lower));\n   123:         lower\n   124:     }\n   125: \n   126:     /// Returns `true` if the iterator is empty.\n   127:     ///\n   128:     /// This method has a default implementation using\n   129:     /// [`ExactSizeIterator::len()`], so you don't need to implement it yourself.\n   130:     ///\n   131:     /// # Examples\n   132:     ///",
    "nanvix_source": "   106:     /// ```\n   107:     /// // a finite range knows exactly how many times it will iterate\n   108:     /// let mut range = 0..5;\n   109:     ///\n   110:     /// assert_eq!(5, range.len());\n   111:     /// let _ = range.next();\n   112:     /// assert_eq!(4, range.len());\n   113:     /// ```\n   114:     #[inline]\n   115:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   116:     fn len(&self) -> usize {\n   117:         let (lower, upper) = self.size_hint();\n   118:         // Note: This assertion is overly defensive, but it checks the invariant\n   119:         // guaranteed by the trait. If this trait were rust-internal,\n   120:         // we could use debug_assert!; assert_eq! will check all Rust user\n   121:         // implementations too.\n   122:         assert_eq!(upper, Some(lower));\n   123:         lower\n   124:     }\n   125: \n   126:     /// Returns `true` if the iterator is empty.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Extend::extend",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                                      "generic": "A"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "extend",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:78",
        "kind": "trait",
        "name": "Extend",
        "path": [
          "core",
          "iter",
          "traits",
          "collect",
          "Extend"
        ]
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
            "iter",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   400:     /// As this is the only required method for this trait, the [trait-level] docs\n   401:     /// contain more details.\n   402:     ///\n   403:     /// [trait-level]: Extend\n   404:     ///\n   405:     /// # Examples\n   406:     ///\n   407:     /// ```\n   408:     /// // You can extend a String with some chars:\n   409:     /// let mut message = String::from(\"abc\");\n   410:     ///\n   411:     /// message.extend(['d', 'e', 'f'].iter());\n   412:     ///\n   413:     /// assert_eq!(\"abcdef\", &message);\n   414:     /// ```\n   415:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   416:     fn extend<T: IntoIterator<Item = A>>(&mut self, iter: T);\n   417: \n   418:     /// Extends a collection with exactly one element.\n   419:     #[unstable(feature = \"extend_one\", issue = \"72631\")]\n   420:     fn extend_one(&mut self, item: A) {\n   421:         self.extend(Some(item));\n   422:     }\n   423: \n   424:     /// Reserves capacity in a collection for the given number of additional elements.\n   425:     ///\n   426:     /// The default implementation does nothing.\n   427:     #[unstable(feature = \"extend_one\", issue = \"72631\")]\n   428:     fn extend_reserve(&mut self, additional: usize) {\n   429:         let _ = additional;\n   430:     }\n   431: \n   432:     /// Extends a collection with one element, without checking there is enough capacity for it.",
    "nanvix_source": "   406:     ///\n   407:     /// ```\n   408:     /// // You can extend a String with some chars:\n   409:     /// let mut message = String::from(\"abc\");\n   410:     ///\n   411:     /// message.extend(['d', 'e', 'f'].iter());\n   412:     ///\n   413:     /// assert_eq!(\"abcdef\", &message);\n   414:     /// ```\n   415:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   416:     fn extend<T: IntoIterator<Item = A>>(&mut self, iter: T);\n   417: \n   418:     /// Extends a collection with exactly one element.\n   419:     #[unstable(feature = \"extend_one\", issue = \"72631\")]\n   420:     fn extend_one(&mut self, item: A) {\n   421:         self.extend(Some(item));\n   422:     }\n   423: \n   424:     /// Reserves capacity in a collection for the given number of additional elements.\n   425:     ///\n   426:     /// The default implementation does nothing.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::by_ref",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
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
      "name": "by_ref",
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
    "verification_source": "  1940:     ///\n  1941:     /// # Examples\n  1942:     ///\n  1943:     /// ```\n  1944:     /// let mut words = [\"hello\", \"world\", \"of\", \"Rust\"].into_iter();\n  1945:     ///\n  1946:     /// // Take the first two words.\n  1947:     /// let hello_world: Vec<_> = words.by_ref().take(2).collect();\n  1948:     /// assert_eq!(hello_world, vec![\"hello\", \"world\"]);\n  1949:     ///\n  1950:     /// // Collect the rest of the words.\n  1951:     /// // We can only do this because we used `by_ref` earlier.\n  1952:     /// let of_rust: Vec<_> = words.collect();\n  1953:     /// assert_eq!(of_rust, vec![\"of\", \"Rust\"]);\n  1954:     /// ```\n  1955:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1956:     fn by_ref(&mut self) -> &mut Self\n  1957:     where\n  1958:         Self: Sized,\n  1959:     {\n  1960:         self\n  1961:     }\n  1962: \n  1963:     /// Transforms an iterator into a collection.\n  1964:     ///\n  1965:     /// `collect()` takes ownership of an iterator and produces whichever\n  1966:     /// collection type you request. The iterator itself carries no knowledge of\n  1967:     /// the eventual container; the target collection is chosen entirely by the\n  1968:     /// type you ask `collect()` to return. This makes `collect()` one of the\n  1969:     /// more powerful methods in the standard library, and it shows up in a wide\n  1970:     /// variety of contexts.\n  1971:     ///\n  1972:     /// The most basic pattern in which `collect()` is used is to turn one",
    "nanvix_source": "  1944:     /// // Take the first two words.\n  1945:     /// let hello_world: Vec<_> = words.by_ref().take(2).collect();\n  1946:     /// assert_eq!(hello_world, vec![\"hello\", \"world\"]);\n  1947:     ///\n  1948:     /// // Collect the rest of the words.\n  1949:     /// // We can only do this because we used `by_ref` earlier.\n  1950:     /// let of_rust: Vec<_> = words.collect();\n  1951:     /// assert_eq!(of_rust, vec![\"of\", \"Rust\"]);\n  1952:     /// ```\n  1953:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1954:     fn by_ref(&mut self) -> &mut Self\n  1955:     where\n  1956:         Self: Sized,\n  1957:     {\n  1958:         self\n  1959:     }\n  1960: \n  1961:     /// Transforms an iterator into a collection.\n  1962:     ///\n  1963:     /// `collect()` takes ownership of an iterator and produces whichever\n  1964:     /// collection type you request. The iterator itself carries no knowledge of",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::chain",
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
            "name": "U"
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
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
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
                "generic": "U"
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
              "generic": "U"
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
                  },
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "U"
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
    "verification_source": "   496:     /// ```\n   497:     ///\n   498:     /// If you work with Windows API, you may wish to convert [`OsStr`] to `Vec<u16>`:\n   499:     ///\n   500:     /// ```\n   501:     /// #[cfg(windows)]\n   502:     /// fn os_str_to_utf16(s: &std::ffi::OsStr) -> Vec<u16> {\n   503:     ///     use std::os::windows::ffi::OsStrExt;\n   504:     ///     s.encode_wide().chain(std::iter::once(0)).collect()\n   505:     /// }\n   506:     /// ```\n   507:     ///\n   508:     /// [`once`]: crate::iter::once\n   509:     /// [`OsStr`]: ../../std/ffi/struct.OsStr.html\n   510:     #[inline]\n   511:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   512:     fn chain<U>(self, other: U) -> Chain<Self, U::IntoIter>\n   513:     where\n   514:         Self: Sized,\n   515:         U: [const] IntoIterator<Item = Self::Item>,\n   516:     {\n   517:         Chain::new(self, other.into_iter())\n   518:     }\n   519: \n   520:     /// 'Zips up' two iterators into a single iterator of pairs.\n   521:     ///\n   522:     /// `zip()` returns a new iterator that will iterate over two other\n   523:     /// iterators, returning a tuple where the first element comes from the\n   524:     /// first iterator, and the second element comes from the second iterator.\n   525:     ///\n   526:     /// In other words, it zips two iterators together, into a single one.\n   527:     ///\n   528:     /// If either iterator returns [`None`], [`next`] from the zipped iterator",
    "nanvix_source": "   500:     /// fn os_str_to_utf16(s: &std::ffi::OsStr) -> Vec<u16> {\n   501:     ///     use std::os::windows::ffi::OsStrExt;\n   502:     ///     s.encode_wide().chain(std::iter::once(0)).collect()\n   503:     /// }\n   504:     /// ```\n   505:     ///\n   506:     /// [`once`]: crate::iter::once\n   507:     /// [`OsStr`]: ../../std/ffi/struct.OsStr.html\n   508:     #[inline]\n   509:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   510:     fn chain<U>(self, other: U) -> Chain<Self, U::IntoIter>\n   511:     where\n   512:         Self: Sized,\n   513:         U: [const] IntoIterator<Item = Self::Item>,\n   514:     {\n   515:         Chain::new(self, other.into_iter())\n   516:     }\n   517: \n   518:     /// 'Zips up' two iterators into a single iterator of pairs.\n   519:     ///\n   520:     /// `zip()` returns a new iterator that will iterate over two other",
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
