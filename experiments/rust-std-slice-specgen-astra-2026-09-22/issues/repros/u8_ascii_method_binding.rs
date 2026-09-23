use vstd::prelude::*;

verus! {

pub const fn lowercase_classification(byte: &u8) -> bool {
    byte.is_ascii_lowercase()
}

pub const fn uppercase_classification(byte: &u8) -> bool {
    byte.is_ascii_uppercase()
}

pub const fn uppercase_conversion(byte: &u8) -> u8 {
    byte.to_ascii_uppercase()
}

pub const fn lowercase_conversion(byte: &u8) -> u8 {
    byte.to_ascii_lowercase()
}

pub const fn uppercase_mutation(byte: &mut u8) {
    byte.make_ascii_uppercase();
}

pub const fn lowercase_mutation(byte: &mut u8) {
    byte.make_ascii_lowercase();
}

}
