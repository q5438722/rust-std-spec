For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::Atomic::load",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "load",
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1714:     ///\n  1715:     /// Panics if `order` is [`Release`] or [`AcqRel`].\n  1716:     ///\n  1717:     /// # Examples\n  1718:     ///\n  1719:     /// ```\n  1720:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1721:     ///\n  1722:     /// let ptr = &mut 5;\n  1723:     /// let some_ptr = AtomicPtr::new(ptr);\n  1724:     ///\n  1725:     /// let value = some_ptr.load(Ordering::Relaxed);\n  1726:     /// ```\n  1727:     #[inline]\n  1728:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1729:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1730:     pub fn load(&self, order: Ordering) -> *mut T {\n  1731:         // SAFETY: data races are prevented by atomic intrinsics.\n  1732:         unsafe { atomic_load(self.as_ptr(), order) }\n  1733:     }\n  1734: \n  1735:     /// Stores a value into the pointer.\n  1736:     ///\n  1737:     /// `store` takes an [`Ordering`] argument which describes the memory ordering\n  1738:     /// of this operation. Possible values are [`SeqCst`], [`Release`] and [`Relaxed`].\n  1739:     ///\n  1740:     /// # Panics\n  1741:     ///\n  1742:     /// Panics if `order` is [`Acquire`] or [`AcqRel`].\n  1743:     ///\n  1744:     /// # Examples\n  1745:     ///\n  1746:     /// ```",
    "nanvix_source": "  1709:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1710:     ///\n  1711:     /// let ptr = &mut 5;\n  1712:     /// let some_ptr = AtomicPtr::new(ptr);\n  1713:     ///\n  1714:     /// let value = some_ptr.load(Ordering::Relaxed);\n  1715:     /// ```\n  1716:     #[inline]\n  1717:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1718:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1719:     pub fn load(&self, order: Ordering) -> *mut T {\n  1720:         // SAFETY: data races are prevented by atomic intrinsics.\n  1721:         unsafe { atomic_load(self.as_ptr(), order) }\n  1722:     }\n  1723: \n  1724:     /// Stores a value into the pointer.\n  1725:     ///\n  1726:     /// `store` takes an [`Ordering`] argument which describes the memory ordering\n  1727:     /// of this operation. Possible values are [`SeqCst`], [`Release`] and [`Relaxed`].\n  1728:     ///\n  1729:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::new",
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
              "primitive": "bool"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 8239,
            "path": "AtomicBool"
          }
        }
      }
    },
    "verification_source": "   520: #[cfg(target_has_atomic_load_store = \"8\")]\n   521: impl AtomicBool {\n   522:     /// Creates a new `AtomicBool`.\n   523:     ///\n   524:     /// # Examples\n   525:     ///\n   526:     /// ```\n   527:     /// use std::sync::atomic::AtomicBool;\n   528:     ///\n   529:     /// let atomic_true = AtomicBool::new(true);\n   530:     /// let atomic_false = AtomicBool::new(false);\n   531:     /// ```\n   532:     #[inline]\n   533:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   534:     #[rustc_const_stable(feature = \"const_atomic_new\", since = \"1.24.0\")]\n   535:     #[must_use]\n   536:     pub const fn new(v: bool) -> AtomicBool {\n   537:         // SAFETY:\n   538:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n   539:         unsafe { transmute(v) }\n   540:     }\n   541: \n   542:     /// Creates a new `AtomicBool` from a pointer.\n   543:     ///\n   544:     /// # Examples\n   545:     ///\n   546:     /// ```\n   547:     /// use std::sync::atomic::{self, AtomicBool};\n   548:     ///\n   549:     /// // Get a pointer to an allocated value\n   550:     /// let ptr: *mut bool = Box::into_raw(Box::new(false));\n   551:     ///\n   552:     /// assert!(ptr.cast::<AtomicBool>().is_aligned());",
    "nanvix_source": "   521:     /// ```\n   522:     /// use std::sync::atomic::AtomicBool;\n   523:     ///\n   524:     /// let atomic_true = AtomicBool::new(true);\n   525:     /// let atomic_false = AtomicBool::new(false);\n   526:     /// ```\n   527:     #[inline]\n   528:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   529:     #[rustc_const_stable(feature = \"const_atomic_new\", since = \"1.24.0\")]\n   530:     #[must_use]\n   531:     pub const fn new(v: bool) -> AtomicBool {\n   532:         // SAFETY:\n   533:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n   534:         unsafe { transmute(v) }\n   535:     }\n   536: \n   537:     /// Creates a new `AtomicBool` from a pointer.\n   538:     ///\n   539:     /// # Examples\n   540:     ///\n   541:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::store",
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
      "unit_return_variant",
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
      "name": "store",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
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
        "output": null
      }
    },
    "verification_source": "  1744:     /// # Examples\n  1745:     ///\n  1746:     /// ```\n  1747:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1748:     ///\n  1749:     /// let ptr = &mut 5;\n  1750:     /// let some_ptr = AtomicPtr::new(ptr);\n  1751:     ///\n  1752:     /// let other_ptr = &mut 10;\n  1753:     ///\n  1754:     /// some_ptr.store(other_ptr, Ordering::Relaxed);\n  1755:     /// ```\n  1756:     #[inline]\n  1757:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1758:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1759:     #[rustc_should_not_be_called_on_const_items]\n  1760:     pub fn store(&self, ptr: *mut T, order: Ordering) {\n  1761:         // SAFETY: data races are prevented by atomic intrinsics.\n  1762:         unsafe {\n  1763:             atomic_store(self.as_ptr(), ptr, order);\n  1764:         }\n  1765:     }\n  1766: \n  1767:     /// Stores a value into the pointer, returning the previous value.\n  1768:     ///\n  1769:     /// `swap` takes an [`Ordering`] argument which describes the memory ordering\n  1770:     /// of this operation. All ordering modes are possible. Note that using\n  1771:     /// [`Acquire`] makes the store part of this operation [`Relaxed`], and\n  1772:     /// using [`Release`] makes the load part [`Relaxed`].\n  1773:     ///\n  1774:     /// **Note:** This method is only available on platforms that support atomic\n  1775:     /// operations on pointers.\n  1776:     ///",
    "nanvix_source": "  1739:     /// let some_ptr = AtomicPtr::new(ptr);\n  1740:     ///\n  1741:     /// let other_ptr = &mut 10;\n  1742:     ///\n  1743:     /// some_ptr.store(other_ptr, Ordering::Relaxed);\n  1744:     /// ```\n  1745:     #[inline]\n  1746:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1747:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1748:     #[rustc_should_not_be_called_on_const_items]\n  1749:     pub fn store(&self, ptr: *mut T, order: Ordering) {\n  1750:         // SAFETY: data races are prevented by atomic intrinsics.\n  1751:         unsafe {\n  1752:             atomic_store(self.as_ptr(), ptr, order);\n  1753:         }\n  1754:     }\n  1755: \n  1756:     /// Stores a value into the pointer, returning the previous value.\n  1757:     ///\n  1758:     /// `swap` takes an [`Ordering`] argument which describes the memory ordering\n  1759:     /// of this operation. All ordering modes are possible. Note that using",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::swap",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "swap",
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1778:     ///\n  1779:     /// ```\n  1780:     /// use std::sync::atomic::{AtomicPtr, Ordering};\n  1781:     ///\n  1782:     /// let ptr = &mut 5;\n  1783:     /// let some_ptr = AtomicPtr::new(ptr);\n  1784:     ///\n  1785:     /// let other_ptr = &mut 10;\n  1786:     ///\n  1787:     /// let value = some_ptr.swap(other_ptr, Ordering::Relaxed);\n  1788:     /// ```\n  1789:     #[inline]\n  1790:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1791:     #[cfg(target_has_atomic = \"ptr\")]\n  1792:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1793:     #[rustc_should_not_be_called_on_const_items]\n  1794:     pub fn swap(&self, ptr: *mut T, order: Ordering) -> *mut T {\n  1795:         // SAFETY: data races are prevented by atomic intrinsics.\n  1796:         unsafe { atomic_swap(self.as_ptr(), ptr, order) }\n  1797:     }\n  1798: \n  1799:     /// Stores a value into the pointer if the current value is the same as the `current` value.\n  1800:     ///\n  1801:     /// The return value is always the previous value. If it is equal to `current`, then the value\n  1802:     /// was updated.\n  1803:     ///\n  1804:     /// `compare_and_swap` also takes an [`Ordering`] argument which describes the memory\n  1805:     /// ordering of this operation. Notice that even when using [`AcqRel`], the operation\n  1806:     /// might fail and hence just perform an `Acquire` load, but not have `Release` semantics.\n  1807:     /// Using [`Acquire`] makes the store part of this operation [`Relaxed`] if it\n  1808:     /// happens, and using [`Release`] makes the load part [`Relaxed`].\n  1809:     ///\n  1810:     /// **Note:** This method is only available on platforms that support atomic",
    "nanvix_source": "  1773:     ///\n  1774:     /// let other_ptr = &mut 10;\n  1775:     ///\n  1776:     /// let value = some_ptr.swap(other_ptr, Ordering::Relaxed);\n  1777:     /// ```\n  1778:     #[inline]\n  1779:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1780:     #[cfg(target_has_atomic = \"ptr\")]\n  1781:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1782:     #[rustc_should_not_be_called_on_const_items]\n  1783:     pub fn swap(&self, ptr: *mut T, order: Ordering) -> *mut T {\n  1784:         // SAFETY: data races are prevented by atomic intrinsics.\n  1785:         unsafe { atomic_swap(self.as_ptr(), ptr, order) }\n  1786:     }\n  1787: \n  1788:     /// Stores a value into the pointer if the current value is the same as the `current` value.\n  1789:     ///\n  1790:     /// The return value is always the previous value. If it is equal to `current`, then the value\n  1791:     /// was updated.\n  1792:     ///\n  1793:     /// `compare_and_swap` also takes an [`Ordering`] argument which describes the memory",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::try_update",
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
                                "primitive": "bool"
                              }
                            ],
                            "output": {
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
            "name": "impl FnMut(bool) -> Option<bool>"
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
                              "primitive": "bool"
                            }
                          ],
                          "output": {
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
                      "primitive": "bool"
                    }
                  },
                  {
                    "type": {
                      "primitive": "bool"
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
    "verification_source": "  1373:     /// # Examples\n  1374:     ///\n  1375:     /// ```rust\n  1376:     /// use std::sync::atomic::{AtomicBool, Ordering};\n  1377:     ///\n  1378:     /// let x = AtomicBool::new(false);\n  1379:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |_| None), Err(false));\n  1380:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |x| Some(!x)), Ok(false));\n  1381:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |x| Some(!x)), Ok(true));\n  1382:     /// assert_eq!(x.load(Ordering::SeqCst), false);\n  1383:     /// ```\n  1384:     #[inline]\n  1385:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  1386:     #[cfg(target_has_atomic = \"8\")]\n  1387:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1388:     #[rustc_should_not_be_called_on_const_items]\n  1389:     pub fn try_update(\n  1390:         &self,\n  1391:         set_order: Ordering,\n  1392:         fetch_order: Ordering,\n  1393:         mut f: impl FnMut(bool) -> Option<bool>,\n  1394:     ) -> Result<bool, bool> {\n  1395:         let mut prev = self.load(fetch_order);\n  1396:         while let Some(next) = f(prev) {\n  1397:             match self.compare_exchange_weak(prev, next, set_order, fetch_order) {\n  1398:                 x @ Ok(_) => return x,\n  1399:                 Err(next_prev) => prev = next_prev,\n  1400:             }\n  1401:         }\n  1402:         Err(prev)\n  1403:     }\n  1404: \n  1405:     /// Fetches the value, applies a function to it that it return a new value.",
    "nanvix_source": "  1371:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |_| None), Err(false));\n  1372:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |x| Some(!x)), Ok(false));\n  1373:     /// assert_eq!(x.try_update(Ordering::SeqCst, Ordering::SeqCst, |x| Some(!x)), Ok(true));\n  1374:     /// assert_eq!(x.load(Ordering::SeqCst), false);\n  1375:     /// ```\n  1376:     #[inline]\n  1377:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  1378:     #[cfg(target_has_atomic = \"8\")]\n  1379:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1380:     #[rustc_should_not_be_called_on_const_items]\n  1381:     pub fn try_update(\n  1382:         &self,\n  1383:         set_order: Ordering,\n  1384:         fetch_order: Ordering,\n  1385:         mut f: impl FnMut(bool) -> Option<bool>,\n  1386:     ) -> Result<bool, bool> {\n  1387:         let mut prev = self.load(fetch_order);\n  1388:         while let Some(next) = f(prev) {\n  1389:             match self.compare_exchange_weak(prev, next, set_order, fetch_order) {\n  1390:                 x @ Ok(_) => return x,\n  1391:                 Err(next_prev) => prev = next_prev,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::update",
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
                                "primitive": "bool"
                              }
                            ],
                            "output": {
                              "primitive": "bool"
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
            "name": "impl FnMut(bool) -> bool"
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
                              "primitive": "bool"
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1436:     /// # Examples\n  1437:     ///\n  1438:     /// ```rust\n  1439:     ///\n  1440:     /// use std::sync::atomic::{AtomicBool, Ordering};\n  1441:     ///\n  1442:     /// let x = AtomicBool::new(false);\n  1443:     /// assert_eq!(x.update(Ordering::SeqCst, Ordering::SeqCst, |x| !x), false);\n  1444:     /// assert_eq!(x.update(Ordering::SeqCst, Ordering::SeqCst, |x| !x), true);\n  1445:     /// assert_eq!(x.load(Ordering::SeqCst), false);\n  1446:     /// ```\n  1447:     #[inline]\n  1448:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  1449:     #[cfg(target_has_atomic = \"8\")]\n  1450:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1451:     #[rustc_should_not_be_called_on_const_items]\n  1452:     pub fn update(\n  1453:         &self,\n  1454:         set_order: Ordering,\n  1455:         fetch_order: Ordering,\n  1456:         mut f: impl FnMut(bool) -> bool,\n  1457:     ) -> bool {\n  1458:         let mut prev = self.load(fetch_order);\n  1459:         loop {\n  1460:             match self.compare_exchange_weak(prev, f(prev), set_order, fetch_order) {\n  1461:                 Ok(x) => break x,\n  1462:                 Err(next_prev) => prev = next_prev,\n  1463:             }\n  1464:         }\n  1465:     }\n  1466: }\n  1467: \n  1468: #[cfg(target_has_atomic_load_store = \"ptr\")]",
    "nanvix_source": "  1434:     /// let x = AtomicBool::new(false);\n  1435:     /// assert_eq!(x.update(Ordering::SeqCst, Ordering::SeqCst, |x| !x), false);\n  1436:     /// assert_eq!(x.update(Ordering::SeqCst, Ordering::SeqCst, |x| !x), true);\n  1437:     /// assert_eq!(x.load(Ordering::SeqCst), false);\n  1438:     /// ```\n  1439:     #[inline]\n  1440:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  1441:     #[cfg(target_has_atomic = \"8\")]\n  1442:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1443:     #[rustc_should_not_be_called_on_const_items]\n  1444:     pub fn update(\n  1445:         &self,\n  1446:         set_order: Ordering,\n  1447:         fetch_order: Ordering,\n  1448:         mut f: impl FnMut(bool) -> bool,\n  1449:     ) -> bool {\n  1450:         let mut prev = self.load(fetch_order);\n  1451:         loop {\n  1452:             match self.compare_exchange_weak(prev, f(prev), set_order, fetch_order) {\n  1453:                 Ok(x) => break x,\n  1454:                 Err(next_prev) => prev = next_prev,",
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
