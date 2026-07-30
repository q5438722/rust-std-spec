For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::ffi::CString::from_vec_with_nul_unchecked",
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
      "name": "from_vec_with_nul_unchecked",
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
    "verification_source": "   619:     /// # Safety\n   620:     ///\n   621:     /// The given [`Vec`] **must** have one nul byte as its last element.\n   622:     /// This means it cannot be empty nor have any other nul byte anywhere else.\n   623:     ///\n   624:     /// # Example\n   625:     ///\n   626:     /// ```\n   627:     /// use std::ffi::CString;\n   628:     /// assert_eq!(\n   629:     ///     unsafe { CString::from_vec_with_nul_unchecked(b\"abc\\0\".to_vec()) },\n   630:     ///     unsafe { CString::from_vec_unchecked(b\"abc\".to_vec()) }\n   631:     /// );\n   632:     /// ```\n   633:     #[must_use]\n   634:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   635:     pub unsafe fn from_vec_with_nul_unchecked(v: Vec<u8>) -> Self {\n   636:         debug_assert!(memchr::memchr(0, &v).unwrap() + 1 == v.len());\n   637:         unsafe { Self::_from_vec_with_nul_unchecked(v) }\n   638:     }\n   639: \n   640:     unsafe fn _from_vec_with_nul_unchecked(v: Vec<u8>) -> Self {\n   641:         Self { inner: v.into_boxed_slice() }\n   642:     }\n   643: \n   644:     /// Attempts to convert a <code>[Vec]<[u8]></code> to a [`CString`].\n   645:     ///\n   646:     /// Runtime checks are present to ensure there is only one nul byte in the\n   647:     /// [`Vec`], its last element.\n   648:     ///\n   649:     /// # Errors\n   650:     ///\n   651:     /// If a nul byte is present and not the last element or no nul bytes",
    "nanvix_source": "   625:     ///\n   626:     /// ```\n   627:     /// use std::ffi::CString;\n   628:     /// assert_eq!(\n   629:     ///     unsafe { CString::from_vec_with_nul_unchecked(b\"abc\\0\".to_vec()) },\n   630:     ///     unsafe { CString::from_vec_unchecked(b\"abc\".to_vec()) }\n   631:     /// );\n   632:     /// ```\n   633:     #[must_use]\n   634:     #[stable(feature = \"cstring_from_vec_with_nul\", since = \"1.58.0\")]\n   635:     pub unsafe fn from_vec_with_nul_unchecked(v: Vec<u8>) -> Self {\n   636:         debug_assert!(memchr::memchr(0, &v).unwrap() + 1 == v.len());\n   637:         unsafe { Self::_from_vec_with_nul_unchecked(v) }\n   638:     }\n   639: \n   640:     unsafe fn _from_vec_with_nul_unchecked(v: Vec<u8>) -> Self {\n   641:         Self { inner: v.into_boxed_slice() }\n   642:     }\n   643: \n   644:     /// Attempts to convert a <code>[Vec]<[u8]></code> to a [`CString`].\n   645:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::ffi::CString::into_raw",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "other",
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
            "self",
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
              "resolved_path": {
                "args": null,
                "id": 3297,
                "path": "c_char"
              }
            }
          }
        }
      }
    },
    "verification_source": "   439:     ///\n   440:     /// let ptr = c_string.into_raw();\n   441:     ///\n   442:     /// unsafe {\n   443:     ///     assert_eq!(b'f', *ptr as u8);\n   444:     ///     assert_eq!(b'o', *ptr.add(1) as u8);\n   445:     ///     assert_eq!(b'o', *ptr.add(2) as u8);\n   446:     ///     assert_eq!(b'\\0', *ptr.add(3) as u8);\n   447:     ///\n   448:     ///     // retake pointer to free memory\n   449:     ///     let _ = CString::from_raw(ptr);\n   450:     /// }\n   451:     /// ```\n   452:     #[inline]\n   453:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   454:     #[stable(feature = \"cstr_memory\", since = \"1.4.0\")]\n   455:     pub fn into_raw(self) -> *mut c_char {\n   456:         Box::into_raw(self.into_inner()) as *mut c_char\n   457:     }\n   458: \n   459:     /// Converts the `CString` into a [`String`] if it contains valid UTF-8 data.\n   460:     ///\n   461:     /// On failure, ownership of the original `CString` is returned.\n   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```\n   466:     /// use std::ffi::CString;\n   467:     ///\n   468:     /// let valid_utf8 = vec![b'f', b'o', b'o'];\n   469:     /// let cstring = CString::new(valid_utf8).expect(\"CString::new failed\");\n   470:     /// assert_eq!(cstring.into_string().expect(\"into_string() call failed\"), \"foo\");\n   471:     ///",
    "nanvix_source": "   445:     ///     assert_eq!(b'o', *ptr.add(2) as u8);\n   446:     ///     assert_eq!(b'\\0', *ptr.add(3) as u8);\n   447:     ///\n   448:     ///     // retake pointer to free memory\n   449:     ///     let _ = CString::from_raw(ptr);\n   450:     /// }\n   451:     /// ```\n   452:     #[inline]\n   453:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   454:     #[stable(feature = \"cstr_memory\", since = \"1.4.0\")]\n   455:     pub fn into_raw(self) -> *mut c_char {\n   456:         Box::into_raw(self.into_inner()) as *mut c_char\n   457:     }\n   458: \n   459:     /// Converts the `CString` into a [`String`] if it contains valid UTF-8 data.\n   460:     ///\n   461:     /// On failure, ownership of the original `CString` is returned.\n   462:     ///\n   463:     /// # Examples\n   464:     ///\n   465:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::as_ptr",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3610",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "this",
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
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1647:     /// The counts are not affected in any way and the `Rc` is not consumed. The pointer is valid\n  1648:     /// for as long as there are strong counts in the `Rc`.\n  1649:     ///\n  1650:     /// # Examples\n  1651:     ///\n  1652:     /// ```\n  1653:     /// use std::rc::Rc;\n  1654:     ///\n  1655:     /// let x = Rc::new(0);\n  1656:     /// let y = Rc::clone(&x);\n  1657:     /// let x_ptr = Rc::as_ptr(&x);\n  1658:     /// assert_eq!(x_ptr, Rc::as_ptr(&y));\n  1659:     /// assert_eq!(unsafe { *x_ptr }, 0);\n  1660:     /// ```\n  1661:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  1662:     #[rustc_never_returns_null_ptr]\n  1663:     pub fn as_ptr(this: &Self) -> *const T {\n  1664:         let ptr: *mut RcInner<T> = NonNull::as_ptr(this.ptr);\n  1665: \n  1666:         // SAFETY: This cannot go through Deref::deref or Rc::inner because\n  1667:         // this is required to retain raw/mut provenance such that e.g. `get_mut` can\n  1668:         // write through the pointer after the Rc is recovered through `from_raw`.\n  1669:         unsafe { &raw mut (*ptr).value }\n  1670:     }\n  1671: \n  1672:     /// Constructs an `Rc<T, A>` from a raw pointer in the provided allocator.\n  1673:     ///\n  1674:     /// The raw pointer must have been previously returned by a call to [`Rc<U,\n  1675:     /// A>::into_raw`][into_raw] or [`Rc<U, A>::into_raw_with_allocator`][into_raw_with_allocator].\n  1676:     ///\n  1677:     /// # Safety\n  1678:     ///\n  1679:     /// * Creating a `Rc<T, A>` from a pointer other than one returned from",
    "nanvix_source": "  1659:     /// use std::rc::Rc;\n  1660:     ///\n  1661:     /// let x = Rc::new(0);\n  1662:     /// let y = Rc::clone(&x);\n  1663:     /// let x_ptr = Rc::as_ptr(&x);\n  1664:     /// assert_eq!(x_ptr, Rc::as_ptr(&y));\n  1665:     /// assert_eq!(unsafe { *x_ptr }, 0);\n  1666:     /// ```\n  1667:     #[stable(feature = \"weak_into_raw\", since = \"1.45.0\")]\n  1668:     #[rustc_never_returns_null_ptr]\n  1669:     pub fn as_ptr(this: &Self) -> *const T {\n  1670:         let ptr: *mut RcInner<T> = NonNull::as_ptr(this.ptr);\n  1671: \n  1672:         // SAFETY: This cannot go through Deref::deref or Rc::inner because\n  1673:         // this is required to retain raw/mut provenance such that e.g. `get_mut` can\n  1674:         // write through the pointer after the Rc is recovered through `from_raw`.\n  1675:         unsafe { &raw mut (*ptr).value }\n  1676:     }\n  1677: \n  1678:     /// Constructs an `Rc<T, A>` from a raw pointer in the provided allocator.\n  1679:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::assume_init",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3582",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
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
            "id": 302,
            "path": "Rc"
          }
        }
      }
    },
    "verification_source": "  1278:     /// # Examples\n  1279:     ///\n  1280:     /// ```\n  1281:     /// use std::rc::Rc;\n  1282:     ///\n  1283:     /// let mut five = Rc::<u32>::new_uninit();\n  1284:     ///\n  1285:     /// // Deferred initialization:\n  1286:     /// Rc::get_mut(&mut five).unwrap().write(5);\n  1287:     ///\n  1288:     /// let five = unsafe { five.assume_init() };\n  1289:     ///\n  1290:     /// assert_eq!(*five, 5)\n  1291:     /// ```\n  1292:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1293:     #[inline]\n  1294:     pub unsafe fn assume_init(self) -> Rc<T, A> {\n  1295:         let (ptr, alloc) = Rc::into_inner_with_allocator(self);\n  1296:         unsafe { Rc::from_inner_in(ptr.cast(), alloc) }\n  1297:     }\n  1298: }\n  1299: \n  1300: impl<T: ?Sized + CloneToUninit> Rc<T> {\n  1301:     /// Constructs a new `Rc<T>` with a clone of `value`.\n  1302:     ///\n  1303:     /// # Examples\n  1304:     ///\n  1305:     /// ```\n  1306:     /// #![feature(clone_from_ref)]\n  1307:     /// use std::rc::Rc;\n  1308:     ///\n  1309:     /// let hello: Rc<str> = Rc::clone_from_ref(\"hello\");\n  1310:     /// ```",
    "nanvix_source": "  1292:     ///\n  1293:     /// // Deferred initialization:\n  1294:     /// Rc::get_mut(&mut five).unwrap().write(5);\n  1295:     ///\n  1296:     /// let five = unsafe { five.assume_init() };\n  1297:     ///\n  1298:     /// assert_eq!(*five, 5)\n  1299:     /// ```\n  1300:     #[stable(feature = \"new_uninit\", since = \"1.82.0\")]\n  1301:     #[inline]\n  1302:     pub unsafe fn assume_init(self) -> Rc<T, A> {\n  1303:         let (ptr, alloc) = Rc::into_inner_with_allocator(self);\n  1304:         unsafe { Rc::from_inner_in(ptr.cast(), alloc) }\n  1305:     }\n  1306: }\n  1307: \n  1308: impl<T: ?Sized + CloneToUninit> Rc<T> {\n  1309:     /// Constructs a new `Rc<T>` with a clone of `value`.\n  1310:     ///\n  1311:     /// # Examples\n  1312:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::decrement_strong_count",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
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
        "is_unsafe": true
      },
      "name": "decrement_strong_count",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3598",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1584:     /// use std::rc::Rc;\n  1585:     ///\n  1586:     /// let five = Rc::new(5);\n  1587:     ///\n  1588:     /// unsafe {\n  1589:     ///     let ptr = Rc::into_raw(five);\n  1590:     ///     Rc::increment_strong_count(ptr);\n  1591:     ///\n  1592:     ///     let five = Rc::from_raw(ptr);\n  1593:     ///     assert_eq!(2, Rc::strong_count(&five));\n  1594:     ///     Rc::decrement_strong_count(ptr);\n  1595:     ///     assert_eq!(1, Rc::strong_count(&five));\n  1596:     /// }\n  1597:     /// ```\n  1598:     #[inline]\n  1599:     #[stable(feature = \"rc_mutate_strong_count\", since = \"1.53.0\")]\n  1600:     pub unsafe fn decrement_strong_count(ptr: *const T) {\n  1601:         unsafe { Self::decrement_strong_count_in(ptr, Global) }\n  1602:     }\n  1603: }\n  1604: \n  1605: impl<T: ?Sized, A: Allocator> Rc<T, A> {\n  1606:     /// Returns a reference to the underlying allocator.\n  1607:     ///\n  1608:     /// Note: this is an associated function, which means that you have\n  1609:     /// to call it as `Rc::allocator(&r)` instead of `r.allocator()`. This\n  1610:     /// is so that there is no conflict with a method on the inner type.\n  1611:     #[inline]\n  1612:     #[unstable(feature = \"allocator_api\", issue = \"32838\")]\n  1613:     pub fn allocator(this: &Self) -> &A {\n  1614:         &this.alloc\n  1615:     }\n  1616: ",
    "nanvix_source": "  1596:     ///     Rc::increment_strong_count(ptr);\n  1597:     ///\n  1598:     ///     let five = Rc::from_raw(ptr);\n  1599:     ///     assert_eq!(2, Rc::strong_count(&five));\n  1600:     ///     Rc::decrement_strong_count(ptr);\n  1601:     ///     assert_eq!(1, Rc::strong_count(&five));\n  1602:     /// }\n  1603:     /// ```\n  1604:     #[inline]\n  1605:     #[stable(feature = \"rc_mutate_strong_count\", since = \"1.53.0\")]\n  1606:     pub unsafe fn decrement_strong_count(ptr: *const T) {\n  1607:         unsafe { Self::decrement_strong_count_in(ptr, Global) }\n  1608:     }\n  1609: }\n  1610: \n  1611: impl<T: ?Sized, A: Allocator> Rc<T, A> {\n  1612:     /// Returns a reference to the underlying allocator.\n  1613:     ///\n  1614:     /// Note: this is an associated function, which means that you have\n  1615:     /// to call it as `Rc::allocator(&r)` instead of `r.allocator()`. This\n  1616:     /// is so that there is no conflict with a method on the inner type.",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Rc::from_raw",
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
            "id": 302,
            "path": "Rc"
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
        "impl_id": "alloc:3598",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:302",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Rc"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
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
    "verification_source": "  1487:     ///\n  1488:     /// Convert a slice back into its original array:\n  1489:     ///\n  1490:     /// ```\n  1491:     /// use std::rc::Rc;\n  1492:     ///\n  1493:     /// let x: Rc<[u32]> = Rc::new([1, 2, 3]);\n  1494:     /// let x_ptr: *const [u32] = Rc::into_raw(x);\n  1495:     ///\n  1496:     /// unsafe {\n  1497:     ///     let x: Rc<[u32; 3]> = Rc::from_raw(x_ptr.cast::<[u32; 3]>());\n  1498:     ///     assert_eq!(&*x, &[1, 2, 3]);\n  1499:     /// }\n  1500:     /// ```\n  1501:     #[inline]\n  1502:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1503:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  1504:         unsafe { Self::from_raw_in(ptr, Global) }\n  1505:     }\n  1506: \n  1507:     /// Consumes the `Rc`, returning the wrapped pointer.\n  1508:     ///\n  1509:     /// To avoid a memory leak the pointer must be converted back to an `Rc` using\n  1510:     /// [`Rc::from_raw`].\n  1511:     ///\n  1512:     /// # Examples\n  1513:     ///\n  1514:     /// ```\n  1515:     /// use std::rc::Rc;\n  1516:     ///\n  1517:     /// let x = Rc::new(\"hello\".to_owned());\n  1518:     /// let x_ptr = Rc::into_raw(x);\n  1519:     /// assert_eq!(unsafe { &*x_ptr }, \"hello\");",
    "nanvix_source": "  1501:     /// let x: Rc<[u32]> = Rc::new([1, 2, 3]);\n  1502:     /// let x_ptr: *const [u32] = Rc::into_raw(x);\n  1503:     ///\n  1504:     /// unsafe {\n  1505:     ///     let x: Rc<[u32; 3]> = Rc::from_raw(x_ptr.cast::<[u32; 3]>());\n  1506:     ///     assert_eq!(&*x, &[1, 2, 3]);\n  1507:     /// }\n  1508:     /// ```\n  1509:     #[inline]\n  1510:     #[stable(feature = \"rc_raw\", since = \"1.17.0\")]\n  1511:     pub unsafe fn from_raw(ptr: *const T) -> Self {\n  1512:         unsafe { Self::from_raw_in(ptr, Global) }\n  1513:     }\n  1514: \n  1515:     /// Consumes the `Rc`, returning the wrapped pointer.\n  1516:     ///\n  1517:     /// To avoid a memory leak the pointer must be converted back to an `Rc` using\n  1518:     /// [`Rc::from_raw`].\n  1519:     ///\n  1520:     /// # Examples\n  1521:     ///",
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
