For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicI64::fetch_update",
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
                              "primitive": "i64"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "primitive": "i64"
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
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
                      "primitive": "i64"
                    }
                  },
                  {
                    "type": {
                      "primitive": "i64"
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
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI64::from_mut",
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
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
                  "primitive": "i64"
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
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI64::from_mut_slice",
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
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
                    "primitive": "i64"
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
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI64::from_ptr",
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
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "from_ptr",
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
                    "type": {
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "i64"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "resolved_path": {
                "args": null,
                "id": 12052,
                "path": "AtomicI64"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI64::get_mut",
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
      "name": "get_mut",
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
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
              "primitive": "i64"
            }
          }
        }
      }
    },
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI64::get_mut_slice",
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
      "name": "get_mut_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "this"
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
                      "primitive": "i64"
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
        "impl_id": "core:29630",
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
            "this",
            {
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "primitive": "i64"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3714:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3715:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3716:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3717:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3718:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3722:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3723:     \"u32\",\n  3724:     \"\",\n  3725:     atomic_umin, atomic_umax,\n  3726:     4,\n  3727:     u32 AtomicU32\n  3728: }\n  3729: #[cfg(target_has_atomic_load_store = \"64\")]\n  3730: atomic_int! {\n  3731:     cfg(target_has_atomic = \"64\"),\n  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }",
    "nanvix_source": "  3706:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3707:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3708:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3709:     \"u32\",\n  3710:     \"\",\n  3711:     atomic_umin, atomic_umax,\n  3712:     4,\n  3713:     u32 AtomicU32\n  3714: }\n  3715: #[cfg(target_has_atomic_load_store = \"64\")]\n  3716: atomic_int! {\n  3717:     cfg(target_has_atomic = \"64\"),\n  3718:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3719:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3720:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3721:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3722:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3723:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
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
