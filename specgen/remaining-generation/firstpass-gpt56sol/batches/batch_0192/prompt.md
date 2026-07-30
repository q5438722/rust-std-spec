For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::Metadata::is_dir",
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
      "name": "is_dir",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
    "verification_source": "  1964:     /// obtained from [`symlink_metadata`].\n  1965:     ///\n  1966:     /// # Examples\n  1967:     ///\n  1968:     /// ```no_run\n  1969:     /// fn main() -> std::io::Result<()> {\n  1970:     ///     use std::fs;\n  1971:     ///\n  1972:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1973:     ///\n  1974:     ///     assert!(!metadata.is_dir());\n  1975:     ///     Ok(())\n  1976:     /// }\n  1977:     /// ```\n  1978:     #[must_use]\n  1979:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1980:     pub fn is_dir(&self) -> bool {\n  1981:         self.file_type().is_dir()\n  1982:     }\n  1983: \n  1984:     /// Returns `true` if this metadata is for a regular file. The\n  1985:     /// result is mutually exclusive to the result of\n  1986:     /// [`Metadata::is_dir`], and will be false for symlink metadata\n  1987:     /// obtained from [`symlink_metadata`].\n  1988:     ///\n  1989:     /// When the goal is simply to read from (or write to) the source, the most\n  1990:     /// reliable way to test the source can be read (or written to) is to open\n  1991:     /// it. Only using `is_file` can break workflows like `diff <( prog_a )` on\n  1992:     /// a Unix-like system for example. See [`File::open`] or\n  1993:     /// [`OpenOptions::open`] for more information.\n  1994:     ///\n  1995:     /// # Examples\n  1996:     ///",
    "nanvix_source": "  1939:     ///     use std::fs;\n  1940:     ///\n  1941:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1942:     ///\n  1943:     ///     assert!(!metadata.is_dir());\n  1944:     ///     Ok(())\n  1945:     /// }\n  1946:     /// ```\n  1947:     #[must_use]\n  1948:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1949:     pub fn is_dir(&self) -> bool {\n  1950:         self.file_type().is_dir()\n  1951:     }\n  1952: \n  1953:     /// Returns `true` if this metadata is for a regular file. The\n  1954:     /// result is mutually exclusive to the result of\n  1955:     /// [`Metadata::is_dir`], and will be false for symlink metadata\n  1956:     /// obtained from [`symlink_metadata`].\n  1957:     ///\n  1958:     /// When the goal is simply to read from (or write to) the source, the most\n  1959:     /// reliable way to test the source can be read (or written to) is to open",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::is_file",
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
      "name": "is_file",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
    "verification_source": "  1993:     /// [`OpenOptions::open`] for more information.\n  1994:     ///\n  1995:     /// # Examples\n  1996:     ///\n  1997:     /// ```no_run\n  1998:     /// use std::fs;\n  1999:     ///\n  2000:     /// fn main() -> std::io::Result<()> {\n  2001:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2002:     ///\n  2003:     ///     assert!(metadata.is_file());\n  2004:     ///     Ok(())\n  2005:     /// }\n  2006:     /// ```\n  2007:     #[must_use]\n  2008:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2009:     pub fn is_file(&self) -> bool {\n  2010:         self.file_type().is_file()\n  2011:     }\n  2012: \n  2013:     /// Returns `true` if this metadata is for a symbolic link.\n  2014:     ///\n  2015:     /// # Examples\n  2016:     ///\n  2017:     #[cfg_attr(unix, doc = \"```no_run\")]\n  2018:     #[cfg_attr(not(unix), doc = \"```ignore\")]\n  2019:     /// use std::fs;\n  2020:     /// use std::path::Path;\n  2021:     /// use std::os::unix::fs::symlink;\n  2022:     ///\n  2023:     /// fn main() -> std::io::Result<()> {\n  2024:     ///     let link_path = Path::new(\"link\");\n  2025:     ///     symlink(\"/origin_does_not_exist/\", link_path)?;",
    "nanvix_source": "  1968:     ///\n  1969:     /// fn main() -> std::io::Result<()> {\n  1970:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  1971:     ///\n  1972:     ///     assert!(metadata.is_file());\n  1973:     ///     Ok(())\n  1974:     /// }\n  1975:     /// ```\n  1976:     #[must_use]\n  1977:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1978:     pub fn is_file(&self) -> bool {\n  1979:         self.file_type().is_file()\n  1980:     }\n  1981: \n  1982:     /// Returns `true` if this metadata is for a symbolic link.\n  1983:     ///\n  1984:     /// # Examples\n  1985:     ///\n  1986:     #[cfg_attr(unix, doc = \"```no_run\")]\n  1987:     #[cfg_attr(not(unix), doc = \"```ignore\")]\n  1988:     /// use std::fs;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::is_symlink",
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
      "name": "is_symlink",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
    "verification_source": "  2019:     /// use std::fs;\n  2020:     /// use std::path::Path;\n  2021:     /// use std::os::unix::fs::symlink;\n  2022:     ///\n  2023:     /// fn main() -> std::io::Result<()> {\n  2024:     ///     let link_path = Path::new(\"link\");\n  2025:     ///     symlink(\"/origin_does_not_exist/\", link_path)?;\n  2026:     ///\n  2027:     ///     let metadata = fs::symlink_metadata(link_path)?;\n  2028:     ///\n  2029:     ///     assert!(metadata.is_symlink());\n  2030:     ///     Ok(())\n  2031:     /// }\n  2032:     /// ```\n  2033:     #[must_use]\n  2034:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  2035:     pub fn is_symlink(&self) -> bool {\n  2036:         self.file_type().is_symlink()\n  2037:     }\n  2038: \n  2039:     /// Returns the size of the file, in bytes, this metadata is for.\n  2040:     ///\n  2041:     /// # Examples\n  2042:     ///\n  2043:     /// ```no_run\n  2044:     /// use std::fs;\n  2045:     ///\n  2046:     /// fn main() -> std::io::Result<()> {\n  2047:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2048:     ///\n  2049:     ///     assert_eq!(0, metadata.len());\n  2050:     ///     Ok(())\n  2051:     /// }",
    "nanvix_source": "  1994:     ///     symlink(\"/origin_does_not_exist/\", link_path)?;\n  1995:     ///\n  1996:     ///     let metadata = fs::symlink_metadata(link_path)?;\n  1997:     ///\n  1998:     ///     assert!(metadata.is_symlink());\n  1999:     ///     Ok(())\n  2000:     /// }\n  2001:     /// ```\n  2002:     #[must_use]\n  2003:     #[stable(feature = \"is_symlink\", since = \"1.58.0\")]\n  2004:     pub fn is_symlink(&self) -> bool {\n  2005:         self.file_type().is_symlink()\n  2006:     }\n  2007: \n  2008:     /// Returns the size of the file, in bytes, this metadata is for.\n  2009:     ///\n  2010:     /// # Examples\n  2011:     ///\n  2012:     /// ```no_run\n  2013:     /// use std::fs;\n  2014:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::len",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "  2039:     /// Returns the size of the file, in bytes, this metadata is for.\n  2040:     ///\n  2041:     /// # Examples\n  2042:     ///\n  2043:     /// ```no_run\n  2044:     /// use std::fs;\n  2045:     ///\n  2046:     /// fn main() -> std::io::Result<()> {\n  2047:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2048:     ///\n  2049:     ///     assert_eq!(0, metadata.len());\n  2050:     ///     Ok(())\n  2051:     /// }\n  2052:     /// ```\n  2053:     #[must_use]\n  2054:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2055:     pub fn len(&self) -> u64 {\n  2056:         self.0.size()\n  2057:     }\n  2058: \n  2059:     /// Returns the permissions of the file this metadata is for.\n  2060:     ///\n  2061:     /// # Examples\n  2062:     ///\n  2063:     /// ```no_run\n  2064:     /// use std::fs;\n  2065:     ///\n  2066:     /// fn main() -> std::io::Result<()> {\n  2067:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2068:     ///\n  2069:     ///     assert!(!metadata.permissions().readonly());\n  2070:     ///     Ok(())\n  2071:     /// }",
    "nanvix_source": "  2014:     ///\n  2015:     /// fn main() -> std::io::Result<()> {\n  2016:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2017:     ///\n  2018:     ///     assert_eq!(0, metadata.len());\n  2019:     ///     Ok(())\n  2020:     /// }\n  2021:     /// ```\n  2022:     #[must_use]\n  2023:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2024:     pub fn len(&self) -> u64 {\n  2025:         self.0.size()\n  2026:     }\n  2027: \n  2028:     /// Returns the permissions of the file this metadata is for.\n  2029:     ///\n  2030:     /// # Examples\n  2031:     ///\n  2032:     /// ```no_run\n  2033:     /// use std::fs;\n  2034:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::modified",
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
      "name": "modified",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
                      "resolved_path": {
                        "args": null,
                        "id": 2591,
                        "path": "SystemTime"
                      }
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
    "verification_source": "  2091:     /// ```no_run\n  2092:     /// use std::fs;\n  2093:     ///\n  2094:     /// fn main() -> std::io::Result<()> {\n  2095:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2096:     ///\n  2097:     ///     if let Ok(time) = metadata.modified() {\n  2098:     ///         println!(\"{time:?}\");\n  2099:     ///     } else {\n  2100:     ///         println!(\"Not supported on this platform\");\n  2101:     ///     }\n  2102:     ///     Ok(())\n  2103:     /// }\n  2104:     /// ```\n  2105:     #[doc(alias = \"mtime\", alias = \"ftLastWriteTime\")]\n  2106:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2107:     pub fn modified(&self) -> io::Result<SystemTime> {\n  2108:         self.0.modified().map(FromInner::from_inner)\n  2109:     }\n  2110: \n  2111:     /// Returns the last access time of this metadata.\n  2112:     ///\n  2113:     /// The returned value corresponds to the `atime` field of `stat` on Unix\n  2114:     /// platforms and the `ftLastAccessTime` field on Windows platforms.\n  2115:     ///\n  2116:     /// Note that not all platforms will keep this field update in a file's\n  2117:     /// metadata, for example Windows has an option to disable updating this\n  2118:     /// time when files are accessed and Linux similarly has `noatime`.\n  2119:     ///\n  2120:     /// # Errors\n  2121:     ///\n  2122:     /// This field might not be available on all platforms, and will return an\n  2123:     /// `Err` on platforms where it is not available.",
    "nanvix_source": "  2066:     ///     if let Ok(time) = metadata.modified() {\n  2067:     ///         println!(\"{time:?}\");\n  2068:     ///     } else {\n  2069:     ///         println!(\"Not supported on this platform\");\n  2070:     ///     }\n  2071:     ///     Ok(())\n  2072:     /// }\n  2073:     /// ```\n  2074:     #[doc(alias = \"mtime\", alias = \"ftLastWriteTime\")]\n  2075:     #[stable(feature = \"fs_time\", since = \"1.10.0\")]\n  2076:     pub fn modified(&self) -> io::Result<SystemTime> {\n  2077:         self.0.modified().map(FromInner::from_inner)\n  2078:     }\n  2079: \n  2080:     /// Returns the last access time of this metadata.\n  2081:     ///\n  2082:     /// The returned value corresponds to the `atime` field of `stat` on Unix\n  2083:     /// platforms and the `ftLastAccessTime` field on Windows platforms.\n  2084:     ///\n  2085:     /// Note that not all platforms will keep this field update in a file's\n  2086:     /// metadata, for example Windows has an option to disable updating this",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::Metadata::permissions",
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
      "name": "permissions",
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
            "id": 2584,
            "path": "Metadata"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2783",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2584",
        "resolved_owner_path": [
          "std",
          "fs",
          "Metadata"
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
            "id": 2587,
            "path": "Permissions"
          }
        }
      }
    },
    "verification_source": "  2059:     /// Returns the permissions of the file this metadata is for.\n  2060:     ///\n  2061:     /// # Examples\n  2062:     ///\n  2063:     /// ```no_run\n  2064:     /// use std::fs;\n  2065:     ///\n  2066:     /// fn main() -> std::io::Result<()> {\n  2067:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2068:     ///\n  2069:     ///     assert!(!metadata.permissions().readonly());\n  2070:     ///     Ok(())\n  2071:     /// }\n  2072:     /// ```\n  2073:     #[must_use]\n  2074:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2075:     pub fn permissions(&self) -> Permissions {\n  2076:         Permissions(self.0.perm())\n  2077:     }\n  2078: \n  2079:     /// Returns the last modification time listed in this metadata.\n  2080:     ///\n  2081:     /// The returned value corresponds to the `mtime` field of `stat` on Unix\n  2082:     /// platforms and the `ftLastWriteTime` field on Windows platforms.\n  2083:     ///\n  2084:     /// # Errors\n  2085:     ///\n  2086:     /// This field might not be available on all platforms, and will return an\n  2087:     /// `Err` on platforms where it is not available.\n  2088:     ///\n  2089:     /// # Examples\n  2090:     ///\n  2091:     /// ```no_run",
    "nanvix_source": "  2034:     ///\n  2035:     /// fn main() -> std::io::Result<()> {\n  2036:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n  2037:     ///\n  2038:     ///     assert!(!metadata.permissions().readonly());\n  2039:     ///     Ok(())\n  2040:     /// }\n  2041:     /// ```\n  2042:     #[must_use]\n  2043:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2044:     pub fn permissions(&self) -> Permissions {\n  2045:         Permissions(self.0.perm())\n  2046:     }\n  2047: \n  2048:     /// Returns the last modification time listed in this metadata.\n  2049:     ///\n  2050:     /// The returned value corresponds to the `mtime` field of `stat` on Unix\n  2051:     /// platforms and the `ftLastWriteTime` field on Windows platforms.\n  2052:     ///\n  2053:     /// # Errors\n  2054:     ///",
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
