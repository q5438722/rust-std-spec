For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::fmt::Write::write_fmt",
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
      "formatting_effect"
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
      "name": "write_fmt",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:29961",
        "kind": "trait",
        "name": "Write",
        "path": [
          "core",
          "fmt",
          "Write"
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
            "args",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "lifetime": "'_"
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 10035,
                "path": "Arguments"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 919,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   196:     ///\n   197:     /// # Examples\n   198:     ///\n   199:     /// ```\n   200:     /// use std::fmt::{Error, Write};\n   201:     ///\n   202:     /// fn writer<W: Write>(f: &mut W, s: &str) -> Result<(), Error> {\n   203:     ///     f.write_fmt(format_args!(\"{s}\"))\n   204:     /// }\n   205:     ///\n   206:     /// let mut buf = String::new();\n   207:     /// writer(&mut buf, \"world\")?;\n   208:     /// assert_eq!(&buf, \"world\");\n   209:     /// # std::fmt::Result::Ok(())\n   210:     /// ```\n   211:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   212:     fn write_fmt(&mut self, args: Arguments<'_>) -> Result {\n   213:         // We use a specialization for `Sized` types to avoid an indirection\n   214:         // through `&mut self`\n   215:         trait SpecWriteFmt {\n   216:             fn spec_write_fmt(self, args: Arguments<'_>) -> Result;\n   217:         }\n   218: \n   219:         impl<W: Write + ?Sized> SpecWriteFmt for &mut W {\n   220:             #[inline]\n   221:             default fn spec_write_fmt(mut self, args: Arguments<'_>) -> Result {\n   222:                 if let Some(s) = args.as_statically_known_str() {\n   223:                     self.write_str(s)\n   224:                 } else {\n   225:                     write(&mut self, args)\n   226:                 }\n   227:             }\n   228:         }",
    "nanvix_source": "   204:     /// fn writer<W: Write>(f: &mut W, s: &str) -> Result<(), Error> {\n   205:     ///     f.write_fmt(format_args!(\"{s}\"))\n   206:     /// }\n   207:     ///\n   208:     /// let mut buf = String::new();\n   209:     /// writer(&mut buf, \"world\")?;\n   210:     /// assert_eq!(&buf, \"world\");\n   211:     /// # std::fmt::Result::Ok(())\n   212:     /// ```\n   213:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   214:     fn write_fmt(&mut self, args: Arguments<'_>) -> Result {\n   215:         // We use a specialization for `Sized` types to avoid an indirection\n   216:         // through `&mut self`\n   217:         trait SpecWriteFmt {\n   218:             fn spec_write_fmt(self, args: Arguments<'_>) -> Result;\n   219:         }\n   220: \n   221:         impl<W: Write + ?Sized> SpecWriteFmt for &mut W {\n   222:             #[inline]\n   223:             default fn spec_write_fmt(mut self, args: Arguments<'_>) -> Result {\n   224:                 if let Some(s) = args.as_statically_known_str() {",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::fmt::Write::write_str",
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
      "formatting_effect"
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
      "name": "write_str",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:29961",
        "kind": "trait",
        "name": "Write",
        "path": [
          "core",
          "fmt",
          "Write"
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
            "s",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "primitive": "str"
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 919,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   138:     ///\n   139:     /// # Examples\n   140:     ///\n   141:     /// ```\n   142:     /// use std::fmt::{Error, Write};\n   143:     ///\n   144:     /// fn writer<W: Write>(f: &mut W, s: &str) -> Result<(), Error> {\n   145:     ///     f.write_str(s)\n   146:     /// }\n   147:     ///\n   148:     /// let mut buf = String::new();\n   149:     /// writer(&mut buf, \"hola\")?;\n   150:     /// assert_eq!(&buf, \"hola\");\n   151:     /// # std::fmt::Result::Ok(())\n   152:     /// ```\n   153:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   154:     fn write_str(&mut self, s: &str) -> Result;\n   155: \n   156:     /// Writes a [`char`] into this writer, returning whether the write succeeded.\n   157:     ///\n   158:     /// A single [`char`] may be encoded as more than one byte.\n   159:     /// This method can only succeed if the entire byte sequence was successfully\n   160:     /// written, and this method will not return until all data has been\n   161:     /// written or an error occurs.\n   162:     ///\n   163:     /// # Errors\n   164:     ///\n   165:     /// This function will return an instance of [`Error`] on error.\n   166:     ///\n   167:     /// # Examples\n   168:     ///\n   169:     /// ```\n   170:     /// use std::fmt::{Error, Write};",
    "nanvix_source": "   146:     /// fn writer<W: Write>(f: &mut W, s: &str) -> Result<(), Error> {\n   147:     ///     f.write_str(s)\n   148:     /// }\n   149:     ///\n   150:     /// let mut buf = String::new();\n   151:     /// writer(&mut buf, \"hola\")?;\n   152:     /// assert_eq!(&buf, \"hola\");\n   153:     /// # std::fmt::Result::Ok(())\n   154:     /// ```\n   155:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   156:     fn write_str(&mut self, s: &str) -> Result;\n   157: \n   158:     /// Writes a [`char`] into this writer, returning whether the write succeeded.\n   159:     ///\n   160:     /// A single [`char`] may be encoded as more than one byte.\n   161:     /// This method can only succeed if the entire byte sequence was successfully\n   162:     /// written, and this method will not return until all data has been\n   163:     /// written or an error occurs.\n   164:     ///\n   165:     /// # Errors\n   166:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::Future::poll",
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
      "name": "poll",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self",
          "cx"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:215",
        "kind": "trait",
        "name": "Future",
        "path": [
          "core",
          "future",
          "future",
          "Future"
        ]
      },
      "signature": {
        "inputs": [
          [
            "self",
            {
              "resolved_path": {
                "args": {
                  "angle_bracketed": {
                    "args": [
                      {
                        "type": {
                          "borrowed_ref": {
                            "is_mutable": true,
                            "lifetime": null,
                            "type": {
                              "generic": "Self"
                            }
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 9981,
                "path": "Pin"
              }
            }
          ],
          [
            "cx",
            {
              "borrowed_ref": {
                "is_mutable": true,
                "lifetime": null,
                "type": {
                  "resolved_path": {
                    "args": {
                      "angle_bracketed": {
                        "args": [
                          {
                            "lifetime": "'_"
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 13510,
                    "path": "Context"
                  }
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
                      "qualified_path": {
                        "args": null,
                        "name": "Output",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 215,
                          "path": ""
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 10198,
            "path": "Poll"
          }
        }
      }
    },
    "verification_source": "    86:     /// ready to make progress (by calling `wake()`). If you're familiar with the\n    87:     /// `poll(2)` or `select(2)` syscalls on Unix it's worth noting that futures\n    88:     /// typically do *not* suffer the same problems of \"all wakeups must poll\n    89:     /// all events\"; they are more like `epoll(4)`.\n    90:     ///\n    91:     /// An implementation of `poll` should strive to return quickly, and should\n    92:     /// not block. Returning quickly prevents unnecessarily clogging up\n    93:     /// threads or event loops. If it is known ahead of time that a call to\n    94:     /// `poll` may end up taking a while, the work should be offloaded to a\n    95:     /// thread pool (or something similar) to ensure that `poll` can return\n    96:     /// quickly.\n    97:     ///\n    98:     /// # Panics\n    99:     ///\n   100:     /// Once a future has completed (returned `Ready` from `poll`), calling its\n   101:     /// `poll` method again may panic, block forever, or cause other kinds of\n   102:     /// problems; the `Future` trait places no requirements on the effects of\n   103:     /// such a call. However, as the `poll` method is not marked `unsafe`,\n   104:     /// Rust's usual rules apply: calls must never cause undefined behavior\n   105:     /// (memory corruption, incorrect use of `unsafe` functions, or the like),\n   106:     /// regardless of the future's state.\n   107:     ///\n   108:     /// [`Poll::Ready(val)`]: Poll::Ready\n   109:     /// [`Waker`]: crate::task::Waker\n   110:     /// [`Waker::wake`]: crate::task::Waker::wake\n   111:     #[lang = \"poll\"]\n   112:     #[stable(feature = \"futures_api\", since = \"1.36.0\")]\n   113:     fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;\n   114: }\n   115: \n   116: #[stable(feature = \"futures_api\", since = \"1.36.0\")]\n   117: impl<F: ?Sized + Future + Unpin> Future for &mut F {\n   118:     type Output = F::Output;",
    "nanvix_source": "    92:     /// not block. Returning quickly prevents unnecessarily clogging up\n    93:     /// threads or event loops. If it is known ahead of time that a call to\n    94:     /// `poll` may end up taking a while, the work should be offloaded to a\n    95:     /// thread pool (or something similar) to ensure that `poll` can return\n    96:     /// quickly.\n    97:     ///\n    98:     /// # Panics\n    99:     ///\n   100:     /// Once a future has completed (returned `Ready` from `poll`), calling its\n   101:     /// `poll` method again may panic, block forever, or cause other kinds of\n   102:     /// problems; the `Future` trait places no requirements on the effects of\n   103:     /// such a call. However, as the `poll` method is not marked `unsafe`,\n   104:     /// Rust's usual rules apply: calls must never cause undefined behavior\n   105:     /// (memory corruption, incorrect use of `unsafe` functions, or the like),\n   106:     /// regardless of the future's state.\n   107:     ///\n   108:     /// [`Poll::Ready(val)`]: Poll::Ready\n   109:     /// [`Waker`]: crate::task::Waker\n   110:     /// [`Waker::wake`]: crate::task::Waker::wake\n   111:     #[lang = \"poll\"]\n   112:     #[stable(feature = \"futures_api\", since = \"1.36.0\")]",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::future::IntoFuture::into_future",
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
      "name": "into_future",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:217",
        "kind": "trait",
        "name": "IntoFuture",
        "path": [
          "core",
          "future",
          "into_future",
          "IntoFuture"
        ]
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
          "qualified_path": {
            "args": null,
            "name": "IntoFuture",
            "self_type": {
              "generic": "Self"
            },
            "trait": {
              "args": null,
              "id": 217,
              "path": ""
            }
          }
        }
      }
    },
    "verification_source": "   101: #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   102: #[rustc_diagnostic_item = \"IntoFuture\"]\n   103: #[diagnostic::on_unimplemented(\n   104:     label = \"`{Self}` is not a future\",\n   105:     message = \"`{Self}` is not a future\",\n   106:     note = \"{Self} must be a future or must implement `IntoFuture` to be awaited\"\n   107: )]\n   108: pub trait IntoFuture {\n   109:     /// The output that the future will produce on completion.\n   110:     #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   111:     type Output;\n   112: \n   113:     /// Which kind of future are we turning this into?\n   114:     #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   115:     type IntoFuture: Future<Output = Self::Output>;\n   116: \n   117:     /// Creates a future from a value.\n   118:     ///\n   119:     /// # Examples\n   120:     ///\n   121:     /// Basic usage:\n   122:     ///\n   123:     /// ```no_run\n   124:     /// use std::future::IntoFuture;\n   125:     ///\n   126:     /// # async fn foo() {\n   127:     /// let v = async { \"meow\" };\n   128:     /// let mut fut = v.into_future();\n   129:     /// assert_eq!(\"meow\", fut.await);\n   130:     /// # }\n   131:     /// ```\n   132:     #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   133:     #[lang = \"into_future\"]",
    "nanvix_source": "   107: )]\n   108: pub trait IntoFuture {\n   109:     /// The output that the future will produce on completion.\n   110:     #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   111:     type Output;\n   112: \n   113:     /// Which kind of future are we turning this into?\n   114:     #[stable(feature = \"into_future\", since = \"1.64.0\")]\n   115:     type IntoFuture: Future<Output = Self::Output>;\n   116: \n   117:     /// Creates a future from a value.\n   118:     ///\n   119:     /// # Examples\n   120:     ///\n   121:     /// Basic usage:\n   122:     ///\n   123:     /// ```no_run\n   124:     /// use std::future::IntoFuture;\n   125:     ///\n   126:     /// # async fn foo() {\n   127:     /// let v = async { \"meow\" };",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::DoubleEndedIterator::nth_back",
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
      "name": "nth_back",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:74",
        "kind": "trait",
        "name": "DoubleEndedIterator",
        "path": [
          "core",
          "iter",
          "traits",
          "double_ended",
          "DoubleEndedIterator"
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
                      "qualified_path": {
                        "args": null,
                        "name": "Item",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": ""
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
    "verification_source": "   179:     ///\n   180:     /// let mut iter = a.iter();\n   181:     ///\n   182:     /// assert_eq!(iter.nth_back(1), Some(&2));\n   183:     /// assert_eq!(iter.nth_back(1), None);\n   184:     /// ```\n   185:     ///\n   186:     /// Returning `None` if there are less than `n + 1` elements:\n   187:     ///\n   188:     /// ```\n   189:     /// let a = [1, 2, 3];\n   190:     /// assert_eq!(a.iter().nth_back(10), None);\n   191:     /// ```\n   192:     #[inline]\n   193:     #[stable(feature = \"iter_nth_back\", since = \"1.37.0\")]\n   194:     #[rustc_non_const_trait_method]\n   195:     fn nth_back(&mut self, n: usize) -> Option<Self::Item> {\n   196:         if self.advance_back_by(n).is_err() {\n   197:             return None;\n   198:         }\n   199:         self.next_back()\n   200:     }\n   201: \n   202:     /// This is the reverse version of [`Iterator::try_fold()`]: it takes\n   203:     /// elements starting from the back of the iterator.\n   204:     ///\n   205:     /// # Examples\n   206:     ///\n   207:     /// Basic usage:\n   208:     ///\n   209:     /// ```\n   210:     /// let a = [\"1\", \"2\", \"3\"];\n   211:     /// let sum = a.iter()",
    "nanvix_source": "   233:     ///\n   234:     /// Returning `None` if there are less than `n + 1` elements:\n   235:     ///\n   236:     /// ```\n   237:     /// let a = [1, 2, 3];\n   238:     /// assert_eq!(a.iter().nth_back(10), None);\n   239:     /// ```\n   240:     #[inline]\n   241:     #[stable(feature = \"iter_nth_back\", since = \"1.37.0\")]\n   242:     #[rustc_non_const_trait_method]\n   243:     fn nth_back(&mut self, n: usize) -> Option<Self::Item> {\n   244:         if self.advance_back_by(n).is_err() {\n   245:             return None;\n   246:         }\n   247:         self.next_back()\n   248:     }\n   249: \n   250:     /// This is the reverse version of [`Iterator::try_fold()`]: it takes\n   251:     /// elements starting from the back of the iterator.\n   252:     ///\n   253:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::iter::DoubleEndedIterator::rfind",
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
        "params": [
          {
            "kind": {
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "P"
          }
        ],
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
                "generic": "Self"
              }
            }
          },
          {
            "bound_predicate": {
              "bounds": [
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": {
                        "parenthesized": {
                          "inputs": [
                            {
                              "borrowed_ref": {
                                "is_mutable": false,
                                "lifetime": null,
                                "type": {
                                  "qualified_path": {
                                    "args": null,
                                    "name": "Item",
                                    "self_type": {
                                      "generic": "Self"
                                    },
                                    "trait": {
                                      "args": null,
                                      "id": 82,
                                      "path": ""
                                    }
                                  }
                                }
                              }
                            }
                          ],
                          "output": {
                            "primitive": "bool"
                          }
                        }
                      },
                      "id": 22,
                      "path": "FnMut"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "P"
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
      "name": "rfind",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": false,
        "return_reference_is_mutable": false
      },
      "owner": {
        "item_id": "core:74",
        "kind": "trait",
        "name": "DoubleEndedIterator",
        "path": [
          "core",
          "iter",
          "traits",
          "double_ended",
          "DoubleEndedIterator"
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
            "predicate",
            {
              "generic": "P"
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
                      "qualified_path": {
                        "args": null,
                        "name": "Item",
                        "self_type": {
                          "generic": "Self"
                        },
                        "trait": {
                          "args": null,
                          "id": 82,
                          "path": ""
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
    "verification_source": "   355:     ///\n   356:     /// Stopping at the first `true`:\n   357:     ///\n   358:     /// ```\n   359:     /// let a = [1, 2, 3];\n   360:     ///\n   361:     /// let mut iter = a.iter();\n   362:     ///\n   363:     /// assert_eq!(iter.rfind(|&&x| x == 2), Some(&2));\n   364:     ///\n   365:     /// // we can still use `iter`, as there are more elements.\n   366:     /// assert_eq!(iter.next_back(), Some(&1));\n   367:     /// ```\n   368:     #[inline]\n   369:     #[stable(feature = \"iter_rfind\", since = \"1.27.0\")]\n   370:     #[rustc_non_const_trait_method]\n   371:     fn rfind<P>(&mut self, predicate: P) -> Option<Self::Item>\n   372:     where\n   373:         Self: Sized,\n   374:         P: FnMut(&Self::Item) -> bool,\n   375:     {\n   376:         #[inline]\n   377:         fn check<T>(mut predicate: impl FnMut(&T) -> bool) -> impl FnMut((), T) -> ControlFlow<T> {\n   378:             move |(), x| {\n   379:                 if predicate(&x) { ControlFlow::Break(x) } else { ControlFlow::Continue(()) }\n   380:             }\n   381:         }\n   382: \n   383:         self.try_rfold((), check(predicate)).break_value()\n   384:     }\n   385: }\n   386: \n   387: #[stable(feature = \"rust1\", since = \"1.0.0\")]",
    "nanvix_source": "   409:     /// let mut iter = a.iter();\n   410:     ///\n   411:     /// assert_eq!(iter.rfind(|&&x| x == 2), Some(&2));\n   412:     ///\n   413:     /// // we can still use `iter`, as there are more elements.\n   414:     /// assert_eq!(iter.next_back(), Some(&1));\n   415:     /// ```\n   416:     #[inline]\n   417:     #[stable(feature = \"iter_rfind\", since = \"1.27.0\")]\n   418:     #[rustc_non_const_trait_method]\n   419:     fn rfind<P>(&mut self, predicate: P) -> Option<Self::Item>\n   420:     where\n   421:         Self: Sized,\n   422:         P: FnMut(&Self::Item) -> bool,\n   423:     {\n   424:         #[inline]\n   425:         fn check<T>(mut predicate: impl FnMut(&T) -> bool) -> impl FnMut((), T) -> ControlFlow<T> {\n   426:             move |(), x| {\n   427:                 if predicate(&x) { ControlFlow::Break(x) } else { ControlFlow::Continue(()) }\n   428:             }\n   429:         }",
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
