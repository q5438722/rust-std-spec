For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::DebugStruct::finish_non_exhaustive",
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
            "id": 13417,
            "path": "DebugStruct"
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
        "impl_id": "core:29782",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13417",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugStruct"
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
    "verification_source": "   181:     /// }\n   182:     ///\n   183:     /// impl fmt::Debug for Bar {\n   184:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   185:     ///         fmt.debug_struct(\"Bar\")\n   186:     ///            .field(\"bar\", &self.bar)\n   187:     ///            .finish_non_exhaustive() // Show that some other field(s) exist.\n   188:     ///     }\n   189:     /// }\n   190:     ///\n   191:     /// assert_eq!(\n   192:     ///     format!(\"{:?}\", Bar { bar: 10, hidden: 1.0 }),\n   193:     ///     \"Bar { bar: 10, .. }\",\n   194:     /// );\n   195:     /// ```\n   196:     #[stable(feature = \"debug_non_exhaustive\", since = \"1.53.0\")]\n   197:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   198:         self.result = self.result.and_then(|_| {\n   199:             if self.has_fields {\n   200:                 if self.is_pretty() {\n   201:                     let mut slot = None;\n   202:                     let mut state = Default::default();\n   203:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n   204:                     writer.write_str(\"..\\n\")?;\n   205:                     self.fmt.write_str(\"}\")\n   206:                 } else {\n   207:                     self.fmt.write_str(\", .. }\")\n   208:                 }\n   209:             } else {\n   210:                 self.fmt.write_str(\" { .. }\")\n   211:             }\n   212:         });\n   213:         self.result",
    "nanvix_source": "   187:     ///            .finish_non_exhaustive() // Show that some other field(s) exist.\n   188:     ///     }\n   189:     /// }\n   190:     ///\n   191:     /// assert_eq!(\n   192:     ///     format!(\"{:?}\", Bar { bar: 10, hidden: 1.0 }),\n   193:     ///     \"Bar { bar: 10, .. }\",\n   194:     /// );\n   195:     /// ```\n   196:     #[stable(feature = \"debug_non_exhaustive\", since = \"1.53.0\")]\n   197:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   198:         self.result = self.result.and_then(|_| {\n   199:             if self.has_fields {\n   200:                 if self.is_pretty() {\n   201:                     let mut slot = None;\n   202:                     let mut state = Default::default();\n   203:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n   204:                     writer.write_str(\"..\\n\")?;\n   205:                     self.fmt.write_str(\"}\")\n   206:                 } else {\n   207:                     self.fmt.write_str(\", .. }\")",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugTuple::field",
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
      "name": "field",
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
            "id": 13419,
            "path": "DebugTuple"
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
        "impl_id": "core:29799",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13419",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugTuple"
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
    "verification_source": "   313:     ///\n   314:     /// impl fmt::Debug for Foo {\n   315:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   316:     ///         fmt.debug_tuple(\"Foo\")\n   317:     ///            .field(&self.0) // We add the first field.\n   318:     ///            .field(&self.1) // We add the second field.\n   319:     ///            .finish() // We're good to go!\n   320:     ///     }\n   321:     /// }\n   322:     ///\n   323:     /// assert_eq!(\n   324:     ///     format!(\"{:?}\", Foo(10, \"Hello World\".to_string())),\n   325:     ///     r#\"Foo(10, \"Hello World\")\"#,\n   326:     /// );\n   327:     /// ```\n   328:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   329:     pub fn field(&mut self, value: &dyn fmt::Debug) -> &mut Self {\n   330:         self.field_with(|f| value.fmt(f))\n   331:     }\n   332: \n   333:     /// Adds a new field to the generated tuple struct output.\n   334:     ///\n   335:     /// This method is equivalent to [`DebugTuple::field`], but formats the\n   336:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n   337:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   338:     pub fn field_with<F>(&mut self, value_fmt: F) -> &mut Self\n   339:     where\n   340:         F: FnOnce(&mut fmt::Formatter<'_>) -> fmt::Result,\n   341:     {\n   342:         self.result = self.result.and_then(|_| {\n   343:             if self.is_pretty() {\n   344:                 if self.fields == 0 {\n   345:                     self.fmt.write_str(\"(\\n\")?;",
    "nanvix_source": "   319:     ///            .finish() // We're good to go!\n   320:     ///     }\n   321:     /// }\n   322:     ///\n   323:     /// assert_eq!(\n   324:     ///     format!(\"{:?}\", Foo(10, \"Hello World\".to_string())),\n   325:     ///     r#\"Foo(10, \"Hello World\")\"#,\n   326:     /// );\n   327:     /// ```\n   328:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   329:     pub fn field(&mut self, value: &dyn fmt::Debug) -> &mut Self {\n   330:         self.field_with(|f| value.fmt(f))\n   331:     }\n   332: \n   333:     /// Adds a new field to the generated tuple struct output.\n   334:     ///\n   335:     /// This method is equivalent to [`DebugTuple::field`], but formats the\n   336:     /// value using a provided closure rather than by calling [`Debug::fmt`].\n   337:     #[unstable(feature = \"debug_closure_helpers\", issue = \"117729\")]\n   338:     pub fn field_with<F>(&mut self, value_fmt: F) -> &mut Self\n   339:     where",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugTuple::finish",
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
            "id": 13419,
            "path": "DebugTuple"
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
        "impl_id": "core:29799",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13419",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugTuple"
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
    "verification_source": "   415:     /// impl fmt::Debug for Foo {\n   416:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   417:     ///         fmt.debug_tuple(\"Foo\")\n   418:     ///            .field(&self.0)\n   419:     ///            .field(&self.1)\n   420:     ///            .finish() // You need to call it to \"finish\" the\n   421:     ///                      // tuple formatting.\n   422:     ///     }\n   423:     /// }\n   424:     ///\n   425:     /// assert_eq!(\n   426:     ///     format!(\"{:?}\", Foo(10, \"Hello World\".to_string())),\n   427:     ///     r#\"Foo(10, \"Hello World\")\"#,\n   428:     /// );\n   429:     /// ```\n   430:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   431:     pub fn finish(&mut self) -> fmt::Result {\n   432:         if self.fields > 0 {\n   433:             self.result = self.result.and_then(|_| {\n   434:                 if self.fields == 1 && self.empty_name && !self.is_pretty() {\n   435:                     self.fmt.write_str(\",\")?;\n   436:                 }\n   437:                 self.fmt.write_str(\")\")\n   438:             });\n   439:         }\n   440:         self.result\n   441:     }\n   442: \n   443:     fn is_pretty(&self) -> bool {\n   444:         self.fmt.alternate()\n   445:     }\n   446: }\n   447: ",
    "nanvix_source": "   421:     ///                      // tuple formatting.\n   422:     ///     }\n   423:     /// }\n   424:     ///\n   425:     /// assert_eq!(\n   426:     ///     format!(\"{:?}\", Foo(10, \"Hello World\".to_string())),\n   427:     ///     r#\"Foo(10, \"Hello World\")\"#,\n   428:     /// );\n   429:     /// ```\n   430:     #[stable(feature = \"debug_builders\", since = \"1.2.0\")]\n   431:     pub fn finish(&mut self) -> fmt::Result {\n   432:         if self.fields > 0 {\n   433:             self.result = self.result.and_then(|_| {\n   434:                 if self.fields == 1 && self.empty_name && !self.is_pretty() {\n   435:                     self.fmt.write_str(\",\")?;\n   436:                 }\n   437:                 self.fmt.write_str(\")\")\n   438:             });\n   439:         }\n   440:         self.result\n   441:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::DebugTuple::finish_non_exhaustive",
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
            "id": 13419,
            "path": "DebugTuple"
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
        "impl_id": "core:29799",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13419",
        "resolved_owner_path": [
          "core",
          "fmt",
          "builders",
          "DebugTuple"
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
    "verification_source": "   371:     /// struct Foo(i32, String);\n   372:     ///\n   373:     /// impl fmt::Debug for Foo {\n   374:     ///     fn fmt(&self, fmt: &mut fmt::Formatter<'_>) -> fmt::Result {\n   375:     ///         fmt.debug_tuple(\"Foo\")\n   376:     ///            .field(&self.0)\n   377:     ///            .finish_non_exhaustive() // Show that some other field(s) exist.\n   378:     ///     }\n   379:     /// }\n   380:     ///\n   381:     /// assert_eq!(\n   382:     ///     format!(\"{:?}\", Foo(10, \"secret!\".to_owned())),\n   383:     ///     \"Foo(10, ..)\",\n   384:     /// );\n   385:     /// ```\n   386:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   387:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   388:         self.result = self.result.and_then(|_| {\n   389:             if self.fields > 0 {\n   390:                 if self.is_pretty() {\n   391:                     let mut slot = None;\n   392:                     let mut state = Default::default();\n   393:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n   394:                     writer.write_str(\"..\\n\")?;\n   395:                     self.fmt.write_str(\")\")\n   396:                 } else {\n   397:                     self.fmt.write_str(\", ..)\")\n   398:                 }\n   399:             } else {\n   400:                 self.fmt.write_str(\"(..)\")\n   401:             }\n   402:         });\n   403:         self.result",
    "nanvix_source": "   377:     ///            .finish_non_exhaustive() // Show that some other field(s) exist.\n   378:     ///     }\n   379:     /// }\n   380:     ///\n   381:     /// assert_eq!(\n   382:     ///     format!(\"{:?}\", Foo(10, \"secret!\".to_owned())),\n   383:     ///     \"Foo(10, ..)\",\n   384:     /// );\n   385:     /// ```\n   386:     #[stable(feature = \"debug_more_non_exhaustive\", since = \"1.83.0\")]\n   387:     pub fn finish_non_exhaustive(&mut self) -> fmt::Result {\n   388:         self.result = self.result.and_then(|_| {\n   389:             if self.fields > 0 {\n   390:                 if self.is_pretty() {\n   391:                     let mut slot = None;\n   392:                     let mut state = Default::default();\n   393:                     let mut writer = PadAdapter::wrap(self.fmt, &mut slot, &mut state);\n   394:                     writer.write_str(\"..\\n\")?;\n   395:                     self.fmt.write_str(\")\")\n   396:                 } else {\n   397:                     self.fmt.write_str(\", ..)\")",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::align",
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
      "name": "align",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
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
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
                      "resolved_path": {
                        "args": null,
                        "id": 10020,
                        "path": "Alignment"
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
    "verification_source": "  2198:     ///                 Alignment::Center  => \"center\",\n  2199:     ///             }\n  2200:     ///         } else {\n  2201:     ///             \"into the void\"\n  2202:     ///         };\n  2203:     ///         write!(formatter, \"{s}\")\n  2204:     ///     }\n  2205:     /// }\n  2206:     ///\n  2207:     /// assert_eq!(format!(\"{Foo:<}\"), \"left\");\n  2208:     /// assert_eq!(format!(\"{Foo:>}\"), \"right\");\n  2209:     /// assert_eq!(format!(\"{Foo:^}\"), \"center\");\n  2210:     /// assert_eq!(format!(\"{Foo}\"), \"into the void\");\n  2211:     /// ```\n  2212:     #[must_use]\n  2213:     #[stable(feature = \"fmt_flags_align\", since = \"1.28.0\")]\n  2214:     pub fn align(&self) -> Option<Alignment> {\n  2215:         self.options.get_align()\n  2216:     }\n  2217: \n  2218:     /// Returns the optionally specified integer width that the output should be.\n  2219:     ///\n  2220:     /// # Examples\n  2221:     ///\n  2222:     /// ```\n  2223:     /// use std::fmt;\n  2224:     ///\n  2225:     /// struct Foo(i32);\n  2226:     ///\n  2227:     /// impl fmt::Display for Foo {\n  2228:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2229:     ///         if let Some(width) = formatter.width() {\n  2230:     ///             // If we received a width, we use it",
    "nanvix_source": "  2204:     ///     }\n  2205:     /// }\n  2206:     ///\n  2207:     /// assert_eq!(format!(\"{Foo:<}\"), \"left\");\n  2208:     /// assert_eq!(format!(\"{Foo:>}\"), \"right\");\n  2209:     /// assert_eq!(format!(\"{Foo:^}\"), \"center\");\n  2210:     /// assert_eq!(format!(\"{Foo}\"), \"into the void\");\n  2211:     /// ```\n  2212:     #[must_use]\n  2213:     #[stable(feature = \"fmt_flags_align\", since = \"1.28.0\")]\n  2214:     pub fn align(&self) -> Option<Alignment> {\n  2215:         self.options.get_align()\n  2216:     }\n  2217: \n  2218:     /// Returns the optionally specified integer width that the output should be.\n  2219:     ///\n  2220:     /// # Examples\n  2221:     ///\n  2222:     /// ```\n  2223:     /// use std::fmt;\n  2224:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Formatter::alternate",
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
      "name": "alternate",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 918,
            "path": "Formatter"
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
        "impl_id": "core:30045",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:918",
        "resolved_owner_path": [
          "core",
          "fmt",
          "Formatter"
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
    "verification_source": "  2356:     ///\n  2357:     /// impl fmt::Display for Foo {\n  2358:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2359:     ///         if formatter.alternate() {\n  2360:     ///             write!(formatter, \"Foo({})\", self.0)\n  2361:     ///         } else {\n  2362:     ///             write!(formatter, \"{}\", self.0)\n  2363:     ///         }\n  2364:     ///     }\n  2365:     /// }\n  2366:     ///\n  2367:     /// assert_eq!(format!(\"{:#}\", Foo(23)), \"Foo(23)\");\n  2368:     /// assert_eq!(format!(\"{}\", Foo(23)), \"23\");\n  2369:     /// ```\n  2370:     #[must_use]\n  2371:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2372:     pub fn alternate(&self) -> bool {\n  2373:         self.options.flags & flags::ALTERNATE_FLAG != 0\n  2374:     }\n  2375: \n  2376:     /// Determines if the `0` flag was specified.\n  2377:     ///\n  2378:     /// # Examples\n  2379:     ///\n  2380:     /// ```\n  2381:     /// use std::fmt;\n  2382:     ///\n  2383:     /// struct Foo(i32);\n  2384:     ///\n  2385:     /// impl fmt::Display for Foo {\n  2386:     ///     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2387:     ///         assert!(formatter.sign_aware_zero_pad());\n  2388:     ///         assert_eq!(formatter.width(), Some(4));",
    "nanvix_source": "  2362:     ///             write!(formatter, \"{}\", self.0)\n  2363:     ///         }\n  2364:     ///     }\n  2365:     /// }\n  2366:     ///\n  2367:     /// assert_eq!(format!(\"{:#}\", Foo(23)), \"Foo(23)\");\n  2368:     /// assert_eq!(format!(\"{}\", Foo(23)), \"23\");\n  2369:     /// ```\n  2370:     #[must_use]\n  2371:     #[stable(feature = \"fmt_flags\", since = \"1.5.0\")]\n  2372:     pub fn alternate(&self) -> bool {\n  2373:         self.options.flags & flags::ALTERNATE_FLAG != 0\n  2374:     }\n  2375: \n  2376:     /// Determines if the `0` flag was specified.\n  2377:     ///\n  2378:     /// # Examples\n  2379:     ///\n  2380:     /// ```\n  2381:     /// use std::fmt;\n  2382:     ///",
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
