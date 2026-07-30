For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Result::unwrap_err_unchecked",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
        "is_unsafe": true
      },
      "name": "unwrap_err_unchecked",
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
          "generic": "E"
        }
      }
    },
    "verification_source": "  1669:     /// [undefined behavior]: https://doc.rust-lang.org/reference/behavior-considered-undefined.html\n  1670:     ///\n  1671:     /// # Examples\n  1672:     ///\n  1673:     /// ```no_run\n  1674:     /// let x: Result<u32, &str> = Ok(2);\n  1675:     /// unsafe { x.unwrap_err_unchecked() }; // Undefined behavior!\n  1676:     /// ```\n  1677:     ///\n  1678:     /// ```\n  1679:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1680:     /// assert_eq!(unsafe { x.unwrap_err_unchecked() }, \"emergency failure\");\n  1681:     /// ```\n  1682:     #[inline]\n  1683:     #[track_caller]\n  1684:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1685:     pub unsafe fn unwrap_err_unchecked(self) -> E {\n  1686:         match self {\n  1687:             // SAFETY: the safety contract must be upheld by the caller.\n  1688:             Ok(_) => unsafe { hint::unreachable_unchecked() },\n  1689:             Err(e) => e,\n  1690:         }\n  1691:     }\n  1692: }\n  1693: \n  1694: impl<T, E> Result<&T, E> {\n  1695:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by copying the contents of the\n  1696:     /// `Ok` part.\n  1697:     ///\n  1698:     /// # Examples\n  1699:     ///\n  1700:     /// ```\n  1701:     /// let val = 12;",
    "nanvix_source": "  1674:     /// ```\n  1675:     ///\n  1676:     /// ```\n  1677:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1678:     /// assert_eq!(unsafe { x.unwrap_err_unchecked() }, \"emergency failure\");\n  1679:     /// ```\n  1680:     #[inline]\n  1681:     #[track_caller]\n  1682:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1683:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1684:     pub const unsafe fn unwrap_err_unchecked(self) -> E\n  1685:     where\n  1686:         T: [const] Destruct,\n  1687:         E: [const] Destruct,\n  1688:     {\n  1689:         match self {\n  1690:             // SAFETY: the safety contract must be upheld by the caller.\n  1691:             Ok(_) => unsafe { hint::unreachable_unchecked() },\n  1692:             Err(e) => e,\n  1693:         }\n  1694:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::unwrap_or",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
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
      "name": "unwrap_or",
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
            "default",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1574:     ///\n  1575:     /// [`unwrap_or_else`]: Result::unwrap_or_else\n  1576:     ///\n  1577:     /// # Examples\n  1578:     ///\n  1579:     /// ```\n  1580:     /// let default = 2;\n  1581:     /// let x: Result<u32, &str> = Ok(9);\n  1582:     /// assert_eq!(x.unwrap_or(default), 9);\n  1583:     ///\n  1584:     /// let x: Result<u32, &str> = Err(\"error\");\n  1585:     /// assert_eq!(x.unwrap_or(default), default);\n  1586:     /// ```\n  1587:     #[inline]\n  1588:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1589:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1590:     pub const fn unwrap_or(self, default: T) -> T\n  1591:     where\n  1592:         T: [const] Destruct,\n  1593:         E: [const] Destruct,\n  1594:     {\n  1595:         match self {\n  1596:             Ok(t) => t,\n  1597:             Err(_) => default,\n  1598:         }\n  1599:     }\n  1600: \n  1601:     /// Returns the contained [`Ok`] value or computes it from a closure.\n  1602:     ///\n  1603:     ///\n  1604:     /// # Examples\n  1605:     ///\n  1606:     /// ```",
    "nanvix_source": "  1578:     /// let default = 2;\n  1579:     /// let x: Result<u32, &str> = Ok(9);\n  1580:     /// assert_eq!(x.unwrap_or(default), 9);\n  1581:     ///\n  1582:     /// let x: Result<u32, &str> = Err(\"error\");\n  1583:     /// assert_eq!(x.unwrap_or(default), default);\n  1584:     /// ```\n  1585:     #[inline]\n  1586:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1587:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1588:     pub const fn unwrap_or(self, default: T) -> T\n  1589:     where\n  1590:         T: [const] Destruct,\n  1591:         E: [const] Destruct,\n  1592:     {\n  1593:         match self {\n  1594:             Ok(t) => t,\n  1595:             Err(_) => default,\n  1596:         }\n  1597:     }\n  1598: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Result::unwrap_or_default",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
    "target": "core::fmt::Result::unwrap_or_else",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
    "target": "core::fmt::Result::unwrap_unchecked",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "formatting_effect"
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
    "target": "core::fmt::from_fn",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "formatting_effect"
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
                          "parenthesized": {
                            "inputs": [
                              {
                                "borrowed_ref": {
                                  "is_mutable": true,
                                  "lifetime": null,
                                  "type": {
                                    "resolved_path": {
                                      "args": {
                                        "angle_bracketed": {
                                          "args": [
                                            {
                                              "lifetime": "'_"
                                            }
                                          ],
                                          "constraints": []
                                        }
                                      },
                                      "id": 918,
                                      "path": "fmt::Formatter"
                                    }
                                  }
                                }
                              }
                            ],
                            "output": {
                              "resolved_path": {
                                "args": null,
                                "id": 919,
                                "path": "fmt::Result"
                              }
                            }
                          }
                        },
                        "id": 20,
                        "path": "Fn"
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
        "is_const": true,
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
            "id": 13427,
            "path": "FromFn"
          }
        }
      }
    },
    "verification_source": "  1208:     fn is_pretty(&self) -> bool {\n  1209:         self.fmt.alternate()\n  1210:     }\n  1211: }\n  1212: \n  1213: /// Creates a type whose [`fmt::Debug`] and [`fmt::Display`] impls are\n  1214: /// forwarded to the provided closure.\n  1215: ///\n  1216: /// # Examples\n  1217: ///\n  1218: /// ```\n  1219: /// use std::fmt;\n  1220: ///\n  1221: /// let value = 'a';\n  1222: /// assert_eq!(format!(\"{}\", value), \"a\");\n  1223: /// assert_eq!(format!(\"{:?}\", value), \"'a'\");\n  1224: ///\n  1225: /// let wrapped = fmt::from_fn(|f| write!(f, \"{value:?}\"));\n  1226: /// assert_eq!(format!(\"{}\", wrapped), \"'a'\");\n  1227: /// assert_eq!(format!(\"{:?}\", wrapped), \"'a'\");\n  1228: /// ```\n  1229: #[stable(feature = \"fmt_from_fn\", since = \"1.93.0\")]\n  1230: #[rustc_const_stable(feature = \"const_fmt_from_fn\", since = \"1.95.0\")]\n  1231: #[must_use = \"returns a type implementing Debug and Display, which do not have any effects unless they are used\"]\n  1232: pub const fn from_fn<F: Fn(&mut fmt::Formatter<'_>) -> fmt::Result>(f: F) -> FromFn<F> {\n  1233:     FromFn(f)\n  1234: }\n  1235: \n  1236: /// Implements [`fmt::Debug`] and [`fmt::Display`] via the provided closure.\n  1237: ///\n  1238: /// Created with [`from_fn`].\n  1239: #[stable(feature = \"fmt_from_fn\", since = \"1.93.0\")]\n  1240: pub struct FromFn<F>(F);",
    "nanvix_source": "  1214: /// forwarded to the provided closure.\n  1215: ///\n  1216: /// # Examples\n  1217: ///\n  1218: /// ```\n  1219: /// use std::fmt;\n  1220: ///\n  1221: /// let value = 'a';\n  1222: /// assert_eq!(format!(\"{}\", value), \"a\");\n  1223: /// assert_eq!(format!(\"{:?}\", value), \"'a'\");\n  1224: ///\n  1225: /// let wrapped = fmt::from_fn(|f| write!(f, \"{value:?}\"));\n  1226: /// assert_eq!(format!(\"{}\", wrapped), \"'a'\");\n  1227: /// assert_eq!(format!(\"{:?}\", wrapped), \"'a'\");\n  1228: /// ```\n  1229: #[stable(feature = \"fmt_from_fn\", since = \"1.93.0\")]\n  1230: #[rustc_const_stable(feature = \"const_fmt_from_fn\", since = \"1.95.0\")]\n  1231: #[must_use = \"returns a type implementing Debug and Display, which do not have any effects unless they are used\"]\n  1232: pub const fn from_fn<F: Fn(&mut fmt::Formatter<'_>) -> fmt::Result>(f: F) -> FromFn<F> {\n  1233:     FromFn(f)\n  1234: }",
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
