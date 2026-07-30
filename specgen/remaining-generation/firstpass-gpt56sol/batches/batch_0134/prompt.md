For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::panic::Location::column",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "column",
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
            "id": 8274,
            "path": "Location"
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
        "impl_id": "core:28189",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8274",
        "resolved_owner_path": [
          "core",
          "panic",
          "location",
          "Location"
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   263:     /// ```\n   264:     #[must_use]\n   265:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   266:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   267:     #[inline]\n   268:     pub const fn line(&self) -> u32 {\n   269:         self.line\n   270:     }\n   271: \n   272:     /// Returns the column from which the panic originated.\n   273:     ///\n   274:     /// # Examples\n   275:     ///\n   276:     /// ```should_panic\n   277:     /// use std::panic;\n   278:     ///\n   279:     /// panic::set_hook(Box::new(|panic_info| {\n   280:     ///     if let Some(location) = panic_info.location() {\n   281:     ///         println!(\"panic occurred at column {}\", location.column());\n   282:     ///     } else {\n   283:     ///         println!(\"panic occurred but can't get location information...\");\n   284:     ///     }\n   285:     /// }));\n   286:     ///\n   287:     /// panic!(\"Normal panic\");\n   288:     /// ```\n   289:     #[must_use]\n   290:     #[stable(feature = \"panic_col\", since = \"1.25.0\")]\n   291:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   292:     #[inline]\n   293:     pub const fn column(&self) -> u32 {\n   294:         self.col\n   295:     }",
    "nanvix_source": "   269:         self.line\n   270:     }\n   271: \n   272:     /// Returns the column from which the panic originated.\n   273:     ///\n   274:     /// # Examples\n   275:     ///\n   276:     /// ```should_panic\n   277:     /// use std::panic;\n   278:     ///\n   279:     /// panic::set_hook(Box::new(|panic_info| {\n   280:     ///     if let Some(location) = panic_info.location() {\n   281:     ///         println!(\"panic occurred at column {}\", location.column());\n   282:     ///     } else {\n   283:     ///         println!(\"panic occurred but can't get location information...\");\n   284:     ///     }\n   285:     /// }));\n   286:     ///\n   287:     /// panic!(\"Normal panic\");\n   288:     /// ```\n   289:     #[must_use]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::Location::file",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "file",
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
            "id": 8274,
            "path": "Location"
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
        "impl_id": "core:28189",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8274",
        "resolved_owner_path": [
          "core",
          "panic",
          "location",
          "Location"
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
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "   204:     /// ```should_panic\n   205:     /// use std::panic;\n   206:     ///\n   207:     /// panic::set_hook(Box::new(|panic_info| {\n   208:     ///     if let Some(location) = panic_info.location() {\n   209:     ///         println!(\"panic occurred in file '{}'\", location.file());\n   210:     ///     } else {\n   211:     ///         println!(\"panic occurred but can't get location information...\");\n   212:     ///     }\n   213:     /// }));\n   214:     ///\n   215:     /// panic!(\"Normal panic\");\n   216:     /// ```\n   217:     #[must_use]\n   218:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   219:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   220:     pub const fn file(&self) -> &'a str {\n   221:         // SAFETY: The filename is valid.\n   222:         unsafe { self.filename.as_ref() }\n   223:     }\n   224: \n   225:     /// Returns the name of the source file as a nul-terminated `CStr`.\n   226:     ///\n   227:     /// This is useful for interop with APIs that expect C/C++ `__FILE__` or\n   228:     /// `std::source_location::file_name`, both of which return a nul-terminated `const char*`.\n   229:     #[must_use]\n   230:     #[inline]\n   231:     #[stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   232:     #[rustc_const_stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   233:     pub const fn file_as_c_str(&self) -> &'a CStr {\n   234:         let filename = self.filename.as_ptr();\n   235: \n   236:         // SAFETY: The filename is valid for `filename_len+1` bytes, so this addition can't",
    "nanvix_source": "   210:     ///     } else {\n   211:     ///         println!(\"panic occurred but can't get location information...\");\n   212:     ///     }\n   213:     /// }));\n   214:     ///\n   215:     /// panic!(\"Normal panic\");\n   216:     /// ```\n   217:     #[must_use]\n   218:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   219:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   220:     pub const fn file(&self) -> &'a str {\n   221:         // SAFETY: The filename is valid.\n   222:         unsafe { self.filename.as_ref() }\n   223:     }\n   224: \n   225:     /// Returns the name of the source file as a nul-terminated `CStr`.\n   226:     ///\n   227:     /// This is useful for interop with APIs that expect C/C++ `__FILE__` or\n   228:     /// `std::source_location::file_name`, both of which return a nul-terminated `const char*`.\n   229:     #[must_use]\n   230:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::Location::file_as_c_str",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "file_as_c_str",
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
            "id": 8274,
            "path": "Location"
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
        "impl_id": "core:28189",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8274",
        "resolved_owner_path": [
          "core",
          "panic",
          "location",
          "Location"
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
                "id": 10771,
                "path": "CStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   217:     #[must_use]\n   218:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   219:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   220:     pub const fn file(&self) -> &'a str {\n   221:         // SAFETY: The filename is valid.\n   222:         unsafe { self.filename.as_ref() }\n   223:     }\n   224: \n   225:     /// Returns the name of the source file as a nul-terminated `CStr`.\n   226:     ///\n   227:     /// This is useful for interop with APIs that expect C/C++ `__FILE__` or\n   228:     /// `std::source_location::file_name`, both of which return a nul-terminated `const char*`.\n   229:     #[must_use]\n   230:     #[inline]\n   231:     #[stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   232:     #[rustc_const_stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   233:     pub const fn file_as_c_str(&self) -> &'a CStr {\n   234:         let filename = self.filename.as_ptr();\n   235: \n   236:         // SAFETY: The filename is valid for `filename_len+1` bytes, so this addition can't\n   237:         // overflow.\n   238:         let cstr_len = unsafe { crate::mem::size_of_val_raw(filename).unchecked_add(1) };\n   239: \n   240:         // SAFETY: The filename is valid for `filename_len+1` bytes.\n   241:         let slice = unsafe { crate::slice::from_raw_parts(filename.cast(), cstr_len) };\n   242: \n   243:         // SAFETY: The filename is guaranteed to have a trailing nul byte and no interior nul bytes.\n   244:         unsafe { CStr::from_bytes_with_nul_unchecked(slice) }\n   245:     }\n   246: \n   247:     /// Returns the line number from which the panic originated.\n   248:     ///\n   249:     /// # Examples",
    "nanvix_source": "   223:     }\n   224: \n   225:     /// Returns the name of the source file as a nul-terminated `CStr`.\n   226:     ///\n   227:     /// This is useful for interop with APIs that expect C/C++ `__FILE__` or\n   228:     /// `std::source_location::file_name`, both of which return a nul-terminated `const char*`.\n   229:     #[must_use]\n   230:     #[inline]\n   231:     #[stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   232:     #[rustc_const_stable(feature = \"file_with_nul\", since = \"1.92.0\")]\n   233:     pub const fn file_as_c_str(&self) -> &'a CStr {\n   234:         let filename = self.filename.as_ptr();\n   235: \n   236:         // SAFETY: The filename is valid for `filename_len+1` bytes, so this addition can't\n   237:         // overflow.\n   238:         let cstr_len = unsafe { crate::mem::size_of_val_raw(filename).unchecked_add(1) };\n   239: \n   240:         // SAFETY: The filename is valid for `filename_len+1` bytes.\n   241:         let slice = unsafe { crate::slice::from_raw_parts(filename.cast(), cstr_len) };\n   242: \n   243:         // SAFETY: The filename is guaranteed to have a trailing nul byte and no interior nul bytes.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::Location::line",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "line",
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
            "id": 8274,
            "path": "Location"
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
        "impl_id": "core:28189",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8274",
        "resolved_owner_path": [
          "core",
          "panic",
          "location",
          "Location"
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   250:     ///\n   251:     /// ```should_panic\n   252:     /// use std::panic;\n   253:     ///\n   254:     /// panic::set_hook(Box::new(|panic_info| {\n   255:     ///     if let Some(location) = panic_info.location() {\n   256:     ///         println!(\"panic occurred at line {}\", location.line());\n   257:     ///     } else {\n   258:     ///         println!(\"panic occurred but can't get location information...\");\n   259:     ///     }\n   260:     /// }));\n   261:     ///\n   262:     /// panic!(\"Normal panic\");\n   263:     /// ```\n   264:     #[must_use]\n   265:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   266:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   267:     #[inline]\n   268:     pub const fn line(&self) -> u32 {\n   269:         self.line\n   270:     }\n   271: \n   272:     /// Returns the column from which the panic originated.\n   273:     ///\n   274:     /// # Examples\n   275:     ///\n   276:     /// ```should_panic\n   277:     /// use std::panic;\n   278:     ///\n   279:     /// panic::set_hook(Box::new(|panic_info| {\n   280:     ///     if let Some(location) = panic_info.location() {\n   281:     ///         println!(\"panic occurred at column {}\", location.column());\n   282:     ///     } else {",
    "nanvix_source": "   256:     ///         println!(\"panic occurred at line {}\", location.line());\n   257:     ///     } else {\n   258:     ///         println!(\"panic occurred but can't get location information...\");\n   259:     ///     }\n   260:     /// }));\n   261:     ///\n   262:     /// panic!(\"Normal panic\");\n   263:     /// ```\n   264:     #[must_use]\n   265:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   266:     #[rustc_const_stable(feature = \"const_location_fields\", since = \"1.79.0\")]\n   267:     #[inline]\n   268:     pub const fn line(&self) -> u32 {\n   269:         self.line\n   270:     }\n   271: \n   272:     /// Returns the column from which the panic originated.\n   273:     ///\n   274:     /// # Examples\n   275:     ///\n   276:     /// ```should_panic",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::PanicInfo::location",
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
      "name": "location",
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
            "id": 12971,
            "path": "PanicInfo"
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
        "impl_id": "core:28214",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:12971",
        "resolved_owner_path": [
          "core",
          "panic",
          "panic_info",
          "PanicInfo"
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
                            "id": 8274,
                            "path": "Location"
                          }
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "    75:     ///\n    76:     /// panic::set_hook(Box::new(|panic_info| {\n    77:     ///     if let Some(location) = panic_info.location() {\n    78:     ///         println!(\"panic occurred in file '{}' at line {}\",\n    79:     ///             location.file(),\n    80:     ///             location.line(),\n    81:     ///         );\n    82:     ///     } else {\n    83:     ///         println!(\"panic occurred but can't get location information...\");\n    84:     ///     }\n    85:     /// }));\n    86:     ///\n    87:     /// panic!(\"Normal panic\");\n    88:     /// ```\n    89:     #[must_use]\n    90:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    91:     pub fn location(&self) -> Option<&Location<'_>> {\n    92:         // NOTE: If this is changed to sometimes return None,\n    93:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n    94:         Some(&self.location)\n    95:     }\n    96: \n    97:     /// Returns the payload associated with the panic.\n    98:     ///\n    99:     /// On this type, `core::panic::PanicInfo`, this method never returns anything useful.\n   100:     /// It only exists because of compatibility with [`std::panic::PanicHookInfo`],\n   101:     /// which used to be the same type.\n   102:     ///\n   103:     /// See [`std::panic::PanicHookInfo::payload`].\n   104:     ///\n   105:     /// [`std::panic::PanicHookInfo`]: ../../std/panic/struct.PanicHookInfo.html\n   106:     /// [`std::panic::PanicHookInfo::payload`]: ../../std/panic/struct.PanicHookInfo.html#method.payload\n   107:     #[deprecated(since = \"1.81.0\", note = \"this never returns anything useful\")]",
    "nanvix_source": "    81:     ///         );\n    82:     ///     } else {\n    83:     ///         println!(\"panic occurred but can't get location information...\");\n    84:     ///     }\n    85:     /// }));\n    86:     ///\n    87:     /// panic!(\"Normal panic\");\n    88:     /// ```\n    89:     #[must_use]\n    90:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n    91:     pub fn location(&self) -> Option<&'static Location<'static>> {\n    92:         // NOTE: If this is changed to sometimes return None,\n    93:         // deal with that case in std::panicking::default_hook and core::panicking::panic_fmt.\n    94:         Some(self.location)\n    95:     }\n    96: \n    97:     /// Returns the payload associated with the panic.\n    98:     ///\n    99:     /// On this type, `core::panic::PanicInfo`, this method never returns anything useful.\n   100:     /// It only exists because of compatibility with [`std::panic::PanicHookInfo`],\n   101:     /// which used to be the same type.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::PanicInfo::message",
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
      "name": "message",
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
            "id": 12971,
            "path": "PanicInfo"
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
        "impl_id": "core:28214",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:12971",
        "resolved_owner_path": [
          "core",
          "panic",
          "panic_info",
          "PanicInfo"
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
            "id": 13398,
            "path": "PanicMessage"
          }
        }
      }
    },
    "verification_source": "    45:     /// # Example\n    46:     ///\n    47:     /// The type returned by this method implements `Display`, so it can\n    48:     /// be passed directly to [`write!()`] and similar macros.\n    49:     ///\n    50:     /// [`write!()`]: core::write\n    51:     ///\n    52:     /// ```ignore (no_std)\n    53:     /// #[panic_handler]\n    54:     /// fn panic_handler(panic_info: &PanicInfo<'_>) -> ! {\n    55:     ///     write!(DEBUG_OUTPUT, \"panicked: {}\", panic_info.message());\n    56:     ///     loop {}\n    57:     /// }\n    58:     /// ```\n    59:     #[must_use]\n    60:     #[stable(feature = \"panic_info_message\", since = \"1.81.0\")]\n    61:     pub fn message(&self) -> PanicMessage<'_> {\n    62:         PanicMessage { message: self.message }\n    63:     }\n    64: \n    65:     /// Returns information about the location from which the panic originated,\n    66:     /// if available.\n    67:     ///\n    68:     /// This method will currently always return [`Some`], but this may change\n    69:     /// in future versions.\n    70:     ///\n    71:     /// # Examples\n    72:     ///\n    73:     /// ```should_panic\n    74:     /// use std::panic;\n    75:     ///\n    76:     /// panic::set_hook(Box::new(|panic_info| {\n    77:     ///     if let Some(location) = panic_info.location() {",
    "nanvix_source": "    51:     ///\n    52:     /// ```ignore (no_std)\n    53:     /// #[panic_handler]\n    54:     /// fn panic_handler(panic_info: &PanicInfo<'_>) -> ! {\n    55:     ///     write!(DEBUG_OUTPUT, \"panicked: {}\", panic_info.message());\n    56:     ///     loop {}\n    57:     /// }\n    58:     /// ```\n    59:     #[must_use]\n    60:     #[stable(feature = \"panic_info_message\", since = \"1.81.0\")]\n    61:     pub fn message(&self) -> PanicMessage<'_> {\n    62:         PanicMessage { message: self.message }\n    63:     }\n    64: \n    65:     /// Returns information about the location from which the panic originated,\n    66:     /// if available.\n    67:     ///\n    68:     /// This method will currently always return [`Some`], but this may change\n    69:     /// in future versions.\n    70:     ///\n    71:     /// # Examples",
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
