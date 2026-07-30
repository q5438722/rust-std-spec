For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::MetadataExt::ino",
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
      "name": "ino",
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
    "verification_source": "   556:     /// Returns the inode number.\n   557:     ///\n   558:     /// # Examples\n   559:     ///\n   560:     /// ```no_run\n   561:     /// use std::fs;\n   562:     /// use std::os::unix::fs::MetadataExt;\n   563:     /// use std::io;\n   564:     ///\n   565:     /// fn main() -> io::Result<()> {\n   566:     ///     let meta = fs::metadata(\"some_file\")?;\n   567:     ///     let inode = meta.ino();\n   568:     ///     Ok(())\n   569:     /// }\n   570:     /// ```\n   571:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   572:     fn ino(&self) -> u64;\n   573:     /// Returns the rights applied to this file.\n   574:     ///\n   575:     /// # Examples\n   576:     ///\n   577:     /// ```no_run\n   578:     /// use std::fs;\n   579:     /// use std::os::unix::fs::MetadataExt;\n   580:     /// use std::io;\n   581:     ///\n   582:     /// fn main() -> io::Result<()> {\n   583:     ///     let meta = fs::metadata(\"some_file\")?;\n   584:     ///     let mode = meta.mode();\n   585:     ///     let user_has_write_access      = mode & 0o200;\n   586:     ///     let user_has_read_write_access = mode & 0o600;\n   587:     ///     let group_has_read_access      = mode & 0o040;\n   588:     ///     let others_have_exec_access    = mode & 0o001;",
    "nanvix_source": "   565:     /// use std::os::unix::fs::MetadataExt;\n   566:     /// use std::io;\n   567:     ///\n   568:     /// fn main() -> io::Result<()> {\n   569:     ///     let meta = fs::metadata(\"some_file\")?;\n   570:     ///     let inode = meta.ino();\n   571:     ///     Ok(())\n   572:     /// }\n   573:     /// ```\n   574:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   575:     fn ino(&self) -> u64;\n   576:     /// Returns the rights applied to this file.\n   577:     ///\n   578:     /// # Examples\n   579:     ///\n   580:     /// ```no_run\n   581:     /// use std::fs;\n   582:     /// use std::os::unix::fs::MetadataExt;\n   583:     /// use std::io;\n   584:     ///\n   585:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::mode",
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
      "name": "mode",
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
    "verification_source": "   577:     /// ```no_run\n   578:     /// use std::fs;\n   579:     /// use std::os::unix::fs::MetadataExt;\n   580:     /// use std::io;\n   581:     ///\n   582:     /// fn main() -> io::Result<()> {\n   583:     ///     let meta = fs::metadata(\"some_file\")?;\n   584:     ///     let mode = meta.mode();\n   585:     ///     let user_has_write_access      = mode & 0o200;\n   586:     ///     let user_has_read_write_access = mode & 0o600;\n   587:     ///     let group_has_read_access      = mode & 0o040;\n   588:     ///     let others_have_exec_access    = mode & 0o001;\n   589:     ///     Ok(())\n   590:     /// }\n   591:     /// ```\n   592:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   593:     fn mode(&self) -> u32;\n   594:     /// Returns the number of hard links pointing to this file.\n   595:     ///\n   596:     /// # Examples\n   597:     ///\n   598:     /// ```no_run\n   599:     /// use std::fs;\n   600:     /// use std::os::unix::fs::MetadataExt;\n   601:     /// use std::io;\n   602:     ///\n   603:     /// fn main() -> io::Result<()> {\n   604:     ///     let meta = fs::metadata(\"some_file\")?;\n   605:     ///     let nb_hard_links = meta.nlink();\n   606:     ///     Ok(())\n   607:     /// }\n   608:     /// ```\n   609:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   586:     ///     let meta = fs::metadata(\"some_file\")?;\n   587:     ///     let mode = meta.mode();\n   588:     ///     let user_has_write_access      = mode & 0o200;\n   589:     ///     let user_has_read_write_access = mode & 0o600;\n   590:     ///     let group_has_read_access      = mode & 0o040;\n   591:     ///     let others_have_exec_access    = mode & 0o001;\n   592:     ///     Ok(())\n   593:     /// }\n   594:     /// ```\n   595:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   596:     fn mode(&self) -> u32;\n   597:     /// Returns the number of hard links pointing to this file.\n   598:     ///\n   599:     /// # Examples\n   600:     ///\n   601:     /// ```no_run\n   602:     /// use std::fs;\n   603:     /// use std::os::unix::fs::MetadataExt;\n   604:     /// use std::io;\n   605:     ///\n   606:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::mtime",
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
      "name": "mtime",
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
    "verification_source": "   715:     /// Returns the last modification time of the file, in seconds since Unix Epoch.\n   716:     ///\n   717:     /// # Examples\n   718:     ///\n   719:     /// ```no_run\n   720:     /// use std::fs;\n   721:     /// use std::os::unix::fs::MetadataExt;\n   722:     /// use std::io;\n   723:     ///\n   724:     /// fn main() -> io::Result<()> {\n   725:     ///     let meta = fs::metadata(\"some_file\")?;\n   726:     ///     let last_modification_time = meta.mtime();\n   727:     ///     Ok(())\n   728:     /// }\n   729:     /// ```\n   730:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   731:     fn mtime(&self) -> i64;\n   732:     /// Returns the last modification time of the file, in nanoseconds since [`mtime`].\n   733:     ///\n   734:     /// [`mtime`]: MetadataExt::mtime\n   735:     ///\n   736:     /// # Examples\n   737:     ///\n   738:     /// ```no_run\n   739:     /// use std::fs;\n   740:     /// use std::os::unix::fs::MetadataExt;\n   741:     /// use std::io;\n   742:     ///\n   743:     /// fn main() -> io::Result<()> {\n   744:     ///     let meta = fs::metadata(\"some_file\")?;\n   745:     ///     let nano_last_modification_time = meta.mtime_nsec();\n   746:     ///     Ok(())\n   747:     /// }",
    "nanvix_source": "   724:     /// use std::os::unix::fs::MetadataExt;\n   725:     /// use std::io;\n   726:     ///\n   727:     /// fn main() -> io::Result<()> {\n   728:     ///     let meta = fs::metadata(\"some_file\")?;\n   729:     ///     let last_modification_time = meta.mtime();\n   730:     ///     Ok(())\n   731:     /// }\n   732:     /// ```\n   733:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   734:     fn mtime(&self) -> i64;\n   735:     /// Returns the last modification time of the file, in nanoseconds since [`mtime`].\n   736:     ///\n   737:     /// [`mtime`]: MetadataExt::mtime\n   738:     ///\n   739:     /// # Examples\n   740:     ///\n   741:     /// ```no_run\n   742:     /// use std::fs;\n   743:     /// use std::os::unix::fs::MetadataExt;\n   744:     /// use std::io;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::mtime_nsec",
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
      "name": "mtime_nsec",
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
    "verification_source": "   734:     /// [`mtime`]: MetadataExt::mtime\n   735:     ///\n   736:     /// # Examples\n   737:     ///\n   738:     /// ```no_run\n   739:     /// use std::fs;\n   740:     /// use std::os::unix::fs::MetadataExt;\n   741:     /// use std::io;\n   742:     ///\n   743:     /// fn main() -> io::Result<()> {\n   744:     ///     let meta = fs::metadata(\"some_file\")?;\n   745:     ///     let nano_last_modification_time = meta.mtime_nsec();\n   746:     ///     Ok(())\n   747:     /// }\n   748:     /// ```\n   749:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   750:     fn mtime_nsec(&self) -> i64;\n   751:     /// Returns the last status change time of the file, in seconds since Unix Epoch.\n   752:     ///\n   753:     /// # Examples\n   754:     ///\n   755:     /// ```no_run\n   756:     /// use std::fs;\n   757:     /// use std::os::unix::fs::MetadataExt;\n   758:     /// use std::io;\n   759:     ///\n   760:     /// fn main() -> io::Result<()> {\n   761:     ///     let meta = fs::metadata(\"some_file\")?;\n   762:     ///     let last_status_change_time = meta.ctime();\n   763:     ///     Ok(())\n   764:     /// }\n   765:     /// ```\n   766:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   743:     /// use std::os::unix::fs::MetadataExt;\n   744:     /// use std::io;\n   745:     ///\n   746:     /// fn main() -> io::Result<()> {\n   747:     ///     let meta = fs::metadata(\"some_file\")?;\n   748:     ///     let nano_last_modification_time = meta.mtime_nsec();\n   749:     ///     Ok(())\n   750:     /// }\n   751:     /// ```\n   752:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   753:     fn mtime_nsec(&self) -> i64;\n   754:     /// Returns the last status change time of the file, in seconds since Unix Epoch.\n   755:     ///\n   756:     /// # Examples\n   757:     ///\n   758:     /// ```no_run\n   759:     /// use std::fs;\n   760:     /// use std::os::unix::fs::MetadataExt;\n   761:     /// use std::io;\n   762:     ///\n   763:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::nlink",
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
      "name": "nlink",
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
    "verification_source": "   594:     /// Returns the number of hard links pointing to this file.\n   595:     ///\n   596:     /// # Examples\n   597:     ///\n   598:     /// ```no_run\n   599:     /// use std::fs;\n   600:     /// use std::os::unix::fs::MetadataExt;\n   601:     /// use std::io;\n   602:     ///\n   603:     /// fn main() -> io::Result<()> {\n   604:     ///     let meta = fs::metadata(\"some_file\")?;\n   605:     ///     let nb_hard_links = meta.nlink();\n   606:     ///     Ok(())\n   607:     /// }\n   608:     /// ```\n   609:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   610:     fn nlink(&self) -> u64;\n   611:     /// Returns the user ID of the owner of this file.\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```no_run\n   616:     /// use std::fs;\n   617:     /// use std::os::unix::fs::MetadataExt;\n   618:     /// use std::io;\n   619:     ///\n   620:     /// fn main() -> io::Result<()> {\n   621:     ///     let meta = fs::metadata(\"some_file\")?;\n   622:     ///     let user_id = meta.uid();\n   623:     ///     Ok(())\n   624:     /// }\n   625:     /// ```\n   626:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   603:     /// use std::os::unix::fs::MetadataExt;\n   604:     /// use std::io;\n   605:     ///\n   606:     /// fn main() -> io::Result<()> {\n   607:     ///     let meta = fs::metadata(\"some_file\")?;\n   608:     ///     let nb_hard_links = meta.nlink();\n   609:     ///     Ok(())\n   610:     /// }\n   611:     /// ```\n   612:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   613:     fn nlink(&self) -> u64;\n   614:     /// Returns the user ID of the owner of this file.\n   615:     ///\n   616:     /// # Examples\n   617:     ///\n   618:     /// ```no_run\n   619:     /// use std::fs;\n   620:     /// use std::os::unix::fs::MetadataExt;\n   621:     /// use std::io;\n   622:     ///\n   623:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::rdev",
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
      "name": "rdev",
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
    "verification_source": "   645:     /// Returns the device ID of this file (if it is a special one).\n   646:     ///\n   647:     /// # Examples\n   648:     ///\n   649:     /// ```no_run\n   650:     /// use std::fs;\n   651:     /// use std::os::unix::fs::MetadataExt;\n   652:     /// use std::io;\n   653:     ///\n   654:     /// fn main() -> io::Result<()> {\n   655:     ///     let meta = fs::metadata(\"some_file\")?;\n   656:     ///     let device_id = meta.rdev();\n   657:     ///     Ok(())\n   658:     /// }\n   659:     /// ```\n   660:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   661:     fn rdev(&self) -> u64;\n   662:     /// Returns the total size of this file in bytes.\n   663:     ///\n   664:     /// # Examples\n   665:     ///\n   666:     /// ```no_run\n   667:     /// use std::fs;\n   668:     /// use std::os::unix::fs::MetadataExt;\n   669:     /// use std::io;\n   670:     ///\n   671:     /// fn main() -> io::Result<()> {\n   672:     ///     let meta = fs::metadata(\"some_file\")?;\n   673:     ///     let file_size = meta.size();\n   674:     ///     Ok(())\n   675:     /// }\n   676:     /// ```\n   677:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   654:     /// use std::os::unix::fs::MetadataExt;\n   655:     /// use std::io;\n   656:     ///\n   657:     /// fn main() -> io::Result<()> {\n   658:     ///     let meta = fs::metadata(\"some_file\")?;\n   659:     ///     let device_id = meta.rdev();\n   660:     ///     Ok(())\n   661:     /// }\n   662:     /// ```\n   663:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   664:     fn rdev(&self) -> u64;\n   665:     /// Returns the total size of this file in bytes.\n   666:     ///\n   667:     /// # Examples\n   668:     ///\n   669:     /// ```no_run\n   670:     /// use std::fs;\n   671:     /// use std::os::unix::fs::MetadataExt;\n   672:     /// use std::io;\n   673:     ///\n   674:     /// fn main() -> io::Result<()> {",
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
