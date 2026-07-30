For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::RChunksExact::remainder",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "remainder",
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
                    "lifetime": "'a"
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
            "id": 10074,
            "path": "RChunksExact"
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
        "impl_id": "core:31565",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10074",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "RChunksExact"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2672:     /// # Example\n  2673:     ///\n  2674:     /// ```\n  2675:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  2676:     /// let mut iter = slice.rchunks_exact(2);\n  2677:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2678:     /// assert_eq!(iter.next(), Some(&['e', 'm'][..]));\n  2679:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2680:     /// assert_eq!(iter.next(), Some(&['o', 'r'][..]));\n  2681:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2682:     /// assert_eq!(iter.next(), None);\n  2683:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2684:     /// ```\n  2685:     #[must_use]\n  2686:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2687:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  2688:     pub const fn remainder(&self) -> &'a [T] {\n  2689:         self.rem\n  2690:     }\n  2691: }\n  2692: \n  2693: // FIXME(#26925) Remove in favor of `#[derive(Clone)]`\n  2694: #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2695: impl<'a, T> Clone for RChunksExact<'a, T> {\n  2696:     fn clone(&self) -> RChunksExact<'a, T> {\n  2697:         RChunksExact { v: self.v, rem: self.rem, chunk_size: self.chunk_size }\n  2698:     }\n  2699: }\n  2700: \n  2701: #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2702: impl<'a, T> Iterator for RChunksExact<'a, T> {\n  2703:     type Item = &'a [T];\n  2704: ",
    "nanvix_source": "  2676:     /// assert_eq!(iter.next(), Some(&['e', 'm'][..]));\n  2677:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2678:     /// assert_eq!(iter.next(), Some(&['o', 'r'][..]));\n  2679:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2680:     /// assert_eq!(iter.next(), None);\n  2681:     /// assert_eq!(iter.remainder(), &['l'][..]);\n  2682:     /// ```\n  2683:     #[must_use]\n  2684:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2685:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  2686:     pub const fn remainder(&self) -> &'a [T] {\n  2687:         self.rem\n  2688:     }\n  2689: }\n  2690: \n  2691: // FIXME(#26925) Remove in favor of `#[derive(Clone)]`\n  2692: #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2693: impl<'a, T> Clone for RChunksExact<'a, T> {\n  2694:     fn clone(&self) -> RChunksExact<'a, T> {\n  2695:         RChunksExact { v: self.v, rem: self.rem, chunk_size: self.chunk_size }\n  2696:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::CharIndices::as_str",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_str",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10092,
            "path": "CharIndices"
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
        "impl_id": "core:31737",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10092",
        "resolved_owner_path": [
          "core",
          "str",
          "iter",
          "CharIndices"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   218:             (index, ch)\n   219:         })\n   220:     }\n   221: }\n   222: \n   223: #[stable(feature = \"fused\", since = \"1.26.0\")]\n   224: impl FusedIterator for CharIndices<'_> {}\n   225: \n   226: impl<'a> CharIndices<'a> {\n   227:     /// Views the underlying data as a subslice of the original data.\n   228:     ///\n   229:     /// This has the same lifetime as the original slice, and so the\n   230:     /// iterator can continue to be used while this exists.\n   231:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   232:     #[must_use]\n   233:     #[inline]\n   234:     pub fn as_str(&self) -> &'a str {\n   235:         self.iter.as_str()\n   236:     }\n   237: \n   238:     /// Returns the byte position of the next character, or the length\n   239:     /// of the underlying string if there are no more characters.\n   240:     ///\n   241:     /// This means that, when the iterator has not been fully consumed,\n   242:     /// the returned value will match the index that will be returned\n   243:     /// by the next call to [`next()`](Self::next).\n   244:     ///\n   245:     /// # Examples\n   246:     ///\n   247:     /// ```\n   248:     /// let mut chars = \"a\u697d\".char_indices();\n   249:     ///\n   250:     /// // `next()` has not been called yet, so `offset()` returns the byte",
    "nanvix_source": "   224: impl FusedIterator for CharIndices<'_> {}\n   225: \n   226: impl<'a> CharIndices<'a> {\n   227:     /// Views the underlying data as a subslice of the original data.\n   228:     ///\n   229:     /// This has the same lifetime as the original slice, and so the\n   230:     /// iterator can continue to be used while this exists.\n   231:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   232:     #[must_use]\n   233:     #[inline]\n   234:     pub fn as_str(&self) -> &'a str {\n   235:         self.iter.as_str()\n   236:     }\n   237: \n   238:     /// Returns the byte position of the next character, or the length\n   239:     /// of the underlying string if there are no more characters.\n   240:     ///\n   241:     /// This means that, when the iterator has not been fully consumed,\n   242:     /// the returned value will match the index that will be returned\n   243:     /// by the next call to [`next()`](Self::next).\n   244:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::CharIndices::offset",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "offset",
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
            "id": 10092,
            "path": "CharIndices"
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
        "impl_id": "core:31737",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10092",
        "resolved_owner_path": [
          "core",
          "str",
          "iter",
          "CharIndices"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   254:     /// assert_eq!(chars.next(), Some((0, 'a')));\n   255:     ///\n   256:     /// // `next()` has been called once, so `offset()` returns the byte index\n   257:     /// // of the second character ...\n   258:     /// assert_eq!(chars.offset(), 1);\n   259:     /// // ... which matches the index returned by the next call to `next()`.\n   260:     /// assert_eq!(chars.next(), Some((1, '\u697d')));\n   261:     ///\n   262:     /// // Once the iterator has been consumed, `offset()` returns the length\n   263:     /// // in bytes of the string.\n   264:     /// assert_eq!(chars.offset(), 4);\n   265:     /// assert_eq!(chars.next(), None);\n   266:     /// ```\n   267:     #[inline]\n   268:     #[must_use]\n   269:     #[stable(feature = \"char_indices_offset\", since = \"1.82.0\")]\n   270:     pub fn offset(&self) -> usize {\n   271:         self.front_offset\n   272:     }\n   273: }\n   274: \n   275: /// An iterator over the bytes of a string slice.\n   276: ///\n   277: /// This struct is created by the [`bytes`] method on [`str`].\n   278: /// See its documentation for more.\n   279: ///\n   280: /// [`bytes`]: str::bytes\n   281: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n   282: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   283: #[derive(Clone, Debug)]\n   284: pub struct Bytes<'a>(pub(super) Copied<slice::Iter<'a, u8>>);\n   285: \n   286: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   260:     /// assert_eq!(chars.next(), Some((1, '\u697d')));\n   261:     ///\n   262:     /// // Once the iterator has been consumed, `offset()` returns the length\n   263:     /// // in bytes of the string.\n   264:     /// assert_eq!(chars.offset(), 4);\n   265:     /// assert_eq!(chars.next(), None);\n   266:     /// ```\n   267:     #[inline]\n   268:     #[must_use]\n   269:     #[stable(feature = \"char_indices_offset\", since = \"1.82.0\")]\n   270:     pub fn offset(&self) -> usize {\n   271:         self.front_offset\n   272:     }\n   273: }\n   274: \n   275: /// An iterator over the bytes of a string slice.\n   276: ///\n   277: /// This struct is created by the [`bytes`] method on [`str`].\n   278: /// See its documentation for more.\n   279: ///\n   280: /// [`bytes`]: str::bytes",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::Chars::as_str",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_str",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10089,
            "path": "Chars"
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
        "impl_id": "core:31722",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10089",
        "resolved_owner_path": [
          "core",
          "str",
          "iter",
          "Chars"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   140:     ///\n   141:     /// # Examples\n   142:     ///\n   143:     /// ```\n   144:     /// let mut chars = \"abc\".chars();\n   145:     ///\n   146:     /// assert_eq!(chars.as_str(), \"abc\");\n   147:     /// chars.next();\n   148:     /// assert_eq!(chars.as_str(), \"bc\");\n   149:     /// chars.next();\n   150:     /// chars.next();\n   151:     /// assert_eq!(chars.as_str(), \"\");\n   152:     /// ```\n   153:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   154:     #[must_use]\n   155:     #[inline]\n   156:     pub fn as_str(&self) -> &'a str {\n   157:         // SAFETY: `Chars` is only made from a str, which guarantees the iter is valid UTF-8.\n   158:         unsafe { from_utf8_unchecked(self.iter.as_slice()) }\n   159:     }\n   160: }\n   161: \n   162: /// An iterator over the [`char`]s of a string slice, and their positions.\n   163: ///\n   164: /// This struct is created by the [`char_indices`] method on [`str`].\n   165: /// See its documentation for more.\n   166: ///\n   167: /// [`char`]: prim@char\n   168: /// [`char_indices`]: str::char_indices\n   169: #[derive(Clone, Debug)]\n   170: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n   171: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   172: pub struct CharIndices<'a> {",
    "nanvix_source": "   146:     /// assert_eq!(chars.as_str(), \"abc\");\n   147:     /// chars.next();\n   148:     /// assert_eq!(chars.as_str(), \"bc\");\n   149:     /// chars.next();\n   150:     /// chars.next();\n   151:     /// assert_eq!(chars.as_str(), \"\");\n   152:     /// ```\n   153:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   154:     #[must_use]\n   155:     #[inline]\n   156:     pub fn as_str(&self) -> &'a str {\n   157:         // SAFETY: `Chars` is only made from a str, which guarantees the iter is valid UTF-8.\n   158:         unsafe { from_utf8_unchecked(self.iter.as_slice()) }\n   159:     }\n   160: }\n   161: \n   162: /// An iterator over the [`char`]s of a string slice, and their positions.\n   163: ///\n   164: /// This struct is created by the [`char_indices`] method on [`str`].\n   165: /// See its documentation for more.\n   166: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::Utf8Chunk::invalid",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "invalid",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10180,
            "path": "Utf8Chunk"
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
        "impl_id": "core:32271",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10180",
        "resolved_owner_path": [
          "core",
          "str",
          "lossy",
          "Utf8Chunk"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "    88:     /// Returns the invalid sequence that caused a failure.\n    89:     ///\n    90:     /// The returned slice will have a maximum length of 3 and starts after the\n    91:     /// substring given by [`valid`]. Decoding will resume after this sequence.\n    92:     ///\n    93:     /// If empty, this is the last chunk in the string. If non-empty, an\n    94:     /// unexpected byte was encountered or the end of the input was reached\n    95:     /// unexpectedly.\n    96:     ///\n    97:     /// Lossy decoding would replace this sequence with [`U+FFFD REPLACEMENT\n    98:     /// CHARACTER`].\n    99:     ///\n   100:     /// [`valid`]: Self::valid\n   101:     /// [`U+FFFD REPLACEMENT CHARACTER`]: crate::char::REPLACEMENT_CHARACTER\n   102:     #[must_use]\n   103:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n   104:     pub fn invalid(&self) -> &'a [u8] {\n   105:         self.invalid\n   106:     }\n   107: }\n   108: \n   109: #[must_use]\n   110: #[unstable(feature = \"str_internals\", issue = \"none\")]\n   111: pub struct Debug<'a>(&'a [u8]);\n   112: \n   113: #[unstable(feature = \"str_internals\", issue = \"none\")]\n   114: impl fmt::Debug for Debug<'_> {\n   115:     fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {\n   116:         f.write_char('\"')?;\n   117: \n   118:         for chunk in self.0.utf8_chunks() {\n   119:             // Valid part.\n   120:             // Here we partially parse UTF-8 again which is suboptimal.",
    "nanvix_source": "    94:     /// unexpected byte was encountered or the end of the input was reached\n    95:     /// unexpectedly.\n    96:     ///\n    97:     /// Lossy decoding would replace this sequence with [`U+FFFD REPLACEMENT\n    98:     /// CHARACTER`].\n    99:     ///\n   100:     /// [`valid`]: Self::valid\n   101:     /// [`U+FFFD REPLACEMENT CHARACTER`]: crate::char::REPLACEMENT_CHARACTER\n   102:     #[must_use]\n   103:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n   104:     pub fn invalid(&self) -> &'a [u8] {\n   105:         self.invalid\n   106:     }\n   107: }\n   108: \n   109: #[must_use]\n   110: #[unstable(feature = \"str_internals\", issue = \"none\")]\n   111: pub struct Debug<'a>(&'a [u8]);\n   112: \n   113: #[unstable(feature = \"str_internals\", issue = \"none\")]\n   114: impl fmt::Debug for Debug<'_> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::Utf8Chunk::valid",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "valid",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 10180,
            "path": "Utf8Chunk"
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
        "impl_id": "core:32271",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10180",
        "resolved_owner_path": [
          "core",
          "str",
          "lossy",
          "Utf8Chunk"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "    68: /// assert_eq!(b\"\\xF1\\x80\", chunk.invalid());\n    69: /// ```\n    70: #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n    71: #[derive(Clone, Debug, PartialEq, Eq)]\n    72: pub struct Utf8Chunk<'a> {\n    73:     valid: &'a str,\n    74:     invalid: &'a [u8],\n    75: }\n    76: \n    77: impl<'a> Utf8Chunk<'a> {\n    78:     /// Returns the next validated UTF-8 substring.\n    79:     ///\n    80:     /// This substring can be empty at the start of the string or between\n    81:     /// broken UTF-8 characters.\n    82:     #[must_use]\n    83:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n    84:     pub fn valid(&self) -> &'a str {\n    85:         self.valid\n    86:     }\n    87: \n    88:     /// Returns the invalid sequence that caused a failure.\n    89:     ///\n    90:     /// The returned slice will have a maximum length of 3 and starts after the\n    91:     /// substring given by [`valid`]. Decoding will resume after this sequence.\n    92:     ///\n    93:     /// If empty, this is the last chunk in the string. If non-empty, an\n    94:     /// unexpected byte was encountered or the end of the input was reached\n    95:     /// unexpectedly.\n    96:     ///\n    97:     /// Lossy decoding would replace this sequence with [`U+FFFD REPLACEMENT\n    98:     /// CHARACTER`].\n    99:     ///\n   100:     /// [`valid`]: Self::valid",
    "nanvix_source": "    74:     invalid: &'a [u8],\n    75: }\n    76: \n    77: impl<'a> Utf8Chunk<'a> {\n    78:     /// Returns the next validated UTF-8 substring.\n    79:     ///\n    80:     /// This substring can be empty at the start of the string or between\n    81:     /// broken UTF-8 characters.\n    82:     #[must_use]\n    83:     #[stable(feature = \"utf8_chunks\", since = \"1.79.0\")]\n    84:     pub fn valid(&self) -> &'a str {\n    85:         self.valid\n    86:     }\n    87: \n    88:     /// Returns the invalid sequence that caused a failure.\n    89:     ///\n    90:     /// The returned slice will have a maximum length of 3 and starts after the\n    91:     /// substring given by [`valid`]. Decoding will resume after this sequence.\n    92:     ///\n    93:     /// If empty, this is the last chunk in the string. If non-empty, an\n    94:     /// unexpected byte was encountered or the end of the input was reached",
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
