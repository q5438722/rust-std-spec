For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::PathBuf::clear",
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
    "verification_source": "  1807: \n  1808:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1809:     ///\n  1810:     /// [`capacity`]: OsString::capacity\n  1811:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1812:     #[must_use]\n  1813:     #[inline]\n  1814:     pub fn capacity(&self) -> usize {\n  1815:         self.inner.capacity()\n  1816:     }\n  1817: \n  1818:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1819:     ///\n  1820:     /// [`clear`]: OsString::clear\n  1821:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1822:     #[inline]\n  1823:     pub fn clear(&mut self) {\n  1824:         self.inner.clear()\n  1825:     }\n  1826: \n  1827:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1828:     ///\n  1829:     /// [`reserve`]: OsString::reserve\n  1830:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1831:     #[inline]\n  1832:     pub fn reserve(&mut self, additional: usize) {\n  1833:         self.inner.reserve(additional)\n  1834:     }\n  1835: \n  1836:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`try_reserve`]: OsString::try_reserve\n  1839:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]",
    "nanvix_source": "  1831:     #[inline]\n  1832:     pub fn capacity(&self) -> usize {\n  1833:         self.inner.capacity()\n  1834:     }\n  1835: \n  1836:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`clear`]: OsString::clear\n  1839:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1840:     #[inline]\n  1841:     pub fn clear(&mut self) {\n  1842:         self.inner.clear()\n  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve`]: OsString::reserve\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1849:     #[inline]\n  1850:     pub fn reserve(&mut self, additional: usize) {\n  1851:         self.inner.reserve(additional)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::into_boxed_path",
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
      "name": "into_boxed_path",
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
                        "id": 1802,
                        "path": "Path"
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
    "verification_source": "  1787:     /// use std::path::PathBuf;\n  1788:     ///\n  1789:     /// let p = PathBuf::from(\"/the/head\");\n  1790:     /// let os_str = p.into_os_string();\n  1791:     /// ```\n  1792:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1793:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1794:     #[inline]\n  1795:     pub fn into_os_string(self) -> OsString {\n  1796:         self.inner\n  1797:     }\n  1798: \n  1799:     /// Converts this `PathBuf` into a [boxed](Box) [`Path`].\n  1800:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  1801:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1802:     #[inline]\n  1803:     pub fn into_boxed_path(self) -> Box<Path> {\n  1804:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1805:         unsafe { Box::from_raw(rw) }\n  1806:     }\n  1807: \n  1808:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1809:     ///\n  1810:     /// [`capacity`]: OsString::capacity\n  1811:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1812:     #[must_use]\n  1813:     #[inline]\n  1814:     pub fn capacity(&self) -> usize {\n  1815:         self.inner.capacity()\n  1816:     }\n  1817: \n  1818:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1819:     ///",
    "nanvix_source": "  1811:     /// ```\n  1812:     #[stable(feature = \"pathbuf_into_string\", since = \"CURRENT_RUSTC_VERSION\")]\n  1813:     pub fn into_string(self) -> Result<String, PathBuf> {\n  1814:         self.into_os_string().into_string().map_err(PathBuf::from)\n  1815:     }\n  1816: \n  1817:     /// Converts this `PathBuf` into a [boxed](Box) [`Path`].\n  1818:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  1819:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1820:     #[inline]\n  1821:     pub fn into_boxed_path(self) -> Box<Path> {\n  1822:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1823:         unsafe { Box::from_raw(rw) }\n  1824:     }\n  1825: \n  1826:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1827:     ///\n  1828:     /// [`capacity`]: OsString::capacity\n  1829:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1830:     #[must_use]\n  1831:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::into_os_string",
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
      "name": "into_os_string",
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
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "  1779:         &mut self.inner\n  1780:     }\n  1781: \n  1782:     /// Consumes the `PathBuf`, yielding its internal [`OsString`] storage.\n  1783:     ///\n  1784:     /// # Examples\n  1785:     ///\n  1786:     /// ```\n  1787:     /// use std::path::PathBuf;\n  1788:     ///\n  1789:     /// let p = PathBuf::from(\"/the/head\");\n  1790:     /// let os_str = p.into_os_string();\n  1791:     /// ```\n  1792:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1793:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1794:     #[inline]\n  1795:     pub fn into_os_string(self) -> OsString {\n  1796:         self.inner\n  1797:     }\n  1798: \n  1799:     /// Converts this `PathBuf` into a [boxed](Box) [`Path`].\n  1800:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  1801:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1802:     #[inline]\n  1803:     pub fn into_boxed_path(self) -> Box<Path> {\n  1804:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1805:         unsafe { Box::from_raw(rw) }\n  1806:     }\n  1807: \n  1808:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1809:     ///\n  1810:     /// [`capacity`]: OsString::capacity\n  1811:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]",
    "nanvix_source": "  1785:     ///\n  1786:     /// ```\n  1787:     /// use std::path::PathBuf;\n  1788:     ///\n  1789:     /// let p = PathBuf::from(\"/the/head\");\n  1790:     /// let os_str = p.into_os_string();\n  1791:     /// ```\n  1792:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1793:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1794:     #[inline]\n  1795:     pub fn into_os_string(self) -> OsString {\n  1796:         self.inner\n  1797:     }\n  1798: \n  1799:     /// Converts the `PathBuf` into a `String` if it contains valid Unicode data.\n  1800:     ///\n  1801:     /// On failure, ownership of the original `PathBuf` is returned.\n  1802:     ///\n  1803:     /// # Examples\n  1804:     ///\n  1805:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::new",
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
        "inputs": [],
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
    "verification_source": "  1216: }\n  1217: \n  1218: impl PathBuf {\n  1219:     /// Allocates an empty `PathBuf`.\n  1220:     ///\n  1221:     /// # Examples\n  1222:     ///\n  1223:     /// ```\n  1224:     /// use std::path::PathBuf;\n  1225:     ///\n  1226:     /// let path = PathBuf::new();\n  1227:     /// ```\n  1228:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1229:     #[must_use]\n  1230:     #[inline]\n  1231:     #[rustc_const_stable(feature = \"const_pathbuf_osstring_new\", since = \"1.91.0\")]\n  1232:     pub const fn new() -> PathBuf {\n  1233:         PathBuf { inner: OsString::new() }\n  1234:     }\n  1235: \n  1236:     /// Creates a new `PathBuf` with a given capacity used to create the\n  1237:     /// internal [`OsString`]. See [`with_capacity`] defined on [`OsString`].\n  1238:     ///\n  1239:     /// # Examples\n  1240:     ///\n  1241:     /// ```\n  1242:     /// use std::path::PathBuf;\n  1243:     ///\n  1244:     /// let mut path = PathBuf::with_capacity(10);\n  1245:     /// let capacity = path.capacity();\n  1246:     ///\n  1247:     /// // This push is done without reallocating\n  1248:     /// path.push(r\"C:\\\");",
    "nanvix_source": "  1222:     ///\n  1223:     /// ```\n  1224:     /// use std::path::PathBuf;\n  1225:     ///\n  1226:     /// let path = PathBuf::new();\n  1227:     /// ```\n  1228:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1229:     #[must_use]\n  1230:     #[inline]\n  1231:     #[rustc_const_stable(feature = \"const_pathbuf_osstring_new\", since = \"1.91.0\")]\n  1232:     pub const fn new() -> PathBuf {\n  1233:         PathBuf { inner: OsString::new() }\n  1234:     }\n  1235: \n  1236:     /// Creates a new `PathBuf` with a given capacity used to create the\n  1237:     /// internal [`OsString`]. See [`with_capacity`] defined on [`OsString`].\n  1238:     ///\n  1239:     /// # Examples\n  1240:     ///\n  1241:     /// ```\n  1242:     /// use std::path::PathBuf;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::pop",
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
      "name": "pop",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1426:     ///\n  1427:     /// [`self.parent`]: Path::parent\n  1428:     ///\n  1429:     /// # Examples\n  1430:     ///\n  1431:     /// ```\n  1432:     /// use std::path::{Path, PathBuf};\n  1433:     ///\n  1434:     /// let mut p = PathBuf::from(\"/spirited/away.rs\");\n  1435:     ///\n  1436:     /// p.pop();\n  1437:     /// assert_eq!(Path::new(\"/spirited\"), p);\n  1438:     /// p.pop();\n  1439:     /// assert_eq!(Path::new(\"/\"), p);\n  1440:     /// ```\n  1441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1442:     pub fn pop(&mut self) -> bool {\n  1443:         match self.parent().map(|p| p.as_u8_slice().len()) {\n  1444:             Some(len) => {\n  1445:                 self.inner.truncate(len);\n  1446:                 true\n  1447:             }\n  1448:             None => false,\n  1449:         }\n  1450:     }\n  1451: \n  1452:     /// Sets whether the path has a trailing [separator](MAIN_SEPARATOR).\n  1453:     ///\n  1454:     /// The value returned by [`has_trailing_sep`](Path::has_trailing_sep) will be equivalent to\n  1455:     /// the provided value if possible.\n  1456:     ///\n  1457:     /// # Examples\n  1458:     ///",
    "nanvix_source": "  1432:     /// use std::path::{Path, PathBuf};\n  1433:     ///\n  1434:     /// let mut p = PathBuf::from(\"/spirited/away.rs\");\n  1435:     ///\n  1436:     /// p.pop();\n  1437:     /// assert_eq!(Path::new(\"/spirited\"), p);\n  1438:     /// p.pop();\n  1439:     /// assert_eq!(Path::new(\"/\"), p);\n  1440:     /// ```\n  1441:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1442:     pub fn pop(&mut self) -> bool {\n  1443:         match self.parent().map(|p| p.as_u8_slice().len()) {\n  1444:             Some(len) => {\n  1445:                 self.inner.truncate(len);\n  1446:                 true\n  1447:             }\n  1448:             None => false,\n  1449:         }\n  1450:     }\n  1451: \n  1452:     /// Sets whether the path has a trailing [separator](MAIN_SEPARATOR).",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::push",
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
                                    "id": 1802,
                                    "path": "Path"
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
            "name": "P"
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
            "path",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1321:     /// let mut path = PathBuf::from(\"/tmp\");\n  1322:     /// path.push(\"file.bk\");\n  1323:     /// assert_eq!(path, PathBuf::from(\"/tmp/file.bk\"));\n  1324:     /// ```\n  1325:     ///\n  1326:     /// Pushing an absolute path replaces the existing path:\n  1327:     ///\n  1328:     /// ```\n  1329:     /// use std::path::PathBuf;\n  1330:     ///\n  1331:     /// let mut path = PathBuf::from(\"/tmp\");\n  1332:     /// path.push(\"/etc\");\n  1333:     /// assert_eq!(path, PathBuf::from(\"/etc\"));\n  1334:     /// ```\n  1335:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1336:     #[rustc_confusables(\"append\", \"put\")]\n  1337:     pub fn push<P: AsRef<Path>>(&mut self, path: P) {\n  1338:         self._push(path.as_ref())\n  1339:     }\n  1340: \n  1341:     fn _push(&mut self, path: &Path) {\n  1342:         // in general, a separator is needed if the rightmost byte is not a separator\n  1343:         let buf = self.inner.as_encoded_bytes();\n  1344:         let mut need_sep = buf.last().map(|c| !is_sep_byte(*c)).unwrap_or(false);\n  1345: \n  1346:         // in the special case of `C:` on Windows, do *not* add a separator\n  1347:         let comps = self.components();\n  1348: \n  1349:         if comps.prefix_len() > 0\n  1350:             && comps.prefix_len() == comps.path.len()\n  1351:             && comps.prefix.unwrap().is_drive()\n  1352:         {\n  1353:             need_sep = false",
    "nanvix_source": "  1327:     ///\n  1328:     /// ```\n  1329:     /// use std::path::PathBuf;\n  1330:     ///\n  1331:     /// let mut path = PathBuf::from(\"/tmp\");\n  1332:     /// path.push(\"/etc\");\n  1333:     /// assert_eq!(path, PathBuf::from(\"/etc\"));\n  1334:     /// ```\n  1335:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1336:     #[rustc_confusables(\"append\", \"put\")]\n  1337:     pub fn push<P: AsRef<Path>>(&mut self, path: P) {\n  1338:         self._push(path.as_ref())\n  1339:     }\n  1340: \n  1341:     fn _push(&mut self, path: &Path) {\n  1342:         // in general, a separator is needed if the rightmost byte is not a separator\n  1343:         let buf = self.inner.as_encoded_bytes();\n  1344:         let mut need_sep = buf.last().map(|c| !is_sep_byte(*c)).unwrap_or(false);\n  1345: \n  1346:         // in the special case of `C:` on Windows, do *not* add a separator\n  1347:         let comps = self.components();",
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
