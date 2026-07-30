For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::is_absolute",
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
      "name": "is_absolute",
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
    "verification_source": "  2519:     ///\n  2520:     /// * On Windows, a path is absolute if it has a prefix and starts with the\n  2521:     /// root: `c:\\windows` is absolute, while `c:temp` and `\\temp` are not.\n  2522:     ///\n  2523:     /// # Examples\n  2524:     ///\n  2525:     /// ```\n  2526:     /// use std::path::Path;\n  2527:     ///\n  2528:     /// assert!(!Path::new(\"foo.txt\").is_absolute());\n  2529:     /// ```\n  2530:     ///\n  2531:     /// [`has_root`]: Path::has_root\n  2532:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2533:     #[must_use]\n  2534:     #[allow(deprecated)]\n  2535:     pub fn is_absolute(&self) -> bool {\n  2536:         sys::path::is_absolute(self)\n  2537:     }\n  2538: \n  2539:     /// Returns `true` if the `Path` is relative, i.e., not absolute.\n  2540:     ///\n  2541:     /// See [`is_absolute`]'s documentation for more details.\n  2542:     ///\n  2543:     /// # Examples\n  2544:     ///\n  2545:     /// ```\n  2546:     /// use std::path::Path;\n  2547:     ///\n  2548:     /// assert!(Path::new(\"foo.txt\").is_relative());\n  2549:     /// ```\n  2550:     ///\n  2551:     /// [`is_absolute`]: Path::is_absolute",
    "nanvix_source": "  2543:     /// ```\n  2544:     /// use std::path::Path;\n  2545:     ///\n  2546:     /// assert!(!Path::new(\"foo.txt\").is_absolute());\n  2547:     /// ```\n  2548:     ///\n  2549:     /// [`has_root`]: Path::has_root\n  2550:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2551:     #[must_use]\n  2552:     #[allow(deprecated)]\n  2553:     pub fn is_absolute(&self) -> bool {\n  2554:         sys::path::is_absolute(self)\n  2555:     }\n  2556: \n  2557:     /// Returns `true` if the `Path` is relative, i.e., not absolute.\n  2558:     ///\n  2559:     /// See [`is_absolute`]'s documentation for more details.\n  2560:     ///\n  2561:     /// # Examples\n  2562:     ///\n  2563:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::is_dir",
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
      "name": "is_dir",
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
    "verification_source": "  3594:     ///\n  3595:     /// # Examples\n  3596:     ///\n  3597:     /// ```no_run\n  3598:     /// use std::path::Path;\n  3599:     /// assert_eq!(Path::new(\"./is_a_directory/\").is_dir(), true);\n  3600:     /// assert_eq!(Path::new(\"a_file.txt\").is_dir(), false);\n  3601:     /// ```\n  3602:     ///\n  3603:     /// # See Also\n  3604:     ///\n  3605:     /// This is a convenience function that coerces errors to false. If you want to\n  3606:     /// check errors, call [`fs::metadata`] and handle its [`Result`]. Then call\n  3607:     /// [`fs::Metadata::is_dir`] if it was [`Ok`].\n  3608:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3609:     #[must_use]\n  3610:     pub fn is_dir(&self) -> bool {\n  3611:         fs::metadata(self).map(|m| m.is_dir()).unwrap_or(false)\n  3612:     }\n  3613: \n  3614:     /// Returns `true` if the path exists on disk and is pointing at a symbolic link.\n  3615:     ///\n  3616:     /// This function will not traverse symbolic links.\n  3617:     /// In case of a broken symbolic link this will also return true.\n  3618:     ///\n  3619:     /// If you cannot access the directory containing the file, e.g., because of a\n  3620:     /// permission error, this will return false.\n  3621:     ///\n  3622:     /// # Examples\n  3623:     ///\n  3624:     /// ```rust,no_run\n  3625:     /// # #[cfg(unix)] {\n  3626:     /// use std::path::Path;",
    "nanvix_source": "  3630:     /// assert_eq!(Path::new(\"a_file.txt\").is_dir(), false);\n  3631:     /// ```\n  3632:     ///\n  3633:     /// # See Also\n  3634:     ///\n  3635:     /// This is a convenience function that coerces errors to false. If you want to\n  3636:     /// check errors, call [`fs::metadata`] and handle its [`Result`]. Then call\n  3637:     /// [`fs::Metadata::is_dir`] if it was [`Ok`].\n  3638:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3639:     #[must_use]\n  3640:     pub fn is_dir(&self) -> bool {\n  3641:         fs::metadata(self).map(|m| m.is_dir()).unwrap_or(false)\n  3642:     }\n  3643: \n  3644:     /// Returns `true` if the path exists on disk and is pointing at a symbolic link.\n  3645:     ///\n  3646:     /// This function will not traverse symbolic links.\n  3647:     /// In case of a broken symbolic link this will also return true.\n  3648:     ///\n  3649:     /// If you cannot access the directory containing the file, e.g., because of a\n  3650:     /// permission error, this will return false.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::is_empty",
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
      "name": "is_empty",
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
    "verification_source": "  2831:     /// # Examples\n  2832:     ///\n  2833:     /// ```\n  2834:     /// #![feature(path_is_empty)]\n  2835:     /// use std::path::Path;\n  2836:     ///\n  2837:     /// let path = Path::new(\"\");\n  2838:     /// assert!(path.is_empty());\n  2839:     ///\n  2840:     /// let path = Path::new(\"foo\");\n  2841:     /// assert!(!path.is_empty());\n  2842:     ///\n  2843:     /// let path = Path::new(\".\");\n  2844:     /// assert!(!path.is_empty());\n  2845:     /// ```\n  2846:     #[unstable(feature = \"path_is_empty\", issue = \"148494\")]\n  2847:     pub fn is_empty(&self) -> bool {\n  2848:         self.as_os_str().is_empty()\n  2849:     }\n  2850: \n  2851:     /// Extracts the stem (non-extension) portion of [`self.file_name`].\n  2852:     ///\n  2853:     /// [`self.file_name`]: Path::file_name\n  2854:     ///\n  2855:     /// The stem is:\n  2856:     ///\n  2857:     /// * [`None`], if there is no file name;\n  2858:     /// * The entire file name if there is no embedded `.`;\n  2859:     /// * The entire file name if the file name begins with `.` and has no other `.`s within;\n  2860:     /// * Otherwise, the portion of the file name before the final `.`\n  2861:     ///\n  2862:     /// # Examples\n  2863:     ///",
    "nanvix_source": "  2858:     /// let path = Path::new(\"\");\n  2859:     /// assert!(path.is_empty());\n  2860:     ///\n  2861:     /// let path = Path::new(\"foo\");\n  2862:     /// assert!(!path.is_empty());\n  2863:     ///\n  2864:     /// let path = Path::new(\".\");\n  2865:     /// assert!(!path.is_empty());\n  2866:     /// ```\n  2867:     #[stable(feature = \"path_is_empty\", since = \"CURRENT_RUSTC_VERSION\")]\n  2868:     pub fn is_empty(&self) -> bool {\n  2869:         self.as_os_str().is_empty()\n  2870:     }\n  2871: \n  2872:     /// Extracts the stem (non-extension) portion of [`self.file_name`].\n  2873:     ///\n  2874:     /// [`self.file_name`]: Path::file_name\n  2875:     ///\n  2876:     /// The stem is:\n  2877:     ///\n  2878:     /// * [`None`], if there is no file name;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::is_file",
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
      "name": "is_file",
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
    "verification_source": "  3567:     /// assert_eq!(Path::new(\"a_file.txt\").is_file(), true);\n  3568:     /// ```\n  3569:     ///\n  3570:     /// # See Also\n  3571:     ///\n  3572:     /// This is a convenience function that coerces errors to false. If you want to\n  3573:     /// check errors, call [`fs::metadata`] and handle its [`Result`]. Then call\n  3574:     /// [`fs::Metadata::is_file`] if it was [`Ok`].\n  3575:     ///\n  3576:     /// When the goal is simply to read from (or write to) the source, the most\n  3577:     /// reliable way to test the source can be read (or written to) is to open\n  3578:     /// it. Only using `is_file` can break workflows like `diff <( prog_a )` on\n  3579:     /// a Unix-like system for example. See [`fs::File::open`] or\n  3580:     /// [`fs::OpenOptions::open`] for more information.\n  3581:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3582:     #[must_use]\n  3583:     pub fn is_file(&self) -> bool {\n  3584:         fs::metadata(self).map(|m| m.is_file()).unwrap_or(false)\n  3585:     }\n  3586: \n  3587:     /// Returns `true` if the path exists on disk and is pointing at a directory.\n  3588:     ///\n  3589:     /// This function will traverse symbolic links to query information about the\n  3590:     /// destination file.\n  3591:     ///\n  3592:     /// If you cannot access the metadata of the file, e.g. because of a\n  3593:     /// permission error or broken symbolic links, this will return `false`.\n  3594:     ///\n  3595:     /// # Examples\n  3596:     ///\n  3597:     /// ```no_run\n  3598:     /// use std::path::Path;\n  3599:     /// assert_eq!(Path::new(\"./is_a_directory/\").is_dir(), true);",
    "nanvix_source": "  3603:     /// check errors, call [`fs::metadata`] and handle its [`Result`]. Then call\n  3604:     /// [`fs::Metadata::is_file`] if it was [`Ok`].\n  3605:     ///\n  3606:     /// When the goal is simply to read from (or write to) the source, the most\n  3607:     /// reliable way to test the source can be read (or written to) is to open\n  3608:     /// it. Only using `is_file` can break workflows like `diff <( prog_a )` on\n  3609:     /// a Unix-like system for example. See [`fs::File::open`] or\n  3610:     /// [`fs::OpenOptions::open`] for more information.\n  3611:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3612:     #[must_use]\n  3613:     pub fn is_file(&self) -> bool {\n  3614:         fs::metadata(self).map(|m| m.is_file()).unwrap_or(false)\n  3615:     }\n  3616: \n  3617:     /// Returns `true` if the path exists on disk and is pointing at a directory.\n  3618:     ///\n  3619:     /// This function will traverse symbolic links to query information about the\n  3620:     /// destination file.\n  3621:     ///\n  3622:     /// If you cannot access the metadata of the file, e.g. because of a\n  3623:     /// permission error or broken symbolic links, this will return `false`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::is_relative",
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
      "name": "is_relative",
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
    "verification_source": "  2539:     /// Returns `true` if the `Path` is relative, i.e., not absolute.\n  2540:     ///\n  2541:     /// See [`is_absolute`]'s documentation for more details.\n  2542:     ///\n  2543:     /// # Examples\n  2544:     ///\n  2545:     /// ```\n  2546:     /// use std::path::Path;\n  2547:     ///\n  2548:     /// assert!(Path::new(\"foo.txt\").is_relative());\n  2549:     /// ```\n  2550:     ///\n  2551:     /// [`is_absolute`]: Path::is_absolute\n  2552:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2553:     #[must_use]\n  2554:     #[inline]\n  2555:     pub fn is_relative(&self) -> bool {\n  2556:         !self.is_absolute()\n  2557:     }\n  2558: \n  2559:     pub(crate) fn prefix(&self) -> Option<Prefix<'_>> {\n  2560:         self.components().prefix\n  2561:     }\n  2562: \n  2563:     /// Returns `true` if the `Path` has a root.\n  2564:     ///\n  2565:     /// * On Unix, a path has a root if it begins with `/`.\n  2566:     ///\n  2567:     /// * On Windows, a path has a root if it:\n  2568:     ///     * has no prefix and begins with a separator, e.g., `\\windows`\n  2569:     ///     * has a prefix followed by a separator, e.g., `c:\\windows` but not `c:windows`\n  2570:     ///     * has any non-disk prefix, e.g., `\\\\server\\share`\n  2571:     ///",
    "nanvix_source": "  2563:     /// ```\n  2564:     /// use std::path::Path;\n  2565:     ///\n  2566:     /// assert!(Path::new(\"foo.txt\").is_relative());\n  2567:     /// ```\n  2568:     ///\n  2569:     /// [`is_absolute`]: Path::is_absolute\n  2570:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2571:     #[must_use]\n  2572:     #[inline]\n  2573:     pub fn is_relative(&self) -> bool {\n  2574:         !self.is_absolute()\n  2575:     }\n  2576: \n  2577:     pub(crate) fn prefix(&self) -> Option<Prefix<'_>> {\n  2578:         self.components().prefix\n  2579:     }\n  2580: \n  2581:     /// Returns `true` if the `Path` has a root.\n  2582:     ///\n  2583:     /// * On Unix, a path has a root if it begins with `/`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::is_symlink",
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
      "name": "is_symlink",
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
    "verification_source": "  3627:     /// use std::os::unix::fs::symlink;\n  3628:     ///\n  3629:     /// let link_path = Path::new(\"link\");\n  3630:     /// symlink(\"/origin_does_not_exist/\", link_path).unwrap();\n  3631:     /// assert_eq!(link_path.is_symlink(), true);\n  3632:     /// assert_eq!(link_path.exists(), false);\n  3633:     /// # }\n  3634:     /// ```\n  3635:     ///\n  3636:     /// # See Also\n  3637:     ///\n  3638:     /// This is a convenience function that coerces errors to false. If you want to\n  3639:     /// check errors, call [`fs::symlink_metadata`] and handle its [`Result`]. Then call\n  3640:     /// [`fs::Metadata::is_symlink`] if it was [`Ok`].\n  3641:     #[must_use]\n  3642:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  3643:     pub fn is_symlink(&self) -> bool {\n  3644:         fs::symlink_metadata(self).map(|m| m.is_symlink()).unwrap_or(false)\n  3645:     }\n  3646: \n  3647:     /// Converts a [`Box<Path>`](Box) into a [`PathBuf`] without copying or\n  3648:     /// allocating.\n  3649:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  3650:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  3651:     pub fn into_path_buf(self: Box<Self>) -> PathBuf {\n  3652:         let rw = Box::into_raw(self) as *mut OsStr;\n  3653:         let inner = unsafe { Box::from_raw(rw) };\n  3654:         PathBuf { inner: OsString::from(inner) }\n  3655:     }\n  3656: }\n  3657: \n  3658: #[unstable(feature = \"clone_to_uninit\", issue = \"126799\")]\n  3659: unsafe impl CloneToUninit for Path {",
    "nanvix_source": "  3663:     /// # }\n  3664:     /// ```\n  3665:     ///\n  3666:     /// # See Also\n  3667:     ///\n  3668:     /// This is a convenience function that coerces errors to false. If you want to\n  3669:     /// check errors, call [`fs::symlink_metadata`] and handle its [`Result`]. Then call\n  3670:     /// [`fs::Metadata::is_symlink`] if it was [`Ok`].\n  3671:     #[must_use]\n  3672:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  3673:     pub fn is_symlink(&self) -> bool {\n  3674:         fs::symlink_metadata(self).map(|m| m.is_symlink()).unwrap_or(false)\n  3675:     }\n  3676: \n  3677:     /// Converts a [`Box<Path>`](Box) into a [`PathBuf`] without copying or\n  3678:     /// allocating.\n  3679:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  3680:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  3681:     pub fn into_path_buf(self: Box<Self>) -> PathBuf {\n  3682:         let rw = Box::into_raw(self) as *mut OsStr;\n  3683:         let inner = unsafe { Box::from_raw(rw) };",
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
