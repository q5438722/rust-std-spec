# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `targets` | 101 |
| `initial_add_spec` | 98 |
| `initial_skip` | 3 |
| `final_add_spec` | 79 |
| `final_skip` | 22 |
| `typecheck_passed` | 79 |
| `det_unsat` | 78 |
| `det_sat` | 0 |
| `det_unknown` | 0 |
| `raw_reward` | 78 |
| `guarded_reward` | 78 |
| `semantic_guarded_reward` | 75 |
| `llm_errors` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 79 |
| `add_spec->skip` | 19 |
| `skip->skip` | 3 |

## Frequent issues

| Issue | Count |
|---|---:|
| `determinism_unsupported_contract_form` | 5 |
| `checker_status:runner_crash` | 1 |
| `structured_contract_mismatch` | 1 |

## Guarded-deterministic candidates

| Target | Ensures |
|---|---|
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

75 of 78 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.

| Target | Ensures |
|---|---|
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
| `alloc::collections::BTreeMap::split_off` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::BTreeSet::is_subset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::is_superset` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::pop_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::collections::BTreeSet::split_off` | add_spec | skip | 0 |  | 0 | 0 |  |
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
| `alloc::string::String::replace_range` | skip | skip | 0 |  | 0 | 0 |  |
| `alloc::string::String::split_off` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::string::String::truncate` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::vec::Vec::extend_from_within` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::vec::Vec::into_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::array::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::cmp::min` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::hint::select_unpredictable` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::min_align_of` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::min_align_of_val` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::mem::needs_drop` | skip | skip | 0 |  | 0 | 0 |  |
| `core::mem::take` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::ops::Range::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::into_inner` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::is_empty` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::ops::RangeInclusive::start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
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
| `core::result::Result::unwrap_or_default` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::as_chunks` | add_spec | add_spec | 1 |  | 0 | 0 | checker_status:runner_crash;structured_contract_mismatch |
| `core::slice::as_flattened` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::binary_search` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::contains` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::element_offset` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::ends_with` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::fill` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::from_ref` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::is_sorted` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::make_ascii_lowercase` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::make_ascii_uppercase` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::reverse` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::rotate_left` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::rotate_right` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::split_at_checked` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_first_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::split_last_chunk` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::starts_with` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::strip_circumfix` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::strip_suffix` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::subslice_range` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::slice::swap` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::swap_with_slice` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::trim_ascii` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_end` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::slice::trim_ascii_start` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::ceil_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::eq_ignore_ascii_case` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::floor_char_boundary` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::make_ascii_uppercase` | add_spec | skip | 0 |  | 0 | 0 |  |
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
| `std::collections::HashSet::replace` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `std::collections::HashSet::take` | add_spec | add_spec | 1 | unsat | 1 | 0 | borrowed_key_uniqueness_precondition |
| `core::slice::strip_prefix` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::slice::as_rchunks` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::str::trim` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
