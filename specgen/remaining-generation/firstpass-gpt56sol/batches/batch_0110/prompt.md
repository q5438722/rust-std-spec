For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::ffi::IntoStringError::utf8_error",
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
      "name": "utf8_error",
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
            "id": 967,
            "path": "Utf8Error"
          }
        }
      }
    },
    "verification_source": "  1043:         }\n  1044:     }\n  1045: }\n  1046: \n  1047: impl IntoStringError {\n  1048:     /// Consumes this error, returning original [`CString`] which generated the\n  1049:     /// error.\n  1050:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1051:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1052:     pub fn into_cstring(self) -> CString {\n  1053:         self.inner\n  1054:     }\n  1055: \n  1056:     /// Access the underlying UTF-8 error that was the cause of this error.\n  1057:     #[must_use]\n  1058:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1059:     pub fn utf8_error(&self) -> Utf8Error {\n  1060:         self.error\n  1061:     }\n  1062: }\n  1063: \n  1064: #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1065: impl fmt::Display for IntoStringError {\n  1066:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1067:         \"C string contained non-utf8 bytes\".fmt(f)\n  1068:     }\n  1069: }\n  1070: \n  1071: #[stable(feature = \"cstr_borrow\", since = \"1.3.0\")]\n  1072: impl ToOwned for CStr {\n  1073:     type Owned = CString;\n  1074: \n  1075:     fn to_owned(&self) -> CString {",
    "nanvix_source": "  1049:     /// error.\n  1050:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1051:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1052:     pub fn into_cstring(self) -> CString {\n  1053:         self.inner\n  1054:     }\n  1055: \n  1056:     /// Access the underlying UTF-8 error that was the cause of this error.\n  1057:     #[must_use]\n  1058:     #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1059:     pub fn utf8_error(&self) -> Utf8Error {\n  1060:         self.error\n  1061:     }\n  1062: }\n  1063: \n  1064: #[stable(feature = \"cstring_into\", since = \"1.7.0\")]\n  1065: impl fmt::Display for IntoStringError {\n  1066:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1067:         \"C string contained non-utf8 bytes\".fmt(f)\n  1068:     }\n  1069: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::NulError::into_vec",
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
      "name": "into_vec",
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
            "id": 3293,
            "path": "NulError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3382",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3293",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "NulError"
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
    "verification_source": "  1005:         self.0\n  1006:     }\n  1007: \n  1008:     /// Consumes this error, returning the underlying vector of bytes which\n  1009:     /// generated the error in the first place.\n  1010:     ///\n  1011:     /// # Examples\n  1012:     ///\n  1013:     /// ```\n  1014:     /// use std::ffi::CString;\n  1015:     ///\n  1016:     /// let nul_error = CString::new(\"foo\\0bar\").unwrap_err();\n  1017:     /// assert_eq!(nul_error.into_vec(), b\"foo\\0bar\");\n  1018:     /// ```\n  1019:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1020:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1021:     pub fn into_vec(self) -> Vec<u8> {\n  1022:         self.1\n  1023:     }\n  1024: }\n  1025: \n  1026: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1027: impl fmt::Display for NulError {\n  1028:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1029:         write!(f, \"nul byte found in provided data at position: {}\", self.0)\n  1030:     }\n  1031: }\n  1032: \n  1033: #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n  1034: impl fmt::Display for FromVecWithNulError {\n  1035:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1036:         match self.error_kind {\n  1037:             FromBytesWithNulErrorKind::InteriorNul(pos) => {",
    "nanvix_source": "  1011:     /// # Examples\n  1012:     ///\n  1013:     /// ```\n  1014:     /// use std::ffi::CString;\n  1015:     ///\n  1016:     /// let nul_error = CString::new(\"foo\\0bar\").unwrap_err();\n  1017:     /// assert_eq!(nul_error.into_vec(), b\"foo\\0bar\");\n  1018:     /// ```\n  1019:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1020:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1021:     pub fn into_vec(self) -> Vec<u8> {\n  1022:         self.1\n  1023:     }\n  1024: }\n  1025: \n  1026: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1027: impl fmt::Display for NulError {\n  1028:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  1029:         write!(f, \"nul byte found in provided data at position: {}\", self.0)\n  1030:     }\n  1031: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::NulError::nul_position",
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
      "name": "nul_position",
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
            "id": 3293,
            "path": "NulError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3382",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3293",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "NulError"
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
    "verification_source": "   988:     /// Returns the position of the nul byte in the slice that caused\n   989:     /// [`CString::new`] to fail.\n   990:     ///\n   991:     /// # Examples\n   992:     ///\n   993:     /// ```\n   994:     /// use std::ffi::CString;\n   995:     ///\n   996:     /// let nul_error = CString::new(\"foo\\0bar\").unwrap_err();\n   997:     /// assert_eq!(nul_error.nul_position(), 3);\n   998:     ///\n   999:     /// let nul_error = CString::new(\"foo bar\\0\").unwrap_err();\n  1000:     /// assert_eq!(nul_error.nul_position(), 7);\n  1001:     /// ```\n  1002:     #[must_use]\n  1003:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1004:     pub fn nul_position(&self) -> usize {\n  1005:         self.0\n  1006:     }\n  1007: \n  1008:     /// Consumes this error, returning the underlying vector of bytes which\n  1009:     /// generated the error in the first place.\n  1010:     ///\n  1011:     /// # Examples\n  1012:     ///\n  1013:     /// ```\n  1014:     /// use std::ffi::CString;\n  1015:     ///\n  1016:     /// let nul_error = CString::new(\"foo\\0bar\").unwrap_err();\n  1017:     /// assert_eq!(nul_error.into_vec(), b\"foo\\0bar\");\n  1018:     /// ```\n  1019:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1020:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   994:     /// use std::ffi::CString;\n   995:     ///\n   996:     /// let nul_error = CString::new(\"foo\\0bar\").unwrap_err();\n   997:     /// assert_eq!(nul_error.nul_position(), 3);\n   998:     ///\n   999:     /// let nul_error = CString::new(\"foo bar\\0\").unwrap_err();\n  1000:     /// assert_eq!(nul_error.nul_position(), 7);\n  1001:     /// ```\n  1002:     #[must_use]\n  1003:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1004:     pub fn nul_position(&self) -> usize {\n  1005:         self.0\n  1006:     }\n  1007: \n  1008:     /// Consumes this error, returning the underlying vector of bytes which\n  1009:     /// generated the error in the first place.\n  1010:     ///\n  1011:     /// # Examples\n  1012:     ///\n  1013:     /// ```\n  1014:     /// use std::ffi::CString;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3551,
            "path": "Weak"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:3733",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3551,
            "path": "Weak"
          }
        }
      }
    },
    "verification_source": "  3211:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  3212:     ///\n  3213:     /// [`upgrade`]: Weak::upgrade\n  3214:     ///\n  3215:     /// # Examples\n  3216:     ///\n  3217:     /// ```\n  3218:     /// use std::rc::Weak;\n  3219:     ///\n  3220:     /// let empty: Weak<i64> = Weak::new();\n  3221:     /// assert!(empty.upgrade().is_none());\n  3222:     /// ```\n  3223:     #[inline]\n  3224:     #[stable(feature = \"downgraded_weak\", since = \"1.10.0\")]\n  3225:     #[rustc_const_stable(feature = \"const_weak_new\", since = \"1.73.0\")]\n  3226:     #[must_use]\n  3227:     pub const fn new() -> Weak<T> {\n  3228:         Weak { ptr: NonNull::without_provenance(NonZeroUsize::MAX), alloc: Global }\n  3229:     }\n  3230: }\n  3231: \n  3232: impl<T, A: Allocator> Weak<T, A> {\n  3233:     /// Constructs a new `Weak<T>`, without allocating any memory, technically in the provided\n  3234:     /// allocator.\n  3235:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  3236:     ///\n  3237:     /// [`upgrade`]: Weak::upgrade\n  3238:     ///\n  3239:     /// # Examples\n  3240:     ///\n  3241:     /// ```\n  3242:     /// use std::rc::Weak;\n  3243:     ///",
    "nanvix_source": "  3226:     /// ```\n  3227:     /// use std::rc::Weak;\n  3228:     ///\n  3229:     /// let empty: Weak<i64> = Weak::new();\n  3230:     /// assert!(empty.upgrade().is_none());\n  3231:     /// ```\n  3232:     #[inline]\n  3233:     #[stable(feature = \"downgraded_weak\", since = \"1.10.0\")]\n  3234:     #[rustc_const_stable(feature = \"const_weak_new\", since = \"1.73.0\")]\n  3235:     #[must_use]\n  3236:     pub const fn new() -> Weak<T> {\n  3237:         Weak { ptr: NonNull::without_provenance(NonZeroUsize::MAX), alloc: Global }\n  3238:     }\n  3239: }\n  3240: \n  3241: impl<T, A: Allocator> Weak<T, A> {\n  3242:     /// Constructs a new `Weak<T>`, without allocating any memory, technically in the provided\n  3243:     /// allocator.\n  3244:     /// Calling [`upgrade`] on the return value always gives [`None`].\n  3245:     ///\n  3246:     /// [`upgrade`]: Weak::upgrade",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::ptr_eq",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
      "name": "ptr_eq",
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
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3551,
            "path": "Weak"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 29,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:3747",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
            "other",
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
    "verification_source": "  3612:     /// Comparing `Weak::new`.\n  3613:     ///\n  3614:     /// ```\n  3615:     /// use std::rc::{Rc, Weak};\n  3616:     ///\n  3617:     /// let first = Weak::new();\n  3618:     /// let second = Weak::new();\n  3619:     /// assert!(first.ptr_eq(&second));\n  3620:     ///\n  3621:     /// let third_rc = Rc::new(());\n  3622:     /// let third = Rc::downgrade(&third_rc);\n  3623:     /// assert!(!first.ptr_eq(&third));\n  3624:     /// ```\n  3625:     #[inline]\n  3626:     #[must_use]\n  3627:     #[stable(feature = \"weak_ptr_eq\", since = \"1.39.0\")]\n  3628:     pub fn ptr_eq(&self, other: &Self) -> bool {\n  3629:         ptr::addr_eq(self.ptr.as_ptr(), other.ptr.as_ptr())\n  3630:     }\n  3631: }\n  3632: \n  3633: #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  3634: unsafe impl<#[may_dangle] T: ?Sized, A: Allocator> Drop for Weak<T, A> {\n  3635:     /// Drops the `Weak` pointer.\n  3636:     ///\n  3637:     /// # Examples\n  3638:     ///\n  3639:     /// ```\n  3640:     /// use std::rc::{Rc, Weak};\n  3641:     ///\n  3642:     /// struct Foo;\n  3643:     ///\n  3644:     /// impl Drop for Foo {",
    "nanvix_source": "  3633:     /// let second = Weak::new();\n  3634:     /// assert!(first.ptr_eq(&second));\n  3635:     ///\n  3636:     /// let third_rc = Rc::new(());\n  3637:     /// let third = Rc::downgrade(&third_rc);\n  3638:     /// assert!(!first.ptr_eq(&third));\n  3639:     /// ```\n  3640:     #[inline]\n  3641:     #[must_use]\n  3642:     #[stable(feature = \"weak_ptr_eq\", since = \"1.39.0\")]\n  3643:     pub fn ptr_eq(&self, other: &Self) -> bool {\n  3644:         ptr::addr_eq(self.ptr.as_ptr(), other.ptr.as_ptr())\n  3645:     }\n  3646: }\n  3647: \n  3648: #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  3649: unsafe impl<#[may_dangle] T: ?Sized, A: Allocator> Drop for Weak<T, A> {\n  3650:     /// Drops the `Weak` pointer.\n  3651:     ///\n  3652:     /// # Examples\n  3653:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::strong_count",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
      "name": "strong_count",
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
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 3551,
            "path": "Weak"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 29,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:3747",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
    "verification_source": "  3532: \n  3533:         if inner.strong() == 0 {\n  3534:             None\n  3535:         } else {\n  3536:             unsafe {\n  3537:                 inner.inc_strong();\n  3538:                 Some(Rc::from_inner_in(self.ptr, self.alloc.clone()))\n  3539:             }\n  3540:         }\n  3541:     }\n  3542: \n  3543:     /// Gets the number of strong (`Rc`) pointers pointing to this allocation.\n  3544:     ///\n  3545:     /// If `self` was created using [`Weak::new`], this will return 0.\n  3546:     #[must_use]\n  3547:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3548:     pub fn strong_count(&self) -> usize {\n  3549:         if let Some(inner) = self.inner() { inner.strong() } else { 0 }\n  3550:     }\n  3551: \n  3552:     /// Gets the number of `Weak` pointers pointing to this allocation.\n  3553:     ///\n  3554:     /// If no strong pointers remain, this will return zero.\n  3555:     #[must_use]\n  3556:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3557:     pub fn weak_count(&self) -> usize {\n  3558:         if let Some(inner) = self.inner() {\n  3559:             if inner.strong() > 0 {\n  3560:                 inner.weak() - 1 // subtract the implicit weak ptr\n  3561:             } else {\n  3562:                 0\n  3563:             }\n  3564:         } else {",
    "nanvix_source": "  3553:                 Some(Rc::from_inner_in(self.ptr, self.alloc.clone()))\n  3554:             }\n  3555:         }\n  3556:     }\n  3557: \n  3558:     /// Gets the number of strong (`Rc`) pointers pointing to this allocation.\n  3559:     ///\n  3560:     /// If `self` was created using [`Weak::new`], this will return 0.\n  3561:     #[must_use]\n  3562:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3563:     pub fn strong_count(&self) -> usize {\n  3564:         if let Some(inner) = self.inner() { inner.strong() } else { 0 }\n  3565:     }\n  3566: \n  3567:     /// Gets the number of `Weak` pointers pointing to this allocation.\n  3568:     ///\n  3569:     /// If no strong pointers remain, this will return zero.\n  3570:     #[must_use]\n  3571:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3572:     pub fn weak_count(&self) -> usize {\n  3573:         if let Some(inner) = self.inner() {",
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
