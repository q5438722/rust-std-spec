For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicUsize::try_update",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state"
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
                            "inputs": [
                              {
                                "primitive": "usize"
                              }
                            ],
                            "output": {
                              "resolved_path": {
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
                                "id": 84,
                                "path": "Option"
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
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnMut(usize) -> Option<usize>"
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
      "name": "try_update",
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
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29708",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "set_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ],
          [
            "fetch_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
                              "primitive": "usize"
                            }
                          ],
                          "output": {
                            "resolved_path": {
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
                              "id": 84,
                              "path": "Option"
                            }
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::update",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state"
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
                            "inputs": [
                              {
                                "primitive": "usize"
                              }
                            ],
                            "output": {
                              "primitive": "usize"
                            }
                          }
                        },
                        "id": 22,
                        "path": "FnMut"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnMut(usize) -> usize"
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
      "name": "update",
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
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29708",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "set_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ],
          [
            "fetch_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
                              "primitive": "usize"
                            }
                          ],
                          "output": {
                            "primitive": "usize"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::compiler_fence",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "unit_return_variant"
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
      "name": "compiler_fence",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4445: ///     compiler_fence(Ordering::Release);\n  4446: ///     IS_READY.store(true, Ordering::Relaxed);\n  4447: /// }\n  4448: ///\n  4449: /// fn signal_handler() {\n  4450: ///     if IS_READY.load(Ordering::Relaxed) {\n  4451: ///         // Acquires writes that were released with relaxed stores that we read from.\n  4452: ///         compiler_fence(Ordering::Acquire);\n  4453: ///         assert_eq!(unsafe { IMPORTANT_VARIABLE }, 42);\n  4454: ///     }\n  4455: /// }\n  4456: /// ```\n  4457: #[inline]\n  4458: #[stable(feature = \"compiler_fences\", since = \"1.21.0\")]\n  4459: #[rustc_diagnostic_item = \"compiler_fence\"]\n  4460: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  4461: pub fn compiler_fence(order: Ordering) {\n  4462:     // SAFETY: using an atomic fence is safe.\n  4463:     unsafe {\n  4464:         match order {\n  4465:             Acquire => intrinsics::atomic_singlethreadfence::<{ AO::Acquire }>(),\n  4466:             Release => intrinsics::atomic_singlethreadfence::<{ AO::Release }>(),\n  4467:             AcqRel => intrinsics::atomic_singlethreadfence::<{ AO::AcqRel }>(),\n  4468:             SeqCst => intrinsics::atomic_singlethreadfence::<{ AO::SeqCst }>(),\n  4469:             Relaxed => panic!(\"there is no such thing as a relaxed fence\"),\n  4470:         }\n  4471:     }\n  4472: }\n  4473: \n  4474: #[cfg(target_has_atomic_load_store = \"8\")]\n  4475: #[stable(feature = \"atomic_debug\", since = \"1.3.0\")]\n  4476: impl fmt::Debug for AtomicBool {\n  4477:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "nanvix_source": "  4445: ///         compiler_fence(Ordering::Acquire);\n  4446: ///         assert_eq!(unsafe { IMPORTANT_VARIABLE }, 42);\n  4447: ///     }\n  4448: /// }\n  4449: /// ```\n  4450: #[inline]\n  4451: #[stable(feature = \"compiler_fences\", since = \"1.21.0\")]\n  4452: #[rustc_diagnostic_item = \"compiler_fence\"]\n  4453: #[doc(alias = \"atomic_signal_fence\")]\n  4454: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  4455: pub fn compiler_fence(order: Ordering) {\n  4456:     // SAFETY: using an atomic fence is safe.\n  4457:     unsafe {\n  4458:         match order {\n  4459:             Acquire => intrinsics::atomic_singlethreadfence::<{ AO::Acquire }>(),\n  4460:             Release => intrinsics::atomic_singlethreadfence::<{ AO::Release }>(),\n  4461:             AcqRel => intrinsics::atomic_singlethreadfence::<{ AO::AcqRel }>(),\n  4462:             SeqCst => intrinsics::atomic_singlethreadfence::<{ AO::SeqCst }>(),\n  4463:             Relaxed => panic!(\"there is no such thing as a relaxed fence\"),\n  4464:         }\n  4465:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::fence",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "unit_return_variant"
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
      "name": "fence",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4367: ///             .compare_exchange_weak(false, true, Ordering::Relaxed, Ordering::Relaxed)\n  4368: ///             .is_err()\n  4369: ///         {}\n  4370: ///         // This fence synchronizes-with store in `unlock`.\n  4371: ///         fence(Ordering::Acquire);\n  4372: ///     }\n  4373: ///\n  4374: ///     pub fn unlock(&self) {\n  4375: ///         self.flag.store(false, Ordering::Release);\n  4376: ///     }\n  4377: /// }\n  4378: /// ```\n  4379: #[inline]\n  4380: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  4381: #[rustc_diagnostic_item = \"fence\"]\n  4382: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  4383: pub fn fence(order: Ordering) {\n  4384:     // SAFETY: using an atomic fence is safe.\n  4385:     unsafe {\n  4386:         match order {\n  4387:             Acquire => intrinsics::atomic_fence::<{ AO::Acquire }>(),\n  4388:             Release => intrinsics::atomic_fence::<{ AO::Release }>(),\n  4389:             AcqRel => intrinsics::atomic_fence::<{ AO::AcqRel }>(),\n  4390:             SeqCst => intrinsics::atomic_fence::<{ AO::SeqCst }>(),\n  4391:             Relaxed => panic!(\"there is no such thing as a relaxed fence\"),\n  4392:         }\n  4393:     }\n  4394: }\n  4395: \n  4396: /// A \"compiler-only\" atomic fence.\n  4397: ///\n  4398: /// Like [`fence`], this function establishes synchronization with other atomic operations and\n  4399: /// fences. However, unlike [`fence`], `compiler_fence` only establishes synchronization with",
    "nanvix_source": "  4361: ///     pub fn unlock(&self) {\n  4362: ///         self.flag.store(false, Ordering::Release);\n  4363: ///     }\n  4364: /// }\n  4365: /// ```\n  4366: #[inline]\n  4367: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  4368: #[rustc_diagnostic_item = \"fence\"]\n  4369: #[doc(alias = \"atomic_thread_fence\")]\n  4370: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  4371: pub fn fence(order: Ordering) {\n  4372:     // SAFETY: using an atomic fence is safe.\n  4373:     unsafe {\n  4374:         match order {\n  4375:             Acquire => intrinsics::atomic_fence::<{ AO::Acquire }>(),\n  4376:             Release => intrinsics::atomic_fence::<{ AO::Release }>(),\n  4377:             AcqRel => intrinsics::atomic_fence::<{ AO::AcqRel }>(),\n  4378:             SeqCst => intrinsics::atomic_fence::<{ AO::SeqCst }>(),\n  4379:             Relaxed => panic!(\"there is no such thing as a relaxed fence\"),\n  4380:         }\n  4381:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::spin_loop_hint",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "unit_return_variant"
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
      "name": "spin_loop_hint",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4469:             Relaxed => panic!(\"there is no such thing as a relaxed fence\"),\n  4470:         }\n  4471:     }\n  4472: }\n  4473: \n  4474: #[cfg(target_has_atomic_load_store = \"8\")]\n  4475: #[stable(feature = \"atomic_debug\", since = \"1.3.0\")]\n  4476: impl fmt::Debug for AtomicBool {\n  4477:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4478:         fmt::Debug::fmt(&self.load(Ordering::Relaxed), f)\n  4479:     }\n  4480: }\n  4481: \n  4482: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  4483: #[stable(feature = \"atomic_debug\", since = \"1.3.0\")]\n  4484: impl<T> fmt::Debug for AtomicPtr<T> {\n  4485:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4486:         fmt::Debug::fmt(&self.load(Ordering::Relaxed), f)\n  4487:     }\n  4488: }\n  4489: \n  4490: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  4491: #[stable(feature = \"atomic_pointer\", since = \"1.24.0\")]\n  4492: impl<T> fmt::Pointer for AtomicPtr<T> {\n  4493:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4494:         fmt::Pointer::fmt(&self.load(Ordering::Relaxed), f)\n  4495:     }\n  4496: }\n  4497: \n  4498: /// Signals the processor that it is inside a busy-wait spin-loop (\"spin lock\").\n  4499: ///\n  4500: /// This function is deprecated in favor of [`hint::spin_loop`].\n  4501: ///",
    "nanvix_source": "  4469: #[stable(feature = \"atomic_debug\", since = \"1.3.0\")]\n  4470: impl fmt::Debug for AtomicBool {\n  4471:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4472:         fmt::Debug::fmt(&self.load(Ordering::Relaxed), f)\n  4473:     }\n  4474: }\n  4475: \n  4476: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  4477: #[stable(feature = \"atomic_debug\", since = \"1.3.0\")]\n  4478: impl<T> fmt::Debug for AtomicPtr<T> {\n  4479:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4480:         fmt::Debug::fmt(&self.load(Ordering::Relaxed), f)\n  4481:     }\n  4482: }\n  4483: \n  4484: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  4485: #[stable(feature = \"atomic_pointer\", since = \"1.24.0\")]\n  4486: impl<T> fmt::Pointer for AtomicPtr<T> {\n  4487:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  4488:         fmt::Pointer::fmt(&self.load(Ordering::Relaxed), f)\n  4489:     }",
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
