use std::alloc::Allocator;
use std::ops::Index;
use std::slice::SliceIndex;
use vstd::prelude::*;
use vstd::std_specs::core::IndexSpec;

verus! {

#[inline]
#[track_caller]
pub fn index_source<T, I: SliceIndex<[T]>, A: Allocator>(
    vec: &Vec<T, A>,
    index: I,
) -> (r: &<Vec<T, A> as Index<I>>::Output)
    requires
        vec.index_req(&index),
    ensures
        exists|s: &[T]| #[trigger] s@ == vec@
            && call_ensures(<I as SliceIndex<[T]>>::index, (index, s), r),
{
    Index::index(&**vec, index)
}

}
