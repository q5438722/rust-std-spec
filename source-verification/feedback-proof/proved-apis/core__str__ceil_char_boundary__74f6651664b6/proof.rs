#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::seq::lemma_seq_subrange_len;
use vstd::string::StringSliceAdditionalSpecFns;
use vstd::utf8::{
    is_char_boundary,
    is_char_boundary_iff_not_is_continuation_byte,
    is_char_boundary_start_end_of_seq,
    is_continuation_byte,
    length_of_first_scalar,
    pop_first_scalar,
    valid_first_scalar,
    valid_utf8,
};

verus! {

const fn source_str_len(s: &str) -> (len: usize)
    ensures
        len as int == s.spec_bytes().len(),
{
    let bytes = s.as_bytes();
    let len = bytes.len();
    proof {
        vstd::slice::axiom_spec_len(bytes);
    }
    len
}

const fn source_u8_is_utf8_char_boundary(byte: u8) -> (result: bool)
    ensures
        result == !is_continuation_byte(byte),
{
    let result = (byte as i8) >= -0x40;
    proof {
        assert(
            ((byte as i8) >= -0x40i8) <==> !(0x80u8 <= byte && byte <= 0xbfu8)
        ) by (bit_vector);
    }
    result
}

proof fn char_boundary_within_three(bytes: Seq<u8>, index: int)
    requires
        valid_utf8(bytes),
        0 <= index <= bytes.len(),
    ensures
        exists|boundary: int|
            index <= boundary <= bytes.len()
            && boundary <= index + 3
            && is_char_boundary(bytes, boundary),
    decreases index,
{
    if index == 0 {
        is_char_boundary_start_end_of_seq(bytes);
        assert(exists|boundary: int|
            index <= boundary <= bytes.len()
            && boundary <= index + 3
            && is_char_boundary(bytes, boundary)) by {
            assert(is_char_boundary(bytes, 0));
        }
    } else {
        assert(bytes.len() != 0);
        reveal_with_fuel(valid_utf8, 2);
        let width = length_of_first_scalar(bytes);
        assert(valid_first_scalar(bytes));
        assert(1 <= width <= 4);
        assert(width <= bytes.len());

        if index < width {
            assert(width <= index + 3);
            assert(is_char_boundary(bytes, width)) by {
                reveal_with_fuel(is_char_boundary, 2);
            }
            assert(exists|boundary: int|
                index <= boundary <= bytes.len()
                && boundary <= index + 3
                && is_char_boundary(bytes, boundary)) by {
                assert(is_char_boundary(bytes, width));
            }
        } else {
            let tail = pop_first_scalar(bytes);
            lemma_seq_subrange_len(bytes, width, bytes.len() as int);
            assert(tail.len() == bytes.len() - width);
            assert(0 <= index - width <= tail.len());
            assert(valid_utf8(tail));
            char_boundary_within_three(tail, index - width);
            let boundary_tail = choose|boundary: int|
                index - width <= boundary <= tail.len()
                && boundary <= index - width + 3
                && is_char_boundary(tail, boundary);
            let boundary = boundary_tail + width;
            assert(index <= boundary <= bytes.len());
            assert(boundary <= index + 3);
            assert(is_char_boundary(bytes, boundary)) by {
                reveal_with_fuel(is_char_boundary, 2);
            }
            assert(exists|candidate: int|
                index <= candidate <= bytes.len()
                && candidate <= index + 3
                && is_char_boundary(bytes, candidate)) by {
                assert(is_char_boundary(bytes, boundary));
            }
        }
    }
}

pub const fn source_core_str_ceil_char_boundary(
    s: &str,
    index: usize,
) -> (res: usize)
    ensures
        s.spec_bytes().len() >= res as int,
        is_char_boundary(s.spec_bytes(), res as int),
        index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(),
        s.spec_bytes().len() >= index as int ==> res as int >= index as int,
        forall|i: int| i >= index as int && s.spec_bytes().len() >= i
            && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> i >= res as int,
        index as int + 3 >= res as int,
{
    proof {
        vstd::utf8::encode_utf8_valid_utf8(s@);
        is_char_boundary_start_end_of_seq(s.spec_bytes());
    }

    if index >= source_str_len(s) {
        source_str_len(s)
    } else {
        let mut i = index;
        proof {
            char_boundary_within_three(s.spec_bytes(), index as int);
        }
        let ghost next_boundary = choose|boundary: int|
            index as int <= boundary <= s.spec_bytes().len()
            && boundary <= index as int + 3
            && is_char_boundary(s.spec_bytes(), boundary);

        while i < source_str_len(s)
            invariant
                index as int <= i as int <= next_boundary,
                next_boundary <= s.spec_bytes().len(),
                next_boundary <= index as int + 3,
                is_char_boundary(s.spec_bytes(), next_boundary),
                valid_utf8(s.spec_bytes()),
                is_char_boundary(s.spec_bytes(), s.spec_bytes().len() as int),
                forall|candidate: int|
                    index as int <= candidate < i as int
                    ==> !is_char_boundary(s.spec_bytes(), candidate),
            ensures
                is_char_boundary(s.spec_bytes(), i as int),
            decreases
                s.spec_bytes().len() - i as int,
        {
            let byte = s.as_bytes()[i];
            if source_u8_is_utf8_char_boundary(byte) {
                proof {
                    is_char_boundary_iff_not_is_continuation_byte(
                        s.spec_bytes(),
                        i as int,
                    );
                    assert(is_char_boundary(s.spec_bytes(), i as int));
                }
                break;
            }
            proof {
                is_char_boundary_iff_not_is_continuation_byte(
                    s.spec_bytes(),
                    i as int,
                );
                assert(!is_char_boundary(s.spec_bytes(), i as int));
                assert((i as int) < next_boundary);
                assert forall|candidate: int|
                    index as int <= candidate < i as int + 1
                    implies !is_char_boundary(s.spec_bytes(), candidate) by {
                    if candidate == i as int {
                        assert(!is_char_boundary(s.spec_bytes(), candidate));
                    }
                }
            }
            i += 1;
        }

        //  The character boundary will be within four bytes of the index
        proof {
            assert(index as int <= i as int);
            assert(is_char_boundary(s.spec_bytes(), i as int));
            assert forall|candidate: int|
                candidate >= index as int
                && s.spec_bytes().len() >= candidate
                && #[trigger] is_char_boundary(s.spec_bytes(), candidate)
                implies candidate >= i as int by {
                if candidate < i as int {
                    assert(!is_char_boundary(s.spec_bytes(), candidate));
                }
            }
            assert(i as int <= index as int + 3);
        }

        // Verus does not support the panic branch of `debug_assert!`; retain
        // its condition as the ghost check above.

        i
    }
}

} // verus!

fn main() {}