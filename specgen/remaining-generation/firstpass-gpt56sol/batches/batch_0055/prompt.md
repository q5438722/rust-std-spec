For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::collections::HashMap::get_disjoint_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Q"
          },
          {
            "kind": {
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Q"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 399,
                      "path": "Borrow"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
                      "args": null,
                      "id": 554,
                      "path": "Hash"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 136,
                      "path": "Eq"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Q"
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
      "name": "get_disjoint_mut",
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
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "K"
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
                        "args": null,
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "args": null,
                        "id": 834,
                        "path": "Allocator"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "A"
                }
              }
            }
          ]
        },
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          ],
          [
            "ks",
            {
              "array": {
                "len": "N",
                "type": {
                  "borrowed_ref": {
                    "is_mutable": false,
                    "lifetime": null,
                    "type": {
                      "generic": "Q"
                    }
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "array": {
            "len": "N",
            "type": {
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
                              "generic": "V"
                            }
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1151:     ///\n  1152:     /// ```should_panic\n  1153:     /// use std::collections::HashMap;\n  1154:     ///\n  1155:     /// let mut libraries = HashMap::new();\n  1156:     /// libraries.insert(\"Athen\u00e6um\".to_string(), 1807);\n  1157:     ///\n  1158:     /// // Duplicate keys panic!\n  1159:     /// let got = libraries.get_disjoint_mut([\n  1160:     ///     \"Athen\u00e6um\",\n  1161:     ///     \"Athen\u00e6um\",\n  1162:     /// ]);\n  1163:     /// ```\n  1164:     #[inline]\n  1165:     #[doc(alias = \"get_many_mut\")]\n  1166:     #[stable(feature = \"map_many_mut\", since = \"1.86.0\")]\n  1167:     pub fn get_disjoint_mut<Q: ?Sized, const N: usize>(\n  1168:         &mut self,\n  1169:         ks: [&Q; N],\n  1170:     ) -> [Option<&'_ mut V>; N]\n  1171:     where\n  1172:         K: Borrow<Q>,\n  1173:         Q: Hash + Eq,\n  1174:     {\n  1175:         self.base.get_disjoint_mut(ks)\n  1176:     }\n  1177: \n  1178:     /// Attempts to get mutable references to `N` values in the map at once, without validating that\n  1179:     /// the values are unique.\n  1180:     ///\n  1181:     /// Returns an array of length `N` with the results of each query. `None` will be used if\n  1182:     /// the key is missing.\n  1183:     ///",
    "nanvix_source": "  1162:     ///\n  1163:     /// // Duplicate keys panic!\n  1164:     /// let got = libraries.get_disjoint_mut([\n  1165:     ///     \"Athen\u00e6um\",\n  1166:     ///     \"Athen\u00e6um\",\n  1167:     /// ]);\n  1168:     /// ```\n  1169:     #[inline]\n  1170:     #[doc(alias = \"get_many_mut\")]\n  1171:     #[stable(feature = \"map_many_mut\", since = \"1.86.0\")]\n  1172:     pub fn get_disjoint_mut<Q: ?Sized, const N: usize>(\n  1173:         &mut self,\n  1174:         ks: [&Q; N],\n  1175:     ) -> [Option<&'_ mut V>; N]\n  1176:     where\n  1177:         K: Borrow<Q>,\n  1178:         Q: Hash + Eq,\n  1179:     {\n  1180:         self.base.get_disjoint_mut(ks)\n  1181:     }\n  1182: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::get_disjoint_unchecked_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Q"
          },
          {
            "kind": {
              "const": {
                "default": null,
                "type": {
                  "primitive": "usize"
                }
              }
            },
            "name": "N"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Q"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 399,
                      "path": "Borrow"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
                      "args": null,
                      "id": 554,
                      "path": "Hash"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 136,
                      "path": "Eq"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Q"
              }
            }
          }
        ]
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": true
      },
      "name": "get_disjoint_unchecked_mut",
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
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "K"
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
                        "args": null,
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "args": null,
                        "id": 834,
                        "path": "Allocator"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "A"
                }
              }
            }
          ]
        },
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          ],
          [
            "ks",
            {
              "array": {
                "len": "N",
                "type": {
                  "borrowed_ref": {
                    "is_mutable": false,
                    "lifetime": null,
                    "type": {
                      "generic": "Q"
                    }
                  }
                }
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "array": {
            "len": "N",
            "type": {
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
                              "generic": "V"
                            }
                          }
                        }
                      }
                    ],
                    "constraints": []
                  }
                },
                "id": 56,
                "path": "Option"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1218:     ///         Some(&mut 1807),\n  1219:     ///         Some(&mut 1800),\n  1220:     ///     ],\n  1221:     /// );\n  1222:     ///\n  1223:     /// // SAFETY: The keys do not overlap.\n  1224:     /// let got = unsafe { libraries.get_disjoint_unchecked_mut([\n  1225:     ///     \"Athen\u00e6um\",\n  1226:     ///     \"New York Public Library\",\n  1227:     /// ]) };\n  1228:     /// // Missing keys result in None\n  1229:     /// assert_eq!(got, [Some(&mut 1807), None]);\n  1230:     /// ```\n  1231:     #[inline]\n  1232:     #[doc(alias = \"get_many_unchecked_mut\")]\n  1233:     #[stable(feature = \"map_many_mut\", since = \"1.86.0\")]\n  1234:     pub unsafe fn get_disjoint_unchecked_mut<Q: ?Sized, const N: usize>(\n  1235:         &mut self,\n  1236:         ks: [&Q; N],\n  1237:     ) -> [Option<&'_ mut V>; N]\n  1238:     where\n  1239:         K: Borrow<Q>,\n  1240:         Q: Hash + Eq,\n  1241:     {\n  1242:         unsafe { self.base.get_disjoint_unchecked_mut(ks) }\n  1243:     }\n  1244: \n  1245:     /// Returns `true` if the map contains a value for the specified key.\n  1246:     ///\n  1247:     /// The key may be any borrowed form of the map's key type, but\n  1248:     /// [`Hash`] and [`Eq`] on the borrowed form *must* match those for\n  1249:     /// the key type.\n  1250:     ///",
    "nanvix_source": "  1229:     /// let got = unsafe { libraries.get_disjoint_unchecked_mut([\n  1230:     ///     \"Athen\u00e6um\",\n  1231:     ///     \"New York Public Library\",\n  1232:     /// ]) };\n  1233:     /// // Missing keys result in None\n  1234:     /// assert_eq!(got, [Some(&mut 1807), None]);\n  1235:     /// ```\n  1236:     #[inline]\n  1237:     #[doc(alias = \"get_many_unchecked_mut\")]\n  1238:     #[stable(feature = \"map_many_mut\", since = \"1.86.0\")]\n  1239:     pub unsafe fn get_disjoint_unchecked_mut<Q: ?Sized, const N: usize>(\n  1240:         &mut self,\n  1241:         ks: [&Q; N],\n  1242:     ) -> [Option<&'_ mut V>; N]\n  1243:     where\n  1244:         K: Borrow<Q>,\n  1245:         Q: Hash + Eq,\n  1246:     {\n  1247:         unsafe { self.base.get_disjoint_unchecked_mut(ks) }\n  1248:     }\n  1249: ",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::collections::HashMap::get_mut",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
              "type": {
                "bounds": [],
                "default": null,
                "is_synthetic": false
              }
            },
            "name": "Q"
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
                      "args": {
                        "angle_bracketed": {
                          "args": [
                            {
                              "type": {
                                "generic": "Q"
                              }
                            }
                          ],
                          "constraints": []
                        }
                      },
                      "id": 399,
                      "path": "Borrow"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "K"
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
                      "args": null,
                      "id": 554,
                      "path": "Hash"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "none",
                    "trait": {
                      "args": null,
                      "id": 136,
                      "path": "Eq"
                    }
                  }
                },
                {
                  "trait_bound": {
                    "generic_params": [],
                    "modifier": "maybe",
                    "trait": {
                      "args": null,
                      "id": 8,
                      "path": "Sized"
                    }
                  }
                }
              ],
              "generic_params": [],
              "type": {
                "generic": "Q"
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
      "name": "get_mut",
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
        "for": {
          "resolved_path": {
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "type": {
                      "generic": "K"
                    }
                  },
                  {
                    "type": {
                      "generic": "V"
                    }
                  },
                  {
                    "type": {
                      "generic": "S"
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
            "id": 832,
            "path": "HashMap"
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
              "name": "K"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "V"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "S"
            },
            {
              "kind": {
                "type": {
                  "bounds": [],
                  "default": null,
                  "is_synthetic": false
                }
              },
              "name": "A"
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
                        "id": 136,
                        "path": "Eq"
                      }
                    }
                  },
                  {
                    "trait_bound": {
                      "generic_params": [],
                      "modifier": "none",
                      "trait": {
                        "args": null,
                        "id": 554,
                        "path": "Hash"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "K"
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
                        "args": null,
                        "id": 842,
                        "path": "BuildHasher"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "S"
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
                        "args": null,
                        "id": 834,
                        "path": "Allocator"
                      }
                    }
                  }
                ],
                "generic_params": [],
                "type": {
                  "generic": "A"
                }
              }
            }
          ]
        },
        "impl_id": "std:890",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:832",
        "resolved_owner_path": [
          "std",
          "collections",
          "hash",
          "map",
          "HashMap"
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
          ],
          [
            "k",
            {
              "borrowed_ref": {
                "is_mutable": false,
                "lifetime": null,
                "type": {
                  "generic": "Q"
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
                        "is_mutable": true,
                        "lifetime": null,
                        "type": {
                          "generic": "V"
                        }
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 56,
            "path": "Option"
          }
        }
      }
    },
    "verification_source": "  1276:     /// the key type.\n  1277:     ///\n  1278:     /// # Examples\n  1279:     ///\n  1280:     /// ```\n  1281:     /// use std::collections::HashMap;\n  1282:     ///\n  1283:     /// let mut map = HashMap::new();\n  1284:     /// map.insert(1, \"a\");\n  1285:     /// if let Some(x) = map.get_mut(&1) {\n  1286:     ///     *x = \"b\";\n  1287:     /// }\n  1288:     /// assert_eq!(map[&1], \"b\");\n  1289:     /// ```\n  1290:     #[inline]\n  1291:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1292:     pub fn get_mut<Q: ?Sized>(&mut self, k: &Q) -> Option<&mut V>\n  1293:     where\n  1294:         K: Borrow<Q>,\n  1295:         Q: Hash + Eq,\n  1296:     {\n  1297:         self.base.get_mut(k)\n  1298:     }\n  1299: \n  1300:     /// Inserts a key-value pair into the map.\n  1301:     ///\n  1302:     /// If the map did not have this key present, [`None`] is returned.\n  1303:     ///\n  1304:     /// If the map did have this key present, the value is updated, and the old\n  1305:     /// value is returned. The key is not updated, though; this matters for\n  1306:     /// types that can be `==` without being identical. See the [module-level\n  1307:     /// documentation] for more.\n  1308:     ///",
    "nanvix_source": "  1287:     ///\n  1288:     /// let mut map = HashMap::new();\n  1289:     /// map.insert(1, \"a\");\n  1290:     /// if let Some(x) = map.get_mut(&1) {\n  1291:     ///     *x = \"b\";\n  1292:     /// }\n  1293:     /// assert_eq!(map[&1], \"b\");\n  1294:     /// ```\n  1295:     #[inline]\n  1296:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1297:     pub fn get_mut<Q: ?Sized>(&mut self, k: &Q) -> Option<&mut V>\n  1298:     where\n  1299:         K: Borrow<Q>,\n  1300:         Q: Hash + Eq,\n  1301:     {\n  1302:         self.base.get_mut(k)\n  1303:     }\n  1304: \n  1305:     /// Inserts a key-value pair into the map.\n  1306:     ///\n  1307:     /// If the map did not have this key present, [`None`] is returned.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::ffi::OsString::leak",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "leak",
      "observability": {
        "has_modeled_output": true,
        "mutable_inputs": [],
        "return_is_raw_pointer": false,
        "return_is_reference": true,
        "return_is_unit": false,
        "return_reference_is_mutable": true
      },
      "owner": {
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1846,
            "path": "OsString"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:2095",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1846",
        "resolved_owner_path": [
          "std",
          "ffi",
          "os_str",
          "OsString"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": "'a",
            "type": {
              "resolved_path": {
                "args": null,
                "id": 1857,
                "path": "OsStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   557: \n   558:     /// Consumes and leaks the `OsString`, returning a mutable reference to the contents,\n   559:     /// `&'a mut OsStr`.\n   560:     ///\n   561:     /// The caller has free choice over the returned lifetime, including 'static.\n   562:     /// Indeed, this function is ideally used for data that lives for the remainder of\n   563:     /// the program\u2019s life, as dropping the returned reference will cause a memory leak.\n   564:     ///\n   565:     /// It does not reallocate or shrink the `OsString`, so the leaked allocation may include\n   566:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n   567:     /// capacity, call [`into_boxed_os_str`], and then [`Box::leak`] instead.\n   568:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n   569:     ///\n   570:     /// [`into_boxed_os_str`]: Self::into_boxed_os_str\n   571:     #[stable(feature = \"os_string_pathbuf_leak\", since = \"1.89.0\")]\n   572:     #[inline]\n   573:     pub fn leak<'a>(self) -> &'a mut OsStr {\n   574:         OsStr::from_inner_mut(self.inner.leak())\n   575:     }\n   576: \n   577:     /// Truncate the `OsString` to the specified length.\n   578:     ///\n   579:     /// If `new_len` is greater than the string's current length, this has no\n   580:     /// effect.\n   581:     ///\n   582:     /// # Panics\n   583:     ///\n   584:     /// Panics if `len` does not lie on a valid `OsStr` boundary\n   585:     /// (as described in [`OsStr::slice_encoded_bytes`]).\n   586:     #[inline]\n   587:     #[unstable(feature = \"os_string_truncate\", issue = \"133262\")]\n   588:     pub fn truncate(&mut self, len: usize) {\n   589:         if len <= self.len() {",
    "nanvix_source": "   555:     /// the program\u2019s life, as dropping the returned reference will cause a memory leak.\n   556:     ///\n   557:     /// It does not reallocate or shrink the `OsString`, so the leaked allocation may include\n   558:     /// unused capacity that is not part of the returned slice. If you want to discard excess\n   559:     /// capacity, call [`into_boxed_os_str`], and then [`Box::leak`] instead.\n   560:     /// However, keep in mind that trimming the capacity may result in a reallocation and copy.\n   561:     ///\n   562:     /// [`into_boxed_os_str`]: Self::into_boxed_os_str\n   563:     #[stable(feature = \"os_string_pathbuf_leak\", since = \"1.89.0\")]\n   564:     #[inline]\n   565:     pub fn leak<'a>(self) -> &'a mut OsStr {\n   566:         OsStr::from_inner_mut(self.inner.leak())\n   567:     }\n   568: \n   569:     /// Truncate the `OsString` to the specified length.\n   570:     ///\n   571:     /// If `new_len` is greater than the string's current length, this has no\n   572:     /// effect.\n   573:     ///\n   574:     /// # Panics\n   575:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::Path::as_mut_os_str",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_mut_os_str",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1802,
            "path": "Path"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:7116",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1802",
        "resolved_owner_path": [
          "std",
          "path",
          "Path"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 1857,
                "path": "OsStr"
              }
            }
          }
        }
      }
    },
    "verification_source": "  2423:     ///\n  2424:     /// # Examples\n  2425:     ///\n  2426:     /// ```\n  2427:     /// use std::path::{Path, PathBuf};\n  2428:     ///\n  2429:     /// let mut path = PathBuf::from(\"Foo.TXT\");\n  2430:     ///\n  2431:     /// assert_ne!(path, Path::new(\"foo.txt\"));\n  2432:     ///\n  2433:     /// path.as_mut_os_str().make_ascii_lowercase();\n  2434:     /// assert_eq!(path, Path::new(\"foo.txt\"));\n  2435:     /// ```\n  2436:     #[stable(feature = \"path_as_mut_os_str\", since = \"1.70.0\")]\n  2437:     #[must_use]\n  2438:     #[inline]\n  2439:     pub fn as_mut_os_str(&mut self) -> &mut OsStr {\n  2440:         &mut self.inner\n  2441:     }\n  2442: \n  2443:     /// Yields a [`&str`] slice if the `Path` is valid unicode.\n  2444:     ///\n  2445:     /// This conversion may entail doing a check for UTF-8 validity.\n  2446:     /// Note that validation is performed because non-UTF-8 strings are\n  2447:     /// perfectly valid for some OS.\n  2448:     ///\n  2449:     /// [`&str`]: str\n  2450:     ///\n  2451:     /// # Examples\n  2452:     ///\n  2453:     /// ```\n  2454:     /// use std::path::Path;\n  2455:     ///",
    "nanvix_source": "  2447:     /// let mut path = PathBuf::from(\"Foo.TXT\");\n  2448:     ///\n  2449:     /// assert_ne!(path, Path::new(\"foo.txt\"));\n  2450:     ///\n  2451:     /// path.as_mut_os_str().make_ascii_lowercase();\n  2452:     /// assert_eq!(path, Path::new(\"foo.txt\"));\n  2453:     /// ```\n  2454:     #[stable(feature = \"path_as_mut_os_str\", since = \"1.70.0\")]\n  2455:     #[must_use]\n  2456:     #[inline]\n  2457:     pub fn as_mut_os_str(&mut self) -> &mut OsStr {\n  2458:         &mut self.inner\n  2459:     }\n  2460: \n  2461:     /// Yields a [`&str`] slice if the `Path` is valid unicode.\n  2462:     ///\n  2463:     /// This conversion may entail doing a check for UTF-8 validity.\n  2464:     /// Note that validation is performed because non-UTF-8 strings are\n  2465:     /// perfectly valid for some OS.\n  2466:     ///\n  2467:     /// [`&str`]: str",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::path::PathBuf::as_mut_os_string",
    "generation_group": "determinism_checker_unsupported",
    "classification": "determinism_checker_unsupported",
    "classification_reasons": [
      "mutable_reference_return_not_supported"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "as_mut_os_string",
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
        "for": {
          "resolved_path": {
            "args": null,
            "id": 1799,
            "path": "PathBuf"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "std:6965",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:1799",
        "resolved_owner_path": [
          "std",
          "path",
          "PathBuf"
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
          "borrowed_ref": {
            "is_mutable": true,
            "lifetime": null,
            "type": {
              "resolved_path": {
                "args": null,
                "id": 1846,
                "path": "OsString"
              }
            }
          }
        }
      }
    },
    "verification_source": "  1762:     ///\n  1763:     /// ```\n  1764:     /// use std::path::{Path, PathBuf};\n  1765:     ///\n  1766:     /// let mut path = PathBuf::from(\"/foo\");\n  1767:     ///\n  1768:     /// path.push(\"bar\");\n  1769:     /// assert_eq!(path, Path::new(\"/foo/bar\"));\n  1770:     ///\n  1771:     /// // OsString's `push` does not add a separator.\n  1772:     /// path.as_mut_os_string().push(\"baz\");\n  1773:     /// assert_eq!(path, Path::new(\"/foo/barbaz\"));\n  1774:     /// ```\n  1775:     #[stable(feature = \"path_as_mut_os_str\", since = \"1.70.0\")]\n  1776:     #[must_use]\n  1777:     #[inline]\n  1778:     pub fn as_mut_os_string(&mut self) -> &mut OsString {\n  1779:         &mut self.inner\n  1780:     }\n  1781: \n  1782:     /// Consumes the `PathBuf`, yielding its internal [`OsString`] storage.\n  1783:     ///\n  1784:     /// # Examples\n  1785:     ///\n  1786:     /// ```\n  1787:     /// use std::path::PathBuf;\n  1788:     ///\n  1789:     /// let p = PathBuf::from(\"/the/head\");\n  1790:     /// let os_str = p.into_os_string();\n  1791:     /// ```\n  1792:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1793:     #[must_use = \"`self` will be dropped if the result is not used\"]\n  1794:     #[inline]",
    "nanvix_source": "  1768:     /// path.push(\"bar\");\n  1769:     /// assert_eq!(path, Path::new(\"/foo/bar\"));\n  1770:     ///\n  1771:     /// // OsString's `push` does not add a separator.\n  1772:     /// path.as_mut_os_string().push(\"baz\");\n  1773:     /// assert_eq!(path, Path::new(\"/foo/barbaz\"));\n  1774:     /// ```\n  1775:     #[stable(feature = \"path_as_mut_os_str\", since = \"1.70.0\")]\n  1776:     #[must_use]\n  1777:     #[inline]\n  1778:     pub fn as_mut_os_string(&mut self) -> &mut OsString {\n  1779:         &mut self.inner\n  1780:     }\n  1781: \n  1782:     /// Consumes the `PathBuf`, yielding its internal [`OsString`] storage.\n  1783:     ///\n  1784:     /// # Examples\n  1785:     ///\n  1786:     /// ```\n  1787:     /// use std::path::PathBuf;\n  1788:     ///",
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
