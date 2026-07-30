For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::boxed::Box::into_pin",
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
                  "outlives": "'static"
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
      "name": "into_pin",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:494",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "boxed",
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
                      "generic": "Self"
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
    "verification_source": "  1892:     /// as it'll introduce an ambiguity when calling `Pin::from`.\n  1893:     /// A demonstration of such a poor impl is shown below.\n  1894:     ///\n  1895:     /// ```compile_fail\n  1896:     /// # use std::pin::Pin;\n  1897:     /// struct Foo; // A type defined in this crate.\n  1898:     /// impl From<Box<()>> for Pin<Foo> {\n  1899:     ///     fn from(_: Box<()>) -> Pin<Foo> {\n  1900:     ///         Pin::new(Foo)\n  1901:     ///     }\n  1902:     /// }\n  1903:     ///\n  1904:     /// let foo = Box::new(());\n  1905:     /// let bar = Pin::from(foo);\n  1906:     /// ```\n  1907:     #[stable(feature = \"box_into_pin\", since = \"1.63.0\")]\n  1908:     pub fn into_pin(boxed: Self) -> Pin<Self>\n  1909:     where\n  1910:         A: 'static,\n  1911:     {\n  1912:         // It's not possible to move or replace the insides of a `Pin<Box<T>>`\n  1913:         // when `T: !Unpin`, so it's safe to pin it directly without any\n  1914:         // additional requirements.\n  1915:         unsafe { Pin::new_unchecked(boxed) }\n  1916:     }\n  1917: }\n  1918: \n  1919: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1920: unsafe impl<#[may_dangle] T: ?Sized, A: Allocator> Drop for Box<T, A> {\n  1921:     #[inline]\n  1922:     fn drop(&mut self) {\n  1923:         // the T in the Box is dropped by the compiler before the destructor is run\n  1924: ",
    "nanvix_source": "  1970:     /// impl From<Box<()>> for Pin<Foo> {\n  1971:     ///     fn from(_: Box<()>) -> Pin<Foo> {\n  1972:     ///         Pin::new(Foo)\n  1973:     ///     }\n  1974:     /// }\n  1975:     ///\n  1976:     /// let foo = Box::new(());\n  1977:     /// let bar = Pin::from(foo);\n  1978:     /// ```\n  1979:     #[stable(feature = \"box_into_pin\", since = \"1.63.0\")]\n  1980:     pub fn into_pin(boxed: Self) -> Pin<Self>\n  1981:     where\n  1982:         A: 'static,\n  1983:     {\n  1984:         // It's not possible to move or replace the insides of a `Pin<Box<T>>`\n  1985:         // when `T: !Unpin`, so it's safe to pin it directly without any\n  1986:         // additional requirements.\n  1987:         unsafe { Pin::new_unchecked(boxed) }\n  1988:     }\n  1989: }\n  1990: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::new_uninit_slice",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:469",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
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
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "   900:     ///\n   901:     /// # Examples\n   902:     ///\n   903:     /// ```\n   904:     /// let mut values = Box::<[u32]>::new_uninit_slice(3);\n   905:     /// // Deferred initialization:\n   906:     /// values[0].write(1);\n   907:     /// values[1].write(2);\n   908:     /// values[2].write(3);\n   909:     /// let values = unsafe { values.assume_init() };\n   910:     ///\n   911:     /// assert_eq!(*values, [1, 2, 3])\n   912:     /// ```\n   913:     #[cfg(not(no_global_oom_handling))]\n   914:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   915:     #[must_use]\n   916:     pub fn new_uninit_slice(len: usize) -> Box<[mem::MaybeUninit<T>]> {\n   917:         unsafe { RawVec::with_capacity(len).into_box(len) }\n   918:     }\n   919: \n   920:     /// Constructs a new boxed slice with uninitialized contents, with the memory\n   921:     /// being filled with `0` bytes.\n   922:     ///\n   923:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and incorrect usage\n   924:     /// of this method.\n   925:     ///\n   926:     /// # Examples\n   927:     ///\n   928:     /// ```\n   929:     /// let values = Box::<[u32]>::new_zeroed_slice(3);\n   930:     /// let values = unsafe { values.assume_init() };\n   931:     ///\n   932:     /// assert_eq!(*values, [0, 0, 0])",
    "nanvix_source": "   908:     /// values[0].write(1);\n   909:     /// values[1].write(2);\n   910:     /// values[2].write(3);\n   911:     /// let values = unsafe { values.assume_init() };\n   912:     ///\n   913:     /// assert_eq!(*values, [1, 2, 3])\n   914:     /// ```\n   915:     #[cfg(not(no_global_oom_handling))]\n   916:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n   917:     #[must_use]\n   918:     pub fn new_uninit_slice(len: usize) -> Box<[mem::MaybeUninit<T>]> {\n   919:         unsafe { RawVec::with_capacity(len).into_box(len) }\n   920:     }\n   921: \n   922:     /// Constructs a new boxed slice with uninitialized contents, with the memory\n   923:     /// being filled with `0` bytes.\n   924:     ///\n   925:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and incorrect usage\n   926:     /// of this method.\n   927:     ///\n   928:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::new_zeroed",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:445",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
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
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "   324:     /// of this method.\n   325:     ///\n   326:     /// # Examples\n   327:     ///\n   328:     /// ```\n   329:     /// let zero = Box::<u32>::new_zeroed();\n   330:     /// let zero = unsafe { zero.assume_init() };\n   331:     ///\n   332:     /// assert_eq!(*zero, 0)\n   333:     /// ```\n   334:     ///\n   335:     /// [zeroed]: mem::MaybeUninit::zeroed\n   336:     #[cfg(not(no_global_oom_handling))]\n   337:     #[inline]\n   338:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   339:     #[must_use]\n   340:     pub fn new_zeroed() -> Box<mem::MaybeUninit<T>> {\n   341:         Self::new_zeroed_in(Global)\n   342:     }\n   343: \n   344:     /// Constructs a new `Pin<Box<T>>`. If `T` does not implement [`Unpin`], then\n   345:     /// `x` will be pinned in memory and unable to be moved.\n   346:     ///\n   347:     /// Constructing and pinning of the `Box` can also be done in two steps: `Box::pin(x)`\n   348:     /// does the same as <code>[Box::into_pin]\\([Box::new]\\(x))</code>. Consider using\n   349:     /// [`into_pin`](Box::into_pin) if you already have a `Box<T>`, or if you want to\n   350:     /// construct a (pinned) `Box` in a different way than with [`Box::new`].\n   351:     #[cfg(not(no_global_oom_handling))]\n   352:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   353:     #[must_use]\n   354:     #[inline(always)]\n   355:     pub fn pin(x: T) -> Pin<Box<T>> {\n   356:         Box::new(x).into()",
    "nanvix_source": "   332:     /// let zero = unsafe { zero.assume_init() };\n   333:     ///\n   334:     /// assert_eq!(*zero, 0)\n   335:     /// ```\n   336:     ///\n   337:     /// [zeroed]: mem::MaybeUninit::zeroed\n   338:     #[cfg(not(no_global_oom_handling))]\n   339:     #[inline]\n   340:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   341:     #[must_use]\n   342:     pub fn new_zeroed() -> Box<mem::MaybeUninit<T>> {\n   343:         Self::new_zeroed_in(Global)\n   344:     }\n   345: \n   346:     /// Constructs a new `Pin<Box<T>>`. If `T` does not implement [`Unpin`], then\n   347:     /// `x` will be pinned in memory and unable to be moved.\n   348:     ///\n   349:     /// Constructing and pinning of the `Box` can also be done in two steps: `Box::pin(x)`\n   350:     /// does the same as <code>[Box::into_pin]\\([Box::new]\\(x))</code>. Consider using\n   351:     /// [`into_pin`](Box::into_pin) if you already have a `Box<T>`, or if you want to\n   352:     /// construct a (pinned) `Box` in a different way than with [`Box::new`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::new_zeroed_slice",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:469",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
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
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "   923:     /// See [`MaybeUninit::zeroed`][zeroed] for examples of correct and incorrect usage\n   924:     /// of this method.\n   925:     ///\n   926:     /// # Examples\n   927:     ///\n   928:     /// ```\n   929:     /// let values = Box::<[u32]>::new_zeroed_slice(3);\n   930:     /// let values = unsafe { values.assume_init() };\n   931:     ///\n   932:     /// assert_eq!(*values, [0, 0, 0])\n   933:     /// ```\n   934:     ///\n   935:     /// [zeroed]: mem::MaybeUninit::zeroed\n   936:     #[cfg(not(no_global_oom_handling))]\n   937:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   938:     #[must_use]\n   939:     pub fn new_zeroed_slice(len: usize) -> Box<[mem::MaybeUninit<T>]> {\n   940:         unsafe { RawVec::with_capacity_zeroed(len).into_box(len) }\n   941:     }\n   942: \n   943:     /// Constructs a new boxed slice with uninitialized contents. Returns an error if\n   944:     /// the allocation fails.\n   945:     ///\n   946:     /// # Examples\n   947:     ///\n   948:     /// ```\n   949:     /// #![feature(allocator_api)]\n   950:     ///\n   951:     /// let mut values = Box::<[u32]>::try_new_uninit_slice(3)?;\n   952:     /// // Deferred initialization:\n   953:     /// values[0].write(1);\n   954:     /// values[1].write(2);\n   955:     /// values[2].write(3);",
    "nanvix_source": "   931:     /// let values = Box::<[u32]>::new_zeroed_slice(3);\n   932:     /// let values = unsafe { values.assume_init() };\n   933:     ///\n   934:     /// assert_eq!(*values, [0, 0, 0])\n   935:     /// ```\n   936:     ///\n   937:     /// [zeroed]: mem::MaybeUninit::zeroed\n   938:     #[cfg(not(no_global_oom_handling))]\n   939:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   940:     #[must_use]\n   941:     pub fn new_zeroed_slice(len: usize) -> Box<[mem::MaybeUninit<T>]> {\n   942:         unsafe { RawVec::with_capacity_zeroed(len).into_box(len) }\n   943:     }\n   944: \n   945:     /// Constructs a new boxed slice with uninitialized contents. Returns an error if\n   946:     /// the allocation fails.\n   947:     ///\n   948:     /// # Examples\n   949:     ///\n   950:     /// ```\n   951:     /// #![feature(allocator_api)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::pin",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:445",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "x",
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
                        "id": 82,
                        "path": "Box"
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
    "verification_source": "   339:     #[must_use]\n   340:     pub fn new_zeroed() -> Box<mem::MaybeUninit<T>> {\n   341:         Self::new_zeroed_in(Global)\n   342:     }\n   343: \n   344:     /// Constructs a new `Pin<Box<T>>`. If `T` does not implement [`Unpin`], then\n   345:     /// `x` will be pinned in memory and unable to be moved.\n   346:     ///\n   347:     /// Constructing and pinning of the `Box` can also be done in two steps: `Box::pin(x)`\n   348:     /// does the same as <code>[Box::into_pin]\\([Box::new]\\(x))</code>. Consider using\n   349:     /// [`into_pin`](Box::into_pin) if you already have a `Box<T>`, or if you want to\n   350:     /// construct a (pinned) `Box` in a different way than with [`Box::new`].\n   351:     #[cfg(not(no_global_oom_handling))]\n   352:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   353:     #[must_use]\n   354:     #[inline(always)]\n   355:     pub fn pin(x: T) -> Pin<Box<T>> {\n   356:         Box::new(x).into()\n   357:     }\n   358: \n   359:     /// Allocates memory on the heap then places `x` into it,\n   360:     /// returning an error if the allocation fails\n   361:     ///\n   362:     /// This doesn't actually allocate if `T` is zero-sized.\n   363:     ///\n   364:     /// # Examples\n   365:     ///\n   366:     /// ```\n   367:     /// #![feature(allocator_api)]\n   368:     ///\n   369:     /// let five = Box::try_new(5)?;\n   370:     /// # Ok::<(), std::alloc::AllocError>(())\n   371:     /// ```",
    "nanvix_source": "   347:     /// `x` will be pinned in memory and unable to be moved.\n   348:     ///\n   349:     /// Constructing and pinning of the `Box` can also be done in two steps: `Box::pin(x)`\n   350:     /// does the same as <code>[Box::into_pin]\\([Box::new]\\(x))</code>. Consider using\n   351:     /// [`into_pin`](Box::into_pin) if you already have a `Box<T>`, or if you want to\n   352:     /// construct a (pinned) `Box` in a different way than with [`Box::new`].\n   353:     #[cfg(not(no_global_oom_handling))]\n   354:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   355:     #[must_use]\n   356:     #[inline(always)]\n   357:     pub fn pin(x: T) -> Pin<Box<T>> {\n   358:         Box::new(x).into()\n   359:     }\n   360: \n   361:     /// Allocates memory on the heap then places `x` into it,\n   362:     /// returning an error if the allocation fails\n   363:     ///\n   364:     /// This doesn't actually allocate if `T` is zero-sized.\n   365:     ///\n   366:     /// # Examples\n   367:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::write",
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
      "name": "write",
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:477",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "boxed",
            {
              "generic": "Self"
            }
          ],
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
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "  1205:     ///\n  1206:     /// let mut array = [0; 1024];\n  1207:     /// for (i, place) in array.iter_mut().enumerate() {\n  1208:     ///     *place = i;\n  1209:     /// }\n  1210:     ///\n  1211:     /// // The optimizer may be able to elide this copy, so previous code writes\n  1212:     /// // to heap directly.\n  1213:     /// let big_box = Box::write(big_box, array);\n  1214:     ///\n  1215:     /// for (i, x) in big_box.iter().enumerate() {\n  1216:     ///     assert_eq!(*x, i);\n  1217:     /// }\n  1218:     /// ```\n  1219:     #[stable(feature = \"box_uninit_write\", since = \"1.87.0\")]\n  1220:     #[inline]\n  1221:     pub fn write(mut boxed: Self, value: T) -> Box<T, A> {\n  1222:         unsafe {\n  1223:             (*boxed).write(value);\n  1224:             boxed.assume_init()\n  1225:         }\n  1226:     }\n  1227: }\n  1228: \n  1229: impl<T, A: Allocator> Box<[mem::MaybeUninit<T>], A> {\n  1230:     /// Converts to `Box<[T], A>`.\n  1231:     ///\n  1232:     /// # Safety\n  1233:     ///\n  1234:     /// As with [`MaybeUninit::assume_init`],\n  1235:     /// it is up to the caller to guarantee that the values\n  1236:     /// really are in an initialized state.\n  1237:     /// Calling this when the content is not yet fully initialized",
    "nanvix_source": "  1225:     /// // The optimizer may be able to elide this copy, so previous code writes\n  1226:     /// // to heap directly.\n  1227:     /// let big_box = Box::write(big_box, array);\n  1228:     ///\n  1229:     /// for (i, x) in big_box.iter().enumerate() {\n  1230:     ///     assert_eq!(*x, i);\n  1231:     /// }\n  1232:     /// ```\n  1233:     #[stable(feature = \"box_uninit_write\", since = \"1.87.0\")]\n  1234:     #[inline]\n  1235:     pub fn write(mut boxed: Self, value: T) -> Box<T, A> {\n  1236:         unsafe {\n  1237:             (*boxed).write(value);\n  1238:             boxed.assume_init()\n  1239:         }\n  1240:     }\n  1241: }\n  1242: \n  1243: impl<T, A: Allocator> Box<[mem::MaybeUninit<T>], A> {\n  1244:     /// Converts to `Box<[T], A>`.\n  1245:     ///",
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
