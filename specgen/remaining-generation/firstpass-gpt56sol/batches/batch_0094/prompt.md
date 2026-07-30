For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::split_inclusive",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
                            "primitive": "bool"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "split_inclusive",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 10054,
            "path": "SplitInclusive"
          }
        }
      }
    },
    "verification_source": "  2286:     /// ```\n  2287:     ///\n  2288:     /// If the last element of the slice is matched,\n  2289:     /// that element will be considered the terminator of the preceding slice.\n  2290:     /// That slice will be the last item returned by the iterator.\n  2291:     ///\n  2292:     /// ```\n  2293:     /// let slice = [3, 10, 40, 33];\n  2294:     /// let mut iter = slice.split_inclusive(|num| num % 3 == 0);\n  2295:     ///\n  2296:     /// assert_eq!(iter.next().unwrap(), &[3]);\n  2297:     /// assert_eq!(iter.next().unwrap(), &[10, 40, 33]);\n  2298:     /// assert!(iter.next().is_none());\n  2299:     /// ```\n  2300:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  2301:     #[inline]\n  2302:     pub fn split_inclusive<F>(&self, pred: F) -> SplitInclusive<'_, T, F>\n  2303:     where\n  2304:         F: FnMut(&T) -> bool,\n  2305:     {\n  2306:         SplitInclusive::new(self, pred)\n  2307:     }\n  2308: \n  2309:     /// Returns an iterator over mutable subslices separated by elements that\n  2310:     /// match `pred`. The matched element is contained in the previous\n  2311:     /// subslice as a terminator.\n  2312:     ///\n  2313:     /// # Examples\n  2314:     ///\n  2315:     /// ```\n  2316:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2317:     ///\n  2318:     /// for group in v.split_inclusive_mut(|num| *num % 3 == 0) {",
    "nanvix_source": "  2295:     /// ```\n  2296:     /// let slice = [3, 10, 40, 33];\n  2297:     /// let mut iter = slice.split_inclusive(|num| num % 3 == 0);\n  2298:     ///\n  2299:     /// assert_eq!(iter.next().unwrap(), &[3]);\n  2300:     /// assert_eq!(iter.next().unwrap(), &[10, 40, 33]);\n  2301:     /// assert!(iter.next().is_none());\n  2302:     /// ```\n  2303:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  2304:     #[inline]\n  2305:     pub fn split_inclusive<F>(&self, pred: F) -> SplitInclusive<'_, T, F>\n  2306:     where\n  2307:         F: FnMut(&T) -> bool,\n  2308:     {\n  2309:         SplitInclusive::new(self, pred)\n  2310:     }\n  2311: \n  2312:     /// Returns an iterator over mutable subslices separated by elements that\n  2313:     /// match `pred`. The matched element is contained in the previous\n  2314:     /// subslice as a terminator.\n  2315:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::splitn",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
                            "primitive": "bool"
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "splitn",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "n",
            {
              "primitive": "usize"
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
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
            "id": 13449,
            "path": "SplitN"
          }
        }
      }
    },
    "verification_source": "  2400:     /// slice.\n  2401:     ///\n  2402:     /// # Examples\n  2403:     ///\n  2404:     /// Print the slice split once by numbers divisible by 3 (i.e., `[10, 40]`,\n  2405:     /// `[20, 60, 50]`):\n  2406:     ///\n  2407:     /// ```\n  2408:     /// let v = [10, 40, 30, 20, 60, 50];\n  2409:     ///\n  2410:     /// for group in v.splitn(2, |num| *num % 3 == 0) {\n  2411:     ///     println!(\"{group:?}\");\n  2412:     /// }\n  2413:     /// ```\n  2414:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2415:     #[inline]\n  2416:     pub fn splitn<F>(&self, n: usize, pred: F) -> SplitN<'_, T, F>\n  2417:     where\n  2418:         F: FnMut(&T) -> bool,\n  2419:     {\n  2420:         SplitN::new(self.split(pred), n)\n  2421:     }\n  2422: \n  2423:     /// Returns an iterator over mutable subslices separated by elements that match\n  2424:     /// `pred`, limited to returning at most `n` items. The matched element is\n  2425:     /// not contained in the subslices.\n  2426:     ///\n  2427:     /// The last element returned, if any, will contain the remainder of the\n  2428:     /// slice.\n  2429:     ///\n  2430:     /// # Examples\n  2431:     ///\n  2432:     /// ```",
    "nanvix_source": "  2409:     ///\n  2410:     /// ```\n  2411:     /// let v = [10, 40, 30, 20, 60, 50];\n  2412:     ///\n  2413:     /// for group in v.splitn(2, |num| *num % 3 == 0) {\n  2414:     ///     println!(\"{group:?}\");\n  2415:     /// }\n  2416:     /// ```\n  2417:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2418:     #[inline]\n  2419:     pub fn splitn<F>(&self, n: usize, pred: F) -> SplitN<'_, T, F>\n  2420:     where\n  2421:         F: FnMut(&T) -> bool,\n  2422:     {\n  2423:         SplitN::new(self.split(pred), n)\n  2424:     }\n  2425: \n  2426:     /// Returns an iterator over mutable subslices separated by elements that match\n  2427:     /// `pred`, limited to returning at most `n` items. The matched element is\n  2428:     /// not contained in the subslices.\n  2429:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::utf8_chunks",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "utf8_chunks",
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
          "slice": {
            "primitive": "u8"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51885",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 10183,
            "path": "Utf8Chunks"
          }
        }
      }
    },
    "verification_source": "    30:     ///         for byte in chunk.invalid() {\n    31:     ///             write!(repr, \"\\\\x{:02X}\", byte).unwrap();\n    32:     ///         }\n    33:     ///     }\n    34:     ///     repr.push('\"');\n    35:     ///     repr\n    36:     /// }\n    37:     ///\n    38:     /// fn main() {\n    39:     ///     let lit = cstr_literal(b\"\\xferris the \\xf0\\x9f\\xa6\\x80\\x07\");\n    40:     ///     let expected = stringify!(c\"\\xFErris the \ud83e\udd80\\u{7}\");\n    41:     ///     assert_eq!(lit, expected);\n    42:     /// }\n    43:     /// ```\n    44:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n    45:     pub fn utf8_chunks(&self) -> Utf8Chunks<'_> {\n    46:         Utf8Chunks { source: self }\n    47:     }\n    48: }\n    49: \n    50: /// An item returned by the [`Utf8Chunks`] iterator.\n    51: ///\n    52: /// A `Utf8Chunk` stores a sequence of [`u8`] up to the first broken character\n    53: /// when decoding a UTF-8 string.\n    54: ///\n    55: /// # Examples\n    56: ///\n    57: /// ```\n    58: /// // An invalid UTF-8 string\n    59: /// let bytes = b\"foo\\xF1\\x80bar\";\n    60: ///\n    61: /// // Decode the first `Utf8Chunk`\n    62: /// let chunk = bytes.utf8_chunks().next().unwrap();",
    "nanvix_source": "    36:     /// }\n    37:     ///\n    38:     /// fn main() {\n    39:     ///     let lit = cstr_literal(b\"\\xferris the \\xf0\\x9f\\xa6\\x80\\x07\");\n    40:     ///     let expected = stringify!(c\"\\xFErris the \ud83e\udd80\\u{7}\");\n    41:     ///     assert_eq!(lit, expected);\n    42:     /// }\n    43:     /// ```\n    44:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n    45:     pub fn utf8_chunks(&self) -> Utf8Chunks<'_> {\n    46:         Utf8Chunks { source: self }\n    47:     }\n    48: }\n    49: \n    50: /// An item returned by the [`Utf8Chunks`] iterator.\n    51: ///\n    52: /// A `Utf8Chunk` stores a sequence of [`u8`] up to the first broken character\n    53: /// when decoding a UTF-8 string.\n    54: ///\n    55: /// # Examples\n    56: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::windows",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "windows",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "size",
            {
              "primitive": "usize"
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
            "id": 10060,
            "path": "Windows"
          }
        }
      }
    },
    "verification_source": "  1099:     /// [LendingIterator]: https://blog.rust-lang.org/2022/10/28/gats-stabilization.html\n  1100:     /// ```\n  1101:     /// use std::cell::Cell;\n  1102:     ///\n  1103:     /// let mut array = ['R', 'u', 's', 't', ' ', '2', '0', '1', '5'];\n  1104:     /// let slice = &mut array[..];\n  1105:     /// let slice_of_cells: &[Cell<char>] = Cell::from_mut(slice).as_slice_of_cells();\n  1106:     /// for w in slice_of_cells.windows(3) {\n  1107:     ///     Cell::swap(&w[0], &w[2]);\n  1108:     /// }\n  1109:     /// assert_eq!(array, ['s', 't', ' ', '2', '0', '1', '5', 'u', 'R']);\n  1110:     /// ```\n  1111:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1112:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1113:     #[inline]\n  1114:     #[track_caller]\n  1115:     pub const fn windows(&self, size: usize) -> Windows<'_, T> {\n  1116:         let size = NonZero::new(size).expect(\"window size must be non-zero\");\n  1117:         Windows::new(self, size)\n  1118:     }\n  1119: \n  1120:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1121:     /// beginning of the slice.\n  1122:     ///\n  1123:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1124:     /// slice, then the last chunk will not have length `chunk_size`.\n  1125:     ///\n  1126:     /// See [`chunks_exact`] for a variant of this iterator that returns chunks of always exactly\n  1127:     /// `chunk_size` elements, and [`rchunks`] for the same iterator but starting at the end of the\n  1128:     /// slice.\n  1129:     ///\n  1130:     /// If your `chunk_size` is a constant, consider using [`as_chunks`] instead, which will\n  1131:     /// give references to arrays of exactly that length, rather than slices.",
    "nanvix_source": "  1108:     /// let slice_of_cells: &[Cell<char>] = Cell::from_mut(slice).as_slice_of_cells();\n  1109:     /// for w in slice_of_cells.windows(3) {\n  1110:     ///     Cell::swap(&w[0], &w[2]);\n  1111:     /// }\n  1112:     /// assert_eq!(array, ['s', 't', ' ', '2', '0', '1', '5', 'u', 'R']);\n  1113:     /// ```\n  1114:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1115:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1116:     #[inline]\n  1117:     #[track_caller]\n  1118:     pub const fn windows(&self, size: usize) -> Windows<'_, T> {\n  1119:         let size = NonZero::new(size).expect(\"window size must be non-zero\");\n  1120:         Windows::new(self, size)\n  1121:     }\n  1122: \n  1123:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1124:     /// beginning of the slice.\n  1125:     ///\n  1126:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1127:     /// slice, then the last chunk will not have length `chunk_size`.\n  1128:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::bytes",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "bytes",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 10095,
            "path": "Bytes"
          }
        }
      }
    },
    "verification_source": "  1126:     /// through a string slice by byte. This method returns such an iterator.\n  1127:     ///\n  1128:     /// # Examples\n  1129:     ///\n  1130:     /// ```\n  1131:     /// let mut bytes = \"bors\".bytes();\n  1132:     ///\n  1133:     /// assert_eq!(Some(b'b'), bytes.next());\n  1134:     /// assert_eq!(Some(b'o'), bytes.next());\n  1135:     /// assert_eq!(Some(b'r'), bytes.next());\n  1136:     /// assert_eq!(Some(b's'), bytes.next());\n  1137:     ///\n  1138:     /// assert_eq!(None, bytes.next());\n  1139:     /// ```\n  1140:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1141:     #[inline]\n  1142:     pub fn bytes(&self) -> Bytes<'_> {\n  1143:         Bytes(self.as_bytes().iter().copied())\n  1144:     }\n  1145: \n  1146:     /// Splits a string slice by whitespace.\n  1147:     ///\n  1148:     /// The iterator returned will return string slices that are sub-slices of\n  1149:     /// the original string slice, separated by any amount of whitespace.\n  1150:     ///\n  1151:     /// 'Whitespace' is defined according to the terms of the Unicode Derived\n  1152:     /// Core Property `White_Space`. If you only want to split on ASCII whitespace\n  1153:     /// instead, use [`split_ascii_whitespace`].\n  1154:     ///\n  1155:     /// [`split_ascii_whitespace`]: str::split_ascii_whitespace\n  1156:     ///\n  1157:     /// # Examples\n  1158:     ///",
    "nanvix_source": "  1148:     ///\n  1149:     /// assert_eq!(Some(b'b'), bytes.next());\n  1150:     /// assert_eq!(Some(b'o'), bytes.next());\n  1151:     /// assert_eq!(Some(b'r'), bytes.next());\n  1152:     /// assert_eq!(Some(b's'), bytes.next());\n  1153:     ///\n  1154:     /// assert_eq!(None, bytes.next());\n  1155:     /// ```\n  1156:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1157:     #[inline]\n  1158:     pub fn bytes(&self) -> Bytes<'_> {\n  1159:         Bytes(self.as_bytes().iter().copied())\n  1160:     }\n  1161: \n  1162:     /// Splits a string slice by whitespace.\n  1163:     ///\n  1164:     /// The iterator returned will return string slices that are sub-slices of\n  1165:     /// the original string slice, separated by any amount of whitespace.\n  1166:     ///\n  1167:     /// 'Whitespace' is defined according to the terms of the Unicode Derived\n  1168:     /// Core Property `White_Space`. If you only want to split on ASCII whitespace",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::char_indices",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "char_indices",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 10092,
            "path": "CharIndices"
          }
        }
      }
    },
    "verification_source": "  1103:     /// ```\n  1104:     /// let yes = \"y\u0306es\";\n  1105:     ///\n  1106:     /// let mut char_indices = yes.char_indices();\n  1107:     ///\n  1108:     /// assert_eq!(Some((0, 'y')), char_indices.next()); // not (0, 'y\u0306')\n  1109:     /// assert_eq!(Some((1, '\\u{0306}')), char_indices.next());\n  1110:     ///\n  1111:     /// // note the 3 here - the previous character took up two bytes\n  1112:     /// assert_eq!(Some((3, 'e')), char_indices.next());\n  1113:     /// assert_eq!(Some((4, 's')), char_indices.next());\n  1114:     ///\n  1115:     /// assert_eq!(None, char_indices.next());\n  1116:     /// ```\n  1117:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1118:     #[inline]\n  1119:     pub fn char_indices(&self) -> CharIndices<'_> {\n  1120:         CharIndices { front_offset: 0, iter: self.chars() }\n  1121:     }\n  1122: \n  1123:     /// Returns an iterator over the bytes of a string slice.\n  1124:     ///\n  1125:     /// As a string slice consists of a sequence of bytes, we can iterate\n  1126:     /// through a string slice by byte. This method returns such an iterator.\n  1127:     ///\n  1128:     /// # Examples\n  1129:     ///\n  1130:     /// ```\n  1131:     /// let mut bytes = \"bors\".bytes();\n  1132:     ///\n  1133:     /// assert_eq!(Some(b'b'), bytes.next());\n  1134:     /// assert_eq!(Some(b'o'), bytes.next());\n  1135:     /// assert_eq!(Some(b'r'), bytes.next());",
    "nanvix_source": "  1125:     /// assert_eq!(Some((1, '\\u{0306}')), char_indices.next());\n  1126:     ///\n  1127:     /// // note the 3 here - the previous character took up two bytes\n  1128:     /// assert_eq!(Some((3, 'e')), char_indices.next());\n  1129:     /// assert_eq!(Some((4, 's')), char_indices.next());\n  1130:     ///\n  1131:     /// assert_eq!(None, char_indices.next());\n  1132:     /// ```\n  1133:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1134:     #[inline]\n  1135:     pub fn char_indices(&self) -> CharIndices<'_> {\n  1136:         CharIndices { front_offset: 0, iter: self.chars() }\n  1137:     }\n  1138: \n  1139:     /// Returns an iterator over the bytes of a string slice.\n  1140:     ///\n  1141:     /// As a string slice consists of a sequence of bytes, we can iterate\n  1142:     /// through a string slice by byte. This method returns such an iterator.\n  1143:     ///\n  1144:     /// # Examples\n  1145:     ///",
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
