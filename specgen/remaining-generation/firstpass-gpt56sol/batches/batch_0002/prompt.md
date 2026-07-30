For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::str::rsplit_once",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
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
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "rsplit_once",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "delimiter",
            {
              "generic": "P"
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
                      "tuple": [
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "primitive": "str"
                            }
                          }
                        },
                        {
                          "borrowed_ref": {
                            "is_mutable": false,
                            "lifetime": null,
                            "type": {
                              "primitive": "str"
                            }
                          }
                        }
                      ]
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
    "verification_source": "  1969:         unsafe { Some((self.get_unchecked(..start), self.get_unchecked(end..))) }\n  1970:     }\n  1971: \n  1972:     /// Splits the string on the last occurrence of the specified delimiter and\n  1973:     /// returns prefix before delimiter and suffix after delimiter.\n  1974:     ///\n  1975:     /// # Examples\n  1976:     ///\n  1977:     /// ```\n  1978:     /// assert_eq!(\"cfg\".rsplit_once('='), None);\n  1979:     /// assert_eq!(\"cfg=\".rsplit_once('='), Some((\"cfg\", \"\")));\n  1980:     /// assert_eq!(\"cfg=foo\".rsplit_once('='), Some((\"cfg\", \"foo\")));\n  1981:     /// assert_eq!(\"cfg=foo=bar\".rsplit_once('='), Some((\"cfg=foo\", \"bar\")));\n  1982:     /// ```\n  1983:     #[stable(feature = \"str_split_once\", since = \"1.52.0\")]\n  1984:     #[inline]\n  1985:     pub fn rsplit_once<P: Pattern>(&self, delimiter: P) -> Option<(&'_ str, &'_ str)>\n  1986:     where\n  1987:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1988:     {\n  1989:         let (start, end) = delimiter.into_searcher(self).next_match_back()?;\n  1990:         // SAFETY: `Searcher` is known to return valid indices.\n  1991:         unsafe { Some((self.get_unchecked(..start), self.get_unchecked(end..))) }\n  1992:     }\n  1993: \n  1994:     /// Returns an iterator over the disjoint matches of a pattern within the\n  1995:     /// given string slice.\n  1996:     ///\n  1997:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1998:     /// function or closure that determines if a character matches.\n  1999:     ///\n  2000:     /// [`char`]: prim@char\n  2001:     /// [pattern]: self::pattern",
    "nanvix_source": "  1994:     /// # Examples\n  1995:     ///\n  1996:     /// ```\n  1997:     /// assert_eq!(\"cfg\".rsplit_once('='), None);\n  1998:     /// assert_eq!(\"cfg=\".rsplit_once('='), Some((\"cfg\", \"\")));\n  1999:     /// assert_eq!(\"cfg=foo\".rsplit_once('='), Some((\"cfg\", \"foo\")));\n  2000:     /// assert_eq!(\"cfg=foo=bar\".rsplit_once('='), Some((\"cfg=foo\", \"bar\")));\n  2001:     /// ```\n  2002:     #[stable(feature = \"str_split_once\", since = \"1.52.0\")]\n  2003:     #[inline]\n  2004:     pub fn rsplit_once<P: Pattern>(&self, delimiter: P) -> Option<(&'_ str, &'_ str)>\n  2005:     where\n  2006:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2007:     {\n  2008:         let (start, end) = delimiter.into_searcher(self).next_match_back()?;\n  2009:         // SAFETY: `Searcher` is known to return valid indices.\n  2010:         unsafe { Some((self.get_unchecked(..start), self.get_unchecked(end..))) }\n  2011:     }\n  2012: \n  2013:     /// Returns an iterator over the disjoint matches of a pattern within the\n  2014:     /// given string slice.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rsplit_terminator",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
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
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "rsplit_terminator",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
            {
              "generic": "P"
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
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10109,
            "path": "RSplitTerminator"
          }
        }
      }
    },
    "verification_source": "  1826:     /// [`split_terminator`]: str::split_terminator\n  1827:     ///\n  1828:     /// # Examples\n  1829:     ///\n  1830:     /// ```\n  1831:     /// let v: Vec<&str> = \"A.B.\".rsplit_terminator('.').collect();\n  1832:     /// assert_eq!(v, [\"B\", \"A\"]);\n  1833:     ///\n  1834:     /// let v: Vec<&str> = \"A..B..\".rsplit_terminator(\".\").collect();\n  1835:     /// assert_eq!(v, [\"\", \"B\", \"\", \"A\"]);\n  1836:     ///\n  1837:     /// let v: Vec<&str> = \"A.B:C.D\".rsplit_terminator(&['.', ':'][..]).collect();\n  1838:     /// assert_eq!(v, [\"D\", \"C\", \"B\", \"A\"]);\n  1839:     /// ```\n  1840:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1841:     #[inline]\n  1842:     pub fn rsplit_terminator<P: Pattern>(&self, pat: P) -> RSplitTerminator<'_, P>\n  1843:     where\n  1844:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1845:     {\n  1846:         RSplitTerminator(self.split_terminator(pat).0)\n  1847:     }\n  1848: \n  1849:     /// Returns an iterator over substrings of the given string slice, separated\n  1850:     /// by a pattern, restricted to returning at most `n` items.\n  1851:     ///\n  1852:     /// If `n` substrings are returned, the last substring (the `n`th substring)\n  1853:     /// will contain the remainder of the string.\n  1854:     ///\n  1855:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1856:     /// function or closure that determines if a character matches.\n  1857:     ///\n  1858:     /// [`char`]: prim@char",
    "nanvix_source": "  1851:     /// assert_eq!(v, [\"B\", \"A\"]);\n  1852:     ///\n  1853:     /// let v: Vec<&str> = \"A..B..\".rsplit_terminator(\".\").collect();\n  1854:     /// assert_eq!(v, [\"\", \"B\", \"\", \"A\"]);\n  1855:     ///\n  1856:     /// let v: Vec<&str> = \"A.B:C.D\".rsplit_terminator(&['.', ':'][..]).collect();\n  1857:     /// assert_eq!(v, [\"D\", \"C\", \"B\", \"A\"]);\n  1858:     /// ```\n  1859:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1860:     #[inline]\n  1861:     pub fn rsplit_terminator<P: Pattern>(&self, pat: P) -> RSplitTerminator<'_, P>\n  1862:     where\n  1863:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1864:     {\n  1865:         RSplitTerminator(self.split_terminator(pat).0)\n  1866:     }\n  1867: \n  1868:     /// Returns an iterator over substrings of the given string slice, separated\n  1869:     /// by a pattern, restricted to returning at most `n` items.\n  1870:     ///\n  1871:     /// If `n` substrings are returned, the last substring (the `n`th substring)",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::rsplitn",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
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
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "rsplitn",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "n",
            {
              "primitive": "usize"
            }
          ],
          [
            "pat",
            {
              "generic": "P"
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
                      "generic": "P"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10115,
            "path": "RSplitN"
          }
        }
      }
    },
    "verification_source": "  1930:     ///\n  1931:     /// let v: Vec<&str> = \"lionXXtigerXleopard\".rsplitn(3, 'X').collect();\n  1932:     /// assert_eq!(v, [\"leopard\", \"tiger\", \"lionX\"]);\n  1933:     ///\n  1934:     /// let v: Vec<&str> = \"lion::tiger::leopard\".rsplitn(2, \"::\").collect();\n  1935:     /// assert_eq!(v, [\"leopard\", \"lion::tiger\"]);\n  1936:     /// ```\n  1937:     ///\n  1938:     /// A more complex pattern, using a closure:\n  1939:     ///\n  1940:     /// ```\n  1941:     /// let v: Vec<&str> = \"abc1defXghi\".rsplitn(2, |c| c == '1' || c == 'X').collect();\n  1942:     /// assert_eq!(v, [\"ghi\", \"abc1def\"]);\n  1943:     /// ```\n  1944:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1945:     #[inline]\n  1946:     pub fn rsplitn<P: Pattern>(&self, n: usize, pat: P) -> RSplitN<'_, P>\n  1947:     where\n  1948:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1949:     {\n  1950:         RSplitN(self.splitn(n, pat).0)\n  1951:     }\n  1952: \n  1953:     /// Splits the string on the first occurrence of the specified delimiter and\n  1954:     /// returns prefix before delimiter and suffix after delimiter.\n  1955:     ///\n  1956:     /// # Examples\n  1957:     ///\n  1958:     /// ```\n  1959:     /// assert_eq!(\"cfg\".split_once('='), None);\n  1960:     /// assert_eq!(\"cfg=\".split_once('='), Some((\"cfg\", \"\")));\n  1961:     /// assert_eq!(\"cfg=foo\".split_once('='), Some((\"cfg\", \"foo\")));\n  1962:     /// assert_eq!(\"cfg=foo=bar\".split_once('='), Some((\"cfg\", \"foo=bar\")));",
    "nanvix_source": "  1955:     /// ```\n  1956:     ///\n  1957:     /// A more complex pattern, using a closure:\n  1958:     ///\n  1959:     /// ```\n  1960:     /// let v: Vec<&str> = \"abc1defXghi\".rsplitn(2, |c| c == '1' || c == 'X').collect();\n  1961:     /// assert_eq!(v, [\"ghi\", \"abc1def\"]);\n  1962:     /// ```\n  1963:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1964:     #[inline]\n  1965:     pub fn rsplitn<P: Pattern>(&self, n: usize, pat: P) -> RSplitN<'_, P>\n  1966:     where\n  1967:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1968:     {\n  1969:         RSplitN(self.splitn(n, pat).0)\n  1970:     }\n  1971: \n  1972:     /// Splits the string on the first occurrence of the specified delimiter and\n  1973:     /// returns prefix before delimiter and suffix after delimiter.\n  1974:     ///\n  1975:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::strip_circumfix",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "S"
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "lifetime": "'a"
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "S"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
              "generic": "P"
            }
          ],
          [
            "suffix",
            {
              "generic": "S"
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
                          "primitive": "str"
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
    "verification_source": "  2487:     /// [pattern]: self::pattern\n  2488:     /// [`trim_start_matches`]: Self::trim_start_matches\n  2489:     /// [`trim_end_matches`]: Self::trim_end_matches\n  2490:     ///\n  2491:     /// # Examples\n  2492:     ///\n  2493:     /// ```\n  2494:     /// #![feature(strip_circumfix)]\n  2495:     ///\n  2496:     /// assert_eq!(\"bar:hello:foo\".strip_circumfix(\"bar:\", \":foo\"), Some(\"hello\"));\n  2497:     /// assert_eq!(\"bar:foo\".strip_circumfix(\"foo\", \"foo\"), None);\n  2498:     /// assert_eq!(\"foo:bar;\".strip_circumfix(\"foo:\", ';'), Some(\"bar\"));\n  2499:     /// ```\n  2500:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2501:                   without modifying the original\"]\n  2502:     #[unstable(feature = \"strip_circumfix\", issue = \"147946\")]\n  2503:     pub fn strip_circumfix<P: Pattern, S: Pattern>(&self, prefix: P, suffix: S) -> Option<&str>\n  2504:     where\n  2505:         for<'a> S::Searcher<'a>: ReverseSearcher<'a>,\n  2506:     {\n  2507:         self.strip_prefix(prefix)?.strip_suffix(suffix)\n  2508:     }\n  2509: \n  2510:     /// Returns a string slice with the optional prefix removed.\n  2511:     ///\n  2512:     /// If the string starts with the pattern `prefix`, returns the substring after the prefix.\n  2513:     /// Unlike [`strip_prefix`], this method always returns `&str` for easy method chaining,\n  2514:     /// instead of returning [`Option<&str>`].\n  2515:     ///\n  2516:     /// If the string does not start with `prefix`, returns the original string unchanged.\n  2517:     ///\n  2518:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  2519:     /// function or closure that determines if a character matches.",
    "nanvix_source": "  2513:     ///\n  2514:     /// ```\n  2515:     /// assert_eq!(\"bar:hello:foo\".strip_circumfix(\"bar:\", \":foo\"), Some(\"hello\"));\n  2516:     /// assert_eq!(\"bar:foo\".strip_circumfix(\"foo\", \"foo\"), None);\n  2517:     /// assert_eq!(\"foo:bar;\".strip_circumfix(\"foo:\", ';'), Some(\"bar\"));\n  2518:     /// assert_eq!(\"foo:bar:baz\".strip_circumfix(\"foo:bar:\", \":bar:baz\"), None);\n  2519:     /// ```\n  2520:     #[must_use = \"this returns the remaining substring as a new slice, \\\n  2521:                   without modifying the original\"]\n  2522:     #[stable(feature = \"strip_circumfix\", since = \"CURRENT_RUSTC_VERSION\")]\n  2523:     pub fn strip_circumfix<P: Pattern, S: Pattern>(&self, prefix: P, suffix: S) -> Option<&str>\n  2524:     where\n  2525:         for<'a> S::Searcher<'a>: ReverseSearcher<'a>,\n  2526:     {\n  2527:         self.strip_prefix(prefix)?.strip_suffix(suffix)\n  2528:     }\n  2529: \n  2530:     /// Returns a string slice with the optional prefix removed.\n  2531:     ///\n  2532:     /// If the string starts with the pattern `prefix`, returns the substring after the prefix.\n  2533:     /// Unlike [`strip_prefix`], this method always returns `&str` for easy method chaining,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::trim_end_matches",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
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
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "trim_end_matches",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  2607:     /// ```\n  2608:     /// assert_eq!(\"11foo1bar11\".trim_end_matches('1'), \"11foo1bar\");\n  2609:     /// assert_eq!(\"123foo1bar123\".trim_end_matches(char::is_numeric), \"123foo1bar\");\n  2610:     ///\n  2611:     /// let x: &[_] = &['1', '2'];\n  2612:     /// assert_eq!(\"12foo1bar12\".trim_end_matches(x), \"12foo1bar\");\n  2613:     /// ```\n  2614:     ///\n  2615:     /// A more complex pattern, using a closure:\n  2616:     ///\n  2617:     /// ```\n  2618:     /// assert_eq!(\"1fooX\".trim_end_matches(|c| c == '1' || c == 'X'), \"1foo\");\n  2619:     /// ```\n  2620:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2621:                   without modifying the original\"]\n  2622:     #[stable(feature = \"trim_direction\", since = \"1.30.0\")]\n  2623:     pub fn trim_end_matches<P: Pattern>(&self, pat: P) -> &str\n  2624:     where\n  2625:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2626:     {\n  2627:         let mut j = 0;\n  2628:         let mut matcher = pat.into_searcher(self);\n  2629:         if let Some((_, b)) = matcher.next_reject_back() {\n  2630:             j = b;\n  2631:         }\n  2632:         // SAFETY: `Searcher` is known to return valid indices.\n  2633:         unsafe { self.get_unchecked(0..j) }\n  2634:     }\n  2635: \n  2636:     /// Returns a string slice with all prefixes that match a pattern\n  2637:     /// repeatedly removed.\n  2638:     ///\n  2639:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a",
    "nanvix_source": "  2633:     /// ```\n  2634:     ///\n  2635:     /// A more complex pattern, using a closure:\n  2636:     ///\n  2637:     /// ```\n  2638:     /// assert_eq!(\"1fooX\".trim_end_matches(|c| c == '1' || c == 'X'), \"1foo\");\n  2639:     /// ```\n  2640:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2641:                   without modifying the original\"]\n  2642:     #[stable(feature = \"trim_direction\", since = \"1.30.0\")]\n  2643:     pub fn trim_end_matches<P: Pattern>(&self, pat: P) -> &str\n  2644:     where\n  2645:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  2646:     {\n  2647:         let mut j = 0;\n  2648:         let mut matcher = pat.into_searcher(self);\n  2649:         if let Some((_, b)) = matcher.next_reject_back() {\n  2650:             j = b;\n  2651:         }\n  2652:         // SAFETY: `Searcher` is known to return valid indices.\n  2653:         unsafe { self.get_unchecked(0..j) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::trim_matches",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
                        "args": null,
                        "id": 10099,
                        "path": "Pattern"
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
                      "id": 27119,
                      "path": "DoubleEndedSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
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
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "trim_matches",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  2342:     /// ```\n  2343:     /// assert_eq!(\"11foo1bar11\".trim_matches('1'), \"foo1bar\");\n  2344:     /// assert_eq!(\"123foo1bar123\".trim_matches(char::is_numeric), \"foo1bar\");\n  2345:     ///\n  2346:     /// let x: &[_] = &['1', '2'];\n  2347:     /// assert_eq!(\"12foo1bar12\".trim_matches(x), \"foo1bar\");\n  2348:     /// ```\n  2349:     ///\n  2350:     /// A more complex pattern, using a closure:\n  2351:     ///\n  2352:     /// ```\n  2353:     /// assert_eq!(\"1foo1barXX\".trim_matches(|c| c == '1' || c == 'X'), \"foo1bar\");\n  2354:     /// ```\n  2355:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2356:                   without modifying the original\"]\n  2357:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2358:     pub fn trim_matches<P: Pattern>(&self, pat: P) -> &str\n  2359:     where\n  2360:         for<'a> P::Searcher<'a>: DoubleEndedSearcher<'a>,\n  2361:     {\n  2362:         let mut i = 0;\n  2363:         let mut j = 0;\n  2364:         let mut matcher = pat.into_searcher(self);\n  2365:         if let Some((a, b)) = matcher.next_reject() {\n  2366:             i = a;\n  2367:             j = b; // Remember earliest known match, correct it below if\n  2368:             // last match is different\n  2369:         }\n  2370:         if let Some((_, b)) = matcher.next_reject_back() {\n  2371:             j = b;\n  2372:         }\n  2373:         // SAFETY: `Searcher` is known to return valid indices.\n  2374:         unsafe { self.get_unchecked(i..j) }",
    "nanvix_source": "  2367:     /// ```\n  2368:     ///\n  2369:     /// A more complex pattern, using a closure:\n  2370:     ///\n  2371:     /// ```\n  2372:     /// assert_eq!(\"1foo1barXX\".trim_matches(|c| c == '1' || c == 'X'), \"foo1bar\");\n  2373:     /// ```\n  2374:     #[must_use = \"this returns the trimmed string as a new slice, \\\n  2375:                   without modifying the original\"]\n  2376:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2377:     pub fn trim_matches<P: Pattern>(&self, pat: P) -> &str\n  2378:     where\n  2379:         for<'a> P::Searcher<'a>: DoubleEndedSearcher<'a>,\n  2380:     {\n  2381:         let mut i = 0;\n  2382:         let mut j = 0;\n  2383:         let mut matcher = pat.into_searcher(self);\n  2384:         if let Some((a, b)) = matcher.next_reject() {\n  2385:             i = a;\n  2386:             j = b; // Remember earliest known match, correct it below if\n  2387:             // last match is different",
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
