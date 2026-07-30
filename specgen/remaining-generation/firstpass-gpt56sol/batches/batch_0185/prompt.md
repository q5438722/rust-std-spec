For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::env::remove_var",
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
      "external_or_hidden_runtime_state",
      "unit_return_variant"
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
        "is_unsafe": true
      },
      "name": "remove_var",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
        "output": null
      }
    },
    "verification_source": "   413: ///\n   414: /// let key = \"KEY\";\n   415: /// unsafe {\n   416: ///     env::set_var(key, \"VALUE\");\n   417: /// }\n   418: /// assert_eq!(env::var(key), Ok(\"VALUE\".to_string()));\n   419: ///\n   420: /// unsafe {\n   421: ///     env::remove_var(key);\n   422: /// }\n   423: /// assert!(env::var(key).is_err());\n   424: /// ```\n   425: #[rustc_deprecated_safe_2024(\n   426:     audit_that = \"the environment access only happens in single-threaded code\"\n   427: )]\n   428: #[stable(feature = \"env\", since = \"1.0.0\")]\n   429: pub unsafe fn remove_var<K: AsRef<OsStr>>(key: K) {\n   430:     let key = key.as_ref();\n   431:     unsafe { env_imp::unsetenv(key) }\n   432:         .unwrap_or_else(|e| panic!(\"failed to remove environment variable `{key:?}`: {e}\"))\n   433: }\n   434: \n   435: /// An iterator that splits an environment variable into paths according to\n   436: /// platform-specific conventions.\n   437: ///\n   438: /// The iterator element type is [`PathBuf`].\n   439: ///\n   440: /// This structure is created by [`env::split_paths()`]. See its\n   441: /// documentation for more.\n   442: ///\n   443: /// [`env::split_paths()`]: split_paths\n   444: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n   445: #[stable(feature = \"env\", since = \"1.0.0\")]",
    "nanvix_source": "   420: ///\n   421: /// unsafe {\n   422: ///     env::remove_var(key);\n   423: /// }\n   424: /// assert!(env::var(key).is_err());\n   425: /// ```\n   426: #[rustc_deprecated_safe_2024(\n   427:     audit_that = \"the environment access only happens in single-threaded code\"\n   428: )]\n   429: #[stable(feature = \"env\", since = \"1.0.0\")]\n   430: pub unsafe fn remove_var<K: AsRef<OsStr>>(key: K) {\n   431:     let key = key.as_ref();\n   432:     unsafe { env_imp::unsetenv(key) }\n   433:         .unwrap_or_else(|e| panic!(\"failed to remove environment variable `{key:?}`: {e}\"))\n   434: }\n   435: \n   436: /// An iterator that splits an environment variable into paths according to\n   437: /// platform-specific conventions.\n   438: ///\n   439: /// The iterator element type is [`PathBuf`].\n   440: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::set_current_dir",
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
      "name": "set_current_dir",
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
    "verification_source": "    64: /// Returns an [`Err`] if the operation fails.\n    65: ///\n    66: /// [currently]: crate::io#platform-specific-behavior\n    67: ///\n    68: /// # Examples\n    69: ///\n    70: /// ```\n    71: /// use std::env;\n    72: /// use std::path::Path;\n    73: ///\n    74: /// let root = Path::new(\"/\");\n    75: /// assert!(env::set_current_dir(&root).is_ok());\n    76: /// println!(\"Successfully changed working directory to {}!\", root.display());\n    77: /// ```\n    78: #[doc(alias = \"chdir\", alias = \"SetCurrentDirectory\", alias = \"SetCurrentDirectoryW\")]\n    79: #[stable(feature = \"env\", since = \"1.0.0\")]\n    80: pub fn set_current_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n    81:     paths_imp::chdir(path.as_ref())\n    82: }\n    83: \n    84: /// An iterator over a snapshot of the environment variables of this process.\n    85: ///\n    86: /// This structure is created by [`env::vars()`]. See its documentation for more.\n    87: ///\n    88: /// [`env::vars()`]: vars\n    89: #[stable(feature = \"env\", since = \"1.0.0\")]\n    90: pub struct Vars {\n    91:     inner: VarsOs,\n    92: }\n    93: \n    94: /// An iterator over a snapshot of the environment variables of this process.\n    95: ///\n    96: /// This structure is created by [`env::vars_os()`]. See its documentation for more.",
    "nanvix_source": "    70: /// ```\n    71: /// use std::env;\n    72: /// use std::path::Path;\n    73: ///\n    74: /// let root = Path::new(\"/\");\n    75: /// assert!(env::set_current_dir(&root).is_ok());\n    76: /// println!(\"Successfully changed working directory to {}!\", root.display());\n    77: /// ```\n    78: #[doc(alias = \"chdir\", alias = \"SetCurrentDirectory\", alias = \"SetCurrentDirectoryW\")]\n    79: #[stable(feature = \"env\", since = \"1.0.0\")]\n    80: pub fn set_current_dir<P: AsRef<Path>>(path: P) -> io::Result<()> {\n    81:     paths_imp::chdir(path.as_ref())\n    82: }\n    83: \n    84: /// An iterator over a snapshot of the environment variables of this process.\n    85: ///\n    86: /// This structure is created by [`env::vars()`]. See its documentation for more.\n    87: ///\n    88: /// [`env::vars()`]: vars\n    89: #[stable(feature = \"env\", since = \"1.0.0\")]\n    90: pub struct Vars {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::set_var",
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
      "external_or_hidden_runtime_state",
      "unit_return_variant"
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
            "name": "V"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "set_var",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
          ],
          [
            "value",
            {
              "generic": "V"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   342: ///\n   343: /// # Examples\n   344: ///\n   345: /// ```\n   346: /// use std::env;\n   347: ///\n   348: /// let key = \"KEY\";\n   349: /// unsafe {\n   350: ///     env::set_var(key, \"VALUE\");\n   351: /// }\n   352: /// assert_eq!(env::var(key), Ok(\"VALUE\".to_string()));\n   353: /// ```\n   354: #[rustc_deprecated_safe_2024(\n   355:     audit_that = \"the environment access only happens in single-threaded code\"\n   356: )]\n   357: #[stable(feature = \"env\", since = \"1.0.0\")]\n   358: pub unsafe fn set_var<K: AsRef<OsStr>, V: AsRef<OsStr>>(key: K, value: V) {\n   359:     let (key, value) = (key.as_ref(), value.as_ref());\n   360:     unsafe { env_imp::setenv(key, value) }.unwrap_or_else(|e| {\n   361:         panic!(\"failed to set environment variable `{key:?}` to `{value:?}`: {e}\")\n   362:     })\n   363: }\n   364: \n   365: /// Removes an environment variable from the environment of the currently running process.\n   366: ///\n   367: /// # Safety\n   368: ///\n   369: /// This function is safe to call in a single-threaded program.\n   370: ///\n   371: /// This function is also always safe to call on Windows, in single-threaded\n   372: /// and multi-threaded programs.\n   373: ///\n   374: /// In multi-threaded programs on other operating systems, the only safe option is",
    "nanvix_source": "   349: /// let key = \"KEY\";\n   350: /// unsafe {\n   351: ///     env::set_var(key, \"VALUE\");\n   352: /// }\n   353: /// assert_eq!(env::var(key), Ok(\"VALUE\".to_string()));\n   354: /// ```\n   355: #[rustc_deprecated_safe_2024(\n   356:     audit_that = \"the environment access only happens in single-threaded code\"\n   357: )]\n   358: #[stable(feature = \"env\", since = \"1.0.0\")]\n   359: pub unsafe fn set_var<K: AsRef<OsStr>, V: AsRef<OsStr>>(key: K, value: V) {\n   360:     let (key, value) = (key.as_ref(), value.as_ref());\n   361:     unsafe { env_imp::setenv(key, value) }.unwrap_or_else(|e| {\n   362:         panic!(\"failed to set environment variable `{key:?}` to `{value:?}`: {e}\")\n   363:     })\n   364: }\n   365: \n   366: /// Removes an environment variable from the environment of the currently running process.\n   367: ///\n   368: /// # Safety\n   369: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::split_paths",
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
                  },
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
            "name": "T"
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
      "name": "split_paths",
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
            "unparsed",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "T"
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
            "id": 1895,
            "path": "SplitPaths"
          }
        }
      }
    },
    "verification_source": "   466: /// # Examples\n   467: ///\n   468: /// ```\n   469: /// use std::env;\n   470: ///\n   471: /// let key = \"PATH\";\n   472: /// match env::var_os(key) {\n   473: ///     Some(paths) => {\n   474: ///         for path in env::split_paths(&paths) {\n   475: ///             println!(\"'{}'\", path.display());\n   476: ///         }\n   477: ///     }\n   478: ///     None => println!(\"{key} is not defined in the environment.\")\n   479: /// }\n   480: /// ```\n   481: #[stable(feature = \"env\", since = \"1.0.0\")]\n   482: pub fn split_paths<T: AsRef<OsStr> + ?Sized>(unparsed: &T) -> SplitPaths<'_> {\n   483:     SplitPaths { inner: paths_imp::split_paths(unparsed.as_ref()) }\n   484: }\n   485: \n   486: #[stable(feature = \"env\", since = \"1.0.0\")]\n   487: impl<'a> Iterator for SplitPaths<'a> {\n   488:     type Item = PathBuf;\n   489:     fn next(&mut self) -> Option<PathBuf> {\n   490:         self.inner.next()\n   491:     }\n   492:     fn size_hint(&self) -> (usize, Option<usize>) {\n   493:         self.inner.size_hint()\n   494:     }\n   495: }\n   496: \n   497: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   498: impl fmt::Debug for SplitPaths<'_> {",
    "nanvix_source": "   473: /// match env::var_os(key) {\n   474: ///     Some(paths) => {\n   475: ///         for path in env::split_paths(&paths) {\n   476: ///             println!(\"'{}'\", path.display());\n   477: ///         }\n   478: ///     }\n   479: ///     None => println!(\"{key} is not defined in the environment.\")\n   480: /// }\n   481: /// ```\n   482: #[stable(feature = \"env\", since = \"1.0.0\")]\n   483: pub fn split_paths<T: AsRef<OsStr> + ?Sized>(unparsed: &T) -> SplitPaths<'_> {\n   484:     SplitPaths { inner: paths_imp::split_paths(unparsed.as_ref()) }\n   485: }\n   486: \n   487: #[stable(feature = \"env\", since = \"1.0.0\")]\n   488: impl<'a> Iterator for SplitPaths<'a> {\n   489:     type Item = PathBuf;\n   490:     fn next(&mut self) -> Option<PathBuf> {\n   491:         self.inner.next()\n   492:     }\n   493:     fn size_hint(&self) -> (usize, Option<usize>) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::temp_dir",
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
      "name": "temp_dir",
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
            "id": 1799,
            "path": "crate::path::PathBuf"
          }
        }
      }
    },
    "verification_source": "   687: /// [changes]: io#platform-specific-behavior\n   688: /// [GetTempPath2]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-gettemppath2a\n   689: /// [GetTempPath]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-gettemppatha\n   690: /// [appledoc]: https://developer.apple.com/library/archive/documentation/Security/Conceptual/SecureCodingGuide/Articles/RaceConditions.html#//apple_ref/doc/uid/TP40002585-SW10\n   691: ///\n   692: /// ```no_run\n   693: /// use std::env;\n   694: ///\n   695: /// fn main() {\n   696: ///     let dir = env::temp_dir();\n   697: ///     println!(\"Temporary directory: {}\", dir.display());\n   698: /// }\n   699: /// ```\n   700: #[must_use]\n   701: #[doc(alias = \"GetTempPath\", alias = \"GetTempPath2\")]\n   702: #[stable(feature = \"env\", since = \"1.0.0\")]\n   703: pub fn temp_dir() -> PathBuf {\n   704:     paths_imp::temp_dir()\n   705: }\n   706: \n   707: /// Returns the full filesystem path of the current running executable.\n   708: ///\n   709: /// # Platform-specific behavior\n   710: ///\n   711: /// If the executable was invoked through a symbolic link, some platforms will\n   712: /// return the path of the symbolic link and other platforms will return the\n   713: /// path of the symbolic link\u2019s target.\n   714: ///\n   715: /// If the executable is renamed while it is running, platforms may return the\n   716: /// path at the time it was loaded instead of the new path.\n   717: ///\n   718: /// # Errors\n   719: ///",
    "nanvix_source": "   696: /// use std::env;\n   697: ///\n   698: /// fn main() {\n   699: ///     let dir = env::temp_dir();\n   700: ///     println!(\"Temporary directory: {}\", dir.display());\n   701: /// }\n   702: /// ```\n   703: #[must_use]\n   704: #[doc(alias = \"GetTempPath\", alias = \"GetTempPath2\")]\n   705: #[stable(feature = \"env\", since = \"1.0.0\")]\n   706: pub fn temp_dir() -> PathBuf {\n   707:     paths_imp::temp_dir()\n   708: }\n   709: \n   710: /// Returns the full filesystem path of the current running executable.\n   711: ///\n   712: /// # Platform-specific behavior\n   713: ///\n   714: /// If the executable was invoked through a symbolic link, some platforms will\n   715: /// return the path of the symbolic link and other platforms will return the\n   716: /// path of the symbolic link\u2019s target.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::var",
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
      "name": "var",
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
                        "id": 218,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1856,
                        "path": "VarError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   206: ///\n   207: /// Use [`env!`] or [`option_env!`] instead if you want to check environment\n   208: /// variables at compile time.\n   209: ///\n   210: /// # Examples\n   211: ///\n   212: /// ```\n   213: /// use std::env;\n   214: ///\n   215: /// let key = \"HOME\";\n   216: /// match env::var(key) {\n   217: ///     Ok(val) => println!(\"{key}: {val:?}\"),\n   218: ///     Err(e) => println!(\"couldn't interpret {key}: {e}\"),\n   219: /// }\n   220: /// ```\n   221: #[stable(feature = \"env\", since = \"1.0.0\")]\n   222: pub fn var<K: AsRef<OsStr>>(key: K) -> Result<String, VarError> {\n   223:     _var(key.as_ref())\n   224: }\n   225: \n   226: fn _var(key: &OsStr) -> Result<String, VarError> {\n   227:     match var_os(key) {\n   228:         Some(s) => s.into_string().map_err(VarError::NotUnicode),\n   229:         None => Err(VarError::NotPresent),\n   230:     }\n   231: }\n   232: \n   233: /// Fetches the environment variable `key` from the current process, returning\n   234: /// [`None`] if the variable isn't set or if there is another error.\n   235: ///\n   236: /// It may return `None` if the environment variable's name contains\n   237: /// the equal sign character (`=`) or the NUL character.\n   238: ///",
    "nanvix_source": "   218: /// ```\n   219: /// use std::env;\n   220: ///\n   221: /// let key = \"HOME\";\n   222: /// match env::var(key) {\n   223: ///     Ok(val) => println!(\"{key}: {val:?}\"),\n   224: ///     Err(e) => println!(\"couldn't interpret {key}: {e}\"),\n   225: /// }\n   226: /// ```\n   227: #[stable(feature = \"env\", since = \"1.0.0\")]\n   228: pub fn var<K: AsRef<OsStr>>(key: K) -> Result<String, VarError> {\n   229:     fn inner(key: &OsStr) -> Result<String, VarError> {\n   230:         env_imp::getenv(key)\n   231:             .ok_or(VarError::NotPresent)?\n   232:             .into_string()\n   233:             .map_err(VarError::NotUnicode)\n   234:     }\n   235:     inner(key.as_ref())\n   236: }\n   237: \n   238: /// Fetches the environment variable `key` from the current process, returning",
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
