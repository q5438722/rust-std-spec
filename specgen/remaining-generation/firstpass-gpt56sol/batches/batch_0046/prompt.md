For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::option::Option::as_pin_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
      "name": "as_pin_mut",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "generic": "Self"
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
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "borrowed_ref": {
                                    "is_mutable": true,
                                    "lifetime": null,
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
    "verification_source": "   781:         // FIXME(const-hack): use `map` once that is possible\n   782:         match Pin::get_ref(self).as_ref() {\n   783:             // SAFETY: `x` is guaranteed to be pinned because it comes from `self`\n   784:             // which is pinned.\n   785:             Some(x) => unsafe { Some(Pin::new_unchecked(x)) },\n   786:             None => None,\n   787:         }\n   788:     }\n   789: \n   790:     /// Converts from <code>[Pin]<[&mut] Option\\<T>></code> to <code>Option<[Pin]<[&mut] T>></code>.\n   791:     ///\n   792:     /// [&mut]: reference \"mutable reference\"\n   793:     #[inline]\n   794:     #[must_use]\n   795:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   796:     #[rustc_const_stable(feature = \"const_option_ext\", since = \"1.84.0\")]\n   797:     pub const fn as_pin_mut(self: Pin<&mut Self>) -> Option<Pin<&mut T>> {\n   798:         // SAFETY: `get_unchecked_mut` is never used to move the `Option` inside `self`.\n   799:         // `x` is guaranteed to be pinned because it comes from `self` which is pinned.\n   800:         unsafe {\n   801:             // FIXME(const-hack): use `map` once that is possible\n   802:             match Pin::get_unchecked_mut(self).as_mut() {\n   803:                 Some(x) => Some(Pin::new_unchecked(x)),\n   804:                 None => None,\n   805:             }\n   806:         }\n   807:     }\n   808: \n   809:     #[inline]\n   810:     const fn len(&self) -> usize {\n   811:         // Using the intrinsic avoids emitting a branch to get the 0 or 1.\n   812:         let discriminant: isize = crate::intrinsics::discriminant_value(self);\n   813:         discriminant as usize",
    "nanvix_source": "   785:         }\n   786:     }\n   787: \n   788:     /// Converts from <code>[Pin]<[&mut] Option\\<T>></code> to <code>Option<[Pin]<[&mut] T>></code>.\n   789:     ///\n   790:     /// [&mut]: reference \"mutable reference\"\n   791:     #[inline]\n   792:     #[must_use]\n   793:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n   794:     #[rustc_const_stable(feature = \"const_option_ext\", since = \"1.84.0\")]\n   795:     pub const fn as_pin_mut(self: Pin<&mut Self>) -> Option<Pin<&mut T>> {\n   796:         // SAFETY: `get_unchecked_mut` is never used to move the `Option` inside `self`.\n   797:         // `x` is guaranteed to be pinned because it comes from `self` which is pinned.\n   798:         unsafe {\n   799:             // FIXME(const-hack): use `map` once that is possible\n   800:             match Pin::get_unchecked_mut(self).as_mut() {\n   801:                 Some(x) => Some(Pin::new_unchecked(x)),\n   802:                 None => None,\n   803:             }\n   804:         }\n   805:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::get_or_insert_default",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "get_or_insert_default",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1762:     ///\n  1763:     /// ```\n  1764:     /// let mut x = None;\n  1765:     ///\n  1766:     /// {\n  1767:     ///     let y: &mut u32 = x.get_or_insert_default();\n  1768:     ///     assert_eq!(y, &0);\n  1769:     ///\n  1770:     ///     *y = 7;\n  1771:     /// }\n  1772:     ///\n  1773:     /// assert_eq!(x, Some(7));\n  1774:     /// ```\n  1775:     #[inline]\n  1776:     #[stable(feature = \"option_get_or_insert_default\", since = \"1.83.0\")]\n  1777:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1778:     pub const fn get_or_insert_default(&mut self) -> &mut T\n  1779:     where\n  1780:         T: [const] Default,\n  1781:     {\n  1782:         self.get_or_insert_with(T::default)\n  1783:     }\n  1784: \n  1785:     /// Inserts a value computed from `f` into the option if it is [`None`],\n  1786:     /// then returns a mutable reference to the contained value.\n  1787:     ///\n  1788:     /// # Examples\n  1789:     ///\n  1790:     /// ```\n  1791:     /// let mut x = None;\n  1792:     ///\n  1793:     /// {\n  1794:     ///     let y: &mut u32 = x.get_or_insert_with(|| 5);",
    "nanvix_source": "  1768:     ///     assert_eq!(y, &0);\n  1769:     ///\n  1770:     ///     *y = 7;\n  1771:     /// }\n  1772:     ///\n  1773:     /// assert_eq!(x, Some(7));\n  1774:     /// ```\n  1775:     #[inline]\n  1776:     #[stable(feature = \"option_get_or_insert_default\", since = \"1.83.0\")]\n  1777:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1778:     pub const fn get_or_insert_default(&mut self) -> &mut T\n  1779:     where\n  1780:         T: [const] Default,\n  1781:     {\n  1782:         self.get_or_insert_with(T::default)\n  1783:     }\n  1784: \n  1785:     /// Inserts a value computed from `f` into the option if it is [`None`],\n  1786:     /// then returns a mutable reference to the contained value.\n  1787:     ///\n  1788:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::get_or_insert_with",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
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
                          "inputs": [],
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
      "name": "get_or_insert_with",
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
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1789:     ///\n  1790:     /// ```\n  1791:     /// let mut x = None;\n  1792:     ///\n  1793:     /// {\n  1794:     ///     let y: &mut u32 = x.get_or_insert_with(|| 5);\n  1795:     ///     assert_eq!(y, &5);\n  1796:     ///\n  1797:     ///     *y = 7;\n  1798:     /// }\n  1799:     ///\n  1800:     /// assert_eq!(x, Some(7));\n  1801:     /// ```\n  1802:     #[inline]\n  1803:     #[stable(feature = \"option_entry\", since = \"1.20.0\")]\n  1804:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1805:     pub const fn get_or_insert_with<F>(&mut self, f: F) -> &mut T\n  1806:     where\n  1807:         F: [const] FnOnce() -> T + [const] Destruct,\n  1808:     {\n  1809:         if let None = self {\n  1810:             // The effect of the following statement is identical to\n  1811:             //     *self = Some(f());\n  1812:             // except that it does not drop the old value of `*self`. This is not a leak, because\n  1813:             // we just checked that the old value is `None`, which contains no fields to drop.\n  1814:             // This implementation strategy\n  1815:             //\n  1816:             // * avoids needing a `T: [const] Destruct` bound, to the benefit of `const` callers,\n  1817:             // * and avoids possibly compiling needless drop code (as would sometimes happen in the\n  1818:             //   previous implementation), to the benefit of non-`const` callers.\n  1819:             //\n  1820:             // FIXME(const-hack): It would be nice if this weird trick were made obsolete\n  1821:             // (though that is likely to be hard/wontfix).",
    "nanvix_source": "  1795:     ///     assert_eq!(y, &5);\n  1796:     ///\n  1797:     ///     *y = 7;\n  1798:     /// }\n  1799:     ///\n  1800:     /// assert_eq!(x, Some(7));\n  1801:     /// ```\n  1802:     #[inline]\n  1803:     #[stable(feature = \"option_entry\", since = \"1.20.0\")]\n  1804:     #[rustc_const_unstable(feature = \"const_option_ops\", issue = \"143956\")]\n  1805:     pub const fn get_or_insert_with<F>(&mut self, f: F) -> &mut T\n  1806:     where\n  1807:         F: [const] FnOnce() -> T + [const] Destruct,\n  1808:     {\n  1809:         if let None = self {\n  1810:             // The effect of the following statement is identical to\n  1811:             //     *self = Some(f());\n  1812:             // except that it does not drop the old value of `*self`. This is not a leak, because\n  1813:             // we just checked that the old value is `None`, which contains no fields to drop.\n  1814:             // This implementation strategy\n  1815:             //",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::as_deref_mut",
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
                      "id": 8650,
                      "path": "DerefMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Ptr"
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
      "name": "as_deref_mut",
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
                      "generic": "Ptr"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 8650,
                          "path": "DerefMut"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29038",
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
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "generic": "Self"
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
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "Ptr"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
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
    "verification_source": "  1412:     {\n  1413:         // SAFETY: see documentation on this function\n  1414:         unsafe { Pin::new_unchecked(&mut *self.pointer) }\n  1415:     }\n  1416: \n  1417:     /// Gets `Pin<&mut T>` to the underlying pinned value from this nested `Pin`-pointer.\n  1418:     ///\n  1419:     /// This is a generic method to go from `Pin<&mut Pin<Pointer<T>>>` to `Pin<&mut T>`. It is\n  1420:     /// safe because the existence of a `Pin<Pointer<T>>` ensures that the pointee, `T`, cannot\n  1421:     /// move in the future, and this method does not enable the pointee to move. \"Malicious\"\n  1422:     /// implementations of `Ptr::DerefMut` are likewise ruled out by the contract of\n  1423:     /// `Pin::new_unchecked`.\n  1424:     #[stable(feature = \"pin_deref_mut\", since = \"1.84.0\")]\n  1425:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1426:     #[inline(always)]\n  1427:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1428:     pub const fn as_deref_mut(self: Pin<&mut Self>) -> Pin<&mut Ptr::Target>\n  1429:     where\n  1430:         Ptr: [const] DerefMut,\n  1431:     {\n  1432:         // SAFETY: What we're asserting here is that going from\n  1433:         //\n  1434:         //     Pin<&mut Pin<Ptr>>\n  1435:         //\n  1436:         // to\n  1437:         //\n  1438:         //     Pin<&mut Ptr::Target>\n  1439:         //\n  1440:         // is safe.\n  1441:         //\n  1442:         // We need to ensure that two things hold for that to be the case:\n  1443:         //\n  1444:         // 1) Once we give out a `Pin<&mut Ptr::Target>`, a `&mut Ptr::Target` will not be given out.",
    "nanvix_source": "  1418:     ///\n  1419:     /// This is a generic method to go from `Pin<&mut Pin<Pointer<T>>>` to `Pin<&mut T>`. It is\n  1420:     /// safe because the existence of a `Pin<Pointer<T>>` ensures that the pointee, `T`, cannot\n  1421:     /// move in the future, and this method does not enable the pointee to move. \"Malicious\"\n  1422:     /// implementations of `Ptr::DerefMut` are likewise ruled out by the contract of\n  1423:     /// `Pin::new_unchecked`.\n  1424:     #[stable(feature = \"pin_deref_mut\", since = \"1.84.0\")]\n  1425:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1426:     #[inline(always)]\n  1427:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1428:     pub const fn as_deref_mut(self: Pin<&mut Self>) -> Pin<&mut Ptr::Target>\n  1429:     where\n  1430:         Ptr: [const] DerefMut,\n  1431:     {\n  1432:         // SAFETY: What we're asserting here is that going from\n  1433:         //\n  1434:         //     Pin<&mut Pin<Ptr>>\n  1435:         //\n  1436:         // to\n  1437:         //\n  1438:         //     Pin<&mut Ptr::Target>",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::as_mut",
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
                      "id": 8650,
                      "path": "DerefMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Ptr"
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
                      "generic": "Ptr"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 8650,
                          "path": "DerefMut"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29038",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "Ptr"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
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
    "verification_source": "  1393:     /// # struct Type {}\n  1394:     /// impl Type {\n  1395:     ///     fn method(self: Pin<&mut Self>) {\n  1396:     ///         // do something\n  1397:     ///     }\n  1398:     ///\n  1399:     ///     fn call_method_twice(mut self: Pin<&mut Self>) {\n  1400:     ///         // `method` consumes `self`, so reborrow the `Pin<&mut Self>` via `as_mut`.\n  1401:     ///         self.as_mut().method();\n  1402:     ///         self.as_mut().method();\n  1403:     ///     }\n  1404:     /// }\n  1405:     /// ```\n  1406:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1407:     #[inline(always)]\n  1408:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1409:     pub const fn as_mut(&mut self) -> Pin<&mut Ptr::Target>\n  1410:     where\n  1411:         Ptr: [const] DerefMut,\n  1412:     {\n  1413:         // SAFETY: see documentation on this function\n  1414:         unsafe { Pin::new_unchecked(&mut *self.pointer) }\n  1415:     }\n  1416: \n  1417:     /// Gets `Pin<&mut T>` to the underlying pinned value from this nested `Pin`-pointer.\n  1418:     ///\n  1419:     /// This is a generic method to go from `Pin<&mut Pin<Pointer<T>>>` to `Pin<&mut T>`. It is\n  1420:     /// safe because the existence of a `Pin<Pointer<T>>` ensures that the pointee, `T`, cannot\n  1421:     /// move in the future, and this method does not enable the pointee to move. \"Malicious\"\n  1422:     /// implementations of `Ptr::DerefMut` are likewise ruled out by the contract of\n  1423:     /// `Pin::new_unchecked`.\n  1424:     #[stable(feature = \"pin_deref_mut\", since = \"1.84.0\")]\n  1425:     #[must_use = \"`self` will be dropped if the result is not used\"]",
    "nanvix_source": "  1399:     ///     fn call_method_twice(mut self: Pin<&mut Self>) {\n  1400:     ///         // `method` consumes `self`, so reborrow the `Pin<&mut Self>` via `as_mut`.\n  1401:     ///         self.as_mut().method();\n  1402:     ///         self.as_mut().method();\n  1403:     ///     }\n  1404:     /// }\n  1405:     /// ```\n  1406:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1407:     #[inline(always)]\n  1408:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1409:     pub const fn as_mut(&mut self) -> Pin<&mut Ptr::Target>\n  1410:     where\n  1411:         Ptr: [const] DerefMut,\n  1412:     {\n  1413:         // SAFETY: see documentation on this function\n  1414:         unsafe { Pin::new_unchecked(&mut *self.pointer) }\n  1415:     }\n  1416: \n  1417:     /// Gets `Pin<&mut T>` to the underlying pinned value from this nested `Pin`-pointer.\n  1418:     ///\n  1419:     /// This is a generic method to go from `Pin<&mut Pin<Pointer<T>>>` to `Pin<&mut T>`. It is",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::get_mut",
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
                      "id": 16,
                      "path": "Unpin"
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
      "name": "get_mut",
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
    "verification_source": "  1580:         Pin { pointer: self.pointer }\n  1581:     }\n  1582: \n  1583:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1584:     ///\n  1585:     /// This requires that the data inside this `Pin` is `Unpin`.\n  1586:     ///\n  1587:     /// Note: `Pin` also implements `DerefMut` to the data, which can be used\n  1588:     /// to access the inner value. However, `DerefMut` only provides a reference\n  1589:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of\n  1590:     /// the `Pin` itself. This method allows turning the `Pin` into a reference\n  1591:     /// with the same lifetime as the original `Pin`.\n  1592:     #[inline(always)]\n  1593:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1594:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1595:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1596:     pub const fn get_mut(self) -> &'a mut T\n  1597:     where\n  1598:         T: Unpin,\n  1599:     {\n  1600:         self.pointer\n  1601:     }\n  1602: \n  1603:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1604:     ///\n  1605:     /// # Safety\n  1606:     ///\n  1607:     /// This function is unsafe. You must guarantee that you will never move\n  1608:     /// the data out of the mutable reference you receive when you call this\n  1609:     /// function, so that the invariants on the `Pin` type can be upheld.\n  1610:     ///\n  1611:     /// If the underlying data is `Unpin`, `Pin::get_mut` should be used\n  1612:     /// instead.",
    "nanvix_source": "  1586:     ///\n  1587:     /// Note: `Pin` also implements `DerefMut` to the data, which can be used\n  1588:     /// to access the inner value. However, `DerefMut` only provides a reference\n  1589:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of\n  1590:     /// the `Pin` itself. This method allows turning the `Pin` into a reference\n  1591:     /// with the same lifetime as the original `Pin`.\n  1592:     #[inline(always)]\n  1593:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1594:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1595:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1596:     pub const fn get_mut(self) -> &'a mut T\n  1597:     where\n  1598:         T: Unpin,\n  1599:     {\n  1600:         self.pointer\n  1601:     }\n  1602: \n  1603:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1604:     ///\n  1605:     /// # Safety\n  1606:     ///",
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
