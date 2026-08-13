// Excerpt from Rust 1.96 `library/core/src/num/mod.rs`.
// Used only as source provenance for the `byte_make_ascii_uppercase` boundary in
// `proof_harnesses/064_core_slice_make_ascii_uppercase/harness.rs`.

/// If the bit selected by this mask is set, ascii is lower case.
const ASCII_CASE_MASK: u8 = 0b0010_0000;

impl u8 {
    #[must_use = "to uppercase the value in-place, use `make_ascii_uppercase()`"]
    #[stable(feature = "ascii_methods_on_intrinsics", since = "1.23.0")]
    #[rustc_const_stable(feature = "const_ascii_methods_on_intrinsics", since = "1.52.0")]
    #[inline]
    pub const fn to_ascii_uppercase(&self) -> u8 {
        // Toggle the 6th bit if this is a lowercase letter
        *self ^ ((self.is_ascii_lowercase() as u8) * ASCII_CASE_MASK)
    }

    #[stable(feature = "ascii_methods_on_intrinsics", since = "1.23.0")]
    #[rustc_const_stable(feature = "const_make_ascii", since = "1.84.0")]
    #[inline]
    pub const fn make_ascii_uppercase(&mut self) {
        *self = self.to_ascii_uppercase();
    }

    #[must_use]
    #[stable(feature = "ascii_ctype_on_intrinsics", since = "1.24.0")]
    #[rustc_const_stable(feature = "const_ascii_ctype_on_intrinsics", since = "1.47.0")]
    #[inline]
    pub const fn is_ascii_lowercase(&self) -> bool {
        matches!(*self, b'a'..=b'z')
    }
}
