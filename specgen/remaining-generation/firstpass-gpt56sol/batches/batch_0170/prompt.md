For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BinaryHeap::try_reserve_exact",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
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
    "verification_source": "  1248:     /// use std::collections::TryReserveError;\n  1249:     ///\n  1250:     /// fn find_max_slow(data: &[u32]) -> Result<Option<u32>, TryReserveError> {\n  1251:     ///     let mut heap = BinaryHeap::new();\n  1252:     ///\n  1253:     ///     // Pre-reserve the memory, exiting if we can't\n  1254:     ///     heap.try_reserve_exact(data.len())?;\n  1255:     ///\n  1256:     ///     // Now we know this can't OOM in the middle of our complex work\n  1257:     ///     heap.extend(data.iter());\n  1258:     ///\n  1259:     ///     Ok(heap.pop())\n  1260:     /// }\n  1261:     /// # find_max_slow(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1262:     /// ```\n  1263:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1264:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1265:         self.data.try_reserve_exact(additional)\n  1266:     }\n  1267: \n  1268:     /// Tries to reserve capacity for at least `additional` elements more than the\n  1269:     /// current length. The allocator may reserve more space to speculatively\n  1270:     /// avoid frequent allocations. After calling `try_reserve`, capacity will be\n  1271:     /// greater than or equal to `self.len() + additional` if it returns\n  1272:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1273:     /// preserves the contents even if an error occurs.\n  1274:     ///\n  1275:     /// # Errors\n  1276:     ///\n  1277:     /// If the capacity overflows, or the allocator reports a failure, then an error\n  1278:     /// is returned.\n  1279:     ///\n  1280:     /// # Examples",
    "nanvix_source": "  1254:     ///     heap.try_reserve_exact(data.len())?;\n  1255:     ///\n  1256:     ///     // Now we know this can't OOM in the middle of our complex work\n  1257:     ///     heap.extend(data.iter());\n  1258:     ///\n  1259:     ///     Ok(heap.pop())\n  1260:     /// }\n  1261:     /// # find_max_slow(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1262:     /// ```\n  1263:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1264:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1265:         self.data.try_reserve_exact(additional)\n  1266:     }\n  1267: \n  1268:     /// Tries to reserve capacity for at least `additional` elements more than the\n  1269:     /// current length. The allocator may reserve more space to speculatively\n  1270:     /// avoid frequent allocations. After calling `try_reserve`, capacity will be\n  1271:     /// greater than or equal to `self.len() + additional` if it returns\n  1272:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1273:     /// preserves the contents even if an error occurs.\n  1274:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::with_capacity",
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
      "name": "with_capacity",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:982",
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
            "capacity",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 979,
            "path": "BinaryHeap"
          }
        }
      }
    },
    "verification_source": "   519:     ///\n   520:     /// The binary heap will be able to hold at least `capacity` elements without\n   521:     /// reallocating. This method is allowed to allocate for more elements than\n   522:     /// `capacity`. If `capacity` is zero, the binary heap will not allocate.\n   523:     ///\n   524:     /// # Examples\n   525:     ///\n   526:     /// Basic usage:\n   527:     ///\n   528:     /// ```\n   529:     /// use std::collections::BinaryHeap;\n   530:     /// let mut heap = BinaryHeap::with_capacity(10);\n   531:     /// heap.push(4);\n   532:     /// ```\n   533:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   534:     #[must_use]\n   535:     pub fn with_capacity(capacity: usize) -> BinaryHeap<T> {\n   536:         BinaryHeap { data: Vec::with_capacity(capacity) }\n   537:     }\n   538: }\n   539: \n   540: impl<T, A: Allocator> BinaryHeap<T, A> {\n   541:     /// Creates an empty `BinaryHeap` as a max-heap, using `A` as allocator.\n   542:     ///\n   543:     /// # Examples\n   544:     ///\n   545:     /// Basic usage:\n   546:     ///\n   547:     /// ```\n   548:     /// #![feature(allocator_api)]\n   549:     ///\n   550:     /// use std::alloc::System;\n   551:     /// use std::collections::BinaryHeap;",
    "nanvix_source": "   525:     ///\n   526:     /// Basic usage:\n   527:     ///\n   528:     /// ```\n   529:     /// use std::collections::BinaryHeap;\n   530:     /// let mut heap = BinaryHeap::with_capacity(10);\n   531:     /// heap.push(4);\n   532:     /// ```\n   533:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   534:     #[must_use]\n   535:     pub fn with_capacity(capacity: usize) -> BinaryHeap<T> {\n   536:         BinaryHeap { data: Vec::with_capacity(capacity) }\n   537:     }\n   538: }\n   539: \n   540: impl<T, A: Allocator> BinaryHeap<T, A> {\n   541:     /// Creates an empty `BinaryHeap` as a max-heap, using `A` as allocator.\n   542:     ///\n   543:     /// # Examples\n   544:     ///\n   545:     /// Basic usage:",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::capacity",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   981:         unsafe { ptr::swap(self.ptr().add(ri), self.ptr().add(rj)) }\n   982:     }\n   983: \n   984:     /// Returns the number of elements the deque can hold without\n   985:     /// reallocating.\n   986:     ///\n   987:     /// # Examples\n   988:     ///\n   989:     /// ```\n   990:     /// use std::collections::VecDeque;\n   991:     ///\n   992:     /// let buf: VecDeque<i32> = VecDeque::with_capacity(10);\n   993:     /// assert!(buf.capacity() >= 10);\n   994:     /// ```\n   995:     #[inline]\n   996:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   997:     pub fn capacity(&self) -> usize {\n   998:         if T::IS_ZST { usize::MAX } else { self.buf.capacity() }\n   999:     }\n  1000: \n  1001:     /// Reserves the minimum capacity for at least `additional` more elements to be inserted in the\n  1002:     /// given deque. Does nothing if the capacity is already sufficient.\n  1003:     ///\n  1004:     /// Note that the allocator may give the collection more space than it requests. Therefore\n  1005:     /// capacity can not be relied upon to be precisely minimal. Prefer [`reserve`] if future\n  1006:     /// insertions are expected.\n  1007:     ///\n  1008:     /// # Panics\n  1009:     ///\n  1010:     /// Panics if the new capacity overflows `usize`.\n  1011:     ///\n  1012:     /// # Examples\n  1013:     ///",
    "nanvix_source": "  1040:     /// # Examples\n  1041:     ///\n  1042:     /// ```\n  1043:     /// use std::collections::VecDeque;\n  1044:     ///\n  1045:     /// let buf: VecDeque<i32> = VecDeque::with_capacity(10);\n  1046:     /// assert!(buf.capacity() >= 10);\n  1047:     /// ```\n  1048:     #[inline]\n  1049:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1050:     pub fn capacity(&self) -> usize {\n  1051:         if T::IS_ZST { usize::MAX } else { self.buf.capacity() }\n  1052:     }\n  1053: \n  1054:     /// Reserves the minimum capacity for at least `additional` more elements to be inserted in the\n  1055:     /// given deque. Does nothing if the capacity is already sufficient.\n  1056:     ///\n  1057:     /// Note that the allocator may give the collection more space than it requests. Therefore\n  1058:     /// capacity can not be relied upon to be precisely minimal. Prefer [`reserve`] if future\n  1059:     /// insertions are expected.\n  1060:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::reserve_exact",
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
      "name": "reserve_exact",
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1008:     /// # Panics\n  1009:     ///\n  1010:     /// Panics if the new capacity overflows `usize`.\n  1011:     ///\n  1012:     /// # Examples\n  1013:     ///\n  1014:     /// ```\n  1015:     /// use std::collections::VecDeque;\n  1016:     ///\n  1017:     /// let mut buf: VecDeque<i32> = [1].into();\n  1018:     /// buf.reserve_exact(10);\n  1019:     /// assert!(buf.capacity() >= 11);\n  1020:     /// ```\n  1021:     ///\n  1022:     /// [`reserve`]: VecDeque::reserve\n  1023:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1024:     pub fn reserve_exact(&mut self, additional: usize) {\n  1025:         let new_cap = self.len.checked_add(additional).expect(\"capacity overflow\");\n  1026:         let old_cap = self.capacity();\n  1027: \n  1028:         if new_cap > old_cap {\n  1029:             self.buf.reserve_exact(self.len, additional);\n  1030:             unsafe {\n  1031:                 self.handle_capacity_increase(old_cap);\n  1032:             }\n  1033:         }\n  1034:     }\n  1035: \n  1036:     /// Reserves capacity for at least `additional` more elements to be inserted in the given\n  1037:     /// deque. The collection may reserve more space to speculatively avoid frequent reallocations.\n  1038:     ///\n  1039:     /// # Panics\n  1040:     ///",
    "nanvix_source": "  1067:     /// ```\n  1068:     /// use std::collections::VecDeque;\n  1069:     ///\n  1070:     /// let mut buf: VecDeque<i32> = [1].into();\n  1071:     /// buf.reserve_exact(10);\n  1072:     /// assert!(buf.capacity() >= 11);\n  1073:     /// ```\n  1074:     ///\n  1075:     /// [`reserve`]: VecDeque::reserve\n  1076:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1077:     pub fn reserve_exact(&mut self, additional: usize) {\n  1078:         let new_cap = self.len.checked_add(additional).expect(\"capacity overflow\");\n  1079:         let old_cap = self.capacity();\n  1080: \n  1081:         if new_cap > old_cap {\n  1082:             self.buf.reserve_exact(self.len, additional);\n  1083:             unsafe {\n  1084:                 self.handle_capacity_increase(old_cap);\n  1085:             }\n  1086:         }\n  1087:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::shrink_to",
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
    "verification_source": "  1194:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1195:     ///\n  1196:     /// # Examples\n  1197:     ///\n  1198:     /// ```\n  1199:     /// use std::collections::VecDeque;\n  1200:     ///\n  1201:     /// let mut buf = VecDeque::with_capacity(15);\n  1202:     /// buf.extend(0..4);\n  1203:     /// assert_eq!(buf.capacity(), 15);\n  1204:     /// buf.shrink_to(6);\n  1205:     /// assert!(buf.capacity() >= 6);\n  1206:     /// buf.shrink_to(0);\n  1207:     /// assert!(buf.capacity() >= 4);\n  1208:     /// ```\n  1209:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1210:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1211:         let target_cap = min_capacity.max(self.len);\n  1212: \n  1213:         // never shrink ZSTs\n  1214:         if T::IS_ZST || self.capacity() <= target_cap {\n  1215:             return;\n  1216:         }\n  1217: \n  1218:         // There are three cases of interest:\n  1219:         //   All elements are out of desired bounds\n  1220:         //   Elements are contiguous, and tail is out of desired bounds\n  1221:         //   Elements are discontiguous\n  1222:         //\n  1223:         // At all other times, element positions are unaffected.\n  1224: \n  1225:         // `head` and `len` are at most `isize::MAX` and `target_cap < self.capacity()`, so nothing can\n  1226:         // overflow.",
    "nanvix_source": "  1253:     ///\n  1254:     /// let mut buf = VecDeque::with_capacity(15);\n  1255:     /// buf.extend(0..4);\n  1256:     /// assert_eq!(buf.capacity(), 15);\n  1257:     /// buf.shrink_to(6);\n  1258:     /// assert!(buf.capacity() >= 6);\n  1259:     /// buf.shrink_to(0);\n  1260:     /// assert!(buf.capacity() >= 4);\n  1261:     /// ```\n  1262:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1263:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1264:         let target_cap = min_capacity.max(self.len);\n  1265: \n  1266:         // never shrink ZSTs\n  1267:         if T::IS_ZST || self.capacity() <= target_cap {\n  1268:             return;\n  1269:         }\n  1270: \n  1271:         // There are three cases of interest:\n  1272:         //   All elements are out of desired bounds\n  1273:         //   Elements are contiguous, and tail is out of desired bounds",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::shrink_to_fit",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1169:     ///\n  1170:     /// It will drop down as close as possible to the length but the allocator may still inform the\n  1171:     /// deque that there is space for a few more elements.\n  1172:     ///\n  1173:     /// # Examples\n  1174:     ///\n  1175:     /// ```\n  1176:     /// use std::collections::VecDeque;\n  1177:     ///\n  1178:     /// let mut buf = VecDeque::with_capacity(15);\n  1179:     /// buf.extend(0..4);\n  1180:     /// assert_eq!(buf.capacity(), 15);\n  1181:     /// buf.shrink_to_fit();\n  1182:     /// assert!(buf.capacity() >= 4);\n  1183:     /// ```\n  1184:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1185:     pub fn shrink_to_fit(&mut self) {\n  1186:         self.shrink_to(0);\n  1187:     }\n  1188: \n  1189:     /// Shrinks the capacity of the deque with a lower bound.\n  1190:     ///\n  1191:     /// The capacity will remain at least as large as both the length\n  1192:     /// and the supplied value.\n  1193:     ///\n  1194:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1195:     ///\n  1196:     /// # Examples\n  1197:     ///\n  1198:     /// ```\n  1199:     /// use std::collections::VecDeque;\n  1200:     ///\n  1201:     /// let mut buf = VecDeque::with_capacity(15);",
    "nanvix_source": "  1228:     /// ```\n  1229:     /// use std::collections::VecDeque;\n  1230:     ///\n  1231:     /// let mut buf = VecDeque::with_capacity(15);\n  1232:     /// buf.extend(0..4);\n  1233:     /// assert_eq!(buf.capacity(), 15);\n  1234:     /// buf.shrink_to_fit();\n  1235:     /// assert!(buf.capacity() >= 4);\n  1236:     /// ```\n  1237:     #[stable(feature = \"deque_extras_15\", since = \"1.5.0\")]\n  1238:     pub fn shrink_to_fit(&mut self) {\n  1239:         self.shrink_to(0);\n  1240:     }\n  1241: \n  1242:     /// Shrinks the capacity of the deque with a lower bound.\n  1243:     ///\n  1244:     /// The capacity will remain at least as large as both the length\n  1245:     /// and the supplied value.\n  1246:     ///\n  1247:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1248:     ///",
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
