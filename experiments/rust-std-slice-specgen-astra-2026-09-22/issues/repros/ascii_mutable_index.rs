use vstd::prelude::*;

verus! {

// Isolates the original indexed reborrow and the scalar assignment operation.
pub const fn indexed_write(slice: &mut [u8], i: usize, value: u8)
    requires
        i < old(slice)@.len(),
    ensures
        final(slice)@ == old(slice)@.update(i as int, value),
{
    let byte = &mut slice[i];
    *byte = value;
}

}
