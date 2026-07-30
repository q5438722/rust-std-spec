For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::encode_utf16",
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
      "name": "encode_utf16",
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
            "id": 10144,
            "path": "EncodeUtf16"
          }
        }
      }
    },
    "verification_source": "  1322:     /// Returns an iterator of `u16` over the string encoded\n  1323:     /// as native endian UTF-16 (without byte-order mark).\n  1324:     ///\n  1325:     /// # Examples\n  1326:     ///\n  1327:     /// ```\n  1328:     /// let text = \"Za\u017c\u00f3\u0142\u0107 g\u0119\u015bl\u0105 ja\u017a\u0144\";\n  1329:     ///\n  1330:     /// let utf8_len = text.len();\n  1331:     /// let utf16_len = text.encode_utf16().count();\n  1332:     ///\n  1333:     /// assert!(utf16_len <= utf8_len);\n  1334:     /// ```\n  1335:     #[must_use = \"this returns the encoded string as an iterator, \\\n  1336:                   without modifying the original\"]\n  1337:     #[stable(feature = \"encode_utf16\", since = \"1.8.0\")]\n  1338:     pub fn encode_utf16(&self) -> EncodeUtf16<'_> {\n  1339:         EncodeUtf16 { chars: self.chars(), extra: 0 }\n  1340:     }\n  1341: \n  1342:     /// Returns `true` if the given pattern matches a sub-slice of\n  1343:     /// this string slice.\n  1344:     ///\n  1345:     /// Returns `false` if it does not.\n  1346:     ///\n  1347:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1348:     /// function or closure that determines if a character matches.\n  1349:     ///\n  1350:     /// [`char`]: prim@char\n  1351:     /// [pattern]: self::pattern\n  1352:     ///\n  1353:     /// # Examples\n  1354:     ///",
    "nanvix_source": "  1347:     /// let text = \"Za\u017c\u00f3\u0142\u0107 g\u0119\u015bl\u0105 ja\u017a\u0144\";\n  1348:     ///\n  1349:     /// let utf8_len = text.len();\n  1350:     /// let utf16_len = text.encode_utf16().count();\n  1351:     ///\n  1352:     /// assert!(utf16_len <= utf8_len);\n  1353:     /// ```\n  1354:     #[must_use = \"this returns the encoded string as an iterator, \\\n  1355:                   without modifying the original\"]\n  1356:     #[stable(feature = \"encode_utf16\", since = \"1.8.0\")]\n  1357:     pub fn encode_utf16(&self) -> EncodeUtf16<'_> {\n  1358:         EncodeUtf16 { chars: self.chars(), extra: 0 }\n  1359:     }\n  1360: \n  1361:     /// Returns `true` if the given pattern matches a sub-slice of\n  1362:     /// this string slice.\n  1363:     ///\n  1364:     /// Returns `false` if it does not.\n  1365:     ///\n  1366:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1367:     /// function or closure that determines if a character matches.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::escape_debug",
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
      "name": "escape_debug",
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
            "id": 10147,
            "path": "EscapeDebug"
          }
        }
      }
    },
    "verification_source": "  2993:     ///\n  2994:     ///\n  2995:     /// Both are equivalent to:\n  2996:     ///\n  2997:     /// ```\n  2998:     /// println!(\"\u2764\\\\n!\");\n  2999:     /// ```\n  3000:     ///\n  3001:     /// Using `to_string`:\n  3002:     ///\n  3003:     /// ```\n  3004:     /// assert_eq!(\"\u2764\\n!\".escape_debug().to_string(), \"\u2764\\\\n!\");\n  3005:     /// ```\n  3006:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3007:                   without modifying the original\"]\n  3008:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3009:     pub fn escape_debug(&self) -> EscapeDebug<'_> {\n  3010:         let mut chars = self.chars();\n  3011:         EscapeDebug {\n  3012:             inner: chars\n  3013:                 .next()\n  3014:                 .map(|first| first.escape_debug_ext(EscapeDebugExtArgs::ESCAPE_ALL))\n  3015:                 .into_iter()\n  3016:                 .flatten()\n  3017:                 .chain(chars.flat_map(CharEscapeDebugContinue)),\n  3018:         }\n  3019:     }\n  3020: \n  3021:     /// Returns an iterator that escapes each char in `self` with [`char::escape_default`].\n  3022:     ///\n  3023:     /// # Examples\n  3024:     ///\n  3025:     /// As an iterator:",
    "nanvix_source": "  3084:     /// ```\n  3085:     ///\n  3086:     /// Using `to_string`:\n  3087:     ///\n  3088:     /// ```\n  3089:     /// assert_eq!(\"\u2764\\n!\".escape_debug().to_string(), \"\u2764\\\\n!\");\n  3090:     /// ```\n  3091:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3092:                   without modifying the original\"]\n  3093:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3094:     pub fn escape_debug(&self) -> EscapeDebug<'_> {\n  3095:         let mut chars = self.chars();\n  3096:         EscapeDebug {\n  3097:             inner: chars\n  3098:                 .next()\n  3099:                 .map(|first| first.escape_debug_ext(EscapeDebugExtArgs::ESCAPE_ALL))\n  3100:                 .into_iter()\n  3101:                 .flatten()\n  3102:                 .chain(chars.flat_map(CharEscapeDebugContinue)),\n  3103:         }\n  3104:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::escape_default",
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
      "name": "escape_default",
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
            "id": 10150,
            "path": "EscapeDefault"
          }
        }
      }
    },
    "verification_source": "  3039:     ///\n  3040:     ///\n  3041:     /// Both are equivalent to:\n  3042:     ///\n  3043:     /// ```\n  3044:     /// println!(\"\\\\u{{2764}}\\\\n!\");\n  3045:     /// ```\n  3046:     ///\n  3047:     /// Using `to_string`:\n  3048:     ///\n  3049:     /// ```\n  3050:     /// assert_eq!(\"\u2764\\n!\".escape_default().to_string(), \"\\\\u{2764}\\\\n!\");\n  3051:     /// ```\n  3052:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3053:                   without modifying the original\"]\n  3054:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3055:     pub fn escape_default(&self) -> EscapeDefault<'_> {\n  3056:         EscapeDefault { inner: self.chars().flat_map(CharEscapeDefault) }\n  3057:     }\n  3058: \n  3059:     /// Returns an iterator that escapes each char in `self` with [`char::escape_unicode`].\n  3060:     ///\n  3061:     /// # Examples\n  3062:     ///\n  3063:     /// As an iterator:\n  3064:     ///\n  3065:     /// ```\n  3066:     /// for c in \"\u2764\\n!\".escape_unicode() {\n  3067:     ///     print!(\"{c}\");\n  3068:     /// }\n  3069:     /// println!();\n  3070:     /// ```\n  3071:     ///",
    "nanvix_source": "  3130:     /// ```\n  3131:     ///\n  3132:     /// Using `to_string`:\n  3133:     ///\n  3134:     /// ```\n  3135:     /// assert_eq!(\"\u2764\\n!\".escape_default().to_string(), \"\\\\u{2764}\\\\n!\");\n  3136:     /// ```\n  3137:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3138:                   without modifying the original\"]\n  3139:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3140:     pub fn escape_default(&self) -> EscapeDefault<'_> {\n  3141:         EscapeDefault { inner: self.chars().flat_map(CharEscapeDefault) }\n  3142:     }\n  3143: \n  3144:     /// Returns an iterator that escapes each char in `self` with [`char::escape_unicode`].\n  3145:     ///\n  3146:     /// # Examples\n  3147:     ///\n  3148:     /// As an iterator:\n  3149:     ///\n  3150:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::escape_unicode",
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
      "name": "escape_unicode",
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
            "id": 10153,
            "path": "EscapeUnicode"
          }
        }
      }
    },
    "verification_source": "  3077:     ///\n  3078:     ///\n  3079:     /// Both are equivalent to:\n  3080:     ///\n  3081:     /// ```\n  3082:     /// println!(\"\\\\u{{2764}}\\\\u{{a}}\\\\u{{21}}\");\n  3083:     /// ```\n  3084:     ///\n  3085:     /// Using `to_string`:\n  3086:     ///\n  3087:     /// ```\n  3088:     /// assert_eq!(\"\u2764\\n!\".escape_unicode().to_string(), \"\\\\u{2764}\\\\u{a}\\\\u{21}\");\n  3089:     /// ```\n  3090:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3091:                   without modifying the original\"]\n  3092:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3093:     pub fn escape_unicode(&self) -> EscapeUnicode<'_> {\n  3094:         EscapeUnicode { inner: self.chars().flat_map(CharEscapeUnicode) }\n  3095:     }\n  3096: \n  3097:     /// Returns the range that a substring points to.\n  3098:     ///\n  3099:     /// Returns `None` if `substr` does not point within `self`.\n  3100:     ///\n  3101:     /// Unlike [`str::find`], **this does not search through the string**.\n  3102:     /// Instead, it uses pointer arithmetic to find where in the string\n  3103:     /// `substr` is derived from.\n  3104:     ///\n  3105:     /// This is useful for extending [`str::split`] and similar methods.\n  3106:     ///\n  3107:     /// Note that this method may return false positives (typically either\n  3108:     /// `Some(0..0)` or `Some(self.len()..self.len())`) if `substr` is a\n  3109:     /// zero-length `str` that points at the beginning or end of another,",
    "nanvix_source": "  3168:     /// ```\n  3169:     ///\n  3170:     /// Using `to_string`:\n  3171:     ///\n  3172:     /// ```\n  3173:     /// assert_eq!(\"\u2764\\n!\".escape_unicode().to_string(), \"\\\\u{2764}\\\\u{a}\\\\u{21}\");\n  3174:     /// ```\n  3175:     #[must_use = \"this returns the escaped string as an iterator, \\\n  3176:                   without modifying the original\"]\n  3177:     #[stable(feature = \"str_escape\", since = \"1.34.0\")]\n  3178:     pub fn escape_unicode(&self) -> EscapeUnicode<'_> {\n  3179:         EscapeUnicode { inner: self.chars().flat_map(CharEscapeUnicode) }\n  3180:     }\n  3181: \n  3182:     /// Returns the range that a substring points to.\n  3183:     ///\n  3184:     /// Returns `None` if `substr` does not point within `self`.\n  3185:     ///\n  3186:     /// Unlike [`str::find`], **this does not search through the string**.\n  3187:     /// Instead, it uses pointer arithmetic to find where in the string\n  3188:     /// `substr` is derived from.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::lines",
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
            "id": 10129,
            "path": "Lines"
          }
        }
      }
    },
    "verification_source": "  1293:     /// assert_eq!(Some(\"\"), lines.next());\n  1294:     /// assert_eq!(Some(\"baz\"), lines.next());\n  1295:     ///\n  1296:     /// assert_eq!(None, lines.next());\n  1297:     /// ```\n  1298:     ///\n  1299:     /// An empty string returns an empty iterator:\n  1300:     ///\n  1301:     /// ```\n  1302:     /// let text = \"\";\n  1303:     /// let mut lines = text.lines();\n  1304:     ///\n  1305:     /// assert_eq!(lines.next(), None);\n  1306:     /// ```\n  1307:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1308:     #[inline]\n  1309:     pub fn lines(&self) -> Lines<'_> {\n  1310:         Lines(self.split_inclusive('\\n').map(LinesMap))\n  1311:     }\n  1312: \n  1313:     /// Returns an iterator over the lines of a string.\n  1314:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1315:     #[deprecated(since = \"1.4.0\", note = \"use lines() instead now\", suggestion = \"lines\")]\n  1316:     #[inline]\n  1317:     #[allow(deprecated)]\n  1318:     pub fn lines_any(&self) -> LinesAny<'_> {\n  1319:         LinesAny(self.lines())\n  1320:     }\n  1321: \n  1322:     /// Returns an iterator of `u16` over the string encoded\n  1323:     /// as native endian UTF-16 (without byte-order mark).\n  1324:     ///\n  1325:     /// # Examples",
    "nanvix_source": "  1318:     /// An empty string returns an empty iterator:\n  1319:     ///\n  1320:     /// ```\n  1321:     /// let text = \"\";\n  1322:     /// let mut lines = text.lines();\n  1323:     ///\n  1324:     /// assert_eq!(lines.next(), None);\n  1325:     /// ```\n  1326:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1327:     #[inline]\n  1328:     pub fn lines(&self) -> Lines<'_> {\n  1329:         Lines(self.split_inclusive('\\n').map(LinesMap))\n  1330:     }\n  1331: \n  1332:     /// Returns an iterator over the lines of a string.\n  1333:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1334:     #[deprecated(since = \"1.4.0\", note = \"use lines() instead now\", suggestion = \"lines\")]\n  1335:     #[inline]\n  1336:     #[allow(deprecated)]\n  1337:     pub fn lines_any(&self) -> LinesAny<'_> {\n  1338:         LinesAny(self.lines())",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::lines_any",
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
      "name": "lines_any",
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
            "id": 10132,
            "path": "LinesAny"
          }
        }
      }
    },
    "verification_source": "  1302:     /// let text = \"\";\n  1303:     /// let mut lines = text.lines();\n  1304:     ///\n  1305:     /// assert_eq!(lines.next(), None);\n  1306:     /// ```\n  1307:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1308:     #[inline]\n  1309:     pub fn lines(&self) -> Lines<'_> {\n  1310:         Lines(self.split_inclusive('\\n').map(LinesMap))\n  1311:     }\n  1312: \n  1313:     /// Returns an iterator over the lines of a string.\n  1314:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1315:     #[deprecated(since = \"1.4.0\", note = \"use lines() instead now\", suggestion = \"lines\")]\n  1316:     #[inline]\n  1317:     #[allow(deprecated)]\n  1318:     pub fn lines_any(&self) -> LinesAny<'_> {\n  1319:         LinesAny(self.lines())\n  1320:     }\n  1321: \n  1322:     /// Returns an iterator of `u16` over the string encoded\n  1323:     /// as native endian UTF-16 (without byte-order mark).\n  1324:     ///\n  1325:     /// # Examples\n  1326:     ///\n  1327:     /// ```\n  1328:     /// let text = \"Za\u017c\u00f3\u0142\u0107 g\u0119\u015bl\u0105 ja\u017a\u0144\";\n  1329:     ///\n  1330:     /// let utf8_len = text.len();\n  1331:     /// let utf16_len = text.encode_utf16().count();\n  1332:     ///\n  1333:     /// assert!(utf16_len <= utf8_len);\n  1334:     /// ```",
    "nanvix_source": "  1327:     #[inline]\n  1328:     pub fn lines(&self) -> Lines<'_> {\n  1329:         Lines(self.split_inclusive('\\n').map(LinesMap))\n  1330:     }\n  1331: \n  1332:     /// Returns an iterator over the lines of a string.\n  1333:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1334:     #[deprecated(since = \"1.4.0\", note = \"use lines() instead now\", suggestion = \"lines\")]\n  1335:     #[inline]\n  1336:     #[allow(deprecated)]\n  1337:     pub fn lines_any(&self) -> LinesAny<'_> {\n  1338:         LinesAny(self.lines())\n  1339:     }\n  1340: \n  1341:     /// Returns an iterator of `u16` over the string encoded\n  1342:     /// as native endian UTF-16 (without byte-order mark).\n  1343:     ///\n  1344:     /// # Examples\n  1345:     ///\n  1346:     /// ```\n  1347:     /// let text = \"Za\u017c\u00f3\u0142\u0107 g\u0119\u015bl\u0105 ja\u017a\u0144\";",
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
