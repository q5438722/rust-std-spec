For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Result::unwrap_or_default",
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
    "nanvix_source": "  1253:     ///\n  1254:     /// assert_eq!(1909, good_year);\n  1255:     /// assert_eq!(0, bad_year);\n  1256:     /// ```\n  1257:     ///\n  1258:     /// [`parse`]: str::parse\n  1259:     /// [`FromStr`]: crate::str::FromStr\n  1260:     #[inline]\n  1261:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1262:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1263:     pub const fn unwrap_or_default(self) -> T\n  1264:     where\n  1265:         T: [const] Default + [const] Destruct,\n  1266:         E: [const] Destruct,\n  1267:     {\n  1268:         match self {\n  1269:             Ok(x) => x,\n  1270:             Err(_) => Default::default(),\n  1271:         }\n  1272:     }\n  1273: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap_or_else",
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
    "nanvix_source": "  1604:     /// ```\n  1605:     /// fn count(x: &str) -> usize { x.len() }\n  1606:     ///\n  1607:     /// assert_eq!(Ok(2).unwrap_or_else(count), 2);\n  1608:     /// assert_eq!(Err(\"foo\").unwrap_or_else(count), 3);\n  1609:     /// ```\n  1610:     #[inline]\n  1611:     #[track_caller]\n  1612:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1613:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1614:     pub const fn unwrap_or_else<F>(self, op: F) -> T\n  1615:     where\n  1616:         F: [const] FnOnce(E) -> T + [const] Destruct,\n  1617:     {\n  1618:         match self {\n  1619:             Ok(t) => t,\n  1620:             Err(e) => op(e),\n  1621:         }\n  1622:     }\n  1623: \n  1624:     /// Returns the contained [`Ok`] value, consuming the `self` value,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::unwrap_unchecked",
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
    "nanvix_source": "  1638:     /// ```\n  1639:     ///\n  1640:     /// ```no_run\n  1641:     /// let x: Result<u32, &str> = Err(\"emergency failure\");\n  1642:     /// unsafe { x.unwrap_unchecked() }; // Undefined behavior!\n  1643:     /// ```\n  1644:     #[inline]\n  1645:     #[track_caller]\n  1646:     #[stable(feature = \"option_result_unwrap_unchecked\", since = \"1.58.0\")]\n  1647:     #[rustc_const_unstable(feature = \"const_result_unwrap_unchecked\", issue = \"148714\")]\n  1648:     pub const unsafe fn unwrap_unchecked(self) -> T {\n  1649:         match self {\n  1650:             Ok(t) => t,\n  1651:             Err(e) => {\n  1652:                 // FIXME(const-hack): to avoid E: const Destruct bound\n  1653:                 super::mem::forget(e);\n  1654:                 // SAFETY: the safety contract must be upheld by the caller.\n  1655:                 unsafe { hint::unreachable_unchecked() }\n  1656:             }\n  1657:         }\n  1658:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Seek::rewind",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "    67:     /// let hello = \"Hello!\\n\";\n    68:     /// write!(f, \"{hello}\")?;\n    69:     /// f.rewind()?;\n    70:     ///\n    71:     /// let mut buf = String::new();\n    72:     /// f.read_to_string(&mut buf)?;\n    73:     /// assert_eq!(&buf, hello);\n    74:     /// # std::io::Result::Ok(())\n    75:     /// ```\n    76:     #[stable(feature = \"seek_rewind\", since = \"1.55.0\")]\n    77:     fn rewind(&mut self) -> Result<()> {\n    78:         self.seek(SeekFrom::Start(0))?;\n    79:         Ok(())\n    80:     }\n    81: \n    82:     /// Returns the length of this stream (in bytes).\n    83:     ///\n    84:     /// The default implementation uses up to three seek operations. If this\n    85:     /// method returns successfully, the seek position is unchanged (i.e. the\n    86:     /// position before calling this method is the same as afterwards).\n    87:     /// However, if this method returns an error, the seek position is",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Seek::seek",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "    36:     /// this method returns the new position from the start of the stream.\n    37:     /// That position can be used later with [`SeekFrom::Start`].\n    38:     ///\n    39:     /// # Errors\n    40:     ///\n    41:     /// Seeking can fail, for example because it might involve flushing a buffer.\n    42:     ///\n    43:     /// Seeking to a negative offset is considered an error.\n    44:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    45:     fn seek(&mut self, pos: SeekFrom) -> Result<u64>;\n    46: \n    47:     /// Rewind to the beginning of a stream.\n    48:     ///\n    49:     /// This is a convenience method, equivalent to `seek(SeekFrom::Start(0))`.\n    50:     ///\n    51:     /// # Errors\n    52:     ///\n    53:     /// Rewinding can fail, for example because it might involve flushing a buffer.\n    54:     ///\n    55:     /// # Example\n    56:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Seek::seek_relative",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   161:     /// };\n   162:     ///\n   163:     /// fn main() -> io::Result<()> {\n   164:     ///     let mut f = File::open(\"foo.txt\")?;\n   165:     ///     f.seek_relative(10)?;\n   166:     ///     assert_eq!(f.stream_position()?, 10);\n   167:     ///     Ok(())\n   168:     /// }\n   169:     /// ```\n   170:     #[stable(feature = \"seek_seek_relative\", since = \"1.80.0\")]\n   171:     fn seek_relative(&mut self, offset: i64) -> Result<()> {\n   172:         self.seek(SeekFrom::Current(offset))?;\n   173:         Ok(())\n   174:     }\n   175: }\n   176: \n   177: /// The default implementation of [`Seek::stream_len`].\n   178: /// This may be desirable in `libstd` where the default implementation is desirable,\n   179: /// but additional work needs to be done before or after.\n   180: #[doc(hidden)]\n   181: #[unstable(feature = \"core_io_internals\", reason = \"exposed only for libstd\", issue = \"none\")]",
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
