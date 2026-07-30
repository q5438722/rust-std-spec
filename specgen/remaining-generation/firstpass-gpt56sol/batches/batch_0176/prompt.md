For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashSet::with_hasher",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "with_hasher",
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1347,
            "path": "HashSet"
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
              "name": "S"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:1356",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1347",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "set",
          "HashSet"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "hasher",
            {
              "generic": "S"
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
                      "generic": "S"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 1347,
            "path": "HashSet"
          }
        }
      }
    },
    "verification_source": "   230:     /// the `HashSet` to be useful, see its documentation for details.\n   231:     ///\n   232:     /// # Examples\n   233:     ///\n   234:     /// ```\n   235:     /// use std::collections::HashSet;\n   236:     /// use std::hash::RandomState;\n   237:     ///\n   238:     /// let s = RandomState::new();\n   239:     /// let mut set = HashSet::with_hasher(s);\n   240:     /// set.insert(2);\n   241:     /// ```\n   242:     #[inline]\n   243:     #[must_use]\n   244:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   245:     #[rustc_const_stable(feature = \"const_collections_with_hasher\", since = \"1.85.0\")]\n   246:     pub const fn with_hasher(hasher: S) -> HashSet<T, S> {\n   247:         HashSet { base: base::HashSet::with_hasher(hasher) }\n   248:     }\n   249: \n   250:     /// Creates an empty `HashSet` with at least the specified capacity, using\n   251:     /// `hasher` to hash the keys.\n   252:     ///\n   253:     /// The hash set will be able to hold at least `capacity` elements without\n   254:     /// reallocating. This method is allowed to allocate for more elements than\n   255:     /// `capacity`. If `capacity` is zero, the hash set will not allocate.\n   256:     ///\n   257:     /// Warning: `hasher` is normally randomly generated, and\n   258:     /// is designed to allow `HashSet`s to be resistant to attacks that\n   259:     /// cause many collisions and very poor performance. Setting it\n   260:     /// manually using this function can expose a DoS attack vector.\n   261:     ///\n   262:     /// The `hash_builder` passed should implement the [`BuildHasher`] trait for",
    "nanvix_source": "   236:     /// use std::hash::RandomState;\n   237:     ///\n   238:     /// let s = RandomState::new();\n   239:     /// let mut set = HashSet::with_hasher(s);\n   240:     /// set.insert(2);\n   241:     /// ```\n   242:     #[inline]\n   243:     #[must_use]\n   244:     #[stable(feature = \"hashmap_build_hasher\", since = \"1.7.0\")]\n   245:     #[rustc_const_stable(feature = \"const_collections_with_hasher\", since = \"1.85.0\")]\n   246:     pub const fn with_hasher(hasher: S) -> HashSet<T, S> {\n   247:         HashSet { base: base::HashSet::with_hasher(hasher) }\n   248:     }\n   249: \n   250:     /// Creates an empty `HashSet` with at least the specified capacity, using\n   251:     /// `hasher` to hash the keys.\n   252:     ///\n   253:     /// The hash set will be able to hold at least `capacity` elements without\n   254:     /// reallocating. This method is allowed to allocate for more elements than\n   255:     /// `capacity`. If `capacity` is zero, the hash set will not allocate.\n   256:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_unsafe": false
      },
      "name": "capacity",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
    "verification_source": "   334: \n   335:     /// Returns the capacity this `OsString` can hold without reallocating.\n   336:     ///\n   337:     /// See the main `OsString` documentation information about encoding and capacity units.\n   338:     ///\n   339:     /// # Examples\n   340:     ///\n   341:     /// ```\n   342:     /// use std::ffi::OsString;\n   343:     ///\n   344:     /// let os_string = OsString::with_capacity(10);\n   345:     /// assert!(os_string.capacity() >= 10);\n   346:     /// ```\n   347:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   348:     #[must_use]\n   349:     #[inline]\n   350:     pub fn capacity(&self) -> usize {\n   351:         self.inner.capacity()\n   352:     }\n   353: \n   354:     /// Reserves capacity for at least `additional` more capacity to be inserted\n   355:     /// in the given `OsString`. Does nothing if the capacity is\n   356:     /// already sufficient.\n   357:     ///\n   358:     /// The collection may reserve more space to speculatively avoid frequent reallocations.\n   359:     ///\n   360:     /// See the main `OsString` documentation information about encoding and capacity units.\n   361:     ///\n   362:     /// # Examples\n   363:     ///\n   364:     /// ```\n   365:     /// use std::ffi::OsString;\n   366:     ///",
    "nanvix_source": "   332:     ///\n   333:     /// ```\n   334:     /// use std::ffi::OsString;\n   335:     ///\n   336:     /// let os_string = OsString::with_capacity(10);\n   337:     /// assert!(os_string.capacity() >= 10);\n   338:     /// ```\n   339:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   340:     #[must_use]\n   341:     #[inline]\n   342:     pub fn capacity(&self) -> usize {\n   343:         self.inner.capacity()\n   344:     }\n   345: \n   346:     /// Reserves capacity for at least `additional` more capacity to be inserted\n   347:     /// in the given `OsString`. Does nothing if the capacity is\n   348:     /// already sufficient.\n   349:     ///\n   350:     /// The collection may reserve more space to speculatively avoid frequent reallocations.\n   351:     ///\n   352:     /// See the main `OsString` documentation information about encoding and capacity units.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "reserve",
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
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   357:     ///\n   358:     /// The collection may reserve more space to speculatively avoid frequent reallocations.\n   359:     ///\n   360:     /// See the main `OsString` documentation information about encoding and capacity units.\n   361:     ///\n   362:     /// # Examples\n   363:     ///\n   364:     /// ```\n   365:     /// use std::ffi::OsString;\n   366:     ///\n   367:     /// let mut s = OsString::new();\n   368:     /// s.reserve(10);\n   369:     /// assert!(s.capacity() >= 10);\n   370:     /// ```\n   371:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   372:     #[inline]\n   373:     pub fn reserve(&mut self, additional: usize) {\n   374:         self.inner.reserve(additional)\n   375:     }\n   376: \n   377:     /// Tries to reserve capacity for at least `additional` more length units\n   378:     /// in the given `OsString`. The string may reserve more space to speculatively avoid\n   379:     /// frequent reallocations. After calling `try_reserve`, capacity will be\n   380:     /// greater than or equal to `self.len() + additional` if it returns `Ok(())`.\n   381:     /// Does nothing if capacity is already sufficient. This method preserves\n   382:     /// the contents even if an error occurs.\n   383:     ///\n   384:     /// See the main `OsString` documentation information about encoding and capacity units.\n   385:     ///\n   386:     /// # Errors\n   387:     ///\n   388:     /// If the capacity overflows, or the allocator reports a failure, then an error\n   389:     /// is returned.",
    "nanvix_source": "   355:     ///\n   356:     /// ```\n   357:     /// use std::ffi::OsString;\n   358:     ///\n   359:     /// let mut s = OsString::new();\n   360:     /// s.reserve(10);\n   361:     /// assert!(s.capacity() >= 10);\n   362:     /// ```\n   363:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   364:     #[inline]\n   365:     pub fn reserve(&mut self, additional: usize) {\n   366:         self.inner.reserve(additional)\n   367:     }\n   368: \n   369:     /// Tries to reserve capacity for at least `additional` more length units\n   370:     /// in the given `OsString`. The string may reserve more space to speculatively avoid\n   371:     /// frequent reallocations. After calling `try_reserve`, capacity will be\n   372:     /// greater than or equal to `self.len() + additional` if it returns `Ok(())`.\n   373:     /// Does nothing if capacity is already sufficient. This method preserves\n   374:     /// the contents even if an error occurs.\n   375:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "reserve_exact",
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
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   423:     ///\n   424:     /// [`reserve`]: OsString::reserve\n   425:     ///\n   426:     /// See the main `OsString` documentation information about encoding and capacity units.\n   427:     ///\n   428:     /// # Examples\n   429:     ///\n   430:     /// ```\n   431:     /// use std::ffi::OsString;\n   432:     ///\n   433:     /// let mut s = OsString::new();\n   434:     /// s.reserve_exact(10);\n   435:     /// assert!(s.capacity() >= 10);\n   436:     /// ```\n   437:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   438:     #[inline]\n   439:     pub fn reserve_exact(&mut self, additional: usize) {\n   440:         self.inner.reserve_exact(additional)\n   441:     }\n   442: \n   443:     /// Tries to reserve the minimum capacity for at least `additional`\n   444:     /// more length units in the given `OsString`. After calling\n   445:     /// `try_reserve_exact`, capacity will be greater than or equal to\n   446:     /// `self.len() + additional` if it returns `Ok(())`.\n   447:     /// Does nothing if the capacity is already sufficient.\n   448:     ///\n   449:     /// Note that the allocator may give the `OsString` more space than it\n   450:     /// requests. Therefore, capacity can not be relied upon to be precisely\n   451:     /// minimal. Prefer [`try_reserve`] if future insertions are expected.\n   452:     ///\n   453:     /// [`try_reserve`]: OsString::try_reserve\n   454:     ///\n   455:     /// See the main `OsString` documentation information about encoding and capacity units.",
    "nanvix_source": "   421:     ///\n   422:     /// ```\n   423:     /// use std::ffi::OsString;\n   424:     ///\n   425:     /// let mut s = OsString::new();\n   426:     /// s.reserve_exact(10);\n   427:     /// assert!(s.capacity() >= 10);\n   428:     /// ```\n   429:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n   430:     #[inline]\n   431:     pub fn reserve_exact(&mut self, additional: usize) {\n   432:         self.inner.reserve_exact(additional)\n   433:     }\n   434: \n   435:     /// Tries to reserve the minimum capacity for at least `additional`\n   436:     /// more length units in the given `OsString`. After calling\n   437:     /// `try_reserve_exact`, capacity will be greater than or equal to\n   438:     /// `self.len() + additional` if it returns `Ok(())`.\n   439:     /// Does nothing if the capacity is already sufficient.\n   440:     ///\n   441:     /// Note that the allocator may give the `OsString` more space than it",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to",
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
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   520:     ///\n   521:     /// ```\n   522:     /// use std::ffi::OsString;\n   523:     ///\n   524:     /// let mut s = OsString::from(\"foo\");\n   525:     ///\n   526:     /// s.reserve(100);\n   527:     /// assert!(s.capacity() >= 100);\n   528:     ///\n   529:     /// s.shrink_to(10);\n   530:     /// assert!(s.capacity() >= 10);\n   531:     /// s.shrink_to(0);\n   532:     /// assert!(s.capacity() >= 3);\n   533:     /// ```\n   534:     #[inline]\n   535:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   536:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   537:         self.inner.shrink_to(min_capacity)\n   538:     }\n   539: \n   540:     /// Converts this `OsString` into a boxed [`OsStr`].\n   541:     ///\n   542:     /// # Examples\n   543:     ///\n   544:     /// ```\n   545:     /// use std::ffi::{OsString, OsStr};\n   546:     ///\n   547:     /// let s = OsString::from(\"hello\");\n   548:     ///\n   549:     /// let b: Box<OsStr> = s.into_boxed_os_str();\n   550:     /// ```\n   551:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   552:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]",
    "nanvix_source": "   518:     /// s.reserve(100);\n   519:     /// assert!(s.capacity() >= 100);\n   520:     ///\n   521:     /// s.shrink_to(10);\n   522:     /// assert!(s.capacity() >= 10);\n   523:     /// s.shrink_to(0);\n   524:     /// assert!(s.capacity() >= 3);\n   525:     /// ```\n   526:     #[inline]\n   527:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n   528:     pub fn shrink_to(&mut self, min_capacity: usize) {\n   529:         self.inner.shrink_to(min_capacity)\n   530:     }\n   531: \n   532:     /// Converts this `OsString` into a boxed [`OsStr`].\n   533:     ///\n   534:     /// # Examples\n   535:     ///\n   536:     /// ```\n   537:     /// use std::ffi::{OsString, OsStr};\n   538:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to_fit",
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
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   490:     ///\n   491:     /// # Examples\n   492:     ///\n   493:     /// ```\n   494:     /// use std::ffi::OsString;\n   495:     ///\n   496:     /// let mut s = OsString::from(\"foo\");\n   497:     ///\n   498:     /// s.reserve(100);\n   499:     /// assert!(s.capacity() >= 100);\n   500:     ///\n   501:     /// s.shrink_to_fit();\n   502:     /// assert_eq!(3, s.capacity());\n   503:     /// ```\n   504:     #[stable(feature = \"osstring_shrink_to_fit\", since = \"1.19.0\")]\n   505:     #[inline]\n   506:     pub fn shrink_to_fit(&mut self) {\n   507:         self.inner.shrink_to_fit()\n   508:     }\n   509: \n   510:     /// Shrinks the capacity of the `OsString` with a lower bound.\n   511:     ///\n   512:     /// The capacity will remain at least as large as both the length\n   513:     /// and the supplied value.\n   514:     ///\n   515:     /// If the current capacity is less than the lower limit, this is a no-op.\n   516:     ///\n   517:     /// See the main `OsString` documentation information about encoding and capacity units.\n   518:     ///\n   519:     /// # Examples\n   520:     ///\n   521:     /// ```\n   522:     /// use std::ffi::OsString;",
    "nanvix_source": "   488:     /// let mut s = OsString::from(\"foo\");\n   489:     ///\n   490:     /// s.reserve(100);\n   491:     /// assert!(s.capacity() >= 100);\n   492:     ///\n   493:     /// s.shrink_to_fit();\n   494:     /// assert_eq!(3, s.capacity());\n   495:     /// ```\n   496:     #[stable(feature = \"osstring_shrink_to_fit\", since = \"1.19.0\")]\n   497:     #[inline]\n   498:     pub fn shrink_to_fit(&mut self) {\n   499:         self.inner.shrink_to_fit()\n   500:     }\n   501: \n   502:     /// Shrinks the capacity of the `OsString` with a lower bound.\n   503:     ///\n   504:     /// The capacity will remain at least as large as both the length\n   505:     /// and the supplied value.\n   506:     ///\n   507:     /// If the current capacity is less than the lower limit, this is a no-op.\n   508:     ///",
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
