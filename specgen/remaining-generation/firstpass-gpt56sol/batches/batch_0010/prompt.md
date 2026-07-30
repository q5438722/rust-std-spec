For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::Atomic::fetch_or",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "fetch_or",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2345:     ///\n  2346:     /// let pointer = &mut 3i64 as *mut i64;\n  2347:     ///\n  2348:     /// let atom = AtomicPtr::<i64>::new(pointer);\n  2349:     /// // Tag the bottom bit of the pointer.\n  2350:     /// assert_eq!(atom.fetch_or(1, Ordering::Relaxed).addr() & 1, 0);\n  2351:     /// // Extract and untag.\n  2352:     /// let tagged = atom.load(Ordering::Relaxed);\n  2353:     /// assert_eq!(tagged.addr() & 1, 1);\n  2354:     /// assert_eq!(tagged.map_addr(|p| p & !1), pointer);\n  2355:     /// ```\n  2356:     #[inline]\n  2357:     #[cfg(target_has_atomic = \"ptr\")]\n  2358:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2359:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2360:     #[rustc_should_not_be_called_on_const_items]\n  2361:     pub fn fetch_or(&self, val: usize, order: Ordering) -> *mut T {\n  2362:         // SAFETY: data races are prevented by atomic intrinsics.\n  2363:         unsafe { atomic_or(self.as_ptr(), val, order).cast() }\n  2364:     }\n  2365: \n  2366:     /// Performs a bitwise \"and\" operation on the address of the current\n  2367:     /// pointer, and the argument `val`, and stores a pointer with provenance of\n  2368:     /// the current pointer and the resulting address.\n  2369:     ///\n  2370:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2371:     /// `ptr = ptr.map_addr(|a| a & val)`. This can be used in tagged\n  2372:     /// pointer schemes to atomically unset tag bits.\n  2373:     ///\n  2374:     /// **Caveat**: This operation returns the previous value. To compute the\n  2375:     /// stored value without losing provenance, you may use [`map_addr`]. For\n  2376:     /// example: `a.fetch_and(val).map_addr(|a| a & val)`.\n  2377:     ///",
    "nanvix_source": "  2340:     /// // Extract and untag.\n  2341:     /// let tagged = atom.load(Ordering::Relaxed);\n  2342:     /// assert_eq!(tagged.addr() & 1, 1);\n  2343:     /// assert_eq!(tagged.map_addr(|p| p & !1), pointer);\n  2344:     /// ```\n  2345:     #[inline]\n  2346:     #[cfg(target_has_atomic = \"ptr\")]\n  2347:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2348:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2349:     #[rustc_should_not_be_called_on_const_items]\n  2350:     pub fn fetch_or(&self, val: usize, order: Ordering) -> *mut T {\n  2351:         // SAFETY: data races are prevented by atomic intrinsics.\n  2352:         unsafe { atomic_or(self.as_ptr(), val, order).cast() }\n  2353:     }\n  2354: \n  2355:     /// Performs a bitwise \"and\" operation on the address of the current\n  2356:     /// pointer, and the argument `val`, and stores a pointer with provenance of\n  2357:     /// the current pointer and the resulting address.\n  2358:     ///\n  2359:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2360:     /// `ptr = ptr.map_addr(|a| a & val)`. This can be used in tagged",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_ptr_add",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality"
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
      "name": "fetch_ptr_add",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2178:     ///\n  2179:     /// # Examples\n  2180:     ///\n  2181:     /// ```\n  2182:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2183:     ///\n  2184:     /// let atom = AtomicPtr::<i64>::new(core::ptr::null_mut());\n  2185:     /// assert_eq!(atom.fetch_ptr_add(1, Ordering::Relaxed).addr(), 0);\n  2186:     /// // Note: units of `size_of::<i64>()`.\n  2187:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), 8);\n  2188:     /// ```\n  2189:     #[inline]\n  2190:     #[cfg(target_has_atomic = \"ptr\")]\n  2191:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2192:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2193:     #[rustc_should_not_be_called_on_const_items]\n  2194:     pub fn fetch_ptr_add(&self, val: usize, order: Ordering) -> *mut T {\n  2195:         self.fetch_byte_add(val.wrapping_mul(size_of::<T>()), order)\n  2196:     }\n  2197: \n  2198:     /// Offsets the pointer's address by subtracting `val` (in units of `T`),\n  2199:     /// returning the previous pointer.\n  2200:     ///\n  2201:     /// This is equivalent to using [`wrapping_sub`] to atomically perform the\n  2202:     /// equivalent of `ptr = ptr.wrapping_sub(val);`.\n  2203:     ///\n  2204:     /// This method operates in units of `T`, which means that it cannot be used\n  2205:     /// to offset the pointer by an amount which is not a multiple of\n  2206:     /// `size_of::<T>()`. This can sometimes be inconvenient, as you may want to\n  2207:     /// work with a deliberately misaligned pointer. In such cases, you may use\n  2208:     /// the [`fetch_byte_sub`](Self::fetch_byte_sub) method instead.\n  2209:     ///\n  2210:     /// `fetch_ptr_sub` takes an [`Ordering`] argument which describes the memory",
    "nanvix_source": "  2173:     /// let atom = AtomicPtr::<i64>::new(core::ptr::null_mut());\n  2174:     /// assert_eq!(atom.fetch_ptr_add(1, Ordering::Relaxed).addr(), 0);\n  2175:     /// // Note: units of `size_of::<i64>()`.\n  2176:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), 8);\n  2177:     /// ```\n  2178:     #[inline]\n  2179:     #[cfg(target_has_atomic = \"ptr\")]\n  2180:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2181:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2182:     #[rustc_should_not_be_called_on_const_items]\n  2183:     pub fn fetch_ptr_add(&self, val: usize, order: Ordering) -> *mut T {\n  2184:         self.fetch_byte_add(val.wrapping_mul(size_of::<T>()), order)\n  2185:     }\n  2186: \n  2187:     /// Offsets the pointer's address by subtracting `val` (in units of `T`),\n  2188:     /// returning the previous pointer.\n  2189:     ///\n  2190:     /// This is equivalent to using [`wrapping_sub`] to atomically perform the\n  2191:     /// equivalent of `ptr = ptr.wrapping_sub(val);`.\n  2192:     ///\n  2193:     /// This method operates in units of `T`, which means that it cannot be used",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_ptr_sub",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality"
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
      "name": "fetch_ptr_sub",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2223:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2224:     ///\n  2225:     /// let array = [1i32, 2i32];\n  2226:     /// let atom = AtomicPtr::new(array.as_ptr().wrapping_add(1) as *mut _);\n  2227:     ///\n  2228:     /// assert!(core::ptr::eq(\n  2229:     ///     atom.fetch_ptr_sub(1, Ordering::Relaxed),\n  2230:     ///     &array[1],\n  2231:     /// ));\n  2232:     /// assert!(core::ptr::eq(atom.load(Ordering::Relaxed), &array[0]));\n  2233:     /// ```\n  2234:     #[inline]\n  2235:     #[cfg(target_has_atomic = \"ptr\")]\n  2236:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2237:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2238:     #[rustc_should_not_be_called_on_const_items]\n  2239:     pub fn fetch_ptr_sub(&self, val: usize, order: Ordering) -> *mut T {\n  2240:         self.fetch_byte_sub(val.wrapping_mul(size_of::<T>()), order)\n  2241:     }\n  2242: \n  2243:     /// Offsets the pointer's address by adding `val` *bytes*, returning the\n  2244:     /// previous pointer.\n  2245:     ///\n  2246:     /// This is equivalent to using [`wrapping_byte_add`] to atomically\n  2247:     /// perform `ptr = ptr.wrapping_byte_add(val)`.\n  2248:     ///\n  2249:     /// `fetch_byte_add` takes an [`Ordering`] argument which describes the\n  2250:     /// memory ordering of this operation. All ordering modes are possible. Note\n  2251:     /// that using [`Acquire`] makes the store part of this operation\n  2252:     /// [`Relaxed`], and using [`Release`] makes the load part [`Relaxed`].\n  2253:     ///\n  2254:     /// **Note**: This method is only available on platforms that support atomic\n  2255:     /// operations on [`AtomicPtr`].",
    "nanvix_source": "  2218:     ///     atom.fetch_ptr_sub(1, Ordering::Relaxed),\n  2219:     ///     &array[1],\n  2220:     /// ));\n  2221:     /// assert!(core::ptr::eq(atom.load(Ordering::Relaxed), &array[0]));\n  2222:     /// ```\n  2223:     #[inline]\n  2224:     #[cfg(target_has_atomic = \"ptr\")]\n  2225:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2226:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2227:     #[rustc_should_not_be_called_on_const_items]\n  2228:     pub fn fetch_ptr_sub(&self, val: usize, order: Ordering) -> *mut T {\n  2229:         self.fetch_byte_sub(val.wrapping_mul(size_of::<T>()), order)\n  2230:     }\n  2231: \n  2232:     /// Offsets the pointer's address by adding `val` *bytes*, returning the\n  2233:     /// previous pointer.\n  2234:     ///\n  2235:     /// This is equivalent to using [`wrapping_byte_add`] to atomically\n  2236:     /// perform `ptr = ptr.wrapping_byte_add(val)`.\n  2237:     ///\n  2238:     /// `fetch_byte_add` takes an [`Ordering`] argument which describes the",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_sub",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "multiple_rust_declarations_share_path"
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
      "name": "fetch_sub",
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
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29500",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "u8"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "u8"
        }
      }
    },
    "verification_source": "  3624:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3625:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3626:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3627:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3628:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3632:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3633:     \"i8\",\n  3634:     \"\",\n  3635:     atomic_min, atomic_max,\n  3636:     1,\n  3637:     i8 AtomicI8\n  3638: }\n  3639: #[cfg(target_has_atomic_load_store = \"8\")]\n  3640: atomic_int! {\n  3641:     cfg(target_has_atomic = \"8\"),\n  3642:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3643:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3644:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3645:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3646:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3647:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3648:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3649:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3650:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3651:     \"u8\",\n  3652:     \"\",\n  3653:     atomic_umin, atomic_umax,\n  3654:     1,\n  3655:     u8 AtomicU8\n  3656: }",
    "nanvix_source": "  3616:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3617:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3618:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3619:     \"i8\",\n  3620:     \"\",\n  3621:     atomic_min, atomic_max,\n  3622:     1,\n  3623:     i8 AtomicI8\n  3624: }\n  3625: #[cfg(target_has_atomic_load_store = \"8\")]\n  3626: atomic_int! {\n  3627:     cfg(target_has_atomic = \"8\"),\n  3628:     cfg(target_has_atomic_primitive_alignment = \"8\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3632:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3633:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3634:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3635:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3636:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_update",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "primitive": "bool"
                            }
                          ],
                          "output": {
                            "resolved_path": {
                              "args": {
                                "angle_bracketed": {
                                  "args": [
                                    {
                                      "type": {
                                        "primitive": "bool"
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
      "name": "fetch_update",
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
                      "primitive": "bool"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 13729,
            "path": "Atomic"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:29422",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "set_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ],
          [
            "fetch_order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "bool"
                    }
                  },
                  {
                    "type": {
                      "primitive": "bool"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1309:     #[rustc_should_not_be_called_on_const_items]\n  1310:     pub const fn as_ptr(&self) -> *mut bool {\n  1311:         self.v.get().cast()\n  1312:     }\n  1313: \n  1314:     /// An alias for [`AtomicBool::try_update`].\n  1315:     #[inline]\n  1316:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1317:     #[cfg(target_has_atomic = \"8\")]\n  1318:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1319:     #[rustc_should_not_be_called_on_const_items]\n  1320:     #[deprecated(\n  1321:         since = \"1.99.0\",\n  1322:         note = \"renamed to `try_update` for consistency\",\n  1323:         suggestion = \"try_update\"\n  1324:     )]\n  1325:     pub fn fetch_update<F>(\n  1326:         &self,\n  1327:         set_order: Ordering,\n  1328:         fetch_order: Ordering,\n  1329:         f: F,\n  1330:     ) -> Result<bool, bool>\n  1331:     where\n  1332:         F: FnMut(bool) -> Option<bool>,\n  1333:     {\n  1334:         self.try_update(set_order, fetch_order, f)\n  1335:     }\n  1336: \n  1337:     /// Fetches the value, and applies a function to it that returns an optional\n  1338:     /// new value. Returns a `Result` of `Ok(previous_value)` if the function\n  1339:     /// returned `Some(_)`, else `Err(previous_value)`.\n  1340:     ///\n  1341:     /// See also: [`update`](`AtomicBool::update`).",
    "nanvix_source": "  1307:     #[inline]\n  1308:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1309:     #[cfg(target_has_atomic = \"8\")]\n  1310:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1311:     #[rustc_should_not_be_called_on_const_items]\n  1312:     #[deprecated(\n  1313:         since = \"1.99.0\",\n  1314:         note = \"renamed to `try_update` for consistency\",\n  1315:         suggestion = \"try_update\"\n  1316:     )]\n  1317:     pub fn fetch_update<F>(\n  1318:         &self,\n  1319:         set_order: Ordering,\n  1320:         fetch_order: Ordering,\n  1321:         f: F,\n  1322:     ) -> Result<bool, bool>\n  1323:     where\n  1324:         F: FnMut(bool) -> Option<bool>,\n  1325:     {\n  1326:         self.try_update(set_order, fetch_order, f)\n  1327:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_xor",
    "generation_group": "concurrency_or_hidden_state",
    "classification": "concurrency_or_hidden_state",
    "classification_reasons": [
      "atomic_state_not_exposed_by_ordinary_view"
    ],
    "category": "atomic",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "concurrency_or_hidden_state",
      "raw_pointer_equality",
      "multiple_rust_declarations_share_path"
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
      "name": "fetch_xor",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                      "raw_pointer": {
                        "is_mutable": true,
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
            "id": 13729,
            "path": "Atomic"
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
        "impl_id": "core:29452",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13729",
        "resolved_owner_path": [
          "core",
          "sync",
          "atomic",
          "Atomic"
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
            "val",
            {
              "primitive": "usize"
            }
          ],
          [
            "order",
            {
              "resolved_path": {
                "args": null,
                "id": 10014,
                "path": "Ordering"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  2443:     ///\n  2444:     /// ```\n  2445:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2446:     ///\n  2447:     /// let pointer = &mut 3i64 as *mut i64;\n  2448:     /// let atom = AtomicPtr::<i64>::new(pointer);\n  2449:     ///\n  2450:     /// // Toggle a tag bit on the pointer.\n  2451:     /// atom.fetch_xor(1, Ordering::Relaxed);\n  2452:     /// assert_eq!(atom.load(Ordering::Relaxed).addr() & 1, 1);\n  2453:     /// ```\n  2454:     #[inline]\n  2455:     #[cfg(target_has_atomic = \"ptr\")]\n  2456:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2457:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2458:     #[rustc_should_not_be_called_on_const_items]\n  2459:     pub fn fetch_xor(&self, val: usize, order: Ordering) -> *mut T {\n  2460:         // SAFETY: data races are prevented by atomic intrinsics.\n  2461:         unsafe { atomic_xor(self.as_ptr(), val, order).cast() }\n  2462:     }\n  2463: \n  2464:     /// Returns a mutable pointer to the underlying pointer.\n  2465:     ///\n  2466:     /// Doing non-atomic reads and writes on the resulting pointer can be a data race.\n  2467:     /// This method is mostly useful for FFI, where the function signature may use\n  2468:     /// `*mut *mut T` instead of `&AtomicPtr<T>`.\n  2469:     ///\n  2470:     /// Returning an `*mut` pointer from a shared reference to this atomic is safe because the\n  2471:     /// atomic types work with interior mutability. All modifications of an atomic change the value\n  2472:     /// through a shared reference, and can do so safely as long as they use atomic operations. Any\n  2473:     /// use of the returned raw pointer requires an `unsafe` block and still has to uphold the\n  2474:     /// requirements of the [memory model].\n  2475:     ///",
    "nanvix_source": "  2438:     ///\n  2439:     /// // Toggle a tag bit on the pointer.\n  2440:     /// atom.fetch_xor(1, Ordering::Relaxed);\n  2441:     /// assert_eq!(atom.load(Ordering::Relaxed).addr() & 1, 1);\n  2442:     /// ```\n  2443:     #[inline]\n  2444:     #[cfg(target_has_atomic = \"ptr\")]\n  2445:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2446:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2447:     #[rustc_should_not_be_called_on_const_items]\n  2448:     pub fn fetch_xor(&self, val: usize, order: Ordering) -> *mut T {\n  2449:         // SAFETY: data races are prevented by atomic intrinsics.\n  2450:         unsafe { atomic_xor(self.as_ptr(), val, order).cast() }\n  2451:     }\n  2452: \n  2453:     /// Returns a mutable pointer to the underlying pointer.\n  2454:     ///\n  2455:     /// Doing non-atomic reads and writes on the resulting pointer can be a data race.\n  2456:     /// This method is mostly useful for FFI, where the function signature may use\n  2457:     /// `*mut *mut T` instead of `&AtomicPtr<T>`.\n  2458:     ///",
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
