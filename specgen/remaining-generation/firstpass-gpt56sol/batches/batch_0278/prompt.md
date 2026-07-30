For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::io::empty",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "    68: /// ```rust\n    69: /// use std::io::{self, Read};\n    70: ///\n    71: /// let mut buffer = String::new();\n    72: /// io::empty().read_to_string(&mut buffer).unwrap();\n    73: /// assert!(buffer.is_empty());\n    74: /// ```\n    75: #[must_use]\n    76: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    77: #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n    78: pub const fn empty() -> Empty {\n    79:     Empty\n    80: }\n    81: \n    82: /// A reader which yields one byte over and over and over and over and over and...\n    83: ///\n    84: /// This struct is generally created by calling [`repeat()`]. Please\n    85: /// see the documentation of [`repeat()`] for more details.\n    86: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    87: #[non_exhaustive]\n    88: pub struct Repeat {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::repeat",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   115: /// ```\n   116: /// use std::io::{self, Read};\n   117: ///\n   118: /// let mut buffer = [0; 3];\n   119: /// io::repeat(0b101).read_exact(&mut buffer).unwrap();\n   120: /// assert_eq!(buffer, [0b101, 0b101, 0b101]);\n   121: /// ```\n   122: #[must_use]\n   123: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   124: #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n   125: pub const fn repeat(byte: u8) -> Repeat {\n   126:     Repeat { byte }\n   127: }\n   128: \n   129: #[stable(feature = \"std_debug\", since = \"1.16.0\")]\n   130: impl fmt::Debug for Repeat {\n   131:     fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {\n   132:         f.debug_struct(\"Repeat\").finish_non_exhaustive()\n   133:     }\n   134: }\n   135: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::io::sink",
    "generation_group": "toolchain_unavailable",
    "classification": "toolchain_unavailable",
    "classification_reasons": [
      "not_in_verus_rust_1_96"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "not_in_verus_rust_1_96"
    ],
    "available_in_verus_rust_1_96": false,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {},
    "verification_source": "",
    "nanvix_source": "   155: /// ```rust\n   156: /// use std::io::{self, Write};\n   157: ///\n   158: /// let buffer = vec![1, 2, 3, 5, 8];\n   159: /// let num_bytes = io::sink().write(&buffer).unwrap();\n   160: /// assert_eq!(num_bytes, 5);\n   161: /// ```\n   162: #[must_use]\n   163: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   164: #[rustc_const_stable(feature = \"const_io_structs\", since = \"1.79.0\")]\n   165: pub const fn sink() -> Sink {\n   166:     Sink\n   167: }\n   168: \n   169: /// Adapter to chain together two readers.\n   170: ///\n   171: /// This struct is generally created by calling [`chain`] on a reader.\n   172: /// Please see the documentation of [`chain`] for more details.\n   173: ///\n   174: /// [`chain`]: ../../std/io/trait.Read.html#method.chain\n   175: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::into_string",
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
    "nanvix_source": "  1803:     /// # Examples\n  1804:     ///\n  1805:     /// ```\n  1806:     /// use std::path::PathBuf;\n  1807:     ///\n  1808:     /// let path_buf = PathBuf::from(\"foo\");\n  1809:     /// let string = path_buf.into_string();\n  1810:     /// assert_eq!(string, Ok(String::from(\"foo\")));\n  1811:     /// ```\n  1812:     #[stable(feature = \"pathbuf_into_string\", since = \"CURRENT_RUSTC_VERSION\")]\n  1813:     pub fn into_string(self) -> Result<String, PathBuf> {\n  1814:         self.into_os_string().into_string().map_err(PathBuf::from)\n  1815:     }\n  1816: \n  1817:     /// Converts this `PathBuf` into a [boxed](Box) [`Path`].\n  1818:     #[stable(feature = \"into_boxed_path\", since = \"1.20.0\")]\n  1819:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1820:     #[inline]\n  1821:     pub fn into_boxed_path(self) -> Box<Path> {\n  1822:         let rw = Box::into_raw(self.inner.into_boxed_os_str()) as *mut Path;\n  1823:         unsafe { Box::from_raw(rw) }",
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
