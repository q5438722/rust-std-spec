For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::borrow::Cow::to_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "to_mut",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "B"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 129,
            "path": "Cow"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 26,
                          "path": "ToOwned"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "B"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:134",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:129",
        "resolved_owner_path": [
          "alloc",
          "borrow",
          "Cow"
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
              "qualified_path": {
                "args": null,
                "name": "Owned",
                "self_type": {
                  "generic": "B"
                },
                "trait": {
                  "args": null,
                  "id": 26,
                  "path": "ToOwned"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   267:     /// Clones the data if it is not already owned.\n   268:     ///\n   269:     /// # Examples\n   270:     ///\n   271:     /// ```\n   272:     /// use std::borrow::Cow;\n   273:     ///\n   274:     /// let mut cow = Cow::Borrowed(\"foo\");\n   275:     /// cow.to_mut().make_ascii_uppercase();\n   276:     ///\n   277:     /// assert_eq!(\n   278:     ///   cow,\n   279:     ///   Cow::Owned(String::from(\"FOO\")) as Cow<'_, str>\n   280:     /// );\n   281:     /// ```\n   282:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   283:     pub fn to_mut(&mut self) -> &mut <B as ToOwned>::Owned {\n   284:         match *self {\n   285:             Borrowed(borrowed) => {\n   286:                 *self = Owned(borrowed.to_owned());\n   287:                 match *self {\n   288:                     Borrowed(..) => unreachable!(),\n   289:                     Owned(ref mut owned) => owned,\n   290:                 }\n   291:             }\n   292:             Owned(ref mut owned) => owned,\n   293:         }\n   294:     }\n   295: \n   296:     /// Extracts the owned data.\n   297:     ///\n   298:     /// Clones the data if it is not already owned.\n   299:     ///",
    "nanvix_source": "   273:     ///\n   274:     /// let mut cow = Cow::Borrowed(\"foo\");\n   275:     /// cow.to_mut().make_ascii_uppercase();\n   276:     ///\n   277:     /// assert_eq!(\n   278:     ///   cow,\n   279:     ///   Cow::Owned(String::from(\"FOO\")) as Cow<'_, str>\n   280:     /// );\n   281:     /// ```\n   282:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   283:     pub fn to_mut(&mut self) -> &mut <B as ToOwned>::Owned {\n   284:         match *self {\n   285:             Borrowed(borrowed) => {\n   286:                 *self = Owned(borrowed.to_owned());\n   287:                 match *self {\n   288:                     Borrowed(..) => unreachable!(),\n   289:                     Owned(ref mut owned) => owned,\n   290:                 }\n   291:             }\n   292:             Owned(ref mut owned) => owned,\n   293:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::leak",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "outlives": "'a"
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
      "name": "leak",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
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
            "b",
            {
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1852:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  1853:     /// ```\n  1854:     ///\n  1855:     /// Unsized data:\n  1856:     ///\n  1857:     /// ```\n  1858:     /// let x = vec![1, 2, 3].into_boxed_slice();\n  1859:     /// let static_ref = Box::leak(x);\n  1860:     /// static_ref[0] = 4;\n  1861:     /// assert_eq!(*static_ref, [4, 2, 3]);\n  1862:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  1863:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  1864:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  1865:     /// ```\n  1866:     #[stable(feature = \"box_leak\", since = \"1.26.0\")]\n  1867:     #[inline]\n  1868:     pub fn leak<'a>(b: Self) -> &'a mut T\n  1869:     where\n  1870:         A: 'a,\n  1871:     {\n  1872:         let (ptr, alloc) = Box::into_raw_with_allocator(b);\n  1873:         mem::forget(alloc);\n  1874:         unsafe { &mut *ptr }\n  1875:     }\n  1876: \n  1877:     /// Converts a `Box<T>` into a `Pin<Box<T>>`. If `T` does not implement [`Unpin`], then\n  1878:     /// `*boxed` will be pinned in memory and unable to be moved.\n  1879:     ///\n  1880:     /// This conversion does not allocate on the heap and happens in place.\n  1881:     ///\n  1882:     /// This is also available via [`From`].\n  1883:     ///\n  1884:     /// Constructing and pinning a `Box` with <code>Box::into_pin([Box::new]\\(x))</code>",
    "nanvix_source": "  1930:     /// let x = vec![1, 2, 3].into_boxed_slice();\n  1931:     /// let static_ref = Box::leak(x);\n  1932:     /// static_ref[0] = 4;\n  1933:     /// assert_eq!(*static_ref, [4, 2, 3]);\n  1934:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  1935:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  1936:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  1937:     /// ```\n  1938:     #[stable(feature = \"box_leak\", since = \"1.26.0\")]\n  1939:     #[inline]\n  1940:     pub fn leak<'a>(b: Self) -> &'a mut T\n  1941:     where\n  1942:         A: 'a,\n  1943:     {\n  1944:         let (ptr, alloc) = Box::into_raw_with_allocator(b);\n  1945:         mem::forget(alloc);\n  1946:         unsafe { &mut *ptr }\n  1947:     }\n  1948: \n  1949:     /// Converts a `Box<T>` into a `Pin<Box<T>>`. If `T` does not implement [`Unpin`], then\n  1950:     /// `*boxed` will be pinned in memory and unable to be moved.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
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
            "name": "Q"
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Q"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 30,
                      "path": "Borrow"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 176,
                      "path": "Ord"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 176,
                      "path": "Ord"
                    }
                  }
                },
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
              "generic_params": [],
              "type": {
                "generic": "Q"
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
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
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
            "id": 1268,
            "path": "BTreeMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
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
                    },
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
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:1419",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1268",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "BTreeMap"
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
          ],
          [
            "key",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
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
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "V"
                        }
                      }
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
    "verification_source": "   990:     /// on the borrowed form *must* match the ordering on the key type.\n   991:     ///\n   992:     /// # Examples\n   993:     ///\n   994:     /// ```\n   995:     /// use std::collections::BTreeMap;\n   996:     ///\n   997:     /// let mut map = BTreeMap::new();\n   998:     /// map.insert(1, \"a\");\n   999:     /// if let Some(x) = map.get_mut(&1) {\n  1000:     ///     *x = \"b\";\n  1001:     /// }\n  1002:     /// assert_eq!(map[&1], \"b\");\n  1003:     /// ```\n  1004:     // See `get` for implementation notes, this is basically a copy-paste with mut's added\n  1005:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1006:     pub fn get_mut<Q: ?Sized>(&mut self, key: &Q) -> Option<&mut V>\n  1007:     where\n  1008:         K: Borrow<Q> + Ord,\n  1009:         Q: Ord,\n  1010:     {\n  1011:         let root_node = self.root.as_mut()?.borrow_mut();\n  1012:         match root_node.search_tree(key) {\n  1013:             Found(handle) => Some(handle.into_val_mut()),\n  1014:             GoDown(_) => None,\n  1015:         }\n  1016:     }\n  1017: \n  1018:     /// Inserts a key-value pair into the map.\n  1019:     ///\n  1020:     /// If the map did not have this key present, `None` is returned.\n  1021:     ///\n  1022:     /// If the map did have this key present, the value is updated, and the old",
    "nanvix_source": "   996:     ///\n   997:     /// let mut map = BTreeMap::new();\n   998:     /// map.insert(1, \"a\");\n   999:     /// if let Some(x) = map.get_mut(&1) {\n  1000:     ///     *x = \"b\";\n  1001:     /// }\n  1002:     /// assert_eq!(map[&1], \"b\");\n  1003:     /// ```\n  1004:     // See `get` for implementation notes, this is basically a copy-paste with mut's added\n  1005:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1006:     pub fn get_mut<Q: ?Sized>(&mut self, key: &Q) -> Option<&mut V>\n  1007:     where\n  1008:         K: Borrow<Q> + Ord,\n  1009:         Q: Ord,\n  1010:     {\n  1011:         let root_node = self.root.as_mut()?.borrow_mut();\n  1012:         match root_node.search_tree(key) {\n  1013:             Found(handle) => Some(handle.into_val_mut()),\n  1014:             GoDown(_) => None,\n  1015:         }\n  1016:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::back_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "back_mut",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
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
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   808:     /// use std::collections::LinkedList;\n   809:     ///\n   810:     /// let mut dl = LinkedList::new();\n   811:     /// assert_eq!(dl.back(), None);\n   812:     ///\n   813:     /// dl.push_back(1);\n   814:     /// assert_eq!(dl.back(), Some(&1));\n   815:     ///\n   816:     /// match dl.back_mut() {\n   817:     ///     None => {},\n   818:     ///     Some(x) => *x = 5,\n   819:     /// }\n   820:     /// assert_eq!(dl.back(), Some(&5));\n   821:     /// ```\n   822:     #[inline]\n   823:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   824:     pub fn back_mut(&mut self) -> Option<&mut T> {\n   825:         unsafe { self.tail.as_mut().map(|node| &mut node.as_mut().element) }\n   826:     }\n   827: \n   828:     /// Adds an element to the front of the list.\n   829:     ///\n   830:     /// This operation should compute in *O*(1) time.\n   831:     ///\n   832:     /// # Examples\n   833:     ///\n   834:     /// ```\n   835:     /// use std::collections::LinkedList;\n   836:     ///\n   837:     /// let mut dl = LinkedList::new();\n   838:     ///\n   839:     /// dl.push_front(2);\n   840:     /// assert_eq!(dl.front().unwrap(), &2);",
    "nanvix_source": "   814:     /// assert_eq!(dl.back(), Some(&1));\n   815:     ///\n   816:     /// match dl.back_mut() {\n   817:     ///     None => {},\n   818:     ///     Some(x) => *x = 5,\n   819:     /// }\n   820:     /// assert_eq!(dl.back(), Some(&5));\n   821:     /// ```\n   822:     #[inline]\n   823:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   824:     pub fn back_mut(&mut self) -> Option<&mut T> {\n   825:         unsafe { self.tail.as_mut().map(|node| &mut node.as_mut().element) }\n   826:     }\n   827: \n   828:     /// Adds an element to the front of the list.\n   829:     ///\n   830:     /// This operation should compute in *O*(1) time.\n   831:     ///\n   832:     /// # Examples\n   833:     ///\n   834:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::front_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "front_mut",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
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
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   757:     ///\n   758:     /// let mut dl = LinkedList::new();\n   759:     /// assert_eq!(dl.front(), None);\n   760:     ///\n   761:     /// dl.push_front(1);\n   762:     /// assert_eq!(dl.front(), Some(&1));\n   763:     ///\n   764:     /// match dl.front_mut() {\n   765:     ///     None => {},\n   766:     ///     Some(x) => *x = 5,\n   767:     /// }\n   768:     /// assert_eq!(dl.front(), Some(&5));\n   769:     /// ```\n   770:     #[inline]\n   771:     #[must_use]\n   772:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   773:     pub fn front_mut(&mut self) -> Option<&mut T> {\n   774:         unsafe { self.head.as_mut().map(|node| &mut node.as_mut().element) }\n   775:     }\n   776: \n   777:     /// Provides a reference to the back element, or `None` if the list is\n   778:     /// empty.\n   779:     ///\n   780:     /// This operation should compute in *O*(1) time.\n   781:     ///\n   782:     /// # Examples\n   783:     ///\n   784:     /// ```\n   785:     /// use std::collections::LinkedList;\n   786:     ///\n   787:     /// let mut dl = LinkedList::new();\n   788:     /// assert_eq!(dl.back(), None);\n   789:     ///",
    "nanvix_source": "   763:     ///\n   764:     /// match dl.front_mut() {\n   765:     ///     None => {},\n   766:     ///     Some(x) => *x = 5,\n   767:     /// }\n   768:     /// assert_eq!(dl.front(), Some(&5));\n   769:     /// ```\n   770:     #[inline]\n   771:     #[must_use]\n   772:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   773:     pub fn front_mut(&mut self) -> Option<&mut T> {\n   774:         unsafe { self.head.as_mut().map(|node| &mut node.as_mut().element) }\n   775:     }\n   776: \n   777:     /// Provides a reference to the back element, or `None` if the list is\n   778:     /// empty.\n   779:     ///\n   780:     /// This operation should compute in *O*(1) time.\n   781:     ///\n   782:     /// # Examples\n   783:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::push_back_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "push_back_mut",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
          ],
          [
            "elt",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   922:     ///\n   923:     /// This operation should compute in *O*(1) time.\n   924:     ///\n   925:     /// # Examples\n   926:     ///\n   927:     /// ```\n   928:     /// use std::collections::LinkedList;\n   929:     ///\n   930:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   931:     ///\n   932:     /// let ptr = dl.push_back_mut(2);\n   933:     /// *ptr += 4;\n   934:     /// assert_eq!(dl.back().unwrap(), &6);\n   935:     /// ```\n   936:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n   937:     #[must_use = \"if you don't need a reference to the value, use `LinkedList::push_back` instead\"]\n   938:     pub fn push_back_mut(&mut self, elt: T) -> &mut T {\n   939:         let mut node =\n   940:             Box::into_non_null_with_allocator(Box::new_in(Node::new(elt), &self.alloc)).0;\n   941:         // SAFETY: node is a unique pointer to a node in self.alloc\n   942:         unsafe {\n   943:             self.push_back_node(node);\n   944:             &mut node.as_mut().element\n   945:         }\n   946:     }\n   947: \n   948:     /// Removes the last element from a list and returns it, or `None` if\n   949:     /// it is empty.\n   950:     ///\n   951:     /// This operation should compute in *O*(1) time.\n   952:     ///\n   953:     /// # Examples\n   954:     ///",
    "nanvix_source": "   928:     /// use std::collections::LinkedList;\n   929:     ///\n   930:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   931:     ///\n   932:     /// let ptr = dl.push_back_mut(2);\n   933:     /// *ptr += 4;\n   934:     /// assert_eq!(dl.back().unwrap(), &6);\n   935:     /// ```\n   936:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n   937:     #[must_use = \"if you don't need a reference to the value, use `LinkedList::push_back` instead\"]\n   938:     pub fn push_back_mut(&mut self, elt: T) -> &mut T {\n   939:         let mut node =\n   940:             Box::into_non_null_with_allocator(Box::new_in(Node::new(elt), &self.alloc)).0;\n   941:         // SAFETY: node is a unique pointer to a node in self.alloc\n   942:         unsafe {\n   943:             self.push_back_node(node);\n   944:             &mut node.as_mut().element\n   945:         }\n   946:     }\n   947: \n   948:     /// Removes the last element from a list and returns it, or `None` if",
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
