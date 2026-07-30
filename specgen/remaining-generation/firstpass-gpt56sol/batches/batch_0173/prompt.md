For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::vec::Vec::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
    "verification_source": "  1617:     ///\n  1618:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1619:     ///\n  1620:     /// # Examples\n  1621:     ///\n  1622:     /// ```\n  1623:     /// let mut vec = Vec::with_capacity(10);\n  1624:     /// vec.extend([1, 2, 3]);\n  1625:     /// assert!(vec.capacity() >= 10);\n  1626:     /// vec.shrink_to(4);\n  1627:     /// assert!(vec.capacity() >= 4);\n  1628:     /// vec.shrink_to(0);\n  1629:     /// assert!(vec.capacity() >= 3);\n  1630:     /// ```\n  1631:     #[cfg(not(no_global_oom_handling))]\n  1632:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1633:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1634:         if self.capacity() > min_capacity {\n  1635:             self.buf.shrink_to_fit(cmp::max(self.len, min_capacity));\n  1636:         }\n  1637:     }\n  1638: \n  1639:     /// Tries to shrink the capacity of the vector as much as possible\n  1640:     ///\n  1641:     /// The behavior of this method depends on the allocator, which may either shrink the vector\n  1642:     /// in-place or reallocate. The resulting vector might still have some excess capacity, just as\n  1643:     /// is the case for [`with_capacity`]. See [`Allocator::shrink`] for more details.\n  1644:     ///\n  1645:     /// [`with_capacity`]: Vec::with_capacity\n  1646:     ///\n  1647:     /// # Errors\n  1648:     ///\n  1649:     /// This function returns an error if the allocator fails to shrink the allocation,",
    "nanvix_source": "  1621:     /// let mut vec = Vec::with_capacity(10);\n  1622:     /// vec.extend([1, 2, 3]);\n  1623:     /// assert!(vec.capacity() >= 10);\n  1624:     /// vec.shrink_to(4);\n  1625:     /// assert!(vec.capacity() >= 4);\n  1626:     /// vec.shrink_to(0);\n  1627:     /// assert!(vec.capacity() >= 3);\n  1628:     /// ```\n  1629:     #[cfg(not(no_global_oom_handling))]\n  1630:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1631:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1632:         if self.capacity() > min_capacity {\n  1633:             self.buf.shrink_to_fit(cmp::max(self.len, min_capacity));\n  1634:         }\n  1635:     }\n  1636: \n  1637:     /// Tries to shrink the capacity of the vector as much as possible\n  1638:     ///\n  1639:     /// The behavior of this method depends on the allocator, which may either shrink the vector\n  1640:     /// in-place or reallocate. The resulting vector might still have some excess capacity, just as\n  1641:     /// is the case for [`with_capacity`]. See [`Allocator::shrink`] for more details.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
    "verification_source": "  1588:     /// is the case for [`with_capacity`]. See [`Allocator::shrink`] for more details.\n  1589:     ///\n  1590:     /// [`with_capacity`]: Vec::with_capacity\n  1591:     ///\n  1592:     /// # Examples\n  1593:     ///\n  1594:     /// ```\n  1595:     /// let mut vec = Vec::with_capacity(10);\n  1596:     /// vec.extend([1, 2, 3]);\n  1597:     /// assert!(vec.capacity() >= 10);\n  1598:     /// vec.shrink_to_fit();\n  1599:     /// assert!(vec.capacity() >= 3);\n  1600:     /// ```\n  1601:     #[cfg(not(no_global_oom_handling))]\n  1602:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1603:     #[inline]\n  1604:     pub fn shrink_to_fit(&mut self) {\n  1605:         // The capacity is never less than the length, and there's nothing to do when\n  1606:         // they are equal, so we can avoid the panic case in `RawVec::shrink_to_fit`\n  1607:         // by only calling it with a greater capacity.\n  1608:         if self.capacity() > self.len {\n  1609:             self.buf.shrink_to_fit(self.len);\n  1610:         }\n  1611:     }\n  1612: \n  1613:     /// Shrinks the capacity of the vector with a lower bound.\n  1614:     ///\n  1615:     /// The capacity will remain at least as large as both the length\n  1616:     /// and the supplied value.\n  1617:     ///\n  1618:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1619:     ///\n  1620:     /// # Examples",
    "nanvix_source": "  1592:     /// ```\n  1593:     /// let mut vec = Vec::with_capacity(10);\n  1594:     /// vec.extend([1, 2, 3]);\n  1595:     /// assert!(vec.capacity() >= 10);\n  1596:     /// vec.shrink_to_fit();\n  1597:     /// assert!(vec.capacity() >= 3);\n  1598:     /// ```\n  1599:     #[cfg(not(no_global_oom_handling))]\n  1600:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1601:     #[inline]\n  1602:     pub fn shrink_to_fit(&mut self) {\n  1603:         // The capacity is never less than the length, and there's nothing to do when\n  1604:         // they are equal, so we can avoid the panic case in `RawVec::shrink_to_fit`\n  1605:         // by only calling it with a greater capacity.\n  1606:         if self.capacity() > self.len {\n  1607:             self.buf.shrink_to_fit(self.len);\n  1608:         }\n  1609:     }\n  1610: \n  1611:     /// Shrinks the capacity of the vector with a lower bound.\n  1612:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::try_reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 114,
            "path": "Vec"
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
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4948",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:114",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "Vec"
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
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1564:     /// fn process_data(data: &[u32]) -> Result<Vec<u32>, TryReserveError> {\n  1565:     ///     let mut output = Vec::new();\n  1566:     ///\n  1567:     ///     // Pre-reserve the memory, exiting if we can't\n  1568:     ///     output.try_reserve_exact(data.len())?;\n  1569:     ///\n  1570:     ///     // Now we know this can't OOM in the middle of our complex work\n  1571:     ///     output.extend(data.iter().map(|&val| {\n  1572:     ///         val * 2 + 5 // very complicated\n  1573:     ///     }));\n  1574:     ///\n  1575:     ///     Ok(output)\n  1576:     /// }\n  1577:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1578:     /// ```\n  1579:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1580:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1581:         self.buf.try_reserve_exact(self.len, additional)\n  1582:     }\n  1583: \n  1584:     /// Shrinks the capacity of the vector as much as possible.\n  1585:     ///\n  1586:     /// The behavior of this method depends on the allocator, which may either shrink the vector\n  1587:     /// in-place or reallocate. The resulting vector might still have some excess capacity, just as\n  1588:     /// is the case for [`with_capacity`]. See [`Allocator::shrink`] for more details.\n  1589:     ///\n  1590:     /// [`with_capacity`]: Vec::with_capacity\n  1591:     ///\n  1592:     /// # Examples\n  1593:     ///\n  1594:     /// ```\n  1595:     /// let mut vec = Vec::with_capacity(10);\n  1596:     /// vec.extend([1, 2, 3]);",
    "nanvix_source": "  1568:     ///     // Now we know this can't OOM in the middle of our complex work\n  1569:     ///     output.extend(data.iter().map(|&val| {\n  1570:     ///         val * 2 + 5 // very complicated\n  1571:     ///     }));\n  1572:     ///\n  1573:     ///     Ok(output)\n  1574:     /// }\n  1575:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1576:     /// ```\n  1577:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1578:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1579:         self.buf.try_reserve_exact(self.len, additional)\n  1580:     }\n  1581: \n  1582:     /// Shrinks the capacity of the vector as much as possible.\n  1583:     ///\n  1584:     /// The behavior of this method depends on the allocator, which may either shrink the vector\n  1585:     /// in-place or reallocate. The resulting vector might still have some excess capacity, just as\n  1586:     /// is the case for [`with_capacity`]. See [`Allocator::shrink`] for more details.\n  1587:     ///\n  1588:     /// [`with_capacity`]: Vec::with_capacity",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::dangling_ptr",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "dangling_ptr",
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
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
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
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9475,
            "path": "NonNull"
          }
        }
      }
    },
    "verification_source": "   254:         // SAFETY: we pass along the prerequisites of these functions to the caller\n   255:         let (size, alignment) = unsafe { (mem::size_of_val_raw(t), Alignment::of_val_raw(t)) };\n   256:         // SAFETY: see rationale in `new` for why this is using the unsafe variant\n   257:         unsafe { Layout::from_size_alignment_unchecked(size, alignment) }\n   258:     }\n   259: \n   260:     /// Creates a `NonNull` that is dangling, but well-aligned for this Layout.\n   261:     ///\n   262:     /// Note that the address of the returned pointer may potentially\n   263:     /// be that of a valid pointer, which means this must not be used\n   264:     /// as a \"not yet initialized\" sentinel value.\n   265:     /// Types that lazily allocate must track initialization by some other means.\n   266:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   267:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   268:     #[must_use]\n   269:     #[inline]\n   270:     pub const fn dangling_ptr(&self) -> NonNull<u8> {\n   271:         NonNull::without_provenance(self.align.as_nonzero_usize())\n   272:     }\n   273: \n   274:     /// Creates a layout describing the record that can hold a value\n   275:     /// of the same layout as `self`, but that also is aligned to\n   276:     /// alignment `align` (measured in bytes).\n   277:     ///\n   278:     /// If `self` already meets the prescribed alignment, then returns\n   279:     /// `self`.\n   280:     ///\n   281:     /// Note that this method does not add any padding to the overall\n   282:     /// size, regardless of whether the returned layout has a different\n   283:     /// alignment. In other words, if `K` has size 16, `K.align_to(32)`\n   284:     /// will *still* have size 16.\n   285:     ///\n   286:     /// Returns an error if the combination of `self.size()` and the given",
    "nanvix_source": "   260:     /// Creates a `NonNull` that is dangling, but well-aligned for this Layout.\n   261:     ///\n   262:     /// Note that the address of the returned pointer may potentially\n   263:     /// be that of a valid pointer, which means this must not be used\n   264:     /// as a \"not yet initialized\" sentinel value.\n   265:     /// Types that lazily allocate must track initialization by some other means.\n   266:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   267:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   268:     #[must_use]\n   269:     #[inline]\n   270:     pub const fn dangling_ptr(&self) -> NonNull<u8> {\n   271:         NonNull::without_provenance(self.align.as_nonzero_usize())\n   272:     }\n   273: \n   274:     /// Creates a layout describing the record that can hold a value\n   275:     /// of the same layout as `self`, but that also is aligned to\n   276:     /// alignment `align` (measured in bytes).\n   277:     ///\n   278:     /// If `self` already meets the prescribed alignment, then returns\n   279:     /// `self`.\n   280:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::fn_addr_eq",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
                        "id": 9617,
                        "path": "FnPtr"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
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
                        "id": 9617,
                        "path": "FnPtr"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
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
      "name": "fn_addr_eq",
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
              "generic": "T"
            }
          ],
          [
            "g",
            {
              "generic": "U"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  2484: ///\n  2485: ///\n  2486: /// # Examples\n  2487: ///\n  2488: /// ```\n  2489: /// use std::ptr;\n  2490: ///\n  2491: /// fn a() { println!(\"a\"); }\n  2492: /// fn b() { println!(\"b\"); }\n  2493: /// assert!(!ptr::fn_addr_eq(a as fn(), b as fn()));\n  2494: /// ```\n  2495: ///\n  2496: /// [subtype]: https://doc.rust-lang.org/reference/subtyping.html\n  2497: #[stable(feature = \"ptr_fn_addr_eq\", since = \"1.85.0\")]\n  2498: #[inline(always)]\n  2499: #[must_use = \"function pointer comparison produces a value\"]\n  2500: pub fn fn_addr_eq<T: FnPtr, U: FnPtr>(f: T, g: U) -> bool {\n  2501:     f.addr() == g.addr()\n  2502: }\n  2503: \n  2504: /// Hash a raw pointer.\n  2505: ///\n  2506: /// This can be used to hash a `&T` reference (which coerces to `*const T` implicitly)\n  2507: /// by its address rather than the value it points to\n  2508: /// (which is what the `Hash for &T` implementation does).\n  2509: ///\n  2510: /// # Examples\n  2511: ///\n  2512: /// ```\n  2513: /// use std::hash::{DefaultHasher, Hash, Hasher};\n  2514: /// use std::ptr;\n  2515: ///\n  2516: /// let five = 5;",
    "nanvix_source": "  2542: ///\n  2543: /// fn a() { println!(\"a\"); }\n  2544: /// fn b() { println!(\"b\"); }\n  2545: /// assert!(!ptr::fn_addr_eq(a as fn(), b as fn()));\n  2546: /// ```\n  2547: ///\n  2548: /// [subtype]: https://doc.rust-lang.org/reference/subtyping.html\n  2549: #[stable(feature = \"ptr_fn_addr_eq\", since = \"1.85.0\")]\n  2550: #[inline(always)]\n  2551: #[must_use = \"function pointer comparison produces a value\"]\n  2552: pub fn fn_addr_eq<T: FnPtr, U: FnPtr>(f: T, g: U) -> bool {\n  2553:     f.addr() == g.addr()\n  2554: }\n  2555: \n  2556: /// Hash a raw pointer.\n  2557: ///\n  2558: /// This can be used to hash a `&T` reference (which coerces to `*const T` implicitly)\n  2559: /// by its address rather than the value it points to\n  2560: /// (which is what the `Hash for &T` implementation does).\n  2561: ///\n  2562: /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::capacity",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 832,
            "path": "HashMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
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
                          "id": 834,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:870",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
    "verification_source": "   469:     }\n   470: \n   471:     /// Returns the number of elements the map can hold without reallocating.\n   472:     ///\n   473:     /// This number is a lower bound; the `HashMap<K, V>` might be able to hold\n   474:     /// more, but is guaranteed to be able to hold at least this many.\n   475:     ///\n   476:     /// # Examples\n   477:     ///\n   478:     /// ```\n   479:     /// use std::collections::HashMap;\n   480:     /// let map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   481:     /// assert!(map.capacity() >= 100);\n   482:     /// ```\n   483:     #[inline]\n   484:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   485:     pub fn capacity(&self) -> usize {\n   486:         self.base.capacity()\n   487:     }\n   488: \n   489:     /// An iterator visiting all keys in arbitrary order.\n   490:     /// The iterator element type is `&'a K`.\n   491:     ///\n   492:     /// # Examples\n   493:     ///\n   494:     /// ```\n   495:     /// use std::collections::HashMap;\n   496:     ///\n   497:     /// let map = HashMap::from([\n   498:     ///     (\"a\", 1),\n   499:     ///     (\"b\", 2),\n   500:     ///     (\"c\", 3),\n   501:     /// ]);",
    "nanvix_source": "   474:     ///\n   475:     /// # Examples\n   476:     ///\n   477:     /// ```\n   478:     /// use std::collections::HashMap;\n   479:     /// let map: HashMap<i32, i32> = HashMap::with_capacity(100);\n   480:     /// assert!(map.capacity() >= 100);\n   481:     /// ```\n   482:     #[inline]\n   483:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   484:     pub fn capacity(&self) -> usize {\n   485:         self.base.capacity()\n   486:     }\n   487: \n   488:     /// An iterator visiting all keys in arbitrary order.\n   489:     /// The iterator element type is `&'a K`.\n   490:     ///\n   491:     /// # Examples\n   492:     ///\n   493:     /// ```\n   494:     /// use std::collections::HashMap;",
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
