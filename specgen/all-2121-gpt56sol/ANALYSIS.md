# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `targets` | 2121 |
| `initial_add_spec` | 437 |
| `initial_skip` | 1684 |
| `final_add_spec` | 214 |
| `final_skip` | 1907 |
| `typecheck_passed` | 212 |
| `det_unsat` | 162 |
| `det_sat` | 0 |
| `det_unknown` | 40 |
| `raw_reward` | 162 |
| `guarded_reward` | 104 |
| `semantic_guarded_reward` | 94 |
| `llm_errors` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 214 |
| `add_spec->skip` | 223 |
| `skip->skip` | 1684 |

## Frequent issues

| Issue | Count |
|---|---:|
| `classification:runtime_or_hidden_state` | 495 |
| `classification:needs_new_vstd_abstraction` | 361 |
| `determinism_unsupported_contract_form` | 309 |
| `classification:trait_contract_integration` | 201 |
| `classification:unsafe_or_representation_sensitive` | 181 |
| `classification:concurrency_or_hidden_state` | 179 |
| `no_modeled_observable_output` | 137 |
| `classification:determinism_checker_unsupported` | 109 |
| `classification:iterator_or_adapter_result` | 101 |
| `classification:formatting_effect` | 79 |
| `classification:higher_order_contract` | 71 |
| `classification:toolchain_unavailable` | 70 |
| `not_in_verus_rust_1_96` | 70 |
| `classification:representation_or_allocator` | 59 |
| `determinism_not_proved:unknown` | 40 |
| `classification:ownership_or_uninitialized_model` | 33 |
| `classification:complex_result_or_pattern_model` | 21 |
| `classification:associated_type_or_projection` | 19 |
| `checker_status:verus_error` | 9 |
| `classification:no_modeled_observable_output` | 9 |
| `structured_contract_mismatch` | 5 |
| `trivial_equal_fn` | 4 |
| `contract_typecheck_failed` | 2 |

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
| `alloc::collections::BTreeSet::is_subset` | `result == this@.subset_of(other@)` |
| `alloc::collections::BTreeSet::is_superset` | `result == other@.subset_of(this@)` |
| `alloc::collections::BTreeSet::last` | `match result { core::option::Option::Some(value) => { &&& !m@.is_empty() &&& *value == m@.find_unique_maximal(|x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,) &&& m@.contains(*value) &&& forall|x: T| #[trigger] m@.contains(x) ==> x.cmp_spec(value) != core::cmp::Ordering::Greater }, core::option::Option::None => m@.is_empty(), }` |
| `alloc::collections::BTreeSet::pop_first` | `if old(m)@.is_empty() { &&& result is None &&& final(m)@ == old(m)@ } else { let first = choose|candidate: T| { &&& old(m)@.contains(candidate) &&& forall|element: T| old(m)@.contains(element) ==> candidate.cmp_spec(&element) != Ordering::Greater }; &&& result == Some(first) &&& old(m)@.contains(first) &&& forall|element: T| old(m)@.contains(element) ==> first.cmp_spec(&element) != Ordering::Greater &&& final(m)@ == old(m)@.remove(first) }` |
| `alloc::collections::BTreeSet::pop_last` | `match result {
            core::option::Option::Some(value) => {
                &&& !old(m)@.is_empty()
                &&& value == old(m)@.find_unique_maximal(
                    |x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,
                )
                &&& old(m)@.contains(value)
                &&& final(m)@ == old(m)@.remove(value)
                &&& forall|x: T| #[trigger] old(m)@.contains(x) ==>
                    x.cmp_spec(&value) != core::cmp::Ordering::Greater
            },
            core::option::Option::None => {
                &&& old(m)@.is_empty()
                &&& final(m)@ == old(m)@
            },
        }` |
| `alloc::collections::BTreeSet::replace` | `{ let matching = old(m)@.filter(|existing: T| existing.cmp_spec(&value) == Ordering::Equal); if matching.is_empty() { &&& result is None &&& final(m)@ == old(m)@.insert(value) } else { let replaced = matching.choose(); &&& result == Some(replaced) &&& old(m)@.contains(replaced) &&& replaced.cmp_spec(&value) == Ordering::Equal &&& final(m)@ == old(m)@.remove(replaced).insert(value) } }` |
| `alloc::collections::BTreeSet::take` | `match result {
            Some(v) => {
                &&& set_contains_borrowed_key(old(m)@, value)
                &&& sets_borrowed_key_to_key(old(m)@, value, &v)
                &&& old(m)@.contains(v)
                &&& final(m)@ == old(m)@.remove(v)
            },
            None => {
                &&& !set_contains_borrowed_key(old(m)@, value)
                &&& final(m)@ == old(m)@
            },
        }` |
| `alloc::string::String::extend_from_within` | `final(s)@ == old(s)@ + decode_utf8(encode_utf8(old(s)@).subrange(slice_range_start(&src), slice_range_end(&src, encode_utf8(old(s)@).len())))` |
| `alloc::string::String::insert` | `final(s)@ == decode_utf8(encode_utf8(old(s)@).subrange(0, idx as int)) + seq![ch] + decode_utf8(encode_utf8(old(s)@).subrange(idx as int, encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::insert_str` | `final(s)@ == decode_utf8(encode_utf8(old(s)@).subrange(0, idx as int)) + string@ + decode_utf8(encode_utf8(old(s)@).subrange(idx as int, encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::is_empty` | `res == (s@.len() == 0)` |
| `alloc::string::String::len` | `res as nat == vstd::utf8::encode_utf8(s@).len()` |
| `alloc::string::String::pop` | `old(s)@.len() == 0 ==> res == core::option::Option::None && final(s)@ == old(s)@; old(s)@.len() > 0 ==> res == core::option::Option::Some(old(s)@[old(s)@.len() - 1]) && final(s)@ == old(s)@.subrange(0, old(s)@.len() - 1)` |
| `alloc::string::String::push` | `final(s)@ == old(s)@.push(ch)` |
| `alloc::string::String::push_str` | `final(s)@ == old(s)@ + string@` |
| `alloc::string::String::remove` | `res == old(s)@[idx as int]; final(s)@ == old(s)@.remove(idx as int)` |
| `alloc::string::String::replace_range` | `final(s)@ == decode_utf8(encode_utf8(old(s)@).subrange(0, slice_range_start(&range))) + replace_with@ + decode_utf8(encode_utf8(old(s)@).subrange(slice_range_end(&range, encode_utf8(old(s)@).len()), encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::split_off` | `final(s)@ == vstd::utf8::decode_utf8(vstd::utf8::encode_utf8(old(s)@).subrange(0, at as int)); res@ == vstd::utf8::decode_utf8(vstd::utf8::encode_utf8(old(s)@).subrange(at as int, vstd::utf8::encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::truncate` | `final(s)@ == if encode_utf8(old(s)@).len() > new_len as int { decode_utf8(encode_utf8(old(s)@).subrange(0, new_len as int)) } else { old(s)@ }` |
| `alloc::vec::Vec::into_flattened` | `flattened@ == vec@.map_values(|array: [T; N]| array@).flatten()` |
| `core::array::from_ref` | `out@ == seq![*s]` |
| `core::cmp::min` | `match v2.cmp_spec(&v1) { core::cmp::Ordering::Less => r == v2, core::cmp::Ordering::Equal => r == v1, core::cmp::Ordering::Greater => r == v1, }` |
| `core::hint::select_unpredictable` | `result == if condition { true_val } else { false_val }` |
| `core::mem::min_align_of` | `res as nat == align_of::<T>()` |
| `core::mem::min_align_of_val` | `res as nat == spec_align_of_val::<T>(val)` |
| `core::ops::Range::is_empty` | `ret == !r.start.is_lt(&r.end)` |
| `core::ops::RangeInclusive::into_inner` | `ret.0 == range@.start; ret.1 == range@.end` |
| `core::ops::RangeInclusive::is_empty` | `ret == (r@.exhausted || !r@.start.is_le(&r@.end))` |
| `core::ops::RangeInclusive::start` | `ret == r@.start` |
| `core::option::Option::and` | `option.is_none() ==> res.is_none(); option.is_some() ==> res == optb` |
| `core::option::Option::flatten` | `res == match option { core::option::Option::Some(inner) => inner, core::option::Option::None => core::option::Option::None, }` |
| `core::option::Option::or` | `option.is_some() ==> res == option; option.is_none() ==> res == optb` |
| `core::option::Option::transpose` | `res == match option { core::option::Option::Some(core::result::Result::Ok(x)) => core::result::Result::Ok(core::option::Option::Some(x)), core::option::Option::Some(core::result::Result::Err(e)) => core::result::Result::Err(e), core::option::Option::None => core::result::Result::Ok(core::option::Option::None), }` |
| `core::option::Option::unzip` | `res == match option { Some((a, b)) => (Some(a), Some(b)), None => (None, None), }` |
| `core::option::Option::xor` | `res == match (option, optb) {
            (Some(a), None) => Some(a),
            (None, Some(b)) => Some(b),
            _ => None,
        }` |
