For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::mem::drop",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
            "name": "T"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
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
      "name": "drop",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "_x",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   983: /// #[derive(Copy, Clone)]\n   984: /// struct Foo(u8);\n   985: ///\n   986: /// let x = 1;\n   987: /// let y = Foo(2);\n   988: /// drop(x); // a copy of `x` is moved and dropped\n   989: /// drop(y); // a copy of `y` is moved and dropped\n   990: ///\n   991: /// println!(\"x: {}, y: {}\", x, y.0); // still available\n   992: /// ```\n   993: ///\n   994: /// [`RefCell`]: crate::cell::RefCell\n   995: #[inline]\n   996: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   997: #[rustc_const_unstable(feature = \"const_destruct\", issue = \"133214\")]\n   998: #[rustc_diagnostic_item = \"mem_drop\"]\n   999: pub const fn drop<T>(_x: T)\n  1000: where\n  1001:     T: [const] Destruct,\n  1002: {\n  1003: }\n  1004: \n  1005: /// Bitwise-copies a value.\n  1006: ///\n  1007: /// This function is not magic; it is literally defined as\n  1008: /// ```\n  1009: /// pub const fn copy<T: Copy>(x: &T) -> T { *x }\n  1010: /// ```\n  1011: ///\n  1012: /// It is useful when you want to pass a function pointer to a combinator, rather than defining a new closure.\n  1013: ///\n  1014: /// Example:\n  1015: /// ```",
    "nanvix_source": "  1028: /// drop(y); // a copy of `y` is moved and dropped\n  1029: ///\n  1030: /// println!(\"x: {}, y: {}\", x, y.0); // still available\n  1031: /// ```\n  1032: ///\n  1033: /// [`RefCell`]: crate::cell::RefCell\n  1034: #[inline]\n  1035: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1036: #[rustc_const_unstable(feature = \"const_destruct\", issue = \"133214\")]\n  1037: #[rustc_diagnostic_item = \"mem_drop\"]\n  1038: pub const fn drop<T>(_x: T)\n  1039: where\n  1040:     T: [const] Destruct,\n  1041: {\n  1042: }\n  1043: \n  1044: /// Bitwise-copies a value.\n  1045: ///\n  1046: /// This function is not magic; it is literally defined as\n  1047: /// ```\n  1048: /// pub const fn copy<T: Copy>(x: &T) -> T { *x }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::forget",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
            "name": "T"
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
      "name": "forget",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "t",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   172: /// double free. In other words, `ManuallyDrop` errs on the side of leaking instead of\n   173: /// erring on the side of (double-)dropping.\n   174: ///\n   175: /// Also, `ManuallyDrop` prevents us from having to \"touch\" `v` after transferring the\n   176: /// ownership to `s` \u2014 the final step of interacting with `v` to dispose of it without\n   177: /// running its destructor is entirely avoided.\n   178: ///\n   179: /// [`Box`]: ../../std/boxed/struct.Box.html\n   180: /// [`Box::leak`]: ../../std/boxed/struct.Box.html#method.leak\n   181: /// [`Box::into_raw`]: ../../std/boxed/struct.Box.html#method.into_raw\n   182: /// [`mem::drop`]: drop\n   183: /// [ub]: ../../reference/behavior-considered-undefined.html\n   184: #[inline]\n   185: #[rustc_const_stable(feature = \"const_forget\", since = \"1.46.0\")]\n   186: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   187: #[rustc_diagnostic_item = \"mem_forget\"]\n   188: pub const fn forget<T>(t: T) {\n   189:     let _ = ManuallyDrop::new(t);\n   190: }\n   191: \n   192: /// Like [`forget`], but also accepts unsized values.\n   193: ///\n   194: /// While Rust does not permit unsized locals since its removal in [#111942] it is\n   195: /// still possible to call functions with unsized values from a function argument\n   196: /// or place expression.\n   197: ///\n   198: /// ```rust\n   199: /// #![feature(unsized_fn_params, forget_unsized)]\n   200: /// #![allow(internal_features)]\n   201: ///\n   202: /// use std::mem::forget_unsized;\n   203: ///\n   204: /// pub fn in_place() {",
    "nanvix_source": "   180: ///\n   181: /// [`Box`]: ../../std/boxed/struct.Box.html\n   182: /// [`Box::leak`]: ../../std/boxed/struct.Box.html#method.leak\n   183: /// [`Box::into_raw`]: ../../std/boxed/struct.Box.html#method.into_raw\n   184: /// [`mem::drop`]: drop\n   185: /// [ub]: ../../reference/behavior-considered-undefined.html\n   186: #[inline]\n   187: #[rustc_const_stable(feature = \"const_forget\", since = \"1.46.0\")]\n   188: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   189: #[rustc_diagnostic_item = \"mem_forget\"]\n   190: pub const fn forget<T>(t: T) {\n   191:     let _ = ManuallyDrop::new(t);\n   192: }\n   193: \n   194: /// Like [`forget`], but also accepts unsized values.\n   195: ///\n   196: /// While Rust does not permit unsized locals since its removal in [#111942] it is\n   197: /// still possible to call functions with unsized values from a function argument\n   198: /// or place expression.\n   199: ///\n   200: /// ```rust",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::panic::set_hook",
    "generation_group": "no_modeled_observable_output",
    "classification": "no_modeled_observable_output",
    "classification_reasons": [
      "unit_result_without_mutable_output_state"
    ],
    "category": "other",
    "kinds": [
      "free_function"
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
      "name": "set_hook",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "hook",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "dyn_trait": {
                            "lifetime": "'static",
                            "traits": [
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": {
                                    "parenthesized": {
                                      "inputs": [
                                        {
                                          "borrowed_ref": {
                                            "is_mutable": false,
                                            "lifetime": null,
                                            "type": {
                                              "resolved_path": {
                                                "args": {
                                                  "angle_bracketed": {
                                                    "args": [
                                                      {
                                                        "lifetime": "'_"
                                                      }
                                                    ],
                                                    "constraints": []
                                                  }
                                                },
                                                "id": 6615,
                                                "path": "crate::panic::PanicHookInfo"
                                              }
                                            }
                                          }
                                        }
                                      ],
                                      "output": null
                                    }
                                  },
                                  "id": 16,
                                  "path": "Fn"
                                }
                              },
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 10,
                                  "path": "Sync"
                                }
                              },
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 6,
                                  "path": "Send"
                                }
                              }
                            ]
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 216,
                "path": "Box"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   126: /// Panics if called from a panicking thread.\n   127: ///\n   128: /// # Examples\n   129: ///\n   130: /// The following will print \"Custom panic hook\":\n   131: ///\n   132: /// ```should_panic\n   133: /// use std::panic;\n   134: ///\n   135: /// panic::set_hook(Box::new(|_| {\n   136: ///     println!(\"Custom panic hook\");\n   137: /// }));\n   138: ///\n   139: /// panic!(\"Normal panic\");\n   140: /// ```\n   141: #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   142: pub fn set_hook(hook: Box<dyn Fn(&PanicHookInfo<'_>) + 'static + Sync + Send>) {\n   143:     if thread::panicking() {\n   144:         panic!(\"cannot modify the panic hook from a panicking thread\");\n   145:     }\n   146: \n   147:     // Drop the old hook after changing the hook to avoid deadlocking if its\n   148:     // destructor panics.\n   149:     drop(HOOK.replace(Hook::Custom(hook)));\n   150: }\n   151: \n   152: /// Unregisters the current panic hook and returns it, registering the default hook\n   153: /// in its place.\n   154: ///\n   155: /// *See also the function [`set_hook`].*\n   156: ///\n   157: /// [`set_hook`]: ./fn.set_hook.html\n   158: ///",
    "nanvix_source": "   132: /// ```should_panic\n   133: /// use std::panic;\n   134: ///\n   135: /// panic::set_hook(Box::new(|_| {\n   136: ///     println!(\"Custom panic hook\");\n   137: /// }));\n   138: ///\n   139: /// panic!(\"Normal panic\");\n   140: /// ```\n   141: #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   142: pub fn set_hook(hook: Box<dyn Fn(&PanicHookInfo<'_>) + 'static + Sync + Send>) {\n   143:     if thread::panicking() {\n   144:         panic!(\"cannot modify the panic hook from a panicking thread\");\n   145:     }\n   146: \n   147:     // Drop the old hook after changing the hook to avoid deadlocking if its\n   148:     // destructor panics.\n   149:     drop(HOOK.replace(Hook::Custom(hook)));\n   150: }\n   151: \n   152: /// Unregisters the current panic hook and returns it, registering the default hook",
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
