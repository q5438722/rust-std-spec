For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::array::map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
            "name": "U"
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
                      "id": 22,
                      "path": "FnMut"
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
          "array": {
            "len": "N",
            "type": {
              "generic": "T"
            }
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
                "const": {
                  "default": null,
                  "type": {
                    "primitive": "usize"
                  }
                }
              },
              "name": "N"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51748",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
          "array": {
            "len": "N",
            "type": {
              "generic": "U"
            }
          }
        }
      }
    },
    "verification_source": "   567:     /// let x = [1, 2, 3];\n   568:     /// let y = x.map(|v| v + 1);\n   569:     /// assert_eq!(y, [2, 3, 4]);\n   570:     ///\n   571:     /// let x = [1, 2, 3];\n   572:     /// let mut temp = 0;\n   573:     /// let y = x.map(|v| { temp += 1; v * temp });\n   574:     /// assert_eq!(y, [1, 4, 9]);\n   575:     ///\n   576:     /// let x = [\"Ferris\", \"Bueller's\", \"Day\", \"Off\"];\n   577:     /// let y = x.map(|v| v.len());\n   578:     /// assert_eq!(y, [6, 9, 3, 3]);\n   579:     /// ```\n   580:     #[must_use]\n   581:     #[stable(feature = \"array_map\", since = \"1.55.0\")]\n   582:     #[rustc_const_unstable(feature = \"const_array\", issue = \"147606\")]\n   583:     pub const fn map<F, U>(self, f: F) -> [U; N]\n   584:     where\n   585:         F: [const] FnMut(T) -> U + [const] Destruct,\n   586:         U: [const] Destruct,\n   587:         T: [const] Destruct,\n   588:     {\n   589:         self.try_map(NeverShortCircuit::wrap_mut_1(f)).0\n   590:     }\n   591: \n   592:     /// A fallible function `f` applied to each element on array `self` in order to\n   593:     /// return an array the same size as `self` or the first error encountered.\n   594:     ///\n   595:     /// The return type of this function depends on the return type of the closure.\n   596:     /// If you return `Result<T, E>` from the closure, you'll get a `Result<[T; N], E>`.\n   597:     /// If you return `Option<T>` from the closure, you'll get an `Option<[T; N]>`.\n   598:     ///\n   599:     /// # Examples",
    "nanvix_source": "   582:     /// let y = x.map(|v| { temp += 1; v * temp });\n   583:     /// assert_eq!(y, [1, 4, 9]);\n   584:     ///\n   585:     /// let x = [\"Ferris\", \"Bueller's\", \"Day\", \"Off\"];\n   586:     /// let y = x.map(|v| v.len());\n   587:     /// assert_eq!(y, [6, 9, 3, 3]);\n   588:     /// ```\n   589:     #[must_use]\n   590:     #[stable(feature = \"array_map\", since = \"1.55.0\")]\n   591:     #[rustc_const_unstable(feature = \"const_array\", issue = \"147606\")]\n   592:     pub const fn map<F, U>(self, f: F) -> [U; N]\n   593:     where\n   594:         F: [const] FnMut(T) -> U + [const] Destruct,\n   595:         U: [const] Destruct,\n   596:         T: [const] Destruct,\n   597:     {\n   598:         self.try_map(NeverShortCircuit::wrap_mut_1(f)).0\n   599:     }\n   600: \n   601:     /// A fallible function `f` applied to each element on array `self` in order to\n   602:     /// return an array the same size as `self` or the first error encountered.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::LazyCell::force",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
      "name": "force",
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11932,
            "path": "LazyCell"
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
                          "args": {
                            "parenthesized": {
                              "inputs": [],
                              "output": {
                                "generic": "T"
                              }
                            }
                          },
                          "id": 24,
                          "path": "FnOnce"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24688",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11932",
        "resolved_owner_path": [
          "core",
          "cell",
          "lazy",
          "LazyCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
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
                              "generic": "F"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 11932,
                    "path": "LazyCell"
                  }
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
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   122:     /// [`new()`]: LazyCell::new\n   123:     /// [`force()`]: LazyCell::force\n   124:     ///\n   125:     /// # Examples\n   126:     ///\n   127:     /// ```\n   128:     /// use std::cell::LazyCell;\n   129:     ///\n   130:     /// let lazy = LazyCell::new(|| 92);\n   131:     ///\n   132:     /// assert_eq!(LazyCell::force(&lazy), &92);\n   133:     /// assert_eq!(&*lazy, &92);\n   134:     /// ```\n   135:     #[inline]\n   136:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   137:     #[rustc_should_not_be_called_on_const_items]\n   138:     pub fn force(this: &LazyCell<T, F>) -> &T {\n   139:         // SAFETY:\n   140:         // This invalidates any mutable references to the data. The resulting\n   141:         // reference lives either until the end of the borrow of `this` (in the\n   142:         // initialized case) or is invalidated in `really_init` (in the\n   143:         // uninitialized case; `really_init` will create and return a fresh reference).\n   144:         let state = unsafe { &*this.state.get() };\n   145:         match state {\n   146:             State::Init(data) => data,\n   147:             // SAFETY: The state is uninitialized.\n   148:             State::Uninit(_) => unsafe { LazyCell::really_init(this) },\n   149:             State::Poisoned => panic_poisoned(),\n   150:         }\n   151:     }\n   152: \n   153:     /// Forces the evaluation of this lazy value and returns a mutable reference to\n   154:     /// the result.",
    "nanvix_source": "   128:     /// use std::cell::LazyCell;\n   129:     ///\n   130:     /// let lazy = LazyCell::new(|| 92);\n   131:     ///\n   132:     /// assert_eq!(LazyCell::force(&lazy), &92);\n   133:     /// assert_eq!(&*lazy, &92);\n   134:     /// ```\n   135:     #[inline]\n   136:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n   137:     #[rustc_should_not_be_called_on_const_items]\n   138:     pub fn force(this: &LazyCell<T, F>) -> &T {\n   139:         // SAFETY:\n   140:         // This invalidates any mutable references to the data. The resulting\n   141:         // reference lives either until the end of the borrow of `this` (in the\n   142:         // initialized case) or is invalidated in `really_init` (in the\n   143:         // uninitialized case; `really_init` will create and return a fresh reference).\n   144:         let state = unsafe { &*this.state.get() };\n   145:         match state {\n   146:             State::Init(data) => data,\n   147:             // SAFETY: The state is uninitialized.\n   148:             State::Uninit(_) => unsafe { LazyCell::really_init(this) },",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::LazyCell::new",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11932,
            "path": "LazyCell"
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
                          "args": {
                            "parenthesized": {
                              "inputs": [],
                              "output": {
                                "generic": "T"
                              }
                            }
                          },
                          "id": 24,
                          "path": "FnOnce"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "F"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24688",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11932",
        "resolved_owner_path": [
          "core",
          "cell",
          "lazy",
          "LazyCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "f",
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
            "id": 11932,
            "path": "LazyCell"
          }
        }
      }
    },
    "verification_source": "    59:     /// Creates a new lazy value with the given initializing function.\n    60:     ///\n    61:     /// # Examples\n    62:     ///\n    63:     /// ```\n    64:     /// use std::cell::LazyCell;\n    65:     ///\n    66:     /// let hello = \"Hello, World!\".to_string();\n    67:     ///\n    68:     /// let lazy = LazyCell::new(|| hello.to_uppercase());\n    69:     ///\n    70:     /// assert_eq!(&*lazy, \"HELLO, WORLD!\");\n    71:     /// ```\n    72:     #[inline]\n    73:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n    74:     #[rustc_const_stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n    75:     pub const fn new(f: F) -> LazyCell<T, F> {\n    76:         LazyCell { state: UnsafeCell::new(State::Uninit(f)) }\n    77:     }\n    78: \n    79:     /// Consumes this `LazyCell` returning the stored value.\n    80:     ///\n    81:     /// Returns `Ok(value)` if `Lazy` is initialized and `Err(f)` otherwise.\n    82:     ///\n    83:     /// # Panics\n    84:     ///\n    85:     /// Panics if the cell is poisoned.\n    86:     ///\n    87:     /// # Examples\n    88:     ///\n    89:     /// ```\n    90:     /// #![feature(lazy_cell_into_inner)]\n    91:     ///",
    "nanvix_source": "    65:     ///\n    66:     /// let hello = \"Hello, World!\".to_string();\n    67:     ///\n    68:     /// let lazy = LazyCell::new(|| hello.to_uppercase());\n    69:     ///\n    70:     /// assert_eq!(&*lazy, \"HELLO, WORLD!\");\n    71:     /// ```\n    72:     #[inline]\n    73:     #[stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n    74:     #[rustc_const_stable(feature = \"lazy_cell\", since = \"1.80.0\")]\n    75:     pub const fn new(f: F) -> LazyCell<T, F> {\n    76:         LazyCell { state: UnsafeCell::new(State::Uninit(f)) }\n    77:     }\n    78: \n    79:     /// Consumes this `LazyCell` returning the stored value.\n    80:     ///\n    81:     /// Returns `Ok(value)` if `Lazy` is initialized and `Err(f)` otherwise.\n    82:     ///\n    83:     /// # Panics\n    84:     ///\n    85:     /// Panics if the cell is poisoned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::get_or_init",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [],
                          "output": {
                            "generic": "T"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "get_or_init",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9782,
            "path": "OnceCell"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24718",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9782",
        "resolved_owner_path": [
          "core",
          "cell",
          "once",
          "OnceCell"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   147:     /// so results in a panic.\n   148:     ///\n   149:     /// # Examples\n   150:     ///\n   151:     /// ```\n   152:     /// use std::cell::OnceCell;\n   153:     ///\n   154:     /// let cell = OnceCell::new();\n   155:     /// let value = cell.get_or_init(|| 92);\n   156:     /// assert_eq!(value, &92);\n   157:     /// let value = cell.get_or_init(|| unreachable!());\n   158:     /// assert_eq!(value, &92);\n   159:     /// ```\n   160:     #[inline]\n   161:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   162:     #[rustc_should_not_be_called_on_const_items]\n   163:     pub fn get_or_init<F>(&self, f: F) -> &T\n   164:     where\n   165:         F: FnOnce() -> T,\n   166:     {\n   167:         match self.get_or_try_init(|| Ok::<T, !>(f())) {\n   168:             Ok(val) => val,\n   169:         }\n   170:     }\n   171: \n   172:     /// Gets the mutable reference of the contents of the cell,\n   173:     /// initializing it to `f()` if the cell was uninitialized.\n   174:     ///\n   175:     /// # Panics\n   176:     ///\n   177:     /// If `f()` panics, the panic is propagated to the caller, and the cell\n   178:     /// remains uninitialized.\n   179:     ///",
    "nanvix_source": "   153:     ///\n   154:     /// let cell = OnceCell::new();\n   155:     /// let value = cell.get_or_init(|| 92);\n   156:     /// assert_eq!(value, &92);\n   157:     /// let value = cell.get_or_init(|| unreachable!());\n   158:     /// assert_eq!(value, &92);\n   159:     /// ```\n   160:     #[inline]\n   161:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   162:     #[rustc_should_not_be_called_on_const_items]\n   163:     pub fn get_or_init<F>(&self, f: F) -> &T\n   164:     where\n   165:         F: FnOnce() -> T,\n   166:     {\n   167:         match self.get_or_try_init(|| Ok::<T, !>(f())) {\n   168:             Ok(val) => val,\n   169:         }\n   170:     }\n   171: \n   172:     /// Gets the mutable reference of the contents of the cell,\n   173:     /// initializing it to `f()` if the cell was uninitialized.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Ref::filter_map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
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
                    "modifier": "none",
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
                                            "generic": "U"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "filter_map",
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
                    "lifetime": "'b"
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
            "id": 13316,
            "path": "Ref"
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
              "name": "'b"
            },
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
                          "id": 12,
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24842",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13316",
        "resolved_owner_path": [
          "core",
          "cell",
          "Ref"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13316,
                "path": "Ref"
              }
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
                                "lifetime": "'b"
                              },
                              {
                                "type": {
                                  "generic": "U"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 13316,
                        "path": "Ref"
                      }
                    }
                  },
                  {
                    "type": {
                      "generic": "Self"
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
    "verification_source": "  1687:     /// This is an associated function that needs to be used as\n  1688:     /// `Ref::filter_map(...)`. A method would interfere with methods of the same\n  1689:     /// name on the contents of a `RefCell` used through `Deref`.\n  1690:     ///\n  1691:     /// # Examples\n  1692:     ///\n  1693:     /// ```\n  1694:     /// use std::cell::{RefCell, Ref};\n  1695:     ///\n  1696:     /// let c = RefCell::new(vec![1, 2, 3]);\n  1697:     /// let b1: Ref<'_, Vec<u32>> = c.borrow();\n  1698:     /// let b2: Result<Ref<'_, u32>, _> = Ref::filter_map(b1, |v| v.get(1));\n  1699:     /// assert_eq!(*b2.unwrap(), 2);\n  1700:     /// ```\n  1701:     #[stable(feature = \"cell_filter_map\", since = \"1.63.0\")]\n  1702:     #[inline]\n  1703:     pub fn filter_map<U: ?Sized, F>(orig: Ref<'b, T>, f: F) -> Result<Ref<'b, U>, Self>\n  1704:     where\n  1705:         F: FnOnce(&T) -> Option<&U>,\n  1706:     {\n  1707:         match f(&*orig) {\n  1708:             Some(value) => Ok(Ref { value: NonNull::from(value), borrow: orig.borrow }),\n  1709:             None => Err(orig),\n  1710:         }\n  1711:     }\n  1712: \n  1713:     /// Tries to makes a new `Ref` for a component of the borrowed data.\n  1714:     /// On failure, the original guard is returned alongside with the error\n  1715:     /// returned by the closure.\n  1716:     ///\n  1717:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1718:     ///\n  1719:     /// This is an associated function that needs to be used as",
    "nanvix_source": "  1693:     /// ```\n  1694:     /// use std::cell::{RefCell, Ref};\n  1695:     ///\n  1696:     /// let c = RefCell::new(vec![1, 2, 3]);\n  1697:     /// let b1: Ref<'_, Vec<u32>> = c.borrow();\n  1698:     /// let b2: Result<Ref<'_, u32>, _> = Ref::filter_map(b1, |v| v.get(1));\n  1699:     /// assert_eq!(*b2.unwrap(), 2);\n  1700:     /// ```\n  1701:     #[stable(feature = \"cell_filter_map\", since = \"1.63.0\")]\n  1702:     #[inline]\n  1703:     pub fn filter_map<U: ?Sized, F>(orig: Ref<'b, T>, f: F) -> Result<Ref<'b, U>, Self>\n  1704:     where\n  1705:         F: FnOnce(&T) -> Option<&U>,\n  1706:     {\n  1707:         match f(&*orig) {\n  1708:             Some(value) => Ok(Ref { value: NonNull::from(value), borrow: orig.borrow }),\n  1709:             None => Err(orig),\n  1710:         }\n  1711:     }\n  1712: \n  1713:     /// Tries to makes a new `Ref` for a component of the borrowed data.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Ref::map",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
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
                        "id": 12,
                        "path": "Sized"
                      }
                    }
                  }
                ],
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
                    "modifier": "none",
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
                          "output": {
                            "borrowed_ref": {
                              "is_mutable": false,
                              "lifetime": null,
                              "type": {
                                "generic": "U"
                              }
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
        "is_const": false,
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
                    "lifetime": "'b"
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
            "id": 13316,
            "path": "Ref"
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
              "name": "'b"
            },
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
                          "id": 12,
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24842",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13316",
        "resolved_owner_path": [
          "core",
          "cell",
          "Ref"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "orig",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'b"
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
                "id": 13316,
                "path": "Ref"
              }
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'b"
                  },
                  {
                    "type": {
                      "generic": "U"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13316,
            "path": "Ref"
          }
        }
      }
    },
    "verification_source": "  1658:     /// This is an associated function that needs to be used as `Ref::map(...)`.\n  1659:     /// A method would interfere with methods of the same name on the contents\n  1660:     /// of a `RefCell` used through `Deref`.\n  1661:     ///\n  1662:     /// # Examples\n  1663:     ///\n  1664:     /// ```\n  1665:     /// use std::cell::{RefCell, Ref};\n  1666:     ///\n  1667:     /// let c = RefCell::new((5, 'b'));\n  1668:     /// let b1: Ref<'_, (u32, char)> = c.borrow();\n  1669:     /// let b2: Ref<'_, u32> = Ref::map(b1, |t| &t.0);\n  1670:     /// assert_eq!(*b2, 5)\n  1671:     /// ```\n  1672:     #[stable(feature = \"cell_map\", since = \"1.8.0\")]\n  1673:     #[inline]\n  1674:     pub fn map<U: ?Sized, F>(orig: Ref<'b, T>, f: F) -> Ref<'b, U>\n  1675:     where\n  1676:         F: FnOnce(&T) -> &U,\n  1677:     {\n  1678:         Ref { value: NonNull::from(f(&*orig)), borrow: orig.borrow }\n  1679:     }\n  1680: \n  1681:     /// Makes a new `Ref` for an optional component of the borrowed data. The\n  1682:     /// original guard is returned as an `Err(..)` if the closure returns\n  1683:     /// `None`.\n  1684:     ///\n  1685:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1686:     ///\n  1687:     /// This is an associated function that needs to be used as\n  1688:     /// `Ref::filter_map(...)`. A method would interfere with methods of the same\n  1689:     /// name on the contents of a `RefCell` used through `Deref`.\n  1690:     ///",
    "nanvix_source": "  1664:     /// ```\n  1665:     /// use std::cell::{RefCell, Ref};\n  1666:     ///\n  1667:     /// let c = RefCell::new((5, 'b'));\n  1668:     /// let b1: Ref<'_, (u32, char)> = c.borrow();\n  1669:     /// let b2: Ref<'_, u32> = Ref::map(b1, |t| &t.0);\n  1670:     /// assert_eq!(*b2, 5)\n  1671:     /// ```\n  1672:     #[stable(feature = \"cell_map\", since = \"1.8.0\")]\n  1673:     #[inline]\n  1674:     pub fn map<U: ?Sized, F>(orig: Ref<'b, T>, f: F) -> Ref<'b, U>\n  1675:     where\n  1676:         F: FnOnce(&T) -> &U,\n  1677:     {\n  1678:         Ref { value: NonNull::from(f(&*orig)), borrow: orig.borrow }\n  1679:     }\n  1680: \n  1681:     /// Makes a new `Ref` for an optional component of the borrowed data. The\n  1682:     /// original guard is returned as an `Err(..)` if the closure returns\n  1683:     /// `None`.\n  1684:     ///",
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
