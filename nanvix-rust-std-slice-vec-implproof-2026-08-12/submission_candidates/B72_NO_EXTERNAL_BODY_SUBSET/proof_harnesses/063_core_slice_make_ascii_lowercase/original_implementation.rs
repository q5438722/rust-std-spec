// Original Rust 1.96 implementation before primitive-helper dispatch lowering.
// Source: core/src/slice/ascii.rs:195-203
pub const fn make_ascii_lowercase(&mut self) {
    // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.
    let mut i = 0;
    while i < self.len() {
        let byte = &mut self[i];
        byte.make_ascii_lowercase();
        i += 1;
    }
}
