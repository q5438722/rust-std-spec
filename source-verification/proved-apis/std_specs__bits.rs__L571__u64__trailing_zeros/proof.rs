#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u64_trailing_zeros_unique(i: u64, n: u64)
    requires
        n < 64,
        (i >> n) & 1u64 == 1u64,
        forall|j: u64| j < n ==> (i >> j) & 1u64 == 0u64,
    ensures
        u64_trailing_zeros(i) == n as u32,
{
    axiom_u64_trailing_zeros(i);
    assert(i == 0 ==> (i >> n) & 1u64 == 0u64) by (bit_vector);
    assert(i != 0);
    assert(u64_trailing_zeros(i) < 64);
    let x = u64_trailing_zeros(i) as u64;
    assert(x < 64);
    if x < n {
        assert((i >> x) & 1u64 == 0u64);
        assert((i >> x) & 1u64 == 1u64);
    } else if n < x {
        assert((i >> n) & 1u64 == 0u64);
    }
    assert(x == n);
}

// Fixed-width executable desugaring of core::intrinsics::cttz::<u64>.
fn source_core_intrinsics_cttz_u64(i: u64) -> (r: u32)
    ensures
        r == u64_trailing_zeros(i),
    decreases i,
{
    if i == 0 {
        proof {
            axiom_u64_trailing_zeros(i);
        }
        64
    } else if (i & 1) != 0 {
        proof {
            assert((i & 1u64) != 0 ==> (i >> 0u64) & 1u64 == 1u64) by (bit_vector);
            assert forall|j: u64| j < 0u64 implies (i >> j) & 1u64 == 0u64 by {
                assert(!(j < 0u64));
            }
            lemma_u64_trailing_zeros_unique(i, 0);
        }
        0
    } else {
        let q = i / 2;
        let r = source_core_intrinsics_cttz_u64(q);
        proof {
            axiom_u64_trailing_zeros(q);
            assert(i != 0 && (i & 1u64) == 0 ==> i / 2 != 0) by (bit_vector);
            assert(q != 0);
            assert(u64_trailing_zeros(q) < 64);
            let y = u64_trailing_zeros(q) as u64;
            assert(y < 64);
            assert((q >> y) & 1u64 == 1u64);
            assert(i / 2 == i >> 1u64) by (bit_vector);
            assert(q == i >> 1u64);
            assert(i / 2 <= 0x7fff_ffff_ffff_ffffu64) by (bit_vector);
            assert(q <= 0x7fff_ffff_ffff_ffffu64);
            assert(
                q <= 0x7fff_ffff_ffff_ffffu64 && y < 64 && (q >> y) & 1u64 == 1u64
                    ==> y < 63
            ) by (bit_vector);
            let n = (y + 1) as u64;
            assert(n < 64);
            assert(n == y + 1);
            assert(
                q == i >> 1u64 && n == y + 1 && y < 63
                    && (q >> y) & 1u64 == 1u64
                    ==> (i >> n) & 1u64 == 1u64
            ) by (bit_vector);
            assert forall|j: u64| j < n implies (i >> j) & 1u64 == 0u64 by {
                if j == 0 {
                    assert(
                        (i & 1u64) == 0 && j == 0
                            ==> (i >> j) & 1u64 == 0u64
                    ) by (bit_vector);
                } else {
                    assert(j - 1u64 < y);
                    assert((q >> ((j - 1) as u64)) & 1u64 == 0u64);
                    assert(
                        q == i >> 1u64 && 0 < j && j < 64
                            && (q >> ((j - 1) as u64)) & 1u64 == 0u64
                            ==> (i >> j) & 1u64 == 0u64
                    ) by (bit_vector);
                }
            }
            lemma_u64_trailing_zeros_unique(i, n);
            assert(r == y as u32);
            assert(1 + r == n as u32);
        }
        1 + r
    }
}

fn source_u64_trailing_zeros(i: u64) -> (r: u32)
    ensures
        r == u64_trailing_zeros(i),
{
    return source_core_intrinsics_cttz_u64(i);
}

}

fn main() {}