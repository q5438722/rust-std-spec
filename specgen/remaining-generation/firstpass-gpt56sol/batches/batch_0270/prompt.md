For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::IoSliceMut::advance",
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
      "unit_return_variant",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "    72:     ///\n    73:     /// let mut data = [1; 8];\n    74:     /// let mut buf = IoSliceMut::new(&mut data);\n    75:     ///\n    76:     /// // Mark 3 bytes as read.\n    77:     /// buf.advance(3);\n    78:     /// assert_eq!(buf.deref(), [1; 5].as_ref());\n    79:     /// ```\n    80:     #[stable(feature = \"io_slice_advance\", since = \"1.81.0\")]\n    81:     #[inline]\n    82:     pub fn advance(&mut self, n: usize) {\n    83:         self.0.advance(n)\n    84:     }\n    85: \n    86:     /// Advance a slice of slices.\n    87:     ///\n    88:     /// Shrinks the slice to remove any `IoSliceMut`s that are fully advanced over.\n    89:     /// If the cursor ends up in the middle of an `IoSliceMut`, it is modified\n    90:     /// to start at that cursor.\n    91:     ///\n    92:     /// For example, if we have a slice of two 8-byte `IoSliceMut`s, and we advance by 10 bytes,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::IoSliceMut::advance_slices",
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
      "unit_return_variant",
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   111:     ///     IoSliceMut::new(&mut buf3),\n   112:     /// ][..];\n   113:     ///\n   114:     /// // Mark 10 bytes as read.\n   115:     /// IoSliceMut::advance_slices(&mut bufs, 10);\n   116:     /// assert_eq!(bufs[0].deref(), [2; 14].as_ref());\n   117:     /// assert_eq!(bufs[1].deref(), [3; 8].as_ref());\n   118:     /// ```\n   119:     #[stable(feature = \"io_slice_advance\", since = \"1.81.0\")]\n   120:     #[inline]\n   121:     pub fn advance_slices(bufs: &mut &mut [IoSliceMut<'a>], n: usize) {\n   122:         // Number of buffers to remove.\n   123:         let mut remove = 0;\n   124:         // Remaining length before reaching n.\n   125:         let mut left = n;\n   126:         for buf in bufs.iter() {\n   127:             if let Some(remainder) = left.checked_sub(buf.len()) {\n   128:                 left = remainder;\n   129:                 remove += 1;\n   130:             } else {\n   131:                 break;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::IoSliceMut::new",
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
    "nanvix_source": "    44: }\n    45: \n    46: impl<'a> IoSliceMut<'a> {\n    47:     /// Creates a new `IoSliceMut` wrapping a byte slice.\n    48:     ///\n    49:     /// # Panics\n    50:     ///\n    51:     /// Panics on Windows if the slice is larger than 4GB.\n    52:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n    53:     #[inline]\n    54:     pub fn new(buf: &'a mut [u8]) -> IoSliceMut<'a> {\n    55:         IoSliceMut(repr::IoSliceMut::new(buf))\n    56:     }\n    57: \n    58:     /// Advance the internal cursor of the slice.\n    59:     ///\n    60:     /// Also see [`IoSliceMut::advance_slices`] to advance the cursors of\n    61:     /// multiple buffers.\n    62:     ///\n    63:     /// # Panics\n    64:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::and",
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
    "nanvix_source": "  1430:     /// let y: Result<&str, &str> = Err(\"late error\");\n  1431:     /// assert_eq!(x.and(y), Err(\"not a 2\"));\n  1432:     ///\n  1433:     /// let x: Result<u32, &str> = Ok(2);\n  1434:     /// let y: Result<&str, &str> = Ok(\"different result type\");\n  1435:     /// assert_eq!(x.and(y), Ok(\"different result type\"));\n  1436:     /// ```\n  1437:     #[inline]\n  1438:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1439:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1440:     pub const fn and<U>(self, res: Result<U, E>) -> Result<U, E>\n  1441:     where\n  1442:         T: [const] Destruct,\n  1443:         E: [const] Destruct,\n  1444:         U: [const] Destruct,\n  1445:     {\n  1446:         match self {\n  1447:             Ok(_) => res,\n  1448:             Err(e) => Err(e),\n  1449:         }\n  1450:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::and_then",
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
    "nanvix_source": "  1476:     /// assert!(root_modified_time.is_ok());\n  1477:     ///\n  1478:     /// let should_fail = Path::new(\"/bad/path\").metadata().and_then(|md| md.modified());\n  1479:     /// assert!(should_fail.is_err());\n  1480:     /// assert_eq!(should_fail.unwrap_err().kind(), ErrorKind::NotFound);\n  1481:     /// ```\n  1482:     #[inline]\n  1483:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1484:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1485:     #[rustc_confusables(\"flat_map\", \"flatmap\")]\n  1486:     pub const fn and_then<U, F>(self, op: F) -> Result<U, E>\n  1487:     where\n  1488:         F: [const] FnOnce(T) -> Result<U, E> + [const] Destruct,\n  1489:     {\n  1490:         match self {\n  1491:             Ok(t) => op(t),\n  1492:             Err(e) => Err(e),\n  1493:         }\n  1494:     }\n  1495: \n  1496:     /// Returns `res` if the result is [`Err`], otherwise returns the [`Ok`] value of `self`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Result::as_deref",
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
    "nanvix_source": "  1034:     /// let y: Result<&str, &u32> = Ok(\"hello\");\n  1035:     /// assert_eq!(x.as_deref(), y);\n  1036:     ///\n  1037:     /// let x: Result<String, u32> = Err(42);\n  1038:     /// let y: Result<&str, &u32> = Err(&42);\n  1039:     /// assert_eq!(x.as_deref(), y);\n  1040:     /// ```\n  1041:     #[inline]\n  1042:     #[stable(feature = \"inner_deref\", since = \"1.47.0\")]\n  1043:     #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n  1044:     pub const fn as_deref(&self) -> Result<&T::Target, &E>\n  1045:     where\n  1046:         T: [const] Deref,\n  1047:     {\n  1048:         self.as_ref().map(Deref::deref)\n  1049:     }\n  1050: \n  1051:     /// Converts from `Result<T, E>` (or `&mut Result<T, E>`) to `Result<&mut <T as DerefMut>::Target, &mut E>`.\n  1052:     ///\n  1053:     /// Coerces the [`Ok`] variant of the original [`Result`] via [`DerefMut`](crate::ops::DerefMut)\n  1054:     /// and returns the new [`Result`].",
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
