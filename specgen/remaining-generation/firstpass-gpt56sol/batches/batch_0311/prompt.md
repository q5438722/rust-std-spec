For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::io::AsHandle::as_handle",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "as_handle",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:588",
        "kind": "trait",
        "name": "AsHandle",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "handle",
          "AsHandle"
        ]
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
            "id": 586,
            "path": "BorrowedHandle"
          }
        }
      }
    },
    "verification_source": "   424: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   425: pub trait AsHandle {\n   426:     /// Borrows the handle.\n   427:     ///\n   428:     /// # Example\n   429:     ///\n   430:     /// ```rust,no_run\n   431:     /// use std::fs::File;\n   432:     /// # use std::io;\n   433:     /// use std::os::windows::io::{AsHandle, BorrowedHandle};\n   434:     ///\n   435:     /// let mut f = File::open(\"foo.txt\")?;\n   436:     /// let borrowed_handle: BorrowedHandle<'_> = f.as_handle();\n   437:     /// # Ok::<(), io::Error>(())\n   438:     /// ```\n   439:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   440:     fn as_handle(&self) -> BorrowedHandle<'_>;\n   441: }\n   442: \n   443: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   444: impl<T: AsHandle + ?Sized> AsHandle for &T {\n   445:     #[inline]\n   446:     fn as_handle(&self) -> BorrowedHandle<'_> {\n   447:         T::as_handle(self)\n   448:     }\n   449: }\n   450: \n   451: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   452: impl<T: AsHandle + ?Sized> AsHandle for &mut T {\n   453:     #[inline]\n   454:     fn as_handle(&self) -> BorrowedHandle<'_> {\n   455:         T::as_handle(self)\n   456:     }",
    "nanvix_source": "   427:     /// ```rust,no_run\n   428:     /// use std::fs::File;\n   429:     /// # use std::io;\n   430:     /// use std::os::windows::io::{AsHandle, BorrowedHandle};\n   431:     ///\n   432:     /// let mut f = File::open(\"foo.txt\")?;\n   433:     /// let borrowed_handle: BorrowedHandle<'_> = f.as_handle();\n   434:     /// # Ok::<(), io::Error>(())\n   435:     /// ```\n   436:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   437:     fn as_handle(&self) -> BorrowedHandle<'_>;\n   438: }\n   439: \n   440: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   441: impl<T: AsHandle + ?Sized> AsHandle for &T {\n   442:     #[inline]\n   443:     fn as_handle(&self) -> BorrowedHandle<'_> {\n   444:         T::as_handle(self)\n   445:     }\n   446: }\n   447: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::AsRawHandle::as_raw_handle",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "as_raw_handle",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:595",
        "kind": "trait",
        "name": "AsRawHandle",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "AsRawHandle"
        ]
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
            "args": null,
            "id": 593,
            "path": "RawHandle"
          }
        }
      }
    },
    "verification_source": "    27:     /// raw handle to the caller, and the handle is only guaranteed\n    28:     /// to be valid while the original object has not yet been destroyed.\n    29:     ///\n    30:     /// This function may return null, such as when called on [`Stdin`],\n    31:     /// [`Stdout`], or [`Stderr`] when the console is detached.\n    32:     ///\n    33:     /// However, borrowing is not strictly required. See [`AsHandle::as_handle`]\n    34:     /// for an API which strictly borrows a handle.\n    35:     ///\n    36:     /// [`Stdin`]: io::Stdin\n    37:     /// [`Stdout`]: io::Stdout\n    38:     /// [`Stderr`]: io::Stderr\n    39:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    40:     fn as_raw_handle(&self) -> RawHandle;\n    41: }\n    42: \n    43: /// Constructs I/O objects from raw handles.\n    44: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    45: pub trait FromRawHandle {\n    46:     /// Constructs a new I/O object from the specified raw handle.\n    47:     ///\n    48:     /// This function is typically used to **consume ownership** of the handle\n    49:     /// given, passing responsibility for closing the handle to the returned\n    50:     /// object. When used in this way, the returned object\n    51:     /// will take responsibility for closing it when the object goes out of\n    52:     /// scope.\n    53:     ///\n    54:     /// However, consuming ownership is not strictly required. Use a\n    55:     /// `From<OwnedHandle>::from` implementation for an API which strictly\n    56:     /// consumes ownership.\n    57:     ///\n    58:     /// # Safety\n    59:     ///",
    "nanvix_source": "    33:     /// However, borrowing is not strictly required. See [`AsHandle::as_handle`]\n    34:     /// for an API which strictly borrows a handle.\n    35:     ///\n    36:     /// [`Stdin`]: io::Stdin\n    37:     /// [`Stdout`]: io::Stdout\n    38:     /// [`Stderr`]: io::Stderr\n    39:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    40:     fn as_raw_handle(&self) -> RawHandle;\n    41: }\n    42: \n    43: /// Constructs I/O objects from raw handles.\n    44: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    45: pub trait FromRawHandle {\n    46:     /// Constructs a new I/O object from the specified raw handle.\n    47:     ///\n    48:     /// This function is typically used to **consume ownership** of the handle\n    49:     /// given, passing responsibility for closing the handle to the returned\n    50:     /// object. When used in this way, the returned object\n    51:     /// will take responsibility for closing it when the object goes out of\n    52:     /// scope.\n    53:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::AsRawSocket::as_raw_socket",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "as_raw_socket",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:4762",
        "kind": "trait",
        "name": "AsRawSocket",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "AsRawSocket"
        ]
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
            "args": null,
            "id": 4760,
            "path": "RawSocket"
          }
        }
      }
    },
    "verification_source": "   173:     }\n   174: }\n   175: \n   176: /// Extracts raw sockets.\n   177: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   178: pub trait AsRawSocket {\n   179:     /// Extracts the raw socket.\n   180:     ///\n   181:     /// This function is typically used to **borrow** an owned socket.\n   182:     /// When used in this way, this method does **not** pass ownership of the\n   183:     /// raw socket to the caller, and the socket is only guaranteed\n   184:     /// to be valid while the original object has not yet been destroyed.\n   185:     ///\n   186:     /// However, borrowing is not strictly required. See [`AsSocket::as_socket`]\n   187:     /// for an API which strictly borrows a socket.\n   188:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   189:     fn as_raw_socket(&self) -> RawSocket;\n   190: }\n   191: \n   192: /// Creates I/O objects from raw sockets.\n   193: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   194: pub trait FromRawSocket {\n   195:     /// Constructs a new I/O object from the specified raw socket.\n   196:     ///\n   197:     /// This function is typically used to **consume ownership** of the socket\n   198:     /// given, passing responsibility for closing the socket to the returned\n   199:     /// object. When used in this way, the returned object\n   200:     /// will take responsibility for closing it when the object goes out of\n   201:     /// scope.\n   202:     ///\n   203:     /// However, consuming ownership is not strictly required. Use a\n   204:     /// `From<OwnedSocket>::from` implementation for an API which strictly\n   205:     /// consumes ownership.",
    "nanvix_source": "   179:     /// Extracts the raw socket.\n   180:     ///\n   181:     /// This function is typically used to **borrow** an owned socket.\n   182:     /// When used in this way, this method does **not** pass ownership of the\n   183:     /// raw socket to the caller, and the socket is only guaranteed\n   184:     /// to be valid while the original object has not yet been destroyed.\n   185:     ///\n   186:     /// However, borrowing is not strictly required. See [`AsSocket::as_socket`]\n   187:     /// for an API which strictly borrows a socket.\n   188:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   189:     fn as_raw_socket(&self) -> RawSocket;\n   190: }\n   191: \n   192: /// Creates I/O objects from raw sockets.\n   193: #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   194: pub trait FromRawSocket {\n   195:     /// Constructs a new I/O object from the specified raw socket.\n   196:     ///\n   197:     /// This function is typically used to **consume ownership** of the socket\n   198:     /// given, passing responsibility for closing the socket to the returned\n   199:     /// object. When used in this way, the returned object",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::AsSocket::as_socket",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "as_socket",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:4772",
        "kind": "trait",
        "name": "AsSocket",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "socket",
          "AsSocket"
        ]
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
            "id": 4770,
            "path": "BorrowedSocket"
          }
        }
      }
    },
    "verification_source": "   206:         f.debug_struct(\"BorrowedSocket\").field(\"socket\", &self.socket).finish()\n   207:     }\n   208: }\n   209: \n   210: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   211: impl fmt::Debug for OwnedSocket {\n   212:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   213:         f.debug_struct(\"OwnedSocket\").field(\"socket\", &self.socket).finish()\n   214:     }\n   215: }\n   216: \n   217: /// A trait to borrow the socket from an underlying object.\n   218: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   219: pub trait AsSocket {\n   220:     /// Borrows the socket.\n   221:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   222:     fn as_socket(&self) -> BorrowedSocket<'_>;\n   223: }\n   224: \n   225: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   226: impl<T: AsSocket> AsSocket for &T {\n   227:     #[inline]\n   228:     fn as_socket(&self) -> BorrowedSocket<'_> {\n   229:         T::as_socket(self)\n   230:     }\n   231: }\n   232: \n   233: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   234: impl<T: AsSocket> AsSocket for &mut T {\n   235:     #[inline]\n   236:     fn as_socket(&self) -> BorrowedSocket<'_> {\n   237:         T::as_socket(self)\n   238:     }",
    "nanvix_source": "   212:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   213:         f.debug_struct(\"OwnedSocket\").field(\"socket\", &self.socket).finish()\n   214:     }\n   215: }\n   216: \n   217: /// A trait to borrow the socket from an underlying object.\n   218: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   219: pub trait AsSocket {\n   220:     /// Borrows the socket.\n   221:     #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   222:     fn as_socket(&self) -> BorrowedSocket<'_>;\n   223: }\n   224: \n   225: #[stable(feature = \"io_safety\", since = \"1.63.0\")]\n   226: impl<T: AsSocket> AsSocket for &T {\n   227:     #[inline]\n   228:     fn as_socket(&self) -> BorrowedSocket<'_> {\n   229:         T::as_socket(self)\n   230:     }\n   231: }\n   232: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::FromRawHandle::from_raw_handle",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
        "item_id": "std:2684",
        "kind": "trait",
        "name": "FromRawHandle",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "FromRawHandle"
        ]
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
    "verification_source": "    56:     /// consumes ownership.\n    57:     ///\n    58:     /// # Safety\n    59:     ///\n    60:     /// The `handle` passed in must:\n    61:     ///   - be an [owned handle][io-safety]; in particular, it must be open.\n    62:     ///   - be a handle for a resource that may be freed via [`CloseHandle`]\n    63:     ///     (as opposed to `RegCloseKey` or other close functions).\n    64:     ///\n    65:     /// Note that the handle *may* have the value `INVALID_HANDLE_VALUE` (-1),\n    66:     /// which is sometimes a valid handle value. See [here] for the full story.\n    67:     ///\n    68:     /// [`CloseHandle`]: https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle\n    69:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n    70:     /// [io-safety]: io#io-safety\n    71:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    72:     unsafe fn from_raw_handle(handle: RawHandle) -> Self;\n    73: }\n    74: \n    75: /// A trait to express the ability to consume an object and acquire ownership of\n    76: /// its raw `HANDLE`.\n    77: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n    78: pub trait IntoRawHandle {\n    79:     /// Consumes this object, returning the raw underlying handle.\n    80:     ///\n    81:     /// This function is typically used to **transfer ownership** of the underlying\n    82:     /// handle to the caller. When used in this way, callers are then the unique\n    83:     /// owners of the handle and must close it once it's no longer needed.\n    84:     ///\n    85:     /// However, transferring ownership is not strictly required. Use a\n    86:     /// `Into<OwnedHandle>::into` implementation for an API which strictly\n    87:     /// transfers ownership.\n    88:     #[must_use = \"losing the raw handle may leak resources\"]",
    "nanvix_source": "    62:     ///   - be a handle for a resource that may be freed via [`CloseHandle`]\n    63:     ///     (as opposed to `RegCloseKey` or other close functions).\n    64:     ///\n    65:     /// Note that the handle *may* have the value `INVALID_HANDLE_VALUE` (-1),\n    66:     /// which is sometimes a valid handle value. See [here] for the full story.\n    67:     ///\n    68:     /// [`CloseHandle`]: https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle\n    69:     /// [here]: https://devblogs.microsoft.com/oldnewthing/20040302-00/?p=40443\n    70:     /// [io-safety]: io#io-safety\n    71:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n    72:     unsafe fn from_raw_handle(handle: RawHandle) -> Self;\n    73: }\n    74: \n    75: /// A trait to express the ability to consume an object and acquire ownership of\n    76: /// its raw `HANDLE`.\n    77: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n    78: pub trait IntoRawHandle {\n    79:     /// Consumes this object, returning the raw underlying handle.\n    80:     ///\n    81:     /// This function is typically used to **transfer ownership** of the underlying\n    82:     /// handle to the caller. When used in this way, callers are then the unique",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::FromRawSocket::from_raw_socket",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "from_raw_socket",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:4765",
        "kind": "trait",
        "name": "FromRawSocket",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "FromRawSocket"
        ]
      },
      "signature": {
        "inputs": [
          [
            "sock",
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
    "verification_source": "   200:     /// will take responsibility for closing it when the object goes out of\n   201:     /// scope.\n   202:     ///\n   203:     /// However, consuming ownership is not strictly required. Use a\n   204:     /// `From<OwnedSocket>::from` implementation for an API which strictly\n   205:     /// consumes ownership.\n   206:     ///\n   207:     /// # Safety\n   208:     ///\n   209:     /// The `socket` passed in must:\n   210:     ///   - be an [owned socket][io-safety]; in particular, it must be open.\n   211:     ///   - be a socket that may be freed via [`closesocket`].\n   212:     ///\n   213:     /// [`closesocket`]: https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-closesocket\n   214:     /// [io-safety]: io#io-safety\n   215:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   216:     unsafe fn from_raw_socket(sock: RawSocket) -> Self;\n   217: }\n   218: \n   219: /// A trait to express the ability to consume an object and acquire ownership of\n   220: /// its raw `SOCKET`.\n   221: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   222: pub trait IntoRawSocket {\n   223:     /// Consumes this object, returning the raw underlying socket.\n   224:     ///\n   225:     /// This function is typically used to **transfer ownership** of the underlying\n   226:     /// socket to the caller. When used in this way, callers are then the unique\n   227:     /// owners of the socket and must close it once it's no longer needed.\n   228:     ///\n   229:     /// However, transferring ownership is not strictly required. Use a\n   230:     /// `Into<OwnedSocket>::into` implementation for an API which strictly\n   231:     /// transfers ownership.\n   232:     #[must_use = \"losing the raw socket may leak resources\"]",
    "nanvix_source": "   206:     ///\n   207:     /// # Safety\n   208:     ///\n   209:     /// The `socket` passed in must:\n   210:     ///   - be an [owned socket][io-safety]; in particular, it must be open.\n   211:     ///   - be a socket that may be freed via [`closesocket`].\n   212:     ///\n   213:     /// [`closesocket`]: https://docs.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-closesocket\n   214:     /// [io-safety]: io#io-safety\n   215:     #[stable(feature = \"from_raw_os\", since = \"1.1.0\")]\n   216:     unsafe fn from_raw_socket(sock: RawSocket) -> Self;\n   217: }\n   218: \n   219: /// A trait to express the ability to consume an object and acquire ownership of\n   220: /// its raw `SOCKET`.\n   221: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   222: pub trait IntoRawSocket {\n   223:     /// Consumes this object, returning the raw underlying socket.\n   224:     ///\n   225:     /// This function is typically used to **transfer ownership** of the underlying\n   226:     /// socket to the caller. When used in this way, callers are then the unique",
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
