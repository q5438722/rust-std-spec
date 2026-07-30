For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::fchown",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
                        "args": null,
                        "id": 2700,
                        "path": "AsFd"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
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
      "name": "fchown",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "fd",
            {
              "generic": "F"
            }
          ],
          [
            "uid",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u32"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
              }
            }
          ],
          [
            "gid",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u32"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
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
    "verification_source": "  1126: /// Change the owner and group of the file referenced by the specified open file descriptor.\n  1127: ///\n  1128: /// For semantics and required privileges, see [`chown`].\n  1129: ///\n  1130: /// # Examples\n  1131: ///\n  1132: /// ```no_run\n  1133: /// use std::os::unix::fs;\n  1134: ///\n  1135: /// fn main() -> std::io::Result<()> {\n  1136: ///     let f = std::fs::File::open(\"/file\")?;\n  1137: ///     fs::fchown(&f, Some(0), Some(0))?;\n  1138: ///     Ok(())\n  1139: /// }\n  1140: /// ```\n  1141: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1142: pub fn fchown<F: AsFd>(fd: F, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1143:     sys::fs::fchown(fd.as_fd().as_raw_fd(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1144: }\n  1145: \n  1146: /// Change the owner and group of the specified path, without dereferencing symbolic links.\n  1147: ///\n  1148: /// Identical to [`chown`], except that if called on a symbolic link, this will change the owner\n  1149: /// and group of the link itself rather than the owner and group of the link target.\n  1150: ///\n  1151: /// # Examples\n  1152: ///\n  1153: /// ```no_run\n  1154: /// use std::os::unix::fs;\n  1155: ///\n  1156: /// fn main() -> std::io::Result<()> {\n  1157: ///     fs::lchown(\"/symlink\", Some(0), Some(0))?;\n  1158: ///     Ok(())",
    "nanvix_source": "  1131: /// ```no_run\n  1132: /// use std::os::unix::fs;\n  1133: ///\n  1134: /// fn main() -> std::io::Result<()> {\n  1135: ///     let f = std::fs::File::open(\"/file\")?;\n  1136: ///     fs::fchown(&f, Some(0), Some(0))?;\n  1137: ///     Ok(())\n  1138: /// }\n  1139: /// ```\n  1140: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1141: pub fn fchown<F: AsFd>(fd: F, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1142:     sys::fs::fchown(fd.as_fd().as_raw_fd(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1143: }\n  1144: \n  1145: /// Change the owner and group of the specified path, without dereferencing symbolic links.\n  1146: ///\n  1147: /// Identical to [`chown`], except that if called on a symbolic link, this will change the owner\n  1148: /// and group of the link itself rather than the owner and group of the link target.\n  1149: ///\n  1150: /// # Examples\n  1151: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::lchown",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
                                    "path": "crate::path::Path"
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
      "name": "lchown",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "dir",
            {
              "generic": "P"
            }
          ],
          [
            "uid",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u32"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
              }
            }
          ],
          [
            "gid",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u32"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
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
    "verification_source": "  1146: /// Change the owner and group of the specified path, without dereferencing symbolic links.\n  1147: ///\n  1148: /// Identical to [`chown`], except that if called on a symbolic link, this will change the owner\n  1149: /// and group of the link itself rather than the owner and group of the link target.\n  1150: ///\n  1151: /// # Examples\n  1152: ///\n  1153: /// ```no_run\n  1154: /// use std::os::unix::fs;\n  1155: ///\n  1156: /// fn main() -> std::io::Result<()> {\n  1157: ///     fs::lchown(\"/symlink\", Some(0), Some(0))?;\n  1158: ///     Ok(())\n  1159: /// }\n  1160: /// ```\n  1161: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1162: pub fn lchown<P: AsRef<Path>>(dir: P, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1163:     sys::fs::lchown(dir.as_ref(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1164: }\n  1165: \n  1166: /// Change the root directory of the current process to the specified path.\n  1167: ///\n  1168: /// This typically requires privileges, such as root or a specific capability.\n  1169: ///\n  1170: /// This does not change the current working directory; you should call\n  1171: /// [`std::env::set_current_dir`][`crate::env::set_current_dir`] afterwards.\n  1172: ///\n  1173: /// # Examples\n  1174: ///\n  1175: /// ```no_run\n  1176: /// use std::os::unix::fs;\n  1177: ///\n  1178: /// fn main() -> std::io::Result<()> {",
    "nanvix_source": "  1151: ///\n  1152: /// ```no_run\n  1153: /// use std::os::unix::fs;\n  1154: ///\n  1155: /// fn main() -> std::io::Result<()> {\n  1156: ///     fs::lchown(\"/symlink\", Some(0), Some(0))?;\n  1157: ///     Ok(())\n  1158: /// }\n  1159: /// ```\n  1160: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1161: pub fn lchown<P: AsRef<Path>>(dir: P, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1162:     sys::fs::lchown(dir.as_ref(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1163: }\n  1164: \n  1165: /// Change the root directory of the current process to the specified path.\n  1166: ///\n  1167: /// This typically requires privileges, such as root or a specific capability.\n  1168: ///\n  1169: /// This does not change the current working directory; you should call\n  1170: /// [`std::env::set_current_dir`][`crate::env::set_current_dir`] afterwards.\n  1171: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::symlink",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
                                    "path": "crate::path::Path"
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
          },
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
                                    "path": "crate::path::Path"
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
            "name": "Q"
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
      "name": "symlink",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "original",
            {
              "generic": "P"
            }
          ],
          [
            "link",
            {
              "generic": "Q"
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
    "verification_source": "  1048: \n  1049: /// Creates a new symbolic link on the filesystem.\n  1050: ///\n  1051: /// The `link` path will be a symbolic link pointing to the `original` path.\n  1052: ///\n  1053: /// # Examples\n  1054: ///\n  1055: /// ```no_run\n  1056: /// use std::os::unix::fs;\n  1057: ///\n  1058: /// fn main() -> std::io::Result<()> {\n  1059: ///     fs::symlink(\"a.txt\", \"b.txt\")?;\n  1060: ///     Ok(())\n  1061: /// }\n  1062: /// ```\n  1063: #[stable(feature = \"symlink\", since = \"1.1.0\")]\n  1064: pub fn symlink<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  1065:     sys::fs::symlink(original.as_ref(), link.as_ref())\n  1066: }\n  1067: \n  1068: /// Unix-specific extensions to [`fs::DirBuilder`].\n  1069: #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1070: pub trait DirBuilderExt {\n  1071:     /// Sets the mode to create new directories with. This option defaults to\n  1072:     /// 0o777.\n  1073:     ///\n  1074:     /// # Examples\n  1075:     ///\n  1076:     /// ```no_run\n  1077:     /// use std::fs::DirBuilder;\n  1078:     /// use std::os::unix::fs::DirBuilderExt;\n  1079:     ///\n  1080:     /// let mut builder = DirBuilder::new();",
    "nanvix_source": "  1053: ///\n  1054: /// ```no_run\n  1055: /// use std::os::unix::fs;\n  1056: ///\n  1057: /// fn main() -> std::io::Result<()> {\n  1058: ///     fs::symlink(\"a.txt\", \"b.txt\")?;\n  1059: ///     Ok(())\n  1060: /// }\n  1061: /// ```\n  1062: #[stable(feature = \"symlink\", since = \"1.1.0\")]\n  1063: pub fn symlink<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  1064:     sys::fs::symlink(original.as_ref(), link.as_ref())\n  1065: }\n  1066: \n  1067: /// Unix-specific extensions to [`fs::DirBuilder`].\n  1068: #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  1069: pub trait DirBuilderExt {\n  1070:     /// Sets the mode to create new directories with. This option defaults to\n  1071:     /// 0o777.\n  1072:     ///\n  1073:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::SocketAddr::as_pathname",
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
      "external_or_hidden_runtime_state",
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
      "name": "as_pathname",
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
            "args": null,
            "id": 5186,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5190",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5186",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "addr",
          "SocketAddr"
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 1802,
                            "path": "Path"
                          }
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   218:     /// ```\n   219:     ///\n   220:     /// Without a pathname:\n   221:     ///\n   222:     /// ```\n   223:     /// use std::os::unix::net::UnixDatagram;\n   224:     ///\n   225:     /// fn main() -> std::io::Result<()> {\n   226:     ///     let socket = UnixDatagram::unbound()?;\n   227:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   228:     ///     assert_eq!(addr.as_pathname(), None);\n   229:     ///     Ok(())\n   230:     /// }\n   231:     /// ```\n   232:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   233:     #[must_use]\n   234:     pub fn as_pathname(&self) -> Option<&Path> {\n   235:         if let AddressKind::Pathname(path) = self.address() { Some(path) } else { None }\n   236:     }\n   237: \n   238:     fn address(&self) -> AddressKind<'_> {\n   239:         let len = self.len as usize - SUN_PATH_OFFSET;\n   240:         let path = unsafe { mem::transmute::<&[libc::c_char], &[u8]>(&self.addr.sun_path) };\n   241: \n   242:         // macOS seems to return a len of 16 and a zeroed sun_path for unnamed addresses\n   243:         if len == 0\n   244:             || (cfg!(not(any(target_os = \"linux\", target_os = \"android\", target_os = \"cygwin\")))\n   245:                 && self.addr.sun_path[0] == 0)\n   246:         {\n   247:             AddressKind::Unnamed\n   248:         } else if self.addr.sun_path[0] == 0 {\n   249:             AddressKind::Abstract(ByteStr::from_bytes(&path[1..len]))\n   250:         } else {",
    "nanvix_source": "   231:     ///\n   232:     /// fn main() -> std::io::Result<()> {\n   233:     ///     let socket = UnixDatagram::unbound()?;\n   234:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   235:     ///     assert_eq!(addr.as_pathname(), None);\n   236:     ///     Ok(())\n   237:     /// }\n   238:     /// ```\n   239:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   240:     #[must_use]\n   241:     pub fn as_pathname(&self) -> Option<&Path> {\n   242:         if let AddressKind::Pathname(path) = self.address() { Some(path) } else { None }\n   243:     }\n   244: \n   245:     fn address(&self) -> AddressKind<'_> {\n   246:         let len = self.len as usize - SUN_PATH_OFFSET;\n   247:         let path = unsafe { mem::transmute::<&[libc::c_char], &[u8]>(&self.addr.sun_path) };\n   248: \n   249:         // macOS seems to return a len of 16 and a zeroed sun_path for unnamed addresses\n   250:         if len == 0\n   251:             || (cfg!(not(any(target_os = \"linux\", target_os = \"android\", target_os = \"cygwin\")))",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::SocketAddr::from_pathname",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
              "generic_params": [],
              "type": {
                "generic": "P"
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
      "name": "from_pathname",
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
            "id": 5186,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5190",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5186",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "addr",
          "SocketAddr"
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
                        "id": 5186,
                        "path": "SocketAddr"
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
    "verification_source": "   144:     ///\n   145:     /// # fn main() -> std::io::Result<()> {\n   146:     /// let address = SocketAddr::from_pathname(\"/path/to/socket\")?;\n   147:     /// assert_eq!(address.as_pathname(), Some(Path::new(\"/path/to/socket\")));\n   148:     /// # Ok(())\n   149:     /// # }\n   150:     /// ```\n   151:     ///\n   152:     /// Creating a `SocketAddr` with a NULL byte results in an error.\n   153:     ///\n   154:     /// ```\n   155:     /// use std::os::unix::net::SocketAddr;\n   156:     ///\n   157:     /// assert!(SocketAddr::from_pathname(\"/path/with/\\0/bytes\").is_err());\n   158:     /// ```\n   159:     #[stable(feature = \"unix_socket_creation\", since = \"1.61.0\")]\n   160:     pub fn from_pathname<P>(path: P) -> io::Result<SocketAddr>\n   161:     where\n   162:         P: AsRef<Path>,\n   163:     {\n   164:         sockaddr_un(path.as_ref()).map(|(addr, len)| SocketAddr { addr, len })\n   165:     }\n   166: \n   167:     /// Returns `true` if the address is unnamed.\n   168:     ///\n   169:     /// # Examples\n   170:     ///\n   171:     /// A named address:\n   172:     ///\n   173:     /// ```no_run\n   174:     /// use std::os::unix::net::UnixListener;\n   175:     ///\n   176:     /// fn main() -> std::io::Result<()> {",
    "nanvix_source": "   157:     /// ```\n   158:     ///\n   159:     /// Creating a `SocketAddr` with a NULL byte results in an error.\n   160:     ///\n   161:     /// ```\n   162:     /// use std::os::unix::net::SocketAddr;\n   163:     ///\n   164:     /// assert!(SocketAddr::from_pathname(\"/path/with/\\0/bytes\").is_err());\n   165:     /// ```\n   166:     #[stable(feature = \"unix_socket_creation\", since = \"1.61.0\")]\n   167:     pub fn from_pathname<P>(path: P) -> io::Result<SocketAddr>\n   168:     where\n   169:         P: AsRef<Path>,\n   170:     {\n   171:         sockaddr_un(path.as_ref()).map(|(addr, len)| SocketAddr { addr, len })\n   172:     }\n   173: \n   174:     /// Returns `true` if the address is unnamed.\n   175:     ///\n   176:     /// # Examples\n   177:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::SocketAddr::is_unnamed",
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
      "name": "is_unnamed",
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
            "id": 5186,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5190",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5186",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "addr",
          "SocketAddr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   182:     /// ```\n   183:     ///\n   184:     /// An unnamed address:\n   185:     ///\n   186:     /// ```\n   187:     /// use std::os::unix::net::UnixDatagram;\n   188:     ///\n   189:     /// fn main() -> std::io::Result<()> {\n   190:     ///     let socket = UnixDatagram::unbound()?;\n   191:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   192:     ///     assert_eq!(addr.is_unnamed(), true);\n   193:     ///     Ok(())\n   194:     /// }\n   195:     /// ```\n   196:     #[must_use]\n   197:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   198:     pub fn is_unnamed(&self) -> bool {\n   199:         matches!(self.address(), AddressKind::Unnamed)\n   200:     }\n   201: \n   202:     /// Returns the contents of this address if it is a `pathname` address.\n   203:     ///\n   204:     /// # Examples\n   205:     ///\n   206:     /// With a pathname:\n   207:     ///\n   208:     /// ```no_run\n   209:     /// use std::os::unix::net::UnixListener;\n   210:     /// use std::path::Path;\n   211:     ///\n   212:     /// fn main() -> std::io::Result<()> {\n   213:     ///     let socket = UnixListener::bind(\"/tmp/sock\")?;\n   214:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");",
    "nanvix_source": "   195:     ///\n   196:     /// fn main() -> std::io::Result<()> {\n   197:     ///     let socket = UnixDatagram::unbound()?;\n   198:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   199:     ///     assert_eq!(addr.is_unnamed(), true);\n   200:     ///     Ok(())\n   201:     /// }\n   202:     /// ```\n   203:     #[must_use]\n   204:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   205:     pub fn is_unnamed(&self) -> bool {\n   206:         matches!(self.address(), AddressKind::Unnamed)\n   207:     }\n   208: \n   209:     /// Returns the contents of this address if it is a `pathname` address.\n   210:     ///\n   211:     /// # Examples\n   212:     ///\n   213:     /// With a pathname:\n   214:     ///\n   215:     /// ```no_run",
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
