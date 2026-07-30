For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::sync::Arc::unwrap_or_clone",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
      "name": "unwrap_or_clone",
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
            "id": 346,
            "path": "Arc"
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
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:4420",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:346",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Arc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
    "verification_source": "  2576:     /// let inner = Arc::unwrap_or_clone(arc);\n  2577:     /// // The inner value was not cloned\n  2578:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2579:     ///\n  2580:     /// let arc = Arc::new(inner);\n  2581:     /// let arc2 = arc.clone();\n  2582:     /// let inner = Arc::unwrap_or_clone(arc);\n  2583:     /// // Because there were 2 references, we had to clone the inner value.\n  2584:     /// assert!(!ptr::eq(ptr, inner.as_ptr()));\n  2585:     /// // `arc2` is the last reference, so when we unwrap it we get back\n  2586:     /// // the original `String`.\n  2587:     /// let inner = Arc::unwrap_or_clone(arc2);\n  2588:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2589:     /// ```\n  2590:     #[inline]\n  2591:     #[stable(feature = \"arc_unwrap_or_clone\", since = \"1.76.0\")]\n  2592:     pub fn unwrap_or_clone(this: Self) -> T {\n  2593:         Arc::try_unwrap(this).unwrap_or_else(|arc| (*arc).clone())\n  2594:     }\n  2595: }\n  2596: \n  2597: impl<T: ?Sized, A: Allocator> Arc<T, A> {\n  2598:     /// Returns a mutable reference into the given `Arc`, if there are\n  2599:     /// no other `Arc` or [`Weak`] pointers to the same allocation.\n  2600:     ///\n  2601:     /// Returns [`None`] otherwise, because it is not safe to\n  2602:     /// mutate a shared value.\n  2603:     ///\n  2604:     /// See also [`make_mut`][make_mut], which will [`clone`][clone]\n  2605:     /// the inner value when there are other `Arc` pointers.\n  2606:     ///\n  2607:     /// [make_mut]: Arc::make_mut\n  2608:     /// [clone]: Clone::clone",
    "nanvix_source": "  2597:     /// let inner = Arc::unwrap_or_clone(arc);\n  2598:     /// // Because there were 2 references, we had to clone the inner value.\n  2599:     /// assert!(!ptr::eq(ptr, inner.as_ptr()));\n  2600:     /// // `arc2` is the last reference, so when we unwrap it we get back\n  2601:     /// // the original `String`.\n  2602:     /// let inner = Arc::unwrap_or_clone(arc2);\n  2603:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2604:     /// ```\n  2605:     #[inline]\n  2606:     #[stable(feature = \"arc_unwrap_or_clone\", since = \"1.76.0\")]\n  2607:     pub fn unwrap_or_clone(this: Self) -> T {\n  2608:         Arc::try_unwrap(this).unwrap_or_else(|arc| (*arc).clone())\n  2609:     }\n  2610: }\n  2611: \n  2612: impl<T: ?Sized, A: Allocator> Arc<T, A> {\n  2613:     /// Returns a mutable reference into the given `Arc`, if there are\n  2614:     /// no other `Arc` or [`Weak`] pointers to the same allocation.\n  2615:     ///\n  2616:     /// Returns [`None`] otherwise, because it is not safe to\n  2617:     /// mutate a shared value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::weak_count",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4417",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:346",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Arc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
    "verification_source": "  1968:     ///\n  1969:     /// # Examples\n  1970:     ///\n  1971:     /// ```\n  1972:     /// use std::sync::Arc;\n  1973:     ///\n  1974:     /// let five = Arc::new(5);\n  1975:     /// let _weak_five = Arc::downgrade(&five);\n  1976:     ///\n  1977:     /// // This assertion is deterministic because we haven't shared\n  1978:     /// // the `Arc` or `Weak` between threads.\n  1979:     /// assert_eq!(1, Arc::weak_count(&five));\n  1980:     /// ```\n  1981:     #[inline]\n  1982:     #[must_use]\n  1983:     #[stable(feature = \"arc_counts\", since = \"1.15.0\")]\n  1984:     pub fn weak_count(this: &Self) -> usize {\n  1985:         let cnt = this.inner().weak.load(Relaxed);\n  1986:         // If the weak count is currently locked, the value of the\n  1987:         // count was 0 just before taking the lock.\n  1988:         if cnt == usize::MAX { 0 } else { cnt - 1 }\n  1989:     }\n  1990: \n  1991:     /// Gets the number of strong (`Arc`) pointers to this allocation.\n  1992:     ///\n  1993:     /// # Safety\n  1994:     ///\n  1995:     /// This method by itself is safe, but using it correctly requires extra care.\n  1996:     /// Another thread can change the strong count at any time,\n  1997:     /// including potentially between calling this method and acting on the result.\n  1998:     ///\n  1999:     /// # Examples\n  2000:     ///",
    "nanvix_source": "  1986:     /// let five = Arc::new(5);\n  1987:     /// let _weak_five = Arc::downgrade(&five);\n  1988:     ///\n  1989:     /// // This assertion is deterministic because we haven't shared\n  1990:     /// // the `Arc` or `Weak` between threads.\n  1991:     /// assert_eq!(1, Arc::weak_count(&five));\n  1992:     /// ```\n  1993:     #[inline]\n  1994:     #[must_use]\n  1995:     #[stable(feature = \"arc_counts\", since = \"1.15.0\")]\n  1996:     pub fn weak_count(this: &Self) -> usize {\n  1997:         let cnt = this.inner().weak.load(Relaxed);\n  1998:         // If the weak count is currently locked, the value of the\n  1999:         // count was 0 just before taking the lock.\n  2000:         if cnt == usize::MAX { 0 } else { cnt - 1 }\n  2001:     }\n  2002: \n  2003:     /// Gets the number of strong (`Arc`) pointers to this allocation.\n  2004:     ///\n  2005:     /// # Safety\n  2006:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::MaybeUninit::zeroed",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
      "name": "zeroed",
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
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
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
            "id": 8278,
            "path": "MaybeUninit"
          }
        }
      }
    },
    "verification_source": "   463:     ///\n   464:     /// ```rust,no_run\n   465:     /// use std::mem::MaybeUninit;\n   466:     ///\n   467:     /// enum NotZero { One = 1, Two = 2 }\n   468:     ///\n   469:     /// let x = MaybeUninit::<(u8, NotZero)>::zeroed();\n   470:     /// let x = unsafe { x.assume_init() };\n   471:     /// // Inside a pair, we create a `NotZero` that does not have a valid discriminant.\n   472:     /// // This is undefined behavior. \u26a0\ufe0f\n   473:     /// ```\n   474:     #[inline]\n   475:     #[must_use]\n   476:     #[rustc_diagnostic_item = \"maybe_uninit_zeroed\"]\n   477:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   478:     #[rustc_const_stable(feature = \"const_maybe_uninit_zeroed\", since = \"1.75.0\")]\n   479:     pub const fn zeroed() -> MaybeUninit<T> {\n   480:         let mut u = MaybeUninit::<T>::uninit();\n   481:         // SAFETY: `u.as_mut_ptr()` points to allocated memory.\n   482:         unsafe { u.as_mut_ptr().write_bytes(0u8, 1) };\n   483:         u\n   484:     }\n   485: \n   486:     /// Sets the value of the `MaybeUninit<T>`.\n   487:     ///\n   488:     /// This overwrites any previous value without dropping it, so be careful\n   489:     /// not to use this twice unless you want to skip running the destructor.\n   490:     /// For your convenience, this also returns a mutable reference to the\n   491:     /// (now safely initialized) contents of `self`.\n   492:     ///\n   493:     /// As the content is stored inside a `ManuallyDrop`, the destructor is not\n   494:     /// run for the inner data if the MaybeUninit leaves scope without a call to\n   495:     /// [`assume_init`], [`assume_init_drop`], or similar. Code that receives",
    "nanvix_source": "   470:     /// let x = MaybeUninit::<(u8, NotZero)>::zeroed();\n   471:     /// let x = unsafe { x.assume_init() };\n   472:     /// // Inside a pair, we create a `NotZero` that does not have a valid discriminant.\n   473:     /// // This is undefined behavior. \u26a0\ufe0f\n   474:     /// ```\n   475:     #[inline]\n   476:     #[must_use]\n   477:     #[rustc_diagnostic_item = \"maybe_uninit_zeroed\"]\n   478:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   479:     #[rustc_const_stable(feature = \"const_maybe_uninit_zeroed\", since = \"1.75.0\")]\n   480:     pub const fn zeroed() -> MaybeUninit<T> {\n   481:         let mut u = MaybeUninit::<T>::uninit();\n   482:         // SAFETY: `u.as_mut_ptr()` points to allocated memory.\n   483:         unsafe { u.as_mut_ptr().write_bytes(0u8, 1) };\n   484:         u\n   485:     }\n   486: \n   487:     /// Sets the value of the `MaybeUninit<T>`.\n   488:     ///\n   489:     /// This overwrites any previous value without dropping it, so be careful\n   490:     /// not to use this twice unless you want to skip running the destructor.",
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
