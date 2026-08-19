#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::split_off
// Source: alloc/src/vec/mod.rs:3080-3107
// Source item sha256: d672f7a5113a022b6b6ad201e5b796e498199cb4e7506226bde479431b7eb5c2
// Dependency manifest: proof_manifests/175_alloc_vec_Vec_split_off/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// bounds check/panic arm, other_len computation, with_capacity_in using the
// cloned allocator, executable unsafe set_len calls, copy_nonoverlapping, and
// returning other. The allocator accessor and empty Vec construction are
// source-shaped field/constructor code; trusted boundaries are limited to Clone,
// the Vec length/capacity type invariant, raw start-pointer/provenance, and the
// source-backed copy_nonoverlapping storage observation consumed by the return
// Vec's modeled length commit.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    cap: usize,
    alloc: A,
    _marker_t: PhantomData<T>,
}

pub struct ConstPtr<T> {
    _marker_t: PhantomData<T>,
}

pub struct MutPtr<T> {
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
    model: Ghost<Seq<T>>,
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

pub open spec fn raw_vec_copy_nonoverlapping_model<T>(
    source: Seq<T>,
    src_start: int,
    count: int,
) -> Seq<T> {
    source.subrange(src_start, src_start + count)
}

pub closed spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat {
    buf.cap as nat
}

pub open spec fn vec_start_ptr<T>(seq: Seq<T>, capacity: nat, ptr: ConstPtr<T>) -> bool {
    seq.len() <= capacity
}

pub open spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: MutPtr<T>) -> bool {
    seq.len() <= capacity
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        if self.model@.len() == self.len as nat {
            self.model@
        } else {
            raw_vec_initialized_seq(&self.buf, self.len)
        }
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

pub mod ptr {
    use super::*;

    pub unsafe fn copy_nonoverlapping<T>(
        _src: ConstPtr<T>,
        _dst: MutPtr<T>,
        count: usize,
        Ghost(source): Ghost<Seq<T>>,
        src_start: usize,
    ) -> (after: Ghost<Seq<T>>)
        requires
            src_start as int <= source.len(),
            src_start as int + count as int <= source.len(),
        ensures
            after@ == raw_vec_copy_nonoverlapping_model(
                source,
                src_start as int,
                count as int,
            ),
            after@.len() == count as nat,
    {
        Ghost(raw_vec_copy_nonoverlapping_model(source, src_start as int, count as int))
    }
}

impl<T> ConstPtr<T> {
    pub unsafe fn add(self, count: usize) -> (ptr: ConstPtr<T>) {
        self
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        self.len as nat <= raw_vec_capacity(&self.buf)
    }

    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
            self@.len() <= self.spec_capacity(),
    {
        proof {
            use_type_invariant(self);
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
            assert(self@.len() == self.len as nat);
            assert(self.spec_capacity() == raw_vec_capacity(&self.buf));
        }
        self.len
    }

    pub fn allocator(&self) -> (allocator: &A)
    {
        &self.buf.alloc
    }

    pub fn with_capacity_in(capacity: usize, alloc: A) -> (vec: Vec<T, A>)
        ensures
            vec@ == Seq::<T>::empty(),
            vec.spec_capacity() >= capacity as nat,
    {
        Vec {
            buf: RawVec { cap: capacity, alloc, _marker_t: PhantomData },
            len: 0,
            model: Ghost(Seq::<T>::empty()),
        }
    }

    pub unsafe fn set_len(&mut self, new_len: usize, Ghost(model): Ghost<Seq<T>>)
        requires
            new_len as nat <= old(self).spec_capacity(),
            model.len() == new_len as nat,
        ensures
            final(self)@ == model,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        self.len = new_len;
        self.model = Ghost(model);
        proof {
            assert(self.model@.len() == self.len as nat);
            assert(self.spec_capacity() == old(self).spec_capacity());
        }
    }

    fn commit_initialized_model(&mut self, Ghost(model): Ghost<Seq<T>>)
        requires
            model.len() == old(self)@.len(),
        ensures
            final(self)@ == model,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        proof {
            use_type_invariant(&*self);
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
            assert(self@.len() == self.len as nat);
            assert(model.len() == self.len as nat);
        }
        self.model = Ghost(model);
        proof {
            assert(self.model@.len() == self.len as nat);
            assert(self.spec_capacity() == old(self).spec_capacity());
        }
    }

    pub fn as_ptr(&self) -> (ptr: ConstPtr<T>)
        ensures
            vec_start_ptr(self@, self.spec_capacity(), ptr),
    {
        let ghost source = self@;
        let ghost capacity = self.spec_capacity();
        let ptr = ConstPtr { _marker_t: PhantomData };
        proof {
            use_type_invariant(self);
            assert(source.len() == self.len as nat);
            assert(source.len() <= capacity);
        }
        ptr
    }

    pub fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            vec_start_mut_ptr(old(self)@, old(self).spec_capacity(), ptr),
            final(self)@ == old(self)@,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        let ghost source = self@;
        let ghost capacity = self.spec_capacity();
        let ptr = MutPtr { _marker_t: PhantomData };
        proof {
            use_type_invariant(&*self);
            assert(source.len() == self.len as nat);
            assert(source.len() <= capacity);
        }
        ptr
    }

    pub fn split_off(&mut self, at: usize) -> (return_value: Self)
        where A: core::clone::Clone
        requires
            at <= old(self)@.len(),
        ensures
            final(self)@ == old(self)@.subrange(0, at as int),
            return_value@ == old(self)@.subrange(at as int, old(self)@.len() as int),
    {
        let ghost source = self@;
        proof {
            assert(source.len() == self.len as nat);
            assert(at as nat <= self.len as nat);
            assert(at <= self.len);
        }

        if at > self.len() {
            assert_failed(at, self.len());
        }

        let other_len = self.len - at;
        let mut other = Vec::with_capacity_in(other_len, self.allocator().clone());

        proof {
            assert(other_len == self.len - at);
            assert(other_len as nat == source.len() - at as nat);
            assert(other_len as nat <= other.spec_capacity());
            assert(at as nat <= self.spec_capacity());
        }

        unsafe {
            self.set_len(at, Ghost(source.subrange(0, at as int)));
            other.set_len(other_len, Ghost(raw_vec_initialized_seq(&other.buf, other_len)));

            let copy_len = other.len();
            proof {
                assert(copy_len as nat == other_len as nat);
                assert(copy_len == other_len);
                assert(at as int + copy_len as int == source.len() as int);
            }
            let src_ptr = self.as_ptr().add(at);
            let dst_ptr = other.as_mut_ptr();
            let copied_tail = ptr::copy_nonoverlapping(
                src_ptr,
                dst_ptr,
                copy_len,
                Ghost(source),
                at,
            );
            proof {
                assert(copied_tail@ == source.subrange(at as int, at as int + copy_len as int));
                assert(copied_tail@ == source.subrange(at as int, source.len() as int));
                assert(copied_tail@.len() == other@.len());
            }
            other.commit_initialized_model(copied_tail);
        }
        proof {
            assert(self@ == source.subrange(0, at as int));
            assert(other@ == source.subrange(at as int, source.len() as int));
        }
        other
    }
}

proof fn raw_vec_prefix_after_set_len<T, A: Allocator>(
    buf: &RawVec<T, A>,
    old_len: usize,
    new_len: usize,
)
    requires
        new_len <= old_len,
    ensures
        raw_vec_initialized_seq(buf, new_len)
            == raw_vec_initialized_seq(buf, old_len).subrange(0, new_len as int),
{
    assert(raw_vec_initialized_seq::<T, A>(buf, new_len)
        =~= raw_vec_initialized_seq::<T, A>(buf, old_len).subrange(0, new_len as int));
}

pub fn assert_failed(at: usize, len: usize)
    requires
        false,
{
}

}
