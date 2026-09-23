use std::alloc::Allocator;
use std::iter::ExactSizeIterator;
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

// A local trait avoids an orphan impl while retaining the original method bodies.
pub trait Iterator {
    type Item;
    fn count(self) -> usize where Self: Sized;
}

impl<T, A: Allocator> Iterator for IntoIter<T, A> {
    type Item = T;

    fn count(self) -> usize {
        #[cfg(verus_keep_ghost)]
        ensures(|result: usize| verus_proof_expr! {
            result == IteratorSpec::remaining(&self).len()
        });
        self.len()
    }
}

}