| `core::option::Option::zip` | `res == match (option, other) { (Some(a), Some(b)) => Some((a, b)), _ => None, }` |
| `core::result::Result::and` | `result is Ok ==> and_result == res; result is Err ==> and_result == Result::<U, E>::Err(result->Err_0)` |
| `core::result::Result::expect_err` | `e == result->Err_0` |
| `core::result::Result::flatten` | `result is Ok ==> flattened == result->Ok_0; result is Err ==> flattened is Err; result is Err ==> flattened->Err_0 == result->Err_0` |
| `core::result::Result::or` | `result is Ok ==> output == Result::<T, F>::Ok(result->Ok_0); result is Err ==> output == res` |
| `core::result::Result::transpose` | `transposed == (match result { core::result::Result::Ok(core::option::Option::Some(value)) => { core::option::Option::Some(core::result::Result::Ok(value)) }, core::result::Result::Ok(core::option::Option::None) => { core::option::Option::None }, core::result::Result::Err(error) => { core::option::Option::Some(core::result::Result::Err(error)) }, })` |
| `core::result::Result::unwrap_or` | `match result { core::result::Result::Ok(value) => t == value, core::result::Result::Err(_) => t == default, }` |
| `core::slice::as_chunks` | `{ let chunks = choose|candidate: Seq<[T; N]>| { &&& candidate.len() == slice@.len() / (N as nat) &&& forall|i: int| 0 <= i < candidate.len() ==> (#[trigger] candidate[i])@ == slice@.subrange(i * (N as int), (i + 1) * (N as int)) }; &&& ret.0@ == chunks &&& ret.0@.len() == slice@.len() / (N as nat) &&& ret.1@.len() == slice@.len() % (N as nat) &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len() &&& forall|i: int| 0 <= i < ret.0@.len() ==> (#[trigger] ret.0@[i])@ == slice@.subrange(i * (N as int), (i + 1) * (N as int)) &&& ret.1@ == slice@.subrange(((slice@.len() / (N as nat)) * (N as nat)) as int, slice@.len() as int) }` |
| `core::slice::as_flattened` | `ret@.len() == slice@.len() * N; ret@ == slice@.flat_map(|a: [T; N]| a@)` |
| `core::slice::binary_search` | `match result { core::result::Result::Ok(index) => { &&& slice@.len() > index &&& slice@[index as int].cmp_spec(x) == core::cmp::Ordering::Equal &&& forall|i: int| #![auto] i > index as int && slice@.len() > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Greater }, core::result::Result::Err(index) => { &&& slice@.len() >= index &&& forall|i: int| #![auto] i >= 0 && index as int > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Less &&& forall|i: int| #![auto] i >= index as int && slice@.len() > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Greater }, }` |
| `core::slice::contains` | `ret <==> exists|i: int| i >= 0 && slice@.len() > i && slice@[i].eq_spec(x)` |
| `core::slice::ends_with` | `result == (slice@.len() >= needle@.len() && (forall|i: int| i >= 0 && needle@.len() > i ==> needle@[i].eq_spec(&slice@[slice@.len() - needle@.len() + i])))` |
| `core::slice::eq_ignore_ascii_case` | `result == (slice@.len() == other@.len() && forall|i: int| i >= 0 && slice@.len() > i ==> (if slice@[i] >= 65 && 90 >= slice@[i] { slice@[i] as int + 32 } else { slice@[i] as int }) == (if other@[i] >= 65 && 90 >= other@[i] { other@[i] as int + 32 } else { other@[i] as int }))` |
| `core::slice::first_chunk` | `ret.is_some() <==> slice@.len() >= (N as int); ret.is_some() ==> ret.unwrap()@ == slice@.subrange(0, N as int)` |
| `core::slice::from_ref` | `r@ == seq![*s]` |
| `core::slice::is_ascii` | `ret == (forall|i: int| (i >= 0 && slice@.len() > i) ==> 0x7f >= slice@[i])` |
| `core::slice::is_sorted` | `ret <==> forall|i: int| i >= 0 && slice@.len() > i + 1 ==> (#[trigger] slice@[i]).is_le(&slice@[i + 1])` |
| `core::slice::last_chunk` | `slice.len() < N ==> ret.is_none(); N <= slice.len() ==> ret.is_some() && ret.unwrap()@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int)` |
| `core::slice::split_at_checked` | `ret.is_some() <==> mid <= slice@.len(); ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, mid as int); ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int)` |
| `core::slice::split_first` | `match ret {
            None => slice@.len() == 0,
            Some((first, rest)) => {
                &&& slice@.len() > 0
                &&& *first == slice@[0]
                &&& rest@ == slice@.subrange(1, slice@.len() as int)
            },
        }` |
| `core::slice::split_first_chunk` | `slice.len() < N ==> ret.is_none(); N <= slice.len() ==> ret.is_some() && ret.unwrap().0@ == slice@.subrange(0, N as int) && ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int)` |
| `core::slice::split_last` | `match ret { core::option::Option::None => slice@.len() == 0, core::option::Option::Some((last, init)) => { &&& slice@.len() > 0 &&& *last == slice@[slice@.len() as int - 1] &&& init@ == slice@.subrange(0, slice@.len() as int - 1) }, }` |
| `core::slice::split_last_chunk` | `match ret { core::option::Option::Some((init, last)) => { &&& slice@.len() >= N &&& init@ == slice@.subrange(0, slice@.len() as int - N as int) &&& last@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int) }, core::option::Option::None => N > slice@.len(), }` |
| `core::slice::starts_with` | `result == (slice@.len() >= needle@.len() && (forall|i: int| i >= 0 && needle@.len() > i ==> needle@[i].eq_spec(&slice@[i])))` |
| `core::slice::trim_ascii` | `exists|start: int, end: int| start >= 0 && end >= start && slice@.len() >= end && (forall|i: int| (i >= 0 && start > i) ==> (slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8)) && (start == slice@.len() || !(slice@[start] == 0x09u8 || slice@[start] == 0x0au8 || slice@[start] == 0x0cu8 || slice@[start] == 0x0du8 || slice@[start] == 0x20u8)) && (forall|i: int| (i >= end && slice@.len() > i) ==> (slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8)) && (end == start || !(slice@[end - 1] == 0x09u8 || slice@[end - 1] == 0x0au8 || slice@[end - 1] == 0x0cu8 || slice@[end - 1] == 0x0du8 || slice@[end - 1] == 0x20u8)) && ret@ == slice@.subrange(start, end)` |
| `core::slice::trim_ascii_end` | `slice@.len() >= result@.len(); result@ == slice@.subrange(0, result@.len() as int); forall|i: int| i >= (result@.len() as int) && slice@.len() > i ==> (slice@[i] == 9 || slice@[i] == 10 || slice@[i] == 12 || slice@[i] == 13 || slice@[i] == 32); result@.len() > 0 ==> !(slice@[(result@.len() as int) - 1] == 9 || slice@[(result@.len() as int) - 1] == 10 || slice@[(result@.len() as int) - 1] == 12 || slice@[(result@.len() as int) - 1] == 13 || slice@[(result@.len() as int) - 1] == 32)` |
| `core::slice::trim_ascii_start` | `exists|start: int| start >= 0 && slice@.len() >= start && ret@ == slice@.subrange(start, slice@.len() as int) && (forall|i: int| i >= 0 && start > i ==> slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8) && (slice@.len() > start ==> !(slice@[start] == 0x09u8 || slice@[start] == 0x0au8 || slice@[start] == 0x0cu8 || slice@[start] == 0x0du8 || slice@[start] == 0x20u8))` |
| `core::str::ceil_char_boundary` | `s.spec_bytes().len() >= res as int; is_char_boundary(s.spec_bytes(), res as int); index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(); s.spec_bytes().len() >= index as int ==> res as int >= index as int; forall|i: int| i >= index as int && s.spec_bytes().len() >= i && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> i >= res as int; index as int + 3 >= res as int` |
| `core::str::eq_ignore_ascii_case` | `res == (s.spec_bytes().len() == other.spec_bytes().len() && forall|i: int| i >= 0 && s.spec_bytes().len() > i ==> (if s.spec_bytes()[i] >= 65 && 90 >= s.spec_bytes()[i] { s.spec_bytes()[i] as int + 32 } else { s.spec_bytes()[i] as int }) == (if other.spec_bytes()[i] >= 65 && 90 >= other.spec_bytes()[i] { other.spec_bytes()[i] as int + 32 } else { other.spec_bytes()[i] as int }))` |
| `core::str::floor_char_boundary` | `index >= res; s.spec_bytes().len() >= res as int; is_char_boundary(s.spec_bytes(), res as int); index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(); forall|i: int| index as int >= i && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> res as int >= i` |
| `core::str::trim_ascii` | `ret@ == (s@.fold_left((Seq::<char>::empty(), Seq::<char>::empty()), |state: (Seq<char>, Seq<char>), c: char| { let code = c as nat; if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 { if state.0.len() == 0 { state } else { (state.0, state.1.push(c)) } } else { ((state.0 + state.1).push(c), Seq::<char>::empty()) } })).0` |
| `core::str::trim_ascii_end` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> (s@[i] as nat == 0x09 || s@[i] as nat == 0x0a || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d || s@[i] as nat == 0x20); res@.len() > 0 ==> !(res@.last() as nat == 0x09 || res@.last() as nat == 0x0a || res@.last() as nat == 0x0c || res@.last() as nat == 0x0d || res@.last() as nat == 0x20)` |
| `core::str::trim_ascii_start` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> (s@[i] as nat == 0x09 || s@[i] as nat == 0x0a || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d || s@[i] as nat == 0x20)) && (s@.len() > start ==> !(s@[start] as nat == 0x09 || s@[start] as nat == 0x0a || s@[start] as nat == 0x0c || s@[start] as nat == 0x0d || s@[start] as nat == 0x20))` |
| `core::str::trim_end` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000); res@.len() > 0 ==> !((res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat) || res@.last() as nat == 0x0020 || res@.last() as nat == 0x0085 || res@.last() as nat == 0x00a0 || res@.last() as nat == 0x1680 || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat) || res@.last() as nat == 0x2028 || res@.last() as nat == 0x2029 || res@.last() as nat == 0x202f || res@.last() as nat == 0x205f || res@.last() as nat == 0x3000)` |
| `core::str::trim_left` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000)) && (s@.len() > start ==> !((s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat) || s@[start] as nat == 0x0020 || s@[start] as nat == 0x0085 || s@[start] as nat == 0x00a0 || s@[start] as nat == 0x1680 || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat) || s@[start] as nat == 0x2028 || s@[start] as nat == 0x2029 || s@[start] as nat == 0x202f || s@[start] as nat == 0x205f || s@[start] as nat == 0x3000))` |
| `core::str::trim_right` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000); res@.len() > 0 ==> !((res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat) || res@.last() as nat == 0x0020 || res@.last() as nat == 0x0085 || res@.last() as nat == 0x00a0 || res@.last() as nat == 0x1680 || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat) || res@.last() as nat == 0x2028 || res@.last() as nat == 0x2029 || res@.last() as nat == 0x202f || res@.last() as nat == 0x205f || res@.last() as nat == 0x3000)` |
| `core::str::trim_start` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000)) && (s@.len() > start ==> !((s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat) || s@[start] as nat == 0x0020 || s@[start] as nat == 0x0085 || s@[start] as nat == 0x00a0 || s@[start] as nat == 0x1680 || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat) || s@[start] as nat == 0x2028 || s@[start] as nat == 0x2029 || s@[start] as nat == 0x202f || s@[start] as nat == 0x205f || s@[start] as nat == 0x3000))` |
| `std::collections::HashMap::remove_entry` | `match result {
            Some((key, value)) => {
                &&& contains_borrowed_key(old(m)@, k)
                &&& sets_borrowed_key_to_key(old(m)@.dom(), k, &key)
                &&& old(m)@.contains_key(key)
                &&& old(m)@[key] == value
                &&& final(m)@ == old(m)@.remove(key)
            },
            None => {
                &&& !contains_borrowed_key(old(m)@, k)
                &&& final(m)@ == old(m)@
            },
        }` |
