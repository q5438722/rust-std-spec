#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u32_trailing_zeros_unique(i: u32, n: u32)
    requires
        n < 32,
        (i >> n) & 1u32 == 1u32,
        forall|j: u32| j < n ==> (i >> j) & 1u32 == 0u32,
    ensures
        u32_trailing_zeros(i) == n,
{
    axiom_u32_trailing_zeros(i);
    assert(i == 0 ==> (i >> n) & 1u32 == 0u32) by (bit_vector);
    assert(i != 0);
    assert(u32_trailing_zeros(i) < 32);
    let x = u32_trailing_zeros(i);
    assert(x < 32);
    if x < n {
        assert((i >> x) & 1u32 == 0u32);
        assert((i >> x) & 1u32 == 1u32);
    } else if n < x {
        assert((i >> n) & 1u32 == 0u32);
    }
    assert(x == n);
}

// Fixed-width executable desugaring of core::intrinsics::cttz::<u32>.
fn source_core_intrinsics_cttz_u32(i: u32) -> (r: u32)
    ensures
        r == u32_trailing_zeros(i),
    decreases i,
{
    if i == 0 {
        proof {
            axiom_u32_trailing_zeros(i);
        }
        32
    } else if (i & 1) != 0 {
        proof {
            assert((i & 1u32) != 0 ==> (i >> 0u32) & 1u32 == 1u32) by (bit_vector);
            assert forall|j: u32| j < 0u32 implies (i >> j) & 1u32 == 0u32 by {
                assert(!(j < 0u32));
            }
            lemma_u32_trailing_zeros_unique(i, 0);
        }
        0
    } else {
        let q = i / 2;
        let r = source_core_intrinsics_cttz_u32(q);
        proof {
            axiom_u32_trailing_zeros(q);
            assert(i != 0 && (i & 1u32) == 0 ==> i / 2 != 0) by (bit_vector);
            assert(q != 0);
            assert(u32_trailing_zeros(q) < 32);
            let y = u32_trailing_zeros(q);
            assert(y < 32);
            assert((q >> y) & 1u32 == 1u32);
            assert(i / 2 == i >> 1u32) by (bit_vector);
            assert(q == i >> 1u32);
            assert(i / 2 <= 0x7fffffffu32) by (bit_vector);
            assert(q <= 0x7fffffffu32);
            assert(
                q <= 0x7fffffffu32 && y < 32 && (q >> y) & 1u32 == 1u32 ==> y < 31
            ) by (bit_vector);
            let n = (y + 1) as u32;
            assert(n < 32);
            assert(n == y + 1);
            assert(
                q == i >> 1u32 && n == y + 1 && y < 31
                    && (q >> y) & 1u32 == 1u32
                    ==> (i >> n) & 1u32 == 1u32
            ) by (bit_vector);
            assert forall|j: u32| j < n implies (i >> j) & 1u32 == 0u32 by {
                if j == 0 {
                    assert(
                        (i & 1u32) == 0 && j == 0
                            ==> (i >> j) & 1u32 == 0u32
                    ) by (bit_vector);
                } else {
                    assert(j - 1u32 < y);
                    assert((q >> ((j - 1) as u32)) & 1u32 == 0u32);
                    assert(
                        q == i >> 1u32 && 0 < j && j < 32
                            && (q >> ((j - 1) as u32)) & 1u32 == 0u32
                            ==> (i >> j) & 1u32 == 0u32
                    ) by (bit_vector);
                }
            }
            lemma_u32_trailing_zeros_unique(i, n);
            assert(r == y);
            assert(1 + r == n);
        }
        1 + r
    }
}

fn source_u32_trailing_zeros(i: u32) -> (r: u32)
    ensures
        r == u32_trailing_zeros(i),
{
    return source_core_intrinsics_cttz_u32(i);
}

}

fn main() {}