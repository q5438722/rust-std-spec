For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixListener::incoming",
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
                    "lifetime": "'_"
                  }
                ],
                "constraints": []
              }
            },
            "id": 5453,
            "path": "Incoming"
          }
        }
      }
    },
    "verification_source": "   289:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   290:     ///\n   291:     ///     for stream in listener.incoming() {\n   292:     ///         match stream {\n   293:     ///             Ok(stream) => {\n   294:     ///                 thread::spawn(|| handle_client(stream));\n   295:     ///             }\n   296:     ///             Err(err) => {\n   297:     ///                 break;\n   298:     ///             }\n   299:     ///         }\n   300:     ///     }\n   301:     ///     Ok(())\n   302:     /// }\n   303:     /// ```\n   304:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   305:     pub fn incoming(&self) -> Incoming<'_> {\n   306:         Incoming { listener: self }\n   307:     }\n   308: }\n   309: \n   310: #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   311: impl AsRawFd for UnixListener {\n   312:     #[inline]\n   313:     fn as_raw_fd(&self) -> RawFd {\n   314:         self.0.as_inner().as_raw_fd()\n   315:     }\n   316: }\n   317: \n   318: #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   319: impl FromRawFd for UnixListener {\n   320:     #[inline]\n   321:     unsafe fn from_raw_fd(fd: RawFd) -> UnixListener {",
    "nanvix_source": "   295:     ///             }\n   296:     ///             Err(err) => {\n   297:     ///                 break;\n   298:     ///             }\n   299:     ///         }\n   300:     ///     }\n   301:     ///     Ok(())\n   302:     /// }\n   303:     /// ```\n   304:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   305:     pub fn incoming(&self) -> Incoming<'_> {\n   306:         Incoming { listener: self }\n   307:     }\n   308: }\n   309: \n   310: #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   311: impl AsRawFd for UnixListener {\n   312:     #[inline]\n   313:     fn as_raw_fd(&self) -> RawFd {\n   314:         self.0.as_inner().as_raw_fd()\n   315:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::local_addr",
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
    "verification_source": "   205:     }\n   206: \n   207:     /// Returns the local socket address of this listener.\n   208:     ///\n   209:     /// # Examples\n   210:     ///\n   211:     /// ```no_run\n   212:     /// use std::os::unix::net::UnixListener;\n   213:     ///\n   214:     /// fn main() -> std::io::Result<()> {\n   215:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   216:     ///     let addr = listener.local_addr().expect(\"Couldn't get local address\");\n   217:     ///     Ok(())\n   218:     /// }\n   219:     /// ```\n   220:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   221:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   222:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   223:     }\n   224: \n   225:     /// Moves the socket into or out of nonblocking mode.\n   226:     ///\n   227:     /// This will result in the `accept` operation becoming nonblocking,\n   228:     /// i.e., immediately returning from their calls. If the IO operation is\n   229:     /// successful, `Ok` is returned and no further action is required. If the\n   230:     /// IO operation could not be completed and needs to be retried, an error\n   231:     /// with kind [`io::ErrorKind::WouldBlock`] is returned.\n   232:     ///\n   233:     /// # Examples\n   234:     ///\n   235:     /// ```no_run\n   236:     /// use std::os::unix::net::UnixListener;\n   237:     ///",
    "nanvix_source": "   211:     /// ```no_run\n   212:     /// use std::os::unix::net::UnixListener;\n   213:     ///\n   214:     /// fn main() -> std::io::Result<()> {\n   215:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   216:     ///     let addr = listener.local_addr().expect(\"Couldn't get local address\");\n   217:     ///     Ok(())\n   218:     /// }\n   219:     /// ```\n   220:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   221:     pub fn local_addr(&self) -> io::Result<SocketAddr> {\n   222:         SocketAddr::new(|addr, len| unsafe { libc::getsockname(self.as_raw_fd(), addr, len) })\n   223:     }\n   224: \n   225:     /// Moves the socket into or out of nonblocking mode.\n   226:     ///\n   227:     /// This will result in the `accept` operation becoming nonblocking,\n   228:     /// i.e., immediately returning from their calls. If the IO operation is\n   229:     /// successful, `Ok` is returned and no further action is required. If the\n   230:     /// IO operation could not be completed and needs to be retried, an error\n   231:     /// with kind [`io::ErrorKind::WouldBlock`] is returned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::set_nonblocking",
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
    "verification_source": "   229:     /// successful, `Ok` is returned and no further action is required. If the\n   230:     /// IO operation could not be completed and needs to be retried, an error\n   231:     /// with kind [`io::ErrorKind::WouldBlock`] is returned.\n   232:     ///\n   233:     /// # Examples\n   234:     ///\n   235:     /// ```no_run\n   236:     /// use std::os::unix::net::UnixListener;\n   237:     ///\n   238:     /// fn main() -> std::io::Result<()> {\n   239:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   240:     ///     listener.set_nonblocking(true).expect(\"Couldn't set non blocking\");\n   241:     ///     Ok(())\n   242:     /// }\n   243:     /// ```\n   244:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   245:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   246:         self.0.set_nonblocking(nonblocking)\n   247:     }\n   248: \n   249:     /// Returns the value of the `SO_ERROR` option.\n   250:     ///\n   251:     /// # Examples\n   252:     ///\n   253:     /// ```no_run\n   254:     /// use std::os::unix::net::UnixListener;\n   255:     ///\n   256:     /// fn main() -> std::io::Result<()> {\n   257:     ///     let listener = UnixListener::bind(\"/tmp/sock\")?;\n   258:     ///\n   259:     ///     if let Ok(Some(err)) = listener.take_error() {\n   260:     ///         println!(\"Got error: {err:?}\");\n   261:     ///     }",
    "nanvix_source": "   235:     /// ```no_run\n   236:     /// use std::os::unix::net::UnixListener;\n   237:     ///\n   238:     /// fn main() -> std::io::Result<()> {\n   239:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   240:     ///     listener.set_nonblocking(true).expect(\"Couldn't set non blocking\");\n   241:     ///     Ok(())\n   242:     /// }\n   243:     /// ```\n   244:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   245:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   246:         self.0.set_nonblocking(nonblocking)\n   247:     }\n   248: \n   249:     /// Returns the value of the `SO_ERROR` option.\n   250:     ///\n   251:     /// # Examples\n   252:     ///\n   253:     /// ```no_run\n   254:     /// use std::os::unix::net::UnixListener;\n   255:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::take_error",
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
    "verification_source": "   253:     /// ```no_run\n   254:     /// use std::os::unix::net::UnixListener;\n   255:     ///\n   256:     /// fn main() -> std::io::Result<()> {\n   257:     ///     let listener = UnixListener::bind(\"/tmp/sock\")?;\n   258:     ///\n   259:     ///     if let Ok(Some(err)) = listener.take_error() {\n   260:     ///         println!(\"Got error: {err:?}\");\n   261:     ///     }\n   262:     ///     Ok(())\n   263:     /// }\n   264:     /// ```\n   265:     ///\n   266:     /// # Platform specific\n   267:     /// On Redox this always returns `None`.\n   268:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   269:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   270:         self.0.take_error()\n   271:     }\n   272: \n   273:     /// Returns an iterator over incoming connections.\n   274:     ///\n   275:     /// The iterator will never return [`None`] and will also not yield the\n   276:     /// peer's [`SocketAddr`] structure.\n   277:     ///\n   278:     /// # Examples\n   279:     ///\n   280:     /// ```no_run\n   281:     /// use std::thread;\n   282:     /// use std::os::unix::net::{UnixStream, UnixListener};\n   283:     ///\n   284:     /// fn handle_client(stream: UnixStream) {\n   285:     ///     // ...",
    "nanvix_source": "   259:     ///     if let Ok(Some(err)) = listener.take_error() {\n   260:     ///         println!(\"Got error: {err:?}\");\n   261:     ///     }\n   262:     ///     Ok(())\n   263:     /// }\n   264:     /// ```\n   265:     ///\n   266:     /// # Platform specific\n   267:     /// On Redox this always returns `None`.\n   268:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   269:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   270:         self.0.take_error()\n   271:     }\n   272: \n   273:     /// Returns an iterator over incoming connections.\n   274:     ///\n   275:     /// The iterator will never return [`None`] and will also not yield the\n   276:     /// peer's [`SocketAddr`] structure.\n   277:     ///\n   278:     /// # Examples\n   279:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixListener::try_clone",
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
    "verification_source": "   187:     /// The returned `UnixListener` is a reference to the same socket that this\n   188:     /// object references. Both handles can be used to accept incoming\n   189:     /// connections and options set on one listener will affect the other.\n   190:     ///\n   191:     /// # Examples\n   192:     ///\n   193:     /// ```no_run\n   194:     /// use std::os::unix::net::UnixListener;\n   195:     ///\n   196:     /// fn main() -> std::io::Result<()> {\n   197:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   198:     ///     let listener_copy = listener.try_clone().expect(\"try_clone failed\");\n   199:     ///     Ok(())\n   200:     /// }\n   201:     /// ```\n   202:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   203:     pub fn try_clone(&self) -> io::Result<UnixListener> {\n   204:         self.0.duplicate().map(UnixListener)\n   205:     }\n   206: \n   207:     /// Returns the local socket address of this listener.\n   208:     ///\n   209:     /// # Examples\n   210:     ///\n   211:     /// ```no_run\n   212:     /// use std::os::unix::net::UnixListener;\n   213:     ///\n   214:     /// fn main() -> std::io::Result<()> {\n   215:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   216:     ///     let addr = listener.local_addr().expect(\"Couldn't get local address\");\n   217:     ///     Ok(())\n   218:     /// }\n   219:     /// ```",
    "nanvix_source": "   193:     /// ```no_run\n   194:     /// use std::os::unix::net::UnixListener;\n   195:     ///\n   196:     /// fn main() -> std::io::Result<()> {\n   197:     ///     let listener = UnixListener::bind(\"/path/to/the/socket\")?;\n   198:     ///     let listener_copy = listener.try_clone().expect(\"try_clone failed\");\n   199:     ///     Ok(())\n   200:     /// }\n   201:     /// ```\n   202:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   203:     pub fn try_clone(&self) -> io::Result<UnixListener> {\n   204:         self.0.duplicate().map(UnixListener)\n   205:     }\n   206: \n   207:     /// Returns the local socket address of this listener.\n   208:     ///\n   209:     /// # Examples\n   210:     ///\n   211:     /// ```no_run\n   212:     /// use std::os::unix::net::UnixListener;\n   213:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixStream::connect",
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
    "verification_source": "    96:     /// Connects to the socket named by `path`.\n    97:     ///\n    98:     /// # Examples\n    99:     ///\n   100:     /// ```no_run\n   101:     /// use std::os::unix::net::UnixStream;\n   102:     ///\n   103:     /// let socket = match UnixStream::connect(\"/tmp/sock\") {\n   104:     ///     Ok(sock) => sock,\n   105:     ///     Err(e) => {\n   106:     ///         println!(\"Couldn't connect: {e:?}\");\n   107:     ///         return\n   108:     ///     }\n   109:     /// };\n   110:     /// ```\n   111:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   112:     pub fn connect<P: AsRef<Path>>(path: P) -> io::Result<UnixStream> {\n   113:         unsafe {\n   114:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   115:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   116: \n   117:             cvt(libc::connect(inner.as_raw_fd(), (&raw const addr) as *const _, len))?;\n   118:             Ok(UnixStream(inner))\n   119:         }\n   120:     }\n   121: \n   122:     /// Connects to the socket specified by [`address`].\n   123:     ///\n   124:     /// [`address`]: crate::os::unix::net::SocketAddr\n   125:     ///\n   126:     /// # Examples\n   127:     ///\n   128:     /// ```no_run",
    "nanvix_source": "    98:     ///\n    99:     /// let socket = match UnixStream::connect(\"/tmp/sock\") {\n   100:     ///     Ok(sock) => sock,\n   101:     ///     Err(e) => {\n   102:     ///         println!(\"Couldn't connect: {e:?}\");\n   103:     ///         return\n   104:     ///     }\n   105:     /// };\n   106:     /// ```\n   107:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   108:     pub fn connect<P: AsRef<Path>>(path: P) -> io::Result<UnixStream> {\n   109:         unsafe {\n   110:             let inner = Socket::new(libc::AF_UNIX, libc::SOCK_STREAM)?;\n   111:             let (addr, len) = sockaddr_un(path.as_ref())?;\n   112: \n   113:             cvt(libc::connect(inner.as_raw_fd(), (&raw const addr) as *const _, len))?;\n   114:             Ok(UnixStream(inner))\n   115:         }\n   116:     }\n   117: \n   118:     /// Connects to the socket specified by [`address`].",
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
