For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::borrow::Cow::into_owned",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
        "is_unsafe": false
      },
      "name": "into_owned",
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
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "B"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 129,
            "path": "Cow"
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
                    },
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 26,
                          "path": "ToOwned"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "B"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:134",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:129",
        "resolved_owner_path": [
          "alloc",
          "borrow",
          "Cow"
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
          "qualified_path": {
            "args": null,
            "name": "Owned",
            "self_type": {
              "generic": "B"
            },
            "trait": {
              "args": null,
              "id": 26,
              "path": "ToOwned"
            }
          }
        }
      }
    },
    "verification_source": "   315:     ///\n   316:     /// Calling `into_owned` on a `Cow::Owned` returns the owned data. The data is moved out of the\n   317:     /// `Cow` without being cloned.\n   318:     ///\n   319:     /// ```\n   320:     /// use std::borrow::Cow;\n   321:     ///\n   322:     /// let s = \"Hello world!\";\n   323:     /// let cow: Cow<'_, str> = Cow::Owned(String::from(s));\n   324:     ///\n   325:     /// assert_eq!(\n   326:     ///   cow.into_owned(),\n   327:     ///   String::from(s)\n   328:     /// );\n   329:     /// ```\n   330:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   331:     pub fn into_owned(self) -> <B as ToOwned>::Owned {\n   332:         match self {\n   333:             Borrowed(borrowed) => borrowed.to_owned(),\n   334:             Owned(owned) => owned,\n   335:         }\n   336:     }\n   337: }\n   338: \n   339: // FIXME(inference): const bounds removed due to inference regressions found by crater;\n   340: //   see https://github.com/rust-lang/rust/issues/147964\n   341: // #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   342: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   343: impl<B: ?Sized + ToOwned> Deref for Cow<'_, B>\n   344: // where\n   345: //     B::Owned: [const] Borrow<B>,\n   346: {\n   347:     type Target = B;",
    "nanvix_source": "   321:     ///\n   322:     /// let s = \"Hello world!\";\n   323:     /// let cow: Cow<'_, str> = Cow::Owned(String::from(s));\n   324:     ///\n   325:     /// assert_eq!(\n   326:     ///   cow.into_owned(),\n   327:     ///   String::from(s)\n   328:     /// );\n   329:     /// ```\n   330:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   331:     pub fn into_owned(self) -> <B as ToOwned>::Owned {\n   332:         match self {\n   333:             Borrowed(borrowed) => borrowed.to_owned(),\n   334:             Owned(owned) => owned,\n   335:         }\n   336:     }\n   337: }\n   338: \n   339: // FIXME(inference): const bounds removed due to inference regressions found by crater;\n   340: //   see https://github.com/rust-lang/rust/issues/147964\n   341: // #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::option::Option::as_deref",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8635,
                      "path": "Deref"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_deref",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
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
        "impl_id": "core:28056",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:84",
        "resolved_owner_path": [
          "core",
          "option",
          "Option"
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
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
    "verification_source": "  1374:     ///\n  1375:     /// Leaves the original Option in-place, creating a new one with a reference\n  1376:     /// to the original one, additionally coercing the contents via [`Deref`].\n  1377:     ///\n  1378:     /// # Examples\n  1379:     ///\n  1380:     /// ```\n  1381:     /// let x: Option<String> = Some(\"hey\".to_owned());\n  1382:     /// assert_eq!(x.as_deref(), Some(\"hey\"));\n  1383:     ///\n  1384:     /// let x: Option<String> = None;\n  1385:     /// assert_eq!(x.as_deref(), None);\n  1386:     /// ```\n  1387:     #[inline]\n  1388:     #[stable(feature = \"option_deref\", since = \"1.40.0\")]\n  1389:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1390:     pub const fn as_deref(&self) -> Option<&T::Target>\n  1391:     where\n  1392:         T: [const] Deref,\n  1393:     {\n  1394:         self.as_ref().map(Deref::deref)\n  1395:     }\n  1396: \n  1397:     /// Converts from `Option<T>` (or `&mut Option<T>`) to `Option<&mut T::Target>`.\n  1398:     ///\n  1399:     /// Leaves the original `Option` in-place, creating a new one containing a mutable reference to\n  1400:     /// the inner type's [`Deref::Target`] type.\n  1401:     ///\n  1402:     /// # Examples\n  1403:     ///\n  1404:     /// ```\n  1405:     /// let mut x: Option<String> = Some(\"hey\".to_owned());\n  1406:     /// assert_eq!(x.as_deref_mut().map(|x| {",
    "nanvix_source": "  1376:     /// ```\n  1377:     /// let x: Option<String> = Some(\"hey\".to_owned());\n  1378:     /// assert_eq!(x.as_deref(), Some(\"hey\"));\n  1379:     ///\n  1380:     /// let x: Option<String> = None;\n  1381:     /// assert_eq!(x.as_deref(), None);\n  1382:     /// ```\n  1383:     #[inline]\n  1384:     #[stable(feature = \"option_deref\", since = \"1.40.0\")]\n  1385:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1386:     pub const fn as_deref(&self) -> Option<&T::Target>\n  1387:     where\n  1388:         T: [const] Deref,\n  1389:     {\n  1390:         self.as_ref().map(Deref::deref)\n  1391:     }\n  1392: \n  1393:     /// Converts from `Option<T>` (or `&mut Option<T>`) to `Option<&mut T::Target>`.\n  1394:     ///\n  1395:     /// Leaves the original `Option` in-place, creating a new one containing a mutable reference to\n  1396:     /// the inner type's [`Deref::Target`] type.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::as_ref",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8635,
                      "path": "Deref"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Ptr"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_ref",
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
                      "generic": "Ptr"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 8635,
                          "path": "Deref"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29034",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "Ptr"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
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
    "verification_source": "  1345:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1346:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1347:     pub const unsafe fn new_unchecked(pointer: Ptr) -> Pin<Ptr> {\n  1348:         Pin { pointer }\n  1349:     }\n  1350: \n  1351:     /// Gets a shared reference to the pinned value this [`Pin`] points to.\n  1352:     ///\n  1353:     /// This is a generic method to go from `&Pin<Pointer<T>>` to `Pin<&T>`.\n  1354:     /// It is safe because, as part of the contract of `Pin::new_unchecked`,\n  1355:     /// the pointee cannot move after `Pin<Pointer<T>>` got created.\n  1356:     /// \"Malicious\" implementations of `Pointer::Deref` are likewise\n  1357:     /// ruled out by the contract of `Pin::new_unchecked`.\n  1358:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1359:     #[inline(always)]\n  1360:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1361:     pub const fn as_ref(&self) -> Pin<&Ptr::Target>\n  1362:     where\n  1363:         Ptr: [const] Deref,\n  1364:     {\n  1365:         // SAFETY: see documentation on this function\n  1366:         unsafe { Pin::new_unchecked(&*self.pointer) }\n  1367:     }\n  1368: }\n  1369: \n  1370: // These methods being in a `Ptr: DerefMut` impl block concerns semver stability.\n  1371: // Currently, calling e.g. `.set()` on a `Pin<&T>` sees that `Ptr: DerefMut`\n  1372: // doesn't hold, and goes to check for a `.set()` method on `T`. But, if the\n  1373: // `where Ptr: DerefMut` bound is moved to the method, rustc sees the impl block\n  1374: // as a valid candidate, and doesn't go on to check other candidates when it\n  1375: // sees that the bound on the method.\n  1376: impl<Ptr: DerefMut> Pin<Ptr> {\n  1377:     /// Gets a mutable reference to the pinned value this `Pin<Ptr>` points to.",
    "nanvix_source": "  1351:     /// Gets a shared reference to the pinned value this [`Pin`] points to.\n  1352:     ///\n  1353:     /// This is a generic method to go from `&Pin<Pointer<T>>` to `Pin<&T>`.\n  1354:     /// It is safe because, as part of the contract of `Pin::new_unchecked`,\n  1355:     /// the pointee cannot move after `Pin<Pointer<T>>` got created.\n  1356:     /// \"Malicious\" implementations of `Pointer::Deref` are likewise\n  1357:     /// ruled out by the contract of `Pin::new_unchecked`.\n  1358:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1359:     #[inline(always)]\n  1360:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1361:     pub const fn as_ref(&self) -> Pin<&Ptr::Target>\n  1362:     where\n  1363:         Ptr: [const] Deref,\n  1364:     {\n  1365:         // SAFETY: see documentation on this function\n  1366:         unsafe { Pin::new_unchecked(&*self.pointer) }\n  1367:     }\n  1368: }\n  1369: \n  1370: // These methods being in a `Ptr: DerefMut` impl block concerns semver stability.\n  1371: // Currently, calling e.g. `.set()` on a `Pin<&T>` sees that `Ptr: DerefMut`",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::set",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "other",
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
                "qualified_path": {
                  "args": null,
                  "name": "Target",
                  "self_type": {
                    "generic": "Ptr"
                  },
                  "trait": {
                    "args": null,
                    "id": 8635,
                    "path": ""
                  }
                }
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
      "name": "set",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                      "generic": "Ptr"
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
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 8650,
                          "path": "DerefMut"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Ptr"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29038",
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
              "qualified_path": {
                "args": null,
                "name": "Target",
                "self_type": {
                  "generic": "Ptr"
                },
                "trait": {
                  "args": null,
                  "id": 8635,
                  "path": ""
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1465:     ///\n  1466:     /// # Example\n  1467:     ///\n  1468:     /// ```\n  1469:     /// use std::pin::Pin;\n  1470:     ///\n  1471:     /// let mut val: u8 = 5;\n  1472:     /// let mut pinned: Pin<&mut u8> = Pin::new(&mut val);\n  1473:     /// println!(\"{}\", pinned); // 5\n  1474:     /// pinned.set(10);\n  1475:     /// println!(\"{}\", pinned); // 10\n  1476:     /// ```\n  1477:     ///\n  1478:     /// [subtle-details]: self#subtle-details-and-the-drop-guarantee\n  1479:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1480:     #[inline(always)]\n  1481:     pub fn set(&mut self, value: Ptr::Target)\n  1482:     where\n  1483:         Ptr::Target: Sized,\n  1484:     {\n  1485:         *(self.pointer) = value;\n  1486:     }\n  1487: }\n  1488: \n  1489: impl<Ptr: Deref> Pin<Ptr> {\n  1490:     /// Unwraps this `Pin<Ptr>`, returning the underlying `Ptr`.\n  1491:     ///\n  1492:     /// # Safety\n  1493:     ///\n  1494:     /// This function is unsafe. You must guarantee that you will continue to\n  1495:     /// treat the pointer `Ptr` as pinned after you call this function, so that\n  1496:     /// the invariants on the `Pin` type can be upheld. If the code using the\n  1497:     /// resulting `Ptr` does not continue to maintain the pinning invariants that",
    "nanvix_source": "  1471:     /// let mut val: u8 = 5;\n  1472:     /// let mut pinned: Pin<&mut u8> = Pin::new(&mut val);\n  1473:     /// println!(\"{}\", pinned); // 5\n  1474:     /// pinned.set(10);\n  1475:     /// println!(\"{}\", pinned); // 10\n  1476:     /// ```\n  1477:     ///\n  1478:     /// [subtle-details]: self#subtle-details-and-the-drop-guarantee\n  1479:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1480:     #[inline(always)]\n  1481:     pub fn set(&mut self, value: Ptr::Target)\n  1482:     where\n  1483:         Ptr::Target: Sized,\n  1484:     {\n  1485:         *(self.pointer) = value;\n  1486:     }\n  1487: }\n  1488: \n  1489: impl<Ptr: Deref> Pin<Ptr> {\n  1490:     /// Unwraps this `Pin<Ptr>`, returning the underlying `Ptr`.\n  1491:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::result::Result::as_deref",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 8635,
                      "path": "Deref"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "as_deref",
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
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "qualified_path": {
                            "args": null,
                            "name": "Target",
                            "self_type": {
                              "generic": "T"
                            },
                            "trait": {
                              "args": null,
                              "id": 8635,
                              "path": ""
                            }
                          }
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "generic": "E"
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
    "verification_source": "  1030:     /// and returns the new [`Result`].\n  1031:     ///\n  1032:     /// # Examples\n  1033:     ///\n  1034:     /// ```\n  1035:     /// let x: Result<String, u32> = Ok(\"hello\".to_string());\n  1036:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1037:     /// assert_eq!(x.as_deref(), y);\n  1038:     ///\n  1039:     /// let x: Result<String, u32> = Err(42);\n  1040:     /// let y: Result<&str, &u32> = Err(&42);\n  1041:     /// assert_eq!(x.as_deref(), y);\n  1042:     /// ```\n  1043:     #[inline]\n  1044:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1045:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1046:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1047:     where\n  1048:         T: [const] Deref,\n  1049:     {\n  1050:         self.as_ref().map(Deref::deref)\n  1051:     }\n  1052: \n  1053:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1054:     ///\n  1055:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1056:     /// and returns the new [`Result`].\n  1057:     ///\n  1058:     /// # Examples\n  1059:     ///\n  1060:     /// ```\n  1061:     /// let mut s = \"HELLO\".to_string();\n  1062:     /// let mut x: Result<String, u32> = Ok(\"hello\".to_string());",
    "nanvix_source": "  1034:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1035:     /// assert_eq!(x.as_deref(), y);\n  1036:     ///\n  1037:     /// let x: Result<String, u32> = Err(42);\n  1038:     /// let y: Result<&str, &u32> = Err(&42);\n  1039:     /// assert_eq!(x.as_deref(), y);\n  1040:     /// ```\n  1041:     #[inline]\n  1042:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1043:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1044:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1045:     where\n  1046:         T: [const] Deref,\n  1047:     {\n  1048:         self.as_ref().map(Deref::deref)\n  1049:     }\n  1050: \n  1051:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1052:     ///\n  1053:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1054:     /// and returns the new [`Result`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::ends_with",
    "generation_group": "associated_type_or_projection",
    "classification": "associated_type_or_projection",
    "classification_reasons": [
      "associated_type_signature_requires_manual_integration"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
                        "id": 10099,
                        "path": "Pattern"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
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
                        "angle_bracketed": {
                          "args": [
                            {
                              "lifetime": "'a"
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 27488,
                      "path": "ReverseSearcher"
                    }
                  }
                }
              ],
              "generic_params": [
                {
                  "kind": {
                    "lifetime": {
                      "outlives": []
                    }
                  },
                  "name": "'a"
                }
              ],
              "type": {
                "qualified_path": {
                  "args": {
                    "angle_bracketed": {
                      "args": [
                        {
                          "lifetime": "'a"
                        }
                      ],
                      "constraints": []
                    }
                  },
                  "name": "Searcher",
                  "self_type": {
                    "generic": "P"
                  },
                  "trait": {
                    "args": null,
                    "id": 10099,
                    "path": ""
                  }
                }
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
      "name": "ends_with",
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
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
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
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "pat",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1410:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1411:     /// function or closure that determines if a character matches.\n  1412:     ///\n  1413:     /// [`char`]: prim@char\n  1414:     /// [pattern]: self::pattern\n  1415:     ///\n  1416:     /// # Examples\n  1417:     ///\n  1418:     /// ```\n  1419:     /// let bananas = \"bananas\";\n  1420:     ///\n  1421:     /// assert!(bananas.ends_with(\"anas\"));\n  1422:     /// assert!(!bananas.ends_with(\"nana\"));\n  1423:     /// ```\n  1424:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1425:     #[rustc_diagnostic_item = \"str_ends_with\"]\n  1426:     pub fn ends_with<P: Pattern>(&self, pat: P) -> bool\n  1427:     where\n  1428:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1429:     {\n  1430:         pat.is_suffix_of(self)\n  1431:     }\n  1432: \n  1433:     /// Returns the byte index of the first character of this string slice that\n  1434:     /// matches the pattern.\n  1435:     ///\n  1436:     /// Returns [`None`] if the pattern doesn't match.\n  1437:     ///\n  1438:     /// The [pattern] can be a `&str`, [`char`], a slice of [`char`]s, or a\n  1439:     /// function or closure that determines if a character matches.\n  1440:     ///\n  1441:     /// [`char`]: prim@char\n  1442:     /// [pattern]: self::pattern",
    "nanvix_source": "  1435:     /// # Examples\n  1436:     ///\n  1437:     /// ```\n  1438:     /// let bananas = \"bananas\";\n  1439:     ///\n  1440:     /// assert!(bananas.ends_with(\"anas\"));\n  1441:     /// assert!(!bananas.ends_with(\"nana\"));\n  1442:     /// ```\n  1443:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1444:     #[rustc_diagnostic_item = \"str_ends_with\"]\n  1445:     pub fn ends_with<P: Pattern>(&self, pat: P) -> bool\n  1446:     where\n  1447:         for<'a> P::Searcher<'a>: ReverseSearcher<'a>,\n  1448:     {\n  1449:         pat.is_suffix_of(self)\n  1450:     }\n  1451: \n  1452:     /// Returns the byte index of the first character of this string slice that\n  1453:     /// matches the pattern.\n  1454:     ///\n  1455:     /// Returns [`None`] if the pattern doesn't match.",
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
