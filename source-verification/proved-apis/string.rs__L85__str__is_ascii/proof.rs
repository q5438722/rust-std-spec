#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub open spec fn is_ascii_bytes(bytes: Seq<u8>) -> bool {
    forall|i: int| 0 <= i < bytes.len() ==> bytes[i] <= 0x7f
}

pub assume_specification[ <[u8]>::is_ascii ](slice: &[u8]) -> (ret: bool)
    ensures
        ret == is_ascii_bytes(slice@),
;

proof fn is_ascii_bytes_concat(left: Seq<u8>, right: Seq<u8>)
    ensures
        is_ascii_bytes(left + right) <==> is_ascii_bytes(left) && is_ascii_bytes(right),
{
    if is_ascii_bytes(left + right) {
        assert forall|i: int| 0 <= i < left.len() implies left[i] <= 0x7f by {
            assert((left + right)[i] == left[i]);
        }
        assert forall|i: int| 0 <= i < right.len() implies right[i] <= 0x7f by {
            assert((left + right)[left.len() + i] == right[i]);
        }
    }
    if is_ascii_bytes(left) && is_ascii_bytes(right) {
        assert forall|i: int| 0 <= i < (left + right).len() implies
            (left + right)[i] <= 0x7f by {
            if i < left.len() {
                assert((left + right)[i] == left[i]);
            } else {
                assert((left + right)[i] == right[i - left.len()]);
            }
        }
    }
}

proof fn is_ascii_scalar(c: char)
    ensures
        is_ascii_bytes(encode_scalar(c as u32)) <==> '\0' <= c <= '\u{7f}',
{
    char_is_scalar(c);
    let scalar = c as u32;
    if has_width_1_encoding(scalar) {
        assert(leading_byte_width_1(scalar) <= 0x7f) by (bit_vector)
            requires
                has_width_1_encoding(scalar),
        ;
    } else if has_width_2_encoding(scalar) {
        assert(leading_byte_width_2(scalar) > 0x7f) by (bit_vector)
            requires
                has_width_2_encoding(scalar),
        ;
    } else if has_width_3_encoding(scalar) {
        assert(leading_byte_width_3(scalar) > 0x7f) by (bit_vector)
            requires
                has_width_3_encoding(scalar),
        ;
    } else {
        assert(has_width_4_encoding(scalar));
        assert(leading_byte_width_4(scalar) > 0x7f) by (bit_vector)
            requires
                has_width_4_encoding(scalar),
        ;
    }
}

proof fn is_ascii_utf8(chars: Seq<char>)
    ensures
        is_ascii_bytes(encode_utf8(chars)) <==> is_ascii_chars(chars),
    decreases chars.len(),
{
    if chars.len() == 0 {
    } else {
        let first = chars[0];
        let rest = chars.drop_first();
        is_ascii_scalar(first);
        is_ascii_utf8(rest);
        is_ascii_bytes_concat(encode_scalar(first as u32), encode_utf8(rest));

        assert(is_ascii_chars(chars) <==>
            ('\0' <= first <= '\u{7f}' && is_ascii_chars(rest))) by {
            if is_ascii_chars(chars) {
                assert('\0' <= chars[0] <= '\u{7f}');
                assert forall|i: int| 0 <= i < rest.len() implies
                    '\0' <= #[trigger] rest[i] <= '\u{7f}' by {
                    assert(rest[i] == chars[i + 1]);
                }
            }
            if '\0' <= first <= '\u{7f}' && is_ascii_chars(rest) {
                assert forall|i: int| 0 <= i < chars.len() implies
                    '\0' <= #[trigger] chars[i] <= '\u{7f}' by {
                    if i > 0 {
                        assert(chars[i] == rest[i - 1]);
                    }
                }
            }
        }
    }
}

fn source_str_is_ascii(s: &str) -> (b: bool)
    ensures
        b == is_ascii(s),
{
    let bytes = s.as_bytes();
    let b = bytes.is_ascii();
    proof {
        is_ascii_utf8(s@);
    }
    b
}

} // verus!

fn main() {}