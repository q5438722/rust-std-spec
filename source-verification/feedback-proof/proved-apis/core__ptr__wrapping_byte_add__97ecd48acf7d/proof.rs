#![feature(set_ptr_value, sized_hierarchy)]
#![allow(dead_code)]

use vstd::layout::size_of;
use vstd::prelude::*;

verus! {

pub assume_specification<T: core::marker::PointeeSized, U>[
    <*const T>::cast::<U>
](ptr: *const T) -> (result: *const U)
    ensures
        result == ptr as *const U,
    opens_invariants none
    no_unwind
;

pub assume_specification<T: core::marker::PointeeSized>[
    <*const T>::wrapping_add
](ptr: *const T, count: usize) -> (result: *const T)
    where
        T: Sized,
    ensures
        result@.addr as int
            == (ptr@.addr as int + (count as int) * (size_of::<T>() as int))
                % ((usize::MAX as int) + 1),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
    opens_invariants none
    no_unwind
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
    opens_invariants none
    no_unwind
;

proof fn lemma_usize_wrapping_add_mod(x: usize, y: usize)
    ensures
        x.wrapping_add(y) as int
            == (x as int + y as int) % ((usize::MAX as int) + 1),
{
    let sum = x as int + y as int;
    let modulus = (usize::MAX as int) + 1;
    if sum > usize::MAX as int {
        let remainder = sum - modulus;
        assert(0 <= remainder < modulus);
        assert(sum == modulus + remainder);
        vstd::arithmetic::div_mod::lemma_fundamental_div_mod_converse_mod(
            sum,
            modulus,
            1,
            remainder,
        );
    } else {
        assert(0 <= sum < modulus);
        assert(sum == 0 * modulus + sum);
        vstd::arithmetic::div_mod::lemma_fundamental_div_mod_converse_mod(
            sum,
            modulus,
            0,
            sum,
        );
    }
}

pub fn source_core_ptr_wrapping_byte_add<T: core::marker::PointeeSized>(
    ptr: *const T,
    count: usize,
) -> (result: *const T)
    ensures
        result == ptr.with_addr(ptr.addr().wrapping_add(count)),
    opens_invariants none
    no_unwind
{
    let thin = ptr.cast::<u8>();
    let advanced = thin.wrapping_add(count);
    proof {
        lemma_usize_wrapping_add_mod(ptr@.addr, count);
        assert(size_of::<u8>() == 1);
        assert(advanced@.addr == ptr@.addr.wrapping_add(count));
    }
    advanced.with_metadata_of(ptr)
}

}

fn main() {}