For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicI16::get_mut",
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
                      "primitive": "i16"
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
        "impl_id": "core:29526",
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
              "primitive": "i16"
            }
          }
        }
      }
    },
    "verification_source": "  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }\n  3657: #[cfg(target_has_atomic_load_store = \"16\")]\n  3658: atomic_int! {\n  3659:     cfg(target_has_atomic = \"16\"),\n  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }",
    "nanvix_source": "  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3637:     \"u8\",\n  3638:     \"\",\n  3639:     atomic_umin, atomic_umax,\n  3640:     1,\n  3641:     u8 AtomicU8\n  3642: }\n  3643: #[cfg(target_has_atomic_load_store = \"16\")]\n  3644: atomic_int! {\n  3645:     cfg(target_has_atomic = \"16\"),\n  3646:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3650:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3651:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI16::get_mut_slice",
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
                      "primitive": "i16"
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
        "impl_id": "core:29526",
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
                "primitive": "i16"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }\n  3657: #[cfg(target_has_atomic_load_store = \"16\")]\n  3658: atomic_int! {\n  3659:     cfg(target_has_atomic = \"16\"),\n  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }",
    "nanvix_source": "  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3637:     \"u8\",\n  3638:     \"\",\n  3639:     atomic_umin, atomic_umax,\n  3640:     1,\n  3641:     u8 AtomicU8\n  3642: }\n  3643: #[cfg(target_has_atomic_load_store = \"16\")]\n  3644: atomic_int! {\n  3645:     cfg(target_has_atomic = \"16\"),\n  3646:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3650:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3651:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI16::into_inner",
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
                      "primitive": "i16"
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
        "impl_id": "core:29526",
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
          "primitive": "i16"
        }
      }
    },
    "verification_source": "  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }\n  3657: #[cfg(target_has_atomic_load_store = \"16\")]\n  3658: atomic_int! {\n  3659:     cfg(target_has_atomic = \"16\"),\n  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }",
    "nanvix_source": "  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3637:     \"u8\",\n  3638:     \"\",\n  3639:     atomic_umin, atomic_umax,\n  3640:     1,\n  3641:     u8 AtomicU8\n  3642: }\n  3643: #[cfg(target_has_atomic_load_store = \"16\")]\n  3644: atomic_int! {\n  3645:     cfg(target_has_atomic = \"16\"),\n  3646:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3650:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3651:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI16::try_update",
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
                                "primitive": "i16"
                              }
                            ],
                            "output": {
                              "resolved_path": {
                                "args": {
                                  "angle_bracketed": {
                                    "args": [
                                      {
                                        "type": {
                                          "primitive": "i16"
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
            "name": "impl FnMut(i16) -> Option<i16>"
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
                      "primitive": "i16"
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
        "impl_id": "core:29526",
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
                              "primitive": "i16"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "primitive": "i16"
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
                      "primitive": "i16"
                    }
                  },
                  {
                    "type": {
                      "primitive": "i16"
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
    "verification_source": "  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }\n  3657: #[cfg(target_has_atomic_load_store = \"16\")]\n  3658: atomic_int! {\n  3659:     cfg(target_has_atomic = \"16\"),\n  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }",
    "nanvix_source": "  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3637:     \"u8\",\n  3638:     \"\",\n  3639:     atomic_umin, atomic_umax,\n  3640:     1,\n  3641:     u8 AtomicU8\n  3642: }\n  3643: #[cfg(target_has_atomic_load_store = \"16\")]\n  3644: atomic_int! {\n  3645:     cfg(target_has_atomic = \"16\"),\n  3646:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3650:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3651:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI16::update",
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
                                "primitive": "i16"
                              }
                            ],
                            "output": {
                              "primitive": "i16"
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
            "name": "impl FnMut(i16) -> i16"
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
                      "primitive": "i16"
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
        "impl_id": "core:29526",
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
                              "primitive": "i16"
                            }
                          ],
                          "output": {
                            "primitive": "i16"
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
          "primitive": "i16"
        }
      }
    },
    "verification_source": "  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }\n  3657: #[cfg(target_has_atomic_load_store = \"16\")]\n  3658: atomic_int! {\n  3659:     cfg(target_has_atomic = \"16\"),\n  3660:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3661:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3662:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3663:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3664:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3665:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3666:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3667:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3668:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3669:     \"i16\",\n  3670:     \"\",\n  3671:     atomic_min, atomic_max,\n  3672:     2,\n  3673:     i16 AtomicI16\n  3674: }",
    "nanvix_source": "  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3637:     \"u8\",\n  3638:     \"\",\n  3639:     atomic_umin, atomic_umax,\n  3640:     1,\n  3641:     u8 AtomicU8\n  3642: }\n  3643: #[cfg(target_has_atomic_load_store = \"16\")]\n  3644: atomic_int! {\n  3645:     cfg(target_has_atomic = \"16\"),\n  3646:     cfg(target_has_atomic_primitive_alignment = \"16\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3650:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3651:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3652:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3653:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3654:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicI32::as_ptr",
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
                      "primitive": "i32"
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
        "impl_id": "core:29578",
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
              "primitive": "i32"
            }
          }
        }
      }
    },
    "verification_source": "  3678:     cfg(target_has_atomic_equal_alignment = \"16\"),\n  3679:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3680:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3681:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3682:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3686:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3687:     \"u16\",\n  3688:     \"\",\n  3689:     atomic_umin, atomic_umax,\n  3690:     2,\n  3691:     u16 AtomicU16\n  3692: }\n  3693: #[cfg(target_has_atomic_load_store = \"32\")]\n  3694: atomic_int! {\n  3695:     cfg(target_has_atomic = \"32\"),\n  3696:     cfg(target_has_atomic_equal_alignment = \"32\"),\n  3697:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3698:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3699:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3700:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3701:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3702:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3703:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3704:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3705:     \"i32\",\n  3706:     \"\",\n  3707:     atomic_min, atomic_max,\n  3708:     4,\n  3709:     i32 AtomicI32\n  3710: }",
    "nanvix_source": "  3670:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3671:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3672:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3673:     \"u16\",\n  3674:     \"\",\n  3675:     atomic_umin, atomic_umax,\n  3676:     2,\n  3677:     u16 AtomicU16\n  3678: }\n  3679: #[cfg(target_has_atomic_load_store = \"32\")]\n  3680: atomic_int! {\n  3681:     cfg(target_has_atomic = \"32\"),\n  3682:     cfg(target_has_atomic_primitive_alignment = \"32\"),\n  3683:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3684:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3685:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3686:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3687:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3688:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3689:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3690:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
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
