For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::TcpListener::ttl",
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
      "name": "ttl",
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
                      "primitive": "u32"
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
    "verification_source": "   930:     }\n   931: \n   932:     /// Gets the value of the `IP_TTL` option for this socket.\n   933:     ///\n   934:     /// For more information about this option, see [`TcpListener::set_ttl`].\n   935:     ///\n   936:     /// # Examples\n   937:     ///\n   938:     /// ```no_run\n   939:     /// use std::net::TcpListener;\n   940:     ///\n   941:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n   942:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n   943:     /// assert_eq!(listener.ttl().unwrap_or(0), 100);\n   944:     /// ```\n   945:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   946:     pub fn ttl(&self) -> io::Result<u32> {\n   947:         self.0.ttl()\n   948:     }\n   949: \n   950:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   951:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   952:     #[allow(missing_docs)]\n   953:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n   954:         self.0.set_only_v6(only_v6)\n   955:     }\n   956: \n   957:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   958:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n   959:     #[allow(missing_docs)]\n   960:     pub fn only_v6(&self) -> io::Result<bool> {\n   961:         self.0.only_v6()\n   962:     }",
    "nanvix_source": "  1020:     /// # Examples\n  1021:     ///\n  1022:     /// ```no_run\n  1023:     /// use std::net::TcpListener;\n  1024:     ///\n  1025:     /// let listener = TcpListener::bind(\"127.0.0.1:80\").unwrap();\n  1026:     /// listener.set_ttl(100).expect(\"could not set TTL\");\n  1027:     /// assert_eq!(listener.ttl().unwrap_or(0), 100);\n  1028:     /// ```\n  1029:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1030:     pub fn ttl(&self) -> io::Result<u32> {\n  1031:         self.0.ttl()\n  1032:     }\n  1033: \n  1034:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n  1035:     #[deprecated(since = \"1.16.0\", note = \"this option can only be set before the socket is bound\")]\n  1036:     #[allow(missing_docs)]\n  1037:     pub fn set_only_v6(&self, only_v6: bool) -> io::Result<()> {\n  1038:         self.0.set_only_v6(only_v6)\n  1039:     }\n  1040: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::connect",
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
                        "args": null,
                        "id": 1888,
                        "path": "ToSocketAddrs"
                      }
                    }
                  }
                ],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "A"
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
      "name": "connect",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "generic": "A"
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
                        "id": 3224,
                        "path": "TcpStream"
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
    "verification_source": "   152:     /// a TCP connection to `127.0.0.1:8081`:\n   153:     ///\n   154:     /// ```no_run\n   155:     /// use std::net::{SocketAddr, TcpStream};\n   156:     ///\n   157:     /// let addrs = [\n   158:     ///     SocketAddr::from(([127, 0, 0, 1], 8080)),\n   159:     ///     SocketAddr::from(([127, 0, 0, 1], 8081)),\n   160:     /// ];\n   161:     /// if let Ok(stream) = TcpStream::connect(&addrs[..]) {\n   162:     ///     println!(\"Connected to the server!\");\n   163:     /// } else {\n   164:     ///     println!(\"Couldn't connect to server...\");\n   165:     /// }\n   166:     /// ```\n   167:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   168:     pub fn connect<A: ToSocketAddrs>(addr: A) -> io::Result<TcpStream> {\n   169:         net_imp::TcpStream::connect(addr).map(TcpStream)\n   170:     }\n   171: \n   172:     /// Opens a TCP connection to a remote host with a timeout.\n   173:     ///\n   174:     /// Unlike `connect`, `connect_timeout` takes a single [`SocketAddr`] since\n   175:     /// timeout must be applied to individual addresses.\n   176:     ///\n   177:     /// It is an error to pass a zero `Duration` to this function.\n   178:     ///\n   179:     /// Unlike other methods on `TcpStream`, this does not correspond to a\n   180:     /// single system call. It instead calls `connect` in nonblocking mode and\n   181:     /// then uses an OS-specific mechanism to await the completion of the\n   182:     /// connection request.\n   183:     #[stable(feature = \"tcpstream_connect_timeout\", since = \"1.21.0\")]\n   184:     pub fn connect_timeout(addr: &SocketAddr, timeout: Duration) -> io::Result<TcpStream> {",
    "nanvix_source": "   158:     ///     SocketAddr::from(([127, 0, 0, 1], 8080)),\n   159:     ///     SocketAddr::from(([127, 0, 0, 1], 8081)),\n   160:     /// ];\n   161:     /// if let Ok(stream) = TcpStream::connect(&addrs[..]) {\n   162:     ///     println!(\"Connected to the server!\");\n   163:     /// } else {\n   164:     ///     println!(\"Couldn't connect to server...\");\n   165:     /// }\n   166:     /// ```\n   167:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   168:     pub fn connect<A: ToSocketAddrs>(addr: A) -> io::Result<TcpStream> {\n   169:         net_imp::TcpStream::connect(addr).map(TcpStream)\n   170:     }\n   171: \n   172:     /// Opens a TCP connection to a remote host with a timeout.\n   173:     ///\n   174:     /// Unlike `connect`, `connect_timeout` takes a single [`SocketAddr`] since\n   175:     /// timeout must be applied to individual addresses.\n   176:     ///\n   177:     /// It is an error to pass a zero `Duration` to this function.\n   178:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::connect_timeout",
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
      "name": "connect_timeout",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 4670,
                    "path": "SocketAddr"
                  }
                }
              }
            }
          ],
          [
            "timeout",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
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
                        "id": 3224,
                        "path": "TcpStream"
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
    "verification_source": "   168:     pub fn connect<A: ToSocketAddrs>(addr: A) -> io::Result<TcpStream> {\n   169:         net_imp::TcpStream::connect(addr).map(TcpStream)\n   170:     }\n   171: \n   172:     /// Opens a TCP connection to a remote host with a timeout.\n   173:     ///\n   174:     /// Unlike `connect`, `connect_timeout` takes a single [`SocketAddr`] since\n   175:     /// timeout must be applied to individual addresses.\n   176:     ///\n   177:     /// It is an error to pass a zero `Duration` to this function.\n   178:     ///\n   179:     /// Unlike other methods on `TcpStream`, this does not correspond to a\n   180:     /// single system call. It instead calls `connect` in nonblocking mode and\n   181:     /// then uses an OS-specific mechanism to await the completion of the\n   182:     /// connection request.\n   183:     #[stable(feature = \"tcpstream_connect_timeout\", since = \"1.21.0\")]\n   184:     pub fn connect_timeout(addr: &SocketAddr, timeout: Duration) -> io::Result<TcpStream> {\n   185:         net_imp::TcpStream::connect_timeout(addr, timeout).map(TcpStream)\n   186:     }\n   187: \n   188:     /// Returns the socket address of the remote peer of this TCP connection.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```no_run\n   193:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpStream};\n   194:     ///\n   195:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   196:     ///                        .expect(\"Couldn't connect to the server...\");\n   197:     /// assert_eq!(stream.peer_addr().unwrap(),\n   198:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   199:     /// ```\n   200:     #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   174:     /// Unlike `connect`, `connect_timeout` takes a single [`SocketAddr`] since\n   175:     /// timeout must be applied to individual addresses.\n   176:     ///\n   177:     /// It is an error to pass a zero `Duration` to this function.\n   178:     ///\n   179:     /// Unlike other methods on `TcpStream`, this does not correspond to a\n   180:     /// single system call. It instead calls `connect` in nonblocking mode and\n   181:     /// then uses an OS-specific mechanism to await the completion of the\n   182:     /// connection request.\n   183:     #[stable(feature = \"tcpstream_connect_timeout\", since = \"1.21.0\")]\n   184:     pub fn connect_timeout(addr: &SocketAddr, timeout: Duration) -> io::Result<TcpStream> {\n   185:         net_imp::TcpStream::connect_timeout(addr, timeout).map(TcpStream)\n   186:     }\n   187: \n   188:     /// Returns the socket address of the remote peer of this TCP connection.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```no_run\n   193:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpStream};\n   194:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::local_addr",
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
      "name": "local_addr",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
                        "id": 4670,
                        "path": "SocketAddr"
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
    "verification_source": "   202:         self.0.peer_addr()\n   203:     }\n   204: \n   205:     /// Returns the socket address of the local half of this TCP connection.\n   206:     ///\n   207:     /// # Examples\n   208:     ///\n   209:     /// ```no_run\n   210:     /// use std::net::{IpAddr, Ipv4Addr, TcpStream};\n   211:     ///\n   212:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   213:     ///                        .expect(\"Couldn't connect to the server...\");\n   214:     /// assert_eq!(stream.local_addr().unwrap().ip(),\n   215:     ///            IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   216:     /// ```\n   217:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   218:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   219:         self.0.socket_addr()\n   220:     }\n   221: \n   222:     /// Shuts down the read, write, or both halves of this connection.\n   223:     ///\n   224:     /// This function will cause all pending and future I/O on the specified\n   225:     /// portions to return immediately with an appropriate value (see the\n   226:     /// documentation of [`Shutdown`]).\n   227:     ///\n   228:     /// # Platform-specific behavior\n   229:     ///\n   230:     /// Calling this function multiple times may result in different behavior,\n   231:     /// depending on the operating system. On Linux, the second call will\n   232:     /// return `Ok(())`, but on macOS, it will return `ErrorKind::NotConnected`.\n   233:     /// This may change in the future.\n   234:     ///",
    "nanvix_source": "   208:     ///\n   209:     /// ```no_run\n   210:     /// use std::net::{IpAddr, Ipv4Addr, TcpStream};\n   211:     ///\n   212:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   213:     ///                        .expect(\"Couldn't connect to the server...\");\n   214:     /// assert_eq!(stream.local_addr().unwrap().ip(),\n   215:     ///            IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   216:     /// ```\n   217:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   218:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   219:         self.0.socket_addr()\n   220:     }\n   221: \n   222:     /// Shuts down the read, write, or both halves of this connection.\n   223:     ///\n   224:     /// This function will cause all pending and future I/O on the specified\n   225:     /// portions to return immediately with an appropriate value (see the\n   226:     /// documentation of [`Shutdown`]).\n   227:     ///\n   228:     /// # Platform-specific behavior",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::nodelay",
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
      "name": "nodelay",
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
    "verification_source": "   498: \n   499:     /// Gets the value of the `TCP_NODELAY` option on this socket.\n   500:     ///\n   501:     /// For more information about this option, see [`TcpStream::set_nodelay`].\n   502:     ///\n   503:     /// # Examples\n   504:     ///\n   505:     /// ```no_run\n   506:     /// use std::net::TcpStream;\n   507:     ///\n   508:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   509:     ///                        .expect(\"Couldn't connect to the server...\");\n   510:     /// stream.set_nodelay(true).expect(\"set_nodelay call failed\");\n   511:     /// assert_eq!(stream.nodelay().unwrap_or(false), true);\n   512:     /// ```\n   513:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   514:     pub fn nodelay(&self) -> io::Result<bool> {\n   515:         self.0.nodelay()\n   516:     }\n   517: \n   518:     /// Sets the value for the `IP_TTL` option on this socket.\n   519:     ///\n   520:     /// This value sets the time-to-live field that is used in every packet sent\n   521:     /// from this socket.\n   522:     ///\n   523:     /// # Examples\n   524:     ///\n   525:     /// ```no_run\n   526:     /// use std::net::TcpStream;\n   527:     ///\n   528:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   529:     ///                        .expect(\"Couldn't connect to the server...\");\n   530:     /// stream.set_ttl(100).expect(\"set_ttl call failed\");",
    "nanvix_source": "   555:     ///\n   556:     /// ```no_run\n   557:     /// use std::net::TcpStream;\n   558:     ///\n   559:     /// let stream = TcpStream::connect(\"127.0.0.1:8080\")\n   560:     ///                        .expect(\"Couldn't connect to the server...\");\n   561:     /// stream.set_nodelay(true).expect(\"set_nodelay call failed\");\n   562:     /// assert_eq!(stream.nodelay().unwrap_or(false), true);\n   563:     /// ```\n   564:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   565:     pub fn nodelay(&self) -> io::Result<bool> {\n   566:         self.0.nodelay()\n   567:     }\n   568: \n   569:     /// Sets the value for the `IP_TTL` option on this socket.\n   570:     ///\n   571:     /// This value sets the time-to-live field that is used in every packet sent\n   572:     /// from this socket.\n   573:     ///\n   574:     /// # Examples\n   575:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpStream::peek",
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
      "name": "peek",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "buf"
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
            "id": 3224,
            "path": "TcpStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4742",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:3224",
        "resolved_owner_path": [
          "std",
          "net",
          "tcp",
          "TcpStream"
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
            "buf",
            {
              "borrowed_ref": {
                "is_mutable": true,
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
                      "primitive": "usize"
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
    "verification_source": "   410:     /// returns the number of bytes peeked.\n   411:     ///\n   412:     /// Successive calls return the same data. This is accomplished by passing\n   413:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   414:     ///\n   415:     /// # Examples\n   416:     ///\n   417:     /// ```no_run\n   418:     /// use std::net::TcpStream;\n   419:     ///\n   420:     /// let stream = TcpStream::connect(\"127.0.0.1:8000\")\n   421:     ///                        .expect(\"Couldn't connect to the server...\");\n   422:     /// let mut buf = [0; 10];\n   423:     /// let len = stream.peek(&mut buf).expect(\"peek failed\");\n   424:     /// ```\n   425:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   426:     pub fn peek(&self, buf: &mut [u8]) -> io::Result<usize> {\n   427:         self.0.peek(buf)\n   428:     }\n   429: \n   430:     /// Sets the value of the `SO_LINGER` option on this socket.\n   431:     ///\n   432:     /// This value controls how the socket is closed when data remains\n   433:     /// to be sent. If `SO_LINGER` is set, the socket will remain open\n   434:     /// for the specified duration as the system attempts to send pending data.\n   435:     /// Otherwise, the system may close the socket immediately, or wait for a\n   436:     /// default timeout.\n   437:     ///\n   438:     /// # Examples\n   439:     ///\n   440:     /// ```no_run\n   441:     /// #![feature(tcp_linger)]\n   442:     ///",
    "nanvix_source": "   416:     ///\n   417:     /// ```no_run\n   418:     /// use std::net::TcpStream;\n   419:     ///\n   420:     /// let stream = TcpStream::connect(\"127.0.0.1:8000\")\n   421:     ///                        .expect(\"Couldn't connect to the server...\");\n   422:     /// let mut buf = [0; 10];\n   423:     /// let len = stream.peek(&mut buf).expect(\"peek failed\");\n   424:     /// ```\n   425:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   426:     pub fn peek(&self, buf: &mut [u8]) -> io::Result<usize> {\n   427:         self.0.peek(buf)\n   428:     }\n   429: \n   430:     /// Sets the value of the `SO_LINGER` option on this socket.\n   431:     ///\n   432:     /// This value controls how the socket is closed when data remains\n   433:     /// to be sent. If `SO_LINGER` is set, the socket will remain open\n   434:     /// for the specified duration as the system attempts to send pending data.\n   435:     /// Otherwise, the system may close the socket immediately, or wait for a\n   436:     /// default timeout.",
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
