For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::fs::FileTypeExt::is_symlink_dir",
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
      "name": "is_symlink_dir",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3104",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   584:     }\n   585:     fn file_index(&self) -> Option<u64> {\n   586:         self.as_inner().file_index()\n   587:     }\n   588:     fn change_time(&self) -> Option<u64> {\n   589:         self.as_inner().changed_u64()\n   590:     }\n   591: }\n   592: \n   593: /// Windows-specific extensions to [`fs::FileType`].\n   594: ///\n   595: /// On Windows, a symbolic link knows whether it is a file or directory.\n   596: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   597: pub trait FileTypeExt: Sealed {\n   598:     /// Returns `true` if this file type is a symbolic link that is also a directory.\n   599:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   600:     fn is_symlink_dir(&self) -> bool;\n   601:     /// Returns `true` if this file type is a symbolic link that is also a file.\n   602:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   603:     fn is_symlink_file(&self) -> bool;\n   604: }\n   605: \n   606: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   607: impl Sealed for fs::FileType {}\n   608: \n   609: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   610: impl FileTypeExt for fs::FileType {\n   611:     fn is_symlink_dir(&self) -> bool {\n   612:         self.as_inner().is_symlink_dir()\n   613:     }\n   614:     fn is_symlink_file(&self) -> bool {\n   615:         self.as_inner().is_symlink_file()\n   616:     }",
    "nanvix_source": "   645:     }\n   646: }\n   647: \n   648: /// Windows-specific extensions to [`fs::FileType`].\n   649: ///\n   650: /// On Windows, a symbolic link knows whether it is a file or directory.\n   651: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   652: pub impl(self) trait FileTypeExt {\n   653:     /// Returns `true` if this file type is a symbolic link that is also a directory.\n   654:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   655:     fn is_symlink_dir(&self) -> bool;\n   656:     /// Returns `true` if this file type is a symbolic link that is also a file.\n   657:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   658:     fn is_symlink_file(&self) -> bool;\n   659: }\n   660: \n   661: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   662: impl FileTypeExt for fs::FileType {\n   663:     fn is_symlink_dir(&self) -> bool {\n   664:         self.as_inner().is_symlink_dir()\n   665:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::FileTypeExt::is_symlink_file",
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
      "name": "is_symlink_file",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3104",
        "kind": "trait",
        "name": "FileTypeExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   587:     }\n   588:     fn change_time(&self) -> Option<u64> {\n   589:         self.as_inner().changed_u64()\n   590:     }\n   591: }\n   592: \n   593: /// Windows-specific extensions to [`fs::FileType`].\n   594: ///\n   595: /// On Windows, a symbolic link knows whether it is a file or directory.\n   596: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   597: pub trait FileTypeExt: Sealed {\n   598:     /// Returns `true` if this file type is a symbolic link that is also a directory.\n   599:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   600:     fn is_symlink_dir(&self) -> bool;\n   601:     /// Returns `true` if this file type is a symbolic link that is also a file.\n   602:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   603:     fn is_symlink_file(&self) -> bool;\n   604: }\n   605: \n   606: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   607: impl Sealed for fs::FileType {}\n   608: \n   609: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   610: impl FileTypeExt for fs::FileType {\n   611:     fn is_symlink_dir(&self) -> bool {\n   612:         self.as_inner().is_symlink_dir()\n   613:     }\n   614:     fn is_symlink_file(&self) -> bool {\n   615:         self.as_inner().is_symlink_file()\n   616:     }\n   617: }\n   618: \n   619: /// Windows-specific extensions to [`fs::FileTimes`].",
    "nanvix_source": "   648: /// Windows-specific extensions to [`fs::FileType`].\n   649: ///\n   650: /// On Windows, a symbolic link knows whether it is a file or directory.\n   651: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   652: pub impl(self) trait FileTypeExt {\n   653:     /// Returns `true` if this file type is a symbolic link that is also a directory.\n   654:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   655:     fn is_symlink_dir(&self) -> bool;\n   656:     /// Returns `true` if this file type is a symbolic link that is also a file.\n   657:     #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   658:     fn is_symlink_file(&self) -> bool;\n   659: }\n   660: \n   661: #[stable(feature = \"windows_file_type_ext\", since = \"1.64.0\")]\n   662: impl FileTypeExt for fs::FileType {\n   663:     fn is_symlink_dir(&self) -> bool {\n   664:         self.as_inner().is_symlink_dir()\n   665:     }\n   666:     fn is_symlink_file(&self) -> bool {\n   667:         self.as_inner().is_symlink_file()\n   668:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::MetadataExt::creation_time",
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
      "name": "creation_time",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2882",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   416:     /// # Examples\n   417:     ///\n   418:     /// ```no_run\n   419:     /// use std::io;\n   420:     /// use std::fs;\n   421:     /// use std::os::windows::prelude::*;\n   422:     ///\n   423:     /// fn main() -> io::Result<()> {\n   424:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   425:     ///     let creation_time = metadata.creation_time();\n   426:     ///     Ok(())\n   427:     /// }\n   428:     /// ```\n   429:     ///\n   430:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   431:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   432:     fn creation_time(&self) -> u64;\n   433: \n   434:     /// Returns the value of the `ftLastAccessTime` field of this metadata.\n   435:     ///\n   436:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   437:     /// which represents the number of 100-nanosecond intervals since\n   438:     /// January 1, 1601 (UTC). The struct is automatically\n   439:     /// converted to a `u64` value, as that is the recommended way\n   440:     /// to use it.\n   441:     ///\n   442:     /// For a file, the value specifies the last time that a file was read\n   443:     /// from or written to. For a directory, the value specifies when\n   444:     /// the directory was created. For both files and directories, the\n   445:     /// specified date is correct, but the time of day is always set to\n   446:     /// midnight.\n   447:     ///\n   448:     /// If the underlying filesystem does not support last access time, the",
    "nanvix_source": "   477:     ///\n   478:     /// fn main() -> io::Result<()> {\n   479:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   480:     ///     let creation_time = metadata.creation_time();\n   481:     ///     Ok(())\n   482:     /// }\n   483:     /// ```\n   484:     ///\n   485:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   486:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   487:     fn creation_time(&self) -> u64;\n   488: \n   489:     /// Returns the value of the `ftLastAccessTime` field of this metadata.\n   490:     ///\n   491:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   492:     /// which represents the number of 100-nanosecond intervals since\n   493:     /// January 1, 1601 (UTC). The struct is automatically\n   494:     /// converted to a `u64` value, as that is the recommended way\n   495:     /// to use it.\n   496:     ///\n   497:     /// For a file, the value specifies the last time that a file was read",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::MetadataExt::file_attributes",
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
      "name": "file_attributes",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2882",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   387:     ///\n   388:     /// ```no_run\n   389:     /// use std::io;\n   390:     /// use std::fs;\n   391:     /// use std::os::windows::prelude::*;\n   392:     ///\n   393:     /// fn main() -> io::Result<()> {\n   394:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   395:     ///     let attributes = metadata.file_attributes();\n   396:     ///     Ok(())\n   397:     /// }\n   398:     /// ```\n   399:     ///\n   400:     /// [File Attribute Constants]:\n   401:     ///     https://docs.microsoft.com/windows/win32/fileio/file-attribute-constants\n   402:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   403:     fn file_attributes(&self) -> u32;\n   404: \n   405:     /// Returns the value of the `ftCreationTime` field of this metadata.\n   406:     ///\n   407:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   408:     /// which represents the number of 100-nanosecond intervals since\n   409:     /// January 1, 1601 (UTC). The struct is automatically\n   410:     /// converted to a `u64` value, as that is the recommended way\n   411:     /// to use it.\n   412:     ///\n   413:     /// If the underlying filesystem does not support creation time, the\n   414:     /// returned value is 0.\n   415:     ///\n   416:     /// # Examples\n   417:     ///\n   418:     /// ```no_run\n   419:     /// use std::io;",
    "nanvix_source": "   448:     /// fn main() -> io::Result<()> {\n   449:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   450:     ///     let attributes = metadata.file_attributes();\n   451:     ///     Ok(())\n   452:     /// }\n   453:     /// ```\n   454:     ///\n   455:     /// [File Attribute Constants]:\n   456:     ///     https://docs.microsoft.com/windows/win32/fileio/file-attribute-constants\n   457:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   458:     fn file_attributes(&self) -> u32;\n   459: \n   460:     /// Returns the value of the `ftCreationTime` field of this metadata.\n   461:     ///\n   462:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   463:     /// which represents the number of 100-nanosecond intervals since\n   464:     /// January 1, 1601 (UTC). The struct is automatically\n   465:     /// converted to a `u64` value, as that is the recommended way\n   466:     /// to use it.\n   467:     ///\n   468:     /// If the underlying filesystem does not support creation time, the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::MetadataExt::file_size",
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
      "name": "file_size",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2882",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   505:     /// The returned value does not have meaning for directories.\n   506:     ///\n   507:     /// # Examples\n   508:     ///\n   509:     /// ```no_run\n   510:     /// use std::io;\n   511:     /// use std::fs;\n   512:     /// use std::os::windows::prelude::*;\n   513:     ///\n   514:     /// fn main() -> io::Result<()> {\n   515:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   516:     ///     let file_size = metadata.file_size();\n   517:     ///     Ok(())\n   518:     /// }\n   519:     /// ```\n   520:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   521:     fn file_size(&self) -> u64;\n   522: \n   523:     /// Returns the value of the `dwVolumeSerialNumber` field of this\n   524:     /// metadata.\n   525:     ///\n   526:     /// This will return `None` if the `Metadata` instance was created from a\n   527:     /// call to `DirEntry::metadata`. If this `Metadata` was created by using\n   528:     /// `fs::metadata` or `File::metadata`, then this will return `Some`.\n   529:     #[unstable(feature = \"windows_by_handle\", issue = \"63010\")]\n   530:     fn volume_serial_number(&self) -> Option<u32>;\n   531: \n   532:     /// Returns the value of the `nNumberOfLinks` field of this\n   533:     /// metadata.\n   534:     ///\n   535:     /// This will return `None` if the `Metadata` instance was created from a\n   536:     /// call to `DirEntry::metadata`. If this `Metadata` was created by using\n   537:     /// `fs::metadata` or `File::metadata`, then this will return `Some`.",
    "nanvix_source": "   566:     /// use std::fs;\n   567:     /// use std::os::windows::prelude::*;\n   568:     ///\n   569:     /// fn main() -> io::Result<()> {\n   570:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   571:     ///     let file_size = metadata.file_size();\n   572:     ///     Ok(())\n   573:     /// }\n   574:     /// ```\n   575:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   576:     fn file_size(&self) -> u64;\n   577: \n   578:     /// Returns the value of the `dwVolumeSerialNumber` field of this\n   579:     /// metadata.\n   580:     ///\n   581:     /// This will return `None` if the `Metadata` instance was created from a\n   582:     /// call to `DirEntry::metadata`. If this `Metadata` was created by using\n   583:     /// `fs::metadata` or `File::metadata`, then this will return `Some`.\n   584:     #[unstable(feature = \"windows_by_handle\", issue = \"63010\")]\n   585:     fn volume_serial_number(&self) -> Option<u32>;\n   586: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::MetadataExt::last_access_time",
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
      "name": "last_access_time",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2882",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "windows",
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
    "verification_source": "   451:     /// # Examples\n   452:     ///\n   453:     /// ```no_run\n   454:     /// use std::io;\n   455:     /// use std::fs;\n   456:     /// use std::os::windows::prelude::*;\n   457:     ///\n   458:     /// fn main() -> io::Result<()> {\n   459:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   460:     ///     let last_access_time = metadata.last_access_time();\n   461:     ///     Ok(())\n   462:     /// }\n   463:     /// ```\n   464:     ///\n   465:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   466:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   467:     fn last_access_time(&self) -> u64;\n   468: \n   469:     /// Returns the value of the `ftLastWriteTime` field of this metadata.\n   470:     ///\n   471:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   472:     /// which represents the number of 100-nanosecond intervals since\n   473:     /// January 1, 1601 (UTC). The struct is automatically\n   474:     /// converted to a `u64` value, as that is the recommended way\n   475:     /// to use it.\n   476:     ///\n   477:     /// For a file, the value specifies the last time that a file was written\n   478:     /// to. For a directory, the structure specifies when the directory was\n   479:     /// created.\n   480:     ///\n   481:     /// If the underlying filesystem does not support the last write time,\n   482:     /// the returned value is 0.\n   483:     ///",
    "nanvix_source": "   512:     ///\n   513:     /// fn main() -> io::Result<()> {\n   514:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   515:     ///     let last_access_time = metadata.last_access_time();\n   516:     ///     Ok(())\n   517:     /// }\n   518:     /// ```\n   519:     ///\n   520:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   521:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   522:     fn last_access_time(&self) -> u64;\n   523: \n   524:     /// Returns the value of the `ftLastWriteTime` field of this metadata.\n   525:     ///\n   526:     /// The returned 64-bit value is equivalent to a [`FILETIME`] struct,\n   527:     /// which represents the number of 100-nanosecond intervals since\n   528:     /// January 1, 1601 (UTC). The struct is automatically\n   529:     /// converted to a `u64` value, as that is the recommended way\n   530:     /// to use it.\n   531:     ///\n   532:     /// For a file, the value specifies the last time that a file was written",
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
