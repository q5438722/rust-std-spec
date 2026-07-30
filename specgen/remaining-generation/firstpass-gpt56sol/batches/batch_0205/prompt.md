For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::TcpListener::only_v6",
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
      "name": "only_v6",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
                      "primitive": "bool"
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
    "verification_source": "   944:     /// ```\n   945:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   946:     pub fn ttl(&self) -> io::Result<u32> {\n   947:         self.0.ttl()\n   948:     }\n   949: \n   950:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   951:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   952:     #[allow(missing_docs)]\n   953:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n   954:         self.0.set_only_v6(only_v6)\n   955:     }\n   956: \n   957:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   958:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   959:     #[allow(missing_docs)]\n   960:     pub fn only_v6(&self) -> io::Result<bool> {\n   961:         self.0.only_v6()\n   962:     }\n   963: \n   964:     /// Gets the value of the `SO_ERROR` option on this socket.\n   965:     ///\n   966:     /// This will retrieve the stored error in the underlying socket, clearing\n   967:     /// the field in the process. This can be useful for checking errors between\n   968:     /// calls.\n   969:     ///\n   970:     /// # Examples\n   971:     ///\n   972:     /// ```no_run\n   973:     /// use std::net::TcpListener;\n   974:     ///\n   975:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   976:     /// listener.take_error().expect(\"No error was expected\");",
    "nanvix_source": "  1034:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1035:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n  1036:     #[allow(missing_docs)]\n  1037:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n  1038:         self.0.set_only_v6(only_v6)\n  1039:     }\n  1040: \n  1041:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1042:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n  1043:     #[allow(missing_docs)]\n  1044:     pub fn only_v6(&self) -> io::Result<bool> {\n  1045:         self.0.only_v6()\n  1046:     }\n  1047: \n  1048:     /// Gets the value of the `SO_ERROR` option on this socket.\n  1049:     ///\n  1050:     /// This will retrieve the stored error in the underlying socket, clearing\n  1051:     /// the field in the process. This can be useful for checking errors between\n  1052:     /// calls.\n  1053:     ///\n  1054:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::set_nonblocking",
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
      "name": "set_nonblocking",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
            "nonblocking",
            {
              "primitive": "bool"
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
    "verification_source": "  1010:     ///     match stream {\n  1011:     ///         Ok(s) => {\n  1012:     ///             // do something with the TcpStream\n  1013:     ///             handle_connection(s);\n  1014:     ///         }\n  1015:     ///         Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {\n  1016:     ///             // wait until network socket is ready, typically implemented\n  1017:     ///             // via platform-specific APIs such as epoll or IOCP\n  1018:     ///             wait_for_fd();\n  1019:     ///             continue;\n  1020:     ///         }\n  1021:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n  1022:     ///     }\n  1023:     /// }\n  1024:     /// ```\n  1025:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1026:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n  1027:         self.0.set_nonblocking(nonblocking)\n  1028:     }\n  1029: }\n  1030: \n  1031: // In addition to the `impl`s here, `TcpListener` also has `impl`s for\n  1032: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n  1033: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n  1034: // `AsSocket`/`From<OwnedSocket>`/`Into<OwnedSocket>` and\n  1035: // `AsRawSocket`/`IntoRawSocket`/`FromRawSocket` on Windows.\n  1036: \n  1037: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1038: impl<'a> Iterator for Incoming<'a> {\n  1039:     type Item = io::Result<TcpStream>;\n  1040:     fn next(&mut self) -> Option<io::Result<TcpStream>> {\n  1041:         Some(self.listener.accept().map(|p| p.0))\n  1042:     }",
    "nanvix_source": "  1100:     ///             // wait until network socket is ready, typically implemented\n  1101:     ///             // via platform-specific APIs such as epoll or IOCP\n  1102:     ///             wait_for_fd();\n  1103:     ///             continue;\n  1104:     ///         }\n  1105:     ///         Err(e) => panic!(\"encountered IO error: {e}\"),\n  1106:     ///     }\n  1107:     /// }\n  1108:     /// ```\n  1109:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1110:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n  1111:         self.0.set_nonblocking(nonblocking)\n  1112:     }\n  1113: }\n  1114: \n  1115: // In addition to the `impl`s here, `TcpListener` also has `impl`s for\n  1116: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n  1117: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n  1118: // `AsSocket`/`From<OwnedSocket>`/`Into<OwnedSocket>` and\n  1119: // `AsRawSocket`/`IntoRawSocket`/`FromRawSocket` on Windows.\n  1120: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::set_only_v6",
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
      "name": "set_only_v6",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
            "only_v6",
            {
              "primitive": "bool"
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
    "verification_source": "   937:     ///\n   938:     /// ```no_run\n   939:     /// use std::net::TcpListener;\n   940:     ///\n   941:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   942:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n   943:     /// assert_eq!(listener.ttl().unwrap_or(0), 100);\n   944:     /// ```\n   945:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   946:     pub fn ttl(&self) -> io::Result<u32> {\n   947:         self.0.ttl()\n   948:     }\n   949: \n   950:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   951:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   952:     #[allow(missing_docs)]\n   953:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n   954:         self.0.set_only_v6(only_v6)\n   955:     }\n   956: \n   957:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   958:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   959:     #[allow(missing_docs)]\n   960:     pub fn only_v6(&self) -> io::Result<bool> {\n   961:         self.0.only_v6()\n   962:     }\n   963: \n   964:     /// Gets the value of the `SO_ERROR` option on this socket.\n   965:     ///\n   966:     /// This will retrieve the stored error in the underlying socket, clearing\n   967:     /// the field in the process. This can be useful for checking errors between\n   968:     /// calls.\n   969:     ///",
    "nanvix_source": "  1027:     /// assert_eq!(listener.ttl().unwrap_or(0), 100);\n  1028:     /// ```\n  1029:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1030:     pub fn ttl(&self) -> io::Result<u32> {\n  1031:         self.0.ttl()\n  1032:     }\n  1033: \n  1034:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1035:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n  1036:     #[allow(missing_docs)]\n  1037:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n  1038:         self.0.set_only_v6(only_v6)\n  1039:     }\n  1040: \n  1041:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1042:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n  1043:     #[allow(missing_docs)]\n  1044:     pub fn only_v6(&self) -> io::Result<bool> {\n  1045:         self.0.only_v6()\n  1046:     }\n  1047: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::set_ttl",
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
      "name": "set_ttl",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
            "ttl",
            {
              "primitive": "u32"
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
    "verification_source": "   912:     }\n   913: \n   914:     /// Sets the value for the `IP_TTL` option on this socket.\n   915:     ///\n   916:     /// This value sets the time-to-live field that is used in every packet sent\n   917:     /// from this socket.\n   918:     ///\n   919:     /// # Examples\n   920:     ///\n   921:     /// ```no_run\n   922:     /// use std::net::TcpListener;\n   923:     ///\n   924:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   925:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n   926:     /// ```\n   927:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   928:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n   929:         self.0.set_ttl(ttl)\n   930:     }\n   931: \n   932:     /// Gets the value of the `IP_TTL` option for this socket.\n   933:     ///\n   934:     /// For more information about this option, see [`TcpListener::set_ttl`].\n   935:     ///\n   936:     /// # Examples\n   937:     ///\n   938:     /// ```no_run\n   939:     /// use std::net::TcpListener;\n   940:     ///\n   941:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   942:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n   943:     /// assert_eq!(listener.ttl().unwrap_or(0), 100);\n   944:     /// ```",
    "nanvix_source": "  1002:     ///\n  1003:     /// # Examples\n  1004:     ///\n  1005:     /// ```no_run\n  1006:     /// use std::net::TcpListener;\n  1007:     ///\n  1008:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n  1009:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n  1010:     /// ```\n  1011:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1012:     pub fn set_ttl(&self, ttl: u32) -> io::Result<()> {\n  1013:         self.0.set_ttl(ttl)\n  1014:     }\n  1015: \n  1016:     /// Gets the value of the `IP_TTL` option for this socket.\n  1017:     ///\n  1018:     /// For more information about this option, see [`TcpListener::set_ttl`].\n  1019:     ///\n  1020:     /// # Examples\n  1021:     ///\n  1022:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::take_error",
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
      "name": "take_error",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
                        "args": {
                          "angle_bracketed": {
                            "args": [
                              {
                                "type": {
                                  "resolved_path": {
                                    "args": null,
                                    "id": 2710,
                                    "path": "io::Error"
                                  }
                                }
                              }
                            ],
                            "constraints": []
                          }
                        },
                        "id": 56,
                        "path": "Option"
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
    "verification_source": "   963: \n   964:     /// Gets the value of the `SO_ERROR` option on this socket.\n   965:     ///\n   966:     /// This will retrieve the stored error in the underlying socket, clearing\n   967:     /// the field in the process. This can be useful for checking errors between\n   968:     /// calls.\n   969:     ///\n   970:     /// # Examples\n   971:     ///\n   972:     /// ```no_run\n   973:     /// use std::net::TcpListener;\n   974:     ///\n   975:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   976:     /// listener.take_error().expect(\"No error was expected\");\n   977:     /// ```\n   978:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   979:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   980:         self.0.take_error()\n   981:     }\n   982: \n   983:     /// Moves this TCP stream into or out of nonblocking mode.\n   984:     ///\n   985:     /// This will result in the `accept` operation becoming nonblocking,\n   986:     /// i.e., immediately returning from their calls. If the IO operation is\n   987:     /// successful, `Ok` is returned and no further action is required. If the\n   988:     /// IO operation could not be completed and needs to be retried, an error\n   989:     /// with kind [`io::ErrorKind::WouldBlock`] is returned.\n   990:     ///\n   991:     /// On Unix platforms, calling this method corresponds to calling `fcntl`\n   992:     /// `FIONBIO`. On Windows calling this method corresponds to calling\n   993:     /// `ioctlsocket` `FIONBIO`.\n   994:     ///\n   995:     /// # Examples",
    "nanvix_source": "  1053:     ///\n  1054:     /// # Examples\n  1055:     ///\n  1056:     /// ```no_run\n  1057:     /// use std::net::TcpListener;\n  1058:     ///\n  1059:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n  1060:     /// listener.take_error().expect(\"No error was expected\");\n  1061:     /// ```\n  1062:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1063:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n  1064:         self.0.take_error()\n  1065:     }\n  1066: \n  1067:     /// Moves this TCP stream into or out of nonblocking mode.\n  1068:     ///\n  1069:     /// This will result in the `accept` operation becoming nonblocking,\n  1070:     /// i.e., immediately returning from their calls. If the IO operation is\n  1071:     /// successful, `Ok` is returned and no further action is required. If the\n  1072:     /// IO operation could not be completed and needs to be retried, an error\n  1073:     /// with kind [`io::ErrorKind::WouldBlock`] is returned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::try_clone",
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
      "name": "try_clone",
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
            "id": 4722,
            "path": "TcpListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4810",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4722",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpListener"
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
                        "id": 4722,
                        "path": "TcpListener"
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
    "verification_source": "   802: \n   803:     /// Creates a new independently owned handle to the underlying socket.\n   804:     ///\n   805:     /// The returned [`TcpListener`] is a reference to the same socket that this\n   806:     /// object references. Both handles can be used to accept incoming\n   807:     /// connections and options set on one listener will affect the other.\n   808:     ///\n   809:     /// # Examples\n   810:     ///\n   811:     /// ```no_run\n   812:     /// use std::net::TcpListener;\n   813:     ///\n   814:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   815:     /// let listener_clone = listener.try_clone().unwrap();\n   816:     /// ```\n   817:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   818:     pub fn try_clone(&self) -> io::Result<TcpListener> {\n   819:         self.0.duplicate().map(TcpListener)\n   820:     }\n   821: \n   822:     /// Accept a new incoming connection from this listener.\n   823:     ///\n   824:     /// This function will block the calling thread until a new TCP connection\n   825:     /// is established. When established, the corresponding [`TcpStream`] and the\n   826:     /// remote peer's address will be returned.\n   827:     ///\n   828:     /// # Examples\n   829:     ///\n   830:     /// ```no_run\n   831:     /// use std::net::TcpListener;\n   832:     ///\n   833:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   834:     /// match listener.accept() {",
    "nanvix_source": "   859:     ///\n   860:     /// # Examples\n   861:     ///\n   862:     /// ```no_run\n   863:     /// use std::net::TcpListener;\n   864:     ///\n   865:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   866:     /// let listener_clone = listener.try_clone().unwrap();\n   867:     /// ```\n   868:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   869:     pub fn try_clone(&self) -> io::Result<TcpListener> {\n   870:         self.0.duplicate().map(TcpListener)\n   871:     }\n   872: \n   873:     /// Accept a new incoming connection from this listener.\n   874:     ///\n   875:     /// This function will block the calling thread until a new TCP connection\n   876:     /// is established. When established, the corresponding [`TcpStream`] and the\n   877:     /// remote peer's address will be returned.\n   878:     ///\n   879:     /// # Errors",
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
