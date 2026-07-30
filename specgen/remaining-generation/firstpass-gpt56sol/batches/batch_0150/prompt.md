For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::panic::PanicHookInfo::location",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "location",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
                            "id": 6625,
                            "path": "Location"
                          }
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   147:     /// panic::set_hook(Box::new(|panic_info| {\n   148:     ///     if let Some(location) = panic_info.location() {\n   149:     ///         println!(\"panic occurred in file '{}' at line {}\",\n   150:     ///             location.file(),\n   151:     ///             location.line(),\n   152:     ///         );\n   153:     ///     } else {\n   154:     ///         println!(\"panic occurred but can't get location information...\");\n   155:     ///     }\n   156:     /// }));\n   157:     ///\n   158:     /// panic!(\"Normal panic\");\n   159:     /// ```\n   160:     #[must_use]\n   161:     #[inline]\n   162:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   163:     pub fn location(&self) -> Option<&Location<'_>> {\n   164:         // NOTE: If this is changed to sometimes return None,\n   165:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n   166:         Some(&self.location)\n   167:     }\n   168: \n   169:     /// Returns whether the panic handler is allowed to unwind the stack from\n   170:     /// the point where the panic occurred.\n   171:     ///\n   172:     /// This is true for most kinds of panics with the exception of panics\n   173:     /// caused by trying to unwind out of a `Drop` implementation or a function\n   174:     /// whose ABI does not support unwinding.\n   175:     ///\n   176:     /// It is safe for a panic handler to unwind even when this function returns\n   177:     /// false, however this will simply cause the panic handler to be called\n   178:     /// again.\n   179:     #[must_use]",
    "nanvix_source": "   153:     ///     } else {\n   154:     ///         println!(\"panic occurred but can't get location information...\");\n   155:     ///     }\n   156:     /// }));\n   157:     ///\n   158:     /// panic!(\"Normal panic\");\n   159:     /// ```\n   160:     #[must_use]\n   161:     #[inline]\n   162:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   163:     pub fn location(&self) -> Option<&'static Location<'static>> {\n   164:         // NOTE: If this is changed to sometimes return None,\n   165:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n   166:         Some(self.location)\n   167:     }\n   168: \n   169:     /// Returns whether the panic handler is allowed to unwind the stack from\n   170:     /// the point where the panic occurred.\n   171:     ///\n   172:     /// This is true for most kinds of panics with the exception of panics\n   173:     /// caused by trying to unwind out of a `Drop` implementation or a function",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::PanicHookInfo::payload",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "payload",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
              "dyn_trait": {
                "lifetime": null,
                "traits": [
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 417,
                      "path": "Any"
                    }
                  },
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 6,
                      "path": "Send"
                    }
                  }
                ]
              }
            }
          }
        }
      }
    },
    "verification_source": "    79:     ///\n    80:     /// panic::set_hook(Box::new(|panic_info| {\n    81:     ///     if let Some(s) = panic_info.payload().downcast_ref::<&str>() {\n    82:     ///         println!(\"panic occurred: {s:?}\");\n    83:     ///     } else if let Some(s) = panic_info.payload().downcast_ref::<String>() {\n    84:     ///         println!(\"panic occurred: {s:?}\");\n    85:     ///     } else {\n    86:     ///         println!(\"panic occurred\");\n    87:     ///     }\n    88:     /// }));\n    89:     ///\n    90:     /// panic!(\"Normal panic\");\n    91:     /// ```\n    92:     #[must_use]\n    93:     #[inline]\n    94:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    95:     pub fn payload(&self) -> &(dyn Any + Send) {\n    96:         self.payload\n    97:     }\n    98: \n    99:     /// Returns the payload associated with the panic, if it is a string.\n   100:     ///\n   101:     /// This returns the payload if it is of type `&'static str` or `String`.\n   102:     ///\n   103:     /// A invocation of the `panic!()` macro in Rust 2021 or later will always result in a\n   104:     /// panic payload where `payload_as_str` returns `Some`.\n   105:     ///\n   106:     /// Only an invocation of [`panic_any`]\n   107:     /// (or, in Rust 2018 and earlier, `panic!(x)` where `x` is something other than a string)\n   108:     /// can result in a panic payload where `payload_as_str` returns `None`.\n   109:     ///\n   110:     /// # Example\n   111:     ///",
    "nanvix_source": "    85:     ///     } else {\n    86:     ///         println!(\"panic occurred\");\n    87:     ///     }\n    88:     /// }));\n    89:     ///\n    90:     /// panic!(\"Normal panic\");\n    91:     /// ```\n    92:     #[must_use]\n    93:     #[inline]\n    94:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    95:     pub fn payload(&self) -> &(dyn Any + Send) {\n    96:         self.payload\n    97:     }\n    98: \n    99:     /// Returns the payload associated with the panic, if it is a string.\n   100:     ///\n   101:     /// This returns the payload if it is of type `&'static str` or `String`.\n   102:     ///\n   103:     /// A invocation of the `panic!()` macro in Rust 2021 or later will always result in a\n   104:     /// panic payload where `payload_as_str` returns `Some`.\n   105:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::PanicHookInfo::payload_as_str",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "payload_as_str",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
                          "primitive": "str"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   110:     /// # Example\n   111:     ///\n   112:     /// ```should_panic\n   113:     /// std::panic::set_hook(Box::new(|panic_info| {\n   114:     ///     if let Some(s) = panic_info.payload_as_str() {\n   115:     ///         println!(\"panic occurred: {s:?}\");\n   116:     ///     } else {\n   117:     ///         println!(\"panic occurred\");\n   118:     ///     }\n   119:     /// }));\n   120:     ///\n   121:     /// panic!(\"Normal panic\");\n   122:     /// ```\n   123:     #[must_use]\n   124:     #[inline]\n   125:     #[stable(feature = \"panic_payload_as_str\", since = \"1.91.0\")]\n   126:     pub fn payload_as_str(&self) -> Option<&str> {\n   127:         if let Some(s) = self.payload.downcast_ref::<&str>() {\n   128:             Some(s)\n   129:         } else if let Some(s) = self.payload.downcast_ref::<String>() {\n   130:             Some(s)\n   131:         } else {\n   132:             None\n   133:         }\n   134:     }\n   135: \n   136:     /// Returns information about the location from which the panic originated,\n   137:     /// if available.\n   138:     ///\n   139:     /// This method will currently always return [`Some`], but this may change\n   140:     /// in future versions.\n   141:     ///\n   142:     /// # Examples",
    "nanvix_source": "   116:     ///     } else {\n   117:     ///         println!(\"panic occurred\");\n   118:     ///     }\n   119:     /// }));\n   120:     ///\n   121:     /// panic!(\"Normal panic\");\n   122:     /// ```\n   123:     #[must_use]\n   124:     #[inline]\n   125:     #[stable(feature = \"panic_payload_as_str\", since = \"1.91.0\")]\n   126:     pub fn payload_as_str(&self) -> Option<&str> {\n   127:         if let Some(s) = self.payload.downcast_ref::<&str>() {\n   128:             Some(s)\n   129:         } else if let Some(s) = self.payload.downcast_ref::<String>() {\n   130:             Some(s)\n   131:         } else {\n   132:             None\n   133:         }\n   134:     }\n   135: \n   136:     /// Returns information about the location from which the panic originated,",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::PanicInfo::location",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "location",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
                            "id": 6625,
                            "path": "Location"
                          }
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   147:     /// panic::set_hook(Box::new(|panic_info| {\n   148:     ///     if let Some(location) = panic_info.location() {\n   149:     ///         println!(\"panic occurred in file '{}' at line {}\",\n   150:     ///             location.file(),\n   151:     ///             location.line(),\n   152:     ///         );\n   153:     ///     } else {\n   154:     ///         println!(\"panic occurred but can't get location information...\");\n   155:     ///     }\n   156:     /// }));\n   157:     ///\n   158:     /// panic!(\"Normal panic\");\n   159:     /// ```\n   160:     #[must_use]\n   161:     #[inline]\n   162:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   163:     pub fn location(&self) -> Option<&Location<'_>> {\n   164:         // NOTE: If this is changed to sometimes return None,\n   165:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n   166:         Some(&self.location)\n   167:     }\n   168: \n   169:     /// Returns whether the panic handler is allowed to unwind the stack from\n   170:     /// the point where the panic occurred.\n   171:     ///\n   172:     /// This is true for most kinds of panics with the exception of panics\n   173:     /// caused by trying to unwind out of a `Drop` implementation or a function\n   174:     /// whose ABI does not support unwinding.\n   175:     ///\n   176:     /// It is safe for a panic handler to unwind even when this function returns\n   177:     /// false, however this will simply cause the panic handler to be called\n   178:     /// again.\n   179:     #[must_use]",
    "nanvix_source": "   153:     ///     } else {\n   154:     ///         println!(\"panic occurred but can't get location information...\");\n   155:     ///     }\n   156:     /// }));\n   157:     ///\n   158:     /// panic!(\"Normal panic\");\n   159:     /// ```\n   160:     #[must_use]\n   161:     #[inline]\n   162:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   163:     pub fn location(&self) -> Option<&'static Location<'static>> {\n   164:         // NOTE: If this is changed to sometimes return None,\n   165:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n   166:         Some(self.location)\n   167:     }\n   168: \n   169:     /// Returns whether the panic handler is allowed to unwind the stack from\n   170:     /// the point where the panic occurred.\n   171:     ///\n   172:     /// This is true for most kinds of panics with the exception of panics\n   173:     /// caused by trying to unwind out of a `Drop` implementation or a function",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::PanicInfo::payload",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "payload",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
              "dyn_trait": {
                "lifetime": null,
                "traits": [
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 417,
                      "path": "Any"
                    }
                  },
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 6,
                      "path": "Send"
                    }
                  }
                ]
              }
            }
          }
        }
      }
    },
    "verification_source": "    79:     ///\n    80:     /// panic::set_hook(Box::new(|panic_info| {\n    81:     ///     if let Some(s) = panic_info.payload().downcast_ref::<&str>() {\n    82:     ///         println!(\"panic occurred: {s:?}\");\n    83:     ///     } else if let Some(s) = panic_info.payload().downcast_ref::<String>() {\n    84:     ///         println!(\"panic occurred: {s:?}\");\n    85:     ///     } else {\n    86:     ///         println!(\"panic occurred\");\n    87:     ///     }\n    88:     /// }));\n    89:     ///\n    90:     /// panic!(\"Normal panic\");\n    91:     /// ```\n    92:     #[must_use]\n    93:     #[inline]\n    94:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    95:     pub fn payload(&self) -> &(dyn Any + Send) {\n    96:         self.payload\n    97:     }\n    98: \n    99:     /// Returns the payload associated with the panic, if it is a string.\n   100:     ///\n   101:     /// This returns the payload if it is of type `&'static str` or `String`.\n   102:     ///\n   103:     /// A invocation of the `panic!()` macro in Rust 2021 or later will always result in a\n   104:     /// panic payload where `payload_as_str` returns `Some`.\n   105:     ///\n   106:     /// Only an invocation of [`panic_any`]\n   107:     /// (or, in Rust 2018 and earlier, `panic!(x)` where `x` is something other than a string)\n   108:     /// can result in a panic payload where `payload_as_str` returns `None`.\n   109:     ///\n   110:     /// # Example\n   111:     ///",
    "nanvix_source": "    85:     ///     } else {\n    86:     ///         println!(\"panic occurred\");\n    87:     ///     }\n    88:     /// }));\n    89:     ///\n    90:     /// panic!(\"Normal panic\");\n    91:     /// ```\n    92:     #[must_use]\n    93:     #[inline]\n    94:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    95:     pub fn payload(&self) -> &(dyn Any + Send) {\n    96:         self.payload\n    97:     }\n    98: \n    99:     /// Returns the payload associated with the panic, if it is a string.\n   100:     ///\n   101:     /// This returns the payload if it is of type `&'static str` or `String`.\n   102:     ///\n   103:     /// A invocation of the `panic!()` macro in Rust 2021 or later will always result in a\n   104:     /// panic payload where `payload_as_str` returns `Some`.\n   105:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::PanicInfo::payload_as_str",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "payload_as_str",
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
            "id": 6615,
            "path": "PanicHookInfo"
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
        "impl_id": "std:6627",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6615",
        "resolved_owner_path": [
          "std",
          "panic",
          "PanicHookInfo"
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
                          "primitive": "str"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   110:     /// # Example\n   111:     ///\n   112:     /// ```should_panic\n   113:     /// std::panic::set_hook(Box::new(|panic_info| {\n   114:     ///     if let Some(s) = panic_info.payload_as_str() {\n   115:     ///         println!(\"panic occurred: {s:?}\");\n   116:     ///     } else {\n   117:     ///         println!(\"panic occurred\");\n   118:     ///     }\n   119:     /// }));\n   120:     ///\n   121:     /// panic!(\"Normal panic\");\n   122:     /// ```\n   123:     #[must_use]\n   124:     #[inline]\n   125:     #[stable(feature = \"panic_payload_as_str\", since = \"1.91.0\")]\n   126:     pub fn payload_as_str(&self) -> Option<&str> {\n   127:         if let Some(s) = self.payload.downcast_ref::<&str>() {\n   128:             Some(s)\n   129:         } else if let Some(s) = self.payload.downcast_ref::<String>() {\n   130:             Some(s)\n   131:         } else {\n   132:             None\n   133:         }\n   134:     }\n   135: \n   136:     /// Returns information about the location from which the panic originated,\n   137:     /// if available.\n   138:     ///\n   139:     /// This method will currently always return [`Some`], but this may change\n   140:     /// in future versions.\n   141:     ///\n   142:     /// # Examples",
    "nanvix_source": "   116:     ///     } else {\n   117:     ///         println!(\"panic occurred\");\n   118:     ///     }\n   119:     /// }));\n   120:     ///\n   121:     /// panic!(\"Normal panic\");\n   122:     /// ```\n   123:     #[must_use]\n   124:     #[inline]\n   125:     #[stable(feature = \"panic_payload_as_str\", since = \"1.91.0\")]\n   126:     pub fn payload_as_str(&self) -> Option<&str> {\n   127:         if let Some(s) = self.payload.downcast_ref::<&str>() {\n   128:             Some(s)\n   129:         } else if let Some(s) = self.payload.downcast_ref::<String>() {\n   130:             Some(s)\n   131:         } else {\n   132:             None\n   133:         }\n   134:     }\n   135: \n   136:     /// Returns information about the location from which the panic originated,",
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
