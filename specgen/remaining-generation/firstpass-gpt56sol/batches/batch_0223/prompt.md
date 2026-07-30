For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::fs::symlink_dir",
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
          },
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
            "name": "Q"
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
      "name": "symlink_dir",
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
            "original",
            {
              "generic": "P"
            }
          ],
          [
            "link",
            {
              "generic": "Q"
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
    "verification_source": "   678: ///\n   679: /// The `original` path must be a directory or a symlink to a directory,\n   680: /// otherwise the symlink will be broken. Use [`symlink_file`] for other files.\n   681: ///\n   682: /// This function currently corresponds to [`CreateSymbolicLinkW`][CreateSymbolicLinkW].\n   683: /// Note that this [may change in the future][changes].\n   684: ///\n   685: /// [CreateSymbolicLinkW]: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createsymboliclinkw\n   686: /// [changes]: io#platform-specific-behavior\n   687: ///\n   688: /// # Examples\n   689: ///\n   690: /// ```no_run\n   691: /// use std::os::windows::fs;\n   692: ///\n   693: /// fn main() -> std::io::Result<()> {\n   694: ///     fs::symlink_dir(\"a\", \"b\")?;\n   695: ///     Ok(())\n   696: /// }\n   697: /// ```\n   698: ///\n   699: /// # Limitations\n   700: ///\n   701: /// Windows treats symlink creation as a [privileged action][symlink-security],\n   702: /// therefore this function is likely to fail unless the user makes changes to\n   703: /// their system to permit symlink creation. Users can try enabling Developer\n   704: /// Mode, granting the `SeCreateSymbolicLinkPrivilege` privilege, or running\n   705: /// the process as an administrator.\n   706: ///\n   707: /// [symlink-security]: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links\n   708: #[stable(feature = \"symlink\", since = \"1.1.0\")]\n   709: pub fn symlink_dir<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n   710:     sys::fs::symlink_inner(original.as_ref(), link.as_ref(), true)",
    "nanvix_source": "   736: ///\n   737: /// [CreateSymbolicLinkW]: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createsymboliclinkw\n   738: /// [changes]: io#platform-specific-behavior\n   739: ///\n   740: /// # Examples\n   741: ///\n   742: /// ```no_run\n   743: /// use std::os::windows::fs;\n   744: ///\n   745: /// fn main() -> std::io::Result<()> {\n   746: ///     fs::symlink_dir(\"a\", \"b\")?;\n   747: ///     Ok(())\n   748: /// }\n   749: /// ```\n   750: ///\n   751: /// # Limitations\n   752: ///\n   753: /// Windows treats symlink creation as a [privileged action][symlink-security],\n   754: /// therefore this function is likely to fail unless the user makes changes to\n   755: /// their system to permit symlink creation. Users can try enabling Developer\n   756: /// Mode, granting the `SeCreateSymbolicLinkPrivilege` privilege, or running",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::symlink_file",
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
          },
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
            "name": "Q"
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
      "name": "symlink_file",
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
            "original",
            {
              "generic": "P"
            }
          ],
          [
            "link",
            {
              "generic": "Q"
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
    "verification_source": "   654: /// fn main() -> std::io::Result<()> {\n   655: ///     fs::symlink_file(\"a.txt\", \"b.txt\")?;\n   656: ///     Ok(())\n   657: /// }\n   658: /// ```\n   659: ///\n   660: /// # Limitations\n   661: ///\n   662: /// Windows treats symlink creation as a [privileged action][symlink-security],\n   663: /// therefore this function is likely to fail unless the user makes changes to\n   664: /// their system to permit symlink creation. Users can try enabling Developer\n   665: /// Mode, granting the `SeCreateSymbolicLinkPrivilege` privilege, or running\n   666: /// the process as an administrator.\n   667: ///\n   668: /// [symlink-security]: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links\n   669: #[stable(feature = \"symlink\", since = \"1.1.0\")]\n   670: pub fn symlink_file<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n   671:     sys::fs::symlink_inner(original.as_ref(), link.as_ref(), false)\n   672: }\n   673: \n   674: /// Creates a new symlink to a directory on the filesystem.\n   675: ///\n   676: /// The `link` path will be a directory symbolic link pointing to the `original`\n   677: /// path.\n   678: ///\n   679: /// The `original` path must be a directory or a symlink to a directory,\n   680: /// otherwise the symlink will be broken. Use [`symlink_file`] for other files.\n   681: ///\n   682: /// This function currently corresponds to [`CreateSymbolicLinkW`][CreateSymbolicLinkW].\n   683: /// Note that this [may change in the future][changes].\n   684: ///\n   685: /// [CreateSymbolicLinkW]: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createsymboliclinkw\n   686: /// [changes]: io#platform-specific-behavior",
    "nanvix_source": "   712: /// # Limitations\n   713: ///\n   714: /// Windows treats symlink creation as a [privileged action][symlink-security],\n   715: /// therefore this function is likely to fail unless the user makes changes to\n   716: /// their system to permit symlink creation. Users can try enabling Developer\n   717: /// Mode, granting the `SeCreateSymbolicLinkPrivilege` privilege, or running\n   718: /// the process as an administrator.\n   719: ///\n   720: /// [symlink-security]: https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/create-symbolic-links\n   721: #[stable(feature = \"symlink\", since = \"1.1.0\")]\n   722: pub fn symlink_file<P: AsRef<Path>, Q: AsRef<Path>>(original: P, link: Q) -> io::Result<()> {\n   723:     sys::fs::symlink_inner(original.as_ref(), link.as_ref(), false)\n   724: }\n   725: \n   726: /// Creates a new symlink to a directory on the filesystem.\n   727: ///\n   728: /// The `link` path will be a directory symbolic link pointing to the `original`\n   729: /// path.\n   730: ///\n   731: /// The `original` path must be a directory or a symlink to a directory,\n   732: /// otherwise the symlink will be broken. Use [`symlink_file`] for other files.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::BorrowedHandle::borrow_raw",
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
            "id": 586,
            "path": "BorrowedHandle"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5920",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:586",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "BorrowedHandle"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "handle",
            {
              "resolved_path": {
                "args": null,
                "id": 593,
                "path": "RawHandle"
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
    "verification_source": "   134:     ///\n   135:     /// # Safety\n   136:     ///\n   137:     /// The resource pointed to by `handle` must be a valid open handle, it\n   138:     /// must remain open for the duration of the returned `BorrowedHandle`.\n   139:     ///\n   140:     /// Note that it *may* have the value `INVALID_HANDLE_VALUE` (-1), which is\n   141:     /// sometimes a valid handle value. See [here] for the full story.\n   142:     ///\n   143:     /// And, it *may* have the value `NULL` (0), which can occur when consoles are\n   144:     /// detached from processes, or when `windows_subsystem` is used.\n   145:     ///\n   146:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   147:     #[inline]\n   148:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n   149:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   150:     pub const unsafe fn borrow_raw(handle: RawHandle) -> Self {\n   151:         Self { handle, _phantom: PhantomData }\n   152:     }\n   153: }\n   154: \n   155: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   156: impl TryFrom<HandleOrNull> for OwnedHandle {\n   157:     type Error = NullHandleError;\n   158: \n   159:     #[inline]\n   160:     fn try_from(handle_or_null: HandleOrNull) -> Result<Self, NullHandleError> {\n   161:         let handle_or_null = ManuallyDrop::new(handle_or_null);\n   162:         if handle_or_null.is_valid() {\n   163:             // SAFETY: The handle is not null.\n   164:             Ok(unsafe { OwnedHandle::from_raw_handle(handle_or_null.0) })\n   165:         } else {\n   166:             Err(NullHandleError(()))",
    "nanvix_source": "   140:     /// Note that it *may* have the value `INVALID_HANDLE_VALUE` (-1), which is\n   141:     /// sometimes a valid handle value. See [here] for the full story.\n   142:     ///\n   143:     /// And, it *may* have the value `NULL` (0), which can occur when consoles are\n   144:     /// detached from processes, or when `windows_subsystem` is used.\n   145:     ///\n   146:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   147:     #[inline]\n   148:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n   149:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   150:     pub const unsafe fn borrow_raw(handle: RawHandle) -> Self {\n   151:         Self { handle, _phantom: PhantomData }\n   152:     }\n   153: }\n   154: \n   155: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   156: impl TryFrom<HandleOrNull> for OwnedHandle {\n   157:     type Error = NullHandleError;\n   158: \n   159:     #[inline]\n   160:     fn try_from(handle_or_null: HandleOrNull) -> Result<Self, NullHandleError> {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::BorrowedHandle::try_clone_to_owned",
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
            "id": 586,
            "path": "BorrowedHandle"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5922",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:586",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "BorrowedHandle"
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
                        "id": 590,
                        "path": "OwnedHandle"
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
    "verification_source": "   180:     }\n   181: }\n   182: \n   183: impl OwnedHandle {\n   184:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   185:     /// object as the existing `OwnedHandle` instance.\n   186:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   187:     pub fn try_clone(&self) -> io::Result<Self> {\n   188:         self.as_handle().try_clone_to_owned()\n   189:     }\n   190: }\n   191: \n   192: impl BorrowedHandle<'_> {\n   193:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   194:     /// object as the existing `BorrowedHandle` instance.\n   195:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   196:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedHandle> {\n   197:         self.duplicate(0, false, sys::c::DUPLICATE_SAME_ACCESS)\n   198:     }\n   199: \n   200:     pub(crate) fn duplicate(\n   201:         &self,\n   202:         access: u32,\n   203:         inherit: bool,\n   204:         options: u32,\n   205:     ) -> io::Result<OwnedHandle> {\n   206:         let handle = self.as_raw_handle();\n   207: \n   208:         // `Stdin`, `Stdout`, and `Stderr` can all hold null handles, such as\n   209:         // in a process with a detached console. `DuplicateHandle` would fail\n   210:         // if we passed it a null handle, but we can treat null as a valid\n   211:         // handle which doesn't do any I/O, and allow it to be duplicated.\n   212:         if handle.is_null() {",
    "nanvix_source": "   186:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   187:     pub fn try_clone(&self) -> io::Result<Self> {\n   188:         self.as_handle().try_clone_to_owned()\n   189:     }\n   190: }\n   191: \n   192: impl BorrowedHandle<'_> {\n   193:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   194:     /// object as the existing `BorrowedHandle` instance.\n   195:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   196:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedHandle> {\n   197:         self.duplicate(0, false, sys::c::DUPLICATE_SAME_ACCESS)\n   198:     }\n   199: \n   200:     pub(crate) fn duplicate(\n   201:         &self,\n   202:         access: u32,\n   203:         inherit: bool,\n   204:         options: u32,\n   205:     ) -> io::Result<OwnedHandle> {\n   206:         let handle = self.as_raw_handle();",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::BorrowedSocket::borrow_raw",
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
            "id": 4770,
            "path": "BorrowedSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6179",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4770",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "socket",
          "BorrowedSocket"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "socket",
            {
              "resolved_path": {
                "args": null,
                "id": 4760,
                "path": "RawSocket"
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
    "verification_source": "    48: pub struct OwnedSocket {\n    49:     socket: ValidRawSocket,\n    50: }\n    51: \n    52: impl BorrowedSocket<'_> {\n    53:     /// Returns a `BorrowedSocket` holding the given raw socket.\n    54:     ///\n    55:     /// # Safety\n    56:     ///\n    57:     /// The resource pointed to by `socket` must remain open for the duration of\n    58:     /// the returned `BorrowedSocket`, and it must not have the value\n    59:     /// `INVALID_SOCKET`.\n    60:     #[inline]\n    61:     #[track_caller]\n    62:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    63:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    64:     pub const unsafe fn borrow_raw(socket: RawSocket) -> Self {\n    65:         Self { socket: ValidRawSocket::new(socket).expect(\"socket != -1\"), _phantom: PhantomData }\n    66:     }\n    67: }\n    68: \n    69: impl OwnedSocket {\n    70:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    71:     /// object as the existing `OwnedSocket` instance.\n    72:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    73:     pub fn try_clone(&self) -> io::Result<Self> {\n    74:         self.as_socket().try_clone_to_owned()\n    75:     }\n    76: \n    77:     // FIXME(strict_provenance_magic): we defined RawSocket to be a u64 ;-;\n    78:     #[allow(fuzzy_provenance_casts)]\n    79:     #[cfg(not(target_vendor = \"uwp\"))]\n    80:     pub(crate) fn set_no_inherit(&self) -> io::Result<()> {",
    "nanvix_source": "    54:     ///\n    55:     /// # Safety\n    56:     ///\n    57:     /// The resource pointed to by `socket` must remain open for the duration of\n    58:     /// the returned `BorrowedSocket`, and it must not have the value\n    59:     /// `INVALID_SOCKET`.\n    60:     #[inline]\n    61:     #[track_caller]\n    62:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    63:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    64:     pub const unsafe fn borrow_raw(socket: RawSocket) -> Self {\n    65:         Self { socket: ValidRawSocket::new(socket).expect(\"socket != -1\"), _phantom: PhantomData }\n    66:     }\n    67: }\n    68: \n    69: impl OwnedSocket {\n    70:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    71:     /// object as the existing `OwnedSocket` instance.\n    72:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    73:     pub fn try_clone(&self) -> io::Result<Self> {\n    74:         self.as_socket().try_clone_to_owned()",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::BorrowedSocket::try_clone_to_owned",
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
            "id": 4770,
            "path": "BorrowedSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6181",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4770",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "socket",
          "BorrowedSocket"
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
                        "id": 4774,
                        "path": "OwnedSocket"
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
    "verification_source": "    85:                 0,\n    86:             )\n    87:         })\n    88:         .map(drop)\n    89:     }\n    90: \n    91:     #[cfg(target_vendor = \"uwp\")]\n    92:     pub(crate) fn set_no_inherit(&self) -> io::Result<()> {\n    93:         Err(io::const_error!(io::ErrorKind::Unsupported, \"unavailable on UWP\"))\n    94:     }\n    95: }\n    96: \n    97: impl BorrowedSocket<'_> {\n    98:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    99:     /// object as the existing `BorrowedSocket` instance.\n   100:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   101:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedSocket> {\n   102:         let mut info = unsafe { mem::zeroed::<sys::c::WSAPROTOCOL_INFOW>() };\n   103:         let result = unsafe {\n   104:             sys::c::WSADuplicateSocketW(\n   105:                 self.as_raw_socket() as sys::c::SOCKET,\n   106:                 sys::c::GetCurrentProcessId(),\n   107:                 &mut info,\n   108:             )\n   109:         };\n   110:         sys::net::cvt(result)?;\n   111:         let socket = unsafe {\n   112:             sys::c::WSASocketW(\n   113:                 info.iAddressFamily,\n   114:                 info.iSocketType,\n   115:                 info.iProtocol,\n   116:                 &info,\n   117:                 0,",
    "nanvix_source": "    91:     #[cfg(target_vendor = \"uwp\")]\n    92:     pub(crate) fn set_no_inherit(&self) -> io::Result<()> {\n    93:         Err(io::const_error!(io::ErrorKind::Unsupported, \"unavailable on UWP\"))\n    94:     }\n    95: }\n    96: \n    97: impl BorrowedSocket<'_> {\n    98:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    99:     /// object as the existing `BorrowedSocket` instance.\n   100:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   101:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedSocket> {\n   102:         let mut info = unsafe { mem::zeroed::<sys::c::WSAPROTOCOL_INFOW>() };\n   103:         let result = unsafe {\n   104:             sys::c::WSADuplicateSocketW(\n   105:                 self.as_raw_socket() as sys::c::SOCKET,\n   106:                 sys::c::GetCurrentProcessId(),\n   107:                 &mut info,\n   108:             )\n   109:         };\n   110:         sys::net::cvt(result)?;\n   111:         let socket = unsafe {",
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
