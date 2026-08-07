# Prior vs Fresh Semantic Taxonomy Audit

Generated at UTC `2026-08-07T07:06:30Z`.

This reproducible audit classifies every row in `prior_fresh_delta/decision_changes.csv` using fresh issue tags, fresh final-candidate rationales, and requires source-fidelity references/excerpts where a fresh accepted contract has preconditions.

## Counts

| Measure | Value |
| --- | ---: |
| changed rows | 147 |
| unclassified rows | 0 |
| unjustified change rows | 0 |
| unjustified downgrades | 0 |
| unjustified upgrades | 0 |

## Transition Counts

| Transition | Rows |
| --- | ---: |
| `add_spec->skip` | 117 |
| `skip->add_spec` | 30 |

## Taxonomy Counts

| Taxonomy | Rows |
| --- | ---: |
| `accepted_collection_lookup_or_conversion_contract` | 1 |
| `accepted_enum_result_forwarding_contract` | 1 |
| `accepted_slice_array_view_contract` | 16 |
| `accepted_source_justified_precondition` | 7 |
| `accepted_string_view_contract` | 5 |
| `associated_type_or_projection_gap` | 2 |
| `borrowed_key_model_underdetermined` | 3 |
| `clone_semantics_unmodeled` | 1 |
| `complex_result_or_pattern_model_gap` | 1 |
| `determinism_unsupported_contract_form` | 2 |
| `duplicate_existing_vstd_spec` | 5 |
| `formatting_effect_unmodeled` | 2 |
| `higher_order_behavior_unmodeled` | 37 |
| `needs_new_vstd_abstraction` | 4 |
| `ownership_or_uninitialized_model_gap` | 8 |
| `representation_or_allocator_model_gap` | 1 |
| `runtime_or_hidden_state` | 17 |
| `source_unspecified_after_exhaustion` | 2 |
| `trait_contract_integration_gap` | 1 |
| `unsafe_or_representation_sensitive` | 31 |

## Acceptance Checks

| Check | Passed |
| --- | --- |
| `decision_change_rows_147` | `true` |
| `classified_rows_147` | `true` |
| `unclassified_rows_zero` | `true` |
| `add_spec_to_skip_rows_117` | `true` |
| `add_spec_to_skip_all_have_fresh_rationale` | `true` |
| `add_spec_to_skip_all_source_backed_verdicts` | `true` |
| `skip_to_add_spec_rows_30` | `true` |
| `skip_to_add_spec_all_remain_accepted` | `true` |
| `skip_to_add_spec_issues_empty` | `true` |
| `skip_to_add_spec_requires_source_justified_where_present` | `true` |
| `unjustified_downgrade_rows_zero` | `true` |
| `unjustified_upgrade_rows_zero` | `true` |
| `unjustified_change_rows_zero` | `true` |
| `final_verification_2121_targets` | `true` |
| `final_verification_127_accepted` | `true` |
| `final_verification_1994_skips` | `true` |
| `final_verification_zero_missing_extra_duplicates` | `true` |
| `final_verification_skip_rationales_non_empty` | `true` |

## Artifacts

- `semantic_taxonomy_audit.csv`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/semantic_taxonomy_audit.csv`
- `semantic_taxonomy_summary.json`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/semantic_taxonomy_summary.json`
- `SEMANTIC_TAXONOMY_AUDIT.md`: `/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol-fresh-20260806-0453/prior_fresh_delta/SEMANTIC_TAXONOMY_AUDIT.md`
