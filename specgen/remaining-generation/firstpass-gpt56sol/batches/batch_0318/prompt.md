For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::sync::Arc::from_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "from_raw",
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4409",
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1636:     ///\n  1637:     /// Convert a slice back into its original array:\n  1638:     ///\n  1639:     /// ```\n  1640:     /// use std::sync::Arc;\n  1641:     ///\n  1642:     /// let x: Arc<[u32]> = Arc::new([1, 2, 3]);\n  1643:     /// let x_ptr: *const [u32] = Arc::into_raw(x);\n  1644:     ///\n  1645:     /// unsafe {\n  1646:     ///     let x: Arc<[u32; 3]> = Arc::from_raw(x_ptr.cast::<[u32; 3]>());\n  1647:     ///     assert_eq!(&*x, &[1, 2, 3]);\n  1648:     /// }\n  1649:     /// ```\n  1650:     #[inline]\n  1651:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1652:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  1653:         unsafe { Arc::from_raw_in(ptr, Global) }\n  1654:     }\n  1655: \n  1656:     /// Consumes the `Arc`, returning the wrapped pointer.\n  1657:     ///\n  1658:     /// To avoid a memory leak the pointer must be converted back to an `Arc` using\n  1659:     /// [`Arc::from_raw`].\n  1660:     ///\n  1661:     /// # Examples\n  1662:     ///\n  1663:     /// ```\n  1664:     /// use std::sync::Arc;\n  1665:     ///\n  1666:     /// let x = Arc::new(\"hello\".to_owned());\n  1667:     /// let x_ptr = Arc::into_raw(x);\n  1668:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");",
    "nanvix_source": "  1654:     /// let x: Arc<[u32]> = Arc::new([1, 2, 3]);\n  1655:     /// let x_ptr: *const [u32] = Arc::into_raw(x);\n  1656:     ///\n  1657:     /// unsafe {\n  1658:     ///     let x: Arc<[u32; 3]> = Arc::from_raw(x_ptr.cast::<[u32; 3]>());\n  1659:     ///     assert_eq!(&*x, &[1, 2, 3]);\n  1660:     /// }\n  1661:     /// ```\n  1662:     #[inline]\n  1663:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1664:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  1665:         unsafe { Arc::from_raw_in(ptr, Global) }\n  1666:     }\n  1667: \n  1668:     /// Consumes the `Arc`, returning the wrapped pointer.\n  1669:     ///\n  1670:     /// To avoid a memory leak the pointer must be converted back to an `Arc` using\n  1671:     /// [`Arc::from_raw`].\n  1672:     ///\n  1673:     /// # Examples\n  1674:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::increment_strong_count",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
        "is_unsafe": true
      },
      "name": "increment_strong_count",
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
                      "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4409",
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
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1698:     /// let five = Arc::new(5);\n  1699:     ///\n  1700:     /// unsafe {\n  1701:     ///     let ptr = Arc::into_raw(five);\n  1702:     ///     Arc::increment_strong_count(ptr);\n  1703:     ///\n  1704:     ///     // This assertion is deterministic because we haven't shared\n  1705:     ///     // the `Arc` between threads.\n  1706:     ///     let five = Arc::from_raw(ptr);\n  1707:     ///     assert_eq!(2, Arc::strong_count(&five));\n  1708:     /// #   // Prevent leaks for Miri.\n  1709:     /// #   Arc::decrement_strong_count(ptr);\n  1710:     /// }\n  1711:     /// ```\n  1712:     #[inline]\n  1713:     #[stable(feature = \"arc_mutate_strong_count\", since = \"1.51.0\")]\n  1714:     pub unsafe fn increment_strong_count(ptr: *const T) {\n  1715:         unsafe { Arc::increment_strong_count_in(ptr, Global) }\n  1716:     }\n  1717: \n  1718:     /// Decrements the strong reference count on the `Arc<T>` associated with the\n  1719:     /// provided pointer by one.\n  1720:     ///\n  1721:     /// # Safety\n  1722:     ///\n  1723:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the\n  1724:     /// same layout requirements specified in [`Arc::from_raw_in`][from_raw_in].\n  1725:     /// The associated `Arc` instance must be valid (i.e. the strong count must be at\n  1726:     /// least 1) when invoking this method, and `ptr` must point to a block of memory\n  1727:     /// allocated by the global allocator. This method can be used to release the final\n  1728:     /// `Arc` and backing storage, but **should not** be called after the final `Arc` has been\n  1729:     /// released.\n  1730:     ///",
    "nanvix_source": "  1716:     ///     // This assertion is deterministic because we haven't shared\n  1717:     ///     // the `Arc` between threads.\n  1718:     ///     let five = Arc::from_raw(ptr);\n  1719:     ///     assert_eq!(2, Arc::strong_count(&five));\n  1720:     /// #   // Prevent leaks for Miri.\n  1721:     /// #   Arc::decrement_strong_count(ptr);\n  1722:     /// }\n  1723:     /// ```\n  1724:     #[inline]\n  1725:     #[stable(feature = \"arc_mutate_strong_count\", since = \"1.51.0\")]\n  1726:     pub unsafe fn increment_strong_count(ptr: *const T) {\n  1727:         unsafe { Arc::increment_strong_count_in(ptr, Global) }\n  1728:     }\n  1729: \n  1730:     /// Decrements the strong reference count on the `Arc<T>` associated with the\n  1731:     /// provided pointer by one.\n  1732:     ///\n  1733:     /// # Safety\n  1734:     ///\n  1735:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the\n  1736:     /// same layout requirements specified in [`Arc::from_raw_in`][from_raw_in].",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::into_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "into_raw",
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
                      "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4409",
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1659:     /// [`Arc::from_raw`].\n  1660:     ///\n  1661:     /// # Examples\n  1662:     ///\n  1663:     /// ```\n  1664:     /// use std::sync::Arc;\n  1665:     ///\n  1666:     /// let x = Arc::new(\"hello\".to_owned());\n  1667:     /// let x_ptr = Arc::into_raw(x);\n  1668:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1669:     /// # // Prevent leaks for Miri.\n  1670:     /// # drop(unsafe { Arc::from_raw(x_ptr) });\n  1671:     /// ```\n  1672:     #[must_use = \"losing the pointer will leak memory\"]\n  1673:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1674:     #[rustc_never_returns_null_ptr]\n  1675:     pub fn into_raw(this: Self) -> *const T {\n  1676:         let this = ManuallyDrop::new(this);\n  1677:         Self::as_ptr(&*this)\n  1678:     }\n  1679: \n  1680:     /// Increments the strong reference count on the `Arc<T>` associated with the\n  1681:     /// provided pointer by one.\n  1682:     ///\n  1683:     /// # Safety\n  1684:     ///\n  1685:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the\n  1686:     /// same layout requirements specified in [`Arc::from_raw_in`][from_raw_in].\n  1687:     /// The associated `Arc` instance must be valid (i.e. the strong count must be at\n  1688:     /// least 1) for the duration of this method, and `ptr` must point to a block of memory\n  1689:     /// allocated by the global allocator.\n  1690:     ///\n  1691:     /// [from_raw_in]: Arc::from_raw_in",
    "nanvix_source": "  1677:     ///\n  1678:     /// let x = Arc::new(\"hello\".to_owned());\n  1679:     /// let x_ptr = Arc::into_raw(x);\n  1680:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");\n  1681:     /// # // Prevent leaks for Miri.\n  1682:     /// # drop(unsafe { Arc::from_raw(x_ptr) });\n  1683:     /// ```\n  1684:     #[must_use = \"losing the pointer will leak memory\"]\n  1685:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1686:     #[rustc_never_returns_null_ptr]\n  1687:     pub fn into_raw(this: Self) -> *const T {\n  1688:         let this = ManuallyDrop::new(this);\n  1689:         Self::as_ptr(&*this)\n  1690:     }\n  1691: \n  1692:     /// Increments the strong reference count on the `Arc<T>` associated with the\n  1693:     /// provided pointer by one.\n  1694:     ///\n  1695:     /// # Safety\n  1696:     ///\n  1697:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
            "id": 4358,
            "path": "Weak"
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
        "impl_id": "alloc:4551",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  3097:     /// let strong = Arc::new(\"hello\".to_owned());\n  3098:     /// let weak = Arc::downgrade(&strong);\n  3099:     /// // Both point to the same object\n  3100:     /// assert!(ptr::eq(&*strong, weak.as_ptr()));\n  3101:     /// // The strong here keeps it alive, so we can still access the object.\n  3102:     /// assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3103:     ///\n  3104:     /// drop(strong);\n  3105:     /// // But not any more. We can do weak.as_ptr(), but accessing the pointer would lead to\n  3106:     /// // undefined behavior.\n  3107:     /// // assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3108:     /// ```\n  3109:     ///\n  3110:     /// [`null`]: core::ptr::null \"ptr::null\"\n  3111:     #[must_use]\n  3112:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3113:     pub fn as_ptr(&self) -> *const T {\n  3114:         let ptr: *mut ArcInner<T> = NonNull::as_ptr(self.ptr);\n  3115: \n  3116:         if is_dangling(ptr) {\n  3117:             // If the pointer is dangling, we return the sentinel directly. This cannot be\n  3118:             // a valid payload address, as the payload is at least as aligned as ArcInner (usize).\n  3119:             ptr as *const T\n  3120:         } else {\n  3121:             // SAFETY: if is_dangling returns false, then the pointer is dereferenceable.\n  3122:             // The payload may be dropped at this point, and we have to maintain provenance,\n  3123:             // so use raw pointer manipulation.\n  3124:             unsafe { &raw mut (*ptr).data }\n  3125:         }\n  3126:     }\n  3127: \n  3128:     /// Consumes the `Weak<T>`, returning the wrapped pointer and allocator.\n  3129:     ///",
    "nanvix_source": "  3118:     ///\n  3119:     /// drop(strong);\n  3120:     /// // But not any more. We can do weak.as_ptr(), but accessing the pointer would lead to\n  3121:     /// // undefined behavior.\n  3122:     /// // assert_eq!(\"hello\", unsafe { &*weak.as_ptr() });\n  3123:     /// ```\n  3124:     ///\n  3125:     /// [`null`]: core::ptr::null \"ptr::null\"\n  3126:     #[must_use]\n  3127:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3128:     pub fn as_ptr(&self) -> *const T {\n  3129:         let ptr: *mut ArcInner<T> = NonNull::as_ptr(self.ptr);\n  3130: \n  3131:         if is_dangling(ptr) {\n  3132:             // If the pointer is dangling, we return the sentinel directly. This cannot be\n  3133:             // a valid payload address, as the payload is at least as aligned as ArcInner (usize).\n  3134:             ptr as *const T\n  3135:         } else {\n  3136:             // SAFETY: if is_dangling returns false, then the pointer is dereferenceable.\n  3137:             // The payload may be dropped at this point, and we have to maintain provenance,\n  3138:             // so use raw pointer manipulation.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::from_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "from_raw",
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
            "id": 4358,
            "path": "Weak"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4547",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  3024:     /// assert_eq!(2, Arc::weak_count(&strong));\n  3025:     ///\n  3026:     /// assert_eq!(\"hello\", &*unsafe { Weak::from_raw(raw_1) }.upgrade().unwrap());\n  3027:     /// assert_eq!(1, Arc::weak_count(&strong));\n  3028:     ///\n  3029:     /// drop(strong);\n  3030:     ///\n  3031:     /// // Decrement the last weak count.\n  3032:     /// assert!(unsafe { Weak::from_raw(raw_2) }.upgrade().is_none());\n  3033:     /// ```\n  3034:     ///\n  3035:     /// [`new`]: Weak::new\n  3036:     /// [`into_raw`]: Weak::into_raw\n  3037:     /// [`upgrade`]: Weak::upgrade\n  3038:     #[inline]\n  3039:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3040:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  3041:         unsafe { Weak::from_raw_in(ptr, Global) }\n  3042:     }\n  3043: \n  3044:     /// Consumes the `Weak<T>` and turns it into a raw pointer.\n  3045:     ///\n  3046:     /// This converts the weak pointer into a raw pointer, while still preserving the ownership of\n  3047:     /// one weak reference (the weak count is not modified by this operation). It can be turned\n  3048:     /// back into the `Weak<T>` with [`from_raw`].\n  3049:     ///\n  3050:     /// The same restrictions of accessing the target of the pointer as with\n  3051:     /// [`as_ptr`] apply.\n  3052:     ///\n  3053:     /// # Examples\n  3054:     ///\n  3055:     /// ```\n  3056:     /// use std::sync::{Arc, Weak};",
    "nanvix_source": "  3045:     ///\n  3046:     /// // Decrement the last weak count.\n  3047:     /// assert!(unsafe { Weak::from_raw(raw_2) }.upgrade().is_none());\n  3048:     /// ```\n  3049:     ///\n  3050:     /// [`new`]: Weak::new\n  3051:     /// [`into_raw`]: Weak::into_raw\n  3052:     /// [`upgrade`]: Weak::upgrade\n  3053:     #[inline]\n  3054:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3055:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  3056:         unsafe { Weak::from_raw_in(ptr, Global) }\n  3057:     }\n  3058: \n  3059:     /// Consumes the `Weak<T>` and turns it into a raw pointer.\n  3060:     ///\n  3061:     /// This converts the weak pointer into a raw pointer, while still preserving the ownership of\n  3062:     /// one weak reference (the weak count is not modified by this operation). It can be turned\n  3063:     /// back into the `Weak<T>` with [`from_raw`].\n  3064:     ///\n  3065:     /// The same restrictions of accessing the target of the pointer as with",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Weak::into_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "into_raw",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4358,
            "path": "Weak"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4547",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4358",
        "resolved_owner_path": [
          "alloc",
          "sync",
          "Weak"
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
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  3057:     ///\n  3058:     /// let strong = Arc::new(\"hello\".to_owned());\n  3059:     /// let weak = Arc::downgrade(&strong);\n  3060:     /// let raw = weak.into_raw();\n  3061:     ///\n  3062:     /// assert_eq!(1, Arc::weak_count(&strong));\n  3063:     /// assert_eq!(\"hello\", unsafe { &*raw });\n  3064:     ///\n  3065:     /// drop(unsafe { Weak::from_raw(raw) });\n  3066:     /// assert_eq!(0, Arc::weak_count(&strong));\n  3067:     /// ```\n  3068:     ///\n  3069:     /// [`from_raw`]: Weak::from_raw\n  3070:     /// [`as_ptr`]: Weak::as_ptr\n  3071:     #[must_use = \"losing the pointer will leak memory\"]\n  3072:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3073:     pub fn into_raw(self) -> *const T {\n  3074:         ManuallyDrop::new(self).as_ptr()\n  3075:     }\n  3076: }\n  3077: \n  3078: impl<T: ?Sized, A: Allocator> Weak<T, A> {\n  3079:     /// Returns a reference to the underlying allocator.\n  3080:     #[inline]\n  3081:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  3082:     pub fn allocator(&self) -> &A {\n  3083:         &self.alloc\n  3084:     }\n  3085: \n  3086:     /// Returns a raw pointer to the object `T` pointed to by this `Weak<T>`.\n  3087:     ///\n  3088:     /// The pointer is valid only if there are some strong references. The pointer may be dangling,\n  3089:     /// unaligned or even [`null`] otherwise.",
    "nanvix_source": "  3078:     /// assert_eq!(\"hello\", unsafe { &*raw });\n  3079:     ///\n  3080:     /// drop(unsafe { Weak::from_raw(raw) });\n  3081:     /// assert_eq!(0, Arc::weak_count(&strong));\n  3082:     /// ```\n  3083:     ///\n  3084:     /// [`from_raw`]: Weak::from_raw\n  3085:     /// [`as_ptr`]: Weak::as_ptr\n  3086:     #[must_use = \"losing the pointer will leak memory\"]\n  3087:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  3088:     pub fn into_raw(self) -> *const T {\n  3089:         ManuallyDrop::new(self).as_ptr()\n  3090:     }\n  3091: }\n  3092: \n  3093: impl<T: ?Sized, A: Allocator> Weak<T, A> {\n  3094:     /// Returns a reference to the underlying allocator.\n  3095:     #[inline]\n  3096:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  3097:     pub fn allocator(&self) -> &A {\n  3098:         &self.alloc",
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
