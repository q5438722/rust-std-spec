For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::Atomic::from_mut",
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
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
                  "primitive": "bool"
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
    "verification_source": "   611:     /// Gets atomic access to a `&mut bool`.\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```\n   616:     /// #![feature(atomic_from_mut)]\n   617:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   618:     ///\n   619:     /// let mut some_bool = true;\n   620:     /// let a = AtomicBool::from_mut(&mut some_bool);\n   621:     /// a.store(false, Ordering::Relaxed);\n   622:     /// assert_eq!(some_bool, false);\n   623:     /// ```\n   624:     #[inline]\n   625:     #[cfg(target_has_atomic_equal_alignment = \"8\")]\n   626:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n   627:     pub fn from_mut(v: &mut bool) -> &mut Self {\n   628:         // SAFETY: the mutable reference guarantees unique ownership, and\n   629:         // alignment of both `bool` and `Self` is 1.\n   630:         unsafe { &mut *(v as *mut bool as *mut Self) }\n   631:     }\n   632: \n   633:     /// Gets non-atomic access to a `&mut [AtomicBool]` slice.\n   634:     ///\n   635:     /// This is safe because the mutable reference guarantees that no other threads are\n   636:     /// concurrently accessing the atomic data.\n   637:     ///\n   638:     /// # Examples\n   639:     ///\n   640:     /// ```ignore-wasm\n   641:     /// #![feature(atomic_from_mut)]\n   642:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   643:     ///",
    "nanvix_source": "   611:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   612:     ///\n   613:     /// let mut some_bool = true;\n   614:     /// let a = AtomicBool::from_mut(&mut some_bool);\n   615:     /// a.store(false, Ordering::Relaxed);\n   616:     /// assert_eq!(some_bool, false);\n   617:     /// ```\n   618:     #[inline]\n   619:     #[cfg(target_has_atomic_primitive_alignment = \"8\")]\n   620:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n   621:     pub fn from_mut(v: &mut bool) -> &mut Self {\n   622:         // SAFETY: the mutable reference guarantees unique ownership, and\n   623:         // alignment of both `bool` and `Self` is 1.\n   624:         unsafe { &mut *(v as *mut bool as *mut Self) }\n   625:     }\n   626: \n   627:     /// Gets non-atomic access to a `&mut [AtomicBool]` slice.\n   628:     ///\n   629:     /// This is safe because the mutable reference guarantees that no other threads are\n   630:     /// concurrently accessing the atomic data.\n   631:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::from_mut_slice",
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
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
                    "primitive": "bool"
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
    "verification_source": "   671:     /// ```rust,ignore-wasm\n   672:     /// #![feature(atomic_from_mut)]\n   673:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   674:     ///\n   675:     /// let mut some_bools = [false; 10];\n   676:     /// let a = &*AtomicBool::from_mut_slice(&mut some_bools);\n   677:     /// std::thread::scope(|s| {\n   678:     ///     for i in 0..a.len() {\n   679:     ///         s.spawn(move || a[i].store(true, Ordering::Relaxed));\n   680:     ///     }\n   681:     /// });\n   682:     /// assert_eq!(some_bools, [true; 10]);\n   683:     /// ```\n   684:     #[inline]\n   685:     #[cfg(target_has_atomic_equal_alignment = \"8\")]\n   686:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n   687:     pub fn from_mut_slice(v: &mut [bool]) -> &mut [Self] {\n   688:         // SAFETY: the mutable reference guarantees unique ownership, and\n   689:         // alignment of both `bool` and `Self` is 1.\n   690:         unsafe { &mut *(v as *mut [bool] as *mut [Self]) }\n   691:     }\n   692: \n   693:     /// Consumes the atomic and returns the contained value.\n   694:     ///\n   695:     /// This is safe because passing `self` by value guarantees that no other threads are\n   696:     /// concurrently accessing the atomic data.\n   697:     ///\n   698:     /// # Examples\n   699:     ///\n   700:     /// ```\n   701:     /// use std::sync::atomic::AtomicBool;\n   702:     ///\n   703:     /// let some_bool = AtomicBool::new(true);",
    "nanvix_source": "   669:     /// std::thread::scope(|s| {\n   670:     ///     for i in 0..a.len() {\n   671:     ///         s.spawn(move || a[i].store(true, Ordering::Relaxed));\n   672:     ///     }\n   673:     /// });\n   674:     /// assert_eq!(some_bools, [true; 10]);\n   675:     /// ```\n   676:     #[inline]\n   677:     #[cfg(target_has_atomic_primitive_alignment = \"8\")]\n   678:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n   679:     pub fn from_mut_slice(v: &mut [bool]) -> &mut [Self] {\n   680:         // SAFETY: the mutable reference guarantees unique ownership, and\n   681:         // alignment of both `bool` and `Self` is 1.\n   682:         unsafe { &mut *(v as *mut [bool] as *mut [Self]) }\n   683:     }\n   684: \n   685:     /// Consumes the atomic and returns the contained value.\n   686:     ///\n   687:     /// This is safe because passing `self` by value guarantees that no other threads are\n   688:     /// concurrently accessing the atomic data.\n   689:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::from_ptr",
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
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
                  "primitive": "bool"
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
                "id": 8239,
                "path": "AtomicBool"
              }
            }
          }
        }
      }
    },
    "verification_source": "   568:     /// ```\n   569:     ///\n   570:     /// # Safety\n   571:     ///\n   572:     /// * `ptr` must be aligned to `align_of::<AtomicBool>()` (note that this is always true, since\n   573:     ///   `align_of::<AtomicBool>() == 1`).\n   574:     /// * `ptr` must be [valid] for both reads and writes for the whole lifetime `'a`.\n   575:     /// * You must adhere to the [Memory model for atomic accesses]. In particular, it is not\n   576:     ///   allowed to mix conflicting atomic and non-atomic accesses, or atomic accesses of different\n   577:     ///   sizes, without synchronization.\n   578:     ///\n   579:     /// [valid]: crate::ptr#safety\n   580:     /// [Memory model for atomic accesses]: self#memory-model-for-atomic-accesses\n   581:     #[inline]\n   582:     #[stable(feature = \"atomic_from_ptr\", since = \"1.75.0\")]\n   583:     #[rustc_const_stable(feature = \"const_atomic_from_ptr\", since = \"1.84.0\")]\n   584:     pub const unsafe fn from_ptr<'a>(ptr: *mut bool) -> &'a AtomicBool {\n   585:         // SAFETY: guaranteed by the caller\n   586:         unsafe { &*ptr.cast() }\n   587:     }\n   588: \n   589:     /// Returns a mutable reference to the underlying [`bool`].\n   590:     ///\n   591:     /// This is safe because the mutable reference guarantees that no other threads are\n   592:     /// concurrently accessing the atomic data.\n   593:     ///\n   594:     /// # Examples\n   595:     ///\n   596:     /// ```\n   597:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   598:     ///\n   599:     /// let mut some_bool = AtomicBool::new(true);\n   600:     /// assert_eq!(*some_bool.get_mut(), true);",
    "nanvix_source": "   569:     /// * `ptr` must be [valid] for both reads and writes for the whole lifetime `'a`.\n   570:     /// * You must adhere to the [Memory model for atomic accesses]. In particular, it is not\n   571:     ///   allowed to mix conflicting atomic and non-atomic accesses, or atomic accesses of different\n   572:     ///   sizes, without synchronization.\n   573:     ///\n   574:     /// [valid]: crate::ptr#safety\n   575:     /// [Memory model for atomic accesses]: self#memory-model-for-atomic-accesses\n   576:     #[inline]\n   577:     #[stable(feature = \"atomic_from_ptr\", since = \"1.75.0\")]\n   578:     #[rustc_const_stable(feature = \"const_atomic_from_ptr\", since = \"1.84.0\")]\n   579:     pub const unsafe fn from_ptr<'a>(ptr: *mut bool) -> &'a AtomicBool {\n   580:         // SAFETY: guaranteed by the caller\n   581:         unsafe { &*ptr.cast() }\n   582:     }\n   583: \n   584:     /// Returns a mutable reference to the underlying [`bool`].\n   585:     ///\n   586:     /// This is safe because the mutable reference guarantees that no other threads are\n   587:     /// concurrently accessing the atomic data.\n   588:     ///\n   589:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::get_mut",
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
      "reference_identity_vs_view",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
              "primitive": "bool"
            }
          }
        }
      }
    },
    "verification_source": "   590:     ///\n   591:     /// This is safe because the mutable reference guarantees that no other threads are\n   592:     /// concurrently accessing the atomic data.\n   593:     ///\n   594:     /// # Examples\n   595:     ///\n   596:     /// ```\n   597:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   598:     ///\n   599:     /// let mut some_bool = AtomicBool::new(true);\n   600:     /// assert_eq!(*some_bool.get_mut(), true);\n   601:     /// *some_bool.get_mut() = false;\n   602:     /// assert_eq!(some_bool.load(Ordering::SeqCst), false);\n   603:     /// ```\n   604:     #[inline]\n   605:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n   606:     pub fn get_mut(&mut self) -> &mut bool {\n   607:         // SAFETY: the mutable reference guarantees unique ownership.\n   608:         unsafe { &mut *self.as_ptr() }\n   609:     }\n   610: \n   611:     /// Gets atomic access to a `&mut bool`.\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```\n   616:     /// #![feature(atomic_from_mut)]\n   617:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   618:     ///\n   619:     /// let mut some_bool = true;\n   620:     /// let a = AtomicBool::from_mut(&mut some_bool);\n   621:     /// a.store(false, Ordering::Relaxed);\n   622:     /// assert_eq!(some_bool, false);",
    "nanvix_source": "   591:     /// ```\n   592:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   593:     ///\n   594:     /// let mut some_bool = AtomicBool::new(true);\n   595:     /// assert_eq!(*some_bool.get_mut(), true);\n   596:     /// *some_bool.get_mut() = false;\n   597:     /// assert_eq!(some_bool.load(Ordering::SeqCst), false);\n   598:     /// ```\n   599:     #[inline]\n   600:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n   601:     pub fn get_mut(&mut self) -> &mut bool {\n   602:         // SAFETY: the mutable reference guarantees unique ownership.\n   603:         unsafe { &mut *self.as_ptr() }\n   604:     }\n   605: \n   606:     /// Gets atomic access to a `&mut bool`.\n   607:     ///\n   608:     /// # Examples\n   609:     ///\n   610:     /// ```\n   611:     /// use std::sync::atomic::{AtomicBool, Ordering};",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::get_mut_slice",
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
      "reference_identity_vs_view",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
                "primitive": "bool"
              }
            }
          }
        }
      }
    },
    "verification_source": "   646:     /// let view: &mut [bool] = AtomicBool::get_mut_slice(&mut some_bools);\n   647:     /// assert_eq!(view, [false; 10]);\n   648:     /// view[..5].copy_from_slice(&[true; 5]);\n   649:     ///\n   650:     /// std::thread::scope(|s| {\n   651:     ///     for t in &some_bools[..5] {\n   652:     ///         s.spawn(move || assert_eq!(t.load(Ordering::Relaxed), true));\n   653:     ///     }\n   654:     ///\n   655:     ///     for f in &some_bools[5..] {\n   656:     ///         s.spawn(move || assert_eq!(f.load(Ordering::Relaxed), false));\n   657:     ///     }\n   658:     /// });\n   659:     /// ```\n   660:     #[inline]\n   661:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n   662:     pub fn get_mut_slice(this: &mut [Self]) -> &mut [bool] {\n   663:         // SAFETY: the mutable reference guarantees unique ownership.\n   664:         unsafe { &mut *(this as *mut [Self] as *mut [bool]) }\n   665:     }\n   666: \n   667:     /// Gets atomic access to a `&mut [bool]` slice.\n   668:     ///\n   669:     /// # Examples\n   670:     ///\n   671:     /// ```rust,ignore-wasm\n   672:     /// #![feature(atomic_from_mut)]\n   673:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   674:     ///\n   675:     /// let mut some_bools = [false; 10];\n   676:     /// let a = &*AtomicBool::from_mut_slice(&mut some_bools);\n   677:     /// std::thread::scope(|s| {\n   678:     ///     for i in 0..a.len() {",
    "nanvix_source": "   645:     ///         s.spawn(move || assert_eq!(t.load(Ordering::Relaxed), true));\n   646:     ///     }\n   647:     ///\n   648:     ///     for f in &some_bools[5..] {\n   649:     ///         s.spawn(move || assert_eq!(f.load(Ordering::Relaxed), false));\n   650:     ///     }\n   651:     /// });\n   652:     /// ```\n   653:     #[inline]\n   654:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n   655:     pub fn get_mut_slice(this: &mut [Self]) -> &mut [bool] {\n   656:         // SAFETY: the mutable reference guarantees unique ownership.\n   657:         unsafe { &mut *(this as *mut [Self] as *mut [bool]) }\n   658:     }\n   659: \n   660:     /// Gets atomic access to a `&mut [bool]` slice.\n   661:     ///\n   662:     /// # Examples\n   663:     ///\n   664:     /// ```rust,ignore-wasm\n   665:     /// use std::sync::atomic::{AtomicBool, Ordering};",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::into_inner",
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
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
                      "primitive": "bool"
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
        "impl_id": "core:29422",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   693:     /// Consumes the atomic and returns the contained value.\n   694:     ///\n   695:     /// This is safe because passing `self` by value guarantees that no other threads are\n   696:     /// concurrently accessing the atomic data.\n   697:     ///\n   698:     /// # Examples\n   699:     ///\n   700:     /// ```\n   701:     /// use std::sync::atomic::AtomicBool;\n   702:     ///\n   703:     /// let some_bool = AtomicBool::new(true);\n   704:     /// assert_eq!(some_bool.into_inner(), true);\n   705:     /// ```\n   706:     #[inline]\n   707:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n   708:     #[rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\")]\n   709:     pub const fn into_inner(self) -> bool {\n   710:         // SAFETY:\n   711:         // * `Atomic<T>` is essentially a transparent wrapper around `T`.\n   712:         // * all operations on `Atomic<bool>` ensure that `T::Storage` remains\n   713:         //   a valid `bool`.\n   714:         unsafe { transmute(self) }\n   715:     }\n   716: \n   717:     /// Loads a value from the bool.\n   718:     ///\n   719:     /// `load` takes an [`Ordering`] argument which describes the memory ordering\n   720:     /// of this operation. Possible values are [`SeqCst`], [`Acquire`] and [`Relaxed`].\n   721:     ///\n   722:     /// # Panics\n   723:     ///\n   724:     /// Panics if `order` is [`Release`] or [`AcqRel`].\n   725:     ///",
    "nanvix_source": "   691:     ///\n   692:     /// ```\n   693:     /// use std::sync::atomic::AtomicBool;\n   694:     ///\n   695:     /// let some_bool = AtomicBool::new(true);\n   696:     /// assert_eq!(some_bool.into_inner(), true);\n   697:     /// ```\n   698:     #[inline]\n   699:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n   700:     #[rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\")]\n   701:     pub const fn into_inner(self) -> bool {\n   702:         // SAFETY:\n   703:         // * `Atomic<T>` is essentially a transparent wrapper around `T`.\n   704:         // * all operations on `Atomic<bool>` ensure that `T::Storage` remains\n   705:         //   a valid `bool`.\n   706:         unsafe { transmute(self) }\n   707:     }\n   708: \n   709:     /// Loads a value from the bool.\n   710:     ///\n   711:     /// `load` takes an [`Ordering`] argument which describes the memory ordering",
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
