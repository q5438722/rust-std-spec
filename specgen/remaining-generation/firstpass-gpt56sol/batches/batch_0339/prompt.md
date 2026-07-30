For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::write_bytes",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant",
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
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
                "generic": "T"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "write_bytes",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        },
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
                          "id": 7872,
                          "path": "PointeeSized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51704",
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
              "generic": "Self"
            }
          ],
          [
            "val",
            {
              "primitive": "u8"
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1416:     {\n  1417:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1418:         unsafe { write(self, val) }\n  1419:     }\n  1420: \n  1421:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1422:     /// bytes of memory starting at `self` to `val`.\n  1423:     ///\n  1424:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1425:     ///\n  1426:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1427:     #[doc(alias = \"memset\")]\n  1428:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1429:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1430:     #[inline(always)]\n  1431:     #[track_caller]\n  1432:     pub const unsafe fn write_bytes(self, val: u8, count: usize)\n  1433:     where\n  1434:         T: Sized,\n  1435:     {\n  1436:         // SAFETY: the caller must uphold the safety contract for `write_bytes`.\n  1437:         unsafe { write_bytes(self, val, count) }\n  1438:     }\n  1439: \n  1440:     /// Performs a volatile write of a memory location with the given value without\n  1441:     /// reading or dropping the old value.\n  1442:     ///\n  1443:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1444:     /// to not be elided or reordered by the compiler across other volatile\n  1445:     /// operations.\n  1446:     ///\n  1447:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1448:     ///",
    "nanvix_source": "  1404:     /// bytes of memory starting at `self` to `val`.\n  1405:     ///\n  1406:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1407:     ///\n  1408:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1409:     #[doc(alias = \"memset\")]\n  1410:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1411:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1412:     #[inline(always)]\n  1413:     #[track_caller]\n  1414:     pub const unsafe fn write_bytes(self, val: u8, count: usize)\n  1415:     where\n  1416:         T: Sized,\n  1417:     {\n  1418:         // SAFETY: the caller must uphold the safety contract for `write_bytes`.\n  1419:         unsafe { write_bytes(self, val, count) }\n  1420:     }\n  1421: \n  1422:     /// Performs a volatile write of a memory location with the given value without\n  1423:     /// reading or dropping the old value.\n  1424:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::write_unaligned",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant",
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
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
                "generic": "T"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "write_unaligned",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        },
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
                          "id": 7872,
                          "path": "PointeeSized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51704",
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
              "generic": "Self"
            }
          ],
          [
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1457:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1458:         unsafe { write_volatile(self, val) }\n  1459:     }\n  1460: \n  1461:     /// Overwrites a memory location with the given value without reading or\n  1462:     /// dropping the old value.\n  1463:     ///\n  1464:     /// Unlike `write`, the pointer may be unaligned.\n  1465:     ///\n  1466:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1467:     ///\n  1468:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1469:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1470:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1471:     #[inline(always)]\n  1472:     #[track_caller]\n  1473:     pub const unsafe fn write_unaligned(self, val: T)\n  1474:     where\n  1475:         T: Sized,\n  1476:     {\n  1477:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1478:         unsafe { write_unaligned(self, val) }\n  1479:     }\n  1480: \n  1481:     /// Replaces the value at `self` with `src`, returning the old\n  1482:     /// value, without dropping either.\n  1483:     ///\n  1484:     /// See [`ptr::replace`] for safety concerns and examples.\n  1485:     ///\n  1486:     /// [`ptr::replace`]: crate::ptr::replace()\n  1487:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1488:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]\n  1489:     #[inline(always)]",
    "nanvix_source": "  1445:     ///\n  1446:     /// Unlike `write`, the pointer may be unaligned.\n  1447:     ///\n  1448:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1449:     ///\n  1450:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1451:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1452:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1453:     #[inline(always)]\n  1454:     #[track_caller]\n  1455:     pub const unsafe fn write_unaligned(self, val: T)\n  1456:     where\n  1457:         T: Sized,\n  1458:     {\n  1459:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1460:         unsafe { write_unaligned(self, val) }\n  1461:     }\n  1462: \n  1463:     /// Replaces the value at `self` with `src`, returning the old\n  1464:     /// value, without dropping either.\n  1465:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::write_volatile",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function",
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant",
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
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
        "is_unsafe": true
      },
      "name": "write_volatile",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        },
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
                          "id": 7872,
                          "path": "PointeeSized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51704",
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
              "generic": "Self"
            }
          ],
          [
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1437:         unsafe { write_bytes(self, val, count) }\n  1438:     }\n  1439: \n  1440:     /// Performs a volatile write of a memory location with the given value without\n  1441:     /// reading or dropping the old value.\n  1442:     ///\n  1443:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1444:     /// to not be elided or reordered by the compiler across other volatile\n  1445:     /// operations.\n  1446:     ///\n  1447:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1448:     ///\n  1449:     /// [`ptr::write_volatile`]: crate::ptr::write_volatile()\n  1450:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1451:     #[inline(always)]\n  1452:     #[track_caller]\n  1453:     pub unsafe fn write_volatile(self, val: T)\n  1454:     where\n  1455:         T: Sized,\n  1456:     {\n  1457:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1458:         unsafe { write_volatile(self, val) }\n  1459:     }\n  1460: \n  1461:     /// Overwrites a memory location with the given value without reading or\n  1462:     /// dropping the old value.\n  1463:     ///\n  1464:     /// Unlike `write`, the pointer may be unaligned.\n  1465:     ///\n  1466:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1467:     ///\n  1468:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1469:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]",
    "nanvix_source": "  1425:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1426:     /// to not be elided or reordered by the compiler across other volatile\n  1427:     /// operations.\n  1428:     ///\n  1429:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1430:     ///\n  1431:     /// [`ptr::write_volatile`]: crate::ptr::write_volatile()\n  1432:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1433:     #[inline(always)]\n  1434:     #[track_caller]\n  1435:     pub unsafe fn write_volatile(self, val: T)\n  1436:     where\n  1437:         T: Sized,\n  1438:     {\n  1439:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1440:         unsafe { write_volatile(self, val) }\n  1441:     }\n  1442: \n  1443:     /// Overwrites a memory location with the given value without reading or\n  1444:     /// dropping the old value.\n  1445:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::cloned",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "multiple_rust_declarations_share_path"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 42,
                      "path": "Clone"
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
      "name": "cloned",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
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
        "impl_id": "core:29313",
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
        }
      }
    },
    "verification_source": "  1721:     }\n  1722: \n  1723:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by cloning the contents of the\n  1724:     /// `Ok` part.\n  1725:     ///\n  1726:     /// # Examples\n  1727:     ///\n  1728:     /// ```\n  1729:     /// let val = 12;\n  1730:     /// let x: Result<&i32, i32> = Ok(&val);\n  1731:     /// assert_eq!(x, Ok(&12));\n  1732:     /// let cloned = x.cloned();\n  1733:     /// assert_eq!(cloned, Ok(12));\n  1734:     /// ```\n  1735:     #[inline]\n  1736:     #[stable(feature = \"result_cloned\", since = \"1.59.0\")]\n  1737:     pub fn cloned(self) -> Result<T, E>\n  1738:     where\n  1739:         T: Clone,\n  1740:     {\n  1741:         self.map(|t| t.clone())\n  1742:     }\n  1743: }\n  1744: \n  1745: impl<T, E> Result<&mut T, E> {\n  1746:     /// Maps a `Result<&mut T, E>` to a `Result<T, E>` by copying the contents of the\n  1747:     /// `Ok` part.\n  1748:     ///\n  1749:     /// # Examples\n  1750:     ///\n  1751:     /// ```\n  1752:     /// let mut val = 12;\n  1753:     /// let x: Result<&mut i32, i32> = Ok(&mut val);",
    "nanvix_source": "  1730:     ///\n  1731:     /// ```\n  1732:     /// let val = 12;\n  1733:     /// let x: Result<&i32, i32> = Ok(&val);\n  1734:     /// assert_eq!(x, Ok(&12));\n  1735:     /// let cloned = x.cloned();\n  1736:     /// assert_eq!(cloned, Ok(12));\n  1737:     /// ```\n  1738:     #[inline]\n  1739:     #[stable(feature = \"result_cloned\", since = \"1.59.0\")]\n  1740:     pub fn cloned(self) -> Result<T, E>\n  1741:     where\n  1742:         T: Clone,\n  1743:     {\n  1744:         self.map(|t| t.clone())\n  1745:     }\n  1746: }\n  1747: \n  1748: impl<T, E> Result<&mut T, E> {\n  1749:     /// Maps a `Result<&mut T, E>` to a `Result<T, E>` by copying the contents of the\n  1750:     /// `Ok` part.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::copied",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "multiple_rust_declarations_share_path"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 6,
                      "path": "Copy"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "copied",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "T"
                        }
                      }
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
        "impl_id": "core:29313",
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
        }
      }
    },
    "verification_source": "  1695:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by copying the contents of the\n  1696:     /// `Ok` part.\n  1697:     ///\n  1698:     /// # Examples\n  1699:     ///\n  1700:     /// ```\n  1701:     /// let val = 12;\n  1702:     /// let x: Result<&i32, i32> = Ok(&val);\n  1703:     /// assert_eq!(x, Ok(&12));\n  1704:     /// let copied = x.copied();\n  1705:     /// assert_eq!(copied, Ok(12));\n  1706:     /// ```\n  1707:     #[inline]\n  1708:     #[stable(feature = \"result_copied\", since = \"1.59.0\")]\n  1709:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1710:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1711:     pub const fn copied(self) -> Result<T, E>\n  1712:     where\n  1713:         T: Copy,\n  1714:     {\n  1715:         // FIXME(const-hack): this implementation, which sidesteps using `Result::map` since it's not const\n  1716:         // ready yet, should be reverted when possible to avoid code repetition\n  1717:         match self {\n  1718:             Ok(&v) => Ok(v),\n  1719:             Err(e) => Err(e),\n  1720:         }\n  1721:     }\n  1722: \n  1723:     /// Maps a `Result<&T, E>` to a `Result<T, E>` by cloning the contents of the\n  1724:     /// `Ok` part.\n  1725:     ///\n  1726:     /// # Examples\n  1727:     ///",
    "nanvix_source": "  1704:     /// let val = 12;\n  1705:     /// let x: Result<&i32, i32> = Ok(&val);\n  1706:     /// assert_eq!(x, Ok(&12));\n  1707:     /// let copied = x.copied();\n  1708:     /// assert_eq!(copied, Ok(12));\n  1709:     /// ```\n  1710:     #[inline]\n  1711:     #[stable(feature = \"result_copied\", since = \"1.59.0\")]\n  1712:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1713:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1714:     pub const fn copied(self) -> Result<T, E>\n  1715:     where\n  1716:         T: Copy,\n  1717:     {\n  1718:         // FIXME(const-hack): this implementation, which sidesteps using `Result::map` since it's not const\n  1719:         // ready yet, should be reverted when possible to avoid code repetition\n  1720:         match self {\n  1721:             Ok(&v) => Ok(v),\n  1722:             Err(e) => Err(e),\n  1723:         }\n  1724:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::unwrap_err_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
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
