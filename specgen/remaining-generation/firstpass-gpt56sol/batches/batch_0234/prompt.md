For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::LockResult::expect",
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
                "generic": "E"
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
      "name": "expect",
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
            "msg",
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1163:     /// let path = std::env::var(\"IMPORTANT_PATH\")\n  1164:     ///     .expect(\"env variable `IMPORTANT_PATH` should be set by `wrapper_script.sh`\");\n  1165:     /// ```\n  1166:     ///\n  1167:     /// **Hint**: If you're having trouble remembering how to phrase expect\n  1168:     /// error messages remember to focus on the word \"should\" as in \"env\n  1169:     /// variable should be set by blah\" or \"the given binary should be available\n  1170:     /// and executable by the current user\".\n  1171:     ///\n  1172:     /// For more detail on expect message styles and the reasoning behind our recommendation please\n  1173:     /// refer to the section on [\"Common Message\n  1174:     /// Styles\"](../../std/error/index.html#common-message-styles) in the\n  1175:     /// [`std::error`](../../std/error/index.html) module docs.\n  1176:     #[inline]\n  1177:     #[track_caller]\n  1178:     #[stable(feature = \"result_expect\", since = \"1.4.0\")]\n  1179:     pub fn expect(self, msg: &str) -> T\n  1180:     where\n  1181:         E: fmt::Debug,\n  1182:     {\n  1183:         match self {\n  1184:             Ok(t) => t,\n  1185:             Err(e) => unwrap_failed(msg, &e),\n  1186:         }\n  1187:     }\n  1188: \n  1189:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1190:     ///\n  1191:     /// Because this function may panic, its use is generally discouraged.\n  1192:     /// Panics are meant for unrecoverable errors, and\n  1193:     /// [may abort the entire program][panic-abort].\n  1194:     ///\n  1195:     /// Instead, prefer to use [the `?` (try) operator][try-operator], or pattern matching",
    "nanvix_source": "  1167:     /// variable should be set by blah\" or \"the given binary should be available\n  1168:     /// and executable by the current user\".\n  1169:     ///\n  1170:     /// For more detail on expect message styles and the reasoning behind our recommendation please\n  1171:     /// refer to the section on [\"Common Message\n  1172:     /// Styles\"](../../std/error/index.html#common-message-styles) in the\n  1173:     /// [`std::error`](../../std/error/index.html) module docs.\n  1174:     #[inline]\n  1175:     #[track_caller]\n  1176:     #[stable(feature = \"result_expect\", since = \"1.4.0\")]\n  1177:     pub fn expect(self, msg: &str) -> T\n  1178:     where\n  1179:         E: fmt::Debug,\n  1180:     {\n  1181:         match self {\n  1182:             Ok(t) => t,\n  1183:             Err(e) => unwrap_failed(msg, &e),\n  1184:         }\n  1185:     }\n  1186: \n  1187:     /// Returns the contained [`Ok`] value, consuming the `self` value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::expect_err",
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
      "name": "expect_err",
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
            "msg",
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
          "generic": "E"
        }
      }
    },
    "verification_source": "  1277:     ///\n  1278:     /// # Panics\n  1279:     ///\n  1280:     /// Panics if the value is an [`Ok`], with a panic message including the\n  1281:     /// passed message, and the content of the [`Ok`].\n  1282:     ///\n  1283:     ///\n  1284:     /// # Examples\n  1285:     ///\n  1286:     /// ```should_panic\n  1287:     /// let x: Result<u32, &str> = Ok(10);\n  1288:     /// x.expect_err(\"Testing expect_err\"); // panics with `Testing expect_err: 10`\n  1289:     /// ```\n  1290:     #[inline]\n  1291:     #[track_caller]\n  1292:     #[stable(feature = \"result_expect_err\", since = \"1.17.0\")]\n  1293:     pub fn expect_err(self, msg: &str) -> E\n  1294:     where\n  1295:         T: fmt::Debug,\n  1296:     {\n  1297:         match self {\n  1298:             Ok(t) => unwrap_failed(msg, &t),\n  1299:             Err(e) => e,\n  1300:         }\n  1301:     }\n  1302: \n  1303:     /// Returns the contained [`Err`] value, consuming the `self` value.\n  1304:     ///\n  1305:     /// # Panics\n  1306:     ///\n  1307:     /// Panics if the value is an [`Ok`], with a custom panic message provided\n  1308:     /// by the [`Ok`]'s value.\n  1309:     ///",
    "nanvix_source": "  1281:     ///\n  1282:     /// # Examples\n  1283:     ///\n  1284:     /// ```should_panic\n  1285:     /// let x: Result<u32, &str> = Ok(10);\n  1286:     /// x.expect_err(\"Testing expect_err\"); // panics with `Testing expect_err: 10`\n  1287:     /// ```\n  1288:     #[inline]\n  1289:     #[track_caller]\n  1290:     #[stable(feature = \"result_expect_err\", since = \"1.17.0\")]\n  1291:     pub fn expect_err(self, msg: &str) -> E\n  1292:     where\n  1293:         T: fmt::Debug,\n  1294:     {\n  1295:         match self {\n  1296:             Ok(t) => unwrap_failed(msg, &t),\n  1297:             Err(e) => e,\n  1298:         }\n  1299:     }\n  1300: \n  1301:     /// Returns the contained [`Err`] value, consuming the `self` value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::flatten",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "flatten",
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
        "impl_id": "core:29320",
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
    "verification_source": "  1836:     ///\n  1837:     /// let x: Result<Result<&'static str, u32>, u32> = Err(6);\n  1838:     /// assert_eq!(Err(6), x.flatten());\n  1839:     /// ```\n  1840:     ///\n  1841:     /// Flattening only removes one level of nesting at a time:\n  1842:     ///\n  1843:     /// ```\n  1844:     /// let x: Result<Result<Result<&'static str, u32>, u32>, u32> = Ok(Ok(Ok(\"hello\")));\n  1845:     /// assert_eq!(Ok(Ok(\"hello\")), x.flatten());\n  1846:     /// assert_eq!(Ok(\"hello\"), x.flatten().flatten());\n  1847:     /// ```\n  1848:     #[inline]\n  1849:     #[stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1850:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1851:     #[rustc_const_stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1852:     pub const fn flatten(self) -> Result<T, E> {\n  1853:         // FIXME(const-hack): could be written with `and_then`\n  1854:         match self {\n  1855:             Ok(inner) => inner,\n  1856:             Err(e) => Err(e),\n  1857:         }\n  1858:     }\n  1859: }\n  1860: \n  1861: // This is a separate function to reduce the code size of the methods\n  1862: #[cfg(not(panic = \"immediate-abort\"))]\n  1863: #[inline(never)]\n  1864: #[cold]\n  1865: #[track_caller]\n  1866: fn unwrap_failed(msg: &str, error: &dyn fmt::Debug) -> ! {\n  1867:     panic!(\"{msg}: {error:?}\");\n  1868: }",
    "nanvix_source": "  1845:     ///\n  1846:     /// ```\n  1847:     /// let x: Result<Result<Result<&'static str, u32>, u32>, u32> = Ok(Ok(Ok(\"hello\")));\n  1848:     /// assert_eq!(Ok(Ok(\"hello\")), x.flatten());\n  1849:     /// assert_eq!(Ok(\"hello\"), x.flatten().flatten());\n  1850:     /// ```\n  1851:     #[inline]\n  1852:     #[stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1853:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1854:     #[rustc_const_stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1855:     pub const fn flatten(self) -> Result<T, E> {\n  1856:         // FIXME(const-hack): could be written with `and_then`\n  1857:         match self {\n  1858:             Ok(inner) => inner,\n  1859:             Err(e) => Err(e),\n  1860:         }\n  1861:     }\n  1862: }\n  1863: \n  1864: // This is a separate function to reduce the code size of the methods\n  1865: #[cfg(not(panic = \"immediate-abort\"))]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::inspect",
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": null
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
      "name": "inspect",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "   972:     /// Calls a function with a reference to the contained value if [`Ok`].\n   973:     ///\n   974:     /// Returns the original result.\n   975:     ///\n   976:     /// # Examples\n   977:     ///\n   978:     /// ```\n   979:     /// let x: u8 = \"4\"\n   980:     ///     .parse::<u8>()\n   981:     ///     .inspect(|x| println!(\"original: {x}\"))\n   982:     ///     .map(|x| x.pow(3))\n   983:     ///     .expect(\"failed to parse number\");\n   984:     /// ```\n   985:     #[inline]\n   986:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n   987:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   988:     pub const fn inspect<F>(self, f: F) -> Self\n   989:     where\n   990:         F: [const] FnOnce(&T) + [const] Destruct,\n   991:     {\n   992:         if let Ok(ref t) = self {\n   993:             f(t);\n   994:         }\n   995: \n   996:         self\n   997:     }\n   998: \n   999:     /// Calls a function with a reference to the contained value if [`Err`].\n  1000:     ///\n  1001:     /// Returns the original result.\n  1002:     ///\n  1003:     /// # Examples\n  1004:     ///",
    "nanvix_source": "   976:     /// ```\n   977:     /// let x: u8 = \"4\"\n   978:     ///     .parse::<u8>()\n   979:     ///     .inspect(|x| println!(\"original: {x}\"))\n   980:     ///     .map(|x| x.pow(3))\n   981:     ///     .expect(\"failed to parse number\");\n   982:     /// ```\n   983:     #[inline]\n   984:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n   985:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   986:     pub const fn inspect<F>(self, f: F) -> Self\n   987:     where\n   988:         F: [const] FnOnce(&T) + [const] Destruct,\n   989:     {\n   990:         if let Ok(ref t) = self {\n   991:             f(t);\n   992:         }\n   993: \n   994:         self\n   995:     }\n   996: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::inspect_err",
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
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "E"
                                }
                              }
                            }
                          ],
                          "output": null
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
      "name": "inspect_err",
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
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1000:     ///\n  1001:     /// Returns the original result.\n  1002:     ///\n  1003:     /// # Examples\n  1004:     ///\n  1005:     /// ```\n  1006:     /// use std::{fs, io};\n  1007:     ///\n  1008:     /// fn read() -> io::Result<String> {\n  1009:     ///     fs::read_to_string(\"address.txt\")\n  1010:     ///         .inspect_err(|e| eprintln!(\"failed to read file: {e}\"))\n  1011:     /// }\n  1012:     /// ```\n  1013:     #[inline]\n  1014:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1015:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1016:     pub const fn inspect_err<F>(self, f: F) -> Self\n  1017:     where\n  1018:         F: [const] FnOnce(&E) + [const] Destruct,\n  1019:     {\n  1020:         if let Err(ref e) = self {\n  1021:             f(e);\n  1022:         }\n  1023: \n  1024:         self\n  1025:     }\n  1026: \n  1027:     /// Converts from `Result<T, E>` (or `&Result<T, E>`) to `Result<&<T as Deref>::Target, &E>`.\n  1028:     ///\n  1029:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`Deref`](crate::ops::Deref)\n  1030:     /// and returns the new [`Result`].\n  1031:     ///\n  1032:     /// # Examples",
    "nanvix_source": "  1004:     /// use std::{fs, io};\n  1005:     ///\n  1006:     /// fn read() -> io::Result<String> {\n  1007:     ///     fs::read_to_string(\"address.txt\")\n  1008:     ///         .inspect_err(|e| eprintln!(\"failed to read file: {e}\"))\n  1009:     /// }\n  1010:     /// ```\n  1011:     #[inline]\n  1012:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1013:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1014:     pub const fn inspect_err<F>(self, f: F) -> Self\n  1015:     where\n  1016:         F: [const] FnOnce(&E) + [const] Destruct,\n  1017:     {\n  1018:         if let Err(ref e) = self {\n  1019:             f(e);\n  1020:         }\n  1021: \n  1022:         self\n  1023:     }\n  1024: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::LockResult::is_err",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "is_err",
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
    "verification_source": "   630: \n   631:     /// Returns `true` if the result is [`Err`].\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```\n   636:     /// let x: Result<i32, &str> = Ok(-3);\n   637:     /// assert_eq!(x.is_err(), false);\n   638:     ///\n   639:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   640:     /// assert_eq!(x.is_err(), true);\n   641:     /// ```\n   642:     #[must_use = \"if you intended to assert that this is err, consider `.unwrap_err()` instead\"]\n   643:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   644:     #[inline]\n   645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   646:     pub const fn is_err(&self) -> bool {\n   647:         !self.is_ok()\n   648:     }\n   649: \n   650:     /// Returns `true` if the result is [`Err`] and the value inside of it matches a predicate.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::io::{Error, ErrorKind};\n   656:     ///\n   657:     /// let x: Result<u32, Error> = Err(Error::new(ErrorKind::NotFound, \"!\"));\n   658:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), true);\n   659:     ///\n   660:     /// let x: Result<u32, Error> = Err(Error::new(ErrorKind::PermissionDenied, \"!\"));\n   661:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   662:     ///",
    "nanvix_source": "   636:     /// let x: Result<i32, &str> = Ok(-3);\n   637:     /// assert_eq!(x.is_err(), false);\n   638:     ///\n   639:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   640:     /// assert_eq!(x.is_err(), true);\n   641:     /// ```\n   642:     #[must_use = \"if you intended to assert that this is err, consider `.unwrap_err()` instead\"]\n   643:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   644:     #[inline]\n   645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   646:     pub const fn is_err(&self) -> bool {\n   647:         !self.is_ok()\n   648:     }\n   649: \n   650:     /// Returns `true` if the result is [`Err`] and the value inside of it matches a predicate.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::io::{Error, ErrorKind};\n   656:     ///",
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
