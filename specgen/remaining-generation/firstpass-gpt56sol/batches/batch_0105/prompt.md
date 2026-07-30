For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::front",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "front",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1964:     /// empty.\n  1965:     ///\n  1966:     /// # Examples\n  1967:     ///\n  1968:     /// ```\n  1969:     /// use std::collections::VecDeque;\n  1970:     ///\n  1971:     /// let mut d = VecDeque::new();\n  1972:     /// assert_eq!(d.front(), None);\n  1973:     ///\n  1974:     /// d.push_back(1);\n  1975:     /// d.push_back(2);\n  1976:     /// assert_eq!(d.front(), Some(&1));\n  1977:     /// ```\n  1978:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1979:     #[rustc_confusables(\"first\")]\n  1980:     pub fn front(&self) -> Option<&T> {\n  1981:         self.get(0)\n  1982:     }\n  1983: \n  1984:     /// Provides a mutable reference to the front element, or `None` if the\n  1985:     /// deque is empty.\n  1986:     ///\n  1987:     /// # Examples\n  1988:     ///\n  1989:     /// ```\n  1990:     /// use std::collections::VecDeque;\n  1991:     ///\n  1992:     /// let mut d = VecDeque::new();\n  1993:     /// assert_eq!(d.front_mut(), None);\n  1994:     ///\n  1995:     /// d.push_back(1);\n  1996:     /// d.push_back(2);",
    "nanvix_source": "  2034:     ///\n  2035:     /// let mut d = VecDeque::new();\n  2036:     /// assert_eq!(d.front(), None);\n  2037:     ///\n  2038:     /// d.push_back(1);\n  2039:     /// d.push_back(2);\n  2040:     /// assert_eq!(d.front(), Some(&1));\n  2041:     /// ```\n  2042:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2043:     #[rustc_confusables(\"first\")]\n  2044:     pub fn front(&self) -> Option<&T> {\n  2045:         self.get(0)\n  2046:     }\n  2047: \n  2048:     /// Provides a mutable reference to the front element, or `None` if the\n  2049:     /// deque is empty.\n  2050:     ///\n  2051:     /// # Examples\n  2052:     ///\n  2053:     /// ```\n  2054:     /// use std::collections::VecDeque;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::get",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "get",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "index",
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
                      "borrowed_ref": {
                        "is_mutable": false,
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
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   897:     ///\n   898:     /// Element at index 0 is the front of the queue.\n   899:     ///\n   900:     /// # Examples\n   901:     ///\n   902:     /// ```\n   903:     /// use std::collections::VecDeque;\n   904:     ///\n   905:     /// let mut buf = VecDeque::new();\n   906:     /// buf.push_back(3);\n   907:     /// buf.push_back(4);\n   908:     /// buf.push_back(5);\n   909:     /// buf.push_back(6);\n   910:     /// assert_eq!(buf.get(1), Some(&4));\n   911:     /// ```\n   912:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   913:     pub fn get(&self, index: usize) -> Option<&T> {\n   914:         if index < self.len {\n   915:             let idx = self.to_physical_idx(index);\n   916:             unsafe { Some(&*self.ptr().add(idx)) }\n   917:         } else {\n   918:             None\n   919:         }\n   920:     }\n   921: \n   922:     /// Provides a mutable reference to the element at the given index.\n   923:     ///\n   924:     /// Element at index 0 is the front of the queue.\n   925:     ///\n   926:     /// # Examples\n   927:     ///\n   928:     /// ```\n   929:     /// use std::collections::VecDeque;",
    "nanvix_source": "   956:     /// use std::collections::VecDeque;\n   957:     ///\n   958:     /// let mut buf = VecDeque::new();\n   959:     /// buf.push_back(3);\n   960:     /// buf.push_back(4);\n   961:     /// buf.push_back(5);\n   962:     /// buf.push_back(6);\n   963:     /// assert_eq!(buf.get(1), Some(&4));\n   964:     /// ```\n   965:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   966:     pub fn get(&self, index: usize) -> Option<&T> {\n   967:         if index < self.len {\n   968:             let idx = self.to_wrapped_index(index);\n   969:             unsafe { Some(&*self.ptr().add(idx.as_index())) }\n   970:         } else {\n   971:             None\n   972:         }\n   973:     }\n   974: \n   975:     /// Provides a mutable reference to the element at the given index.\n   976:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::is_empty",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "is_empty",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
    "verification_source": "  1640:         self.len\n  1641:     }\n  1642: \n  1643:     /// Returns `true` if the deque is empty.\n  1644:     ///\n  1645:     /// # Examples\n  1646:     ///\n  1647:     /// ```\n  1648:     /// use std::collections::VecDeque;\n  1649:     ///\n  1650:     /// let mut deque = VecDeque::new();\n  1651:     /// assert!(deque.is_empty());\n  1652:     /// deque.push_front(1);\n  1653:     /// assert!(!deque.is_empty());\n  1654:     /// ```\n  1655:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1656:     pub fn is_empty(&self) -> bool {\n  1657:         self.len == 0\n  1658:     }\n  1659: \n  1660:     /// Given a range into the logical buffer of the deque, this function\n  1661:     /// return two ranges into the physical buffer that correspond to\n  1662:     /// the given range. The `len` parameter should usually just be `self.len`;\n  1663:     /// the reason it's passed explicitly is that if the deque is wrapped in\n  1664:     /// a `Drain`, then `self.len` is not actually the length of the deque.\n  1665:     ///\n  1666:     /// # Safety\n  1667:     ///\n  1668:     /// This function is always safe to call. For the resulting ranges to be valid\n  1669:     /// ranges into the physical buffer, the caller must ensure that the result of\n  1670:     /// calling `slice::range(range, ..len)` represents a valid range into the\n  1671:     /// logical buffer, and that all elements in that range are initialized.\n  1672:     fn slice_ranges<R>(&self, range: R, len: usize) -> (Range<usize>, Range<usize>)",
    "nanvix_source": "  1710:     ///\n  1711:     /// ```\n  1712:     /// use std::collections::VecDeque;\n  1713:     ///\n  1714:     /// let mut deque = VecDeque::new();\n  1715:     /// assert!(deque.is_empty());\n  1716:     /// deque.push_front(1);\n  1717:     /// assert!(!deque.is_empty());\n  1718:     /// ```\n  1719:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1720:     pub fn is_empty(&self) -> bool {\n  1721:         self.len == 0\n  1722:     }\n  1723: \n  1724:     /// Given a range into the logical buffer of the deque, this function\n  1725:     /// return two ranges into the physical buffer that correspond to\n  1726:     /// the given range. The `len` parameter should usually just be `self.len`;\n  1727:     /// the reason it's passed explicitly is that if the deque is wrapped in\n  1728:     /// a `Drain`, then `self.len` is not actually the length of the deque.\n  1729:     ///\n  1730:     /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::rotate_left",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "rotate_left",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "n",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2975:     ///\n  2976:     /// ```\n  2977:     /// use std::collections::VecDeque;\n  2978:     ///\n  2979:     /// let mut buf: VecDeque<_> = (0..10).collect();\n  2980:     ///\n  2981:     /// buf.rotate_left(3);\n  2982:     /// assert_eq!(buf, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]);\n  2983:     ///\n  2984:     /// for i in 1..10 {\n  2985:     ///     assert_eq!(i * 3 % 10, buf[0]);\n  2986:     ///     buf.rotate_left(3);\n  2987:     /// }\n  2988:     /// assert_eq!(buf, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);\n  2989:     /// ```\n  2990:     #[stable(feature = \"vecdeque_rotate\", since = \"1.36.0\")]\n  2991:     pub fn rotate_left(&mut self, n: usize) {\n  2992:         assert!(n <= self.len());\n  2993:         let k = self.len - n;\n  2994:         if n <= k {\n  2995:             unsafe { self.rotate_left_inner(n) }\n  2996:         } else {\n  2997:             unsafe { self.rotate_right_inner(k) }\n  2998:         }\n  2999:     }\n  3000: \n  3001:     /// Rotates the double-ended queue `n` places to the right.\n  3002:     ///\n  3003:     /// Equivalently,\n  3004:     /// - Rotates the first item into position `n`.\n  3005:     /// - Pops the last `n` items and pushes them to the front.\n  3006:     /// - Rotates `len() - n` places to the left.\n  3007:     ///",
    "nanvix_source": "  3063:     /// buf.rotate_left(3);\n  3064:     /// assert_eq!(buf, [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]);\n  3065:     ///\n  3066:     /// for i in 1..10 {\n  3067:     ///     assert_eq!(i * 3 % 10, buf[0]);\n  3068:     ///     buf.rotate_left(3);\n  3069:     /// }\n  3070:     /// assert_eq!(buf, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);\n  3071:     /// ```\n  3072:     #[stable(feature = \"vecdeque_rotate\", since = \"1.36.0\")]\n  3073:     pub fn rotate_left(&mut self, n: usize) {\n  3074:         assert!(n <= self.len());\n  3075:         let k = self.len - n;\n  3076:         if n <= k {\n  3077:             unsafe { self.rotate_left_inner(n) }\n  3078:         } else {\n  3079:             unsafe { self.rotate_right_inner(k) }\n  3080:         }\n  3081:     }\n  3082: \n  3083:     /// Rotates the double-ended queue `n` places to the right.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::rotate_right",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "rotate_right",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "n",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  3018:     ///\n  3019:     /// ```\n  3020:     /// use std::collections::VecDeque;\n  3021:     ///\n  3022:     /// let mut buf: VecDeque<_> = (0..10).collect();\n  3023:     ///\n  3024:     /// buf.rotate_right(3);\n  3025:     /// assert_eq!(buf, [7, 8, 9, 0, 1, 2, 3, 4, 5, 6]);\n  3026:     ///\n  3027:     /// for i in 1..10 {\n  3028:     ///     assert_eq!(0, buf[i * 3 % 10]);\n  3029:     ///     buf.rotate_right(3);\n  3030:     /// }\n  3031:     /// assert_eq!(buf, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);\n  3032:     /// ```\n  3033:     #[stable(feature = \"vecdeque_rotate\", since = \"1.36.0\")]\n  3034:     pub fn rotate_right(&mut self, n: usize) {\n  3035:         assert!(n <= self.len());\n  3036:         let k = self.len - n;\n  3037:         if n <= k {\n  3038:             unsafe { self.rotate_right_inner(n) }\n  3039:         } else {\n  3040:             unsafe { self.rotate_left_inner(k) }\n  3041:         }\n  3042:     }\n  3043: \n  3044:     // SAFETY: the following two methods require that the rotation amount\n  3045:     // be less than half the length of the deque.\n  3046:     //\n  3047:     // `wrap_copy` requires that `min(x, capacity() - x) + copy_len <= capacity()`,\n  3048:     // but then `min` is never more than half the capacity, regardless of x,\n  3049:     // so it's sound to call here because we're calling with something\n  3050:     // less than half the length, which is never above half the capacity.",
    "nanvix_source": "  3106:     /// buf.rotate_right(3);\n  3107:     /// assert_eq!(buf, [7, 8, 9, 0, 1, 2, 3, 4, 5, 6]);\n  3108:     ///\n  3109:     /// for i in 1..10 {\n  3110:     ///     assert_eq!(0, buf[i * 3 % 10]);\n  3111:     ///     buf.rotate_right(3);\n  3112:     /// }\n  3113:     /// assert_eq!(buf, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);\n  3114:     /// ```\n  3115:     #[stable(feature = \"vecdeque_rotate\", since = \"1.36.0\")]\n  3116:     pub fn rotate_right(&mut self, n: usize) {\n  3117:         assert!(n <= self.len());\n  3118:         let k = self.len - n;\n  3119:         if n <= k {\n  3120:             unsafe { self.rotate_right_inner(n) }\n  3121:         } else {\n  3122:             unsafe { self.rotate_left_inner(k) }\n  3123:         }\n  3124:     }\n  3125: \n  3126:     // SAFETY: the following two methods require that the rotation amount",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::swap",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "swap",
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
            "id": 2511,
            "path": "VecDeque"
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
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
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
            "i",
            {
              "primitive": "usize"
            }
          ],
          [
            "j",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   960:     /// Panics if either index is out of bounds.\n   961:     ///\n   962:     /// # Examples\n   963:     ///\n   964:     /// ```\n   965:     /// use std::collections::VecDeque;\n   966:     ///\n   967:     /// let mut buf = VecDeque::new();\n   968:     /// buf.push_back(3);\n   969:     /// buf.push_back(4);\n   970:     /// buf.push_back(5);\n   971:     /// assert_eq!(buf, [3, 4, 5]);\n   972:     /// buf.swap(0, 2);\n   973:     /// assert_eq!(buf, [5, 4, 3]);\n   974:     /// ```\n   975:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   976:     pub fn swap(&mut self, i: usize, j: usize) {\n   977:         assert!(i < self.len());\n   978:         assert!(j < self.len());\n   979:         let ri = self.to_physical_idx(i);\n   980:         let rj = self.to_physical_idx(j);\n   981:         unsafe { ptr::swap(self.ptr().add(ri), self.ptr().add(rj)) }\n   982:     }\n   983: \n   984:     /// Returns the number of elements the deque can hold without\n   985:     /// reallocating.\n   986:     ///\n   987:     /// # Examples\n   988:     ///\n   989:     /// ```\n   990:     /// use std::collections::VecDeque;\n   991:     ///\n   992:     /// let buf: VecDeque<i32> = VecDeque::with_capacity(10);",
    "nanvix_source": "  1019:     ///\n  1020:     /// let mut buf = VecDeque::new();\n  1021:     /// buf.push_back(3);\n  1022:     /// buf.push_back(4);\n  1023:     /// buf.push_back(5);\n  1024:     /// assert_eq!(buf, [3, 4, 5]);\n  1025:     /// buf.swap(0, 2);\n  1026:     /// assert_eq!(buf, [5, 4, 3]);\n  1027:     /// ```\n  1028:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1029:     pub fn swap(&mut self, i: usize, j: usize) {\n  1030:         assert!(i < self.len());\n  1031:         assert!(j < self.len());\n  1032:         let ri = self.to_wrapped_index(i);\n  1033:         let rj = self.to_wrapped_index(j);\n  1034:         unsafe { ptr::swap(self.ptr().add(ri.as_index()), self.ptr().add(rj.as_index())) }\n  1035:     }\n  1036: \n  1037:     /// Returns the number of elements the deque can hold without\n  1038:     /// reallocating.\n  1039:     ///",
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
