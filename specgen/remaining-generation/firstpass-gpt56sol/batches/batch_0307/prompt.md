For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::fs::MetadataExt::size",
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
      "name": "size",
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
    "verification_source": "   662:     /// Returns the total size of this file in bytes.\n   663:     ///\n   664:     /// # Examples\n   665:     ///\n   666:     /// ```no_run\n   667:     /// use std::fs;\n   668:     /// use std::os::unix::fs::MetadataExt;\n   669:     /// use std::io;\n   670:     ///\n   671:     /// fn main() -> io::Result<()> {\n   672:     ///     let meta = fs::metadata(\"some_file\")?;\n   673:     ///     let file_size = meta.size();\n   674:     ///     Ok(())\n   675:     /// }\n   676:     /// ```\n   677:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   678:     fn size(&self) -> u64;\n   679:     /// Returns the last access time of the file, in seconds since Unix Epoch.\n   680:     ///\n   681:     /// # Examples\n   682:     ///\n   683:     /// ```no_run\n   684:     /// use std::fs;\n   685:     /// use std::os::unix::fs::MetadataExt;\n   686:     /// use std::io;\n   687:     ///\n   688:     /// fn main() -> io::Result<()> {\n   689:     ///     let meta = fs::metadata(\"some_file\")?;\n   690:     ///     let last_access_time = meta.atime();\n   691:     ///     Ok(())\n   692:     /// }\n   693:     /// ```\n   694:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   671:     /// use std::os::unix::fs::MetadataExt;\n   672:     /// use std::io;\n   673:     ///\n   674:     /// fn main() -> io::Result<()> {\n   675:     ///     let meta = fs::metadata(\"some_file\")?;\n   676:     ///     let file_size = meta.size();\n   677:     ///     Ok(())\n   678:     /// }\n   679:     /// ```\n   680:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   681:     fn size(&self) -> u64;\n   682:     /// Returns the last access time of the file, in seconds since Unix Epoch.\n   683:     ///\n   684:     /// # Examples\n   685:     ///\n   686:     /// ```no_run\n   687:     /// use std::fs;\n   688:     /// use std::os::unix::fs::MetadataExt;\n   689:     /// use std::io;\n   690:     ///\n   691:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::MetadataExt::uid",
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
      "name": "uid",
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
    "verification_source": "   611:     /// Returns the user ID of the owner of this file.\n   612:     ///\n   613:     /// # Examples\n   614:     ///\n   615:     /// ```no_run\n   616:     /// use std::fs;\n   617:     /// use std::os::unix::fs::MetadataExt;\n   618:     /// use std::io;\n   619:     ///\n   620:     /// fn main() -> io::Result<()> {\n   621:     ///     let meta = fs::metadata(\"some_file\")?;\n   622:     ///     let user_id = meta.uid();\n   623:     ///     Ok(())\n   624:     /// }\n   625:     /// ```\n   626:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   627:     fn uid(&self) -> u32;\n   628:     /// Returns the group ID of the owner of this file.\n   629:     ///\n   630:     /// # Examples\n   631:     ///\n   632:     /// ```no_run\n   633:     /// use std::fs;\n   634:     /// use std::os::unix::fs::MetadataExt;\n   635:     /// use std::io;\n   636:     ///\n   637:     /// fn main() -> io::Result<()> {\n   638:     ///     let meta = fs::metadata(\"some_file\")?;\n   639:     ///     let group_id = meta.gid();\n   640:     ///     Ok(())\n   641:     /// }\n   642:     /// ```\n   643:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]",
    "nanvix_source": "   620:     /// use std::os::unix::fs::MetadataExt;\n   621:     /// use std::io;\n   622:     ///\n   623:     /// fn main() -> io::Result<()> {\n   624:     ///     let meta = fs::metadata(\"some_file\")?;\n   625:     ///     let user_id = meta.uid();\n   626:     ///     Ok(())\n   627:     /// }\n   628:     /// ```\n   629:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   630:     fn uid(&self) -> u32;\n   631:     /// Returns the group ID of the owner of this file.\n   632:     ///\n   633:     /// # Examples\n   634:     ///\n   635:     /// ```no_run\n   636:     /// use std::fs;\n   637:     /// use std::os::unix::fs::MetadataExt;\n   638:     /// use std::io;\n   639:     ///\n   640:     /// fn main() -> io::Result<()> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::OpenOptionsExt::custom_flags",
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
      "name": "custom_flags",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2975",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "flags",
            {
              "primitive": "i32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   504:     ///\n   505:     /// # Examples\n   506:     ///\n   507:     /// ```no_run\n   508:     /// # mod libc { pub const O_NOFOLLOW: i32 = 0; }\n   509:     /// use std::fs::OpenOptions;\n   510:     /// use std::os::unix::fs::OpenOptionsExt;\n   511:     ///\n   512:     /// # fn main() {\n   513:     /// let mut options = OpenOptions::new();\n   514:     /// options.write(true);\n   515:     /// options.custom_flags(libc::O_NOFOLLOW);\n   516:     /// let file = options.open(\"foo.txt\");\n   517:     /// # }\n   518:     /// ```\n   519:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   520:     fn custom_flags(&mut self, flags: i32) -> &mut Self;\n   521: }\n   522: \n   523: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   524: impl OpenOptionsExt for OpenOptions {\n   525:     fn mode(&mut self, mode: u32) -> &mut OpenOptions {\n   526:         self.as_inner_mut().mode(mode);\n   527:         self\n   528:     }\n   529: \n   530:     fn custom_flags(&mut self, flags: i32) -> &mut OpenOptions {\n   531:         self.as_inner_mut().custom_flags(flags);\n   532:         self\n   533:     }\n   534: }\n   535: \n   536: /// Unix-specific extensions to [`fs::Metadata`].",
    "nanvix_source": "   513:     /// use std::os::unix::fs::OpenOptionsExt;\n   514:     ///\n   515:     /// # fn main() {\n   516:     /// let mut options = OpenOptions::new();\n   517:     /// options.write(true);\n   518:     /// options.custom_flags(libc::O_NOFOLLOW);\n   519:     /// let file = options.open(\"foo.txt\");\n   520:     /// # }\n   521:     /// ```\n   522:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   523:     fn custom_flags(&mut self, flags: i32) -> &mut Self;\n   524: }\n   525: \n   526: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   527: impl OpenOptionsExt for OpenOptions {\n   528:     fn mode(&mut self, mode: u32) -> &mut OpenOptions {\n   529:         self.as_inner_mut().mode(mode);\n   530:         self\n   531:     }\n   532: \n   533:     fn custom_flags(&mut self, flags: i32) -> &mut OpenOptions {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::OpenOptionsExt::mode",
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
      "name": "mode",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2975",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "mode",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   479:     /// The operating system masks out bits with the system's `umask`, to produce\n   480:     /// the final permissions.\n   481:     ///\n   482:     /// # Examples\n   483:     ///\n   484:     /// ```no_run\n   485:     /// use std::fs::OpenOptions;\n   486:     /// use std::os::unix::fs::OpenOptionsExt;\n   487:     ///\n   488:     /// # fn main() {\n   489:     /// let mut options = OpenOptions::new();\n   490:     /// options.mode(0o644); // Give read/write for owner and read for others.\n   491:     /// let file = options.open(\"foo.txt\");\n   492:     /// # }\n   493:     /// ```\n   494:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   495:     fn mode(&mut self, mode: u32) -> &mut Self;\n   496: \n   497:     /// Pass custom flags to the `flags` argument of `open`.\n   498:     ///\n   499:     /// The bits that define the access mode are masked out with `O_ACCMODE`, to\n   500:     /// ensure they do not interfere with the access mode set by Rust's options.\n   501:     ///\n   502:     /// Custom flags can only set flags, not remove flags set by Rust's options.\n   503:     /// This function overwrites any previously-set custom flags.\n   504:     ///\n   505:     /// # Examples\n   506:     ///\n   507:     /// ```no_run\n   508:     /// # mod libc { pub const O_NOFOLLOW: i32 = 0; }\n   509:     /// use std::fs::OpenOptions;\n   510:     /// use std::os::unix::fs::OpenOptionsExt;\n   511:     ///",
    "nanvix_source": "   488:     /// use std::fs::OpenOptions;\n   489:     /// use std::os::unix::fs::OpenOptionsExt;\n   490:     ///\n   491:     /// # fn main() {\n   492:     /// let mut options = OpenOptions::new();\n   493:     /// options.mode(0o644); // Give read/write for owner and read for others.\n   494:     /// let file = options.open(\"foo.txt\");\n   495:     /// # }\n   496:     /// ```\n   497:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   498:     fn mode(&mut self, mode: u32) -> &mut Self;\n   499: \n   500:     /// Pass custom flags to the `flags` argument of `open`.\n   501:     ///\n   502:     /// The bits that define the access mode are masked out with `O_ACCMODE`, to\n   503:     /// ensure they do not interfere with the access mode set by Rust's options.\n   504:     ///\n   505:     /// Custom flags can only set flags, not remove flags set by Rust's options.\n   506:     /// This function overwrites any previously-set custom flags.\n   507:     ///\n   508:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::PermissionsExt::from_mode",
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
      "name": "from_mode",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:3026",
        "kind": "trait",
        "name": "PermissionsExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "PermissionsExt"
        ]
      },
      "signature": {
        "inputs": [
          [
            "mode",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   437: /// permissions.set_mode(other_mode);\n   438: /// assert_eq!(permissions.mode(), other_mode);\n   439: /// ```\n   440: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   441: pub trait PermissionsExt {\n   442:     /// Returns the mode permission bits\n   443:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   444:     fn mode(&self) -> u32;\n   445: \n   446:     /// Sets the mode permission bits.\n   447:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   448:     fn set_mode(&mut self, mode: u32);\n   449: \n   450:     /// Creates a new instance from the given mode permission bits.\n   451:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   452:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   453:     fn from_mode(mode: u32) -> Self;\n   454: }\n   455: \n   456: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   457: impl PermissionsExt for Permissions {\n   458:     fn mode(&self) -> u32 {\n   459:         self.as_inner().mode()\n   460:     }\n   461: \n   462:     fn set_mode(&mut self, mode: u32) {\n   463:         *self = Permissions::from_inner(FromInner::from_inner(mode));\n   464:     }\n   465: \n   466:     fn from_mode(mode: u32) -> Permissions {\n   467:         Permissions::from_inner(FromInner::from_inner(mode))\n   468:     }\n   469: }",
    "nanvix_source": "   446:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   447:     fn mode(&self) -> u32;\n   448: \n   449:     /// Sets the mode permission bits.\n   450:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   451:     fn set_mode(&mut self, mode: u32);\n   452: \n   453:     /// Creates a new instance from the given mode permission bits.\n   454:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   455:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   456:     fn from_mode(mode: u32) -> Self;\n   457: }\n   458: \n   459: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   460: impl PermissionsExt for Permissions {\n   461:     fn mode(&self) -> u32 {\n   462:         self.as_inner().mode()\n   463:     }\n   464: \n   465:     fn set_mode(&mut self, mode: u32) {\n   466:         *self = Permissions::from_inner(FromInner::from_inner(mode));",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::PermissionsExt::mode",
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
        "item_id": "std:3026",
        "kind": "trait",
        "name": "PermissionsExt",
        "path": [
          "std",
          "os",
          "unix",
          "fs",
          "PermissionsExt"
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
    "verification_source": "   428: /// use std::os::unix::fs::PermissionsExt;\n   429: ///\n   430: /// // read/write for owner and read for others\n   431: /// let my_mode = 0o644;\n   432: /// let mut permissions = Permissions::from_mode(my_mode);\n   433: /// assert_eq!(permissions.mode(), my_mode);\n   434: ///\n   435: /// // read/write/execute for owner\n   436: /// let other_mode = 0o700;\n   437: /// permissions.set_mode(other_mode);\n   438: /// assert_eq!(permissions.mode(), other_mode);\n   439: /// ```\n   440: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   441: pub trait PermissionsExt {\n   442:     /// Returns the mode permission bits\n   443:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   444:     fn mode(&self) -> u32;\n   445: \n   446:     /// Sets the mode permission bits.\n   447:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   448:     fn set_mode(&mut self, mode: u32);\n   449: \n   450:     /// Creates a new instance from the given mode permission bits.\n   451:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   452:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   453:     fn from_mode(mode: u32) -> Self;\n   454: }\n   455: \n   456: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   457: impl PermissionsExt for Permissions {\n   458:     fn mode(&self) -> u32 {\n   459:         self.as_inner().mode()\n   460:     }",
    "nanvix_source": "   437: ///\n   438: /// // read/write/execute for owner\n   439: /// let other_mode = 0o700;\n   440: /// permissions.set_mode(other_mode);\n   441: /// assert_eq!(permissions.mode(), other_mode);\n   442: /// ```\n   443: #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   444: pub trait PermissionsExt {\n   445:     /// Returns the mode permission bits\n   446:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   447:     fn mode(&self) -> u32;\n   448: \n   449:     /// Sets the mode permission bits.\n   450:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   451:     fn set_mode(&mut self, mode: u32);\n   452: \n   453:     /// Creates a new instance from the given mode permission bits.\n   454:     #[stable(feature = \"fs_ext\", since = \"1.1.0\")]\n   455:     #[cfg_attr(not(test), rustc_diagnostic_item = \"permissions_from_mode\")]\n   456:     fn from_mode(mode: u32) -> Self;\n   457: }",
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
