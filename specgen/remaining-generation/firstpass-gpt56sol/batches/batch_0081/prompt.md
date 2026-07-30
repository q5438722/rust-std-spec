For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::rsplit",
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
      "name": "rsplit",
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
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 10057,
            "path": "RSplit"
          }
        }
      }
    },
    "verification_source": "  2346:     /// ```\n  2347:     ///\n  2348:     /// As with `split()`, if the first or last element is matched, an empty\n  2349:     /// slice will be the first (or last) item returned by the iterator.\n  2350:     ///\n  2351:     /// ```\n  2352:     /// let v = &[0, 1, 1, 2, 3, 5, 8];\n  2353:     /// let mut it = v.rsplit(|n| *n % 2 == 0);\n  2354:     /// assert_eq!(it.next().unwrap(), &[]);\n  2355:     /// assert_eq!(it.next().unwrap(), &[3, 5]);\n  2356:     /// assert_eq!(it.next().unwrap(), &[1, 1]);\n  2357:     /// assert_eq!(it.next().unwrap(), &[]);\n  2358:     /// assert_eq!(it.next(), None);\n  2359:     /// ```\n  2360:     #[stable(feature = \"slice_rsplit\", since = \"1.27.0\")]\n  2361:     #[inline]\n  2362:     pub fn rsplit<F>(&self, pred: F) -> RSplit<'_, T, F>\n  2363:     where\n  2364:         F: FnMut(&T) -> bool,\n  2365:     {\n  2366:         RSplit::new(self, pred)\n  2367:     }\n  2368: \n  2369:     /// Returns an iterator over mutable subslices separated by elements that\n  2370:     /// match `pred`, starting at the end of the slice and working\n  2371:     /// backwards. The matched element is not contained in the subslices.\n  2372:     ///\n  2373:     /// # Examples\n  2374:     ///\n  2375:     /// ```\n  2376:     /// let mut v = [100, 400, 300, 200, 600, 500];\n  2377:     ///\n  2378:     /// let mut count = 0;",
    "nanvix_source": "  2355:     /// let v = &[0, 1, 1, 2, 3, 5, 8];\n  2356:     /// let mut it = v.rsplit(|n| *n % 2 == 0);\n  2357:     /// assert_eq!(it.next().unwrap(), &[]);\n  2358:     /// assert_eq!(it.next().unwrap(), &[3, 5]);\n  2359:     /// assert_eq!(it.next().unwrap(), &[1, 1]);\n  2360:     /// assert_eq!(it.next().unwrap(), &[]);\n  2361:     /// assert_eq!(it.next(), None);\n  2362:     /// ```\n  2363:     #[stable(feature = \"slice_rsplit\", since = \"1.27.0\")]\n  2364:     #[inline]\n  2365:     pub fn rsplit<F>(&self, pred: F) -> RSplit<'_, T, F>\n  2366:     where\n  2367:         F: FnMut(&T) -> bool,\n  2368:     {\n  2369:         RSplit::new(self, pred)\n  2370:     }\n  2371: \n  2372:     /// Returns an iterator over mutable subslices separated by elements that\n  2373:     /// match `pred`, starting at the end of the slice and working\n  2374:     /// backwards. The matched element is not contained in the subslices.\n  2375:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rsplit_mut",
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
      "name": "rsplit_mut",
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 13447,
            "path": "RSplitMut"
          }
        }
      }
    },
    "verification_source": "  2372:     ///\n  2373:     /// # Examples\n  2374:     ///\n  2375:     /// ```\n  2376:     /// let mut v = [100, 400, 300, 200, 600, 500];\n  2377:     ///\n  2378:     /// let mut count = 0;\n  2379:     /// for group in v.rsplit_mut(|num| *num % 3 == 0) {\n  2380:     ///     count += 1;\n  2381:     ///     group[0] = count;\n  2382:     /// }\n  2383:     /// assert_eq!(v, [3, 400, 300, 2, 600, 1]);\n  2384:     /// ```\n  2385:     ///\n  2386:     #[stable(feature = \"slice_rsplit\", since = \"1.27.0\")]\n  2387:     #[inline]\n  2388:     pub fn rsplit_mut<F>(&mut self, pred: F) -> RSplitMut<'_, T, F>\n  2389:     where\n  2390:         F: FnMut(&T) -> bool,\n  2391:     {\n  2392:         RSplitMut::new(self, pred)\n  2393:     }\n  2394: \n  2395:     /// Returns an iterator over subslices separated by elements that match\n  2396:     /// `pred`, limited to returning at most `n` items. The matched element is\n  2397:     /// not contained in the subslices.\n  2398:     ///\n  2399:     /// The last element returned, if any, will contain the remainder of the\n  2400:     /// slice.\n  2401:     ///\n  2402:     /// # Examples\n  2403:     ///\n  2404:     /// Print the slice split once by numbers divisible by 3 (i.e., `[10, 40]`,",
    "nanvix_source": "  2381:     /// let mut count = 0;\n  2382:     /// for group in v.rsplit_mut(|num| *num % 3 == 0) {\n  2383:     ///     count += 1;\n  2384:     ///     group[0] = count;\n  2385:     /// }\n  2386:     /// assert_eq!(v, [3, 400, 300, 2, 600, 1]);\n  2387:     /// ```\n  2388:     ///\n  2389:     #[stable(feature = \"slice_rsplit\", since = \"1.27.0\")]\n  2390:     #[inline]\n  2391:     pub fn rsplit_mut<F>(&mut self, pred: F) -> RSplitMut<'_, T, F>\n  2392:     where\n  2393:         F: FnMut(&T) -> bool,\n  2394:     {\n  2395:         RSplitMut::new(self, pred)\n  2396:     }\n  2397: \n  2398:     /// Returns an iterator over subslices separated by elements that match\n  2399:     /// `pred`, limited to returning at most `n` items. The matched element is\n  2400:     /// not contained in the subslices.\n  2401:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rsplitn",
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
      "name": "rsplitn",
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
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "n",
            {
              "primitive": "usize"
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 13451,
            "path": "RSplitN"
          }
        }
      }
    },
    "verification_source": "  2455:     /// slice.\n  2456:     ///\n  2457:     /// # Examples\n  2458:     ///\n  2459:     /// Print the slice split once, starting from the end, by numbers divisible\n  2460:     /// by 3 (i.e., `[50]`, `[10, 40, 30, 20]`):\n  2461:     ///\n  2462:     /// ```\n  2463:     /// let v = [10, 40, 30, 20, 60, 50];\n  2464:     ///\n  2465:     /// for group in v.rsplitn(2, |num| *num % 3 == 0) {\n  2466:     ///     println!(\"{group:?}\");\n  2467:     /// }\n  2468:     /// ```\n  2469:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2470:     #[inline]\n  2471:     pub fn rsplitn<F>(&self, n: usize, pred: F) -> RSplitN<'_, T, F>\n  2472:     where\n  2473:         F: FnMut(&T) -> bool,\n  2474:     {\n  2475:         RSplitN::new(self.rsplit(pred), n)\n  2476:     }\n  2477: \n  2478:     /// Returns an iterator over subslices separated by elements that match\n  2479:     /// `pred` limited to returning at most `n` items. This starts at the end of\n  2480:     /// the slice and works backwards. The matched element is not contained in\n  2481:     /// the subslices.\n  2482:     ///\n  2483:     /// The last element returned, if any, will contain the remainder of the\n  2484:     /// slice.\n  2485:     ///\n  2486:     /// # Examples\n  2487:     ///",
    "nanvix_source": "  2464:     ///\n  2465:     /// ```\n  2466:     /// let v = [10, 40, 30, 20, 60, 50];\n  2467:     ///\n  2468:     /// for group in v.rsplitn(2, |num| *num % 3 == 0) {\n  2469:     ///     println!(\"{group:?}\");\n  2470:     /// }\n  2471:     /// ```\n  2472:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2473:     #[inline]\n  2474:     pub fn rsplitn<F>(&self, n: usize, pred: F) -> RSplitN<'_, T, F>\n  2475:     where\n  2476:         F: FnMut(&T) -> bool,\n  2477:     {\n  2478:         RSplitN::new(self.rsplit(pred), n)\n  2479:     }\n  2480: \n  2481:     /// Returns an iterator over subslices separated by elements that match\n  2482:     /// `pred` limited to returning at most `n` items. This starts at the end of\n  2483:     /// the slice and works backwards. The matched element is not contained in\n  2484:     /// the subslices.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rsplitn_mut",
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
      "name": "rsplitn_mut",
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "n",
            {
              "primitive": "usize"
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 13455,
            "path": "RSplitNMut"
          }
        }
      }
    },
    "verification_source": "  2482:     ///\n  2483:     /// The last element returned, if any, will contain the remainder of the\n  2484:     /// slice.\n  2485:     ///\n  2486:     /// # Examples\n  2487:     ///\n  2488:     /// ```\n  2489:     /// let mut s = [10, 40, 30, 20, 60, 50];\n  2490:     ///\n  2491:     /// for group in s.rsplitn_mut(2, |num| *num % 3 == 0) {\n  2492:     ///     group[0] = 1;\n  2493:     /// }\n  2494:     /// assert_eq!(s, [1, 40, 30, 20, 60, 1]);\n  2495:     /// ```\n  2496:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2497:     #[inline]\n  2498:     pub fn rsplitn_mut<F>(&mut self, n: usize, pred: F) -> RSplitNMut<'_, T, F>\n  2499:     where\n  2500:         F: FnMut(&T) -> bool,\n  2501:     {\n  2502:         RSplitNMut::new(self.rsplit_mut(pred), n)\n  2503:     }\n  2504: \n  2505:     /// Splits the slice on the first element that matches the specified\n  2506:     /// predicate.\n  2507:     ///\n  2508:     /// If any matching elements are present in the slice, returns the prefix\n  2509:     /// before the match and suffix after. The matching element itself is not\n  2510:     /// included. If no elements match, returns `None`.\n  2511:     ///\n  2512:     /// # Examples\n  2513:     ///\n  2514:     /// ```",
    "nanvix_source": "  2491:     /// ```\n  2492:     /// let mut s = [10, 40, 30, 20, 60, 50];\n  2493:     ///\n  2494:     /// for group in s.rsplitn_mut(2, |num| *num % 3 == 0) {\n  2495:     ///     group[0] = 1;\n  2496:     /// }\n  2497:     /// assert_eq!(s, [1, 40, 30, 20, 60, 1]);\n  2498:     /// ```\n  2499:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2500:     #[inline]\n  2501:     pub fn rsplitn_mut<F>(&mut self, n: usize, pred: F) -> RSplitNMut<'_, T, F>\n  2502:     where\n  2503:         F: FnMut(&T) -> bool,\n  2504:     {\n  2505:         RSplitNMut::new(self.rsplit_mut(pred), n)\n  2506:     }\n  2507: \n  2508:     /// Splits the slice on the first element that matches the specified\n  2509:     /// predicate.\n  2510:     ///\n  2511:     /// If any matching elements are present in the slice, returns the prefix",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::sort_unstable_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
                    "modifier": "none",
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
                            },
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
      "name": "sort_unstable_by",
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "compare",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3172:     /// # Examples\n  3173:     ///\n  3174:     /// ```\n  3175:     /// let mut v = [4, -5, 1, -3, 2];\n  3176:     /// v.sort_unstable_by(|a, b| a.cmp(b));\n  3177:     /// assert_eq!(v, [-5, -3, 1, 2, 4]);\n  3178:     ///\n  3179:     /// // reverse sorting\n  3180:     /// v.sort_unstable_by(|a, b| b.cmp(a));\n  3181:     /// assert_eq!(v, [4, 2, 1, -3, -5]);\n  3182:     /// ```\n  3183:     ///\n  3184:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3185:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3186:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3187:     #[inline]\n  3188:     pub fn sort_unstable_by<F>(&mut self, mut compare: F)\n  3189:     where\n  3190:         F: FnMut(&T, &T) -> Ordering,\n  3191:     {\n  3192:         sort::unstable::sort(self, &mut |a, b| compare(a, b) == Ordering::Less);\n  3193:     }\n  3194: \n  3195:     /// Sorts the slice in ascending order with a key extraction function, **without** preserving\n  3196:     /// the initial order of equal elements.\n  3197:     ///\n  3198:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not\n  3199:     /// allocate), and *O*(*n* \\* log(*n*)) worst-case.\n  3200:     ///\n  3201:     /// If the implementation of [`Ord`] for `K` does not implement a [total order], the function\n  3202:     /// may panic; even if the function exits normally, the resulting order of elements in the slice\n  3203:     /// is unspecified. See also the note on panicking below.\n  3204:     ///",
    "nanvix_source": "  3184:     ///\n  3185:     /// // reverse sorting\n  3186:     /// v.sort_unstable_by(|a, b| b.cmp(a));\n  3187:     /// assert_eq!(v, [4, 2, 1, -3, -5]);\n  3188:     /// ```\n  3189:     ///\n  3190:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3191:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3192:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3193:     #[inline]\n  3194:     pub fn sort_unstable_by<F>(&mut self, mut compare: F)\n  3195:     where\n  3196:         F: FnMut(&T, &T) -> Ordering,\n  3197:     {\n  3198:         sort::unstable::sort(self, &mut |a, b| compare(a, b) == Ordering::Less);\n  3199:     }\n  3200: \n  3201:     /// Sorts the slice in ascending order with a key extraction function, **without** preserving\n  3202:     /// the initial order of equal elements.\n  3203:     ///\n  3204:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::sort_unstable_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
            "name": "K"
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
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "K"
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
                "generic": "K"
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
      "name": "sort_unstable_by_key",
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
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3224:     /// May panic if the implementation of [`Ord`] for `K` does not implement a [total order], or if\n  3225:     /// the [`Ord`] implementation panics.\n  3226:     ///\n  3227:     /// # Examples\n  3228:     ///\n  3229:     /// ```\n  3230:     /// let mut v = [4i32, -5, 1, -3, 2];\n  3231:     ///\n  3232:     /// v.sort_unstable_by_key(|k| k.abs());\n  3233:     /// assert_eq!(v, [1, 2, -3, 4, -5]);\n  3234:     /// ```\n  3235:     ///\n  3236:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3237:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3238:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3239:     #[inline]\n  3240:     pub fn sort_unstable_by_key<K, F>(&mut self, mut f: F)\n  3241:     where\n  3242:         F: FnMut(&T) -> K,\n  3243:         K: Ord,\n  3244:     {\n  3245:         sort::unstable::sort(self, &mut |a, b| f(a).lt(&f(b)));\n  3246:     }\n  3247: \n  3248:     /// Partially sorts the slice in ascending order **without** preserving the initial order of equal elements.\n  3249:     ///\n  3250:     /// Upon completion, for the specified range `start..end`, it's guaranteed that:\n  3251:     ///\n  3252:     /// 1. Every element in `self[..start]` is smaller than or equal to\n  3253:     /// 2. Every element in `self[start..end]`, which is sorted, and smaller than or equal to\n  3254:     /// 3. Every element in `self[end..]`.\n  3255:     ///\n  3256:     /// This partial sort is unstable, meaning it may reorder equal elements in the specified range.",
    "nanvix_source": "  3236:     /// let mut v = [4i32, -5, 1, -3, 2];\n  3237:     ///\n  3238:     /// v.sort_unstable_by_key(|k| k.abs());\n  3239:     /// assert_eq!(v, [1, 2, -3, 4, -5]);\n  3240:     /// ```\n  3241:     ///\n  3242:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3243:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3244:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3245:     #[inline]\n  3246:     pub fn sort_unstable_by_key<K, F>(&mut self, mut f: F)\n  3247:     where\n  3248:         F: FnMut(&T) -> K,\n  3249:         K: Ord,\n  3250:     {\n  3251:         sort::unstable::sort(self, &mut |a, b| f(a).lt(&f(b)));\n  3252:     }\n  3253: \n  3254:     /// Partially sorts the slice in ascending order **without** preserving the initial order of equal elements.\n  3255:     ///\n  3256:     /// Upon completion, for the specified range `start..end`, it's guaranteed that:",
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
