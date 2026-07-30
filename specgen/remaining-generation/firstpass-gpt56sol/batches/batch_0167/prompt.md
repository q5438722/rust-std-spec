For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::sync::Arc::new_zeroed",
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
    "verification_source": "   532:     /// # Examples\n   533:     ///\n   534:     /// ```\n   535:     /// use std::sync::Arc;\n   536:     ///\n   537:     /// let zero = Arc::<u32>::new_zeroed();\n   538:     /// let zero = unsafe { zero.assume_init() };\n   539:     ///\n   540:     /// assert_eq!(*zero, 0)\n   541:     /// ```\n   542:     ///\n   543:     /// [zeroed]: mem::MaybeUninit::zeroed\n   544:     #[cfg(not(no_global_oom_handling))]\n   545:     #[inline]\n   546:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   547:     #[must_use]\n   548:     pub fn new_zeroed() -> Arc<mem::MaybeUninit<T>> {\n   549:         unsafe {\n   550:             Arc::from_ptr(Arc::allocate_for_layout(\n   551:                 Layout::new::<T>(),\n   552:                 |layout| Global.allocate_zeroed(layout),\n   553:                 <*mut u8>::cast,\n   554:             ))\n   555:         }\n   556:     }\n   557: \n   558:     /// Constructs a new `Pin<Arc<T>>`. If `T` does not implement `Unpin`, then\n   559:     /// `data` will be pinned in memory and unable to be moved.\n   560:     #[cfg(not(no_global_oom_handling))]\n   561:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   562:     #[must_use]\n   563:     pub fn pin(data: T) -> Pin<Arc<T>> {\n   564:         unsafe { Pin::new_unchecked(Arc::new(data)) }",
    "nanvix_source": "   542:     /// let zero = unsafe { zero.assume_init() };\n   543:     ///\n   544:     /// assert_eq!(*zero, 0)\n   545:     /// ```\n   546:     ///\n   547:     /// [zeroed]: mem::MaybeUninit::zeroed\n   548:     #[cfg(not(no_global_oom_handling))]\n   549:     #[inline]\n   550:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n   551:     #[must_use]\n   552:     pub fn new_zeroed() -> Arc<mem::MaybeUninit<T>> {\n   553:         unsafe {\n   554:             Arc::from_ptr(Arc::allocate_for_layout(\n   555:                 Layout::new::<T>(),\n   556:                 |layout| Global.allocate_zeroed(layout),\n   557:                 <*mut u8>::cast,\n   558:             ))\n   559:         }\n   560:     }\n   561: \n   562:     /// Constructs a new `Pin<Arc<T>>`. If `T` does not implement `Unpin`, then",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::new_zeroed_slice",
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
    "verification_source": "  1288:     /// # Examples\n  1289:     ///\n  1290:     /// ```\n  1291:     /// use std::sync::Arc;\n  1292:     ///\n  1293:     /// let values = Arc::<[u32]>::new_zeroed_slice(3);\n  1294:     /// let values = unsafe { values.assume_init() };\n  1295:     ///\n  1296:     /// assert_eq!(*values, [0, 0, 0])\n  1297:     /// ```\n  1298:     ///\n  1299:     /// [zeroed]: mem::MaybeUninit::zeroed\n  1300:     #[cfg(not(no_global_oom_handling))]\n  1301:     #[inline]\n  1302:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n  1303:     #[must_use]\n  1304:     pub fn new_zeroed_slice(len: usize) -> Arc<[mem::MaybeUninit<T>]> {\n  1305:         unsafe {\n  1306:             Arc::from_ptr(Arc::allocate_for_layout(\n  1307:                 Layout::array::<T>(len).unwrap(),\n  1308:                 |layout| Global.allocate_zeroed(layout),\n  1309:                 |mem| {\n  1310:                     ptr::slice_from_raw_parts_mut(mem as *mut T, len)\n  1311:                         as *mut ArcInner<[mem::MaybeUninit<T>]>\n  1312:                 },\n  1313:             ))\n  1314:         }\n  1315:     }\n  1316: \n  1317:     /// Converts the reference-counted slice into a reference-counted array.\n  1318:     ///\n  1319:     /// This operation does not reallocate; the underlying array of the slice is simply reinterpreted as an array type.\n  1320:     ///",
    "nanvix_source": "  1298:     /// let values = unsafe { values.assume_init() };\n  1299:     ///\n  1300:     /// assert_eq!(*values, [0, 0, 0])\n  1301:     /// ```\n  1302:     ///\n  1303:     /// [zeroed]: mem::MaybeUninit::zeroed\n  1304:     #[cfg(not(no_global_oom_handling))]\n  1305:     #[inline]\n  1306:     #[stable(feature = \"new_zeroed_alloc\", since = \"1.92.0\")]\n  1307:     #[must_use]\n  1308:     pub fn new_zeroed_slice(len: usize) -> Arc<[mem::MaybeUninit<T>]> {\n  1309:         unsafe {\n  1310:             Arc::from_ptr(Arc::allocate_for_layout(\n  1311:                 Layout::array::<T>(len).unwrap(),\n  1312:                 |layout| Global.allocate_zeroed(layout),\n  1313:                 |mem| mem.cast::<T>().cast_slice(len) as *mut ArcInner<[mem::MaybeUninit<T>]>,\n  1314:             ))\n  1315:         }\n  1316:     }\n  1317: }\n  1318: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::pin",
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
            "data",
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
                        "id": 346,
                        "path": "Arc"
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
    "verification_source": "   547:     #[must_use]\n   548:     pub fn new_zeroed() -> Arc<mem::MaybeUninit<T>> {\n   549:         unsafe {\n   550:             Arc::from_ptr(Arc::allocate_for_layout(\n   551:                 Layout::new::<T>(),\n   552:                 |layout| Global.allocate_zeroed(layout),\n   553:                 <*mut u8>::cast,\n   554:             ))\n   555:         }\n   556:     }\n   557: \n   558:     /// Constructs a new `Pin<Arc<T>>`. If `T` does not implement `Unpin`, then\n   559:     /// `data` will be pinned in memory and unable to be moved.\n   560:     #[cfg(not(no_global_oom_handling))]\n   561:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   562:     #[must_use]\n   563:     pub fn pin(data: T) -> Pin<Arc<T>> {\n   564:         unsafe { Pin::new_unchecked(Arc::new(data)) }\n   565:     }\n   566: \n   567:     /// Constructs a new `Pin<Arc<T>>`, return an error if allocation fails.\n   568:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   569:     #[inline]\n   570:     pub fn try_pin(data: T) -> Result<Pin<Arc<T>>, AllocError> {\n   571:         unsafe { Ok(Pin::new_unchecked(Arc::try_new(data)?)) }\n   572:     }\n   573: \n   574:     /// Constructs a new `Arc<T>`, returning an error if allocation fails.\n   575:     ///\n   576:     /// # Examples\n   577:     ///\n   578:     /// ```\n   579:     /// #![feature(allocator_api)]",
    "nanvix_source": "   557:                 <*mut u8>::cast,\n   558:             ))\n   559:         }\n   560:     }\n   561: \n   562:     /// Constructs a new `Pin<Arc<T>>`. If `T` does not implement `Unpin`, then\n   563:     /// `data` will be pinned in memory and unable to be moved.\n   564:     #[cfg(not(no_global_oom_handling))]\n   565:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   566:     #[must_use]\n   567:     pub fn pin(data: T) -> Pin<Arc<T>> {\n   568:         unsafe { Pin::new_unchecked(Arc::new(data)) }\n   569:     }\n   570: \n   571:     /// Constructs a new `Pin<Arc<T>>`, return an error if allocation fails.\n   572:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n   573:     #[inline]\n   574:     pub fn try_pin(data: T) -> Result<Pin<Arc<T>>, AllocError> {\n   575:         unsafe { Ok(Pin::new_unchecked(Arc::try_new(data)?)) }\n   576:     }\n   577: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::ptr_eq",
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
    "verification_source": "  2138:     ///\n  2139:     /// ```\n  2140:     /// use std::sync::Arc;\n  2141:     ///\n  2142:     /// let five = Arc::new(5);\n  2143:     /// let same_five = Arc::clone(&five);\n  2144:     /// let other_five = Arc::new(5);\n  2145:     ///\n  2146:     /// assert!(Arc::ptr_eq(&five, &same_five));\n  2147:     /// assert!(!Arc::ptr_eq(&five, &other_five));\n  2148:     /// ```\n  2149:     ///\n  2150:     /// [`ptr::eq`]: core::ptr::eq \"ptr::eq\"\n  2151:     #[inline]\n  2152:     #[must_use]\n  2153:     #[stable(feature = \"ptr_eq\", since = \"1.17.0\")]\n  2154:     pub fn ptr_eq(this: &Self, other: &Self) -> bool {\n  2155:         ptr::addr_eq(this.ptr.as_ptr(), other.ptr.as_ptr())\n  2156:     }\n  2157: }\n  2158: \n  2159: impl<T: ?Sized> Arc<T> {\n  2160:     /// Allocates an `ArcInner<T>` with sufficient space for\n  2161:     /// a possibly-unsized inner value where the value has the layout provided.\n  2162:     ///\n  2163:     /// The function `mem_to_arcinner` is called with the data pointer\n  2164:     /// and must return back a (potentially fat)-pointer for the `ArcInner<T>`.\n  2165:     #[cfg(not(no_global_oom_handling))]\n  2166:     unsafe fn allocate_for_layout(\n  2167:         value_layout: Layout,\n  2168:         allocate: impl FnOnce(Layout) -> Result<NonNull<[u8]>, AllocError>,\n  2169:         mem_to_arcinner: impl FnOnce(*mut u8) -> *mut ArcInner<T>,\n  2170:     ) -> *mut ArcInner<T> {",
    "nanvix_source": "  2156:     /// let other_five = Arc::new(5);\n  2157:     ///\n  2158:     /// assert!(Arc::ptr_eq(&five, &same_five));\n  2159:     /// assert!(!Arc::ptr_eq(&five, &other_five));\n  2160:     /// ```\n  2161:     ///\n  2162:     /// [`ptr::eq`]: core::ptr::eq \"ptr::eq\"\n  2163:     #[inline]\n  2164:     #[must_use]\n  2165:     #[stable(feature = \"ptr_eq\", since = \"1.17.0\")]\n  2166:     pub fn ptr_eq(this: &Self, other: &Self) -> bool {\n  2167:         ptr::addr_eq(this.ptr.as_ptr(), other.ptr.as_ptr())\n  2168:     }\n  2169: }\n  2170: \n  2171: impl<T: ?Sized> Arc<T> {\n  2172:     /// Allocates an `ArcInner<T>` with sufficient space for\n  2173:     /// a possibly-unsized inner value where the value has the layout provided.\n  2174:     ///\n  2175:     /// The function `mem_to_arcinner` is called with the data pointer\n  2176:     /// and must return back a (potentially fat)-pointer for the `ArcInner<T>`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::strong_count",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1998:     ///\n  1999:     /// # Examples\n  2000:     ///\n  2001:     /// ```\n  2002:     /// use std::sync::Arc;\n  2003:     ///\n  2004:     /// let five = Arc::new(5);\n  2005:     /// let _also_five = Arc::clone(&five);\n  2006:     ///\n  2007:     /// // This assertion is deterministic because we haven't shared\n  2008:     /// // the `Arc` between threads.\n  2009:     /// assert_eq!(2, Arc::strong_count(&five));\n  2010:     /// ```\n  2011:     #[inline]\n  2012:     #[must_use]\n  2013:     #[stable(feature = \"arc_counts\", since = \"1.15.0\")]\n  2014:     pub fn strong_count(this: &Self) -> usize {\n  2015:         this.inner().strong.load(Relaxed)\n  2016:     }\n  2017: \n  2018:     /// Increments the strong reference count on the `Arc<T>` associated with the\n  2019:     /// provided pointer by one.\n  2020:     ///\n  2021:     /// # Safety\n  2022:     ///\n  2023:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the\n  2024:     /// same layout requirements specified in [`Arc::from_raw_in`][from_raw_in].\n  2025:     /// The associated `Arc` instance must be valid (i.e. the strong count must be at\n  2026:     /// least 1) for the duration of this method, and `ptr` must point to a block of memory\n  2027:     /// allocated by `alloc`.\n  2028:     ///\n  2029:     /// [from_raw_in]: Arc::from_raw_in\n  2030:     ///",
    "nanvix_source": "  2016:     /// let five = Arc::new(5);\n  2017:     /// let _also_five = Arc::clone(&five);\n  2018:     ///\n  2019:     /// // This assertion is deterministic because we haven't shared\n  2020:     /// // the `Arc` between threads.\n  2021:     /// assert_eq!(2, Arc::strong_count(&five));\n  2022:     /// ```\n  2023:     #[inline]\n  2024:     #[must_use]\n  2025:     #[stable(feature = \"arc_counts\", since = \"1.15.0\")]\n  2026:     pub fn strong_count(this: &Self) -> usize {\n  2027:         this.inner().strong.load(Relaxed)\n  2028:     }\n  2029: \n  2030:     /// Increments the strong reference count on the `Arc<T>` associated with the\n  2031:     /// provided pointer by one.\n  2032:     ///\n  2033:     /// # Safety\n  2034:     ///\n  2035:     /// The pointer must have been obtained through `Arc::into_raw` and must satisfy the\n  2036:     /// same layout requirements specified in [`Arc::from_raw_in`][from_raw_in].",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::sync::Arc::try_unwrap",
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
      "name": "try_unwrap",
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
    "verification_source": "  1095:     /// to use the value.\n  1096:     ///\n  1097:     /// # Examples\n  1098:     ///\n  1099:     /// ```\n  1100:     /// use std::sync::Arc;\n  1101:     ///\n  1102:     /// let x = Arc::new(3);\n  1103:     /// assert_eq!(Arc::try_unwrap(x), Ok(3));\n  1104:     ///\n  1105:     /// let x = Arc::new(4);\n  1106:     /// let _y = Arc::clone(&x);\n  1107:     /// assert_eq!(*Arc::try_unwrap(x).unwrap_err(), 4);\n  1108:     /// ```\n  1109:     #[inline]\n  1110:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  1111:     pub fn try_unwrap(this: Self) -> Result<T, Self> {\n  1112:         if this.inner().strong.compare_exchange(1, 0, Relaxed, Relaxed).is_err() {\n  1113:             return Err(this);\n  1114:         }\n  1115: \n  1116:         acquire!(this.inner().strong);\n  1117: \n  1118:         let this = ManuallyDrop::new(this);\n  1119:         let elem: T = unsafe { ptr::read(&this.ptr.as_ref().data) };\n  1120:         let alloc: A = unsafe { ptr::read(&this.alloc) }; // copy the allocator\n  1121: \n  1122:         // Make a weak pointer to clean up the implicit strong-weak reference\n  1123:         let _weak = Weak { ptr: this.ptr, alloc };\n  1124: \n  1125:         Ok(elem)\n  1126:     }\n  1127: ",
    "nanvix_source": "  1105:     ///\n  1106:     /// let x = Arc::new(3);\n  1107:     /// assert_eq!(Arc::try_unwrap(x), Ok(3));\n  1108:     ///\n  1109:     /// let x = Arc::new(4);\n  1110:     /// let _y = Arc::clone(&x);\n  1111:     /// assert_eq!(*Arc::try_unwrap(x).unwrap_err(), 4);\n  1112:     /// ```\n  1113:     #[inline]\n  1114:     #[stable(feature = \"arc_unique\", since = \"1.4.0\")]\n  1115:     pub fn try_unwrap(this: Self) -> Result<T, Self> {\n  1116:         if this.inner().strong.compare_exchange(1, 0, Relaxed, Relaxed).is_err() {\n  1117:             return Err(this);\n  1118:         }\n  1119: \n  1120:         acquire!(this.inner().strong);\n  1121: \n  1122:         let this = ManuallyDrop::new(this);\n  1123:         let elem: T = unsafe { ptr::read(&this.ptr.as_ref().data) };\n  1124:         let alloc: A = unsafe { ptr::read(&this.alloc) }; // copy the allocator\n  1125: ",
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
