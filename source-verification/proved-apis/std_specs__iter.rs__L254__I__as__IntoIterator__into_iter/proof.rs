#![allow(dead_code)]
#![allow(unused_imports)]

use core::iter::{IntoIterator, Iterator};
use vstd::prelude::*;
use vstd::std_specs::iter::*;

verus! {

fn source_iterator_into_iter<I: Iterator>(i: I) -> (r: I)
    ensures
        r == i,
{
    i
}

}

fn main() {}