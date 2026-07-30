For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicUsize::from_mut",
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "primitive": "usize"
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
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::from_mut_slice",
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "usize"
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
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::from_ptr",
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "usize"
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
                "id": 9622,
                "path": "AtomicUsize"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::get_mut",
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
              "primitive": "usize"
            }
          }
        }
      }
    },
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::get_mut_slice",
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
                "primitive": "usize"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3849:         )]\n  3850:         pub const ATOMIC_ISIZE_INIT: AtomicIsize = AtomicIsize::new(0);\n  3851: \n  3852:         /// An [`AtomicUsize`] initialized to `0`.\n  3853:         #[cfg(target_pointer_width = $target_pointer_width)]\n  3854:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3855:         #[deprecated(\n  3856:             since = \"1.34.0\",\n  3857:             note = \"the `new` function is now preferred\",\n  3858:             suggestion = \"AtomicUsize::new(0)\",\n  3859:         )]\n  3860:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3861:     )* };\n  3862: }\n  3863: \n  3864: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3865: atomic_int_ptr_sized! {\n  3866:     \"16\" 2\n  3867:     \"32\" 4\n  3868:     \"64\" 8\n  3869: }\n  3870: \n  3871: #[inline]\n  3872: #[cfg(target_has_atomic)]\n  3873: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3874:     match order {\n  3875:         Release => Relaxed,\n  3876:         Relaxed => Relaxed,\n  3877:         SeqCst => SeqCst,\n  3878:         Acquire => Acquire,\n  3879:         AcqRel => Acquire,\n  3880:     }\n  3881: }",
    "nanvix_source": "  3841:         #[deprecated(\n  3842:             since = \"1.34.0\",\n  3843:             note = \"the `new` function is now preferred\",\n  3844:             suggestion = \"AtomicUsize::new(0)\",\n  3845:         )]\n  3846:         pub const ATOMIC_USIZE_INIT: AtomicUsize = AtomicUsize::new(0);\n  3847:     )* };\n  3848: }\n  3849: \n  3850: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  3851: atomic_int_ptr_sized! {\n  3852:     \"16\" 2\n  3853:     \"32\" 4\n  3854:     \"64\" 8\n  3855: }\n  3856: \n  3857: #[inline]\n  3858: #[cfg(target_has_atomic)]\n  3859: fn strongest_failure_ordering(order: Ordering) -> Ordering {\n  3860:     match order {\n  3861:         Release => Relaxed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicUsize::into_inner",
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
              "generic": "Self"
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
