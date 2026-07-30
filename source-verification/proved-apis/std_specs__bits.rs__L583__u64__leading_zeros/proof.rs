#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

// Fixed-width executable desugaring of core::intrinsics::ctlz::<u64>.
fn source_core_intrinsics_ctlz_u64(i: u64) -> (r: u32)
    ensures
        r as int == u64_leading_zeros(i),
    decreases i,
{
    if i == 0 {
        proof {
            reveal(u64_leading_zeros);
        }
        64
    } else {
        let q = i / 2;
        let r = source_core_intrinsics_ctlz_u64(q);
        proof {
            axiom_u64_leading_zeros(q);
            assert(i / 2 == i >> 1u64) by (bit_vector);
            assert(q == i >> 1u64);
            assert((((i >> 1u64) >> 63u64) & 1u64) == 0u64) by (bit_vector);
            assert((q >> 63u64) & 1u64 == 0u64);
            if u64_leading_zeros(q) == 0 {
                assert((q >> 63u64) & 1u64 != 0u64);
            }
            assert(u64_leading_zeros(q) > 0);
            assert(r > 0);
            reveal(u64_leading_zeros);
        }
        r - 1
    }
}

fn source_u64_leading_zeros(i: u64) -> (r: u32)
    ensures
        r as int == u64_leading_zeros(i),
{
    return source_core_intrinsics_ctlz_u64(i as u64);
}

} // verus!

fn main() {}