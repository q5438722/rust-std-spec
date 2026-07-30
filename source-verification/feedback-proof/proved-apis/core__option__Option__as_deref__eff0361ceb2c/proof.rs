#![allow(dead_code)]

use core::ops::Deref;
use core::option::Option;
use vstd::prelude::*;

verus! {

fn source_option_as_deref<T: Deref>(
    option: &Option<T>,
) -> (res: Option<&T::Target>)
    ensures
        match option {
            Some(value) => res is Some && call_ensures(
                <T as Deref>::deref,
                (value,),
                res->0,
            ),
            None => res is None,
        },
{
    option.as_ref().map(Deref::deref)
}

} // verus!

fn main() {}