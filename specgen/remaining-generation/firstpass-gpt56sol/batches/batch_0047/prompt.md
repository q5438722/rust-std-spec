For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::pin::Pin::get_unchecked_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_unsafe": true
      },
      "name": "get_unchecked_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                        "is_mutable": true,
                        "lifetime": "'a",
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
            "id": 9981,
            "path": "Pin"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:29048",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1601:     }\n  1602: \n  1603:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1604:     ///\n  1605:     /// # Safety\n  1606:     ///\n  1607:     /// This function is unsafe. You must guarantee that you will never move\n  1608:     /// the data out of the mutable reference you receive when you call this\n  1609:     /// function, so that the invariants on the `Pin` type can be upheld.\n  1610:     ///\n  1611:     /// If the underlying data is `Unpin`, `Pin::get_mut` should be used\n  1612:     /// instead.\n  1613:     #[inline(always)]\n  1614:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1615:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1616:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1617:     pub const unsafe fn get_unchecked_mut(self) -> &'a mut T {\n  1618:         self.pointer\n  1619:     }\n  1620: \n  1621:     /// Constructs a new pin by mapping the interior value.\n  1622:     ///\n  1623:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1624:     /// you could use this to get access to that field in one line of code.\n  1625:     /// However, there are several gotchas with these \"pinning projections\";\n  1626:     /// see the [`pin` module] documentation for further details on that topic.\n  1627:     ///\n  1628:     /// # Safety\n  1629:     ///\n  1630:     /// This function is unsafe. You must guarantee that the data you return\n  1631:     /// will not move so long as the argument value does not move (for example,\n  1632:     /// because it is one of the fields of that value), and also that you do\n  1633:     /// not move out of the argument you receive to the interior function.",
    "nanvix_source": "  1607:     /// This function is unsafe. You must guarantee that you will never move\n  1608:     /// the data out of the mutable reference you receive when you call this\n  1609:     /// function, so that the invariants on the `Pin` type can be upheld.\n  1610:     ///\n  1611:     /// If the underlying data is `Unpin`, `Pin::get_mut` should be used\n  1612:     /// instead.\n  1613:     #[inline(always)]\n  1614:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1615:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1616:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1617:     pub const unsafe fn get_unchecked_mut(self) -> &'a mut T {\n  1618:         self.pointer\n  1619:     }\n  1620: \n  1621:     /// Constructs a new pin by mapping the interior value.\n  1622:     ///\n  1623:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1624:     /// you could use this to get access to that field in one line of code.\n  1625:     /// However, there are several gotchas with these \"pinning projections\";\n  1626:     /// see the [`pin` module] documentation for further details on that topic.\n  1627:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::map_unchecked_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "U"
          },
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
                    "modifier": "maybe",
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
                "generic": "U"
              }
            }
          },
          {
            "bound_predicate": {
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
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "borrowed_ref": {
                              "is_mutable": true,
                              "lifetime": null,
                              "type": {
                                "generic": "U"
                              }
                            }
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
        "is_const": false,
        "is_unsafe": true
      },
      "name": "map_unchecked_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                        "is_mutable": true,
                        "lifetime": "'a",
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
            "id": 9981,
            "path": "Pin"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            },
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:29048",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
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
            "func",
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
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": "'a",
                        "type": {
                          "generic": "U"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9981,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "  1622:     ///\n  1623:     /// For example, if you wanted to get a `Pin` of a field of something,\n  1624:     /// you could use this to get access to that field in one line of code.\n  1625:     /// However, there are several gotchas with these \"pinning projections\";\n  1626:     /// see the [`pin` module] documentation for further details on that topic.\n  1627:     ///\n  1628:     /// # Safety\n  1629:     ///\n  1630:     /// This function is unsafe. You must guarantee that the data you return\n  1631:     /// will not move so long as the argument value does not move (for example,\n  1632:     /// because it is one of the fields of that value), and also that you do\n  1633:     /// not move out of the argument you receive to the interior function.\n  1634:     ///\n  1635:     /// [`pin` module]: self#projections-and-structural-pinning\n  1636:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1637:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1638:     pub unsafe fn map_unchecked_mut<U, F>(self, func: F) -> Pin<&'a mut U>\n  1639:     where\n  1640:         U: ?Sized,\n  1641:         F: FnOnce(&mut T) -> &mut U,\n  1642:     {\n  1643:         // SAFETY: the caller is responsible for not moving the\n  1644:         // value out of this reference.\n  1645:         let pointer = unsafe { Pin::get_unchecked_mut(self) };\n  1646:         let new_pointer = func(pointer);\n  1647:         // SAFETY: as the value of `this` is guaranteed to not have\n  1648:         // been moved out, this call to `new_unchecked` is safe.\n  1649:         unsafe { Pin::new_unchecked(new_pointer) }\n  1650:     }\n  1651: }\n  1652: \n  1653: impl<T: ?Sized> Pin<&'static T> {\n  1654:     /// Gets a pinning reference from a `&'static` reference.",
    "nanvix_source": "  1628:     /// # Safety\n  1629:     ///\n  1630:     /// This function is unsafe. You must guarantee that the data you return\n  1631:     /// will not move so long as the argument value does not move (for example,\n  1632:     /// because it is one of the fields of that value), and also that you do\n  1633:     /// not move out of the argument you receive to the interior function.\n  1634:     ///\n  1635:     /// [`pin` module]: self#projections-and-structural-pinning\n  1636:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1637:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1638:     pub unsafe fn map_unchecked_mut<U, F>(self, func: F) -> Pin<&'a mut U>\n  1639:     where\n  1640:         U: ?Sized,\n  1641:         F: FnOnce(&mut T) -> &mut U,\n  1642:     {\n  1643:         // SAFETY: the caller is responsible for not moving the\n  1644:         // value out of this reference.\n  1645:         let pointer = unsafe { Pin::get_unchecked_mut(self) };\n  1646:         let new_pointer = func(pointer);\n  1647:         // SAFETY: as the value of `this` is guaranteed to not have\n  1648:         // been moved out, this call to `new_unchecked` is safe.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::static_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
      "name": "static_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "r"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                        "is_mutable": true,
                        "lifetime": "'static",
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
            "id": 9981,
            "path": "Pin"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
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
        "impl_id": "core:29052",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "r",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": "'static",
                "type": {
                  "generic": "T"
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
                        "is_mutable": true,
                        "lifetime": "'static",
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
            "id": 9981,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "  1658:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1659:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1660:     pub const fn static_ref(r: &'static T) -> Pin<&'static T> {\n  1661:         // SAFETY: The 'static borrow guarantees the data will not be\n  1662:         // moved/invalidated until it gets dropped (which is never).\n  1663:         unsafe { Pin::new_unchecked(r) }\n  1664:     }\n  1665: }\n  1666: \n  1667: impl<T: ?Sized> Pin<&'static mut T> {\n  1668:     /// Gets a pinning mutable reference from a static mutable reference.\n  1669:     ///\n  1670:     /// This is safe because `T` is borrowed for the `'static` lifetime, which\n  1671:     /// never ends.\n  1672:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1673:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1674:     pub const fn static_mut(r: &'static mut T) -> Pin<&'static mut T> {\n  1675:         // SAFETY: The 'static borrow guarantees the data will not be\n  1676:         // moved/invalidated until it gets dropped (which is never).\n  1677:         unsafe { Pin::new_unchecked(r) }\n  1678:     }\n  1679: }\n  1680: \n  1681: #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1682: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1683: impl<Ptr: [const] Deref> const Deref for Pin<Ptr> {\n  1684:     type Target = Ptr::Target;\n  1685:     fn deref(&self) -> &Ptr::Target {\n  1686:         Pin::get_ref(Pin::as_ref(self))\n  1687:     }\n  1688: }\n  1689: \n  1690: mod helper {",
    "nanvix_source": "  1664:     }\n  1665: }\n  1666: \n  1667: impl<T: ?Sized> Pin<&'static mut T> {\n  1668:     /// Gets a pinning mutable reference from a static mutable reference.\n  1669:     ///\n  1670:     /// This is safe because `T` is borrowed for the `'static` lifetime, which\n  1671:     /// never ends.\n  1672:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1673:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1674:     pub const fn static_mut(r: &'static mut T) -> Pin<&'static mut T> {\n  1675:         // SAFETY: The 'static borrow guarantees the data will not be\n  1676:         // moved/invalidated until it gets dropped (which is never).\n  1677:         unsafe { Pin::new_unchecked(r) }\n  1678:     }\n  1679: }\n  1680: \n  1681: #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1682: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1683: const impl<Ptr: [const] Deref> Deref for Pin<Ptr> {\n  1684:     type Target = Ptr::Target;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::as_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "as_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
            "id": 9475,
            "path": "NonNull"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   462:     /// use std::ptr::NonNull;\n   463:     ///\n   464:     /// let mut x = 0u32;\n   465:     /// let mut ptr = NonNull::new(&mut x).expect(\"null pointer\");\n   466:     ///\n   467:     /// let x_ref = unsafe { ptr.as_mut() };\n   468:     /// assert_eq!(*x_ref, 0);\n   469:     /// *x_ref += 2;\n   470:     /// assert_eq!(*x_ref, 2);\n   471:     /// ```\n   472:     ///\n   473:     /// [the module documentation]: crate::ptr#safety\n   474:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   475:     #[rustc_const_stable(feature = \"const_ptr_as_ref\", since = \"1.83.0\")]\n   476:     #[must_use]\n   477:     #[inline(always)]\n   478:     pub const unsafe fn as_mut<'a>(&mut self) -> &'a mut T {\n   479:         // SAFETY: the caller must guarantee that `self` meets all the\n   480:         // requirements for a mutable reference.\n   481:         unsafe { &mut *self.as_ptr() }\n   482:     }\n   483: \n   484:     /// Casts to a pointer of another type.\n   485:     ///\n   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::ptr::NonNull;\n   490:     ///\n   491:     /// let mut x = 0u32;\n   492:     /// let ptr = NonNull::new(&mut x as *mut _).expect(\"null pointer\");\n   493:     ///\n   494:     /// let casted_ptr = ptr.cast::<i8>();",
    "nanvix_source": "   465:     /// assert_eq!(*x_ref, 0);\n   466:     /// *x_ref += 2;\n   467:     /// assert_eq!(*x_ref, 2);\n   468:     /// ```\n   469:     ///\n   470:     /// [the module documentation]: crate::ptr#safety\n   471:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   472:     #[rustc_const_stable(feature = \"const_ptr_as_ref\", since = \"1.83.0\")]\n   473:     #[must_use]\n   474:     #[inline(always)]\n   475:     pub const unsafe fn as_mut<'a>(&mut self) -> &'a mut T {\n   476:         // SAFETY: the caller must guarantee that `self` meets all the\n   477:         // requirements for a mutable reference.\n   478:         unsafe { &mut *self.as_ptr() }\n   479:     }\n   480: \n   481:     /// Casts to a pointer of another type.\n   482:     ///\n   483:     /// # Examples\n   484:     ///\n   485:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::as_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "as_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
                        "is_mutable": true,
                        "lifetime": "'a",
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
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   567:     /// # Null-unchecked version\n   568:     ///\n   569:     /// If you are sure the pointer can never be null, you can use `as_mut_unchecked` which returns\n   570:     /// `&mut T` instead of `Option<&mut T>`.\n   571:     ///\n   572:     /// ```\n   573:     /// let mut s = [1, 2, 3];\n   574:     /// let ptr: *mut u32 = s.as_mut_ptr();\n   575:     /// let first_value = unsafe { ptr.as_mut_unchecked() };\n   576:     /// *first_value = 4;\n   577:     /// # assert_eq!(s, [4, 2, 3]);\n   578:     /// println!(\"{s:?}\"); // It'll print: \"[4, 2, 3]\".\n   579:     /// ```\n   580:     #[stable(feature = \"ptr_as_ref\", since = \"1.9.0\")]\n   581:     #[rustc_const_stable(feature = \"const_ptr_is_null\", since = \"1.84.0\")]\n   582:     #[inline]\n   583:     pub const unsafe fn as_mut<'a>(self) -> Option<&'a mut T> {\n   584:         // SAFETY: the caller must guarantee that `self` is be valid for\n   585:         // a mutable reference if it isn't null.\n   586:         if self.is_null() { None } else { unsafe { Some(&mut *self) } }\n   587:     }\n   588: \n   589:     /// Returns a unique reference to the value behind the pointer.\n   590:     /// If the pointer may be null or the value may be uninitialized, [`as_uninit_mut`] must be used instead.\n   591:     /// If the pointer may be null, but the value is known to have been initialized, [`as_mut`] must be used instead.\n   592:     ///\n   593:     /// For the shared counterpart see [`as_ref_unchecked`].\n   594:     ///\n   595:     /// [`as_mut`]: #method.as_mut\n   596:     /// [`as_uninit_mut`]: #method.as_uninit_mut\n   597:     /// [`as_ref_unchecked`]: #method.as_mut_unchecked\n   598:     ///\n   599:     /// # Safety",
    "nanvix_source": "   578:     /// let mut s = [1, 2, 3];\n   579:     /// let ptr: *mut u32 = s.as_mut_ptr();\n   580:     /// let first_value = unsafe { ptr.as_mut_unchecked() };\n   581:     /// *first_value = 4;\n   582:     /// # assert_eq!(s, [4, 2, 3]);\n   583:     /// println!(\"{s:?}\"); // It'll print: \"[4, 2, 3]\".\n   584:     /// ```\n   585:     #[stable(feature = \"ptr_as_ref\", since = \"1.9.0\")]\n   586:     #[rustc_const_stable(feature = \"const_ptr_is_null\", since = \"1.84.0\")]\n   587:     #[inline]\n   588:     pub const unsafe fn as_mut<'a>(self) -> Option<&'a mut T> {\n   589:         // SAFETY: the caller must guarantee that `self` is be valid for\n   590:         // a mutable reference if it isn't null.\n   591:         if self.is_null() { None } else { unsafe { Some(&mut *self) } }\n   592:     }\n   593: \n   594:     /// Returns a unique reference to the value behind the pointer.\n   595:     /// If the pointer may be null or the value may be uninitialized, [`as_uninit_mut`] must be used instead.\n   596:     /// If the pointer may be null, but the value is known to have been initialized, [`as_mut`] must be used instead.\n   597:     ///\n   598:     /// For the shared counterpart see [`as_ref_unchecked`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::as_mut_unchecked",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "as_mut_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   602:     /// the pointer is [convertible to a reference](crate::ptr#pointer-to-reference-conversion).\n   603:     ///\n   604:     /// # Examples\n   605:     ///\n   606:     /// ```\n   607:     /// let mut s = [1, 2, 3];\n   608:     /// let ptr: *mut u32 = s.as_mut_ptr();\n   609:     /// let first_value = unsafe { ptr.as_mut_unchecked() };\n   610:     /// *first_value = 4;\n   611:     /// # assert_eq!(s, [4, 2, 3]);\n   612:     /// println!(\"{s:?}\"); // It'll print: \"[4, 2, 3]\".\n   613:     /// ```\n   614:     #[stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   615:     #[rustc_const_stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   616:     #[inline]\n   617:     #[must_use]\n   618:     pub const unsafe fn as_mut_unchecked<'a>(self) -> &'a mut T {\n   619:         // SAFETY: the caller must guarantee that `self` is valid for a reference\n   620:         unsafe { &mut *self }\n   621:     }\n   622: \n   623:     /// Returns `None` if the pointer is null, or else returns a unique reference to\n   624:     /// the value wrapped in `Some`. In contrast to [`as_mut`], this does not require\n   625:     /// that the value has to be initialized.\n   626:     ///\n   627:     /// For the shared counterpart see [`as_uninit_ref`].\n   628:     ///\n   629:     /// [`as_mut`]: #method.as_mut\n   630:     /// [`as_uninit_ref`]: pointer#method.as_uninit_ref-1\n   631:     ///\n   632:     /// # Safety\n   633:     ///\n   634:     /// When calling this method, you have to ensure that *either* the pointer is null *or*",
    "nanvix_source": "   613:     /// let ptr: *mut u32 = s.as_mut_ptr();\n   614:     /// let first_value = unsafe { ptr.as_mut_unchecked() };\n   615:     /// *first_value = 4;\n   616:     /// # assert_eq!(s, [4, 2, 3]);\n   617:     /// println!(\"{s:?}\"); // It'll print: \"[4, 2, 3]\".\n   618:     /// ```\n   619:     #[stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   620:     #[rustc_const_stable(feature = \"ptr_as_ref_unchecked\", since = \"1.95.0\")]\n   621:     #[inline]\n   622:     #[must_use]\n   623:     pub const unsafe fn as_mut_unchecked<'a>(self) -> &'a mut T {\n   624:         // SAFETY: the caller must guarantee that `self` is valid for a reference\n   625:         unsafe { &mut *self }\n   626:     }\n   627: \n   628:     /// Returns `None` if the pointer is null, or else returns a unique reference to\n   629:     /// the value wrapped in `Some`. In contrast to [`as_mut`], this does not require\n   630:     /// that the value has to be initialized.\n   631:     ///\n   632:     /// For the shared counterpart see [`as_uninit_ref`].\n   633:     ///",
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
