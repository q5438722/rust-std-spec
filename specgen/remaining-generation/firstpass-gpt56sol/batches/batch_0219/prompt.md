For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixDatagram::try_clone",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                        "id": 5380,
                        "path": "UnixDatagram"
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
    "verification_source": "   260:     /// The returned `UnixDatagram` is a reference to the same socket that this\n   261:     /// object references. Both handles can be used to accept incoming\n   262:     /// connections and options set on one side will affect the other.\n   263:     ///\n   264:     /// # Examples\n   265:     ///\n   266:     /// ```no_run\n   267:     /// use std::os::unix::net::UnixDatagram;\n   268:     ///\n   269:     /// fn main() -> std::io::Result<()> {\n   270:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   271:     ///     let sock_copy = sock.try_clone().expect(\"try_clone failed\");\n   272:     ///     Ok(())\n   273:     /// }\n   274:     /// ```\n   275:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   276:     pub fn try_clone(&self) -> io::Result<UnixDatagram> {\n   277:         self.0.duplicate().map(UnixDatagram)\n   278:     }\n   279: \n   280:     /// Returns the address of this socket.\n   281:     ///\n   282:     /// # Examples\n   283:     ///\n   284:     /// ```no_run\n   285:     /// use std::os::unix::net::UnixDatagram;\n   286:     ///\n   287:     /// fn main() -> std::io::Result<()> {\n   288:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   289:     ///     let addr = sock.local_addr().expect(\"Couldn't get local address\");\n   290:     ///     Ok(())\n   291:     /// }\n   292:     /// ```",
    "nanvix_source": "   263:     /// ```no_run\n   264:     /// use std::os::unix::net::UnixDatagram;\n   265:     ///\n   266:     /// fn main() -> std::io::Result<()> {\n   267:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   268:     ///     let sock_copy = sock.try_clone().expect(\"try_clone failed\");\n   269:     ///     Ok(())\n   270:     /// }\n   271:     /// ```\n   272:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   273:     pub fn try_clone(&self) -> io::Result<UnixDatagram> {\n   274:         self.0.duplicate().map(UnixDatagram)\n   275:     }\n   276: \n   277:     /// Returns the address of this socket.\n   278:     ///\n   279:     /// # Examples\n   280:     ///\n   281:     /// ```no_run\n   282:     /// use std::os::unix::net::UnixDatagram;\n   283:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::unbound",
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
      "name": "unbound",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
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
                        "id": 5380,
                        "path": "UnixDatagram"
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
    "verification_source": "   144:     /// Creates a Unix Datagram socket which is not bound to any address.\n   145:     ///\n   146:     /// # Examples\n   147:     ///\n   148:     /// ```no_run\n   149:     /// use std::os::unix::net::UnixDatagram;\n   150:     ///\n   151:     /// let sock = match UnixDatagram::unbound() {\n   152:     ///     Ok(sock) => sock,\n   153:     ///     Err(e) => {\n   154:     ///         println!(\"Couldn't unbound: {e:?}\");\n   155:     ///         return\n   156:     ///     }\n   157:     /// };\n   158:     /// ```\n   159:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   160:     pub fn unbound() -> io::Result<UnixDatagram> {\n   161:         let inner = Socket::new(libc::AF_UNIX, libc::SOCK_DGRAM)?;\n   162:         Ok(UnixDatagram(inner))\n   163:     }\n   164: \n   165:     /// Creates an unnamed pair of connected sockets.\n   166:     ///\n   167:     /// Returns two `UnixDatagrams`s which are connected to each other.\n   168:     ///\n   169:     /// # Examples\n   170:     ///\n   171:     /// ```no_run\n   172:     /// use std::os::unix::net::UnixDatagram;\n   173:     ///\n   174:     /// let (sock1, sock2) = match UnixDatagram::pair() {\n   175:     ///     Ok((sock1, sock2)) => (sock1, sock2),\n   176:     ///     Err(e) => {",
    "nanvix_source": "   147:     ///\n   148:     /// let sock = match UnixDatagram::unbound() {\n   149:     ///     Ok(sock) => sock,\n   150:     ///     Err(e) => {\n   151:     ///         println!(\"Couldn't unbound: {e:?}\");\n   152:     ///         return\n   153:     ///     }\n   154:     /// };\n   155:     /// ```\n   156:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   157:     pub fn unbound() -> io::Result<UnixDatagram> {\n   158:         let inner = Socket::new(libc::AF_UNIX, libc::SOCK_DGRAM)?;\n   159:         Ok(UnixDatagram(inner))\n   160:     }\n   161: \n   162:     /// Creates an unnamed pair of connected sockets.\n   163:     ///\n   164:     /// Returns two `UnixDatagrams`s which are connected to each other.\n   165:     ///\n   166:     /// # Examples\n   167:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::write_timeout",
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
      "name": "write_timeout",
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
            "id": 5380,
            "path": "UnixDatagram"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5409",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5380",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "datagram",
          "UnixDatagram"
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
                                    "id": 513,
                                    "path": "Duration"
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
    "verification_source": "   801:     ///\n   802:     /// # Examples\n   803:     ///\n   804:     /// ```\n   805:     /// use std::os::unix::net::UnixDatagram;\n   806:     /// use std::time::Duration;\n   807:     ///\n   808:     /// fn main() -> std::io::Result<()> {\n   809:     ///     let sock = UnixDatagram::unbound()?;\n   810:     ///     sock.set_write_timeout(Some(Duration::new(1, 0)))\n   811:     ///         .expect(\"set_write_timeout function failed\");\n   812:     ///     assert_eq!(sock.write_timeout()?, Some(Duration::new(1, 0)));\n   813:     ///     Ok(())\n   814:     /// }\n   815:     /// ```\n   816:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   817:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   818:         self.0.timeout(libc::SO_SNDTIMEO)\n   819:     }\n   820: \n   821:     /// Moves the socket into or out of nonblocking mode.\n   822:     ///\n   823:     /// # Examples\n   824:     ///\n   825:     /// ```\n   826:     /// use std::os::unix::net::UnixDatagram;\n   827:     ///\n   828:     /// fn main() -> std::io::Result<()> {\n   829:     ///     let sock = UnixDatagram::unbound()?;\n   830:     ///     sock.set_nonblocking(true).expect(\"set_nonblocking function failed\");\n   831:     ///     Ok(())\n   832:     /// }\n   833:     /// ```",
    "nanvix_source": "   804:     ///\n   805:     /// fn main() -> std::io::Result<()> {\n   806:     ///     let sock = UnixDatagram::unbound()?;\n   807:     ///     sock.set_write_timeout(Some(Duration::new(1, 0)))\n   808:     ///         .expect(\"set_write_timeout function failed\");\n   809:     ///     assert_eq!(sock.write_timeout()?, Some(Duration::new(1, 0)));\n   810:     ///     Ok(())\n   811:     /// }\n   812:     /// ```\n   813:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   814:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   815:         self.0.timeout(libc::SO_SNDTIMEO)\n   816:     }\n   817: \n   818:     /// Moves the socket into or out of nonblocking mode.\n   819:     ///\n   820:     /// # Examples\n   821:     ///\n   822:     /// ```\n   823:     /// use std::os::unix::net::UnixDatagram;\n   824:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::accept",
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
            "id": 5444,
            "path": "UnixListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5454",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5444",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "listener",
          "UnixListener"
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
                            "id": 4284,
                            "path": "UnixStream"
                          }
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 5186,
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
    "verification_source": "   161:     /// # Examples\n   162:     ///\n   163:     /// ```no_run\n   164:     /// use std::os::unix::net::UnixListener;\n   165:     ///\n   166:     /// fn main() -> std::io::Result<()> {\n   167:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   168:     ///\n   169:     ///     match listener.accept() {\n   170:     ///         Ok((socket, addr)) => println!(\"Got a client: {addr:?}\"),\n   171:     ///         Err(e) => println!(\"accept function failed: {e:?}\"),\n   172:     ///     }\n   173:     ///     Ok(())\n   174:     /// }\n   175:     /// ```\n   176:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   177:     pub fn accept(&self) -> io::Result<(UnixStream, SocketAddr)> {\n   178:         let mut storage: libc::sockaddr_un = unsafe { mem::zeroed() };\n   179:         let mut len = size_of_val(&storage) as libc::socklen_t;\n   180:         let sock = self.0.accept((&raw mut storage) as *mut _, &mut len)?;\n   181:         let addr = SocketAddr::from_parts(storage, len)?;\n   182:         Ok((UnixStream(sock), addr))\n   183:     }\n   184: \n   185:     /// Creates a new independently owned handle to the underlying socket.\n   186:     ///\n   187:     /// The returned `UnixListener` is a reference to the same socket that this\n   188:     /// object references. Both handles can be used to accept incoming\n   189:     /// connections and options set on one listener will affect the other.\n   190:     ///\n   191:     /// # Examples\n   192:     ///\n   193:     /// ```no_run",
    "nanvix_source": "   167:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   168:     ///\n   169:     ///     match listener.accept() {\n   170:     ///         Ok((socket, addr)) => println!(\"Got a client: {addr:?}\"),\n   171:     ///         Err(e) => println!(\"accept function failed: {e:?}\"),\n   172:     ///     }\n   173:     ///     Ok(())\n   174:     /// }\n   175:     /// ```\n   176:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   177:     pub fn accept(&self) -> io::Result<(UnixStream, SocketAddr)> {\n   178:         let mut storage: libc::sockaddr_un = unsafe { mem::zeroed() };\n   179:         let mut len = size_of_val(&storage) as libc::socklen_t;\n   180:         let sock = self.0.accept((&raw mut storage) as *mut _, &mut len)?;\n   181:         let addr = SocketAddr::from_parts(storage, len)?;\n   182:         Ok((UnixStream(sock), addr))\n   183:     }\n   184: \n   185:     /// Creates a new independently owned handle to the underlying socket.\n   186:     ///\n   187:     /// The returned `UnixListener` is a reference to the same socket that this",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::bind",
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
            "id": 5444,
            "path": "UnixListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5454",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5444",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "listener",
          "UnixListener"
        ],
        "trait": null
      },
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
                        "id": 5444,
                        "path": "UnixListener"
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
    "verification_source": "    55:     /// Creates a new `UnixListener` bound to the specified socket.\n    56:     ///\n    57:     /// # Examples\n    58:     ///\n    59:     /// ```no_run\n    60:     /// use std::os::unix::net::UnixListener;\n    61:     ///\n    62:     /// let listener = match UnixListener::bind(\"/path/to/the/socket\") {\n    63:     ///     Ok(sock) => sock,\n    64:     ///     Err(e) => {\n    65:     ///         println!(\"Couldn't connect: {e:?}\");\n    66:     ///         return\n    67:     ///     }\n    68:     /// };\n    69:     /// ```\n    70:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n    71:     pub fn bind<P: AsRef<Path>>(path: P) -> io::Result<UnixListener> {\n    72:         unsafe {\n    73:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n    74:             let (addr, len) = sockaddr_un(path.as_ref())?;\n    75:             #[cfg(any(\n    76:                 target_os = \"windows\",\n    77:                 target_os = \"redox\",\n    78:                 target_os = \"espidf\",\n    79:                 target_os = \"horizon\"\n    80:             ))]\n    81:             const backlog: core::ffi::c_int = 128;\n    82:             #[cfg(any(\n    83:                 // Silently capped to `/proc/sys/net/core/somaxconn`.\n    84:                 target_os = \"linux\",\n    85:                 // Silently capped to `kern.ipc.soacceptqueue`.\n    86:                 target_os = \"freebsd\",\n    87:                 // Silently capped to `kern.somaxconn sysctl`.",
    "nanvix_source": "    61:     ///\n    62:     /// let listener = match UnixListener::bind(\"/path/to/the/socket\") {\n    63:     ///     Ok(sock) => sock,\n    64:     ///     Err(e) => {\n    65:     ///         println!(\"Couldn't connect: {e:?}\");\n    66:     ///         return\n    67:     ///     }\n    68:     /// };\n    69:     /// ```\n    70:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n    71:     pub fn bind<P: AsRef<Path>>(path: P) -> io::Result<UnixListener> {\n    72:         unsafe {\n    73:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n    74:             let (addr, len) = sockaddr_un(path.as_ref())?;\n    75:             #[cfg(any(\n    76:                 target_os = \"windows\",\n    77:                 target_os = \"redox\",\n    78:                 target_os = \"espidf\",\n    79:                 target_os = \"horizon\"\n    80:             ))]\n    81:             const backlog: core::ffi::c_int = 128;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::bind_addr",
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
      "name": "bind_addr",
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
            "id": 5444,
            "path": "UnixListener"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5454",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5444",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "listener",
          "UnixListener"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "socket_addr",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 5186,
                    "path": "SocketAddr"
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
                      "resolved_path": {
                        "args": null,
                        "id": 5444,
                        "path": "UnixListener"
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
    "verification_source": "   120:     ///\n   121:     /// fn main() -> std::io::Result<()> {\n   122:     ///     let listener1 = UnixListener::bind(\"path/to/socket\")?;\n   123:     ///     let addr = listener1.local_addr()?;\n   124:     ///\n   125:     ///     let listener2 = match UnixListener::bind_addr(&addr) {\n   126:     ///         Ok(sock) => sock,\n   127:     ///         Err(err) => {\n   128:     ///             println!(\"Couldn't bind: {err:?}\");\n   129:     ///             return Err(err);\n   130:     ///         }\n   131:     ///     };\n   132:     ///     Ok(())\n   133:     /// }\n   134:     /// ```\n   135:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   136:     pub fn bind_addr(socket_addr: &SocketAddr) -> io::Result<UnixListener> {\n   137:         unsafe {\n   138:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   139:             #[cfg(target_os = \"linux\")]\n   140:             const backlog: core::ffi::c_int = -1;\n   141:             #[cfg(not(target_os = \"linux\"))]\n   142:             const backlog: core::ffi::c_int = 128;\n   143:             cvt(libc::bind(\n   144:                 inner.as_raw_fd(),\n   145:                 (&raw const socket_addr.addr) as *const _,\n   146:                 socket_addr.len as _,\n   147:             ))?;\n   148:             cvt(libc::listen(inner.as_raw_fd(), backlog))?;\n   149:             Ok(UnixListener(inner))\n   150:         }\n   151:     }\n   152: ",
    "nanvix_source": "   126:     ///         Ok(sock) => sock,\n   127:     ///         Err(err) => {\n   128:     ///             println!(\"Couldn't bind: {err:?}\");\n   129:     ///             return Err(err);\n   130:     ///         }\n   131:     ///     };\n   132:     ///     Ok(())\n   133:     /// }\n   134:     /// ```\n   135:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   136:     pub fn bind_addr(socket_addr: &SocketAddr) -> io::Result<UnixListener> {\n   137:         unsafe {\n   138:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   139:             #[cfg(target_os = \"linux\")]\n   140:             const backlog: core::ffi::c_int = -1;\n   141:             #[cfg(not(target_os = \"linux\"))]\n   142:             const backlog: core::ffi::c_int = 128;\n   143:             cvt(libc::bind(\n   144:                 inner.as_raw_fd(),\n   145:                 (&raw const socket_addr.addr) as *const _,\n   146:                 socket_addr.len as _,",
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
