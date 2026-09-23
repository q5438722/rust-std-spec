use vstd::prelude::*;
#[path = "../specs/slice/mod.rs"]
mod contracts;
use contracts::*;

verus! {

pub fn empty_domain() {
    let values: [u8; 0] = [];
    let s: &[u8] = &values;
    assert(len_post(s, 0));
    assert(is_empty_post(s, true));
    assert(first_post(s, None));
    assert(split_first_post(s, None));
    assert(split_last_post(s, None));
    assert(last_post(s, None));
    assert(!len_post(s, 1));
    assert(!is_empty_post(s, false));
}

pub fn singleton_domain() {
    let values = [17u8];
    let s: &[u8] = &values;
    let empty: &[u8] = &[];
    assert(empty@ =~= s@.subrange(1, 1));
    assert(empty@ =~= s@.subrange(0, 0));
    assert(len_post(s, 1));
    assert(is_empty_post(s, false));
    assert(first_post(s, Some(&values[0])));
    assert(split_first_post(s, Some((&values[0], empty))));
    assert(split_last_post(s, Some((&values[0], empty))));
    assert(last_post(s, Some(&values[0])));
    assert(!first_post(s, None));
    assert(!last_post(s, None));
}

pub fn ordered_domain() {
    let values = [10u8, 40, 30];
    let tail_values = [40u8, 30];
    let init_values = [10u8, 40];
    let s: &[u8] = &values;
    let tail: &[u8] = &tail_values;
    let init: &[u8] = &init_values;
    assert(tail@ =~= s@.subrange(1, 3));
    assert(init@ =~= s@.subrange(0, 2));
    assert(len_post(s, 3));
    assert(is_empty_post(s, false));
    assert(first_post(s, Some(&values[0])));
    assert(split_first_post(s, Some((&values[0], tail))));
    assert(split_last_post(s, Some((&values[2], init))));
    assert(last_post(s, Some(&values[2])));
    assert(!first_post(s, Some(&values[1])));
    assert(!split_first_post(s, Some((&values[0], init))));
    assert(!split_last_post(s, Some((&values[0], tail))));
    assert(!split_last_post(s, Some((&values[2], s))));
}

pub fn zero_sized_domain() {
    let values = [(), (), ()];
    let rest_values = [(), ()];
    let s: &[()] = &values;
    let rest: &[()] = &rest_values;
    assert(rest@ =~= s@.subrange(1, 3));
    assert(rest@ =~= s@.subrange(0, 2));
    assert(len_post(s, 3));
    assert(is_empty_post(s, false));
    assert(first_post(s, Some(&values[0])));
    assert(split_first_post(s, Some((&values[0], rest))));
    assert(split_last_post(s, Some((&values[2], rest))));
    assert(last_post(s, Some(&values[2])));
    assert(!split_first_post(s, Some((&values[0], s))));
}

pub struct NonCopy {
    pub value: u8,
}

pub fn non_copy_domain() {
    let values = [NonCopy { value: 10 }, NonCopy { value: 30 }];
    let tail_values = [NonCopy { value: 30 }];
    let init_values = [NonCopy { value: 10 }];
    let s: &[NonCopy] = &values;
    let tail: &[NonCopy] = &tail_values;
    let init: &[NonCopy] = &init_values;
    assert(tail@ =~= s@.subrange(1, 2));
    assert(init@ =~= s@.subrange(0, 1));
    assert(len_post(s, 2));
    assert(is_empty_post(s, false));
    assert(first_post(s, Some(&values[0])));
    assert(split_first_post(s, Some((&values[0], tail))));
    assert(split_last_post(s, Some((&values[1], init))));
    assert(last_post(s, Some(&values[1])));
    assert(!last_post(s, Some(&values[0])));
}

}
