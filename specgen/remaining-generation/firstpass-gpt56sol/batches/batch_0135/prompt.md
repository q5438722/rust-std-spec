For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::panic::PanicInfo::payload",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "payload",
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
            "id": 12971,
            "path": "PanicInfo"
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
        "impl_id": "core:28214",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:12971",
        "resolved_owner_path": [
          "core",
          "panic",
          "panic_info",
          "PanicInfo"
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
              "dyn_trait": {
                "lifetime": null,
                "traits": [
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 916,
                      "path": "crate::any::Any"
                    }
                  },
                  {
                    "generic_params": [],
                    "trait": {
                      "args": null,
                      "id": 10,
                      "path": "Send"
                    }
                  }
                ]
              }
            }
          }
        }
      }
    },
    "verification_source": "    94:         Some(&self.location)\n    95:     }\n    96: \n    97:     /// Returns the payload associated with the panic.\n    98:     ///\n    99:     /// On this type, `core::panic::PanicInfo`, this method never returns anything useful.\n   100:     /// It only exists because of compatibility with [`std::panic::PanicHookInfo`],\n   101:     /// which used to be the same type.\n   102:     ///\n   103:     /// See [`std::panic::PanicHookInfo::payload`].\n   104:     ///\n   105:     /// [`std::panic::PanicHookInfo`]: ../../std/panic/struct.PanicHookInfo.html\n   106:     /// [`std::panic::PanicHookInfo::payload`]: ../../std/panic/struct.PanicHookInfo.html#method.payload\n   107:     #[deprecated(since = \"1.81.0\", note = \"this never returns anything useful\")]\n   108:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   109:     #[allow(deprecated, deprecated_in_future)]\n   110:     pub fn payload(&self) -> &(dyn crate::any::Any + Send) {\n   111:         struct NoPayload;\n   112:         &NoPayload\n   113:     }\n   114: \n   115:     /// Returns whether the panic handler is allowed to unwind the stack from\n   116:     /// the point where the panic occurred.\n   117:     ///\n   118:     /// This is true for most kinds of panics with the exception of panics\n   119:     /// caused by trying to unwind out of a `Drop` implementation or a function\n   120:     /// whose ABI does not support unwinding.\n   121:     ///\n   122:     /// It is safe for a panic handler to unwind even when this function returns\n   123:     /// false, however this will simply cause the panic handler to be called\n   124:     /// again.\n   125:     #[must_use]\n   126:     #[unstable(feature = \"panic_can_unwind\", issue = \"92988\")]",
    "nanvix_source": "   100:     /// It only exists because of compatibility with [`std::panic::PanicHookInfo`],\n   101:     /// which used to be the same type.\n   102:     ///\n   103:     /// See [`std::panic::PanicHookInfo::payload`].\n   104:     ///\n   105:     /// [`std::panic::PanicHookInfo`]: ../../std/panic/struct.PanicHookInfo.html\n   106:     /// [`std::panic::PanicHookInfo::payload`]: ../../std/panic/struct.PanicHookInfo.html#method.payload\n   107:     #[deprecated(since = \"1.81.0\", note = \"this never returns anything useful\")]\n   108:     #[stable(feature = \"panic_hooks\", since = \"1.10.0\")]\n   109:     #[allow(deprecated, deprecated_in_future)]\n   110:     pub fn payload(&self) -> &(dyn crate::any::Any + Send) {\n   111:         struct NoPayload;\n   112:         &NoPayload\n   113:     }\n   114: \n   115:     /// Returns whether the panic handler is allowed to unwind the stack from\n   116:     /// the point where the panic occurred.\n   117:     ///\n   118:     /// This is true for most kinds of panics with the exception of panics\n   119:     /// caused by trying to unwind out of a `Drop` implementation or a function\n   120:     /// whose ABI does not support unwinding.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::PanicMessage::as_str",
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
            "id": 13398,
            "path": "PanicMessage"
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
        "impl_id": "core:28231",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:13398",
        "resolved_owner_path": [
          "core",
          "panic",
          "panic_info",
          "PanicMessage"
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
                        "lifetime": "'static",
                        "type": {
                          "primitive": "str"
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
    "verification_source": "   142: \n   143: #[stable(feature = \"panic_hook_display\", since = \"1.26.0\")]\n   144: impl Display for PanicInfo<'_> {\n   145:     fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {\n   146:         formatter.write_str(\"panicked at \")?;\n   147:         self.location.fmt(formatter)?;\n   148:         formatter.write_str(\":\\n\")?;\n   149:         formatter.write_fmt(*self.message)?;\n   150:         Ok(())\n   151:     }\n   152: }\n   153: \n   154: impl<'a> PanicMessage<'a> {\n   155:     /// Gets the formatted message, if it has no arguments to be formatted at runtime.\n   156:     ///\n   157:     /// This can be used to avoid allocations in some cases.\n   158:     ///\n   159:     /// # Guarantees\n   160:     ///\n   161:     /// For `panic!(\"just a literal\")`, this function is guaranteed to\n   162:     /// return `Some(\"just a literal\")`.\n   163:     ///\n   164:     /// For most cases with placeholders, this function will return `None`.\n   165:     ///\n   166:     /// See [`fmt::Arguments::as_str`] for details.\n   167:     #[stable(feature = \"panic_info_message\", since = \"1.81.0\")]\n   168:     #[rustc_const_stable(feature = \"const_arguments_as_str\", since = \"1.84.0\")]\n   169:     #[must_use]\n   170:     #[inline]\n   171:     pub const fn as_str(&self) -> Option<&'static str> {\n   172:         self.message.as_str()\n   173:     }\n   174: }",
    "nanvix_source": "   148:         formatter.write_str(\":\\n\")?;\n   149:         formatter.write_fmt(*self.message)?;\n   150:         Ok(())\n   151:     }\n   152: }\n   153: \n   154: impl<'a> PanicMessage<'a> {\n   155:     /// Gets the formatted message, if it has no arguments to be formatted at runtime.\n   156:     ///\n   157:     /// This can be used to avoid allocations in some cases.\n   158:     ///\n   159:     /// # Guarantees\n   160:     ///\n   161:     /// For `panic!(\"just a literal\")`, this function is guaranteed to\n   162:     /// return `Some(\"just a literal\")`.\n   163:     ///\n   164:     /// For most cases with placeholders, this function will return `None`.\n   165:     ///\n   166:     /// See [`fmt::Arguments::as_str`] for details.\n   167:     #[stable(feature = \"panic_info_message\", since = \"1.81.0\")]\n   168:     #[rustc_const_stable(feature = \"const_arguments_as_str\", since = \"1.84.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::get_ref",
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
      "name": "get_ref",
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
                        "lifetime": "'a",
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
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            },
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
        "impl_id": "core:29043",
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
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1552:     /// not a problem as long as there does not also exist a `Pin<&T>` pointing\n  1553:     /// to the inner `T` inside the `RefCell`, and `RefCell<T>` does not let you get a\n  1554:     /// `Pin<&T>` pointer to its contents. See the discussion on [\"pinning projections\"]\n  1555:     /// for further details.\n  1556:     ///\n  1557:     /// Note: `Pin` also implements `Deref` to the target, which can be used\n  1558:     /// to access the inner value. However, `Deref` only provides a reference\n  1559:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of\n  1560:     /// the reference contained in the `Pin`. This method allows turning the `Pin` into a reference\n  1561:     /// with the same lifetime as the reference it wraps.\n  1562:     ///\n  1563:     /// [\"pinning projections\"]: self#projections-and-structural-pinning\n  1564:     #[inline(always)]\n  1565:     #[must_use]\n  1566:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1567:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1568:     pub const fn get_ref(self) -> &'a T {\n  1569:         self.pointer\n  1570:     }\n  1571: }\n  1572: \n  1573: impl<'a, T: ?Sized> Pin<&'a mut T> {\n  1574:     /// Converts this `Pin<&mut T>` into a `Pin<&T>` with the same lifetime.\n  1575:     #[inline(always)]\n  1576:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1577:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1578:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1579:     pub const fn into_ref(self) -> Pin<&'a T> {\n  1580:         Pin { pointer: self.pointer }\n  1581:     }\n  1582: \n  1583:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1584:     ///",
    "nanvix_source": "  1558:     /// to access the inner value. However, `Deref` only provides a reference\n  1559:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of\n  1560:     /// the reference contained in the `Pin`. This method allows turning the `Pin` into a reference\n  1561:     /// with the same lifetime as the reference it wraps.\n  1562:     ///\n  1563:     /// [\"pinning projections\"]: self#projections-and-structural-pinning\n  1564:     #[inline(always)]\n  1565:     #[must_use]\n  1566:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1567:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1568:     pub const fn get_ref(self) -> &'a T {\n  1569:         self.pointer\n  1570:     }\n  1571: }\n  1572: \n  1573: impl<'a, T: ?Sized> Pin<&'a mut T> {\n  1574:     /// Converts this `Pin<&mut T>` into a `Pin<&T>` with the same lifetime.\n  1575:     #[inline(always)]\n  1576:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1577:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1578:     #[stable(feature = \"pin\", since = \"1.33.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::into_inner",
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
      "name": "into_inner",
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
                          "args": {
                            "angle_bracketed": {
                              "args": [],
                              "constraints": [
                                {
                                  "args": null,
                                  "binding": {
                                    "constraint": [
                                      {
                                        "trait_bound": {
                                          "generic_params": [],
                                          "modifier": "none",
                                          "trait": {
                                            "args": null,
                                            "id": 16,
                                            "path": "Unpin"
                                          }
                                        }
                                      }
                                    ]
                                  },
                                  "name": "Target"
                                }
                              ]
                            }
                          },
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
        "impl_id": "core:29031",
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
            "pin",
            {
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
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Ptr"
        }
      }
    },
    "verification_source": "  1194:     /// ```\n  1195:     /// use std::pin::Pin;\n  1196:     ///\n  1197:     /// let mut val: u8 = 5;\n  1198:     /// let pinned: Pin<&mut u8> = Pin::new(&mut val);\n  1199:     ///\n  1200:     /// // Unwrap the pin to get the underlying mutable reference to the value. We can do\n  1201:     /// // this because `val` doesn't care about being moved, so the `Pin` was just\n  1202:     /// // a \"facade\" anyway.\n  1203:     /// let r = Pin::into_inner(pinned);\n  1204:     /// assert_eq!(*r, 5);\n  1205:     /// ```\n  1206:     #[inline(always)]\n  1207:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1208:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1209:     #[stable(feature = \"pin_into_inner\", since = \"1.39.0\")]\n  1210:     pub const fn into_inner(pin: Pin<Ptr>) -> Ptr {\n  1211:         pin.pointer\n  1212:     }\n  1213: }\n  1214: \n  1215: impl<Ptr: Deref> Pin<Ptr> {\n  1216:     /// Constructs a new `Pin<Ptr>` around a reference to some data of a type that\n  1217:     /// may or may not implement [`Unpin`].\n  1218:     ///\n  1219:     /// If `pointer` dereferences to an [`Unpin`] type, [`Pin::new`] should be used\n  1220:     /// instead.\n  1221:     ///\n  1222:     /// # Safety\n  1223:     ///\n  1224:     /// This constructor is unsafe because we cannot guarantee that the data\n  1225:     /// pointed to by `pointer` is pinned. At its core, pinning a value means making the\n  1226:     /// guarantee that the value's data will not be moved nor have its storage invalidated until",
    "nanvix_source": "  1200:     /// // Unwrap the pin to get the underlying mutable reference to the value. We can do\n  1201:     /// // this because `val` doesn't care about being moved, so the `Pin` was just\n  1202:     /// // a \"facade\" anyway.\n  1203:     /// let r = Pin::into_inner(pinned);\n  1204:     /// assert_eq!(*r, 5);\n  1205:     /// ```\n  1206:     #[inline(always)]\n  1207:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1208:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1209:     #[stable(feature = \"pin_into_inner\", since = \"1.39.0\")]\n  1210:     pub const fn into_inner(pin: Pin<Ptr>) -> Ptr {\n  1211:         pin.pointer\n  1212:     }\n  1213: }\n  1214: \n  1215: impl<Ptr: Deref> Pin<Ptr> {\n  1216:     /// Constructs a new `Pin<Ptr>` around a reference to some data of a type that\n  1217:     /// may or may not implement [`Unpin`].\n  1218:     ///\n  1219:     /// If `pointer` dereferences to an [`Unpin`] type, [`Pin::new`] should be used\n  1220:     /// instead.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::into_ref",
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
      "name": "into_ref",
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
                        "is_mutable": true,
                        "lifetime": "'a",
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
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            },
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
        "impl_id": "core:29048",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": "'a",
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
    "verification_source": "  1563:     /// [\"pinning projections\"]: self#projections-and-structural-pinning\n  1564:     #[inline(always)]\n  1565:     #[must_use]\n  1566:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1567:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1568:     pub const fn get_ref(self) -> &'a T {\n  1569:         self.pointer\n  1570:     }\n  1571: }\n  1572: \n  1573: impl<'a, T: ?Sized> Pin<&'a mut T> {\n  1574:     /// Converts this `Pin<&mut T>` into a `Pin<&T>` with the same lifetime.\n  1575:     #[inline(always)]\n  1576:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1577:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1578:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1579:     pub const fn into_ref(self) -> Pin<&'a T> {\n  1580:         Pin { pointer: self.pointer }\n  1581:     }\n  1582: \n  1583:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1584:     ///\n  1585:     /// This requires that the data inside this `Pin` is `Unpin`.\n  1586:     ///\n  1587:     /// Note: `Pin` also implements `DerefMut` to the data, which can be used\n  1588:     /// to access the inner value. However, `DerefMut` only provides a reference\n  1589:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of\n  1590:     /// the `Pin` itself. This method allows turning the `Pin` into a reference\n  1591:     /// with the same lifetime as the original `Pin`.\n  1592:     #[inline(always)]\n  1593:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1594:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1595:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]",
    "nanvix_source": "  1569:         self.pointer\n  1570:     }\n  1571: }\n  1572: \n  1573: impl<'a, T: ?Sized> Pin<&'a mut T> {\n  1574:     /// Converts this `Pin<&mut T>` into a `Pin<&T>` with the same lifetime.\n  1575:     #[inline(always)]\n  1576:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1577:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1578:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1579:     pub const fn into_ref(self) -> Pin<&'a T> {\n  1580:         Pin { pointer: self.pointer }\n  1581:     }\n  1582: \n  1583:     /// Gets a mutable reference to the data inside of this `Pin`.\n  1584:     ///\n  1585:     /// This requires that the data inside this `Pin` is `Unpin`.\n  1586:     ///\n  1587:     /// Note: `Pin` also implements `DerefMut` to the data, which can be used\n  1588:     /// to access the inner value. However, `DerefMut` only provides a reference\n  1589:     /// that lives for as long as the borrow of the `Pin`, not the lifetime of",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::pin::Pin::new",
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
      "name": "new",
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
                          "args": {
                            "angle_bracketed": {
                              "args": [],
                              "constraints": [
                                {
                                  "args": null,
                                  "binding": {
                                    "constraint": [
                                      {
                                        "trait_bound": {
                                          "generic_params": [],
                                          "modifier": "none",
                                          "trait": {
                                            "args": null,
                                            "id": 16,
                                            "path": "Unpin"
                                          }
                                        }
                                      }
                                    ]
                                  },
                                  "name": "Target"
                                }
                              ]
                            }
                          },
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
        "impl_id": "core:29031",
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
            "pointer",
            {
              "generic": "Ptr"
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
        }
      }
    },
    "verification_source": "  1165:     ///\n  1166:     /// # Examples\n  1167:     ///\n  1168:     /// ```\n  1169:     /// use std::pin::Pin;\n  1170:     ///\n  1171:     /// let mut val: u8 = 5;\n  1172:     ///\n  1173:     /// // Since `val` doesn't care about being moved, we can safely create a \"facade\" `Pin`\n  1174:     /// // which will allow `val` to participate in `Pin`-bound apis  without checking that\n  1175:     /// // pinning guarantees are actually upheld.\n  1176:     /// let mut pinned: Pin<&mut u8> = Pin::new(&mut val);\n  1177:     /// ```\n  1178:     #[inline(always)]\n  1179:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1180:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1181:     pub const fn new(pointer: Ptr) -> Pin<Ptr> {\n  1182:         // SAFETY: the value pointed to is `Unpin`, and so has no requirements\n  1183:         // around pinning.\n  1184:         unsafe { Pin::new_unchecked(pointer) }\n  1185:     }\n  1186: \n  1187:     /// Unwraps this `Pin<Ptr>`, returning the underlying pointer.\n  1188:     ///\n  1189:     /// Doing this operation safely requires that the data pointed at by this pinning pointer\n  1190:     /// implements [`Unpin`] so that we can ignore the pinning invariants when unwrapping it.\n  1191:     ///\n  1192:     /// # Examples\n  1193:     ///\n  1194:     /// ```\n  1195:     /// use std::pin::Pin;\n  1196:     ///\n  1197:     /// let mut val: u8 = 5;",
    "nanvix_source": "  1171:     /// let mut val: u8 = 5;\n  1172:     ///\n  1173:     /// // Since `val` doesn't care about being moved, we can safely create a \"facade\" `Pin`\n  1174:     /// // which will allow `val` to participate in `Pin`-bound apis  without checking that\n  1175:     /// // pinning guarantees are actually upheld.\n  1176:     /// let mut pinned: Pin<&mut u8> = Pin::new(&mut val);\n  1177:     /// ```\n  1178:     #[inline(always)]\n  1179:     #[rustc_const_stable(feature = \"const_pin\", since = \"1.84.0\")]\n  1180:     #[stable(feature = \"pin\", since = \"1.33.0\")]\n  1181:     pub const fn new(pointer: Ptr) -> Pin<Ptr> {\n  1182:         // SAFETY: the value pointed to is `Unpin`, and so has no requirements\n  1183:         // around pinning.\n  1184:         unsafe { Pin::new_unchecked(pointer) }\n  1185:     }\n  1186: \n  1187:     /// Unwraps this `Pin<Ptr>`, returning the underlying pointer.\n  1188:     ///\n  1189:     /// Doing this operation safely requires that the data pointed at by this pinning pointer\n  1190:     /// implements [`Unpin`] so that we can ignore the pinning invariants when unwrapping it.\n  1191:     ///",
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
