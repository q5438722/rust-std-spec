For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::iter::Iterator::is_sorted",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
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
      "name": "is_sorted",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4037:     /// Note that if `Self::Item` is only `PartialOrd`, but not `Ord`, the above definition\n  4038:     /// implies that this function returns `false` if any two consecutive items are not\n  4039:     /// comparable.\n  4040:     ///\n  4041:     /// # Examples\n  4042:     ///\n  4043:     /// ```\n  4044:     /// assert!([1, 2, 2, 9].iter().is_sorted());\n  4045:     /// assert!(![1, 3, 2, 4].iter().is_sorted());\n  4046:     /// assert!([0].iter().is_sorted());\n  4047:     /// assert!(std::iter::empty::<i32>().is_sorted());\n  4048:     /// assert!(![0.0, 1.0, f32::NAN].iter().is_sorted());\n  4049:     /// ```\n  4050:     #[inline]\n  4051:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4052:     #[rustc_non_const_trait_method]\n  4053:     fn is_sorted(self) -> bool\n  4054:     where\n  4055:         Self: Sized,\n  4056:         Self::Item: PartialOrd,\n  4057:     {\n  4058:         self.is_sorted_by(|a, b| a <= b)\n  4059:     }\n  4060: \n  4061:     /// Checks if the elements of this iterator are sorted using the given comparator function.\n  4062:     ///\n  4063:     /// Instead of using `PartialOrd::partial_cmp`, this function uses the given `compare`\n  4064:     /// function to determine whether two elements are to be considered in sorted order.\n  4065:     ///\n  4066:     /// # Examples\n  4067:     ///\n  4068:     /// ```\n  4069:     /// assert!([1, 2, 2, 9].iter().is_sorted_by(|a, b| a <= b));",
    "nanvix_source": "  4041:     /// ```\n  4042:     /// assert!([1, 2, 2, 9].iter().is_sorted());\n  4043:     /// assert!(![1, 3, 2, 4].iter().is_sorted());\n  4044:     /// assert!([0].iter().is_sorted());\n  4045:     /// assert!(std::iter::empty::<i32>().is_sorted());\n  4046:     /// assert!(![0.0, 1.0, f32::NAN].iter().is_sorted());\n  4047:     /// ```\n  4048:     #[inline]\n  4049:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4050:     #[rustc_non_const_trait_method]\n  4051:     fn is_sorted(self) -> bool\n  4052:     where\n  4053:         Self: Sized,\n  4054:         Self::Item: PartialOrd,\n  4055:     {\n  4056:         self.is_sorted_by(|a, b| a <= b)\n  4057:     }\n  4058: \n  4059:     /// Checks if the elements of this iterator are sorted using the given comparator function.\n  4060:     ///\n  4061:     /// Instead of using `PartialOrd::partial_cmp`, this function uses the given `compare`",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::is_sorted_by",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "F"
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "qualified_path": {
                                    "args": null,
                                    "name": "Item",
                                    "self_type": {
                                      "generic": "Self"
                                    },
                                    "trait": {
                                      "args": null,
                                      "id": 82,
                                      "path": ""
                                    }
                                  }
                                }
                              }
                            },
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "qualified_path": {
                                    "args": null,
                                    "name": "Item",
                                    "self_type": {
                                      "generic": "Self"
                                    },
                                    "trait": {
                                      "args": null,
                                      "id": 82,
                                      "path": ""
                                    }
                                  }
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
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
      "name": "is_sorted_by",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "compare",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4064:     /// function to determine whether two elements are to be considered in sorted order.\n  4065:     ///\n  4066:     /// # Examples\n  4067:     ///\n  4068:     /// ```\n  4069:     /// assert!([1, 2, 2, 9].iter().is_sorted_by(|a, b| a <= b));\n  4070:     /// assert!(![1, 2, 2, 9].iter().is_sorted_by(|a, b| a < b));\n  4071:     ///\n  4072:     /// assert!([0].iter().is_sorted_by(|a, b| true));\n  4073:     /// assert!([0].iter().is_sorted_by(|a, b| false));\n  4074:     ///\n  4075:     /// assert!(std::iter::empty::<i32>().is_sorted_by(|a, b| false));\n  4076:     /// assert!(std::iter::empty::<i32>().is_sorted_by(|a, b| true));\n  4077:     /// ```\n  4078:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4079:     #[rustc_non_const_trait_method]\n  4080:     fn is_sorted_by<F>(mut self, compare: F) -> bool\n  4081:     where\n  4082:         Self: Sized,\n  4083:         F: FnMut(&Self::Item, &Self::Item) -> bool,\n  4084:     {\n  4085:         #[inline]\n  4086:         fn check<'a, T>(\n  4087:             last: &'a mut T,\n  4088:             mut compare: impl FnMut(&T, &T) -> bool + 'a,\n  4089:         ) -> impl FnMut(T) -> bool + 'a {\n  4090:             move |curr| {\n  4091:                 if !compare(&last, &curr) {\n  4092:                     return false;\n  4093:                 }\n  4094:                 *last = curr;\n  4095:                 true\n  4096:             }",
    "nanvix_source": "  4068:     /// assert!(![1, 2, 2, 9].iter().is_sorted_by(|a, b| a < b));\n  4069:     ///\n  4070:     /// assert!([0].iter().is_sorted_by(|a, b| true));\n  4071:     /// assert!([0].iter().is_sorted_by(|a, b| false));\n  4072:     ///\n  4073:     /// assert!(std::iter::empty::<i32>().is_sorted_by(|a, b| false));\n  4074:     /// assert!(std::iter::empty::<i32>().is_sorted_by(|a, b| true));\n  4075:     /// ```\n  4076:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4077:     #[rustc_non_const_trait_method]\n  4078:     fn is_sorted_by<F>(mut self, compare: F) -> bool\n  4079:     where\n  4080:         Self: Sized,\n  4081:         F: FnMut(&Self::Item, &Self::Item) -> bool,\n  4082:     {\n  4083:         #[inline]\n  4084:         fn check<'a, T>(\n  4085:             last: &'a mut T,\n  4086:             mut compare: impl FnMut(&T, &T) -> bool + 'a,\n  4087:         ) -> impl FnMut(T) -> bool + 'a {\n  4088:             move |curr| {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::is_sorted_by_key",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "F"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "K"
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
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "qualified_path": {
                                "args": null,
                                "name": "Item",
                                "self_type": {
                                  "generic": "Self"
                                },
                                "trait": {
                                  "args": null,
                                  "id": 82,
                                  "path": ""
                                }
                              }
                            }
                          ],
                          "output": {
                            "generic": "K"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "F"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 58,
                      "path": "PartialOrd"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
      "name": "is_sorted_by_key",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "f",
            {
              "generic": "F"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  4109:     ///\n  4110:     /// Instead of comparing the iterator's elements directly, this function compares the keys of\n  4111:     /// the elements, as determined by `f`. Apart from that, it's equivalent to [`is_sorted`]; see\n  4112:     /// its documentation for more information.\n  4113:     ///\n  4114:     /// [`is_sorted`]: Iterator::is_sorted\n  4115:     ///\n  4116:     /// # Examples\n  4117:     ///\n  4118:     /// ```\n  4119:     /// assert!([\"c\", \"bb\", \"aaa\"].iter().is_sorted_by_key(|s| s.len()));\n  4120:     /// assert!(![-2i32, -1, 0, 3].iter().is_sorted_by_key(|n| n.abs()));\n  4121:     /// ```\n  4122:     #[inline]\n  4123:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4124:     #[rustc_non_const_trait_method]\n  4125:     fn is_sorted_by_key<F, K>(self, f: F) -> bool\n  4126:     where\n  4127:         Self: Sized,\n  4128:         F: FnMut(Self::Item) -> K,\n  4129:         K: PartialOrd,\n  4130:     {\n  4131:         self.map(f).is_sorted()\n  4132:     }\n  4133: \n  4134:     /// See [TrustedRandomAccess][super::super::TrustedRandomAccess]\n  4135:     // The unusual name is to avoid name collisions in method resolution\n  4136:     // see #76479.\n  4137:     #[inline]\n  4138:     #[doc(hidden)]\n  4139:     #[unstable(feature = \"trusted_random_access\", issue = \"none\")]\n  4140:     #[rustc_non_const_trait_method]\n  4141:     unsafe fn __iterator_get_unchecked(&mut self, _idx: usize) -> Self::Item",
    "nanvix_source": "  4113:     ///\n  4114:     /// # Examples\n  4115:     ///\n  4116:     /// ```\n  4117:     /// assert!([\"c\", \"bb\", \"aaa\"].iter().is_sorted_by_key(|s| s.len()));\n  4118:     /// assert!(![-2i32, -1, 0, 3].iter().is_sorted_by_key(|n| n.abs()));\n  4119:     /// ```\n  4120:     #[inline]\n  4121:     #[stable(feature = \"is_sorted\", since = \"1.82.0\")]\n  4122:     #[rustc_non_const_trait_method]\n  4123:     fn is_sorted_by_key<F, K>(self, f: F) -> bool\n  4124:     where\n  4125:         Self: Sized,\n  4126:         F: FnMut(Self::Item) -> K,\n  4127:         K: PartialOrd,\n  4128:     {\n  4129:         self.map(f).is_sorted()\n  4130:     }\n  4131: \n  4132:     /// See [TrustedRandomAccess][super::super::TrustedRandomAccess]\n  4133:     // The unusual name is to avoid name collisions in method resolution",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::last",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
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
      "name": "last",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
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
                      "qualified_path": {
                        "args": null,
                        "name": "Item",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": ""
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
    "verification_source": "   243:     ///\n   244:     /// # Panics\n   245:     ///\n   246:     /// This function might panic if the iterator is infinite.\n   247:     ///\n   248:     /// # Examples\n   249:     ///\n   250:     /// ```\n   251:     /// let a = [1, 2, 3];\n   252:     /// assert_eq!(a.into_iter().last(), Some(3));\n   253:     ///\n   254:     /// let a = [1, 2, 3, 4, 5];\n   255:     /// assert_eq!(a.into_iter().last(), Some(5));\n   256:     /// ```\n   257:     #[inline]\n   258:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   259:     fn last(self) -> Option<Self::Item>\n   260:     where\n   261:         Self: Sized + [const] Destruct,\n   262:         Self::Item: [const] Destruct,\n   263:     {\n   264:         #[inline]\n   265:         #[rustc_const_unstable(feature = \"const_destruct\", issue = \"133214\")]\n   266:         const fn some<T>(_: Option<T>, x: T) -> Option<T>\n   267:         where\n   268:             T: [const] Destruct,\n   269:         {\n   270:             Some(x)\n   271:         }\n   272: \n   273:         self.fold(None, some)\n   274:     }\n   275: ",
    "nanvix_source": "   247:     ///\n   248:     /// ```\n   249:     /// let a = [1, 2, 3];\n   250:     /// assert_eq!(a.into_iter().last(), Some(3));\n   251:     ///\n   252:     /// let a = [1, 2, 3, 4, 5];\n   253:     /// assert_eq!(a.into_iter().last(), Some(5));\n   254:     /// ```\n   255:     #[inline]\n   256:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   257:     fn last(self) -> Option<Self::Item>\n   258:     where\n   259:         Self: Sized + [const] Destruct,\n   260:         Self::Item: [const] Destruct,\n   261:     {\n   262:         #[inline]\n   263:         #[rustc_const_unstable(feature = \"const_destruct\", issue = \"133214\")]\n   264:         const fn some<T>(_: Option<T>, x: T) -> Option<T>\n   265:         where\n   266:             T: [const] Destruct,\n   267:         {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::le",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "I"
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
                      "args": null,
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
              }
            }
          },
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
                              "type": {
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
                                  },
                                  "trait": {
                                    "args": null,
                                    "id": 80,
                                    "path": ""
                                  }
                                }
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
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
                    "path": ""
                  }
                }
              }
            }
          },
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
                "generic": "Self"
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
      "name": "le",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "other",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  3963:         self.partial_cmp(other) == Some(Ordering::Less)\n  3964:     }\n  3965: \n  3966:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3967:     /// less or equal to those of another.\n  3968:     ///\n  3969:     /// # Examples\n  3970:     ///\n  3971:     /// ```\n  3972:     /// assert_eq!([1].iter().le([1].iter()), true);\n  3973:     /// assert_eq!([1].iter().le([1, 2].iter()), true);\n  3974:     /// assert_eq!([1, 2].iter().le([1].iter()), false);\n  3975:     /// assert_eq!([1, 2].iter().le([1, 2].iter()), true);\n  3976:     /// ```\n  3977:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3978:     #[rustc_non_const_trait_method]\n  3979:     fn le<I>(self, other: I) -> bool\n  3980:     where\n  3981:         I: IntoIterator,\n  3982:         Self::Item: PartialOrd<I::Item>,\n  3983:         Self: Sized,\n  3984:     {\n  3985:         matches!(self.partial_cmp(other), Some(Ordering::Less | Ordering::Equal))\n  3986:     }\n  3987: \n  3988:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3989:     /// greater than those of another.\n  3990:     ///\n  3991:     /// # Examples\n  3992:     ///\n  3993:     /// ```\n  3994:     /// assert_eq!([1].iter().gt([1].iter()), false);\n  3995:     /// assert_eq!([1].iter().gt([1, 2].iter()), false);",
    "nanvix_source": "  3967:     /// # Examples\n  3968:     ///\n  3969:     /// ```\n  3970:     /// assert_eq!([1].iter().le([1].iter()), true);\n  3971:     /// assert_eq!([1].iter().le([1, 2].iter()), true);\n  3972:     /// assert_eq!([1, 2].iter().le([1].iter()), false);\n  3973:     /// assert_eq!([1, 2].iter().le([1, 2].iter()), true);\n  3974:     /// ```\n  3975:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3976:     #[rustc_non_const_trait_method]\n  3977:     fn le<I>(self, other: I) -> bool\n  3978:     where\n  3979:         I: IntoIterator,\n  3980:         Self::Item: PartialOrd<I::Item>,\n  3981:         Self: Sized,\n  3982:     {\n  3983:         matches!(self.partial_cmp(other), Some(Ordering::Less | Ordering::Equal))\n  3984:     }\n  3985: \n  3986:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3987:     /// greater than those of another.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::Iterator::lt",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
            "name": "I"
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
                      "args": null,
                      "id": 80,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
              }
            }
          },
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
                              "type": {
                                "qualified_path": {
                                  "args": null,
                                  "name": "Item",
                                  "self_type": {
                                    "generic": "I"
                                  },
                                  "trait": {
                                    "args": null,
                                    "id": 80,
                                    "path": ""
                                  }
                                }
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
                "qualified_path": {
                  "args": null,
                  "name": "Item",
                  "self_type": {
                    "generic": "Self"
                  },
                  "trait": {
                    "args": null,
                    "id": 82,
                    "path": ""
                  }
                }
              }
            }
          },
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
                "generic": "Self"
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
      "name": "lt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:82",
        "kind": "trait",
        "name": "Iterator",
        "path": [
          "core",
          "iter",
          "traits",
          "iterator",
          "Iterator"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "other",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  3941:         !self.eq(other)\n  3942:     }\n  3943: \n  3944:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3945:     /// less than those of another.\n  3946:     ///\n  3947:     /// # Examples\n  3948:     ///\n  3949:     /// ```\n  3950:     /// assert_eq!([1].iter().lt([1].iter()), false);\n  3951:     /// assert_eq!([1].iter().lt([1, 2].iter()), true);\n  3952:     /// assert_eq!([1, 2].iter().lt([1].iter()), false);\n  3953:     /// assert_eq!([1, 2].iter().lt([1, 2].iter()), false);\n  3954:     /// ```\n  3955:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3956:     #[rustc_non_const_trait_method]\n  3957:     fn lt<I>(self, other: I) -> bool\n  3958:     where\n  3959:         I: IntoIterator,\n  3960:         Self::Item: PartialOrd<I::Item>,\n  3961:         Self: Sized,\n  3962:     {\n  3963:         self.partial_cmp(other) == Some(Ordering::Less)\n  3964:     }\n  3965: \n  3966:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3967:     /// less or equal to those of another.\n  3968:     ///\n  3969:     /// # Examples\n  3970:     ///\n  3971:     /// ```\n  3972:     /// assert_eq!([1].iter().le([1].iter()), true);\n  3973:     /// assert_eq!([1].iter().le([1, 2].iter()), true);",
    "nanvix_source": "  3945:     /// # Examples\n  3946:     ///\n  3947:     /// ```\n  3948:     /// assert_eq!([1].iter().lt([1].iter()), false);\n  3949:     /// assert_eq!([1].iter().lt([1, 2].iter()), true);\n  3950:     /// assert_eq!([1, 2].iter().lt([1].iter()), false);\n  3951:     /// assert_eq!([1, 2].iter().lt([1, 2].iter()), false);\n  3952:     /// ```\n  3953:     #[stable(feature = \"iter_order\", since = \"1.5.0\")]\n  3954:     #[rustc_non_const_trait_method]\n  3955:     fn lt<I>(self, other: I) -> bool\n  3956:     where\n  3957:         I: IntoIterator,\n  3958:         Self::Item: PartialOrd<I::Item>,\n  3959:         Self: Sized,\n  3960:     {\n  3961:         self.partial_cmp(other) == Some(Ordering::Less)\n  3962:     }\n  3963: \n  3964:     /// Determines if the elements of this [`Iterator`] are [lexicographically](Ord#lexicographical-comparison)\n  3965:     /// less or equal to those of another.",
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
