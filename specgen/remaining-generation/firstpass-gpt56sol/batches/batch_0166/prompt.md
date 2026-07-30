For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::sync::Arc::downcast",
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
            "name": "T"
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
                      "args": null,
                      "id": 56,
                      "path": "Any"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 8,
                      "path": "Send"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 10,
                      "path": "Sync"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
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
                          },
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 8,
                              "path": "Send"
                            }
                          },
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 10,
                              "path": "Sync"
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
        "impl_id": "alloc:4426",
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
                        "id": 346,
                        "path": "Arc"
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
    "verification_source": "  2872:     /// ```\n  2873:     /// use std::any::Any;\n  2874:     /// use std::sync::Arc;\n  2875:     ///\n  2876:     /// fn print_if_string(value: Arc<dyn Any + Send + Sync>) {\n  2877:     ///     if let Ok(string) = value.downcast::<String>() {\n  2878:     ///         println!(\"String ({}): {}\", string.len(), string);\n  2879:     ///     }\n  2880:     /// }\n  2881:     ///\n  2882:     /// let my_string = \"Hello World\".to_string();\n  2883:     /// print_if_string(Arc::new(my_string));\n  2884:     /// print_if_string(Arc::new(0i8));\n  2885:     /// ```\n  2886:     #[inline]\n  2887:     #[stable(feature = \"rc_downcast\", since = \"1.29.0\")]\n  2888:     pub fn downcast<T>(self) -> Result<Arc<T, A>, Self>\n  2889:     where\n  2890:         T: Any + Send + Sync,\n  2891:     {\n  2892:         if (*self).is::<T>() {\n  2893:             unsafe {\n  2894:                 let (ptr, alloc) = Arc::into_inner_with_allocator(self);\n  2895:                 Ok(Arc::from_inner_in(ptr.cast(), alloc))\n  2896:             }\n  2897:         } else {\n  2898:             Err(self)\n  2899:         }\n  2900:     }\n  2901: \n  2902:     /// Downcasts the `Arc<dyn Any + Send + Sync>` to a concrete type.\n  2903:     ///\n  2904:     /// For a safe alternative see [`downcast`].",
    "nanvix_source": "  2893:     ///         println!(\"String ({}): {}\", string.len(), string);\n  2894:     ///     }\n  2895:     /// }\n  2896:     ///\n  2897:     /// let my_string = \"Hello World\".to_string();\n  2898:     /// print_if_string(Arc::new(my_string));\n  2899:     /// print_if_string(Arc::new(0i8));\n  2900:     /// ```\n  2901:     #[inline]\n  2902:     #[stable(feature = \"rc_downcast\", since = \"1.29.0\")]\n  2903:     pub fn downcast<T>(self) -> Result<Arc<T, A>, Self>\n  2904:     where\n  2905:         T: Any + Send + Sync,\n  2906:     {\n  2907:         if (*self).is::<T>() {\n  2908:             unsafe {\n  2909:                 let (ptr, alloc) = Arc::into_inner_with_allocator(self);\n  2910:                 Ok(Arc::from_inner_in(ptr.cast(), alloc))\n  2911:             }\n  2912:         } else {\n  2913:             Err(self)",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::downgrade",
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
        "impl_id": "alloc:4417",
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
            "id": 4358,
            "path": "Weak"
          }
        }
      }
    },
    "verification_source": "  1908:     }\n  1909: \n  1910:     /// Creates a new [`Weak`] pointer to this allocation.\n  1911:     ///\n  1912:     /// # Examples\n  1913:     ///\n  1914:     /// ```\n  1915:     /// use std::sync::Arc;\n  1916:     ///\n  1917:     /// let five = Arc::new(5);\n  1918:     ///\n  1919:     /// let weak_five = Arc::downgrade(&five);\n  1920:     /// ```\n  1921:     #[must_use = \"this returns a new `Weak` pointer, \\\n  1922:                   without modifying the original `Arc`\"]\n  1923:     #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  1924:     pub fn downgrade(this: &Self) -> Weak<T, A>\n  1925:     where\n  1926:         A: Clone,\n  1927:     {\n  1928:         // This Relaxed is OK because we're checking the value in the CAS\n  1929:         // below.\n  1930:         let mut cur = this.inner().weak.load(Relaxed);\n  1931: \n  1932:         loop {\n  1933:             // check if the weak counter is currently \"locked\"; if so, spin.\n  1934:             if cur == usize::MAX {\n  1935:                 hint::spin_loop();\n  1936:                 cur = this.inner().weak.load(Relaxed);\n  1937:                 continue;\n  1938:             }\n  1939: \n  1940:             // We can't allow the refcount to increase much past `MAX_REFCOUNT`.",
    "nanvix_source": "  1926:     /// ```\n  1927:     /// use std::sync::Arc;\n  1928:     ///\n  1929:     /// let five = Arc::new(5);\n  1930:     ///\n  1931:     /// let weak_five = Arc::downgrade(&five);\n  1932:     /// ```\n  1933:     #[must_use = \"this returns a new `Weak` pointer, \\\n  1934:                   without modifying the original `Arc`\"]\n  1935:     #[stable(feature = \"arc_weak\", since = \"1.4.0\")]\n  1936:     pub fn downgrade(this: &Self) -> Weak<T, A>\n  1937:     where\n  1938:         A: Clone,\n  1939:     {\n  1940:         // This Relaxed is OK because we're checking the value in the CAS\n  1941:         // below.\n  1942:         let mut cur = this.inner().weak.load(Relaxed);\n  1943: \n  1944:         loop {\n  1945:             // check if the weak counter is currently \"locked\"; if so, spin.\n  1946:             if cur == usize::MAX {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::into_inner",
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4385",
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
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1210:     /// let mut x = LinkedList::new();\n  1211:     /// let size = 100000;\n  1212:     /// # let size = if cfg!(miri) { 100 } else { size };\n  1213:     /// for i in 0..size {\n  1214:     ///     x.push(i); // Adds i to the front of x\n  1215:     /// }\n  1216:     /// let y = x.clone();\n  1217:     ///\n  1218:     /// // Drop the clones in parallel\n  1219:     /// let x_thread = std::thread::spawn(|| drop(x));\n  1220:     /// let y_thread = std::thread::spawn(|| drop(y));\n  1221:     /// x_thread.join().unwrap();\n  1222:     /// y_thread.join().unwrap();\n  1223:     /// ```\n  1224:     #[inline]\n  1225:     #[stable(feature = \"arc_into_inner\", since = \"1.70.0\")]\n  1226:     pub fn into_inner(this: Self) -> Option<T> {\n  1227:         // Make sure that the ordinary `Drop` implementation isn\u2019t called as well\n  1228:         let mut this = mem::ManuallyDrop::new(this);\n  1229: \n  1230:         // Following the implementation of `drop` and `drop_slow`\n  1231:         if this.inner().strong.fetch_sub(1, Release) != 1 {\n  1232:             return None;\n  1233:         }\n  1234: \n  1235:         acquire!(this.inner().strong);\n  1236: \n  1237:         // SAFETY: This mirrors the line\n  1238:         //\n  1239:         //     unsafe { ptr::drop_in_place(Self::get_mut_unchecked(self)) };\n  1240:         //\n  1241:         // in `drop_slow`. Instead of dropping the value behind the pointer,\n  1242:         // it is read and eventually returned; `ptr::read` has the same",
    "nanvix_source": "  1220:     /// let y = x.clone();\n  1221:     ///\n  1222:     /// // Drop the clones in parallel\n  1223:     /// let x_thread = std::thread::spawn(|| drop(x));\n  1224:     /// let y_thread = std::thread::spawn(|| drop(y));\n  1225:     /// x_thread.join().unwrap();\n  1226:     /// y_thread.join().unwrap();\n  1227:     /// ```\n  1228:     #[inline]\n  1229:     #[stable(feature = \"arc_into_inner\", since = \"1.70.0\")]\n  1230:     pub fn into_inner(this: Self) -> Option<T> {\n  1231:         // Make sure that the ordinary `Drop` implementation isn\u2019t called as well\n  1232:         let mut this = mem::ManuallyDrop::new(this);\n  1233: \n  1234:         // Following the implementation of `drop` and `drop_slow`\n  1235:         if this.inner().strong.fetch_sub(1, Release) != 1 {\n  1236:             return None;\n  1237:         }\n  1238: \n  1239:         acquire!(this.inner().strong);\n  1240: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::new_cyclic",
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
                                    "id": 4358,
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4373",
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
            "id": 346,
            "path": "Arc"
          }
        }
      }
    },
    "verification_source": "   473:     ///         Arc::new_cyclic(|me| {\n   474:     ///             // Create the actual struct here.\n   475:     ///             Gadget { me: me.clone() }\n   476:     ///         })\n   477:     ///     }\n   478:     ///\n   479:     ///     /// Returns a reference counted pointer to Self.\n   480:     ///     fn me(&self) -> Arc<Self> {\n   481:     ///         self.me.upgrade().unwrap()\n   482:     ///     }\n   483:     /// }\n   484:     /// ```\n   485:     /// [`upgrade`]: Weak::upgrade\n   486:     #[cfg(not(no_global_oom_handling))]\n   487:     #[inline]\n   488:     #[stable(feature = \"arc_new_cyclic\", since = \"1.60.0\")]\n   489:     pub fn new_cyclic<F>(data_fn: F) -> Arc<T>\n   490:     where\n   491:         F: FnOnce(&Weak<T>) -> T,\n   492:     {\n   493:         Self::new_cyclic_in(data_fn, Global)\n   494:     }\n   495: \n   496:     /// Constructs a new `Arc` with uninitialized contents.\n   497:     ///\n   498:     /// # Examples\n   499:     ///\n   500:     /// ```\n   501:     /// use std::sync::Arc;\n   502:     ///\n   503:     /// let mut five = Arc::<u32>::new_uninit();\n   504:     ///\n   505:     /// // Deferred initialization:",
    "nanvix_source": "   483:     ///     /// Returns a reference counted pointer to Self.\n   484:     ///     fn me(&self) -> Arc<Self> {\n   485:     ///         self.me.upgrade().unwrap()\n   486:     ///     }\n   487:     /// }\n   488:     /// ```\n   489:     /// [`upgrade`]: Weak::upgrade\n   490:     #[cfg(not(no_global_oom_handling))]\n   491:     #[inline]\n   492:     #[stable(feature = \"arc_new_cyclic\", since = \"1.60.0\")]\n   493:     pub fn new_cyclic<F>(data_fn: F) -> Arc<T>\n   494:     where\n   495:         F: FnOnce(&Weak<T>) -> T,\n   496:     {\n   497:         Self::new_cyclic_in(data_fn, Global)\n   498:     }\n   499: \n   500:     /// Constructs a new `Arc` with uninitialized contents.\n   501:     ///\n   502:     /// # Examples\n   503:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::new_uninit",
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4373",
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
            "id": 346,
            "path": "Arc"
          }
        }
      }
    },
    "verification_source": "   500:     /// ```\n   501:     /// use std::sync::Arc;\n   502:     ///\n   503:     /// let mut five = Arc::<u32>::new_uninit();\n   504:     ///\n   505:     /// // Deferred initialization:\n   506:     /// Arc::get_mut(&mut five).unwrap().write(5);\n   507:     ///\n   508:     /// let five = unsafe { five.assume_init() };\n   509:     ///\n   510:     /// assert_eq!(*five, 5)\n   511:     /// ```\n   512:     #[cfg(not(no_global_oom_handling))]\n   513:     #[inline]\n   514:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   515:     #[must_use]\n   516:     pub fn new_uninit() -> Arc<mem::MaybeUninit<T>> {\n   517:         unsafe {\n   518:             Arc::from_ptr(Arc::allocate_for_layout(\n   519:                 Layout::new::<T>(),\n   520:                 |layout| Global.allocate(layout),\n   521:                 <*mut u8>::cast,\n   522:             ))\n   523:         }\n   524:     }\n   525: \n   526:     /// Constructs a new `Arc` with uninitialized contents, with the memory\n   527:     /// being filled with `0` bytes.\n   528:     ///\n   529:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and incorrect usage\n   530:     /// of this method.\n   531:     ///\n   532:     /// # Examples",
    "nanvix_source": "   510:     /// Arc::get_mut(&mut five).unwrap().write(5);\n   511:     ///\n   512:     /// let five = unsafe { five.assume_init() };\n   513:     ///\n   514:     /// assert_eq!(*five, 5)\n   515:     /// ```\n   516:     #[cfg(not(no_global_oom_handling))]\n   517:     #[inline]\n   518:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   519:     #[must_use]\n   520:     pub fn new_uninit() -> Arc<mem::MaybeUninit<T>> {\n   521:         unsafe {\n   522:             Arc::from_ptr(Arc::allocate_for_layout(\n   523:                 Layout::new::<T>(),\n   524:                 |layout| Global.allocate(layout),\n   525:                 <*mut u8>::cast,\n   526:             ))\n   527:         }\n   528:     }\n   529: \n   530:     /// Constructs a new `Arc` with uninitialized contents, with the memory",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::new_uninit_slice",
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
            "id": 346,
            "path": "Arc"
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
        "impl_id": "alloc:4389",
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
            "id": 346,
            "path": "Arc"
          }
        }
      }
    },
    "verification_source": "  1262:     /// let mut values = Arc::<[u32]>::new_uninit_slice(3);\n  1263:     ///\n  1264:     /// // Deferred initialization:\n  1265:     /// let data = Arc::get_mut(&mut values).unwrap();\n  1266:     /// data[0].write(1);\n  1267:     /// data[1].write(2);\n  1268:     /// data[2].write(3);\n  1269:     ///\n  1270:     /// let values = unsafe { values.assume_init() };\n  1271:     ///\n  1272:     /// assert_eq!(*values, [1, 2, 3])\n  1273:     /// ```\n  1274:     #[cfg(not(no_global_oom_handling))]\n  1275:     #[inline]\n  1276:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1277:     #[must_use]\n  1278:     pub fn new_uninit_slice(len: usize) -> Arc<[mem::MaybeUninit<T>]> {\n  1279:         unsafe { Arc::from_ptr(Arc::allocate_for_slice(len)) }\n  1280:     }\n  1281: \n  1282:     /// Constructs a new atomically reference-counted slice with uninitialized contents, with the memory being\n  1283:     /// filled with `0` bytes.\n  1284:     ///\n  1285:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and\n  1286:     /// incorrect usage of this method.\n  1287:     ///\n  1288:     /// # Examples\n  1289:     ///\n  1290:     /// ```\n  1291:     /// use std::sync::Arc;\n  1292:     ///\n  1293:     /// let values = Arc::<[u32]>::new_zeroed_slice(3);\n  1294:     /// let values = unsafe { values.assume_init() };",
    "nanvix_source": "  1272:     /// data[2].write(3);\n  1273:     ///\n  1274:     /// let values = unsafe { values.assume_init() };\n  1275:     ///\n  1276:     /// assert_eq!(*values, [1, 2, 3])\n  1277:     /// ```\n  1278:     #[cfg(not(no_global_oom_handling))]\n  1279:     #[inline]\n  1280:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1281:     #[must_use]\n  1282:     pub fn new_uninit_slice(len: usize) -> Arc<[mem::MaybeUninit<T>]> {\n  1283:         unsafe { Arc::from_ptr(Arc::allocate_for_slice(len)) }\n  1284:     }\n  1285: \n  1286:     /// Constructs a new atomically reference-counted slice with uninitialized contents, with the memory being\n  1287:     /// filled with `0` bytes.\n  1288:     ///\n  1289:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and\n  1290:     /// incorrect usage of this method.\n  1291:     ///\n  1292:     /// # Examples",
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
