For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::result::Result::as_deref_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8650,
                      "path": "DerefMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_deref_mut",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
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
    "verification_source": "  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());\n  1063:     /// let y: Result<&mut str, &mut u32> = Ok(&mut s);\n  1064:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1065:     ///\n  1066:     /// let mut i = 42;\n  1067:     /// let mut x: Result<String, u32> = Err(42);\n  1068:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1069:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1070:     /// ```\n  1071:     #[inline]\n  1072:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1073:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1074:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1075:     where\n  1076:         T: [const] DerefMut,\n  1077:     {\n  1078:         self.as_mut().map(DerefMut::deref_mut)\n  1079:     }\n  1080: \n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082:     // Iterator constructors\n  1083:     /////////////////////////////////////////////////////////////////////////\n  1084: \n  1085:     /// Returns an iterator over the possibly contained value.\n  1086:     ///\n  1087:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1088:     ///\n  1089:     /// # Examples\n  1090:     ///",
    "nanvix_source": "  1062:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1063:     ///\n  1064:     /// let mut i = 42;\n  1065:     /// let mut x: Result<String, u32> = Err(42);\n  1066:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1067:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1068:     /// ```\n  1069:     #[inline]\n  1070:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1071:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1072:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1073:     where\n  1074:         T: [const] DerefMut,\n  1075:     {\n  1076:         self.as_mut().map(DerefMut::deref_mut)\n  1077:     }\n  1078: \n  1079:     /////////////////////////////////////////////////////////////////////////\n  1080:     // Iterator constructors\n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::as_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "as_mut",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
                        }
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
    "verification_source": "   782:     ///         Ok(v) => *v = 42,\n   783:     ///         Err(e) => *e = 0,\n   784:     ///     }\n   785:     /// }\n   786:     ///\n   787:     /// let mut x: Result<i32, i32> = Ok(2);\n   788:     /// mutate(&mut x);\n   789:     /// assert_eq!(x.unwrap(), 42);\n   790:     ///\n   791:     /// let mut x: Result<i32, i32> = Err(13);\n   792:     /// mutate(&mut x);\n   793:     /// assert_eq!(x.unwrap_err(), 0);\n   794:     /// ```\n   795:     #[inline]\n   796:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   797:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n   798:     pub const fn as_mut(&mut self) -> Result<&mut T, &mut E> {\n   799:         match *self {\n   800:             Ok(ref mut x) => Ok(x),\n   801:             Err(ref mut x) => Err(x),\n   802:         }\n   803:     }\n   804: \n   805:     /////////////////////////////////////////////////////////////////////////\n   806:     // Transforming contained values\n   807:     /////////////////////////////////////////////////////////////////////////\n   808: \n   809:     /// Maps a `Result<T, E>` to `Result<U, E>` by applying a function to a\n   810:     /// contained [`Ok`] value, leaving an [`Err`] value untouched.\n   811:     ///\n   812:     /// This function can be used to compose the results of two functions.\n   813:     ///\n   814:     /// # Examples",
    "nanvix_source": "   788:     /// mutate(&mut x);\n   789:     /// assert_eq!(x.unwrap(), 42);\n   790:     ///\n   791:     /// let mut x: Result<i32, i32> = Err(13);\n   792:     /// mutate(&mut x);\n   793:     /// assert_eq!(x.unwrap_err(), 0);\n   794:     /// ```\n   795:     #[inline]\n   796:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   797:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n   798:     pub const fn as_mut(&mut self) -> Result<&mut T, &mut E> {\n   799:         match *self {\n   800:             Ok(ref mut x) => Ok(x),\n   801:             Err(ref mut x) => Err(x),\n   802:         }\n   803:     }\n   804: \n   805:     /////////////////////////////////////////////////////////////////////////\n   806:     // Transforming contained values\n   807:     /////////////////////////////////////////////////////////////////////////\n   808: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::ChunksExactMut::into_remainder",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "into_remainder",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13736,
            "path": "ChunksExactMut"
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
            },
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
        "impl_id": "core:31516",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13736",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "ChunksExactMut"
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
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2025: \n  2026: impl<'a, T> ChunksExactMut<'a, T> {\n  2027:     #[inline]\n  2028:     pub(super) const fn new(slice: &'a mut [T], chunk_size: usize) -> Self {\n  2029:         let rem = slice.len() % chunk_size;\n  2030:         let fst_len = slice.len() - rem;\n  2031:         // SAFETY: 0 <= fst_len <= slice.len() by construction above\n  2032:         let (fst, snd) = unsafe { slice.split_at_mut_unchecked(fst_len) };\n  2033:         Self { v: fst, rem: snd, chunk_size, _marker: PhantomData }\n  2034:     }\n  2035: \n  2036:     /// Returns the remainder of the original slice that is not going to be\n  2037:     /// returned by the iterator. The returned slice has at most `chunk_size-1`\n  2038:     /// elements.\n  2039:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2040:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  2041:     pub fn into_remainder(self) -> &'a mut [T] {\n  2042:         self.rem\n  2043:     }\n  2044: }\n  2045: \n  2046: #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  2047: impl<'a, T> Iterator for ChunksExactMut<'a, T> {\n  2048:     type Item = &'a mut [T];\n  2049: \n  2050:     #[inline]\n  2051:     fn next(&mut self) -> Option<&'a mut [T]> {\n  2052:         // SAFETY: we have `&mut self`, so are allowed to temporarily materialize a mut slice\n  2053:         unsafe { &mut *self.v }.split_at_mut_checked(self.chunk_size).and_then(|(chunk, rest)| {\n  2054:             self.v = rest;\n  2055:             Some(chunk)\n  2056:         })\n  2057:     }",
    "nanvix_source": "  2029:         // SAFETY: 0 <= fst_len <= slice.len() by construction above\n  2030:         let (fst, snd) = unsafe { slice.split_at_mut_unchecked(fst_len) };\n  2031:         Self { v: fst, rem: snd, chunk_size, _marker: PhantomData }\n  2032:     }\n  2033: \n  2034:     /// Returns the remainder of the original slice that is not going to be\n  2035:     /// returned by the iterator. The returned slice has at most `chunk_size-1`\n  2036:     /// elements.\n  2037:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2038:     #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  2039:     pub fn into_remainder(self) -> &'a mut [T] {\n  2040:         self.rem\n  2041:     }\n  2042: }\n  2043: \n  2044: #[stable(feature = \"chunks_exact\", since = \"1.31.0\")]\n  2045: impl<'a, T> Iterator for ChunksExactMut<'a, T> {\n  2046:     type Item = &'a mut [T];\n  2047: \n  2048:     #[inline]\n  2049:     fn next(&mut self) -> Option<&'a mut [T]> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::IterMut::into_slice",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "into_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 11725,
            "path": "IterMut"
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
            },
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
        "impl_id": "core:31338",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:11725",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "IterMut"
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
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "   260:     ///\n   261:     /// // Then we call `iter_mut` on the slice to get the `IterMut` struct:\n   262:     /// let mut iter = slice.iter_mut();\n   263:     /// // Now, we call the `next` method to remove the first element of the iterator,\n   264:     /// // unwrap and dereference what we get from `next` and increase its value by 1:\n   265:     /// *iter.next().unwrap() += 1;\n   266:     /// // Here the iterator does not contain the first element of the slice any more,\n   267:     /// // so `into_slice` only returns the last two elements of the slice,\n   268:     /// // and so this prints \"[2, 3]\":\n   269:     /// println!(\"{:?}\", iter.into_slice());\n   270:     /// // The underlying slice still contains three elements, but its first element\n   271:     /// // was increased by 1, so this prints \"[2, 2, 3]\":\n   272:     /// println!(\"{:?}\", slice);\n   273:     /// ```\n   274:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   275:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   276:     pub fn into_slice(self) -> &'a mut [T] {\n   277:         // SAFETY: the iterator was created from a mutable slice with pointer\n   278:         // `self.ptr` and length `len!(self)`. This guarantees that all the prerequisites\n   279:         // for `from_raw_parts_mut` are fulfilled.\n   280:         unsafe { from_raw_parts_mut(self.ptr.as_ptr(), len!(self)) }\n   281:     }\n   282: \n   283:     /// Views the underlying data as a subslice of the original data.\n   284:     ///\n   285:     /// # Examples\n   286:     ///\n   287:     /// Basic usage:\n   288:     ///\n   289:     /// ```\n   290:     /// // First, we need a slice to call the `iter_mut` method on:\n   291:     /// let slice = &mut [1, 2, 3];\n   292:     ///",
    "nanvix_source": "   264:     /// // Here the iterator does not contain the first element of the slice any more,\n   265:     /// // so `into_slice` only returns the last two elements of the slice,\n   266:     /// // and so this prints \"[2, 3]\":\n   267:     /// println!(\"{:?}\", iter.into_slice());\n   268:     /// // The underlying slice still contains three elements, but its first element\n   269:     /// // was increased by 1, so this prints \"[2, 2, 3]\":\n   270:     /// println!(\"{:?}\", slice);\n   271:     /// ```\n   272:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   273:     #[stable(feature = \"iter_to_slice\", since = \"1.4.0\")]\n   274:     pub fn into_slice(self) -> &'a mut [T] {\n   275:         // SAFETY: the iterator was created from a mutable slice with pointer\n   276:         // `self.ptr` and length `len!(self)`. This guarantees that all the prerequisites\n   277:         // for `from_raw_parts_mut` are fulfilled.\n   278:         unsafe { from_raw_parts_mut(self.ptr.as_ptr(), len!(self)) }\n   279:     }\n   280: \n   281:     /// Views the underlying data as a subslice of the original data.\n   282:     ///\n   283:     /// # Examples\n   284:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::RChunksExactMut::into_remainder",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "into_remainder",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13740,
            "path": "RChunksExactMut"
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
            },
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
        "impl_id": "core:31580",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13740",
        "resolved_owner_path": [
          "core",
          "slice",
          "iter",
          "RChunksExactMut"
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
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2841: \n  2842: impl<'a, T> RChunksExactMut<'a, T> {\n  2843:     #[inline]\n  2844:     pub(super) const fn new(slice: &'a mut [T], chunk_size: usize) -> Self {\n  2845:         let rem = slice.len() % chunk_size;\n  2846:         // SAFETY: 0 <= rem <= slice.len() by construction above\n  2847:         let (fst, snd) = unsafe { slice.split_at_mut_unchecked(rem) };\n  2848:         Self { v: snd, rem: fst, chunk_size }\n  2849:     }\n  2850: \n  2851:     /// Returns the remainder of the original slice that is not going to be\n  2852:     /// returned by the iterator. The returned slice has at most `chunk_size-1`\n  2853:     /// elements.\n  2854:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2855:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2856:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  2857:     pub const fn into_remainder(self) -> &'a mut [T] {\n  2858:         self.rem\n  2859:     }\n  2860: }\n  2861: \n  2862: #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2863: impl<'a, T> Iterator for RChunksExactMut<'a, T> {\n  2864:     type Item = &'a mut [T];\n  2865: \n  2866:     #[inline]\n  2867:     fn next(&mut self) -> Option<&'a mut [T]> {\n  2868:         if self.v.len() < self.chunk_size {\n  2869:             None\n  2870:         } else {\n  2871:             let len = self.v.len();\n  2872:             // SAFETY: The self.v contract ensures that any split_at_mut is valid.\n  2873:             let (head, tail) = unsafe { self.v.split_at_mut(len - self.chunk_size) };",
    "nanvix_source": "  2845:         let (fst, snd) = unsafe { slice.split_at_mut_unchecked(rem) };\n  2846:         Self { v: snd, rem: fst, chunk_size }\n  2847:     }\n  2848: \n  2849:     /// Returns the remainder of the original slice that is not going to be\n  2850:     /// returned by the iterator. The returned slice has at most `chunk_size-1`\n  2851:     /// elements.\n  2852:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2853:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2854:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  2855:     pub const fn into_remainder(self) -> &'a mut [T] {\n  2856:         self.rem\n  2857:     }\n  2858: }\n  2859: \n  2860: #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  2861: impl<'a, T> Iterator for RChunksExactMut<'a, T> {\n  2862:     type Item = &'a mut [T];\n  2863: \n  2864:     #[inline]\n  2865:     fn next(&mut self) -> Option<&'a mut [T]> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::align_to_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
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
            "name": "U"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "align_to_mut",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
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
        "output": {
          "tuple": [
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            },
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "U"
                  }
                }
              }
            },
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            }
          ]
        }
      }
    },
    "verification_source": "  4548:     ///\n  4549:     /// # Examples\n  4550:     ///\n  4551:     /// Basic usage:\n  4552:     ///\n  4553:     /// ```\n  4554:     /// unsafe {\n  4555:     ///     let mut bytes: [u8; 7] = [1, 2, 3, 4, 5, 6, 7];\n  4556:     ///     let (prefix, shorts, suffix) = bytes.align_to_mut::<u16>();\n  4557:     ///     // less_efficient_algorithm_for_bytes(prefix);\n  4558:     ///     // more_efficient_algorithm_for_aligned_shorts(shorts);\n  4559:     ///     // less_efficient_algorithm_for_bytes(suffix);\n  4560:     /// }\n  4561:     /// ```\n  4562:     #[stable(feature = \"slice_align_to\", since = \"1.30.0\")]\n  4563:     #[must_use]\n  4564:     pub unsafe fn align_to_mut<U>(&mut self) -> (&mut [T], &mut [U], &mut [T]) {\n  4565:         // Note that most of this function will be constant-evaluated,\n  4566:         if U::IS_ZST || T::IS_ZST {\n  4567:             // handle ZSTs specially, which is \u2013 don't handle them at all.\n  4568:             return (self, &mut [], &mut []);\n  4569:         }\n  4570: \n  4571:         // First, find at what point do we split between the first and 2nd slice. Easy with\n  4572:         // ptr.align_offset.\n  4573:         let ptr = self.as_ptr();\n  4574:         // SAFETY: Here we are ensuring we will use aligned pointers for U for the\n  4575:         // rest of the method. This is done by passing a pointer to &[T] with an\n  4576:         // alignment targeted for U.\n  4577:         // `crate::ptr::align_offset` is called with a correctly aligned and\n  4578:         // valid pointer `ptr` (it comes from a reference to `self`) and with\n  4579:         // a size that is a power of two (since it comes from the alignment for U),\n  4580:         // satisfying its safety constraints.",
    "nanvix_source": "  4561:     /// unsafe {\n  4562:     ///     let mut bytes: [u8; 7] = [1, 2, 3, 4, 5, 6, 7];\n  4563:     ///     let (prefix, shorts, suffix) = bytes.align_to_mut::<u16>();\n  4564:     ///     // less_efficient_algorithm_for_bytes(prefix);\n  4565:     ///     // more_efficient_algorithm_for_aligned_shorts(shorts);\n  4566:     ///     // less_efficient_algorithm_for_bytes(suffix);\n  4567:     /// }\n  4568:     /// ```\n  4569:     #[stable(feature = \"slice_align_to\", since = \"1.30.0\")]\n  4570:     #[must_use]\n  4571:     pub unsafe fn align_to_mut<U>(&mut self) -> (&mut [T], &mut [U], &mut [T]) {\n  4572:         // Note that most of this function will be constant-evaluated,\n  4573:         if U::IS_ZST || T::IS_ZST {\n  4574:             // handle ZSTs specially, which is \u2013 don't handle them at all.\n  4575:             return (self, &mut [], &mut []);\n  4576:         }\n  4577: \n  4578:         // First, find at what point do we split between the first and 2nd slice. Easy with\n  4579:         // ptr.align_offset.\n  4580:         let ptr = self.as_ptr();\n  4581:         // SAFETY: Here we are ensuring we will use aligned pointers for U for the",
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
