For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::fs::File::set_modified",
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
      "name": "set_modified",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
            "time",
            {
              "resolved_path": {
                "args": null,
                "id": 2591,
                "path": "SystemTime"
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
    "verification_source": "  1261:     ///     Ok(())\n  1262:     /// }\n  1263:     /// ```\n  1264:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1265:     #[doc(alias = \"futimens\")]\n  1266:     #[doc(alias = \"futimes\")]\n  1267:     #[doc(alias = \"SetFileTime\")]\n  1268:     pub fn set_times(&self, times: FileTimes) -> io::Result<()> {\n  1269:         self.inner.set_times(times.0)\n  1270:     }\n  1271: \n  1272:     /// Changes the modification time of the underlying file.\n  1273:     ///\n  1274:     /// This is an alias for `set_times(FileTimes::new().set_modified(time))`.\n  1275:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1276:     #[inline]\n  1277:     pub fn set_modified(&self, time: SystemTime) -> io::Result<()> {\n  1278:         self.set_times(FileTimes::new().set_modified(time))\n  1279:     }\n  1280: }\n  1281: \n  1282: // In addition to the `impl`s here, `File` also has `impl`s for\n  1283: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n  1284: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n  1285: // `AsHandle`/`From<OwnedHandle>`/`Into<OwnedHandle>` and\n  1286: // `AsRawHandle`/`IntoRawHandle`/`FromRawHandle` on Windows.\n  1287: \n  1288: impl AsInner<fs_imp::File> for File {\n  1289:     #[inline]\n  1290:     fn as_inner(&self) -> &fs_imp::File {\n  1291:         &self.inner\n  1292:     }\n  1293: }",
    "nanvix_source": "  1266:     #[doc(alias = \"filetime\")]\n  1267:     pub fn set_times(&self, times: FileTimes) -> io::Result<()> {\n  1268:         self.inner.set_times(times.0)\n  1269:     }\n  1270: \n  1271:     /// Changes the modification time of the underlying file.\n  1272:     ///\n  1273:     /// This is an alias for `set_times(FileTimes::new().set_modified(time))`.\n  1274:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1275:     #[inline]\n  1276:     pub fn set_modified(&self, time: SystemTime) -> io::Result<()> {\n  1277:         self.set_times(FileTimes::new().set_modified(time))\n  1278:     }\n  1279: }\n  1280: \n  1281: // In addition to the `impl`s here, `File` also has `impl`s for\n  1282: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n  1283: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and\n  1284: // `AsHandle`/`From<OwnedHandle>`/`Into<OwnedHandle>` and\n  1285: // `AsRawHandle`/`IntoRawHandle`/`FromRawHandle` on Windows.\n  1286: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::set_permissions",
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
      "name": "set_permissions",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
            "perm",
            {
              "resolved_path": {
                "args": null,
                "id": 2587,
                "path": "Permissions"
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
    "verification_source": "  1206:     /// ```no_run\n  1207:     /// fn main() -> std::io::Result<()> {\n  1208:     ///     use std::fs::File;\n  1209:     ///\n  1210:     ///     let file = File::open(\"foo.txt\")?;\n  1211:     ///     let mut perms = file.metadata()?.permissions();\n  1212:     ///     perms.set_readonly(true);\n  1213:     ///     file.set_permissions(perms)?;\n  1214:     ///     Ok(())\n  1215:     /// }\n  1216:     /// ```\n  1217:     ///\n  1218:     /// Note that this method alters the permissions of the underlying file,\n  1219:     /// even though it takes `&self` rather than `&mut self`.\n  1220:     #[doc(alias = \"fchmod\", alias = \"SetFileInformationByHandle\")]\n  1221:     #[stable(feature = \"set_permissions_atomic\", since = \"1.16.0\")]\n  1222:     pub fn set_permissions(&self, perm: Permissions) -> io::Result<()> {\n  1223:         self.inner.set_permissions(perm.0)\n  1224:     }\n  1225: \n  1226:     /// Changes the timestamps of the underlying file.\n  1227:     ///\n  1228:     /// # Platform-specific behavior\n  1229:     ///\n  1230:     /// This function currently corresponds to the `futimens` function on Unix (falling back to\n  1231:     /// `futimes` on macOS before 10.13) and the `SetFileTime` function on Windows. Note that this\n  1232:     /// [may change in the future][changes].\n  1233:     ///\n  1234:     /// On most platforms, including UNIX and Windows platforms, this function can also change the\n  1235:     /// timestamps of a directory. To get a `File` representing a directory in order to call\n  1236:     /// `set_times`, open the directory with `File::open` without attempting to obtain write\n  1237:     /// permission.\n  1238:     ///",
    "nanvix_source": "  1210:     ///     perms.set_readonly(true);\n  1211:     ///     file.set_permissions(perms)?;\n  1212:     ///     Ok(())\n  1213:     /// }\n  1214:     /// ```\n  1215:     ///\n  1216:     /// Note that this method alters the permissions of the underlying file,\n  1217:     /// even though it takes `&self` rather than `&mut self`.\n  1218:     #[doc(alias = \"fchmod\", alias = \"SetFileInformationByHandle\")]\n  1219:     #[stable(feature = \"set_permissions_atomic\", since = \"1.16.0\")]\n  1220:     pub fn set_permissions(&self, perm: Permissions) -> io::Result<()> {\n  1221:         self.inner.set_permissions(perm.0)\n  1222:     }\n  1223: \n  1224:     /// Changes the timestamps of the underlying file.\n  1225:     ///\n  1226:     /// # Platform-specific behavior\n  1227:     ///\n  1228:     /// This function currently corresponds to the `futimens` function on Unix (falling back to\n  1229:     /// `futimes` on macOS before 10.13) and the `SetFileTime` function on Windows. Note that this\n  1230:     /// [may change in the future][changes].",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::set_times",
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
      "name": "set_times",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
            "times",
            {
              "resolved_path": {
                "args": null,
                "id": 2589,
                "path": "FileTimes"
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
    "verification_source": "  1252:     /// fn main() -> std::io::Result<()> {\n  1253:     ///     use std::fs::{self, File, FileTimes};\n  1254:     ///\n  1255:     ///     let src = fs::metadata(\"src\")?;\n  1256:     ///     let dest = File::open(\"dest\")?;\n  1257:     ///     let times = FileTimes::new()\n  1258:     ///         .set_accessed(src.accessed()?)\n  1259:     ///         .set_modified(src.modified()?);\n  1260:     ///     dest.set_times(times)?;\n  1261:     ///     Ok(())\n  1262:     /// }\n  1263:     /// ```\n  1264:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1265:     #[doc(alias = \"futimens\")]\n  1266:     #[doc(alias = \"futimes\")]\n  1267:     #[doc(alias = \"SetFileTime\")]\n  1268:     pub fn set_times(&self, times: FileTimes) -> io::Result<()> {\n  1269:         self.inner.set_times(times.0)\n  1270:     }\n  1271: \n  1272:     /// Changes the modification time of the underlying file.\n  1273:     ///\n  1274:     /// This is an alias for `set_times(FileTimes::new().set_modified(time))`.\n  1275:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1276:     #[inline]\n  1277:     pub fn set_modified(&self, time: SystemTime) -> io::Result<()> {\n  1278:         self.set_times(FileTimes::new().set_modified(time))\n  1279:     }\n  1280: }\n  1281: \n  1282: // In addition to the `impl`s here, `File` also has `impl`s for\n  1283: // `AsFd`/`From<OwnedFd>`/`Into<OwnedFd>` and\n  1284: // `AsRawFd`/`IntoRawFd`/`FromRawFd`, on Unix and WASI, and",
    "nanvix_source": "  1257:     ///         .set_modified(src.modified()?);\n  1258:     ///     dest.set_times(times)?;\n  1259:     ///     Ok(())\n  1260:     /// }\n  1261:     /// ```\n  1262:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1263:     #[doc(alias = \"futimens\")]\n  1264:     #[doc(alias = \"futimes\")]\n  1265:     #[doc(alias = \"SetFileTime\")]\n  1266:     #[doc(alias = \"filetime\")]\n  1267:     pub fn set_times(&self, times: FileTimes) -> io::Result<()> {\n  1268:         self.inner.set_times(times.0)\n  1269:     }\n  1270: \n  1271:     /// Changes the modification time of the underlying file.\n  1272:     ///\n  1273:     /// This is an alias for `set_times(FileTimes::new().set_modified(time))`.\n  1274:     #[stable(feature = \"file_set_times\", since = \"1.75.0\")]\n  1275:     #[inline]\n  1276:     pub fn set_modified(&self, time: SystemTime) -> io::Result<()> {\n  1277:         self.set_times(FileTimes::new().set_modified(time))",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::sync_all",
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
      "name": "sync_all",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
    "verification_source": "   764:     /// # Examples\n   765:     ///\n   766:     /// ```no_run\n   767:     /// use std::fs::File;\n   768:     /// use std::io::prelude::*;\n   769:     ///\n   770:     /// fn main() -> std::io::Result<()> {\n   771:     ///     let mut f = File::create(\"foo.txt\")?;\n   772:     ///     f.write_all(b\"Hello, world!\")?;\n   773:     ///\n   774:     ///     f.sync_all()?;\n   775:     ///     Ok(())\n   776:     /// }\n   777:     /// ```\n   778:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   779:     #[doc(alias = \"fsync\")]\n   780:     pub fn sync_all(&self) -> io::Result<()> {\n   781:         self.inner.fsync()\n   782:     }\n   783: \n   784:     /// This function is similar to [`sync_all`], except that it might not\n   785:     /// synchronize file metadata to the filesystem.\n   786:     ///\n   787:     /// This is intended for use cases that must synchronize content, but don't\n   788:     /// need the metadata on disk. The goal of this method is to reduce disk\n   789:     /// operations.\n   790:     ///\n   791:     /// Note that some platforms may simply implement this in terms of\n   792:     /// [`sync_all`].\n   793:     ///\n   794:     /// [`sync_all`]: File::sync_all\n   795:     ///\n   796:     /// # Examples",
    "nanvix_source": "   769:     /// fn main() -> std::io::Result<()> {\n   770:     ///     let mut f = File::create(\"foo.txt\")?;\n   771:     ///     f.write_all(b\"Hello, world!\")?;\n   772:     ///\n   773:     ///     f.sync_all()?;\n   774:     ///     Ok(())\n   775:     /// }\n   776:     /// ```\n   777:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   778:     #[doc(alias = \"fsync\")]\n   779:     pub fn sync_all(&self) -> io::Result<()> {\n   780:         self.inner.fsync()\n   781:     }\n   782: \n   783:     /// This function is similar to [`sync_all`], except that it might not\n   784:     /// synchronize file metadata to the filesystem.\n   785:     ///\n   786:     /// This is intended for use cases that must synchronize content, but don't\n   787:     /// need the metadata on disk. The goal of this method is to reduce disk\n   788:     /// operations.\n   789:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::sync_data",
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
      "name": "sync_data",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
    "verification_source": "   796:     /// # Examples\n   797:     ///\n   798:     /// ```no_run\n   799:     /// use std::fs::File;\n   800:     /// use std::io::prelude::*;\n   801:     ///\n   802:     /// fn main() -> std::io::Result<()> {\n   803:     ///     let mut f = File::create(\"foo.txt\")?;\n   804:     ///     f.write_all(b\"Hello, world!\")?;\n   805:     ///\n   806:     ///     f.sync_data()?;\n   807:     ///     Ok(())\n   808:     /// }\n   809:     /// ```\n   810:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   811:     #[doc(alias = \"fdatasync\")]\n   812:     pub fn sync_data(&self) -> io::Result<()> {\n   813:         self.inner.datasync()\n   814:     }\n   815: \n   816:     /// Acquire an exclusive lock on the file. Blocks until the lock can be acquired.\n   817:     ///\n   818:     /// This acquires an exclusive lock; no other file handle to this file, in this or any other\n   819:     /// process, may acquire another lock.\n   820:     ///\n   821:     /// This lock may be advisory or mandatory. This lock is meant to interact with [`lock`],\n   822:     /// [`try_lock`], [`lock_shared`], [`try_lock_shared`], and [`unlock`]. Its interactions with\n   823:     /// other methods, such as [`read`] and [`write`] are platform specific, and it may or may not\n   824:     /// cause non-lockholders to block.\n   825:     ///\n   826:     /// If this file handle/descriptor, or a clone of it, already holds a lock the exact behavior\n   827:     /// is unspecified and platform dependent, including the possibility that it will deadlock.\n   828:     /// However, if this method returns, then an exclusive lock is held.",
    "nanvix_source": "   801:     /// fn main() -> std::io::Result<()> {\n   802:     ///     let mut f = File::create(\"foo.txt\")?;\n   803:     ///     f.write_all(b\"Hello, world!\")?;\n   804:     ///\n   805:     ///     f.sync_data()?;\n   806:     ///     Ok(())\n   807:     /// }\n   808:     /// ```\n   809:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   810:     #[doc(alias = \"fdatasync\")]\n   811:     pub fn sync_data(&self) -> io::Result<()> {\n   812:         self.inner.datasync()\n   813:     }\n   814: \n   815:     /// Acquire an exclusive lock on the file. Blocks until the lock can be acquired.\n   816:     ///\n   817:     /// This acquires an exclusive lock. No *other* file handle to this file, in this or any other\n   818:     /// process, may acquire another lock.\n   819:     /// If this file handle/descriptor, or a clone of it, already holds a lock, the exact behavior\n   820:     /// is unspecified and platform dependent, including the possibility that it will deadlock.\n   821:     /// However, if this method returns, then an exclusive lock is held.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::fs::File::try_clone",
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
            "id": 2556,
            "path": "File"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2592",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2556",
        "resolved_owner_path": [
          "std",
          "fs",
          "File"
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
                        "id": 2556,
                        "path": "File"
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
    "verification_source": "  1168:     /// use std::io::SeekFrom;\n  1169:     /// use std::io::prelude::*;\n  1170:     ///\n  1171:     /// fn main() -> std::io::Result<()> {\n  1172:     ///     let mut file = File::open(\"foo.txt\")?;\n  1173:     ///     let mut file_copy = file.try_clone()?;\n  1174:     ///\n  1175:     ///     file.seek(SeekFrom::Start(3))?;\n  1176:     ///\n  1177:     ///     let mut contents = vec![];\n  1178:     ///     file_copy.read_to_end(&mut contents)?;\n  1179:     ///     assert_eq!(contents, b\"def\\n\");\n  1180:     ///     Ok(())\n  1181:     /// }\n  1182:     /// ```\n  1183:     #[stable(feature = \"file_try_clone\", since = \"1.9.0\")]\n  1184:     pub fn try_clone(&self) -> io::Result<File> {\n  1185:         Ok(File { inner: self.inner.duplicate()? })\n  1186:     }\n  1187: \n  1188:     /// Changes the permissions on the underlying file.\n  1189:     ///\n  1190:     /// # Platform-specific behavior\n  1191:     ///\n  1192:     /// This function currently corresponds to the `fchmod` function on Unix and\n  1193:     /// the `SetFileInformationByHandle` function on Windows. Note that, this\n  1194:     /// [may change in the future][changes].\n  1195:     ///\n  1196:     /// [changes]: io#platform-specific-behavior\n  1197:     ///\n  1198:     /// # Errors\n  1199:     ///\n  1200:     /// This function will return an error if the user lacks permission change",
    "nanvix_source": "  1172:     ///\n  1173:     ///     file.seek(SeekFrom::Start(3))?;\n  1174:     ///\n  1175:     ///     let mut contents = vec![];\n  1176:     ///     file_copy.read_to_end(&mut contents)?;\n  1177:     ///     assert_eq!(contents, b\"def\\n\");\n  1178:     ///     Ok(())\n  1179:     /// }\n  1180:     /// ```\n  1181:     #[stable(feature = \"file_try_clone\", since = \"1.9.0\")]\n  1182:     pub fn try_clone(&self) -> io::Result<File> {\n  1183:         Ok(File { inner: self.inner.duplicate()? })\n  1184:     }\n  1185: \n  1186:     /// Changes the permissions on the underlying file.\n  1187:     ///\n  1188:     /// # Platform-specific behavior\n  1189:     ///\n  1190:     /// This function currently corresponds to the `fchmod` function on Unix and\n  1191:     /// the `SetFileInformationByHandle` function on Windows. Note that, this\n  1192:     /// [may change in the future][changes].",
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
