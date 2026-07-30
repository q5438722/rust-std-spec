#![allow(dead_code)]

use core::ffi::{CStr, FromBytesUntilNulError};
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

verus! {

pub uninterp spec fn zero_valid<T>() -> bool;

pub axiom fn from_bytes_until_nul_error_zero_valid()
    ensures
        zero_valid::<FromBytesUntilNulError>(),
;

pub axiom fn first_nul_index_characterization(bytes: Seq<u8>)
    requires
        contains_nul(bytes),
    ensures
        0 <= first_nul_index(bytes) < bytes.len(),
        bytes[first_nul_index(bytes)] == 0,
        forall|j: int| 0 <= j < first_nul_index(bytes) ==> bytes[j] != 0,
;

#[verifier::external_fn_specification]
pub unsafe fn ex_zeroed<T>() -> T
    requires
        zero_valid::<T>(),
{
    core::mem::zeroed::<T>()
}

fn source_memchr(needle: u8, text: &[u8]) -> (result: Option<usize>)
    ensures
        result matches Some(pos) ==> (
            pos < text.len()
            && text@[pos as int] == needle
            && forall|j: int| 0 <= j < pos ==> text@[j] != needle
        ),
        result is None ==> forall|j: int| 0 <= j < text@.len() ==> text@[j] != needle,
{
    let mut i: usize = 0;
    while i < text.len()
        invariant
            i <= text.len(),
            forall|j: int| 0 <= j < i ==> text@[j] != needle,
        decreases text.len() - i,
    {
        if text[i] == needle {
            return Some(i);
        }
        i += 1;
    }
    None
}

proof fn lemma_first_nul_index(bytes: Seq<u8>, pos: int)
    requires
        0 <= pos < bytes.len(),
        bytes[pos] == 0,
        forall|j: int| 0 <= j < pos ==> bytes[j] != 0,
    ensures
        contains_nul(bytes),
        first_nul_index(bytes) == pos,
{
    assert(contains_nul(bytes)) by {
        assert(exists|i: int| 0 <= i < bytes.len() && bytes[i] == 0);
    }
    first_nul_index_characterization(bytes);
    let first = first_nul_index(bytes);
    assert(0 <= first < bytes.len());
    assert(bytes[first] == 0);
    assert(forall|j: int| 0 <= j < first ==> bytes[j] != 0);
    if first < pos {
        assert(bytes[first] != 0);
        assert(false);
    }
    if pos < first {
        assert(bytes[pos] != 0);
        assert(false);
    }
}

proof fn lemma_nul_prefix_valid(bytes: Seq<u8>, pos: int)
    requires
        0 <= pos < bytes.len(),
        bytes[pos] == 0,
        forall|j: int| 0 <= j < pos ==> bytes[j] != 0,
    ensures
        c_string_bytes_with_nul_valid(bytes.subrange(0, pos + 1)),
        bytes.subrange(0, pos + 1).drop_last() == bytes.subrange(0, pos),
{
    let prefix = bytes.subrange(0, pos + 1);
    assert(prefix.len() == pos + 1);
    assert(prefix.last() == bytes[pos]);
    assert_seqs_equal!(prefix.drop_last() == bytes.subrange(0, pos));
    assert(c_string_bytes_valid(prefix.drop_last())) by {
        assert forall|i: int| 0 <= i < prefix.drop_last().len()
            implies #[trigger] prefix.drop_last()[i] != 0 by {
            assert(prefix.drop_last()[i] == bytes[i]);
        }
    }
}

unsafe fn source_from_bytes_with_nul_unchecked<'a>(
    bytes: &'a [u8],
) -> (result: &'a CStr)
    requires
        c_string_bytes_with_nul_valid(bytes@),
    ensures
        result@ == bytes@.drop_last(),
{
    let parsed = CStr::from_bytes_with_nul(bytes);
    proof {
        assert(parsed is Ok);
    }
    parsed.unwrap()
}

fn source_cstr_from_bytes_until_nul<'a>(
    bytes: &'a [u8],
) -> (result: Result<&'a CStr, FromBytesUntilNulError>)
    ensures
        contains_nul(bytes@) ==> (result matches Ok(value) && value@ == bytes@.subrange(
            0,
            first_nul_index(bytes@),
        )),
        !contains_nul(bytes@) ==> result is Err,
{
    let nul_pos = source_memchr(0, bytes);
    match nul_pos {
        Some(nul_pos) => {
            proof {
                lemma_first_nul_index(bytes@, nul_pos as int);
                lemma_nul_prefix_valid(bytes@, nul_pos as int);
            }
            let subslice = &bytes[0..nul_pos + 1];
            Ok(unsafe { source_from_bytes_with_nul_unchecked(subslice) })
        }
        None => {
            proof {
                from_bytes_until_nul_error_zero_valid();
            }
            Err(unsafe { core::mem::zeroed() })
        }
    }
}

} // verus!

fn main() {}