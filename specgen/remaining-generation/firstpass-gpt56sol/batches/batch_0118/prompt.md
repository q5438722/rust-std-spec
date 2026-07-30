For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::RefCell::borrow",
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
      "name": "borrow",
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
            "id": 9393,
            "path": "RefCell"
          }
        },
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
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
            "id": 13316,
            "path": "Ref"
          }
        }
      }
    },
    "verification_source": "  1105:     ///\n  1106:     /// An example of panic:\n  1107:     ///\n  1108:     /// ```should_panic\n  1109:     /// use std::cell::RefCell;\n  1110:     ///\n  1111:     /// let c = RefCell::new(5);\n  1112:     ///\n  1113:     /// let m = c.borrow_mut();\n  1114:     /// let b = c.borrow(); // this causes a panic\n  1115:     /// ```\n  1116:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1117:     #[inline]\n  1118:     #[track_caller]\n  1119:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1120:     #[rustc_should_not_be_called_on_const_items]\n  1121:     pub const fn borrow(&self) -> Ref<'_, T> {\n  1122:         match self.try_borrow() {\n  1123:             Ok(b) => b,\n  1124:             Err(err) => panic_already_mutably_borrowed(err),\n  1125:         }\n  1126:     }\n  1127: \n  1128:     /// Immutably borrows the wrapped value, returning an error if the value is currently mutably\n  1129:     /// borrowed.\n  1130:     ///\n  1131:     /// The borrow lasts until the returned `Ref` exits scope. Multiple immutable borrows can be\n  1132:     /// taken out at the same time.\n  1133:     ///\n  1134:     /// This is the non-panicking variant of [`borrow`](#method.borrow).\n  1135:     ///\n  1136:     /// # Examples\n  1137:     ///",
    "nanvix_source": "  1111:     /// let c = RefCell::new(5);\n  1112:     ///\n  1113:     /// let m = c.borrow_mut();\n  1114:     /// let b = c.borrow(); // this causes a panic\n  1115:     /// ```\n  1116:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1117:     #[inline]\n  1118:     #[track_caller]\n  1119:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1120:     #[rustc_should_not_be_called_on_const_items]\n  1121:     pub const fn borrow(&self) -> Ref<'_, T> {\n  1122:         match self.try_borrow() {\n  1123:             Ok(b) => b,\n  1124:             Err(err) => panic_already_mutably_borrowed(err),\n  1125:         }\n  1126:     }\n  1127: \n  1128:     /// Immutably borrows the wrapped value, returning an error if the value is currently mutably\n  1129:     /// borrowed.\n  1130:     ///\n  1131:     /// The borrow lasts until the returned `Ref` exits scope. Multiple immutable borrows can be",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::borrow_mut",
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
      "name": "borrow_mut",
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
            "id": 9393,
            "path": "RefCell"
          }
        },
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
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
            "id": 13318,
            "path": "RefMut"
          }
        }
      }
    },
    "verification_source": "  1205:     ///\n  1206:     /// An example of panic:\n  1207:     ///\n  1208:     /// ```should_panic\n  1209:     /// use std::cell::RefCell;\n  1210:     ///\n  1211:     /// let c = RefCell::new(5);\n  1212:     /// let m = c.borrow();\n  1213:     ///\n  1214:     /// let b = c.borrow_mut(); // this causes a panic\n  1215:     /// ```\n  1216:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1217:     #[inline]\n  1218:     #[track_caller]\n  1219:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1220:     #[rustc_should_not_be_called_on_const_items]\n  1221:     pub const fn borrow_mut(&self) -> RefMut<'_, T> {\n  1222:         match self.try_borrow_mut() {\n  1223:             Ok(b) => b,\n  1224:             Err(err) => panic_already_borrowed(err),\n  1225:         }\n  1226:     }\n  1227: \n  1228:     /// Mutably borrows the wrapped value, returning an error if the value is currently borrowed.\n  1229:     ///\n  1230:     /// The borrow lasts until the returned `RefMut` or all `RefMut`s derived\n  1231:     /// from it exit scope. The value cannot be borrowed while this borrow is\n  1232:     /// active.\n  1233:     ///\n  1234:     /// This is the non-panicking variant of [`borrow_mut`](#method.borrow_mut).\n  1235:     ///\n  1236:     /// # Examples\n  1237:     ///",
    "nanvix_source": "  1211:     /// let c = RefCell::new(5);\n  1212:     /// let m = c.borrow();\n  1213:     ///\n  1214:     /// let b = c.borrow_mut(); // this causes a panic\n  1215:     /// ```\n  1216:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1217:     #[inline]\n  1218:     #[track_caller]\n  1219:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1220:     #[rustc_should_not_be_called_on_const_items]\n  1221:     pub const fn borrow_mut(&self) -> RefMut<'_, T> {\n  1222:         match self.try_borrow_mut() {\n  1223:             Ok(b) => b,\n  1224:             Err(err) => panic_already_borrowed(err),\n  1225:         }\n  1226:     }\n  1227: \n  1228:     /// Mutably borrows the wrapped value, returning an error if the value is currently borrowed.\n  1229:     ///\n  1230:     /// The borrow lasts until the returned `RefMut` or all `RefMut`s derived\n  1231:     /// from it exit scope. The value cannot be borrowed while this borrow is",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::into_inner",
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
            "id": 9393,
            "path": "RefCell"
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
        "impl_id": "core:24784",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   979: \n   980:     /// Consumes the `RefCell`, returning the wrapped value.\n   981:     ///\n   982:     /// # Examples\n   983:     ///\n   984:     /// ```\n   985:     /// use std::cell::RefCell;\n   986:     ///\n   987:     /// let c = RefCell::new(5);\n   988:     ///\n   989:     /// let five = c.into_inner();\n   990:     /// ```\n   991:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   992:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   993:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   994:     #[inline]\n   995:     pub const fn into_inner(self) -> T {\n   996:         // Since this function takes `self` (the `RefCell`) by value, the\n   997:         // compiler statically verifies that it is not currently borrowed.\n   998:         self.value.into_inner()\n   999:     }\n  1000: \n  1001:     /// Replaces the wrapped value with a new one, returning the old value,\n  1002:     /// without deinitializing either one.\n  1003:     ///\n  1004:     /// This function corresponds to [`std::mem::replace`](../mem/fn.replace.html).\n  1005:     ///\n  1006:     /// # Panics\n  1007:     ///\n  1008:     /// Panics if the value is currently borrowed.\n  1009:     ///\n  1010:     /// # Examples\n  1011:     ///",
    "nanvix_source": "   985:     /// use std::cell::RefCell;\n   986:     ///\n   987:     /// let c = RefCell::new(5);\n   988:     ///\n   989:     /// let five = c.into_inner();\n   990:     /// ```\n   991:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   992:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n   993:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   994:     #[inline]\n   995:     pub const fn into_inner(self) -> T {\n   996:         // Since this function takes `self` (the `RefCell`) by value, the\n   997:         // compiler statically verifies that it is not currently borrowed.\n   998:         self.value.into_inner()\n   999:     }\n  1000: \n  1001:     /// Replaces the wrapped value with a new one, returning the old value,\n  1002:     /// without deinitializing either one.\n  1003:     ///\n  1004:     /// This function corresponds to [`std::mem::replace`](../mem/fn.replace.html).\n  1005:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::new",
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
            "id": 9393,
            "path": "RefCell"
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
        "impl_id": "core:24784",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9393,
            "path": "RefCell"
          }
        }
      }
    },
    "verification_source": "   955:     x > UNUSED\n   956: }\n   957: \n   958: impl<T> RefCell<T> {\n   959:     /// Creates a new `RefCell` containing `value`.\n   960:     ///\n   961:     /// # Examples\n   962:     ///\n   963:     /// ```\n   964:     /// use std::cell::RefCell;\n   965:     ///\n   966:     /// let c = RefCell::new(5);\n   967:     /// ```\n   968:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   969:     #[rustc_const_stable(feature = \"const_refcell_new\", since = \"1.24.0\")]\n   970:     #[inline]\n   971:     pub const fn new(value: T) -> RefCell<T> {\n   972:         RefCell {\n   973:             value: UnsafeCell::new(value),\n   974:             borrow: Cell::new(UNUSED),\n   975:             #[cfg(feature = \"debug_refcell\")]\n   976:             borrowed_at: Cell::new(None),\n   977:         }\n   978:     }\n   979: \n   980:     /// Consumes the `RefCell`, returning the wrapped value.\n   981:     ///\n   982:     /// # Examples\n   983:     ///\n   984:     /// ```\n   985:     /// use std::cell::RefCell;\n   986:     ///\n   987:     /// let c = RefCell::new(5);",
    "nanvix_source": "   961:     /// # Examples\n   962:     ///\n   963:     /// ```\n   964:     /// use std::cell::RefCell;\n   965:     ///\n   966:     /// let c = RefCell::new(5);\n   967:     /// ```\n   968:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   969:     #[rustc_const_stable(feature = \"const_refcell_new\", since = \"1.24.0\")]\n   970:     #[inline]\n   971:     pub const fn new(value: T) -> RefCell<T> {\n   972:         RefCell {\n   973:             value: UnsafeCell::new(value),\n   974:             borrow: Cell::new(UNUSED),\n   975:             #[cfg(feature = \"debug_refcell\")]\n   976:             borrowed_at: Cell::new(None),\n   977:         }\n   978:     }\n   979: \n   980:     /// Consumes the `RefCell`, returning the wrapped value.\n   981:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::replace",
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
      "name": "replace",
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
            "id": 9393,
            "path": "RefCell"
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
        "impl_id": "core:24784",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
            "t",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1009:     ///\n  1010:     /// # Examples\n  1011:     ///\n  1012:     /// ```\n  1013:     /// use std::cell::RefCell;\n  1014:     /// let cell = RefCell::new(5);\n  1015:     /// let old_value = cell.replace(6);\n  1016:     /// assert_eq!(old_value, 5);\n  1017:     /// assert_eq!(cell, RefCell::new(6));\n  1018:     /// ```\n  1019:     #[inline]\n  1020:     #[stable(feature = \"refcell_replace\", since = \"1.24.0\")]\n  1021:     #[track_caller]\n  1022:     #[rustc_confusables(\"swap\")]\n  1023:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1024:     #[rustc_should_not_be_called_on_const_items]\n  1025:     pub const fn replace(&self, t: T) -> T {\n  1026:         mem::replace(&mut self.borrow_mut(), t)\n  1027:     }\n  1028: \n  1029:     /// Replaces the wrapped value with a new one computed from `f`, returning\n  1030:     /// the old value, without deinitializing either one.\n  1031:     ///\n  1032:     /// # Panics\n  1033:     ///\n  1034:     /// Panics if the value is currently borrowed.\n  1035:     ///\n  1036:     /// # Examples\n  1037:     ///\n  1038:     /// ```\n  1039:     /// use std::cell::RefCell;\n  1040:     /// let cell = RefCell::new(5);\n  1041:     /// let old_value = cell.replace_with(|&mut old| old + 1);",
    "nanvix_source": "  1015:     /// let old_value = cell.replace(6);\n  1016:     /// assert_eq!(old_value, 5);\n  1017:     /// assert_eq!(cell, RefCell::new(6));\n  1018:     /// ```\n  1019:     #[inline]\n  1020:     #[stable(feature = \"refcell_replace\", since = \"1.24.0\")]\n  1021:     #[track_caller]\n  1022:     #[rustc_confusables(\"swap\")]\n  1023:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1024:     #[rustc_should_not_be_called_on_const_items]\n  1025:     pub const fn replace(&self, t: T) -> T {\n  1026:         mem::replace(&mut self.borrow_mut(), t)\n  1027:     }\n  1028: \n  1029:     /// Replaces the wrapped value with a new one computed from `f`, returning\n  1030:     /// the old value, without deinitializing either one.\n  1031:     ///\n  1032:     /// # Panics\n  1033:     ///\n  1034:     /// Panics if the value is currently borrowed.\n  1035:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::take",
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
            "id": 9393,
            "path": "RefCell"
          }
        },
        "generics": {
          "params": [
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
                          "id": 70,
                          "path": "Default"
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
        "impl_id": "core:24794",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  1414:     /// # Panics\n  1415:     ///\n  1416:     /// Panics if the value is currently borrowed.\n  1417:     ///\n  1418:     /// # Examples\n  1419:     ///\n  1420:     /// ```\n  1421:     /// use std::cell::RefCell;\n  1422:     ///\n  1423:     /// let c = RefCell::new(5);\n  1424:     /// let five = c.take();\n  1425:     ///\n  1426:     /// assert_eq!(five, 5);\n  1427:     /// assert_eq!(c.into_inner(), 0);\n  1428:     /// ```\n  1429:     #[stable(feature = \"refcell_take\", since = \"1.50.0\")]\n  1430:     pub fn take(&self) -> T {\n  1431:         self.replace(Default::default())\n  1432:     }\n  1433: }\n  1434: \n  1435: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1436: unsafe impl<T: ?Sized> Send for RefCell<T> where T: Send {}\n  1437: \n  1438: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1439: impl<T: ?Sized> !Sync for RefCell<T> {}\n  1440: \n  1441: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1442: impl<T: Clone> Clone for RefCell<T> {\n  1443:     /// # Panics\n  1444:     ///\n  1445:     /// Panics if the value is currently mutably borrowed.\n  1446:     #[inline]",
    "nanvix_source": "  1420:     /// ```\n  1421:     /// use std::cell::RefCell;\n  1422:     ///\n  1423:     /// let c = RefCell::new(5);\n  1424:     /// let five = c.take();\n  1425:     ///\n  1426:     /// assert_eq!(five, 5);\n  1427:     /// assert_eq!(c.into_inner(), 0);\n  1428:     /// ```\n  1429:     #[stable(feature = \"refcell_take\", since = \"1.50.0\")]\n  1430:     pub fn take(&self) -> T {\n  1431:         self.replace(Default::default())\n  1432:     }\n  1433: }\n  1434: \n  1435: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1436: unsafe impl<T: ?Sized> Send for RefCell<T> where T: Send {}\n  1437: \n  1438: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1439: impl<T: ?Sized> !Sync for RefCell<T> {}\n  1440: ",
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
