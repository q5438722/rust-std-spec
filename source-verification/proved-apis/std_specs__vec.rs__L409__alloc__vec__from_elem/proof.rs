#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_alloc_vec_from_elem<T: Clone>(elem: T, n: usize) -> (v: Vec<T>)
    ensures
        v.len() == n,
        forall |i| 0 <= i < n ==> cloned(elem, #[trigger] v@[i]),
{
    let mut v = Vec::with_capacity(n);
    // `extend_with` reserves, writes clones for `1..n`, then moves the original
    // into the last slot. `push` desugars its private pointer/length updates.
    v.reserve(n);

    if n > 0 {
        let mut i: usize = 0;
        while i < n - 1
            invariant
                i <= n - 1,
                v@.len() == i,
                forall |j: int| #![all_triggers]
                    0 <= j < i ==> cloned::<T>(elem, v@[j]),
            decreases n - 1 - i,
        {
            let value = elem.clone();
            assert(cloned::<T>(elem, value));
            v.push(value);
            i += 1;
        }

        assert(cloned::<T>(elem, elem));
        v.push(elem);
    }

    v
}

} // verus!

fn main() {}