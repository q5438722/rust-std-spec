For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::ops::BitXor::bitxor",
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
      "name": "bitxor",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:2723",
        "kind": "trait",
        "name": "BitXor",
        "path": [
          "core",
          "ops",
          "bit",
          "BitXor"
        ]
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "qualified_path": {
            "args": null,
            "name": "Output",
            "self_type": {
              "generic": "Self"
            },
            "trait": {
              "args": null,
              "id": 2723,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "   359:     /// The resulting type after applying the `^` operator.\n   360:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   361:     type Output;\n   362: \n   363:     /// Performs the `^` operation.\n   364:     ///\n   365:     /// # Examples\n   366:     ///\n   367:     /// ```\n   368:     /// assert_eq!(true ^ false, true);\n   369:     /// assert_eq!(true ^ true, false);\n   370:     /// assert_eq!(5u8 ^ 1u8, 4);\n   371:     /// assert_eq!(5u8 ^ 2u8, 7);\n   372:     /// ```\n   373:     #[must_use]\n   374:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   375:     fn bitxor(self, rhs: Rhs) -> Self::Output;\n   376: }\n   377: \n   378: macro_rules! bitxor_impl {\n   379:     ($($t:ty)*) => ($(\n   380:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   381:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   382:         impl const BitXor for $t {\n   383:             type Output = $t;\n   384: \n   385:             #[inline]\n   386:             fn bitxor(self, other: $t) -> $t { self ^ other }\n   387:         }\n   388: \n   389:         forward_ref_binop! { impl BitXor, bitxor for $t, $t,\n   390:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   391:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }",
    "nanvix_source": "   365:     /// # Examples\n   366:     ///\n   367:     /// ```\n   368:     /// assert_eq!(true ^ false, true);\n   369:     /// assert_eq!(true ^ true, false);\n   370:     /// assert_eq!(5u8 ^ 1u8, 4);\n   371:     /// assert_eq!(5u8 ^ 2u8, 7);\n   372:     /// ```\n   373:     #[must_use]\n   374:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   375:     fn bitxor(self, rhs: Rhs) -> Self::Output;\n   376: }\n   377: \n   378: macro_rules! bitxor_impl {\n   379:     ($($t:ty)*) => ($(\n   380:         #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   381:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   382:         const impl BitXor for $t {\n   383:             type Output = $t;\n   384: \n   385:             #[inline]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::BitXorAssign::bitxor_assign",
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
      "name": "bitxor_assign",
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
        "item_id": "core:2735",
        "kind": "trait",
        "name": "BitXorAssign",
        "path": [
          "core",
          "ops",
          "bit",
          "BitXorAssign"
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   873:     /// x ^= false;\n   874:     /// assert_eq!(x, true);\n   875:     ///\n   876:     /// let mut x = true;\n   877:     /// x ^= true;\n   878:     /// assert_eq!(x, false);\n   879:     ///\n   880:     /// let mut x: u8 = 5;\n   881:     /// x ^= 1;\n   882:     /// assert_eq!(x, 4);\n   883:     ///\n   884:     /// let mut x: u8 = 5;\n   885:     /// x ^= 2;\n   886:     /// assert_eq!(x, 7);\n   887:     /// ```\n   888:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   889:     fn bitxor_assign(&mut self, rhs: Rhs);\n   890: }\n   891: \n   892: macro_rules! bitxor_assign_impl {\n   893:     ($($t:ty)+) => ($(\n   894:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   895:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   896:         impl const BitXorAssign for $t {\n   897:             #[inline]\n   898:             fn bitxor_assign(&mut self, other: $t) { *self ^= other }\n   899:         }\n   900: \n   901:         forward_ref_op_assign! { impl BitXorAssign, bitxor_assign for $t, $t,\n   902:         #[stable(feature = \"op_assign_builtins_by_ref\", since = \"1.22.0\")]\n   903:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }\n   904:     )+)\n   905: }",
    "nanvix_source": "   879:     ///\n   880:     /// let mut x: u8 = 5;\n   881:     /// x ^= 1;\n   882:     /// assert_eq!(x, 4);\n   883:     ///\n   884:     /// let mut x: u8 = 5;\n   885:     /// x ^= 2;\n   886:     /// assert_eq!(x, 7);\n   887:     /// ```\n   888:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   889:     fn bitxor_assign(&mut self, rhs: Rhs);\n   890: }\n   891: \n   892: macro_rules! bitxor_assign_impl {\n   893:     ($($t:ty)+) => ($(\n   894:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   895:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   896:         const impl BitXorAssign for $t {\n   897:             #[inline]\n   898:             fn bitxor_assign(&mut self, other: $t) { *self ^= other }\n   899:         }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::DivAssign::div_assign",
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
      "name": "div_assign",
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
        "item_id": "core:1715",
        "kind": "trait",
        "name": "DivAssign",
        "path": [
          "core",
          "ops",
          "arith",
          "DivAssign"
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   958:     message = \"cannot divide-assign `{Self}` by `{Rhs}`\",\n   959:     label = \"no implementation for `{Self} /= {Rhs}`\"\n   960: )]\n   961: #[doc(alias = \"/\")]\n   962: #[doc(alias = \"/=\")]\n   963: pub const trait DivAssign<Rhs = Self> {\n   964:     /// Performs the `/=` operation.\n   965:     ///\n   966:     /// # Example\n   967:     ///\n   968:     /// ```\n   969:     /// let mut x: u32 = 12;\n   970:     /// x /= 2;\n   971:     /// assert_eq!(x, 6);\n   972:     /// ```\n   973:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   974:     fn div_assign(&mut self, rhs: Rhs);\n   975: }\n   976: \n   977: macro_rules! div_assign_impl {\n   978:     ($($t:ty)+) => ($(\n   979:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   980:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   981:         impl const DivAssign for $t {\n   982:             #[inline]\n   983:             #[track_caller]\n   984:             fn div_assign(&mut self, other: $t) { *self /= other }\n   985:         }\n   986: \n   987:         forward_ref_op_assign! { impl DivAssign, div_assign for $t, $t,\n   988:         #[stable(feature = \"op_assign_builtins_by_ref\", since = \"1.22.0\")]\n   989:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }\n   990:     )+)",
    "nanvix_source": "   964:     /// Performs the `/=` operation.\n   965:     ///\n   966:     /// # Example\n   967:     ///\n   968:     /// ```\n   969:     /// let mut x: u32 = 12;\n   970:     /// x /= 2;\n   971:     /// assert_eq!(x, 6);\n   972:     /// ```\n   973:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   974:     fn div_assign(&mut self, rhs: Rhs);\n   975: }\n   976: \n   977: macro_rules! div_assign_impl {\n   978:     ($($t:ty)+) => ($(\n   979:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   980:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   981:         const impl DivAssign for $t {\n   982:             #[inline]\n   983:             #[track_caller]\n   984:             fn div_assign(&mut self, other: $t) { *self /= other }",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::Drop::drop",
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
      "name": "drop",
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
        "item_id": "core:18",
        "kind": "trait",
        "name": "Drop",
        "path": [
          "core",
          "ops",
          "drop",
          "Drop"
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
        "output": null
      }
    },
    "verification_source": "   202: /// [drop check]: ../../nomicon/dropck.html\n   203: /// [nomicon]: ../../nomicon/phantom-data.html#an-exception-the-special-case-of-the-standard-library-and-its-unstable-may_dangle\n   204: #[lang = \"drop\"]\n   205: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   206: #[rustc_const_unstable(feature = \"const_destruct\", issue = \"133214\")]\n   207: pub const trait Drop {\n   208:     /// Executes the destructor for this type.\n   209:     ///\n   210:     /// This method is called implicitly when the value goes out of scope,\n   211:     /// and cannot be called explicitly (this is compiler error [E0040]).\n   212:     /// However, the [`mem::drop`] function in the prelude can be\n   213:     /// used to call the argument's `Drop` implementation.\n   214:     ///\n   215:     /// When this method has been called, `self` has not yet been deallocated.\n   216:     /// That only happens after the method is over.\n   217:     /// If this wasn't the case, `self` would be a dangling reference.\n   218:     ///\n   219:     /// # Panics\n   220:     ///\n   221:     /// Implementations should generally avoid [`panic!`]ing, because `drop()` may itself be called\n   222:     /// during unwinding due to a panic, and if the `drop()` panics in that situation (a \u201cdouble\n   223:     /// panic\u201d), this will likely abort the program. It is possible to check [`panicking()`] first,\n   224:     /// which may be desirable for a `Drop` implementation that is reporting a bug of the kind\n   225:     /// \u201cyou didn't finish using this before it was dropped\u201d; but most types should simply clean up\n   226:     /// their owned allocations or other resources and return normally from `drop()`, regardless of\n   227:     /// what state they are in.\n   228:     ///\n   229:     /// Note that even if this panics, the value is considered to be dropped;\n   230:     /// you must not cause `drop` to be called again. This is normally automatically\n   231:     /// handled by the compiler, but when using unsafe code, can sometimes occur\n   232:     /// unintentionally, particularly when using [`ptr::drop_in_place`].\n   233:     ///\n   234:     /// [E0040]: ../../error_codes/E0040.html",
    "nanvix_source": "   223:     /// Implementations should generally avoid [`panic!`]ing, because `drop()` may itself be called\n   224:     /// during unwinding due to a panic, and if the `drop()` panics in that situation (a \u201cdouble\n   225:     /// panic\u201d), this will likely abort the program. It is possible to check [`panicking()`] first,\n   226:     /// which may be desirable for a `Drop` implementation that is reporting a bug of the kind\n   227:     /// \u201cyou didn't finish using this before it was dropped\u201d; but most types should simply clean up\n   228:     /// their owned allocations or other resources and return normally from `drop()`, regardless of\n   229:     /// what state they are in.\n   230:     ///\n   231:     /// Note that even if this panics, the value is considered to be dropped;\n   232:     /// you must not cause `drop` to be called again. This is normally automatically\n   233:     /// handled by the compiler, but when using unsafe code, can sometimes occur\n   234:     /// unintentionally, particularly when using [`ptr::drop_in_place`].\n   235:     ///\n   236:     /// [E0040]: ../../error_codes/E0040.html\n   237:     /// [`panic!`]: crate::panic!\n   238:     /// [`panicking()`]: ../../std/thread/fn.panicking.html\n   239:     /// [`mem::drop`]: drop\n   240:     /// [`ptr::drop_in_place`]: crate::ptr::drop_in_place\n   241:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   242:     #[rustc_default_body_unstable(feature = \"pin_ergonomics\", issue = \"130494\")]\n   243:     fn drop(&mut self) {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::IndexMut::index_mut",
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
      "name": "index_mut",
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
        "item_id": "core:23560",
        "kind": "trait",
        "name": "IndexMut",
        "path": [
          "core",
          "ops",
          "index",
          "IndexMut"
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
            "index",
            {
              "generic": "Idx"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "qualified_path": {
                "args": null,
                "name": "Output",
                "self_type": {
                  "generic": "Self"
                },
                "trait": {
                  "args": null,
                  "id": 23559,
                  "path": ""
                }
              }
            }
          }
        }
      }
    },
    "verification_source": "   141: /// // `*balance.index_mut(Side::Left)`, since we are writing\n   142: /// // `balance[Side::Left]`.\n   143: /// balance[Side::Left] = Weight::Kilogram(3.0);\n   144: /// ```\n   145: #[lang = \"index_mut\"]\n   146: #[rustc_on_unimplemented(\n   147:     on(\n   148:         Self = \"&str\",\n   149:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   150: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   151:     ),\n   152:     on(\n   153:         Self = \"str\",\n   154:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   155: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   156:     ),\n   157:     on(\n   158:         Self = \"alloc::string::String\",\n   159:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   160: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   161:     ),\n   162:     message = \"the type `{Self}` cannot be mutably indexed by `{Idx}`\",\n   163:     label = \"`{Self}` cannot be mutably indexed by `{Idx}`\"\n   164: )]\n   165: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   166: #[doc(alias = \"[\")]\n   167: #[doc(alias = \"]\")]\n   168: #[doc(alias = \"[]\")]\n   169: #[rustc_const_unstable(feature = \"const_index\", issue = \"143775\")]\n   170: pub const trait IndexMut<Idx: ?Sized>: [const] Index<Idx> {\n   171:     /// Performs the mutable indexing (`container[index]`) operation.\n   172:     ///\n   173:     /// # Panics",
    "nanvix_source": "   147:     on(\n   148:         Self = \"&str\",\n   149:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   150: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   151:     ),\n   152:     on(\n   153:         Self = \"str\",\n   154:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   155: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   156:     ),\n   157:     on(\n   158:         Self = \"alloc::string::String\",\n   159:         note = \"you can use `.chars().nth()` or `.bytes().nth()`\n   160: see chapter in The Book <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>\"\n   161:     ),\n   162:     message = \"the type `{Self}` cannot be mutably indexed by `{Idx}`\",\n   163:     label = \"`{Self}` cannot be mutably indexed by `{Idx}`\"\n   164: )]\n   165: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   166: #[doc(alias = \"[\")]\n   167: #[doc(alias = \"]\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::ops::MulAssign::mul_assign",
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
      "name": "mul_assign",
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
        "item_id": "core:2666",
        "kind": "trait",
        "name": "MulAssign",
        "path": [
          "core",
          "ops",
          "arith",
          "MulAssign"
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
            "rhs",
            {
              "generic": "Rhs"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   896:     message = \"cannot multiply-assign `{Self}` by `{Rhs}`\",\n   897:     label = \"no implementation for `{Self} *= {Rhs}`\"\n   898: )]\n   899: #[doc(alias = \"*\")]\n   900: #[doc(alias = \"*=\")]\n   901: pub const trait MulAssign<Rhs = Self> {\n   902:     /// Performs the `*=` operation.\n   903:     ///\n   904:     /// # Example\n   905:     ///\n   906:     /// ```\n   907:     /// let mut x: u32 = 12;\n   908:     /// x *= 2;\n   909:     /// assert_eq!(x, 24);\n   910:     /// ```\n   911:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   912:     fn mul_assign(&mut self, rhs: Rhs);\n   913: }\n   914: \n   915: macro_rules! mul_assign_impl {\n   916:     ($($t:ty)+) => ($(\n   917:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   918:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   919:         impl const MulAssign for $t {\n   920:             #[inline]\n   921:             #[track_caller]\n   922:             #[rustc_inherit_overflow_checks]\n   923:             fn mul_assign(&mut self, other: $t) { *self *= other }\n   924:         }\n   925: \n   926:         forward_ref_op_assign! { impl MulAssign, mul_assign for $t, $t,\n   927:         #[stable(feature = \"op_assign_builtins_by_ref\", since = \"1.22.0\")]\n   928:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")] }",
    "nanvix_source": "   902:     /// Performs the `*=` operation.\n   903:     ///\n   904:     /// # Example\n   905:     ///\n   906:     /// ```\n   907:     /// let mut x: u32 = 12;\n   908:     /// x *= 2;\n   909:     /// assert_eq!(x, 24);\n   910:     /// ```\n   911:     #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   912:     fn mul_assign(&mut self, rhs: Rhs);\n   913: }\n   914: \n   915: macro_rules! mul_assign_impl {\n   916:     ($($t:ty)+) => ($(\n   917:         #[stable(feature = \"op_assign_traits\", since = \"1.8.0\")]\n   918:         #[rustc_const_unstable(feature = \"const_ops\", issue = \"143802\")]\n   919:         const impl MulAssign for $t {\n   920:             #[inline]\n   921:             #[track_caller]\n   922:             #[rustc_inherit_overflow_checks]",
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
