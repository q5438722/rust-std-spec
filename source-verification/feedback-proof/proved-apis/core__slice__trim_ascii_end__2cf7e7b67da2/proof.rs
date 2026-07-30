#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub open spec fn is_ascii_whitespace_byte(b: u8) -> bool {
    b == 9 || b == 10 || b == 12 || b == 13 || b == 32
}

pub assume_specification[ u8::is_ascii_whitespace ](b: &u8) -> (result: bool)
    ensures
        result == is_ascii_whitespace_byte(*b),
;

pub fn source_trim_ascii_end(slice: &[u8]) -> (result: &[u8])
    ensures
        slice@.len() >= result@.len(),
        result@ == slice@.subrange(0, result@.len() as int),
        forall|i: int| i >= (result@.len() as int) && slice@.len() > i ==> (
            slice@[i] == 9 || slice@[i] == 10 || slice@[i] == 12
                || slice@[i] == 13 || slice@[i] == 32
        ),
        result@.len() > 0 ==> !(
            slice@[(result@.len() as int) - 1] == 9
                || slice@[(result@.len() as int) - 1] == 10
                || slice@[(result@.len() as int) - 1] == 12
                || slice@[(result@.len() as int) - 1] == 13
                || slice@[(result@.len() as int) - 1] == 32
        ),
{
    let mut bytes = slice;
    // Mechanical lowering of the unsupported `[rest @ .., last]` slice pattern.
    loop
        invariant
            bytes@.len() <= slice@.len(),
            bytes@ == slice@.subrange(0, bytes@.len() as int),
            forall|i: int| i >= bytes@.len() && slice@.len() > i
                ==> is_ascii_whitespace_byte(slice@[i]),
        ensures
            bytes@.len() == 0 || !is_ascii_whitespace_byte(
                slice@[(bytes@.len() as int) - 1],
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
        proof {
            assert(len > 0);
            assert((len - 1) as int == old_len - 1);
            assert(0 <= len - 1 < bytes@.len());
            assert(0 <= len - 1 <= bytes@.len());
        }
        let rest = &bytes[0..len - 1];
        let last = &bytes[len - 1];

        proof {
            assert(rest@ == bytes@.subrange(0, old_len - 1));
            assert(*last == bytes@[old_len - 1]);
            vstd::seq::lemma_seq_subrange_composition(
                slice@, 0, old_len, 0, old_len - 1,
            );
            vstd::seq::lemma_seq_subrange_index(
                slice@, 0, old_len, old_len - 1,
            );
            assert(rest@ == slice@.subrange(0, old_len - 1));
            assert(*last == slice@[old_len - 1]);
            vstd::seq::lemma_seq_subrange_len(bytes@, 0, old_len - 1);
            assert(rest@.len() == old_len - 1);
        }

        if last.is_ascii_whitespace() {
            proof {
                assert(is_ascii_whitespace_byte(*last));
                assert(is_ascii_whitespace_byte(slice@[old_len - 1]));
                assert forall|i: int|
                    i >= rest@.len() && slice@.len() > i
                    implies is_ascii_whitespace_byte(slice@[i]) by {
                    if i < old_len {
                        assert(i == old_len - 1);
                    } else {
                        assert(i >= old_len);
                    }
                }
            }
            bytes = rest;
        } else {
            proof {
                assert(!is_ascii_whitespace_byte(*last));
                assert(!is_ascii_whitespace_byte(slice@[old_len - 1]));
                assert(bytes@.len() > 0);
                assert(!(
                    slice@[(bytes@.len() as int) - 1] == 9
                        || slice@[(bytes@.len() as int) - 1] == 10
                        || slice@[(bytes@.len() as int) - 1] == 12
                        || slice@[(bytes@.len() as int) - 1] == 13
                        || slice@[(bytes@.len() as int) - 1] == 32
                ));
            }
            break;
        }
    }
    bytes
}

}

fn main() {}