For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::match_indices",
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
      "name": "match_indices",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10118,
            "path": "MatchIndices"
          }
        }
      }
    },
    "verification_source": "  2087:     /// [`rmatch_indices`]: str::rmatch_indices\n  2088:     ///\n  2089:     /// # Examples\n  2090:     ///\n  2091:     /// ```\n  2092:     /// let v: Vec<_> = \"abcXXXabcYYYabc\".match_indices(\"abc\").collect();\n  2093:     /// assert_eq!(v, [(0, \"abc\"), (6, \"abc\"), (12, \"abc\")]);\n  2094:     ///\n  2095:     /// let v: Vec<_> = \"1abcabc2\".match_indices(\"abc\").collect();\n  2096:     /// assert_eq!(v, [(1, \"abc\"), (4, \"abc\")]);\n  2097:     ///\n  2098:     /// let v: Vec<_> = \"ababa\".match_indices(\"aba\").collect();\n  2099:     /// assert_eq!(v, [(0, \"aba\")]); // only the first `aba`\n  2100:     /// ```\n  2101:     #[stable(feature = \"str_match_indices\", since = \"1.5.0\")]\n  2102:     #[inline]\n  2103:     pub fn match_indices<P: Pattern>(&self, pat: P) -> MatchIndices<'_, P> {\n  2104:         MatchIndices(MatchIndicesInternal(pat.into_searcher(self)))\n  2105:     }\n  2106: \n  2107:     /// Returns an iterator over the disjoint matches of a pattern within `self`,\n  2108:     /// yielded in reverse order along with the index of the match.\n  2109:     ///\n  2110:     /// For matches of `pat` within `self` that overlap, only the indices\n  2111:     /// corresponding to the last match are returned.\n  2112:     ///\n  2113:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2114:     /// function or closure that determines if a character matches.\n  2115:     ///\n  2116:     /// [`char`]: prim@char\n  2117:     /// [pattern]: self::pattern\n  2118:     ///\n  2119:     /// # Iterator behavior",
    "nanvix_source": "  2112:     /// assert_eq!(v, [(0, \"abc\"), (6, \"abc\"), (12, \"abc\")]);\n  2113:     ///\n  2114:     /// let v: Vec<_> = \"1abcabc2\".match_indices(\"abc\").collect();\n  2115:     /// assert_eq!(v, [(1, \"abc\"), (4, \"abc\")]);\n  2116:     ///\n  2117:     /// let v: Vec<_> = \"ababa\".match_indices(\"aba\").collect();\n  2118:     /// assert_eq!(v, [(0, \"aba\")]); // only the first `aba`\n  2119:     /// ```\n  2120:     #[stable(feature = \"str_match_indices\", since = \"1.5.0\")]\n  2121:     #[inline]\n  2122:     pub fn match_indices<P: Pattern>(&self, pat: P) -> MatchIndices<'_, P> {\n  2123:         MatchIndices(MatchIndicesInternal(pat.into_searcher(self)))\n  2124:     }\n  2125: \n  2126:     /// Returns an iterator over the disjoint matches of a pattern within `self`,\n  2127:     /// yielded in reverse order along with the index of the match.\n  2128:     ///\n  2129:     /// For matches of `pat` within `self` that overlap, only the indices\n  2130:     /// corresponding to the last match are returned.\n  2131:     ///\n  2132:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::matches",
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
      "name": "matches",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10124,
            "path": "Matches"
          }
        }
      }
    },
    "verification_source": "  2009:     /// If the pattern allows a reverse search but its results might differ\n  2010:     /// from a forward search, the [`rmatches`] method can be used.\n  2011:     ///\n  2012:     /// [`rmatches`]: str::rmatches\n  2013:     ///\n  2014:     /// # Examples\n  2015:     ///\n  2016:     /// ```\n  2017:     /// let v: Vec<&str> = \"abcXXXabcYYYabc\".matches(\"abc\").collect();\n  2018:     /// assert_eq!(v, [\"abc\", \"abc\", \"abc\"]);\n  2019:     ///\n  2020:     /// let v: Vec<&str> = \"1abc2abc3\".matches(char::is_numeric).collect();\n  2021:     /// assert_eq!(v, [\"1\", \"2\", \"3\"]);\n  2022:     /// ```\n  2023:     #[stable(feature = \"str_matches\", since = \"1.2.0\")]\n  2024:     #[inline]\n  2025:     pub fn matches<P: Pattern>(&self, pat: P) -> Matches<'_, P> {\n  2026:         Matches(MatchesInternal(pat.into_searcher(self)))\n  2027:     }\n  2028: \n  2029:     /// Returns an iterator over the disjoint matches of a pattern within this\n  2030:     /// string slice, yielded in reverse order.\n  2031:     ///\n  2032:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2033:     /// function or closure that determines if a character matches.\n  2034:     ///\n  2035:     /// [`char`]: prim@char\n  2036:     /// [pattern]: self::pattern\n  2037:     ///\n  2038:     /// # Iterator behavior\n  2039:     ///\n  2040:     /// The returned iterator requires that the pattern supports a reverse\n  2041:     /// search, and it will be a [`DoubleEndedIterator`] if a forward/reverse",
    "nanvix_source": "  2034:     ///\n  2035:     /// ```\n  2036:     /// let v: Vec<&str> = \"abcXXXabcYYYabc\".matches(\"abc\").collect();\n  2037:     /// assert_eq!(v, [\"abc\", \"abc\", \"abc\"]);\n  2038:     ///\n  2039:     /// let v: Vec<&str> = \"1abc2abc3\".matches(char::is_numeric).collect();\n  2040:     /// assert_eq!(v, [\"1\", \"2\", \"3\"]);\n  2041:     /// ```\n  2042:     #[stable(feature = \"str_matches\", since = \"1.2.0\")]\n  2043:     #[inline]\n  2044:     pub fn matches<P: Pattern>(&self, pat: P) -> Matches<'_, P> {\n  2045:         Matches(MatchesInternal(pat.into_searcher(self)))\n  2046:     }\n  2047: \n  2048:     /// Returns an iterator over the disjoint matches of a pattern within this\n  2049:     /// string slice, yielded in reverse order.\n  2050:     ///\n  2051:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2052:     /// function or closure that determines if a character matches.\n  2053:     ///\n  2054:     /// [`char`]: prim@char",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10100,
            "path": "Split"
          }
        }
      }
    },
    "verification_source": "  1635:     /// let d: Vec<_> = x.split(' ').collect();\n  1636:     ///\n  1637:     /// assert_eq!(d, &[\"\", \"\", \"\", \"\", \"a\", \"\", \"b\", \"c\"]);\n  1638:     /// ```\n  1639:     ///\n  1640:     /// It does _not_ give you:\n  1641:     ///\n  1642:     /// ```,ignore\n  1643:     /// assert_eq!(d, &[\"a\", \"b\", \"c\"]);\n  1644:     /// ```\n  1645:     ///\n  1646:     /// Use [`split_whitespace`] for this behavior.\n  1647:     ///\n  1648:     /// [`split_whitespace`]: str::split_whitespace\n  1649:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1650:     #[inline]\n  1651:     pub fn split<P: Pattern>(&self, pat: P) -> Split<'_, P> {\n  1652:         Split(SplitInternal {\n  1653:             start: 0,\n  1654:             end: self.len(),\n  1655:             matcher: pat.into_searcher(self),\n  1656:             allow_trailing_empty: true,\n  1657:             finished: false,\n  1658:         })\n  1659:     }\n  1660: \n  1661:     /// Returns an iterator over substrings of this string slice, separated by\n  1662:     /// characters matched by a pattern.\n  1663:     ///\n  1664:     /// Differs from the iterator produced by `split` in that `split_inclusive`\n  1665:     /// leaves the matched part as the terminator of the substring.\n  1666:     ///\n  1667:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
    "nanvix_source": "  1660:     ///\n  1661:     /// ```,ignore\n  1662:     /// assert_eq!(d, &[\"a\", \"b\", \"c\"]);\n  1663:     /// ```\n  1664:     ///\n  1665:     /// Use [`split_whitespace`] for this behavior.\n  1666:     ///\n  1667:     /// [`split_whitespace`]: str::split_whitespace\n  1668:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1669:     #[inline]\n  1670:     pub fn split<P: Pattern>(&self, pat: P) -> Split<'_, P> {\n  1671:         Split(SplitInternal {\n  1672:             start: 0,\n  1673:             end: self.len(),\n  1674:             matcher: pat.into_searcher(self),\n  1675:             allow_trailing_empty: true,\n  1676:             finished: false,\n  1677:         })\n  1678:     }\n  1679: \n  1680:     /// Returns an iterator over substrings of this string slice, separated by",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_ascii_whitespace",
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
      "name": "split_ascii_whitespace",
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
            "id": 10138,
            "path": "SplitAsciiWhitespace"
          }
        }
      }
    },
    "verification_source": "  1229:     /// assert_eq!(Some(\"a\"), iter.next());\n  1230:     /// assert_eq!(Some(\"little\"), iter.next());\n  1231:     /// assert_eq!(Some(\"lamb\"), iter.next());\n  1232:     ///\n  1233:     /// assert_eq!(None, iter.next());\n  1234:     /// ```\n  1235:     ///\n  1236:     /// If the string is empty or all ASCII whitespace, the iterator yields no string slices:\n  1237:     /// ```\n  1238:     /// assert_eq!(\"\".split_ascii_whitespace().next(), None);\n  1239:     /// assert_eq!(\"   \".split_ascii_whitespace().next(), None);\n  1240:     /// ```\n  1241:     #[must_use = \"this returns the split string as an iterator, \\\n  1242:                   without modifying the original\"]\n  1243:     #[stable(feature = \"split_ascii_whitespace\", since = \"1.34.0\")]\n  1244:     #[inline]\n  1245:     pub fn split_ascii_whitespace(&self) -> SplitAsciiWhitespace<'_> {\n  1246:         let inner =\n  1247:             self.as_bytes().split(IsAsciiWhitespace).filter(BytesIsNotEmpty).map(UnsafeBytesToStr);\n  1248:         SplitAsciiWhitespace { inner }\n  1249:     }\n  1250: \n  1251:     /// Returns an iterator over the lines of a string, as string slices.\n  1252:     ///\n  1253:     /// Lines are split at line endings that are either newlines (`\\n`) or\n  1254:     /// sequences of a carriage return followed by a line feed (`\\r\\n`).\n  1255:     ///\n  1256:     /// Line terminators are not included in the lines returned by the iterator.\n  1257:     ///\n  1258:     /// Note that any carriage return (`\\r`) not immediately followed by a\n  1259:     /// line feed (`\\n`) does not split a line. These carriage returns are\n  1260:     /// thereby included in the produced lines.\n  1261:     ///",
    "nanvix_source": "  1254:     ///\n  1255:     /// If the string is empty or all ASCII whitespace, the iterator yields no string slices:\n  1256:     /// ```\n  1257:     /// assert_eq!(\"\".split_ascii_whitespace().next(), None);\n  1258:     /// assert_eq!(\"   \".split_ascii_whitespace().next(), None);\n  1259:     /// ```\n  1260:     #[must_use = \"this returns the split string as an iterator, \\\n  1261:                   without modifying the original\"]\n  1262:     #[stable(feature = \"split_ascii_whitespace\", since = \"1.34.0\")]\n  1263:     #[inline]\n  1264:     pub fn split_ascii_whitespace(&self) -> SplitAsciiWhitespace<'_> {\n  1265:         let inner =\n  1266:             self.as_bytes().split(IsAsciiWhitespace).filter(BytesIsNotEmpty).map(UnsafeBytesToStr);\n  1267:         SplitAsciiWhitespace { inner }\n  1268:     }\n  1269: \n  1270:     /// Returns an iterator over the lines of a string, as string slices.\n  1271:     ///\n  1272:     /// Lines are split at line endings that are either newlines (`\\n`) or\n  1273:     /// sequences of a carriage return followed by a line feed (`\\r\\n`).\n  1274:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_inclusive",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10142,
            "path": "SplitInclusive"
          }
        }
      }
    },
    "verification_source": "  1676:     /// let v: Vec<&str> = \"Mary had a little lamb\\nlittle lamb\\nlittle lamb.\"\n  1677:     ///     .split_inclusive('\\n').collect();\n  1678:     /// assert_eq!(v, [\"Mary had a little lamb\\n\", \"little lamb\\n\", \"little lamb.\"]);\n  1679:     /// ```\n  1680:     ///\n  1681:     /// If the last element of the string is matched,\n  1682:     /// that element will be considered the terminator of the preceding substring.\n  1683:     /// That substring will be the last item returned by the iterator.\n  1684:     ///\n  1685:     /// ```\n  1686:     /// let v: Vec<&str> = \"Mary had a little lamb\\nlittle lamb\\nlittle lamb.\\n\"\n  1687:     ///     .split_inclusive('\\n').collect();\n  1688:     /// assert_eq!(v, [\"Mary had a little lamb\\n\", \"little lamb\\n\", \"little lamb.\\n\"]);\n  1689:     /// ```\n  1690:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  1691:     #[inline]\n  1692:     pub fn split_inclusive<P: Pattern>(&self, pat: P) -> SplitInclusive<'_, P> {\n  1693:         SplitInclusive(SplitInternal {\n  1694:             start: 0,\n  1695:             end: self.len(),\n  1696:             matcher: pat.into_searcher(self),\n  1697:             allow_trailing_empty: false,\n  1698:             finished: false,\n  1699:         })\n  1700:     }\n  1701: \n  1702:     /// Returns an iterator over substrings of the given string slice, separated\n  1703:     /// by characters matched by a pattern and yielded in reverse order.\n  1704:     ///\n  1705:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1706:     /// function or closure that determines if a character matches.\n  1707:     ///\n  1708:     /// [`char`]: prim@char",
    "nanvix_source": "  1701:     /// that element will be considered the terminator of the preceding substring.\n  1702:     /// That substring will be the last item returned by the iterator.\n  1703:     ///\n  1704:     /// ```\n  1705:     /// let v: Vec<&str> = \"Mary had a little lamb\\nlittle lamb\\nlittle lamb.\\n\"\n  1706:     ///     .split_inclusive('\\n').collect();\n  1707:     /// assert_eq!(v, [\"Mary had a little lamb\\n\", \"little lamb\\n\", \"little lamb.\\n\"]);\n  1708:     /// ```\n  1709:     #[stable(feature = \"split_inclusive\", since = \"1.51.0\")]\n  1710:     #[inline]\n  1711:     pub fn split_inclusive<P: Pattern>(&self, pat: P) -> SplitInclusive<'_, P> {\n  1712:         SplitInclusive(SplitInternal {\n  1713:             start: 0,\n  1714:             end: self.len(),\n  1715:             matcher: pat.into_searcher(self),\n  1716:             allow_trailing_empty: false,\n  1717:             finished: false,\n  1718:         })\n  1719:     }\n  1720: \n  1721:     /// Returns an iterator over substrings of the given string slice, separated",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::split_terminator",
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
      "name": "split_terminator",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10106,
            "path": "SplitTerminator"
          }
        }
      }
    },
    "verification_source": "  1780:     /// [`rsplit_terminator`]: str::rsplit_terminator\n  1781:     ///\n  1782:     /// # Examples\n  1783:     ///\n  1784:     /// ```\n  1785:     /// let v: Vec<&str> = \"A.B.\".split_terminator('.').collect();\n  1786:     /// assert_eq!(v, [\"A\", \"B\"]);\n  1787:     ///\n  1788:     /// let v: Vec<&str> = \"A..B..\".split_terminator(\".\").collect();\n  1789:     /// assert_eq!(v, [\"A\", \"\", \"B\", \"\"]);\n  1790:     ///\n  1791:     /// let v: Vec<&str> = \"A.B:C.D\".split_terminator(&['.', ':'][..]).collect();\n  1792:     /// assert_eq!(v, [\"A\", \"B\", \"C\", \"D\"]);\n  1793:     /// ```\n  1794:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1795:     #[inline]\n  1796:     pub fn split_terminator<P: Pattern>(&self, pat: P) -> SplitTerminator<'_, P> {\n  1797:         SplitTerminator(SplitInternal { allow_trailing_empty: false, ..self.split(pat).0 })\n  1798:     }\n  1799: \n  1800:     /// Returns an iterator over substrings of `self`, separated by characters\n  1801:     /// matched by a pattern and yielded in reverse order.\n  1802:     ///\n  1803:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1804:     /// function or closure that determines if a character matches.\n  1805:     ///\n  1806:     /// [`char`]: prim@char\n  1807:     /// [pattern]: self::pattern\n  1808:     ///\n  1809:     /// Equivalent to [`split`], except that the trailing substring is\n  1810:     /// skipped if empty.\n  1811:     ///\n  1812:     /// [`split`]: str::split",
    "nanvix_source": "  1805:     /// assert_eq!(v, [\"A\", \"B\"]);\n  1806:     ///\n  1807:     /// let v: Vec<&str> = \"A..B..\".split_terminator(\".\").collect();\n  1808:     /// assert_eq!(v, [\"A\", \"\", \"B\", \"\"]);\n  1809:     ///\n  1810:     /// let v: Vec<&str> = \"A.B:C.D\".split_terminator(&['.', ':'][..]).collect();\n  1811:     /// assert_eq!(v, [\"A\", \"B\", \"C\", \"D\"]);\n  1812:     /// ```\n  1813:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1814:     #[inline]\n  1815:     pub fn split_terminator<P: Pattern>(&self, pat: P) -> SplitTerminator<'_, P> {\n  1816:         SplitTerminator(SplitInternal { allow_trailing_empty: false, ..self.split(pat).0 })\n  1817:     }\n  1818: \n  1819:     /// Returns an iterator over substrings of `self`, separated by characters\n  1820:     /// matched by a pattern and yielded in reverse order.\n  1821:     ///\n  1822:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1823:     /// function or closure that determines if a character matches.\n  1824:     ///\n  1825:     /// [`char`]: prim@char",
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
