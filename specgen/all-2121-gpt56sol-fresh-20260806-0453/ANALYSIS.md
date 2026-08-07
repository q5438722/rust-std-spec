# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `manifest_targets` | 2121 |
| `targets` | 2121 |
| `missing_targets` | 0 |
| `initial_add_spec` | 872 |
| `initial_skip` | 1249 |
| `final_add_spec` | 127 |
| `final_skip` | 1994 |
| `typecheck_passed` | 127 |
| `typechecked_final_add_spec` | 127 |
| `det_unsat` | 127 |
| `det_sat` | 0 |
| `det_unknown` | 0 |
| `raw_reward` | 127 |
| `guarded_reward` | 127 |
| `semantic_guarded_reward` | 127 |
| `accepted_semantic_candidates` | 127 |
| `llm_errors` | 0 |
| `exceptions` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 127 |
| `add_spec->skip` | 745 |
| `skip->skip` | 1249 |

## Frequent issues

| Issue | Count |
|---|---:|
| `determinism_unsupported_contract_form` | 611 |
| `classification:runtime_or_hidden_state` | 494 |
| `duplicate_vstd_assume_specification` | 226 |
| `classification:trait_contract_integration` | 201 |
| `classification:concurrency_or_hidden_state` | 179 |
| `classification:unsafe_or_representation_sensitive` | 178 |
| `classification:needs_new_vstd_abstraction` | 174 |
| `no_modeled_observable_output` | 137 |
| `classification:iterator_or_adapter_result` | 101 |
| `classification:determinism_checker_unsupported` | 87 |
| `classification:formatting_effect` | 79 |
| `classification:higher_order_contract` | 71 |
| `classification:toolchain_unavailable` | 70 |
| `not_in_verus_rust_1_96` | 70 |
| `classification:representation_or_allocator` | 59 |
| `classification:ownership_or_uninitialized_model` | 33 |
| `classification:complex_result_or_pattern_model` | 21 |
| `classification:associated_type_or_projection` | 19 |
| `classification:no_modeled_observable_output` | 9 |
| `clone_semantics_unmodeled` | 3 |
| `panic_location_abstraction_missing` | 3 |
| `permitted_partition_order_underdetermined` | 3 |
| `higher_order_closure_comparator_underdetermined` | 2 |
| `value_unspecified_after_exhaustion` | 2 |
| `higher_order_closure_key_extraction_underdetermined` | 2 |
| `generic_pattern_reverse_search_underdetermined` | 2 |
| `cow_to_mut_payload_reference_model_missing` | 1 |
| `implementation_dependent_split_point` | 1 |
| `peekable_next_if_closure_observation_underdetermined` | 1 |
| `peekable_next_if_map_mut_closure_observation_underdetermined` | 1 |

## Guarded-deterministic candidates

| Target | Ensures |
|---|---|
| `alloc::collections::BTreeMap::append` | `final(m)@ == old(m)@.union_prefer_right(old(other)@); final(other)@ == Map::<Key, Value>::empty()` |
| `alloc::collections::BTreeMap::first_key_value` | `match result {
            Some((key, value)) => {
                &&& m@.contains_key(*key)
                &&& m@[*key] == *value
                &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                    (*key).cmp_spec(&other) != core::cmp::Ordering::Greater
                &&& *key == choose|candidate: Key| {
                    m@.contains_key(candidate)
                        && forall|other: Key| #[trigger] m@.contains_key(other) ==>
                            candidate.cmp_spec(&other) != core::cmp::Ordering::Greater
                }
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeMap::get_mut` | `{
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        }` |
| `alloc::collections::BTreeMap::last_key_value` | `match result {
            Some((k, v)) => {
                &&& *k == choose|max_key: Key| {
                    &&& m@.contains_key(max_key)
                    &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                        other.cmp_spec(&max_key) != core::cmp::Ordering::Greater
                }
                &&& m@.contains_key(*k)
                &&& m@[*k] == *v
                &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                    other.cmp_spec(k) != core::cmp::Ordering::Greater
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeMap::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let k = choose|k: Key| {
                &&& old(m)@.contains_key(k)
                &&& forall|key: Key| #[trigger] old(m)@.contains_key(key) ==>
                    key == k || k.cmp_spec(&key) == core::cmp::Ordering::Less
            };
            &&& result == Some((k, old(m)@[k]))
            &&& final(m)@ == old(m)@.remove(k)
        }` |
