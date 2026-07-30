For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::time::SystemTime::elapsed",
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
    "verification_source": "   644:     ///\n   645:     /// Returns an [`Err`] if `self` is later than the current system time, and\n   646:     /// the error contains how far from the current system time `self` is.\n   647:     ///\n   648:     /// # Examples\n   649:     ///\n   650:     /// ```no_run\n   651:     /// use std::thread::sleep;\n   652:     /// use std::time::{Duration, SystemTime};\n   653:     ///\n   654:     /// let sys_time = SystemTime::now();\n   655:     /// let one_sec = Duration::from_secs(1);\n   656:     /// sleep(one_sec);\n   657:     /// assert!(sys_time.elapsed().unwrap() >= one_sec);\n   658:     /// ```\n   659:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   660:     pub fn elapsed(&self) -> Result<Duration, SystemTimeError> {\n   661:         SystemTime::now().duration_since(*self)\n   662:     }\n   663: \n   664:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   665:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   666:     /// otherwise.\n   667:     ///\n   668:     /// In the case that the `duration` is smaller than the time precision of the operating\n   669:     /// system, `Some(self)` will be returned.\n   670:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]\n   671:     pub fn checked_add(&self, duration: Duration) -> Option<SystemTime> {\n   672:         self.0.checked_add_duration(&duration).map(SystemTime)\n   673:     }\n   674: \n   675:     /// Returns `Some(t)` where `t` is the time `self - duration` if `t` can be represented as\n   676:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`",
    "nanvix_source": "   650:     /// ```no_run\n   651:     /// use std::thread::sleep;\n   652:     /// use std::time::{Duration, SystemTime};\n   653:     ///\n   654:     /// let sys_time = SystemTime::now();\n   655:     /// let one_sec = Duration::from_secs(1);\n   656:     /// sleep(one_sec);\n   657:     /// assert!(sys_time.elapsed().unwrap() >= one_sec);\n   658:     /// ```\n   659:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   660:     pub fn elapsed(&self) -> Result<Duration, SystemTimeError> {\n   661:         SystemTime::now().duration_since(*self)\n   662:     }\n   663: \n   664:     /// Returns `Some(t)` where `t` is the time `self + duration` if `t` can be represented as\n   665:     /// `SystemTime` (which means it's inside the bounds of the underlying data structure), `None`\n   666:     /// otherwise.\n   667:     ///\n   668:     /// In the case that the `duration` is smaller than the time precision of the operating\n   669:     /// system, `Some(self)` will be returned.\n   670:     #[stable(feature = \"time_checked_add\", since = \"1.34.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::SystemTime::now",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 2591,
            "path": "SystemTime"
          }
        }
      }
    },
    "verification_source": "   585:     ///         .unwrap_or(SystemTime::MIN);\n   586:     /// ```\n   587:     #[unstable(feature = \"time_systemtime_limits\", issue = \"149067\")]\n   588:     pub const MIN: SystemTime = SystemTime(time::SystemTime::MIN);\n   589: \n   590:     /// Returns the system time corresponding to \"now\".\n   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// use std::time::SystemTime;\n   596:     ///\n   597:     /// let sys_time = SystemTime::now();\n   598:     /// ```\n   599:     #[must_use]\n   600:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   601:     pub fn now() -> SystemTime {\n   602:         SystemTime(time::SystemTime::now())\n   603:     }\n   604: \n   605:     /// Returns the amount of time elapsed from an earlier point in time.\n   606:     ///\n   607:     /// This function may fail because measurements taken earlier are not\n   608:     /// guaranteed to always be before later measurements (due to anomalies such\n   609:     /// as the system clock being adjusted either forwards or backwards).\n   610:     /// [`Instant`] can be used to measure elapsed time without this risk of failure.\n   611:     ///\n   612:     /// If successful, <code>[Ok]\\([Duration])</code> is returned where the duration represents\n   613:     /// the amount of time elapsed from the specified measurement to this one.\n   614:     ///\n   615:     /// Returns an [`Err`] if `earlier` is later than `self`, and the error\n   616:     /// contains how far from `self` the time is.\n   617:     ///",
    "nanvix_source": "   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// use std::time::SystemTime;\n   596:     ///\n   597:     /// let sys_time = SystemTime::now();\n   598:     /// ```\n   599:     #[must_use]\n   600:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   601:     pub fn now() -> SystemTime {\n   602:         SystemTime(time::SystemTime::now())\n   603:     }\n   604: \n   605:     /// Returns the amount of time elapsed from an earlier point in time.\n   606:     ///\n   607:     /// This function may fail because measurements taken earlier are not\n   608:     /// guaranteed to always be before later measurements (due to anomalies such\n   609:     /// as the system clock being adjusted either forwards or backwards).\n   610:     /// [`Instant`] can be used to measure elapsed time without this risk of failure.\n   611:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::time::SystemTimeError::duration",
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
      "name": "duration",
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
            "id": 9349,
            "path": "SystemTimeError"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:9400",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:9349",
        "resolved_owner_path": [
          "std",
          "time",
          "SystemTimeError"
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
    "verification_source": "   808: pub const UNIX_EPOCH: SystemTime = SystemTime(time::UNIX_EPOCH);\n   809: \n   810: impl SystemTimeError {\n   811:     /// Returns the positive duration which represents how far forward the\n   812:     /// second system time was from the first.\n   813:     ///\n   814:     /// A `SystemTimeError` is returned from the [`SystemTime::duration_since`]\n   815:     /// and [`SystemTime::elapsed`] methods whenever the second system time\n   816:     /// represents a point later in time than the `self` of the method call.\n   817:     ///\n   818:     /// # Examples\n   819:     ///\n   820:     /// ```no_run\n   821:     /// use std::thread::sleep;\n   822:     /// use std::time::{Duration, SystemTime};\n   823:     ///\n   824:     /// let sys_time = SystemTime::now();\n   825:     /// sleep(Duration::from_secs(1));\n   826:     /// let new_sys_time = SystemTime::now();\n   827:     /// match sys_time.duration_since(new_sys_time) {\n   828:     ///     Ok(_) => {}\n   829:     ///     Err(e) => println!(\"SystemTimeError difference: {:?}\", e.duration()),\n   830:     /// }\n   831:     /// ```\n   832:     #[must_use]\n   833:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   834:     pub fn duration(&self) -> Duration {\n   835:         self.0\n   836:     }\n   837: }\n   838: \n   839: #[stable(feature = \"time2\", since = \"1.8.0\")]\n   840: impl Error for SystemTimeError {}",
    "nanvix_source": "   816:     /// A `SystemTimeError` is returned from the [`SystemTime::duration_since`]\n   817:     /// and [`SystemTime::elapsed`] methods whenever the second system time\n   818:     /// represents a point later in time than the `self` of the method call.\n   819:     ///\n   820:     /// # Examples\n   821:     ///\n   822:     /// ```no_run\n   823:     /// use std::thread::sleep;\n   824:     /// use std::time::{Duration, SystemTime};\n   825:     ///\n   826:     /// let sys_time = SystemTime::now();\n   827:     /// sleep(Duration::from_secs(1));\n   828:     /// let new_sys_time = SystemTime::now();\n   829:     /// match sys_time.duration_since(new_sys_time) {\n   830:     ///     Ok(_) => {}\n   831:     ///     Err(e) => println!(\"SystemTimeError difference: {:?}\", e.duration()),\n   832:     /// }\n   833:     /// ```\n   834:     #[must_use]\n   835:     #[stable(feature = \"time2\", since = \"1.8.0\")]\n   836:     pub fn duration(&self) -> Duration {",
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
