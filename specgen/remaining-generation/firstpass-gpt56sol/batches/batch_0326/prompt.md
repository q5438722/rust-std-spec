For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::copy_from_nonoverlapping",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
    ],
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
                      "id": 12,
                      "path": "Sized"
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
        "is_unsafe": true
      },
      "name": "copy_from_nonoverlapping",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
          ],
          [
            "src",
            {
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
                "id": 9475,
                "path": "NonNull"
              }
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1090:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1091:         unsafe { ptr::copy(src.as_ptr(), self.as_ptr(), count) }\n  1092:     }\n  1093: \n  1094:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1095:     /// and destination may *not* overlap.\n  1096:     ///\n  1097:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1098:     ///\n  1099:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1100:     ///\n  1101:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1102:     #[inline(always)]\n  1103:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1104:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1105:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1106:     pub const unsafe fn copy_from_nonoverlapping(self, src: NonNull<T>, count: usize)\n  1107:     where\n  1108:         T: Sized,\n  1109:     {\n  1110:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1111:         unsafe { ptr::copy_nonoverlapping(src.as_ptr(), self.as_ptr(), count) }\n  1112:     }\n  1113: \n  1114:     /// Executes the destructor (if any) of the pointed-to value.\n  1115:     ///\n  1116:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1117:     ///\n  1118:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1119:     #[inline(always)]\n  1120:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1121:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1122:     pub const unsafe fn drop_in_place(self)",
    "nanvix_source": "  1029:     ///\n  1030:     /// NOTE: this has the *opposite* argument order of [`ptr::copy_nonoverlapping`].\n  1031:     ///\n  1032:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1033:     ///\n  1034:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1035:     #[inline(always)]\n  1036:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1037:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1038:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1039:     pub const unsafe fn copy_from_nonoverlapping(self, src: NonNull<T>, count: usize)\n  1040:     where\n  1041:         T: Sized,\n  1042:     {\n  1043:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1044:         unsafe { ptr::copy_nonoverlapping(src.as_ptr(), self.as_ptr(), count) }\n  1045:     }\n  1046: \n  1047:     /// Executes the destructor (if any) of the pointed-to value.\n  1048:     ///\n  1049:     /// See [`ptr::drop_in_place`] for safety concerns and examples.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::copy_to",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
    ],
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
                      "id": 12,
                      "path": "Sized"
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
        "is_unsafe": true
      },
      "name": "copy_to",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
          ],
          [
            "dest",
            {
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
                "id": 9475,
                "path": "NonNull"
              }
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1030:         // SAFETY: the caller must uphold the safety contract for `read_unaligned`.\n  1031:         unsafe { ptr::read_unaligned(self.as_ptr()) }\n  1032:     }\n  1033: \n  1034:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1035:     /// and destination may overlap.\n  1036:     ///\n  1037:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n  1038:     ///\n  1039:     /// See [`ptr::copy`] for safety concerns and examples.\n  1040:     ///\n  1041:     /// [`ptr::copy`]: crate::ptr::copy()\n  1042:     #[inline(always)]\n  1043:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1044:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1045:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1046:     pub const unsafe fn copy_to(self, dest: NonNull<T>, count: usize)\n  1047:     where\n  1048:         T: Sized,\n  1049:     {\n  1050:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1051:         unsafe { ptr::copy(self.as_ptr(), dest.as_ptr(), count) }\n  1052:     }\n  1053: \n  1054:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1055:     /// and destination may *not* overlap.\n  1056:     ///\n  1057:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n  1058:     ///\n  1059:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1060:     ///\n  1061:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1062:     #[inline(always)]",
    "nanvix_source": "   969:     ///\n   970:     /// NOTE: this has the *same* argument order as [`ptr::copy`].\n   971:     ///\n   972:     /// See [`ptr::copy`] for safety concerns and examples.\n   973:     ///\n   974:     /// [`ptr::copy`]: crate::ptr::copy()\n   975:     #[inline(always)]\n   976:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   977:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   978:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   979:     pub const unsafe fn copy_to(self, dest: NonNull<T>, count: usize)\n   980:     where\n   981:         T: Sized,\n   982:     {\n   983:         // SAFETY: the caller must uphold the safety contract for `copy`.\n   984:         unsafe { ptr::copy(self.as_ptr(), dest.as_ptr(), count) }\n   985:     }\n   986: \n   987:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n   988:     /// and destination may *not* overlap.\n   989:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::copy_to_nonoverlapping",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
    ],
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
                      "id": 12,
                      "path": "Sized"
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
        "is_unsafe": true
      },
      "name": "copy_to_nonoverlapping",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
          ],
          [
            "dest",
            {
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
                "id": 9475,
                "path": "NonNull"
              }
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1050:         // SAFETY: the caller must uphold the safety contract for `copy`.\n  1051:         unsafe { ptr::copy(self.as_ptr(), dest.as_ptr(), count) }\n  1052:     }\n  1053: \n  1054:     /// Copies `count * size_of::<T>()` bytes from `self` to `dest`. The source\n  1055:     /// and destination may *not* overlap.\n  1056:     ///\n  1057:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n  1058:     ///\n  1059:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n  1060:     ///\n  1061:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n  1062:     #[inline(always)]\n  1063:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1064:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1065:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  1066:     pub const unsafe fn copy_to_nonoverlapping(self, dest: NonNull<T>, count: usize)\n  1067:     where\n  1068:         T: Sized,\n  1069:     {\n  1070:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1071:         unsafe { ptr::copy_nonoverlapping(self.as_ptr(), dest.as_ptr(), count) }\n  1072:     }\n  1073: \n  1074:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1075:     /// and destination may overlap.\n  1076:     ///\n  1077:     /// NOTE: this has the *opposite* argument order of [`ptr::copy`].\n  1078:     ///\n  1079:     /// See [`ptr::copy`] for safety concerns and examples.\n  1080:     ///\n  1081:     /// [`ptr::copy`]: crate::ptr::copy()\n  1082:     #[inline(always)]",
    "nanvix_source": "   989:     ///\n   990:     /// NOTE: this has the *same* argument order as [`ptr::copy_nonoverlapping`].\n   991:     ///\n   992:     /// See [`ptr::copy_nonoverlapping`] for safety concerns and examples.\n   993:     ///\n   994:     /// [`ptr::copy_nonoverlapping`]: crate::ptr::copy_nonoverlapping()\n   995:     #[inline(always)]\n   996:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   997:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   998:     #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n   999:     pub const unsafe fn copy_to_nonoverlapping(self, dest: NonNull<T>, count: usize)\n  1000:     where\n  1001:         T: Sized,\n  1002:     {\n  1003:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1004:         unsafe { ptr::copy_nonoverlapping(self.as_ptr(), dest.as_ptr(), count) }\n  1005:     }\n  1006: \n  1007:     /// Copies `count * size_of::<T>()` bytes from `src` to `self`. The source\n  1008:     /// and destination may overlap.\n  1009:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::drop_in_place",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
    ],
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
        "is_unsafe": true
      },
      "name": "drop_in_place",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
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
        "output": null
      }
    },
    "verification_source": "  1106:     pub const unsafe fn copy_from_nonoverlapping(self, src: NonNull<T>, count: usize)\n  1107:     where\n  1108:         T: Sized,\n  1109:     {\n  1110:         // SAFETY: the caller must uphold the safety contract for `copy_nonoverlapping`.\n  1111:         unsafe { ptr::copy_nonoverlapping(src.as_ptr(), self.as_ptr(), count) }\n  1112:     }\n  1113: \n  1114:     /// Executes the destructor (if any) of the pointed-to value.\n  1115:     ///\n  1116:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1117:     ///\n  1118:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1119:     #[inline(always)]\n  1120:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1121:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1122:     pub const unsafe fn drop_in_place(self)\n  1123:     where\n  1124:         T: [const] Destruct,\n  1125:     {\n  1126:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1127:         unsafe { ptr::drop_in_place(self.as_ptr()) }\n  1128:     }\n  1129: \n  1130:     /// Overwrites a memory location with the given value without reading or\n  1131:     /// dropping the old value.\n  1132:     ///\n  1133:     /// See [`ptr::write`] for safety concerns and examples.\n  1134:     ///\n  1135:     /// [`ptr::write`]: crate::ptr::write()\n  1136:     #[inline(always)]\n  1137:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1138:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]",
    "nanvix_source": "  1045:     }\n  1046: \n  1047:     /// Executes the destructor (if any) of the pointed-to value.\n  1048:     ///\n  1049:     /// See [`ptr::drop_in_place`] for safety concerns and examples.\n  1050:     ///\n  1051:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place()\n  1052:     #[inline(always)]\n  1053:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1054:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n  1055:     pub const unsafe fn drop_in_place(mut self)\n  1056:     where\n  1057:         T: [const] Destruct,\n  1058:     {\n  1059:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1060:         unsafe { ptr::drop_glue(self.as_mut()) }\n  1061:     }\n  1062: \n  1063:     /// Overwrites a memory location with the given value without reading or\n  1064:     /// dropping the old value.\n  1065:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::new",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
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
                      "generic": "Self"
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
    "verification_source": "   253:     ///\n   254:     /// # Examples\n   255:     ///\n   256:     /// ```\n   257:     /// use std::ptr::NonNull;\n   258:     ///\n   259:     /// let mut x = 0u32;\n   260:     /// let ptr = NonNull::<u32>::new(&mut x as *mut _).expect(\"ptr is null!\");\n   261:     ///\n   262:     /// if let Some(ptr) = NonNull::<u32>::new(std::ptr::null_mut()) {\n   263:     ///     unreachable!();\n   264:     /// }\n   265:     /// ```\n   266:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   267:     #[rustc_const_stable(feature = \"const_nonnull_new\", since = \"1.85.0\")]\n   268:     #[inline]\n   269:     pub const fn new(ptr: *mut T) -> Option<Self> {\n   270:         if !ptr.is_null() {\n   271:             // SAFETY: The pointer is already checked and is not null\n   272:             Some(unsafe { Self::new_unchecked(ptr) })\n   273:         } else {\n   274:             None\n   275:         }\n   276:     }\n   277: \n   278:     /// Converts a reference to a `NonNull` pointer.\n   279:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   280:     #[rustc_const_stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]\n   281:     #[inline]\n   282:     pub const fn from_ref(r: &T) -> Self {\n   283:         // SAFETY: A reference cannot be null.\n   284:         unsafe { transmute(r as *const T) }\n   285:     }",
    "nanvix_source": "   256:     /// let mut x = 0u32;\n   257:     /// let ptr = NonNull::<u32>::new(&mut x as *mut _).expect(\"ptr is null!\");\n   258:     ///\n   259:     /// if let Some(ptr) = NonNull::<u32>::new(std::ptr::null_mut()) {\n   260:     ///     unreachable!();\n   261:     /// }\n   262:     /// ```\n   263:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   264:     #[rustc_const_stable(feature = \"const_nonnull_new\", since = \"1.85.0\")]\n   265:     #[inline]\n   266:     pub const fn new(ptr: *mut T) -> Option<Self> {\n   267:         if !ptr.is_null() {\n   268:             // SAFETY: The pointer is already checked and is not null\n   269:             Some(unsafe { Self::new_unchecked(ptr) })\n   270:         } else {\n   271:             None\n   272:         }\n   273:     }\n   274: \n   275:     /// Converts a reference to a `NonNull` pointer.\n   276:     #[stable(feature = \"non_null_from_ref\", since = \"1.89.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::new_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
        "is_unsafe": true
      },
      "name": "new_unchecked",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 9475,
            "path": "NonNull"
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
                          "id": 7872,
                          "path": "PointeeSized"
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
        "impl_id": "core:9534",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9475",
        "resolved_owner_path": [
          "core",
          "ptr",
          "non_null",
          "NonNull"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   217:     /// let mut x = 0u32;\n   218:     /// let ptr = unsafe { NonNull::new_unchecked(&mut x as *mut _) };\n   219:     /// ```\n   220:     ///\n   221:     /// *Incorrect* usage of this function:\n   222:     ///\n   223:     /// ```rust,no_run\n   224:     /// use std::ptr::NonNull;\n   225:     ///\n   226:     /// // NEVER DO THAT!!! This is undefined behavior. \u26a0\ufe0f\n   227:     /// let ptr = unsafe { NonNull::<u32>::new_unchecked(std::ptr::null_mut()) };\n   228:     /// ```\n   229:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   230:     #[rustc_const_stable(feature = \"const_nonnull_new_unchecked\", since = \"1.25.0\")]\n   231:     #[inline]\n   232:     #[track_caller]\n   233:     pub const unsafe fn new_unchecked(ptr: *mut T) -> Self {\n   234:         // SAFETY: the caller must guarantee that `ptr` is non-null.\n   235:         unsafe {\n   236:             assert_unsafe_precondition!(\n   237:                 check_language_ub,\n   238:                 \"NonNull::new_unchecked requires that the pointer is non-null\",\n   239:                 (ptr: *mut () = ptr as *mut ()) => !ptr.is_null()\n   240:             );\n   241:             transmute(ptr)\n   242:         }\n   243:     }\n   244: \n   245:     /// Creates a new `NonNull` if `ptr` is non-null.\n   246:     ///\n   247:     /// # Panics during const evaluation\n   248:     ///\n   249:     /// This method will panic during const evaluation if the pointer cannot be",
    "nanvix_source": "   220:     /// ```rust,no_run\n   221:     /// use std::ptr::NonNull;\n   222:     ///\n   223:     /// // NEVER DO THAT!!! This is undefined behavior. \u26a0\ufe0f\n   224:     /// let ptr = unsafe { NonNull::<u32>::new_unchecked(std::ptr::null_mut()) };\n   225:     /// ```\n   226:     #[stable(feature = \"nonnull\", since = \"1.25.0\")]\n   227:     #[rustc_const_stable(feature = \"const_nonnull_new_unchecked\", since = \"1.25.0\")]\n   228:     #[inline]\n   229:     #[track_caller]\n   230:     pub const unsafe fn new_unchecked(ptr: *mut T) -> Self {\n   231:         // SAFETY: the caller must guarantee that `ptr` is non-null.\n   232:         unsafe {\n   233:             assert_unsafe_precondition!(\n   234:                 check_language_ub,\n   235:                 \"NonNull::new_unchecked requires that the pointer is non-null\",\n   236:                 (ptr: *mut () = ptr as *mut ()) => !ptr.is_null()\n   237:             );\n   238:             transmute(ptr)\n   239:         }\n   240:     }",
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
