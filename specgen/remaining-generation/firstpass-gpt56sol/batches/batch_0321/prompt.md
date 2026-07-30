For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ffi::CStr::from_bytes_with_nul_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "from_bytes_with_nul_unchecked",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "bytes",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "slice": {
                    "primitive": "u8"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 10771,
                "path": "CStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   372:     ///\n   373:     /// # Examples\n   374:     ///\n   375:     /// ```\n   376:     /// use std::ffi::CStr;\n   377:     ///\n   378:     /// let bytes = b\"Hello world!\\0\";\n   379:     ///\n   380:     /// let cstr = unsafe { CStr::from_bytes_with_nul_unchecked(bytes) };\n   381:     /// assert_eq!(cstr.to_bytes_with_nul(), bytes);\n   382:     /// ```\n   383:     #[inline]\n   384:     #[must_use]\n   385:     #[stable(feature = \"cstr_from_bytes\", since = \"1.10.0\")]\n   386:     #[rustc_const_stable(feature = \"const_cstr_unchecked\", since = \"1.59.0\")]\n   387:     #[rustc_allow_const_fn_unstable(const_eval_select)]\n   388:     pub const unsafe fn from_bytes_with_nul_unchecked(bytes: &[u8]) -> &CStr {\n   389:         const_eval_select!(\n   390:             @capture { bytes: &[u8] } -> &CStr:\n   391:             if const {\n   392:                 // Saturating so that an empty slice panics in the assert with a good\n   393:                 // message, not here due to underflow.\n   394:                 let mut i = bytes.len().saturating_sub(1);\n   395:                 assert!(!bytes.is_empty() && bytes[i] == 0, \"input was not nul-terminated\");\n   396: \n   397:                 // Ending nul byte exists, skip to the rest.\n   398:                 while i != 0 {\n   399:                     i -= 1;\n   400:                     let byte = bytes[i];\n   401:                     assert!(byte != 0, \"input contained interior nul\");\n   402:                 }\n   403: \n   404:                 // SAFETY: See runtime cast comment below.",
    "nanvix_source": "   379:     /// let bytes = b\"Hello world!\\0\";\n   380:     ///\n   381:     /// let cstr = unsafe { CStr::from_bytes_with_nul_unchecked(bytes) };\n   382:     /// assert_eq!(cstr.to_bytes_with_nul(), bytes);\n   383:     /// ```\n   384:     #[inline]\n   385:     #[must_use]\n   386:     #[stable(feature = \"cstr_from_bytes\", since = \"1.10.0\")]\n   387:     #[rustc_const_stable(feature = \"const_cstr_unchecked\", since = \"1.59.0\")]\n   388:     #[rustc_allow_const_fn_unstable(const_eval_select)]\n   389:     pub const unsafe fn from_bytes_with_nul_unchecked(bytes: &[u8]) -> &CStr {\n   390:         const_eval_select!(\n   391:             @capture { bytes: &[u8] } -> &CStr:\n   392:             if const {\n   393:                 // Saturating so that an empty slice panics in the assert with a good\n   394:                 // message, not here due to underflow.\n   395:                 let mut i = bytes.len().saturating_sub(1);\n   396:                 assert!(!bytes.is_empty() && bytes[i] == 0, \"input was not nul-terminated\");\n   397: \n   398:                 // Ending nul byte exists, skip to the rest.\n   399:                 while i != 0 {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ffi::CStr::from_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "reference_identity_vs_view"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "lifetime": {
                "outlives": []
              }
            },
            "name": "'a"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "from_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 10771,
            "path": "CStr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:25249",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:10771",
        "resolved_owner_path": [
          "core",
          "ffi",
          "c_str",
          "CStr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "resolved_path": {
                    "args": null,
                    "id": 25237,
                    "path": "c_char"
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": "'a",
            "type": {
              "resolved_path": {
                "args": null,
                "id": 10771,
                "path": "CStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   237:     /// use std::ffi::{c_char, CStr};\n   238:     ///\n   239:     /// const HELLO_PTR: *const c_char = {\n   240:     ///     const BYTES: &[u8] = b\"Hello, world!\\0\";\n   241:     ///     BYTES.as_ptr().cast()\n   242:     /// };\n   243:     /// const HELLO: &CStr = unsafe { CStr::from_ptr(HELLO_PTR) };\n   244:     ///\n   245:     /// assert_eq!(c\"Hello, world!\", HELLO);\n   246:     /// ```\n   247:     ///\n   248:     /// [valid]: core::ptr#safety\n   249:     #[inline] // inline is necessary for codegen to see strlen.\n   250:     #[must_use]\n   251:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   252:     #[rustc_const_stable(feature = \"const_cstr_from_ptr\", since = \"1.81.0\")]\n   253:     pub const unsafe fn from_ptr<'a>(ptr: *const c_char) -> &'a CStr {\n   254:         // SAFETY: The caller has provided a pointer that points to a valid C\n   255:         // string with a NUL terminator less than `isize::MAX` from `ptr`.\n   256:         let len = unsafe { strlen(ptr) };\n   257: \n   258:         // SAFETY: The caller has provided a valid pointer with length less than\n   259:         // `isize::MAX`, so `from_raw_parts` is safe. The content remains valid\n   260:         // and doesn't change for the lifetime of the returned `CStr`. This\n   261:         // means the call to `from_bytes_with_nul_unchecked` is correct.\n   262:         //\n   263:         // The cast from c_char to u8 is ok because a c_char is always one byte.\n   264:         unsafe { Self::from_bytes_with_nul_unchecked(slice::from_raw_parts(ptr.cast(), len + 1)) }\n   265:     }\n   266: \n   267:     /// Creates a C string wrapper from a byte slice with any number of nuls.\n   268:     ///\n   269:     /// This method will create a `CStr` from any byte slice that contains at",
    "nanvix_source": "   244:     /// const HELLO: &CStr = unsafe { CStr::from_ptr(HELLO_PTR) };\n   245:     ///\n   246:     /// assert_eq!(c\"Hello, world!\", HELLO);\n   247:     /// ```\n   248:     ///\n   249:     /// [valid]: core::ptr#safety\n   250:     #[inline] // inline is necessary for codegen to see strlen.\n   251:     #[must_use]\n   252:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   253:     #[rustc_const_stable(feature = \"const_cstr_from_ptr\", since = \"1.81.0\")]\n   254:     pub const unsafe fn from_ptr<'a>(ptr: *const c_char) -> &'a CStr {\n   255:         // SAFETY: The caller has provided a pointer that points to a valid C\n   256:         // string with a NUL terminator less than `isize::MAX` from `ptr`.\n   257:         let len = unsafe { strlen(ptr) };\n   258: \n   259:         // SAFETY: The caller has provided a valid pointer with length less than\n   260:         // `isize::MAX`, so `from_raw_parts` is safe. The content remains valid\n   261:         // and doesn't change for the lifetime of the returned `CStr`. This\n   262:         // means the call to `from_bytes_with_nul_unchecked` is correct.\n   263:         //\n   264:         // The cast from c_char to u8 is ok because a c_char is always one byte.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::hint::assert_unchecked",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "assert_unchecked",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "cond",
            {
              "primitive": "bool"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   186: /// ```asm\n   187: /// next_value:\n   188: ///         mov     eax, dword ptr [rdi]\n   189: ///         inc     eax\n   190: ///         ret\n   191: /// ```\n   192: ///\n   193: /// This example is quite unlike anything that would be used in the real world: it is redundant\n   194: /// to put an assertion right next to code that checks the same thing, and dereferencing a\n   195: /// pointer already has the builtin assumption that it is nonnull. However, it illustrates the\n   196: /// kind of changes the optimizer can make even when the behavior is less obviously related.\n   197: #[track_caller]\n   198: #[inline(always)]\n   199: #[doc(alias = \"assume\")]\n   200: #[stable(feature = \"hint_assert_unchecked\", since = \"1.81.0\")]\n   201: #[rustc_const_stable(feature = \"hint_assert_unchecked\", since = \"1.81.0\")]\n   202: pub const unsafe fn assert_unchecked(cond: bool) {\n   203:     // SAFETY: The caller promised `cond` is true.\n   204:     unsafe {\n   205:         ub_checks::assert_unsafe_precondition!(\n   206:             check_language_ub,\n   207:             \"hint::assert_unchecked must never be called when the condition is false\",\n   208:             (cond: bool = cond) => cond,\n   209:         );\n   210:         crate::intrinsics::assume(cond);\n   211:     }\n   212: }\n   213: \n   214: /// Emits a machine instruction to signal the processor that it is running in\n   215: /// a busy-wait spin-loop (\"spin lock\").\n   216: ///\n   217: /// Upon receiving the spin-loop signal the processor can optimize its behavior by,\n   218: /// for example, saving power or switching hyper-threads.",
    "nanvix_source": "   192: ///\n   193: /// This example is quite unlike anything that would be used in the real world: it is redundant\n   194: /// to put an assertion right next to code that checks the same thing, and dereferencing a\n   195: /// pointer already has the builtin assumption that it is nonnull. However, it illustrates the\n   196: /// kind of changes the optimizer can make even when the behavior is less obviously related.\n   197: #[track_caller]\n   198: #[inline(always)]\n   199: #[doc(alias = \"assume\")]\n   200: #[stable(feature = \"hint_assert_unchecked\", since = \"1.81.0\")]\n   201: #[rustc_const_stable(feature = \"hint_assert_unchecked\", since = \"1.81.0\")]\n   202: pub const unsafe fn assert_unchecked(cond: bool) {\n   203:     // SAFETY: The caller promised `cond` is true.\n   204:     unsafe {\n   205:         ub_checks::assert_unsafe_precondition!(\n   206:             check_language_ub,\n   207:             \"hint::assert_unchecked must never be called when the condition is false\",\n   208:             (cond: bool = cond) => cond,\n   209:         );\n   210:         crate::intrinsics::assume(cond);\n   211:     }\n   212: }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::intrinsics::copy",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "copy",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "src",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "dst",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2964: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2965: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2966: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2967: #[rustc_nounwind]\n  2968: #[rustc_intrinsic]\n  2969: pub const unsafe fn copy_nonoverlapping<T>(src: *const T, dst: *mut T, count: usize);\n  2970: \n  2971: /// This is an accidentally-stable alias to [`ptr::copy`]; use that instead.\n  2972: // Note (intentionally not in the doc comment): `ptr::copy` adds some extra\n  2973: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2974: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  2975: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2976: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2977: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2978: #[rustc_nounwind]\n  2979: #[rustc_intrinsic]\n  2980: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize);\n  2981: \n  2982: /// This is an accidentally-stable alias to [`ptr::write_bytes`]; use that instead.\n  2983: // Note (intentionally not in the doc comment): `ptr::write_bytes` adds some extra\n  2984: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2985: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  2986: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2987: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2988: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2989: #[rustc_nounwind]\n  2990: #[rustc_intrinsic]\n  2991: pub const unsafe fn write_bytes<T>(dst: *mut T, val: u8, count: usize);\n  2992: \n  2993: /// Returns the minimum of two `f16` values, ignoring NaN.\n  2994: ///\n  2995: /// This behaves like IEEE 754-2019 minimumNumber, *except* that it does not order signed\n  2996: /// zeros deterministically. In particular:",
    "nanvix_source": "  3044: \n  3045: /// This is an accidentally-stable alias to [`ptr::copy`]; use that instead.\n  3046: // Note (intentionally not in the doc comment): `ptr::copy` adds some extra\n  3047: // debug assertions; if you are writing compiler tests or code inside the standard library\n  3048: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  3049: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3050: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  3051: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  3052: #[rustc_nounwind]\n  3053: #[rustc_intrinsic]\n  3054: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize);\n  3055: \n  3056: /// This is an accidentally-stable alias to [`ptr::write_bytes`]; use that instead.\n  3057: // Note (intentionally not in the doc comment): `ptr::write_bytes` adds some extra\n  3058: // debug assertions; if you are writing compiler tests or code inside the standard library\n  3059: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  3060: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3061: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  3062: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  3063: #[rustc_nounwind]\n  3064: #[rustc_intrinsic]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::intrinsics::copy_nonoverlapping",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "T"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "copy_nonoverlapping",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "src",
            {
              "raw_pointer": {
                "is_mutable": false,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "dst",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "generic": "T"
                }
              }
            }
          ],
          [
            "count",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  2953: /// This is used to implement functions like `ptr::metadata`.\n  2954: #[rustc_nounwind]\n  2955: #[unstable(feature = \"core_intrinsics\", issue = \"none\")]\n  2956: #[rustc_intrinsic_const_stable_indirect]\n  2957: #[rustc_intrinsic]\n  2958: pub const fn ptr_metadata<P: ptr::Pointee<Metadata = M> + PointeeSized, M>(ptr: *const P) -> M;\n  2959: \n  2960: /// This is an accidentally-stable alias to [`ptr::copy_nonoverlapping`]; use that instead.\n  2961: // Note (intentionally not in the doc comment): `ptr::copy_nonoverlapping` adds some extra\n  2962: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2963: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  2964: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2965: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2966: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2967: #[rustc_nounwind]\n  2968: #[rustc_intrinsic]\n  2969: pub const unsafe fn copy_nonoverlapping<T>(src: *const T, dst: *mut T, count: usize);\n  2970: \n  2971: /// This is an accidentally-stable alias to [`ptr::copy`]; use that instead.\n  2972: // Note (intentionally not in the doc comment): `ptr::copy` adds some extra\n  2973: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2974: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  2975: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2976: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2977: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2978: #[rustc_nounwind]\n  2979: #[rustc_intrinsic]\n  2980: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize);\n  2981: \n  2982: /// This is an accidentally-stable alias to [`ptr::write_bytes`]; use that instead.\n  2983: // Note (intentionally not in the doc comment): `ptr::write_bytes` adds some extra\n  2984: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2985: // that wants to avoid those debug assertions, directly call this intrinsic instead.",
    "nanvix_source": "  3033: \n  3034: /// This is an accidentally-stable alias to [`ptr::copy_nonoverlapping`]; use that instead.\n  3035: // Note (intentionally not in the doc comment): `ptr::copy_nonoverlapping` adds some extra\n  3036: // debug assertions; if you are writing compiler tests or code inside the standard library\n  3037: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  3038: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3039: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  3040: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  3041: #[rustc_nounwind]\n  3042: #[rustc_intrinsic]\n  3043: pub const unsafe fn copy_nonoverlapping<T>(src: *const T, dst: *mut T, count: usize);\n  3044: \n  3045: /// This is an accidentally-stable alias to [`ptr::copy`]; use that instead.\n  3046: // Note (intentionally not in the doc comment): `ptr::copy` adds some extra\n  3047: // debug assertions; if you are writing compiler tests or code inside the standard library\n  3048: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  3049: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3050: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  3051: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  3052: #[rustc_nounwind]\n  3053: #[rustc_intrinsic]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::intrinsics::transmute",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "other",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Src"
          },
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Dst"
          }
        ],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "transmute",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "src",
            {
              "generic": "Src"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Dst"
        }
      }
    },
    "verification_source": "   825: ///         // This now has three mutable references pointing at the same\n   826: ///         // memory. `slice`, the rvalue ret.0, and the rvalue ret.1.\n   827: ///         // `slice` is never used after `let ptr = ...`, and so one can\n   828: ///         // treat it as \"dead\", and therefore, you only have two real\n   829: ///         // mutable slices.\n   830: ///         (slice::from_raw_parts_mut(ptr, mid),\n   831: ///          slice::from_raw_parts_mut(ptr.add(mid), len - mid))\n   832: ///     }\n   833: /// }\n   834: /// ```\n   835: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   836: #[rustc_allowed_through_unstable_modules = \"import this function via `std::mem` instead\"]\n   837: #[rustc_const_stable(feature = \"const_transmute\", since = \"1.56.0\")]\n   838: #[rustc_diagnostic_item = \"transmute\"]\n   839: #[rustc_nounwind]\n   840: #[rustc_intrinsic]\n   841: pub const unsafe fn transmute<Src, Dst>(src: Src) -> Dst;\n   842: \n   843: /// Like [`transmute`], but even less checked at compile-time: rather than\n   844: /// giving an error for `size_of::<Src>() != size_of::<Dst>()`, it's\n   845: /// **Undefined Behavior** at runtime.\n   846: ///\n   847: /// Prefer normal `transmute` where possible, for the extra checking, since\n   848: /// both do exactly the same thing at runtime, if they both compile.\n   849: ///\n   850: /// This is not expected to ever be exposed directly to users, rather it\n   851: /// may eventually be exposed through some more-constrained API.\n   852: #[rustc_intrinsic_const_stable_indirect]\n   853: #[rustc_nounwind]\n   854: #[rustc_intrinsic]\n   855: pub const unsafe fn transmute_unchecked<Src, Dst>(src: Src) -> Dst;\n   856: \n   857: /// Returns `true` if the actual type given as `T` requires drop",
    "nanvix_source": "   833: ///         (fst, snd)\n   834: ///     }\n   835: /// }\n   836: /// ```\n   837: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   838: #[rustc_allowed_through_unstable_modules = \"import this function via `std::mem` instead\"]\n   839: #[rustc_const_stable(feature = \"const_transmute\", since = \"1.56.0\")]\n   840: #[rustc_diagnostic_item = \"transmute\"]\n   841: #[rustc_nounwind]\n   842: #[rustc_intrinsic]\n   843: pub const unsafe fn transmute<Src, Dst>(src: Src) -> Dst;\n   844: \n   845: /// Like [`transmute`], but even less checked at compile-time: rather than\n   846: /// giving an error for `size_of::<Src>() != size_of::<Dst>()`, it's\n   847: /// **Undefined Behavior** at runtime.\n   848: ///\n   849: /// Prefer normal `transmute` where possible, for the extra checking, since\n   850: /// both do exactly the same thing at runtime, if they both compile.\n   851: ///\n   852: /// This is not expected to ever be exposed directly to users, rather it\n   853: /// may eventually be exposed through some more-constrained API.",
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
