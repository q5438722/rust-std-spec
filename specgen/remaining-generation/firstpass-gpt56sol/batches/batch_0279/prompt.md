For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::borrow::ToOwned::clone_into",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "clone_into",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "target"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "alloc:26",
        "kind": "trait",
        "name": "ToOwned",
        "path": [
          "alloc",
          "borrow",
          "ToOwned"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "target",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "qualified_path": {
                    "args": null,
                    "name": "Owned",
                    "self_type": {
                      "generic": "Self"
                    },
                    "trait": {
                      "args": null,
                      "id": 26,
                      "path": ""
                    }
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "    50:     /// Uses borrowed data to replace owned data, usually by cloning.\n    51:     ///\n    52:     /// This is borrow-generalized version of [`Clone::clone_from`].\n    53:     ///\n    54:     /// # Examples\n    55:     ///\n    56:     /// Basic usage:\n    57:     ///\n    58:     /// ```\n    59:     /// let mut s: String = String::new();\n    60:     /// \"hello\".clone_into(&mut s);\n    61:     ///\n    62:     /// let mut v: Vec<i32> = Vec::new();\n    63:     /// [1, 2][..].clone_into(&mut v);\n    64:     /// ```\n    65:     #[stable(feature = \"toowned_clone_into\", since = \"1.63.0\")]\n    66:     fn clone_into(&self, target: &mut Self::Owned) {\n    67:         *target = self.to_owned();\n    68:     }\n    69: }\n    70: \n    71: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    72: impl<T> ToOwned for T\n    73: where\n    74:     T: Clone,\n    75: {\n    76:     type Owned = T;\n    77:     fn to_owned(&self) -> T {\n    78:         self.clone()\n    79:     }\n    80: \n    81:     fn clone_into(&self, target: &mut T) {\n    82:         target.clone_from(self);",
    "nanvix_source": "    56:     /// Basic usage:\n    57:     ///\n    58:     /// ```\n    59:     /// let mut s: String = String::new();\n    60:     /// \"hello\".clone_into(&mut s);\n    61:     ///\n    62:     /// let mut v: Vec<i32> = Vec::new();\n    63:     /// [1, 2][..].clone_into(&mut v);\n    64:     /// ```\n    65:     #[stable(feature = \"toowned_clone_into\", since = \"1.63.0\")]\n    66:     fn clone_into(&self, target: &mut Self::Owned) {\n    67:         *target = self.to_owned();\n    68:     }\n    69: }\n    70: \n    71: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    72: impl<T> ToOwned for T\n    73: where\n    74:     T: Clone,\n    75: {\n    76:     type Owned = T;",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::borrow::ToOwned::to_owned",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
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
      "name": "to_owned",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "alloc:26",
        "kind": "trait",
        "name": "ToOwned",
        "path": [
          "alloc",
          "borrow",
          "ToOwned"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "qualified_path": {
            "args": null,
            "name": "Owned",
            "self_type": {
              "generic": "Self"
            },
            "trait": {
              "args": null,
              "id": 26,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "    32:     /// Creates owned data from borrowed data, usually by cloning.\n    33:     ///\n    34:     /// # Examples\n    35:     ///\n    36:     /// Basic usage:\n    37:     ///\n    38:     /// ```\n    39:     /// let s: &str = \"a\";\n    40:     /// let ss: String = s.to_owned();\n    41:     ///\n    42:     /// let v: &[i32] = &[1, 2];\n    43:     /// let vv: Vec<i32> = v.to_owned();\n    44:     /// ```\n    45:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46:     #[must_use = \"cloning is often expensive and is not expected to have side effects\"]\n    47:     #[rustc_diagnostic_item = \"to_owned_method\"]\n    48:     fn to_owned(&self) -> Self::Owned;\n    49: \n    50:     /// Uses borrowed data to replace owned data, usually by cloning.\n    51:     ///\n    52:     /// This is borrow-generalized version of [`Clone::clone_from`].\n    53:     ///\n    54:     /// # Examples\n    55:     ///\n    56:     /// Basic usage:\n    57:     ///\n    58:     /// ```\n    59:     /// let mut s: String = String::new();\n    60:     /// \"hello\".clone_into(&mut s);\n    61:     ///\n    62:     /// let mut v: Vec<i32> = Vec::new();\n    63:     /// [1, 2][..].clone_into(&mut v);\n    64:     /// ```",
    "nanvix_source": "    38:     /// ```\n    39:     /// let s: &str = \"a\";\n    40:     /// let ss: String = s.to_owned();\n    41:     ///\n    42:     /// let v: &[i32] = &[1, 2];\n    43:     /// let vv: Vec<i32> = v.to_owned();\n    44:     /// ```\n    45:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n    46:     #[must_use = \"cloning is often expensive and is not expected to have side effects\"]\n    47:     #[rustc_diagnostic_item = \"to_owned_method\"]\n    48:     fn to_owned(&self) -> Self::Owned;\n    49: \n    50:     /// Uses borrowed data to replace owned data, usually by cloning.\n    51:     ///\n    52:     /// This is borrow-generalized version of [`Clone::clone_from`].\n    53:     ///\n    54:     /// # Examples\n    55:     ///\n    56:     /// Basic usage:\n    57:     ///\n    58:     /// ```",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::GlobalAlloc::alloc",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "alloc",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:32756",
        "kind": "trait",
        "name": "GlobalAlloc",
        "path": [
          "core",
          "alloc",
          "global",
          "GlobalAlloc"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 9440,
                "path": "Layout"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   162:     ///\n   163:     /// Returning a null pointer indicates that either memory is exhausted\n   164:     /// or `layout` does not meet this allocator's size or alignment constraints.\n   165:     ///\n   166:     /// Implementations are encouraged to return null on memory\n   167:     /// exhaustion rather than aborting, but this is not\n   168:     /// a strict requirement. (Specifically: it is *legal* to\n   169:     /// implement this trait atop an underlying native allocation\n   170:     /// library that aborts on memory exhaustion.)\n   171:     ///\n   172:     /// Clients wishing to abort computation in response to an\n   173:     /// allocation error are encouraged to call the [`handle_alloc_error`] function,\n   174:     /// rather than directly invoking `panic!` or similar.\n   175:     ///\n   176:     /// [`handle_alloc_error`]: ../../alloc/alloc/fn.handle_alloc_error.html\n   177:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   178:     unsafe fn alloc(&self, layout: Layout) -> *mut u8;\n   179: \n   180:     /// Deallocates the block of memory at the given `ptr` pointer with the given `layout`.\n   181:     ///\n   182:     /// # Safety\n   183:     ///\n   184:     /// The caller must ensure:\n   185:     ///\n   186:     /// * `ptr` is a block of memory currently allocated via this allocator and,\n   187:     ///\n   188:     /// * `layout` is the same layout that was used to allocate that block of\n   189:     ///   memory.\n   190:     ///\n   191:     /// Otherwise the behavior is undefined.\n   192:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   193:     unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout);\n   194: ",
    "nanvix_source": "   168:     /// a strict requirement. (Specifically: it is *legal* to\n   169:     /// implement this trait atop an underlying native allocation\n   170:     /// library that aborts on memory exhaustion.)\n   171:     ///\n   172:     /// Clients wishing to abort computation in response to an\n   173:     /// allocation error are encouraged to call the [`handle_alloc_error`] function,\n   174:     /// rather than directly invoking `panic!` or similar.\n   175:     ///\n   176:     /// [`handle_alloc_error`]: ../../alloc/alloc/fn.handle_alloc_error.html\n   177:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   178:     unsafe fn alloc(&self, layout: Layout) -> *mut u8;\n   179: \n   180:     /// Deallocates the block of memory at the given `ptr` pointer with the given `layout`.\n   181:     ///\n   182:     /// # Safety\n   183:     ///\n   184:     /// The caller must ensure:\n   185:     ///\n   186:     /// * `ptr` is a block of memory currently allocated via this allocator and,\n   187:     ///\n   188:     /// * `layout` is the same layout that was used to allocate that block of",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::GlobalAlloc::alloc_zeroed",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "alloc_zeroed",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:32756",
        "kind": "trait",
        "name": "GlobalAlloc",
        "path": [
          "core",
          "alloc",
          "global",
          "GlobalAlloc"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 9440,
                "path": "Layout"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "raw_pointer": {
            "is_mutable": true,
            "type": {
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   200:     /// The caller has to ensure that `layout` has non-zero size. Like `alloc`\n   201:     /// zero sized `layout` will result in undefined behavior.\n   202:     /// However the allocated block of memory is guaranteed to be initialized.\n   203:     ///\n   204:     /// # Errors\n   205:     ///\n   206:     /// Returning a null pointer indicates that either memory is exhausted\n   207:     /// or `layout` does not meet allocator's size or alignment constraints,\n   208:     /// just as in `alloc`.\n   209:     ///\n   210:     /// Clients wishing to abort computation in response to an\n   211:     /// allocation error are encouraged to call the [`handle_alloc_error`] function,\n   212:     /// rather than directly invoking `panic!` or similar.\n   213:     ///\n   214:     /// [`handle_alloc_error`]: ../../alloc/alloc/fn.handle_alloc_error.html\n   215:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   216:     unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {\n   217:         let size = layout.size();\n   218:         // SAFETY: the safety contract for `alloc` must be upheld by the caller.\n   219:         let ptr = unsafe { self.alloc(layout) };\n   220:         if !ptr.is_null() {\n   221:             // SAFETY: as allocation succeeded, the region from `ptr`\n   222:             // of size `size` is guaranteed to be valid for writes.\n   223:             unsafe { ptr::write_bytes(ptr, 0, size) };\n   224:         }\n   225:         ptr\n   226:     }\n   227: \n   228:     /// Shrinks or grows a block of memory to the given `new_size` in bytes.\n   229:     /// The block is described by the given `ptr` pointer and `layout`.\n   230:     ///\n   231:     /// If this returns a non-null pointer, then ownership of the memory block\n   232:     /// referenced by `ptr` has been transferred to this allocator.",
    "nanvix_source": "   206:     /// Returning a null pointer indicates that either memory is exhausted\n   207:     /// or `layout` does not meet allocator's size or alignment constraints,\n   208:     /// just as in `alloc`.\n   209:     ///\n   210:     /// Clients wishing to abort computation in response to an\n   211:     /// allocation error are encouraged to call the [`handle_alloc_error`] function,\n   212:     /// rather than directly invoking `panic!` or similar.\n   213:     ///\n   214:     /// [`handle_alloc_error`]: ../../alloc/alloc/fn.handle_alloc_error.html\n   215:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   216:     unsafe fn alloc_zeroed(&self, layout: Layout) -> *mut u8 {\n   217:         let size = layout.size();\n   218:         // SAFETY: the safety contract for `alloc` must be upheld by the caller.\n   219:         let ptr = unsafe { self.alloc(layout) };\n   220:         if !ptr.is_null() {\n   221:             // SAFETY: as allocation succeeded, the region from `ptr`\n   222:             // of size `size` is guaranteed to be valid for writes.\n   223:             unsafe { ptr::write_bytes(ptr, 0, size) };\n   224:         }\n   225:         ptr\n   226:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::GlobalAlloc::dealloc",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "unit_return_variant"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "dealloc",
      "observability": {
        "has_modeled_output": false,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:32756",
        "kind": "trait",
        "name": "GlobalAlloc",
        "path": [
          "core",
          "alloc",
          "global",
          "GlobalAlloc"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "u8"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 9440,
                "path": "Layout"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   177:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   178:     unsafe fn alloc(&self, layout: Layout) -> *mut u8;\n   179: \n   180:     /// Deallocates the block of memory at the given `ptr` pointer with the given `layout`.\n   181:     ///\n   182:     /// # Safety\n   183:     ///\n   184:     /// The caller must ensure:\n   185:     ///\n   186:     /// * `ptr` is a block of memory currently allocated via this allocator and,\n   187:     ///\n   188:     /// * `layout` is the same layout that was used to allocate that block of\n   189:     ///   memory.\n   190:     ///\n   191:     /// Otherwise the behavior is undefined.\n   192:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   193:     unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout);\n   194: \n   195:     /// Behaves like `alloc`, but also ensures that the contents\n   196:     /// are set to zero before being returned.\n   197:     ///\n   198:     /// # Safety\n   199:     ///\n   200:     /// The caller has to ensure that `layout` has non-zero size. Like `alloc`\n   201:     /// zero sized `layout` will result in undefined behavior.\n   202:     /// However the allocated block of memory is guaranteed to be initialized.\n   203:     ///\n   204:     /// # Errors\n   205:     ///\n   206:     /// Returning a null pointer indicates that either memory is exhausted\n   207:     /// or `layout` does not meet allocator's size or alignment constraints,\n   208:     /// just as in `alloc`.\n   209:     ///",
    "nanvix_source": "   183:     ///\n   184:     /// The caller must ensure:\n   185:     ///\n   186:     /// * `ptr` is a block of memory currently allocated via this allocator and,\n   187:     ///\n   188:     /// * `layout` is the same layout that was used to allocate that block of\n   189:     ///   memory.\n   190:     ///\n   191:     /// Otherwise the behavior is undefined.\n   192:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   193:     unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout);\n   194: \n   195:     /// Behaves like `alloc`, but also ensures that the contents\n   196:     /// are set to zero before being returned.\n   197:     ///\n   198:     /// # Safety\n   199:     ///\n   200:     /// The caller has to ensure that `layout` has non-zero size. Like `alloc`\n   201:     /// zero sized `layout` will result in undefined behavior.\n   202:     /// However the allocated block of memory is guaranteed to be initialized.\n   203:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::GlobalAlloc::realloc",
    "generation_group": "trait_contract_integration",
    "classification": "trait_contract_integration",
    "classification_reasons": [
      "requires_external_trait_specification_edit"
    ],
    "category": "trait_method",
    "kinds": [
      "trait_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive",
      "raw_pointer_equality"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "external_trait_specification",
    "verification_signature": {
      "generics": {
        "params": [],
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "realloc",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:32756",
        "kind": "trait",
        "name": "GlobalAlloc",
        "path": [
          "core",
          "alloc",
          "global",
          "GlobalAlloc"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "ptr",
            {
              "raw_pointer": {
                "is_mutable": true,
                "type": {
                  "primitive": "u8"
                }
              }
            }
          ],
          [
            "layout",
            {
              "resolved_path": {
                "args": null,
                "id": 9440,
                "path": "Layout"
              }
            }
          ],
          [
            "new_size",
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
              "primitive": "u8"
            }
          }
        }
      }
    },
    "verification_source": "   256:     /// * `new_size` is greater than zero.\n   257:     ///\n   258:     /// * `new_size`, when rounded up to the nearest multiple of `layout.align()`,\n   259:     ///   does not overflow `isize` (i.e., the rounded value must be less than or\n   260:     ///   equal to `isize::MAX`).\n   261:     ///\n   262:     /// If these are not followed, the behavior is undefined.\n   263:     ///\n   264:     /// (Extension subtraits might provide more specific bounds on\n   265:     /// behavior, e.g., guarantee a sentinel address or a null pointer\n   266:     /// in response to a zero-size allocation request.)\n   267:     ///\n   268:     /// # Errors\n   269:     ///\n   270:     /// Returns null if the new layout does not meet the size\n   271:     /// and alignment constraints of the allocator, or if reallocation\n   272:     /// otherwise fails.\n   273:     ///\n   274:     /// Implementations are encouraged to return null on memory\n   275:     /// exhaustion rather than panicking or aborting, but this is not\n   276:     /// a strict requirement. (Specifically: it is *legal* to\n   277:     /// implement this trait atop an underlying native allocation\n   278:     /// library that aborts on memory exhaustion.)\n   279:     ///\n   280:     /// Clients wishing to abort computation in response to a\n   281:     /// reallocation error are encouraged to call the [`handle_alloc_error`] function,\n   282:     /// rather than directly invoking `panic!` or similar.\n   283:     ///\n   284:     /// [`handle_alloc_error`]: ../../alloc/alloc/fn.handle_alloc_error.html\n   285:     #[stable(feature = \"global_alloc\", since = \"1.28.0\")]\n   286:     unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, new_size: usize) -> *mut u8 {\n   287:         let alignment = layout.alignment();\n   288:         // SAFETY: the caller must ensure that the `new_size` does not overflow",
    "nanvix_source": "   262:     /// If these are not followed, the behavior is undefined.\n   263:     ///\n   264:     /// (Extension subtraits might provide more specific bounds on\n   265:     /// behavior, e.g., guarantee a sentinel address or a null pointer\n   266:     /// in response to a zero-size allocation request.)\n   267:     ///\n   268:     /// # Errors\n   269:     ///\n   270:     /// Returns null if the new layout does not meet the size\n   271:     /// and alignment constraints of the allocator, or if reallocation\n   272:     /// otherwise fails.\n   273:     ///\n   274:     /// Implementations are encouraged to return null on memory\n   275:     /// exhaustion rather than panicking or aborting, but this is not\n   276:     /// a strict requirement. (Specifically: it is *legal* to\n   277:     /// implement this trait atop an underlying native allocation\n   278:     /// library that aborts on memory exhaustion.)\n   279:     ///\n   280:     /// Clients wishing to abort computation in response to a\n   281:     /// reallocation error are encouraged to call the [`handle_alloc_error`] function,\n   282:     /// rather than directly invoking `panic!` or similar.",
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
