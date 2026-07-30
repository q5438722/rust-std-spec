For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::expect",
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
    "nanvix_source": "  1167:     /// variable should be set by blah\" or \"the given binary should be available\n  1168:     /// and executable by the current user\".\n  1169:     ///\n  1170:     /// For more detail on expect message styles and the reasoning behind our recommendation please\n  1171:     /// refer to the section on [\"Common Message\n  1172:     /// Styles\"](../../std/error/index.html#common-message-styles) in the\n  1173:     /// [`std::error`](../../std/error/index.html) module docs.\n  1174:     #[inline]\n  1175:     #[track_caller]\n  1176:     #[stable(feature = \"result_expect\", since = \"1.4.0\")]\n  1177:     pub fn expect(self, msg: &str) -> T\n  1178:     where\n  1179:         E: fmt::Debug,\n  1180:     {\n  1181:         match self {\n  1182:             Ok(t) => t,\n  1183:             Err(e) => unwrap_failed(msg, &e),\n  1184:         }\n  1185:     }\n  1186: \n  1187:     /// Returns the contained [`Ok`] value, consuming the `self` value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::expect_err",
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
    "nanvix_source": "  1281:     ///\n  1282:     /// # Examples\n  1283:     ///\n  1284:     /// ```should_panic\n  1285:     /// let x: Result<u32, &str> = Ok(10);\n  1286:     /// x.expect_err(\"Testing expect_err\"); // panics with `Testing expect_err: 10`\n  1287:     /// ```\n  1288:     #[inline]\n  1289:     #[track_caller]\n  1290:     #[stable(feature = \"result_expect_err\", since = \"1.17.0\")]\n  1291:     pub fn expect_err(self, msg: &str) -> E\n  1292:     where\n  1293:         T: fmt::Debug,\n  1294:     {\n  1295:         match self {\n  1296:             Ok(t) => unwrap_failed(msg, &t),\n  1297:             Err(e) => e,\n  1298:         }\n  1299:     }\n  1300: \n  1301:     /// Returns the contained [`Err`] value, consuming the `self` value.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::flatten",
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
    "nanvix_source": "  1845:     ///\n  1846:     /// ```\n  1847:     /// let x: Result<Result<Result<&'static str, u32>, u32>, u32> = Ok(Ok(Ok(\"hello\")));\n  1848:     /// assert_eq!(Ok(Ok(\"hello\")), x.flatten());\n  1849:     /// assert_eq!(Ok(\"hello\"), x.flatten().flatten());\n  1850:     /// ```\n  1851:     #[inline]\n  1852:     #[stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1853:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1854:     #[rustc_const_stable(feature = \"result_flattening\", since = \"1.89.0\")]\n  1855:     pub const fn flatten(self) -> Result<T, E> {\n  1856:         // FIXME(const-hack): could be written with `and_then`\n  1857:         match self {\n  1858:             Ok(inner) => inner,\n  1859:             Err(e) => Err(e),\n  1860:         }\n  1861:     }\n  1862: }\n  1863: \n  1864: // This is a separate function to reduce the code size of the methods\n  1865: #[cfg(not(panic = \"immediate-abort\"))]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::inspect",
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
    "nanvix_source": "   976:     /// ```\n   977:     /// let x: u8 = \"4\"\n   978:     ///     .parse::<u8>()\n   979:     ///     .inspect(|x| println!(\"original: {x}\"))\n   980:     ///     .map(|x| x.pow(3))\n   981:     ///     .expect(\"failed to parse number\");\n   982:     /// ```\n   983:     #[inline]\n   984:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n   985:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n   986:     pub const fn inspect<F>(self, f: F) -> Self\n   987:     where\n   988:         F: [const] FnOnce(&T) + [const] Destruct,\n   989:     {\n   990:         if let Ok(ref t) = self {\n   991:             f(t);\n   992:         }\n   993: \n   994:         self\n   995:     }\n   996: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::inspect_err",
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
    "nanvix_source": "  1004:     /// use std::{fs, io};\n  1005:     ///\n  1006:     /// fn read() -> io::Result<String> {\n  1007:     ///     fs::read_to_string(\"address.txt\")\n  1008:     ///         .inspect_err(|e| eprintln!(\"failed to read file: {e}\"))\n  1009:     /// }\n  1010:     /// ```\n  1011:     #[inline]\n  1012:     #[stable(feature = \"result_option_inspect\", since = \"1.76.0\")]\n  1013:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1014:     pub const fn inspect_err<F>(self, f: F) -> Self\n  1015:     where\n  1016:         F: [const] FnOnce(&E) + [const] Destruct,\n  1017:     {\n  1018:         if let Err(ref e) = self {\n  1019:             f(e);\n  1020:         }\n  1021: \n  1022:         self\n  1023:     }\n  1024: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::is_err",
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
    "nanvix_source": "   636:     /// let x: Result<i32, &str> = Ok(-3);\n   637:     /// assert_eq!(x.is_err(), false);\n   638:     ///\n   639:     /// let x: Result<i32, &str> = Err(\"Some error message\");\n   640:     /// assert_eq!(x.is_err(), true);\n   641:     /// ```\n   642:     #[must_use = \"if you intended to assert that this is err, consider `.unwrap_err()` instead\"]\n   643:     #[rustc_const_stable(feature = \"const_result_basics\", since = \"1.48.0\")]\n   644:     #[inline]\n   645:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   646:     pub const fn is_err(&self) -> bool {\n   647:         !self.is_ok()\n   648:     }\n   649: \n   650:     /// Returns `true` if the result is [`Err`] and the value inside of it matches a predicate.\n   651:     ///\n   652:     /// # Examples\n   653:     ///\n   654:     /// ```\n   655:     /// use std::io::{Error, ErrorKind};\n   656:     ///",
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
