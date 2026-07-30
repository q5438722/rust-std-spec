For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::NonNull::replace",
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
      "name": "replace",
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
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "src",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1201:     where\n  1202:         T: Sized,\n  1203:     {\n  1204:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1205:         unsafe { ptr::write_unaligned(self.as_ptr(), val) }\n  1206:     }\n  1207: \n  1208:     /// Replaces the value at `self` with `src`, returning the old\n  1209:     /// value, without dropping either.\n  1210:     ///\n  1211:     /// See [`ptr::replace`] for safety concerns and examples.\n  1212:     ///\n  1213:     /// [`ptr::replace`]: crate::ptr::replace()\n  1214:     #[inline(always)]\n  1215:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1216:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]\n  1217:     pub const unsafe fn replace(self, src: T) -> T\n  1218:     where\n  1219:         T: Sized,\n  1220:     {\n  1221:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1222:         unsafe { ptr::replace(self.as_ptr(), src) }\n  1223:     }\n  1224: \n  1225:     /// Swaps the values at two mutable locations of the same type, without\n  1226:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1227:     /// otherwise equivalent.\n  1228:     ///\n  1229:     /// See [`ptr::swap`] for safety concerns and examples.\n  1230:     ///\n  1231:     /// [`ptr::swap`]: crate::ptr::swap()\n  1232:     #[inline(always)]\n  1233:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]",
    "nanvix_source": "  1140: \n  1141:     /// Replaces the value at `self` with `src`, returning the old\n  1142:     /// value, without dropping either.\n  1143:     ///\n  1144:     /// See [`ptr::replace`] for safety concerns and examples.\n  1145:     ///\n  1146:     /// [`ptr::replace`]: crate::ptr::replace()\n  1147:     #[inline(always)]\n  1148:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1149:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]\n  1150:     pub const unsafe fn replace(self, src: T) -> T\n  1151:     where\n  1152:         T: Sized,\n  1153:     {\n  1154:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1155:         unsafe { ptr::replace(self.as_ptr(), src) }\n  1156:     }\n  1157: \n  1158:     /// Swaps the values at two mutable locations of the same type, without\n  1159:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1160:     /// otherwise equivalent.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::sub",
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
      "name": "sub",
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
            "self",
            {
              "generic": "Self"
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
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   712:     /// ```\n   713:     /// use std::ptr::NonNull;\n   714:     ///\n   715:     /// let s: &str = \"123\";\n   716:     ///\n   717:     /// unsafe {\n   718:     ///     let end: NonNull<u8> = NonNull::new(s.as_ptr().cast_mut()).unwrap().add(3);\n   719:     ///     println!(\"{}\", end.sub(1).read() as char);\n   720:     ///     println!(\"{}\", end.sub(2).read() as char);\n   721:     /// }\n   722:     /// ```\n   723:     #[inline(always)]\n   724:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   725:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   726:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   727:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   728:     pub const unsafe fn sub(self, count: usize) -> Self\n   729:     where\n   730:         T: Sized,\n   731:     {\n   732:         if T::IS_ZST {\n   733:             // Pointer arithmetic does nothing when the pointee is a ZST.\n   734:             self\n   735:         } else {\n   736:             // SAFETY: the caller must uphold the safety contract for `offset`.\n   737:             // Because the pointee is *not* a ZST, that means that `count` is\n   738:             // at most `isize::MAX`, and thus the negation cannot overflow.\n   739:             unsafe { self.offset((count as isize).unchecked_neg()) }\n   740:         }\n   741:     }\n   742: \n   743:     /// Calculates the offset from a pointer in bytes (convenience for\n   744:     /// `.byte_offset((count as isize).wrapping_neg())`).",
    "nanvix_source": "   651:     ///     let end: NonNull<u8> = NonNull::new(s.as_ptr().cast_mut()).unwrap().add(3);\n   652:     ///     println!(\"{}\", end.sub(1).read() as char);\n   653:     ///     println!(\"{}\", end.sub(2).read() as char);\n   654:     /// }\n   655:     /// ```\n   656:     #[inline(always)]\n   657:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   658:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n   659:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   660:     #[rustc_const_stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n   661:     pub const unsafe fn sub(self, count: usize) -> Self\n   662:     where\n   663:         T: Sized,\n   664:     {\n   665:         if T::IS_ZST {\n   666:             // Pointer arithmetic does nothing when the pointee is a ZST.\n   667:             self\n   668:         } else {\n   669:             // SAFETY: the caller must uphold the safety contract for `offset`.\n   670:             // Because the pointee is *not* a ZST, that means that `count` is\n   671:             // at most `isize::MAX`, and thus the negation cannot overflow.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::swap",
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
      "name": "swap",
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
            "with",
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1219:         T: Sized,\n  1220:     {\n  1221:         // SAFETY: the caller must uphold the safety contract for `replace`.\n  1222:         unsafe { ptr::replace(self.as_ptr(), src) }\n  1223:     }\n  1224: \n  1225:     /// Swaps the values at two mutable locations of the same type, without\n  1226:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1227:     /// otherwise equivalent.\n  1228:     ///\n  1229:     /// See [`ptr::swap`] for safety concerns and examples.\n  1230:     ///\n  1231:     /// [`ptr::swap`]: crate::ptr::swap()\n  1232:     #[inline(always)]\n  1233:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1234:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n  1235:     pub const unsafe fn swap(self, with: NonNull<T>)\n  1236:     where\n  1237:         T: Sized,\n  1238:     {\n  1239:         // SAFETY: the caller must uphold the safety contract for `swap`.\n  1240:         unsafe { ptr::swap(self.as_ptr(), with.as_ptr()) }\n  1241:     }\n  1242: \n  1243:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1244:     /// `align`.\n  1245:     ///\n  1246:     /// If it is not possible to align the pointer, the implementation returns\n  1247:     /// `usize::MAX`.\n  1248:     ///\n  1249:     /// The offset is expressed in number of `T` elements, and not bytes.\n  1250:     ///\n  1251:     /// There are no guarantees whatsoever that offsetting the pointer will not overflow or go",
    "nanvix_source": "  1158:     /// Swaps the values at two mutable locations of the same type, without\n  1159:     /// deinitializing either. They may overlap, unlike `mem::swap` which is\n  1160:     /// otherwise equivalent.\n  1161:     ///\n  1162:     /// See [`ptr::swap`] for safety concerns and examples.\n  1163:     ///\n  1164:     /// [`ptr::swap`]: crate::ptr::swap()\n  1165:     #[inline(always)]\n  1166:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1167:     #[rustc_const_stable(feature = \"const_swap\", since = \"1.85.0\")]\n  1168:     pub const unsafe fn swap(self, with: NonNull<T>)\n  1169:     where\n  1170:         T: Sized,\n  1171:     {\n  1172:         // SAFETY: the caller must uphold the safety contract for `swap`.\n  1173:         unsafe { ptr::swap(self.as_ptr(), with.as_ptr()) }\n  1174:     }\n  1175: \n  1176:     /// Computes the offset that needs to be applied to the pointer in order to make it aligned to\n  1177:     /// `align`.\n  1178:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::write",
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
      "name": "write",
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
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1124:         T: [const] Destruct,\n  1125:     {\n  1126:         // SAFETY: the caller must uphold the safety contract for `drop_in_place`.\n  1127:         unsafe { ptr::drop_in_place(self.as_ptr()) }\n  1128:     }\n  1129: \n  1130:     /// Overwrites a memory location with the given value without reading or\n  1131:     /// dropping the old value.\n  1132:     ///\n  1133:     /// See [`ptr::write`] for safety concerns and examples.\n  1134:     ///\n  1135:     /// [`ptr::write`]: crate::ptr::write()\n  1136:     #[inline(always)]\n  1137:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1138:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1139:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1140:     pub const unsafe fn write(self, val: T)\n  1141:     where\n  1142:         T: Sized,\n  1143:     {\n  1144:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1145:         unsafe { ptr::write(self.as_ptr(), val) }\n  1146:     }\n  1147: \n  1148:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1149:     /// bytes of memory starting at `self` to `val`.\n  1150:     ///\n  1151:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1152:     ///\n  1153:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1154:     #[inline(always)]\n  1155:     #[doc(alias = \"memset\")]\n  1156:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces",
    "nanvix_source": "  1063:     /// Overwrites a memory location with the given value without reading or\n  1064:     /// dropping the old value.\n  1065:     ///\n  1066:     /// See [`ptr::write`] for safety concerns and examples.\n  1067:     ///\n  1068:     /// [`ptr::write`]: crate::ptr::write()\n  1069:     #[inline(always)]\n  1070:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1071:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1072:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1073:     pub const unsafe fn write(self, val: T)\n  1074:     where\n  1075:         T: Sized,\n  1076:     {\n  1077:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1078:         unsafe { ptr::write(self.as_ptr(), val) }\n  1079:     }\n  1080: \n  1081:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1082:     /// bytes of memory starting at `self` to `val`.\n  1083:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::write_bytes",
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
      "name": "write_bytes",
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
            "val",
            {
              "primitive": "u8"
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
    "verification_source": "  1143:     {\n  1144:         // SAFETY: the caller must uphold the safety contract for `write`.\n  1145:         unsafe { ptr::write(self.as_ptr(), val) }\n  1146:     }\n  1147: \n  1148:     /// Invokes memset on the specified pointer, setting `count * size_of::<T>()`\n  1149:     /// bytes of memory starting at `self` to `val`.\n  1150:     ///\n  1151:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1152:     ///\n  1153:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1154:     #[inline(always)]\n  1155:     #[doc(alias = \"memset\")]\n  1156:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1157:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1158:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1159:     pub const unsafe fn write_bytes(self, val: u8, count: usize)\n  1160:     where\n  1161:         T: Sized,\n  1162:     {\n  1163:         // SAFETY: the caller must uphold the safety contract for `write_bytes`.\n  1164:         unsafe { ptr::write_bytes(self.as_ptr(), val, count) }\n  1165:     }\n  1166: \n  1167:     /// Performs a volatile write of a memory location with the given value without\n  1168:     /// reading or dropping the old value.\n  1169:     ///\n  1170:     /// Volatile operations are intended to act on I/O memory, and are guaranteed\n  1171:     /// to not be elided or reordered by the compiler across other volatile\n  1172:     /// operations.\n  1173:     ///\n  1174:     /// See [`ptr::write_volatile`] for safety concerns and examples.\n  1175:     ///",
    "nanvix_source": "  1082:     /// bytes of memory starting at `self` to `val`.\n  1083:     ///\n  1084:     /// See [`ptr::write_bytes`] for safety concerns and examples.\n  1085:     ///\n  1086:     /// [`ptr::write_bytes`]: crate::ptr::write_bytes()\n  1087:     #[inline(always)]\n  1088:     #[doc(alias = \"memset\")]\n  1089:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1090:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1091:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1092:     pub const unsafe fn write_bytes(self, val: u8, count: usize)\n  1093:     where\n  1094:         T: Sized,\n  1095:     {\n  1096:         // SAFETY: the caller must uphold the safety contract for `write_bytes`.\n  1097:         unsafe { ptr::write_bytes(self.as_ptr(), val, count) }\n  1098:     }\n  1099: \n  1100:     /// Performs a volatile write of a memory location with the given value without\n  1101:     /// reading or dropping the old value.\n  1102:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::NonNull::write_unaligned",
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
      "name": "write_unaligned",
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
            "val",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1184:         // SAFETY: the caller must uphold the safety contract for `write_volatile`.\n  1185:         unsafe { ptr::write_volatile(self.as_ptr(), val) }\n  1186:     }\n  1187: \n  1188:     /// Overwrites a memory location with the given value without reading or\n  1189:     /// dropping the old value.\n  1190:     ///\n  1191:     /// Unlike `write`, the pointer may be unaligned.\n  1192:     ///\n  1193:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1194:     ///\n  1195:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1196:     #[inline(always)]\n  1197:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1198:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1199:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1200:     pub const unsafe fn write_unaligned(self, val: T)\n  1201:     where\n  1202:         T: Sized,\n  1203:     {\n  1204:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1205:         unsafe { ptr::write_unaligned(self.as_ptr(), val) }\n  1206:     }\n  1207: \n  1208:     /// Replaces the value at `self` with `src`, returning the old\n  1209:     /// value, without dropping either.\n  1210:     ///\n  1211:     /// See [`ptr::replace`] for safety concerns and examples.\n  1212:     ///\n  1213:     /// [`ptr::replace`]: crate::ptr::replace()\n  1214:     #[inline(always)]\n  1215:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1216:     #[rustc_const_stable(feature = \"const_inherent_ptr_replace\", since = \"1.88.0\")]",
    "nanvix_source": "  1123:     ///\n  1124:     /// Unlike `write`, the pointer may be unaligned.\n  1125:     ///\n  1126:     /// See [`ptr::write_unaligned`] for safety concerns and examples.\n  1127:     ///\n  1128:     /// [`ptr::write_unaligned`]: crate::ptr::write_unaligned()\n  1129:     #[inline(always)]\n  1130:     #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1131:     #[stable(feature = \"non_null_convenience\", since = \"1.80.0\")]\n  1132:     #[rustc_const_stable(feature = \"const_ptr_write\", since = \"1.83.0\")]\n  1133:     pub const unsafe fn write_unaligned(self, val: T)\n  1134:     where\n  1135:         T: Sized,\n  1136:     {\n  1137:         // SAFETY: the caller must uphold the safety contract for `write_unaligned`.\n  1138:         unsafe { ptr::write_unaligned(self.as_ptr(), val) }\n  1139:     }\n  1140: \n  1141:     /// Replaces the value at `self` with `src`, returning the old\n  1142:     /// value, without dropping either.\n  1143:     ///",
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
