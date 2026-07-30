For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::read_dir",
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
      "name": "read_dir",
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
                        "id": 2886,
                        "path": "ReadDir"
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
    "verification_source": "  3297: ///     let mut entries = fs::read_dir(\".\")?\n  3298: ///         .map(|res| res.map(|e| e.path()))\n  3299: ///         .collect::<Result<Vec<_>, io::Error>>()?;\n  3300: ///\n  3301: ///     // The order in which `read_dir` returns entries is not guaranteed. If reproducible\n  3302: ///     // ordering is required the entries should be explicitly sorted.\n  3303: ///\n  3304: ///     entries.sort();\n  3305: ///\n  3306: ///     // The entries have now been sorted by their path.\n  3307: ///\n  3308: ///     Ok(())\n  3309: /// }\n  3310: /// ```\n  3311: #[doc(alias = \"ls\", alias = \"opendir\", alias = \"FindFirstFile\", alias = \"FindNextFile\")]\n  3312: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3313: pub fn read_dir<P: AsRef<Path>>(path: P) -> io::Result<ReadDir> {\n  3314:     fs_imp::read_dir(path.as_ref()).map(ReadDir)\n  3315: }\n  3316: \n  3317: /// Changes the permissions found on a file or a directory.\n  3318: ///\n  3319: /// # Platform-specific behavior\n  3320: ///\n  3321: /// This function currently corresponds to the `chmod` function on Unix\n  3322: /// and the `SetFileAttributes` function on Windows.\n  3323: /// Note that, this [may change in the future][changes].\n  3324: ///\n  3325: /// [changes]: io#platform-specific-behavior\n  3326: ///\n  3327: /// ## Symlinks\n  3328: /// On UNIX-like systems, this function will update the permission bits\n  3329: /// of the file pointed to by the symlink.",
    "nanvix_source": "  3277: ///\n  3278: ///     entries.sort();\n  3279: ///\n  3280: ///     // The entries have now been sorted by their path.\n  3281: ///\n  3282: ///     Ok(())\n  3283: /// }\n  3284: /// ```\n  3285: #[doc(alias = \"ls\", alias = \"opendir\", alias = \"FindFirstFile\", alias = \"FindNextFile\")]\n  3286: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3287: pub fn read_dir<P: AsRef<Path>>(path: P) -> io::Result<ReadDir> {\n  3288:     fs_imp::read_dir(path.as_ref()).map(ReadDir)\n  3289: }\n  3290: \n  3291: /// Changes the permissions found on a file or a directory.\n  3292: ///\n  3293: /// # Platform-specific behavior\n  3294: ///\n  3295: /// This function currently corresponds to the `chmod` function on Unix\n  3296: /// and the `SetFileAttributes` function on Windows.\n  3297: /// Note that, this [may change in the future][changes].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::read_link",
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
      "name": "read_link",
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
                        "id": 1799,
                        "path": "crate::path::PathBuf"
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
    "verification_source": "  2978: /// limited to just these cases:\n  2979: ///\n  2980: /// * `path` is not a symbolic link.\n  2981: /// * `path` does not exist.\n  2982: ///\n  2983: /// # Examples\n  2984: ///\n  2985: /// ```no_run\n  2986: /// use std::fs;\n  2987: ///\n  2988: /// fn main() -> std::io::Result<()> {\n  2989: ///     let path = fs::read_link(\"a.txt\")?;\n  2990: ///     Ok(())\n  2991: /// }\n  2992: /// ```\n  2993: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2994: pub fn read_link<P: AsRef<Path>>(path: P) -> io::Result<PathBuf> {\n  2995:     fs_imp::read_link(path.as_ref())\n  2996: }\n  2997: \n  2998: /// Returns the canonical, absolute form of a path with all intermediate\n  2999: /// components normalized and symbolic links resolved.\n  3000: ///\n  3001: /// # Platform-specific behavior\n  3002: ///\n  3003: /// This function currently corresponds to the `realpath` function on Unix\n  3004: /// and the `CreateFile` and `GetFinalPathNameByHandle` functions on Windows.\n  3005: /// Note that this [may change in the future][changes].\n  3006: ///\n  3007: /// On Windows, this converts the path to use [extended length path][path]\n  3008: /// syntax, which allows your program to use longer path names, but means you\n  3009: /// can only join backslash-delimited paths to it, and it may be incompatible\n  3010: /// with other applications (if passed to the application on the command-line,",
    "nanvix_source": "  2958: ///\n  2959: /// ```no_run\n  2960: /// use std::fs;\n  2961: ///\n  2962: /// fn main() -> std::io::Result<()> {\n  2963: ///     let path = fs::read_link(\"a.txt\")?;\n  2964: ///     Ok(())\n  2965: /// }\n  2966: /// ```\n  2967: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2968: pub fn read_link<P: AsRef<Path>>(path: P) -> io::Result<PathBuf> {\n  2969:     fs_imp::read_link(path.as_ref())\n  2970: }\n  2971: \n  2972: /// Returns the canonical, absolute form of a path with all intermediate\n  2973: /// components normalized and symbolic links resolved.\n  2974: ///\n  2975: /// # Platform-specific behavior\n  2976: ///\n  2977: /// This function currently corresponds to the `realpath` function on Unix\n  2978: /// and the `CreateFile` and `GetFinalPathNameByHandle` functions on Windows.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::read_to_string",
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
      "name": "read_to_string",
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
                        "id": 218,
                        "path": "String"
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
    "verification_source": "   367: /// While reading from the file, this function handles [`io::ErrorKind::Interrupted`]\n   368: /// with automatic retries. See [io::Read] documentation for details.\n   369: ///\n   370: /// # Examples\n   371: ///\n   372: /// ```no_run\n   373: /// use std::fs;\n   374: /// use std::error::Error;\n   375: ///\n   376: /// fn main() -> Result<(), Box<dyn Error>> {\n   377: ///     let message: String = fs::read_to_string(\"message.txt\")?;\n   378: ///     println!(\"{}\", message);\n   379: ///     Ok(())\n   380: /// }\n   381: /// ```\n   382: #[stable(feature = \"fs_read_write\", since = \"1.26.0\")]\n   383: pub fn read_to_string<P: AsRef<Path>>(path: P) -> io::Result<String> {\n   384:     fn inner(path: &Path) -> io::Result<String> {\n   385:         let mut file = File::open(path)?;\n   386:         let size = file.metadata().map(|m| usize::try_from(m.len()).unwrap_or(usize::MAX)).ok();\n   387:         let mut string = String::new();\n   388:         string.try_reserve_exact(size.unwrap_or(0))?;\n   389:         io::default_read_to_string(&mut file, &mut string, size)?;\n   390:         Ok(string)\n   391:     }\n   392:     inner(path.as_ref())\n   393: }\n   394: \n   395: /// Writes a slice as the entire contents of a file.\n   396: ///\n   397: /// This function will create a file if it does not exist,\n   398: /// and will entirely replace its contents if it does.\n   399: ///",
    "nanvix_source": "   372: /// use std::fs;\n   373: /// use std::error::Error;\n   374: ///\n   375: /// fn main() -> Result<(), Box<dyn Error>> {\n   376: ///     let message: String = fs::read_to_string(\"message.txt\")?;\n   377: ///     println!(\"{}\", message);\n   378: ///     Ok(())\n   379: /// }\n   380: /// ```\n   381: #[stable(feature = \"fs_read_write\", since = \"1.26.0\")]\n   382: pub fn read_to_string<P: AsRef<Path>>(path: P) -> io::Result<String> {\n   383:     fn inner(path: &Path) -> io::Result<String> {\n   384:         let mut file = File::open(path)?;\n   385:         let size = file.metadata().map(|m| usize::try_from(m.len()).unwrap_or(usize::MAX)).ok();\n   386:         let mut string = String::new();\n   387:         string.try_reserve_exact(size.unwrap_or(0))?;\n   388:         io::default_read_to_string(&mut file, &mut string, size)?;\n   389:         Ok(string)\n   390:     }\n   391:     inner(path.as_ref())\n   392: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::remove_dir",
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
      "name": "remove_dir",
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
    "verification_source": "  3154: /// path does not exist. Note that the inverse is not true,\n  3155: /// i.e. if a path does not exist, its removal may fail for a number of reasons,\n  3156: /// such as insufficient permissions.\n  3157: ///\n  3158: /// # Examples\n  3159: ///\n  3160: /// ```no_run\n  3161: /// use std::fs;\n  3162: ///\n  3163: /// fn main() -> std::io::Result<()> {\n  3164: ///     fs::remove_dir(\"/some/dir\")?;\n  3165: ///     Ok(())\n  3166: /// }\n  3167: /// ```\n  3168: #[doc(alias = \"rmdir\", alias = \"RemoveDirectory\")]\n  3169: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3170: pub fn remove_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3171:     fs_imp::remove_dir(path.as_ref())\n  3172: }\n  3173: \n  3174: /// Removes a directory at this path, after removing all its contents. Use\n  3175: /// carefully!\n  3176: ///\n  3177: /// This function does **not** follow symbolic links and it will simply remove the\n  3178: /// symbolic link itself.\n  3179: ///\n  3180: /// # Platform-specific behavior\n  3181: ///\n  3182: /// These implementation details [may change in the future][changes].\n  3183: ///\n  3184: /// - \"Unix-like\": By default, this function currently corresponds to\n  3185: /// `openat`, `fdopendir`, `unlinkat` and `lstat`\n  3186: /// on Unix-family platforms, except where noted otherwise.",
    "nanvix_source": "  3134: /// ```no_run\n  3135: /// use std::fs;\n  3136: ///\n  3137: /// fn main() -> std::io::Result<()> {\n  3138: ///     fs::remove_dir(\"/some/dir\")?;\n  3139: ///     Ok(())\n  3140: /// }\n  3141: /// ```\n  3142: #[doc(alias = \"rmdir\", alias = \"RemoveDirectory\")]\n  3143: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3144: pub fn remove_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3145:     fs_imp::remove_dir(path.as_ref())\n  3146: }\n  3147: \n  3148: /// Removes a directory at this path, after removing all its contents. Use\n  3149: /// carefully!\n  3150: ///\n  3151: /// This function does **not** follow symbolic links and it will simply remove the\n  3152: /// symbolic link itself.\n  3153: ///\n  3154: /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::remove_dir_all",
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
      "name": "remove_dir_all",
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
    "verification_source": "  3218: /// [`io::ErrorKind::NotFound`] is only returned if no removal occurs.\n  3219: ///\n  3220: /// [`fs::remove_file`]: remove_file\n  3221: /// [`fs::remove_dir`]: remove_dir\n  3222: ///\n  3223: /// # Examples\n  3224: ///\n  3225: /// ```no_run\n  3226: /// use std::fs;\n  3227: ///\n  3228: /// fn main() -> std::io::Result<()> {\n  3229: ///     fs::remove_dir_all(\"/some/dir\")?;\n  3230: ///     Ok(())\n  3231: /// }\n  3232: /// ```\n  3233: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3234: pub fn remove_dir_all<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3235:     fs_imp::remove_dir_all(path.as_ref())\n  3236: }\n  3237: \n  3238: /// Returns an iterator over the entries within a directory.\n  3239: ///\n  3240: /// The iterator will yield instances of <code>[io::Result]<[DirEntry]></code>.\n  3241: /// New errors may be encountered after an iterator is initially constructed.\n  3242: /// Entries for the current and parent directories (typically `.` and `..`) are\n  3243: /// skipped.\n  3244: ///\n  3245: /// The order in which `read_dir` returns entries can change between calls. If reproducible\n  3246: /// ordering is required, the entries should be explicitly sorted.\n  3247: ///\n  3248: /// # Platform-specific behavior\n  3249: ///\n  3250: /// This function currently corresponds to the `opendir` function on Unix",
    "nanvix_source": "  3198: ///\n  3199: /// ```no_run\n  3200: /// use std::fs;\n  3201: ///\n  3202: /// fn main() -> std::io::Result<()> {\n  3203: ///     fs::remove_dir_all(\"/some/dir\")?;\n  3204: ///     Ok(())\n  3205: /// }\n  3206: /// ```\n  3207: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3208: pub fn remove_dir_all<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3209:     fs_imp::remove_dir_all(path.as_ref())\n  3210: }\n  3211: \n  3212: /// Returns an iterator over the entries within a directory.\n  3213: ///\n  3214: /// The iterator will yield instances of <code>[io::Result]<[DirEntry]></code>.\n  3215: /// New errors may be encountered after an iterator is initially constructed.\n  3216: /// Entries for the current and parent directories (typically `.` and `..`) are\n  3217: /// skipped.\n  3218: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::remove_file",
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
      "name": "remove_file",
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
    "verification_source": "  2684: /// path does not exist. Note that the inverse is not true,\n  2685: /// i.e. if a path does not exist, its removal may fail for a number of reasons,\n  2686: /// such as insufficient permissions.\n  2687: ///\n  2688: /// # Examples\n  2689: ///\n  2690: /// ```no_run\n  2691: /// use std::fs;\n  2692: ///\n  2693: /// fn main() -> std::io::Result<()> {\n  2694: ///     fs::remove_file(\"a.txt\")?;\n  2695: ///     Ok(())\n  2696: /// }\n  2697: /// ```\n  2698: #[doc(alias = \"rm\", alias = \"unlink\", alias = \"DeleteFile\")]\n  2699: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2700: pub fn remove_file<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  2701:     fs_imp::remove_file(path.as_ref())\n  2702: }\n  2703: \n  2704: /// Given a path, queries the file system to get information about a file,\n  2705: /// directory, etc.\n  2706: ///\n  2707: /// This function will traverse symbolic links to query information about the\n  2708: /// destination file.\n  2709: ///\n  2710: /// # Platform-specific behavior\n  2711: ///\n  2712: /// This function currently corresponds to the `stat` function on Unix\n  2713: /// and the `GetFileInformationByHandle` function on Windows.\n  2714: /// Note that, this [may change in the future][changes].\n  2715: ///\n  2716: /// [changes]: io#platform-specific-behavior",
    "nanvix_source": "  2661: /// ```no_run\n  2662: /// use std::fs;\n  2663: ///\n  2664: /// fn main() -> std::io::Result<()> {\n  2665: ///     fs::remove_file(\"a.txt\")?;\n  2666: ///     Ok(())\n  2667: /// }\n  2668: /// ```\n  2669: #[doc(alias = \"rm\", alias = \"unlink\", alias = \"DeleteFile\")]\n  2670: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2671: pub fn remove_file<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  2672:     fs_imp::remove_file(path.as_ref())\n  2673: }\n  2674: \n  2675: /// Given a path, queries the file system to get information about a file,\n  2676: /// directory, etc.\n  2677: ///\n  2678: /// This function will traverse symbolic links to query information about the\n  2679: /// destination file.\n  2680: ///\n  2681: /// # Platform-specific behavior",
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
