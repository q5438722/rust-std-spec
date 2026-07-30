For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixStream::connect_addr",
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
      "name": "connect_addr",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                        "id": 4284,
                        "path": "UnixStream"
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
    "verification_source": "   130:     ///\n   131:     /// fn main() -> std::io::Result<()> {\n   132:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   133:     ///     let addr = listener.local_addr()?;\n   134:     ///\n   135:     ///     let sock = match UnixStream::connect_addr(&addr) {\n   136:     ///         Ok(sock) => sock,\n   137:     ///         Err(e) => {\n   138:     ///             println!(\"Couldn't connect: {e:?}\");\n   139:     ///             return Err(e)\n   140:     ///         }\n   141:     ///     };\n   142:     ///     Ok(())\n   143:     /// }\n   144:     /// ````\n   145:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   146:     pub fn connect_addr(socket_addr: &SocketAddr) -> io::Result<UnixStream> {\n   147:         unsafe {\n   148:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   149:             cvt(libc::connect(\n   150:                 inner.as_raw_fd(),\n   151:                 (&raw const socket_addr.addr) as *const _,\n   152:                 socket_addr.len,\n   153:             ))?;\n   154:             Ok(UnixStream(inner))\n   155:         }\n   156:     }\n   157: \n   158:     /// Creates an unnamed pair of connected sockets.\n   159:     ///\n   160:     /// Returns two `UnixStream`s which are connected to each other.\n   161:     ///\n   162:     /// # Examples",
    "nanvix_source": "   132:     ///         Ok(sock) => sock,\n   133:     ///         Err(e) => {\n   134:     ///             println!(\"Couldn't connect: {e:?}\");\n   135:     ///             return Err(e)\n   136:     ///         }\n   137:     ///     };\n   138:     ///     Ok(())\n   139:     /// }\n   140:     /// ````\n   141:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   142:     pub fn connect_addr(socket_addr: &SocketAddr) -> io::Result<UnixStream> {\n   143:         unsafe {\n   144:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   145:             cvt(libc::connect(\n   146:                 inner.as_raw_fd(),\n   147:                 (&raw const socket_addr.addr) as *const _,\n   148:                 socket_addr.len,\n   149:             ))?;\n   150:             Ok(UnixStream(inner))\n   151:         }\n   152:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::local_addr",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                        "id": 5186,
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
    "verification_source": "   202:     }\n   203: \n   204:     /// Returns the socket address of the local half of this connection.\n   205:     ///\n   206:     /// # Examples\n   207:     ///\n   208:     /// ```no_run\n   209:     /// use std::os::unix::net::UnixStream;\n   210:     ///\n   211:     /// fn main() -> std::io::Result<()> {\n   212:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   213:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   214:     ///     Ok(())\n   215:     /// }\n   216:     /// ```\n   217:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   218:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   219:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   220:     }\n   221: \n   222:     /// Returns the socket address of the remote half of this connection.\n   223:     ///\n   224:     /// # Examples\n   225:     ///\n   226:     /// ```no_run\n   227:     /// use std::os::unix::net::UnixStream;\n   228:     ///\n   229:     /// fn main() -> std::io::Result<()> {\n   230:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   231:     ///     let addr = socket.peer_addr().expect(\"Couldn't get peer address\");\n   232:     ///     Ok(())\n   233:     /// }\n   234:     /// ```",
    "nanvix_source": "   204:     /// ```no_run\n   205:     /// use std::os::unix::net::UnixStream;\n   206:     ///\n   207:     /// fn main() -> std::io::Result<()> {\n   208:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   209:     ///     let addr = socket.local_addr().expect(\"Couldn't get local address\");\n   210:     ///     Ok(())\n   211:     /// }\n   212:     /// ```\n   213:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   214:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   215:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   216:     }\n   217: \n   218:     /// Returns the socket address of the remote half of this connection.\n   219:     ///\n   220:     /// # Examples\n   221:     ///\n   222:     /// ```no_run\n   223:     /// use std::os::unix::net::UnixStream;\n   224:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::pair",
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
      "name": "pair",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                            "id": 4284,
                            "path": "UnixStream"
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
    "verification_source": "   160:     /// Returns two `UnixStream`s which are connected to each other.\n   161:     ///\n   162:     /// # Examples\n   163:     ///\n   164:     /// ```no_run\n   165:     /// use std::os::unix::net::UnixStream;\n   166:     ///\n   167:     /// let (sock1, sock2) = match UnixStream::pair() {\n   168:     ///     Ok((sock1, sock2)) => (sock1, sock2),\n   169:     ///     Err(e) => {\n   170:     ///         println!(\"Couldn't create a pair of sockets: {e:?}\");\n   171:     ///         return\n   172:     ///     }\n   173:     /// };\n   174:     /// ```\n   175:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   176:     pub fn pair() -> io::Result<(UnixStream, UnixStream)> {\n   177:         let (i1, i2) = Socket::new_pair(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   178:         Ok((UnixStream(i1), UnixStream(i2)))\n   179:     }\n   180: \n   181:     /// Creates a new independently owned handle to the underlying socket.\n   182:     ///\n   183:     /// The returned `UnixStream` is a reference to the same stream that this\n   184:     /// object references. Both handles will read and write the same stream of\n   185:     /// data, and options set on one stream will be propagated to the other\n   186:     /// stream.\n   187:     ///\n   188:     /// # Examples\n   189:     ///\n   190:     /// ```no_run\n   191:     /// use std::os::unix::net::UnixStream;\n   192:     ///",
    "nanvix_source": "   162:     ///\n   163:     /// let (sock1, sock2) = match UnixStream::pair() {\n   164:     ///     Ok((sock1, sock2)) => (sock1, sock2),\n   165:     ///     Err(e) => {\n   166:     ///         println!(\"Couldn't create a pair of sockets: {e:?}\");\n   167:     ///         return\n   168:     ///     }\n   169:     /// };\n   170:     /// ```\n   171:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   172:     pub fn pair() -> io::Result<(UnixStream, UnixStream)> {\n   173:         let (i1, i2) = Socket::new_pair(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   174:         Ok((UnixStream(i1), UnixStream(i2)))\n   175:     }\n   176: \n   177:     /// Creates a new independently owned handle to the underlying socket.\n   178:     ///\n   179:     /// The returned `UnixStream` is a reference to the same stream that this\n   180:     /// object references. Both handles will read and write the same stream of\n   181:     /// data, and options set on one stream will be propagated to the other\n   182:     /// stream.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::peer_addr",
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
      "name": "peer_addr",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
                        "id": 5186,
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
    "verification_source": "   220:     }\n   221: \n   222:     /// Returns the socket address of the remote half of this connection.\n   223:     ///\n   224:     /// # Examples\n   225:     ///\n   226:     /// ```no_run\n   227:     /// use std::os::unix::net::UnixStream;\n   228:     ///\n   229:     /// fn main() -> std::io::Result<()> {\n   230:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   231:     ///     let addr = socket.peer_addr().expect(\"Couldn't get peer address\");\n   232:     ///     Ok(())\n   233:     /// }\n   234:     /// ```\n   235:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   236:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   237:         SocketAddr::new(|addr, len| unsafe { libc::getpeername(self.as_raw_fd(), addr, len) })\n   238:     }\n   239: \n   240:     /// Gets the peer credentials for this Unix domain socket.\n   241:     ///\n   242:     /// # Examples\n   243:     ///\n   244:     /// ```no_run\n   245:     /// #![feature(peer_credentials_unix_socket)]\n   246:     /// use std::os::unix::net::UnixStream;\n   247:     ///\n   248:     /// fn main() -> std::io::Result<()> {\n   249:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   250:     ///     let peer_cred = socket.peer_cred().expect(\"Couldn't get peer credentials\");\n   251:     ///     Ok(())\n   252:     /// }",
    "nanvix_source": "   222:     /// ```no_run\n   223:     /// use std::os::unix::net::UnixStream;\n   224:     ///\n   225:     /// fn main() -> std::io::Result<()> {\n   226:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   227:     ///     let addr = socket.peer_addr().expect(\"Couldn't get peer address\");\n   228:     ///     Ok(())\n   229:     /// }\n   230:     /// ```\n   231:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   232:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   233:         SocketAddr::new(|addr, len| unsafe { libc::getpeername(self.as_raw_fd(), addr, len) })\n   234:     }\n   235: \n   236:     /// Gets the peer credentials for this Unix domain socket.\n   237:     ///\n   238:     /// # Examples\n   239:     ///\n   240:     /// ```no_run\n   241:     /// #![feature(peer_credentials_unix_socket)]\n   242:     /// use std::os::unix::net::UnixStream;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::read_timeout",
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
      "name": "read_timeout",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
    "verification_source": "   355:     /// Returns the read timeout of this socket.\n   356:     ///\n   357:     /// # Examples\n   358:     ///\n   359:     /// ```no_run\n   360:     /// use std::os::unix::net::UnixStream;\n   361:     /// use std::time::Duration;\n   362:     ///\n   363:     /// fn main() -> std::io::Result<()> {\n   364:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   365:     ///     socket.set_read_timeout(Some(Duration::new(1, 0))).expect(\"Couldn't set read timeout\");\n   366:     ///     assert_eq!(socket.read_timeout()?, Some(Duration::new(1, 0)));\n   367:     ///     Ok(())\n   368:     /// }\n   369:     /// ```\n   370:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   371:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   372:         self.0.timeout(libc::SO_RCVTIMEO)\n   373:     }\n   374: \n   375:     /// Returns the write timeout of this socket.\n   376:     ///\n   377:     /// # Examples\n   378:     ///\n   379:     /// ```no_run\n   380:     /// use std::os::unix::net::UnixStream;\n   381:     /// use std::time::Duration;\n   382:     ///\n   383:     /// fn main() -> std::io::Result<()> {\n   384:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   385:     ///     socket.set_write_timeout(Some(Duration::new(1, 0)))\n   386:     ///         .expect(\"Couldn't set write timeout\");\n   387:     ///     assert_eq!(socket.write_timeout()?, Some(Duration::new(1, 0)));",
    "nanvix_source": "   358:     /// use std::time::Duration;\n   359:     ///\n   360:     /// fn main() -> std::io::Result<()> {\n   361:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   362:     ///     socket.set_read_timeout(Some(Duration::new(1, 0))).expect(\"Couldn't set read timeout\");\n   363:     ///     assert_eq!(socket.read_timeout()?, Some(Duration::new(1, 0)));\n   364:     ///     Ok(())\n   365:     /// }\n   366:     /// ```\n   367:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   368:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   369:         self.0.timeout(libc::SO_RCVTIMEO)\n   370:     }\n   371: \n   372:     /// Returns the write timeout of this socket.\n   373:     ///\n   374:     /// # Examples\n   375:     ///\n   376:     /// ```no_run\n   377:     /// use std::os::unix::net::UnixStream;\n   378:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::set_nonblocking",
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
            "id": 4284,
            "path": "UnixStream"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5530",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4284",
        "resolved_owner_path": [
          "std",
          "os",
          "unix",
          "net",
          "stream",
          "UnixStream"
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
    "verification_source": "   394:     }\n   395: \n   396:     /// Moves the socket into or out of nonblocking mode.\n   397:     ///\n   398:     /// # Examples\n   399:     ///\n   400:     /// ```no_run\n   401:     /// use std::os::unix::net::UnixStream;\n   402:     ///\n   403:     /// fn main() -> std::io::Result<()> {\n   404:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   405:     ///     socket.set_nonblocking(true).expect(\"Couldn't set nonblocking\");\n   406:     ///     Ok(())\n   407:     /// }\n   408:     /// ```\n   409:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   410:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   411:         self.0.set_nonblocking(nonblocking)\n   412:     }\n   413: \n   414:     /// Set the id of the socket for network filtering purpose\n   415:     ///\n   416:     #[cfg_attr(\n   417:         any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\"),\n   418:         doc = \"```no_run\"\n   419:     )]\n   420:     #[cfg_attr(\n   421:         not(any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\")),\n   422:         doc = \"```ignore\"\n   423:     )]\n   424:     /// #![feature(unix_set_mark)]\n   425:     /// use std::os::unix::net::UnixStream;\n   426:     ///",
    "nanvix_source": "   397:     /// ```no_run\n   398:     /// use std::os::unix::net::UnixStream;\n   399:     ///\n   400:     /// fn main() -> std::io::Result<()> {\n   401:     ///     let socket = UnixStream::connect(\"/tmp/sock\")?;\n   402:     ///     socket.set_nonblocking(true).expect(\"Couldn't set nonblocking\");\n   403:     ///     Ok(())\n   404:     /// }\n   405:     /// ```\n   406:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   407:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   408:         self.0.set_nonblocking(nonblocking)\n   409:     }\n   410: \n   411:     /// Set the id of the socket for network filtering purpose\n   412:     ///\n   413:     #[cfg_attr(\n   414:         any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\"),\n   415:         doc = \"```no_run\"\n   416:     )]\n   417:     #[cfg_attr(",
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
