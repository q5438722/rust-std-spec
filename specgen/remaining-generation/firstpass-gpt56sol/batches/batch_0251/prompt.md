For each Rust standard-library API below, decide whether a useful trusted Verus
contract can be proposed in the current vstd vocabulary.

Targets:
```json
[
  {
    "target": "std::sync::mpsc::Receiver::recv_timeout",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "recv_timeout",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7865,
            "path": "Receiver"
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
        "impl_id": "std:7876",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7865",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Receiver"
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
            "timeout",
            {
              "resolved_path": {
                "args": null,
                "id": 513,
                "path": "Duration"
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
                      "generic": "T"
                    }
                  },
                  {
                    "type": {
                      "resolved_path": {
                        "args": null,
                        "id": 7659,
                        "path": "RecvTimeoutError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   915:     /// use std::time::Duration;\n   916:     /// use std::sync::mpsc;\n   917:     ///\n   918:     /// let (send, recv) = mpsc::channel();\n   919:     ///\n   920:     /// thread::spawn(move || {\n   921:     ///     thread::sleep(Duration::from_millis(800));\n   922:     ///     send.send('a').unwrap();\n   923:     /// });\n   924:     ///\n   925:     /// assert_eq!(\n   926:     ///     recv.recv_timeout(Duration::from_millis(400)),\n   927:     ///     Err(mpsc::RecvTimeoutError::Timeout)\n   928:     /// );\n   929:     /// ```\n   930:     #[stable(feature = \"mpsc_recv_timeout\", since = \"1.12.0\")]\n   931:     pub fn recv_timeout(&self, timeout: Duration) -> Result<T, RecvTimeoutError> {\n   932:         self.inner.recv_timeout(timeout)\n   933:     }\n   934: \n   935:     /// Attempts to wait for a value on this receiver, returning an error if the\n   936:     /// corresponding channel has hung up, or if `deadline` is reached.\n   937:     ///\n   938:     /// This function will always block the current thread if there is no data\n   939:     /// available and it's possible for more data to be sent. Once a message is\n   940:     /// sent to the corresponding [`Sender`] (or [`SyncSender`]), then this\n   941:     /// receiver will wake up and return that message.\n   942:     ///\n   943:     /// If the corresponding [`Sender`] has disconnected, or it disconnects while\n   944:     /// this call is blocking, this call will wake up and return [`Err`] to\n   945:     /// indicate that no more messages can ever be received on this channel.\n   946:     /// However, since channels are buffered, messages sent before the disconnect\n   947:     /// will still be properly received.",
    "nanvix_source": "   939:     ///     thread::sleep(Duration::from_millis(800));\n   940:     ///     send.send('a').unwrap();\n   941:     /// });\n   942:     ///\n   943:     /// assert_eq!(\n   944:     ///     recv.recv_timeout(Duration::from_millis(400)),\n   945:     ///     Err(mpsc::RecvTimeoutError::Timeout)\n   946:     /// );\n   947:     /// ```\n   948:     #[stable(feature = \"mpsc_recv_timeout\", since = \"1.12.0\")]\n   949:     pub fn recv_timeout(&self, timeout: Duration) -> Result<T, RecvTimeoutError> {\n   950:         self.inner.recv_timeout(timeout)\n   951:     }\n   952: \n   953:     /// Attempts to wait for a value on this receiver, returning an error if the\n   954:     /// corresponding channel has hung up, or if `deadline` is reached.\n   955:     ///\n   956:     /// This function will always block the current thread if there is no data\n   957:     /// available and it's possible for more data to be sent. Once a message is\n   958:     /// sent to the corresponding [`Sender`] (or [`SyncSender`]), then this\n   959:     /// receiver will wake up and return that message.",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::Receiver::try_iter",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "try_iter",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7865,
            "path": "Receiver"
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
        "impl_id": "std:7876",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7865",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Receiver"
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
            "args": {
              "angle_bracketed": {
                "args": [
                  {
                    "lifetime": "'_"
                  },
                  {
                    "type": {
                      "generic": "T"
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 7874,
            "path": "TryIter"
          }
        }
      }
    },
    "verification_source": "  1045:     ///     sender.send(3).unwrap();\n  1046:     /// });\n  1047:     ///\n  1048:     /// // nothing is in the buffer yet\n  1049:     /// assert!(receiver.try_iter().next().is_none());\n  1050:     ///\n  1051:     /// // block for two seconds\n  1052:     /// thread::sleep(Duration::from_secs(2));\n  1053:     ///\n  1054:     /// let mut iter = receiver.try_iter();\n  1055:     /// assert_eq!(iter.next(), Some(1));\n  1056:     /// assert_eq!(iter.next(), Some(2));\n  1057:     /// assert_eq!(iter.next(), Some(3));\n  1058:     /// assert_eq!(iter.next(), None);\n  1059:     /// ```\n  1060:     #[stable(feature = \"receiver_try_iter\", since = \"1.15.0\")]\n  1061:     pub fn try_iter(&self) -> TryIter<'_, T> {\n  1062:         TryIter { rx: self }\n  1063:     }\n  1064: \n  1065:     /// Returns `true` if the channel is disconnected.\n  1066:     ///\n  1067:     /// Note that a return value of `false` does not guarantee the channel will\n  1068:     /// remain connected. The channel may be disconnected immediately after this method\n  1069:     /// returns, so a subsequent [`Receiver::recv`] may still fail with [`RecvError`].\n  1070:     ///\n  1071:     /// # Examples\n  1072:     ///\n  1073:     /// ```\n  1074:     /// #![feature(mpsc_is_disconnected)]\n  1075:     ///\n  1076:     /// use std::sync::mpsc::channel;\n  1077:     ///",
    "nanvix_source": "  1069:     /// // block for two seconds\n  1070:     /// thread::sleep(Duration::from_secs(2));\n  1071:     ///\n  1072:     /// let mut iter = receiver.try_iter();\n  1073:     /// assert_eq!(iter.next(), Some(1));\n  1074:     /// assert_eq!(iter.next(), Some(2));\n  1075:     /// assert_eq!(iter.next(), Some(3));\n  1076:     /// assert_eq!(iter.next(), None);\n  1077:     /// ```\n  1078:     #[stable(feature = \"receiver_try_iter\", since = \"1.15.0\")]\n  1079:     pub fn try_iter(&self) -> TryIter<'_, T> {\n  1080:         TryIter { rx: self }\n  1081:     }\n  1082: \n  1083:     /// Returns `true` if the channel is disconnected.\n  1084:     ///\n  1085:     /// Note that a return value of `false` does not guarantee the channel will\n  1086:     /// remain connected. The channel may be disconnected immediately after this method\n  1087:     /// returns, so a subsequent [`Receiver::recv`] may still fail with [`RecvError`].\n  1088:     ///\n  1089:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::Receiver::try_recv",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "try_recv",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7865,
            "path": "Receiver"
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
        "impl_id": "std:7876",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7865",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Receiver"
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
                      "resolved_path": {
                        "args": null,
                        "id": 7663,
                        "path": "TryRecvError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   796:     ///\n   797:     /// Compared with [`recv`], this function has two failure cases instead of one\n   798:     /// (one for disconnection, one for an empty buffer).\n   799:     ///\n   800:     /// [`recv`]: Self::recv\n   801:     ///\n   802:     /// # Examples\n   803:     ///\n   804:     /// ```rust\n   805:     /// use std::sync::mpsc::{Receiver, channel};\n   806:     ///\n   807:     /// let (_, receiver): (_, Receiver<i32>) = channel();\n   808:     ///\n   809:     /// assert!(receiver.try_recv().is_err());\n   810:     /// ```\n   811:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   812:     pub fn try_recv(&self) -> Result<T, TryRecvError> {\n   813:         self.inner.try_recv()\n   814:     }\n   815: \n   816:     /// Attempts to wait for a value on this receiver, returning an error if the\n   817:     /// corresponding channel has hung up.\n   818:     ///\n   819:     /// This function will always block the current thread if there is no data\n   820:     /// available and it's possible for more data to be sent (at least one sender\n   821:     /// still exists). Once a message is sent to the corresponding [`Sender`]\n   822:     /// (or [`SyncSender`]), this receiver will wake up and return that\n   823:     /// message.\n   824:     ///\n   825:     /// If the corresponding [`Sender`] has disconnected, or it disconnects while\n   826:     /// this call is blocking, this call will wake up and return [`Err`] to\n   827:     /// indicate that no more messages can ever be received on this channel.\n   828:     /// However, since channels are buffered, messages sent before the disconnect",
    "nanvix_source": "   820:     /// # Examples\n   821:     ///\n   822:     /// ```rust\n   823:     /// use std::sync::mpsc::{Receiver, channel};\n   824:     ///\n   825:     /// let (_, receiver): (_, Receiver<i32>) = channel();\n   826:     ///\n   827:     /// assert!(receiver.try_recv().is_err());\n   828:     /// ```\n   829:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   830:     pub fn try_recv(&self) -> Result<T, TryRecvError> {\n   831:         self.inner.try_recv()\n   832:     }\n   833: \n   834:     /// Attempts to wait for a value on this receiver, returning an error if the\n   835:     /// corresponding channel has hung up.\n   836:     ///\n   837:     /// This function will always block the current thread if there is no data\n   838:     /// available and it's possible for more data to be sent (at least one sender\n   839:     /// still exists). Once a message is sent to the corresponding [`Sender`]\n   840:     /// (or [`SyncSender`]), this receiver will wake up and return that",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::Sender::send",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "send",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7867,
            "path": "Sender"
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
        "impl_id": "std:7968",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7867",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "Sender"
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
            "t",
            {
              "generic": "T"
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
                        "id": 7661,
                        "path": "SendError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   591:     ///\n   592:     /// # Examples\n   593:     ///\n   594:     /// ```\n   595:     /// use std::sync::mpsc::channel;\n   596:     ///\n   597:     /// let (tx, rx) = channel();\n   598:     ///\n   599:     /// // This send is always successful\n   600:     /// tx.send(1).unwrap();\n   601:     ///\n   602:     /// // This send will fail because the receiver is gone\n   603:     /// drop(rx);\n   604:     /// assert_eq!(tx.send(1).unwrap_err().0, 1);\n   605:     /// ```\n   606:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   607:     pub fn send(&self, t: T) -> Result<(), SendError<T>> {\n   608:         self.inner.send(t)\n   609:     }\n   610: \n   611:     /// Returns `true` if the channel is disconnected.\n   612:     ///\n   613:     /// Note that a return value of `false` does not guarantee the channel will\n   614:     /// remain connected. The channel may be disconnected immediately after this method\n   615:     /// returns, so a subsequent [`Sender::send`] may still fail with [`SendError`].\n   616:     ///\n   617:     /// # Examples\n   618:     ///\n   619:     /// ```\n   620:     /// #![feature(mpsc_is_disconnected)]\n   621:     ///\n   622:     /// use std::sync::mpsc::channel;\n   623:     ///",
    "nanvix_source": "   607:     /// let (tx, rx) = channel();\n   608:     ///\n   609:     /// // This send is always successful\n   610:     /// tx.send(1).unwrap();\n   611:     ///\n   612:     /// // This send will fail because the receiver is gone\n   613:     /// drop(rx);\n   614:     /// assert_eq!(tx.send(1).unwrap_err().0, 1);\n   615:     /// ```\n   616:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   617:     pub fn send(&self, t: T) -> Result<(), SendError<T>> {\n   618:         self.inner.send(t)\n   619:     }\n   620: \n   621:     /// Returns `true` if the channel is disconnected.\n   622:     ///\n   623:     /// Note that a return value of `false` does not guarantee the channel will\n   624:     /// remain connected. The channel may be disconnected immediately after this method\n   625:     /// returns, so a subsequent [`Sender::send`] may still fail with [`SendError`].\n   626:     ///\n   627:     /// # Examples",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::SyncSender::send",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "send",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7868,
            "path": "SyncSender"
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
        "impl_id": "std:7992",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7868",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "SyncSender"
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
            "t",
            {
              "generic": "T"
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
                        "id": 7661,
                        "path": "SendError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   680:     ///\n   681:     /// // Create a rendezvous sync_channel with buffer size 0\n   682:     /// let (sync_sender, receiver) = sync_channel(0);\n   683:     ///\n   684:     /// thread::spawn(move || {\n   685:     ///    println!(\"sending message...\");\n   686:     ///    sync_sender.send(1).unwrap();\n   687:     ///    // Thread is now blocked until the message is received\n   688:     ///\n   689:     ///    println!(\"...message received!\");\n   690:     /// });\n   691:     ///\n   692:     /// let msg = receiver.recv().unwrap();\n   693:     /// assert_eq!(1, msg);\n   694:     /// ```\n   695:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   696:     pub fn send(&self, t: T) -> Result<(), SendError<T>> {\n   697:         self.inner.send(t)\n   698:     }\n   699: \n   700:     /// Attempts to send a value on this channel without blocking.\n   701:     ///\n   702:     /// This method differs from [`send`] by returning immediately if the\n   703:     /// channel's buffer is full or no receiver is waiting to acquire some\n   704:     /// data. Compared with [`send`], this function has two failure cases\n   705:     /// instead of one (one for disconnection, one for a full buffer).\n   706:     ///\n   707:     /// See [`send`] for notes about guarantees of whether the\n   708:     /// receiver has received the data or not if this function is successful.\n   709:     ///\n   710:     /// [`send`]: Self::send\n   711:     ///\n   712:     /// # Examples",
    "nanvix_source": "   699:     ///    sync_sender.send(1).unwrap();\n   700:     ///    // Thread is now blocked until the message is received\n   701:     ///\n   702:     ///    println!(\"...message received!\");\n   703:     /// });\n   704:     ///\n   705:     /// let msg = receiver.recv().unwrap();\n   706:     /// assert_eq!(1, msg);\n   707:     /// ```\n   708:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   709:     pub fn send(&self, t: T) -> Result<(), SendError<T>> {\n   710:         self.inner.send(t)\n   711:     }\n   712: \n   713:     /// Attempts to send a value on this channel without blocking.\n   714:     ///\n   715:     /// This method differs from [`send`] by returning immediately if the\n   716:     /// channel's buffer is full or no receiver is waiting to acquire some\n   717:     /// data. Compared with [`send`], this function has two failure cases\n   718:     /// instead of one (one for disconnection, one for a full buffer).\n   719:     ///",
    "previous_skip_rationale": ""
  },
  {
    "target": "std::sync::mpsc::SyncSender::try_send",
    "generation_group": "runtime_or_hidden_state",
    "classification": "runtime_or_hidden_state",
    "classification_reasons": [
      "external_or_hidden_runtime_state"
    ],
    "category": "io_os_runtime",
    "kinds": [
      "inherent_method"
    ],
    "semantic_risks": [
      "external_or_hidden_runtime_state",
      "concurrency_or_hidden_state"
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
      "name": "try_send",
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
                  }
                ],
                "constraints": []
              }
            },
            "id": 7868,
            "path": "SyncSender"
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
        "impl_id": "std:7992",
        "kind": "inherent_impl",
        "resolved_owner_id": "std:7868",
        "resolved_owner_path": [
          "std",
          "sync",
          "mpsc",
          "SyncSender"
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
            "t",
            {
              "generic": "T"
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
                        "id": 7665,
                        "path": "TrySendError"
                      }
                    }
                  }
                ],
                "constraints": []
              }
            },
            "id": 62,
            "path": "Result"
          }
        }
      }
    },
    "verification_source": "   738:     /// println!(\"message {msg} received\");\n   739:     ///\n   740:     /// msg = receiver.recv().unwrap();\n   741:     /// println!(\"message {msg} received\");\n   742:     ///\n   743:     /// // Third message may have never been sent\n   744:     /// match receiver.try_recv() {\n   745:     ///     Ok(msg) => println!(\"message {msg} received\"),\n   746:     ///     Err(_) => println!(\"the third message was never sent\"),\n   747:     /// }\n   748:     ///\n   749:     /// // Wait for threads to complete\n   750:     /// handle1.join().unwrap();\n   751:     /// handle2.join().unwrap();\n   752:     /// ```\n   753:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   754:     pub fn try_send(&self, t: T) -> Result<(), TrySendError<T>> {\n   755:         self.inner.try_send(t)\n   756:     }\n   757: \n   758:     // Attempts to send for a value on this receiver, returning an error if the\n   759:     // corresponding channel has hung up, or if it waits more than `timeout`.\n   760:     //\n   761:     // This method is currently only used for tests.\n   762:     #[unstable(issue = \"none\", feature = \"std_internals\")]\n   763:     #[doc(hidden)]\n   764:     pub fn send_timeout(&self, t: T, timeout: Duration) -> Result<(), mpmc::SendTimeoutError<T>> {\n   765:         self.inner.send_timeout(t, timeout)\n   766:     }\n   767: }\n   768: \n   769: #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   770: impl<T> Clone for SyncSender<T> {",
    "nanvix_source": "   757:     /// match receiver.try_recv() {\n   758:     ///     Ok(msg) => println!(\"message {msg} received\"),\n   759:     ///     Err(_) => println!(\"the third message was never sent\"),\n   760:     /// }\n   761:     ///\n   762:     /// // Wait for threads to complete\n   763:     /// handle1.join().unwrap();\n   764:     /// handle2.join().unwrap();\n   765:     /// ```\n   766:     #[stable(feature = \"rust1\", since = \"1.0.0\")]\n   767:     pub fn try_send(&self, t: T) -> Result<(), TrySendError<T>> {\n   768:         self.inner.try_send(t)\n   769:     }\n   770: \n   771:     // Attempts to send for a value on this receiver, returning an error if the\n   772:     // corresponding channel has hung up, or if it waits more than `timeout`.\n   773:     //\n   774:     // This method is currently only used for tests.\n   775:     #[unstable(issue = \"none\", feature = \"std_internals\")]\n   776:     #[doc(hidden)]\n   777:     pub fn send_timeout(&self, t: T, timeout: Duration) -> Result<(), mpmc::SendTimeoutError<T>> {",
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
