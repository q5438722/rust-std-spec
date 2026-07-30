For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::mem::needs_drop",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
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
      "name": "needs_drop",
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
        "inputs": [],
        "is_c_variadic": false,
        "output": {
          "primitive": "bool"
        }
      }
    },
    "verification_source": "   644: ///             // drop the data\n   645: ///             if mem::needs_drop::<T>() {\n   646: ///                 for x in self.iter_mut() {\n   647: ///                     ptr::drop_in_place(x);\n   648: ///                 }\n   649: ///             }\n   650: ///             self.free_buffer();\n   651: ///         }\n   652: ///     }\n   653: /// }\n   654: /// ```\n   655: #[inline]\n   656: #[must_use]\n   657: #[stable(feature = \"needs_drop\", since = \"1.21.0\")]\n   658: #[rustc_const_stable(feature = \"const_mem_needs_drop\", since = \"1.36.0\")]\n   659: #[rustc_diagnostic_item = \"needs_drop\"]\n   660: pub const fn needs_drop<T: ?Sized>() -> bool {\n   661:     const { intrinsics::needs_drop::<T>() }\n   662: }\n   663: \n   664: /// Returns the value of type `T` represented by the all-zero byte-pattern.\n   665: ///\n   666: /// This means that, for example, the padding byte in `(u8, u16)` is not\n   667: /// necessarily zeroed.\n   668: ///\n   669: /// There is no guarantee that an all-zero byte-pattern represents a valid value\n   670: /// of some type `T`. For example, the all-zero byte-pattern is not a valid value\n   671: /// for reference types (`&T`, `&mut T`) and function pointers. Using `zeroed`\n   672: /// on such types causes immediate [undefined behavior][ub] because [the Rust\n   673: /// compiler assumes][inv] that there always is a valid value in a variable it\n   674: /// considers initialized.\n   675: ///\n   676: /// This has the same effect as [`MaybeUninit::zeroed().assume_init()`][zeroed].",
    "nanvix_source": "   689: ///             self.free_buffer();\n   690: ///         }\n   691: ///     }\n   692: /// }\n   693: /// ```\n   694: #[inline]\n   695: #[must_use]\n   696: #[stable(feature = \"needs_drop\", since = \"1.21.0\")]\n   697: #[rustc_const_stable(feature = \"const_mem_needs_drop\", since = \"1.36.0\")]\n   698: #[rustc_diagnostic_item = \"needs_drop\"]\n   699: pub const fn needs_drop<T: ?Sized>() -> bool {\n   700:     const { intrinsics::needs_drop::<T>() }\n   701: }\n   702: \n   703: /// Returns the value of type `T` represented by the all-zero byte-pattern.\n   704: ///\n   705: /// This means that, for example, the padding byte in `(u8, u16)` is not\n   706: /// necessarily zeroed.\n   707: ///\n   708: /// There is no guarantee that an all-zero byte-pattern represents a valid value\n   709: /// of some type `T`. For example, the all-zero byte-pattern is not a valid value",
    "previous_skip_rationale": "The implementation delegates entirely to the compiler intrinsic intrinsics::needs_drop::<T>(). No supplied public vstd predicate models whether a type has drop glue, so no useful non-vacuous result relation is expressible."
  },
  {
    "target": "core::mem::take",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
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
                "bounds": [
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "maybe_const",
                      "trait": {
                        "args": null,
                        "id": 70,
                        "path": "Default"
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
      "name": "take",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "dest"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": null,
      "signature": {
        "inputs": [
          [
            "dest",
            {
              "borrowed_ref": {
                "is_mutable": true,
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
          "generic": "T"
        }
      }
    },
    "verification_source": "   832: /// # struct Buffer<T> { buf: Vec<T> }\n   833: /// impl<T> Buffer<T> {\n   834: ///     fn get_and_reset(&mut self) -> Vec<T> {\n   835: ///         mem::take(&mut self.buf)\n   836: ///     }\n   837: /// }\n   838: ///\n   839: /// let mut buffer = Buffer { buf: vec![0, 1] };\n   840: /// assert_eq!(buffer.buf.len(), 2);\n   841: ///\n   842: /// assert_eq!(buffer.get_and_reset(), vec![0, 1]);\n   843: /// assert_eq!(buffer.buf.len(), 0);\n   844: /// ```\n   845: #[inline]\n   846: #[stable(feature = \"mem_take\", since = \"1.40.0\")]\n   847: #[rustc_const_unstable(feature = \"const_default\", issue = \"143894\")]\n   848: pub const fn take<T: [const] Default>(dest: &mut T) -> T {\n   849:     replace(dest, T::default())\n   850: }\n   851: \n   852: /// Moves `src` into the referenced `dest`, returning the previous `dest` value.\n   853: ///\n   854: /// Neither value is dropped.\n   855: ///\n   856: /// * If you want to replace the values of two variables, see [`swap`].\n   857: /// * If you want to replace with a default value, see [`take`].\n   858: ///\n   859: /// # Examples\n   860: ///\n   861: /// A simple example:\n   862: ///\n   863: /// ```\n   864: /// use std::mem;",
    "nanvix_source": "   877: ///\n   878: /// let mut buffer = Buffer { buf: vec![0, 1] };\n   879: /// assert_eq!(buffer.buf.len(), 2);\n   880: ///\n   881: /// assert_eq!(buffer.get_and_reset(), vec![0, 1]);\n   882: /// assert_eq!(buffer.buf.len(), 0);\n   883: /// ```\n   884: #[inline]\n   885: #[stable(feature = \"mem_take\", since = \"1.40.0\")]\n   886: #[rustc_const_unstable(feature = \"const_default\", issue = \"143894\")]\n   887: pub const fn take<T: [const] Default>(dest: &mut T) -> T {\n   888:     replace(dest, T::default())\n   889: }\n   890: \n   891: /// Moves `src` into the referenced `dest`, returning the previous `dest` value.\n   892: ///\n   893: /// Neither value is dropped.\n   894: ///\n   895: /// * If you want to replace the values of two variables, see [`swap`].\n   896: /// * If you want to replace with a default value, see [`take`].\n   897: ///",
    "previous_skip_rationale": "The return is the old destination value, but the observable destination post-state is produced by T::default(). Existing vstd vocabulary exposes that value only through the relational T::default.ensures predicate, which does not imply a unique result. Adding a uniqueness precondition would invent an unjustified API domain, while omitting the destination post-state would leave an observable output unconstrained."
  },
  {
    "target": "core::result::Result::unwrap_or_default",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [],
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 70,
                      "path": "Default"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "T"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "E"
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
      "name": "unwrap_or_default",
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
                      "generic": "E"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 90,
            "path": "Result"
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
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "E"
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:29310",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:90",
        "resolved_owner_path": [
          "core",
          "result",
          "Result"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "generic": "Self"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "generic": "T"
        }
      }
    },
    "verification_source": "  1249:     ///\n  1250:     /// ```\n  1251:     /// let good_year_from_input = \"1909\";\n  1252:     /// let bad_year_from_input = \"190blarg\";\n  1253:     /// let good_year = good_year_from_input.parse().unwrap_or_default();\n  1254:     /// let bad_year = bad_year_from_input.parse().unwrap_or_default();\n  1255:     ///\n  1256:     /// assert_eq!(1909, good_year);\n  1257:     /// assert_eq!(0, bad_year);\n  1258:     /// ```\n  1259:     ///\n  1260:     /// [`parse`]: str::parse\n  1261:     /// [`FromStr`]: crate::str::FromStr\n  1262:     #[inline]\n  1263:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1264:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1265:     pub const fn unwrap_or_default(self) -> T\n  1266:     where\n  1267:         T: [const] Default + [const] Destruct,\n  1268:         E: [const] Destruct,\n  1269:     {\n  1270:         match self {\n  1271:             Ok(x) => x,\n  1272:             Err(_) => Default::default(),\n  1273:         }\n  1274:     }\n  1275: \n  1276:     /// Returns the contained [`Err`] value, consuming the `self` value.\n  1277:     ///\n  1278:     /// # Panics\n  1279:     ///\n  1280:     /// Panics if the value is an [`Ok`], with a panic message including the\n  1281:     /// passed message, and the content of the [`Ok`].",
    "nanvix_source": "  1253:     ///\n  1254:     /// assert_eq!(1909, good_year);\n  1255:     /// assert_eq!(0, bad_year);\n  1256:     /// ```\n  1257:     ///\n  1258:     /// [`parse`]: str::parse\n  1259:     /// [`FromStr`]: crate::str::FromStr\n  1260:     #[inline]\n  1261:     #[stable(feature = \"result_unwrap_or_default\", since = \"1.16.0\")]\n  1262:     #[rustc_const_unstable(feature = \"const_result_trait_fn\", issue = \"144211\")]\n  1263:     pub const fn unwrap_or_default(self) -> T\n  1264:     where\n  1265:         T: [const] Default + [const] Destruct,\n  1266:         E: [const] Destruct,\n  1267:     {\n  1268:         match self {\n  1269:             Ok(x) => x,\n  1270:             Err(_) => Default::default(),\n  1271:         }\n  1272:     }\n  1273: ",
    "previous_skip_rationale": "The Ok branch is precise, but existing vstd vocabulary can describe the Err branch only through T::default.ensures((), res), which is not guaranteed to be functional. Enforcing uniqueness would either add an unjustified domain restriction or overstate Default's contract. Leaving the Err result unconstrained would not provide a useful deterministic contract."
  },
  {
    "target": "core::slice::clone_from_slice",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
                    "modifier": "maybe_const",
                    "trait": {
                      "args": null,
                      "id": 42,
                      "path": "Clone"
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
      "name": "clone_from_slice",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "src",
            {
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4238:     /// ```\n  4239:     /// let mut slice = [1, 2, 3, 4, 5];\n  4240:     ///\n  4241:     /// {\n  4242:     ///     let (left, right) = slice.split_at_mut(2);\n  4243:     ///     left.clone_from_slice(&right[1..]);\n  4244:     /// }\n  4245:     ///\n  4246:     /// assert_eq!(slice, [4, 5, 3, 4, 5]);\n  4247:     /// ```\n  4248:     ///\n  4249:     /// [`copy_from_slice`]: slice::copy_from_slice\n  4250:     /// [`split_at_mut`]: slice::split_at_mut\n  4251:     #[stable(feature = \"clone_from_slice\", since = \"1.7.0\")]\n  4252:     #[track_caller]\n  4253:     #[rustc_const_unstable(feature = \"const_clone\", issue = \"142757\")]\n  4254:     pub const fn clone_from_slice(&mut self, src: &[T])\n  4255:     where\n  4256:         T: [const] Clone + [const] Destruct,\n  4257:     {\n  4258:         self.spec_clone_from(src);\n  4259:     }\n  4260: \n  4261:     /// Copies all elements from `src` into `self`, using a memcpy.\n  4262:     ///\n  4263:     /// The length of `src` must be the same as `self`.\n  4264:     ///\n  4265:     /// If `T` does not implement `Copy`, use [`clone_from_slice`].\n  4266:     ///\n  4267:     /// # Panics\n  4268:     ///\n  4269:     /// This function will panic if the two slices have different lengths.\n  4270:     ///",
    "nanvix_source": "  4250:     /// }\n  4251:     ///\n  4252:     /// assert_eq!(slice, [4, 5, 3, 4, 5]);\n  4253:     /// ```\n  4254:     ///\n  4255:     /// [`copy_from_slice`]: slice::copy_from_slice\n  4256:     /// [`split_at_mut`]: slice::split_at_mut\n  4257:     #[stable(feature = \"clone_from_slice\", since = \"1.7.0\")]\n  4258:     #[track_caller]\n  4259:     #[rustc_const_unstable(feature = \"const_clone\", issue = \"142757\")]\n  4260:     pub const fn clone_from_slice(&mut self, src: &[T])\n  4261:     where\n  4262:         T: [const] Clone + [const] Destruct,\n  4263:     {\n  4264:         self.spec_clone_from(src);\n  4265:     }\n  4266: \n  4267:     /// Copies all elements from `src` into `self`, using a memcpy.\n  4268:     ///\n  4269:     /// The length of `src` must be the same as `self`.\n  4270:     ///",
    "previous_skip_rationale": "The source justifies only the relational `cloned` postcondition for arbitrary `T: Clone`. Existing vstd vocabulary provides no law making two such clone results semantically equal, while asserting sequence equality or adding an ad hoc uniqueness precondition would be unjustified."
  },
  {
    "target": "core::slice::element_offset",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [],
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
      "name": "element_offset",
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
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
            "element",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "primitive": "usize"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 84,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  5244:     /// Returning `None` with an unaligned element:\n  5245:     /// ```\n  5246:     /// let arr: &[[u32; 2]] = &[[0, 1], [2, 3]];\n  5247:     /// let flat_arr: &[u32] = arr.as_flattened();\n  5248:     ///\n  5249:     /// let ok_elm: &[u32; 2] = flat_arr[0..2].try_into().unwrap();\n  5250:     /// let weird_elm: &[u32; 2] = flat_arr[1..3].try_into().unwrap();\n  5251:     ///\n  5252:     /// assert_eq!(ok_elm, &[0, 1]);\n  5253:     /// assert_eq!(weird_elm, &[1, 2]);\n  5254:     ///\n  5255:     /// assert_eq!(arr.element_offset(ok_elm), Some(0)); // Points to element 0\n  5256:     /// assert_eq!(arr.element_offset(weird_elm), None); // Points between element 0 and 1\n  5257:     /// ```\n  5258:     #[must_use]\n  5259:     #[stable(feature = \"element_offset\", since = \"1.94.0\")]\n  5260:     pub fn element_offset(&self, element: &T) -> Option<usize> {\n  5261:         if T::IS_ZST {\n  5262:             panic!(\"elements are zero-sized\");\n  5263:         }\n  5264: \n  5265:         let self_start = self.as_ptr().addr();\n  5266:         let elem_start = ptr::from_ref(element).addr();\n  5267: \n  5268:         let byte_offset = elem_start.wrapping_sub(self_start);\n  5269: \n  5270:         if !byte_offset.is_multiple_of(size_of::<T>()) {\n  5271:             return None;\n  5272:         }\n  5273: \n  5274:         let offset = byte_offset / size_of::<T>();\n  5275: \n  5276:         if offset < self.len() { Some(offset) } else { None }",
    "nanvix_source": "  5257:     /// let weird_elm: &[u32; 2] = flat_arr[1..3].try_into().unwrap();\n  5258:     ///\n  5259:     /// assert_eq!(ok_elm, &[0, 1]);\n  5260:     /// assert_eq!(weird_elm, &[1, 2]);\n  5261:     ///\n  5262:     /// assert_eq!(arr.element_offset(ok_elm), Some(0)); // Points to element 0\n  5263:     /// assert_eq!(arr.element_offset(weird_elm), None); // Points between element 0 and 1\n  5264:     /// ```\n  5265:     #[must_use]\n  5266:     #[stable(feature = \"element_offset\", since = \"1.94.0\")]\n  5267:     pub fn element_offset(&self, element: &T) -> Option<usize> {\n  5268:         if T::IS_ZST {\n  5269:             panic!(\"elements are zero-sized\");\n  5270:         }\n  5271: \n  5272:         let self_start = self.as_ptr().addr();\n  5273:         let elem_start = ptr::from_ref(element).addr();\n  5274: \n  5275:         let byte_offset = elem_start.wrapping_sub(self_start);\n  5276: \n  5277:         if !byte_offset.is_multiple_of(size_of::<T>()) {",
    "previous_skip_rationale": "The result depends on pointer addresses, alignment, and provenance rather than element values. Existing vstd slice and reference views cannot express that relationship or distinguish equal-valued elements at different locations. The previous implications therefore leave both None and potentially several Some results admissible, and no source-justified deterministic ordinary contract is available."
  },
  {
    "target": "core::slice::fill",
    "generation_group": "retry_suitable_skip",
    "classification": "suitable_now",
    "classification_reasons": [],
    "category": "data_structure",
    "kinds": [
      "primitive_method"
    ],
    "semantic_risks": [
      "unit_return_variant"
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
                      "id": 42,
                      "path": "Clone"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "fill",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
        "return_reference_is_mutable": false
      },
      "owner": {
        "for": {
          "slice": {
            "generic": "T"
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
            }
          ],
          "where_predicates": []
        },
        "impl_id": "core:51877",
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
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "generic": "Self"
                }
              }
            }
          ],
          [
            "value",
            {
              "generic": "T"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  4150:                 returned.assume_init()\n  4151:             }\n  4152:         }\n  4153:     }\n  4154: \n  4155:     /// Fills `self` with elements by cloning `value`.\n  4156:     ///\n  4157:     /// # Examples\n  4158:     ///\n  4159:     /// ```\n  4160:     /// let mut buf = vec![0; 10];\n  4161:     /// buf.fill(1);\n  4162:     /// assert_eq!(buf, vec![1; 10]);\n  4163:     /// ```\n  4164:     #[doc(alias = \"memset\")]\n  4165:     #[stable(feature = \"slice_fill\", since = \"1.50.0\")]\n  4166:     pub fn fill(&mut self, value: T)\n  4167:     where\n  4168:         T: Clone,\n  4169:     {\n  4170:         specialize::SpecFill::spec_fill(self, value);\n  4171:     }\n  4172: \n  4173:     /// Fills `self` with elements returned by calling a closure repeatedly.\n  4174:     ///\n  4175:     /// This method uses a closure to create new values. If you'd rather\n  4176:     /// [`Clone`] a given value, use [`fill`]. If you want to use the [`Default`]\n  4177:     /// trait to generate values, you can pass [`Default::default`] as the\n  4178:     /// argument.\n  4179:     ///\n  4180:     /// [`fill`]: slice::fill\n  4181:     ///\n  4182:     /// # Examples",
    "nanvix_source": "  4162:     ///\n  4163:     /// # Examples\n  4164:     ///\n  4165:     /// ```\n  4166:     /// let mut buf = vec![0; 10];\n  4167:     /// buf.fill(1);\n  4168:     /// assert_eq!(buf, vec![1; 10]);\n  4169:     /// ```\n  4170:     #[doc(alias = \"memset\")]\n  4171:     #[stable(feature = \"slice_fill\", since = \"1.50.0\")]\n  4172:     pub fn fill(&mut self, value: T)\n  4173:     where\n  4174:         T: Clone,\n  4175:     {\n  4176:         specialize::SpecFill::spec_fill(self, value);\n  4177:     }\n  4178: \n  4179:     /// Fills `self` with elements returned by calling a closure repeatedly.\n  4180:     ///\n  4181:     /// This method uses a closure to create new values. If you'd rather\n  4182:     /// [`Clone`] a given value, use [`fill`]. If you want to use the [`Default`]",
    "previous_skip_rationale": "A useful contract must describe the post-state of the exact `&mut [T]` receiver. The determinism checker materializes that state as by-value `[T]`, which is unsized and cannot typecheck. No ordinary contract-only revision can preserve the API signature and observable semantics while avoiding this limitation."
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
