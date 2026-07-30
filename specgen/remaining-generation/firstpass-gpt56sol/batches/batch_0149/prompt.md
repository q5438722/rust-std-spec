For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::ffi::OsString::clear",
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
      "name": "clear",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   315: \n   316:     /// Truncates the `OsString` to zero length.\n   317:     ///\n   318:     /// # Examples\n   319:     ///\n   320:     /// ```\n   321:     /// use std::ffi::OsString;\n   322:     ///\n   323:     /// let mut os_string = OsString::from(\"foo\");\n   324:     /// assert_eq!(&os_string, \"foo\");\n   325:     ///\n   326:     /// os_string.clear();\n   327:     /// assert_eq!(&os_string, \"\");\n   328:     /// ```\n   329:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   330:     #[inline]\n   331:     pub fn clear(&mut self) {\n   332:         self.inner.clear()\n   333:     }\n   334: \n   335:     /// Returns the capacity this `OsString` can hold without reallocating.\n   336:     ///\n   337:     /// See the main `OsString` documentation information about encoding and capacity units.\n   338:     ///\n   339:     /// # Examples\n   340:     ///\n   341:     /// ```\n   342:     /// use std::ffi::OsString;\n   343:     ///\n   344:     /// let os_string = OsString::with_capacity(10);\n   345:     /// assert!(os_string.capacity() >= 10);\n   346:     /// ```\n   347:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]",
    "nanvix_source": "   313:     /// use std::ffi::OsString;\n   314:     ///\n   315:     /// let mut os_string = OsString::from(\"foo\");\n   316:     /// assert_eq!(&os_string, \"foo\");\n   317:     ///\n   318:     /// os_string.clear();\n   319:     /// assert_eq!(&os_string, \"\");\n   320:     /// ```\n   321:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   322:     #[inline]\n   323:     pub fn clear(&mut self) {\n   324:         self.inner.clear()\n   325:     }\n   326: \n   327:     /// Returns the capacity this `OsString` can hold without reallocating.\n   328:     ///\n   329:     /// See the main `OsString` documentation information about encoding and capacity units.\n   330:     ///\n   331:     /// # Examples\n   332:     ///\n   333:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::into_boxed_os_str",
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
      "name": "into_boxed_os_str",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
                        "id": 1857,
                        "path": "OsStr"
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
      }
    },
    "verification_source": "   537:         self.inner.shrink_to(min_capacity)\n   538:     }\n   539: \n   540:     /// Converts this `OsString` into a boxed [`OsStr`].\n   541:     ///\n   542:     /// # Examples\n   543:     ///\n   544:     /// ```\n   545:     /// use std::ffi::{OsString, OsStr};\n   546:     ///\n   547:     /// let s = OsString::from(\"hello\");\n   548:     ///\n   549:     /// let b: Box<OsStr> = s.into_boxed_os_str();\n   550:     /// ```\n   551:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   552:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n   553:     pub fn into_boxed_os_str(self) -> Box<OsStr> {\n   554:         let rw = Box::into_raw(self.inner.into_box()) as *mut OsStr;\n   555:         unsafe { Box::from_raw(rw) }\n   556:     }\n   557: \n   558:     /// Consumes and leaks the `OsString`, returning a mutable reference to the contents,\n   559:     /// `&'a mut OsStr`.\n   560:     ///\n   561:     /// The caller has free choice over the returned lifetime, including 'static.\n   562:     /// Indeed, this function is ideally used for data that lives for the remainder of\n   563:     /// the program\u2019s life, as dropping the returned reference will cause a memory leak.\n   564:     ///\n   565:     /// It does not reallocate or shrink the `OsString`, so the leaked allocation may include\n   566:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n   567:     /// capacity, call [`into_boxed_os_str`], and then [`Box::leak`] instead.\n   568:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n   569:     ///",
    "nanvix_source": "   535:     ///\n   536:     /// ```\n   537:     /// use std::ffi::{OsString, OsStr};\n   538:     ///\n   539:     /// let s = OsString::from(\"hello\");\n   540:     ///\n   541:     /// let b: Box<OsStr> = s.into_boxed_os_str();\n   542:     /// ```\n   543:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   544:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n   545:     pub fn into_boxed_os_str(self) -> Box<OsStr> {\n   546:         let rw = Box::into_raw(self.inner.into_box()) as *mut OsStr;\n   547:         unsafe { Box::from_raw(rw) }\n   548:     }\n   549: \n   550:     /// Consumes and leaks the `OsString`, returning a mutable reference to the contents,\n   551:     /// `&'a mut OsStr`.\n   552:     ///\n   553:     /// The caller has free choice over the returned lifetime, including 'static.\n   554:     /// Indeed, this function is ideally used for data that lives for the remainder of\n   555:     /// the program\u2019s life, as dropping the returned reference will cause a memory leak.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::into_encoded_bytes",
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
      "name": "into_encoded_bytes",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
            "id": 222,
            "path": "Vec"
          }
        }
      }
    },
    "verification_source": "   207:     /// Converts the `OsString` into a byte vector.  To convert the byte vector back into an\n   208:     /// `OsString`, use the [`OsString::from_encoded_bytes_unchecked`] function.\n   209:     ///\n   210:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   211:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   212:     /// ASCII.\n   213:     ///\n   214:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n   215:     /// be treated as opaque and only comparable within the same Rust version built for the same\n   216:     /// target platform.  For example, sending the bytes over the network or storing it in a file\n   217:     /// will likely result in incompatible data.  See [`OsString`] for more encoding details\n   218:     /// and [`std::ffi`] for platform-specific, specified conversions.\n   219:     ///\n   220:     /// [`std::ffi`]: crate::ffi\n   221:     #[inline]\n   222:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   223:     pub fn into_encoded_bytes(self) -> Vec<u8> {\n   224:         self.inner.into_encoded_bytes()\n   225:     }\n   226: \n   227:     /// Converts the `OsString` into a [`String`] if it contains valid Unicode data.\n   228:     ///\n   229:     /// On failure, ownership of the original `OsString` is returned.\n   230:     ///\n   231:     /// # Examples\n   232:     ///\n   233:     /// ```\n   234:     /// use std::ffi::OsString;\n   235:     ///\n   236:     /// let os_string = OsString::from(\"foo\");\n   237:     /// let string = os_string.into_string();\n   238:     /// assert_eq!(string, Ok(String::from(\"foo\")));\n   239:     /// ```",
    "nanvix_source": "   205:     ///\n   206:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n   207:     /// be treated as opaque and only comparable within the same Rust version built for the same\n   208:     /// target platform.  For example, sending the bytes over the network or storing it in a file\n   209:     /// will likely result in incompatible data.  See [`OsString`] for more encoding details\n   210:     /// and [`std::ffi`] for platform-specific, specified conversions.\n   211:     ///\n   212:     /// [`std::ffi`]: crate::ffi\n   213:     #[inline]\n   214:     #[stable(feature = \"os_str_bytes\", since = \"1.74.0\")]\n   215:     pub fn into_encoded_bytes(self) -> Vec<u8> {\n   216:         self.inner.into_encoded_bytes()\n   217:     }\n   218: \n   219:     /// Converts the `OsString` into a [`String`] if it contains valid Unicode data.\n   220:     ///\n   221:     /// On failure, ownership of the original `OsString` is returned.\n   222:     ///\n   223:     /// # Examples\n   224:     ///\n   225:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::into_string",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
                        "id": 218,
                        "path": "String"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1846,
                        "path": "OsString"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   226: \n   227:     /// Converts the `OsString` into a [`String`] if it contains valid Unicode data.\n   228:     ///\n   229:     /// On failure, ownership of the original `OsString` is returned.\n   230:     ///\n   231:     /// # Examples\n   232:     ///\n   233:     /// ```\n   234:     /// use std::ffi::OsString;\n   235:     ///\n   236:     /// let os_string = OsString::from(\"foo\");\n   237:     /// let string = os_string.into_string();\n   238:     /// assert_eq!(string, Ok(String::from(\"foo\")));\n   239:     /// ```\n   240:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   241:     #[inline]\n   242:     pub fn into_string(self) -> Result<String, OsString> {\n   243:         self.inner.into_string().map_err(|buf| OsString { inner: buf })\n   244:     }\n   245: \n   246:     /// Extends the string with the given <code>&[OsStr]</code> slice.\n   247:     ///\n   248:     /// # Examples\n   249:     ///\n   250:     /// ```\n   251:     /// use std::ffi::OsString;\n   252:     ///\n   253:     /// let mut os_string = OsString::from(\"foo\");\n   254:     /// os_string.push(\"bar\");\n   255:     /// assert_eq!(&os_string, \"foobar\");\n   256:     /// ```\n   257:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   258:     #[inline]",
    "nanvix_source": "   224:     ///\n   225:     /// ```\n   226:     /// use std::ffi::OsString;\n   227:     ///\n   228:     /// let os_string = OsString::from(\"foo\");\n   229:     /// let string = os_string.into_string();\n   230:     /// assert_eq!(string, Ok(String::from(\"foo\")));\n   231:     /// ```\n   232:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   233:     #[inline]\n   234:     pub fn into_string(self) -> Result<String, OsString> {\n   235:         self.inner.into_string().map_err(|buf| OsString { inner: buf })\n   236:     }\n   237: \n   238:     /// Extends the string with the given <code>&[OsStr]</code> slice.\n   239:     ///\n   240:     /// # Examples\n   241:     ///\n   242:     /// ```\n   243:     /// use std::ffi::OsString;\n   244:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::new",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
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
    "verification_source": "   125: impl crate::sealed::Sealed for OsStr {}\n   126: \n   127: impl OsString {\n   128:     /// Constructs a new empty `OsString`.\n   129:     ///\n   130:     /// # Examples\n   131:     ///\n   132:     /// ```\n   133:     /// use std::ffi::OsString;\n   134:     ///\n   135:     /// let os_string = OsString::new();\n   136:     /// ```\n   137:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   138:     #[must_use]\n   139:     #[inline]\n   140:     #[rustc_const_stable(feature = \"const_pathbuf_osstring_new\", since = \"1.91.0\")]\n   141:     pub const fn new() -> OsString {\n   142:         OsString { inner: Buf::from_string(String::new()) }\n   143:     }\n   144: \n   145:     /// Converts bytes to an `OsString` without checking that the bytes contains\n   146:     /// valid [`OsStr`]-encoded data.\n   147:     ///\n   148:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   149:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   150:     /// ASCII.\n   151:     ///\n   152:     /// See the [module's toplevel documentation about conversions][conversions] for safe,\n   153:     /// cross-platform [conversions] from/to native representations.\n   154:     ///\n   155:     /// # Safety\n   156:     ///\n   157:     /// As the encoding is unspecified, callers must pass in bytes that originated as a mixture of",
    "nanvix_source": "   123:     ///\n   124:     /// ```\n   125:     /// use std::ffi::OsString;\n   126:     ///\n   127:     /// let os_string = OsString::new();\n   128:     /// ```\n   129:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   130:     #[must_use]\n   131:     #[inline]\n   132:     #[rustc_const_stable(feature = \"const_pathbuf_osstring_new\", since = \"1.91.0\")]\n   133:     pub const fn new() -> OsString {\n   134:         OsString { inner: Buf::from_string(String::new()) }\n   135:     }\n   136: \n   137:     /// Converts bytes to an `OsString` without checking that the bytes contains\n   138:     /// valid [`OsStr`]-encoded data.\n   139:     ///\n   140:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   141:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   142:     /// ASCII.\n   143:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::push",
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
      "unit_return_variant"
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
      "name": "push",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
            "s",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   244:     }\n   245: \n   246:     /// Extends the string with the given <code>&[OsStr]</code> slice.\n   247:     ///\n   248:     /// # Examples\n   249:     ///\n   250:     /// ```\n   251:     /// use std::ffi::OsString;\n   252:     ///\n   253:     /// let mut os_string = OsString::from(\"foo\");\n   254:     /// os_string.push(\"bar\");\n   255:     /// assert_eq!(&os_string, \"foobar\");\n   256:     /// ```\n   257:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   258:     #[inline]\n   259:     #[rustc_confusables(\"append\", \"put\")]\n   260:     pub fn push<T: AsRef<OsStr>>(&mut self, s: T) {\n   261:         trait SpecPushTo {\n   262:             fn spec_push_to(&self, buf: &mut OsString);\n   263:         }\n   264: \n   265:         impl<T: AsRef<OsStr>> SpecPushTo for T {\n   266:             #[inline]\n   267:             default fn spec_push_to(&self, buf: &mut OsString) {\n   268:                 buf.inner.push_slice(&self.as_ref().inner);\n   269:             }\n   270:         }\n   271: \n   272:         // Use a more efficient implementation when the string is UTF-8.\n   273:         macro spec_str($T:ty) {\n   274:             impl SpecPushTo for $T {\n   275:                 #[inline]\n   276:                 fn spec_push_to(&self, buf: &mut OsString) {",
    "nanvix_source": "   242:     /// ```\n   243:     /// use std::ffi::OsString;\n   244:     ///\n   245:     /// let mut os_string = OsString::from(\"foo\");\n   246:     /// os_string.push(\"bar\");\n   247:     /// assert_eq!(&os_string, \"foobar\");\n   248:     /// ```\n   249:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   250:     #[inline]\n   251:     #[rustc_confusables(\"append\", \"put\")]\n   252:     pub fn push<T: AsRef<OsStr>>(&mut self, s: T) {\n   253:         trait SpecPushTo {\n   254:             fn spec_push_to(&self, buf: &mut OsString);\n   255:         }\n   256: \n   257:         impl<T: AsRef<OsStr>> SpecPushTo for T {\n   258:             #[inline]\n   259:             default fn spec_push_to(&self, buf: &mut OsString) {\n   260:                 buf.inner.push_slice(&self.as_ref().inner);\n   261:             }\n   262:         }",
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
