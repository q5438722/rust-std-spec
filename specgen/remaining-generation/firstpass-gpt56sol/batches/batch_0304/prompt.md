For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::FileTypeExt::is_block_device",
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
      "name": "is_block_device",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3095",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileTypeExt"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   891:     ///\n   892:     /// # Examples\n   893:     ///\n   894:     /// ```no_run\n   895:     /// use std::fs;\n   896:     /// use std::os::unix::fs::FileTypeExt;\n   897:     /// use std::io;\n   898:     ///\n   899:     /// fn main() -> io::Result<()> {\n   900:     ///     let meta = fs::metadata(\"block_device_file\")?;\n   901:     ///     let file_type = meta.file_type();\n   902:     ///     assert!(file_type.is_block_device());\n   903:     ///     Ok(())\n   904:     /// }\n   905:     /// ```\n   906:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   907:     fn is_block_device(&self) -> bool;\n   908:     /// Returns `true` if this file type is a char device.\n   909:     ///\n   910:     /// # Examples\n   911:     ///\n   912:     /// ```no_run\n   913:     /// use std::fs;\n   914:     /// use std::os::unix::fs::FileTypeExt;\n   915:     /// use std::io;\n   916:     ///\n   917:     /// fn main() -> io::Result<()> {\n   918:     ///     let meta = fs::metadata(\"char_device_file\")?;\n   919:     ///     let file_type = meta.file_type();\n   920:     ///     assert!(file_type.is_char_device());\n   921:     ///     Ok(())\n   922:     /// }\n   923:     /// ```",
    "nanvix_source": "   900:     /// use std::io;\n   901:     ///\n   902:     /// fn main() -> io::Result<()> {\n   903:     ///     let meta = fs::metadata(\"block_device_file\")?;\n   904:     ///     let file_type = meta.file_type();\n   905:     ///     assert!(file_type.is_block_device());\n   906:     ///     Ok(())\n   907:     /// }\n   908:     /// ```\n   909:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   910:     fn is_block_device(&self) -> bool;\n   911:     /// Returns `true` if this file type is a char device.\n   912:     ///\n   913:     /// # Examples\n   914:     ///\n   915:     /// ```no_run\n   916:     /// use std::fs;\n   917:     /// use std::os::unix::fs::FileTypeExt;\n   918:     /// use std::io;\n   919:     ///\n   920:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileTypeExt::is_char_device",
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
      "name": "is_char_device",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3095",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileTypeExt"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   909:     ///\n   910:     /// # Examples\n   911:     ///\n   912:     /// ```no_run\n   913:     /// use std::fs;\n   914:     /// use std::os::unix::fs::FileTypeExt;\n   915:     /// use std::io;\n   916:     ///\n   917:     /// fn main() -> io::Result<()> {\n   918:     ///     let meta = fs::metadata(\"char_device_file\")?;\n   919:     ///     let file_type = meta.file_type();\n   920:     ///     assert!(file_type.is_char_device());\n   921:     ///     Ok(())\n   922:     /// }\n   923:     /// ```\n   924:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   925:     fn is_char_device(&self) -> bool;\n   926:     /// Returns `true` if this file type is a fifo.\n   927:     ///\n   928:     /// # Examples\n   929:     ///\n   930:     /// ```no_run\n   931:     /// use std::fs;\n   932:     /// use std::os::unix::fs::FileTypeExt;\n   933:     /// use std::io;\n   934:     ///\n   935:     /// fn main() -> io::Result<()> {\n   936:     ///     let meta = fs::metadata(\"fifo_file\")?;\n   937:     ///     let file_type = meta.file_type();\n   938:     ///     assert!(file_type.is_fifo());\n   939:     ///     Ok(())\n   940:     /// }\n   941:     /// ```",
    "nanvix_source": "   918:     /// use std::io;\n   919:     ///\n   920:     /// fn main() -> io::Result<()> {\n   921:     ///     let meta = fs::metadata(\"char_device_file\")?;\n   922:     ///     let file_type = meta.file_type();\n   923:     ///     assert!(file_type.is_char_device());\n   924:     ///     Ok(())\n   925:     /// }\n   926:     /// ```\n   927:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   928:     fn is_char_device(&self) -> bool;\n   929:     /// Returns `true` if this file type is a fifo.\n   930:     ///\n   931:     /// # Examples\n   932:     ///\n   933:     /// ```no_run\n   934:     /// use std::fs;\n   935:     /// use std::os::unix::fs::FileTypeExt;\n   936:     /// use std::io;\n   937:     ///\n   938:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileTypeExt::is_fifo",
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
      "name": "is_fifo",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3095",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileTypeExt"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   927:     ///\n   928:     /// # Examples\n   929:     ///\n   930:     /// ```no_run\n   931:     /// use std::fs;\n   932:     /// use std::os::unix::fs::FileTypeExt;\n   933:     /// use std::io;\n   934:     ///\n   935:     /// fn main() -> io::Result<()> {\n   936:     ///     let meta = fs::metadata(\"fifo_file\")?;\n   937:     ///     let file_type = meta.file_type();\n   938:     ///     assert!(file_type.is_fifo());\n   939:     ///     Ok(())\n   940:     /// }\n   941:     /// ```\n   942:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   943:     fn is_fifo(&self) -> bool;\n   944:     /// Returns `true` if this file type is a socket.\n   945:     ///\n   946:     /// # Examples\n   947:     ///\n   948:     /// ```no_run\n   949:     /// use std::fs;\n   950:     /// use std::os::unix::fs::FileTypeExt;\n   951:     /// use std::io;\n   952:     ///\n   953:     /// fn main() -> io::Result<()> {\n   954:     ///     let meta = fs::metadata(\"unix.socket\")?;\n   955:     ///     let file_type = meta.file_type();\n   956:     ///     assert!(file_type.is_socket());\n   957:     ///     Ok(())\n   958:     /// }\n   959:     /// ```",
    "nanvix_source": "   936:     /// use std::io;\n   937:     ///\n   938:     /// fn main() -> io::Result<()> {\n   939:     ///     let meta = fs::metadata(\"fifo_file\")?;\n   940:     ///     let file_type = meta.file_type();\n   941:     ///     assert!(file_type.is_fifo());\n   942:     ///     Ok(())\n   943:     /// }\n   944:     /// ```\n   945:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   946:     fn is_fifo(&self) -> bool;\n   947:     /// Returns `true` if this file type is a socket.\n   948:     ///\n   949:     /// # Examples\n   950:     ///\n   951:     /// ```no_run\n   952:     /// use std::fs;\n   953:     /// use std::os::unix::fs::FileTypeExt;\n   954:     /// use std::io;\n   955:     ///\n   956:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::FileTypeExt::is_socket",
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
      "name": "is_socket",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3095",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "FileTypeExt"
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
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   945:     ///\n   946:     /// # Examples\n   947:     ///\n   948:     /// ```no_run\n   949:     /// use std::fs;\n   950:     /// use std::os::unix::fs::FileTypeExt;\n   951:     /// use std::io;\n   952:     ///\n   953:     /// fn main() -> io::Result<()> {\n   954:     ///     let meta = fs::metadata(\"unix.socket\")?;\n   955:     ///     let file_type = meta.file_type();\n   956:     ///     assert!(file_type.is_socket());\n   957:     ///     Ok(())\n   958:     /// }\n   959:     /// ```\n   960:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   961:     fn is_socket(&self) -> bool;\n   962: }\n   963: \n   964: #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   965: impl FileTypeExt for fs::FileType {\n   966:     fn is_block_device(&self) -> bool {\n   967:         self.as_inner().is(libc::S_IFBLK)\n   968:     }\n   969:     fn is_char_device(&self) -> bool {\n   970:         self.as_inner().is(libc::S_IFCHR)\n   971:     }\n   972:     fn is_fifo(&self) -> bool {\n   973:         self.as_inner().is(libc::S_IFIFO)\n   974:     }\n   975:     fn is_socket(&self) -> bool {\n   976:         self.as_inner().is(libc::S_IFSOCK)\n   977:     }",
    "nanvix_source": "   954:     /// use std::io;\n   955:     ///\n   956:     /// fn main() -> io::Result<()> {\n   957:     ///     let meta = fs::metadata(\"unix.socket\")?;\n   958:     ///     let file_type = meta.file_type();\n   959:     ///     assert!(file_type.is_socket());\n   960:     ///     Ok(())\n   961:     /// }\n   962:     /// ```\n   963:     #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   964:     fn is_socket(&self) -> bool;\n   965: }\n   966: \n   967: #[stable(feature = \"file_type_ext\", since = \"1.5.0\")]\n   968: impl FileTypeExt for fs::FileType {\n   969:     fn is_block_device(&self) -> bool {\n   970:         self.as_inner().is(libc::S_IFBLK)\n   971:     }\n   972:     fn is_char_device(&self) -> bool {\n   973:         self.as_inner().is(libc::S_IFCHR)\n   974:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::atime",
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
      "name": "atime",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2846",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "MetadataExt"
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
          "primitive": "i64"
        }
      }
    },
    "verification_source": "   679:     /// Returns the last access time of the file, in seconds since Unix Epoch.\n   680:     ///\n   681:     /// # Examples\n   682:     ///\n   683:     /// ```no_run\n   684:     /// use std::fs;\n   685:     /// use std::os::unix::fs::MetadataExt;\n   686:     /// use std::io;\n   687:     ///\n   688:     /// fn main() -> io::Result<()> {\n   689:     ///     let meta = fs::metadata(\"some_file\")?;\n   690:     ///     let last_access_time = meta.atime();\n   691:     ///     Ok(())\n   692:     /// }\n   693:     /// ```\n   694:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   695:     fn atime(&self) -> i64;\n   696:     /// Returns the last access time of the file, in nanoseconds since [`atime`].\n   697:     ///\n   698:     /// [`atime`]: MetadataExt::atime\n   699:     ///\n   700:     /// # Examples\n   701:     ///\n   702:     /// ```no_run\n   703:     /// use std::fs;\n   704:     /// use std::os::unix::fs::MetadataExt;\n   705:     /// use std::io;\n   706:     ///\n   707:     /// fn main() -> io::Result<()> {\n   708:     ///     let meta = fs::metadata(\"some_file\")?;\n   709:     ///     let nano_last_access_time = meta.atime_nsec();\n   710:     ///     Ok(())\n   711:     /// }",
    "nanvix_source": "   688:     /// use std::os::unix::fs::MetadataExt;\n   689:     /// use std::io;\n   690:     ///\n   691:     /// fn main() -> io::Result<()> {\n   692:     ///     let meta = fs::metadata(\"some_file\")?;\n   693:     ///     let last_access_time = meta.atime();\n   694:     ///     Ok(())\n   695:     /// }\n   696:     /// ```\n   697:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   698:     fn atime(&self) -> i64;\n   699:     /// Returns the last access time of the file, in nanoseconds since [`atime`].\n   700:     ///\n   701:     /// [`atime`]: MetadataExt::atime\n   702:     ///\n   703:     /// # Examples\n   704:     ///\n   705:     /// ```no_run\n   706:     /// use std::fs;\n   707:     /// use std::os::unix::fs::MetadataExt;\n   708:     /// use std::io;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::atime_nsec",
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
      "name": "atime_nsec",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2846",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "MetadataExt"
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
          "primitive": "i64"
        }
      }
    },
    "verification_source": "   698:     /// [`atime`]: MetadataExt::atime\n   699:     ///\n   700:     /// # Examples\n   701:     ///\n   702:     /// ```no_run\n   703:     /// use std::fs;\n   704:     /// use std::os::unix::fs::MetadataExt;\n   705:     /// use std::io;\n   706:     ///\n   707:     /// fn main() -> io::Result<()> {\n   708:     ///     let meta = fs::metadata(\"some_file\")?;\n   709:     ///     let nano_last_access_time = meta.atime_nsec();\n   710:     ///     Ok(())\n   711:     /// }\n   712:     /// ```\n   713:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   714:     fn atime_nsec(&self) -> i64;\n   715:     /// Returns the last modification time of the file, in seconds since Unix Epoch.\n   716:     ///\n   717:     /// # Examples\n   718:     ///\n   719:     /// ```no_run\n   720:     /// use std::fs;\n   721:     /// use std::os::unix::fs::MetadataExt;\n   722:     /// use std::io;\n   723:     ///\n   724:     /// fn main() -> io::Result<()> {\n   725:     ///     let meta = fs::metadata(\"some_file\")?;\n   726:     ///     let last_modification_time = meta.mtime();\n   727:     ///     Ok(())\n   728:     /// }\n   729:     /// ```\n   730:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   707:     /// use std::os::unix::fs::MetadataExt;\n   708:     /// use std::io;\n   709:     ///\n   710:     /// fn main() -> io::Result<()> {\n   711:     ///     let meta = fs::metadata(\"some_file\")?;\n   712:     ///     let nano_last_access_time = meta.atime_nsec();\n   713:     ///     Ok(())\n   714:     /// }\n   715:     /// ```\n   716:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   717:     fn atime_nsec(&self) -> i64;\n   718:     /// Returns the last modification time of the file, in seconds since Unix Epoch.\n   719:     ///\n   720:     /// # Examples\n   721:     ///\n   722:     /// ```no_run\n   723:     /// use std::fs;\n   724:     /// use std::os::unix::fs::MetadataExt;\n   725:     /// use std::io;\n   726:     ///\n   727:     /// fn main() -> io::Result<()> {",
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
