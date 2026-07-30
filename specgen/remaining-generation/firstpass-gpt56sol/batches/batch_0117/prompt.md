For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::OnceCell::get",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "get",
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
    "verification_source": "    39: \n    40: impl<T> OnceCell<T> {\n    41:     /// Creates a new uninitialized cell.\n    42:     #[inline]\n    43:     #[must_use]\n    44:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    45:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n    46:     pub const fn new() -> OnceCell<T> {\n    47:         OnceCell { inner: UnsafeCell::new(None) }\n    48:     }\n    49: \n    50:     /// Gets the reference to the underlying value.\n    51:     ///\n    52:     /// Returns `None` if the cell is uninitialized.\n    53:     #[inline]\n    54:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant\n    57:         unsafe { &*self.inner.get() }.as_ref()\n    58:     }\n    59: \n    60:     /// Gets the mutable reference to the underlying value.\n    61:     ///\n    62:     /// Returns `None` if the cell is uninitialized.\n    63:     #[inline]\n    64:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    65:     pub fn get_mut(&mut self) -> Option<&mut T> {\n    66:         self.inner.get_mut().as_mut()\n    67:     }\n    68: \n    69:     /// Initializes the contents of the cell to `value`.\n    70:     ///\n    71:     /// # Errors",
    "nanvix_source": "    45:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n    46:     pub const fn new() -> OnceCell<T> {\n    47:         OnceCell { inner: UnsafeCell::new(None) }\n    48:     }\n    49: \n    50:     /// Gets the reference to the underlying value.\n    51:     ///\n    52:     /// Returns `None` if the cell is uninitialized.\n    53:     #[inline]\n    54:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant\n    57:         unsafe { &*self.inner.get() }.as_ref()\n    58:     }\n    59: \n    60:     /// Gets the mutable reference to the underlying value.\n    61:     ///\n    62:     /// Returns `None` if the cell is uninitialized.\n    63:     #[inline]\n    64:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    65:     pub fn get_mut(&mut self) -> Option<&mut T> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::into_inner",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "into_inner",
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
    "verification_source": "   307:     /// # Examples\n   308:     ///\n   309:     /// ```\n   310:     /// use std::cell::OnceCell;\n   311:     ///\n   312:     /// let cell: OnceCell<String> = OnceCell::new();\n   313:     /// assert_eq!(cell.into_inner(), None);\n   314:     ///\n   315:     /// let cell = OnceCell::new();\n   316:     /// let _ = cell.set(\"hello\".to_owned());\n   317:     /// assert_eq!(cell.into_inner(), Some(\"hello\".to_owned()));\n   318:     /// ```\n   319:     #[inline]\n   320:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   321:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   322:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   323:     pub const fn into_inner(self) -> Option<T> {\n   324:         // Because `into_inner` takes `self` by value, the compiler statically verifies\n   325:         // that it is not currently borrowed. So it is safe to move out `Option<T>`.\n   326:         self.inner.into_inner()\n   327:     }\n   328: \n   329:     /// Takes the value out of this `OnceCell`, moving it back to an uninitialized state.\n   330:     ///\n   331:     /// Has no effect and returns `None` if the `OnceCell` is uninitialized.\n   332:     ///\n   333:     /// Safety is guaranteed by requiring a mutable reference.\n   334:     ///\n   335:     /// # Examples\n   336:     ///\n   337:     /// ```\n   338:     /// use std::cell::OnceCell;\n   339:     ///",
    "nanvix_source": "   313:     /// assert_eq!(cell.into_inner(), None);\n   314:     ///\n   315:     /// let cell = OnceCell::new();\n   316:     /// let _ = cell.set(\"hello\".to_owned());\n   317:     /// assert_eq!(cell.into_inner(), Some(\"hello\".to_owned()));\n   318:     /// ```\n   319:     #[inline]\n   320:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   321:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   322:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   323:     pub const fn into_inner(self) -> Option<T> {\n   324:         // Because `into_inner` takes `self` by value, the compiler statically verifies\n   325:         // that it is not currently borrowed. So it is safe to move out `Option<T>`.\n   326:         self.inner.into_inner()\n   327:     }\n   328: \n   329:     /// Takes the value out of this `OnceCell`, moving it back to an uninitialized state.\n   330:     ///\n   331:     /// Has no effect and returns `None` if the `OnceCell` is uninitialized.\n   332:     ///\n   333:     /// Safety is guaranteed by requiring a mutable reference.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "inputs": [],
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9782,
            "path": "OnceCell"
          }
        }
      }
    },
    "verification_source": "    30: /// });\n    31: /// assert_eq!(value, \"Hello, World!\");\n    32: /// assert!(cell.get().is_some());\n    33: /// ```\n    34: #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    35: pub struct OnceCell<T> {\n    36:     // Invariant: written to at most once.\n    37:     inner: UnsafeCell<Option<T>>,\n    38: }\n    39: \n    40: impl<T> OnceCell<T> {\n    41:     /// Creates a new uninitialized cell.\n    42:     #[inline]\n    43:     #[must_use]\n    44:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    45:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n    46:     pub const fn new() -> OnceCell<T> {\n    47:         OnceCell { inner: UnsafeCell::new(None) }\n    48:     }\n    49: \n    50:     /// Gets the reference to the underlying value.\n    51:     ///\n    52:     /// Returns `None` if the cell is uninitialized.\n    53:     #[inline]\n    54:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant\n    57:         unsafe { &*self.inner.get() }.as_ref()\n    58:     }\n    59: \n    60:     /// Gets the mutable reference to the underlying value.\n    61:     ///\n    62:     /// Returns `None` if the cell is uninitialized.",
    "nanvix_source": "    36:     // Invariant: written to at most once.\n    37:     inner: UnsafeCell<Option<T>>,\n    38: }\n    39: \n    40: impl<T> OnceCell<T> {\n    41:     /// Creates a new uninitialized cell.\n    42:     #[inline]\n    43:     #[must_use]\n    44:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    45:     #[rustc_const_stable(feature = \"once_cell\", since = \"1.70.0\")]\n    46:     pub const fn new() -> OnceCell<T> {\n    47:         OnceCell { inner: UnsafeCell::new(None) }\n    48:     }\n    49: \n    50:     /// Gets the reference to the underlying value.\n    51:     ///\n    52:     /// Returns `None` if the cell is uninitialized.\n    53:     #[inline]\n    54:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    55:     pub fn get(&self) -> Option<&T> {\n    56:         // SAFETY: Safe due to `inner`'s invariant",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::set",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "set",
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
            "value",
            {
              "generic": "T"
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
                      "generic": "T"
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
    "verification_source": "    76:     /// # Examples\n    77:     ///\n    78:     /// ```\n    79:     /// use std::cell::OnceCell;\n    80:     ///\n    81:     /// let cell = OnceCell::new();\n    82:     /// assert!(cell.get().is_none());\n    83:     ///\n    84:     /// assert_eq!(cell.set(92), Ok(()));\n    85:     /// assert_eq!(cell.set(62), Err(62));\n    86:     ///\n    87:     /// assert!(cell.get().is_some());\n    88:     /// ```\n    89:     #[inline]\n    90:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    91:     #[rustc_should_not_be_called_on_const_items]\n    92:     pub fn set(&self, value: T) -> Result<(), T> {\n    93:         match self.try_insert(value) {\n    94:             Ok(_) => Ok(()),\n    95:             Err((_, value)) => Err(value),\n    96:         }\n    97:     }\n    98: \n    99:     /// Initializes the contents of the cell to `value` if the cell was\n   100:     /// uninitialized, then returns a reference to it.\n   101:     ///\n   102:     /// # Errors\n   103:     ///\n   104:     /// This method returns `Ok(&value)` if the cell was uninitialized\n   105:     /// and `Err((&current_value, value))` if it was already initialized.\n   106:     ///\n   107:     /// # Examples\n   108:     ///",
    "nanvix_source": "    82:     /// assert!(cell.get().is_none());\n    83:     ///\n    84:     /// assert_eq!(cell.set(92), Ok(()));\n    85:     /// assert_eq!(cell.set(62), Err(62));\n    86:     ///\n    87:     /// assert!(cell.get().is_some());\n    88:     /// ```\n    89:     #[inline]\n    90:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n    91:     #[rustc_should_not_be_called_on_const_items]\n    92:     pub fn set(&self, value: T) -> Result<(), T> {\n    93:         match self.try_insert(value) {\n    94:             Ok(_) => Ok(()),\n    95:             Err((_, value)) => Err(value),\n    96:         }\n    97:     }\n    98: \n    99:     /// Initializes the contents of the cell to `value` if the cell was\n   100:     /// uninitialized, then returns a reference to it.\n   101:     ///\n   102:     /// # Errors",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::OnceCell::take",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "take",
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
                      "generic": "T"
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
    "verification_source": "   334:     ///\n   335:     /// # Examples\n   336:     ///\n   337:     /// ```\n   338:     /// use std::cell::OnceCell;\n   339:     ///\n   340:     /// let mut cell: OnceCell<String> = OnceCell::new();\n   341:     /// assert_eq!(cell.take(), None);\n   342:     ///\n   343:     /// let mut cell = OnceCell::new();\n   344:     /// let _ = cell.set(\"hello\".to_owned());\n   345:     /// assert_eq!(cell.take(), Some(\"hello\".to_owned()));\n   346:     /// assert_eq!(cell.get(), None);\n   347:     /// ```\n   348:     #[inline]\n   349:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   350:     pub fn take(&mut self) -> Option<T> {\n   351:         mem::take(self).into_inner()\n   352:     }\n   353: }\n   354: \n   355: #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   356: #[rustc_const_unstable(feature = \"const_default\", issue = \"143894\")]\n   357: impl<T> const Default for OnceCell<T> {\n   358:     #[inline]\n   359:     fn default() -> Self {\n   360:         Self::new()\n   361:     }\n   362: }\n   363: \n   364: #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   365: impl<T: fmt::Debug> fmt::Debug for OnceCell<T> {\n   366:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
    "nanvix_source": "   340:     /// let mut cell: OnceCell<String> = OnceCell::new();\n   341:     /// assert_eq!(cell.take(), None);\n   342:     ///\n   343:     /// let mut cell = OnceCell::new();\n   344:     /// let _ = cell.set(\"hello\".to_owned());\n   345:     /// assert_eq!(cell.take(), Some(\"hello\".to_owned()));\n   346:     /// assert_eq!(cell.get(), None);\n   347:     /// ```\n   348:     #[inline]\n   349:     #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   350:     pub fn take(&mut self) -> Option<T> {\n   351:         mem::take(self).into_inner()\n   352:     }\n   353: }\n   354: \n   355: #[stable(feature = \"once_cell\", since = \"1.70.0\")]\n   356: #[rustc_const_unstable(feature = \"const_default\", issue = \"143894\")]\n   357: const impl<T> Default for OnceCell<T> {\n   358:     #[inline]\n   359:     fn default() -> Self {\n   360:         Self::new()",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::Ref::clone",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "clone",
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
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
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
      }
    },
    "verification_source": "  1634: #[unstable(feature = \"deref_pure_trait\", issue = \"87121\")]\n  1635: unsafe impl<T: ?Sized> DerefPure for Ref<'_, T> {}\n  1636: \n  1637: impl<'b, T: ?Sized> Ref<'b, T> {\n  1638:     /// Copies a `Ref`.\n  1639:     ///\n  1640:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1641:     ///\n  1642:     /// This is an associated function that needs to be used as\n  1643:     /// `Ref::clone(...)`. A `Clone` implementation or a method would interfere\n  1644:     /// with the widespread use of `r.borrow().clone()` to clone the contents of\n  1645:     /// a `RefCell`.\n  1646:     #[stable(feature = \"cell_extras\", since = \"1.15.0\")]\n  1647:     #[must_use]\n  1648:     #[inline]\n  1649:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1650:     pub const fn clone(orig: &Ref<'b, T>) -> Ref<'b, T> {\n  1651:         Ref { value: orig.value, borrow: orig.borrow.clone() }\n  1652:     }\n  1653: \n  1654:     /// Makes a new `Ref` for a component of the borrowed data.\n  1655:     ///\n  1656:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1657:     ///\n  1658:     /// This is an associated function that needs to be used as `Ref::map(...)`.\n  1659:     /// A method would interfere with methods of the same name on the contents\n  1660:     /// of a `RefCell` used through `Deref`.\n  1661:     ///\n  1662:     /// # Examples\n  1663:     ///\n  1664:     /// ```\n  1665:     /// use std::cell::{RefCell, Ref};\n  1666:     ///",
    "nanvix_source": "  1640:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1641:     ///\n  1642:     /// This is an associated function that needs to be used as\n  1643:     /// `Ref::clone(...)`. A `Clone` implementation or a method would interfere\n  1644:     /// with the widespread use of `r.borrow().clone()` to clone the contents of\n  1645:     /// a `RefCell`.\n  1646:     #[stable(feature = \"cell_extras\", since = \"1.15.0\")]\n  1647:     #[must_use]\n  1648:     #[inline]\n  1649:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1650:     pub const fn clone(orig: &Ref<'b, T>) -> Ref<'b, T> {\n  1651:         Ref { value: orig.value, borrow: orig.borrow.clone() }\n  1652:     }\n  1653: \n  1654:     /// Makes a new `Ref` for a component of the borrowed data.\n  1655:     ///\n  1656:     /// The `RefCell` is already immutably borrowed, so this cannot fail.\n  1657:     ///\n  1658:     /// This is an associated function that needs to be used as `Ref::map(...)`.\n  1659:     /// A method would interfere with methods of the same name on the contents\n  1660:     /// of a `RefCell` used through `Deref`.",
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
