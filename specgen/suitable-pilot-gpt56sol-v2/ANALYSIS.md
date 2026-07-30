# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `targets` | 32 |
| `initial_add_spec` | 31 |
| `initial_skip` | 1 |
| `final_add_spec` | 24 |
| `final_skip` | 8 |
| `typecheck_passed` | 24 |
| `det_unsat` | 24 |
| `det_sat` | 0 |
| `det_unknown` | 0 |
| `raw_reward` | 24 |
| `guarded_reward` | 24 |
| `semantic_guarded_reward` | 18 |
| `llm_errors` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 24 |
| `add_spec->skip` | 7 |
| `skip->skip` | 1 |

## Frequent issues

| Issue | Count |
|---|---:|

## Guarded-deterministic candidates

| Target | Ensures |
|---|---|
| `alloc::collections::BTreeMap::append` | `final(m)@ == old(m)@.union_prefer_right(old(other)@); final(other)@ == Map::<Key, Value>::empty()` |
| `alloc::collections::BTreeSet::append` | `final(m)@ == old(m)@.union(old(other)@); final(other)@ == Set::<Key>::empty()` |
| `alloc::string::String::clear` | `final(s)@ == Seq::<char>::empty()` |
| `core::mem::replace` | `res == *old(dest); *final(dest) == src` |
| `core::option::Option::replace` | `res == *old(option); *final(option) == core::option::Option::Some(value)` |
| `alloc::collections::BTreeMap::first_key_value` | `match result {
            Some((key, value)) => {
                let min_key = m@.dom().find_unique_minimal(
                    |left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,
                );
                &&& !m@.is_empty()
                &&& *key == min_key
                &&& m@.contains_key(*key)
                &&& *value == m@[*key]
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::first` | `match result { Some(v) => { &&& !m@.is_empty() &&& *v == m@.find_unique_minimal(|x: Key, y: Key| x.cmp_spec(&y) != Ordering::Greater,) &&& m@.contains(*v) &&& forall|x: Key| #[trigger] m@.contains(x) ==> v.cmp_spec(&x) != Ordering::Greater }, None => m@.is_empty(), }` |
| `alloc::string::String::as_bytes` | `res@ == encode_utf8(s@)` |
| `core::array::each_ref` | `forall|i: int| i >= 0 && N > i ==> *out[i] == ar[i]` |
| `core::ops::RangeInclusive::end` | `*ret == r@.end` |
| `core::slice::as_array` | `ret.is_some() <==> slice@.len() == N; ret.is_some() ==> ret.unwrap()@ == slice@` |
| `core::str::split_at_checked` | `res.is_some() <==> is_char_boundary(s.spec_bytes(), mid as int); res.is_some() ==> res.unwrap().0@ == decode_utf8(s.spec_bytes().subrange(0, mid as int)); res.is_some() ==> res.unwrap().1@ == decode_utf8(s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int))` |
| `alloc::collections::BTreeSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `alloc::string::String::into_bytes` | `res@ == vstd::utf8::encode_utf8(s@)` |
| `alloc::vec::Vec::into_boxed_slice` | `slice@ == vec@` |
| `core::array::repeat` | `forall|i: int| i >= 0 && N > i ==> result@[i] == val` |
| `core::cmp::max` | `match v2.cmp_spec(&v1) { core::cmp::Ordering::Less => r == v1, core::cmp::Ordering::Equal => r == v2, core::cmp::Ordering::Greater => r == v2, }` |
| `core::convert::identity` | `ret == x` |
| `core::hint::black_box` | `output == dummy` |
| `alloc::collections::BTreeMap::last_key_value` | `match result { Some((key, value)) => { let max_key = m@.dom().find_unique_maximal(|left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,); &&& !m@.is_empty() &&& *key == max_key &&& m@.contains_key(*key) &&& *value == m@[*key] }, None => m@.is_empty(), }` |
| `alloc::collections::BTreeMap::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let key = old(m)@.dom().find_unique_minimal(
                |left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,
            );
            &&& result == Some((key, old(m)@[key]))
            &&& final(m)@ == old(m)@.remove(key)
        }` |
| `alloc::collections::BTreeMap::pop_last` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let key = old(m)@.dom().find_unique_maximal(
                |left: Key, right: Key| left.cmp_spec(&right) != core::cmp::Ordering::Greater,
            );
            &&& result == Some((key, old(m)@[key]))
            &&& final(m)@ == old(m)@.remove(key)
        }` |
| `alloc::collections::BTreeMap::remove_entry` | `match result {
            Some((stored_key, value)) => {
                &&& contains_borrowed_key(old(m)@, key)
                &&& sets_borrowed_key_to_key(old(m)@.dom(), key, &stored_key)
                &&& old(m)@.contains_key(stored_key)
                &&& old(m)@[stored_key] == value
                &&& final(m)@ == old(m)@.remove(stored_key)
            },
            None => {
                &&& !contains_borrowed_key(old(m)@, key)
                &&& final(m)@ == old(m)@
            },
        }` |