| `std::collections::HashSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `std::collections::HashSet::is_subset` | `result == m@.subset_of(other@)` |
| `std::collections::HashSet::is_superset` | `result == other@.subset_of(m@)` |
| `std::collections::HashSet::replace` | `final(m)@ == old(m)@.insert(value); match result { core::option::Option::Some(replaced) => old(m)@.contains(replaced) && replaced == value, core::option::Option::None => !old(m)@.contains(value), }` |
| `std::collections::HashSet::take` | `sets_differ_by_borrowed_key(old(m)@, final(m)@, value); match result {
            Some(v) => {
                &&& set_contains_borrowed_key(old(m)@, value)
                &&& sets_borrowed_key_to_key(old(m)@, value, &v)
                &&& old(m)@.contains(v)
                &&& final(m)@ == old(m)@.remove(v)
            },
            None => {
                &&& !set_contains_borrowed_key(old(m)@, value)
                &&& final(m)@ == old(m)@
            },
        }` |
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
| `core::str::trim` | `res@ == (s@.fold_left((Seq::<char>::empty(), Seq::<char>::empty()), |state: (Seq<char>, Seq<char>), c: char| { let code = c as nat; if (code >= 0x0009 && 0x000d >= code) || code == 0x0020 || code == 0x0085 || code == 0x00a0 || code == 0x1680 || (code >= 0x2000 && 0x200a >= code) || code == 0x2028 || code == 0x2029 || code == 0x202f || code == 0x205f || code == 0x3000 { if state.0.len() == 0 { state } else { (state.0, state.1.push(c)) } } else { ((state.0 + state.1).push(c), Seq::<char>::empty()) } })).0` |

## Semantic-gated candidates

94 of 104 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.

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
| `alloc::collections::BTreeSet::is_subset` | `result == this@.subset_of(other@)` |
| `alloc::collections::BTreeSet::is_superset` | `result == other@.subset_of(this@)` |
| `alloc::collections::BTreeSet::last` | `match result { core::option::Option::Some(value) => { &&& !m@.is_empty() &&& *value == m@.find_unique_maximal(|x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,) &&& m@.contains(*value) &&& forall|x: T| #[trigger] m@.contains(x) ==> x.cmp_spec(value) != core::cmp::Ordering::Greater }, core::option::Option::None => m@.is_empty(), }` |
| `alloc::collections::BTreeSet::pop_first` | `if old(m)@.is_empty() { &&& result is None &&& final(m)@ == old(m)@ } else { let first = choose|candidate: T| { &&& old(m)@.contains(candidate) &&& forall|element: T| old(m)@.contains(element) ==> candidate.cmp_spec(&element) != Ordering::Greater }; &&& result == Some(first) &&& old(m)@.contains(first) &&& forall|element: T| old(m)@.contains(element) ==> first.cmp_spec(&element) != Ordering::Greater &&& final(m)@ == old(m)@.remove(first) }` |
| `alloc::collections::BTreeSet::pop_last` | `match result {
            core::option::Option::Some(value) => {
                &&& !old(m)@.is_empty()
                &&& value == old(m)@.find_unique_maximal(
                    |x: T, y: T| x.cmp_spec(&y) != core::cmp::Ordering::Greater,
                )
                &&& old(m)@.contains(value)
                &&& final(m)@ == old(m)@.remove(value)
                &&& forall|x: T| #[trigger] old(m)@.contains(x) ==>
                    x.cmp_spec(&value) != core::cmp::Ordering::Greater
            },
            core::option::Option::None => {
                &&& old(m)@.is_empty()
                &&& final(m)@ == old(m)@
            },
        }` |
| `alloc::collections::BTreeSet::replace` | `{ let matching = old(m)@.filter(|existing: T| existing.cmp_spec(&value) == Ordering::Equal); if matching.is_empty() { &&& result is None &&& final(m)@ == old(m)@.insert(value) } else { let replaced = matching.choose(); &&& result == Some(replaced) &&& old(m)@.contains(replaced) &&& replaced.cmp_spec(&value) == Ordering::Equal &&& final(m)@ == old(m)@.remove(replaced).insert(value) } }` |
| `alloc::string::String::extend_from_within` | `final(s)@ == old(s)@ + decode_utf8(encode_utf8(old(s)@).subrange(slice_range_start(&src), slice_range_end(&src, encode_utf8(old(s)@).len())))` |
| `alloc::string::String::insert` | `final(s)@ == decode_utf8(encode_utf8(old(s)@).subrange(0, idx as int)) + seq![ch] + decode_utf8(encode_utf8(old(s)@).subrange(idx as int, encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::insert_str` | `final(s)@ == decode_utf8(encode_utf8(old(s)@).subrange(0, idx as int)) + string@ + decode_utf8(encode_utf8(old(s)@).subrange(idx as int, encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::is_empty` | `res == (s@.len() == 0)` |
| `alloc::string::String::len` | `res as nat == vstd::utf8::encode_utf8(s@).len()` |
| `alloc::string::String::pop` | `old(s)@.len() == 0 ==> res == core::option::Option::None && final(s)@ == old(s)@; old(s)@.len() > 0 ==> res == core::option::Option::Some(old(s)@[old(s)@.len() - 1]) && final(s)@ == old(s)@.subrange(0, old(s)@.len() - 1)` |
| `alloc::string::String::push` | `final(s)@ == old(s)@.push(ch)` |
| `alloc::string::String::push_str` | `final(s)@ == old(s)@ + string@` |
| `alloc::string::String::remove` | `res == old(s)@[idx as int]; final(s)@ == old(s)@.remove(idx as int)` |
| `alloc::string::String::split_off` | `final(s)@ == vstd::utf8::decode_utf8(vstd::utf8::encode_utf8(old(s)@).subrange(0, at as int)); res@ == vstd::utf8::decode_utf8(vstd::utf8::encode_utf8(old(s)@).subrange(at as int, vstd::utf8::encode_utf8(old(s)@).len() as int))` |
| `alloc::string::String::truncate` | `final(s)@ == if encode_utf8(old(s)@).len() > new_len as int { decode_utf8(encode_utf8(old(s)@).subrange(0, new_len as int)) } else { old(s)@ }` |
| `alloc::vec::Vec::into_flattened` | `flattened@ == vec@.map_values(|array: [T; N]| array@).flatten()` |
| `core::array::from_ref` | `out@ == seq![*s]` |
| `core::cmp::min` | `match v2.cmp_spec(&v1) { core::cmp::Ordering::Less => r == v2, core::cmp::Ordering::Equal => r == v1, core::cmp::Ordering::Greater => r == v1, }` |
| `core::hint::select_unpredictable` | `result == if condition { true_val } else { false_val }` |
| `core::mem::min_align_of` | `res as nat == align_of::<T>()` |
| `core::mem::min_align_of_val` | `res as nat == spec_align_of_val::<T>(val)` |
| `core::ops::Range::is_empty` | `ret == !r.start.is_lt(&r.end)` |
| `core::ops::RangeInclusive::into_inner` | `ret.0 == range@.start; ret.1 == range@.end` |
| `core::ops::RangeInclusive::is_empty` | `ret == (r@.exhausted || !r@.start.is_le(&r@.end))` |
| `core::ops::RangeInclusive::start` | `ret == r@.start` |
| `core::option::Option::and` | `option.is_none() ==> res.is_none(); option.is_some() ==> res == optb` |
| `core::option::Option::flatten` | `res == match option { core::option::Option::Some(inner) => inner, core::option::Option::None => core::option::Option::None, }` |
| `core::option::Option::or` | `option.is_some() ==> res == option; option.is_none() ==> res == optb` |
| `core::option::Option::transpose` | `res == match option { core::option::Option::Some(core::result::Result::Ok(x)) => core::result::Result::Ok(core::option::Option::Some(x)), core::option::Option::Some(core::result::Result::Err(e)) => core::result::Result::Err(e), core::option::Option::None => core::result::Result::Ok(core::option::Option::None), }` |
| `core::option::Option::unzip` | `res == match option { Some((a, b)) => (Some(a), Some(b)), None => (None, None), }` |
| `core::option::Option::xor` | `res == match (option, optb) {
            (Some(a), None) => Some(a),
            (None, Some(b)) => Some(b),
            _ => None,
        }` |
| `core::option::Option::zip` | `res == match (option, other) { (Some(a), Some(b)) => Some((a, b)), _ => None, }` |
| `core::result::Result::and` | `result is Ok ==> and_result == res; result is Err ==> and_result == Result::<U, E>::Err(result->Err_0)` |
| `core::result::Result::expect_err` | `e == result->Err_0` |
| `core::result::Result::flatten` | `result is Ok ==> flattened == result->Ok_0; result is Err ==> flattened is Err; result is Err ==> flattened->Err_0 == result->Err_0` |
| `core::result::Result::or` | `result is Ok ==> output == Result::<T, F>::Ok(result->Ok_0); result is Err ==> output == res` |
| `core::result::Result::transpose` | `transposed == (match result { core::result::Result::Ok(core::option::Option::Some(value)) => { core::option::Option::Some(core::result::Result::Ok(value)) }, core::result::Result::Ok(core::option::Option::None) => { core::option::Option::None }, core::result::Result::Err(error) => { core::option::Option::Some(core::result::Result::Err(error)) }, })` |
| `core::result::Result::unwrap_or` | `match result { core::result::Result::Ok(value) => t == value, core::result::Result::Err(_) => t == default, }` |
| `core::slice::as_chunks` | `{ let chunks = choose|candidate: Seq<[T; N]>| { &&& candidate.len() == slice@.len() / (N as nat) &&& forall|i: int| 0 <= i < candidate.len() ==> (#[trigger] candidate[i])@ == slice@.subrange(i * (N as int), (i + 1) * (N as int)) }; &&& ret.0@ == chunks &&& ret.0@.len() == slice@.len() / (N as nat) &&& ret.1@.len() == slice@.len() % (N as nat) &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len() &&& forall|i: int| 0 <= i < ret.0@.len() ==> (#[trigger] ret.0@[i])@ == slice@.subrange(i * (N as int), (i + 1) * (N as int)) &&& ret.1@ == slice@.subrange(((slice@.len() / (N as nat)) * (N as nat)) as int, slice@.len() as int) }` |
| `core::slice::as_flattened` | `ret@.len() == slice@.len() * N; ret@ == slice@.flat_map(|a: [T; N]| a@)` |
| `core::slice::binary_search` | `match result { core::result::Result::Ok(index) => { &&& slice@.len() > index &&& slice@[index as int].cmp_spec(x) == core::cmp::Ordering::Equal &&& forall|i: int| #![auto] i > index as int && slice@.len() > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Greater }, core::result::Result::Err(index) => { &&& slice@.len() >= index &&& forall|i: int| #![auto] i >= 0 && index as int > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Less &&& forall|i: int| #![auto] i >= index as int && slice@.len() > i ==> slice@[i].cmp_spec(x) == core::cmp::Ordering::Greater }, }` |
| `core::slice::contains` | `ret <==> exists|i: int| i >= 0 && slice@.len() > i && slice@[i].eq_spec(x)` |
| `core::slice::ends_with` | `result == (slice@.len() >= needle@.len() && (forall|i: int| i >= 0 && needle@.len() > i ==> needle@[i].eq_spec(&slice@[slice@.len() - needle@.len() + i])))` |
| `core::slice::eq_ignore_ascii_case` | `result == (slice@.len() == other@.len() && forall|i: int| i >= 0 && slice@.len() > i ==> (if slice@[i] >= 65 && 90 >= slice@[i] { slice@[i] as int + 32 } else { slice@[i] as int }) == (if other@[i] >= 65 && 90 >= other@[i] { other@[i] as int + 32 } else { other@[i] as int }))` |
| `core::slice::first_chunk` | `ret.is_some() <==> slice@.len() >= (N as int); ret.is_some() ==> ret.unwrap()@ == slice@.subrange(0, N as int)` |
| `core::slice::from_ref` | `r@ == seq![*s]` |
| `core::slice::is_ascii` | `ret == (forall|i: int| (i >= 0 && slice@.len() > i) ==> 0x7f >= slice@[i])` |
| `core::slice::is_sorted` | `ret <==> forall|i: int| i >= 0 && slice@.len() > i + 1 ==> (#[trigger] slice@[i]).is_le(&slice@[i + 1])` |
| `core::slice::last_chunk` | `slice.len() < N ==> ret.is_none(); N <= slice.len() ==> ret.is_some() && ret.unwrap()@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int)` |
| `core::slice::split_at_checked` | `ret.is_some() <==> mid <= slice@.len(); ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, mid as int); ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int)` |
| `core::slice::split_first` | `match ret {
            None => slice@.len() == 0,
            Some((first, rest)) => {
                &&& slice@.len() > 0
                &&& *first == slice@[0]
                &&& rest@ == slice@.subrange(1, slice@.len() as int)
            },
        }` |
| `core::slice::split_first_chunk` | `slice.len() < N ==> ret.is_none(); N <= slice.len() ==> ret.is_some() && ret.unwrap().0@ == slice@.subrange(0, N as int) && ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int)` |
| `core::slice::split_last` | `match ret { core::option::Option::None => slice@.len() == 0, core::option::Option::Some((last, init)) => { &&& slice@.len() > 0 &&& *last == slice@[slice@.len() as int - 1] &&& init@ == slice@.subrange(0, slice@.len() as int - 1) }, }` |
| `core::slice::split_last_chunk` | `match ret { core::option::Option::Some((init, last)) => { &&& slice@.len() >= N &&& init@ == slice@.subrange(0, slice@.len() as int - N as int) &&& last@ == slice@.subrange(slice@.len() as int - N as int, slice@.len() as int) }, core::option::Option::None => N > slice@.len(), }` |
| `core::slice::starts_with` | `result == (slice@.len() >= needle@.len() && (forall|i: int| i >= 0 && needle@.len() > i ==> needle@[i].eq_spec(&slice@[i])))` |
| `core::slice::trim_ascii` | `exists|start: int, end: int| start >= 0 && end >= start && slice@.len() >= end && (forall|i: int| (i >= 0 && start > i) ==> (slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8)) && (start == slice@.len() || !(slice@[start] == 0x09u8 || slice@[start] == 0x0au8 || slice@[start] == 0x0cu8 || slice@[start] == 0x0du8 || slice@[start] == 0x20u8)) && (forall|i: int| (i >= end && slice@.len() > i) ==> (slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8)) && (end == start || !(slice@[end - 1] == 0x09u8 || slice@[end - 1] == 0x0au8 || slice@[end - 1] == 0x0cu8 || slice@[end - 1] == 0x0du8 || slice@[end - 1] == 0x20u8)) && ret@ == slice@.subrange(start, end)` |
| `core::slice::trim_ascii_end` | `slice@.len() >= result@.len(); result@ == slice@.subrange(0, result@.len() as int); forall|i: int| i >= (result@.len() as int) && slice@.len() > i ==> (slice@[i] == 9 || slice@[i] == 10 || slice@[i] == 12 || slice@[i] == 13 || slice@[i] == 32); result@.len() > 0 ==> !(slice@[(result@.len() as int) - 1] == 9 || slice@[(result@.len() as int) - 1] == 10 || slice@[(result@.len() as int) - 1] == 12 || slice@[(result@.len() as int) - 1] == 13 || slice@[(result@.len() as int) - 1] == 32)` |
| `core::slice::trim_ascii_start` | `exists|start: int| start >= 0 && slice@.len() >= start && ret@ == slice@.subrange(start, slice@.len() as int) && (forall|i: int| i >= 0 && start > i ==> slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8 || slice@[i] == 0x0du8 || slice@[i] == 0x20u8) && (slice@.len() > start ==> !(slice@[start] == 0x09u8 || slice@[start] == 0x0au8 || slice@[start] == 0x0cu8 || slice@[start] == 0x0du8 || slice@[start] == 0x20u8))` |
| `core::str::ceil_char_boundary` | `s.spec_bytes().len() >= res as int; is_char_boundary(s.spec_bytes(), res as int); index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(); s.spec_bytes().len() >= index as int ==> res as int >= index as int; forall|i: int| i >= index as int && s.spec_bytes().len() >= i && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> i >= res as int; index as int + 3 >= res as int` |
| `core::str::eq_ignore_ascii_case` | `res == (s.spec_bytes().len() == other.spec_bytes().len() && forall|i: int| i >= 0 && s.spec_bytes().len() > i ==> (if s.spec_bytes()[i] >= 65 && 90 >= s.spec_bytes()[i] { s.spec_bytes()[i] as int + 32 } else { s.spec_bytes()[i] as int }) == (if other.spec_bytes()[i] >= 65 && 90 >= other.spec_bytes()[i] { other.spec_bytes()[i] as int + 32 } else { other.spec_bytes()[i] as int }))` |
| `core::str::floor_char_boundary` | `index >= res; s.spec_bytes().len() >= res as int; is_char_boundary(s.spec_bytes(), res as int); index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(); forall|i: int| index as int >= i && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> res as int >= i` |
| `core::str::trim_ascii` | `ret@ == (s@.fold_left((Seq::<char>::empty(), Seq::<char>::empty()), |state: (Seq<char>, Seq<char>), c: char| { let code = c as nat; if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 { if state.0.len() == 0 { state } else { (state.0, state.1.push(c)) } } else { ((state.0 + state.1).push(c), Seq::<char>::empty()) } })).0` |
| `core::str::trim_ascii_end` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> (s@[i] as nat == 0x09 || s@[i] as nat == 0x0a || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d || s@[i] as nat == 0x20); res@.len() > 0 ==> !(res@.last() as nat == 0x09 || res@.last() as nat == 0x0a || res@.last() as nat == 0x0c || res@.last() as nat == 0x0d || res@.last() as nat == 0x20)` |
| `core::str::trim_ascii_start` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> (s@[i] as nat == 0x09 || s@[i] as nat == 0x0a || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d || s@[i] as nat == 0x20)) && (s@.len() > start ==> !(s@[start] as nat == 0x09 || s@[start] as nat == 0x0a || s@[start] as nat == 0x0c || s@[start] as nat == 0x0d || s@[start] as nat == 0x20))` |
| `core::str::trim_end` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000); res@.len() > 0 ==> !((res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat) || res@.last() as nat == 0x0020 || res@.last() as nat == 0x0085 || res@.last() as nat == 0x00a0 || res@.last() as nat == 0x1680 || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat) || res@.last() as nat == 0x2028 || res@.last() as nat == 0x2029 || res@.last() as nat == 0x202f || res@.last() as nat == 0x205f || res@.last() as nat == 0x3000)` |
| `core::str::trim_left` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000)) && (s@.len() > start ==> !((s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat) || s@[start] as nat == 0x0020 || s@[start] as nat == 0x0085 || s@[start] as nat == 0x00a0 || s@[start] as nat == 0x1680 || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat) || s@[start] as nat == 0x2028 || s@[start] as nat == 0x2029 || s@[start] as nat == 0x202f || s@[start] as nat == 0x205f || s@[start] as nat == 0x3000))` |
| `core::str::trim_right` | `s@.len() >= res@.len(); res@ == s@.subrange(0, res@.len() as int); forall|i: int| i >= res@.len() as int && s@.len() > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000); res@.len() > 0 ==> !((res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat) || res@.last() as nat == 0x0020 || res@.last() as nat == 0x0085 || res@.last() as nat == 0x00a0 || res@.last() as nat == 0x1680 || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat) || res@.last() as nat == 0x2028 || res@.last() as nat == 0x2029 || res@.last() as nat == 0x202f || res@.last() as nat == 0x205f || res@.last() as nat == 0x3000)` |
| `core::str::trim_start` | `exists|start: int| start >= 0 && s@.len() >= start && res@ == s@.subrange(start, s@.len() as int) && (forall|i: int| i >= 0 && start > i ==> ((s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat) || s@[i] as nat == 0x0020 || s@[i] as nat == 0x0085 || s@[i] as nat == 0x00a0 || s@[i] as nat == 0x1680 || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat) || s@[i] as nat == 0x2028 || s@[i] as nat == 0x2029 || s@[i] as nat == 0x202f || s@[i] as nat == 0x205f || s@[i] as nat == 0x3000)) && (s@.len() > start ==> !((s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat) || s@[start] as nat == 0x0020 || s@[start] as nat == 0x0085 || s@[start] as nat == 0x00a0 || s@[start] as nat == 0x1680 || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat) || s@[start] as nat == 0x2028 || s@[start] as nat == 0x2029 || s@[start] as nat == 0x202f || s@[start] as nat == 0x205f || s@[start] as nat == 0x3000))` |
| `std::collections::HashSet::is_disjoint` | `result == m@.disjoint(other@)` |
| `std::collections::HashSet::is_subset` | `result == m@.subset_of(other@)` |
| `std::collections::HashSet::is_superset` | `result == other@.subset_of(m@)` |
| `std::collections::HashSet::replace` | `final(m)@ == old(m)@.insert(value); match result { core::option::Option::Some(replaced) => old(m)@.contains(replaced) && replaced == value, core::option::Option::None => !old(m)@.contains(value), }` |
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
| `core::str::trim` | `res@ == (s@.fold_left((Seq::<char>::empty(), Seq::<char>::empty()), |state: (Seq<char>, Seq<char>), c: char| { let code = c as nat; if (code >= 0x0009 && 0x000d >= code) || code == 0x0020 || code == 0x0085 || code == 0x00a0 || code == 0x1680 || (code >= 0x2000 && 0x200a >= code) || code == 0x2028 || code == 0x2029 || code == 0x202f || code == 0x205f || code == 0x3000 { if state.0.len() == 0 { state } else { (state.0, state.1.push(c)) } } else { ((state.0 + state.1).push(c), Seq::<char>::empty()) } })).0` |

