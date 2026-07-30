#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::Range;
use vstd::prelude::*;
use vstd::seq::{lemma_seq_subrange_composition, lemma_seq_subrange_len};
use vstd::std_specs::slice::*;

verus! {

fn source_range_slice_index<T>(i: Range<usize>, slice: &[T]) -> (r: &[T])
    requires
        i.start <= i.end,
        i.end <= slice@.len(),
    ensures
        r@ == slice@.subrange(i.start as int, i.end as int),
{
    match usize::checked_sub(i.end, i.start) {
        Some(new_len) => {
            if i.end <= slice.len() {
                // Desugar the private offset-and-length raw-slice helper into equivalent splits.
                let (_, tail) = slice.split_at(i.start);
                proof {
                    lemma_seq_subrange_len(
                        slice@,
                        i.start as int,
                        slice@.len() as int,
                    );
                }
                let (result, _) = tail.split_at(new_len);
                proof {
                    lemma_seq_subrange_composition(
                        slice@,
                        i.start as int,
                        slice@.len() as int,
                        0,
                        new_len as int,
                    );
                }
                result
            } else {
                assert(false);
                vstd::pervasive::__call_panic(&[])
            }
        }
        None => {
            assert(false);
            vstd::pervasive::__call_panic(&[])
        }
    }
}

}

fn main() {}