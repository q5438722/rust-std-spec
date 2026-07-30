For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Formatter::debug_list",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
            "name": "'b"
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
      "name": "debug_list",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                "lifetime": "'b",
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
                    "lifetime": "'b"
                  },
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13423,
            "path": "DebugList"
          }
        }
      }
    },
    "verification_source": "  2721:     /// # Examples\n  2722:     ///\n  2723:     /// ```rust\n  2724:     /// use std::fmt;\n  2725:     ///\n  2726:     /// struct Foo(Vec<i32>);\n  2727:     ///\n  2728:     /// impl fmt::Debug for Foo {\n  2729:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2730:     ///         fmt.debug_list().entries(self.0.iter()).finish()\n  2731:     ///     }\n  2732:     /// }\n  2733:     ///\n  2734:     /// assert_eq!(format!(\"{:?}\", Foo(vec![10, 11])), \"[10, 11]\");\n  2735:     /// ```\n  2736:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2737:     pub fn debug_list<'b>(&'b mut self) -> DebugList<'b, 'a> {\n  2738:         builders::debug_list_new(self)\n  2739:     }\n  2740: \n  2741:     /// Creates a `DebugSet` builder designed to assist with creation of\n  2742:     /// `fmt::Debug` implementations for set-like structures.\n  2743:     ///\n  2744:     /// # Examples\n  2745:     ///\n  2746:     /// ```rust\n  2747:     /// use std::fmt;\n  2748:     ///\n  2749:     /// struct Foo(Vec<i32>);\n  2750:     ///\n  2751:     /// impl fmt::Debug for Foo {\n  2752:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2753:     ///         fmt.debug_set().entries(self.0.iter()).finish()",
    "nanvix_source": "  2727:     ///\n  2728:     /// impl fmt::Debug for Foo {\n  2729:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2730:     ///         fmt.debug_list().entries(self.0.iter()).finish()\n  2731:     ///     }\n  2732:     /// }\n  2733:     ///\n  2734:     /// assert_eq!(format!(\"{:?}\", Foo(vec![10, 11])), \"[10, 11]\");\n  2735:     /// ```\n  2736:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2737:     pub fn debug_list<'b>(&'b mut self) -> DebugList<'b, 'a> {\n  2738:         builders::debug_list_new(self)\n  2739:     }\n  2740: \n  2741:     /// Creates a `DebugSet` builder designed to assist with creation of\n  2742:     /// `fmt::Debug` implementations for set-like structures.\n  2743:     ///\n  2744:     /// # Examples\n  2745:     ///\n  2746:     /// ```rust\n  2747:     /// use std::fmt;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::debug_map",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
            "name": "'b"
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
      "name": "debug_map",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                "lifetime": "'b",
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
                    "lifetime": "'b"
                  },
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13425,
            "path": "DebugMap"
          }
        }
      }
    },
    "verification_source": "  2805:     /// use std::fmt;\n  2806:     ///\n  2807:     /// struct Foo(Vec<(String, i32)>);\n  2808:     ///\n  2809:     /// impl fmt::Debug for Foo {\n  2810:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2811:     ///         fmt.debug_map().entries(self.0.iter().map(|&(ref k, ref v)| (k, v))).finish()\n  2812:     ///     }\n  2813:     /// }\n  2814:     ///\n  2815:     /// assert_eq!(\n  2816:     ///     format!(\"{:?}\",  Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  2817:     ///     r#\"{\"A\": 10, \"B\": 11}\"#\n  2818:     ///  );\n  2819:     /// ```\n  2820:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2821:     pub fn debug_map<'b>(&'b mut self) -> DebugMap<'b, 'a> {\n  2822:         builders::debug_map_new(self)\n  2823:     }\n  2824: \n  2825:     /// Returns the sign of this formatter (`+` or `-`).\n  2826:     #[unstable(feature = \"formatting_options\", issue = \"118117\")]\n  2827:     pub const fn sign(&self) -> Option<Sign> {\n  2828:         self.options.get_sign()\n  2829:     }\n  2830: \n  2831:     /// Returns the formatting options this formatter corresponds to.\n  2832:     #[unstable(feature = \"formatting_options\", issue = \"118117\")]\n  2833:     pub const fn options(&self) -> FormattingOptions {\n  2834:         self.options\n  2835:     }\n  2836: }\n  2837: ",
    "nanvix_source": "  2811:     ///         fmt.debug_map().entries(self.0.iter().map(|&(ref k, ref v)| (k, v))).finish()\n  2812:     ///     }\n  2813:     /// }\n  2814:     ///\n  2815:     /// assert_eq!(\n  2816:     ///     format!(\"{:?}\",  Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  2817:     ///     r#\"{\"A\": 10, \"B\": 11}\"#\n  2818:     ///  );\n  2819:     /// ```\n  2820:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2821:     pub fn debug_map<'b>(&'b mut self) -> DebugMap<'b, 'a> {\n  2822:         builders::debug_map_new(self)\n  2823:     }\n  2824: \n  2825:     /// Returns the sign of this formatter (`+` or `-`).\n  2826:     #[unstable(feature = \"formatting_options\", issue = \"118117\")]\n  2827:     pub const fn sign(&self) -> Option<Sign> {\n  2828:         self.options.get_sign()\n  2829:     }\n  2830: \n  2831:     /// Returns the formatting options this formatter corresponds to.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::debug_set",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
            "name": "'b"
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
      "name": "debug_set",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                "lifetime": "'b",
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
                    "lifetime": "'b"
                  },
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13421,
            "path": "DebugSet"
          }
        }
      }
    },
    "verification_source": "  2779:     ///     }\n  2780:     /// }\n  2781:     ///\n  2782:     /// impl<'a, K, V> fmt::Debug for Table<'a, K, V>\n  2783:     /// where\n  2784:     ///     K: 'a + fmt::Debug, V: 'a + fmt::Debug\n  2785:     /// {\n  2786:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2787:     ///         fmt.debug_set()\n  2788:     ///         .entries(self.0.iter().map(Arm))\n  2789:     ///         .entry(&Arm(&(format_args!(\"_\"), &self.1)))\n  2790:     ///         .finish()\n  2791:     ///     }\n  2792:     /// }\n  2793:     /// ```\n  2794:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2795:     pub fn debug_set<'b>(&'b mut self) -> DebugSet<'b, 'a> {\n  2796:         builders::debug_set_new(self)\n  2797:     }\n  2798: \n  2799:     /// Creates a `DebugMap` builder designed to assist with creation of\n  2800:     /// `fmt::Debug` implementations for map-like structures.\n  2801:     ///\n  2802:     /// # Examples\n  2803:     ///\n  2804:     /// ```rust\n  2805:     /// use std::fmt;\n  2806:     ///\n  2807:     /// struct Foo(Vec<(String, i32)>);\n  2808:     ///\n  2809:     /// impl fmt::Debug for Foo {\n  2810:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2811:     ///         fmt.debug_map().entries(self.0.iter().map(|&(ref k, ref v)| (k, v))).finish()",
    "nanvix_source": "  2785:     /// {\n  2786:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2787:     ///         fmt.debug_set()\n  2788:     ///         .entries(self.0.iter().map(Arm))\n  2789:     ///         .entry(&Arm(&(format_args!(\"_\"), &self.1)))\n  2790:     ///         .finish()\n  2791:     ///     }\n  2792:     /// }\n  2793:     /// ```\n  2794:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2795:     pub fn debug_set<'b>(&'b mut self) -> DebugSet<'b, 'a> {\n  2796:         builders::debug_set_new(self)\n  2797:     }\n  2798: \n  2799:     /// Creates a `DebugMap` builder designed to assist with creation of\n  2800:     /// `fmt::Debug` implementations for map-like structures.\n  2801:     ///\n  2802:     /// # Examples\n  2803:     ///\n  2804:     /// ```rust\n  2805:     /// use std::fmt;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::debug_struct",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
            "name": "'b"
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
      "name": "debug_struct",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                "lifetime": "'b",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "name",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
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
                    "lifetime": "'b"
                  },
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13417,
            "path": "DebugStruct"
          }
        }
      }
    },
    "verification_source": "  2432:     ///             .field(\"baz\", &self.baz)\n  2433:     ///             .field(\"addr\", &format_args!(\"{}\", self.addr))\n  2434:     ///             .finish()\n  2435:     ///     }\n  2436:     /// }\n  2437:     ///\n  2438:     /// assert_eq!(\n  2439:     ///     \"Foo { bar: 10, baz: \\\"Hello World\\\", addr: 127.0.0.1 }\",\n  2440:     ///     format!(\"{:?}\", Foo {\n  2441:     ///         bar: 10,\n  2442:     ///         baz: \"Hello World\".to_string(),\n  2443:     ///         addr: Ipv4Addr::new(127, 0, 0, 1),\n  2444:     ///     })\n  2445:     /// );\n  2446:     /// ```\n  2447:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2448:     pub fn debug_struct<'b>(&'b mut self, name: &str) -> DebugStruct<'b, 'a> {\n  2449:         builders::debug_struct_new(self, name)\n  2450:     }\n  2451: \n  2452:     /// Shrinks `derive(Debug)` code, for faster compilation and smaller\n  2453:     /// binaries. `debug_struct_fields_finish` is more general, but this is\n  2454:     /// faster for 1 field.\n  2455:     #[doc(hidden)]\n  2456:     #[unstable(feature = \"fmt_helpers_for_derive\", issue = \"none\")]\n  2457:     pub fn debug_struct_field1_finish<'b>(\n  2458:         &'b mut self,\n  2459:         name: &str,\n  2460:         name1: &str,\n  2461:         value1: &dyn Debug,\n  2462:     ) -> Result {\n  2463:         let mut builder = builders::debug_struct_new(self, name);\n  2464:         builder.field(name1, value1);",
    "nanvix_source": "  2438:     /// assert_eq!(\n  2439:     ///     \"Foo { bar: 10, baz: \\\"Hello World\\\", addr: 127.0.0.1 }\",\n  2440:     ///     format!(\"{:?}\", Foo {\n  2441:     ///         bar: 10,\n  2442:     ///         baz: \"Hello World\".to_string(),\n  2443:     ///         addr: Ipv4Addr::new(127, 0, 0, 1),\n  2444:     ///     })\n  2445:     /// );\n  2446:     /// ```\n  2447:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2448:     pub fn debug_struct<'b>(&'b mut self, name: &str) -> DebugStruct<'b, 'a> {\n  2449:         builders::debug_struct_new(self, name)\n  2450:     }\n  2451: \n  2452:     /// Shrinks `derive(Debug)` code, for faster compilation and smaller\n  2453:     /// binaries. `debug_struct_fields_finish` is more general, but this is\n  2454:     /// faster for 1 field.\n  2455:     #[doc(hidden)]\n  2456:     #[unstable(feature = \"fmt_helpers_for_derive\", issue = \"none\")]\n  2457:     pub fn debug_struct_field1_finish<'b>(\n  2458:         &'b mut self,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::debug_tuple",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
            "name": "'b"
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
      "name": "debug_tuple",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                "lifetime": "'b",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "name",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
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
                    "lifetime": "'b"
                  },
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13419,
            "path": "DebugTuple"
          }
        }
      }
    },
    "verification_source": "  2591:     /// impl<T> fmt::Debug for Foo<T> {\n  2592:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2593:     ///         fmt.debug_tuple(\"Foo\")\n  2594:     ///             .field(&self.0)\n  2595:     ///             .field(&self.1)\n  2596:     ///             .field(&format_args!(\"_\"))\n  2597:     ///             .finish()\n  2598:     ///     }\n  2599:     /// }\n  2600:     ///\n  2601:     /// assert_eq!(\n  2602:     ///     \"Foo(10, \\\"Hello\\\", _)\",\n  2603:     ///     format!(\"{:?}\", Foo(10, \"Hello\".to_string(), PhantomData::<u8>))\n  2604:     /// );\n  2605:     /// ```\n  2606:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2607:     pub fn debug_tuple<'b>(&'b mut self, name: &str) -> DebugTuple<'b, 'a> {\n  2608:         builders::debug_tuple_new(self, name)\n  2609:     }\n  2610: \n  2611:     /// Shrinks `derive(Debug)` code, for faster compilation and smaller\n  2612:     /// binaries. `debug_tuple_fields_finish` is more general, but this is faster\n  2613:     /// for 1 field.\n  2614:     #[doc(hidden)]\n  2615:     #[unstable(feature = \"fmt_helpers_for_derive\", issue = \"none\")]\n  2616:     pub fn debug_tuple_field1_finish<'b>(&'b mut self, name: &str, value1: &dyn Debug) -> Result {\n  2617:         let mut builder = builders::debug_tuple_new(self, name);\n  2618:         builder.field(value1);\n  2619:         builder.finish()\n  2620:     }\n  2621: \n  2622:     /// Shrinks `derive(Debug)` code, for faster compilation and smaller\n  2623:     /// binaries. `debug_tuple_fields_finish` is more general, but this is faster",
    "nanvix_source": "  2597:     ///             .finish()\n  2598:     ///     }\n  2599:     /// }\n  2600:     ///\n  2601:     /// assert_eq!(\n  2602:     ///     \"Foo(10, \\\"Hello\\\", _)\",\n  2603:     ///     format!(\"{:?}\", Foo(10, \"Hello\".to_string(), PhantomData::<u8>))\n  2604:     /// );\n  2605:     /// ```\n  2606:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  2607:     pub fn debug_tuple<'b>(&'b mut self, name: &str) -> DebugTuple<'b, 'a> {\n  2608:         builders::debug_tuple_new(self, name)\n  2609:     }\n  2610: \n  2611:     /// Shrinks `derive(Debug)` code, for faster compilation and smaller\n  2612:     /// binaries. `debug_tuple_fields_finish` is more general, but this is faster\n  2613:     /// for 1 field.\n  2614:     #[doc(hidden)]\n  2615:     #[unstable(feature = \"fmt_helpers_for_derive\", issue = \"none\")]\n  2616:     pub fn debug_tuple_field1_finish<'b>(&'b mut self, name: &str, value1: &dyn Debug) -> Result {\n  2617:         let mut builder = builders::debug_tuple_new(self, name);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::fill",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "fill",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
          "primitive": "char"
        }
      }
    },
    "verification_source": "  2163:     ///             for _ in 0..width {\n  2164:     ///                 write!(formatter, \"{c}\")?;\n  2165:     ///             }\n  2166:     ///             Ok(())\n  2167:     ///         } else {\n  2168:     ///             write!(formatter, \"{c}\")\n  2169:     ///         }\n  2170:     ///     }\n  2171:     /// }\n  2172:     ///\n  2173:     /// // We set alignment to the right with \">\".\n  2174:     /// assert_eq!(format!(\"{Foo:G>3}\"), \"GGG\");\n  2175:     /// assert_eq!(format!(\"{Foo:t>6}\"), \"tttttt\");\n  2176:     /// ```\n  2177:     #[must_use]\n  2178:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2179:     pub fn fill(&self) -> char {\n  2180:         self.options.get_fill()\n  2181:     }\n  2182: \n  2183:     /// Returns a flag indicating what form of alignment was requested.\n  2184:     ///\n  2185:     /// # Examples\n  2186:     ///\n  2187:     /// ```\n  2188:     /// use std::fmt::{self, Alignment};\n  2189:     ///\n  2190:     /// struct Foo;\n  2191:     ///\n  2192:     /// impl fmt::Display for Foo {\n  2193:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2194:     ///         let s = if let Some(s) = formatter.align() {\n  2195:     ///             match s {",
    "nanvix_source": "  2169:     ///         }\n  2170:     ///     }\n  2171:     /// }\n  2172:     ///\n  2173:     /// // We set alignment to the right with \">\".\n  2174:     /// assert_eq!(format!(\"{Foo:G>3}\"), \"GGG\");\n  2175:     /// assert_eq!(format!(\"{Foo:t>6}\"), \"tttttt\");\n  2176:     /// ```\n  2177:     #[must_use]\n  2178:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2179:     pub fn fill(&self) -> char {\n  2180:         self.options.get_fill()\n  2181:     }\n  2182: \n  2183:     /// Returns a flag indicating what form of alignment was requested.\n  2184:     ///\n  2185:     /// # Examples\n  2186:     ///\n  2187:     /// ```\n  2188:     /// use std::fmt::{self, Alignment};\n  2189:     ///",
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
