For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicPtr::into_inner",
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
      "name": "into_inner",
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
              "generic": "Self"
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
    "verification_source": "  1686:     ///\n  1687:     /// This is safe because passing `self` by value guarantees that no other threads are\n  1688:     /// concurrently accessing the atomic data.\n  1689:     ///\n  1690:     /// # Examples\n  1691:     ///\n  1692:     /// ```\n  1693:     /// use std::sync::atomic::AtomicPtr;\n  1694:     ///\n  1695:     /// let mut data = 5;\n  1696:     /// let atomic_ptr = AtomicPtr::new(&mut data);\n  1697:     /// assert_eq!(unsafe { *atomic_ptr.into_inner() }, 5);\n  1698:     /// ```\n  1699:     #[inline]\n  1700:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n  1701:     #[rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\")]\n  1702:     pub const fn into_inner(self) -> *mut T {\n  1703:         // SAFETY:\n  1704:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1705:         unsafe { transmute(self) }\n  1706:     }\n  1707: \n  1708:     /// Loads a value from the pointer.\n  1709:     ///\n  1710:     /// `load` takes an [`Ordering`] argument which describes the memory ordering\n  1711:     /// of this operation. Possible values are [`SeqCst`], [`Acquire`] and [`Relaxed`].\n  1712:     ///\n  1713:     /// # Panics\n  1714:     ///\n  1715:     /// Panics if `order` is [`Release`] or [`AcqRel`].\n  1716:     ///\n  1717:     /// # Examples\n  1718:     ///",
    "nanvix_source": "  1681:     /// ```\n  1682:     /// use std::sync::atomic::AtomicPtr;\n  1683:     ///\n  1684:     /// let mut data = 5;\n  1685:     /// let atomic_ptr = AtomicPtr::new(&mut data);\n  1686:     /// assert_eq!(unsafe { *atomic_ptr.into_inner() }, 5);\n  1687:     /// ```\n  1688:     #[inline]\n  1689:     #[stable(feature = \"atomic_access\", since = \"1.15.0\")]\n  1690:     #[rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\")]\n  1691:     pub const fn into_inner(self) -> *mut T {\n  1692:         // SAFETY:\n  1693:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1694:         unsafe { transmute(self) }\n  1695:     }\n  1696: \n  1697:     /// Loads a value from the pointer.\n  1698:     ///\n  1699:     /// `load` takes an [`Ordering`] argument which describes the memory ordering\n  1700:     /// of this operation. Possible values are [`SeqCst`], [`Acquire`] and [`Relaxed`].\n  1701:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::load",
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
    "target": "core::sync::atomic::AtomicPtr::new",
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
            "p",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9623,
            "path": "AtomicPtr"
          }
        }
      }
    },
    "verification_source": "  1467: \n  1468: #[cfg(target_has_atomic_load_store = \"ptr\")]\n  1469: impl<T> AtomicPtr<T> {\n  1470:     /// Creates a new `AtomicPtr`.\n  1471:     ///\n  1472:     /// # Examples\n  1473:     ///\n  1474:     /// ```\n  1475:     /// use std::sync::atomic::AtomicPtr;\n  1476:     ///\n  1477:     /// let ptr = &mut 5;\n  1478:     /// let atomic_ptr = AtomicPtr::new(ptr);\n  1479:     /// ```\n  1480:     #[inline]\n  1481:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1482:     #[rustc_const_stable(feature = \"const_atomic_new\", since = \"1.24.0\")]\n  1483:     pub const fn new(p: *mut T) -> AtomicPtr<T> {\n  1484:         // SAFETY:\n  1485:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1486:         unsafe { transmute(p) }\n  1487:     }\n  1488: \n  1489:     /// Creates a new `AtomicPtr` from a pointer.\n  1490:     ///\n  1491:     /// # Examples\n  1492:     ///\n  1493:     /// ```\n  1494:     /// use std::sync::atomic::{self, AtomicPtr};\n  1495:     ///\n  1496:     /// // Get a pointer to an allocated value\n  1497:     /// let ptr: *mut *mut u8 = Box::into_raw(Box::new(std::ptr::null_mut()));\n  1498:     ///\n  1499:     /// assert!(ptr.cast::<AtomicPtr<u8>>().is_aligned());",
    "nanvix_source": "  1465:     ///\n  1466:     /// ```\n  1467:     /// use std::sync::atomic::AtomicPtr;\n  1468:     ///\n  1469:     /// let ptr = &mut 5;\n  1470:     /// let atomic_ptr = AtomicPtr::new(ptr);\n  1471:     /// ```\n  1472:     #[inline]\n  1473:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1474:     #[rustc_const_stable(feature = \"const_atomic_new\", since = \"1.24.0\")]\n  1475:     pub const fn new(p: *mut T) -> AtomicPtr<T> {\n  1476:         // SAFETY:\n  1477:         // `Atomic<T>` is essentially a transparent wrapper around `T`.\n  1478:         unsafe { transmute(p) }\n  1479:     }\n  1480: \n  1481:     /// Creates a new `AtomicPtr` from a pointer.\n  1482:     ///\n  1483:     /// # Examples\n  1484:     ///\n  1485:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicPtr::store",
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
    "target": "core::sync::atomic::AtomicPtr::swap",
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
    "target": "core::sync::atomic::AtomicPtr::try_update",
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
            "name": "impl FnMut(*mut T) -> Option<*mut T>"
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
                      "raw_pointer": {
                        "is_mutable": true,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2058:     /// assert_eq!(some_ptr.try_update(Ordering::SeqCst, Ordering::SeqCst, |_| None), Err(ptr));\n  2059:     /// let result = some_ptr.try_update(Ordering::SeqCst, Ordering::SeqCst, |x| {\n  2060:     ///     if x == ptr {\n  2061:     ///         Some(new)\n  2062:     ///     } else {\n  2063:     ///         None\n  2064:     ///     }\n  2065:     /// });\n  2066:     /// assert_eq!(result, Ok(ptr));\n  2067:     /// assert_eq!(some_ptr.load(Ordering::SeqCst), new);\n  2068:     /// ```\n  2069:     #[inline]\n  2070:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  2071:     #[cfg(target_has_atomic = \"ptr\")]\n  2072:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2073:     #[rustc_should_not_be_called_on_const_items]\n  2074:     pub fn try_update(\n  2075:         &self,\n  2076:         set_order: Ordering,\n  2077:         fetch_order: Ordering,\n  2078:         mut f: impl FnMut(*mut T) -> Option<*mut T>,\n  2079:     ) -> Result<*mut T, *mut T> {\n  2080:         let mut prev = self.load(fetch_order);\n  2081:         while let Some(next) = f(prev) {\n  2082:             match self.compare_exchange_weak(prev, next, set_order, fetch_order) {\n  2083:                 x @ Ok(_) => return x,\n  2084:                 Err(next_prev) => prev = next_prev,\n  2085:             }\n  2086:         }\n  2087:         Err(prev)\n  2088:     }\n  2089: \n  2090:     /// Fetches the value, applies a function to it that it return a new value.",
    "nanvix_source": "  2053:     ///     }\n  2054:     /// });\n  2055:     /// assert_eq!(result, Ok(ptr));\n  2056:     /// assert_eq!(some_ptr.load(Ordering::SeqCst), new);\n  2057:     /// ```\n  2058:     #[inline]\n  2059:     #[stable(feature = \"atomic_try_update\", since = \"1.95.0\")]\n  2060:     #[cfg(target_has_atomic = \"ptr\")]\n  2061:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2062:     #[rustc_should_not_be_called_on_const_items]\n  2063:     pub fn try_update(\n  2064:         &self,\n  2065:         set_order: Ordering,\n  2066:         fetch_order: Ordering,\n  2067:         mut f: impl FnMut(*mut T) -> Option<*mut T>,\n  2068:     ) -> Result<*mut T, *mut T> {\n  2069:         let mut prev = self.load(fetch_order);\n  2070:         while let Some(next) = f(prev) {\n  2071:             match self.compare_exchange_weak(prev, next, set_order, fetch_order) {\n  2072:                 x @ Ok(_) => return x,\n  2073:                 Err(next_prev) => prev = next_prev,",
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
