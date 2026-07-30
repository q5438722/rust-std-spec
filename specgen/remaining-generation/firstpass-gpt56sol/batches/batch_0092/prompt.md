For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::array_windows",
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
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "array_windows",
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
                    "const": {
                      "expr": "N",
                      "is_literal": false,
                      "value": null
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10069,
            "path": "ArrayWindows"
          }
        }
      }
    },
    "verification_source": "  1630:     /// # Examples\n  1631:     ///\n  1632:     /// ```\n  1633:     /// let slice = [0, 1, 2, 3];\n  1634:     /// let mut iter = slice.array_windows();\n  1635:     /// assert_eq!(iter.next().unwrap(), &[0, 1]);\n  1636:     /// assert_eq!(iter.next().unwrap(), &[1, 2]);\n  1637:     /// assert_eq!(iter.next().unwrap(), &[2, 3]);\n  1638:     /// assert!(iter.next().is_none());\n  1639:     /// ```\n  1640:     ///\n  1641:     /// [`windows`]: slice::windows\n  1642:     #[stable(feature = \"array_windows\", since = \"1.94.0\")]\n  1643:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     pub const fn array_windows<const N: usize>(&self) -> ArrayWindows<'_, T, N> {\n  1647:         assert!(N != 0, \"window size must be non-zero\");\n  1648:         ArrayWindows::new(self)\n  1649:     }\n  1650: \n  1651:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1652:     /// of the slice.\n  1653:     ///\n  1654:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1655:     /// slice, then the last chunk will not have length `chunk_size`.\n  1656:     ///\n  1657:     /// See [`rchunks_exact`] for a variant of this iterator that returns chunks of always exactly\n  1658:     /// `chunk_size` elements, and [`chunks`] for the same iterator but starting at the beginning\n  1659:     /// of the slice.\n  1660:     ///\n  1661:     /// If your `chunk_size` is a constant, consider using [`as_rchunks`] instead, which will\n  1662:     /// give references to arrays of exactly that length, rather than slices.",
    "nanvix_source": "  1639:     /// assert_eq!(iter.next().unwrap(), &[1, 2]);\n  1640:     /// assert_eq!(iter.next().unwrap(), &[2, 3]);\n  1641:     /// assert!(iter.next().is_none());\n  1642:     /// ```\n  1643:     ///\n  1644:     /// [`windows`]: slice::windows\n  1645:     #[stable(feature = \"array_windows\", since = \"1.94.0\")]\n  1646:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1647:     #[inline]\n  1648:     #[track_caller]\n  1649:     pub const fn array_windows<const N: usize>(&self) -> ArrayWindows<'_, T, N> {\n  1650:         assert!(N != 0, \"window size must be non-zero\");\n  1651:         ArrayWindows::new(self)\n  1652:     }\n  1653: \n  1654:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1655:     /// of the slice.\n  1656:     ///\n  1657:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1658:     /// slice, then the last chunk will not have length `chunk_size`.\n  1659:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::chunks",
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
      "name": "chunks",
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
            "chunk_size",
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
            "id": 10063,
            "path": "Chunks"
          }
        }
      }
    },
    "verification_source": "  1139:     /// ```\n  1140:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1141:     /// let mut iter = slice.chunks(2);\n  1142:     /// assert_eq!(iter.next().unwrap(), &['l', 'o']);\n  1143:     /// assert_eq!(iter.next().unwrap(), &['r', 'e']);\n  1144:     /// assert_eq!(iter.next().unwrap(), &['m']);\n  1145:     /// assert!(iter.next().is_none());\n  1146:     /// ```\n  1147:     ///\n  1148:     /// [`chunks_exact`]: slice::chunks_exact\n  1149:     /// [`rchunks`]: slice::rchunks\n  1150:     /// [`as_chunks`]: slice::as_chunks\n  1151:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1152:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1153:     #[inline]\n  1154:     #[track_caller]\n  1155:     pub const fn chunks(&self, chunk_size: usize) -> Chunks<'_, T> {\n  1156:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1157:         Chunks::new(self, chunk_size)\n  1158:     }\n  1159: \n  1160:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1161:     /// beginning of the slice.\n  1162:     ///\n  1163:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1164:     /// length of the slice, then the last chunk will not have length `chunk_size`.\n  1165:     ///\n  1166:     /// See [`chunks_exact_mut`] for a variant of this iterator that returns chunks of always\n  1167:     /// exactly `chunk_size` elements, and [`rchunks_mut`] for the same iterator but starting at\n  1168:     /// the end of the slice.\n  1169:     ///\n  1170:     /// If your `chunk_size` is a constant, consider using [`as_chunks_mut`] instead, which will\n  1171:     /// give references to arrays of exactly that length, rather than slices.",
    "nanvix_source": "  1148:     /// assert!(iter.next().is_none());\n  1149:     /// ```\n  1150:     ///\n  1151:     /// [`chunks_exact`]: slice::chunks_exact\n  1152:     /// [`rchunks`]: slice::rchunks\n  1153:     /// [`as_chunks`]: slice::as_chunks\n  1154:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1155:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1156:     #[inline]\n  1157:     #[track_caller]\n  1158:     pub const fn chunks(&self, chunk_size: usize) -> Chunks<'_, T> {\n  1159:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1160:         Chunks::new(self, chunk_size)\n  1161:     }\n  1162: \n  1163:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1164:     /// beginning of the slice.\n  1165:     ///\n  1166:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1167:     /// length of the slice, then the last chunk will not have length `chunk_size`.\n  1168:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::chunks_exact",
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
      "name": "chunks_exact",
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
            "chunk_size",
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
            "id": 10066,
            "path": "ChunksExact"
          }
        }
      }
    },
    "verification_source": "  1226:     /// ```\n  1227:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1228:     /// let mut iter = slice.chunks_exact(2);\n  1229:     /// assert_eq!(iter.next().unwrap(), &['l', 'o']);\n  1230:     /// assert_eq!(iter.next().unwrap(), &['r', 'e']);\n  1231:     /// assert!(iter.next().is_none());\n  1232:     /// assert_eq!(iter.remainder(), &['m']);\n  1233:     /// ```\n  1234:     ///\n  1235:     /// [`chunks`]: slice::chunks\n  1236:     /// [`rchunks_exact`]: slice::rchunks_exact\n  1237:     /// [`as_chunks`]: slice::as_chunks\n  1238:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1239:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1240:     #[inline]\n  1241:     #[track_caller]\n  1242:     pub const fn chunks_exact(&self, chunk_size: usize) -> ChunksExact<'_, T> {\n  1243:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1244:         ChunksExact::new(self, chunk_size)\n  1245:     }\n  1246: \n  1247:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1248:     /// beginning of the slice.\n  1249:     ///\n  1250:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1251:     /// length of the slice, then the last up to `chunk_size-1` elements will be omitted and can be\n  1252:     /// retrieved from the `into_remainder` function of the iterator.\n  1253:     ///\n  1254:     /// Due to each chunk having exactly `chunk_size` elements, the compiler can often optimize the\n  1255:     /// resulting code better than in the case of [`chunks_mut`].\n  1256:     ///\n  1257:     /// See [`chunks_mut`] for a variant of this iterator that also returns the remainder as a\n  1258:     /// smaller chunk, and [`rchunks_exact_mut`] for the same iterator but starting at the end of",
    "nanvix_source": "  1235:     /// assert_eq!(iter.remainder(), &['m']);\n  1236:     /// ```\n  1237:     ///\n  1238:     /// [`chunks`]: slice::chunks\n  1239:     /// [`rchunks_exact`]: slice::rchunks_exact\n  1240:     /// [`as_chunks`]: slice::as_chunks\n  1241:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1242:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1243:     #[inline]\n  1244:     #[track_caller]\n  1245:     pub const fn chunks_exact(&self, chunk_size: usize) -> ChunksExact<'_, T> {\n  1246:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1247:         ChunksExact::new(self, chunk_size)\n  1248:     }\n  1249: \n  1250:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1251:     /// beginning of the slice.\n  1252:     ///\n  1253:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1254:     /// length of the slice, then the last up to `chunk_size-1` elements will be omitted and can be\n  1255:     /// retrieved from the `into_remainder` function of the iterator.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::chunks_exact_mut",
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
      "name": "chunks_exact_mut",
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
          ],
          [
            "chunk_size",
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
            "id": 13736,
            "path": "ChunksExactMut"
          }
        }
      }
    },
    "verification_source": "  1274:     /// for chunk in v.chunks_exact_mut(2) {\n  1275:     ///     for elem in chunk.iter_mut() {\n  1276:     ///         *elem += count;\n  1277:     ///     }\n  1278:     ///     count += 1;\n  1279:     /// }\n  1280:     /// assert_eq!(v, &[1, 1, 2, 2, 0]);\n  1281:     /// ```\n  1282:     ///\n  1283:     /// [`chunks_mut`]: slice::chunks_mut\n  1284:     /// [`rchunks_exact_mut`]: slice::rchunks_exact_mut\n  1285:     /// [`as_chunks_mut`]: slice::as_chunks_mut\n  1286:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1287:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1288:     #[inline]\n  1289:     #[track_caller]\n  1290:     pub const fn chunks_exact_mut(&mut self, chunk_size: usize) -> ChunksExactMut<'_, T> {\n  1291:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1292:         ChunksExactMut::new(self, chunk_size)\n  1293:     }\n  1294: \n  1295:     /// Splits the slice into a slice of `N`-element arrays,\n  1296:     /// assuming that there's no remainder.\n  1297:     ///\n  1298:     /// This is the inverse operation to [`as_flattened`].\n  1299:     ///\n  1300:     /// [`as_flattened`]: slice::as_flattened\n  1301:     ///\n  1302:     /// As this is `unsafe`, consider whether you could use [`as_chunks`] or\n  1303:     /// [`as_rchunks`] instead, perhaps via something like\n  1304:     /// `if let (chunks, []) = slice.as_chunks()` or\n  1305:     /// `let (chunks, []) = slice.as_chunks() else { unreachable!() };`.\n  1306:     ///",
    "nanvix_source": "  1283:     /// assert_eq!(v, &[1, 1, 2, 2, 0]);\n  1284:     /// ```\n  1285:     ///\n  1286:     /// [`chunks_mut`]: slice::chunks_mut\n  1287:     /// [`rchunks_exact_mut`]: slice::rchunks_exact_mut\n  1288:     /// [`as_chunks_mut`]: slice::as_chunks_mut\n  1289:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  1290:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1291:     #[inline]\n  1292:     #[track_caller]\n  1293:     pub const fn chunks_exact_mut(&mut self, chunk_size: usize) -> ChunksExactMut<'_, T> {\n  1294:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1295:         ChunksExactMut::new(self, chunk_size)\n  1296:     }\n  1297: \n  1298:     /// Splits the slice into a slice of `N`-element arrays,\n  1299:     /// assuming that there's no remainder.\n  1300:     ///\n  1301:     /// This is the inverse operation to [`as_flattened`].\n  1302:     ///\n  1303:     /// [`as_flattened`]: slice::as_flattened",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::chunks_mut",
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
      "name": "chunks_mut",
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
          ],
          [
            "chunk_size",
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
            "id": 13734,
            "path": "ChunksMut"
          }
        }
      }
    },
    "verification_source": "  1183:     /// for chunk in v.chunks_mut(2) {\n  1184:     ///     for elem in chunk.iter_mut() {\n  1185:     ///         *elem += count;\n  1186:     ///     }\n  1187:     ///     count += 1;\n  1188:     /// }\n  1189:     /// assert_eq!(v, &[1, 1, 2, 2, 3]);\n  1190:     /// ```\n  1191:     ///\n  1192:     /// [`chunks_exact_mut`]: slice::chunks_exact_mut\n  1193:     /// [`rchunks_mut`]: slice::rchunks_mut\n  1194:     /// [`as_chunks_mut`]: slice::as_chunks_mut\n  1195:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1196:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1197:     #[inline]\n  1198:     #[track_caller]\n  1199:     pub const fn chunks_mut(&mut self, chunk_size: usize) -> ChunksMut<'_, T> {\n  1200:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1201:         ChunksMut::new(self, chunk_size)\n  1202:     }\n  1203: \n  1204:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1205:     /// beginning of the slice.\n  1206:     ///\n  1207:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1208:     /// slice, then the last up to `chunk_size-1` elements will be omitted and can be retrieved\n  1209:     /// from the `remainder` function of the iterator.\n  1210:     ///\n  1211:     /// Due to each chunk having exactly `chunk_size` elements, the compiler can often optimize the\n  1212:     /// resulting code better than in the case of [`chunks`].\n  1213:     ///\n  1214:     /// See [`chunks`] for a variant of this iterator that also returns the remainder as a smaller\n  1215:     /// chunk, and [`rchunks_exact`] for the same iterator but starting at the end of the slice.",
    "nanvix_source": "  1192:     /// assert_eq!(v, &[1, 1, 2, 2, 3]);\n  1193:     /// ```\n  1194:     ///\n  1195:     /// [`chunks_exact_mut`]: slice::chunks_exact_mut\n  1196:     /// [`rchunks_mut`]: slice::rchunks_mut\n  1197:     /// [`as_chunks_mut`]: slice::as_chunks_mut\n  1198:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1199:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1200:     #[inline]\n  1201:     #[track_caller]\n  1202:     pub const fn chunks_mut(&mut self, chunk_size: usize) -> ChunksMut<'_, T> {\n  1203:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1204:         ChunksMut::new(self, chunk_size)\n  1205:     }\n  1206: \n  1207:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1208:     /// beginning of the slice.\n  1209:     ///\n  1210:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1211:     /// slice, then the last up to `chunk_size-1` elements will be omitted and can be retrieved\n  1212:     /// from the `remainder` function of the iterator.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::escape_ascii",
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
      "name": "escape_ascii",
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
        "impl_id": "core:51785",
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
            "id": 10044,
            "path": "EscapeAscii"
          }
        }
      }
    },
    "verification_source": "   202:         }\n   203:     }\n   204: \n   205:     /// Returns an iterator that produces an escaped version of this slice,\n   206:     /// treating it as an ASCII string.\n   207:     ///\n   208:     /// # Examples\n   209:     ///\n   210:     /// ```\n   211:     /// let s = b\"0\\t\\r\\n'\\\"\\\\\\x9d\";\n   212:     /// let escaped = s.escape_ascii().to_string();\n   213:     /// assert_eq!(escaped, \"0\\\\t\\\\r\\\\n\\\\'\\\\\\\"\\\\\\\\\\\\x9d\");\n   214:     /// ```\n   215:     #[must_use = \"this returns the escaped bytes as an iterator, \\\n   216:                   without modifying the original\"]\n   217:     #[stable(feature = \"inherent_ascii_escape\", since = \"1.60.0\")]\n   218:     pub fn escape_ascii(&self) -> EscapeAscii<'_> {\n   219:         EscapeAscii { inner: self.iter().flat_map(EscapeByte) }\n   220:     }\n   221: \n   222:     /// Returns a byte slice with leading ASCII whitespace bytes removed.\n   223:     ///\n   224:     /// 'Whitespace' refers to the definition used by\n   225:     /// [`u8::is_ascii_whitespace`].\n   226:     ///\n   227:     /// # Examples\n   228:     ///\n   229:     /// ```\n   230:     /// assert_eq!(b\" \\t hello world\\n\".trim_ascii_start(), b\"hello world\\n\");\n   231:     /// assert_eq!(b\"  \".trim_ascii_start(), b\"\");\n   232:     /// assert_eq!(b\"\".trim_ascii_start(), b\"\");\n   233:     /// ```\n   234:     #[stable(feature = \"byte_slice_trim_ascii\", since = \"1.80.0\")]",
    "nanvix_source": "   208:     /// # Examples\n   209:     ///\n   210:     /// ```\n   211:     /// let s = b\"0\\t\\r\\n'\\\"\\\\\\x9d\";\n   212:     /// let escaped = s.escape_ascii().to_string();\n   213:     /// assert_eq!(escaped, \"0\\\\t\\\\r\\\\n\\\\'\\\\\\\"\\\\\\\\\\\\x9d\");\n   214:     /// ```\n   215:     #[must_use = \"this returns the escaped bytes as an iterator, \\\n   216:                   without modifying the original\"]\n   217:     #[stable(feature = \"inherent_ascii_escape\", since = \"1.60.0\")]\n   218:     pub fn escape_ascii(&self) -> EscapeAscii<'_> {\n   219:         EscapeAscii { inner: self.iter().flat_map(EscapeByte) }\n   220:     }\n   221: \n   222:     /// Returns a byte slice with leading ASCII whitespace bytes removed.\n   223:     ///\n   224:     /// 'Whitespace' refers to the definition used by\n   225:     /// [`u8::is_ascii_whitespace`]. Importantly, this definition excludes\n   226:     /// the `\\0x0B` byte even though it has the Unicode [`White_Space`] property\n   227:     /// and is removed by [`str::trim_start`].\n   228:     ///",
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
