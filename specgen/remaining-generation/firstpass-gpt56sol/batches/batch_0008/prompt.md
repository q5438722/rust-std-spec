For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::Atomic::as_ptr",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "as_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "primitive": "bool"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29422",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "bool"
            }
          }
        }
      }
    },
    "verification_source": "  1294:     ///     fn my_atomic_op(arg: *mut bool);\n  1295:     /// }\n  1296:     ///\n  1297:     /// let mut atomic = AtomicBool::new(true);\n  1298:     /// unsafe {\n  1299:     ///     my_atomic_op(atomic.as_ptr());\n  1300:     /// }\n  1301:     /// # }\n  1302:     /// ```\n  1303:     ///\n  1304:     /// [memory model]: self#memory-model-for-atomic-accesses\n  1305:     #[inline]\n  1306:     #[stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1307:     #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1308:     #[rustc_never_returns_null_ptr]\n  1309:     #[rustc_should_not_be_called_on_const_items]\n  1310:     pub const fn as_ptr(&self) -> *mut bool {\n  1311:         self.v.get().cast()\n  1312:     }\n  1313: \n  1314:     /// An alias for [`AtomicBool::try_update`].\n  1315:     #[inline]\n  1316:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1317:     #[cfg(target_has_atomic = \"8\")]\n  1318:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1319:     #[rustc_should_not_be_called_on_const_items]\n  1320:     #[deprecated(\n  1321:         since = \"1.99.0\",\n  1322:         note = \"renamed to `try_update` for consistency\",\n  1323:         suggestion = \"try_update\"\n  1324:     )]\n  1325:     pub fn fetch_update<F>(\n  1326:         &self,",
    "nanvix_source": "  1292:     /// }\n  1293:     /// # }\n  1294:     /// ```\n  1295:     ///\n  1296:     /// [memory model]: self#memory-model-for-atomic-accesses\n  1297:     #[inline]\n  1298:     #[stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1299:     #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1300:     #[rustc_never_returns_null_ptr]\n  1301:     #[rustc_should_not_be_called_on_const_items]\n  1302:     pub const fn as_ptr(&self) -> *mut bool {\n  1303:         self.v.get().cast()\n  1304:     }\n  1305: \n  1306:     /// An alias for [`AtomicBool::try_update`].\n  1307:     #[inline]\n  1308:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1309:     #[cfg(target_has_atomic = \"8\")]\n  1310:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1311:     #[rustc_should_not_be_called_on_const_items]\n  1312:     #[deprecated(",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::compare_and_swap",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "compare_and_swap",
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
                      "primitive": "bool"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29422",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "current",
            {
              "primitive": "bool"
            }
          ],
          [
            "new",
            {
              "primitive": "bool"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
    "verification_source": "   852:     ///\n   853:     /// assert_eq!(some_bool.compare_and_swap(true, false, Ordering::Relaxed), true);\n   854:     /// assert_eq!(some_bool.load(Ordering::Relaxed), false);\n   855:     ///\n   856:     /// assert_eq!(some_bool.compare_and_swap(true, true, Ordering::Relaxed), false);\n   857:     /// assert_eq!(some_bool.load(Ordering::Relaxed), false);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   861:     #[deprecated(\n   862:         since = \"1.50.0\",\n   863:         note = \"Use `compare_exchange` or `compare_exchange_weak` instead\"\n   864:     )]\n   865:     #[cfg(target_has_atomic = \"8\")]\n   866:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   867:     #[rustc_should_not_be_called_on_const_items]\n   868:     pub fn compare_and_swap(&self, current: bool, new: bool, order: Ordering) -> bool {\n   869:         match self.compare_exchange(current, new, order, strongest_failure_ordering(order)) {\n   870:             Ok(x) => x,\n   871:             Err(x) => x,\n   872:         }\n   873:     }\n   874: \n   875:     /// Stores a value into the [`bool`] if the current value is the same as the `current` value.\n   876:     ///\n   877:     /// The return value is a result indicating whether the new value was written and containing\n   878:     /// the previous value. On success this value is guaranteed to be equal to `current`.\n   879:     ///\n   880:     /// `compare_exchange` takes two [`Ordering`] arguments to describe the memory\n   881:     /// ordering of this operation. `success` describes the required ordering for the\n   882:     /// read-modify-write operation that takes place if the comparison with `current` succeeds.\n   883:     /// `failure` describes the required ordering for the load operation that takes place when\n   884:     /// the comparison fails. Using [`Acquire`] as success ordering makes the store part",
    "nanvix_source": "   850:     /// ```\n   851:     #[inline]\n   852:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   853:     #[deprecated(\n   854:         since = \"1.50.0\",\n   855:         note = \"Use `compare_exchange` or `compare_exchange_weak` instead\"\n   856:     )]\n   857:     #[cfg(target_has_atomic = \"8\")]\n   858:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   859:     #[rustc_should_not_be_called_on_const_items]\n   860:     pub fn compare_and_swap(&self, current: bool, new: bool, order: Ordering) -> bool {\n   861:         match self.compare_exchange(current, new, order, strongest_failure_ordering(order)) {\n   862:             Ok(x) => x,\n   863:             Err(x) => x,\n   864:         }\n   865:     }\n   866: \n   867:     /// Stores a value into the [`bool`] if the current value is the same as the `current` value.\n   868:     ///\n   869:     /// The return value is a result indicating whether the new value was written and containing\n   870:     /// the previous value. On success this value is guaranteed to be equal to `current`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::compare_exchange",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "compare_exchange",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "current",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "new",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "success",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ],
          [
            "failure",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
                      "raw_pointer": {
                        "is_mutable": true,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1896:     /// `compare_exchange` is a [compare-and-swap operation] and thus exhibits the usual downsides\n  1897:     /// of CAS operations. In particular, a load of the value followed by a successful\n  1898:     /// `compare_exchange` with the previous load *does not ensure* that other threads have not\n  1899:     /// changed the value in the interim. This is usually important when the *equality* check in\n  1900:     /// the `compare_exchange` is being used to check the *identity* of a value, but equality\n  1901:     /// does not necessarily imply identity. This is a particularly common case for pointers, as\n  1902:     /// a pointer holding the same address does not imply that the same object exists at that\n  1903:     /// address! In this case, `compare_exchange` can lead to the [ABA problem].\n  1904:     ///\n  1905:     /// [ABA Problem]: https://en.wikipedia.org/wiki/ABA_problem\n  1906:     /// [compare-and-swap operation]: https://en.wikipedia.org/wiki/Compare-and-swap\n  1907:     #[inline]\n  1908:     #[stable(feature = \"extended_compare_and_swap\", since = \"1.10.0\")]\n  1909:     #[cfg(target_has_atomic = \"ptr\")]\n  1910:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1911:     #[rustc_should_not_be_called_on_const_items]\n  1912:     pub fn compare_exchange(\n  1913:         &self,\n  1914:         current: *mut T,\n  1915:         new: *mut T,\n  1916:         success: Ordering,\n  1917:         failure: Ordering,\n  1918:     ) -> Result<*mut T, *mut T> {\n  1919:         // SAFETY: data races are prevented by atomic intrinsics.\n  1920:         unsafe { atomic_compare_exchange(self.as_ptr(), current, new, success, failure) }\n  1921:     }\n  1922: \n  1923:     /// Stores a value into the pointer if the current value is the same as the `current` value.\n  1924:     ///\n  1925:     /// Unlike [`AtomicPtr::compare_exchange`], this function is allowed to spuriously fail even when the\n  1926:     /// comparison succeeds, which can result in more efficient code on some platforms. The\n  1927:     /// return value is a result indicating whether the new value was written and containing the\n  1928:     /// previous value.",
    "nanvix_source": "  1891:     /// a pointer holding the same address does not imply that the same object exists at that\n  1892:     /// address! In this case, `compare_exchange` can lead to the [ABA problem].\n  1893:     ///\n  1894:     /// [ABA Problem]: https://en.wikipedia.org/wiki/ABA_problem\n  1895:     /// [compare-and-swap operation]: https://en.wikipedia.org/wiki/Compare-and-swap\n  1896:     #[inline]\n  1897:     #[stable(feature = \"extended_compare_and_swap\", since = \"1.10.0\")]\n  1898:     #[cfg(target_has_atomic = \"ptr\")]\n  1899:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1900:     #[rustc_should_not_be_called_on_const_items]\n  1901:     pub fn compare_exchange(\n  1902:         &self,\n  1903:         current: *mut T,\n  1904:         new: *mut T,\n  1905:         success: Ordering,\n  1906:         failure: Ordering,\n  1907:     ) -> Result<*mut T, *mut T> {\n  1908:         // SAFETY: data races are prevented by atomic intrinsics.\n  1909:         unsafe { atomic_compare_exchange(self.as_ptr(), current, new, success, failure) }\n  1910:     }\n  1911: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::compare_exchange_weak",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "compare_exchange_weak",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "current",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "new",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "success",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ],
          [
            "failure",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
                      "raw_pointer": {
                        "is_mutable": true,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1960:     /// `compare_exchange` is a [compare-and-swap operation] and thus exhibits the usual downsides\n  1961:     /// of CAS operations. In particular, a load of the value followed by a successful\n  1962:     /// `compare_exchange` with the previous load *does not ensure* that other threads have not\n  1963:     /// changed the value in the interim. This is usually important when the *equality* check in\n  1964:     /// the `compare_exchange` is being used to check the *identity* of a value, but equality\n  1965:     /// does not necessarily imply identity. This is a particularly common case for pointers, as\n  1966:     /// a pointer holding the same address does not imply that the same object exists at that\n  1967:     /// address! In this case, `compare_exchange` can lead to the [ABA problem].\n  1968:     ///\n  1969:     /// [ABA Problem]: https://en.wikipedia.org/wiki/ABA_problem\n  1970:     /// [compare-and-swap operation]: https://en.wikipedia.org/wiki/Compare-and-swap\n  1971:     #[inline]\n  1972:     #[stable(feature = \"extended_compare_and_swap\", since = \"1.10.0\")]\n  1973:     #[cfg(target_has_atomic = \"ptr\")]\n  1974:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1975:     #[rustc_should_not_be_called_on_const_items]\n  1976:     pub fn compare_exchange_weak(\n  1977:         &self,\n  1978:         current: *mut T,\n  1979:         new: *mut T,\n  1980:         success: Ordering,\n  1981:         failure: Ordering,\n  1982:     ) -> Result<*mut T, *mut T> {\n  1983:         // SAFETY: This intrinsic is unsafe because it operates on a raw pointer\n  1984:         // but we know for sure that the pointer is valid (we just got it from\n  1985:         // an `UnsafeCell` that we have by reference) and the atomic operation\n  1986:         // itself allows us to safely mutate the `UnsafeCell` contents.\n  1987:         unsafe { atomic_compare_exchange_weak(self.as_ptr(), current, new, success, failure) }\n  1988:     }\n  1989: \n  1990:     /// An alias for [`AtomicPtr::try_update`].\n  1991:     #[inline]\n  1992:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]",
    "nanvix_source": "  1955:     /// a pointer holding the same address does not imply that the same object exists at that\n  1956:     /// address! In this case, `compare_exchange` can lead to the [ABA problem].\n  1957:     ///\n  1958:     /// [ABA Problem]: https://en.wikipedia.org/wiki/ABA_problem\n  1959:     /// [compare-and-swap operation]: https://en.wikipedia.org/wiki/Compare-and-swap\n  1960:     #[inline]\n  1961:     #[stable(feature = \"extended_compare_and_swap\", since = \"1.10.0\")]\n  1962:     #[cfg(target_has_atomic = \"ptr\")]\n  1963:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1964:     #[rustc_should_not_be_called_on_const_items]\n  1965:     pub fn compare_exchange_weak(\n  1966:         &self,\n  1967:         current: *mut T,\n  1968:         new: *mut T,\n  1969:         success: Ordering,\n  1970:         failure: Ordering,\n  1971:     ) -> Result<*mut T, *mut T> {\n  1972:         // SAFETY: This intrinsic is unsafe because it operates on a raw pointer\n  1973:         // but we know for sure that the pointer is valid (we just got it from\n  1974:         // an `UnsafeCell` that we have by reference) and the atomic operation\n  1975:         // itself allows us to safely mutate the `UnsafeCell` contents.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_add",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "multiple_rust_declarations_share_path"
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
      "name": "fetch_add",
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
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29500",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "u8"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "u8"
        }
      }
    },
    "verification_source": "  3624:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3625:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3626:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3627:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3628:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3632:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3633:     \"i8\",\n  3634:     \"\",\n  3635:     atomic_min, atomic_max,\n  3636:     1,\n  3637:     i8 AtomicI8\n  3638: }\n  3639: #[cfg(target_has_atomic_load_store = \"8\")]\n  3640: atomic_int! {\n  3641:     cfg(target_has_atomic = \"8\"),\n  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }",
    "nanvix_source": "  3616:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3617:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3618:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3619:     \"i8\",\n  3620:     \"\",\n  3621:     atomic_min, atomic_max,\n  3622:     1,\n  3623:     i8 AtomicI8\n  3624: }\n  3625: #[cfg(target_has_atomic_load_store = \"8\")]\n  3626: atomic_int! {\n  3627:     cfg(target_has_atomic = \"8\"),\n  3628:     cfg(target_has_atomic_primitive_alignment = \"8\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3632:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3633:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_and",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "fetch_and",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2395:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2396:     ///\n  2397:     /// let pointer = &mut 3i64 as *mut i64;\n  2398:     /// // A tagged pointer\n  2399:     /// let atom = AtomicPtr::<i64>::new(pointer.map_addr(|a| a | 1));\n  2400:     /// assert_eq!(atom.fetch_or(1, Ordering::Relaxed).addr() & 1, 1);\n  2401:     /// // Untag, and extract the previously tagged pointer.\n  2402:     /// let untagged = atom.fetch_and(!1, Ordering::Relaxed)\n  2403:     ///     .map_addr(|a| a & !1);\n  2404:     /// assert_eq!(untagged, pointer);\n  2405:     /// ```\n  2406:     #[inline]\n  2407:     #[cfg(target_has_atomic = \"ptr\")]\n  2408:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2409:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2410:     #[rustc_should_not_be_called_on_const_items]\n  2411:     pub fn fetch_and(&self, val: usize, order: Ordering) -> *mut T {\n  2412:         // SAFETY: data races are prevented by atomic intrinsics.\n  2413:         unsafe { atomic_and(self.as_ptr(), val, order).cast() }\n  2414:     }\n  2415: \n  2416:     /// Performs a bitwise \"xor\" operation on the address of the current\n  2417:     /// pointer, and the argument `val`, and stores a pointer with provenance of\n  2418:     /// the current pointer and the resulting address.\n  2419:     ///\n  2420:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2421:     /// `ptr = ptr.map_addr(|a| a ^ val)`. This can be used in tagged\n  2422:     /// pointer schemes to atomically toggle tag bits.\n  2423:     ///\n  2424:     /// **Caveat**: This operation returns the previous value. To compute the\n  2425:     /// stored value without losing provenance, you may use [`map_addr`]. For\n  2426:     /// example: `a.fetch_xor(val).map_addr(|a| a ^ val)`.\n  2427:     ///",
    "nanvix_source": "  2390:     /// // Untag, and extract the previously tagged pointer.\n  2391:     /// let untagged = atom.fetch_and(!1, Ordering::Relaxed)\n  2392:     ///     .map_addr(|a| a & !1);\n  2393:     /// assert_eq!(untagged, pointer);\n  2394:     /// ```\n  2395:     #[inline]\n  2396:     #[cfg(target_has_atomic = \"ptr\")]\n  2397:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2398:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2399:     #[rustc_should_not_be_called_on_const_items]\n  2400:     pub fn fetch_and(&self, val: usize, order: Ordering) -> *mut T {\n  2401:         // SAFETY: data races are prevented by atomic intrinsics.\n  2402:         unsafe { atomic_and(self.as_ptr(), val, order).cast() }\n  2403:     }\n  2404: \n  2405:     /// Performs a bitwise \"xor\" operation on the address of the current\n  2406:     /// pointer, and the argument `val`, and stores a pointer with provenance of\n  2407:     /// the current pointer and the resulting address.\n  2408:     ///\n  2409:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2410:     /// `ptr = ptr.map_addr(|a| a ^ val)`. This can be used in tagged",
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
