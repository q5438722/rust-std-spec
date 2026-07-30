# Static proof fidelity audit

- Proofs: **406**
- High-risk static findings: **20**
- Proofs containing explicit axioms: **64**
- Proofs containing lower `assume_specification`: **103**

## Flag counts

- `control_flow_shape_changed`: 145
- `very_low_source_similarity`: 86
- `contains_axiom`: 64
- `same_named_call`: 50
- `extra_requires`: 20

## High-risk targets

- `std_specs__duration.rs__L210__Duration__as_secs_f32` — contains_axiom, extra_requires, very_low_source_similarity
- `std_specs__duration.rs__L215__Duration__as_secs_f64` — contains_axiom, extra_requires, very_low_source_similarity
- `std_specs__duration.rs__L322__Duration__mul_f64` — contains_axiom, extra_requires
- `std_specs__duration.rs__L329__Duration__mul_f32` — contains_axiom, extra_requires
- `std_specs__duration.rs__L336__Duration__div_f64` — contains_axiom, extra_requires
- `std_specs__duration.rs__L343__Duration__div_f32` — contains_axiom, extra_requires
- `std_specs__duration.rs__L394__Duration__div_duration_f32` — contains_axiom, extra_requires
- `std_specs__duration.rs__L403__Duration__div_duration_f64` — contains_axiom, extra_requires
- `std_specs__slice.rs__L44__usize__as__SliceIndex__T__index` — extra_requires
- `std_specs__slice.rs__L56__Range__usize__as__SliceIndex__T__index` — control_flow_shape_changed, extra_requires, very_low_source_similarity
- `std_specs__slice.rs__L75__T__as__Index__I__index` — extra_requires, same_named_call
- `std_specs__slice.rs__L83__T__N__as__Index__I__index` — extra_requires, same_named_call
- `std_specs__vec.rs__L184__Vec__T__A__index` — extra_requires, same_named_call
- `std_specs__vec.rs__L192__Vec__T__A__swap_remove` — control_flow_shape_changed, extra_requires, very_low_source_similarity
- `std_specs__vec.rs__L203__Vec__T__A__insert` — extra_requires
- `std_specs__vec.rs__L220__Vec__T__A__remove` — extra_requires
- `std_specs__vecdeque.rs__L263__VecDeque__T__A__rotate_left` — control_flow_shape_changed, extra_requires
- `std_specs__vecdeque.rs__L276__VecDeque__T__A__rotate_right` — control_flow_shape_changed, extra_requires, very_low_source_similarity
- `std_specs__vecdeque.rs__L312__VecDeque__T__A__insert` — extra_requires
- `std_specs__vecdeque.rs__L71__VecDeque__T__A__index` — extra_requires
