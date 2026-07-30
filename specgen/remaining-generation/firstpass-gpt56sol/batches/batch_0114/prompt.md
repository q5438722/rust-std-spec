For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::alloc::Layout::for_value",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
    ],
    "available_in_verus_rust_1_96": true,
    "recommended_contract_form": "assume_specification",
    "verification_signature": {
      "generics": {
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe",
                      "trait": {
                        "args": null,
                        "id": 12,
                        "path": "Sized"
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
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": false
      },
      "name": "for_value",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "t",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "T"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   201:     /// Constructs a `Layout` suitable for holding a value of type `T`.\n   202:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   203:     #[rustc_const_stable(feature = \"alloc_layout_const_new\", since = \"1.42.0\")]\n   204:     #[must_use]\n   205:     #[inline]\n   206:     pub const fn new<T>() -> Self {\n   207:         <T as SizedTypeProperties>::LAYOUT\n   208:     }\n   209: \n   210:     /// Produces layout describing a record that could be used to\n   211:     /// allocate backing structure for `T` (which could be a trait\n   212:     /// or other unsized type like a slice).\n   213:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   214:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   215:     #[must_use]\n   216:     #[inline]\n   217:     pub const fn for_value<T: ?Sized>(t: &T) -> Self {\n   218:         let (size, alignment) = (size_of_val(t), Alignment::of_val(t));\n   219:         // SAFETY: see rationale in `new` for why this is using the unsafe variant\n   220:         unsafe { Layout::from_size_alignment_unchecked(size, alignment) }\n   221:     }\n   222: \n   223:     /// Produces layout describing a record that could be used to\n   224:     /// allocate backing structure for `T` (which could be a trait\n   225:     /// or other unsized type like a slice).\n   226:     ///\n   227:     /// # Safety\n   228:     ///\n   229:     /// This function is only safe to call if the following conditions hold:\n   230:     ///\n   231:     /// - If `T` is `Sized`, this function is always safe to call.\n   232:     /// - If the unsized tail of `T` is:\n   233:     ///     - a [slice], then the length of the slice tail must be an initialized",
    "nanvix_source": "   207:         <T as SizedTypeProperties>::LAYOUT\n   208:     }\n   209: \n   210:     /// Produces layout describing a record that could be used to\n   211:     /// allocate backing structure for `T` (which could be a trait\n   212:     /// or other unsized type like a slice).\n   213:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   214:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   215:     #[must_use]\n   216:     #[inline]\n   217:     pub const fn for_value<T: ?Sized>(t: &T) -> Self {\n   218:         let (size, alignment) = (size_of_val(t), Alignment::of_val(t));\n   219:         // SAFETY: see rationale in `new` for why this is using the unsafe variant\n   220:         unsafe { Layout::from_size_alignment_unchecked(size, alignment) }\n   221:     }\n   222: \n   223:     /// Produces layout describing a record that could be used to\n   224:     /// allocate backing structure for `T` (which could be a trait\n   225:     /// or other unsized type like a slice).\n   226:     ///\n   227:     /// # Safety",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::from_size_align",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
        "is_unsafe": false
      },
      "name": "from_size_align",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "size",
            {
              "primitive": "usize"
            }
          ],
          [
            "align",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10215,
                        "path": "LayoutError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "    43: \n    44: impl Layout {\n    45:     /// Constructs a `Layout` from a given `size` and `align`,\n    46:     /// or returns `LayoutError` if any of the following conditions\n    47:     /// are not met:\n    48:     ///\n    49:     /// * `align` must not be zero,\n    50:     ///\n    51:     /// * `align` must be a power of two,\n    52:     ///\n    53:     /// * `size`, when rounded up to the nearest multiple of `align`,\n    54:     ///   must not overflow `isize` (i.e., the rounded value must be\n    55:     ///   less than or equal to `isize::MAX`).\n    56:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n    57:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n    58:     #[inline]\n    59:     pub const fn from_size_align(size: usize, align: usize) -> Result<Self, LayoutError> {\n    60:         if Layout::is_size_align_valid(size, align) {\n    61:             // SAFETY: Layout::is_size_align_valid checks the preconditions for this call.\n    62:             unsafe { Ok(Layout { size, align: mem::transmute(align) }) }\n    63:         } else {\n    64:             Err(LayoutError)\n    65:         }\n    66:     }\n    67: \n    68:     #[inline]\n    69:     const fn is_size_align_valid(size: usize, align: usize) -> bool {\n    70:         let Some(alignment) = Alignment::new(align) else { return false };\n    71:         Self::is_size_alignment_valid(size, alignment)\n    72:     }\n    73: \n    74:     const fn is_size_alignment_valid(size: usize, alignment: Alignment) -> bool {\n    75:         size <= Self::max_size_for_alignment(alignment)",
    "nanvix_source": "    49:     /// * `align` must not be zero,\n    50:     ///\n    51:     /// * `align` must be a power of two,\n    52:     ///\n    53:     /// * `size`, when rounded up to the nearest multiple of `align`,\n    54:     ///   must not overflow `isize` (i.e., the rounded value must be\n    55:     ///   less than or equal to `isize::MAX`).\n    56:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n    57:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n    58:     #[inline]\n    59:     pub const fn from_size_align(size: usize, align: usize) -> Result<Self, LayoutError> {\n    60:         if Layout::is_size_align_valid(size, align) {\n    61:             // SAFETY: Layout::is_size_align_valid checks the preconditions for this call.\n    62:             unsafe { Ok(Layout { size, align: mem::transmute(align) }) }\n    63:         } else {\n    64:             Err(LayoutError)\n    65:         }\n    66:     }\n    67: \n    68:     #[inline]\n    69:     const fn is_size_align_valid(size: usize, align: usize) -> bool {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
      "name": "new",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "generic": "Self"
        }
      }
    },
    "verification_source": "   190: \n   191:     /// The minimum byte alignment for a memory block of this layout.\n   192:     ///\n   193:     /// The returned alignment is guaranteed to be a power of two.\n   194:     #[unstable(feature = \"ptr_alignment_type\", issue = \"102070\")]\n   195:     #[must_use = \"this returns the minimum alignment, without modifying the layout\"]\n   196:     #[inline]\n   197:     pub const fn alignment(&self) -> Alignment {\n   198:         self.align\n   199:     }\n   200: \n   201:     /// Constructs a `Layout` suitable for holding a value of type `T`.\n   202:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   203:     #[rustc_const_stable(feature = \"alloc_layout_const_new\", since = \"1.42.0\")]\n   204:     #[must_use]\n   205:     #[inline]\n   206:     pub const fn new<T>() -> Self {\n   207:         <T as SizedTypeProperties>::LAYOUT\n   208:     }\n   209: \n   210:     /// Produces layout describing a record that could be used to\n   211:     /// allocate backing structure for `T` (which could be a trait\n   212:     /// or other unsized type like a slice).\n   213:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   214:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   215:     #[must_use]\n   216:     #[inline]\n   217:     pub const fn for_value<T: ?Sized>(t: &T) -> Self {\n   218:         let (size, alignment) = (size_of_val(t), Alignment::of_val(t));\n   219:         // SAFETY: see rationale in `new` for why this is using the unsafe variant\n   220:         unsafe { Layout::from_size_alignment_unchecked(size, alignment) }\n   221:     }\n   222: ",
    "nanvix_source": "   196:     #[inline]\n   197:     pub const fn alignment(&self) -> Alignment {\n   198:         self.align\n   199:     }\n   200: \n   201:     /// Constructs a `Layout` suitable for holding a value of type `T`.\n   202:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   203:     #[rustc_const_stable(feature = \"alloc_layout_const_new\", since = \"1.42.0\")]\n   204:     #[must_use]\n   205:     #[inline]\n   206:     pub const fn new<T>() -> Self {\n   207:         <T as SizedTypeProperties>::LAYOUT\n   208:     }\n   209: \n   210:     /// Produces layout describing a record that could be used to\n   211:     /// allocate backing structure for `T` (which could be a trait\n   212:     /// or other unsized type like a slice).\n   213:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   214:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   215:     #[must_use]\n   216:     #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::pad_to_align",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
        "is_unsafe": false
      },
      "name": "pad_to_align",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        }
      }
    },
    "verification_source": "   365:         unsafe {\n   366:             let align_m1 = unchecked_sub(alignment.as_usize(), 1);\n   367:             unchecked_add(self.size, align_m1) & !align_m1\n   368:         }\n   369:     }\n   370: \n   371:     /// Creates a layout by rounding the size of this layout up to a multiple\n   372:     /// of the layout's alignment.\n   373:     ///\n   374:     /// This is equivalent to adding the result of `padding_needed_for`\n   375:     /// to the layout's current size.\n   376:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   377:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   378:     #[must_use = \"this returns a new `Layout`, \\\n   379:                   without modifying the original\"]\n   380:     #[inline]\n   381:     pub const fn pad_to_align(&self) -> Layout {\n   382:         // This cannot overflow. Quoting from the invariant of Layout:\n   383:         // > `size`, when rounded up to the nearest multiple of `align`,\n   384:         // > must not overflow isize (i.e., the rounded value must be\n   385:         // > less than or equal to `isize::MAX`)\n   386:         let new_size = self.size_rounded_up_to_custom_alignment(self.align);\n   387: \n   388:         // SAFETY: padded size is guaranteed to not exceed `isize::MAX`.\n   389:         unsafe { Layout::from_size_alignment_unchecked(new_size, self.alignment()) }\n   390:     }\n   391: \n   392:     /// Creates a layout describing the record for `n` instances of\n   393:     /// `self`, with a suitable amount of padding between each to\n   394:     /// ensure that each instance is given its requested size and\n   395:     /// alignment. On success, returns `(k, offs)` where `k` is the\n   396:     /// layout of the array and `offs` is the distance between the start\n   397:     /// of each element in the array.",
    "nanvix_source": "   371:     /// Creates a layout by rounding the size of this layout up to a multiple\n   372:     /// of the layout's alignment.\n   373:     ///\n   374:     /// This is equivalent to adding the result of `padding_needed_for`\n   375:     /// to the layout's current size.\n   376:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   377:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   378:     #[must_use = \"this returns a new `Layout`, \\\n   379:                   without modifying the original\"]\n   380:     #[inline]\n   381:     pub const fn pad_to_align(&self) -> Layout {\n   382:         // This cannot overflow. Quoting from the invariant of Layout:\n   383:         // > `size`, when rounded up to the nearest multiple of `align`,\n   384:         // > must not overflow isize (i.e., the rounded value must be\n   385:         // > less than or equal to `isize::MAX`)\n   386:         let new_size = self.size_rounded_up_to_custom_alignment(self.align);\n   387: \n   388:         // SAFETY: padded size is guaranteed to not exceed `isize::MAX`.\n   389:         unsafe { Layout::from_size_alignment_unchecked(new_size, self.alignment()) }\n   390:     }\n   391: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::repeat",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
        "is_unsafe": false
      },
      "name": "repeat",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
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
            "n",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "tuple": [
                        {
                          "generic": "Self"
                        },
                        {
                          "primitive": "usize"
                        }
                      ]
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10215,
                        "path": "LayoutError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   413:     /// assert_eq!(repeated, (Layout::from_size_align(36, 4).unwrap(), 12));\n   414:     ///\n   415:     /// // But you can manually make layouts which don't meet that rule.\n   416:     /// let padding_needed = Layout::from_size_align(6, 4).unwrap();\n   417:     /// let repeated = padding_needed.repeat(3).unwrap();\n   418:     /// assert_eq!(repeated, (Layout::from_size_align(22, 4).unwrap(), 8));\n   419:     ///\n   420:     /// // Repeating an element zero times has zero size, but keeps the alignment (like `[T; 0]`)\n   421:     /// let repeated = normal.repeat(0).unwrap();\n   422:     /// assert_eq!(repeated, (Layout::from_size_align(0, 4).unwrap(), 12));\n   423:     /// let repeated = padding_needed.repeat(0).unwrap();\n   424:     /// assert_eq!(repeated, (Layout::from_size_align(0, 4).unwrap(), 8));\n   425:     /// ```\n   426:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   427:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   428:     #[inline]\n   429:     pub const fn repeat(&self, n: usize) -> Result<(Self, usize), LayoutError> {\n   430:         // FIXME(const-hack): the following could be way shorter with `?`\n   431:         let padded = self.pad_to_align();\n   432:         let Ok(result) = (if let Some(k) = n.checked_sub(1) {\n   433:             let Ok(repeated) = padded.repeat_packed(k) else {\n   434:                 return Err(LayoutError);\n   435:             };\n   436:             repeated.extend_packed(*self)\n   437:         } else {\n   438:             debug_assert!(n == 0);\n   439:             self.repeat_packed(0)\n   440:         }) else {\n   441:             return Err(LayoutError);\n   442:         };\n   443:         Ok((result, padded.size()))\n   444:     }\n   445: ",
    "nanvix_source": "   419:     ///\n   420:     /// // Repeating an element zero times has zero size, but keeps the alignment (like `[T; 0]`)\n   421:     /// let repeated = normal.repeat(0).unwrap();\n   422:     /// assert_eq!(repeated, (Layout::from_size_align(0, 4).unwrap(), 12));\n   423:     /// let repeated = padding_needed.repeat(0).unwrap();\n   424:     /// assert_eq!(repeated, (Layout::from_size_align(0, 4).unwrap(), 8));\n   425:     /// ```\n   426:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   427:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   428:     #[inline]\n   429:     pub const fn repeat(&self, n: usize) -> Result<(Self, usize), LayoutError> {\n   430:         // FIXME(const-hack): the following could be way shorter with `?`\n   431:         let padded = self.pad_to_align();\n   432:         let Ok(result) = (if let Some(k) = n.checked_sub(1) {\n   433:             let Ok(repeated) = padded.repeat_packed(k) else {\n   434:                 return Err(LayoutError);\n   435:             };\n   436:             repeated.extend_packed(*self)\n   437:         } else {\n   438:             debug_assert!(n == 0);\n   439:             self.repeat_packed(0)",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::repeat_packed",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "memory_pointer",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "unsafe_or_ownership_sensitive"
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
        "is_unsafe": false
      },
      "name": "repeat_packed",
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
          "resolved_path": {
            "args": null,
            "id": 9440,
            "path": "Layout"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:32780",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9440",
        "resolved_owner_path": [
          "core",
          "alloc",
          "layout",
          "Layout"
        ],
        "trait": null
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
            "n",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "Self"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 10215,
                        "path": "LayoutError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   510: \n   511:     /// Creates a layout describing the record for `n` instances of\n   512:     /// `self`, with no padding between each instance.\n   513:     ///\n   514:     /// Note that, unlike `repeat`, `repeat_packed` does not guarantee\n   515:     /// that the repeated instances of `self` will be properly\n   516:     /// aligned, even if a given instance of `self` is properly\n   517:     /// aligned. In other words, if the layout returned by\n   518:     /// `repeat_packed` is used to allocate an array, it is not\n   519:     /// guaranteed that all elements in the array will be properly\n   520:     /// aligned.\n   521:     ///\n   522:     /// On arithmetic overflow, returns `LayoutError`.\n   523:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   524:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   525:     #[inline]\n   526:     pub const fn repeat_packed(&self, n: usize) -> Result<Self, LayoutError> {\n   527:         if let Some(size) = self.size.checked_mul(n) {\n   528:             // The safe constructor is called here to enforce the isize size limit.\n   529:             Layout::from_size_alignment(size, self.align)\n   530:         } else {\n   531:             Err(LayoutError)\n   532:         }\n   533:     }\n   534: \n   535:     /// Creates a layout describing the record for `self` followed by\n   536:     /// `next` with no additional padding between the two. Since no\n   537:     /// padding is inserted, the alignment of `next` is irrelevant,\n   538:     /// and is not incorporated *at all* into the resulting layout.\n   539:     ///\n   540:     /// On arithmetic overflow, returns `LayoutError`.\n   541:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   542:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]",
    "nanvix_source": "   516:     /// aligned, even if a given instance of `self` is properly\n   517:     /// aligned. In other words, if the layout returned by\n   518:     /// `repeat_packed` is used to allocate an array, it is not\n   519:     /// guaranteed that all elements in the array will be properly\n   520:     /// aligned.\n   521:     ///\n   522:     /// On arithmetic overflow, returns `LayoutError`.\n   523:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   524:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   525:     #[inline]\n   526:     pub const fn repeat_packed(&self, n: usize) -> Result<Self, LayoutError> {\n   527:         if let Some(size) = self.size.checked_mul(n) {\n   528:             // The safe constructor is called here to enforce the isize size limit.\n   529:             Layout::from_size_alignment(size, self.align)\n   530:         } else {\n   531:             Err(LayoutError)\n   532:         }\n   533:     }\n   534: \n   535:     /// Creates a layout describing the record for `self` followed by\n   536:     /// `next` with no additional padding between the two. Since no",
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
