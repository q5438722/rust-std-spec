For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::BufRead::lines",
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
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "lines",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
        ]
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3747,
            "path": "Lines"
          }
        }
      }
    },
    "verification_source": "  2668:     /// ```\n  2669:     /// use std::io::{self, BufRead};\n  2670:     ///\n  2671:     /// let cursor = io::Cursor::new(b\"lorem\\nipsum\\r\\ndolor\");\n  2672:     ///\n  2673:     /// let mut lines_iter = cursor.lines().map(|l| l.unwrap());\n  2674:     /// assert_eq!(lines_iter.next(), Some(String::from(\"lorem\")));\n  2675:     /// assert_eq!(lines_iter.next(), Some(String::from(\"ipsum\")));\n  2676:     /// assert_eq!(lines_iter.next(), Some(String::from(\"dolor\")));\n  2677:     /// assert_eq!(lines_iter.next(), None);\n  2678:     /// ```\n  2679:     ///\n  2680:     /// # Errors\n  2681:     ///\n  2682:     /// Each line of the iterator has the same error semantics as [`BufRead::read_line`].\n  2683:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2684:     fn lines(self) -> Lines<Self>\n  2685:     where\n  2686:         Self: Sized,\n  2687:     {\n  2688:         Lines { buf: self }\n  2689:     }\n  2690: }\n  2691: \n  2692: /// Adapter to chain together two readers.\n  2693: ///\n  2694: /// This struct is generally created by calling [`chain`] on a reader.\n  2695: /// Please see the documentation of [`chain`] for more details.\n  2696: ///\n  2697: /// [`chain`]: Read::chain\n  2698: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2699: #[derive(Debug)]\n  2700: pub struct Chain<T, U> {",
    "nanvix_source": "  2210:     /// assert_eq!(lines_iter.next(), Some(String::from(\"lorem\")));\n  2211:     /// assert_eq!(lines_iter.next(), Some(String::from(\"ipsum\")));\n  2212:     /// assert_eq!(lines_iter.next(), Some(String::from(\"dolor\")));\n  2213:     /// assert_eq!(lines_iter.next(), None);\n  2214:     /// ```\n  2215:     ///\n  2216:     /// # Errors\n  2217:     ///\n  2218:     /// Each line of the iterator has the same error semantics as [`BufRead::read_line`].\n  2219:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2220:     fn lines(self) -> Lines<Self>\n  2221:     where\n  2222:         Self: Sized,\n  2223:     {\n  2224:         Lines { buf: self }\n  2225:     }\n  2226: }\n  2227: \n  2228: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2229: impl<T: Read, U: Read> Read for Chain<T, U> {\n  2230:     fn read(&mut self, buf: &mut [u8]) -> Result<usize> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::read_line",
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
      "external_or_hidden_runtime_state"
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
      "name": "read_line",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "buf"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
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
            "buf",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 218,
                    "path": "String"
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
                    "type": {
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2593:     /// buf.clear();\n  2594:     ///\n  2595:     /// // cursor is at 'b'\n  2596:     /// let num_bytes = cursor.read_line(&mut buf)\n  2597:     ///     .expect(\"reading from cursor won't fail\");\n  2598:     /// assert_eq!(num_bytes, 3);\n  2599:     /// assert_eq!(buf, \"bar\");\n  2600:     /// buf.clear();\n  2601:     ///\n  2602:     /// // cursor is at EOF\n  2603:     /// let num_bytes = cursor.read_line(&mut buf)\n  2604:     ///     .expect(\"reading from cursor won't fail\");\n  2605:     /// assert_eq!(num_bytes, 0);\n  2606:     /// assert_eq!(buf, \"\");\n  2607:     /// ```\n  2608:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2609:     fn read_line(&mut self, buf: &mut String) -> Result<usize> {\n  2610:         // Note that we are not calling the `.read_until` method here, but\n  2611:         // rather our hardcoded implementation. For more details as to why, see\n  2612:         // the comments in `default_read_to_string`.\n  2613:         unsafe { append_to_string(buf, |b| read_until(self, b'\\n', b)) }\n  2614:     }\n  2615: \n  2616:     /// Returns an iterator over the contents of this reader split on the byte\n  2617:     /// `byte`.\n  2618:     ///\n  2619:     /// The iterator returned from this function will return instances of\n  2620:     /// <code>[io::Result]<[Vec]\\<u8>></code>. Each vector returned will *not* have\n  2621:     /// the delimiter byte at the end.\n  2622:     ///\n  2623:     /// This function will yield errors whenever [`read_until`] would have\n  2624:     /// also yielded an error.\n  2625:     ///",
    "nanvix_source": "  2135:     /// assert_eq!(buf, \"bar\");\n  2136:     /// buf.clear();\n  2137:     ///\n  2138:     /// // cursor is at EOF\n  2139:     /// let num_bytes = cursor.read_line(&mut buf)\n  2140:     ///     .expect(\"reading from cursor won't fail\");\n  2141:     /// assert_eq!(num_bytes, 0);\n  2142:     /// assert_eq!(buf, \"\");\n  2143:     /// ```\n  2144:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2145:     fn read_line(&mut self, buf: &mut String) -> Result<usize> {\n  2146:         // Note that we are not calling the `.read_until` method here, but\n  2147:         // rather our hardcoded implementation. For more details as to why, see\n  2148:         // the comments in `default_read_to_string`.\n  2149:         unsafe { append_to_string(buf, |b| read_until(self, b'\\n', b)) }\n  2150:     }\n  2151: \n  2152:     /// Returns an iterator over the contents of this reader split on the byte\n  2153:     /// `byte`.\n  2154:     ///\n  2155:     /// The iterator returned from this function will return instances of",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::read_until",
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
      "external_or_hidden_runtime_state"
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
      "name": "read_until",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "buf"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
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
            "byte",
            {
              "primitive": "u8"
            }
          ],
          [
            "buf",
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
                            "type": {
                              "primitive": "u8"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 222,
                    "path": "Vec"
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
                    "type": {
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2460:     /// buf.clear();\n  2461:     ///\n  2462:     /// // cursor is at 'i'\n  2463:     /// let num_bytes = cursor.read_until(b'-', &mut buf)\n  2464:     ///     .expect(\"reading from cursor won't fail\");\n  2465:     /// assert_eq!(num_bytes, 5);\n  2466:     /// assert_eq!(buf, b\"ipsum\");\n  2467:     /// buf.clear();\n  2468:     ///\n  2469:     /// // cursor is at EOF\n  2470:     /// let num_bytes = cursor.read_until(b'-', &mut buf)\n  2471:     ///     .expect(\"reading from cursor won't fail\");\n  2472:     /// assert_eq!(num_bytes, 0);\n  2473:     /// assert_eq!(buf, b\"\");\n  2474:     /// ```\n  2475:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2476:     fn read_until(&mut self, byte: u8, buf: &mut Vec<u8>) -> Result<usize> {\n  2477:         read_until(self, byte, buf)\n  2478:     }\n  2479: \n  2480:     /// Skips all bytes until the delimiter `byte` or EOF is reached.\n  2481:     ///\n  2482:     /// This function will read (and discard) bytes from the underlying stream until the\n  2483:     /// delimiter or EOF is found.\n  2484:     ///\n  2485:     /// If successful, this function will return the total number of bytes read,\n  2486:     /// including the delimiter byte if found.\n  2487:     ///\n  2488:     /// This is useful for efficiently skipping data such as NUL-terminated strings\n  2489:     /// in binary file formats without buffering.\n  2490:     ///\n  2491:     /// This function is blocking and should be used carefully: it is possible for\n  2492:     /// an attacker to continuously send bytes without ever sending the delimiter",
    "nanvix_source": "  2002:     /// assert_eq!(buf, b\"ipsum\");\n  2003:     /// buf.clear();\n  2004:     ///\n  2005:     /// // cursor is at EOF\n  2006:     /// let num_bytes = cursor.read_until(b'-', &mut buf)\n  2007:     ///     .expect(\"reading from cursor won't fail\");\n  2008:     /// assert_eq!(num_bytes, 0);\n  2009:     /// assert_eq!(buf, b\"\");\n  2010:     /// ```\n  2011:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2012:     fn read_until(&mut self, byte: u8, buf: &mut Vec<u8>) -> Result<usize> {\n  2013:         read_until(self, byte, buf)\n  2014:     }\n  2015: \n  2016:     /// Skips all bytes until the delimiter `byte` or EOF is reached.\n  2017:     ///\n  2018:     /// This function will read (and discard) bytes from the underlying stream until the\n  2019:     /// delimiter or EOF is found.\n  2020:     ///\n  2021:     /// If successful, this function will return the total number of bytes read,\n  2022:     /// including the delimiter byte if found.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::skip_until",
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
      "external_or_hidden_runtime_state"
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
      "name": "skip_until",
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
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
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
            "byte",
            {
              "primitive": "u8"
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
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  2525:     ///     .expect(\"reading from cursor won't fail\");\n  2526:     /// assert_eq!(num_bytes, 30);\n  2527:     ///\n  2528:     /// // read animal type\n  2529:     /// let mut animal = Vec::new();\n  2530:     /// let num_bytes = cursor.read_until(b'\\0', &mut animal)\n  2531:     ///     .expect(\"reading from cursor won't fail\");\n  2532:     /// assert_eq!(num_bytes, 11);\n  2533:     /// assert_eq!(animal, b\"Crustacean\\0\");\n  2534:     ///\n  2535:     /// // reach EOF\n  2536:     /// let num_bytes = cursor.skip_until(b'\\0')\n  2537:     ///     .expect(\"reading from cursor won't fail\");\n  2538:     /// assert_eq!(num_bytes, 1);\n  2539:     /// ```\n  2540:     #[stable(feature = \"bufread_skip_until\", since = \"1.83.0\")]\n  2541:     fn skip_until(&mut self, byte: u8) -> Result<usize> {\n  2542:         skip_until(self, byte)\n  2543:     }\n  2544: \n  2545:     /// Reads all bytes until a newline (the `0xA` byte) is reached, and append\n  2546:     /// them to the provided `String` buffer.\n  2547:     ///\n  2548:     /// Previous content of the buffer will be preserved. To avoid appending to\n  2549:     /// the buffer, you need to [`clear`] it first.\n  2550:     ///\n  2551:     /// This function will read bytes from the underlying stream until the\n  2552:     /// newline delimiter (the `0xA` byte) or EOF is found. Once found, all bytes\n  2553:     /// up to, and including, the delimiter (if found) will be appended to\n  2554:     /// `buf`.\n  2555:     ///\n  2556:     /// If successful, this function will return the total number of bytes read.\n  2557:     ///",
    "nanvix_source": "  2067:     ///     .expect(\"reading from cursor won't fail\");\n  2068:     /// assert_eq!(num_bytes, 11);\n  2069:     /// assert_eq!(animal, b\"Crustacean\\0\");\n  2070:     ///\n  2071:     /// // reach EOF\n  2072:     /// let num_bytes = cursor.skip_until(b'\\0')\n  2073:     ///     .expect(\"reading from cursor won't fail\");\n  2074:     /// assert_eq!(num_bytes, 1);\n  2075:     /// ```\n  2076:     #[stable(feature = \"bufread_skip_until\", since = \"1.83.0\")]\n  2077:     fn skip_until(&mut self, byte: u8) -> Result<usize> {\n  2078:         skip_until(self, byte)\n  2079:     }\n  2080: \n  2081:     /// Reads all bytes until a newline (the `0xA` byte) is reached, and append\n  2082:     /// them to the provided `String` buffer.\n  2083:     ///\n  2084:     /// Previous content of the buffer will be preserved. To avoid appending to\n  2085:     /// the buffer, you need to [`clear`] it first.\n  2086:     ///\n  2087:     /// This function will read bytes from the underlying stream until the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufRead::split",
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
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "split",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2561",
        "kind": "trait",
        "name": "BufRead",
        "path": [
          "std",
          "io",
          "BufRead"
        ]
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
            "byte",
            {
              "primitive": "u8"
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4516,
            "path": "Split"
          }
        }
      }
    },
    "verification_source": "  2631:     /// [`std::io::Cursor`][`Cursor`] is a type that implements `BufRead`. In\n  2632:     /// this example, we use [`Cursor`] to iterate over all hyphen delimited\n  2633:     /// segments in a byte slice\n  2634:     ///\n  2635:     /// ```\n  2636:     /// use std::io::{self, BufRead};\n  2637:     ///\n  2638:     /// let cursor = io::Cursor::new(b\"lorem-ipsum-dolor\");\n  2639:     ///\n  2640:     /// let mut split_iter = cursor.split(b'-').map(|l| l.unwrap());\n  2641:     /// assert_eq!(split_iter.next(), Some(b\"lorem\".to_vec()));\n  2642:     /// assert_eq!(split_iter.next(), Some(b\"ipsum\".to_vec()));\n  2643:     /// assert_eq!(split_iter.next(), Some(b\"dolor\".to_vec()));\n  2644:     /// assert_eq!(split_iter.next(), None);\n  2645:     /// ```\n  2646:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2647:     fn split(self, byte: u8) -> Split<Self>\n  2648:     where\n  2649:         Self: Sized,\n  2650:     {\n  2651:         Split { buf: self, delim: byte }\n  2652:     }\n  2653: \n  2654:     /// Returns an iterator over the lines of this reader.\n  2655:     ///\n  2656:     /// The iterator returned from this function will yield instances of\n  2657:     /// <code>[io::Result]<[String]></code>. Each string returned will *not* have a newline\n  2658:     /// byte (the `0xA` byte) or `CRLF` (`0xD`, `0xA` bytes) at the end.\n  2659:     ///\n  2660:     /// [io::Result]: self::Result \"io::Result\"\n  2661:     ///\n  2662:     /// # Examples\n  2663:     ///",
    "nanvix_source": "  2173:     ///\n  2174:     /// let cursor = io::Cursor::new(b\"lorem-ipsum-dolor\");\n  2175:     ///\n  2176:     /// let mut split_iter = cursor.split(b'-').map(|l| l.unwrap());\n  2177:     /// assert_eq!(split_iter.next(), Some(b\"lorem\".to_vec()));\n  2178:     /// assert_eq!(split_iter.next(), Some(b\"ipsum\".to_vec()));\n  2179:     /// assert_eq!(split_iter.next(), Some(b\"dolor\".to_vec()));\n  2180:     /// assert_eq!(split_iter.next(), None);\n  2181:     /// ```\n  2182:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2183:     fn split(self, byte: u8) -> Split<Self>\n  2184:     where\n  2185:         Self: Sized,\n  2186:     {\n  2187:         Split { buf: self, delim: byte }\n  2188:     }\n  2189: \n  2190:     /// Returns an iterator over the lines of this reader.\n  2191:     ///\n  2192:     /// The iterator returned from this function will yield instances of\n  2193:     /// <code>[io::Result]<[String]></code>. Each string returned will *not* have a newline",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::IsTerminal::is_terminal",
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
      "external_or_hidden_runtime_state"
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
      "name": "is_terminal",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2654",
        "kind": "trait",
        "name": "IsTerminal",
        "path": [
          "std",
          "io",
          "stdio",
          "IsTerminal"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1230:     ///     println!(\"Hello {}\", name.trim_end());\n  1231:     ///\n  1232:     ///     Ok(())\n  1233:     /// }\n  1234:     /// ```\n  1235:     ///\n  1236:     /// The example can be run in two ways:\n  1237:     ///\n  1238:     /// - If you run this example by piping some text to it, e.g. `echo \"foo\" | path/to/executable`\n  1239:     ///   it will print: `Hello foo`.\n  1240:     /// - If you instead run the example interactively by running `path/to/executable` directly, it will\n  1241:     ///   prompt for input.\n  1242:     ///\n  1243:     /// [changes]: io#platform-specific-behavior\n  1244:     /// [`Stdin`]: crate::io::Stdin\n  1245:     #[doc(alias = \"isatty\")]\n  1246:     #[stable(feature = \"is_terminal\", since = \"1.70.0\")]\n  1247:     fn is_terminal(&self) -> bool;\n  1248: }\n  1249: \n  1250: macro_rules! impl_is_terminal {\n  1251:     ($($t:ty),*$(,)?) => {$(\n  1252:         #[unstable(feature = \"sealed\", issue = \"none\")]\n  1253:         impl crate::sealed::Sealed for $t {}\n  1254: \n  1255:         #[stable(feature = \"is_terminal\", since = \"1.70.0\")]\n  1256:         impl IsTerminal for $t {\n  1257:             #[inline]\n  1258:             fn is_terminal(&self) -> bool {\n  1259:                 crate::sys::io::is_terminal(self)\n  1260:             }\n  1261:         }\n  1262:     )*}",
    "nanvix_source": "  1236:     ///\n  1237:     /// The example can be run in two ways:\n  1238:     ///\n  1239:     /// - If you run this example by piping some text to it, e.g. `echo \"foo\" | path/to/executable`\n  1240:     ///   it will print: `Hello foo`.\n  1241:     /// - If you instead run the example interactively by running `path/to/executable` directly, it will\n  1242:     ///   prompt for input.\n  1243:     ///\n  1244:     /// [changes]: io#platform-specific-behavior\n  1245:     /// [`Stdin`]: crate::io::Stdin\n  1246:     #[doc(alias = \"isatty\", alias = \"atty\")]\n  1247:     #[stable(feature = \"is_terminal\", since = \"1.70.0\")]\n  1248:     fn is_terminal(&self) -> bool;\n  1249: }\n  1250: \n  1251: macro_rules! impl_is_terminal {\n  1252:     ($($t:ty),*$(,)?) => {$(\n  1253:         #[stable(feature = \"is_terminal\", since = \"1.70.0\")]\n  1254:         impl IsTerminal for $t {\n  1255:             #[inline]\n  1256:             fn is_terminal(&self) -> bool {",
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
