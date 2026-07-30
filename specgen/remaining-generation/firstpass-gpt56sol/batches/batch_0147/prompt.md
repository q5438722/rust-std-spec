For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::ffi::OsStr::is_ascii",
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
      "name": "is_ascii",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
    "verification_source": "  1224:     /// An empty string returns `true`.\n  1225:     ///\n  1226:     /// # Examples\n  1227:     ///\n  1228:     /// ```\n  1229:     /// use std::ffi::OsString;\n  1230:     ///\n  1231:     /// let ascii = OsString::from(\"hello!\\n\");\n  1232:     /// let non_ascii = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1233:     ///\n  1234:     /// assert!(ascii.is_ascii());\n  1235:     /// assert!(!non_ascii.is_ascii());\n  1236:     /// ```\n  1237:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1238:     #[must_use]\n  1239:     #[inline]\n  1240:     pub fn is_ascii(&self) -> bool {\n  1241:         self.inner.is_ascii()\n  1242:     }\n  1243: \n  1244:     /// Checks that two strings are an ASCII case-insensitive match.\n  1245:     ///\n  1246:     /// Same as `to_ascii_lowercase(a) == to_ascii_lowercase(b)`,\n  1247:     /// but without allocating and copying temporaries.\n  1248:     ///\n  1249:     /// # Examples\n  1250:     ///\n  1251:     /// ```\n  1252:     /// use std::ffi::OsString;\n  1253:     ///\n  1254:     /// assert!(OsString::from(\"Ferris\").eq_ignore_ascii_case(\"FERRIS\"));\n  1255:     /// assert!(OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00f6S\"));\n  1256:     /// assert!(!OsString::from(\"Ferr\u00f6s\").eq_ignore_ascii_case(\"FERR\u00d6S\"));",
    "nanvix_source": "  1277:     ///\n  1278:     /// let ascii = OsString::from(\"hello!\\n\");\n  1279:     /// let non_ascii = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1280:     ///\n  1281:     /// assert!(ascii.is_ascii());\n  1282:     /// assert!(!non_ascii.is_ascii());\n  1283:     /// ```\n  1284:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1285:     #[must_use]\n  1286:     #[inline]\n  1287:     pub fn is_ascii(&self) -> bool {\n  1288:         self.inner.is_ascii()\n  1289:     }\n  1290: \n  1291:     /// Checks that two strings are an ASCII case-insensitive match.\n  1292:     ///\n  1293:     /// Same as `to_ascii_lowercase(a) == to_ascii_lowercase(b)`,\n  1294:     /// but without allocating and copying temporaries.\n  1295:     ///\n  1296:     /// # Examples\n  1297:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::is_empty",
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
      "name": "is_empty",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
    "verification_source": "   996:     /// Checks whether the `OsStr` is empty.\n   997:     ///\n   998:     /// # Examples\n   999:     ///\n  1000:     /// ```\n  1001:     /// use std::ffi::OsStr;\n  1002:     ///\n  1003:     /// let os_str = OsStr::new(\"\");\n  1004:     /// assert!(os_str.is_empty());\n  1005:     ///\n  1006:     /// let os_str = OsStr::new(\"foo\");\n  1007:     /// assert!(!os_str.is_empty());\n  1008:     /// ```\n  1009:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1010:     #[must_use]\n  1011:     #[inline]\n  1012:     pub fn is_empty(&self) -> bool {\n  1013:         self.inner.inner.is_empty()\n  1014:     }\n  1015: \n  1016:     /// Returns the length of this `OsStr`.\n  1017:     ///\n  1018:     /// Note that this does **not** return the number of bytes in the string in\n  1019:     /// OS string form.\n  1020:     ///\n  1021:     /// The length returned is that of the underlying storage used by `OsStr`.\n  1022:     /// As discussed in the [`OsString`] introduction, [`OsString`] and `OsStr`\n  1023:     /// store strings in a form best suited for cheap inter-conversion between\n  1024:     /// native-platform and Rust string forms, which may differ significantly\n  1025:     /// from both of them, including in storage size and encoding.\n  1026:     ///\n  1027:     /// This number is simply useful for passing to other methods, like\n  1028:     /// [`OsString::with_capacity`] to avoid reallocations.",
    "nanvix_source": "   994:     ///\n   995:     /// let os_str = OsStr::new(\"\");\n   996:     /// assert!(os_str.is_empty());\n   997:     ///\n   998:     /// let os_str = OsStr::new(\"foo\");\n   999:     /// assert!(!os_str.is_empty());\n  1000:     /// ```\n  1001:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1002:     #[must_use]\n  1003:     #[inline]\n  1004:     pub fn is_empty(&self) -> bool {\n  1005:         self.inner.inner.is_empty()\n  1006:     }\n  1007: \n  1008:     /// Returns the length of this `OsStr`.\n  1009:     ///\n  1010:     /// Note that this does **not** return the number of bytes in the string in\n  1011:     /// OS string form.\n  1012:     ///\n  1013:     /// The length returned is that of the underlying storage used by `OsStr`.\n  1014:     /// As discussed in the [`OsString`] introduction, [`OsString`] and `OsStr`",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::len",
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
      "name": "len",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
    "verification_source": "  1030:     /// See the main `OsString` documentation information about encoding and capacity units.\n  1031:     ///\n  1032:     /// # Examples\n  1033:     ///\n  1034:     /// ```\n  1035:     /// use std::ffi::OsStr;\n  1036:     ///\n  1037:     /// let os_str = OsStr::new(\"\");\n  1038:     /// assert_eq!(os_str.len(), 0);\n  1039:     ///\n  1040:     /// let os_str = OsStr::new(\"foo\");\n  1041:     /// assert_eq!(os_str.len(), 3);\n  1042:     /// ```\n  1043:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1044:     #[must_use]\n  1045:     #[inline]\n  1046:     pub fn len(&self) -> usize {\n  1047:         self.inner.inner.len()\n  1048:     }\n  1049: \n  1050:     /// Converts a <code>[Box]<[OsStr]></code> into an [`OsString`] without copying or allocating.\n  1051:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n  1052:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1053:     pub fn into_os_string(self: Box<Self>) -> OsString {\n  1054:         let boxed = unsafe { Box::from_raw(Box::into_raw(self) as *mut Slice) };\n  1055:         OsString { inner: Buf::from_box(boxed) }\n  1056:     }\n  1057: \n  1058:     /// Converts an OS string slice to a byte slice.  To convert the byte slice back into an OS\n  1059:     /// string slice, use the [`OsStr::from_encoded_bytes_unchecked`] function.\n  1060:     ///\n  1061:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n  1062:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit",
    "nanvix_source": "  1028:     ///\n  1029:     /// let os_str = OsStr::new(\"\");\n  1030:     /// assert_eq!(os_str.len(), 0);\n  1031:     ///\n  1032:     /// let os_str = OsStr::new(\"foo\");\n  1033:     /// assert_eq!(os_str.len(), 3);\n  1034:     /// ```\n  1035:     #[stable(feature = \"osstring_simple_functions\", since = \"1.9.0\")]\n  1036:     #[must_use]\n  1037:     #[inline]\n  1038:     pub fn len(&self) -> usize {\n  1039:         self.inner.inner.len()\n  1040:     }\n  1041: \n  1042:     /// Converts a <code>[Box]<[OsStr]></code> into an [`OsString`] without copying or allocating.\n  1043:     #[stable(feature = \"into_boxed_os_str\", since = \"1.20.0\")]\n  1044:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1045:     pub fn into_os_string(self: Box<Self>) -> OsString {\n  1046:         let boxed = unsafe { Box::from_raw(Box::into_raw(self) as *mut Slice) };\n  1047:         OsString { inner: Buf::from_box(boxed) }\n  1048:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::make_ascii_lowercase",
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
      "name": "make_ascii_lowercase",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1133:     /// To return a new lowercased value without modifying the existing one, use\n  1134:     /// [`OsStr::to_ascii_lowercase`].\n  1135:     ///\n  1136:     /// # Examples\n  1137:     ///\n  1138:     /// ```\n  1139:     /// use std::ffi::OsString;\n  1140:     ///\n  1141:     /// let mut s = OsString::from(\"GR\u00dc\u00dfE, J\u00dcRGEN \u2764\");\n  1142:     ///\n  1143:     /// s.make_ascii_lowercase();\n  1144:     ///\n  1145:     /// assert_eq!(\"gr\u00dc\u00dfe, j\u00dcrgen \u2764\", s);\n  1146:     /// ```\n  1147:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1148:     #[inline]\n  1149:     pub fn make_ascii_lowercase(&mut self) {\n  1150:         self.inner.make_ascii_lowercase()\n  1151:     }\n  1152: \n  1153:     /// Converts this string to its ASCII upper case equivalent in-place.\n  1154:     ///\n  1155:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n  1156:     /// but non-ASCII letters are unchanged.\n  1157:     ///\n  1158:     /// To return a new uppercased value without modifying the existing one, use\n  1159:     /// [`OsStr::to_ascii_uppercase`].\n  1160:     ///\n  1161:     /// # Examples\n  1162:     ///\n  1163:     /// ```\n  1164:     /// use std::ffi::OsString;\n  1165:     ///",
    "nanvix_source": "  1186:     /// use std::ffi::OsString;\n  1187:     ///\n  1188:     /// let mut s = OsString::from(\"GR\u00dc\u00dfE, J\u00dcRGEN \u2764\");\n  1189:     ///\n  1190:     /// s.make_ascii_lowercase();\n  1191:     ///\n  1192:     /// assert_eq!(\"gr\u00dc\u00dfe, j\u00dcrgen \u2764\", s);\n  1193:     /// ```\n  1194:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1195:     #[inline]\n  1196:     pub fn make_ascii_lowercase(&mut self) {\n  1197:         self.inner.make_ascii_lowercase()\n  1198:     }\n  1199: \n  1200:     /// Converts this string to its ASCII upper case equivalent in-place.\n  1201:     ///\n  1202:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n  1203:     /// but non-ASCII letters are unchanged.\n  1204:     ///\n  1205:     /// To return a new uppercased value without modifying the existing one, use\n  1206:     /// [`OsStr::to_ascii_uppercase`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::make_ascii_uppercase",
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
      "name": "make_ascii_uppercase",
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
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1158:     /// To return a new uppercased value without modifying the existing one, use\n  1159:     /// [`OsStr::to_ascii_uppercase`].\n  1160:     ///\n  1161:     /// # Examples\n  1162:     ///\n  1163:     /// ```\n  1164:     /// use std::ffi::OsString;\n  1165:     ///\n  1166:     /// let mut s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1167:     ///\n  1168:     /// s.make_ascii_uppercase();\n  1169:     ///\n  1170:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s);\n  1171:     /// ```\n  1172:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1173:     #[inline]\n  1174:     pub fn make_ascii_uppercase(&mut self) {\n  1175:         self.inner.make_ascii_uppercase()\n  1176:     }\n  1177: \n  1178:     /// Returns a copy of this string where each character is mapped to its\n  1179:     /// ASCII lower case equivalent.\n  1180:     ///\n  1181:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n  1182:     /// but non-ASCII letters are unchanged.\n  1183:     ///\n  1184:     /// To lowercase the value in-place, use [`OsStr::make_ascii_lowercase`].\n  1185:     ///\n  1186:     /// # Examples\n  1187:     ///\n  1188:     /// ```\n  1189:     /// use std::ffi::OsString;\n  1190:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");",
    "nanvix_source": "  1211:     /// use std::ffi::OsString;\n  1212:     ///\n  1213:     /// let mut s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1214:     ///\n  1215:     /// s.make_ascii_uppercase();\n  1216:     ///\n  1217:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s);\n  1218:     /// ```\n  1219:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1220:     #[inline]\n  1221:     pub fn make_ascii_uppercase(&mut self) {\n  1222:         self.inner.make_ascii_uppercase()\n  1223:     }\n  1224: \n  1225:     /// Returns a copy of this string where each character is mapped to its\n  1226:     /// ASCII lower case equivalent.\n  1227:     ///\n  1228:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n  1229:     /// but non-ASCII letters are unchanged.\n  1230:     ///\n  1231:     /// To lowercase the value in-place, use [`OsStr::make_ascii_lowercase`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::new",
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
        "params": [
          {
            "kind": {
              "type": {
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
                                  "resolved_path": {
                                    "args": null,
                                    "id": 1857,
                                    "path": "OsStr"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 40,
                        "path": "AsRef"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 8,
                        "path": "Sized"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "S"
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
      "name": "new",
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
            "args": null,
            "id": 1857,
            "path": "OsStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2298",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1857",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "s",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "S"
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
              "resolved_path": {
                "args": null,
                "id": 1857,
                "path": "OsStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   822:     }\n   823: }\n   824: \n   825: impl OsStr {\n   826:     /// Coerces into an `OsStr` slice.\n   827:     ///\n   828:     /// # Examples\n   829:     ///\n   830:     /// ```\n   831:     /// use std::ffi::OsStr;\n   832:     ///\n   833:     /// let os_str = OsStr::new(\"foo\");\n   834:     /// ```\n   835:     #[inline]\n   836:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   837:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   838:     pub const fn new<S: [const] AsRef<OsStr> + ?Sized>(s: &S) -> &OsStr {\n   839:         s.as_ref()\n   840:     }\n   841: \n   842:     /// Converts a slice of bytes to an OS string slice without checking that the string contains\n   843:     /// valid `OsStr`-encoded data.\n   844:     ///\n   845:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   846:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   847:     /// ASCII.\n   848:     ///\n   849:     /// See the [module's toplevel documentation about conversions][conversions] for safe,\n   850:     /// cross-platform [conversions] from/to native representations.\n   851:     ///\n   852:     /// # Safety\n   853:     ///\n   854:     /// As the encoding is unspecified, callers must pass in bytes that originated as a mixture of",
    "nanvix_source": "   820:     /// # Examples\n   821:     ///\n   822:     /// ```\n   823:     /// use std::ffi::OsStr;\n   824:     ///\n   825:     /// let os_str = OsStr::new(\"foo\");\n   826:     /// ```\n   827:     #[inline]\n   828:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   829:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   830:     pub const fn new<S: [const] AsRef<OsStr> + ?Sized>(s: &S) -> &OsStr {\n   831:         s.as_ref()\n   832:     }\n   833: \n   834:     /// Converts a slice of bytes to an OS string slice without checking that the string contains\n   835:     /// valid `OsStr`-encoded data.\n   836:     ///\n   837:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   838:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   839:     /// ASCII.\n   840:     ///",
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
