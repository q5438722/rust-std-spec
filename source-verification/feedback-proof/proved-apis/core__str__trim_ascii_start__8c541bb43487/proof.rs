#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub open spec fn is_ascii_whitespace_byte(b: u8) -> bool {
    b == 0x09u8 || b == 0x0au8 || b == 0x0cu8 || b == 0x0du8 || b == 0x20u8
}

pub open spec fn is_ascii_whitespace_char(c: char) -> bool {
    c as u32 == 0x09u32
        || c as u32 == 0x0au32
        || c as u32 == 0x0cu32
        || c as u32 == 0x0du32
        || c as u32 == 0x20u32
}

pub open spec fn is_ascii_whitespace_char_nat(c: char) -> bool {
    c as nat == 0x09
        || c as nat == 0x0a
        || c as nat == 0x0c
        || c as nat == 0x0d
        || c as nat == 0x20
}

pub assume_specification<'a>[ core::str::from_utf8_unchecked ](
    bytes: &'a [u8],
) -> (result: &'a str)
    requires
        valid_utf8(bytes@),
    ensures
        result.spec_bytes() == bytes@,
;

pub assume_specification[ <[u8]>::trim_ascii_start ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        exists|start: int|
            start >= 0
            && slice@.len() >= start
            && ret@ == slice@.subrange(start, slice@.len() as int)
            && (forall|i: int|
                i >= 0 && start > i ==> is_ascii_whitespace_byte(slice@[i]))
            && (slice@.len() > start ==>
                !is_ascii_whitespace_byte(slice@[start])),
;

proof fn lemma_ascii_whitespace_byte_bit_facts(b: u8)
    by (bit_vector)
    requires
        is_ascii_whitespace_byte(b),
    ensures
        is_leading_byte_width_1(b),
        (b & 0x7fu8) == b,
{
}

proof fn lemma_ascii_whitespace_scalar_bit_facts(c: u32)
    by (bit_vector)
    requires
        c == 0x09u32
            || c == 0x0au32
            || c == 0x0cu32
            || c == 0x0du32
            || c == 0x20u32,
    ensures
        has_width_1_encoding(c),
        is_ascii_whitespace_byte(leading_byte_width_1(c)),
{
}

proof fn lemma_ascii_whitespace_char_casts(c: char)
    ensures
        is_ascii_whitespace_char(c) <==> is_ascii_whitespace_char_nat(c),
{
    char_is_scalar(c);
    if is_ascii_whitespace_char(c) {
        if c as u32 == 0x09u32 {
            assert(c as nat == 0x09);
        } else if c as u32 == 0x0au32 {
            assert(c as nat == 0x0a);
        } else if c as u32 == 0x0cu32 {
            assert(c as nat == 0x0c);
        } else if c as u32 == 0x0du32 {
            assert(c as nat == 0x0d);
        } else {
            assert(c as u32 == 0x20u32);
            assert(c as nat == 0x20);
        }
    }
    if is_ascii_whitespace_char_nat(c) {
        if c as nat == 0x09 {
            assert(c as u32 == 0x09u32);
        } else if c as nat == 0x0a {
            assert(c as u32 == 0x0au32);
        } else if c as nat == 0x0c {
            assert(c as u32 == 0x0cu32);
        } else if c as nat == 0x0d {
            assert(c as u32 == 0x0du32);
        } else {
            assert(c as nat == 0x20);
            assert(c as u32 == 0x20u32);
        }
    }
}

proof fn lemma_whitespace_byte_starts_whitespace_char(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_byte(encode_utf8(chars)[0]),
    ensures
        is_ascii_whitespace_char(chars[0]),
        length_of_first_scalar(encode_utf8(chars)) == 1,
        pop_first_scalar(encode_utf8(chars)) =~= encode_utf8(chars.drop_first()),
{
    let bytes = encode_utf8(chars);
    let b = bytes[0];
    char_is_scalar(chars[0]);
    lemma_ascii_whitespace_byte_bit_facts(b);
    encode_utf8_first_scalar(chars);
    assert(decode_first_scalar(bytes) == b as u32) by {
        reveal(decode_first_scalar);
        reveal(decode_first_codepoint);
        reveal(codepoint_width_1);
        reveal(leading_bits_width_1);
    }
    assert(is_ascii_whitespace_char(chars[0])) by {
        if b == 0x09u8 {
            assert(chars[0] as u32 == 0x09u32);
        } else if b == 0x0au8 {
            assert(chars[0] as u32 == 0x0au32);
        } else if b == 0x0cu8 {
            assert(chars[0] as u32 == 0x0cu32);
        } else if b == 0x0du8 {
            assert(chars[0] as u32 == 0x0du32);
        } else {
            assert(b == 0x20u8);
            assert(chars[0] as u32 == 0x20u32);
        }
    }
    assert(length_of_first_scalar(bytes) == 1) by {
        reveal(length_of_first_scalar);
        reveal(length_of_first_codepoint);
    }
    assert(pop_first_scalar(bytes) =~= encode_utf8(chars.drop_first()));
}

proof fn lemma_whitespace_char_starts_whitespace_byte(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_char(chars[0]),
    ensures
        is_ascii_whitespace_byte(encode_utf8(chars)[0]),
{
    let c = chars[0];
    char_is_scalar(c);
    lemma_ascii_whitespace_scalar_bit_facts(c as u32);
    reveal(encode_utf8);
    reveal(encode_scalar);
}

proof fn lemma_ascii_whitespace_prefix_is_char_prefix(chars: Seq<char>, start: int)
    requires
        0 <= start <= encode_utf8(chars).len(),
        forall|i: int|
            0 <= i < start ==> is_ascii_whitespace_byte(encode_utf8(chars)[i]),
    ensures
        start <= chars.len(),
        forall|i: int|
            0 <= i < start ==> is_ascii_whitespace_char(chars[i]),
        encode_utf8(chars).subrange(start, encode_utf8(chars).len() as int)
            =~= encode_utf8(chars.subrange(start, chars.len() as int)),
    decreases start,
{
    let bytes = encode_utf8(chars);
    if start == 0 {
        assert(bytes.subrange(0, bytes.len() as int) =~= bytes);
        assert(chars.subrange(0, chars.len() as int) =~= chars);
    } else {
        assert(bytes.len() > 0);
        assert(chars.len() > 0) by {
            if chars.len() == 0 {
                reveal(encode_utf8);
            }
        }
        assert(is_ascii_whitespace_byte(bytes[0]));
        lemma_whitespace_byte_starts_whitespace_char(chars);

        let rest_chars = chars.drop_first();
        let rest_bytes = encode_utf8(rest_chars);
        assert(bytes.subrange(1, bytes.len() as int) =~= rest_bytes) by {
            reveal(pop_first_scalar);
        }
        assert(0 <= start - 1 <= rest_bytes.len());
        assert forall|i: int|
            0 <= i < start - 1 implies is_ascii_whitespace_byte(rest_bytes[i]) by {
            assert(0 <= i < rest_bytes.len());
            assert(0 <= i + 1 < bytes.len());
            assert(rest_bytes[i] == bytes[i + 1]);
        }

        lemma_ascii_whitespace_prefix_is_char_prefix(rest_chars, start - 1);

        assert(start <= chars.len());
        assert forall|i: int|
            0 <= i < start implies is_ascii_whitespace_char(chars[i]) by {
            if i == 0 {
                assert(is_ascii_whitespace_char(chars[0]));
            } else {
                assert(0 <= i - 1 < rest_chars.len());
                assert(chars[i] == rest_chars[i - 1]);
                assert(is_ascii_whitespace_char(rest_chars[i - 1]));
            }
        }
        assert(bytes.subrange(start, bytes.len() as int)
            =~= rest_bytes.subrange(start - 1, rest_bytes.len() as int));
        assert(chars.subrange(start, chars.len() as int)
            =~= rest_chars.subrange(start - 1, rest_chars.len() as int));
    }
}

proof fn lemma_nonwhitespace_byte_starts_nonwhitespace_char(
    chars: Seq<char>,
    start: int,
)
    requires
        0 <= start < chars.len(),
        start < encode_utf8(chars).len(),
        encode_utf8(chars).subrange(start, encode_utf8(chars).len() as int)
            =~= encode_utf8(chars.subrange(start, chars.len() as int)),
        !is_ascii_whitespace_byte(encode_utf8(chars)[start]),
    ensures
        !is_ascii_whitespace_char(chars[start]),
{
    let suffix = chars.subrange(start, chars.len() as int);
    assert(suffix.len() > 0);
    assert(suffix[0] == chars[start]);
    assert(encode_utf8(suffix).len() > 0) by {
        reveal(encode_utf8);
    }
    assert(encode_utf8(suffix)[0] == encode_utf8(chars)[start]);
    if is_ascii_whitespace_char(chars[start]) {
        lemma_whitespace_char_starts_whitespace_byte(suffix);
    }
}

pub const fn source_str_trim_ascii_start(s: &str) -> (res: &str)
    ensures
        exists|start: int|
            start >= 0
            && s@.len() >= start
            && res@ == s@.subrange(start, s@.len() as int)
            && (forall|i: int| i >= 0 && start > i ==> (
                s@[i] as nat == 0x09 || s@[i] as nat == 0x0a
                    || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d
                    || s@[i] as nat == 0x20
            ))
            && (s@.len() > start ==> !(
                s@[start] as nat == 0x09 || s@[start] as nat == 0x0a
                    || s@[start] as nat == 0x0c || s@[start] as nat == 0x0d
                    || s@[start] as nat == 0x20
            )),
{
    let bytes = s.as_bytes();
    let trimmed = bytes.trim_ascii_start();
    let ghost start = choose|start: int|
        start >= 0
        && bytes@.len() >= start
        && trimmed@ == bytes@.subrange(start, bytes@.len() as int)
        && (forall|i: int|
            i >= 0 && start > i ==> is_ascii_whitespace_byte(bytes@[i]))
        && (bytes@.len() > start ==> !is_ascii_whitespace_byte(bytes@[start]));
    proof {
        lemma_ascii_whitespace_prefix_is_char_prefix(s@, start);
        if s@.len() > start {
            let suffix = s@.subrange(start, s@.len() as int);
            assert(suffix.len() > 0);
            assert(encode_utf8(suffix).len() > 0) by {
                reveal(encode_utf8);
            }
            assert(bytes@.subrange(start, bytes@.len() as int).len() > 0);
            assert(bytes@.len() > start);
            lemma_nonwhitespace_byte_starts_nonwhitespace_char(s@, start);
        }
        encode_utf8_valid_utf8(s@.subrange(start, s@.len() as int));
        assert(trimmed@ =~= encode_utf8(s@.subrange(start, s@.len() as int)));
    }
    let res = unsafe { core::str::from_utf8_unchecked(trimmed) };
    proof {
        encode_utf8_decode_utf8(res@);
        encode_utf8_decode_utf8(s@.subrange(start, s@.len() as int));
        assert(res@ == s@.subrange(start, s@.len() as int));
        assert forall|i: int|
            0 <= i < start implies is_ascii_whitespace_char_nat(s@[i]) by {
            lemma_ascii_whitespace_char_casts(s@[i]);
        }
        if s@.len() > start {
            lemma_ascii_whitespace_char_casts(s@[start]);
            assert(!is_ascii_whitespace_char_nat(s@[start]));
        }
        assert(exists|witness: int|
            witness >= 0
            && s@.len() >= witness
            && res@ == s@.subrange(witness, s@.len() as int)
            && (forall|i: int|
                i >= 0 && witness > i ==> is_ascii_whitespace_char_nat(s@[i]))
            && (s@.len() > witness ==> !is_ascii_whitespace_char_nat(s@[witness]))
        ) by {
            assert(start >= 0);
        }
    }
    res
}

} // verus!

fn main() {}