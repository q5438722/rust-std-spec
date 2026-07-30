For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::vec::Vec::drain",
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "primitive": "usize"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 1409,
                      "path": "RangeBounds"
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
      "name": "drain",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "range",
            {
              "generic": "R"
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4735,
            "path": "Drain"
          }
        }
      }
    },
    "verification_source": "  2932:     /// [`mem::forget`], for example), the vector may have lost and leaked\n  2933:     /// elements arbitrarily, including elements outside the range.\n  2934:     ///\n  2935:     /// # Examples\n  2936:     ///\n  2937:     /// ```\n  2938:     /// let mut v = vec![1, 2, 3];\n  2939:     /// let u: Vec<_> = v.drain(1..).collect();\n  2940:     /// assert_eq!(v, &[1]);\n  2941:     /// assert_eq!(u, &[2, 3]);\n  2942:     ///\n  2943:     /// // A full range clears the vector, like `clear()` does\n  2944:     /// v.drain(..);\n  2945:     /// assert_eq!(v, &[]);\n  2946:     /// ```\n  2947:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  2948:     pub fn drain<R>(&mut self, range: R) -> Drain<'_, T, A>\n  2949:     where\n  2950:         R: RangeBounds<usize>,\n  2951:     {\n  2952:         // Memory safety\n  2953:         //\n  2954:         // When the Drain is first created, it shortens the length of\n  2955:         // the source vector to make sure no uninitialized or moved-from elements\n  2956:         // are accessible at all if the Drain's destructor never gets to run.\n  2957:         //\n  2958:         // Drain will ptr::read out the values to remove.\n  2959:         // When finished, remaining tail of the vec is copied back to cover\n  2960:         // the hole, and the vector length is restored to the new length.\n  2961:         //\n  2962:         let len = self.len();\n  2963:         let Range { start, end } = slice::range(range, ..len);\n  2964: ",
    "nanvix_source": "  2975:     /// let mut v = vec![1, 2, 3];\n  2976:     /// let u: Vec<_> = v.drain(1..).collect();\n  2977:     /// assert_eq!(v, &[1]);\n  2978:     /// assert_eq!(u, &[2, 3]);\n  2979:     ///\n  2980:     /// // A full range clears the vector, like `clear()` does\n  2981:     /// v.drain(..);\n  2982:     /// assert_eq!(v, &[]);\n  2983:     /// ```\n  2984:     #[stable(feature = \"drain\", since = \"1.6.0\")]\n  2985:     pub fn drain<R>(&mut self, range: R) -> Drain<'_, T, A>\n  2986:     where\n  2987:         R: RangeBounds<usize>,\n  2988:     {\n  2989:         // Memory safety\n  2990:         //\n  2991:         // When the Drain is first created, it shortens the length of\n  2992:         // the source vector to make sure no uninitialized or moved-from elements\n  2993:         // are accessible at all if the Drain's destructor never gets to run.\n  2994:         //\n  2995:         // Drain will ptr::read out the values to remove.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::extract_if",
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
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": true,
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
                      "id": 534,
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
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "primitive": "usize"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 1409,
                      "path": "RangeBounds"
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
      "name": "extract_if",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4953",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "range",
            {
              "generic": "R"
            }
          ],
          [
            "filter",
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
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4672,
            "path": "ExtractIf"
          }
        }
      }
    },
    "verification_source": "  4158:     /// let evens = numbers.extract_if(.., |x| *x % 2 == 0).collect::<Vec<_>>();\n  4159:     /// let odds = numbers;\n  4160:     ///\n  4161:     /// assert_eq!(evens, vec![2, 4, 6, 8, 14]);\n  4162:     /// assert_eq!(odds, vec![1, 3, 5, 9, 11, 13, 15]);\n  4163:     /// ```\n  4164:     ///\n  4165:     /// Using the range argument to only process a part of the vector:\n  4166:     ///\n  4167:     /// ```\n  4168:     /// let mut items = vec![0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2];\n  4169:     /// let ones = items.extract_if(7.., |x| *x == 1).collect::<Vec<_>>();\n  4170:     /// assert_eq!(items, vec![0, 0, 0, 0, 0, 0, 0, 2, 2, 2]);\n  4171:     /// assert_eq!(ones.len(), 3);\n  4172:     /// ```\n  4173:     #[stable(feature = \"extract_if\", since = \"1.87.0\")]\n  4174:     pub fn extract_if<F, R>(&mut self, range: R, filter: F) -> ExtractIf<'_, T, F, A>\n  4175:     where\n  4176:         F: FnMut(&mut T) -> bool,\n  4177:         R: RangeBounds<usize>,\n  4178:     {\n  4179:         ExtractIf::new(self, filter, range)\n  4180:     }\n  4181: }\n  4182: \n  4183: /// Extend implementation that copies elements out of references before pushing them onto the Vec.\n  4184: ///\n  4185: /// This implementation is specialized for slice iterators, where it uses [`copy_from_slice`] to\n  4186: /// append the entire slice at once.\n  4187: ///\n  4188: /// [`copy_from_slice`]: slice::copy_from_slice\n  4189: #[cfg(not(no_global_oom_handling))]\n  4190: #[stable(feature = \"extend_ref\", since = \"1.2.0\")]",
    "nanvix_source": "  4214:     ///\n  4215:     /// Using the range argument to only process a part of the vector:\n  4216:     ///\n  4217:     /// ```\n  4218:     /// let mut items = vec![0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2];\n  4219:     /// let ones = items.extract_if(7.., |x| *x == 1).collect::<Vec<_>>();\n  4220:     /// assert_eq!(items, vec![0, 0, 0, 0, 0, 0, 0, 2, 2, 2]);\n  4221:     /// assert_eq!(ones.len(), 3);\n  4222:     /// ```\n  4223:     #[stable(feature = \"extract_if\", since = \"1.87.0\")]\n  4224:     pub fn extract_if<F, R>(&mut self, range: R, filter: F) -> ExtractIf<'_, T, F, A>\n  4225:     where\n  4226:         F: FnMut(&mut T) -> bool,\n  4227:         R: RangeBounds<usize>,\n  4228:     {\n  4229:         ExtractIf::new(self, filter, range)\n  4230:     }\n  4231: }\n  4232: \n  4233: /// Extend implementation that copies elements out of references before pushing them onto the Vec.\n  4234: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::retain",
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
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 534,
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
      "name": "retain",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2435:     /// let mut vec = vec![1, 2, 3, 4];\n  2436:     /// vec.retain(|&x| x % 2 == 0);\n  2437:     /// assert_eq!(vec, [2, 4]);\n  2438:     /// ```\n  2439:     ///\n  2440:     /// Because the elements are visited exactly once in the original order,\n  2441:     /// external state may be used to decide which elements to keep.\n  2442:     ///\n  2443:     /// ```\n  2444:     /// let mut vec = vec![1, 2, 3, 4, 5];\n  2445:     /// let keep = [false, true, true, false, true];\n  2446:     /// let mut iter = keep.iter();\n  2447:     /// vec.retain(|_| *iter.next().unwrap());\n  2448:     /// assert_eq!(vec, [2, 3, 5]);\n  2449:     /// ```\n  2450:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2451:     pub fn retain<F>(&mut self, mut f: F)\n  2452:     where\n  2453:         F: FnMut(&T) -> bool,\n  2454:     {\n  2455:         self.retain_mut(|elem| f(elem));\n  2456:     }\n  2457: \n  2458:     /// Retains only the elements specified by the predicate, passing a mutable reference to it.\n  2459:     ///\n  2460:     /// In other words, remove all elements `e` such that `f(&mut e)` returns `false`.\n  2461:     /// This method operates in place, visiting each element exactly once in the\n  2462:     /// original order, and preserves the order of the retained elements.\n  2463:     ///\n  2464:     /// # Examples\n  2465:     ///\n  2466:     /// ```\n  2467:     /// let mut vec = vec![1, 2, 3, 4];",
    "nanvix_source": "  2478:     /// external state may be used to decide which elements to keep.\n  2479:     ///\n  2480:     /// ```\n  2481:     /// let mut vec = vec![1, 2, 3, 4, 5];\n  2482:     /// let keep = [false, true, true, false, true];\n  2483:     /// let mut iter = keep.iter();\n  2484:     /// vec.retain(|_| *iter.next().unwrap());\n  2485:     /// assert_eq!(vec, [2, 3, 5]);\n  2486:     /// ```\n  2487:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2488:     pub fn retain<F>(&mut self, mut f: F)\n  2489:     where\n  2490:         F: FnMut(&T) -> bool,\n  2491:     {\n  2492:         self.retain_mut(|elem| f(elem));\n  2493:     }\n  2494: \n  2495:     /// Retains only the elements specified by the predicate, passing a mutable reference to it.\n  2496:     ///\n  2497:     /// In other words, remove all elements `e` such that `f(&mut e)` returns `false`.\n  2498:     /// This method operates in place, visiting each element exactly once in the",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::retain_mut",
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
                                "is_mutable": true,
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
                      "id": 534,
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
      "name": "retain_mut",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2461:     /// This method operates in place, visiting each element exactly once in the\n  2462:     /// original order, and preserves the order of the retained elements.\n  2463:     ///\n  2464:     /// # Examples\n  2465:     ///\n  2466:     /// ```\n  2467:     /// let mut vec = vec![1, 2, 3, 4];\n  2468:     /// vec.retain_mut(|x| if *x <= 3 {\n  2469:     ///     *x += 1;\n  2470:     ///     true\n  2471:     /// } else {\n  2472:     ///     false\n  2473:     /// });\n  2474:     /// assert_eq!(vec, [2, 3, 4]);\n  2475:     /// ```\n  2476:     #[stable(feature = \"vec_retain_mut\", since = \"1.61.0\")]\n  2477:     pub fn retain_mut<F>(&mut self, mut f: F)\n  2478:     where\n  2479:         F: FnMut(&mut T) -> bool,\n  2480:     {\n  2481:         let original_len = self.len();\n  2482: \n  2483:         if original_len == 0 {\n  2484:             // Empty case: explicit return allows better optimization, vs letting compiler infer it\n  2485:             return;\n  2486:         }\n  2487: \n  2488:         // Vec: [Kept, Kept, Hole, Hole, Hole, Hole, Unchecked, Unchecked]\n  2489:         //      |            ^- write                ^- read             |\n  2490:         //      |<-              original_len                          ->|\n  2491:         // Kept: Elements which predicate returns true on.\n  2492:         // Hole: Moved or dropped element slot.\n  2493:         // Unchecked: Unchecked valid elements.",
    "nanvix_source": "  2504:     /// let mut vec = vec![1, 2, 3, 4];\n  2505:     /// vec.retain_mut(|x| if *x <= 3 {\n  2506:     ///     *x += 1;\n  2507:     ///     true\n  2508:     /// } else {\n  2509:     ///     false\n  2510:     /// });\n  2511:     /// assert_eq!(vec, [2, 3, 4]);\n  2512:     /// ```\n  2513:     #[stable(feature = \"vec_retain_mut\", since = \"1.61.0\")]\n  2514:     pub fn retain_mut<F>(&mut self, mut f: F)\n  2515:     where\n  2516:         F: FnMut(&mut T) -> bool,\n  2517:     {\n  2518:         let original_len = self.len();\n  2519: \n  2520:         if original_len == 0 {\n  2521:             // Empty case: explicit return allows better optimization, vs letting compiler infer it\n  2522:             return;\n  2523:         }\n  2524: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::splice",
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
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "primitive": "usize"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 1409,
                      "path": "RangeBounds"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "R"
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
                                    "generic": "T"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 219,
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
      "name": "splice",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4953",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
            "range",
            {
              "generic": "R"
            }
          ],
          [
            "replace_with",
            {
              "generic": "I"
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
                      "qualified_path": {
                        "args": null,
                        "name": "IntoIter",
                        "self_type": {
                          "generic": "I"
                        },
                        "trait": {
                          "args": null,
                          "id": 219,
                          "path": ""
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4702,
            "path": "Splice"
          }
        }
      }
    },
    "verification_source": "  4075:     /// assert_eq!(v, [1, 7, 8, 9, 4]);\n  4076:     /// assert_eq!(u, [2, 3]);\n  4077:     /// ```\n  4078:     ///\n  4079:     /// Using `splice` to insert new items into a vector efficiently at a specific position\n  4080:     /// indicated by an empty range:\n  4081:     ///\n  4082:     /// ```\n  4083:     /// let mut v = vec![1, 5];\n  4084:     /// let new = [2, 3, 4];\n  4085:     /// v.splice(1..1, new);\n  4086:     /// assert_eq!(v, [1, 2, 3, 4, 5]);\n  4087:     /// ```\n  4088:     #[cfg(not(no_global_oom_handling))]\n  4089:     #[inline]\n  4090:     #[stable(feature = \"vec_splice\", since = \"1.21.0\")]\n  4091:     pub fn splice<R, I>(&mut self, range: R, replace_with: I) -> Splice<'_, I::IntoIter, A>\n  4092:     where\n  4093:         R: RangeBounds<usize>,\n  4094:         I: IntoIterator<Item = T>,\n  4095:     {\n  4096:         Splice { drain: self.drain(range), replace_with: replace_with.into_iter() }\n  4097:     }\n  4098: \n  4099:     /// Creates an iterator which uses a closure to determine if an element in the range should be removed.\n  4100:     ///\n  4101:     /// If the closure returns `true`, the element is removed from the vector\n  4102:     /// and yielded. If the closure returns `false`, or panics, the element\n  4103:     /// remains in the vector and will not be yielded.\n  4104:     ///\n  4105:     /// Only elements that fall in the provided range are considered for extraction, but any elements\n  4106:     /// after the range will still have to be moved if any element has been extracted.\n  4107:     ///",
    "nanvix_source": "  4131:     ///\n  4132:     /// ```\n  4133:     /// let mut v = vec![1, 5];\n  4134:     /// let new = [2, 3, 4];\n  4135:     /// v.splice(1..1, new);\n  4136:     /// assert_eq!(v, [1, 2, 3, 4, 5]);\n  4137:     /// ```\n  4138:     #[cfg(not(no_global_oom_handling))]\n  4139:     #[inline]\n  4140:     #[stable(feature = \"vec_splice\", since = \"1.21.0\")]\n  4141:     pub fn splice<R, I>(&mut self, range: R, replace_with: I) -> Splice<'_, I::IntoIter, A>\n  4142:     where\n  4143:         R: RangeBounds<usize>,\n  4144:         I: IntoIterator<Item = T>,\n  4145:     {\n  4146:         Splice { drain: self.drain(range), replace_with: replace_with.into_iter() }\n  4147:     }\n  4148: \n  4149:     /// Creates an iterator which uses a closure to determine if an element in the range should be removed.\n  4150:     ///\n  4151:     /// If the closure returns `true`, the element is removed from the vector",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Peekable::next_if",
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
            "name": "impl FnOnce(&I::Item) -> bool"
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
      "name": "next_if",
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
            "func",
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
    "verification_source": "   271:     /// assert_eq!(iter.next_if(|&x| x == 0), Some(0));\n   272:     /// // The next item returned is now 1, so `next_if` will return `None`.\n   273:     /// assert_eq!(iter.next_if(|&x| x == 0), None);\n   274:     /// // `next_if` retains the next item if the predicate evaluates to `false` for it.\n   275:     /// assert_eq!(iter.next(), Some(1));\n   276:     /// ```\n   277:     ///\n   278:     /// Consume any number less than 10.\n   279:     /// ```\n   280:     /// let mut iter = (1..20).peekable();\n   281:     /// // Consume all numbers less than 10\n   282:     /// while iter.next_if(|&x| x < 10).is_some() {}\n   283:     /// // The next value returned will be 10\n   284:     /// assert_eq!(iter.next(), Some(10));\n   285:     /// ```\n   286:     #[stable(feature = \"peekable_next_if\", since = \"1.51.0\")]\n   287:     pub fn next_if(&mut self, func: impl FnOnce(&I::Item) -> bool) -> Option<I::Item> {\n   288:         match self.next() {\n   289:             Some(matched) if func(&matched) => Some(matched),\n   290:             other => {\n   291:                 // Since we called `self.next()`, we consumed `self.peeked`.\n   292:                 assert!(self.peeked.is_none());\n   293:                 self.peeked = Some(other);\n   294:                 None\n   295:             }\n   296:         }\n   297:     }\n   298: \n   299:     /// Consume and return the next item if it is equal to `expected`.\n   300:     ///\n   301:     /// # Example\n   302:     /// Consume a number if it's equal to 0.\n   303:     /// ```",
    "nanvix_source": "   277:     ///\n   278:     /// Consume any number less than 10.\n   279:     /// ```\n   280:     /// let mut iter = (1..20).peekable();\n   281:     /// // Consume all numbers less than 10\n   282:     /// while iter.next_if(|&x| x < 10).is_some() {}\n   283:     /// // The next value returned will be 10\n   284:     /// assert_eq!(iter.next(), Some(10));\n   285:     /// ```\n   286:     #[stable(feature = \"peekable_next_if\", since = \"1.51.0\")]\n   287:     pub fn next_if(&mut self, func: impl FnOnce(&I::Item) -> bool) -> Option<I::Item> {\n   288:         match self.next() {\n   289:             Some(matched) if func(&matched) => Some(matched),\n   290:             other => {\n   291:                 // Since we called `self.next()`, we consumed `self.peeked`.\n   292:                 assert!(self.peeked.is_none());\n   293:                 self.peeked = Some(other);\n   294:                 None\n   295:             }\n   296:         }\n   297:     }",
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
