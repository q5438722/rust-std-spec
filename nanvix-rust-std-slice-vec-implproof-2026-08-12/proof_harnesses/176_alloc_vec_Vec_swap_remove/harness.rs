#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::swap_remove
// Source: alloc/src/vec/mod.rs:2223-2245
// Source item sha256: 5ce05988c4432399b0b8fd878d97db4b3d838b2d9e8fee4b9f5fa474778b9214
// Dependency manifest: proof_manifests/176_alloc_vec_Vec_swap_remove/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// len observation, unreachable bounds panic under the exact-vstd precondition,
// ptr::read of the removed element, as_mut_ptr, ptr::copy of the last element
// into the removed slot, set_len(len - 1), and returning the saved value.
// Trusted boundaries are limited to the reviewed raw pointer/provenance effects
// of as_ptr/as_mut_ptr/add/read/copy and the unsafe length commit.

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

pub struct ConstPtr<T> {
    raw: *const T,
    _marker_t: PhantomData<T>,
}

pub struct MutPtr<T> {
    raw: *mut T,
    _marker_t: PhantomData<T>,
}

impl<T> Copy for ConstPtr<T> {
}

impl<T> Clone for ConstPtr<T> {
    fn clone(&self) -> ConstPtr<T> {
        *self
    }
}

impl<T> Copy for MutPtr<T> {
}

impl<T> Clone for MutPtr<T> {
    fn clone(&self) -> MutPtr<T> {
        *self
    }
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

impl<T, A: Allocator> VecAdditionalSpecFns<T> for Vec<T, A> {
    open spec fn spec_index(&self, i: int) -> T {
        self@.index(i)
    }
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn read<T>(src: ConstPtr<T>, Ghost(source): Ghost<Seq<T>>, index: usize) -> (value: T)
        requires
            index < source.len(),
        ensures
            value == source[index as int],
    {
        core::ptr::read(src.raw)
    }

    #[verifier::external_body]
    pub unsafe fn copy<T>(src: MutPtr<T>, dst: MutPtr<T>, count: usize) {
    }
}

impl<T> ConstPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: ConstPtr<T>) {
        self
    }
}

impl<T> MutPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: MutPtr<T>) {
        self
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub closed spec fn spec_len(&self) -> usize {
        self.len
    }

    #[verifier::external_body]
    #[verifier::when_used_as_spec(spec_len)]
    pub fn len(&self) -> (len: usize)
        ensures
            len == self.spec_len(),
            len as nat == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: ConstPtr<T>)
    {
        ConstPtr { raw: self.buf.ptr, _marker_t: PhantomData }
    }

    #[verifier::external_body]
    pub fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            final(self)@ == old(self)@,
    {
        MutPtr { raw: self.buf.ptr, _marker_t: PhantomData }
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len as nat <= old(self)@.len(),
        ensures
            final(self)@.len() == new_len as nat,
    {
        self.len = new_len;
    }

    pub fn swap_remove(&mut self, i: usize) -> (element: T)
        requires
            i < old(self).len(),
        ensures
            element == old(self)[i as int],
            final(self)@ == old(self)@.update(i as int, old(self)@.last()).drop_last(),
    {
        let ghost source = self@;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
            assert(i < len);
            assert(source.len() > 0);
        }

        if i >= len {
            proof {
                assert(false);
            }
            rust_1_96_swap_remove_assert_failed(i, len);
        }

        unsafe {
            let value = ptr::read(self.as_ptr().add(i), Ghost(source), i);
            let base_ptr = self.as_mut_ptr();
            ptr::copy(base_ptr.add(len - 1), base_ptr.add(i), 1);
            self.set_len(len - 1);
            proof {
                rust_1_96_swap_remove_raw_copy_effect::<T, A>(self, source, i, len);
            }
            value
        }
    }
}

#[verifier::external_body]
pub fn rust_1_96_swap_remove_assert_failed(index: usize, len: usize)
    requires
        false,
{
    panic!("swap_remove index should be < len")
}

#[verifier::external_body]
proof fn rust_1_96_swap_remove_raw_copy_effect<T, A: Allocator>(
    vec: &Vec<T, A>,
    source: Seq<T>,
    i: usize,
    len: usize,
)
    requires
        source.len() > 0,
        i < source.len(),
        len as nat == source.len(),
        vec@.len() == source.len() - 1,
    ensures
        vec@ == source.update(i as int, source.last()).drop_last(),
{
}

}
