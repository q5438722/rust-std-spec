For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::make_contiguous",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "make_contiguous",
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
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2816:     ///\n  2817:     /// let mut buf = VecDeque::new();\n  2818:     ///\n  2819:     /// buf.push_back(2);\n  2820:     /// buf.push_back(1);\n  2821:     /// buf.push_front(3);\n  2822:     ///\n  2823:     /// buf.make_contiguous();\n  2824:     /// if let (slice, &[]) = buf.as_slices() {\n  2825:     ///     // we can now be sure that `slice` contains all elements of the deque,\n  2826:     ///     // while still having immutable access to `buf`.\n  2827:     ///     assert_eq!(buf.len(), slice.len());\n  2828:     ///     assert_eq!(slice, &[3, 2, 1] as &[_]);\n  2829:     /// }\n  2830:     /// ```\n  2831:     #[stable(feature = \"deque_make_contiguous\", since = \"1.48.0\")]\n  2832:     pub fn make_contiguous(&mut self) -> &mut [T] {\n  2833:         if T::IS_ZST {\n  2834:             self.head = 0;\n  2835:         }\n  2836: \n  2837:         if self.is_contiguous() {\n  2838:             unsafe { return slice::from_raw_parts_mut(self.ptr().add(self.head), self.len) }\n  2839:         }\n  2840: \n  2841:         let &mut Self { head, len, .. } = self;\n  2842:         let ptr = self.ptr();\n  2843:         let cap = self.capacity();\n  2844: \n  2845:         let free = cap - len;\n  2846:         let head_len = cap - head;\n  2847:         let tail = len - head_len;\n  2848:         let tail_len = tail;",
    "nanvix_source": "  2886:     ///\n  2887:     /// buf.make_contiguous();\n  2888:     /// if let (slice, &[]) = buf.as_slices() {\n  2889:     ///     // we can now be sure that `slice` contains all elements of the deque,\n  2890:     ///     // while still having immutable access to `buf`.\n  2891:     ///     assert_eq!(buf.len(), slice.len());\n  2892:     ///     assert_eq!(slice, &[3, 2, 1] as &[_]);\n  2893:     /// }\n  2894:     /// ```\n  2895:     #[stable(feature = \"deque_make_contiguous\", since = \"1.48.0\")]\n  2896:     pub fn make_contiguous(&mut self) -> &mut [T] {\n  2897:         if T::IS_ZST {\n  2898:             self.head = WrappedIndex::zero();\n  2899:         }\n  2900: \n  2901:         if self.is_contiguous() {\n  2902:             unsafe {\n  2903:                 return slice::from_raw_parts_mut(self.ptr().add(self.head.as_index()), self.len);\n  2904:             }\n  2905:         }\n  2906: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::push_back_mut",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "push_back_mut",
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
            "value",
            {
              "generic": "T"
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
    "verification_source": "  2213:     }\n  2214: \n  2215:     /// Appends an element to the back of the deque, returning a reference to it.\n  2216:     ///\n  2217:     /// # Examples\n  2218:     ///\n  2219:     /// ```\n  2220:     /// use std::collections::VecDeque;\n  2221:     ///\n  2222:     /// let mut d = VecDeque::from([1, 2, 3]);\n  2223:     /// let x = d.push_back_mut(9);\n  2224:     /// *x += 1;\n  2225:     /// assert_eq!(d.back(), Some(&10));\n  2226:     /// ```\n  2227:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2228:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::push_back` instead\"]\n  2229:     pub fn push_back_mut(&mut self, value: T) -> &mut T {\n  2230:         if self.is_full() {\n  2231:             self.grow();\n  2232:         }\n  2233: \n  2234:         let len = self.len;\n  2235:         self.len += 1;\n  2236:         unsafe { self.buffer_write(self.to_physical_idx(len), value) }\n  2237:     }\n  2238: \n  2239:     /// Prepends all contents of the iterator to the front of the deque.\n  2240:     /// The order of the contents is preserved.\n  2241:     ///\n  2242:     /// To get behavior like [`append`][VecDeque::append] where elements are moved\n  2243:     /// from the other collection to this one, use `self.prepend(other.drain(..))`.\n  2244:     ///\n  2245:     /// # Examples",
    "nanvix_source": "  2283:     /// ```\n  2284:     /// use std::collections::VecDeque;\n  2285:     ///\n  2286:     /// let mut d = VecDeque::from([1, 2, 3]);\n  2287:     /// let x = d.push_back_mut(9);\n  2288:     /// *x += 1;\n  2289:     /// assert_eq!(d.back(), Some(&10));\n  2290:     /// ```\n  2291:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2292:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::push_back` instead\"]\n  2293:     pub fn push_back_mut(&mut self, value: T) -> &mut T {\n  2294:         if self.is_full() {\n  2295:             self.grow();\n  2296:         }\n  2297: \n  2298:         let len = self.len;\n  2299:         self.len += 1;\n  2300:         unsafe { self.buffer_write(self.to_wrapped_index(len), value) }\n  2301:     }\n  2302: \n  2303:     /// Prepends all contents of the iterator to the front of the deque.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::push_front_mut",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "push_front_mut",
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
            "value",
            {
              "generic": "T"
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
    "verification_source": "  2170:     }\n  2171: \n  2172:     /// Prepends an element to the deque, returning a reference to it.\n  2173:     ///\n  2174:     /// # Examples\n  2175:     ///\n  2176:     /// ```\n  2177:     /// use std::collections::VecDeque;\n  2178:     ///\n  2179:     /// let mut d = VecDeque::from([1, 2, 3]);\n  2180:     /// let x = d.push_front_mut(8);\n  2181:     /// *x -= 1;\n  2182:     /// assert_eq!(d.front(), Some(&7));\n  2183:     /// ```\n  2184:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2185:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::push_front` instead\"]\n  2186:     pub fn push_front_mut(&mut self, value: T) -> &mut T {\n  2187:         if self.is_full() {\n  2188:             self.grow();\n  2189:         }\n  2190: \n  2191:         self.head = self.wrap_sub(self.head, 1);\n  2192:         self.len += 1;\n  2193:         // SAFETY: We know that self.head is within range of the deque.\n  2194:         unsafe { self.buffer_write(self.head, value) }\n  2195:     }\n  2196: \n  2197:     /// Appends an element to the back of the deque.\n  2198:     ///\n  2199:     /// # Examples\n  2200:     ///\n  2201:     /// ```\n  2202:     /// use std::collections::VecDeque;",
    "nanvix_source": "  2240:     /// ```\n  2241:     /// use std::collections::VecDeque;\n  2242:     ///\n  2243:     /// let mut d = VecDeque::from([1, 2, 3]);\n  2244:     /// let x = d.push_front_mut(8);\n  2245:     /// *x -= 1;\n  2246:     /// assert_eq!(d.front(), Some(&7));\n  2247:     /// ```\n  2248:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2249:     #[must_use = \"if you don't need a reference to the value, use `VecDeque::push_front` instead\"]\n  2250:     pub fn push_front_mut(&mut self, value: T) -> &mut T {\n  2251:         if self.is_full() {\n  2252:             self.grow();\n  2253:         }\n  2254: \n  2255:         self.head = self.wrap_sub(self.head, 1);\n  2256:         self.len += 1;\n  2257:         // SAFETY: We know that self.head is within range of the deque.\n  2258:         unsafe { self.buffer_write(self.head, value) }\n  2259:     }\n  2260: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::Entry::or_default",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "or_default",
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
                    "lifetime": "'a"
                  },
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1269,
            "path": "Entry"
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
              "name": "K"
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
                          "id": 63,
                          "path": "Default"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:1278",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1269",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "Entry"
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
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   298: \n   299: impl<'a, K: Ord, V: Default, A: Allocator + Clone> Entry<'a, K, V, A> {\n   300:     #[stable(feature = \"entry_or_default\", since = \"1.28.0\")]\n   301:     /// Ensures a value is in the entry by inserting the default value if empty,\n   302:     /// and returns a mutable reference to the value in the entry.\n   303:     ///\n   304:     /// # Examples\n   305:     ///\n   306:     /// ```\n   307:     /// use std::collections::BTreeMap;\n   308:     ///\n   309:     /// let mut map: BTreeMap<&str, Option<usize>> = BTreeMap::new();\n   310:     /// map.entry(\"poneyland\").or_default();\n   311:     ///\n   312:     /// assert_eq!(map[\"poneyland\"], None);\n   313:     /// ```\n   314:     pub fn or_default(self) -> &'a mut V {\n   315:         match self {\n   316:             Occupied(entry) => entry.into_mut(),\n   317:             Vacant(entry) => entry.insert(Default::default()),\n   318:         }\n   319:     }\n   320: }\n   321: \n   322: impl<'a, K: Ord, V, A: Allocator + Clone> VacantEntry<'a, K, V, A> {\n   323:     /// Gets a reference to the key that would be used when inserting a value\n   324:     /// through the VacantEntry.\n   325:     ///\n   326:     /// # Examples\n   327:     ///\n   328:     /// ```\n   329:     /// use std::collections::BTreeMap;\n   330:     ///",
    "nanvix_source": "   353:     /// # Examples\n   354:     ///\n   355:     /// ```\n   356:     /// use std::collections::BTreeMap;\n   357:     ///\n   358:     /// let mut map: BTreeMap<&str, Option<usize>> = BTreeMap::new();\n   359:     /// map.entry(\"poneyland\").or_default();\n   360:     ///\n   361:     /// assert_eq!(map[\"poneyland\"], None);\n   362:     /// ```\n   363:     pub fn or_default(self) -> &'a mut V {\n   364:         match self {\n   365:             Occupied(entry) => entry.into_mut(),\n   366:             Vacant(entry) => entry.insert(Default::default()),\n   367:         }\n   368:     }\n   369: }\n   370: \n   371: impl<'a, K: Ord, V, A: Allocator + Clone> VacantEntry<'a, K, V, A> {\n   372:     /// Gets a reference to the key that would be used when inserting a value\n   373:     /// through the VacantEntry.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::Entry::or_insert",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "or_insert",
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
                    "lifetime": "'a"
                  },
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1269,
            "path": "Entry"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:1276",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1269",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "Entry"
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
              "generic": "V"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   145: \n   146: impl<'a, K: Ord, V, A: Allocator + Clone> Entry<'a, K, V, A> {\n   147:     /// Ensures a value is in the entry by inserting the default if empty, and returns\n   148:     /// a mutable reference to the value in the entry.\n   149:     ///\n   150:     /// # Examples\n   151:     ///\n   152:     /// ```\n   153:     /// use std::collections::BTreeMap;\n   154:     ///\n   155:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   156:     /// map.entry(\"poneyland\").or_insert(12);\n   157:     ///\n   158:     /// assert_eq!(map[\"poneyland\"], 12);\n   159:     /// ```\n   160:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   161:     pub fn or_insert(self, default: V) -> &'a mut V {\n   162:         match self {\n   163:             Occupied(entry) => entry.into_mut(),\n   164:             Vacant(entry) => entry.insert(default),\n   165:         }\n   166:     }\n   167: \n   168:     /// Ensures a value is in the entry by inserting the result of the default function if empty,\n   169:     /// and returns a mutable reference to the value in the entry.\n   170:     ///\n   171:     /// # Examples\n   172:     ///\n   173:     /// ```\n   174:     /// use std::collections::BTreeMap;\n   175:     ///\n   176:     /// let mut map: BTreeMap<&str, String> = BTreeMap::new();\n   177:     /// let s = \"hoho\".to_string();",
    "nanvix_source": "   134:     ///\n   135:     /// ```\n   136:     /// use std::collections::BTreeMap;\n   137:     ///\n   138:     /// let mut map: BTreeMap<&str, usize> = BTreeMap::new();\n   139:     /// map.entry(\"poneyland\").or_insert(12);\n   140:     ///\n   141:     /// assert_eq!(map[\"poneyland\"], 12);\n   142:     /// ```\n   143:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   144:     pub fn or_insert(self, default: V) -> &'a mut V {\n   145:         match self {\n   146:             Occupied(entry) => entry.into_mut(),\n   147:             Vacant(entry) => entry.insert(default),\n   148:         }\n   149:     }\n   150: \n   151:     /// Ensures a value is in the entry by inserting the result of the default function if empty,\n   152:     /// and returns a mutable reference to the value in the entry.\n   153:     ///\n   154:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::btree_map::Entry::or_insert_with",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "parenthesized": {
                            "inputs": [],
                            "output": {
                              "generic": "V"
                            }
                          }
                        },
                        "id": 441,
                        "path": "FnOnce"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "or_insert_with",
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
                    "lifetime": "'a"
                  },
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1269,
            "path": "Entry"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 25,
                          "path": "Clone"
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
        "impl_id": "alloc:1276",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:1269",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "btree",
          "map",
          "entry",
          "Entry"
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
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "generic": "V"
            }
          }
        }
      }
    },
    "verification_source": "   168:     /// Ensures a value is in the entry by inserting the result of the default function if empty,\n   169:     /// and returns a mutable reference to the value in the entry.\n   170:     ///\n   171:     /// # Examples\n   172:     ///\n   173:     /// ```\n   174:     /// use std::collections::BTreeMap;\n   175:     ///\n   176:     /// let mut map: BTreeMap<&str, String> = BTreeMap::new();\n   177:     /// let s = \"hoho\".to_string();\n   178:     ///\n   179:     /// map.entry(\"poneyland\").or_insert_with(|| s);\n   180:     ///\n   181:     /// assert_eq!(map[\"poneyland\"], \"hoho\".to_string());\n   182:     /// ```\n   183:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   184:     pub fn or_insert_with<F: FnOnce() -> V>(self, default: F) -> &'a mut V {\n   185:         match self {\n   186:             Occupied(entry) => entry.into_mut(),\n   187:             Vacant(entry) => entry.insert(default()),\n   188:         }\n   189:     }\n   190: \n   191:     /// Ensures a value is in the entry by inserting, if empty, the result of the default function.\n   192:     ///\n   193:     /// This method allows for generating key-derived values for insertion by providing the default\n   194:     /// function a reference to the key that was moved during the `.entry(key)` method call.\n   195:     ///\n   196:     /// The reference to the moved key is provided so that cloning or copying the key is\n   197:     /// unnecessary, unlike with `.or_insert_with(|| ... )`.\n   198:     ///\n   199:     /// # Examples\n   200:     ///",
    "nanvix_source": "   157:     /// use std::collections::BTreeMap;\n   158:     ///\n   159:     /// let mut map: BTreeMap<&str, String> = BTreeMap::new();\n   160:     /// let s = \"hoho\".to_string();\n   161:     ///\n   162:     /// map.entry(\"poneyland\").or_insert_with(|| s);\n   163:     ///\n   164:     /// assert_eq!(map[\"poneyland\"], \"hoho\".to_string());\n   165:     /// ```\n   166:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   167:     pub fn or_insert_with<F: FnOnce() -> V>(self, default: F) -> &'a mut V {\n   168:         self.or_try_insert_with(|| Result::<_, !>::Ok(default())).unwrap()\n   169:     }\n   170: \n   171:     /// Ensures a value is in the entry by inserting the result of a fallible default function\n   172:     /// if empty, and returns a mutable reference to the value in the entry.\n   173:     ///\n   174:     /// This method works identically to [`or_insert_with`] except that the default function\n   175:     /// should return a `Result` and, in the case of an error, the error is propagated.\n   176:     ///\n   177:     /// [`or_insert_with`]: Self::or_insert_with",
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
