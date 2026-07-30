#![allow(dead_code)]

use core::ffi::{CStr, FromBytesWithNulError};
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

fn make_interior_nul_error(position: usize) -> FromBytesWithNulError {
    FromBytesWithNulError::InteriorNul { position }
}

fn make_not_nul_terminated_error() -> FromBytesWithNulError {
    FromBytesWithNulError::NotNulTerminated
}

verus! {

pub assume_specification[ make_interior_nul_error ](
    position: usize,
) -> (result: FromBytesWithNulError);

pub assume_specification[ make_not_nul_terminated_error ](
) -> (result: FromBytesWithNulError);

pub assume_specification[ CStr::from_bytes_with_nul_unchecked ](
    bytes: &[u8],
) -> (result: &CStr)
    requires
        c_string_bytes_with_nul_valid(bytes@),
    ensures
        result@ == bytes@.drop_last(),
;

unsafe fn cstr_from_valid_bytes<'a>(bytes: &'a [u8]) -> (result: &'a CStr)
    requires
        c_string_bytes_with_nul_valid(bytes@),
    ensures
        result@ == bytes@.drop_last(),
{
    CStr::from_bytes_with_nul_unchecked(bytes)
}

fn source_memchr(x: u8, text: &[u8]) -> (result: Option<usize>)
    ensures
        result matches Some(i) ==> (
            i < text@.len()
            && text@[i as int] == x
            && forall|j: int| 0 <= j < i ==> #[trigger] text@[j] != x
        ),
        result is None ==> forall|j: int|
            0 <= j < text@.len() ==> #[trigger] text@[j] != x,
{
    let mut i = 0;
    while i < text.len()
        invariant
            i <= text@.len(),
            forall|j: int| 0 <= j < i ==> #[trigger] text@[j] != x,
        decreases text@.len() - i,
    {
        if text[i] == x {
            return Some(i);
        }
        i += 1;
    }
    None
}

fn source_cstr_parse_bytes(
    bytes: &[u8],
) -> (result: Result<&CStr, FromBytesWithNulError>)
    ensures
        c_string_bytes_with_nul_valid(bytes@) ==> (result matches Ok(value) && value@
            == bytes@.drop_last()),
        !c_string_bytes_with_nul_valid(bytes@) ==> result is Err,
{
    let nul_pos = source_memchr(0, bytes);
    proof {
        vstd::slice::axiom_spec_len(bytes);
        if let Some(position) = nul_pos {
            assert(position < bytes@.len());
            assert(position < usize::MAX);
        }
    }
    match nul_pos {
        Some(nul_pos) if nul_pos + 1 == bytes.len() => {
            proof {
                assert(nul_pos as int == bytes@.len() - 1);
                assert(bytes@.len() > 0);
                assert(bytes@.last() == 0);
                assert forall|j: int| 0 <= j < bytes@.drop_last().len() implies
                    #[trigger] bytes@.drop_last()[j] != 0 by {
                    assert(bytes@.drop_last()[j] == bytes@[j]);
                }
                assert(c_string_bytes_valid(bytes@.drop_last()));
                assert(c_string_bytes_with_nul_valid(bytes@));
            }
            Ok(unsafe { cstr_from_valid_bytes(bytes) })
        }
        Some(position) => {
            proof {
                if c_string_bytes_with_nul_valid(bytes@) {
                    assert(bytes@.len() > 0);
                    assert(position < bytes@.len());
                    assert(position + 1 != bytes@.len());
                    assert((position as int) < bytes@.drop_last().len());
                    assert(bytes@.drop_last()[position as int] == bytes@[position as int]);
                    assert(bytes@.drop_last()[position as int] != 0);
                    assert(false);
                }
            }
            Err(make_interior_nul_error(position))
        }
        None => {
            proof {
                if c_string_bytes_with_nul_valid(bytes@) {
                    assert(bytes@.len() > 0);
                    let last = bytes@.len() - 1;
                    assert(bytes@[last] == 0);
                    assert(false);
                }
            }
            Err(make_not_nul_terminated_error())
        }
    }
}

} // verus!

fn main() {}