For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::is_err_and",
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
    "nanvix_source": "   664:     /// assert_eq!(x.is_err_and(|x| x.kind() == ErrorKind::NotFound), false);\n   665:     ///\n   666:     /// let x: Result<u32, String> = Err(\"ownership\".to_string());\n   667:     /// assert_eq!(x.as_ref().is_err_and(|x| x.len() > 1), true);\n   668:     /// println!(\"still alive {:?}\", x);\n   669:     /// ```\n   670:     #[must_use]\n   671:     #[inline]\n   672:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   673:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   674:     pub const fn is_err_and<F>(self, f: F) -> bool\n   675:     where\n   676:         F: [const] FnOnce(E) -> bool + [const] Destruct,\n   677:         E: [const] Destruct,\n   678:         T: [const] Destruct,\n   679:     {\n   680:         match self {\n   681:             Ok(_) => false,\n   682:             Err(e) => f(e),\n   683:         }\n   684:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::is_ok",
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
    "nanvix_source": "   583:     /// let x: Result<i32, &str> = Ok(-3);\n   584:     /// assert_eq!(x.is_ok(), true);\n   585:     ///\n   586:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   587:     /// assert_eq!(x.is_ok(), false);\n   588:     /// ```\n   589:     #[must_use = \"if you intended to assert that this is ok, consider `.unwrap()` instead\"]\n   590:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   591:     #[inline]\n   592:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   593:     pub const fn is_ok(&self) -> bool {\n   594:         matches!(*self, Ok(_))\n   595:     }\n   596: \n   597:     /// Returns `true` if the result is [`Ok`] and the value inside of it matches a predicate.\n   598:     ///\n   599:     /// # Examples\n   600:     ///\n   601:     /// ```\n   602:     /// let x: Result<u32, &str> = Ok(2);\n   603:     /// assert_eq!(x.is_ok_and(|x| x > 1), true);",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::is_ok_and",
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
    "nanvix_source": "   609:     /// assert_eq!(x.is_ok_and(|x| x > 1), false);\n   610:     ///\n   611:     /// let x: Result<String, &str> = Ok(\"ownership\".to_string());\n   612:     /// assert_eq!(x.as_ref().is_ok_and(|x| x.len() > 1), true);\n   613:     /// println!(\"still alive {:?}\", x);\n   614:     /// ```\n   615:     #[must_use]\n   616:     #[inline]\n   617:     #[stable(feature = \"is_some_and\", since = \"1.70.0\")]\n   618:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   619:     pub const fn is_ok_and<F>(self, f: F) -> bool\n   620:     where\n   621:         F: [const] FnOnce(T) -> bool + [const] Destruct,\n   622:         T: [const] Destruct,\n   623:         E: [const] Destruct,\n   624:     {\n   625:         match self {\n   626:             Err(_) => false,\n   627:             Ok(x) => f(x),\n   628:         }\n   629:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::iter",
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
    "nanvix_source": "  1089:     /// ```\n  1090:     /// let x: Result<u32, &str> = Ok(7);\n  1091:     /// assert_eq!(x.iter().next(), Some(&7));\n  1092:     ///\n  1093:     /// let x: Result<u32, &str> = Err(\"nothing!\");\n  1094:     /// assert_eq!(x.iter().next(), None);\n  1095:     /// ```\n  1096:     #[inline]\n  1097:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1098:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1099:     pub const fn iter(&self) -> Iter<'_, T> {\n  1100:         Iter { inner: self.as_ref().ok() }\n  1101:     }\n  1102: \n  1103:     /// Returns a mutable iterator over the possibly contained value.\n  1104:     ///\n  1105:     /// The iterator yields one value if the result is [`Result::Ok`], otherwise none.\n  1106:     ///\n  1107:     /// # Examples\n  1108:     ///\n  1109:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::iter_mut",
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
    "nanvix_source": "  1113:     ///     None => {},\n  1114:     /// }\n  1115:     /// assert_eq!(x, Ok(40));\n  1116:     ///\n  1117:     /// let mut x: Result<u32, &str> = Err(\"nothing!\");\n  1118:     /// assert_eq!(x.iter_mut().next(), None);\n  1119:     /// ```\n  1120:     #[inline]\n  1121:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1122:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1123:     pub const fn iter_mut(&mut self) -> IterMut<'_, T> {\n  1124:         IterMut { inner: self.as_mut().ok() }\n  1125:     }\n  1126: \n  1127:     /////////////////////////////////////////////////////////////////////////\n  1128:     // Extract a value\n  1129:     /////////////////////////////////////////////////////////////////////////\n  1130: \n  1131:     /// Returns the contained [`Ok`] value, consuming the `self` value.\n  1132:     ///\n  1133:     /// Because this function may panic, its use is generally discouraged.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::map",
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
    "nanvix_source": "   821:     /// for num in line.lines() {\n   822:     ///     match num.parse::<i32>().map(|i| i * 2) {\n   823:     ///         Ok(n) => println!(\"{n}\"),\n   824:     ///         Err(..) => {}\n   825:     ///     }\n   826:     /// }\n   827:     /// ```\n   828:     #[inline]\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   831:     pub const fn map<U, F>(self, op: F) -> Result<U, E>\n   832:     where\n   833:         F: [const] FnOnce(T) -> U + [const] Destruct,\n   834:     {\n   835:         match self {\n   836:             Ok(t) => Ok(op(t)),\n   837:             Err(e) => Err(e),\n   838:         }\n   839:     }\n   840: \n   841:     /// Returns the provided default (if [`Err`]), or",
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
