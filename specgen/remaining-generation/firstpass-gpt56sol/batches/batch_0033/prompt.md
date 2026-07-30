For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicU64::get_mut_slice",
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
                      "primitive": "u64"
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
        "impl_id": "core:29656",
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
                "primitive": "u64"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }\n  3747: #[cfg(target_has_atomic_load_store = \"64\")]\n  3748: atomic_int! {\n  3749:     cfg(target_has_atomic = \"64\"),\n  3750:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3751:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3752:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3753:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3754:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3755:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3756:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3757:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3758:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3759:     \"u64\",\n  3760:     \"\",\n  3761:     atomic_umin, atomic_umax,\n  3762:     8,\n  3763:     u64 AtomicU64\n  3764: }",
    "nanvix_source": "  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3727:     \"i64\",\n  3728:     \"\",\n  3729:     atomic_min, atomic_max,\n  3730:     8,\n  3731:     i64 AtomicI64\n  3732: }\n  3733: #[cfg(target_has_atomic_load_store = \"64\")]\n  3734: atomic_int! {\n  3735:     cfg(target_has_atomic = \"64\"),\n  3736:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3740:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3741:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3742:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3743:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3744:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU64::into_inner",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "into_inner",
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
                      "primitive": "u64"
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
        "impl_id": "core:29656",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "u64"
        }
      }
    },
    "verification_source": "  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }\n  3747: #[cfg(target_has_atomic_load_store = \"64\")]\n  3748: atomic_int! {\n  3749:     cfg(target_has_atomic = \"64\"),\n  3750:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3751:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3752:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3753:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3754:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3755:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3756:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3757:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3758:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3759:     \"u64\",\n  3760:     \"\",\n  3761:     atomic_umin, atomic_umax,\n  3762:     8,\n  3763:     u64 AtomicU64\n  3764: }",
    "nanvix_source": "  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3727:     \"i64\",\n  3728:     \"\",\n  3729:     atomic_min, atomic_max,\n  3730:     8,\n  3731:     i64 AtomicI64\n  3732: }\n  3733: #[cfg(target_has_atomic_load_store = \"64\")]\n  3734: atomic_int! {\n  3735:     cfg(target_has_atomic = \"64\"),\n  3736:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3740:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3741:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3742:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3743:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3744:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU64::try_update",
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
                                "primitive": "u64"
                              }
                            ],
                            "output": {
                              "resolved_path": {
                                "args": {
                                  "angle_bracketed": {
                                    "args": [
                                      {
                                        "type": {
                                          "primitive": "u64"
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
            "name": "impl FnMut(u64) -> Option<u64>"
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
                      "primitive": "u64"
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
        "impl_id": "core:29656",
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
                              "primitive": "u64"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "primitive": "u64"
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
                      "primitive": "u64"
                    }
                  },
                  {
                    "type": {
                      "primitive": "u64"
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
    "verification_source": "  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }\n  3747: #[cfg(target_has_atomic_load_store = \"64\")]\n  3748: atomic_int! {\n  3749:     cfg(target_has_atomic = \"64\"),\n  3750:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3751:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3752:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3753:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3754:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3755:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3756:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3757:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3758:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3759:     \"u64\",\n  3760:     \"\",\n  3761:     atomic_umin, atomic_umax,\n  3762:     8,\n  3763:     u64 AtomicU64\n  3764: }",
    "nanvix_source": "  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3727:     \"i64\",\n  3728:     \"\",\n  3729:     atomic_min, atomic_max,\n  3730:     8,\n  3731:     i64 AtomicI64\n  3732: }\n  3733: #[cfg(target_has_atomic_load_store = \"64\")]\n  3734: atomic_int! {\n  3735:     cfg(target_has_atomic = \"64\"),\n  3736:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3740:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3741:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3742:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3743:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3744:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU64::update",
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
                                "primitive": "u64"
                              }
                            ],
                            "output": {
                              "primitive": "u64"
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
            "name": "impl FnMut(u64) -> u64"
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
                      "primitive": "u64"
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
        "impl_id": "core:29656",
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
                              "primitive": "u64"
                            }
                          ],
                          "output": {
                            "primitive": "u64"
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "  3732:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3733:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3734:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3735:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3736:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3740:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3741:     \"i64\",\n  3742:     \"\",\n  3743:     atomic_min, atomic_max,\n  3744:     8,\n  3745:     i64 AtomicI64\n  3746: }\n  3747: #[cfg(target_has_atomic_load_store = \"64\")]\n  3748: atomic_int! {\n  3749:     cfg(target_has_atomic = \"64\"),\n  3750:     cfg(target_has_atomic_equal_alignment = \"64\"),\n  3751:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3752:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3753:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3754:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3755:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3756:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3757:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3758:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3759:     \"u64\",\n  3760:     \"\",\n  3761:     atomic_umin, atomic_umax,\n  3762:     8,\n  3763:     u64 AtomicU64\n  3764: }",
    "nanvix_source": "  3724:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3725:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3726:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3727:     \"i64\",\n  3728:     \"\",\n  3729:     atomic_min, atomic_max,\n  3730:     8,\n  3731:     i64 AtomicI64\n  3732: }\n  3733: #[cfg(target_has_atomic_load_store = \"64\")]\n  3734: atomic_int! {\n  3735:     cfg(target_has_atomic = \"64\"),\n  3736:     cfg(target_has_atomic_primitive_alignment = \"64\"),\n  3737:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3738:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3739:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3740:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3741:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3742:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3743:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3744:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU8::as_ptr",
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
                      "primitive": "u8"
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
        "impl_id": "core:29500",
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
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "  3624:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3625:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3626:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3627:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3628:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3632:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3633:     \"i8\",\n  3634:     \"\",\n  3635:     atomic_min, atomic_max,\n  3636:     1,\n  3637:     i8 AtomicI8\n  3638: }\n  3639: #[cfg(target_has_atomic_load_store = \"8\")]\n  3640: atomic_int! {\n  3641:     cfg(target_has_atomic = \"8\"),\n  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }",
    "nanvix_source": "  3616:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3617:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3618:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3619:     \"i8\",\n  3620:     \"\",\n  3621:     atomic_min, atomic_max,\n  3622:     1,\n  3623:     i8 AtomicI8\n  3624: }\n  3625: #[cfg(target_has_atomic_load_store = \"8\")]\n  3626: atomic_int! {\n  3627:     cfg(target_has_atomic = \"8\"),\n  3628:     cfg(target_has_atomic_primitive_alignment = \"8\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3632:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3633:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicU8::compare_and_swap",
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
                      "primitive": "u8"
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
        "impl_id": "core:29500",
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
              "primitive": "u8"
            }
          ],
          [
            "new",
            {
              "primitive": "u8"
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
          "primitive": "u8"
        }
      }
    },
    "verification_source": "  3624:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3625:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3626:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3627:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3628:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3632:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3633:     \"i8\",\n  3634:     \"\",\n  3635:     atomic_min, atomic_max,\n  3636:     1,\n  3637:     i8 AtomicI8\n  3638: }\n  3639: #[cfg(target_has_atomic_load_store = \"8\")]\n  3640: atomic_int! {\n  3641:     cfg(target_has_atomic = \"8\"),\n  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }",
    "nanvix_source": "  3616:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3617:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3618:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3619:     \"i8\",\n  3620:     \"\",\n  3621:     atomic_min, atomic_max,\n  3622:     1,\n  3623:     i8 AtomicI8\n  3624: }\n  3625: #[cfg(target_has_atomic_load_store = \"8\")]\n  3626: atomic_int! {\n  3627:     cfg(target_has_atomic = \"8\"),\n  3628:     cfg(target_has_atomic_primitive_alignment = \"8\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3632:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3633:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
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
