#![feature(allocator_api)]
#![feature(slice_index_methods)]
#![allow(unused_imports)]

// Clients of the official contracts, not proofs of the Rust implementations.
use std::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::cmp::PartialEqSpec;
use vstd::std_specs::core::IndexSpec;
use vstd::std_specs::iter::IteratorSpec;

verus! {

#[cfg(probe_positive)]
fn len_generic<T, A: Allocator>(v: &Vec<T, A>) -> (n: usize)
    ensures n == v@.len(),
{
    v.len()
}

#[cfg(probe_positive)]
fn index_range<T, A: Allocator>(v: &Vec<T, A>, lo: usize, hi: usize) -> (s: &[T])
    requires lo <= hi <= v@.len(),
    ensures s@ == v@.subrange(lo as int, hi as int),
{
    &v[lo..hi]
}

#[cfg(probe_positive)]
fn index_mut_usize<T, A: Allocator>(v: &mut Vec<T, A>, i: usize, x: T)
    requires i < old(v)@.len(),
    ensures final(v)@ == old(v)@.update(i as int, x),
{
    v[i] = x;
}

#[cfg(probe_positive)]
fn index_generic<T, I: std::slice::SliceIndex<[T]>, A: Allocator>(
    v: &Vec<T, A>, i: I,
) -> (r: &<Vec<T, A> as std::ops::Index<I>>::Output)
    requires v.index_req(&i),
    ensures exists|s: &[T]| #[trigger] s@ == v@ &&
        call_ensures(<I as std::slice::SliceIndex<[T]>>::index, (i, s), r),
{
    <Vec<T, A> as std::ops::Index<I>>::index(v, i)
}

#[cfg(probe_positive)]
fn box_into_vec<T, A: Allocator>(b: Box<[T], A>) -> (v: Vec<T, A>)
    ensures v@ == b@,
{
    b.into_vec()
}

#[cfg(probe_next)]
fn next_generic<T, A: Allocator>(it: &mut std::vec::IntoIter<T, A>) -> (r: Option<T>)
    requires IteratorSpec::remaining(old(it)).len() > 0,
    ensures
        r == Some(IteratorSpec::remaining(old(it))[0]),
        IteratorSpec::remaining(final(it)) == IteratorSpec::remaining(old(it)).drop_first(),
{
    it.next()
}

#[cfg(probe_next_back)]
fn next_back_generic<T, A: Allocator>(it: &mut std::vec::IntoIter<T, A>) -> (r: Option<T>)
    requires IteratorSpec::remaining(old(it)).len() > 0,
    ensures
        r == Some(IteratorSpec::remaining(old(it)).last()),
        IteratorSpec::remaining(final(it)) == IteratorSpec::remaining(old(it)).drop_last(),
{
    it.next_back()
}

#[cfg(probe_from_iter)]
fn from_iterator<T, I: IntoIterator<Item = T>>(it: I) -> (v: Vec<T>)
    ensures v@ == vstd::std_specs::iter::into_iter_remaining::<T, I>(it),
{
    Vec::from_iter(it)
}

#[cfg(probe_eq)]
fn eq_vec<T: PartialEq<U>, U, A1: Allocator, A2: Allocator>(
    x: &Vec<T, A1>, y: &Vec<U, A2>,
) -> (b: bool)
    ensures <Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::obeys_eq_spec()
        ==> b == <Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::eq_spec(x, y),
{
    <Vec<T, A1> as PartialEq<Vec<U, A2>>>::eq(x, y)
}

#[cfg(probe_ne)]
fn ne_vec<T: PartialEq<U>, U, A1: Allocator, A2: Allocator>(
    x: &Vec<T, A1>, y: &Vec<U, A2>,
) -> (b: bool)
    ensures <Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::obeys_eq_spec()
        ==> b == !<Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::eq_spec(x, y),
{
    <Vec<T, A1> as PartialEq<Vec<U, A2>>>::ne(x, y)
}

#[cfg(probe_as_ref_vec)]
fn as_ref_vec<T, A: Allocator>(v: &Vec<T, A>) -> (r: &Vec<T, A>)
    ensures r@ == v@,
{
    <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref(v)
}

#[cfg(probe_as_ref_slice)]
fn as_ref_slice<T, A: Allocator>(v: &Vec<T, A>) -> (r: &[T])
    ensures r@ == v@,
{
    <Vec<T, A> as AsRef<[T]>>::as_ref(v)
}

#[cfg(probe_as_mut_vec)]
fn as_mut_vec<T, A: Allocator>(v: &mut Vec<T, A>) -> (r: &mut Vec<T, A>)
    ensures r@ == old(v)@, final(r)@ == final(v)@,
{
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut(v)
}

#[cfg(probe_as_mut_slice)]
fn as_mut_slice<T, A: Allocator>(v: &mut Vec<T, A>) -> (r: &mut [T])
    ensures r@ == old(v)@, final(r)@ == final(v)@,
{
    <Vec<T, A> as AsMut<[T]>>::as_mut(v)
}

#[cfg(probe_index_mut_range)]
fn index_mut_range<T, A: Allocator>(v: &mut Vec<T, A>, lo: usize, hi: usize) -> (r: &mut [T])
    requires lo <= hi <= old(v)@.len(),
    ensures
        r@ == old(v)@.subrange(lo as int, hi as int),
        final(v)@ == old(v)@.subrange(0, lo as int) + final(r)@ + old(v)@.subrange(hi as int, old(v)@.len() as int),
{
    &mut v[lo..hi]
}

#[cfg(probe_index_mut_usize_ufcs)]
fn index_mut_usize_ufcs<T, A: Allocator>(v: &mut Vec<T, A>, i: usize, x: T)
    requires i < old(v)@.len(),
    ensures final(v)@ == old(v)@.update(i as int, x),
{
    *<Vec<T, A> as std::ops::IndexMut<usize>>::index_mut(v, i) = x;
}

#[cfg(probe_into_iter_elts_after_next)]
fn into_iter_elts_after_next<T>(v: Vec<T>) -> (it: std::vec::IntoIter<T>)
    requires v@.len() > 0,
    ensures vstd::std_specs::vec::into_iter_elts(it) == IteratorSpec::remaining(&it),
{
    let mut it = v.into_iter();
    let _first = it.next();
    it
}

#[cfg(probe_from_iter_vec_contents)]
fn from_iter_vec_contents<T>(v: Vec<T>) -> (r: Vec<T>)
    ensures r@ == v@,
{
    Vec::from_iter(v)
}

#[cfg(probe_try_reserve_variant)]
fn try_reserve_variant<T, A: Allocator>(v: &mut Vec<T, A>) -> (r: Result<(), std::collections::TryReserveError>)
    ensures r.is_ok(),
{
    v.try_reserve(0)
}

}
