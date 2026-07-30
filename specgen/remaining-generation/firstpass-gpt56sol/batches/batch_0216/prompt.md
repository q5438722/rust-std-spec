For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixDatagram::bind",
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
    "verification_source": "    83:     /// Creates a Unix datagram socket bound to the given path.\n    84:     ///\n    85:     /// # Examples\n    86:     ///\n    87:     /// ```no_run\n    88:     /// use std::os::unix::net::UnixDatagram;\n    89:     ///\n    90:     /// let sock = match UnixDatagram::bind(\"/path/to/the/socket\") {\n    91:     ///     Ok(sock) => sock,\n    92:     ///     Err(e) => {\n    93:     ///         println!(\"Couldn't bind: {e:?}\");\n    94:     ///         return\n    95:     ///     }\n    96:     /// };\n    97:     /// ```\n    98:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n    99:     pub fn bind<P: AsRef<Path>>(path: P) -> io::Result<UnixDatagram> {\n   100:         unsafe {\n   101:             let socket = UnixDatagram::unbound()?;\n   102:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   103: \n   104:             cvt(libc::bind(socket.as_raw_fd(), (&raw const addr) as *const _, len as _))?;\n   105: \n   106:             Ok(socket)\n   107:         }\n   108:     }\n   109: \n   110:     /// Creates a Unix datagram socket bound to an address.\n   111:     ///\n   112:     /// # Examples\n   113:     ///\n   114:     /// ```no_run\n   115:     /// use std::os::unix::net::{UnixDatagram};",
    "nanvix_source": "    86:     ///\n    87:     /// let sock = match UnixDatagram::bind(\"/path/to/the/socket\") {\n    88:     ///     Ok(sock) => sock,\n    89:     ///     Err(e) => {\n    90:     ///         println!(\"Couldn't bind: {e:?}\");\n    91:     ///         return\n    92:     ///     }\n    93:     /// };\n    94:     /// ```\n    95:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n    96:     pub fn bind<P: AsRef<Path>>(path: P) -> io::Result<UnixDatagram> {\n    97:         unsafe {\n    98:             let socket = UnixDatagram::unbound()?;\n    99:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   100: \n   101:             cvt(libc::bind(socket.as_raw_fd(), (&raw const addr) as *const _, len as _))?;\n   102: \n   103:             Ok(socket)\n   104:         }\n   105:     }\n   106: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::bind_addr",
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
    "verification_source": "   116:     ///\n   117:     /// fn main() -> std::io::Result<()> {\n   118:     ///     let sock1 = UnixDatagram::bind(\"path/to/socket\")?;\n   119:     ///     let addr = sock1.local_addr()?;\n   120:     ///\n   121:     ///     let sock2 = match UnixDatagram::bind_addr(&addr) {\n   122:     ///         Ok(sock) => sock,\n   123:     ///         Err(err) => {\n   124:     ///             println!(\"Couldn't bind: {err:?}\");\n   125:     ///             return Err(err);\n   126:     ///         }\n   127:     ///     };\n   128:     ///     Ok(())\n   129:     /// }\n   130:     /// ```\n   131:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   132:     pub fn bind_addr(socket_addr: &SocketAddr) -> io::Result<UnixDatagram> {\n   133:         unsafe {\n   134:             let socket = UnixDatagram::unbound()?;\n   135:             cvt(libc::bind(\n   136:                 socket.as_raw_fd(),\n   137:                 (&raw const socket_addr.addr) as *const _,\n   138:                 socket_addr.len as _,\n   139:             ))?;\n   140:             Ok(socket)\n   141:         }\n   142:     }\n   143: \n   144:     /// Creates a Unix Datagram socket which is not bound to any address.\n   145:     ///\n   146:     /// # Examples\n   147:     ///\n   148:     /// ```no_run",
    "nanvix_source": "   119:     ///         Ok(sock) => sock,\n   120:     ///         Err(err) => {\n   121:     ///             println!(\"Couldn't bind: {err:?}\");\n   122:     ///             return Err(err);\n   123:     ///         }\n   124:     ///     };\n   125:     ///     Ok(())\n   126:     /// }\n   127:     /// ```\n   128:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   129:     pub fn bind_addr(socket_addr: &SocketAddr) -> io::Result<UnixDatagram> {\n   130:         unsafe {\n   131:             let socket = UnixDatagram::unbound()?;\n   132:             cvt(libc::bind(\n   133:                 socket.as_raw_fd(),\n   134:                 (&raw const socket_addr.addr) as *const _,\n   135:                 socket_addr.len as _,\n   136:             ))?;\n   137:             Ok(socket)\n   138:         }\n   139:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::connect",
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
    "verification_source": "   199:     /// ```no_run\n   200:     /// use std::os::unix::net::UnixDatagram;\n   201:     ///\n   202:     /// fn main() -> std::io::Result<()> {\n   203:     ///     let sock = UnixDatagram::unbound()?;\n   204:     ///     match sock.connect(\"/path/to/the/socket\") {\n   205:     ///         Ok(sock) => sock,\n   206:     ///         Err(e) => {\n   207:     ///             println!(\"Couldn't connect: {e:?}\");\n   208:     ///             return Err(e)\n   209:     ///         }\n   210:     ///     };\n   211:     ///     Ok(())\n   212:     /// }\n   213:     /// ```\n   214:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   215:     pub fn connect<P: AsRef<Path>>(&self, path: P) -> io::Result<()> {\n   216:         unsafe {\n   217:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   218: \n   219:             cvt(libc::connect(self.as_raw_fd(), (&raw const addr) as *const _, len))?;\n   220:         }\n   221:         Ok(())\n   222:     }\n   223: \n   224:     /// Connects the socket to an address.\n   225:     ///\n   226:     /// # Examples\n   227:     ///\n   228:     /// ```no_run\n   229:     /// use std::os::unix::net::{UnixDatagram};\n   230:     ///\n   231:     /// fn main() -> std::io::Result<()> {",
    "nanvix_source": "   202:     ///         Ok(sock) => sock,\n   203:     ///         Err(e) => {\n   204:     ///             println!(\"Couldn't connect: {e:?}\");\n   205:     ///             return Err(e)\n   206:     ///         }\n   207:     ///     };\n   208:     ///     Ok(())\n   209:     /// }\n   210:     /// ```\n   211:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   212:     pub fn connect<P: AsRef<Path>>(&self, path: P) -> io::Result<()> {\n   213:         unsafe {\n   214:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   215: \n   216:             cvt(libc::connect(self.as_raw_fd(), (&raw const addr) as *const _, len))?;\n   217:         }\n   218:         Ok(())\n   219:     }\n   220: \n   221:     /// Connects the socket to an address.\n   222:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::connect_addr",
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
          ],
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
    "verification_source": "   231:     /// fn main() -> std::io::Result<()> {\n   232:     ///     let bound = UnixDatagram::bind(\"/path/to/socket\")?;\n   233:     ///     let addr = bound.local_addr()?;\n   234:     ///\n   235:     ///     let sock = UnixDatagram::unbound()?;\n   236:     ///     match sock.connect_addr(&addr) {\n   237:     ///         Ok(sock) => sock,\n   238:     ///         Err(e) => {\n   239:     ///             println!(\"Couldn't connect: {e:?}\");\n   240:     ///             return Err(e)\n   241:     ///         }\n   242:     ///     };\n   243:     ///     Ok(())\n   244:     /// }\n   245:     /// ```\n   246:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   247:     pub fn connect_addr(&self, socket_addr: &SocketAddr) -> io::Result<()> {\n   248:         unsafe {\n   249:             cvt(libc::connect(\n   250:                 self.as_raw_fd(),\n   251:                 (&raw const socket_addr.addr) as *const _,\n   252:                 socket_addr.len,\n   253:             ))?;\n   254:         }\n   255:         Ok(())\n   256:     }\n   257: \n   258:     /// Creates a new independently owned handle to the underlying socket.\n   259:     ///\n   260:     /// The returned `UnixDatagram` is a reference to the same socket that this\n   261:     /// object references. Both handles can be used to accept incoming\n   262:     /// connections and options set on one side will affect the other.\n   263:     ///",
    "nanvix_source": "   234:     ///         Ok(sock) => sock,\n   235:     ///         Err(e) => {\n   236:     ///             println!(\"Couldn't connect: {e:?}\");\n   237:     ///             return Err(e)\n   238:     ///         }\n   239:     ///     };\n   240:     ///     Ok(())\n   241:     /// }\n   242:     /// ```\n   243:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   244:     pub fn connect_addr(&self, socket_addr: &SocketAddr) -> io::Result<()> {\n   245:         unsafe {\n   246:             cvt(libc::connect(\n   247:                 self.as_raw_fd(),\n   248:                 (&raw const socket_addr.addr) as *const _,\n   249:                 socket_addr.len,\n   250:             ))?;\n   251:         }\n   252:         Ok(())\n   253:     }\n   254: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::local_addr",
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
    "verification_source": "   278:     }\n   279: \n   280:     /// Returns the address of this socket.\n   281:     ///\n   282:     /// # Examples\n   283:     ///\n   284:     /// ```no_run\n   285:     /// use std::os::unix::net::UnixDatagram;\n   286:     ///\n   287:     /// fn main() -> std::io::Result<()> {\n   288:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   289:     ///     let addr = sock.local_addr().expect(\"Couldn't get local address\");\n   290:     ///     Ok(())\n   291:     /// }\n   292:     /// ```\n   293:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   294:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   295:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   296:     }\n   297: \n   298:     /// Returns the address of this socket's peer.\n   299:     ///\n   300:     /// The [`connect`] method will connect the socket to a peer.\n   301:     ///\n   302:     /// [`connect`]: UnixDatagram::connect\n   303:     ///\n   304:     /// # Examples\n   305:     ///\n   306:     /// ```no_run\n   307:     /// use std::os::unix::net::UnixDatagram;\n   308:     ///\n   309:     /// fn main() -> std::io::Result<()> {\n   310:     ///     let sock = UnixDatagram::unbound()?;",
    "nanvix_source": "   281:     /// ```no_run\n   282:     /// use std::os::unix::net::UnixDatagram;\n   283:     ///\n   284:     /// fn main() -> std::io::Result<()> {\n   285:     ///     let sock = UnixDatagram::bind(\"/path/to/the/socket\")?;\n   286:     ///     let addr = sock.local_addr().expect(\"Couldn't get local address\");\n   287:     ///     Ok(())\n   288:     /// }\n   289:     /// ```\n   290:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   291:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   292:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   293:     }\n   294: \n   295:     /// Returns the address of this socket's peer.\n   296:     ///\n   297:     /// The [`connect`] method will connect the socket to a peer.\n   298:     ///\n   299:     /// [`connect`]: UnixDatagram::connect\n   300:     ///\n   301:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::pair",
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
                      "tuple": [
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 5380,
                            "path": "UnixDatagram"
                          }
                        },
                        {
                          "resolved_path": {
                            "args": null,
                            "id": 5380,
                            "path": "UnixDatagram"
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
    "verification_source": "   167:     /// Returns two `UnixDatagrams`s which are connected to each other.\n   168:     ///\n   169:     /// # Examples\n   170:     ///\n   171:     /// ```no_run\n   172:     /// use std::os::unix::net::UnixDatagram;\n   173:     ///\n   174:     /// let (sock1, sock2) = match UnixDatagram::pair() {\n   175:     ///     Ok((sock1, sock2)) => (sock1, sock2),\n   176:     ///     Err(e) => {\n   177:     ///         println!(\"Couldn't unbound: {e:?}\");\n   178:     ///         return\n   179:     ///     }\n   180:     /// };\n   181:     /// ```\n   182:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   183:     pub fn pair() -> io::Result<(UnixDatagram, UnixDatagram)> {\n   184:         let (i1, i2) = Socket::new_pair(libc::AF_UNIX, libc::SOCK_DGRAM)?;\n   185:         Ok((UnixDatagram(i1), UnixDatagram(i2)))\n   186:     }\n   187: \n   188:     /// Connects the socket to the specified path address.\n   189:     ///\n   190:     /// The [`send`] method may be used to send data to the specified address.\n   191:     /// [`recv`] and [`recv_from`] will only receive data from that address.\n   192:     ///\n   193:     /// [`send`]: UnixDatagram::send\n   194:     /// [`recv`]: UnixDatagram::recv\n   195:     /// [`recv_from`]: UnixDatagram::recv_from\n   196:     ///\n   197:     /// # Examples\n   198:     ///\n   199:     /// ```no_run",
    "nanvix_source": "   170:     ///\n   171:     /// let (sock1, sock2) = match UnixDatagram::pair() {\n   172:     ///     Ok((sock1, sock2)) => (sock1, sock2),\n   173:     ///     Err(e) => {\n   174:     ///         println!(\"Couldn't unbound: {e:?}\");\n   175:     ///         return\n   176:     ///     }\n   177:     /// };\n   178:     /// ```\n   179:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   180:     pub fn pair() -> io::Result<(UnixDatagram, UnixDatagram)> {\n   181:         let (i1, i2) = Socket::new_pair(libc::AF_UNIX, libc::SOCK_DGRAM)?;\n   182:         Ok((UnixDatagram(i1), UnixDatagram(i2)))\n   183:     }\n   184: \n   185:     /// Connects the socket to the specified path address.\n   186:     ///\n   187:     /// The [`send`] method may be used to send data to the specified address.\n   188:     /// [`recv`] and [`recv_from`] will only receive data from that address.\n   189:     ///\n   190:     /// [`send`]: UnixDatagram::send",
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
