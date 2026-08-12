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
spec fn det___rust_std_candidate_equal<T>(r1: (*mut T, usize, usize), r2: (*mut T, usize, usize)) -> bool {
    ((true /* raw pointer: opaque by default */) && (r1.1 == r2.1) && (r1.2 == r2.2))
}

proof fn det___rust_std_candidate<T>(g_vec_leneq: bool, k_vec_leneq: nat, g_vec_lenrng: bool, k_vec_lenrng_lo: nat, k_vec_lenrng_hi: nat, g_r1_1_eq: bool, k_r1_1_eq: int, g_r1_1_rng: bool, k_r1_1_rng_lo: int, k_r1_1_rng_hi: int, g_r1_2_eq: bool, k_r1_2_eq: int, g_r1_2_rng: bool, k_r1_2_rng_lo: int, k_r1_2_rng_hi: int, g_r2_1_eq: bool, k_r2_1_eq: int, g_r2_1_rng: bool, k_r2_1_rng_lo: int, k_r2_1_rng_hi: int, g_r2_2_eq: bool, k_r2_2_eq: int, g_r2_2_rng: bool, k_r2_2_rng_lo: int, k_r2_2_rng_hi: int, g_neq_tuple: bool, vec: Vec<T>, r1: (*mut T, usize, usize), r2: (*mut T, usize, usize))
    ensures
        ({
            &&& (r1.1 == vec@.len())
            &&& (r1.2 as nat == vec.spec_capacity())
            &&& (vec_raw_parts_round_trip(vec@, vec.spec_capacity(), r1.0, r1.1, r1.2))
            &&& (r2.1 == vec@.len())
            &&& (r2.2 as nat == vec.spec_capacity())
            &&& (vec_raw_parts_round_trip(vec@, vec.spec_capacity(), r2.0, r2.1, r2.2))
        }) ==> det___rust_std_candidate_equal::<T>(r1, r2),
{
    if g_vec_leneq { assume(vec@.len() == k_vec_leneq); }
    if g_vec_lenrng { assume(vec@.len() >= k_vec_lenrng_lo && vec@.len() <= k_vec_lenrng_hi); }
    if g_r1_1_eq { assume(r1.1 as int == k_r1_1_eq); }
    if g_r1_1_rng { assume(r1.1 as int >= k_r1_1_rng_lo && r1.1 as int <= k_r1_1_rng_hi); }
    if g_r1_2_eq { assume(r1.2 as int == k_r1_2_eq); }
    if g_r1_2_rng { assume(r1.2 as int >= k_r1_2_rng_lo && r1.2 as int <= k_r1_2_rng_hi); }
    if g_r2_1_eq { assume(r2.1 as int == k_r2_1_eq); }
    if g_r2_1_rng { assume(r2.1 as int >= k_r2_1_rng_lo && r2.1 as int <= k_r2_1_rng_hi); }
    if g_r2_2_eq { assume(r2.2 as int == k_r2_2_eq); }
    if g_r2_2_rng { assume(r2.2 as int >= k_r2_2_rng_lo && r2.2 as int <= k_r2_2_rng_hi); }
    if g_neq_tuple { assume(!det___rust_std_candidate_equal::<T>(r1, r2)); }
}
}

fn main() {}
