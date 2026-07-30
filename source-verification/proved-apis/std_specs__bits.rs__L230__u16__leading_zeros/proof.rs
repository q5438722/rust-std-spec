#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

proof fn lemma_u16_leading_zeros_unique(i: u16, n: u16)
    requires
        n < 16,
        (i >> sub(15u16, n)) & 1u16 == 1u16,
        forall|j: u16| 16 - n <= j < 16 ==> (i >> j) & 1u16 == 0u16,
    ensures
        u16_leading_zeros(i) == n as u32,
{
    axiom_u16_leading_zeros(i);
    let x = u16_leading_zeros(i);
    assert(i == 0 ==> (i >> sub(15u16, n)) & 1u16 == 0u16) by (bit_vector);
    assert(i != 0);
    assert(x < 16);
    if x < n {
        assert((i >> sub(15u16, x as u16)) & 1u16 != 0u16);
        assert((i >> sub(15u16, x as u16)) & 1u16 == 0u16);
    } else if x > n {
        assert((i >> sub(15u16, n)) & 1u16 == 0u16);
    }
}

// Fixed-width executable desugaring of core::intrinsics::ctlz::<u16>.
fn source_core_intrinsics_ctlz_u16(i: u16) -> (r: u32)
    ensures
        r == u16_leading_zeros(i),
{
    if i >= 0x8000u16 {
        proof {
            assert(i >= 0x8000u16 ==> (i >> 15u16) & 1u16 == 1u16) by (bit_vector);
            lemma_u16_leading_zeros_unique(i, 0);
        }
        0
    } else if i >= 0x4000u16 {
        proof {
            assert(0x4000u16 <= i < 0x8000u16
                ==> (i >> 14u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 15u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x8000u16 && 15u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 1);
        }
        1
    } else if i >= 0x2000u16 {
        proof {
            assert(0x2000u16 <= i < 0x4000u16
                ==> (i >> 13u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 14u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x4000u16 && 14u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 2);
        }
        2
    } else if i >= 0x1000u16 {
        proof {
            assert(0x1000u16 <= i < 0x2000u16
                ==> (i >> 12u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 13u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x2000u16 && 13u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 3);
        }
        3
    } else if i >= 0x0800u16 {
        proof {
            assert(0x0800u16 <= i < 0x1000u16
                ==> (i >> 11u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 12u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x1000u16 && 12u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 4);
        }
        4
    } else if i >= 0x0400u16 {
        proof {
            assert(0x0400u16 <= i < 0x0800u16
                ==> (i >> 10u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 11u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0800u16 && 11u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 5);
        }
        5
    } else if i >= 0x0200u16 {
        proof {
            assert(0x0200u16 <= i < 0x0400u16
                ==> (i >> 9u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 10u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0400u16 && 10u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 6);
        }
        6
    } else if i >= 0x0100u16 {
        proof {
            assert(0x0100u16 <= i < 0x0200u16
                ==> (i >> 8u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 9u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0200u16 && 9u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 7);
        }
        7
    } else if i >= 0x0080u16 {
        proof {
            assert(0x0080u16 <= i < 0x0100u16
                ==> (i >> 7u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 8u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0100u16 && 8u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 8);
        }
        8
    } else if i >= 0x0040u16 {
        proof {
            assert(0x0040u16 <= i < 0x0080u16
                ==> (i >> 6u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 7u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0080u16 && 7u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 9);
        }
        9
    } else if i >= 0x0020u16 {
        proof {
            assert(0x0020u16 <= i < 0x0040u16
                ==> (i >> 5u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 6u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0040u16 && 6u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 10);
        }
        10
    } else if i >= 0x0010u16 {
        proof {
            assert(0x0010u16 <= i < 0x0020u16
                ==> (i >> 4u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 5u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0020u16 && 5u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 11);
        }
        11
    } else if i >= 0x0008u16 {
        proof {
            assert(0x0008u16 <= i < 0x0010u16
                ==> (i >> 3u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 4u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0010u16 && 4u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 12);
        }
        12
    } else if i >= 0x0004u16 {
        proof {
            assert(0x0004u16 <= i < 0x0008u16
                ==> (i >> 2u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 3u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0008u16 && 3u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 13);
        }
        13
    } else if i >= 0x0002u16 {
        proof {
            assert(0x0002u16 <= i < 0x0004u16
                ==> (i >> 1u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 2u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0004u16 && 2u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 14);
        }
        14
    } else if i >= 0x0001u16 {
        proof {
            assert(0x0001u16 <= i < 0x0002u16
                ==> (i >> 0u16) & 1u16 == 1u16) by (bit_vector);
            assert forall|j: u16| 1u16 <= j < 16u16 implies
                (i >> j) & 1u16 == 0u16 by {
                assert(i < 0x0002u16 && 1u16 <= j < 16u16
                    ==> (i >> j) & 1u16 == 0u16) by (bit_vector);
            }
            lemma_u16_leading_zeros_unique(i, 15);
        }
        15
    } else {
        proof {
            assert(i < 1u16 ==> i == 0u16) by (bit_vector);
            assert(i == 0u16);
            axiom_u16_leading_zeros(i);
        }
        16
    }
}

fn source_u16_leading_zeros(i: u16) -> (r: u32)
    ensures
        r == u16_leading_zeros(i),
{
    return source_core_intrinsics_ctlz_u16(i);
}

} // verus!

fn main() {}