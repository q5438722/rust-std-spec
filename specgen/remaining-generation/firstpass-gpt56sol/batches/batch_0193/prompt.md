For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::OpenOptions::append",
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
      "external_or_hidden_runtime_state",
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
      "name": "append",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "append",
            {
              "primitive": "bool"
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
    "verification_source": "  1769:     ///\n  1770:     /// [`write()`]: Write::write \"io::Write::write\"\n  1771:     /// [`flush()`]: Write::flush \"io::Write::flush\"\n  1772:     /// [stream_position]: Seek::stream_position \"io::Seek::stream_position\"\n  1773:     /// [seek]: Seek::seek \"io::Seek::seek\"\n  1774:     /// [Current]: SeekFrom::Current \"io::SeekFrom::Current\"\n  1775:     /// [End]: SeekFrom::End \"io::SeekFrom::End\"\n  1776:     ///\n  1777:     /// # Examples\n  1778:     ///\n  1779:     /// ```no_run\n  1780:     /// use std::fs::OpenOptions;\n  1781:     ///\n  1782:     /// let file = OpenOptions::new().append(true).open(\"foo.txt\");\n  1783:     /// ```\n  1784:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1785:     pub fn append(&mut self, append: bool) -> &mut Self {\n  1786:         self.0.append(append);\n  1787:         self\n  1788:     }\n  1789: \n  1790:     /// Sets the option for truncating a previous file.\n  1791:     ///\n  1792:     /// If a file is successfully opened with this option set to true, it will truncate\n  1793:     /// the file to 0 length if it already exists.\n  1794:     ///\n  1795:     /// The file must be opened with write access for truncate to work.\n  1796:     ///\n  1797:     /// # Examples\n  1798:     ///\n  1799:     /// ```no_run\n  1800:     /// use std::fs::OpenOptions;\n  1801:     ///",
    "nanvix_source": "  1744:     /// [End]: SeekFrom::End \"io::SeekFrom::End\"\n  1745:     ///\n  1746:     /// # Examples\n  1747:     ///\n  1748:     /// ```no_run\n  1749:     /// use std::fs::OpenOptions;\n  1750:     ///\n  1751:     /// let file = OpenOptions::new().append(true).open(\"foo.txt\");\n  1752:     /// ```\n  1753:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1754:     pub fn append(&mut self, append: bool) -> &mut Self {\n  1755:         self.0.append(append);\n  1756:         self\n  1757:     }\n  1758: \n  1759:     /// Sets the option for truncating a previous file.\n  1760:     ///\n  1761:     /// If a file is successfully opened with this option set to true, it will truncate\n  1762:     /// the file to 0 length if it already exists.\n  1763:     ///\n  1764:     /// The file must be opened with write access for truncate to work.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::create",
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
      "external_or_hidden_runtime_state",
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
      "name": "create",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "create",
            {
              "primitive": "bool"
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
    "verification_source": "  1814:     ///\n  1815:     /// See also [`std::fs::write()`][self::write] for a simple function to\n  1816:     /// create a file with some given data.\n  1817:     ///\n  1818:     /// # Errors\n  1819:     ///\n  1820:     /// If `.create(true)` is set without `.write(true)` or `.append(true)`,\n  1821:     /// calling [`open`](Self::open) will fail with [`InvalidInput`](io::ErrorKind::InvalidInput) error.\n  1822:     /// # Examples\n  1823:     ///\n  1824:     /// ```no_run\n  1825:     /// use std::fs::OpenOptions;\n  1826:     ///\n  1827:     /// let file = OpenOptions::new().write(true).create(true).open(\"foo.txt\");\n  1828:     /// ```\n  1829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1830:     pub fn create(&mut self, create: bool) -> &mut Self {\n  1831:         self.0.create(create);\n  1832:         self\n  1833:     }\n  1834: \n  1835:     /// Sets the option to create a new file, failing if it already exists.\n  1836:     ///\n  1837:     /// No file is allowed to exist at the target location, also no (dangling) symlink. In this\n  1838:     /// way, if the call succeeds, the file returned is guaranteed to be new.\n  1839:     /// If a file exists at the target location, creating a new file will fail with [`AlreadyExists`]\n  1840:     /// or another error based on the situation. See [`OpenOptions::open`] for a\n  1841:     /// non-exhaustive list of likely errors.\n  1842:     ///\n  1843:     /// This option is useful because it is atomic. Otherwise between checking\n  1844:     /// whether a file exists and creating a new one, the file may have been\n  1845:     /// created by another process (a [TOCTOU] race condition / attack).\n  1846:     ///",
    "nanvix_source": "  1789:     /// If `.create(true)` is set without `.write(true)` or `.append(true)`,\n  1790:     /// calling [`open`](Self::open) will fail with [`InvalidInput`](io::ErrorKind::InvalidInput) error.\n  1791:     /// # Examples\n  1792:     ///\n  1793:     /// ```no_run\n  1794:     /// use std::fs::OpenOptions;\n  1795:     ///\n  1796:     /// let file = OpenOptions::new().write(true).create(true).open(\"foo.txt\");\n  1797:     /// ```\n  1798:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1799:     pub fn create(&mut self, create: bool) -> &mut Self {\n  1800:         self.0.create(create);\n  1801:         self\n  1802:     }\n  1803: \n  1804:     /// Sets the option to create a new file, failing if it already exists.\n  1805:     ///\n  1806:     /// No file is allowed to exist at the target location, also no (dangling) symlink. In this\n  1807:     /// way, if the call succeeds, the file returned is guaranteed to be new.\n  1808:     /// If a file exists at the target location, creating a new file will fail with [`AlreadyExists`]\n  1809:     /// or another error based on the situation. See [`OpenOptions::open`] for a",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::create_new",
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
      "external_or_hidden_runtime_state",
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
      "name": "create_new",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "create_new",
            {
              "primitive": "bool"
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
    "verification_source": "  1852:     ///\n  1853:     /// [`.create()`]: OpenOptions::create\n  1854:     /// [`.truncate()`]: OpenOptions::truncate\n  1855:     /// [`AlreadyExists`]: io::ErrorKind::AlreadyExists\n  1856:     /// [TOCTOU]: self#time-of-check-to-time-of-use-toctou\n  1857:     ///\n  1858:     /// # Examples\n  1859:     ///\n  1860:     /// ```no_run\n  1861:     /// use std::fs::OpenOptions;\n  1862:     ///\n  1863:     /// let file = OpenOptions::new().write(true)\n  1864:     ///                              .create_new(true)\n  1865:     ///                              .open(\"foo.txt\");\n  1866:     /// ```\n  1867:     #[stable(feature = \"expand_open_options2\", since = \"1.9.0\")]\n  1868:     pub fn create_new(&mut self, create_new: bool) -> &mut Self {\n  1869:         self.0.create_new(create_new);\n  1870:         self\n  1871:     }\n  1872: \n  1873:     /// Opens a file at `path` with the options specified by `self`.\n  1874:     ///\n  1875:     /// # Errors\n  1876:     ///\n  1877:     /// This function will return an error under a number of different\n  1878:     /// circumstances. Some of these error conditions are listed here, together\n  1879:     /// with their [`io::ErrorKind`]. The mapping to [`io::ErrorKind`]s is not\n  1880:     /// part of the compatibility contract of the function.\n  1881:     ///\n  1882:     /// * [`NotFound`]: The specified file does not exist and neither `create`\n  1883:     ///   or `create_new` is set.\n  1884:     /// * [`NotFound`]: One of the directory components of the file path does",
    "nanvix_source": "  1827:     /// # Examples\n  1828:     ///\n  1829:     /// ```no_run\n  1830:     /// use std::fs::OpenOptions;\n  1831:     ///\n  1832:     /// let file = OpenOptions::new().write(true)\n  1833:     ///                              .create_new(true)\n  1834:     ///                              .open(\"foo.txt\");\n  1835:     /// ```\n  1836:     #[stable(feature = \"expand_open_options2\", since = \"1.9.0\")]\n  1837:     pub fn create_new(&mut self, create_new: bool) -> &mut Self {\n  1838:         self.0.create_new(create_new);\n  1839:         self\n  1840:     }\n  1841: \n  1842:     /// Opens a file at `path` with the options specified by `self`.\n  1843:     ///\n  1844:     /// # Errors\n  1845:     ///\n  1846:     /// This function will return an error under a number of different\n  1847:     /// circumstances. Some of these error conditions are listed here, together",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::new",
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
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
    "verification_source": "  1678: impl OpenOptions {\n  1679:     /// Creates a blank new set of options ready for configuration.\n  1680:     ///\n  1681:     /// All options are initially set to `false`.\n  1682:     ///\n  1683:     /// # Examples\n  1684:     ///\n  1685:     /// ```no_run\n  1686:     /// use std::fs::OpenOptions;\n  1687:     ///\n  1688:     /// let mut options = OpenOptions::new();\n  1689:     /// let file = options.read(true).open(\"foo.txt\");\n  1690:     /// ```\n  1691:     #[cfg_attr(not(test), rustc_diagnostic_item = \"open_options_new\")]\n  1692:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1693:     #[must_use]\n  1694:     pub fn new() -> Self {\n  1695:         OpenOptions(fs_imp::OpenOptions::new())\n  1696:     }\n  1697: \n  1698:     /// Sets the option for read access.\n  1699:     ///\n  1700:     /// This option, when true, will indicate that the file should be\n  1701:     /// `read`-able if opened.\n  1702:     ///\n  1703:     /// # Examples\n  1704:     ///\n  1705:     /// ```no_run\n  1706:     /// use std::fs::OpenOptions;\n  1707:     ///\n  1708:     /// let file = OpenOptions::new().read(true).open(\"foo.txt\");\n  1709:     /// ```\n  1710:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "  1653:     ///\n  1654:     /// ```no_run\n  1655:     /// use std::fs::OpenOptions;\n  1656:     ///\n  1657:     /// let mut options = OpenOptions::new();\n  1658:     /// let file = options.read(true).open(\"foo.txt\");\n  1659:     /// ```\n  1660:     #[cfg_attr(not(test), rustc_diagnostic_item = \"open_options_new\")]\n  1661:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1662:     #[must_use]\n  1663:     pub fn new() -> Self {\n  1664:         OpenOptions(fs_imp::OpenOptions::new())\n  1665:     }\n  1666: \n  1667:     /// Sets the option for read access.\n  1668:     ///\n  1669:     /// This option, when true, will indicate that the file should be\n  1670:     /// `read`-able if opened.\n  1671:     ///\n  1672:     /// # Examples\n  1673:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::open",
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
      "name": "open",
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
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
          ],
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
                        "id": 2556,
                        "path": "File"
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
    "verification_source": "  1901:     ///   open files, too long filename, too many symbolic links in the\n  1902:     ///   specified path (Unix-like systems only), etc.\n  1903:     ///\n  1904:     /// # Examples\n  1905:     ///\n  1906:     /// ```no_run\n  1907:     /// use std::fs::OpenOptions;\n  1908:     ///\n  1909:     /// let file = OpenOptions::new().read(true).open(\"foo.txt\");\n  1910:     /// ```\n  1911:     ///\n  1912:     /// [`AlreadyExists`]: io::ErrorKind::AlreadyExists\n  1913:     /// [`InvalidInput`]: io::ErrorKind::InvalidInput\n  1914:     /// [`NotFound`]: io::ErrorKind::NotFound\n  1915:     /// [`PermissionDenied`]: io::ErrorKind::PermissionDenied\n  1916:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1917:     pub fn open<P: AsRef<Path>>(&self, path: P) -> io::Result<File> {\n  1918:         self._open(path.as_ref())\n  1919:     }\n  1920: \n  1921:     fn _open(&self, path: &Path) -> io::Result<File> {\n  1922:         fs_imp::File::open(path, &self.0).map(|inner| File { inner })\n  1923:     }\n  1924: }\n  1925: \n  1926: impl AsInner<fs_imp::OpenOptions> for OpenOptions {\n  1927:     #[inline]\n  1928:     fn as_inner(&self) -> &fs_imp::OpenOptions {\n  1929:         &self.0\n  1930:     }\n  1931: }\n  1932: \n  1933: impl AsInnerMut<fs_imp::OpenOptions> for OpenOptions {",
    "nanvix_source": "  1876:     /// use std::fs::OpenOptions;\n  1877:     ///\n  1878:     /// let file = OpenOptions::new().read(true).open(\"foo.txt\");\n  1879:     /// ```\n  1880:     ///\n  1881:     /// [`AlreadyExists`]: io::ErrorKind::AlreadyExists\n  1882:     /// [`InvalidInput`]: io::ErrorKind::InvalidInput\n  1883:     /// [`NotFound`]: io::ErrorKind::NotFound\n  1884:     /// [`PermissionDenied`]: io::ErrorKind::PermissionDenied\n  1885:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1886:     pub fn open<P: AsRef<Path>>(&self, path: P) -> io::Result<File> {\n  1887:         self._open(path.as_ref())\n  1888:     }\n  1889: \n  1890:     fn _open(&self, path: &Path) -> io::Result<File> {\n  1891:         fs_imp::File::open(path, &self.0).map(|inner| File { inner })\n  1892:     }\n  1893: }\n  1894: \n  1895: impl AsInner<fs_imp::OpenOptions> for OpenOptions {\n  1896:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::OpenOptions::read",
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
      "external_or_hidden_runtime_state",
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
      "name": "read",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 2571,
            "path": "OpenOptions"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2951",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2571",
        "resolved_owner_path": [
          "std",
          "fs",
          "OpenOptions"
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
            "read",
            {
              "primitive": "bool"
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
    "verification_source": "  1695:         OpenOptions(fs_imp::OpenOptions::new())\n  1696:     }\n  1697: \n  1698:     /// Sets the option for read access.\n  1699:     ///\n  1700:     /// This option, when true, will indicate that the file should be\n  1701:     /// `read`-able if opened.\n  1702:     ///\n  1703:     /// # Examples\n  1704:     ///\n  1705:     /// ```no_run\n  1706:     /// use std::fs::OpenOptions;\n  1707:     ///\n  1708:     /// let file = OpenOptions::new().read(true).open(\"foo.txt\");\n  1709:     /// ```\n  1710:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1711:     pub fn read(&mut self, read: bool) -> &mut Self {\n  1712:         self.0.read(read);\n  1713:         self\n  1714:     }\n  1715: \n  1716:     /// Sets the option for write access.\n  1717:     ///\n  1718:     /// This option, when true, will indicate that the file should be\n  1719:     /// `write`-able if opened.\n  1720:     ///\n  1721:     /// If the file already exists, any write calls on it will overwrite its\n  1722:     /// contents, without truncating it.\n  1723:     ///\n  1724:     /// # Examples\n  1725:     ///\n  1726:     /// ```no_run\n  1727:     /// use std::fs::OpenOptions;",
    "nanvix_source": "  1670:     /// `read`-able if opened.\n  1671:     ///\n  1672:     /// # Examples\n  1673:     ///\n  1674:     /// ```no_run\n  1675:     /// use std::fs::OpenOptions;\n  1676:     ///\n  1677:     /// let file = OpenOptions::new().read(true).open(\"foo.txt\");\n  1678:     /// ```\n  1679:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1680:     pub fn read(&mut self, read: bool) -> &mut Self {\n  1681:         self.0.read(read);\n  1682:         self\n  1683:     }\n  1684: \n  1685:     /// Sets the option for write access.\n  1686:     ///\n  1687:     /// This option, when true, will indicate that the file should be\n  1688:     /// `write`-able if opened.\n  1689:     ///\n  1690:     /// If the file already exists, any write calls on it will overwrite its",
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
