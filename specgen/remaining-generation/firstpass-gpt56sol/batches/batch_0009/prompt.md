For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::Atomic::fetch_byte_add",
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
      "name": "fetch_byte_add",
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
    "verification_source": "  2258:     ///\n  2259:     /// # Examples\n  2260:     ///\n  2261:     /// ```\n  2262:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2263:     ///\n  2264:     /// let atom = AtomicPtr::<i64>::new(core::ptr::null_mut());\n  2265:     /// assert_eq!(atom.fetch_byte_add(1, Ordering::Relaxed).addr(), 0);\n  2266:     /// // Note: in units of bytes, not `size_of::<i64>()`.\n  2267:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), 1);\n  2268:     /// ```\n  2269:     #[inline]\n  2270:     #[cfg(target_has_atomic = \"ptr\")]\n  2271:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2272:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2273:     #[rustc_should_not_be_called_on_const_items]\n  2274:     pub fn fetch_byte_add(&self, val: usize, order: Ordering) -> *mut T {\n  2275:         // SAFETY: data races are prevented by atomic intrinsics.\n  2276:         unsafe { atomic_add(self.as_ptr(), val, order).cast() }\n  2277:     }\n  2278: \n  2279:     /// Offsets the pointer's address by subtracting `val` *bytes*, returning the\n  2280:     /// previous pointer.\n  2281:     ///\n  2282:     /// This is equivalent to using [`wrapping_byte_sub`] to atomically\n  2283:     /// perform `ptr = ptr.wrapping_byte_sub(val)`.\n  2284:     ///\n  2285:     /// `fetch_byte_sub` takes an [`Ordering`] argument which describes the\n  2286:     /// memory ordering of this operation. All ordering modes are possible. Note\n  2287:     /// that using [`Acquire`] makes the store part of this operation\n  2288:     /// [`Relaxed`], and using [`Release`] makes the load part [`Relaxed`].\n  2289:     ///\n  2290:     /// **Note**: This method is only available on platforms that support atomic",
    "nanvix_source": "  2253:     /// let atom = AtomicPtr::<i64>::new(core::ptr::null_mut());\n  2254:     /// assert_eq!(atom.fetch_byte_add(1, Ordering::Relaxed).addr(), 0);\n  2255:     /// // Note: in units of bytes, not `size_of::<i64>()`.\n  2256:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), 1);\n  2257:     /// ```\n  2258:     #[inline]\n  2259:     #[cfg(target_has_atomic = \"ptr\")]\n  2260:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2261:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2262:     #[rustc_should_not_be_called_on_const_items]\n  2263:     pub fn fetch_byte_add(&self, val: usize, order: Ordering) -> *mut T {\n  2264:         // SAFETY: data races are prevented by atomic intrinsics.\n  2265:         unsafe { atomic_add(self.as_ptr(), val, order).cast() }\n  2266:     }\n  2267: \n  2268:     /// Offsets the pointer's address by subtracting `val` *bytes*, returning the\n  2269:     /// previous pointer.\n  2270:     ///\n  2271:     /// This is equivalent to using [`wrapping_byte_sub`] to atomically\n  2272:     /// perform `ptr = ptr.wrapping_byte_sub(val)`.\n  2273:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_byte_sub",
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
      "name": "fetch_byte_sub",
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
    "verification_source": "  2294:     ///\n  2295:     /// # Examples\n  2296:     ///\n  2297:     /// ```\n  2298:     /// use core::sync::atomic::{AtomicPtr, Ordering};\n  2299:     ///\n  2300:     /// let mut arr = [0i64, 1];\n  2301:     /// let atom = AtomicPtr::<i64>::new(&raw mut arr[1]);\n  2302:     /// assert_eq!(atom.fetch_byte_sub(8, Ordering::Relaxed).addr(), (&raw const arr[1]).addr());\n  2303:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), (&raw const arr[0]).addr());\n  2304:     /// ```\n  2305:     #[inline]\n  2306:     #[cfg(target_has_atomic = \"ptr\")]\n  2307:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2308:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2309:     #[rustc_should_not_be_called_on_const_items]\n  2310:     pub fn fetch_byte_sub(&self, val: usize, order: Ordering) -> *mut T {\n  2311:         // SAFETY: data races are prevented by atomic intrinsics.\n  2312:         unsafe { atomic_sub(self.as_ptr(), val, order).cast() }\n  2313:     }\n  2314: \n  2315:     /// Performs a bitwise \"or\" operation on the address of the current pointer,\n  2316:     /// and the argument `val`, and stores a pointer with provenance of the\n  2317:     /// current pointer and the resulting address.\n  2318:     ///\n  2319:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2320:     /// `ptr = ptr.map_addr(|a| a | val)`. This can be used in tagged\n  2321:     /// pointer schemes to atomically set tag bits.\n  2322:     ///\n  2323:     /// **Caveat**: This operation returns the previous value. To compute the\n  2324:     /// stored value without losing provenance, you may use [`map_addr`]. For\n  2325:     /// example: `a.fetch_or(val).map_addr(|a| a | val)`.\n  2326:     ///",
    "nanvix_source": "  2289:     /// let mut arr = [0i64, 1];\n  2290:     /// let atom = AtomicPtr::<i64>::new(&raw mut arr[1]);\n  2291:     /// assert_eq!(atom.fetch_byte_sub(8, Ordering::Relaxed).addr(), (&raw const arr[1]).addr());\n  2292:     /// assert_eq!(atom.load(Ordering::Relaxed).addr(), (&raw const arr[0]).addr());\n  2293:     /// ```\n  2294:     #[inline]\n  2295:     #[cfg(target_has_atomic = \"ptr\")]\n  2296:     #[stable(feature = \"strict_provenance_atomic_ptr\", since = \"1.91.0\")]\n  2297:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2298:     #[rustc_should_not_be_called_on_const_items]\n  2299:     pub fn fetch_byte_sub(&self, val: usize, order: Ordering) -> *mut T {\n  2300:         // SAFETY: data races are prevented by atomic intrinsics.\n  2301:         unsafe { atomic_sub(self.as_ptr(), val, order).cast() }\n  2302:     }\n  2303: \n  2304:     /// Performs a bitwise \"or\" operation on the address of the current pointer,\n  2305:     /// and the argument `val`, and stores a pointer with provenance of the\n  2306:     /// current pointer and the resulting address.\n  2307:     ///\n  2308:     /// This is equivalent to using [`map_addr`] to atomically perform\n  2309:     /// `ptr = ptr.map_addr(|a| a | val)`. This can be used in tagged",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_max",
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
      "name": "fetch_max",
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
    "target": "core::sync::atomic::Atomic::fetch_min",
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
      "name": "fetch_min",
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
    "target": "core::sync::atomic::Atomic::fetch_nand",
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
      "name": "fetch_nand",
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
                      "primitive": "i8"
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
        "impl_id": "core:29474",
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
              "primitive": "i8"
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
          "primitive": "i8"
        }
      }
    },
    "verification_source": "  3606:             /// # }\n  3607:             /// ```\n  3608:             ///\n  3609:             /// [memory model]: self#memory-model-for-atomic-accesses\n  3610:             #[inline]\n  3611:             #[stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  3612:             #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  3613:             #[rustc_never_returns_null_ptr]\n  3614:             pub const fn as_ptr(&self) -> *mut $int_type {\n  3615:                 self.v.get().cast()\n  3616:             }\n  3617:         }\n  3618:     }\n  3619: }\n  3620: \n  3621: #[cfg(target_has_atomic_load_store = \"8\")]\n  3622: atomic_int! {\n  3623:     cfg(target_has_atomic = \"8\"),\n  3624:     cfg(target_has_atomic_equal_alignment = \"8\"),\n  3625:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3626:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3627:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3628:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3629:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3630:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3631:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3632:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),\n  3633:     \"i8\",\n  3634:     \"\",\n  3635:     atomic_min, atomic_max,\n  3636:     1,\n  3637:     i8 AtomicI8\n  3638: }",
    "nanvix_source": "  3598:             #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  3599:             #[rustc_never_returns_null_ptr]\n  3600:             pub const fn as_ptr(&self) -> *mut $int_type {\n  3601:                 self.v.get().cast()\n  3602:             }\n  3603:         }\n  3604:     }\n  3605: }\n  3606: \n  3607: #[cfg(target_has_atomic_load_store = \"8\")]\n  3608: atomic_int! {\n  3609:     cfg(target_has_atomic = \"8\"),\n  3610:     cfg(target_has_atomic_primitive_alignment = \"8\"),\n  3611:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3612:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3613:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3614:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3615:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3616:     stable(feature = \"integer_atomics_stable\", since = \"1.34.0\"),\n  3617:     rustc_const_stable(feature = \"const_integer_atomics\", since = \"1.34.0\"),\n  3618:     rustc_const_stable(feature = \"const_atomic_into_inner\", since = \"1.79.0\"),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::Atomic::fetch_not",
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
      "concurrency_or_hidden_state"
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
      "name": "fetch_not",
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1255:     /// ```\n  1256:     /// use std::sync::atomic::{AtomicBool, Ordering};\n  1257:     ///\n  1258:     /// let foo = AtomicBool::new(true);\n  1259:     /// assert_eq!(foo.fetch_not(Ordering::SeqCst), true);\n  1260:     /// assert_eq!(foo.load(Ordering::SeqCst), false);\n  1261:     ///\n  1262:     /// let foo = AtomicBool::new(false);\n  1263:     /// assert_eq!(foo.fetch_not(Ordering::SeqCst), false);\n  1264:     /// assert_eq!(foo.load(Ordering::SeqCst), true);\n  1265:     /// ```\n  1266:     #[inline]\n  1267:     #[stable(feature = \"atomic_bool_fetch_not\", since = \"1.81.0\")]\n  1268:     #[cfg(target_has_atomic = \"8\")]\n  1269:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1270:     #[rustc_should_not_be_called_on_const_items]\n  1271:     pub fn fetch_not(&self, order: Ordering) -> bool {\n  1272:         self.fetch_xor(true, order)\n  1273:     }\n  1274: \n  1275:     /// Returns a mutable pointer to the underlying [`bool`].\n  1276:     ///\n  1277:     /// Doing non-atomic reads and writes on the resulting boolean can be a data race.\n  1278:     /// This method is mostly useful for FFI, where the function signature may use\n  1279:     /// `*mut bool` instead of `&AtomicBool`.\n  1280:     ///\n  1281:     /// Returning an `*mut` pointer from a shared reference to this atomic is safe because the\n  1282:     /// atomic types work with interior mutability. All modifications of an atomic change the value\n  1283:     /// through a shared reference, and can do so safely as long as they use atomic operations. Any\n  1284:     /// use of the returned raw pointer requires an `unsafe` block and still has to uphold the\n  1285:     /// requirements of the [memory model].\n  1286:     ///\n  1287:     /// # Examples",
    "nanvix_source": "  1253:     ///\n  1254:     /// let foo = AtomicBool::new(false);\n  1255:     /// assert_eq!(foo.fetch_not(Ordering::SeqCst), false);\n  1256:     /// assert_eq!(foo.load(Ordering::SeqCst), true);\n  1257:     /// ```\n  1258:     #[inline]\n  1259:     #[stable(feature = \"atomic_bool_fetch_not\", since = \"1.81.0\")]\n  1260:     #[cfg(target_has_atomic = \"8\")]\n  1261:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1262:     #[rustc_should_not_be_called_on_const_items]\n  1263:     pub fn fetch_not(&self, order: Ordering) -> bool {\n  1264:         self.fetch_xor(true, order)\n  1265:     }\n  1266: \n  1267:     /// Returns a mutable pointer to the underlying [`bool`].\n  1268:     ///\n  1269:     /// Doing non-atomic reads and writes on the resulting boolean can be a data race.\n  1270:     /// This method is mostly useful for FFI, where the function signature may use\n  1271:     /// `*mut bool` instead of `&AtomicBool`.\n  1272:     ///\n  1273:     /// Returning an `*mut` pointer from a shared reference to this atomic is safe because the",
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
