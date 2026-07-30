#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_take_if<T, P>(
    option: &mut Option<T>,
    predicate: P,
) -> (result: Option<T>)
where
    P: FnOnce(&mut T) -> bool,
    requires
        *old(option) is Some ==> forall |arg: &mut T| #![auto]
            *arg == old(option)->0 ==> predicate.requires((arg,)),
    ensures
        *old(option) is None ==> result is None && *final(option) is None,
        *old(option) is Some ==> exists |arg: &mut T, take: bool| #![auto] {
            &&& *arg == old(option)->0
            &&& predicate.ensures((arg,), take)
            &&& if take {
                result == Some(*final(arg)) && *final(option) is None
            } else {
                result is None && *final(option) == Some(*final(arg))
            }
        },
{
    let take = {
        let mapped = option.as_mut();
        let default = false;
        let f = predicate;
        match mapped {
            Some(arg) => f(arg),
            None => default,
        }
    };
    if take {
        option.take()
    } else {
        None
    }
}

} // verus!

fn main() {}