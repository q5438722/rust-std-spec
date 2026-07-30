#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

fn source_u8_is_utf8_char_boundary(byte: u8) -> (result: bool)
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

fn source_str_is_char_boundary(s: &str, index: usize) -> (result: bool)
    ensures
        result == is_char_boundary(s.spec_bytes(), index as int),
{
    proof {
        encode_utf8_valid_utf8(s@);
    }

    if index == 0 {
        return true;
    }

    let bytes_for_len = s.as_bytes();
    let len = <[u8]>::len(bytes_for_len);
    proof {
        vstd::slice::axiom_spec_len(bytes_for_len);
    }
    if index >= len {
        let bytes_for_end = s.as_bytes();
        let end = <[u8]>::len(bytes_for_end);
        let result = index == end;
        proof {
            vstd::slice::axiom_spec_len(bytes_for_end);
            if result {
                assert(index as int == s.spec_bytes().len());
                is_char_boundary_start_end_of_seq(s.spec_bytes());
            } else {
                assert(s.spec_bytes().len() < index as int);
                reveal_with_fuel(is_char_boundary, 1);
            }
            assert(result == is_char_boundary(s.spec_bytes(), index as int));
        }
        result
    } else {
        let byte = s.as_bytes()[index];
        let result = source_u8_is_utf8_char_boundary(byte);
        proof {
            is_char_boundary_iff_not_is_continuation_byte(
                s.spec_bytes(),
                index as int,
            );
            assert(result == is_char_boundary(s.spec_bytes(), index as int));
        }
        result
    }
}

} // verus!

fn main() {}