For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::option::Option::map_or",
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
                            "generic": "U"
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
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "U"
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
      "name": "map_or",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "default",
            {
              "generic": "U"
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
          "generic": "U"
        }
      }
    },
    "verification_source": "  1208:     ///\n  1209:     /// [`map_or_else`]: Option::map_or_else\n  1210:     ///\n  1211:     /// # Examples\n  1212:     ///\n  1213:     /// ```\n  1214:     /// let x = Some(\"foo\");\n  1215:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n  1216:     ///\n  1217:     /// let x: Option<&str> = None;\n  1218:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n  1219:     /// ```\n  1220:     #[inline]\n  1221:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1222:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n  1223:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1224:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n  1225:     where\n  1226:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1227:         U: [const] Destruct,\n  1228:     {\n  1229:         match self {\n  1230:             Some(t) => f(t),\n  1231:             None => default,\n  1232:         }\n  1233:     }\n  1234: \n  1235:     /// Computes a default function result (if none), or\n  1236:     /// applies a different function to the contained value (if any).\n  1237:     ///\n  1238:     /// # Basic examples\n  1239:     ///\n  1240:     /// ```",
    "nanvix_source": "  1212:     /// let x = Some(\"foo\");\n  1213:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n  1214:     ///\n  1215:     /// let x: Option<&str> = None;\n  1216:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n  1217:     /// ```\n  1218:     #[inline]\n  1219:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1220:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n  1221:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1222:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n  1223:     where\n  1224:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1225:         U: [const] Destruct,\n  1226:     {\n  1227:         match self {\n  1228:             Some(t) => f(t),\n  1229:             None => default,\n  1230:         }\n  1231:     }\n  1232: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::map_or_default",
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
                      "args": null,
                      "id": 70,
                      "path": "Default"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
              }
            }
          },
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
      "name": "map_or_default",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
          "generic": "U"
        }
      }
    },
    "verification_source": "  1286:     /// # Examples\n  1287:     ///\n  1288:     /// ```\n  1289:     /// #![feature(result_option_map_or_default)]\n  1290:     ///\n  1291:     /// let x: Option<&str> = Some(\"hi\");\n  1292:     /// let y: Option<&str> = None;\n  1293:     ///\n  1294:     /// assert_eq!(x.map_or_default(|x| x.len()), 2);\n  1295:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n  1296:     /// ```\n  1297:     ///\n  1298:     /// [default value]: Default::default\n  1299:     #[inline]\n  1300:     #[unstable(feature = \"result_option_map_or_default\", issue = \"138099\")]\n  1301:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1302:     pub const fn map_or_default<U, F>(self, f: F) -> U\n  1303:     where\n  1304:         U: [const] Default,\n  1305:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1306:     {\n  1307:         match self {\n  1308:             Some(t) => f(t),\n  1309:             None => U::default(),\n  1310:         }\n  1311:     }\n  1312: \n  1313:     /// Transforms the `Option<T>` into a [`Result<T, E>`], mapping [`Some(v)`] to\n  1314:     /// [`Ok(v)`] and [`None`] to [`Err(err)`].\n  1315:     ///\n  1316:     /// Arguments passed to `ok_or` are eagerly evaluated; if you are passing the\n  1317:     /// result of a function call, it is recommended to use [`ok_or_else`], which is\n  1318:     /// lazily evaluated.",
    "nanvix_source": "  1288:     /// let y: Option<&str> = None;\n  1289:     ///\n  1290:     /// assert_eq!(x.map_or_default(|x| x.len()), 2);\n  1291:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n  1292:     /// ```\n  1293:     ///\n  1294:     /// [default value]: Default::default\n  1295:     #[inline]\n  1296:     #[stable(feature = \"result_option_map_or_default\", since = \"CURRENT_RUSTC_VERSION\")]\n  1297:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1298:     pub const fn map_or_default<U, F>(self, f: F) -> U\n  1299:     where\n  1300:         U: [const] Default,\n  1301:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1302:     {\n  1303:         match self {\n  1304:             Some(t) => f(t),\n  1305:             None => U::default(),\n  1306:         }\n  1307:     }\n  1308: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::map_or_else",
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
            "name": "D"
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
                          "inputs": [],
                          "output": {
                            "generic": "U"
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
                "generic": "D"
              }
            }
          },
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
      "name": "map_or_else",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "default",
            {
              "generic": "D"
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
          "generic": "U"
        }
      }
    },
    "verification_source": "  1255:     /// parses a command line argument (if present), or the contents of a file to\n  1256:     /// an integer.  However, unlike accessing the command line argument, reading\n  1257:     /// the file is fallible, so it must be wrapped with `Ok`.\n  1258:     ///\n  1259:     /// ```no_run\n  1260:     /// # fn main() -> Result<(), Box<dyn std::error::Error>> {\n  1261:     /// let v: u64 = std::env::args()\n  1262:     ///    .nth(1)\n  1263:     ///    .map_or_else(|| std::fs::read_to_string(\"/etc/someconfig.conf\"), Ok)?\n  1264:     ///    .parse()?;\n  1265:     /// #   Ok(())\n  1266:     /// # }\n  1267:     /// ```\n  1268:     #[inline]\n  1269:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1270:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1271:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n  1272:     where\n  1273:         D: [const] FnOnce() -> U + [const] Destruct,\n  1274:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1275:     {\n  1276:         match self {\n  1277:             Some(t) => f(t),\n  1278:             None => default(),\n  1279:         }\n  1280:     }\n  1281: \n  1282:     /// Maps an `Option<T>` to a `U` by applying function `f` to the contained\n  1283:     /// value if the option is [`Some`], otherwise if [`None`], returns the\n  1284:     /// [default value] for the type `U`.\n  1285:     ///\n  1286:     /// # Examples\n  1287:     ///",
    "nanvix_source": "  1259:     /// let v: u64 = std::env::args()\n  1260:     ///    .nth(1)\n  1261:     ///    .map_or_else(|| std::fs::read_to_string(\"/etc/someconfig.conf\"), Ok)?\n  1262:     ///    .parse()?;\n  1263:     /// #   Ok(())\n  1264:     /// # }\n  1265:     /// ```\n  1266:     #[inline]\n  1267:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1268:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1269:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n  1270:     where\n  1271:         D: [const] FnOnce() -> U + [const] Destruct,\n  1272:         F: [const] FnOnce(T) -> U + [const] Destruct,\n  1273:     {\n  1274:         match self {\n  1275:             Some(t) => f(t),\n  1276:             None => default(),\n  1277:         }\n  1278:     }\n  1279: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::or_else",
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
                          "inputs": [],
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
      "name": "or_else",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
    "verification_source": "  1631:     /// Returns the option if it contains a value, otherwise calls `f` and\n  1632:     /// returns the result.\n  1633:     ///\n  1634:     /// # Examples\n  1635:     ///\n  1636:     /// ```\n  1637:     /// fn nobody() -> Option<&'static str> { None }\n  1638:     /// fn vikings() -> Option<&'static str> { Some(\"vikings\") }\n  1639:     ///\n  1640:     /// assert_eq!(Some(\"barbarians\").or_else(vikings), Some(\"barbarians\"));\n  1641:     /// assert_eq!(None.or_else(vikings), Some(\"vikings\"));\n  1642:     /// assert_eq!(None.or_else(nobody), None);\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1646:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1647:     pub const fn or_else<F>(self, f: F) -> Option<T>\n  1648:     where\n  1649:         F: [const] FnOnce() -> Option<T> + [const] Destruct,\n  1650:         //FIXME(const_hack): this `T: [const] Destruct` is unnecessary, but even precise live drops can't tell\n  1651:         // no value of type `T` gets dropped here\n  1652:         T: [const] Destruct,\n  1653:     {\n  1654:         match self {\n  1655:             x @ Some(_) => x,\n  1656:             None => f(),\n  1657:         }\n  1658:     }\n  1659: \n  1660:     /// Returns [`Some`] if exactly one of `self`, `optb` is [`Some`], otherwise returns [`None`].\n  1661:     ///\n  1662:     /// # Examples\n  1663:     ///",
    "nanvix_source": "  1633:     /// fn nobody() -> Option<&'static str> { None }\n  1634:     /// fn vikings() -> Option<&'static str> { Some(\"vikings\") }\n  1635:     ///\n  1636:     /// assert_eq!(Some(\"barbarians\").or_else(vikings), Some(\"barbarians\"));\n  1637:     /// assert_eq!(None.or_else(vikings), Some(\"vikings\"));\n  1638:     /// assert_eq!(None.or_else(nobody), None);\n  1639:     /// ```\n  1640:     #[inline]\n  1641:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1642:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1643:     pub const fn or_else<F>(self, f: F) -> Option<T>\n  1644:     where\n  1645:         F: [const] FnOnce() -> Option<T> + [const] Destruct,\n  1646:         //FIXME(const_hack): this `T: [const] Destruct` is unnecessary, but even precise live drops can't tell\n  1647:         // no value of type `T` gets dropped here\n  1648:         T: [const] Destruct,\n  1649:     {\n  1650:         match self {\n  1651:             x @ Some(_) => x,\n  1652:             None => f(),\n  1653:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::take_if",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
                                "is_mutable": true,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
                "generic": "P"
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
      "name": "take_if",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "predicate",
            {
              "generic": "P"
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
    "verification_source": "  1915:     /// let prev = x.take_if(|v| if *v == 42 {\n  1916:     ///     *v += 1;\n  1917:     ///     false\n  1918:     /// } else {\n  1919:     ///     false\n  1920:     /// });\n  1921:     /// assert_eq!(x, Some(43));\n  1922:     /// assert_eq!(prev, None);\n  1923:     ///\n  1924:     /// let prev = x.take_if(|v| *v == 43);\n  1925:     /// assert_eq!(x, None);\n  1926:     /// assert_eq!(prev, Some(43));\n  1927:     /// ```\n  1928:     #[inline]\n  1929:     #[stable(feature = \"option_take_if\", since = \"1.80.0\")]\n  1930:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1931:     pub const fn take_if<P>(&mut self, predicate: P) -> Option<T>\n  1932:     where\n  1933:         P: [const] FnOnce(&mut T) -> bool + [const] Destruct,\n  1934:     {\n  1935:         if self.as_mut().map_or(false, predicate) { self.take() } else { None }\n  1936:     }\n  1937: \n  1938:     /// Replaces the actual value in the option by the value given in parameter,\n  1939:     /// returning the old value if present,\n  1940:     /// leaving a [`Some`] in its place without deinitializing either one.\n  1941:     ///\n  1942:     /// # Examples\n  1943:     ///\n  1944:     /// ```\n  1945:     /// let mut x = Some(2);\n  1946:     /// let old = x.replace(5);\n  1947:     /// assert_eq!(x, Some(5));",
    "nanvix_source": "  1921:     /// assert_eq!(x, Some(43));\n  1922:     /// assert_eq!(prev, None);\n  1923:     ///\n  1924:     /// let prev = x.take_if(|v| *v == 43);\n  1925:     /// assert_eq!(x, None);\n  1926:     /// assert_eq!(prev, Some(43));\n  1927:     /// ```\n  1928:     #[inline]\n  1929:     #[stable(feature = \"option_take_if\", since = \"1.80.0\")]\n  1930:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1931:     pub const fn take_if<P>(&mut self, predicate: P) -> Option<T>\n  1932:     where\n  1933:         P: [const] FnOnce(&mut T) -> bool + [const] Destruct,\n  1934:     {\n  1935:         if self.as_mut().map_or(false, predicate) { self.take() } else { None }\n  1936:     }\n  1937: \n  1938:     /// Replaces the actual value in the option by the value given in parameter,\n  1939:     /// returning the old value if present,\n  1940:     /// leaving a [`Some`] in its place without deinitializing either one.\n  1941:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::map_addr",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
    ],
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
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "parenthesized": {
                            "inputs": [
                              {
                                "resolved_path": {
                                  "args": {
                                    "angle_bracketed": {
                                      "args": [
                                        {
                                          "type": {
                                            "primitive": "usize"
                                          }
                                        }
                                      ],
                                      "constraints": []
                                    }
                                  },
                                  "id": 1039,
                                  "path": "NonZero"
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
                                          "primitive": "usize"
                                        }
                                      }
                                    ],
                                    "constraints": []
                                  }
                                },
                                "id": 1039,
                                "path": "NonZero"
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
                "default": null,
                "is_synthetic": true
              }
            },
            "name": "impl FnOnce(NonZero<usize>) -> NonZero<usize>"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "map_addr",
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
              "impl_trait": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "resolved_path": {
                                "args": {
                                  "angle_bracketed": {
                                    "args": [
                                      {
                                        "type": {
                                          "primitive": "usize"
                                        }
                                      }
                                    ],
                                    "constraints": []
                                  }
                                },
                                "id": 1039,
                                "path": "NonZero"
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
                                        "primitive": "usize"
                                      }
                                    }
                                  ],
                                  "constraints": []
                                }
                              },
                              "id": 1039,
                              "path": "NonZero"
                            }
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
                    }
                  }
                }
              ]
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   359:     #[inline]\n   360:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   361:     pub fn with_addr(self, addr: NonZero<usize>) -> Self {\n   362:         // SAFETY: The result of `ptr::from::with_addr` is non-null because `addr` is guaranteed to be non-zero.\n   363:         unsafe { NonNull::new_unchecked(self.as_ptr().with_addr(addr.get()) as *mut _) }\n   364:     }\n   365: \n   366:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the\n   367:     /// [provenance][crate::ptr#provenance] of `self`.\n   368:     ///\n   369:     /// For more details, see the equivalent method on a raw pointer, [`pointer::map_addr`].\n   370:     ///\n   371:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   372:     #[must_use]\n   373:     #[inline]\n   374:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   375:     pub fn map_addr(self, f: impl FnOnce(NonZero<usize>) -> NonZero<usize>) -> Self {\n   376:         self.with_addr(f(self.addr()))\n   377:     }\n   378: \n   379:     /// Acquires the underlying `*mut` pointer.\n   380:     ///\n   381:     /// # Examples\n   382:     ///\n   383:     /// ```\n   384:     /// use std::ptr::NonNull;\n   385:     ///\n   386:     /// let mut x = 0u32;\n   387:     /// let ptr = NonNull::new(&mut x).expect(\"ptr is null!\");\n   388:     ///\n   389:     /// let x_value = unsafe { *ptr.as_ptr() };\n   390:     /// assert_eq!(x_value, 0);\n   391:     ///",
    "nanvix_source": "   362: \n   363:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the\n   364:     /// [provenance][crate::ptr#provenance] of `self`.\n   365:     ///\n   366:     /// For more details, see the equivalent method on a raw pointer, [`pointer::map_addr`].\n   367:     ///\n   368:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   369:     #[must_use]\n   370:     #[inline]\n   371:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   372:     pub fn map_addr(self, f: impl FnOnce(NonZero<usize>) -> NonZero<usize>) -> Self {\n   373:         self.with_addr(f(self.addr()))\n   374:     }\n   375: \n   376:     /// Acquires the underlying `*mut` pointer.\n   377:     ///\n   378:     /// # Examples\n   379:     ///\n   380:     /// ```\n   381:     /// use std::ptr::NonNull;\n   382:     ///",
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
