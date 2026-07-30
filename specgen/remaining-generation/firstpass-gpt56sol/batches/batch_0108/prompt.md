For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::ffi::CString::as_bytes",
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
    "verification_source": "   530:     /// terminator, and it is guaranteed to not have any interior nul\n   531:     /// bytes. If you need the nul terminator, use\n   532:     /// [`CString::as_bytes_with_nul`] instead.\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::ffi::CString;\n   538:     ///\n   539:     /// let c_string = CString::from(c\"foo\");\n   540:     /// let bytes = c_string.as_bytes();\n   541:     /// assert_eq!(bytes, &[b'f', b'o', b'o']);\n   542:     /// ```\n   543:     #[inline]\n   544:     #[must_use]\n   545:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   546:     pub fn as_bytes(&self) -> &[u8] {\n   547:         // SAFETY: CString has a length at least 1\n   548:         unsafe { self.inner.get_unchecked(..self.inner.len() - 1) }\n   549:     }\n   550: \n   551:     /// Equivalent to [`CString::as_bytes()`] except that the\n   552:     /// returned slice includes the trailing nul terminator.\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```\n   557:     /// use std::ffi::CString;\n   558:     ///\n   559:     /// let c_string = CString::from(c\"foo\");\n   560:     /// let bytes = c_string.as_bytes_with_nul();\n   561:     /// assert_eq!(bytes, &[b'f', b'o', b'o', b'\\0']);\n   562:     /// ```",
    "nanvix_source": "   536:     /// ```\n   537:     /// use std::ffi::CString;\n   538:     ///\n   539:     /// let c_string = CString::from(c\"foo\");\n   540:     /// let bytes = c_string.as_bytes();\n   541:     /// assert_eq!(bytes, &[b'f', b'o', b'o']);\n   542:     /// ```\n   543:     #[inline]\n   544:     #[must_use]\n   545:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   546:     pub fn as_bytes(&self) -> &[u8] {\n   547:         // SAFETY: CString has a length at least 1\n   548:         unsafe { self.inner.get_unchecked(..self.inner.len() - 1) }\n   549:     }\n   550: \n   551:     /// Equivalent to [`CString::as_bytes()`] except that the\n   552:     /// returned slice includes the trailing nul terminator.\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::as_bytes_with_nul",
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
      "name": "as_bytes_with_nul",
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
    "verification_source": "   550: \n   551:     /// Equivalent to [`CString::as_bytes()`] except that the\n   552:     /// returned slice includes the trailing nul terminator.\n   553:     ///\n   554:     /// # Examples\n   555:     ///\n   556:     /// ```\n   557:     /// use std::ffi::CString;\n   558:     ///\n   559:     /// let c_string = CString::from(c\"foo\");\n   560:     /// let bytes = c_string.as_bytes_with_nul();\n   561:     /// assert_eq!(bytes, &[b'f', b'o', b'o', b'\\0']);\n   562:     /// ```\n   563:     #[inline]\n   564:     #[must_use]\n   565:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   566:     pub fn as_bytes_with_nul(&self) -> &[u8] {\n   567:         &self.inner\n   568:     }\n   569: \n   570:     /// Extracts a [`CStr`] slice containing the entire string.\n   571:     ///\n   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// use std::ffi::{CString, CStr};\n   576:     ///\n   577:     /// let c_string = CString::from(c\"foo\");\n   578:     /// let cstr = c_string.as_c_str();\n   579:     /// assert_eq!(cstr,\n   580:     ///            CStr::from_bytes_with_nul(b\"foo\\0\").expect(\"CStr::from_bytes_with_nul failed\"));\n   581:     /// ```\n   582:     #[inline]",
    "nanvix_source": "   556:     /// ```\n   557:     /// use std::ffi::CString;\n   558:     ///\n   559:     /// let c_string = CString::from(c\"foo\");\n   560:     /// let bytes = c_string.as_bytes_with_nul();\n   561:     /// assert_eq!(bytes, &[b'f', b'o', b'o', b'\\0']);\n   562:     /// ```\n   563:     #[inline]\n   564:     #[must_use]\n   565:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   566:     pub fn as_bytes_with_nul(&self) -> &[u8] {\n   567:         &self.inner\n   568:     }\n   569: \n   570:     /// Extracts a [`CStr`] slice containing the entire string.\n   571:     ///\n   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// use std::ffi::{CString, CStr};\n   576:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::as_c_str",
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
      "name": "as_c_str",
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
                "id": 112,
                "path": "CStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   570:     /// Extracts a [`CStr`] slice containing the entire string.\n   571:     ///\n   572:     /// # Examples\n   573:     ///\n   574:     /// ```\n   575:     /// use std::ffi::{CString, CStr};\n   576:     ///\n   577:     /// let c_string = CString::from(c\"foo\");\n   578:     /// let cstr = c_string.as_c_str();\n   579:     /// assert_eq!(cstr,\n   580:     ///            CStr::from_bytes_with_nul(b\"foo\\0\").expect(\"CStr::from_bytes_with_nul failed\"));\n   581:     /// ```\n   582:     #[inline]\n   583:     #[must_use]\n   584:     #[stable(feature = \"as_c_str\", since = \"1.20.0\")]\n   585:     #[rustc_diagnostic_item = \"cstring_as_c_str\"]\n   586:     pub fn as_c_str(&self) -> &CStr {\n   587:         unsafe { CStr::from_bytes_with_nul_unchecked(self.as_bytes_with_nul()) }\n   588:     }\n   589: \n   590:     /// Converts this `CString` into a boxed [`CStr`].\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// let c_string = c\"foo\".to_owned();\n   596:     /// let boxed = c_string.into_boxed_c_str();\n   597:     /// assert_eq!(boxed.to_bytes_with_nul(), b\"foo\\0\");\n   598:     /// ```\n   599:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   600:     #[stable(feature = \"into_boxed_c_str\", since = \"1.20.0\")]\n   601:     pub fn into_boxed_c_str(self) -> Box<CStr> {\n   602:         unsafe { Box::from_raw(Box::into_raw(self.into_inner()) as *mut CStr) }",
    "nanvix_source": "   576:     ///\n   577:     /// let c_string = CString::from(c\"foo\");\n   578:     /// let cstr = c_string.as_c_str();\n   579:     /// assert_eq!(cstr,\n   580:     ///            CStr::from_bytes_with_nul(b\"foo\\0\").expect(\"CStr::from_bytes_with_nul failed\"));\n   581:     /// ```\n   582:     #[inline]\n   583:     #[must_use]\n   584:     #[stable(feature = \"as_c_str\", since = \"1.20.0\")]\n   585:     #[rustc_diagnostic_item = \"cstring_as_c_str\"]\n   586:     pub fn as_c_str(&self) -> &CStr {\n   587:         unsafe { CStr::from_bytes_with_nul_unchecked(self.as_bytes_with_nul()) }\n   588:     }\n   589: \n   590:     /// Converts this `CString` into a boxed [`CStr`].\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// let c_string = c\"foo\".to_owned();\n   596:     /// let boxed = c_string.into_boxed_c_str();",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::from_vec_with_nul",
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
      "name": "from_vec_with_nul",
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
            "v",
            {
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
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 3306,
                        "path": "FromVecWithNulError"
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
    "verification_source": "   662:     ///     CString::from_vec_with_nul(b\"abc\\0\".to_vec())\n   663:     ///         .expect(\"CString::from_vec_with_nul failed\"),\n   664:     ///     c\"abc\".to_owned()\n   665:     /// );\n   666:     /// ```\n   667:     ///\n   668:     /// An incorrectly formatted [`Vec`] will produce an error.\n   669:     ///\n   670:     /// ```\n   671:     /// use std::ffi::{CString, FromVecWithNulError};\n   672:     /// // Interior nul byte\n   673:     /// let _: FromVecWithNulError = CString::from_vec_with_nul(b\"a\\0bc\".to_vec()).unwrap_err();\n   674:     /// // No nul byte\n   675:     /// let _: FromVecWithNulError = CString::from_vec_with_nul(b\"abc\".to_vec()).unwrap_err();\n   676:     /// ```\n   677:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   678:     pub fn from_vec_with_nul(v: Vec<u8>) -> Result<Self, FromVecWithNulError> {\n   679:         let nul_pos = memchr::memchr(0, &v);\n   680:         match nul_pos {\n   681:             Some(nul_pos) if nul_pos + 1 == v.len() => {\n   682:                 // SAFETY: We know there is only one nul byte, at the end\n   683:                 // of the vec.\n   684:                 Ok(unsafe { Self::_from_vec_with_nul_unchecked(v) })\n   685:             }\n   686:             Some(nul_pos) => Err(FromVecWithNulError {\n   687:                 error_kind: FromBytesWithNulErrorKind::InteriorNul(nul_pos),\n   688:                 bytes: v,\n   689:             }),\n   690:             None => Err(FromVecWithNulError {\n   691:                 error_kind: FromBytesWithNulErrorKind::NotNulTerminated,\n   692:                 bytes: v,\n   693:             }),\n   694:         }",
    "nanvix_source": "   668:     /// An incorrectly formatted [`Vec`] will produce an error.\n   669:     ///\n   670:     /// ```\n   671:     /// use std::ffi::{CString, FromVecWithNulError};\n   672:     /// // Interior nul byte\n   673:     /// let _: FromVecWithNulError = CString::from_vec_with_nul(b\"a\\0bc\".to_vec()).unwrap_err();\n   674:     /// // No nul byte\n   675:     /// let _: FromVecWithNulError = CString::from_vec_with_nul(b\"abc\".to_vec()).unwrap_err();\n   676:     /// ```\n   677:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   678:     pub fn from_vec_with_nul(v: Vec<u8>) -> Result<Self, FromVecWithNulError> {\n   679:         let nul_pos = memchr::memchr(0, &v);\n   680:         match nul_pos {\n   681:             Some(nul_pos) if nul_pos + 1 == v.len() => {\n   682:                 // SAFETY: We know there is only one nul byte, at the end\n   683:                 // of the vec.\n   684:                 Ok(unsafe { Self::_from_vec_with_nul_unchecked(v) })\n   685:             }\n   686:             Some(nul_pos) => Err(FromVecWithNulError {\n   687:                 error_kind: FromBytesWithNulErrorKind::InteriorNul(nul_pos),\n   688:                 bytes: v,",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::into_boxed_c_str",
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
      "name": "into_boxed_c_str",
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
                        "id": 112,
                        "path": "CStr"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "   585:     #[rustc_diagnostic_item = \"cstring_as_c_str\"]\n   586:     pub fn as_c_str(&self) -> &CStr {\n   587:         unsafe { CStr::from_bytes_with_nul_unchecked(self.as_bytes_with_nul()) }\n   588:     }\n   589: \n   590:     /// Converts this `CString` into a boxed [`CStr`].\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// let c_string = c\"foo\".to_owned();\n   596:     /// let boxed = c_string.into_boxed_c_str();\n   597:     /// assert_eq!(boxed.to_bytes_with_nul(), b\"foo\\0\");\n   598:     /// ```\n   599:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   600:     #[stable(feature = \"into_boxed_c_str\", since = \"1.20.0\")]\n   601:     pub fn into_boxed_c_str(self) -> Box<CStr> {\n   602:         unsafe { Box::from_raw(Box::into_raw(self.into_inner()) as *mut CStr) }\n   603:     }\n   604: \n   605:     /// Bypass \"move out of struct which implements [`Drop`] trait\" restriction.\n   606:     #[inline]\n   607:     fn into_inner(self) -> Box<[u8]> {\n   608:         // Rationale: `mem::forget(self)` invalidates the previous call to `ptr::read(&self.inner)`\n   609:         // so we use `ManuallyDrop` to ensure `self` is not dropped.\n   610:         // Then we can return the box directly without invalidating it.\n   611:         // See https://github.com/rust-lang/rust/issues/62553.\n   612:         let this = mem::ManuallyDrop::new(self);\n   613:         unsafe { ptr::read(&this.inner) }\n   614:     }\n   615: \n   616:     /// Converts a <code>[Vec]<[u8]></code> to a [`CString`] without checking the\n   617:     /// invariants on the given [`Vec`].",
    "nanvix_source": "   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// let c_string = c\"foo\".to_owned();\n   596:     /// let boxed = c_string.into_boxed_c_str();\n   597:     /// assert_eq!(boxed.to_bytes_with_nul(), b\"foo\\0\");\n   598:     /// ```\n   599:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   600:     #[stable(feature = \"into_boxed_c_str\", since = \"1.20.0\")]\n   601:     pub fn into_boxed_c_str(self) -> Box<CStr> {\n   602:         unsafe { Box::from_raw(Box::into_raw(self.into_inner()) as *mut CStr) }\n   603:     }\n   604: \n   605:     /// Bypass \"move out of struct which implements [`Drop`] trait\" restriction.\n   606:     #[inline]\n   607:     fn into_inner(self) -> Box<[u8]> {\n   608:         // Rationale: `mem::forget(self)` invalidates the previous call to `ptr::read(&self.inner)`\n   609:         // so we use `ManuallyDrop` to ensure `self` is not dropped.\n   610:         // Then we can return the box directly without invalidating it.\n   611:         // See https://github.com/rust-lang/rust/issues/62553.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::into_bytes",
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
    "verification_source": "   486:     ///\n   487:     /// The returned buffer does **not** contain the trailing nul\n   488:     /// terminator, and it is guaranteed to not have any interior nul\n   489:     /// bytes.\n   490:     ///\n   491:     /// # Examples\n   492:     ///\n   493:     /// ```\n   494:     /// use std::ffi::CString;\n   495:     ///\n   496:     /// let c_string = CString::from(c\"foo\");\n   497:     /// let bytes = c_string.into_bytes();\n   498:     /// assert_eq!(bytes, vec![b'f', b'o', b'o']);\n   499:     /// ```\n   500:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   501:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   502:     pub fn into_bytes(self) -> Vec<u8> {\n   503:         let mut vec = self.into_inner().into_vec();\n   504:         let _nul = vec.pop();\n   505:         debug_assert_eq!(_nul, Some(0u8));\n   506:         vec\n   507:     }\n   508: \n   509:     /// Equivalent to [`CString::into_bytes()`] except that the\n   510:     /// returned vector includes the trailing nul terminator.\n   511:     ///\n   512:     /// # Examples\n   513:     ///\n   514:     /// ```\n   515:     /// use std::ffi::CString;\n   516:     ///\n   517:     /// let c_string = CString::from(c\"foo\");\n   518:     /// let bytes = c_string.into_bytes_with_nul();",
    "nanvix_source": "   492:     ///\n   493:     /// ```\n   494:     /// use std::ffi::CString;\n   495:     ///\n   496:     /// let c_string = CString::from(c\"foo\");\n   497:     /// let bytes = c_string.into_bytes();\n   498:     /// assert_eq!(bytes, vec![b'f', b'o', b'o']);\n   499:     /// ```\n   500:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   501:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n   502:     pub fn into_bytes(self) -> Vec<u8> {\n   503:         let mut vec = self.into_inner().into_vec();\n   504:         let _nul = vec.pop();\n   505:         debug_assert_eq!(_nul, Some(0u8));\n   506:         vec\n   507:     }\n   508: \n   509:     /// Equivalent to [`CString::into_bytes()`] except that the\n   510:     /// returned vector includes the trailing nul terminator.\n   511:     ///\n   512:     /// # Examples",
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
