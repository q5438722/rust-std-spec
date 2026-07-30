#![allow(dead_code, unused_imports)]

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

pub open spec fn byte_trim_bounds(bytes: Seq<u8>, start: int, end: int) -> bool {
    &&& 0 <= start <= end <= bytes.len()
    &&& (forall|i: int| 0 <= i < start ==> is_ascii_whitespace_byte(bytes[i]))
    &&& (start == bytes.len() || !is_ascii_whitespace_byte(bytes[start]))
    &&& (forall|i: int| end <= i < bytes.len() ==> is_ascii_whitespace_byte(bytes[i]))
    &&& (end == start || !is_ascii_whitespace_byte(bytes[end - 1]))
}

pub assume_specification[ <[u8]>::trim_ascii ](slice: &[u8]) -> (ret: &[u8])
    ensures
        exists|bounds: (int, int)|
            byte_trim_bounds(slice@, bounds.0, bounds.1)
            && ret@ == slice@.subrange(bounds.0, bounds.1),
;

pub assume_specification<'a>[ core::str::from_utf8_unchecked ](
    bytes: &'a [u8],
) -> (result: &'a str)
    requires
        valid_utf8(bytes@),
    ensures
        result.spec_bytes() == bytes@,
;

pub open spec fn trim_step(
    state: (Seq<char>, Seq<char>),
    c: char,
) -> (Seq<char>, Seq<char>) {
    let code = c as nat;
    if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 {
        if state.0.len() == 0 {
            state
        } else {
            (state.0, state.1.push(c))
        }
    } else {
        ((state.0 + state.1).push(c), Seq::<char>::empty())
    }
}

pub open spec fn trim_step_fn() -> spec_fn(
    (Seq<char>, Seq<char>),
    char,
) -> (Seq<char>, Seq<char>) {
    |state: (Seq<char>, Seq<char>), c: char| {
        let code = c as nat;
        if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 {
            if state.0.len() == 0 {
                state
            } else {
                (state.0, state.1.push(c))
            }
        } else {
            ((state.0 + state.1).push(c), Seq::<char>::empty())
        }
    }
}

pub open spec fn folded_trim(chars: Seq<char>) -> Seq<char> {
    (chars.fold_left(
        (Seq::<char>::empty(), Seq::<char>::empty()),
        |state: (Seq<char>, Seq<char>), c: char| {
            let code = c as nat;
            if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 {
                if state.0.len() == 0 {
                    state
                } else {
                    (state.0, state.1.push(c))
                }
            } else {
                ((state.0 + state.1).push(c), Seq::<char>::empty())
            }
        },
    )).0
}

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

proof fn lemma_encode_utf8_concat(left: Seq<char>, right: Seq<char>)
    ensures
        encode_utf8(left + right) =~= encode_utf8(left) + encode_utf8(right),
    decreases left.len(),
{
    if left.len() == 0 {
        assert(left + right =~= right);
        reveal(encode_utf8);
    } else {
        let rest = left.drop_first();
        assert((left + right)[0] == left[0]);
        assert((left + right).drop_first() =~= rest + right);
        lemma_encode_utf8_concat(rest, right);
        reveal_with_fuel(encode_utf8, 2);
    }
}

proof fn lemma_last_continuation_not_ascii_whitespace(scalar: u32)
    by (bit_vector)
    ensures
        !is_ascii_whitespace_byte(0x80u8 | (scalar & 0x3fu32) as u8),
{
}

proof fn lemma_width_one_whitespace_scalar(scalar: u32)
    by (bit_vector)
    requires
        has_width_1_encoding(scalar),
        is_ascii_whitespace_byte((scalar & 0x7fu32) as u8),
    ensures
        scalar == 0x09u32
            || scalar == 0x0au32
            || scalar == 0x0cu32
            || scalar == 0x0du32
            || scalar == 0x20u32,
{
}

proof fn lemma_encode_scalar_last_whitespace(c: char)
    requires
        is_ascii_whitespace_byte(encode_scalar(c as u32).last()),
    ensures
        is_ascii_whitespace_char(c),
        encode_scalar(c as u32) =~= seq![encode_scalar(c as u32).last()],
{
    char_is_scalar(c);
    let scalar = c as u32;
    reveal(is_scalar);
    reveal(encode_scalar);
    if has_width_1_encoding(scalar) {
        reveal(leading_byte_width_1);
        lemma_width_one_whitespace_scalar(scalar);
    } else if has_width_2_encoding(scalar) {
        reveal(last_continuation_byte);
        lemma_last_continuation_not_ascii_whitespace(scalar);
    } else if has_width_3_encoding(scalar) {
        reveal(last_continuation_byte);
        lemma_last_continuation_not_ascii_whitespace(scalar);
    } else {
        reveal(last_continuation_byte);
        lemma_last_continuation_not_ascii_whitespace(scalar);
    }
}

proof fn lemma_encode_utf8_last_whitespace(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_byte(encode_utf8(chars).last()),
    ensures
        is_ascii_whitespace_char(chars.last()),
        encode_utf8(chars).drop_last() =~= encode_utf8(chars.drop_last()),
{
    let prefix = chars.drop_last();
    let c = chars.last();
    let scalar_bytes = encode_scalar(c as u32);
    assert(chars =~= prefix + seq![c]);
    lemma_encode_utf8_concat(prefix, seq![c]);
    char_is_scalar(c);
    assert(encode_utf8(seq![c]) =~= scalar_bytes) by {
        reveal_with_fuel(encode_utf8, 2);
    }
    assert(scalar_bytes.len() > 0) by {
        reveal(encode_scalar);
        reveal(is_scalar);
    }
    assert(encode_utf8(chars).last() == scalar_bytes.last());
    lemma_encode_scalar_last_whitespace(c);
    assert(scalar_bytes.len() == 1);
    Seq::<u8>::drop_last_distributes_over_add(encode_utf8(prefix), scalar_bytes);
}

proof fn lemma_whitespace_char_ends_whitespace_byte(chars: Seq<char>)
    requires
        chars.len() > 0,
        is_ascii_whitespace_char(chars.last()),
    ensures
        is_ascii_whitespace_byte(encode_utf8(chars).last()),
{
    let prefix = chars.drop_last();
    let c = chars.last();
    char_is_scalar(c);
    lemma_ascii_whitespace_scalar_bit_facts(c as u32);
    lemma_encode_utf8_concat(prefix, seq![c]);
    assert(encode_utf8(seq![c]) =~= encode_scalar(c as u32)) by {
        reveal_with_fuel(encode_utf8, 2);
    }
    assert(encode_scalar(c as u32) =~= seq![leading_byte_width_1(c as u32)]) by {
        reveal(encode_scalar);
    }
    assert(chars =~= prefix + seq![c]);
}

proof fn lemma_ascii_whitespace_suffix_is_char_suffix(chars: Seq<char>, end: int)
    requires
        0 <= end <= encode_utf8(chars).len(),
        forall|i: int|
            end <= i < encode_utf8(chars).len()
                ==> is_ascii_whitespace_byte(encode_utf8(chars)[i]),
    ensures
        exists|char_end: int|
            0 <= char_end <= chars.len()
            && chars.len() - char_end == encode_utf8(chars).len() - end
            && (forall|i: int|
                char_end <= i < chars.len()
                    ==> is_ascii_whitespace_char(chars[i]))
            && encode_utf8(chars).subrange(0, end)
                =~= encode_utf8(chars.subrange(0, char_end)),
    decreases encode_utf8(chars).len() - end,
{
    let bytes = encode_utf8(chars);
    if end == bytes.len() {
        assert(bytes.subrange(0, end) =~= bytes);
        assert(chars.subrange(0, chars.len() as int) =~= chars);
        assert(exists|char_end: int|
            char_end == chars.len()
            && 0 <= char_end <= chars.len()
            && chars.len() - char_end == bytes.len() - end
            && (forall|i: int|
                char_end <= i < chars.len()
                    ==> is_ascii_whitespace_char(chars[i]))
            && bytes.subrange(0, end)
                =~= encode_utf8(chars.subrange(0, char_end)));
    } else {
        assert(end < bytes.len());
        assert(bytes.len() > 0);
        assert(chars.len() > 0) by {
            if chars.len() == 0 {
                reveal(encode_utf8);
            }
        }
        assert(is_ascii_whitespace_byte(bytes.last()));
        lemma_encode_utf8_last_whitespace(chars);

        let shorter = chars.drop_last();
        let shorter_bytes = encode_utf8(shorter);
        assert(shorter_bytes =~= bytes.drop_last());
        assert(shorter_bytes.len() == bytes.len() - 1);
        assert(0 <= end <= shorter_bytes.len());
        assert forall|i: int|
            end <= i < shorter_bytes.len()
                implies is_ascii_whitespace_byte(shorter_bytes[i]) by {
            assert(shorter_bytes[i] == bytes[i]);
        }

        lemma_ascii_whitespace_suffix_is_char_suffix(shorter, end);
        let char_end = choose|char_end: int|
            0 <= char_end <= shorter.len()
            && shorter.len() - char_end == shorter_bytes.len() - end
            && (forall|i: int|
                char_end <= i < shorter.len()
                    ==> is_ascii_whitespace_char(shorter[i]))
            && shorter_bytes.subrange(0, end)
                =~= encode_utf8(shorter.subrange(0, char_end));

        assert(bytes.subrange(0, end) =~= shorter_bytes.subrange(0, end));
        assert(chars.subrange(0, char_end) =~= shorter.subrange(0, char_end));
        assert forall|i: int|
            char_end <= i < chars.len()
                implies is_ascii_whitespace_char(chars[i]) by {
            if i < shorter.len() {
                assert(shorter[i] == chars[i]);
            } else {
                assert(i == chars.len() - 1);
                assert(chars[i] == chars.last());
            }
        }
        assert(chars.len() - char_end == bytes.len() - end);
        assert(exists|witness: int|
            witness == char_end
            && 0 <= witness <= chars.len()
            && chars.len() - witness == bytes.len() - end
            && (forall|i: int|
                witness <= i < chars.len()
                    ==> is_ascii_whitespace_char(chars[i]))
            && bytes.subrange(0, end)
                =~= encode_utf8(chars.subrange(0, witness)));
    }
}

pub open spec fn char_trim_bounds(chars: Seq<char>, start: int, end: int) -> bool {
    &&& 0 <= start <= end <= chars.len()
    &&& (forall|i: int|
        0 <= i < start ==> is_ascii_whitespace_char_nat(chars[i]))
    &&& (end > start ==> !is_ascii_whitespace_char_nat(chars[start]))
    &&& (forall|i: int|
        end <= i < chars.len() ==> is_ascii_whitespace_char_nat(chars[i]))
    &&& (end > start ==> !is_ascii_whitespace_char_nat(chars[end - 1]))
}

proof fn lemma_byte_trim_is_char_trim(
    chars: Seq<char>,
    trimmed: Seq<u8>,
    start: int,
    end: int,
)
    requires
        byte_trim_bounds(encode_utf8(chars), start, end),
        trimmed == encode_utf8(chars).subrange(start, end),
    ensures
        valid_utf8(trimmed),
        exists|char_end: int|
            char_trim_bounds(chars, start, char_end)
            && trimmed =~= encode_utf8(chars.subrange(start, char_end)),
{
    let bytes = encode_utf8(chars);
    lemma_ascii_whitespace_prefix_is_char_prefix(chars, start);
    let suffix_chars = chars.subrange(start, chars.len() as int);
    let suffix_bytes = encode_utf8(suffix_chars);
    assert(suffix_bytes =~= bytes.subrange(start, bytes.len() as int));

    let relative_end = end - start;
    assert(0 <= relative_end <= suffix_bytes.len());
    assert forall|i: int|
        relative_end <= i < suffix_bytes.len()
            implies is_ascii_whitespace_byte(suffix_bytes[i]) by {
        assert(0 <= i + start < bytes.len());
        assert(suffix_bytes[i] == bytes[i + start]);
    }
    lemma_ascii_whitespace_suffix_is_char_suffix(suffix_chars, relative_end);
    let relative_char_end = choose|relative_char_end: int|
        0 <= relative_char_end <= suffix_chars.len()
        && suffix_chars.len() - relative_char_end
            == suffix_bytes.len() - relative_end
        && (forall|i: int|
            relative_char_end <= i < suffix_chars.len()
                ==> is_ascii_whitespace_char(suffix_chars[i]))
        && suffix_bytes.subrange(0, relative_end)
            =~= encode_utf8(suffix_chars.subrange(0, relative_char_end));
    let char_end = start + relative_char_end;

    assert(0 <= start <= char_end <= chars.len());
    vstd::seq::lemma_seq_subrange_composition(
        bytes,
        start,
        bytes.len() as int,
        0,
        relative_end,
    );
    vstd::seq::lemma_seq_subrange_composition(
        chars,
        start,
        chars.len() as int,
        0,
        relative_char_end,
    );
    assert(trimmed =~= encode_utf8(chars.subrange(start, char_end)));
    encode_utf8_valid_utf8(chars.subrange(start, char_end));

    assert forall|i: int|
        0 <= i < start implies is_ascii_whitespace_char_nat(chars[i]) by {
        assert(is_ascii_whitespace_char(chars[i]));
        lemma_ascii_whitespace_char_casts(chars[i]);
    }
    assert forall|i: int|
        char_end <= i < chars.len()
            implies is_ascii_whitespace_char_nat(chars[i]) by {
        let j = i - start;
        assert(relative_char_end <= j < suffix_chars.len());
        assert(suffix_chars[j] == chars[i]);
        assert(is_ascii_whitespace_char(chars[i]));
        lemma_ascii_whitespace_char_casts(chars[i]);
    }

    if char_end > start {
        assert(relative_char_end > 0);
        assert(relative_end > 0) by {
            if relative_end == 0 {
                assert(suffix_bytes.subrange(0, relative_end).len() == 0);
                assert(encode_utf8(
                    suffix_chars.subrange(0, relative_char_end)
                ).len() == 0);
                assert(suffix_chars.subrange(0, relative_char_end).len() > 0);
                reveal(encode_utf8);
            }
        }
        assert(start < bytes.len());
        assert(!is_ascii_whitespace_byte(bytes[start]));
        lemma_nonwhitespace_byte_starts_nonwhitespace_char(chars, start);
        lemma_ascii_whitespace_char_casts(chars[start]);
        assert(!is_ascii_whitespace_char_nat(chars[start]));

        let middle = chars.subrange(start, char_end);
        assert(middle.len() > 0);
        assert(encode_utf8(middle).len() > 0);
        assert(encode_utf8(middle).last() == bytes[end - 1]) by {
            assert(trimmed.len() == end - start);
            assert(trimmed.last() == bytes[end - 1]);
        }
        assert(!is_ascii_whitespace_byte(bytes[end - 1]));
        if is_ascii_whitespace_char(middle.last()) {
            lemma_whitespace_char_ends_whitespace_byte(middle);
        }
        assert(!is_ascii_whitespace_char(middle.last()));
        assert(middle.last() == chars[char_end - 1]);
        lemma_ascii_whitespace_char_casts(chars[char_end - 1]);
        assert(!is_ascii_whitespace_char_nat(chars[char_end - 1]));
    }

    assert(char_trim_bounds(chars, start, char_end));
    assert(exists|witness: int|
        witness == char_end
        && char_trim_bounds(chars, start, witness)
        && trimmed =~= encode_utf8(chars.subrange(start, witness)));
}

proof fn lemma_fold_all_whitespace(chars: Seq<char>)
    requires
        forall|i: int|
            0 <= i < chars.len() ==> is_ascii_whitespace_char_nat(chars[i]),
    ensures
        chars.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            trim_step_fn(),
        ) == (Seq::<char>::empty(), Seq::<char>::empty()),
    decreases chars.len(),
{
    reveal_with_fuel(Seq::fold_left, 2);
    if chars.len() > 0 {
        let prefix = chars.drop_last();
        assert forall|i: int|
            0 <= i < prefix.len()
                implies is_ascii_whitespace_char_nat(prefix[i]) by {
            assert(prefix[i] == chars[i]);
        }
        lemma_fold_all_whitespace(prefix);
        assert(is_ascii_whitespace_char_nat(chars.last()));
        reveal(trim_step_fn);
    }
}

proof fn lemma_fold_started(chars: Seq<char>)
    requires
        chars.len() > 0,
        !is_ascii_whitespace_char_nat(chars[0]),
    ensures
        ({
            let state = chars.fold_left(
                (Seq::<char>::empty(), Seq::<char>::empty()),
                trim_step_fn(),
            );
            &&& state.0 + state.1 =~= chars
            &&& state.0.len() > 0
            &&& (!is_ascii_whitespace_char_nat(chars.last())
                ==> state.1.len() == 0)
        }),
    decreases chars.len(),
{
    reveal_with_fuel(Seq::fold_left, 2);
    if chars.len() == 1 {
        assert(chars.drop_last().len() == 0);
        assert(chars =~= seq![chars.last()]);
        reveal(trim_step_fn);
    } else {
        let prefix = chars.drop_last();
        assert(prefix.len() > 0);
        assert(prefix[0] == chars[0]);
        lemma_fold_started(prefix);
        let previous = prefix.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            trim_step_fn(),
        );
        let current = chars.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            trim_step_fn(),
        );
        assert(previous.0 + previous.1 =~= prefix);
        if is_ascii_whitespace_char_nat(chars.last()) {
            assert(current == (previous.0, previous.1.push(chars.last()))) by {
                reveal(trim_step_fn);
            }
            assert(previous.0 + previous.1.push(chars.last())
                =~= (previous.0 + previous.1).push(chars.last()));
            assert(chars =~= prefix.push(chars.last()));
        } else {
            assert(current == (
                (previous.0 + previous.1).push(chars.last()),
                Seq::<char>::empty(),
            )) by {
                reveal(trim_step_fn);
            }
            assert(chars =~= prefix.push(chars.last()));
        }
    }
}

