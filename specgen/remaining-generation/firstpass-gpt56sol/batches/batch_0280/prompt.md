For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::borrow::Borrow::borrow",
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
      "reference_identity_vs_view"
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
      "name": "borrow",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:893",
        "kind": "trait",
        "name": "Borrow",
        "path": [
          "core",
          "borrow",
          "Borrow"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "Borrowed"
            }
          }
        }
      }
    },
    "verification_source": "   163:     /// ```\n   164:     /// use std::borrow::Borrow;\n   165:     ///\n   166:     /// fn check<T: Borrow<str>>(s: T) {\n   167:     ///     assert_eq!(\"Hello\", s.borrow());\n   168:     /// }\n   169:     ///\n   170:     /// let s = \"Hello\".to_string();\n   171:     ///\n   172:     /// check(s);\n   173:     ///\n   174:     /// let s = \"Hello\";\n   175:     ///\n   176:     /// check(s);\n   177:     /// ```\n   178:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   179:     fn borrow(&self) -> &Borrowed;\n   180: }\n   181: \n   182: /// A trait for mutably borrowing data.\n   183: ///\n   184: /// As a companion to [`Borrow<T>`] this trait allows a type to borrow as\n   185: /// an underlying type by providing a mutable reference. See [`Borrow<T>`]\n   186: /// for more information on borrowing as another type.\n   187: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   188: #[rustc_diagnostic_item = \"BorrowMut\"]\n   189: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   190: pub const trait BorrowMut<Borrowed: ?Sized>: [const] Borrow<Borrowed> {\n   191:     /// Mutably borrows from an owned value.\n   192:     ///\n   193:     /// # Examples\n   194:     ///\n   195:     /// ```",
    "nanvix_source": "   169:     ///\n   170:     /// let s = \"Hello\".to_string();\n   171:     ///\n   172:     /// check(s);\n   173:     ///\n   174:     /// let s = \"Hello\";\n   175:     ///\n   176:     /// check(s);\n   177:     /// ```\n   178:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   179:     fn borrow(&self) -> &Borrowed;\n   180: }\n   181: \n   182: /// A trait for mutably borrowing data.\n   183: ///\n   184: /// As a companion to [`Borrow<T>`] this trait allows a type to borrow as\n   185: /// an underlying type by providing a mutable reference. See [`Borrow<T>`]\n   186: /// for more information on borrowing as another type.\n   187: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   188: #[rustc_diagnostic_item = \"BorrowMut\"]\n   189: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::borrow::BorrowMut::borrow_mut",
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
      "reference_identity_vs_view"
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
      "name": "borrow_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "core:896",
        "kind": "trait",
        "name": "BorrowMut",
        "path": [
          "core",
          "borrow",
          "BorrowMut"
        ]
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "Borrowed"
            }
          }
        }
      }
    },
    "verification_source": "   190: pub const trait BorrowMut<Borrowed: ?Sized>: [const] Borrow<Borrowed> {\n   191:     /// Mutably borrows from an owned value.\n   192:     ///\n   193:     /// # Examples\n   194:     ///\n   195:     /// ```\n   196:     /// use std::borrow::BorrowMut;\n   197:     ///\n   198:     /// fn check<T: BorrowMut<[i32]>>(mut v: T) {\n   199:     ///     assert_eq!(&mut [1, 2, 3], v.borrow_mut());\n   200:     /// }\n   201:     ///\n   202:     /// let v = vec![1, 2, 3];\n   203:     ///\n   204:     /// check(v);\n   205:     /// ```\n   206:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   207:     fn borrow_mut(&mut self) -> &mut Borrowed;\n   208: }\n   209: \n   210: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   211: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   212: impl<T: ?Sized> const Borrow<T> for T {\n   213:     #[rustc_diagnostic_item = \"noop_method_borrow\"]\n   214:     fn borrow(&self) -> &T {\n   215:         self\n   216:     }\n   217: }\n   218: \n   219: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   220: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   221: impl<T: ?Sized> const BorrowMut<T> for T {\n   222:     fn borrow_mut(&mut self) -> &mut T {",
    "nanvix_source": "   196:     /// use std::borrow::BorrowMut;\n   197:     ///\n   198:     /// fn check<T: BorrowMut<[i32]>>(mut v: T) {\n   199:     ///     assert_eq!(&mut [1, 2, 3], v.borrow_mut());\n   200:     /// }\n   201:     ///\n   202:     /// let v = vec![1, 2, 3];\n   203:     ///\n   204:     /// check(v);\n   205:     /// ```\n   206:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   207:     fn borrow_mut(&mut self) -> &mut Borrowed;\n   208: }\n   209: \n   210: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   211: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   212: const impl<T: ?Sized> Borrow<T> for T {\n   213:     #[rustc_diagnostic_item = \"noop_method_borrow\"]\n   214:     fn borrow(&self) -> &T {\n   215:         self\n   216:     }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::clone::Clone::clone_from",
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
        "where_predicates": [
          {
            "bound_predicate": {
              "bounds": [],
              "generic_params": [],
              "type": {
                "generic": "Self"
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
      "name": "clone_from",
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
        "item_id": "core:42",
        "kind": "trait",
        "name": "Clone",
        "path": [
          "core",
          "clone",
          "Clone"
        ]
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
            "source",
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
        "output": null
      }
    },
    "verification_source": "   229:     /// assert_eq!(*data_clone.lock().unwrap(), vec![1, 2, 3, 4]);\n   230:     /// ```\n   231:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   232:     #[must_use = \"cloning is often expensive and is not expected to have side effects\"]\n   233:     // Clone::clone is special because the compiler generates MIR to implement it for some types.\n   234:     // See InstanceKind::CloneShim.\n   235:     #[lang = \"clone_fn\"]\n   236:     fn clone(&self) -> Self;\n   237: \n   238:     /// Performs copy-assignment from `source`.\n   239:     ///\n   240:     /// `a.clone_from(&b)` is equivalent to `a = b.clone()` in functionality,\n   241:     /// but can be overridden to reuse the resources of `a` to avoid unnecessary\n   242:     /// allocations.\n   243:     #[inline]\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     fn clone_from(&mut self, source: &Self)\n   246:     where\n   247:         Self: [const] Destruct,\n   248:     {\n   249:         *self = source.clone()\n   250:     }\n   251: }\n   252: \n   253: /// Indicates that the `Clone` implementation is identical to copying the value.\n   254: ///\n   255: /// This is used for some optimizations in the standard library, which specializes\n   256: /// on this trait to select faster implementations of functions such as\n   257: /// [`clone_from_slice`](slice::clone_from_slice). It is automatically implemented\n   258: /// when using `#[derive(Clone, Copy)]`.\n   259: ///\n   260: /// Note that this trait does not imply that the type is `Copy`, because e.g.\n   261: /// `core::ops::Range<i32>` could soundly implement this trait.",
    "nanvix_source": "   235:     #[lang = \"clone_fn\"]\n   236:     fn clone(&self) -> Self;\n   237: \n   238:     /// Performs copy-assignment from `source`.\n   239:     ///\n   240:     /// `a.clone_from(&b)` is equivalent to `a = b.clone()` in functionality,\n   241:     /// but can be overridden to reuse the resources of `a` to avoid unnecessary\n   242:     /// allocations.\n   243:     #[inline]\n   244:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   245:     fn clone_from(&mut self, source: &Self)\n   246:     where\n   247:         Self: [const] Destruct,\n   248:     {\n   249:         *self = source.clone()\n   250:     }\n   251: }\n   252: \n   253: /// Indicates that the `Clone` implementation is identical to copying the value.\n   254: ///\n   255: /// This is used for some optimizations in the standard library, which specializes",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::convert::AsMut::as_mut",
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
      "reference_identity_vs_view"
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
      "name": "as_mut",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "item_id": "core:62",
        "kind": "trait",
        "name": "AsMut",
        "path": [
          "core",
          "convert",
          "AsMut"
        ]
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
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   359: ///     };\n   360: ///     caesar(&mut doc, 1);\n   361: ///     assert_eq!(doc.content, [18, 20, 9]);\n   362: ///     null_terminate(&mut doc);\n   363: ///     assert_eq!(doc.content, [18, 20, 9, 0]);\n   364: /// }\n   365: /// ```\n   366: ///\n   367: /// Note, however, that APIs don't need to be generic. In many cases taking a `&mut [u8]` or\n   368: /// `&mut Vec<u8>`, for example, is the better choice (callers need to pass the correct type then).\n   369: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   370: #[rustc_diagnostic_item = \"AsMut\"]\n   371: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   372: pub const trait AsMut<T: PointeeSized>: PointeeSized {\n   373:     /// Converts this type into a mutable reference of the (usually inferred) input type.\n   374:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   375:     fn as_mut(&mut self) -> &mut T;\n   376: }\n   377: \n   378: /// A value-to-value conversion that consumes the input value. The\n   379: /// opposite of [`From`].\n   380: ///\n   381: /// One should avoid implementing [`Into`] and implement [`From`] instead.\n   382: /// Implementing [`From`] automatically provides one with an implementation of [`Into`]\n   383: /// thanks to the blanket implementation in the standard library.\n   384: ///\n   385: /// Prefer using [`Into`] over [`From`] when specifying trait bounds on a generic function\n   386: /// to ensure that types that only implement [`Into`] can be used as well.\n   387: ///\n   388: /// **Note: This trait must not fail**. If the conversion can fail, use [`TryInto`].\n   389: ///\n   390: /// # Generic Implementations\n   391: ///",
    "nanvix_source": "   366: /// ```\n   367: ///\n   368: /// Note, however, that APIs don't need to be generic. In many cases taking a `&mut [u8]` or\n   369: /// `&mut Vec<u8>`, for example, is the better choice (callers need to pass the correct type then).\n   370: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   371: #[rustc_diagnostic_item = \"AsMut\"]\n   372: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   373: pub const trait AsMut<T: PointeeSized>: PointeeSized {\n   374:     /// Converts this type into a mutable reference of the (usually inferred) input type.\n   375:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   376:     fn as_mut(&mut self) -> &mut T;\n   377: }\n   378: \n   379: /// A value-to-value conversion that consumes the input value. The\n   380: /// opposite of [`From`].\n   381: ///\n   382: /// One should avoid implementing [`Into`] and implement [`From`] instead.\n   383: /// Implementing [`From`] automatically provides one with an implementation of [`Into`]\n   384: /// thanks to the blanket implementation in the standard library.\n   385: ///\n   386: /// Prefer using [`Into`] over [`From`] when specifying trait bounds on a generic function",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::convert::AsRef::as_ref",
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
      "reference_identity_vs_view"
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
      "name": "as_ref",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:64",
        "kind": "trait",
        "name": "AsRef",
        "path": [
          "core",
          "convert",
          "AsRef"
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
          "borrowed_ref": {
            "is_mutable": false,
            "lifetime": null,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   207: /// fn is_hello<T: AsRef<str>>(s: T) {\n   208: ///    assert_eq!(\"hello\", s.as_ref());\n   209: /// }\n   210: ///\n   211: /// let s = \"hello\";\n   212: /// is_hello(s);\n   213: ///\n   214: /// let s = \"hello\".to_string();\n   215: /// is_hello(s);\n   216: /// ```\n   217: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   218: #[rustc_diagnostic_item = \"AsRef\"]\n   219: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   220: pub const trait AsRef<T: PointeeSized>: PointeeSized {\n   221:     /// Converts this type into a shared reference of the (usually inferred) input type.\n   222:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   223:     fn as_ref(&self) -> &T;\n   224: }\n   225: \n   226: /// Used to do a cheap mutable-to-mutable reference conversion.\n   227: ///\n   228: /// This trait is similar to [`AsRef`] but used for converting between mutable\n   229: /// references. If you need to do a costly conversion it is better to\n   230: /// implement [`From`] with type `&mut T` or write a custom function.\n   231: ///\n   232: /// **Note: This trait must not fail**. If the conversion can fail, use a\n   233: /// dedicated method which returns an [`Option<T>`] or a [`Result<T, E>`].\n   234: ///\n   235: /// # Generic Implementations\n   236: ///\n   237: /// `AsMut` auto-dereferences if the inner type is a mutable reference\n   238: /// (e.g.: `foo.as_mut()` will work the same if `foo` has type `&mut Foo` or `&mut &mut Foo`).\n   239: ///",
    "nanvix_source": "   214: ///\n   215: /// let s = \"hello\".to_string();\n   216: /// is_hello(s);\n   217: /// ```\n   218: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   219: #[rustc_diagnostic_item = \"AsRef\"]\n   220: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   221: pub const trait AsRef<T: PointeeSized>: PointeeSized {\n   222:     /// Converts this type into a shared reference of the (usually inferred) input type.\n   223:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   224:     fn as_ref(&self) -> &T;\n   225: }\n   226: \n   227: /// Used to do a cheap mutable-to-mutable reference conversion.\n   228: ///\n   229: /// This trait is similar to [`AsRef`] but used for converting between mutable\n   230: /// references. If you need to do a costly conversion it is better to\n   231: /// implement [`From`] with type `&mut T` or write a custom function.\n   232: ///\n   233: /// **Note: This trait must not fail**. If the conversion can fail, use a\n   234: /// dedicated method which returns an [`Option<T>`] or a [`Result<T, E>`].",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::error::Error::cause",
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
      "reference_identity_vs_view"
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
      "name": "cause",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:934",
        "kind": "trait",
        "name": "Error",
        "path": [
          "core",
          "error",
          "Error"
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "borrowed_ref": {
                        "is_mutable": false,
                        "lifetime": null,
                        "type": {
                          "dyn_trait": {
                            "lifetime": null,
                            "traits": [
                              {
                                "generic_params": [],
                                "trait": {
                                  "args": null,
                                  "id": 934,
                                  "path": "Error"
                                }
                              }
                            ]
                          }
                        }
                      }
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
    "verification_source": "   131:     ///     // Print `e` itself, no need for description().\n   132:     ///     eprintln!(\"Error: {e}\");\n   133:     /// }\n   134:     /// ```\n   135:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   136:     #[deprecated(since = \"1.42.0\", note = \"use the Display impl or to_string()\")]\n   137:     fn description(&self) -> &str {\n   138:         \"description() is deprecated; use Display\"\n   139:     }\n   140: \n   141:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   142:     #[deprecated(\n   143:         since = \"1.33.0\",\n   144:         note = \"replaced by Error::source, which can support downcasting\"\n   145:     )]\n   146:     #[allow(missing_docs)]\n   147:     fn cause(&self) -> Option<&dyn Error> {\n   148:         self.source()\n   149:     }\n   150: \n   151:     /// Provides type-based access to context intended for error reports.\n   152:     ///\n   153:     /// Used in conjunction with [`Request::provide_value`] and [`Request::provide_ref`] to extract\n   154:     /// references to member variables from `dyn Error` trait objects.\n   155:     ///\n   156:     /// # Example\n   157:     ///\n   158:     /// ```rust\n   159:     /// #![feature(error_generic_member_access)]\n   160:     /// use core::fmt;\n   161:     /// use core::error::{request_ref, Request};\n   162:     ///\n   163:     /// #[derive(Debug)]",
    "nanvix_source": "   137:     fn description(&self) -> &str {\n   138:         \"description() is deprecated; use Display\"\n   139:     }\n   140: \n   141:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   142:     #[deprecated(\n   143:         since = \"1.33.0\",\n   144:         note = \"replaced by Error::source, which can support downcasting\"\n   145:     )]\n   146:     #[allow(missing_docs)]\n   147:     fn cause(&self) -> Option<&dyn Error> {\n   148:         self.source()\n   149:     }\n   150: \n   151:     /// Provides type-based access to context intended for error reports.\n   152:     ///\n   153:     /// Used in conjunction with [`Request::provide_value`] and [`Request::provide_ref`] to extract\n   154:     /// references to member variables from `dyn Error` trait objects.\n   155:     ///\n   156:     /// # Example\n   157:     ///",
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
