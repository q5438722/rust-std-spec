For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashMap::hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
      "name": "hasher",
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
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
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
                          "id": 834,
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
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "S"
            }
          }
        }
      }
    },
    "verification_source": "   864:     }\n   865: \n   866:     /// Returns a reference to the map's [`BuildHasher`].\n   867:     ///\n   868:     /// # Examples\n   869:     ///\n   870:     /// ```\n   871:     /// use std::collections::HashMap;\n   872:     /// use std::hash::RandomState;\n   873:     ///\n   874:     /// let hasher = RandomState::new();\n   875:     /// let map: HashMap<i32, i32> = HashMap::with_hasher(hasher);\n   876:     /// let hasher: &RandomState = map.hasher();\n   877:     /// ```\n   878:     #[inline]\n   879:     #[stable(feature = \"hashmap_public_hasher\", since = \"1.9.0\")]\n   880:     pub fn hasher(&self) -> &S {\n   881:         self.base.hasher()\n   882:     }\n   883: }\n   884: \n   885: impl<K, V, S, A> HashMap<K, V, S, A>\n   886: where\n   887:     K: Eq + Hash,\n   888:     S: BuildHasher,\n   889:     A: Allocator,\n   890: {\n   891:     /// Reserves capacity for at least `additional` more elements to be inserted\n   892:     /// in the `HashMap`. The collection may reserve more space to speculatively\n   893:     /// avoid frequent reallocations. After calling `reserve`,\n   894:     /// capacity will be greater than or equal to `self.len() + additional`.\n   895:     /// Does nothing if capacity is already sufficient.\n   896:     ///",
    "nanvix_source": "   875:     /// ```\n   876:     /// use std::collections::HashMap;\n   877:     /// use std::hash::RandomState;\n   878:     ///\n   879:     /// let hasher = RandomState::new();\n   880:     /// let map: HashMap<i32, i32> = HashMap::with_hasher(hasher);\n   881:     /// let hasher: &RandomState = map.hasher();\n   882:     /// ```\n   883:     #[inline]\n   884:     #[stable(feature = \"hashmap_public_hasher\", since = \"1.9.0\")]\n   885:     pub fn hasher(&self) -> &S {\n   886:         self.base.hasher()\n   887:     }\n   888: }\n   889: \n   890: impl<K, V, S, A> HashMap<K, V, S, A>\n   891: where\n   892:     K: Eq + Hash,\n   893:     S: BuildHasher,\n   894:     A: Allocator,\n   895: {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
        "is_unsafe": false
      },
      "name": "shrink_to",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
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
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "id": 834,
                        "path": "Allocator"
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
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   968:     /// # Examples\n   969:     ///\n   970:     /// ```\n   971:     /// use std::collections::HashMap;\n   972:     ///\n   973:     /// let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   974:     /// map.insert(1, 2);\n   975:     /// map.insert(3, 4);\n   976:     /// assert!(map.capacity() >= 100);\n   977:     /// map.shrink_to(10);\n   978:     /// assert!(map.capacity() >= 10);\n   979:     /// map.shrink_to(0);\n   980:     /// assert!(map.capacity() >= 2);\n   981:     /// ```\n   982:     #[inline]\n   983:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   984:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   985:         self.base.shrink_to(min_capacity);\n   986:     }\n   987: \n   988:     /// Gets the given key's corresponding entry in the map for in-place manipulation.\n   989:     ///\n   990:     /// # Examples\n   991:     ///\n   992:     /// ```\n   993:     /// use std::collections::HashMap;\n   994:     ///\n   995:     /// let mut letters = HashMap::new();\n   996:     ///\n   997:     /// for ch in \"a short treatise on fungi\".chars() {\n   998:     ///     letters.entry(ch).and_modify(|counter| *counter += 1).or_insert(1);\n   999:     /// }\n  1000:     ///",
    "nanvix_source": "   979:     /// map.insert(1, 2);\n   980:     /// map.insert(3, 4);\n   981:     /// assert!(map.capacity() >= 100);\n   982:     /// map.shrink_to(10);\n   983:     /// assert!(map.capacity() >= 10);\n   984:     /// map.shrink_to(0);\n   985:     /// assert!(map.capacity() >= 2);\n   986:     /// ```\n   987:     #[inline]\n   988:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   989:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   990:         self.base.shrink_to(min_capacity);\n   991:     }\n   992: \n   993:     /// Gets the given key's corresponding entry in the map for in-place manipulation.\n   994:     ///\n   995:     /// # Examples\n   996:     ///\n   997:     /// ```\n   998:     /// use std::collections::HashMap;\n   999:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
        "is_unsafe": false
      },
      "name": "shrink_to_fit",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
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
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "id": 834,
                        "path": "Allocator"
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
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
        "output": null
      }
    },
    "verification_source": "   942:     /// and possibly leaving some space in accordance with the resize policy.\n   943:     ///\n   944:     /// # Examples\n   945:     ///\n   946:     /// ```\n   947:     /// use std::collections::HashMap;\n   948:     ///\n   949:     /// let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   950:     /// map.insert(1, 2);\n   951:     /// map.insert(3, 4);\n   952:     /// assert!(map.capacity() >= 100);\n   953:     /// map.shrink_to_fit();\n   954:     /// assert!(map.capacity() >= 2);\n   955:     /// ```\n   956:     #[inline]\n   957:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   958:     pub fn shrink_to_fit(&mut self) {\n   959:         self.base.shrink_to_fit();\n   960:     }\n   961: \n   962:     /// Shrinks the capacity of the map with a lower limit. It will drop\n   963:     /// down no lower than the supplied limit while maintaining the internal rules\n   964:     /// and possibly leaving some space in accordance with the resize policy.\n   965:     ///\n   966:     /// If the current capacity is less than the lower limit, this is a no-op.\n   967:     ///\n   968:     /// # Examples\n   969:     ///\n   970:     /// ```\n   971:     /// use std::collections::HashMap;\n   972:     ///\n   973:     /// let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   974:     /// map.insert(1, 2);",
    "nanvix_source": "   953:     ///\n   954:     /// let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   955:     /// map.insert(1, 2);\n   956:     /// map.insert(3, 4);\n   957:     /// assert!(map.capacity() >= 100);\n   958:     /// map.shrink_to_fit();\n   959:     /// assert!(map.capacity() >= 2);\n   960:     /// ```\n   961:     #[inline]\n   962:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   963:     pub fn shrink_to_fit(&mut self) {\n   964:         self.base.shrink_to_fit();\n   965:     }\n   966: \n   967:     /// Shrinks the capacity of the map with a lower limit. It will drop\n   968:     /// down no lower than the supplied limit while maintaining the internal rules\n   969:     /// and possibly leaving some space in accordance with the resize policy.\n   970:     ///\n   971:     /// If the current capacity is less than the lower limit, this is a no-op.\n   972:     ///\n   973:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
      "name": "try_reserve",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
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
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "id": 834,
                        "path": "Allocator"
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
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
            "additional",
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 874,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   920:     ///\n   921:     /// # Errors\n   922:     ///\n   923:     /// If the capacity overflows, or the allocator reports a failure, then an error\n   924:     /// is returned.\n   925:     ///\n   926:     /// # Examples\n   927:     ///\n   928:     /// ```\n   929:     /// use std::collections::HashMap;\n   930:     ///\n   931:     /// let mut map: HashMap<&str, isize> = HashMap::new();\n   932:     /// map.try_reserve(10).expect(\"why is the test harness OOMing on a handful of bytes?\");\n   933:     /// ```\n   934:     #[inline]\n   935:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n   936:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   937:         self.base.try_reserve(additional).map_err(map_try_reserve_error)\n   938:     }\n   939: \n   940:     /// Shrinks the capacity of the map as much as possible. It will drop\n   941:     /// down as much as possible while maintaining the internal rules\n   942:     /// and possibly leaving some space in accordance with the resize policy.\n   943:     ///\n   944:     /// # Examples\n   945:     ///\n   946:     /// ```\n   947:     /// use std::collections::HashMap;\n   948:     ///\n   949:     /// let mut map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   950:     /// map.insert(1, 2);\n   951:     /// map.insert(3, 4);\n   952:     /// assert!(map.capacity() >= 100);",
    "nanvix_source": "   931:     /// # Examples\n   932:     ///\n   933:     /// ```\n   934:     /// use std::collections::HashMap;\n   935:     ///\n   936:     /// let mut map: HashMap<&str, isize> = HashMap::new();\n   937:     /// map.try_reserve(10).expect(\"why is the test harness OOMing on a handful of bytes?\");\n   938:     /// ```\n   939:     #[inline]\n   940:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n   941:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   942:         self.base.try_reserve(additional).map_err(map_try_reserve_error)\n   943:     }\n   944: \n   945:     /// Shrinks the capacity of the map as much as possible. It will drop\n   946:     /// down as much as possible while maintaining the internal rules\n   947:     /// and possibly leaving some space in accordance with the resize policy.\n   948:     ///\n   949:     /// # Examples\n   950:     ///\n   951:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::with_capacity_and_hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
      "name": "with_capacity_and_hasher",
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:843",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "capacity",
            {
              "primitive": "usize"
            }
          ],
          [
            "hasher",
            {
              "generic": "S"
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        }
      }
    },
    "verification_source": "   385:     /// The `hasher` passed should implement the [`BuildHasher`] trait for\n   386:     /// the `HashMap` to be useful, see its documentation for details.\n   387:     ///\n   388:     /// # Examples\n   389:     ///\n   390:     /// ```\n   391:     /// use std::collections::HashMap;\n   392:     /// use std::hash::RandomState;\n   393:     ///\n   394:     /// let s = RandomState::new();\n   395:     /// let mut map = HashMap::with_capacity_and_hasher(10, s);\n   396:     /// map.insert(1, 2);\n   397:     /// ```\n   398:     #[inline]\n   399:     #[must_use]\n   400:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   401:     pub fn with_capacity_and_hasher(capacity: usize, hasher: S) -> HashMap<K, V, S> {\n   402:         HashMap { base: base::HashMap::with_capacity_and_hasher(capacity, hasher) }\n   403:     }\n   404: }\n   405: \n   406: impl<K, V, S, A: Allocator> HashMap<K, V, S, A> {\n   407:     /// Creates an empty `HashMap` which will use the given hash builder and\n   408:     /// allocator.\n   409:     ///\n   410:     /// The created map has the default initial capacity.\n   411:     ///\n   412:     /// Warning: `hash_builder` is normally randomly generated, and\n   413:     /// is designed to allow HashMaps to be resistant to attacks that\n   414:     /// cause many collisions and very poor performance. Setting it\n   415:     /// manually using this function can expose a DoS attack vector.\n   416:     ///\n   417:     /// The `hash_builder` passed should implement the [`BuildHasher`] trait for",
    "nanvix_source": "   390:     /// use std::collections::HashMap;\n   391:     /// use std::hash::RandomState;\n   392:     ///\n   393:     /// let s = RandomState::new();\n   394:     /// let mut map = HashMap::with_capacity_and_hasher(10, s);\n   395:     /// map.insert(1, 2);\n   396:     /// ```\n   397:     #[inline]\n   398:     #[must_use]\n   399:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   400:     pub fn with_capacity_and_hasher(capacity: usize, hasher: S) -> HashMap<K, V, S> {\n   401:         HashMap { base: base::HashMap::with_capacity_and_hasher(capacity, hasher) }\n   402:     }\n   403: }\n   404: \n   405: impl<K, V, S, A: Allocator> HashMap<K, V, S, A> {\n   406:     /// Creates an empty `HashMap` which will use the given hash builder and\n   407:     /// allocator.\n   408:     ///\n   409:     /// The created map has the default initial capacity.\n   410:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::with_hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "other",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "with_hasher",
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:843",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "hash_builder",
            {
              "generic": "S"
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
          }
        }
      }
    },
    "verification_source": "   353:     /// the `HashMap` to be useful, see its documentation for details.\n   354:     ///\n   355:     /// # Examples\n   356:     ///\n   357:     /// ```\n   358:     /// use std::collections::HashMap;\n   359:     /// use std::hash::RandomState;\n   360:     ///\n   361:     /// let s = RandomState::new();\n   362:     /// let mut map = HashMap::with_hasher(s);\n   363:     /// map.insert(1, 2);\n   364:     /// ```\n   365:     #[inline]\n   366:     #[must_use]\n   367:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   368:     #[rustc_const_stable(feature = \"const_collections_with_hasher\", since = \"1.85.0\")]\n   369:     pub const fn with_hasher(hash_builder: S) -> HashMap<K, V, S> {\n   370:         HashMap { base: base::HashMap::with_hasher(hash_builder) }\n   371:     }\n   372: \n   373:     /// Creates an empty `HashMap` with at least the specified capacity, using\n   374:     /// `hasher` to hash the keys.\n   375:     ///\n   376:     /// The hash map will be able to hold at least `capacity` elements without\n   377:     /// reallocating. This method is allowed to allocate for more elements than\n   378:     /// `capacity`. If `capacity` is zero, the hash map will not allocate.\n   379:     ///\n   380:     /// Warning: `hasher` is normally randomly generated, and\n   381:     /// is designed to allow HashMaps to be resistant to attacks that\n   382:     /// cause many collisions and very poor performance. Setting it\n   383:     /// manually using this function can expose a DoS attack vector.\n   384:     ///\n   385:     /// The `hasher` passed should implement the [`BuildHasher`] trait for",
    "nanvix_source": "   358:     /// use std::hash::RandomState;\n   359:     ///\n   360:     /// let s = RandomState::new();\n   361:     /// let mut map = HashMap::with_hasher(s);\n   362:     /// map.insert(1, 2);\n   363:     /// ```\n   364:     #[inline]\n   365:     #[must_use]\n   366:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   367:     #[rustc_const_stable(feature = \"const_collections_with_hasher\", since = \"1.85.0\")]\n   368:     pub const fn with_hasher(hash_builder: S) -> HashMap<K, V, S> {\n   369:         HashMap { base: base::HashMap::with_hasher(hash_builder) }\n   370:     }\n   371: \n   372:     /// Creates an empty `HashMap` with at least the specified capacity, using\n   373:     /// `hasher` to hash the keys.\n   374:     ///\n   375:     /// The hash map will be able to hold at least `capacity` elements without\n   376:     /// reallocating. This method is allowed to allocate for more elements than\n   377:     /// `capacity`. If `capacity` is zero, the hash map will not allocate.\n   378:     ///",
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
