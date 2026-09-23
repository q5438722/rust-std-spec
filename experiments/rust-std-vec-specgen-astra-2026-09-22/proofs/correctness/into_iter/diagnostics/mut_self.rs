#![feature(allocator_api)]

use std::alloc::Allocator;
use std::iter::DoubleEndedIterator;
use std::vec::IntoIter;
use vstd::prelude::*;

verus! {

pub trait Iterator {
    type Item;
    fn last(self) -> Option<Self::Item> where Self: Sized;
}

impl<T, A: Allocator> Iterator for IntoIter<T, A> {
    type Item = T;

    fn last(mut self) -> Option<T> {
        self.next_back()
    }
}

}
