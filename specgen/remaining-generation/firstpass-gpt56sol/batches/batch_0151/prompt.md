For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::panic::panic_any",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "free_function"
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
                    "outlives": "'static"
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 417,
                        "path": "Any"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 6,
                        "path": "Send"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "M"
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
      "name": "panic_any",
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
            "msg",
            {
              "generic": "M"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "never"
        }
      }
    },
    "verification_source": "   243: pub use crate::panicking::update_hook;\n   244: #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   245: pub use crate::panicking::{set_hook, take_hook};\n   246: \n   247: /// Panics the current thread with the given message as the panic payload.\n   248: ///\n   249: /// The message can be of any (`Any + Send`) type, not just strings.\n   250: ///\n   251: /// The message is wrapped in a `Box<'static + Any + Send>`, which can be\n   252: /// accessed later using [`PanicHookInfo::payload`].\n   253: ///\n   254: /// See the [`panic!`] macro for more information about panicking.\n   255: #[stable(feature = \"panic_any\", since = \"1.51.0\")]\n   256: #[inline]\n   257: #[track_caller]\n   258: #[cfg_attr(not(test), rustc_diagnostic_item = \"panic_any\")]\n   259: pub fn panic_any<M: 'static + Any + Send>(msg: M) -> ! {\n   260:     crate::panicking::begin_panic(msg);\n   261: }\n   262: \n   263: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   264: impl<T: ?Sized> UnwindSafe for Mutex<T> {}\n   265: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   266: impl<T: ?Sized> UnwindSafe for RwLock<T> {}\n   267: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   268: impl UnwindSafe for Condvar {}\n   269: \n   270: #[stable(feature = \"unwind_safe_lock_refs\", since = \"1.12.0\")]\n   271: impl<T: ?Sized> RefUnwindSafe for Mutex<T> {}\n   272: #[stable(feature = \"unwind_safe_lock_refs\", since = \"1.12.0\")]\n   273: impl<T: ?Sized> RefUnwindSafe for RwLock<T> {}\n   274: #[stable(feature = \"unwind_safe_lock_refs\", since = \"1.12.0\")]\n   275: impl RefUnwindSafe for Condvar {}",
    "nanvix_source": "   249: /// The message can be of any (`Any + Send`) type, not just strings.\n   250: ///\n   251: /// The message is wrapped in a `Box<'static + Any + Send>`, which can be\n   252: /// accessed later using [`PanicHookInfo::payload`].\n   253: ///\n   254: /// See the [`panic!`] macro for more information about panicking.\n   255: #[stable(feature = \"panic_any\", since = \"1.51.0\")]\n   256: #[inline]\n   257: #[track_caller]\n   258: #[cfg_attr(not(test), rustc_diagnostic_item = \"panic_any\")]\n   259: pub fn panic_any<M: 'static + Any + Send>(msg: M) -> ! {\n   260:     crate::panicking::begin_panic(msg);\n   261: }\n   262: \n   263: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   264: impl<T: ?Sized> UnwindSafe for Mutex<T> {}\n   265: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   266: impl<T: ?Sized> UnwindSafe for RwLock<T> {}\n   267: #[stable(feature = \"catch_unwind\", since = \"1.9.0\")]\n   268: impl UnwindSafe for Condvar {}\n   269: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::resume_unwind",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "free_function"
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
      "name": "resume_unwind",
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
            "payload",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "dyn_trait": {
                            "lifetime": null,
                            "traits": [
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 417,
                                  "path": "Any"
                                }
                              },
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 6,
                                  "path": "Send"
                                }
                              }
                            ]
                          }
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
          "primitive": "never"
        }
      }
    },
    "verification_source": "   374: /// # Examples\n   375: ///\n   376: /// ```should_panic\n   377: /// use std::panic;\n   378: ///\n   379: /// let result = panic::catch_unwind(|| {\n   380: ///     if 1 != 2 {\n   381: ///         panic!(\"oh no!\");\n   382: ///     }\n   383: /// });\n   384: ///\n   385: /// if let Err(err) = result {\n   386: ///     panic::resume_unwind(err);\n   387: /// }\n   388: /// ```\n   389: #[stable(feature = \"resume_unwind\", since = \"1.9.0\")]\n   390: pub fn resume_unwind(payload: Box<dyn Any + Send>) -> ! {\n   391:     panicking::resume_unwind(payload)\n   392: }\n   393: \n   394: /// Makes all future panics abort directly without running the panic hook or unwinding.\n   395: ///\n   396: /// There is no way to undo this; the effect lasts until the process exits or\n   397: /// execs (or the equivalent).\n   398: ///\n   399: /// # Use after fork\n   400: ///\n   401: /// This function is particularly useful for calling after `libc::fork`.  After `fork`, in a\n   402: /// multithreaded program it is (on many platforms) not safe to call the allocator.  It is also\n   403: /// generally highly undesirable for an unwind to unwind past the `fork`, because that results in\n   404: /// the unwind propagating to code that was only ever expecting to run in the parent.\n   405: ///\n   406: /// `panic::always_abort()` helps avoid both of these.  It directly avoids any further unwinding,",
    "nanvix_source": "   380: ///     if 1 != 2 {\n   381: ///         panic!(\"oh no!\");\n   382: ///     }\n   383: /// });\n   384: ///\n   385: /// if let Err(err) = result {\n   386: ///     panic::resume_unwind(err);\n   387: /// }\n   388: /// ```\n   389: #[stable(feature = \"resume_unwind\", since = \"1.9.0\")]\n   390: pub fn resume_unwind(payload: Box<dyn Any + Send>) -> ! {\n   391:     panicking::resume_unwind(payload)\n   392: }\n   393: \n   394: /// Makes all future panics abort directly without running the panic hook or unwinding.\n   395: ///\n   396: /// There is no way to undo this; the effect lasts until the process exits or\n   397: /// execs (or the equivalent).\n   398: ///\n   399: /// # Use after fork\n   400: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Component::as_os_str",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 2403,
            "path": "Component"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6794",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2403",
        "resolved_owner_path": [
          "std",
          "path",
          "Component"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
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
    "verification_source": "   557: }\n   558: \n   559: impl<'a> Component<'a> {\n   560:     /// Extracts the underlying [`OsStr`] slice.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```\n   565:     /// use std::path::Path;\n   566:     ///\n   567:     /// let path = Path::new(\"./tmp/foo/bar.txt\");\n   568:     /// let components: Vec<_> = path.components().map(|comp| comp.as_os_str()).collect();\n   569:     /// assert_eq!(&components, &[\".\", \"tmp\", \"foo\", \"bar.txt\"]);\n   570:     /// ```\n   571:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   572:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   573:     pub fn as_os_str(self) -> &'a OsStr {\n   574:         match self {\n   575:             Component::Prefix(p) => p.as_os_str(),\n   576:             Component::RootDir => OsStr::new(MAIN_SEPARATOR_STR),\n   577:             Component::CurDir => OsStr::new(\".\"),\n   578:             Component::ParentDir => OsStr::new(\"..\"),\n   579:             Component::Normal(path) => path,\n   580:         }\n   581:     }\n   582: }\n   583: \n   584: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   585: impl AsRef<OsStr> for Component<'_> {\n   586:     #[inline]\n   587:     fn as_ref(&self) -> &OsStr {\n   588:         self.as_os_str()\n   589:     }",
    "nanvix_source": "   563:     ///\n   564:     /// ```\n   565:     /// use std::path::Path;\n   566:     ///\n   567:     /// let path = Path::new(\"./tmp/foo/bar.txt\");\n   568:     /// let components: Vec<_> = path.components().map(|comp| comp.as_os_str()).collect();\n   569:     /// assert_eq!(&components, &[\".\", \"tmp\", \"foo\", \"bar.txt\"]);\n   570:     /// ```\n   571:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   572:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   573:     pub fn as_os_str(self) -> &'a OsStr {\n   574:         match self {\n   575:             Component::Prefix(p) => p.as_os_str(),\n   576:             Component::RootDir => OsStr::new(MAIN_SEPARATOR_STR),\n   577:             Component::CurDir => OsStr::new(\".\"),\n   578:             Component::ParentDir => OsStr::new(\"..\"),\n   579:             Component::Normal(path) => path,\n   580:         }\n   581:     }\n   582: }\n   583: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Components::as_path",
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
      "name": "as_path",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 2406,
            "path": "Components"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6834",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2406",
        "resolved_owner_path": [
          "std",
          "path",
          "Components"
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
            "lifetime": "'a",
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
    "verification_source": "   712: \n   713:     /// Extracts a slice corresponding to the portion of the path remaining for iteration.\n   714:     ///\n   715:     /// # Examples\n   716:     ///\n   717:     /// ```\n   718:     /// use std::path::Path;\n   719:     ///\n   720:     /// let mut components = Path::new(\"/tmp/foo/bar.txt\").components();\n   721:     /// components.next();\n   722:     /// components.next();\n   723:     ///\n   724:     /// assert_eq!(Path::new(\"foo/bar.txt\"), components.as_path());\n   725:     /// ```\n   726:     #[must_use]\n   727:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   728:     pub fn as_path(&self) -> &'a Path {\n   729:         let mut comps = self.clone();\n   730:         if comps.front == State::Body {\n   731:             comps.trim_left();\n   732:         }\n   733:         if comps.back == State::Body {\n   734:             comps.trim_right();\n   735:         }\n   736:         unsafe { Path::from_u8_slice(comps.path) }\n   737:     }\n   738: \n   739:     /// Is the *original* path rooted?\n   740:     fn has_root(&self) -> bool {\n   741:         if self.has_physical_root {\n   742:             return true;\n   743:         }\n   744:         if HAS_PREFIXES && let Some(p) = self.prefix {",
    "nanvix_source": "   718:     /// use std::path::Path;\n   719:     ///\n   720:     /// let mut components = Path::new(\"/tmp/foo/bar.txt\").components();\n   721:     /// components.next();\n   722:     /// components.next();\n   723:     ///\n   724:     /// assert_eq!(Path::new(\"foo/bar.txt\"), components.as_path());\n   725:     /// ```\n   726:     #[must_use]\n   727:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   728:     pub fn as_path(&self) -> &'a Path {\n   729:         let mut comps = self.clone();\n   730:         if comps.front == State::Body {\n   731:             comps.trim_left();\n   732:         }\n   733:         if comps.back == State::Body {\n   734:             comps.trim_right();\n   735:         }\n   736:         unsafe { Path::from_u8_slice(comps.path) }\n   737:     }\n   738: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Iter::as_path",
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
      "name": "as_path",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 2409,
            "path": "Iter"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6874",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2409",
        "resolved_owner_path": [
          "std",
          "path",
          "Iter"
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
            "lifetime": "'a",
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
    "verification_source": "   861:     /// Extracts a slice corresponding to the portion of the path remaining for iteration.\n   862:     ///\n   863:     /// # Examples\n   864:     ///\n   865:     /// ```\n   866:     /// use std::path::Path;\n   867:     ///\n   868:     /// let mut iter = Path::new(\"/tmp/foo/bar.txt\").iter();\n   869:     /// iter.next();\n   870:     /// iter.next();\n   871:     ///\n   872:     /// assert_eq!(Path::new(\"foo/bar.txt\"), iter.as_path());\n   873:     /// ```\n   874:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   875:     #[must_use]\n   876:     #[inline]\n   877:     pub fn as_path(&self) -> &'a Path {\n   878:         self.inner.as_path()\n   879:     }\n   880: }\n   881: \n   882: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   883: impl AsRef<Path> for Iter<'_> {\n   884:     #[inline]\n   885:     fn as_ref(&self) -> &Path {\n   886:         self.as_path()\n   887:     }\n   888: }\n   889: \n   890: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   891: impl AsRef<OsStr> for Iter<'_> {\n   892:     #[inline]\n   893:     fn as_ref(&self) -> &OsStr {",
    "nanvix_source": "   867:     ///\n   868:     /// let mut iter = Path::new(\"/tmp/foo/bar.txt\").iter();\n   869:     /// iter.next();\n   870:     /// iter.next();\n   871:     ///\n   872:     /// assert_eq!(Path::new(\"foo/bar.txt\"), iter.as_path());\n   873:     /// ```\n   874:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   875:     #[must_use]\n   876:     #[inline]\n   877:     pub fn as_path(&self) -> &'a Path {\n   878:         self.inner.as_path()\n   879:     }\n   880: }\n   881: \n   882: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   883: impl AsRef<Path> for Iter<'_> {\n   884:     #[inline]\n   885:     fn as_ref(&self) -> &Path {\n   886:         self.as_path()\n   887:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::ancestors",
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
      "name": "ancestors",
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
            "id": 6906,
            "path": "Ancestors"
          }
        }
      }
    },
    "verification_source": "  2641:     /// assert_eq!(ancestors.next(), Some(Path::new(\"/foo/bar\")));\n  2642:     /// assert_eq!(ancestors.next(), Some(Path::new(\"/foo\")));\n  2643:     /// assert_eq!(ancestors.next(), Some(Path::new(\"/\")));\n  2644:     /// assert_eq!(ancestors.next(), None);\n  2645:     ///\n  2646:     /// let mut ancestors = Path::new(\"../foo/bar\").ancestors();\n  2647:     /// assert_eq!(ancestors.next(), Some(Path::new(\"../foo/bar\")));\n  2648:     /// assert_eq!(ancestors.next(), Some(Path::new(\"../foo\")));\n  2649:     /// assert_eq!(ancestors.next(), Some(Path::new(\"..\")));\n  2650:     /// assert_eq!(ancestors.next(), Some(Path::new(\"\")));\n  2651:     /// assert_eq!(ancestors.next(), None);\n  2652:     /// ```\n  2653:     ///\n  2654:     /// [`parent`]: Path::parent\n  2655:     #[stable(feature = \"path_ancestors\", since = \"1.28.0\")]\n  2656:     #[inline]\n  2657:     pub fn ancestors(&self) -> Ancestors<'_> {\n  2658:         Ancestors { next: Some(&self) }\n  2659:     }\n  2660: \n  2661:     /// Returns the final component of the `Path`, if there is one.\n  2662:     ///\n  2663:     /// If the path is a normal file, this is the file name. If it's the path of a directory, this\n  2664:     /// is the directory name.\n  2665:     ///\n  2666:     /// Returns [`None`] if the path terminates in `..`.\n  2667:     ///\n  2668:     /// # Examples\n  2669:     ///\n  2670:     /// ```\n  2671:     /// use std::path::Path;\n  2672:     /// use std::ffi::OsStr;\n  2673:     ///",
    "nanvix_source": "  2665:     /// assert_eq!(ancestors.next(), Some(Path::new(\"../foo/bar\")));\n  2666:     /// assert_eq!(ancestors.next(), Some(Path::new(\"../foo\")));\n  2667:     /// assert_eq!(ancestors.next(), Some(Path::new(\"..\")));\n  2668:     /// assert_eq!(ancestors.next(), Some(Path::new(\"\")));\n  2669:     /// assert_eq!(ancestors.next(), None);\n  2670:     /// ```\n  2671:     ///\n  2672:     /// [`parent`]: Path::parent\n  2673:     #[stable(feature = \"path_ancestors\", since = \"1.28.0\")]\n  2674:     #[inline]\n  2675:     pub fn ancestors(&self) -> Ancestors<'_> {\n  2676:         Ancestors { next: Some(&self) }\n  2677:     }\n  2678: \n  2679:     /// Returns the final component of the `Path`, if there is one.\n  2680:     ///\n  2681:     /// If the path is a normal file, this is the file name. If it's the path of a directory, this\n  2682:     /// is the directory name.\n  2683:     ///\n  2684:     /// Returns [`None`] if the path terminates in `..`.\n  2685:     ///",
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
