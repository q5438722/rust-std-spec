For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::split_inclusive_mut",
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
      "name": "split_inclusive_mut",
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
            "id": 13444,
            "path": "SplitInclusiveMut"
          }
        }
      }
    },
    "verification_source": "  2310:     /// match `pred`. The matched element is contained in the previous\n  2311:     /// subslice as a terminator.\n  2312:     ///\n  2313:     /// # Examples\n  2314:     ///\n  2315:     /// ```\n  2316:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2317:     ///\n  2318:     /// for group in v.split_inclusive_mut(|num| *num % 3 == 0) {\n  2319:     ///     let terminator_idx = group.len()-1;\n  2320:     ///     group[terminator_idx] = 1;\n  2321:     /// }\n  2322:     /// assert_eq!(v, [10, 40, 1, 20, 1, 1]);\n  2323:     /// ```\n  2324:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  2325:     #[inline]\n  2326:     pub fn split_inclusive_mut<F>(&mut self, pred: F) -> SplitInclusiveMut<'_, T, F>\n  2327:     where\n  2328:         F: FnMut(&T) -> bool,\n  2329:     {\n  2330:         SplitInclusiveMut::new(self, pred)\n  2331:     }\n  2332: \n  2333:     /// Returns an iterator over subslices separated by elements that match\n  2334:     /// `pred`, starting at the end of the slice and working backwards.\n  2335:     /// The matched element is not contained in the subslices.\n  2336:     ///\n  2337:     /// # Examples\n  2338:     ///\n  2339:     /// ```\n  2340:     /// let slice = [11, 22, 33, 0, 44, 55];\n  2341:     /// let mut iter = slice.rsplit(|num| *num == 0);\n  2342:     ///",
    "nanvix_source": "  2319:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2320:     ///\n  2321:     /// for group in v.split_inclusive_mut(|num| *num % 3 == 0) {\n  2322:     ///     let terminator_idx = group.len()-1;\n  2323:     ///     group[terminator_idx] = 1;\n  2324:     /// }\n  2325:     /// assert_eq!(v, [10, 40, 1, 20, 1, 1]);\n  2326:     /// ```\n  2327:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  2328:     #[inline]\n  2329:     pub fn split_inclusive_mut<F>(&mut self, pred: F) -> SplitInclusiveMut<'_, T, F>\n  2330:     where\n  2331:         F: FnMut(&T) -> bool,\n  2332:     {\n  2333:         SplitInclusiveMut::new(self, pred)\n  2334:     }\n  2335: \n  2336:     /// Returns an iterator over subslices separated by elements that match\n  2337:     /// `pred`, starting at the end of the slice and working backwards.\n  2338:     /// The matched element is not contained in the subslices.\n  2339:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_mut",
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
      "name": "split_mut",
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
            "id": 13442,
            "path": "SplitMut"
          }
        }
      }
    },
    "verification_source": "  2250: \n  2251:     /// Returns an iterator over mutable subslices separated by elements that\n  2252:     /// match `pred`. The matched element is not contained in the subslices.\n  2253:     ///\n  2254:     /// # Examples\n  2255:     ///\n  2256:     /// ```\n  2257:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2258:     ///\n  2259:     /// for group in v.split_mut(|num| *num % 3 == 0) {\n  2260:     ///     group[0] = 1;\n  2261:     /// }\n  2262:     /// assert_eq!(v, [1, 40, 30, 1, 60, 1]);\n  2263:     /// ```\n  2264:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2265:     #[inline]\n  2266:     pub fn split_mut<F>(&mut self, pred: F) -> SplitMut<'_, T, F>\n  2267:     where\n  2268:         F: FnMut(&T) -> bool,\n  2269:     {\n  2270:         SplitMut::new(self, pred)\n  2271:     }\n  2272: \n  2273:     /// Returns an iterator over subslices separated by elements that match\n  2274:     /// `pred`. The matched element is contained in the end of the previous\n  2275:     /// subslice as a terminator.\n  2276:     ///\n  2277:     /// # Examples\n  2278:     ///\n  2279:     /// ```\n  2280:     /// let slice = [10, 40, 33, 20];\n  2281:     /// let mut iter = slice.split_inclusive(|num| num % 3 == 0);\n  2282:     ///",
    "nanvix_source": "  2259:     /// ```\n  2260:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2261:     ///\n  2262:     /// for group in v.split_mut(|num| *num % 3 == 0) {\n  2263:     ///     group[0] = 1;\n  2264:     /// }\n  2265:     /// assert_eq!(v, [1, 40, 30, 1, 60, 1]);\n  2266:     /// ```\n  2267:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2268:     #[inline]\n  2269:     pub fn split_mut<F>(&mut self, pred: F) -> SplitMut<'_, T, F>\n  2270:     where\n  2271:         F: FnMut(&T) -> bool,\n  2272:     {\n  2273:         SplitMut::new(self, pred)\n  2274:     }\n  2275: \n  2276:     /// Returns an iterator over subslices separated by elements that match\n  2277:     /// `pred`. The matched element is contained in the end of the previous\n  2278:     /// subslice as a terminator.\n  2279:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::splitn_mut",
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
      "name": "splitn_mut",
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
            "id": 13453,
            "path": "SplitNMut"
          }
        }
      }
    },
    "verification_source": "  2426:     ///\n  2427:     /// The last element returned, if any, will contain the remainder of the\n  2428:     /// slice.\n  2429:     ///\n  2430:     /// # Examples\n  2431:     ///\n  2432:     /// ```\n  2433:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2434:     ///\n  2435:     /// for group in v.splitn_mut(2, |num| *num % 3 == 0) {\n  2436:     ///     group[0] = 1;\n  2437:     /// }\n  2438:     /// assert_eq!(v, [1, 40, 30, 1, 60, 50]);\n  2439:     /// ```\n  2440:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2441:     #[inline]\n  2442:     pub fn splitn_mut<F>(&mut self, n: usize, pred: F) -> SplitNMut<'_, T, F>\n  2443:     where\n  2444:         F: FnMut(&T) -> bool,\n  2445:     {\n  2446:         SplitNMut::new(self.split_mut(pred), n)\n  2447:     }\n  2448: \n  2449:     /// Returns an iterator over subslices separated by elements that match\n  2450:     /// `pred` limited to returning at most `n` items. This starts at the end of\n  2451:     /// the slice and works backwards. The matched element is not contained in\n  2452:     /// the subslices.\n  2453:     ///\n  2454:     /// The last element returned, if any, will contain the remainder of the\n  2455:     /// slice.\n  2456:     ///\n  2457:     /// # Examples\n  2458:     ///",
    "nanvix_source": "  2435:     /// ```\n  2436:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2437:     ///\n  2438:     /// for group in v.splitn_mut(2, |num| *num % 3 == 0) {\n  2439:     ///     group[0] = 1;\n  2440:     /// }\n  2441:     /// assert_eq!(v, [1, 40, 30, 1, 60, 50]);\n  2442:     /// ```\n  2443:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2444:     #[inline]\n  2445:     pub fn splitn_mut<F>(&mut self, n: usize, pred: F) -> SplitNMut<'_, T, F>\n  2446:     where\n  2447:         F: FnMut(&T) -> bool,\n  2448:     {\n  2449:         SplitNMut::new(self.split_mut(pred), n)\n  2450:     }\n  2451: \n  2452:     /// Returns an iterator over subslices separated by elements that match\n  2453:     /// `pred` limited to returning at most `n` items. This starts at the end of\n  2454:     /// the slice and works backwards. The matched element is not contained in\n  2455:     /// the subslices.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::catch_unwind",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "parenthesized": {
                            "inputs": [],
                            "output": {
                              "generic": "R"
                            }
                          }
                        },
                        "id": 20,
                        "path": "FnOnce"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 394,
                        "path": "UnwindSafe"
                      }
                    }
                  }
                ],
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "catch_unwind",
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
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 561,
            "path": "crate::thread::Result"
          }
        }
      }
    },
    "verification_source": "   342: /// # Examples\n   343: ///\n   344: /// ```\n   345: /// use std::panic;\n   346: ///\n   347: /// let result = panic::catch_unwind(|| {\n   348: ///     println!(\"hello!\");\n   349: /// });\n   350: /// assert!(result.is_ok());\n   351: ///\n   352: /// let result = panic::catch_unwind(|| {\n   353: ///     panic!(\"oh no!\");\n   354: /// });\n   355: /// assert!(result.is_err());\n   356: /// ```\n   357: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   358: pub fn catch_unwind<F: FnOnce() -> R + UnwindSafe, R>(f: F) -> Result<R> {\n   359:     unsafe { panicking::catch_unwind(f) }\n   360: }\n   361: \n   362: /// Triggers a panic without invoking the panic hook.\n   363: ///\n   364: /// This is designed to be used in conjunction with [`catch_unwind`] to, for\n   365: /// example, carry a panic across a layer of C code.\n   366: ///\n   367: /// # Notes\n   368: ///\n   369: /// Note that panics in Rust are not always implemented via unwinding, but they\n   370: /// may be implemented by aborting the process. If this function is called when\n   371: /// panics are implemented this way then this function will abort the process,\n   372: /// not trigger an unwind.\n   373: ///\n   374: /// # Examples",
    "nanvix_source": "   348: ///     println!(\"hello!\");\n   349: /// });\n   350: /// assert!(result.is_ok());\n   351: ///\n   352: /// let result = panic::catch_unwind(|| {\n   353: ///     panic!(\"oh no!\");\n   354: /// });\n   355: /// assert!(result.is_err());\n   356: /// ```\n   357: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   358: pub fn catch_unwind<F: FnOnce() -> R + UnwindSafe, R>(f: F) -> Result<R> {\n   359:     unsafe { panicking::catch_unwind(f) }\n   360: }\n   361: \n   362: /// Triggers a panic without invoking the panic hook.\n   363: ///\n   364: /// This is designed to be used in conjunction with [`catch_unwind`] to, for\n   365: /// example, carry a panic across a layer of C code.\n   366: ///\n   367: /// # Notes\n   368: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::take_hook",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "other",
    "kinds": [
      "free_function"
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
      "name": "take_hook",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
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
                      "dyn_trait": {
                        "lifetime": "'static",
                        "traits": [
                          {
                            "generic_params": [],
                            "trait": {
                              "args": {
                                "parenthesized": {
                                  "inputs": [
                                    {
                                      "borrowed_ref": {
                                        "is_mutable": false,
                                        "lifetime": null,
                                        "type": {
                                          "resolved_path": {
                                            "args": {
                                              "angle_bracketed": {
                                                "args": [
                                                  {
                                                    "lifetime": "'_"
                                                  }
                                                ],
                                                "constraints": []
                                              }
                                            },
                                            "id": 6615,
                                            "path": "crate::panic::PanicHookInfo"
                                          }
                                        }
                                      }
                                    }
                                  ],
                                  "output": null
                                }
                              },
                              "id": 16,
                              "path": "Fn"
                            }
                          },
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 10,
                              "path": "Sync"
                            }
                          },
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 6,
                              "path": "Send"
                            }
                          }
                        ]
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 216,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "   166: ///\n   167: /// The following will print \"Normal panic\":\n   168: ///\n   169: /// ```should_panic\n   170: /// use std::panic;\n   171: ///\n   172: /// panic::set_hook(Box::new(|_| {\n   173: ///     println!(\"Custom panic hook\");\n   174: /// }));\n   175: ///\n   176: /// let _ = panic::take_hook();\n   177: ///\n   178: /// panic!(\"Normal panic\");\n   179: /// ```\n   180: #[must_use]\n   181: #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   182: pub fn take_hook() -> Box<dyn Fn(&PanicHookInfo<'_>) + 'static + Sync + Send> {\n   183:     if thread::panicking() {\n   184:         panic!(\"cannot modify the panic hook from a panicking thread\");\n   185:     }\n   186: \n   187:     HOOK.replace(Hook::Default).into_box()\n   188: }\n   189: \n   190: /// Atomic combination of [`take_hook`] and [`set_hook`]. Use this to replace the panic handler with\n   191: /// a new panic handler that does something and then executes the old handler.\n   192: ///\n   193: /// [`take_hook`]: ./fn.take_hook.html\n   194: /// [`set_hook`]: ./fn.set_hook.html\n   195: ///\n   196: /// # Panics\n   197: ///\n   198: /// Panics if called from a panicking thread.",
    "nanvix_source": "   172: /// panic::set_hook(Box::new(|_| {\n   173: ///     println!(\"Custom panic hook\");\n   174: /// }));\n   175: ///\n   176: /// let _ = panic::take_hook();\n   177: ///\n   178: /// panic!(\"Normal panic\");\n   179: /// ```\n   180: #[must_use]\n   181: #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   182: pub fn take_hook() -> Box<dyn Fn(&PanicHookInfo<'_>) + 'static + Sync + Send> {\n   183:     if thread::panicking() {\n   184:         panic!(\"cannot modify the panic hook from a panicking thread\");\n   185:     }\n   186: \n   187:     HOOK.replace(Hook::Default).into_box()\n   188: }\n   189: \n   190: /// Atomic combination of [`take_hook`] and [`set_hook`]. Use this to replace the panic handler with\n   191: /// a new panic handler that does something and then executes the old handler.\n   192: ///",
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
