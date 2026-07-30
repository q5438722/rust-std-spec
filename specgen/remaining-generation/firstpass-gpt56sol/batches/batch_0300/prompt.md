For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::Read::read_to_string",
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
      "name": "read_to_string",
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
    "verification_source": "   957:     ///\n   958:     /// # Usage Notes\n   959:     ///\n   960:     /// `read_to_string` attempts to read a source until EOF, but many sources are continuous streams\n   961:     /// that do not send EOF. In these cases, `read_to_string` will block indefinitely. Standard input\n   962:     /// is one such stream which may be finite if piped, but is typically continuous. For example,\n   963:     /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n   964:     /// Reading user input or running programs that remain open indefinitely will never terminate\n   965:     /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n   966:     ///\n   967:     /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n   968:     ///\n   969:     ///[`read`]: Read::read\n   970:     ///\n   971:     /// [`std::fs::read_to_string`]: crate::fs::read_to_string\n   972:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   973:     fn read_to_string(&mut self, buf: &mut String) -> Result<usize> {\n   974:         default_read_to_string(self, buf, None)\n   975:     }\n   976: \n   977:     /// Reads the exact number of bytes required to fill `buf`.\n   978:     ///\n   979:     /// This function reads as many bytes as necessary to completely fill the\n   980:     /// specified buffer `buf`.\n   981:     ///\n   982:     /// *Implementations* of this method can make no assumptions about the contents of `buf` when\n   983:     /// this function is called. It is recommended that implementations only write data to `buf`\n   984:     /// instead of reading its contents. The documentation on [`read`] has a more detailed\n   985:     /// explanation of this subject.\n   986:     ///\n   987:     /// # Errors\n   988:     ///\n   989:     /// If this function encounters an error of the kind",
    "nanvix_source": "   969:     /// `cat file | my-rust-program` will correctly terminate with an `EOF` upon closure of cat.\n   970:     /// Reading user input or running programs that remain open indefinitely will never terminate\n   971:     /// the stream with `EOF` (e.g. `yes | my-rust-program`).\n   972:     ///\n   973:     /// Using `.lines()` with a [`BufReader`] or using [`read`] can provide a better solution\n   974:     ///\n   975:     ///[`read`]: Read::read\n   976:     ///\n   977:     /// [`std::fs::read_to_string`]: crate::fs::read_to_string\n   978:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   979:     fn read_to_string(&mut self, buf: &mut String) -> Result<usize> {\n   980:         default_read_to_string(self, buf, None)\n   981:     }\n   982: \n   983:     /// Reads the exact number of bytes required to fill `buf`.\n   984:     ///\n   985:     /// This function reads as many bytes as necessary to completely fill the\n   986:     /// specified buffer `buf`.\n   987:     ///\n   988:     /// *Implementations* of this method can make no assumptions about the contents of `buf` when\n   989:     /// this function is called. It is recommended that implementations only write data to `buf`",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::read_vectored",
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
      "name": "read_vectored",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "bufs"
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
            "bufs",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
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
                      "id": 2612,
                      "path": "IoSliceMut"
                    }
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
    "verification_source": "   791:     ///     Ok(())\n   792:     /// }\n   793:     /// ```\n   794:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   795:     fn read(&mut self, buf: &mut [u8]) -> Result<usize>;\n   796: \n   797:     /// Like `read`, except that it reads into a slice of buffers.\n   798:     ///\n   799:     /// Data is copied to fill each buffer in order, with the final buffer\n   800:     /// written to possibly being only partially filled. This method must\n   801:     /// behave equivalently to a single call to `read` with concatenated\n   802:     /// buffers.\n   803:     ///\n   804:     /// The default implementation calls `read` with either the first nonempty\n   805:     /// buffer provided, or an empty one if none exists.\n   806:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n   807:     fn read_vectored(&mut self, bufs: &mut [IoSliceMut<'_>]) -> Result<usize> {\n   808:         default_read_vectored(|b| self.read(b), bufs)\n   809:     }\n   810: \n   811:     /// Determines if this `Read`er has an efficient `read_vectored`\n   812:     /// implementation.\n   813:     ///\n   814:     /// If a `Read`er does not override the default `read_vectored`\n   815:     /// implementation, code using it may want to avoid the method all together\n   816:     /// and coalesce writes into a single buffer for higher performance.\n   817:     ///\n   818:     /// The default implementation returns `false`.\n   819:     #[unstable(feature = \"can_vector\", issue = \"69941\")]\n   820:     fn is_read_vectored(&self) -> bool {\n   821:         false\n   822:     }\n   823: ",
    "nanvix_source": "   803:     /// Like `read`, except that it reads into a slice of buffers.\n   804:     ///\n   805:     /// Data is copied to fill each buffer in order, with the final buffer\n   806:     /// written to possibly being only partially filled. This method must\n   807:     /// behave equivalently to a single call to `read` with concatenated\n   808:     /// buffers.\n   809:     ///\n   810:     /// The default implementation calls `read` with either the first nonempty\n   811:     /// buffer provided, or an empty one if none exists.\n   812:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n   813:     fn read_vectored(&mut self, bufs: &mut [IoSliceMut<'_>]) -> Result<usize> {\n   814:         default_read_vectored(|b| self.read(b), bufs)\n   815:     }\n   816: \n   817:     /// Determines if this `Read`er has an efficient `read_vectored`\n   818:     /// implementation.\n   819:     ///\n   820:     /// If a `Read`er does not override the default `read_vectored`\n   821:     /// implementation, code using it may want to avoid the method all together\n   822:     /// and coalesce writes into a single buffer for higher performance.\n   823:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Read::take",
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
      "name": "take",
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
            "limit",
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
                      "generic": "Self"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 4215,
            "path": "Take"
          }
        }
      }
    },
    "verification_source": "  1205:     /// use std::io;\n  1206:     /// use std::io::prelude::*;\n  1207:     /// use std::fs::File;\n  1208:     ///\n  1209:     /// fn main() -> io::Result<()> {\n  1210:     ///     let f = File::open(\"foo.txt\")?;\n  1211:     ///     let mut buffer = [0; 5];\n  1212:     ///\n  1213:     ///     // read at most five bytes\n  1214:     ///     let mut handle = f.take(5);\n  1215:     ///\n  1216:     ///     handle.read(&mut buffer)?;\n  1217:     ///     Ok(())\n  1218:     /// }\n  1219:     /// ```\n  1220:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1221:     fn take(self, limit: u64) -> Take<Self>\n  1222:     where\n  1223:         Self: Sized,\n  1224:     {\n  1225:         Take { inner: self, len: limit, limit }\n  1226:     }\n  1227: \n  1228:     /// Read and return a fixed array of bytes from this source.\n  1229:     ///\n  1230:     /// This function uses an array sized based on a const generic size known at compile time. You\n  1231:     /// can specify the size with turbofish (`reader.read_array::<8>()`), or let type inference\n  1232:     /// determine the number of bytes needed based on how the return value gets used. For instance,\n  1233:     /// this function works well with functions like [`u64::from_le_bytes`] to turn an array of\n  1234:     /// bytes into an integer of the same size.\n  1235:     ///\n  1236:     /// Like `read_exact`, if this function encounters an \"end of file\" before reading the desired\n  1237:     /// number of bytes, it returns an error of the kind [`ErrorKind::UnexpectedEof`].",
    "nanvix_source": "  1217:     ///     let mut buffer = [0; 5];\n  1218:     ///\n  1219:     ///     // read at most five bytes\n  1220:     ///     let mut handle = f.take(5);\n  1221:     ///\n  1222:     ///     handle.read(&mut buffer)?;\n  1223:     ///     Ok(())\n  1224:     /// }\n  1225:     /// ```\n  1226:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1227:     fn take(self, limit: u64) -> Take<Self>\n  1228:     where\n  1229:         Self: Sized,\n  1230:     {\n  1231:         core::io::take(self, limit)\n  1232:     }\n  1233: \n  1234:     /// Read and return a fixed array of bytes from this source.\n  1235:     ///\n  1236:     /// This function uses an array sized based on a const generic size known at compile time. You\n  1237:     /// can specify the size with turbofish (`reader.read_array::<8>()`), or let type inference",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Write::by_ref",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
    "verification_source": "  1986:     ///\n  1987:     /// ```no_run\n  1988:     /// use std::io::Write;\n  1989:     /// use std::fs::File;\n  1990:     ///\n  1991:     /// fn main() -> std::io::Result<()> {\n  1992:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1993:     ///\n  1994:     ///     let reference = buffer.by_ref();\n  1995:     ///\n  1996:     ///     // we can use reference just like our original buffer\n  1997:     ///     reference.write_all(b\"some bytes\")?;\n  1998:     ///     Ok(())\n  1999:     /// }\n  2000:     /// ```\n  2001:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2002:     fn by_ref(&mut self) -> &mut Self\n  2003:     where\n  2004:         Self: Sized,\n  2005:     {\n  2006:         self\n  2007:     }\n  2008: }\n  2009: \n  2010: /// The `Seek` trait provides a cursor which can be moved within a stream of\n  2011: /// bytes.\n  2012: ///\n  2013: /// The stream typically has a fixed size, allowing seeking relative to either\n  2014: /// end or the current offset.\n  2015: ///\n  2016: /// # Examples\n  2017: ///\n  2018: /// [`File`]s implement `Seek`:",
    "nanvix_source": "  1747:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1748:     ///\n  1749:     ///     let reference = buffer.by_ref();\n  1750:     ///\n  1751:     ///     // we can use reference just like our original buffer\n  1752:     ///     reference.write_all(b\"some bytes\")?;\n  1753:     ///     Ok(())\n  1754:     /// }\n  1755:     /// ```\n  1756:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1757:     fn by_ref(&mut self) -> &mut Self\n  1758:     where\n  1759:         Self: Sized,\n  1760:     {\n  1761:         self\n  1762:     }\n  1763: }\n  1764: \n  1765: fn read_until<R: BufRead + ?Sized>(r: &mut R, delim: u8, buf: &mut Vec<u8>) -> Result<usize> {\n  1766:     let mut read = 0;\n  1767:     loop {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Write::flush",
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
      "name": "flush",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
    "verification_source": "  1807:     /// # Examples\n  1808:     ///\n  1809:     /// ```no_run\n  1810:     /// use std::io::prelude::*;\n  1811:     /// use std::io::BufWriter;\n  1812:     /// use std::fs::File;\n  1813:     ///\n  1814:     /// fn main() -> std::io::Result<()> {\n  1815:     ///     let mut buffer = BufWriter::new(File::create(\"foo.txt\")?);\n  1816:     ///\n  1817:     ///     buffer.write_all(b\"some bytes\")?;\n  1818:     ///     buffer.flush()?;\n  1819:     ///     Ok(())\n  1820:     /// }\n  1821:     /// ```\n  1822:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1823:     fn flush(&mut self) -> Result<()>;\n  1824: \n  1825:     /// Attempts to write an entire buffer into this writer.\n  1826:     ///\n  1827:     /// This method will continuously call [`write`] until there is no more data\n  1828:     /// to be written or an error of non-[`ErrorKind::Interrupted`] kind is\n  1829:     /// returned. This method will not return until the entire buffer has been\n  1830:     /// successfully written or such an error occurs. The first error that is\n  1831:     /// not of [`ErrorKind::Interrupted`] kind generated from this method will be\n  1832:     /// returned.\n  1833:     ///\n  1834:     /// If the buffer contains no data, this will never call [`write`].\n  1835:     ///\n  1836:     /// # Errors\n  1837:     ///\n  1838:     /// This function will return the first error of\n  1839:     /// non-[`ErrorKind::Interrupted`] kind that [`write`] returns.",
    "nanvix_source": "  1568:     ///\n  1569:     /// fn main() -> std::io::Result<()> {\n  1570:     ///     let mut buffer = BufWriter::new(File::create(\"foo.txt\")?);\n  1571:     ///\n  1572:     ///     buffer.write_all(b\"some bytes\")?;\n  1573:     ///     buffer.flush()?;\n  1574:     ///     Ok(())\n  1575:     /// }\n  1576:     /// ```\n  1577:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1578:     fn flush(&mut self) -> Result<()>;\n  1579: \n  1580:     /// Attempts to write an entire buffer into this writer.\n  1581:     ///\n  1582:     /// This method will continuously call [`write`] until there is no more data\n  1583:     /// to be written or an error of non-[`ErrorKind::Interrupted`] kind is\n  1584:     /// returned. This method will not return until the entire buffer has been\n  1585:     /// successfully written or such an error occurs. The first error that is\n  1586:     /// not of [`ErrorKind::Interrupted`] kind generated from this method will be\n  1587:     /// returned.\n  1588:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Write::write",
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
      "name": "write",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
    "verification_source": "  1730:     ///\n  1731:     /// ```no_run\n  1732:     /// use std::io::prelude::*;\n  1733:     /// use std::fs::File;\n  1734:     ///\n  1735:     /// fn main() -> std::io::Result<()> {\n  1736:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1737:     ///\n  1738:     ///     // Writes some prefix of the byte string, not necessarily all of it.\n  1739:     ///     buffer.write(b\"some bytes\")?;\n  1740:     ///     Ok(())\n  1741:     /// }\n  1742:     /// ```\n  1743:     ///\n  1744:     /// [`Ok(n)`]: Ok\n  1745:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1746:     fn write(&mut self, buf: &[u8]) -> Result<usize>;\n  1747: \n  1748:     /// Like [`write`], except that it writes from a slice of buffers.\n  1749:     ///\n  1750:     /// Data is copied from each buffer in order, with the final buffer\n  1751:     /// read from possibly being only partially consumed. This method must\n  1752:     /// behave as a call to [`write`] with the buffers concatenated would.\n  1753:     ///\n  1754:     /// The default implementation calls [`write`] with either the first nonempty\n  1755:     /// buffer provided, or an empty one if none exists.\n  1756:     ///\n  1757:     /// # Examples\n  1758:     ///\n  1759:     /// ```no_run\n  1760:     /// use std::io::IoSlice;\n  1761:     /// use std::io::prelude::*;\n  1762:     /// use std::fs::File;",
    "nanvix_source": "  1491:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1492:     ///\n  1493:     ///     // Writes some prefix of the byte string, not necessarily all of it.\n  1494:     ///     buffer.write(b\"some bytes\")?;\n  1495:     ///     Ok(())\n  1496:     /// }\n  1497:     /// ```\n  1498:     ///\n  1499:     /// [`Ok(n)`]: Ok\n  1500:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1501:     fn write(&mut self, buf: &[u8]) -> Result<usize>;\n  1502: \n  1503:     /// Like [`write`], except that it writes from a slice of buffers.\n  1504:     ///\n  1505:     /// Data is copied from each buffer in order, with the final buffer\n  1506:     /// read from possibly being only partially consumed. This method must\n  1507:     /// behave as a call to [`write`] with the buffers concatenated would.\n  1508:     ///\n  1509:     /// The default implementation calls [`write`] with either the first nonempty\n  1510:     /// buffer provided, or an empty one if none exists.\n  1511:     ///",
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
