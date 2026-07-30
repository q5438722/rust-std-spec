For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::net::UdpSocket::write_timeout",
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
    "verification_source": "   385:     /// Returns the write timeout of this socket.\n   386:     ///\n   387:     /// If the timeout is [`None`], then [`write`] calls will block indefinitely.\n   388:     ///\n   389:     /// [`write`]: io::Write::write\n   390:     ///\n   391:     /// # Examples\n   392:     ///\n   393:     /// ```no_run\n   394:     /// use std::net::UdpSocket;\n   395:     ///\n   396:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   397:     /// socket.set_write_timeout(None).expect(\"set_write_timeout call failed\");\n   398:     /// assert_eq!(socket.write_timeout().unwrap(), None);\n   399:     /// ```\n   400:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   401:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   402:         self.0.write_timeout()\n   403:     }\n   404: \n   405:     /// Sets the value of the `SO_BROADCAST` option for this socket.\n   406:     ///\n   407:     /// When enabled, this socket is allowed to send packets to a broadcast\n   408:     /// address.\n   409:     ///\n   410:     /// # Examples\n   411:     ///\n   412:     /// ```no_run\n   413:     /// use std::net::UdpSocket;\n   414:     ///\n   415:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   416:     /// socket.set_broadcast(false).expect(\"set_broadcast call failed\");\n   417:     /// ```",
    "nanvix_source": "   391:     /// # Examples\n   392:     ///\n   393:     /// ```no_run\n   394:     /// use std::net::UdpSocket;\n   395:     ///\n   396:     /// let socket = UdpSocket::bind(\"127.0.0.1:34254\").expect(\"couldn't bind to address\");\n   397:     /// socket.set_write_timeout(None).expect(\"set_write_timeout call failed\");\n   398:     /// assert_eq!(socket.write_timeout().unwrap(), None);\n   399:     /// ```\n   400:     #[stable(feature = \"socket_timeout\", since = \"1.4.0\")]\n   401:     pub fn write_timeout(&self) -> io::Result<Option<Duration>> {\n   402:         self.0.write_timeout()\n   403:     }\n   404: \n   405:     /// Sets the value of the `SO_BROADCAST` option for this socket.\n   406:     ///\n   407:     /// When enabled, this socket is allowed to send packets to a broadcast\n   408:     /// address.\n   409:     ///\n   410:     /// # Examples\n   411:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::BorrowedFd::borrow_raw",
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
        "is_const": true,
        "is_unsafe": true
      },
      "name": "borrow_raw",
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
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6512",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2698",
        "resolved_owner_path": [
          "std",
          "os",
          "fd",
          "owned",
          "BorrowedFd"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "fd",
            {
              "resolved_path": {
                "args": null,
                "id": 2688,
                "path": "RawFd"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "    73: \n    74: impl BorrowedFd<'_> {\n    75:     /// Returns a `BorrowedFd` holding the given raw file descriptor.\n    76:     ///\n    77:     /// # Safety\n    78:     ///\n    79:     /// The resource pointed to by `fd` must remain open for the duration of\n    80:     /// the returned `BorrowedFd`.\n    81:     ///\n    82:     /// # Panics\n    83:     ///\n    84:     /// Panics if the raw file descriptor has the value `-1`.\n    85:     #[inline]\n    86:     #[track_caller]\n    87:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    88:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    89:     pub const unsafe fn borrow_raw(fd: RawFd) -> Self {\n    90:         Self { fd: ValidRawFd::new(fd).expect(\"fd != -1\"), _phantom: PhantomData }\n    91:     }\n    92: }\n    93: \n    94: impl OwnedFd {\n    95:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n    96:     /// description as the existing `OwnedFd` instance.\n    97:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    98:     pub fn try_clone(&self) -> io::Result<Self> {\n    99:         self.as_fd().try_clone_to_owned()\n   100:     }\n   101: }\n   102: \n   103: impl BorrowedFd<'_> {\n   104:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n   105:     /// description as the existing `BorrowedFd` instance.",
    "nanvix_source": "    79:     /// The resource pointed to by `fd` must remain open for the duration of\n    80:     /// the returned `BorrowedFd`.\n    81:     ///\n    82:     /// # Panics\n    83:     ///\n    84:     /// Panics if the raw file descriptor has the value `-1`.\n    85:     #[inline]\n    86:     #[track_caller]\n    87:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    88:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    89:     pub const unsafe fn borrow_raw(fd: RawFd) -> Self {\n    90:         Self { fd: ValidRawFd::new(fd).expect(\"fd != -1\"), _phantom: PhantomData }\n    91:     }\n    92: }\n    93: \n    94: impl OwnedFd {\n    95:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n    96:     /// description as the existing `OwnedFd` instance.\n    97:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    98:     pub fn try_clone(&self) -> io::Result<Self> {\n    99:         self.as_fd().try_clone_to_owned()",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::BorrowedFd::try_clone_to_owned",
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
      "name": "try_clone_to_owned",
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
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6513",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2698",
        "resolved_owner_path": [
          "std",
          "os",
          "fd",
          "owned",
          "BorrowedFd"
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
                        "id": 2702,
                        "path": "OwnedFd"
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
    "verification_source": "    97:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    98:     pub fn try_clone(&self) -> io::Result<Self> {\n    99:         self.as_fd().try_clone_to_owned()\n   100:     }\n   101: }\n   102: \n   103: impl BorrowedFd<'_> {\n   104:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n   105:     /// description as the existing `BorrowedFd` instance.\n   106:     #[cfg(not(any(\n   107:         target_arch = \"wasm32\",\n   108:         target_os = \"hermit\",\n   109:         target_os = \"trusty\",\n   110:         target_os = \"motor\"\n   111:     )))]\n   112:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   113:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedFd> {\n   114:         // We want to atomically duplicate this file descriptor and set the\n   115:         // CLOEXEC flag, and currently that's done via F_DUPFD_CLOEXEC. This\n   116:         // is a POSIX flag that was added to Linux in 2.6.24.\n   117:         #[cfg(not(any(target_os = \"espidf\", target_os = \"vita\")))]\n   118:         let cmd = libc::F_DUPFD_CLOEXEC;\n   119: \n   120:         // For ESP-IDF, F_DUPFD is used instead, because the CLOEXEC semantics\n   121:         // will never be supported, as this is a bare metal framework with\n   122:         // no capabilities for multi-process execution. While F_DUPFD is also\n   123:         // not supported yet, it might be (currently it returns ENOSYS).\n   124:         #[cfg(any(target_os = \"espidf\", target_os = \"vita\"))]\n   125:         let cmd = libc::F_DUPFD;\n   126: \n   127:         // Avoid using file descriptors below 3 as they are used for stdio\n   128:         let fd = cvt(unsafe { libc::fcntl(self.as_raw_fd(), cmd, 3) })?;\n   129:         Ok(unsafe { OwnedFd::from_raw_fd(fd) })",
    "nanvix_source": "   103: impl BorrowedFd<'_> {\n   104:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n   105:     /// description as the existing `BorrowedFd` instance.\n   106:     #[cfg(not(any(\n   107:         target_arch = \"wasm32\",\n   108:         target_os = \"hermit\",\n   109:         target_os = \"trusty\",\n   110:         target_os = \"motor\"\n   111:     )))]\n   112:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   113:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedFd> {\n   114:         // We want to atomically duplicate this file descriptor and set the\n   115:         // CLOEXEC flag, and currently that's done via F_DUPFD_CLOEXEC. This\n   116:         // is a POSIX flag that was added to Linux in 2.6.24.\n   117:         #[cfg(not(any(target_os = \"espidf\", target_os = \"vita\")))]\n   118:         let cmd = libc::F_DUPFD_CLOEXEC;\n   119: \n   120:         // For ESP-IDF, F_DUPFD is used instead, because the CLOEXEC semantics\n   121:         // will never be supported, as this is a bare metal framework with\n   122:         // no capabilities for multi-process execution. While F_DUPFD is also\n   123:         // not supported yet, it might be (currently it returns ENOSYS).",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::fd::OwnedFd::try_clone",
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
            "id": 2702,
            "path": "OwnedFd"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6539",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2702",
        "resolved_owner_path": [
          "std",
          "os",
          "fd",
          "owned",
          "OwnedFd"
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
                      "generic": "Self"
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
    "verification_source": "    82:     /// # Panics\n    83:     ///\n    84:     /// Panics if the raw file descriptor has the value `-1`.\n    85:     #[inline]\n    86:     #[track_caller]\n    87:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    88:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    89:     pub const unsafe fn borrow_raw(fd: RawFd) -> Self {\n    90:         Self { fd: ValidRawFd::new(fd).expect(\"fd != -1\"), _phantom: PhantomData }\n    91:     }\n    92: }\n    93: \n    94: impl OwnedFd {\n    95:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n    96:     /// description as the existing `OwnedFd` instance.\n    97:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    98:     pub fn try_clone(&self) -> io::Result<Self> {\n    99:         self.as_fd().try_clone_to_owned()\n   100:     }\n   101: }\n   102: \n   103: impl BorrowedFd<'_> {\n   104:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n   105:     /// description as the existing `BorrowedFd` instance.\n   106:     #[cfg(not(any(\n   107:         target_arch = \"wasm32\",\n   108:         target_os = \"hermit\",\n   109:         target_os = \"trusty\",\n   110:         target_os = \"motor\"\n   111:     )))]\n   112:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   113:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedFd> {\n   114:         // We want to atomically duplicate this file descriptor and set the",
    "nanvix_source": "    88:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    89:     pub const unsafe fn borrow_raw(fd: RawFd) -> Self {\n    90:         Self { fd: ValidRawFd::new(fd).expect(\"fd != -1\"), _phantom: PhantomData }\n    91:     }\n    92: }\n    93: \n    94: impl OwnedFd {\n    95:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n    96:     /// description as the existing `OwnedFd` instance.\n    97:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    98:     pub fn try_clone(&self) -> io::Result<Self> {\n    99:         self.as_fd().try_clone_to_owned()\n   100:     }\n   101: }\n   102: \n   103: impl BorrowedFd<'_> {\n   104:     /// Creates a new `OwnedFd` instance that shares the same underlying file\n   105:     /// description as the existing `BorrowedFd` instance.\n   106:     #[cfg(not(any(\n   107:         target_arch = \"wasm32\",\n   108:         target_os = \"hermit\",",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::chown",
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
                                    "path": "crate::path::Path"
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
      "name": "chown",
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
        "inputs": [
          [
            "dir",
            {
              "generic": "P"
            }
          ],
          [
            "uid",
            {
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
                "id": 56,
                "path": "Option"
              }
            }
          ],
          [
            "gid",
            {
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
    "verification_source": "  1106: /// This call may also clear file capabilities, if there was any.\n  1107: ///\n  1108: /// If called on a symbolic link, this will change the owner and group of the link target. To\n  1109: /// change the owner and group of the link itself, see [`lchown`].\n  1110: ///\n  1111: /// # Examples\n  1112: ///\n  1113: /// ```no_run\n  1114: /// use std::os::unix::fs;\n  1115: ///\n  1116: /// fn main() -> std::io::Result<()> {\n  1117: ///     fs::chown(\"/sandbox\", Some(0), Some(0))?;\n  1118: ///     Ok(())\n  1119: /// }\n  1120: /// ```\n  1121: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1122: pub fn chown<P: AsRef<Path>>(dir: P, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1123:     sys::fs::chown(dir.as_ref(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1124: }\n  1125: \n  1126: /// Change the owner and group of the file referenced by the specified open file descriptor.\n  1127: ///\n  1128: /// For semantics and required privileges, see [`chown`].\n  1129: ///\n  1130: /// # Examples\n  1131: ///\n  1132: /// ```no_run\n  1133: /// use std::os::unix::fs;\n  1134: ///\n  1135: /// fn main() -> std::io::Result<()> {\n  1136: ///     let f = std::fs::File::open(\"/file\")?;\n  1137: ///     fs::fchown(&f, Some(0), Some(0))?;\n  1138: ///     Ok(())",
    "nanvix_source": "  1111: ///\n  1112: /// ```no_run\n  1113: /// use std::os::unix::fs;\n  1114: ///\n  1115: /// fn main() -> std::io::Result<()> {\n  1116: ///     fs::chown(\"/sandbox\", Some(0), Some(0))?;\n  1117: ///     Ok(())\n  1118: /// }\n  1119: /// ```\n  1120: #[stable(feature = \"unix_chown\", since = \"1.73.0\")]\n  1121: pub fn chown<P: AsRef<Path>>(dir: P, uid: Option<u32>, gid: Option<u32>) -> io::Result<()> {\n  1122:     sys::fs::chown(dir.as_ref(), uid.unwrap_or(u32::MAX), gid.unwrap_or(u32::MAX))\n  1123: }\n  1124: \n  1125: /// Change the owner and group of the file referenced by the specified open file descriptor.\n  1126: ///\n  1127: /// For semantics and required privileges, see [`chown`].\n  1128: ///\n  1129: /// # Examples\n  1130: ///\n  1131: /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::unix::fs::chroot",
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
                                    "path": "crate::path::Path"
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
      "name": "chroot",
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
        "inputs": [
          [
            "dir",
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
    "verification_source": "  1168: /// This typically requires privileges, such as root or a specific capability.\n  1169: ///\n  1170: /// This does not change the current working directory; you should call\n  1171: /// [`std::env::set_current_dir`][`crate::env::set_current_dir`] afterwards.\n  1172: ///\n  1173: /// # Examples\n  1174: ///\n  1175: /// ```no_run\n  1176: /// use std::os::unix::fs;\n  1177: ///\n  1178: /// fn main() -> std::io::Result<()> {\n  1179: ///     fs::chroot(\"/sandbox\")?;\n  1180: ///     std::env::set_current_dir(\"/\")?;\n  1181: ///     // continue working in sandbox\n  1182: ///     Ok(())\n  1183: /// }\n  1184: /// ```\n  1185: #[stable(feature = \"unix_chroot\", since = \"1.56.0\")]\n  1186: #[cfg(not(target_os = \"fuchsia\"))]\n  1187: pub fn chroot<P: AsRef<Path>>(dir: P) -> io::Result<()> {\n  1188:     sys::fs::chroot(dir.as_ref())\n  1189: }\n  1190: \n  1191: /// Create a FIFO special file at the specified path with the specified mode.\n  1192: ///\n  1193: /// # Examples\n  1194: ///\n  1195: /// ```no_run\n  1196: /// # #![feature(unix_mkfifo)]\n  1197: /// # #[cfg(not(unix))]\n  1198: /// # fn main() {}\n  1199: /// # #[cfg(unix)]\n  1200: /// # fn main() -> std::io::Result<()> {",
    "nanvix_source": "  1173: ///\n  1174: /// ```no_run\n  1175: /// use std::os::unix::fs;\n  1176: ///\n  1177: /// fn main() -> std::io::Result<()> {\n  1178: ///     fs::chroot(\"/sandbox\")?;\n  1179: ///     std::env::set_current_dir(\"/\")?;\n  1180: ///     // continue working in sandbox\n  1181: ///     Ok(())\n  1182: /// }\n  1183: /// ```\n  1184: #[stable(feature = \"unix_chroot\", since = \"1.56.0\")]\n  1185: #[cfg(not(target_os = \"fuchsia\"))]\n  1186: pub fn chroot<P: AsRef<Path>>(dir: P) -> io::Result<()> {\n  1187:     sys::fs::chroot(dir.as_ref())\n  1188: }\n  1189: \n  1190: /// Create a FIFO special file at the specified path with the specified mode.\n  1191: ///\n  1192: /// # Examples\n  1193: ///",
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
