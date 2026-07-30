For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ffi::CStr::count_bytes",
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
      "name": "count_bytes",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   498:     ///\n   499:     /// > **Note**: This method is currently implemented as a constant-time\n   500:     /// > cast, but it is planned to alter its definition in the future to\n   501:     /// > perform the length calculation whenever this method is called.\n   502:     ///\n   503:     /// # Examples\n   504:     ///\n   505:     /// ```\n   506:     /// assert_eq!(c\"foo\".count_bytes(), 3);\n   507:     /// assert_eq!(c\"\".count_bytes(), 0);\n   508:     /// ```\n   509:     #[inline]\n   510:     #[must_use]\n   511:     #[doc(alias(\"len\", \"strlen\"))]\n   512:     #[stable(feature = \"cstr_count_bytes\", since = \"1.79.0\")]\n   513:     #[rustc_const_stable(feature = \"const_cstr_from_ptr\", since = \"1.81.0\")]\n   514:     pub const fn count_bytes(&self) -> usize {\n   515:         self.inner.len() - 1\n   516:     }\n   517: \n   518:     /// Returns `true` if `self.to_bytes()` has a length of 0.\n   519:     ///\n   520:     /// # Examples\n   521:     ///\n   522:     /// ```\n   523:     /// assert!(!c\"foo\".is_empty());\n   524:     /// assert!(c\"\".is_empty());\n   525:     /// ```\n   526:     #[inline]\n   527:     #[stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   528:     #[rustc_const_stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   529:     pub const fn is_empty(&self) -> bool {\n   530:         // SAFETY: We know there is at least one byte; for empty strings it",
    "nanvix_source": "   505:     ///\n   506:     /// ```\n   507:     /// assert_eq!(c\"foo\".count_bytes(), 3);\n   508:     /// assert_eq!(c\"\".count_bytes(), 0);\n   509:     /// ```\n   510:     #[inline]\n   511:     #[must_use]\n   512:     #[doc(alias(\"len\", \"strlen\"))]\n   513:     #[stable(feature = \"cstr_count_bytes\", since = \"1.79.0\")]\n   514:     #[rustc_const_stable(feature = \"const_cstr_from_ptr\", since = \"1.81.0\")]\n   515:     pub const fn count_bytes(&self) -> usize {\n   516:         self.inner.len() - 1\n   517:     }\n   518: \n   519:     /// Returns `true` if `self.to_bytes()` has a length of 0.\n   520:     ///\n   521:     /// # Examples\n   522:     ///\n   523:     /// ```\n   524:     /// assert!(!c\"foo\".is_empty());\n   525:     /// assert!(c\"\".is_empty());",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::from_bytes_until_nul",
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
      "name": "from_bytes_until_nul",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
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
                            "id": 10771,
                            "path": "CStr"
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 9830,
                        "path": "FromBytesUntilNulError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   282:     /// use std::ffi::CStr;\n   283:     ///\n   284:     /// let mut buffer = [0u8; 16];\n   285:     /// unsafe {\n   286:     ///     // Here we might call an unsafe C function that writes a string\n   287:     ///     // into the buffer.\n   288:     ///     let buf_ptr = buffer.as_mut_ptr();\n   289:     ///     buf_ptr.write_bytes(b'A', 8);\n   290:     /// }\n   291:     /// // Attempt to extract a C nul-terminated string from the buffer.\n   292:     /// let c_str = CStr::from_bytes_until_nul(&buffer[..]).unwrap();\n   293:     /// assert_eq!(c_str.to_str().unwrap(), \"AAAAAAAA\");\n   294:     /// ```\n   295:     ///\n   296:     #[stable(feature = \"cstr_from_bytes_until_nul\", since = \"1.69.0\")]\n   297:     #[rustc_const_stable(feature = \"cstr_from_bytes_until_nul\", since = \"1.69.0\")]\n   298:     pub const fn from_bytes_until_nul(bytes: &[u8]) -> Result<&CStr, FromBytesUntilNulError> {\n   299:         let nul_pos = memchr::memchr(0, bytes);\n   300:         match nul_pos {\n   301:             Some(nul_pos) => {\n   302:                 // FIXME(const-hack) replace with range index\n   303:                 // SAFETY: nul_pos + 1 <= bytes.len()\n   304:                 let subslice = unsafe { crate::slice::from_raw_parts(bytes.as_ptr(), nul_pos + 1) };\n   305:                 // SAFETY: We know there is a nul byte at nul_pos, so this slice\n   306:                 // (ending at the nul byte) is a well-formed C string.\n   307:                 Ok(unsafe { CStr::from_bytes_with_nul_unchecked(subslice) })\n   308:             }\n   309:             None => Err(FromBytesUntilNulError(())),\n   310:         }\n   311:     }\n   312: \n   313:     /// Creates a C string wrapper from a byte slice with exactly one nul\n   314:     /// terminator.",
    "nanvix_source": "   289:     ///     let buf_ptr = buffer.as_mut_ptr();\n   290:     ///     buf_ptr.write_bytes(b'A', 8);\n   291:     /// }\n   292:     /// // Attempt to extract a C nul-terminated string from the buffer.\n   293:     /// let c_str = CStr::from_bytes_until_nul(&buffer[..]).unwrap();\n   294:     /// assert_eq!(c_str.to_str().unwrap(), \"AAAAAAAA\");\n   295:     /// ```\n   296:     ///\n   297:     #[stable(feature = \"cstr_from_bytes_until_nul\", since = \"1.69.0\")]\n   298:     #[rustc_const_stable(feature = \"cstr_from_bytes_until_nul\", since = \"1.69.0\")]\n   299:     pub const fn from_bytes_until_nul(bytes: &[u8]) -> Result<&CStr, FromBytesUntilNulError> {\n   300:         let nul_pos = memchr::memchr(0, bytes);\n   301:         match nul_pos {\n   302:             Some(nul_pos) => {\n   303:                 // FIXME(const-hack) replace with range index\n   304:                 // SAFETY: nul_pos + 1 <= bytes.len()\n   305:                 let subslice = unsafe { crate::slice::from_raw_parts(bytes.as_ptr(), nul_pos + 1) };\n   306:                 // SAFETY: We know there is a nul byte at nul_pos, so this slice\n   307:                 // (ending at the nul byte) is a well-formed C string.\n   308:                 Ok(unsafe { CStr::from_bytes_with_nul_unchecked(subslice) })\n   309:             }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::from_bytes_with_nul",
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
      "name": "from_bytes_with_nul",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
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
                          "generic": "Self"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 9827,
                        "path": "FromBytesWithNulError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   335:     /// use std::ffi::{CStr, FromBytesWithNulError};\n   336:     ///\n   337:     /// let cstr = CStr::from_bytes_with_nul(b\"hello\");\n   338:     /// assert_eq!(cstr, Err(FromBytesWithNulError::NotNulTerminated));\n   339:     /// ```\n   340:     ///\n   341:     /// Creating a `CStr` with an interior nul byte is an error:\n   342:     ///\n   343:     /// ```\n   344:     /// use std::ffi::{CStr, FromBytesWithNulError};\n   345:     ///\n   346:     /// let cstr = CStr::from_bytes_with_nul(b\"he\\0llo\\0\");\n   347:     /// assert_eq!(cstr, Err(FromBytesWithNulError::InteriorNul { position: 2 }));\n   348:     /// ```\n   349:     #[stable(feature = \"cstr_from_bytes\", since = \"1.10.0\")]\n   350:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   351:     pub const fn from_bytes_with_nul(bytes: &[u8]) -> Result<&Self, FromBytesWithNulError> {\n   352:         let nul_pos = memchr::memchr(0, bytes);\n   353:         match nul_pos {\n   354:             Some(nul_pos) if nul_pos + 1 == bytes.len() => {\n   355:                 // SAFETY: We know there is only one nul byte, at the end\n   356:                 // of the byte slice.\n   357:                 Ok(unsafe { Self::from_bytes_with_nul_unchecked(bytes) })\n   358:             }\n   359:             Some(position) => Err(FromBytesWithNulError::InteriorNul { position }),\n   360:             None => Err(FromBytesWithNulError::NotNulTerminated),\n   361:         }\n   362:     }\n   363: \n   364:     /// Unsafely creates a C string wrapper from a byte slice.\n   365:     ///\n   366:     /// This function will cast the provided `bytes` to a `CStr` wrapper without\n   367:     /// performing any sanity checks.",
    "nanvix_source": "   342:     /// Creating a `CStr` with an interior nul byte is an error:\n   343:     ///\n   344:     /// ```\n   345:     /// use std::ffi::{CStr, FromBytesWithNulError};\n   346:     ///\n   347:     /// let cstr = CStr::from_bytes_with_nul(b\"he\\0llo\\0\");\n   348:     /// assert_eq!(cstr, Err(FromBytesWithNulError::InteriorNul { position: 2 }));\n   349:     /// ```\n   350:     #[stable(feature = \"cstr_from_bytes\", since = \"1.10.0\")]\n   351:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   352:     pub const fn from_bytes_with_nul(bytes: &[u8]) -> Result<&Self, FromBytesWithNulError> {\n   353:         let nul_pos = memchr::memchr(0, bytes);\n   354:         match nul_pos {\n   355:             Some(nul_pos) if nul_pos + 1 == bytes.len() => {\n   356:                 // SAFETY: We know there is only one nul byte, at the end\n   357:                 // of the byte slice.\n   358:                 Ok(unsafe { Self::from_bytes_with_nul_unchecked(bytes) })\n   359:             }\n   360:             Some(position) => Err(FromBytesWithNulError::InteriorNul { position }),\n   361:             None => Err(FromBytesWithNulError::NotNulTerminated),\n   362:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::is_empty",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
    "verification_source": "   513:     #[rustc_const_stable(feature = \"const_cstr_from_ptr\", since = \"1.81.0\")]\n   514:     pub const fn count_bytes(&self) -> usize {\n   515:         self.inner.len() - 1\n   516:     }\n   517: \n   518:     /// Returns `true` if `self.to_bytes()` has a length of 0.\n   519:     ///\n   520:     /// # Examples\n   521:     ///\n   522:     /// ```\n   523:     /// assert!(!c\"foo\".is_empty());\n   524:     /// assert!(c\"\".is_empty());\n   525:     /// ```\n   526:     #[inline]\n   527:     #[stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   528:     #[rustc_const_stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   529:     pub const fn is_empty(&self) -> bool {\n   530:         // SAFETY: We know there is at least one byte; for empty strings it\n   531:         // is the NUL terminator.\n   532:         // FIXME(const-hack): use get_unchecked\n   533:         unsafe { *self.inner.as_ptr() == 0 }\n   534:     }\n   535: \n   536:     /// Converts this C string to a byte slice.\n   537:     ///\n   538:     /// The returned slice will **not** contain the trailing nul terminator that this C\n   539:     /// string has.\n   540:     ///\n   541:     /// > **Note**: This method is currently implemented as a constant-time\n   542:     /// > cast, but it is planned to alter its definition in the future to\n   543:     /// > perform the length calculation whenever this method is called.\n   544:     ///\n   545:     /// # Examples",
    "nanvix_source": "   520:     ///\n   521:     /// # Examples\n   522:     ///\n   523:     /// ```\n   524:     /// assert!(!c\"foo\".is_empty());\n   525:     /// assert!(c\"\".is_empty());\n   526:     /// ```\n   527:     #[inline]\n   528:     #[stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   529:     #[rustc_const_stable(feature = \"cstr_is_empty\", since = \"1.71.0\")]\n   530:     pub const fn is_empty(&self) -> bool {\n   531:         // SAFETY: We know there is at least one byte; for empty strings it\n   532:         // is the NUL terminator.\n   533:         // FIXME(const-hack): use get_unchecked\n   534:         unsafe { *self.inner.as_ptr() == 0 }\n   535:     }\n   536: \n   537:     /// Converts this C string to a byte slice.\n   538:     ///\n   539:     /// The returned slice will **not** contain the trailing nul terminator that this C\n   540:     /// string has.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::to_bytes",
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
      "name": "to_bytes",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "   539:     /// string has.\n   540:     ///\n   541:     /// > **Note**: This method is currently implemented as a constant-time\n   542:     /// > cast, but it is planned to alter its definition in the future to\n   543:     /// > perform the length calculation whenever this method is called.\n   544:     ///\n   545:     /// # Examples\n   546:     ///\n   547:     /// ```\n   548:     /// assert_eq!(c\"foo\".to_bytes(), b\"foo\");\n   549:     /// ```\n   550:     #[inline]\n   551:     #[must_use = \"this returns the result of the operation, \\\n   552:                   without modifying the original\"]\n   553:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   554:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   555:     pub const fn to_bytes(&self) -> &[u8] {\n   556:         let bytes = self.to_bytes_with_nul();\n   557:         // FIXME(const-hack) replace with range index\n   558:         // SAFETY: to_bytes_with_nul returns slice with length at least 1\n   559:         unsafe { slice::from_raw_parts(bytes.as_ptr(), bytes.len() - 1) }\n   560:     }\n   561: \n   562:     /// Converts this C string to a byte slice containing the trailing 0 byte.\n   563:     ///\n   564:     /// This function is the equivalent of [`CStr::to_bytes`] except that it\n   565:     /// will retain the trailing nul terminator instead of chopping it off.\n   566:     ///\n   567:     /// > **Note**: This method is currently implemented as a 0-cost cast, but\n   568:     /// > it is planned to alter its definition in the future to perform the\n   569:     /// > length calculation whenever this method is called.\n   570:     ///\n   571:     /// # Examples",
    "nanvix_source": "   546:     /// # Examples\n   547:     ///\n   548:     /// ```\n   549:     /// assert_eq!(c\"foo\".to_bytes(), b\"foo\");\n   550:     /// ```\n   551:     #[inline]\n   552:     #[must_use = \"this returns the result of the operation, \\\n   553:                   without modifying the original\"]\n   554:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   555:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   556:     pub const fn to_bytes(&self) -> &[u8] {\n   557:         let bytes = self.to_bytes_with_nul();\n   558:         // FIXME(const-hack) replace with range index\n   559:         // SAFETY: to_bytes_with_nul returns slice with length at least 1\n   560:         unsafe { slice::from_raw_parts(bytes.as_ptr(), bytes.len() - 1) }\n   561:     }\n   562: \n   563:     /// Converts this C string to a byte slice containing the trailing 0 byte.\n   564:     ///\n   565:     /// This function is the equivalent of [`CStr::to_bytes`] except that it\n   566:     /// will retain the trailing nul terminator instead of chopping it off.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::to_bytes_with_nul",
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
      "name": "to_bytes_with_nul",
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
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "   565:     /// will retain the trailing nul terminator instead of chopping it off.\n   566:     ///\n   567:     /// > **Note**: This method is currently implemented as a 0-cost cast, but\n   568:     /// > it is planned to alter its definition in the future to perform the\n   569:     /// > length calculation whenever this method is called.\n   570:     ///\n   571:     /// # Examples\n   572:     ///\n   573:     /// ```\n   574:     /// assert_eq!(c\"foo\".to_bytes_with_nul(), b\"foo\\0\");\n   575:     /// ```\n   576:     #[inline]\n   577:     #[must_use = \"this returns the result of the operation, \\\n   578:                   without modifying the original\"]\n   579:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   580:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   581:     pub const fn to_bytes_with_nul(&self) -> &[u8] {\n   582:         // SAFETY: Transmuting a slice of `c_char`s to a slice of `u8`s\n   583:         // is safe on all supported targets.\n   584:         unsafe { &*((&raw const self.inner) as *const [u8]) }\n   585:     }\n   586: \n   587:     /// Iterates over the bytes in this C string.\n   588:     ///\n   589:     /// The returned iterator will **not** contain the trailing nul terminator\n   590:     /// that this C string has.\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// #![feature(cstr_bytes)]\n   596:     ///\n   597:     /// assert!(c\"foo\".bytes().eq(*b\"foo\"));",
    "nanvix_source": "   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// assert_eq!(c\"foo\".to_bytes_with_nul(), b\"foo\\0\");\n   576:     /// ```\n   577:     #[inline]\n   578:     #[must_use = \"this returns the result of the operation, \\\n   579:                   without modifying the original\"]\n   580:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   581:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   582:     pub const fn to_bytes_with_nul(&self) -> &[u8] {\n   583:         // SAFETY: Transmuting a slice of `c_char`s to a slice of `u8`s\n   584:         // is safe on all supported targets.\n   585:         unsafe { &*((&raw const self.inner) as *const [u8]) }\n   586:     }\n   587: \n   588:     /// Iterates over the bytes in this C string.\n   589:     ///\n   590:     /// The returned iterator will **not** contain the trailing nul terminator\n   591:     /// that this C string has.\n   592:     ///",
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
