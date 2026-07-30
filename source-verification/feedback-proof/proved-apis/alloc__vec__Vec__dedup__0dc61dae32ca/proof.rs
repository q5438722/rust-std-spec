#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::seq::Seq;
use vstd::std_specs::cmp::PartialEqSpec;

verus! {

pub assume_specification<T, A: Allocator, F>[
    Vec::<T, A>::dedup_by
](
    vec: &mut Vec<T, A>,
    same_bucket: F,
)
where
    F: FnMut(&mut T, &mut T) -> bool,
    requires
        forall|a: &mut T, b: &mut T| #[trigger] same_bucket.requires((a, b)),
    ensures
        forall|step: spec_fn(Seq<T>, T) -> Seq<T>| {
            &&& (forall|element: T|
                #[trigger] step(Seq::<T>::empty(), element)
                    == Seq::<T>::empty().push(element))
            &&& (forall|
                kept: Seq<T>,
                element: T,
                a: &mut T,
                b: &mut T,
                result: bool,
            |
                #![trigger
                    same_bucket.ensures((a, b), result),
                    step(kept, element)
                ]
                kept.len() > 0
                && *a == element
                && *b == kept.last()
                && same_bucket.ensures((a, b), result)
                ==> {
                    &&& *final(a) == *a
                    &&& *final(b) == *b
                    &&& step(kept, element) == if result {
                        kept
                    } else {
                        kept.push(element)
                    }
                })
            ==> final(vec)@ == #[trigger] old(vec)@.fold_left(
                Seq::<T>::empty(),
                step,
            )
        },
;

pub fn source_vec_dedup<T: core::cmp::PartialEq, A: Allocator>(
    vec: &mut Vec<T, A>,
)
    requires
        T::obeys_eq_spec(),
    ensures
        final(vec)@ == old(vec)@.fold_left(
            Seq::<T>::empty(),
            |kept: Seq<T>, element: T| {
                if kept.len() == 0 {
                    kept.push(element)
                } else if element.eq_spec(&kept.last()) {
                    kept
                } else {
                    kept.push(element)
                }
            },
        ),
{
    let ghost input = vec@;
    let same_bucket =
        |a: &mut T, b: &mut T| -> (result: bool)
            requires
                T::obeys_eq_spec(),
            ensures
                *final(a) == *old(a),
                *final(b) == *old(b),
                result == (*old(a)).eq_spec(&*old(b)),
        {
            // Inline the &mut PartialEq forwarding impl used by `a == b`.
            <T as core::cmp::PartialEq>::eq(&*a, &*b)
        };
    vec.dedup_by(same_bucket);
    proof {
        assert(vec@ == input.fold_left(
            Seq::<T>::empty(),
            |kept: Seq<T>, element: T| {
                if kept.len() == 0 {
                    kept.push(element)
                } else if element.eq_spec(&kept.last()) {
                    kept
                } else {
                    kept.push(element)
                }
            },
        ));
    }
}

} // verus!

fn main() {}