For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::File::try_lock",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "try_lock",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 2580,
                        "path": "TryLockError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   967:     /// use std::fs::{File, TryLockError};\n   968:     ///\n   969:     /// fn main() -> std::io::Result<()> {\n   970:     ///     let f = File::create(\"foo.txt\")?;\n   971:     ///     // Explicit handling of the WouldBlock error\n   972:     ///     match f.try_lock() {\n   973:     ///         Ok(_) => (),\n   974:     ///         Err(TryLockError::WouldBlock) => (), // Lock not acquired\n   975:     ///         Err(TryLockError::Error(err)) => return Err(err),\n   976:     ///     }\n   977:     ///     // Alternately, propagate the error as an io::Error\n   978:     ///     f.try_lock()?;\n   979:     ///     Ok(())\n   980:     /// }\n   981:     /// ```\n   982:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   983:     pub fn try_lock(&self) -> Result<(), TryLockError> {\n   984:         self.inner.try_lock()\n   985:     }\n   986: \n   987:     /// Try to acquire a shared (non-exclusive) lock on the file.\n   988:     ///\n   989:     /// Returns `Err(TryLockError::WouldBlock)` if a different lock is already held on this file\n   990:     /// (via another handle/descriptor).\n   991:     ///\n   992:     /// This acquires a shared lock; more than one file handle, in this or any other process, may\n   993:     /// hold a shared lock, but none may hold an exclusive lock at the same time.\n   994:     ///\n   995:     /// This lock may be advisory or mandatory. This lock is meant to interact with [`lock`],\n   996:     /// [`try_lock`], [`lock_shared`], [`try_lock_shared`], and [`unlock`]. Its interactions with\n   997:     /// other methods, such as [`read`] and [`write`] are platform specific, and it may or may not\n   998:     /// cause non-lockholders to block.\n   999:     ///",
    "nanvix_source": "   971:     ///         Ok(_) => (),\n   972:     ///         Err(TryLockError::WouldBlock) => (), // Lock not acquired\n   973:     ///         Err(TryLockError::Error(err)) => return Err(err),\n   974:     ///     }\n   975:     ///     // Alternately, propagate the error as an io::Error\n   976:     ///     f.try_lock()?;\n   977:     ///     Ok(())\n   978:     /// }\n   979:     /// ```\n   980:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n   981:     pub fn try_lock(&self) -> Result<(), TryLockError> {\n   982:         self.inner.try_lock()\n   983:     }\n   984: \n   985:     /// Try to acquire a shared (non-exclusive) lock on the file.\n   986:     ///\n   987:     /// Returns `Err(TryLockError::WouldBlock)` if a different lock is already held on this file\n   988:     /// (via another handle/descriptor).\n   989:     ///\n   990:     /// This acquires a shared lock; more than one file handle, in this or any other process, may\n   991:     /// hold a shared lock, but none may hold an exclusive lock at the same time.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::try_lock_shared",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "try_lock_shared",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 2580,
                        "path": "TryLockError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1031:     ///\n  1032:     /// fn main() -> std::io::Result<()> {\n  1033:     ///     let f = File::open(\"foo.txt\")?;\n  1034:     ///     // Explicit handling of the WouldBlock error\n  1035:     ///     match f.try_lock_shared() {\n  1036:     ///         Ok(_) => (),\n  1037:     ///         Err(TryLockError::WouldBlock) => (), // Lock not acquired\n  1038:     ///         Err(TryLockError::Error(err)) => return Err(err),\n  1039:     ///     }\n  1040:     ///     // Alternately, propagate the error as an io::Error\n  1041:     ///     f.try_lock_shared()?;\n  1042:     ///\n  1043:     ///     Ok(())\n  1044:     /// }\n  1045:     /// ```\n  1046:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n  1047:     pub fn try_lock_shared(&self) -> Result<(), TryLockError> {\n  1048:         self.inner.try_lock_shared()\n  1049:     }\n  1050: \n  1051:     /// Release all locks on the file.\n  1052:     ///\n  1053:     /// All locks are released when the file (along with any other file descriptors/handles\n  1054:     /// duplicated or inherited from it) is closed. This method allows releasing locks without\n  1055:     /// closing the file.\n  1056:     ///\n  1057:     /// If no lock is currently held via this file descriptor/handle, this method may return an\n  1058:     /// error, or may return successfully without taking any action.\n  1059:     ///\n  1060:     /// # Platform-specific behavior\n  1061:     ///\n  1062:     /// This function currently corresponds to the `flock` function on Unix with the `LOCK_UN` flag,\n  1063:     /// and the `UnlockFile` function on Windows. Note that, this",
    "nanvix_source": "  1035:     ///         Err(TryLockError::WouldBlock) => (), // Lock not acquired\n  1036:     ///         Err(TryLockError::Error(err)) => return Err(err),\n  1037:     ///     }\n  1038:     ///     // Alternately, propagate the error as an io::Error\n  1039:     ///     f.try_lock_shared()?;\n  1040:     ///\n  1041:     ///     Ok(())\n  1042:     /// }\n  1043:     /// ```\n  1044:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n  1045:     pub fn try_lock_shared(&self) -> Result<(), TryLockError> {\n  1046:         self.inner.try_lock_shared()\n  1047:     }\n  1048: \n  1049:     /// Release all locks on the file.\n  1050:     ///\n  1051:     /// All locks are released when the file (along with any other file descriptors/handles\n  1052:     /// duplicated or inherited from it) is closed. This method allows releasing locks without\n  1053:     /// closing the file.\n  1054:     ///\n  1055:     /// If no lock is currently held via this file descriptor/handle, this method may return an",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::unlock",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "unlock",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
                      "tuple": []
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "io::Result"
          }
        }
      }
    },
    "verification_source": "  1068:     ///\n  1069:     /// [changes]: io#platform-specific-behavior\n  1070:     ///\n  1071:     /// # Examples\n  1072:     ///\n  1073:     /// ```no_run\n  1074:     /// use std::fs::File;\n  1075:     ///\n  1076:     /// fn main() -> std::io::Result<()> {\n  1077:     ///     let f = File::open(\"foo.txt\")?;\n  1078:     ///     f.lock()?;\n  1079:     ///     f.unlock()?;\n  1080:     ///     Ok(())\n  1081:     /// }\n  1082:     /// ```\n  1083:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n  1084:     pub fn unlock(&self) -> io::Result<()> {\n  1085:         self.inner.unlock()\n  1086:     }\n  1087: \n  1088:     /// Truncates or extends the underlying file, updating the size of\n  1089:     /// this file to become `size`.\n  1090:     ///\n  1091:     /// If the `size` is less than the current file's size, then the file will\n  1092:     /// be shrunk. If it is greater than the current file's size, then the file\n  1093:     /// will be extended to `size` and have all of the intermediate data filled\n  1094:     /// in with 0s.\n  1095:     ///\n  1096:     /// The file's cursor isn't changed. In particular, if the cursor was at the\n  1097:     /// end and the file is shrunk using this operation, the cursor will now be\n  1098:     /// past the end.\n  1099:     ///\n  1100:     /// # Errors",
    "nanvix_source": "  1072:     /// use std::fs::File;\n  1073:     ///\n  1074:     /// fn main() -> std::io::Result<()> {\n  1075:     ///     let f = File::open(\"foo.txt\")?;\n  1076:     ///     f.lock()?;\n  1077:     ///     f.unlock()?;\n  1078:     ///     Ok(())\n  1079:     /// }\n  1080:     /// ```\n  1081:     #[stable(feature = \"file_lock\", since = \"1.89.0\")]\n  1082:     pub fn unlock(&self) -> io::Result<()> {\n  1083:         self.inner.unlock()\n  1084:     }\n  1085: \n  1086:     /// Truncates or extends the underlying file, updating the size of\n  1087:     /// this file to become `size`.\n  1088:     ///\n  1089:     /// If the `size` is less than the current file's size, then the file will\n  1090:     /// be shrunk. If it is greater than the current file's size, then the file\n  1091:     /// will be extended to `size` and have all of the intermediate data filled\n  1092:     /// in with 0s.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::FileTimes::new",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
            "args": null,
            "id": 2589,
            "path": "FileTimes"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2994",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2589",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileTimes"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  2203:     fn as_inner(&self) -> &fs_imp::FileAttr {\n  2204:         &self.0\n  2205:     }\n  2206: }\n  2207: \n  2208: impl FromInner<fs_imp::FileAttr> for Metadata {\n  2209:     fn from_inner(attr: fs_imp::FileAttr) -> Metadata {\n  2210:         Metadata(attr)\n  2211:     }\n  2212: }\n  2213: \n  2214: impl FileTimes {\n  2215:     /// Creates a new `FileTimes` with no times set.\n  2216:     ///\n  2217:     /// Using the resulting `FileTimes` in [`File::set_times`] will not modify any timestamps.\n  2218:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2219:     pub fn new() -> Self {\n  2220:         Self::default()\n  2221:     }\n  2222: \n  2223:     /// Set the last access time of a file.\n  2224:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2225:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2226:         self.0.set_accessed(t.into_inner());\n  2227:         self\n  2228:     }\n  2229: \n  2230:     /// Set the last modified time of a file.\n  2231:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2232:     pub fn set_modified(mut self, t: SystemTime) -> Self {\n  2233:         self.0.set_modified(t.into_inner());\n  2234:         self\n  2235:     }",
    "nanvix_source": "  2184:     fn from_inner(attr: fs_imp::FileAttr) -> Metadata {\n  2185:         Metadata(attr)\n  2186:     }\n  2187: }\n  2188: \n  2189: impl FileTimes {\n  2190:     /// Creates a new `FileTimes` with no times set.\n  2191:     ///\n  2192:     /// Using the resulting `FileTimes` in [`File::set_times`] will not modify any timestamps.\n  2193:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2194:     pub fn new() -> Self {\n  2195:         Self::default()\n  2196:     }\n  2197: \n  2198:     /// Set the last access time of a file.\n  2199:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2200:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2201:         self.0.set_accessed(t.into_inner());\n  2202:         self\n  2203:     }\n  2204: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::FileTimes::set_accessed",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "set_accessed",
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
            "id": 2589,
            "path": "FileTimes"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2994",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2589",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileTimes"
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
            "t",
            {
              "resolved_path": {
                "args": null,
                "id": 2591,
                "path": "SystemTime"
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
    "verification_source": "  2209:     fn from_inner(attr: fs_imp::FileAttr) -> Metadata {\n  2210:         Metadata(attr)\n  2211:     }\n  2212: }\n  2213: \n  2214: impl FileTimes {\n  2215:     /// Creates a new `FileTimes` with no times set.\n  2216:     ///\n  2217:     /// Using the resulting `FileTimes` in [`File::set_times`] will not modify any timestamps.\n  2218:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2219:     pub fn new() -> Self {\n  2220:         Self::default()\n  2221:     }\n  2222: \n  2223:     /// Set the last access time of a file.\n  2224:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2225:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2226:         self.0.set_accessed(t.into_inner());\n  2227:         self\n  2228:     }\n  2229: \n  2230:     /// Set the last modified time of a file.\n  2231:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2232:     pub fn set_modified(mut self, t: SystemTime) -> Self {\n  2233:         self.0.set_modified(t.into_inner());\n  2234:         self\n  2235:     }\n  2236: }\n  2237: \n  2238: impl AsInnerMut<fs_imp::FileTimes> for FileTimes {\n  2239:     fn as_inner_mut(&mut self) -> &mut fs_imp::FileTimes {\n  2240:         &mut self.0\n  2241:     }",
    "nanvix_source": "  2190:     /// Creates a new `FileTimes` with no times set.\n  2191:     ///\n  2192:     /// Using the resulting `FileTimes` in [`File::set_times`] will not modify any timestamps.\n  2193:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2194:     pub fn new() -> Self {\n  2195:         Self::default()\n  2196:     }\n  2197: \n  2198:     /// Set the last access time of a file.\n  2199:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2200:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2201:         self.0.set_accessed(t.into_inner());\n  2202:         self\n  2203:     }\n  2204: \n  2205:     /// Set the last modified time of a file.\n  2206:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2207:     pub fn set_modified(mut self, t: SystemTime) -> Self {\n  2208:         self.0.set_modified(t.into_inner());\n  2209:         self\n  2210:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::FileTimes::set_modified",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
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
      "name": "set_modified",
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
            "id": 2589,
            "path": "FileTimes"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2994",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2589",
        "resolved_owner_path": [
          "std",
          "fs",
          "FileTimes"
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
            "t",
            {
              "resolved_path": {
                "args": null,
                "id": 2591,
                "path": "SystemTime"
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
    "verification_source": "  2216:     ///\n  2217:     /// Using the resulting `FileTimes` in [`File::set_times`] will not modify any timestamps.\n  2218:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2219:     pub fn new() -> Self {\n  2220:         Self::default()\n  2221:     }\n  2222: \n  2223:     /// Set the last access time of a file.\n  2224:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2225:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2226:         self.0.set_accessed(t.into_inner());\n  2227:         self\n  2228:     }\n  2229: \n  2230:     /// Set the last modified time of a file.\n  2231:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2232:     pub fn set_modified(mut self, t: SystemTime) -> Self {\n  2233:         self.0.set_modified(t.into_inner());\n  2234:         self\n  2235:     }\n  2236: }\n  2237: \n  2238: impl AsInnerMut<fs_imp::FileTimes> for FileTimes {\n  2239:     fn as_inner_mut(&mut self) -> &mut fs_imp::FileTimes {\n  2240:         &mut self.0\n  2241:     }\n  2242: }\n  2243: \n  2244: // For implementing OS extension traits in `std::os`\n  2245: #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2246: impl Sealed for FileTimes {}\n  2247: \n  2248: impl Permissions {",
    "nanvix_source": "  2197: \n  2198:     /// Set the last access time of a file.\n  2199:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2200:     pub fn set_accessed(mut self, t: SystemTime) -> Self {\n  2201:         self.0.set_accessed(t.into_inner());\n  2202:         self\n  2203:     }\n  2204: \n  2205:     /// Set the last modified time of a file.\n  2206:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  2207:     pub fn set_modified(mut self, t: SystemTime) -> Self {\n  2208:         self.0.set_modified(t.into_inner());\n  2209:         self\n  2210:     }\n  2211: }\n  2212: \n  2213: impl AsInnerMut<fs_imp::FileTimes> for FileTimes {\n  2214:     fn as_inner_mut(&mut self) -> &mut fs_imp::FileTimes {\n  2215:         &mut self.0\n  2216:     }\n  2217: }",
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
