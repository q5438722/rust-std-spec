use std::alloc::Allocator;
use std::iter::DoubleEndedIterator;
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

pub trait Iterator {
    type Item;
    fn last(self) -> Option<Self::Item> where Self: Sized;
}

impl<T, A: Allocator> Iterator for IntoIter<T, A> {
    type Item = T;

    fn last(mut self) -> Option<T> {
        #[cfg(verus_keep_ghost)]
        ensures(|result: Option<T>| verus_proof_expr! {
            result == if IteratorSpec::remaining(&self).len() == 0 {
                None
            } else {
                Some(IteratorSpec::remaining(&self).last())
            }
        });
        self.next_back()
    }
}

}
