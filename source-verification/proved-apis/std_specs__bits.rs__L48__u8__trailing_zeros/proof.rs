#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u8_trailing_zeros_unique(i: u8, n: u8)
    requires
        n < 8,
        (i >> n) & 1u8 == 1u8,
        forall|j: u8| j < n ==> (i >> j) & 1u8 == 0u8,
    ensures
        u8_trailing_zeros(i) == n as u32,
{
    axiom_u8_trailing_zeros(i);
    let x = u8_trailing_zeros(i);
    assert(i == 0 ==> (i >> n) & 1u8 == 0u8) by (bit_vector);
    assert(i != 0);
    assert(x < 8);
    if x < n {
        assert((i >> x as u8) & 1u8 == 1u8);
        assert((i >> x as u8) & 1u8 == 0u8);
    } else if x > n {
        assert((i >> n) & 1u8 == 0u8);
    }
}

// Fixed-width executable desugaring of core::intrinsics::cttz::<u8>.
fn source_core_intrinsics_cttz_u8(i: u8) -> (r: u32)
    ensures
        r == u8_trailing_zeros(i),
{
    if i == 0 {
        proof {
            axiom_u8_trailing_zeros(i);
        }
        8
    } else if (i & 0x01u8) != 0 {
        proof {
            assert((i & 0x01u8) != 0 ==> (i >> 0u8) & 1u8 == 1u8) by (bit_vector);
            lemma_u8_trailing_zeros_unique(i, 0);
        }
        0
    } else if (i & 0x02u8) != 0 {
        proof {
            assert((i & 0x02u8) != 0 ==> (i >> 1u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 1u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && j < 1u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 1);
        }
        1
    } else if (i & 0x04u8) != 0 {
        proof {
            assert((i & 0x04u8) != 0 ==> (i >> 2u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 2u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0 && j < 2u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 2);
        }
        2
    } else if (i & 0x08u8) != 0 {
        proof {
            assert((i & 0x08u8) != 0 ==> (i >> 3u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 3u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0
                    && (i & 0x04u8) == 0 && j < 3u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 3);
        }
        3
    } else if (i & 0x10u8) != 0 {
        proof {
            assert((i & 0x10u8) != 0 ==> (i >> 4u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 4u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0
                    && (i & 0x04u8) == 0 && (i & 0x08u8) == 0 && j < 4u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 4);
        }
        4
    } else if (i & 0x20u8) != 0 {
        proof {
            assert((i & 0x20u8) != 0 ==> (i >> 5u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 5u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0
                    && (i & 0x04u8) == 0 && (i & 0x08u8) == 0
                    && (i & 0x10u8) == 0 && j < 5u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 5);
        }
        5
    } else if (i & 0x40u8) != 0 {
        proof {
            assert((i & 0x40u8) != 0 ==> (i >> 6u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 6u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0
                    && (i & 0x04u8) == 0 && (i & 0x08u8) == 0
                    && (i & 0x10u8) == 0 && (i & 0x20u8) == 0 && j < 6u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 6);
        }
        6
    } else {
        proof {
            assert(i != 0
                && (i & 0x01u8) == 0 && (i & 0x02u8) == 0
                && (i & 0x04u8) == 0 && (i & 0x08u8) == 0
                && (i & 0x10u8) == 0 && (i & 0x20u8) == 0
                && (i & 0x40u8) == 0
                ==> (i >> 7u8) & 1u8 == 1u8) by (bit_vector);
            assert forall|j: u8| j < 7u8 implies (i >> j) & 1u8 == 0u8 by {
                assert((i & 0x01u8) == 0 && (i & 0x02u8) == 0
                    && (i & 0x04u8) == 0 && (i & 0x08u8) == 0
                    && (i & 0x10u8) == 0 && (i & 0x20u8) == 0
                    && (i & 0x40u8) == 0 && j < 7u8
                    ==> (i >> j) & 1u8 == 0u8) by (bit_vector);
            }
            lemma_u8_trailing_zeros_unique(i, 7);
        }
        7
    }
}

fn source_u8_trailing_zeros(i: u8) -> (r: u32)
    ensures
        r == u8_trailing_zeros(i),
{
    return source_core_intrinsics_cttz_u8(i);
}

}

fn main() {}