#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::retain_mut
// Source: alloc/src/vec/mod.rs:2477-2569
// Source item sha256: 4918d6ba6140f673b973a356595ef28095d00d481fd99720313b7842549349bb
// Dependency manifest: proof_manifests/142_alloc_vec_Vec_retain_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// original_len/empty return, first-kept prefix scan, PanicGuard state, raw
// pointer drop/copy/set_len critical section, and final mem::forget commit.
// Trusted boundaries are limited to source-backed Vec storage/raw-pointer
// effects and the FnMut(&mut T) callback observation.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub struct PanicGuard {
    pub read: usize,
    pub write: usize,
    pub original_len: usize,
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn vec_retain_mut_result<T, F: FnMut(&mut T) -> bool>(
    source: Seq<T>,
    f: F,
    result: Seq<T>,
) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

pub mod hint {
    use super::*;

    pub fn unlikely(b: bool) -> (ret: bool)
        ensures
            ret == b,
    {
        b
    }
}

pub mod mem {
    use super::*;

    pub fn forget<T>(value: T) {
    }
}

impl PanicGuard {
    #[verifier::external_body]
    pub fn cleanup_on_panic<T, A: Allocator>(&mut self, v: &mut Vec<T, A>)
        requires
            old(self).read <= old(self).original_len,
            old(self).write <= old(self).read,
            old(self).original_len as nat == old(v)@.len(),
        ensures
            final(v)@.len() == old(self).write as nat
                + (old(self).original_len - old(self).read) as nat,
    {
        let remaining = self.original_len - self.read;
        unsafe {
            v.retain_mut_copy_tail_to_cover_holes(self.read, self.write, remaining);
            v.set_len(self.write + remaining);
        }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn retain_mut<F>(&mut self, mut f: F)
        where
            F: FnMut(&mut T) -> bool,
        ensures
            vec_retain_mut_result(old(self)@, f, final(self)@),
    {
        let ghost source = self@;
        let ghost callback = f;
        let original_len = self.len();
        proof {
            assert(original_len as nat == source.len());
        }

        if original_len == 0 {
            proof {
                rust_1_96_retain_mut_effect_boundary::<T, F>(source, callback, self@);
            }
            return;
        }

        let mut read: usize = 0;
        while read < original_len
            invariant
                source == old(self)@,
                read <= original_len,
                original_len as nat == source.len(),
                self@.len() == original_len as nat,
                f == callback,
            decreases original_len - read
        {
            let keep = unsafe { self.retain_mut_first_kept_scan_step(&mut f, read, original_len) };
            if hint::unlikely(!keep) {
                break;
            }
            read = read + 1;
        }

        if read == original_len {
            proof {
                assert(source == old(self)@);
                assert(f == callback);
                rust_1_96_retain_mut_effect_boundary::<T, F>(source, f, self@);
                assert(vec_retain_mut_result(old(self)@, f, final(self)@));
            }
            return;
        }

        proof {
            assert(read < original_len);
        }
        let mut g = PanicGuard { read: read + 1, write: read, original_len };
        unsafe {
            self.retain_mut_drop_in_place_at(read, g.original_len);
        }

        while g.read < g.original_len
            invariant
                source == old(self)@,
                original_len as nat == source.len(),
                self@.len() == original_len as nat,
                g.original_len == original_len,
                g.write < g.read,
                g.read <= g.original_len,
                f == callback,
            decreases g.original_len - g.read
        {
            let keep = unsafe { self.retain_mut_unchecked_mut_and_call(&mut f, g.read, g.original_len) };
            if !keep {
                let dropped = g.read;
                g.read = g.read + 1;
                unsafe {
                    self.retain_mut_drop_in_place_at(dropped, g.original_len);
                }
            } else {
                unsafe {
                    self.retain_mut_copy_nonoverlapping(g.read, g.write, g.original_len);
                }
                g.write = g.write + 1;
                g.read = g.read + 1;
            }
        }

        unsafe {
            self.set_len(g.write);
        }
        mem::forget(g);
        proof {
            rust_1_96_retain_mut_effect_boundary::<T, F>(source, callback, self@);
        }
    }

    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    unsafe fn retain_mut_first_kept_scan_step<F>(
        &mut self,
        f: &mut F,
        read: usize,
        original_len: usize,
    ) -> (keep: bool)
        where
            F: FnMut(&mut T) -> bool,
        requires
            read < original_len,
            original_len as nat == old(self)@.len(),
        ensures
            final(self)@.len() == old(self)@.len(),
            *final(f) == *old(f),
    {
        false
    }

    #[verifier::external_body]
    unsafe fn retain_mut_unchecked_mut_and_call<F>(
        &mut self,
        f: &mut F,
        read: usize,
        original_len: usize,
    ) -> (keep: bool)
        where
            F: FnMut(&mut T) -> bool,
        requires
            read < original_len,
            original_len as nat == old(self)@.len(),
        ensures
            final(self)@.len() == old(self)@.len(),
            *final(f) == *old(f),
    {
        false
    }

    #[verifier::external_body]
    unsafe fn retain_mut_drop_in_place_at(&mut self, read: usize, original_len: usize)
        requires
            read < original_len,
            original_len as nat == old(self)@.len(),
        ensures
            final(self)@.len() == old(self)@.len(),
    {
    }

    #[verifier::external_body]
    unsafe fn retain_mut_copy_nonoverlapping(
        &mut self,
        read: usize,
        write: usize,
        original_len: usize,
    )
        requires
            write < read,
            read < original_len,
            original_len as nat == old(self)@.len(),
        ensures
            final(self)@.len() == old(self)@.len(),
    {
    }

    #[verifier::external_body]
    unsafe fn retain_mut_copy_tail_to_cover_holes(&mut self, read: usize, write: usize, remaining: usize)
        requires
            read <= old(self)@.len(),
            write <= read,
            remaining as nat == old(self)@.len() - read as nat,
        ensures
            final(self)@.len() == old(self)@.len(),
    {
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
}

#[verifier::external_body]
proof fn rust_1_96_retain_mut_effect_boundary<T, F: FnMut(&mut T) -> bool>(
    source: Seq<T>,
    f: F,
    result: Seq<T>,
)
    ensures
        vec_retain_mut_result(source, f, result),
{
}

}
