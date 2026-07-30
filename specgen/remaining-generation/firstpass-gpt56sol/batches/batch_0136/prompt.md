For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::pin::Pin::static_ref",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
      "name": "static_ref",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": "'static",
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
            "id": 9981,
            "path": "Pin"
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
        "impl_id": "core:29050",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9981",
        "resolved_owner_path": [
          "core",
          "pin",
          "Pin"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "r",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": "'static",
                "type": {
                  "generic": "T"
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
                        "lifetime": "'static",
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
            "id": 9981,
            "path": "Pin"
          }
        }
      }
    },
    "verification_source": "  1644:         // value out of this reference.\n  1645:         let pointer = unsafe { Pin::get_unchecked_mut(self) };\n  1646:         let new_pointer = func(pointer);\n  1647:         // SAFETY: as the value of `this` is guaranteed to not have\n  1648:         // been moved out, this call to `new_unchecked` is safe.\n  1649:         unsafe { Pin::new_unchecked(new_pointer) }\n  1650:     }\n  1651: }\n  1652: \n  1653: impl<T: ?Sized> Pin<&'static T> {\n  1654:     /// Gets a pinning reference from a `&'static` reference.\n  1655:     ///\n  1656:     /// This is safe because `T` is borrowed immutably for the `'static` lifetime, which\n  1657:     /// never ends.\n  1658:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1659:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1660:     pub const fn static_ref(r: &'static T) -> Pin<&'static T> {\n  1661:         // SAFETY: The 'static borrow guarantees the data will not be\n  1662:         // moved/invalidated until it gets dropped (which is never).\n  1663:         unsafe { Pin::new_unchecked(r) }\n  1664:     }\n  1665: }\n  1666: \n  1667: impl<T: ?Sized> Pin<&'static mut T> {\n  1668:     /// Gets a pinning mutable reference from a static mutable reference.\n  1669:     ///\n  1670:     /// This is safe because `T` is borrowed for the `'static` lifetime, which\n  1671:     /// never ends.\n  1672:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1673:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1674:     pub const fn static_mut(r: &'static mut T) -> Pin<&'static mut T> {\n  1675:         // SAFETY: The 'static borrow guarantees the data will not be\n  1676:         // moved/invalidated until it gets dropped (which is never).",
    "nanvix_source": "  1650:     }\n  1651: }\n  1652: \n  1653: impl<T: ?Sized> Pin<&'static T> {\n  1654:     /// Gets a pinning reference from a `&'static` reference.\n  1655:     ///\n  1656:     /// This is safe because `T` is borrowed immutably for the `'static` lifetime, which\n  1657:     /// never ends.\n  1658:     #[stable(feature = \"pin_static_ref\", since = \"1.61.0\")]\n  1659:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1660:     pub const fn static_ref(r: &'static T) -> Pin<&'static T> {\n  1661:         // SAFETY: The 'static borrow guarantees the data will not be\n  1662:         // moved/invalidated until it gets dropped (which is never).\n  1663:         unsafe { Pin::new_unchecked(r) }\n  1664:     }\n  1665: }\n  1666: \n  1667: impl<T: ?Sized> Pin<&'static mut T> {\n  1668:     /// Gets a pinning mutable reference from a static mutable reference.\n  1669:     ///\n  1670:     /// This is safe because `T` is borrowed for the `'static` lifetime, which",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::addr",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "addr",
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1039,
            "path": "NonZero"
          }
        }
      }
    },
    "verification_source": "   317:     #[unstable(feature = \"ptr_metadata\", issue = \"81513\")]\n   318:     #[must_use = \"this returns the result of the operation, \\\n   319:                   without modifying the original\"]\n   320:     #[inline]\n   321:     pub const fn to_raw_parts(self) -> (NonNull<()>, <T as super::Pointee>::Metadata) {\n   322:         (self.cast(), super::metadata(self.as_ptr()))\n   323:     }\n   324: \n   325:     /// Gets the \"address\" portion of the pointer.\n   326:     ///\n   327:     /// For more details, see the equivalent method on a raw pointer, [`pointer::addr`].\n   328:     ///\n   329:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   330:     #[must_use]\n   331:     #[inline]\n   332:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   333:     pub fn addr(self) -> NonZero<usize> {\n   334:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   335:         // meaning that the address will be non-zero.\n   336:         unsafe { NonZero::new_unchecked(self.as_ptr().addr()) }\n   337:     }\n   338: \n   339:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   340:     /// [`with_exposed_provenance`][NonNull::with_exposed_provenance] and returns the \"address\" portion.\n   341:     ///\n   342:     /// For more details, see the equivalent method on a raw pointer, [`pointer::expose_provenance`].\n   343:     ///\n   344:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   345:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   346:     pub fn expose_provenance(self) -> NonZero<usize> {\n   347:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   348:         // meaning that the address will be non-zero.\n   349:         unsafe { NonZero::new_unchecked(self.as_ptr().expose_provenance()) }",
    "nanvix_source": "   320:     }\n   321: \n   322:     /// Gets the \"address\" portion of the pointer.\n   323:     ///\n   324:     /// For more details, see the equivalent method on a raw pointer, [`pointer::addr`].\n   325:     ///\n   326:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   327:     #[must_use]\n   328:     #[inline]\n   329:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   330:     pub fn addr(self) -> NonZero<usize> {\n   331:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   332:         // meaning that the address will be non-zero.\n   333:         unsafe { NonZero::new_unchecked(self.as_ptr().addr()) }\n   334:     }\n   335: \n   336:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   337:     /// [`with_exposed_provenance`][NonNull::with_exposed_provenance] and returns the \"address\" portion.\n   338:     ///\n   339:     /// For more details, see the equivalent method on a raw pointer, [`pointer::expose_provenance`].\n   340:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::align_offset",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
    ],
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
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
      "name": "align_offset",
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
            "align",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1276:     /// let x = [5_u8, 6, 7, 8, 9];\n  1277:     /// let ptr = NonNull::new(x.as_ptr() as *mut u8).unwrap();\n  1278:     /// let offset = ptr.align_offset(align_of::<u16>());\n  1279:     ///\n  1280:     /// if offset < x.len() - 1 {\n  1281:     ///     let u16_ptr = ptr.add(offset).cast::<u16>();\n  1282:     ///     assert!(u16_ptr.read() == u16::from_ne_bytes([5, 6]) || u16_ptr.read() == u16::from_ne_bytes([6, 7]));\n  1283:     /// } else {\n  1284:     ///     // while the pointer can be aligned via `offset`, it would point\n  1285:     ///     // outside the allocation\n  1286:     /// }\n  1287:     /// # }\n  1288:     /// ```\n  1289:     #[inline]\n  1290:     #[must_use]\n  1291:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1292:     pub fn align_offset(self, align: usize) -> usize\n  1293:     where\n  1294:         T: Sized,\n  1295:     {\n  1296:         if !align.is_power_of_two() {\n  1297:             panic!(\"align_offset: align is not a power-of-two\");\n  1298:         }\n  1299: \n  1300:         {\n  1301:             // SAFETY: `align` has been checked to be a power of 2 above.\n  1302:             unsafe { ptr::align_offset(self.as_ptr(), align) }\n  1303:         }\n  1304:     }\n  1305: \n  1306:     /// Returns whether the pointer is properly aligned for `T`.\n  1307:     ///\n  1308:     /// # Examples",
    "nanvix_source": "  1215:     ///     assert!(u16_ptr.read() == u16::from_ne_bytes([5, 6]) || u16_ptr.read() == u16::from_ne_bytes([6, 7]));\n  1216:     /// } else {\n  1217:     ///     // while the pointer can be aligned via `offset`, it would point\n  1218:     ///     // outside the allocation\n  1219:     /// }\n  1220:     /// # }\n  1221:     /// ```\n  1222:     #[inline]\n  1223:     #[must_use]\n  1224:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1225:     pub fn align_offset(self, align: usize) -> usize\n  1226:     where\n  1227:         T: Sized,\n  1228:     {\n  1229:         if !align.is_power_of_two() {\n  1230:             panic!(\"align_offset: align is not a power-of-two\");\n  1231:         }\n  1232: \n  1233:         {\n  1234:             // SAFETY: `align` has been checked to be a power of 2 above.\n  1235:             unsafe { ptr::align_offset(self.as_ptr(), align) }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::cast",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
            "name": "U"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "cast",
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
                      "generic": "U"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9475,
            "path": "NonNull"
          }
        }
      }
    },
    "verification_source": "   486:     /// # Examples\n   487:     ///\n   488:     /// ```\n   489:     /// use std::ptr::NonNull;\n   490:     ///\n   491:     /// let mut x = 0u32;\n   492:     /// let ptr = NonNull::new(&mut x as *mut _).expect(\"null pointer\");\n   493:     ///\n   494:     /// let casted_ptr = ptr.cast::<i8>();\n   495:     /// let raw_ptr: *mut i8 = casted_ptr.as_ptr();\n   496:     /// ```\n   497:     #[stable(feature = \"nonnull_cast\", since = \"1.27.0\")]\n   498:     #[rustc_const_stable(feature = \"const_nonnull_cast\", since = \"1.36.0\")]\n   499:     #[must_use = \"this returns the result of the operation, \\\n   500:                   without modifying the original\"]\n   501:     #[inline]\n   502:     pub const fn cast<U>(self) -> NonNull<U> {\n   503:         // SAFETY: `self` is a `NonNull` pointer which is necessarily non-null\n   504:         unsafe { transmute(self.as_ptr() as *mut U) }\n   505:     }\n   506: \n   507:     /// Try to cast to a pointer of another type by checking alignment.\n   508:     ///\n   509:     /// If the pointer is properly aligned to the target type, it will be\n   510:     /// cast to the target type. Otherwise, `None` is returned.\n   511:     ///\n   512:     /// # Examples\n   513:     ///\n   514:     /// ```rust\n   515:     /// #![feature(pointer_try_cast_aligned)]\n   516:     /// use std::ptr::NonNull;\n   517:     ///\n   518:     /// let mut x = 0u64;",
    "nanvix_source": "   489:     /// let ptr = NonNull::new(&mut x as *mut _).expect(\"null pointer\");\n   490:     ///\n   491:     /// let casted_ptr = ptr.cast::<i8>();\n   492:     /// let raw_ptr: *mut i8 = casted_ptr.as_ptr();\n   493:     /// ```\n   494:     #[stable(feature = \"nonnull_cast\", since = \"1.27.0\")]\n   495:     #[rustc_const_stable(feature = \"const_nonnull_cast\", since = \"1.36.0\")]\n   496:     #[must_use = \"this returns the result of the operation, \\\n   497:                   without modifying the original\"]\n   498:     #[inline]\n   499:     pub const fn cast<U>(self) -> NonNull<U> {\n   500:         // SAFETY: `self` is a `NonNull` pointer which is necessarily non-null\n   501:         unsafe { transmute(self.as_ptr() as *mut U) }\n   502:     }\n   503: \n   504:     /// Try to cast to a pointer of another type by checking alignment.\n   505:     ///\n   506:     /// If the pointer is properly aligned to the target type, it will be\n   507:     /// cast to the target type. Otherwise, `None` is returned.\n   508:     ///\n   509:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::dangling",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "dangling",
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
            "id": 9475,
            "path": "NonNull"
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
        "impl_id": "core:9486",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   113:     /// as a \"not yet initialized\" sentinel value.\n   114:     /// Types that lazily allocate must track initialization by some other means.\n   115:     ///\n   116:     /// # Examples\n   117:     ///\n   118:     /// ```\n   119:     /// use std::ptr::NonNull;\n   120:     ///\n   121:     /// let ptr = NonNull::<u32>::dangling();\n   122:     /// // Important: don't try to access the value of `ptr` without\n   123:     /// // initializing it first! The pointer is not null but isn't valid either!\n   124:     /// ```\n   125:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   126:     #[rustc_const_stable(feature = \"const_nonnull_dangling\", since = \"1.36.0\")]\n   127:     #[must_use]\n   128:     #[inline]\n   129:     pub const fn dangling() -> Self {\n   130:         let align = crate::mem::Alignment::of::<T>();\n   131:         NonNull::without_provenance(align.as_nonzero_usize())\n   132:     }\n   133: \n   134:     /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n   135:     /// [provenance][crate::ptr#provenance].\n   136:     ///\n   137:     /// For more details, see the equivalent method on a raw pointer, [`ptr::with_exposed_provenance_mut`].\n   138:     ///\n   139:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   140:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   141:     #[rustc_const_unstable(feature = \"const_nonnull_with_exposed_provenance\", issue = \"154215\")]\n   142:     #[inline]\n   143:     pub const fn with_exposed_provenance(addr: NonZero<usize>) -> Self {\n   144:         // SAFETY: we know `addr` is non-zero.\n   145:         unsafe {",
    "nanvix_source": "   116:     /// use std::ptr::NonNull;\n   117:     ///\n   118:     /// let ptr = NonNull::<u32>::dangling();\n   119:     /// // Important: don't try to access the value of `ptr` without\n   120:     /// // initializing it first! The pointer is not null but isn't valid either!\n   121:     /// ```\n   122:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   123:     #[rustc_const_stable(feature = \"const_nonnull_dangling\", since = \"1.36.0\")]\n   124:     #[must_use]\n   125:     #[inline]\n   126:     pub const fn dangling() -> Self {\n   127:         let align = crate::mem::Alignment::of::<T>();\n   128:         NonNull::without_provenance(align.as_nonzero_usize())\n   129:     }\n   130: \n   131:     /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n   132:     /// [provenance][crate::ptr#provenance].\n   133:     ///\n   134:     /// For more details, see the equivalent method on a raw pointer, [`ptr::with_exposed_provenance_mut`].\n   135:     ///\n   136:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::expose_provenance",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "expose_provenance",
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1039,
            "path": "NonZero"
          }
        }
      }
    },
    "verification_source": "   330:     #[must_use]\n   331:     #[inline]\n   332:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   333:     pub fn addr(self) -> NonZero<usize> {\n   334:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   335:         // meaning that the address will be non-zero.\n   336:         unsafe { NonZero::new_unchecked(self.as_ptr().addr()) }\n   337:     }\n   338: \n   339:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   340:     /// [`with_exposed_provenance`][NonNull::with_exposed_provenance] and returns the \"address\" portion.\n   341:     ///\n   342:     /// For more details, see the equivalent method on a raw pointer, [`pointer::expose_provenance`].\n   343:     ///\n   344:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   345:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   346:     pub fn expose_provenance(self) -> NonZero<usize> {\n   347:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   348:         // meaning that the address will be non-zero.\n   349:         unsafe { NonZero::new_unchecked(self.as_ptr().expose_provenance()) }\n   350:     }\n   351: \n   352:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   353:     /// `self`.\n   354:     ///\n   355:     /// For more details, see the equivalent method on a raw pointer, [`pointer::with_addr`].\n   356:     ///\n   357:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   358:     #[must_use]\n   359:     #[inline]\n   360:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   361:     pub fn with_addr(self, addr: NonZero<usize>) -> Self {\n   362:         // SAFETY: The result of `ptr::from::with_addr` is non-null because `addr` is guaranteed to be non-zero.",
    "nanvix_source": "   333:         unsafe { NonZero::new_unchecked(self.as_ptr().addr()) }\n   334:     }\n   335: \n   336:     /// Exposes the [\"provenance\"][crate::ptr#provenance] part of the pointer for future use in\n   337:     /// [`with_exposed_provenance`][NonNull::with_exposed_provenance] and returns the \"address\" portion.\n   338:     ///\n   339:     /// For more details, see the equivalent method on a raw pointer, [`pointer::expose_provenance`].\n   340:     ///\n   341:     /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   342:     #[stable(feature = \"nonnull_provenance\", since = \"1.89.0\")]\n   343:     pub fn expose_provenance(self) -> NonZero<usize> {\n   344:         // SAFETY: The pointer is guaranteed by the type to be non-null,\n   345:         // meaning that the address will be non-zero.\n   346:         unsafe { NonZero::new_unchecked(self.as_ptr().expose_provenance()) }\n   347:     }\n   348: \n   349:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   350:     /// `self`.\n   351:     ///\n   352:     /// For more details, see the equivalent method on a raw pointer, [`pointer::with_addr`].\n   353:     ///",
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
