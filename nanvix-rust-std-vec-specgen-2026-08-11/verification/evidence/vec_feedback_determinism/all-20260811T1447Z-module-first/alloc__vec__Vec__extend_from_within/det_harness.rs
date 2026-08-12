#![allow(unused_imports, dead_code)]
#![feature(allocator_api)]
#![feature(vec_into_raw_parts)]
extern crate alloc;
use vstd::prelude::*;
use alloc::boxed::Box;
use alloc::vec::*;
use vstd::seq::*;
use vstd::view::*;

verus! {
#[verifier::reject_recursive_types(A)]
#[verifier::reject_recursive_types(T)]
#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExDrain<'a, T, A>(std::vec::Drain<'a, T, A>)
where
    T: 'a,
    A: std::alloc::Allocator,
;

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
#[verifier::reject_recursive_types(F)]
#[verifier::reject_recursive_types(A)]
pub struct ExExtractIf<'a, T, F, A: core::alloc::Allocator>(ExtractIf<'a, T, F, A>);

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

impl<T, A: core::alloc::Allocator> CapacitySpec for Vec<T, A> {
    #[verifier::external_body]
    uninterp spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn spec_vec_len<T, A: core::alloc::Allocator>(v: &Vec<T, A>) -> usize;

pub broadcast proof fn axiom_spec_len<T, A: core::alloc::Allocator>(v: &Vec<T, A>)
    ensures
        #[trigger] spec_vec_len(v) == v@.len(),
{
    admit();
}

pub uninterp spec fn vec_start_ptr<T>(seq: Seq<T>, capacity: nat, ptr: *const T) -> bool;
pub uninterp spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: *mut T) -> bool;
pub uninterp spec fn vec_raw_parts_domain<T>(ptr: *mut T, length: usize, capacity: usize) -> bool;
pub uninterp spec fn vec_raw_parts_initialized_seq<T>(ptr: *mut T, length: usize) -> Seq<T>;
pub uninterp spec fn vec_raw_parts_round_trip<T>(
    seq: Seq<T>,
    capacity: nat,
    ptr: *mut T,
    length: usize,
    raw_capacity: usize,
) -> bool;

pub open spec fn vec_set_len_domain<T>(seq: Seq<T>, capacity: nat, new_len: usize) -> bool {
    new_len as nat <= capacity
}

pub uninterp spec fn vec_set_len_result<T>(
    old_seq: Seq<T>,
    capacity: nat,
    new_len: usize,
    final_seq: Seq<T>,
) -> bool;

pub uninterp spec fn vec_spare_capacity_relation<T>(
    seq: Seq<T>,
    capacity: nat,
    spare: Seq<core::mem::MaybeUninit<T>>,
) -> bool;

pub uninterp spec fn vec_drain_remaining<T, A: core::alloc::Allocator>(drain: &Drain<'_, T, A>) -> Seq<T>;
pub uninterp spec fn vec_into_iter_remaining<T, A: core::alloc::Allocator>(iter: &IntoIter<T, A>) -> Seq<T>;
pub uninterp spec fn vec_into_iter_remaining_mut<T, A: core::alloc::Allocator>(iter: IntoIter<T, A>) -> Seq<T>;

pub uninterp spec fn vec_range_start<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> int;
pub uninterp spec fn vec_range_end<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub open spec fn vec_range_bounds_valid<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> bool {
    0 <= vec_range_start(source, range)
        && vec_range_start(source, range) <= vec_range_end(source, range)
        && vec_range_end(source, range) <= source.len()
}

pub open spec fn vec_extend_from_within_result<T: core::clone::Clone, R: core::ops::RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    result: Seq<T>,
) -> bool {
    let start = vec_range_start(source, range);
    let end = vec_range_end(source, range);
    &&& vec_range_bounds_valid(source, range)
    &&& result.len() == source.len() + (end - start)
    &&& result.subrange(0, source.len() as int) == source
    &&& forall|i: int| #![trigger result[i]]
        source.len() <= i < result.len()
        ==> cloned::<T>(source[start + i - source.len()], result[i])
}

pub uninterp spec fn vec_drain_created<T, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    drain: Drain<'_, T, A>,
    shortened_vec: Seq<T>,
) -> bool;

pub uninterp spec fn vec_extract_if_created<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> bool, R: core::ops::RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    filter: F,
    iter: ExtractIf<'_, T, F, A>,
    shortened_vec: Seq<T>,
) -> bool;

