#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub assume_specification<T>[ core::slice::from_mut ](value: &mut T) -> (res: &mut [T])
    ensures
        res@ == seq![*old(value)],
        final(res)@ == seq![*final(value)],
;

fn source_option_as_mut_slice<T>(option: &mut Option<T>) -> (res: &mut [T])
    ensures
        res@ == (match *old(option) {
            Some(x) => seq![x],
            None => seq![],
        }),
        final(res)@.len() == res@.len(),
        final(option)@ == (match *old(option) {
            Some(_) => Some(final(res)@[0]),
            None => None,
        }),
{
    // This is the source's Some/None safety argument with unsupported
    // offset_of! pointer arithmetic desugared to its safe equivalents.
    match option {
        Some(value) => core::slice::from_mut(value),
        None => &mut [],
    }
}

} // verus!

fn main() {}