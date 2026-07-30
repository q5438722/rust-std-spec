For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::create_dir",
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
      "name": "create_dir",
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
    "verification_source": "  3063: ///   function.)\n  3064: /// * `path` already exists.\n  3065: ///\n  3066: /// # Examples\n  3067: ///\n  3068: /// ```no_run\n  3069: /// use std::fs;\n  3070: ///\n  3071: /// fn main() -> std::io::Result<()> {\n  3072: ///     fs::create_dir(\"/some/dir\")?;\n  3073: ///     Ok(())\n  3074: /// }\n  3075: /// ```\n  3076: #[doc(alias = \"mkdir\", alias = \"CreateDirectory\")]\n  3077: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3078: #[cfg_attr(not(test), rustc_diagnostic_item = \"fs_create_dir\")]\n  3079: pub fn create_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3080:     DirBuilder::new().create(path.as_ref())\n  3081: }\n  3082: \n  3083: /// Recursively create a directory and all of its parent components if they\n  3084: /// are missing.\n  3085: ///\n  3086: /// This function is not atomic. If it returns an error, any parent components it was able to create\n  3087: /// will remain.\n  3088: ///\n  3089: /// If the empty path is passed to this function, it always succeeds without\n  3090: /// creating any directories.\n  3091: ///\n  3092: /// # Platform-specific behavior\n  3093: ///\n  3094: /// This function currently corresponds to multiple calls to the `mkdir`\n  3095: /// function on Unix and the `CreateDirectoryW` function on Windows.",
    "nanvix_source": "  3043: /// use std::fs;\n  3044: ///\n  3045: /// fn main() -> std::io::Result<()> {\n  3046: ///     fs::create_dir(\"/some/dir\")?;\n  3047: ///     Ok(())\n  3048: /// }\n  3049: /// ```\n  3050: #[doc(alias = \"mkdir\", alias = \"CreateDirectory\")]\n  3051: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3052: #[cfg_attr(not(test), rustc_diagnostic_item = \"fs_create_dir\")]\n  3053: pub fn create_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3054:     DirBuilder::new().create(path.as_ref())\n  3055: }\n  3056: \n  3057: /// Recursively create a directory and all of its parent components if they\n  3058: /// are missing.\n  3059: ///\n  3060: /// This function is not atomic. If it returns an error, any parent components it was able to create\n  3061: /// will remain.\n  3062: ///\n  3063: /// If the empty path is passed to this function, it always succeeds without",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::create_dir_all",
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
      "name": "create_dir_all",
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
    "verification_source": "  3109: /// concurrently from multiple threads or processes is guaranteed not to fail\n  3110: /// due to a race condition with itself.\n  3111: ///\n  3112: /// [`fs::create_dir`]: create_dir\n  3113: ///\n  3114: /// # Examples\n  3115: ///\n  3116: /// ```no_run\n  3117: /// use std::fs;\n  3118: ///\n  3119: /// fn main() -> std::io::Result<()> {\n  3120: ///     fs::create_dir_all(\"/some/dir\")?;\n  3121: ///     Ok(())\n  3122: /// }\n  3123: /// ```\n  3124: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3125: pub fn create_dir_all<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3126:     DirBuilder::new().recursive(true).create(path.as_ref())\n  3127: }\n  3128: \n  3129: /// Removes an empty directory.\n  3130: ///\n  3131: /// If you want to remove a directory that is not empty, as well as all\n  3132: /// of its contents recursively, consider using [`remove_dir_all`]\n  3133: /// instead.\n  3134: ///\n  3135: /// # Platform-specific behavior\n  3136: ///\n  3137: /// This function currently corresponds to the `rmdir` function on Unix\n  3138: /// and the `RemoveDirectory` function on Windows.\n  3139: /// Note that, this [may change in the future][changes].\n  3140: ///\n  3141: /// [changes]: io#platform-specific-behavior",
    "nanvix_source": "  3089: ///\n  3090: /// ```no_run\n  3091: /// use std::fs;\n  3092: ///\n  3093: /// fn main() -> std::io::Result<()> {\n  3094: ///     fs::create_dir_all(\"/some/dir\")?;\n  3095: ///     Ok(())\n  3096: /// }\n  3097: /// ```\n  3098: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3099: pub fn create_dir_all<P: AsRef<Path>>(path: P) -> io::Result<()> {\n  3100:     DirBuilder::new().recursive(true).create(path.as_ref())\n  3101: }\n  3102: \n  3103: /// Removes an empty directory.\n  3104: ///\n  3105: /// If you want to remove a directory that is not empty, as well as all\n  3106: /// of its contents recursively, consider using [`remove_dir_all`]\n  3107: /// instead.\n  3108: ///\n  3109: /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::exists",
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
      "name": "exists",
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
                      "primitive": "bool"
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
    "verification_source": "  3494:     }\n  3495: }\n  3496: \n  3497: impl AsInnerMut<fs_imp::DirBuilder> for DirBuilder {\n  3498:     #[inline]\n  3499:     fn as_inner_mut(&mut self) -> &mut fs_imp::DirBuilder {\n  3500:         &mut self.inner\n  3501:     }\n  3502: }\n  3503: \n  3504: /// Returns `Ok(true)` if the path points at an existing entity.\n  3505: ///\n  3506: /// This function will traverse symbolic links to query information about the\n  3507: /// destination file. In case of broken symbolic links this will return `Ok(false)`.\n  3508: ///\n  3509: /// As opposed to the [`Path::exists`] method, this will only return `Ok(true)` or `Ok(false)`\n  3510: /// if the path was _verified_ to exist or not exist. If its existence can neither be confirmed\n  3511: /// nor denied, an `Err(_)` will be propagated instead. This can be the case if e.g. listing\n  3512: /// permission is denied on one of the parent directories.\n  3513: ///\n  3514: /// Note that while this avoids some pitfalls of the `exists()` method, it still can not\n  3515: /// prevent time-of-check to time-of-use ([TOCTOU]) bugs. You should only use it in scenarios\n  3516: /// where those bugs are not an issue.\n  3517: ///\n  3518: /// # Examples\n  3519: ///\n  3520: /// ```no_run\n  3521: /// use std::fs;\n  3522: ///\n  3523: /// assert!(!fs::exists(\"does_not_exist.txt\").expect(\"Can't check existence of file does_not_exist.txt\"));\n  3524: /// assert!(fs::exists(\"/root/secret_file.txt\").is_err());\n  3525: /// ```\n  3526: ///",
    "nanvix_source": "  3474:         &mut self.inner\n  3475:     }\n  3476: }\n  3477: \n  3478: /// Returns `Ok(true)` if the path points at an existing entity.\n  3479: ///\n  3480: /// This function will traverse symbolic links to query information about the\n  3481: /// destination file. In case of broken symbolic links this will return `Ok(false)`.\n  3482: ///\n  3483: /// As opposed to the [`Path::exists`] method, this will only return `Ok(true)` or `Ok(false)`\n  3484: /// if the path was _verified_ to exist or not exist. If its existence can neither be confirmed\n  3485: /// nor denied, an `Err(_)` will be propagated instead. This can be the case if e.g. listing\n  3486: /// permission is denied on one of the parent directories.\n  3487: ///\n  3488: /// Note that while this avoids some pitfalls of the `exists()` method, it still can not\n  3489: /// prevent time-of-check to time-of-use ([TOCTOU]) bugs. You should only use it in scenarios\n  3490: /// where those bugs are not an issue.\n  3491: ///\n  3492: /// # Examples\n  3493: ///\n  3494: /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::hard_link",
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
      "name": "hard_link",
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
    "verification_source": "  2912: ///\n  2913: /// * The `original` path is not a file or doesn't exist.\n  2914: /// * The 'link' path already exists.\n  2915: ///\n  2916: /// # Examples\n  2917: ///\n  2918: /// ```no_run\n  2919: /// use std::fs;\n  2920: ///\n  2921: /// fn main() -> std::io::Result<()> {\n  2922: ///     fs::hard_link(\"a.txt\", \"b.txt\")?; // Hard link a.txt to b.txt\n  2923: ///     Ok(())\n  2924: /// }\n  2925: /// ```\n  2926: #[doc(alias = \"CreateHardLink\", alias = \"linkat\")]\n  2927: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2928: pub fn hard_link<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  2929:     fs_imp::hard_link(original.as_ref(), link.as_ref())\n  2930: }\n  2931: \n  2932: /// Creates a new symbolic link on the filesystem.\n  2933: ///\n  2934: /// The `link` path will be a symbolic link pointing to the `original` path.\n  2935: /// On Windows, this will be a file symlink, not a directory symlink;\n  2936: /// for this reason, the platform-specific [`std::os::unix::fs::symlink`]\n  2937: /// and [`std::os::windows::fs::symlink_file`] or [`symlink_dir`] should be\n  2938: /// used instead to make the intent explicit.\n  2939: ///\n  2940: /// [`std::os::unix::fs::symlink`]: crate::os::unix::fs::symlink\n  2941: /// [`std::os::windows::fs::symlink_file`]: crate::os::windows::fs::symlink_file\n  2942: /// [`symlink_dir`]: crate::os::windows::fs::symlink_dir\n  2943: ///\n  2944: /// # Examples",
    "nanvix_source": "  2892: /// ```no_run\n  2893: /// use std::fs;\n  2894: ///\n  2895: /// fn main() -> std::io::Result<()> {\n  2896: ///     fs::hard_link(\"a.txt\", \"b.txt\")?; // Hard link a.txt to b.txt\n  2897: ///     Ok(())\n  2898: /// }\n  2899: /// ```\n  2900: #[doc(alias = \"CreateHardLink\", alias = \"linkat\")]\n  2901: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2902: pub fn hard_link<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  2903:     fs_imp::hard_link(original.as_ref(), link.as_ref())\n  2904: }\n  2905: \n  2906: /// Creates a new symbolic link on the filesystem.\n  2907: ///\n  2908: /// The `link` path will be a symbolic link pointing to the `original` path.\n  2909: /// On Windows, this will be a file symlink, not a directory symlink;\n  2910: /// for this reason, the platform-specific [`std::os::unix::fs::symlink`]\n  2911: /// and [`std::os::windows::fs::symlink_file`] or [`symlink_dir`] should be\n  2912: /// used instead to make the intent explicit.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::metadata",
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
      "name": "metadata",
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
    "verification_source": "  2723: /// * The user lacks permissions to perform `metadata` call on `path`.\n  2724: /// * `path` does not exist.\n  2725: ///\n  2726: /// # Examples\n  2727: ///\n  2728: /// ```rust,no_run\n  2729: /// use std::fs;\n  2730: ///\n  2731: /// fn main() -> std::io::Result<()> {\n  2732: ///     let attr = fs::metadata(\"/some/file/path.txt\")?;\n  2733: ///     // inspect attr ...\n  2734: ///     Ok(())\n  2735: /// }\n  2736: /// ```\n  2737: #[doc(alias = \"stat\")]\n  2738: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2739: pub fn metadata<P: AsRef<Path>>(path: P) -> io::Result<Metadata> {\n  2740:     fs_imp::metadata(path.as_ref()).map(Metadata)\n  2741: }\n  2742: \n  2743: /// Queries the metadata about a file without following symlinks.\n  2744: ///\n  2745: /// # Platform-specific behavior\n  2746: ///\n  2747: /// This function currently corresponds to the `lstat` function on Unix\n  2748: /// and the `GetFileInformationByHandle` function on Windows.\n  2749: /// Note that, this [may change in the future][changes].\n  2750: ///\n  2751: /// [changes]: io#platform-specific-behavior\n  2752: ///\n  2753: /// # Errors\n  2754: ///\n  2755: /// This function will return an error in the following situations, but is not",
    "nanvix_source": "  2700: /// use std::fs;\n  2701: ///\n  2702: /// fn main() -> std::io::Result<()> {\n  2703: ///     let attr = fs::metadata(\"/some/file/path.txt\")?;\n  2704: ///     // inspect attr ...\n  2705: ///     Ok(())\n  2706: /// }\n  2707: /// ```\n  2708: #[doc(alias = \"stat\")]\n  2709: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2710: pub fn metadata<P: AsRef<Path>>(path: P) -> io::Result<Metadata> {\n  2711:     fs_imp::metadata(path.as_ref()).map(Metadata)\n  2712: }\n  2713: \n  2714: /// Queries the metadata about a file without following symlinks.\n  2715: ///\n  2716: /// # Platform-specific behavior\n  2717: ///\n  2718: /// This function currently corresponds to the `lstat` function on Unix\n  2719: /// and the `GetFileInformationByHandle` function on Windows.\n  2720: /// Note that, this [may change in the future][changes].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::read",
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
      "name": "read",
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
    "verification_source": "   325: ///\n   326: /// While reading from the file, this function handles [`io::ErrorKind::Interrupted`]\n   327: /// with automatic retries. See [io::Read] documentation for details.\n   328: ///\n   329: /// # Examples\n   330: ///\n   331: /// ```no_run\n   332: /// use std::fs;\n   333: ///\n   334: /// fn main() -> Result<(), Box<dyn std::error::Error + 'static>> {\n   335: ///     let data: Vec<u8> = fs::read(\"image.jpg\")?;\n   336: ///     assert_eq!(data[0..3], [0xFF, 0xD8, 0xFF]);\n   337: ///     Ok(())\n   338: /// }\n   339: /// ```\n   340: #[stable(feature = \"fs_read_write_bytes\", since = \"1.26.0\")]\n   341: pub fn read<P: AsRef<Path>>(path: P) -> io::Result<Vec<u8>> {\n   342:     fn inner(path: &Path) -> io::Result<Vec<u8>> {\n   343:         let mut file = File::open(path)?;\n   344:         let size = file.metadata().map(|m| usize::try_from(m.len()).unwrap_or(usize::MAX)).ok();\n   345:         let mut bytes = Vec::try_with_capacity(size.unwrap_or(0))?;\n   346:         io::default_read_to_end(&mut file, &mut bytes, size)?;\n   347:         Ok(bytes)\n   348:     }\n   349:     inner(path.as_ref())\n   350: }\n   351: \n   352: /// Reads the entire contents of a file into a string.\n   353: ///\n   354: /// This is a convenience function for using [`File::open`] and [`read_to_string`]\n   355: /// with fewer imports and without an intermediate variable.\n   356: ///\n   357: /// [`read_to_string`]: Read::read_to_string",
    "nanvix_source": "   330: /// ```no_run\n   331: /// use std::fs;\n   332: ///\n   333: /// fn main() -> Result<(), Box<dyn std::error::Error + 'static>> {\n   334: ///     let data: Vec<u8> = fs::read(\"image.jpg\")?;\n   335: ///     assert_eq!(data[0..3], [0xFF, 0xD8, 0xFF]);\n   336: ///     Ok(())\n   337: /// }\n   338: /// ```\n   339: #[stable(feature = \"fs_read_write_bytes\", since = \"1.26.0\")]\n   340: pub fn read<P: AsRef<Path>>(path: P) -> io::Result<Vec<u8>> {\n   341:     fn inner(path: &Path) -> io::Result<Vec<u8>> {\n   342:         let mut file = File::open(path)?;\n   343:         let size = file.metadata().map(|m| usize::try_from(m.len()).unwrap_or(usize::MAX)).ok();\n   344:         let mut bytes = Vec::try_with_capacity(size.unwrap_or(0))?;\n   345:         io::default_read_to_end(&mut file, &mut bytes, size)?;\n   346:         Ok(bytes)\n   347:     }\n   348:     inner(path.as_ref())\n   349: }\n   350: ",
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
