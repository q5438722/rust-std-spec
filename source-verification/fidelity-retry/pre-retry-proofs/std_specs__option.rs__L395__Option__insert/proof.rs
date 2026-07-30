#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_insert<T>(
    option: &mut Option<T>,
    value: T,
) -> (res: &mut T)
    ensures
        *res == value,
        *final(option) == Some(*final(res)),
{
    *option = Some(value);

    // Expand the source's unsupported `as_mut().unwrap_unchecked()` chain.
    let option_ref = match *option {
        Some(ref mut value_ref) => Some(value_ref),
        None => None,
    };
    match option_ref {
        Some(value_ref) => value_ref,
        None => {
            proof {
                assert(false);
            }
            vstd::pervasive::unreached()
        },
    }
}

} // verus!

fn main() {}