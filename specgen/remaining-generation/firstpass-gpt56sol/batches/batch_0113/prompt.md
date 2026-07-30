For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::vec::IntoIter::as_slice",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "data_structure",
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_slice",
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 605,
            "path": "IntoIter"
          }
        },
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
            },
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
                          "id": 4,
                          "path": "Allocator"
                        }
                      }
                    }
                  ],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "alloc:4782",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:605",
        "resolved_owner_path": [
          "alloc",
          "vec",
          "into_iter",
          "IntoIter"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "slice": {
                "generic": "T"
              }
            }
          }
        }
      }
    },
    "verification_source": "    72:     }\n    73: }\n    74: \n    75: impl<T, A: Allocator> IntoIter<T, A> {\n    76:     /// Returns the remaining items of this iterator as a slice.\n    77:     ///\n    78:     /// # Examples\n    79:     ///\n    80:     /// ```\n    81:     /// let vec = vec!['a', 'b', 'c'];\n    82:     /// let mut into_iter = vec.into_iter();\n    83:     /// assert_eq!(into_iter.as_slice(), &['a', 'b', 'c']);\n    84:     /// let _ = into_iter.next().unwrap();\n    85:     /// assert_eq!(into_iter.as_slice(), &['b', 'c']);\n    86:     /// ```\n    87:     #[stable(feature = \"vec_into_iter_as_slice\", since = \"1.15.0\")]\n    88:     pub fn as_slice(&self) -> &[T] {\n    89:         unsafe { slice::from_raw_parts(self.ptr.as_ptr(), self.len()) }\n    90:     }\n    91: \n    92:     /// Returns the remaining items of this iterator as a mutable slice.\n    93:     ///\n    94:     /// # Examples\n    95:     ///\n    96:     /// ```\n    97:     /// let vec = vec!['a', 'b', 'c'];\n    98:     /// let mut into_iter = vec.into_iter();\n    99:     /// assert_eq!(into_iter.as_slice(), &['a', 'b', 'c']);\n   100:     /// into_iter.as_mut_slice()[2] = 'z';\n   101:     /// assert_eq!(into_iter.next().unwrap(), 'a');\n   102:     /// assert_eq!(into_iter.next().unwrap(), 'b');\n   103:     /// assert_eq!(into_iter.next().unwrap(), 'z');\n   104:     /// ```",
    "nanvix_source": "    78:     /// # Examples\n    79:     ///\n    80:     /// ```\n    81:     /// let vec = vec!['a', 'b', 'c'];\n    82:     /// let mut into_iter = vec.into_iter();\n    83:     /// assert_eq!(into_iter.as_slice(), &['a', 'b', 'c']);\n    84:     /// let _ = into_iter.next().unwrap();\n    85:     /// assert_eq!(into_iter.as_slice(), &['b', 'c']);\n    86:     /// ```\n    87:     #[stable(feature = \"vec_into_iter_as_slice\", since = \"1.15.0\")]\n    88:     pub fn as_slice(&self) -> &[T] {\n    89:         unsafe { slice::from_raw_parts(self.ptr.as_ptr(), self.len()) }\n    90:     }\n    91: \n    92:     /// Returns the remaining items of this iterator as a mutable slice.\n    93:     ///\n    94:     /// # Examples\n    95:     ///\n    96:     /// ```\n    97:     /// let vec = vec!['a', 'b', 'c'];\n    98:     /// let mut into_iter = vec.into_iter();",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::align",
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
      "name": "align",
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
          "primitive": "usize"
        }
      }
    },
    "verification_source": "   171:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   172:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   173:     #[must_use]\n   174:     #[inline]\n   175:     pub const fn size(&self) -> usize {\n   176:         self.size\n   177:     }\n   178: \n   179:     /// The minimum byte alignment for a memory block of this layout.\n   180:     ///\n   181:     /// The returned alignment is guaranteed to be a power of two.\n   182:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   183:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   184:     #[must_use = \"this returns the minimum alignment, \\\n   185:                   without modifying the layout\"]\n   186:     #[inline]\n   187:     pub const fn align(&self) -> usize {\n   188:         self.align.as_usize()\n   189:     }\n   190: \n   191:     /// The minimum byte alignment for a memory block of this layout.\n   192:     ///\n   193:     /// The returned alignment is guaranteed to be a power of two.\n   194:     #[unstable(feature = \"ptr_alignment_type\", issue = \"102070\")]\n   195:     #[must_use = \"this returns the minimum alignment, without modifying the layout\"]\n   196:     #[inline]\n   197:     pub const fn alignment(&self) -> Alignment {\n   198:         self.align\n   199:     }\n   200: \n   201:     /// Constructs a `Layout` suitable for holding a value of type `T`.\n   202:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   203:     #[rustc_const_stable(feature = \"alloc_layout_const_new\", since = \"1.42.0\")]",
    "nanvix_source": "   177:     }\n   178: \n   179:     /// The minimum byte alignment for a memory block of this layout.\n   180:     ///\n   181:     /// The returned alignment is guaranteed to be a power of two.\n   182:     #[stable(feature = \"alloc_layout\", since = \"1.28.0\")]\n   183:     #[rustc_const_stable(feature = \"const_alloc_layout_size_align\", since = \"1.50.0\")]\n   184:     #[must_use = \"this returns the minimum alignment, \\\n   185:                   without modifying the layout\"]\n   186:     #[inline]\n   187:     pub const fn align(&self) -> usize {\n   188:         self.align.as_usize()\n   189:     }\n   190: \n   191:     /// The minimum byte alignment for a memory block of this layout.\n   192:     ///\n   193:     /// The returned alignment is guaranteed to be a power of two.\n   194:     #[unstable(feature = \"ptr_alignment_type\", issue = \"102070\")]\n   195:     #[must_use = \"this returns the minimum alignment, without modifying the layout\"]\n   196:     #[inline]\n   197:     pub const fn alignment(&self) -> Alignment {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::align_to",
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
      "name": "align_to",
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
    "verification_source": "   275:     /// of the same layout as `self`, but that also is aligned to\n   276:     /// alignment `align` (measured in bytes).\n   277:     ///\n   278:     /// If `self` already meets the prescribed alignment, then returns\n   279:     /// `self`.\n   280:     ///\n   281:     /// Note that this method does not add any padding to the overall\n   282:     /// size, regardless of whether the returned layout has a different\n   283:     /// alignment. In other words, if `K` has size 16, `K.align_to(32)`\n   284:     /// will *still* have size 16.\n   285:     ///\n   286:     /// Returns an error if the combination of `self.size()` and the given\n   287:     /// `align` violates the conditions listed in [`Layout::from_size_align`].\n   288:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   289:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   290:     #[inline]\n   291:     pub const fn align_to(&self, align: usize) -> Result<Self, LayoutError> {\n   292:         if let Some(alignment) = Alignment::new(align) {\n   293:             self.adjust_alignment_to(alignment)\n   294:         } else {\n   295:             Err(LayoutError)\n   296:         }\n   297:     }\n   298: \n   299:     /// Creates a layout describing the record that can hold a value\n   300:     /// of the same layout as `self`, but that also is aligned to\n   301:     /// alignment `alignment`.\n   302:     ///\n   303:     /// If `self` already meets the prescribed alignment, then returns\n   304:     /// `self`.\n   305:     ///\n   306:     /// Note that this method does not add any padding to the overall\n   307:     /// size, regardless of whether the returned layout has a different",
    "nanvix_source": "   281:     /// Note that this method does not add any padding to the overall\n   282:     /// size, regardless of whether the returned layout has a different\n   283:     /// alignment. In other words, if `K` has size 16, `K.align_to(32)`\n   284:     /// will *still* have size 16.\n   285:     ///\n   286:     /// Returns an error if the combination of `self.size()` and the given\n   287:     /// `align` violates the conditions listed in [`Layout::from_size_align`].\n   288:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   289:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   290:     #[inline]\n   291:     pub const fn align_to(&self, align: usize) -> Result<Self, LayoutError> {\n   292:         if let Some(alignment) = Alignment::new(align) {\n   293:             self.adjust_alignment_to(alignment)\n   294:         } else {\n   295:             Err(LayoutError)\n   296:         }\n   297:     }\n   298: \n   299:     /// Creates a layout describing the record that can hold a value\n   300:     /// of the same layout as `self`, but that also is aligned to\n   301:     /// alignment `alignment`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::array",
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
      "name": "array",
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
    "verification_source": "   543:     #[inline]\n   544:     pub const fn extend_packed(&self, next: Self) -> Result<Self, LayoutError> {\n   545:         // SAFETY: each `size` is at most `isize::MAX == usize::MAX/2`, so the\n   546:         // sum is at most `usize::MAX/2*2 == usize::MAX - 1`, and cannot overflow.\n   547:         let new_size = unsafe { unchecked_add(self.size, next.size) };\n   548:         // The safe constructor enforces that the new size isn't too big for the alignment\n   549:         Layout::from_size_alignment(new_size, self.align)\n   550:     }\n   551: \n   552:     /// Creates a layout describing the record for a `[T; n]`.\n   553:     ///\n   554:     /// On arithmetic overflow or when the total size would exceed\n   555:     /// `isize::MAX`, returns `LayoutError`.\n   556:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   557:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   558:     #[inline]\n   559:     pub const fn array<T>(n: usize) -> Result<Self, LayoutError> {\n   560:         // Reduce the amount of code we need to monomorphize per `T`.\n   561:         return inner(T::LAYOUT, n);\n   562: \n   563:         #[inline]\n   564:         const fn inner(element_layout: Layout, n: usize) -> Result<Layout, LayoutError> {\n   565:             let Layout { size: element_size, align: alignment } = element_layout;\n   566: \n   567:             // We need to check two things about the size:\n   568:             //  - That the total size won't overflow a `usize`, and\n   569:             //  - That the total size still fits in an `isize`.\n   570:             // By using division we can check them both with a single threshold.\n   571:             // That'd usually be a bad idea, but thankfully here the element size\n   572:             // and alignment are constants, so the compiler will fold all of it.\n   573:             if element_size != 0 && n > Layout::max_size_for_alignment(alignment) / element_size {\n   574:                 return Err(LayoutError);\n   575:             }",
    "nanvix_source": "   549:         Layout::from_size_alignment(new_size, self.align)\n   550:     }\n   551: \n   552:     /// Creates a layout describing the record for a `[T; n]`.\n   553:     ///\n   554:     /// On arithmetic overflow or when the total size would exceed\n   555:     /// `isize::MAX`, returns `LayoutError`.\n   556:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   557:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   558:     #[inline]\n   559:     pub const fn array<T>(n: usize) -> Result<Self, LayoutError> {\n   560:         // Reduce the amount of code we need to monomorphize per `T`.\n   561:         return inner(T::LAYOUT, n);\n   562: \n   563:         #[inline]\n   564:         const fn inner(element_layout: Layout, n: usize) -> Result<Layout, LayoutError> {\n   565:             let Layout { size: element_size, align: alignment } = element_layout;\n   566: \n   567:             // We need to check two things about the size:\n   568:             //  - That the total size won't overflow a `usize`, and\n   569:             //  - That the total size still fits in an `isize`.",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::extend",
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
      "name": "extend",
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
            "next",
            {
              "generic": "Self"
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
    "verification_source": "   478:     ///         offsets.push(offset);\n   479:     ///     }\n   480:     ///     // Remember to finalize with `pad_to_align`!\n   481:     ///     Ok((layout.pad_to_align(), offsets))\n   482:     /// }\n   483:     /// # // test that it works\n   484:     /// # #[repr(C)] struct S { a: u64, b: u32, c: u16, d: u32 }\n   485:     /// # let s = Layout::new::<S>();\n   486:     /// # let u16 = Layout::new::<u16>();\n   487:     /// # let u32 = Layout::new::<u32>();\n   488:     /// # let u64 = Layout::new::<u64>();\n   489:     /// # assert_eq!(repr_c(&[u64, u32, u16, u32]), Ok((s, vec![0, 8, 12, 16])));\n   490:     /// ```\n   491:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   492:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   493:     #[inline]\n   494:     pub const fn extend(&self, next: Self) -> Result<(Self, usize), LayoutError> {\n   495:         let new_alignment = Alignment::max(self.align, next.align);\n   496:         let offset = self.size_rounded_up_to_custom_alignment(next.align);\n   497: \n   498:         // SAFETY: `offset` is at most `isize::MAX + 1` (such as from aligning\n   499:         // to `Alignment::MAX`) and `next.size` is at most `isize::MAX` (from the\n   500:         // `Layout` type invariant).  Thus the largest possible `new_size` is\n   501:         // `isize::MAX + 1 + isize::MAX`, which is `usize::MAX`, and cannot overflow.\n   502:         let new_size = unsafe { unchecked_add(offset, next.size) };\n   503: \n   504:         if let Ok(layout) = Layout::from_size_alignment(new_size, new_alignment) {\n   505:             Ok((layout, offset))\n   506:         } else {\n   507:             Err(LayoutError)\n   508:         }\n   509:     }\n   510: ",
    "nanvix_source": "   484:     /// # #[repr(C)] struct S { a: u64, b: u32, c: u16, d: u32 }\n   485:     /// # let s = Layout::new::<S>();\n   486:     /// # let u16 = Layout::new::<u16>();\n   487:     /// # let u32 = Layout::new::<u32>();\n   488:     /// # let u64 = Layout::new::<u64>();\n   489:     /// # assert_eq!(repr_c(&[u64, u32, u16, u32]), Ok((s, vec![0, 8, 12, 16])));\n   490:     /// ```\n   491:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   492:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   493:     #[inline]\n   494:     pub const fn extend(&self, next: Self) -> Result<(Self, usize), LayoutError> {\n   495:         let new_alignment = Alignment::max(self.align, next.align);\n   496:         let offset = self.size_rounded_up_to_custom_alignment(next.align);\n   497: \n   498:         // SAFETY: `offset` is at most `isize::MAX + 1` (such as from aligning\n   499:         // to `Alignment::MAX`) and `next.size` is at most `isize::MAX` (from the\n   500:         // `Layout` type invariant).  Thus the largest possible `new_size` is\n   501:         // `isize::MAX + 1 + isize::MAX`, which is `usize::MAX`, and cannot overflow.\n   502:         let new_size = unsafe { unchecked_add(offset, next.size) };\n   503: \n   504:         if let Ok(layout) = Layout::from_size_alignment(new_size, new_alignment) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::alloc::Layout::extend_packed",
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
      "name": "extend_packed",
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
            "next",
            {
              "generic": "Self"
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
    "verification_source": "   528:             // The safe constructor is called here to enforce the isize size limit.\n   529:             Layout::from_size_alignment(size, self.align)\n   530:         } else {\n   531:             Err(LayoutError)\n   532:         }\n   533:     }\n   534: \n   535:     /// Creates a layout describing the record for `self` followed by\n   536:     /// `next` with no additional padding between the two. Since no\n   537:     /// padding is inserted, the alignment of `next` is irrelevant,\n   538:     /// and is not incorporated *at all* into the resulting layout.\n   539:     ///\n   540:     /// On arithmetic overflow, returns `LayoutError`.\n   541:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   542:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   543:     #[inline]\n   544:     pub const fn extend_packed(&self, next: Self) -> Result<Self, LayoutError> {\n   545:         // SAFETY: each `size` is at most `isize::MAX == usize::MAX/2`, so the\n   546:         // sum is at most `usize::MAX/2*2 == usize::MAX - 1`, and cannot overflow.\n   547:         let new_size = unsafe { unchecked_add(self.size, next.size) };\n   548:         // The safe constructor enforces that the new size isn't too big for the alignment\n   549:         Layout::from_size_alignment(new_size, self.align)\n   550:     }\n   551: \n   552:     /// Creates a layout describing the record for a `[T; n]`.\n   553:     ///\n   554:     /// On arithmetic overflow or when the total size would exceed\n   555:     /// `isize::MAX`, returns `LayoutError`.\n   556:     #[stable(feature = \"alloc_layout_manipulation\", since = \"1.44.0\")]\n   557:     #[rustc_const_stable(feature = \"const_alloc_layout\", since = \"1.85.0\")]\n   558:     #[inline]\n   559:     pub const fn array<T>(n: usize) -> Result<Self, LayoutError> {\n   560:         // Reduce the amount of code we need to monomorphize per `T`.",
    "nanvix_source": "   534: \n   535:     /// Creates a layout describing the record for `self` followed by\n   536:     /// `next` with no additional padding between the two. Since no\n   537:     /// padding is inserted, the alignment of `next` is irrelevant,\n   538:     /// and is not incorporated *at all* into the resulting layout.\n   539:     ///\n   540:     /// On arithmetic overflow, returns `LayoutError`.\n   541:     #[stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   542:     #[rustc_const_stable(feature = \"alloc_layout_extra\", since = \"1.95.0\")]\n   543:     #[inline]\n   544:     pub const fn extend_packed(&self, next: Self) -> Result<Self, LayoutError> {\n   545:         // SAFETY: each `size` is at most `isize::MAX == usize::MAX/2`, so the\n   546:         // sum is at most `usize::MAX/2*2 == usize::MAX - 1`, and cannot overflow.\n   547:         let new_size = unsafe { unchecked_add(self.size, next.size) };\n   548:         // The safe constructor enforces that the new size isn't too big for the alignment\n   549:         Layout::from_size_alignment(new_size, self.align)\n   550:     }\n   551: \n   552:     /// Creates a layout describing the record for a `[T; n]`.\n   553:     ///\n   554:     /// On arithmetic overflow or when the total size would exceed",
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
