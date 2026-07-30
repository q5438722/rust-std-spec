For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::from_micros",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_micros",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "micros",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   254:     /// Creates a new `Duration` from the specified number of microseconds.\n   255:     ///\n   256:     /// # Examples\n   257:     ///\n   258:     /// ```\n   259:     /// use std::time::Duration;\n   260:     ///\n   261:     /// let duration = Duration::from_micros(1_000_002);\n   262:     ///\n   263:     /// assert_eq!(1, duration.as_secs());\n   264:     /// assert_eq!(2_000, duration.subsec_nanos());\n   265:     /// ```\n   266:     #[stable(feature = \"duration_from_micros\", since = \"1.27.0\")]\n   267:     #[must_use]\n   268:     #[inline]\n   269:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   270:     pub const fn from_micros(micros: u64) -> Duration {\n   271:         let secs = micros / MICROS_PER_SEC;\n   272:         let subsec_micros = (micros % MICROS_PER_SEC) as u32;\n   273:         // SAFETY: (x % 1_000_000) * 1_000 < 1_000_000_000\n   274:         //         => x % 1_000_000 < 1_000_000\n   275:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_micros * NANOS_PER_MICRO) };\n   276: \n   277:         Duration { secs, nanos: subsec_nanos }\n   278:     }\n   279: \n   280:     /// Creates a new `Duration` from the specified number of nanoseconds.\n   281:     ///\n   282:     /// Note: Using this on the return value of `as_nanos()` might cause unexpected behavior:\n   283:     /// `as_nanos()` returns a u128, and can return values that do not fit in u64, e.g. 585 years.\n   284:     /// Instead, consider using the pattern `Duration::new(d.as_secs(), d.subsec_nanos())`\n   285:     /// if you cannot copy/clone the Duration directly.\n   286:     ///",
    "nanvix_source": "   260:     ///\n   261:     /// let duration = Duration::from_micros(1_000_002);\n   262:     ///\n   263:     /// assert_eq!(1, duration.as_secs());\n   264:     /// assert_eq!(2_000, duration.subsec_nanos());\n   265:     /// ```\n   266:     #[stable(feature = \"duration_from_micros\", since = \"1.27.0\")]\n   267:     #[must_use]\n   268:     #[inline]\n   269:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   270:     pub const fn from_micros(micros: u64) -> Duration {\n   271:         let secs = micros / MICROS_PER_SEC;\n   272:         let subsec_micros = (micros % MICROS_PER_SEC) as u32;\n   273:         // SAFETY: (x % 1_000_000) * 1_000 < 1_000_000_000\n   274:         //         => x % 1_000_000 < 1_000_000\n   275:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_micros * NANOS_PER_MICRO) };\n   276: \n   277:         Duration { secs, nanos: subsec_nanos }\n   278:     }\n   279: \n   280:     /// Creates a new `Duration` from the specified number of nanoseconds.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_millis",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_millis",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "millis",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   228:     /// Creates a new `Duration` from the specified number of milliseconds.\n   229:     ///\n   230:     /// # Examples\n   231:     ///\n   232:     /// ```\n   233:     /// use std::time::Duration;\n   234:     ///\n   235:     /// let duration = Duration::from_millis(2_569);\n   236:     ///\n   237:     /// assert_eq!(2, duration.as_secs());\n   238:     /// assert_eq!(569_000_000, duration.subsec_nanos());\n   239:     /// ```\n   240:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   241:     #[must_use]\n   242:     #[inline]\n   243:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   244:     pub const fn from_millis(millis: u64) -> Duration {\n   245:         let secs = millis / MILLIS_PER_SEC;\n   246:         let subsec_millis = (millis % MILLIS_PER_SEC) as u32;\n   247:         // SAFETY: (x % 1_000) * 1_000_000 < 1_000_000_000\n   248:         //         => x % 1_000 < 1_000\n   249:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_millis * NANOS_PER_MILLI) };\n   250: \n   251:         Duration { secs, nanos: subsec_nanos }\n   252:     }\n   253: \n   254:     /// Creates a new `Duration` from the specified number of microseconds.\n   255:     ///\n   256:     /// # Examples\n   257:     ///\n   258:     /// ```\n   259:     /// use std::time::Duration;\n   260:     ///",
    "nanvix_source": "   234:     ///\n   235:     /// let duration = Duration::from_millis(2_569);\n   236:     ///\n   237:     /// assert_eq!(2, duration.as_secs());\n   238:     /// assert_eq!(569_000_000, duration.subsec_nanos());\n   239:     /// ```\n   240:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   241:     #[must_use]\n   242:     #[inline]\n   243:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   244:     pub const fn from_millis(millis: u64) -> Duration {\n   245:         let secs = millis / MILLIS_PER_SEC;\n   246:         let subsec_millis = (millis % MILLIS_PER_SEC) as u32;\n   247:         // SAFETY: (x % 1_000) * 1_000_000 < 1_000_000_000\n   248:         //         => x % 1_000 < 1_000\n   249:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_millis * NANOS_PER_MILLI) };\n   250: \n   251:         Duration { secs, nanos: subsec_nanos }\n   252:     }\n   253: \n   254:     /// Creates a new `Duration` from the specified number of microseconds.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_mins",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_mins",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "mins",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   434:     /// Panics if the given number of minutes overflows the `Duration` size.\n   435:     ///\n   436:     /// # Examples\n   437:     ///\n   438:     /// ```\n   439:     /// use std::time::Duration;\n   440:     ///\n   441:     /// let duration = Duration::from_mins(10);\n   442:     ///\n   443:     /// assert_eq!(10 * 60, duration.as_secs());\n   444:     /// assert_eq!(0, duration.subsec_nanos());\n   445:     /// ```\n   446:     #[stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   447:     #[rustc_const_stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   448:     #[must_use]\n   449:     #[inline]\n   450:     pub const fn from_mins(mins: u64) -> Duration {\n   451:         if mins > u64::MAX / SECS_PER_MINUTE {\n   452:             panic!(\"overflow in Duration::from_mins\");\n   453:         }\n   454: \n   455:         Duration::from_secs(mins * SECS_PER_MINUTE)\n   456:     }\n   457: \n   458:     /// Returns true if this `Duration` spans no time.\n   459:     ///\n   460:     /// # Examples\n   461:     ///\n   462:     /// ```\n   463:     /// use std::time::Duration;\n   464:     ///\n   465:     /// assert!(Duration::ZERO.is_zero());\n   466:     /// assert!(Duration::new(0, 0).is_zero());",
    "nanvix_source": "   440:     ///\n   441:     /// let duration = Duration::from_mins(10);\n   442:     ///\n   443:     /// assert_eq!(10 * 60, duration.as_secs());\n   444:     /// assert_eq!(0, duration.subsec_nanos());\n   445:     /// ```\n   446:     #[stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   447:     #[rustc_const_stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   448:     #[must_use]\n   449:     #[inline]\n   450:     pub const fn from_mins(mins: u64) -> Duration {\n   451:         if mins > u64::MAX / SECS_PER_MINUTE {\n   452:             panic!(\"overflow in Duration::from_mins\");\n   453:         }\n   454: \n   455:         Duration::from_secs(mins * SECS_PER_MINUTE)\n   456:     }\n   457: \n   458:     /// Returns true if this `Duration` spans no time.\n   459:     ///\n   460:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_nanos",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_nanos",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "nanos",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   285:     /// if you cannot copy/clone the Duration directly.\n   286:     ///\n   287:     /// # Examples\n   288:     ///\n   289:     /// ```\n   290:     /// use std::time::Duration;\n   291:     ///\n   292:     /// let duration = Duration::from_nanos(1_000_000_123);\n   293:     ///\n   294:     /// assert_eq!(1, duration.as_secs());\n   295:     /// assert_eq!(123, duration.subsec_nanos());\n   296:     /// ```\n   297:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   298:     #[must_use]\n   299:     #[inline]\n   300:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   301:     pub const fn from_nanos(nanos: u64) -> Duration {\n   302:         const NANOS_PER_SEC: u64 = self::NANOS_PER_SEC as u64;\n   303:         let secs = nanos / NANOS_PER_SEC;\n   304:         let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;\n   305:         // SAFETY: x % 1_000_000_000 < 1_000_000_000\n   306:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };\n   307: \n   308:         Duration { secs, nanos: subsec_nanos }\n   309:     }\n   310: \n   311:     /// Creates a new `Duration` from the specified number of nanoseconds.\n   312:     ///\n   313:     /// # Panics\n   314:     ///\n   315:     /// Panics if the given number of nanoseconds is greater than [`Duration::MAX`].\n   316:     ///\n   317:     /// # Examples",
    "nanvix_source": "   291:     ///\n   292:     /// let duration = Duration::from_nanos(1_000_000_123);\n   293:     ///\n   294:     /// assert_eq!(1, duration.as_secs());\n   295:     /// assert_eq!(123, duration.subsec_nanos());\n   296:     /// ```\n   297:     #[stable(feature = \"duration_extras\", since = \"1.27.0\")]\n   298:     #[must_use]\n   299:     #[inline]\n   300:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   301:     pub const fn from_nanos(nanos: u64) -> Duration {\n   302:         const NANOS_PER_SEC: u64 = self::NANOS_PER_SEC as u64;\n   303:         let secs = nanos / NANOS_PER_SEC;\n   304:         let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;\n   305:         // SAFETY: x % 1_000_000_000 < 1_000_000_000\n   306:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };\n   307: \n   308:         Duration { secs, nanos: subsec_nanos }\n   309:     }\n   310: \n   311:     /// Creates a new `Duration` from the specified number of nanoseconds.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_nanos_u128",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_nanos_u128",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "nanos",
            {
              "primitive": "u128"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   318:     ///\n   319:     /// ```\n   320:     /// use std::time::Duration;\n   321:     ///\n   322:     /// let nanos = 10_u128.pow(24) + 321;\n   323:     /// let duration = Duration::from_nanos_u128(nanos);\n   324:     ///\n   325:     /// assert_eq!(10_u64.pow(15), duration.as_secs());\n   326:     /// assert_eq!(321, duration.subsec_nanos());\n   327:     /// ```\n   328:     #[stable(feature = \"duration_from_nanos_u128\", since = \"1.93.0\")]\n   329:     #[rustc_const_stable(feature = \"duration_from_nanos_u128\", since = \"1.93.0\")]\n   330:     #[must_use]\n   331:     #[inline]\n   332:     #[track_caller]\n   333:     #[rustc_allow_const_fn_unstable(const_trait_impl, const_convert)] // for `u64::try_from`\n   334:     pub const fn from_nanos_u128(nanos: u128) -> Duration {\n   335:         const NANOS_PER_SEC: u128 = self::NANOS_PER_SEC as u128;\n   336:         let Ok(secs) = u64::try_from(nanos / NANOS_PER_SEC) else {\n   337:             panic!(\"overflow in `Duration::from_nanos_u128`\");\n   338:         };\n   339:         let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;\n   340:         // SAFETY: x % 1_000_000_000 < 1_000_000_000 also, subsec_nanos >= 0 since u128 >=0 and u32 >=0\n   341:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };\n   342: \n   343:         Duration { secs: secs as u64, nanos: subsec_nanos }\n   344:     }\n   345: \n   346:     /// Creates a new `Duration` from the specified number of weeks.\n   347:     ///\n   348:     /// # Panics\n   349:     ///\n   350:     /// Panics if the given number of weeks overflows the `Duration` size.",
    "nanvix_source": "   324:     ///\n   325:     /// assert_eq!(10_u64.pow(15), duration.as_secs());\n   326:     /// assert_eq!(321, duration.subsec_nanos());\n   327:     /// ```\n   328:     #[stable(feature = \"duration_from_nanos_u128\", since = \"1.93.0\")]\n   329:     #[rustc_const_stable(feature = \"duration_from_nanos_u128\", since = \"1.93.0\")]\n   330:     #[must_use]\n   331:     #[inline]\n   332:     #[track_caller]\n   333:     #[rustc_allow_const_fn_unstable(const_trait_impl, const_convert)] // for `u64::try_from`\n   334:     pub const fn from_nanos_u128(nanos: u128) -> Duration {\n   335:         const NANOS_PER_SEC: u128 = self::NANOS_PER_SEC as u128;\n   336:         let Ok(secs) = u64::try_from(nanos / NANOS_PER_SEC) else {\n   337:             panic!(\"overflow in `Duration::from_nanos_u128`\");\n   338:         };\n   339:         let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;\n   340:         // SAFETY: x % 1_000_000_000 < 1_000_000_000 also, subsec_nanos >= 0 since u128 >=0 and u32 >=0\n   341:         let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };\n   342: \n   343:         Duration { secs: secs as u64, nanos: subsec_nanos }\n   344:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_secs",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
      "name": "from_secs",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "secs",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   208:     /// Creates a new `Duration` from the specified number of whole seconds.\n   209:     ///\n   210:     /// # Examples\n   211:     ///\n   212:     /// ```\n   213:     /// use std::time::Duration;\n   214:     ///\n   215:     /// let duration = Duration::from_secs(5);\n   216:     ///\n   217:     /// assert_eq!(5, duration.as_secs());\n   218:     /// assert_eq!(0, duration.subsec_nanos());\n   219:     /// ```\n   220:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   221:     #[must_use]\n   222:     #[inline]\n   223:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   224:     pub const fn from_secs(secs: u64) -> Duration {\n   225:         Duration { secs, nanos: Nanoseconds::ZERO }\n   226:     }\n   227: \n   228:     /// Creates a new `Duration` from the specified number of milliseconds.\n   229:     ///\n   230:     /// # Examples\n   231:     ///\n   232:     /// ```\n   233:     /// use std::time::Duration;\n   234:     ///\n   235:     /// let duration = Duration::from_millis(2_569);\n   236:     ///\n   237:     /// assert_eq!(2, duration.as_secs());\n   238:     /// assert_eq!(569_000_000, duration.subsec_nanos());\n   239:     /// ```\n   240:     #[stable(feature = \"duration\", since = \"1.3.0\")]",
    "nanvix_source": "   214:     ///\n   215:     /// let duration = Duration::from_secs(5);\n   216:     ///\n   217:     /// assert_eq!(5, duration.as_secs());\n   218:     /// assert_eq!(0, duration.subsec_nanos());\n   219:     /// ```\n   220:     #[stable(feature = \"duration\", since = \"1.3.0\")]\n   221:     #[must_use]\n   222:     #[inline]\n   223:     #[rustc_const_stable(feature = \"duration_consts\", since = \"1.32.0\")]\n   224:     pub const fn from_secs(secs: u64) -> Duration {\n   225:         Duration { secs, nanos: Nanoseconds::ZERO }\n   226:     }\n   227: \n   228:     /// Creates a new `Duration` from the specified number of milliseconds.\n   229:     ///\n   230:     /// # Examples\n   231:     ///\n   232:     /// ```\n   233:     /// use std::time::Duration;\n   234:     ///",
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
