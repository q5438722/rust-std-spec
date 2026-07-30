For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::rc::Weak::upgrade",
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
                      "id": 25,
                      "path": "Clone"
                    }
                  }
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
      "name": "upgrade",
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
            "id": 3551,
            "path": "Weak"
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
        "impl_id": "alloc:3747",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
                ],
                "constraints": []
              }
            },
            "id": 181,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  3511:     /// let five = Rc::new(5);\n  3512:     ///\n  3513:     /// let weak_five = Rc::downgrade(&five);\n  3514:     ///\n  3515:     /// let strong_five: Option<Rc<_>> = weak_five.upgrade();\n  3516:     /// assert!(strong_five.is_some());\n  3517:     ///\n  3518:     /// // Destroy all strong pointers.\n  3519:     /// drop(strong_five);\n  3520:     /// drop(five);\n  3521:     ///\n  3522:     /// assert!(weak_five.upgrade().is_none());\n  3523:     /// ```\n  3524:     #[must_use = \"this returns a new `Rc`, \\\n  3525:                   without modifying the original weak pointer\"]\n  3526:     #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  3527:     pub fn upgrade(&self) -> Option<Rc<T, A>>\n  3528:     where\n  3529:         A: Clone,\n  3530:     {\n  3531:         let inner = self.inner()?;\n  3532: \n  3533:         if inner.strong() == 0 {\n  3534:             None\n  3535:         } else {\n  3536:             unsafe {\n  3537:                 inner.inc_strong();\n  3538:                 Some(Rc::from_inner_in(self.ptr, self.alloc.clone()))\n  3539:             }\n  3540:         }\n  3541:     }\n  3542: \n  3543:     /// Gets the number of strong (`Rc`) pointers pointing to this allocation.",
    "nanvix_source": "  3532:     ///\n  3533:     /// // Destroy all strong pointers.\n  3534:     /// drop(strong_five);\n  3535:     /// drop(five);\n  3536:     ///\n  3537:     /// assert!(weak_five.upgrade().is_none());\n  3538:     /// ```\n  3539:     #[must_use = \"this returns a new `Rc`, \\\n  3540:                   without modifying the original weak pointer\"]\n  3541:     #[stable(feature = \"rc_weak\", since = \"1.4.0\")]\n  3542:     pub fn upgrade(&self) -> Option<Rc<T, A>>\n  3543:     where\n  3544:         A: Clone,\n  3545:     {\n  3546:         let inner = self.inner()?;\n  3547: \n  3548:         if inner.strong() == 0 {\n  3549:             None\n  3550:         } else {\n  3551:             unsafe {\n  3552:                 inner.inc_strong();",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::rc::Weak::weak_count",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "weak_count",
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
            "id": 3551,
            "path": "Weak"
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
        "impl_id": "alloc:3747",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:3551",
        "resolved_owner_path": [
          "alloc",
          "rc",
          "Weak"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  3541:     }\n  3542: \n  3543:     /// Gets the number of strong (`Rc`) pointers pointing to this allocation.\n  3544:     ///\n  3545:     /// If `self` was created using [`Weak::new`], this will return 0.\n  3546:     #[must_use]\n  3547:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3548:     pub fn strong_count(&self) -> usize {\n  3549:         if let Some(inner) = self.inner() { inner.strong() } else { 0 }\n  3550:     }\n  3551: \n  3552:     /// Gets the number of `Weak` pointers pointing to this allocation.\n  3553:     ///\n  3554:     /// If no strong pointers remain, this will return zero.\n  3555:     #[must_use]\n  3556:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3557:     pub fn weak_count(&self) -> usize {\n  3558:         if let Some(inner) = self.inner() {\n  3559:             if inner.strong() > 0 {\n  3560:                 inner.weak() - 1 // subtract the implicit weak ptr\n  3561:             } else {\n  3562:                 0\n  3563:             }\n  3564:         } else {\n  3565:             0\n  3566:         }\n  3567:     }\n  3568: \n  3569:     /// Returns `None` when the pointer is dangling and there is no allocated `RcInner`,\n  3570:     /// (i.e., when this `Weak` was created by `Weak::new`).\n  3571:     #[inline]\n  3572:     fn inner(&self) -> Option<WeakInner<'_>> {\n  3573:         if is_dangling(self.ptr.as_ptr()) {",
    "nanvix_source": "  3562:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3563:     pub fn strong_count(&self) -> usize {\n  3564:         if let Some(inner) = self.inner() { inner.strong() } else { 0 }\n  3565:     }\n  3566: \n  3567:     /// Gets the number of `Weak` pointers pointing to this allocation.\n  3568:     ///\n  3569:     /// If no strong pointers remain, this will return zero.\n  3570:     #[must_use]\n  3571:     #[stable(feature = \"weak_counts\", since = \"1.41.0\")]\n  3572:     pub fn weak_count(&self) -> usize {\n  3573:         if let Some(inner) = self.inner() {\n  3574:             if inner.strong() > 0 {\n  3575:                 inner.weak() - 1 // subtract the implicit weak ptr\n  3576:             } else {\n  3577:                 0\n  3578:             }\n  3579:         } else {\n  3580:             0\n  3581:         }\n  3582:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::Drain::as_str",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_str",
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 4066,
            "path": "Drain"
          }
        },
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
          "where_predicates": []
        },
        "impl_id": "alloc:4318",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:4066",
        "resolved_owner_path": [
          "alloc",
          "string",
          "Drain"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "primitive": "str"
            }
          }
        }
      }
    },
    "verification_source": "  3526: }\n  3527: \n  3528: impl<'a> Drain<'a> {\n  3529:     /// Returns the remaining (sub)string of this iterator as a slice.\n  3530:     ///\n  3531:     /// # Examples\n  3532:     ///\n  3533:     /// ```\n  3534:     /// let mut s = String::from(\"abc\");\n  3535:     /// let mut drain = s.drain(..);\n  3536:     /// assert_eq!(drain.as_str(), \"abc\");\n  3537:     /// let _ = drain.next().unwrap();\n  3538:     /// assert_eq!(drain.as_str(), \"bc\");\n  3539:     /// ```\n  3540:     #[must_use]\n  3541:     #[stable(feature = \"string_drain_as_str\", since = \"1.55.0\")]\n  3542:     pub fn as_str(&self) -> &str {\n  3543:         self.iter.as_str()\n  3544:     }\n  3545: }\n  3546: \n  3547: #[stable(feature = \"string_drain_as_str\", since = \"1.55.0\")]\n  3548: impl<'a> AsRef<str> for Drain<'a> {\n  3549:     fn as_ref(&self) -> &str {\n  3550:         self.as_str()\n  3551:     }\n  3552: }\n  3553: \n  3554: #[stable(feature = \"string_drain_as_str\", since = \"1.55.0\")]\n  3555: impl<'a> AsRef<[u8]> for Drain<'a> {\n  3556:     fn as_ref(&self) -> &[u8] {\n  3557:         self.as_str().as_bytes()\n  3558:     }",
    "nanvix_source": "  3559:     ///\n  3560:     /// ```\n  3561:     /// let mut s = String::from(\"abc\");\n  3562:     /// let mut drain = s.drain(..);\n  3563:     /// assert_eq!(drain.as_str(), \"abc\");\n  3564:     /// let _ = drain.next().unwrap();\n  3565:     /// assert_eq!(drain.as_str(), \"bc\");\n  3566:     /// ```\n  3567:     #[must_use]\n  3568:     #[stable(feature = \"string_drain_as_str\", since = \"1.55.0\")]\n  3569:     pub fn as_str(&self) -> &str {\n  3570:         self.iter.as_str()\n  3571:     }\n  3572: }\n  3573: \n  3574: #[stable(feature = \"string_drain_as_str\", since = \"1.55.0\")]\n  3575: impl<'a> AsRef<str> for Drain<'a> {\n  3576:     fn as_ref(&self) -> &str {\n  3577:         self.as_str()\n  3578:     }\n  3579: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::FromUtf8Error::as_bytes",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "as_bytes",
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
            "args": null,
            "id": 963,
            "path": "FromUtf8Error"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4227",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:963",
        "resolved_owner_path": [
          "alloc",
          "string",
          "FromUtf8Error"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2210: \n  2211: impl FromUtf8Error {\n  2212:     /// Returns a slice of [`u8`]s bytes that were attempted to convert to a `String`.\n  2213:     ///\n  2214:     /// # Examples\n  2215:     ///\n  2216:     /// ```\n  2217:     /// // some invalid bytes, in a vector\n  2218:     /// let bytes = vec![0, 159];\n  2219:     ///\n  2220:     /// let value = String::from_utf8(bytes);\n  2221:     ///\n  2222:     /// assert_eq!(&[0, 159], value.unwrap_err().as_bytes());\n  2223:     /// ```\n  2224:     #[must_use]\n  2225:     #[stable(feature = \"from_utf8_error_as_bytes\", since = \"1.26.0\")]\n  2226:     pub fn as_bytes(&self) -> &[u8] {\n  2227:         &self.bytes[..]\n  2228:     }\n  2229: \n  2230:     /// Converts the bytes into a `String` lossily, substituting invalid UTF-8\n  2231:     /// sequences with replacement characters.\n  2232:     ///\n  2233:     /// See [`String::from_utf8_lossy`] for more details on replacement of\n  2234:     /// invalid sequences, and [`String::from_utf8_lossy_owned`] for the\n  2235:     /// `String` function which corresponds to this function.\n  2236:     ///\n  2237:     /// # Examples\n  2238:     ///\n  2239:     /// ```\n  2240:     /// #![feature(string_from_utf8_lossy_owned)]\n  2241:     /// // some invalid bytes\n  2242:     /// let input: Vec<u8> = b\"Hello \\xF0\\x90\\x80World\".into();",
    "nanvix_source": "  2221:     /// ```\n  2222:     /// // some invalid bytes, in a vector\n  2223:     /// let bytes = vec![0, 159];\n  2224:     ///\n  2225:     /// let value = String::from_utf8(bytes);\n  2226:     ///\n  2227:     /// assert_eq!(&[0, 159], value.unwrap_err().as_bytes());\n  2228:     /// ```\n  2229:     #[must_use]\n  2230:     #[stable(feature = \"from_utf8_error_as_bytes\", since = \"1.26.0\")]\n  2231:     pub fn as_bytes(&self) -> &[u8] {\n  2232:         &self.bytes[..]\n  2233:     }\n  2234: \n  2235:     /// Converts the bytes into a `String` lossily, substituting invalid UTF-8\n  2236:     /// sequences with replacement characters.\n  2237:     ///\n  2238:     /// See [`String::from_utf8_lossy`] for more details on replacement of\n  2239:     /// invalid sequences, and [`String::from_utf8_lossy_owned`] for the\n  2240:     /// `String` function which corresponds to this function.\n  2241:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::FromUtf8Error::into_bytes",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "into_bytes",
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
            "id": 963,
            "path": "FromUtf8Error"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4227",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:963",
        "resolved_owner_path": [
          "alloc",
          "string",
          "FromUtf8Error"
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
      }
    },
    "verification_source": "  2280:     /// This method is carefully constructed to avoid allocation. It will\n  2281:     /// consume the error, moving out the bytes, so that a copy of the bytes\n  2282:     /// does not need to be made.\n  2283:     ///\n  2284:     /// # Examples\n  2285:     ///\n  2286:     /// ```\n  2287:     /// // some invalid bytes, in a vector\n  2288:     /// let bytes = vec![0, 159];\n  2289:     ///\n  2290:     /// let value = String::from_utf8(bytes);\n  2291:     ///\n  2292:     /// assert_eq!(vec![0, 159], value.unwrap_err().into_bytes());\n  2293:     /// ```\n  2294:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2295:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2296:     pub fn into_bytes(self) -> Vec<u8> {\n  2297:         self.bytes\n  2298:     }\n  2299: \n  2300:     /// Fetch a `Utf8Error` to get more details about the conversion failure.\n  2301:     ///\n  2302:     /// The [`Utf8Error`] type provided by [`std::str`] represents an error that may\n  2303:     /// occur when converting a slice of [`u8`]s to a [`&str`]. In this sense, it's\n  2304:     /// an analogue to `FromUtf8Error`. See its documentation for more details\n  2305:     /// on using it.\n  2306:     ///\n  2307:     /// [`std::str`]: core::str \"std::str\"\n  2308:     /// [`&str`]: prim@str \"&str\"\n  2309:     ///\n  2310:     /// # Examples\n  2311:     ///\n  2312:     /// ```",
    "nanvix_source": "  2309:     /// ```\n  2310:     /// // some invalid bytes, in a vector\n  2311:     /// let bytes = vec![0, 159];\n  2312:     ///\n  2313:     /// let value = String::from_utf8(bytes);\n  2314:     ///\n  2315:     /// assert_eq!(vec![0, 159], value.unwrap_err().into_bytes());\n  2316:     /// ```\n  2317:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  2318:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2319:     pub fn into_bytes(self) -> Vec<u8> {\n  2320:         self.bytes\n  2321:     }\n  2322: \n  2323:     /// Fetch a `Utf8Error` to get more details about the conversion failure.\n  2324:     ///\n  2325:     /// The [`Utf8Error`] type provided by [`std::str`] represents an error that may\n  2326:     /// occur when converting a slice of [`u8`]s to a [`&str`]. In this sense, it's\n  2327:     /// an analogue to `FromUtf8Error`. See its documentation for more details\n  2328:     /// on using it.\n  2329:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::FromUtf8Error::utf8_error",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "utf8_error",
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
            "id": 963,
            "path": "FromUtf8Error"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4227",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:963",
        "resolved_owner_path": [
          "alloc",
          "string",
          "FromUtf8Error"
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
            "args": null,
            "id": 967,
            "path": "Utf8Error"
          }
        }
      }
    },
    "verification_source": "  2307:     /// [`std::str`]: core::str \"std::str\"\n  2308:     /// [`&str`]: prim@str \"&str\"\n  2309:     ///\n  2310:     /// # Examples\n  2311:     ///\n  2312:     /// ```\n  2313:     /// // some invalid bytes, in a vector\n  2314:     /// let bytes = vec![0, 159];\n  2315:     ///\n  2316:     /// let error = String::from_utf8(bytes).unwrap_err().utf8_error();\n  2317:     ///\n  2318:     /// // the first byte is invalid here\n  2319:     /// assert_eq!(1, error.valid_up_to());\n  2320:     /// ```\n  2321:     #[must_use]\n  2322:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2323:     pub fn utf8_error(&self) -> Utf8Error {\n  2324:         self.error\n  2325:     }\n  2326: }\n  2327: \n  2328: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2329: impl fmt::Display for FromUtf8Error {\n  2330:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2331:         fmt::Display::fmt(&self.error, f)\n  2332:     }\n  2333: }\n  2334: \n  2335: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2336: impl fmt::Display for FromUtf16Error {\n  2337:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2338:         fmt::Display::fmt(\"invalid utf-16: lone surrogate found\", f)\n  2339:     }",
    "nanvix_source": "  2336:     /// // some invalid bytes, in a vector\n  2337:     /// let bytes = vec![0, 159];\n  2338:     ///\n  2339:     /// let error = String::from_utf8(bytes).unwrap_err().utf8_error();\n  2340:     ///\n  2341:     /// // the first byte is invalid here\n  2342:     /// assert_eq!(1, error.valid_up_to());\n  2343:     /// ```\n  2344:     #[must_use]\n  2345:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2346:     pub fn utf8_error(&self) -> Utf8Error {\n  2347:         self.error\n  2348:     }\n  2349: }\n  2350: \n  2351: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2352: impl fmt::Display for FromUtf8Error {\n  2353:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n  2354:         fmt::Display::fmt(&self.error, f)\n  2355:     }\n  2356: }",
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
