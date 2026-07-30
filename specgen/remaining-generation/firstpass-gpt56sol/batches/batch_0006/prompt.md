For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::sort_unstable",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
                      "id": 50,
                      "path": "Ord"
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
      "name": "sort_unstable",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
        "output": null
      }
    },
    "verification_source": "  3117:     /// May panic if the implementation of [`Ord`] for `T` does not implement a [total order], or if\n  3118:     /// the [`Ord`] implementation panics.\n  3119:     ///\n  3120:     /// # Examples\n  3121:     ///\n  3122:     /// ```\n  3123:     /// let mut v = [4, -5, 1, -3, 2];\n  3124:     ///\n  3125:     /// v.sort_unstable();\n  3126:     /// assert_eq!(v, [-5, -3, 1, 2, 4]);\n  3127:     /// ```\n  3128:     ///\n  3129:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3130:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3131:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3132:     #[inline]\n  3133:     pub fn sort_unstable(&mut self)\n  3134:     where\n  3135:         T: Ord,\n  3136:     {\n  3137:         sort::unstable::sort(self, &mut T::lt);\n  3138:     }\n  3139: \n  3140:     /// Sorts the slice in ascending order with a comparison function, **without** preserving the\n  3141:     /// initial order of equal elements.\n  3142:     ///\n  3143:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not\n  3144:     /// allocate), and *O*(*n* \\* log(*n*)) worst-case.\n  3145:     ///\n  3146:     /// If the comparison function `compare` does not implement a [total order], the function\n  3147:     /// may panic; even if the function exits normally, the resulting order of elements in the slice\n  3148:     /// is unspecified. See also the note on panicking below.\n  3149:     ///",
    "nanvix_source": "  3129:     /// let mut v = [4, -5, 1, -3, 2];\n  3130:     ///\n  3131:     /// v.sort_unstable();\n  3132:     /// assert_eq!(v, [-5, -3, 1, 2, 4]);\n  3133:     /// ```\n  3134:     ///\n  3135:     /// [ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort\n  3136:     /// [total order]: https://en.wikipedia.org/wiki/Total_order\n  3137:     #[stable(feature = \"sort_unstable\", since = \"1.20.0\")]\n  3138:     #[inline]\n  3139:     pub fn sort_unstable(&mut self)\n  3140:     where\n  3141:         T: Ord,\n  3142:     {\n  3143:         sort::unstable::sort(self, &mut T::lt);\n  3144:     }\n  3145: \n  3146:     /// Sorts the slice in ascending order with a comparison function, **without** preserving the\n  3147:     /// initial order of equal elements.\n  3148:     ///\n  3149:     /// This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::contains",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "contains",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1347:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1348:     /// function or closure that determines if a character matches.\n  1349:     ///\n  1350:     /// [`char`]: prim@char\n  1351:     /// [pattern]: self::pattern\n  1352:     ///\n  1353:     /// # Examples\n  1354:     ///\n  1355:     /// ```\n  1356:     /// let bananas = \"bananas\";\n  1357:     ///\n  1358:     /// assert!(bananas.contains(\"nana\"));\n  1359:     /// assert!(!bananas.contains(\"apples\"));\n  1360:     /// ```\n  1361:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1362:     #[inline]\n  1363:     pub fn contains<P: Pattern>(&self, pat: P) -> bool {\n  1364:         pat.is_contained_in(self)\n  1365:     }\n  1366: \n  1367:     /// Returns `true` if the given pattern matches a prefix of this\n  1368:     /// string slice.\n  1369:     ///\n  1370:     /// Returns `false` if it does not.\n  1371:     ///\n  1372:     /// The [pattern] can be a `&str`, in which case this function will return true if\n  1373:     /// the `&str` is a prefix of this string slice.\n  1374:     ///\n  1375:     /// The [pattern] can also be a [`char`], a slice of [`char`]s, or a\n  1376:     /// function or closure that determines if a character matches.\n  1377:     /// These will only be checked against the first character of this string slice.\n  1378:     /// Look at the second example below regarding behavior for slices of [`char`]s.\n  1379:     ///",
    "nanvix_source": "  1372:     /// # Examples\n  1373:     ///\n  1374:     /// ```\n  1375:     /// let bananas = \"bananas\";\n  1376:     ///\n  1377:     /// assert!(bananas.contains(\"nana\"));\n  1378:     /// assert!(!bananas.contains(\"apples\"));\n  1379:     /// ```\n  1380:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1381:     #[inline]\n  1382:     pub fn contains<P: Pattern>(&self, pat: P) -> bool {\n  1383:         pat.is_contained_in(self)\n  1384:     }\n  1385: \n  1386:     /// Returns `true` if the given pattern matches a prefix of this\n  1387:     /// string slice.\n  1388:     ///\n  1389:     /// Returns `false` if it does not.\n  1390:     ///\n  1391:     /// The [pattern] can be a `&str`, in which case this function will return true if\n  1392:     /// the `&str` is a prefix of this string slice.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::find",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "find",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
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
                      "primitive": "usize"
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
    "verification_source": "  1461:     /// assert_eq!(s.find(char::is_whitespace), Some(5));\n  1462:     /// assert_eq!(s.find(char::is_lowercase), Some(1));\n  1463:     /// assert_eq!(s.find(|c: char| c.is_whitespace() || c.is_lowercase()), Some(1));\n  1464:     /// assert_eq!(s.find(|c: char| (c < 'o') && (c > 'a')), Some(4));\n  1465:     /// ```\n  1466:     ///\n  1467:     /// Not finding the pattern:\n  1468:     ///\n  1469:     /// ```\n  1470:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n  1471:     /// let x: &[_] = &['1', '2'];\n  1472:     ///\n  1473:     /// assert_eq!(s.find(x), None);\n  1474:     /// ```\n  1475:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1476:     #[inline]\n  1477:     pub fn find<P: Pattern>(&self, pat: P) -> Option<usize> {\n  1478:         pat.into_searcher(self).next_match().map(|(i, _)| i)\n  1479:     }\n  1480: \n  1481:     /// Returns the byte index for the first character of the last match of the pattern in\n  1482:     /// this string slice.\n  1483:     ///\n  1484:     /// Returns [`None`] if the pattern doesn't match.\n  1485:     ///\n  1486:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1487:     /// function or closure that determines if a character matches.\n  1488:     ///\n  1489:     /// [`char`]: prim@char\n  1490:     /// [pattern]: self::pattern\n  1491:     ///\n  1492:     /// # Examples\n  1493:     ///",
    "nanvix_source": "  1486:     /// Not finding the pattern:\n  1487:     ///\n  1488:     /// ```\n  1489:     /// let s = \"L\u00f6we \u8001\u864e L\u00e9opard\";\n  1490:     /// let x: &[_] = &['1', '2'];\n  1491:     ///\n  1492:     /// assert_eq!(s.find(x), None);\n  1493:     /// ```\n  1494:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1495:     #[inline]\n  1496:     pub fn find<P: Pattern>(&self, pat: P) -> Option<usize> {\n  1497:         pat.into_searcher(self).next_match().map(|(i, _)| i)\n  1498:     }\n  1499: \n  1500:     /// Returns the byte index for the first character of the last match of the pattern in\n  1501:     /// this string slice.\n  1502:     ///\n  1503:     /// Returns [`None`] if the pattern doesn't match.\n  1504:     ///\n  1505:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1506:     /// function or closure that determines if a character matches.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_once",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "split_once",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "delimiter",
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "primitive": "str"
                            }
                          }
                        },
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
    "verification_source": "  1950:         RSplitN(self.splitn(n, pat).0)\n  1951:     }\n  1952: \n  1953:     /// Splits the string on the first occurrence of the specified delimiter and\n  1954:     /// returns prefix before delimiter and suffix after delimiter.\n  1955:     ///\n  1956:     /// # Examples\n  1957:     ///\n  1958:     /// ```\n  1959:     /// assert_eq!(\"cfg\".split_once('='), None);\n  1960:     /// assert_eq!(\"cfg=\".split_once('='), Some((\"cfg\", \"\")));\n  1961:     /// assert_eq!(\"cfg=foo\".split_once('='), Some((\"cfg\", \"foo\")));\n  1962:     /// assert_eq!(\"cfg=foo=bar\".split_once('='), Some((\"cfg\", \"foo=bar\")));\n  1963:     /// ```\n  1964:     #[stable(feature = \"str_split_once\", since = \"1.52.0\")]\n  1965:     #[inline]\n  1966:     pub fn split_once<P: Pattern>(&self, delimiter: P) -> Option<(&'_ str, &'_ str)> {\n  1967:         let (start, end) = delimiter.into_searcher(self).next_match()?;\n  1968:         // SAFETY: `Searcher` is known to return valid indices.\n  1969:         unsafe { Some((self.get_unchecked(..start), self.get_unchecked(end..))) }\n  1970:     }\n  1971: \n  1972:     /// Splits the string on the last occurrence of the specified delimiter and\n  1973:     /// returns prefix before delimiter and suffix after delimiter.\n  1974:     ///\n  1975:     /// # Examples\n  1976:     ///\n  1977:     /// ```\n  1978:     /// assert_eq!(\"cfg\".rsplit_once('='), None);\n  1979:     /// assert_eq!(\"cfg=\".rsplit_once('='), Some((\"cfg\", \"\")));\n  1980:     /// assert_eq!(\"cfg=foo\".rsplit_once('='), Some((\"cfg\", \"foo\")));\n  1981:     /// assert_eq!(\"cfg=foo=bar\".rsplit_once('='), Some((\"cfg=foo\", \"bar\")));\n  1982:     /// ```",
    "nanvix_source": "  1975:     /// # Examples\n  1976:     ///\n  1977:     /// ```\n  1978:     /// assert_eq!(\"cfg\".split_once('='), None);\n  1979:     /// assert_eq!(\"cfg=\".split_once('='), Some((\"cfg\", \"\")));\n  1980:     /// assert_eq!(\"cfg=foo\".split_once('='), Some((\"cfg\", \"foo\")));\n  1981:     /// assert_eq!(\"cfg=foo=bar\".split_once('='), Some((\"cfg\", \"foo=bar\")));\n  1982:     /// ```\n  1983:     #[stable(feature = \"str_split_once\", since = \"1.52.0\")]\n  1984:     #[inline]\n  1985:     pub fn split_once<P: Pattern>(&self, delimiter: P) -> Option<(&'_ str, &'_ str)> {\n  1986:         let (start, end) = delimiter.into_searcher(self).next_match()?;\n  1987:         // SAFETY: `Searcher` is known to return valid indices.\n  1988:         unsafe { Some((self.get_unchecked(..start), self.get_unchecked(end..))) }\n  1989:     }\n  1990: \n  1991:     /// Splits the string on the last occurrence of the specified delimiter and\n  1992:     /// returns prefix before delimiter and suffix after delimiter.\n  1993:     ///\n  1994:     /// # Examples\n  1995:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::starts_with",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "starts_with",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1385:     /// ```\n  1386:     /// let bananas = \"bananas\";\n  1387:     ///\n  1388:     /// assert!(bananas.starts_with(\"bana\"));\n  1389:     /// assert!(!bananas.starts_with(\"nana\"));\n  1390:     /// ```\n  1391:     ///\n  1392:     /// ```\n  1393:     /// let bananas = \"bananas\";\n  1394:     ///\n  1395:     /// // Note that both of these assert successfully.\n  1396:     /// assert!(bananas.starts_with(&['b', 'a', 'n', 'a']));\n  1397:     /// assert!(bananas.starts_with(&['a', 'b', 'c', 'd']));\n  1398:     /// ```\n  1399:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1400:     #[rustc_diagnostic_item = \"str_starts_with\"]\n  1401:     pub fn starts_with<P: Pattern>(&self, pat: P) -> bool {\n  1402:         pat.is_prefix_of(self)\n  1403:     }\n  1404: \n  1405:     /// Returns `true` if the given pattern matches a suffix of this\n  1406:     /// string slice.\n  1407:     ///\n  1408:     /// Returns `false` if it does not.\n  1409:     ///\n  1410:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1411:     /// function or closure that determines if a character matches.\n  1412:     ///\n  1413:     /// [`char`]: prim@char\n  1414:     /// [pattern]: self::pattern\n  1415:     ///\n  1416:     /// # Examples\n  1417:     ///",
    "nanvix_source": "  1410:     ///\n  1411:     /// ```\n  1412:     /// let bananas = \"bananas\";\n  1413:     ///\n  1414:     /// // Note that both of these assert successfully.\n  1415:     /// assert!(bananas.starts_with(&['b', 'a', 'n', 'a']));\n  1416:     /// assert!(bananas.starts_with(&['a', 'b', 'c', 'd']));\n  1417:     /// ```\n  1418:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1419:     #[rustc_diagnostic_item = \"str_starts_with\"]\n  1420:     pub fn starts_with<P: Pattern>(&self, pat: P) -> bool {\n  1421:         pat.is_prefix_of(self)\n  1422:     }\n  1423: \n  1424:     /// Returns `true` if the given pattern matches a suffix of this\n  1425:     /// string slice.\n  1426:     ///\n  1427:     /// Returns `false` if it does not.\n  1428:     ///\n  1429:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1430:     /// function or closure that determines if a character matches.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::strip_prefix",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
      "name": "strip_prefix",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "prefix",
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
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  2423:     /// function or closure that determines if a character matches.\n  2424:     ///\n  2425:     /// [`char`]: prim@char\n  2426:     /// [pattern]: self::pattern\n  2427:     /// [`trim_start_matches`]: Self::trim_start_matches\n  2428:     ///\n  2429:     /// # Examples\n  2430:     ///\n  2431:     /// ```\n  2432:     /// assert_eq!(\"foo:bar\".strip_prefix(\"foo:\"), Some(\"bar\"));\n  2433:     /// assert_eq!(\"foo:bar\".strip_prefix(\"bar\"), None);\n  2434:     /// assert_eq!(\"foofoo\".strip_prefix(\"foo\"), Some(\"foo\"));\n  2435:     /// ```\n  2436:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2437:                   without modifying the original\"]\n  2438:     #[stable(feature = \"str_strip\", since = \"1.45.0\")]\n  2439:     pub fn strip_prefix<P: Pattern>(&self, prefix: P) -> Option<&str> {\n  2440:         prefix.strip_prefix_of(self)\n  2441:     }\n  2442: \n  2443:     /// Returns a string slice with the suffix removed.\n  2444:     ///\n  2445:     /// If the string ends with the pattern `suffix`, returns the substring before the suffix,\n  2446:     /// wrapped in `Some`.  Unlike [`trim_end_matches`], this method removes the suffix exactly once.\n  2447:     ///\n  2448:     /// If the string does not end with `suffix`, returns `None`.\n  2449:     ///\n  2450:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2451:     /// function or closure that determines if a character matches.\n  2452:     ///\n  2453:     /// [`char`]: prim@char\n  2454:     /// [pattern]: self::pattern\n  2455:     /// [`trim_end_matches`]: Self::trim_end_matches",
    "nanvix_source": "  2448:     /// # Examples\n  2449:     ///\n  2450:     /// ```\n  2451:     /// assert_eq!(\"foo:bar\".strip_prefix(\"foo:\"), Some(\"bar\"));\n  2452:     /// assert_eq!(\"foo:bar\".strip_prefix(\"bar\"), None);\n  2453:     /// assert_eq!(\"foofoo\".strip_prefix(\"foo\"), Some(\"foo\"));\n  2454:     /// ```\n  2455:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2456:                   without modifying the original\"]\n  2457:     #[stable(feature = \"str_strip\", since = \"1.45.0\")]\n  2458:     pub fn strip_prefix<P: Pattern>(&self, prefix: P) -> Option<&str> {\n  2459:         prefix.strip_prefix_of(self)\n  2460:     }\n  2461: \n  2462:     /// Returns a string slice with the suffix removed.\n  2463:     ///\n  2464:     /// If the string ends with the pattern `suffix`, returns the substring before the suffix,\n  2465:     /// wrapped in `Some`.  Unlike [`trim_end_matches`], this method removes the suffix exactly once.\n  2466:     ///\n  2467:     /// If the string does not end with `suffix`, returns `None`.\n  2468:     ///",
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
