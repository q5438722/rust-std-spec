For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::PathBuf::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "shrink_to",
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
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1861:     }\n  1862: \n  1863:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1867:     #[inline]\n  1868:     pub fn shrink_to_fit(&mut self) {\n  1869:         self.inner.shrink_to_fit()\n  1870:     }\n  1871: \n  1872:     /// Invokes [`shrink_to`] on the underlying instance of [`OsString`].\n  1873:     ///\n  1874:     /// [`shrink_to`]: OsString::shrink_to\n  1875:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1876:     #[inline]\n  1877:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1878:         self.inner.shrink_to(min_capacity)\n  1879:     }\n  1880: }\n  1881: \n  1882: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1883: impl Clone for PathBuf {\n  1884:     #[inline]\n  1885:     fn clone(&self) -> Self {\n  1886:         PathBuf { inner: self.inner.clone() }\n  1887:     }\n  1888: \n  1889:     /// Clones the contents of `source` into `self`.\n  1890:     ///\n  1891:     /// This method is preferred over simply assigning `source.clone()` to `self`,\n  1892:     /// as it avoids reallocation if possible.\n  1893:     #[inline]",
    "nanvix_source": "  1885:     #[inline]\n  1886:     pub fn shrink_to_fit(&mut self) {\n  1887:         self.inner.shrink_to_fit()\n  1888:     }\n  1889: \n  1890:     /// Invokes [`shrink_to`] on the underlying instance of [`OsString`].\n  1891:     ///\n  1892:     /// [`shrink_to`]: OsString::shrink_to\n  1893:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1894:     #[inline]\n  1895:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1896:         self.inner.shrink_to(min_capacity)\n  1897:     }\n  1898: }\n  1899: \n  1900: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1901: impl Clone for PathBuf {\n  1902:     #[inline]\n  1903:     fn clone(&self) -> Self {\n  1904:         PathBuf { inner: self.inner.clone() }\n  1905:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "shrink_to_fit",
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
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
    "verification_source": "  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1858:     #[inline]\n  1859:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve_exact(additional)\n  1861:     }\n  1862: \n  1863:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1867:     #[inline]\n  1868:     pub fn shrink_to_fit(&mut self) {\n  1869:         self.inner.shrink_to_fit()\n  1870:     }\n  1871: \n  1872:     /// Invokes [`shrink_to`] on the underlying instance of [`OsString`].\n  1873:     ///\n  1874:     /// [`shrink_to`]: OsString::shrink_to\n  1875:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1876:     #[inline]\n  1877:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1878:         self.inner.shrink_to(min_capacity)\n  1879:     }\n  1880: }\n  1881: \n  1882: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1883: impl Clone for PathBuf {\n  1884:     #[inline]",
    "nanvix_source": "  1876:     #[inline]\n  1877:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1878:         self.inner.try_reserve_exact(additional)\n  1879:     }\n  1880: \n  1881:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1882:     ///\n  1883:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1884:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1885:     #[inline]\n  1886:     pub fn shrink_to_fit(&mut self) {\n  1887:         self.inner.shrink_to_fit()\n  1888:     }\n  1889: \n  1890:     /// Invokes [`shrink_to`] on the underlying instance of [`OsString`].\n  1891:     ///\n  1892:     /// [`shrink_to`]: OsString::shrink_to\n  1893:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1894:     #[inline]\n  1895:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1896:         self.inner.shrink_to(min_capacity)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "try_reserve",
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
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
            "additional",
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 874,
                        "path": "TryReserveError"
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
    "verification_source": "  1825:     }\n  1826: \n  1827:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1828:     ///\n  1829:     /// [`reserve`]: OsString::reserve\n  1830:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1831:     #[inline]\n  1832:     pub fn reserve(&mut self, additional: usize) {\n  1833:         self.inner.reserve(additional)\n  1834:     }\n  1835: \n  1836:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`try_reserve`]: OsString::try_reserve\n  1839:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1840:     #[inline]\n  1841:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1842:         self.inner.try_reserve(additional)\n  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve_exact`]: OsString::reserve_exact\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1849:     #[inline]\n  1850:     pub fn reserve_exact(&mut self, additional: usize) {\n  1851:         self.inner.reserve_exact(additional)\n  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]",
    "nanvix_source": "  1849:     #[inline]\n  1850:     pub fn reserve(&mut self, additional: usize) {\n  1851:         self.inner.reserve(additional)\n  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve`]: OsString::try_reserve\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1858:     #[inline]\n  1859:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve(additional)\n  1861:     }\n  1862: \n  1863:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`reserve_exact`]: OsString::reserve_exact\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1867:     #[inline]\n  1868:     pub fn reserve_exact(&mut self, additional: usize) {\n  1869:         self.inner.reserve_exact(additional)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::try_reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "try_reserve_exact",
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
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
            "additional",
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 874,
                        "path": "TryReserveError"
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
    "verification_source": "  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve_exact`]: OsString::reserve_exact\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1849:     #[inline]\n  1850:     pub fn reserve_exact(&mut self, additional: usize) {\n  1851:         self.inner.reserve_exact(additional)\n  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1858:     #[inline]\n  1859:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve_exact(additional)\n  1861:     }\n  1862: \n  1863:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1867:     #[inline]\n  1868:     pub fn shrink_to_fit(&mut self) {\n  1869:         self.inner.shrink_to_fit()\n  1870:     }\n  1871: \n  1872:     /// Invokes [`shrink_to`] on the underlying instance of [`OsString`].\n  1873:     ///\n  1874:     /// [`shrink_to`]: OsString::shrink_to\n  1875:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]",
    "nanvix_source": "  1867:     #[inline]\n  1868:     pub fn reserve_exact(&mut self, additional: usize) {\n  1869:         self.inner.reserve_exact(additional)\n  1870:     }\n  1871: \n  1872:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1873:     ///\n  1874:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1875:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1876:     #[inline]\n  1877:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1878:         self.inner.try_reserve_exact(additional)\n  1879:     }\n  1880: \n  1881:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1882:     ///\n  1883:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1884:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1885:     #[inline]\n  1886:     pub fn shrink_to_fit(&mut self) {\n  1887:         self.inner.shrink_to_fit()",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::with_capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
      "name": "with_capacity",
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
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        }
      }
    },
    "verification_source": "  1241:     /// ```\n  1242:     /// use std::path::PathBuf;\n  1243:     ///\n  1244:     /// let mut path = PathBuf::with_capacity(10);\n  1245:     /// let capacity = path.capacity();\n  1246:     ///\n  1247:     /// // This push is done without reallocating\n  1248:     /// path.push(r\"C:\\\");\n  1249:     ///\n  1250:     /// assert_eq!(capacity, path.capacity());\n  1251:     /// ```\n  1252:     ///\n  1253:     /// [`with_capacity`]: OsString::with_capacity\n  1254:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1255:     #[must_use]\n  1256:     #[inline]\n  1257:     pub fn with_capacity(capacity: usize) -> PathBuf {\n  1258:         PathBuf { inner: OsString::with_capacity(capacity) }\n  1259:     }\n  1260: \n  1261:     /// Coerces to a [`Path`] slice.\n  1262:     ///\n  1263:     /// # Examples\n  1264:     ///\n  1265:     /// ```\n  1266:     /// use std::path::{Path, PathBuf};\n  1267:     ///\n  1268:     /// let p = PathBuf::from(\"/test\");\n  1269:     /// assert_eq!(Path::new(\"/test\"), p.as_path());\n  1270:     /// ```\n  1271:     #[cfg_attr(not(test), rustc_diagnostic_item = \"pathbuf_as_path\")]\n  1272:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1273:     #[must_use]",
    "nanvix_source": "  1247:     /// // This push is done without reallocating\n  1248:     /// path.push(r\"C:\\\");\n  1249:     ///\n  1250:     /// assert_eq!(capacity, path.capacity());\n  1251:     /// ```\n  1252:     ///\n  1253:     /// [`with_capacity`]: OsString::with_capacity\n  1254:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1255:     #[must_use]\n  1256:     #[inline]\n  1257:     pub fn with_capacity(capacity: usize) -> PathBuf {\n  1258:         PathBuf { inner: OsString::with_capacity(capacity) }\n  1259:     }\n  1260: \n  1261:     /// Coerces to a [`Path`] slice.\n  1262:     ///\n  1263:     /// # Examples\n  1264:     ///\n  1265:     /// ```\n  1266:     /// use std::path::{Path, PathBuf};\n  1267:     ///",
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