| `alloc::collections::BTreeMap::pop_last` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let k = choose|k: Key|
                old(m)@.contains_key(k)
                && forall|other: Key| #![auto]
                    old(m)@.contains_key(other) ==> {
                        other.cmp_spec(&k) is Less || other == k
                    };
            &&& result == Some((k, old(m)@[k]))
            &&& final(m)@ == old(m)@.remove(k)
        }` |
| `alloc::collections::BTreeSet::append` | `final(m)@ == old(m)@.union(old(other)@); final(other)@ == vstd::set::Set::<Key>::empty()` |
| `alloc::collections::BTreeSet::first` | `match result {
            Some(v) => {
                &&& m@.contains(*v)
                &&& forall|other: Key| #[trigger] m@.contains(other) ==>
                    (*v).cmp_spec(&other) != core::cmp::Ordering::Greater
                &&& *v == choose|candidate: Key| {
                    m@.contains(candidate)
                        && forall|other: Key| #[trigger] m@.contains(other) ==>
                            candidate.cmp_spec(&other) != core::cmp::Ordering::Greater
                }
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `alloc::collections::BTreeSet::is_subset` | `result == m@.subset_of(other@)` |
| `alloc::collections::BTreeSet::is_superset` | `result == other@.subset_of(m@)` |
| `alloc::collections::BTreeSet::last` | `match result {
            core::option::Option::Some(value) => {
                &&& !m@.is_empty()
                &&& *value == m@.find_unique_maximal(
                    |x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,
                )
                &&& m@.contains(*value)
                &&& forall|x: T| #[trigger] m@.contains(x) ==>
                    x.cmp_spec(value) != core::cmp::Ordering::Greater
            },
            core::option::Option::None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let first = choose|candidate: T| {
                &&& old(m)@.contains(candidate)
                &&& forall|element: T| old(m)@.contains(element)
                    ==> candidate.cmp_spec(&element) != Ordering::Greater
            };
            &&& result == Some(first)
            &&& old(m)@.contains(first)
            &&& forall|element: T| old(m)@.contains(element)
                ==> first.cmp_spec(&element) != Ordering::Greater
            &&& final(m)@ == old(m)@.remove(first)
        }` |
| `alloc::collections::BTreeSet::pop_last` | `forall|v: Key| #![auto]
            result == Some(v) <==> old(m)@.contains(v)
                && forall|k: Key| #![auto]
                    old(m)@.contains(k) && k != v ==> k.cmp_spec(&v) is Less; (result is None) == old(m)@.is_empty(); match result {
            Some(v) => final(m)@ == old(m)@.remove(v),
            None => final(m)@ == old(m)@,
        }` |
| `alloc::collections::BTreeSet::replace` | `final(m)@ == old(m)@.insert(value); result == if old(m)@.contains(value) { Some(value) } else { None }` |
| `alloc::collections::LinkedList::back_mut` | `result is Some == (old(list)@.len() != 0); result is None == (old(list)@.len() == 0); result matches Some(value) ==> {
            &&& *value == old(list)@.last()
            &&& *final(value) == *value
            &&& final(list)@ == old(list)@
        }; result is None ==> final(list)@ == old(list)@` |
| `alloc::collections::VecDeque::binary_search` | `match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }` |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | `result@ == bytes@.drop_last()` |
| `alloc::string::String::as_bytes` | `res@ == encode_utf8(s@)` |
| `alloc::string::String::clear` | `final(s)@ == Seq::<char>::empty(); final(s).spec_capacity() == old(s).spec_capacity()` |
| `alloc::string::String::from_utf8_unchecked` | `forall|chars: vstd::prelude::Seq<char>|
            vstd::utf8::encode_utf8(chars) == bytes@ ==> res@ == chars` |
| `alloc::string::String::insert` | `final(s)@ == old(s)@.insert(
            choose |i: int| 0 <= i <= old(s)@.len()
                && encode_utf8(old(s)@.subrange(0, i)).len() == idx as nat,
            ch,
        )` |
| `alloc::string::String::insert_str` | `final(s)@ == vstd::utf8::decode_utf8(
            vstd::utf8::encode_utf8(old(s)@).take(idx as int)
                + vstd::utf8::encode_utf8(string@)
                + vstd::utf8::encode_utf8(old(s)@).skip(idx as int)
        )` |
| `alloc::string::String::into_bytes` | `res@ == vstd::utf8::encode_utf8(s@)` |
| `alloc::string::String::is_empty` | `result == (s@.len() == 0)` |
| `alloc::string::String::len` | `result as nat == encode_utf8(s@).len()` |
| `alloc::string::String::pop` | `old(s)@.len() == 0 ==> result == None && final(s)@ == old(s)@; old(s)@.len() > 0 ==> result == Some(old(s)@[old(s)@.len() - 1])
            && final(s)@ == old(s)@.drop_last()` |
| `alloc::string::String::push` | `final(s)@ == old(s)@.push(ch)` |
| `alloc::string::String::push_str` | `final(s)@ == old(s)@ + string@` |
| `alloc::string::String::remove` | `forall |i: int| #![trigger encode_utf8(old(s)@.subrange(0, i))]
            0 <= i < old(s)@.len()
            && idx as nat == encode_utf8(old(s)@.subrange(0, i)).len()
            ==> result == old(s)@[i]
                && final(s)@ == old(s)@.subrange(0, i)
                    + old(s)@.subrange(i + 1, old(s)@.len() as int)` |
| `alloc::string::String::replace_range` | `final(s)@ == string_replace_range_result(&range, encode_utf8(old(s)@), replace_with@)` |
| `alloc::string::String::split_off` | `forall |i: int| #![auto]
            0 <= i <= old(s)@.len()
                && vstd::utf8::encode_utf8(old(s)@.take(i)).len() == at as nat
            ==> final(s)@ == old(s)@.take(i)
                && result@ == old(s)@.skip(i); final(s).spec_capacity() == old(s).spec_capacity()` |
| `alloc::string::String::truncate` | `final(s)@ == if (new_len as nat) < encode_utf8(old(s)@).len() {
            old(s)@.take(choose |i: int| 0 <= i <= old(s)@.len()
                && encode_utf8(old(s)@.take(i)).len() == new_len as nat)
        } else {
            old(s)@
        }` |
| `alloc::vec::Vec::dedup` | `final(vec)@ == Seq::new(old(vec)@.len(), |i: int| i)
            .filter(|i: int| i == 0 || !old(vec)@[i].eq_spec(&old(vec)@[i - 1]))
            .map(|_j: int, i: int| old(vec)@[i])` |
| `alloc::vec::Vec::into_boxed_slice` | `slice@ == vec@` |
| `alloc::vec::Vec::into_flattened` | `result@ == Seq::new(vec@.len() * (N as nat), |k: int|
            (vec@[k / (N as int)])@[k % (N as int)])` |
| `core::array::as_mut_slice` | `out@ == old(ar)@; final(out)@ == out@; final(out)@ == final(ar)@` |
| `core::array::each_mut` | `forall|i: int| #![auto] 0 <= i < N ==> *out[i] == old(ar)@[i]; forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == *out[i]; forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == final(ar)@[i]` |
| `core::array::each_ref` | `forall|i: int| 0 <= i < N ==> *(out@[i]) == ar@[i]` |
| `core::array::from_mut` | `out@[0] == *old(s); final(out)@ == out@; *final(s) == final(out)@[0]` |
| `core::array::from_ref` | `out@ == seq![*s]` |
| `core::cmp::max` | `match v1.cmp_spec(&v2) {
            core::cmp::Ordering::Greater => r == v1,
            core::cmp::Ordering::Less | core::cmp::Ordering::Equal => r == v2,
        }` |
| `core::cmp::min` | `match v1.cmp_spec(&v2) {
            core::cmp::Ordering::Less => r == v1,
            core::cmp::Ordering::Equal => r == v1,
            core::cmp::Ordering::Greater => r == v2,
        }` |
| `core::convert::identity` | `ret == x` |
| `core::hint::black_box` | `output == dummy` |
| `core::hint::select_unpredictable` | `condition ==> result == true_val; !condition ==> result == false_val` |
| `core::mem::min_align_of` | `res == core::mem::align_of::<T>()` |
| `core::mem::min_align_of_val` | `res == core::mem::align_of_val(val)` |
| `core::mem::replace` | `res == *old(dest); *final(dest) == src` |
| `core::ops::Range::is_empty` | `ret == !r.start.is_lt(&r.end)` |
| `core::ops::RangeInclusive::into_inner` | `ret.0 == r@.start; ret.1 == r@.end` |
| `core::ops::RangeInclusive::is_empty` | `ret == (r@.exhausted || !r@.start.is_le(&r@.end))` |
| `core::option::Option::and` | `option.is_none() ==> res.is_none(); option.is_some() ==> res == optb` |
| `core::option::Option::flatten` | `res == match option {
            Some(inner) => inner,
            None => None,
        }` |
| `core::option::Option::or` | `option.is_some() ==> res == option; option.is_none() ==> res == optb` |
| `core::option::Option::replace` | `res == *old(option); *final(option) == core::option::Option::Some(value)` |
| `core::option::Option::transpose` | `res == match option { Some(Ok(x)) => Ok(Some(x)), Some(Err(e)) => Err(e), None => Ok(None) }` |
| `core::option::Option::unzip` | `option is Some ==> res.0 is Some && res.1 is Some && option->0 == (res.0->0, res.1->0); option is None ==> res.0 is None && res.1 is None` |
| `core::option::Option::xor` | `res == match (option, optb) { (Some(a), None) => Some(a), (None, Some(b)) => Some(b), _ => None }` |
| `core::option::Option::zip` | `res == match (option, other) {
            (core::option::Option::Some(a), core::option::Option::Some(b)) => core::option::Option::Some((a, b)),
            _ => core::option::Option::None,
        }` |
| `core::result::Result::and` | `result is Ok ==> and_result == res; result is Err ==> and_result is Err && and_result->Err_0 == result->Err_0` |
| `core::result::Result::expect_err` | `e == result->Err_0` |
| `core::result::Result::flatten` | `flattened == match result {
            core::result::Result::Ok(inner) => inner,
            core::result::Result::Err(e) => core::result::Result::Err(e),
        }` |
| `core::result::Result::or` | `result is Ok ==> or_result is Ok && or_result->Ok_0 == result->Ok_0; result is Err ==> or_result == res` |
| `core::result::Result::transpose` | `transposed == match result {
            core::result::Result::Ok(core::option::Option::Some(x)) => core::option::Option::Some(core::result::Result::Ok(x)),
            core::result::Result::Ok(core::option::Option::None) => core::option::Option::None,
            core::result::Result::Err(e) => core::option::Option::Some(core::result::Result::Err(e)),
        }` |
| `core::result::Result::unwrap_or` | `result is Ok ==> value == result->Ok_0; result is Err ==> value == default` |
| `core::slice::as_array` | `ret.is_some() <==> slice@.len() == N; ret.is_some() ==> ret.unwrap()@ == slice@` |
| `core::slice::as_chunks` | `{
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == slice@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == slice@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == slice@.len() / (N as nat)
            &&& ret.1@.len() == slice@.len() % (N as nat)
            &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len()
            &&& forall|i: int| 0 <= i < ret.0@.len() ==>
                (#[trigger] ret.0@[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                )
            &&& ret.1@ == slice@.subrange(
                ((slice@.len() / (N as nat)) * (N as nat)) as int,
                slice@.len() as int,
            )
        }` |
| `core::slice::as_chunks_mut` | `{
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == old(slice)@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == old(slice)@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == old(slice)@.len() / (N as nat)
            &&& ret.1@ == old(slice)@.subrange(
                ((old(slice)@.len() / (N as nat)) * (N as nat)) as int,
                old(slice)@.len() as int,
            )
            &&& final(ret.0)@ == ret.0@
            &&& final(ret.1)@ == ret.1@
            &&& final(slice)@ == old(slice)@
        }` |
| `core::slice::as_flattened` | `ret@.len() == slice@.len() * N; forall|i: int| 0 <= i < ret@.len() ==> ret@[i] == slice@[i / (N as int)][i % (N as int)]` |
| `core::slice::as_mut_array` | `ret is Some == (old(slice)@.len() == N); ret matches Some(out) ==> {
            &&& out@ == old(slice)@
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::as_rchunks` | `ret.0@ == slice@.subrange(
            0,
            (slice@.len() % (N as nat)) as int,
        ); ret.1@ == Seq::new(
            slice@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    (slice@.len() % (N as nat)) as int + i * (N as int),
                    (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ); forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == slice@.subrange(
                (slice@.len() % (N as nat)) as int + i * (N as int),
                (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
            )` |
| `core::slice::as_rchunks_mut` | `ret.0@ == old(slice)@.subrange(
            0,
            (old(slice)@.len() % (N as nat)) as int,
        ); ret.1@ == Seq::new(
            old(slice)@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == old(slice)@.subrange(
                    (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                    (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ); forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == old(slice)@.subrange(
                (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
            ); final(ret.0)@ == ret.0@; final(ret.1)@ == ret.1@; final(slice)@ == old(slice)@` |
| `core::slice::binary_search` | `match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }` |
| `core::slice::contains` | `result <==> exists|i: int| 0 <= i < slice@.len() && slice@[i].eq_spec(x)` |
| `core::slice::eq_ignore_ascii_case` | `result == (
            slice@.len() == other@.len()
            && forall|i: int| 0 <= i < slice@.len() ==> {
                let a = (#[trigger] slice@[i]) as int;
                let b = other@[i] as int;
                a == b
                    || (65 <= a && a <= 90 && b == a + 32)
                    || (65 <= b && b <= 90 && a == b + 32)
            }
        )` |
| `core::slice::first_chunk` | `match ret {
            Option::Some(chunk) =>
                slice@.len() >= N && chunk@ == slice@.subrange(0, N as int),
            Option::None => slice@.len() < N,
        }` |
| `core::slice::first_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(0, N as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@ + old(slice)@.subrange(N as int, old(slice)@.len() as int)
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::from_mut` | `ret@ == seq![*old(s)]; final(ret)@ == ret@; final(ret)@ == seq![*final(s)]; *final(s) == *old(s)` |
| `core::slice::from_ref` | `result@ == seq![*s]` |
| `core::slice::is_ascii` | `ret == (forall|i: int| 0 <= i < slice@.len() ==> slice@[i] <= 0x7f)` |
| `core::slice::is_sorted` | `result <==> forall|i: int|
            0 <= i && i + 1 < slice@.len()
                ==> (#[trigger] slice@[i]).is_le(&slice@[i + 1])` |
| `core::slice::last_chunk` | `ret.is_some() <==> N <= slice.len(); ret.is_some() ==> ret.unwrap()@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int)` |
| `core::slice::last_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - N as int) + final(out)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::reverse` | `final(slice)@ == old(slice)@.reverse()` |
| `core::slice::split_at_checked` | `ret is Some == (mid <= slice.len()); ret matches Some((left, right)) ==> {
            &&& left@ == slice@.subrange(0, mid as int)
            &&& right@ == slice@.subrange(mid as int, slice@.len() as int)
        }` |
| `core::slice::split_at_mut_checked` | `ret is Some == (mid <= old(slice)@.len()); ret matches Some((left, right)) ==> {
            &&& left@ == old(slice)@.subrange(0, mid as int)
            &&& right@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            &&& final(left)@ == left@
            &&& final(right)@ == right@
            &&& final(slice)@ == final(left)@ + final(right)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_at_mut_unchecked` | `ret.0@ == old(slice)@.subrange(0, mid as int); ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int); final(ret.0)@ == ret.0@; final(ret.1)@ == ret.1@; final(slice)@ == final(ret.0)@ + final(ret.1)@` |
| `core::slice::split_first` | `ret.is_some() == (slice@.len() > 0); match ret {
            Some((first, tail)) =>
                *first == slice@[0]
                && tail@ == slice@.subrange(1, slice@.len() as int),
            None => true,
        }` |
| `core::slice::split_first_chunk` | `ret.is_some() <==> N <= slice.len(); ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, N as int); ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int)` |
| `core::slice::split_first_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some((first, tail)) ==> {
            &&& first@ == old(slice)@.subrange(0, N as int)
            &&& tail@ == old(slice)@.subrange(N as int, old(slice)@.len() as int)
            &&& final(first)@ == first@
            &&& final(tail)@ == tail@
            &&& final(slice)@ == final(first)@ + final(tail)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_first_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some((first, tail)) ==> {
            &&& *first == old(slice)@[0]
            &&& tail@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& *final(first) == *first
            &&& final(tail)@ == tail@
            &&& final(slice)@ == seq![*final(first)] + final(tail)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_last` | `ret.is_some() == (slice@.len() > 0); ret.is_some() ==> *ret.unwrap().0 == slice@[slice@.len() - 1]; ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(0, slice@.len() - 1)` |
| `core::slice::split_last_chunk` | `ret matches Some(_) <==> N <= slice@.len(); ret matches Some(parts) ==> parts.0@ == slice@.subrange(0, slice@.len() - N as int); ret matches Some(parts) ==> parts.1@ == slice@.subrange(slice@.len() - N as int, slice@.len() as int)` |
| `core::slice::split_last_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some((init, last)) ==> {
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - N as int)
            &&& last@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(init)@ == init@
            &&& final(last)@ == last@
            &&& final(slice)@ == final(init)@ + final(last)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_last_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some((last, init)) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& *final(last) == *last
            &&& final(init)@ == init@
            &&& final(slice)@ == final(init)@ + seq![*final(last)]
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_off_first` | `ret.is_none() == (old(slice)@.len() == 0); ret.is_some() ==> *ret.unwrap() == old(slice)@[0]; old(slice)@.len() == 0 ==> final(slice)@ == old(slice)@; old(slice)@.len() > 0 ==> final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int)` |
| `core::slice::split_off_first_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some(first) ==> {
            &&& *first == old(slice)@[0]
            &&& *final(first) == *first
            &&& final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& old(slice)@ == seq![*final(first)] + final(slice)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_off_last_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some(last) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& *final(last) == *last
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& old(slice)@ == final(slice)@ + seq![*final(last)]
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::starts_with` | `ret <==> (
            needle@.len() <= slice@.len()
            && forall|i: int| 0 <= i < needle@.len() ==> slice@[i].eq_spec(&needle@[i])
        )` |
| `core::slice::trim_ascii` | `exists|start: int, end: int| {
            &&& 0 <= start <= end <= slice@.len()
            &&& r@ == slice@.subrange(start, end)
            &&& (forall|i: int| 0 <= i < start ==> spec_is_ascii_whitespace(slice@[i]))
            &&& (forall|i: int| end <= i < slice@.len() ==> spec_is_ascii_whitespace(slice@[i]))
            &&& (start < end ==> !spec_is_ascii_whitespace(slice@[start]))
            &&& (start < end ==> !spec_is_ascii_whitespace(slice@[end - 1]))
        }` |
| `core::slice::trim_ascii_end` | `result@ == slice@.subrange(0, result@.len() as int); result@.len() <= slice@.len(); forall|i: int| result@.len() <= i < slice@.len() ==> {
            let byte = #[trigger] slice@[i];
            byte == 0x09 || byte == 0x0a || byte == 0x0c || byte == 0x0d || byte == 0x20
        }; result@.len() > 0 ==> {
            let byte = result@[(result@.len() - 1) as int];
            !(byte == 0x09 || byte == 0x0a || byte == 0x0c || byte == 0x0d || byte == 0x20)
        }` |
| `core::slice::trim_ascii_start` | `exists|start: int|
            0 <= start <= slice@.len()
            && (forall|i: int| 0 <= i < start ==> (
                slice@[i] == 0x09u8
                || slice@[i] == 0x0au8
                || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8
                || slice@[i] == 0x20u8
            ))
            && (start == slice@.len() || (
                slice@[start] != 0x09u8
                && slice@[start] != 0x0au8
                && slice@[start] != 0x0cu8
                && slice@[start] != 0x0du8
                && slice@[start] != 0x20u8
            ))
            && ret@ == slice@.subrange(start, slice@.len() as int)` |
| `core::str::ceil_char_boundary` | `result <= s.len(); index >= s.len() ==> result == s.len(); index < s.len() ==> index <= result; s.is_char_boundary(result); forall|i: usize| index <= i && i < result ==> !s.is_char_boundary(i)` |
| `core::str::eq_ignore_ascii_case` | `result == (s.spec_bytes().len() == other.spec_bytes().len() && forall|i: int| 0 <= i < s.spec_bytes().len() ==> (if 65 <= s.spec_bytes()[i] && s.spec_bytes()[i] <= 90 { (s.spec_bytes()[i] as int) + 32 } else { s.spec_bytes()[i] as int }) == (if 65 <= other.spec_bytes()[i] && other.spec_bytes()[i] <= 90 { (other.spec_bytes()[i] as int) + 32 } else { other.spec_bytes()[i] as int }))` |
| `core::str::floor_char_boundary` | `result <= index; result <= s.spec_bytes().len(); s.is_char_boundary(result); forall|i: usize| result < i && i <= index ==> !s.is_char_boundary(i)` |
| `core::str::from_utf8` | `valid_utf8(v@) ==> (result matches Ok(string) && string@ == decode_utf8(v@)); !valid_utf8(v@) ==> result is Err` |
| `core::str::from_utf8_mut` | `final(v)@ == old(v)@; valid_utf8(old(v)@) ==> (result matches Ok(string) && string@ == decode_utf8(old(v)@)); !valid_utf8(old(v)@) ==> result is Err` |
| `core::str::make_ascii_lowercase` | `final(s).spec_bytes().len() == old(s).spec_bytes().len(); forall|i: int| 0 <= i < old(s).spec_bytes().len() ==> #[trigger] final(s).spec_bytes()[i] as int
            == if 0x41u8 <= old(s).spec_bytes()[i] && old(s).spec_bytes()[i] <= 0x5au8 {
                old(s).spec_bytes()[i] as int + 32
            } else {
                old(s).spec_bytes()[i] as int
            }` |
| `core::str::make_ascii_uppercase` | `final(s).spec_bytes().len() == old(s).spec_bytes().len(); forall|i: int| 0 <= i < old(s).spec_bytes().len() ==>
            final(s).spec_bytes()[i] as int == if 0x61u8 <= old(s).spec_bytes()[i] && old(s).spec_bytes()[i] <= 0x7au8 {
                old(s).spec_bytes()[i] as int - 0x20int
            } else {
                old(s).spec_bytes()[i] as int
            }` |
| `core::str::split_at_checked` | `ret.is_some() == is_char_boundary(s.spec_bytes(), mid as int); ret.is_some() ==> ret.unwrap().0.spec_bytes() == s.spec_bytes().subrange(0, mid as int); ret.is_some() ==> ret.unwrap().1.spec_bytes() == s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int)` |
| `core::str::split_at_mut_checked` | `ret is Some <==> is_char_boundary(old(s).spec_bytes(), mid as int); ret matches Some((left, right)) ==> {
            &&& left.spec_bytes() =~= old(s).spec_bytes().subrange(0, mid as int)
            &&& right.spec_bytes() =~= old(s).spec_bytes().subrange(mid as int, old(s).spec_bytes().len() as int)
            &&& final(left).spec_bytes() == left.spec_bytes()
            &&& final(right).spec_bytes() == right.spec_bytes()
            &&& final(s).spec_bytes() == final(left).spec_bytes() + final(right).spec_bytes()
        }; ret is None ==> final(s).spec_bytes() == old(s).spec_bytes()` |
| `core::str::trim` | `result@ == ({
            let bounds = choose|bounds: (int, int)|
                0 <= bounds.0
                && bounds.0 <= bounds.1
                && bounds.1 <= s@.len()
                && (forall|i: int| 0 <= i < bounds.0 ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (forall|i: int| bounds.1 <= i < s@.len() ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.0]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.1 - 1]));
            s@.subrange(bounds.0, bounds.1)
        })` |
| `core::str::trim_ascii` | `result@ == ({
            let bounds = choose|bounds: (int, int)|
                0 <= bounds.0
                && bounds.0 <= bounds.1
                && bounds.1 <= s@.len()
                && (forall|i: int| 0 <= i < bounds.0 ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (forall|i: int| bounds.1 <= i < s@.len() ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (bounds.0 < bounds.1 ==> !(s@[bounds.0] == ' ' || s@[bounds.0] == '\t' || s@[bounds.0] == '\n' || s@[bounds.0] == '\x0c' || s@[bounds.0] == '\r'))
                && (bounds.0 < bounds.1 ==> !(s@[bounds.1 - 1] == ' ' || s@[bounds.1 - 1] == '\t' || s@[bounds.1 - 1] == '\n' || s@[bounds.1 - 1] == '\x0c' || s@[bounds.1 - 1] == '\r'));
            s@.subrange(bounds.0, bounds.1)
        })` |
| `core::str::trim_ascii_end` | `result@ == s@.subrange(0, result@.len() as int); result@.len() <= s@.len(); forall|i: int| result@.len() <= i < s@.len() ==> {
            let c = #[trigger] s@[i];
            c == ' ' || c == '\t' || c == '\n' || c == '\x0c' || c == '\r'
        }; result@.len() > 0 ==> {
            let c = result@[(result@.len() - 1) as int];
            !(c == ' ' || c == '\t' || c == '\n' || c == '\x0c' || c == '\r')
        }` |
| `core::str::trim_ascii_start` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (start == s@.len() || !(s@[start] == ' ' || s@[start] == '\t' || s@[start] == '\n' || s@[start] == '\x0c' || s@[start] == '\r'));
            s@.subrange(start, s@.len() as int)
        })` |
| `core::str::trim_end` | `result@ == s@.subrange(0, result@.len() as int); result@.len() <= s@.len(); forall|i: int| result@.len() <= i < s@.len() ==> {
            let c = #[trigger] s@[i];
            str_unicode_white_space(c)
        }; result@.len() > 0 ==> {
            let c = result@[(result@.len() - 1) as int];
            !str_unicode_white_space(c)
        }` |
| `core::str::trim_left` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (start == s@.len() || !str_unicode_white_space(s@[start]));
            s@.subrange(start, s@.len() as int)
        })` |
