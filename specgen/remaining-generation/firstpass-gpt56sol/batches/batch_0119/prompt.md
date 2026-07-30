For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::cell::RefCell::try_borrow",
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
      "name": "try_borrow",
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
            "id": 9393,
            "path": "RefCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'_"
                              },
                              {
                                "type": {
                                  "generic": "T"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 13316,
                        "path": "Ref"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 12904,
                        "path": "BorrowError"
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
    "verification_source": "  1142:     ///\n  1143:     /// {\n  1144:     ///     let m = c.borrow_mut();\n  1145:     ///     assert!(c.try_borrow().is_err());\n  1146:     /// }\n  1147:     ///\n  1148:     /// {\n  1149:     ///     let m = c.borrow();\n  1150:     ///     assert!(c.try_borrow().is_ok());\n  1151:     /// }\n  1152:     /// ```\n  1153:     #[stable(feature = \"try_borrow\", since = \"1.13.0\")]\n  1154:     #[inline]\n  1155:     #[cfg_attr(feature = \"debug_refcell\", track_caller)]\n  1156:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1157:     #[rustc_should_not_be_called_on_const_items]\n  1158:     pub const fn try_borrow(&self) -> Result<Ref<'_, T>, BorrowError> {\n  1159:         match BorrowRef::new(&self.borrow) {\n  1160:             Some(b) => {\n  1161:                 #[cfg(feature = \"debug_refcell\")]\n  1162:                 {\n  1163:                     // `borrowed_at` is always the *first* active borrow\n  1164:                     if b.borrow.get() == 1 {\n  1165:                         self.borrowed_at.replace(Some(crate::panic::Location::caller()));\n  1166:                     }\n  1167:                 }\n  1168: \n  1169:                 // SAFETY: `BorrowRef` ensures that there is only immutable access\n  1170:                 // to the value while borrowed.\n  1171:                 let value = unsafe { NonNull::new_unchecked(self.value.get()) };\n  1172:                 Ok(Ref { value, borrow: b })\n  1173:             }\n  1174:             None => Err(BorrowError {",
    "nanvix_source": "  1148:     /// {\n  1149:     ///     let m = c.borrow();\n  1150:     ///     assert!(c.try_borrow().is_ok());\n  1151:     /// }\n  1152:     /// ```\n  1153:     #[stable(feature = \"try_borrow\", since = \"1.13.0\")]\n  1154:     #[inline]\n  1155:     #[cfg_attr(feature = \"debug_refcell\", track_caller)]\n  1156:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1157:     #[rustc_should_not_be_called_on_const_items]\n  1158:     pub const fn try_borrow(&self) -> Result<Ref<'_, T>, BorrowError> {\n  1159:         match BorrowRef::new(&self.borrow) {\n  1160:             Some(b) => {\n  1161:                 #[cfg(feature = \"debug_refcell\")]\n  1162:                 {\n  1163:                     // `borrowed_at` is always the *first* active borrow\n  1164:                     if b.borrow.get() == 1 {\n  1165:                         self.borrowed_at.replace(Some(crate::panic::Location::caller()));\n  1166:                     }\n  1167:                 }\n  1168: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::RefCell::try_borrow_mut",
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
      "name": "try_borrow_mut",
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
            "id": 9393,
            "path": "RefCell"
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
                        "modifier": "maybe",
                        "trait": {
                          "args": null,
                          "id": 12,
                          "path": "Sized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:24792",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9393",
        "resolved_owner_path": [
          "core",
          "cell",
          "RefCell"
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
                      "resolved_path": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "lifetime": "'_"
                              },
                              {
                                "type": {
                                  "generic": "T"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 13318,
                        "path": "RefMut"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 12906,
                        "path": "BorrowMutError"
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
    "verification_source": "  1239:     /// use std::cell::RefCell;\n  1240:     ///\n  1241:     /// let c = RefCell::new(5);\n  1242:     ///\n  1243:     /// {\n  1244:     ///     let m = c.borrow();\n  1245:     ///     assert!(c.try_borrow_mut().is_err());\n  1246:     /// }\n  1247:     ///\n  1248:     /// assert!(c.try_borrow_mut().is_ok());\n  1249:     /// ```\n  1250:     #[stable(feature = \"try_borrow\", since = \"1.13.0\")]\n  1251:     #[inline]\n  1252:     #[cfg_attr(feature = \"debug_refcell\", track_caller)]\n  1253:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1254:     #[rustc_should_not_be_called_on_const_items]\n  1255:     pub const fn try_borrow_mut(&self) -> Result<RefMut<'_, T>, BorrowMutError> {\n  1256:         match BorrowRefMut::new(&self.borrow) {\n  1257:             Some(b) => {\n  1258:                 #[cfg(feature = \"debug_refcell\")]\n  1259:                 {\n  1260:                     self.borrowed_at.replace(Some(crate::panic::Location::caller()));\n  1261:                 }\n  1262: \n  1263:                 // SAFETY: `BorrowRefMut` guarantees unique access.\n  1264:                 let value = unsafe { NonNull::new_unchecked(self.value.get()) };\n  1265:                 Ok(RefMut { value, borrow: b, marker: PhantomData })\n  1266:             }\n  1267:             None => Err(BorrowMutError {\n  1268:                 // If a borrow occurred, then we must already have an outstanding borrow,\n  1269:                 // so `borrowed_at` will be `Some`\n  1270:                 #[cfg(feature = \"debug_refcell\")]\n  1271:                 location: self.borrowed_at.get().unwrap(),",
    "nanvix_source": "  1245:     ///     assert!(c.try_borrow_mut().is_err());\n  1246:     /// }\n  1247:     ///\n  1248:     /// assert!(c.try_borrow_mut().is_ok());\n  1249:     /// ```\n  1250:     #[stable(feature = \"try_borrow\", since = \"1.13.0\")]\n  1251:     #[inline]\n  1252:     #[cfg_attr(feature = \"debug_refcell\", track_caller)]\n  1253:     #[rustc_const_unstable(feature = \"const_ref_cell\", issue = \"137844\")]\n  1254:     #[rustc_should_not_be_called_on_const_items]\n  1255:     pub const fn try_borrow_mut(&self) -> Result<RefMut<'_, T>, BorrowMutError> {\n  1256:         match BorrowRefMut::new(&self.borrow) {\n  1257:             Some(b) => {\n  1258:                 #[cfg(feature = \"debug_refcell\")]\n  1259:                 {\n  1260:                     self.borrowed_at.replace(Some(crate::panic::Location::caller()));\n  1261:                 }\n  1262: \n  1263:                 // SAFETY: `BorrowRefMut` guarantees unique access.\n  1264:                 let value = unsafe { NonNull::new_unchecked(self.value.get()) };\n  1265:                 Ok(RefMut { value, borrow: b, marker: PhantomData })",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::into_inner",
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
      "name": "into_inner",
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
            "id": 9473,
            "path": "UnsafeCell"
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
        "impl_id": "core:24889",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9473",
        "resolved_owner_path": [
          "core",
          "cell",
          "UnsafeCell"
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
          "generic": "T"
        }
      }
    },
    "verification_source": "  2349: \n  2350:     /// Unwraps the value, consuming the cell.\n  2351:     ///\n  2352:     /// # Examples\n  2353:     ///\n  2354:     /// ```\n  2355:     /// use std::cell::UnsafeCell;\n  2356:     ///\n  2357:     /// let uc = UnsafeCell::new(5);\n  2358:     ///\n  2359:     /// let five = uc.into_inner();\n  2360:     /// ```\n  2361:     #[inline(always)]\n  2362:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2363:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n  2364:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  2365:     pub const fn into_inner(self) -> T {\n  2366:         self.value\n  2367:     }\n  2368: \n  2369:     /// Replace the value in this `UnsafeCell` and return the old value.\n  2370:     ///\n  2371:     /// # Safety\n  2372:     ///\n  2373:     /// The caller must take care to avoid aliasing and data races.\n  2374:     ///\n  2375:     /// - It is Undefined Behavior to allow calls to race with\n  2376:     ///   any other access to the wrapped value.\n  2377:     /// - It is Undefined Behavior to call this while any other\n  2378:     ///   reference(s) to the wrapped value are alive.\n  2379:     ///\n  2380:     /// # Examples\n  2381:     ///",
    "nanvix_source": "  2355:     /// use std::cell::UnsafeCell;\n  2356:     ///\n  2357:     /// let uc = UnsafeCell::new(5);\n  2358:     ///\n  2359:     /// let five = uc.into_inner();\n  2360:     /// ```\n  2361:     #[inline(always)]\n  2362:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2363:     #[rustc_const_stable(feature = \"const_cell_into_inner\", since = \"1.83.0\")]\n  2364:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  2365:     pub const fn into_inner(self) -> T {\n  2366:         self.value\n  2367:     }\n  2368: \n  2369:     /// Replace the value in this `UnsafeCell` and return the old value.\n  2370:     ///\n  2371:     /// # Safety\n  2372:     ///\n  2373:     /// The caller must take care to avoid aliasing and data races.\n  2374:     ///\n  2375:     /// - It is Undefined Behavior to allow calls to race with",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cell::UnsafeCell::new",
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
            "id": 9473,
            "path": "UnsafeCell"
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
        "impl_id": "core:24889",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9473",
        "resolved_owner_path": [
          "core",
          "cell",
          "UnsafeCell"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "value",
            {
              "generic": "T"
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
            "id": 9473,
            "path": "UnsafeCell"
          }
        }
      }
    },
    "verification_source": "  2330: impl<T> UnsafeCell<T> {\n  2331:     /// Constructs a new instance of `UnsafeCell` which will wrap the specified\n  2332:     /// value.\n  2333:     ///\n  2334:     /// All access to the inner value through `&UnsafeCell<T>` requires `unsafe` code.\n  2335:     ///\n  2336:     /// # Examples\n  2337:     ///\n  2338:     /// ```\n  2339:     /// use std::cell::UnsafeCell;\n  2340:     ///\n  2341:     /// let uc = UnsafeCell::new(5);\n  2342:     /// ```\n  2343:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2344:     #[rustc_const_stable(feature = \"const_unsafe_cell_new\", since = \"1.32.0\")]\n  2345:     #[inline(always)]\n  2346:     pub const fn new(value: T) -> UnsafeCell<T> {\n  2347:         UnsafeCell { value }\n  2348:     }\n  2349: \n  2350:     /// Unwraps the value, consuming the cell.\n  2351:     ///\n  2352:     /// # Examples\n  2353:     ///\n  2354:     /// ```\n  2355:     /// use std::cell::UnsafeCell;\n  2356:     ///\n  2357:     /// let uc = UnsafeCell::new(5);\n  2358:     ///\n  2359:     /// let five = uc.into_inner();\n  2360:     /// ```\n  2361:     #[inline(always)]\n  2362:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "  2336:     /// # Examples\n  2337:     ///\n  2338:     /// ```\n  2339:     /// use std::cell::UnsafeCell;\n  2340:     ///\n  2341:     /// let uc = UnsafeCell::new(5);\n  2342:     /// ```\n  2343:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2344:     #[rustc_const_stable(feature = \"const_unsafe_cell_new\", since = \"1.32.0\")]\n  2345:     #[inline(always)]\n  2346:     pub const fn new(value: T) -> UnsafeCell<T> {\n  2347:         UnsafeCell { value }\n  2348:     }\n  2349: \n  2350:     /// Unwraps the value, consuming the cell.\n  2351:     ///\n  2352:     /// # Examples\n  2353:     ///\n  2354:     /// ```\n  2355:     /// use std::cell::UnsafeCell;\n  2356:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::is_eq",
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
      "name": "is_eq",
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
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   422: \n   423:     /// Returns `true` if the ordering is the `Equal` variant.\n   424:     ///\n   425:     /// # Examples\n   426:     ///\n   427:     /// ```\n   428:     /// use std::cmp::Ordering;\n   429:     ///\n   430:     /// assert_eq!(Ordering::Less.is_eq(), false);\n   431:     /// assert_eq!(Ordering::Equal.is_eq(), true);\n   432:     /// assert_eq!(Ordering::Greater.is_eq(), false);\n   433:     /// ```\n   434:     #[inline]\n   435:     #[must_use]\n   436:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   437:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   438:     pub const fn is_eq(self) -> bool {\n   439:         // All the `is_*` methods are implemented as comparisons against zero\n   440:         // to follow how clang's libcxx implements their equivalents in\n   441:         // <https://github.com/llvm/llvm-project/blob/60486292b79885b7800b082754153202bef5b1f0/libcxx/include/__compare/is_eq.h#L23-L28>\n   442: \n   443:         self.as_raw() == 0\n   444:     }\n   445: \n   446:     /// Returns `true` if the ordering is not the `Equal` variant.\n   447:     ///\n   448:     /// # Examples\n   449:     ///\n   450:     /// ```\n   451:     /// use std::cmp::Ordering;\n   452:     ///\n   453:     /// assert_eq!(Ordering::Less.is_ne(), true);\n   454:     /// assert_eq!(Ordering::Equal.is_ne(), false);",
    "nanvix_source": "   429:     /// use std::cmp::Ordering;\n   430:     ///\n   431:     /// assert_eq!(Ordering::Less.is_eq(), false);\n   432:     /// assert_eq!(Ordering::Equal.is_eq(), true);\n   433:     /// assert_eq!(Ordering::Greater.is_eq(), false);\n   434:     /// ```\n   435:     #[inline]\n   436:     #[must_use]\n   437:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   438:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   439:     pub const fn is_eq(self) -> bool {\n   440:         // All the `is_*` methods are implemented as comparisons against zero\n   441:         // to follow how clang's libcxx implements their equivalents in\n   442:         // <https://github.com/llvm/llvm-project/blob/60486292b79885b7800b082754153202bef5b1f0/libcxx/include/__compare/is_eq.h#L23-L28>\n   443: \n   444:         self.as_raw() == 0\n   445:     }\n   446: \n   447:     /// Returns `true` if the ordering is not the `Equal` variant.\n   448:     ///\n   449:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::cmp::Ordering::is_ge",
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
      "name": "is_ge",
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
            "args": null,
            "id": 1682,
            "path": "Ordering"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:11181",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:1682",
        "resolved_owner_path": [
          "core",
          "cmp",
          "Ordering"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   521: \n   522:     /// Returns `true` if the ordering is either the `Greater` or `Equal` variant.\n   523:     ///\n   524:     /// # Examples\n   525:     ///\n   526:     /// ```\n   527:     /// use std::cmp::Ordering;\n   528:     ///\n   529:     /// assert_eq!(Ordering::Less.is_ge(), false);\n   530:     /// assert_eq!(Ordering::Equal.is_ge(), true);\n   531:     /// assert_eq!(Ordering::Greater.is_ge(), true);\n   532:     /// ```\n   533:     #[inline]\n   534:     #[must_use]\n   535:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   536:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   537:     pub const fn is_ge(self) -> bool {\n   538:         self.as_raw() >= 0\n   539:     }\n   540: \n   541:     /// Reverses the `Ordering`.\n   542:     ///\n   543:     /// * `Less` becomes `Greater`.\n   544:     /// * `Greater` becomes `Less`.\n   545:     /// * `Equal` becomes `Equal`.\n   546:     ///\n   547:     /// # Examples\n   548:     ///\n   549:     /// Basic behavior:\n   550:     ///\n   551:     /// ```\n   552:     /// use std::cmp::Ordering;\n   553:     ///",
    "nanvix_source": "   528:     /// use std::cmp::Ordering;\n   529:     ///\n   530:     /// assert_eq!(Ordering::Less.is_ge(), false);\n   531:     /// assert_eq!(Ordering::Equal.is_ge(), true);\n   532:     /// assert_eq!(Ordering::Greater.is_ge(), true);\n   533:     /// ```\n   534:     #[inline]\n   535:     #[must_use]\n   536:     #[rustc_const_stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   537:     #[stable(feature = \"ordering_helpers\", since = \"1.53.0\")]\n   538:     pub const fn is_ge(self) -> bool {\n   539:         self.as_raw() >= 0\n   540:     }\n   541: \n   542:     /// Reverses the `Ordering`.\n   543:     ///\n   544:     /// * `Less` becomes `Greater`.\n   545:     /// * `Greater` becomes `Less`.\n   546:     /// * `Equal` becomes `Equal`.\n   547:     ///\n   548:     /// # Examples",
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
