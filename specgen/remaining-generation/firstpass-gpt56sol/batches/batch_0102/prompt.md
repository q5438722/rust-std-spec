For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BinaryHeap::push",
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
      "name": "push",
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
            "id": 979,
            "path": "BinaryHeap"
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
                          "id": 176,
                          "path": "Ord"
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
        "impl_id": "alloc:995",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "item",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   731:     ///\n   732:     /// The expected cost of `push`, averaged over every possible ordering of\n   733:     /// the elements being pushed, and over a sufficiently large number of\n   734:     /// pushes, is *O*(1). This is the most meaningful cost metric when pushing\n   735:     /// elements that are *not* already in any sorted pattern.\n   736:     ///\n   737:     /// The time complexity degrades if elements are pushed in predominantly\n   738:     /// ascending order. In the worst case, elements are pushed in ascending\n   739:     /// sorted order and the amortized cost per push is *O*(log(*n*)) against a heap\n   740:     /// containing *n* elements.\n   741:     ///\n   742:     /// The worst case cost of a *single* call to `push` is *O*(*n*). The worst case\n   743:     /// occurs when capacity is exhausted and needs a resize. The resize cost\n   744:     /// has been amortized in the previous figures.\n   745:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   746:     #[rustc_confusables(\"append\", \"put\")]\n   747:     pub fn push(&mut self, item: T) {\n   748:         let old_len = self.len();\n   749:         self.data.push(item);\n   750:         // SAFETY: Since we pushed a new item it means that\n   751:         //  old_len = self.len() - 1 < self.len()\n   752:         unsafe { self.sift_up(0, old_len) };\n   753:     }\n   754: \n   755:     /// Consumes the `BinaryHeap` and returns a vector in sorted\n   756:     /// (ascending) order.\n   757:     ///\n   758:     /// # Examples\n   759:     ///\n   760:     /// Basic usage:\n   761:     ///\n   762:     /// ```\n   763:     /// use std::collections::BinaryHeap;",
    "nanvix_source": "   737:     /// The time complexity degrades if elements are pushed in predominantly\n   738:     /// ascending order. In the worst case, elements are pushed in ascending\n   739:     /// sorted order and the amortized cost per push is *O*(log(*n*)) against a heap\n   740:     /// containing *n* elements.\n   741:     ///\n   742:     /// The worst case cost of a *single* call to `push` is *O*(*n*). The worst case\n   743:     /// occurs when capacity is exhausted and needs a resize. The resize cost\n   744:     /// has been amortized in the previous figures.\n   745:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   746:     #[rustc_confusables(\"append\", \"put\")]\n   747:     pub fn push(&mut self, item: T) {\n   748:         let old_len = self.len();\n   749:         self.data.push(item);\n   750:         // SAFETY: Since we pushed a new item it means that\n   751:         //  old_len = self.len() - 1 < self.len()\n   752:         unsafe { self.sift_up(0, old_len) };\n   753:     }\n   754: \n   755:     /// Consumes the `BinaryHeap` and returns a vector in sorted\n   756:     /// (ascending) order.\n   757:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::append",
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
      "name": "append",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "other"
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
            "other",
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
    "verification_source": "   465:     ///\n   466:     /// let mut list2 = LinkedList::new();\n   467:     /// list2.push_back('b');\n   468:     /// list2.push_back('c');\n   469:     ///\n   470:     /// list1.append(&mut list2);\n   471:     ///\n   472:     /// let mut iter = list1.iter();\n   473:     /// assert_eq!(iter.next(), Some(&'a'));\n   474:     /// assert_eq!(iter.next(), Some(&'b'));\n   475:     /// assert_eq!(iter.next(), Some(&'c'));\n   476:     /// assert!(iter.next().is_none());\n   477:     ///\n   478:     /// assert!(list2.is_empty());\n   479:     /// ```\n   480:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   481:     pub fn append(&mut self, other: &mut Self) {\n   482:         match self.tail {\n   483:             None => mem::swap(self, other),\n   484:             Some(mut tail) => {\n   485:                 // `as_mut` is okay here because we have exclusive access to the entirety\n   486:                 // of both lists.\n   487:                 if let Some(mut other_head) = other.head.take() {\n   488:                     unsafe {\n   489:                         tail.as_mut().next = Some(other_head);\n   490:                         other_head.as_mut().prev = Some(tail);\n   491:                     }\n   492: \n   493:                     self.tail = other.tail.take();\n   494:                     self.len += mem::replace(&mut other.len, 0);\n   495:                 }\n   496:             }\n   497:         }",
    "nanvix_source": "   471:     ///\n   472:     /// let mut iter = list1.iter();\n   473:     /// assert_eq!(iter.next(), Some(&'a'));\n   474:     /// assert_eq!(iter.next(), Some(&'b'));\n   475:     /// assert_eq!(iter.next(), Some(&'c'));\n   476:     /// assert!(iter.next().is_none());\n   477:     ///\n   478:     /// assert!(list2.is_empty());\n   479:     /// ```\n   480:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   481:     pub fn append(&mut self, other: &mut Self) {\n   482:         match self.tail {\n   483:             None => mem::swap(self, other),\n   484:             Some(mut tail) => {\n   485:                 // `as_mut` is okay here because we have exclusive access to the entirety\n   486:                 // of both lists.\n   487:                 if let Some(mut other_head) = other.head.take() {\n   488:                     unsafe {\n   489:                         tail.as_mut().next = Some(other_head);\n   490:                         other_head.as_mut().prev = Some(tail);\n   491:                     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::back",
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
      "name": "back",
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
    "verification_source": "   780:     /// This operation should compute in *O*(1) time.\n   781:     ///\n   782:     /// # Examples\n   783:     ///\n   784:     /// ```\n   785:     /// use std::collections::LinkedList;\n   786:     ///\n   787:     /// let mut dl = LinkedList::new();\n   788:     /// assert_eq!(dl.back(), None);\n   789:     ///\n   790:     /// dl.push_back(1);\n   791:     /// assert_eq!(dl.back(), Some(&1));\n   792:     /// ```\n   793:     #[inline]\n   794:     #[must_use]\n   795:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   796:     pub fn back(&self) -> Option<&T> {\n   797:         unsafe { self.tail.as_ref().map(|node| &node.as_ref().element) }\n   798:     }\n   799: \n   800:     /// Provides a mutable reference to the back element, or `None` if the list\n   801:     /// is empty.\n   802:     ///\n   803:     /// This operation should compute in *O*(1) time.\n   804:     ///\n   805:     /// # Examples\n   806:     ///\n   807:     /// ```\n   808:     /// use std::collections::LinkedList;\n   809:     ///\n   810:     /// let mut dl = LinkedList::new();\n   811:     /// assert_eq!(dl.back(), None);\n   812:     ///",
    "nanvix_source": "   786:     ///\n   787:     /// let mut dl = LinkedList::new();\n   788:     /// assert_eq!(dl.back(), None);\n   789:     ///\n   790:     /// dl.push_back(1);\n   791:     /// assert_eq!(dl.back(), Some(&1));\n   792:     /// ```\n   793:     #[inline]\n   794:     #[must_use]\n   795:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   796:     pub fn back(&self) -> Option<&T> {\n   797:         unsafe { self.tail.as_ref().map(|node| &node.as_ref().element) }\n   798:     }\n   799: \n   800:     /// Provides a mutable reference to the back element, or `None` if the list\n   801:     /// is empty.\n   802:     ///\n   803:     /// This operation should compute in *O*(1) time.\n   804:     ///\n   805:     /// # Examples\n   806:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::clear",
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
      "name": "clear",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   669:     /// ```\n   670:     /// use std::collections::LinkedList;\n   671:     ///\n   672:     /// let mut dl = LinkedList::new();\n   673:     ///\n   674:     /// dl.push_front(2);\n   675:     /// dl.push_front(1);\n   676:     /// assert_eq!(dl.len(), 2);\n   677:     /// assert_eq!(dl.front(), Some(&1));\n   678:     ///\n   679:     /// dl.clear();\n   680:     /// assert_eq!(dl.len(), 0);\n   681:     /// assert_eq!(dl.front(), None);\n   682:     /// ```\n   683:     #[inline]\n   684:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   685:     pub fn clear(&mut self) {\n   686:         // We need to drop the nodes while keeping self.alloc\n   687:         // We can do this by moving (head, tail, len) into a new list that borrows self.alloc\n   688:         drop(LinkedList {\n   689:             head: self.head.take(),\n   690:             tail: self.tail.take(),\n   691:             len: mem::take(&mut self.len),\n   692:             alloc: &self.alloc,\n   693:             marker: PhantomData,\n   694:         });\n   695:     }\n   696: \n   697:     /// Returns `true` if the `LinkedList` contains an element equal to the\n   698:     /// given value.\n   699:     ///\n   700:     /// This operation should compute linearly in *O*(*n*) time.\n   701:     ///",
    "nanvix_source": "   675:     /// dl.push_front(1);\n   676:     /// assert_eq!(dl.len(), 2);\n   677:     /// assert_eq!(dl.front(), Some(&1));\n   678:     ///\n   679:     /// dl.clear();\n   680:     /// assert_eq!(dl.len(), 0);\n   681:     /// assert_eq!(dl.front(), None);\n   682:     /// ```\n   683:     #[inline]\n   684:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   685:     pub fn clear(&mut self) {\n   686:         // We need to drop the nodes while keeping self.alloc\n   687:         // We can do this by moving (head, tail, len) into a new list that borrows self.alloc\n   688:         drop(LinkedList {\n   689:             head: self.head.take(),\n   690:             tail: self.tail.take(),\n   691:             len: mem::take(&mut self.len),\n   692:             alloc: &self.alloc,\n   693:             marker: PhantomData,\n   694:         });\n   695:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::contains",
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
                      "id": 179,
                      "path": "PartialEq"
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
      "name": "contains",
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
          ],
          [
            "x",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "T"
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
    "verification_source": "   701:     ///\n   702:     /// # Examples\n   703:     ///\n   704:     /// ```\n   705:     /// use std::collections::LinkedList;\n   706:     ///\n   707:     /// let mut list: LinkedList<u32> = LinkedList::new();\n   708:     ///\n   709:     /// list.push_back(0);\n   710:     /// list.push_back(1);\n   711:     /// list.push_back(2);\n   712:     ///\n   713:     /// assert_eq!(list.contains(&0), true);\n   714:     /// assert_eq!(list.contains(&10), false);\n   715:     /// ```\n   716:     #[stable(feature = \"linked_list_contains\", since = \"1.12.0\")]\n   717:     pub fn contains(&self, x: &T) -> bool\n   718:     where\n   719:         T: PartialEq<T>,\n   720:     {\n   721:         self.iter().any(|e| e == x)\n   722:     }\n   723: \n   724:     /// Provides a reference to the front element, or `None` if the list is\n   725:     /// empty.\n   726:     ///\n   727:     /// This operation should compute in *O*(1) time.\n   728:     ///\n   729:     /// # Examples\n   730:     ///\n   731:     /// ```\n   732:     /// use std::collections::LinkedList;\n   733:     ///",
    "nanvix_source": "   707:     /// let mut list: LinkedList<u32> = LinkedList::new();\n   708:     ///\n   709:     /// list.push_back(0);\n   710:     /// list.push_back(1);\n   711:     /// list.push_back(2);\n   712:     ///\n   713:     /// assert_eq!(list.contains(&0), true);\n   714:     /// assert_eq!(list.contains(&10), false);\n   715:     /// ```\n   716:     #[stable(feature = \"linked_list_contains\", since = \"1.12.0\")]\n   717:     pub fn contains(&self, x: &T) -> bool\n   718:     where\n   719:         T: PartialEq<T>,\n   720:     {\n   721:         self.iter().any(|e| e == x)\n   722:     }\n   723: \n   724:     /// Provides a reference to the front element, or `None` if the list is\n   725:     /// empty.\n   726:     ///\n   727:     /// This operation should compute in *O*(1) time.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::LinkedList::front",
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
    "verification_source": "   728:     ///\n   729:     /// # Examples\n   730:     ///\n   731:     /// ```\n   732:     /// use std::collections::LinkedList;\n   733:     ///\n   734:     /// let mut dl = LinkedList::new();\n   735:     /// assert_eq!(dl.front(), None);\n   736:     ///\n   737:     /// dl.push_front(1);\n   738:     /// assert_eq!(dl.front(), Some(&1));\n   739:     /// ```\n   740:     #[inline]\n   741:     #[must_use]\n   742:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   743:     #[rustc_confusables(\"first\")]\n   744:     pub fn front(&self) -> Option<&T> {\n   745:         unsafe { self.head.as_ref().map(|node| &node.as_ref().element) }\n   746:     }\n   747: \n   748:     /// Provides a mutable reference to the front element, or `None` if the list\n   749:     /// is empty.\n   750:     ///\n   751:     /// This operation should compute in *O*(1) time.\n   752:     ///\n   753:     /// # Examples\n   754:     ///\n   755:     /// ```\n   756:     /// use std::collections::LinkedList;\n   757:     ///\n   758:     /// let mut dl = LinkedList::new();\n   759:     /// assert_eq!(dl.front(), None);\n   760:     ///",
    "nanvix_source": "   734:     /// let mut dl = LinkedList::new();\n   735:     /// assert_eq!(dl.front(), None);\n   736:     ///\n   737:     /// dl.push_front(1);\n   738:     /// assert_eq!(dl.front(), Some(&1));\n   739:     /// ```\n   740:     #[inline]\n   741:     #[must_use]\n   742:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   743:     #[rustc_confusables(\"first\")]\n   744:     pub fn front(&self) -> Option<&T> {\n   745:         unsafe { self.head.as_ref().map(|node| &node.as_ref().element) }\n   746:     }\n   747: \n   748:     /// Provides a mutable reference to the front element, or `None` if the list\n   749:     /// is empty.\n   750:     ///\n   751:     /// This operation should compute in *O*(1) time.\n   752:     ///\n   753:     /// # Examples\n   754:     ///",
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
