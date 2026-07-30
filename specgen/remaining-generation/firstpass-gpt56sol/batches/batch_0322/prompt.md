For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::intrinsics::write_bytes",
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
      "name": "write_bytes",
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
            "val",
            {
              "primitive": "u8"
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
    "verification_source": "  2975: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2976: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2977: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2978: #[rustc_nounwind]\n  2979: #[rustc_intrinsic]\n  2980: pub const unsafe fn copy<T>(src: *const T, dst: *mut T, count: usize);\n  2981: \n  2982: /// This is an accidentally-stable alias to [`ptr::write_bytes`]; use that instead.\n  2983: // Note (intentionally not in the doc comment): `ptr::write_bytes` adds some extra\n  2984: // debug assertions; if you are writing compiler tests or code inside the standard library\n  2985: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  2986: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  2987: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  2988: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  2989: #[rustc_nounwind]\n  2990: #[rustc_intrinsic]\n  2991: pub const unsafe fn write_bytes<T>(dst: *mut T, val: u8, count: usize);\n  2992: \n  2993: /// Returns the minimum of two `f16` values, ignoring NaN.\n  2994: ///\n  2995: /// This behaves like IEEE 754-2019 minimumNumber, *except* that it does not order signed\n  2996: /// zeros deterministically. In particular:\n  2997: /// If one of the arguments is NaN (quiet or signaling), then the other argument is returned. If\n  2998: /// both arguments are NaN, returns NaN. If the inputs compare equal (such as for the case of `+0.0`\n  2999: /// and `-0.0`), either input may be returned non-deterministically.\n  3000: ///\n  3001: /// Note that, unlike most intrinsics, this is safe to call;\n  3002: /// it does not require an `unsafe` block.\n  3003: /// Therefore, implementations must not require the user to uphold\n  3004: /// any safety invariants.\n  3005: ///\n  3006: /// The stabilized version of this intrinsic is [`f16::min`].\n  3007: #[rustc_nounwind]",
    "nanvix_source": "  3055: \n  3056: /// This is an accidentally-stable alias to [`ptr::write_bytes`]; use that instead.\n  3057: // Note (intentionally not in the doc comment): `ptr::write_bytes` adds some extra\n  3058: // debug assertions; if you are writing compiler tests or code inside the standard library\n  3059: // that wants to avoid those debug assertions, directly call this intrinsic instead.\n  3060: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  3061: #[rustc_allowed_through_unstable_modules = \"import this function via `std::ptr` instead\"]\n  3062: #[rustc_const_stable(feature = \"const_intrinsic_copy\", since = \"1.83.0\")]\n  3063: #[rustc_nounwind]\n  3064: #[rustc_intrinsic]\n  3065: pub const unsafe fn write_bytes<T>(dst: *mut T, val: u8, count: usize);\n  3066: \n  3067: /// Returns the minimum of two `f16` values, ignoring NaN.\n  3068: ///\n  3069: /// This behaves like IEEE 754-2019 minimumNumber, *except* that it does not order signed\n  3070: /// zeros deterministically. In particular:\n  3071: /// If one of the arguments is NaN (quiet or signaling), then the other argument is returned. If\n  3072: /// both arguments are NaN, returns NaN. If the inputs compare equal (such as for the case of `+0.0`\n  3073: /// and `-0.0`), either input may be returned non-deterministically.\n  3074: ///\n  3075: /// Note that, unlike most intrinsics, this is safe to call;",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::ManuallyDrop::drop",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
              "bounds": [],
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
        "is_unsafe": true
      },
      "name": "drop",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "slot"
        ],
        "return_is_raw_pointer": false,
        "return_is_reference": false,
        "return_is_unit": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8610,
            "path": "ManuallyDrop"
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
        "impl_id": "core:8618",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8610",
        "resolved_owner_path": [
          "core",
          "mem",
          "manually_drop",
          "ManuallyDrop"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "slot",
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
                            "type": {
                              "generic": "T"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 8610,
                    "path": "ManuallyDrop"
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
    "verification_source": "   244:     /// # Safety\n   245:     ///\n   246:     /// This function runs the destructor of the contained value. Other than changes made by\n   247:     /// the destructor itself, the memory is left unchanged, and so as far as the compiler is\n   248:     /// concerned still holds a bit-pattern which is valid for the type `T`.\n   249:     ///\n   250:     /// However, this \"zombie\" value should not be exposed to safe code, and this function\n   251:     /// should not be called more than once. To use a value after it's been dropped, or drop\n   252:     /// a value multiple times, can cause Undefined Behavior (depending on what `drop` does).\n   253:     /// This is normally prevented by the type system, but users of `ManuallyDrop` must\n   254:     /// uphold those guarantees without assistance from the compiler.\n   255:     ///\n   256:     /// [pinned]: crate::pin\n   257:     #[stable(feature = \"manually_drop\", since = \"1.20.0\")]\n   258:     #[inline]\n   259:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n   260:     pub const unsafe fn drop(slot: &mut ManuallyDrop<T>)\n   261:     where\n   262:         T: [const] Destruct,\n   263:     {\n   264:         // SAFETY: we are dropping the value pointed to by a mutable reference\n   265:         // which is guaranteed to be valid for writes.\n   266:         // It is up to the caller to make sure that `slot` isn't dropped again.\n   267:         unsafe { ptr::drop_in_place(slot.value.as_mut()) }\n   268:     }\n   269: }\n   270: \n   271: #[stable(feature = \"manually_drop\", since = \"1.20.0\")]\n   272: #[rustc_const_unstable(feature = \"const_convert\", issue = \"143773\")]\n   273: impl<T: ?Sized> const Deref for ManuallyDrop<T> {\n   274:     type Target = T;\n   275:     #[inline(always)]\n   276:     fn deref(&self) -> &T {",
    "nanvix_source": "   247:     /// However, this \"zombie\" value should not be exposed to safe code, and this function\n   248:     /// should not be called more than once. To use a value after it's been dropped, or drop\n   249:     /// a value multiple times, can cause Undefined Behavior (depending on what `drop` does).\n   250:     /// This is normally prevented by the type system, but users of `ManuallyDrop` must\n   251:     /// uphold those guarantees without assistance from the compiler.\n   252:     ///\n   253:     /// [pinned]: crate::pin\n   254:     #[stable(feature = \"manually_drop\", since = \"1.20.0\")]\n   255:     #[inline]\n   256:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n   257:     pub const unsafe fn drop(slot: &mut ManuallyDrop<T>)\n   258:     where\n   259:         T: [const] Destruct,\n   260:     {\n   261:         // SAFETY: we are dropping the value pointed to by a mutable reference\n   262:         // which is guaranteed to be valid for writes.\n   263:         // It is up to the caller to make sure that `slot` isn't dropped again.\n   264:         unsafe { ptr::drop_in_place(slot.value.as_mut()) }\n   265:     }\n   266: }\n   267: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::ManuallyDrop::take",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": true,
        "is_unsafe": true
      },
      "name": "take",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "slot"
        ],
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8610,
            "path": "ManuallyDrop"
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
        "impl_id": "core:8615",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8610",
        "resolved_owner_path": [
          "core",
          "mem",
          "manually_drop",
          "ManuallyDrop"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "slot",
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
                            "type": {
                              "generic": "T"
                            }
                          }
                        ],
                        "constraints": []
                      }
                    },
                    "id": 8610,
                    "path": "ManuallyDrop"
                  }
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
    "verification_source": "   211:     /// Instead of using [`ManuallyDrop::drop`] to manually drop the value,\n   212:     /// you can use this method to take the value and use it however desired.\n   213:     ///\n   214:     /// Whenever possible, it is preferable to use [`into_inner`][`ManuallyDrop::into_inner`]\n   215:     /// instead, which prevents duplicating the content of the `ManuallyDrop<T>`.\n   216:     ///\n   217:     /// # Safety\n   218:     ///\n   219:     /// This function semantically moves out the contained value without preventing further usage,\n   220:     /// leaving the state of this container unchanged.\n   221:     /// It is your responsibility to ensure that this `ManuallyDrop` is not used again.\n   222:     ///\n   223:     #[must_use = \"if you don't need the value, you can use `ManuallyDrop::drop` instead\"]\n   224:     #[stable(feature = \"manually_drop_take\", since = \"1.42.0\")]\n   225:     #[rustc_const_unstable(feature = \"const_manually_drop_take\", issue = \"148773\")]\n   226:     #[inline]\n   227:     pub const unsafe fn take(slot: &mut ManuallyDrop<T>) -> T {\n   228:         // SAFETY: we are reading from a reference, which is guaranteed\n   229:         // to be valid for reads.\n   230:         unsafe { ptr::read(slot.value.as_ref()) }\n   231:     }\n   232: }\n   233: \n   234: impl<T: ?Sized> ManuallyDrop<T> {\n   235:     /// Manually drops the contained value.\n   236:     ///\n   237:     /// This is exactly equivalent to calling [`ptr::drop_in_place`] with a\n   238:     /// pointer to the contained value. As such, unless the contained value is a\n   239:     /// packed struct, the destructor will be called in-place without moving the\n   240:     /// value, and thus can be used to safely drop [pinned] data.\n   241:     ///\n   242:     /// If you have ownership of the value, you can use [`ManuallyDrop::into_inner`] instead.\n   243:     ///",
    "nanvix_source": "   214:     /// # Safety\n   215:     ///\n   216:     /// This function semantically moves out the contained value without preventing further usage,\n   217:     /// leaving the state of this container unchanged.\n   218:     /// It is your responsibility to ensure that this `ManuallyDrop` is not used again.\n   219:     ///\n   220:     #[must_use = \"if you don't need the value, you can use `ManuallyDrop::drop` instead\"]\n   221:     #[stable(feature = \"manually_drop_take\", since = \"1.42.0\")]\n   222:     #[rustc_const_unstable(feature = \"const_manually_drop_take\", issue = \"148773\")]\n   223:     #[inline]\n   224:     pub const unsafe fn take(slot: &mut ManuallyDrop<T>) -> T {\n   225:         // SAFETY: we are reading from a reference, which is guaranteed\n   226:         // to be valid for reads.\n   227:         unsafe { ptr::read(slot.value.as_ref()) }\n   228:     }\n   229: }\n   230: \n   231: impl<T: ?Sized> ManuallyDrop<T> {\n   232:     /// Manually drops the contained value.\n   233:     ///\n   234:     /// This is exactly equivalent to calling [`ptr::drop_in_place`] with a",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::MaybeUninit::as_mut_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_mut_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [
          "self"
        ],
        "return_is_raw_pointer": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
        ],
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
    "verification_source": "   642:     /// *Incorrect* usage of this method:\n   643:     ///\n   644:     /// ```rust,no_run\n   645:     /// use std::mem::MaybeUninit;\n   646:     ///\n   647:     /// let mut x = MaybeUninit::<Vec<u32>>::uninit();\n   648:     /// let x_vec = unsafe { &mut *x.as_mut_ptr() };\n   649:     /// // We have created a reference to an uninitialized vector! This is undefined behavior. \u26a0\ufe0f\n   650:     /// ```\n   651:     ///\n   652:     /// (Notice that the rules around references to uninitialized data are not finalized yet, but\n   653:     /// until they are, it is advisable to avoid them.)\n   654:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   655:     #[rustc_const_stable(feature = \"const_maybe_uninit_as_mut_ptr\", since = \"1.83.0\")]\n   656:     #[rustc_as_ptr]\n   657:     #[inline(always)]\n   658:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n   659:         // `MaybeUninit` and `ManuallyDrop` are both `repr(transparent)` so we can cast the pointer.\n   660:         self as *mut _ as *mut T\n   661:     }\n   662: \n   663:     /// Extracts the value from the `MaybeUninit<T>` container. This is a great way\n   664:     /// to ensure that the data will get dropped, because the resulting `T` is\n   665:     /// subject to the usual drop handling.\n   666:     ///\n   667:     /// # Safety\n   668:     ///\n   669:     /// It is up to the caller to guarantee that the `MaybeUninit<T>` really is in an initialized\n   670:     /// state, i.e., a state that is considered [\"valid\" for type `T`][validity]. Calling this when\n   671:     /// the content is not yet fully initialized causes immediate undefined behavior. The\n   672:     /// [type-level documentation][inv] contains more information about this initialization\n   673:     /// invariant.\n   674:     ///",
    "nanvix_source": "   649:     /// let x_vec = unsafe { &mut *x.as_mut_ptr() };\n   650:     /// // We have created a reference to an uninitialized vector! This is undefined behavior. \u26a0\ufe0f\n   651:     /// ```\n   652:     ///\n   653:     /// (Notice that the rules around references to uninitialized data are not finalized yet, but\n   654:     /// until they are, it is advisable to avoid them.)\n   655:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   656:     #[rustc_const_stable(feature = \"const_maybe_uninit_as_mut_ptr\", since = \"1.83.0\")]\n   657:     #[rustc_as_ptr]\n   658:     #[inline(always)]\n   659:     pub const fn as_mut_ptr(&mut self) -> *mut T {\n   660:         // `MaybeUninit` and `ManuallyDrop` are both `repr(transparent)` so we can cast the pointer.\n   661:         self as *mut _ as *mut T\n   662:     }\n   663: \n   664:     /// Extracts the value from the `MaybeUninit<T>` container. This is a great way\n   665:     /// to ensure that the data will get dropped, because the resulting `T` is\n   666:     /// subject to the usual drop handling.\n   667:     ///\n   668:     /// # Safety\n   669:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::MaybeUninit::as_ptr",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature",
      "raw_pointer_result"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "raw_pointer_equality"
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
      "name": "as_ptr",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": true,
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
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
          "raw_pointer": {
            "is_mutable": false,
            "type": {
              "generic": "T"
            }
          }
        }
      }
    },
    "verification_source": "   600:     /// *Incorrect* usage of this method:\n   601:     ///\n   602:     /// ```rust,no_run\n   603:     /// use std::mem::MaybeUninit;\n   604:     ///\n   605:     /// let x = MaybeUninit::<Vec<u32>>::uninit();\n   606:     /// let x_vec = unsafe { &*x.as_ptr() };\n   607:     /// // We have created a reference to an uninitialized vector! This is undefined behavior. \u26a0\ufe0f\n   608:     /// ```\n   609:     ///\n   610:     /// (Notice that the rules around references to uninitialized data are not finalized yet, but\n   611:     /// until they are, it is advisable to avoid them.)\n   612:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   613:     #[rustc_const_stable(feature = \"const_maybe_uninit_as_ptr\", since = \"1.59.0\")]\n   614:     #[rustc_as_ptr]\n   615:     #[inline(always)]\n   616:     pub const fn as_ptr(&self) -> *const T {\n   617:         // `MaybeUninit` and `ManuallyDrop` are both `repr(transparent)` so we can cast the pointer.\n   618:         self as *const _ as *const T\n   619:     }\n   620: \n   621:     /// Gets a mutable pointer to the contained value. Reading from this pointer or turning it\n   622:     /// into a reference is undefined behavior unless the `MaybeUninit<T>` is initialized.\n   623:     ///\n   624:     /// # Examples\n   625:     ///\n   626:     /// Correct usage of this method:\n   627:     ///\n   628:     /// ```rust\n   629:     /// use std::mem::MaybeUninit;\n   630:     ///\n   631:     /// let mut x = MaybeUninit::<Vec<u32>>::uninit();\n   632:     /// x.write(vec![0, 1, 2]);",
    "nanvix_source": "   607:     /// let x_vec = unsafe { &*x.as_ptr() };\n   608:     /// // We have created a reference to an uninitialized vector! This is undefined behavior. \u26a0\ufe0f\n   609:     /// ```\n   610:     ///\n   611:     /// (Notice that the rules around references to uninitialized data are not finalized yet, but\n   612:     /// until they are, it is advisable to avoid them.)\n   613:     #[stable(feature = \"maybe_uninit\", since = \"1.36.0\")]\n   614:     #[rustc_const_stable(feature = \"const_maybe_uninit_as_ptr\", since = \"1.59.0\")]\n   615:     #[rustc_as_ptr]\n   616:     #[inline(always)]\n   617:     pub const fn as_ptr(&self) -> *const T {\n   618:         // `MaybeUninit` and `ManuallyDrop` are both `repr(transparent)` so we can cast the pointer.\n   619:         self as *const _ as *const T\n   620:     }\n   621: \n   622:     /// Gets a mutable pointer to the contained value. Reading from this pointer or turning it\n   623:     /// into a reference is undefined behavior unless the `MaybeUninit<T>` is initialized.\n   624:     ///\n   625:     /// # Examples\n   626:     ///\n   627:     /// Correct usage of this method:",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::mem::MaybeUninit::assume_init_drop",
    "generation_group": "unsafe_or_representation_sensitive",
    "classification": "unsafe_or_representation_sensitive",
    "classification_reasons": [
      "unsafe_or_raw_pointer_signature"
    ],
    "category": "data_structure",
    "kinds": [
      "inherent_method"
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
              "bounds": [],
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
        "is_unsafe": true
      },
      "name": "assume_init_drop",
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
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 8278,
            "path": "MaybeUninit"
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
        "impl_id": "core:8682",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:8278",
        "resolved_owner_path": [
          "core",
          "mem",
          "maybe_uninit",
          "MaybeUninit"
        ],
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
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   809:     /// It is up to the caller to guarantee that the `MaybeUninit<T>` really is\n   810:     /// in an initialized state. Calling this when the content is not yet fully\n   811:     /// initialized causes undefined behavior.\n   812:     ///\n   813:     /// On top of that, all additional invariants of the type `T` must be\n   814:     /// satisfied, as the `Drop` implementation of `T` (or its members) may\n   815:     /// rely on this. For example, setting a `Vec<T>` to an invalid but\n   816:     /// non-null address makes it initialized (under the current implementation;\n   817:     /// this does not constitute a stable guarantee), because the only\n   818:     /// requirement the compiler knows about it is that the data pointer must be\n   819:     /// non-null. Dropping such a `Vec<T>` however will cause undefined\n   820:     /// behavior.\n   821:     ///\n   822:     /// [`assume_init`]: MaybeUninit::assume_init\n   823:     #[stable(feature = \"maybe_uninit_extra\", since = \"1.60.0\")]\n   824:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n   825:     pub const unsafe fn assume_init_drop(&mut self)\n   826:     where\n   827:         T: [const] Destruct,\n   828:     {\n   829:         // SAFETY: the caller must guarantee that `self` is initialized and\n   830:         // satisfies all invariants of `T`.\n   831:         // Dropping the value in place is safe if that is the case.\n   832:         unsafe { ptr::drop_in_place(self.as_mut_ptr()) }\n   833:     }\n   834: \n   835:     /// Gets a shared reference to the contained value.\n   836:     ///\n   837:     /// This can be useful when we want to access a `MaybeUninit` that has been\n   838:     /// initialized but don't have ownership of the `MaybeUninit` (preventing the use\n   839:     /// of `.assume_init()`).\n   840:     ///\n   841:     /// # Safety",
    "nanvix_source": "   816:     /// rely on this. For example, setting a `Vec<T>` to an invalid but\n   817:     /// non-null address makes it initialized (under the current implementation;\n   818:     /// this does not constitute a stable guarantee), because the only\n   819:     /// requirement the compiler knows about it is that the data pointer must be\n   820:     /// non-null. Dropping such a `Vec<T>` however will cause undefined\n   821:     /// behavior.\n   822:     ///\n   823:     /// [`assume_init`]: MaybeUninit::assume_init\n   824:     #[stable(feature = \"maybe_uninit_extra\", since = \"1.60.0\")]\n   825:     #[rustc_const_unstable(feature = \"const_drop_in_place\", issue = \"109342\")]\n   826:     pub const unsafe fn assume_init_drop(&mut self)\n   827:     where\n   828:         T: [const] Destruct,\n   829:     {\n   830:         // SAFETY: the caller must guarantee that `self` is initialized and\n   831:         // satisfies all invariants of `T`.\n   832:         // Dropping the value in place is safe if that is the case.\n   833:         unsafe { ptr::drop_in_place(self.as_mut_ptr()) }\n   834:     }\n   835: \n   836:     /// Gets a shared reference to the contained value.",
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
