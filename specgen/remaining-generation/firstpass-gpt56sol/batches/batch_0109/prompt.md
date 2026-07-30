For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::ffi::CString::into_bytes_with_nul",
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
      "name": "into_bytes_with_nul",
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
            "id": 108,
            "path": "CString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3307",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:108",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "CString"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
          }
        }
      }
    },
    "verification_source": "   507:     }\n   508: \n   509:     /// Equivalent to [`CString::into_bytes()`] except that the\n   510:     /// returned vector includes the trailing nul terminator.\n   511:     ///\n   512:     /// # Examples\n   513:     ///\n   514:     /// ```\n   515:     /// use std::ffi::CString;\n   516:     ///\n   517:     /// let c_string = CString::from(c\"foo\");\n   518:     /// let bytes = c_string.into_bytes_with_nul();\n   519:     /// assert_eq!(bytes, vec![b'f', b'o', b'o', b'\\0']);\n   520:     /// ```\n   521:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   522:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   523:     pub fn into_bytes_with_nul(self) -> Vec<u8> {\n   524:         self.into_inner().into_vec()\n   525:     }\n   526: \n   527:     /// Returns the contents of this `CString` as a slice of bytes.\n   528:     ///\n   529:     /// The returned slice does **not** contain the trailing nul\n   530:     /// terminator, and it is guaranteed to not have any interior nul\n   531:     /// bytes. If you need the nul terminator, use\n   532:     /// [`CString::as_bytes_with_nul`] instead.\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::ffi::CString;\n   538:     ///\n   539:     /// let c_string = CString::from(c\"foo\");",
    "nanvix_source": "   513:     ///\n   514:     /// ```\n   515:     /// use std::ffi::CString;\n   516:     ///\n   517:     /// let c_string = CString::from(c\"foo\");\n   518:     /// let bytes = c_string.into_bytes_with_nul();\n   519:     /// assert_eq!(bytes, vec![b'f', b'o', b'o', b'\\0']);\n   520:     /// ```\n   521:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   522:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   523:     pub fn into_bytes_with_nul(self) -> Vec<u8> {\n   524:         self.into_inner().into_vec()\n   525:     }\n   526: \n   527:     /// Returns the contents of this `CString` as a slice of bytes.\n   528:     ///\n   529:     /// The returned slice does **not** contain the trailing nul\n   530:     /// terminator, and it is guaranteed to not have any interior nul\n   531:     /// bytes. If you need the nul terminator, use\n   532:     /// [`CString::as_bytes_with_nul`] instead.\n   533:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::into_string",
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
      "name": "into_string",
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
            "id": 108,
            "path": "CString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3307",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:108",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "CString"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 119,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 3299,
                        "path": "IntoStringError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```\n   466:     /// use std::ffi::CString;\n   467:     ///\n   468:     /// let valid_utf8 = vec![b'f', b'o', b'o'];\n   469:     /// let cstring = CString::new(valid_utf8).expect(\"CString::new failed\");\n   470:     /// assert_eq!(cstring.into_string().expect(\"into_string() call failed\"), \"foo\");\n   471:     ///\n   472:     /// let invalid_utf8 = vec![b'f', 0xff, b'o', b'o'];\n   473:     /// let cstring = CString::new(invalid_utf8).expect(\"CString::new failed\");\n   474:     /// let err = cstring.into_string().err().expect(\"into_string().err() failed\");\n   475:     /// assert_eq!(err.utf8_error().valid_up_to(), 1);\n   476:     /// ```\n   477:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   478:     pub fn into_string(self) -> Result<String, IntoStringError> {\n   479:         String::from_utf8(self.into_bytes()).map_err(|e| IntoStringError {\n   480:             error: e.utf8_error(),\n   481:             inner: unsafe { Self::_from_vec_unchecked(e.into_bytes()) },\n   482:         })\n   483:     }\n   484: \n   485:     /// Consumes the `CString` and returns the underlying byte buffer.\n   486:     ///\n   487:     /// The returned buffer does **not** contain the trailing nul\n   488:     /// terminator, and it is guaranteed to not have any interior nul\n   489:     /// bytes.\n   490:     ///\n   491:     /// # Examples\n   492:     ///\n   493:     /// ```\n   494:     /// use std::ffi::CString;",
    "nanvix_source": "   468:     /// let valid_utf8 = vec![b'f', b'o', b'o'];\n   469:     /// let cstring = CString::new(valid_utf8).expect(\"CString::new failed\");\n   470:     /// assert_eq!(cstring.into_string().expect(\"into_string() call failed\"), \"foo\");\n   471:     ///\n   472:     /// let invalid_utf8 = vec![b'f', 0xff, b'o', b'o'];\n   473:     /// let cstring = CString::new(invalid_utf8).expect(\"CString::new failed\");\n   474:     /// let err = cstring.into_string().err().expect(\"into_string().err() failed\");\n   475:     /// assert_eq!(err.utf8_error().valid_up_to(), 1);\n   476:     /// ```\n   477:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   478:     pub fn into_string(self) -> Result<String, IntoStringError> {\n   479:         String::from_utf8(self.into_bytes()).map_err(|e| IntoStringError {\n   480:             error: e.utf8_error(),\n   481:             inner: unsafe { Self::_from_vec_unchecked(e.into_bytes()) },\n   482:         })\n   483:     }\n   484: \n   485:     /// Consumes the `CString` and returns the underlying byte buffer.\n   486:     ///\n   487:     /// The returned buffer does **not** contain the trailing nul\n   488:     /// terminator, and it is guaranteed to not have any interior nul",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::new",
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
                                    "args": {
                                      "angle_bracketed": {
                                        "args": [
                                          {
                                            "type": {
                                              "primitive": "u8"
                                            }
                                          }
                                        ],
                                        "constraints": []
                                      }
                                    },
                                    "id": 114,
                                    "path": "Vec"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 40,
                        "path": "Into"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
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
      "name": "new",
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
            "id": 108,
            "path": "CString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3307",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:108",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "CString"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "t",
            {
              "generic": "T"
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
                        "id": 108,
                        "path": "CString"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 3293,
                        "path": "NulError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   241:     /// use std::os::raw::c_char;\n   242:     ///\n   243:     /// extern \"C\" { fn puts(s: *const c_char); }\n   244:     ///\n   245:     /// let to_print = CString::new(\"Hello!\").expect(\"CString::new failed\");\n   246:     /// unsafe {\n   247:     ///     puts(to_print.as_ptr());\n   248:     /// }\n   249:     /// ```\n   250:     ///\n   251:     /// # Errors\n   252:     ///\n   253:     /// This function will return an error if the supplied bytes contain an\n   254:     /// internal 0 byte. The [`NulError`] returned will contain the bytes as well as\n   255:     /// the position of the nul byte.\n   256:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   257:     pub fn new<T: Into<Vec<u8>>>(t: T) -> Result<CString, NulError> {\n   258:         trait SpecNewImpl {\n   259:             fn spec_new_impl(self) -> Result<CString, NulError>;\n   260:         }\n   261: \n   262:         impl<T: Into<Vec<u8>>> SpecNewImpl for T {\n   263:             default fn spec_new_impl(self) -> Result<CString, NulError> {\n   264:                 let bytes: Vec<u8> = self.into();\n   265:                 match memchr::memchr(0, &bytes) {\n   266:                     Some(i) => Err(NulError(i, bytes)),\n   267:                     None => Ok(unsafe { CString::_from_vec_unchecked(bytes) }),\n   268:                 }\n   269:             }\n   270:         }\n   271: \n   272:         // Specialization for avoiding reallocation\n   273:         #[inline(always)] // Without that it is not inlined into specializations",
    "nanvix_source": "   247:     ///     puts(to_print.as_ptr());\n   248:     /// }\n   249:     /// ```\n   250:     ///\n   251:     /// # Errors\n   252:     ///\n   253:     /// This function will return an error if the supplied bytes contain an\n   254:     /// internal 0 byte. The [`NulError`] returned will contain the bytes as well as\n   255:     /// the position of the nul byte.\n   256:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   257:     pub fn new<T: Into<Vec<u8>>>(t: T) -> Result<CString, NulError> {\n   258:         trait SpecNewImpl {\n   259:             fn spec_new_impl(self) -> Result<CString, NulError>;\n   260:         }\n   261: \n   262:         impl<T: Into<Vec<u8>>> SpecNewImpl for T {\n   263:             default fn spec_new_impl(self) -> Result<CString, NulError> {\n   264:                 let bytes: Vec<u8> = self.into();\n   265:                 match memchr::memchr(0, &bytes) {\n   266:                     Some(i) => Err(NulError(i, bytes)),\n   267:                     None => Ok(unsafe { CString::_from_vec_unchecked(bytes) }),",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::FromVecWithNulError::as_bytes",
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
      "name": "as_bytes",
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
            "id": 3306,
            "path": "FromVecWithNulError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3415",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3306",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "FromVecWithNulError"
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
    "verification_source": "   166:     /// # Examples\n   167:     ///\n   168:     /// Basic usage:\n   169:     ///\n   170:     /// ```\n   171:     /// use std::ffi::CString;\n   172:     ///\n   173:     /// // Some invalid bytes in a vector\n   174:     /// let bytes = b\"f\\0oo\".to_vec();\n   175:     ///\n   176:     /// let value = CString::from_vec_with_nul(bytes.clone());\n   177:     ///\n   178:     /// assert_eq!(&bytes[..], value.unwrap_err().as_bytes());\n   179:     /// ```\n   180:     #[must_use]\n   181:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   182:     pub fn as_bytes(&self) -> &[u8] {\n   183:         &self.bytes[..]\n   184:     }\n   185: \n   186:     /// Returns the bytes that were attempted to convert to a [`CString`].\n   187:     ///\n   188:     /// This method is carefully constructed to avoid allocation. It will\n   189:     /// consume the error, moving out the bytes, so that a copy of the bytes\n   190:     /// does not need to be made.\n   191:     ///\n   192:     /// # Examples\n   193:     ///\n   194:     /// Basic usage:\n   195:     ///\n   196:     /// ```\n   197:     /// use std::ffi::CString;\n   198:     ///",
    "nanvix_source": "   172:     ///\n   173:     /// // Some invalid bytes in a vector\n   174:     /// let bytes = b\"f\\0oo\".to_vec();\n   175:     ///\n   176:     /// let value = CString::from_vec_with_nul(bytes.clone());\n   177:     ///\n   178:     /// assert_eq!(&bytes[..], value.unwrap_err().as_bytes());\n   179:     /// ```\n   180:     #[must_use]\n   181:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   182:     pub fn as_bytes(&self) -> &[u8] {\n   183:         &self.bytes[..]\n   184:     }\n   185: \n   186:     /// Returns the bytes that were attempted to convert to a [`CString`].\n   187:     ///\n   188:     /// This method is carefully constructed to avoid allocation. It will\n   189:     /// consume the error, moving out the bytes, so that a copy of the bytes\n   190:     /// does not need to be made.\n   191:     ///\n   192:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::FromVecWithNulError::into_bytes",
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
      "name": "into_bytes",
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
            "id": 3306,
            "path": "FromVecWithNulError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3415",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3306",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "FromVecWithNulError"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
          }
        }
      }
    },
    "verification_source": "   192:     /// # Examples\n   193:     ///\n   194:     /// Basic usage:\n   195:     ///\n   196:     /// ```\n   197:     /// use std::ffi::CString;\n   198:     ///\n   199:     /// // Some invalid bytes in a vector\n   200:     /// let bytes = b\"f\\0oo\".to_vec();\n   201:     ///\n   202:     /// let value = CString::from_vec_with_nul(bytes.clone());\n   203:     ///\n   204:     /// assert_eq!(bytes, value.unwrap_err().into_bytes());\n   205:     /// ```\n   206:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   207:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   208:     pub fn into_bytes(self) -> Vec<u8> {\n   209:         self.bytes\n   210:     }\n   211: }\n   212: \n   213: /// An error indicating invalid UTF-8 when converting a [`CString`] into a [`String`].\n   214: ///\n   215: /// `CString` is just a wrapper over a buffer of bytes with a nul terminator;\n   216: /// [`CString::into_string`] performs UTF-8 validation on those bytes and may\n   217: /// return this error.\n   218: ///\n   219: /// This `struct` is created by [`CString::into_string()`]. See\n   220: /// its documentation for more.\n   221: #[derive(Clone, PartialEq, Eq, Debug)]\n   222: #[stable(feature = \"alloc_c_string\", since = \"1.64.0\")]\n   223: pub struct IntoStringError {\n   224:     inner: CString,",
    "nanvix_source": "   198:     ///\n   199:     /// // Some invalid bytes in a vector\n   200:     /// let bytes = b\"f\\0oo\".to_vec();\n   201:     ///\n   202:     /// let value = CString::from_vec_with_nul(bytes.clone());\n   203:     ///\n   204:     /// assert_eq!(bytes, value.unwrap_err().into_bytes());\n   205:     /// ```\n   206:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   207:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   208:     pub fn into_bytes(self) -> Vec<u8> {\n   209:         self.bytes\n   210:     }\n   211: }\n   212: \n   213: /// An error indicating invalid UTF-8 when converting a [`CString`] into a [`String`].\n   214: ///\n   215: /// `CString` is just a wrapper over a buffer of bytes with a nul terminator;\n   216: /// [`CString::into_string`] performs UTF-8 validation on those bytes and may\n   217: /// return this error.\n   218: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::IntoStringError::into_cstring",
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
      "name": "into_cstring",
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
            "id": 3299,
            "path": "IntoStringError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3448",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3299",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "IntoStringError"
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
          "resolved_path": {
            "args": null,
            "id": 108,
            "path": "CString"
          }
        }
      }
    },
    "verification_source": "  1036:         match self.error_kind {\n  1037:             FromBytesWithNulErrorKind::InteriorNul(pos) => {\n  1038:                 write!(f, \"data provided contains an interior nul byte at pos {pos}\")\n  1039:             }\n  1040:             FromBytesWithNulErrorKind::NotNulTerminated => {\n  1041:                 write!(f, \"data provided is not nul terminated\")\n  1042:             }\n  1043:         }\n  1044:     }\n  1045: }\n  1046: \n  1047: impl IntoStringError {\n  1048:     /// Consumes this error, returning original [`CString`] which generated the\n  1049:     /// error.\n  1050:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1051:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1052:     pub fn into_cstring(self) -> CString {\n  1053:         self.inner\n  1054:     }\n  1055: \n  1056:     /// Access the underlying UTF-8 error that was the cause of this error.\n  1057:     #[must_use]\n  1058:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1059:     pub fn utf8_error(&self) -> Utf8Error {\n  1060:         self.error\n  1061:     }\n  1062: }\n  1063: \n  1064: #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1065: impl fmt::Display for IntoStringError {\n  1066:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1067:         \"C string contained non-utf8 bytes\".fmt(f)\n  1068:     }",
    "nanvix_source": "  1042:             }\n  1043:         }\n  1044:     }\n  1045: }\n  1046: \n  1047: impl IntoStringError {\n  1048:     /// Consumes this error, returning original [`CString`] which generated the\n  1049:     /// error.\n  1050:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1051:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1052:     pub fn into_cstring(self) -> CString {\n  1053:         self.inner\n  1054:     }\n  1055: \n  1056:     /// Access the underlying UTF-8 error that was the cause of this error.\n  1057:     #[must_use]\n  1058:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1059:     pub fn utf8_error(&self) -> Utf8Error {\n  1060:         self.error\n  1061:     }\n  1062: }",
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
