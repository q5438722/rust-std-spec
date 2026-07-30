#![feature(core_intrinsics)]
#![feature(fmt_arguments_from_str)]
#![feature(panic_internals)]
#![feature(ub_checks)]
#![allow(dead_code)]
#![allow(internal_features)]

use core::assert_unsafe_precondition;
use core::intrinsics::unchecked_sub;
use core::slice::from_raw_parts;
use vstd::prelude::*;

verus! {

pub uninterp spec fn raw_slice_view<T>(ptr: *const T, len: usize) -> Seq<T>;
pub uninterp spec fn raw_slice_valid<T>(ptr: *const T, len: usize) -> bool;
pub uninterp spec fn ptr_add_valid<T>(ptr: *const T, count: usize) -> bool;
pub uninterp spec fn spec_ptr_add<T>(ptr: *const T, count: usize) -> *const T;

pub assume_specification<T>[ <[T]>::as_ptr ](
    slice: &[T],
) -> (ptr: *const T)
    ensures
        forall |count: usize| count as int <= slice@.len() ==> (
            raw_slice_valid(ptr, count)
                && raw_slice_view(ptr, count) == slice@.subrange(0, count as int)
        ),
        forall |start: usize| start as int <= slice@.len() ==>
            #[trigger] ptr_add_valid(ptr, start),
        forall |start: usize, count: usize|
            start as int + count as int <= slice@.len() ==> (
                raw_slice_valid(spec_ptr_add(ptr, start), count)
                    && raw_slice_view(spec_ptr_add(ptr, start), count)
                        == slice@.subrange(start as int, start as int + count as int)
            ),
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ <*const T>::add ](
    ptr: *const T,
    count: usize,
) -> (result: *const T)
    requires ptr_add_valid(ptr, count),
    ensures result == spec_ptr_add(ptr, count),
    opens_invariants none
    no_unwind
;

pub assume_specification<'a, T>[ core::slice::from_raw_parts::<T> ](
    data: *const T,
    len: usize,
) -> (slice: &'a [T])
    requires raw_slice_valid(data, len),
    ensures slice@ == raw_slice_view(data, len),
    opens_invariants none
    no_unwind
;

pub uninterp spec fn compiler_unchecked_sub<T>(lhs: T, rhs: T) -> T;

pub assume_specification<T: Copy>[
    core::intrinsics::unchecked_sub::<T>
](
    lhs: T,
    rhs: T,
) -> (result: T)
    ensures result == compiler_unchecked_sub(lhs, rhs),
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_compiler_unchecked_sub_usize(lhs: usize, rhs: usize)
    requires rhs <= lhs,
    ensures compiler_unchecked_sub(lhs, rhs) == lhs - rhs,
;

pub const unsafe fn source_core_slice_split_at_unchecked<T>(
    slice: &[T],
    mid: usize,
) -> (ret: (&[T], &[T]))
    requires mid <= slice.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    let len = slice.len();
    let ptr = slice.as_ptr();

    #[cfg(not(verus_keep_ghost))]
    assert_unsafe_precondition!(
        check_library_ub,
        "slice::split_at_unchecked requires the index to be within the slice",
        (mid: usize = mid, len: usize = len) => mid <= len,
    );

    proof {
        axiom_compiler_unchecked_sub_usize(len, mid);
        assert(mid as int + (len - mid) as int <= slice@.len());
        assert(ptr_add_valid(ptr, mid));
    }

    unsafe { (from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))) }
}

} // verus!

fn main() {}