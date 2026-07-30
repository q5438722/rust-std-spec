For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::LockResult::as_deref_mut",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state",
      "reference_identity_vs_view"
    ],
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8650,
                      "path": "DerefMut"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_deref_mut",
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
                      }
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
    "verification_source": "  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());\n  1063:     /// let y: Result<&mut str, &mut u32> = Ok(&mut s);\n  1064:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1065:     ///\n  1066:     /// let mut i = 42;\n  1067:     /// let mut x: Result<String, u32> = Err(42);\n  1068:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1069:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1070:     /// ```\n  1071:     #[inline]\n  1072:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1073:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1074:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1075:     where\n  1076:         T: [const] DerefMut,\n  1077:     {\n  1078:         self.as_mut().map(DerefMut::deref_mut)\n  1079:     }\n  1080: \n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082:     // Iterator constructors\n  1083:     /////////////////////////////////////////////////////////////////////////\n  1084: \n  1085:     /// Returns an iterator over the possibly contained value.\n  1086:     ///\n  1087:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1088:     ///\n  1089:     /// # Examples\n  1090:     ///",
    "nanvix_source": "  1062:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1063:     ///\n  1064:     /// let mut i = 42;\n  1065:     /// let mut x: Result<String, u32> = Err(42);\n  1066:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1067:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1068:     /// ```\n  1069:     #[inline]\n  1070:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1071:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1072:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1073:     where\n  1074:         T: [const] DerefMut,\n  1075:     {\n  1076:         self.as_mut().map(DerefMut::deref_mut)\n  1077:     }\n  1078: \n  1079:     /////////////////////////////////////////////////////////////////////////\n  1080:     // Iterator constructors\n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::as_mut",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state",
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
      "name": "as_mut",
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
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
                      }
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
    "verification_source": "   782:     ///         Ok(v) => *v = 42,\n   783:     ///         Err(e) => *e = 0,\n   784:     ///     }\n   785:     /// }\n   786:     ///\n   787:     /// let mut x: Result<i32, i32> = Ok(2);\n   788:     /// mutate(&mut x);\n   789:     /// assert_eq!(x.unwrap(), 42);\n   790:     ///\n   791:     /// let mut x: Result<i32, i32> = Err(13);\n   792:     /// mutate(&mut x);\n   793:     /// assert_eq!(x.unwrap_err(), 0);\n   794:     /// ```\n   795:     #[inline]\n   796:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   797:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n   798:     pub const fn as_mut(&mut self) -> Result<&mut T, &mut E> {\n   799:         match *self {\n   800:             Ok(ref mut x) => Ok(x),\n   801:             Err(ref mut x) => Err(x),\n   802:         }\n   803:     }\n   804: \n   805:     /////////////////////////////////////////////////////////////////////////\n   806:     // Transforming contained values\n   807:     /////////////////////////////////////////////////////////////////////////\n   808: \n   809:     /// Maps a `Result<T, E>` to `Result<U, E>` by applying a function to a\n   810:     /// contained [`Ok`] value, leaving an [`Err`] value untouched.\n   811:     ///\n   812:     /// This function can be used to compose the results of two functions.\n   813:     ///\n   814:     /// # Examples",
    "nanvix_source": "   788:     /// mutate(&mut x);\n   789:     /// assert_eq!(x.unwrap(), 42);\n   790:     ///\n   791:     /// let mut x: Result<i32, i32> = Err(13);\n   792:     /// mutate(&mut x);\n   793:     /// assert_eq!(x.unwrap_err(), 0);\n   794:     /// ```\n   795:     #[inline]\n   796:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   797:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n   798:     pub const fn as_mut(&mut self) -> Result<&mut T, &mut E> {\n   799:         match *self {\n   800:             Ok(ref mut x) => Ok(x),\n   801:             Err(ref mut x) => Err(x),\n   802:         }\n   803:     }\n   804: \n   805:     /////////////////////////////////////////////////////////////////////////\n   806:     // Transforming contained values\n   807:     /////////////////////////////////////////////////////////////////////////\n   808: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::as_ref",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state",
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
      "name": "as_ref",
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
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
                      }
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
    "verification_source": "   752:     ///\n   753:     /// Produces a new `Result`, containing a reference\n   754:     /// into the original, leaving the original in place.\n   755:     ///\n   756:     /// # Examples\n   757:     ///\n   758:     /// ```\n   759:     /// let x: Result<u32, &str> = Ok(2);\n   760:     /// assert_eq!(x.as_ref(), Ok(&2));\n   761:     ///\n   762:     /// let x: Result<u32, &str> = Err(\"Error\");\n   763:     /// assert_eq!(x.as_ref(), Err(&\"Error\"));\n   764:     /// ```\n   765:     #[inline]\n   766:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   767:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   768:     pub const fn as_ref(&self) -> Result<&T, &E> {\n   769:         match *self {\n   770:             Ok(ref x) => Ok(x),\n   771:             Err(ref x) => Err(x),\n   772:         }\n   773:     }\n   774: \n   775:     /// Converts from `&mut Result<T, E>` to `Result<&mut T, &mut E>`.\n   776:     ///\n   777:     /// # Examples\n   778:     ///\n   779:     /// ```\n   780:     /// fn mutate(r: &mut Result<i32, i32>) {\n   781:     ///     match r.as_mut() {\n   782:     ///         Ok(v) => *v = 42,\n   783:     ///         Err(e) => *e = 0,\n   784:     ///     }",
    "nanvix_source": "   758:     /// ```\n   759:     /// let x: Result<u32, &str> = Ok(2);\n   760:     /// assert_eq!(x.as_ref(), Ok(&2));\n   761:     ///\n   762:     /// let x: Result<u32, &str> = Err(\"Error\");\n   763:     /// assert_eq!(x.as_ref(), Err(&\"Error\"));\n   764:     /// ```\n   765:     #[inline]\n   766:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   767:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   768:     pub const fn as_ref(&self) -> Result<&T, &E> {\n   769:         match *self {\n   770:             Ok(ref x) => Ok(x),\n   771:             Err(ref x) => Err(x),\n   772:         }\n   773:     }\n   774: \n   775:     /// Converts from `&mut Result<T, E>` to `Result<&mut T, &mut E>`.\n   776:     ///\n   777:     /// # Examples\n   778:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::cloned",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state",
      "multiple_rust_declarations_share_path"
    ],
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
                      "id": 42,
                      "path": "Clone"
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
      "name": "cloned",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
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
        "impl_id": "core:29313",
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
    "verification_source": "  1721:     }\n  1722: \n  1723:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by cloning the contents of the\n  1724:     /// `Ok` part.\n  1725:     ///\n  1726:     /// # Examples\n  1727:     ///\n  1728:     /// ```\n  1729:     /// let val = 12;\n  1730:     /// let x: Result<&i32, i32> = Ok(&val);\n  1731:     /// assert_eq!(x, Ok(&12));\n  1732:     /// let cloned = x.cloned();\n  1733:     /// assert_eq!(cloned, Ok(12));\n  1734:     /// ```\n  1735:     #[inline]\n  1736:     #[stable(feature = \"result_cloned\", since = \"1.59.0\")]\n  1737:     pub fn cloned(self) -> Result<T, E>\n  1738:     where\n  1739:         T: Clone,\n  1740:     {\n  1741:         self.map(|t| t.clone())\n  1742:     }\n  1743: }\n  1744: \n  1745: impl<T, E> Result<&mut T, E> {\n  1746:     /// Maps a `Result<&mut T, E>` to a `Result<T, E>` by copying the contents of the\n  1747:     /// `Ok` part.\n  1748:     ///\n  1749:     /// # Examples\n  1750:     ///\n  1751:     /// ```\n  1752:     /// let mut val = 12;\n  1753:     /// let x: Result<&mut i32, i32> = Ok(&mut val);",
    "nanvix_source": "  1730:     ///\n  1731:     /// ```\n  1732:     /// let val = 12;\n  1733:     /// let x: Result<&i32, i32> = Ok(&val);\n  1734:     /// assert_eq!(x, Ok(&12));\n  1735:     /// let cloned = x.cloned();\n  1736:     /// assert_eq!(cloned, Ok(12));\n  1737:     /// ```\n  1738:     #[inline]\n  1739:     #[stable(feature = \"result_cloned\", since = \"1.59.0\")]\n  1740:     pub fn cloned(self) -> Result<T, E>\n  1741:     where\n  1742:         T: Clone,\n  1743:     {\n  1744:         self.map(|t| t.clone())\n  1745:     }\n  1746: }\n  1747: \n  1748: impl<T, E> Result<&mut T, E> {\n  1749:     /// Maps a `Result<&mut T, E>` to a `Result<T, E>` by copying the contents of the\n  1750:     /// `Ok` part.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::copied",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state",
      "multiple_rust_declarations_share_path"
    ],
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
                      "id": 6,
                      "path": "Copy"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "copied",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
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
        "impl_id": "core:29313",
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
    "verification_source": "  1695:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by copying the contents of the\n  1696:     /// `Ok` part.\n  1697:     ///\n  1698:     /// # Examples\n  1699:     ///\n  1700:     /// ```\n  1701:     /// let val = 12;\n  1702:     /// let x: Result<&i32, i32> = Ok(&val);\n  1703:     /// assert_eq!(x, Ok(&12));\n  1704:     /// let copied = x.copied();\n  1705:     /// assert_eq!(copied, Ok(12));\n  1706:     /// ```\n  1707:     #[inline]\n  1708:     #[stable(feature = \"result_copied\", since = \"1.59.0\")]\n  1709:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1710:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1711:     pub const fn copied(self) -> Result<T, E>\n  1712:     where\n  1713:         T: Copy,\n  1714:     {\n  1715:         // FIXME(const-hack): this implementation, which sidesteps using `Result::map` since it's not const\n  1716:         // ready yet, should be reverted when possible to avoid code repetition\n  1717:         match self {\n  1718:             Ok(&v) => Ok(v),\n  1719:             Err(e) => Err(e),\n  1720:         }\n  1721:     }\n  1722: \n  1723:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by cloning the contents of the\n  1724:     /// `Ok` part.\n  1725:     ///\n  1726:     /// # Examples\n  1727:     ///",
    "nanvix_source": "  1704:     /// let val = 12;\n  1705:     /// let x: Result<&i32, i32> = Ok(&val);\n  1706:     /// assert_eq!(x, Ok(&12));\n  1707:     /// let copied = x.copied();\n  1708:     /// assert_eq!(copied, Ok(12));\n  1709:     /// ```\n  1710:     #[inline]\n  1711:     #[stable(feature = \"result_copied\", since = \"1.59.0\")]\n  1712:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1713:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1714:     pub const fn copied(self) -> Result<T, E>\n  1715:     where\n  1716:         T: Copy,\n  1717:     {\n  1718:         // FIXME(const-hack): this implementation, which sidesteps using `Result::map` since it's not const\n  1719:         // ready yet, should be reverted when possible to avoid code repetition\n  1720:         match self {\n  1721:             Ok(&v) => Ok(v),\n  1722:             Err(e) => Err(e),\n  1723:         }\n  1724:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::err",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": [
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
      "name": "err",
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
                      "generic": "E"
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
    "verification_source": "   720:     ///\n   721:     /// Converts `self` into an [`Option<E>`], consuming `self`,\n   722:     /// and discarding the success value, if any.\n   723:     ///\n   724:     /// # Examples\n   725:     ///\n   726:     /// ```\n   727:     /// let x: Result<u32, &str> = Ok(2);\n   728:     /// assert_eq!(x.err(), None);\n   729:     ///\n   730:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   731:     /// assert_eq!(x.err(), Some(\"Nothing here\"));\n   732:     /// ```\n   733:     #[inline]\n   734:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   735:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   736:     pub const fn err(self) -> Option<E>\n   737:     where\n   738:         T: [const] Destruct,\n   739:         E: [const] Destruct,\n   740:     {\n   741:         match self {\n   742:             Ok(_) => None,\n   743:             Err(x) => Some(x),\n   744:         }\n   745:     }\n   746: \n   747:     /////////////////////////////////////////////////////////////////////////\n   748:     // Adapter for working with references\n   749:     /////////////////////////////////////////////////////////////////////////\n   750: \n   751:     /// Converts from `&Result<T, E>` to `Result<&T, &E>`.\n   752:     ///",
    "nanvix_source": "   726:     /// ```\n   727:     /// let x: Result<u32, &str> = Ok(2);\n   728:     /// assert_eq!(x.err(), None);\n   729:     ///\n   730:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   731:     /// assert_eq!(x.err(), Some(\"Nothing here\"));\n   732:     /// ```\n   733:     #[inline]\n   734:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   735:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   736:     pub const fn err(self) -> Option<E>\n   737:     where\n   738:         T: [const] Destruct,\n   739:         E: [const] Destruct,\n   740:     {\n   741:         match self {\n   742:             Ok(_) => None,\n   743:             Err(x) => Some(x),\n   744:         }\n   745:     }\n   746: ",
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
