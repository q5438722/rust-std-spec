For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::LowerHex::fmt",
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
        "item_id": "core:1655",
        "kind": "trait",
        "name": "LowerHex",
        "path": [
          "core",
          "fmt",
          "LowerHex"
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
    "verification_source": "  1364: ///         let val = self.0;\n  1365: ///\n  1366: ///         fmt::LowerHex::fmt(&val, f) // delegate to i32's implementation\n  1367: ///     }\n  1368: /// }\n  1369: ///\n  1370: /// let l = Length(9);\n  1371: ///\n  1372: /// assert_eq!(format!(\"l as hex is: {l:x}\"), \"l as hex is: 9\");\n  1373: ///\n  1374: /// assert_eq!(format!(\"l as hex is: {l:#010x}\"), \"l as hex is: 0x00000009\");\n  1375: /// ```\n  1376: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1377: pub trait LowerHex: PointeeSized {\n  1378:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1379:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1380:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1381: }\n  1382: \n  1383: /// `X` formatting.\n  1384: ///\n  1385: /// The `UpperHex` trait should format its output as a number in hexadecimal, with `A` through `F`\n  1386: /// in upper case.\n  1387: ///\n  1388: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1389: /// negative values are formatted as the two\u2019s complement representation.\n  1390: ///\n  1391: /// The alternate flag, `#`, adds a `0x` in front of the output.\n  1392: ///\n  1393: /// For more information on formatters, see [the module-level documentation][module].\n  1394: ///\n  1395: /// [module]: ../../std/fmt/index.html\n  1396: ///",
    "nanvix_source": "  1370: /// let l = Length(9);\n  1371: ///\n  1372: /// assert_eq!(format!(\"l as hex is: {l:x}\"), \"l as hex is: 9\");\n  1373: ///\n  1374: /// assert_eq!(format!(\"l as hex is: {l:#010x}\"), \"l as hex is: 0x00000009\");\n  1375: /// ```\n  1376: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1377: pub trait LowerHex: PointeeSized {\n  1378:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1379:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1380:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1381: }\n  1382: \n  1383: /// `X` formatting.\n  1384: ///\n  1385: /// The `UpperHex` trait should format its output as a number in hexadecimal, with `A` through `F`\n  1386: /// in upper case.\n  1387: ///\n  1388: /// For primitive signed integers (`i8` to `i128`, and `isize`),\n  1389: /// negative values are formatted as the two\u2019s complement representation.\n  1390: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Octal::fmt",
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
        "item_id": "core:1652",
        "kind": "trait",
        "name": "Octal",
        "path": [
          "core",
          "fmt",
          "Octal"
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
    "verification_source": "  1250: ///         let val = self.0;\n  1251: ///\n  1252: ///         fmt::Octal::fmt(&val, f) // delegate to i32's implementation\n  1253: ///     }\n  1254: /// }\n  1255: ///\n  1256: /// let l = Length(9);\n  1257: ///\n  1258: /// assert_eq!(format!(\"l as octal is: {l:o}\"), \"l as octal is: 11\");\n  1259: ///\n  1260: /// assert_eq!(format!(\"l as octal is: {l:#06o}\"), \"l as octal is: 0o0011\");\n  1261: /// ```\n  1262: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1263: pub trait Octal: PointeeSized {\n  1264:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1265:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1266:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1267: }\n  1268: \n  1269: /// `b` formatting.\n  1270: ///\n  1271: /// The `Binary` trait should format its output as a number in binary.\n  1272: ///\n  1273: /// For primitive signed integers ([`i8`] to [`i128`], and [`isize`]),\n  1274: /// negative values are formatted as the two\u2019s complement representation.\n  1275: ///\n  1276: /// The alternate flag, `#`, adds a `0b` in front of the output.\n  1277: ///\n  1278: /// For more information on formatters, see [the module-level documentation][module].\n  1279: ///\n  1280: /// [module]: ../../std/fmt/index.html\n  1281: ///\n  1282: /// # Examples",
    "nanvix_source": "  1256: /// let l = Length(9);\n  1257: ///\n  1258: /// assert_eq!(format!(\"l as octal is: {l:o}\"), \"l as octal is: 11\");\n  1259: ///\n  1260: /// assert_eq!(format!(\"l as octal is: {l:#06o}\"), \"l as octal is: 0o0011\");\n  1261: /// ```\n  1262: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1263: pub trait Octal: PointeeSized {\n  1264:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1265:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1266:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1267: }\n  1268: \n  1269: /// `b` formatting.\n  1270: ///\n  1271: /// The `Binary` trait should format its output as a number in binary.\n  1272: ///\n  1273: /// For primitive signed integers ([`i8`] to [`i128`], and [`isize`]),\n  1274: /// negative values are formatted as the two\u2019s complement representation.\n  1275: ///\n  1276: /// The alternate flag, `#`, adds a `0b` in front of the output.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Pointer::fmt",
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
        "item_id": "core:9577",
        "kind": "trait",
        "name": "Pointer",
        "path": [
          "core",
          "fmt",
          "Pointer"
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
    "verification_source": "  1478: ///     }\n  1479: /// }\n  1480: ///\n  1481: /// let l = Length(42);\n  1482: ///\n  1483: /// println!(\"l is in memory here: {l:p}\");\n  1484: ///\n  1485: /// let l_ptr = format!(\"{l:018p}\");\n  1486: /// assert_eq!(l_ptr.len(), 18);\n  1487: /// assert_eq!(&l_ptr[..2], \"0x\");\n  1488: /// ```\n  1489: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1490: #[rustc_diagnostic_item = \"Pointer\"]\n  1491: pub trait Pointer: PointeeSized {\n  1492:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1493:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1494:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1495: }\n  1496: \n  1497: /// `e` formatting.\n  1498: ///\n  1499: /// The `LowerExp` trait should format its output in scientific notation with a lower-case `e`.\n  1500: ///\n  1501: /// For more information on formatters, see [the module-level documentation][module].\n  1502: ///\n  1503: /// [module]: ../../std/fmt/index.html\n  1504: ///\n  1505: /// # Examples\n  1506: ///\n  1507: /// Basic usage with `f64`:\n  1508: ///\n  1509: /// ```\n  1510: /// let x = 42.0; // 42.0 is '4.2e1' in scientific notation",
    "nanvix_source": "  1484: ///\n  1485: /// let l_ptr = format!(\"{l:018p}\");\n  1486: /// assert_eq!(l_ptr.len(), 18);\n  1487: /// assert_eq!(&l_ptr[..2], \"0x\");\n  1488: /// ```\n  1489: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1490: #[rustc_diagnostic_item = \"Pointer\"]\n  1491: pub trait Pointer: PointeeSized {\n  1492:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1493:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1494:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1495: }\n  1496: \n  1497: /// `e` formatting.\n  1498: ///\n  1499: /// The `LowerExp` trait should format its output in scientific notation with a lower-case `e`.\n  1500: ///\n  1501: /// For more information on formatters, see [the module-level documentation][module].\n  1502: ///\n  1503: /// [module]: ../../std/fmt/index.html\n  1504: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::UpperExp::fmt",
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
        "item_id": "core:1664",
        "kind": "trait",
        "name": "UpperExp",
        "path": [
          "core",
          "fmt",
          "UpperExp"
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
    "verification_source": "  1580: /// let l = Length(100);\n  1581: ///\n  1582: /// assert_eq!(\n  1583: ///     format!(\"l in scientific notation is: {l:E}\"),\n  1584: ///     \"l in scientific notation is: 1E2\"\n  1585: /// );\n  1586: ///\n  1587: /// assert_eq!(\n  1588: ///     format!(\"l in scientific notation is: {l:05E}\"),\n  1589: ///     \"l in scientific notation is: 001E2\"\n  1590: /// );\n  1591: /// ```\n  1592: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1593: pub trait UpperExp: PointeeSized {\n  1594:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1595:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1596:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1597: }\n  1598: \n  1599: /// Takes an output stream and an `Arguments` struct that can be precompiled with\n  1600: /// the `format_args!` macro.\n  1601: ///\n  1602: /// The arguments will be formatted according to the specified format string\n  1603: /// into the output stream provided.\n  1604: ///\n  1605: /// # Examples\n  1606: ///\n  1607: /// Basic usage:\n  1608: ///\n  1609: /// ```\n  1610: /// use std::fmt;\n  1611: ///\n  1612: /// let mut output = String::new();",
    "nanvix_source": "  1586: ///\n  1587: /// assert_eq!(\n  1588: ///     format!(\"l in scientific notation is: {l:05E}\"),\n  1589: ///     \"l in scientific notation is: 001E2\"\n  1590: /// );\n  1591: /// ```\n  1592: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1593: pub trait UpperExp: PointeeSized {\n  1594:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1595:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1596:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1597: }\n  1598: \n  1599: /// Takes an output stream and an `Arguments` struct that can be precompiled with\n  1600: /// the `format_args!` macro.\n  1601: ///\n  1602: /// The arguments will be formatted according to the specified format string\n  1603: /// into the output stream provided.\n  1604: ///\n  1605: /// # Examples\n  1606: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::UpperHex::fmt",
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
        "item_id": "core:1658",
        "kind": "trait",
        "name": "UpperHex",
        "path": [
          "core",
          "fmt",
          "UpperHex"
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
    "verification_source": "  1419: ///         let val = self.0;\n  1420: ///\n  1421: ///         fmt::UpperHex::fmt(&val, f) // delegate to i32's implementation\n  1422: ///     }\n  1423: /// }\n  1424: ///\n  1425: /// let l = Length(i32::MAX);\n  1426: ///\n  1427: /// assert_eq!(format!(\"l as hex is: {l:X}\"), \"l as hex is: 7FFFFFFF\");\n  1428: ///\n  1429: /// assert_eq!(format!(\"l as hex is: {l:#010X}\"), \"l as hex is: 0x7FFFFFFF\");\n  1430: /// ```\n  1431: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1432: pub trait UpperHex: PointeeSized {\n  1433:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1434:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1435:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1436: }\n  1437: \n  1438: /// `p` formatting.\n  1439: ///\n  1440: /// The `Pointer` trait should format its output as a memory location. This is commonly presented\n  1441: /// as hexadecimal. For more information on formatters, see [the module-level documentation][module].\n  1442: ///\n  1443: /// Printing of pointers is not a reliable way to discover how Rust programs are implemented.\n  1444: /// The act of reading an address changes the program itself, and may change how the data is represented\n  1445: /// in memory, and may affect which optimizations are applied to the code.\n  1446: ///\n  1447: /// The printed pointer values are not guaranteed to be stable nor unique identifiers of objects.\n  1448: /// Rust allows moving values to different memory locations, and may reuse the same memory locations\n  1449: /// for different purposes.\n  1450: ///\n  1451: /// There is no guarantee that the printed value can be converted back to a pointer.",
    "nanvix_source": "  1425: /// let l = Length(i32::MAX);\n  1426: ///\n  1427: /// assert_eq!(format!(\"l as hex is: {l:X}\"), \"l as hex is: 7FFFFFFF\");\n  1428: ///\n  1429: /// assert_eq!(format!(\"l as hex is: {l:#010X}\"), \"l as hex is: 0x7FFFFFFF\");\n  1430: /// ```\n  1431: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1432: pub trait UpperHex: PointeeSized {\n  1433:     #[doc = include_str!(\"fmt_trait_method_doc.md\")]\n  1434:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1435:     fn fmt(&self, f: &mut Formatter<'_>) -> Result;\n  1436: }\n  1437: \n  1438: /// `p` formatting.\n  1439: ///\n  1440: /// The `Pointer` trait should format its output as a memory location. This is commonly presented\n  1441: /// as hexadecimal. For more information on formatters, see [the module-level documentation][module].\n  1442: ///\n  1443: /// Printing of pointers is not a reliable way to discover how Rust programs are implemented.\n  1444: /// The act of reading an address changes the program itself, and may change how the data is represented\n  1445: /// in memory, and may affect which optimizations are applied to the code.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Write::write_char",
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
      "name": "write_char",
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
        "item_id": "core:29961",
        "kind": "trait",
        "name": "Write",
        "path": [
          "core",
          "fmt",
          "Write"
        ]
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
            "c",
            {
              "primitive": "char"
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
    "verification_source": "   167:     /// # Examples\n   168:     ///\n   169:     /// ```\n   170:     /// use std::fmt::{Error, Write};\n   171:     ///\n   172:     /// fn writer<W: Write>(f: &mut W, c: char) -> Result<(), Error> {\n   173:     ///     f.write_char(c)\n   174:     /// }\n   175:     ///\n   176:     /// let mut buf = String::new();\n   177:     /// writer(&mut buf, 'a')?;\n   178:     /// writer(&mut buf, 'b')?;\n   179:     /// assert_eq!(&buf, \"ab\");\n   180:     /// # std::fmt::Result::Ok(())\n   181:     /// ```\n   182:     #[stable(feature = \"fmt_write_char\", since = \"1.1.0\")]\n   183:     fn write_char(&mut self, c: char) -> Result {\n   184:         self.write_str(c.encode_utf8(&mut [0; char::MAX_LEN_UTF8]))\n   185:     }\n   186: \n   187:     /// Glue for usage of the [`write!`] macro with implementors of this trait.\n   188:     ///\n   189:     /// This method should generally not be invoked manually, but rather through\n   190:     /// the [`write!`] macro itself.\n   191:     ///\n   192:     /// # Errors\n   193:     ///\n   194:     /// This function will return an instance of [`Error`] on error. Please see\n   195:     /// [write_str](Write::write_str) for details.\n   196:     ///\n   197:     /// # Examples\n   198:     ///\n   199:     /// ```",
    "nanvix_source": "   175:     ///     f.write_char(c)\n   176:     /// }\n   177:     ///\n   178:     /// let mut buf = String::new();\n   179:     /// writer(&mut buf, 'a')?;\n   180:     /// writer(&mut buf, 'b')?;\n   181:     /// assert_eq!(&buf, \"ab\");\n   182:     /// # std::fmt::Result::Ok(())\n   183:     /// ```\n   184:     #[stable(feature = \"fmt_write_char\", since = \"1.1.0\")]\n   185:     fn write_char(&mut self, c: char) -> Result {\n   186:         self.write_str(c.encode_utf8(&mut [0; char::MAX_LEN_UTF8]))\n   187:     }\n   188: \n   189:     /// Glue for usage of the [`write!`] macro with implementors of this trait.\n   190:     ///\n   191:     /// This method should generally not be invoked manually, but rather through\n   192:     /// the [`write!`] macro itself.\n   193:     ///\n   194:     /// # Errors\n   195:     ///",
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
