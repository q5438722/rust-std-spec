For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::process::Command::env",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "V"
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
              "generic_params": [],
              "type": {
                "generic": "K"
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
              "generic_params": [],
              "type": {
                "generic": "V"
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
      "name": "env",
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
            "key",
            {
              "generic": "K"
            }
          ],
          [
            "val",
            {
              "generic": "V"
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
    "verification_source": "   794:     /// [`Command::env_clear`] or for a single key using [`Command::env_remove`].\n   795:     ///\n   796:     /// Note that environment variable names are case-insensitive (but\n   797:     /// case-preserving) on Windows and case-sensitive on all other platforms.\n   798:     ///\n   799:     /// # Examples\n   800:     ///\n   801:     /// ```no_run\n   802:     /// use std::process::Command;\n   803:     ///\n   804:     /// Command::new(\"ls\")\n   805:     ///     .env(\"PATH\", \"/bin\")\n   806:     ///     .spawn()\n   807:     ///     .expect(\"ls command failed to start\");\n   808:     /// ```\n   809:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   810:     pub fn env<K, V>(&mut self, key: K, val: V) -> &mut Command\n   811:     where\n   812:         K: AsRef<OsStr>,\n   813:         V: AsRef<OsStr>,\n   814:     {\n   815:         self.inner.env_mut().set(key.as_ref(), val.as_ref());\n   816:         self\n   817:     }\n   818: \n   819:     /// Inserts or updates multiple explicit environment variable mappings.\n   820:     ///\n   821:     /// This method allows you to add multiple environment variable mappings to the spawned process\n   822:     /// or overwrite previously set values. You can use [`Command::env`] to set a single environment\n   823:     /// variable.\n   824:     ///\n   825:     /// Child processes will inherit environment variables from their parent process by default.\n   826:     /// Environment variables explicitly set using [`Command::envs`] take precedence over inherited",
    "nanvix_source": "   821:     ///\n   822:     /// ```no_run\n   823:     /// use std::process::Command;\n   824:     ///\n   825:     /// Command::new(\"ls\")\n   826:     ///     .env(\"PATH\", \"/bin\")\n   827:     ///     .spawn()\n   828:     ///     .expect(\"ls command failed to start\");\n   829:     /// ```\n   830:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   831:     pub fn env<K, V>(&mut self, key: K, val: V) -> &mut Command\n   832:     where\n   833:         K: AsRef<OsStr>,\n   834:         V: AsRef<OsStr>,\n   835:     {\n   836:         self.inner.env_mut().set(key.as_ref(), val.as_ref());\n   837:         self\n   838:     }\n   839: \n   840:     /// Inserts or updates multiple explicit environment variable mappings.\n   841:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::env_clear",
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
      "name": "env_clear",
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
    "verification_source": "   910:     ///\n   911:     /// # Examples\n   912:     ///\n   913:     /// The behavior of `sort` is affected by `LANG` and `LC_*` environment variables.\n   914:     /// Clearing the environment makes `sort`'s behavior independent of the parent processes' language.\n   915:     ///\n   916:     /// ```no_run\n   917:     /// use std::process::Command;\n   918:     ///\n   919:     /// Command::new(\"sort\")\n   920:     ///     .arg(\"file.txt\")\n   921:     ///     .env_clear()\n   922:     ///     .spawn()?;\n   923:     /// # std::io::Result::Ok(())\n   924:     /// ```\n   925:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   926:     pub fn env_clear(&mut self) -> &mut Command {\n   927:         self.inner.env_mut().clear();\n   928:         self\n   929:     }\n   930: \n   931:     /// Sets the working directory for the child process.\n   932:     ///\n   933:     /// # Platform-specific behavior\n   934:     ///\n   935:     /// If the program path is relative (e.g., `\"./script.sh\"`), it's ambiguous\n   936:     /// whether it should be interpreted relative to the parent's working\n   937:     /// directory or relative to `current_dir`. The behavior in this case is\n   938:     /// platform specific and unstable, and it's recommended to use\n   939:     /// [`canonicalize`] to get an absolute program path instead.\n   940:     ///\n   941:     /// # Examples\n   942:     ///",
    "nanvix_source": "   937:     /// ```no_run\n   938:     /// use std::process::Command;\n   939:     ///\n   940:     /// Command::new(\"sort\")\n   941:     ///     .arg(\"file.txt\")\n   942:     ///     .env_clear()\n   943:     ///     .spawn()?;\n   944:     /// # std::io::Result::Ok(())\n   945:     /// ```\n   946:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   947:     pub fn env_clear(&mut self) -> &mut Command {\n   948:         self.inner.env_mut().clear();\n   949:         self\n   950:     }\n   951: \n   952:     /// Sets the working directory for the child process.\n   953:     ///\n   954:     /// # Platform-specific behavior\n   955:     ///\n   956:     /// If the program path is relative (e.g., `\"./script.sh\"`), it's ambiguous\n   957:     /// whether it should be interpreted relative to the parent's working",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::env_remove",
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
      "name": "env_remove",
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
            "key",
            {
              "generic": "K"
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
    "verification_source": "   878:     ///\n   879:     /// # Examples\n   880:     ///\n   881:     /// Prevent any inherited `GIT_DIR` variable from changing the target of the `git` command,\n   882:     /// while allowing all other variables, like `GIT_AUTHOR_NAME`.\n   883:     ///\n   884:     /// ```no_run\n   885:     /// use std::process::Command;\n   886:     ///\n   887:     /// Command::new(\"git\")\n   888:     ///     .arg(\"commit\")\n   889:     ///     .env_remove(\"GIT_DIR\")\n   890:     ///     .spawn()?;\n   891:     /// # std::io::Result::Ok(())\n   892:     /// ```\n   893:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   894:     pub fn env_remove<K: AsRef<OsStr>>(&mut self, key: K) -> &mut Command {\n   895:         self.inner.env_mut().remove(key.as_ref());\n   896:         self\n   897:     }\n   898: \n   899:     /// Clears all explicitly set environment variables and prevents inheriting any parent process\n   900:     /// environment variables.\n   901:     ///\n   902:     /// This method will remove all explicitly added environment variables set via [`Command::env`]\n   903:     /// or [`Command::envs`]. In addition, it will prevent the spawned child process from inheriting\n   904:     /// any environment variable from its parent process.\n   905:     ///\n   906:     /// After calling [`Command::env_clear`], the iterator from [`Command::get_envs`] will be\n   907:     /// empty.\n   908:     ///\n   909:     /// You can use [`Command::env_remove`] to clear a single mapping.\n   910:     ///",
    "nanvix_source": "   905:     /// ```no_run\n   906:     /// use std::process::Command;\n   907:     ///\n   908:     /// Command::new(\"git\")\n   909:     ///     .arg(\"commit\")\n   910:     ///     .env_remove(\"GIT_DIR\")\n   911:     ///     .spawn()?;\n   912:     /// # std::io::Result::Ok(())\n   913:     /// ```\n   914:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   915:     pub fn env_remove<K: AsRef<OsStr>>(&mut self, key: K) -> &mut Command {\n   916:         self.inner.env_mut().remove(key.as_ref());\n   917:         self\n   918:     }\n   919: \n   920:     /// Clears all explicitly set environment variables and prevents inheriting any parent process\n   921:     /// environment variables.\n   922:     ///\n   923:     /// This method will remove all explicitly added environment variables set via [`Command::env`]\n   924:     /// or [`Command::envs`]. In addition, it will prevent the spawned child process from inheriting\n   925:     /// any environment variable from its parent process.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::envs",
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
            "name": "K"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "V"
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
                                    "tuple": [
                                      {
                                        "generic": "K"
                                      },
                                      {
                                        "generic": "V"
                                      }
                                    ]
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
              "generic_params": [],
              "type": {
                "generic": "K"
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
              "generic_params": [],
              "type": {
                "generic": "V"
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
      "name": "envs",
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
            "vars",
            {
              "generic": "I"
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
    "verification_source": "   838:     /// use std::collections::HashMap;\n   839:     ///\n   840:     /// let filtered_env : HashMap<String, String> =\n   841:     ///     env::vars().filter(|&(ref k, _)|\n   842:     ///         k == \"TERM\" || k == \"TZ\" || k == \"LANG\" || k == \"PATH\"\n   843:     ///     ).collect();\n   844:     ///\n   845:     /// Command::new(\"printenv\")\n   846:     ///     .stdin(Stdio::null())\n   847:     ///     .stdout(Stdio::inherit())\n   848:     ///     .env_clear()\n   849:     ///     .envs(&filtered_env)\n   850:     ///     .spawn()\n   851:     ///     .expect(\"printenv failed to start\");\n   852:     /// ```\n   853:     #[stable(feature = \"command_envs\", since = \"1.19.0\")]\n   854:     pub fn envs<I, K, V>(&mut self, vars: I) -> &mut Command\n   855:     where\n   856:         I: IntoIterator<Item = (K, V)>,\n   857:         K: AsRef<OsStr>,\n   858:         V: AsRef<OsStr>,\n   859:     {\n   860:         for (ref key, ref val) in vars {\n   861:             self.inner.env_mut().set(key.as_ref(), val.as_ref());\n   862:         }\n   863:         self\n   864:     }\n   865: \n   866:     /// Removes an explicitly set environment variable and prevents inheriting it from a parent\n   867:     /// process.\n   868:     ///\n   869:     /// This method will remove the explicit value of an environment variable set via\n   870:     /// [`Command::env`] or [`Command::envs`]. In addition, it will prevent the spawned child",
    "nanvix_source": "   865:     ///\n   866:     /// Command::new(\"printenv\")\n   867:     ///     .stdin(Stdio::null())\n   868:     ///     .stdout(Stdio::inherit())\n   869:     ///     .env_clear()\n   870:     ///     .envs(&filtered_env)\n   871:     ///     .spawn()\n   872:     ///     .expect(\"printenv failed to start\");\n   873:     /// ```\n   874:     #[stable(feature = \"command_envs\", since = \"1.19.0\")]\n   875:     pub fn envs<I, K, V>(&mut self, vars: I) -> &mut Command\n   876:     where\n   877:         I: IntoIterator<Item = (K, V)>,\n   878:         K: AsRef<OsStr>,\n   879:         V: AsRef<OsStr>,\n   880:     {\n   881:         for (ref key, ref val) in vars {\n   882:             self.inner.env_mut().set(key.as_ref(), val.as_ref());\n   883:         }\n   884:         self\n   885:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::get_args",
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
      "name": "get_args",
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
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 7384,
            "path": "CommandArgs"
          }
        }
      }
    },
    "verification_source": "  1133:     /// This does not include the path to the program as the first argument;\n  1134:     /// it only includes the arguments specified with [`Command::arg`] and\n  1135:     /// [`Command::args`].\n  1136:     ///\n  1137:     /// # Examples\n  1138:     ///\n  1139:     /// ```\n  1140:     /// use std::ffi::OsStr;\n  1141:     /// use std::process::Command;\n  1142:     ///\n  1143:     /// let mut cmd = Command::new(\"echo\");\n  1144:     /// cmd.arg(\"first\").arg(\"second\");\n  1145:     /// let args: Vec<&OsStr> = cmd.get_args().collect();\n  1146:     /// assert_eq!(args, &[\"first\", \"second\"]);\n  1147:     /// ```\n  1148:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1149:     pub fn get_args(&self) -> CommandArgs<'_> {\n  1150:         CommandArgs { inner: self.inner.get_args() }\n  1151:     }\n  1152: \n  1153:     /// Returns an iterator of the environment variables explicitly set for the child process.\n  1154:     ///\n  1155:     /// Environment variables explicitly set using [`Command::env`], [`Command::envs`], and\n  1156:     /// [`Command::env_remove`] can be retrieved with this method.\n  1157:     ///\n  1158:     /// Note that this output does not include environment variables inherited from the parent\n  1159:     /// process.\n  1160:     ///\n  1161:     /// Each element is a tuple key/value pair `(&OsStr, Option<&OsStr>)`. A [`None`] value\n  1162:     /// indicates its key was explicitly removed via [`Command::env_remove`]. The associated key for\n  1163:     /// the [`None`] value will no longer inherit from its parent process.\n  1164:     ///\n  1165:     /// An empty iterator can indicate that no explicit mappings were added or that",
    "nanvix_source": "  1207:     /// ```\n  1208:     /// use std::ffi::OsStr;\n  1209:     /// use std::process::Command;\n  1210:     ///\n  1211:     /// let mut cmd = Command::new(\"echo\");\n  1212:     /// cmd.arg(\"first\").arg(\"second\");\n  1213:     /// let args: Vec<&OsStr> = cmd.get_args().collect();\n  1214:     /// assert_eq!(args, &[\"first\", \"second\"]);\n  1215:     /// ```\n  1216:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1217:     pub fn get_args(&self) -> CommandArgs<'_> {\n  1218:         CommandArgs { inner: self.inner.get_args() }\n  1219:     }\n  1220: \n  1221:     /// Returns an iterator of the environment variables explicitly set for the child process.\n  1222:     ///\n  1223:     /// Environment variables explicitly set using [`Command::env`], [`Command::envs`], and\n  1224:     /// [`Command::env_remove`] can be retrieved with this method.\n  1225:     ///\n  1226:     /// Note that this output does not include environment variables inherited from the parent\n  1227:     /// process. To see the full list of environment variables, including those inherited from the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::get_current_dir",
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
      "name": "get_current_dir",
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
    "verification_source": "  1189:     ///\n  1190:     /// This returns [`None`] if the working directory will not be changed.\n  1191:     ///\n  1192:     /// # Examples\n  1193:     ///\n  1194:     /// ```\n  1195:     /// use std::path::Path;\n  1196:     /// use std::process::Command;\n  1197:     ///\n  1198:     /// let mut cmd = Command::new(\"ls\");\n  1199:     /// assert_eq!(cmd.get_current_dir(), None);\n  1200:     /// cmd.current_dir(\"/bin\");\n  1201:     /// assert_eq!(cmd.get_current_dir(), Some(Path::new(\"/bin\")));\n  1202:     /// ```\n  1203:     #[must_use]\n  1204:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1205:     pub fn get_current_dir(&self) -> Option<&Path> {\n  1206:         self.inner.get_current_dir()\n  1207:     }\n  1208: \n  1209:     /// Returns whether the environment will be cleared for the child process.\n  1210:     ///\n  1211:     /// This returns `true` if [`Command::env_clear`] was called, and `false` otherwise.\n  1212:     /// When `true`, the child process will not inherit any environment variables from\n  1213:     /// its parent process.\n  1214:     ///\n  1215:     /// # Examples\n  1216:     ///\n  1217:     /// ```\n  1218:     /// #![feature(command_resolved_envs)]\n  1219:     /// use std::process::Command;\n  1220:     ///\n  1221:     /// let mut cmd = Command::new(\"ls\");",
    "nanvix_source": "  1300:     /// use std::path::Path;\n  1301:     /// use std::process::Command;\n  1302:     ///\n  1303:     /// let mut cmd = Command::new(\"ls\");\n  1304:     /// assert_eq!(cmd.get_current_dir(), None);\n  1305:     /// cmd.current_dir(\"/bin\");\n  1306:     /// assert_eq!(cmd.get_current_dir(), Some(Path::new(\"/bin\")));\n  1307:     /// ```\n  1308:     #[must_use]\n  1309:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1310:     pub fn get_current_dir(&self) -> Option<&Path> {\n  1311:         self.inner.get_current_dir()\n  1312:     }\n  1313: \n  1314:     /// Returns whether the environment will be cleared for the child process.\n  1315:     ///\n  1316:     /// This returns `true` if [`Command::env_clear`] was called, and `false` otherwise.\n  1317:     /// When `true`, the child process will not inherit any environment variables from\n  1318:     /// its parent process.\n  1319:     ///\n  1320:     /// # Examples",
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
