#![allow(dead_code, unused_imports)]

use vstd::prelude::*;

verus! {

pub open spec fn is_ascii_whitespace_byte(b: u8) -> bool {
    b == 0x09u8
        || b == 0x0au8
        || b == 0x0cu8
        || b == 0x0du8
        || b == 0x20u8
}

pub assume_specification[ u8::is_ascii_whitespace ](b: &u8) -> (result: bool)
    ensures
        result == is_ascii_whitespace_byte(*b),
;

pub fn source_trim_ascii_start(slice: &[u8]) -> (ret: &[u8])
    ensures
        exists|start: int|
            start >= 0
            && slice@.len() >= start
            && ret@ == (#[trigger] slice@.subrange(start, slice@.len() as int))
            && (forall|i: int| i >= 0 && start > i ==>
                slice@[i] == 0x09u8
                || slice@[i] == 0x0au8
                || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8
                || slice@[i] == 0x20u8)
            && (slice@.len() > start ==>
                !(slice@[start] == 0x09u8
                || slice@[start] == 0x0au8
                || slice@[start] == 0x0cu8
                || slice@[start] == 0x0du8
                || slice@[start] == 0x20u8)),
{
    let mut bytes = slice;
    // Mechanical lowering of the unsupported `[first, rest @ ..]` slice pattern.
    loop
        invariant
            bytes@.len() <= slice@.len(),
            bytes@ == slice@.subrange(
                slice@.len() as int - bytes@.len() as int,
                slice@.len() as int,
            ),
            forall|i: int|
                0 <= i < slice@.len() as int - bytes@.len() as int
                    ==> is_ascii_whitespace_byte(slice@[i]),
        ensures
            bytes@.len() == 0 || !is_ascii_whitespace_byte(
                slice@[slice@.len() as int - bytes@.len() as int],
            ),
        decreases
            bytes@.len(),
    {
        let len = bytes.len();
        proof {
            vstd::slice::axiom_spec_len(bytes);
            assert(len == bytes@.len());
        }
        if len == 0 {
            break;
        }

        let ghost old_len: int = bytes@.len() as int;
        let ghost old_start: int = slice@.len() as int - old_len;
        proof {
            assert(len > 0);
            assert(old_len > 0);
            assert(0 <= old_start < slice@.len());
            assert(old_start + old_len == slice@.len());
            assert(0 <= 1 <= old_len);
        }
        let first = &bytes[0];
        let rest = &bytes[1..len];

        proof {
            assert(*first == bytes@[0]);
            assert(rest@ == bytes@.subrange(1, old_len));
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                old_start,
                slice@.len() as int,
                0,
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                old_start,
                slice@.len() as int,
                1,
                old_len,
            );
            assert(*first == slice@[old_start]);
            assert(rest@ == slice@.subrange(old_start + 1, slice@.len() as int));
            vstd::seq::lemma_seq_subrange_len(bytes@, 1, old_len);
            assert(rest@.len() == old_len - 1);
            assert(
                slice@.len() as int - rest@.len() as int == old_start + 1
            );
        }

        if first.is_ascii_whitespace() {
            proof {
                assert(is_ascii_whitespace_byte(*first));
                assert(is_ascii_whitespace_byte(slice@[old_start]));
                assert forall|i: int|
                    0 <= i < slice@.len() as int - rest@.len() as int
                    implies is_ascii_whitespace_byte(slice@[i]) by {
                    if i < old_start {
                        assert(
                            i < slice@.len() as int - bytes@.len() as int
                        );
                    } else {
                        assert(i == old_start);
                    }
                }
            }
            bytes = rest;
        } else {
            proof {
                assert(!is_ascii_whitespace_byte(*first));
                assert(!is_ascii_whitespace_byte(slice@[old_start]));
                assert(
                    slice@.len() as int - bytes@.len() as int == old_start
                );
            }
            break;
        }
    }
    proof {
        let start = slice@.len() as int - bytes@.len() as int;
        assert(start >= 0);
        assert(slice@.len() >= start);
        assert(bytes@ == slice@.subrange(start, slice@.len() as int));
        assert forall|i: int| i >= 0 && start > i implies
            slice@[i] == 0x09u8
                || slice@[i] == 0x0au8
                || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8
                || slice@[i] == 0x20u8 by {
            assert(is_ascii_whitespace_byte(slice@[i]));
        }
        assert(slice@.len() > start ==> !(
            slice@[start] == 0x09u8
                || slice@[start] == 0x0au8
                || slice@[start] == 0x0cu8
                || slice@[start] == 0x0du8
                || slice@[start] == 0x20u8
        )) by {
            if slice@.len() > start {
                assert(bytes@.len() > 0);
                assert(!is_ascii_whitespace_byte(slice@[start]));
            }
        }
        assert(exists|witness: int|
            witness >= 0
            && slice@.len() >= witness
            && bytes@ == slice@.subrange(witness, slice@.len() as int)
            && (forall|i: int|
                i >= 0 && witness > i ==>
                    is_ascii_whitespace_byte(slice@[i]))
            && (slice@.len() > witness ==>
                !is_ascii_whitespace_byte(slice@[witness]))
        ) by {
            assert(start >= 0);
        }
        reveal(is_ascii_whitespace_byte);
    }
    bytes
}

}

fn main() {}