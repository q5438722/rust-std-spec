#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::remove
// Source: alloc/src/vec/mod.rs:2367-2380
// Source item sha256: 26e35fd4f7dc7706abc1b2b1c43c40292645cf9bd7dc9a127f897931fed3d522
// Dependency manifest: proof_manifests/169_alloc_vec_Vec_remove/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// flow `match self.try_remove(i) { Some(elem) => elem, None => assert_failed(...) }`,
// adapted only to the exact existing-vstd parameter name `i`. The trusted
// boundary is the source-backed unstable `Vec::try_remove` implementation and
// its unreachable panic arm under the copied vstd precondition.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub closed spec fn len(&self) -> usize {
        self.len
    }

    #[verifier::external_body]
    fn try_remove(&mut self, index: usize) -> (ret: Option<T>)
        ensures
            index < old(self).len() ==> ret == Some(old(self)@[index as int])
                && final(self)@ == old(self)@.remove(index as int),
            index >= old(self).len() ==> ret == None::<T> && final(self)@ == old(self)@,
    {
        None
    }

    pub fn remove(&mut self, i: usize) -> (element: T)
        requires
            i < old(self).len(),
        ensures
            element == old(self)@[i as int],
            final(self)@ == old(self)@.remove(i as int),
    {
        match self.try_remove(i) {
            Some(elem) => elem,
            None => {
                proof {
                    assert(false);
                }
                rust_1_96_remove_assert_failed(i, self.len)
            },
        }
    }
}

#[verifier::external_body]
pub fn rust_1_96_remove_assert_failed<T>(index: usize, len: usize) -> (element: T)
    ensures
        false,
{
    panic!("removal index should be < len")
}

}
