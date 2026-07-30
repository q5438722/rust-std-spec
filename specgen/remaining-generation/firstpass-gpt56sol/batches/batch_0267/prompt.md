For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::boxed::BoxedArrayIntoIter::as_mut_slice",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "data_structure",
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
    "nanvix_source": "   238: impl<T, const N: usize, A: Allocator> BoxedArrayIntoIter<T, N, A> {\n   239:     /// Returns an immutable slice of all elements that have not been yielded\n   240:     /// yet.\n   241:     #[stable(feature = \"boxed_array_value_iter\", since = \"CURRENT_RUSTC_VERSION\")]\n   242:     pub fn as_slice(&self) -> &[T] {\n   243:         self.inner.as_slice()\n   244:     }\n   245: \n   246:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   247:     #[stable(feature = \"boxed_array_value_iter\", since = \"CURRENT_RUSTC_VERSION\")]\n   248:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   249:         self.inner.as_mut_slice()\n   250:     }\n   251: }\n   252: \n   253: #[stable(feature = \"boxed_array_value_iter\", since = \"CURRENT_RUSTC_VERSION\")]\n   254: impl<T, const N: usize, A: Allocator> Iterator for BoxedArrayIntoIter<T, N, A> {\n   255:     type Item = T;\n   256:     fn next(&mut self) -> Option<Self::Item> {\n   257:         self.inner.next()\n   258:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::boxed::BoxedArrayIntoIter::as_slice",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "data_structure",
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
    "nanvix_source": "   232: #[rustc_insignificant_dtor]\n   233: pub struct BoxedArrayIntoIter<T, const N: usize, A: Allocator = Global> {\n   234:     // FIXME: make a more efficient implementation (without the need to store capacity)\n   235:     inner: vec::IntoIter<T, A>,\n   236: }\n   237: \n   238: impl<T, const N: usize, A: Allocator> BoxedArrayIntoIter<T, N, A> {\n   239:     /// Returns an immutable slice of all elements that have not been yielded\n   240:     /// yet.\n   241:     #[stable(feature = \"boxed_array_value_iter\", since = \"CURRENT_RUSTC_VERSION\")]\n   242:     pub fn as_slice(&self) -> &[T] {\n   243:         self.inner.as_slice()\n   244:     }\n   245: \n   246:     /// Returns a mutable slice of all elements that have not been yielded yet.\n   247:     #[stable(feature = \"boxed_array_value_iter\", since = \"CURRENT_RUSTC_VERSION\")]\n   248:     pub fn as_mut_slice(&mut self) -> &mut [T] {\n   249:         self.inner.as_mut_slice()\n   250:     }\n   251: }\n   252: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Chain::get_mut",
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
    "nanvix_source": "   271:     /// fn main() -> io::Result<()> {\n   272:     ///     let mut foo_file = File::open(\"foo.txt\")?;\n   273:     ///     let mut bar_file = File::open(\"bar.txt\")?;\n   274:     ///\n   275:     ///     let mut chain = foo_file.chain(bar_file);\n   276:     ///     let (foo_file, bar_file) = chain.get_mut();\n   277:     ///     Ok(())\n   278:     /// }\n   279:     /// ```\n   280:     #[stable(feature = \"more_io_inner_methods\", since = \"1.20.0\")]\n   281:     pub fn get_mut(&mut self) -> (&mut T, &mut U) {\n   282:         (&mut self.first, &mut self.second)\n   283:     }\n   284: }\n   285: \n   286: #[doc(hidden)]\n   287: #[unstable(feature = \"core_io_internals\", reason = \"exposed only for libstd\", issue = \"none\")]\n   288: #[must_use]\n   289: #[inline]\n   290: pub const fn chain<T, U>(first: T, second: U) -> Chain<T, U> {\n   291:     Chain { first, second, done_first: false }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Chain::get_ref",
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
    "nanvix_source": "   244:     /// fn main() -> io::Result<()> {\n   245:     ///     let mut foo_file = File::open(\"foo.txt\")?;\n   246:     ///     let mut bar_file = File::open(\"bar.txt\")?;\n   247:     ///\n   248:     ///     let chain = foo_file.chain(bar_file);\n   249:     ///     let (foo_file, bar_file) = chain.get_ref();\n   250:     ///     Ok(())\n   251:     /// }\n   252:     /// ```\n   253:     #[stable(feature = \"more_io_inner_methods\", since = \"1.20.0\")]\n   254:     pub fn get_ref(&self) -> (&T, &U) {\n   255:         (&self.first, &self.second)\n   256:     }\n   257: \n   258:     /// Gets mutable references to the underlying readers in this `Chain`.\n   259:     ///\n   260:     /// Care should be taken to avoid modifying the internal I/O state of the\n   261:     /// underlying readers as doing so may corrupt the internal state of this\n   262:     /// `Chain`.\n   263:     ///\n   264:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Chain::into_inner",
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
    "nanvix_source": "   217:     /// fn main() -> io::Result<()> {\n   218:     ///     let mut foo_file = File::open(\"foo.txt\")?;\n   219:     ///     let mut bar_file = File::open(\"bar.txt\")?;\n   220:     ///\n   221:     ///     let chain = foo_file.chain(bar_file);\n   222:     ///     let (foo_file, bar_file) = chain.into_inner();\n   223:     ///     Ok(())\n   224:     /// }\n   225:     /// ```\n   226:     #[stable(feature = \"more_io_inner_methods\", since = \"1.20.0\")]\n   227:     pub fn into_inner(self) -> (T, U) {\n   228:         (self.first, self.second)\n   229:     }\n   230: \n   231:     /// Gets references to the underlying readers in this `Chain`.\n   232:     ///\n   233:     /// Care should be taken to avoid modifying the internal I/O state of the\n   234:     /// underlying readers as doing so may corrupt the internal state of this\n   235:     /// `Chain`.\n   236:     ///\n   237:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::Cursor::get_mut",
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
    "nanvix_source": "   149:     /// use std::io::Cursor;\n   150:     ///\n   151:     /// let mut buff = Cursor::new(Vec::new());\n   152:     /// # fn force_inference(_: &Cursor<Vec<u8>>) {}\n   153:     /// # force_inference(&buff);\n   154:     ///\n   155:     /// let reference = buff.get_mut();\n   156:     /// ```\n   157:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   158:     #[rustc_const_stable(feature = \"const_mut_cursor\", since = \"1.86.0\")]\n   159:     pub const fn get_mut(&mut self) -> &mut T {\n   160:         &mut self.inner\n   161:     }\n   162: \n   163:     /// Returns the current position of this cursor.\n   164:     ///\n   165:     /// # Examples\n   166:     ///\n   167:     /// ```\n   168:     /// use std::io::Cursor;\n   169:     /// use std::io::prelude::*;",
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
