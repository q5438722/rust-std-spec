For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::process::Stdio::null",
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
      "name": "null",
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
            "id": 2706,
            "path": "Stdio"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7489",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2706",
        "resolved_owner_path": [
          "std",
          "process",
          "Stdio"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 2706,
            "path": "Stdio"
          }
        }
      }
    },
    "verification_source": "  1545:     /// With stdin:\n  1546:     ///\n  1547:     /// ```no_run\n  1548:     /// use std::process::{Command, Stdio};\n  1549:     ///\n  1550:     /// let output = Command::new(\"rev\")\n  1551:     ///     .stdin(Stdio::null())\n  1552:     ///     .stdout(Stdio::piped())\n  1553:     ///     .output()\n  1554:     ///     .expect(\"Failed to execute command\");\n  1555:     ///\n  1556:     /// assert_eq!(String::from_utf8_lossy(&output.stdout), \"\");\n  1557:     /// // Ignores any piped-in input\n  1558:     /// ```\n  1559:     #[must_use]\n  1560:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1561:     pub fn null() -> Stdio {\n  1562:         Stdio(imp::Stdio::Null)\n  1563:     }\n  1564: \n  1565:     /// Returns `true` if this requires [`Command`] to create a new pipe.\n  1566:     ///\n  1567:     /// # Example\n  1568:     ///\n  1569:     /// ```\n  1570:     /// #![feature(stdio_makes_pipe)]\n  1571:     /// use std::process::Stdio;\n  1572:     ///\n  1573:     /// let io = Stdio::piped();\n  1574:     /// assert_eq!(io.makes_pipe(), true);\n  1575:     /// ```\n  1576:     #[unstable(feature = \"stdio_makes_pipe\", issue = \"98288\")]\n  1577:     pub fn makes_pipe(&self) -> bool {",
    "nanvix_source": "  1665:     ///     .stdin(Stdio::null())\n  1666:     ///     .stdout(Stdio::piped())\n  1667:     ///     .output()\n  1668:     ///     .expect(\"Failed to execute command\");\n  1669:     ///\n  1670:     /// assert_eq!(String::from_utf8_lossy(&output.stdout), \"\");\n  1671:     /// // Ignores any piped-in input\n  1672:     /// ```\n  1673:     #[must_use]\n  1674:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1675:     pub fn null() -> Stdio {\n  1676:         Stdio(imp::Stdio::Null)\n  1677:     }\n  1678: \n  1679:     /// Returns `true` if this requires [`Command`] to create a new pipe.\n  1680:     ///\n  1681:     /// # Example\n  1682:     ///\n  1683:     /// ```\n  1684:     /// #![feature(stdio_makes_pipe)]\n  1685:     /// use std::process::Stdio;",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Stdio::piped",
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
      "name": "piped",
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
            "id": 2706,
            "path": "Stdio"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7489",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:2706",
        "resolved_owner_path": [
          "std",
          "process",
          "Stdio"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 2706,
            "path": "Stdio"
          }
        }
      }
    },
    "verification_source": "  1465:     /// std::thread::spawn(move || {\n  1466:     ///     stdin.write_all(\"Hello, world!\".as_bytes()).expect(\"Failed to write to stdin\");\n  1467:     /// });\n  1468:     ///\n  1469:     /// let output = child.wait_with_output().expect(\"Failed to read stdout\");\n  1470:     /// assert_eq!(String::from_utf8_lossy(&output.stdout), \"!dlrow ,olleH\");\n  1471:     /// ```\n  1472:     ///\n  1473:     /// Writing more than a pipe buffer's worth of input to stdin without also reading\n  1474:     /// stdout and stderr at the same time may cause a deadlock.\n  1475:     /// This is an issue when running any program that doesn't guarantee that it reads\n  1476:     /// its entire stdin before writing more than a pipe buffer's worth of output.\n  1477:     /// The size of a pipe buffer varies on different targets.\n  1478:     ///\n  1479:     #[must_use]\n  1480:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1481:     pub fn piped() -> Stdio {\n  1482:         Stdio(imp::Stdio::MakePipe)\n  1483:     }\n  1484: \n  1485:     /// The child inherits from the corresponding parent descriptor.\n  1486:     ///\n  1487:     /// # Examples\n  1488:     ///\n  1489:     /// With stdout:\n  1490:     ///\n  1491:     /// ```no_run\n  1492:     /// use std::process::{Command, Stdio};\n  1493:     ///\n  1494:     /// let output = Command::new(\"echo\")\n  1495:     ///     .arg(\"Hello, world!\")\n  1496:     ///     .stdout(Stdio::inherit())\n  1497:     ///     .output()",
    "nanvix_source": "  1585:     /// ```\n  1586:     ///\n  1587:     /// Writing more than a pipe buffer's worth of input to stdin without also reading\n  1588:     /// stdout and stderr at the same time may cause a deadlock.\n  1589:     /// This is an issue when running any program that doesn't guarantee that it reads\n  1590:     /// its entire stdin before writing more than a pipe buffer's worth of output.\n  1591:     /// The size of a pipe buffer varies on different targets.\n  1592:     ///\n  1593:     #[must_use]\n  1594:     #[stable(feature = \"process\", since = \"1.0.0\")]\n  1595:     pub fn piped() -> Stdio {\n  1596:         Stdio(imp::Stdio::MakePipe)\n  1597:     }\n  1598: \n  1599:     /// The child inherits from the corresponding parent descriptor.\n  1600:     ///\n  1601:     /// # Examples\n  1602:     ///\n  1603:     /// With stdout:\n  1604:     ///\n  1605:     /// ```no_run",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::abort",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "abort",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "primitive": "never"
        }
      }
    },
    "verification_source": "  2519: ///         println!(\"This will never be printed!\");\n  2520: ///     }\n  2521: /// }\n  2522: ///\n  2523: /// fn main() {\n  2524: ///     let _x = HasDrop;\n  2525: ///     process::abort();\n  2526: ///     // the destructor implemented for HasDrop will never get run\n  2527: /// }\n  2528: /// ```\n  2529: ///\n  2530: /// [panic hook]: crate::panic::set_hook\n  2531: #[stable(feature = \"process_abort\", since = \"1.17.0\")]\n  2532: #[cold]\n  2533: #[cfg_attr(not(test), rustc_diagnostic_item = \"process_abort\")]\n  2534: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2535: pub fn abort() -> ! {\n  2536:     crate::sys::abort_internal();\n  2537: }\n  2538: \n  2539: /// Returns the OS-assigned process identifier associated with this process.\n  2540: ///\n  2541: /// # Examples\n  2542: ///\n  2543: /// ```no_run\n  2544: /// use std::process;\n  2545: ///\n  2546: /// println!(\"My pid is {}\", process::id());\n  2547: /// ```\n  2548: #[must_use]\n  2549: #[stable(feature = \"getpid\", since = \"1.26.0\")]\n  2550: pub fn id() -> u32 {\n  2551:     imp::getpid()",
    "nanvix_source": "  2627: ///     process::abort();\n  2628: ///     // the destructor implemented for HasDrop will never get run\n  2629: /// }\n  2630: /// ```\n  2631: ///\n  2632: /// [panic hook]: crate::panic::set_hook\n  2633: #[stable(feature = \"process_abort\", since = \"1.17.0\")]\n  2634: #[cold]\n  2635: #[cfg_attr(not(test), rustc_diagnostic_item = \"process_abort\")]\n  2636: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2637: pub fn abort() -> ! {\n  2638:     crate::sys::abort_internal();\n  2639: }\n  2640: \n  2641: #[doc(inline)]\n  2642: #[unstable(feature = \"abort_immediate\", issue = \"154601\")]\n  2643: pub use core::process::abort_immediate;\n  2644: \n  2645: /// Returns the OS-assigned process identifier associated with this process.\n  2646: ///\n  2647: /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::exit",
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
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "exit",
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
            "code",
            {
              "primitive": "i32"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "never"
        }
      }
    },
    "verification_source": "  2452: /// Note that if a binary contains multiple copies of the Rust runtime (e.g., when combining\n  2453: /// multiple `cdylib` or `staticlib`), they each have their own separate lock, so from the\n  2454: /// perspective of code running in one of the Rust runtimes, the \"outside\" Rust code is basically C\n  2455: /// code, and concurrent `exit` again causes undefined behavior.\n  2456: ///\n  2457: /// Individual C implementations might provide more guarantees than the standard and permit concurrent\n  2458: /// calls to `exit`; consult the documentation of your C implementation for details.\n  2459: ///\n  2460: /// For some of the on-going discussion to make `exit` thread-safe in C, see:\n  2461: /// - [Rust issue #126600](https://github.com/rust-lang/rust/issues/126600)\n  2462: /// - [Austin Group Bugzilla (for POSIX)](https://austingroupbugs.net/view.php?id=1845)\n  2463: /// - [GNU C library Bugzilla](https://sourceware.org/bugzilla/show_bug.cgi?id=31997)\n  2464: ///\n  2465: /// [C-exit]: https://en.cppreference.com/w/c/program/exit\n  2466: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2467: #[cfg_attr(not(test), rustc_diagnostic_item = \"process_exit\")]\n  2468: pub fn exit(code: i32) -> ! {\n  2469:     crate::rt::cleanup();\n  2470:     crate::sys::exit::exit(code)\n  2471: }\n  2472: \n  2473: /// Terminates the process in an abnormal fashion.\n  2474: ///\n  2475: /// The function will never return and will immediately terminate the current\n  2476: /// process in a platform specific \"abnormal\" manner. As a consequence,\n  2477: /// no destructors on the current stack or any other thread's stack\n  2478: /// will be run, Rust IO buffers (eg, from `BufWriter`) will not be flushed,\n  2479: /// and C stdio buffers will (on most platforms) not be flushed.\n  2480: ///\n  2481: /// This is in contrast to the default behavior of [`panic!`] which unwinds\n  2482: /// the current thread's stack and calls all destructors.\n  2483: /// When `panic=\"abort\"` is set, either as an argument to `rustc` or in a\n  2484: /// crate's Cargo.toml, [`panic!`] and `abort` are similar. However,",
    "nanvix_source": "  2560: /// calls to `exit`; consult the documentation of your C implementation for details.\n  2561: ///\n  2562: /// For some of the on-going discussion to make `exit` thread-safe in C, see:\n  2563: /// - [Rust issue #126600](https://github.com/rust-lang/rust/issues/126600)\n  2564: /// - [Austin Group Bugzilla (for POSIX)](https://austingroupbugs.net/view.php?id=1845)\n  2565: /// - [GNU C library Bugzilla](https://sourceware.org/bugzilla/show_bug.cgi?id=31997)\n  2566: ///\n  2567: /// [C-exit]: https://en.cppreference.com/w/c/program/exit\n  2568: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2569: #[cfg_attr(not(test), rustc_diagnostic_item = \"process_exit\")]\n  2570: pub fn exit(code: i32) -> ! {\n  2571:     crate::rt::cleanup();\n  2572:     crate::sys::exit::exit(code)\n  2573: }\n  2574: \n  2575: /// Terminates the process in an abnormal fashion.\n  2576: ///\n  2577: /// The function will never return and will immediately terminate the current\n  2578: /// process in a platform specific \"abnormal\" manner. As a consequence,\n  2579: /// no destructors on the current stack or any other thread's stack\n  2580: /// will be run, Rust IO buffers (eg, from `BufWriter`) will not be flushed,",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::id",
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
      "owner": null,
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "primitive": "u32"
        }
      }
    },
    "verification_source": "  2534: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  2535: pub fn abort() -> ! {\n  2536:     crate::sys::abort_internal();\n  2537: }\n  2538: \n  2539: /// Returns the OS-assigned process identifier associated with this process.\n  2540: ///\n  2541: /// # Examples\n  2542: ///\n  2543: /// ```no_run\n  2544: /// use std::process;\n  2545: ///\n  2546: /// println!(\"My pid is {}\", process::id());\n  2547: /// ```\n  2548: #[must_use]\n  2549: #[stable(feature = \"getpid\", since = \"1.26.0\")]\n  2550: pub fn id() -> u32 {\n  2551:     imp::getpid()\n  2552: }\n  2553: \n  2554: /// A trait for implementing arbitrary return types in the `main` function.\n  2555: ///\n  2556: /// The C-main function only supports returning integers.\n  2557: /// So, every type implementing the `Termination` trait has to be converted\n  2558: /// to an integer.\n  2559: ///\n  2560: /// The default implementations are returning `libc::EXIT_SUCCESS` to indicate\n  2561: /// a successful execution. In case of a failure, `libc::EXIT_FAILURE` is returned.\n  2562: ///\n  2563: /// Because different runtimes have different specifications on the return value\n  2564: /// of the `main` function, this trait is likely to be available only on\n  2565: /// standard library's runtime for convenience. Other runtimes are not required\n  2566: /// to provide similar functionality.",
    "nanvix_source": "  2646: ///\n  2647: /// # Examples\n  2648: ///\n  2649: /// ```no_run\n  2650: /// use std::process;\n  2651: ///\n  2652: /// println!(\"My pid is {}\", process::id());\n  2653: /// ```\n  2654: #[must_use]\n  2655: #[stable(feature = \"getpid\", since = \"1.26.0\")]\n  2656: pub fn id() -> u32 {\n  2657:     imp::getpid()\n  2658: }\n  2659: \n  2660: /// A trait for implementing arbitrary return types in the `main` function.\n  2661: ///\n  2662: /// The C-main function only supports returning integers.\n  2663: /// So, every type implementing the `Termination` trait has to be converted\n  2664: /// to an integer.\n  2665: ///\n  2666: /// The default implementations are returning `libc::EXIT_SUCCESS` to indicate",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::Barrier::new",
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
      "concurrency_or_hidden_state"
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
            "id": 8321,
            "path": "Barrier"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:8326",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:8321",
        "resolved_owner_path": [
          "std",
          "sync",
          "barrier",
          "Barrier"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "n",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 8321,
            "path": "Barrier"
          }
        }
      }
    },
    "verification_source": "    68:     /// A barrier will block all threads which call [`wait()`] until the `n`th thread calls [`wait()`],\n    69:     /// and then wake up all threads at once.\n    70:     ///\n    71:     /// [`wait()`]: Barrier::wait\n    72:     ///\n    73:     /// # Examples\n    74:     ///\n    75:     /// ```\n    76:     /// use std::sync::Barrier;\n    77:     ///\n    78:     /// let barrier = Barrier::new(10);\n    79:     /// ```\n    80:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    81:     #[rustc_const_stable(feature = \"const_barrier\", since = \"1.78.0\")]\n    82:     #[must_use]\n    83:     #[inline]\n    84:     pub const fn new(n: usize) -> Barrier {\n    85:         Barrier {\n    86:             lock: Mutex::new(BarrierState { count: 0, generation_id: 0 }),\n    87:             cvar: Condvar::new(),\n    88:             num_threads: n,\n    89:         }\n    90:     }\n    91: \n    92:     /// Blocks the current thread until all threads have rendezvoused here.\n    93:     ///\n    94:     /// Barriers are re-usable after all threads have rendezvoused once, and can\n    95:     /// be used continuously.\n    96:     ///\n    97:     /// A single (arbitrary) thread will receive a [`BarrierWaitResult`] that\n    98:     /// returns `true` from [`BarrierWaitResult::is_leader()`] when returning\n    99:     /// from this function, and all other threads will receive a result that\n   100:     /// will return `false` from [`BarrierWaitResult::is_leader()`].",
    "nanvix_source": "    74:     ///\n    75:     /// ```\n    76:     /// use std::sync::Barrier;\n    77:     ///\n    78:     /// let barrier = Barrier::new(10);\n    79:     /// ```\n    80:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    81:     #[rustc_const_stable(feature = \"const_barrier\", since = \"1.78.0\")]\n    82:     #[must_use]\n    83:     #[inline]\n    84:     pub const fn new(n: usize) -> Barrier {\n    85:         Barrier {\n    86:             lock: Mutex::new(BarrierState { count: 0, generation_id: 0 }),\n    87:             cvar: Condvar::new(),\n    88:             num_threads: n,\n    89:         }\n    90:     }\n    91: \n    92:     /// Blocks the current thread until all threads have rendezvoused here.\n    93:     ///\n    94:     /// Barriers are re-usable after all threads have rendezvoused once, and can",
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
