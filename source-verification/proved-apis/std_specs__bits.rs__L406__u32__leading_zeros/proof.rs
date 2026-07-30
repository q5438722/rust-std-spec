#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u32_leading_zeros_unique(i: u32, n: u32)
    requires
        n < 32,
        (i >> sub(31u32, n)) & 1u32 == 1u32,
        forall|j: u32| 32 - n <= j < 32 ==> (i >> j) & 1u32 == 0u32,
    ensures
        u32_leading_zeros(i) == n,
{
    axiom_u32_leading_zeros(i);
    let x = u32_leading_zeros(i);
    assert(i == 0 ==> (i >> sub(31u32, n)) & 1u32 == 0u32) by (bit_vector);
    assert(i != 0);
    assert(x < 32);
    if x < n {
        assert((i >> sub(31u32, x)) & 1u32 != 0u32);
        assert((i >> sub(31u32, x)) & 1u32 == 0u32);
    } else if x > n {
        assert((i >> sub(31u32, n)) & 1u32 == 0u32);
    }
}

// Fixed-width executable desugaring of core::intrinsics::ctlz::<u32>.
fn source_core_intrinsics_ctlz_u32(i: u32) -> (r: u32)
    ensures
        r == u32_leading_zeros(i),
    decreases i,
{
    if i == 0 {
        proof {
            axiom_u32_leading_zeros(i);
        }
        32
    } else {
        let q = i / 2;
        let r = source_core_intrinsics_ctlz_u32(q);
        proof {
            axiom_u32_leading_zeros(q);
            let z = u32_leading_zeros(q);
            assert(i / 2 == i >> 1u32) by (bit_vector);
            assert(q == i / 2);
            assert(q == i >> 1u32);
            assert(i / 2 <= 0x7fff_ffffu32) by (bit_vector);
            assert(q <= 0x7fff_ffffu32);
            if z == 0 {
                assert((q >> 31u32) & 1u32 != 0u32);
                assert(q <= 0x7fff_ffffu32
                    ==> (q >> 31u32) & 1u32 == 0u32) by (bit_vector);
            }
            assert(z > 0);
            let n = (z - 1) as u32;
            assert(n < 32);
            if q == 0 {
                assert(i != 0 && q == 0 && q == i >> 1u32 ==> i == 1) by (bit_vector);
                assert(i == 1);
                assert(z == 32);
                assert(n == 31);
                assert(i == 1 && n == 31
                    ==> (i >> sub(31u32, n)) & 1u32 == 1u32) by (bit_vector);
                assert forall|j: u32| 32 - n <= j < 32 implies
                    (i >> j) & 1u32 == 0u32 by {
                    assert(i == 1 && n == 31 && 32 - n <= j < 32
                        ==> (i >> j) & 1u32 == 0u32) by (bit_vector);
                }
            } else {
                assert(z < 32);
                assert((q >> sub(31u32, z)) & 1u32 != 0u32);
                assert(
                    (q >> sub(31u32, z)) & 1u32 != 0u32
                        ==> (q >> sub(31u32, z)) & 1u32 == 1u32
                ) by (bit_vector);
                assert(
                    q == i >> 1u32 && n == z - 1 && 0 < z < 32
                        && (q >> sub(31u32, z)) & 1u32 == 1u32
                        ==> (i >> sub(31u32, n)) & 1u32 == 1u32
                ) by (bit_vector);
                assert forall|j: u32| 32 - n <= j < 32 implies
                    (i >> j) & 1u32 == 0u32 by {
                    let k = (j - 1) as u32;
                    assert(32 - z <= k < 32);
                    assert((q >> k) & 1u32 == 0u32);
                    assert(
                        q == i >> 1u32 && k == j - 1
                            && (q >> k) & 1u32 == 0u32
                            ==> (i >> j) & 1u32 == 0u32
                    ) by (bit_vector);
                }
            }
            lemma_u32_leading_zeros_unique(i, n);
            assert(r == z);
            assert(r - 1 == n);
        }
        r - 1
    }
}

fn source_u32_leading_zeros(i: u32) -> (r: u32)
    ensures
        r == u32_leading_zeros(i),
{
    return source_core_intrinsics_ctlz_u32(i);
}

} // verus!

fn main() {}