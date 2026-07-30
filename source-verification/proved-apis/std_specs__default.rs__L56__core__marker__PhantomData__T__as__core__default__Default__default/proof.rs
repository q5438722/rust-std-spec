#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::marker::{PhantomData, PointeeSized};
use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn source_phantom_data_default<T: PointeeSized>() -> (r: PhantomData<T>)
    ensures
        r == PhantomData::<T>,
{
    PhantomData::<T>
}

}

fn main() {}