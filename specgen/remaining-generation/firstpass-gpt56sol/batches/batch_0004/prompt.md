For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BTreeMap::first_entry",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "first_entry",
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
                                "lifetime": "'_"
                              },
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
                        "id": 1265,
                        "path": "OccupiedEntry"
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
    "verification_source": "   822:     ///\n   823:     /// ```\n   824:     /// use std::collections::BTreeMap;\n   825:     ///\n   826:     /// let mut map = BTreeMap::new();\n   827:     /// map.insert(1, \"a\");\n   828:     /// map.insert(2, \"b\");\n   829:     /// if let Some(mut entry) = map.first_entry() {\n   830:     ///     if *entry.key() > 0 {\n   831:     ///         entry.insert(\"first\");\n   832:     ///     }\n   833:     /// }\n   834:     /// assert_eq!(*map.get(&1).unwrap(), \"first\");\n   835:     /// assert_eq!(*map.get(&2).unwrap(), \"b\");\n   836:     /// ```\n   837:     #[stable(feature = \"map_first_last\", since = \"1.66.0\")]\n   838:     pub fn first_entry(&mut self) -> Option<OccupiedEntry<'_, K, V, A>>\n   839:     where\n   840:         K: Ord,\n   841:     {\n   842:         let (map, dormant_map) = DormantMutRef::new(self);\n   843:         let root_node = map.root.as_mut()?.borrow_mut();\n   844:         let kv = root_node.first_leaf_edge().right_kv().ok()?;\n   845:         Some(OccupiedEntry {\n   846:             handle: kv.forget_node_type(),\n   847:             dormant_map,\n   848:             alloc: (*map.alloc).clone(),\n   849:             _marker: PhantomData,\n   850:         })\n   851:     }\n   852: \n   853:     /// Removes and returns the first element in the map.\n   854:     /// The key of this element is the minimum key that was in the map.",
    "nanvix_source": "   828:     /// map.insert(2, \"b\");\n   829:     /// if let Some(mut entry) = map.first_entry() {\n   830:     ///     if *entry.key() > 0 {\n   831:     ///         entry.insert(\"first\");\n   832:     ///     }\n   833:     /// }\n   834:     /// assert_eq!(*map.get(&1).unwrap(), \"first\");\n   835:     /// assert_eq!(*map.get(&2).unwrap(), \"b\");\n   836:     /// ```\n   837:     #[stable(feature = \"map_first_last\", since = \"1.66.0\")]\n   838:     pub fn first_entry(&mut self) -> Option<OccupiedEntry<'_, K, V, A>>\n   839:     where\n   840:         K: Ord,\n   841:     {\n   842:         let (map, dormant_map) = DormantMutRef::new(self);\n   843:         let root_node = map.root.as_mut()?.borrow_mut();\n   844:         let kv = root_node.first_leaf_edge().right_kv().ok()?;\n   845:         Some(OccupiedEntry {\n   846:             handle: kv.forget_node_type(),\n   847:             dormant_map,\n   848:             alloc: (*map.alloc).clone(),",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BTreeMap::last_entry",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "last_entry",
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
                                "lifetime": "'_"
                              },
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
                        "id": 1265,
                        "path": "OccupiedEntry"
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
    "verification_source": "   905:     ///\n   906:     /// ```\n   907:     /// use std::collections::BTreeMap;\n   908:     ///\n   909:     /// let mut map = BTreeMap::new();\n   910:     /// map.insert(1, \"a\");\n   911:     /// map.insert(2, \"b\");\n   912:     /// if let Some(mut entry) = map.last_entry() {\n   913:     ///     if *entry.key() > 0 {\n   914:     ///         entry.insert(\"last\");\n   915:     ///     }\n   916:     /// }\n   917:     /// assert_eq!(*map.get(&1).unwrap(), \"a\");\n   918:     /// assert_eq!(*map.get(&2).unwrap(), \"last\");\n   919:     /// ```\n   920:     #[stable(feature = \"map_first_last\", since = \"1.66.0\")]\n   921:     pub fn last_entry(&mut self) -> Option<OccupiedEntry<'_, K, V, A>>\n   922:     where\n   923:         K: Ord,\n   924:     {\n   925:         let (map, dormant_map) = DormantMutRef::new(self);\n   926:         let root_node = map.root.as_mut()?.borrow_mut();\n   927:         let kv = root_node.last_leaf_edge().left_kv().ok()?;\n   928:         Some(OccupiedEntry {\n   929:             handle: kv.forget_node_type(),\n   930:             dormant_map,\n   931:             alloc: (*map.alloc).clone(),\n   932:             _marker: PhantomData,\n   933:         })\n   934:     }\n   935: \n   936:     /// Removes and returns the last element in the map.\n   937:     /// The key of this element is the maximum key that was in the map.",
    "nanvix_source": "   911:     /// map.insert(2, \"b\");\n   912:     /// if let Some(mut entry) = map.last_entry() {\n   913:     ///     if *entry.key() > 0 {\n   914:     ///         entry.insert(\"last\");\n   915:     ///     }\n   916:     /// }\n   917:     /// assert_eq!(*map.get(&1).unwrap(), \"a\");\n   918:     /// assert_eq!(*map.get(&2).unwrap(), \"last\");\n   919:     /// ```\n   920:     #[stable(feature = \"map_first_last\", since = \"1.66.0\")]\n   921:     pub fn last_entry(&mut self) -> Option<OccupiedEntry<'_, K, V, A>>\n   922:     where\n   923:         K: Ord,\n   924:     {\n   925:         let (map, dormant_map) = DormantMutRef::new(self);\n   926:         let root_node = map.root.as_mut()?.borrow_mut();\n   927:         let kv = root_node.last_leaf_edge().left_kv().ok()?;\n   928:         Some(OccupiedEntry {\n   929:             handle: kv.forget_node_type(),\n   930:             dormant_map,\n   931:             alloc: (*map.alloc).clone(),",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf16",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u16"
                  }
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
                      "resolved_path": {
                        "args": null,
                        "id": 119,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 4036,
                        "path": "FromUtf16Error"
                      }
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
    "verification_source": "   700:     /// # Examples\n   701:     ///\n   702:     /// ```\n   703:     /// // \ud834\udd1emusic\n   704:     /// let v = &[0xD834, 0xDD1E, 0x006d, 0x0075,\n   705:     ///           0x0073, 0x0069, 0x0063];\n   706:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   707:     ///            String::from_utf16(v).unwrap());\n   708:     ///\n   709:     /// // \ud834\udd1emu<invalid>ic\n   710:     /// let v = &[0xD834, 0xDD1E, 0x006d, 0x0075,\n   711:     ///           0xD800, 0x0069, 0x0063];\n   712:     /// assert!(String::from_utf16(v).is_err());\n   713:     /// ```\n   714:     #[cfg(not(no_global_oom_handling))]\n   715:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   716:     pub fn from_utf16(v: &[u16]) -> Result<String, FromUtf16Error> {\n   717:         // This isn't done via collect::<Result<_, _>>() for performance reasons.\n   718:         // FIXME: the function can be simplified again when #48994 is closed.\n   719:         let mut ret = String::with_capacity(v.len());\n   720:         for c in char::decode_utf16(v.iter().cloned()) {\n   721:             let Ok(c) = c else {\n   722:                 return Err(FromUtf16Error(()));\n   723:             };\n   724:             ret.push(c);\n   725:         }\n   726:         Ok(ret)\n   727:     }\n   728: \n   729:     /// Decode a native endian UTF-16\u2013encoded slice `v` into a `String`,\n   730:     /// replacing invalid data with [the replacement character (`U+FFFD`)][U+FFFD].\n   731:     ///\n   732:     /// Unlike [`from_utf8_lossy`] which returns a [`Cow<'a, str>`],",
    "nanvix_source": "   715:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   716:     ///            String::from_utf16(v).unwrap());\n   717:     ///\n   718:     /// // \ud834\udd1emu<invalid>ic\n   719:     /// let v = &[0xD834, 0xDD1E, 0x006d, 0x0075,\n   720:     ///           0xD800, 0x0069, 0x0063];\n   721:     /// assert!(String::from_utf16(v).is_err());\n   722:     /// ```\n   723:     #[cfg(not(no_global_oom_handling))]\n   724:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   725:     pub fn from_utf16(v: &[u16]) -> Result<String, FromUtf16Error> {\n   726:         // This isn't done via collect::<Result<_, _>>() for performance reasons.\n   727:         // FIXME: the function can be simplified again when #48994 is closed.\n   728:         let mut ret = String::with_capacity(v.len());\n   729:         for c in char::decode_utf16(v.iter().cloned()) {\n   730:             let Ok(c) = c else {\n   731:                 return Err(FromUtf16Error { kind: FromUtf16ErrorKind::LoneSurrogate });\n   732:             };\n   733:             ret.push(c);\n   734:         }\n   735:         Ok(ret)",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf16_lossy",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16_lossy",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u16"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   739:     ///\n   740:     /// # Examples\n   741:     ///\n   742:     /// ```\n   743:     /// // \ud834\udd1emus<invalid>ic<invalid>\n   744:     /// let v = &[0xD834, 0xDD1E, 0x006d, 0x0075,\n   745:     ///           0x0073, 0xDD1E, 0x0069, 0x0063,\n   746:     ///           0xD834];\n   747:     ///\n   748:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   749:     ///            String::from_utf16_lossy(v));\n   750:     /// ```\n   751:     #[cfg(not(no_global_oom_handling))]\n   752:     #[must_use]\n   753:     #[inline]\n   754:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   755:     pub fn from_utf16_lossy(v: &[u16]) -> String {\n   756:         char::decode_utf16(v.iter().cloned())\n   757:             .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   758:             .collect()\n   759:     }\n   760: \n   761:     /// Decode a UTF-16LE\u2013encoded vector `v` into a `String`,\n   762:     /// returning [`Err`] if `v` contains any invalid data.\n   763:     ///\n   764:     /// # Examples\n   765:     ///\n   766:     /// Basic usage:\n   767:     ///\n   768:     /// ```\n   769:     /// #![feature(str_from_utf16_endian)]\n   770:     /// // \ud834\udd1emusic\n   771:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,",
    "nanvix_source": "   754:     ///           0x0073, 0xDD1E, 0x0069, 0x0063,\n   755:     ///           0xD834];\n   756:     ///\n   757:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   758:     ///            String::from_utf16_lossy(v));\n   759:     /// ```\n   760:     #[cfg(not(no_global_oom_handling))]\n   761:     #[must_use]\n   762:     #[inline]\n   763:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   764:     pub fn from_utf16_lossy(v: &[u16]) -> String {\n   765:         char::decode_utf16(v.iter().cloned())\n   766:             .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   767:             .collect()\n   768:     }\n   769: \n   770:     /// Decode a UTF-16LE\u2013encoded vector `v` into a `String`,\n   771:     /// returning [`Err`] if `v` contains any invalid data.\n   772:     ///\n   773:     /// # Examples\n   774:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf16be",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16be",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
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
                      "resolved_path": {
                        "args": null,
                        "id": 119,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 4036,
                        "path": "FromUtf16Error"
                      }
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
    "verification_source": "   842:     ///\n   843:     /// ```\n   844:     /// #![feature(str_from_utf16_endian)]\n   845:     /// // \ud834\udd1emusic\n   846:     /// let v = &[0xD8, 0x34, 0xDD, 0x1E, 0x00, 0x6d, 0x00, 0x75,\n   847:     ///           0x00, 0x73, 0x00, 0x69, 0x00, 0x63];\n   848:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   849:     ///            String::from_utf16be(v).unwrap());\n   850:     ///\n   851:     /// // \ud834\udd1emu<invalid>ic\n   852:     /// let v = &[0xD8, 0x34, 0xDD, 0x1E, 0x00, 0x6d, 0x00, 0x75,\n   853:     ///           0xD8, 0x00, 0x00, 0x69, 0x00, 0x63];\n   854:     /// assert!(String::from_utf16be(v).is_err());\n   855:     /// ```\n   856:     #[cfg(not(no_global_oom_handling))]\n   857:     #[unstable(feature = \"str_from_utf16_endian\", issue = \"116258\")]\n   858:     pub fn from_utf16be(v: &[u8]) -> Result<String, FromUtf16Error> {\n   859:         let (chunks, []) = v.as_chunks::<2>() else {\n   860:             return Err(FromUtf16Error(()));\n   861:         };\n   862:         match (cfg!(target_endian = \"big\"), unsafe { v.align_to::<u16>() }) {\n   863:             (true, ([], v, [])) => Self::from_utf16(v),\n   864:             _ => char::decode_utf16(chunks.iter().copied().map(u16::from_be_bytes))\n   865:                 .collect::<Result<_, _>>()\n   866:                 .map_err(|_| FromUtf16Error(())),\n   867:         }\n   868:     }\n   869: \n   870:     /// Decode a UTF-16BE\u2013encoded slice `v` into a `String`, replacing\n   871:     /// invalid data with [the replacement character (`U+FFFD`)][U+FFFD].\n   872:     ///\n   873:     /// Unlike [`from_utf8_lossy`] which returns a [`Cow<'a, str>`],\n   874:     /// `from_utf16le_lossy` returns a `String` since the UTF-16 to UTF-8",
    "nanvix_source": "   854:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   855:     ///            String::from_utf16be(v).unwrap());\n   856:     ///\n   857:     /// // \ud834\udd1emu<invalid>ic\n   858:     /// let v = &[0xD8, 0x34, 0xDD, 0x1E, 0x00, 0x6d, 0x00, 0x75,\n   859:     ///           0xD8, 0x00, 0x00, 0x69, 0x00, 0x63];\n   860:     /// assert!(String::from_utf16be(v).is_err());\n   861:     /// ```\n   862:     #[cfg(not(no_global_oom_handling))]\n   863:     #[stable(feature = \"str_from_utf16_endian\", since = \"CURRENT_RUSTC_VERSION\")]\n   864:     pub fn from_utf16be(v: &[u8]) -> Result<String, FromUtf16Error> {\n   865:         let (chunks, []) = v.as_chunks::<2>() else {\n   866:             return Err(FromUtf16Error { kind: FromUtf16ErrorKind::OddBytes });\n   867:         };\n   868:         match (cfg!(target_endian = \"big\"), unsafe { v.align_to::<u16>() }) {\n   869:             (true, ([], v, [])) => Self::from_utf16(v),\n   870:             _ => char::decode_utf16(chunks.iter().copied().map(u16::from_be_bytes))\n   871:                 .collect::<Result<_, _>>()\n   872:                 .map_err(|_| FromUtf16Error { kind: FromUtf16ErrorKind::LoneSurrogate }),\n   873:         }\n   874:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf16be_lossy",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16be_lossy",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   881:     /// # Examples\n   882:     ///\n   883:     /// Basic usage:\n   884:     ///\n   885:     /// ```\n   886:     /// #![feature(str_from_utf16_endian)]\n   887:     /// // \ud834\udd1emus<invalid>ic<invalid>\n   888:     /// let v = &[0xD8, 0x34, 0xDD, 0x1E, 0x00, 0x6d, 0x00, 0x75,\n   889:     ///           0x00, 0x73, 0xDD, 0x1E, 0x00, 0x69, 0x00, 0x63,\n   890:     ///           0xD8, 0x34];\n   891:     ///\n   892:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   893:     ///            String::from_utf16be_lossy(v));\n   894:     /// ```\n   895:     #[cfg(not(no_global_oom_handling))]\n   896:     #[unstable(feature = \"str_from_utf16_endian\", issue = \"116258\")]\n   897:     pub fn from_utf16be_lossy(v: &[u8]) -> String {\n   898:         match (cfg!(target_endian = \"big\"), unsafe { v.align_to::<u16>() }) {\n   899:             (true, ([], v, [])) => Self::from_utf16_lossy(v),\n   900:             (true, ([], v, [_remainder])) => Self::from_utf16_lossy(v) + \"\\u{FFFD}\",\n   901:             _ => {\n   902:                 let (chunks, remainder) = v.as_chunks::<2>();\n   903:                 let string = char::decode_utf16(chunks.iter().copied().map(u16::from_be_bytes))\n   904:                     .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   905:                     .collect();\n   906:                 if remainder.is_empty() { string } else { string + \"\\u{FFFD}\" }\n   907:             }\n   908:         }\n   909:     }\n   910: \n   911:     /// Decomposes a `String` into its raw components: `(pointer, length, capacity)`.\n   912:     ///\n   913:     /// Returns the raw pointer to the underlying data, the length of",
    "nanvix_source": "   892:     /// // \ud834\udd1emus<invalid>ic<invalid>\n   893:     /// let v = &[0xD8, 0x34, 0xDD, 0x1E, 0x00, 0x6d, 0x00, 0x75,\n   894:     ///           0x00, 0x73, 0xDD, 0x1E, 0x00, 0x69, 0x00, 0x63,\n   895:     ///           0xD8, 0x34];\n   896:     ///\n   897:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   898:     ///            String::from_utf16be_lossy(v));\n   899:     /// ```\n   900:     #[cfg(not(no_global_oom_handling))]\n   901:     #[stable(feature = \"str_from_utf16_endian\", since = \"CURRENT_RUSTC_VERSION\")]\n   902:     pub fn from_utf16be_lossy(v: &[u8]) -> String {\n   903:         match (cfg!(target_endian = \"big\"), unsafe { v.align_to::<u16>() }) {\n   904:             (true, ([], v, [])) => Self::from_utf16_lossy(v),\n   905:             (true, ([], v, [_remainder])) => Self::from_utf16_lossy(v) + \"\\u{FFFD}\",\n   906:             _ => {\n   907:                 let (chunks, remainder) = v.as_chunks::<2>();\n   908:                 let string = char::decode_utf16(chunks.iter().copied().map(u16::from_be_bytes))\n   909:                     .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   910:                     .collect();\n   911:                 if remainder.is_empty() { string } else { string + \"\\u{FFFD}\" }\n   912:             }",
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
