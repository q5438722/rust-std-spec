For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::from_fn",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
            "name": "F"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [],
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
                              "id": 84,
                              "path": "Option"
                            }
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "from_fn",
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
            "f",
            {
              "generic": "F"
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9922,
            "path": "FromFn"
          }
        }
      }
    },
    "verification_source": "    25: ///\n    26: /// [module-level documentation]: crate::iter\n    27: ///\n    28: /// ```\n    29: /// let mut count = 0;\n    30: /// let counter = std::iter::from_fn(move || {\n    31: ///     // Increment our count. This is why we started at zero.\n    32: ///     count += 1;\n    33: ///\n    34: ///     // Check to see if we've finished counting or not.\n    35: ///     if count < 6 {\n    36: ///         Some(count)\n    37: ///     } else {\n    38: ///         None\n    39: ///     }\n    40: /// });\n    41: /// assert_eq!(counter.collect::<Vec<_>>(), &[1, 2, 3, 4, 5]);\n    42: /// ```\n    43: #[inline]\n    44: #[stable(feature = \"iter_from_fn\", since = \"1.34.0\")]\n    45: pub fn from_fn<T, F>(f: F) -> FromFn<F>\n    46: where\n    47:     F: FnMut() -> Option<T>,\n    48: {\n    49:     FromFn(f)\n    50: }\n    51: \n    52: /// An iterator where each iteration calls the provided closure `F: FnMut() -> Option<T>`.\n    53: ///\n    54: /// This `struct` is created by the [`iter::from_fn()`] function.\n    55: /// See its documentation for more.\n    56: ///\n    57: /// [`iter::from_fn()`]: from_fn",
    "nanvix_source": "    31: ///     // Increment our count. This is why we started at zero.\n    32: ///     count += 1;\n    33: ///\n    34: ///     // Check to see if we've finished counting or not.\n    35: ///     if count < 6 {\n    36: ///         Some(count)\n    37: ///     } else {\n    38: ///         None\n    39: ///     }\n    40: /// });\n    41: /// assert_eq!(counter.collect::<Vec<_>>(), &[1, 2, 3, 4, 5]);\n    42: /// ```\n    43: #[inline]\n    44: #[stable(feature = \"iter_from_fn\", since = \"1.34.0\")]\n    45: pub fn from_fn<T, F>(f: F) -> FromFn<F>\n    46: where\n    47:     F: FnMut() -> Option<T>,\n    48: {\n    49:     FromFn(f)\n    50: }\n    51: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::once",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "once",
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
            "value",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9925,
            "path": "Once"
          }
        }
      }
    },
    "verification_source": "    40: /// // PathBufs, so we use map\n    41: /// let dirs = dirs.map(|file| file.unwrap().path());\n    42: ///\n    43: /// // now, our iterator just for our config file\n    44: /// let config = iter::once(PathBuf::from(\".foorc\"));\n    45: ///\n    46: /// // chain the two iterators together into one big iterator\n    47: /// let files = dirs.chain(config);\n    48: ///\n    49: /// // this will give us all of the files in .foo as well as .foorc\n    50: /// for f in files {\n    51: ///     println!(\"{f:?}\");\n    52: /// }\n    53: /// # std::io::Result::Ok(())\n    54: /// ```\n    55: #[stable(feature = \"iter_once\", since = \"1.2.0\")]\n    56: pub fn once<T>(value: T) -> Once<T> {\n    57:     Once { inner: Some(value).into_iter() }\n    58: }\n    59: \n    60: /// An iterator that yields an element exactly once.\n    61: ///\n    62: /// This `struct` is created by the [`once()`] function. See its documentation for more.\n    63: #[derive(Clone, Debug)]\n    64: #[stable(feature = \"iter_once\", since = \"1.2.0\")]\n    65: #[rustc_diagnostic_item = \"IterOnce\"]\n    66: pub struct Once<T> {\n    67:     inner: crate::option::IntoIter<T>,\n    68: }\n    69: \n    70: #[stable(feature = \"iter_once\", since = \"1.2.0\")]\n    71: impl<T> Iterator for Once<T> {\n    72:     type Item = T;",
    "nanvix_source": "    46: /// // chain the two iterators together into one big iterator\n    47: /// let files = dirs.chain(config);\n    48: ///\n    49: /// // this will give us all of the files in .foo as well as .foorc\n    50: /// for f in files {\n    51: ///     println!(\"{f:?}\");\n    52: /// }\n    53: /// # std::io::Result::Ok(())\n    54: /// ```\n    55: #[stable(feature = \"iter_once\", since = \"1.2.0\")]\n    56: pub fn once<T>(value: T) -> Once<T> {\n    57:     Once { inner: Some(value).into_iter() }\n    58: }\n    59: \n    60: /// An iterator that yields an element exactly once.\n    61: ///\n    62: /// This `struct` is created by the [`once()`] function. See its documentation for more.\n    63: #[derive(Clone, Debug)]\n    64: #[stable(feature = \"iter_once\", since = \"1.2.0\")]\n    65: #[rustc_diagnostic_item = \"IterOnce\"]\n    66: pub struct Once<T> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::once_with",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "A"
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
                        "args": {
                          "parenthesized": {
                            "inputs": [],
                            "output": {
                              "generic": "A"
                            }
                          }
                        },
                        "id": 24,
                        "path": "FnOnce"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
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
      "name": "once_with",
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
            "make",
            {
              "generic": "F"
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9928,
            "path": "OnceWith"
          }
        }
      }
    },
    "verification_source": "    45: /// // PathBufs, so we use map\n    46: /// let dirs = dirs.map(|file| file.unwrap().path());\n    47: ///\n    48: /// // now, our iterator just for our config file\n    49: /// let config = iter::once_with(|| PathBuf::from(\".foorc\"));\n    50: ///\n    51: /// // chain the two iterators together into one big iterator\n    52: /// let files = dirs.chain(config);\n    53: ///\n    54: /// // this will give us all of the files in .foo as well as .foorc\n    55: /// for f in files {\n    56: ///     println!(\"{f:?}\");\n    57: /// }\n    58: /// ```\n    59: #[inline]\n    60: #[stable(feature = \"iter_once_with\", since = \"1.43.0\")]\n    61: pub fn once_with<A, F: FnOnce() -> A>(make: F) -> OnceWith<F> {\n    62:     OnceWith { make: Some(make) }\n    63: }\n    64: \n    65: /// An iterator that yields a single element of type `A` by\n    66: /// applying the provided closure `F: FnOnce() -> A`.\n    67: ///\n    68: /// This `struct` is created by the [`once_with()`] function.\n    69: /// See its documentation for more.\n    70: #[derive(Clone)]\n    71: #[stable(feature = \"iter_once_with\", since = \"1.43.0\")]\n    72: pub struct OnceWith<F> {\n    73:     make: Option<F>,\n    74: }\n    75: \n    76: #[stable(feature = \"iter_once_with_debug\", since = \"1.68.0\")]\n    77: impl<F> fmt::Debug for OnceWith<F> {",
    "nanvix_source": "    51: /// // chain the two iterators together into one big iterator\n    52: /// let files = dirs.chain(config);\n    53: ///\n    54: /// // this will give us all of the files in .foo as well as .foorc\n    55: /// for f in files {\n    56: ///     println!(\"{f:?}\");\n    57: /// }\n    58: /// ```\n    59: #[inline]\n    60: #[stable(feature = \"iter_once_with\", since = \"1.43.0\")]\n    61: pub fn once_with<A, F: FnOnce() -> A>(make: F) -> OnceWith<F> {\n    62:     OnceWith { make: Some(make) }\n    63: }\n    64: \n    65: /// An iterator that yields a single element of type `A` by\n    66: /// applying the provided closure `F: FnOnce() -> A`.\n    67: ///\n    68: /// This `struct` is created by the [`once_with()`] function.\n    69: /// See its documentation for more.\n    70: #[derive(Clone)]\n    71: #[stable(feature = \"iter_once_with\", since = \"1.43.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::repeat",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 42,
                        "path": "Clone"
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
      "name": "repeat",
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
            "elt",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9931,
            "path": "Repeat"
          }
        }
      }
    },
    "verification_source": "    48: /// use std::iter;\n    49: ///\n    50: /// // that last example was too many fours. Let's only have four fours.\n    51: /// let mut four_fours = iter::repeat(4).take(4);\n    52: ///\n    53: /// assert_eq!(Some(4), four_fours.next());\n    54: /// assert_eq!(Some(4), four_fours.next());\n    55: /// assert_eq!(Some(4), four_fours.next());\n    56: /// assert_eq!(Some(4), four_fours.next());\n    57: ///\n    58: /// // ... and now we're done\n    59: /// assert_eq!(None, four_fours.next());\n    60: /// ```\n    61: #[inline]\n    62: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    63: #[rustc_diagnostic_item = \"iter_repeat\"]\n    64: pub fn repeat<T: Clone>(elt: T) -> Repeat<T> {\n    65:     Repeat { element: elt }\n    66: }\n    67: \n    68: /// An iterator that repeats an element endlessly.\n    69: ///\n    70: /// This `struct` is created by the [`repeat()`] function. See its documentation for more.\n    71: #[derive(Clone, Debug)]\n    72: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    73: pub struct Repeat<A> {\n    74:     element: A,\n    75: }\n    76: \n    77: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    78: impl<A: Clone> Iterator for Repeat<A> {\n    79:     type Item = A;\n    80: ",
    "nanvix_source": "    54: /// assert_eq!(Some(4), four_fours.next());\n    55: /// assert_eq!(Some(4), four_fours.next());\n    56: /// assert_eq!(Some(4), four_fours.next());\n    57: ///\n    58: /// // ... and now we're done\n    59: /// assert_eq!(None, four_fours.next());\n    60: /// ```\n    61: #[inline]\n    62: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    63: #[rustc_diagnostic_item = \"iter_repeat\"]\n    64: pub fn repeat<T: Clone>(elt: T) -> Repeat<T> {\n    65:     Repeat { element: elt }\n    66: }\n    67: \n    68: /// An iterator that repeats an element endlessly.\n    69: ///\n    70: /// This `struct` is created by the [`repeat()`] function. See its documentation for more.\n    71: #[derive(Clone, Debug)]\n    72: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    73: pub struct Repeat<A> {\n    74:     element: A,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::repeat_n",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 42,
                        "path": "Clone"
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
      "name": "repeat_n",
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
            "element",
            {
              "generic": "T"
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9934,
            "path": "RepeatN"
          }
        }
      }
    },
    "verification_source": "    43: ///     // It starts by cloning things\n    44: ///     let cloned = it.next().unwrap();\n    45: ///     assert_eq!(cloned.len(), 0);\n    46: ///     assert_eq!(cloned.capacity(), 0);\n    47: /// }\n    48: ///\n    49: /// // ... but the last item is the original one\n    50: /// let last = it.next().unwrap();\n    51: /// assert_eq!(last.len(), 0);\n    52: /// assert_eq!(last.capacity(), 123);\n    53: ///\n    54: /// // ... and now we're done\n    55: /// assert_eq!(None, it.next());\n    56: /// ```\n    57: #[inline]\n    58: #[stable(feature = \"iter_repeat_n\", since = \"1.82.0\")]\n    59: pub fn repeat_n<T: Clone>(element: T, count: usize) -> RepeatN<T> {\n    60:     RepeatN { inner: RepeatNInner::new(element, count) }\n    61: }\n    62: \n    63: #[derive(Clone, Copy)]\n    64: struct RepeatNInner<T> {\n    65:     count: NonZero<usize>,\n    66:     element: T,\n    67: }\n    68: \n    69: impl<T> RepeatNInner<T> {\n    70:     fn new(element: T, count: usize) -> Option<Self> {\n    71:         let count = NonZero::<usize>::new(count)?;\n    72:         Some(Self { element, count })\n    73:     }\n    74: }\n    75: ",
    "nanvix_source": "    49: /// // ... but the last item is the original one\n    50: /// let last = it.next().unwrap();\n    51: /// assert_eq!(last.len(), 0);\n    52: /// assert_eq!(last.capacity(), 123);\n    53: ///\n    54: /// // ... and now we're done\n    55: /// assert_eq!(None, it.next());\n    56: /// ```\n    57: #[inline]\n    58: #[stable(feature = \"iter_repeat_n\", since = \"1.82.0\")]\n    59: pub fn repeat_n<T: Clone>(element: T, count: usize) -> RepeatN<T> {\n    60:     RepeatN { inner: RepeatNInner::new(element, count) }\n    61: }\n    62: \n    63: #[derive(Clone, Copy)]\n    64: struct RepeatNInner<T> {\n    65:     count: NonZero<usize>,\n    66:     element: T,\n    67: }\n    68: \n    69: impl<T> RepeatNInner<T> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::repeat_with",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
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
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "A"
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
                        "args": {
                          "parenthesized": {
                            "inputs": [],
                            "output": {
                              "generic": "A"
                            }
                          }
                        },
                        "id": 22,
                        "path": "FnMut"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "F"
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
      "name": "repeat_with",
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
            "repeater",
            {
              "generic": "F"
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
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9937,
            "path": "RepeatWith"
          }
        }
      }
    },
    "verification_source": "    49: ///\n    50: /// // From the zeroth to the third power of two:\n    51: /// let mut curr = 1;\n    52: /// let mut pow2 = iter::repeat_with(|| { let tmp = curr; curr *= 2; tmp })\n    53: ///                     .take(4);\n    54: ///\n    55: /// assert_eq!(Some(1), pow2.next());\n    56: /// assert_eq!(Some(2), pow2.next());\n    57: /// assert_eq!(Some(4), pow2.next());\n    58: /// assert_eq!(Some(8), pow2.next());\n    59: ///\n    60: /// // ... and now we're done\n    61: /// assert_eq!(None, pow2.next());\n    62: /// ```\n    63: #[inline]\n    64: #[stable(feature = \"iterator_repeat_with\", since = \"1.28.0\")]\n    65: pub fn repeat_with<A, F: FnMut() -> A>(repeater: F) -> RepeatWith<F> {\n    66:     RepeatWith { repeater }\n    67: }\n    68: \n    69: /// An iterator that repeats elements of type `A` endlessly by\n    70: /// applying the provided closure `F: FnMut() -> A`.\n    71: ///\n    72: /// This `struct` is created by the [`repeat_with()`] function.\n    73: /// See its documentation for more.\n    74: #[derive(Copy, Clone)]\n    75: #[stable(feature = \"iterator_repeat_with\", since = \"1.28.0\")]\n    76: pub struct RepeatWith<F> {\n    77:     repeater: F,\n    78: }\n    79: \n    80: #[stable(feature = \"iterator_repeat_with_debug\", since = \"1.68.0\")]\n    81: impl<F> fmt::Debug for RepeatWith<F> {",
    "nanvix_source": "    55: /// assert_eq!(Some(1), pow2.next());\n    56: /// assert_eq!(Some(2), pow2.next());\n    57: /// assert_eq!(Some(4), pow2.next());\n    58: /// assert_eq!(Some(8), pow2.next());\n    59: ///\n    60: /// // ... and now we're done\n    61: /// assert_eq!(None, pow2.next());\n    62: /// ```\n    63: #[inline]\n    64: #[stable(feature = \"iterator_repeat_with\", since = \"1.28.0\")]\n    65: pub fn repeat_with<A, F: FnMut() -> A>(repeater: F) -> RepeatWith<F> {\n    66:     RepeatWith { repeater }\n    67: }\n    68: \n    69: /// An iterator that repeats elements of type `A` endlessly by\n    70: /// applying the provided closure `F: FnMut() -> A`.\n    71: ///\n    72: /// This `struct` is created by the [`repeat_with()`] function.\n    73: /// See its documentation for more.\n    74: #[derive(Copy, Clone)]\n    75: #[stable(feature = \"iterator_repeat_with\", since = \"1.28.0\")]",
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
