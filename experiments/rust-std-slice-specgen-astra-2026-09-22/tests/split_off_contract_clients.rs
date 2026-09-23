use vstd::prelude::*;
#[path = "../specs/slice/split_off.rs"]
mod bindings;

verus! {

pub fn consecutive_first<T>(owner: &[T])
    requires owner@.len() >= 2,
{
    let mut remaining = owner;
    let first = remaining.split_off_first();
    let second = remaining.split_off_first();
    assert(first.is_some() && second.is_some());
    assert(*first.unwrap() == owner@[0]);
    assert(*second.unwrap() == owner@[1]);
    assert(remaining@ =~= owner@.subrange(2, owner@.len() as int));
}

pub fn consecutive_last<T>(owner: &[T])
    requires owner@.len() >= 2,
{
    let mut remaining = owner;
    let last = remaining.split_off_last();
    let penultimate = remaining.split_off_last();
    assert(last.is_some() && penultimate.is_some());
    assert(*last.unwrap() == owner@[owner@.len() - 1]);
    assert(*penultimate.unwrap() == owner@[owner@.len() - 2]);
    assert(remaining@ =~= owner@.subrange(0, owner@.len() - 2));
}

pub fn alternating_and_exhaustion<T>(owner: &[T])
    requires owner@.len() == 2,
{
    let mut remaining = owner;
    let first = remaining.split_off_first();
    let last = remaining.split_off_last();
    let exhausted_first = remaining.split_off_first();
    let exhausted_last = remaining.split_off_last();
    assert(first.is_some() && last.is_some());
    assert(*first.unwrap() == owner@[0]);
    assert(*last.unwrap() == owner@[1]);
    assert(exhausted_first.is_none() && exhausted_last.is_none());
    assert(remaining@ =~= seq![]);
}

pub fn first_slot_can_be_reassigned<'a, T>(owner: &'a [T], unrelated: &'a [T])
    requires owner@.len() > 0,
{
    let mut remaining = owner;
    let first = remaining.split_off_first();
    remaining = unrelated;
    assert(first.is_some() && *first.unwrap() == owner@[0]);
    assert(remaining@ == unrelated@);
}

pub fn last_slot_can_be_reassigned<'a, T>(owner: &'a [T], unrelated: &'a [T])
    requires owner@.len() > 0,
{
    let mut remaining = owner;
    let last = remaining.split_off_last();
    remaining = unrelated;
    assert(last.is_some() && *last.unwrap() == owner@[owner@.len() - 1]);
    assert(remaining@ == unrelated@);
}

pub fn first_outlives_the_local_slot<T>(owner: &[T])
    requires owner@.len() > 0,
{
    let first = {
        let mut remaining = owner;
        remaining.split_off_first()
    };
    assert(first.is_some() && *first.unwrap() == owner@[0]);
}

pub fn last_outlives_the_local_slot<T>(owner: &[T])
    requires owner@.len() > 0,
{
    let last = {
        let mut remaining = owner;
        remaining.split_off_last()
    };
    assert(last.is_some() && *last.unwrap() == owner@[owner@.len() - 1]);
}

}
