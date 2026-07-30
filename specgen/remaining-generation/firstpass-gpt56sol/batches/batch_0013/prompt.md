For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::sync::atomic::AtomicBool::as_ptr",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_ptr",
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "bool"
            }
          }
        }
      }
    },
    "verification_source": "  1294:     ///     fn my_atomic_op(arg: *mut bool);\n  1295:     /// }\n  1296:     ///\n  1297:     /// let mut atomic = AtomicBool::new(true);\n  1298:     /// unsafe {\n  1299:     ///     my_atomic_op(atomic.as_ptr());\n  1300:     /// }\n  1301:     /// # }\n  1302:     /// ```\n  1303:     ///\n  1304:     /// [memory model]: self#memory-model-for-atomic-accesses\n  1305:     #[inline]\n  1306:     #[stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1307:     #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1308:     #[rustc_never_returns_null_ptr]\n  1309:     #[rustc_should_not_be_called_on_const_items]\n  1310:     pub const fn as_ptr(&self) -> *mut bool {\n  1311:         self.v.get().cast()\n  1312:     }\n  1313: \n  1314:     /// An alias for [`AtomicBool::try_update`].\n  1315:     #[inline]\n  1316:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1317:     #[cfg(target_has_atomic = \"8\")]\n  1318:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1319:     #[rustc_should_not_be_called_on_const_items]\n  1320:     #[deprecated(\n  1321:         since = \"1.99.0\",\n  1322:         note = \"renamed to `try_update` for consistency\",\n  1323:         suggestion = \"try_update\"\n  1324:     )]\n  1325:     pub fn fetch_update<F>(\n  1326:         &self,",
    "nanvix_source": "  1292:     /// }\n  1293:     /// # }\n  1294:     /// ```\n  1295:     ///\n  1296:     /// [memory model]: self#memory-model-for-atomic-accesses\n  1297:     #[inline]\n  1298:     #[stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1299:     #[rustc_const_stable(feature = \"atomic_as_ptr\", since = \"1.70.0\")]\n  1300:     #[rustc_never_returns_null_ptr]\n  1301:     #[rustc_should_not_be_called_on_const_items]\n  1302:     pub const fn as_ptr(&self) -> *mut bool {\n  1303:         self.v.get().cast()\n  1304:     }\n  1305: \n  1306:     /// An alias for [`AtomicBool::try_update`].\n  1307:     #[inline]\n  1308:     #[stable(feature = \"atomic_fetch_update\", since = \"1.53.0\")]\n  1309:     #[cfg(target_has_atomic = \"8\")]\n  1310:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1311:     #[rustc_should_not_be_called_on_const_items]\n  1312:     #[deprecated(",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicBool::compare_and_swap",
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
      "name": "compare_and_swap",
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
            "current",
            {
              "primitive": "bool"
            }
          ],
          [
            "new",
            {
              "primitive": "bool"
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
    "verification_source": "   852:     ///\n   853:     /// assert_eq!(some_bool.compare_and_swap(true, false, Ordering::Relaxed), true);\n   854:     /// assert_eq!(some_bool.load(Ordering::Relaxed), false);\n   855:     ///\n   856:     /// assert_eq!(some_bool.compare_and_swap(true, true, Ordering::Relaxed), false);\n   857:     /// assert_eq!(some_bool.load(Ordering::Relaxed), false);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   861:     #[deprecated(\n   862:         since = \"1.50.0\",\n   863:         note = \"Use `compare_exchange` or `compare_exchange_weak` instead\"\n   864:     )]\n   865:     #[cfg(target_has_atomic = \"8\")]\n   866:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   867:     #[rustc_should_not_be_called_on_const_items]\n   868:     pub fn compare_and_swap(&self, current: bool, new: bool, order: Ordering) -> bool {\n   869:         match self.compare_exchange(current, new, order, strongest_failure_ordering(order)) {\n   870:             Ok(x) => x,\n   871:             Err(x) => x,\n   872:         }\n   873:     }\n   874: \n   875:     /// Stores a value into the [`bool`] if the current value is the same as the `current` value.\n   876:     ///\n   877:     /// The return value is a result indicating whether the new value was written and containing\n   878:     /// the previous value. On success this value is guaranteed to be equal to `current`.\n   879:     ///\n   880:     /// `compare_exchange` takes two [`Ordering`] arguments to describe the memory\n   881:     /// ordering of this operation. `success` describes the required ordering for the\n   882:     /// read-modify-write operation that takes place if the comparison with `current` succeeds.\n   883:     /// `failure` describes the required ordering for the load operation that takes place when\n   884:     /// the comparison fails. Using [`Acquire`] as success ordering makes the store part",
    "nanvix_source": "   850:     /// ```\n   851:     #[inline]\n   852:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   853:     #[deprecated(\n   854:         since = \"1.50.0\",\n   855:         note = \"Use `compare_exchange` or `compare_exchange_weak` instead\"\n   856:     )]\n   857:     #[cfg(target_has_atomic = \"8\")]\n   858:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   859:     #[rustc_should_not_be_called_on_const_items]\n   860:     pub fn compare_and_swap(&self, current: bool, new: bool, order: Ordering) -> bool {\n   861:         match self.compare_exchange(current, new, order, strongest_failure_ordering(order)) {\n   862:             Ok(x) => x,\n   863:             Err(x) => x,\n   864:         }\n   865:     }\n   866: \n   867:     /// Stores a value into the [`bool`] if the current value is the same as the `current` value.\n   868:     ///\n   869:     /// The return value is a result indicating whether the new value was written and containing\n   870:     /// the previous value. On success this value is guaranteed to be equal to `current`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicBool::fetch_not",
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
  },
  {
    "target": "core::sync::atomic::AtomicBool::fetch_update",
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
    "target": "core::sync::atomic::AtomicBool::from_mut",
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
      "name": "from_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "primitive": "bool"
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
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   611:     /// Gets atomic access to a `&mut bool`.\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```\n   616:     /// #![feature(atomic_from_mut)]\n   617:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   618:     ///\n   619:     /// let mut some_bool = true;\n   620:     /// let a = AtomicBool::from_mut(&mut some_bool);\n   621:     /// a.store(false, Ordering::Relaxed);\n   622:     /// assert_eq!(some_bool, false);\n   623:     /// ```\n   624:     #[inline]\n   625:     #[cfg(target_has_atomic_equal_alignment = \"8\")]\n   626:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n   627:     pub fn from_mut(v: &mut bool) -> &mut Self {\n   628:         // SAFETY: the mutable reference guarantees unique ownership, and\n   629:         // alignment of both `bool` and `Self` is 1.\n   630:         unsafe { &mut *(v as *mut bool as *mut Self) }\n   631:     }\n   632: \n   633:     /// Gets non-atomic access to a `&mut [AtomicBool]` slice.\n   634:     ///\n   635:     /// This is safe because the mutable reference guarantees that no other threads are\n   636:     /// concurrently accessing the atomic data.\n   637:     ///\n   638:     /// # Examples\n   639:     ///\n   640:     /// ```ignore-wasm\n   641:     /// #![feature(atomic_from_mut)]\n   642:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   643:     ///",
    "nanvix_source": "   611:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   612:     ///\n   613:     /// let mut some_bool = true;\n   614:     /// let a = AtomicBool::from_mut(&mut some_bool);\n   615:     /// a.store(false, Ordering::Relaxed);\n   616:     /// assert_eq!(some_bool, false);\n   617:     /// ```\n   618:     #[inline]\n   619:     #[cfg(target_has_atomic_primitive_alignment = \"8\")]\n   620:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n   621:     pub fn from_mut(v: &mut bool) -> &mut Self {\n   622:         // SAFETY: the mutable reference guarantees unique ownership, and\n   623:         // alignment of both `bool` and `Self` is 1.\n   624:         unsafe { &mut *(v as *mut bool as *mut Self) }\n   625:     }\n   626: \n   627:     /// Gets non-atomic access to a `&mut [AtomicBool]` slice.\n   628:     ///\n   629:     /// This is safe because the mutable reference guarantees that no other threads are\n   630:     /// concurrently accessing the atomic data.\n   631:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::sync::atomic::AtomicBool::from_mut_slice",
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
      "name": "from_mut_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
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
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "bool"
                  }
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
                "generic": "Self"
              }
            }
          }
        }
      }
    },
    "verification_source": "   671:     /// ```rust,ignore-wasm\n   672:     /// #![feature(atomic_from_mut)]\n   673:     /// use std::sync::atomic::{AtomicBool, Ordering};\n   674:     ///\n   675:     /// let mut some_bools = [false; 10];\n   676:     /// let a = &*AtomicBool::from_mut_slice(&mut some_bools);\n   677:     /// std::thread::scope(|s| {\n   678:     ///     for i in 0..a.len() {\n   679:     ///         s.spawn(move || a[i].store(true, Ordering::Relaxed));\n   680:     ///     }\n   681:     /// });\n   682:     /// assert_eq!(some_bools, [true; 10]);\n   683:     /// ```\n   684:     #[inline]\n   685:     #[cfg(target_has_atomic_equal_alignment = \"8\")]\n   686:     #[unstable(feature = \"atomic_from_mut\", issue = \"76314\")]\n   687:     pub fn from_mut_slice(v: &mut [bool]) -> &mut [Self] {\n   688:         // SAFETY: the mutable reference guarantees unique ownership, and\n   689:         // alignment of both `bool` and `Self` is 1.\n   690:         unsafe { &mut *(v as *mut [bool] as *mut [Self]) }\n   691:     }\n   692: \n   693:     /// Consumes the atomic and returns the contained value.\n   694:     ///\n   695:     /// This is safe because passing `self` by value guarantees that no other threads are\n   696:     /// concurrently accessing the atomic data.\n   697:     ///\n   698:     /// # Examples\n   699:     ///\n   700:     /// ```\n   701:     /// use std::sync::atomic::AtomicBool;\n   702:     ///\n   703:     /// let some_bool = AtomicBool::new(true);",
    "nanvix_source": "   669:     /// std::thread::scope(|s| {\n   670:     ///     for i in 0..a.len() {\n   671:     ///         s.spawn(move || a[i].store(true, Ordering::Relaxed));\n   672:     ///     }\n   673:     /// });\n   674:     /// assert_eq!(some_bools, [true; 10]);\n   675:     /// ```\n   676:     #[inline]\n   677:     #[cfg(target_has_atomic_primitive_alignment = \"8\")]\n   678:     #[stable(feature = \"atomic_from_mut\", since = \"CURRENT_RUSTC_VERSION\")]\n   679:     pub fn from_mut_slice(v: &mut [bool]) -> &mut [Self] {\n   680:         // SAFETY: the mutable reference guarantees unique ownership, and\n   681:         // alignment of both `bool` and `Self` is 1.\n   682:         unsafe { &mut *(v as *mut [bool] as *mut [Self]) }\n   683:     }\n   684: \n   685:     /// Consumes the atomic and returns the contained value.\n   686:     ///\n   687:     /// This is safe because passing `self` by value guarantees that no other threads are\n   688:     /// concurrently accessing the atomic data.\n   689:     ///",
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
