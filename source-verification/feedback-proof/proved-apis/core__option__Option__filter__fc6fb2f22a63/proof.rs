#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_filter<T, P: FnOnce(&T) -> bool>(
    option: Option<T>,
    predicate: P,
) -> (res: Option<T>)
    requires
        option.is_some() ==> predicate.requires((&option.unwrap(),)),
        option.is_some() ==> forall|keep1: bool, keep2: bool|
            #![trigger predicate.ensures((&option.unwrap(),), keep1),
                       predicate.ensures((&option.unwrap(),), keep2)]
            predicate.ensures((&option.unwrap(),), keep1)
                && predicate.ensures((&option.unwrap(),), keep2)
                ==> keep1 == keep2,
    ensures
        option.is_none() ==> res.is_none(),
        option.is_some() ==> exists|keep: bool| {
            &&& #[trigger] predicate.ensures((&option.unwrap(),), keep)
            &&& res == if keep { option } else { None }
        },
{
    if let Some(x) = option {
        if predicate(&x) {
            return Some(x);
        }
    }
    None
}

} // verus!

fn main() {}