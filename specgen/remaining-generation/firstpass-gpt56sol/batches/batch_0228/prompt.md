For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::process::Command::stderr",
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
                                    "id": 2706,
                                    "path": "Stdio"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 44,
                        "path": "Into"
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
      "name": "stderr",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
            "cfg",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1019:     /// [`piped`]: Stdio::piped\n  1020:     /// [`spawn`]: Self::spawn\n  1021:     /// [`status`]: Self::status\n  1022:     /// [`output`]: Self::output\n  1023:     ///\n  1024:     /// # Examples\n  1025:     ///\n  1026:     /// ```no_run\n  1027:     /// use std::process::{Command, Stdio};\n  1028:     ///\n  1029:     /// Command::new(\"ls\")\n  1030:     ///     .stderr(Stdio::null())\n  1031:     ///     .spawn()\n  1032:     ///     .expect(\"ls command failed to start\");\n  1033:     /// ```\n  1034:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1035:     pub fn stderr<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n  1036:         self.inner.stderr(cfg.into().0);\n  1037:         self\n  1038:     }\n  1039: \n  1040:     /// Executes the command as a child process, returning a handle to it.\n  1041:     ///\n  1042:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  1043:     ///\n  1044:     /// # Examples\n  1045:     ///\n  1046:     /// ```no_run\n  1047:     /// use std::process::Command;\n  1048:     ///\n  1049:     /// Command::new(\"ls\")\n  1050:     ///     .spawn()\n  1051:     ///     .expect(\"ls command failed to start\");",
    "nanvix_source": "  1046:     ///\n  1047:     /// ```no_run\n  1048:     /// use std::process::{Command, Stdio};\n  1049:     ///\n  1050:     /// Command::new(\"ls\")\n  1051:     ///     .stderr(Stdio::null())\n  1052:     ///     .spawn()\n  1053:     ///     .expect(\"ls command failed to start\");\n  1054:     /// ```\n  1055:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1056:     pub fn stderr<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n  1057:         self.inner.stderr(cfg.into().0);\n  1058:         self\n  1059:     }\n  1060: \n  1061:     /// Executes the command as a child process, returning a handle to it.\n  1062:     ///\n  1063:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  1064:     ///\n  1065:     /// # Errors\n  1066:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::stdin",
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
                                    "id": 2706,
                                    "path": "Stdio"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 44,
                        "path": "Into"
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
      "name": "stdin",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
            "cfg",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "   965:     /// [`piped`]: Stdio::piped\n   966:     /// [`spawn`]: Self::spawn\n   967:     /// [`status`]: Self::status\n   968:     /// [`output`]: Self::output\n   969:     ///\n   970:     /// # Examples\n   971:     ///\n   972:     /// ```no_run\n   973:     /// use std::process::{Command, Stdio};\n   974:     ///\n   975:     /// Command::new(\"ls\")\n   976:     ///     .stdin(Stdio::null())\n   977:     ///     .spawn()\n   978:     ///     .expect(\"ls command failed to start\");\n   979:     /// ```\n   980:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   981:     pub fn stdin<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n   982:         self.inner.stdin(cfg.into().0);\n   983:         self\n   984:     }\n   985: \n   986:     /// Configuration for the child process's standard output (stdout) handle.\n   987:     ///\n   988:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n   989:     /// defaults to [`piped`] when used with [`output`].\n   990:     ///\n   991:     /// [`inherit`]: Stdio::inherit\n   992:     /// [`piped`]: Stdio::piped\n   993:     /// [`spawn`]: Self::spawn\n   994:     /// [`status`]: Self::status\n   995:     /// [`output`]: Self::output\n   996:     ///\n   997:     /// # Examples",
    "nanvix_source": "   992:     ///\n   993:     /// ```no_run\n   994:     /// use std::process::{Command, Stdio};\n   995:     ///\n   996:     /// Command::new(\"ls\")\n   997:     ///     .stdin(Stdio::null())\n   998:     ///     .spawn()\n   999:     ///     .expect(\"ls command failed to start\");\n  1000:     /// ```\n  1001:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1002:     pub fn stdin<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n  1003:         self.inner.stdin(cfg.into().0);\n  1004:         self\n  1005:     }\n  1006: \n  1007:     /// Configuration for the child process's standard output (stdout) handle.\n  1008:     ///\n  1009:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n  1010:     /// defaults to [`piped`] when used with [`output`].\n  1011:     ///\n  1012:     /// [`inherit`]: Stdio::inherit",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::stdout",
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
                                    "id": 2706,
                                    "path": "Stdio"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 44,
                        "path": "Into"
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
      "name": "stdout",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
            "cfg",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "   992:     /// [`piped`]: Stdio::piped\n   993:     /// [`spawn`]: Self::spawn\n   994:     /// [`status`]: Self::status\n   995:     /// [`output`]: Self::output\n   996:     ///\n   997:     /// # Examples\n   998:     ///\n   999:     /// ```no_run\n  1000:     /// use std::process::{Command, Stdio};\n  1001:     ///\n  1002:     /// Command::new(\"ls\")\n  1003:     ///     .stdout(Stdio::null())\n  1004:     ///     .spawn()\n  1005:     ///     .expect(\"ls command failed to start\");\n  1006:     /// ```\n  1007:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1008:     pub fn stdout<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n  1009:         self.inner.stdout(cfg.into().0);\n  1010:         self\n  1011:     }\n  1012: \n  1013:     /// Configuration for the child process's standard error (stderr) handle.\n  1014:     ///\n  1015:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n  1016:     /// defaults to [`piped`] when used with [`output`].\n  1017:     ///\n  1018:     /// [`inherit`]: Stdio::inherit\n  1019:     /// [`piped`]: Stdio::piped\n  1020:     /// [`spawn`]: Self::spawn\n  1021:     /// [`status`]: Self::status\n  1022:     /// [`output`]: Self::output\n  1023:     ///\n  1024:     /// # Examples",
    "nanvix_source": "  1019:     ///\n  1020:     /// ```no_run\n  1021:     /// use std::process::{Command, Stdio};\n  1022:     ///\n  1023:     /// Command::new(\"ls\")\n  1024:     ///     .stdout(Stdio::null())\n  1025:     ///     .spawn()\n  1026:     ///     .expect(\"ls command failed to start\");\n  1027:     /// ```\n  1028:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1029:     pub fn stdout<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {\n  1030:         self.inner.stdout(cfg.into().0);\n  1031:         self\n  1032:     }\n  1033: \n  1034:     /// Configuration for the child process's standard error (stderr) handle.\n  1035:     ///\n  1036:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n  1037:     /// defaults to [`piped`] when used with [`output`].\n  1038:     ///\n  1039:     /// [`inherit`]: Stdio::inherit",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::ExitStatus::code",
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
      "name": "code",
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
            "id": 5632,
            "path": "ExitStatus"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7508",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5632",
        "resolved_owner_path": [
          "std",
          "process",
          "ExitStatus"
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
                      "primitive": "i32"
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
    "verification_source": "  1892:     ///\n  1893:     /// ```no_run\n  1894:     /// use std::process::Command;\n  1895:     ///\n  1896:     /// let status = Command::new(\"mkdir\")\n  1897:     ///     .arg(\"projects\")\n  1898:     ///     .status()\n  1899:     ///     .expect(\"failed to execute mkdir\");\n  1900:     ///\n  1901:     /// match status.code() {\n  1902:     ///     Some(code) => println!(\"Exited with status code: {code}\"),\n  1903:     ///     None => println!(\"Process terminated by signal\")\n  1904:     /// }\n  1905:     /// ```\n  1906:     #[must_use]\n  1907:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1908:     pub fn code(&self) -> Option<i32> {\n  1909:         self.0.code()\n  1910:     }\n  1911: }\n  1912: \n  1913: impl AsInner<imp::ExitStatus> for ExitStatus {\n  1914:     #[inline]\n  1915:     fn as_inner(&self) -> &imp::ExitStatus {\n  1916:         &self.0\n  1917:     }\n  1918: }\n  1919: \n  1920: impl FromInner<imp::ExitStatus> for ExitStatus {\n  1921:     fn from_inner(s: imp::ExitStatus) -> ExitStatus {\n  1922:         ExitStatus(s)\n  1923:     }\n  1924: }",
    "nanvix_source": "  2008:     ///     .status()\n  2009:     ///     .expect(\"failed to execute mkdir\");\n  2010:     ///\n  2011:     /// match status.code() {\n  2012:     ///     Some(code) => println!(\"Exited with status code: {code}\"),\n  2013:     ///     None => println!(\"Process terminated by signal\")\n  2014:     /// }\n  2015:     /// ```\n  2016:     #[must_use]\n  2017:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2018:     pub fn code(&self) -> Option<i32> {\n  2019:         self.0.code()\n  2020:     }\n  2021: }\n  2022: \n  2023: impl AsInner<imp::ExitStatus> for ExitStatus {\n  2024:     #[inline]\n  2025:     fn as_inner(&self) -> &imp::ExitStatus {\n  2026:         &self.0\n  2027:     }\n  2028: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::ExitStatus::success",
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
      "name": "success",
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
            "id": 5632,
            "path": "ExitStatus"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7508",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5632",
        "resolved_owner_path": [
          "std",
          "process",
          "ExitStatus"
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
    "verification_source": "  1860:     /// ```rust,no_run\n  1861:     /// use std::process::Command;\n  1862:     ///\n  1863:     /// let status = Command::new(\"mkdir\")\n  1864:     ///     .arg(\"projects\")\n  1865:     ///     .status()\n  1866:     ///     .expect(\"failed to execute mkdir\");\n  1867:     ///\n  1868:     /// if status.success() {\n  1869:     ///     println!(\"'projects/' directory created\");\n  1870:     /// } else {\n  1871:     ///     println!(\"failed to create 'projects/' directory: {status}\");\n  1872:     /// }\n  1873:     /// ```\n  1874:     #[must_use]\n  1875:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1876:     pub fn success(&self) -> bool {\n  1877:         self.0.exit_ok().is_ok()\n  1878:     }\n  1879: \n  1880:     /// Returns the exit code of the process, if any.\n  1881:     ///\n  1882:     /// In Unix terms the return value is the **exit status**: the value passed to `exit`, if the\n  1883:     /// process finished by calling `exit`.  Note that on Unix the exit status is truncated to 8\n  1884:     /// bits, and that values that didn't come from a program's call to `exit` may be invented by the\n  1885:     /// runtime system (often, for example, 255, 254, 127 or 126).\n  1886:     ///\n  1887:     /// On Unix, this will return `None` if the process was terminated by a signal.\n  1888:     /// [`ExitStatusExt`](crate::os::unix::process::ExitStatusExt) is an\n  1889:     /// extension trait for extracting any such signal, and other details, from the `ExitStatus`.\n  1890:     ///\n  1891:     /// # Examples\n  1892:     ///",
    "nanvix_source": "  1976:     ///     .expect(\"failed to execute mkdir\");\n  1977:     ///\n  1978:     /// if status.success() {\n  1979:     ///     println!(\"'projects/' directory created\");\n  1980:     /// } else {\n  1981:     ///     println!(\"failed to create 'projects/' directory: {status}\");\n  1982:     /// }\n  1983:     /// ```\n  1984:     #[must_use]\n  1985:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1986:     pub fn success(&self) -> bool {\n  1987:         self.0.exit_ok().is_ok()\n  1988:     }\n  1989: \n  1990:     /// Returns the exit code of the process, if any.\n  1991:     ///\n  1992:     /// In Unix terms the return value is the **exit status**: the value passed to `exit`, if the\n  1993:     /// process finished by calling `exit`.  Note that on Unix the exit status is truncated to 8\n  1994:     /// bits, and that values that didn't come from a program's call to `exit` may be invented by the\n  1995:     /// runtime system (often, for example, 255, 254, 127 or 126).\n  1996:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Stdio::inherit",
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
      "name": "inherit",
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
            "id": 2706,
            "path": "Stdio"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7489",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2706",
        "resolved_owner_path": [
          "std",
          "process",
          "Stdio"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 2706,
            "path": "Stdio"
          }
        }
      }
    },
    "verification_source": "  1505:     ///\n  1506:     /// ```no_run\n  1507:     /// use std::process::{Command, Stdio};\n  1508:     /// use std::io::{self, Write};\n  1509:     ///\n  1510:     /// let output = Command::new(\"rev\")\n  1511:     ///     .stdin(Stdio::inherit())\n  1512:     ///     .stdout(Stdio::piped())\n  1513:     ///     .output()?;\n  1514:     ///\n  1515:     /// print!(\"You piped in the reverse of: \");\n  1516:     /// io::stdout().write_all(&output.stdout)?;\n  1517:     /// # io::Result::Ok(())\n  1518:     /// ```\n  1519:     #[must_use]\n  1520:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1521:     pub fn inherit() -> Stdio {\n  1522:         Stdio(imp::Stdio::Inherit)\n  1523:     }\n  1524: \n  1525:     /// This stream will be ignored. This is the equivalent of attaching the\n  1526:     /// stream to `/dev/null`.\n  1527:     ///\n  1528:     /// # Examples\n  1529:     ///\n  1530:     /// With stdout:\n  1531:     ///\n  1532:     /// ```no_run\n  1533:     /// use std::process::{Command, Stdio};\n  1534:     ///\n  1535:     /// let output = Command::new(\"echo\")\n  1536:     ///     .arg(\"Hello, world!\")\n  1537:     ///     .stdout(Stdio::null())",
    "nanvix_source": "  1625:     ///     .stdin(Stdio::inherit())\n  1626:     ///     .stdout(Stdio::piped())\n  1627:     ///     .output()?;\n  1628:     ///\n  1629:     /// print!(\"You piped in the reverse of: \");\n  1630:     /// io::stdout().write_all(&output.stdout)?;\n  1631:     /// # io::Result::Ok(())\n  1632:     /// ```\n  1633:     #[must_use]\n  1634:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1635:     pub fn inherit() -> Stdio {\n  1636:         Stdio(imp::Stdio::Inherit)\n  1637:     }\n  1638: \n  1639:     /// This stream will be ignored. This is the equivalent of attaching the\n  1640:     /// stream to `/dev/null`.\n  1641:     ///\n  1642:     /// # Examples\n  1643:     ///\n  1644:     /// With stdout:\n  1645:     ///",
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
