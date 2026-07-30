#![feature(sized_hierarchy)]
#![allow(dead_code)]

use vstd::layout::size_of;
use vstd::prelude::*;

verus! {

pub assume_specification<T: core::marker::PointeeSized>[<*const T>::wrapping_offset](
    ptr: *const T,
    count: isize,
) -> (result: *const T)
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

pub fn source_core_ptr_wrapping_add<T: core::marker::PointeeSized>(
    ptr: *const T,
    count: usize,
) -> (result: *const T)
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
{
    let offset = #[verifier::truncate] (count as isize);
    let result = ptr.wrapping_offset(offset);
    proof {
        let m: int = (usize::MAX as int) + 1;
        let a: int = ptr@.addr as int;
        let c: int = count as int;
        let s: int = size_of::<T>() as int;

        assert(m > 0);
        if count <= isize::MAX as usize {
            assert(offset as int == c);
        } else {
            if count == isize::MAX as usize + 1 {
                if usize::BITS == 32 {
                    assert(isize::MAX as usize == 0x7fff_ffffusize);
                    assert(count == 0x8000_0000usize);
                    assert(offset == (-2_147_483_648i32) as isize) by (bit_vector)
                        requires
                            usize::BITS == 32,
                            count == 0x8000_0000usize,
                            offset == #[verifier::truncate] (count as isize),
                    ;
                    assert(offset as int == -2_147_483_648int);
                    assert(usize::MAX as int == 0xffff_ffffint);
                } else {
                    assert(usize::BITS == 64);
                    assert(isize::MAX as usize == 0x7fff_ffff_ffff_ffffu64 as usize);
                    assert(count == 0x8000_0000_0000_0000u64 as usize);
                    assert(
                        offset == (-9_223_372_036_854_775_808i64) as isize
                    ) by (bit_vector)
                        requires
                            usize::BITS == 64,
                            count == 0x8000_0000_0000_0000u64 as usize,
                            offset == #[verifier::truncate] (count as isize),
                    ;
                    assert(offset as int == -9_223_372_036_854_775_808int);
                    assert(usize::MAX as int == 0xffff_ffff_ffff_ffffu64 as int);
                }
                assert(offset as int == c - m);
            } else {
                let magnitude: usize = (usize::MAX - count + 1) as usize;
                assert(magnitude <= isize::MAX as usize);
                let signed_magnitude = magnitude as isize;
                if usize::BITS == 32 {
                    assert(isize::MAX as usize == 0x7fff_ffffusize);
                    assert(usize::MAX == 0xffff_ffffusize);
                    assert(count > 0x8000_0000usize);
                    assert(offset == -signed_magnitude) by (bit_vector)
                        requires
                            usize::BITS == 32,
                            count > 0x8000_0000usize,
                            offset == #[verifier::truncate] (count as isize),
                            magnitude == (0xffff_ffffusize - count + 1) as usize,
                            signed_magnitude == magnitude as isize,
                    ;
                } else {
                    assert(usize::BITS == 64);
                    assert(isize::MAX as usize == 0x7fff_ffff_ffff_ffffu64 as usize);
                    assert(usize::MAX == 0xffff_ffff_ffff_ffffu64 as usize);
                    assert(count > 0x8000_0000_0000_0000u64 as usize);
                    assert(offset == -signed_magnitude) by (bit_vector)
                        requires
                            usize::BITS == 64,
                            count > 0x8000_0000_0000_0000u64 as usize,
                            offset == #[verifier::truncate] (count as isize),
                            magnitude
                                == (0xffff_ffff_ffff_ffffu64 as usize - count + 1)
                                    as usize,
                            signed_magnitude == magnitude as isize,
                    ;
                }
                assert(signed_magnitude as int == magnitude as int);
                assert(magnitude as int == m - c);
                assert(offset as int == c - m);
            }
            vstd::arithmetic::div_mod::lemma_mod_multiples_vanish(
                -s,
                a + c * s,
                m,
            );
            assert(m * (-s) + (a + c * s) == a + (c - m) * s) by (nonlinear_arith);
            assert((a + (offset as int) * s) % m == (a + c * s) % m);
        }
    }
    result
}

} // verus!

fn main() {}