For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::os::windows::io::IntoRawHandle::into_raw_handle",
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
      "name": "into_raw_handle",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:598",
        "kind": "trait",
        "name": "IntoRawHandle",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "IntoRawHandle"
        ]
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
            "args": null,
            "id": 593,
            "path": "RawHandle"
          }
        }
      }
    },
    "verification_source": "    74: \n    75: /// A trait to express the ability to consume an object and acquire ownership of\n    76: /// its raw `HANDLE`.\n    77: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n    78: pub trait IntoRawHandle {\n    79:     /// Consumes this object, returning the raw underlying handle.\n    80:     ///\n    81:     /// This function is typically used to **transfer ownership** of the underlying\n    82:     /// handle to the caller. When used in this way, callers are then the unique\n    83:     /// owners of the handle and must close it once it's no longer needed.\n    84:     ///\n    85:     /// However, transferring ownership is not strictly required. Use a\n    86:     /// `Into<OwnedHandle>::into` implementation for an API which strictly\n    87:     /// transfers ownership.\n    88:     #[must_use = \"losing the raw handle may leak resources\"]\n    89:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n    90:     fn into_raw_handle(self) -> RawHandle;\n    91: }\n    92: \n    93: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    94: impl AsRawHandle for fs::File {\n    95:     #[inline]\n    96:     fn as_raw_handle(&self) -> RawHandle {\n    97:         self.as_inner().as_raw_handle() as RawHandle\n    98:     }\n    99: }\n   100: \n   101: #[stable(feature = \"asraw_stdio\", since = \"1.21.0\")]\n   102: impl AsRawHandle for io::Stdin {\n   103:     fn as_raw_handle(&self) -> RawHandle {\n   104:         stdio_handle(unsafe { sys::c::GetStdHandle(sys::c::STD_INPUT_HANDLE) as RawHandle })\n   105:     }\n   106: }",
    "nanvix_source": "    80:     ///\n    81:     /// This function is typically used to **transfer ownership** of the underlying\n    82:     /// handle to the caller. When used in this way, callers are then the unique\n    83:     /// owners of the handle and must close it once it's no longer needed.\n    84:     ///\n    85:     /// However, transferring ownership is not strictly required. Use a\n    86:     /// `Into<OwnedHandle>::into` implementation for an API which strictly\n    87:     /// transfers ownership.\n    88:     #[must_use = \"losing the raw handle may leak resources\"]\n    89:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n    90:     fn into_raw_handle(self) -> RawHandle;\n    91: }\n    92: \n    93: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    94: impl AsRawHandle for fs::File {\n    95:     #[inline]\n    96:     fn as_raw_handle(&self) -> RawHandle {\n    97:         self.as_inner().as_raw_handle() as RawHandle\n    98:     }\n    99: }\n   100: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::os::windows::io::IntoRawSocket::into_raw_socket",
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
      "name": "into_raw_socket",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:4768",
        "kind": "trait",
        "name": "IntoRawSocket",
        "path": [
          "std",
          "os",
          "windows",
          "io",
          "raw",
          "IntoRawSocket"
        ]
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
            "args": null,
            "id": 4760,
            "path": "RawSocket"
          }
        }
      }
    },
    "verification_source": "   218: \n   219: /// A trait to express the ability to consume an object and acquire ownership of\n   220: /// its raw `SOCKET`.\n   221: #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   222: pub trait IntoRawSocket {\n   223:     /// Consumes this object, returning the raw underlying socket.\n   224:     ///\n   225:     /// This function is typically used to **transfer ownership** of the underlying\n   226:     /// socket to the caller. When used in this way, callers are then the unique\n   227:     /// owners of the socket and must close it once it's no longer needed.\n   228:     ///\n   229:     /// However, transferring ownership is not strictly required. Use a\n   230:     /// `Into<OwnedSocket>::into` implementation for an API which strictly\n   231:     /// transfers ownership.\n   232:     #[must_use = \"losing the raw socket may leak resources\"]\n   233:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   234:     fn into_raw_socket(self) -> RawSocket;\n   235: }\n   236: \n   237: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   238: impl AsRawSocket for net::TcpStream {\n   239:     #[inline]\n   240:     fn as_raw_socket(&self) -> RawSocket {\n   241:         self.as_inner().socket().as_raw_socket()\n   242:     }\n   243: }\n   244: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245: impl AsRawSocket for net::TcpListener {\n   246:     #[inline]\n   247:     fn as_raw_socket(&self) -> RawSocket {\n   248:         self.as_inner().socket().as_raw_socket()\n   249:     }\n   250: }",
    "nanvix_source": "   224:     ///\n   225:     /// This function is typically used to **transfer ownership** of the underlying\n   226:     /// socket to the caller. When used in this way, callers are then the unique\n   227:     /// owners of the socket and must close it once it's no longer needed.\n   228:     ///\n   229:     /// However, transferring ownership is not strictly required. Use a\n   230:     /// `Into<OwnedSocket>::into` implementation for an API which strictly\n   231:     /// transfers ownership.\n   232:     #[must_use = \"losing the raw socket may leak resources\"]\n   233:     #[stable(feature = \"into_raw_os\", since = \"1.4.0\")]\n   234:     fn into_raw_socket(self) -> RawSocket;\n   235: }\n   236: \n   237: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   238: impl AsRawSocket for net::TcpStream {\n   239:     #[inline]\n   240:     fn as_raw_socket(&self) -> RawSocket {\n   241:         self.as_inner().socket().as_raw_socket()\n   242:     }\n   243: }\n   244: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::process::Termination::report",
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
      "name": "report",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "std:7579",
        "kind": "trait",
        "name": "Termination",
        "path": [
          "std",
          "process",
          "Termination"
        ]
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
            "args": null,
            "id": 6388,
            "path": "ExitCode"
          }
        }
      }
    },
    "verification_source": "  2562: ///\n  2563: /// Because different runtimes have different specifications on the return value\n  2564: /// of the `main` function, this trait is likely to be available only on\n  2565: /// standard library's runtime for convenience. Other runtimes are not required\n  2566: /// to provide similar functionality.\n  2567: #[cfg_attr(not(any(test, doctest)), lang = \"termination\")]\n  2568: #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2569: #[rustc_on_unimplemented(on(\n  2570:     cause = \"MainFunctionType\",\n  2571:     message = \"`main` has invalid return type `{Self}`\",\n  2572:     label = \"`main` can only return types that implement `{This}`\"\n  2573: ))]\n  2574: pub trait Termination {\n  2575:     /// Is called to get the representation of the value as status code.\n  2576:     /// This status code is returned to the operating system.\n  2577:     #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2578:     fn report(self) -> ExitCode;\n  2579: }\n  2580: \n  2581: #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2582: impl Termination for () {\n  2583:     #[inline]\n  2584:     fn report(self) -> ExitCode {\n  2585:         ExitCode::SUCCESS\n  2586:     }\n  2587: }\n  2588: \n  2589: #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2590: impl Termination for ! {\n  2591:     fn report(self) -> ExitCode {\n  2592:         self\n  2593:     }\n  2594: }",
    "nanvix_source": "  2674: #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2675: #[rustc_on_unimplemented(on(\n  2676:     cause = \"MainFunctionType\",\n  2677:     message = \"`main` has invalid return type `{Self}`\",\n  2678:     label = \"`main` can only return types that implement `{This}`\"\n  2679: ))]\n  2680: pub trait Termination {\n  2681:     /// Is called to get the representation of the value as status code.\n  2682:     /// This status code is returned to the operating system.\n  2683:     #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2684:     fn report(self) -> ExitCode;\n  2685: }\n  2686: \n  2687: #[stable(feature = \"termination_trait_lib\", since = \"1.61.0\")]\n  2688: impl Termination for () {\n  2689:     #[inline]\n  2690:     fn report(self) -> ExitCode {\n  2691:         ExitCode::SUCCESS\n  2692:     }\n  2693: }\n  2694: ",
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
