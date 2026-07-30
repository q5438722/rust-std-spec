For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::time::Duration::checked_sub",
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
      "name": "checked_sub",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
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
            "rhs",
            {
              "resolved_path": {
                "args": null,
                "id": 10186,
                "path": "Duration"
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
                        "id": 10186,
                        "path": "Duration"
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
    "verification_source": "   710:     /// Checked `Duration` subtraction. Computes `self - other`, returning [`None`]\n   711:     /// if the result would be negative or if overflow occurred.\n   712:     ///\n   713:     /// # Examples\n   714:     ///\n   715:     /// ```\n   716:     /// use std::time::Duration;\n   717:     ///\n   718:     /// assert_eq!(Duration::new(0, 1).checked_sub(Duration::new(0, 0)), Some(Duration::new(0, 1)));\n   719:     /// assert_eq!(Duration::new(0, 0).checked_sub(Duration::new(0, 1)), None);\n   720:     /// ```\n   721:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   722:     #[must_use = \"this returns the result of the operation, \\\n   723:                   without modifying the original\"]\n   724:     #[inline]\n   725:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   726:     pub const fn checked_sub(self, rhs: Duration) -> Option<Duration> {\n   727:         if let Some(mut secs) = self.secs.checked_sub(rhs.secs) {\n   728:             let nanos = if self.nanos.as_inner() >= rhs.nanos.as_inner() {\n   729:                 self.nanos.as_inner() - rhs.nanos.as_inner()\n   730:             } else if let Some(sub_secs) = secs.checked_sub(1) {\n   731:                 secs = sub_secs;\n   732:                 self.nanos.as_inner() + NANOS_PER_SEC - rhs.nanos.as_inner()\n   733:             } else {\n   734:                 return None;\n   735:             };\n   736:             debug_assert!(nanos < NANOS_PER_SEC);\n   737:             Some(Duration::new(secs, nanos))\n   738:         } else {\n   739:             None\n   740:         }\n   741:     }\n   742: ",
    "nanvix_source": "   716:     /// use std::time::Duration;\n   717:     ///\n   718:     /// assert_eq!(Duration::new(0, 1).checked_sub(Duration::new(0, 0)), Some(Duration::new(0, 1)));\n   719:     /// assert_eq!(Duration::new(0, 0).checked_sub(Duration::new(0, 1)), None);\n   720:     /// ```\n   721:     #[stable(feature = \"duration_checked_ops\", since = \"1.16.0\")]\n   722:     #[must_use = \"this returns the result of the operation, \\\n   723:                   without modifying the original\"]\n   724:     #[inline]\n   725:     #[rustc_const_stable(feature = \"duration_consts_2\", since = \"1.58.0\")]\n   726:     pub const fn checked_sub(self, rhs: Duration) -> Option<Duration> {\n   727:         if let Some(mut secs) = self.secs.checked_sub(rhs.secs) {\n   728:             let nanos = if self.nanos.as_inner() >= rhs.nanos.as_inner() {\n   729:                 self.nanos.as_inner() - rhs.nanos.as_inner()\n   730:             } else if let Some(sub_secs) = secs.checked_sub(1) {\n   731:                 secs = sub_secs;\n   732:                 self.nanos.as_inner() + NANOS_PER_SEC - rhs.nanos.as_inner()\n   733:             } else {\n   734:                 return None;\n   735:             };\n   736:             debug_assert!(nanos < NANOS_PER_SEC);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::div_duration_f32",
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
      "name": "div_duration_f32",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
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
            "rhs",
            {
              "resolved_path": {
                "args": null,
                "id": 10186,
                "path": "Duration"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "f32"
        }
      }
    },
    "verification_source": "  1110: \n  1111:     /// Divides `Duration` by `Duration` and returns `f32`.\n  1112:     ///\n  1113:     /// # Examples\n  1114:     /// ```\n  1115:     /// use std::time::Duration;\n  1116:     ///\n  1117:     /// let dur1 = Duration::new(2, 700_000_000);\n  1118:     /// let dur2 = Duration::new(5, 400_000_000);\n  1119:     /// assert_eq!(dur1.div_duration_f32(dur2), 0.5);\n  1120:     /// ```\n  1121:     #[stable(feature = \"div_duration\", since = \"1.80.0\")]\n  1122:     #[must_use = \"this returns the result of the operation, \\\n  1123:                   without modifying the original\"]\n  1124:     #[inline]\n  1125:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n  1126:     pub const fn div_duration_f32(self, rhs: Duration) -> f32 {\n  1127:         let self_nanos =\n  1128:             (self.secs as f32) * (NANOS_PER_SEC as f32) + (self.nanos.as_inner() as f32);\n  1129:         let rhs_nanos = (rhs.secs as f32) * (NANOS_PER_SEC as f32) + (rhs.nanos.as_inner() as f32);\n  1130:         self_nanos / rhs_nanos\n  1131:     }\n  1132: \n  1133:     /// Divides `Duration` by `Duration` and returns `u128`, rounding the result towards zero.\n  1134:     ///\n  1135:     /// # Examples\n  1136:     /// ```\n  1137:     /// #![feature(duration_integer_division)]\n  1138:     /// use std::time::Duration;\n  1139:     ///\n  1140:     /// let dur = Duration::new(2, 0);\n  1141:     /// assert_eq!(dur.div_duration_floor(Duration::new(1, 000_000_001)), 1);\n  1142:     /// assert_eq!(dur.div_duration_floor(Duration::new(1, 000_000_000)), 2);",
    "nanvix_source": "  1192:     ///\n  1193:     /// let dur1 = Duration::new(2, 700_000_000);\n  1194:     /// let dur2 = Duration::new(5, 400_000_000);\n  1195:     /// assert_eq!(dur1.div_duration_f32(dur2), 0.5);\n  1196:     /// ```\n  1197:     #[stable(feature = \"div_duration\", since = \"1.80.0\")]\n  1198:     #[must_use = \"this returns the result of the operation, \\\n  1199:                   without modifying the original\"]\n  1200:     #[inline]\n  1201:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n  1202:     pub const fn div_duration_f32(self, rhs: Duration) -> f32 {\n  1203:         let self_nanos =\n  1204:             (self.secs as f32) * (NANOS_PER_SEC as f32) + (self.nanos.as_inner() as f32);\n  1205:         let rhs_nanos = (rhs.secs as f32) * (NANOS_PER_SEC as f32) + (rhs.nanos.as_inner() as f32);\n  1206:         self_nanos / rhs_nanos\n  1207:     }\n  1208: \n  1209:     /// Divides `Duration` by `Duration` and returns `u128`, rounding the result towards zero.\n  1210:     ///\n  1211:     /// # Examples\n  1212:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::div_duration_f64",
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
      "name": "div_duration_f64",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
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
            "rhs",
            {
              "resolved_path": {
                "args": null,
                "id": 10186,
                "path": "Duration"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "f64"
        }
      }
    },
    "verification_source": "  1088: \n  1089:     /// Divides `Duration` by `Duration` and returns `f64`.\n  1090:     ///\n  1091:     /// # Examples\n  1092:     /// ```\n  1093:     /// use std::time::Duration;\n  1094:     ///\n  1095:     /// let dur1 = Duration::new(2, 700_000_000);\n  1096:     /// let dur2 = Duration::new(5, 400_000_000);\n  1097:     /// assert_eq!(dur1.div_duration_f64(dur2), 0.5);\n  1098:     /// ```\n  1099:     #[stable(feature = \"div_duration\", since = \"1.80.0\")]\n  1100:     #[must_use = \"this returns the result of the operation, \\\n  1101:                   without modifying the original\"]\n  1102:     #[inline]\n  1103:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n  1104:     pub const fn div_duration_f64(self, rhs: Duration) -> f64 {\n  1105:         let self_nanos =\n  1106:             (self.secs as f64) * (NANOS_PER_SEC as f64) + (self.nanos.as_inner() as f64);\n  1107:         let rhs_nanos = (rhs.secs as f64) * (NANOS_PER_SEC as f64) + (rhs.nanos.as_inner() as f64);\n  1108:         self_nanos / rhs_nanos\n  1109:     }\n  1110: \n  1111:     /// Divides `Duration` by `Duration` and returns `f32`.\n  1112:     ///\n  1113:     /// # Examples\n  1114:     /// ```\n  1115:     /// use std::time::Duration;\n  1116:     ///\n  1117:     /// let dur1 = Duration::new(2, 700_000_000);\n  1118:     /// let dur2 = Duration::new(5, 400_000_000);\n  1119:     /// assert_eq!(dur1.div_duration_f32(dur2), 0.5);\n  1120:     /// ```",
    "nanvix_source": "  1170:     ///\n  1171:     /// let dur1 = Duration::new(2, 700_000_000);\n  1172:     /// let dur2 = Duration::new(5, 400_000_000);\n  1173:     /// assert_eq!(dur1.div_duration_f64(dur2), 0.5);\n  1174:     /// ```\n  1175:     #[stable(feature = \"div_duration\", since = \"1.80.0\")]\n  1176:     #[must_use = \"this returns the result of the operation, \\\n  1177:                   without modifying the original\"]\n  1178:     #[inline]\n  1179:     #[rustc_const_stable(feature = \"duration_consts_float\", since = \"1.83.0\")]\n  1180:     pub const fn div_duration_f64(self, rhs: Duration) -> f64 {\n  1181:         let self_nanos =\n  1182:             (self.secs as f64) * (NANOS_PER_SEC as f64) + (self.nanos.as_inner() as f64);\n  1183:         let rhs_nanos = (rhs.secs as f64) * (NANOS_PER_SEC as f64) + (rhs.nanos.as_inner() as f64);\n  1184:         self_nanos / rhs_nanos\n  1185:     }\n  1186: \n  1187:     /// Divides `Duration` by `Duration` and returns `f32`.\n  1188:     ///\n  1189:     /// # Examples\n  1190:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::div_f32",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "div_f32",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
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
            "rhs",
            {
              "primitive": "f32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "  1069:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1070:     ///\n  1071:     /// # Examples\n  1072:     /// ```\n  1073:     /// use std::time::Duration;\n  1074:     ///\n  1075:     /// let dur = Duration::new(2, 700_000_000);\n  1076:     /// // note that due to rounding errors result is slightly\n  1077:     /// // different from 0.859_872_611\n  1078:     /// assert_eq!(dur.div_f32(3.14), Duration::new(0, 859_872_580));\n  1079:     /// assert_eq!(dur.div_f32(3.14e5), Duration::new(0, 8_599));\n  1080:     /// ```\n  1081:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1082:     #[must_use = \"this returns the result of the operation, \\\n  1083:                   without modifying the original\"]\n  1084:     #[inline]\n  1085:     pub fn div_f32(self, rhs: f32) -> Duration {\n  1086:         Duration::from_secs_f32(self.as_secs_f32() / rhs)\n  1087:     }\n  1088: \n  1089:     /// Divides `Duration` by `Duration` and returns `f64`.\n  1090:     ///\n  1091:     /// # Examples\n  1092:     /// ```\n  1093:     /// use std::time::Duration;\n  1094:     ///\n  1095:     /// let dur1 = Duration::new(2, 700_000_000);\n  1096:     /// let dur2 = Duration::new(5, 400_000_000);\n  1097:     /// assert_eq!(dur1.div_duration_f64(dur2), 0.5);\n  1098:     /// ```\n  1099:     #[stable(feature = \"div_duration\", since = \"1.80.0\")]\n  1100:     #[must_use = \"this returns the result of the operation, \\\n  1101:                   without modifying the original\"]",
    "nanvix_source": "  1151:     /// // Note that this `3.14_f32` argument already has more floating-point\n  1152:     /// // representation error than a direct `3.14_f64` would, so the result\n  1153:     /// // is slightly different from the ideally rounded 0.859_872_611.\n  1154:     /// assert_eq!(dur.div_f32(3.14), Duration::new(0, 859_872_583));\n  1155:     /// assert_eq!(dur.div_f32(3.14e5), Duration::new(0, 8_599));\n  1156:     /// ```\n  1157:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1158:     #[must_use = \"this returns the result of the operation, \\\n  1159:                   without modifying the original\"]\n  1160:     #[inline]\n  1161:     pub fn div_f32(self, rhs: f32) -> Duration {\n  1162:         self.div_f64(rhs.into())\n  1163:     }\n  1164: \n  1165:     /// Divides `Duration` by `Duration` and returns `f64`.\n  1166:     ///\n  1167:     /// # Examples\n  1168:     /// ```\n  1169:     /// use std::time::Duration;\n  1170:     ///\n  1171:     /// let dur1 = Duration::new(2, 700_000_000);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::div_f64",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "div_f64",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
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
            "rhs",
            {
              "primitive": "f64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "  1046:     ///\n  1047:     /// # Panics\n  1048:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1049:     ///\n  1050:     /// # Examples\n  1051:     /// ```\n  1052:     /// use std::time::Duration;\n  1053:     ///\n  1054:     /// let dur = Duration::new(2, 700_000_000);\n  1055:     /// assert_eq!(dur.div_f64(3.14), Duration::new(0, 859_872_611));\n  1056:     /// assert_eq!(dur.div_f64(3.14e5), Duration::new(0, 8_599));\n  1057:     /// ```\n  1058:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1059:     #[must_use = \"this returns the result of the operation, \\\n  1060:                   without modifying the original\"]\n  1061:     #[inline]\n  1062:     pub fn div_f64(self, rhs: f64) -> Duration {\n  1063:         Duration::from_secs_f64(self.as_secs_f64() / rhs)\n  1064:     }\n  1065: \n  1066:     /// Divides `Duration` by `f32`.\n  1067:     ///\n  1068:     /// # Panics\n  1069:     /// This method will panic if result is negative, overflows `Duration` or not finite.\n  1070:     ///\n  1071:     /// # Examples\n  1072:     /// ```\n  1073:     /// use std::time::Duration;\n  1074:     ///\n  1075:     /// let dur = Duration::new(2, 700_000_000);\n  1076:     /// // note that due to rounding errors result is slightly\n  1077:     /// // different from 0.859_872_611\n  1078:     /// assert_eq!(dur.div_f32(3.14), Duration::new(0, 859_872_580));",
    "nanvix_source": "  1123:     ///\n  1124:     /// ```should_panic\n  1125:     /// # use std::time::Duration;\n  1126:     /// // In the extreme, rounding can even overflow `Duration`, which panics.\n  1127:     /// let _ = Duration::from_secs(u64::MAX).div_f64(1.0);\n  1128:     /// ```\n  1129:     #[stable(feature = \"duration_float\", since = \"1.38.0\")]\n  1130:     #[must_use = \"this returns the result of the operation, \\\n  1131:                   without modifying the original\"]\n  1132:     #[inline]\n  1133:     pub fn div_f64(self, rhs: f64) -> Duration {\n  1134:         Duration::from_secs_f64(self.as_secs_f64() / rhs)\n  1135:     }\n  1136: \n  1137:     /// Divides `Duration` by `f32`.\n  1138:     ///\n  1139:     /// Since the significand of `f32` is quite limited compared to the range of `Duration`\n  1140:     /// -- only about 16.8ms of exact nanosecond precision -- this method currently forwards\n  1141:     /// to [`div_f64`][Self::div_f64] for greater accuracy.\n  1142:     ///\n  1143:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::time::Duration::from_hours",
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
      "name": "from_hours",
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
            "id": 10186,
            "path": "Duration"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32378",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10186",
        "resolved_owner_path": [
          "core",
          "time",
          "Duration"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "hours",
            {
              "primitive": "u64"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 10186,
            "path": "Duration"
          }
        }
      }
    },
    "verification_source": "   406:     /// Panics if the given number of hours overflows the `Duration` size.\n   407:     ///\n   408:     /// # Examples\n   409:     ///\n   410:     /// ```\n   411:     /// use std::time::Duration;\n   412:     ///\n   413:     /// let duration = Duration::from_hours(6);\n   414:     ///\n   415:     /// assert_eq!(6 * 60 * 60, duration.as_secs());\n   416:     /// assert_eq!(0, duration.subsec_nanos());\n   417:     /// ```\n   418:     #[stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   419:     #[rustc_const_stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   420:     #[must_use]\n   421:     #[inline]\n   422:     pub const fn from_hours(hours: u64) -> Duration {\n   423:         if hours > u64::MAX / (SECS_PER_MINUTE * MINS_PER_HOUR) {\n   424:             panic!(\"overflow in Duration::from_hours\");\n   425:         }\n   426: \n   427:         Duration::from_secs(hours * MINS_PER_HOUR * SECS_PER_MINUTE)\n   428:     }\n   429: \n   430:     /// Creates a new `Duration` from the specified number of minutes.\n   431:     ///\n   432:     /// # Panics\n   433:     ///\n   434:     /// Panics if the given number of minutes overflows the `Duration` size.\n   435:     ///\n   436:     /// # Examples\n   437:     ///\n   438:     /// ```",
    "nanvix_source": "   412:     ///\n   413:     /// let duration = Duration::from_hours(6);\n   414:     ///\n   415:     /// assert_eq!(6 * 60 * 60, duration.as_secs());\n   416:     /// assert_eq!(0, duration.subsec_nanos());\n   417:     /// ```\n   418:     #[stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   419:     #[rustc_const_stable(feature = \"duration_constructors_lite\", since = \"1.91.0\")]\n   420:     #[must_use]\n   421:     #[inline]\n   422:     pub const fn from_hours(hours: u64) -> Duration {\n   423:         if hours > u64::MAX / (SECS_PER_MINUTE * MINS_PER_HOUR) {\n   424:             panic!(\"overflow in Duration::from_hours\");\n   425:         }\n   426: \n   427:         Duration::from_secs(hours * MINS_PER_HOUR * SECS_PER_MINUTE)\n   428:     }\n   429: \n   430:     /// Creates a new `Duration` from the specified number of minutes.\n   431:     ///\n   432:     /// # Panics",
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
