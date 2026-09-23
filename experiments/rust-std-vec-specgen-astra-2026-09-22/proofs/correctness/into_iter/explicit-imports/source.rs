#![no_implicit_prelude]

extern crate core;
extern crate std;
extern crate vstd;

use core::marker::Sized;
use std::alloc::Allocator;
use std::iter::{DoubleEndedIterator, ExactSizeIterator};
use std::option::Option::{self, None, Some};
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

// A local trait avoids an orphan impl while retaining the original method bodies.
pub trait Iterator {
    type Item;
    fn count(self) -> usize where Self: Sized;
    fn last(self) -> Option<Self::Item> where Self: Sized;
}

impl<T, A: Allocator> Iterator for IntoIter<T, A> {
    type Item = T;

    fn count(self) -> (result: usize)
        ensures
            result == IteratorSpec::remaining(&self).len(),
    {
        self.len()
    }

    fn last(mut self) -> (result: Option<T>)
        ensures
            result == if IteratorSpec::remaining(&self).len() == 0 {
                None
            } else {
                Some(IteratorSpec::remaining(&self).last())
            },
    {
        self.next_back()
    }
}

}
