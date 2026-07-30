For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::starts_with",
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
      "name": "starts_with",
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
            "base",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2777:     ///\n  2778:     /// let path = Path::new(\"/etc/passwd\");\n  2779:     ///\n  2780:     /// assert!(path.starts_with(\"/etc\"));\n  2781:     /// assert!(path.starts_with(\"/etc/\"));\n  2782:     /// assert!(path.starts_with(\"/etc/passwd\"));\n  2783:     /// assert!(path.starts_with(\"/etc/passwd/\")); // extra slash is okay\n  2784:     /// assert!(path.starts_with(\"/etc/passwd///\")); // multiple extra slashes are okay\n  2785:     ///\n  2786:     /// assert!(!path.starts_with(\"/e\"));\n  2787:     /// assert!(!path.starts_with(\"/etc/passwd.txt\"));\n  2788:     ///\n  2789:     /// assert!(!Path::new(\"/etc/foo.rs\").starts_with(\"/etc/foo\"));\n  2790:     /// ```\n  2791:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2792:     #[must_use]\n  2793:     pub fn starts_with<P: AsRef<Path>>(&self, base: P) -> bool {\n  2794:         self._starts_with(base.as_ref())\n  2795:     }\n  2796: \n  2797:     fn _starts_with(&self, base: &Path) -> bool {\n  2798:         iter_after(self.components(), base.components()).is_some()\n  2799:     }\n  2800: \n  2801:     /// Determines whether `child` is a suffix of `self`.\n  2802:     ///\n  2803:     /// Only considers whole path components to match.\n  2804:     ///\n  2805:     /// # Examples\n  2806:     ///\n  2807:     /// ```\n  2808:     /// use std::path::Path;\n  2809:     ///",
    "nanvix_source": "  2801:     /// assert!(path.starts_with(\"/etc/passwd/\")); // extra slash is okay\n  2802:     /// assert!(path.starts_with(\"/etc/passwd///\")); // multiple extra slashes are okay\n  2803:     ///\n  2804:     /// assert!(!path.starts_with(\"/e\"));\n  2805:     /// assert!(!path.starts_with(\"/etc/passwd.txt\"));\n  2806:     ///\n  2807:     /// assert!(!Path::new(\"/etc/foo.rs\").starts_with(\"/etc/foo\"));\n  2808:     /// ```\n  2809:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2810:     #[must_use]\n  2811:     pub fn starts_with<P: AsRef<Path>>(&self, base: P) -> bool {\n  2812:         self._starts_with(base.as_ref())\n  2813:     }\n  2814: \n  2815:     fn _starts_with(&self, base: &Path) -> bool {\n  2816:         iter_after(self.components(), base.components()).is_some()\n  2817:     }\n  2818: \n  2819:     /// Determines whether `child` is a suffix of `self`.\n  2820:     ///\n  2821:     /// Only considers whole path components to match.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::strip_prefix",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
              "generic_params": [],
              "type": {
                "generic": "P"
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
      "name": "strip_prefix",
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
          ],
          [
            "base",
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
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 7090,
                        "path": "StripPrefixError"
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
    "verification_source": "  2705:     /// let path = Path::new(\"/test/haha/foo.txt\");\n  2706:     ///\n  2707:     /// assert_eq!(path.strip_prefix(\"/\"), Ok(Path::new(\"test/haha/foo.txt\")));\n  2708:     /// assert_eq!(path.strip_prefix(\"/test\"), Ok(Path::new(\"haha/foo.txt\")));\n  2709:     /// assert_eq!(path.strip_prefix(\"/test/\"), Ok(Path::new(\"haha/foo.txt\")));\n  2710:     /// assert_eq!(path.strip_prefix(\"/test/haha/foo.txt\"), Ok(Path::new(\"\")));\n  2711:     /// assert_eq!(path.strip_prefix(\"/test/haha/foo.txt/\"), Ok(Path::new(\"\")));\n  2712:     ///\n  2713:     /// assert!(path.strip_prefix(\"test\").is_err());\n  2714:     /// assert!(path.strip_prefix(\"/te\").is_err());\n  2715:     /// assert!(path.strip_prefix(\"/haha\").is_err());\n  2716:     ///\n  2717:     /// let prefix = PathBuf::from(\"/test/\");\n  2718:     /// assert_eq!(path.strip_prefix(prefix), Ok(Path::new(\"haha/foo.txt\")));\n  2719:     /// ```\n  2720:     #[stable(since = \"1.7.0\", feature = \"path_strip_prefix\")]\n  2721:     pub fn strip_prefix<P>(&self, base: P) -> Result<&Path, StripPrefixError>\n  2722:     where\n  2723:         P: AsRef<Path>,\n  2724:     {\n  2725:         self._strip_prefix(base.as_ref())\n  2726:     }\n  2727: \n  2728:     /// Returns a path with the optional prefix removed.\n  2729:     ///\n  2730:     /// If `base` is not a prefix of `self` (i.e., [`starts_with`] returns `false`), returns the original path (`self`)\n  2731:     ///\n  2732:     /// [`starts_with`]: Path::starts_with\n  2733:     ///\n  2734:     /// # Examples\n  2735:     ///\n  2736:     /// ```\n  2737:     /// #![feature(trim_prefix_suffix)]",
    "nanvix_source": "  2729:     /// assert_eq!(path.strip_prefix(\"/test/haha/foo.txt/\"), Ok(Path::new(\"\")));\n  2730:     ///\n  2731:     /// assert!(path.strip_prefix(\"test\").is_err());\n  2732:     /// assert!(path.strip_prefix(\"/te\").is_err());\n  2733:     /// assert!(path.strip_prefix(\"/haha\").is_err());\n  2734:     ///\n  2735:     /// let prefix = PathBuf::from(\"/test/\");\n  2736:     /// assert_eq!(path.strip_prefix(prefix), Ok(Path::new(\"haha/foo.txt\")));\n  2737:     /// ```\n  2738:     #[stable(since = \"1.7.0\", feature = \"path_strip_prefix\")]\n  2739:     pub fn strip_prefix<P>(&self, base: P) -> Result<&Path, StripPrefixError>\n  2740:     where\n  2741:         P: AsRef<Path>,\n  2742:     {\n  2743:         self._strip_prefix(base.as_ref())\n  2744:     }\n  2745: \n  2746:     /// Returns a path with the optional prefix removed.\n  2747:     ///\n  2748:     /// If `base` is not a prefix of `self` (i.e., [`starts_with`] returns `false`), returns the original path (`self`)\n  2749:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::symlink_metadata",
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
      "name": "symlink_metadata",
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
                      "resolved_path": {
                        "args": null,
                        "id": 2584,
                        "path": "fs::Metadata"
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
    "verification_source": "  3310: \n  3311:     /// Queries the metadata about a file without following symlinks.\n  3312:     ///\n  3313:     /// This is an alias to [`fs::symlink_metadata`].\n  3314:     ///\n  3315:     /// # Examples\n  3316:     ///\n  3317:     /// ```no_run\n  3318:     /// use std::path::Path;\n  3319:     ///\n  3320:     /// let path = Path::new(\"/Minas/tirith\");\n  3321:     /// let metadata = path.symlink_metadata().expect(\"symlink_metadata call failed\");\n  3322:     /// println!(\"{:?}\", metadata.file_type());\n  3323:     /// ```\n  3324:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3325:     #[inline]\n  3326:     pub fn symlink_metadata(&self) -> io::Result<fs::Metadata> {\n  3327:         fs::symlink_metadata(self)\n  3328:     }\n  3329: \n  3330:     /// Returns the canonical, absolute form of the path with all intermediate\n  3331:     /// components normalized and symbolic links resolved.\n  3332:     ///\n  3333:     /// This is an alias to [`fs::canonicalize`].\n  3334:     ///\n  3335:     /// # Errors\n  3336:     ///\n  3337:     /// This method will return an error in the following situations, but is not\n  3338:     /// limited to just these cases:\n  3339:     ///\n  3340:     /// * `path` does not exist.\n  3341:     /// * A non-final component in path is not a directory.\n  3342:     ///",
    "nanvix_source": "  3346:     ///\n  3347:     /// ```no_run\n  3348:     /// use std::path::Path;\n  3349:     ///\n  3350:     /// let path = Path::new(\"/Minas/tirith\");\n  3351:     /// let metadata = path.symlink_metadata().expect(\"symlink_metadata call failed\");\n  3352:     /// println!(\"{:?}\", metadata.file_type());\n  3353:     /// ```\n  3354:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3355:     #[inline]\n  3356:     pub fn symlink_metadata(&self) -> io::Result<fs::Metadata> {\n  3357:         fs::symlink_metadata(self)\n  3358:     }\n  3359: \n  3360:     /// Returns the canonical, absolute form of the path with all intermediate\n  3361:     /// components normalized and symbolic links resolved.\n  3362:     ///\n  3363:     /// This is an alias to [`fs::canonicalize`].\n  3364:     ///\n  3365:     /// # Errors\n  3366:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::to_path_buf",
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
      "name": "to_path_buf",
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
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        }
      }
    },
    "verification_source": "  2494: \n  2495:     /// Converts a `Path` to an owned [`PathBuf`].\n  2496:     ///\n  2497:     /// # Examples\n  2498:     ///\n  2499:     /// ```\n  2500:     /// use std::path::{Path, PathBuf};\n  2501:     ///\n  2502:     /// let path_buf = Path::new(\"foo.txt\").to_path_buf();\n  2503:     /// assert_eq!(path_buf, PathBuf::from(\"foo.txt\"));\n  2504:     /// ```\n  2505:     #[rustc_conversion_suggestion]\n  2506:     #[must_use = \"this returns the result of the operation, \\\n  2507:                   without modifying the original\"]\n  2508:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2509:     #[cfg_attr(not(test), rustc_diagnostic_item = \"path_to_pathbuf\")]\n  2510:     pub fn to_path_buf(&self) -> PathBuf {\n  2511:         PathBuf::from(self.inner.to_os_string())\n  2512:     }\n  2513: \n  2514:     /// Returns `true` if the `Path` is absolute, i.e., if it is independent of\n  2515:     /// the current directory.\n  2516:     ///\n  2517:     /// * On Unix, a path is absolute if it starts with the root, so\n  2518:     /// `is_absolute` and [`has_root`] are equivalent.\n  2519:     ///\n  2520:     /// * On Windows, a path is absolute if it has a prefix and starts with the\n  2521:     /// root: `c:\\windows` is absolute, while `c:temp` and `\\temp` are not.\n  2522:     ///\n  2523:     /// # Examples\n  2524:     ///\n  2525:     /// ```\n  2526:     /// use std::path::Path;",
    "nanvix_source": "  2518:     /// use std::path::{Path, PathBuf};\n  2519:     ///\n  2520:     /// let path_buf = Path::new(\"foo.txt\").to_path_buf();\n  2521:     /// assert_eq!(path_buf, PathBuf::from(\"foo.txt\"));\n  2522:     /// ```\n  2523:     #[rustc_conversion_suggestion]\n  2524:     #[must_use = \"this returns the result of the operation, \\\n  2525:                   without modifying the original\"]\n  2526:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2527:     #[cfg_attr(not(test), rustc_diagnostic_item = \"path_to_pathbuf\")]\n  2528:     pub fn to_path_buf(&self) -> PathBuf {\n  2529:         PathBuf::from(self.inner.to_os_string())\n  2530:     }\n  2531: \n  2532:     /// Returns `true` if the `Path` is absolute, i.e., if it is independent of\n  2533:     /// the current directory.\n  2534:     ///\n  2535:     /// * On Unix, a path is absolute if it starts with the root, so\n  2536:     /// `is_absolute` and [`has_root`] are equivalent.\n  2537:     ///\n  2538:     /// * On Windows, a path is absolute if it has a prefix and starts with the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::to_str",
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
      "name": "to_str",
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
                          "primitive": "str"
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
    "verification_source": "  2447:     /// perfectly valid for some OS.\n  2448:     ///\n  2449:     /// [`&str`]: str\n  2450:     ///\n  2451:     /// # Examples\n  2452:     ///\n  2453:     /// ```\n  2454:     /// use std::path::Path;\n  2455:     ///\n  2456:     /// let path = Path::new(\"foo.txt\");\n  2457:     /// assert_eq!(path.to_str(), Some(\"foo.txt\"));\n  2458:     /// ```\n  2459:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2460:     #[must_use = \"this returns the result of the operation, \\\n  2461:                   without modifying the original\"]\n  2462:     #[inline]\n  2463:     pub fn to_str(&self) -> Option<&str> {\n  2464:         self.inner.to_str()\n  2465:     }\n  2466: \n  2467:     /// Converts a `Path` to a [`Cow<str>`].\n  2468:     ///\n  2469:     /// Any non-UTF-8 sequences are replaced with\n  2470:     /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD].\n  2471:     ///\n  2472:     /// [U+FFFD]: super::char::REPLACEMENT_CHARACTER\n  2473:     ///\n  2474:     /// # Examples\n  2475:     ///\n  2476:     /// Calling `to_string_lossy` on a `Path` with valid unicode:\n  2477:     ///\n  2478:     /// ```\n  2479:     /// use std::path::Path;",
    "nanvix_source": "  2471:     /// ```\n  2472:     /// use std::path::Path;\n  2473:     ///\n  2474:     /// let path = Path::new(\"foo.txt\");\n  2475:     /// assert_eq!(path.to_str(), Some(\"foo.txt\"));\n  2476:     /// ```\n  2477:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2478:     #[must_use = \"this returns the result of the operation, \\\n  2479:                   without modifying the original\"]\n  2480:     #[inline]\n  2481:     pub fn to_str(&self) -> Option<&str> {\n  2482:         self.inner.to_str()\n  2483:     }\n  2484: \n  2485:     /// Converts a `Path` to a [`Cow<str>`].\n  2486:     ///\n  2487:     /// Any non-UTF-8 sequences are replaced with\n  2488:     /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD].\n  2489:     ///\n  2490:     /// [U+FFFD]: super::char::REPLACEMENT_CHARACTER\n  2491:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::to_string_lossy",
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
      "name": "to_string_lossy",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "primitive": "str"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2178,
            "path": "Cow"
          }
        }
      }
    },
    "verification_source": "  2475:     ///\n  2476:     /// Calling `to_string_lossy` on a `Path` with valid unicode:\n  2477:     ///\n  2478:     /// ```\n  2479:     /// use std::path::Path;\n  2480:     ///\n  2481:     /// let path = Path::new(\"foo.txt\");\n  2482:     /// assert_eq!(path.to_string_lossy(), \"foo.txt\");\n  2483:     /// ```\n  2484:     ///\n  2485:     /// Had `path` contained invalid unicode, the `to_string_lossy` call might\n  2486:     /// have returned `\"fo\ufffd.txt\"`.\n  2487:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2488:     #[must_use = \"this returns the result of the operation, \\\n  2489:                   without modifying the original\"]\n  2490:     #[inline]\n  2491:     pub fn to_string_lossy(&self) -> Cow<'_, str> {\n  2492:         self.inner.to_string_lossy()\n  2493:     }\n  2494: \n  2495:     /// Converts a `Path` to an owned [`PathBuf`].\n  2496:     ///\n  2497:     /// # Examples\n  2498:     ///\n  2499:     /// ```\n  2500:     /// use std::path::{Path, PathBuf};\n  2501:     ///\n  2502:     /// let path_buf = Path::new(\"foo.txt\").to_path_buf();\n  2503:     /// assert_eq!(path_buf, PathBuf::from(\"foo.txt\"));\n  2504:     /// ```\n  2505:     #[rustc_conversion_suggestion]\n  2506:     #[must_use = \"this returns the result of the operation, \\\n  2507:                   without modifying the original\"]",
    "nanvix_source": "  2499:     /// let path = Path::new(\"foo.txt\");\n  2500:     /// assert_eq!(path.to_string_lossy(), \"foo.txt\");\n  2501:     /// ```\n  2502:     ///\n  2503:     /// Had `path` contained invalid unicode, the `to_string_lossy` call might\n  2504:     /// have returned `\"fo\ufffd.txt\"`.\n  2505:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2506:     #[must_use = \"this returns the result of the operation, \\\n  2507:                   without modifying the original\"]\n  2508:     #[inline]\n  2509:     pub fn to_string_lossy(&self) -> Cow<'_, str> {\n  2510:         self.inner.to_string_lossy()\n  2511:     }\n  2512: \n  2513:     /// Converts a `Path` to an owned [`PathBuf`].\n  2514:     ///\n  2515:     /// # Examples\n  2516:     ///\n  2517:     /// ```\n  2518:     /// use std::path::{Path, PathBuf};\n  2519:     ///",
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
