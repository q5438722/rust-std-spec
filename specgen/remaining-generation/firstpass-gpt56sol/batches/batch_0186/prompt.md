For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::env::var_os",
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
                                    "id": 1857,
                                    "path": "crate::ffi::OsStr"
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
            "name": "K"
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
      "name": "var_os",
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
            "key",
            {
              "generic": "K"
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
                        "id": 1846,
                        "path": "crate::ffi::OsString"
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
    "verification_source": "   243: /// # Examples\n   244: ///\n   245: /// ```\n   246: /// use std::env;\n   247: ///\n   248: /// let key = \"HOME\";\n   249: /// match env::var_os(key) {\n   250: ///     Some(val) => println!(\"{key}: {val:?}\"),\n   251: ///     None => println!(\"{key} is not defined in the environment.\")\n   252: /// }\n   253: /// ```\n   254: ///\n   255: /// If expecting a delimited variable (such as `PATH`), [`split_paths`]\n   256: /// can be used to separate items.\n   257: #[must_use]\n   258: #[stable(feature = \"env\", since = \"1.0.0\")]\n   259: pub fn var_os<K: AsRef<OsStr>>(key: K) -> Option<OsString> {\n   260:     _var_os(key.as_ref())\n   261: }\n   262: \n   263: fn _var_os(key: &OsStr) -> Option<OsString> {\n   264:     env_imp::getenv(key)\n   265: }\n   266: \n   267: /// The error type for operations interacting with environment variables.\n   268: /// Possibly returned from [`env::var()`].\n   269: ///\n   270: /// [`env::var()`]: var\n   271: #[derive(Debug, PartialEq, Eq, Clone)]\n   272: #[stable(feature = \"env\", since = \"1.0.0\")]\n   273: pub enum VarError {\n   274:     /// The specified environment variable was not present in the current\n   275:     /// process's environment.",
    "nanvix_source": "   254: /// match env::var_os(key) {\n   255: ///     Some(val) => println!(\"{key}: {val:?}\"),\n   256: ///     None => println!(\"{key} is not defined in the environment.\")\n   257: /// }\n   258: /// ```\n   259: ///\n   260: /// If expecting a delimited variable (such as `PATH`), [`split_paths`]\n   261: /// can be used to separate items.\n   262: #[must_use]\n   263: #[stable(feature = \"env\", since = \"1.0.0\")]\n   264: pub fn var_os<K: AsRef<OsStr>>(key: K) -> Option<OsString> {\n   265:     env_imp::getenv(key.as_ref())\n   266: }\n   267: \n   268: /// The error type for operations interacting with environment variables.\n   269: /// Possibly returned from [`env::var()`].\n   270: ///\n   271: /// [`env::var()`]: var\n   272: #[derive(Debug, PartialEq, Eq, Clone)]\n   273: #[stable(feature = \"env\", since = \"1.0.0\")]\n   274: pub enum VarError {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::vars",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "vars",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1805,
            "path": "Vars"
          }
        }
      }
    },
    "verification_source": "   113: /// While iterating, the returned iterator will panic if any key or value in the\n   114: /// environment is not valid unicode. If this is not desired, consider using\n   115: /// [`env::vars_os()`].\n   116: ///\n   117: /// # Examples\n   118: ///\n   119: /// ```\n   120: /// // Print all environment variables.\n   121: /// for (key, value) in std::env::vars() {\n   122: ///     println!(\"{key}: {value}\");\n   123: /// }\n   124: /// ```\n   125: ///\n   126: /// [`env::vars_os()`]: vars_os\n   127: #[must_use]\n   128: #[stable(feature = \"env\", since = \"1.0.0\")]\n   129: pub fn vars() -> Vars {\n   130:     Vars { inner: vars_os() }\n   131: }\n   132: \n   133: /// Returns an iterator of (variable, value) pairs of OS strings, for all the\n   134: /// environment variables of the current process.\n   135: ///\n   136: /// The returned iterator contains a snapshot of the process's environment\n   137: /// variables at the time of this invocation. Modifications to environment\n   138: /// variables afterwards will not be reflected in the returned iterator.\n   139: ///\n   140: /// Note that the returned iterator will not check if the environment variables\n   141: /// are valid Unicode. If you want to panic on invalid UTF-8,\n   142: /// use the [`vars`] function instead.\n   143: ///\n   144: /// # Examples\n   145: ///",
    "nanvix_source": "   125: /// ```\n   126: /// // Print all environment variables.\n   127: /// for (key, value) in std::env::vars() {\n   128: ///     println!(\"{key}: {value}\");\n   129: /// }\n   130: /// ```\n   131: ///\n   132: /// [`env::vars_os()`]: vars_os\n   133: #[must_use]\n   134: #[stable(feature = \"env\", since = \"1.0.0\")]\n   135: pub fn vars() -> Vars {\n   136:     Vars { inner: vars_os() }\n   137: }\n   138: \n   139: /// Returns an iterator of (variable, value) pairs of OS strings, for all the\n   140: /// environment variables of the current process.\n   141: ///\n   142: /// The returned iterator contains a snapshot of the process's environment\n   143: /// variables at the time of this invocation. Modifications to environment\n   144: /// variables afterwards will not be reflected in the returned iterator.\n   145: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::vars_os",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "vars_os",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1829,
            "path": "VarsOs"
          }
        }
      }
    },
    "verification_source": "   138: /// variables afterwards will not be reflected in the returned iterator.\n   139: ///\n   140: /// Note that the returned iterator will not check if the environment variables\n   141: /// are valid Unicode. If you want to panic on invalid UTF-8,\n   142: /// use the [`vars`] function instead.\n   143: ///\n   144: /// # Examples\n   145: ///\n   146: /// ```\n   147: /// // Print all environment variables.\n   148: /// for (key, value) in std::env::vars_os() {\n   149: ///     println!(\"{key:?}: {value:?}\");\n   150: /// }\n   151: /// ```\n   152: #[must_use]\n   153: #[stable(feature = \"env\", since = \"1.0.0\")]\n   154: pub fn vars_os() -> VarsOs {\n   155:     VarsOs { inner: env_imp::env() }\n   156: }\n   157: \n   158: #[stable(feature = \"env\", since = \"1.0.0\")]\n   159: impl Iterator for Vars {\n   160:     type Item = (String, String);\n   161:     fn next(&mut self) -> Option<(String, String)> {\n   162:         self.inner.next().map(|(a, b)| (a.into_string().unwrap(), b.into_string().unwrap()))\n   163:     }\n   164:     fn size_hint(&self) -> (usize, Option<usize>) {\n   165:         self.inner.size_hint()\n   166:     }\n   167: }\n   168: \n   169: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   170: impl fmt::Debug for Vars {",
    "nanvix_source": "   150: /// # Examples\n   151: ///\n   152: /// ```\n   153: /// // Print all environment variables.\n   154: /// for (key, value) in std::env::vars_os() {\n   155: ///     println!(\"{key:?}: {value:?}\");\n   156: /// }\n   157: /// ```\n   158: #[must_use]\n   159: #[stable(feature = \"env\", since = \"1.0.0\")]\n   160: pub fn vars_os() -> VarsOs {\n   161:     VarsOs { inner: env_imp::env() }\n   162: }\n   163: \n   164: #[stable(feature = \"env\", since = \"1.0.0\")]\n   165: impl Iterator for Vars {\n   166:     type Item = (String, String);\n   167:     fn next(&mut self) -> Option<(String, String)> {\n   168:         self.inner.next().map(|(a, b)| (a.into_string().unwrap(), b.into_string().unwrap()))\n   169:     }\n   170:     fn size_hint(&self) -> (usize, Option<usize>) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirBuilder::create",
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
      "name": "create",
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
            "id": 3107,
            "path": "DirBuilder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3111",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3107",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirBuilder"
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
    "verification_source": "  3427:     /// It is considered an error if the directory already exists unless\n  3428:     /// recursive mode is enabled.\n  3429:     ///\n  3430:     /// # Examples\n  3431:     ///\n  3432:     /// ```no_run\n  3433:     /// use std::fs::{self, DirBuilder};\n  3434:     ///\n  3435:     /// let path = \"/tmp/foo/bar/baz\";\n  3436:     /// DirBuilder::new()\n  3437:     ///     .recursive(true)\n  3438:     ///     .create(path).unwrap();\n  3439:     ///\n  3440:     /// assert!(fs::metadata(path).unwrap().is_dir());\n  3441:     /// ```\n  3442:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3443:     pub fn create<P: AsRef<Path>>(&self, path: P) -> io::Result<()> {\n  3444:         self._create(path.as_ref())\n  3445:     }\n  3446: \n  3447:     fn _create(&self, path: &Path) -> io::Result<()> {\n  3448:         if self.recursive { self.create_dir_all(path) } else { self.inner.mkdir(path) }\n  3449:     }\n  3450: \n  3451:     fn create_dir_all(&self, path: &Path) -> io::Result<()> {\n  3452:         // if path's parent is None, it is \"/\" path, which should\n  3453:         // return Ok immediately\n  3454:         if path == Path::new(\"\") || path.parent() == None {\n  3455:             return Ok(());\n  3456:         }\n  3457: \n  3458:         let ancestors = path.ancestors();\n  3459:         let mut uncreated_dirs = 0;",
    "nanvix_source": "  3407:     /// use std::fs::{self, DirBuilder};\n  3408:     ///\n  3409:     /// let path = \"/tmp/foo/bar/baz\";\n  3410:     /// DirBuilder::new()\n  3411:     ///     .recursive(true)\n  3412:     ///     .create(path).unwrap();\n  3413:     ///\n  3414:     /// assert!(fs::metadata(path).unwrap().is_dir());\n  3415:     /// ```\n  3416:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3417:     pub fn create<P: AsRef<Path>>(&self, path: P) -> io::Result<()> {\n  3418:         self._create(path.as_ref())\n  3419:     }\n  3420: \n  3421:     fn _create(&self, path: &Path) -> io::Result<()> {\n  3422:         if self.recursive { self.create_dir_all(path) } else { self.inner.mkdir(path) }\n  3423:     }\n  3424: \n  3425:     fn create_dir_all(&self, path: &Path) -> io::Result<()> {\n  3426:         // if path's parent is None, it is \"/\" path, which should\n  3427:         // return Ok immediately",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirBuilder::new",
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
      "name": "new",
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
            "id": 3107,
            "path": "DirBuilder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3111",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3107",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirBuilder"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 3107,
            "path": "DirBuilder"
          }
        }
      }
    },
    "verification_source": "  3384:     fs_imp::set_permissions_nofollow(path.as_ref(), perm)\n  3385: }\n  3386: \n  3387: impl DirBuilder {\n  3388:     /// Creates a new set of options with default mode/security settings for all\n  3389:     /// platforms and also non-recursive.\n  3390:     ///\n  3391:     /// # Examples\n  3392:     ///\n  3393:     /// ```\n  3394:     /// use std::fs::DirBuilder;\n  3395:     ///\n  3396:     /// let builder = DirBuilder::new();\n  3397:     /// ```\n  3398:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3399:     #[must_use]\n  3400:     pub fn new() -> DirBuilder {\n  3401:         DirBuilder { inner: fs_imp::DirBuilder::new(), recursive: false }\n  3402:     }\n  3403: \n  3404:     /// Indicates that directories should be created recursively, creating all\n  3405:     /// parent directories. Parents that do not exist are created with the same\n  3406:     /// security and permissions settings.\n  3407:     ///\n  3408:     /// This option defaults to `false`.\n  3409:     ///\n  3410:     /// # Examples\n  3411:     ///\n  3412:     /// ```\n  3413:     /// use std::fs::DirBuilder;\n  3414:     ///\n  3415:     /// let mut builder = DirBuilder::new();\n  3416:     /// builder.recursive(true);",
    "nanvix_source": "  3364:     ///\n  3365:     /// # Examples\n  3366:     ///\n  3367:     /// ```\n  3368:     /// use std::fs::DirBuilder;\n  3369:     ///\n  3370:     /// let builder = DirBuilder::new();\n  3371:     /// ```\n  3372:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3373:     #[must_use]\n  3374:     pub fn new() -> DirBuilder {\n  3375:         DirBuilder { inner: fs_imp::DirBuilder::new(), recursive: false }\n  3376:     }\n  3377: \n  3378:     /// Indicates that directories should be created recursively, creating all\n  3379:     /// parent directories. Parents that do not exist are created with the same\n  3380:     /// security and permissions settings.\n  3381:     ///\n  3382:     /// This option defaults to `false`.\n  3383:     ///\n  3384:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirBuilder::recursive",
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
      "name": "recursive",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 3107,
            "path": "DirBuilder"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3111",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3107",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirBuilder"
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
            "recursive",
            {
              "primitive": "bool"
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
    "verification_source": "  3403: \n  3404:     /// Indicates that directories should be created recursively, creating all\n  3405:     /// parent directories. Parents that do not exist are created with the same\n  3406:     /// security and permissions settings.\n  3407:     ///\n  3408:     /// This option defaults to `false`.\n  3409:     ///\n  3410:     /// # Examples\n  3411:     ///\n  3412:     /// ```\n  3413:     /// use std::fs::DirBuilder;\n  3414:     ///\n  3415:     /// let mut builder = DirBuilder::new();\n  3416:     /// builder.recursive(true);\n  3417:     /// ```\n  3418:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3419:     pub fn recursive(&mut self, recursive: bool) -> &mut Self {\n  3420:         self.recursive = recursive;\n  3421:         self\n  3422:     }\n  3423: \n  3424:     /// Creates the specified directory with the options configured in this\n  3425:     /// builder.\n  3426:     ///\n  3427:     /// It is considered an error if the directory already exists unless\n  3428:     /// recursive mode is enabled.\n  3429:     ///\n  3430:     /// # Examples\n  3431:     ///\n  3432:     /// ```no_run\n  3433:     /// use std::fs::{self, DirBuilder};\n  3434:     ///\n  3435:     /// let path = \"/tmp/foo/bar/baz\";",
    "nanvix_source": "  3383:     ///\n  3384:     /// # Examples\n  3385:     ///\n  3386:     /// ```\n  3387:     /// use std::fs::DirBuilder;\n  3388:     ///\n  3389:     /// let mut builder = DirBuilder::new();\n  3390:     /// builder.recursive(true);\n  3391:     /// ```\n  3392:     #[stable(feature = \"dir_builder\", since = \"1.6.0\")]\n  3393:     pub fn recursive(&mut self, recursive: bool) -> &mut Self {\n  3394:         self.recursive = recursive;\n  3395:         self\n  3396:     }\n  3397: \n  3398:     /// Creates the specified directory with the options configured in this\n  3399:     /// builder.\n  3400:     ///\n  3401:     /// It is considered an error if the directory already exists unless\n  3402:     /// recursive mode is enabled.\n  3403:     ///",
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
