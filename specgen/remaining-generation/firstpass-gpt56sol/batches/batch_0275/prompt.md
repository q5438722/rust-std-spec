For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::or_else",
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
    "nanvix_source": "  1547:     /// fn err(x: u32) -> Result<u32, u32> { Err(x) }\n  1548:     ///\n  1549:     /// assert_eq!(Ok(2).or_else(sq).or_else(sq), Ok(2));\n  1550:     /// assert_eq!(Ok(2).or_else(err).or_else(sq), Ok(2));\n  1551:     /// assert_eq!(Err(3).or_else(sq).or_else(err), Ok(9));\n  1552:     /// assert_eq!(Err(3).or_else(err).or_else(err), Err(3));\n  1553:     /// ```\n  1554:     #[inline]\n  1555:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1556:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1557:     pub const fn or_else<F, O>(self, op: O) -> Result<T, F>\n  1558:     where\n  1559:         O: [const] FnOnce(E) -> Result<T, F> + [const] Destruct,\n  1560:     {\n  1561:         match self {\n  1562:             Ok(t) => Ok(t),\n  1563:             Err(e) => op(e),\n  1564:         }\n  1565:     }\n  1566: \n  1567:     /// Returns the contained [`Ok`] value or a provided default.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::transpose",
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
    "nanvix_source": "  1809:     /// struct SomeErr;\n  1810:     ///\n  1811:     /// let x: Result<Option<i32>, SomeErr> = Ok(Some(5));\n  1812:     /// let y: Option<Result<i32, SomeErr>> = Some(Ok(5));\n  1813:     /// assert_eq!(x.transpose(), y);\n  1814:     /// ```\n  1815:     #[inline]\n  1816:     #[stable(feature = \"transpose_result\", since = \"1.33.0\")]\n  1817:     #[rustc_const_stable(feature = \"const_result\", since = \"1.83.0\")]\n  1818:     #[rustc_allow_const_fn_unstable(const_precise_live_drops)]\n  1819:     pub const fn transpose(self) -> Option<Result<T, E>> {\n  1820:         match self {\n  1821:             Ok(Some(x)) => Some(Ok(x)),\n  1822:             Ok(None) => None,\n  1823:             Err(e) => Some(Err(e)),\n  1824:         }\n  1825:     }\n  1826: }\n  1827: \n  1828: impl<T, E> Result<Result<T, E>, E> {\n  1829:     /// Converts from `Result<Result<T, E>, E>` to `Result<T, E>`",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap",
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
    "nanvix_source": "  1215:     /// assert_eq!(x.unwrap(), 2);\n  1216:     /// ```\n  1217:     ///\n  1218:     /// ```should_panic\n  1219:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1220:     /// x.unwrap(); // panics with `emergency failure`\n  1221:     /// ```\n  1222:     #[inline(always)]\n  1223:     #[track_caller]\n  1224:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1225:     pub fn unwrap(self) -> T\n  1226:     where\n  1227:         E: fmt::Debug,\n  1228:     {\n  1229:         match self {\n  1230:             Ok(t) => t,\n  1231:             Err(e) => unwrap_failed(\"called `Result::unwrap()` on an `Err` value\", &e),\n  1232:         }\n  1233:     }\n  1234: \n  1235:     /// Returns the contained [`Ok`] value or a default",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap_err",
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
    "nanvix_source": "  1312:     /// x.unwrap_err(); // panics with `2`\n  1313:     /// ```\n  1314:     ///\n  1315:     /// ```\n  1316:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1317:     /// assert_eq!(x.unwrap_err(), \"emergency failure\");\n  1318:     /// ```\n  1319:     #[inline]\n  1320:     #[track_caller]\n  1321:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1322:     pub fn unwrap_err(self) -> E\n  1323:     where\n  1324:         T: fmt::Debug,\n  1325:     {\n  1326:         match self {\n  1327:             Ok(t) => unwrap_failed(\"called `Result::unwrap_err()` on an `Ok` value\", &t),\n  1328:             Err(e) => e,\n  1329:         }\n  1330:     }\n  1331: \n  1332:     /// Returns the contained [`Ok`] value, but never panics.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap_err_unchecked",
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
    "nanvix_source": "  1674:     /// ```\n  1675:     ///\n  1676:     /// ```\n  1677:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1678:     /// assert_eq!(unsafe { x.unwrap_err_unchecked() }, \"emergency failure\");\n  1679:     /// ```\n  1680:     #[inline]\n  1681:     #[track_caller]\n  1682:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1683:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1684:     pub const unsafe fn unwrap_err_unchecked(self) -> E\n  1685:     where\n  1686:         T: [const] Destruct,\n  1687:         E: [const] Destruct,\n  1688:     {\n  1689:         match self {\n  1690:             // SAFETY: the safety contract must be upheld by the caller.\n  1691:             Ok(_) => unsafe { hint::unreachable_unchecked() },\n  1692:             Err(e) => e,\n  1693:         }\n  1694:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap_or",
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
    "nanvix_source": "  1578:     /// let default = 2;\n  1579:     /// let x: Result<u32, &str> = Ok(9);\n  1580:     /// assert_eq!(x.unwrap_or(default), 9);\n  1581:     ///\n  1582:     /// let x: Result<u32, &str> = Err(\"error\");\n  1583:     /// assert_eq!(x.unwrap_or(default), default);\n  1584:     /// ```\n  1585:     #[inline]\n  1586:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1587:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1588:     pub const fn unwrap_or(self, default: T) -> T\n  1589:     where\n  1590:         T: [const] Destruct,\n  1591:         E: [const] Destruct,\n  1592:     {\n  1593:         match self {\n  1594:             Ok(t) => t,\n  1595:             Err(_) => default,\n  1596:         }\n  1597:     }\n  1598: ",
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
