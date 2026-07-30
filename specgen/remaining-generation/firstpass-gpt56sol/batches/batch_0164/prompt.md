For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::rc::Rc::downcast",
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
                        "id": 56,
                        "path": "Any"
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "downcast",
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
                      "dyn_trait": {
                        "lifetime": null,
                        "traits": [
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 56,
                              "path": "Any"
                            }
                          }
                        ]
                      }
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
        "impl_id": "alloc:3616",
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
            "self",
            {
              "generic": "Self"
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
                    }
                  },
                  {
                    "type": {
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2159:     /// ```\n  2160:     /// use std::any::Any;\n  2161:     /// use std::rc::Rc;\n  2162:     ///\n  2163:     /// fn print_if_string(value: Rc<dyn Any>) {\n  2164:     ///     if let Ok(string) = value.downcast::<String>() {\n  2165:     ///         println!(\"String ({}): {}\", string.len(), string);\n  2166:     ///     }\n  2167:     /// }\n  2168:     ///\n  2169:     /// let my_string = \"Hello World\".to_string();\n  2170:     /// print_if_string(Rc::new(my_string));\n  2171:     /// print_if_string(Rc::new(0i8));\n  2172:     /// ```\n  2173:     #[inline]\n  2174:     #[stable(feature = \"rc_downcast\", since = \"1.29.0\")]\n  2175:     pub fn downcast<T: Any>(self) -> Result<Rc<T, A>, Self> {\n  2176:         if (*self).is::<T>() {\n  2177:             unsafe {\n  2178:                 let (ptr, alloc) = Rc::into_inner_with_allocator(self);\n  2179:                 Ok(Rc::from_inner_in(ptr.cast(), alloc))\n  2180:             }\n  2181:         } else {\n  2182:             Err(self)\n  2183:         }\n  2184:     }\n  2185: \n  2186:     /// Downcasts the `Rc<dyn Any>` to a concrete type.\n  2187:     ///\n  2188:     /// For a safe alternative see [`downcast`].\n  2189:     ///\n  2190:     /// # Examples\n  2191:     ///",
    "nanvix_source": "  2171:     ///         println!(\"String ({}): {}\", string.len(), string);\n  2172:     ///     }\n  2173:     /// }\n  2174:     ///\n  2175:     /// let my_string = \"Hello World\".to_string();\n  2176:     /// print_if_string(Rc::new(my_string));\n  2177:     /// print_if_string(Rc::new(0i8));\n  2178:     /// ```\n  2179:     #[inline]\n  2180:     #[stable(feature = \"rc_downcast\", since = \"1.29.0\")]\n  2181:     pub fn downcast<T: Any>(self) -> Result<Rc<T, A>, Self> {\n  2182:         if (*self).is::<T>() {\n  2183:             unsafe {\n  2184:                 let (ptr, alloc) = Rc::into_inner_with_allocator(self);\n  2185:                 Ok(Rc::from_inner_in(ptr.cast(), alloc))\n  2186:             }\n  2187:         } else {\n  2188:             Err(self)\n  2189:         }\n  2190:     }\n  2191: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::downgrade",
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
        "where_predicates": [
          {
            "bound_predicate": {
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
              "generic_params": [],
              "type": {
                "generic": "A"
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
      "name": "downgrade",
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
            "id": 3551,
            "path": "Weak"
          }
        }
      }
    },
    "verification_source": "  1750:     }\n  1751: \n  1752:     /// Creates a new [`Weak`] pointer to this allocation.\n  1753:     ///\n  1754:     /// # Examples\n  1755:     ///\n  1756:     /// ```\n  1757:     /// use std::rc::Rc;\n  1758:     ///\n  1759:     /// let five = Rc::new(5);\n  1760:     ///\n  1761:     /// let weak_five = Rc::downgrade(&five);\n  1762:     /// ```\n  1763:     #[must_use = \"this returns a new `Weak` pointer, \\\n  1764:                   without modifying the original `Rc`\"]\n  1765:     #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  1766:     pub fn downgrade(this: &Self) -> Weak<T, A>\n  1767:     where\n  1768:         A: Clone,\n  1769:     {\n  1770:         this.inner().inc_weak();\n  1771:         // Make sure we do not create a dangling Weak\n  1772:         debug_assert!(!is_dangling(this.ptr.as_ptr()));\n  1773:         Weak { ptr: this.ptr, alloc: this.alloc.clone() }\n  1774:     }\n  1775: \n  1776:     /// Gets the number of [`Weak`] pointers to this allocation.\n  1777:     ///\n  1778:     /// # Examples\n  1779:     ///\n  1780:     /// ```\n  1781:     /// use std::rc::Rc;\n  1782:     ///",
    "nanvix_source": "  1762:     /// ```\n  1763:     /// use std::rc::Rc;\n  1764:     ///\n  1765:     /// let five = Rc::new(5);\n  1766:     ///\n  1767:     /// let weak_five = Rc::downgrade(&five);\n  1768:     /// ```\n  1769:     #[must_use = \"this returns a new `Weak` pointer, \\\n  1770:                   without modifying the original `Rc`\"]\n  1771:     #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  1772:     pub fn downgrade(this: &Self) -> Weak<T, A>\n  1773:     where\n  1774:         A: Clone,\n  1775:     {\n  1776:         this.inner().inc_weak();\n  1777:         // Make sure we do not create a dangling Weak\n  1778:         debug_assert!(!is_dangling(this.ptr.as_ptr()));\n  1779:         Weak { ptr: this.ptr, alloc: this.alloc.clone() }\n  1780:     }\n  1781: \n  1782:     /// Gets the number of [`Weak`] pointers to this allocation.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::new_cyclic",
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
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
                                    "id": 3551,
                                    "path": "Weak"
                                  }
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 441,
                      "path": "FnOnce"
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
      "name": "new_cyclic",
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
            "data_fn",
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
    },
    "verification_source": "   469:     ///         // `Rc` we're constructing.\n   470:     ///         Rc::new_cyclic(|me| {\n   471:     ///             // Create the actual struct here.\n   472:     ///             Gadget { me: me.clone() }\n   473:     ///         })\n   474:     ///     }\n   475:     ///\n   476:     ///     /// Returns a reference counted pointer to Self.\n   477:     ///     fn me(&self) -> Rc<Self> {\n   478:     ///         self.me.upgrade().unwrap()\n   479:     ///     }\n   480:     /// }\n   481:     /// ```\n   482:     /// [`upgrade`]: Weak::upgrade\n   483:     #[cfg(not(no_global_oom_handling))]\n   484:     #[stable(feature = \"arc_new_cyclic\", since = \"1.60.0\")]\n   485:     pub fn new_cyclic<F>(data_fn: F) -> Rc<T>\n   486:     where\n   487:         F: FnOnce(&Weak<T>) -> T,\n   488:     {\n   489:         Self::new_cyclic_in(data_fn, Global)\n   490:     }\n   491: \n   492:     /// Constructs a new `Rc` with uninitialized contents.\n   493:     ///\n   494:     /// # Examples\n   495:     ///\n   496:     /// ```\n   497:     /// use std::rc::Rc;\n   498:     ///\n   499:     /// let mut five = Rc::<u32>::new_uninit();\n   500:     ///\n   501:     /// // Deferred initialization:",
    "nanvix_source": "   475:     ///\n   476:     ///     /// Returns a reference counted pointer to Self.\n   477:     ///     fn me(&self) -> Rc<Self> {\n   478:     ///         self.me.upgrade().unwrap()\n   479:     ///     }\n   480:     /// }\n   481:     /// ```\n   482:     /// [`upgrade`]: Weak::upgrade\n   483:     #[cfg(not(no_global_oom_handling))]\n   484:     #[stable(feature = \"arc_new_cyclic\", since = \"1.60.0\")]\n   485:     pub fn new_cyclic<F>(data_fn: F) -> Rc<T>\n   486:     where\n   487:         F: FnOnce(&Weak<T>) -> T,\n   488:     {\n   489:         Self::new_cyclic_in(data_fn, Global)\n   490:     }\n   491: \n   492:     /// Constructs a new `Rc` with uninitialized contents.\n   493:     ///\n   494:     /// # Examples\n   495:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::new_uninit",
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
      "name": "new_uninit",
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
        "inputs": [],
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
                        "id": 431,
                        "path": "mem::MaybeUninit"
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
    "verification_source": "   495:     ///\n   496:     /// ```\n   497:     /// use std::rc::Rc;\n   498:     ///\n   499:     /// let mut five = Rc::<u32>::new_uninit();\n   500:     ///\n   501:     /// // Deferred initialization:\n   502:     /// Rc::get_mut(&mut five).unwrap().write(5);\n   503:     ///\n   504:     /// let five = unsafe { five.assume_init() };\n   505:     ///\n   506:     /// assert_eq!(*five, 5)\n   507:     /// ```\n   508:     #[cfg(not(no_global_oom_handling))]\n   509:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   510:     #[must_use]\n   511:     pub fn new_uninit() -> Rc<mem::MaybeUninit<T>> {\n   512:         unsafe {\n   513:             Rc::from_ptr(Rc::allocate_for_layout(\n   514:                 Layout::new::<T>(),\n   515:                 |layout| Global.allocate(layout),\n   516:                 <*mut u8>::cast,\n   517:             ))\n   518:         }\n   519:     }\n   520: \n   521:     /// Constructs a new `Rc` with uninitialized contents, with the memory\n   522:     /// being filled with `0` bytes.\n   523:     ///\n   524:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and\n   525:     /// incorrect usage of this method.\n   526:     ///\n   527:     /// # Examples",
    "nanvix_source": "   501:     /// // Deferred initialization:\n   502:     /// Rc::get_mut(&mut five).unwrap().write(5);\n   503:     ///\n   504:     /// let five = unsafe { five.assume_init() };\n   505:     ///\n   506:     /// assert_eq!(*five, 5)\n   507:     /// ```\n   508:     #[cfg(not(no_global_oom_handling))]\n   509:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   510:     #[must_use]\n   511:     pub fn new_uninit() -> Rc<mem::MaybeUninit<T>> {\n   512:         unsafe {\n   513:             Rc::from_ptr(Rc::allocate_for_layout(\n   514:                 Layout::new::<T>(),\n   515:                 |layout| Global.allocate(layout),\n   516:                 <*mut u8>::cast,\n   517:             ))\n   518:         }\n   519:     }\n   520: \n   521:     /// Constructs a new `Rc` with uninitialized contents, with the memory",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::new_uninit_slice",
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
      "name": "new_uninit_slice",
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
    "verification_source": "  1117:     ///\n  1118:     /// let mut values = Rc::<[u32]>::new_uninit_slice(3);\n  1119:     ///\n  1120:     /// // Deferred initialization:\n  1121:     /// let data = Rc::get_mut(&mut values).unwrap();\n  1122:     /// data[0].write(1);\n  1123:     /// data[1].write(2);\n  1124:     /// data[2].write(3);\n  1125:     ///\n  1126:     /// let values = unsafe { values.assume_init() };\n  1127:     ///\n  1128:     /// assert_eq!(*values, [1, 2, 3])\n  1129:     /// ```\n  1130:     #[cfg(not(no_global_oom_handling))]\n  1131:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1132:     #[must_use]\n  1133:     pub fn new_uninit_slice(len: usize) -> Rc<[mem::MaybeUninit<T>]> {\n  1134:         unsafe { Rc::from_ptr(Rc::allocate_for_slice(len)) }\n  1135:     }\n  1136: \n  1137:     /// Constructs a new reference-counted slice with uninitialized contents, with the memory being\n  1138:     /// filled with `0` bytes.\n  1139:     ///\n  1140:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and\n  1141:     /// incorrect usage of this method.\n  1142:     ///\n  1143:     /// # Examples\n  1144:     ///\n  1145:     /// ```\n  1146:     /// use std::rc::Rc;\n  1147:     ///\n  1148:     /// let values = Rc::<[u32]>::new_zeroed_slice(3);\n  1149:     /// let values = unsafe { values.assume_init() };",
    "nanvix_source": "  1123:     /// data[1].write(2);\n  1124:     /// data[2].write(3);\n  1125:     ///\n  1126:     /// let values = unsafe { values.assume_init() };\n  1127:     ///\n  1128:     /// assert_eq!(*values, [1, 2, 3])\n  1129:     /// ```\n  1130:     #[cfg(not(no_global_oom_handling))]\n  1131:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1132:     #[must_use]\n  1133:     pub fn new_uninit_slice(len: usize) -> Rc<[mem::MaybeUninit<T>]> {\n  1134:         unsafe { Rc::from_ptr(Rc::allocate_for_slice(len)) }\n  1135:     }\n  1136: \n  1137:     /// Constructs a new reference-counted slice with uninitialized contents, with the memory being\n  1138:     /// filled with `0` bytes.\n  1139:     ///\n  1140:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and\n  1141:     /// incorrect usage of this method.\n  1142:     ///\n  1143:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::new_zeroed",
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
      "name": "new_zeroed",
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
        "inputs": [],
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
                        "id": 431,
                        "path": "mem::MaybeUninit"
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
    "verification_source": "   526:     ///\n   527:     /// # Examples\n   528:     ///\n   529:     /// ```\n   530:     /// use std::rc::Rc;\n   531:     ///\n   532:     /// let zero = Rc::<u32>::new_zeroed();\n   533:     /// let zero = unsafe { zero.assume_init() };\n   534:     ///\n   535:     /// assert_eq!(*zero, 0)\n   536:     /// ```\n   537:     ///\n   538:     /// [zeroed]: mem::MaybeUninit::zeroed\n   539:     #[cfg(not(no_global_oom_handling))]\n   540:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   541:     #[must_use]\n   542:     pub fn new_zeroed() -> Rc<mem::MaybeUninit<T>> {\n   543:         unsafe {\n   544:             Rc::from_ptr(Rc::allocate_for_layout(\n   545:                 Layout::new::<T>(),\n   546:                 |layout| Global.allocate_zeroed(layout),\n   547:                 <*mut u8>::cast,\n   548:             ))\n   549:         }\n   550:     }\n   551: \n   552:     /// Constructs a new `Rc<T>`, returning an error if the allocation fails\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```\n   557:     /// #![feature(allocator_api)]\n   558:     /// use std::rc::Rc;",
    "nanvix_source": "   532:     /// let zero = Rc::<u32>::new_zeroed();\n   533:     /// let zero = unsafe { zero.assume_init() };\n   534:     ///\n   535:     /// assert_eq!(*zero, 0)\n   536:     /// ```\n   537:     ///\n   538:     /// [zeroed]: mem::MaybeUninit::zeroed\n   539:     #[cfg(not(no_global_oom_handling))]\n   540:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   541:     #[must_use]\n   542:     pub fn new_zeroed() -> Rc<mem::MaybeUninit<T>> {\n   543:         unsafe {\n   544:             Rc::from_ptr(Rc::allocate_for_layout(\n   545:                 Layout::new::<T>(),\n   546:                 |layout| Global.allocate_zeroed(layout),\n   547:                 <*mut u8>::cast,\n   548:             ))\n   549:         }\n   550:     }\n   551: \n   552:     /// Constructs a new `Rc<T>`, returning an error if the allocation fails",
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
