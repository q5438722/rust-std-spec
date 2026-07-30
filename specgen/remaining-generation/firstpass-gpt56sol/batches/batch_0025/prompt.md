For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicPtr::fetch_byte_add",
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
    "target": "core::sync::atomic::AtomicPtr::fetch_byte_sub",
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
    "target": "core::sync::atomic::AtomicPtr::fetch_or",
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
    "target": "core::sync::atomic::AtomicPtr::fetch_ptr_add",
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
    "target": "core::sync::atomic::AtomicPtr::fetch_ptr_sub",
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
    "target": "core::sync::atomic::AtomicPtr::fetch_update",
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
                              "raw_pointer": {
                                "is_mutable": true,
                                "type": {
                                  "generic": "T"
                                }
                              }
                            }
                          ],
                          "output": {
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
                      "raw_pointer": {
                        "is_mutable": true,
                        "type": {
                          "generic": "T"
                        }
                      }
                    }
                  },
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1985:         // an `UnsafeCell` that we have by reference) and the atomic operation\n  1986:         // itself allows us to safely mutate the `UnsafeCell` contents.\n  1987:         unsafe { atomic_compare_exchange_weak(self.as_ptr(), current, new, success, failure) }\n  1988:     }\n  1989: \n  1990:     /// An alias for [`AtomicPtr::try_update`].\n  1991:     #[inline]\n  1992:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1993:     #[cfg(target_has_atomic = \"ptr\")]\n  1994:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1995:     #[rustc_should_not_be_called_on_const_items]\n  1996:     #[deprecated(\n  1997:         since = \"1.99.0\",\n  1998:         note = \"renamed to `try_update` for consistency\",\n  1999:         suggestion = \"try_update\"\n  2000:     )]\n  2001:     pub fn fetch_update<F>(\n  2002:         &self,\n  2003:         set_order: Ordering,\n  2004:         fetch_order: Ordering,\n  2005:         f: F,\n  2006:     ) -> Result<*mut T, *mut T>\n  2007:     where\n  2008:         F: FnMut(*mut T) -> Option<*mut T>,\n  2009:     {\n  2010:         self.try_update(set_order, fetch_order, f)\n  2011:     }\n  2012:     /// Fetches the value, and applies a function to it that returns an optional\n  2013:     /// new value. Returns a `Result` of `Ok(previous_value)` if the function\n  2014:     /// returned `Some(_)`, else `Err(previous_value)`.\n  2015:     ///\n  2016:     /// See also: [`update`](`AtomicPtr::update`).\n  2017:     ///",
    "nanvix_source": "  1980:     #[inline]\n  1981:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1982:     #[cfg(target_has_atomic = \"ptr\")]\n  1983:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1984:     #[rustc_should_not_be_called_on_const_items]\n  1985:     #[deprecated(\n  1986:         since = \"1.99.0\",\n  1987:         note = \"renamed to `try_update` for consistency\",\n  1988:         suggestion = \"try_update\"\n  1989:     )]\n  1990:     pub fn fetch_update<F>(\n  1991:         &self,\n  1992:         set_order: Ordering,\n  1993:         fetch_order: Ordering,\n  1994:         f: F,\n  1995:     ) -> Result<*mut T, *mut T>\n  1996:     where\n  1997:         F: FnMut(*mut T) -> Option<*mut T>,\n  1998:     {\n  1999:         self.try_update(set_order, fetch_order, f)\n  2000:     }",
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
