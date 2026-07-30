For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::fd::FromRawFd::from_raw_fd",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "from_raw_fd",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2693",
        "kind": "trait",
        "name": "FromRawFd",
        "path": [
          "std",
          "os",
          "fd",
          "raw",
          "FromRawFd"
        ]
      },
      "signature": {
        "inputs": [
          [
            "fd",
            {
              "resolved_path": {
                "args": null,
                "id": 2688,
                "path": "RawFd"
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
    "verification_source": "    97:     /// ```no_run\n    98:     /// use std::fs::File;\n    99:     /// # use std::io;\n   100:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n   101:     /// use std::os::fd::{FromRawFd, IntoRawFd, RawFd};\n   102:     ///\n   103:     /// let f = File::open(\"foo.txt\")?;\n   104:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   105:     /// let raw_fd: RawFd = f.into_raw_fd();\n   106:     /// // SAFETY: no other functions should call `from_raw_fd`, so there\n   107:     /// // is only one owner for the file descriptor.\n   108:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   109:     /// let f = unsafe { File::from_raw_fd(raw_fd) };\n   110:     /// # Ok::<(), io::Error>(())\n   111:     /// ```\n   112:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   113:     unsafe fn from_raw_fd(fd: RawFd) -> Self;\n   114: }\n   115: \n   116: /// A trait to express the ability to consume an object and acquire ownership of\n   117: /// its raw file descriptor.\n   118: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   119: pub trait IntoRawFd {\n   120:     /// Consumes this object, returning the raw underlying file descriptor.\n   121:     ///\n   122:     /// This function is typically used to **transfer ownership** of the underlying\n   123:     /// file descriptor to the caller. When used in this way, callers are then the unique\n   124:     /// owners of the file descriptor and must close it once it's no longer needed.\n   125:     ///\n   126:     /// However, transferring ownership is not strictly required. Use a\n   127:     /// [`Into<OwnedFd>::into`] implementation for an API which strictly\n   128:     /// transfers ownership.\n   129:     ///",
    "nanvix_source": "   103:     /// let f = File::open(\"foo.txt\")?;\n   104:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   105:     /// let raw_fd: RawFd = f.into_raw_fd();\n   106:     /// // SAFETY: no other functions should call `from_raw_fd`, so there\n   107:     /// // is only one owner for the file descriptor.\n   108:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   109:     /// let f = unsafe { File::from_raw_fd(raw_fd) };\n   110:     /// # Ok::<(), io::Error>(())\n   111:     /// ```\n   112:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   113:     unsafe fn from_raw_fd(fd: RawFd) -> Self;\n   114: }\n   115: \n   116: /// A trait to express the ability to consume an object and acquire ownership of\n   117: /// its raw file descriptor.\n   118: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   119: pub trait IntoRawFd {\n   120:     /// Consumes this object, returning the raw underlying file descriptor.\n   121:     ///\n   122:     /// This function is typically used to **transfer ownership** of the underlying\n   123:     /// file descriptor to the caller. When used in this way, callers are then the unique",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::IntoRawFd::into_raw_fd",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "into_raw_fd",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2696",
        "kind": "trait",
        "name": "IntoRawFd",
        "path": [
          "std",
          "os",
          "fd",
          "raw",
          "IntoRawFd"
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
            "args": null,
            "id": 2688,
            "path": "RawFd"
          }
        }
      }
    },
    "verification_source": "   129:     ///\n   130:     /// # Example\n   131:     ///\n   132:     /// ```no_run\n   133:     /// use std::fs::File;\n   134:     /// # use std::io;\n   135:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n   136:     /// use std::os::fd::{IntoRawFd, RawFd};\n   137:     ///\n   138:     /// let f = File::open(\"foo.txt\")?;\n   139:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n   140:     /// let raw_fd: RawFd = f.into_raw_fd();\n   141:     /// # Ok::<(), io::Error>(())\n   142:     /// ```\n   143:     #[must_use = \"losing the raw file descriptor may leak resources\"]\n   144:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   145:     fn into_raw_fd(self) -> RawFd;\n   146: }\n   147: \n   148: #[stable(feature = \"raw_fd_reflexive_traits\", since = \"1.48.0\")]\n   149: impl AsRawFd for RawFd {\n   150:     #[inline]\n   151:     fn as_raw_fd(&self) -> RawFd {\n   152:         *self\n   153:     }\n   154: }\n   155: #[stable(feature = \"raw_fd_reflexive_traits\", since = \"1.48.0\")]\n   156: impl IntoRawFd for RawFd {\n   157:     #[inline]\n   158:     fn into_raw_fd(self) -> RawFd {\n   159:         self\n   160:     }\n   161: }",
    "nanvix_source": "   135:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n   136:     /// use std::os::fd::{IntoRawFd, RawFd};\n   137:     ///\n   138:     /// let f = File::open(\"foo.txt\")?;\n   139:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n   140:     /// let raw_fd: RawFd = f.into_raw_fd();\n   141:     /// # Ok::<(), io::Error>(())\n   142:     /// ```\n   143:     #[must_use = \"losing the raw file descriptor may leak resources\"]\n   144:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   145:     fn into_raw_fd(self) -> RawFd;\n   146: }\n   147: \n   148: #[stable(feature = \"raw_fd_reflexive_traits\", since = \"1.48.0\")]\n   149: impl AsRawFd for RawFd {\n   150:     #[inline]\n   151:     fn as_raw_fd(&self) -> RawFd {\n   152:         *self\n   153:     }\n   154: }\n   155: #[stable(feature = \"raw_fd_reflexive_traits\", since = \"1.48.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::ffi::OsStrExt::as_bytes",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "as_bytes",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2392",
        "kind": "trait",
        "name": "OsStrExt",
        "path": [
          "std",
          "os",
          "unix",
          "ffi",
          "os_str",
          "OsStrExt"
        ]
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
              "slice": {
                "primitive": "u8"
              }
            }
          }
        }
      }
    },
    "verification_source": "    25:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26:     fn into_vec(self) -> Vec<u8>;\n    27: }\n    28: \n    29: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    30: impl OsStringExt for OsString {\n    31:     #[inline]\n    32:     fn from_vec(vec: Vec<u8>) -> OsString {\n    33:         FromInner::from_inner(Buf { inner: vec })\n    34:     }\n    35:     #[inline]\n    36:     fn into_vec(self) -> Vec<u8> {\n    37:         self.into_inner().inner\n    38:     }\n    39: }\n    40: \n    41: /// Platform-specific extensions to [`OsStr`].\n    42: ///\n    43: /// This trait is sealed: it cannot be implemented outside the standard library.\n    44: /// This is so that future additional methods are not breaking changes.\n    45: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46: pub trait OsStrExt: Sealed {\n    47:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    48:     /// Creates an [`OsStr`] from a byte slice.\n    49:     ///\n    50:     /// See the module documentation for an example.\n    51:     fn from_bytes(slice: &[u8]) -> &Self;\n    52: \n    53:     /// Gets the underlying byte view of the [`OsStr`] slice.\n    54:     ///\n    55:     /// See the module documentation for an example.\n    56:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    57:     fn as_bytes(&self) -> &[u8];",
    "nanvix_source": "    24: \n    25: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26: impl OsStringExt for OsString {\n    27:     #[inline]\n    28:     fn from_vec(vec: Vec<u8>) -> OsString {\n    29:         FromInner::from_inner(Buf { inner: vec })\n    30:     }\n    31:     #[inline]\n    32:     fn into_vec(self) -> Vec<u8> {\n    33:         self.into_inner().inner\n    34:     }\n    35: }\n    36: \n    37: /// Platform-specific extensions to [`OsStr`].\n    38: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    39: pub impl(self) trait OsStrExt {\n    40:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    41:     /// Creates an [`OsStr`] from a byte slice.\n    42:     ///\n    43:     /// See the module documentation for an example.\n    44:     fn from_bytes(slice: &[u8]) -> &Self;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::ffi::OsStrExt::from_bytes",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "from_bytes",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2392",
        "kind": "trait",
        "name": "OsStrExt",
        "path": [
          "std",
          "os",
          "unix",
          "ffi",
          "os_str",
          "OsStrExt"
        ]
      },
      "signature": {
        "inputs": [
          [
            "slice",
            {
              "borrowed_ref": {
                "is_mutable": false,
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "    22:     /// Yields the underlying byte vector of this [`OsString`].\n    23:     ///\n    24:     /// See the module documentation for an example.\n    25:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26:     fn into_vec(self) -> Vec<u8>;\n    27: }\n    28: \n    29: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    30: impl OsStringExt for OsString {\n    31:     #[inline]\n    32:     fn from_vec(vec: Vec<u8>) -> OsString {\n    33:         FromInner::from_inner(Buf { inner: vec })\n    34:     }\n    35:     #[inline]\n    36:     fn into_vec(self) -> Vec<u8> {\n    37:         self.into_inner().inner\n    38:     }\n    39: }\n    40: \n    41: /// Platform-specific extensions to [`OsStr`].\n    42: ///\n    43: /// This trait is sealed: it cannot be implemented outside the standard library.\n    44: /// This is so that future additional methods are not breaking changes.\n    45: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46: pub trait OsStrExt: Sealed {\n    47:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    48:     /// Creates an [`OsStr`] from a byte slice.\n    49:     ///\n    50:     /// See the module documentation for an example.\n    51:     fn from_bytes(slice: &[u8]) -> &Self;\n    52: \n    53:     /// Gets the underlying byte view of the [`OsStr`] slice.\n    54:     ///",
    "nanvix_source": "    22:     fn into_vec(self) -> Vec<u8>;\n    23: }\n    24: \n    25: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26: impl OsStringExt for OsString {\n    27:     #[inline]\n    28:     fn from_vec(vec: Vec<u8>) -> OsString {\n    29:         FromInner::from_inner(Buf { inner: vec })\n    30:     }\n    31:     #[inline]\n    32:     fn into_vec(self) -> Vec<u8> {\n    33:         self.into_inner().inner\n    34:     }\n    35: }\n    36: \n    37: /// Platform-specific extensions to [`OsStr`].\n    38: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    39: pub impl(self) trait OsStrExt {\n    40:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    41:     /// Creates an [`OsStr`] from a byte slice.\n    42:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::ffi::OsStringExt::from_vec",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "from_vec",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2232",
        "kind": "trait",
        "name": "OsStringExt",
        "path": [
          "std",
          "os",
          "unix",
          "ffi",
          "os_str",
          "OsStringExt"
        ]
      },
      "signature": {
        "inputs": [
          [
            "vec",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "primitive": "u8"
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 222,
                "path": "Vec"
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
    "verification_source": "    17:     ///\n    18:     /// See the module documentation for an example.\n    19:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    20:     fn from_vec(vec: Vec<u8>) -> Self;\n    21: \n    22:     /// Yields the underlying byte vector of this [`OsString`].\n    23:     ///\n    24:     /// See the module documentation for an example.\n    25:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26:     fn into_vec(self) -> Vec<u8>;\n    27: }\n    28: \n    29: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    30: impl OsStringExt for OsString {\n    31:     #[inline]\n    32:     fn from_vec(vec: Vec<u8>) -> OsString {\n    33:         FromInner::from_inner(Buf { inner: vec })\n    34:     }\n    35:     #[inline]\n    36:     fn into_vec(self) -> Vec<u8> {\n    37:         self.into_inner().inner\n    38:     }\n    39: }\n    40: \n    41: /// Platform-specific extensions to [`OsStr`].\n    42: ///\n    43: /// This trait is sealed: it cannot be implemented outside the standard library.\n    44: /// This is so that future additional methods are not breaking changes.\n    45: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46: pub trait OsStrExt: Sealed {\n    47:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    48:     /// Creates an [`OsStr`] from a byte slice.\n    49:     ///",
    "nanvix_source": "    21:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    22:     fn into_vec(self) -> Vec<u8>;\n    23: }\n    24: \n    25: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26: impl OsStringExt for OsString {\n    27:     #[inline]\n    28:     fn from_vec(vec: Vec<u8>) -> OsString {\n    29:         FromInner::from_inner(Buf { inner: vec })\n    30:     }\n    31:     #[inline]\n    32:     fn into_vec(self) -> Vec<u8> {\n    33:         self.into_inner().inner\n    34:     }\n    35: }\n    36: \n    37: /// Platform-specific extensions to [`OsStr`].\n    38: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    39: pub impl(self) trait OsStrExt {\n    40:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    41:     /// Creates an [`OsStr`] from a byte slice.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::ffi::OsStringExt::into_vec",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "into_vec",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2232",
        "kind": "trait",
        "name": "OsStringExt",
        "path": [
          "std",
          "os",
          "unix",
          "ffi",
          "os_str",
          "OsStringExt"
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
                      "primitive": "u8"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 222,
            "path": "Vec"
          }
        }
      }
    },
    "verification_source": "    20:     fn from_vec(vec: Vec<u8>) -> Self;\n    21: \n    22:     /// Yields the underlying byte vector of this [`OsString`].\n    23:     ///\n    24:     /// See the module documentation for an example.\n    25:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26:     fn into_vec(self) -> Vec<u8>;\n    27: }\n    28: \n    29: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    30: impl OsStringExt for OsString {\n    31:     #[inline]\n    32:     fn from_vec(vec: Vec<u8>) -> OsString {\n    33:         FromInner::from_inner(Buf { inner: vec })\n    34:     }\n    35:     #[inline]\n    36:     fn into_vec(self) -> Vec<u8> {\n    37:         self.into_inner().inner\n    38:     }\n    39: }\n    40: \n    41: /// Platform-specific extensions to [`OsStr`].\n    42: ///\n    43: /// This trait is sealed: it cannot be implemented outside the standard library.\n    44: /// This is so that future additional methods are not breaking changes.\n    45: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46: pub trait OsStrExt: Sealed {\n    47:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    48:     /// Creates an [`OsStr`] from a byte slice.\n    49:     ///\n    50:     /// See the module documentation for an example.\n    51:     fn from_bytes(slice: &[u8]) -> &Self;\n    52: ",
    "nanvix_source": "    22:     fn into_vec(self) -> Vec<u8>;\n    23: }\n    24: \n    25: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    26: impl OsStringExt for OsString {\n    27:     #[inline]\n    28:     fn from_vec(vec: Vec<u8>) -> OsString {\n    29:         FromInner::from_inner(Buf { inner: vec })\n    30:     }\n    31:     #[inline]\n    32:     fn into_vec(self) -> Vec<u8> {\n    33:         self.into_inner().inner\n    34:     }\n    35: }\n    36: \n    37: /// Platform-specific extensions to [`OsStr`].\n    38: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    39: pub impl(self) trait OsStrExt {\n    40:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    41:     /// Creates an [`OsStr`] from a byte slice.\n    42:     ///",
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
