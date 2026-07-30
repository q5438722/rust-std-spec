For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::chunk_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "chunk_by",
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
            "pred",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10078,
            "path": "ChunkBy"
          }
        }
      }
    },
    "verification_source": "  1848:     ///\n  1849:     /// This method can be used to extract the sorted subslices:\n  1850:     ///\n  1851:     /// ```\n  1852:     /// let slice = &[1, 1, 2, 3, 2, 3, 2, 3, 4];\n  1853:     ///\n  1854:     /// let mut iter = slice.chunk_by(|a, b| a <= b);\n  1855:     ///\n  1856:     /// assert_eq!(iter.next(), Some(&[1, 1, 2, 3][..]));\n  1857:     /// assert_eq!(iter.next(), Some(&[2, 3][..]));\n  1858:     /// assert_eq!(iter.next(), Some(&[2, 3, 4][..]));\n  1859:     /// assert_eq!(iter.next(), None);\n  1860:     /// ```\n  1861:     #[stable(feature = \"slice_group_by\", since = \"1.77.0\")]\n  1862:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1863:     #[inline]\n  1864:     pub const fn chunk_by<F>(&self, pred: F) -> ChunkBy<'_, T, F>\n  1865:     where\n  1866:         F: FnMut(&T, &T) -> bool,\n  1867:     {\n  1868:         ChunkBy::new(self, pred)\n  1869:     }\n  1870: \n  1871:     /// Returns an iterator over the slice producing non-overlapping mutable\n  1872:     /// runs of elements using the predicate to separate them.\n  1873:     ///\n  1874:     /// The predicate is called for every pair of consecutive elements,\n  1875:     /// meaning that it is called on `slice[0]` and `slice[1]`,\n  1876:     /// followed by `slice[1]` and `slice[2]`, and so on.\n  1877:     ///\n  1878:     /// # Examples\n  1879:     ///\n  1880:     /// ```",
    "nanvix_source": "  1857:     /// let mut iter = slice.chunk_by(|a, b| a <= b);\n  1858:     ///\n  1859:     /// assert_eq!(iter.next(), Some(&[1, 1, 2, 3][..]));\n  1860:     /// assert_eq!(iter.next(), Some(&[2, 3][..]));\n  1861:     /// assert_eq!(iter.next(), Some(&[2, 3, 4][..]));\n  1862:     /// assert_eq!(iter.next(), None);\n  1863:     /// ```\n  1864:     #[stable(feature = \"slice_group_by\", since = \"1.77.0\")]\n  1865:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1866:     #[inline]\n  1867:     pub const fn chunk_by<F>(&self, pred: F) -> ChunkBy<'_, T, F>\n  1868:     where\n  1869:         F: FnMut(&T, &T) -> bool,\n  1870:     {\n  1871:         ChunkBy::new(self, pred)\n  1872:     }\n  1873: \n  1874:     /// Returns an iterator over the slice producing non-overlapping mutable\n  1875:     /// runs of elements using the predicate to separate them.\n  1876:     ///\n  1877:     /// The predicate is called for every pair of consecutive elements,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::chunk_by_mut",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "chunk_by_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pred",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13464,
            "path": "ChunkByMut"
          }
        }
      }
    },
    "verification_source": "  1890:     ///\n  1891:     /// This method can be used to extract the sorted subslices:\n  1892:     ///\n  1893:     /// ```\n  1894:     /// let slice = &mut [1, 1, 2, 3, 2, 3, 2, 3, 4];\n  1895:     ///\n  1896:     /// let mut iter = slice.chunk_by_mut(|a, b| a <= b);\n  1897:     ///\n  1898:     /// assert_eq!(iter.next(), Some(&mut [1, 1, 2, 3][..]));\n  1899:     /// assert_eq!(iter.next(), Some(&mut [2, 3][..]));\n  1900:     /// assert_eq!(iter.next(), Some(&mut [2, 3, 4][..]));\n  1901:     /// assert_eq!(iter.next(), None);\n  1902:     /// ```\n  1903:     #[stable(feature = \"slice_group_by\", since = \"1.77.0\")]\n  1904:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1905:     #[inline]\n  1906:     pub const fn chunk_by_mut<F>(&mut self, pred: F) -> ChunkByMut<'_, T, F>\n  1907:     where\n  1908:         F: FnMut(&T, &T) -> bool,\n  1909:     {\n  1910:         ChunkByMut::new(self, pred)\n  1911:     }\n  1912: \n  1913:     /// Divides one slice into two at an index.\n  1914:     ///\n  1915:     /// The first will contain all indices from `[0, mid)` (excluding\n  1916:     /// the index `mid` itself) and the second will contain all\n  1917:     /// indices from `[mid, len)` (excluding the index `len` itself).\n  1918:     ///\n  1919:     /// # Panics\n  1920:     ///\n  1921:     /// Panics if `mid > len`.  For a non-panicking alternative see\n  1922:     /// [`split_at_checked`](slice::split_at_checked).",
    "nanvix_source": "  1899:     /// let mut iter = slice.chunk_by_mut(|a, b| a <= b);\n  1900:     ///\n  1901:     /// assert_eq!(iter.next(), Some(&mut [1, 1, 2, 3][..]));\n  1902:     /// assert_eq!(iter.next(), Some(&mut [2, 3][..]));\n  1903:     /// assert_eq!(iter.next(), Some(&mut [2, 3, 4][..]));\n  1904:     /// assert_eq!(iter.next(), None);\n  1905:     /// ```\n  1906:     #[stable(feature = \"slice_group_by\", since = \"1.77.0\")]\n  1907:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1908:     #[inline]\n  1909:     pub const fn chunk_by_mut<F>(&mut self, pred: F) -> ChunkByMut<'_, T, F>\n  1910:     where\n  1911:         F: FnMut(&T, &T) -> bool,\n  1912:     {\n  1913:         ChunkByMut::new(self, pred)\n  1914:     }\n  1915: \n  1916:     /// Divides one slice into two at an index.\n  1917:     ///\n  1918:     /// The first will contain all indices from `[0, mid)` (excluding\n  1919:     /// the index `mid` itself) and the second will contain all",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::fill_with",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                            "generic": "T"
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
      "name": "fill_with",
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
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4174:     ///\n  4175:     /// This method uses a closure to create new values. If you'd rather\n  4176:     /// [`Clone`] a given value, use [`fill`]. If you want to use the [`Default`]\n  4177:     /// trait to generate values, you can pass [`Default::default`] as the\n  4178:     /// argument.\n  4179:     ///\n  4180:     /// [`fill`]: slice::fill\n  4181:     ///\n  4182:     /// # Examples\n  4183:     ///\n  4184:     /// ```\n  4185:     /// let mut buf = vec![1; 10];\n  4186:     /// buf.fill_with(Default::default);\n  4187:     /// assert_eq!(buf, vec![0; 10]);\n  4188:     /// ```\n  4189:     #[stable(feature = \"slice_fill_with\", since = \"1.51.0\")]\n  4190:     pub fn fill_with<F>(&mut self, mut f: F)\n  4191:     where\n  4192:         F: FnMut() -> T,\n  4193:     {\n  4194:         for el in self {\n  4195:             *el = f();\n  4196:         }\n  4197:     }\n  4198: \n  4199:     /// Copies the elements from `src` into `self`.\n  4200:     ///\n  4201:     /// The length of `src` must be the same as `self`.\n  4202:     ///\n  4203:     /// # Panics\n  4204:     ///\n  4205:     /// This function will panic if the two slices have different lengths.\n  4206:     ///",
    "nanvix_source": "  4186:     /// [`fill`]: slice::fill\n  4187:     ///\n  4188:     /// # Examples\n  4189:     ///\n  4190:     /// ```\n  4191:     /// let mut buf = vec![1; 10];\n  4192:     /// buf.fill_with(Default::default);\n  4193:     /// assert_eq!(buf, vec![0; 10]);\n  4194:     /// ```\n  4195:     #[stable(feature = \"slice_fill_with\", since = \"1.51.0\")]\n  4196:     pub fn fill_with<F>(&mut self, mut f: F)\n  4197:     where\n  4198:         F: FnMut() -> T,\n  4199:     {\n  4200:         for el in self {\n  4201:             *el = f();\n  4202:         }\n  4203:     }\n  4204: \n  4205:     /// Copies the elements from `src` into `self`.\n  4206:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::is_sorted_by",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
      "name": "is_sorted_by",
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
                "lifetime": "'a",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "compare",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4755:     ///\n  4756:     /// # Examples\n  4757:     ///\n  4758:     /// ```\n  4759:     /// assert!([1, 2, 2, 9].is_sorted_by(|a, b| a <= b));\n  4760:     /// assert!(![1, 2, 2, 9].is_sorted_by(|a, b| a < b));\n  4761:     ///\n  4762:     /// assert!([0].is_sorted_by(|a, b| true));\n  4763:     /// assert!([0].is_sorted_by(|a, b| false));\n  4764:     ///\n  4765:     /// let empty: [i32; 0] = [];\n  4766:     /// assert!(empty.is_sorted_by(|a, b| false));\n  4767:     /// assert!(empty.is_sorted_by(|a, b| true));\n  4768:     /// ```\n  4769:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4770:     #[must_use]\n  4771:     pub fn is_sorted_by<'a, F>(&'a self, mut compare: F) -> bool\n  4772:     where\n  4773:         F: FnMut(&'a T, &'a T) -> bool,\n  4774:     {\n  4775:         self.array_windows().all(|[a, b]| compare(a, b))\n  4776:     }\n  4777: \n  4778:     /// Checks if the elements of this slice are sorted using the given key extraction function.\n  4779:     ///\n  4780:     /// Instead of comparing the slice's elements directly, this function compares the keys of the\n  4781:     /// elements, as determined by `f`. Apart from that, it's equivalent to [`is_sorted`]; see its\n  4782:     /// documentation for more information.\n  4783:     ///\n  4784:     /// [`is_sorted`]: slice::is_sorted\n  4785:     ///\n  4786:     /// # Examples\n  4787:     ///",
    "nanvix_source": "  4768:     ///\n  4769:     /// assert!([0].is_sorted_by(|a, b| true));\n  4770:     /// assert!([0].is_sorted_by(|a, b| false));\n  4771:     ///\n  4772:     /// let empty: [i32; 0] = [];\n  4773:     /// assert!(empty.is_sorted_by(|a, b| false));\n  4774:     /// assert!(empty.is_sorted_by(|a, b| true));\n  4775:     /// ```\n  4776:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4777:     #[must_use]\n  4778:     pub fn is_sorted_by<'a, F>(&'a self, mut compare: F) -> bool\n  4779:     where\n  4780:         F: FnMut(&'a T, &'a T) -> bool,\n  4781:     {\n  4782:         self.array_windows().all(|[a, b]| compare(a, b))\n  4783:     }\n  4784: \n  4785:     /// Checks if the elements of this slice are sorted using the given key extraction function.\n  4786:     ///\n  4787:     /// Instead of comparing the slice's elements directly, this function compares the keys of the\n  4788:     /// elements, as determined by `f`. Apart from that, it's equivalent to [`is_sorted`]; see its",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::is_sorted_by_key",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
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
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": "'a",
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "K"
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
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
      "name": "is_sorted_by_key",
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
                "lifetime": "'a",
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4779:     ///\n  4780:     /// Instead of comparing the slice's elements directly, this function compares the keys of the\n  4781:     /// elements, as determined by `f`. Apart from that, it's equivalent to [`is_sorted`]; see its\n  4782:     /// documentation for more information.\n  4783:     ///\n  4784:     /// [`is_sorted`]: slice::is_sorted\n  4785:     ///\n  4786:     /// # Examples\n  4787:     ///\n  4788:     /// ```\n  4789:     /// assert!([\"c\", \"bb\", \"aaa\"].is_sorted_by_key(|s| s.len()));\n  4790:     /// assert!(![-2i32, -1, 0, 3].is_sorted_by_key(|n| n.abs()));\n  4791:     /// ```\n  4792:     #[inline]\n  4793:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4794:     #[must_use]\n  4795:     pub fn is_sorted_by_key<'a, F, K>(&'a self, f: F) -> bool\n  4796:     where\n  4797:         F: FnMut(&'a T) -> K,\n  4798:         K: PartialOrd,\n  4799:     {\n  4800:         self.iter().is_sorted_by_key(f)\n  4801:     }\n  4802: \n  4803:     /// Returns the index of the partition point according to the given predicate\n  4804:     /// (the index of the first element of the second partition).\n  4805:     ///\n  4806:     /// The slice is assumed to be partitioned according to the given predicate.\n  4807:     /// This means that all elements for which the predicate returns true are at the start of the slice\n  4808:     /// and all elements for which the predicate returns false are at the end.\n  4809:     /// For example, `[7, 15, 3, 5, 4, 12, 6]` is partitioned under the predicate `x % 2 != 0`\n  4810:     /// (all odd numbers are at the start, all even at the end).\n  4811:     ///",
    "nanvix_source": "  4792:     ///\n  4793:     /// # Examples\n  4794:     ///\n  4795:     /// ```\n  4796:     /// assert!([\"c\", \"bb\", \"aaa\"].is_sorted_by_key(|s| s.len()));\n  4797:     /// assert!(![-2i32, -1, 0, 3].is_sorted_by_key(|n| n.abs()));\n  4798:     /// ```\n  4799:     #[inline]\n  4800:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4801:     #[must_use]\n  4802:     pub fn is_sorted_by_key<'a, F, K>(&'a self, f: F) -> bool\n  4803:     where\n  4804:         F: FnMut(&'a T) -> K,\n  4805:         K: PartialOrd,\n  4806:     {\n  4807:         self.iter().is_sorted_by_key(f)\n  4808:     }\n  4809: \n  4810:     /// Returns the index of the partition point according to the given predicate\n  4811:     /// (the index of the first element of the second partition).\n  4812:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::partition_point",
    "generation_group": "higher_order_contract",
    "classification": "higher_order_contract",
    "classification_reasons": [
      "closure_call_ensures_or_prophetic_model_required"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
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
      "name": "partition_point",
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
            "pred",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  4838:     /// let a: [i32; 0] = [];\n  4839:     /// assert_eq!(a.partition_point(|x| x < &100), 0);\n  4840:     /// ```\n  4841:     ///\n  4842:     /// If you want to insert an item to a sorted vector, while maintaining\n  4843:     /// sort order:\n  4844:     ///\n  4845:     /// ```\n  4846:     /// let mut s = vec![0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55];\n  4847:     /// let num = 42;\n  4848:     /// let idx = s.partition_point(|&x| x <= num);\n  4849:     /// s.insert(idx, num);\n  4850:     /// assert_eq!(s, [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  4851:     /// ```\n  4852:     #[stable(feature = \"partition_point\", since = \"1.52.0\")]\n  4853:     #[must_use]\n  4854:     pub fn partition_point<P>(&self, mut pred: P) -> usize\n  4855:     where\n  4856:         P: FnMut(&T) -> bool,\n  4857:     {\n  4858:         self.binary_search_by(|x| if pred(x) { Less } else { Greater }).unwrap_or_else(|i| i)\n  4859:     }\n  4860: \n  4861:     /// Removes the subslice corresponding to the given range\n  4862:     /// and returns a reference to it.\n  4863:     ///\n  4864:     /// Returns `None` and does not modify the slice if the given\n  4865:     /// range is out of bounds.\n  4866:     ///\n  4867:     /// Note that this method only accepts one-sided ranges such as\n  4868:     /// `2..` or `..6`, but not `2..6`.\n  4869:     ///\n  4870:     /// # Examples",
    "nanvix_source": "  4851:     ///\n  4852:     /// ```\n  4853:     /// let mut s = vec![0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55];\n  4854:     /// let num = 42;\n  4855:     /// let idx = s.partition_point(|&x| x <= num);\n  4856:     /// s.insert(idx, num);\n  4857:     /// assert_eq!(s, [0, 1, 1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 42, 55]);\n  4858:     /// ```\n  4859:     #[stable(feature = \"partition_point\", since = \"1.52.0\")]\n  4860:     #[must_use]\n  4861:     pub fn partition_point<P>(&self, mut pred: P) -> usize\n  4862:     where\n  4863:         P: FnMut(&T) -> bool,\n  4864:     {\n  4865:         self.binary_search_by(|x| if pred(x) { Less } else { Greater }).unwrap_or_else(|i| i)\n  4866:     }\n  4867: \n  4868:     /// Removes the subslice corresponding to the given range\n  4869:     /// and returns a reference to it.\n  4870:     ///\n  4871:     /// Returns `None` and does not modify the slice if the given",
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
