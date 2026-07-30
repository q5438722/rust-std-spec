For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::Write::write_all",
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
      "name": "write_all",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
            "buf",
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1841:     /// [`write`]: Write::write\n  1842:     ///\n  1843:     /// # Examples\n  1844:     ///\n  1845:     /// ```no_run\n  1846:     /// use std::io::prelude::*;\n  1847:     /// use std::fs::File;\n  1848:     ///\n  1849:     /// fn main() -> std::io::Result<()> {\n  1850:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1851:     ///\n  1852:     ///     buffer.write_all(b\"some bytes\")?;\n  1853:     ///     Ok(())\n  1854:     /// }\n  1855:     /// ```\n  1856:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1857:     fn write_all(&mut self, mut buf: &[u8]) -> Result<()> {\n  1858:         while !buf.is_empty() {\n  1859:             match self.write(buf) {\n  1860:                 Ok(0) => {\n  1861:                     return Err(Error::WRITE_ALL_EOF);\n  1862:                 }\n  1863:                 Ok(n) => buf = &buf[n..],\n  1864:                 Err(ref e) if e.is_interrupted() => {}\n  1865:                 Err(e) => return Err(e),\n  1866:             }\n  1867:         }\n  1868:         Ok(())\n  1869:     }\n  1870: \n  1871:     /// Attempts to write multiple buffers into this writer.\n  1872:     ///\n  1873:     /// This method will continuously call [`write_vectored`] until there is no",
    "nanvix_source": "  1602:     /// use std::fs::File;\n  1603:     ///\n  1604:     /// fn main() -> std::io::Result<()> {\n  1605:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1606:     ///\n  1607:     ///     buffer.write_all(b\"some bytes\")?;\n  1608:     ///     Ok(())\n  1609:     /// }\n  1610:     /// ```\n  1611:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1612:     fn write_all(&mut self, mut buf: &[u8]) -> Result<()> {\n  1613:         while !buf.is_empty() {\n  1614:             match self.write(buf) {\n  1615:                 Ok(0) => {\n  1616:                     return Err(Error::WRITE_ALL_EOF);\n  1617:                 }\n  1618:                 Ok(n) => buf = &buf[n..],\n  1619:                 Err(ref e) if e.is_interrupted() => {}\n  1620:                 Err(e) => return Err(e),\n  1621:             }\n  1622:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Write::write_fmt",
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
      "name": "write_fmt",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
            "args",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'_"
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 3369,
                "path": "fmt::Arguments"
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
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1956:     ///\n  1957:     /// ```no_run\n  1958:     /// use std::io::prelude::*;\n  1959:     /// use std::fs::File;\n  1960:     ///\n  1961:     /// fn main() -> std::io::Result<()> {\n  1962:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1963:     ///\n  1964:     ///     // this call\n  1965:     ///     write!(buffer, \"{:.*}\", 2, 1.234567)?;\n  1966:     ///     // turns into this:\n  1967:     ///     buffer.write_fmt(format_args!(\"{:.*}\", 2, 1.234567))?;\n  1968:     ///     Ok(())\n  1969:     /// }\n  1970:     /// ```\n  1971:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1972:     fn write_fmt(&mut self, args: fmt::Arguments<'_>) -> Result<()> {\n  1973:         if let Some(s) = args.as_statically_known_str() {\n  1974:             self.write_all(s.as_bytes())\n  1975:         } else {\n  1976:             default_write_fmt(self, args)\n  1977:         }\n  1978:     }\n  1979: \n  1980:     /// Creates a \"by reference\" adapter for this instance of `Write`.\n  1981:     ///\n  1982:     /// The returned adapter also implements `Write` and will simply borrow this\n  1983:     /// current writer.\n  1984:     ///\n  1985:     /// # Examples\n  1986:     ///\n  1987:     /// ```no_run\n  1988:     /// use std::io::Write;",
    "nanvix_source": "  1717:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1718:     ///\n  1719:     ///     // this call\n  1720:     ///     write!(buffer, \"{:.*}\", 2, 1.234567)?;\n  1721:     ///     // turns into this:\n  1722:     ///     buffer.write_fmt(format_args!(\"{:.*}\", 2, 1.234567))?;\n  1723:     ///     Ok(())\n  1724:     /// }\n  1725:     /// ```\n  1726:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1727:     fn write_fmt(&mut self, args: fmt::Arguments<'_>) -> Result<()> {\n  1728:         if let Some(s) = args.as_statically_known_str() {\n  1729:             self.write_all(s.as_bytes())\n  1730:         } else {\n  1731:             default_write_fmt(self, args)\n  1732:         }\n  1733:     }\n  1734: \n  1735:     /// Creates a \"by reference\" adapter for this instance of `Write`.\n  1736:     ///\n  1737:     /// The returned adapter also implements `Write` and will simply borrow this",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::Write::write_vectored",
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
      "name": "write_vectored",
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
        "item_id": "std:2630",
        "kind": "trait",
        "name": "Write",
        "path": [
          "std",
          "io",
          "Write"
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
            "bufs",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "resolved_path": {
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "lifetime": "'_"
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 2624,
                      "path": "IoSlice"
                    }
                  }
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
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 468,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1764:     /// fn main() -> std::io::Result<()> {\n  1765:     ///     let data1 = [1; 8];\n  1766:     ///     let data2 = [15; 8];\n  1767:     ///     let io_slice1 = IoSlice::new(&data1);\n  1768:     ///     let io_slice2 = IoSlice::new(&data2);\n  1769:     ///\n  1770:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1771:     ///\n  1772:     ///     // Writes some prefix of the byte string, not necessarily all of it.\n  1773:     ///     buffer.write_vectored(&[io_slice1, io_slice2])?;\n  1774:     ///     Ok(())\n  1775:     /// }\n  1776:     /// ```\n  1777:     ///\n  1778:     /// [`write`]: Write::write\n  1779:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n  1780:     fn write_vectored(&mut self, bufs: &[IoSlice<'_>]) -> Result<usize> {\n  1781:         default_write_vectored(|b| self.write(b), bufs)\n  1782:     }\n  1783: \n  1784:     /// Determines if this `Write`r has an efficient [`write_vectored`]\n  1785:     /// implementation.\n  1786:     ///\n  1787:     /// If a `Write`r does not override the default [`write_vectored`]\n  1788:     /// implementation, code using it may want to avoid the method all together\n  1789:     /// and coalesce writes into a single buffer for higher performance.\n  1790:     ///\n  1791:     /// The default implementation returns `false`.\n  1792:     ///\n  1793:     /// [`write_vectored`]: Write::write_vectored\n  1794:     #[unstable(feature = \"can_vector\", issue = \"69941\")]\n  1795:     fn is_write_vectored(&self) -> bool {\n  1796:         false",
    "nanvix_source": "  1525:     ///     let mut buffer = File::create(\"foo.txt\")?;\n  1526:     ///\n  1527:     ///     // Writes some prefix of the byte string, not necessarily all of it.\n  1528:     ///     buffer.write_vectored(&[io_slice1, io_slice2])?;\n  1529:     ///     Ok(())\n  1530:     /// }\n  1531:     /// ```\n  1532:     ///\n  1533:     /// [`write`]: Write::write\n  1534:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n  1535:     fn write_vectored(&mut self, bufs: &[IoSlice<'_>]) -> Result<usize> {\n  1536:         default_write_vectored(|b| self.write(b), bufs)\n  1537:     }\n  1538: \n  1539:     /// Determines if this `Write`r has an efficient [`write_vectored`]\n  1540:     /// implementation.\n  1541:     ///\n  1542:     /// If a `Write`r does not override the default [`write_vectored`]\n  1543:     /// implementation, code using it may want to avoid the method all together\n  1544:     /// and coalesce writes into a single buffer for higher performance.\n  1545:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::ToSocketAddrs::to_socket_addrs",
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
      "name": "to_socket_addrs",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:1888",
        "kind": "trait",
        "name": "ToSocketAddrs",
        "path": [
          "std",
          "net",
          "socket_addr",
          "ToSocketAddrs"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "qualified_path": {
                        "args": null,
                        "name": "Iter",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 1888,
                          "path": ""
                        }
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
    "verification_source": "   119: /// [`TcpStream::connect`]: crate::net::TcpStream::connect\n   120: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   121: pub trait ToSocketAddrs {\n   122:     /// Returned iterator over socket addresses which this type may correspond\n   123:     /// to.\n   124:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   125:     type Iter: Iterator<Item = SocketAddr>;\n   126: \n   127:     /// Converts this object to an iterator of resolved [`SocketAddr`]s.\n   128:     ///\n   129:     /// The returned iterator might not actually yield any values depending on the\n   130:     /// outcome of any resolution performed.\n   131:     ///\n   132:     /// Note that this function may block the current thread while resolution is\n   133:     /// performed.\n   134:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   135:     fn to_socket_addrs(&self) -> io::Result<Self::Iter>;\n   136: }\n   137: \n   138: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   139: impl ToSocketAddrs for SocketAddr {\n   140:     type Iter = option::IntoIter<SocketAddr>;\n   141:     fn to_socket_addrs(&self) -> io::Result<option::IntoIter<SocketAddr>> {\n   142:         Ok(Some(*self).into_iter())\n   143:     }\n   144: }\n   145: \n   146: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   147: impl ToSocketAddrs for SocketAddrV4 {\n   148:     type Iter = option::IntoIter<SocketAddr>;\n   149:     fn to_socket_addrs(&self) -> io::Result<option::IntoIter<SocketAddr>> {\n   150:         SocketAddr::V4(*self).to_socket_addrs()\n   151:     }",
    "nanvix_source": "   125:     type Iter: Iterator<Item = SocketAddr>;\n   126: \n   127:     /// Converts this object to an iterator of resolved [`SocketAddr`]s.\n   128:     ///\n   129:     /// The returned iterator might not actually yield any values depending on the\n   130:     /// outcome of any resolution performed.\n   131:     ///\n   132:     /// Note that this function may block the current thread while resolution is\n   133:     /// performed.\n   134:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   135:     fn to_socket_addrs(&self) -> io::Result<Self::Iter>;\n   136: }\n   137: \n   138: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   139: impl ToSocketAddrs for SocketAddr {\n   140:     type Iter = option::IntoIter<SocketAddr>;\n   141:     fn to_socket_addrs(&self) -> io::Result<option::IntoIter<SocketAddr>> {\n   142:         Ok(Some(*self).into_iter())\n   143:     }\n   144: }\n   145: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::AsFd::as_fd",
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
      "name": "as_fd",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2700",
        "kind": "trait",
        "name": "AsFd",
        "path": [
          "std",
          "os",
          "fd",
          "owned",
          "AsFd"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 2698,
            "path": "BorrowedFd"
          }
        }
      }
    },
    "verification_source": "   262:     /// Borrows the file descriptor.\n   263:     ///\n   264:     /// # Example\n   265:     ///\n   266:     /// ```rust,no_run\n   267:     /// use std::fs::File;\n   268:     /// # use std::io;\n   269:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   270:     /// # use std::os::fd::{AsFd, BorrowedFd};\n   271:     ///\n   272:     /// let mut f = File::open(\"foo.txt\")?;\n   273:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   274:     /// let borrowed_fd: BorrowedFd<'_> = f.as_fd();\n   275:     /// # Ok::<(), io::Error>(())\n   276:     /// ```\n   277:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   278:     fn as_fd(&self) -> BorrowedFd<'_>;\n   279: }\n   280: \n   281: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   282: impl<T: AsFd + ?Sized> AsFd for &T {\n   283:     #[inline]\n   284:     fn as_fd(&self) -> BorrowedFd<'_> {\n   285:         T::as_fd(self)\n   286:     }\n   287: }\n   288: \n   289: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   290: impl<T: AsFd + ?Sized> AsFd for &mut T {\n   291:     #[inline]\n   292:     fn as_fd(&self) -> BorrowedFd<'_> {\n   293:         T::as_fd(self)\n   294:     }",
    "nanvix_source": "   265:     /// # use std::io;\n   266:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   267:     /// # use std::os::fd::{AsFd, BorrowedFd};\n   268:     ///\n   269:     /// let mut f = File::open(\"foo.txt\")?;\n   270:     /// # #[cfg(any(unix, target_os = \"wasi\"))]\n   271:     /// let borrowed_fd: BorrowedFd<'_> = f.as_fd();\n   272:     /// # Ok::<(), io::Error>(())\n   273:     /// ```\n   274:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   275:     fn as_fd(&self) -> BorrowedFd<'_>;\n   276: }\n   277: \n   278: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   279: impl<T: AsFd + ?Sized> AsFd for &T {\n   280:     #[inline]\n   281:     fn as_fd(&self) -> BorrowedFd<'_> {\n   282:         T::as_fd(self)\n   283:     }\n   284: }\n   285: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::AsRawFd::as_raw_fd",
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
      "name": "as_raw_fd",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2690",
        "kind": "trait",
        "name": "AsRawFd",
        "path": [
          "std",
          "os",
          "fd",
          "raw",
          "AsRawFd"
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
          "resolved_path": {
            "args": null,
            "id": 2688,
            "path": "RawFd"
          }
        }
      }
    },
    "verification_source": "    53:     ///\n    54:     /// # Example\n    55:     ///\n    56:     /// ```no_run\n    57:     /// use std::fs::File;\n    58:     /// # use std::io;\n    59:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n    60:     /// use std::os::fd::{AsRawFd, RawFd};\n    61:     ///\n    62:     /// let mut f = File::open(\"foo.txt\")?;\n    63:     /// // Note that `raw_fd` is only valid as long as `f` exists.\n    64:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n    65:     /// let raw_fd: RawFd = f.as_raw_fd();\n    66:     /// # Ok::<(), io::Error>(())\n    67:     /// ```\n    68:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    69:     fn as_raw_fd(&self) -> RawFd;\n    70: }\n    71: \n    72: /// A trait to express the ability to construct an object from a raw file\n    73: /// descriptor.\n    74: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    75: pub trait FromRawFd {\n    76:     /// Constructs a new instance of `Self` from the given raw file\n    77:     /// descriptor.\n    78:     ///\n    79:     /// This function is typically used to **consume ownership** of the\n    80:     /// specified file descriptor. When used in this way, the returned object\n    81:     /// will take responsibility for closing it when the object goes out of\n    82:     /// scope.\n    83:     ///\n    84:     /// However, consuming ownership is not strictly required. Use a\n    85:     /// [`From<OwnedFd>::from`] implementation for an API which strictly",
    "nanvix_source": "    59:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n    60:     /// use std::os::fd::{AsRawFd, RawFd};\n    61:     ///\n    62:     /// let mut f = File::open(\"foo.txt\")?;\n    63:     /// // Note that `raw_fd` is only valid as long as `f` exists.\n    64:     /// #[cfg(any(unix, target_os = \"wasi\"))]\n    65:     /// let raw_fd: RawFd = f.as_raw_fd();\n    66:     /// # Ok::<(), io::Error>(())\n    67:     /// ```\n    68:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    69:     fn as_raw_fd(&self) -> RawFd;\n    70: }\n    71: \n    72: /// A trait to express the ability to construct an object from a raw file\n    73: /// descriptor.\n    74: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    75: pub trait FromRawFd {\n    76:     /// Constructs a new instance of `Self` from the given raw file\n    77:     /// descriptor.\n    78:     ///\n    79:     /// This function is typically used to **consume ownership** of the",
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
