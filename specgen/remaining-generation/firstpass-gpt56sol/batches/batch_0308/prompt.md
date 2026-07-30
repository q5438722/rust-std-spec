For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::PermissionsExt::set_mode",
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
      "unit_return_variant"
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
      "name": "set_mode",
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
        "item_id": "std:3026",
        "kind": "trait",
        "name": "PermissionsExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "PermissionsExt"
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
        "output": null
      }
    },
    "verification_source": "   432: /// let mut permissions = Permissions::from_mode(my_mode);\n   433: /// assert_eq!(permissions.mode(), my_mode);\n   434: ///\n   435: /// // read/write/execute for owner\n   436: /// let other_mode = 0o700;\n   437: /// permissions.set_mode(other_mode);\n   438: /// assert_eq!(permissions.mode(), other_mode);\n   439: /// ```\n   440: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   441: pub trait PermissionsExt {\n   442:     /// Returns the mode permission bits\n   443:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   444:     fn mode(&self) -> u32;\n   445: \n   446:     /// Sets the mode permission bits.\n   447:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   448:     fn set_mode(&mut self, mode: u32);\n   449: \n   450:     /// Creates a new instance from the given mode permission bits.\n   451:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   452:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   453:     fn from_mode(mode: u32) -> Self;\n   454: }\n   455: \n   456: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   457: impl PermissionsExt for Permissions {\n   458:     fn mode(&self) -> u32 {\n   459:         self.as_inner().mode()\n   460:     }\n   461: \n   462:     fn set_mode(&mut self, mode: u32) {\n   463:         *self = Permissions::from_inner(FromInner::from_inner(mode));\n   464:     }",
    "nanvix_source": "   441: /// assert_eq!(permissions.mode(), other_mode);\n   442: /// ```\n   443: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   444: pub trait PermissionsExt {\n   445:     /// Returns the mode permission bits\n   446:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   447:     fn mode(&self) -> u32;\n   448: \n   449:     /// Sets the mode permission bits.\n   450:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   451:     fn set_mode(&mut self, mode: u32);\n   452: \n   453:     /// Creates a new instance from the given mode permission bits.\n   454:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   455:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   456:     fn from_mode(mode: u32) -> Self;\n   457: }\n   458: \n   459: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   460: impl PermissionsExt for Permissions {\n   461:     fn mode(&self) -> u32 {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::ffi::OsStrExt::encode_wide",
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
      "name": "encode_wide",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2400",
        "kind": "trait",
        "name": "OsStrExt",
        "path": [
          "std",
          "os",
          "windows",
          "ffi",
          "OsStrExt"
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
            "id": 2398,
            "path": "EncodeWide"
          }
        }
      }
    },
    "verification_source": "   108:     /// This is lossless: calling [`OsStringExt::from_wide`] and then\n   109:     /// `encode_wide` on the result will yield the original code units.\n   110:     /// Note that the encoding does not add a final null terminator.\n   111:     ///\n   112:     /// # Examples\n   113:     ///\n   114:     /// ```\n   115:     /// use std::ffi::OsString;\n   116:     /// use std::os::windows::prelude::*;\n   117:     ///\n   118:     /// // UTF-16 encoding for \"Unicode\".\n   119:     /// let source = [0x0055, 0x006E, 0x0069, 0x0063, 0x006F, 0x0064, 0x0065];\n   120:     ///\n   121:     /// let string = OsString::from_wide(&source[..]);\n   122:     ///\n   123:     /// let result: Vec<u16> = string.encode_wide().collect();\n   124:     /// assert_eq!(&source[..], &result[..]);\n   125:     /// ```\n   126:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   127:     fn encode_wide(&self) -> EncodeWide<'_>;\n   128: }\n   129: \n   130: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   131: impl OsStrExt for OsStr {\n   132:     #[inline]\n   133:     fn encode_wide(&self) -> EncodeWide<'_> {\n   134:         EncodeWide { inner: self.as_inner().inner.encode_wide() }\n   135:     }\n   136: }\n   137: \n   138: /// Iterator returned by [`OsStrExt::encode_wide`].\n   139: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   140: #[derive(Clone)]",
    "nanvix_source": "   107:     /// ```\n   108:     /// use std::ffi::OsString;\n   109:     /// use std::os::windows::prelude::*;\n   110:     ///\n   111:     /// // UTF-16 encoding for \"Unicode\".\n   112:     /// let source = [0x0055, 0x006E, 0x0069, 0x0063, 0x006F, 0x0064, 0x0065];\n   113:     ///\n   114:     /// let string = OsString::from_wide(&source[..]);\n   115:     ///\n   116:     /// let result: Vec<u16> = string.encode_wide().collect();\n   117:     /// assert_eq!(&source[..], &result[..]);\n   118:     /// ```\n   119:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   120:     fn encode_wide(&self) -> EncodeWide<'_>;\n   121: }\n   122: \n   123: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124: impl OsStrExt for OsStr {\n   125:     #[inline]\n   126:     fn encode_wide(&self) -> EncodeWide<'_> {\n   127:         EncodeWide { inner: self.as_inner().inner.encode_wide() }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::ffi::OsStringExt::from_wide",
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
      "name": "from_wide",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2239",
        "kind": "trait",
        "name": "OsStringExt",
        "path": [
          "std",
          "os",
          "windows",
          "ffi",
          "OsStringExt"
        ]
      },
      "signature": {
        "inputs": [
          [
            "wide",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u16"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "    73:     ///\n    74:     /// This is lossless: calling [`OsStrExt::encode_wide`] on the resulting string\n    75:     /// will always return the original code units.\n    76:     ///\n    77:     /// # Examples\n    78:     ///\n    79:     /// ```\n    80:     /// use std::ffi::OsString;\n    81:     /// use std::os::windows::prelude::*;\n    82:     ///\n    83:     /// // UTF-16 encoding for \"Unicode\".\n    84:     /// let source = [0x0055, 0x006E, 0x0069, 0x0063, 0x006F, 0x0064, 0x0065];\n    85:     ///\n    86:     /// let string = OsString::from_wide(&source[..]);\n    87:     /// ```\n    88:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    89:     fn from_wide(wide: &[u16]) -> Self;\n    90: }\n    91: \n    92: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    93: impl OsStringExt for OsString {\n    94:     fn from_wide(wide: &[u16]) -> OsString {\n    95:         FromInner::from_inner(Buf { inner: Wtf8Buf::from_wide(wide) })\n    96:     }\n    97: }\n    98: \n    99: /// Windows-specific extensions to [`OsStr`].\n   100: ///\n   101: /// This trait is sealed: it cannot be implemented outside the standard library.\n   102: /// This is so that future additional methods are not breaking changes.\n   103: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   104: pub trait OsStrExt: Sealed {\n   105:     /// Re-encodes an `OsStr` as a wide character sequence, i.e., potentially",
    "nanvix_source": "    75:     /// ```\n    76:     /// use std::ffi::OsString;\n    77:     /// use std::os::windows::prelude::*;\n    78:     ///\n    79:     /// // UTF-16 encoding for \"Unicode\".\n    80:     /// let source = [0x0055, 0x006E, 0x0069, 0x0063, 0x006F, 0x0064, 0x0065];\n    81:     ///\n    82:     /// let string = OsString::from_wide(&source[..]);\n    83:     /// ```\n    84:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    85:     fn from_wide(wide: &[u16]) -> Self;\n    86: }\n    87: \n    88: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    89: impl OsStringExt for OsString {\n    90:     fn from_wide(wide: &[u16]) -> OsString {\n    91:         FromInner::from_inner(Buf { inner: Wtf8Buf::from_wide(wide) })\n    92:     }\n    93: }\n    94: \n    95: /// Windows-specific extensions to [`OsStr`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::FileExt::seek_read",
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
      "name": "seek_read",
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
        "item_id": "std:2673",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "    35:     /// ```no_run\n    36:     /// use std::io;\n    37:     /// use std::fs::File;\n    38:     /// use std::os::windows::prelude::*;\n    39:     ///\n    40:     /// fn main() -> io::Result<()> {\n    41:     ///     let mut file = File::open(\"foo.txt\")?;\n    42:     ///     let mut buffer = [0; 10];\n    43:     ///\n    44:     ///     // Read 10 bytes, starting 72 bytes from the\n    45:     ///     // start of the file.\n    46:     ///     file.seek_read(&mut buffer[..], 72)?;\n    47:     ///     Ok(())\n    48:     /// }\n    49:     /// ```\n    50:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n    51:     fn seek_read(&self, buf: &mut [u8], offset: u64) -> io::Result<usize>;\n    52: \n    53:     /// Seeks to a given position and reads some bytes into the buffer.\n    54:     ///\n    55:     /// This is equivalent to the [`seek_read`](FileExt::seek_read) method, except that it is passed\n    56:     /// a [`BorrowedCursor`] rather than `&mut [u8]` to allow use with uninitialized buffers. The\n    57:     /// new data will be appended to any existing contents of `buf`.\n    58:     ///\n    59:     /// Reading beyond the end of the file will always succeed without reading any bytes.\n    60:     ///\n    61:     /// # Examples\n    62:     ///\n    63:     /// ```no_run\n    64:     /// #![feature(core_io_borrowed_buf)]\n    65:     /// #![feature(read_buf_at)]\n    66:     ///\n    67:     /// use std::io;",
    "nanvix_source": "    40:     ///     let mut file = File::open(\"foo.txt\")?;\n    41:     ///     let mut buffer = [0; 10];\n    42:     ///\n    43:     ///     // Read 10 bytes, starting 72 bytes from the\n    44:     ///     // start of the file.\n    45:     ///     file.seek_read(&mut buffer[..], 72)?;\n    46:     ///     Ok(())\n    47:     /// }\n    48:     /// ```\n    49:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n    50:     fn seek_read(&self, buf: &mut [u8], offset: u64) -> io::Result<usize>;\n    51: \n    52:     /// Seeks to a given position and reads some bytes into the buffer.\n    53:     ///\n    54:     /// This is equivalent to the [`seek_read`](FileExt::seek_read) method, except that it is passed\n    55:     /// a [`BorrowedCursor`] rather than `&mut [u8]` to allow use with uninitialized buffers. The\n    56:     /// new data will be appended to any existing contents of `buf`.\n    57:     ///\n    58:     /// Reading beyond the end of the file will always succeed without reading any bytes.\n    59:     ///\n    60:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::FileExt::seek_write",
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
      "name": "seek_write",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2673",
        "kind": "trait",
        "name": "FileExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   106:     /// # Examples\n   107:     ///\n   108:     /// ```no_run\n   109:     /// use std::fs::File;\n   110:     /// use std::os::windows::prelude::*;\n   111:     ///\n   112:     /// fn main() -> std::io::Result<()> {\n   113:     ///     let mut buffer = File::create(\"foo.txt\")?;\n   114:     ///\n   115:     ///     // Write a byte string starting 72 bytes from\n   116:     ///     // the start of the file.\n   117:     ///     buffer.seek_write(b\"some bytes\", 72)?;\n   118:     ///     Ok(())\n   119:     /// }\n   120:     /// ```\n   121:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   122:     fn seek_write(&self, buf: &[u8], offset: u64) -> io::Result<usize>;\n   123: }\n   124: \n   125: #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   126: impl FileExt for fs::File {\n   127:     fn seek_read(&self, buf: &mut [u8], offset: u64) -> io::Result<usize> {\n   128:         self.as_inner().read_at(buf, offset)\n   129:     }\n   130: \n   131:     fn seek_read_buf(&self, buf: BorrowedCursor<'_>, offset: u64) -> io::Result<()> {\n   132:         self.as_inner().read_buf_at(buf, offset)\n   133:     }\n   134: \n   135:     fn seek_write(&self, buf: &[u8], offset: u64) -> io::Result<usize> {\n   136:         self.as_inner().write_at(buf, offset)\n   137:     }\n   138: }",
    "nanvix_source": "   111:     /// fn main() -> std::io::Result<()> {\n   112:     ///     let mut buffer = File::create(\"foo.txt\")?;\n   113:     ///\n   114:     ///     // Write a byte string starting 72 bytes from\n   115:     ///     // the start of the file.\n   116:     ///     buffer.seek_write(b\"some bytes\", 72)?;\n   117:     ///     Ok(())\n   118:     /// }\n   119:     /// ```\n   120:     #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   121:     fn seek_write(&self, buf: &[u8], offset: u64) -> io::Result<usize>;\n   122: }\n   123: \n   124: #[stable(feature = \"file_offset\", since = \"1.15.0\")]\n   125: impl FileExt for fs::File {\n   126:     fn seek_read(&self, buf: &mut [u8], offset: u64) -> io::Result<usize> {\n   127:         self.as_inner().read_at(buf, offset)\n   128:     }\n   129: \n   130:     fn seek_read_buf(&self, buf: BorrowedCursor<'_, u8>, offset: u64) -> io::Result<()> {\n   131:         self.as_inner().read_buf_at(buf, offset)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::FileTimesExt::set_created",
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
      "name": "set_created",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3023",
        "kind": "trait",
        "name": "FileTimesExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "FileTimesExt"
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
            "t",
            {
              "resolved_path": {
                "args": null,
                "id": 2591,
                "path": "SystemTime"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   608: \n   609: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   610: impl FileTypeExt for fs::FileType {\n   611:     fn is_symlink_dir(&self) -> bool {\n   612:         self.as_inner().is_symlink_dir()\n   613:     }\n   614:     fn is_symlink_file(&self) -> bool {\n   615:         self.as_inner().is_symlink_file()\n   616:     }\n   617: }\n   618: \n   619: /// Windows-specific extensions to [`fs::FileTimes`].\n   620: #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   621: pub trait FileTimesExt: Sealed {\n   622:     /// Set the creation time of a file.\n   623:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   624:     fn set_created(self, t: SystemTime) -> Self;\n   625: }\n   626: \n   627: #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   628: impl FileTimesExt for fs::FileTimes {\n   629:     fn set_created(mut self, t: SystemTime) -> Self {\n   630:         self.as_inner_mut().set_created(t.into_inner());\n   631:         self\n   632:     }\n   633: }\n   634: \n   635: /// Creates a new symlink to a non-directory file on the filesystem.\n   636: ///\n   637: /// The `link` path will be a file symbolic link pointing to the `original`\n   638: /// path.\n   639: ///\n   640: /// The `original` path should not be a directory or a symlink to a directory,",
    "nanvix_source": "   666:     fn is_symlink_file(&self) -> bool {\n   667:         self.as_inner().is_symlink_file()\n   668:     }\n   669: }\n   670: \n   671: /// Windows-specific extensions to [`fs::FileTimes`].\n   672: #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   673: pub impl(self) trait FileTimesExt {\n   674:     /// Set the creation time of a file.\n   675:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   676:     fn set_created(self, t: SystemTime) -> Self;\n   677: }\n   678: \n   679: #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n   680: impl FileTimesExt for fs::FileTimes {\n   681:     fn set_created(mut self, t: SystemTime) -> Self {\n   682:         self.as_inner_mut().set_created(t.into_inner());\n   683:         self\n   684:     }\n   685: }\n   686: ",
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
