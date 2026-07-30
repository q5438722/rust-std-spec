For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::DebugMap::entries",
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
            "name": "K"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "V"
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
                "generic": "K"
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
                      "args": null,
                      "id": 921,
                      "path": "fmt::Debug"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "V"
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
                                    "tuple": [
                                      {
                                        "generic": "K"
                                      },
                                      {
                                        "generic": "V"
                                      }
                                    ]
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
    "verification_source": "  1089:     /// impl fmt::Debug for Foo {\n  1090:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1091:     ///         fmt.debug_map()\n  1092:     ///            // We map our vec so each entries' first field will become\n  1093:     ///            // the \"key\".\n  1094:     ///            .entries(self.0.iter().map(|&(ref k, ref v)| (k, v)))\n  1095:     ///            .finish()\n  1096:     ///     }\n  1097:     /// }\n  1098:     ///\n  1099:     /// assert_eq!(\n  1100:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1101:     ///     r#\"{\"A\": 10, \"B\": 11}\"#,\n  1102:     /// );\n  1103:     /// ```\n  1104:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  1105:     pub fn entries<K, V, I>(&mut self, entries: I) -> &mut Self\n  1106:     where\n  1107:         K: fmt::Debug,\n  1108:         V: fmt::Debug,\n  1109:         I: IntoIterator<Item = (K, V)>,\n  1110:     {\n  1111:         for (k, v) in entries {\n  1112:             self.entry(&k, &v);\n  1113:         }\n  1114:         self\n  1115:     }\n  1116: \n  1117:     /// Marks the map as non-exhaustive, indicating to the reader that there are some other\n  1118:     /// entries that are not shown in the debug representation.\n  1119:     ///\n  1120:     /// # Examples\n  1121:     ///",
    "nanvix_source": "  1095:     ///            .finish()\n  1096:     ///     }\n  1097:     /// }\n  1098:     ///\n  1099:     /// assert_eq!(\n  1100:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1101:     ///     r#\"{\"A\": 10, \"B\": 11}\"#,\n  1102:     /// );\n  1103:     /// ```\n  1104:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  1105:     pub fn entries<K, V, I>(&mut self, entries: I) -> &mut Self\n  1106:     where\n  1107:         K: fmt::Debug,\n  1108:         V: fmt::Debug,\n  1109:         I: IntoIterator<Item = (K, V)>,\n  1110:     {\n  1111:         for (k, v) in entries {\n  1112:             self.entry(&k, &v);\n  1113:         }\n  1114:         self\n  1115:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugMap::entry",
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
            "key",
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
          ],
          [
            "value",
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
    "verification_source": "   919:     /// struct Foo(Vec<(String, i32)>);\n   920:     ///\n   921:     /// impl fmt::Debug for Foo {\n   922:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   923:     ///         fmt.debug_map()\n   924:     ///            .entry(&\"whole\", &self.0) // We add the \"whole\" entry.\n   925:     ///            .finish()\n   926:     ///     }\n   927:     /// }\n   928:     ///\n   929:     /// assert_eq!(\n   930:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n   931:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n   932:     /// );\n   933:     /// ```\n   934:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   935:     pub fn entry(&mut self, key: &dyn fmt::Debug, value: &dyn fmt::Debug) -> &mut Self {\n   936:         self.key(key).value(value)\n   937:     }\n   938: \n   939:     /// Adds the key part of a new entry to the map output.\n   940:     ///\n   941:     /// This method, together with `value`, is an alternative to `entry` that\n   942:     /// can be used when the complete entry isn't known upfront. Prefer the `entry`\n   943:     /// method when it's possible to use.\n   944:     ///\n   945:     /// # Panics\n   946:     ///\n   947:     /// `key` must be called before `value` and each call to `key` must be followed\n   948:     /// by a corresponding call to `value`. Otherwise this method will panic.\n   949:     ///\n   950:     /// # Examples\n   951:     ///",
    "nanvix_source": "   925:     ///            .finish()\n   926:     ///     }\n   927:     /// }\n   928:     ///\n   929:     /// assert_eq!(\n   930:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n   931:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n   932:     /// );\n   933:     /// ```\n   934:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   935:     pub fn entry(&mut self, key: &dyn fmt::Debug, value: &dyn fmt::Debug) -> &mut Self {\n   936:         self.key(key).value(value)\n   937:     }\n   938: \n   939:     /// Adds the key part of a new entry to the map output.\n   940:     ///\n   941:     /// This method, together with `value`, is an alternative to `entry` that\n   942:     /// can be used when the complete entry isn't known upfront. Prefer the `entry`\n   943:     /// method when it's possible to use.\n   944:     ///\n   945:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugMap::finish",
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
    "verification_source": "  1183:     /// struct Foo(Vec<(String, i32)>);\n  1184:     ///\n  1185:     /// impl fmt::Debug for Foo {\n  1186:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1187:     ///         fmt.debug_map()\n  1188:     ///            .entries(self.0.iter().map(|&(ref k, ref v)| (k, v)))\n  1189:     ///            .finish() // Ends the map formatting.\n  1190:     ///     }\n  1191:     /// }\n  1192:     ///\n  1193:     /// assert_eq!(\n  1194:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1195:     ///     r#\"{\"A\": 10, \"B\": 11}\"#,\n  1196:     /// );\n  1197:     /// ```\n  1198:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  1199:     pub fn finish(&mut self) -> fmt::Result {\n  1200:         self.result = self.result.and_then(|_| {\n  1201:             assert!(!self.has_key, \"attempted to finish a map with a partial entry\");\n  1202: \n  1203:             self.fmt.write_str(\"}\")\n  1204:         });\n  1205:         self.result\n  1206:     }\n  1207: \n  1208:     fn is_pretty(&self) -> bool {\n  1209:         self.fmt.alternate()\n  1210:     }\n  1211: }\n  1212: \n  1213: /// Creates a type whose [`fmt::Debug`] and [`fmt::Display`] impls are\n  1214: /// forwarded to the provided closure.\n  1215: ///",
    "nanvix_source": "  1189:     ///            .finish() // Ends the map formatting.\n  1190:     ///     }\n  1191:     /// }\n  1192:     ///\n  1193:     /// assert_eq!(\n  1194:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1195:     ///     r#\"{\"A\": 10, \"B\": 11}\"#,\n  1196:     /// );\n  1197:     /// ```\n  1198:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n  1199:     pub fn finish(&mut self) -> fmt::Result {\n  1200:         self.result = self.result.and_then(|_| {\n  1201:             assert!(!self.has_key, \"attempted to finish a map with a partial entry\");\n  1202: \n  1203:             self.fmt.write_str(\"}\")\n  1204:         });\n  1205:         self.result\n  1206:     }\n  1207: \n  1208:     fn is_pretty(&self) -> bool {\n  1209:         self.fmt.alternate()",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugMap::finish_non_exhaustive",
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
    "verification_source": "  1134:     ///         } else {\n  1135:     ///             f.finish()\n  1136:     ///         }\n  1137:     ///     }\n  1138:     /// }\n  1139:     ///\n  1140:     /// assert_eq!(\n  1141:     ///     format!(\"{:?}\", Foo(vec![\n  1142:     ///         (\"A\".to_string(), 10),\n  1143:     ///         (\"B\".to_string(), 11),\n  1144:     ///         (\"C\".to_string(), 12),\n  1145:     ///     ])),\n  1146:     ///     r#\"{\"A\": 10, \"B\": 11, ..}\"#,\n  1147:     /// );\n  1148:     /// ```\n  1149:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n  1150:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n  1151:         self.result = self.result.and_then(|_| {\n  1152:             assert!(!self.has_key, \"attempted to finish a map with a partial entry\");\n  1153: \n  1154:             if self.has_fields {\n  1155:                 if self.is_pretty() {\n  1156:                     let mut slot = None;\n  1157:                     let mut state = Default::default();\n  1158:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n  1159:                     writer.write_str(\"..\\n\")?;\n  1160:                     self.fmt.write_str(\"}\")\n  1161:                 } else {\n  1162:                     self.fmt.write_str(\", ..}\")\n  1163:                 }\n  1164:             } else {\n  1165:                 self.fmt.write_str(\"..}\")\n  1166:             }",
    "nanvix_source": "  1140:     /// assert_eq!(\n  1141:     ///     format!(\"{:?}\", Foo(vec![\n  1142:     ///         (\"A\".to_string(), 10),\n  1143:     ///         (\"B\".to_string(), 11),\n  1144:     ///         (\"C\".to_string(), 12),\n  1145:     ///     ])),\n  1146:     ///     r#\"{\"A\": 10, \"B\": 11, ..}\"#,\n  1147:     /// );\n  1148:     /// ```\n  1149:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n  1150:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n  1151:         self.result = self.result.and_then(|_| {\n  1152:             assert!(!self.has_key, \"attempted to finish a map with a partial entry\");\n  1153: \n  1154:             if self.has_fields {\n  1155:                 if self.is_pretty() {\n  1156:                     let mut slot = None;\n  1157:                     let mut state = Default::default();\n  1158:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n  1159:                     writer.write_str(\"..\\n\")?;\n  1160:                     self.fmt.write_str(\"}\")",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugMap::key",
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
      "name": "key",
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
            "key",
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
    "verification_source": "   955:     /// struct Foo(Vec<(String, i32)>);\n   956:     ///\n   957:     /// impl fmt::Debug for Foo {\n   958:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   959:     ///         fmt.debug_map()\n   960:     ///            .key(&\"whole\").value(&self.0) // We add the \"whole\" entry.\n   961:     ///            .finish()\n   962:     ///     }\n   963:     /// }\n   964:     ///\n   965:     /// assert_eq!(\n   966:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n   967:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n   968:     /// );\n   969:     /// ```\n   970:     #[stable(feature = \"debug_map_key_value\", since = \"1.42.0\")]\n   971:     pub fn key(&mut self, key: &dyn fmt::Debug) -> &mut Self {\n   972:         self.key_with(|f| key.fmt(f))\n   973:     }\n   974: \n   975:     /// Adds the key part of a new entry to the map output.\n   976:     ///\n   977:     /// This method is equivalent to [`DebugMap::key`], but formats the\n   978:     /// key using a provided closure rather than by calling [`Debug::fmt`].\n   979:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   980:     pub fn key_with<F>(&mut self, key_fmt: F) -> &mut Self\n   981:     where\n   982:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n   983:     {\n   984:         self.result = self.result.and_then(|_| {\n   985:             assert!(\n   986:                 !self.has_key,\n   987:                 \"attempted to begin a new map entry \\",
    "nanvix_source": "   961:     ///            .finish()\n   962:     ///     }\n   963:     /// }\n   964:     ///\n   965:     /// assert_eq!(\n   966:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n   967:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n   968:     /// );\n   969:     /// ```\n   970:     #[stable(feature = \"debug_map_key_value\", since = \"1.42.0\")]\n   971:     pub fn key(&mut self, key: &dyn fmt::Debug) -> &mut Self {\n   972:         self.key_with(|f| key.fmt(f))\n   973:     }\n   974: \n   975:     /// Adds the key part of a new entry to the map output.\n   976:     ///\n   977:     /// This method is equivalent to [`DebugMap::key`], but formats the\n   978:     /// key using a provided closure rather than by calling [`Debug::fmt`].\n   979:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   980:     pub fn key_with<F>(&mut self, key_fmt: F) -> &mut Self\n   981:     where",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugMap::value",
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
      "name": "value",
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
            "id": 13425,
            "path": "DebugMap"
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
        "impl_id": "core:29851",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13425",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugMap"
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
            "value",
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
    "verification_source": "  1031:     /// struct Foo(Vec<(String, i32)>);\n  1032:     ///\n  1033:     /// impl fmt::Debug for Foo {\n  1034:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1035:     ///         fmt.debug_map()\n  1036:     ///            .key(&\"whole\").value(&self.0) // We add the \"whole\" entry.\n  1037:     ///            .finish()\n  1038:     ///     }\n  1039:     /// }\n  1040:     ///\n  1041:     /// assert_eq!(\n  1042:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1043:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n  1044:     /// );\n  1045:     /// ```\n  1046:     #[stable(feature = \"debug_map_key_value\", since = \"1.42.0\")]\n  1047:     pub fn value(&mut self, value: &dyn fmt::Debug) -> &mut Self {\n  1048:         self.value_with(|f| value.fmt(f))\n  1049:     }\n  1050: \n  1051:     /// Adds the value part of a new entry to the map output.\n  1052:     ///\n  1053:     /// This method is equivalent to [`DebugMap::value`], but formats the\n  1054:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n  1055:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n  1056:     pub fn value_with<F>(&mut self, value_fmt: F) -> &mut Self\n  1057:     where\n  1058:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n  1059:     {\n  1060:         self.result = self.result.and_then(|_| {\n  1061:             assert!(self.has_key, \"attempted to format a map value before its key\");\n  1062: \n  1063:             if self.is_pretty() {",
    "nanvix_source": "  1037:     ///            .finish()\n  1038:     ///     }\n  1039:     /// }\n  1040:     ///\n  1041:     /// assert_eq!(\n  1042:     ///     format!(\"{:?}\", Foo(vec![(\"A\".to_string(), 10), (\"B\".to_string(), 11)])),\n  1043:     ///     r#\"{\"whole\": [(\"A\", 10), (\"B\", 11)]}\"#,\n  1044:     /// );\n  1045:     /// ```\n  1046:     #[stable(feature = \"debug_map_key_value\", since = \"1.42.0\")]\n  1047:     pub fn value(&mut self, value: &dyn fmt::Debug) -> &mut Self {\n  1048:         self.value_with(|f| value.fmt(f))\n  1049:     }\n  1050: \n  1051:     /// Adds the value part of a new entry to the map output.\n  1052:     ///\n  1053:     /// This method is equivalent to [`DebugMap::value`], but formats the\n  1054:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n  1055:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n  1056:     pub fn value_with<F>(&mut self, value_fmt: F) -> &mut Self\n  1057:     where",
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
