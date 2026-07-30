For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::DirEntry::file_name",
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
      "name": "file_name",
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
            "id": 2885,
            "path": "DirEntry"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2912",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2885",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirEntry"
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
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "  2625:     /// # Examples\n  2626:     ///\n  2627:     /// ```\n  2628:     /// use std::fs;\n  2629:     ///\n  2630:     /// if let Ok(entries) = fs::read_dir(\".\") {\n  2631:     ///     for entry in entries {\n  2632:     ///         if let Ok(entry) = entry {\n  2633:     ///             // Here, `entry` is a `DirEntry`.\n  2634:     ///             println!(\"{:?}\", entry.file_name());\n  2635:     ///         }\n  2636:     ///     }\n  2637:     /// }\n  2638:     /// ```\n  2639:     #[must_use]\n  2640:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2641:     pub fn file_name(&self) -> OsString {\n  2642:         self.0.file_name()\n  2643:     }\n  2644: }\n  2645: \n  2646: #[stable(feature = \"dir_entry_debug\", since = \"1.13.0\")]\n  2647: impl fmt::Debug for DirEntry {\n  2648:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2649:         f.debug_tuple(\"DirEntry\").field(&self.path()).finish()\n  2650:     }\n  2651: }\n  2652: \n  2653: impl AsInner<fs_imp::DirEntry> for DirEntry {\n  2654:     #[inline]\n  2655:     fn as_inner(&self) -> &fs_imp::DirEntry {\n  2656:         &self.0\n  2657:     }",
    "nanvix_source": "  2602:     ///     for entry in entries {\n  2603:     ///         if let Ok(entry) = entry {\n  2604:     ///             // Here, `entry` is a `DirEntry`.\n  2605:     ///             println!(\"{:?}\", entry.file_name());\n  2606:     ///         }\n  2607:     ///     }\n  2608:     /// }\n  2609:     /// ```\n  2610:     #[must_use]\n  2611:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2612:     pub fn file_name(&self) -> OsString {\n  2613:         self.0.file_name()\n  2614:     }\n  2615: }\n  2616: \n  2617: #[stable(feature = \"dir_entry_debug\", since = \"1.13.0\")]\n  2618: impl fmt::Debug for DirEntry {\n  2619:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2620:         f.debug_tuple(\"DirEntry\").field(&self.path()).finish()\n  2621:     }\n  2622: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirEntry::file_type",
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
      "name": "file_type",
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
            "id": 2885,
            "path": "DirEntry"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2912",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2885",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirEntry"
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
                        "id": 2774,
                        "path": "FileType"
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
    "verification_source": "  2596:     ///\n  2597:     /// if let Ok(entries) = fs::read_dir(\".\") {\n  2598:     ///     for entry in entries {\n  2599:     ///         if let Ok(entry) = entry {\n  2600:     ///             // Here, `entry` is a `DirEntry`.\n  2601:     ///             if let Ok(file_type) = entry.file_type() {\n  2602:     ///                 // Now let's show our entry's file type!\n  2603:     ///                 println!(\"{:?}: {:?}\", entry.path(), file_type);\n  2604:     ///             } else {\n  2605:     ///                 println!(\"Couldn't get file type for {:?}\", entry.path());\n  2606:     ///             }\n  2607:     ///         }\n  2608:     ///     }\n  2609:     /// }\n  2610:     /// ```\n  2611:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2612:     pub fn file_type(&self) -> io::Result<FileType> {\n  2613:         self.0.file_type().map(FileType)\n  2614:     }\n  2615: \n  2616:     /// Returns the file name of this directory entry without any\n  2617:     /// leading path component(s).\n  2618:     ///\n  2619:     /// As an example,\n  2620:     /// the output of the function will result in \"foo\" for all the following paths:\n  2621:     /// - \"./foo\"\n  2622:     /// - \"/the/foo\"\n  2623:     /// - \"../../foo\"\n  2624:     ///\n  2625:     /// # Examples\n  2626:     ///\n  2627:     /// ```\n  2628:     /// use std::fs;",
    "nanvix_source": "  2573:     ///                 // Now let's show our entry's file type!\n  2574:     ///                 println!(\"{:?}: {:?}\", entry.path(), file_type);\n  2575:     ///             } else {\n  2576:     ///                 println!(\"Couldn't get file type for {:?}\", entry.path());\n  2577:     ///             }\n  2578:     ///         }\n  2579:     ///     }\n  2580:     /// }\n  2581:     /// ```\n  2582:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2583:     pub fn file_type(&self) -> io::Result<FileType> {\n  2584:         self.0.file_type().map(FileType)\n  2585:     }\n  2586: \n  2587:     /// Returns the file name of this directory entry without any\n  2588:     /// leading path component(s).\n  2589:     ///\n  2590:     /// As an example,\n  2591:     /// the output of the function will result in \"foo\" for all the following paths:\n  2592:     /// - \"./foo\"\n  2593:     /// - \"/the/foo\"",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirEntry::metadata",
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
      "name": "metadata",
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
            "id": 2885,
            "path": "DirEntry"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2912",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2885",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirEntry"
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
    "verification_source": "  2561:     ///\n  2562:     /// if let Ok(entries) = fs::read_dir(\".\") {\n  2563:     ///     for entry in entries {\n  2564:     ///         if let Ok(entry) = entry {\n  2565:     ///             // Here, `entry` is a `DirEntry`.\n  2566:     ///             if let Ok(metadata) = entry.metadata() {\n  2567:     ///                 // Now let's show our entry's permissions!\n  2568:     ///                 println!(\"{:?}: {:?}\", entry.path(), metadata.permissions());\n  2569:     ///             } else {\n  2570:     ///                 println!(\"Couldn't get metadata for {:?}\", entry.path());\n  2571:     ///             }\n  2572:     ///         }\n  2573:     ///     }\n  2574:     /// }\n  2575:     /// ```\n  2576:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2577:     pub fn metadata(&self) -> io::Result<Metadata> {\n  2578:         self.0.metadata().map(Metadata)\n  2579:     }\n  2580: \n  2581:     /// Returns the file type for the file that this entry points at.\n  2582:     ///\n  2583:     /// This function will not traverse symlinks if this entry points at a\n  2584:     /// symlink.\n  2585:     ///\n  2586:     /// # Platform-specific behavior\n  2587:     ///\n  2588:     /// On Windows and most Unix platforms this function is free (no extra\n  2589:     /// system calls needed), but some Unix platforms may require the equivalent\n  2590:     /// call to `symlink_metadata` to learn about the target file type.\n  2591:     ///\n  2592:     /// # Examples\n  2593:     ///",
    "nanvix_source": "  2538:     ///                 // Now let's show our entry's permissions!\n  2539:     ///                 println!(\"{:?}: {:?}\", entry.path(), metadata.permissions());\n  2540:     ///             } else {\n  2541:     ///                 println!(\"Couldn't get metadata for {:?}\", entry.path());\n  2542:     ///             }\n  2543:     ///         }\n  2544:     ///     }\n  2545:     /// }\n  2546:     /// ```\n  2547:     #[stable(feature = \"dir_entry_ext\", since = \"1.1.0\")]\n  2548:     pub fn metadata(&self) -> io::Result<Metadata> {\n  2549:         self.0.metadata().map(Metadata)\n  2550:     }\n  2551: \n  2552:     /// Returns the file type for the file that this entry points at.\n  2553:     ///\n  2554:     /// This function will not traverse symlinks if this entry points at a\n  2555:     /// symlink.\n  2556:     ///\n  2557:     /// # Platform-specific behavior\n  2558:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::DirEntry::path",
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
      "name": "path",
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
            "id": 2885,
            "path": "DirEntry"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2912",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2885",
        "resolved_owner_path": [
          "std",
          "fs",
          "DirEntry"
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
    "verification_source": "  2523:     ///     }\n  2524:     ///     Ok(())\n  2525:     /// }\n  2526:     /// ```\n  2527:     ///\n  2528:     /// This prints output like:\n  2529:     ///\n  2530:     /// ```text\n  2531:     /// \"./whatever.txt\"\n  2532:     /// \"./foo.html\"\n  2533:     /// \"./hello_world.rs\"\n  2534:     /// ```\n  2535:     ///\n  2536:     /// The exact text, of course, depends on what files you have in `.`.\n  2537:     #[must_use]\n  2538:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2539:     pub fn path(&self) -> PathBuf {\n  2540:         self.0.path()\n  2541:     }\n  2542: \n  2543:     /// Returns the metadata for the file that this entry points at.\n  2544:     ///\n  2545:     /// This function will not traverse symlinks if this entry points at a\n  2546:     /// symlink. To traverse symlinks use [`fs::metadata`] or [`fs::File::metadata`].\n  2547:     ///\n  2548:     /// [`fs::metadata`]: metadata\n  2549:     /// [`fs::File::metadata`]: File::metadata\n  2550:     ///\n  2551:     /// # Platform-specific behavior\n  2552:     ///\n  2553:     /// On Windows this function is cheap to call (no extra system calls\n  2554:     /// needed), but on Unix platforms this function is the equivalent of\n  2555:     /// calling `symlink_metadata` on the path.",
    "nanvix_source": "  2500:     ///\n  2501:     /// ```text\n  2502:     /// \"./whatever.txt\"\n  2503:     /// \"./foo.html\"\n  2504:     /// \"./hello_world.rs\"\n  2505:     /// ```\n  2506:     ///\n  2507:     /// The exact text, of course, depends on what files you have in `.`.\n  2508:     #[must_use]\n  2509:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2510:     pub fn path(&self) -> PathBuf {\n  2511:         self.0.path()\n  2512:     }\n  2513: \n  2514:     /// Returns the metadata for the file that this entry points at.\n  2515:     ///\n  2516:     /// This function will not traverse symlinks if this entry points at a\n  2517:     /// symlink. To traverse symlinks use [`fs::metadata`] or [`fs::File::metadata`].\n  2518:     ///\n  2519:     /// [`fs::metadata`]: metadata\n  2520:     /// [`fs::File::metadata`]: File::metadata",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::create",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
        ],
        "trait": null
      },
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
                        "id": 2556,
                        "path": "File"
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
    "verification_source": "   622:     /// See also [`std::fs::write()`][self::write] for a simple function to\n   623:     /// create a file with some given data.\n   624:     ///\n   625:     /// # Examples\n   626:     ///\n   627:     /// ```no_run\n   628:     /// use std::fs::File;\n   629:     /// use std::io::Write;\n   630:     ///\n   631:     /// fn main() -> std::io::Result<()> {\n   632:     ///     let mut f = File::create(\"foo.txt\")?;\n   633:     ///     f.write_all(&1234_u32.to_be_bytes())?;\n   634:     ///     Ok(())\n   635:     /// }\n   636:     /// ```\n   637:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   638:     pub fn create<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   639:         OpenOptions::new().write(true).create(true).truncate(true).open(path.as_ref())\n   640:     }\n   641: \n   642:     /// Opens a file in write-only mode with buffering.\n   643:     ///\n   644:     /// This function will create a file if it does not exist,\n   645:     /// and will truncate it if it does.\n   646:     ///\n   647:     /// Depending on the platform, this function may fail if the\n   648:     /// full directory path does not exist.\n   649:     ///\n   650:     /// See the [`OpenOptions::open`] method and the\n   651:     /// [`BufWriter`][io::BufWriter] type for more details.\n   652:     ///\n   653:     /// See also [`std::fs::write()`][self::write] for a simple function to\n   654:     /// create a file with some given data.",
    "nanvix_source": "   627:     /// use std::fs::File;\n   628:     /// use std::io::Write;\n   629:     ///\n   630:     /// fn main() -> std::io::Result<()> {\n   631:     ///     let mut f = File::create(\"foo.txt\")?;\n   632:     ///     f.write_all(&1234_u32.to_be_bytes())?;\n   633:     ///     Ok(())\n   634:     /// }\n   635:     /// ```\n   636:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   637:     pub fn create<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   638:         OpenOptions::new().write(true).create(true).truncate(true).open(path.as_ref())\n   639:     }\n   640: \n   641:     /// Opens a file in write-only mode with buffering.\n   642:     ///\n   643:     /// This function will create a file if it does not exist,\n   644:     /// and will truncate it if it does.\n   645:     ///\n   646:     /// Depending on the platform, this function may fail if the\n   647:     /// full directory path does not exist.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::create_new",
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
      "name": "create_new",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
        ],
        "trait": null
      },
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
                        "id": 2556,
                        "path": "File"
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
    "verification_source": "   696:     /// [`AlreadyExists`]: crate::io::ErrorKind::AlreadyExists\n   697:     /// [TOCTOU]: self#time-of-check-to-time-of-use-toctou\n   698:     ///\n   699:     /// # Examples\n   700:     ///\n   701:     /// ```no_run\n   702:     /// use std::fs::File;\n   703:     /// use std::io::Write;\n   704:     ///\n   705:     /// fn main() -> std::io::Result<()> {\n   706:     ///     let mut f = File::create_new(\"foo.txt\")?;\n   707:     ///     f.write_all(\"Hello, world!\".as_bytes())?;\n   708:     ///     Ok(())\n   709:     /// }\n   710:     /// ```\n   711:     #[stable(feature = \"file_create_new\", since = \"1.77.0\")]\n   712:     pub fn create_new<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   713:         OpenOptions::new().read(true).write(true).create_new(true).open(path.as_ref())\n   714:     }\n   715: \n   716:     /// Returns a new OpenOptions object.\n   717:     ///\n   718:     /// This function returns a new OpenOptions object that you can use to\n   719:     /// open or create a file with specific options if `open()` or `create()`\n   720:     /// are not appropriate.\n   721:     ///\n   722:     /// It is equivalent to `OpenOptions::new()`, but allows you to write more\n   723:     /// readable code. Instead of\n   724:     /// `OpenOptions::new().append(true).open(\"example.log\")`,\n   725:     /// you can write `File::options().append(true).open(\"example.log\")`. This\n   726:     /// also avoids the need to import `OpenOptions`.\n   727:     ///\n   728:     /// See the [`OpenOptions::new`] function for more details.",
    "nanvix_source": "   701:     /// use std::fs::File;\n   702:     /// use std::io::Write;\n   703:     ///\n   704:     /// fn main() -> std::io::Result<()> {\n   705:     ///     let mut f = File::create_new(\"foo.txt\")?;\n   706:     ///     f.write_all(\"Hello, world!\".as_bytes())?;\n   707:     ///     Ok(())\n   708:     /// }\n   709:     /// ```\n   710:     #[stable(feature = \"file_create_new\", since = \"1.77.0\")]\n   711:     pub fn create_new<P: AsRef<Path>>(path: P) -> io::Result<File> {\n   712:         OpenOptions::new().read(true).write(true).create_new(true).open(path.as_ref())\n   713:     }\n   714: \n   715:     /// Returns a new OpenOptions object.\n   716:     ///\n   717:     /// This function returns a new OpenOptions object that you can use to\n   718:     /// open or create a file with specific options if `open()` or `create()`\n   719:     /// are not appropriate.\n   720:     ///\n   721:     /// It is equivalent to `OpenOptions::new()`, but allows you to write more",
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
