#![feature(sized_hierarchy)]
#![allow(dead_code)]

use vstd::layout::size_of;
use vstd::prelude::*;

verus! {

pub assume_specification[<isize>::wrapping_neg](
    value: isize,
) -> (result: isize)
    ensures
        result as int
            == if value == isize::MIN {
                value as int
            } else {
                -(value as int)
            },
;

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
;

pub fn source_core_ptr_wrapping_sub<T: core::marker::PointeeSized>(
    ptr: *const T,
    count: usize,
) -> (result: *const T)
    where
        T: Sized,
    ensures
        result@.addr as int
            == (ptr@.addr as int - (count as int) * (size_of::<T>() as int))
                % ((usize::MAX as int) + 1),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
{
    let offset = #[verifier::truncate] (count as isize);
    let negated = offset.wrapping_neg();
    let result = ptr.wrapping_offset(negated);
    proof {
        let m: int = (usize::MAX as int) + 1;
        let a: int = ptr@.addr as int;
        let c: int = count as int;
        let s: int = size_of::<T>() as int;

        assert(m > 0);
        if count <= isize::MAX as usize {
            assert(offset as int == c);
            assert(offset != isize::MIN);
            assert(negated as int == -c);
            assert(a + (negated as int) * s == a - c * s) by (nonlinear_arith)
                requires
                    negated as int == -c,
            ;
        } else if count == isize::MAX as usize + 1 {
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
                assert(isize::MIN as int == -2_147_483_648int);
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
                assert(isize::MIN as int == -9_223_372_036_854_775_808int);
            }
            assert(offset == isize::MIN);
            assert(negated as int == offset as int);
            assert(offset as int == -c);
            assert(a + (negated as int) * s == a - c * s) by (nonlinear_arith)
                requires
                    negated as int == -c,
            ;
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
            assert(offset != isize::MIN);
            assert(signed_magnitude as int == magnitude as int);
            assert(magnitude as int == m - c);
            assert(negated as int == m - c);
            vstd::arithmetic::div_mod::lemma_mod_multiples_vanish(
                s,
                a - c * s,
                m,
            );
            assert(m * s + (a - c * s) == a + (m - c) * s) by (nonlinear_arith);
            assert((a + (negated as int) * s) % m == (a - c * s) % m);
        }
        assert((a + (negated as int) * s) % m == (a - c * s) % m);
    }
    result
}

} // verus!

fn main() {}