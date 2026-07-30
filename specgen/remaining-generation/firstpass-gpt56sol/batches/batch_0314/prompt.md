For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::boxed::Box::assume_init",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
        "is_unsafe": true
      },
      "name": "assume_init",
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
                        "path": "mem::MaybeUninit"
                      }
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
            "id": 82,
            "path": "Box"
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
        "impl_id": "alloc:477",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
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
            "id": 82,
            "path": "Box"
          }
        }
      }
    },
    "verification_source": "  1171:     /// causes immediate undefined behavior.\n  1172:     ///\n  1173:     /// [`MaybeUninit::assume_init`]: mem::MaybeUninit::assume_init\n  1174:     ///\n  1175:     /// # Examples\n  1176:     ///\n  1177:     /// ```\n  1178:     /// let mut five = Box::<u32>::new_uninit();\n  1179:     /// // Deferred initialization:\n  1180:     /// five.write(5);\n  1181:     /// let five: Box<u32> = unsafe { five.assume_init() };\n  1182:     ///\n  1183:     /// assert_eq!(*five, 5)\n  1184:     /// ```\n  1185:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1186:     #[inline(always)]\n  1187:     pub unsafe fn assume_init(self) -> Box<T, A> {\n  1188:         // This is used in the `vec!` macro, so we optimize for minimal IR generation\n  1189:         // even in debug builds.\n  1190:         // SAFETY: `Box<T>` and `Box<MaybeUninit<T>>` have the same layout.\n  1191:         unsafe { core::intrinsics::transmute_unchecked(self) }\n  1192:     }\n  1193: \n  1194:     /// Writes the value and converts to `Box<T, A>`.\n  1195:     ///\n  1196:     /// This method converts the box similarly to [`Box::assume_init`] but\n  1197:     /// writes `value` into it before conversion thus guaranteeing safety.\n  1198:     /// In some scenarios use of this method may improve performance because\n  1199:     /// the compiler may be able to optimize copying from stack.\n  1200:     ///\n  1201:     /// # Examples\n  1202:     ///\n  1203:     /// ```",
    "nanvix_source": "  1191:     /// ```\n  1192:     /// let mut five = Box::<u32>::new_uninit();\n  1193:     /// // Deferred initialization:\n  1194:     /// five.write(5);\n  1195:     /// let five: Box<u32> = unsafe { five.assume_init() };\n  1196:     ///\n  1197:     /// assert_eq!(*five, 5)\n  1198:     /// ```\n  1199:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1200:     #[inline(always)]\n  1201:     pub unsafe fn assume_init(self) -> Box<T, A> {\n  1202:         // This is used in the `vec!` macro, so we optimize for minimal IR generation\n  1203:         // even in debug builds.\n  1204:         // SAFETY: `Box<T>` and `Box<MaybeUninit<T>>` have the same layout.\n  1205:         unsafe { core::intrinsics::transmute_unchecked(self) }\n  1206:     }\n  1207: \n  1208:     /// Writes the value and converts to `Box<T, A>`.\n  1209:     ///\n  1210:     /// This method converts the box similarly to [`Box::assume_init`] but\n  1211:     /// writes `value` into it before conversion thus guaranteeing safety.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::downcast",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "multiple_rust_declarations_share_path"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 56,
                        "path": "Any"
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "downcast",
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
                      "dyn_trait": {
                        "lifetime": null,
                        "traits": [
                          {
                            "generic_params": [],
                            "trait": {
                              "args": null,
                              "id": 56,
                              "path": "Any"
                            }
                          }
                        ]
                      }
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
            "id": 82,
            "path": "crate::boxed::Box"
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
        "impl_id": "alloc:422",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
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
                        "id": 82,
                        "path": "Box"
                      }
                    }
                  },
                  {
                    "type": {
                      "generic": "Self"
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
    "verification_source": "   317:     ///\n   318:     /// ```\n   319:     /// use std::any::Any;\n   320:     ///\n   321:     /// fn print_if_string(value: Box<dyn Any>) {\n   322:     ///     if let Ok(string) = value.downcast::<String>() {\n   323:     ///         println!(\"String ({}): {}\", string.len(), string);\n   324:     ///     }\n   325:     /// }\n   326:     ///\n   327:     /// let my_string = \"Hello World\".to_string();\n   328:     /// print_if_string(Box::new(my_string));\n   329:     /// print_if_string(Box::new(0i8));\n   330:     /// ```\n   331:     #[inline]\n   332:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   333:     pub fn downcast<T: Any>(self) -> Result<Box<T, A>, Self> {\n   334:         if self.is::<T>() { unsafe { Ok(self.downcast_unchecked::<T>()) } } else { Err(self) }\n   335:     }\n   336: \n   337:     /// Downcasts the box to a concrete type.\n   338:     ///\n   339:     /// For a safe alternative see [`downcast`].\n   340:     ///\n   341:     /// # Examples\n   342:     ///\n   343:     /// ```\n   344:     /// #![feature(downcast_unchecked)]\n   345:     ///\n   346:     /// use std::any::Any;\n   347:     ///\n   348:     /// let x: Box<dyn Any> = Box::new(1_usize);\n   349:     ///",
    "nanvix_source": "   323:     ///         println!(\"String ({}): {}\", string.len(), string);\n   324:     ///     }\n   325:     /// }\n   326:     ///\n   327:     /// let my_string = \"Hello World\".to_string();\n   328:     /// print_if_string(Box::new(my_string));\n   329:     /// print_if_string(Box::new(0i8));\n   330:     /// ```\n   331:     #[inline]\n   332:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   333:     pub fn downcast<T: Any>(self) -> Result<Box<T, A>, Self> {\n   334:         if self.is::<T>() { unsafe { Ok(self.downcast_unchecked::<T>()) } } else { Err(self) }\n   335:     }\n   336: \n   337:     /// Downcasts the box to a concrete type.\n   338:     ///\n   339:     /// For a safe alternative see [`downcast`].\n   340:     ///\n   341:     /// # Examples\n   342:     ///\n   343:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::from_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "from_raw",
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
            "id": 82,
            "path": "Box"
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
                          "id": 29,
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
        "impl_id": "alloc:485",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "raw",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1292:     /// use std::alloc::{alloc, Layout};\n  1293:     ///\n  1294:     /// unsafe {\n  1295:     ///     let ptr = alloc(Layout::new::<i32>()) as *mut i32;\n  1296:     ///     // In general .write is required to avoid attempting to destruct\n  1297:     ///     // the (uninitialized) previous contents of `ptr`, though for this\n  1298:     ///     // simple example `*ptr = 5` would have worked as well.\n  1299:     ///     ptr.write(5);\n  1300:     ///     let x = Box::from_raw(ptr);\n  1301:     /// }\n  1302:     /// ```\n  1303:     ///\n  1304:     /// [memory layout]: self#memory-layout\n  1305:     #[stable(feature = \"box_raw\", since = \"1.4.0\")]\n  1306:     #[inline]\n  1307:     #[must_use = \"call `drop(Box::from_raw(ptr))` if you intend to drop the `Box`\"]\n  1308:     pub unsafe fn from_raw(raw: *mut T) -> Self {\n  1309:         unsafe { Self::from_raw_in(raw, Global) }\n  1310:     }\n  1311: \n  1312:     /// Constructs a box from a `NonNull` pointer.\n  1313:     ///\n  1314:     /// After calling this function, the `NonNull` pointer is owned by\n  1315:     /// the resulting `Box`. Specifically, the `Box` destructor will call\n  1316:     /// the destructor of `T` and free the allocated memory. For this\n  1317:     /// to be safe, the memory must have been allocated in accordance\n  1318:     /// with the [memory layout] used by `Box` .\n  1319:     ///\n  1320:     /// # Safety\n  1321:     ///\n  1322:     /// This function is unsafe because improper use may lead to\n  1323:     /// memory problems. For example, a double-free may occur if the\n  1324:     /// function is called twice on the same `NonNull` pointer.",
    "nanvix_source": "  1314:     ///     ptr.write(5);\n  1315:     ///     let x = Box::from_raw(ptr);\n  1316:     /// }\n  1317:     /// ```\n  1318:     ///\n  1319:     /// [memory layout]: self#memory-layout\n  1320:     /// [considerations for unsafe code]: self#considerations-for-unsafe-code\n  1321:     #[stable(feature = \"box_raw\", since = \"1.4.0\")]\n  1322:     #[inline]\n  1323:     #[must_use = \"call `drop(Box::from_raw(ptr))` if you intend to drop the `Box`\"]\n  1324:     pub unsafe fn from_raw(raw: *mut T) -> Self {\n  1325:         unsafe { Self::from_raw_in(raw, Global) }\n  1326:     }\n  1327: \n  1328:     /// Constructs a box from a `NonNull` pointer.\n  1329:     ///\n  1330:     /// After calling this function, the `NonNull` pointer is owned by\n  1331:     /// the resulting `Box`. Specifically, the `Box` destructor will call\n  1332:     /// the destructor of `T` and free the allocated memory. For this\n  1333:     /// to be safe, the memory must have been allocated in accordance\n  1334:     /// with the [memory layout] used by `Box` .",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::Box::into_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
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
      "name": "into_raw",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 82,
            "path": "Box"
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
                          "id": 29,
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
        "impl_id": "alloc:485",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:82",
        "resolved_owner_path": [
          "alloc",
          "boxed",
          "Box"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "b",
            {
              "generic": "Self"
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
    "verification_source": "  1400:     ///     dealloc(ptr as *mut u8, Layout::new::<String>());\n  1401:     /// }\n  1402:     /// ```\n  1403:     /// Note: This is equivalent to the following:\n  1404:     /// ```\n  1405:     /// let x = Box::new(String::from(\"Hello\"));\n  1406:     /// let ptr = Box::into_raw(x);\n  1407:     /// unsafe {\n  1408:     ///     drop(Box::from_raw(ptr));\n  1409:     /// }\n  1410:     /// ```\n  1411:     ///\n  1412:     /// [memory layout]: self#memory-layout\n  1413:     #[must_use = \"losing the pointer will leak memory\"]\n  1414:     #[stable(feature = \"box_raw\", since = \"1.4.0\")]\n  1415:     #[inline]\n  1416:     pub fn into_raw(b: Self) -> *mut T {\n  1417:         // Avoid `into_raw_with_allocator` as that interacts poorly with Miri's Stacked Borrows.\n  1418:         let mut b = mem::ManuallyDrop::new(b);\n  1419:         // We go through the built-in deref for `Box`, which is crucial for Miri to recognize this\n  1420:         // operation for it's alias tracking.\n  1421:         &raw mut **b\n  1422:     }\n  1423: \n  1424:     /// Consumes the `Box`, returning a wrapped `NonNull` pointer.\n  1425:     ///\n  1426:     /// The pointer will be properly aligned.\n  1427:     ///\n  1428:     /// After calling this function, the caller is responsible for the\n  1429:     /// memory previously managed by the `Box`. In particular, the\n  1430:     /// caller should properly destroy `T` and release the memory, taking\n  1431:     /// into account the [memory layout] used by `Box`. The easiest way to\n  1432:     /// do this is to convert the `NonNull` pointer back into a `Box` with the",
    "nanvix_source": "  1424:     /// let ptr = Box::into_raw(x);\n  1425:     /// unsafe {\n  1426:     ///     drop(Box::from_raw(ptr));\n  1427:     /// }\n  1428:     /// ```\n  1429:     ///\n  1430:     /// [memory layout]: self#memory-layout\n  1431:     #[must_use = \"losing the pointer will leak memory\"]\n  1432:     #[stable(feature = \"box_raw\", since = \"1.4.0\")]\n  1433:     #[inline]\n  1434:     pub fn into_raw(b: Self) -> *mut T {\n  1435:         // Avoid `into_raw_with_allocator` as that interacts poorly with Miri's Stacked Borrows.\n  1436:         let mut b = mem::ManuallyDrop::new(b);\n  1437:         // We need to give Miri (specifically, Stacked Borrows) a chance to recognize this as a\n  1438:         // safe-to-raw-pointer cast. To achieve this, we first create a mutable reference, and then\n  1439:         // cast that to a raw pointer -- this cast is recognized by the aliasing model and leads to\n  1440:         // a suitable retag.\n  1441:         // It would be wrong for `into_raw_with_allocator` to do the same as that would induce\n  1442:         // uniqueness assumptions (from the `&mut`) that we only want with the default allocator.\n  1443:         (&mut **b) as *mut T\n  1444:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::from_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
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
        "is_unsafe": true
      },
      "name": "from_raw",
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
            "id": 108,
            "path": "CString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3307",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:108",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "CString"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 3297,
                    "path": "c_char"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 108,
            "path": "CString"
          }
        }
      }
    },
    "verification_source": "   386:     /// use std::ffi::CString;\n   387:     /// use std::os::raw::c_char;\n   388:     ///\n   389:     /// extern \"C\" {\n   390:     ///     fn some_extern_function(s: *mut c_char);\n   391:     /// }\n   392:     ///\n   393:     /// let c_string = CString::from(c\"Hello!\");\n   394:     /// let raw = c_string.into_raw();\n   395:     /// unsafe {\n   396:     ///     some_extern_function(raw);\n   397:     ///     let c_string = CString::from_raw(raw);\n   398:     /// }\n   399:     /// ```\n   400:     #[must_use = \"call `drop(from_raw(ptr))` if you intend to drop the `CString`\"]\n   401:     #[stable(feature = \"cstr_memory\", since = \"1.4.0\")]\n   402:     pub unsafe fn from_raw(ptr: *mut c_char) -> CString {\n   403:         // SAFETY: This is called with a pointer that was obtained from a call\n   404:         // to `CString::into_raw` and the length has not been modified. As such,\n   405:         // we know there is a NUL byte (and only one) at the end and that the\n   406:         // information about the size of the allocation is correct on Rust's\n   407:         // side.\n   408:         unsafe {\n   409:             unsafe extern \"C\" {\n   410:                 /// Provided by libc or compiler_builtins.\n   411:                 fn strlen(s: *const c_char) -> usize;\n   412:             }\n   413:             let len = strlen(ptr) + 1; // Including the NUL byte\n   414:             let slice = slice::from_raw_parts_mut(ptr, len);\n   415:             CString { inner: Box::from_raw(slice as *mut [c_char] as *mut [u8]) }\n   416:         }\n   417:     }\n   418: ",
    "nanvix_source": "   392:     ///\n   393:     /// let c_string = CString::from(c\"Hello!\");\n   394:     /// let raw = c_string.into_raw();\n   395:     /// unsafe {\n   396:     ///     some_extern_function(raw);\n   397:     ///     let c_string = CString::from_raw(raw);\n   398:     /// }\n   399:     /// ```\n   400:     #[must_use = \"call `drop(from_raw(ptr))` if you intend to drop the `CString`\"]\n   401:     #[stable(feature = \"cstr_memory\", since = \"1.4.0\")]\n   402:     pub unsafe fn from_raw(ptr: *mut c_char) -> CString {\n   403:         // SAFETY: This is called with a pointer that was obtained from a call\n   404:         // to `CString::into_raw` and the length has not been modified. As such,\n   405:         // we know there is a NUL byte (and only one) at the end and that the\n   406:         // information about the size of the allocation is correct on Rust's\n   407:         // side.\n   408:         unsafe {\n   409:             unsafe extern \"C\" {\n   410:                 /// Provided by libc or compiler_builtins.\n   411:                 fn strlen(s: *const c_char) -> usize;\n   412:             }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::from_vec_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
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
        "is_unsafe": true
      },
      "name": "from_vec_unchecked",
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
            "id": 108,
            "path": "CString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:3307",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:108",
        "resolved_owner_path": [
          "alloc",
          "ffi",
          "c_str",
          "CString"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
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
                "id": 114,
                "path": "Vec"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   324:     /// # Safety\n   325:     ///\n   326:     /// The caller must ensure `v` contains no nul bytes in its contents.\n   327:     ///\n   328:     /// # Examples\n   329:     ///\n   330:     /// ```\n   331:     /// use std::ffi::CString;\n   332:     ///\n   333:     /// let raw = b\"foo\".to_vec();\n   334:     /// unsafe {\n   335:     ///     let c_string = CString::from_vec_unchecked(raw);\n   336:     /// }\n   337:     /// ```\n   338:     #[must_use]\n   339:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   340:     pub unsafe fn from_vec_unchecked(v: Vec<u8>) -> Self {\n   341:         debug_assert!(memchr::memchr(0, &v).is_none());\n   342:         unsafe { Self::_from_vec_unchecked(v) }\n   343:     }\n   344: \n   345:     unsafe fn _from_vec_unchecked(mut v: Vec<u8>) -> Self {\n   346:         v.reserve_exact(1);\n   347:         v.push(0);\n   348:         Self { inner: v.into_boxed_slice() }\n   349:     }\n   350: \n   351:     /// Retakes ownership of a `CString` that was transferred to C via\n   352:     /// [`CString::into_raw`].\n   353:     ///\n   354:     /// Additionally, the length of the string will be recalculated from the pointer.\n   355:     ///\n   356:     /// # Safety",
    "nanvix_source": "   330:     /// ```\n   331:     /// use std::ffi::CString;\n   332:     ///\n   333:     /// let raw = b\"foo\".to_vec();\n   334:     /// unsafe {\n   335:     ///     let c_string = CString::from_vec_unchecked(raw);\n   336:     /// }\n   337:     /// ```\n   338:     #[must_use]\n   339:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   340:     pub unsafe fn from_vec_unchecked(v: Vec<u8>) -> Self {\n   341:         debug_assert!(memchr::memchr(0, &v).is_none());\n   342:         unsafe { Self::_from_vec_unchecked(v) }\n   343:     }\n   344: \n   345:     unsafe fn _from_vec_unchecked(mut v: Vec<u8>) -> Self {\n   346:         v.reserve_exact(1);\n   347:         v.push(0);\n   348:         Self { inner: v.into_boxed_slice() }\n   349:     }\n   350: ",
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
