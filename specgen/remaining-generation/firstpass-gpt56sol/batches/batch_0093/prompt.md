For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::iter_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "iter_mut",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "id": 11725,
            "path": "IterMut"
          }
        }
      }
    },
    "verification_source": "  1044:     /// Returns an iterator that allows modifying each value.\n  1045:     ///\n  1046:     /// The iterator yields all items from start to end.\n  1047:     ///\n  1048:     /// # Examples\n  1049:     ///\n  1050:     /// ```\n  1051:     /// let x = &mut [1, 2, 4];\n  1052:     /// for elem in x.iter_mut() {\n  1053:     ///     *elem += 2;\n  1054:     /// }\n  1055:     /// assert_eq!(x, &[3, 4, 6]);\n  1056:     /// ```\n  1057:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1058:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1059:     #[inline]\n  1060:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1061:         IterMut::new(self)\n  1062:     }\n  1063: \n  1064:     /// Returns an iterator over all contiguous windows of length\n  1065:     /// `size`. The windows overlap. If the slice is shorter than\n  1066:     /// `size`, the iterator returns no values.\n  1067:     ///\n  1068:     /// # Panics\n  1069:     ///\n  1070:     /// Panics if `size` is zero.\n  1071:     ///\n  1072:     /// # Examples\n  1073:     ///\n  1074:     /// ```\n  1075:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1076:     /// let mut iter = slice.windows(3);",
    "nanvix_source": "  1053:     /// ```\n  1054:     /// let x = &mut [1, 2, 4];\n  1055:     /// for elem in x.iter_mut() {\n  1056:     ///     *elem += 2;\n  1057:     /// }\n  1058:     /// assert_eq!(x, &[3, 4, 6]);\n  1059:     /// ```\n  1060:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1061:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1062:     #[inline]\n  1063:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1064:         IterMut::new(self)\n  1065:     }\n  1066: \n  1067:     /// Returns an iterator over all contiguous windows of length\n  1068:     /// `size`. The windows overlap. If the slice is shorter than\n  1069:     /// `size`, the iterator returns no values.\n  1070:     ///\n  1071:     /// # Panics\n  1072:     ///\n  1073:     /// Panics if `size` is zero.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rchunks",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "rchunks",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "chunk_size",
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
            "id": 10072,
            "path": "RChunks"
          }
        }
      }
    },
    "verification_source": "  1670:     /// ```\n  1671:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1672:     /// let mut iter = slice.rchunks(2);\n  1673:     /// assert_eq!(iter.next().unwrap(), &['e', 'm']);\n  1674:     /// assert_eq!(iter.next().unwrap(), &['o', 'r']);\n  1675:     /// assert_eq!(iter.next().unwrap(), &['l']);\n  1676:     /// assert!(iter.next().is_none());\n  1677:     /// ```\n  1678:     ///\n  1679:     /// [`rchunks_exact`]: slice::rchunks_exact\n  1680:     /// [`chunks`]: slice::chunks\n  1681:     /// [`as_rchunks`]: slice::as_rchunks\n  1682:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1683:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1684:     #[inline]\n  1685:     #[track_caller]\n  1686:     pub const fn rchunks(&self, chunk_size: usize) -> RChunks<'_, T> {\n  1687:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1688:         RChunks::new(self, chunk_size)\n  1689:     }\n  1690: \n  1691:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1692:     /// of the slice.\n  1693:     ///\n  1694:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1695:     /// length of the slice, then the last chunk will not have length `chunk_size`.\n  1696:     ///\n  1697:     /// See [`rchunks_exact_mut`] for a variant of this iterator that returns chunks of always\n  1698:     /// exactly `chunk_size` elements, and [`chunks_mut`] for the same iterator but starting at the\n  1699:     /// beginning of the slice.\n  1700:     ///\n  1701:     /// If your `chunk_size` is a constant, consider using [`as_rchunks_mut`] instead, which will\n  1702:     /// give references to arrays of exactly that length, rather than slices.",
    "nanvix_source": "  1679:     /// assert!(iter.next().is_none());\n  1680:     /// ```\n  1681:     ///\n  1682:     /// [`rchunks_exact`]: slice::rchunks_exact\n  1683:     /// [`chunks`]: slice::chunks\n  1684:     /// [`as_rchunks`]: slice::as_rchunks\n  1685:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1686:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1687:     #[inline]\n  1688:     #[track_caller]\n  1689:     pub const fn rchunks(&self, chunk_size: usize) -> RChunks<'_, T> {\n  1690:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1691:         RChunks::new(self, chunk_size)\n  1692:     }\n  1693: \n  1694:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1695:     /// of the slice.\n  1696:     ///\n  1697:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1698:     /// length of the slice, then the last chunk will not have length `chunk_size`.\n  1699:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rchunks_exact",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "rchunks_exact",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "chunk_size",
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
            "id": 10074,
            "path": "RChunksExact"
          }
        }
      }
    },
    "verification_source": "  1759:     /// let slice = ['l', 'o', 'r', 'e', 'm'];\n  1760:     /// let mut iter = slice.rchunks_exact(2);\n  1761:     /// assert_eq!(iter.next().unwrap(), &['e', 'm']);\n  1762:     /// assert_eq!(iter.next().unwrap(), &['o', 'r']);\n  1763:     /// assert!(iter.next().is_none());\n  1764:     /// assert_eq!(iter.remainder(), &['l']);\n  1765:     /// ```\n  1766:     ///\n  1767:     /// [`chunks`]: slice::chunks\n  1768:     /// [`rchunks`]: slice::rchunks\n  1769:     /// [`chunks_exact`]: slice::chunks_exact\n  1770:     /// [`as_rchunks`]: slice::as_rchunks\n  1771:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1772:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1773:     #[inline]\n  1774:     #[track_caller]\n  1775:     pub const fn rchunks_exact(&self, chunk_size: usize) -> RChunksExact<'_, T> {\n  1776:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1777:         RChunksExact::new(self, chunk_size)\n  1778:     }\n  1779: \n  1780:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1781:     /// of the slice.\n  1782:     ///\n  1783:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1784:     /// length of the slice, then the last up to `chunk_size-1` elements will be omitted and can be\n  1785:     /// retrieved from the `into_remainder` function of the iterator.\n  1786:     ///\n  1787:     /// Due to each chunk having exactly `chunk_size` elements, the compiler can often optimize the\n  1788:     /// resulting code better than in the case of [`chunks_mut`].\n  1789:     ///\n  1790:     /// See [`rchunks_mut`] for a variant of this iterator that also returns the remainder as a\n  1791:     /// smaller chunk, and [`chunks_exact_mut`] for the same iterator but starting at the beginning",
    "nanvix_source": "  1768:     /// ```\n  1769:     ///\n  1770:     /// [`chunks`]: slice::chunks\n  1771:     /// [`rchunks`]: slice::rchunks\n  1772:     /// [`chunks_exact`]: slice::chunks_exact\n  1773:     /// [`as_rchunks`]: slice::as_rchunks\n  1774:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1775:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1776:     #[inline]\n  1777:     #[track_caller]\n  1778:     pub const fn rchunks_exact(&self, chunk_size: usize) -> RChunksExact<'_, T> {\n  1779:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1780:         RChunksExact::new(self, chunk_size)\n  1781:     }\n  1782: \n  1783:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the end\n  1784:     /// of the slice.\n  1785:     ///\n  1786:     /// The chunks are mutable slices, and do not overlap. If `chunk_size` does not divide the\n  1787:     /// length of the slice, then the last up to `chunk_size-1` elements will be omitted and can be\n  1788:     /// retrieved from the `into_remainder` function of the iterator.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rchunks_exact_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "rchunks_exact_mut",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "chunk_size",
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
            "id": 13740,
            "path": "RChunksExactMut"
          }
        }
      }
    },
    "verification_source": "  1808:     ///     for elem in chunk.iter_mut() {\n  1809:     ///         *elem += count;\n  1810:     ///     }\n  1811:     ///     count += 1;\n  1812:     /// }\n  1813:     /// assert_eq!(v, &[0, 2, 2, 1, 1]);\n  1814:     /// ```\n  1815:     ///\n  1816:     /// [`chunks_mut`]: slice::chunks_mut\n  1817:     /// [`rchunks_mut`]: slice::rchunks_mut\n  1818:     /// [`chunks_exact_mut`]: slice::chunks_exact_mut\n  1819:     /// [`as_rchunks_mut`]: slice::as_rchunks_mut\n  1820:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1821:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1822:     #[inline]\n  1823:     #[track_caller]\n  1824:     pub const fn rchunks_exact_mut(&mut self, chunk_size: usize) -> RChunksExactMut<'_, T> {\n  1825:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1826:         RChunksExactMut::new(self, chunk_size)\n  1827:     }\n  1828: \n  1829:     /// Returns an iterator over the slice producing non-overlapping runs\n  1830:     /// of elements using the predicate to separate them.\n  1831:     ///\n  1832:     /// The predicate is called for every pair of consecutive elements,\n  1833:     /// meaning that it is called on `slice[0]` and `slice[1]`,\n  1834:     /// followed by `slice[1]` and `slice[2]`, and so on.\n  1835:     ///\n  1836:     /// # Examples\n  1837:     ///\n  1838:     /// ```\n  1839:     /// let slice = &[1, 1, 1, 3, 3, 2, 2, 2];\n  1840:     ///",
    "nanvix_source": "  1817:     /// ```\n  1818:     ///\n  1819:     /// [`chunks_mut`]: slice::chunks_mut\n  1820:     /// [`rchunks_mut`]: slice::rchunks_mut\n  1821:     /// [`chunks_exact_mut`]: slice::chunks_exact_mut\n  1822:     /// [`as_rchunks_mut`]: slice::as_rchunks_mut\n  1823:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1824:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1825:     #[inline]\n  1826:     #[track_caller]\n  1827:     pub const fn rchunks_exact_mut(&mut self, chunk_size: usize) -> RChunksExactMut<'_, T> {\n  1828:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1829:         RChunksExactMut::new(self, chunk_size)\n  1830:     }\n  1831: \n  1832:     /// Returns an iterator over the slice producing non-overlapping runs\n  1833:     /// of elements using the predicate to separate them.\n  1834:     ///\n  1835:     /// The predicate is called for every pair of consecutive elements,\n  1836:     /// meaning that it is called on `slice[0]` and `slice[1]`,\n  1837:     /// followed by `slice[1]` and `slice[2]`, and so on.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::rchunks_mut",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "rchunks_mut",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "chunk_size",
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
            "id": 13738,
            "path": "RChunksMut"
          }
        }
      }
    },
    "verification_source": "  1714:     /// for chunk in v.rchunks_mut(2) {\n  1715:     ///     for elem in chunk.iter_mut() {\n  1716:     ///         *elem += count;\n  1717:     ///     }\n  1718:     ///     count += 1;\n  1719:     /// }\n  1720:     /// assert_eq!(v, &[3, 2, 2, 1, 1]);\n  1721:     /// ```\n  1722:     ///\n  1723:     /// [`rchunks_exact_mut`]: slice::rchunks_exact_mut\n  1724:     /// [`chunks_mut`]: slice::chunks_mut\n  1725:     /// [`as_rchunks_mut`]: slice::as_rchunks_mut\n  1726:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1727:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1728:     #[inline]\n  1729:     #[track_caller]\n  1730:     pub const fn rchunks_mut(&mut self, chunk_size: usize) -> RChunksMut<'_, T> {\n  1731:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1732:         RChunksMut::new(self, chunk_size)\n  1733:     }\n  1734: \n  1735:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1736:     /// end of the slice.\n  1737:     ///\n  1738:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1739:     /// slice, then the last up to `chunk_size-1` elements will be omitted and can be retrieved\n  1740:     /// from the `remainder` function of the iterator.\n  1741:     ///\n  1742:     /// Due to each chunk having exactly `chunk_size` elements, the compiler can often optimize the\n  1743:     /// resulting code better than in the case of [`rchunks`].\n  1744:     ///\n  1745:     /// See [`rchunks`] for a variant of this iterator that also returns the remainder as a smaller\n  1746:     /// chunk, and [`chunks_exact`] for the same iterator but starting at the beginning of the",
    "nanvix_source": "  1723:     /// assert_eq!(v, &[3, 2, 2, 1, 1]);\n  1724:     /// ```\n  1725:     ///\n  1726:     /// [`rchunks_exact_mut`]: slice::rchunks_exact_mut\n  1727:     /// [`chunks_mut`]: slice::chunks_mut\n  1728:     /// [`as_rchunks_mut`]: slice::as_rchunks_mut\n  1729:     #[stable(feature = \"rchunks\", since = \"1.31.0\")]\n  1730:     #[rustc_const_unstable(feature = \"const_slice_make_iter\", issue = \"137737\")]\n  1731:     #[inline]\n  1732:     #[track_caller]\n  1733:     pub const fn rchunks_mut(&mut self, chunk_size: usize) -> RChunksMut<'_, T> {\n  1734:         assert!(chunk_size != 0, \"chunk size must be non-zero\");\n  1735:         RChunksMut::new(self, chunk_size)\n  1736:     }\n  1737: \n  1738:     /// Returns an iterator over `chunk_size` elements of the slice at a time, starting at the\n  1739:     /// end of the slice.\n  1740:     ///\n  1741:     /// The chunks are slices and do not overlap. If `chunk_size` does not divide the length of the\n  1742:     /// slice, then the last up to `chunk_size-1` elements will be omitted and can be retrieved\n  1743:     /// from the `remainder` function of the iterator.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split",
    "generation_group": "iterator_or_adapter_result",
    "classification": "iterator_or_adapter_result",
    "classification_reasons": [
      "iterator_or_adapter_semantics_require_prophetic_model"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
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
        "is_unsafe": false
      },
      "name": "split",
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
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
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
            "pred",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "F"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10051,
            "path": "Split"
          }
        }
      }
    },
    "verification_source": "  2228:     /// ```\n  2229:     ///\n  2230:     /// If two matched elements are directly adjacent, an empty slice will be\n  2231:     /// present between them:\n  2232:     ///\n  2233:     /// ```\n  2234:     /// let slice = [10, 6, 33, 20];\n  2235:     /// let mut iter = slice.split(|num| num % 3 == 0);\n  2236:     ///\n  2237:     /// assert_eq!(iter.next().unwrap(), &[10]);\n  2238:     /// assert_eq!(iter.next().unwrap(), &[]);\n  2239:     /// assert_eq!(iter.next().unwrap(), &[20]);\n  2240:     /// assert!(iter.next().is_none());\n  2241:     /// ```\n  2242:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2243:     #[inline]\n  2244:     pub fn split<F>(&self, pred: F) -> Split<'_, T, F>\n  2245:     where\n  2246:         F: FnMut(&T) -> bool,\n  2247:     {\n  2248:         Split::new(self, pred)\n  2249:     }\n  2250: \n  2251:     /// Returns an iterator over mutable subslices separated by elements that\n  2252:     /// match `pred`. The matched element is not contained in the subslices.\n  2253:     ///\n  2254:     /// # Examples\n  2255:     ///\n  2256:     /// ```\n  2257:     /// let mut v = [10, 40, 30, 20, 60, 50];\n  2258:     ///\n  2259:     /// for group in v.split_mut(|num| *num % 3 == 0) {\n  2260:     ///     group[0] = 1;",
    "nanvix_source": "  2237:     /// let slice = [10, 6, 33, 20];\n  2238:     /// let mut iter = slice.split(|num| num % 3 == 0);\n  2239:     ///\n  2240:     /// assert_eq!(iter.next().unwrap(), &[10]);\n  2241:     /// assert_eq!(iter.next().unwrap(), &[]);\n  2242:     /// assert_eq!(iter.next().unwrap(), &[20]);\n  2243:     /// assert!(iter.next().is_none());\n  2244:     /// ```\n  2245:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2246:     #[inline]\n  2247:     pub fn split<F>(&self, pred: F) -> Split<'_, T, F>\n  2248:     where\n  2249:         F: FnMut(&T) -> bool,\n  2250:     {\n  2251:         Split::new(self, pred)\n  2252:     }\n  2253: \n  2254:     /// Returns an iterator over mutable subslices separated by elements that\n  2255:     /// match `pred`. The matched element is not contained in the subslices.\n  2256:     ///\n  2257:     /// # Examples",
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
