For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::sync::Weak::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
            "id": 4358,
            "path": "Weak"
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
        "impl_id": "alloc:4541",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
        ],
        "trait": null
      },
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
            "id": 4358,
            "path": "Weak"
          }
        }
      }
    },
    "verification_source": "  2943:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  2944:     ///\n  2945:     /// [`upgrade`]: Weak::upgrade\n  2946:     ///\n  2947:     /// # Examples\n  2948:     ///\n  2949:     /// ```\n  2950:     /// use std::sync::Weak;\n  2951:     ///\n  2952:     /// let empty: Weak<i64> = Weak::new();\n  2953:     /// assert!(empty.upgrade().is_none());\n  2954:     /// ```\n  2955:     #[inline]\n  2956:     #[stable(feature = \"downgraded_weak\", since = \"1.10.0\")]\n  2957:     #[rustc_const_stable(feature = \"const_weak_new\", since = \"1.73.0\")]\n  2958:     #[must_use]\n  2959:     pub const fn new() -> Weak<T> {\n  2960:         Weak { ptr: NonNull::without_provenance(NonZeroUsize::MAX), alloc: Global }\n  2961:     }\n  2962: }\n  2963: \n  2964: impl<T, A: Allocator> Weak<T, A> {\n  2965:     /// Constructs a new `Weak<T, A>`, without allocating any memory, technically in the provided\n  2966:     /// allocator.\n  2967:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  2968:     ///\n  2969:     /// [`upgrade`]: Weak::upgrade\n  2970:     ///\n  2971:     /// # Examples\n  2972:     ///\n  2973:     /// ```\n  2974:     /// #![feature(allocator_api)]\n  2975:     ///",
    "nanvix_source": "  2964:     /// ```\n  2965:     /// use std::sync::Weak;\n  2966:     ///\n  2967:     /// let empty: Weak<i64> = Weak::new();\n  2968:     /// assert!(empty.upgrade().is_none());\n  2969:     /// ```\n  2970:     #[inline]\n  2971:     #[stable(feature = \"downgraded_weak\", since = \"1.10.0\")]\n  2972:     #[rustc_const_stable(feature = \"const_weak_new\", since = \"1.73.0\")]\n  2973:     #[must_use]\n  2974:     pub const fn new() -> Weak<T> {\n  2975:         Weak { ptr: NonNull::without_provenance(NonZeroUsize::MAX), alloc: Global }\n  2976:     }\n  2977: }\n  2978: \n  2979: impl<T, A: Allocator> Weak<T, A> {\n  2980:     /// Constructs a new `Weak<T, A>`, without allocating any memory, technically in the provided\n  2981:     /// allocator.\n  2982:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  2983:     ///\n  2984:     /// [`upgrade`]: Weak::upgrade",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::ptr_eq",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "ptr_eq",
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
            "id": 4358,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:4555",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
            "other",
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
    "verification_source": "  3373:     /// ```\n  3374:     /// use std::sync::{Arc, Weak};\n  3375:     ///\n  3376:     /// let first = Weak::new();\n  3377:     /// let second = Weak::new();\n  3378:     /// assert!(first.ptr_eq(&second));\n  3379:     ///\n  3380:     /// let third_rc = Arc::new(());\n  3381:     /// let third = Arc::downgrade(&third_rc);\n  3382:     /// assert!(!first.ptr_eq(&third));\n  3383:     /// ```\n  3384:     ///\n  3385:     /// [`ptr::eq`]: core::ptr::eq \"ptr::eq\"\n  3386:     #[inline]\n  3387:     #[must_use]\n  3388:     #[stable(feature = \"weak_ptr_eq\", since = \"1.39.0\")]\n  3389:     pub fn ptr_eq(&self, other: &Self) -> bool {\n  3390:         ptr::addr_eq(self.ptr.as_ptr(), other.ptr.as_ptr())\n  3391:     }\n  3392: }\n  3393: \n  3394: #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  3395: impl<T: ?Sized, A: Allocator + Clone> Clone for Weak<T, A> {\n  3396:     /// Makes a clone of the `Weak` pointer that points to the same allocation.\n  3397:     ///\n  3398:     /// # Examples\n  3399:     ///\n  3400:     /// ```\n  3401:     /// use std::sync::{Arc, Weak};\n  3402:     ///\n  3403:     /// let weak_five = Arc::downgrade(&Arc::new(5));\n  3404:     ///\n  3405:     /// let _ = Weak::clone(&weak_five);",
    "nanvix_source": "  3400:     ///\n  3401:     /// let third_rc = Arc::new(());\n  3402:     /// let third = Arc::downgrade(&third_rc);\n  3403:     /// assert!(!first.ptr_eq(&third));\n  3404:     /// ```\n  3405:     ///\n  3406:     /// [`ptr::eq`]: core::ptr::eq \"ptr::eq\"\n  3407:     #[inline]\n  3408:     #[must_use]\n  3409:     #[stable(feature = \"weak_ptr_eq\", since = \"1.39.0\")]\n  3410:     pub fn ptr_eq(&self, other: &Self) -> bool {\n  3411:         ptr::addr_eq(self.ptr.as_ptr(), other.ptr.as_ptr())\n  3412:     }\n  3413: }\n  3414: \n  3415: #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  3416: impl<T: ?Sized, A: Allocator + Clone> Clone for Weak<T, A> {\n  3417:     /// Makes a clone of the `Weak` pointer that points to the same allocation.\n  3418:     ///\n  3419:     /// # Examples\n  3420:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::strong_count",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "strong_count",
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
            "id": 4358,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:4555",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  3278:         // Acquire is necessary for the success case to synchronise with `Arc::new_cyclic`, when the inner\n  3279:         // value can be initialized after `Weak` references have already been created. In that case, we\n  3280:         // expect to observe the fully initialized value.\n  3281:         if self.inner()?.strong.try_update(Acquire, Relaxed, checked_increment).is_ok() {\n  3282:             // SAFETY: pointer is not null, verified in checked_increment\n  3283:             unsafe { Some(Arc::from_inner_in(self.ptr, self.alloc.clone())) }\n  3284:         } else {\n  3285:             None\n  3286:         }\n  3287:     }\n  3288: \n  3289:     /// Gets the number of strong (`Arc`) pointers pointing to this allocation.\n  3290:     ///\n  3291:     /// If `self` was created using [`Weak::new`], this will return 0.\n  3292:     #[must_use]\n  3293:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3294:     pub fn strong_count(&self) -> usize {\n  3295:         if let Some(inner) = self.inner() { inner.strong.load(Relaxed) } else { 0 }\n  3296:     }\n  3297: \n  3298:     /// Gets an approximation of the number of `Weak` pointers pointing to this\n  3299:     /// allocation.\n  3300:     ///\n  3301:     /// If `self` was created using [`Weak::new`], or if there are no remaining\n  3302:     /// strong pointers, this will return 0.\n  3303:     ///\n  3304:     /// # Accuracy\n  3305:     ///\n  3306:     /// Due to implementation details, the returned value can be off by 1 in\n  3307:     /// either direction when other threads are manipulating any `Arc`s or\n  3308:     /// `Weak`s pointing to the same allocation.\n  3309:     #[must_use]\n  3310:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]",
    "nanvix_source": "  3305:         } else {\n  3306:             None\n  3307:         }\n  3308:     }\n  3309: \n  3310:     /// Gets the number of strong (`Arc`) pointers pointing to this allocation.\n  3311:     ///\n  3312:     /// If `self` was created using [`Weak::new`], this will return 0.\n  3313:     #[must_use]\n  3314:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3315:     pub fn strong_count(&self) -> usize {\n  3316:         if let Some(inner) = self.inner() { inner.strong.load(Relaxed) } else { 0 }\n  3317:     }\n  3318: \n  3319:     /// Gets an approximation of the number of `Weak` pointers pointing to this\n  3320:     /// allocation.\n  3321:     ///\n  3322:     /// If `self` was created using [`Weak::new`], or if there are no remaining\n  3323:     /// strong pointers, this will return 0.\n  3324:     ///\n  3325:     /// # Accuracy",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::upgrade",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
                      "id": 25,
                      "path": "Clone"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "A"
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
      "name": "upgrade",
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
            "id": 4358,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:4555",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
                    "type": {
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
                        "id": 346,
                        "path": "Arc"
                      }
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
    "verification_source": "  3242:     /// let five = Arc::new(5);\n  3243:     ///\n  3244:     /// let weak_five = Arc::downgrade(&five);\n  3245:     ///\n  3246:     /// let strong_five: Option<Arc<_>> = weak_five.upgrade();\n  3247:     /// assert!(strong_five.is_some());\n  3248:     ///\n  3249:     /// // Destroy all strong pointers.\n  3250:     /// drop(strong_five);\n  3251:     /// drop(five);\n  3252:     ///\n  3253:     /// assert!(weak_five.upgrade().is_none());\n  3254:     /// ```\n  3255:     #[must_use = \"this returns a new `Arc`, \\\n  3256:                   without modifying the original weak pointer\"]\n  3257:     #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  3258:     pub fn upgrade(&self) -> Option<Arc<T, A>>\n  3259:     where\n  3260:         A: Clone,\n  3261:     {\n  3262:         #[inline]\n  3263:         fn checked_increment(n: usize) -> Option<usize> {\n  3264:             // Any write of 0 we can observe leaves the field in permanently zero state.\n  3265:             if n == 0 {\n  3266:                 return None;\n  3267:             }\n  3268:             // See comments in `Arc::clone` for why we do this (for `mem::forget`).\n  3269:             assert!(n <= MAX_REFCOUNT, \"{}\", INTERNAL_OVERFLOW_ERROR);\n  3270:             Some(n + 1)\n  3271:         }\n  3272: \n  3273:         // We use a CAS loop to increment the strong count instead of a\n  3274:         // fetch_add as this function should never take the reference count",
    "nanvix_source": "  3269:     ///\n  3270:     /// // Destroy all strong pointers.\n  3271:     /// drop(strong_five);\n  3272:     /// drop(five);\n  3273:     ///\n  3274:     /// assert!(weak_five.upgrade().is_none());\n  3275:     /// ```\n  3276:     #[must_use = \"this returns a new `Arc`, \\\n  3277:                   without modifying the original weak pointer\"]\n  3278:     #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  3279:     pub fn upgrade(&self) -> Option<Arc<T, A>>\n  3280:     where\n  3281:         A: Clone,\n  3282:     {\n  3283:         #[inline]\n  3284:         fn checked_increment(n: usize) -> Option<usize> {\n  3285:             // Any write of 0 we can observe leaves the field in permanently zero state.\n  3286:             if n == 0 {\n  3287:                 return None;\n  3288:             }\n  3289:             // See comments in `Arc::clone` for why we do this (for `mem::forget`).",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::weak_count",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "weak_count",
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
            "id": 4358,
            "path": "Weak"
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
                          "id": 29,
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
        "impl_id": "alloc:4555",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  3295:         if let Some(inner) = self.inner() { inner.strong.load(Relaxed) } else { 0 }\n  3296:     }\n  3297: \n  3298:     /// Gets an approximation of the number of `Weak` pointers pointing to this\n  3299:     /// allocation.\n  3300:     ///\n  3301:     /// If `self` was created using [`Weak::new`], or if there are no remaining\n  3302:     /// strong pointers, this will return 0.\n  3303:     ///\n  3304:     /// # Accuracy\n  3305:     ///\n  3306:     /// Due to implementation details, the returned value can be off by 1 in\n  3307:     /// either direction when other threads are manipulating any `Arc`s or\n  3308:     /// `Weak`s pointing to the same allocation.\n  3309:     #[must_use]\n  3310:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3311:     pub fn weak_count(&self) -> usize {\n  3312:         if let Some(inner) = self.inner() {\n  3313:             let weak = inner.weak.load(Acquire);\n  3314:             let strong = inner.strong.load(Relaxed);\n  3315:             if strong == 0 {\n  3316:                 0\n  3317:             } else {\n  3318:                 // Since we observed that there was at least one strong pointer\n  3319:                 // after reading the weak count, we know that the implicit weak\n  3320:                 // reference (present whenever any strong references are alive)\n  3321:                 // was still around when we observed the weak count, and can\n  3322:                 // therefore safely subtract it.\n  3323:                 weak - 1\n  3324:             }\n  3325:         } else {\n  3326:             0\n  3327:         }",
    "nanvix_source": "  3322:     /// If `self` was created using [`Weak::new`], or if there are no remaining\n  3323:     /// strong pointers, this will return 0.\n  3324:     ///\n  3325:     /// # Accuracy\n  3326:     ///\n  3327:     /// Due to implementation details, the returned value can be off by 1 in\n  3328:     /// either direction when other threads are manipulating any `Arc`s or\n  3329:     /// `Weak`s pointing to the same allocation.\n  3330:     #[must_use]\n  3331:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3332:     pub fn weak_count(&self) -> usize {\n  3333:         if let Some(inner) = self.inner() {\n  3334:             let weak = inner.weak.load(Acquire);\n  3335:             let strong = inner.strong.load(Relaxed);\n  3336:             if strong == 0 {\n  3337:                 0\n  3338:             } else {\n  3339:                 // Since we observed that there was at least one strong pointer\n  3340:                 // after reading the weak count, we know that the implicit weak\n  3341:                 // reference (present whenever any strong references are alive)\n  3342:                 // was still around when we observed the weak count, and can",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Drain::as_slice",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
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
                    "lifetime": "'a"
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
        "impl_id": "alloc:4739",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4735",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "drain",
          "Drain"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "    40: }\n    41: \n    42: impl<'a, T, A: Allocator> Drain<'a, T, A> {\n    43:     /// Returns the remaining items of this iterator as a slice.\n    44:     ///\n    45:     /// # Examples\n    46:     ///\n    47:     /// ```\n    48:     /// let mut vec = vec!['a', 'b', 'c'];\n    49:     /// let mut drain = vec.drain(..);\n    50:     /// assert_eq!(drain.as_slice(), &['a', 'b', 'c']);\n    51:     /// let _ = drain.next().unwrap();\n    52:     /// assert_eq!(drain.as_slice(), &['b', 'c']);\n    53:     /// ```\n    54:     #[must_use]\n    55:     #[stable(feature = \"vec_drain_as_slice\", since = \"1.46.0\")]\n    56:     pub fn as_slice(&self) -> &[T] {\n    57:         self.iter.as_slice()\n    58:     }\n    59: \n    60:     /// Returns a reference to the underlying allocator.\n    61:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n    62:     #[must_use]\n    63:     #[inline]\n    64:     pub fn allocator(&self) -> &A {\n    65:         unsafe { self.vec.as_ref().allocator() }\n    66:     }\n    67: \n    68:     /// Keep unyielded elements in the source `Vec`.\n    69:     ///\n    70:     /// # Examples\n    71:     ///\n    72:     /// ```",
    "nanvix_source": "    46:     ///\n    47:     /// ```\n    48:     /// let mut vec = vec!['a', 'b', 'c'];\n    49:     /// let mut drain = vec.drain(..);\n    50:     /// assert_eq!(drain.as_slice(), &['a', 'b', 'c']);\n    51:     /// let _ = drain.next().unwrap();\n    52:     /// assert_eq!(drain.as_slice(), &['b', 'c']);\n    53:     /// ```\n    54:     #[must_use]\n    55:     #[stable(feature = \"vec_drain_as_slice\", since = \"1.46.0\")]\n    56:     pub fn as_slice(&self) -> &[T] {\n    57:         self.iter.as_slice()\n    58:     }\n    59: \n    60:     /// Returns a reference to the underlying allocator.\n    61:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n    62:     #[must_use]\n    63:     #[inline]\n    64:     pub fn allocator(&self) -> &A {\n    65:         unsafe { self.vec.as_ref().allocator() }\n    66:     }",
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
