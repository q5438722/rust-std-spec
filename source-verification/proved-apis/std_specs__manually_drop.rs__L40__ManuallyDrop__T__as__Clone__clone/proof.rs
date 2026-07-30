#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::manually_drop::*;
use core::clone::Clone;
use core::mem::ManuallyDrop;

verus! {

fn source_manually_drop_clone<T: Clone + ?Sized>(
    m: &ManuallyDrop<T>,
) -> (res: ManuallyDrop<T>)
    ensures
        cloned(m@, res@),
{
    let value = T::clone(&**m);
    assert(cloned(m@, value));
    ManuallyDrop::new(value)
}

}

fn main() {}