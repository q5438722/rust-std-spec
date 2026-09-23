use vstd::prelude::*;

verus! {

// Rust 1.96 num/mod.rs:781-814; only the receiver name is lifted.
pub const fn is_ascii_uppercase(byte: &u8) -> (result: bool)
    ensures
        result == (b'A' <= *byte <= b'Z'),
{
    matches!(*byte, b'A'..=b'Z')
}

// Rust 1.96 num/mod.rs:816-848; only the receiver name is lifted.
pub const fn is_ascii_lowercase(byte: &u8) -> (result: bool)
    ensures
        result == (b'a' <= *byte <= b'z'),
{
    matches!(*byte, b'a'..=b'z')
}

}
