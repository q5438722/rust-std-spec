For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::TryLockResult::unwrap_or_default",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
                      "id": 70,
                      "path": "Default"
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
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
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
      "name": "unwrap_or_default",
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
    "verification_source": "  1249:     ///\n  1250:     /// ```\n  1251:     /// let good_year_from_input = \"1909\";\n  1252:     /// let bad_year_from_input = \"190blarg\";\n  1253:     /// let good_year = good_year_from_input.parse().unwrap_or_default();\n  1254:     /// let bad_year = bad_year_from_input.parse().unwrap_or_default();\n  1255:     ///\n  1256:     /// assert_eq!(1909, good_year);\n  1257:     /// assert_eq!(0, bad_year);\n  1258:     /// ```\n  1259:     ///\n  1260:     /// [`parse`]: str::parse\n  1261:     /// [`FromStr`]: crate::str::FromStr\n  1262:     #[inline]\n  1263:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1264:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1265:     pub const fn unwrap_or_default(self) -> T\n  1266:     where\n  1267:         T: [const] Default + [const] Destruct,\n  1268:         E: [const] Destruct,\n  1269:     {\n  1270:         match self {\n  1271:             Ok(x) => x,\n  1272:             Err(_) => Default::default(),\n  1273:         }\n  1274:     }\n  1275: \n  1276:     /// Returns the contained [`Err`] value, consuming the `self` value.\n  1277:     ///\n  1278:     /// # Panics\n  1279:     ///\n  1280:     /// Panics if the value is an [`Ok`], with a panic message including the\n  1281:     /// passed message, and the content of the [`Ok`].",
    "nanvix_source": "  1253:     ///\n  1254:     /// assert_eq!(1909, good_year);\n  1255:     /// assert_eq!(0, bad_year);\n  1256:     /// ```\n  1257:     ///\n  1258:     /// [`parse`]: str::parse\n  1259:     /// [`FromStr`]: crate::str::FromStr\n  1260:     #[inline]\n  1261:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1262:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1263:     pub const fn unwrap_or_default(self) -> T\n  1264:     where\n  1265:         T: [const] Default + [const] Destruct,\n  1266:         E: [const] Destruct,\n  1267:     {\n  1268:         match self {\n  1269:             Ok(x) => x,\n  1270:             Err(_) => Default::default(),\n  1271:         }\n  1272:     }\n  1273: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::TryLockResult::unwrap_or_else",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "generic": "E"
                            }
                          ],
                          "output": {
                            "generic": "T"
                          }
                        }
                      },
                      "id": 24,
                      "path": "FnOnce"
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
      "name": "unwrap_or_else",
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
              "generic": "Self"
            }
          ],
          [
            "op",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1600: \n  1601:     /// Returns the contained [`Ok`] value or computes it from a closure.\n  1602:     ///\n  1603:     ///\n  1604:     /// # Examples\n  1605:     ///\n  1606:     /// ```\n  1607:     /// fn count(x: &str) -> usize { x.len() }\n  1608:     ///\n  1609:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1610:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1611:     /// ```\n  1612:     #[inline]\n  1613:     #[track_caller]\n  1614:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1615:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1616:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1617:     where\n  1618:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1619:     {\n  1620:         match self {\n  1621:             Ok(t) => t,\n  1622:             Err(e) => op(e),\n  1623:         }\n  1624:     }\n  1625: \n  1626:     /// Returns the contained [`Ok`] value, consuming the `self` value,\n  1627:     /// without checking that the value is not an [`Err`].\n  1628:     ///\n  1629:     /// # Safety\n  1630:     ///\n  1631:     /// Calling this method on an [`Err`] is *[undefined behavior]*.\n  1632:     ///",
    "nanvix_source": "  1604:     /// ```\n  1605:     /// fn count(x: &str) -> usize { x.len() }\n  1606:     ///\n  1607:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1608:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1609:     /// ```\n  1610:     #[inline]\n  1611:     #[track_caller]\n  1612:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1613:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1614:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1615:     where\n  1616:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1617:     {\n  1618:         match self {\n  1619:             Ok(t) => t,\n  1620:             Err(e) => op(e),\n  1621:         }\n  1622:     }\n  1623: \n  1624:     /// Returns the contained [`Ok`] value, consuming the `self` value,",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::TryLockResult::unwrap_unchecked",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
        "is_unsafe": true
      },
      "name": "unwrap_unchecked",
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
    "verification_source": "  1634:     ///\n  1635:     /// # Examples\n  1636:     ///\n  1637:     /// ```\n  1638:     /// let x: Result<u32, &str> = Ok(2);\n  1639:     /// assert_eq!(unsafe { x.unwrap_unchecked() }, 2);\n  1640:     /// ```\n  1641:     ///\n  1642:     /// ```no_run\n  1643:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1644:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1645:     /// ```\n  1646:     #[inline]\n  1647:     #[track_caller]\n  1648:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1649:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1650:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1651:         match self {\n  1652:             Ok(t) => t,\n  1653:             Err(e) => {\n  1654:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1655:                 super::mem::forget(e);\n  1656:                 // SAFETY: the safety contract must be upheld by the caller.\n  1657:                 unsafe { hint::unreachable_unchecked() }\n  1658:             }\n  1659:         }\n  1660:     }\n  1661: \n  1662:     /// Returns the contained [`Err`] value, consuming the `self` value,\n  1663:     /// without checking that the value is not an [`Ok`].\n  1664:     ///\n  1665:     /// # Safety\n  1666:     ///",
    "nanvix_source": "  1638:     /// ```\n  1639:     ///\n  1640:     /// ```no_run\n  1641:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1642:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1647:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1648:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1649:         match self {\n  1650:             Ok(t) => t,\n  1651:             Err(e) => {\n  1652:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1653:                 super::mem::forget(e);\n  1654:                 // SAFETY: the safety contract must be upheld by the caller.\n  1655:                 unsafe { hint::unreachable_unchecked() }\n  1656:             }\n  1657:         }\n  1658:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::WaitTimeoutResult::timed_out",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "timed_out",
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
            "id": 8524,
            "path": "WaitTimeoutResult"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9254",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8524",
        "resolved_owner_path": [
          "std",
          "sync",
          "WaitTimeoutResult"
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
    "verification_source": "   267:     /// ```\n   268:     /// use std::sync::{Arc, Condvar, Mutex};\n   269:     /// use std::thread;\n   270:     /// use std::time::Duration;\n   271:     ///\n   272:     /// let pair = Arc::new((Mutex::new(false), Condvar::new()));\n   273:     /// let pair2 = Arc::clone(&pair);\n   274:     ///\n   275:     /// # let handle =\n   276:     /// thread::spawn(move || {\n   277:     ///     let (lock, cvar) = &*pair2;\n   278:     ///\n   279:     ///     // Let's wait 20 milliseconds before notifying the condvar.\n   280:     ///     thread::sleep(Duration::from_millis(20));\n   281:     ///\n   282:     ///     let mut started = lock.lock().unwrap();\n   283:     ///     // We update the boolean value.\n   284:     ///     *started = true;\n   285:     ///     cvar.notify_one();\n   286:     /// });\n   287:     ///\n   288:     /// // Wait for the thread to start up.\n   289:     /// let (lock, cvar) = &*pair;\n   290:     /// loop {\n   291:     ///     // Let's put a timeout on the condvar's wait.\n   292:     ///     let result = cvar.wait_timeout(lock.lock().unwrap(), Duration::from_millis(10)).unwrap();\n   293:     ///     // 10 milliseconds have passed.\n   294:     ///     if result.1.timed_out() {\n   295:     ///         // timed out now and we can leave.\n   296:     ///         break\n   297:     ///     }\n   298:     /// }\n   299:     /// # // Prevent leaks for Miri.",
    "nanvix_source": "   281:     /// let pair2 = Arc::clone(&pair);\n   282:     ///\n   283:     /// # let handle =\n   284:     /// thread::spawn(move || {\n   285:     ///     let (lock, cvar) = &*pair2;\n   286:     ///\n   287:     ///     // Let's wait 20 milliseconds before notifying the condvar.\n   288:     ///     thread::sleep(Duration::from_millis(20));\n   289:     ///\n   290:     ///     let mut started = lock.lock().unwrap();\n   291:     ///     // We update the boolean value.\n   292:     ///     *started = true;\n   293:     ///     cvar.notify_one();\n   294:     /// });\n   295:     ///\n   296:     /// // Wait for the thread to start up.\n   297:     /// let (lock, cvar) = &*pair;\n   298:     /// loop {\n   299:     ///     // Let's put a timeout on the condvar's wait.\n   300:     ///     let result = cvar.wait_timeout(lock.lock().unwrap(), Duration::from_millis(10)).unwrap();\n   301:     ///     // 10 milliseconds have passed.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::Receiver::iter",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "iter",
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
            "id": 7865,
            "path": "Receiver"
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
        "impl_id": "std:7876",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7865",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Receiver"
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
                    "lifetime": "'_"
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
            "id": 7872,
            "path": "Iter"
          }
        }
      }
    },
    "verification_source": "  1004:     ///\n  1005:     /// let (send, recv) = channel();\n  1006:     ///\n  1007:     /// thread::spawn(move || {\n  1008:     ///     send.send(1).unwrap();\n  1009:     ///     send.send(2).unwrap();\n  1010:     ///     send.send(3).unwrap();\n  1011:     /// });\n  1012:     ///\n  1013:     /// let mut iter = recv.iter();\n  1014:     /// assert_eq!(iter.next(), Some(1));\n  1015:     /// assert_eq!(iter.next(), Some(2));\n  1016:     /// assert_eq!(iter.next(), Some(3));\n  1017:     /// assert_eq!(iter.next(), None);\n  1018:     /// ```\n  1019:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1020:     pub fn iter(&self) -> Iter<'_, T> {\n  1021:         Iter { rx: self }\n  1022:     }\n  1023: \n  1024:     /// Returns an iterator that will attempt to yield all pending values.\n  1025:     /// It will return `None` if there are no more pending values or if the\n  1026:     /// channel has hung up. The iterator will never [`panic!`] or block the\n  1027:     /// user by waiting for values.\n  1028:     ///\n  1029:     /// # Examples\n  1030:     ///\n  1031:     /// ```no_run\n  1032:     /// use std::sync::mpsc::channel;\n  1033:     /// use std::thread;\n  1034:     /// use std::time::Duration;\n  1035:     ///\n  1036:     /// let (sender, receiver) = channel();",
    "nanvix_source": "  1028:     ///     send.send(3).unwrap();\n  1029:     /// });\n  1030:     ///\n  1031:     /// let mut iter = recv.iter();\n  1032:     /// assert_eq!(iter.next(), Some(1));\n  1033:     /// assert_eq!(iter.next(), Some(2));\n  1034:     /// assert_eq!(iter.next(), Some(3));\n  1035:     /// assert_eq!(iter.next(), None);\n  1036:     /// ```\n  1037:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1038:     pub fn iter(&self) -> Iter<'_, T> {\n  1039:         Iter { rx: self }\n  1040:     }\n  1041: \n  1042:     /// Returns an iterator that will attempt to yield all pending values.\n  1043:     /// It will return `None` if there are no more pending values or if the\n  1044:     /// channel has hung up. The iterator will never [`panic!`] or block the\n  1045:     /// user by waiting for values.\n  1046:     ///\n  1047:     /// # Examples\n  1048:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::Receiver::recv",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "recv",
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
            "id": 7865,
            "path": "Receiver"
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
        "impl_id": "std:7876",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7865",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Receiver"
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
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 7657,
                        "path": "RecvError"
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
    "verification_source": "   855:     /// let handle = thread::spawn(move || {\n   856:     ///     send.send(1u8).unwrap();\n   857:     ///     send.send(2).unwrap();\n   858:     ///     send.send(3).unwrap();\n   859:     ///     drop(send);\n   860:     /// });\n   861:     ///\n   862:     /// // wait for the thread to join so we ensure the sender is dropped\n   863:     /// handle.join().unwrap();\n   864:     ///\n   865:     /// assert_eq!(Ok(1), recv.recv());\n   866:     /// assert_eq!(Ok(2), recv.recv());\n   867:     /// assert_eq!(Ok(3), recv.recv());\n   868:     /// assert_eq!(Err(RecvError), recv.recv());\n   869:     /// ```\n   870:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   871:     pub fn recv(&self) -> Result<T, RecvError> {\n   872:         self.inner.recv()\n   873:     }\n   874: \n   875:     /// Attempts to wait for a value on this receiver, returning an error if the\n   876:     /// corresponding channel has hung up, or if it waits more than `timeout`.\n   877:     ///\n   878:     /// This function will always block the current thread if there is no data\n   879:     /// available and it's possible for more data to be sent (at least one sender\n   880:     /// still exists). Once a message is sent to the corresponding [`Sender`]\n   881:     /// (or [`SyncSender`]), this receiver will wake up and return that\n   882:     /// message.\n   883:     ///\n   884:     /// If the corresponding [`Sender`] has disconnected, or it disconnects while\n   885:     /// this call is blocking, this call will wake up and return [`Err`] to\n   886:     /// indicate that no more messages can ever be received on this channel.\n   887:     /// However, since channels are buffered, messages sent before the disconnect",
    "nanvix_source": "   879:     ///\n   880:     /// // wait for the thread to join so we ensure the sender is dropped\n   881:     /// handle.join().unwrap();\n   882:     ///\n   883:     /// assert_eq!(Ok(1), recv.recv());\n   884:     /// assert_eq!(Ok(2), recv.recv());\n   885:     /// assert_eq!(Ok(3), recv.recv());\n   886:     /// assert_eq!(Err(RecvError), recv.recv());\n   887:     /// ```\n   888:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   889:     pub fn recv(&self) -> Result<T, RecvError> {\n   890:         self.inner.recv()\n   891:     }\n   892: \n   893:     /// Attempts to wait for a value on this receiver, returning an error if the\n   894:     /// corresponding channel has hung up, or if it waits more than `timeout`.\n   895:     ///\n   896:     /// This function will always block the current thread if there is no data\n   897:     /// available and it's possible for more data to be sent (at least one sender\n   898:     /// still exists). Once a message is sent to the corresponding [`Sender`]\n   899:     /// (or [`SyncSender`]), this receiver will wake up and return that",
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
