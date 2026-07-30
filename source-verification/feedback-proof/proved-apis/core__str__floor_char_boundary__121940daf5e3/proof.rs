#![allow(dead_code)]

use vstd::prelude::*;
use vstd::string::StringSliceAdditionalSpecFns;
use vstd::utf8::is_char_boundary;

#[cfg(verus_keep_ghost)]
macro_rules! debug_assert {
    ($condition:expr $(,)?) => {
        proof! {
            assert($condition);
        }
    };
}

verus! {

const fn source_u8_is_utf8_char_boundary(byte: u8) -> (result: bool)
    ensures
        result == !vstd::utf8::is_continuation_byte(byte),
{
    let result = (byte as i8) >= -0x40;
    proof {
        assert(
            ((byte as i8) >= -0x40i8)
                <==> !(0x80u8 <= byte && byte <= 0xbfu8)
        ) by (bit_vector);
    }
    result
}

proof fn char_boundary_in_bounds(bytes: Seq<u8>, index: int)
    requires
        vstd::utf8::valid_utf8(bytes),
        is_char_boundary(bytes, index),
    ensures
        0 <= index <= bytes.len(),
{
    reveal_with_fuel(is_char_boundary, 2);
    assert(index == 0 || !(index < 0 || bytes.len() < index));
}

proof fn close_char_boundary(bytes: Seq<u8>, index: int) -> (boundary: int)
    requires
        vstd::utf8::valid_utf8(bytes),
        0 <= index < bytes.len(),
    ensures
        0 <= boundary <= index,
        index <= boundary + 3,
        is_char_boundary(bytes, boundary),
    decreases bytes.len(),
{
    reveal_with_fuel(vstd::utf8::valid_utf8, 2);
    let scalar_len = vstd::utf8::length_of_first_scalar(bytes);
    let rest = vstd::utf8::pop_first_scalar(bytes);
    assert(vstd::utf8::valid_first_scalar(bytes));
    assert(vstd::utf8::valid_utf8(rest));
    assert(1 <= scalar_len <= 4) by {
        reveal(vstd::utf8::length_of_first_scalar);
    }
    assert(scalar_len <= bytes.len()) by {
        reveal(vstd::utf8::valid_first_scalar);
        reveal(vstd::utf8::valid_leading_and_continuation_bytes_first_codepoint);
        reveal(vstd::utf8::length_of_first_scalar);
    }
    reveal(vstd::utf8::pop_first_scalar);
    vstd::seq::lemma_seq_subrange_len(bytes, scalar_len, bytes.len() as int);
    assert(rest.len() == bytes.len() - scalar_len);

    if index < scalar_len {
        vstd::utf8::is_char_boundary_start_end_of_seq(bytes);
        0
    } else {
        assert(0 <= index - scalar_len < rest.len());
        let boundary_in_rest = close_char_boundary(rest, index - scalar_len);
        let boundary = boundary_in_rest + scalar_len;
        assert(
            is_char_boundary(bytes, boundary)
                == is_char_boundary(rest, boundary_in_rest)
        ) by {
            reveal_with_fuel(is_char_boundary, 1);
        }
        boundary
    }
}

pub const fn source_core_str_floor_char_boundary(
    s: &str,
    index: usize,
) -> (res: usize)
    ensures
        index >= res,
        s.spec_bytes().len() >= res as int,
        is_char_boundary(s.spec_bytes(), res as int),
        index as int >= s.spec_bytes().len() ==> res as int == s.spec_bytes().len(),
        forall|i: int| index as int >= i
            && #[trigger] is_char_boundary(s.spec_bytes(), i) ==> res as int >= i,
{
    proof {
        vstd::utf8::encode_utf8_valid_utf8(s@);
    }

    // Mechanically inline the first `str::len` call.
    let bytes_for_len = s.as_bytes();
    let len = <[u8]>::len(bytes_for_len);
    proof {
        vstd::slice::axiom_spec_len(bytes_for_len);
    }
    if index >= len {
        // Mechanically inline the second `str::len` call.
        let bytes_for_res = s.as_bytes();
        let res = <[u8]>::len(bytes_for_res);
        proof {
            vstd::slice::axiom_spec_len(bytes_for_res);
            assert(res as int == s.spec_bytes().len());
            vstd::utf8::is_char_boundary_start_end_of_seq(s.spec_bytes());
            assert(is_char_boundary(s.spec_bytes(), res as int));
            assert forall|i: int| index as int >= i
                && #[trigger] is_char_boundary(s.spec_bytes(), i)
                implies res as int >= i by {
                char_boundary_in_bounds(s.spec_bytes(), i);
            }
        }
        res
    } else {
        proof {
            vstd::utf8::is_char_boundary_start_end_of_seq(s.spec_bytes());
        }
        let ghost close = close_char_boundary(s.spec_bytes(), index as int);
        let mut i = index;
        while i > 0
            invariant
                i <= index,
                (index as int) < s.spec_bytes().len(),
                vstd::utf8::valid_utf8(s.spec_bytes()),
                is_char_boundary(s.spec_bytes(), 0),
                0 <= close <= i as int,
                index as int <= close + 3,
                is_char_boundary(s.spec_bytes(), close),
                forall|j: int| (i as int) < j <= index as int
                    ==> !is_char_boundary(s.spec_bytes(), j),
            ensures
                is_char_boundary(s.spec_bytes(), i as int),
            decreases i,
        {
            let byte = s.as_bytes()[i];
            let boundary = source_u8_is_utf8_char_boundary(byte);
            proof {
                assert(byte == s.spec_bytes()[i as int]);
                vstd::utf8::is_char_boundary_iff_not_is_continuation_byte(
                    s.spec_bytes(),
                    i as int,
                );
                assert(boundary == is_char_boundary(s.spec_bytes(), i as int));
            }
            if boundary {
                break;
            }
            let old_i = i;
            i -= 1;
            proof {
                assert(i as int == old_i as int - 1);
                assert(close < old_i as int);
                assert(close <= i as int);
                assert forall|j: int| (i as int) < j <= index as int
                    implies !is_char_boundary(s.spec_bytes(), j) by {
                    if j == old_i as int {
                        assert(!is_char_boundary(s.spec_bytes(), j));
                    } else {
                        assert((old_i as int) < j);
                    }
                }
            }
        }

        proof {
            assert(is_char_boundary(s.spec_bytes(), i as int));
            assert forall|j: int| index as int >= j
                && #[trigger] is_char_boundary(s.spec_bytes(), j)
                implies i as int >= j by {
                if (i as int) < j {
                    assert(!is_char_boundary(s.spec_bytes(), j));
                }
            }
        }

        //  The character boundary will be within four bytes of the index
        debug_assert!(i >= index.saturating_sub(3));

        i
    }
}

} // verus!

fn main() {}