For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::VecDeque::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_reserve",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
        ],
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
            "additional",
            {
              "primitive": "usize"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1138:     /// fn process_data(data: &[u32]) -> Result<VecDeque<u32>, TryReserveError> {\n  1139:     ///     let mut output = VecDeque::new();\n  1140:     ///\n  1141:     ///     // Pre-reserve the memory, exiting if we can't\n  1142:     ///     output.try_reserve(data.len())?;\n  1143:     ///\n  1144:     ///     // Now we know this can't OOM in the middle of our complex work\n  1145:     ///     output.extend(data.iter().map(|&val| {\n  1146:     ///         val * 2 + 5 // very complicated\n  1147:     ///     }));\n  1148:     ///\n  1149:     ///     Ok(output)\n  1150:     /// }\n  1151:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1152:     /// ```\n  1153:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1154:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1155:         let new_cap =\n  1156:             self.len.checked_add(additional).ok_or(TryReserveErrorKind::CapacityOverflow)?;\n  1157:         let old_cap = self.capacity();\n  1158: \n  1159:         if new_cap > old_cap {\n  1160:             self.buf.try_reserve(self.len, additional)?;\n  1161:             unsafe {\n  1162:                 self.handle_capacity_increase(old_cap);\n  1163:             }\n  1164:         }\n  1165:         Ok(())\n  1166:     }\n  1167: \n  1168:     /// Shrinks the capacity of the deque as much as possible.\n  1169:     ///\n  1170:     /// It will drop down as close as possible to the length but the allocator may still inform the",
    "nanvix_source": "  1197:     ///     // Now we know this can't OOM in the middle of our complex work\n  1198:     ///     output.extend(data.iter().map(|&val| {\n  1199:     ///         val * 2 + 5 // very complicated\n  1200:     ///     }));\n  1201:     ///\n  1202:     ///     Ok(output)\n  1203:     /// }\n  1204:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1205:     /// ```\n  1206:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1207:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1208:         let new_cap =\n  1209:             self.len.checked_add(additional).ok_or(TryReserveErrorKind::CapacityOverflow)?;\n  1210:         let old_cap = self.capacity();\n  1211: \n  1212:         if new_cap > old_cap {\n  1213:             self.buf.try_reserve(self.len, additional)?;\n  1214:             unsafe {\n  1215:                 self.handle_capacity_increase(old_cap);\n  1216:             }\n  1217:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::VecDeque::try_reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_reserve_exact",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
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
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2511,
            "path": "VecDeque"
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
                          "args": null,
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:3127",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:2511",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "vec_deque",
          "VecDeque"
        ],
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
            "additional",
            {
              "primitive": "usize"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1090:     /// fn process_data(data: &[u32]) -> Result<VecDeque<u32>, TryReserveError> {\n  1091:     ///     let mut output = VecDeque::new();\n  1092:     ///\n  1093:     ///     // Pre-reserve the memory, exiting if we can't\n  1094:     ///     output.try_reserve_exact(data.len())?;\n  1095:     ///\n  1096:     ///     // Now we know this can't OOM(Out-Of-Memory) in the middle of our complex work\n  1097:     ///     output.extend(data.iter().map(|&val| {\n  1098:     ///         val * 2 + 5 // very complicated\n  1099:     ///     }));\n  1100:     ///\n  1101:     ///     Ok(output)\n  1102:     /// }\n  1103:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1104:     /// ```\n  1105:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1106:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1107:         let new_cap =\n  1108:             self.len.checked_add(additional).ok_or(TryReserveErrorKind::CapacityOverflow)?;\n  1109:         let old_cap = self.capacity();\n  1110: \n  1111:         if new_cap > old_cap {\n  1112:             self.buf.try_reserve_exact(self.len, additional)?;\n  1113:             unsafe {\n  1114:                 self.handle_capacity_increase(old_cap);\n  1115:             }\n  1116:         }\n  1117:         Ok(())\n  1118:     }\n  1119: \n  1120:     /// Tries to reserve capacity for at least `additional` more elements to be inserted\n  1121:     /// in the given deque. The collection may reserve more space to speculatively avoid\n  1122:     /// frequent reallocations. After calling `try_reserve`, capacity will be",
    "nanvix_source": "  1149:     ///     // Now we know this can't OOM(Out-Of-Memory) in the middle of our complex work\n  1150:     ///     output.extend(data.iter().map(|&val| {\n  1151:     ///         val * 2 + 5 // very complicated\n  1152:     ///     }));\n  1153:     ///\n  1154:     ///     Ok(output)\n  1155:     /// }\n  1156:     /// # process_data(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1157:     /// ```\n  1158:     #[stable(feature = \"try_reserve\", since = \"1.57.0\")]\n  1159:     pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1160:         let new_cap =\n  1161:             self.len.checked_add(additional).ok_or(TryReserveErrorKind::CapacityOverflow)?;\n  1162:         let old_cap = self.capacity();\n  1163: \n  1164:         if new_cap > old_cap {\n  1165:             self.buf.try_reserve_exact(self.len, additional)?;\n  1166:             unsafe {\n  1167:                 self.handle_capacity_increase(old_cap);\n  1168:             }\n  1169:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
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
      "name": "capacity",
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
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "  1156:         self.vec.extend_from_within(src);\n  1157:     }\n  1158: \n  1159:     /// Returns this `String`'s capacity, in bytes.\n  1160:     ///\n  1161:     /// # Examples\n  1162:     ///\n  1163:     /// ```\n  1164:     /// let s = String::with_capacity(10);\n  1165:     ///\n  1166:     /// assert!(s.capacity() >= 10);\n  1167:     /// ```\n  1168:     #[inline]\n  1169:     #[must_use]\n  1170:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1171:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1172:     pub const fn capacity(&self) -> usize {\n  1173:         self.vec.capacity()\n  1174:     }\n  1175: \n  1176:     /// Reserves capacity for at least `additional` bytes more than the\n  1177:     /// current length. The allocator may reserve more space to speculatively\n  1178:     /// avoid frequent allocations. After calling `reserve`,\n  1179:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1180:     /// Does nothing if capacity is already sufficient.\n  1181:     ///\n  1182:     /// # Panics\n  1183:     ///\n  1184:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1185:     ///\n  1186:     /// # Examples\n  1187:     ///\n  1188:     /// Basic usage:",
    "nanvix_source": "  1167:     ///\n  1168:     /// ```\n  1169:     /// let s = String::with_capacity(10);\n  1170:     ///\n  1171:     /// assert!(s.capacity() >= 10);\n  1172:     /// ```\n  1173:     #[inline]\n  1174:     #[must_use]\n  1175:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1176:     #[rustc_const_stable(feature = \"const_vec_string_slice\", since = \"1.87.0\")]\n  1177:     pub const fn capacity(&self) -> usize {\n  1178:         self.vec.capacity()\n  1179:     }\n  1180: \n  1181:     /// Reserves capacity for at least `additional` bytes more than the\n  1182:     /// current length. The allocator may reserve more space to speculatively\n  1183:     /// avoid frequent allocations. After calling `reserve`,\n  1184:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1185:     /// Does nothing if capacity is already sufficient.\n  1186:     ///\n  1187:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
      "name": "reserve",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1203:     /// s.push('b');\n  1204:     ///\n  1205:     /// // s now has a length of 2 and a capacity of at least 10\n  1206:     /// let capacity = s.capacity();\n  1207:     /// assert_eq!(2, s.len());\n  1208:     /// assert!(capacity >= 10);\n  1209:     ///\n  1210:     /// // Since we already have at least an extra 8 capacity, calling this...\n  1211:     /// s.reserve(8);\n  1212:     ///\n  1213:     /// // ... doesn't actually increase.\n  1214:     /// assert_eq!(capacity, s.capacity());\n  1215:     /// ```\n  1216:     #[cfg(not(no_global_oom_handling))]\n  1217:     #[inline]\n  1218:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1219:     pub fn reserve(&mut self, additional: usize) {\n  1220:         self.vec.reserve(additional)\n  1221:     }\n  1222: \n  1223:     /// Reserves the minimum capacity for at least `additional` bytes more than\n  1224:     /// the current length. Unlike [`reserve`], this will not\n  1225:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1226:     /// After calling `reserve_exact`, capacity will be greater than or equal to\n  1227:     /// `self.len() + additional`. Does nothing if the capacity is already\n  1228:     /// sufficient.\n  1229:     ///\n  1230:     /// [`reserve`]: String::reserve\n  1231:     ///\n  1232:     /// # Panics\n  1233:     ///\n  1234:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1235:     ///",
    "nanvix_source": "  1214:     ///\n  1215:     /// // Since we already have at least an extra 8 capacity, calling this...\n  1216:     /// s.reserve(8);\n  1217:     ///\n  1218:     /// // ... doesn't actually increase.\n  1219:     /// assert_eq!(capacity, s.capacity());\n  1220:     /// ```\n  1221:     #[cfg(not(no_global_oom_handling))]\n  1222:     #[inline]\n  1223:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1224:     pub fn reserve(&mut self, additional: usize) {\n  1225:         self.vec.reserve(additional)\n  1226:     }\n  1227: \n  1228:     /// Reserves the minimum capacity for at least `additional` bytes more than\n  1229:     /// the current length. Unlike [`reserve`], this will not\n  1230:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1231:     /// After calling `reserve_exact`, capacity will be greater than or equal to\n  1232:     /// `self.len() + additional`. Does nothing if the capacity is already\n  1233:     /// sufficient.\n  1234:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
      "name": "reserve_exact",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1253:     /// s.push('b');\n  1254:     ///\n  1255:     /// // s now has a length of 2 and a capacity of at least 10\n  1256:     /// let capacity = s.capacity();\n  1257:     /// assert_eq!(2, s.len());\n  1258:     /// assert!(capacity >= 10);\n  1259:     ///\n  1260:     /// // Since we already have at least an extra 8 capacity, calling this...\n  1261:     /// s.reserve_exact(8);\n  1262:     ///\n  1263:     /// // ... doesn't actually increase.\n  1264:     /// assert_eq!(capacity, s.capacity());\n  1265:     /// ```\n  1266:     #[cfg(not(no_global_oom_handling))]\n  1267:     #[inline]\n  1268:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1269:     pub fn reserve_exact(&mut self, additional: usize) {\n  1270:         self.vec.reserve_exact(additional)\n  1271:     }\n  1272: \n  1273:     /// Tries to reserve capacity for at least `additional` bytes more than the\n  1274:     /// current length. The allocator may reserve more space to speculatively\n  1275:     /// avoid frequent allocations. After calling `try_reserve`, capacity will be\n  1276:     /// greater than or equal to `self.len() + additional` if it returns\n  1277:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1278:     /// preserves the contents even if an error occurs.\n  1279:     ///\n  1280:     /// # Errors\n  1281:     ///\n  1282:     /// If the capacity overflows, or the allocator reports a failure, then an error\n  1283:     /// is returned.\n  1284:     ///\n  1285:     /// # Examples",
    "nanvix_source": "  1264:     ///\n  1265:     /// // Since we already have at least an extra 8 capacity, calling this...\n  1266:     /// s.reserve_exact(8);\n  1267:     ///\n  1268:     /// // ... doesn't actually increase.\n  1269:     /// assert_eq!(capacity, s.capacity());\n  1270:     /// ```\n  1271:     #[cfg(not(no_global_oom_handling))]\n  1272:     #[inline]\n  1273:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1274:     pub fn reserve_exact(&mut self, additional: usize) {\n  1275:         self.vec.reserve_exact(additional)\n  1276:     }\n  1277: \n  1278:     /// Tries to reserve capacity for at least `additional` bytes more than the\n  1279:     /// current length. The allocator may reserve more space to speculatively\n  1280:     /// avoid frequent allocations. After calling `try_reserve`, capacity will be\n  1281:     /// greater than or equal to `self.len() + additional` if it returns\n  1282:     /// `Ok(())`. Does nothing if capacity is already sufficient. This method\n  1283:     /// preserves the contents even if an error occurs.\n  1284:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::string::String::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
      "name": "shrink_to",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 119,
            "path": "String"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "alloc:4074",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:119",
        "resolved_owner_path": [
          "alloc",
          "string",
          "String"
        ],
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
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1376:     /// # Examples\n  1377:     ///\n  1378:     /// ```\n  1379:     /// let mut s = String::from(\"foo\");\n  1380:     ///\n  1381:     /// s.reserve(100);\n  1382:     /// assert!(s.capacity() >= 100);\n  1383:     ///\n  1384:     /// s.shrink_to(10);\n  1385:     /// assert!(s.capacity() >= 10);\n  1386:     /// s.shrink_to(0);\n  1387:     /// assert!(s.capacity() >= 3);\n  1388:     /// ```\n  1389:     #[cfg(not(no_global_oom_handling))]\n  1390:     #[inline]\n  1391:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1392:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1393:         self.vec.shrink_to(min_capacity)\n  1394:     }\n  1395: \n  1396:     /// Appends the given [`char`] to the end of this `String`.\n  1397:     ///\n  1398:     /// # Panics\n  1399:     ///\n  1400:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1401:     ///\n  1402:     /// # Examples\n  1403:     ///\n  1404:     /// ```\n  1405:     /// let mut s = String::from(\"abc\");\n  1406:     ///\n  1407:     /// s.push('1');\n  1408:     /// s.push('2');",
    "nanvix_source": "  1387:     /// assert!(s.capacity() >= 100);\n  1388:     ///\n  1389:     /// s.shrink_to(10);\n  1390:     /// assert!(s.capacity() >= 10);\n  1391:     /// s.shrink_to(0);\n  1392:     /// assert!(s.capacity() >= 3);\n  1393:     /// ```\n  1394:     #[cfg(not(no_global_oom_handling))]\n  1395:     #[inline]\n  1396:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1397:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1398:         self.vec.shrink_to(min_capacity)\n  1399:     }\n  1400: \n  1401:     /// Appends the given [`char`] to the end of this `String`.\n  1402:     ///\n  1403:     /// # Panics\n  1404:     ///\n  1405:     /// Panics if the new capacity exceeds `isize::MAX` _bytes_.\n  1406:     ///\n  1407:     /// # Examples",
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
