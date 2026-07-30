For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::peek_from",
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
      "name": "peek_from",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
                      "tuple": [
                        {
                          "primitive": "usize"
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
    "verification_source": "   161:     ///\n   162:     /// Do not use this function to implement busy waiting, instead use `libc::poll` to\n   163:     /// synchronize IO events on one or more sockets.\n   164:     ///\n   165:     /// # Examples\n   166:     ///\n   167:     /// ```no_run\n   168:     /// use std::net::UdpSocket;\n   169:     ///\n   170:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   171:     /// let mut buf = [0; 10];\n   172:     /// let (number_of_bytes, src_addr) = socket.peek_from(&mut buf)\n   173:     ///                                         .expect(\"Didn't receive data\");\n   174:     /// let filled_buf = &mut buf[..number_of_bytes];\n   175:     /// ```\n   176:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   177:     pub fn peek_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   178:         self.0.peek_from(buf)\n   179:     }\n   180: \n   181:     /// Sends data on the socket to the given address. On success, returns the\n   182:     /// number of bytes written. Note that the operating system may refuse\n   183:     /// buffers larger than 65507. However, partial writes are not possible\n   184:     /// until buffer sizes above `i32::MAX`.\n   185:     ///\n   186:     /// Address type can be any implementor of [`ToSocketAddrs`] trait. See its\n   187:     /// documentation for concrete examples.\n   188:     ///\n   189:     /// It is possible for `addr` to yield multiple addresses, but `send_to`\n   190:     /// will only send data to the first address yielded by `addr`.\n   191:     ///\n   192:     /// This will return an error when the IP version of the local socket\n   193:     /// does not match that returned from [`ToSocketAddrs`].",
    "nanvix_source": "   167:     /// ```no_run\n   168:     /// use std::net::UdpSocket;\n   169:     ///\n   170:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   171:     /// let mut buf = [0; 10];\n   172:     /// let (number_of_bytes, src_addr) = socket.peek_from(&mut buf)\n   173:     ///                                         .expect(\"Didn't receive data\");\n   174:     /// let filled_buf = &mut buf[..number_of_bytes];\n   175:     /// ```\n   176:     #[stable(feature = \"peek\", since = \"1.18.0\")]\n   177:     pub fn peek_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   178:         self.0.peek_from(buf)\n   179:     }\n   180: \n   181:     /// Sends data on the socket to the given address. On success, returns the\n   182:     /// number of bytes written. Note that the operating system may refuse\n   183:     /// buffers larger than 65507. However, partial writes are not possible\n   184:     /// until buffer sizes above `i32::MAX`.\n   185:     ///\n   186:     /// Address type can be any implementor of [`ToSocketAddrs`] trait. See its\n   187:     /// documentation for concrete examples.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::peer_addr",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   224:     /// assert_eq!(socket.peer_addr().unwrap(),\n   225:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(192, 168, 0, 1), 41203)));\n   226:     /// ```\n   227:     ///\n   228:     /// If the socket isn't connected, it will return a [`NotConnected`] error.\n   229:     ///\n   230:     /// [`NotConnected`]: io::ErrorKind::NotConnected\n   231:     ///\n   232:     /// ```no_run\n   233:     /// use std::net::UdpSocket;\n   234:     ///\n   235:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   236:     /// assert_eq!(socket.peer_addr().unwrap_err().kind(),\n   237:     ///            std::io::ErrorKind::NotConnected);\n   238:     /// ```\n   239:     #[stable(feature = \"udp_peer_addr\", since = \"1.40.0\")]\n   240:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   241:         self.0.peer_addr()\n   242:     }\n   243: \n   244:     /// Returns the socket address that this socket was created from.\n   245:     ///\n   246:     /// # Examples\n   247:     ///\n   248:     /// ```no_run\n   249:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};\n   250:     ///\n   251:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   252:     /// assert_eq!(socket.local_addr().unwrap(),\n   253:     ///            SocketAddr::V4(SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 34254)));\n   254:     /// ```\n   255:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   256:     pub fn local_addr(&self) -> io::Result<SocketAddr> {",
    "nanvix_source": "   230:     /// [`NotConnected`]: io::ErrorKind::NotConnected\n   231:     ///\n   232:     /// ```no_run\n   233:     /// use std::net::UdpSocket;\n   234:     ///\n   235:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   236:     /// assert_eq!(socket.peer_addr().unwrap_err().kind(),\n   237:     ///            std::io::ErrorKind::NotConnected);\n   238:     /// ```\n   239:     #[stable(feature = \"udp_peer_addr\", since = \"1.40.0\")]\n   240:     pub fn peer_addr(&self) -> io::Result<SocketAddr> {\n   241:         self.0.peer_addr()\n   242:     }\n   243: \n   244:     /// Returns the socket address that this socket was created from.\n   245:     ///\n   246:     /// # Examples\n   247:     ///\n   248:     /// ```no_run\n   249:     /// use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4, UdpSocket};\n   250:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::read_timeout",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   365:     /// Returns the read timeout of this socket.\n   366:     ///\n   367:     /// If the timeout is [`None`], then [`read`] calls will block indefinitely.\n   368:     ///\n   369:     /// [`read`]: io::Read::read\n   370:     ///\n   371:     /// # Examples\n   372:     ///\n   373:     /// ```no_run\n   374:     /// use std::net::UdpSocket;\n   375:     ///\n   376:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   377:     /// socket.set_read_timeout(None).expect(\"set_read_timeout call failed\");\n   378:     /// assert_eq!(socket.read_timeout().unwrap(), None);\n   379:     /// ```\n   380:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   381:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   382:         self.0.read_timeout()\n   383:     }\n   384: \n   385:     /// Returns the write timeout of this socket.\n   386:     ///\n   387:     /// If the timeout is [`None`], then [`write`] calls will block indefinitely.\n   388:     ///\n   389:     /// [`write`]: io::Write::write\n   390:     ///\n   391:     /// # Examples\n   392:     ///\n   393:     /// ```no_run\n   394:     /// use std::net::UdpSocket;\n   395:     ///\n   396:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   397:     /// socket.set_write_timeout(None).expect(\"set_write_timeout call failed\");",
    "nanvix_source": "   371:     /// # Examples\n   372:     ///\n   373:     /// ```no_run\n   374:     /// use std::net::UdpSocket;\n   375:     ///\n   376:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   377:     /// socket.set_read_timeout(None).expect(\"set_read_timeout call failed\");\n   378:     /// assert_eq!(socket.read_timeout().unwrap(), None);\n   379:     /// ```\n   380:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   381:     pub fn read_timeout(&self) -> io::Result<Option<Duration>> {\n   382:         self.0.read_timeout()\n   383:     }\n   384: \n   385:     /// Returns the write timeout of this socket.\n   386:     ///\n   387:     /// If the timeout is [`None`], then [`write`] calls will block indefinitely.\n   388:     ///\n   389:     /// [`write`]: io::Write::write\n   390:     ///\n   391:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::recv",
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
      "name": "recv",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   720:     /// system call does so.\n   721:     ///\n   722:     /// # Examples\n   723:     ///\n   724:     /// ```no_run\n   725:     /// use std::net::UdpSocket;\n   726:     ///\n   727:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   728:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   729:     /// let mut buf = [0; 10];\n   730:     /// match socket.recv(&mut buf) {\n   731:     ///     Ok(received) => println!(\"received {received} bytes {:?}\", &buf[..received]),\n   732:     ///     Err(e) => println!(\"recv function failed: {e:?}\"),\n   733:     /// }\n   734:     /// ```\n   735:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   736:     pub fn recv(&self, buf: &mut [u8]) -> io::Result<usize> {\n   737:         self.0.recv(buf)\n   738:     }\n   739: \n   740:     /// Receives single datagram on the socket from the remote address to which it is\n   741:     /// connected, without removing the message from input queue. On success, returns\n   742:     /// the number of bytes peeked.\n   743:     ///\n   744:     /// The function must be called with valid byte array `buf` of sufficient size to\n   745:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   746:     /// excess bytes may be discarded.\n   747:     ///\n   748:     /// Successive calls return the same data. This is accomplished by passing\n   749:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   750:     ///\n   751:     /// Do not use this function to implement busy waiting, instead use `libc::poll` to\n   752:     /// synchronize IO events on one or more sockets.",
    "nanvix_source": "   726:     ///\n   727:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   728:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   729:     /// let mut buf = [0; 10];\n   730:     /// match socket.recv(&mut buf) {\n   731:     ///     Ok(received) => println!(\"received {received} bytes {:?}\", &buf[..received]),\n   732:     ///     Err(e) => println!(\"recv function failed: {e:?}\"),\n   733:     /// }\n   734:     /// ```\n   735:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   736:     pub fn recv(&self, buf: &mut [u8]) -> io::Result<usize> {\n   737:         self.0.recv(buf)\n   738:     }\n   739: \n   740:     /// Receives single datagram on the socket from the remote address to which it is\n   741:     /// connected, without removing the message from input queue. On success, returns\n   742:     /// the number of bytes peeked.\n   743:     ///\n   744:     /// The function must be called with valid byte array `buf` of sufficient size to\n   745:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   746:     /// excess bytes may be discarded.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::recv_from",
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
      "name": "recv_from",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
                      "tuple": [
                        {
                          "primitive": "usize"
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
    "verification_source": "   132:     /// Refer to the platform-specific documentation on this function; it is considered\n   133:     /// correct for its behavior to differ from [`UdpSocket::recv`] if the underlying system\n   134:     /// call does so.\n   135:     ///\n   136:     /// # Examples\n   137:     ///\n   138:     /// ```no_run\n   139:     /// use std::net::UdpSocket;\n   140:     ///\n   141:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   142:     /// let mut buf = [0; 10];\n   143:     /// let (number_of_bytes, src_addr) = socket.recv_from(&mut buf)\n   144:     ///                                         .expect(\"Didn't receive data\");\n   145:     /// let filled_buf = &mut buf[..number_of_bytes];\n   146:     /// ```\n   147:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   148:     pub fn recv_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   149:         self.0.recv_from(buf)\n   150:     }\n   151: \n   152:     /// Receives a single datagram message on the socket, without removing it from the\n   153:     /// queue. On success, returns the number of bytes read and the origin.\n   154:     ///\n   155:     /// The function must be called with valid byte array `buf` of sufficient size to\n   156:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   157:     /// excess bytes may be discarded.\n   158:     ///\n   159:     /// Successive calls return the same data. This is accomplished by passing\n   160:     /// `MSG_PEEK` as a flag to the underlying `recvfrom` system call.\n   161:     ///\n   162:     /// Do not use this function to implement busy waiting, instead use `libc::poll` to\n   163:     /// synchronize IO events on one or more sockets.\n   164:     ///",
    "nanvix_source": "   138:     /// ```no_run\n   139:     /// use std::net::UdpSocket;\n   140:     ///\n   141:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   142:     /// let mut buf = [0; 10];\n   143:     /// let (number_of_bytes, src_addr) = socket.recv_from(&mut buf)\n   144:     ///                                         .expect(\"Didn't receive data\");\n   145:     /// let filled_buf = &mut buf[..number_of_bytes];\n   146:     /// ```\n   147:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   148:     pub fn recv_from(&self, buf: &mut [u8]) -> io::Result<(usize, SocketAddr)> {\n   149:         self.0.recv_from(buf)\n   150:     }\n   151: \n   152:     /// Receives a single datagram message on the socket, without removing it from the\n   153:     /// queue. On success, returns the number of bytes read and the origin.\n   154:     ///\n   155:     /// The function must be called with valid byte array `buf` of sufficient size to\n   156:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   157:     /// excess bytes may be discarded.\n   158:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::net::UdpSocket::send",
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
      "name": "send",
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
            "id": 4677,
            "path": "UdpSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:4930",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4677",
        "resolved_owner_path": [
          "std",
          "net",
          "udp",
          "UdpSocket"
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
    "verification_source": "   688:     /// system may refuse buffers larger than 65507. However, partial writes are\n   689:     /// not possible until buffer sizes above `i32::MAX`.\n   690:     ///\n   691:     /// [`UdpSocket::connect`] will connect this socket to a remote address. This\n   692:     /// method will fail if the socket is not connected.\n   693:     ///\n   694:     /// # Examples\n   695:     ///\n   696:     /// ```no_run\n   697:     /// use std::net::UdpSocket;\n   698:     ///\n   699:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   700:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   701:     /// socket.send(&[0, 1, 2]).expect(\"couldn't send message\");\n   702:     /// ```\n   703:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   704:     pub fn send(&self, buf: &[u8]) -> io::Result<usize> {\n   705:         self.0.send(buf)\n   706:     }\n   707: \n   708:     /// Receives a single datagram message on the socket from the remote address to\n   709:     /// which it is connected. On success, returns the number of bytes read.\n   710:     ///\n   711:     /// The function must be called with valid byte array `buf` of sufficient size to\n   712:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   713:     /// excess bytes may be discarded.\n   714:     ///\n   715:     /// [`UdpSocket::connect`] will connect this socket to a remote address. This\n   716:     /// method will fail if the socket is not connected.\n   717:     ///\n   718:     /// Refer to the platform-specific documentation on this function; it is considered\n   719:     /// correct for its behavior to differ from [`UdpSocket::recv_from`] if the underlying\n   720:     /// system call does so.",
    "nanvix_source": "   694:     /// # Examples\n   695:     ///\n   696:     /// ```no_run\n   697:     /// use std::net::UdpSocket;\n   698:     ///\n   699:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   700:     /// socket.connect(\"127.0.0.1:8080\").expect(\"connect function failed\");\n   701:     /// socket.send(&[0, 1, 2]).expect(\"couldn't send message\");\n   702:     /// ```\n   703:     #[stable(feature = \"net2_mutators\", since = \"1.9.0\")]\n   704:     pub fn send(&self, buf: &[u8]) -> io::Result<usize> {\n   705:         self.0.send(buf)\n   706:     }\n   707: \n   708:     /// Receives a single datagram message on the socket from the remote address to\n   709:     /// which it is connected. On success, returns the number of bytes read.\n   710:     ///\n   711:     /// The function must be called with valid byte array `buf` of sufficient size to\n   712:     /// hold the message bytes. If a message is too long to fit in the supplied buffer,\n   713:     /// excess bytes may be discarded.\n   714:     ///",
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
