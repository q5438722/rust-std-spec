For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::PathBuf::set_extension",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "set_extension",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
          ],
          [
            "extension",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "  1638:     /// p.set_extension(\"dark.side\");\n  1639:     /// assert_eq!(Path::new(\"/feel/the.dark.side\"), p.as_path());\n  1640:     ///\n  1641:     /// p.set_extension(\"cookie\");\n  1642:     /// assert_eq!(Path::new(\"/feel/the.dark.cookie\"), p.as_path());\n  1643:     ///\n  1644:     /// p.set_extension(\"\");\n  1645:     /// assert_eq!(Path::new(\"/feel/the.dark\"), p.as_path());\n  1646:     ///\n  1647:     /// p.set_extension(\"\");\n  1648:     /// assert_eq!(Path::new(\"/feel/the\"), p.as_path());\n  1649:     ///\n  1650:     /// p.set_extension(\"\");\n  1651:     /// assert_eq!(Path::new(\"/feel/the\"), p.as_path());\n  1652:     /// ```\n  1653:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1654:     pub fn set_extension<S: AsRef<OsStr>>(&mut self, extension: S) -> bool {\n  1655:         self._set_extension(extension.as_ref())\n  1656:     }\n  1657: \n  1658:     fn _set_extension(&mut self, extension: &OsStr) -> bool {\n  1659:         validate_extension(extension);\n  1660: \n  1661:         let file_stem = match self.file_stem() {\n  1662:             None => return false,\n  1663:             Some(f) => f.as_encoded_bytes(),\n  1664:         };\n  1665: \n  1666:         // truncate until right after the file stem\n  1667:         let end_file_stem = file_stem[file_stem.len()..].as_ptr().addr();\n  1668:         let start = self.inner.as_encoded_bytes().as_ptr().addr();\n  1669:         self.inner.truncate(end_file_stem.wrapping_sub(start));\n  1670: ",
    "nanvix_source": "  1644:     /// p.set_extension(\"\");\n  1645:     /// assert_eq!(Path::new(\"/feel/the.dark\"), p.as_path());\n  1646:     ///\n  1647:     /// p.set_extension(\"\");\n  1648:     /// assert_eq!(Path::new(\"/feel/the\"), p.as_path());\n  1649:     ///\n  1650:     /// p.set_extension(\"\");\n  1651:     /// assert_eq!(Path::new(\"/feel/the\"), p.as_path());\n  1652:     /// ```\n  1653:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1654:     pub fn set_extension<S: AsRef<OsStr>>(&mut self, extension: S) -> bool {\n  1655:         self._set_extension(extension.as_ref())\n  1656:     }\n  1657: \n  1658:     fn _set_extension(&mut self, extension: &OsStr) -> bool {\n  1659:         validate_extension(extension);\n  1660: \n  1661:         let file_stem = match self.file_stem() {\n  1662:             None => return false,\n  1663:             Some(f) => f.as_encoded_bytes(),\n  1664:         };",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::set_file_name",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "set_file_name",
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
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
          ],
          [
            "file_name",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1569:     /// assert!(buf == PathBuf::from(\"/foo.txt\"));\n  1570:     /// assert!(buf.file_name().is_some());\n  1571:     ///\n  1572:     /// buf.set_file_name(\"bar.txt\");\n  1573:     /// assert!(buf == PathBuf::from(\"/bar.txt\"));\n  1574:     ///\n  1575:     /// buf.set_file_name(\"baz\");\n  1576:     /// assert!(buf == PathBuf::from(\"/baz\"));\n  1577:     ///\n  1578:     /// buf.set_file_name(\"../b/c.txt\");\n  1579:     /// assert!(buf == PathBuf::from(\"/../b/c.txt\"));\n  1580:     ///\n  1581:     /// buf.set_file_name(\"baz\");\n  1582:     /// assert!(buf == PathBuf::from(\"/../b/baz\"));\n  1583:     /// ```\n  1584:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1585:     pub fn set_file_name<S: AsRef<OsStr>>(&mut self, file_name: S) {\n  1586:         self._set_file_name(file_name.as_ref())\n  1587:     }\n  1588: \n  1589:     fn _set_file_name(&mut self, file_name: &OsStr) {\n  1590:         if self.file_name().is_some() {\n  1591:             let popped = self.pop();\n  1592:             debug_assert!(popped);\n  1593:         }\n  1594:         self.push(file_name);\n  1595:     }\n  1596: \n  1597:     /// Updates [`self.extension`] to `Some(extension)` or to `None` if\n  1598:     /// `extension` is empty.\n  1599:     ///\n  1600:     /// Returns `false` and does nothing if [`self.file_name`] is [`None`],\n  1601:     /// returns `true` and updates the extension otherwise.",
    "nanvix_source": "  1575:     /// buf.set_file_name(\"baz\");\n  1576:     /// assert!(buf == PathBuf::from(\"/baz\"));\n  1577:     ///\n  1578:     /// buf.set_file_name(\"../b/c.txt\");\n  1579:     /// assert!(buf == PathBuf::from(\"/../b/c.txt\"));\n  1580:     ///\n  1581:     /// buf.set_file_name(\"baz\");\n  1582:     /// assert!(buf == PathBuf::from(\"/../b/baz\"));\n  1583:     /// ```\n  1584:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1585:     pub fn set_file_name<S: AsRef<OsStr>>(&mut self, file_name: S) {\n  1586:         self._set_file_name(file_name.as_ref())\n  1587:     }\n  1588: \n  1589:     fn _set_file_name(&mut self, file_name: &OsStr) {\n  1590:         if self.file_name().is_some() {\n  1591:             let popped = self.pop();\n  1592:             debug_assert!(popped);\n  1593:         }\n  1594:         self.push(file_name);\n  1595:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Prefix::is_verbatim",
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
      "name": "is_verbatim",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 6710,
            "path": "Prefix"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6712",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6710",
        "resolved_owner_path": [
          "std",
          "path",
          "Prefix"
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
    "verification_source": "   220:     /// # Examples\n   221:     ///\n   222:     /// ```\n   223:     /// use std::path::Prefix::*;\n   224:     /// use std::ffi::OsStr;\n   225:     ///\n   226:     /// assert!(Verbatim(OsStr::new(\"pictures\")).is_verbatim());\n   227:     /// assert!(VerbatimUNC(OsStr::new(\"server\"), OsStr::new(\"share\")).is_verbatim());\n   228:     /// assert!(VerbatimDisk(b'C').is_verbatim());\n   229:     /// assert!(!DeviceNS(OsStr::new(\"BrainInterface\")).is_verbatim());\n   230:     /// assert!(!UNC(OsStr::new(\"server\"), OsStr::new(\"share\")).is_verbatim());\n   231:     /// assert!(!Disk(b'C').is_verbatim());\n   232:     /// ```\n   233:     #[inline]\n   234:     #[must_use]\n   235:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   236:     pub fn is_verbatim(&self) -> bool {\n   237:         use self::Prefix::*;\n   238:         matches!(*self, Verbatim(_) | VerbatimDisk(_) | VerbatimUNC(..))\n   239:     }\n   240: \n   241:     #[inline]\n   242:     fn is_drive(&self) -> bool {\n   243:         matches!(*self, Prefix::Disk(_))\n   244:     }\n   245: \n   246:     #[inline]\n   247:     fn has_implicit_root(&self) -> bool {\n   248:         !self.is_drive()\n   249:     }\n   250: }\n   251: \n   252: ////////////////////////////////////////////////////////////////////////////////",
    "nanvix_source": "   226:     /// assert!(Verbatim(OsStr::new(\"pictures\")).is_verbatim());\n   227:     /// assert!(VerbatimUNC(OsStr::new(\"server\"), OsStr::new(\"share\")).is_verbatim());\n   228:     /// assert!(VerbatimDisk(b'C').is_verbatim());\n   229:     /// assert!(!DeviceNS(OsStr::new(\"BrainInterface\")).is_verbatim());\n   230:     /// assert!(!UNC(OsStr::new(\"server\"), OsStr::new(\"share\")).is_verbatim());\n   231:     /// assert!(!Disk(b'C').is_verbatim());\n   232:     /// ```\n   233:     #[inline]\n   234:     #[must_use]\n   235:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   236:     pub fn is_verbatim(&self) -> bool {\n   237:         use self::Prefix::*;\n   238:         matches!(*self, Verbatim(_) | VerbatimDisk(_) | VerbatimUNC(..))\n   239:     }\n   240: \n   241:     #[inline]\n   242:     fn is_drive(&self) -> bool {\n   243:         matches!(*self, Prefix::Disk(_))\n   244:     }\n   245: \n   246:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PrefixComponent::as_os_str",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 6754,
            "path": "PrefixComponent"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6755",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6754",
        "resolved_owner_path": [
          "std",
          "path",
          "PrefixComponent"
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
            "lifetime": "'a",
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
    "verification_source": "   451: impl<'a> PrefixComponent<'a> {\n   452:     /// Returns the parsed prefix data.\n   453:     ///\n   454:     /// See [`Prefix`]'s documentation for more information on the different\n   455:     /// kinds of prefixes.\n   456:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   457:     #[must_use]\n   458:     #[inline]\n   459:     pub fn kind(&self) -> Prefix<'a> {\n   460:         self.parsed\n   461:     }\n   462: \n   463:     /// Returns the raw [`OsStr`] slice for this prefix.\n   464:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   465:     #[must_use]\n   466:     #[inline]\n   467:     pub fn as_os_str(&self) -> &'a OsStr {\n   468:         self.raw\n   469:     }\n   470: }\n   471: \n   472: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   473: impl<'a> PartialEq for PrefixComponent<'a> {\n   474:     #[inline]\n   475:     fn eq(&self, other: &PrefixComponent<'a>) -> bool {\n   476:         self.parsed == other.parsed\n   477:     }\n   478: }\n   479: \n   480: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   481: impl<'a> PartialOrd for PrefixComponent<'a> {\n   482:     #[inline]\n   483:     fn partial_cmp(&self, other: &PrefixComponent<'a>) -> Option<cmp::Ordering> {",
    "nanvix_source": "   457:     #[must_use]\n   458:     #[inline]\n   459:     pub fn kind(&self) -> Prefix<'a> {\n   460:         self.parsed\n   461:     }\n   462: \n   463:     /// Returns the raw [`OsStr`] slice for this prefix.\n   464:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   465:     #[must_use]\n   466:     #[inline]\n   467:     pub fn as_os_str(&self) -> &'a OsStr {\n   468:         self.raw\n   469:     }\n   470: }\n   471: \n   472: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   473: impl<'a> PartialEq for PrefixComponent<'a> {\n   474:     #[inline]\n   475:     fn eq(&self, other: &PrefixComponent<'a>) -> bool {\n   476:         self.parsed == other.parsed\n   477:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PrefixComponent::kind",
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
      "name": "kind",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 6754,
            "path": "PrefixComponent"
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "lifetime": {
                  "outlives": []
                }
              },
              "name": "'a"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "std:6755",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:6754",
        "resolved_owner_path": [
          "std",
          "path",
          "PrefixComponent"
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
                    "lifetime": "'a"
                  }
                ],
                "constraints": []
              }
            },
            "id": 6710,
            "path": "Prefix"
          }
        }
      }
    },
    "verification_source": "   443: pub struct PrefixComponent<'a> {\n   444:     /// The prefix as an unparsed `OsStr` slice.\n   445:     raw: &'a OsStr,\n   446: \n   447:     /// The parsed prefix data.\n   448:     parsed: Prefix<'a>,\n   449: }\n   450: \n   451: impl<'a> PrefixComponent<'a> {\n   452:     /// Returns the parsed prefix data.\n   453:     ///\n   454:     /// See [`Prefix`]'s documentation for more information on the different\n   455:     /// kinds of prefixes.\n   456:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   457:     #[must_use]\n   458:     #[inline]\n   459:     pub fn kind(&self) -> Prefix<'a> {\n   460:         self.parsed\n   461:     }\n   462: \n   463:     /// Returns the raw [`OsStr`] slice for this prefix.\n   464:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   465:     #[must_use]\n   466:     #[inline]\n   467:     pub fn as_os_str(&self) -> &'a OsStr {\n   468:         self.raw\n   469:     }\n   470: }\n   471: \n   472: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   473: impl<'a> PartialEq for PrefixComponent<'a> {\n   474:     #[inline]\n   475:     fn eq(&self, other: &PrefixComponent<'a>) -> bool {",
    "nanvix_source": "   449: }\n   450: \n   451: impl<'a> PrefixComponent<'a> {\n   452:     /// Returns the parsed prefix data.\n   453:     ///\n   454:     /// See [`Prefix`]'s documentation for more information on the different\n   455:     /// kinds of prefixes.\n   456:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   457:     #[must_use]\n   458:     #[inline]\n   459:     pub fn kind(&self) -> Prefix<'a> {\n   460:         self.parsed\n   461:     }\n   462: \n   463:     /// Returns the raw [`OsStr`] slice for this prefix.\n   464:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   465:     #[must_use]\n   466:     #[inline]\n   467:     pub fn as_os_str(&self) -> &'a OsStr {\n   468:         self.raw\n   469:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::absolute",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
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
                      "modifier": "none",
                      "trait": {
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 1802,
                                    "path": "Path"
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
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "absolute",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "path",
            {
              "generic": "P"
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
                        "id": 1799,
                        "path": "PathBuf"
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
    "verification_source": "  4079: ///     assert_eq!(absolute, Path::new(\"/foo/test/../bar.rs\"));\n  4080: ///     Ok(())\n  4081: /// }\n  4082: /// # #[cfg(not(unix))]\n  4083: /// # fn main() {}\n  4084: /// ```\n  4085: ///\n  4086: /// ## Windows paths\n  4087: ///\n  4088: /// ```\n  4089: /// # #[cfg(windows)]\n  4090: /// fn main() -> std::io::Result<()> {\n  4091: ///     use std::path::{self, Path};\n  4092: ///\n  4093: ///     // Relative to absolute\n  4094: ///     let absolute = path::absolute(\"foo/./bar\")?;\n  4095: ///     assert!(absolute.ends_with(r\"foo\\bar\"));\n  4096: ///\n  4097: ///     // Absolute to absolute\n  4098: ///     let absolute = path::absolute(r\"C:\\foo//test\\..\\./bar.rs\")?;\n  4099: ///\n  4100: ///     assert_eq!(absolute, Path::new(r\"C:\\foo\\bar.rs\"));\n  4101: ///     Ok(())\n  4102: /// }\n  4103: /// # #[cfg(not(windows))]\n  4104: /// # fn main() {}\n  4105: /// ```\n  4106: ///\n  4107: /// Note that this [may change in the future][changes].\n  4108: ///\n  4109: /// [changes]: io#platform-specific-behavior\n  4110: /// [posix-semantics]: https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_13\n  4111: /// [windows-path]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfullpathnamew",
    "nanvix_source": "  4115: ///\n  4116: /// ## Windows paths\n  4117: ///\n  4118: /// ```\n  4119: /// # #[cfg(windows)]\n  4120: /// fn main() -> std::io::Result<()> {\n  4121: ///     use std::path::{self, Path};\n  4122: ///\n  4123: ///     // Relative to absolute\n  4124: ///     let absolute = path::absolute(\"foo/./bar\")?;\n  4125: ///     assert!(absolute.ends_with(r\"foo\\bar\"));\n  4126: ///\n  4127: ///     // Absolute to absolute\n  4128: ///     let absolute = path::absolute(r\"C:\\foo//test\\..\\./bar.rs\")?;\n  4129: ///\n  4130: ///     assert_eq!(absolute, Path::new(r\"C:\\foo\\bar.rs\"));\n  4131: ///     Ok(())\n  4132: /// }\n  4133: /// # #[cfg(not(windows))]\n  4134: /// # fn main() {}\n  4135: /// ```",
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
