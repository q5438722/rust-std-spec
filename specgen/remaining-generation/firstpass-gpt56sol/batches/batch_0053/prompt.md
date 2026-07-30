For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::slice::split_off_last_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "split_off_last_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "borrowed_ref": {
                    "is_mutable": true,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
                  }
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
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  5069:     ///\n  5070:     /// Returns `None` if the slice is empty.\n  5071:     ///\n  5072:     /// # Examples\n  5073:     ///\n  5074:     /// ```\n  5075:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5076:     /// let last = slice.split_off_last_mut().unwrap();\n  5077:     /// *last = 'd';\n  5078:     ///\n  5079:     /// assert_eq!(slice, &['a', 'b']);\n  5080:     /// assert_eq!(last, &'d');\n  5081:     /// ```\n  5082:     #[inline]\n  5083:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5084:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5085:     pub const fn split_off_last_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {\n  5086:         // FIXME(const-hack): Use `mem::take` and `?` when available in const.\n  5087:         // Original: `mem::take(self).split_last_mut()?`\n  5088:         let Some((last, rem)) = mem::replace(self, &mut []).split_last_mut() else { return None };\n  5089:         *self = rem;\n  5090:         Some(last)\n  5091:     }\n  5092: \n  5093:     /// Returns mutable references to many indices at once, without doing any checks.\n  5094:     ///\n  5095:     /// An index can be either a `usize`, a [`Range`] or a [`RangeInclusive`]. Note\n  5096:     /// that this method takes an array, so all indices must be of the same type.\n  5097:     /// If passed an array of `usize`s this method gives back an array of mutable references\n  5098:     /// to single elements, while if passed an array of ranges it gives back an array of\n  5099:     /// mutable references to slices.\n  5100:     ///\n  5101:     /// For a safe alternative see [`get_disjoint_mut`].",
    "nanvix_source": "  5082:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c'];\n  5083:     /// let last = slice.split_off_last_mut().unwrap();\n  5084:     /// *last = 'd';\n  5085:     ///\n  5086:     /// assert_eq!(slice, &['a', 'b']);\n  5087:     /// assert_eq!(last, &'d');\n  5088:     /// ```\n  5089:     #[inline]\n  5090:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  5091:     #[rustc_const_unstable(feature = \"const_split_off_first_last\", issue = \"138539\")]\n  5092:     pub const fn split_off_last_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {\n  5093:         // FIXME(const-hack): Use `mem::take` and `?` when available in const.\n  5094:         // Original: `mem::take(self).split_last_mut()?`\n  5095:         let Some((last, rem)) = mem::replace(self, &mut []).split_last_mut() else { return None };\n  5096:         *self = rem;\n  5097:         Some(last)\n  5098:     }\n  5099: \n  5100:     /// Returns mutable references to many indices at once, without doing any checks.\n  5101:     ///\n  5102:     /// An index can be either a `usize`, a [`Range`] or a [`RangeInclusive`]. Note",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::split_off_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
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
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "primitive": "usize"
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 23782,
                        "path": "OneSidedRange"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "R"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "split_off_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
        "impl_id": "core:51877",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "borrowed_ref": {
                    "is_mutable": true,
                    "lifetime": "'a",
                    "type": {
                      "generic": "Self"
                    }
                  }
                }
              }
            }
          ],
          [
            "range",
            {
              "generic": "R"
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
                        "is_mutable": true,
                        "lifetime": "'a",
                        "type": {
                          "generic": "Self"
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
    "verification_source": "  4956:     /// ```\n  4957:     ///\n  4958:     /// Getting `None` when `range` is out of bounds:\n  4959:     ///\n  4960:     /// ```\n  4961:     /// let mut slice: &mut [_] = &mut ['a', 'b', 'c', 'd'];\n  4962:     ///\n  4963:     /// assert_eq!(None, slice.split_off_mut(5..));\n  4964:     /// assert_eq!(None, slice.split_off_mut(..5));\n  4965:     /// assert_eq!(None, slice.split_off_mut(..=4));\n  4966:     /// let expected: &mut [_] = &mut ['a', 'b', 'c', 'd'];\n  4967:     /// assert_eq!(Some(expected), slice.split_off_mut(..4));\n  4968:     /// ```\n  4969:     #[inline]\n  4970:     #[must_use = \"method does not modify the slice if the range is out of bounds\"]\n  4971:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  4972:     pub fn split_off_mut<'a, R: OneSidedRange<usize>>(\n  4973:         self: &mut &'a mut Self,\n  4974:         range: R,\n  4975:     ) -> Option<&'a mut Self> {\n  4976:         let (direction, split_index) = split_point_of(range)?;\n  4977:         if split_index > self.len() {\n  4978:             return None;\n  4979:         }\n  4980:         let (front, back) = mem::take(self).split_at_mut(split_index);\n  4981:         match direction {\n  4982:             Direction::Front => {\n  4983:                 *self = back;\n  4984:                 Some(front)\n  4985:             }\n  4986:             Direction::Back => {\n  4987:                 *self = front;\n  4988:                 Some(back)",
    "nanvix_source": "  4969:     ///\n  4970:     /// assert_eq!(None, slice.split_off_mut(5..));\n  4971:     /// assert_eq!(None, slice.split_off_mut(..5));\n  4972:     /// assert_eq!(None, slice.split_off_mut(..=4));\n  4973:     /// let expected: &mut [_] = &mut ['a', 'b', 'c', 'd'];\n  4974:     /// assert_eq!(Some(expected), slice.split_off_mut(..4));\n  4975:     /// ```\n  4976:     #[inline]\n  4977:     #[must_use = \"method does not modify the slice if the range is out of bounds\"]\n  4978:     #[stable(feature = \"slice_take\", since = \"1.87.0\")]\n  4979:     pub fn split_off_mut<'a, R: OneSidedRange<usize>>(\n  4980:         self: &mut &'a mut Self,\n  4981:         range: R,\n  4982:     ) -> Option<&'a mut Self> {\n  4983:         let (direction, split_index) = split_point_of(range)?;\n  4984:         if split_index > self.len() {\n  4985:             return None;\n  4986:         }\n  4987:         let (front, back) = mem::take(self).split_at_mut(split_index);\n  4988:         match direction {\n  4989:             Direction::Front => {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::write_clone_of_slice",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "write_clone_of_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "slice": {
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
              "id": 8278,
              "path": "MaybeUninit"
            }
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
        "impl_id": "core:51771",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "src",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1206:     /// let mut vec = Vec::with_capacity(32);\n  1207:     /// let src = [\"rust\", \"is\", \"a\", \"pretty\", \"cool\", \"language\"].map(|s| s.to_string());\n  1208:     ///\n  1209:     /// vec.spare_capacity_mut()[..src.len()].write_clone_of_slice(&src);\n  1210:     ///\n  1211:     /// // SAFETY: we have just cloned all the elements of len into the spare capacity\n  1212:     /// // the first src.len() elements of the vec are valid now.\n  1213:     /// unsafe {\n  1214:     ///     vec.set_len(src.len());\n  1215:     /// }\n  1216:     ///\n  1217:     /// assert_eq!(vec, src);\n  1218:     /// ```\n  1219:     ///\n  1220:     /// [`write_copy_of_slice`]: slice::write_copy_of_slice\n  1221:     #[stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1222:     pub fn write_clone_of_slice(&mut self, src: &[T]) -> &mut [T]\n  1223:     where\n  1224:         T: Clone,\n  1225:     {\n  1226:         // unlike copy_from_slice this does not call clone_from_slice on the slice\n  1227:         // this is because `MaybeUninit<T: Clone>` does not implement Clone.\n  1228: \n  1229:         assert_eq!(self.len(), src.len(), \"destination and source slices have different lengths\");\n  1230: \n  1231:         // NOTE: We need to explicitly slice them to the same length\n  1232:         // for bounds checking to be elided, and the optimizer will\n  1233:         // generate memcpy for simple cases (for example T = u8).\n  1234:         let len = self.len();\n  1235:         let src = &src[..len];\n  1236: \n  1237:         // guard is needed b/c panic might happen during a clone\n  1238:         let mut guard = Guard { slice: self, initialized: 0 };",
    "nanvix_source": "  1213:     /// // the first src.len() elements of the vec are valid now.\n  1214:     /// unsafe {\n  1215:     ///     vec.set_len(src.len());\n  1216:     /// }\n  1217:     ///\n  1218:     /// assert_eq!(vec, src);\n  1219:     /// ```\n  1220:     ///\n  1221:     /// [`write_copy_of_slice`]: slice::write_copy_of_slice\n  1222:     #[stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1223:     pub fn write_clone_of_slice(&mut self, src: &[T]) -> &mut [T]\n  1224:     where\n  1225:         T: Clone,\n  1226:     {\n  1227:         // unlike copy_from_slice this does not call clone_from_slice on the slice\n  1228:         // this is because `MaybeUninit<T: Clone>` does not implement Clone.\n  1229: \n  1230:         assert_eq!(self.len(), src.len(), \"destination and source slices have different lengths\");\n  1231: \n  1232:         // NOTE: We need to explicitly slice them to the same length\n  1233:         // for bounds checking to be elided, and the optimizer will",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::slice::write_copy_of_slice",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
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
                      "id": 6,
                      "path": "Copy"
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
      "name": "write_copy_of_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "slice": {
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
              "id": 8278,
              "path": "MaybeUninit"
            }
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
        "impl_id": "core:51771",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "src",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "generic": "T"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1146:     /// let src = [0; 16];\n  1147:     ///\n  1148:     /// vec.spare_capacity_mut()[..src.len()].write_copy_of_slice(&src);\n  1149:     ///\n  1150:     /// // SAFETY: we have just copied all the elements of len into the spare capacity\n  1151:     /// // the first src.len() elements of the vec are valid now.\n  1152:     /// unsafe {\n  1153:     ///     vec.set_len(src.len());\n  1154:     /// }\n  1155:     ///\n  1156:     /// assert_eq!(vec, src);\n  1157:     /// ```\n  1158:     ///\n  1159:     /// [`write_clone_of_slice`]: slice::write_clone_of_slice\n  1160:     #[stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1161:     #[rustc_const_stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1162:     pub const fn write_copy_of_slice(&mut self, src: &[T]) -> &mut [T]\n  1163:     where\n  1164:         T: Copy,\n  1165:     {\n  1166:         // SAFETY: &[T] and &[MaybeUninit<T>] have the same layout\n  1167:         let uninit_src: &[MaybeUninit<T>] = unsafe { super::transmute(src) };\n  1168: \n  1169:         self.copy_from_slice(uninit_src);\n  1170: \n  1171:         // SAFETY: Valid elements have just been copied into `self` so it is initialized\n  1172:         unsafe { self.assume_init_mut() }\n  1173:     }\n  1174: \n  1175:     /// Clones the elements from `src` to `self`,\n  1176:     /// returning a mutable reference to the now initialized contents of `self`.\n  1177:     /// Any already initialized elements will not be dropped.\n  1178:     ///",
    "nanvix_source": "  1153:     /// unsafe {\n  1154:     ///     vec.set_len(src.len());\n  1155:     /// }\n  1156:     ///\n  1157:     /// assert_eq!(vec, src);\n  1158:     /// ```\n  1159:     ///\n  1160:     /// [`write_clone_of_slice`]: slice::write_clone_of_slice\n  1161:     #[stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1162:     #[rustc_const_stable(feature = \"maybe_uninit_write_slice\", since = \"1.93.0\")]\n  1163:     pub const fn write_copy_of_slice(&mut self, src: &[T]) -> &mut [T]\n  1164:     where\n  1165:         T: Copy,\n  1166:     {\n  1167:         // SAFETY: &[T] and &[MaybeUninit<T>] have the same layout\n  1168:         let uninit_src: &[MaybeUninit<T>] = unsafe { super::transmute(src) };\n  1169: \n  1170:         self.copy_from_slice(uninit_src);\n  1171: \n  1172:         // SAFETY: Valid elements have just been copied into `self` so it is initialized\n  1173:         unsafe { self.assume_init_mut() }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::as_bytes_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
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
        "is_unsafe": true
      },
      "name": "as_bytes_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
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
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "   527:     ///\n   528:     /// unsafe {\n   529:     ///     let bytes = s.as_bytes_mut();\n   530:     ///\n   531:     ///     bytes[0] = 0xF0;\n   532:     ///     bytes[1] = 0x9F;\n   533:     ///     bytes[2] = 0x8D;\n   534:     ///     bytes[3] = 0x94;\n   535:     /// }\n   536:     ///\n   537:     /// assert_eq!(\"\ud83c\udf54\u2208\ud83c\udf0f\", s);\n   538:     /// ```\n   539:     #[stable(feature = \"str_mut_extras\", since = \"1.20.0\")]\n   540:     #[rustc_const_stable(feature = \"const_str_as_mut\", since = \"1.83.0\")]\n   541:     #[must_use]\n   542:     #[inline(always)]\n   543:     pub const unsafe fn as_bytes_mut(&mut self) -> &mut [u8] {\n   544:         // SAFETY: the cast from `&str` to `&[u8]` is safe since `str`\n   545:         // has the same layout as `&[u8]` (only std can make this guarantee).\n   546:         // The pointer dereference is safe since it comes from a mutable reference which\n   547:         // is guaranteed to be valid for writes.\n   548:         unsafe { &mut *(self as *mut str as *mut [u8]) }\n   549:     }\n   550: \n   551:     /// Converts a string slice to a raw pointer.\n   552:     ///\n   553:     /// As string slices are a slice of bytes, the raw pointer points to a\n   554:     /// [`u8`]. This pointer will be pointing to the first byte of the string\n   555:     /// slice.\n   556:     ///\n   557:     /// The caller must ensure that the returned pointer is never written to.\n   558:     /// If you need to mutate the contents of the string slice, use [`as_mut_ptr`].\n   559:     ///",
    "nanvix_source": "   548:     ///     bytes[2] = 0x8D;\n   549:     ///     bytes[3] = 0x94;\n   550:     /// }\n   551:     ///\n   552:     /// assert_eq!(\"\ud83c\udf54\u2208\ud83c\udf0f\", s);\n   553:     /// ```\n   554:     #[stable(feature = \"str_mut_extras\", since = \"1.20.0\")]\n   555:     #[rustc_const_stable(feature = \"const_str_as_mut\", since = \"1.83.0\")]\n   556:     #[must_use]\n   557:     #[inline(always)]\n   558:     pub const unsafe fn as_bytes_mut(&mut self) -> &mut [u8] {\n   559:         // SAFETY: the cast from `&str` to `&[u8]` is safe since `str`\n   560:         // has the same layout as `&[u8]` (only std can make this guarantee).\n   561:         // The pointer dereference is safe since it comes from a mutable reference which\n   562:         // is guaranteed to be valid for writes.\n   563:         unsafe { &mut *(self as *mut str as *mut [u8]) }\n   564:     }\n   565: \n   566:     /// Converts a string slice to a raw pointer.\n   567:     ///\n   568:     /// As string slices are a slice of bytes, the raw pointer points to a",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::str::from_utf8_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
    ],
    "category": "data_structure",
    "kinds": [
      "free_function",
      "primitive_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view",
      "multiple_rust_declarations_share_path"
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
      "name": "from_utf8_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "v"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "primitive": "str"
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:51935",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "v",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
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
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "primitive": "str"
                        }
                      }
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10083,
                        "path": "Utf8Error"
                      }
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
    "verification_source": "   268:     /// assert_eq!(\"Hello, Rust!\", outstr);\n   269:     /// ```\n   270:     ///\n   271:     /// Incorrect bytes:\n   272:     ///\n   273:     /// ```\n   274:     /// // Some invalid bytes in a mutable vector\n   275:     /// let mut invalid = vec![128, 223];\n   276:     ///\n   277:     /// assert!(str::from_utf8_mut(&mut invalid).is_err());\n   278:     /// ```\n   279:     /// See the docs for [`Utf8Error`] for more details on the kinds of\n   280:     /// errors that can be returned.\n   281:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   282:     #[rustc_const_stable(feature = \"const_str_from_utf8\", since = \"1.87.0\")]\n   283:     #[rustc_diagnostic_item = \"str_inherent_from_utf8_mut\"]\n   284:     pub const fn from_utf8_mut(v: &mut [u8]) -> Result<&mut str, Utf8Error> {\n   285:         converts::from_utf8_mut(v)\n   286:     }\n   287: \n   288:     /// Converts a slice of bytes to a string slice without checking\n   289:     /// that the string contains valid UTF-8.\n   290:     ///\n   291:     /// See the safe version, [`from_utf8`], for more information.\n   292:     ///\n   293:     /// # Safety\n   294:     ///\n   295:     /// The bytes passed in must be valid UTF-8.\n   296:     ///\n   297:     /// # Examples\n   298:     ///\n   299:     /// Basic usage:\n   300:     ///",
    "nanvix_source": "   275:     /// // Some invalid bytes in a mutable vector\n   276:     /// let mut invalid = vec![128, 223];\n   277:     ///\n   278:     /// assert!(str::from_utf8_mut(&mut invalid).is_err());\n   279:     /// ```\n   280:     /// See the docs for [`Utf8Error`] for more details on the kinds of\n   281:     /// errors that can be returned.\n   282:     #[stable(feature = \"inherent_str_constructors\", since = \"1.87.0\")]\n   283:     #[rustc_const_stable(feature = \"const_str_from_utf8\", since = \"1.87.0\")]\n   284:     #[rustc_diagnostic_item = \"str_inherent_from_utf8_mut\"]\n   285:     pub const fn from_utf8_mut(v: &mut [u8]) -> Result<&mut str, Utf8Error> {\n   286:         converts::from_utf8_mut(v)\n   287:     }\n   288: \n   289:     /// Converts a slice of bytes to a string slice without checking\n   290:     /// that the string contains valid UTF-8.\n   291:     ///\n   292:     /// See the safe version, [`from_utf8`], for more information.\n   293:     ///\n   294:     /// # Safety\n   295:     ///",
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
