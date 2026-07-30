For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicPtr::update",
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
      "concurrency_or_hidden_state",
      "raw_pointer_equality"
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
                                "raw_pointer": {
                                  "is_mutable": true,
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              }
                            ],
                            "output": {
                              "raw_pointer": {
                                "is_mutable": true,
                                "type": {
                                  "generic": "T"
                                }
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
            "name": "impl FnMut(*mut T) -> *mut T"
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
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
                        "type": {
                          "generic": "T"
                        }
                      }
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
        "impl_id": "core:29452",
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
                              "raw_pointer": {
                                "is_mutable": true,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "raw_pointer": {
                              "is_mutable": true,
                              "type": {
                                "generic": "T"
                              }
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2126:     ///\n  2127:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  2128:     ///\n  2129:     /// let ptr: *mut _ = &mut 5;\n  2130:     /// let some_ptr = AtomicPtr::new(ptr);\n  2131:     ///\n  2132:     /// let new: *mut _ = &mut 10;\n  2133:     /// let result = some_ptr.update(Ordering::SeqCst, Ordering::SeqCst, |_| new);\n  2134:     /// assert_eq!(result, ptr);\n  2135:     /// assert_eq!(some_ptr.load(Ordering::SeqCst), new);\n  2136:     /// ```\n  2137:     #[inline]\n  2138:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  2139:     #[cfg(target_has_atomic = \"ptr\")]\n  2140:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2141:     #[rustc_should_not_be_called_on_const_items]\n  2142:     pub fn update(\n  2143:         &self,\n  2144:         set_order: Ordering,\n  2145:         fetch_order: Ordering,\n  2146:         mut f: impl FnMut(*mut T) -> *mut T,\n  2147:     ) -> *mut T {\n  2148:         let mut prev = self.load(fetch_order);\n  2149:         loop {\n  2150:             match self.compare_exchange_weak(prev, f(prev), set_order, fetch_order) {\n  2151:                 Ok(x) => break x,\n  2152:                 Err(next_prev) => prev = next_prev,\n  2153:             }\n  2154:         }\n  2155:     }\n  2156: \n  2157:     /// Offsets the pointer's address by adding `val` (in units of `T`),\n  2158:     /// returning the previous pointer.",
    "nanvix_source": "  2121:     /// let new: *mut _ = &mut 10;\n  2122:     /// let result = some_ptr.update(Ordering::SeqCst, Ordering::SeqCst, |_| new);\n  2123:     /// assert_eq!(result, ptr);\n  2124:     /// assert_eq!(some_ptr.load(Ordering::SeqCst), new);\n  2125:     /// ```\n  2126:     #[inline]\n  2127:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  2128:     #[cfg(target_has_atomic = \"ptr\")]\n  2129:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2130:     #[rustc_should_not_be_called_on_const_items]\n  2131:     pub fn update(\n  2132:         &self,\n  2133:         set_order: Ordering,\n  2134:         fetch_order: Ordering,\n  2135:         mut f: impl FnMut(*mut T) -> *mut T,\n  2136:     ) -> *mut T {\n  2137:         let mut prev = self.load(fetch_order);\n  2138:         loop {\n  2139:             match self.compare_exchange_weak(prev, f(prev), set_order, fetch_order) {\n  2140:                 Ok(x) => break x,\n  2141:                 Err(next_prev) => prev = next_prev,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU16::as_ptr",
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
      "concurrency_or_hidden_state",
      "raw_pointer_equality"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "primitive": "u16"
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
        "impl_id": "core:29552",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "u16"
            }
          }
        }
      }
    },
    "verification_source": "  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }\n  3675: #[cfg(target_has_atomic_load_store = \"16\")]\n  3676: atomic_int! {\n  3677:     cfg(target_has_atomic = \"16\"),\n  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }",
    "nanvix_source": "  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3655:     \"i16\",\n  3656:     \"\",\n  3657:     atomic_min, atomic_max,\n  3658:     2,\n  3659:     i16 AtomicI16\n  3660: }\n  3661: #[cfg(target_has_atomic_load_store = \"16\")]\n  3662: atomic_int! {\n  3663:     cfg(target_has_atomic = \"16\"),\n  3664:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3668:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3669:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU16::compare_and_swap",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "compare_and_swap",
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
                      "primitive": "u16"
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
        "impl_id": "core:29552",
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
            "current",
            {
              "primitive": "u16"
            }
          ],
          [
            "new",
            {
              "primitive": "u16"
            }
          ],
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
        "output": {
          "primitive": "u16"
        }
      }
    },
    "verification_source": "  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }\n  3675: #[cfg(target_has_atomic_load_store = \"16\")]\n  3676: atomic_int! {\n  3677:     cfg(target_has_atomic = \"16\"),\n  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }",
    "nanvix_source": "  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3655:     \"i16\",\n  3656:     \"\",\n  3657:     atomic_min, atomic_max,\n  3658:     2,\n  3659:     i16 AtomicI16\n  3660: }\n  3661: #[cfg(target_has_atomic_load_store = \"16\")]\n  3662: atomic_int! {\n  3663:     cfg(target_has_atomic = \"16\"),\n  3664:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3668:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3669:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU16::fetch_update",
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
                              "primitive": "u16"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "primitive": "u16"
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
      "name": "fetch_update",
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
                      "primitive": "u16"
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
        "impl_id": "core:29552",
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
                      "primitive": "u16"
                    }
                  },
                  {
                    "type": {
                      "primitive": "u16"
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
    "verification_source": "  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }\n  3675: #[cfg(target_has_atomic_load_store = \"16\")]\n  3676: atomic_int! {\n  3677:     cfg(target_has_atomic = \"16\"),\n  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }",
    "nanvix_source": "  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3655:     \"i16\",\n  3656:     \"\",\n  3657:     atomic_min, atomic_max,\n  3658:     2,\n  3659:     i16 AtomicI16\n  3660: }\n  3661: #[cfg(target_has_atomic_load_store = \"16\")]\n  3662: atomic_int! {\n  3663:     cfg(target_has_atomic = \"16\"),\n  3664:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3668:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3669:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU16::from_mut",
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
      "concurrency_or_hidden_state",
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
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "u16"
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
        "impl_id": "core:29552",
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "primitive": "u16"
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
    "verification_source": "  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }\n  3675: #[cfg(target_has_atomic_load_store = \"16\")]\n  3676: atomic_int! {\n  3677:     cfg(target_has_atomic = \"16\"),\n  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }",
    "nanvix_source": "  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3655:     \"i16\",\n  3656:     \"\",\n  3657:     atomic_min, atomic_max,\n  3658:     2,\n  3659:     i16 AtomicI16\n  3660: }\n  3661: #[cfg(target_has_atomic_load_store = \"16\")]\n  3662: atomic_int! {\n  3663:     cfg(target_has_atomic = \"16\"),\n  3664:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3668:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3669:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU16::from_mut_slice",
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
      "concurrency_or_hidden_state",
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
      "name": "from_mut_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "u16"
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
        "impl_id": "core:29552",
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u16"
                  }
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
              "slice": {
                "generic": "Self"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }\n  3675: #[cfg(target_has_atomic_load_store = \"16\")]\n  3676: atomic_int! {\n  3677:     cfg(target_has_atomic = \"16\"),\n  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }",
    "nanvix_source": "  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3655:     \"i16\",\n  3656:     \"\",\n  3657:     atomic_min, atomic_max,\n  3658:     2,\n  3659:     i16 AtomicI16\n  3660: }\n  3661: #[cfg(target_has_atomic_load_store = \"16\")]\n  3662: atomic_int! {\n  3663:     cfg(target_has_atomic = \"16\"),\n  3664:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3668:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3669:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
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