| `core::str::trim_right` | `result@.len() <= s@.len(); result@ == s@.take(result@.len() as int); forall|i: int| result@.len() <= i < s@.len() ==> (
            s@[i] == '\u{9}' || s@[i] == '\u{a}' || s@[i] == '\u{b}' || s@[i] == '\u{c}' || s@[i] == '\u{d}' ||
            s@[i] == '\u{20}' || s@[i] == '\u{85}' || s@[i] == '\u{a0}' || s@[i] == '\u{1680}' ||
            s@[i] == '\u{2000}' || s@[i] == '\u{2001}' || s@[i] == '\u{2002}' || s@[i] == '\u{2003}' ||
            s@[i] == '\u{2004}' || s@[i] == '\u{2005}' || s@[i] == '\u{2006}' || s@[i] == '\u{2007}' ||
            s@[i] == '\u{2008}' || s@[i] == '\u{2009}' || s@[i] == '\u{200a}' || s@[i] == '\u{2028}' ||
            s@[i] == '\u{2029}' || s@[i] == '\u{202f}' || s@[i] == '\u{205f}' || s@[i] == '\u{3000}'
        ); result@.len() == 0 || !(
            result@[result@.len() - 1] == '\u{9}' || result@[result@.len() - 1] == '\u{a}' ||
            result@[result@.len() - 1] == '\u{b}' || result@[result@.len() - 1] == '\u{c}' ||
            result@[result@.len() - 1] == '\u{d}' || result@[result@.len() - 1] == '\u{20}' ||
            result@[result@.len() - 1] == '\u{85}' || result@[result@.len() - 1] == '\u{a0}' ||
            result@[result@.len() - 1] == '\u{1680}' || result@[result@.len() - 1] == '\u{2000}' ||
            result@[result@.len() - 1] == '\u{2001}' || result@[result@.len() - 1] == '\u{2002}' ||
            result@[result@.len() - 1] == '\u{2003}' || result@[result@.len() - 1] == '\u{2004}' ||
            result@[result@.len() - 1] == '\u{2005}' || result@[result@.len() - 1] == '\u{2006}' ||
            result@[result@.len() - 1] == '\u{2007}' || result@[result@.len() - 1] == '\u{2008}' ||
            result@[result@.len() - 1] == '\u{2009}' || result@[result@.len() - 1] == '\u{200a}' ||
            result@[result@.len() - 1] == '\u{2028}' || result@[result@.len() - 1] == '\u{2029}' ||
            result@[result@.len() - 1] == '\u{202f}' || result@[result@.len() - 1] == '\u{205f}' ||
            result@[result@.len() - 1] == '\u{3000}'
        )` |
| `core::str::trim_start` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (start == s@.len() || !str_unicode_white_space(s@[start]));
            s@.subrange(start, s@.len() as int)
        })` |
| `std::collections::HashMap::get_mut` | `{
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        }` |
| `std::collections::HashMap::remove_entry` | `{
            let old_map = old(m)@;
            let removed_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &removed_key)
            &&& result == if contains_borrowed_key(old_map, k) {
                Some((removed_key, old_map[removed_key]))
            } else {
                None
            }
            &&& final(m)@ == if contains_borrowed_key(old_map, k) {
                old_map.remove(removed_key)
            } else {
                old_map
            }
        }` |
| `std::collections::HashSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `std::collections::HashSet::is_subset` | `result == m@.subset_of(other@)` |
| `std::collections::HashSet::is_superset` | `result == other@.subset_of(m@)` |
| `std::collections::HashSet::replace` | `match result {
            Some(replaced) => {
                &&& sets_borrowed_key_to_key(old(m)@, &value, &replaced)
                &&& final(m)@ == old(m)@.remove(replaced).insert(value)
            },
            None => {
                &&& !set_contains_borrowed_key(old(m)@, &value)
                &&& final(m)@ == old(m)@.insert(value)
            },
        }` |
| `std::thread::Result::flatten` | `match value {
            core::result::Result::Ok(inner) => result == inner,
            core::result::Result::Err(e) => result == core::result::Result::Err(e),
        }` |

## Semantic-gated candidates

127 of 127 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.
127 semantic-gated candidates have no semantic review holdback and form the accepted subset.
The machine-checkable accepted subset is written to `accepted_semantic_candidates.csv` and `accepted_semantic_candidates.json`; `final_candidates.csv` remains one row per API and includes raw model decisions.

| Target | Ensures |
|---|---|
| `alloc::collections::BTreeMap::append` | `final(m)@ == old(m)@.union_prefer_right(old(other)@); final(other)@ == Map::<Key, Value>::empty()` |
| `alloc::collections::BTreeMap::first_key_value` | `match result {
            Some((key, value)) => {
                &&& m@.contains_key(*key)
                &&& m@[*key] == *value
                &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                    (*key).cmp_spec(&other) != core::cmp::Ordering::Greater
                &&& *key == choose|candidate: Key| {
                    m@.contains_key(candidate)
                        && forall|other: Key| #[trigger] m@.contains_key(other) ==>
                            candidate.cmp_spec(&other) != core::cmp::Ordering::Greater
                }
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeMap::get_mut` | `{
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        }` |
| `alloc::collections::BTreeMap::last_key_value` | `match result {
            Some((k, v)) => {
                &&& *k == choose|max_key: Key| {
                    &&& m@.contains_key(max_key)
                    &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                        other.cmp_spec(&max_key) != core::cmp::Ordering::Greater
                }
                &&& m@.contains_key(*k)
                &&& m@[*k] == *v
                &&& forall|other: Key| #[trigger] m@.contains_key(other) ==>
                    other.cmp_spec(k) != core::cmp::Ordering::Greater
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeMap::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let k = choose|k: Key| {
                &&& old(m)@.contains_key(k)
                &&& forall|key: Key| #[trigger] old(m)@.contains_key(key) ==>
                    key == k || k.cmp_spec(&key) == core::cmp::Ordering::Less
            };
            &&& result == Some((k, old(m)@[k]))
            &&& final(m)@ == old(m)@.remove(k)
        }` |
