For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::join",
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
      "name": "join",
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
            "path",
            {
              "generic": "P"
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
    "verification_source": "  3040:     /// * if `self` has a verbatim prefix (e.g. `\\\\?\\C:\\windows`)\n  3041:     ///   and `path` is not empty, the new path is normalized: all references\n  3042:     ///   to `.` and `..` are removed.\n  3043:     ///\n  3044:     /// See [`PathBuf::push`] for more details on what it means to adjoin a path.\n  3045:     ///\n  3046:     /// # Examples\n  3047:     ///\n  3048:     /// ```\n  3049:     /// use std::path::{Path, PathBuf};\n  3050:     ///\n  3051:     /// assert_eq!(Path::new(\"/etc\").join(\"passwd\"), PathBuf::from(\"/etc/passwd\"));\n  3052:     /// assert_eq!(Path::new(\"/etc\").join(\"/bin/sh\"), PathBuf::from(\"/bin/sh\"));\n  3053:     /// ```\n  3054:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3055:     #[must_use]\n  3056:     pub fn join<P: AsRef<Path>>(&self, path: P) -> PathBuf {\n  3057:         self._join(path.as_ref())\n  3058:     }\n  3059: \n  3060:     fn _join(&self, path: &Path) -> PathBuf {\n  3061:         let mut buf = self.to_path_buf();\n  3062:         buf.push(path);\n  3063:         buf\n  3064:     }\n  3065: \n  3066:     /// Creates an owned [`PathBuf`] like `self` but with the given file name.\n  3067:     ///\n  3068:     /// See [`PathBuf::set_file_name`] for more details.\n  3069:     ///\n  3070:     /// # Examples\n  3071:     ///\n  3072:     /// ```",
    "nanvix_source": "  3067:     /// # Examples\n  3068:     ///\n  3069:     /// ```\n  3070:     /// use std::path::{Path, PathBuf};\n  3071:     ///\n  3072:     /// assert_eq!(Path::new(\"/etc\").join(\"passwd\"), PathBuf::from(\"/etc/passwd\"));\n  3073:     /// assert_eq!(Path::new(\"/etc\").join(\"/bin/sh\"), PathBuf::from(\"/bin/sh\"));\n  3074:     /// ```\n  3075:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3076:     #[must_use]\n  3077:     pub fn join<P: AsRef<Path>>(&self, path: P) -> PathBuf {\n  3078:         self._join(path.as_ref())\n  3079:     }\n  3080: \n  3081:     fn _join(&self, path: &Path) -> PathBuf {\n  3082:         let mut buf = self.to_path_buf();\n  3083:         buf.push(path);\n  3084:         buf\n  3085:     }\n  3086: \n  3087:     /// Creates an owned [`PathBuf`] like `self` but with the given file name.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::metadata",
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
    "verification_source": "  3291:     /// This function will traverse symbolic links to query information about the\n  3292:     /// destination file.\n  3293:     ///\n  3294:     /// This is an alias to [`fs::metadata`].\n  3295:     ///\n  3296:     /// # Examples\n  3297:     ///\n  3298:     /// ```no_run\n  3299:     /// use std::path::Path;\n  3300:     ///\n  3301:     /// let path = Path::new(\"/Minas/tirith\");\n  3302:     /// let metadata = path.metadata().expect(\"metadata call failed\");\n  3303:     /// println!(\"{:?}\", metadata.file_type());\n  3304:     /// ```\n  3305:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3306:     #[inline]\n  3307:     pub fn metadata(&self) -> io::Result<fs::Metadata> {\n  3308:         fs::metadata(self)\n  3309:     }\n  3310: \n  3311:     /// Queries the metadata about a file without following symlinks.\n  3312:     ///\n  3313:     /// This is an alias to [`fs::symlink_metadata`].\n  3314:     ///\n  3315:     /// # Examples\n  3316:     ///\n  3317:     /// ```no_run\n  3318:     /// use std::path::Path;\n  3319:     ///\n  3320:     /// let path = Path::new(\"/Minas/tirith\");\n  3321:     /// let metadata = path.symlink_metadata().expect(\"symlink_metadata call failed\");\n  3322:     /// println!(\"{:?}\", metadata.file_type());\n  3323:     /// ```",
    "nanvix_source": "  3327:     ///\n  3328:     /// ```no_run\n  3329:     /// use std::path::Path;\n  3330:     ///\n  3331:     /// let path = Path::new(\"/Minas/tirith\");\n  3332:     /// let metadata = path.metadata().expect(\"metadata call failed\");\n  3333:     /// println!(\"{:?}\", metadata.file_type());\n  3334:     /// ```\n  3335:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3336:     #[inline]\n  3337:     pub fn metadata(&self) -> io::Result<fs::Metadata> {\n  3338:         fs::metadata(self)\n  3339:     }\n  3340: \n  3341:     /// Queries the metadata about a file without following symlinks.\n  3342:     ///\n  3343:     /// This is an alias to [`fs::symlink_metadata`].\n  3344:     ///\n  3345:     /// # Examples\n  3346:     ///\n  3347:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::new",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe_const",
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
            "name": "S"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
            "s",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "S"
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
    "verification_source": "  2378:     ///\n  2379:     /// Path::new(\"foo.txt\");\n  2380:     /// ```\n  2381:     ///\n  2382:     /// You can create `Path`s from `String`s, or even other `Path`s:\n  2383:     ///\n  2384:     /// ```\n  2385:     /// use std::path::Path;\n  2386:     ///\n  2387:     /// let string = String::from(\"foo.txt\");\n  2388:     /// let from_string = Path::new(&string);\n  2389:     /// let from_path = Path::new(&from_string);\n  2390:     /// assert_eq!(from_string, from_path);\n  2391:     /// ```\n  2392:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2393:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  2394:     pub const fn new<S: [const] AsRef<OsStr> + ?Sized>(s: &S) -> &Path {\n  2395:         unsafe { &*(s.as_ref() as *const OsStr as *const Path) }\n  2396:     }\n  2397: \n  2398:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  2399:     const fn from_inner_mut(inner: &mut OsStr) -> &mut Path {\n  2400:         // SAFETY: Path is just a wrapper around OsStr,\n  2401:         // therefore converting &mut OsStr to &mut Path is safe.\n  2402:         unsafe { &mut *(inner as *mut OsStr as *mut Path) }\n  2403:     }\n  2404: \n  2405:     /// Yields the underlying [`OsStr`] slice.\n  2406:     ///\n  2407:     /// # Examples\n  2408:     ///\n  2409:     /// ```\n  2410:     /// use std::path::Path;",
    "nanvix_source": "  2402:     /// ```\n  2403:     /// use std::path::Path;\n  2404:     ///\n  2405:     /// let string = String::from(\"foo.txt\");\n  2406:     /// let from_string = Path::new(&string);\n  2407:     /// let from_path = Path::new(&from_string);\n  2408:     /// assert_eq!(from_string, from_path);\n  2409:     /// ```\n  2410:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2411:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  2412:     pub const fn new<S: [const] AsRef<OsStr> + ?Sized>(s: &S) -> &Path {\n  2413:         unsafe { &*(s.as_ref() as *const OsStr as *const Path) }\n  2414:     }\n  2415: \n  2416:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  2417:     const fn from_inner_mut(inner: &mut OsStr) -> &mut Path {\n  2418:         // SAFETY: Path is just a wrapper around OsStr,\n  2419:         // therefore converting &mut OsStr to &mut Path is safe.\n  2420:         unsafe { &mut *(inner as *mut OsStr as *mut Path) }\n  2421:     }\n  2422: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::parent",
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
      "name": "parent",
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
    "verification_source": "  2601:     ///\n  2602:     /// let grand_parent = parent.parent().unwrap();\n  2603:     /// assert_eq!(grand_parent, Path::new(\"/\"));\n  2604:     /// assert_eq!(grand_parent.parent(), None);\n  2605:     ///\n  2606:     /// let relative_path = Path::new(\"foo/bar\");\n  2607:     /// let parent = relative_path.parent();\n  2608:     /// assert_eq!(parent, Some(Path::new(\"foo\")));\n  2609:     /// let grand_parent = parent.and_then(Path::parent);\n  2610:     /// assert_eq!(grand_parent, Some(Path::new(\"\")));\n  2611:     /// let great_grand_parent = grand_parent.and_then(Path::parent);\n  2612:     /// assert_eq!(great_grand_parent, None);\n  2613:     /// ```\n  2614:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2615:     #[doc(alias = \"dirname\")]\n  2616:     #[must_use]\n  2617:     pub fn parent(&self) -> Option<&Path> {\n  2618:         let mut comps = self.components();\n  2619:         let comp = comps.next_back();\n  2620:         comp.and_then(|p| match p {\n  2621:             Component::Normal(_) | Component::CurDir | Component::ParentDir => {\n  2622:                 Some(comps.as_path())\n  2623:             }\n  2624:             _ => None,\n  2625:         })\n  2626:     }\n  2627: \n  2628:     /// Produces an iterator over `Path` and its ancestors.\n  2629:     ///\n  2630:     /// The iterator will yield the `Path` that is returned if the [`parent`] method is used zero\n  2631:     /// or more times. If the [`parent`] method returns [`None`], the iterator will do likewise.\n  2632:     /// The iterator will always yield at least one value, namely `Some(&self)`. Next it will yield\n  2633:     /// `&self.parent()`, `&self.parent().and_then(Path::parent)` and so on.",
    "nanvix_source": "  2625:     /// let parent = relative_path.parent();\n  2626:     /// assert_eq!(parent, Some(Path::new(\"foo\")));\n  2627:     /// let grand_parent = parent.and_then(Path::parent);\n  2628:     /// assert_eq!(grand_parent, Some(Path::new(\"\")));\n  2629:     /// let great_grand_parent = grand_parent.and_then(Path::parent);\n  2630:     /// assert_eq!(great_grand_parent, None);\n  2631:     /// ```\n  2632:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2633:     #[doc(alias = \"dirname\")]\n  2634:     #[must_use]\n  2635:     pub fn parent(&self) -> Option<&Path> {\n  2636:         let mut comps = self.components();\n  2637:         let comp = comps.next_back();\n  2638:         comp.and_then(|p| match p {\n  2639:             Component::Normal(_) | Component::CurDir | Component::ParentDir => {\n  2640:                 Some(comps.as_path())\n  2641:             }\n  2642:             _ => None,\n  2643:         })\n  2644:     }\n  2645: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::read_dir",
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
      "name": "read_dir",
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
                        "id": 2886,
                        "path": "fs::ReadDir"
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
    "verification_source": "  3469:     /// This is an alias to [`fs::read_dir`].\n  3470:     ///\n  3471:     /// # Examples\n  3472:     ///\n  3473:     /// ```no_run\n  3474:     /// use std::path::Path;\n  3475:     ///\n  3476:     /// let path = Path::new(\"/laputa\");\n  3477:     /// for entry in path.read_dir().expect(\"read_dir call failed\") {\n  3478:     ///     if let Ok(entry) = entry {\n  3479:     ///         println!(\"{:?}\", entry.path());\n  3480:     ///     }\n  3481:     /// }\n  3482:     /// ```\n  3483:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3484:     #[inline]\n  3485:     pub fn read_dir(&self) -> io::Result<fs::ReadDir> {\n  3486:         fs::read_dir(self)\n  3487:     }\n  3488: \n  3489:     /// Returns `true` if the path points at an existing entity.\n  3490:     ///\n  3491:     /// Warning: this method may be error-prone, consider using [`try_exists()`] instead!\n  3492:     /// It also has a risk of introducing time-of-check to time-of-use ([TOCTOU]) bugs.\n  3493:     ///\n  3494:     /// This function will traverse symbolic links to query information about the\n  3495:     /// destination file.\n  3496:     ///\n  3497:     /// If you cannot access the metadata of the file, e.g. because of a\n  3498:     /// permission error or broken symbolic links, this will return `false`.\n  3499:     ///\n  3500:     /// # Examples\n  3501:     ///",
    "nanvix_source": "  3505:     ///\n  3506:     /// let path = Path::new(\"/laputa\");\n  3507:     /// for entry in path.read_dir().expect(\"read_dir call failed\") {\n  3508:     ///     if let Ok(entry) = entry {\n  3509:     ///         println!(\"{:?}\", entry.path());\n  3510:     ///     }\n  3511:     /// }\n  3512:     /// ```\n  3513:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3514:     #[inline]\n  3515:     pub fn read_dir(&self) -> io::Result<fs::ReadDir> {\n  3516:         fs::read_dir(self)\n  3517:     }\n  3518: \n  3519:     /// Returns `true` if the path points at an existing entity.\n  3520:     ///\n  3521:     /// Warning: this method may be error-prone, consider using [`try_exists()`] instead!\n  3522:     /// It also has a risk of introducing time-of-check to time-of-use ([TOCTOU]) bugs.\n  3523:     ///\n  3524:     /// This function will traverse symbolic links to query information about the\n  3525:     /// destination file.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::read_link",
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
      "name": "read_link",
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
                        "id": 1799,
                        "path": "PathBuf"
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
    "verification_source": "  3444:     }\n  3445: \n  3446:     /// Reads a symbolic link, returning the file that the link points to.\n  3447:     ///\n  3448:     /// This is an alias to [`fs::read_link`].\n  3449:     ///\n  3450:     /// # Examples\n  3451:     ///\n  3452:     /// ```no_run\n  3453:     /// use std::path::Path;\n  3454:     ///\n  3455:     /// let path = Path::new(\"/laputa/sky_castle.rs\");\n  3456:     /// let path_link = path.read_link().expect(\"read_link call failed\");\n  3457:     /// ```\n  3458:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3459:     #[inline]\n  3460:     pub fn read_link(&self) -> io::Result<PathBuf> {\n  3461:         fs::read_link(self)\n  3462:     }\n  3463: \n  3464:     /// Returns an iterator over the entries within a directory.\n  3465:     ///\n  3466:     /// The iterator will yield instances of <code>[io::Result]<[fs::DirEntry]></code>. New\n  3467:     /// errors may be encountered after an iterator is initially constructed.\n  3468:     ///\n  3469:     /// This is an alias to [`fs::read_dir`].\n  3470:     ///\n  3471:     /// # Examples\n  3472:     ///\n  3473:     /// ```no_run\n  3474:     /// use std::path::Path;\n  3475:     ///\n  3476:     /// let path = Path::new(\"/laputa\");",
    "nanvix_source": "  3480:     /// # Examples\n  3481:     ///\n  3482:     /// ```no_run\n  3483:     /// use std::path::Path;\n  3484:     ///\n  3485:     /// let path = Path::new(\"/laputa/sky_castle.rs\");\n  3486:     /// let path_link = path.read_link().expect(\"read_link call failed\");\n  3487:     /// ```\n  3488:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3489:     #[inline]\n  3490:     pub fn read_link(&self) -> io::Result<PathBuf> {\n  3491:         fs::read_link(self)\n  3492:     }\n  3493: \n  3494:     /// Returns an iterator over the entries within a directory.\n  3495:     ///\n  3496:     /// The iterator will yield instances of <code>[io::Result]<[fs::DirEntry]></code>. New\n  3497:     /// errors may be encountered after an iterator is initially constructed.\n  3498:     ///\n  3499:     /// This is an alias to [`fs::read_dir`].\n  3500:     ///",
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
