For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::map_err",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   950:     ///\n   951:     /// let x: Result<u32, u32> = Ok(2);\n   952:     /// assert_eq!(x.map_err(stringify), Ok(2));\n   953:     ///\n   954:     /// let x: Result<u32, u32> = Err(13);\n   955:     /// assert_eq!(x.map_err(stringify), Err(\"error code: 13\".to_string()));\n   956:     /// ```\n   957:     #[inline]\n   958:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   959:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   960:     pub const fn map_err<F, O>(self, op: O) -> Result<T, F>\n   961:     where\n   962:         O: [const] FnOnce(E) -> F + [const] Destruct,\n   963:     {\n   964:         match self {\n   965:             Ok(t) => Ok(t),\n   966:             Err(e) => Err(op(e)),\n   967:         }\n   968:     }\n   969: \n   970:     /// Calls a function with a reference to the contained value if [`Ok`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::map_or",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   853:     /// let x: Result<_, &str> = Ok(\"foo\");\n   854:     /// assert_eq!(x.map_or(42, |v| v.len()), 3);\n   855:     ///\n   856:     /// let x: Result<&str, _> = Err(\"bar\");\n   857:     /// assert_eq!(x.map_or(42, |v| v.len()), 42);\n   858:     /// ```\n   859:     #[inline]\n   860:     #[stable(feature = \"result_map_or\", since = \"1.41.0\")]\n   861:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   862:     #[must_use = \"if you don't need the returned value, use `if let` instead\"]\n   863:     pub const fn map_or<U, F>(self, default: U, f: F) -> U\n   864:     where\n   865:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   866:         T: [const] Destruct,\n   867:         E: [const] Destruct,\n   868:         U: [const] Destruct,\n   869:     {\n   870:         match self {\n   871:             Ok(t) => f(t),\n   872:             Err(_) => default,\n   873:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::map_or_default",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   916:     /// let y: Result<&str, _> = Err(\"bar\");\n   917:     ///\n   918:     /// assert_eq!(x.map_or_default(|x| x.len()), 3);\n   919:     /// assert_eq!(y.map_or_default(|y| y.len()), 0);\n   920:     /// ```\n   921:     ///\n   922:     /// [default value]: Default::default\n   923:     #[inline]\n   924:     #[stable(feature = \"result_option_map_or_default\", since = \"CURRENT_RUSTC_VERSION\")]\n   925:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   926:     pub const fn map_or_default<U, F>(self, f: F) -> U\n   927:     where\n   928:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   929:         U: [const] Default,\n   930:         T: [const] Destruct,\n   931:         E: [const] Destruct,\n   932:     {\n   933:         match self {\n   934:             Ok(t) => f(t),\n   935:             Err(_) => U::default(),\n   936:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::map_or_else",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   887:     ///\n   888:     /// let x : Result<_, &str> = Ok(\"foo\");\n   889:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 3);\n   890:     ///\n   891:     /// let x : Result<&str, _> = Err(\"bar\");\n   892:     /// assert_eq!(x.map_or_else(|e| k * 2, |v| v.len()), 42);\n   893:     /// ```\n   894:     #[inline]\n   895:     #[stable(feature = \"result_map_or_else\", since = \"1.41.0\")]\n   896:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   897:     pub const fn map_or_else<U, D, F>(self, default: D, f: F) -> U\n   898:     where\n   899:         D: [const] FnOnce(E) -> U + [const] Destruct,\n   900:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   901:     {\n   902:         match self {\n   903:             Ok(t) => f(t),\n   904:             Err(e) => default(e),\n   905:         }\n   906:     }\n   907: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::ok",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   698:     /// let x: Result<u32, &str> = Ok(2);\n   699:     /// assert_eq!(x.ok(), Some(2));\n   700:     ///\n   701:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   702:     /// assert_eq!(x.ok(), None);\n   703:     /// ```\n   704:     #[inline]\n   705:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   706:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   707:     #[rustc_diagnostic_item = \"result_ok_method\"]\n   708:     pub const fn ok(self) -> Option<T>\n   709:     where\n   710:         T: [const] Destruct,\n   711:         E: [const] Destruct,\n   712:     {\n   713:         match self {\n   714:             Ok(x) => Some(x),\n   715:             Err(_) => None,\n   716:         }\n   717:     }\n   718: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::or",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "  1516:     /// let y: Result<u32, &str> = Err(\"late error\");\n  1517:     /// assert_eq!(x.or(y), Err(\"late error\"));\n  1518:     ///\n  1519:     /// let x: Result<u32, &str> = Ok(2);\n  1520:     /// let y: Result<u32, &str> = Ok(100);\n  1521:     /// assert_eq!(x.or(y), Ok(2));\n  1522:     /// ```\n  1523:     #[inline]\n  1524:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1525:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1526:     pub const fn or<F>(self, res: Result<T, F>) -> Result<T, F>\n  1527:     where\n  1528:         T: [const] Destruct,\n  1529:         E: [const] Destruct,\n  1530:         F: [const] Destruct,\n  1531:     {\n  1532:         match self {\n  1533:             Ok(v) => Ok(v),\n  1534:             Err(_) => res,\n  1535:         }\n  1536:     }",
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