| `alloc::collections::BTreeMap::pop_last` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let k = choose|k: Key|
                old(m)@.contains_key(k)
                && forall|other: Key| #![auto]
                    old(m)@.contains_key(other) ==> {
                        other.cmp_spec(&k) is Less || other == k
                    };
            &&& result == Some((k, old(m)@[k]))
            &&& final(m)@ == old(m)@.remove(k)
        }` |
| `alloc::collections::BTreeSet::append` | `final(m)@ == old(m)@.union(old(other)@); final(other)@ == vstd::set::Set::<Key>::empty()` |
| `alloc::collections::BTreeSet::first` | `match result {
            Some(v) => {
                &&& m@.contains(*v)
                &&& forall|other: Key| #[trigger] m@.contains(other) ==>
                    (*v).cmp_spec(&other) != core::cmp::Ordering::Greater
                &&& *v == choose|candidate: Key| {
                    m@.contains(candidate)
                        && forall|other: Key| #[trigger] m@.contains(other) ==>
                            candidate.cmp_spec(&other) != core::cmp::Ordering::Greater
                }
            },
            None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `alloc::collections::BTreeSet::is_subset` | `result == m@.subset_of(other@)` |
| `alloc::collections::BTreeSet::is_superset` | `result == other@.subset_of(m@)` |
| `alloc::collections::BTreeSet::last` | `match result {
            core::option::Option::Some(value) => {
                &&& !m@.is_empty()
                &&& *value == m@.find_unique_maximal(
                    |x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,
                )
                &&& m@.contains(*value)
                &&& forall|x: T| #[trigger] m@.contains(x) ==>
                    x.cmp_spec(value) != core::cmp::Ordering::Greater
            },
            core::option::Option::None => m@.is_empty(),
        }` |
| `alloc::collections::BTreeSet::pop_first` | `if old(m)@.is_empty() {
            &&& result is None
            &&& final(m)@ == old(m)@
        } else {
            let first = choose|candidate: T| {
                &&& old(m)@.contains(candidate)
                &&& forall|element: T| old(m)@.contains(element)
                    ==> candidate.cmp_spec(&element) != Ordering::Greater
            };
            &&& result == Some(first)
            &&& old(m)@.contains(first)
            &&& forall|element: T| old(m)@.contains(element)
                ==> first.cmp_spec(&element) != Ordering::Greater
            &&& final(m)@ == old(m)@.remove(first)
        }` |
| `alloc::collections::BTreeSet::pop_last` | `forall|v: Key| #![auto]
            result == Some(v) <==> old(m)@.contains(v)
                && forall|k: Key| #![auto]
                    old(m)@.contains(k) && k != v ==> k.cmp_spec(&v) is Less; (result is None) == old(m)@.is_empty(); match result {
            Some(v) => final(m)@ == old(m)@.remove(v),
            None => final(m)@ == old(m)@,
        }` |
| `alloc::collections::BTreeSet::replace` | `final(m)@ == old(m)@.insert(value); result == if old(m)@.contains(value) { Some(value) } else { None }` |
| `alloc::collections::LinkedList::back_mut` | `result is Some == (old(list)@.len() != 0); result is None == (old(list)@.len() == 0); result matches Some(value) ==> {
            &&& *value == old(list)@.last()
            &&& *final(value) == *value
            &&& final(list)@ == old(list)@
        }; result is None ==> final(list)@ == old(list)@` |
| `alloc::collections::VecDeque::binary_search` | `match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }` |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | `result@ == bytes@.drop_last()` |
| `alloc::string::String::as_bytes` | `res@ == encode_utf8(s@)` |
| `alloc::string::String::clear` | `final(s)@ == Seq::<char>::empty(); final(s).spec_capacity() == old(s).spec_capacity()` |
| `alloc::string::String::from_utf8_unchecked` | `forall|chars: vstd::prelude::Seq<char>|
            vstd::utf8::encode_utf8(chars) == bytes@ ==> res@ == chars` |
| `alloc::string::String::insert` | `final(s)@ == old(s)@.insert(
            choose |i: int| 0 <= i <= old(s)@.len()
                && encode_utf8(old(s)@.subrange(0, i)).len() == idx as nat,
            ch,
        )` |
| `alloc::string::String::insert_str` | `final(s)@ == vstd::utf8::decode_utf8(
            vstd::utf8::encode_utf8(old(s)@).take(idx as int)
                + vstd::utf8::encode_utf8(string@)
                + vstd::utf8::encode_utf8(old(s)@).skip(idx as int)
        )` |
| `alloc::string::String::into_bytes` | `res@ == vstd::utf8::encode_utf8(s@)` |
| `alloc::string::String::is_empty` | `result == (s@.len() == 0)` |
| `alloc::string::String::len` | `result as nat == encode_utf8(s@).len()` |
| `alloc::string::String::pop` | `old(s)@.len() == 0 ==> result == None && final(s)@ == old(s)@; old(s)@.len() > 0 ==> result == Some(old(s)@[old(s)@.len() - 1])
            && final(s)@ == old(s)@.drop_last()` |
| `alloc::string::String::push` | `final(s)@ == old(s)@.push(ch)` |
| `alloc::string::String::push_str` | `final(s)@ == old(s)@ + string@` |
| `alloc::string::String::remove` | `forall |i: int| #![trigger encode_utf8(old(s)@.subrange(0, i))]
            0 <= i < old(s)@.len()
            && idx as nat == encode_utf8(old(s)@.subrange(0, i)).len()
            ==> result == old(s)@[i]
                && final(s)@ == old(s)@.subrange(0, i)
                    + old(s)@.subrange(i + 1, old(s)@.len() as int)` |
| `alloc::string::String::replace_range` | `final(s)@ == string_replace_range_result(&range, encode_utf8(old(s)@), replace_with@)` |
| `alloc::string::String::split_off` | `forall |i: int| #![auto]
            0 <= i <= old(s)@.len()
                && vstd::utf8::encode_utf8(old(s)@.take(i)).len() == at as nat
            ==> final(s)@ == old(s)@.take(i)
                && result@ == old(s)@.skip(i); final(s).spec_capacity() == old(s).spec_capacity()` |
| `alloc::string::String::truncate` | `final(s)@ == if (new_len as nat) < encode_utf8(old(s)@).len() {
            old(s)@.take(choose |i: int| 0 <= i <= old(s)@.len()
                && encode_utf8(old(s)@.take(i)).len() == new_len as nat)
        } else {
            old(s)@
        }` |
| `alloc::vec::Vec::dedup` | `final(vec)@ == Seq::new(old(vec)@.len(), |i: int| i)
            .filter(|i: int| i == 0 || !old(vec)@[i].eq_spec(&old(vec)@[i - 1]))
            .map(|_j: int, i: int| old(vec)@[i])` |
| `alloc::vec::Vec::into_boxed_slice` | `slice@ == vec@` |
| `alloc::vec::Vec::into_flattened` | `result@ == Seq::new(vec@.len() * (N as nat), |k: int|
            (vec@[k / (N as int)])@[k % (N as int)])` |
| `core::array::as_mut_slice` | `out@ == old(ar)@; final(out)@ == out@; final(out)@ == final(ar)@` |
| `core::array::each_mut` | `forall|i: int| #![auto] 0 <= i < N ==> *out[i] == old(ar)@[i]; forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == *out[i]; forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == final(ar)@[i]` |
| `core::array::each_ref` | `forall|i: int| 0 <= i < N ==> *(out@[i]) == ar@[i]` |
| `core::array::from_mut` | `out@[0] == *old(s); final(out)@ == out@; *final(s) == final(out)@[0]` |
| `core::array::from_ref` | `out@ == seq![*s]` |
| `core::cmp::max` | `match v1.cmp_spec(&v2) {
            core::cmp::Ordering::Greater => r == v1,
            core::cmp::Ordering::Less | core::cmp::Ordering::Equal => r == v2,
        }` |
| `core::cmp::min` | `match v1.cmp_spec(&v2) {
            core::cmp::Ordering::Less => r == v1,
            core::cmp::Ordering::Equal => r == v1,
            core::cmp::Ordering::Greater => r == v2,
        }` |
| `core::convert::identity` | `ret == x` |
| `core::hint::black_box` | `output == dummy` |
| `core::hint::select_unpredictable` | `condition ==> result == true_val; !condition ==> result == false_val` |
| `core::mem::min_align_of` | `res == core::mem::align_of::<T>()` |
| `core::mem::min_align_of_val` | `res == core::mem::align_of_val(val)` |
| `core::mem::replace` | `res == *old(dest); *final(dest) == src` |
| `core::ops::Range::is_empty` | `ret == !r.start.is_lt(&r.end)` |
| `core::ops::RangeInclusive::into_inner` | `ret.0 == r@.start; ret.1 == r@.end` |
| `core::ops::RangeInclusive::is_empty` | `ret == (r@.exhausted || !r@.start.is_le(&r@.end))` |
| `core::option::Option::and` | `option.is_none() ==> res.is_none(); option.is_some() ==> res == optb` |
| `core::option::Option::flatten` | `res == match option {
            Some(inner) => inner,
            None => None,
        }` |
| `core::option::Option::or` | `option.is_some() ==> res == option; option.is_none() ==> res == optb` |
| `core::option::Option::replace` | `res == *old(option); *final(option) == core::option::Option::Some(value)` |
| `core::option::Option::transpose` | `res == match option { Some(Ok(x)) => Ok(Some(x)), Some(Err(e)) => Err(e), None => Ok(None) }` |
| `core::option::Option::unzip` | `option is Some ==> res.0 is Some && res.1 is Some && option->0 == (res.0->0, res.1->0); option is None ==> res.0 is None && res.1 is None` |
| `core::option::Option::xor` | `res == match (option, optb) { (Some(a), None) => Some(a), (None, Some(b)) => Some(b), _ => None }` |
| `core::option::Option::zip` | `res == match (option, other) {
            (core::option::Option::Some(a), core::option::Option::Some(b)) => core::option::Option::Some((a, b)),
            _ => core::option::Option::None,
        }` |
| `core::result::Result::and` | `result is Ok ==> and_result == res; result is Err ==> and_result is Err && and_result->Err_0 == result->Err_0` |
| `core::result::Result::expect_err` | `e == result->Err_0` |
| `core::result::Result::flatten` | `flattened == match result {
            core::result::Result::Ok(inner) => inner,
            core::result::Result::Err(e) => core::result::Result::Err(e),
        }` |
| `core::result::Result::or` | `result is Ok ==> or_result is Ok && or_result->Ok_0 == result->Ok_0; result is Err ==> or_result == res` |
| `core::result::Result::transpose` | `transposed == match result {
            core::result::Result::Ok(core::option::Option::Some(x)) => core::option::Option::Some(core::result::Result::Ok(x)),
            core::result::Result::Ok(core::option::Option::None) => core::option::Option::None,
            core::result::Result::Err(e) => core::option::Option::Some(core::result::Result::Err(e)),
        }` |
| `core::result::Result::unwrap_or` | `result is Ok ==> value == result->Ok_0; result is Err ==> value == default` |
| `core::slice::as_array` | `ret.is_some() <==> slice@.len() == N; ret.is_some() ==> ret.unwrap()@ == slice@` |
| `core::slice::as_chunks` | `{
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == slice@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == slice@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == slice@.len() / (N as nat)
            &&& ret.1@.len() == slice@.len() % (N as nat)
            &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len()
            &&& forall|i: int| 0 <= i < ret.0@.len() ==>
                (#[trigger] ret.0@[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                )
            &&& ret.1@ == slice@.subrange(
                ((slice@.len() / (N as nat)) * (N as nat)) as int,
                slice@.len() as int,
            )
        }` |
| `core::slice::as_chunks_mut` | `{
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == old(slice)@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == old(slice)@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == old(slice)@.len() / (N as nat)
            &&& ret.1@ == old(slice)@.subrange(
                ((old(slice)@.len() / (N as nat)) * (N as nat)) as int,
                old(slice)@.len() as int,
            )
            &&& final(ret.0)@ == ret.0@
            &&& final(ret.1)@ == ret.1@
            &&& final(slice)@ == old(slice)@
        }` |
| `core::slice::as_flattened` | `ret@.len() == slice@.len() * N; forall|i: int| 0 <= i < ret@.len() ==> ret@[i] == slice@[i / (N as int)][i % (N as int)]` |
| `core::slice::as_mut_array` | `ret is Some == (old(slice)@.len() == N); ret matches Some(out) ==> {
            &&& out@ == old(slice)@
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::as_rchunks` | `ret.0@ == slice@.subrange(
            0,
            (slice@.len() % (N as nat)) as int,
        ); ret.1@ == Seq::new(
            slice@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    (slice@.len() % (N as nat)) as int + i * (N as int),
                    (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ); forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == slice@.subrange(
                (slice@.len() % (N as nat)) as int + i * (N as int),
                (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
            )` |
| `core::slice::as_rchunks_mut` | `ret.0@ == old(slice)@.subrange(
            0,
            (old(slice)@.len() % (N as nat)) as int,
        ); ret.1@ == Seq::new(
            old(slice)@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == old(slice)@.subrange(
                    (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                    (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ); forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == old(slice)@.subrange(
                (old(slice)@.len() % (N as nat)) as int + i * (N as int),
                (old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int),
            ); final(ret.0)@ == ret.0@; final(ret.1)@ == ret.1@; final(slice)@ == old(slice)@` |
| `core::slice::binary_search` | `match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }` |
| `core::slice::contains` | `result <==> exists|i: int| 0 <= i < slice@.len() && slice@[i].eq_spec(x)` |
| `core::slice::eq_ignore_ascii_case` | `result == (
            slice@.len() == other@.len()
            && forall|i: int| 0 <= i < slice@.len() ==> {
                let a = (#[trigger] slice@[i]) as int;
                let b = other@[i] as int;
                a == b
                    || (65 <= a && a <= 90 && b == a + 32)
                    || (65 <= b && b <= 90 && a == b + 32)
            }
        )` |
| `core::slice::first_chunk` | `match ret {
            Option::Some(chunk) =>
                slice@.len() >= N && chunk@ == slice@.subrange(0, N as int),
            Option::None => slice@.len() < N,
        }` |
| `core::slice::first_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(0, N as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == final(out)@ + old(slice)@.subrange(N as int, old(slice)@.len() as int)
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::from_mut` | `ret@ == seq![*old(s)]; final(ret)@ == ret@; final(ret)@ == seq![*final(s)]; *final(s) == *old(s)` |
| `core::slice::from_ref` | `result@ == seq![*s]` |
| `core::slice::is_ascii` | `ret == (forall|i: int| 0 <= i < slice@.len() ==> slice@[i] <= 0x7f)` |
| `core::slice::is_sorted` | `result <==> forall|i: int|
            0 <= i && i + 1 < slice@.len()
                ==> (#[trigger] slice@[i]).is_le(&slice@[i + 1])` |
| `core::slice::last_chunk` | `ret.is_some() <==> N <= slice.len(); ret.is_some() ==> ret.unwrap()@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int)` |
| `core::slice::last_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some(out) ==> {
            &&& out@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(out)@ == out@
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - N as int) + final(out)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::reverse` | `final(slice)@ == old(slice)@.reverse()` |
| `core::slice::split_at_checked` | `ret is Some == (mid <= slice.len()); ret matches Some((left, right)) ==> {
            &&& left@ == slice@.subrange(0, mid as int)
            &&& right@ == slice@.subrange(mid as int, slice@.len() as int)
        }` |
| `core::slice::split_at_mut_checked` | `ret is Some == (mid <= old(slice)@.len()); ret matches Some((left, right)) ==> {
            &&& left@ == old(slice)@.subrange(0, mid as int)
            &&& right@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            &&& final(left)@ == left@
            &&& final(right)@ == right@
            &&& final(slice)@ == final(left)@ + final(right)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_at_mut_unchecked` | `ret.0@ == old(slice)@.subrange(0, mid as int); ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int); final(ret.0)@ == ret.0@; final(ret.1)@ == ret.1@; final(slice)@ == final(ret.0)@ + final(ret.1)@` |
| `core::slice::split_first` | `ret.is_some() == (slice@.len() > 0); match ret {
            Some((first, tail)) =>
                *first == slice@[0]
                && tail@ == slice@.subrange(1, slice@.len() as int),
            None => true,
        }` |
| `core::slice::split_first_chunk` | `ret.is_some() <==> N <= slice.len(); ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, N as int); ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int)` |
| `core::slice::split_first_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some((first, tail)) ==> {
            &&& first@ == old(slice)@.subrange(0, N as int)
            &&& tail@ == old(slice)@.subrange(N as int, old(slice)@.len() as int)
            &&& final(first)@ == first@
            &&& final(tail)@ == tail@
            &&& final(slice)@ == final(first)@ + final(tail)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_first_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some((first, tail)) ==> {
            &&& *first == old(slice)@[0]
            &&& tail@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& *final(first) == *first
            &&& final(tail)@ == tail@
            &&& final(slice)@ == seq![*final(first)] + final(tail)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_last` | `ret.is_some() == (slice@.len() > 0); ret.is_some() ==> *ret.unwrap().0 == slice@[slice@.len() - 1]; ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(0, slice@.len() - 1)` |
| `core::slice::split_last_chunk` | `ret matches Some(_) <==> N <= slice@.len(); ret matches Some(parts) ==> parts.0@ == slice@.subrange(0, slice@.len() - N as int); ret matches Some(parts) ==> parts.1@ == slice@.subrange(slice@.len() - N as int, slice@.len() as int)` |
| `core::slice::split_last_chunk_mut` | `ret is Some == (N as int <= old(slice)@.len()); ret matches Some((init, last)) ==> {
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - N as int)
            &&& last@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int)
            &&& final(init)@ == init@
            &&& final(last)@ == last@
            &&& final(slice)@ == final(init)@ + final(last)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_last_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some((last, init)) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& *final(last) == *last
            &&& final(init)@ == init@
            &&& final(slice)@ == final(init)@ + seq![*final(last)]
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_off_first` | `ret.is_none() == (old(slice)@.len() == 0); ret.is_some() ==> *ret.unwrap() == old(slice)@[0]; old(slice)@.len() == 0 ==> final(slice)@ == old(slice)@; old(slice)@.len() > 0 ==> final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int)` |
| `core::slice::split_off_first_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some(first) ==> {
            &&& *first == old(slice)@[0]
            &&& *final(first) == *first
            &&& final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            &&& old(slice)@ == seq![*final(first)] + final(slice)@
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::split_off_last_mut` | `ret is Some == (old(slice)@.len() != 0); ret matches Some(last) ==> {
            &&& *last == old(slice)@[(old(slice)@.len() - 1) as int]
            &&& *final(last) == *last
            &&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
            &&& old(slice)@ == final(slice)@ + seq![*final(last)]
        }; ret is None ==> final(slice)@ == old(slice)@` |
| `core::slice::starts_with` | `ret <==> (
            needle@.len() <= slice@.len()
            && forall|i: int| 0 <= i < needle@.len() ==> slice@[i].eq_spec(&needle@[i])
        )` |
| `core::slice::trim_ascii` | `exists|start: int, end: int| {
            &&& 0 <= start <= end <= slice@.len()
            &&& r@ == slice@.subrange(start, end)
            &&& (forall|i: int| 0 <= i < start ==> spec_is_ascii_whitespace(slice@[i]))
            &&& (forall|i: int| end <= i < slice@.len() ==> spec_is_ascii_whitespace(slice@[i]))
            &&& (start < end ==> !spec_is_ascii_whitespace(slice@[start]))
            &&& (start < end ==> !spec_is_ascii_whitespace(slice@[end - 1]))
        }` |
| `core::slice::trim_ascii_end` | `result@ == slice@.subrange(0, result@.len() as int); result@.len() <= slice@.len(); forall|i: int| result@.len() <= i < slice@.len() ==> {
            let byte = #[trigger] slice@[i];
            byte == 0x09 || byte == 0x0a || byte == 0x0c || byte == 0x0d || byte == 0x20
        }; result@.len() > 0 ==> {
            let byte = result@[(result@.len() - 1) as int];
            !(byte == 0x09 || byte == 0x0a || byte == 0x0c || byte == 0x0d || byte == 0x20)
        }` |
| `core::slice::trim_ascii_start` | `exists|start: int|
            0 <= start <= slice@.len()
            && (forall|i: int| 0 <= i < start ==> (
                slice@[i] == 0x09u8
                || slice@[i] == 0x0au8
                || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8
                || slice@[i] == 0x20u8
            ))
            && (start == slice@.len() || (
                slice@[start] != 0x09u8
                && slice@[start] != 0x0au8
                && slice@[start] != 0x0cu8
                && slice@[start] != 0x0du8
                && slice@[start] != 0x20u8
            ))
            && ret@ == slice@.subrange(start, slice@.len() as int)` |
| `core::str::ceil_char_boundary` | `result <= s.len(); index >= s.len() ==> result == s.len(); index < s.len() ==> index <= result; s.is_char_boundary(result); forall|i: usize| index <= i && i < result ==> !s.is_char_boundary(i)` |
| `core::str::eq_ignore_ascii_case` | `result == (s.spec_bytes().len() == other.spec_bytes().len() && forall|i: int| 0 <= i < s.spec_bytes().len() ==> (if 65 <= s.spec_bytes()[i] && s.spec_bytes()[i] <= 90 { (s.spec_bytes()[i] as int) + 32 } else { s.spec_bytes()[i] as int }) == (if 65 <= other.spec_bytes()[i] && other.spec_bytes()[i] <= 90 { (other.spec_bytes()[i] as int) + 32 } else { other.spec_bytes()[i] as int }))` |
| `core::str::floor_char_boundary` | `result <= index; result <= s.spec_bytes().len(); s.is_char_boundary(result); forall|i: usize| result < i && i <= index ==> !s.is_char_boundary(i)` |
| `core::str::from_utf8` | `valid_utf8(v@) ==> (result matches Ok(string) && string@ == decode_utf8(v@)); !valid_utf8(v@) ==> result is Err` |
| `core::str::from_utf8_mut` | `final(v)@ == old(v)@; valid_utf8(old(v)@) ==> (result matches Ok(string) && string@ == decode_utf8(old(v)@)); !valid_utf8(old(v)@) ==> result is Err` |
| `core::str::make_ascii_lowercase` | `final(s).spec_bytes().len() == old(s).spec_bytes().len(); forall|i: int| 0 <= i < old(s).spec_bytes().len() ==> #[trigger] final(s).spec_bytes()[i] as int
            == if 0x41u8 <= old(s).spec_bytes()[i] && old(s).spec_bytes()[i] <= 0x5au8 {
                old(s).spec_bytes()[i] as int + 32
            } else {
                old(s).spec_bytes()[i] as int
            }` |
| `core::str::make_ascii_uppercase` | `final(s).spec_bytes().len() == old(s).spec_bytes().len(); forall|i: int| 0 <= i < old(s).spec_bytes().len() ==>
            final(s).spec_bytes()[i] as int == if 0x61u8 <= old(s).spec_bytes()[i] && old(s).spec_bytes()[i] <= 0x7au8 {
                old(s).spec_bytes()[i] as int - 0x20int
            } else {
                old(s).spec_bytes()[i] as int
            }` |
| `core::str::split_at_checked` | `ret.is_some() == is_char_boundary(s.spec_bytes(), mid as int); ret.is_some() ==> ret.unwrap().0.spec_bytes() == s.spec_bytes().subrange(0, mid as int); ret.is_some() ==> ret.unwrap().1.spec_bytes() == s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int)` |
| `core::str::split_at_mut_checked` | `ret is Some <==> is_char_boundary(old(s).spec_bytes(), mid as int); ret matches Some((left, right)) ==> {
            &&& left.spec_bytes() =~= old(s).spec_bytes().subrange(0, mid as int)
            &&& right.spec_bytes() =~= old(s).spec_bytes().subrange(mid as int, old(s).spec_bytes().len() as int)
            &&& final(left).spec_bytes() == left.spec_bytes()
            &&& final(right).spec_bytes() == right.spec_bytes()
            &&& final(s).spec_bytes() == final(left).spec_bytes() + final(right).spec_bytes()
        }; ret is None ==> final(s).spec_bytes() == old(s).spec_bytes()` |
| `core::str::trim` | `result@ == ({
            let bounds = choose|bounds: (int, int)|
                0 <= bounds.0
                && bounds.0 <= bounds.1
                && bounds.1 <= s@.len()
                && (forall|i: int| 0 <= i < bounds.0 ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (forall|i: int| bounds.1 <= i < s@.len() ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.0]))
                && (bounds.0 == bounds.1 || !str_unicode_white_space(s@[bounds.1 - 1]));
            s@.subrange(bounds.0, bounds.1)
        })` |
| `core::str::trim_ascii` | `result@ == ({
            let bounds = choose|bounds: (int, int)|
                0 <= bounds.0
                && bounds.0 <= bounds.1
                && bounds.1 <= s@.len()
                && (forall|i: int| 0 <= i < bounds.0 ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (forall|i: int| bounds.1 <= i < s@.len() ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (bounds.0 < bounds.1 ==> !(s@[bounds.0] == ' ' || s@[bounds.0] == '\t' || s@[bounds.0] == '\n' || s@[bounds.0] == '\x0c' || s@[bounds.0] == '\r'))
                && (bounds.0 < bounds.1 ==> !(s@[bounds.1 - 1] == ' ' || s@[bounds.1 - 1] == '\t' || s@[bounds.1 - 1] == '\n' || s@[bounds.1 - 1] == '\x0c' || s@[bounds.1 - 1] == '\r'));
            s@.subrange(bounds.0, bounds.1)
        })` |
| `core::str::trim_ascii_end` | `result@ == s@.subrange(0, result@.len() as int); result@.len() <= s@.len(); forall|i: int| result@.len() <= i < s@.len() ==> {
            let c = #[trigger] s@[i];
            c == ' ' || c == '\t' || c == '\n' || c == '\x0c' || c == '\r'
        }; result@.len() > 0 ==> {
            let c = result@[(result@.len() - 1) as int];
            !(c == ' ' || c == '\t' || c == '\n' || c == '\x0c' || c == '\r')
        }` |
| `core::str::trim_ascii_start` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==> (s@[i] == ' ' || s@[i] == '\t' || s@[i] == '\n' || s@[i] == '\x0c' || s@[i] == '\r'))
                && (start == s@.len() || !(s@[start] == ' ' || s@[start] == '\t' || s@[start] == '\n' || s@[start] == '\x0c' || s@[start] == '\r'));
            s@.subrange(start, s@.len() as int)
        })` |
| `core::str::trim_end` | `result@ == s@.subrange(0, result@.len() as int); result@.len() <= s@.len(); forall|i: int| result@.len() <= i < s@.len() ==> {
            let c = #[trigger] s@[i];
            str_unicode_white_space(c)
        }; result@.len() > 0 ==> {
            let c = result@[(result@.len() - 1) as int];
            !str_unicode_white_space(c)
        }` |
| `core::str::trim_left` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (start == s@.len() || !str_unicode_white_space(s@[start]));
            s@.subrange(start, s@.len() as int)
        })` |
