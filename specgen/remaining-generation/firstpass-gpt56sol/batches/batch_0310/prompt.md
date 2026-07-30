For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::fs::MetadataExt::last_write_time",
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
      "name": "last_write_time",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:2882",
        "kind": "trait",
        "name": "MetadataExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "MetadataExt"
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
          "primitive": "u64"
        }
      }
    },
    "verification_source": "   484:     /// # Examples\n   485:     ///\n   486:     /// ```no_run\n   487:     /// use std::io;\n   488:     /// use std::fs;\n   489:     /// use std::os::windows::prelude::*;\n   490:     ///\n   491:     /// fn main() -> io::Result<()> {\n   492:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   493:     ///     let last_write_time = metadata.last_write_time();\n   494:     ///     Ok(())\n   495:     /// }\n   496:     /// ```\n   497:     ///\n   498:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   499:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   500:     fn last_write_time(&self) -> u64;\n   501: \n   502:     /// Returns the value of the `nFileSize` fields of this\n   503:     /// metadata.\n   504:     ///\n   505:     /// The returned value does not have meaning for directories.\n   506:     ///\n   507:     /// # Examples\n   508:     ///\n   509:     /// ```no_run\n   510:     /// use std::io;\n   511:     /// use std::fs;\n   512:     /// use std::os::windows::prelude::*;\n   513:     ///\n   514:     /// fn main() -> io::Result<()> {\n   515:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   516:     ///     let file_size = metadata.file_size();",
    "nanvix_source": "   545:     ///\n   546:     /// fn main() -> io::Result<()> {\n   547:     ///     let metadata = fs::metadata(\"foo.txt\")?;\n   548:     ///     let last_write_time = metadata.last_write_time();\n   549:     ///     Ok(())\n   550:     /// }\n   551:     /// ```\n   552:     ///\n   553:     /// [`FILETIME`]: https://docs.microsoft.com/windows/win32/api/minwinbase/ns-minwinbase-filetime\n   554:     #[stable(feature = \"metadata_ext\", since = \"1.1.0\")]\n   555:     fn last_write_time(&self) -> u64;\n   556: \n   557:     /// Returns the value of the `nFileSize` fields of this\n   558:     /// metadata.\n   559:     ///\n   560:     /// The returned value does not have meaning for directories.\n   561:     ///\n   562:     /// # Examples\n   563:     ///\n   564:     /// ```no_run\n   565:     /// use std::io;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::OpenOptionsExt::access_mode",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "access_mode",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2985",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "access",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   150:     /// the permissions to read, write and append data, attributes (like hidden\n   151:     /// and system), and extended attributes.\n   152:     ///\n   153:     /// # Examples\n   154:     ///\n   155:     /// ```no_run\n   156:     /// use std::fs::OpenOptions;\n   157:     /// use std::os::windows::prelude::*;\n   158:     ///\n   159:     /// // Open without read and write permission, for example if you only need\n   160:     /// // to call `stat` on the file\n   161:     /// let file = OpenOptions::new().access_mode(0).open(\"foo.txt\");\n   162:     /// ```\n   163:     ///\n   164:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   165:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   166:     fn access_mode(&mut self, access: u32) -> &mut Self;\n   167: \n   168:     /// Overrides the `dwShareMode` argument to the call to [`CreateFile`] with\n   169:     /// the specified value.\n   170:     ///\n   171:     /// By default `share_mode` is set to\n   172:     /// `FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE`. This allows\n   173:     /// other processes to read, write, and delete/rename the same file\n   174:     /// while it is open. Removing any of the flags will prevent other\n   175:     /// processes from performing the corresponding operation until the file\n   176:     /// handle is closed.\n   177:     ///\n   178:     /// # Examples\n   179:     ///\n   180:     /// ```no_run\n   181:     /// use std::fs::OpenOptions;\n   182:     /// use std::os::windows::prelude::*;",
    "nanvix_source": "   155:     /// use std::fs::OpenOptions;\n   156:     /// use std::os::windows::prelude::*;\n   157:     ///\n   158:     /// // Open without read and write permission, for example if you only need\n   159:     /// // to call `stat` on the file\n   160:     /// let file = OpenOptions::new().access_mode(0).open(\"foo.txt\");\n   161:     /// ```\n   162:     ///\n   163:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   164:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   165:     fn access_mode(&mut self, access: u32) -> &mut Self;\n   166: \n   167:     /// Overrides the `dwShareMode` argument to the call to [`CreateFile`] with\n   168:     /// the specified value.\n   169:     ///\n   170:     /// By default `share_mode` is set to\n   171:     /// `FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE`. This allows\n   172:     /// other processes to read, write, and delete/rename the same file\n   173:     /// while it is open. Removing any of the flags will prevent other\n   174:     /// processes from performing the corresponding operation until the file\n   175:     /// handle is closed.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::OpenOptionsExt::attributes",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "attributes",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2985",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "val",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   247:     /// extern crate winapi;\n   248:     /// # mod winapi { pub const FILE_ATTRIBUTE_HIDDEN: u32 = 2; }\n   249:     ///\n   250:     /// use std::fs::OpenOptions;\n   251:     /// use std::os::windows::prelude::*;\n   252:     ///\n   253:     /// let file = OpenOptions::new()\n   254:     ///     .write(true)\n   255:     ///     .create(true)\n   256:     ///     .attributes(winapi::FILE_ATTRIBUTE_HIDDEN)\n   257:     ///     .open(\"foo.txt\");\n   258:     /// ```\n   259:     ///\n   260:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   261:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   262:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   263:     fn attributes(&mut self, val: u32) -> &mut Self;\n   264: \n   265:     /// Sets the `dwSecurityQosFlags` argument to the call to [`CreateFile2`] to\n   266:     /// the specified value (or combines it with `custom_flags` and `attributes`\n   267:     /// to set the `dwFlagsAndAttributes` for [`CreateFile`]).\n   268:     ///\n   269:     /// By default `security_qos_flags` is not set. It should be specified when\n   270:     /// opening a named pipe, to control to which degree a server process can\n   271:     /// act on behalf of a client process (security impersonation level).\n   272:     ///\n   273:     /// When `security_qos_flags` is not set, a malicious program can gain the\n   274:     /// elevated privileges of a privileged Rust process when it allows opening\n   275:     /// user-specified paths, by tricking it into opening a named pipe. So\n   276:     /// arguably `security_qos_flags` should also be set when opening arbitrary\n   277:     /// paths. However the bits can then conflict with other flags, specifically\n   278:     /// `FILE_FLAG_OPEN_NO_RECALL`.\n   279:     ///",
    "nanvix_source": "   252:     /// let file = OpenOptions::new()\n   253:     ///     .write(true)\n   254:     ///     .create(true)\n   255:     ///     .attributes(winapi::FILE_ATTRIBUTE_HIDDEN)\n   256:     ///     .open(\"foo.txt\");\n   257:     /// ```\n   258:     ///\n   259:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   260:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   261:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   262:     fn attributes(&mut self, val: u32) -> &mut Self;\n   263: \n   264:     /// Sets the `dwSecurityQosFlags` argument to the call to [`CreateFile2`] to\n   265:     /// the specified value (or combines it with `custom_flags` and `attributes`\n   266:     /// to set the `dwFlagsAndAttributes` for [`CreateFile`]).\n   267:     ///\n   268:     /// By default `security_qos_flags` is not set. It should be specified when\n   269:     /// opening a named pipe, to control to which degree a server process can\n   270:     /// act on behalf of a client process (security impersonation level).\n   271:     ///\n   272:     /// When `security_qos_flags` is not set, a malicious program can gain the",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::OpenOptionsExt::custom_flags",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "custom_flags",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2985",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "flags",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   209:     /// extern crate winapi;\n   210:     /// # mod winapi { pub const FILE_FLAG_DELETE_ON_CLOSE: u32 = 0x04000000; }\n   211:     ///\n   212:     /// use std::fs::OpenOptions;\n   213:     /// use std::os::windows::prelude::*;\n   214:     ///\n   215:     /// let file = OpenOptions::new()\n   216:     ///     .create(true)\n   217:     ///     .write(true)\n   218:     ///     .custom_flags(winapi::FILE_FLAG_DELETE_ON_CLOSE)\n   219:     ///     .open(\"foo.txt\");\n   220:     /// ```\n   221:     ///\n   222:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   223:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   224:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   225:     fn custom_flags(&mut self, flags: u32) -> &mut Self;\n   226: \n   227:     /// Sets the `dwFileAttributes` argument to the call to [`CreateFile2`] to\n   228:     /// the specified value (or combines it with `custom_flags` and\n   229:     /// `security_qos_flags` to set the `dwFlagsAndAttributes` for\n   230:     /// [`CreateFile`]).\n   231:     ///\n   232:     /// If a _new_ file is created because it does not yet exist and\n   233:     /// `.create(true)` or `.create_new(true)` are specified, the new file is\n   234:     /// given the attributes declared with `.attributes()`.\n   235:     ///\n   236:     /// If an _existing_ file is opened with `.create(true).truncate(true)`, its\n   237:     /// existing attributes are preserved and combined with the ones declared\n   238:     /// with `.attributes()`.\n   239:     ///\n   240:     /// In all other cases the attributes get ignored.\n   241:     ///",
    "nanvix_source": "   214:     /// let file = OpenOptions::new()\n   215:     ///     .create(true)\n   216:     ///     .write(true)\n   217:     ///     .custom_flags(winapi::FILE_FLAG_DELETE_ON_CLOSE)\n   218:     ///     .open(\"foo.txt\");\n   219:     /// ```\n   220:     ///\n   221:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   222:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   223:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   224:     fn custom_flags(&mut self, flags: u32) -> &mut Self;\n   225: \n   226:     /// Sets the `dwFileAttributes` argument to the call to [`CreateFile2`] to\n   227:     /// the specified value (or combines it with `custom_flags` and\n   228:     /// `security_qos_flags` to set the `dwFlagsAndAttributes` for\n   229:     /// [`CreateFile`]).\n   230:     ///\n   231:     /// If a _new_ file is created because it does not yet exist and\n   232:     /// `.create(true)` or `.create_new(true)` are specified, the new file is\n   233:     /// given the attributes declared with `.attributes()`.\n   234:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::OpenOptionsExt::security_qos_flags",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "security_qos_flags",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2985",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "flags",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   293:     ///\n   294:     /// let file = OpenOptions::new()\n   295:     ///     .write(true)\n   296:     ///     .create(true)\n   297:     ///\n   298:     ///     // Sets the flag value to `SecurityIdentification`.\n   299:     ///     .security_qos_flags(winapi::SECURITY_IDENTIFICATION)\n   300:     ///\n   301:     ///     .open(r\"\\\\.\\pipe\\MyPipe\");\n   302:     /// ```\n   303:     ///\n   304:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   305:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   306:     /// [Impersonation Levels]:\n   307:     ///     https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level\n   308:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   309:     fn security_qos_flags(&mut self, flags: u32) -> &mut Self;\n   310: }\n   311: \n   312: #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   313: impl OpenOptionsExt for OpenOptions {\n   314:     fn access_mode(&mut self, access: u32) -> &mut OpenOptions {\n   315:         self.as_inner_mut().access_mode(access);\n   316:         self\n   317:     }\n   318: \n   319:     fn share_mode(&mut self, share: u32) -> &mut OpenOptions {\n   320:         self.as_inner_mut().share_mode(share);\n   321:         self\n   322:     }\n   323: \n   324:     fn custom_flags(&mut self, flags: u32) -> &mut OpenOptions {\n   325:         self.as_inner_mut().custom_flags(flags);",
    "nanvix_source": "   298:     ///     .security_qos_flags(winapi::SECURITY_IDENTIFICATION)\n   299:     ///\n   300:     ///     .open(r\"\\\\.\\pipe\\MyPipe\");\n   301:     /// ```\n   302:     ///\n   303:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   304:     /// [`CreateFile2`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfile2\n   305:     /// [Impersonation Levels]:\n   306:     ///     https://docs.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-security_impersonation_level\n   307:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   308:     fn security_qos_flags(&mut self, flags: u32) -> &mut Self;\n   309: }\n   310: \n   311: #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   312: impl OpenOptionsExt for OpenOptions {\n   313:     fn access_mode(&mut self, access: u32) -> &mut OpenOptions {\n   314:         self.as_inner_mut().access_mode(access);\n   315:         self\n   316:     }\n   317: \n   318:     fn share_mode(&mut self, share: u32) -> &mut OpenOptions {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::fs::OpenOptionsExt::share_mode",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "share_mode",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "std:2985",
        "kind": "trait",
        "name": "OpenOptionsExt",
        "path": [
          "std",
          "os",
          "windows",
          "fs",
          "OpenOptionsExt"
        ]
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
          ],
          [
            "val",
            {
              "primitive": "u32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Self"
            }
          }
        }
      }
    },
    "verification_source": "   178:     /// # Examples\n   179:     ///\n   180:     /// ```no_run\n   181:     /// use std::fs::OpenOptions;\n   182:     /// use std::os::windows::prelude::*;\n   183:     ///\n   184:     /// // Do not allow others to read or modify this file while we have it open\n   185:     /// // for writing.\n   186:     /// let file = OpenOptions::new()\n   187:     ///     .write(true)\n   188:     ///     .share_mode(0)\n   189:     ///     .open(\"foo.txt\");\n   190:     /// ```\n   191:     ///\n   192:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   193:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   194:     fn share_mode(&mut self, val: u32) -> &mut Self;\n   195: \n   196:     /// Sets extra flags for the `dwFileFlags` argument to the call to\n   197:     /// [`CreateFile2`] to the specified value (or combines it with\n   198:     /// `attributes` and `security_qos_flags` to set the `dwFlagsAndAttributes`\n   199:     /// for [`CreateFile`]).\n   200:     ///\n   201:     /// Custom flags can only set flags, not remove flags set by Rust's options.\n   202:     /// This option overwrites any previously set custom flags.\n   203:     ///\n   204:     /// # Examples\n   205:     ///\n   206:     /// ```no_run\n   207:     /// # #![allow(unexpected_cfgs)]\n   208:     /// # #[cfg(for_demonstration_only)]\n   209:     /// extern crate winapi;\n   210:     /// # mod winapi { pub const FILE_FLAG_DELETE_ON_CLOSE: u32 = 0x04000000; }",
    "nanvix_source": "   183:     /// // Do not allow others to read or modify this file while we have it open\n   184:     /// // for writing.\n   185:     /// let file = OpenOptions::new()\n   186:     ///     .write(true)\n   187:     ///     .share_mode(0)\n   188:     ///     .open(\"foo.txt\");\n   189:     /// ```\n   190:     ///\n   191:     /// [`CreateFile`]: https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea\n   192:     #[stable(feature = \"open_options_ext\", since = \"1.10.0\")]\n   193:     fn share_mode(&mut self, val: u32) -> &mut Self;\n   194: \n   195:     /// Sets extra flags for the `dwFileFlags` argument to the call to\n   196:     /// [`CreateFile2`] to the specified value (or combines it with\n   197:     /// `attributes` and `security_qos_flags` to set the `dwFlagsAndAttributes`\n   198:     /// for [`CreateFile`]).\n   199:     ///\n   200:     /// Custom flags can only set flags, not remove flags set by Rust's options.\n   201:     /// This option overwrites any previously set custom flags.\n   202:     ///\n   203:     /// # Examples",
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
