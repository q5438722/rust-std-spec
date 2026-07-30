For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::rename",
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
      "name": "rename",
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
            "from",
            {
              "generic": "P"
            }
          ],
          [
            "to",
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
    "verification_source": "  2804: /// * `from` does not exist.\n  2805: /// * The user lacks permissions to view contents.\n  2806: /// * `from` and `to` are on separate filesystems.\n  2807: ///\n  2808: /// # Examples\n  2809: ///\n  2810: /// ```no_run\n  2811: /// use std::fs;\n  2812: ///\n  2813: /// fn main() -> std::io::Result<()> {\n  2814: ///     fs::rename(\"a.txt\", \"b.txt\")?; // Rename a.txt to b.txt\n  2815: ///     Ok(())\n  2816: /// }\n  2817: /// ```\n  2818: #[doc(alias = \"mv\", alias = \"MoveFile\", alias = \"MoveFileEx\")]\n  2819: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2820: pub fn rename<P: AsRef<Path>, Q: AsRef<Path>>(from: P, to: Q) -> io::Result<()> {\n  2821:     fs_imp::rename(from.as_ref(), to.as_ref())\n  2822: }\n  2823: \n  2824: /// Copies the contents of one file to another. This function will also\n  2825: /// copy the permission bits of the original file to the destination file.\n  2826: ///\n  2827: /// This function will **overwrite** the contents of `to`.\n  2828: ///\n  2829: /// Note that if `from` and `to` both point to the same file, then the file\n  2830: /// will likely get truncated by this operation.\n  2831: ///\n  2832: /// On success, the total number of bytes copied is returned and it is equal to\n  2833: /// the length of the `to` file as reported by `metadata`.\n  2834: ///\n  2835: /// If you want to copy the contents of one file to another and you\u2019re\n  2836: /// working with [`File`]s, see the [`io::copy`](io::copy()) function.",
    "nanvix_source": "  2783: /// ```no_run\n  2784: /// use std::fs;\n  2785: ///\n  2786: /// fn main() -> std::io::Result<()> {\n  2787: ///     fs::rename(\"a.txt\", \"b.txt\")?; // Rename a.txt to b.txt\n  2788: ///     Ok(())\n  2789: /// }\n  2790: /// ```\n  2791: #[doc(alias = \"mv\", alias = \"MoveFile\", alias = \"MoveFileEx\")]\n  2792: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2793: pub fn rename<P: AsRef<Path>, Q: AsRef<Path>>(from: P, to: Q) -> io::Result<()> {\n  2794:     fs_imp::rename(from.as_ref(), to.as_ref())\n  2795: }\n  2796: \n  2797: /// Copies the contents of one file to another. This function will also\n  2798: /// copy the permission bits of the original file to the destination file.\n  2799: ///\n  2800: /// This function will **overwrite** the contents of `to`.\n  2801: ///\n  2802: /// Note that if `from` and `to` both point to the same file, then the file\n  2803: /// will likely get truncated by this operation.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::set_permissions",
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
      "name": "set_permissions",
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
          ],
          [
            "perm",
            {
              "resolved_path": {
                "args": null,
                "id": 2587,
                "path": "Permissions"
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
    "verification_source": "  3348: /// * The user lacks the permission to change attributes of the file.\n  3349: ///\n  3350: /// # Examples\n  3351: ///\n  3352: /// ```no_run\n  3353: /// use std::fs;\n  3354: ///\n  3355: /// fn main() -> std::io::Result<()> {\n  3356: ///     let mut perms = fs::metadata(\"foo.txt\")?.permissions();\n  3357: ///     perms.set_readonly(true);\n  3358: ///     fs::set_permissions(\"foo.txt\", perms)?;\n  3359: ///     Ok(())\n  3360: /// }\n  3361: /// ```\n  3362: #[doc(alias = \"chmod\", alias = \"SetFileAttributes\")]\n  3363: #[stable(feature = \"set_permissions\", since = \"1.1.0\")]\n  3364: pub fn set_permissions<P: AsRef<Path>>(path: P, perm: Permissions) -> io::Result<()> {\n  3365:     fs_imp::set_permissions(path.as_ref(), perm.0)\n  3366: }\n  3367: \n  3368: /// Set the permissions of a file, unless it is a symlink.\n  3369: ///\n  3370: /// Note that the non-final path elements are allowed to be symlinks.\n  3371: ///\n  3372: /// # Platform-specific behavior\n  3373: ///\n  3374: /// Currently unimplemented on Windows.\n  3375: ///\n  3376: /// On Unix platforms, this results in a [`FilesystemLoop`] error if the last element is a symlink.\n  3377: ///\n  3378: /// This behavior may change in the future.\n  3379: ///\n  3380: /// [`FilesystemLoop`]: crate::io::ErrorKind::FilesystemLoop",
    "nanvix_source": "  3328: ///\n  3329: /// fn main() -> std::io::Result<()> {\n  3330: ///     let mut perms = fs::metadata(\"foo.txt\")?.permissions();\n  3331: ///     perms.set_readonly(true);\n  3332: ///     fs::set_permissions(\"foo.txt\", perms)?;\n  3333: ///     Ok(())\n  3334: /// }\n  3335: /// ```\n  3336: #[doc(alias = \"chmod\", alias = \"SetFileAttributes\")]\n  3337: #[stable(feature = \"set_permissions\", since = \"1.1.0\")]\n  3338: pub fn set_permissions<P: AsRef<Path>>(path: P, perm: Permissions) -> io::Result<()> {\n  3339:     fs_imp::set_permissions(path.as_ref(), perm.0)\n  3340: }\n  3341: \n  3342: /// Set the permissions of a file, unless it is a symlink.\n  3343: ///\n  3344: /// Note that the non-final path elements are allowed to be symlinks.\n  3345: ///\n  3346: /// # Platform-specific behavior\n  3347: ///\n  3348: /// Currently unimplemented on Windows.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::soft_link",
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
      "name": "soft_link",
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
    "verification_source": "  2944: /// # Examples\n  2945: ///\n  2946: /// ```no_run\n  2947: /// use std::fs;\n  2948: ///\n  2949: /// fn main() -> std::io::Result<()> {\n  2950: ///     fs::soft_link(\"a.txt\", \"b.txt\")?;\n  2951: ///     Ok(())\n  2952: /// }\n  2953: /// ```\n  2954: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2955: #[deprecated(\n  2956:     since = \"1.1.0\",\n  2957:     note = \"replaced with std::os::unix::fs::symlink and \\\n  2958:             std::os::windows::fs::{symlink_file, symlink_dir}\"\n  2959: )]\n  2960: pub fn soft_link<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  2961:     fs_imp::symlink(original.as_ref(), link.as_ref())\n  2962: }\n  2963: \n  2964: /// Reads a symbolic link, returning the file that the link points to.\n  2965: ///\n  2966: /// # Platform-specific behavior\n  2967: ///\n  2968: /// This function currently corresponds to the `readlink` function on Unix\n  2969: /// and the `CreateFile` function with `FILE_FLAG_OPEN_REPARSE_POINT` and\n  2970: /// `FILE_FLAG_BACKUP_SEMANTICS` flags on Windows.\n  2971: /// Note that, this [may change in the future][changes].\n  2972: ///\n  2973: /// [changes]: io#platform-specific-behavior\n  2974: ///\n  2975: /// # Errors\n  2976: ///",
    "nanvix_source": "  2924: ///     fs::soft_link(\"a.txt\", \"b.txt\")?;\n  2925: ///     Ok(())\n  2926: /// }\n  2927: /// ```\n  2928: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2929: #[deprecated(\n  2930:     since = \"1.1.0\",\n  2931:     note = \"replaced with std::os::unix::fs::symlink and \\\n  2932:             std::os::windows::fs::{symlink_file, symlink_dir}\"\n  2933: )]\n  2934: pub fn soft_link<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n  2935:     fs_imp::symlink(original.as_ref(), link.as_ref())\n  2936: }\n  2937: \n  2938: /// Reads a symbolic link, returning the file that the link points to.\n  2939: ///\n  2940: /// # Platform-specific behavior\n  2941: ///\n  2942: /// This function currently corresponds to the `readlink` function on Unix\n  2943: /// and the `CreateFile` function with `FILE_FLAG_OPEN_REPARSE_POINT` and\n  2944: /// `FILE_FLAG_BACKUP_SEMANTICS` flags on Windows.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::symlink_metadata",
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
      "name": "symlink_metadata",
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
    "verification_source": "  2758: /// * The user lacks permissions to perform `metadata` call on `path`.\n  2759: /// * `path` does not exist.\n  2760: ///\n  2761: /// # Examples\n  2762: ///\n  2763: /// ```rust,no_run\n  2764: /// use std::fs;\n  2765: ///\n  2766: /// fn main() -> std::io::Result<()> {\n  2767: ///     let attr = fs::symlink_metadata(\"/some/file/path.txt\")?;\n  2768: ///     // inspect attr ...\n  2769: ///     Ok(())\n  2770: /// }\n  2771: /// ```\n  2772: #[doc(alias = \"lstat\")]\n  2773: #[stable(feature = \"symlink_metadata\", since = \"1.1.0\")]\n  2774: pub fn symlink_metadata<P: AsRef<Path>>(path: P) -> io::Result<Metadata> {\n  2775:     fs_imp::symlink_metadata(path.as_ref()).map(Metadata)\n  2776: }\n  2777: \n  2778: /// Renames a file or directory to a new name, replacing the original file if\n  2779: /// `to` already exists.\n  2780: ///\n  2781: /// This will not work if the new name is on a different mount point.\n  2782: ///\n  2783: /// # Platform-specific behavior\n  2784: ///\n  2785: /// This function currently corresponds to the `rename` function on Unix\n  2786: /// and the `MoveFileExW` or `SetFileInformationByHandle` function on Windows.\n  2787: ///\n  2788: /// Because of this, the behavior when both `from` and `to` exist differs. On\n  2789: /// Unix, if `from` is a directory, `to` must also be an (empty) directory. If\n  2790: /// `from` is not a directory, `to` must also be not a directory. The behavior",
    "nanvix_source": "  2735: /// use std::fs;\n  2736: ///\n  2737: /// fn main() -> std::io::Result<()> {\n  2738: ///     let attr = fs::symlink_metadata(\"/some/file/path.txt\")?;\n  2739: ///     // inspect attr ...\n  2740: ///     Ok(())\n  2741: /// }\n  2742: /// ```\n  2743: #[doc(alias = \"lstat\")]\n  2744: #[stable(feature = \"symlink_metadata\", since = \"1.1.0\")]\n  2745: pub fn symlink_metadata<P: AsRef<Path>>(path: P) -> io::Result<Metadata> {\n  2746:     fs_imp::symlink_metadata(path.as_ref()).map(Metadata)\n  2747: }\n  2748: \n  2749: /// Renames a file or directory to a new name, replacing the original file if\n  2750: /// `to` already exists.\n  2751: ///\n  2752: /// This will not work if the new name is on a different mount point.\n  2753: ///\n  2754: /// # Platform-specific behavior\n  2755: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::write",
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
                                  "slice": {
                                    "primitive": "u8"
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
            "name": "C"
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
      "name": "write",
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
          ],
          [
            "contents",
            {
              "generic": "C"
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
    "verification_source": "   404: /// with fewer imports.\n   405: ///\n   406: /// [`write_all`]: Write::write_all\n   407: ///\n   408: /// # Examples\n   409: ///\n   410: /// ```no_run\n   411: /// use std::fs;\n   412: ///\n   413: /// fn main() -> std::io::Result<()> {\n   414: ///     fs::write(\"foo.txt\", b\"Lorem ipsum\")?;\n   415: ///     fs::write(\"bar.txt\", \"dolor sit\")?;\n   416: ///     Ok(())\n   417: /// }\n   418: /// ```\n   419: #[stable(feature = \"fs_read_write_bytes\", since = \"1.26.0\")]\n   420: pub fn write<P: AsRef<Path>, C: AsRef<[u8]>>(path: P, contents: C) -> io::Result<()> {\n   421:     fn inner(path: &Path, contents: &[u8]) -> io::Result<()> {\n   422:         File::create(path)?.write_all(contents)\n   423:     }\n   424:     inner(path.as_ref(), contents.as_ref())\n   425: }\n   426: \n   427: /// Changes the timestamps of the file or directory at the specified path.\n   428: ///\n   429: /// This function will attempt to set the access and modification times\n   430: /// to the times specified. If the path refers to a symbolic link, this function\n   431: /// will follow the link and change the timestamps of the target file.\n   432: ///\n   433: /// # Platform-specific behavior\n   434: ///\n   435: /// This function currently corresponds to the `utimensat` function on Unix platforms, the\n   436: /// `setattrlist` function on Apple platforms, and the `SetFileTime` function on Windows.",
    "nanvix_source": "   409: /// ```no_run\n   410: /// use std::fs;\n   411: ///\n   412: /// fn main() -> std::io::Result<()> {\n   413: ///     fs::write(\"foo.txt\", b\"Lorem ipsum\")?;\n   414: ///     fs::write(\"bar.txt\", \"dolor sit\")?;\n   415: ///     Ok(())\n   416: /// }\n   417: /// ```\n   418: #[stable(feature = \"fs_read_write_bytes\", since = \"1.26.0\")]\n   419: pub fn write<P: AsRef<Path>, C: AsRef<[u8]>>(path: P, contents: C) -> io::Result<()> {\n   420:     fn inner(path: &Path, contents: &[u8]) -> io::Result<()> {\n   421:         File::create(path)?.write_all(contents)\n   422:     }\n   423:     inner(path.as_ref(), contents.as_ref())\n   424: }\n   425: \n   426: /// Changes the timestamps of the file or directory at the specified path.\n   427: ///\n   428: /// This function will attempt to set the access and modification times\n   429: /// to the times specified. If the path refers to a symbolic link, this function",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::BufReader::buffer",
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
      "name": "buffer",
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
                    "type": {
                      "generic": "R"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2552,
            "path": "BufReader"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 8,
                          "path": "Sized"
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
          "where_predicates": []
        },
        "impl_id": "std:3237",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2552",
        "resolved_owner_path": [
          "std",
          "io",
          "buffered",
          "bufreader",
          "BufReader"
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
            "lifetime": null,
            "type": {
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "   210:     /// ```no_run\n   211:     /// use std::io::{BufReader, BufRead};\n   212:     /// use std::fs::File;\n   213:     ///\n   214:     /// fn main() -> std::io::Result<()> {\n   215:     ///     let f = File::open(\"log.txt\")?;\n   216:     ///     let mut reader = BufReader::new(f);\n   217:     ///     assert!(reader.buffer().is_empty());\n   218:     ///\n   219:     ///     if reader.fill_buf()?.len() > 0 {\n   220:     ///         assert!(!reader.buffer().is_empty());\n   221:     ///     }\n   222:     ///     Ok(())\n   223:     /// }\n   224:     /// ```\n   225:     #[stable(feature = \"bufreader_buffer\", since = \"1.37.0\")]\n   226:     pub fn buffer(&self) -> &[u8] {\n   227:         self.buf.buffer()\n   228:     }\n   229: \n   230:     /// Returns the number of bytes the internal buffer can hold at once.\n   231:     ///\n   232:     /// # Examples\n   233:     ///\n   234:     /// ```no_run\n   235:     /// use std::io::{BufReader, BufRead};\n   236:     /// use std::fs::File;\n   237:     ///\n   238:     /// fn main() -> std::io::Result<()> {\n   239:     ///     let f = File::open(\"log.txt\")?;\n   240:     ///     let mut reader = BufReader::new(f);\n   241:     ///\n   242:     ///     let capacity = reader.capacity();",
    "nanvix_source": "   217:     ///     let mut reader = BufReader::new(f);\n   218:     ///     assert!(reader.buffer().is_empty());\n   219:     ///\n   220:     ///     if reader.fill_buf()?.len() > 0 {\n   221:     ///         assert!(!reader.buffer().is_empty());\n   222:     ///     }\n   223:     ///     Ok(())\n   224:     /// }\n   225:     /// ```\n   226:     #[stable(feature = \"bufreader_buffer\", since = \"1.37.0\")]\n   227:     pub fn buffer(&self) -> &[u8] {\n   228:         self.buf.buffer()\n   229:     }\n   230: \n   231:     /// Returns the number of bytes the internal buffer can hold at once.\n   232:     ///\n   233:     /// # Examples\n   234:     ///\n   235:     /// ```no_run\n   236:     /// use std::io::{BufReader, BufRead};\n   237:     /// use std::fs::File;",
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
