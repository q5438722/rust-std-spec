For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::unix::net::UnixDatagram::send_to_addr",
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
      "name": "send_to_addr",
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
    "verification_source": "   542:     ///\n   543:     /// # Examples\n   544:     ///\n   545:     /// ```no_run\n   546:     /// use std::os::unix::net::{UnixDatagram};\n   547:     ///\n   548:     /// fn main() -> std::io::Result<()> {\n   549:     ///     let bound = UnixDatagram::bind(\"/path/to/socket\")?;\n   550:     ///     let addr = bound.local_addr()?;\n   551:     ///\n   552:     ///     let sock = UnixDatagram::unbound()?;\n   553:     ///     sock.send_to_addr(b\"bacon egg and cheese\", &addr).expect(\"send_to_addr function failed\");\n   554:     ///     Ok(())\n   555:     /// }\n   556:     /// ```\n   557:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   558:     pub fn send_to_addr(&self, buf: &[u8], socket_addr: &SocketAddr) -> io::Result<usize> {\n   559:         unsafe {\n   560:             let count = cvt(libc::sendto(\n   561:                 self.as_raw_fd(),\n   562:                 buf.as_ptr() as *const _,\n   563:                 buf.len(),\n   564:                 MSG_NOSIGNAL,\n   565:                 (&raw const socket_addr.addr) as *const _,\n   566:                 socket_addr.len,\n   567:             ))?;\n   568:             Ok(count as usize)\n   569:         }\n   570:     }\n   571: \n   572:     /// Sends data on the socket to the socket's peer.\n   573:     ///\n   574:     /// The peer address may be set by the `connect` method, and this method",
    "nanvix_source": "   545:     /// fn main() -> std::io::Result<()> {\n   546:     ///     let bound = UnixDatagram::bind(\"/path/to/socket\")?;\n   547:     ///     let addr = bound.local_addr()?;\n   548:     ///\n   549:     ///     let sock = UnixDatagram::unbound()?;\n   550:     ///     sock.send_to_addr(b\"bacon egg and cheese\", &addr).expect(\"send_to_addr function failed\");\n   551:     ///     Ok(())\n   552:     /// }\n   553:     /// ```\n   554:     #[stable(feature = \"unix_socket_abstract\", since = \"1.70.0\")]\n   555:     pub fn send_to_addr(&self, buf: &[u8], socket_addr: &SocketAddr) -> io::Result<usize> {\n   556:         unsafe {\n   557:             let count = cvt(libc::sendto(\n   558:                 self.as_raw_fd(),\n   559:                 buf.as_ptr() as *const _,\n   560:                 buf.len(),\n   561:                 MSG_NOSIGNAL,\n   562:                 (&raw const socket_addr.addr) as *const _,\n   563:                 socket_addr.len,\n   564:             ))?;\n   565:             Ok(count as usize)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::set_nonblocking",
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
    "verification_source": "   819:     }\n   820: \n   821:     /// Moves the socket into or out of nonblocking mode.\n   822:     ///\n   823:     /// # Examples\n   824:     ///\n   825:     /// ```\n   826:     /// use std::os::unix::net::UnixDatagram;\n   827:     ///\n   828:     /// fn main() -> std::io::Result<()> {\n   829:     ///     let sock = UnixDatagram::unbound()?;\n   830:     ///     sock.set_nonblocking(true).expect(\"set_nonblocking function failed\");\n   831:     ///     Ok(())\n   832:     /// }\n   833:     /// ```\n   834:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   835:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   836:         self.0.set_nonblocking(nonblocking)\n   837:     }\n   838: \n   839:     /// Set the id of the socket for network filtering purpose\n   840:     ///\n   841:     #[cfg_attr(\n   842:         any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\"),\n   843:         doc = \"```no_run\"\n   844:     )]\n   845:     #[cfg_attr(\n   846:         not(any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\")),\n   847:         doc = \"```ignore\"\n   848:     )]\n   849:     /// #![feature(unix_set_mark)]\n   850:     /// use std::os::unix::net::UnixDatagram;\n   851:     ///",
    "nanvix_source": "   822:     /// ```\n   823:     /// use std::os::unix::net::UnixDatagram;\n   824:     ///\n   825:     /// fn main() -> std::io::Result<()> {\n   826:     ///     let sock = UnixDatagram::unbound()?;\n   827:     ///     sock.set_nonblocking(true).expect(\"set_nonblocking function failed\");\n   828:     ///     Ok(())\n   829:     /// }\n   830:     /// ```\n   831:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   832:     pub fn set_nonblocking(&self, nonblocking: bool) -> io::Result<()> {\n   833:         self.0.set_nonblocking(nonblocking)\n   834:     }\n   835: \n   836:     /// Set the id of the socket for network filtering purpose\n   837:     ///\n   838:     #[cfg_attr(\n   839:         any(target_os = \"linux\", target_os = \"freebsd\", target_os = \"openbsd\"),\n   840:         doc = \"```no_run\"\n   841:     )]\n   842:     #[cfg_attr(",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::set_read_timeout",
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
      "name": "set_read_timeout",
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
            "timeout",
            {
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
    "verification_source": "   715:     /// method:\n   716:     ///\n   717:     /// ```no_run\n   718:     /// use std::io;\n   719:     /// use std::os::unix::net::UnixDatagram;\n   720:     /// use std::time::Duration;\n   721:     ///\n   722:     /// fn main() -> std::io::Result<()> {\n   723:     ///     let socket = UnixDatagram::unbound()?;\n   724:     ///     let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   725:     ///     let err = result.unwrap_err();\n   726:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   727:     ///     Ok(())\n   728:     /// }\n   729:     /// ```\n   730:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   731:     pub fn set_read_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   732:         self.0.set_timeout(timeout, libc::SO_RCVTIMEO)\n   733:     }\n   734: \n   735:     /// Sets the write timeout for the socket.\n   736:     ///\n   737:     /// If the provided value is [`None`], then [`send`] and [`send_to`] calls will\n   738:     /// block indefinitely. An [`Err`] is returned if the zero [`Duration`] is passed to this\n   739:     /// method.\n   740:     ///\n   741:     /// [`send`]: UnixDatagram::send\n   742:     /// [`send_to`]: UnixDatagram::send_to\n   743:     ///\n   744:     /// # Examples\n   745:     ///\n   746:     /// ```\n   747:     /// use std::os::unix::net::UnixDatagram;",
    "nanvix_source": "   718:     ///\n   719:     /// fn main() -> std::io::Result<()> {\n   720:     ///     let socket = UnixDatagram::unbound()?;\n   721:     ///     let result = socket.set_read_timeout(Some(Duration::new(0, 0)));\n   722:     ///     let err = result.unwrap_err();\n   723:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   724:     ///     Ok(())\n   725:     /// }\n   726:     /// ```\n   727:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   728:     pub fn set_read_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   729:         self.0.set_timeout(timeout, libc::SO_RCVTIMEO)\n   730:     }\n   731: \n   732:     /// Sets the write timeout for the socket.\n   733:     ///\n   734:     /// If the provided value is [`None`], then [`send`] and [`send_to`] calls will\n   735:     /// block indefinitely. An [`Err`] is returned if the zero [`Duration`] is passed to this\n   736:     /// method.\n   737:     ///\n   738:     /// [`send`]: UnixDatagram::send",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::set_write_timeout",
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
      "name": "set_write_timeout",
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
            "timeout",
            {
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
    "verification_source": "   759:     /// method:\n   760:     ///\n   761:     /// ```no_run\n   762:     /// use std::io;\n   763:     /// use std::os::unix::net::UnixDatagram;\n   764:     /// use std::time::Duration;\n   765:     ///\n   766:     /// fn main() -> std::io::Result<()> {\n   767:     ///     let socket = UnixDatagram::unbound()?;\n   768:     ///     let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   769:     ///     let err = result.unwrap_err();\n   770:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   771:     ///     Ok(())\n   772:     /// }\n   773:     /// ```\n   774:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   775:     pub fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   776:         self.0.set_timeout(timeout, libc::SO_SNDTIMEO)\n   777:     }\n   778: \n   779:     /// Returns the read timeout of this socket.\n   780:     ///\n   781:     /// # Examples\n   782:     ///\n   783:     /// ```\n   784:     /// use std::os::unix::net::UnixDatagram;\n   785:     /// use std::time::Duration;\n   786:     ///\n   787:     /// fn main() -> std::io::Result<()> {\n   788:     ///     let sock = UnixDatagram::unbound()?;\n   789:     ///     sock.set_read_timeout(Some(Duration::new(1, 0)))\n   790:     ///         .expect(\"set_read_timeout function failed\");\n   791:     ///     assert_eq!(sock.read_timeout()?, Some(Duration::new(1, 0)));",
    "nanvix_source": "   762:     ///\n   763:     /// fn main() -> std::io::Result<()> {\n   764:     ///     let socket = UnixDatagram::unbound()?;\n   765:     ///     let result = socket.set_write_timeout(Some(Duration::new(0, 0)));\n   766:     ///     let err = result.unwrap_err();\n   767:     ///     assert_eq!(err.kind(), io::ErrorKind::InvalidInput);\n   768:     ///     Ok(())\n   769:     /// }\n   770:     /// ```\n   771:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   772:     pub fn set_write_timeout(&self, timeout: Option<Duration>) -> io::Result<()> {\n   773:         self.0.set_timeout(timeout, libc::SO_SNDTIMEO)\n   774:     }\n   775: \n   776:     /// Returns the read timeout of this socket.\n   777:     ///\n   778:     /// # Examples\n   779:     ///\n   780:     /// ```\n   781:     /// use std::os::unix::net::UnixDatagram;\n   782:     /// use std::time::Duration;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::shutdown",
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
      "name": "shutdown",
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
            "how",
            {
              "resolved_path": {
                "args": null,
                "id": 4727,
                "path": "Shutdown"
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
    "verification_source": "   885:     ///\n   886:     /// This function will cause all pending and future I/O calls on the\n   887:     /// specified portions to immediately return with an appropriate value\n   888:     /// (see the documentation of [`Shutdown`]).\n   889:     ///\n   890:     /// ```no_run\n   891:     /// use std::os::unix::net::UnixDatagram;\n   892:     /// use std::net::Shutdown;\n   893:     ///\n   894:     /// fn main() -> std::io::Result<()> {\n   895:     ///     let sock = UnixDatagram::unbound()?;\n   896:     ///     sock.shutdown(Shutdown::Both).expect(\"shutdown function failed\");\n   897:     ///     Ok(())\n   898:     /// }\n   899:     /// ```\n   900:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   901:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   902:         self.0.shutdown(how)\n   903:     }\n   904: \n   905:     /// Receives data on the socket from the remote address to which it is\n   906:     /// connected, without removing that data from the queue. On success,\n   907:     /// returns the number of bytes peeked.\n   908:     ///\n   909:     /// Successive calls return the same data. This is accomplished by passing\n   910:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   911:     ///\n   912:     /// # Examples\n   913:     ///\n   914:     /// ```no_run\n   915:     /// #![feature(unix_socket_peek)]\n   916:     ///\n   917:     /// use std::os::unix::net::UnixDatagram;",
    "nanvix_source": "   888:     /// use std::os::unix::net::UnixDatagram;\n   889:     /// use std::net::Shutdown;\n   890:     ///\n   891:     /// fn main() -> std::io::Result<()> {\n   892:     ///     let sock = UnixDatagram::unbound()?;\n   893:     ///     sock.shutdown(Shutdown::Both).expect(\"shutdown function failed\");\n   894:     ///     Ok(())\n   895:     /// }\n   896:     /// ```\n   897:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   898:     pub fn shutdown(&self, how: Shutdown) -> io::Result<()> {\n   899:         self.0.shutdown(how)\n   900:     }\n   901: \n   902:     /// Receives data on the socket from the remote address to which it is\n   903:     /// connected, without removing that data from the queue. On success,\n   904:     /// returns the number of bytes peeked.\n   905:     ///\n   906:     /// Successive calls return the same data. This is accomplished by passing\n   907:     /// `MSG_PEEK` as a flag to the underlying `recv` system call.\n   908:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::net::UnixDatagram::take_error",
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
    "verification_source": "   864:     /// Returns the value of the `SO_ERROR` option.\n   865:     ///\n   866:     /// # Examples\n   867:     ///\n   868:     /// ```no_run\n   869:     /// use std::os::unix::net::UnixDatagram;\n   870:     ///\n   871:     /// fn main() -> std::io::Result<()> {\n   872:     ///     let sock = UnixDatagram::unbound()?;\n   873:     ///     if let Ok(Some(err)) = sock.take_error() {\n   874:     ///         println!(\"Got error: {err:?}\");\n   875:     ///     }\n   876:     ///     Ok(())\n   877:     /// }\n   878:     /// ```\n   879:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   880:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   881:         self.0.take_error()\n   882:     }\n   883: \n   884:     /// Shut down the read, write, or both halves of this connection.\n   885:     ///\n   886:     /// This function will cause all pending and future I/O calls on the\n   887:     /// specified portions to immediately return with an appropriate value\n   888:     /// (see the documentation of [`Shutdown`]).\n   889:     ///\n   890:     /// ```no_run\n   891:     /// use std::os::unix::net::UnixDatagram;\n   892:     /// use std::net::Shutdown;\n   893:     ///\n   894:     /// fn main() -> std::io::Result<()> {\n   895:     ///     let sock = UnixDatagram::unbound()?;\n   896:     ///     sock.shutdown(Shutdown::Both).expect(\"shutdown function failed\");",
    "nanvix_source": "   867:     ///\n   868:     /// fn main() -> std::io::Result<()> {\n   869:     ///     let sock = UnixDatagram::unbound()?;\n   870:     ///     if let Ok(Some(err)) = sock.take_error() {\n   871:     ///         println!(\"Got error: {err:?}\");\n   872:     ///     }\n   873:     ///     Ok(())\n   874:     /// }\n   875:     /// ```\n   876:     #[stable(feature = \"unix_socket\", since = \"1.10.0\")]\n   877:     pub fn take_error(&self) -> io::Result<Option<io::Error>> {\n   878:         self.0.take_error()\n   879:     }\n   880: \n   881:     /// Shut down the read, write, or both halves of this connection.\n   882:     ///\n   883:     /// This function will cause all pending and future I/O calls on the\n   884:     /// specified portions to immediately return with an appropriate value\n   885:     /// (see the documentation of [`Shutdown`]).\n   886:     ///\n   887:     /// ```no_run",
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
