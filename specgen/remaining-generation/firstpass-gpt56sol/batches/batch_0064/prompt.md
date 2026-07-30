For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Result::and_then",
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
      "name": "and_then",
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
    "verification_source": "  1472:     ///\n  1473:     /// ```\n  1474:     /// use std::{io::ErrorKind, path::Path};\n  1475:     ///\n  1476:     /// // Note: on Windows \"/\" maps to \"C:\\\"\n  1477:     /// let root_modified_time = Path::new(\"/\").metadata().and_then(|md| md.modified());\n  1478:     /// assert!(root_modified_time.is_ok());\n  1479:     ///\n  1480:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1481:     /// assert!(should_fail.is_err());\n  1482:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1483:     /// ```\n  1484:     #[inline]\n  1485:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1486:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1487:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1488:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1489:     where\n  1490:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1491:     {\n  1492:         match self {\n  1493:             Ok(t) => op(t),\n  1494:             Err(e) => Err(e),\n  1495:         }\n  1496:     }\n  1497: \n  1498:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.\n  1499:     ///\n  1500:     /// Arguments passed to `or` are eagerly evaluated; if you are passing the\n  1501:     /// result of a function call, it is recommended to use [`or_else`], which is\n  1502:     /// lazily evaluated.\n  1503:     ///\n  1504:     /// [`or_else`]: Result::or_else",
    "nanvix_source": "  1476:     /// assert!(root_modified_time.is_ok());\n  1477:     ///\n  1478:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1479:     /// assert!(should_fail.is_err());\n  1480:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1481:     /// ```\n  1482:     #[inline]\n  1483:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1484:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1485:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1486:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1487:     where\n  1488:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1489:     {\n  1490:         match self {\n  1491:             Ok(t) => op(t),\n  1492:             Err(e) => Err(e),\n  1493:         }\n  1494:     }\n  1495: \n  1496:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::as_deref",
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
                      "id": 8635,
                      "path": "Deref"
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
      "name": "as_deref",
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
    "verification_source": "  1030:     /// and returns the new [`Result`].\n  1031:     ///\n  1032:     /// # Examples\n  1033:     ///\n  1034:     /// ```\n  1035:     /// let x: Result<String, u32> = Ok(\"hello\".to_string());\n  1036:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1037:     /// assert_eq!(x.as_deref(), y);\n  1038:     ///\n  1039:     /// let x: Result<String, u32> = Err(42);\n  1040:     /// let y: Result<&str, &u32> = Err(&42);\n  1041:     /// assert_eq!(x.as_deref(), y);\n  1042:     /// ```\n  1043:     #[inline]\n  1044:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1045:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1046:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1047:     where\n  1048:         T: [const] Deref,\n  1049:     {\n  1050:         self.as_ref().map(Deref::deref)\n  1051:     }\n  1052: \n  1053:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1054:     ///\n  1055:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1056:     /// and returns the new [`Result`].\n  1057:     ///\n  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());",
    "nanvix_source": "  1034:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1035:     /// assert_eq!(x.as_deref(), y);\n  1036:     ///\n  1037:     /// let x: Result<String, u32> = Err(42);\n  1038:     /// let y: Result<&str, &u32> = Err(&42);\n  1039:     /// assert_eq!(x.as_deref(), y);\n  1040:     /// ```\n  1041:     #[inline]\n  1042:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1043:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1044:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1045:     where\n  1046:         T: [const] Deref,\n  1047:     {\n  1048:         self.as_ref().map(Deref::deref)\n  1049:     }\n  1050: \n  1051:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1052:     ///\n  1053:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1054:     /// and returns the new [`Result`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::as_deref_mut",
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
    "target": "core::fmt::Result::as_mut",
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
    "target": "core::fmt::Result::as_ref",
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
    "target": "core::fmt::Result::cloned",
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