proof fn lemma_fold_whitespace_after(base: Seq<char>, tail: Seq<char>)
    requires
        base.len() > 0,
        forall|i: int|
            0 <= i < tail.len() ==> is_ascii_whitespace_char_nat(tail[i]),
    ensures
        tail.fold_left(
            (base, Seq::<char>::empty()),
            trim_step_fn(),
        ) == (base, tail),
    decreases tail.len(),
{
    reveal_with_fuel(Seq::fold_left, 2);
    if tail.len() > 0 {
        let prefix = tail.drop_last();
        assert forall|i: int|
            0 <= i < prefix.len()
                implies is_ascii_whitespace_char_nat(prefix[i]) by {
            assert(prefix[i] == tail[i]);
        }
        lemma_fold_whitespace_after(base, prefix);
        assert(is_ascii_whitespace_char_nat(tail.last()));
        assert(tail =~= prefix.push(tail.last()));
        reveal(trim_step_fn);
    }
}

proof fn lemma_fold_is_trimmed_subrange(chars: Seq<char>, start: int, end: int)
    requires
        char_trim_bounds(chars, start, end),
    ensures
        folded_trim(chars) =~= chars.subrange(start, end),
{
    let initial = (Seq::<char>::empty(), Seq::<char>::empty());
    let prefix = chars.subrange(0, start);
    let rest = chars.subrange(start, chars.len() as int);
    let middle = chars.subrange(start, end);
    let tail = chars.subrange(end, chars.len() as int);

    assert forall|i: int|
        0 <= i < prefix.len()
            implies is_ascii_whitespace_char_nat(prefix[i]) by {
        assert(prefix[i] == chars[i]);
    }
    lemma_fold_all_whitespace(prefix);
    chars.lemma_fold_left_split(initial, trim_step_fn(), start);

    assert(rest.len() == chars.len() - start);
    assert(0 <= end - start <= rest.len());
    vstd::seq::lemma_seq_subrange_composition(
        chars,
        start,
        chars.len() as int,
        0,
        end - start,
    );
    vstd::seq::lemma_seq_subrange_composition(
        chars,
        start,
        chars.len() as int,
        end - start,
        rest.len() as int,
    );
    assert(rest.subrange(0, end - start) =~= middle);
    assert(rest.subrange(end - start, rest.len() as int) =~= tail);
    rest.lemma_fold_left_split(initial, trim_step_fn(), end - start);

    assert forall|i: int|
        0 <= i < tail.len()
            implies is_ascii_whitespace_char_nat(tail[i]) by {
        assert(tail[i] == chars[i + end]);
    }

    if end == start {
        assert(middle.len() == 0);
        assert(rest =~= tail);
        lemma_fold_all_whitespace(tail);
    } else {
        assert(middle.len() > 0);
        assert(middle[0] == chars[start]);
        assert(middle.last() == chars[end - 1]);
        assert(!is_ascii_whitespace_char_nat(middle[0]));
        assert(!is_ascii_whitespace_char_nat(middle.last()));
        lemma_fold_started(middle);
        let middle_state = middle.fold_left(initial, trim_step_fn());
        assert(middle_state.0 + middle_state.1 =~= middle);
        assert(middle_state.1.len() == 0);
        assert(middle_state.1 =~= Seq::<char>::empty());
        assert(middle_state.0 =~= middle);
        lemma_fold_whitespace_after(middle, tail);
        assert(tail.fold_left(middle_state, trim_step_fn()) == (middle, tail));
    }
    reveal(folded_trim);
    reveal(trim_step_fn);
}

