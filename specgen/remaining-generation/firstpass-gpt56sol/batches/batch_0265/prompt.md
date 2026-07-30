For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::time::Instant::elapsed",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "elapsed",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "id": 513,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   374:     ///\n   375:     /// [Monotonicity]: Instant#monotonicity\n   376:     ///\n   377:     /// # Examples\n   378:     ///\n   379:     /// ```no_run\n   380:     /// use std::thread::sleep;\n   381:     /// use std::time::{Duration, Instant};\n   382:     ///\n   383:     /// let instant = Instant::now();\n   384:     /// let three_secs = Duration::from_secs(3);\n   385:     /// sleep(three_secs);\n   386:     /// assert!(instant.elapsed() >= three_secs);\n   387:     /// ```\n   388:     #[must_use]\n   389:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   390:     pub fn elapsed(&self) -> Duration {\n   391:         Instant::now() - *self\n   392:     }\n   393: \n   394:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   395:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   396:     /// otherwise.\n   397:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   398:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   399:         self.0.checked_add_duration(&duration).map(Instant)\n   400:     }\n   401: \n   402:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   403:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   404:     /// otherwise.\n   405:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   406:     pub fn checked_sub(&self, duration: Duration) -> Option<Instant> {",
    "nanvix_source": "   378:     /// use std::thread::sleep;\n   379:     /// use std::time::{Duration, Instant};\n   380:     ///\n   381:     /// let instant = Instant::now();\n   382:     /// let three_secs = Duration::from_secs(3);\n   383:     /// sleep(three_secs);\n   384:     /// assert!(instant.elapsed() >= three_secs);\n   385:     /// ```\n   386:     #[must_use]\n   387:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   388:     pub fn elapsed(&self) -> Duration {\n   389:         Instant::now() - *self\n   390:     }\n   391: \n   392:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   393:     /// `Instant` (which means it's inside the bounds of the underlying data structure), `None`\n   394:     /// otherwise.\n   395:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   396:     pub fn checked_add(&self, duration: Duration) -> Option<Instant> {\n   397:         self.0.checked_add_duration(&duration).map(Instant)\n   398:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::now",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "now",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 516,
            "path": "Instant"
          }
        }
      }
    },
    "verification_source": "   271: #[stable(feature = \"time2\", since = \"1.8.0\")]\n   272: pub struct SystemTimeError(Duration);\n   273: \n   274: impl Instant {\n   275:     /// Returns an instant corresponding to \"now\".\n   276:     ///\n   277:     /// # Examples\n   278:     ///\n   279:     /// ```\n   280:     /// use std::time::Instant;\n   281:     ///\n   282:     /// let now = Instant::now();\n   283:     /// ```\n   284:     #[must_use]\n   285:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   286:     #[cfg_attr(not(test), rustc_diagnostic_item = \"instant_now\")]\n   287:     pub fn now() -> Instant {\n   288:         Instant(time::Instant::now())\n   289:     }\n   290: \n   291:     /// Returns the amount of time elapsed from another instant to this one,\n   292:     /// or zero duration if that instant is later than this one.\n   293:     ///\n   294:     /// # Panics\n   295:     ///\n   296:     /// Previous Rust versions panicked when `earlier` was later than `self`. Currently this\n   297:     /// method saturates. Future versions may reintroduce the panic in some circumstances.\n   298:     /// See [Monotonicity].\n   299:     ///\n   300:     /// [Monotonicity]: Instant#monotonicity\n   301:     ///\n   302:     /// # Examples\n   303:     ///",
    "nanvix_source": "   275:     /// # Examples\n   276:     ///\n   277:     /// ```\n   278:     /// use std::time::Instant;\n   279:     ///\n   280:     /// let now = Instant::now();\n   281:     /// ```\n   282:     #[must_use]\n   283:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   284:     #[cfg_attr(not(test), rustc_diagnostic_item = \"instant_now\")]\n   285:     pub fn now() -> Instant {\n   286:         Instant(time::Instant::now())\n   287:     }\n   288: \n   289:     /// Returns the amount of time elapsed from another instant to this one,\n   290:     /// or zero duration if that instant is later than this one.\n   291:     ///\n   292:     /// # Panics\n   293:     ///\n   294:     /// Previous Rust versions panicked when `earlier` was later than `self`. Currently this\n   295:     /// method saturates. Future versions may reintroduce the panic in some circumstances.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::Instant::saturating_duration_since",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "saturating_duration_since",
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
            "id": 516,
            "path": "Instant"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9296",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:516",
        "resolved_owner_path": [
          "std",
          "time",
          "Instant"
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
            "earlier",
            {
              "resolved_path": {
                "args": null,
                "id": 516,
                "path": "Instant"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 513,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   347:     /// or zero duration if that instant is later than this one.\n   348:     ///\n   349:     /// # Examples\n   350:     ///\n   351:     /// ```no_run\n   352:     /// use std::time::{Duration, Instant};\n   353:     /// use std::thread::sleep;\n   354:     ///\n   355:     /// let now = Instant::now();\n   356:     /// sleep(Duration::new(1, 0));\n   357:     /// let new_now = Instant::now();\n   358:     /// println!(\"{:?}\", new_now.saturating_duration_since(now));\n   359:     /// println!(\"{:?}\", now.saturating_duration_since(new_now)); // 0ns\n   360:     /// ```\n   361:     #[must_use]\n   362:     #[stable(feature = \"checked_duration_since\", since = \"1.39.0\")]\n   363:     pub fn saturating_duration_since(&self, earlier: Instant) -> Duration {\n   364:         self.checked_duration_since(earlier).unwrap_or_default()\n   365:     }\n   366: \n   367:     /// Returns the amount of time elapsed since this instant.\n   368:     ///\n   369:     /// # Panics\n   370:     ///\n   371:     /// Previous Rust versions panicked when the current time was earlier than self. Currently this\n   372:     /// method returns a Duration of zero in that case. Future versions may reintroduce the panic.\n   373:     /// See [Monotonicity].\n   374:     ///\n   375:     /// [Monotonicity]: Instant#monotonicity\n   376:     ///\n   377:     /// # Examples\n   378:     ///\n   379:     /// ```no_run",
    "nanvix_source": "   351:     /// use std::thread::sleep;\n   352:     ///\n   353:     /// let now = Instant::now();\n   354:     /// sleep(Duration::new(1, 0));\n   355:     /// let new_now = Instant::now();\n   356:     /// println!(\"{:?}\", new_now.saturating_duration_since(now));\n   357:     /// println!(\"{:?}\", now.saturating_duration_since(new_now)); // 0ns\n   358:     /// ```\n   359:     #[must_use]\n   360:     #[stable(feature = \"checked_duration_since\", since = \"1.39.0\")]\n   361:     pub fn saturating_duration_since(&self, earlier: Instant) -> Duration {\n   362:         self.checked_duration_since(earlier).unwrap_or_default()\n   363:     }\n   364: \n   365:     /// Returns the amount of time elapsed since this instant.\n   366:     ///\n   367:     /// # Panics\n   368:     ///\n   369:     /// Previous Rust versions panicked when the current time was earlier than self. Currently this\n   370:     /// method returns a Duration of zero in that case. Future versions may reintroduce the panic.\n   371:     /// See [Monotonicity].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::SystemTime::checked_add",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "checked_add",
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
            "id": 2591,
            "path": "SystemTime"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9357",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2591",
        "resolved_owner_path": [
          "std",
          "time",
          "SystemTime"
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
            "duration",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
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
                        "args": null,
                        "id": 2591,
                        "path": "SystemTime"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   655:     /// let one_sec = Duration::from_secs(1);\n   656:     /// sleep(one_sec);\n   657:     /// assert!(sys_time.elapsed().unwrap() >= one_sec);\n   658:     /// ```\n   659:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   660:     pub fn elapsed(&self) -> Result<Duration, SystemTimeError> {\n   661:         SystemTime::now().duration_since(*self)\n   662:     }\n   663: \n   664:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   665:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   666:     /// otherwise.\n   667:     ///\n   668:     /// In the case that the `duration` is smaller than the time precision of the operating\n   669:     /// system, `Some(self)` will be returned.\n   670:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   671:     pub fn checked_add(&self, duration: Duration) -> Option<SystemTime> {\n   672:         self.0.checked_add_duration(&duration).map(SystemTime)\n   673:     }\n   674: \n   675:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   676:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   677:     /// otherwise.\n   678:     ///\n   679:     /// In the case that the `duration` is smaller than the time precision of the operating\n   680:     /// system, `Some(self)` will be returned.\n   681:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   682:     pub fn checked_sub(&self, duration: Duration) -> Option<SystemTime> {\n   683:         self.0.checked_sub_duration(&duration).map(SystemTime)\n   684:     }\n   685: \n   686:     /// Saturating [`SystemTime`] addition, computing `self + duration`,\n   687:     /// returning [`SystemTime::MAX`] if overflow occurred.",
    "nanvix_source": "   661:         SystemTime::now().duration_since(*self)\n   662:     }\n   663: \n   664:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   665:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   666:     /// otherwise.\n   667:     ///\n   668:     /// In the case that the `duration` is smaller than the time precision of the operating\n   669:     /// system, `Some(self)` will be returned.\n   670:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   671:     pub fn checked_add(&self, duration: Duration) -> Option<SystemTime> {\n   672:         self.0.checked_add_duration(&duration).map(SystemTime)\n   673:     }\n   674: \n   675:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   676:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   677:     /// otherwise.\n   678:     ///\n   679:     /// In the case that the `duration` is smaller than the time precision of the operating\n   680:     /// system, `Some(self)` will be returned.\n   681:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::SystemTime::checked_sub",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "checked_sub",
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
            "id": 2591,
            "path": "SystemTime"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9357",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2591",
        "resolved_owner_path": [
          "std",
          "time",
          "SystemTime"
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
            "duration",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
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
                        "args": null,
                        "id": 2591,
                        "path": "SystemTime"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   666:     /// otherwise.\n   667:     ///\n   668:     /// In the case that the `duration` is smaller than the time precision of the operating\n   669:     /// system, `Some(self)` will be returned.\n   670:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   671:     pub fn checked_add(&self, duration: Duration) -> Option<SystemTime> {\n   672:         self.0.checked_add_duration(&duration).map(SystemTime)\n   673:     }\n   674: \n   675:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   676:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   677:     /// otherwise.\n   678:     ///\n   679:     /// In the case that the `duration` is smaller than the time precision of the operating\n   680:     /// system, `Some(self)` will be returned.\n   681:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   682:     pub fn checked_sub(&self, duration: Duration) -> Option<SystemTime> {\n   683:         self.0.checked_sub_duration(&duration).map(SystemTime)\n   684:     }\n   685: \n   686:     /// Saturating [`SystemTime`] addition, computing `self + duration`,\n   687:     /// returning [`SystemTime::MAX`] if overflow occurred.\n   688:     ///\n   689:     /// In the case that the `duration` is smaller than the time precision of\n   690:     /// the operating system, `self` will be returned.\n   691:     #[unstable(feature = \"time_saturating_systemtime\", issue = \"151199\")]\n   692:     pub fn saturating_add(&self, duration: Duration) -> SystemTime {\n   693:         self.checked_add(duration).unwrap_or(SystemTime::MAX)\n   694:     }\n   695: \n   696:     /// Saturating [`SystemTime`] subtraction, computing `self - duration`,\n   697:     /// returning [`SystemTime::MIN`] if overflow occurred.\n   698:     ///",
    "nanvix_source": "   672:         self.0.checked_add_duration(&duration).map(SystemTime)\n   673:     }\n   674: \n   675:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   676:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   677:     /// otherwise.\n   678:     ///\n   679:     /// In the case that the `duration` is smaller than the time precision of the operating\n   680:     /// system, `Some(self)` will be returned.\n   681:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   682:     pub fn checked_sub(&self, duration: Duration) -> Option<SystemTime> {\n   683:         self.0.checked_sub_duration(&duration).map(SystemTime)\n   684:     }\n   685: \n   686:     /// Saturating [`SystemTime`] addition, computing `self + duration`,\n   687:     /// returning [`SystemTime::MAX`] if overflow occurred.\n   688:     ///\n   689:     /// In the case that the `duration` is smaller than the time precision of\n   690:     /// the operating system, `self` will be returned.\n   691:     #[unstable(feature = \"time_saturating_systemtime\", issue = \"151199\")]\n   692:     pub fn saturating_add(&self, duration: Duration) -> SystemTime {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::SystemTime::duration_since",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "duration_since",
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
            "id": 2591,
            "path": "SystemTime"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9357",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2591",
        "resolved_owner_path": [
          "std",
          "time",
          "SystemTime"
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
            "earlier",
            {
              "resolved_path": {
                "args": null,
                "id": 2591,
                "path": "SystemTime"
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
                        "args": null,
                        "id": 513,
                        "path": "Duration"
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 9349,
                        "path": "SystemTimeError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   614:     ///\n   615:     /// Returns an [`Err`] if `earlier` is later than `self`, and the error\n   616:     /// contains how far from `self` the time is.\n   617:     ///\n   618:     /// # Examples\n   619:     ///\n   620:     /// ```no_run\n   621:     /// use std::time::SystemTime;\n   622:     ///\n   623:     /// let sys_time = SystemTime::now();\n   624:     /// let new_sys_time = SystemTime::now();\n   625:     /// let difference = new_sys_time.duration_since(sys_time)\n   626:     ///     .expect(\"Clock may have gone backwards\");\n   627:     /// println!(\"{difference:?}\");\n   628:     /// ```\n   629:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   630:     pub fn duration_since(&self, earlier: SystemTime) -> Result<Duration, SystemTimeError> {\n   631:         self.0.sub_time(&earlier.0).map_err(SystemTimeError)\n   632:     }\n   633: \n   634:     /// Returns the difference from this system time to the\n   635:     /// current clock time.\n   636:     ///\n   637:     /// This function may fail as the underlying system clock is susceptible to\n   638:     /// drift and updates (e.g., the system clock could go backwards), so this\n   639:     /// function might not always succeed. If successful, <code>[Ok]\\([Duration])</code> is\n   640:     /// returned where the duration represents the amount of time elapsed from\n   641:     /// this time measurement to the current time.\n   642:     ///\n   643:     /// To measure elapsed time reliably, use [`Instant`] instead.\n   644:     ///\n   645:     /// Returns an [`Err`] if `self` is later than the current system time, and\n   646:     /// the error contains how far from the current system time `self` is.",
    "nanvix_source": "   620:     /// ```no_run\n   621:     /// use std::time::SystemTime;\n   622:     ///\n   623:     /// let sys_time = SystemTime::now();\n   624:     /// let new_sys_time = SystemTime::now();\n   625:     /// let difference = new_sys_time.duration_since(sys_time)\n   626:     ///     .expect(\"Clock may have gone backwards\");\n   627:     /// println!(\"{difference:?}\");\n   628:     /// ```\n   629:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   630:     pub fn duration_since(&self, earlier: SystemTime) -> Result<Duration, SystemTimeError> {\n   631:         self.0.sub_time(&earlier.0).map_err(SystemTimeError)\n   632:     }\n   633: \n   634:     /// Returns the difference from this system time to the\n   635:     /// current clock time.\n   636:     ///\n   637:     /// This function may fail as the underlying system clock is susceptible to\n   638:     /// drift and updates (e.g., the system clock could go backwards), so this\n   639:     /// function might not always succeed. If successful, <code>[Ok]\\([Duration])</code> is\n   640:     /// returned where the duration represents the amount of time elapsed from",
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
