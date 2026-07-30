For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::as_deref_mut",
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
      "reference_identity_vs_view",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "  1062:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1063:     ///\n  1064:     /// let mut i = 42;\n  1065:     /// let mut x: Result<String, u32> = Err(42);\n  1066:     /// let y: Result<&mut str, &mut u32> = Err(&mut i);\n  1067:     /// assert_eq!(x.as_deref_mut().map(|x| { x.make_ascii_uppercase(); x }), y);\n  1068:     /// ```\n  1069:     #[inline]\n  1070:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1071:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1072:     pub const fn as_deref_mut(&mut self) -> Result<&mut T::Target, &mut E>\n  1073:     where\n  1074:         T: [const] DerefMut,\n  1075:     {\n  1076:         self.as_mut().map(DerefMut::deref_mut)\n  1077:     }\n  1078: \n  1079:     /////////////////////////////////////////////////////////////////////////\n  1080:     // Iterator constructors\n  1081:     /////////////////////////////////////////////////////////////////////////\n  1082: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::as_mut",
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
      "reference_identity_vs_view",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   788:     /// mutate(&mut x);\n   789:     /// assert_eq!(x.unwrap(), 42);\n   790:     ///\n   791:     /// let mut x: Result<i32, i32> = Err(13);\n   792:     /// mutate(&mut x);\n   793:     /// assert_eq!(x.unwrap_err(), 0);\n   794:     /// ```\n   795:     #[inline]\n   796:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   797:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n   798:     pub const fn as_mut(&mut self) -> Result<&mut T, &mut E> {\n   799:         match *self {\n   800:             Ok(ref mut x) => Ok(x),\n   801:             Err(ref mut x) => Err(x),\n   802:         }\n   803:     }\n   804: \n   805:     /////////////////////////////////////////////////////////////////////////\n   806:     // Transforming contained values\n   807:     /////////////////////////////////////////////////////////////////////////\n   808: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::as_ref",
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
      "reference_identity_vs_view",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   758:     /// ```\n   759:     /// let x: Result<u32, &str> = Ok(2);\n   760:     /// assert_eq!(x.as_ref(), Ok(&2));\n   761:     ///\n   762:     /// let x: Result<u32, &str> = Err(\"Error\");\n   763:     /// assert_eq!(x.as_ref(), Err(&\"Error\"));\n   764:     /// ```\n   765:     #[inline]\n   766:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   767:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   768:     pub const fn as_ref(&self) -> Result<&T, &E> {\n   769:         match *self {\n   770:             Ok(ref x) => Ok(x),\n   771:             Err(ref x) => Err(x),\n   772:         }\n   773:     }\n   774: \n   775:     /// Converts from `&mut Result<T, E>` to `Result<&mut T, &mut E>`.\n   776:     ///\n   777:     /// # Examples\n   778:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::cloned",
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
      "multiple_rust_declarations_share_path",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "  1730:     ///\n  1731:     /// ```\n  1732:     /// let val = 12;\n  1733:     /// let x: Result<&i32, i32> = Ok(&val);\n  1734:     /// assert_eq!(x, Ok(&12));\n  1735:     /// let cloned = x.cloned();\n  1736:     /// assert_eq!(cloned, Ok(12));\n  1737:     /// ```\n  1738:     #[inline]\n  1739:     #[stable(feature = \"result_cloned\", since = \"1.59.0\")]\n  1740:     pub fn cloned(self) -> Result<T, E>\n  1741:     where\n  1742:         T: Clone,\n  1743:     {\n  1744:         self.map(|t| t.clone())\n  1745:     }\n  1746: }\n  1747: \n  1748: impl<T, E> Result<&mut T, E> {\n  1749:     /// Maps a `Result<&mut T, E>` to a `Result<T, E>` by copying the contents of the\n  1750:     /// `Ok` part.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::copied",
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
      "multiple_rust_declarations_share_path",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "  1704:     /// let val = 12;\n  1705:     /// let x: Result<&i32, i32> = Ok(&val);\n  1706:     /// assert_eq!(x, Ok(&12));\n  1707:     /// let copied = x.copied();\n  1708:     /// assert_eq!(copied, Ok(12));\n  1709:     /// ```\n  1710:     #[inline]\n  1711:     #[stable(feature = \"result_copied\", since = \"1.59.0\")]\n  1712:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1713:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1714:     pub const fn copied(self) -> Result<T, E>\n  1715:     where\n  1716:         T: Copy,\n  1717:     {\n  1718:         // FIXME(const-hack): this implementation, which sidesteps using `Result::map` since it's not const\n  1719:         // ready yet, should be reverted when possible to avoid code repetition\n  1720:         match self {\n  1721:             Ok(&v) => Ok(v),\n  1722:             Err(e) => Err(e),\n  1723:         }\n  1724:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::err",
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
    "nanvix_source": "   726:     /// ```\n   727:     /// let x: Result<u32, &str> = Ok(2);\n   728:     /// assert_eq!(x.err(), None);\n   729:     ///\n   730:     /// let x: Result<u32, &str> = Err(\"Nothing here\");\n   731:     /// assert_eq!(x.err(), Some(\"Nothing here\"));\n   732:     /// ```\n   733:     #[inline]\n   734:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   735:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   736:     pub const fn err(self) -> Option<E>\n   737:     where\n   738:         T: [const] Destruct,\n   739:         E: [const] Destruct,\n   740:     {\n   741:         match self {\n   742:             Ok(_) => None,\n   743:             Err(x) => Some(x),\n   744:         }\n   745:     }\n   746: ",
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
