For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::process::Child::try_wait",
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
      "name": "try_wait",
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
    "verification_source": "  2316:     /// use std::process::Command;\n  2317:     ///\n  2318:     /// let mut child = Command::new(\"ls\").spawn()?;\n  2319:     ///\n  2320:     /// match child.try_wait() {\n  2321:     ///     Ok(Some(status)) => println!(\"exited with: {status}\"),\n  2322:     ///     Ok(None) => {\n  2323:     ///         println!(\"status not ready yet, let's really wait\");\n  2324:     ///         let res = child.wait();\n  2325:     ///         println!(\"result: {res:?}\");\n  2326:     ///     }\n  2327:     ///     Err(e) => println!(\"error attempting to wait: {e}\"),\n  2328:     /// }\n  2329:     /// # std::io::Result::Ok(())\n  2330:     /// ```\n  2331:     #[stable(feature = \"process_try_wait\", since = \"1.18.0\")]\n  2332:     pub fn try_wait(&mut self) -> io::Result<Option<ExitStatus>> {\n  2333:         Ok(self.handle.try_wait()?.map(ExitStatus))\n  2334:     }\n  2335: \n  2336:     /// Simultaneously waits for the child to exit and collect all remaining\n  2337:     /// output on the stdout/stderr handles, returning an `Output`\n  2338:     /// instance.\n  2339:     ///\n  2340:     /// The stdin handle to the child process, if any, will be closed\n  2341:     /// before waiting. This helps avoid deadlock: it ensures that the\n  2342:     /// child does not block waiting for input from the parent, while\n  2343:     /// the parent waits for the child to exit.\n  2344:     ///\n  2345:     /// By default, stdin, stdout and stderr are inherited from the parent.\n  2346:     /// In order to capture the output into this `Result<Output>` it is\n  2347:     /// necessary to create new pipes between parent and child. Use\n  2348:     /// `stdout(Stdio::piped())` or `stderr(Stdio::piped())`, respectively.",
    "nanvix_source": "  2424:     ///     Ok(None) => {\n  2425:     ///         println!(\"status not ready yet, let's really wait\");\n  2426:     ///         let res = child.wait();\n  2427:     ///         println!(\"result: {res:?}\");\n  2428:     ///     }\n  2429:     ///     Err(e) => println!(\"error attempting to wait: {e}\"),\n  2430:     /// }\n  2431:     /// # std::io::Result::Ok(())\n  2432:     /// ```\n  2433:     #[stable(feature = \"process_try_wait\", since = \"1.18.0\")]\n  2434:     pub fn try_wait(&mut self) -> io::Result<Option<ExitStatus>> {\n  2435:         Ok(self.handle.try_wait()?.map(ExitStatus))\n  2436:     }\n  2437: \n  2438:     /// Simultaneously waits for the child to exit and collect all remaining\n  2439:     /// output on the stdout/stderr handles, returning an `Output`\n  2440:     /// instance.\n  2441:     ///\n  2442:     /// The stdin handle to the child process, if any, will be closed\n  2443:     /// before waiting. This helps avoid deadlock: it ensures that the\n  2444:     /// child does not block waiting for input from the parent, while",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Child::wait",
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
      "name": "wait",
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
    "verification_source": "  2277:     /// the parent waits for the child to exit.\n  2278:     ///\n  2279:     /// # Examples\n  2280:     ///\n  2281:     /// ```no_run\n  2282:     /// use std::process::Command;\n  2283:     ///\n  2284:     /// let mut command = Command::new(\"ls\");\n  2285:     /// if let Ok(mut child) = command.spawn() {\n  2286:     ///     child.wait().expect(\"command wasn't running\");\n  2287:     ///     println!(\"Child has finished its execution!\");\n  2288:     /// } else {\n  2289:     ///     println!(\"ls command didn't start\");\n  2290:     /// }\n  2291:     /// ```\n  2292:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2293:     pub fn wait(&mut self) -> io::Result<ExitStatus> {\n  2294:         drop(self.stdin.take());\n  2295:         self.handle.wait().map(ExitStatus)\n  2296:     }\n  2297: \n  2298:     /// Attempts to collect the exit status of the child if it has already\n  2299:     /// exited.\n  2300:     ///\n  2301:     /// This function will not block the calling thread and will only\n  2302:     /// check to see if the child process has exited or not. If the child has\n  2303:     /// exited then on Unix the process ID is reaped. This function is\n  2304:     /// guaranteed to repeatedly return a successful exit status so long as the\n  2305:     /// child has already exited.\n  2306:     ///\n  2307:     /// If the child has exited, then `Ok(Some(status))` is returned. If the\n  2308:     /// exit status is not available at this time then `Ok(None)` is returned.\n  2309:     /// If an error occurs, then that error is returned.",
    "nanvix_source": "  2385:     ///\n  2386:     /// let mut command = Command::new(\"ls\");\n  2387:     /// if let Ok(mut child) = command.spawn() {\n  2388:     ///     child.wait().expect(\"command wasn't running\");\n  2389:     ///     println!(\"Child has finished its execution!\");\n  2390:     /// } else {\n  2391:     ///     println!(\"ls command didn't start\");\n  2392:     /// }\n  2393:     /// ```\n  2394:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2395:     pub fn wait(&mut self) -> io::Result<ExitStatus> {\n  2396:         drop(self.stdin.take());\n  2397:         self.handle.wait().map(ExitStatus)\n  2398:     }\n  2399: \n  2400:     /// Attempts to collect the exit status of the child if it has already\n  2401:     /// exited.\n  2402:     ///\n  2403:     /// This function will not block the calling thread and will only\n  2404:     /// check to see if the child process has exited or not. If the child has\n  2405:     /// exited then on Unix the process ID is reaped. This function is",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Child::wait_with_output",
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
      "name": "wait_with_output",
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
              "generic": "Self"
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
    "verification_source": "  2353:     /// use std::process::{Command, Stdio};\n  2354:     ///\n  2355:     /// let child = Command::new(\"/bin/cat\")\n  2356:     ///     .arg(\"file.txt\")\n  2357:     ///     .stdout(Stdio::piped())\n  2358:     ///     .spawn()\n  2359:     ///     .expect(\"failed to execute child\");\n  2360:     ///\n  2361:     /// let output = child\n  2362:     ///     .wait_with_output()\n  2363:     ///     .expect(\"failed to wait on child\");\n  2364:     ///\n  2365:     /// assert!(output.status.success());\n  2366:     /// ```\n  2367:     ///\n  2368:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2369:     pub fn wait_with_output(mut self) -> io::Result<Output> {\n  2370:         drop(self.stdin.take());\n  2371: \n  2372:         let (mut stdout, mut stderr) = (Vec::new(), Vec::new());\n  2373:         match (self.stdout.take(), self.stderr.take()) {\n  2374:             (None, None) => {}\n  2375:             (Some(mut out), None) => {\n  2376:                 let res = out.read_to_end(&mut stdout);\n  2377:                 res.unwrap();\n  2378:             }\n  2379:             (None, Some(mut err)) => {\n  2380:                 let res = err.read_to_end(&mut stderr);\n  2381:                 res.unwrap();\n  2382:             }\n  2383:             (Some(out), Some(err)) => {\n  2384:                 let res = imp::read_output(out.inner, &mut stdout, err.inner, &mut stderr);\n  2385:                 res.unwrap();",
    "nanvix_source": "  2461:     ///     .expect(\"failed to execute child\");\n  2462:     ///\n  2463:     /// let output = child\n  2464:     ///     .wait_with_output()\n  2465:     ///     .expect(\"failed to wait on child\");\n  2466:     ///\n  2467:     /// assert!(output.status.success());\n  2468:     /// ```\n  2469:     ///\n  2470:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  2471:     pub fn wait_with_output(mut self) -> io::Result<Output> {\n  2472:         drop(self.stdin.take());\n  2473: \n  2474:         let (mut stdout, mut stderr) = (Vec::new(), Vec::new());\n  2475:         match (self.stdout.take(), self.stderr.take()) {\n  2476:             (None, None) => {}\n  2477:             (Some(mut out), None) => {\n  2478:                 let res = out.read_to_end(&mut stdout);\n  2479:                 res.unwrap();\n  2480:             }\n  2481:             (None, Some(mut err)) => {",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::arg",
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
      "name": "arg",
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
          ],
          [
            "arg",
            {
              "generic": "S"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "   712:     /// [windows-args]: crate::process#windows-argument-splitting\n   713:     ///\n   714:     /// </div>\n   715:     ///\n   716:     /// # Examples\n   717:     ///\n   718:     /// ```no_run\n   719:     /// use std::process::Command;\n   720:     ///\n   721:     /// Command::new(\"ls\")\n   722:     ///     .arg(\"-l\")\n   723:     ///     .arg(\"-a\")\n   724:     ///     .spawn()\n   725:     ///     .expect(\"ls command failed to start\");\n   726:     /// ```\n   727:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   728:     pub fn arg<S: AsRef<OsStr>>(&mut self, arg: S) -> &mut Command {\n   729:         self.inner.arg(arg.as_ref());\n   730:         self\n   731:     }\n   732: \n   733:     /// Adds multiple arguments to pass to the program.\n   734:     ///\n   735:     /// To pass a single argument see [`arg`].\n   736:     ///\n   737:     /// [`arg`]: Command::arg\n   738:     ///\n   739:     /// Note that the arguments are not passed through a shell, but given\n   740:     /// literally to the program. This means that shell syntax like quotes,\n   741:     /// escaped characters, word splitting, glob patterns, variable substitution, etc.\n   742:     /// have no effect.\n   743:     ///\n   744:     /// <div class=\"warning\">",
    "nanvix_source": "   739:     /// ```no_run\n   740:     /// use std::process::Command;\n   741:     ///\n   742:     /// Command::new(\"ls\")\n   743:     ///     .arg(\"-l\")\n   744:     ///     .arg(\"-a\")\n   745:     ///     .spawn()\n   746:     ///     .expect(\"ls command failed to start\");\n   747:     /// ```\n   748:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   749:     pub fn arg<S: AsRef<OsStr>>(&mut self, arg: S) -> &mut Command {\n   750:         self.inner.arg(arg.as_ref());\n   751:         self\n   752:     }\n   753: \n   754:     /// Adds multiple arguments to pass to the program.\n   755:     ///\n   756:     /// To pass a single argument see [`arg`].\n   757:     ///\n   758:     /// [`arg`]: Command::arg\n   759:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::args",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "I"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "S"
          }
        ],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "angle_bracketed": {
                          "args": [],
                          "constraints": [
                            {
                              "args": null,
                              "binding": {
                                "equality": {
                                  "type": {
                                    "generic": "S"
                                  }
                                }
                              },
                              "name": "Item"
                            }
                          ]
                        }
                      },
                      "id": 52,
                      "path": "IntoIterator"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "I"
              }
            }
          },
          {
            "bound_predicate": {
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
              "generic_params": [],
              "type": {
                "generic": "S"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "args",
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
          ],
          [
            "args",
            {
              "generic": "I"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "   758:     /// [`raw_arg`]: crate::os::windows::process::CommandExt::raw_arg\n   759:     /// [windows-args]: crate::process#windows-argument-splitting\n   760:     ///\n   761:     /// </div>\n   762:     ///\n   763:     /// # Examples\n   764:     ///\n   765:     /// ```no_run\n   766:     /// use std::process::Command;\n   767:     ///\n   768:     /// Command::new(\"ls\")\n   769:     ///     .args([\"-l\", \"-a\"])\n   770:     ///     .spawn()\n   771:     ///     .expect(\"ls command failed to start\");\n   772:     /// ```\n   773:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   774:     pub fn args<I, S>(&mut self, args: I) -> &mut Command\n   775:     where\n   776:         I: IntoIterator<Item = S>,\n   777:         S: AsRef<OsStr>,\n   778:     {\n   779:         for arg in args {\n   780:             self.arg(arg.as_ref());\n   781:         }\n   782:         self\n   783:     }\n   784: \n   785:     /// Inserts or updates an explicit environment variable mapping.\n   786:     ///\n   787:     /// This method allows you to add an environment variable mapping to the spawned process or\n   788:     /// overwrite a previously set value. You can use [`Command::envs`] to set multiple environment\n   789:     /// variables simultaneously.\n   790:     ///",
    "nanvix_source": "   785:     ///\n   786:     /// ```no_run\n   787:     /// use std::process::Command;\n   788:     ///\n   789:     /// Command::new(\"ls\")\n   790:     ///     .args([\"-l\", \"-a\"])\n   791:     ///     .spawn()\n   792:     ///     .expect(\"ls command failed to start\");\n   793:     /// ```\n   794:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   795:     pub fn args<I, S>(&mut self, args: I) -> &mut Command\n   796:     where\n   797:         I: IntoIterator<Item = S>,\n   798:         S: AsRef<OsStr>,\n   799:     {\n   800:         for arg in args {\n   801:             self.arg(arg.as_ref());\n   802:         }\n   803:         self\n   804:     }\n   805: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Command::current_dir",
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
      "name": "current_dir",
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
          ],
          [
            "dir",
            {
              "generic": "P"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 5602,
                "path": "Command"
              }
            }
          }
        }
      }
    },
    "verification_source": "   938:     /// platform specific and unstable, and it's recommended to use\n   939:     /// [`canonicalize`] to get an absolute program path instead.\n   940:     ///\n   941:     /// # Examples\n   942:     ///\n   943:     /// ```no_run\n   944:     /// use std::process::Command;\n   945:     ///\n   946:     /// Command::new(\"ls\")\n   947:     ///     .current_dir(\"/bin\")\n   948:     ///     .spawn()\n   949:     ///     .expect(\"ls command failed to start\");\n   950:     /// ```\n   951:     ///\n   952:     /// [`canonicalize`]: crate::fs::canonicalize\n   953:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   954:     pub fn current_dir<P: AsRef<Path>>(&mut self, dir: P) -> &mut Command {\n   955:         self.inner.cwd(dir.as_ref().as_ref());\n   956:         self\n   957:     }\n   958: \n   959:     /// Configuration for the child process's standard input (stdin) handle.\n   960:     ///\n   961:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n   962:     /// defaults to [`piped`] when used with [`output`].\n   963:     ///\n   964:     /// [`inherit`]: Stdio::inherit\n   965:     /// [`piped`]: Stdio::piped\n   966:     /// [`spawn`]: Self::spawn\n   967:     /// [`status`]: Self::status\n   968:     /// [`output`]: Self::output\n   969:     ///\n   970:     /// # Examples",
    "nanvix_source": "   965:     /// use std::process::Command;\n   966:     ///\n   967:     /// Command::new(\"ls\")\n   968:     ///     .current_dir(\"/bin\")\n   969:     ///     .spawn()\n   970:     ///     .expect(\"ls command failed to start\");\n   971:     /// ```\n   972:     ///\n   973:     /// [`canonicalize`]: crate::fs::canonicalize\n   974:     #[stable(feature = \"process\", since = \"1.0.0\")]\n   975:     pub fn current_dir<P: AsRef<Path>>(&mut self, dir: P) -> &mut Command {\n   976:         self.inner.cwd(dir.as_ref().as_ref());\n   977:         self\n   978:     }\n   979: \n   980:     /// Configuration for the child process's standard input (stdin) handle.\n   981:     ///\n   982:     /// Defaults to [`inherit`] when used with [`spawn`] or [`status`], and\n   983:     /// defaults to [`piped`] when used with [`output`].\n   984:     ///\n   985:     /// [`inherit`]: Stdio::inherit",
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
