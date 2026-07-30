For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::io::HandleOrInvalid::from_raw_handle",
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
        "is_unsafe": true
      },
      "name": "from_raw_handle",
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
            "id": 5973,
            "path": "HandleOrInvalid"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6027",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5973",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "HandleOrInvalid"
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
    "verification_source": "   357:     /// from a Windows API that uses `INVALID_HANDLE_VALUE` to indicate\n   358:     /// failure, such as `CreateFileW`.\n   359:     ///\n   360:     /// Use `HandleOrNull` instead of `HandleOrInvalid` for APIs that\n   361:     /// use null to indicate failure.\n   362:     ///\n   363:     /// # Safety\n   364:     ///\n   365:     /// The passed `handle` value must either satisfy the safety requirements\n   366:     /// of [`FromRawHandle::from_raw_handle`], or be\n   367:     /// `INVALID_HANDLE_VALUE` (-1). Note that not all Windows APIs use\n   368:     /// `INVALID_HANDLE_VALUE` for errors; see [here] for the full story.\n   369:     ///\n   370:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   371:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   372:     #[inline]\n   373:     pub unsafe fn from_raw_handle(handle: RawHandle) -> Self {\n   374:         Self(handle)\n   375:     }\n   376: \n   377:     fn is_valid(&self) -> bool {\n   378:         self.0 != sys::c::INVALID_HANDLE_VALUE\n   379:     }\n   380: }\n   381: \n   382: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   383: impl Drop for OwnedHandle {\n   384:     #[inline]\n   385:     fn drop(&mut self) {\n   386:         unsafe {\n   387:             let _ = sys::c::CloseHandle(self.handle);\n   388:         }\n   389:     }",
    "nanvix_source": "   363:     /// # Safety\n   364:     ///\n   365:     /// The passed `handle` value must either satisfy the safety requirements\n   366:     /// of [`FromRawHandle::from_raw_handle`], or be\n   367:     /// `INVALID_HANDLE_VALUE` (-1). Note that not all Windows APIs use\n   368:     /// `INVALID_HANDLE_VALUE` for errors; see [here] for the full story.\n   369:     ///\n   370:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   371:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   372:     #[inline]\n   373:     pub unsafe fn from_raw_handle(handle: RawHandle) -> Self {\n   374:         Self(handle)\n   375:     }\n   376: \n   377:     fn is_valid(&self) -> bool {\n   378:         self.0 != sys::c::INVALID_HANDLE_VALUE\n   379:     }\n   380: }\n   381: \n   382: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   383: impl Drop for OwnedHandle {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::HandleOrNull::from_raw_handle",
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
        "is_unsafe": true
      },
      "name": "from_raw_handle",
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
            "id": 5968,
            "path": "HandleOrNull"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6006",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5968",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "HandleOrNull"
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
    "verification_source": "   330:     /// Constructs a new instance of `Self` from the given `RawHandle` returned\n   331:     /// from a Windows API that uses null to indicate failure, such as\n   332:     /// `CreateThread`.\n   333:     ///\n   334:     /// Use `HandleOrInvalid` instead of `HandleOrNull` for APIs that\n   335:     /// use `INVALID_HANDLE_VALUE` to indicate failure.\n   336:     ///\n   337:     /// # Safety\n   338:     ///\n   339:     /// The passed `handle` value must either satisfy the safety requirements\n   340:     /// of [`FromRawHandle::from_raw_handle`], or be null. Note that not all\n   341:     /// Windows APIs use null for errors; see [here] for the full story.\n   342:     ///\n   343:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   344:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   345:     #[inline]\n   346:     pub unsafe fn from_raw_handle(handle: RawHandle) -> Self {\n   347:         Self(handle)\n   348:     }\n   349: \n   350:     fn is_valid(&self) -> bool {\n   351:         !self.0.is_null()\n   352:     }\n   353: }\n   354: \n   355: impl HandleOrInvalid {\n   356:     /// Constructs a new instance of `Self` from the given `RawHandle` returned\n   357:     /// from a Windows API that uses `INVALID_HANDLE_VALUE` to indicate\n   358:     /// failure, such as `CreateFileW`.\n   359:     ///\n   360:     /// Use `HandleOrNull` instead of `HandleOrInvalid` for APIs that\n   361:     /// use null to indicate failure.\n   362:     ///",
    "nanvix_source": "   336:     ///\n   337:     /// # Safety\n   338:     ///\n   339:     /// The passed `handle` value must either satisfy the safety requirements\n   340:     /// of [`FromRawHandle::from_raw_handle`], or be null. Note that not all\n   341:     /// Windows APIs use null for errors; see [here] for the full story.\n   342:     ///\n   343:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n   344:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   345:     #[inline]\n   346:     pub unsafe fn from_raw_handle(handle: RawHandle) -> Self {\n   347:         Self(handle)\n   348:     }\n   349: \n   350:     fn is_valid(&self) -> bool {\n   351:         !self.0.is_null()\n   352:     }\n   353: }\n   354: \n   355: impl HandleOrInvalid {\n   356:     /// Constructs a new instance of `Self` from the given `RawHandle` returned",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::OwnedHandle::try_clone",
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
            "id": 590,
            "path": "OwnedHandle"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:5950",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:590",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "OwnedHandle"
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
    "verification_source": "   171: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   172: impl Drop for HandleOrNull {\n   173:     #[inline]\n   174:     fn drop(&mut self) {\n   175:         if self.is_valid() {\n   176:             unsafe {\n   177:                 let _ = sys::c::CloseHandle(self.0);\n   178:             }\n   179:         }\n   180:     }\n   181: }\n   182: \n   183: impl OwnedHandle {\n   184:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   185:     /// object as the existing `OwnedHandle` instance.\n   186:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   187:     pub fn try_clone(&self) -> io::Result<Self> {\n   188:         self.as_handle().try_clone_to_owned()\n   189:     }\n   190: }\n   191: \n   192: impl BorrowedHandle<'_> {\n   193:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   194:     /// object as the existing `BorrowedHandle` instance.\n   195:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   196:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedHandle> {\n   197:         self.duplicate(0, false, sys::c::DUPLICATE_SAME_ACCESS)\n   198:     }\n   199: \n   200:     pub(crate) fn duplicate(\n   201:         &self,\n   202:         access: u32,\n   203:         inherit: bool,",
    "nanvix_source": "   177:                 let _ = sys::c::CloseHandle(self.0);\n   178:             }\n   179:         }\n   180:     }\n   181: }\n   182: \n   183: impl OwnedHandle {\n   184:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   185:     /// object as the existing `OwnedHandle` instance.\n   186:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   187:     pub fn try_clone(&self) -> io::Result<Self> {\n   188:         self.as_handle().try_clone_to_owned()\n   189:     }\n   190: }\n   191: \n   192: impl BorrowedHandle<'_> {\n   193:     /// Creates a new `OwnedHandle` instance that shares the same underlying\n   194:     /// object as the existing `BorrowedHandle` instance.\n   195:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   196:     pub fn try_clone_to_owned(&self) -> io::Result<OwnedHandle> {\n   197:         self.duplicate(0, false, sys::c::DUPLICATE_SAME_ACCESS)",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::OwnedSocket::try_clone",
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
            "id": 4774,
            "path": "OwnedSocket"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6207",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:4774",
        "resolved_owner_path": [
          "std",
          "os",
          "windows",
          "io",
          "socket",
          "OwnedSocket"
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
    "verification_source": "    57:     /// The resource pointed to by `socket` must remain open for the duration of\n    58:     /// the returned `BorrowedSocket`, and it must not have the value\n    59:     /// `INVALID_SOCKET`.\n    60:     #[inline]\n    61:     #[track_caller]\n    62:     #[rustc_const_stable(feature = \"io_safety\", since = \"1.63.0\")]\n    63:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    64:     pub const unsafe fn borrow_raw(socket: RawSocket) -> Self {\n    65:         Self { socket: ValidRawSocket::new(socket).expect(\"socket != -1\"), _phantom: PhantomData }\n    66:     }\n    67: }\n    68: \n    69: impl OwnedSocket {\n    70:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    71:     /// object as the existing `OwnedSocket` instance.\n    72:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    73:     pub fn try_clone(&self) -> io::Result<Self> {\n    74:         self.as_socket().try_clone_to_owned()\n    75:     }\n    76: \n    77:     // FIXME(strict_provenance_magic): we defined RawSocket to be a u64 ;-;\n    78:     #[allow(fuzzy_provenance_casts)]\n    79:     #[cfg(not(target_vendor = \"uwp\"))]\n    80:     pub(crate) fn set_no_inherit(&self) -> io::Result<()> {\n    81:         cvt(unsafe {\n    82:             sys::c::SetHandleInformation(\n    83:                 self.as_raw_socket() as sys::c::HANDLE,\n    84:                 sys::c::HANDLE_FLAG_INHERIT,\n    85:                 0,\n    86:             )\n    87:         })\n    88:         .map(drop)\n    89:     }",
    "nanvix_source": "    63:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    64:     pub const unsafe fn borrow_raw(socket: RawSocket) -> Self {\n    65:         Self { socket: ValidRawSocket::new(socket).expect(\"socket != -1\"), _phantom: PhantomData }\n    66:     }\n    67: }\n    68: \n    69: impl OwnedSocket {\n    70:     /// Creates a new `OwnedSocket` instance that shares the same underlying\n    71:     /// object as the existing `OwnedSocket` instance.\n    72:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n    73:     pub fn try_clone(&self) -> io::Result<Self> {\n    74:         self.as_socket().try_clone_to_owned()\n    75:     }\n    76: \n    77:     // FIXME(strict_provenance_magic): we defined RawSocket to be a u64 ;-;\n    78:     #[allow(implicit_provenance_casts)]\n    79:     #[cfg(not(target_vendor = \"uwp\"))]\n    80:     pub(crate) fn set_no_inherit(&self) -> io::Result<()> {\n    81:         cvt(unsafe {\n    82:             sys::c::SetHandleInformation(\n    83:                 self.as_raw_socket() as sys::c::HANDLE,",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Child::id",
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
      "name": "id",
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
            "id": 5654,
            "path": "Child"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7294",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5654",
        "resolved_owner_path": [
          "std",
          "process",
          "Child"
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
          "primitive": "u32"
        }
      }
    },
    "verification_source": "  2250:     ///\n  2251:     /// # Examples\n  2252:     ///\n  2253:     /// ```no_run\n  2254:     /// use std::process::Command;\n  2255:     ///\n  2256:     /// let mut command = Command::new(\"ls\");\n  2257:     /// if let Ok(child) = command.spawn() {\n  2258:     ///     println!(\"Child's ID is {}\", child.id());\n  2259:     /// } else {\n  2260:     ///     println!(\"ls command didn't start\");\n  2261:     /// }\n  2262:     /// ```\n  2263:     #[must_use]\n  2264:     #[stable(feature = \"process_id\", since = \"1.3.0\")]\n  2265:     #[cfg_attr(not(test), rustc_diagnostic_item = \"child_id\")]\n  2266:     pub fn id(&self) -> u32 {\n  2267:         self.handle.id()\n  2268:     }\n  2269: \n  2270:     /// Waits for the child to exit completely, returning the status that it\n  2271:     /// exited with. This function will continue to have the same return value\n  2272:     /// after it has been called at least once.\n  2273:     ///\n  2274:     /// The stdin handle to the child process, if any, will be closed\n  2275:     /// before waiting. This helps avoid deadlock: it ensures that the\n  2276:     /// child does not block waiting for input from the parent, while\n  2277:     /// the parent waits for the child to exit.\n  2278:     ///\n  2279:     /// # Examples\n  2280:     ///\n  2281:     /// ```no_run\n  2282:     /// use std::process::Command;",
    "nanvix_source": "  2358:     /// let mut command = Command::new(\"ls\");\n  2359:     /// if let Ok(child) = command.spawn() {\n  2360:     ///     println!(\"Child's ID is {}\", child.id());\n  2361:     /// } else {\n  2362:     ///     println!(\"ls command didn't start\");\n  2363:     /// }\n  2364:     /// ```\n  2365:     #[must_use]\n  2366:     #[stable(feature = \"process_id\", since = \"1.3.0\")]\n  2367:     #[cfg_attr(not(test), rustc_diagnostic_item = \"child_id\")]\n  2368:     pub fn id(&self) -> u32 {\n  2369:         self.handle.id()\n  2370:     }\n  2371: \n  2372:     /// Waits for the child to exit completely, returning the status that it\n  2373:     /// exited with. This function will continue to have the same return value\n  2374:     /// after it has been called at least once.\n  2375:     ///\n  2376:     /// The stdin handle to the child process, if any, will be closed\n  2377:     /// before waiting. This helps avoid deadlock: it ensures that the\n  2378:     /// child does not block waiting for input from the parent, while",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Child::kill",
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
      "name": "kill",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
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
            "id": 5654,
            "path": "Child"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7294",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5654",
        "resolved_owner_path": [
          "std",
          "process",
          "Child"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": true,
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
    "verification_source": "  2229:     ///\n  2230:     /// ```no_run\n  2231:     /// use std::process::Command;\n  2232:     ///\n  2233:     /// let mut command = Command::new(\"yes\");\n  2234:     /// if let Ok(mut child) = command.spawn() {\n  2235:     ///     child.kill().expect(\"command couldn't be killed\");\n  2236:     /// } else {\n  2237:     ///     println!(\"yes command didn't start\");\n  2238:     /// }\n  2239:     /// ```\n  2240:     ///\n  2241:     /// [`ErrorKind`]: io::ErrorKind\n  2242:     /// [`InvalidInput`]: io::ErrorKind::InvalidInput\n  2243:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2244:     #[cfg_attr(not(test), rustc_diagnostic_item = \"child_kill\")]\n  2245:     pub fn kill(&mut self) -> io::Result<()> {\n  2246:         self.handle.kill()\n  2247:     }\n  2248: \n  2249:     /// Returns the OS-assigned process identifier associated with this child.\n  2250:     ///\n  2251:     /// # Examples\n  2252:     ///\n  2253:     /// ```no_run\n  2254:     /// use std::process::Command;\n  2255:     ///\n  2256:     /// let mut command = Command::new(\"ls\");\n  2257:     /// if let Ok(child) = command.spawn() {\n  2258:     ///     println!(\"Child's ID is {}\", child.id());\n  2259:     /// } else {\n  2260:     ///     println!(\"ls command didn't start\");\n  2261:     /// }",
    "nanvix_source": "  2337:     ///     child.kill().expect(\"command couldn't be killed\");\n  2338:     /// } else {\n  2339:     ///     println!(\"yes command didn't start\");\n  2340:     /// }\n  2341:     /// ```\n  2342:     ///\n  2343:     /// [`ErrorKind`]: io::ErrorKind\n  2344:     /// [`InvalidInput`]: io::ErrorKind::InvalidInput\n  2345:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2346:     #[cfg_attr(not(test), rustc_diagnostic_item = \"child_kill\")]\n  2347:     pub fn kill(&mut self) -> io::Result<()> {\n  2348:         self.handle.kill()\n  2349:     }\n  2350: \n  2351:     /// Returns the OS-assigned process identifier associated with this child.\n  2352:     ///\n  2353:     /// # Examples\n  2354:     ///\n  2355:     /// ```no_run\n  2356:     /// use std::process::Command;\n  2357:     ///",
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
