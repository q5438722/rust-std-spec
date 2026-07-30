For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::Path::as_os_str",
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
      "name": "as_os_str",
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
    },
    "verification_source": "  2402:         unsafe { &mut *(inner as *mut OsStr as *mut Path) }\n  2403:     }\n  2404: \n  2405:     /// Yields the underlying [`OsStr`] slice.\n  2406:     ///\n  2407:     /// # Examples\n  2408:     ///\n  2409:     /// ```\n  2410:     /// use std::path::Path;\n  2411:     ///\n  2412:     /// let os_str = Path::new(\"foo.txt\").as_os_str();\n  2413:     /// assert_eq!(os_str, std::ffi::OsStr::new(\"foo.txt\"));\n  2414:     /// ```\n  2415:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2416:     #[must_use]\n  2417:     #[inline]\n  2418:     pub fn as_os_str(&self) -> &OsStr {\n  2419:         &self.inner\n  2420:     }\n  2421: \n  2422:     /// Yields a mutable reference to the underlying [`OsStr`] slice.\n  2423:     ///\n  2424:     /// # Examples\n  2425:     ///\n  2426:     /// ```\n  2427:     /// use std::path::{Path, PathBuf};\n  2428:     ///\n  2429:     /// let mut path = PathBuf::from(\"Foo.TXT\");\n  2430:     ///\n  2431:     /// assert_ne!(path, Path::new(\"foo.txt\"));\n  2432:     ///\n  2433:     /// path.as_mut_os_str().make_ascii_lowercase();\n  2434:     /// assert_eq!(path, Path::new(\"foo.txt\"));",
    "nanvix_source": "  2426:     ///\n  2427:     /// ```\n  2428:     /// use std::path::Path;\n  2429:     ///\n  2430:     /// let os_str = Path::new(\"foo.txt\").as_os_str();\n  2431:     /// assert_eq!(os_str, std::ffi::OsStr::new(\"foo.txt\"));\n  2432:     /// ```\n  2433:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2434:     #[must_use]\n  2435:     #[inline]\n  2436:     pub fn as_os_str(&self) -> &OsStr {\n  2437:         &self.inner\n  2438:     }\n  2439: \n  2440:     /// Yields a mutable reference to the underlying [`OsStr`] slice.\n  2441:     ///\n  2442:     /// # Examples\n  2443:     ///\n  2444:     /// ```\n  2445:     /// use std::path::{Path, PathBuf};\n  2446:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::canonicalize",
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
      "name": "canonicalize",
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
    "verification_source": "  3337:     /// This method will return an error in the following situations, but is not\n  3338:     /// limited to just these cases:\n  3339:     ///\n  3340:     /// * `path` does not exist.\n  3341:     /// * A non-final component in path is not a directory.\n  3342:     ///\n  3343:     /// # Examples\n  3344:     ///\n  3345:     /// ```no_run\n  3346:     /// use std::path::{Path, PathBuf};\n  3347:     ///\n  3348:     /// let path = Path::new(\"/foo/test/../test/bar.rs\");\n  3349:     /// assert_eq!(path.canonicalize().unwrap(), PathBuf::from(\"/foo/test/bar.rs\"));\n  3350:     /// ```\n  3351:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3352:     #[inline]\n  3353:     pub fn canonicalize(&self) -> io::Result<PathBuf> {\n  3354:         fs::canonicalize(self)\n  3355:     }\n  3356: \n  3357:     /// Makes the path absolute without accessing the filesystem.\n  3358:     ///\n  3359:     /// This is an alias to [`path::absolute`](absolute).\n  3360:     ///\n  3361:     /// # Errors\n  3362:     ///\n  3363:     /// This function may return an error in the following situations:\n  3364:     ///\n  3365:     /// * If the path is syntactically invalid; in particular, if it is empty.\n  3366:     /// * If getting the [current directory][crate::env::current_dir] fails.\n  3367:     ///\n  3368:     /// # Examples\n  3369:     ///",
    "nanvix_source": "  3373:     /// # Examples\n  3374:     ///\n  3375:     /// ```no_run\n  3376:     /// use std::path::{Path, PathBuf};\n  3377:     ///\n  3378:     /// let path = Path::new(\"/foo/test/../test/bar.rs\");\n  3379:     /// assert_eq!(path.canonicalize().unwrap(), PathBuf::from(\"/foo/test/bar.rs\"));\n  3380:     /// ```\n  3381:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3382:     #[inline]\n  3383:     pub fn canonicalize(&self) -> io::Result<PathBuf> {\n  3384:         fs::canonicalize(self)\n  3385:     }\n  3386: \n  3387:     /// Makes the path absolute without accessing the filesystem.\n  3388:     ///\n  3389:     /// This is an alias to [`path::absolute`](absolute).\n  3390:     ///\n  3391:     /// # Errors\n  3392:     ///\n  3393:     /// This function may return an error in the following situations:",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::components",
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
      "name": "components",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 2406,
            "path": "Components"
          }
        }
      }
    },
    "verification_source": "  3198:     /// # Examples\n  3199:     ///\n  3200:     /// ```\n  3201:     /// use std::path::{Path, Component};\n  3202:     /// use std::ffi::OsStr;\n  3203:     ///\n  3204:     /// let mut components = Path::new(\"/tmp/foo.txt\").components();\n  3205:     ///\n  3206:     /// assert_eq!(components.next(), Some(Component::RootDir));\n  3207:     /// assert_eq!(components.next(), Some(Component::Normal(OsStr::new(\"tmp\"))));\n  3208:     /// assert_eq!(components.next(), Some(Component::Normal(OsStr::new(\"foo.txt\"))));\n  3209:     /// assert_eq!(components.next(), None)\n  3210:     /// ```\n  3211:     ///\n  3212:     /// [`CurDir`]: Component::CurDir\n  3213:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3214:     pub fn components(&self) -> Components<'_> {\n  3215:         let prefix = parse_prefix(self.as_os_str());\n  3216:         Components {\n  3217:             path: self.as_u8_slice(),\n  3218:             prefix,\n  3219:             has_physical_root: has_physical_root(self.as_u8_slice(), prefix),\n  3220:             // use a platform-specific initial state to avoid one turn of\n  3221:             // the state-machine when the platform doesn't have a Prefix.\n  3222:             front: const { if HAS_PREFIXES { State::Prefix } else { State::StartDir } },\n  3223:             back: State::Body,\n  3224:         }\n  3225:     }\n  3226: \n  3227:     /// Produces an iterator over the path's components viewed as [`OsStr`]\n  3228:     /// slices.\n  3229:     ///\n  3230:     /// For more information about the particulars of how the path is separated",
    "nanvix_source": "  3234:     /// let mut components = Path::new(\"/tmp/foo.txt\").components();\n  3235:     ///\n  3236:     /// assert_eq!(components.next(), Some(Component::RootDir));\n  3237:     /// assert_eq!(components.next(), Some(Component::Normal(OsStr::new(\"tmp\"))));\n  3238:     /// assert_eq!(components.next(), Some(Component::Normal(OsStr::new(\"foo.txt\"))));\n  3239:     /// assert_eq!(components.next(), None)\n  3240:     /// ```\n  3241:     ///\n  3242:     /// [`CurDir`]: Component::CurDir\n  3243:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3244:     pub fn components(&self) -> Components<'_> {\n  3245:         let prefix = parse_prefix(self.as_os_str());\n  3246:         Components {\n  3247:             path: self.as_u8_slice(),\n  3248:             prefix,\n  3249:             has_physical_root: has_physical_root(self.as_u8_slice(), prefix),\n  3250:             // use a platform-specific initial state to avoid one turn of\n  3251:             // the state-machine when the platform doesn't have a Prefix.\n  3252:             front: const { if HAS_PREFIXES { State::Prefix } else { State::StartDir } },\n  3253:             back: State::Body,\n  3254:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::display",
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
      "name": "display",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7100,
            "path": "Display"
          }
        }
      }
    },
    "verification_source": "  3258:     /// [`Display`]: fmt::Display\n  3259:     /// [`Debug`]: fmt::Debug\n  3260:     ///\n  3261:     /// # Examples\n  3262:     ///\n  3263:     /// ```\n  3264:     /// use std::path::Path;\n  3265:     ///\n  3266:     /// let path = Path::new(\"/tmp/foo.rs\");\n  3267:     ///\n  3268:     /// println!(\"{}\", path.display());\n  3269:     /// ```\n  3270:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3271:     #[must_use = \"this does not display the path, \\\n  3272:                   it returns an object that can be displayed\"]\n  3273:     #[inline]\n  3274:     pub fn display(&self) -> Display<'_> {\n  3275:         Display { inner: self.inner.display() }\n  3276:     }\n  3277: \n  3278:     /// Returns the same path as `&Path`.\n  3279:     ///\n  3280:     /// This method is redundant when used directly on `&Path`, but\n  3281:     /// it helps dereferencing other `PathBuf`-like types to `Path`s,\n  3282:     /// for example references to `Box<Path>` or `Arc<Path>`.\n  3283:     #[inline]\n  3284:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]\n  3285:     pub const fn as_path(&self) -> &Path {\n  3286:         self\n  3287:     }\n  3288: \n  3289:     /// Queries the file system to get information about a file, directory, etc.\n  3290:     ///",
    "nanvix_source": "  3294:     /// use std::path::Path;\n  3295:     ///\n  3296:     /// let path = Path::new(\"/tmp/foo.rs\");\n  3297:     ///\n  3298:     /// println!(\"{}\", path.display());\n  3299:     /// ```\n  3300:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3301:     #[must_use = \"this does not display the path, \\\n  3302:                   it returns an object that can be displayed\"]\n  3303:     #[inline]\n  3304:     pub fn display(&self) -> Display<'_> {\n  3305:         Display { inner: self.inner.display() }\n  3306:     }\n  3307: \n  3308:     /// Returns the same path as `&Path`.\n  3309:     ///\n  3310:     /// This method is redundant when used directly on `&Path`, but\n  3311:     /// it helps dereferencing other `PathBuf`-like types to `Path`s,\n  3312:     /// for example references to `Box<Path>` or `Arc<Path>`.\n  3313:     #[inline]\n  3314:     #[unstable(feature = \"str_as_str\", issue = \"130366\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::ends_with",
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
      "name": "ends_with",
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
            "child",
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
    "verification_source": "  2805:     /// # Examples\n  2806:     ///\n  2807:     /// ```\n  2808:     /// use std::path::Path;\n  2809:     ///\n  2810:     /// let path = Path::new(\"/etc/resolv.conf\");\n  2811:     ///\n  2812:     /// assert!(path.ends_with(\"resolv.conf\"));\n  2813:     /// assert!(path.ends_with(\"etc/resolv.conf\"));\n  2814:     /// assert!(path.ends_with(\"/etc/resolv.conf\"));\n  2815:     ///\n  2816:     /// assert!(!path.ends_with(\"/resolv.conf\"));\n  2817:     /// assert!(!path.ends_with(\"conf\")); // use .extension() instead\n  2818:     /// ```\n  2819:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2820:     #[must_use]\n  2821:     pub fn ends_with<P: AsRef<Path>>(&self, child: P) -> bool {\n  2822:         self._ends_with(child.as_ref())\n  2823:     }\n  2824: \n  2825:     fn _ends_with(&self, child: &Path) -> bool {\n  2826:         iter_after(self.components().rev(), child.components().rev()).is_some()\n  2827:     }\n  2828: \n  2829:     /// Checks whether the `Path` is empty.\n  2830:     ///\n  2831:     /// # Examples\n  2832:     ///\n  2833:     /// ```\n  2834:     /// #![feature(path_is_empty)]\n  2835:     /// use std::path::Path;\n  2836:     ///\n  2837:     /// let path = Path::new(\"\");",
    "nanvix_source": "  2829:     ///\n  2830:     /// assert!(path.ends_with(\"resolv.conf\"));\n  2831:     /// assert!(path.ends_with(\"etc/resolv.conf\"));\n  2832:     /// assert!(path.ends_with(\"/etc/resolv.conf\"));\n  2833:     ///\n  2834:     /// assert!(!path.ends_with(\"/resolv.conf\"));\n  2835:     /// assert!(!path.ends_with(\"conf\")); // use .extension() instead\n  2836:     /// ```\n  2837:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2838:     #[must_use]\n  2839:     pub fn ends_with<P: AsRef<Path>>(&self, child: P) -> bool {\n  2840:         self._ends_with(child.as_ref())\n  2841:     }\n  2842: \n  2843:     fn _ends_with(&self, child: &Path) -> bool {\n  2844:         iter_after(self.components().rev(), child.components().rev()).is_some()\n  2845:     }\n  2846: \n  2847:     /// Checks whether the `Path` is empty.\n  2848:     ///\n  2849:     /// Passing an empty path to most OS filesystem APIs will always result in an error.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::exists",
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
      "name": "exists",
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
    "verification_source": "  3501:     ///\n  3502:     /// ```no_run\n  3503:     /// use std::path::Path;\n  3504:     /// assert!(!Path::new(\"does_not_exist.txt\").exists());\n  3505:     /// ```\n  3506:     ///\n  3507:     /// # See Also\n  3508:     ///\n  3509:     /// This is a convenience function that coerces errors to false. If you want to\n  3510:     /// check errors, call [`Path::try_exists`].\n  3511:     ///\n  3512:     /// [`try_exists()`]: Self::try_exists\n  3513:     /// [TOCTOU]: fs#time-of-check-to-time-of-use-toctou\n  3514:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3515:     #[must_use]\n  3516:     #[inline]\n  3517:     pub fn exists(&self) -> bool {\n  3518:         fs::metadata(self).is_ok()\n  3519:     }\n  3520: \n  3521:     /// Returns `Ok(true)` if the path points at an existing entity.\n  3522:     ///\n  3523:     /// This function will traverse symbolic links to query information about the\n  3524:     /// destination file. In case of broken symbolic links this will return `Ok(false)`.\n  3525:     ///\n  3526:     /// [`Path::exists()`] only checks whether or not a path was both found and readable. By\n  3527:     /// contrast, `try_exists` will return `Ok(true)` or `Ok(false)`, respectively, if the path\n  3528:     /// was _verified_ to exist or not exist. If its existence can neither be confirmed nor\n  3529:     /// denied, it will propagate an `Err(_)` instead. This can be the case if e.g. listing\n  3530:     /// permission is denied on one of the parent directories.\n  3531:     ///\n  3532:     /// Note that while this avoids some pitfalls of the `exists()` method, it still can not\n  3533:     /// prevent time-of-check to time-of-use ([TOCTOU]) bugs. You should only use it in scenarios",
    "nanvix_source": "  3537:     /// # See Also\n  3538:     ///\n  3539:     /// This is a convenience function that coerces errors to false. If you want to\n  3540:     /// check errors, call [`Path::try_exists`].\n  3541:     ///\n  3542:     /// [`try_exists()`]: Self::try_exists\n  3543:     /// [TOCTOU]: fs#time-of-check-to-time-of-use-toctou\n  3544:     #[stable(feature = \"path_ext\", since = \"1.5.0\")]\n  3545:     #[must_use]\n  3546:     #[inline]\n  3547:     pub fn exists(&self) -> bool {\n  3548:         fs::metadata(self).is_ok()\n  3549:     }\n  3550: \n  3551:     /// Returns `Ok(true)` if the path points at an existing entity.\n  3552:     ///\n  3553:     /// This function will traverse symbolic links to query information about the\n  3554:     /// destination file. In case of broken symbolic links this will return `Ok(false)`.\n  3555:     ///\n  3556:     /// [`Path::exists()`] only checks whether or not a path was both found and readable. By\n  3557:     /// contrast, `try_exists` will return `Ok(true)` or `Ok(false)`, respectively, if the path",
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
