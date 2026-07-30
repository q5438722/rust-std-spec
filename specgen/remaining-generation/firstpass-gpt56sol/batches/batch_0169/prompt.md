For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "alloc::collections::BinaryHeap::capacity",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "capacity",
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
                      "generic": "A"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
    "verification_source": "  1149:     }\n  1150: \n  1151:     /// Returns the number of elements the binary heap can hold without reallocating.\n  1152:     ///\n  1153:     /// # Examples\n  1154:     ///\n  1155:     /// Basic usage:\n  1156:     ///\n  1157:     /// ```\n  1158:     /// use std::collections::BinaryHeap;\n  1159:     /// let mut heap = BinaryHeap::with_capacity(100);\n  1160:     /// assert!(heap.capacity() >= 100);\n  1161:     /// heap.push(4);\n  1162:     /// ```\n  1163:     #[must_use]\n  1164:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1165:     pub fn capacity(&self) -> usize {\n  1166:         self.data.capacity()\n  1167:     }\n  1168: \n  1169:     /// Reserves the minimum capacity for at least `additional` elements more than\n  1170:     /// the current length. Unlike [`reserve`], this will not\n  1171:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1172:     /// After calling `reserve_exact`, capacity will be greater than or equal to\n  1173:     /// `self.len() + additional`. Does nothing if the capacity is already\n  1174:     /// sufficient.\n  1175:     ///\n  1176:     /// [`reserve`]: BinaryHeap::reserve\n  1177:     ///\n  1178:     /// # Panics\n  1179:     ///\n  1180:     /// Panics if the new capacity overflows [`usize`].\n  1181:     ///",
    "nanvix_source": "  1155:     /// Basic usage:\n  1156:     ///\n  1157:     /// ```\n  1158:     /// use std::collections::BinaryHeap;\n  1159:     /// let mut heap = BinaryHeap::with_capacity(100);\n  1160:     /// assert!(heap.capacity() >= 100);\n  1161:     /// heap.push(4);\n  1162:     /// ```\n  1163:     #[must_use]\n  1164:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1165:     pub fn capacity(&self) -> usize {\n  1166:         self.data.capacity()\n  1167:     }\n  1168: \n  1169:     /// Reserves the minimum capacity for at least `additional` elements more than\n  1170:     /// the current length. Unlike [`reserve`], this will not\n  1171:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1172:     /// After calling `reserve_exact`, capacity will be greater than or equal to\n  1173:     /// `self.len() + additional`. Does nothing if the capacity is already\n  1174:     /// sufficient.\n  1175:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "reserve",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1206:     /// # Panics\n  1207:     ///\n  1208:     /// Panics if the new capacity overflows [`usize`].\n  1209:     ///\n  1210:     /// # Examples\n  1211:     ///\n  1212:     /// Basic usage:\n  1213:     ///\n  1214:     /// ```\n  1215:     /// use std::collections::BinaryHeap;\n  1216:     /// let mut heap = BinaryHeap::new();\n  1217:     /// heap.reserve(100);\n  1218:     /// assert!(heap.capacity() >= 100);\n  1219:     /// heap.push(4);\n  1220:     /// ```\n  1221:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1222:     pub fn reserve(&mut self, additional: usize) {\n  1223:         self.data.reserve(additional);\n  1224:     }\n  1225: \n  1226:     /// Tries to reserve the minimum capacity for at least `additional` elements\n  1227:     /// more than the current length. Unlike [`try_reserve`], this will not\n  1228:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1229:     /// After calling `try_reserve_exact`, capacity will be greater than or\n  1230:     /// equal to `self.len() + additional` if it returns `Ok(())`.\n  1231:     /// Does nothing if the capacity is already sufficient.\n  1232:     ///\n  1233:     /// Note that the allocator may give the collection more space than it\n  1234:     /// requests. Therefore, capacity can not be relied upon to be precisely\n  1235:     /// minimal. Prefer [`try_reserve`] if future insertions are expected.\n  1236:     ///\n  1237:     /// [`try_reserve`]: BinaryHeap::try_reserve\n  1238:     ///",
    "nanvix_source": "  1212:     /// Basic usage:\n  1213:     ///\n  1214:     /// ```\n  1215:     /// use std::collections::BinaryHeap;\n  1216:     /// let mut heap = BinaryHeap::new();\n  1217:     /// heap.reserve(100);\n  1218:     /// assert!(heap.capacity() >= 100);\n  1219:     /// heap.push(4);\n  1220:     /// ```\n  1221:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1222:     pub fn reserve(&mut self, additional: usize) {\n  1223:         self.data.reserve(additional);\n  1224:     }\n  1225: \n  1226:     /// Tries to reserve the minimum capacity for at least `additional` elements\n  1227:     /// more than the current length. Unlike [`try_reserve`], this will not\n  1228:     /// deliberately over-allocate to speculatively avoid frequent allocations.\n  1229:     /// After calling `try_reserve_exact`, capacity will be greater than or\n  1230:     /// equal to `self.len() + additional` if it returns `Ok(())`.\n  1231:     /// Does nothing if the capacity is already sufficient.\n  1232:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::reserve_exact",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "reserve_exact",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "additional",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1180:     /// Panics if the new capacity overflows [`usize`].\n  1181:     ///\n  1182:     /// # Examples\n  1183:     ///\n  1184:     /// Basic usage:\n  1185:     ///\n  1186:     /// ```\n  1187:     /// use std::collections::BinaryHeap;\n  1188:     /// let mut heap = BinaryHeap::new();\n  1189:     /// heap.reserve_exact(100);\n  1190:     /// assert!(heap.capacity() >= 100);\n  1191:     /// heap.push(4);\n  1192:     /// ```\n  1193:     ///\n  1194:     /// [`reserve`]: BinaryHeap::reserve\n  1195:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1196:     pub fn reserve_exact(&mut self, additional: usize) {\n  1197:         self.data.reserve_exact(additional);\n  1198:     }\n  1199: \n  1200:     /// Reserves capacity for at least `additional` elements more than the\n  1201:     /// current length. The allocator may reserve more space to speculatively\n  1202:     /// avoid frequent allocations. After calling `reserve`,\n  1203:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1204:     /// Does nothing if capacity is already sufficient.\n  1205:     ///\n  1206:     /// # Panics\n  1207:     ///\n  1208:     /// Panics if the new capacity overflows [`usize`].\n  1209:     ///\n  1210:     /// # Examples\n  1211:     ///\n  1212:     /// Basic usage:",
    "nanvix_source": "  1186:     /// ```\n  1187:     /// use std::collections::BinaryHeap;\n  1188:     /// let mut heap = BinaryHeap::new();\n  1189:     /// heap.reserve_exact(100);\n  1190:     /// assert!(heap.capacity() >= 100);\n  1191:     /// heap.push(4);\n  1192:     /// ```\n  1193:     ///\n  1194:     /// [`reserve`]: BinaryHeap::reserve\n  1195:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1196:     pub fn reserve_exact(&mut self, additional: usize) {\n  1197:         self.data.reserve_exact(additional);\n  1198:     }\n  1199: \n  1200:     /// Reserves capacity for at least `additional` elements more than the\n  1201:     /// current length. The allocator may reserve more space to speculatively\n  1202:     /// avoid frequent allocations. After calling `reserve`,\n  1203:     /// capacity will be greater than or equal to `self.len() + additional`.\n  1204:     /// Does nothing if capacity is already sufficient.\n  1205:     ///\n  1206:     /// # Panics",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::shrink_to",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "min_capacity",
            {
              "primitive": "usize"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "  1326:     /// and the supplied value.\n  1327:     ///\n  1328:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1329:     ///\n  1330:     /// # Examples\n  1331:     ///\n  1332:     /// ```\n  1333:     /// use std::collections::BinaryHeap;\n  1334:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1335:     ///\n  1336:     /// assert!(heap.capacity() >= 100);\n  1337:     /// heap.shrink_to(10);\n  1338:     /// assert!(heap.capacity() >= 10);\n  1339:     /// ```\n  1340:     #[inline]\n  1341:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1342:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1343:         self.data.shrink_to(min_capacity)\n  1344:     }\n  1345: \n  1346:     /// Returns a slice of all values in the underlying vector, in arbitrary\n  1347:     /// order.\n  1348:     ///\n  1349:     /// # Examples\n  1350:     ///\n  1351:     /// Basic usage:\n  1352:     ///\n  1353:     /// ```\n  1354:     /// use std::collections::BinaryHeap;\n  1355:     /// use std::io::{self, Write};\n  1356:     ///\n  1357:     /// let heap = BinaryHeap::from([1, 2, 3, 4, 5, 6, 7]);\n  1358:     ///",
    "nanvix_source": "  1332:     /// ```\n  1333:     /// use std::collections::BinaryHeap;\n  1334:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1335:     ///\n  1336:     /// assert!(heap.capacity() >= 100);\n  1337:     /// heap.shrink_to(10);\n  1338:     /// assert!(heap.capacity() >= 10);\n  1339:     /// ```\n  1340:     #[inline]\n  1341:     #[stable(feature = \"shrink_to\", since = \"1.56.0\")]\n  1342:     pub fn shrink_to(&mut self, min_capacity: usize) {\n  1343:         self.data.shrink_to(min_capacity)\n  1344:     }\n  1345: \n  1346:     /// Returns a slice of all values in the underlying vector, in arbitrary\n  1347:     /// order.\n  1348:     ///\n  1349:     /// # Examples\n  1350:     ///\n  1351:     /// Basic usage:\n  1352:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::shrink_to_fit",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "where_predicates": []
      },
      "header": {
        "abi": "Rust",
        "is_async": false,
        "is_const": false,
        "is_unsafe": false
      },
      "name": "shrink_to_fit",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
    "verification_source": "  1303: \n  1304:     /// Discards as much additional capacity as possible.\n  1305:     ///\n  1306:     /// # Examples\n  1307:     ///\n  1308:     /// Basic usage:\n  1309:     ///\n  1310:     /// ```\n  1311:     /// use std::collections::BinaryHeap;\n  1312:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1313:     ///\n  1314:     /// assert!(heap.capacity() >= 100);\n  1315:     /// heap.shrink_to_fit();\n  1316:     /// assert!(heap.capacity() == 0);\n  1317:     /// ```\n  1318:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1319:     pub fn shrink_to_fit(&mut self) {\n  1320:         self.data.shrink_to_fit();\n  1321:     }\n  1322: \n  1323:     /// Discards capacity with a lower bound.\n  1324:     ///\n  1325:     /// The capacity will remain at least as large as both the length\n  1326:     /// and the supplied value.\n  1327:     ///\n  1328:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1329:     ///\n  1330:     /// # Examples\n  1331:     ///\n  1332:     /// ```\n  1333:     /// use std::collections::BinaryHeap;\n  1334:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1335:     ///",
    "nanvix_source": "  1309:     ///\n  1310:     /// ```\n  1311:     /// use std::collections::BinaryHeap;\n  1312:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1313:     ///\n  1314:     /// assert!(heap.capacity() >= 100);\n  1315:     /// heap.shrink_to_fit();\n  1316:     /// assert!(heap.capacity() == 0);\n  1317:     /// ```\n  1318:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n  1319:     pub fn shrink_to_fit(&mut self) {\n  1320:         self.data.shrink_to_fit();\n  1321:     }\n  1322: \n  1323:     /// Discards capacity with a lower bound.\n  1324:     ///\n  1325:     /// The capacity will remain at least as large as both the length\n  1326:     /// and the supplied value.\n  1327:     ///\n  1328:     /// If the current capacity is less than the lower limit, this is a no-op.\n  1329:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "alloc::collections::BinaryHeap::try_reserve",
    "generation_group": "representation_or_allocator",
    "classification": "representation_or_allocator",
    "classification_reasons": [
      "representation_or_allocator_state_not_in_public_view"
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
        "is_const": false,
        "is_unsafe": false
      },
      "name": "try_reserve",
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
            "id": 979,
            "path": "BinaryHeap"
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
        "impl_id": "alloc:1018",
        "kind": "inherent_impl",
        "resolved_owner_id": "alloc:979",
        "resolved_owner_path": [
          "alloc",
          "collections",
          "binary_heap",
          "BinaryHeap"
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
            "additional",
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
                      "tuple": []
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 1006,
                        "path": "TryReserveError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 46,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "  1284:     /// use std::collections::TryReserveError;\n  1285:     ///\n  1286:     /// fn find_max_slow(data: &[u32]) -> Result<Option<u32>, TryReserveError> {\n  1287:     ///     let mut heap = BinaryHeap::new();\n  1288:     ///\n  1289:     ///     // Pre-reserve the memory, exiting if we can't\n  1290:     ///     heap.try_reserve(data.len())?;\n  1291:     ///\n  1292:     ///     // Now we know this can't OOM in the middle of our complex work\n  1293:     ///     heap.extend(data.iter());\n  1294:     ///\n  1295:     ///     Ok(heap.pop())\n  1296:     /// }\n  1297:     /// # find_max_slow(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1298:     /// ```\n  1299:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1300:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1301:         self.data.try_reserve(additional)\n  1302:     }\n  1303: \n  1304:     /// Discards as much additional capacity as possible.\n  1305:     ///\n  1306:     /// # Examples\n  1307:     ///\n  1308:     /// Basic usage:\n  1309:     ///\n  1310:     /// ```\n  1311:     /// use std::collections::BinaryHeap;\n  1312:     /// let mut heap: BinaryHeap<i32> = BinaryHeap::with_capacity(100);\n  1313:     ///\n  1314:     /// assert!(heap.capacity() >= 100);\n  1315:     /// heap.shrink_to_fit();\n  1316:     /// assert!(heap.capacity() == 0);",
    "nanvix_source": "  1290:     ///     heap.try_reserve(data.len())?;\n  1291:     ///\n  1292:     ///     // Now we know this can't OOM in the middle of our complex work\n  1293:     ///     heap.extend(data.iter());\n  1294:     ///\n  1295:     ///     Ok(heap.pop())\n  1296:     /// }\n  1297:     /// # find_max_slow(&[1, 2, 3]).expect(\"why is the test harness OOMing on 12 bytes?\");\n  1298:     /// ```\n  1299:     #[stable(feature = \"try_reserve_2\", since = \"1.63.0\")]\n  1300:     pub fn try_reserve(&mut self, additional: usize) -> Result<(), TryReserveError> {\n  1301:         self.data.try_reserve(additional)\n  1302:     }\n  1303: \n  1304:     /// Discards as much additional capacity as possible.\n  1305:     ///\n  1306:     /// # Examples\n  1307:     ///\n  1308:     /// Basic usage:\n  1309:     ///\n  1310:     /// ```",
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
