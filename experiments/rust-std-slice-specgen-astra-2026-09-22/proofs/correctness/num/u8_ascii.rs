use vstd::prelude::*;

#[path = "../../../specs/slice/ascii_post.rs"]
mod contracts;

#[path = "u8_ascii_classify.rs"]
mod classify;

verus! {

// Rust 1.96 num/mod.rs:539.
const ASCII_CASE_MASK: u8 = 0b0010_0000;

// Rust 1.96 num/mod.rs:620-642.
pub const fn to_ascii_uppercase(byte: &u8) -> (result: u8)
    ensures
        result == contracts::uppercase_byte(*byte),
{
    proof {
        let value = *byte;
        assert(b'a' <= value <= b'z' ==> (value ^ 32u8) == (value - 32) as u8)
            by (bit_vector);
        assert(value ^ 0u8 == value) by (bit_vector);
    }
    *byte ^ ((classify::is_ascii_lowercase(byte) as u8) * ASCII_CASE_MASK)
}

// Rust 1.96 num/mod.rs:644-667.
pub const fn to_ascii_lowercase(byte: &u8) -> (result: u8)
    ensures
        result == contracts::lowercase_byte(*byte),
{
    proof {
        let value = *byte;
        assert(b'A' <= value <= b'Z' ==> (value | 32u8) == (value + 32) as u8)
            by (bit_vector);
        assert(value | 0u8 == value) by (bit_vector);
    }
    *byte | (classify::is_ascii_uppercase(byte) as u8 * ASCII_CASE_MASK)
}

// Rust 1.96 num/mod.rs:694-718.
pub const fn make_ascii_uppercase(byte: &mut u8)
    ensures
        *final(byte) == contracts::uppercase_byte(*old(byte)),
{
    *byte = to_ascii_uppercase(byte);
}

// Rust 1.96 num/mod.rs:720-744.
pub const fn make_ascii_lowercase(byte: &mut u8)
    ensures
        *final(byte) == contracts::lowercase_byte(*old(byte)),
{
    *byte = to_ascii_lowercase(byte);
}

}
