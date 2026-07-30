For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "core::net::SocketAddr::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ip",
            {
              "resolved_path": {
                "args": null,
                "id": 9943,
                "path": "IpAddr"
              }
            }
          ],
          [
            "port",
            {
              "primitive": "u16"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9958,
            "path": "SocketAddr"
          }
        }
      }
    },
    "verification_source": "   156:     ///\n   157:     /// [IP address]: IpAddr\n   158:     ///\n   159:     /// # Examples\n   160:     ///\n   161:     /// ```\n   162:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   163:     ///\n   164:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   165:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   166:     /// assert_eq!(socket.port(), 8080);\n   167:     /// ```\n   168:     #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n   169:     #[must_use]\n   170:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   171:     #[inline]\n   172:     pub const fn new(ip: IpAddr, port: u16) -> SocketAddr {\n   173:         match ip {\n   174:             IpAddr::V4(a) => SocketAddr::V4(SocketAddrV4::new(a, port)),\n   175:             IpAddr::V6(a) => SocketAddr::V6(SocketAddrV6::new(a, port, 0, 0)),\n   176:         }\n   177:     }\n   178: \n   179:     /// Returns the IP address associated with this socket address.\n   180:     ///\n   181:     /// # Examples\n   182:     ///\n   183:     /// ```\n   184:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   185:     ///\n   186:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   187:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   188:     /// ```",
    "nanvix_source": "   162:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   163:     ///\n   164:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   165:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)));\n   166:     /// assert_eq!(socket.port(), 8080);\n   167:     /// ```\n   168:     #[stable(feature = \"ip_addr\", since = \"1.7.0\")]\n   169:     #[must_use]\n   170:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   171:     #[inline]\n   172:     pub const fn new(ip: IpAddr, port: u16) -> SocketAddr {\n   173:         match ip {\n   174:             IpAddr::V4(a) => SocketAddr::V4(SocketAddrV4::new(a, port)),\n   175:             IpAddr::V6(a) => SocketAddr::V6(SocketAddrV6::new(a, port, 0, 0)),\n   176:         }\n   177:     }\n   178: \n   179:     /// Returns the IP address associated with this socket address.\n   180:     ///\n   181:     /// # Examples\n   182:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::port",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
        "is_unsafe": false
      },
      "name": "port",
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
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
          "primitive": "u16"
        }
      }
    },
    "verification_source": "   221:     }\n   222: \n   223:     /// Returns the port number associated with this socket address.\n   224:     ///\n   225:     /// # Examples\n   226:     ///\n   227:     /// ```\n   228:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   229:     ///\n   230:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   231:     /// assert_eq!(socket.port(), 8080);\n   232:     /// ```\n   233:     #[must_use]\n   234:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   235:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   236:     #[inline]\n   237:     pub const fn port(&self) -> u16 {\n   238:         match *self {\n   239:             SocketAddr::V4(ref a) => a.port(),\n   240:             SocketAddr::V6(ref a) => a.port(),\n   241:         }\n   242:     }\n   243: \n   244:     /// Changes the port number associated with this socket address.\n   245:     ///\n   246:     /// # Examples\n   247:     ///\n   248:     /// ```\n   249:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   250:     ///\n   251:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   252:     /// socket.set_port(1025);\n   253:     /// assert_eq!(socket.port(), 1025);",
    "nanvix_source": "   227:     /// ```\n   228:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   229:     ///\n   230:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   231:     /// assert_eq!(socket.port(), 8080);\n   232:     /// ```\n   233:     #[must_use]\n   234:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   235:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   236:     #[inline]\n   237:     pub const fn port(&self) -> u16 {\n   238:         match *self {\n   239:             SocketAddr::V4(ref a) => a.port(),\n   240:             SocketAddr::V6(ref a) => a.port(),\n   241:         }\n   242:     }\n   243: \n   244:     /// Changes the port number associated with this socket address.\n   245:     ///\n   246:     /// # Examples\n   247:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::set_ip",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_ip",
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
            "args": null,
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
            "new_ip",
            {
              "resolved_path": {
                "args": null,
                "id": 9943,
                "path": "IpAddr"
              }
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   198:     }\n   199: \n   200:     /// Changes the IP address associated with this socket address.\n   201:     ///\n   202:     /// # Examples\n   203:     ///\n   204:     /// ```\n   205:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   206:     ///\n   207:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   208:     /// socket.set_ip(IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));\n   209:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));\n   210:     /// ```\n   211:     #[inline]\n   212:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   213:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   214:     pub const fn set_ip(&mut self, new_ip: IpAddr) {\n   215:         // `match (*self, new_ip)` would have us mutate a copy of self only to throw it away.\n   216:         match (self, new_ip) {\n   217:             (&mut SocketAddr::V4(ref mut a), IpAddr::V4(new_ip)) => a.set_ip(new_ip),\n   218:             (&mut SocketAddr::V6(ref mut a), IpAddr::V6(new_ip)) => a.set_ip(new_ip),\n   219:             (self_, new_ip) => *self_ = Self::new(new_ip, self_.port()),\n   220:         }\n   221:     }\n   222: \n   223:     /// Returns the port number associated with this socket address.\n   224:     ///\n   225:     /// # Examples\n   226:     ///\n   227:     /// ```\n   228:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   229:     ///\n   230:     /// let socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);",
    "nanvix_source": "   204:     /// ```\n   205:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   206:     ///\n   207:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   208:     /// socket.set_ip(IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));\n   209:     /// assert_eq!(socket.ip(), IpAddr::V4(Ipv4Addr::new(10, 10, 0, 1)));\n   210:     /// ```\n   211:     #[inline]\n   212:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   213:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   214:     pub const fn set_ip(&mut self, new_ip: IpAddr) {\n   215:         // `match (*self, new_ip)` would have us mutate a copy of self only to throw it away.\n   216:         match (self, new_ip) {\n   217:             (&mut SocketAddr::V4(ref mut a), IpAddr::V4(new_ip)) => a.set_ip(new_ip),\n   218:             (&mut SocketAddr::V6(ref mut a), IpAddr::V6(new_ip)) => a.set_ip(new_ip),\n   219:             (self_, new_ip) => *self_ = Self::new(new_ip, self_.port()),\n   220:         }\n   221:     }\n   222: \n   223:     /// Returns the port number associated with this socket address.\n   224:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddr::set_port",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "set_port",
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
            "args": null,
            "id": 9958,
            "path": "SocketAddr"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27917",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9958",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddr"
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
            "new_port",
            {
              "primitive": "u16"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": null
      }
    },
    "verification_source": "   242:     }\n   243: \n   244:     /// Changes the port number associated with this socket address.\n   245:     ///\n   246:     /// # Examples\n   247:     ///\n   248:     /// ```\n   249:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   250:     ///\n   251:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   252:     /// socket.set_port(1025);\n   253:     /// assert_eq!(socket.port(), 1025);\n   254:     /// ```\n   255:     #[inline]\n   256:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   257:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   258:     pub const fn set_port(&mut self, new_port: u16) {\n   259:         match *self {\n   260:             SocketAddr::V4(ref mut a) => a.set_port(new_port),\n   261:             SocketAddr::V6(ref mut a) => a.set_port(new_port),\n   262:         }\n   263:     }\n   264: \n   265:     /// Returns [`true`] if the [IP address] in this `SocketAddr` is an\n   266:     /// [`IPv4` address], and [`false`] otherwise.\n   267:     ///\n   268:     /// [IP address]: IpAddr\n   269:     /// [`IPv4` address]: IpAddr::V4\n   270:     ///\n   271:     /// # Examples\n   272:     ///\n   273:     /// ```\n   274:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};",
    "nanvix_source": "   248:     /// ```\n   249:     /// use std::net::{IpAddr, Ipv4Addr, SocketAddr};\n   250:     ///\n   251:     /// let mut socket = SocketAddr::new(IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)), 8080);\n   252:     /// socket.set_port(1025);\n   253:     /// assert_eq!(socket.port(), 1025);\n   254:     /// ```\n   255:     #[inline]\n   256:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]\n   257:     #[rustc_const_stable(feature = \"const_sockaddr_setters\", since = \"1.87.0\")]\n   258:     pub const fn set_port(&mut self, new_port: u16) {\n   259:         match *self {\n   260:             SocketAddr::V4(ref mut a) => a.set_port(new_port),\n   261:             SocketAddr::V6(ref mut a) => a.set_port(new_port),\n   262:         }\n   263:     }\n   264: \n   265:     /// Returns [`true`] if the [IP address] in this `SocketAddr` is an\n   266:     /// [`IPv4` address], and [`false`] otherwise.\n   267:     ///\n   268:     /// [IP address]: IpAddr",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV4::ip",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
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
        "is_const": true,
        "is_unsafe": false
      },
      "name": "ip",
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
            "args": null,
            "id": 9961,
            "path": "SocketAddrV4"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27946",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9961",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV4"
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
              "resolved_path": {
                "args": null,
                "id": 9946,
                "path": "Ipv4Addr"
              }
            }
          }
        }
      }
    },
    "verification_source": "   330:     }\n   331: \n   332:     /// Returns the IP address associated with this socket address.\n   333:     ///\n   334:     /// # Examples\n   335:     ///\n   336:     /// ```\n   337:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   338:     ///\n   339:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   340:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(127, 0, 0, 1));\n   341:     /// ```\n   342:     #[must_use]\n   343:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   344:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   345:     #[inline]\n   346:     pub const fn ip(&self) -> &Ipv4Addr {\n   347:         &self.ip\n   348:     }\n   349: \n   350:     /// Changes the IP address associated with this socket address.\n   351:     ///\n   352:     /// # Examples\n   353:     ///\n   354:     /// ```\n   355:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   356:     ///\n   357:     /// let mut socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   358:     /// socket.set_ip(Ipv4Addr::new(192, 168, 0, 1));\n   359:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(192, 168, 0, 1));\n   360:     /// ```\n   361:     #[inline]\n   362:     #[stable(feature = \"sockaddr_setters\", since = \"1.9.0\")]",
    "nanvix_source": "   336:     /// ```\n   337:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   338:     ///\n   339:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   340:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(127, 0, 0, 1));\n   341:     /// ```\n   342:     #[must_use]\n   343:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   344:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   345:     #[inline]\n   346:     pub const fn ip(&self) -> &Ipv4Addr {\n   347:         &self.ip\n   348:     }\n   349: \n   350:     /// Changes the IP address associated with this socket address.\n   351:     ///\n   352:     /// # Examples\n   353:     ///\n   354:     /// ```\n   355:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   356:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "core::net::SocketAddrV4::new",
    "generation_group": "needs_new_vstd_abstraction",
    "classification": "needs_new_vstd_abstraction",
    "classification_reasons": [
      "no_existing_contract_for_owner_or_module"
    ],
    "category": "other",
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
            "id": 9961,
            "path": "SocketAddrV4"
          }
        },
        "generics": {
          "params": [],
          "where_predicates": []
        },
        "impl_id": "core:27946",
        "kind": "inherent_impl",
        "resolved_owner_id": "core:9961",
        "resolved_owner_path": [
          "core",
          "net",
          "socket_addr",
          "SocketAddrV4"
        ],
        "trait": null
      },
      "signature": {
        "inputs": [
          [
            "ip",
            {
              "resolved_path": {
                "args": null,
                "id": 9946,
                "path": "Ipv4Addr"
              }
            }
          ],
          [
            "port",
            {
              "primitive": "u16"
            }
          ]
        ],
        "is_c_variadic": false,
        "output": {
          "resolved_path": {
            "args": null,
            "id": 9961,
            "path": "SocketAddrV4"
          }
        }
      }
    },
    "verification_source": "   312: impl SocketAddrV4 {\n   313:     /// Creates a new socket address from an [`IPv4` address] and a port number.\n   314:     ///\n   315:     /// [`IPv4` address]: Ipv4Addr\n   316:     ///\n   317:     /// # Examples\n   318:     ///\n   319:     /// ```\n   320:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   321:     ///\n   322:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   323:     /// ```\n   324:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   325:     #[must_use]\n   326:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   327:     #[inline]\n   328:     pub const fn new(ip: Ipv4Addr, port: u16) -> SocketAddrV4 {\n   329:         SocketAddrV4 { ip, port }\n   330:     }\n   331: \n   332:     /// Returns the IP address associated with this socket address.\n   333:     ///\n   334:     /// # Examples\n   335:     ///\n   336:     /// ```\n   337:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   338:     ///\n   339:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   340:     /// assert_eq!(socket.ip(), &Ipv4Addr::new(127, 0, 0, 1));\n   341:     /// ```\n   342:     #[must_use]\n   343:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   344:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]",
    "nanvix_source": "   318:     ///\n   319:     /// ```\n   320:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   321:     ///\n   322:     /// let socket = SocketAddrV4::new(Ipv4Addr::new(127, 0, 0, 1), 8080);\n   323:     /// ```\n   324:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   325:     #[must_use]\n   326:     #[rustc_const_stable(feature = \"const_socketaddr\", since = \"1.69.0\")]\n   327:     #[inline]\n   328:     pub const fn new(ip: Ipv4Addr, port: u16) -> SocketAddrV4 {\n   329:         SocketAddrV4 { ip, port }\n   330:     }\n   331: \n   332:     /// Returns the IP address associated with this socket address.\n   333:     ///\n   334:     /// # Examples\n   335:     ///\n   336:     /// ```\n   337:     /// use std::net::{SocketAddrV4, Ipv4Addr};\n   338:     ///",
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
