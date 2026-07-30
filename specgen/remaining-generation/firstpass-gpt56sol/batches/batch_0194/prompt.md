For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::OpenOptions::truncate",
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
      "name": "truncate",
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
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "truncate",
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
    "verification_source": "  1789: \n  1790:     /// Sets the option for truncating a previous file.\n  1791:     ///\n  1792:     /// If a file is successfully opened with this option set to true, it will truncate\n  1793:     /// the file to 0 length if it already exists.\n  1794:     ///\n  1795:     /// The file must be opened with write access for truncate to work.\n  1796:     ///\n  1797:     /// # Examples\n  1798:     ///\n  1799:     /// ```no_run\n  1800:     /// use std::fs::OpenOptions;\n  1801:     ///\n  1802:     /// let file = OpenOptions::new().write(true).truncate(true).open(\"foo.txt\");\n  1803:     /// ```\n  1804:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1805:     pub fn truncate(&mut self, truncate: bool) -> &mut Self {\n  1806:         self.0.truncate(truncate);\n  1807:         self\n  1808:     }\n  1809: \n  1810:     /// Sets the option to create a new file, or open it if it already exists.\n  1811:     ///\n  1812:     /// In order for the file to be created, [`OpenOptions::write`] or\n  1813:     /// [`OpenOptions::append`] access must be used.\n  1814:     ///\n  1815:     /// See also [`std::fs::write()`][self::write] for a simple function to\n  1816:     /// create a file with some given data.\n  1817:     ///\n  1818:     /// # Errors\n  1819:     ///\n  1820:     /// If `.create(true)` is set without `.write(true)` or `.append(true)`,\n  1821:     /// calling [`open`](Self::open) will fail with [`InvalidInput`](io::ErrorKind::InvalidInput) error.",
    "nanvix_source": "  1764:     /// The file must be opened with write access for truncate to work.\n  1765:     ///\n  1766:     /// # Examples\n  1767:     ///\n  1768:     /// ```no_run\n  1769:     /// use std::fs::OpenOptions;\n  1770:     ///\n  1771:     /// let file = OpenOptions::new().write(true).truncate(true).open(\"foo.txt\");\n  1772:     /// ```\n  1773:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1774:     pub fn truncate(&mut self, truncate: bool) -> &mut Self {\n  1775:         self.0.truncate(truncate);\n  1776:         self\n  1777:     }\n  1778: \n  1779:     /// Sets the option to create a new file, or open it if it already exists.\n  1780:     ///\n  1781:     /// In order for the file to be created, [`OpenOptions::write`] or\n  1782:     /// [`OpenOptions::append`] access must be used.\n  1783:     ///\n  1784:     /// See also [`std::fs::write()`][self::write] for a simple function to",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::write",
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
      "name": "write",
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
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "write",
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
    "verification_source": "  1716:     /// Sets the option for write access.\n  1717:     ///\n  1718:     /// This option, when true, will indicate that the file should be\n  1719:     /// `write`-able if opened.\n  1720:     ///\n  1721:     /// If the file already exists, any write calls on it will overwrite its\n  1722:     /// contents, without truncating it.\n  1723:     ///\n  1724:     /// # Examples\n  1725:     ///\n  1726:     /// ```no_run\n  1727:     /// use std::fs::OpenOptions;\n  1728:     ///\n  1729:     /// let file = OpenOptions::new().write(true).open(\"foo.txt\");\n  1730:     /// ```\n  1731:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1732:     pub fn write(&mut self, write: bool) -> &mut Self {\n  1733:         self.0.write(write);\n  1734:         self\n  1735:     }\n  1736: \n  1737:     /// Sets the option for the append mode.\n  1738:     ///\n  1739:     /// This option, when true, means that writes will append to a file instead\n  1740:     /// of overwriting previous contents.\n  1741:     /// Note that setting `.write(true).append(true)` has the same effect as\n  1742:     /// setting only `.append(true)`.\n  1743:     ///\n  1744:     /// Append mode guarantees that writes will be positioned at the current end of file,\n  1745:     /// even when there are other processes or threads appending to the same file. This is\n  1746:     /// unlike <code>[seek]\\([SeekFrom]::[End]\\(0))</code> followed by `write()`, which\n  1747:     /// has a race between seeking and writing during which another writer can write, with\n  1748:     /// our `write()` overwriting their data.",
    "nanvix_source": "  1691:     /// contents, without truncating it.\n  1692:     ///\n  1693:     /// # Examples\n  1694:     ///\n  1695:     /// ```no_run\n  1696:     /// use std::fs::OpenOptions;\n  1697:     ///\n  1698:     /// let file = OpenOptions::new().write(true).open(\"foo.txt\");\n  1699:     /// ```\n  1700:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1701:     pub fn write(&mut self, write: bool) -> &mut Self {\n  1702:         self.0.write(write);\n  1703:         self\n  1704:     }\n  1705: \n  1706:     /// Sets the option for the append mode.\n  1707:     ///\n  1708:     /// This option, when true, means that writes will append to a file instead\n  1709:     /// of overwriting previous contents.\n  1710:     /// Note that setting `.write(true).append(true)` has the same effect as\n  1711:     /// setting only `.append(true)`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Permissions::readonly",
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
      "name": "readonly",
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
            "id": 2587,
            "path": "Permissions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3029",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2587",
        "resolved_owner_path": [
          "std",
          "fs",
          "Permissions"
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
    "verification_source": "  2282:     ///\n  2283:     /// # Examples\n  2284:     ///\n  2285:     /// ```no_run\n  2286:     /// use std::fs::File;\n  2287:     ///\n  2288:     /// fn main() -> std::io::Result<()> {\n  2289:     ///     let mut f = File::create(\"foo.txt\")?;\n  2290:     ///     let metadata = f.metadata()?;\n  2291:     ///\n  2292:     ///     assert_eq!(false, metadata.permissions().readonly());\n  2293:     ///     Ok(())\n  2294:     /// }\n  2295:     /// ```\n  2296:     #[must_use = \"call `set_readonly` to modify the readonly flag\"]\n  2297:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2298:     pub fn readonly(&self) -> bool {\n  2299:         self.0.readonly()\n  2300:     }\n  2301: \n  2302:     /// Modifies the readonly flag for this set of permissions. If the\n  2303:     /// `readonly` argument is `true`, using the resulting `Permission` will\n  2304:     /// update file permissions to forbid writing. Conversely, if it's `false`,\n  2305:     /// using the resulting `Permission` will update file permissions to allow\n  2306:     /// writing.\n  2307:     ///\n  2308:     /// This operation does **not** modify the files attributes. This only\n  2309:     /// changes the in-memory value of these attributes for this `Permissions`\n  2310:     /// instance. To modify the files attributes use the [`set_permissions`]\n  2311:     /// function which commits these attribute changes to the file.\n  2312:     ///\n  2313:     /// # Note\n  2314:     ///",
    "nanvix_source": "  2259:     /// fn main() -> std::io::Result<()> {\n  2260:     ///     let mut f = File::create(\"foo.txt\")?;\n  2261:     ///     let metadata = f.metadata()?;\n  2262:     ///\n  2263:     ///     assert_eq!(false, metadata.permissions().readonly());\n  2264:     ///     Ok(())\n  2265:     /// }\n  2266:     /// ```\n  2267:     #[must_use = \"call `set_readonly` to modify the readonly flag\"]\n  2268:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2269:     pub fn readonly(&self) -> bool {\n  2270:         self.0.readonly()\n  2271:     }\n  2272: \n  2273:     /// Modifies the readonly flag for this set of permissions. If the\n  2274:     /// `readonly` argument is `true`, using the resulting `Permission` will\n  2275:     /// update file permissions to forbid writing. Conversely, if it's `false`,\n  2276:     /// using the resulting `Permission` will update file permissions to allow\n  2277:     /// writing.\n  2278:     ///\n  2279:     /// This operation does **not** modify the files attributes. This only",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Permissions::set_readonly",
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
      "unit_return_variant"
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
      "name": "set_readonly",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 2587,
            "path": "Permissions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3029",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2587",
        "resolved_owner_path": [
          "std",
          "fs",
          "Permissions"
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
            "readonly",
            {
              "primitive": "bool"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2349:     ///     let f = File::create(\"foo.txt\")?;\n  2350:     ///     let metadata = f.metadata()?;\n  2351:     ///     let mut permissions = metadata.permissions();\n  2352:     ///\n  2353:     ///     permissions.set_readonly(true);\n  2354:     ///\n  2355:     ///     // filesystem doesn't change, only the in memory state of the\n  2356:     ///     // readonly permission\n  2357:     ///     assert_eq!(false, metadata.permissions().readonly());\n  2358:     ///\n  2359:     ///     // just this particular `permissions`.\n  2360:     ///     assert_eq!(true, permissions.readonly());\n  2361:     ///     Ok(())\n  2362:     /// }\n  2363:     /// ```\n  2364:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2365:     pub fn set_readonly(&mut self, readonly: bool) {\n  2366:         self.0.set_readonly(readonly)\n  2367:     }\n  2368: }\n  2369: \n  2370: impl FileType {\n  2371:     /// Tests whether this file type represents a directory. The\n  2372:     /// result is mutually exclusive to the results of\n  2373:     /// [`is_file`] and [`is_symlink`]; only zero or one of these\n  2374:     /// tests may pass.\n  2375:     ///\n  2376:     /// [`is_file`]: FileType::is_file\n  2377:     /// [`is_symlink`]: FileType::is_symlink\n  2378:     ///\n  2379:     /// # Examples\n  2380:     ///\n  2381:     /// ```no_run",
    "nanvix_source": "  2326:     ///     // filesystem doesn't change, only the in memory state of the\n  2327:     ///     // readonly permission\n  2328:     ///     assert_eq!(false, metadata.permissions().readonly());\n  2329:     ///\n  2330:     ///     // just this particular `permissions`.\n  2331:     ///     assert_eq!(true, permissions.readonly());\n  2332:     ///     Ok(())\n  2333:     /// }\n  2334:     /// ```\n  2335:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2336:     pub fn set_readonly(&mut self, readonly: bool) {\n  2337:         self.0.set_readonly(readonly)\n  2338:     }\n  2339: }\n  2340: \n  2341: impl FileType {\n  2342:     /// Tests whether this file type represents a directory. The\n  2343:     /// result is mutually exclusive to the results of\n  2344:     /// [`is_file`] and [`is_symlink`]; only zero or one of these\n  2345:     /// tests may pass.\n  2346:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::canonicalize",
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
      "name": "canonicalize",
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
    "verification_source": "  3021: /// * `path` does not exist.\n  3022: /// * A non-final component in path is not a directory.\n  3023: ///\n  3024: /// # Examples\n  3025: ///\n  3026: /// ```no_run\n  3027: /// use std::fs;\n  3028: ///\n  3029: /// fn main() -> std::io::Result<()> {\n  3030: ///     let path = fs::canonicalize(\"../a/../foo.txt\")?;\n  3031: ///     Ok(())\n  3032: /// }\n  3033: /// ```\n  3034: #[doc(alias = \"realpath\")]\n  3035: #[doc(alias = \"GetFinalPathNameByHandle\")]\n  3036: #[stable(feature = \"fs_canonicalize\", since = \"1.5.0\")]\n  3037: pub fn canonicalize<P: AsRef<Path>>(path: P) -> io::Result<PathBuf> {\n  3038:     fs_imp::canonicalize(path.as_ref())\n  3039: }\n  3040: \n  3041: /// Creates a new, empty directory at the provided path.\n  3042: ///\n  3043: /// # Platform-specific behavior\n  3044: ///\n  3045: /// This function currently corresponds to the `mkdir` function on Unix\n  3046: /// and the `CreateDirectoryW` function on Windows.\n  3047: /// Note that, this [may change in the future][changes].\n  3048: ///\n  3049: /// [changes]: io#platform-specific-behavior\n  3050: ///\n  3051: /// **NOTE**: If a parent of the given path doesn't exist, this function will\n  3052: /// return an error. To create a directory and all its missing parents at the\n  3053: /// same time, use the [`create_dir_all`] function.",
    "nanvix_source": "  3001: /// use std::fs;\n  3002: ///\n  3003: /// fn main() -> std::io::Result<()> {\n  3004: ///     let path = fs::canonicalize(\"../a/../foo.txt\")?;\n  3005: ///     Ok(())\n  3006: /// }\n  3007: /// ```\n  3008: #[doc(alias = \"realpath\")]\n  3009: #[doc(alias = \"GetFinalPathNameByHandle\")]\n  3010: #[stable(feature = \"fs_canonicalize\", since = \"1.5.0\")]\n  3011: pub fn canonicalize<P: AsRef<Path>>(path: P) -> io::Result<PathBuf> {\n  3012:     fs_imp::canonicalize(path.as_ref())\n  3013: }\n  3014: \n  3015: /// Creates a new, empty directory at the provided path.\n  3016: ///\n  3017: /// # Platform-specific behavior\n  3018: ///\n  3019: /// This function currently corresponds to the `mkdir` function on Unix\n  3020: /// and the `CreateDirectoryW` function on Windows.\n  3021: /// Note that, this [may change in the future][changes].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::copy",
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
            "name": "Q"
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
      "name": "copy",
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
            "from",
            {
              "generic": "P"
            }
          ],
          [
            "to",
            {
              "generic": "Q"
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
                      "primitive": "u64"
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
    "verification_source": "  2866: /// * The parent directory of `to` doesn't exist.\n  2867: ///\n  2868: /// # Examples\n  2869: ///\n  2870: /// ```no_run\n  2871: /// use std::fs;\n  2872: ///\n  2873: /// fn main() -> std::io::Result<()> {\n  2874: ///     fs::copy(\"foo.txt\", \"bar.txt\")?;  // Copy foo.txt to bar.txt\n  2875: ///     Ok(())\n  2876: /// }\n  2877: /// ```\n  2878: #[doc(alias = \"cp\")]\n  2879: #[doc(alias = \"CopyFile\", alias = \"CopyFileEx\")]\n  2880: #[doc(alias = \"fclonefileat\", alias = \"fcopyfile\")]\n  2881: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2882: pub fn copy<P: AsRef<Path>, Q: AsRef<Path>>(from: P, to: Q) -> io::Result<u64> {\n  2883:     fs_imp::copy(from.as_ref(), to.as_ref())\n  2884: }\n  2885: \n  2886: /// Creates a new hard link on the filesystem.\n  2887: ///\n  2888: /// The `link` path will be a link pointing to the `original` path. Note that\n  2889: /// systems often require these two paths to both be located on the same\n  2890: /// filesystem.\n  2891: ///\n  2892: /// If `original` names a symbolic link, it is platform-specific whether the\n  2893: /// symbolic link is followed. On platforms where it's possible to not follow\n  2894: /// it, it is not followed, and the created hard link points to the symbolic\n  2895: /// link itself.\n  2896: ///\n  2897: /// # Platform-specific behavior\n  2898: ///",
    "nanvix_source": "  2846: ///\n  2847: /// fn main() -> std::io::Result<()> {\n  2848: ///     fs::copy(\"foo.txt\", \"bar.txt\")?;  // Copy foo.txt to bar.txt\n  2849: ///     Ok(())\n  2850: /// }\n  2851: /// ```\n  2852: #[doc(alias = \"cp\")]\n  2853: #[doc(alias = \"CopyFile\", alias = \"CopyFileEx\")]\n  2854: #[doc(alias = \"fclonefileat\", alias = \"fcopyfile\")]\n  2855: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2856: pub fn copy<P: AsRef<Path>, Q: AsRef<Path>>(from: P, to: Q) -> io::Result<u64> {\n  2857:     fs_imp::copy(from.as_ref(), to.as_ref())\n  2858: }\n  2859: \n  2860: /// Creates a new hard link on the filesystem.\n  2861: ///\n  2862: /// The `link` path will be a link pointing to the `original` path. Note that\n  2863: /// systems often require these two paths to both be located on the same\n  2864: /// filesystem.\n  2865: ///\n  2866: /// If `original` names a symbolic link, it is platform-specific whether the",
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
