For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::ControlFlow::is_break",
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
      "name": "is_break",
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
                      "generic": "B"
                    }
                  },
                  {
                    "type": {
                      "generic": "C"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9735,
            "path": "ControlFlow"
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
              "name": "B"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "C"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23404",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9735",
        "resolved_owner_path": [
          "core",
          "ops",
          "control_flow",
          "ControlFlow"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   139: }\n   140: \n   141: impl<B, C> ControlFlow<B, C> {\n   142:     /// Returns `true` if this is a `Break` variant.\n   143:     ///\n   144:     /// # Examples\n   145:     ///\n   146:     /// ```\n   147:     /// use std::ops::ControlFlow;\n   148:     ///\n   149:     /// assert!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").is_break());\n   150:     /// assert!(!ControlFlow::<&str, i32>::Continue(3).is_break());\n   151:     /// ```\n   152:     #[inline]\n   153:     #[stable(feature = \"control_flow_enum_is\", since = \"1.59.0\")]\n   154:     #[rustc_const_stable(feature = \"min_const_control_flow\", since = \"1.95.0\")]\n   155:     pub const fn is_break(&self) -> bool {\n   156:         matches!(*self, ControlFlow::Break(_))\n   157:     }\n   158: \n   159:     /// Returns `true` if this is a `Continue` variant.\n   160:     ///\n   161:     /// # Examples\n   162:     ///\n   163:     /// ```\n   164:     /// use std::ops::ControlFlow;\n   165:     ///\n   166:     /// assert!(!ControlFlow::<&str, i32>::Break(\"Stop right there!\").is_continue());\n   167:     /// assert!(ControlFlow::<&str, i32>::Continue(3).is_continue());\n   168:     /// ```\n   169:     #[inline]\n   170:     #[stable(feature = \"control_flow_enum_is\", since = \"1.59.0\")]\n   171:     #[rustc_const_stable(feature = \"min_const_control_flow\", since = \"1.95.0\")]",
    "nanvix_source": "   146:     ///\n   147:     /// ```\n   148:     /// use std::ops::ControlFlow;\n   149:     ///\n   150:     /// assert!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").is_break());\n   151:     /// assert!(!ControlFlow::<&str, i32>::Continue(3).is_break());\n   152:     /// ```\n   153:     #[inline]\n   154:     #[stable(feature = \"control_flow_enum_is\", since = \"1.59.0\")]\n   155:     #[rustc_const_stable(feature = \"min_const_control_flow\", since = \"1.95.0\")]\n   156:     pub const fn is_break(&self) -> bool {\n   157:         matches!(*self, ControlFlow::Break(_))\n   158:     }\n   159: \n   160:     /// Returns `true` if this is a `Continue` variant.\n   161:     ///\n   162:     /// # Examples\n   163:     ///\n   164:     /// ```\n   165:     /// use std::ops::ControlFlow;\n   166:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::is_continue",
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
      "name": "is_continue",
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
                      "generic": "B"
                    }
                  },
                  {
                    "type": {
                      "generic": "C"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9735,
            "path": "ControlFlow"
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
              "name": "B"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "C"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23404",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9735",
        "resolved_owner_path": [
          "core",
          "ops",
          "control_flow",
          "ControlFlow"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   156:         matches!(*self, ControlFlow::Break(_))\n   157:     }\n   158: \n   159:     /// Returns `true` if this is a `Continue` variant.\n   160:     ///\n   161:     /// # Examples\n   162:     ///\n   163:     /// ```\n   164:     /// use std::ops::ControlFlow;\n   165:     ///\n   166:     /// assert!(!ControlFlow::<&str, i32>::Break(\"Stop right there!\").is_continue());\n   167:     /// assert!(ControlFlow::<&str, i32>::Continue(3).is_continue());\n   168:     /// ```\n   169:     #[inline]\n   170:     #[stable(feature = \"control_flow_enum_is\", since = \"1.59.0\")]\n   171:     #[rustc_const_stable(feature = \"min_const_control_flow\", since = \"1.95.0\")]\n   172:     pub const fn is_continue(&self) -> bool {\n   173:         matches!(*self, ControlFlow::Continue(_))\n   174:     }\n   175: \n   176:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the\n   177:     /// `ControlFlow` was `Break` and `None` otherwise.\n   178:     ///\n   179:     /// # Examples\n   180:     ///\n   181:     /// ```\n   182:     /// use std::ops::ControlFlow;\n   183:     ///\n   184:     /// assert_eq!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").break_value(), Some(\"Stop right there!\"));\n   185:     /// assert_eq!(ControlFlow::<&str, i32>::Continue(3).break_value(), None);\n   186:     /// ```\n   187:     #[inline]\n   188:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]",
    "nanvix_source": "   163:     ///\n   164:     /// ```\n   165:     /// use std::ops::ControlFlow;\n   166:     ///\n   167:     /// assert!(!ControlFlow::<&str, i32>::Break(\"Stop right there!\").is_continue());\n   168:     /// assert!(ControlFlow::<&str, i32>::Continue(3).is_continue());\n   169:     /// ```\n   170:     #[inline]\n   171:     #[stable(feature = \"control_flow_enum_is\", since = \"1.59.0\")]\n   172:     #[rustc_const_stable(feature = \"min_const_control_flow\", since = \"1.95.0\")]\n   173:     pub const fn is_continue(&self) -> bool {\n   174:         matches!(*self, ControlFlow::Continue(_))\n   175:     }\n   176: \n   177:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the\n   178:     /// `ControlFlow` was `Break` and `None` otherwise.\n   179:     ///\n   180:     /// # Examples\n   181:     ///\n   182:     /// ```\n   183:     /// use std::ops::ControlFlow;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::RangeFrom::contains",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
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
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Idx"
              }
            }
          },
          {
            "bound_predicate": {
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
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Idx"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
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
      "name": "contains",
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
                      "generic": "Idx"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9747,
            "path": "RangeFrom"
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
                              "args": [
                                {
                                  "type": {
                                    "generic": "Idx"
                                  }
                                }
                              ],
                              "constraints": []
                            }
                          },
                          "id": 58,
                          "path": "PartialOrd"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Idx"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23756",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9747",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "RangeFrom"
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
            "item",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "U"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   213:     /// Returns `true` if `item` is contained in the range.\n   214:     ///\n   215:     /// # Examples\n   216:     ///\n   217:     /// ```\n   218:     /// assert!(!(3..).contains(&2));\n   219:     /// assert!( (3..).contains(&3));\n   220:     /// assert!( (3..).contains(&1_000_000_000));\n   221:     ///\n   222:     /// assert!( (0.0..).contains(&0.5));\n   223:     /// assert!(!(0.0..).contains(&f32::NAN));\n   224:     /// assert!(!(f32::NAN..).contains(&0.5));\n   225:     /// ```\n   226:     #[inline]\n   227:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   228:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   229:     pub const fn contains<U>(&self, item: &U) -> bool\n   230:     where\n   231:         Idx: [const] PartialOrd<U>,\n   232:         U: ?Sized + [const] PartialOrd<Idx>,\n   233:     {\n   234:         <Self as RangeBounds<Idx>>::contains(self, item)\n   235:     }\n   236: }\n   237: \n   238: /// A range only bounded exclusively above (`..end`).\n   239: ///\n   240: /// The `RangeTo` `..end` contains all values with `x < end`.\n   241: /// It cannot serve as an [`Iterator`] because it doesn't have a starting point.\n   242: ///\n   243: /// # Examples\n   244: ///\n   245: /// The `..end` syntax is a `RangeTo`:",
    "nanvix_source": "   219:     /// assert!( (3..).contains(&3));\n   220:     /// assert!( (3..).contains(&1_000_000_000));\n   221:     ///\n   222:     /// assert!( (0.0..).contains(&0.5));\n   223:     /// assert!(!(0.0..).contains(&f32::NAN));\n   224:     /// assert!(!(f32::NAN..).contains(&0.5));\n   225:     /// ```\n   226:     #[inline]\n   227:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   228:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   229:     pub const fn contains<U>(&self, item: &U) -> bool\n   230:     where\n   231:         Idx: [const] PartialOrd<U>,\n   232:         U: ?Sized + [const] PartialOrd<Idx>,\n   233:     {\n   234:         <Self as RangeBounds<Idx>>::contains(self, item)\n   235:     }\n   236: }\n   237: \n   238: /// A range only bounded exclusively above (`..end`).\n   239: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::RangeTo::contains",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
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
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Idx"
              }
            }
          },
          {
            "bound_predicate": {
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
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Idx"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
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
      "name": "contains",
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
                      "generic": "Idx"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9750,
            "path": "RangeTo"
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
                              "args": [
                                {
                                  "type": {
                                    "generic": "Idx"
                                  }
                                }
                              ],
                              "constraints": []
                            }
                          },
                          "id": 58,
                          "path": "PartialOrd"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Idx"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23816",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9750",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "RangeTo"
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
            "item",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "U"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   297:     /// Returns `true` if `item` is contained in the range.\n   298:     ///\n   299:     /// # Examples\n   300:     ///\n   301:     /// ```\n   302:     /// assert!( (..5).contains(&-1_000_000_000));\n   303:     /// assert!( (..5).contains(&4));\n   304:     /// assert!(!(..5).contains(&5));\n   305:     ///\n   306:     /// assert!( (..1.0).contains(&0.5));\n   307:     /// assert!(!(..1.0).contains(&f32::NAN));\n   308:     /// assert!(!(..f32::NAN).contains(&0.5));\n   309:     /// ```\n   310:     #[inline]\n   311:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   312:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   313:     pub const fn contains<U>(&self, item: &U) -> bool\n   314:     where\n   315:         Idx: [const] PartialOrd<U>,\n   316:         U: ?Sized + [const] PartialOrd<Idx>,\n   317:     {\n   318:         <Self as RangeBounds<Idx>>::contains(self, item)\n   319:     }\n   320: }\n   321: \n   322: /// A range bounded inclusively below and above (`start..=end`).\n   323: ///\n   324: /// The `RangeInclusive` `start..=end` contains all values with `x >= start`\n   325: /// and `x <= end`. It is empty unless `start <= end`.\n   326: ///\n   327: /// This iterator is [fused], but the specific values of `start` and `end` after\n   328: /// iteration has finished are **unspecified** other than that [`.is_empty()`]\n   329: /// will return `true` once no more values will be produced.",
    "nanvix_source": "   303:     /// assert!( (..5).contains(&4));\n   304:     /// assert!(!(..5).contains(&5));\n   305:     ///\n   306:     /// assert!( (..1.0).contains(&0.5));\n   307:     /// assert!(!(..1.0).contains(&f32::NAN));\n   308:     /// assert!(!(..f32::NAN).contains(&0.5));\n   309:     /// ```\n   310:     #[inline]\n   311:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   312:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   313:     pub const fn contains<U>(&self, item: &U) -> bool\n   314:     where\n   315:         Idx: [const] PartialOrd<U>,\n   316:         U: ?Sized + [const] PartialOrd<Idx>,\n   317:     {\n   318:         <Self as RangeBounds<Idx>>::contains(self, item)\n   319:     }\n   320: }\n   321: \n   322: /// A range bounded inclusively below and above (`start..=end`).\n   323: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::RangeToInclusive::contains",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
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
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Idx"
              }
            }
          },
          {
            "bound_predicate": {
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
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe_const",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Idx"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "U"
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
      "name": "contains",
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
                      "generic": "Idx"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9756,
            "path": "RangeToInclusive"
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
                              "args": [
                                {
                                  "type": {
                                    "generic": "Idx"
                                  }
                                }
                              ],
                              "constraints": []
                            }
                          },
                          "id": 58,
                          "path": "PartialOrd"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "Idx"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:23954",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9756",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "RangeToInclusive"
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
            "item",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "U"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   626:     /// Returns `true` if `item` is contained in the range.\n   627:     ///\n   628:     /// # Examples\n   629:     ///\n   630:     /// ```\n   631:     /// assert!( (..=5).contains(&-1_000_000_000));\n   632:     /// assert!( (..=5).contains(&5));\n   633:     /// assert!(!(..=5).contains(&6));\n   634:     ///\n   635:     /// assert!( (..=1.0).contains(&1.0));\n   636:     /// assert!(!(..=1.0).contains(&f32::NAN));\n   637:     /// assert!(!(..=f32::NAN).contains(&0.5));\n   638:     /// ```\n   639:     #[inline]\n   640:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   641:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   642:     pub const fn contains<U>(&self, item: &U) -> bool\n   643:     where\n   644:         Idx: [const] PartialOrd<U>,\n   645:         U: ?Sized + [const] PartialOrd<Idx>,\n   646:     {\n   647:         <Self as RangeBounds<Idx>>::contains(self, item)\n   648:     }\n   649: }\n   650: \n   651: // RangeToInclusive<Idx> cannot impl From<RangeTo<Idx>>\n   652: // because underflow would be possible with (..0).into()\n   653: \n   654: /// An endpoint of a range of keys.\n   655: ///\n   656: /// # Examples\n   657: ///\n   658: /// `Bound`s are range endpoints:",
    "nanvix_source": "   632:     /// assert!( (..=5).contains(&5));\n   633:     /// assert!(!(..=5).contains(&6));\n   634:     ///\n   635:     /// assert!( (..=1.0).contains(&1.0));\n   636:     /// assert!(!(..=1.0).contains(&f32::NAN));\n   637:     /// assert!(!(..=f32::NAN).contains(&0.5));\n   638:     /// ```\n   639:     #[inline]\n   640:     #[stable(feature = \"range_contains\", since = \"1.35.0\")]\n   641:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   642:     pub const fn contains<U>(&self, item: &U) -> bool\n   643:     where\n   644:         Idx: [const] PartialOrd<U>,\n   645:         U: ?Sized + [const] PartialOrd<Idx>,\n   646:     {\n   647:         <Self as RangeBounds<Idx>>::contains(self, item)\n   648:     }\n   649: }\n   650: \n   651: // RangeToInclusive<Idx> cannot impl From<RangeTo<Idx>>\n   652: // because underflow would be possible with (..0).into()",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::panic::Location::caller",
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
      "name": "caller",
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
            "id": 8274,
            "path": "Location"
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
        "impl_id": "core:28189",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8274",
        "resolved_owner_path": [
          "core",
          "panic",
          "location",
          "Location"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'static",
            "type": {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'static"
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 8274,
                "path": "Location"
              }
            }
          }
        }
      }
    },
    "verification_source": "   164:     ///     // 64 |     let yet_another_location = new_location();\n   165:     ///     //    |                                ^ `let yet_another_location` points here\n   166:     ///     // 65 |     assert_eq!(here.file(), yet_another_location.file());\n   167:     ///     let yet_another_location = new_location();\n   168:     ///     assert_eq!(here.file(), yet_another_location.file());\n   169:     ///     assert_ne!(\n   170:     ///         (here.line(), here.column()),\n   171:     ///         (yet_another_location.line(), yet_another_location.column())\n   172:     ///     );\n   173:     /// }\n   174:     /// ```\n   175:     #[must_use]\n   176:     #[stable(feature = \"track_caller\", since = \"1.46.0\")]\n   177:     #[rustc_const_stable(feature = \"const_caller_location\", since = \"1.79.0\")]\n   178:     #[track_caller]\n   179:     #[inline]\n   180:     pub const fn caller() -> &'static Location<'static> {\n   181:         crate::intrinsics::caller_location()\n   182:     }\n   183: \n   184:     /// Returns the name of the source file from which the panic originated.\n   185:     ///\n   186:     /// # `&str`, not `&Path`\n   187:     ///\n   188:     /// The returned name refers to a source path on the compiling system, but it isn't valid to\n   189:     /// represent this directly as a `&Path`. The compiled code may run on a different system with\n   190:     /// a different `Path` implementation than the system providing the contents and this library\n   191:     /// does not currently have a different \"host path\" type.\n   192:     ///\n   193:     /// The most surprising behavior occurs when \"the same\" file is reachable via multiple paths in\n   194:     /// the module system (usually using the `#[path = \"...\"]` attribute or similar), which can\n   195:     /// cause what appears to be identical code to return differing values from this function.\n   196:     ///",
    "nanvix_source": "   170:     ///         (here.line(), here.column()),\n   171:     ///         (yet_another_location.line(), yet_another_location.column())\n   172:     ///     );\n   173:     /// }\n   174:     /// ```\n   175:     #[must_use]\n   176:     #[stable(feature = \"track_caller\", since = \"1.46.0\")]\n   177:     #[rustc_const_stable(feature = \"const_caller_location\", since = \"1.79.0\")]\n   178:     #[track_caller]\n   179:     #[inline]\n   180:     pub const fn caller() -> &'static Location<'static> {\n   181:         crate::intrinsics::caller_location()\n   182:     }\n   183: \n   184:     /// Returns the name of the source file from which the panic originated.\n   185:     ///\n   186:     /// # `&str`, not `&Path`\n   187:     ///\n   188:     /// The returned name refers to a source path on the compiling system, but it isn't valid to\n   189:     /// represent this directly as a `&Path`. The compiled code may run on a different system with\n   190:     /// a different `Path` implementation than the system providing the contents and this library",
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
