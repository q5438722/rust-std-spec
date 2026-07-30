For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::Bound::as_ref",
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9759,
            "path": "Bound"
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
        "impl_id": "core:24011",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9759",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "Bound"
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
                          "generic": "T"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9759,
            "path": "Bound"
          }
        }
      }
    },
    "verification_source": "   693:     /// An inclusive bound.\n   694:     #[stable(feature = \"collections_bound\", since = \"1.17.0\")]\n   695:     Included(#[stable(feature = \"collections_bound\", since = \"1.17.0\")] T),\n   696:     /// An exclusive bound.\n   697:     #[stable(feature = \"collections_bound\", since = \"1.17.0\")]\n   698:     Excluded(#[stable(feature = \"collections_bound\", since = \"1.17.0\")] T),\n   699:     /// An infinite endpoint. Indicates that there is no bound in this direction.\n   700:     #[stable(feature = \"collections_bound\", since = \"1.17.0\")]\n   701:     Unbounded,\n   702: }\n   703: \n   704: impl<T> Bound<T> {\n   705:     /// Converts from `&Bound<T>` to `Bound<&T>`.\n   706:     #[inline]\n   707:     #[stable(feature = \"bound_as_ref_shared\", since = \"1.65.0\")]\n   708:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   709:     pub const fn as_ref(&self) -> Bound<&T> {\n   710:         match *self {\n   711:             Included(ref x) => Included(x),\n   712:             Excluded(ref x) => Excluded(x),\n   713:             Unbounded => Unbounded,\n   714:         }\n   715:     }\n   716: \n   717:     /// Converts from `&mut Bound<T>` to `Bound<&mut T>`.\n   718:     #[inline]\n   719:     #[unstable(feature = \"bound_as_ref\", issue = \"80996\")]\n   720:     pub const fn as_mut(&mut self) -> Bound<&mut T> {\n   721:         match *self {\n   722:             Included(ref mut x) => Included(x),\n   723:             Excluded(ref mut x) => Excluded(x),\n   724:             Unbounded => Unbounded,\n   725:         }",
    "nanvix_source": "   699:     /// An infinite endpoint. Indicates that there is no bound in this direction.\n   700:     #[stable(feature = \"collections_bound\", since = \"1.17.0\")]\n   701:     Unbounded,\n   702: }\n   703: \n   704: impl<T> Bound<T> {\n   705:     /// Converts from `&Bound<T>` to `Bound<&T>`.\n   706:     #[inline]\n   707:     #[stable(feature = \"bound_as_ref_shared\", since = \"1.65.0\")]\n   708:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   709:     pub const fn as_ref(&self) -> Bound<&T> {\n   710:         match *self {\n   711:             Included(ref x) => Included(x),\n   712:             Excluded(ref x) => Excluded(x),\n   713:             Unbounded => Unbounded,\n   714:         }\n   715:     }\n   716: \n   717:     /// Converts from `&mut Bound<T>` to `Bound<&mut T>`.\n   718:     #[inline]\n   719:     #[unstable(feature = \"bound_as_ref\", issue = \"80996\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::Bound::cloned",
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
                      "id": 42,
                      "path": "Clone"
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
      "name": "cloned",
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
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
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
            "id": 9759,
            "path": "Bound"
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
                          "id": 42,
                          "path": "Clone"
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
        "impl_id": "core:24015",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9759",
        "resolved_owner_path": [
          "core",
          "ops",
          "range",
          "Bound"
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9759,
            "path": "Bound"
          }
        }
      }
    },
    "verification_source": "   787:     ///\n   788:     /// # Examples\n   789:     ///\n   790:     /// ```\n   791:     /// use std::ops::Bound::*;\n   792:     /// use std::ops::RangeBounds;\n   793:     ///\n   794:     /// let a1 = String::from(\"a\");\n   795:     /// let (a2, a3, a4) = (a1.clone(), a1.clone(), a1.clone());\n   796:     ///\n   797:     /// assert_eq!(Included(&a1), (a2..).start_bound());\n   798:     /// assert_eq!(Included(a3), (a4..).start_bound().cloned());\n   799:     /// ```\n   800:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   801:     #[stable(feature = \"bound_cloned\", since = \"1.55.0\")]\n   802:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   803:     pub const fn cloned(self) -> Bound<T>\n   804:     where\n   805:         T: [const] Clone,\n   806:     {\n   807:         match self {\n   808:             Bound::Unbounded => Bound::Unbounded,\n   809:             Bound::Included(x) => Bound::Included(x.clone()),\n   810:             Bound::Excluded(x) => Bound::Excluded(x.clone()),\n   811:         }\n   812:     }\n   813: }\n   814: \n   815: /// `RangeBounds` is implemented by Rust's built-in range types, produced\n   816: /// by range syntax like `..`, `a..`, `..b`, `..=c`, `d..e`, or `f..=g`.\n   817: #[stable(feature = \"collections_range\", since = \"1.28.0\")]\n   818: #[rustc_diagnostic_item = \"RangeBounds\"]\n   819: #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]",
    "nanvix_source": "   793:     ///\n   794:     /// let a1 = String::from(\"a\");\n   795:     /// let (a2, a3, a4) = (a1.clone(), a1.clone(), a1.clone());\n   796:     ///\n   797:     /// assert_eq!(Included(&a1), (a2..).start_bound());\n   798:     /// assert_eq!(Included(a3), (a4..).start_bound().cloned());\n   799:     /// ```\n   800:     #[must_use = \"`self` will be dropped if the result is not used\"]\n   801:     #[stable(feature = \"bound_cloned\", since = \"1.55.0\")]\n   802:     #[rustc_const_unstable(feature = \"const_range\", issue = \"none\")]\n   803:     pub const fn cloned(self) -> Bound<T>\n   804:     where\n   805:         T: [const] Clone,\n   806:     {\n   807:         match self {\n   808:             Bound::Unbounded => Bound::Unbounded,\n   809:             Bound::Included(x) => Bound::Included(x.clone()),\n   810:             Bound::Excluded(x) => Bound::Excluded(x.clone()),\n   811:         }\n   812:     }\n   813: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::break_ok",
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
      "name": "break_ok",
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   251:     ///     value: 0,\n   252:     ///     left: TreeNode::leaf(1),\n   253:     ///     right: Some(Box::new(TreeNode {\n   254:     ///         value: -1,\n   255:     ///         left: TreeNode::leaf(5),\n   256:     ///         right: TreeNode::leaf(2),\n   257:     ///     })),\n   258:     /// };\n   259:     ///\n   260:     /// let res = node.find(|val: &i32| *val > 3);\n   261:     /// assert_eq!(res, Ok(&5));\n   262:     /// ```\n   263:     #[inline]\n   264:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   265:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   266:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   267:     pub const fn break_ok(self) -> Result<B, C> {\n   268:         match self {\n   269:             ControlFlow::Continue(c) => Err(c),\n   270:             ControlFlow::Break(b) => Ok(b),\n   271:         }\n   272:     }\n   273: \n   274:     /// Maps `ControlFlow<B, C>` to `ControlFlow<T, C>` by applying a function\n   275:     /// to the break value in case it exists.\n   276:     #[inline]\n   277:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   278:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   279:     pub const fn map_break<T, F>(self, f: F) -> ControlFlow<T, C>\n   280:     where\n   281:         F: [const] FnOnce(B) -> T + [const] Destruct,\n   282:     {\n   283:         match self {",
    "nanvix_source": "   258:     ///     })),\n   259:     /// };\n   260:     ///\n   261:     /// let res = node.find(|val: &i32| *val > 3);\n   262:     /// assert_eq!(res, Ok(&5));\n   263:     /// ```\n   264:     #[inline]\n   265:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   266:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   267:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   268:     pub const fn break_ok(self) -> Result<B, C> {\n   269:         match self {\n   270:             ControlFlow::Continue(c) => Err(c),\n   271:             ControlFlow::Break(b) => Ok(b),\n   272:         }\n   273:     }\n   274: \n   275:     /// Maps `ControlFlow<B, C>` to `ControlFlow<T, C>` by applying a function\n   276:     /// to the break value in case it exists.\n   277:     #[inline]\n   278:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::break_value",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "break_value",
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
                      "generic": "B"
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
    "verification_source": "   174:     }\n   175: \n   176:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the\n   177:     /// `ControlFlow` was `Break` and `None` otherwise.\n   178:     ///\n   179:     /// # Examples\n   180:     ///\n   181:     /// ```\n   182:     /// use std::ops::ControlFlow;\n   183:     ///\n   184:     /// assert_eq!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").break_value(), Some(\"Stop right there!\"));\n   185:     /// assert_eq!(ControlFlow::<&str, i32>::Continue(3).break_value(), None);\n   186:     /// ```\n   187:     #[inline]\n   188:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   189:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   190:     pub const fn break_value(self) -> Option<B>\n   191:     where\n   192:         Self: [const] Destruct,\n   193:     {\n   194:         match self {\n   195:             ControlFlow::Continue(..) => None,\n   196:             ControlFlow::Break(x) => Some(x),\n   197:         }\n   198:     }\n   199: \n   200:     /// Converts the `ControlFlow` into a `Result` which is `Ok` if the\n   201:     /// `ControlFlow` was `Break` and `Err` if otherwise.\n   202:     ///\n   203:     /// # Examples\n   204:     ///\n   205:     /// ```\n   206:     /// use std::ops::ControlFlow;",
    "nanvix_source": "   181:     ///\n   182:     /// ```\n   183:     /// use std::ops::ControlFlow;\n   184:     ///\n   185:     /// assert_eq!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").break_value(), Some(\"Stop right there!\"));\n   186:     /// assert_eq!(ControlFlow::<&str, i32>::Continue(3).break_value(), None);\n   187:     /// ```\n   188:     #[inline]\n   189:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   190:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   191:     pub const fn break_value(self) -> Option<B>\n   192:     where\n   193:         Self: [const] Destruct,\n   194:     {\n   195:         match self {\n   196:             ControlFlow::Continue(..) => None,\n   197:             ControlFlow::Break(x) => Some(x),\n   198:         }\n   199:     }\n   200: \n   201:     /// Converts the `ControlFlow` into a `Result` which is `Ok` if the",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::continue_ok",
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
      "name": "continue_ok",
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
                      "generic": "C"
                    }
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
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   363:     ///     if *val < 0 {\n   364:     ///         return ControlFlow::Break(\"negative value detected\");\n   365:     ///     }\n   366:     ///\n   367:     ///     if *val > 4 {\n   368:     ///         return ControlFlow::Break(\"too big value detected\");\n   369:     ///     }\n   370:     ///\n   371:     ///     ControlFlow::Continue(())\n   372:     /// });\n   373:     /// assert_eq!(res, Err(\"too big value detected\"));\n   374:     /// ```\n   375:     #[inline]\n   376:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   377:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   378:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   379:     pub const fn continue_ok(self) -> Result<C, B> {\n   380:         match self {\n   381:             ControlFlow::Continue(c) => Ok(c),\n   382:             ControlFlow::Break(b) => Err(b),\n   383:         }\n   384:     }\n   385: \n   386:     /// Maps `ControlFlow<B, C>` to `ControlFlow<B, T>` by applying a function\n   387:     /// to the continue value in case it exists.\n   388:     #[inline]\n   389:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   390:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   391:     pub const fn map_continue<T, F>(self, f: F) -> ControlFlow<B, T>\n   392:     where\n   393:         F: [const] FnOnce(C) -> T + [const] Destruct,\n   394:     {\n   395:         match self {",
    "nanvix_source": "   370:     ///     }\n   371:     ///\n   372:     ///     ControlFlow::Continue(())\n   373:     /// });\n   374:     /// assert_eq!(res, Err(\"too big value detected\"));\n   375:     /// ```\n   376:     #[inline]\n   377:     #[stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   378:     #[rustc_const_stable(feature = \"control_flow_ok\", since = \"1.96.0\")]\n   379:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n   380:     pub const fn continue_ok(self) -> Result<C, B> {\n   381:         match self {\n   382:             ControlFlow::Continue(c) => Ok(c),\n   383:             ControlFlow::Break(b) => Err(b),\n   384:         }\n   385:     }\n   386: \n   387:     /// Maps `ControlFlow<B, C>` to `ControlFlow<B, T>` by applying a function\n   388:     /// to the continue value in case it exists.\n   389:     #[inline]\n   390:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::ControlFlow::continue_value",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "continue_value",
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
                      "generic": "C"
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
    "verification_source": "   287:     }\n   288: \n   289:     /// Converts the `ControlFlow` into an `Option` which is `Some` if the\n   290:     /// `ControlFlow` was `Continue` and `None` otherwise.\n   291:     ///\n   292:     /// # Examples\n   293:     ///\n   294:     /// ```\n   295:     /// use std::ops::ControlFlow;\n   296:     ///\n   297:     /// assert_eq!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").continue_value(), None);\n   298:     /// assert_eq!(ControlFlow::<&str, i32>::Continue(3).continue_value(), Some(3));\n   299:     /// ```\n   300:     #[inline]\n   301:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   302:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   303:     pub const fn continue_value(self) -> Option<C>\n   304:     where\n   305:         Self: [const] Destruct,\n   306:     {\n   307:         match self {\n   308:             ControlFlow::Continue(x) => Some(x),\n   309:             ControlFlow::Break(..) => None,\n   310:         }\n   311:     }\n   312: \n   313:     /// Converts the `ControlFlow` into a `Result` which is `Ok` if the\n   314:     /// `ControlFlow` was `Continue` and `Err` if otherwise.\n   315:     ///\n   316:     /// # Examples\n   317:     ///\n   318:     /// ```\n   319:     /// use std::ops::ControlFlow;",
    "nanvix_source": "   294:     ///\n   295:     /// ```\n   296:     /// use std::ops::ControlFlow;\n   297:     ///\n   298:     /// assert_eq!(ControlFlow::<&str, i32>::Break(\"Stop right there!\").continue_value(), None);\n   299:     /// assert_eq!(ControlFlow::<&str, i32>::Continue(3).continue_value(), Some(3));\n   300:     /// ```\n   301:     #[inline]\n   302:     #[stable(feature = \"control_flow_enum\", since = \"1.83.0\")]\n   303:     #[rustc_const_unstable(feature = \"const_control_flow\", issue = \"148739\")]\n   304:     pub const fn continue_value(self) -> Option<C>\n   305:     where\n   306:         Self: [const] Destruct,\n   307:     {\n   308:         match self {\n   309:             ControlFlow::Continue(x) => Some(x),\n   310:             ControlFlow::Break(..) => None,\n   311:         }\n   312:     }\n   313: \n   314:     /// Converts the `ControlFlow` into a `Result` which is `Ok` if the",
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
