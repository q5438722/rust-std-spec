For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Seek::stream_position",
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
    "nanvix_source": "   135:     ///\n   136:     ///     let before = f.stream_position()?;\n   137:     ///     f.read_line(&mut String::new())?;\n   138:     ///     let after = f.stream_position()?;\n   139:     ///\n   140:     ///     println!(\"The first line was {} bytes long\", after - before);\n   141:     ///     Ok(())\n   142:     /// }\n   143:     /// ```\n   144:     #[stable(feature = \"seek_convenience\", since = \"1.51.0\")]\n   145:     fn stream_position(&mut self) -> Result<u64> {\n   146:         self.seek(SeekFrom::Current(0))\n   147:     }\n   148: \n   149:     /// Seeks relative to the current position.\n   150:     ///\n   151:     /// This is equivalent to `self.seek(SeekFrom::Current(offset))` but\n   152:     /// doesn't return the new position which can allow some implementations\n   153:     /// such as `BufReader` to perform more efficient seeks.\n   154:     ///\n   155:     /// # Example",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Take::get_mut",
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
    "nanvix_source": "   470:     ///\n   471:     ///     let mut buffer = [0; 5];\n   472:     ///     let mut handle = file.take(5);\n   473:     ///     handle.read(&mut buffer)?;\n   474:     ///\n   475:     ///     let file = handle.get_mut();\n   476:     ///     Ok(())\n   477:     /// }\n   478:     /// ```\n   479:     #[stable(feature = \"more_io_inner_methods\", since = \"1.20.0\")]\n   480:     pub fn get_mut(&mut self) -> &mut T {\n   481:         &mut self.inner\n   482:     }\n   483: }\n   484: \n   485: #[stable(feature = \"seek_io_take\", since = \"1.89.0\")]\n   486: impl<T: Seek> Seek for Take<T> {\n   487:     fn seek(&mut self, pos: SeekFrom) -> Result<u64> {\n   488:         let new_position = match pos {\n   489:             SeekFrom::Start(v) => Some(v),\n   490:             SeekFrom::Current(v) => self.position().checked_add_signed(v),",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Take::get_ref",
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
    "nanvix_source": "   441:     ///\n   442:     ///     let mut buffer = [0; 5];\n   443:     ///     let mut handle = file.take(5);\n   444:     ///     handle.read(&mut buffer)?;\n   445:     ///\n   446:     ///     let file = handle.get_ref();\n   447:     ///     Ok(())\n   448:     /// }\n   449:     /// ```\n   450:     #[stable(feature = \"more_io_inner_methods\", since = \"1.20.0\")]\n   451:     pub fn get_ref(&self) -> &T {\n   452:         &self.inner\n   453:     }\n   454: \n   455:     /// Gets a mutable reference to the underlying reader.\n   456:     ///\n   457:     /// Care should be taken to avoid modifying the internal I/O state of the\n   458:     /// underlying reader as doing so may corrupt the internal limit of this\n   459:     /// `Take`.\n   460:     ///\n   461:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Take::into_inner",
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
    "nanvix_source": "   412:     ///\n   413:     ///     let mut buffer = [0; 5];\n   414:     ///     let mut handle = file.take(5);\n   415:     ///     handle.read(&mut buffer)?;\n   416:     ///\n   417:     ///     let file = handle.into_inner();\n   418:     ///     Ok(())\n   419:     /// }\n   420:     /// ```\n   421:     #[stable(feature = \"io_take_into_inner\", since = \"1.15.0\")]\n   422:     pub fn into_inner(self) -> T {\n   423:         self.inner\n   424:     }\n   425: \n   426:     /// Gets a reference to the underlying reader.\n   427:     ///\n   428:     /// Care should be taken to avoid modifying the internal I/O state of the\n   429:     /// underlying reader as doing so may corrupt the internal limit of this\n   430:     /// `Take`.\n   431:     ///\n   432:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Take::limit",
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
    "nanvix_source": "   351:     ///     let f = File::open(\"foo.txt\")?;\n   352:     ///\n   353:     ///     // read at most five bytes\n   354:     ///     let handle = f.take(5);\n   355:     ///\n   356:     ///     println!(\"limit: {}\", handle.limit());\n   357:     ///     Ok(())\n   358:     /// }\n   359:     /// ```\n   360:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   361:     pub fn limit(&self) -> u64 {\n   362:         self.limit\n   363:     }\n   364: \n   365:     /// Returns the number of bytes read so far.\n   366:     #[unstable(feature = \"seek_io_take_position\", issue = \"97227\")]\n   367:     #[inline]\n   368:     pub fn position(&self) -> u64 {\n   369:         self.len - self.limit\n   370:     }\n   371: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Take::set_limit",
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
    "nanvix_source": "   386:     ///\n   387:     ///     // read at most five bytes\n   388:     ///     let mut handle = f.take(5);\n   389:     ///     handle.set_limit(10);\n   390:     ///\n   391:     ///     assert_eq!(handle.limit(), 10);\n   392:     ///     Ok(())\n   393:     /// }\n   394:     /// ```\n   395:     #[stable(feature = \"take_set_limit\", since = \"1.27.0\")]\n   396:     pub fn set_limit(&mut self, limit: u64) {\n   397:         self.len = limit;\n   398:         self.limit = limit;\n   399:     }\n   400: \n   401:     /// Consumes the `Take`, returning the wrapped reader.\n   402:     ///\n   403:     /// # Examples\n   404:     ///\n   405:     /// ```no_run\n   406:     /// use std::io;",
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
