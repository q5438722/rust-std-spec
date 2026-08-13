#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::pop_if
// Source: alloc/src/vec/mod.rs:2843-2846
// Source item sha256: b806e75114ce9beed4d79d88159d2c39f067af6db3209e37d0cc3e551968b9e3
// Dependency manifest: proof_manifests/138_alloc_vec_Vec_pop_if/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// observe the last mutable element, call the predicate on it, and pop only when
// that predicate returns true. The trusted boundary is limited to the
// source-backed last_mut/pop Vec effects and the FnOnce predicate observation.

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

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn fnonce_predicate_returns<P, T>(predicate: P, before: T) -> bool;

pub uninterp spec fn fnonce_predicate_final_value<P, T>(predicate: P, before: T) -> T;

pub open spec fn vec_pop_if_result<T, P: FnOnce(&mut T) -> bool>(
    source: Seq<T>,
    predicate: P,
    ret: Option<T>,
    result: Seq<T>,
) -> bool {
    if source.len() == 0 {
        ret.is_none() && result == source
    } else {
        let last_index = source.len() - 1;
        let prefix = source.subrange(0, last_index as int);
        let before_last = source[last_index as int];
        let after_last = fnonce_predicate_final_value(predicate, before_last);
        if fnonce_predicate_returns(predicate, before_last) {
            ret.is_some() && ret.unwrap() == after_last && result == prefix
        } else {
            ret.is_none() && result == prefix.push(after_last)
        }
    }
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn pop_if<P>(&mut self, mut predicate: P) -> (ret: Option<T>)
        where
            P: FnOnce(&mut T) -> bool,
        ensures
            vec_pop_if_result(old(self)@, predicate, ret, final(self)@),
    {
        let ghost source = self@;
        match self.last_mut() {
            None => {
                proof {
                    assert(source.len() == 0);
                    assert(self@ == source);
                    assert(vec_pop_if_result::<T, P>(source, predicate, None::<T>, self@));
                }
                None
            },
            Some(last) => {
                proof {
                    assert(source.len() != 0);
                }
                let ghost last_index = source.len() - 1;
                let ghost prefix = source.subrange(0, last_index as int);
                let ghost before_last = source[last_index as int];
                let ghost after_last = fnonce_predicate_final_value(predicate, before_last);
                let ghost expected_predicate_result = fnonce_predicate_returns(predicate, before_last);
                let predicate_result = rust_1_96_call_once_predicate(&mut predicate, last);
                proof {
                    assert(predicate_result == expected_predicate_result);
                }
                if predicate_result {
                    proof {
                        assert(self@ == prefix.push(after_last));
                    }
                    let popped = self.pop();
                    proof {
                        assert(popped.is_some());
                        assert(popped.unwrap() == after_last);
                        assert(final(self)@ == prefix);
                        assert(vec_pop_if_result::<T, P>(source, predicate, popped, final(self)@));
                    }
                    popped
                } else {
                    proof {
                        assert(self@ == prefix.push(after_last));
                        assert(vec_pop_if_result::<T, P>(source, predicate, None::<T>, self@));
                    }
                    None
                }
            },
        }
    }

    #[verifier::external_body]
    fn last_mut<'a>(&'a mut self) -> (ret: Option<&'a mut T>)
        ensures
            ret.is_none() <==> old(self)@.len() == 0,
            ret.is_some() <==> old(self)@.len() != 0,
            old(self)@.len() == 0 ==> final(self)@ == old(self)@,
            old(self)@.len() != 0 ==> {
                let last_index = old(self)@.len() - 1;
                &&& *ret.unwrap() == old(self)@[last_index as int]
                &&& final(self)@ == old(self)@.subrange(0, last_index as int)
                    .push(*final(ret.unwrap()))
            },
    {
        if self.len == 0 {
            None
        } else {
            unsafe { Some(&mut *self.buf.ptr.add(self.len - 1)) }
        }
    }

    #[verifier::external_body]
    fn pop(&mut self) -> (ret: Option<T>)
        ensures
            old(self)@.len() == 0 ==> ret.is_none() && final(self)@ == old(self)@,
            old(self)@.len() != 0 ==> {
                let last_index = old(self)@.len() - 1;
                &&& ret.is_some()
                &&& ret.unwrap() == old(self)@[last_index as int]
                &&& final(self)@ == old(self)@.subrange(0, last_index as int)
            },
    {
        if self.len == 0 {
            None
        } else {
            self.len -= 1;
            unsafe { Some(core::ptr::read(self.buf.ptr.add(self.len))) }
        }
    }
}

#[verifier::external_body]
fn rust_1_96_call_once_predicate<T, P>(predicate: &mut P, value: &mut T) -> (ret: bool)
    where
        P: FnOnce(&mut T) -> bool,
    ensures
        *final(predicate) == *old(predicate),
        ret == fnonce_predicate_returns(*old(predicate), *old(value)),
        *final(value) == fnonce_predicate_final_value(*old(predicate), *old(value)),
{
    false
}

}
