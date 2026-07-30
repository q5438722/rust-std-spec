#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_get<'a, T, A: Allocator>(
    v: &'a VecDeque<T, A>,
    index: usize,
) -> (result: Option<&'a T>)
    ensures
        index < v@.len() ==> (result matches Some(value) && *value == v@[index as int]),
        index >= v@.len() ==> result is None,
{
    let len = v.len();
    proof {
        axiom_spec_len(v);
    }

    if index < len {
        let (front, back) = v.as_slices();
        let front_len = front.len();
        let back_len = back.len();

        proof {
            vstd::slice::axiom_spec_len(front);
            vstd::slice::axiom_spec_len(back);
            assert((front@ + back@).len() == front@.len() + back@.len());
        }

        if index < front_len {
            proof {
                assert((front@ + back@)[index as int] == front@[index as int]);
            }
            Some(&front[index])
        } else {
            let physical_index = index - front_len;
            proof {
                assert(index < front_len + back_len);
                assert(physical_index < back_len);
                assert(
                    (front@ + back@)[index as int]
                        == back@[(index - front_len) as int]
                );
            }
            Some(&back[physical_index])
        }
    } else {
        None
    }
}

} // verus!

fn main() {}