pub uninterp spec fn boxed_slice_view<T, A: core::alloc::Allocator>(boxed: alloc::boxed::Box<[T], A>) -> Seq<T>;
pub uninterp spec fn boxed_slice_capacity<T, A: core::alloc::Allocator>(boxed: alloc::boxed::Box<[T], A>) -> nat;

pub uninterp spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T>;

pub open spec fn flatten_array_vec<T, const N: usize>(source: Seq<[T; N]>) -> Seq<T>
    decreases source.len()
{
    if source.len() == 0 {
        Seq::<T>::empty()
    } else {
        array_value_view::<T, N>(source[0]) + flatten_array_vec::<T, N>(source.subrange(1, source.len() as int))
    }
}

pub uninterp spec fn vec_dedup_partial_eq_result<T: core::cmp::PartialEq>(source: Seq<T>, result: Seq<T>) -> bool;
pub uninterp spec fn vec_dedup_by_result<T, F: core::ops::FnMut(&mut T, &mut T) -> bool>(source: Seq<T>, same_bucket: F, result: Seq<T>) -> bool;
pub uninterp spec fn vec_dedup_by_key_result<T, F: core::ops::FnMut(&mut T) -> K, K: core::cmp::PartialEq>(source: Seq<T>, key: F, result: Seq<T>) -> bool;
pub uninterp spec fn vec_pop_if_result<T, P: core::ops::FnOnce(&mut T) -> bool>(source: Seq<T>, predicate: P, ret: Option<T>, result: Seq<T>) -> bool;
pub uninterp spec fn vec_resize_with_result<T, F: core::ops::FnMut() -> T>(source: Seq<T>, new_len: usize, f: F, result: Seq<T>) -> bool;
pub uninterp spec fn vec_retain_result<T, F: core::ops::FnMut(&T) -> bool>(source: Seq<T>, f: F, result: Seq<T>) -> bool;
pub uninterp spec fn vec_retain_mut_result<T, F: core::ops::FnMut(&mut T) -> bool>(source: Seq<T>, f: F, result: Seq<T>) -> bool;

// Generated equal-fn for determinism check.
// Policy: errs_equivalent=True, opaque_ok=False
spec fn det___rust_std_candidate_equal<T: core::clone::Clone>(r1: (), r2: (), post1_vec: Seq<T>, post2_vec: Seq<T>) -> bool {
    (r1 == r2)
    && (post1_vec =~= post2_vec)
}

proof fn det___rust_std_candidate<T: core::clone::Clone, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>(g_pre_vec_leneq: bool, k_pre_vec_leneq: nat, g_pre_vec_lenrng: bool, k_pre_vec_lenrng_lo: nat, k_pre_vec_lenrng_hi: nat, g_post1_vec_leneq: bool, k_post1_vec_leneq: nat, g_post1_vec_lenrng: bool, k_post1_vec_lenrng_lo: nat, k_post1_vec_lenrng_hi: nat, g_post2_vec_leneq: bool, k_post2_vec_leneq: nat, g_post2_vec_lenrng: bool, k_post2_vec_lenrng_lo: nat, k_post2_vec_lenrng_hi: nat, g_neq_tuple: bool, pre_vec: Vec<T, A>, src: R, post1_vec: Vec<T, A>, r1: (), post2_vec: Vec<T, A>, r2: ())
    requires (vec_range_bounds_valid(pre_vec@, src)),
    ensures
        ({
            &&& (vec_extend_from_within_result(pre_vec@, src, post1_vec@))
            &&& (vec_extend_from_within_result(pre_vec@, src, post2_vec@))
        }) ==> det___rust_std_candidate_equal::<T>(r1, r2, post1_vec@, post2_vec@),
{
    if g_pre_vec_leneq { assume(pre_vec@.len() == k_pre_vec_leneq); }
    if g_pre_vec_lenrng { assume(pre_vec@.len() >= k_pre_vec_lenrng_lo && pre_vec@.len() <= k_pre_vec_lenrng_hi); }
    if g_post1_vec_leneq { assume(post1_vec@.len() == k_post1_vec_leneq); }
    if g_post1_vec_lenrng { assume(post1_vec@.len() >= k_post1_vec_lenrng_lo && post1_vec@.len() <= k_post1_vec_lenrng_hi); }
    if g_post2_vec_leneq { assume(post2_vec@.len() == k_post2_vec_leneq); }
    if g_post2_vec_lenrng { assume(post2_vec@.len() >= k_post2_vec_lenrng_lo && post2_vec@.len() <= k_post2_vec_lenrng_hi); }
    if g_neq_tuple { assume(!det___rust_std_candidate_equal::<T>(r1, r2, post1_vec@, post2_vec@)); }
}
}

fn main() {}
