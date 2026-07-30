#![allow(dead_code)]
#![allow(unused_imports)]

use core::panic::Location;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;
use vstd::std_specs::location::*;
use vstd::string::StringSliceAdditionalSpecFns;
use vstd::utf8::valid_utf8;
use vstd::utf8::{encode_utf8_decode_utf8, encode_utf8_valid_utf8};

verus! {

pub assume_specification<'a>[ core::str::from_utf8_unchecked ](
    bytes: &'a [u8],
) -> (result: &'a str)
    requires
        valid_utf8(bytes@),
    ensures
        result.spec_bytes() == bytes@,
;

fn source_location_file<'a>(location: &Location<'a>) -> (result: &'a str)
    ensures
        result@ == location@.file,
{
    // This exposes the same filename bytes as the private `NonNull<str>` field.
    let filename = location.file_as_c_str();
    let bytes = filename.to_bytes();
    proof {
        encode_utf8_valid_utf8(location@.file);
    }
    let result = unsafe { core::str::from_utf8_unchecked(bytes) };
    proof {
        encode_utf8_decode_utf8(result@);
        encode_utf8_decode_utf8(location@.file);
    }
    result
}

} // verus!

fn main() {}