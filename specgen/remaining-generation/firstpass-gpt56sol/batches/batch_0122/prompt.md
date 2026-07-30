For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ffi::CStr::to_str",
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
      "name": "to_str",
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
          "resolved_path": {
            "args": null,
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
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
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10083,
                        "path": "str::Utf8Error"
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
    "verification_source": "   604: \n   605:     /// Yields a <code>&[str]</code> slice if the `CStr` contains valid UTF-8.\n   606:     ///\n   607:     /// If the contents of the `CStr` are valid UTF-8 data, this\n   608:     /// function will return the corresponding <code>&[str]</code> slice. Otherwise,\n   609:     /// it will return an error with details of where UTF-8 validation failed.\n   610:     ///\n   611:     /// [str]: prim@str \"str\"\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```\n   616:     /// assert_eq!(c\"foo\".to_str(), Ok(\"foo\"));\n   617:     /// ```\n   618:     #[stable(feature = \"cstr_to_str\", since = \"1.4.0\")]\n   619:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   620:     pub const fn to_str(&self) -> Result<&str, str::Utf8Error> {\n   621:         // N.B., when `CStr` is changed to perform the length check in `.to_bytes()`\n   622:         // instead of in `from_ptr()`, it may be worth considering if this should\n   623:         // be rewritten to do the UTF-8 check inline with the length calculation\n   624:         // instead of doing it afterwards.\n   625:         str::from_utf8(self.to_bytes())\n   626:     }\n   627: \n   628:     /// Returns an object that implements [`Display`] for safely printing a [`CStr`] that may\n   629:     /// contain non-Unicode data.\n   630:     ///\n   631:     /// Behaves as if `self` were first lossily converted to a `str`, with invalid UTF-8 presented\n   632:     /// as the Unicode replacement character: \ufffd.\n   633:     ///\n   634:     /// [`Display`]: fmt::Display\n   635:     ///\n   636:     /// # Examples",
    "nanvix_source": "   611:     ///\n   612:     /// [str]: prim@str \"str\"\n   613:     ///\n   614:     /// # Examples\n   615:     ///\n   616:     /// ```\n   617:     /// assert_eq!(c\"foo\".to_str(), Ok(\"foo\"));\n   618:     /// ```\n   619:     #[stable(feature = \"cstr_to_str\", since = \"1.4.0\")]\n   620:     #[rustc_const_stable(feature = \"const_cstr_methods\", since = \"1.72.0\")]\n   621:     pub const fn to_str(&self) -> Result<&str, str::Utf8Error> {\n   622:         // N.B., when `CStr` is changed to perform the length check in `.to_bytes()`\n   623:         // instead of in `from_ptr()`, it may be worth considering if this should\n   624:         // be rewritten to do the UTF-8 check inline with the length calculation\n   625:         // instead of doing it afterwards.\n   626:         str::from_utf8(self.to_bytes())\n   627:     }\n   628: \n   629:     /// Returns an object that implements [`Display`] for safely printing a [`CStr`] that may\n   630:     /// contain non-Unicode data.\n   631:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::Ready::into_inner",
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
      "name": "into_inner",
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
            "id": 10195,
            "path": "Ready"
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
        "impl_id": "core:32599",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10195",
        "resolved_owner_path": [
          "core",
          "future",
          "ready",
          "Ready"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "    19:     type Output = T;\n    20: \n    21:     #[inline]\n    22:     fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<T> {\n    23:         Poll::Ready(self.0.take().expect(\"`Ready` polled after completion\"))\n    24:     }\n    25: }\n    26: \n    27: impl<T> Ready<T> {\n    28:     /// Consumes the `Ready`, returning the wrapped value.\n    29:     ///\n    30:     /// # Panics\n    31:     ///\n    32:     /// Will panic if this [`Ready`] was already polled to completion.\n    33:     ///\n    34:     /// # Examples\n    35:     ///\n    36:     /// ```\n    37:     /// use std::future;\n    38:     ///\n    39:     /// let a = future::ready(1);\n    40:     /// assert_eq!(a.into_inner(), 1);\n    41:     /// ```\n    42:     #[stable(feature = \"ready_into_inner\", since = \"1.82.0\")]\n    43:     #[must_use]\n    44:     #[inline]\n    45:     pub fn into_inner(self) -> T {\n    46:         self.0.expect(\"Called `into_inner()` on `Ready` after completion\")\n    47:     }\n    48: }\n    49: \n    50: /// Creates a future that is immediately ready with a value.\n    51: ///",
    "nanvix_source": "    25: }\n    26: \n    27: impl<T> Ready<T> {\n    28:     /// Consumes the `Ready`, returning the wrapped value.\n    29:     ///\n    30:     /// # Panics\n    31:     ///\n    32:     /// Will panic if this [`Ready`] was already polled to completion.\n    33:     ///\n    34:     /// # Examples\n    35:     ///\n    36:     /// ```\n    37:     /// use std::future;\n    38:     ///\n    39:     /// let a = future::ready(1);\n    40:     /// assert_eq!(a.into_inner(), 1);\n    41:     /// ```\n    42:     #[stable(feature = \"ready_into_inner\", since = \"1.82.0\")]\n    43:     #[must_use]\n    44:     #[inline]\n    45:     pub fn into_inner(self) -> T {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::pending",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
      "name": "pending",
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
            "id": 10193,
            "path": "Pending"
          }
        }
      }
    },
    "verification_source": "    14: pub struct Pending<T> {\n    15:     _data: marker::PhantomData<fn() -> T>,\n    16: }\n    17: \n    18: /// Creates a future which never resolves, representing a computation that never\n    19: /// finishes.\n    20: ///\n    21: /// # Examples\n    22: ///\n    23: /// ```no_run\n    24: /// use std::future;\n    25: ///\n    26: /// # async fn run() {\n    27: /// let future = future::pending();\n    28: /// let () = future.await;\n    29: /// unreachable!();\n    30: /// # }\n    31: /// ```\n    32: #[stable(feature = \"future_readiness_fns\", since = \"1.48.0\")]\n    33: pub fn pending<T>() -> Pending<T> {\n    34:     Pending { _data: marker::PhantomData }\n    35: }\n    36: \n    37: #[stable(feature = \"future_readiness_fns\", since = \"1.48.0\")]\n    38: impl<T> Future for Pending<T> {\n    39:     type Output = T;\n    40: \n    41:     fn poll(self: Pin<&mut Self>, _: &mut Context<'_>) -> Poll<T> {\n    42:         Poll::Pending\n    43:     }\n    44: }\n    45: \n    46: #[stable(feature = \"future_readiness_fns\", since = \"1.48.0\")]",
    "nanvix_source": "    20: ///\n    21: /// # Examples\n    22: ///\n    23: /// ```no_run\n    24: /// use std::future;\n    25: ///\n    26: /// # async fn run() {\n    27: /// let future = future::pending();\n    28: /// let () = future.await;\n    29: /// unreachable!();\n    30: /// # }\n    31: /// ```\n    32: #[stable(feature = \"future_readiness_fns\", since = \"1.48.0\")]\n    33: pub fn pending<T>() -> Pending<T> {\n    34:     Pending { _data: marker::PhantomData }\n    35: }\n    36: \n    37: #[stable(feature = \"future_readiness_fns\", since = \"1.48.0\")]\n    38: impl<T> Future for Pending<T> {\n    39:     type Output = T;\n    40: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::ready",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
      "name": "ready",
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
            "t",
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
            "id": 10195,
            "path": "Ready"
          }
        }
      }
    },
    "verification_source": "    30:     /// # Panics\n    31:     ///\n    32:     /// Will panic if this [`Ready`] was already polled to completion.\n    33:     ///\n    34:     /// # Examples\n    35:     ///\n    36:     /// ```\n    37:     /// use std::future;\n    38:     ///\n    39:     /// let a = future::ready(1);\n    40:     /// assert_eq!(a.into_inner(), 1);\n    41:     /// ```\n    42:     #[stable(feature = \"ready_into_inner\", since = \"1.82.0\")]\n    43:     #[must_use]\n    44:     #[inline]\n    45:     pub fn into_inner(self) -> T {\n    46:         self.0.expect(\"Called `into_inner()` on `Ready` after completion\")\n    47:     }\n    48: }\n    49: \n    50: /// Creates a future that is immediately ready with a value.\n    51: ///\n    52: /// Futures created through this function are functionally similar to those\n    53: /// created through `async {}`. The main difference is that futures created\n    54: /// through this function are named and implement `Unpin`.\n    55: ///\n    56: /// # Examples\n    57: ///\n    58: /// ```\n    59: /// use std::future;\n    60: ///\n    61: /// # async fn run() {\n    62: /// let a = future::ready(1);",
    "nanvix_source": "    36:     /// ```\n    37:     /// use std::future;\n    38:     ///\n    39:     /// let a = future::ready(1);\n    40:     /// assert_eq!(a.into_inner(), 1);\n    41:     /// ```\n    42:     #[stable(feature = \"ready_into_inner\", since = \"1.82.0\")]\n    43:     #[must_use]\n    44:     #[inline]\n    45:     pub fn into_inner(self) -> T {\n    46:         self.0.expect(\"Called `into_inner()` on `Ready` after completion\")\n    47:     }\n    48: }\n    49: \n    50: /// Creates a future that is immediately ready with a value.\n    51: ///\n    52: /// Futures created through this function are functionally similar to those\n    53: /// created through `async {}`. The main difference is that futures created\n    54: /// through this function are named and implement `Unpin`.\n    55: ///\n    56: /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::IpAddr::is_ipv4",
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
      "name": "is_ipv4",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   435:     /// otherwise.\n   436:     ///\n   437:     /// [`IPv4` address]: IpAddr::V4\n   438:     ///\n   439:     /// # Examples\n   440:     ///\n   441:     /// ```\n   442:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   443:     ///\n   444:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(203, 0, 113, 6)).is_ipv4(), true);\n   445:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0)).is_ipv4(), false);\n   446:     /// ```\n   447:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   448:     #[stable(feature = \"ipaddr_checker\", since = \"1.16.0\")]\n   449:     #[must_use]\n   450:     #[inline]\n   451:     pub const fn is_ipv4(&self) -> bool {\n   452:         matches!(self, IpAddr::V4(_))\n   453:     }\n   454: \n   455:     /// Returns [`true`] if this address is an [`IPv6` address], and [`false`]\n   456:     /// otherwise.\n   457:     ///\n   458:     /// [`IPv6` address]: IpAddr::V6\n   459:     ///\n   460:     /// # Examples\n   461:     ///\n   462:     /// ```\n   463:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   464:     ///\n   465:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(203, 0, 113, 6)).is_ipv6(), false);\n   466:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0)).is_ipv6(), true);\n   467:     /// ```",
    "nanvix_source": "   441:     /// ```\n   442:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   443:     ///\n   444:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(203, 0, 113, 6)).is_ipv4(), true);\n   445:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0)).is_ipv4(), false);\n   446:     /// ```\n   447:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   448:     #[stable(feature = \"ipaddr_checker\", since = \"1.16.0\")]\n   449:     #[must_use]\n   450:     #[inline]\n   451:     pub const fn is_ipv4(&self) -> bool {\n   452:         matches!(self, IpAddr::V4(_))\n   453:     }\n   454: \n   455:     /// Returns [`true`] if this address is an [`IPv6` address], and [`false`]\n   456:     /// otherwise.\n   457:     ///\n   458:     /// [`IPv6` address]: IpAddr::V6\n   459:     ///\n   460:     /// # Examples\n   461:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::IpAddr::is_ipv6",
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
      "name": "is_ipv6",
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
            "id": 9943,
            "path": "IpAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27758",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9943",
        "resolved_owner_path": [
          "core",
          "net",
          "ip_addr",
          "IpAddr"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   456:     /// otherwise.\n   457:     ///\n   458:     /// [`IPv6` address]: IpAddr::V6\n   459:     ///\n   460:     /// # Examples\n   461:     ///\n   462:     /// ```\n   463:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   464:     ///\n   465:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(203, 0, 113, 6)).is_ipv6(), false);\n   466:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0)).is_ipv6(), true);\n   467:     /// ```\n   468:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   469:     #[stable(feature = \"ipaddr_checker\", since = \"1.16.0\")]\n   470:     #[must_use]\n   471:     #[inline]\n   472:     pub const fn is_ipv6(&self) -> bool {\n   473:         matches!(self, IpAddr::V6(_))\n   474:     }\n   475: \n   476:     /// Converts this address to an `IpAddr::V4` if it is an IPv4-mapped IPv6\n   477:     /// address, otherwise returns `self` as-is.\n   478:     ///\n   479:     /// # Examples\n   480:     ///\n   481:     /// ```\n   482:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   483:     ///\n   484:     /// let localhost_v4 = Ipv4Addr::new(127, 0, 0, 1);\n   485:     ///\n   486:     /// assert_eq!(IpAddr::V4(localhost_v4).to_canonical(), localhost_v4);\n   487:     /// assert_eq!(IpAddr::V6(localhost_v4.to_ipv6_mapped()).to_canonical(), localhost_v4);\n   488:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)).to_canonical().is_loopback(), true);",
    "nanvix_source": "   462:     /// ```\n   463:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};\n   464:     ///\n   465:     /// assert_eq!(IpAddr::V4(Ipv4Addr::new(203, 0, 113, 6)).is_ipv6(), false);\n   466:     /// assert_eq!(IpAddr::V6(Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, 0)).is_ipv6(), true);\n   467:     /// ```\n   468:     #[rustc_const_stable(feature = \"const_ip_50\", since = \"1.50.0\")]\n   469:     #[stable(feature = \"ipaddr_checker\", since = \"1.16.0\")]\n   470:     #[must_use]\n   471:     #[inline]\n   472:     pub const fn is_ipv6(&self) -> bool {\n   473:         matches!(self, IpAddr::V6(_))\n   474:     }\n   475: \n   476:     /// Converts this address to an `IpAddr::V4` if it is an IPv4-mapped IPv6\n   477:     /// address, otherwise returns `self` as-is.\n   478:     ///\n   479:     /// # Examples\n   480:     ///\n   481:     /// ```\n   482:     /// use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};",
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
