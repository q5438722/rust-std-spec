For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::DirBuilderExt::mode",
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "mode",
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
        "item_id": "std:3130",
        "kind": "trait",
        "name": "DirBuilderExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "DirBuilderExt"
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
            "mode",
            {
              "primitive": "u32"
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
    "verification_source": "  1068: /// Unix-specific extensions to [`fs::DirBuilder`].\n  1069: #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1070: pub trait DirBuilderExt {\n  1071:     /// Sets the mode to create new directories with. This option defaults to\n  1072:     /// 0o777.\n  1073:     ///\n  1074:     /// # Examples\n  1075:     ///\n  1076:     /// ```no_run\n  1077:     /// use std::fs::DirBuilder;\n  1078:     /// use std::os::unix::fs::DirBuilderExt;\n  1079:     ///\n  1080:     /// let mut builder = DirBuilder::new();\n  1081:     /// builder.mode(0o755);\n  1082:     /// ```\n  1083:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1084:     fn mode(&mut self, mode: u32) -> &mut Self;\n  1085: }\n  1086: \n  1087: #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1088: impl DirBuilderExt for fs::DirBuilder {\n  1089:     fn mode(&mut self, mode: u32) -> &mut fs::DirBuilder {\n  1090:         self.as_inner_mut().set_mode(mode);\n  1091:         self\n  1092:     }\n  1093: }\n  1094: \n  1095: /// Change the owner and group of the specified path.\n  1096: ///\n  1097: /// Specifying either the uid or gid as `None` will leave it unchanged.\n  1098: ///\n  1099: /// Changing the owner typically requires privileges, such as root or a specific capability.\n  1100: /// Changing the group typically requires either being the owner and a member of the group, or",
    "nanvix_source": "  1073:     /// # Examples\n  1074:     ///\n  1075:     /// ```no_run\n  1076:     /// use std::fs::DirBuilder;\n  1077:     /// use std::os::unix::fs::DirBuilderExt;\n  1078:     ///\n  1079:     /// let mut builder = DirBuilder::new();\n  1080:     /// builder.mode(0o755);\n  1081:     /// ```\n  1082:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1083:     fn mode(&mut self, mode: u32) -> &mut Self;\n  1084: }\n  1085: \n  1086: #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1087: impl DirBuilderExt for fs::DirBuilder {\n  1088:     fn mode(&mut self, mode: u32) -> &mut fs::DirBuilder {\n  1089:         self.as_inner_mut().set_mode(mode);\n  1090:         self\n  1091:     }\n  1092: }\n  1093: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::DirEntryExt::ino",
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
      "name": "ino",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2931",
        "kind": "trait",
        "name": "DirEntryExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "DirEntryExt"
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   986:     /// # Examples\n   987:     ///\n   988:     /// ```\n   989:     /// use std::fs;\n   990:     /// use std::os::unix::fs::DirEntryExt;\n   991:     ///\n   992:     /// if let Ok(entries) = fs::read_dir(\".\") {\n   993:     ///     for entry in entries {\n   994:     ///         if let Ok(entry) = entry {\n   995:     ///             // Here, `entry` is a `DirEntry`.\n   996:     ///             println!(\"{:?}: {}\", entry.file_name(), entry.ino());\n   997:     ///         }\n   998:     ///     }\n   999:     /// }\n  1000:     /// ```\n  1001:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  1002:     fn ino(&self) -> u64;\n  1003: }\n  1004: \n  1005: #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  1006: impl DirEntryExt for fs::DirEntry {\n  1007:     fn ino(&self) -> u64 {\n  1008:         self.as_inner().ino()\n  1009:     }\n  1010: }\n  1011: \n  1012: /// Sealed Unix-specific extension methods for [`fs::DirEntry`].\n  1013: #[unstable(feature = \"dir_entry_ext2\", issue = \"85573\")]\n  1014: pub trait DirEntryExt2: Sealed {\n  1015:     /// Returns a reference to the underlying `OsStr` of this entry's filename.\n  1016:     ///\n  1017:     /// # Examples\n  1018:     ///",
    "nanvix_source": "   995:     /// if let Ok(entries) = fs::read_dir(\".\") {\n   996:     ///     for entry in entries {\n   997:     ///         if let Ok(entry) = entry {\n   998:     ///             // Here, `entry` is a `DirEntry`.\n   999:     ///             println!(\"{:?}: {}\", entry.file_name(), entry.ino());\n  1000:     ///         }\n  1001:     ///     }\n  1002:     /// }\n  1003:     /// ```\n  1004:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  1005:     fn ino(&self) -> u64;\n  1006: }\n  1007: \n  1008: #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  1009: impl DirEntryExt for fs::DirEntry {\n  1010:     fn ino(&self) -> u64 {\n  1011:         self.as_inner().ino()\n  1012:     }\n  1013: }\n  1014: \n  1015: /// Unix-specific extension methods for [`fs::DirEntry`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileExt::read_at",
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
      "name": "read_at",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "buf"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2661",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileExt"
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
          ],
          [
            "offset",
            {
              "primitive": "u64"
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
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "    44:     /// ```no_run\n    45:     /// use std::io;\n    46:     /// use std::fs::File;\n    47:     /// use std::os::unix::prelude::FileExt;\n    48:     ///\n    49:     /// fn main() -> io::Result<()> {\n    50:     ///     let mut buf = [0u8; 8];\n    51:     ///     let file = File::open(\"foo.txt\")?;\n    52:     ///\n    53:     ///     // We now read 8 bytes from the offset 10.\n    54:     ///     let num_bytes_read = file.read_at(&mut buf, 10)?;\n    55:     ///     println!(\"read {num_bytes_read} bytes: {buf:?}\");\n    56:     ///     Ok(())\n    57:     /// }\n    58:     /// ```\n    59:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n    60:     fn read_at(&self, buf: &mut [u8], offset: u64) -> io::Result<usize>;\n    61: \n    62:     /// Like `read_at`, except that it reads into a slice of buffers.\n    63:     ///\n    64:     /// Data is copied to fill each buffer in order, with the final buffer\n    65:     /// written to possibly being only partially filled. This method must behave\n    66:     /// equivalently to a single call to read with concatenated buffers.\n    67:     #[unstable(feature = \"unix_file_vectored_at\", issue = \"89517\")]\n    68:     fn read_vectored_at(&self, bufs: &mut [io::IoSliceMut<'_>], offset: u64) -> io::Result<usize> {\n    69:         io::default_read_vectored(|b| self.read_at(b, offset), bufs)\n    70:     }\n    71: \n    72:     /// Reads the exact number of bytes required to fill `buf` from the given offset.\n    73:     ///\n    74:     /// The offset is relative to the start of the file and thus independent\n    75:     /// from the current cursor.\n    76:     ///",
    "nanvix_source": "    49:     ///     let mut buf = [0u8; 8];\n    50:     ///     let file = File::open(\"foo.txt\")?;\n    51:     ///\n    52:     ///     // We now read 8 bytes from the offset 10.\n    53:     ///     let num_bytes_read = file.read_at(&mut buf, 10)?;\n    54:     ///     println!(\"read {num_bytes_read} bytes: {buf:?}\");\n    55:     ///     Ok(())\n    56:     /// }\n    57:     /// ```\n    58:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n    59:     fn read_at(&self, buf: &mut [u8], offset: u64) -> io::Result<usize>;\n    60: \n    61:     /// Like `read_at`, except that it reads into a slice of buffers.\n    62:     ///\n    63:     /// Data is copied to fill each buffer in order, with the final buffer\n    64:     /// written to possibly being only partially filled. This method must behave\n    65:     /// equivalently to a single call to read with concatenated buffers.\n    66:     #[unstable(feature = \"unix_file_vectored_at\", issue = \"89517\")]\n    67:     fn read_vectored_at(&self, bufs: &mut [io::IoSliceMut<'_>], offset: u64) -> io::Result<usize> {\n    68:         io::default_read_vectored(|b| self.read_at(b, offset), bufs)\n    69:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileExt::read_exact_at",
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
      "name": "read_exact_at",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "buf"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2661",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileExt"
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
          ],
          [
            "offset",
            {
              "primitive": "u64"
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
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "   102:     /// ```no_run\n   103:     /// use std::io;\n   104:     /// use std::fs::File;\n   105:     /// use std::os::unix::prelude::FileExt;\n   106:     ///\n   107:     /// fn main() -> io::Result<()> {\n   108:     ///     let mut buf = [0u8; 8];\n   109:     ///     let file = File::open(\"foo.txt\")?;\n   110:     ///\n   111:     ///     // We now read exactly 8 bytes from the offset 10.\n   112:     ///     file.read_exact_at(&mut buf, 10)?;\n   113:     ///     println!(\"read {} bytes: {:?}\", buf.len(), buf);\n   114:     ///     Ok(())\n   115:     /// }\n   116:     /// ```\n   117:     #[stable(feature = \"rw_exact_all_at\", since = \"1.33.0\")]\n   118:     fn read_exact_at(&self, mut buf: &mut [u8], mut offset: u64) -> io::Result<()> {\n   119:         while !buf.is_empty() {\n   120:             match self.read_at(buf, offset) {\n   121:                 Ok(0) => break,\n   122:                 Ok(n) => {\n   123:                     let tmp = buf;\n   124:                     buf = &mut tmp[n..];\n   125:                     offset += n as u64;\n   126:                 }\n   127:                 Err(ref e) if e.is_interrupted() => {}\n   128:                 Err(e) => return Err(e),\n   129:             }\n   130:         }\n   131:         if !buf.is_empty() { Err(io::Error::READ_EXACT_EOF) } else { Ok(()) }\n   132:     }\n   133: \n   134:     /// Reads some bytes starting from a given offset into the buffer.",
    "nanvix_source": "   107:     ///     let mut buf = [0u8; 8];\n   108:     ///     let file = File::open(\"foo.txt\")?;\n   109:     ///\n   110:     ///     // We now read exactly 8 bytes from the offset 10.\n   111:     ///     file.read_exact_at(&mut buf, 10)?;\n   112:     ///     println!(\"read {} bytes: {:?}\", buf.len(), buf);\n   113:     ///     Ok(())\n   114:     /// }\n   115:     /// ```\n   116:     #[stable(feature = \"rw_exact_all_at\", since = \"1.33.0\")]\n   117:     fn read_exact_at(&self, mut buf: &mut [u8], mut offset: u64) -> io::Result<()> {\n   118:         while !buf.is_empty() {\n   119:             match self.read_at(buf, offset) {\n   120:                 Ok(0) => break,\n   121:                 Ok(n) => {\n   122:                     let tmp = buf;\n   123:                     buf = &mut tmp[n..];\n   124:                     offset += n as u64;\n   125:                 }\n   126:                 Err(ref e) if e.is_interrupted() => {}\n   127:                 Err(e) => return Err(e),",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileExt::write_all_at",
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
      "name": "write_all_at",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2661",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileExt"
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
            "buf",
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
          ],
          [
            "offset",
            {
              "primitive": "u64"
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
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "   314:     /// # Examples\n   315:     ///\n   316:     /// ```no_run\n   317:     /// use std::fs::File;\n   318:     /// use std::io;\n   319:     /// use std::os::unix::prelude::FileExt;\n   320:     ///\n   321:     /// fn main() -> io::Result<()> {\n   322:     ///     let file = File::open(\"foo.txt\")?;\n   323:     ///\n   324:     ///     // We now write at the offset 10.\n   325:     ///     file.write_all_at(b\"sushi\", 10)?;\n   326:     ///     Ok(())\n   327:     /// }\n   328:     /// ```\n   329:     #[stable(feature = \"rw_exact_all_at\", since = \"1.33.0\")]\n   330:     fn write_all_at(&self, mut buf: &[u8], mut offset: u64) -> io::Result<()> {\n   331:         while !buf.is_empty() {\n   332:             match self.write_at(buf, offset) {\n   333:                 Ok(0) => {\n   334:                     return Err(io::Error::WRITE_ALL_EOF);\n   335:                 }\n   336:                 Ok(n) => {\n   337:                     buf = &buf[n..];\n   338:                     offset += n as u64\n   339:                 }\n   340:                 Err(ref e) if e.is_interrupted() => {}\n   341:                 Err(e) => return Err(e),\n   342:             }\n   343:         }\n   344:         Ok(())\n   345:     }\n   346: }",
    "nanvix_source": "   323:     ///\n   324:     /// fn main() -> io::Result<()> {\n   325:     ///     let file = File::open(\"foo.txt\")?;\n   326:     ///\n   327:     ///     // We now write at the offset 10.\n   328:     ///     file.write_all_at(b\"sushi\", 10)?;\n   329:     ///     Ok(())\n   330:     /// }\n   331:     /// ```\n   332:     #[stable(feature = \"rw_exact_all_at\", since = \"1.33.0\")]\n   333:     fn write_all_at(&self, mut buf: &[u8], mut offset: u64) -> io::Result<()> {\n   334:         while !buf.is_empty() {\n   335:             match self.write_at(buf, offset) {\n   336:                 Ok(0) => {\n   337:                     return Err(io::Error::WRITE_ALL_EOF);\n   338:                 }\n   339:                 Ok(n) => {\n   340:                     buf = &buf[n..];\n   341:                     offset += n as u64\n   342:                 }\n   343:                 Err(ref e) if e.is_interrupted() => {}",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileExt::write_at",
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
      "name": "write_at",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2661",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileExt"
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
            "buf",
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
          ],
          [
            "offset",
            {
              "primitive": "u64"
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
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "   265:     /// # Examples\n   266:     ///\n   267:     /// ```no_run\n   268:     /// use std::fs::File;\n   269:     /// use std::io;\n   270:     /// use std::os::unix::prelude::FileExt;\n   271:     ///\n   272:     /// fn main() -> io::Result<()> {\n   273:     ///     let file = File::create(\"foo.txt\")?;\n   274:     ///\n   275:     ///     // We now write at the offset 10.\n   276:     ///     file.write_at(b\"sushi\", 10)?;\n   277:     ///     Ok(())\n   278:     /// }\n   279:     /// ```\n   280:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   281:     fn write_at(&self, buf: &[u8], offset: u64) -> io::Result<usize>;\n   282: \n   283:     /// Like `write_at`, except that it writes from a slice of buffers.\n   284:     ///\n   285:     /// Data is copied from each buffer in order, with the final buffer read\n   286:     /// from possibly being only partially consumed. This method must behave as\n   287:     /// a call to `write_at` with the buffers concatenated would.\n   288:     #[unstable(feature = \"unix_file_vectored_at\", issue = \"89517\")]\n   289:     fn write_vectored_at(&self, bufs: &[io::IoSlice<'_>], offset: u64) -> io::Result<usize> {\n   290:         io::default_write_vectored(|b| self.write_at(b, offset), bufs)\n   291:     }\n   292: \n   293:     /// Attempts to write an entire buffer starting from a given offset.\n   294:     ///\n   295:     /// The offset is relative to the start of the file and thus independent\n   296:     /// from the current cursor.\n   297:     ///",
    "nanvix_source": "   274:     ///\n   275:     /// fn main() -> io::Result<()> {\n   276:     ///     let file = File::create(\"foo.txt\")?;\n   277:     ///\n   278:     ///     // We now write at the offset 10.\n   279:     ///     file.write_at(b\"sushi\", 10)?;\n   280:     ///     Ok(())\n   281:     /// }\n   282:     /// ```\n   283:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   284:     fn write_at(&self, buf: &[u8], offset: u64) -> io::Result<usize>;\n   285: \n   286:     /// Like `write_at`, except that it writes from a slice of buffers.\n   287:     ///\n   288:     /// Data is copied from each buffer in order, with the final buffer read\n   289:     /// from possibly being only partially consumed. This method must behave as\n   290:     /// a call to `write_at` with the buffers concatenated would.\n   291:     #[unstable(feature = \"unix_file_vectored_at\", issue = \"89517\")]\n   292:     fn write_vectored_at(&self, bufs: &[io::IoSlice<'_>], offset: u64) -> io::Result<usize> {\n   293:         io::default_write_vectored(|b| self.write_at(b, offset), bufs)\n   294:     }",
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
