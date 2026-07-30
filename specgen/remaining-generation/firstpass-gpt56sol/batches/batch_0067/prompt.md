For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Result::iter_mut",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "iter_mut",
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
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13412,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  1109:     /// # Examples\n  1110:     ///\n  1111:     /// ```\n  1112:     /// let mut x: Result<u32, &str> = Ok(7);\n  1113:     /// match x.iter_mut().next() {\n  1114:     ///     Some(v) => *v = 40,\n  1115:     ///     None => {},\n  1116:     /// }\n  1117:     /// assert_eq!(x, Ok(40));\n  1118:     ///\n  1119:     /// let mut x: Result<u32, &str> = Err(\"nothing!\");\n  1120:     /// assert_eq!(x.iter_mut().next(), None);\n  1121:     /// ```\n  1122:     #[inline]\n  1123:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1124:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1125:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1126:         IterMut { inner: self.as_mut().ok() }\n  1127:     }\n  1128: \n  1129:     /////////////////////////////////////////////////////////////////////////\n  1130:     // Extract a value\n  1131:     /////////////////////////////////////////////////////////////////////////\n  1132: \n  1133:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1134:     ///\n  1135:     /// Because this function may panic, its use is generally discouraged.\n  1136:     /// Instead, prefer to use pattern matching and handle the [`Err`]\n  1137:     /// case explicitly, or call [`unwrap_or`], [`unwrap_or_else`], or\n  1138:     /// [`unwrap_or_default`].\n  1139:     ///\n  1140:     /// [`unwrap_or`]: Result::unwrap_or\n  1141:     /// [`unwrap_or_else`]: Result::unwrap_or_else",
    "nanvix_source": "  1113:     ///     None => {},\n  1114:     /// }\n  1115:     /// assert_eq!(x, Ok(40));\n  1116:     ///\n  1117:     /// let mut x: Result<u32, &str> = Err(\"nothing!\");\n  1118:     /// assert_eq!(x.iter_mut().next(), None);\n  1119:     /// ```\n  1120:     #[inline]\n  1121:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1122:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1123:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1124:         IterMut { inner: self.as_mut().ok() }\n  1125:     }\n  1126: \n  1127:     /////////////////////////////////////////////////////////////////////////\n  1128:     // Extract a value\n  1129:     /////////////////////////////////////////////////////////////////////////\n  1130: \n  1131:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1132:     ///\n  1133:     /// Because this function may panic, its use is generally discouraged.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::map",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "U"
                          }
                        }
                      },
                      "id": 24,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "map",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "op",
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
                      "generic": "U"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   815:     ///\n   816:     /// Print the numbers on each line of a string multiplied by two.\n   817:     ///\n   818:     /// ```\n   819:     /// let line = \"1\\n2\\n3\\n4\\n\";\n   820:     ///\n   821:     /// for num in line.lines() {\n   822:     ///     match num.parse::<i32>().map(|i| i * 2) {\n   823:     ///         Ok(n) => println!(\"{n}\"),\n   824:     ///         Err(..) => {}\n   825:     ///     }\n   826:     /// }\n   827:     /// ```\n   828:     #[inline]\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   831:     pub const fn map<U, F>(self, op: F) -> Result<U, E>\n   832:     where\n   833:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   834:     {\n   835:         match self {\n   836:             Ok(t) => Ok(op(t)),\n   837:             Err(e) => Err(e),\n   838:         }\n   839:     }\n   840: \n   841:     /// Returns the provided default (if [`Err`]), or\n   842:     /// applies a function to the contained value (if [`Ok`]).\n   843:     ///\n   844:     /// Arguments passed to `map_or` are eagerly evaluated; if you are passing\n   845:     /// the result of a function call, it is recommended to use [`map_or_else`],\n   846:     /// which is lazily evaluated.\n   847:     ///",
    "nanvix_source": "   821:     /// for num in line.lines() {\n   822:     ///     match num.parse::<i32>().map(|i| i * 2) {\n   823:     ///         Ok(n) => println!(\"{n}\"),\n   824:     ///         Err(..) => {}\n   825:     ///     }\n   826:     /// }\n   827:     /// ```\n   828:     #[inline]\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   831:     pub const fn map<U, F>(self, op: F) -> Result<U, E>\n   832:     where\n   833:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   834:     {\n   835:         match self {\n   836:             Ok(t) => Ok(op(t)),\n   837:             Err(e) => Err(e),\n   838:         }\n   839:     }\n   840: \n   841:     /// Returns the provided default (if [`Err`]), or",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::map_err",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "O"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "E"
                            }
                          ],
                          "output": {
                            "generic": "F"
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "O"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "map_err",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "op",
            {
              "generic": "O"
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   946:     ///\n   947:     ///\n   948:     /// # Examples\n   949:     ///\n   950:     /// ```\n   951:     /// fn stringify(x: u32) -> String { format!(\"error code: {x}\") }\n   952:     ///\n   953:     /// let x: Result<u32, u32> = Ok(2);\n   954:     /// assert_eq!(x.map_err(stringify), Ok(2));\n   955:     ///\n   956:     /// let x: Result<u32, u32> = Err(13);\n   957:     /// assert_eq!(x.map_err(stringify), Err(\"error code: 13\".to_string()));\n   958:     /// ```\n   959:     #[inline]\n   960:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   961:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   962:     pub const fn map_err<F, O>(self, op: O) -> Result<T, F>\n   963:     where\n   964:         O: [const] FnOnce(E) -> F + [const] Destruct,\n   965:     {\n   966:         match self {\n   967:             Ok(t) => Ok(t),\n   968:             Err(e) => Err(op(e)),\n   969:         }\n   970:     }\n   971: \n   972:     /// Calls a function with a reference to the contained value if [`Ok`].\n   973:     ///\n   974:     /// Returns the original result.\n   975:     ///\n   976:     /// # Examples\n   977:     ///\n   978:     /// ```",
    "nanvix_source": "   950:     ///\n   951:     /// let x: Result<u32, u32> = Ok(2);\n   952:     /// assert_eq!(x.map_err(stringify), Ok(2));\n   953:     ///\n   954:     /// let x: Result<u32, u32> = Err(13);\n   955:     /// assert_eq!(x.map_err(stringify), Err(\"error code: 13\".to_string()));\n   956:     /// ```\n   957:     #[inline]\n   958:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   959:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   960:     pub const fn map_err<F, O>(self, op: O) -> Result<T, F>\n   961:     where\n   962:         O: [const] FnOnce(E) -> F + [const] Destruct,\n   963:     {\n   964:         match self {\n   965:             Ok(t) => Ok(t),\n   966:             Err(e) => Err(op(e)),\n   967:         }\n   968:     }\n   969: \n   970:     /// Calls a function with a reference to the contained value if [`Ok`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::map_or",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "U"
                          }
                        }
                      },
                      "id": 24,
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
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "map_or",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "default",
            {
              "generic": "U"
            }
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "U"
        }
      }
    },
    "verification_source": "   847:     ///\n   848:     /// [`map_or_else`]: Result::map_or_else\n   849:     ///\n   850:     /// # Examples\n   851:     ///\n   852:     /// ```\n   853:     /// let x: Result<_, &str> = Ok(\"foo\");\n   854:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n   855:     ///\n   856:     /// let x: Result<&str, _> = Err(\"bar\");\n   857:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"result_map_or\", since = \"1.41.0\")]\n   861:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   862:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n   863:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n   864:     where\n   865:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   866:         T: [const] Destruct,\n   867:         E: [const] Destruct,\n   868:         U: [const] Destruct,\n   869:     {\n   870:         match self {\n   871:             Ok(t) => f(t),\n   872:             Err(_) => default,\n   873:         }\n   874:     }\n   875: \n   876:     /// Maps a `Result<T, E>` to `U` by applying fallback function `default` to\n   877:     /// a contained [`Err`] value, or function `f` to a contained [`Ok`] value.\n   878:     ///\n   879:     /// This function can be used to unpack a successful result",
    "nanvix_source": "   853:     /// let x: Result<_, &str> = Ok(\"foo\");\n   854:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n   855:     ///\n   856:     /// let x: Result<&str, _> = Err(\"bar\");\n   857:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"result_map_or\", since = \"1.41.0\")]\n   861:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   862:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n   863:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n   864:     where\n   865:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   866:         T: [const] Destruct,\n   867:         E: [const] Destruct,\n   868:         U: [const] Destruct,\n   869:     {\n   870:         match self {\n   871:             Ok(t) => f(t),\n   872:             Err(_) => default,\n   873:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::map_or_default",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "U"
                          }
                        }
                      },
                      "id": 24,
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
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 70,
                      "path": "Default"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "map_or_default",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "U"
        }
      }
    },
    "verification_source": "   912:     /// # Examples\n   913:     ///\n   914:     /// ```\n   915:     /// #![feature(result_option_map_or_default)]\n   916:     ///\n   917:     /// let x: Result<_, &str> = Ok(\"foo\");\n   918:     /// let y: Result<&str, _> = Err(\"bar\");\n   919:     ///\n   920:     /// assert_eq!(x.map_or_default(|x| x.len()), 3);\n   921:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n   922:     /// ```\n   923:     ///\n   924:     /// [default value]: Default::default\n   925:     #[inline]\n   926:     #[unstable(feature = \"result_option_map_or_default\", issue = \"138099\")]\n   927:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   928:     pub const fn map_or_default<U, F>(self, f: F) -> U\n   929:     where\n   930:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   931:         U: [const] Default,\n   932:         T: [const] Destruct,\n   933:         E: [const] Destruct,\n   934:     {\n   935:         match self {\n   936:             Ok(t) => f(t),\n   937:             Err(_) => U::default(),\n   938:         }\n   939:     }\n   940: \n   941:     /// Maps a `Result<T, E>` to `Result<T, F>` by applying a function to a\n   942:     /// contained [`Err`] value, leaving an [`Ok`] value untouched.\n   943:     ///\n   944:     /// This function can be used to pass through a successful result while handling",
    "nanvix_source": "   916:     /// let y: Result<&str, _> = Err(\"bar\");\n   917:     ///\n   918:     /// assert_eq!(x.map_or_default(|x| x.len()), 3);\n   919:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n   920:     /// ```\n   921:     ///\n   922:     /// [default value]: Default::default\n   923:     #[inline]\n   924:     #[stable(feature = \"result_option_map_or_default\", since = \"CURRENT_RUSTC_VERSION\")]\n   925:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   926:     pub const fn map_or_default<U, F>(self, f: F) -> U\n   927:     where\n   928:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   929:         U: [const] Default,\n   930:         T: [const] Destruct,\n   931:         E: [const] Destruct,\n   932:     {\n   933:         match self {\n   934:             Ok(t) => f(t),\n   935:             Err(_) => U::default(),\n   936:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::map_or_else",
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "E"
                            }
                          ],
                          "output": {
                            "generic": "U"
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "T"
                            }
                          ],
                          "output": {
                            "generic": "U"
                          }
                        }
                      },
                      "id": 24,
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "map_or_else",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
          ],
          [
            "default",
            {
              "generic": "D"
            }
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "U"
        }
      }
    },
    "verification_source": "   881:     ///\n   882:     ///\n   883:     /// # Examples\n   884:     ///\n   885:     /// ```\n   886:     /// let k = 21;\n   887:     ///\n   888:     /// let x : Result<_, &str> = Ok(\"foo\");\n   889:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);\n   890:     ///\n   891:     /// let x : Result<&str, _> = Err(\"bar\");\n   892:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);\n   893:     /// ```\n   894:     #[inline]\n   895:     #[stable(feature = \"result_map_or_else\", since = \"1.41.0\")]\n   896:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   897:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n   898:     where\n   899:         D: [const] FnOnce(E) -> U + [const] Destruct,\n   900:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   901:     {\n   902:         match self {\n   903:             Ok(t) => f(t),\n   904:             Err(e) => default(e),\n   905:         }\n   906:     }\n   907: \n   908:     /// Maps a `Result<T, E>` to a `U` by applying function `f` to the contained\n   909:     /// value if the result is [`Ok`], otherwise if [`Err`], returns the\n   910:     /// [default value] for the type `U`.\n   911:     ///\n   912:     /// # Examples\n   913:     ///",
    "nanvix_source": "   887:     ///\n   888:     /// let x : Result<_, &str> = Ok(\"foo\");\n   889:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);\n   890:     ///\n   891:     /// let x : Result<&str, _> = Err(\"bar\");\n   892:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);\n   893:     /// ```\n   894:     #[inline]\n   895:     #[stable(feature = \"result_map_or_else\", since = \"1.41.0\")]\n   896:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   897:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n   898:     where\n   899:         D: [const] FnOnce(E) -> U + [const] Destruct,\n   900:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   901:     {\n   902:         match self {\n   903:             Ok(t) => f(t),\n   904:             Err(e) => default(e),\n   905:         }\n   906:     }\n   907: ",
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
