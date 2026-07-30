For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::io::stdin",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
      "name": "stdin",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 3739,
            "path": "Stdin"
          }
        }
      }
    },
    "verification_source": "   324: /// Using explicit synchronization:\n   325: ///\n   326: /// ```no_run\n   327: /// use std::io::{self, BufRead};\n   328: ///\n   329: /// fn main() -> io::Result<()> {\n   330: ///     let mut buffer = String::new();\n   331: ///     let stdin = io::stdin();\n   332: ///     let mut handle = stdin.lock();\n   333: ///\n   334: ///     handle.read_line(&mut buffer)?;\n   335: ///     Ok(())\n   336: /// }\n   337: /// ```\n   338: #[must_use]\n   339: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   340: pub fn stdin() -> Stdin {\n   341:     static INSTANCE: OnceLock<Mutex<BufReader<StdinRaw>>> = OnceLock::new();\n   342:     Stdin {\n   343:         inner: INSTANCE.get_or_init(|| {\n   344:             Mutex::new(BufReader::with_capacity(stdio::STDIN_BUF_SIZE, stdin_raw()))\n   345:         }),\n   346:     }\n   347: }\n   348: \n   349: impl Stdin {\n   350:     /// Locks this handle to the standard input stream, returning a readable\n   351:     /// guard.\n   352:     ///\n   353:     /// The lock is released when the returned lock goes out of scope. The\n   354:     /// returned guard also implements the [`Read`] and [`BufRead`] traits for\n   355:     /// accessing the underlying data.\n   356:     ///",
    "nanvix_source": "   331: ///     let mut buffer = String::new();\n   332: ///     let stdin = io::stdin();\n   333: ///     let mut handle = stdin.lock();\n   334: ///\n   335: ///     handle.read_line(&mut buffer)?;\n   336: ///     Ok(())\n   337: /// }\n   338: /// ```\n   339: #[must_use]\n   340: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   341: pub fn stdin() -> Stdin {\n   342:     static INSTANCE: OnceLock<Mutex<BufReader<StdinRaw>>> = OnceLock::new();\n   343:     Stdin {\n   344:         inner: INSTANCE.get_or_init(|| {\n   345:             Mutex::new(BufReader::with_capacity(stdio::STDIN_BUF_SIZE, stdin_raw()))\n   346:         }),\n   347:     }\n   348: }\n   349: \n   350: impl Stdin {\n   351:     /// Locks this handle to the standard input stream, returning a readable",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::io::stdout",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "free_function"
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
      "name": "stdout",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 3846,
            "path": "Stdout"
          }
        }
      }
    },
    "verification_source": "   700: /// ```no_run\n   701: /// use std::io::{self, Write};\n   702: ///\n   703: /// fn main() -> io::Result<()> {\n   704: ///     let mut stdout = io::stdout();\n   705: ///     stdout.write_all(b\"hello, \")?;\n   706: ///     stdout.flush()?;                // Manual flush\n   707: ///     stdout.write_all(b\"world!\\n\")?; // Automatically flushed\n   708: ///     Ok(())\n   709: /// }\n   710: /// ```\n   711: ///\n   712: /// [`flush`]: Write::flush\n   713: #[must_use]\n   714: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   715: #[cfg_attr(not(test), rustc_diagnostic_item = \"io_stdout\")]\n   716: pub fn stdout() -> Stdout {\n   717:     Stdout {\n   718:         inner: STDOUT\n   719:             .get_or_init(|| ReentrantLock::new(RefCell::new(LineWriter::new(stdout_raw())))),\n   720:     }\n   721: }\n   722: \n   723: // Flush the data and disable buffering during shutdown\n   724: // by replacing the line writer by one with zero\n   725: // buffering capacity.\n   726: pub fn cleanup() {\n   727:     let mut initialized = false;\n   728:     let stdout = STDOUT.get_or_init(|| {\n   729:         initialized = true;\n   730:         ReentrantLock::new(RefCell::new(LineWriter::with_capacity(0, stdout_raw())))\n   731:     });\n   732: ",
    "nanvix_source": "   707: ///     stdout.flush()?;                // Manual flush\n   708: ///     stdout.write_all(b\"world!\\n\")?; // Automatically flushed\n   709: ///     Ok(())\n   710: /// }\n   711: /// ```\n   712: ///\n   713: /// [`flush`]: Write::flush\n   714: #[must_use]\n   715: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   716: #[cfg_attr(not(test), rustc_diagnostic_item = \"io_stdout\")]\n   717: pub fn stdout() -> Stdout {\n   718:     Stdout {\n   719:         inner: STDOUT\n   720:             .get_or_init(|| ReentrantLock::new(RefCell::new(LineWriter::new(stdout_raw())))),\n   721:     }\n   722: }\n   723: \n   724: // Flush the data and disable buffering during shutdown\n   725: // by replacing the line writer by one with zero\n   726: // buffering capacity.\n   727: pub fn cleanup() {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::accept",
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
      "name": "accept",
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
                      "tuple": [
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 3224,
                            "path": "TcpStream"
                          }
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 4670,
                            "path": "SocketAddr"
                          }
                        }
                      ]
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
    "verification_source": "   824:     /// This function will block the calling thread until a new TCP connection\n   825:     /// is established. When established, the corresponding [`TcpStream`] and the\n   826:     /// remote peer's address will be returned.\n   827:     ///\n   828:     /// # Examples\n   829:     ///\n   830:     /// ```no_run\n   831:     /// use std::net::TcpListener;\n   832:     ///\n   833:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   834:     /// match listener.accept() {\n   835:     ///     Ok((_socket, addr)) => println!(\"new client: {addr:?}\"),\n   836:     ///     Err(e) => println!(\"couldn't get client: {e:?}\"),\n   837:     /// }\n   838:     /// ```\n   839:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   840:     pub fn accept(&self) -> io::Result<(TcpStream, SocketAddr)> {\n   841:         // On WASM, `TcpStream` is uninhabited (as it's unsupported) and so\n   842:         // the `a` variable here is technically unused.\n   843:         #[cfg_attr(target_arch = \"wasm32\", allow(unused_variables))]\n   844:         self.0.accept().map(|(a, b)| (TcpStream(a), b))\n   845:     }\n   846: \n   847:     /// Returns an iterator over the connections being received on this\n   848:     /// listener.\n   849:     ///\n   850:     /// The returned iterator will never return [`None`] and will also not yield\n   851:     /// the peer's [`SocketAddr`] structure. Iterating over it is equivalent to\n   852:     /// calling [`TcpListener::accept`] in a loop.\n   853:     ///\n   854:     /// # Examples\n   855:     ///\n   856:     /// ```no_run",
    "nanvix_source": "   904:     /// ```no_run\n   905:     /// use std::net::TcpListener;\n   906:     ///\n   907:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   908:     /// match listener.accept() {\n   909:     ///     Ok((_socket, addr)) => println!(\"new client: {addr:?}\"),\n   910:     ///     Err(e) => println!(\"couldn't get client: {e:?}\"),\n   911:     /// }\n   912:     /// ```\n   913:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   914:     pub fn accept(&self) -> io::Result<(TcpStream, SocketAddr)> {\n   915:         // On WASM, `TcpStream` is uninhabited (as it's unsupported) and so\n   916:         // the `a` variable here is technically unused.\n   917:         #[cfg_attr(target_arch = \"wasm32\", allow(unused_variables))]\n   918:         self.0.accept().map(|(a, b)| (TcpStream(a), b))\n   919:     }\n   920: \n   921:     /// Returns an iterator over the connections being received on this\n   922:     /// listener.\n   923:     ///\n   924:     /// The returned iterator will never return [`None`] and will also not yield",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::bind",
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
      "name": "bind",
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
    "verification_source": "   767:     /// let addrs = [\n   768:     ///     SocketAddr::from(([127, 0, 0, 1], 80)),\n   769:     ///     SocketAddr::from(([127, 0, 0, 1], 443)),\n   770:     /// ];\n   771:     /// let listener = TcpListener::bind(&addrs[..]).unwrap();\n   772:     /// ```\n   773:     ///\n   774:     /// Creates a TCP listener bound to a port assigned by the operating system\n   775:     /// at `127.0.0.1`.\n   776:     ///\n   777:     /// ```no_run\n   778:     /// use std::net::TcpListener;\n   779:     ///\n   780:     /// let socket = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n   781:     /// ```\n   782:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   783:     pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<TcpListener> {\n   784:         net_imp::TcpListener::bind(addr).map(TcpListener)\n   785:     }\n   786: \n   787:     /// Returns the local socket address of this listener.\n   788:     ///\n   789:     /// # Examples\n   790:     ///\n   791:     /// ```no_run\n   792:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener};\n   793:     ///\n   794:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   795:     /// assert_eq!(listener.local_addr().unwrap(),\n   796:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   797:     /// ```\n   798:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   799:     pub fn local_addr(&self) -> io::Result<SocketAddr> {",
    "nanvix_source": "   824:     ///\n   825:     /// Creates a TCP listener bound to a port assigned by the operating system\n   826:     /// at `127.0.0.1`.\n   827:     ///\n   828:     /// ```no_run\n   829:     /// use std::net::TcpListener;\n   830:     ///\n   831:     /// let socket = TcpListener::bind(\"127.0.0.1:0\").unwrap();\n   832:     /// ```\n   833:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   834:     pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<TcpListener> {\n   835:         net_imp::TcpListener::bind(addr).map(TcpListener)\n   836:     }\n   837: \n   838:     /// Returns the local socket address of this listener.\n   839:     ///\n   840:     /// # Examples\n   841:     ///\n   842:     /// ```no_run\n   843:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener};\n   844:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::incoming",
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
      "name": "incoming",
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
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 4798,
            "path": "Incoming"
          }
        }
      }
    },
    "verification_source": "   862:     ///\n   863:     /// fn main() -> std::io::Result<()> {\n   864:     ///     let listener = TcpListener::bind(\"127.0.0.1:80\")?;\n   865:     ///\n   866:     ///     for stream in listener.incoming() {\n   867:     ///         match stream {\n   868:     ///             Ok(stream) => {\n   869:     ///                 handle_connection(stream);\n   870:     ///             }\n   871:     ///             Err(e) => { /* connection failed */ }\n   872:     ///         }\n   873:     ///     }\n   874:     ///     Ok(())\n   875:     /// }\n   876:     /// ```\n   877:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   878:     pub fn incoming(&self) -> Incoming<'_> {\n   879:         Incoming { listener: self }\n   880:     }\n   881: \n   882:     /// Turn this into an iterator over the connections being received on this\n   883:     /// listener.\n   884:     ///\n   885:     /// The returned iterator will never return [`None`] and will also not yield\n   886:     /// the peer's [`SocketAddr`] structure. Iterating over it is equivalent to\n   887:     /// calling [`TcpListener::accept`] in a loop.\n   888:     ///\n   889:     /// # Examples\n   890:     ///\n   891:     /// ```no_run\n   892:     /// #![feature(tcplistener_into_incoming)]\n   893:     /// use std::net::{TcpListener, TcpStream};\n   894:     ///",
    "nanvix_source": "   947:     ///             Ok(stream) => {\n   948:     ///                 handle_connection(stream);\n   949:     ///             }\n   950:     ///             Err(e) => { /* connection failed */ }\n   951:     ///         }\n   952:     ///     }\n   953:     ///     Ok(())\n   954:     /// }\n   955:     /// ```\n   956:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   957:     pub fn incoming(&self) -> Incoming<'_> {\n   958:         Incoming { listener: self }\n   959:     }\n   960: \n   961:     /// Turn this into an iterator over the connections being received on this\n   962:     /// listener.\n   963:     ///\n   964:     /// The returned iterator will never return [`None`] and will also not yield\n   965:     /// the peer's [`SocketAddr`] structure. Iterating over it is equivalent to\n   966:     /// calling [`TcpListener::accept`] in a loop.\n   967:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::TcpListener::local_addr",
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
    "verification_source": "   783:     pub fn bind<A: ToSocketAddrs>(addr: A) -> io::Result<TcpListener> {\n   784:         net_imp::TcpListener::bind(addr).map(TcpListener)\n   785:     }\n   786: \n   787:     /// Returns the local socket address of this listener.\n   788:     ///\n   789:     /// # Examples\n   790:     ///\n   791:     /// ```no_run\n   792:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener};\n   793:     ///\n   794:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   795:     /// assert_eq!(listener.local_addr().unwrap(),\n   796:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   797:     /// ```\n   798:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   799:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   800:         self.0.socket_addr()\n   801:     }\n   802: \n   803:     /// Creates a new independently owned handle to the underlying socket.\n   804:     ///\n   805:     /// The returned [`TcpListener`] is a reference to the same socket that this\n   806:     /// object references. Both handles can be used to accept incoming\n   807:     /// connections and options set on one listener will affect the other.\n   808:     ///\n   809:     /// # Examples\n   810:     ///\n   811:     /// ```no_run\n   812:     /// use std::net::TcpListener;\n   813:     ///\n   814:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   815:     /// let listener_clone = listener.try_clone().unwrap();",
    "nanvix_source": "   840:     /// # Examples\n   841:     ///\n   842:     /// ```no_run\n   843:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, TcpListener};\n   844:     ///\n   845:     /// let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n   846:     /// assert_eq!(listener.local_addr().unwrap(),\n   847:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080)));\n   848:     /// ```\n   849:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   850:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   851:         self.0.socket_addr()\n   852:     }\n   853: \n   854:     /// Creates a new independently owned handle to the underlying socket.\n   855:     ///\n   856:     /// The returned [`TcpListener`] is a reference to the same socket that this\n   857:     /// object references. Both handles can be used to accept incoming\n   858:     /// connections and options set on one listener will affect the other.\n   859:     ///\n   860:     /// # Examples",
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
