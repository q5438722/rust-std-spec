For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::path::is_separator",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
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
      "name": "is_separator",
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
            "c",
            {
              "primitive": "char"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   254: ////////////////////////////////////////////////////////////////////////////////\n   255: \n   256: /// Determines whether the character is one of the permitted path\n   257: /// separators for the current platform.\n   258: ///\n   259: /// # Examples\n   260: ///\n   261: /// ```\n   262: /// use std::path;\n   263: ///\n   264: /// assert!(path::is_separator('/')); // '/' works for both Unix and Windows\n   265: /// assert!(!path::is_separator('\u2764'));\n   266: /// ```\n   267: #[must_use]\n   268: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   269: #[rustc_const_unstable(feature = \"const_path_separators\", issue = \"153106\")]\n   270: pub const fn is_separator(c: char) -> bool {\n   271:     c.is_ascii() && is_sep_byte(c as u8)\n   272: }\n   273: \n   274: /// All path separators recognized on the current platform, represented as [`char`]s; for example,\n   275: /// this is `&['/'][..]` on Unix and `&['\\\\', '/'][..]` on Windows. The [primary\n   276: /// separator](MAIN_SEPARATOR) is always element 0 of the slice.\n   277: #[unstable(feature = \"const_path_separators\", issue = \"153106\")]\n   278: pub const SEPARATORS: &[char] = crate::sys::path::SEPARATORS;\n   279: \n   280: /// All path separators recognized on the current platform, represented as [`&str`]s; for example,\n   281: /// this is `&[\"/\"][..]` on Unix and `&[\"\\\\\", \"/\"][..]` on Windows. The [primary\n   282: /// separator](MAIN_SEPARATOR_STR) is always element 0 of the slice.\n   283: #[unstable(feature = \"const_path_separators\", issue = \"153106\")]\n   284: pub const SEPARATORS_STR: &[&str] = crate::sys::path::SEPARATORS_STR;\n   285: \n   286: /// The primary separator of path components for the current platform, represented as a [`char`];",
    "nanvix_source": "   260: ///\n   261: /// ```\n   262: /// use std::path;\n   263: ///\n   264: /// assert!(path::is_separator('/')); // '/' works for both Unix and Windows\n   265: /// assert!(!path::is_separator('\u2764'));\n   266: /// ```\n   267: #[must_use]\n   268: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   269: #[rustc_const_unstable(feature = \"const_path_separators\", issue = \"153106\")]\n   270: pub const fn is_separator(c: char) -> bool {\n   271:     c.is_ascii() && is_sep_byte(c as u8)\n   272: }\n   273: \n   274: /// All path separators recognized on the current platform, represented as [`char`]s; for example,\n   275: /// this is `&['/'][..]` on Unix and `&['\\\\', '/'][..]` on Windows. The [primary\n   276: /// separator](MAIN_SEPARATOR) is always element 0 of the slice.\n   277: #[unstable(feature = \"const_path_separators\", issue = \"153106\")]\n   278: pub const SEPARATORS: &[char] = crate::sys::path::SEPARATORS;\n   279: \n   280: /// All path separators recognized on the current platform, represented as [`&str`]s; for example,",
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
