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

pub assume_specification[ <[u8]>::trim_ascii_end ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        slice@.len() >= ret@.len(),
        ret@ == slice@.subrange(0, ret@.len() as int),
        forall|i: int| i >= ret@.len() && slice@.len() > i ==> (
            slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
        ),
        ret@.len() > 0 ==> !(
            slice@[ret@.len() - 1] == 0x09u8 || slice@[ret@.len() - 1] == 0x0au8
                || slice@[ret@.len() - 1] == 0x0cu8
                || slice@[ret@.len() - 1] == 0x0du8
                || slice@[ret@.len() - 1] == 0x20u8
        ),
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

proof fn lemma_encode_utf8_concat(left: Seq<char>, right: Seq<char>)
    ensures
        encode_utf8(left + right) =~= encode_utf8(left) + encode_utf8(right),
    decreases left.len(),
{
    if left.len() == 0 {
        assert(left =~= seq![]);
        assert(left + right =~= right);
        reveal(encode_utf8);
    } else {
        let tail = left.drop_first();
        assert((left + right)[0] == left[0]);
        assert((left + right).drop_first() =~= tail + right);
        lemma_encode_utf8_concat(tail, right);
        reveal_with_fuel(encode_utf8, 2);
    }
}

proof fn lemma_encode_utf8_split_last(chars: Seq<char>)
    requires
        chars.len() > 0,
    ensures
        encode_utf8(chars) =~= encode_utf8(
            chars.subrange(0, chars.len() as int - 1),
        ) + encode_scalar(chars.last() as u32),
{
    let prefix = chars.subrange(0, chars.len() as int - 1);
    let last = chars.last();
    assert(chars =~= prefix + seq![last]);
    lemma_encode_utf8_concat(prefix, seq![last]);
    char_is_scalar(last);
    reveal_with_fuel(encode_utf8, 2);
}

proof fn lemma_scalar_encoding_ends_in_whitespace(c: u32)
    requires
        is_scalar(c),
        is_ascii_whitespace_byte(encode_scalar(c).last()),
    ensures
        encode_scalar(c).len() == 1,
{
    reveal(encode_scalar);
    if has_width_1_encoding(c) {
    } else {
        assert(!is_ascii_whitespace_byte(last_continuation_byte(c))) by (bit_vector);
        assert(false);
    }
}

proof fn lemma_whitespace_byte_ends_whitespace_char(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_byte(encode_utf8(chars).last()),
    ensures
        is_ascii_whitespace_char(chars.last()),
        encode_scalar(chars.last() as u32).len() == 1,
{
    let prefix = chars.subrange(0, chars.len() as int - 1);
    let last = chars.last();
    char_is_scalar(last);
    lemma_encode_utf8_split_last(chars);
    assert(encode_scalar(last as u32).len() > 0) by {
        reveal(encode_scalar);
    }
    assert(encode_utf8(chars).last() == encode_scalar(last as u32).last());
    lemma_scalar_encoding_ends_in_whitespace(last as u32);
    let singleton = seq![last];
    assert(encode_utf8(singleton) =~= encode_scalar(last as u32)) by {
        reveal_with_fuel(encode_utf8, 2);
    }
    assert(is_ascii_whitespace_byte(encode_utf8(singleton)[0]));
    lemma_whitespace_byte_starts_whitespace_char(singleton);
    assert(singleton[0] == last);
}

proof fn lemma_whitespace_char_ends_whitespace_byte(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_char(chars.last()),
    ensures
        is_ascii_whitespace_byte(encode_utf8(chars).last()),
{
    let last = chars.last();
    char_is_scalar(last);
    lemma_ascii_whitespace_scalar_bit_facts(last as u32);
    lemma_encode_utf8_split_last(chars);
    reveal(encode_scalar);
    assert(encode_scalar(last as u32).len() == 1);
    assert(encode_utf8(chars).last() == encode_scalar(last as u32).last());
}

proof fn lemma_ascii_whitespace_byte_suffix_is_char_suffix(
    chars: Seq<char>,
    end: int,
) -> (k: int)
    requires
        0 <= end <= encode_utf8(chars).len(),
        forall|i: int|
            end <= i < encode_utf8(chars).len()
                ==> is_ascii_whitespace_byte(encode_utf8(chars)[i]),
    ensures
        0 <= k <= chars.len(),
        encode_utf8(chars).subrange(0, end) =~= encode_utf8(
            chars.subrange(0, k),
        ),
        forall|i: int|
            k <= i < chars.len() ==> is_ascii_whitespace_char(chars[i]),
    decreases chars.len(),
{
    let bytes = encode_utf8(chars);
    if chars.len() == 0 {
        assert(bytes.len() == 0) by {
            reveal(encode_utf8);
        }
        assert(end == 0);
        assert(chars.subrange(0, 0) =~= chars);
        0
    } else if end == bytes.len() {
        assert(chars.subrange(0, chars.len() as int) =~= chars);
        chars.len() as int
    } else {
        let n = chars.len() as int;
        let prefix = chars.subrange(0, n - 1);
        let prefix_bytes = encode_utf8(prefix);
        assert(end <= bytes.len() - 1);
        assert(is_ascii_whitespace_byte(bytes[bytes.len() - 1]));
        lemma_whitespace_byte_ends_whitespace_char(chars);
        lemma_encode_utf8_split_last(chars);
        assert(encode_scalar(chars.last() as u32).len() == 1);
        assert(bytes.len() == prefix_bytes.len() + 1);
        assert(end <= prefix_bytes.len());
        assert forall|i: int|
            end <= i < prefix_bytes.len()
                implies is_ascii_whitespace_byte(prefix_bytes[i]) by {
            assert(prefix_bytes[i] == bytes[i]);
        }
        let k = lemma_ascii_whitespace_byte_suffix_is_char_suffix(prefix, end);
        assert(bytes.subrange(0, end) =~= prefix_bytes.subrange(0, end));
        assert(prefix.subrange(0, k) =~= chars.subrange(0, k));
        assert(bytes.subrange(0, end) =~= encode_utf8(chars.subrange(0, k)));
        assert forall|i: int|
            k <= i < chars.len() implies is_ascii_whitespace_char(chars[i]) by {
            if i < n - 1 {
                assert(prefix[i] == chars[i]);
            } else {
                assert(i == n - 1);
                assert(chars[i] == chars.last());
            }
        }
        k
    }
}

pub const fn source_str_trim_ascii_end(s: &str) -> (res: &str)
    ensures
        s@.len() >= res@.len(),
        res@ == s@.subrange(0, res@.len() as int),
        forall|i: int| i >= res@.len() as int && s@.len() > i ==> (
            s@[i] as nat == 0x09 || s@[i] as nat == 0x0a
                || s@[i] as nat == 0x0c || s@[i] as nat == 0x0d
                || s@[i] as nat == 0x20
        ),
        res@.len() > 0 ==> !(
            res@.last() as nat == 0x09 || res@.last() as nat == 0x0a
                || res@.last() as nat == 0x0c || res@.last() as nat == 0x0d
                || res@.last() as nat == 0x20
        ),
{
    let bytes = s.as_bytes();
    let trimmed = bytes.trim_ascii_end();
    let ghost end = trimmed@.len() as int;
    let ghost k: int;
    proof {
        assert forall|i: int|
            end <= i < encode_utf8(s@).len()
                implies is_ascii_whitespace_byte(encode_utf8(s@)[i]) by {
            assert(bytes@[i] == encode_utf8(s@)[i]);
        }
        k = lemma_ascii_whitespace_byte_suffix_is_char_suffix(s@, end);
        assert(trimmed@ =~= encode_utf8(s@).subrange(0, end));
        assert(trimmed@ =~= encode_utf8(s@.subrange(0, k)));
        encode_utf8_valid_utf8(s@.subrange(0, k));
        assert(valid_utf8(trimmed@));
    }
    let res = unsafe { core::str::from_utf8_unchecked(trimmed) };
    proof {
        let prefix = s@.subrange(0, k);
        encode_utf8_decode_utf8(res@);
        encode_utf8_decode_utf8(prefix);
        assert(res@ == prefix);
        assert(prefix.len() == k);
        assert(res@.len() == k);
        assert forall|i: int|
            i >= res@.len() as int && s@.len() > i implies
                is_ascii_whitespace_char_nat(s@[i]) by {
            assert(is_ascii_whitespace_char(s@[i]));
            lemma_ascii_whitespace_char_casts(s@[i]);
        }
        if res@.len() > 0 {
            assert(end > 0) by {
                if end == 0 {
                    assert(trimmed@.len() == 0);
                    assert(res.spec_bytes().len() == 0);
                    assert(encode_utf8(res@).len() == 0);
                    assert(res@.len() == 0) by {
                        if res@.len() > 0 {
                            reveal_with_fuel(encode_utf8, 2);
                            char_is_scalar(res@[0]);
                            reveal(encode_scalar);
                        }
                    }
                }
            }
            assert(!is_ascii_whitespace_byte(trimmed@.last()));
            if is_ascii_whitespace_char(res@.last()) {
                lemma_whitespace_char_ends_whitespace_byte(res@);
                assert(trimmed@ =~= encode_utf8(res@));
                assert(is_ascii_whitespace_byte(trimmed@.last()));
            }
            assert(!is_ascii_whitespace_char(res@.last()));
            lemma_ascii_whitespace_char_casts(res@.last());
        }
    }
    res
}

} // verus!

fn main() {}