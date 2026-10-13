#![feature(allocator_api)]
#[path = "../slice_mod.rs"]
pub mod slice_mod;
#[path = "../slice_non_mod.rs"]
pub mod slice_non_mod;
#[path = "../slice_shared.rs"]
pub mod slice_shared;
#[path = "../vec_mod.rs"]
pub mod vec_mod;
#[path = "../vec_non_mod.rs"]
pub mod vec_non_mod;
pub mod slice_specs {
    pub use super::slice_shared::*;
}
pub mod vec_specs {}

use std::borrow::Cow;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

pub fn example_defaults() {
    let shared: &[u64] = Default::default();
    assert(shared@ == Seq::<u64>::empty());
    let mutable: &mut [u64] = Default::default();
    assert(mutable@ == Seq::<u64>::empty());
    let iter: core::slice::Iter<'_, u64> = Default::default();
    assert(IteratorSpec::remaining(&iter).len() == 0);
    let iter_mut: core::slice::IterMut<'_, u64> = Default::default();
    assert(IteratorSpec::remaining(&iter_mut).len() == 0);

    assert(false);
}

pub fn example_splitting() {
    let array = [10u64, 20, 30];
    let slice: &[u64] = &array;
    let (last, init) = slice.split_last().unwrap();
    assert(*last == 30);
    assert(init@ =~= seq![10u64, 20u64]);
    let (left, right) = unsafe { slice.split_at_unchecked(1) };
    assert(left@ =~= seq![10u64]);
    assert(right@ =~= seq![20u64, 30u64]);
    let mut remaining = slice;
    let first = remaining.split_off_first().unwrap();
    assert(*first == 10);
    let last = remaining.split_off_last().unwrap();
    assert(*last == 30);
    assert(remaining@ =~= seq![20u64]);

    assert(false);
}

pub fn example_mutable_splitting() {
    let mut array = [10u64, 20, 30];
    {
        let slice: &mut [u64] = &mut array;
        let (last, init) = slice.split_last_mut().unwrap();
        *last = 99;
        init[0] = 77;
    }
    assert(array@ =~= seq![77u64, 20u64, 99u64]);
    {
        let mut remaining: &mut [u64] = &mut array;
        {
            let first = remaining.split_off_first_mut().unwrap();
            *first = 11;
        }
        {
            let last = remaining.split_off_last_mut().unwrap();
            *last = 33;
        }
        remaining[0] = 22;
    }
    assert(array@ =~= seq![11u64, 22u64, 33u64]);

    assert(false);
}

pub fn example_ascii() {
    let mut array = [65u8, 98, 32];
    let slice: &mut [u8] = &mut array;
    slice.make_ascii_lowercase();
    assert(slice@ =~= seq![97u8, 98u8, 32u8]);
    slice.make_ascii_uppercase();
    assert(slice@ =~= seq![65u8, 66u8, 32u8]);
    let other = [97u8, 98, 32];
    let other_slice: &[u8] = &other;
    let equal = slice.eq_ignore_ascii_case(other_slice);
    assert(equal);
    let padded = [32u8, 9, 65, 10, 32];
    let padded_slice: &[u8] = &padded;
    let start = padded_slice.trim_ascii_start();
    assert(start@ =~= seq![65u8, 10u8, 32u8]);
    let end = padded_slice.trim_ascii_end();
    assert(end@ =~= seq![32u8, 9u8, 65u8]);
    let both = padded_slice.trim_ascii();
    assert(both@ =~= seq![65u8]);

    assert(false);
}

pub fn example_iterator_current_state() {
    let array = [10u64, 20, 30];
    let slice: &[u64] = &array;
    let mut iter = slice.iter();
    let first = iter.next().unwrap();
    assert(*first == 10);
    let hint = iter.size_hint();
    assert(hint == (2usize, Some(2usize)));
    let last = iter.last().unwrap();
    assert(*last == 30);
    let iter = slice.iter();
    let count = iter.count();
    assert(count == 3);

    assert(false);
}

pub fn example_vec_borrows() {
    let mut vec = Vec::<u64>::new();
    vec.push(10);
    {
        let borrowed: &mut Vec<u64> = AsMut::<Vec<u64>>::as_mut(&mut vec);
        borrowed.push(20);
    }
    assert(vec@ =~= seq![10u64, 20u64]);
    {
        let borrowed: &mut [u64] = AsMut::<[u64]>::as_mut(&mut vec);
        borrowed[0] = 99;
    }
    assert(vec@ =~= seq![99u64, 20u64]);
    let borrowed = AsRef::<[u64]>::as_ref(&vec);
    assert(borrowed@ =~= vec@);

    assert(false);
}

pub fn example_vec_conversions() {
    let array = [10u64, 20, 30];
    let borrowed: Cow<'_, [u64]> = Cow::from(&array);
    match borrowed {
        Cow::Borrowed(slice) => {
            assert(slice@ =~= array@);
        },
        Cow::Owned(_) => {
            assert(false);
        },
    }
    let vec = Vec::from(array);
    assert(vec@ =~= seq![10u64, 20u64, 30u64]);
    let owned: Cow<'_, [u64]> = Cow::from(vec);
    match owned {
        Cow::Owned(contents) => {
            assert(contents@ =~= seq![10u64, 20u64, 30u64]);
        },
        Cow::Borrowed(_) => {
            assert(false);
        },
    }

    assert(false);
}

pub fn example_conditional_equality() {
    let left = Vec::from([10u64, 20]);
    let right = [10u64, 20];
    let slice: &[u64] = &right;
    let equal = <Vec<u64> as PartialEq<&[u64]>>::eq(&left, &slice);
    assert(equal);
    let unequal = <Vec<u64> as PartialEq<[u64; 2]>>::ne(&left, &right);
    assert(!unequal);
    let cow: Cow<'_, [u64]> = Cow::from(slice);
    let cow_equal = <Cow<'_, [u64]> as PartialEq<Vec<u64>>>::eq(&cow, &left);
    assert(cow_equal);

    assert(false);
}

pub fn example_escape_ascii() {
    let bytes = [10u8, 65];
    let slice: &[u8] = &bytes;
    let mut escaped = slice.escape_ascii();
    let first = escaped.next().unwrap();
    assert(first == 92);
    let second = escaped.next().unwrap();
    assert(second == 110);
    proof {
        assert(slice_specs::ascii_model::parts::view(escaped) == (
            Seq::<u8>::empty(),
            seq![65u8],
            Seq::<u8>::empty(),
        ));
        seq![65u8].lemma_flat_map_singleton(
            |byte: u8| slice_specs::ascii_model::values::escape_byte(byte),
        );
        assert(slice_specs::ascii_model::values::escaped(seq![65u8]) =~= seq![65u8]);
        assert(slice_specs::ascii_model::state::contents(
            slice_specs::ascii_model::parts::view(escaped),
        ) =~= seq![65u8]);
    }
    let last = escaped.last().unwrap();
    assert(last == 65);

    assert(false);
}

pub fn example_split_constructors() {
    let bytes = [10u64, 20, 30];
    let slice: &[u64] = &bytes;
    let split = slice.split_inclusive(|x: &u64| -> (r: bool) { *x == 20 });
    let hint = split.size_hint();
    assert(hint == (1usize, Some(3usize)));
    let chunk = slice.chunk_by(|x: &u64, y: &u64| -> (r: bool) { *x == *y });
    let chunk_hint = chunk.size_hint();
    assert(chunk_hint == (1usize, Some(3usize)));

    assert(false);
}

} // verus!
