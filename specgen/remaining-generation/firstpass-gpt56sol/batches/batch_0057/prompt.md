For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::fmt::format",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "free_function"
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
      "name": "format",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "args",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'_"
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 3489,
                "path": "Arguments"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "string::String"
          }
        }
      }
    },
    "verification_source": "   616: \n   617: #[cfg(not(no_global_oom_handling))]\n   618: use crate::string;\n   619: \n   620: /// Takes an [`Arguments`] struct and returns the resulting formatted string.\n   621: ///\n   622: /// The [`Arguments`] instance can be created with the [`format_args!`] macro.\n   623: ///\n   624: /// # Examples\n   625: ///\n   626: /// Basic usage:\n   627: ///\n   628: /// ```\n   629: /// use std::fmt;\n   630: ///\n   631: /// let s = fmt::format(format_args!(\"Hello, {}!\", \"world\"));\n   632: /// assert_eq!(s, \"Hello, world!\");\n   633: /// ```\n   634: ///\n   635: /// Please note that using [`format!`] might be preferable.\n   636: /// Example:\n   637: ///\n   638: /// ```\n   639: /// let s = format!(\"Hello, {}!\", \"world\");\n   640: /// assert_eq!(s, \"Hello, world!\");\n   641: /// ```\n   642: ///\n   643: /// [`format_args!`]: core::format_args\n   644: /// [`format!`]: crate::format\n   645: #[cfg(not(no_global_oom_handling))]\n   646: #[must_use]\n   647: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   648: #[inline]",
    "nanvix_source": "   622: /// The [`Arguments`] instance can be created with the [`format_args!`] macro.\n   623: ///\n   624: /// # Examples\n   625: ///\n   626: /// Basic usage:\n   627: ///\n   628: /// ```\n   629: /// use std::fmt;\n   630: ///\n   631: /// let s = fmt::format(format_args!(\"Hello, {}!\", \"world\"));\n   632: /// assert_eq!(s, \"Hello, world!\");\n   633: /// ```\n   634: ///\n   635: /// Please note that using [`format!`] might be preferable.\n   636: /// Example:\n   637: ///\n   638: /// ```\n   639: /// let s = format!(\"Hello, {}!\", \"world\");\n   640: /// assert_eq!(s, \"Hello, world!\");\n   641: /// ```\n   642: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Arguments::as_str",
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
      "formatting_effect",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_str",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10035,
            "path": "Arguments"
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
        "impl_id": "core:30057",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10035",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Arguments"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": "'static",
                        "type": {
                          "primitive": "str"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   855:     ///         write_str(s)\n   856:     ///     } else {\n   857:     ///         write_str(&args.to_string());\n   858:     ///     }\n   859:     /// }\n   860:     /// ```\n   861:     ///\n   862:     /// ```rust\n   863:     /// assert_eq!(format_args!(\"hello\").as_str(), Some(\"hello\"));\n   864:     /// assert_eq!(format_args!(\"\").as_str(), Some(\"\"));\n   865:     /// assert_eq!(format_args!(\"{:?}\", std::env::current_dir()).as_str(), None);\n   866:     /// ```\n   867:     #[stable(feature = \"fmt_as_str\", since = \"1.52.0\")]\n   868:     #[rustc_const_stable(feature = \"const_arguments_as_str\", since = \"1.84.0\")]\n   869:     #[must_use]\n   870:     #[inline]\n   871:     pub const fn as_str(&self) -> Option<&'static str> {\n   872:         // SAFETY: During const eval, `self.args` must have come from a usize,\n   873:         // not a pointer, because that's the only way to create a fmt::Arguments in const.\n   874:         // (I.e. only fmt::Arguments::from_str is const, fmt::Arguments::new is not.)\n   875:         //\n   876:         // Outside const eval, transmuting a pointer to a usize is fine.\n   877:         let bits: usize = unsafe { mem::transmute(self.args) };\n   878:         if bits & 1 == 1 {\n   879:             // SAFETY: This fmt::Arguments stores a &'static str. See encoding documentation above.\n   880:             Some(unsafe {\n   881:                 str::from_utf8_unchecked(crate::slice::from_raw_parts(\n   882:                     self.template.as_ptr(),\n   883:                     bits >> 1,\n   884:                 ))\n   885:             })\n   886:         } else {\n   887:             None",
    "nanvix_source": "   861:     ///\n   862:     /// ```rust\n   863:     /// assert_eq!(format_args!(\"hello\").as_str(), Some(\"hello\"));\n   864:     /// assert_eq!(format_args!(\"\").as_str(), Some(\"\"));\n   865:     /// assert_eq!(format_args!(\"{:?}\", std::env::current_dir()).as_str(), None);\n   866:     /// ```\n   867:     #[stable(feature = \"fmt_as_str\", since = \"1.52.0\")]\n   868:     #[rustc_const_stable(feature = \"const_arguments_as_str\", since = \"1.84.0\")]\n   869:     #[must_use]\n   870:     #[inline]\n   871:     pub const fn as_str(&self) -> Option<&'static str> {\n   872:         // SAFETY: During const eval, `self.args` must have come from a usize,\n   873:         // not a pointer, because that's the only way to create a fmt::Arguments in const.\n   874:         // (I.e. only fmt::Arguments::from_str is const, fmt::Arguments::new is not.)\n   875:         //\n   876:         // Outside const eval, transmuting a pointer to a usize is fine.\n   877:         let bits: usize = unsafe { mem::transmute(self.args) };\n   878:         if bits & 1 == 1 {\n   879:             // SAFETY: This fmt::Arguments stores a &'static str. See encoding documentation above.\n   880:             Some(unsafe {\n   881:                 str::from_utf8_unchecked(crate::slice::from_raw_parts(",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugList::entries",
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
      "formatting_effect",
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
            "name": "D"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
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
                      "id": 921,
                      "path": "fmt::Debug"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "D"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "D"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
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
      "name": "entries",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13423,
            "path": "DebugList"
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
            },
            {
              "kind": {
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29829",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13423",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugList"
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
            "entries",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   766:     ///\n   767:     /// impl fmt::Debug for Foo {\n   768:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   769:     ///         fmt.debug_list()\n   770:     ///            .entries(self.0.iter())\n   771:     ///            .entries(self.1.iter())\n   772:     ///            .finish()\n   773:     ///     }\n   774:     /// }\n   775:     ///\n   776:     /// assert_eq!(\n   777:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   778:     ///     \"[10, 11, 12, 13]\",\n   779:     /// );\n   780:     /// ```\n   781:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   782:     pub fn entries<D, I>(&mut self, entries: I) -> &mut Self\n   783:     where\n   784:         D: fmt::Debug,\n   785:         I: IntoIterator<Item = D>,\n   786:     {\n   787:         for entry in entries {\n   788:             self.entry(&entry);\n   789:         }\n   790:         self\n   791:     }\n   792: \n   793:     /// Marks the list as non-exhaustive, indicating to the reader that there are some other\n   794:     /// elements that are not shown in the debug representation.\n   795:     ///\n   796:     /// # Examples\n   797:     ///\n   798:     /// ```",
    "nanvix_source": "   772:     ///            .finish()\n   773:     ///     }\n   774:     /// }\n   775:     ///\n   776:     /// assert_eq!(\n   777:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   778:     ///     \"[10, 11, 12, 13]\",\n   779:     /// );\n   780:     /// ```\n   781:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   782:     pub fn entries<D, I>(&mut self, entries: I) -> &mut Self\n   783:     where\n   784:         D: fmt::Debug,\n   785:         I: IntoIterator<Item = D>,\n   786:     {\n   787:         for entry in entries {\n   788:             self.entry(&entry);\n   789:         }\n   790:         self\n   791:     }\n   792: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugList::entry",
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
      "formatting_effect",
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
      "name": "entry",
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
                    "lifetime": "'a"
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13423,
            "path": "DebugList"
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
            },
            {
              "kind": {
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29829",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13423",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugList"
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
            "entry",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "dyn_trait": {
                    "lifetime": null,
                    "traits": [
                      {
                        "generic_params": [],
                        "trait": {
                          "args": null,
                          "id": 921,
                          "path": "fmt::Debug"
                        }
                      }
                    ]
                  }
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
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   724:     ///\n   725:     /// impl fmt::Debug for Foo {\n   726:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   727:     ///         fmt.debug_list()\n   728:     ///            .entry(&self.0) // We add the first \"entry\".\n   729:     ///            .entry(&self.1) // We add the second \"entry\".\n   730:     ///            .finish()\n   731:     ///     }\n   732:     /// }\n   733:     ///\n   734:     /// assert_eq!(\n   735:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   736:     ///     \"[[10, 11], [12, 13]]\",\n   737:     /// );\n   738:     /// ```\n   739:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   740:     pub fn entry(&mut self, entry: &dyn fmt::Debug) -> &mut Self {\n   741:         self.inner.entry_with(|f| entry.fmt(f));\n   742:         self\n   743:     }\n   744: \n   745:     /// Adds a new entry to the list output.\n   746:     ///\n   747:     /// This method is equivalent to [`DebugList::entry`], but formats the\n   748:     /// entry using a provided closure rather than by calling [`Debug::fmt`].\n   749:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   750:     pub fn entry_with<F>(&mut self, entry_fmt: F) -> &mut Self\n   751:     where\n   752:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n   753:     {\n   754:         self.inner.entry_with(entry_fmt);\n   755:         self\n   756:     }",
    "nanvix_source": "   730:     ///            .finish()\n   731:     ///     }\n   732:     /// }\n   733:     ///\n   734:     /// assert_eq!(\n   735:     ///     format!(\"{:?}\", Foo(vec![10, 11], vec![12, 13])),\n   736:     ///     \"[[10, 11], [12, 13]]\",\n   737:     /// );\n   738:     /// ```\n   739:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   740:     pub fn entry(&mut self, entry: &dyn fmt::Debug) -> &mut Self {\n   741:         self.inner.entry_with(|f| entry.fmt(f));\n   742:         self\n   743:     }\n   744: \n   745:     /// Adds a new entry to the list output.\n   746:     ///\n   747:     /// This method is equivalent to [`DebugList::entry`], but formats the\n   748:     /// entry using a provided closure rather than by calling [`Debug::fmt`].\n   749:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   750:     pub fn entry_with<F>(&mut self, entry_fmt: F) -> &mut Self",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugList::finish",
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
      "name": "finish",
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
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13423,
            "path": "DebugList"
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
            },
            {
              "kind": {
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29829",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13423",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugList"
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
            "args": null,
            "id": 919,
            "path": "fmt::Result"
          }
        }
      }
    },
    "verification_source": "   847:     /// struct Foo(Vec<i32>);\n   848:     ///\n   849:     /// impl fmt::Debug for Foo {\n   850:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   851:     ///         fmt.debug_list()\n   852:     ///            .entries(self.0.iter())\n   853:     ///            .finish() // Ends the list formatting.\n   854:     ///     }\n   855:     /// }\n   856:     ///\n   857:     /// assert_eq!(\n   858:     ///     format!(\"{:?}\", Foo(vec![10, 11])),\n   859:     ///     \"[10, 11]\",\n   860:     /// );\n   861:     /// ```\n   862:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   863:     pub fn finish(&mut self) -> fmt::Result {\n   864:         self.inner.result = self.inner.result.and_then(|_| self.inner.fmt.write_str(\"]\"));\n   865:         self.inner.result\n   866:     }\n   867: }\n   868: \n   869: /// A struct to help with [`fmt::Debug`](Debug) implementations.\n   870: ///\n   871: /// This is useful when you wish to output a formatted map as a part of your\n   872: /// [`Debug::fmt`] implementation.\n   873: ///\n   874: /// This can be constructed by the [`Formatter::debug_map`] method.\n   875: ///\n   876: /// # Examples\n   877: ///\n   878: /// ```\n   879: /// use std::fmt;",
    "nanvix_source": "   853:     ///            .finish() // Ends the list formatting.\n   854:     ///     }\n   855:     /// }\n   856:     ///\n   857:     /// assert_eq!(\n   858:     ///     format!(\"{:?}\", Foo(vec![10, 11])),\n   859:     ///     \"[10, 11]\",\n   860:     /// );\n   861:     /// ```\n   862:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   863:     pub fn finish(&mut self) -> fmt::Result {\n   864:         self.inner.result = self.inner.result.and_then(|_| self.inner.fmt.write_str(\"]\"));\n   865:         self.inner.result\n   866:     }\n   867: }\n   868: \n   869: /// A struct to help with [`fmt::Debug`](Debug) implementations.\n   870: ///\n   871: /// This is useful when you wish to output a formatted map as a part of your\n   872: /// [`Debug::fmt`] implementation.\n   873: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugList::finish_non_exhaustive",
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
      "name": "finish_non_exhaustive",
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
                  },
                  {
                    "lifetime": "'b"
                  }
                ],
                "constraints": []
              }
            },
            "id": 13423,
            "path": "DebugList"
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
            },
            {
              "kind": {
                "lifetime": {
                  "outlives": [
                    "'a"
                  ]
                }
              },
              "name": "'b"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29829",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13423",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugList"
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
            "args": null,
            "id": 919,
            "path": "fmt::Result"
          }
        }
      }
    },
    "verification_source": "   806:     ///         let mut f = fmt.debug_list();\n   807:     ///         let mut f = f.entries(self.0.iter().take(2));\n   808:     ///         if self.0.len() > 2 {\n   809:     ///             f.finish_non_exhaustive()\n   810:     ///         } else {\n   811:     ///             f.finish()\n   812:     ///         }\n   813:     ///     }\n   814:     /// }\n   815:     ///\n   816:     /// assert_eq!(\n   817:     ///     format!(\"{:?}\", Foo(vec![1, 2, 3, 4])),\n   818:     ///     \"[1, 2, ..]\",\n   819:     /// );\n   820:     /// ```\n   821:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   822:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   823:         self.inner.result.and_then(|_| {\n   824:             if self.inner.has_fields {\n   825:                 if self.inner.is_pretty() {\n   826:                     let mut slot = None;\n   827:                     let mut state = Default::default();\n   828:                     let mut writer = PadAdapter::wrap(self.inner.fmt, &mut slot, &mut state);\n   829:                     writer.write_str(\"..\\n\")?;\n   830:                     self.inner.fmt.write_str(\"]\")\n   831:                 } else {\n   832:                     self.inner.fmt.write_str(\", ..]\")\n   833:                 }\n   834:             } else {\n   835:                 self.inner.fmt.write_str(\"..]\")\n   836:             }\n   837:         })\n   838:     }",
    "nanvix_source": "   812:     ///         }\n   813:     ///     }\n   814:     /// }\n   815:     ///\n   816:     /// assert_eq!(\n   817:     ///     format!(\"{:?}\", Foo(vec![1, 2, 3, 4])),\n   818:     ///     \"[1, 2, ..]\",\n   819:     /// );\n   820:     /// ```\n   821:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   822:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   823:         self.inner.result.and_then(|_| {\n   824:             if self.inner.has_fields {\n   825:                 if self.inner.is_pretty() {\n   826:                     let mut slot = None;\n   827:                     let mut state = Default::default();\n   828:                     let mut writer = PadAdapter::wrap(self.inner.fmt, &mut slot, &mut state);\n   829:                     writer.write_str(\"..\\n\")?;\n   830:                     self.inner.fmt.write_str(\"]\")\n   831:                 } else {\n   832:                     self.inner.fmt.write_str(\", ..]\")",
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
