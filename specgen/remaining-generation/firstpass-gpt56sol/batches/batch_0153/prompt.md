For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::extension",
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
      "name": "extension",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 1857,
                            "path": "OsStr"
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
    "verification_source": "  2923:     /// * [`None`], if there is no embedded `.`;\n  2924:     /// * [`None`], if the file name begins with `.` and has no other `.`s within;\n  2925:     /// * Otherwise, the portion of the file name after the final `.`\n  2926:     ///\n  2927:     /// [`self.file_name`]: Path::file_name\n  2928:     ///\n  2929:     /// # Examples\n  2930:     ///\n  2931:     /// ```\n  2932:     /// use std::path::Path;\n  2933:     ///\n  2934:     /// assert_eq!(\"rs\", Path::new(\"foo.rs\").extension().unwrap());\n  2935:     /// assert_eq!(\"gz\", Path::new(\"foo.tar.gz\").extension().unwrap());\n  2936:     /// ```\n  2937:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2938:     #[must_use]\n  2939:     pub fn extension(&self) -> Option<&OsStr> {\n  2940:         self.file_name().map(rsplit_file_at_dot).and_then(|(before, after)| before.and(after))\n  2941:     }\n  2942: \n  2943:     /// Checks whether the path ends in a trailing [separator](MAIN_SEPARATOR).\n  2944:     ///\n  2945:     /// This is generally done to ensure that a path is treated as a directory, not a file,\n  2946:     /// although it does not actually guarantee that such a path is a directory on the underlying\n  2947:     /// file system.\n  2948:     ///\n  2949:     /// Despite this behavior, two paths are still considered the same in Rust whether they have a\n  2950:     /// trailing separator or not.\n  2951:     ///\n  2952:     /// # Examples\n  2953:     ///\n  2954:     /// ```\n  2955:     /// #![feature(path_trailing_sep)]",
    "nanvix_source": "  2950:     /// # Examples\n  2951:     ///\n  2952:     /// ```\n  2953:     /// use std::path::Path;\n  2954:     ///\n  2955:     /// assert_eq!(\"rs\", Path::new(\"foo.rs\").extension().unwrap());\n  2956:     /// assert_eq!(\"gz\", Path::new(\"foo.tar.gz\").extension().unwrap());\n  2957:     /// ```\n  2958:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2959:     #[must_use]\n  2960:     pub fn extension(&self) -> Option<&OsStr> {\n  2961:         self.file_name().map(rsplit_file_at_dot).and_then(|(before, after)| before.and(after))\n  2962:     }\n  2963: \n  2964:     /// Checks whether the path ends in a trailing [separator](MAIN_SEPARATOR).\n  2965:     ///\n  2966:     /// This is generally done to ensure that a path is treated as a directory, not a file,\n  2967:     /// although it does not actually guarantee that such a path is a directory on the underlying\n  2968:     /// file system.\n  2969:     ///\n  2970:     /// Despite this behavior, two paths are still considered the same in Rust whether they have a",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::file_name",
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
      "name": "file_name",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 1857,
                            "path": "OsStr"
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
    "verification_source": "  2668:     /// # Examples\n  2669:     ///\n  2670:     /// ```\n  2671:     /// use std::path::Path;\n  2672:     /// use std::ffi::OsStr;\n  2673:     ///\n  2674:     /// assert_eq!(Some(OsStr::new(\"bin\")), Path::new(\"/usr/bin/\").file_name());\n  2675:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"tmp/foo.txt\").file_name());\n  2676:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"foo.txt/.\").file_name());\n  2677:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"foo.txt/.//\").file_name());\n  2678:     /// assert_eq!(None, Path::new(\"foo.txt/..\").file_name());\n  2679:     /// assert_eq!(None, Path::new(\"/\").file_name());\n  2680:     /// ```\n  2681:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2682:     #[doc(alias = \"basename\")]\n  2683:     #[must_use]\n  2684:     pub fn file_name(&self) -> Option<&OsStr> {\n  2685:         self.components().next_back().and_then(|p| match p {\n  2686:             Component::Normal(p) => Some(p),\n  2687:             _ => None,\n  2688:         })\n  2689:     }\n  2690: \n  2691:     /// Returns a path that, when joined onto `base`, yields `self`.\n  2692:     ///\n  2693:     /// # Errors\n  2694:     ///\n  2695:     /// If `base` is not a prefix of `self` (i.e., [`starts_with`]\n  2696:     /// returns `false`), returns [`Err`].\n  2697:     ///\n  2698:     /// [`starts_with`]: Path::starts_with\n  2699:     ///\n  2700:     /// # Examples",
    "nanvix_source": "  2692:     /// assert_eq!(Some(OsStr::new(\"bin\")), Path::new(\"/usr/bin/\").file_name());\n  2693:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"tmp/foo.txt\").file_name());\n  2694:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"foo.txt/.\").file_name());\n  2695:     /// assert_eq!(Some(OsStr::new(\"foo.txt\")), Path::new(\"foo.txt/.//\").file_name());\n  2696:     /// assert_eq!(None, Path::new(\"foo.txt/..\").file_name());\n  2697:     /// assert_eq!(None, Path::new(\"/\").file_name());\n  2698:     /// ```\n  2699:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2700:     #[doc(alias = \"basename\")]\n  2701:     #[must_use]\n  2702:     pub fn file_name(&self) -> Option<&OsStr> {\n  2703:         self.components().next_back().and_then(|p| match p {\n  2704:             Component::Normal(p) => Some(p),\n  2705:             _ => None,\n  2706:         })\n  2707:     }\n  2708: \n  2709:     /// Returns a path that, when joined onto `base`, yields `self`.\n  2710:     ///\n  2711:     /// # Errors\n  2712:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::file_prefix",
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
      "name": "file_prefix",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 1857,
                            "path": "OsStr"
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
    "verification_source": "  2898:     /// use std::path::Path;\n  2899:     ///\n  2900:     /// assert_eq!(\"foo\", Path::new(\"foo.rs\").file_prefix().unwrap());\n  2901:     /// assert_eq!(\"foo\", Path::new(\"foo.tar.gz\").file_prefix().unwrap());\n  2902:     /// assert_eq!(\".config\", Path::new(\".config\").file_prefix().unwrap());\n  2903:     /// assert_eq!(\".config\", Path::new(\".config.toml\").file_prefix().unwrap());\n  2904:     /// ```\n  2905:     ///\n  2906:     /// # See Also\n  2907:     /// This method is similar to [`Path::file_stem`], which extracts the portion of the file name\n  2908:     /// before the *last* `.`\n  2909:     ///\n  2910:     /// [`Path::file_stem`]: Path::file_stem\n  2911:     ///\n  2912:     #[stable(feature = \"path_file_prefix\", since = \"1.91.0\")]\n  2913:     #[must_use]\n  2914:     pub fn file_prefix(&self) -> Option<&OsStr> {\n  2915:         self.file_name().map(split_file_at_dot).and_then(|(before, _after)| Some(before))\n  2916:     }\n  2917: \n  2918:     /// Extracts the extension (without the leading dot) of [`self.file_name`], if possible.\n  2919:     ///\n  2920:     /// The extension is:\n  2921:     ///\n  2922:     /// * [`None`], if there is no file name;\n  2923:     /// * [`None`], if there is no embedded `.`;\n  2924:     /// * [`None`], if the file name begins with `.` and has no other `.`s within;\n  2925:     /// * Otherwise, the portion of the file name after the final `.`\n  2926:     ///\n  2927:     /// [`self.file_name`]: Path::file_name\n  2928:     ///\n  2929:     /// # Examples\n  2930:     ///",
    "nanvix_source": "  2925:     /// ```\n  2926:     ///\n  2927:     /// # See Also\n  2928:     /// This method is similar to [`Path::file_stem`], which extracts the portion of the file name\n  2929:     /// before the *last* `.`\n  2930:     ///\n  2931:     /// [`Path::file_stem`]: Path::file_stem\n  2932:     ///\n  2933:     #[stable(feature = \"path_file_prefix\", since = \"1.91.0\")]\n  2934:     #[must_use]\n  2935:     pub fn file_prefix(&self) -> Option<&OsStr> {\n  2936:         self.file_name().map(split_file_at_dot).and_then(|(before, _after)| Some(before))\n  2937:     }\n  2938: \n  2939:     /// Extracts the extension (without the leading dot) of [`self.file_name`], if possible.\n  2940:     ///\n  2941:     /// The extension is:\n  2942:     ///\n  2943:     /// * [`None`], if there is no file name;\n  2944:     /// * [`None`], if there is no embedded `.`;\n  2945:     /// * [`None`], if the file name begins with `.` and has no other `.`s within;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::file_stem",
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
      "name": "file_stem",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "resolved_path": {
                            "args": null,
                            "id": 1857,
                            "path": "OsStr"
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
    "verification_source": "  2863:     ///\n  2864:     /// ```\n  2865:     /// use std::path::Path;\n  2866:     ///\n  2867:     /// assert_eq!(\"foo\", Path::new(\"foo.rs\").file_stem().unwrap());\n  2868:     /// assert_eq!(\"foo.tar\", Path::new(\"foo.tar.gz\").file_stem().unwrap());\n  2869:     /// ```\n  2870:     ///\n  2871:     /// # See Also\n  2872:     /// This method is similar to [`Path::file_prefix`], which extracts the portion of the file name\n  2873:     /// before the *first* `.`\n  2874:     ///\n  2875:     /// [`Path::file_prefix`]: Path::file_prefix\n  2876:     ///\n  2877:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2878:     #[must_use]\n  2879:     pub fn file_stem(&self) -> Option<&OsStr> {\n  2880:         self.file_name().map(rsplit_file_at_dot).and_then(|(before, after)| before.or(after))\n  2881:     }\n  2882: \n  2883:     /// Extracts the prefix of [`self.file_name`].\n  2884:     ///\n  2885:     /// The prefix is:\n  2886:     ///\n  2887:     /// * [`None`], if there is no file name;\n  2888:     /// * The entire file name if there is no embedded `.`;\n  2889:     /// * The portion of the file name before the first non-beginning `.`;\n  2890:     /// * The entire file name if the file name begins with `.` and has no other `.`s within;\n  2891:     /// * The portion of the file name before the second `.` if the file name begins with `.`\n  2892:     ///\n  2893:     /// [`self.file_name`]: Path::file_name\n  2894:     ///\n  2895:     /// # Examples",
    "nanvix_source": "  2890:     /// ```\n  2891:     ///\n  2892:     /// # See Also\n  2893:     /// This method is similar to [`Path::file_prefix`], which extracts the portion of the file name\n  2894:     /// before the *first* `.`\n  2895:     ///\n  2896:     /// [`Path::file_prefix`]: Path::file_prefix\n  2897:     ///\n  2898:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2899:     #[must_use]\n  2900:     pub fn file_stem(&self) -> Option<&OsStr> {\n  2901:         self.file_name().map(rsplit_file_at_dot).and_then(|(before, after)| before.or(after))\n  2902:     }\n  2903: \n  2904:     /// Extracts the prefix of [`self.file_name`].\n  2905:     ///\n  2906:     /// The prefix is:\n  2907:     ///\n  2908:     /// * [`None`], if there is no file name;\n  2909:     /// * The entire file name if there is no embedded `.`;\n  2910:     /// * The portion of the file name before the first non-beginning `.`;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::has_root",
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
      "name": "has_root",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2566:     ///\n  2567:     /// * On Windows, a path has a root if it:\n  2568:     ///     * has no prefix and begins with a separator, e.g., `\\windows`\n  2569:     ///     * has a prefix followed by a separator, e.g., `c:\\windows` but not `c:windows`\n  2570:     ///     * has any non-disk prefix, e.g., `\\\\server\\share`\n  2571:     ///\n  2572:     /// # Examples\n  2573:     ///\n  2574:     /// ```\n  2575:     /// use std::path::Path;\n  2576:     ///\n  2577:     /// assert!(Path::new(\"/etc/passwd\").has_root());\n  2578:     /// ```\n  2579:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2580:     #[must_use]\n  2581:     #[inline]\n  2582:     pub fn has_root(&self) -> bool {\n  2583:         self.components().has_root()\n  2584:     }\n  2585: \n  2586:     /// Returns the `Path` without its final component, if there is one.\n  2587:     ///\n  2588:     /// This means it returns `Some(\"\")` for relative paths with one component.\n  2589:     ///\n  2590:     /// Returns [`None`] if the path terminates in a root or prefix, or if it's\n  2591:     /// the empty string.\n  2592:     ///\n  2593:     /// # Examples\n  2594:     ///\n  2595:     /// ```\n  2596:     /// use std::path::Path;\n  2597:     ///\n  2598:     /// let path = Path::new(\"/foo/bar\");",
    "nanvix_source": "  2590:     /// # Examples\n  2591:     ///\n  2592:     /// ```\n  2593:     /// use std::path::Path;\n  2594:     ///\n  2595:     /// assert!(Path::new(\"/etc/passwd\").has_root());\n  2596:     /// ```\n  2597:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2598:     #[must_use]\n  2599:     #[inline]\n  2600:     pub fn has_root(&self) -> bool {\n  2601:         self.components().has_root()\n  2602:     }\n  2603: \n  2604:     /// Returns the `Path` without its final component, if there is one.\n  2605:     ///\n  2606:     /// This means it returns `Some(\"\")` for relative paths with one component.\n  2607:     ///\n  2608:     /// Returns [`None`] if the path terminates in a root or prefix, or if it's\n  2609:     /// the empty string.\n  2610:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::into_path_buf",
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
      "name": "into_path_buf",
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
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "generic": "Self"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 216,
                "path": "Box"
              }
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
    "verification_source": "  3635:     ///\n  3636:     /// # See Also\n  3637:     ///\n  3638:     /// This is a convenience function that coerces errors to false. If you want to\n  3639:     /// check errors, call [`fs::symlink_metadata`] and handle its [`Result`]. Then call\n  3640:     /// [`fs::Metadata::is_symlink`] if it was [`Ok`].\n  3641:     #[must_use]\n  3642:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  3643:     pub fn is_symlink(&self) -> bool {\n  3644:         fs::symlink_metadata(self).map(|m| m.is_symlink()).unwrap_or(false)\n  3645:     }\n  3646: \n  3647:     /// Converts a [`Box<Path>`](Box) into a [`PathBuf`] without copying or\n  3648:     /// allocating.\n  3649:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  3650:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  3651:     pub fn into_path_buf(self: Box<Self>) -> PathBuf {\n  3652:         let rw = Box::into_raw(self) as *mut OsStr;\n  3653:         let inner = unsafe { Box::from_raw(rw) };\n  3654:         PathBuf { inner: OsString::from(inner) }\n  3655:     }\n  3656: }\n  3657: \n  3658: #[unstable(feature = \"clone_to_uninit\", issue = \"126799\")]\n  3659: unsafe impl CloneToUninit for Path {\n  3660:     #[inline]\n  3661:     #[cfg_attr(debug_assertions, track_caller)]\n  3662:     unsafe fn clone_to_uninit(&self, dst: *mut u8) {\n  3663:         // SAFETY: Path is just a transparent wrapper around OsStr\n  3664:         unsafe { self.inner.clone_to_uninit(dst) }\n  3665:     }\n  3666: }\n  3667: ",
    "nanvix_source": "  3671:     #[must_use]\n  3672:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  3673:     pub fn is_symlink(&self) -> bool {\n  3674:         fs::symlink_metadata(self).map(|m| m.is_symlink()).unwrap_or(false)\n  3675:     }\n  3676: \n  3677:     /// Converts a [`Box<Path>`](Box) into a [`PathBuf`] without copying or\n  3678:     /// allocating.\n  3679:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  3680:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  3681:     pub fn into_path_buf(self: Box<Self>) -> PathBuf {\n  3682:         let rw = Box::into_raw(self) as *mut OsStr;\n  3683:         let inner = unsafe { Box::from_raw(rw) };\n  3684:         PathBuf { inner: OsString::from(inner) }\n  3685:     }\n  3686: }\n  3687: \n  3688: #[unstable(feature = \"clone_to_uninit\", issue = \"126799\")]\n  3689: unsafe impl CloneToUninit for Path {\n  3690:     #[inline]\n  3691:     #[cfg_attr(debug_assertions, track_caller)]",
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
