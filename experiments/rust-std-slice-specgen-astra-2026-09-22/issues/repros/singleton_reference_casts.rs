use vstd::prelude::*;

verus! {

pub const fn shared_reference_cast<T>(s: &T) -> *const T {
    s as *const T
}

pub const fn mutable_reference_cast<T>(s: &mut T) -> *mut T {
    s as *mut T
}

}
