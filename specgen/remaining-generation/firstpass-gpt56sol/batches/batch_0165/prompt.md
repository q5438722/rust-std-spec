For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::rc::Rc::new_zeroed_slice",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "new_zeroed_slice",
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
                      "slice": {
                        "generic": "T"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3577",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "len",
            {
              "primitive": "usize"
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
                      "slice": {
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
                          "id": 431,
                          "path": "mem::MaybeUninit"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 302,
            "path": "Rc"
          }
        }
      }
    },
    "verification_source": "  1142:     ///\n  1143:     /// # Examples\n  1144:     ///\n  1145:     /// ```\n  1146:     /// use std::rc::Rc;\n  1147:     ///\n  1148:     /// let values = Rc::<[u32]>::new_zeroed_slice(3);\n  1149:     /// let values = unsafe { values.assume_init() };\n  1150:     ///\n  1151:     /// assert_eq!(*values, [0, 0, 0])\n  1152:     /// ```\n  1153:     ///\n  1154:     /// [zeroed]: mem::MaybeUninit::zeroed\n  1155:     #[cfg(not(no_global_oom_handling))]\n  1156:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n  1157:     #[must_use]\n  1158:     pub fn new_zeroed_slice(len: usize) -> Rc<[mem::MaybeUninit<T>]> {\n  1159:         unsafe {\n  1160:             Rc::from_ptr(Rc::allocate_for_layout(\n  1161:                 Layout::array::<T>(len).unwrap(),\n  1162:                 |layout| Global.allocate_zeroed(layout),\n  1163:                 |mem| {\n  1164:                     ptr::slice_from_raw_parts_mut(mem.cast::<T>(), len)\n  1165:                         as *mut RcInner<[mem::MaybeUninit<T>]>\n  1166:                 },\n  1167:             ))\n  1168:         }\n  1169:     }\n  1170: \n  1171:     /// Converts the reference-counted slice into a reference-counted array.\n  1172:     ///\n  1173:     /// This operation does not reallocate; the underlying array of the slice is simply reinterpreted as an array type.\n  1174:     ///",
    "nanvix_source": "  1148:     /// let values = Rc::<[u32]>::new_zeroed_slice(3);\n  1149:     /// let values = unsafe { values.assume_init() };\n  1150:     ///\n  1151:     /// assert_eq!(*values, [0, 0, 0])\n  1152:     /// ```\n  1153:     ///\n  1154:     /// [zeroed]: mem::MaybeUninit::zeroed\n  1155:     #[cfg(not(no_global_oom_handling))]\n  1156:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n  1157:     #[must_use]\n  1158:     pub fn new_zeroed_slice(len: usize) -> Rc<[mem::MaybeUninit<T>]> {\n  1159:         unsafe {\n  1160:             Rc::from_ptr(Rc::allocate_for_layout(\n  1161:                 Layout::array::<T>(len).unwrap(),\n  1162:                 |layout| Global.allocate_zeroed(layout),\n  1163:                 |mem| mem.cast::<T>().cast_slice(len) as *mut RcInner<[mem::MaybeUninit<T>]>,\n  1164:             ))\n  1165:         }\n  1166:     }\n  1167: }\n  1168: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::pin",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "pin",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3561",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "value",
            {
              "generic": "T"
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
                        "id": 302,
                        "path": "Rc"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 436,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "   631:     /// [zeroed]: mem::MaybeUninit::zeroed\n   632:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   633:     pub fn try_new_zeroed() -> Result<Rc<mem::MaybeUninit<T>>, AllocError> {\n   634:         unsafe {\n   635:             Ok(Rc::from_ptr(Rc::try_allocate_for_layout(\n   636:                 Layout::new::<T>(),\n   637:                 |layout| Global.allocate_zeroed(layout),\n   638:                 <*mut u8>::cast,\n   639:             )?))\n   640:         }\n   641:     }\n   642:     /// Constructs a new `Pin<Rc<T>>`. If `T` does not implement `Unpin`, then\n   643:     /// `value` will be pinned in memory and unable to be moved.\n   644:     #[cfg(not(no_global_oom_handling))]\n   645:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   646:     #[must_use]\n   647:     pub fn pin(value: T) -> Pin<Rc<T>> {\n   648:         unsafe { Pin::new_unchecked(Rc::new(value)) }\n   649:     }\n   650: \n   651:     /// Maps the value in an `Rc`, reusing the allocation if possible.\n   652:     ///\n   653:     /// `f` is called on a reference to the value in the `Rc`, and the result is returned, also in\n   654:     /// an `Rc`.\n   655:     ///\n   656:     /// Note: this is an associated function, which means that you have\n   657:     /// to call it as `Rc::map(r, f)` instead of `r.map(f)`. This\n   658:     /// is so that there is no conflict with a method on the inner type.\n   659:     ///\n   660:     /// # Examples\n   661:     ///\n   662:     /// ```\n   663:     /// #![feature(smart_pointer_try_map)]",
    "nanvix_source": "   637:                 |layout| Global.allocate_zeroed(layout),\n   638:                 <*mut u8>::cast,\n   639:             )?))\n   640:         }\n   641:     }\n   642:     /// Constructs a new `Pin<Rc<T>>`. If `T` does not implement `Unpin`, then\n   643:     /// `value` will be pinned in memory and unable to be moved.\n   644:     #[cfg(not(no_global_oom_handling))]\n   645:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   646:     #[must_use]\n   647:     pub fn pin(value: T) -> Pin<Rc<T>> {\n   648:         unsafe { Pin::new_unchecked(Rc::new(value)) }\n   649:     }\n   650: \n   651:     /// Maps the value in an `Rc`, reusing the allocation if possible.\n   652:     ///\n   653:     /// `f` is called on a reference to the value in the `Rc`, and the result is returned, also in\n   654:     /// an `Rc`.\n   655:     ///\n   656:     /// Note: this is an associated function, which means that you have\n   657:     /// to call it as `Rc::map(r, f)` instead of `r.map(f)`. This",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::ptr_eq",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "ptr_eq",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3610",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
            "other",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2003:     #[stable(feature = \"ptr_eq\", since = \"1.17.0\")]\n  2004:     /// Returns `true` if the two `Rc`s point to the same allocation in a vein similar to\n  2005:     /// [`ptr::eq`]. This function ignores the metadata of  `dyn Trait` pointers.\n  2006:     ///\n  2007:     /// # Examples\n  2008:     ///\n  2009:     /// ```\n  2010:     /// use std::rc::Rc;\n  2011:     ///\n  2012:     /// let five = Rc::new(5);\n  2013:     /// let same_five = Rc::clone(&five);\n  2014:     /// let other_five = Rc::new(5);\n  2015:     ///\n  2016:     /// assert!(Rc::ptr_eq(&five, &same_five));\n  2017:     /// assert!(!Rc::ptr_eq(&five, &other_five));\n  2018:     /// ```\n  2019:     pub fn ptr_eq(this: &Self, other: &Self) -> bool {\n  2020:         ptr::addr_eq(this.ptr.as_ptr(), other.ptr.as_ptr())\n  2021:     }\n  2022: }\n  2023: \n  2024: #[cfg(not(no_global_oom_handling))]\n  2025: impl<T: ?Sized + CloneToUninit, A: Allocator + Clone> Rc<T, A> {\n  2026:     /// Makes a mutable reference into the given `Rc`.\n  2027:     ///\n  2028:     /// If there are other `Rc` pointers to the same allocation, then `make_mut` will\n  2029:     /// [`clone`] the inner value to a new allocation to ensure unique ownership.  This is also\n  2030:     /// referred to as clone-on-write.\n  2031:     ///\n  2032:     /// However, if there are no other `Rc` pointers to this allocation, but some [`Weak`]\n  2033:     /// pointers, then the [`Weak`] pointers will be disassociated and the inner value will not\n  2034:     /// be cloned.\n  2035:     ///",
    "nanvix_source": "  2015:     /// ```\n  2016:     /// use std::rc::Rc;\n  2017:     ///\n  2018:     /// let five = Rc::new(5);\n  2019:     /// let same_five = Rc::clone(&five);\n  2020:     /// let other_five = Rc::new(5);\n  2021:     ///\n  2022:     /// assert!(Rc::ptr_eq(&five, &same_five));\n  2023:     /// assert!(!Rc::ptr_eq(&five, &other_five));\n  2024:     /// ```\n  2025:     pub fn ptr_eq(this: &Self, other: &Self) -> bool {\n  2026:         ptr::addr_eq(this.ptr.as_ptr(), other.ptr.as_ptr())\n  2027:     }\n  2028: }\n  2029: \n  2030: #[cfg(not(no_global_oom_handling))]\n  2031: impl<T: ?Sized + CloneToUninit, A: Allocator + Clone> Rc<T, A> {\n  2032:     /// Makes a mutable reference into the given `Rc`.\n  2033:     ///\n  2034:     /// If there are other `Rc` pointers to the same allocation, then `make_mut` will\n  2035:     /// [`clone`] the inner value to a new allocation to ensure unique ownership.  This is also",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::strong_count",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "strong_count",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3610",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1792:     }\n  1793: \n  1794:     /// Gets the number of strong (`Rc`) pointers to this allocation.\n  1795:     ///\n  1796:     /// # Examples\n  1797:     ///\n  1798:     /// ```\n  1799:     /// use std::rc::Rc;\n  1800:     ///\n  1801:     /// let five = Rc::new(5);\n  1802:     /// let _also_five = Rc::clone(&five);\n  1803:     ///\n  1804:     /// assert_eq!(2, Rc::strong_count(&five));\n  1805:     /// ```\n  1806:     #[inline]\n  1807:     #[stable(feature = \"rc_counts\", since = \"1.15.0\")]\n  1808:     pub fn strong_count(this: &Self) -> usize {\n  1809:         this.inner().strong()\n  1810:     }\n  1811: \n  1812:     /// Increments the strong reference count on the `Rc<T>` associated with the\n  1813:     /// provided pointer by one.\n  1814:     ///\n  1815:     /// # Safety\n  1816:     ///\n  1817:     /// The pointer must have been obtained through `Rc::into_raw` and must satisfy the\n  1818:     /// same layout requirements specified in [`Rc::from_raw_in`][from_raw_in].\n  1819:     /// The associated `Rc` instance must be valid (i.e. the strong count must be at\n  1820:     /// least 1) for the duration of this method, and `ptr` must point to a block of memory\n  1821:     /// allocated by `alloc`.\n  1822:     ///\n  1823:     /// [from_raw_in]: Rc::from_raw_in\n  1824:     ///",
    "nanvix_source": "  1804:     /// ```\n  1805:     /// use std::rc::Rc;\n  1806:     ///\n  1807:     /// let five = Rc::new(5);\n  1808:     /// let _also_five = Rc::clone(&five);\n  1809:     ///\n  1810:     /// assert_eq!(2, Rc::strong_count(&five));\n  1811:     /// ```\n  1812:     #[inline]\n  1813:     #[stable(feature = \"rc_counts\", since = \"1.15.0\")]\n  1814:     pub fn strong_count(this: &Self) -> usize {\n  1815:         this.inner().strong()\n  1816:     }\n  1817: \n  1818:     /// Increments the strong reference count on the `Rc<T>` associated with the\n  1819:     /// provided pointer by one.\n  1820:     ///\n  1821:     /// # Safety\n  1822:     ///\n  1823:     /// The pointer must have been obtained through `Rc::into_raw` and must satisfy the\n  1824:     /// same layout requirements specified in [`Rc::from_raw_in`][from_raw_in].",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::unwrap_or_clone",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "unwrap_or_clone",
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
            "id": 302,
            "path": "Rc"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:3613",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  2133:     /// let inner = Rc::unwrap_or_clone(rc);\n  2134:     /// // The inner value was not cloned\n  2135:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2136:     ///\n  2137:     /// let rc = Rc::new(inner);\n  2138:     /// let rc2 = rc.clone();\n  2139:     /// let inner = Rc::unwrap_or_clone(rc);\n  2140:     /// // Because there were 2 references, we had to clone the inner value.\n  2141:     /// assert!(!ptr::eq(ptr, inner.as_ptr()));\n  2142:     /// // `rc2` is the last reference, so when we unwrap it we get back\n  2143:     /// // the original `String`.\n  2144:     /// let inner = Rc::unwrap_or_clone(rc2);\n  2145:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2146:     /// ```\n  2147:     #[inline]\n  2148:     #[stable(feature = \"arc_unwrap_or_clone\", since = \"1.76.0\")]\n  2149:     pub fn unwrap_or_clone(this: Self) -> T {\n  2150:         Rc::try_unwrap(this).unwrap_or_else(|rc| (*rc).clone())\n  2151:     }\n  2152: }\n  2153: \n  2154: impl<A: Allocator> Rc<dyn Any, A> {\n  2155:     /// Attempts to downcast the `Rc<dyn Any>` to a concrete type.\n  2156:     ///\n  2157:     /// # Examples\n  2158:     ///\n  2159:     /// ```\n  2160:     /// use std::any::Any;\n  2161:     /// use std::rc::Rc;\n  2162:     ///\n  2163:     /// fn print_if_string(value: Rc<dyn Any>) {\n  2164:     ///     if let Ok(string) = value.downcast::<String>() {\n  2165:     ///         println!(\"String ({}): {}\", string.len(), string);",
    "nanvix_source": "  2145:     /// let inner = Rc::unwrap_or_clone(rc);\n  2146:     /// // Because there were 2 references, we had to clone the inner value.\n  2147:     /// assert!(!ptr::eq(ptr, inner.as_ptr()));\n  2148:     /// // `rc2` is the last reference, so when we unwrap it we get back\n  2149:     /// // the original `String`.\n  2150:     /// let inner = Rc::unwrap_or_clone(rc2);\n  2151:     /// assert!(ptr::eq(ptr, inner.as_ptr()));\n  2152:     /// ```\n  2153:     #[inline]\n  2154:     #[stable(feature = \"arc_unwrap_or_clone\", since = \"1.76.0\")]\n  2155:     pub fn unwrap_or_clone(this: Self) -> T {\n  2156:         Rc::try_unwrap(this).unwrap_or_else(|rc| (*rc).clone())\n  2157:     }\n  2158: }\n  2159: \n  2160: impl<A: Allocator> Rc<dyn Any, A> {\n  2161:     /// Attempts to downcast the `Rc<dyn Any>` to a concrete type.\n  2162:     ///\n  2163:     /// # Examples\n  2164:     ///\n  2165:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::weak_count",
    "generation_group": "ownership_or_uninitialized_model",
    "classification": "ownership_or_uninitialized_model",
    "classification_reasons": [
      "requires_linear_ownership_or_initialization_model"
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
        "is_unsafe": false
      },
      "name": "weak_count",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3610",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1774:     }\n  1775: \n  1776:     /// Gets the number of [`Weak`] pointers to this allocation.\n  1777:     ///\n  1778:     /// # Examples\n  1779:     ///\n  1780:     /// ```\n  1781:     /// use std::rc::Rc;\n  1782:     ///\n  1783:     /// let five = Rc::new(5);\n  1784:     /// let _weak_five = Rc::downgrade(&five);\n  1785:     ///\n  1786:     /// assert_eq!(1, Rc::weak_count(&five));\n  1787:     /// ```\n  1788:     #[inline]\n  1789:     #[stable(feature = \"rc_counts\", since = \"1.15.0\")]\n  1790:     pub fn weak_count(this: &Self) -> usize {\n  1791:         this.inner().weak() - 1\n  1792:     }\n  1793: \n  1794:     /// Gets the number of strong (`Rc`) pointers to this allocation.\n  1795:     ///\n  1796:     /// # Examples\n  1797:     ///\n  1798:     /// ```\n  1799:     /// use std::rc::Rc;\n  1800:     ///\n  1801:     /// let five = Rc::new(5);\n  1802:     /// let _also_five = Rc::clone(&five);\n  1803:     ///\n  1804:     /// assert_eq!(2, Rc::strong_count(&five));\n  1805:     /// ```\n  1806:     #[inline]",
    "nanvix_source": "  1786:     /// ```\n  1787:     /// use std::rc::Rc;\n  1788:     ///\n  1789:     /// let five = Rc::new(5);\n  1790:     /// let _weak_five = Rc::downgrade(&five);\n  1791:     ///\n  1792:     /// assert_eq!(1, Rc::weak_count(&five));\n  1793:     /// ```\n  1794:     #[inline]\n  1795:     #[stable(feature = \"rc_counts\", since = \"1.15.0\")]\n  1796:     pub fn weak_count(this: &Self) -> usize {\n  1797:         this.inner().weak() - 1\n  1798:     }\n  1799: \n  1800:     /// Gets the number of strong (`Rc`) pointers to this allocation.\n  1801:     ///\n  1802:     /// # Examples\n  1803:     ///\n  1804:     /// ```\n  1805:     /// use std::rc::Rc;\n  1806:     ///",
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
