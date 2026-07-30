For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::process::Command::get_envs",
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
      "name": "get_envs",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
            "id": 7385,
            "path": "CommandEnvs"
          }
        }
      }
    },
    "verification_source": "  1168:     ///\n  1169:     /// # Examples\n  1170:     ///\n  1171:     /// ```\n  1172:     /// use std::ffi::OsStr;\n  1173:     /// use std::process::Command;\n  1174:     ///\n  1175:     /// let mut cmd = Command::new(\"ls\");\n  1176:     /// cmd.env(\"TERM\", \"dumb\").env_remove(\"TZ\");\n  1177:     /// let envs: Vec<(&OsStr, Option<&OsStr>)> = cmd.get_envs().collect();\n  1178:     /// assert_eq!(envs, &[\n  1179:     ///     (OsStr::new(\"TERM\"), Some(OsStr::new(\"dumb\"))),\n  1180:     ///     (OsStr::new(\"TZ\"), None)\n  1181:     /// ]);\n  1182:     /// ```\n  1183:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1184:     pub fn get_envs(&self) -> CommandEnvs<'_> {\n  1185:         CommandEnvs { iter: self.inner.get_envs() }\n  1186:     }\n  1187: \n  1188:     /// Returns the working directory for the child process.\n  1189:     ///\n  1190:     /// This returns [`None`] if the working directory will not be changed.\n  1191:     ///\n  1192:     /// # Examples\n  1193:     ///\n  1194:     /// ```\n  1195:     /// use std::path::Path;\n  1196:     /// use std::process::Command;\n  1197:     ///\n  1198:     /// let mut cmd = Command::new(\"ls\");\n  1199:     /// assert_eq!(cmd.get_current_dir(), None);\n  1200:     /// cmd.current_dir(\"/bin\");",
    "nanvix_source": "  1243:     ///\n  1244:     /// let mut cmd = Command::new(\"ls\");\n  1245:     /// cmd.env(\"TERM\", \"dumb\").env_remove(\"TZ\");\n  1246:     /// let envs: Vec<(&OsStr, Option<&OsStr>)> = cmd.get_envs().collect();\n  1247:     /// assert_eq!(envs, &[\n  1248:     ///     (OsStr::new(\"TERM\"), Some(OsStr::new(\"dumb\"))),\n  1249:     ///     (OsStr::new(\"TZ\"), None)\n  1250:     /// ]);\n  1251:     /// ```\n  1252:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1253:     pub fn get_envs(&self) -> CommandEnvs<'_> {\n  1254:         CommandEnvs { iter: self.inner.get_envs() }\n  1255:     }\n  1256: \n  1257:     /// Returns an iterator of the environment variables that will be set when the process is spawned.\n  1258:     ///\n  1259:     /// This returns the environment as it would be if the command were executed at the time of calling\n  1260:     /// this method. The returned environment includes:\n  1261:     /// - All inherited environment variables from the parent process (unless [`Command::env_clear`] was called)\n  1262:     /// - All environment variables explicitly set via [`Command::env`] or [`Command::envs`]\n  1263:     /// - Excluding any environment variables removed via [`Command::env_remove`]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::get_program",
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
      "external_or_hidden_runtime_state",
      "reference_identity_vs_view"
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
      "name": "get_program",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 1857,
                "path": "OsStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1111:             .map(Child::from_inner)\n  1112:             .and_then(|mut p| p.wait())\n  1113:     }\n  1114: \n  1115:     /// Returns the path to the program that was given to [`Command::new`].\n  1116:     ///\n  1117:     /// # Examples\n  1118:     ///\n  1119:     /// ```\n  1120:     /// use std::process::Command;\n  1121:     ///\n  1122:     /// let cmd = Command::new(\"echo\");\n  1123:     /// assert_eq!(cmd.get_program(), \"echo\");\n  1124:     /// ```\n  1125:     #[must_use]\n  1126:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1127:     pub fn get_program(&self) -> &OsStr {\n  1128:         self.inner.get_program()\n  1129:     }\n  1130: \n  1131:     /// Returns an iterator of the arguments that will be passed to the program.\n  1132:     ///\n  1133:     /// This does not include the path to the program as the first argument;\n  1134:     /// it only includes the arguments specified with [`Command::arg`] and\n  1135:     /// [`Command::args`].\n  1136:     ///\n  1137:     /// # Examples\n  1138:     ///\n  1139:     /// ```\n  1140:     /// use std::ffi::OsStr;\n  1141:     /// use std::process::Command;\n  1142:     ///\n  1143:     /// let mut cmd = Command::new(\"echo\");",
    "nanvix_source": "  1185:     /// # Examples\n  1186:     ///\n  1187:     /// ```\n  1188:     /// use std::process::Command;\n  1189:     ///\n  1190:     /// let cmd = Command::new(\"echo\");\n  1191:     /// assert_eq!(cmd.get_program(), \"echo\");\n  1192:     /// ```\n  1193:     #[must_use]\n  1194:     #[stable(feature = \"command_access\", since = \"1.57.0\")]\n  1195:     pub fn get_program(&self) -> &OsStr {\n  1196:         self.inner.get_program()\n  1197:     }\n  1198: \n  1199:     /// Returns an iterator of the arguments that will be passed to the program.\n  1200:     ///\n  1201:     /// This does not include the path to the program as the first argument;\n  1202:     /// it only includes the arguments specified with [`Command::arg`] and\n  1203:     /// [`Command::args`].\n  1204:     ///\n  1205:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::new",
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
                                    "id": 1857,
                                    "path": "OsStr"
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
            "name": "S"
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
      "name": "new",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "program",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 5602,
            "path": "Command"
          }
        }
      }
    },
    "verification_source": "   649:     /// path along with arguments like `Command::new(\"ls -l\").spawn()`, it will try to search for\n   650:     /// `ls -l` literally. The arguments need to be passed separately, such as via [`arg`] or\n   651:     /// [`args`].\n   652:     ///\n   653:     /// ```no_run\n   654:     /// use std::process::Command;\n   655:     ///\n   656:     /// Command::new(\"ls\")\n   657:     ///     .arg(\"-l\") // arg passed separately\n   658:     ///     .spawn()\n   659:     ///     .expect(\"ls command failed to start\");\n   660:     /// ```\n   661:     ///\n   662:     /// [`arg`]: Self::arg\n   663:     /// [`args`]: Self::args\n   664:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   665:     pub fn new<S: AsRef<OsStr>>(program: S) -> Command {\n   666:         Command { inner: imp::Command::new(program.as_ref()) }\n   667:     }\n   668: \n   669:     /// Adds an argument to pass to the program.\n   670:     ///\n   671:     /// Only one argument can be passed per use. So instead of:\n   672:     ///\n   673:     /// ```no_run\n   674:     /// # std::process::Command::new(\"sh\")\n   675:     /// .arg(\"-C /path/to/repo\")\n   676:     /// # ;\n   677:     /// ```\n   678:     ///\n   679:     /// usage would be:\n   680:     ///\n   681:     /// ```no_run",
    "nanvix_source": "   676:     ///\n   677:     /// Command::new(\"ls\")\n   678:     ///     .arg(\"-l\") // arg passed separately\n   679:     ///     .spawn()\n   680:     ///     .expect(\"ls command failed to start\");\n   681:     /// ```\n   682:     ///\n   683:     /// [`arg`]: Self::arg\n   684:     /// [`args`]: Self::args\n   685:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   686:     pub fn new<S: AsRef<OsStr>>(program: S) -> Command {\n   687:         Command { inner: imp::Command::new(program.as_ref()) }\n   688:     }\n   689: \n   690:     /// Adds an argument to pass to the program.\n   691:     ///\n   692:     /// Only one argument can be passed per use. So instead of:\n   693:     ///\n   694:     /// ```no_run\n   695:     /// # std::process::Command::new(\"sh\")\n   696:     /// .arg(\"-C /path/to/repo\")",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::output",
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
      "name": "output",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
                      "resolved_path": {
                        "args": null,
                        "id": 7293,
                        "path": "Output"
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
    "verification_source": "  1067:     ///\n  1068:     /// ```should_panic\n  1069:     /// use std::process::Command;\n  1070:     /// use std::io::{self, Write};\n  1071:     /// let output = Command::new(\"/bin/cat\")\n  1072:     ///     .arg(\"file.txt\")\n  1073:     ///     .output()?;\n  1074:     ///\n  1075:     /// println!(\"status: {}\", output.status);\n  1076:     /// io::stdout().write_all(&output.stdout)?;\n  1077:     /// io::stderr().write_all(&output.stderr)?;\n  1078:     ///\n  1079:     /// assert!(output.status.success());\n  1080:     /// # io::Result::Ok(())\n  1081:     /// ```\n  1082:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1083:     pub fn output(&mut self) -> io::Result<Output> {\n  1084:         let (status, stdout, stderr) = imp::output(&mut self.inner)?;\n  1085:         Ok(Output { status: ExitStatus(status), stdout, stderr })\n  1086:     }\n  1087: \n  1088:     /// Executes a command as a child process, waiting for it to finish and\n  1089:     /// collecting its status.\n  1090:     ///\n  1091:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  1092:     ///\n  1093:     /// # Examples\n  1094:     ///\n  1095:     /// ```should_panic\n  1096:     /// use std::process::Command;\n  1097:     ///\n  1098:     /// let status = Command::new(\"/bin/cat\")\n  1099:     ///     .arg(\"file.txt\")",
    "nanvix_source": "  1128:     ///     .output()?;\n  1129:     ///\n  1130:     /// println!(\"status: {}\", output.status);\n  1131:     /// io::stdout().write_all(&output.stdout)?;\n  1132:     /// io::stderr().write_all(&output.stderr)?;\n  1133:     ///\n  1134:     /// assert!(output.status.success());\n  1135:     /// # io::Result::Ok(())\n  1136:     /// ```\n  1137:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1138:     pub fn output(&mut self) -> io::Result<Output> {\n  1139:         let (status, stdout, stderr) = imp::output(&mut self.inner)?;\n  1140:         Ok(Output { status: ExitStatus(status), stdout, stderr })\n  1141:     }\n  1142: \n  1143:     /// Executes a command as a child process, waiting for it to finish and\n  1144:     /// collecting its status.\n  1145:     ///\n  1146:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  1147:     ///\n  1148:     /// # Errors",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::spawn",
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
      "name": "spawn",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
                      "resolved_path": {
                        "args": null,
                        "id": 5654,
                        "path": "Child"
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
    "verification_source": "  1038:     }\n  1039: \n  1040:     /// Executes the command as a child process, returning a handle to it.\n  1041:     ///\n  1042:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  1043:     ///\n  1044:     /// # Examples\n  1045:     ///\n  1046:     /// ```no_run\n  1047:     /// use std::process::Command;\n  1048:     ///\n  1049:     /// Command::new(\"ls\")\n  1050:     ///     .spawn()\n  1051:     ///     .expect(\"ls command failed to start\");\n  1052:     /// ```\n  1053:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1054:     pub fn spawn(&mut self) -> io::Result<Child> {\n  1055:         self.inner.spawn(imp::Stdio::Inherit, true).map(Child::from_inner)\n  1056:     }\n  1057: \n  1058:     /// Executes the command as a child process, waiting for it to finish and\n  1059:     /// collecting all of its output.\n  1060:     ///\n  1061:     /// By default, stdout and stderr are captured (and used to provide the\n  1062:     /// resulting output). Stdin is not inherited from the parent and any\n  1063:     /// attempt by the child process to read from the stdin stream will result\n  1064:     /// in the stream immediately closing.\n  1065:     ///\n  1066:     /// # Examples\n  1067:     ///\n  1068:     /// ```should_panic\n  1069:     /// use std::process::Command;\n  1070:     /// use std::io::{self, Write};",
    "nanvix_source": "  1085:     /// # Examples\n  1086:     ///\n  1087:     /// ```no_run\n  1088:     /// use std::process::Command;\n  1089:     ///\n  1090:     /// Command::new(\"ls\")\n  1091:     ///     .spawn()\n  1092:     ///     .expect(\"ls command failed to start\");\n  1093:     /// ```\n  1094:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1095:     pub fn spawn(&mut self) -> io::Result<Child> {\n  1096:         self.inner.spawn(imp::Stdio::Inherit, true).map(Child::from_inner)\n  1097:     }\n  1098: \n  1099:     /// Executes the command as a child process, waiting for it to finish and\n  1100:     /// collecting all of its output.\n  1101:     ///\n  1102:     /// By default, stdout and stderr are captured (and used to provide the\n  1103:     /// resulting output). Stdin is not inherited from the parent and any\n  1104:     /// attempt by the child process to read from the stdin stream will result\n  1105:     /// in the stream immediately closing.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::status",
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
      "name": "status",
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
            "id": 5602,
            "path": "Command"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7388",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:5602",
        "resolved_owner_path": [
          "std",
          "process",
          "Command"
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
                      "resolved_path": {
                        "args": null,
                        "id": 5632,
                        "path": "ExitStatus"
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
    "verification_source": "  1092:     ///\n  1093:     /// # Examples\n  1094:     ///\n  1095:     /// ```should_panic\n  1096:     /// use std::process::Command;\n  1097:     ///\n  1098:     /// let status = Command::new(\"/bin/cat\")\n  1099:     ///     .arg(\"file.txt\")\n  1100:     ///     .status()\n  1101:     ///     .expect(\"failed to execute process\");\n  1102:     ///\n  1103:     /// println!(\"process finished with: {status}\");\n  1104:     ///\n  1105:     /// assert!(status.success());\n  1106:     /// ```\n  1107:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1108:     pub fn status(&mut self) -> io::Result<ExitStatus> {\n  1109:         self.inner\n  1110:             .spawn(imp::Stdio::Inherit, true)\n  1111:             .map(Child::from_inner)\n  1112:             .and_then(|mut p| p.wait())\n  1113:     }\n  1114: \n  1115:     /// Returns the path to the program that was given to [`Command::new`].\n  1116:     ///\n  1117:     /// # Examples\n  1118:     ///\n  1119:     /// ```\n  1120:     /// use std::process::Command;\n  1121:     ///\n  1122:     /// let cmd = Command::new(\"echo\");\n  1123:     /// assert_eq!(cmd.get_program(), \"echo\");\n  1124:     /// ```",
    "nanvix_source": "  1166:     /// let status = Command::new(\"/bin/cat\")\n  1167:     ///     .arg(\"file.txt\")\n  1168:     ///     .status()\n  1169:     ///     .expect(\"failed to execute process\");\n  1170:     ///\n  1171:     /// println!(\"process finished with: {status}\");\n  1172:     ///\n  1173:     /// assert!(status.success());\n  1174:     /// ```\n  1175:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1176:     pub fn status(&mut self) -> io::Result<ExitStatus> {\n  1177:         self.inner\n  1178:             .spawn(imp::Stdio::Inherit, true)\n  1179:             .map(Child::from_inner)\n  1180:             .and_then(|mut p| p.wait())\n  1181:     }\n  1182: \n  1183:     /// Returns the path to the program that was given to [`Command::new`].\n  1184:     ///\n  1185:     /// # Examples\n  1186:     ///",
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
