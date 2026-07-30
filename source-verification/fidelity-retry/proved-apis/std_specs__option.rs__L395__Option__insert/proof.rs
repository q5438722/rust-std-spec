#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub assume_specification<T>[ Option::<T>::unwrap_unchecked ](
    option: Option<T>,
) -> (res: T)
    requires
        option is Some,
    ensures
        res == option->0,
    no_unwind
;

fn source_option_insert<T>(
    option: &mut Option<T>,
    value: T,
) -> (res: &mut T)
    ensures
        *res == value,
        *final(option) == Some(*final(res)),
{
    *option = Some(value);

    // SAFETY: the code above just filled the option
    unsafe { option.as_mut().unwrap_unchecked() }
}

} // verus!

fn main() {}