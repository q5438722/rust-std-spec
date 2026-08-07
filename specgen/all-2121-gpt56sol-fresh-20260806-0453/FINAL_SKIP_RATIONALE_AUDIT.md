# Final Skip Rationale Taxonomy Audit

Generated at UTC `2026-08-07T07:06:28Z`.

This audit covers every `final_candidates.csv` row whose final decision is `skip`, classifies the row by a source-backed rationale taxonomy, and tracks the targeted repair for skips that had a non-empty rationale but empty machine issue tags.

## Counts

| Measure | Value |
| --- | ---: |
| final rows | 2121 |
| add_spec rows | 127 |
| skip rows | 1994 |
| audited skip rows | 1994 |
| empty skip rationales | 0 |
| empty skip issue tags | 0 |
| empty combined issue/taxonomy tags | 0 |
| unclassified skips | 0 |
| unjustified skips | 0 |
| tracked issue-tag repair targets | 16 |
| tracked repair targets with tags | 16 |
| batch issue-tag repairs applied | 0 |
| final CSV issue-tag repairs applied | 0 |
| duplicate existing vstd spec rows | 226 |
| duplicate vstd issue tags | 226 |
| duplicate rows with generic determinism tag | 0 |
| exact vstd skip rows | 198 |
| exact vstd skips not duplicate-classified | 0 |

## Taxonomy Counts

| Taxonomy | Rows |
| --- | ---: |
| `associated_type_or_projection_gap` | 19 |
| `clone_semantics_unmodeled` | 12 |
| `compiler_intrinsic_model_gap` | 1 |
| `complex_result_or_pattern_model_gap` | 26 |
| `determinism_unsupported_contract_form` | 85 |
| `duplicate_existing_vstd_spec` | 226 |
| `formatting_effect_unmodeled` | 68 |
| `higher_order_behavior_unmodeled` | 210 |
| `iterator_or_adapter_result_gap` | 65 |
| `needs_new_vstd_abstraction` | 155 |
| `no_modeled_observable_output` | 48 |
| `one_sided_range_split_point_underdetermined` | 1 |
| `ownership_or_uninitialized_model_gap` | 28 |
| `representation_or_allocator_model_gap` | 29 |
| `runtime_or_hidden_state` | 599 |
| `source_unspecified_after_exhaustion` | 9 |
| `trait_contract_integration_gap` | 146 |
| `unsafe_or_representation_sensitive` | 267 |

## Acceptance Checks

| Check | Passed |
| --- | --- |
| `final_rows_2121` | `true` |
| `add_spec_rows_127` | `true` |
| `skip_rows_1994` | `true` |
| `audited_skip_rows_1994` | `true` |
| `empty_skip_rationale_rows_zero` | `true` |
| `empty_skip_issue_tag_rows_zero` | `true` |
| `empty_combined_issue_taxonomy_rows_zero` | `true` |
| `unclassified_skip_rows_zero` | `true` |
| `unjustified_skip_rows_zero` | `true` |
| `accepted_add_spec_contracts_unchanged` | `true` |
| `duplicate_existing_vstd_spec_rows_match_issue_count` | `true` |
| `duplicate_existing_vstd_spec_rows_all_carry_duplicate_vstd_tag` | `true` |
| `duplicate_existing_vstd_spec_rows_with_generic_determinism_zero` | `true` |
| `exact_vstd_skip_rows_not_duplicate_classified_zero` | `true` |

## Artifacts

- `final_skip_rationale_audit.csv`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/final_skip_rationale_audit.csv`
- `final_skip_rationale_audit_summary.json`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/final_skip_rationale_audit_summary.json`
- `FINAL_SKIP_RATIONALE_AUDIT.md`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/FINAL_SKIP_RATIONALE_AUDIT.md`
