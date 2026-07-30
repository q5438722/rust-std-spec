#![allow(dead_code)]

use core::slice::from_raw_parts;
use core::str::from_utf8_unchecked;
use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::{is_char_boundary, valid_utf8};

verus! {

broadcast use vstd::utf8::encode_utf8_valid_utf8;

pub uninterp spec fn raw_slice_view<T>(ptr: *const T, len: usize) -> Seq<T>;
pub uninterp spec fn raw_slice_valid<T>(ptr: *const T, len: usize) -> bool;
pub uninterp spec fn ptr_add_valid<T>(ptr: *const T, count: usize) -> bool;
pub uninterp spec fn spec_ptr_add<T>(ptr: *const T, count: usize) -> *const T;

pub assume_specification[ str::as_ptr ](
    s: &str,
) -> (ptr: *const u8)
    ensures
        s.spec_bytes().len() <= usize::MAX,
        forall |count: usize| count as int <= s.spec_bytes().len() ==> (
            raw_slice_valid(ptr, count)
                && raw_slice_view(ptr, count)
                    == s.spec_bytes().subrange(0, count as int)
        ),
        forall |start: usize|
            start as int <= s.spec_bytes().len() ==> ptr_add_valid(ptr, start),
        forall |start: usize, count: usize|
            start as int + count as int <= s.spec_bytes().len() ==> (
                raw_slice_valid(spec_ptr_add(ptr, start), count)
                    && raw_slice_view(spec_ptr_add(ptr, start), count)
                        == s.spec_bytes().subrange(
                            start as int,
                            start as int + count as int,
                        )
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

pub assume_specification<'a>[ core::str::from_utf8_unchecked ](
    bytes: &'a [u8],
) -> (result: &'a str)
    requires valid_utf8(bytes@),
    ensures result.spec_bytes() == bytes@,
;

proof fn char_boundary_in_bounds(bytes: Seq<u8>, index: int)
    requires
        valid_utf8(bytes),
        is_char_boundary(bytes, index),
    ensures 0 <= index <= bytes.len(),
{
    reveal_with_fuel(is_char_boundary, 2);
    assert(index == 0 || !(index < 0 || bytes.len() < index));
    assert(0 <= index <= bytes.len());
}

pub const fn source_core_str_split_at_checked(
    s: &str,
    mid: usize,
) -> (res: core::option::Option<(&str, &str)>)
    ensures
        res.is_some() <==> is_char_boundary(s.spec_bytes(), mid as int),
        res.is_some() ==> (
            res.unwrap().0.spec_bytes() =~= s.spec_bytes().subrange(0, mid as int)
            && res.unwrap().1.spec_bytes() =~= s.spec_bytes().subrange(
                mid as int,
                s.spec_bytes().len() as int,
            )
        ),
{
    if s.is_char_boundary(mid) {
        proof {
            vstd::utf8::encode_utf8_valid_utf8(s@);
            assert(valid_utf8(s.spec_bytes()));
            char_boundary_in_bounds(s.spec_bytes(), mid as int);
            assert(mid as int <= s.spec_bytes().len());
            vstd::utf8::valid_utf8_split(s.spec_bytes(), mid as int);
        }

        // Mechanically inline Rust 1.96's private `str::split_at_unchecked`.
        let len = s.len();
        let ptr = s.as_ptr();
        proof {
            assert(len == s.spec_bytes().len() as usize);
            assert(s.spec_bytes().len() <= usize::MAX);
            assert(len as int == s.spec_bytes().len());
            assert(mid <= len);
            assert(raw_slice_valid(ptr, mid));
            assert(
                ((len as int - mid as int) as usize) as int
                    == len as int - mid as int
            );
            assert(
                mid as int + ((len as int - mid as int) as usize) as int
                    <= s.spec_bytes().len()
            );
            assert(
                ptr_add_valid(ptr, mid)
                    && raw_slice_valid(
                        spec_ptr_add(ptr, mid),
                        (len as int - mid as int) as usize,
                    )
            );
        }
        Some(unsafe {
            (
                from_utf8_unchecked(from_raw_parts(ptr, mid)),
                from_utf8_unchecked(from_raw_parts(ptr.add(mid), len - mid)),
            )
        })
    } else {
        None
    }
}

} // verus!

fn main() {}