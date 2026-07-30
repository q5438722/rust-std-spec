For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::Read::by_ref",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "by_ref",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "  1085:     ///     let mut other_buffer = Vec::new();\n  1086:     ///\n  1087:     ///     {\n  1088:     ///         let reference = f.by_ref();\n  1089:     ///\n  1090:     ///         // read at most 5 bytes\n  1091:     ///         reference.take(5).read_to_end(&mut buffer)?;\n  1092:     ///\n  1093:     ///     } // drop our &mut reference so we can use f again\n  1094:     ///\n  1095:     ///     // original file still usable, read the rest\n  1096:     ///     f.read_to_end(&mut other_buffer)?;\n  1097:     ///     Ok(())\n  1098:     /// }\n  1099:     /// ```\n  1100:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1101:     fn by_ref(&mut self) -> &mut Self\n  1102:     where\n  1103:         Self: Sized,\n  1104:     {\n  1105:         self\n  1106:     }\n  1107: \n  1108:     /// Transforms this `Read` instance to an [`Iterator`] over its bytes.\n  1109:     ///\n  1110:     /// The returned type implements [`Iterator`] where the [`Item`] is\n  1111:     /// <code>[Result]<[u8], [io::Error]></code>.\n  1112:     /// The yielded item is [`Ok`] if a byte was successfully read and [`Err`]\n  1113:     /// otherwise. EOF is mapped to returning [`None`] from this iterator.\n  1114:     ///\n  1115:     /// The default implementation calls `read` for each byte,\n  1116:     /// which can be very inefficient for data that's not in memory,\n  1117:     /// such as [`File`]. Consider using a [`BufReader`] in such cases.",
    "nanvix_source": "  1097:     ///         reference.take(5).read_to_end(&mut buffer)?;\n  1098:     ///\n  1099:     ///     } // drop our &mut reference so we can use f again\n  1100:     ///\n  1101:     ///     // original file still usable, read the rest\n  1102:     ///     f.read_to_end(&mut other_buffer)?;\n  1103:     ///     Ok(())\n  1104:     /// }\n  1105:     /// ```\n  1106:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1107:     fn by_ref(&mut self) -> &mut Self\n  1108:     where\n  1109:         Self: Sized,\n  1110:     {\n  1111:         self\n  1112:     }\n  1113: \n  1114:     /// Transforms this `Read` instance to an [`Iterator`] over its bytes.\n  1115:     ///\n  1116:     /// The returned type implements [`Iterator`] where the [`Item`] is\n  1117:     /// <code>[Result]<[u8], [io::Error]></code>.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::bytes",
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
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
            "id": 4211,
            "path": "Bytes"
          }
        }
      }
    },
    "verification_source": "  1128:     /// ```no_run\n  1129:     /// use std::io;\n  1130:     /// use std::io::prelude::*;\n  1131:     /// use std::io::BufReader;\n  1132:     /// use std::fs::File;\n  1133:     ///\n  1134:     /// fn main() -> io::Result<()> {\n  1135:     ///     let f = BufReader::new(File::open(\"foo.txt\")?);\n  1136:     ///\n  1137:     ///     for byte in f.bytes() {\n  1138:     ///         println!(\"{}\", byte?);\n  1139:     ///     }\n  1140:     ///     Ok(())\n  1141:     /// }\n  1142:     /// ```\n  1143:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1144:     fn bytes(self) -> Bytes<Self>\n  1145:     where\n  1146:         Self: Sized,\n  1147:     {\n  1148:         Bytes { inner: self }\n  1149:     }\n  1150: \n  1151:     /// Creates an adapter which will chain this stream with another.\n  1152:     ///\n  1153:     /// The returned `Read` instance will first read all bytes from this object\n  1154:     /// until EOF is encountered. Afterwards the output is equivalent to the\n  1155:     /// output of `next`.\n  1156:     ///\n  1157:     /// # Examples\n  1158:     ///\n  1159:     /// [`File`]s implement `Read`:\n  1160:     ///",
    "nanvix_source": "  1140:     /// fn main() -> io::Result<()> {\n  1141:     ///     let f = BufReader::new(File::open(\"foo.txt\")?);\n  1142:     ///\n  1143:     ///     for byte in f.bytes() {\n  1144:     ///         println!(\"{}\", byte?);\n  1145:     ///     }\n  1146:     ///     Ok(())\n  1147:     /// }\n  1148:     /// ```\n  1149:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1150:     fn bytes(self) -> Bytes<Self>\n  1151:     where\n  1152:         Self: Sized,\n  1153:     {\n  1154:         Bytes { inner: self }\n  1155:     }\n  1156: \n  1157:     /// Creates an adapter which will chain this stream with another.\n  1158:     ///\n  1159:     /// The returned `Read` instance will first read all bytes from this object\n  1160:     /// until EOF is encountered. Afterwards the output is equivalent to the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::chain",
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
                        "id": 2620,
                        "path": "Read"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
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
      "name": "chain",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
            "next",
            {
              "generic": "R"
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
                  },
                  {
                    "type": {
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4213,
            "path": "Chain"
          }
        }
      }
    },
    "verification_source": "  1166:     /// use std::fs::File;\n  1167:     ///\n  1168:     /// fn main() -> io::Result<()> {\n  1169:     ///     let f1 = File::open(\"foo.txt\")?;\n  1170:     ///     let f2 = File::open(\"bar.txt\")?;\n  1171:     ///\n  1172:     ///     let mut handle = f1.chain(f2);\n  1173:     ///     let mut buffer = String::new();\n  1174:     ///\n  1175:     ///     // read the value into a String. We could use any Read method here,\n  1176:     ///     // this is just one example.\n  1177:     ///     handle.read_to_string(&mut buffer)?;\n  1178:     ///     Ok(())\n  1179:     /// }\n  1180:     /// ```\n  1181:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1182:     fn chain<R: Read>(self, next: R) -> Chain<Self, R>\n  1183:     where\n  1184:         Self: Sized,\n  1185:     {\n  1186:         Chain { first: self, second: next, done_first: false }\n  1187:     }\n  1188: \n  1189:     /// Creates an adapter which will read at most `limit` bytes from it.\n  1190:     ///\n  1191:     /// This function returns a new instance of `Read` which will read at most\n  1192:     /// `limit` bytes, after which it will always return EOF ([`Ok(0)`]). Any\n  1193:     /// read errors will not count towards the number of bytes read and future\n  1194:     /// calls to [`read()`] may succeed.\n  1195:     ///\n  1196:     /// # Examples\n  1197:     ///\n  1198:     /// [`File`]s implement `Read`:",
    "nanvix_source": "  1178:     ///     let mut handle = f1.chain(f2);\n  1179:     ///     let mut buffer = String::new();\n  1180:     ///\n  1181:     ///     // read the value into a String. We could use any Read method here,\n  1182:     ///     // this is just one example.\n  1183:     ///     handle.read_to_string(&mut buffer)?;\n  1184:     ///     Ok(())\n  1185:     /// }\n  1186:     /// ```\n  1187:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1188:     fn chain<R: Read>(self, next: R) -> Chain<Self, R>\n  1189:     where\n  1190:         Self: Sized,\n  1191:     {\n  1192:         core::io::chain(self, next)\n  1193:     }\n  1194: \n  1195:     /// Creates an adapter which will read at most `limit` bytes from it.\n  1196:     ///\n  1197:     /// This function returns a new instance of `Read` which will read at most\n  1198:     /// `limit` bytes, after which it will always return EOF ([`Ok(0)`]). Any",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::read",
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
      "name": "read",
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
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
    "verification_source": "   779:     /// use std::io;\n   780:     /// use std::io::prelude::*;\n   781:     /// use std::fs::File;\n   782:     ///\n   783:     /// fn main() -> io::Result<()> {\n   784:     ///     let mut f = File::open(\"foo.txt\")?;\n   785:     ///     let mut buffer = [0; 10];\n   786:     ///\n   787:     ///     // read up to 10 bytes\n   788:     ///     let n = f.read(&mut buffer[..])?;\n   789:     ///\n   790:     ///     println!(\"The bytes: {:?}\", &buffer[..n]);\n   791:     ///     Ok(())\n   792:     /// }\n   793:     /// ```\n   794:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   795:     fn read(&mut self, buf: &mut [u8]) -> Result<usize>;\n   796: \n   797:     /// Like `read`, except that it reads into a slice of buffers.\n   798:     ///\n   799:     /// Data is copied to fill each buffer in order, with the final buffer\n   800:     /// written to possibly being only partially filled. This method must\n   801:     /// behave equivalently to a single call to `read` with concatenated\n   802:     /// buffers.\n   803:     ///\n   804:     /// The default implementation calls `read` with either the first nonempty\n   805:     /// buffer provided, or an empty one if none exists.\n   806:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n   807:     fn read_vectored(&mut self, bufs: &mut [IoSliceMut<'_>]) -> Result<usize> {\n   808:         default_read_vectored(|b| self.read(b), bufs)\n   809:     }\n   810: \n   811:     /// Determines if this `Read`er has an efficient `read_vectored`",
    "nanvix_source": "   791:     ///     let mut buffer = [0; 10];\n   792:     ///\n   793:     ///     // read up to 10 bytes\n   794:     ///     let n = f.read(&mut buffer[..])?;\n   795:     ///\n   796:     ///     println!(\"The bytes: {:?}\", &buffer[..n]);\n   797:     ///     Ok(())\n   798:     /// }\n   799:     /// ```\n   800:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   801:     fn read(&mut self, buf: &mut [u8]) -> Result<usize>;\n   802: \n   803:     /// Like `read`, except that it reads into a slice of buffers.\n   804:     ///\n   805:     /// Data is copied to fill each buffer in order, with the final buffer\n   806:     /// written to possibly being only partially filled. This method must\n   807:     /// behave equivalently to a single call to `read` with concatenated\n   808:     /// buffers.\n   809:     ///\n   810:     /// The default implementation calls `read` with either the first nonempty\n   811:     /// buffer provided, or an empty one if none exists.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::read_exact",
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
      "name": "read_exact",
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
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
                      "tuple": []
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
    "verification_source": "  1010:     ///\n  1011:     /// ```no_run\n  1012:     /// use std::io;\n  1013:     /// use std::io::prelude::*;\n  1014:     /// use std::fs::File;\n  1015:     ///\n  1016:     /// fn main() -> io::Result<()> {\n  1017:     ///     let mut f = File::open(\"foo.txt\")?;\n  1018:     ///     let mut buffer = [0; 10];\n  1019:     ///\n  1020:     ///     // read exactly 10 bytes\n  1021:     ///     f.read_exact(&mut buffer)?;\n  1022:     ///     Ok(())\n  1023:     /// }\n  1024:     /// ```\n  1025:     #[stable(feature = \"read_exact\", since = \"1.6.0\")]\n  1026:     fn read_exact(&mut self, buf: &mut [u8]) -> Result<()> {\n  1027:         default_read_exact(self, buf)\n  1028:     }\n  1029: \n  1030:     /// Pull some bytes from this source into the specified buffer.\n  1031:     ///\n  1032:     /// This is equivalent to the [`read`](Read::read) method, except that it is passed a [`BorrowedCursor`] rather than `[u8]` to allow use\n  1033:     /// with uninitialized buffers. The new data will be appended to any existing contents of `buf`.\n  1034:     ///\n  1035:     /// The default implementation delegates to `read`.\n  1036:     ///\n  1037:     /// This method makes it possible to return both data and an error but it is advised against.\n  1038:     #[unstable(feature = \"read_buf\", issue = \"78485\")]\n  1039:     fn read_buf(&mut self, buf: BorrowedCursor<'_>) -> Result<()> {\n  1040:         default_read_buf(|b| self.read(b), buf)\n  1041:     }\n  1042: ",
    "nanvix_source": "  1022:     /// fn main() -> io::Result<()> {\n  1023:     ///     let mut f = File::open(\"foo.txt\")?;\n  1024:     ///     let mut buffer = [0; 10];\n  1025:     ///\n  1026:     ///     // read exactly 10 bytes\n  1027:     ///     f.read_exact(&mut buffer)?;\n  1028:     ///     Ok(())\n  1029:     /// }\n  1030:     /// ```\n  1031:     #[stable(feature = \"read_exact\", since = \"1.6.0\")]\n  1032:     fn read_exact(&mut self, buf: &mut [u8]) -> Result<()> {\n  1033:         default_read_exact(self, buf)\n  1034:     }\n  1035: \n  1036:     /// Pull some bytes from this source into the specified buffer.\n  1037:     ///\n  1038:     /// This is equivalent to the [`read`](Read::read) method, except that it is passed a [`BorrowedCursor`] rather than `[u8]` to allow use\n  1039:     /// with uninitialized buffers. The new data will be appended to any existing contents of `buf`.\n  1040:     ///\n  1041:     /// The default implementation delegates to `read`.\n  1042:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::read_to_end",
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
      "name": "read_to_end",
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
        "item_id": "std:2620",
        "kind": "trait",
        "name": "Read",
        "path": [
          "std",
          "io",
          "Read"
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
    "verification_source": "   901:     ///\n   902:     /// # Usage Notes\n   903:     ///\n   904:     /// `read_to_end` attempts to read a source until EOF, but many sources are continuous streams\n   905:     /// that do not send EOF. In these cases, `read_to_end` will block indefinitely. Standard input\n   906:     /// is one such stream which may be finite if piped, but is typically continuous. For example,\n   907:     /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n   908:     /// Reading user input or running programs that remain open indefinitely will never terminate\n   909:     /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n   910:     ///\n   911:     /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n   912:     ///\n   913:     ///[`read`]: Read::read\n   914:     ///\n   915:     /// [`Vec::try_reserve`]: crate::vec::Vec::try_reserve\n   916:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   917:     fn read_to_end(&mut self, buf: &mut Vec<u8>) -> Result<usize> {\n   918:         default_read_to_end(self, buf, None)\n   919:     }\n   920: \n   921:     /// Reads all bytes until EOF in this source, appending them to `buf`.\n   922:     ///\n   923:     /// If successful, this function returns the number of bytes which were read\n   924:     /// and appended to `buf`.\n   925:     ///\n   926:     /// # Errors\n   927:     ///\n   928:     /// If the data in this stream is *not* valid UTF-8 then an error is\n   929:     /// returned and `buf` is unchanged.\n   930:     ///\n   931:     /// See [`read_to_end`] for other error semantics.\n   932:     ///\n   933:     /// [`read_to_end`]: Read::read_to_end",
    "nanvix_source": "   913:     /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n   914:     /// Reading user input or running programs that remain open indefinitely will never terminate\n   915:     /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n   916:     ///\n   917:     /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n   918:     ///\n   919:     ///[`read`]: Read::read\n   920:     ///\n   921:     /// [`Vec::try_reserve`]: crate::vec::Vec::try_reserve\n   922:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   923:     fn read_to_end(&mut self, buf: &mut Vec<u8>) -> Result<usize> {\n   924:         default_read_to_end(self, buf, None)\n   925:     }\n   926: \n   927:     /// Reads all bytes until EOF in this source, appending them to `buf`.\n   928:     ///\n   929:     /// If successful, this function returns the number of bytes which were read\n   930:     /// and appended to `buf`.\n   931:     ///\n   932:     /// # Errors\n   933:     ///",
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
