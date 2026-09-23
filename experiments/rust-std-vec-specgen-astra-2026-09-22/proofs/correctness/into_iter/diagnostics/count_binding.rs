#![feature(allocator_api)]

use std::alloc::Allocator;
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

#[verifier::external_trait_specification]
pub trait ExIteratorCount {
    type ExternalTraitSpecificationFor: core::iter::Iterator;
    type Item;
    fn count(self) -> usize where Self: Sized;
}

pub assume_specification<T, A: Allocator>[
    <IntoIter<T, A> as core::iter::Iterator>::count
](iter: IntoIter<T, A>) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
;

}
