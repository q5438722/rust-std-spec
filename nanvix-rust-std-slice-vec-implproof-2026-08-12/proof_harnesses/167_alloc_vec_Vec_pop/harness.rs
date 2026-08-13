#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::pop
// Source: alloc/src/vec/mod.rs:2816-2826
// Source item sha256: 10b844ff4ce79b3395079cef34fd3168cc5b8972bebd01afb6a39e9af9574b34
// Dependency manifest: proof_manifests/167_alloc_vec_Vec_pop/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// len==0 returns None; otherwise decrement len, assert the new len is within
// capacity, read from as_ptr().add(len), and return Some(read_value). Trusted
// boundaries are limited to the reviewed Vec::as_ptr dependency, allocator
// capacity, raw-pointer add/provenance, and unsafe ptr::read.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *const T,
    cap: usize,
    _marker_a: PhantomData<A>,
}

pub struct ConstPtr<T> {
    raw: *const T,
    _marker_t: PhantomData<T>,
}

impl<T> Copy for ConstPtr<T> {
}

impl<T> Clone for ConstPtr<T> {
    fn clone(&self) -> ConstPtr<T> {
        ConstPtr { raw: self.raw, _marker_t: PhantomData }
    }
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

pub closed spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat {
    buf.cap as nat
}

pub uninterp spec fn vec_start_ptr<T>(seq: Seq<T>, capacity: nat, ptr: ConstPtr<T>) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

pub mod hint {
    use vstd::prelude::*;

    pub unsafe fn assert_unchecked(cond: bool)
        requires
            cond,
        ensures
            cond,
    {
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
}

impl<T> ConstPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: ConstPtr<T>)
    {
        self
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == self.spec_capacity(),
    {
        self.buf.capacity()
    }

    pub fn pop(&mut self) -> (value: Option<T>)
        ensures
            old(self)@.len() > 0 ==> value == Some(old(self)@[(old(self)@.len() - 1) as int])
                && final(self)@ == old(self)@.subrange(0, (old(self)@.len() - 1) as int),
            old(self)@.len() == 0 ==> value == None::<T> && final(self)@ == old(self)@,
    {
        let ghost source = self@;
        if self.len == 0 {
            proof {
                assert(source.len() == 0);
                assert(self@ == source);
            }
            None
        } else {
            let old_len = self.len;
            proof {
                assert(source.len() == old_len as nat);
                assert(old_len > 0);
            }
            unsafe {
                self.len -= 1;
                let new_len = self.len;
                let capacity = self.capacity();
                proof {
                    assert(new_len == old_len - 1);
                    rust_1_96_pop_capacity_boundary::<T, A>(source, new_len, capacity);
                    assert((new_len as nat) < (capacity as nat));
                    assert(new_len < capacity);
                }
                hint::assert_unchecked(self.len < capacity);
                let value = ptr::read(self.as_ptr().add(self.len), Ghost(source), self.len);
                proof {
                    raw_vec_prefix_after_decrement::<T, A>(&self.buf, old_len);
                    assert(self@ == source.subrange(0, (source.len() - 1) as int));
                    assert(new_len as nat == source.len() - 1);
                    assert(value == source[(source.len() - 1) as int]);
                }
                Some(value)
            }
        }
    }

    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: ConstPtr<T>)
        ensures
            vec_start_ptr(self@, self.spec_capacity(), ptr),
    {
        ConstPtr { raw: self.buf.ptr, _marker_t: PhantomData }
    }
}

pub proof fn raw_vec_prefix_after_decrement<T, A: Allocator>(buf: &RawVec<T, A>, old_len: usize)
    requires
        old_len > 0,
    ensures
        raw_vec_initialized_seq(buf, (old_len - 1) as usize)
            == raw_vec_initialized_seq(buf, old_len).subrange(0, (old_len - 1) as int),
{
    assert(raw_vec_initialized_seq::<T, A>(buf, (old_len - 1) as usize)
        =~= raw_vec_initialized_seq::<T, A>(buf, old_len).subrange(0, (old_len - 1) as int));
}

#[verifier::external_body]
proof fn rust_1_96_pop_capacity_boundary<T, A: Allocator>(
    source: Seq<T>,
    new_len: usize,
    capacity: usize,
)
    requires
        new_len as nat == source.len() - 1,
        source.len() > 0,
    ensures
        new_len < capacity,
{
}

}
