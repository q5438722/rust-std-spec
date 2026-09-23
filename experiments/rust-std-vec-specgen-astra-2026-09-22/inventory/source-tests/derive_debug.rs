// Inventory-only inspection of derive bounds, not a replacement std implementation or proof.
use std::fmt;

trait Allocator {}
struct Global;
impl Allocator for Global {}

struct Drain<'a, T: 'a, A: Allocator + 'a>(&'a (T, A));

impl<T: fmt::Debug, A: Allocator> fmt::Debug for Drain<'_, T, A> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Drain").finish()
    }
}

#[derive(Debug)]
struct Splice<'a, I: Iterator + 'a, A: Allocator + 'a = Global> {
    drain: Drain<'a, I::Item, A>,
    replace_with: I,
}
