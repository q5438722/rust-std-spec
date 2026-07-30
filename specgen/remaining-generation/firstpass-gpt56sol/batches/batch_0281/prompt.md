For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::error::Error::description",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "description",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:934",
        "kind": "trait",
        "name": "Error",
        "path": [
          "core",
          "error",
          "Error"
        ]
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
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   121:     )]\n   122:     fn type_id(&self, _: private::Internal) -> TypeId\n   123:     where\n   124:         Self: 'static,\n   125:     {\n   126:         TypeId::of::<Self>()\n   127:     }\n   128: \n   129:     /// ```\n   130:     /// if let Err(e) = \"xc\".parse::<u32>() {\n   131:     ///     // Print `e` itself, no need for description().\n   132:     ///     eprintln!(\"Error: {e}\");\n   133:     /// }\n   134:     /// ```\n   135:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   136:     #[deprecated(since = \"1.42.0\", note = \"use the Display impl or to_string()\")]\n   137:     fn description(&self) -> &str {\n   138:         \"description() is deprecated; use Display\"\n   139:     }\n   140: \n   141:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   142:     #[deprecated(\n   143:         since = \"1.33.0\",\n   144:         note = \"replaced by Error::source, which can support downcasting\"\n   145:     )]\n   146:     #[allow(missing_docs)]\n   147:     fn cause(&self) -> Option<&dyn Error> {\n   148:         self.source()\n   149:     }\n   150: \n   151:     /// Provides type-based access to context intended for error reports.\n   152:     ///\n   153:     /// Used in conjunction with [`Request::provide_value`] and [`Request::provide_ref`] to extract",
    "nanvix_source": "   127:     }\n   128: \n   129:     /// ```\n   130:     /// if let Err(e) = \"xc\".parse::<u32>() {\n   131:     ///     // Print `e` itself, no need for description().\n   132:     ///     eprintln!(\"Error: {e}\");\n   133:     /// }\n   134:     /// ```\n   135:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   136:     #[deprecated(since = \"1.42.0\", note = \"use the Display impl or to_string()\")]\n   137:     fn description(&self) -> &str {\n   138:         \"description() is deprecated; use Display\"\n   139:     }\n   140: \n   141:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   142:     #[deprecated(\n   143:         since = \"1.33.0\",\n   144:         note = \"replaced by Error::source, which can support downcasting\"\n   145:     )]\n   146:     #[allow(missing_docs)]\n   147:     fn cause(&self) -> Option<&dyn Error> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::error::Error::source",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "source",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:934",
        "kind": "trait",
        "name": "Error",
        "path": [
          "core",
          "error",
          "Error"
        ]
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
                          "dyn_trait": {
                            "lifetime": "'static",
                            "traits": [
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 934,
                                  "path": "Error"
                                }
                              }
                            ]
                          }
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
    "verification_source": "    95:     ///\n    96:     /// fn get_super_error() -> Result<(), SuperError> {\n    97:     ///     Err(SuperError { source: SuperErrorSideKick })\n    98:     /// }\n    99:     ///\n   100:     /// fn main() {\n   101:     ///     match get_super_error() {\n   102:     ///         Err(e) => {\n   103:     ///             println!(\"Error: {e}\");\n   104:     ///             println!(\"Caused by: {}\", e.source().unwrap());\n   105:     ///         }\n   106:     ///         _ => println!(\"No error\"),\n   107:     ///     }\n   108:     /// }\n   109:     /// ```\n   110:     #[stable(feature = \"error_source\", since = \"1.30.0\")]\n   111:     fn source(&self) -> Option<&(dyn Error + 'static)> {\n   112:         None\n   113:     }\n   114: \n   115:     /// Gets the `TypeId` of `self`.\n   116:     #[doc(hidden)]\n   117:     #[unstable(\n   118:         feature = \"error_type_id\",\n   119:         reason = \"this is memory-unsafe to override in user code\",\n   120:         issue = \"60784\"\n   121:     )]\n   122:     fn type_id(&self, _: private::Internal) -> TypeId\n   123:     where\n   124:         Self: 'static,\n   125:     {\n   126:         TypeId::of::<Self>()\n   127:     }",
    "nanvix_source": "   101:     ///     match get_super_error() {\n   102:     ///         Err(e) => {\n   103:     ///             println!(\"Error: {e}\");\n   104:     ///             println!(\"Caused by: {}\", e.source().unwrap());\n   105:     ///         }\n   106:     ///         _ => println!(\"No error\"),\n   107:     ///     }\n   108:     /// }\n   109:     /// ```\n   110:     #[stable(feature = \"error_source\", since = \"1.30.0\")]\n   111:     fn source(&self) -> Option<&(dyn Error + 'static)> {\n   112:         None\n   113:     }\n   114: \n   115:     /// Gets the `TypeId` of `self`.\n   116:     #[doc(hidden)]\n   117:     #[unstable(\n   118:         feature = \"error_type_id\",\n   119:         reason = \"this is memory-unsafe to override in user code\",\n   120:         issue = \"60784\"\n   121:     )]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Binary::fmt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "fmt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "f"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:1649",
        "kind": "trait",
        "name": "Binary",
        "path": [
          "core",
          "fmt",
          "Binary"
        ]
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
              "borrowed_ref": {
                "is_mutable": true,
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
                    "id": 918,
                    "path": "Formatter"
                  }
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1309: ///\n  1310: /// let l = Length(107);\n  1311: ///\n  1312: /// assert_eq!(format!(\"l as binary is: {l:b}\"), \"l as binary is: 1101011\");\n  1313: ///\n  1314: /// assert_eq!(\n  1315: ///     // Note that the `0b` prefix added by `#` is included in the total width, so we\n  1316: ///     // need to add two to correctly display all 32 bits.\n  1317: ///     format!(\"l as binary is: {l:#034b}\"),\n  1318: ///     \"l as binary is: 0b00000000000000000000000001101011\"\n  1319: /// );\n  1320: /// ```\n  1321: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1322: pub trait Binary: PointeeSized {\n  1323:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1324:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1325:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1326: }\n  1327: \n  1328: /// `x` formatting.\n  1329: ///\n  1330: /// The `LowerHex` trait should format its output as a number in hexadecimal, with `a` through `f`\n  1331: /// in lower case.\n  1332: ///\n  1333: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1334: /// negative values are formatted as the two\u2019s complement representation.\n  1335: ///\n  1336: /// The alternate flag, `#`, adds a `0x` in front of the output.\n  1337: ///\n  1338: /// For more information on formatters, see [the module-level documentation][module].\n  1339: ///\n  1340: /// [module]: ../../std/fmt/index.html\n  1341: ///",
    "nanvix_source": "  1315: ///     // Note that the `0b` prefix added by `#` is included in the total width, so we\n  1316: ///     // need to add two to correctly display all 32 bits.\n  1317: ///     format!(\"l as binary is: {l:#034b}\"),\n  1318: ///     \"l as binary is: 0b00000000000000000000000001101011\"\n  1319: /// );\n  1320: /// ```\n  1321: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1322: pub trait Binary: PointeeSized {\n  1323:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1324:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1325:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1326: }\n  1327: \n  1328: /// `x` formatting.\n  1329: ///\n  1330: /// The `LowerHex` trait should format its output as a number in hexadecimal, with `a` through `f`\n  1331: /// in lower case.\n  1332: ///\n  1333: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1334: /// negative values are formatted as the two\u2019s complement representation.\n  1335: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Debug::fmt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "fmt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "f"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:921",
        "kind": "trait",
        "name": "Debug",
        "path": [
          "core",
          "fmt",
          "Debug"
        ]
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
              "borrowed_ref": {
                "is_mutable": true,
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
                    "id": 918,
                    "path": "Formatter"
                  }
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1068:     ///         f.debug_tuple(\"\")\n  1069:     ///          .field(&self.longitude)\n  1070:     ///          .field(&self.latitude)\n  1071:     ///          .finish()\n  1072:     ///     }\n  1073:     /// }\n  1074:     ///\n  1075:     /// let position = Position { longitude: 1.987, latitude: 2.983 };\n  1076:     /// assert_eq!(format!(\"{position:?}\"), \"(1.987, 2.983)\");\n  1077:     ///\n  1078:     /// assert_eq!(format!(\"{position:#?}\"), \"(\n  1079:     ///     1.987,\n  1080:     ///     2.983,\n  1081:     /// )\");\n  1082:     /// ```\n  1083:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1084:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1085: }\n  1086: \n  1087: // Separate module to reexport the macro `Debug` from prelude without the trait `Debug`.\n  1088: pub(crate) mod macros {\n  1089:     /// Derive macro generating an impl of the trait `Debug`.\n  1090:     #[rustc_builtin_macro]\n  1091:     #[stable(feature = \"builtin_macro_prelude\", since = \"1.38.0\")]\n  1092:     #[allow_internal_unstable(core_intrinsics, fmt_helpers_for_derive)]\n  1093:     pub macro Debug($item:item) {\n  1094:         /* compiler built-in */\n  1095:     }\n  1096: }\n  1097: #[stable(feature = \"builtin_macro_prelude\", since = \"1.38.0\")]\n  1098: #[doc(inline)]\n  1099: pub use macros::Debug;\n  1100: ",
    "nanvix_source": "  1074:     ///\n  1075:     /// let position = Position { longitude: 1.987, latitude: 2.983 };\n  1076:     /// assert_eq!(format!(\"{position:?}\"), \"(1.987, 2.983)\");\n  1077:     ///\n  1078:     /// assert_eq!(format!(\"{position:#?}\"), \"(\n  1079:     ///     1.987,\n  1080:     ///     2.983,\n  1081:     /// )\");\n  1082:     /// ```\n  1083:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1084:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1085: }\n  1086: \n  1087: // Separate module to reexport the macro `Debug` from prelude without the trait `Debug`.\n  1088: pub(crate) mod macros {\n  1089:     /// Derive macro generating an impl of the trait `Debug`.\n  1090:     #[rustc_builtin_macro]\n  1091:     #[stable(feature = \"builtin_macro_prelude\", since = \"1.38.0\")]\n  1092:     #[allow_internal_unstable(core_intrinsics, fmt_helpers_for_derive)]\n  1093:     pub macro Debug($item:item) {\n  1094:         /* compiler built-in */",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Display::fmt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "fmt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "f"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:932",
        "kind": "trait",
        "name": "Display",
        "path": [
          "core",
          "fmt",
          "Display"
        ]
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
              "borrowed_ref": {
                "is_mutable": true,
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
                    "id": 918,
                    "path": "Formatter"
                  }
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1196:     ///     longitude: f32,\n  1197:     ///     latitude: f32,\n  1198:     /// }\n  1199:     ///\n  1200:     /// impl fmt::Display for Position {\n  1201:     ///     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1202:     ///         write!(f, \"({}, {})\", self.longitude, self.latitude)\n  1203:     ///     }\n  1204:     /// }\n  1205:     ///\n  1206:     /// assert_eq!(\n  1207:     ///     \"(1.987, 2.983)\",\n  1208:     ///     format!(\"{}\", Position { longitude: 1.987, latitude: 2.983, }),\n  1209:     /// );\n  1210:     /// ```\n  1211:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1212:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1213: }\n  1214: \n  1215: /// `o` formatting.\n  1216: ///\n  1217: /// The `Octal` trait should format its output as a number in base-8.\n  1218: ///\n  1219: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1220: /// negative values are formatted as the two\u2019s complement representation.\n  1221: ///\n  1222: /// The alternate flag, `#`, adds a `0o` in front of the output.\n  1223: ///\n  1224: /// For more information on formatters, see [the module-level documentation][module].\n  1225: ///\n  1226: /// [module]: ../../std/fmt/index.html\n  1227: ///\n  1228: /// # Examples",
    "nanvix_source": "  1202:     ///         write!(f, \"({}, {})\", self.longitude, self.latitude)\n  1203:     ///     }\n  1204:     /// }\n  1205:     ///\n  1206:     /// assert_eq!(\n  1207:     ///     \"(1.987, 2.983)\",\n  1208:     ///     format!(\"{}\", Position { longitude: 1.987, latitude: 2.983, }),\n  1209:     /// );\n  1210:     /// ```\n  1211:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1212:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1213: }\n  1214: \n  1215: /// `o` formatting.\n  1216: ///\n  1217: /// The `Octal` trait should format its output as a number in base-8.\n  1218: ///\n  1219: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1220: /// negative values are formatted as the two\u2019s complement representation.\n  1221: ///\n  1222: /// The alternate flag, `#`, adds a `0o` in front of the output.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::LowerExp::fmt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "fmt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "f"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:1661",
        "kind": "trait",
        "name": "LowerExp",
        "path": [
          "core",
          "fmt",
          "LowerExp"
        ]
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
              "borrowed_ref": {
                "is_mutable": true,
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
                    "id": 918,
                    "path": "Formatter"
                  }
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1529: /// let l = Length(100);\n  1530: ///\n  1531: /// assert_eq!(\n  1532: ///     format!(\"l in scientific notation is: {l:e}\"),\n  1533: ///     \"l in scientific notation is: 1e2\"\n  1534: /// );\n  1535: ///\n  1536: /// assert_eq!(\n  1537: ///     format!(\"l in scientific notation is: {l:05e}\"),\n  1538: ///     \"l in scientific notation is: 001e2\"\n  1539: /// );\n  1540: /// ```\n  1541: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1542: pub trait LowerExp: PointeeSized {\n  1543:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1544:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1545:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1546: }\n  1547: \n  1548: /// `E` formatting.\n  1549: ///\n  1550: /// The `UpperExp` trait should format its output in scientific notation with an upper-case `E`.\n  1551: ///\n  1552: /// For more information on formatters, see [the module-level documentation][module].\n  1553: ///\n  1554: /// [module]: ../../std/fmt/index.html\n  1555: ///\n  1556: /// # Examples\n  1557: ///\n  1558: /// Basic usage with `f64`:\n  1559: ///\n  1560: /// ```\n  1561: /// let x = 42.0; // 42.0 is '4.2E1' in scientific notation",
    "nanvix_source": "  1535: ///\n  1536: /// assert_eq!(\n  1537: ///     format!(\"l in scientific notation is: {l:05e}\"),\n  1538: ///     \"l in scientific notation is: 001e2\"\n  1539: /// );\n  1540: /// ```\n  1541: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1542: pub trait LowerExp: PointeeSized {\n  1543:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1544:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1545:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1546: }\n  1547: \n  1548: /// `E` formatting.\n  1549: ///\n  1550: /// The `UpperExp` trait should format its output in scientific notation with an upper-case `E`.\n  1551: ///\n  1552: /// For more information on formatters, see [the module-level documentation][module].\n  1553: ///\n  1554: /// [module]: ../../std/fmt/index.html\n  1555: ///",
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
