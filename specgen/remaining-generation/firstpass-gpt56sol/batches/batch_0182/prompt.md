For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::split_off_first",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "split_off_first",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
                  "borrowed_ref": {
                    "is_mutable": false,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
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
                        "lifetime": "'a",
                        "type": {
                          "generic": "T"
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
    "verification_source": "  4994:     /// to it.\n  4995:     ///\n  4996:     /// Returns `None` if the slice is empty.\n  4997:     ///\n  4998:     /// # Examples\n  4999:     ///\n  5000:     /// ```\n  5001:     /// let mut slice: &[_] = &['a', 'b', 'c'];\n  5002:     /// let first = slice.split_off_first().unwrap();\n  5003:     ///\n  5004:     /// assert_eq!(slice, &['b', 'c']);\n  5005:     /// assert_eq!(first, &'a');\n  5006:     /// ```\n  5007:     #[inline]\n  5008:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5009:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5010:     pub const fn split_off_first<'a>(self: &mut &'a Self) -> Option<&'a T> {\n  5011:         // FIXME(const-hack): Use `?` when available in const instead of `let-else`.\n  5012:         let Some((first, rem)) = self.split_first() else { return None };\n  5013:         *self = rem;\n  5014:         Some(first)\n  5015:     }\n  5016: \n  5017:     /// Removes the first element of the slice and returns a mutable\n  5018:     /// reference to it.\n  5019:     ///\n  5020:     /// Returns `None` if the slice is empty.\n  5021:     ///\n  5022:     /// # Examples\n  5023:     ///\n  5024:     /// ```\n  5025:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5026:     /// let first = slice.split_off_first_mut().unwrap();",
    "nanvix_source": "  5007:     /// ```\n  5008:     /// let mut slice: &[_] = &['a', 'b', 'c'];\n  5009:     /// let first = slice.split_off_first().unwrap();\n  5010:     ///\n  5011:     /// assert_eq!(slice, &['b', 'c']);\n  5012:     /// assert_eq!(first, &'a');\n  5013:     /// ```\n  5014:     #[inline]\n  5015:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5016:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5017:     pub const fn split_off_first<'a>(self: &mut &'a Self) -> Option<&'a T> {\n  5018:         // FIXME(const-hack): Use `?` when available in const instead of `let-else`.\n  5019:         let Some((first, rem)) = self.split_first() else { return None };\n  5020:         *self = rem;\n  5021:         Some(first)\n  5022:     }\n  5023: \n  5024:     /// Removes the first element of the slice and returns a mutable\n  5025:     /// reference to it.\n  5026:     ///\n  5027:     /// Returns `None` if the slice is empty.",
    "previous_skip_rationale": "The exact nested mutable-reference signature makes the determinism checker materialize the referenced slice as by-value `[T]`, which is unsized. No ordinary contract-only revision can preserve both the API signature and its observable post-state while avoiding this checker limitation."
  },
  {
    "target": "core::slice::split_off_last",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "split_off_last",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
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
                  "borrowed_ref": {
                    "is_mutable": false,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
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
                        "lifetime": "'a",
                        "type": {
                          "generic": "T"
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
    "verification_source": "  5044:     /// to it.\n  5045:     ///\n  5046:     /// Returns `None` if the slice is empty.\n  5047:     ///\n  5048:     /// # Examples\n  5049:     ///\n  5050:     /// ```\n  5051:     /// let mut slice: &[_] = &['a', 'b', 'c'];\n  5052:     /// let last = slice.split_off_last().unwrap();\n  5053:     ///\n  5054:     /// assert_eq!(slice, &['a', 'b']);\n  5055:     /// assert_eq!(last, &'c');\n  5056:     /// ```\n  5057:     #[inline]\n  5058:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5059:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5060:     pub const fn split_off_last<'a>(self: &mut &'a Self) -> Option<&'a T> {\n  5061:         // FIXME(const-hack): Use `?` when available in const instead of `let-else`.\n  5062:         let Some((last, rem)) = self.split_last() else { return None };\n  5063:         *self = rem;\n  5064:         Some(last)\n  5065:     }\n  5066: \n  5067:     /// Removes the last element of the slice and returns a mutable\n  5068:     /// reference to it.\n  5069:     ///\n  5070:     /// Returns `None` if the slice is empty.\n  5071:     ///\n  5072:     /// # Examples\n  5073:     ///\n  5074:     /// ```\n  5075:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5076:     /// let last = slice.split_off_last_mut().unwrap();",
    "nanvix_source": "  5057:     /// ```\n  5058:     /// let mut slice: &[_] = &['a', 'b', 'c'];\n  5059:     /// let last = slice.split_off_last().unwrap();\n  5060:     ///\n  5061:     /// assert_eq!(slice, &['a', 'b']);\n  5062:     /// assert_eq!(last, &'c');\n  5063:     /// ```\n  5064:     #[inline]\n  5065:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5066:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5067:     pub const fn split_off_last<'a>(self: &mut &'a Self) -> Option<&'a T> {\n  5068:         // FIXME(const-hack): Use `?` when available in const instead of `let-else`.\n  5069:         let Some((last, rem)) = self.split_last() else { return None };\n  5070:         *self = rem;\n  5071:         Some(last)\n  5072:     }\n  5073: \n  5074:     /// Removes the last element of the slice and returns a mutable\n  5075:     /// reference to it.\n  5076:     ///\n  5077:     /// Returns `None` if the slice is empty.",
    "previous_skip_rationale": "The exact nested mutable-reference signature makes the determinism checker materialize the referenced slice as by-value `[T]`, which is unsized. No ordinary contract-only revision can preserve both the API signature and its observable post-state while avoiding this checker limitation."
  },
  {
    "target": "core::slice::strip_circumfix",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
            "name": "S"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
                      "args": null,
                      "id": 54,
                      "path": "PartialEq"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 31660,
                      "path": "SlicePattern"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "S"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "T"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 31660,
                      "path": "SlicePattern"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "P"
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
      "name": "strip_circumfix",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "prefix",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "P"
                }
              }
            }
          ],
          [
            "suffix",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "S"
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
                          "slice": {
                            "generic": "T"
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
    "verification_source": "  2741:     /// # Examples\n  2742:     ///\n  2743:     /// ```\n  2744:     /// #![feature(strip_circumfix)]\n  2745:     ///\n  2746:     /// let v = &[10, 50, 40, 30];\n  2747:     /// assert_eq!(v.strip_circumfix(&[10], &[30]), Some(&[50, 40][..]));\n  2748:     /// assert_eq!(v.strip_circumfix(&[10], &[40, 30]), Some(&[50][..]));\n  2749:     /// assert_eq!(v.strip_circumfix(&[10, 50], &[40, 30]), Some(&[][..]));\n  2750:     /// assert_eq!(v.strip_circumfix(&[50], &[30]), None);\n  2751:     /// assert_eq!(v.strip_circumfix(&[10], &[40]), None);\n  2752:     /// assert_eq!(v.strip_circumfix(&[], &[40, 30]), Some(&[10, 50][..]));\n  2753:     /// assert_eq!(v.strip_circumfix(&[10, 50], &[]), Some(&[40, 30][..]));\n  2754:     /// ```\n  2755:     #[must_use = \"returns the subslice without modifying the original\"]\n  2756:     #[unstable(feature = \"strip_circumfix\", issue = \"147946\")]\n  2757:     pub fn strip_circumfix<S, P>(&self, prefix: &P, suffix: &S) -> Option<&[T]>\n  2758:     where\n  2759:         T: PartialEq,\n  2760:         S: SlicePattern<Item = T> + ?Sized,\n  2761:         P: SlicePattern<Item = T> + ?Sized,\n  2762:     {\n  2763:         self.strip_prefix(prefix)?.strip_suffix(suffix)\n  2764:     }\n  2765: \n  2766:     /// Returns a subslice with the optional prefix removed.\n  2767:     ///\n  2768:     /// If the slice starts with `prefix`, returns the subslice after the prefix.  If `prefix`\n  2769:     /// is empty or the slice does not start with `prefix`, simply returns the original slice.\n  2770:     /// If `prefix` is equal to the original slice, returns an empty slice.\n  2771:     ///\n  2772:     /// # Examples\n  2773:     ///",
    "nanvix_source": "  2753:     /// assert_eq!(v.strip_circumfix(&[10], &[40, 30]), Some(&[50][..]));\n  2754:     /// assert_eq!(v.strip_circumfix(&[10, 50], &[40, 30]), Some(&[][..]));\n  2755:     /// assert_eq!(v.strip_circumfix(&[50], &[30]), None);\n  2756:     /// assert_eq!(v.strip_circumfix(&[10], &[40]), None);\n  2757:     /// assert_eq!(v.strip_circumfix(&[], &[40, 30]), Some(&[10, 50][..]));\n  2758:     /// assert_eq!(v.strip_circumfix(&[10, 50], &[]), Some(&[40, 30][..]));\n  2759:     /// assert_eq!(v.strip_circumfix(&[10, 50, 40], &[50, 40, 30]), None);\n  2760:     /// ```\n  2761:     #[must_use = \"returns the subslice without modifying the original\"]\n  2762:     #[stable(feature = \"strip_circumfix\", since = \"CURRENT_RUSTC_VERSION\")]\n  2763:     pub fn strip_circumfix<S, P>(&self, prefix: &P, suffix: &S) -> Option<&[T]>\n  2764:     where\n  2765:         T: PartialEq,\n  2766:         S: SlicePattern<Item = T> + ?Sized,\n  2767:         P: SlicePattern<Item = T> + ?Sized,\n  2768:     {\n  2769:         self.strip_prefix(prefix)?.strip_suffix(suffix)\n  2770:     }\n  2771: \n  2772:     /// Returns a subslice with the optional prefix removed.\n  2773:     ///",
    "previous_skip_rationale": "Existing vstd vocabulary does not model SlicePattern::as_slice, so the prefix and suffix values or lengths cannot be related to the result. The source-justified contiguous-subslice property leaves both the Option discriminant and selected subrange undetermined, making it insufficient as an ordinary contract."
  },
  {
    "target": "core::slice::strip_prefix",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [],
                            "constraints": [
                              {
                                "args": null,
                                "binding": {
                                  "equality": {
                                    "type": {
                                      "generic": "T"
                                    }
                                  }
                                },
                                "name": "Item"
                              }
                            ]
                          }
                        },
                        "id": 31660,
                        "path": "SlicePattern"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 54,
                      "path": "PartialEq"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "strip_prefix",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "prefix",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "P"
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
                          "slice": {
                            "generic": "T"
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
    "verification_source": "  2666:     /// # Examples\n  2667:     ///\n  2668:     /// ```\n  2669:     /// let v = &[10, 40, 30];\n  2670:     /// assert_eq!(v.strip_prefix(&[10]), Some(&[40, 30][..]));\n  2671:     /// assert_eq!(v.strip_prefix(&[10, 40]), Some(&[30][..]));\n  2672:     /// assert_eq!(v.strip_prefix(&[10, 40, 30]), Some(&[][..]));\n  2673:     /// assert_eq!(v.strip_prefix(&[50]), None);\n  2674:     /// assert_eq!(v.strip_prefix(&[10, 50]), None);\n  2675:     ///\n  2676:     /// let prefix : &str = \"he\";\n  2677:     /// assert_eq!(b\"hello\".strip_prefix(prefix.as_bytes()),\n  2678:     ///            Some(b\"llo\".as_ref()));\n  2679:     /// ```\n  2680:     #[must_use = \"returns the subslice without modifying the original\"]\n  2681:     #[stable(feature = \"slice_strip\", since = \"1.51.0\")]\n  2682:     pub fn strip_prefix<P: SlicePattern<Item = T> + ?Sized>(&self, prefix: &P) -> Option<&[T]>\n  2683:     where\n  2684:         T: PartialEq,\n  2685:     {\n  2686:         // This function will need rewriting if and when SlicePattern becomes more sophisticated.\n  2687:         let prefix = prefix.as_slice();\n  2688:         let n = prefix.len();\n  2689:         if n <= self.len() {\n  2690:             let (head, tail) = self.split_at(n);\n  2691:             if head == prefix {\n  2692:                 return Some(tail);\n  2693:             }\n  2694:         }\n  2695:         None\n  2696:     }\n  2697: \n  2698:     /// Returns a subslice with the suffix removed.",
    "nanvix_source": "  2677:     /// assert_eq!(v.strip_prefix(&[10, 40, 30]), Some(&[][..]));\n  2678:     /// assert_eq!(v.strip_prefix(&[50]), None);\n  2679:     /// assert_eq!(v.strip_prefix(&[10, 50]), None);\n  2680:     ///\n  2681:     /// let prefix : &str = \"he\";\n  2682:     /// assert_eq!(b\"hello\".strip_prefix(prefix.as_bytes()),\n  2683:     ///            Some(b\"llo\".as_ref()));\n  2684:     /// ```\n  2685:     #[must_use = \"returns the subslice without modifying the original\"]\n  2686:     #[stable(feature = \"slice_strip\", since = \"1.51.0\")]\n  2687:     pub fn strip_prefix<P: SlicePattern<Item = T> + ?Sized>(&self, prefix: &P) -> Option<&[T]>\n  2688:     where\n  2689:         T: PartialEq,\n  2690:     {\n  2691:         // This function will need rewriting if and when SlicePattern becomes more sophisticated.\n  2692:         let prefix = prefix.as_slice();\n  2693:         let n = prefix.len();\n  2694:         if n <= self.len() {\n  2695:             let (head, tail) = self.split_at(n);\n  2696:             if head == prefix {\n  2697:                 return Some(tail);",
    "previous_skip_rationale": "vstd has no public semantic model for SlicePattern::as_slice. The source only justifies that a Some result is some suffix of slice, leaving both the Option discriminant and removed-prefix length undetermined; this is insufficient as a useful ordinary contract."
  },
  {
    "target": "core::slice::strip_suffix",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [
      "must_compare_semantic_view_not_reference_identity"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [],
                            "constraints": [
                              {
                                "args": null,
                                "binding": {
                                  "equality": {
                                    "type": {
                                      "generic": "T"
                                    }
                                  }
                                },
                                "name": "Item"
                              }
                            ]
                          }
                        },
                        "id": 31660,
                        "path": "SlicePattern"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 54,
                      "path": "PartialEq"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "strip_suffix",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "suffix",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "P"
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
                          "slice": {
                            "generic": "T"
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
    "verification_source": "  2702:     /// original slice, returns an empty slice.\n  2703:     ///\n  2704:     /// If the slice does not end with `suffix`, returns `None`.\n  2705:     ///\n  2706:     /// # Examples\n  2707:     ///\n  2708:     /// ```\n  2709:     /// let v = &[10, 40, 30];\n  2710:     /// assert_eq!(v.strip_suffix(&[30]), Some(&[10, 40][..]));\n  2711:     /// assert_eq!(v.strip_suffix(&[40, 30]), Some(&[10][..]));\n  2712:     /// assert_eq!(v.strip_suffix(&[10, 40, 30]), Some(&[][..]));\n  2713:     /// assert_eq!(v.strip_suffix(&[50]), None);\n  2714:     /// assert_eq!(v.strip_suffix(&[50, 30]), None);\n  2715:     /// ```\n  2716:     #[must_use = \"returns the subslice without modifying the original\"]\n  2717:     #[stable(feature = \"slice_strip\", since = \"1.51.0\")]\n  2718:     pub fn strip_suffix<P: SlicePattern<Item = T> + ?Sized>(&self, suffix: &P) -> Option<&[T]>\n  2719:     where\n  2720:         T: PartialEq,\n  2721:     {\n  2722:         // This function will need rewriting if and when SlicePattern becomes more sophisticated.\n  2723:         let suffix = suffix.as_slice();\n  2724:         let (len, n) = (self.len(), suffix.len());\n  2725:         if n <= len {\n  2726:             let (head, tail) = self.split_at(len - n);\n  2727:             if tail == suffix {\n  2728:                 return Some(head);\n  2729:             }\n  2730:         }\n  2731:         None\n  2732:     }\n  2733: \n  2734:     /// Returns a subslice with the prefix and suffix removed.",
    "nanvix_source": "  2713:     /// ```\n  2714:     /// let v = &[10, 40, 30];\n  2715:     /// assert_eq!(v.strip_suffix(&[30]), Some(&[10, 40][..]));\n  2716:     /// assert_eq!(v.strip_suffix(&[40, 30]), Some(&[10][..]));\n  2717:     /// assert_eq!(v.strip_suffix(&[10, 40, 30]), Some(&[][..]));\n  2718:     /// assert_eq!(v.strip_suffix(&[50]), None);\n  2719:     /// assert_eq!(v.strip_suffix(&[50, 30]), None);\n  2720:     /// ```\n  2721:     #[must_use = \"returns the subslice without modifying the original\"]\n  2722:     #[stable(feature = \"slice_strip\", since = \"1.51.0\")]\n  2723:     pub fn strip_suffix<P: SlicePattern<Item = T> + ?Sized>(&self, suffix: &P) -> Option<&[T]>\n  2724:     where\n  2725:         T: PartialEq,\n  2726:     {\n  2727:         // This function will need rewriting if and when SlicePattern becomes more sophisticated.\n  2728:         let suffix = suffix.as_slice();\n  2729:         let (len, n) = (self.len(), suffix.len());\n  2730:         if n <= len {\n  2731:             let (head, tail) = self.split_at(len - n);\n  2732:             if tail == suffix {\n  2733:                 return Some(head);",
    "previous_skip_rationale": "Verus lacks a vstd declaration and semantic model for SlicePattern and as_slice, and its associated Item projection makes the ordinary determinism harness ill-typed. Without that model, only a nondeterministic prefix property is source-justified; determining success or the returned prefix length would require false domain restrictions or an ungrounded model."
  },
  {
    "target": "core::slice::subslice_range",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "subslice_range",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "subslice",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "primitive": "usize"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 9993,
                        "path": "core::range::Range"
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
    "verification_source": "  5299:     /// #![feature(substr_range)]\n  5300:     /// use core::range::Range;\n  5301:     ///\n  5302:     /// let nums = &[0, 5, 10, 0, 0, 5];\n  5303:     ///\n  5304:     /// let mut iter = nums\n  5305:     ///     .split(|t| *t == 0)\n  5306:     ///     .map(|n| nums.subslice_range(n).unwrap());\n  5307:     ///\n  5308:     /// assert_eq!(iter.next(), Some(Range { start: 0, end: 0 }));\n  5309:     /// assert_eq!(iter.next(), Some(Range { start: 1, end: 3 }));\n  5310:     /// assert_eq!(iter.next(), Some(Range { start: 4, end: 4 }));\n  5311:     /// assert_eq!(iter.next(), Some(Range { start: 5, end: 6 }));\n  5312:     /// ```\n  5313:     #[must_use]\n  5314:     #[unstable(feature = \"substr_range\", issue = \"126769\")]\n  5315:     pub fn subslice_range(&self, subslice: &[T]) -> Option<core::range::Range<usize>> {\n  5316:         if T::IS_ZST {\n  5317:             panic!(\"elements are zero-sized\");\n  5318:         }\n  5319: \n  5320:         let self_start = self.as_ptr().addr();\n  5321:         let subslice_start = subslice.as_ptr().addr();\n  5322: \n  5323:         let byte_start = subslice_start.wrapping_sub(self_start);\n  5324: \n  5325:         if !byte_start.is_multiple_of(size_of::<T>()) {\n  5326:             return None;\n  5327:         }\n  5328: \n  5329:         let start = byte_start / size_of::<T>();\n  5330:         let end = start.wrapping_add(subslice.len());\n  5331: ",
    "nanvix_source": "  5311:     ///     .split(|t| *t == 0)\n  5312:     ///     .map(|n| nums.subslice_range(n).unwrap());\n  5313:     ///\n  5314:     /// assert_eq!(iter.next(), Some(Range { start: 0, end: 0 }));\n  5315:     /// assert_eq!(iter.next(), Some(Range { start: 1, end: 3 }));\n  5316:     /// assert_eq!(iter.next(), Some(Range { start: 4, end: 4 }));\n  5317:     /// assert_eq!(iter.next(), Some(Range { start: 5, end: 6 }));\n  5318:     /// ```\n  5319:     #[must_use]\n  5320:     #[stable(feature = \"substr_range\", since = \"CURRENT_RUSTC_VERSION\")]\n  5321:     pub fn subslice_range(&self, subslice: &[T]) -> Option<core::range::Range<usize>> {\n  5322:         if T::IS_ZST {\n  5323:             panic!(\"elements are zero-sized\");\n  5324:         }\n  5325: \n  5326:         let self_start = self.as_ptr().addr();\n  5327:         let subslice_start = subslice.as_ptr().addr();\n  5328: \n  5329:         let byte_start = subslice_start.wrapping_sub(self_start);\n  5330: \n  5331:         if !byte_start.is_multiple_of(size_of::<T>()) {",
    "previous_skip_rationale": "The return type core::range::Range is not modeled by existing vstd, and the result depends on pointer addresses, alignment, and provenance rather than slice views. Adding a new external type specification would not make success or the returned range determinable from existing semantic inputs. No useful deterministic ordinary contract is therefore available."
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
