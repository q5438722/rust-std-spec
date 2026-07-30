For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::env::args",
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
      "name": "args",
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
            "id": 1946,
            "path": "Args"
          }
        }
      }
    },
    "verification_source": "   809: ///\n   810: /// The returned iterator will panic during iteration if any argument to the\n   811: /// process is not valid Unicode. If this is not desired,\n   812: /// use the [`args_os`] function instead.\n   813: ///\n   814: /// # Examples\n   815: ///\n   816: /// ```\n   817: /// use std::env;\n   818: ///\n   819: /// // Prints each argument on a separate line\n   820: /// for argument in env::args() {\n   821: ///     println!(\"{argument}\");\n   822: /// }\n   823: /// ```\n   824: #[stable(feature = \"env\", since = \"1.0.0\")]\n   825: pub fn args() -> Args {\n   826:     Args { inner: args_os() }\n   827: }\n   828: \n   829: /// Returns the arguments that this program was started with (normally passed\n   830: /// via the command line).\n   831: ///\n   832: /// The first element is traditionally the path of the executable, but it can be\n   833: /// set to arbitrary text, and might not even exist. This means this property should\n   834: /// not be relied upon for security purposes.\n   835: ///\n   836: /// On Unix systems the shell usually expands unquoted arguments with glob patterns\n   837: /// (such as `*` and `?`). On Windows this is not done, and such arguments are\n   838: /// passed as-is.\n   839: ///\n   840: /// On glibc Linux systems, arguments are retrieved by placing a function in `.init_array`.\n   841: /// glibc passes `argc`, `argv`, and `envp` to functions in `.init_array`, as a non-standard",
    "nanvix_source": "   818: ///\n   819: /// ```\n   820: /// use std::env;\n   821: ///\n   822: /// // Prints each argument on a separate line\n   823: /// for argument in env::args() {\n   824: ///     println!(\"{argument}\");\n   825: /// }\n   826: /// ```\n   827: #[stable(feature = \"env\", since = \"1.0.0\")]\n   828: pub fn args() -> Args {\n   829:     Args { inner: args_os() }\n   830: }\n   831: \n   832: /// Returns the arguments that this program was started with (normally passed\n   833: /// via the command line).\n   834: ///\n   835: /// The first element is traditionally the path of the executable, but it can be\n   836: /// set to arbitrary text, and might not even exist. This means this property should\n   837: /// not be relied upon for security purposes.\n   838: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::args_os",
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
      "name": "args_os",
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
            "id": 1975,
            "path": "ArgsOs"
          }
        }
      }
    },
    "verification_source": "   844: ///\n   845: /// Note that the returned iterator will not check if the arguments to the\n   846: /// process are valid Unicode. If you want to panic on invalid UTF-8,\n   847: /// use the [`args`] function instead.\n   848: ///\n   849: /// # Examples\n   850: ///\n   851: /// ```\n   852: /// use std::env;\n   853: ///\n   854: /// // Prints each argument on a separate line\n   855: /// for argument in env::args_os() {\n   856: ///     println!(\"{argument:?}\");\n   857: /// }\n   858: /// ```\n   859: #[stable(feature = \"env\", since = \"1.0.0\")]\n   860: pub fn args_os() -> ArgsOs {\n   861:     ArgsOs { inner: sys::args::args() }\n   862: }\n   863: \n   864: #[stable(feature = \"env_unimpl_send_sync\", since = \"1.26.0\")]\n   865: impl !Send for Args {}\n   866: \n   867: #[stable(feature = \"env_unimpl_send_sync\", since = \"1.26.0\")]\n   868: impl !Sync for Args {}\n   869: \n   870: #[stable(feature = \"env\", since = \"1.0.0\")]\n   871: impl Iterator for Args {\n   872:     type Item = String;\n   873: \n   874:     fn next(&mut self) -> Option<String> {\n   875:         self.inner.next().map(|s| s.into_string().unwrap())\n   876:     }",
    "nanvix_source": "   853: ///\n   854: /// ```\n   855: /// use std::env;\n   856: ///\n   857: /// // Prints each argument on a separate line\n   858: /// for argument in env::args_os() {\n   859: ///     println!(\"{argument:?}\");\n   860: /// }\n   861: /// ```\n   862: #[stable(feature = \"env\", since = \"1.0.0\")]\n   863: pub fn args_os() -> ArgsOs {\n   864:     ArgsOs { inner: sys::args::args() }\n   865: }\n   866: \n   867: #[stable(feature = \"env_unimpl_send_sync\", since = \"1.26.0\")]\n   868: impl !Send for Args {}\n   869: \n   870: #[stable(feature = \"env_unimpl_send_sync\", since = \"1.26.0\")]\n   871: impl !Sync for Args {}\n   872: \n   873: #[stable(feature = \"env\", since = \"1.0.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::current_dir",
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
      "name": "current_dir",
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
    "verification_source": "    37: ///\n    38: /// # Examples\n    39: ///\n    40: /// ```\n    41: /// use std::env;\n    42: ///\n    43: /// fn main() -> std::io::Result<()> {\n    44: ///     let path = env::current_dir()?;\n    45: ///     println!(\"The current directory is {}\", path.display());\n    46: ///     Ok(())\n    47: /// }\n    48: /// ```\n    49: #[doc(alias = \"pwd\")]\n    50: #[doc(alias = \"getcwd\")]\n    51: #[doc(alias = \"GetCurrentDirectory\")]\n    52: #[stable(feature = \"env\", since = \"1.0.0\")]\n    53: pub fn current_dir() -> io::Result<PathBuf> {\n    54:     paths_imp::getcwd()\n    55: }\n    56: \n    57: /// Changes the current working directory to the specified path.\n    58: ///\n    59: /// # Platform-specific behavior\n    60: ///\n    61: /// This function [currently] corresponds to the `chdir` function on Unix\n    62: /// and the `SetCurrentDirectoryW` function on Windows.\n    63: ///\n    64: /// Returns an [`Err`] if the operation fails.\n    65: ///\n    66: /// [currently]: crate::io#platform-specific-behavior\n    67: ///\n    68: /// # Examples\n    69: ///",
    "nanvix_source": "    43: /// fn main() -> std::io::Result<()> {\n    44: ///     let path = env::current_dir()?;\n    45: ///     println!(\"The current directory is {}\", path.display());\n    46: ///     Ok(())\n    47: /// }\n    48: /// ```\n    49: #[doc(alias = \"pwd\")]\n    50: #[doc(alias = \"getcwd\")]\n    51: #[doc(alias = \"GetCurrentDirectory\")]\n    52: #[stable(feature = \"env\", since = \"1.0.0\")]\n    53: pub fn current_dir() -> io::Result<PathBuf> {\n    54:     paths_imp::getcwd()\n    55: }\n    56: \n    57: /// Changes the current working directory to the specified path.\n    58: ///\n    59: /// # Platform-specific behavior\n    60: ///\n    61: /// This function [currently] corresponds to the `chdir` function on Unix\n    62: /// and the `SetCurrentDirectoryW` function on Windows.\n    63: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::current_exe",
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
      "name": "current_exe",
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
    "verification_source": "   738: /// a different program.\n   739: ///\n   740: /// This list of illustrative example attacks is not exhaustive.\n   741: ///\n   742: /// # Examples\n   743: ///\n   744: /// ```\n   745: /// use std::env;\n   746: ///\n   747: /// match env::current_exe() {\n   748: ///     Ok(exe_path) => println!(\"Path of this executable is: {}\",\n   749: ///                              exe_path.display()),\n   750: ///     Err(e) => println!(\"failed to get current exe path: {e}\"),\n   751: /// };\n   752: /// ```\n   753: #[stable(feature = \"env\", since = \"1.0.0\")]\n   754: pub fn current_exe() -> io::Result<PathBuf> {\n   755:     paths_imp::current_exe()\n   756: }\n   757: \n   758: /// An iterator over the arguments of a process, yielding a [`String`] value for\n   759: /// each argument.\n   760: ///\n   761: /// This struct is created by [`env::args()`]. See its documentation\n   762: /// for more.\n   763: ///\n   764: /// The first element is traditionally the path of the executable, but it can be\n   765: /// set to arbitrary text, and might not even exist. This means this property\n   766: /// should not be relied upon for security purposes.\n   767: ///\n   768: /// [`env::args()`]: args\n   769: #[must_use = \"iterators are lazy and do nothing unless consumed\"]\n   770: #[stable(feature = \"env\", since = \"1.0.0\")]",
    "nanvix_source": "   747: /// ```\n   748: /// use std::env;\n   749: ///\n   750: /// match env::current_exe() {\n   751: ///     Ok(exe_path) => println!(\"Path of this executable is: {}\",\n   752: ///                              exe_path.display()),\n   753: ///     Err(e) => println!(\"failed to get current exe path: {e}\"),\n   754: /// };\n   755: /// ```\n   756: #[stable(feature = \"env\", since = \"1.0.0\")]\n   757: pub fn current_exe() -> io::Result<PathBuf> {\n   758:     paths_imp::current_exe()\n   759: }\n   760: \n   761: /// An iterator over the arguments of a process, yielding a [`String`] value for\n   762: /// each argument.\n   763: ///\n   764: /// This struct is created by [`env::args()`]. See its documentation\n   765: /// for more.\n   766: ///\n   767: /// The first element is traditionally the path of the executable, but it can be",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::home_dir",
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
      "name": "home_dir",
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
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   627: /// Before Rust 1.85.0, this function used to return the value of the 'HOME' environment variable\n   628: /// on Windows, which in Cygwin or Mingw environments could return non-standard paths like `/home/you`\n   629: /// instead of `C:\\Users\\you`.\n   630: ///\n   631: /// # Examples\n   632: ///\n   633: /// ```\n   634: /// use std::env;\n   635: ///\n   636: /// match env::home_dir() {\n   637: ///     Some(path) => println!(\"Your home directory, probably: {}\", path.display()),\n   638: ///     None => println!(\"Impossible to get your home dir!\"),\n   639: /// }\n   640: /// ```\n   641: #[must_use]\n   642: #[stable(feature = \"env\", since = \"1.0.0\")]\n   643: pub fn home_dir() -> Option<PathBuf> {\n   644:     paths_imp::home_dir()\n   645: }\n   646: \n   647: /// Returns the path of a temporary directory.\n   648: ///\n   649: /// The temporary directory may be shared among users, or between processes\n   650: /// with different privileges; thus, the creation of any files or directories\n   651: /// in the temporary directory must use a secure method to create a uniquely\n   652: /// named file. Creating a file or directory with a fixed or predictable name\n   653: /// may result in \"insecure temporary file\" security vulnerabilities. Consider\n   654: /// using a crate that securely creates temporary files or directories.\n   655: ///\n   656: /// Note that the returned value may be a symbolic link, not a directory.\n   657: ///\n   658: /// # Platform-specific behavior\n   659: ///",
    "nanvix_source": "   636: /// use std::env;\n   637: ///\n   638: /// match env::home_dir() {\n   639: ///     Some(path) => println!(\"Your home directory, probably: {}\", path.display()),\n   640: ///     None => println!(\"Impossible to get your home dir!\"),\n   641: /// }\n   642: /// ```\n   643: #[must_use]\n   644: #[stable(feature = \"env\", since = \"1.0.0\")]\n   645: #[doc(alias = \"home\")]\n   646: pub fn home_dir() -> Option<PathBuf> {\n   647:     paths_imp::home_dir()\n   648: }\n   649: \n   650: /// Returns the path of a temporary directory.\n   651: ///\n   652: /// The temporary directory may be shared among users, or between processes\n   653: /// with different privileges; thus, the creation of any files or directories\n   654: /// in the temporary directory must use a secure method to create a uniquely\n   655: /// named file. Creating a file or directory with a fixed or predictable name\n   656: /// may result in \"insecure temporary file\" security vulnerabilities. Consider",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::env::join_paths",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
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
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 52,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
              }
            }
          },
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
              "generic_params": [],
              "type": {
                "generic": "T"
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
      "name": "join_paths",
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
            "paths",
            {
              "generic": "I"
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
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1919,
                        "path": "JoinPathsError"
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
    "verification_source": "   561: /// use std::path::PathBuf;\n   562: ///\n   563: /// fn main() -> Result<(), env::JoinPathsError> {\n   564: ///     if let Some(path) = env::var_os(\"PATH\") {\n   565: ///         let mut paths = env::split_paths(&path).collect::<Vec<_>>();\n   566: ///         paths.push(PathBuf::from(\"/home/xyz/bin\"));\n   567: ///         let new_path = env::join_paths(paths)?;\n   568: ///         unsafe { env::set_var(\"PATH\", &new_path); }\n   569: ///     }\n   570: ///\n   571: ///     Ok(())\n   572: /// }\n   573: /// ```\n   574: ///\n   575: /// [`env::split_paths()`]: split_paths\n   576: #[stable(feature = \"env\", since = \"1.0.0\")]\n   577: pub fn join_paths<I, T>(paths: I) -> Result<OsString, JoinPathsError>\n   578: where\n   579:     I: IntoIterator<Item = T>,\n   580:     T: AsRef<OsStr>,\n   581: {\n   582:     paths_imp::join_paths(paths.into_iter()).map_err(|e| JoinPathsError { inner: e })\n   583: }\n   584: \n   585: #[stable(feature = \"env\", since = \"1.0.0\")]\n   586: impl fmt::Display for JoinPathsError {\n   587:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   588:         self.inner.fmt(f)\n   589:     }\n   590: }\n   591: \n   592: #[stable(feature = \"env\", since = \"1.0.0\")]\n   593: impl Error for JoinPathsError {",
    "nanvix_source": "   568: ///         let new_path = env::join_paths(paths)?;\n   569: ///         unsafe { env::set_var(\"PATH\", &new_path); }\n   570: ///     }\n   571: ///\n   572: ///     Ok(())\n   573: /// }\n   574: /// ```\n   575: ///\n   576: /// [`env::split_paths()`]: split_paths\n   577: #[stable(feature = \"env\", since = \"1.0.0\")]\n   578: pub fn join_paths<I, T>(paths: I) -> Result<OsString, JoinPathsError>\n   579: where\n   580:     I: IntoIterator<Item = T>,\n   581:     T: AsRef<OsStr>,\n   582: {\n   583:     paths_imp::join_paths(paths.into_iter()).map_err(|e| JoinPathsError { inner: e })\n   584: }\n   585: \n   586: #[stable(feature = \"env\", since = \"1.0.0\")]\n   587: impl fmt::Display for JoinPathsError {\n   588:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {",
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
