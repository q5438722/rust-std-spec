For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::Cursor::get_ref",
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
    "nanvix_source": "   127:     /// use std::io::Cursor;\n   128:     ///\n   129:     /// let buff = Cursor::new(Vec::new());\n   130:     /// # fn force_inference(_: &Cursor<Vec<u8>>) {}\n   131:     /// # force_inference(&buff);\n   132:     ///\n   133:     /// let reference = buff.get_ref();\n   134:     /// ```\n   135:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   136:     #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n   137:     pub const fn get_ref(&self) -> &T {\n   138:         &self.inner\n   139:     }\n   140: \n   141:     /// Gets a mutable reference to the underlying value in this cursor.\n   142:     ///\n   143:     /// Care should be taken to avoid modifying the internal I/O state of the\n   144:     /// underlying value as it may corrupt this cursor's position.\n   145:     ///\n   146:     /// # Examples\n   147:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Cursor::into_inner",
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
    "nanvix_source": "   108:     /// ```\n   109:     /// use std::io::Cursor;\n   110:     ///\n   111:     /// let buff = Cursor::new(Vec::new());\n   112:     /// # fn force_inference(_: &Cursor<Vec<u8>>) {}\n   113:     /// # force_inference(&buff);\n   114:     ///\n   115:     /// let vec = buff.into_inner();\n   116:     /// ```\n   117:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   118:     pub fn into_inner(self) -> T {\n   119:         self.inner\n   120:     }\n   121: \n   122:     /// Gets a reference to the underlying value in this cursor.\n   123:     ///\n   124:     /// # Examples\n   125:     ///\n   126:     /// ```\n   127:     /// use std::io::Cursor;\n   128:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Cursor::new",
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
    "nanvix_source": "    90:     ///\n    91:     /// ```\n    92:     /// use std::io::Cursor;\n    93:     ///\n    94:     /// let buff = Cursor::new(Vec::new());\n    95:     /// # fn force_inference(_: &Cursor<Vec<u8>>) {}\n    96:     /// # force_inference(&buff);\n    97:     /// ```\n    98:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    99:     #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n   100:     pub const fn new(inner: T) -> Cursor<T> {\n   101:         Cursor { pos: 0, inner }\n   102:     }\n   103: \n   104:     /// Consumes this cursor, returning the underlying value.\n   105:     ///\n   106:     /// # Examples\n   107:     ///\n   108:     /// ```\n   109:     /// use std::io::Cursor;\n   110:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Cursor::position",
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
    "nanvix_source": "   174:     /// assert_eq!(buff.position(), 0);\n   175:     ///\n   176:     /// buff.seek(SeekFrom::Current(2)).unwrap();\n   177:     /// assert_eq!(buff.position(), 2);\n   178:     ///\n   179:     /// buff.seek(SeekFrom::Current(-1)).unwrap();\n   180:     /// assert_eq!(buff.position(), 1);\n   181:     /// ```\n   182:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   183:     #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n   184:     pub const fn position(&self) -> u64 {\n   185:         self.pos\n   186:     }\n   187: \n   188:     /// Sets the position of this cursor.\n   189:     ///\n   190:     /// # Examples\n   191:     ///\n   192:     /// ```\n   193:     /// use std::io::Cursor;\n   194:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Cursor::set_position",
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
    "nanvix_source": "   197:     /// assert_eq!(buff.position(), 0);\n   198:     ///\n   199:     /// buff.set_position(2);\n   200:     /// assert_eq!(buff.position(), 2);\n   201:     ///\n   202:     /// buff.set_position(4);\n   203:     /// assert_eq!(buff.position(), 4);\n   204:     /// ```\n   205:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   206:     #[rustc_const_stable(feature = \"const_mut_cursor\", since = \"1.86.0\")]\n   207:     pub const fn set_position(&mut self, pos: u64) {\n   208:         self.pos = pos;\n   209:     }\n   210: \n   211:     #[doc(hidden)]\n   212:     #[unstable(feature = \"core_io_internals\", reason = \"exposed only for libstd\", issue = \"none\")]\n   213:     #[inline]\n   214:     pub const fn into_parts_mut(&mut self) -> (&mut u64, &mut T) {\n   215:         (&mut self.pos, &mut self.inner)\n   216:     }\n   217: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Error::get_mut",
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
    "nanvix_source": "   423:     /// fn main() {\n   424:     ///     // Will print \"No inner error\".\n   425:     ///     print_error(&change_error(Error::last_os_error()));\n   426:     ///     // Will print \"Inner error: ...\".\n   427:     ///     print_error(&change_error(Error::new(ErrorKind::Other, MyError::new())));\n   428:     /// }\n   429:     /// ```\n   430:     #[stable(feature = \"io_error_inner\", since = \"1.3.0\")]\n   431:     #[must_use]\n   432:     #[inline]\n   433:     pub fn get_mut(&mut self) -> Option<&mut (dyn error::Error + Send + Sync + 'static)> {\n   434:         match self.repr.data_mut() {\n   435:             ErrorData::Os(..) => None,\n   436:             ErrorData::Simple(..) => None,\n   437:             ErrorData::SimpleMessage(..) => None,\n   438:             ErrorData::Custom(c) => Some(c.error_mut()),\n   439:         }\n   440:     }\n   441: \n   442:     /// Returns the corresponding [`ErrorKind`] for this error.\n   443:     ///",
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
