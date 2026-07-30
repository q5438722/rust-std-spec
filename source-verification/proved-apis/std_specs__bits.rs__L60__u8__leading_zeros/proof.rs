#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(internal_features)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

pub open spec fn compiler_ctlz_u8(i: u8) -> u32 {
    if i == 0 {
        8
    } else if i < 2 {
        7
    } else if i < 4 {
        6
    } else if i < 8 {
        5
    } else if i < 16 {
        4
    } else if i < 32 {
        3
    } else if i < 64 {
        2
    } else if i < 128 {
        1
    } else {
        0
    }
}

pub uninterp spec fn compiler_ctlz<T>(i: T) -> u32;

pub assume_specification<T: Copy>[ core::intrinsics::ctlz::<T> ](i: T) -> (r: u32)
    ensures
        r == compiler_ctlz(i),
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_compiler_ctlz_u8(i: u8)
    ensures
        compiler_ctlz(i) == compiler_ctlz_u8(i),
;

proof fn lemma_u8_leading_zeros_unique(i: u8, zeros: u32)
    requires
        zeros <= 8,
        i == 0 <==> zeros == 8,
        zeros < 8 ==> (i >> sub(7u8, zeros as u8)) & 1u8 != 0u8,
        i >> sub(8u8, zeros as u8) == 0,
    ensures
        compiler_ctlz_u8(i) == zeros,
{
    if zeros == 0 {
        assert(sub(7u8, zeros as u8) == 7);
        assert((i >> 7) & 1u8 != 0u8);
        assert(((i >> 7) & 1u8 != 0u8) ==> i >= 128) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 1 {
        assert(sub(7u8, zeros as u8) == 6);
        assert(sub(8u8, zeros as u8) == 7);
        assert((i >> 6) & 1u8 != 0u8);
        assert(i >> 7 == 0);
        assert(
            ((i >> 6) & 1u8 != 0u8 && i >> 7 == 0) ==> 64 <= i && i < 128
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 2 {
        assert(sub(7u8, zeros as u8) == 5);
        assert(sub(8u8, zeros as u8) == 6);
        assert((i >> 5) & 1u8 != 0u8);
        assert(i >> 6 == 0);
        assert(
            ((i >> 5) & 1u8 != 0u8 && i >> 6 == 0) ==> 32 <= i && i < 64
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 3 {
        assert(sub(7u8, zeros as u8) == 4);
        assert(sub(8u8, zeros as u8) == 5);
        assert((i >> 4) & 1u8 != 0u8);
        assert(i >> 5 == 0);
        assert(
            ((i >> 4) & 1u8 != 0u8 && i >> 5 == 0) ==> 16 <= i && i < 32
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 4 {
        assert(sub(7u8, zeros as u8) == 3);
        assert(sub(8u8, zeros as u8) == 4);
        assert((i >> 3) & 1u8 != 0u8);
        assert(i >> 4 == 0);
        assert(
            ((i >> 3) & 1u8 != 0u8 && i >> 4 == 0) ==> 8 <= i && i < 16
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 5 {
        assert(sub(7u8, zeros as u8) == 2);
        assert(sub(8u8, zeros as u8) == 3);
        assert((i >> 2) & 1u8 != 0u8);
        assert(i >> 3 == 0);
        assert(
            ((i >> 2) & 1u8 != 0u8 && i >> 3 == 0) ==> 4 <= i && i < 8
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 6 {
        assert(sub(7u8, zeros as u8) == 1);
        assert(sub(8u8, zeros as u8) == 2);
        assert((i >> 1) & 1u8 != 0u8);
        assert(i >> 2 == 0);
        assert(
            ((i >> 1) & 1u8 != 0u8 && i >> 2 == 0) ==> 2 <= i && i < 4
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else if zeros == 7 {
        assert(sub(7u8, zeros as u8) == 0);
        assert(sub(8u8, zeros as u8) == 1);
        assert((i >> 0) & 1u8 != 0u8);
        assert(i >> 1 == 0);
        assert(
            ((i >> 0) & 1u8 != 0u8 && i >> 1 == 0) ==> i == 1
        ) by (bit_vector);
        assert(compiler_ctlz_u8(i) == zeros);
    } else {
        assert(zeros == 8);
        assert(i == 0);
        assert(compiler_ctlz_u8(i) == zeros);
    }
}

proof fn lemma_compiler_ctlz_u8_matches_vstd(i: u8)
    ensures
        compiler_ctlz_u8(i) == u8_leading_zeros(i),
{
    axiom_u8_leading_zeros(i);
    lemma_u8_leading_zeros_unique(i, u8_leading_zeros(i));
}

fn source_u8_leading_zeros(i: u8) -> (r: u32)
    ensures
        r == u8_leading_zeros(i),
{
    let r = core::intrinsics::ctlz(i as u8);
    proof {
        axiom_compiler_ctlz_u8(i);
        lemma_compiler_ctlz_u8_matches_vstd(i);
    }
    return r;
}

} // verus!

fn main() {}