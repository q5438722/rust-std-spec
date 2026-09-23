use vstd::prelude::*;

#[path = "../specs/mod.rs"]
mod specs;
#[path = "../proofs/correctness/slice/is_empty.rs"]
mod source_observer;

verus! {

pub fn shared_default_value<'a, T>() -> (result: &'a [T])
    ensures
        result@ =~= Seq::<T>::empty(),
{
    <&'a [T] as core::default::Default>::default()
}

pub fn mutable_default_value<'a, T>() -> (result: &'a mut [T])
    ensures
        result@ =~= Seq::<T>::empty(),
{
    <&'a mut [T] as core::default::Default>::default()
}

pub fn shared_default_is_empty<T>() -> (result: bool)
    ensures
        result,
{
    let slice: &[T] = Default::default();
    source_observer::is_empty(slice)
}

pub fn mutable_default_is_empty<T>() -> (result: bool)
    ensures
        result,
{
    let slice: &mut [T] = Default::default();
    source_observer::is_empty(slice)
}

pub fn nonempty_is_not_default() {
    let array = [7u8];
    let slice: &[u8] = &array;
    assert(!specs::slice_default::post::default_post(slice));
}

}
