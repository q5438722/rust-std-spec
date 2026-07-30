For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::write",
    "generation_group": "formatting_effect",
    "classification": "formatting_effect",
    "classification_reasons": [
      "formatting_state_not_modeled"
    ],
    "category": "formatting",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "formatting_effect"
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
      "name": "write",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "output"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "output",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "dyn_trait": {
                    "lifetime": null,
                    "traits": [
                      {
                        "generic_params": [],
                        "trait": {
                          "args": null,
                          "id": 29961,
                          "path": "Write"
                        }
                      }
                    ]
                  }
                }
              }
            }
          ],
          [
            "fmt",
            {
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
                "id": 10035,
                "path": "Arguments"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 919,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1615: /// assert_eq!(output, \"Hello world!\");\n  1616: /// ```\n  1617: ///\n  1618: /// Please note that using [`write!`] might be preferable. Example:\n  1619: ///\n  1620: /// ```\n  1621: /// use std::fmt::Write;\n  1622: ///\n  1623: /// let mut output = String::new();\n  1624: /// write!(&mut output, \"Hello {}!\", \"world\")\n  1625: ///     .expect(\"Error occurred while trying to write in String\");\n  1626: /// assert_eq!(output, \"Hello world!\");\n  1627: /// ```\n  1628: ///\n  1629: /// [`write!`]: crate::write!\n  1630: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1631: pub fn write(output: &mut dyn Write, fmt: Arguments<'_>) -> Result {\n  1632:     if let Some(s) = fmt.as_str() {\n  1633:         return output.write_str(s);\n  1634:     }\n  1635: \n  1636:     let mut template = fmt.template;\n  1637:     let args = fmt.args;\n  1638: \n  1639:     let mut arg_index = 0;\n  1640: \n  1641:     // See comment on `fmt::Arguments` for the details of how the template is encoded.\n  1642: \n  1643:     // This must match the encoding from `expand_format_args` in\n  1644:     // compiler/rustc_ast_lowering/src/format.rs.\n  1645:     loop {\n  1646:         // SAFETY: We can assume the template is valid.\n  1647:         let n = unsafe {",
    "nanvix_source": "  1621: /// use std::fmt::Write;\n  1622: ///\n  1623: /// let mut output = String::new();\n  1624: /// write!(&mut output, \"Hello {}!\", \"world\")\n  1625: ///     .expect(\"Error occurred while trying to write in String\");\n  1626: /// assert_eq!(output, \"Hello world!\");\n  1627: /// ```\n  1628: ///\n  1629: /// [`write!`]: crate::write!\n  1630: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1631: pub fn write(output: &mut dyn Write, fmt: Arguments<'_>) -> Result {\n  1632:     if let Some(s) = fmt.as_str() {\n  1633:         return output.write_str(s);\n  1634:     }\n  1635: \n  1636:     let mut template = fmt.template;\n  1637:     let args = fmt.args;\n  1638: \n  1639:     let mut arg_index = 0;\n  1640: \n  1641:     // See comment on `fmt::Arguments` for the details of how the template is encoded.",
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