pub const fn source_core_str_trim_ascii(s: &str) -> (ret: &str)
    ensures
        ret@ == (s@.fold_left((Seq::<char>::empty(), Seq::<char>::empty()), |state: (Seq<char>, Seq<char>), c: char| { let code = c as nat; if code == 0x09 || code == 0x0a || code == 0x0c || code == 0x0d || code == 0x20 { if state.0.len() == 0 { state } else { (state.0, state.1.push(c)) } } else { ((state.0 + state.1).push(c), Seq::<char>::empty()) } })).0,
{
    let bytes = s.as_bytes();
    let trimmed = bytes.trim_ascii();
    let ghost bounds = choose|bounds: (int, int)|
        byte_trim_bounds(bytes@, bounds.0, bounds.1)
        && trimmed@ == bytes@.subrange(bounds.0, bounds.1);
    let ghost start = bounds.0;
    let ghost end = bounds.1;
    proof {
        assert(bytes@ == encode_utf8(s@));
        lemma_byte_trim_is_char_trim(s@, trimmed@, start, end);
    }
    let ghost char_end = choose|char_end: int|
        char_trim_bounds(s@, start, char_end)
        && trimmed@ =~= encode_utf8(s@.subrange(start, char_end));
    let ret = unsafe { core::str::from_utf8_unchecked(trimmed) };
    proof {
        encode_utf8_decode_utf8(ret@);
        encode_utf8_decode_utf8(s@.subrange(start, char_end));
        assert(ret@ == s@.subrange(start, char_end));
        lemma_fold_is_trimmed_subrange(s@, start, char_end);
        assert(folded_trim(s@) == ret@);
        reveal(folded_trim);
    }
    ret
}

} // verus!

fn main() {}