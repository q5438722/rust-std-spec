For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::FileType::is_dir",
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
            "id": 2774,
            "path": "FileType"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3062",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2774",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileType"
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
    "verification_source": "  2378:     ///\n  2379:     /// # Examples\n  2380:     ///\n  2381:     /// ```no_run\n  2382:     /// fn main() -> std::io::Result<()> {\n  2383:     ///     use std::fs;\n  2384:     ///\n  2385:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2386:     ///     let file_type = metadata.file_type();\n  2387:     ///\n  2388:     ///     assert_eq!(file_type.is_dir(), false);\n  2389:     ///     Ok(())\n  2390:     /// }\n  2391:     /// ```\n  2392:     #[must_use]\n  2393:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2394:     pub fn is_dir(&self) -> bool {\n  2395:         self.0.is_dir()\n  2396:     }\n  2397: \n  2398:     /// Tests whether this file type represents a regular file.\n  2399:     /// The result is mutually exclusive to the results of\n  2400:     /// [`is_dir`] and [`is_symlink`]; only zero or one of these\n  2401:     /// tests may pass.\n  2402:     ///\n  2403:     /// When the goal is simply to read from (or write to) the source, the most\n  2404:     /// reliable way to test the source can be read (or written to) is to open\n  2405:     /// it. Only using `is_file` can break workflows like `diff <( prog_a )` on\n  2406:     /// a Unix-like system for example. See [`File::open`] or\n  2407:     /// [`OpenOptions::open`] for more information.\n  2408:     ///\n  2409:     /// [`is_dir`]: FileType::is_dir\n  2410:     /// [`is_symlink`]: FileType::is_symlink",
    "nanvix_source": "  2355:     ///\n  2356:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2357:     ///     let file_type = metadata.file_type();\n  2358:     ///\n  2359:     ///     assert_eq!(file_type.is_dir(), false);\n  2360:     ///     Ok(())\n  2361:     /// }\n  2362:     /// ```\n  2363:     #[must_use]\n  2364:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2365:     pub fn is_dir(&self) -> bool {\n  2366:         self.0.is_dir()\n  2367:     }\n  2368: \n  2369:     /// Tests whether this file type represents a regular file.\n  2370:     /// The result is mutually exclusive to the results of\n  2371:     /// [`is_dir`] and [`is_symlink`]; only zero or one of these\n  2372:     /// tests may pass.\n  2373:     ///\n  2374:     /// When the goal is simply to read from (or write to) the source, the most\n  2375:     /// reliable way to test the source can be read (or written to) is to open",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::FileType::is_file",
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
            "id": 2774,
            "path": "FileType"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3062",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2774",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileType"
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
    "verification_source": "  2411:     ///\n  2412:     /// # Examples\n  2413:     ///\n  2414:     /// ```no_run\n  2415:     /// fn main() -> std::io::Result<()> {\n  2416:     ///     use std::fs;\n  2417:     ///\n  2418:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2419:     ///     let file_type = metadata.file_type();\n  2420:     ///\n  2421:     ///     assert_eq!(file_type.is_file(), true);\n  2422:     ///     Ok(())\n  2423:     /// }\n  2424:     /// ```\n  2425:     #[must_use]\n  2426:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2427:     pub fn is_file(&self) -> bool {\n  2428:         self.0.is_file()\n  2429:     }\n  2430: \n  2431:     /// Tests whether this file type represents a symbolic link.\n  2432:     /// The result is mutually exclusive to the results of\n  2433:     /// [`is_dir`] and [`is_file`]; only zero or one of these\n  2434:     /// tests may pass.\n  2435:     ///\n  2436:     /// The underlying [`Metadata`] struct needs to be retrieved\n  2437:     /// with the [`fs::symlink_metadata`] function and not the\n  2438:     /// [`fs::metadata`] function. The [`fs::metadata`] function\n  2439:     /// follows symbolic links, so [`is_symlink`] would always\n  2440:     /// return `false` for the target file.\n  2441:     ///\n  2442:     /// [`fs::metadata`]: metadata\n  2443:     /// [`fs::symlink_metadata`]: symlink_metadata",
    "nanvix_source": "  2388:     ///\n  2389:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2390:     ///     let file_type = metadata.file_type();\n  2391:     ///\n  2392:     ///     assert_eq!(file_type.is_file(), true);\n  2393:     ///     Ok(())\n  2394:     /// }\n  2395:     /// ```\n  2396:     #[must_use]\n  2397:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2398:     pub fn is_file(&self) -> bool {\n  2399:         self.0.is_file()\n  2400:     }\n  2401: \n  2402:     /// Tests whether this file type represents a symbolic link.\n  2403:     /// The result is mutually exclusive to the results of\n  2404:     /// [`is_dir`] and [`is_file`]; only zero or one of these\n  2405:     /// tests may pass.\n  2406:     ///\n  2407:     /// The underlying [`Metadata`] struct needs to be retrieved\n  2408:     /// with the [`fs::symlink_metadata`] function and not the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::FileType::is_symlink",
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
            "id": 2774,
            "path": "FileType"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:3062",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2774",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileType"
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
    "verification_source": "  2447:     ///\n  2448:     /// # Examples\n  2449:     ///\n  2450:     /// ```no_run\n  2451:     /// use std::fs;\n  2452:     ///\n  2453:     /// fn main() -> std::io::Result<()> {\n  2454:     ///     let metadata = fs::symlink_metadata(\"foo.txt\")?;\n  2455:     ///     let file_type = metadata.file_type();\n  2456:     ///\n  2457:     ///     assert_eq!(file_type.is_symlink(), false);\n  2458:     ///     Ok(())\n  2459:     /// }\n  2460:     /// ```\n  2461:     #[must_use]\n  2462:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2463:     pub fn is_symlink(&self) -> bool {\n  2464:         self.0.is_symlink()\n  2465:     }\n  2466: }\n  2467: \n  2468: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n  2469: impl fmt::Debug for FileType {\n  2470:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2471:         f.debug_struct(\"FileType\")\n  2472:             .field(\"is_file\", &self.is_file())\n  2473:             .field(\"is_dir\", &self.is_dir())\n  2474:             .field(\"is_symlink\", &self.is_symlink())\n  2475:             .finish_non_exhaustive()\n  2476:     }\n  2477: }\n  2478: \n  2479: impl AsInner<fs_imp::FileType> for FileType {",
    "nanvix_source": "  2424:     /// fn main() -> std::io::Result<()> {\n  2425:     ///     let metadata = fs::symlink_metadata(\"foo.txt\")?;\n  2426:     ///     let file_type = metadata.file_type();\n  2427:     ///\n  2428:     ///     assert_eq!(file_type.is_symlink(), false);\n  2429:     ///     Ok(())\n  2430:     /// }\n  2431:     /// ```\n  2432:     #[must_use]\n  2433:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  2434:     pub fn is_symlink(&self) -> bool {\n  2435:         self.0.is_symlink()\n  2436:     }\n  2437: }\n  2438: \n  2439: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n  2440: impl fmt::Debug for FileType {\n  2441:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2442:         f.debug_struct(\"FileType\")\n  2443:             .field(\"is_file\", &self.is_file())\n  2444:             .field(\"is_dir\", &self.is_dir())",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::accessed",
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
      "name": "accessed",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
                        "id": 2591,
                        "path": "SystemTime"
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
    "verification_source": "  2127:     /// ```no_run\n  2128:     /// use std::fs;\n  2129:     ///\n  2130:     /// fn main() -> std::io::Result<()> {\n  2131:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2132:     ///\n  2133:     ///     if let Ok(time) = metadata.accessed() {\n  2134:     ///         println!(\"{time:?}\");\n  2135:     ///     } else {\n  2136:     ///         println!(\"Not supported on this platform\");\n  2137:     ///     }\n  2138:     ///     Ok(())\n  2139:     /// }\n  2140:     /// ```\n  2141:     #[doc(alias = \"atime\", alias = \"ftLastAccessTime\")]\n  2142:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2143:     pub fn accessed(&self) -> io::Result<SystemTime> {\n  2144:         self.0.accessed().map(FromInner::from_inner)\n  2145:     }\n  2146: \n  2147:     /// Returns the creation time listed in this metadata.\n  2148:     ///\n  2149:     /// The returned value corresponds to the `btime` field of `statx` on\n  2150:     /// Linux kernel starting from to 4.11, the `birthtime` field of `stat` on other\n  2151:     /// Unix platforms, and the `ftCreationTime` field on Windows platforms.\n  2152:     ///\n  2153:     /// # Errors\n  2154:     ///\n  2155:     /// This field might not be available on all platforms, and will return an\n  2156:     /// `Err` on platforms or filesystems where it is not available.\n  2157:     ///\n  2158:     /// # Examples\n  2159:     ///",
    "nanvix_source": "  2102:     ///     if let Ok(time) = metadata.accessed() {\n  2103:     ///         println!(\"{time:?}\");\n  2104:     ///     } else {\n  2105:     ///         println!(\"Not supported on this platform\");\n  2106:     ///     }\n  2107:     ///     Ok(())\n  2108:     /// }\n  2109:     /// ```\n  2110:     #[doc(alias = \"atime\", alias = \"ftLastAccessTime\")]\n  2111:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2112:     pub fn accessed(&self) -> io::Result<SystemTime> {\n  2113:         self.0.accessed().map(FromInner::from_inner)\n  2114:     }\n  2115: \n  2116:     /// Returns the creation time listed in this metadata.\n  2117:     ///\n  2118:     /// The returned value corresponds to the `btime` field of `statx` on\n  2119:     /// Linux kernel starting from to 4.11, the `birthtime` field of `stat` on other\n  2120:     /// Unix platforms, and the `ftCreationTime` field on Windows platforms.\n  2121:     ///\n  2122:     /// # Errors",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::created",
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
      "name": "created",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
                        "id": 2591,
                        "path": "SystemTime"
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
    "verification_source": "  2160:     /// ```no_run\n  2161:     /// use std::fs;\n  2162:     ///\n  2163:     /// fn main() -> std::io::Result<()> {\n  2164:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2165:     ///\n  2166:     ///     if let Ok(time) = metadata.created() {\n  2167:     ///         println!(\"{time:?}\");\n  2168:     ///     } else {\n  2169:     ///         println!(\"Not supported on this platform or filesystem\");\n  2170:     ///     }\n  2171:     ///     Ok(())\n  2172:     /// }\n  2173:     /// ```\n  2174:     #[doc(alias = \"btime\", alias = \"birthtime\", alias = \"ftCreationTime\")]\n  2175:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2176:     pub fn created(&self) -> io::Result<SystemTime> {\n  2177:         self.0.created().map(FromInner::from_inner)\n  2178:     }\n  2179: }\n  2180: \n  2181: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n  2182: impl fmt::Debug for Metadata {\n  2183:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2184:         let mut debug = f.debug_struct(\"Metadata\");\n  2185:         debug.field(\"file_type\", &self.file_type());\n  2186:         debug.field(\"permissions\", &self.permissions());\n  2187:         debug.field(\"len\", &self.len());\n  2188:         if let Ok(modified) = self.modified() {\n  2189:             debug.field(\"modified\", &modified);\n  2190:         }\n  2191:         if let Ok(accessed) = self.accessed() {\n  2192:             debug.field(\"accessed\", &accessed);",
    "nanvix_source": "  2135:     ///     if let Ok(time) = metadata.created() {\n  2136:     ///         println!(\"{time:?}\");\n  2137:     ///     } else {\n  2138:     ///         println!(\"Not supported on this platform or filesystem\");\n  2139:     ///     }\n  2140:     ///     Ok(())\n  2141:     /// }\n  2142:     /// ```\n  2143:     #[doc(alias = \"btime\", alias = \"birthtime\", alias = \"ftCreationTime\")]\n  2144:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2145:     pub fn created(&self) -> io::Result<SystemTime> {\n  2146:         self.0.created().map(FromInner::from_inner)\n  2147:     }\n  2148: }\n  2149: \n  2150: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n  2151: impl fmt::Debug for Metadata {\n  2152:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2153:         let mut debug = f.debug_struct(\"Metadata\");\n  2154:         debug.field(\"file_type\", &self.file_type());\n  2155:         debug.field(\"permissions\", &self.permissions());",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::file_type",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
            "id": 2774,
            "path": "FileType"
          }
        }
      }
    },
    "verification_source": "  1941:     /// Returns the file type for this metadata.\n  1942:     ///\n  1943:     /// # Examples\n  1944:     ///\n  1945:     /// ```no_run\n  1946:     /// fn main() -> std::io::Result<()> {\n  1947:     ///     use std::fs;\n  1948:     ///\n  1949:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1950:     ///\n  1951:     ///     println!(\"{:?}\", metadata.file_type());\n  1952:     ///     Ok(())\n  1953:     /// }\n  1954:     /// ```\n  1955:     #[must_use]\n  1956:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  1957:     pub fn file_type(&self) -> FileType {\n  1958:         FileType(self.0.file_type())\n  1959:     }\n  1960: \n  1961:     /// Returns `true` if this metadata is for a directory. The\n  1962:     /// result is mutually exclusive to the result of\n  1963:     /// [`Metadata::is_file`], and will be false for symlink metadata\n  1964:     /// obtained from [`symlink_metadata`].\n  1965:     ///\n  1966:     /// # Examples\n  1967:     ///\n  1968:     /// ```no_run\n  1969:     /// fn main() -> std::io::Result<()> {\n  1970:     ///     use std::fs;\n  1971:     ///\n  1972:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1973:     ///",
    "nanvix_source": "  1916:     ///     use std::fs;\n  1917:     ///\n  1918:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1919:     ///\n  1920:     ///     println!(\"{:?}\", metadata.file_type());\n  1921:     ///     Ok(())\n  1922:     /// }\n  1923:     /// ```\n  1924:     #[must_use]\n  1925:     #[stable(feature = \"file_type\", since = \"1.1.0\")]\n  1926:     pub fn file_type(&self) -> FileType {\n  1927:         FileType(self.0.file_type())\n  1928:     }\n  1929: \n  1930:     /// Returns `true` if this metadata is for a directory. The\n  1931:     /// result is mutually exclusive to the result of\n  1932:     /// [`Metadata::is_file`], and will be false for symlink metadata\n  1933:     /// obtained from [`symlink_metadata`].\n  1934:     ///\n  1935:     /// # Examples\n  1936:     ///",
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