| `core::str::trim_right` | `result@.len() <= s@.len(); result@ == s@.take(result@.len() as int); forall|i: int| result@.len() <= i < s@.len() ==> (
            s@[i] == '\u{9}' || s@[i] == '\u{a}' || s@[i] == '\u{b}' || s@[i] == '\u{c}' || s@[i] == '\u{d}' ||
            s@[i] == '\u{20}' || s@[i] == '\u{85}' || s@[i] == '\u{a0}' || s@[i] == '\u{1680}' ||
            s@[i] == '\u{2000}' || s@[i] == '\u{2001}' || s@[i] == '\u{2002}' || s@[i] == '\u{2003}' ||
            s@[i] == '\u{2004}' || s@[i] == '\u{2005}' || s@[i] == '\u{2006}' || s@[i] == '\u{2007}' ||
            s@[i] == '\u{2008}' || s@[i] == '\u{2009}' || s@[i] == '\u{200a}' || s@[i] == '\u{2028}' ||
            s@[i] == '\u{2029}' || s@[i] == '\u{202f}' || s@[i] == '\u{205f}' || s@[i] == '\u{3000}'
        ); result@.len() == 0 || !(
            result@[result@.len() - 1] == '\u{9}' || result@[result@.len() - 1] == '\u{a}' ||
            result@[result@.len() - 1] == '\u{b}' || result@[result@.len() - 1] == '\u{c}' ||
            result@[result@.len() - 1] == '\u{d}' || result@[result@.len() - 1] == '\u{20}' ||
            result@[result@.len() - 1] == '\u{85}' || result@[result@.len() - 1] == '\u{a0}' ||
            result@[result@.len() - 1] == '\u{1680}' || result@[result@.len() - 1] == '\u{2000}' ||
            result@[result@.len() - 1] == '\u{2001}' || result@[result@.len() - 1] == '\u{2002}' ||
            result@[result@.len() - 1] == '\u{2003}' || result@[result@.len() - 1] == '\u{2004}' ||
            result@[result@.len() - 1] == '\u{2005}' || result@[result@.len() - 1] == '\u{2006}' ||
            result@[result@.len() - 1] == '\u{2007}' || result@[result@.len() - 1] == '\u{2008}' ||
            result@[result@.len() - 1] == '\u{2009}' || result@[result@.len() - 1] == '\u{200a}' ||
            result@[result@.len() - 1] == '\u{2028}' || result@[result@.len() - 1] == '\u{2029}' ||
            result@[result@.len() - 1] == '\u{202f}' || result@[result@.len() - 1] == '\u{205f}' ||
            result@[result@.len() - 1] == '\u{3000}'
        )` |
| `core::str::trim_start` | `result@ == ({
            let start = choose|start: int|
                0 <= start
                && start <= s@.len()
                && (forall|i: int| 0 <= i < start ==>
                    #[trigger] str_unicode_white_space(s@[i]))
                && (start == s@.len() || !str_unicode_white_space(s@[start]));
            s@.subrange(start, s@.len() as int)
        })` |
| `std::collections::HashMap::get_mut` | `{
            let old_map = old(m)@;
            let selected_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &selected_key)
            &&& result is Some == contains_borrowed_key(old_map, k)
            &&& match result {
                Some(v) => {
                    &&& *v == old_map[selected_key]
                    &&& *final(v) == *v
                    &&& final(m)@ == old_map
                },
                None => {
                    &&& !contains_borrowed_key(old_map, k)
                    &&& final(m)@ == old_map
                },
            }
        }` |
| `std::collections::HashMap::remove_entry` | `{
            let old_map = old(m)@;
            let removed_key = choose|key: Key|
                sets_borrowed_key_to_key(old_map.dom(), k, &key);
            &&& contains_borrowed_key(old_map, k) ==>
                sets_borrowed_key_to_key(old_map.dom(), k, &removed_key)
            &&& result == if contains_borrowed_key(old_map, k) {
                Some((removed_key, old_map[removed_key]))
            } else {
                None
            }
            &&& final(m)@ == if contains_borrowed_key(old_map, k) {
                old_map.remove(removed_key)
            } else {
                old_map
            }
        }` |
