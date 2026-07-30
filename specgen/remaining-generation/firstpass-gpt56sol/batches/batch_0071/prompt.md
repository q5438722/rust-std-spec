For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::binary_search_by",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": null,
                              "id": 174,
                              "path": "Ordering"
                            }
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
      "name": "binary_search_by",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
                "lifetime": "'a",
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  },
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  3149:     /// Looks up a series of four elements. The first is found, with a\n  3150:     /// uniquely determined position; the second and third are not\n  3151:     /// found; the fourth could match any position in `[1, 4]`.\n  3152:     ///\n  3153:     /// ```\n  3154:     /// use std::collections::VecDeque;\n  3155:     ///\n  3156:     /// let deque: VecDeque<_> = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55].into();\n  3157:     ///\n  3158:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&13)),  Ok(9));\n  3159:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&4)),   Err(7));\n  3160:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&100)), Err(13));\n  3161:     /// let r = deque.binary_search_by(|x| x.cmp(&1));\n  3162:     /// assert!(matches!(r, Ok(1..=4)));\n  3163:     /// ```\n  3164:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3165:     pub fn binary_search_by<'a, F>(&'a self, mut f: F) -> Result<usize, usize>\n  3166:     where\n  3167:         F: FnMut(&'a T) -> Ordering,\n  3168:     {\n  3169:         let (front, back) = self.as_slices();\n  3170:         let cmp_back = back.first().map(|elem| f(elem));\n  3171: \n  3172:         if let Some(Ordering::Equal) = cmp_back {\n  3173:             Ok(front.len())\n  3174:         } else if let Some(Ordering::Less) = cmp_back {\n  3175:             back.binary_search_by(f).map(|idx| idx + front.len()).map_err(|idx| idx + front.len())\n  3176:         } else {\n  3177:             front.binary_search_by(f)\n  3178:         }\n  3179:     }\n  3180: \n  3181:     /// Binary searches this `VecDeque` with a key extraction function.",
    "nanvix_source": "  3237:     ///\n  3238:     /// let deque: VecDeque<_> = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55].into();\n  3239:     ///\n  3240:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&13)),  Ok(9));\n  3241:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&4)),   Err(7));\n  3242:     /// assert_eq!(deque.binary_search_by(|x| x.cmp(&100)), Err(13));\n  3243:     /// let r = deque.binary_search_by(|x| x.cmp(&1));\n  3244:     /// assert!(matches!(r, Ok(1..=4)));\n  3245:     /// ```\n  3246:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3247:     pub fn binary_search_by<'a, F>(&'a self, mut f: F) -> Result<usize, usize>\n  3248:     where\n  3249:         F: FnMut(&'a T) -> Ordering,\n  3250:     {\n  3251:         let (front, back) = self.as_slices();\n  3252:         let cmp_back = back.first().map(|elem| f(elem));\n  3253: \n  3254:         if let Some(Ordering::Equal) = cmp_back {\n  3255:             Ok(front.len())\n  3256:         } else if let Some(Ordering::Less) = cmp_back {\n  3257:             back.binary_search_by(f).map(|idx| idx + front.len()).map_err(|idx| idx + front.len())",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::binary_search_by_key",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
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
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "B"
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
                      "args": null,
                      "id": 176,
                      "path": "Ord"
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
      "name": "binary_search_by_key",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
                "lifetime": "'a",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "b",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "B"
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  },
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  3207:     ///\n  3208:     /// ```\n  3209:     /// use std::collections::VecDeque;\n  3210:     ///\n  3211:     /// let deque: VecDeque<_> = [(0, 0), (2, 1), (4, 1), (5, 1),\n  3212:     ///          (3, 1), (1, 2), (2, 3), (4, 5), (5, 8), (3, 13),\n  3213:     ///          (1, 21), (2, 34), (4, 55)].into();\n  3214:     ///\n  3215:     /// assert_eq!(deque.binary_search_by_key(&13, |&(a, b)| b),  Ok(9));\n  3216:     /// assert_eq!(deque.binary_search_by_key(&4, |&(a, b)| b),   Err(7));\n  3217:     /// assert_eq!(deque.binary_search_by_key(&100, |&(a, b)| b), Err(13));\n  3218:     /// let r = deque.binary_search_by_key(&1, |&(a, b)| b);\n  3219:     /// assert!(matches!(r, Ok(1..=4)));\n  3220:     /// ```\n  3221:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3222:     #[inline]\n  3223:     pub fn binary_search_by_key<'a, B, F>(&'a self, b: &B, mut f: F) -> Result<usize, usize>\n  3224:     where\n  3225:         F: FnMut(&'a T) -> B,\n  3226:         B: Ord,\n  3227:     {\n  3228:         self.binary_search_by(|k| f(k).cmp(b))\n  3229:     }\n  3230: \n  3231:     /// Returns the index of the partition point according to the given predicate\n  3232:     /// (the index of the first element of the second partition).\n  3233:     ///\n  3234:     /// The deque is assumed to be partitioned according to the given predicate.\n  3235:     /// This means that all elements for which the predicate returns true are at the start of the deque\n  3236:     /// and all elements for which the predicate returns false are at the end.\n  3237:     /// For example, `[7, 15, 3, 5, 4, 12, 6]` is partitioned under the predicate `x % 2 != 0`\n  3238:     /// (all odd numbers are at the start, all even at the end).\n  3239:     ///",
    "nanvix_source": "  3295:     ///          (1, 21), (2, 34), (4, 55)].into();\n  3296:     ///\n  3297:     /// assert_eq!(deque.binary_search_by_key(&13, |&(a, b)| b),  Ok(9));\n  3298:     /// assert_eq!(deque.binary_search_by_key(&4, |&(a, b)| b),   Err(7));\n  3299:     /// assert_eq!(deque.binary_search_by_key(&100, |&(a, b)| b), Err(13));\n  3300:     /// let r = deque.binary_search_by_key(&1, |&(a, b)| b);\n  3301:     /// assert!(matches!(r, Ok(1..=4)));\n  3302:     /// ```\n  3303:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3304:     #[inline]\n  3305:     pub fn binary_search_by_key<'a, B, F>(&'a self, b: &B, mut f: F) -> Result<usize, usize>\n  3306:     where\n  3307:         F: FnMut(&'a T) -> B,\n  3308:         B: Ord,\n  3309:     {\n  3310:         self.binary_search_by(|k| f(k).cmp(b))\n  3311:     }\n  3312: \n  3313:     /// Returns the index of the partition point according to the given predicate\n  3314:     /// (the index of the first element of the second partition).\n  3315:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::partition_point",
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
                "generic": "P"
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
      "name": "partition_point",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
          ],
          [
            "pred",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  3259:     /// assert!(deque.iter().skip(i).all(|&x| !(x < 5)));\n  3260:     /// ```\n  3261:     ///\n  3262:     /// If you want to insert an item to a sorted deque, while maintaining\n  3263:     /// sort order:\n  3264:     ///\n  3265:     /// ```\n  3266:     /// use std::collections::VecDeque;\n  3267:     ///\n  3268:     /// let mut deque: VecDeque<_> = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55].into();\n  3269:     /// let num = 42;\n  3270:     /// let idx = deque.partition_point(|&x| x < num);\n  3271:     /// deque.insert(idx, num);\n  3272:     /// assert_eq!(deque, &[0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  3273:     /// ```\n  3274:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3275:     pub fn partition_point<P>(&self, mut pred: P) -> usize\n  3276:     where\n  3277:         P: FnMut(&T) -> bool,\n  3278:     {\n  3279:         let (front, back) = self.as_slices();\n  3280: \n  3281:         if let Some(true) = back.first().map(|v| pred(v)) {\n  3282:             back.partition_point(pred) + front.len()\n  3283:         } else {\n  3284:             front.partition_point(pred)\n  3285:         }\n  3286:     }\n  3287: }\n  3288: \n  3289: impl<T: Clone, A: Allocator> VecDeque<T, A> {\n  3290:     /// Modifies the deque in-place so that `len()` is equal to new_len,\n  3291:     /// either by removing excess elements from the back or by appending clones of `value`",
    "nanvix_source": "  3347:     /// ```\n  3348:     /// use std::collections::VecDeque;\n  3349:     ///\n  3350:     /// let mut deque: VecDeque<_> = [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55].into();\n  3351:     /// let num = 42;\n  3352:     /// let idx = deque.partition_point(|&x| x < num);\n  3353:     /// deque.insert(idx, num);\n  3354:     /// assert_eq!(deque, &[0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  3355:     /// ```\n  3356:     #[stable(feature = \"vecdeque_binary_search\", since = \"1.54.0\")]\n  3357:     pub fn partition_point<P>(&self, mut pred: P) -> usize\n  3358:     where\n  3359:         P: FnMut(&T) -> bool,\n  3360:     {\n  3361:         let (front, back) = self.as_slices();\n  3362: \n  3363:         if let Some(true) = back.first().map(|v| pred(v)) {\n  3364:             back.partition_point(pred) + front.len()\n  3365:         } else {\n  3366:             front.partition_point(pred)\n  3367:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::pop_back_if",
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
                        "id": 441,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(&mut T) -> bool"
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
      "name": "pop_back_if",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "predicate"
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "predicate",
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
                      "id": 441,
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2134:     /// returns `true`, or [`None`] if the predicate returns false or the deque\n  2135:     /// is empty (the predicate will not be called in that case).\n  2136:     ///\n  2137:     /// # Examples\n  2138:     ///\n  2139:     /// ```\n  2140:     /// use std::collections::VecDeque;\n  2141:     ///\n  2142:     /// let mut deque: VecDeque<i32> = vec![0, 1, 2, 3, 4].into();\n  2143:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2144:     ///\n  2145:     /// assert_eq!(deque.pop_back_if(pred), Some(4));\n  2146:     /// assert_eq!(deque, [0, 1, 2, 3]);\n  2147:     /// assert_eq!(deque.pop_back_if(pred), None);\n  2148:     /// ```\n  2149:     #[stable(feature = \"vec_deque_pop_if\", since = \"1.93.0\")]\n  2150:     pub fn pop_back_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2151:         let last = self.back_mut()?;\n  2152:         if predicate(last) { self.pop_back() } else { None }\n  2153:     }\n  2154: \n  2155:     /// Prepends an element to the deque.\n  2156:     ///\n  2157:     /// # Examples\n  2158:     ///\n  2159:     /// ```\n  2160:     /// use std::collections::VecDeque;\n  2161:     ///\n  2162:     /// let mut d = VecDeque::new();\n  2163:     /// d.push_front(1);\n  2164:     /// d.push_front(2);\n  2165:     /// assert_eq!(d.front(), Some(&2));\n  2166:     /// ```",
    "nanvix_source": "  2204:     /// use std::collections::VecDeque;\n  2205:     ///\n  2206:     /// let mut deque: VecDeque<i32> = vec![0, 1, 2, 3, 4].into();\n  2207:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2208:     ///\n  2209:     /// assert_eq!(deque.pop_back_if(pred), Some(4));\n  2210:     /// assert_eq!(deque, [0, 1, 2, 3]);\n  2211:     /// assert_eq!(deque.pop_back_if(pred), None);\n  2212:     /// ```\n  2213:     #[stable(feature = \"vec_deque_pop_if\", since = \"1.93.0\")]\n  2214:     pub fn pop_back_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2215:         let last = self.back_mut()?;\n  2216:         if predicate(last) { self.pop_back() } else { None }\n  2217:     }\n  2218: \n  2219:     /// Prepends an element to the deque.\n  2220:     ///\n  2221:     /// # Examples\n  2222:     ///\n  2223:     /// ```\n  2224:     /// use std::collections::VecDeque;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::pop_front_if",
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
                        "id": 441,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(&mut T) -> bool"
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
      "name": "pop_front_if",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "predicate"
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "predicate",
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
                      "id": 441,
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2112:     /// returns `true`, or [`None`] if the predicate returns false or the deque\n  2113:     /// is empty (the predicate will not be called in that case).\n  2114:     ///\n  2115:     /// # Examples\n  2116:     ///\n  2117:     /// ```\n  2118:     /// use std::collections::VecDeque;\n  2119:     ///\n  2120:     /// let mut deque: VecDeque<i32> = vec![0, 1, 2, 3, 4].into();\n  2121:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2122:     ///\n  2123:     /// assert_eq!(deque.pop_front_if(pred), Some(0));\n  2124:     /// assert_eq!(deque, [1, 2, 3, 4]);\n  2125:     /// assert_eq!(deque.pop_front_if(pred), None);\n  2126:     /// ```\n  2127:     #[stable(feature = \"vec_deque_pop_if\", since = \"1.93.0\")]\n  2128:     pub fn pop_front_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2129:         let first = self.front_mut()?;\n  2130:         if predicate(first) { self.pop_front() } else { None }\n  2131:     }\n  2132: \n  2133:     /// Removes and returns the last element from the deque if the predicate\n  2134:     /// returns `true`, or [`None`] if the predicate returns false or the deque\n  2135:     /// is empty (the predicate will not be called in that case).\n  2136:     ///\n  2137:     /// # Examples\n  2138:     ///\n  2139:     /// ```\n  2140:     /// use std::collections::VecDeque;\n  2141:     ///\n  2142:     /// let mut deque: VecDeque<i32> = vec![0, 1, 2, 3, 4].into();\n  2143:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2144:     ///",
    "nanvix_source": "  2182:     /// use std::collections::VecDeque;\n  2183:     ///\n  2184:     /// let mut deque: VecDeque<i32> = vec![0, 1, 2, 3, 4].into();\n  2185:     /// let pred = |x: &mut i32| *x % 2 == 0;\n  2186:     ///\n  2187:     /// assert_eq!(deque.pop_front_if(pred), Some(0));\n  2188:     /// assert_eq!(deque, [1, 2, 3, 4]);\n  2189:     /// assert_eq!(deque.pop_front_if(pred), None);\n  2190:     /// ```\n  2191:     #[stable(feature = \"vec_deque_pop_if\", since = \"1.93.0\")]\n  2192:     pub fn pop_front_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T> {\n  2193:         let first = self.front_mut()?;\n  2194:         if predicate(first) { self.pop_front() } else { None }\n  2195:     }\n  2196: \n  2197:     /// Removes and returns the last element from the deque if the predicate\n  2198:     /// returns `true`, or [`None`] if the predicate returns false or the deque\n  2199:     /// is empty (the predicate will not be called in that case).\n  2200:     ///\n  2201:     /// # Examples\n  2202:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::resize_with",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                              "generic": "T"
                            }
                          }
                        },
                        "id": 534,
                        "path": "FnMut"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnMut() -> T"
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
      "name": "resize_with",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "new_len",
            {
              "primitive": "usize"
            }
          ],
          [
            "generator",
            {
              "impl_trait": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 534,
                      "path": "FnMut"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2750:     /// buf.push_back(5);\n  2751:     /// buf.push_back(10);\n  2752:     /// buf.push_back(15);\n  2753:     /// assert_eq!(buf, [5, 10, 15]);\n  2754:     ///\n  2755:     /// buf.resize_with(5, Default::default);\n  2756:     /// assert_eq!(buf, [5, 10, 15, 0, 0]);\n  2757:     ///\n  2758:     /// buf.resize_with(2, || unreachable!());\n  2759:     /// assert_eq!(buf, [5, 10]);\n  2760:     ///\n  2761:     /// let mut state = 100;\n  2762:     /// buf.resize_with(5, || { state += 1; state });\n  2763:     /// assert_eq!(buf, [5, 10, 101, 102, 103]);\n  2764:     /// ```\n  2765:     #[stable(feature = \"vec_resize_with\", since = \"1.33.0\")]\n  2766:     pub fn resize_with(&mut self, new_len: usize, generator: impl FnMut() -> T) {\n  2767:         let len = self.len;\n  2768: \n  2769:         if new_len > len {\n  2770:             self.extend(repeat_with(generator).take(new_len - len))\n  2771:         } else {\n  2772:             self.truncate(new_len);\n  2773:         }\n  2774:     }\n  2775: \n  2776:     /// Rearranges the internal storage of this deque so it is one contiguous\n  2777:     /// slice, which is then returned.\n  2778:     ///\n  2779:     /// This method does not allocate and does not change the order of the\n  2780:     /// inserted elements. As it returns a mutable slice, this can be used to\n  2781:     /// sort a deque.\n  2782:     ///",
    "nanvix_source": "  2820:     /// assert_eq!(buf, [5, 10, 15, 0, 0]);\n  2821:     ///\n  2822:     /// buf.resize_with(2, || unreachable!());\n  2823:     /// assert_eq!(buf, [5, 10]);\n  2824:     ///\n  2825:     /// let mut state = 100;\n  2826:     /// buf.resize_with(5, || { state += 1; state });\n  2827:     /// assert_eq!(buf, [5, 10, 101, 102, 103]);\n  2828:     /// ```\n  2829:     #[stable(feature = \"vec_resize_with\", since = \"1.33.0\")]\n  2830:     pub fn resize_with(&mut self, new_len: usize, generator: impl FnMut() -> T) {\n  2831:         let len = self.len;\n  2832: \n  2833:         if new_len > len {\n  2834:             self.extend(repeat_with(generator).take(new_len - len))\n  2835:         } else {\n  2836:             self.truncate(new_len);\n  2837:         }\n  2838:     }\n  2839: \n  2840:     /// Rearranges the internal storage of this deque so it is one contiguous",
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
