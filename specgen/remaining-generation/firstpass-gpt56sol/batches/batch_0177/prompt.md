For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::ffi::OsString::try_reserve",
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
    "verification_source": "   396:     ///\n   397:     /// fn process_data(data: &str) -> Result<OsString, TryReserveError> {\n   398:     ///     let mut s = OsString::new();\n   399:     ///\n   400:     ///     // Pre-reserve the memory, exiting if we can't\n   401:     ///     s.try_reserve(OsStr::new(data).len())?;\n   402:     ///\n   403:     ///     // Now we know this can't OOM in the middle of our complex work\n   404:     ///     s.push(data);\n   405:     ///\n   406:     ///     Ok(s)\n   407:     /// }\n   408:     /// # process_data(\"123\").expect(\"why is the test harness OOMing on 3 bytes?\");\n   409:     /// ```\n   410:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n   411:     #[inline]\n   412:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   413:         self.inner.try_reserve(additional)\n   414:     }\n   415: \n   416:     /// Reserves the minimum capacity for at least `additional` more capacity to\n   417:     /// be inserted in the given `OsString`. Does nothing if the capacity is\n   418:     /// already sufficient.\n   419:     ///\n   420:     /// Note that the allocator may give the collection more space than it\n   421:     /// requests. Therefore, capacity can not be relied upon to be precisely\n   422:     /// minimal. Prefer [`reserve`] if future insertions are expected.\n   423:     ///\n   424:     /// [`reserve`]: OsString::reserve\n   425:     ///\n   426:     /// See the main `OsString` documentation information about encoding and capacity units.\n   427:     ///\n   428:     /// # Examples",
    "nanvix_source": "   394:     ///\n   395:     ///     // Now we know this can't OOM in the middle of our complex work\n   396:     ///     s.push(data);\n   397:     ///\n   398:     ///     Ok(s)\n   399:     /// }\n   400:     /// # process_data(\"123\").expect(\"why is the test harness OOMing on 3 bytes?\");\n   401:     /// ```\n   402:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n   403:     #[inline]\n   404:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   405:         self.inner.try_reserve(additional)\n   406:     }\n   407: \n   408:     /// Reserves the minimum capacity for at least `additional` more capacity to\n   409:     /// be inserted in the given `OsString`. Does nothing if the capacity is\n   410:     /// already sufficient.\n   411:     ///\n   412:     /// Note that the allocator may give the collection more space than it\n   413:     /// requests. Therefore, capacity can not be relied upon to be precisely\n   414:     /// minimal. Prefer [`reserve`] if future insertions are expected.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::try_reserve_exact",
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
    "verification_source": "   467:     ///\n   468:     /// fn process_data(data: &str) -> Result<OsString, TryReserveError> {\n   469:     ///     let mut s = OsString::new();\n   470:     ///\n   471:     ///     // Pre-reserve the memory, exiting if we can't\n   472:     ///     s.try_reserve_exact(OsStr::new(data).len())?;\n   473:     ///\n   474:     ///     // Now we know this can't OOM in the middle of our complex work\n   475:     ///     s.push(data);\n   476:     ///\n   477:     ///     Ok(s)\n   478:     /// }\n   479:     /// # process_data(\"123\").expect(\"why is the test harness OOMing on 3 bytes?\");\n   480:     /// ```\n   481:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n   482:     #[inline]\n   483:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   484:         self.inner.try_reserve_exact(additional)\n   485:     }\n   486: \n   487:     /// Shrinks the capacity of the `OsString` to match its length.\n   488:     ///\n   489:     /// See the main `OsString` documentation information about encoding and capacity units.\n   490:     ///\n   491:     /// # Examples\n   492:     ///\n   493:     /// ```\n   494:     /// use std::ffi::OsString;\n   495:     ///\n   496:     /// let mut s = OsString::from(\"foo\");\n   497:     ///\n   498:     /// s.reserve(100);\n   499:     /// assert!(s.capacity() >= 100);",
    "nanvix_source": "   465:     ///\n   466:     ///     // Now we know this can't OOM in the middle of our complex work\n   467:     ///     s.push(data);\n   468:     ///\n   469:     ///     Ok(s)\n   470:     /// }\n   471:     /// # process_data(\"123\").expect(\"why is the test harness OOMing on 3 bytes?\");\n   472:     /// ```\n   473:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n   474:     #[inline]\n   475:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n   476:         self.inner.try_reserve_exact(additional)\n   477:     }\n   478: \n   479:     /// Shrinks the capacity of the `OsString` to match its length.\n   480:     ///\n   481:     /// See the main `OsString` documentation information about encoding and capacity units.\n   482:     ///\n   483:     /// # Examples\n   484:     ///\n   485:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::with_capacity",
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
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "   296:     /// # Examples\n   297:     ///\n   298:     /// ```\n   299:     /// use std::ffi::OsString;\n   300:     ///\n   301:     /// let mut os_string = OsString::with_capacity(10);\n   302:     /// let capacity = os_string.capacity();\n   303:     ///\n   304:     /// // This push is done without reallocating\n   305:     /// os_string.push(\"foo\");\n   306:     ///\n   307:     /// assert_eq!(capacity, os_string.capacity());\n   308:     /// ```\n   309:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   310:     #[must_use]\n   311:     #[inline]\n   312:     pub fn with_capacity(capacity: usize) -> OsString {\n   313:         OsString { inner: Buf::with_capacity(capacity) }\n   314:     }\n   315: \n   316:     /// Truncates the `OsString` to zero length.\n   317:     ///\n   318:     /// # Examples\n   319:     ///\n   320:     /// ```\n   321:     /// use std::ffi::OsString;\n   322:     ///\n   323:     /// let mut os_string = OsString::from(\"foo\");\n   324:     /// assert_eq!(&os_string, \"foo\");\n   325:     ///\n   326:     /// os_string.clear();\n   327:     /// assert_eq!(&os_string, \"\");\n   328:     /// ```",
    "nanvix_source": "   294:     /// let capacity = os_string.capacity();\n   295:     ///\n   296:     /// // This push is done without reallocating\n   297:     /// os_string.push(\"foo\");\n   298:     ///\n   299:     /// assert_eq!(capacity, os_string.capacity());\n   300:     /// ```\n   301:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   302:     #[must_use]\n   303:     #[inline]\n   304:     pub fn with_capacity(capacity: usize) -> OsString {\n   305:         OsString { inner: Buf::with_capacity(capacity) }\n   306:     }\n   307: \n   308:     /// Truncates the `OsString` to zero length.\n   309:     ///\n   310:     /// # Examples\n   311:     ///\n   312:     /// ```\n   313:     /// use std::ffi::OsString;\n   314:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::capacity",
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
      "name": "capacity",
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
    "verification_source": "  1798: \n  1799:     /// Converts this `PathBuf` into a [boxed](Box) [`Path`].\n  1800:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  1801:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1802:     #[inline]\n  1803:     pub fn into_boxed_path(self) -> Box<Path> {\n  1804:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1805:         unsafe { Box::from_raw(rw) }\n  1806:     }\n  1807: \n  1808:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1809:     ///\n  1810:     /// [`capacity`]: OsString::capacity\n  1811:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1812:     #[must_use]\n  1813:     #[inline]\n  1814:     pub fn capacity(&self) -> usize {\n  1815:         self.inner.capacity()\n  1816:     }\n  1817: \n  1818:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1819:     ///\n  1820:     /// [`clear`]: OsString::clear\n  1821:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1822:     #[inline]\n  1823:     pub fn clear(&mut self) {\n  1824:         self.inner.clear()\n  1825:     }\n  1826: \n  1827:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1828:     ///\n  1829:     /// [`reserve`]: OsString::reserve\n  1830:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]",
    "nanvix_source": "  1822:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1823:         unsafe { Box::from_raw(rw) }\n  1824:     }\n  1825: \n  1826:     /// Invokes [`capacity`] on the underlying instance of [`OsString`].\n  1827:     ///\n  1828:     /// [`capacity`]: OsString::capacity\n  1829:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1830:     #[must_use]\n  1831:     #[inline]\n  1832:     pub fn capacity(&self) -> usize {\n  1833:         self.inner.capacity()\n  1834:     }\n  1835: \n  1836:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`clear`]: OsString::clear\n  1839:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1840:     #[inline]\n  1841:     pub fn clear(&mut self) {\n  1842:         self.inner.clear()",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::reserve",
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
      "name": "reserve",
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1816:     }\n  1817: \n  1818:     /// Invokes [`clear`] on the underlying instance of [`OsString`].\n  1819:     ///\n  1820:     /// [`clear`]: OsString::clear\n  1821:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1822:     #[inline]\n  1823:     pub fn clear(&mut self) {\n  1824:         self.inner.clear()\n  1825:     }\n  1826: \n  1827:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1828:     ///\n  1829:     /// [`reserve`]: OsString::reserve\n  1830:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1831:     #[inline]\n  1832:     pub fn reserve(&mut self, additional: usize) {\n  1833:         self.inner.reserve(additional)\n  1834:     }\n  1835: \n  1836:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`try_reserve`]: OsString::try_reserve\n  1839:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1840:     #[inline]\n  1841:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1842:         self.inner.try_reserve(additional)\n  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve_exact`]: OsString::reserve_exact\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]",
    "nanvix_source": "  1840:     #[inline]\n  1841:     pub fn clear(&mut self) {\n  1842:         self.inner.clear()\n  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve`]: OsString::reserve\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1849:     #[inline]\n  1850:     pub fn reserve(&mut self, additional: usize) {\n  1851:         self.inner.reserve(additional)\n  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve`]: OsString::try_reserve\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1858:     #[inline]\n  1859:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve(additional)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::reserve_exact",
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
      "name": "reserve_exact",
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1834:     }\n  1835: \n  1836:     /// Invokes [`try_reserve`] on the underlying instance of [`OsString`].\n  1837:     ///\n  1838:     /// [`try_reserve`]: OsString::try_reserve\n  1839:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1840:     #[inline]\n  1841:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1842:         self.inner.try_reserve(additional)\n  1843:     }\n  1844: \n  1845:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1846:     ///\n  1847:     /// [`reserve_exact`]: OsString::reserve_exact\n  1848:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1849:     #[inline]\n  1850:     pub fn reserve_exact(&mut self, additional: usize) {\n  1851:         self.inner.reserve_exact(additional)\n  1852:     }\n  1853: \n  1854:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1855:     ///\n  1856:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1857:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1858:     #[inline]\n  1859:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve_exact(additional)\n  1861:     }\n  1862: \n  1863:     /// Invokes [`shrink_to_fit`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`shrink_to_fit`]: OsString::shrink_to_fit\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]",
    "nanvix_source": "  1858:     #[inline]\n  1859:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1860:         self.inner.try_reserve(additional)\n  1861:     }\n  1862: \n  1863:     /// Invokes [`reserve_exact`] on the underlying instance of [`OsString`].\n  1864:     ///\n  1865:     /// [`reserve_exact`]: OsString::reserve_exact\n  1866:     #[stable(feature = \"path_buf_capacity\", since = \"1.44.0\")]\n  1867:     #[inline]\n  1868:     pub fn reserve_exact(&mut self, additional: usize) {\n  1869:         self.inner.reserve_exact(additional)\n  1870:     }\n  1871: \n  1872:     /// Invokes [`try_reserve_exact`] on the underlying instance of [`OsString`].\n  1873:     ///\n  1874:     /// [`try_reserve_exact`]: OsString::try_reserve_exact\n  1875:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1876:     #[inline]\n  1877:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1878:         self.inner.try_reserve_exact(additional)",
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