| `std::collections::HashSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `std::collections::HashSet::is_subset` | `result == m@.subset_of(other@)` |
| `std::collections::HashSet::is_superset` | `result == other@.subset_of(m@)` |
| `std::collections::HashSet::replace` | `match result {
            Some(replaced) => {
                &&& sets_borrowed_key_to_key(old(m)@, &value, &replaced)
                &&& final(m)@ == old(m)@.remove(replaced).insert(value)
            },
            None => {
                &&& !set_contains_borrowed_key(old(m)@, &value)
                &&& final(m)@ == old(m)@.insert(value)
            },
        }` |
| `std::thread::Result::flatten` | `match value {
            core::result::Result::Ok(inner) => result == inner,
            core::result::Result::Err(e) => result == core::result::Result::Err(e),
        }` |

## Accepted requires source-fidelity audit

47 semantic-gated candidate rows with non-empty `requires` were audited against classified-manifest declaration/source_context evidence and Rust/vstd semantic laws before acceptance.

| Target | Classification | Source |
|---|---|---|
| `alloc::collections::BTreeMap::append` | `source_justified` | `alloc/src/collections/btree/map.rs:1236` |
| `alloc::collections::BTreeMap::first_key_value` | `source_justified` | `alloc/src/collections/btree/map.rs:810` |
| `alloc::collections::BTreeMap::get_mut` | `source_justified` | `alloc/src/collections/btree/map.rs:1006` |
| `alloc::collections::BTreeMap::last_key_value` | `source_justified` | `alloc/src/collections/btree/map.rs:893` |
| `alloc::collections::BTreeMap::pop_first` | `source_justified` | `alloc/src/collections/btree/map.rs:872` |
| `alloc::collections::BTreeMap::pop_last` | `source_justified` | `alloc/src/collections/btree/map.rs:955` |
| `alloc::collections::BTreeSet::append` | `source_justified` | `alloc/src/collections/btree/set.rs:1139` |
| `alloc::collections::BTreeSet::first` | `source_justified` | `alloc/src/collections/btree/set.rs:792` |
| `alloc::collections::BTreeSet::is_disjoint` | `source_justified` | `alloc/src/collections/btree/set.rs:658` |
| `alloc::collections::BTreeSet::is_subset` | `source_justified` | `alloc/src/collections/btree/set.rs:684` |
| `alloc::collections::BTreeSet::is_superset` | `source_justified` | `alloc/src/collections/btree/set.rs:765` |
| `alloc::collections::BTreeSet::last` | `source_justified` | `alloc/src/collections/btree/set.rs:819` |
| `alloc::collections::BTreeSet::pop_first` | `source_justified` | `alloc/src/collections/btree/set.rs:843` |
| `alloc::collections::BTreeSet::pop_last` | `source_justified` | `alloc/src/collections/btree/set.rs:867` |
| `alloc::collections::BTreeSet::replace` | `source_justified` | `alloc/src/collections/btree/set.rs:924` |
| `alloc::collections::VecDeque::binary_search` | `source_justified` | `alloc/src/collections/vec_deque/mod.rs:3201` |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | `source_justified` | `alloc/src/ffi/c_str.rs:635` |
| `alloc::string::String::from_utf8_unchecked` | `source_justified` | `alloc/src/string.rs:1018` |
| `alloc::string::String::insert` | `source_justified` | `alloc/src/string.rs:1731` |
| `alloc::string::String::insert_str` | `source_justified` | `alloc/src/string.rs:1788` |
| `alloc::string::String::remove` | `source_justified` | `alloc/src/string.rs:1535` |
| `alloc::string::String::replace_range` | `source_justified` | `alloc/src/string.rs:2080` |
| `alloc::string::String::split_off` | `source_justified` | `alloc/src/string.rs:1917` |
| `alloc::string::String::truncate` | `source_justified` | `alloc/src/string.rs:1478` |
| `alloc::vec::Vec::dedup` | `source_justified` | `alloc/src/vec/mod.rs:3704` |
| `alloc::vec::Vec::into_flattened` | `source_justified` | `alloc/src/vec/mod.rs:3633` |
| `core::cmp::max` | `source_justified` | `core/src/cmp.rs:1681` |
| `core::cmp::min` | `source_justified` | `core/src/cmp.rs:1574` |
| `core::ops::Range::is_empty` | `source_justified` | `core/src/ops/range.rs:151` |
| `core::ops::RangeInclusive::is_empty` | `source_justified` | `core/src/ops/range.rs:559` |
| `core::result::Result::expect_err` | `source_justified` | `core/src/result.rs:1291` |
| `core::slice::as_chunks` | `source_justified` | `core/src/slice/mod.rs:1399` |
| `core::slice::as_chunks_mut` | `source_justified` | `core/src/slice/mod.rs:1555` |
| `core::slice::as_flattened` | `source_justified` | `core/src/slice/mod.rs:5451` |
| `core::slice::as_rchunks` | `source_justified` | `core/src/slice/mod.rs:1446` |
| `core::slice::as_rchunks_mut` | `source_justified` | `core/src/slice/mod.rs:1608` |
| `core::slice::binary_search` | `source_justified` | `core/src/slice/mod.rs:2925` |
| `core::slice::contains` | `source_justified` | `core/src/slice/mod.rs:2594` |
| `core::slice::is_sorted` | `source_justified` | `core/src/slice/mod.rs:4735` |
| `core::slice::split_at_mut_unchecked` | `source_justified` | `core/src/slice/mod.rs:2095` |
| `core::slice::starts_with` | `source_justified` | `core/src/slice/mod.rs:2624` |
| `std::collections::HashMap::get_mut` | `source_justified` | `std/src/collections/hash/map.rs:1297` |
| `std::collections::HashMap::remove_entry` | `source_justified` | `std/src/collections/hash/map.rs:1420` |
| `std::collections::HashSet::is_disjoint` | `source_justified` | `std/src/collections/hash/set.rs:955` |
| `std::collections::HashSet::is_subset` | `source_justified` | `std/src/collections/hash/set.rs:981` |
| `std::collections::HashSet::is_superset` | `source_justified` | `std/src/collections/hash/set.rs:1007` |
| `std::collections::HashSet::replace` | `source_justified` | `std/src/collections/hash/set.rs:1056` |

## Accepted ensures source-fidelity audit

127 accepted semantic candidate rows were audited against classified-manifest declaration/source_context evidence and Rust/vstd semantic laws. Model rationale text is not used as source evidence.

| Target | Classification | Evidence | Source |
|---|---|---|---|
| `alloc::collections::BTreeMap::append` | `source_justified` | `exact_btree_raw_algebra_source_gate` | `alloc/src/collections/btree/map.rs:1236` |
| `alloc::collections::BTreeMap::first_key_value` | `source_justified` | `btree_map_declaration_source_context` | `alloc/src/collections/btree/map.rs:810` |
| `alloc::collections::BTreeMap::get_mut` | `source_justified` | `exact_map_get_mut_source_gate` | `alloc/src/collections/btree/map.rs:1006` |
| `alloc::collections::BTreeMap::last_key_value` | `source_justified` | `btree_map_declaration_source_context` | `alloc/src/collections/btree/map.rs:893` |
| `alloc::collections::BTreeMap::pop_first` | `source_justified` | `btree_map_declaration_source_context` | `alloc/src/collections/btree/map.rs:872` |
| `alloc::collections::BTreeMap::pop_last` | `source_justified` | `btree_map_declaration_source_context` | `alloc/src/collections/btree/map.rs:955` |
| `alloc::collections::BTreeSet::append` | `source_justified` | `exact_btree_raw_algebra_source_gate` | `alloc/src/collections/btree/set.rs:1139` |
| `alloc::collections::BTreeSet::first` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:792` |
| `alloc::collections::BTreeSet::is_disjoint` | `source_justified` | `exact_btree_raw_algebra_source_gate` | `alloc/src/collections/btree/set.rs:658` |
| `alloc::collections::BTreeSet::is_subset` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:684` |
| `alloc::collections::BTreeSet::is_superset` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:765` |
| `alloc::collections::BTreeSet::last` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:819` |
| `alloc::collections::BTreeSet::pop_first` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:843` |
| `alloc::collections::BTreeSet::pop_last` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:867` |
| `alloc::collections::BTreeSet::replace` | `source_justified` | `btree_set_declaration_source_context` | `alloc/src/collections/btree/set.rs:924` |
| `alloc::collections::LinkedList::back_mut` | `source_justified` | `exact_linkedlist_back_mut_source_gate` | `alloc/src/collections/linked_list.rs:824` |
| `alloc::collections::VecDeque::binary_search` | `source_justified` | `exact_binary_search_source_gate` | `alloc/src/collections/vec_deque/mod.rs:3201` |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | `source_justified` | `exact_unsafe_constructor_source_gate` | `alloc/src/ffi/c_str.rs:635` |
| `alloc::string::String::as_bytes` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1450` |
| `alloc::string::String::clear` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1941` |
| `alloc::string::String::from_utf8_unchecked` | `source_justified` | `exact_unsafe_constructor_source_gate` | `alloc/src/string.rs:1018` |
| `alloc::string::String::insert` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1731` |
| `alloc::string::String::insert_str` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1788` |
| `alloc::string::String::into_bytes` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1039` |
| `alloc::string::String::is_empty` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1885` |
| `alloc::string::String::len` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1865` |
| `alloc::string::String::pop` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1502` |
| `alloc::string::String::push` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1421` |
| `alloc::string::String::push_str` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1106` |
| `alloc::string::String::remove` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1535` |
| `alloc::string::String::replace_range` | `source_justified` | `exact_string_replace_range_source_gate` | `alloc/src/string.rs:2080` |
| `alloc::string::String::split_off` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1917` |
| `alloc::string::String::truncate` | `source_justified` | `string_declaration_source_context` | `alloc/src/string.rs:1478` |
| `alloc::vec::Vec::dedup` | `source_justified` | `vec_declaration_source_context` | `alloc/src/vec/mod.rs:3704` |
| `alloc::vec::Vec::into_boxed_slice` | `source_justified` | `vec_declaration_source_context` | `alloc/src/vec/mod.rs:1731` |
| `alloc::vec::Vec::into_flattened` | `source_justified` | `vec_declaration_source_context` | `alloc/src/vec/mod.rs:3633` |
| `core::array::as_mut_slice` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/array/mod.rs:658` |
| `core::array::each_mut` | `source_justified` | `exact_array_each_mut_source_gate` | `core/src/array/mod.rs:719` |
| `core::array::each_ref` | `source_justified` | `array_declaration_source_context` | `core/src/array/mod.rs:688` |
| `core::array::from_mut` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/array/mod.rs:175` |
| `core::array::from_ref` | `source_justified` | `array_declaration_source_context` | `core/src/array/mod.rs:167` |
| `core::cmp::max` | `source_justified` | `cmp_min_max_source_context` | `core/src/cmp.rs:1681` |
| `core::cmp::min` | `source_justified` | `cmp_min_max_source_context` | `core/src/cmp.rs:1574` |
| `core::convert::identity` | `source_justified` | `identity_like_declaration_source_context` | `core/src/convert/mod.rs:106` |
| `core::hint::black_box` | `source_justified` | `identity_like_declaration_source_context` | `core/src/hint.rs:490` |
| `core::hint::select_unpredictable` | `source_justified` | `select_unpredictable_declaration_source_context` | `core/src/hint.rs:832` |
| `core::mem::min_align_of` | `source_justified` | `mem_align_declaration_source_context` | `core/src/mem/mod.rs:489` |
| `core::mem::min_align_of_val` | `source_justified` | `mem_align_declaration_source_context` | `core/src/mem/mod.rs:512` |
| `core::mem::replace` | `source_justified` | `mem_replace_declaration_source_context` | `core/src/mem/mod.rs:954` |
| `core::ops::Range::is_empty` | `source_justified` | `range_declaration_source_context` | `core/src/ops/range.rs:151` |
| `core::ops::RangeInclusive::into_inner` | `source_justified` | `range_inclusive_declaration_source_context` | `core/src/ops/range.rs:457` |
| `core::ops::RangeInclusive::is_empty` | `source_justified` | `range_inclusive_declaration_source_context` | `core/src/ops/range.rs:559` |
| `core::option::Option::and` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:1493` |
| `core::option::Option::flatten` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:2937` |
| `core::option::Option::or` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:1617` |
| `core::option::Option::replace` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:1958` |
| `core::option::Option::transpose` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:2237` |
| `core::option::Option::unzip` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:2110` |
| `core::option::Option::xor` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:1680` |
| `core::option::Option::zip` | `source_justified` | `option_declaration_source_context` | `core/src/option.rs:1979` |
| `core::result::Result::and` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1440` |
| `core::result::Result::expect_err` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1291` |
| `core::result::Result::flatten` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1855` |
| `core::result::Result::or` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1526` |
| `core::result::Result::transpose` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1819` |
| `core::result::Result::unwrap_or` | `source_justified` | `result_declaration_source_context` | `core/src/result.rs:1588` |
| `core::slice::as_array` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:853` |
| `core::slice::as_chunks` | `source_justified` | `slice_chunk_source_context` | `core/src/slice/mod.rs:1399` |
| `core::slice::as_chunks_mut` | `source_justified` | `slice_chunk_source_context` | `core/src/slice/mod.rs:1555` |
| `core::slice::as_flattened` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:5451` |
| `core::slice::as_mut_array` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/slice/mod.rs:872` |
| `core::slice::as_rchunks` | `source_justified` | `slice_chunk_source_context` | `core/src/slice/mod.rs:1446` |
| `core::slice::as_rchunks_mut` | `source_justified` | `slice_chunk_source_context` | `core/src/slice/mod.rs:1608` |
| `core::slice::binary_search` | `source_justified` | `exact_binary_search_source_gate` | `core/src/slice/mod.rs:2925` |
| `core::slice::contains` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:2594` |
| `core::slice::eq_ignore_ascii_case` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/ascii.rs:60` |
| `core::slice::first_chunk` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:327` |
| `core::slice::first_chunk_mut` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/slice/mod.rs:357` |
| `core::slice::from_mut` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/slice/raw.rs:211` |
| `core::slice::from_ref` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/raw.rs:203` |
| `core::slice::is_ascii` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/ascii.rs:18` |
| `core::slice::is_sorted` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:4735` |
| `core::slice::last_chunk` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:509` |
| `core::slice::last_chunk_mut` | `source_justified` | `exact_direct_mut_view_adapter_source_gate` | `core/src/slice/mod.rs:539` |
| `core::slice::reverse` | `source_justified` | `exact_mutating_slice_source_gate` | `core/src/slice/mod.rs:981` |
| `core::slice::split_at_checked` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:2156` |
| `core::slice::split_at_mut_checked` | `source_justified` | `exact_slice_split_at_mut_checked_source_gate` | `core/src/slice/mod.rs:2195` |
| `core::slice::split_at_mut_unchecked` | `source_justified` | `exact_split_at_mut_unchecked_source_gate` | `core/src/slice/mod.rs:2095` |
| `core::slice::split_first` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:198` |
| `core::slice::split_first_chunk` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:387` |
| `core::slice::split_first_chunk_mut` | `source_justified` | `exact_option_mut_tuple_view_source_gate` | `core/src/slice/mod.rs:417` |
| `core::slice::split_first_mut` | `source_justified` | `exact_single_element_mut_split_source_gate` | `core/src/slice/mod.rs:220` |
| `core::slice::split_last` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:240` |
| `core::slice::split_last_chunk` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:447` |
| `core::slice::split_last_chunk_mut` | `source_justified` | `exact_option_mut_tuple_view_source_gate` | `core/src/slice/mod.rs:478` |
| `core::slice::split_last_mut` | `source_justified` | `exact_single_element_mut_split_source_gate` | `core/src/slice/mod.rs:262` |
| `core::slice::split_off_first` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:5017` |
| `core::slice::split_off_first_mut` | `source_justified` | `exact_single_element_mut_split_source_gate` | `core/src/slice/mod.rs:5042` |
| `core::slice::split_off_last_mut` | `source_justified` | `exact_single_element_mut_split_source_gate` | `core/src/slice/mod.rs:5092` |
| `core::slice::starts_with` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/mod.rs:2624` |
| `core::slice::trim_ascii` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/ascii.rs:308` |
| `core::slice::trim_ascii_end` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/ascii.rs:274` |
| `core::slice::trim_ascii_start` | `source_justified` | `slice_declaration_source_context` | `core/src/slice/ascii.rs:241` |
| `core::str::ceil_char_boundary` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:480` |
| `core::str::eq_ignore_ascii_case` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2859` |
| `core::str::floor_char_boundary` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:423` |
| `core::str::from_utf8` | `source_justified` | `exact_str_from_utf8_source_gate` | `core/src/str/mod.rs:252` |
| `core::str::from_utf8_mut` | `source_justified` | `exact_str_from_utf8_mut_source_gate` | `core/src/str/mod.rs:285` |
| `core::str::make_ascii_lowercase` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2966` |
| `core::str::make_ascii_uppercase` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2938` |
| `core::str::split_at_checked` | `source_justified` | `exact_str_split_at_checked_source_gate` | `core/src/str/mod.rs:940` |
| `core::str::split_at_mut_checked` | `source_justified` | `exact_str_split_at_mut_checked_source_gate` | `core/src/str/mod.rs:981` |
| `core::str::trim` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2186` |
| `core::str::trim_ascii` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:3051` |
| `core::str::trim_ascii_end` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:3022` |
| `core::str::trim_ascii_start` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2994` |
| `core::str::trim_end` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2264` |
| `core::str::trim_left` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2304` |
| `core::str::trim_right` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2344` |
| `core::str::trim_start` | `source_justified` | `str_declaration_source_context` | `core/src/str/mod.rs:2225` |
| `std::collections::HashMap::get_mut` | `source_justified` | `exact_map_get_mut_source_gate` | `std/src/collections/hash/map.rs:1297` |
| `std::collections::HashMap::remove_entry` | `source_justified` | `hashmap_remove_entry_source_context` | `std/src/collections/hash/map.rs:1420` |
| `std::collections::HashSet::is_disjoint` | `source_justified` | `hashset_declaration_source_context` | `std/src/collections/hash/set.rs:955` |
| `std::collections::HashSet::is_subset` | `source_justified` | `hashset_declaration_source_context` | `std/src/collections/hash/set.rs:981` |
| `std::collections::HashSet::is_superset` | `source_justified` | `hashset_declaration_source_context` | `std/src/collections/hash/set.rs:1007` |
| `std::collections::HashSet::replace` | `source_justified` | `exact_hashset_replace_source_gate` | `std/src/collections/hash/set.rs:1056` |
| `std::thread::Result::flatten` | `source_justified` | `exact_thread_result_flatten_source_gate` | `core/src/result.rs:1855` |

## Per-target result

| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |
|---|---|---|---:|---|---:|---:|---|
| `alloc::alloc::alloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::alloc_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::dealloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::alloc::handle_alloc_error` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::alloc::realloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::borrow::Cow::into_owned` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `alloc::borrow::Cow::to_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;cow_to_mut_payload_reference_model_missing |
| `alloc::borrow::ToOwned::clone_into` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `alloc::borrow::ToOwned::to_owned` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `alloc::boxed::Box::as_mut_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::assume_init` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::downcast` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::into_pin` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::boxed::Box::into_raw` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::boxed::Box::leak` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::boxed::Box::new_uninit_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::boxed::Box::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_zeroed_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::boxed::Box::pin` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::boxed::Box::write` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::boxed::BoxedArrayIntoIter::as_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `alloc::boxed::BoxedArrayIntoIter::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `alloc::collections::BTreeMap::append` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::entry` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::first_entry` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::first_key_value` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::get_key_value` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::get_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::into_keys` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_values` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::iter_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::last_entry` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::last_key_value` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::pop_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeMap::range` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::remove_entry` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::split_off` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeMap::values_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::append` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::intersection` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::is_disjoint` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_subset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_superset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::range` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::split_off` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::symmetric_difference` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::take` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BTreeSet::union` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::append` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::as_slice` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::clear` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::drain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::into_sorted_vec` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::into_vec` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::is_empty` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::len` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::peek` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::peek_mut` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::pop` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::push` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::BinaryHeap::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::BinaryHeap::with_capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::append` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::back` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::back_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::LinkedList::clear` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::contains` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::front` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::front_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::is_empty` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::len` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::pop_back` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::pop_front` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_back` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_back_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::push_front` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::LinkedList::push_front_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::LinkedList::split_off` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::as_mut_slices` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;implementation_dependent_split_point |
| `alloc::collections::VecDeque::as_slices` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::back` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::back_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::binary_search` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::VecDeque::binary_search_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract;higher_order_closure_comparator_underdetermined |
| `alloc::collections::VecDeque::binary_search_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::contains` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::drain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::front` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::front_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::get` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::get_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::insert_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::is_empty` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::iter_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::make_contiguous` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::partition_point` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::pop_back_if` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::pop_front_if` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::push_back_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::push_front_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::range` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::retain_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::collections::VecDeque::rotate_left` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::rotate_right` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap_remove_back` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::swap_remove_front` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::VecDeque::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::collections::btree_map::Entry::and_modify` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::insert_entry` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::Entry::key` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::or_default` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::Entry::or_insert_with` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with_key` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::insert` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::into_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::key` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::OccupiedEntry::remove` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::remove_entry` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::VacantEntry::insert` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::collections::btree_map::VacantEntry::insert_entry` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::into_key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::as_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::as_bytes_with_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::as_c_str` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::ffi::CString::from_vec_with_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::ffi::CString::into_boxed_c_str` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_bytes_with_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::into_raw` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::ffi::CString::into_string` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::CString::new` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::ffi::FromVecWithNulError::as_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::FromVecWithNulError::into_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::IntoStringError::into_cstring` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::IntoStringError::utf8_error` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::NulError::into_vec` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::ffi::NulError::nul_position` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::fmt::format` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `alloc::rc::Rc::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::rc::Rc::assume_init` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::decrement_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::rc::Rc::downcast` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::downgrade` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::get_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::rc::Rc::increment_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::rc::Rc::into_raw` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::make_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::rc::Rc::new_cyclic` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_zeroed_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::pin` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::strong_count` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::unwrap_or_clone` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Weak::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::upgrade` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::str::from_boxed_utf8_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::string::Drain::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::FromUtf8Error::as_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::FromUtf8Error::into_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::FromUtf8Error::utf8_error` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `alloc::string::String::as_bytes` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::as_mut_str` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::string::String::as_mut_vec` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::string::String::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::clear` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::extend_from_within` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::string::String::from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::from_utf16` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16_lossy` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16be` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16be_lossy` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16le` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf16le_lossy` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8_lossy` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::from_utf8_unchecked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::insert` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::insert_str` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::into_boxed_str` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `alloc::string::String::into_bytes` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::into_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::string::String::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::leak` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::string::String::len` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::pop` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::push` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::push_str` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::remove` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::replace_range` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::split_off` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::truncate` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::string::String::with_capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::sync::Arc::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::assume_init` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::sync::Arc::decrement_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::sync::Arc::downcast` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downgrade` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::increment_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::sync::Arc::into_inner` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::make_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::new_cyclic` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::new_uninit` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_uninit_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_zeroed_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::pin` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::strong_count` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::try_unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::unwrap_or_clone` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Weak::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::upgrade` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::Drain::as_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `alloc::vec::IntoIter::as_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::IntoIter::as_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::Vec::as_mut_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::vec::Vec::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::vec::Vec::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::vec::Vec::dedup` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::dedup_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::vec::Vec::dedup_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::vec::Vec::drain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::vec::Vec::extend_from_within` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `alloc::vec::Vec::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::from_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::vec::Vec::insert_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::vec::Vec::into_boxed_slice` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::into_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::into_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::vec::Vec::leak` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::vec::Vec::pop_if` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::vec::Vec::push_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::vec::Vec::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::vec::Vec::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `alloc::vec::Vec::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::vec::Vec::retain_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `alloc::vec::Vec::set_len` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::vec::Vec::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `alloc::vec::Vec::spare_capacity_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `alloc::vec::Vec::splice` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;duplicate_vstd_assume_specification |
| `core::alloc::GlobalAlloc::alloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::alloc_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::dealloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::alloc::GlobalAlloc::realloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::Layout::align` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::align_to` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::array` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::dangling_ptr` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `core::alloc::Layout::extend` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::extend_packed` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::for_value` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::from_size_align` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::from_size_align_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;duplicate_vstd_assume_specification |
| `core::alloc::Layout::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::pad_to_align` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::repeat` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::repeat_packed` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::alloc::Layout::size` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::array::IntoIter::as_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::array::IntoIter::as_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::array::IntoIter::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::array::as_mut_slice` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::each_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::each_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::from_fn` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::array::from_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::map` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::array::repeat` | skip | skip | 0 |  | 0 | 0 | clone_semantics_unmodeled |
| `core::borrow::Borrow::borrow` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::borrow::BorrowMut::borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::cell::Cell::as_array_of_cells` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::cell::Cell::as_slice_of_cells` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::Cell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::replace` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::set` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::Cell::swap` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::Cell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::update` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::LazyCell::force` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::force_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::LazyCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::new` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::OnceCell::get_or_init` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::set` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Ref::clone` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Ref::filter_map` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::cell::Ref::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::cell::RefCell::borrow` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::RefCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::replace` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::replace_with` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::swap` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::RefCell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow_unguarded` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefMut::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::UnsafeCell::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::get` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::cell::UnsafeCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::raw_get` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::clone::Clone::clone_from` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_eq` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_ge` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_gt` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_le` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_lt` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::is_ne` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::reverse` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::then` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::cmp::Ordering::then_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::cmp::max` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::cmp::max_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::cmp::max_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::cmp::min` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::cmp::min_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::cmp::min_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::convert::AsMut::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::convert::AsRef::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::convert::identity` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::error::Error::cause` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::error::Error::description` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::error::Error::source` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ffi::CStr::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ffi::CStr::count_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_until_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_with_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::from_bytes_with_nul_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ffi::CStr::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::is_empty` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_bytes` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_bytes_with_nul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ffi::CStr::to_str` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::fmt::Arguments::as_str` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Binary::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Debug::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::DebugList::entries` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::entry` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugList::finish_non_exhaustive` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entries` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::entry` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::finish_non_exhaustive` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::key` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugMap::value` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entries` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::entry` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugSet::finish_non_exhaustive` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::field` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugStruct::finish_non_exhaustive` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::field` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::DebugTuple::finish_non_exhaustive` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Display::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Formatter::align` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::alternate` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_list` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_map` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_set` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_struct` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::debug_tuple` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::fill` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::flags` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Formatter::pad` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::pad_integral` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::precision` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_aware_zero_pad` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_minus` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::sign_plus` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::width` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_fmt` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Formatter::write_str` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::LowerExp::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::LowerHex::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::NumBuffer::new` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Octal::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Pointer::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Result::and` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::and_then` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;duplicate_vstd_assume_specification |
| `core::fmt::Result::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::expect` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::expect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::flatten` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::inspect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::is_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;duplicate_vstd_assume_specification |
| `core::fmt::Result::is_err_and` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::is_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::is_ok_and` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::iter` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::map` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::map_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;duplicate_vstd_assume_specification |
| `core::fmt::Result::map_or` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::or` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;duplicate_vstd_assume_specification |
| `core::fmt::Result::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_else` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::UpperExp::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::UpperHex::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_char` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_str` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::from_fn` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::write` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::future::Future::poll` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::future::IntoFuture::into_future` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::future::Ready::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::pending` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::poll_fn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::future::ready` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::hint::assert_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::hint::black_box` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::hint::cold_path` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::hint::select_unpredictable` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::hint::spin_loop` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::intrinsics::copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::intrinsics::copy_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::intrinsics::transmute` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::intrinsics::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::io::Chain::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Chain::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Chain::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::new` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::position` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Cursor::set_position` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Error::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Error::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Error::kind` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Error::raw_os_error` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSlice::advance` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSlice::advance_slices` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSlice::new` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::advance` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::advance_slices` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::IoSliceMut::new` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::and` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::and_then` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::as_deref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::cloned` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::copied` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::expect` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::expect_err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::flatten` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::inspect` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::is_err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::is_err_and` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::is_ok` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::is_ok_and` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::iter` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::map` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::map_err` | add_spec | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;determinism_unsupported_contract_form;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::map_or` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::map_or_else` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::ok` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::or` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::or_else` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::transpose` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_err_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or_default` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_or_else` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Result::unwrap_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Seek::rewind` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;determinism_unsupported_contract_form;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Seek::seek` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;determinism_unsupported_contract_form;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Seek::seek_relative` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;determinism_unsupported_contract_form;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Seek::stream_position` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;determinism_unsupported_contract_form;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Take::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Take::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Take::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Take::limit` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::Take::set_limit` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::empty` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::repeat` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::io::sink` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `core::iter::DoubleEndedIterator::nth_back` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfind` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfold` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;duplicate_vstd_assume_specification |
| `core::iter::DoubleEndedIterator::try_rfold` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::ExactSizeIterator::len` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Extend::extend` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::by_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::chain` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::cloned` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::cmp` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::count` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::cycle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::enumerate` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::eq` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::filter` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::find_map` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::flat_map` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::flatten` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::fold` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::for_each` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::iter::Iterator::fuse` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::ge` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::gt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::inspect` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::last` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::le` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::lt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::map` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::map_while` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::ne` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::nth` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::partial_cmp` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::partition` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::peekable` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::position` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::product` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::reduce` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::rposition` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::scan` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::size_hint` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::skip` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::skip_while` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::step_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::sum` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::take` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::take_while` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::try_fold` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::try_for_each` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::unzip` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::zip` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Peekable::next_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_eq` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;peekable_next_if_closure_observation_underdetermined |
| `core::iter::Peekable::next_if_map` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::Peekable::next_if_map_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;peekable_next_if_map_mut_closure_observation_underdetermined |
| `core::iter::Peekable::peek` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::peek_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::iter::Product::product` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Sum::sum` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::chain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::empty` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::from_fn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::once` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::once_with` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_n` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::repeat_with` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::successors` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::zip` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::mem::ManuallyDrop::drop` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::ManuallyDrop::take` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_mut_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::assume_init_drop` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::assume_init_read` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::write` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `core::mem::discriminant` | skip | skip | 0 |  | 0 | 0 | compiler_intrinsic_discriminant_model_gap |
| `core::mem::drop` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::mem::forget` | add_spec | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::mem::min_align_of` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::min_align_of_val` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::needs_drop` | skip | skip | 0 |  | 0 | 0 | compiler_intrinsic_type_property_model_gap |
| `core::mem::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::take` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::mem::transmute_copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::uninitialized` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::zeroed` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::net::IpAddr::is_ipv4` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_ipv6` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_loopback` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_multicast` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::is_unspecified` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::IpAddr::to_canonical` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::from_bits` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::from_octets` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_broadcast` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_documentation` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_link_local` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_loopback` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_multicast` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_private` | skip | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::is_unspecified` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::octets` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_bits` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_ipv6_compatible` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv4Addr::to_ipv6_mapped` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_bits` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_octets` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::from_segments` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_loopback` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_multicast` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unicast_link_local` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unique_local` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::is_unspecified` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::octets` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::segments` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_bits` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_canonical` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_ipv4` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::Ipv6Addr::to_ipv4_mapped` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::is_ipv4` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::is_ipv6` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::set_ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddr::set_port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::set_ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV4::set_port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::flowinfo` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::scope_id` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_flowinfo` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_ip` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_port` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::net::SocketAddrV6::set_scope_id` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::AddAssign::add_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitAnd::bitand` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitAndAssign::bitand_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitOr::bitor` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitOrAssign::bitor_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitXor::bitxor` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitXorAssign::bitxor_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Bound::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::Bound::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::Bound::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract;higher_order_closure_result_underdetermined |
| `core::ops::ControlFlow::break_ok` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::break_value` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::continue_ok` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::continue_value` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::is_break` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::is_continue` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::ops::ControlFlow::map_break` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::ops::ControlFlow::map_continue` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::ops::DivAssign::div_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Drop::drop` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::IndexMut::index_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::MulAssign::mul_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Not::not` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Range::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeBounds::contains` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::RangeFrom::contains` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::RangeInclusive::end` | add_spec | skip | 0 |  | 0 | 0 | value_unspecified_after_exhaustion;value_unspecified_after_exhaustion |
| `core::ops::RangeInclusive::into_inner` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::start` | add_spec | skip | 0 |  | 0 | 0 | value_unspecified_after_exhaustion;value_unspecified_after_exhaustion |
| `core::ops::RangeTo::contains` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::RangeToInclusive::contains` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::Rem::rem` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::RemAssign::rem_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Shl::shl` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::ShlAssign::shl_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Shr::shr` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::ShrAssign::shr_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::SubAssign::sub_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::option::Option::and` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;determinism_unsupported_contract_form |
| `core::option::Option::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::option::Option::as_pin_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_pin_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `core::option::Option::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::option::Option::filter` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::flatten` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::get_or_insert_default` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::option::Option::get_or_insert_with` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::option::Option::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::is_none_or` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_some_and` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::option::Option::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::map_or` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::map_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::option::Option::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::take_if` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::transpose` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::option::Option::unzip` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::xor` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::zip` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::panic::Location::caller` | skip | skip | 0 |  | 0 | 0 | call_site_intrinsic_hidden_state |
| `core::panic::Location::column` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::file` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::file_as_c_str` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::Location::line` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::panic::PanicInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;panic_location_abstraction_missing |
| `core::panic::PanicInfo::message` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicMessage::as_str` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::pin::Pin::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::into_inner_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::into_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::map_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::map_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::new_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::set` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::static_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::static_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::add` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::addr` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::align_offset` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::NonNull::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;missing_nonnull_pointer_view |
| `core::ptr::NonNull::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::NonNull::byte_offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::cast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::copy_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_from_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_to` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_to_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::dangling` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::drop_in_place` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::expose_provenance` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::from_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ptr::NonNull::from_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_aligned` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::map_addr` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::ptr::NonNull::new` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::NonNull::new_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::NonNull::offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::replace` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::slice_from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::sub` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::swap` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::with_addr` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::with_exposed_provenance` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::without_provenance` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::write` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;duplicate_vstd_assume_specification |
| `core::ptr::addr_eq` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::align_offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::as_array` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::as_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::ptr::as_mut_array` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;raw_pointer_representation_contract |
| `core::ptr::as_mut_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::as_ref_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::byte_add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::byte_offset_from_unsigned` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::cast` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::cast_const` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::cast_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_from_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_to` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_to_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::dangling` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::dangling_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::drop_in_place` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::eq` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::expose_provenance` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::fn_addr_eq` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `core::ptr::from_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::from_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::hash` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_aligned` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::is_empty` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_null` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::len` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::map_addr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::offset_from` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::offset_from_unsigned` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::read` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::replace` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::slice_from_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::slice_from_raw_parts_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::sub` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::swap` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::swap_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::with_addr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::with_exposed_provenance` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::with_exposed_provenance_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::without_provenance` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::without_provenance_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_add` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::wrapping_byte_add` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::wrapping_byte_sub` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::wrapping_offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_sub` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::write` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::result::Result::and` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::and_then` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;determinism_unsupported_contract_form |
| `core::result::Result::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;deref_mut_result_payload_model_missing |
| `core::result::Result::as_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::result::Result::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::result::Result::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::result::Result::expect_err` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::flatten` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::inspect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::is_err_and` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::is_ok_and` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::result::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::map_or` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::map_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::transpose` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::result::Result::unwrap_or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::result::Result::unwrap_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::ChunksExact::remainder` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::ChunksExactMut::into_remainder` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::Iter::as_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::slice::IterMut::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::IterMut::into_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::RChunksExact::remainder` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::RChunksExactMut::into_remainder` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::align_to` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::align_to_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::array_windows` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::as_array` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_chunks` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_chunks_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_chunks_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_chunks_unchecked_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::as_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_flattened_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::as_mut_array` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_mut_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_mut_ptr_range` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_ptr_range` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_rchunks` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_rchunks_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::assume_init_drop` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::assume_init_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::binary_search` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::binary_search_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract;higher_order_closure_comparator_underdetermined |
| `core::slice::binary_search_by_key` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract;higher_order_closure_key_extraction_underdetermined |
| `core::slice::chunk_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunk_by_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunks` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::slice::chunks_exact` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::slice::chunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::clone_from_slice` | skip | skip | 0 |  | 0 | 0 | clone_semantics_unmodeled |
| `core::slice::contains` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::element_offset` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::ends_with` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::escape_ascii` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::fill` | skip | skip | 0 |  | 0 | 0 | clone_semantics_unmodeled |
| `core::slice::fill_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::first_chunk_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::from_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::from_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::from_raw_parts_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::get_disjoint_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::get_disjoint_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::get_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::is_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_sorted` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_sorted_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::slice::is_sorted_by_key` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract;higher_order_closure_key_extraction_underdetermined |
| `core::slice::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::last_chunk_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::make_ascii_lowercase` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::make_ascii_uppercase` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::partition_point` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::slice::rchunks` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::slice::rchunks_exact` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::reverse` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::rotate_left` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::rotate_right` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::rsplit` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::select_nth_unstable` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;permitted_partition_order_underdetermined |
| `core::slice::select_nth_unstable_by` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;permitted_partition_order_underdetermined |
| `core::slice::select_nth_unstable_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;permitted_partition_order_underdetermined |
| `core::slice::sort_unstable` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `core::slice::sort_unstable_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::sort_unstable_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::split` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_at_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_at_mut_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_at_mut_unchecked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_at_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::split_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first_chunk_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_inclusive` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_inclusive_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::split_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last_chunk_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::slice::split_off` | skip | skip | 0 |  | 0 | 0 | one_sided_range_split_point_underdetermined;direction_choice_not_modeled |
| `core::slice::split_off_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_off_first_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_off_last` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::split_off_last_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_off_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::splitn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::splitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::starts_with` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::strip_circumfix` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_prefix` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_suffix` | skip | skip | 0 |  | 0 | 0 | generic_slice_pattern_model_gap |
| `core::slice::subslice_range` | skip | skip | 0 |  | 0 | 0 | pointer_address_or_provenance_model_gap |
| `core::slice::swap` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::swap_with_slice` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::trim_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::utf8_chunks` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::windows` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::write_clone_of_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::slice::write_copy_of_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::str::CharIndices::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::CharIndices::offset` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Chars::as_str` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::str::FromStr::from_str` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::str::Utf8Chunk::invalid` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::str::Utf8Chunk::valid` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Error::error_len` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::str::Utf8Error::valid_up_to` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::str::as_bytes_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::str::as_mut_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::str::bytes` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::str::ceil_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::char_indices` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::contains` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::encode_utf16` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::ends_with` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::escape_debug` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_default` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_unicode` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::find` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::floor_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::from_utf8` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::from_utf8_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::from_utf8_unchecked_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;determinism_unsupported_contract_form |
| `core::str::get` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::lines` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines_any` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::make_ascii_lowercase` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::make_ascii_uppercase` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::match_indices` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::matches` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::parse` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rfind` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;generic_pattern_reverse_search_underdetermined |
| `core::str::rmatch_indices` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_once` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;generic_pattern_reverse_search_underdetermined |
| `core::str::rsplit_terminator` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplitn` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::slice_mut_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::slice_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::str::split` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_ascii_whitespace` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_at_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::split_at_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::split_inclusive` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_once` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `core::str::split_terminator` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_whitespace` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::splitn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::starts_with` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_circumfix` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;determinism_unsupported_contract_form |
| `core::str::strip_prefix` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_suffix` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `core::str::substr_range` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::str::trim` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_ascii_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_ascii_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_end_matches` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;determinism_unsupported_contract_form |
| `core::str::trim_left` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_left_matches` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;determinism_unsupported_contract_form |
| `core::str::trim_matches` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;determinism_unsupported_contract_form |
| `core::str::trim_right` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_right_matches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection;generic_pattern_suffix_trim_underdetermined |
| `core::str::trim_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_start_matches` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model;generic_pattern_prefix_trim_underdetermined |
| `core::sync::atomic::Atomic::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange_weak` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_and` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_max` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_min` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_nand` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_not` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_or` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_ptr_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::fetch_xor` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::from_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::load` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::new` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::store` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::Atomic::swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_not` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicBool::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI16::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI32::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI64::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI64::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI8::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicI8::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicIsize::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange_weak` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::fetch_and` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_or` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_xor` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicPtr::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::load` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::new` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::store` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::AtomicPtr::swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU16::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU32::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU32::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU64::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU8::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicU8::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicUsize::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::compiler_fence` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::fence` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::spin_loop_hint` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::time::Duration::abs_diff` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_micros` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_millis` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_nanos` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::as_secs_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_add` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_div` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_mul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::checked_sub` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_duration_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_duration_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::div_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_hours` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_micros` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_millis` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_mins` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_nanos` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_nanos_u128` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::from_secs_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::is_zero` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::mul_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::mul_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::new` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_add` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_mul` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::saturating_sub` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_micros` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_millis` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::subsec_nanos` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::try_from_secs_f32` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `core::time::Duration::try_from_secs_f64` | add_spec | skip | 0 |  | 0 | 0 | duplicate_vstd_assume_specification |
| `std::collections::HashMap::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::drain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashMap::extract_if` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashMap::get_disjoint_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported;hashmap_get_disjoint_mut_reference_array_model_missing |
| `std::collections::HashMap::get_disjoint_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_key_value` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `std::collections::HashMap::get_mut` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashMap::hasher` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::into_keys` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_values` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::iter_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashMap::remove_entry` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashMap::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::values_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashMap::with_capacity_and_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::with_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::drain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashSet::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::hasher` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::intersection` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::is_disjoint` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::is_subset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::is_superset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::retain` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashSet::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::symmetric_difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::take` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `std::collections::HashSet::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::union` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `std::collections::HashSet::with_capacity_and_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::with_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::env::args` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::args_os` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::current_exe` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::home_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::join_paths` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::remove_var` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::env::set_current_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::set_var` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::env::split_paths` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::temp_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::var_os` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::env::vars_os` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::ffi::OsStr::as_encoded_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::display` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::eq_ignore_ascii_case` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::from_encoded_bytes_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsStr::into_os_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::is_ascii` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::make_ascii_lowercase` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::make_ascii_uppercase` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_ascii_lowercase` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_ascii_uppercase` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_os_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::to_string_lossy` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::from_encoded_bytes_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsString::into_boxed_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_encoded_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::ffi::OsString::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::push` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to_fit` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::fs::DirBuilder::create` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirBuilder::recursive` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_name` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::file_type` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::metadata` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::DirEntry::path` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::create_new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::lock_shared` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::metadata` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::open` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::options` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_len` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_modified` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_permissions` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::set_times` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_all` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::sync_data` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::try_lock_shared` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::File::unlock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_accessed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileTimes::set_modified` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_file` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::FileType::is_symlink` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::accessed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::created` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::file_type` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_file` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::is_symlink` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::len` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::modified` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Metadata::permissions` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::append` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::create_new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::open` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::read` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::truncate` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::OpenOptions::write` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::readonly` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::Permissions::set_readonly` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::canonicalize` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::copy` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::create_dir_all` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::exists` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::hard_link` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::metadata` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_link` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::read_to_string` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_dir_all` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::remove_file` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::rename` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::set_permissions` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::soft_link` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::symlink_metadata` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::fs::write` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufRead::consume` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::fill_buf` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::lines` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::read_line` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::read_until` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::skip_until` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::split` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufReader::buffer` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::seek_relative` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufReader::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::buffer` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::into_parts` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::BufWriter::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IntoInnerError::into_parts` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::IsTerminal::is_terminal` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::LineWriter::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeReader::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeWriter::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Read::by_ref` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::bytes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::chain` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_exact` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_to_end` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_to_string` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_vectored` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::take` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Stderr::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lines` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::read_line` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdout::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Write::by_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::flush` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_all` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_vectored` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::WriterPanicked::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::copy` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::pipe` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::read_to_string` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stderr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdin` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::stdout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::accept` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::bind` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::incoming` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::only_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_only_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::set_ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpListener::ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::connect_timeout` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::net::TcpStream::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::nodelay` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::peek` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::net::TcpStream::peer_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nodelay` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::set_write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::shutdown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::ToSocketAddrs::to_socket_addrs` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::net::UdpSocket::bind` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::broadcast` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::connect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::join_multicast_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::leave_multicast_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_loop_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::multicast_ttl_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peek` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::net::UdpSocket::peek_from` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peer_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv_from` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::send_to` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_broadcast` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_loop_v6` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_multicast_ttl_v4` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::set_write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::ttl` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::AsFd::as_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::AsRawFd::as_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::BorrowedFd::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::BorrowedFd::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::FromRawFd::from_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::IntoRawFd::into_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::OwnedFd::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::ffi::OsStrExt::as_bytes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStrExt::from_bytes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStringExt::from_vec` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::ffi::OsStringExt::into_vec` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::DirBuilderExt::mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::DirEntryExt::ino` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::read_at` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::read_exact_at` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::write_all_at` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileExt::write_at` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_block_device` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_char_device` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_fifo` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::FileTypeExt::is_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::atime` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::atime_nsec` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::blksize` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::blocks` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ctime` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ctime_nsec` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::dev` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::gid` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::ino` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mtime` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::mtime_nsec` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::nlink` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::rdev` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::size` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::MetadataExt::uid` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::OpenOptionsExt::custom_flags` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::OpenOptionsExt::mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::from_mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::PermissionsExt::set_mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::unix::fs::chown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::chroot` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::fchown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::lchown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::fs::symlink` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::as_pathname` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::from_pathname` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::SocketAddr::is_unnamed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::bind_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::connect_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::pair` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::peer_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::recv_from` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::send_to` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to_addr` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_write_timeout` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::os::unix::net::UnixDatagram::shutdown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::unbound` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::accept` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::bind_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::incoming` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixListener::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::connect_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::pair` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::peer_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::set_write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::shutdown` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::take_error` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixStream::write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::ffi::OsStrExt::encode_wide` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::ffi::OsStringExt::from_wide` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::FileExt::seek_read` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::FileExt::seek_write` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTimesExt::set_created` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTypeExt::is_symlink_dir` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::FileTypeExt::is_symlink_file` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::creation_time` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::file_attributes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::file_size` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::last_access_time` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::MetadataExt::last_write_time` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::access_mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::attributes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::custom_flags` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::security_qos_flags` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::OpenOptionsExt::share_mode` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::fs::symlink_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::fs::symlink_file` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::AsHandle::as_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawHandle::as_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawSocket::as_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsSocket::as_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::BorrowedHandle::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::FromRawHandle::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::FromRawSocket::from_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::HandleOrInvalid::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrNull::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::IntoRawHandle::into_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::IntoRawSocket::into_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::OwnedHandle::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedSocket::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::panic::PanicHookInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;panic_location_abstraction_missing |
| `std::panic::PanicHookInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicHookInfo::payload_as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;panic_location_abstraction_missing |
| `std::panic::PanicInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::payload_as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::catch_unwind` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `std::panic::panic_any` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::resume_unwind` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::panic::set_hook` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `std::panic::take_hook` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `std::path::Component::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Components::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Iter::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::ancestors` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::as_mut_os_str` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::Path::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::canonicalize` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::components` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::display` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::ends_with` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::exists` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::extension` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_name` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_prefix` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::file_stem` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::has_root` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::into_path_buf` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_absolute` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_dir` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_empty` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::path::Path::is_file` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_relative` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_symlink` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::iter` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::path::Path::join` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::metadata` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::parent` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::read_dir` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::read_link` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::starts_with` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::strip_prefix` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::symlink_metadata` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_path_buf` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::to_string_lossy` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::try_exists` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_added_extension` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_extension` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::with_file_name` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::add_extension` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::as_mut_os_string` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_boxed_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_os_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_string` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `std::path::PathBuf::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::pop` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::path::PathBuf::push` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::set_extension` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::path::PathBuf::set_file_name` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::shrink_to` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to_fit` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::Prefix::is_verbatim` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::kind` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::absolute` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::is_separator` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::process::Child::id` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::kill` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::try_wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::process::Child::wait_with_output` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::arg` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::args` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::current_dir` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::process::Command::env` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_clear` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_remove` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::envs` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::process::Command::get_args` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_current_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_envs` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::get_program` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::output` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::spawn` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::status` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stderr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdin` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::stdout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::code` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::ExitStatus::success` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::inherit` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::null` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Stdio::piped` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Termination::report` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::process::abort` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::exit` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::id` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Barrier::wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::BarrierWaitResult::is_leader` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::notify_all` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Condvar::notify_one` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Condvar::wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_ms` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_timeout_while` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Condvar::wait_while` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::force_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LazyLock::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::and` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::and_then` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::as_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::sync::LockResult::expect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::flatten` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::sync::LockResult::is_err_and` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::sync::LockResult::is_ok_and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::sync::LockResult::or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::Mutex::clear_poison` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Mutex::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::is_poisoned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Mutex::try_lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::call_once` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Once::call_once_force` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Once::is_completed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::Once::wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::Once::wait_force` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::OnceLock::get` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::get_or_init` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::set` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::OnceLock::take` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceLock::wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::OnceState::is_poisoned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::PoisonError::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::clear_poison` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::sync::RwLock::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::is_poisoned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::read` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_read` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::try_write` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLock::write` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::RwLockWriteGuard::downgrade` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::and_then` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::expect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::flatten` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_err_and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_ok_and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_else` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::sync::TryLockResult::or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or_else` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::transpose` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::WaitTimeoutResult::timed_out` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Sender::send` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::mpsc::SyncSender::send` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::SyncSender::try_send` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::channel` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::sync_channel` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::name` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_scoped` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::spawn_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Builder::stack_size` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::is_finished` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::join` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::JoinHandle::thread` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::get` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::replace` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::set` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::LocalKey::take` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::try_with` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::update` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::LocalKey::with` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::LocalKey::with_borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::and_then` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::as_deref_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::cloned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::thread::Result::expect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::expect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::flatten` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::thread::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::thread::Result::is_err_and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::thread::Result::is_ok_and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::map_or` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::thread::Result::or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::or_else` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;duplicate_vstd_assume_specification |
| `std::thread::Result::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or_default` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Scope::spawn` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::is_finished` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::join` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::thread` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::id` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::name` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::unpark` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::available_parallelism` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::current` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::panicking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::park` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::park_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::park_timeout_ms` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::scope` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::sleep` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::sleep_ms` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::spawn` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::yield_now` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::time::Instant::checked_add` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_duration_since` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::checked_sub` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::duration_since` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::elapsed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::now` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::Instant::saturating_duration_since` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_add` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::checked_sub` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::time::SystemTime::duration_since` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::elapsed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::now` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTimeError::duration` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
