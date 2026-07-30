#![allow(dead_code)]
#![allow(unused_imports)]

use core::clone::Clone;
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_clone_proof<T: Clone>(opt: &Option<T>) -> (res: Option<T>)
    ensures
        opt.is_none() ==> res.is_none(),
        opt.is_some() ==> res.is_some() && cloned::<T>(opt.unwrap(), res.unwrap()),
{
    match opt {
        Some(x) => {
            let cloned_x = x.clone();
            assert(cloned::<T>(*x, cloned_x));
            Some(cloned_x)
        }
        None => None,
    }
}

}

fn main() {}