| `alloc::vec::Vec::dedup` | `final(vec)@ == old(vec)@.fold_left(
            vstd::seq::Seq::<T>::empty(),
            |kept: vstd::seq::Seq<T>, element: T| {
                if kept.len() == 0 {
                    kept.push(element)
                } else if element.eq_spec(&kept.last()) {
                    kept
                } else {
                    kept.push(element)
                }
            },
        )` |

## Semantic-gated candidates

18 of 24 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.

| Target | Ensures |
|---|---|
| `alloc::string::String::clear` | `final(s)@ == Seq::<char>::empty()` |
| `core::mem::replace` | `res == *old(dest); *final(dest) == src` |
| `core::option::Option::replace` | `res == *old(option); *final(option) == core::option::Option::Some(value)` |
| `alloc::collections::BTreeMap::first_key_value` | `match result {
            Some((key, value)) => {
                let min_key = m@.dom().find_unique_minimal(
                    |left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,
                );
                &&& !m@.is_empty()
                &&& *key == min_key
                &&& m@.contains_key(*key)
                &&& *value == m@[*key]
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::first` | `match result { Some(v) => { &&& !m@.is_empty() &&& *v == m@.find_unique_minimal(|x: Key, y: Key| x.cmp_spec(&y) != Ordering::Greater,) &&& m@.contains(*v) &&& forall|x: Key| #[trigger] m@.contains(x) ==> v.cmp_spec(&x) != Ordering::Greater }, None => m@.is_empty(), }` |
| `alloc::string::String::as_bytes` | `res@ == encode_utf8(s@)` |
| `core::array::each_ref` | `forall|i: int| i >= 0 && N > i ==> *out[i] == ar[i]` |
| `core::ops::RangeInclusive::end` | `*ret == r@.end` |
| `core::slice::as_array` | `ret.is_some() <==> slice@.len() == N; ret.is_some() ==> ret.unwrap()@ == slice@` |
| `core::str::split_at_checked` | `res.is_some() <==> is_char_boundary(s.spec_bytes(), mid as int); res.is_some() ==> res.unwrap().0@ == decode_utf8(s.spec_bytes().subrange(0, mid as int)); res.is_some() ==> res.unwrap().1@ == decode_utf8(s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int))` |
| `alloc::string::String::into_bytes` | `res@ == vstd::utf8::encode_utf8(s@)` |
| `alloc::vec::Vec::into_boxed_slice` | `slice@ == vec@` |
| `core::cmp::max` | `match v2.cmp_spec(&v1) { core::cmp::Ordering::Less => r == v1, core::cmp::Ordering::Equal => r == v2, core::cmp::Ordering::Greater => r == v2, }` |
| `core::convert::identity` | `ret == x` |
| `core::hint::black_box` | `output == dummy` |
| `alloc::collections::BTreeMap::last_key_value` | `match result { Some((key, value)) => { let max_key = m@.dom().find_unique_maximal(|left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,); &&& !m@.is_empty() &&& *key == max_key &&& m@.contains_key(*key) &&& *value == m@[*key] }, None => m@.is_empty(), }` |
| `alloc::collections::BTreeMap::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let key = old(m)@.dom().find_unique_minimal(
                |left: Key, right: Key| left.cmp_spec(&right) != Ordering::Greater,
            );
            &&& result == Some((key, old(m)@[key]))
            &&& final(m)@ == old(m)@.remove(key)
        }` |
| `alloc::collections::BTreeMap::pop_last` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let key = old(m)@.dom().find_unique_maximal(
                |left: Key, right: Key| left.cmp_spec(&right) != core::cmp::Ordering::Greater,
            );
            &&& result == Some((key, old(m)@[key]))
            &&& final(m)@ == old(m)@.remove(key)
        }` |

## Per-target result

| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |
|---|---|---|---:|---|---:|---:|---|
| `alloc::collections::BTreeMap::append` | add_spec | add_spec | 1 | unsat | 1 | 0 | raw_btree_view_algebra |
| `alloc::collections::BTreeSet::append` | add_spec | add_spec | 1 | unsat | 1 | 0 | raw_btree_view_algebra |
| `alloc::string::String::clear` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::clone_from_slice` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::str::make_ascii_lowercase` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::split_off_last` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::first_key_value` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::as_bytes` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::each_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_array` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::split_at_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_disjoint` | add_spec | add_spec | 1 | unsat | 1 | 0 | raw_btree_view_algebra |
| `alloc::string::String::into_bytes` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::into_boxed_slice` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::repeat` | add_spec | add_spec | 1 | unsat | 1 | 0 | clone_behavior_domain_strengthening |
| `core::cmp::max` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::convert::identity` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::hint::black_box` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::discriminant` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::last_key_value` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::remove_entry` | add_spec | add_spec | 1 | unsat | 1 | 0 | borrowed_key_domain_strengthening;borrowed_key_uniqueness_precondition |
| `core::slice::split_off` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::vec::Vec::dedup` | add_spec | add_spec | 1 | unsat | 1 | 0 | dedup_pure_old_sequence_model |
| `core::slice::split_off_first` | add_spec | skip | 0 |  | 0 | 0 |  |
| `std::collections::HashMap::get_key_value` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::get_key_value` | add_spec | skip | 0 |  | 0 | 0 |  |
