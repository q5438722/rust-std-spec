For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::string::String::from_utf16le",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16le",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
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
                      "resolved_path": {
                        "args": null,
                        "id": 119,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 4036,
                        "path": "FromUtf16Error"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   767:     ///\n   768:     /// ```\n   769:     /// #![feature(str_from_utf16_endian)]\n   770:     /// // \ud834\udd1emusic\n   771:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,\n   772:     ///           0x73, 0x00, 0x69, 0x00, 0x63, 0x00];\n   773:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   774:     ///            String::from_utf16le(v).unwrap());\n   775:     ///\n   776:     /// // \ud834\udd1emu<invalid>ic\n   777:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,\n   778:     ///           0x00, 0xD8, 0x69, 0x00, 0x63, 0x00];\n   779:     /// assert!(String::from_utf16le(v).is_err());\n   780:     /// ```\n   781:     #[cfg(not(no_global_oom_handling))]\n   782:     #[unstable(feature = \"str_from_utf16_endian\", issue = \"116258\")]\n   783:     pub fn from_utf16le(v: &[u8]) -> Result<String, FromUtf16Error> {\n   784:         let (chunks, []) = v.as_chunks::<2>() else {\n   785:             return Err(FromUtf16Error(()));\n   786:         };\n   787:         match (cfg!(target_endian = \"little\"), unsafe { v.align_to::<u16>() }) {\n   788:             (true, ([], v, [])) => Self::from_utf16(v),\n   789:             _ => char::decode_utf16(chunks.iter().copied().map(u16::from_le_bytes))\n   790:                 .collect::<Result<_, _>>()\n   791:                 .map_err(|_| FromUtf16Error(())),\n   792:         }\n   793:     }\n   794: \n   795:     /// Decode a UTF-16LE\u2013encoded slice `v` into a `String`, replacing\n   796:     /// invalid data with [the replacement character (`U+FFFD`)][U+FFFD].\n   797:     ///\n   798:     /// Unlike [`from_utf8_lossy`] which returns a [`Cow<'a, str>`],\n   799:     /// `from_utf16le_lossy` returns a `String` since the UTF-16 to UTF-8",
    "nanvix_source": "   781:     /// assert_eq!(String::from(\"\ud834\udd1emusic\"),\n   782:     ///            String::from_utf16le(v).unwrap());\n   783:     ///\n   784:     /// // \ud834\udd1emu<invalid>ic\n   785:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,\n   786:     ///           0x00, 0xD8, 0x69, 0x00, 0x63, 0x00];\n   787:     /// assert!(String::from_utf16le(v).is_err());\n   788:     /// ```\n   789:     #[cfg(not(no_global_oom_handling))]\n   790:     #[stable(feature = \"str_from_utf16_endian\", since = \"CURRENT_RUSTC_VERSION\")]\n   791:     pub fn from_utf16le(v: &[u8]) -> Result<String, FromUtf16Error> {\n   792:         let (chunks, []) = v.as_chunks::<2>() else {\n   793:             return Err(FromUtf16Error { kind: FromUtf16ErrorKind::OddBytes });\n   794:         };\n   795:         match (cfg!(target_endian = \"little\"), unsafe { v.align_to::<u16>() }) {\n   796:             (true, ([], v, [])) => Self::from_utf16(v),\n   797:             _ => char::decode_utf16(chunks.iter().copied().map(u16::from_le_bytes))\n   798:                 .collect::<Result<_, _>>()\n   799:                 .map_err(|_| FromUtf16Error { kind: FromUtf16ErrorKind::LoneSurrogate }),\n   800:         }\n   801:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf16le_lossy",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf16le_lossy",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
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
            "id": 119,
            "path": "String"
          }
        }
      }
    },
    "verification_source": "   806:     /// # Examples\n   807:     ///\n   808:     /// Basic usage:\n   809:     ///\n   810:     /// ```\n   811:     /// #![feature(str_from_utf16_endian)]\n   812:     /// // \ud834\udd1emus<invalid>ic<invalid>\n   813:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,\n   814:     ///           0x73, 0x00, 0x1E, 0xDD, 0x69, 0x00, 0x63, 0x00,\n   815:     ///           0x34, 0xD8];\n   816:     ///\n   817:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   818:     ///            String::from_utf16le_lossy(v));\n   819:     /// ```\n   820:     #[cfg(not(no_global_oom_handling))]\n   821:     #[unstable(feature = \"str_from_utf16_endian\", issue = \"116258\")]\n   822:     pub fn from_utf16le_lossy(v: &[u8]) -> String {\n   823:         match (cfg!(target_endian = \"little\"), unsafe { v.align_to::<u16>() }) {\n   824:             (true, ([], v, [])) => Self::from_utf16_lossy(v),\n   825:             (true, ([], v, [_remainder])) => Self::from_utf16_lossy(v) + \"\\u{FFFD}\",\n   826:             _ => {\n   827:                 let (chunks, remainder) = v.as_chunks::<2>();\n   828:                 let string = char::decode_utf16(chunks.iter().copied().map(u16::from_le_bytes))\n   829:                     .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   830:                     .collect();\n   831:                 if remainder.is_empty() { string } else { string + \"\\u{FFFD}\" }\n   832:             }\n   833:         }\n   834:     }\n   835: \n   836:     /// Decode a UTF-16BE\u2013encoded vector `v` into a `String`,\n   837:     /// returning [`Err`] if `v` contains any invalid data.\n   838:     ///",
    "nanvix_source": "   819:     /// // \ud834\udd1emus<invalid>ic<invalid>\n   820:     /// let v = &[0x34, 0xD8, 0x1E, 0xDD, 0x6d, 0x00, 0x75, 0x00,\n   821:     ///           0x73, 0x00, 0x1E, 0xDD, 0x69, 0x00, 0x63, 0x00,\n   822:     ///           0x34, 0xD8];\n   823:     ///\n   824:     /// assert_eq!(String::from(\"\ud834\udd1emus\\u{FFFD}ic\\u{FFFD}\"),\n   825:     ///            String::from_utf16le_lossy(v));\n   826:     /// ```\n   827:     #[cfg(not(no_global_oom_handling))]\n   828:     #[stable(feature = \"str_from_utf16_endian\", since = \"CURRENT_RUSTC_VERSION\")]\n   829:     pub fn from_utf16le_lossy(v: &[u8]) -> String {\n   830:         match (cfg!(target_endian = \"little\"), unsafe { v.align_to::<u16>() }) {\n   831:             (true, ([], v, [])) => Self::from_utf16_lossy(v),\n   832:             (true, ([], v, [_remainder])) => Self::from_utf16_lossy(v) + \"\\u{FFFD}\",\n   833:             _ => {\n   834:                 let (chunks, remainder) = v.as_chunks::<2>();\n   835:                 let string = char::decode_utf16(chunks.iter().copied().map(u16::from_le_bytes))\n   836:                     .map(|r| r.unwrap_or(char::REPLACEMENT_CHARACTER))\n   837:                     .collect();\n   838:                 if remainder.is_empty() { string } else { string + \"\\u{FFFD}\" }\n   839:             }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf8",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf8",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "vec",
            {
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
                "id": 114,
                "path": "Vec"
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
                        "id": 119,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 963,
                        "path": "FromUtf8Error"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   544:     /// // some invalid bytes, in a vector\n   545:     /// let sparkle_heart = vec![0, 159, 146, 150];\n   546:     ///\n   547:     /// assert!(String::from_utf8(sparkle_heart).is_err());\n   548:     /// ```\n   549:     ///\n   550:     /// See the docs for [`FromUtf8Error`] for more details on what you can do\n   551:     /// with this error.\n   552:     ///\n   553:     /// [`from_utf8_unchecked`]: String::from_utf8_unchecked\n   554:     /// [`Vec<u8>`]: crate::vec::Vec \"Vec\"\n   555:     /// [`&str`]: prim@str \"&str\"\n   556:     /// [`into_bytes`]: String::into_bytes\n   557:     #[inline]\n   558:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   559:     #[rustc_diagnostic_item = \"string_from_utf8\"]\n   560:     pub fn from_utf8(vec: Vec<u8>) -> Result<String, FromUtf8Error> {\n   561:         match str::from_utf8(&vec) {\n   562:             Ok(..) => Ok(String { vec }),\n   563:             Err(e) => Err(FromUtf8Error { bytes: vec, error: e }),\n   564:         }\n   565:     }\n   566: \n   567:     /// Converts a slice of bytes to a string, including invalid characters.\n   568:     ///\n   569:     /// Strings are made of bytes ([`u8`]), and a slice of bytes\n   570:     /// ([`&[u8]`][byteslice]) is made of bytes, so this function converts\n   571:     /// between the two. Not all byte slices are valid strings, however: strings\n   572:     /// are required to be valid UTF-8. During this conversion,\n   573:     /// `from_utf8_lossy()` will replace any invalid UTF-8 sequences with\n   574:     /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD], which looks like this: \ufffd\n   575:     ///\n   576:     /// [byteslice]: prim@slice",
    "nanvix_source": "   559:     /// See the docs for [`FromUtf8Error`] for more details on what you can do\n   560:     /// with this error.\n   561:     ///\n   562:     /// [`from_utf8_unchecked`]: String::from_utf8_unchecked\n   563:     /// [`Vec<u8>`]: crate::vec::Vec \"Vec\"\n   564:     /// [`&str`]: prim@str \"&str\"\n   565:     /// [`into_bytes`]: String::into_bytes\n   566:     #[inline]\n   567:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   568:     #[rustc_diagnostic_item = \"string_from_utf8\"]\n   569:     pub fn from_utf8(vec: Vec<u8>) -> Result<String, FromUtf8Error> {\n   570:         match str::from_utf8(&vec) {\n   571:             Ok(..) => Ok(String { vec }),\n   572:             Err(e) => Err(FromUtf8Error { bytes: vec, error: e }),\n   573:         }\n   574:     }\n   575: \n   576:     /// Converts a slice of bytes to a string, including invalid characters.\n   577:     ///\n   578:     /// Strings are made of bytes ([`u8`]), and a slice of bytes\n   579:     /// ([`&[u8]`][byteslice]) is made of bytes, so this function converts",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::from_utf8_lossy",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "from_utf8_lossy",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "primitive": "str"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 129,
            "path": "Cow"
          }
        }
      }
    },
    "verification_source": "   603:     ///\n   604:     /// assert_eq!(\"\ud83d\udc96\", sparkle_heart);\n   605:     /// ```\n   606:     ///\n   607:     /// Incorrect bytes:\n   608:     ///\n   609:     /// ```\n   610:     /// // some invalid bytes\n   611:     /// let input = b\"Hello \\xF0\\x90\\x80World\";\n   612:     /// let output = String::from_utf8_lossy(input);\n   613:     ///\n   614:     /// assert_eq!(\"Hello \ufffdWorld\", output);\n   615:     /// ```\n   616:     #[must_use]\n   617:     #[cfg(not(no_global_oom_handling))]\n   618:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   619:     pub fn from_utf8_lossy(v: &[u8]) -> Cow<'_, str> {\n   620:         let mut iter = v.utf8_chunks();\n   621: \n   622:         let Some(chunk) = iter.next() else {\n   623:             return Cow::Borrowed(\"\");\n   624:         };\n   625:         let first_valid = chunk.valid();\n   626:         if chunk.invalid().is_empty() {\n   627:             debug_assert_eq!(first_valid.len(), v.len());\n   628:             return Cow::Borrowed(first_valid);\n   629:         }\n   630: \n   631:         const REPLACEMENT: &str = \"\\u{FFFD}\";\n   632: \n   633:         let mut res = String::with_capacity(v.len());\n   634:         res.push_str(first_valid);\n   635:         res.push_str(REPLACEMENT);",
    "nanvix_source": "   618:     /// ```\n   619:     /// // some invalid bytes\n   620:     /// let input = b\"Hello \\xF0\\x90\\x80World\";\n   621:     /// let output = String::from_utf8_lossy(input);\n   622:     ///\n   623:     /// assert_eq!(\"Hello \ufffdWorld\", output);\n   624:     /// ```\n   625:     #[must_use]\n   626:     #[cfg(not(no_global_oom_handling))]\n   627:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   628:     pub fn from_utf8_lossy(v: &[u8]) -> Cow<'_, str> {\n   629:         let mut iter = v.utf8_chunks();\n   630: \n   631:         let Some(chunk) = iter.next() else {\n   632:             return Cow::Borrowed(\"\");\n   633:         };\n   634:         let first_valid = chunk.valid();\n   635:         if chunk.invalid().is_empty() {\n   636:             debug_assert_eq!(first_valid.len(), v.len());\n   637:             return Cow::Borrowed(first_valid);\n   638:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::into_boxed_str",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
      "name": "into_boxed_str",
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
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
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
                      "primitive": "str"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "  2158:     /// Note that this call may reallocate and copy the bytes of the string.\n  2159:     ///\n  2160:     /// [`shrink_to_fit`]: String::shrink_to_fit\n  2161:     /// [str]: prim@str \"str\"\n  2162:     ///\n  2163:     /// # Examples\n  2164:     ///\n  2165:     /// ```\n  2166:     /// let s = String::from(\"hello\");\n  2167:     ///\n  2168:     /// let b = s.into_boxed_str();\n  2169:     /// ```\n  2170:     #[cfg(not(no_global_oom_handling))]\n  2171:     #[stable(feature = \"box_str\", since = \"1.4.0\")]\n  2172:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2173:     #[inline]\n  2174:     pub fn into_boxed_str(self) -> Box<str> {\n  2175:         let slice = self.vec.into_boxed_slice();\n  2176:         unsafe { from_boxed_utf8_unchecked(slice) }\n  2177:     }\n  2178: \n  2179:     /// Consumes and leaks the `String`, returning a mutable reference to the contents,\n  2180:     /// `&'a mut str`.\n  2181:     ///\n  2182:     /// The caller has free choice over the returned lifetime, including `'static`. Indeed,\n  2183:     /// this function is ideally used for data that lives for the remainder of the program's life,\n  2184:     /// as dropping the returned reference will cause a memory leak.\n  2185:     ///\n  2186:     /// It does not reallocate or shrink the `String`, so the leaked allocation may include unused\n  2187:     /// capacity that is not part of the returned slice. If you want to discard excess capacity,\n  2188:     /// call [`into_boxed_str`], and then [`Box::leak`] instead. However, keep in mind that\n  2189:     /// trimming the capacity may result in a reallocation and copy.\n  2190:     ///",
    "nanvix_source": "  2169:     ///\n  2170:     /// ```\n  2171:     /// let s = String::from(\"hello\");\n  2172:     ///\n  2173:     /// let b = s.into_boxed_str();\n  2174:     /// ```\n  2175:     #[cfg(not(no_global_oom_handling))]\n  2176:     #[stable(feature = \"box_str\", since = \"1.4.0\")]\n  2177:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2178:     #[inline]\n  2179:     pub fn into_boxed_str(self) -> Box<str> {\n  2180:         let slice = self.vec.into_boxed_slice();\n  2181:         unsafe { from_boxed_utf8_unchecked(slice) }\n  2182:     }\n  2183: \n  2184:     /// Consumes and leaks the `String`, returning a mutable reference to the contents,\n  2185:     /// `&'a mut str`.\n  2186:     ///\n  2187:     /// The caller has free choice over the returned lifetime, including `'static`. Indeed,\n  2188:     /// this function is ideally used for data that lives for the remainder of the program's life,\n  2189:     /// as dropping the returned reference will cause a memory leak.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::as_pin_ref",
    "generation_group": "complex_result_or_pattern_model",
    "classification": "complex_result_or_pattern_model",
    "classification_reasons": [
      "result_type_or_pattern_semantics_need_additional_model"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_pin_ref",
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
                              "generic": "Self"
                            }
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 9981,
                "path": "Pin"
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
                        "id": 9981,
                        "path": "Pin"
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
    "verification_source": "   764:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   765:     #[rustc_const_stable(feature = \"const_option\", since = \"1.83.0\")]\n   766:     pub const fn as_mut(&mut self) -> Option<&mut T> {\n   767:         match *self {\n   768:             Some(ref mut x) => Some(x),\n   769:             None => None,\n   770:         }\n   771:     }\n   772: \n   773:     /// Converts from <code>[Pin]<[&]Option\\<T>></code> to <code>Option<[Pin]<[&]T>></code>.\n   774:     ///\n   775:     /// [&]: reference \"shared reference\"\n   776:     #[inline]\n   777:     #[must_use]\n   778:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   779:     #[rustc_const_stable(feature = \"const_option_ext\", since = \"1.84.0\")]\n   780:     pub const fn as_pin_ref(self: Pin<&Self>) -> Option<Pin<&T>> {\n   781:         // FIXME(const-hack): use `map` once that is possible\n   782:         match Pin::get_ref(self).as_ref() {\n   783:             // SAFETY: `x` is guaranteed to be pinned because it comes from `self`\n   784:             // which is pinned.\n   785:             Some(x) => unsafe { Some(Pin::new_unchecked(x)) },\n   786:             None => None,\n   787:         }\n   788:     }\n   789: \n   790:     /// Converts from <code>[Pin]<[&mut] Option\\<T>></code> to <code>Option<[Pin]<[&mut] T>></code>.\n   791:     ///\n   792:     /// [&mut]: reference \"mutable reference\"\n   793:     #[inline]\n   794:     #[must_use]\n   795:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   796:     #[rustc_const_stable(feature = \"const_option_ext\", since = \"1.84.0\")]",
    "nanvix_source": "   768:         }\n   769:     }\n   770: \n   771:     /// Converts from <code>[Pin]<[&]Option\\<T>></code> to <code>Option<[Pin]<[&]T>></code>.\n   772:     ///\n   773:     /// [&]: reference \"shared reference\"\n   774:     #[inline]\n   775:     #[must_use]\n   776:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   777:     #[rustc_const_stable(feature = \"const_option_ext\", since = \"1.84.0\")]\n   778:     pub const fn as_pin_ref(self: Pin<&Self>) -> Option<Pin<&T>> {\n   779:         // FIXME(const-hack): use `map` once that is possible\n   780:         match Pin::get_ref(self).as_ref() {\n   781:             // SAFETY: `x` is guaranteed to be pinned because it comes from `self`\n   782:             // which is pinned.\n   783:             Some(x) => unsafe { Some(Pin::new_unchecked(x)) },\n   784:             None => None,\n   785:         }\n   786:     }\n   787: \n   788:     /// Converts from <code>[Pin]<[&mut] Option\\<T>></code> to <code>Option<[Pin]<[&mut] T>></code>.",
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
