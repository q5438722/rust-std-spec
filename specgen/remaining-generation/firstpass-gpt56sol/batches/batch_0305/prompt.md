For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::MetadataExt::blksize",
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
      "name": "blksize",
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   787:     /// Returns the block size for filesystem I/O.\n   788:     ///\n   789:     /// # Examples\n   790:     ///\n   791:     /// ```no_run\n   792:     /// use std::fs;\n   793:     /// use std::os::unix::fs::MetadataExt;\n   794:     /// use std::io;\n   795:     ///\n   796:     /// fn main() -> io::Result<()> {\n   797:     ///     let meta = fs::metadata(\"some_file\")?;\n   798:     ///     let block_size = meta.blksize();\n   799:     ///     Ok(())\n   800:     /// }\n   801:     /// ```\n   802:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   803:     fn blksize(&self) -> u64;\n   804:     /// Returns the number of blocks allocated to the file, in 512-byte units.\n   805:     ///\n   806:     /// Please note that this may be smaller than `st_size / 512` when the file has holes.\n   807:     ///\n   808:     /// # Examples\n   809:     ///\n   810:     /// ```no_run\n   811:     /// use std::fs;\n   812:     /// use std::os::unix::fs::MetadataExt;\n   813:     /// use std::io;\n   814:     ///\n   815:     /// fn main() -> io::Result<()> {\n   816:     ///     let meta = fs::metadata(\"some_file\")?;\n   817:     ///     let blocks = meta.blocks();\n   818:     ///     Ok(())\n   819:     /// }",
    "nanvix_source": "   796:     /// use std::os::unix::fs::MetadataExt;\n   797:     /// use std::io;\n   798:     ///\n   799:     /// fn main() -> io::Result<()> {\n   800:     ///     let meta = fs::metadata(\"some_file\")?;\n   801:     ///     let block_size = meta.blksize();\n   802:     ///     Ok(())\n   803:     /// }\n   804:     /// ```\n   805:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   806:     fn blksize(&self) -> u64;\n   807:     /// Returns the number of blocks allocated to the file, in 512-byte units.\n   808:     ///\n   809:     /// Please note that this may be smaller than `st_size / 512` when the file has holes.\n   810:     ///\n   811:     /// # Examples\n   812:     ///\n   813:     /// ```no_run\n   814:     /// use std::fs;\n   815:     /// use std::os::unix::fs::MetadataExt;\n   816:     /// use std::io;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::blocks",
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
      "name": "blocks",
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   806:     /// Please note that this may be smaller than `st_size / 512` when the file has holes.\n   807:     ///\n   808:     /// # Examples\n   809:     ///\n   810:     /// ```no_run\n   811:     /// use std::fs;\n   812:     /// use std::os::unix::fs::MetadataExt;\n   813:     /// use std::io;\n   814:     ///\n   815:     /// fn main() -> io::Result<()> {\n   816:     ///     let meta = fs::metadata(\"some_file\")?;\n   817:     ///     let blocks = meta.blocks();\n   818:     ///     Ok(())\n   819:     /// }\n   820:     /// ```\n   821:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   822:     fn blocks(&self) -> u64;\n   823:     #[cfg(target_os = \"vxworks\")]\n   824:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   825:     fn attrib(&self) -> u8;\n   826: }\n   827: \n   828: #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   829: impl MetadataExt for fs::Metadata {\n   830:     fn dev(&self) -> u64 {\n   831:         self.st_dev()\n   832:     }\n   833:     fn ino(&self) -> u64 {\n   834:         self.st_ino()\n   835:     }\n   836:     fn mode(&self) -> u32 {\n   837:         self.st_mode()\n   838:     }",
    "nanvix_source": "   815:     /// use std::os::unix::fs::MetadataExt;\n   816:     /// use std::io;\n   817:     ///\n   818:     /// fn main() -> io::Result<()> {\n   819:     ///     let meta = fs::metadata(\"some_file\")?;\n   820:     ///     let blocks = meta.blocks();\n   821:     ///     Ok(())\n   822:     /// }\n   823:     /// ```\n   824:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   825:     fn blocks(&self) -> u64;\n   826:     #[cfg(target_os = \"vxworks\")]\n   827:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   828:     fn attrib(&self) -> u8;\n   829: }\n   830: \n   831: #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   832: impl MetadataExt for fs::Metadata {\n   833:     fn dev(&self) -> u64 {\n   834:         self.st_dev()\n   835:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::ctime",
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
      "name": "ctime",
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
    "verification_source": "   751:     /// Returns the last status change time of the file, in seconds since Unix Epoch.\n   752:     ///\n   753:     /// # Examples\n   754:     ///\n   755:     /// ```no_run\n   756:     /// use std::fs;\n   757:     /// use std::os::unix::fs::MetadataExt;\n   758:     /// use std::io;\n   759:     ///\n   760:     /// fn main() -> io::Result<()> {\n   761:     ///     let meta = fs::metadata(\"some_file\")?;\n   762:     ///     let last_status_change_time = meta.ctime();\n   763:     ///     Ok(())\n   764:     /// }\n   765:     /// ```\n   766:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   767:     fn ctime(&self) -> i64;\n   768:     /// Returns the last status change time of the file, in nanoseconds since [`ctime`].\n   769:     ///\n   770:     /// [`ctime`]: MetadataExt::ctime\n   771:     ///\n   772:     /// # Examples\n   773:     ///\n   774:     /// ```no_run\n   775:     /// use std::fs;\n   776:     /// use std::os::unix::fs::MetadataExt;\n   777:     /// use std::io;\n   778:     ///\n   779:     /// fn main() -> io::Result<()> {\n   780:     ///     let meta = fs::metadata(\"some_file\")?;\n   781:     ///     let nano_last_status_change_time = meta.ctime_nsec();\n   782:     ///     Ok(())\n   783:     /// }",
    "nanvix_source": "   760:     /// use std::os::unix::fs::MetadataExt;\n   761:     /// use std::io;\n   762:     ///\n   763:     /// fn main() -> io::Result<()> {\n   764:     ///     let meta = fs::metadata(\"some_file\")?;\n   765:     ///     let last_status_change_time = meta.ctime();\n   766:     ///     Ok(())\n   767:     /// }\n   768:     /// ```\n   769:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   770:     fn ctime(&self) -> i64;\n   771:     /// Returns the last status change time of the file, in nanoseconds since [`ctime`].\n   772:     ///\n   773:     /// [`ctime`]: MetadataExt::ctime\n   774:     ///\n   775:     /// # Examples\n   776:     ///\n   777:     /// ```no_run\n   778:     /// use std::fs;\n   779:     /// use std::os::unix::fs::MetadataExt;\n   780:     /// use std::io;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::ctime_nsec",
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
      "name": "ctime_nsec",
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
    "verification_source": "   770:     /// [`ctime`]: MetadataExt::ctime\n   771:     ///\n   772:     /// # Examples\n   773:     ///\n   774:     /// ```no_run\n   775:     /// use std::fs;\n   776:     /// use std::os::unix::fs::MetadataExt;\n   777:     /// use std::io;\n   778:     ///\n   779:     /// fn main() -> io::Result<()> {\n   780:     ///     let meta = fs::metadata(\"some_file\")?;\n   781:     ///     let nano_last_status_change_time = meta.ctime_nsec();\n   782:     ///     Ok(())\n   783:     /// }\n   784:     /// ```\n   785:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   786:     fn ctime_nsec(&self) -> i64;\n   787:     /// Returns the block size for filesystem I/O.\n   788:     ///\n   789:     /// # Examples\n   790:     ///\n   791:     /// ```no_run\n   792:     /// use std::fs;\n   793:     /// use std::os::unix::fs::MetadataExt;\n   794:     /// use std::io;\n   795:     ///\n   796:     /// fn main() -> io::Result<()> {\n   797:     ///     let meta = fs::metadata(\"some_file\")?;\n   798:     ///     let block_size = meta.blksize();\n   799:     ///     Ok(())\n   800:     /// }\n   801:     /// ```\n   802:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   779:     /// use std::os::unix::fs::MetadataExt;\n   780:     /// use std::io;\n   781:     ///\n   782:     /// fn main() -> io::Result<()> {\n   783:     ///     let meta = fs::metadata(\"some_file\")?;\n   784:     ///     let nano_last_status_change_time = meta.ctime_nsec();\n   785:     ///     Ok(())\n   786:     /// }\n   787:     /// ```\n   788:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   789:     fn ctime_nsec(&self) -> i64;\n   790:     /// Returns the block size for filesystem I/O.\n   791:     ///\n   792:     /// # Examples\n   793:     ///\n   794:     /// ```no_run\n   795:     /// use std::fs;\n   796:     /// use std::os::unix::fs::MetadataExt;\n   797:     /// use std::io;\n   798:     ///\n   799:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::dev",
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
      "name": "dev",
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   539:     /// Returns the ID of the device containing the file.\n   540:     ///\n   541:     /// # Examples\n   542:     ///\n   543:     /// ```no_run\n   544:     /// use std::io;\n   545:     /// use std::fs;\n   546:     /// use std::os::unix::fs::MetadataExt;\n   547:     ///\n   548:     /// fn main() -> io::Result<()> {\n   549:     ///     let meta = fs::metadata(\"some_file\")?;\n   550:     ///     let dev_id = meta.dev();\n   551:     ///     Ok(())\n   552:     /// }\n   553:     /// ```\n   554:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   555:     fn dev(&self) -> u64;\n   556:     /// Returns the inode number.\n   557:     ///\n   558:     /// # Examples\n   559:     ///\n   560:     /// ```no_run\n   561:     /// use std::fs;\n   562:     /// use std::os::unix::fs::MetadataExt;\n   563:     /// use std::io;\n   564:     ///\n   565:     /// fn main() -> io::Result<()> {\n   566:     ///     let meta = fs::metadata(\"some_file\")?;\n   567:     ///     let inode = meta.ino();\n   568:     ///     Ok(())\n   569:     /// }\n   570:     /// ```\n   571:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   548:     /// use std::fs;\n   549:     /// use std::os::unix::fs::MetadataExt;\n   550:     ///\n   551:     /// fn main() -> io::Result<()> {\n   552:     ///     let meta = fs::metadata(\"some_file\")?;\n   553:     ///     let dev_id = meta.dev();\n   554:     ///     Ok(())\n   555:     /// }\n   556:     /// ```\n   557:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   558:     fn dev(&self) -> u64;\n   559:     /// Returns the inode number.\n   560:     ///\n   561:     /// # Examples\n   562:     ///\n   563:     /// ```no_run\n   564:     /// use std::fs;\n   565:     /// use std::os::unix::fs::MetadataExt;\n   566:     /// use std::io;\n   567:     ///\n   568:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::gid",
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
      "name": "gid",
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "   628:     /// Returns the group ID of the owner of this file.\n   629:     ///\n   630:     /// # Examples\n   631:     ///\n   632:     /// ```no_run\n   633:     /// use std::fs;\n   634:     /// use std::os::unix::fs::MetadataExt;\n   635:     /// use std::io;\n   636:     ///\n   637:     /// fn main() -> io::Result<()> {\n   638:     ///     let meta = fs::metadata(\"some_file\")?;\n   639:     ///     let group_id = meta.gid();\n   640:     ///     Ok(())\n   641:     /// }\n   642:     /// ```\n   643:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   644:     fn gid(&self) -> u32;\n   645:     /// Returns the device ID of this file (if it is a special one).\n   646:     ///\n   647:     /// # Examples\n   648:     ///\n   649:     /// ```no_run\n   650:     /// use std::fs;\n   651:     /// use std::os::unix::fs::MetadataExt;\n   652:     /// use std::io;\n   653:     ///\n   654:     /// fn main() -> io::Result<()> {\n   655:     ///     let meta = fs::metadata(\"some_file\")?;\n   656:     ///     let device_id = meta.rdev();\n   657:     ///     Ok(())\n   658:     /// }\n   659:     /// ```\n   660:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   637:     /// use std::os::unix::fs::MetadataExt;\n   638:     /// use std::io;\n   639:     ///\n   640:     /// fn main() -> io::Result<()> {\n   641:     ///     let meta = fs::metadata(\"some_file\")?;\n   642:     ///     let group_id = meta.gid();\n   643:     ///     Ok(())\n   644:     /// }\n   645:     /// ```\n   646:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   647:     fn gid(&self) -> u32;\n   648:     /// Returns the device ID of this file (if it is a special one).\n   649:     ///\n   650:     /// # Examples\n   651:     ///\n   652:     /// ```no_run\n   653:     /// use std::fs;\n   654:     /// use std::os::unix::fs::MetadataExt;\n   655:     /// use std::io;\n   656:     ///\n   657:     /// fn main() -> io::Result<()> {",
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