## Per-target result

| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |
|---|---|---|---:|---|---:|---:|---|
| `alloc::collections::BTreeMap::append` | add_spec | add_spec | 1 | unsat | 1 | 0 | raw_btree_view_algebra |
| `alloc::collections::BTreeSet::append` | add_spec | add_spec | 1 | unsat | 1 | 0 | raw_btree_view_algebra |
| `alloc::string::String::clear` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::clone_from_slice` | skip | skip | 0 |  | 0 | 0 |  |
| `core::str::make_ascii_lowercase` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::split_off_last` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::first_key_value` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::as_bytes` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::each_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::end` | add_spec | add_spec | 1 | unsat | 1 | 1 | value_unspecified_after_exhaustion |
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
| `core::slice::split_off` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::vec::Vec::dedup` | add_spec | add_spec | 1 | unsat | 1 | 0 | dedup_pure_old_sequence_model |
| `core::slice::split_off_first` | skip | skip | 0 |  | 0 | 0 |  |
| `std::collections::HashMap::get_key_value` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::get_key_value` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeMap::split_off` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeSet::is_subset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_superset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::split_off` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeSet::take` | add_spec | add_spec | 1 | unsat | 1 | 0 | borrowed_key_domain_strengthening;borrowed_key_uniqueness_precondition |
| `alloc::string::String::extend_from_within` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::insert` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::insert_str` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::len` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::pop` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::push` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::push_str` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::remove` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::replace_range` | add_spec | add_spec | 1 | unsat | 1 | 0 | generic_range_snapshot_mismatch |
| `alloc::string::String::split_off` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::truncate` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::extend_from_within` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::vec::Vec::into_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::cmp::min` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::hint::select_unpredictable` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::min_align_of` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::min_align_of_val` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::needs_drop` | skip | skip | 0 |  | 0 | 0 |  |
| `core::mem::take` | skip | skip | 0 |  | 0 | 0 |  |
| `core::ops::Range::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::into_inner` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::start` | add_spec | add_spec | 1 | unsat | 1 | 1 | value_unspecified_after_exhaustion |
| `core::option::Option::and` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::flatten` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::transpose` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::unzip` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::xor` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::option::Option::zip` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::and` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::expect_err` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::flatten` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::transpose` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::unwrap_or` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::result::Result::unwrap_or_default` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::as_chunks` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::as_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::binary_search` | add_spec | add_spec | 1 | unsat | 1 | 1 | public_api_allows_any_matching_index |
| `core::slice::contains` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::element_offset` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::ends_with` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::fill` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_sorted` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::make_ascii_lowercase` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::make_ascii_uppercase` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::reverse` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::rotate_left` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::rotate_right` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::split_at_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::starts_with` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::strip_circumfix` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::strip_suffix` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::subslice_range` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::swap` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::swap_with_slice` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::trim_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::ceil_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::floor_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::make_ascii_uppercase` | skip | skip | 0 |  | 0 | 0 |  |
| `core::str::substr_range` | skip | skip | 0 |  | 0 | 0 |  |
| `core::str::trim_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_ascii_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_ascii_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_left` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_right` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashMap::remove_entry` | add_spec | add_spec | 1 | unsat | 1 | 0 | borrowed_key_uniqueness_precondition |
| `std::collections::HashSet::is_disjoint` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::is_subset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::is_superset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 | hash_equivalence_class_view_requires_review |
| `std::collections::HashSet::take` | add_spec | add_spec | 1 | unsat | 1 | 0 | borrowed_key_uniqueness_precondition |
| `core::slice::strip_prefix` | skip | skip | 0 |  | 0 | 0 |  |
| `core::slice::as_rchunks` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::borrow::Cow::into_owned` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:associated_type_or_projection;determinism_not_proved:unknown |
| `core::option::Option::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::pin::Pin::set` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::result::Result::as_deref` | add_spec | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::ends_with` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::get` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:associated_type_or_projection |
| `core::str::parse` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rfind` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatch_indices` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rmatches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_once` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplit_terminator` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::rsplitn` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::strip_circumfix` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_end_matches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_matches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `core::str::trim_right_matches` | skip | skip | 0 |  | 0 | 0 | classification:associated_type_or_projection |
| `alloc::collections::BTreeMap::first_entry` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::collections::BTreeMap::last_entry` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16_lossy` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16be` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16be_lossy` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16le` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf16le_lossy` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf8` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::from_utf8_lossy` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `alloc::string::String::into_boxed_str` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:complex_result_or_pattern_model;determinism_not_proved:unknown |
| `core::option::Option::as_pin_ref` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::slice::sort_unstable` | add_spec | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::contains` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::find` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::split_once` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::starts_with` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_prefix` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::strip_suffix` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::trim_left_matches` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::str::trim_start_matches` | skip | skip | 0 |  | 0 | 0 | classification:complex_result_or_pattern_model |
| `core::sync::atomic::Atomic::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::compare_exchange` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::Atomic::compare_exchange_weak` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
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
| `core::sync::atomic::Atomic::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::load` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::new` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::store` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::Atomic::swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::Atomic::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;determinism_unsupported_contract_form |
| `core::sync::atomic::AtomicBool::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_not` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicBool::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI16::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI32::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI64::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicI8::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
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
| `core::sync::atomic::AtomicPtr::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::compare_exchange_weak` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_and` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_or` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_add` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_ptr_sub` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::fetch_xor` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::load` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::new` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::store` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::AtomicPtr::swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicPtr::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU16::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU32::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU64::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
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
| `core::sync::atomic::AtomicU8::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicU8::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::compare_and_swap` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::fetch_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::get_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::try_update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::AtomicUsize::update` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state |
| `core::sync::atomic::compiler_fence` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::fence` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `core::sync::atomic::spin_loop_hint` | skip | skip | 0 |  | 0 | 0 | classification:concurrency_or_hidden_state;no_modeled_observable_output |
| `alloc::borrow::Cow::to_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::boxed::Box::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::BTreeMap::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::back_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::front_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::push_back_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::LinkedList::push_front_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::as_mut_slices` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::back_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::front_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::insert_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::make_contiguous` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::push_back_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::VecDeque::push_front_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_default` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::Entry::or_insert_with_key` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::OccupiedEntry::into_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::collections::btree_map::VacantEntry::insert` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::rc::Rc::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::rc::Rc::make_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::as_mut_str` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::as_mut_vec` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::string::String::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::sync::Arc::make_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::IntoIter::as_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::insert_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::push_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::vec::Vec::spare_capacity_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::IntoIter::as_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::as_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::each_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::array::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::Cell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::force_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::LazyCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::OnceCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::RefCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::cell::UnsafeCell::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::iter::Peekable::peek_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::mem::MaybeUninit::write` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::as_pin_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::get_or_insert_default` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::option::Option::get_or_insert_with` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::map_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::pin::Pin::static_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::NonNull::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::ptr::as_mut_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::result::Result::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::result::Result::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::ChunksExactMut::into_remainder` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::IterMut::into_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::RChunksExactMut::into_remainder` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::align_to_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_chunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_chunks_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_flattened_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_mut_array` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::as_rchunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::assume_init_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::first_chunk_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::from_raw_parts_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_disjoint_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_disjoint_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::last_chunk_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable_by` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::select_nth_unstable_by_key` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_at_mut_checked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_at_mut_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_first_chunk_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_first_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_last_chunk_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_last_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_first_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_last_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::split_off_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::write_clone_of_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::slice::write_copy_of_slice` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::as_bytes_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::from_utf8_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::from_utf8_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::get_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::slice_mut_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `core::str::split_at_mut_checked` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_disjoint_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_disjoint_unchecked_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::collections::HashMap::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::ffi::OsString::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::Path::as_mut_os_str` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::as_mut_os_string` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `std::path::PathBuf::leak` | skip | skip | 0 |  | 0 | 0 | classification:determinism_checker_unsupported |
| `alloc::fmt::format` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Arguments::as_str` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
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
| `core::fmt::NumBuffer::new` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::and` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::and_then` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::cloned` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::expect` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::expect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::flatten` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_err` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_err_and` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_ok` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::is_ok_and` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_err` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::map_or_else` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::Result::or` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:formatting_effect;determinism_not_proved:unknown |
| `core::fmt::Result::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::Result::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:formatting_effect;determinism_not_proved:unknown |
| `core::fmt::Result::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:formatting_effect;determinism_unsupported_contract_form |
| `core::fmt::from_fn` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `core::fmt::write` | skip | skip | 0 |  | 0 | 0 | classification:formatting_effect |
| `alloc::collections::VecDeque::binary_search_by` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::VecDeque::binary_search_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `alloc::collections::VecDeque::partition_point` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::pop_back_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown;structured_contract_mismatch |
| `alloc::collections::VecDeque::pop_front_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::collections::btree_map::Entry::and_modify` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::dedup_by_key` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::pop_if` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `alloc::vec::Vec::resize_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::array::from_fn` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::array::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::force` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::LazyCell::new` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::OnceCell::get_or_init` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::Ref::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefCell::replace_with` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::filter_map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cell::RefMut::map_split` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::cmp::Ordering::then_with` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown;structured_contract_mismatch |
| `core::cmp::max_by` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::max_by_key` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::min_by` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::cmp::min_by_key` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::future::poll_fn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::ops::Bound::map` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::ops::ControlFlow::map_break` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::ops::ControlFlow::map_continue` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::option::Option::filter` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::inspect` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_none_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::is_some_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::option::Option::map_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::map_or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::option::Option::take_if` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::ptr::NonNull::map_addr` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::and_then` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::inspect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `core::result::Result::is_err_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::is_ok_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::map_or` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::result::Result::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::map_or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::or_else` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::result::Result::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:higher_order_contract;determinism_not_proved:unknown |
| `core::slice::chunk_by` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::chunk_by_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::fill_with` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::is_sorted_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::partition_point` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplit_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::rsplitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::sort_unstable_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::sort_unstable_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract |
| `core::slice::split_inclusive_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::split_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::splitn_mut` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `std::panic::catch_unwind` | add_spec | skip | 0 |  | 0 | 0 | classification:higher_order_contract;determinism_unsupported_contract_form |
| `std::panic::take_hook` | skip | skip | 0 |  | 0 | 0 | classification:higher_order_contract |
| `core::slice::binary_search_by` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;borrowed_key_uniqueness_precondition |
| `core::slice::binary_search_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;structured_contract_mismatch |
| `core::slice::is_sorted_by_key` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:higher_order_contract;structured_contract_mismatch |
| `alloc::collections::BTreeMap::entry` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_keys` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::into_values` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::range_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeMap::values_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::intersection` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::range` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::symmetric_difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BTreeSet::union` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::iter` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::BinaryHeap::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::LinkedList::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::range_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::collections::VecDeque::retain_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::string::String::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::retain_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::vec::Vec::splice` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_eq` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_map` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::next_if_map_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::Peekable::peek` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::chain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::empty` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::from_fn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::once` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result;determinism_unsupported_contract_form |
| `core::iter::once_with` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_n` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::repeat_with` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::successors` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::iter::zip` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::option::Option::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::iter` | add_spec | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::result::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::array_windows` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_exact_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::chunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::escape_ascii` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_exact_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::rchunks_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::split_inclusive` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::splitn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::utf8_chunks` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::slice::windows` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::bytes` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::char_indices` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::encode_utf16` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_debug` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_default` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::escape_unicode` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::lines_any` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::match_indices` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::matches` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_ascii_whitespace` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_inclusive` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_terminator` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::split_whitespace` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `core::str::splitn` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_keys` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::into_values` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashMap::values_mut` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::drain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::extract_if` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::intersection` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::retain` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::symmetric_difference` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::collections::HashSet::union` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `std::path::Path::iter` | skip | skip | 0 |  | 0 | 0 | classification:iterator_or_adapter_result |
| `alloc::alloc::handle_alloc_error` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::append` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::into_sorted_vec` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::into_vec` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::peek` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::peek_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::pop` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::BinaryHeap::push` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::append` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::back` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::contains` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::front` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::pop_back` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::pop_front` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::push_back` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::push_front` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::LinkedList::split_off` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::as_slices` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::back` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::binary_search` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::contains` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::front` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::rotate_left` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::rotate_right` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::swap` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::swap_remove_back` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::VecDeque::swap_remove_front` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::Entry::insert_entry` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::Entry::key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::insert` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::remove` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::OccupiedEntry::remove_entry` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::insert_entry` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::into_key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::collections::btree_map::VacantEntry::key` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::as_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::as_bytes_with_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::as_c_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::from_vec_with_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::into_boxed_c_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::into_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::into_bytes_with_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::into_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::CString::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::FromVecWithNulError::as_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::FromVecWithNulError::into_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::IntoStringError::into_cstring` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::IntoStringError::utf8_error` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::NulError::into_vec` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::ffi::NulError::nul_position` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::upgrade` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::rc::Weak::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::Drain::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::FromUtf8Error::as_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::FromUtf8Error::into_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::string::FromUtf8Error::utf8_error` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::upgrade` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::sync::Weak::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::Drain::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `alloc::vec::IntoIter::as_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::alloc::Layout::align` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::alloc::Layout::align_to` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::array` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::extend` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::extend_packed` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::for_value` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::from_size_align` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::alloc::Layout::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::pad_to_align` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::repeat` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::repeat_packed` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::alloc::Layout::size` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::array::IntoIter::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::array::IntoIter::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::as_array_of_cells` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::as_slice_of_cells` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::replace` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::LazyCell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::get` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::set` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::OnceCell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Ref::clone` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::borrow` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::replace` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::take` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::RefCell::try_borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::UnsafeCell::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cmp::Ordering::is_eq` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_ge` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_gt` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_le` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_lt` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::is_ne` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::reverse` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::cmp::Ordering::then` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ffi::CStr::count_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::from_bytes_until_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::from_bytes_with_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::to_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::to_bytes_with_nul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ffi::CStr::to_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::Ready::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::pending` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::future::ready` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::is_ipv4` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::is_ipv6` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::is_loopback` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::is_multicast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::is_unspecified` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::IpAddr::to_canonical` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::from_bits` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::from_octets` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_broadcast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_documentation` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_link_local` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_loopback` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_multicast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_private` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::is_unspecified` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::octets` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::to_bits` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::to_ipv6_compatible` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv4Addr::to_ipv6_mapped` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::from_bits` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::from_octets` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::from_segments` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::is_loopback` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::is_multicast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::is_unicast_link_local` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::is_unique_local` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::is_unspecified` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::octets` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::segments` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::to_bits` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::to_canonical` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::to_ipv4` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::Ipv6Addr::to_ipv4_mapped` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::is_ipv4` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::is_ipv6` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::set_ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddr::set_port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV4::ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV4::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV4::port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV4::set_ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV4::set_port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::flowinfo` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::scope_id` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::set_flowinfo` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::set_ip` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::set_port` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::net::SocketAddrV6::set_scope_id` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::Bound::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::Bound::cloned` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_not_proved:unknown |
| `core::ops::ControlFlow::break_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::ControlFlow::break_value` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::ControlFlow::continue_ok` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::ControlFlow::continue_value` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::ControlFlow::is_break` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::ControlFlow::is_continue` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::ops::RangeFrom::contains` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::RangeTo::contains` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ops::RangeToInclusive::contains` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::Location::caller` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::Location::column` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::Location::file` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `core::panic::Location::file_as_c_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::Location::line` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicInfo::message` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::panic::PanicMessage::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::into_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::pin::Pin::static_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::addr` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::align_offset` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::cast` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::dangling` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::expose_provenance` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::from_mut` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::from_ref` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_aligned` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::slice_from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::with_addr` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::with_exposed_provenance` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::ptr::NonNull::without_provenance` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::ChunksExact::remainder` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::Iter::as_slice` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::IterMut::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::slice::RChunksExact::remainder` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::CharIndices::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::CharIndices::offset` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Chars::as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Chunk::invalid` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Chunk::valid` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Error::error_len` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::str::Utf8Error::valid_up_to` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::abs_diff` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_micros` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_millis` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_nanos` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_secs` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_secs_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::as_secs_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::checked_add` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::checked_div` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::checked_mul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::checked_sub` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::div_duration_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::div_duration_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::div_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::div_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_hours` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_micros` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_millis` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_mins` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_nanos` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_nanos_u128` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_secs` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_secs_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::from_secs_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::is_zero` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::mul_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::mul_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::saturating_add` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::saturating_mul` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::saturating_sub` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::subsec_micros` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::subsec_millis` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::subsec_nanos` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::try_from_secs_f32` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::time::Duration::try_from_secs_f64` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::as_encoded_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::display` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsStr::eq_ignore_ascii_case` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
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
| `std::ffi::OsString::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_boxed_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_encoded_bytes` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::into_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::ffi::OsString::push` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicHookInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicHookInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicHookInfo::payload_as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::location` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction;determinism_unsupported_contract_form |
| `std::panic::PanicInfo::payload` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::PanicInfo::payload_as_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::panic_any` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::panic::resume_unwind` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Component::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Components::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Iter::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::ancestors` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
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
| `std::path::Path::is_empty` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_file` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_relative` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Path::is_symlink` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
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
| `std::path::PathBuf::as_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::clear` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_boxed_path` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::into_os_string` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::new` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::pop` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::push` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::set_extension` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PathBuf::set_file_name` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::Prefix::is_verbatim` | add_spec | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::as_os_str` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::PrefixComponent::kind` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::absolute` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `std::path::is_separator` | skip | skip | 0 |  | 0 | 0 | classification:needs_new_vstd_abstraction |
| `core::cell::Cell::set` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::Cell::swap` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::Cell::update` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::cell::RefCell::swap` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::hint::cold_path` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::hint::spin_loop` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::mem::drop` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `core::mem::forget` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `std::panic::set_hook` | skip | skip | 0 |  | 0 | 0 | classification:no_modeled_observable_output;no_modeled_observable_output |
| `alloc::boxed::Box::into_pin` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_uninit_slice` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::boxed::Box::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::new_zeroed_slice` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::pin` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::boxed::Box::write` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::downcast` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::downgrade` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_cyclic` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_uninit` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::rc::Rc::new_uninit_slice` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::rc::Rc::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::new_zeroed_slice` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::pin` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::rc::Rc::unwrap_or_clone` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::rc::Rc::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downcast` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::downgrade` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::into_inner` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::sync::Arc::new_cyclic` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_uninit` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::sync::Arc::new_uninit_slice` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::sync::Arc::new_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::new_zeroed_slice` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::pin` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::ptr_eq` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::strong_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::sync::Arc::try_unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_unsupported_contract_form |
| `alloc::sync::Arc::unwrap_or_clone` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:ownership_or_uninitialized_model;determinism_not_proved:unknown |
| `alloc::sync::Arc::weak_count` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `core::mem::MaybeUninit::zeroed` | skip | skip | 0 |  | 0 | 0 | classification:ownership_or_uninitialized_model |
| `alloc::collections::BinaryHeap::capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::shrink_to` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::shrink_to_fit` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::try_reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::try_reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::BinaryHeap::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::capacity` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:representation_or_allocator;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::reserve_exact` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::shrink_to` | add_spec | add_spec | 0 |  | 0 | 0 | classification:representation_or_allocator;contract_typecheck_failed |
| `alloc::collections::VecDeque::shrink_to_fit` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:representation_or_allocator |
| `alloc::collections::VecDeque::try_reserve` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:representation_or_allocator;determinism_not_proved:unknown |
| `alloc::collections::VecDeque::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::string::String::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::string::String::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `alloc::string::String::with_capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::vec::Vec::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::vec::Vec::reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::vec::Vec::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `alloc::vec::Vec::try_reserve_exact` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `core::alloc::Layout::dangling_ptr` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `core::ptr::fn_addr_eq` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::hasher` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashMap::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::with_capacity_and_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashMap::with_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::capacity` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::hasher` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::shrink_to` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::shrink_to_fit` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::try_reserve` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::collections::HashSet::with_capacity_and_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator;determinism_unsupported_contract_form |
| `std::collections::HashSet::with_hasher` | add_spec | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::shrink_to_fit` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::try_reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::ffi::OsString::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::shrink_to_fit` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::try_reserve_exact` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
| `std::path::PathBuf::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:representation_or_allocator |
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
| `std::io::LineWriter::get_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::get_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::into_inner` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::new` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::LineWriter::with_capacity` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeReader::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::PipeWriter::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stderr::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lines` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::io::Stdin::read_line` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::io::Stdout::lock` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::net::TcpStream::connect_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::local_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::nodelay` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::TcpStream::peek` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:runtime_or_hidden_state |
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
| `std::net::UdpSocket::peek` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peek_from` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::peer_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::net::UdpSocket::recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::os::fd::BorrowedFd::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::BorrowedFd::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::fd::OwnedFd::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::os::unix::net::UnixDatagram::send` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::send_to_addr` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_nonblocking` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_read_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::unix::net::UnixDatagram::set_write_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::os::windows::fs::symlink_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::fs::symlink_file` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedHandle::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::borrow_raw` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::BorrowedSocket::try_clone_to_owned` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrInvalid::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::HandleOrNull::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedHandle::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::os::windows::io::OwnedSocket::try_clone` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::id` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::kill` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::try_wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Child::wait_with_output` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::arg` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::args` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::current_dir` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_clear` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::env_remove` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::process::Command::envs` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::sync::LockResult::and` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::and_then` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::LockResult::as_deref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::as_mut` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown;structured_contract_mismatch |
| `std::sync::LockResult::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::expect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::flatten` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::inspect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_err_and` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::is_ok_and` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_default` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::map_or_else` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::ok` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::or` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::LockResult::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::LockResult::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
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
| `std::sync::OnceLock::set` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::sync::TryLockResult::and_then` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::TryLockResult::as_deref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::expect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::flatten` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::inspect_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::is_err_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::TryLockResult::is_ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::is_ok_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::TryLockResult::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::map_or` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::TryLockResult::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::TryLockResult::unwrap_or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::TryLockResult::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::sync::TryLockResult::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::sync::WaitTimeoutResult::timed_out` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::recv_timeout` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Receiver::try_recv` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::sync::mpsc::Sender::send` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::thread::Result::and_then` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::thread::Result::as_deref` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_deref_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::as_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::copied` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::expect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::expect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::flatten` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::inspect_err` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::is_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_err_and` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::thread::Result::is_ok` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::is_ok_and` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::iter_mut` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_default` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::map_or_else` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::ok` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::or` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::thread::Result::transpose` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_err` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_err_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Result::unwrap_or` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Result::unwrap_or_else` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:runtime_or_hidden_state;determinism_not_proved:unknown |
| `std::thread::Result::unwrap_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;determinism_unsupported_contract_form |
| `std::thread::Scope::spawn` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::is_finished` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::join` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::ScopedJoinHandle::thread` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::id` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::name` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::thread::Thread::unpark` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state;no_modeled_observable_output |
| `std::thread::available_parallelism` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
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
| `std::time::SystemTime::checked_sub` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::duration_since` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::elapsed` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTime::now` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `std::time::SystemTimeError::duration` | skip | skip | 0 |  | 0 | 0 | classification:runtime_or_hidden_state |
| `alloc::boxed::BoxedArrayIntoIter::as_mut_slice` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `alloc::boxed::BoxedArrayIntoIter::as_slice` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
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
| `core::io::Result::map_err` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
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
| `std::path::PathBuf::into_string` | skip | skip | 0 |  | 0 | 0 | classification:toolchain_unavailable;no_modeled_observable_output;not_in_verus_rust_1_96 |
| `alloc::borrow::ToOwned::clone_into` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `alloc::borrow::ToOwned::to_owned` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::alloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::alloc_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::alloc::GlobalAlloc::dealloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::alloc::GlobalAlloc::realloc` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::borrow::Borrow::borrow` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::borrow::BorrowMut::borrow_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::clone::Clone::clone_from` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::convert::AsMut::as_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::convert::AsRef::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::error::Error::cause` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::error::Error::description` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::error::Error::source` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Binary::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Debug::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Display::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::LowerExp::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::LowerHex::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Octal::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Pointer::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::UpperExp::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::UpperHex::fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_char` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::fmt::Write::write_str` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::future::Future::poll` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::future::IntoFuture::into_future` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::nth_back` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfind` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::rfold` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::DoubleEndedIterator::try_rfold` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::ExactSizeIterator::len` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Extend::extend` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::by_ref` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::chain` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
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
| `core::iter::Iterator::for_each` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form;no_modeled_observable_output |
| `core::iter::Iterator::fuse` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::ge` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::gt` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::inspect` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration |
| `core::iter::Iterator::is_sorted` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::is_sorted_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::last` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::le` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::lt` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::map` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::map_while` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max` | add_spec | add_spec | 1 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::max_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::min_by_key` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::ne` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::nth` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::partial_cmp` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::partition` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::peekable` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::position` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::product` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::reduce` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::rposition` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::scan` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::size_hint` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::skip` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::skip_while` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::step_by` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::sum` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::take` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::take_while` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::try_fold` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::try_for_each` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::unzip` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Iterator::zip` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Product::product` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::iter::Sum::sum` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::AddAssign::add_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitAnd::bitand` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitAndAssign::bitand_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitOr::bitor` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitOrAssign::bitor_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitXor::bitxor` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::BitXorAssign::bitxor_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::DivAssign::div_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Drop::drop` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::IndexMut::index_mut` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::MulAssign::mul_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Not::not` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::RangeBounds::contains` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration |
| `core::ops::Rem::rem` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::RemAssign::rem_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Shl::shl` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::ShlAssign::shl_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::Shr::shr` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::ShrAssign::shr_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::ops::SubAssign::sub_assign` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `core::str::FromStr::from_str` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::consume` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::fill_buf` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::lines` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::read_line` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::read_until` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::skip_until` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::BufRead::split` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::IsTerminal::is_terminal` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::by_ref` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::bytes` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::chain` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_exact` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_to_end` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_to_string` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::read_vectored` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Read::take` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::by_ref` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::flush` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write` | add_spec | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_all` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_fmt` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::io::Write::write_vectored` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::net::ToSocketAddrs::to_socket_addrs` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::AsFd::as_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::AsRawFd::as_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::FromRawFd::from_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::fd::IntoRawFd::into_raw_fd` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
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
| `std::os::windows::io::AsHandle::as_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawHandle::as_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsRawSocket::as_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::AsSocket::as_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::FromRawHandle::from_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::FromRawSocket::from_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::IntoRawHandle::into_raw_handle` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::os::windows::io::IntoRawSocket::into_raw_socket` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `std::process::Termination::report` | skip | skip | 0 |  | 0 | 0 | classification:trait_contract_integration;determinism_unsupported_contract_form |
| `alloc::alloc::alloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::alloc_zeroed` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::alloc::dealloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::alloc::realloc` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_mut_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::assume_init` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::downcast` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::boxed::Box::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::from_vec_with_nul_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::ffi::CString::into_raw` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::assume_init` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::decrement_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::rc::Rc::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Rc::increment_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::rc::Rc::into_raw` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::rc::Weak::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::str::from_boxed_utf8_unchecked` | add_spec | add_spec | 1 | unknown | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_not_proved:unknown |
| `alloc::string::String::from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::from_utf8_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::string::String::into_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::assume_init` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::decrement_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::sync::Arc::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Arc::increment_strong_count` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `alloc::sync::Arc::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::from_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::sync::Weak::into_raw` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::as_mut_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::into_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `alloc::vec::Vec::set_len` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::alloc::Layout::from_size_align_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::Cell::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefCell::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::RefCell::try_borrow_unguarded` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::UnsafeCell::get` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::cell::UnsafeCell::raw_get` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:verus_error;classification:unsafe_or_representation_sensitive;trivial_equal_fn |
| `core::ffi::CStr::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::from_bytes_with_nul_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ffi::CStr::from_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::hint::assert_unchecked` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::intrinsics::copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::intrinsics::copy_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::intrinsics::transmute` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::intrinsics::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::mem::ManuallyDrop::drop` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::ManuallyDrop::take` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_mut_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::mem::MaybeUninit::assume_init_drop` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::MaybeUninit::assume_init_read` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::transmute_copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::uninitialized` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::mem::zeroed` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::option::Option::copied` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::option::Option::unwrap_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::into_inner_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::map_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::pin::Pin::new_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::copy_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_from_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_to` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::copy_to_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::drop_in_place` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::new` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::new_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::read_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::replace` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::NonNull::swap` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::NonNull::write_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::addr_eq` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::align_offset` | add_spec | add_spec | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;contract_typecheck_failed |
| `core::ptr::as_array` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_mut_array` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_ref` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::as_ref_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_add` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::byte_sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::cast` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive;trivial_equal_fn |
| `core::ptr::cast_const` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::cast_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::copy` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_from_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_to` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::copy_to_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::dangling` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::dangling_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::drop_in_place` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::eq` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::expose_provenance` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::from_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::from_ref` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::hash` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_aligned` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_empty` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::is_null` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::len` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::map_addr` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive;trivial_equal_fn |
| `core::ptr::offset` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::offset_from` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::offset_from_unsigned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::read_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::replace` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::slice_from_raw_parts` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::slice_from_raw_parts_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::sub` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::swap` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::swap_nonoverlapping` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::with_addr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::with_exposed_provenance` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::with_exposed_provenance_mut` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::without_provenance` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::without_provenance_mut` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::ptr::wrapping_add` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_add` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive;trivial_equal_fn |
| `core::ptr::wrapping_byte_offset` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_byte_sub` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_offset` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::wrapping_sub` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::ptr::write` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_bytes` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_unaligned` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::ptr::write_volatile` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;no_modeled_observable_output |
| `core::result::Result::cloned` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::copied` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::unwrap_err_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::result::Result::unwrap_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::align_to` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_chunks_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::as_mut_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_mut_ptr_range` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_ptr` | add_spec | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive;determinism_unsupported_contract_form |
| `core::slice::as_ptr_range` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_drop` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::assume_init_ref` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::from_raw_parts` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::get_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::slice::split_at_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_mut_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::as_ptr` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::from_utf8` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::get_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `core::str::slice_unchecked` | add_spec | add_spec | 1 | unsat | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsStr::from_encoded_bytes_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
| `std::ffi::OsString::from_encoded_bytes_unchecked` | skip | skip | 0 |  | 0 | 0 | classification:unsafe_or_representation_sensitive |
