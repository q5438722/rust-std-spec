#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u16_trailing_zeros_unique(i: u16, n: u16)
    requires
        n < 16,
        (i >> n) & 1u16 == 1u16,
        forall|j: u16| j < n ==> (i >> j) & 1u16 == 0u16,
    ensures
        u16_trailing_zeros(i) == n as u32,
{
    axiom_u16_trailing_zeros(i);
    assert(i == 0 ==> (i >> n) & 1u16 == 0u16) by (bit_vector);
    assert(i != 0);
    assert(u16_trailing_zeros(i) < 16);
    let x = u16_trailing_zeros(i) as u16;
    assert(x < 16);
    if x < n {
        assert((i >> x) & 1u16 == 0u16);
        assert((i >> x) & 1u16 == 1u16);
    } else if n < x {
        assert((i >> n) & 1u16 == 0u16);
    }
    assert(x == n);
}

// Fixed-width executable desugaring of core::intrinsics::cttz::<u16>.
fn source_core_intrinsics_cttz_u16(i: u16) -> (r: u32)
    ensures
        r == u16_trailing_zeros(i),
    decreases i,
{
    if i == 0 {
        proof {
            axiom_u16_trailing_zeros(i);
        }
        16
    } else if (i & 1) != 0 {
        proof {
            assert((i & 1u16) != 0 ==> (i >> 0u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| j < 0u16 implies (i >> j) & 1u16 == 0u16 by {
                assert(!(j < 0u16));
            }
            lemma_u16_trailing_zeros_unique(i, 0);
        }
        0
    } else {
        let q = i / 2;
        let r = source_core_intrinsics_cttz_u16(q);
        proof {
            axiom_u16_trailing_zeros(q);
            assert(i != 0 && (i & 1u16) == 0 ==> i / 2 != 0) by (bit_vector);
            assert(q != 0);
            assert(u16_trailing_zeros(q) < 16);
            let y = u16_trailing_zeros(q) as u16;
            assert(y < 16);
            assert((q >> y) & 1u16 == 1u16);
            assert(i / 2 == i >> 1u16) by (bit_vector);
            assert(q == i >> 1u16);
            assert(i / 2 <= 0x7fffu16) by (bit_vector);
            assert(q <= 0x7fffu16);
            assert(
                q <= 0x7fffu16 && y < 16 && (q >> y) & 1u16 == 1u16 ==> y < 15
            ) by (bit_vector);
            let n = (y + 1) as u16;
            assert(n < 16);
            assert(n == y + 1);
            assert(
                q == i >> 1u16 && n == y + 1 && y < 15
                    && (q >> y) & 1u16 == 1u16
                    ==> (i >> n) & 1u16 == 1u16
            ) by (bit_vector);
            assert forall|j: u16| j < n implies (i >> j) & 1u16 == 0u16 by {
                if j == 0 {
                    assert(
                        (i & 1u16) == 0 && j == 0
                            ==> (i >> j) & 1u16 == 0u16
                    ) by (bit_vector);
                } else {
                    assert(j - 1u16 < y);
                    assert((q >> ((j - 1) as u16)) & 1u16 == 0u16);
                    assert(
                        q == i >> 1u16 && 0 < j && j < 16
                            && (q >> ((j - 1) as u16)) & 1u16 == 0u16
                            ==> (i >> j) & 1u16 == 0u16
                    ) by (bit_vector);
                }
            }
            lemma_u16_trailing_zeros_unique(i, n);
            assert(r == y as u32);
            assert(1 + r == n as u32);
        }
        1 + r
    }
}

fn source_u16_trailing_zeros(i: u16) -> (r: u32)
    ensures
        r == u16_trailing_zeros(i),
{
    return source_core_intrinsics_cttz_u16(i);
}

}

fn main() {}