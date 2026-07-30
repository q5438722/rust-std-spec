For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::try_exists",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
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
      "name": "try_exists",
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
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
    "verification_source": "  3534:     /// where those bugs are not an issue.\n  3535:     ///\n  3536:     /// This is an alias for [`std::fs::exists`](crate::fs::exists).\n  3537:     ///\n  3538:     /// # Examples\n  3539:     ///\n  3540:     /// ```no_run\n  3541:     /// use std::path::Path;\n  3542:     /// assert!(!Path::new(\"does_not_exist.txt\").try_exists().expect(\"Can't check existence of file does_not_exist.txt\"));\n  3543:     /// assert!(Path::new(\"/root/secret_file.txt\").try_exists().is_err());\n  3544:     /// ```\n  3545:     ///\n  3546:     /// [TOCTOU]: fs#time-of-check-to-time-of-use-toctou\n  3547:     /// [`exists()`]: Self::exists\n  3548:     #[stable(feature = \"path_try_exists\", since = \"1.63.0\")]\n  3549:     #[inline]\n  3550:     pub fn try_exists(&self) -> io::Result<bool> {\n  3551:         fs::exists(self)\n  3552:     }\n  3553: \n  3554:     /// Returns `true` if the path exists on disk and is pointing at a regular file.\n  3555:     ///\n  3556:     /// This function will traverse symbolic links to query information about the\n  3557:     /// destination file.\n  3558:     ///\n  3559:     /// If you cannot access the metadata of the file, e.g. because of a\n  3560:     /// permission error or broken symbolic links, this will return `false`.\n  3561:     ///\n  3562:     /// # Examples\n  3563:     ///\n  3564:     /// ```no_run\n  3565:     /// use std::path::Path;\n  3566:     /// assert_eq!(Path::new(\"./is_a_directory/\").is_file(), false);",
    "nanvix_source": "  3570:     /// ```no_run\n  3571:     /// use std::path::Path;\n  3572:     /// assert!(!Path::new(\"does_not_exist.txt\").try_exists().expect(\"Can't check existence of file does_not_exist.txt\"));\n  3573:     /// assert!(Path::new(\"/root/secret_file.txt\").try_exists().is_err());\n  3574:     /// ```\n  3575:     ///\n  3576:     /// [TOCTOU]: fs#time-of-check-to-time-of-use-toctou\n  3577:     /// [`exists()`]: Self::exists\n  3578:     #[stable(feature = \"path_try_exists\", since = \"1.63.0\")]\n  3579:     #[inline]\n  3580:     pub fn try_exists(&self) -> io::Result<bool> {\n  3581:         fs::exists(self)\n  3582:     }\n  3583: \n  3584:     /// Returns `true` if the path exists on disk and is pointing at a regular file.\n  3585:     ///\n  3586:     /// This function will traverse symbolic links to query information about the\n  3587:     /// destination file.\n  3588:     ///\n  3589:     /// If you cannot access the metadata of the file, e.g. because of a\n  3590:     /// permission error or broken symbolic links, this will return `false`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::with_added_extension",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
                                    "id": 1857,
                                    "path": "OsStr"
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
            "name": "S"
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
      "name": "with_added_extension",
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
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
            "extension",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        }
      }
    },
    "verification_source": "  3158:     /// See [`PathBuf::add_extension`] for more details.\n  3159:     ///\n  3160:     /// # Examples\n  3161:     ///\n  3162:     /// ```\n  3163:     /// use std::path::{Path, PathBuf};\n  3164:     ///\n  3165:     /// let path = Path::new(\"foo.rs\");\n  3166:     /// assert_eq!(path.with_added_extension(\"txt\"), PathBuf::from(\"foo.rs.txt\"));\n  3167:     ///\n  3168:     /// let path = Path::new(\"foo.tar.gz\");\n  3169:     /// assert_eq!(path.with_added_extension(\"\"), PathBuf::from(\"foo.tar.gz\"));\n  3170:     /// assert_eq!(path.with_added_extension(\"xz\"), PathBuf::from(\"foo.tar.gz.xz\"));\n  3171:     /// assert_eq!(path.with_added_extension(\"\").with_added_extension(\"txt\"), PathBuf::from(\"foo.tar.gz.txt\"));\n  3172:     /// ```\n  3173:     #[stable(feature = \"path_add_extension\", since = \"1.91.0\")]\n  3174:     pub fn with_added_extension<S: AsRef<OsStr>>(&self, extension: S) -> PathBuf {\n  3175:         let mut new_path = self.to_path_buf();\n  3176:         new_path.add_extension(extension);\n  3177:         new_path\n  3178:     }\n  3179: \n  3180:     /// Produces an iterator over the [`Component`]s of the path.\n  3181:     ///\n  3182:     /// When parsing the path, there is a small amount of normalization:\n  3183:     ///\n  3184:     /// * Repeated separators are ignored, so `a/b` and `a//b` both have\n  3185:     ///   `a` and `b` as components.\n  3186:     ///\n  3187:     /// * Occurrences of `.` are normalized away, except if they are at the\n  3188:     ///   beginning of the path. For example, `a/./b`, `a/b/`, `a/b/.` and\n  3189:     ///   `a/b` all have `a` and `b` as components, but `./a/b` starts with\n  3190:     ///   an additional [`CurDir`] component.",
    "nanvix_source": "  3194:     /// assert_eq!(path.with_added_extension(\"\").with_added_extension(\"txt\"), PathBuf::from(\"foo.tar.gz.txt\"));\n  3195:     ///\n  3196:     /// let path = Path::new(\"/\");\n  3197:     /// assert_eq!(path.with_added_extension(\"gz\"), PathBuf::from(\"/\"));\n  3198:     /// let path = Path::new(\"/dir/\");\n  3199:     /// assert_eq!(path.with_added_extension(\"gz\"), PathBuf::from(\"/dir.gz\"));\n  3200:     /// let path = Path::new(\"/dir/..\");\n  3201:     /// assert_eq!(path.with_added_extension(\"gz\"), PathBuf::from(\"/dir/..\"));\n  3202:     /// ```\n  3203:     #[stable(feature = \"path_add_extension\", since = \"1.91.0\")]\n  3204:     pub fn with_added_extension<S: AsRef<OsStr>>(&self, extension: S) -> PathBuf {\n  3205:         let mut new_path = self.to_path_buf();\n  3206:         new_path.add_extension(extension);\n  3207:         new_path\n  3208:     }\n  3209: \n  3210:     /// Produces an iterator over the [`Component`]s of the path.\n  3211:     ///\n  3212:     /// When parsing the path, there is a small amount of normalization:\n  3213:     ///\n  3214:     /// * Repeated separators are ignored, so `a/b` and `a//b` both have",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::with_extension",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
                                    "id": 1857,
                                    "path": "OsStr"
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
            "name": "S"
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
      "name": "with_extension",
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
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
            "extension",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        }
      }
    },
    "verification_source": "  3111:     /// use std::path::Path;\n  3112:     ///\n  3113:     /// let path = Path::new(\"foo.tar.gz\");\n  3114:     /// assert_eq!(path.with_extension(\"xz\"), Path::new(\"foo.tar.xz\"));\n  3115:     /// assert_eq!(path.with_extension(\"\").with_extension(\"txt\"), Path::new(\"foo.txt\"));\n  3116:     /// ```\n  3117:     ///\n  3118:     /// Adding an extension where one did not exist:\n  3119:     ///\n  3120:     /// ```\n  3121:     /// use std::path::Path;\n  3122:     ///\n  3123:     /// let path = Path::new(\"foo\");\n  3124:     /// assert_eq!(path.with_extension(\"rs\"), Path::new(\"foo.rs\"));\n  3125:     /// ```\n  3126:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3127:     pub fn with_extension<S: AsRef<OsStr>>(&self, extension: S) -> PathBuf {\n  3128:         self._with_extension(extension.as_ref())\n  3129:     }\n  3130: \n  3131:     fn _with_extension(&self, extension: &OsStr) -> PathBuf {\n  3132:         let self_len = self.as_os_str().len();\n  3133:         let self_bytes = self.as_os_str().as_encoded_bytes();\n  3134: \n  3135:         let (new_capacity, slice_to_copy) = match self.extension() {\n  3136:             None => {\n  3137:                 // Enough capacity for the extension and the dot\n  3138:                 let capacity = self_len + extension.len() + 1;\n  3139:                 let whole_path = self_bytes;\n  3140:                 (capacity, whole_path)\n  3141:             }\n  3142:             Some(previous_extension) => {\n  3143:                 let capacity = self_len + extension.len() - previous_extension.len();",
    "nanvix_source": "  3138:     ///\n  3139:     /// Adding an extension where one did not exist:\n  3140:     ///\n  3141:     /// ```\n  3142:     /// use std::path::Path;\n  3143:     ///\n  3144:     /// let path = Path::new(\"foo\");\n  3145:     /// assert_eq!(path.with_extension(\"rs\"), Path::new(\"foo.rs\"));\n  3146:     /// ```\n  3147:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3148:     pub fn with_extension<S: AsRef<OsStr>>(&self, extension: S) -> PathBuf {\n  3149:         self._with_extension(extension.as_ref())\n  3150:     }\n  3151: \n  3152:     fn _with_extension(&self, extension: &OsStr) -> PathBuf {\n  3153:         let self_len = self.as_os_str().len();\n  3154:         let self_bytes = self.as_os_str().as_encoded_bytes();\n  3155: \n  3156:         let (new_capacity, slice_to_copy) = match self.extension() {\n  3157:             None => {\n  3158:                 // Enough capacity for the extension and the dot",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::with_file_name",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
                                    "id": 1857,
                                    "path": "OsStr"
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
            "name": "S"
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
      "name": "with_file_name",
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
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
            "file_name",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        }
      }
    },
    "verification_source": "  3068:     /// See [`PathBuf::set_file_name`] for more details.\n  3069:     ///\n  3070:     /// # Examples\n  3071:     ///\n  3072:     /// ```\n  3073:     /// use std::path::{Path, PathBuf};\n  3074:     ///\n  3075:     /// let path = Path::new(\"/tmp/foo.png\");\n  3076:     /// assert_eq!(path.with_file_name(\"bar\"), PathBuf::from(\"/tmp/bar\"));\n  3077:     /// assert_eq!(path.with_file_name(\"bar.txt\"), PathBuf::from(\"/tmp/bar.txt\"));\n  3078:     ///\n  3079:     /// let path = Path::new(\"/tmp\");\n  3080:     /// assert_eq!(path.with_file_name(\"var\"), PathBuf::from(\"/var\"));\n  3081:     /// ```\n  3082:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3083:     #[must_use]\n  3084:     pub fn with_file_name<S: AsRef<OsStr>>(&self, file_name: S) -> PathBuf {\n  3085:         self._with_file_name(file_name.as_ref())\n  3086:     }\n  3087: \n  3088:     fn _with_file_name(&self, file_name: &OsStr) -> PathBuf {\n  3089:         let mut buf = self.to_path_buf();\n  3090:         buf.set_file_name(file_name);\n  3091:         buf\n  3092:     }\n  3093: \n  3094:     /// Creates an owned [`PathBuf`] like `self` but with the given extension.\n  3095:     ///\n  3096:     /// See [`PathBuf::set_extension`] for more details.\n  3097:     ///\n  3098:     /// # Examples\n  3099:     ///\n  3100:     /// ```",
    "nanvix_source": "  3095:     ///\n  3096:     /// let path = Path::new(\"/tmp/foo.png\");\n  3097:     /// assert_eq!(path.with_file_name(\"bar\"), PathBuf::from(\"/tmp/bar\"));\n  3098:     /// assert_eq!(path.with_file_name(\"bar.txt\"), PathBuf::from(\"/tmp/bar.txt\"));\n  3099:     ///\n  3100:     /// let path = Path::new(\"/tmp\");\n  3101:     /// assert_eq!(path.with_file_name(\"var\"), PathBuf::from(\"/var\"));\n  3102:     /// ```\n  3103:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3104:     #[must_use]\n  3105:     pub fn with_file_name<S: AsRef<OsStr>>(&self, file_name: S) -> PathBuf {\n  3106:         self._with_file_name(file_name.as_ref())\n  3107:     }\n  3108: \n  3109:     fn _with_file_name(&self, file_name: &OsStr) -> PathBuf {\n  3110:         let mut buf = self.to_path_buf();\n  3111:         buf.set_file_name(file_name);\n  3112:         buf\n  3113:     }\n  3114: \n  3115:     /// Creates an owned [`PathBuf`] like `self` but with the given extension.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::add_extension",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
                                    "id": 1857,
                                    "path": "OsStr"
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
            "name": "S"
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
      "name": "add_extension",
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
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
        ],
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
            "extension",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1712:     /// p.add_extension(\"formatted\");\n  1713:     /// assert_eq!(Path::new(\"/feel/the.formatted\"), p.as_path());\n  1714:     ///\n  1715:     /// p.add_extension(\"dark.side\");\n  1716:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark.side\"), p.as_path());\n  1717:     ///\n  1718:     /// p.set_extension(\"cookie\");\n  1719:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark.cookie\"), p.as_path());\n  1720:     ///\n  1721:     /// p.set_extension(\"\");\n  1722:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark\"), p.as_path());\n  1723:     ///\n  1724:     /// p.add_extension(\"\");\n  1725:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark\"), p.as_path());\n  1726:     /// ```\n  1727:     #[stable(feature = \"path_add_extension\", since = \"1.91.0\")]\n  1728:     pub fn add_extension<S: AsRef<OsStr>>(&mut self, extension: S) -> bool {\n  1729:         self._add_extension(extension.as_ref())\n  1730:     }\n  1731: \n  1732:     fn _add_extension(&mut self, extension: &OsStr) -> bool {\n  1733:         validate_extension(extension);\n  1734: \n  1735:         let file_name = match self.file_name() {\n  1736:             None => return false,\n  1737:             Some(f) => f.as_encoded_bytes(),\n  1738:         };\n  1739: \n  1740:         let new = extension.as_encoded_bytes();\n  1741:         if !new.is_empty() {\n  1742:             // truncate until right after the file name\n  1743:             // this is necessary for trimming the trailing separator\n  1744:             let end_file_name = file_name[file_name.len()..].as_ptr().addr();",
    "nanvix_source": "  1718:     /// p.set_extension(\"cookie\");\n  1719:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark.cookie\"), p.as_path());\n  1720:     ///\n  1721:     /// p.set_extension(\"\");\n  1722:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark\"), p.as_path());\n  1723:     ///\n  1724:     /// p.add_extension(\"\");\n  1725:     /// assert_eq!(Path::new(\"/feel/the.formatted.dark\"), p.as_path());\n  1726:     /// ```\n  1727:     #[stable(feature = \"path_add_extension\", since = \"1.91.0\")]\n  1728:     pub fn add_extension<S: AsRef<OsStr>>(&mut self, extension: S) -> bool {\n  1729:         self._add_extension(extension.as_ref())\n  1730:     }\n  1731: \n  1732:     fn _add_extension(&mut self, extension: &OsStr) -> bool {\n  1733:         validate_extension(extension);\n  1734: \n  1735:         let file_name = match self.file_name() {\n  1736:             None => return false,\n  1737:             Some(f) => f.as_encoded_bytes(),\n  1738:         };",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::as_path",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "as_path",
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
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
              "resolved_path": {
                "args": null,
                "id": 1802,
                "path": "Path"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1259:     }\n  1260: \n  1261:     /// Coerces to a [`Path`] slice.\n  1262:     ///\n  1263:     /// # Examples\n  1264:     ///\n  1265:     /// ```\n  1266:     /// use std::path::{Path, PathBuf};\n  1267:     ///\n  1268:     /// let p = PathBuf::from(\"/test\");\n  1269:     /// assert_eq!(Path::new(\"/test\"), p.as_path());\n  1270:     /// ```\n  1271:     #[cfg_attr(not(test), rustc_diagnostic_item = \"pathbuf_as_path\")]\n  1272:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1273:     #[must_use]\n  1274:     #[inline]\n  1275:     pub fn as_path(&self) -> &Path {\n  1276:         self\n  1277:     }\n  1278: \n  1279:     /// Consumes and leaks the `PathBuf`, returning a mutable reference to the contents,\n  1280:     /// `&'a mut Path`.\n  1281:     ///\n  1282:     /// The caller has free choice over the returned lifetime, including 'static.\n  1283:     /// Indeed, this function is ideally used for data that lives for the remainder of\n  1284:     /// the program's life, as dropping the returned reference will cause a memory leak.\n  1285:     ///\n  1286:     /// It does not reallocate or shrink the `PathBuf`, so the leaked allocation may include\n  1287:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n  1288:     /// capacity, call [`into_boxed_path`], and then [`Box::leak`] instead.\n  1289:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n  1290:     ///\n  1291:     /// [`into_boxed_path`]: Self::into_boxed_path",
    "nanvix_source": "  1265:     /// ```\n  1266:     /// use std::path::{Path, PathBuf};\n  1267:     ///\n  1268:     /// let p = PathBuf::from(\"/test\");\n  1269:     /// assert_eq!(Path::new(\"/test\"), p.as_path());\n  1270:     /// ```\n  1271:     #[cfg_attr(not(test), rustc_diagnostic_item = \"pathbuf_as_path\")]\n  1272:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1273:     #[must_use]\n  1274:     #[inline]\n  1275:     pub fn as_path(&self) -> &Path {\n  1276:         self\n  1277:     }\n  1278: \n  1279:     /// Consumes and leaks the `PathBuf`, returning a mutable reference to the contents,\n  1280:     /// `&'a mut Path`.\n  1281:     ///\n  1282:     /// The caller has free choice over the returned lifetime, including 'static.\n  1283:     /// Indeed, this function is ideally used for data that lives for the remainder of\n  1284:     /// the program's life, as dropping the returned reference will cause a memory leak.\n  1285:     ///",
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
