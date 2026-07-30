#![feature(set_ptr_value)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::layout::size_of;

verus! {

pub assume_specification<T: core::marker::PointeeSized, U>[
    <*const T>::cast::<U>
](ptr: *const T) -> (result: *const U)
    ensures
        result == ptr as *const U,
;

pub assume_specification<T: core::marker::PointeeSized>[
    <*const T>::wrapping_sub
](ptr: *const T, count: usize) -> (result: *const T)
    where
        T: Sized,
    ensures
        result@.addr as int ==
            (ptr@.addr as int - (count as int) * (size_of::<T>() as int))
                % ((usize::MAX as int) + 1),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
;

pub assume_specification<
    T: core::marker::PointeeSized,
    U: core::marker::PointeeSized,
>[
    <*const T>::with_metadata_of::<U>
](ptr: *const T, meta: *const U) -> (result: *const U)
    ensures
        result@.addr == ptr@.addr,
        result@.provenance == ptr@.provenance,
        result@.metadata == meta@.metadata,
;

proof fn lemma_usize_wrapping_sub_as_mod(x: usize, y: usize)
    ensures
        x.wrapping_sub(y) as int ==
            (x as int - y as int) % ((usize::MAX as int) + 1),
{
    let m = (usize::MAX as int) + 1;
    let d = x as int - y as int;
    assert(m > 0);
    if x >= y {
        assert(0 <= d < m);
        vstd::arithmetic::div_mod::lemma_small_mod(d as nat, m as nat);
        assert(d % m == d);
    } else {
        assert(0 <= m + d < m);
        vstd::arithmetic::div_mod::lemma_small_mod((m + d) as nat, m as nat);
        vstd::arithmetic::div_mod::lemma_mod_add_multiples_vanish(d, m);
        assert(d % m == m + d);
    }
}

pub fn source_core_ptr_wrapping_byte_sub<T: core::marker::PointeeSized>(
    ptr: *const T,
    count: usize,
) -> (result: *const T)
    ensures
        result@.addr == ptr@.addr.wrapping_sub(count),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
{
    broadcast use vstd::layout::layout_of_primitives;

    proof {
        lemma_usize_wrapping_sub_as_mod(ptr@.addr, count);
    }
    ptr.cast::<u8>().wrapping_sub(count).with_metadata_of(ptr)
}

} // verus!

fn main() {}