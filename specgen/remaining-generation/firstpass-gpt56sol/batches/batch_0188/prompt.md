For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::File::lock",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "lock",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
    "verification_source": "   850:     /// [`unlock`]: File::unlock\n   851:     /// [`read`]: Read::read\n   852:     /// [`write`]: Write::write\n   853:     ///\n   854:     /// # Examples\n   855:     ///\n   856:     /// ```no_run\n   857:     /// use std::fs::File;\n   858:     ///\n   859:     /// fn main() -> std::io::Result<()> {\n   860:     ///     let f = File::create(\"foo.txt\")?;\n   861:     ///     f.lock()?;\n   862:     ///     Ok(())\n   863:     /// }\n   864:     /// ```\n   865:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   866:     pub fn lock(&self) -> io::Result<()> {\n   867:         self.inner.lock()\n   868:     }\n   869: \n   870:     /// Acquire a shared (non-exclusive) lock on the file. Blocks until the lock can be acquired.\n   871:     ///\n   872:     /// This acquires a shared lock; more than one file handle, in this or any other process, may\n   873:     /// hold a shared lock, but none may hold an exclusive lock at the same time.\n   874:     ///\n   875:     /// This lock may be advisory or mandatory. This lock is meant to interact with [`lock`],\n   876:     /// [`try_lock`], [`lock_shared`], [`try_lock_shared`], and [`unlock`]. Its interactions with\n   877:     /// other methods, such as [`read`] and [`write`] are platform specific, and it may or may not\n   878:     /// cause non-lockholders to block.\n   879:     ///\n   880:     /// If this file handle/descriptor, or a clone of it, already holds a lock, the exact behavior\n   881:     /// is unspecified and platform dependent, including the possibility that it will deadlock.\n   882:     /// However, if this method returns, then a shared lock is held.",
    "nanvix_source": "   854:     /// ```no_run\n   855:     /// use std::fs::File;\n   856:     ///\n   857:     /// fn main() -> std::io::Result<()> {\n   858:     ///     let f = File::create(\"foo.txt\")?;\n   859:     ///     f.lock()?;\n   860:     ///     Ok(())\n   861:     /// }\n   862:     /// ```\n   863:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   864:     pub fn lock(&self) -> io::Result<()> {\n   865:         self.inner.lock()\n   866:     }\n   867: \n   868:     /// Acquire a shared (non-exclusive) lock on the file. Blocks until the lock can be acquired.\n   869:     ///\n   870:     /// This acquires a shared lock. More than one file handle to this file, in this or any other\n   871:     /// process, may hold a shared lock, but no *other* file handle may hold an exclusive lock at\n   872:     /// the same time.\n   873:     /// If this file handle/descriptor, or a clone of it, already holds a lock, the exact\n   874:     /// behavior is unspecified and platform dependent, including the possibility that it will",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::lock_shared",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "lock_shared",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
    "verification_source": "   902:     /// [`unlock`]: File::unlock\n   903:     /// [`read`]: Read::read\n   904:     /// [`write`]: Write::write\n   905:     ///\n   906:     /// # Examples\n   907:     ///\n   908:     /// ```no_run\n   909:     /// use std::fs::File;\n   910:     ///\n   911:     /// fn main() -> std::io::Result<()> {\n   912:     ///     let f = File::open(\"foo.txt\")?;\n   913:     ///     f.lock_shared()?;\n   914:     ///     Ok(())\n   915:     /// }\n   916:     /// ```\n   917:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   918:     pub fn lock_shared(&self) -> io::Result<()> {\n   919:         self.inner.lock_shared()\n   920:     }\n   921: \n   922:     /// Try to acquire an exclusive lock on the file.\n   923:     ///\n   924:     /// Returns `Err(TryLockError::WouldBlock)` if a different lock is already held on this file\n   925:     /// (via another handle/descriptor).\n   926:     ///\n   927:     /// This acquires an exclusive lock; no other file handle to this file, in this or any other\n   928:     /// process, may acquire another lock.\n   929:     ///\n   930:     /// This lock may be advisory or mandatory. This lock is meant to interact with [`lock`],\n   931:     /// [`try_lock`], [`lock_shared`], [`try_lock_shared`], and [`unlock`]. Its interactions with\n   932:     /// other methods, such as [`read`] and [`write`] are platform specific, and it may or may not\n   933:     /// cause non-lockholders to block.\n   934:     ///",
    "nanvix_source": "   906:     /// ```no_run\n   907:     /// use std::fs::File;\n   908:     ///\n   909:     /// fn main() -> std::io::Result<()> {\n   910:     ///     let f = File::open(\"foo.txt\")?;\n   911:     ///     f.lock_shared()?;\n   912:     ///     Ok(())\n   913:     /// }\n   914:     /// ```\n   915:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   916:     pub fn lock_shared(&self) -> io::Result<()> {\n   917:         self.inner.lock_shared()\n   918:     }\n   919: \n   920:     /// Try to acquire an exclusive lock on the file.\n   921:     ///\n   922:     /// Returns `Err(TryLockError::WouldBlock)` if a different lock is already held on this file\n   923:     /// (via another handle/descriptor).\n   924:     ///\n   925:     /// This acquires an exclusive lock; no other file handle to this file, in this or any other\n   926:     /// process, may acquire another lock.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::metadata",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "metadata",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 2584,
                        "path": "Metadata"
                      }
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
    "verification_source": "  1124:     }\n  1125: \n  1126:     /// Queries metadata about the underlying file.\n  1127:     ///\n  1128:     /// # Examples\n  1129:     ///\n  1130:     /// ```no_run\n  1131:     /// use std::fs::File;\n  1132:     ///\n  1133:     /// fn main() -> std::io::Result<()> {\n  1134:     ///     let mut f = File::open(\"foo.txt\")?;\n  1135:     ///     let metadata = f.metadata()?;\n  1136:     ///     Ok(())\n  1137:     /// }\n  1138:     /// ```\n  1139:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1140:     pub fn metadata(&self) -> io::Result<Metadata> {\n  1141:         self.inner.file_attr().map(Metadata)\n  1142:     }\n  1143: \n  1144:     /// Creates a new `File` instance that shares the same underlying file handle\n  1145:     /// as the existing `File` instance. Reads, writes, and seeks will affect\n  1146:     /// both `File` instances simultaneously.\n  1147:     ///\n  1148:     /// # Examples\n  1149:     ///\n  1150:     /// Creates two handles for a file named `foo.txt`:\n  1151:     ///\n  1152:     /// ```no_run\n  1153:     /// use std::fs::File;\n  1154:     ///\n  1155:     /// fn main() -> std::io::Result<()> {\n  1156:     ///     let mut file = File::open(\"foo.txt\")?;",
    "nanvix_source": "  1128:     /// ```no_run\n  1129:     /// use std::fs::File;\n  1130:     ///\n  1131:     /// fn main() -> std::io::Result<()> {\n  1132:     ///     let mut f = File::open(\"foo.txt\")?;\n  1133:     ///     let metadata = f.metadata()?;\n  1134:     ///     Ok(())\n  1135:     /// }\n  1136:     /// ```\n  1137:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1138:     pub fn metadata(&self) -> io::Result<Metadata> {\n  1139:         self.inner.file_attr().map(Metadata)\n  1140:     }\n  1141: \n  1142:     /// Creates a new `File` instance that shares the same underlying file handle\n  1143:     /// as the existing `File` instance. Reads, writes, and seeks will affect\n  1144:     /// both `File` instances simultaneously.\n  1145:     ///\n  1146:     /// # Examples\n  1147:     ///\n  1148:     /// Creates two handles for a file named `foo.txt`:",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::open",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
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
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 1802,
                                    "path": "Path"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 40,
                        "path": "AsRef"
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
      "name": "open",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "path",
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
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 2556,
                        "path": "File"
                      }
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
    "verification_source": "   554:     /// Other errors may also be returned according to [`OpenOptions::open`].\n   555:     ///\n   556:     /// # Examples\n   557:     ///\n   558:     /// ```no_run\n   559:     /// use std::fs::File;\n   560:     /// use std::io::Read;\n   561:     ///\n   562:     /// fn main() -> std::io::Result<()> {\n   563:     ///     let mut f = File::open(\"foo.txt\")?;\n   564:     ///     let mut data = vec![];\n   565:     ///     f.read_to_end(&mut data)?;\n   566:     ///     Ok(())\n   567:     /// }\n   568:     /// ```\n   569:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   570:     pub fn open<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   571:         OpenOptions::new().read(true).open(path.as_ref())\n   572:     }\n   573: \n   574:     /// Attempts to open a file in read-only mode with buffering.\n   575:     ///\n   576:     /// See the [`OpenOptions::open`] method, the [`BufReader`][io::BufReader] type,\n   577:     /// and the [`BufRead`][io::BufRead] trait for more details.\n   578:     ///\n   579:     /// If you only need to read the entire file contents,\n   580:     /// consider [`std::fs::read()`][self::read] or\n   581:     /// [`std::fs::read_to_string()`][self::read_to_string] instead.\n   582:     ///\n   583:     /// # Errors\n   584:     ///\n   585:     /// This function will return an error if `path` does not already exist,\n   586:     /// or if memory allocation fails for the new buffer.",
    "nanvix_source": "   559:     /// use std::io::Read;\n   560:     ///\n   561:     /// fn main() -> std::io::Result<()> {\n   562:     ///     let mut f = File::open(\"foo.txt\")?;\n   563:     ///     let mut data = vec![];\n   564:     ///     f.read_to_end(&mut data)?;\n   565:     ///     Ok(())\n   566:     /// }\n   567:     /// ```\n   568:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   569:     pub fn open<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   570:         OpenOptions::new().read(true).open(path.as_ref())\n   571:     }\n   572: \n   573:     /// Attempts to open a file in read-only mode with buffering.\n   574:     ///\n   575:     /// See the [`OpenOptions::open`] method, the [`BufReader`][io::BufReader] type,\n   576:     /// and the [`BufRead`][io::BufRead] trait for more details.\n   577:     ///\n   578:     /// If you only need to read the entire file contents,\n   579:     /// consider [`std::fs::read()`][self::read] or",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::options",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "options",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 2571,
            "path": "OpenOptions"
          }
        }
      }
    },
    "verification_source": "   729:     ///\n   730:     /// # Examples\n   731:     ///\n   732:     /// ```no_run\n   733:     /// use std::fs::File;\n   734:     /// use std::io::Write;\n   735:     ///\n   736:     /// fn main() -> std::io::Result<()> {\n   737:     ///     let mut f = File::options().append(true).open(\"example.log\")?;\n   738:     ///     writeln!(&mut f, \"new line\")?;\n   739:     ///     Ok(())\n   740:     /// }\n   741:     /// ```\n   742:     #[must_use]\n   743:     #[stable(feature = \"with_options\", since = \"1.58.0\")]\n   744:     #[cfg_attr(not(test), rustc_diagnostic_item = \"file_options\")]\n   745:     pub fn options() -> OpenOptions {\n   746:         OpenOptions::new()\n   747:     }\n   748: \n   749:     /// Attempts to sync all OS-internal file content and metadata to disk.\n   750:     ///\n   751:     /// This function will attempt to ensure that all in-memory data reaches the\n   752:     /// filesystem before returning.\n   753:     ///\n   754:     /// This can be used to handle errors that would otherwise only be caught\n   755:     /// when the `File` is closed, as dropping a `File` will ignore all errors.\n   756:     /// Note, however, that `sync_all` is generally more expensive than closing\n   757:     /// a file by dropping it, because the latter is not required to block until\n   758:     /// the data has been written to the filesystem.\n   759:     ///\n   760:     /// If synchronizing the metadata is not required, use [`sync_data`] instead.\n   761:     ///",
    "nanvix_source": "   734:     ///\n   735:     /// fn main() -> std::io::Result<()> {\n   736:     ///     let mut f = File::options().append(true).open(\"example.log\")?;\n   737:     ///     writeln!(&mut f, \"new line\")?;\n   738:     ///     Ok(())\n   739:     /// }\n   740:     /// ```\n   741:     #[must_use]\n   742:     #[stable(feature = \"with_options\", since = \"1.58.0\")]\n   743:     #[cfg_attr(not(test), rustc_diagnostic_item = \"file_options\")]\n   744:     pub fn options() -> OpenOptions {\n   745:         OpenOptions::new()\n   746:     }\n   747: \n   748:     /// Attempts to sync all OS-internal file content and metadata to disk.\n   749:     ///\n   750:     /// This function will attempt to ensure that all in-memory data reaches the\n   751:     /// filesystem before returning.\n   752:     ///\n   753:     /// This can be used to handle errors that would otherwise only be caught\n   754:     /// when the `File` is closed, as dropping a `File` will ignore all errors.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::set_len",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "set_len",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
          ],
          [
            "size",
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
    "verification_source": "  1106:     ///\n  1107:     /// # Examples\n  1108:     ///\n  1109:     /// ```no_run\n  1110:     /// use std::fs::File;\n  1111:     ///\n  1112:     /// fn main() -> std::io::Result<()> {\n  1113:     ///     let mut f = File::create(\"foo.txt\")?;\n  1114:     ///     f.set_len(10)?;\n  1115:     ///     Ok(())\n  1116:     /// }\n  1117:     /// ```\n  1118:     ///\n  1119:     /// Note that this method alters the content of the underlying file, even\n  1120:     /// though it takes `&self` rather than `&mut self`.\n  1121:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1122:     pub fn set_len(&self, size: u64) -> io::Result<()> {\n  1123:         self.inner.truncate(size)\n  1124:     }\n  1125: \n  1126:     /// Queries metadata about the underlying file.\n  1127:     ///\n  1128:     /// # Examples\n  1129:     ///\n  1130:     /// ```no_run\n  1131:     /// use std::fs::File;\n  1132:     ///\n  1133:     /// fn main() -> std::io::Result<()> {\n  1134:     ///     let mut f = File::open(\"foo.txt\")?;\n  1135:     ///     let metadata = f.metadata()?;\n  1136:     ///     Ok(())\n  1137:     /// }\n  1138:     /// ```",
    "nanvix_source": "  1110:     /// fn main() -> std::io::Result<()> {\n  1111:     ///     let mut f = File::create(\"foo.txt\")?;\n  1112:     ///     f.set_len(10)?;\n  1113:     ///     Ok(())\n  1114:     /// }\n  1115:     /// ```\n  1116:     ///\n  1117:     /// Note that this method alters the content of the underlying file, even\n  1118:     /// though it takes `&self` rather than `&mut self`.\n  1119:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1120:     pub fn set_len(&self, size: u64) -> io::Result<()> {\n  1121:         self.inner.truncate(size)\n  1122:     }\n  1123: \n  1124:     /// Queries metadata about the underlying file.\n  1125:     ///\n  1126:     /// # Examples\n  1127:     ///\n  1128:     /// ```no_run\n  1129:     /// use std::fs::File;\n  1130:     ///",
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
