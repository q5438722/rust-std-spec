For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::vec::Vec::insert_mut",
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
      "name": "insert_mut",
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
            "index",
            {
              "primitive": "usize"
            }
          ],
          [
            "element",
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
    "verification_source": "  2287:     /// let mut vec = vec![1, 3, 5, 9];\n  2288:     /// let x = vec.insert_mut(3, 6);\n  2289:     /// *x += 1;\n  2290:     /// assert_eq!(vec, [1, 3, 5, 7, 9]);\n  2291:     /// ```\n  2292:     ///\n  2293:     /// # Time complexity\n  2294:     ///\n  2295:     /// Takes *O*([`Vec::len`]) time. All items after the insertion index must be\n  2296:     /// shifted to the right. In the worst case, all elements are shifted when\n  2297:     /// the insertion index is 0.\n  2298:     #[cfg(not(no_global_oom_handling))]\n  2299:     #[inline]\n  2300:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2301:     #[track_caller]\n  2302:     #[must_use = \"if you don't need a reference to the value, use `Vec::insert` instead\"]\n  2303:     pub fn insert_mut(&mut self, index: usize, element: T) -> &mut T {\n  2304:         #[cold]\n  2305:         #[cfg_attr(not(panic = \"immediate-abort\"), inline(never))]\n  2306:         #[track_caller]\n  2307:         #[optimize(size)]\n  2308:         fn assert_failed(index: usize, len: usize) -> ! {\n  2309:             panic!(\"insertion index (is {index}) should be <= len (is {len})\");\n  2310:         }\n  2311: \n  2312:         let len = self.len();\n  2313:         if index > len {\n  2314:             assert_failed(index, len);\n  2315:         }\n  2316: \n  2317:         // space for the new element\n  2318:         if len == self.buf.capacity() {\n  2319:             self.buf.grow_one();",
    "nanvix_source": "  2330:     /// # Time complexity\n  2331:     ///\n  2332:     /// Takes *O*([`Vec::len`]) time. All items after the insertion index must be\n  2333:     /// shifted to the right. In the worst case, all elements are shifted when\n  2334:     /// the insertion index is 0.\n  2335:     #[cfg(not(no_global_oom_handling))]\n  2336:     #[inline]\n  2337:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  2338:     #[track_caller]\n  2339:     #[must_use = \"if you don't need a reference to the value, use `Vec::insert` instead\"]\n  2340:     pub fn insert_mut(&mut self, index: usize, element: T) -> &mut T {\n  2341:         #[cold]\n  2342:         #[cfg_attr(not(panic = \"immediate-abort\"), inline(never))]\n  2343:         #[track_caller]\n  2344:         #[optimize(size)]\n  2345:         fn assert_failed(index: usize, len: usize) -> ! {\n  2346:             panic!(\"insertion index (is {index}) should be <= len (is {len})\");\n  2347:         }\n  2348: \n  2349:         let len = self.len();\n  2350:         if index > len {",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::leak",
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
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "outlives": "'a"
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "A"
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
      "name": "leak",
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
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  3167:     ///\n  3168:     /// # Examples\n  3169:     ///\n  3170:     /// Simple usage:\n  3171:     ///\n  3172:     /// ```\n  3173:     /// let x = vec![1, 2, 3];\n  3174:     /// let static_ref: &'static mut [usize] = x.leak();\n  3175:     /// static_ref[0] += 1;\n  3176:     /// assert_eq!(static_ref, &[2, 2, 3]);\n  3177:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  3178:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  3179:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  3180:     /// ```\n  3181:     #[stable(feature = \"vec_leak\", since = \"1.47.0\")]\n  3182:     #[inline]\n  3183:     pub fn leak<'a>(self) -> &'a mut [T]\n  3184:     where\n  3185:         A: 'a,\n  3186:     {\n  3187:         let mut me = ManuallyDrop::new(self);\n  3188:         unsafe { slice::from_raw_parts_mut(me.as_mut_ptr(), me.len) }\n  3189:     }\n  3190: \n  3191:     /// Returns the remaining spare capacity of the vector as a slice of\n  3192:     /// `MaybeUninit<T>`.\n  3193:     ///\n  3194:     /// The returned slice can be used to fill the vector with data (e.g. by\n  3195:     /// reading from a file) before marking the data as initialized using the\n  3196:     /// [`set_len`] method.\n  3197:     ///\n  3198:     /// [`set_len`]: Vec::set_len\n  3199:     ///",
    "nanvix_source": "  3214:     /// let x = vec![1, 2, 3];\n  3215:     /// let static_ref: &'static mut [usize] = x.leak();\n  3216:     /// static_ref[0] += 1;\n  3217:     /// assert_eq!(static_ref, &[2, 2, 3]);\n  3218:     /// # // FIXME(https://github.com/rust-lang/miri/issues/3670):\n  3219:     /// # // use -Zmiri-disable-leak-check instead of unleaking in tests meant to leak.\n  3220:     /// # drop(unsafe { Box::from_raw(static_ref) });\n  3221:     /// ```\n  3222:     #[stable(feature = \"vec_leak\", since = \"1.47.0\")]\n  3223:     #[inline]\n  3224:     pub fn leak<'a>(self) -> &'a mut [T]\n  3225:     where\n  3226:         A: 'a,\n  3227:     {\n  3228:         let mut me = ManuallyDrop::new(self);\n  3229:         unsafe { slice::from_raw_parts_mut(me.as_mut_ptr(), me.len) }\n  3230:     }\n  3231: \n  3232:     /// Returns the remaining spare capacity of the vector as a slice of\n  3233:     /// `MaybeUninit<T>`.\n  3234:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::push_mut",
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
      "name": "push_mut",
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
                        "modifier": "maybe_const",
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
        "impl_id": "alloc:4895",
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
    "verification_source": "  1019:     /// assert_eq!(vec, [1, 2, 3]);\n  1020:     ///\n  1021:     /// let last = vec.push_mut(3);\n  1022:     /// *last += 1;\n  1023:     /// assert_eq!(vec, [1, 2, 3, 4]);\n  1024:     /// ```\n  1025:     ///\n  1026:     /// # Time complexity\n  1027:     ///\n  1028:     /// Takes amortized *O*(1) time. If the vector's length would exceed its\n  1029:     /// capacity after the push, *O*(*capacity*) time is taken to copy the\n  1030:     /// vector's elements to a larger allocation. This expensive operation is\n  1031:     /// offset by the *capacity* *O*(1) insertions it allows.\n  1032:     #[inline]\n  1033:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  1034:     #[must_use = \"if you don't need a reference to the value, use `Vec::push` instead\"]\n  1035:     pub fn push_mut(&mut self, value: T) -> &mut T {\n  1036:         // Inform codegen that the length does not change across grow_one().\n  1037:         let len = self.len;\n  1038:         // This will panic or abort if we would allocate > isize::MAX bytes\n  1039:         // or if the length increment would overflow for zero-sized types.\n  1040:         if len == self.buf.capacity() {\n  1041:             self.buf.grow_one();\n  1042:         }\n  1043:         unsafe {\n  1044:             let end = self.as_mut_ptr().add(len);\n  1045:             ptr::write(end, value);\n  1046:             self.len = len + 1;\n  1047:             // SAFETY: We just wrote a value to the pointer that will live the lifetime of the reference.\n  1048:             &mut *end\n  1049:         }\n  1050:     }\n  1051: }",
    "nanvix_source": "  1023:     ///\n  1024:     /// # Time complexity\n  1025:     ///\n  1026:     /// Takes amortized *O*(1) time. If the vector's length would exceed its\n  1027:     /// capacity after the push, *O*(*capacity*) time is taken to copy the\n  1028:     /// vector's elements to a larger allocation. This expensive operation is\n  1029:     /// offset by the *capacity* *O*(1) insertions it allows.\n  1030:     #[inline]\n  1031:     #[stable(feature = \"push_mut\", since = \"1.95.0\")]\n  1032:     #[must_use = \"if you don't need a reference to the value, use `Vec::push` instead\"]\n  1033:     pub fn push_mut(&mut self, value: T) -> &mut T {\n  1034:         // Inform codegen that the length does not change across grow_one().\n  1035:         let len = self.len;\n  1036:         // This will panic or abort if we would allocate > isize::MAX bytes\n  1037:         // or if the length increment would overflow for zero-sized types.\n  1038:         if len == self.buf.capacity() {\n  1039:             self.buf.grow_one();\n  1040:         }\n  1041:         unsafe {\n  1042:             let end = self.as_mut_ptr().add(len);\n  1043:             ptr::write(end, value);",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::vec::Vec::spare_capacity_mut",
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
      "name": "spare_capacity_mut",
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
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
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
                  "id": 431,
                  "path": "MaybeUninit"
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "  3205:     ///\n  3206:     /// // Fill in the first 3 elements.\n  3207:     /// let uninit = v.spare_capacity_mut();\n  3208:     /// uninit[0].write(0);\n  3209:     /// uninit[1].write(1);\n  3210:     /// uninit[2].write(2);\n  3211:     ///\n  3212:     /// // Mark the first 3 elements of the vector as being initialized.\n  3213:     /// unsafe {\n  3214:     ///     v.set_len(3);\n  3215:     /// }\n  3216:     ///\n  3217:     /// assert_eq!(&v, &[0, 1, 2]);\n  3218:     /// ```\n  3219:     #[stable(feature = \"vec_spare_capacity\", since = \"1.60.0\")]\n  3220:     #[inline]\n  3221:     pub fn spare_capacity_mut(&mut self) -> &mut [MaybeUninit<T>] {\n  3222:         // Note:\n  3223:         // This method is not implemented in terms of `split_at_spare_mut`,\n  3224:         // to prevent invalidation of pointers to the buffer.\n  3225:         unsafe {\n  3226:             slice::from_raw_parts_mut(\n  3227:                 self.as_mut_ptr().add(self.len) as *mut MaybeUninit<T>,\n  3228:                 self.buf.capacity() - self.len,\n  3229:             )\n  3230:         }\n  3231:     }\n  3232: \n  3233:     /// Returns vector content as a slice of `T`, along with the remaining spare\n  3234:     /// capacity of the vector as a slice of `MaybeUninit<T>`.\n  3235:     ///\n  3236:     /// The returned spare capacity slice can be used to fill the vector with data\n  3237:     /// (e.g. by reading from a file) before marking the data as initialized using",
    "nanvix_source": "  3252:     ///\n  3253:     /// // Mark the first 3 elements of the vector as being initialized.\n  3254:     /// unsafe {\n  3255:     ///     v.set_len(3);\n  3256:     /// }\n  3257:     ///\n  3258:     /// assert_eq!(&v, &[0, 1, 2]);\n  3259:     /// ```\n  3260:     #[stable(feature = \"vec_spare_capacity\", since = \"1.60.0\")]\n  3261:     #[inline]\n  3262:     pub fn spare_capacity_mut(&mut self) -> &mut [MaybeUninit<T>] {\n  3263:         // Note:\n  3264:         // This method is not implemented in terms of `split_at_spare_mut`,\n  3265:         // to prevent invalidation of pointers to the buffer.\n  3266:         unsafe {\n  3267:             slice::from_raw_parts_mut(\n  3268:                 self.as_mut_ptr().add(self.len) as *mut MaybeUninit<T>,\n  3269:                 self.buf.capacity() - self.len,\n  3270:             )\n  3271:         }\n  3272:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::IntoIter::as_mut_slice",
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
      "name": "as_mut_slice",
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
                    "const": {
                      "expr": "N",
                      "is_literal": false,
                      "value": null
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9764,
            "path": "IntoIter"
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
                "const": {
                  "default": null,
                  "type": {
                    "primitive": "usize"
                  }
                }
              },
              "name": "N"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24280",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9764",
        "resolved_owner_path": [
          "core",
          "array",
          "iter",
          "IntoIter"
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
    "verification_source": "   206:     pub const fn empty() -> Self {\n   207:         let inner = InnerSized::empty();\n   208:         IntoIter { inner: ManuallyDrop::new(inner) }\n   209:     }\n   210: \n   211:     /// Returns an immutable slice of all elements that have not been yielded\n   212:     /// yet.\n   213:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   214:     #[inline]\n   215:     pub fn as_slice(&self) -> &[T] {\n   216:         self.unsize().as_slice()\n   217:     }\n   218: \n   219:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   220:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   221:     #[inline]\n   222:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   223:         self.unsize_mut().as_mut_slice()\n   224:     }\n   225: }\n   226: \n   227: #[stable(feature = \"array_value_iter_default\", since = \"1.89.0\")]\n   228: impl<T, const N: usize> Default for IntoIter<T, N> {\n   229:     fn default() -> Self {\n   230:         IntoIter::empty()\n   231:     }\n   232: }\n   233: \n   234: #[stable(feature = \"array_value_iter_impls\", since = \"1.40.0\")]\n   235: impl<T, const N: usize> Iterator for IntoIter<T, N> {\n   236:     type Item = T;\n   237: \n   238:     #[inline]",
    "nanvix_source": "   218:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   219:     #[inline]\n   220:     pub fn as_slice(&self) -> &[T] {\n   221:         self.unsize().as_slice()\n   222:     }\n   223: \n   224:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   225:     #[stable(feature = \"array_value_iter\", since = \"1.51.0\")]\n   226:     #[inline]\n   227:     #[rustc_const_unstable(feature = \"const_iter\", issue = \"92476\")]\n   228:     pub const fn as_mut_slice(&mut self) -> &mut [T] {\n   229:         self.unsize_mut().as_mut_slice()\n   230:     }\n   231: }\n   232: \n   233: #[stable(feature = \"array_value_iter_default\", since = \"1.89.0\")]\n   234: impl<T, const N: usize> Default for IntoIter<T, N> {\n   235:     fn default() -> Self {\n   236:         IntoIter::empty()\n   237:     }\n   238: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::array::as_mut_slice",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
      "name": "as_mut_slice",
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
          "array": {
            "len": "N",
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            },
            {
              "kind": {
                "const": {
                  "default": null,
                  "type": {
                    "primitive": "usize"
                  }
                }
              },
              "name": "N"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51748",
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
    "verification_source": "   633:         // SAFETY: try_from_fn calls `f` N times.\n   634:         let mut f = unsafe { drain::Drain::new(&mut me, &mut f) };\n   635:         try_from_fn(&mut f)\n   636:     }\n   637: \n   638:     /// Returns a slice containing the entire array. Equivalent to `&s[..]`.\n   639:     #[stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   640:     #[rustc_const_stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   641:     pub const fn as_slice(&self) -> &[T] {\n   642:         self\n   643:     }\n   644: \n   645:     /// Returns a mutable slice containing the entire array. Equivalent to\n   646:     /// `&mut s[..]`.\n   647:     #[stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   648:     #[rustc_const_stable(feature = \"const_array_as_mut_slice\", since = \"1.89.0\")]\n   649:     pub const fn as_mut_slice(&mut self) -> &mut [T] {\n   650:         self\n   651:     }\n   652: \n   653:     /// Borrows each element and returns an array of references with the same\n   654:     /// size as `self`.\n   655:     ///\n   656:     ///\n   657:     /// # Example\n   658:     ///\n   659:     /// ```\n   660:     /// let floats = [3.1, 2.7, -1.0];\n   661:     /// let float_refs: [&f64; 3] = floats.each_ref();\n   662:     /// assert_eq!(float_refs, [&3.1, &2.7, &-1.0]);\n   663:     /// ```\n   664:     ///\n   665:     /// This method is particularly useful if combined with other methods, like",
    "nanvix_source": "   648:     #[stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   649:     #[rustc_const_stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   650:     pub const fn as_slice(&self) -> &[T] {\n   651:         self\n   652:     }\n   653: \n   654:     /// Returns a mutable slice containing the entire array. Equivalent to\n   655:     /// `&mut s[..]`.\n   656:     #[stable(feature = \"array_as_slice\", since = \"1.57.0\")]\n   657:     #[rustc_const_stable(feature = \"const_array_as_mut_slice\", since = \"1.89.0\")]\n   658:     pub const fn as_mut_slice(&mut self) -> &mut [T] {\n   659:         self\n   660:     }\n   661: \n   662:     /// Borrows each element and returns an array of references with the same\n   663:     /// size as `self`.\n   664:     ///\n   665:     ///\n   666:     /// # Example\n   667:     ///\n   668:     /// ```",
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
