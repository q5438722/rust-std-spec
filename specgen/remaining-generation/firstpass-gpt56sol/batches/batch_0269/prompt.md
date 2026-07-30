For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Error::get_ref",
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
    "nanvix_source": "   348:     /// fn main() {\n   349:     ///     // Will print \"No inner error\".\n   350:     ///     print_error(&Error::last_os_error());\n   351:     ///     // Will print \"Inner error: ...\".\n   352:     ///     print_error(&Error::new(ErrorKind::Other, \"oh no!\"));\n   353:     /// }\n   354:     /// ```\n   355:     #[stable(feature = \"io_error_inner\", since = \"1.3.0\")]\n   356:     #[must_use]\n   357:     #[inline]\n   358:     pub fn get_ref(&self) -> Option<&(dyn error::Error + Send + Sync + 'static)> {\n   359:         match self.repr.data() {\n   360:             ErrorData::Os(..) => None,\n   361:             ErrorData::Simple(..) => None,\n   362:             ErrorData::SimpleMessage(..) => None,\n   363:             ErrorData::Custom(c) => Some(c.error_ref()),\n   364:         }\n   365:     }\n   366: \n   367:     /// Returns a mutable reference to the inner error wrapped by this error\n   368:     /// (if any).",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Error::kind",
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
    "nanvix_source": "   462:     ///     // As no error has (visibly) occurred, this may print anything!\n   463:     ///     // It likely prints a placeholder for unidentified (non-)errors.\n   464:     ///     print_error(Error::last_os_error());\n   465:     ///     // Will print \"AddrInUse\".\n   466:     ///     print_error(Error::new(ErrorKind::AddrInUse, \"oh no!\"));\n   467:     /// }\n   468:     /// ```\n   469:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   470:     #[must_use]\n   471:     #[inline]\n   472:     pub fn kind(&self) -> ErrorKind {\n   473:         match self.repr.data() {\n   474:             ErrorData::Os(code) => decode_error_kind(code),\n   475:             ErrorData::Custom(c) => c.kind,\n   476:             ErrorData::Simple(kind) => kind,\n   477:             ErrorData::SimpleMessage(m) => m.kind,\n   478:         }\n   479:     }\n   480: \n   481:     #[unstable(feature = \"core_io_internals\", reason = \"exposed only for libstd\", issue = \"none\")]\n   482:     #[doc(hidden)]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Error::raw_os_error",
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
    "nanvix_source": "   309:     /// fn main() {\n   310:     ///     // Will print \"raw OS error: ...\".\n   311:     ///     print_os_error(&Error::last_os_error());\n   312:     ///     // Will print \"Not an OS error\".\n   313:     ///     print_os_error(&Error::new(ErrorKind::Other, \"oh no!\"));\n   314:     /// }\n   315:     /// ```\n   316:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   317:     #[must_use]\n   318:     #[inline]\n   319:     pub fn raw_os_error(&self) -> Option<RawOsError> {\n   320:         match self.repr.data() {\n   321:             ErrorData::Os(i) => Some(i),\n   322:             ErrorData::Custom(..) => None,\n   323:             ErrorData::Simple(..) => None,\n   324:             ErrorData::SimpleMessage(..) => None,\n   325:         }\n   326:     }\n   327: \n   328:     /// Returns a reference to the inner error wrapped by this error (if any).\n   329:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::IoSlice::advance",
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
    "nanvix_source": "   231:     ///\n   232:     /// let data = [1; 8];\n   233:     /// let mut buf = IoSlice::new(&data);\n   234:     ///\n   235:     /// // Mark 3 bytes as read.\n   236:     /// buf.advance(3);\n   237:     /// assert_eq!(buf.deref(), [1; 5].as_ref());\n   238:     /// ```\n   239:     #[stable(feature = \"io_slice_advance\", since = \"1.81.0\")]\n   240:     #[inline]\n   241:     pub fn advance(&mut self, n: usize) {\n   242:         self.0.advance(n)\n   243:     }\n   244: \n   245:     /// Advance a slice of slices.\n   246:     ///\n   247:     /// Shrinks the slice to remove any `IoSlice`s that are fully advanced over.\n   248:     /// If the cursor ends up in the middle of an `IoSlice`, it is modified\n   249:     /// to start at that cursor.\n   250:     ///\n   251:     /// For example, if we have a slice of two 8-byte `IoSlice`s, and we advance by 10 bytes,",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::IoSlice::advance_slices",
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
    "nanvix_source": "   269:     ///     IoSlice::new(&buf2),\n   270:     ///     IoSlice::new(&buf3),\n   271:     /// ][..];\n   272:     ///\n   273:     /// // Mark 10 bytes as written.\n   274:     /// IoSlice::advance_slices(&mut bufs, 10);\n   275:     /// assert_eq!(bufs[0].deref(), [2; 14].as_ref());\n   276:     /// assert_eq!(bufs[1].deref(), [3; 8].as_ref());\n   277:     #[stable(feature = \"io_slice_advance\", since = \"1.81.0\")]\n   278:     #[inline]\n   279:     pub fn advance_slices(bufs: &mut &mut [IoSlice<'a>], n: usize) {\n   280:         // Number of buffers to remove.\n   281:         let mut remove = 0;\n   282:         // Remaining length before reaching n. This prevents overflow\n   283:         // that could happen if the length of slices in `bufs` were instead\n   284:         // accumulated. Those slice may be aliased and, if they are large\n   285:         // enough, their added length may overflow a `usize`.\n   286:         let mut left = n;\n   287:         for buf in bufs.iter() {\n   288:             if let Some(remainder) = left.checked_sub(buf.len()) {\n   289:                 left = remainder;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::IoSlice::new",
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
    "nanvix_source": "   203: \n   204: impl<'a> IoSlice<'a> {\n   205:     /// Creates a new `IoSlice` wrapping a byte slice.\n   206:     ///\n   207:     /// # Panics\n   208:     ///\n   209:     /// Panics on Windows if the slice is larger than 4GB.\n   210:     #[stable(feature = \"iovec\", since = \"1.36.0\")]\n   211:     #[must_use]\n   212:     #[inline]\n   213:     pub fn new(buf: &'a [u8]) -> IoSlice<'a> {\n   214:         IoSlice(repr::IoSlice::new(buf))\n   215:     }\n   216: \n   217:     /// Advance the internal cursor of the slice.\n   218:     ///\n   219:     /// Also see [`IoSlice::advance_slices`] to advance the cursors of multiple\n   220:     /// buffers.\n   221:     ///\n   222:     /// # Panics\n   223:     ///",
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
