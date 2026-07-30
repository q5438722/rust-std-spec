For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::ffi::OsStr::to_ascii_lowercase",
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
      "name": "to_ascii_lowercase",
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
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "  1180:     ///\n  1181:     /// ASCII letters 'A' to 'Z' are mapped to 'a' to 'z',\n  1182:     /// but non-ASCII letters are unchanged.\n  1183:     ///\n  1184:     /// To lowercase the value in-place, use [`OsStr::make_ascii_lowercase`].\n  1185:     ///\n  1186:     /// # Examples\n  1187:     ///\n  1188:     /// ```\n  1189:     /// use std::ffi::OsString;\n  1190:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1191:     ///\n  1192:     /// assert_eq!(\"gr\u00fc\u00dfe, j\u00fcrgen \u2764\", s.to_ascii_lowercase());\n  1193:     /// ```\n  1194:     #[must_use = \"to lowercase the value in-place, use `make_ascii_lowercase`\"]\n  1195:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1196:     pub fn to_ascii_lowercase(&self) -> OsString {\n  1197:         OsString::from_inner(self.inner.to_ascii_lowercase())\n  1198:     }\n  1199: \n  1200:     /// Returns a copy of this string where each character is mapped to its\n  1201:     /// ASCII upper case equivalent.\n  1202:     ///\n  1203:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n  1204:     /// but non-ASCII letters are unchanged.\n  1205:     ///\n  1206:     /// To uppercase the value in-place, use [`OsStr::make_ascii_uppercase`].\n  1207:     ///\n  1208:     /// # Examples\n  1209:     ///\n  1210:     /// ```\n  1211:     /// use std::ffi::OsString;\n  1212:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");",
    "nanvix_source": "  1233:     /// # Examples\n  1234:     ///\n  1235:     /// ```\n  1236:     /// use std::ffi::OsString;\n  1237:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1238:     ///\n  1239:     /// assert_eq!(\"gr\u00fc\u00dfe, j\u00fcrgen \u2764\", s.to_ascii_lowercase());\n  1240:     /// ```\n  1241:     #[must_use = \"to lowercase the value in-place, use `make_ascii_lowercase`\"]\n  1242:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1243:     pub fn to_ascii_lowercase(&self) -> OsString {\n  1244:         OsString::from_inner(self.inner.to_ascii_lowercase())\n  1245:     }\n  1246: \n  1247:     /// Returns a copy of this string where each character is mapped to its\n  1248:     /// ASCII upper case equivalent.\n  1249:     ///\n  1250:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n  1251:     /// but non-ASCII letters are unchanged.\n  1252:     ///\n  1253:     /// To uppercase the value in-place, use [`OsStr::make_ascii_uppercase`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::to_ascii_uppercase",
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
      "name": "to_ascii_uppercase",
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
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "  1202:     ///\n  1203:     /// ASCII letters 'a' to 'z' are mapped to 'A' to 'Z',\n  1204:     /// but non-ASCII letters are unchanged.\n  1205:     ///\n  1206:     /// To uppercase the value in-place, use [`OsStr::make_ascii_uppercase`].\n  1207:     ///\n  1208:     /// # Examples\n  1209:     ///\n  1210:     /// ```\n  1211:     /// use std::ffi::OsString;\n  1212:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1213:     ///\n  1214:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s.to_ascii_uppercase());\n  1215:     /// ```\n  1216:     #[must_use = \"to uppercase the value in-place, use `make_ascii_uppercase`\"]\n  1217:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1218:     pub fn to_ascii_uppercase(&self) -> OsString {\n  1219:         OsString::from_inner(self.inner.to_ascii_uppercase())\n  1220:     }\n  1221: \n  1222:     /// Checks if all characters in this string are within the ASCII range.\n  1223:     ///\n  1224:     /// An empty string returns `true`.\n  1225:     ///\n  1226:     /// # Examples\n  1227:     ///\n  1228:     /// ```\n  1229:     /// use std::ffi::OsString;\n  1230:     ///\n  1231:     /// let ascii = OsString::from(\"hello!\\n\");\n  1232:     /// let non_ascii = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1233:     ///\n  1234:     /// assert!(ascii.is_ascii());",
    "nanvix_source": "  1255:     /// # Examples\n  1256:     ///\n  1257:     /// ```\n  1258:     /// use std::ffi::OsString;\n  1259:     /// let s = OsString::from(\"Gr\u00fc\u00dfe, J\u00fcrgen \u2764\");\n  1260:     ///\n  1261:     /// assert_eq!(\"GR\u00fc\u00dfE, J\u00fcRGEN \u2764\", s.to_ascii_uppercase());\n  1262:     /// ```\n  1263:     #[must_use = \"to uppercase the value in-place, use `make_ascii_uppercase`\"]\n  1264:     #[stable(feature = \"osstring_ascii\", since = \"1.53.0\")]\n  1265:     pub fn to_ascii_uppercase(&self) -> OsString {\n  1266:         OsString::from_inner(self.inner.to_ascii_uppercase())\n  1267:     }\n  1268: \n  1269:     /// Checks if all characters in this string are within the ASCII range.\n  1270:     ///\n  1271:     /// An empty string returns `true`.\n  1272:     ///\n  1273:     /// # Examples\n  1274:     ///\n  1275:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::to_os_string",
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
      "name": "to_os_string",
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
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        }
      }
    },
    "verification_source": "   976:     /// Copies the slice into an owned [`OsString`].\n   977:     ///\n   978:     /// # Examples\n   979:     ///\n   980:     /// ```\n   981:     /// use std::ffi::{OsStr, OsString};\n   982:     ///\n   983:     /// let os_str = OsStr::new(\"foo\");\n   984:     /// let os_string = os_str.to_os_string();\n   985:     /// assert_eq!(os_string, OsString::from(\"foo\"));\n   986:     /// ```\n   987:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   988:     #[must_use = \"this returns the result of the operation, \\\n   989:                   without modifying the original\"]\n   990:     #[inline]\n   991:     #[cfg_attr(not(test), rustc_diagnostic_item = \"os_str_to_os_string\")]\n   992:     pub fn to_os_string(&self) -> OsString {\n   993:         OsString { inner: self.inner.to_owned() }\n   994:     }\n   995: \n   996:     /// Checks whether the `OsStr` is empty.\n   997:     ///\n   998:     /// # Examples\n   999:     ///\n  1000:     /// ```\n  1001:     /// use std::ffi::OsStr;\n  1002:     ///\n  1003:     /// let os_str = OsStr::new(\"\");\n  1004:     /// assert!(os_str.is_empty());\n  1005:     ///\n  1006:     /// let os_str = OsStr::new(\"foo\");\n  1007:     /// assert!(!os_str.is_empty());\n  1008:     /// ```",
    "nanvix_source": "   974:     ///\n   975:     /// let os_str = OsStr::new(\"foo\");\n   976:     /// let os_string = os_str.to_os_string();\n   977:     /// assert_eq!(os_string, OsString::from(\"foo\"));\n   978:     /// ```\n   979:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   980:     #[must_use = \"this returns the result of the operation, \\\n   981:                   without modifying the original\"]\n   982:     #[inline]\n   983:     #[cfg_attr(not(test), rustc_diagnostic_item = \"os_str_to_os_string\")]\n   984:     pub fn to_os_string(&self) -> OsString {\n   985:         OsString { inner: self.inner.to_owned() }\n   986:     }\n   987: \n   988:     /// Checks whether the `OsStr` is empty.\n   989:     ///\n   990:     /// # Examples\n   991:     ///\n   992:     /// ```\n   993:     /// use std::ffi::OsStr;\n   994:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::to_str",
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
      "name": "to_str",
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
                          "primitive": "str"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "   903:     /// Yields a <code>&[str]</code> slice if the `OsStr` is valid Unicode.\n   904:     ///\n   905:     /// This conversion may entail doing a check for UTF-8 validity.\n   906:     ///\n   907:     /// # Examples\n   908:     ///\n   909:     /// ```\n   910:     /// use std::ffi::OsStr;\n   911:     ///\n   912:     /// let os_str = OsStr::new(\"foo\");\n   913:     /// assert_eq!(os_str.to_str(), Some(\"foo\"));\n   914:     /// ```\n   915:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   916:     #[must_use = \"this returns the result of the operation, \\\n   917:                   without modifying the original\"]\n   918:     #[inline]\n   919:     pub fn to_str(&self) -> Option<&str> {\n   920:         self.inner.to_str().ok()\n   921:     }\n   922: \n   923:     /// Converts an `OsStr` to a <code>[Cow]<[str]></code>.\n   924:     ///\n   925:     /// Any non-UTF-8 sequences are replaced with\n   926:     /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD].\n   927:     ///\n   928:     /// [U+FFFD]: crate::char::REPLACEMENT_CHARACTER\n   929:     ///\n   930:     /// # Examples\n   931:     ///\n   932:     /// Calling `to_string_lossy` on an `OsStr` with invalid unicode:\n   933:     ///\n   934:     /// ```\n   935:     /// // Note, due to differences in how Unix and Windows represent strings,",
    "nanvix_source": "   901:     /// ```\n   902:     /// use std::ffi::OsStr;\n   903:     ///\n   904:     /// let os_str = OsStr::new(\"foo\");\n   905:     /// assert_eq!(os_str.to_str(), Some(\"foo\"));\n   906:     /// ```\n   907:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   908:     #[must_use = \"this returns the result of the operation, \\\n   909:                   without modifying the original\"]\n   910:     #[inline]\n   911:     pub fn to_str(&self) -> Option<&str> {\n   912:         self.inner.to_str().ok()\n   913:     }\n   914: \n   915:     /// Converts an `OsStr` to a <code>[Cow]<[str]></code>.\n   916:     ///\n   917:     /// Any non-UTF-8 sequences are replaced with\n   918:     /// [`U+FFFD REPLACEMENT CHARACTER`][U+FFFD].\n   919:     ///\n   920:     /// [U+FFFD]: crate::char::REPLACEMENT_CHARACTER\n   921:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsStr::to_string_lossy",
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
      "name": "to_string_lossy",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "primitive": "str"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 2178,
            "path": "Cow"
          }
        }
      }
    },
    "verification_source": "   956:     ///     use std::os::windows::prelude::*;\n   957:     ///\n   958:     ///     // Here the values 0x0066 and 0x006f correspond to 'f' and 'o'\n   959:     ///     // respectively. The value 0xD800 is a lone surrogate half, invalid\n   960:     ///     // in a UTF-16 sequence.\n   961:     ///     let source = [0x0066, 0x006f, 0xD800, 0x006f];\n   962:     ///     let os_string = OsString::from_wide(&source[..]);\n   963:     ///     let os_str = os_string.as_os_str();\n   964:     ///\n   965:     ///     assert_eq!(os_str.to_string_lossy(), \"fo\ufffdo\");\n   966:     /// }\n   967:     /// ```\n   968:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   969:     #[must_use = \"this returns the result of the operation, \\\n   970:                   without modifying the original\"]\n   971:     #[inline]\n   972:     pub fn to_string_lossy(&self) -> Cow<'_, str> {\n   973:         self.inner.to_string_lossy()\n   974:     }\n   975: \n   976:     /// Copies the slice into an owned [`OsString`].\n   977:     ///\n   978:     /// # Examples\n   979:     ///\n   980:     /// ```\n   981:     /// use std::ffi::{OsStr, OsString};\n   982:     ///\n   983:     /// let os_str = OsStr::new(\"foo\");\n   984:     /// let os_string = os_str.to_os_string();\n   985:     /// assert_eq!(os_string, OsString::from(\"foo\"));\n   986:     /// ```\n   987:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   988:     #[must_use = \"this returns the result of the operation, \\",
    "nanvix_source": "   954:     ///     let os_string = OsString::from_wide(&source[..]);\n   955:     ///     let os_str = os_string.as_os_str();\n   956:     ///\n   957:     ///     assert_eq!(os_str.to_string_lossy(), \"fo\ufffdo\");\n   958:     /// }\n   959:     /// ```\n   960:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   961:     #[must_use = \"this returns the result of the operation, \\\n   962:                   without modifying the original\"]\n   963:     #[inline]\n   964:     pub fn to_string_lossy(&self) -> Cow<'_, str> {\n   965:         self.inner.to_string_lossy()\n   966:     }\n   967: \n   968:     /// Copies the slice into an owned [`OsString`].\n   969:     ///\n   970:     /// # Examples\n   971:     ///\n   972:     /// ```\n   973:     /// use std::ffi::{OsStr, OsString};\n   974:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::as_os_str",
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
      "name": "as_os_str",
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
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
    "verification_source": "   187: \n   188:     /// Converts to an [`OsStr`] slice.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```\n   193:     /// use std::ffi::{OsString, OsStr};\n   194:     ///\n   195:     /// let os_string = OsString::from(\"foo\");\n   196:     /// let os_str = OsStr::new(\"foo\");\n   197:     /// assert_eq!(os_string.as_os_str(), os_str);\n   198:     /// ```\n   199:     #[cfg_attr(not(test), rustc_diagnostic_item = \"os_string_as_os_str\")]\n   200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   201:     #[must_use]\n   202:     #[inline]\n   203:     pub fn as_os_str(&self) -> &OsStr {\n   204:         self\n   205:     }\n   206: \n   207:     /// Converts the `OsString` into a byte vector.  To convert the byte vector back into an\n   208:     /// `OsString`, use the [`OsString::from_encoded_bytes_unchecked`] function.\n   209:     ///\n   210:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   211:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   212:     /// ASCII.\n   213:     ///\n   214:     /// Note: As the encoding is unspecified, any sub-slice of bytes that is not valid UTF-8 should\n   215:     /// be treated as opaque and only comparable within the same Rust version built for the same\n   216:     /// target platform.  For example, sending the bytes over the network or storing it in a file\n   217:     /// will likely result in incompatible data.  See [`OsString`] for more encoding details\n   218:     /// and [`std::ffi`] for platform-specific, specified conversions.\n   219:     ///",
    "nanvix_source": "   185:     /// use std::ffi::{OsString, OsStr};\n   186:     ///\n   187:     /// let os_string = OsString::from(\"foo\");\n   188:     /// let os_str = OsStr::new(\"foo\");\n   189:     /// assert_eq!(os_string.as_os_str(), os_str);\n   190:     /// ```\n   191:     #[cfg_attr(not(test), rustc_diagnostic_item = \"os_string_as_os_str\")]\n   192:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   193:     #[must_use]\n   194:     #[inline]\n   195:     pub fn as_os_str(&self) -> &OsStr {\n   196:         self\n   197:     }\n   198: \n   199:     /// Converts the `OsString` into a byte vector.  To convert the byte vector back into an\n   200:     /// `OsString`, use the [`OsString::from_encoded_bytes_unchecked`] function.\n   201:     ///\n   202:     /// The byte encoding is an unspecified, platform-specific, self-synchronizing superset of UTF-8.\n   203:     /// By being a self-synchronizing superset of UTF-8, this encoding is also a superset of 7-bit\n   204:     /// ASCII.\n   205:     ///",
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
