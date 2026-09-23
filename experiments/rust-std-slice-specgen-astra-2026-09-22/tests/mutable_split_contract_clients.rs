use vstd::prelude::*;
#[path = "../specs/slice/mutable_splits.rs"]
mod bindings;

verus! {

pub fn first_interleaved_writes<T>(
    slice: &mut [T],
    first_write: T,
    tail_write: T,
    last_first_write: T,
    last_tail_write: T,
)
    requires old(slice)@.len() == 2,
    ensures final(slice)@ =~= seq![last_first_write, last_tail_write],
{
    if let Some((first, tail)) = slice.split_first_mut() {
        *first = first_write;
        tail[0] = tail_write;
        *first = last_first_write;
        tail[0] = last_tail_write;
    }
}

pub fn last_interleaved_writes<T>(
    slice: &mut [T],
    last_write: T,
    init_write: T,
    last_last_write: T,
    last_init_write: T,
)
    requires old(slice)@.len() == 2,
    ensures final(slice)@ =~= seq![last_init_write, last_last_write],
{
    if let Some((last, init)) = slice.split_last_mut() {
        init[0] = init_write;
        *last = last_write;
        init[0] = last_init_write;
        *last = last_last_write;
    }
}

}
