For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::LinkedList::is_empty",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
    "verification_source": "   615:     /// This operation should compute in *O*(1) time.\n   616:     ///\n   617:     /// # Examples\n   618:     ///\n   619:     /// ```\n   620:     /// use std::collections::LinkedList;\n   621:     ///\n   622:     /// let mut dl = LinkedList::new();\n   623:     /// assert!(dl.is_empty());\n   624:     ///\n   625:     /// dl.push_front(\"foo\");\n   626:     /// assert!(!dl.is_empty());\n   627:     /// ```\n   628:     #[inline]\n   629:     #[must_use]\n   630:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   631:     pub fn is_empty(&self) -> bool {\n   632:         self.head.is_none()\n   633:     }\n   634: \n   635:     /// Returns the length of the `LinkedList`.\n   636:     ///\n   637:     /// This operation should compute in *O*(1) time.\n   638:     ///\n   639:     /// # Examples\n   640:     ///\n   641:     /// ```\n   642:     /// use std::collections::LinkedList;\n   643:     ///\n   644:     /// let mut dl = LinkedList::new();\n   645:     ///\n   646:     /// dl.push_front(2);\n   647:     /// assert_eq!(dl.len(), 1);",
    "nanvix_source": "   621:     ///\n   622:     /// let mut dl = LinkedList::new();\n   623:     /// assert!(dl.is_empty());\n   624:     ///\n   625:     /// dl.push_front(\"foo\");\n   626:     /// assert!(!dl.is_empty());\n   627:     /// ```\n   628:     #[inline]\n   629:     #[must_use]\n   630:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   631:     pub fn is_empty(&self) -> bool {\n   632:         self.head.is_none()\n   633:     }\n   634: \n   635:     /// Returns the length of the `LinkedList`.\n   636:     ///\n   637:     /// This operation should compute in *O*(1) time.\n   638:     ///\n   639:     /// # Examples\n   640:     ///\n   641:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::len",
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
      "name": "len",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
    "verification_source": "   643:     ///\n   644:     /// let mut dl = LinkedList::new();\n   645:     ///\n   646:     /// dl.push_front(2);\n   647:     /// assert_eq!(dl.len(), 1);\n   648:     ///\n   649:     /// dl.push_front(1);\n   650:     /// assert_eq!(dl.len(), 2);\n   651:     ///\n   652:     /// dl.push_back(3);\n   653:     /// assert_eq!(dl.len(), 3);\n   654:     /// ```\n   655:     #[inline]\n   656:     #[must_use]\n   657:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   658:     #[rustc_confusables(\"length\", \"size\")]\n   659:     pub fn len(&self) -> usize {\n   660:         self.len\n   661:     }\n   662: \n   663:     /// Removes all elements from the `LinkedList`.\n   664:     ///\n   665:     /// This operation should compute in *O*(*n*) time.\n   666:     ///\n   667:     /// # Examples\n   668:     ///\n   669:     /// ```\n   670:     /// use std::collections::LinkedList;\n   671:     ///\n   672:     /// let mut dl = LinkedList::new();\n   673:     ///\n   674:     /// dl.push_front(2);\n   675:     /// dl.push_front(1);",
    "nanvix_source": "   649:     /// dl.push_front(1);\n   650:     /// assert_eq!(dl.len(), 2);\n   651:     ///\n   652:     /// dl.push_back(3);\n   653:     /// assert_eq!(dl.len(), 3);\n   654:     /// ```\n   655:     #[inline]\n   656:     #[must_use]\n   657:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   658:     #[rustc_confusables(\"length\", \"size\")]\n   659:     pub fn len(&self) -> usize {\n   660:         self.len\n   661:     }\n   662: \n   663:     /// Removes all elements from the `LinkedList`.\n   664:     ///\n   665:     /// This operation should compute in *O*(*n*) time.\n   666:     ///\n   667:     /// # Examples\n   668:     ///\n   669:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::new",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "new",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2515",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   431: }\n   432: \n   433: impl<T> LinkedList<T> {\n   434:     /// Creates an empty `LinkedList`.\n   435:     ///\n   436:     /// # Examples\n   437:     ///\n   438:     /// ```\n   439:     /// use std::collections::LinkedList;\n   440:     ///\n   441:     /// let list: LinkedList<u32> = LinkedList::new();\n   442:     /// ```\n   443:     #[inline]\n   444:     #[rustc_const_stable(feature = \"const_linked_list_new\", since = \"1.39.0\")]\n   445:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   446:     #[must_use]\n   447:     pub const fn new() -> Self {\n   448:         LinkedList { head: None, tail: None, len: 0, alloc: Global, marker: PhantomData }\n   449:     }\n   450: \n   451:     /// Moves all elements from `other` to the end of the list.\n   452:     ///\n   453:     /// This reuses all the nodes from `other` and moves them into `self`. After\n   454:     /// this operation, `other` becomes empty.\n   455:     ///\n   456:     /// This operation should compute in *O*(1) time and *O*(1) memory.\n   457:     ///\n   458:     /// # Examples\n   459:     ///\n   460:     /// ```\n   461:     /// use std::collections::LinkedList;\n   462:     ///\n   463:     /// let mut list1 = LinkedList::new();",
    "nanvix_source": "   437:     ///\n   438:     /// ```\n   439:     /// use std::collections::LinkedList;\n   440:     ///\n   441:     /// let list: LinkedList<u32> = LinkedList::new();\n   442:     /// ```\n   443:     #[inline]\n   444:     #[rustc_const_stable(feature = \"const_linked_list_new\", since = \"1.39.0\")]\n   445:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   446:     #[must_use]\n   447:     pub const fn new() -> Self {\n   448:         LinkedList { head: None, tail: None, len: 0, alloc: Global, marker: PhantomData }\n   449:     }\n   450: \n   451:     /// Moves all elements from `other` to the end of the list.\n   452:     ///\n   453:     /// This reuses all the nodes from `other` and moves them into `self`. After\n   454:     /// this operation, `other` becomes empty.\n   455:     ///\n   456:     /// This operation should compute in *O*(1) time and *O*(1) memory.\n   457:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::pop_back",
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
      "name": "pop_back",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
                      "generic": "T"
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
    "verification_source": "   949:     /// it is empty.\n   950:     ///\n   951:     /// This operation should compute in *O*(1) time.\n   952:     ///\n   953:     /// # Examples\n   954:     ///\n   955:     /// ```\n   956:     /// use std::collections::LinkedList;\n   957:     ///\n   958:     /// let mut d = LinkedList::new();\n   959:     /// assert_eq!(d.pop_back(), None);\n   960:     /// d.push_back(1);\n   961:     /// d.push_back(3);\n   962:     /// assert_eq!(d.pop_back(), Some(3));\n   963:     /// ```\n   964:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   965:     pub fn pop_back(&mut self) -> Option<T> {\n   966:         self.pop_back_node().map(Node::into_element)\n   967:     }\n   968: \n   969:     /// Splits the list into two at the given index. Returns everything after the given index,\n   970:     /// including the index.\n   971:     ///\n   972:     /// This operation should compute in *O*(*n*) time.\n   973:     ///\n   974:     /// # Panics\n   975:     ///\n   976:     /// Panics if `at > len`.\n   977:     ///\n   978:     /// # Examples\n   979:     ///\n   980:     /// ```\n   981:     /// use std::collections::LinkedList;",
    "nanvix_source": "   955:     /// ```\n   956:     /// use std::collections::LinkedList;\n   957:     ///\n   958:     /// let mut d = LinkedList::new();\n   959:     /// assert_eq!(d.pop_back(), None);\n   960:     /// d.push_back(1);\n   961:     /// d.push_back(3);\n   962:     /// assert_eq!(d.pop_back(), Some(3));\n   963:     /// ```\n   964:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   965:     pub fn pop_back(&mut self) -> Option<T> {\n   966:         self.pop_back_node().map(Node::into_element)\n   967:     }\n   968: \n   969:     /// Splits the list into two at the given index. Returns everything after the given index,\n   970:     /// including the index.\n   971:     ///\n   972:     /// This operation should compute in *O*(*n*) time.\n   973:     ///\n   974:     /// # Panics\n   975:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::pop_front",
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
      "name": "pop_front",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
                      "generic": "T"
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
    "verification_source": "   881:     ///\n   882:     /// # Examples\n   883:     ///\n   884:     /// ```\n   885:     /// use std::collections::LinkedList;\n   886:     ///\n   887:     /// let mut d = LinkedList::new();\n   888:     /// assert_eq!(d.pop_front(), None);\n   889:     ///\n   890:     /// d.push_front(1);\n   891:     /// d.push_front(3);\n   892:     /// assert_eq!(d.pop_front(), Some(3));\n   893:     /// assert_eq!(d.pop_front(), Some(1));\n   894:     /// assert_eq!(d.pop_front(), None);\n   895:     /// ```\n   896:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   897:     pub fn pop_front(&mut self) -> Option<T> {\n   898:         self.pop_front_node().map(Node::into_element)\n   899:     }\n   900: \n   901:     /// Adds an element to the back of the list.\n   902:     ///\n   903:     /// This operation should compute in *O*(1) time.\n   904:     ///\n   905:     /// # Examples\n   906:     ///\n   907:     /// ```\n   908:     /// use std::collections::LinkedList;\n   909:     ///\n   910:     /// let mut d = LinkedList::new();\n   911:     /// d.push_back(1);\n   912:     /// d.push_back(3);\n   913:     /// assert_eq!(3, *d.back().unwrap());",
    "nanvix_source": "   887:     /// let mut d = LinkedList::new();\n   888:     /// assert_eq!(d.pop_front(), None);\n   889:     ///\n   890:     /// d.push_front(1);\n   891:     /// d.push_front(3);\n   892:     /// assert_eq!(d.pop_front(), Some(3));\n   893:     /// assert_eq!(d.pop_front(), Some(1));\n   894:     /// assert_eq!(d.pop_front(), None);\n   895:     /// ```\n   896:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   897:     pub fn pop_front(&mut self) -> Option<T> {\n   898:         self.pop_front_node().map(Node::into_element)\n   899:     }\n   900: \n   901:     /// Adds an element to the back of the list.\n   902:     ///\n   903:     /// This operation should compute in *O*(1) time.\n   904:     ///\n   905:     /// # Examples\n   906:     ///\n   907:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::push_back",
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
      "name": "push_back",
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
            "id": 2512,
            "path": "LinkedList"
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
        "impl_id": "alloc:2546",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2512",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "linked_list",
          "LinkedList"
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
            "elt",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   901:     /// Adds an element to the back of the list.\n   902:     ///\n   903:     /// This operation should compute in *O*(1) time.\n   904:     ///\n   905:     /// # Examples\n   906:     ///\n   907:     /// ```\n   908:     /// use std::collections::LinkedList;\n   909:     ///\n   910:     /// let mut d = LinkedList::new();\n   911:     /// d.push_back(1);\n   912:     /// d.push_back(3);\n   913:     /// assert_eq!(3, *d.back().unwrap());\n   914:     /// ```\n   915:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   916:     #[rustc_confusables(\"push\", \"append\")]\n   917:     pub fn push_back(&mut self, elt: T) {\n   918:         let _ = self.push_back_mut(elt);\n   919:     }\n   920: \n   921:     /// Adds an element to the back of the list, returning a reference to it.\n   922:     ///\n   923:     /// This operation should compute in *O*(1) time.\n   924:     ///\n   925:     /// # Examples\n   926:     ///\n   927:     /// ```\n   928:     /// use std::collections::LinkedList;\n   929:     ///\n   930:     /// let mut dl = LinkedList::from([1, 2, 3]);\n   931:     ///\n   932:     /// let ptr = dl.push_back_mut(2);\n   933:     /// *ptr += 4;",
    "nanvix_source": "   907:     /// ```\n   908:     /// use std::collections::LinkedList;\n   909:     ///\n   910:     /// let mut d = LinkedList::new();\n   911:     /// d.push_back(1);\n   912:     /// d.push_back(3);\n   913:     /// assert_eq!(3, *d.back().unwrap());\n   914:     /// ```\n   915:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   916:     #[rustc_confusables(\"push\", \"append\")]\n   917:     pub fn push_back(&mut self, elt: T) {\n   918:         let _ = self.push_back_mut(elt);\n   919:     }\n   920: \n   921:     /// Adds an element to the back of the list, returning a reference to it.\n   922:     ///\n   923:     /// This operation should compute in *O*(1) time.\n   924:     ///\n   925:     /// # Examples\n   926:     ///\n   927:     /// ```",
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
