use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref
](vec: &'a Vec<T, A>) -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
        result@ == vec@,
;

// Generated equal-fn for determinism check.
// Policy: errs_equivalent=False, opaque_ok=False
spec fn __specdet_bb0b11a8961e3d093d8be4cc_equal<T, A: Allocator>(r1: &Vec<T, A>, r2: &Vec<T, A>) -> bool {
    ((r1)@ =~= (r2)@)
}

proof fn __specdet_bb0b11a8961e3d093d8be4cc<'a, T, A: Allocator>(g_vec_leneq: bool, k_vec_leneq: nat, g_vec_lenrng: bool, k_vec_lenrng_lo: nat, k_vec_lenrng_hi: nat, g_r1_leneq: bool, k_r1_leneq: nat, g_r1_lenrng: bool, k_r1_lenrng_lo: nat, k_r1_lenrng_hi: nat, g_r2_leneq: bool, k_r2_leneq: nat, g_r2_lenrng: bool, k_r2_lenrng_lo: nat, k_r2_lenrng_hi: nat, g_neq_tuple: bool, vec: &Vec<T, A>, r1: &Vec<T, A>, r2: &Vec<T, A>)
    ensures
        ({
            &&& (r1 == vec)
            &&& (r1@ == vec@)
            &&& (r2 == vec)
            &&& (r2@ == vec@)
        }) ==> __specdet_bb0b11a8961e3d093d8be4cc_equal::<T, A>(r1, r2),
{
    if g_vec_leneq { assume(vec@.len() == k_vec_leneq); }
    if g_vec_lenrng { assume(vec@.len() >= k_vec_lenrng_lo && vec@.len() <= k_vec_lenrng_hi); }
    if g_r1_leneq { assume(r1@.len() == k_r1_leneq); }
    if g_r1_lenrng { assume(r1@.len() >= k_r1_lenrng_lo && r1@.len() <= k_r1_lenrng_hi); }
    if g_r2_leneq { assume(r2@.len() == k_r2_leneq); }
    if g_r2_lenrng { assume(r2@.len() >= k_r2_lenrng_lo && r2@.len() <= k_r2_lenrng_hi); }
    if g_neq_tuple { assume(!__specdet_bb0b11a8961e3d093d8be4cc_equal::<T, A>(r1, r2)); }
}


pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsRef<[T]>>::as_ref
](vec: &'a Vec<T, A>) -> (result: &'a [T])
    ensures
        result@ == vec@,
;

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut
](vec: &'a mut Vec<T, A>) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        result@ == old(vec)@,
        *final(result) == *final(vec),
        final(result)@ == final(vec)@,
;

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsMut<[T]>>::as_mut
](vec: &'a mut Vec<T, A>) -> (result: &'a mut [T])
    ensures
        result@ == old(vec)@,
        final(result)@ == final(vec)@,
;

}
