For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ptr::with_addr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "multiple_rust_declarations_share_path"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "with_addr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51704",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ],
          [
            "addr",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   179:     }\n   180: \n   181:     /// Creates a new pointer with the given address and the [provenance][crate::ptr#provenance] of\n   182:     /// `self`.\n   183:     ///\n   184:     /// This is similar to a `addr as *mut T` cast, but copies\n   185:     /// the *provenance* of `self` to the new pointer.\n   186:     /// This avoids the inherent ambiguity of the unary cast.\n   187:     ///\n   188:     /// This is equivalent to using [`wrapping_offset`][pointer::wrapping_offset] to offset\n   189:     /// `self` to the given address, and therefore has all the same capabilities and restrictions.\n   190:     ///\n   191:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   192:     #[must_use]\n   193:     #[inline]\n   194:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   195:     pub fn with_addr(self, addr: usize) -> Self {\n   196:         // This should probably be an intrinsic to avoid doing any sort of arithmetic, but\n   197:         // meanwhile, we can implement it with `wrapping_offset`, which preserves the pointer's\n   198:         // provenance.\n   199:         let self_addr = self.addr() as isize;\n   200:         let dest_addr = addr as isize;\n   201:         let offset = dest_addr.wrapping_sub(self_addr);\n   202:         self.wrapping_byte_offset(offset)\n   203:     }\n   204: \n   205:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the original\n   206:     /// pointer's [provenance][crate::ptr#provenance].\n   207:     ///\n   208:     /// This is a convenience for [`with_addr`][pointer::with_addr], see that method for details.\n   209:     ///\n   210:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   211:     #[must_use]",
    "nanvix_source": "   186:     /// the *provenance* of `self` to the new pointer.\n   187:     /// This avoids the inherent ambiguity of the unary cast.\n   188:     ///\n   189:     /// This is equivalent to using [`wrapping_offset`][pointer::wrapping_offset] to offset\n   190:     /// `self` to the given address, and therefore has all the same capabilities and restrictions.\n   191:     ///\n   192:     /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   193:     #[must_use]\n   194:     #[inline]\n   195:     #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   196:     pub fn with_addr(self, addr: usize) -> Self {\n   197:         // This should probably be an intrinsic to avoid doing any sort of arithmetic, but\n   198:         // meanwhile, we can implement it with `wrapping_offset`, which preserves the pointer's\n   199:         // provenance.\n   200:         let self_addr = self.addr() as isize;\n   201:         let dest_addr = addr as isize;\n   202:         let offset = dest_addr.wrapping_sub(self_addr);\n   203:         self.wrapping_byte_offset(offset)\n   204:     }\n   205: \n   206:     /// Creates a new pointer by mapping `self`'s address to a new one, preserving the original",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::with_exposed_provenance",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
        "is_unsafe": false
      },
      "name": "with_exposed_provenance",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   976: /// stay conformant with the Rust memory model. It is recommended to use [Strict\n   977: /// Provenance][self#strict-provenance] APIs such as [`with_addr`][pointer::with_addr] wherever\n   978: /// possible.\n   979: ///\n   980: /// On most platforms this will produce a value with the same bytes as the address. Platforms\n   981: /// which need to store additional information in a pointer may not support this operation,\n   982: /// since it is generally not possible to actually *compute* which provenance the returned\n   983: /// pointer has to pick up.\n   984: ///\n   985: /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   986: #[must_use]\n   987: #[inline(always)]\n   988: #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n   989: #[rustc_const_stable(feature = \"const_exposed_provenance\", since = \"1.91.0\")]\n   990: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n   991: #[allow(fuzzy_provenance_casts)] // this *is* the explicit provenance API one should use instead\n   992: pub const fn with_exposed_provenance<T>(addr: usize) -> *const T {\n   993:     addr as *const T\n   994: }\n   995: \n   996: /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n   997: /// [provenance][crate::ptr#provenance].\n   998: ///\n   999: /// This is fully equivalent to `addr as *mut T`. The provenance of the returned pointer is that\n  1000: /// of *some* pointer that was previously exposed by passing it to\n  1001: /// [`expose_provenance`][pointer::expose_provenance], or a `ptr as usize` cast. In addition, memory\n  1002: /// which is outside the control of the Rust abstract machine (MMIO registers, for example) is\n  1003: /// always considered to be accessible with an exposed provenance, so long as this memory is disjoint\n  1004: /// from memory that will be used by the abstract machine such as the stack, heap, and statics.\n  1005: ///\n  1006: /// The exact provenance that gets picked is not specified. The compiler will do its best to pick\n  1007: /// the \"right\" provenance for you (whatever that may be), but currently we cannot provide any\n  1008: /// guarantees about which provenance the resulting pointer will have -- and therefore there",
    "nanvix_source": "   992: /// since it is generally not possible to actually *compute* which provenance the returned\n   993: /// pointer has to pick up.\n   994: ///\n   995: /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n   996: #[must_use]\n   997: #[inline(always)]\n   998: #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n   999: #[rustc_const_stable(feature = \"const_exposed_provenance\", since = \"1.91.0\")]\n  1000: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1001: #[allow(implicit_provenance_casts)] // this *is* the explicit provenance API one should use instead\n  1002: pub const fn with_exposed_provenance<T>(addr: usize) -> *const T {\n  1003:     addr as *const T\n  1004: }\n  1005: \n  1006: /// Converts an address back to a mutable pointer, picking up some previously 'exposed'\n  1007: /// [provenance][crate::ptr#provenance].\n  1008: ///\n  1009: /// This is fully equivalent to `addr as *mut T`. The provenance of the returned pointer is that\n  1010: /// of *some* pointer that was previously exposed by passing it to\n  1011: /// [`expose_provenance`][pointer::expose_provenance], or a `ptr as usize` cast. In addition, memory\n  1012: /// which is outside the control of the Rust abstract machine (MMIO registers, for example) is",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::with_exposed_provenance_mut",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
        "is_unsafe": false
      },
      "name": "with_exposed_provenance_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "  1017: /// stay conformant with the Rust memory model. It is recommended to use [Strict\n  1018: /// Provenance][self#strict-provenance] APIs such as [`with_addr`][pointer::with_addr] wherever\n  1019: /// possible.\n  1020: ///\n  1021: /// On most platforms this will produce a value with the same bytes as the address. Platforms\n  1022: /// which need to store additional information in a pointer may not support this operation,\n  1023: /// since it is generally not possible to actually *compute* which provenance the returned\n  1024: /// pointer has to pick up.\n  1025: ///\n  1026: /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n  1027: #[must_use]\n  1028: #[inline(always)]\n  1029: #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n  1030: #[rustc_const_stable(feature = \"const_exposed_provenance\", since = \"1.91.0\")]\n  1031: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1032: #[allow(fuzzy_provenance_casts)] // this *is* the explicit provenance API one should use instead\n  1033: pub const fn with_exposed_provenance_mut<T>(addr: usize) -> *mut T {\n  1034:     addr as *mut T\n  1035: }\n  1036: \n  1037: /// Converts a reference to a raw pointer.\n  1038: ///\n  1039: /// For `r: &T`, `from_ref(r)` is equivalent to `r as *const T` (except for the caveat noted below),\n  1040: /// but is a bit safer since it will never silently change type or mutability, in particular if the\n  1041: /// code is refactored.\n  1042: ///\n  1043: /// The caller must ensure that the pointee outlives the pointer this function returns, or else it\n  1044: /// will end up dangling.\n  1045: ///\n  1046: /// The caller must also ensure that the memory the pointer (non-transitively) points to is never\n  1047: /// written to (except inside an `UnsafeCell`) using this pointer or any pointer derived from it. If\n  1048: /// you need to mutate the pointee, use [`from_mut`]. Specifically, to turn a mutable reference `m:\n  1049: /// &mut T` into `*const T`, prefer `from_mut(m).cast_const()` to obtain a pointer that can later be",
    "nanvix_source": "  1033: /// since it is generally not possible to actually *compute* which provenance the returned\n  1034: /// pointer has to pick up.\n  1035: ///\n  1036: /// This is an [Exposed Provenance][crate::ptr#exposed-provenance] API.\n  1037: #[must_use]\n  1038: #[inline(always)]\n  1039: #[stable(feature = \"exposed_provenance\", since = \"1.84.0\")]\n  1040: #[rustc_const_stable(feature = \"const_exposed_provenance\", since = \"1.91.0\")]\n  1041: #[cfg_attr(miri, track_caller)] // even without panics, this helps for Miri backtraces\n  1042: #[allow(implicit_provenance_casts)] // this *is* the explicit provenance API one should use instead\n  1043: pub const fn with_exposed_provenance_mut<T>(addr: usize) -> *mut T {\n  1044:     addr as *mut T\n  1045: }\n  1046: \n  1047: /// Converts a reference to a raw pointer.\n  1048: ///\n  1049: /// For `r: &T`, `from_ref(r)` is equivalent to `r as *const T` (except for the caveat noted below),\n  1050: /// but is a bit safer since it will never silently change type or mutability, in particular if the\n  1051: /// code is refactored.\n  1052: ///\n  1053: /// The caller must ensure that the pointee outlives the pointer this function returns, or else it",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::without_provenance",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
        "is_unsafe": false
      },
      "name": "without_provenance",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   873: /// This is equivalent to `ptr::null().with_addr(addr)`.\n   874: ///\n   875: /// Without provenance, this pointer is not associated with any actual allocation. Such a\n   876: /// no-provenance pointer may be used for zero-sized memory accesses (if suitably aligned), but\n   877: /// non-zero-sized memory accesses with a no-provenance pointer are UB. No-provenance pointers are\n   878: /// little more than a `usize` address in disguise.\n   879: ///\n   880: /// This is different from `addr as *const T`, which creates a pointer that picks up a previously\n   881: /// exposed provenance. See [`with_exposed_provenance`] for more details on that operation.\n   882: ///\n   883: /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   884: #[inline(always)]\n   885: #[must_use]\n   886: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   887: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   888: #[rustc_diagnostic_item = \"ptr_without_provenance\"]\n   889: pub const fn without_provenance<T>(addr: usize) -> *const T {\n   890:     without_provenance_mut(addr)\n   891: }\n   892: \n   893: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   894: ///\n   895: /// This is useful for initializing types which lazily allocate, like\n   896: /// `Vec::new` does.\n   897: ///\n   898: /// Note that the address of the returned pointer may potentially\n   899: /// be that of a valid pointer, which means this must not be used\n   900: /// as a \"not yet initialized\" sentinel value.\n   901: /// Types that lazily allocate must track initialization by some other means.\n   902: #[inline(always)]\n   903: #[must_use]\n   904: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   905: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]",
    "nanvix_source": "   889: ///\n   890: /// This is different from `addr as *const T`, which creates a pointer that picks up a previously\n   891: /// exposed provenance. See [`with_exposed_provenance`] for more details on that operation.\n   892: ///\n   893: /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   894: #[inline(always)]\n   895: #[must_use]\n   896: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   897: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   898: #[rustc_diagnostic_item = \"ptr_without_provenance\"]\n   899: pub const fn without_provenance<T>(addr: usize) -> *const T {\n   900:     without_provenance_mut(addr)\n   901: }\n   902: \n   903: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   904: ///\n   905: /// This is useful for initializing types which lazily allocate, like\n   906: /// `Vec::new` does.\n   907: ///\n   908: /// Note that the address of the returned pointer may potentially\n   909: /// be that of a valid pointer, which means this must not be used",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::without_provenance_mut",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "memory_pointer",
    "kinds": [
      "free_function"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
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
        "is_unsafe": false
      },
      "name": "without_provenance_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "addr",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   913: ///\n   914: /// Without provenance, this pointer is not associated with any actual allocation. Such a\n   915: /// no-provenance pointer may be used for zero-sized memory accesses (if suitably aligned), but\n   916: /// non-zero-sized memory accesses with a no-provenance pointer are UB. No-provenance pointers are\n   917: /// little more than a `usize` address in disguise.\n   918: ///\n   919: /// This is different from `addr as *mut T`, which creates a pointer that picks up a previously\n   920: /// exposed provenance. See [`with_exposed_provenance_mut`] for more details on that operation.\n   921: ///\n   922: /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   923: #[inline(always)]\n   924: #[must_use]\n   925: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   926: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   927: #[rustc_diagnostic_item = \"ptr_without_provenance_mut\"]\n   928: #[allow(integer_to_ptr_transmutes)] // Expected semantics here.\n   929: pub const fn without_provenance_mut<T>(addr: usize) -> *mut T {\n   930:     // An int-to-pointer transmute currently has exactly the intended semantics: it creates a\n   931:     // pointer without provenance. Note that this is *not* a stable guarantee about transmute\n   932:     // semantics, it relies on sysroot crates having special status.\n   933:     // SAFETY: every valid integer is also a valid pointer (as long as you don't dereference that\n   934:     // pointer).\n   935:     unsafe { mem::transmute(addr) }\n   936: }\n   937: \n   938: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   939: ///\n   940: /// This is useful for initializing types which lazily allocate, like\n   941: /// `Vec::new` does.\n   942: ///\n   943: /// Note that the address of the returned pointer may potentially\n   944: /// be that of a valid pointer, which means this must not be used\n   945: /// as a \"not yet initialized\" sentinel value.",
    "nanvix_source": "   929: /// This is different from `addr as *mut T`, which creates a pointer that picks up a previously\n   930: /// exposed provenance. See [`with_exposed_provenance_mut`] for more details on that operation.\n   931: ///\n   932: /// This is a [Strict Provenance][crate::ptr#strict-provenance] API.\n   933: #[inline(always)]\n   934: #[must_use]\n   935: #[stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   936: #[rustc_const_stable(feature = \"strict_provenance\", since = \"1.84.0\")]\n   937: #[rustc_diagnostic_item = \"ptr_without_provenance_mut\"]\n   938: #[allow(integer_to_ptr_transmutes)] // Expected semantics here.\n   939: pub const fn without_provenance_mut<T>(addr: usize) -> *mut T {\n   940:     // An int-to-pointer transmute currently has exactly the intended semantics: it creates a\n   941:     // pointer without provenance. Note that this is *not* a stable guarantee about transmute\n   942:     // semantics, it relies on sysroot crates having special status.\n   943:     // SAFETY: every valid integer is also a valid pointer (as long as you don't dereference that\n   944:     // pointer).\n   945:     unsafe { mem::transmute(addr) }\n   946: }\n   947: \n   948: /// Creates a new pointer that is dangling, but non-null and well-aligned.\n   949: ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ptr::wrapping_add",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "multiple_rust_declarations_share_path"
    ],
    "category": "memory_pointer",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "multiple_rust_declarations_share_path"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 12,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "wrapping_add",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        },
        "generics": {
          "params": [
            {
              "kind": {
                "type": {
                  "bounds": [
                    {
                      "trait_bound": {
                        "generic_params": [],
                        "modifier": "none",
                        "trait": {
                          "args": null,
                          "id": 7872,
                          "path": "PointeeSized"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "T"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51637",
        "kind": "inherent_impl",
        "resolved_owner_id": null,
        "resolved_owner_path": null,
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
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
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "  1037:     /// let end_rounded_up = ptr.wrapping_add(6);\n  1038:     ///\n  1039:     /// let mut out = String::new();\n  1040:     /// while ptr != end_rounded_up {\n  1041:     ///     unsafe {\n  1042:     ///         write!(&mut out, \"{}, \", *ptr)?;\n  1043:     ///     }\n  1044:     ///     ptr = ptr.wrapping_add(step);\n  1045:     /// }\n  1046:     /// assert_eq!(out, \"1, 3, 5, \");\n  1047:     /// # std::fmt::Result::Ok(())\n  1048:     /// ```\n  1049:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1050:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n  1051:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n  1052:     #[inline(always)]\n  1053:     pub const fn wrapping_add(self, count: usize) -> Self\n  1054:     where\n  1055:         T: Sized,\n  1056:     {\n  1057:         self.wrapping_offset(count as isize)\n  1058:     }\n  1059: \n  1060:     /// Adds an unsigned offset in bytes to a pointer using wrapping arithmetic.\n  1061:     ///\n  1062:     /// `count` is in units of bytes.\n  1063:     ///\n  1064:     /// This is purely a convenience for casting to a `u8` pointer and\n  1065:     /// using [wrapping_add][pointer::wrapping_add] on it. See that method for documentation.\n  1066:     ///\n  1067:     /// For non-`Sized` pointees this operation changes only the data pointer,\n  1068:     /// leaving the metadata untouched.\n  1069:     #[must_use]",
    "nanvix_source": "  1025:     ///     }\n  1026:     ///     ptr = ptr.wrapping_add(step);\n  1027:     /// }\n  1028:     /// assert_eq!(out, \"1, 3, 5, \");\n  1029:     /// # std::fmt::Result::Ok(())\n  1030:     /// ```\n  1031:     #[stable(feature = \"pointer_methods\", since = \"1.26.0\")]\n  1032:     #[must_use = \"returns a new pointer rather than modifying its argument\"]\n  1033:     #[rustc_const_stable(feature = \"const_ptr_offset\", since = \"1.61.0\")]\n  1034:     #[inline(always)]\n  1035:     pub const fn wrapping_add(self, count: usize) -> Self\n  1036:     where\n  1037:         T: Sized,\n  1038:     {\n  1039:         self.wrapping_offset(count as isize)\n  1040:     }\n  1041: \n  1042:     /// Adds an unsigned offset in bytes to a pointer using wrapping arithmetic.\n  1043:     ///\n  1044:     /// `count` is in units of bytes.\n  1045:     ///",
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
