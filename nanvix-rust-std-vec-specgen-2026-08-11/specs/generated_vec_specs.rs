// Generated executable alloc::vec contracts for uncovered stable rows.

include!("vec_shared_vocabulary.rs");

verus! {

pub assume_specification<'a, 'b, T, A: core::alloc::Allocator>[ Drain::<'a, T, A>::as_slice ](
    drain: &'b Drain<'a, T, A>,
) -> (ret: &'b [T])
    ensures
        ret@ == vec_drain_remaining::<T, A>(drain),
;

pub assume_specification<T, A: core::alloc::Allocator>[ IntoIter::<T, A>::as_mut_slice ](
    iter: &mut IntoIter<T, A>,
) -> (ret: &mut [T])
    ensures
        ret@ == vec_into_iter_remaining_mut::<T, A>(*old(iter)),
        vec_into_iter_remaining_mut::<T, A>(*final(iter)) == final(ret)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ IntoIter::<T, A>::as_slice ](
    iter: &IntoIter<T, A>,
) -> (ret: &[T])
    ensures
        ret@ == vec_into_iter_remaining::<T, A>(iter),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_mut_ptr ](
    vec: &mut Vec<T, A>,
) -> (ptr: *mut T)
    ensures
        vec_start_mut_ptr(old(vec)@, old(vec).spec_capacity(), ptr),
        final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_ptr ](
    vec: &Vec<T, A>,
) -> (ptr: *const T)
    ensures
        vec_start_ptr(vec@, vec.spec_capacity(), ptr),
;

pub assume_specification<T: core::cmp::PartialEq, A: core::alloc::Allocator>[ Vec::<T, A>::dedup ](
    vec: &mut Vec<T, A>,
)
    ensures
        vec_dedup_partial_eq_result(old(vec)@, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T, &mut T) -> bool>[
    Vec::<T, A>::dedup_by::<F>
](
    vec: &mut Vec<T, A>,
    same_bucket: F,
)
    ensures
        vec_dedup_by_result(old(vec)@, same_bucket, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> K, K: core::cmp::PartialEq>[
    Vec::<T, A>::dedup_by_key::<F, K>
](
    vec: &mut Vec<T, A>,
    key: F,
)
    ensures
        vec_dedup_by_key_result(old(vec)@, key, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>[
    Vec::<T, A>::drain::<R>
](
    vec: &mut Vec<T, A>,
    range: R,
) -> (drain: Drain<'_, T, A>)
    requires
        vec_range_bounds_valid(old(vec)@, range),
    ensures
        vec_drain_created(old(vec)@, range, drain, final(vec)@),
;

pub assume_specification<T: core::clone::Clone, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>[
    Vec::<T, A>::extend_from_within::<R>
](
    vec: &mut Vec<T, A>,
    src: R,
)
    requires
        vec_range_bounds_valid(old(vec)@, src),
    ensures
        vec_extend_from_within_result(old(vec)@, src, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> bool, R: core::ops::RangeBounds<usize>>[
    Vec::<T, A>::extract_if::<F, R>
](
    vec: &mut Vec<T, A>,
    range: R,
    filter: F,
) -> (iter: ExtractIf<'_, T, F, A>)
    requires
        vec_range_bounds_valid(old(vec)@, range),
    ensures
        vec_extract_if_created(old(vec)@, range, filter, iter, final(vec)@),
;

pub assume_specification<T>[ Vec::<T>::from_raw_parts ](
    ptr: *mut T,
    length: usize,
    capacity: usize,
) -> (vec: Vec<T>)
    requires
        vec_raw_parts_domain::<T>(ptr, length, capacity),
    ensures
        vec@ == vec_raw_parts_initialized_seq::<T>(ptr, length),
        vec.spec_capacity() == capacity as nat,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::insert_mut ](
    vec: &mut Vec<T, A>,
    index: usize,
    element: T,
) -> (ret: &mut T)
    requires
        index <= old(vec)@.len(),
    ensures
        *ret == element,
        final(vec)@ == old(vec)@.insert(index as int, *final(ret)),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::into_boxed_slice ](
    vec: Vec<T, A>,
) -> (ret: alloc::boxed::Box<[T], A>)
    ensures
        boxed_slice_view::<T, A>(ret) == vec@,
        boxed_slice_capacity::<T, A>(ret) == vec@.len(),
;

pub assume_specification<T, A: core::alloc::Allocator, const N: usize>[
    Vec::<[T; N], A>::into_flattened
](
    vec: Vec<[T; N], A>,
) -> (ret: Vec<T, A>)
    ensures
        ret@ == flatten_array_vec::<T, N>(vec@),
        ret@.len() == vec@.len() * N,
;

pub assume_specification<T>[ Vec::<T>::into_raw_parts ](
    vec: Vec<T>,
) -> (parts: (*mut T, usize, usize))
    ensures
        parts.1 == vec@.len(),
        parts.2 as nat == vec.spec_capacity(),
        vec_raw_parts_round_trip(vec@, vec.spec_capacity(), parts.0, parts.1, parts.2),
;

pub assume_specification<'a, T, A: core::alloc::Allocator + 'a>[ Vec::<T, A>::leak ](
    vec: Vec<T, A>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == vec@,
        final(ret)@.len() == vec@.len(),
;

pub assume_specification<T, A: core::alloc::Allocator, P: core::ops::FnOnce(&mut T) -> bool>[
    Vec::<T, A>::pop_if
](
    vec: &mut Vec<T, A>,
    predicate: P,
) -> (ret: Option<T>)
    ensures
        vec_pop_if_result(old(vec)@, predicate, ret, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::push_mut ](
    vec: &mut Vec<T, A>,
    value: T,
) -> (ret: &mut T)
    ensures
        *ret == value,
        final(vec)@ == old(vec)@.push(*final(ret)),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut() -> T>[
    Vec::<T, A>::resize_with::<F>
](
    vec: &mut Vec<T, A>,
    new_len: usize,
    f: F,
)
    ensures
        new_len <= old(vec)@.len() ==> final(vec)@ == old(vec)@.subrange(0, new_len as int),
        new_len > old(vec)@.len() ==> vec_resize_with_result(old(vec)@, new_len, f, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&T) -> bool>[
    Vec::<T, A>::retain::<F>
](
    vec: &mut Vec<T, A>,
    f: F,
)
    ensures
        vec_retain_result(old(vec)@, f, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> bool>[
    Vec::<T, A>::retain_mut::<F>
](
    vec: &mut Vec<T, A>,
    f: F,
)
    ensures
        vec_retain_mut_result(old(vec)@, f, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::set_len ](
    vec: &mut Vec<T, A>,
    new_len: usize,
)
    requires
        vec_set_len_domain(old(vec)@, old(vec).spec_capacity(), new_len),
    ensures
        final(vec)@.len() == new_len,
        vec_set_len_result(old(vec)@, old(vec).spec_capacity(), new_len, final(vec)@),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::spare_capacity_mut ](
    vec: &mut Vec<T, A>,
) -> (ret: &mut [core::mem::MaybeUninit<T>])
    ensures
        ret@.len() + old(vec)@.len() == old(vec).spec_capacity(),
        vec_spare_capacity_relation(old(vec)@, old(vec).spec_capacity(), ret@),
        final(vec)@ == old(vec)@,
;

} // verus!

// Machine-readable Vec spec catalog markers. Validators require these to match catalog rows.
// BEGIN VEC_SPEC target=alloc::vec::Drain::as_slice
// status: generated-new-real-relation-spec
// family: vec-iterator-adaptor-state
// source: alloc/src/vec/drain.rs:56
// signature: pub fn as_slice(&self) -> &[T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ == vec_drain_remaining::<T, A>(drain),
// shared_helpers: vec_drain_remaining
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Drain__as_slice/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Drain__as_slice/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Drain__as_slice/det_harness.rs
// target_binding_result: target alloc::vec::Drain::as_slice bound from inventory at alloc/src/vec/drain.rs:56
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<'a, 'b, T, A: core::alloc::Allocator>[ Drain::<'a, T, A>::as_slice ]( drain: &'b Drain<'a, T, A>, ) -> (ret: &'b [T]) ensures ret@ == vec_drain_remaining::<T, A>(drain), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::IntoIter::as_mut_slice
// status: generated-new-real-relation-spec
// family: vec-iterator-adaptor-state
// source: alloc/src/vec/into_iter.rs:106
// signature: pub fn as_mut_slice(&mut self) -> &mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ == vec_into_iter_remaining_mut::<T, A>(*old(iter)), vec_into_iter_remaining_mut::<T, A>(*final(iter)) == final(ret)@,
// shared_helpers: vec_into_iter_remaining_mut
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=unsupported_mut_ref_return; R0=unsupported; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_mut_slice/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_mut_slice/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_mut_slice/det_harness.rs
// target_binding_result: target alloc::vec::IntoIter::as_mut_slice bound from inventory at alloc/src/vec/into_iter.rs:106
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ IntoIter::<T, A>::as_mut_slice ]( iter: &mut IntoIter<T, A>, ) -> (ret: &mut [T]) ensures ret@ == vec_into_iter_remaining_mut::<T, A>(*old(iter)), vec_into_iter_remaining_mut::<T, A>(*final(iter)) == final(ret)@, ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::IntoIter::as_slice
// status: generated-new-real-relation-spec
// family: vec-iterator-adaptor-state
// source: alloc/src/vec/into_iter.rs:88
// signature: pub fn as_slice(&self) -> &[T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ == vec_into_iter_remaining::<T, A>(iter),
// shared_helpers: vec_into_iter_remaining
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_slice/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_slice/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__IntoIter__as_slice/det_harness.rs
// target_binding_result: target alloc::vec::IntoIter::as_slice bound from inventory at alloc/src/vec/into_iter.rs:88
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ IntoIter::<T, A>::as_slice ]( iter: &IntoIter<T, A>, ) -> (ret: &[T]) ensures ret@ == vec_into_iter_remaining::<T, A>(iter), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::as_mut_ptr
// status: generated-new-real-relation-spec
// family: vec-raw-parts-pointer-provenance
// source: alloc/src/vec/mod.rs:2058
// signature: pub const fn as_mut_ptr(&mut self) -> *mut T
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_start_mut_ptr(old(vec)@, old(vec).spec_capacity(), ptr), final(vec)@ == old(vec)@,
// shared_helpers: CapacitySpec::spec_capacity;vec_start_mut_ptr
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_mut_ptr/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_mut_ptr/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_mut_ptr/det_harness.rs
// target_binding_result: target alloc::vec::Vec::as_mut_ptr bound from inventory at alloc/src/vec/mod.rs:2058
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_mut_ptr ]( vec: &mut Vec<T, A>, ) -> (ptr: *mut T) ensures vec_start_mut_ptr(old(vec)@, old(vec).spec_capacity(), ptr), final(vec)@ == old(vec)@, ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::as_ptr
// status: generated-new-real-relation-spec
// family: vec-raw-parts-pointer-provenance
// source: alloc/src/vec/mod.rs:1974
// signature: pub const fn as_ptr(&self) -> *const T
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_start_ptr(vec@, vec.spec_capacity(), ptr),
// shared_helpers: CapacitySpec::spec_capacity;vec_start_ptr
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_ptr/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_ptr/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__as_ptr/det_harness.rs
// target_binding_result: target alloc::vec::Vec::as_ptr bound from inventory at alloc/src/vec/mod.rs:1974
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_ptr ]( vec: &Vec<T, A>, ) -> (ptr: *const T) ensures vec_start_ptr(vec@, vec.spec_capacity(), ptr), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::dedup
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:3704
// signature: pub fn dedup(&mut self)
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_dedup_partial_eq_result(old(vec)@, final(vec)@),
// shared_helpers: vec_dedup_partial_eq_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup/det_harness.rs
// target_binding_result: target alloc::vec::Vec::dedup bound from inventory at alloc/src/vec/mod.rs:3704
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T: core::cmp::PartialEq, A: core::alloc::Allocator>[ Vec::<T, A>::dedup ]( vec: &mut Vec<T, A>, ) ensures vec_dedup_partial_eq_result(old(vec)@, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::dedup_by
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:2651
// signature: pub fn dedup_by<F>(&mut self, mut same_bucket: F) where F: FnMut(&mut T, &mut T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_dedup_by_result(old(vec)@, same_bucket, final(vec)@),
// shared_helpers: vec_dedup_by_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by/det_harness.rs
// target_binding_result: target alloc::vec::Vec::dedup_by bound from inventory at alloc/src/vec/mod.rs:2651
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F>; where F: FnMut(&mut T, &mut T) -> bool
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T, &mut T) -> bool>[ Vec::<T, A>::dedup_by::<F> ]( vec: &mut Vec<T, A>, same_bucket: F, ) ensures vec_dedup_by_result(old(vec)@, same_bucket, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::dedup_by_key
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:2624
// signature: pub fn dedup_by_key<F, K>(&mut self, mut key: F) where F: FnMut(&mut T) -> K, K: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_dedup_by_key_result(old(vec)@, key, final(vec)@),
// shared_helpers: vec_dedup_by_key_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by_key/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by_key/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__dedup_by_key/det_harness.rs
// target_binding_result: target alloc::vec::Vec::dedup_by_key bound from inventory at alloc/src/vec/mod.rs:2624
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F, K>; where F: FnMut(&mut T) -> K, K: PartialEq
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> K, K: core::cmp::PartialEq>[ Vec::<T, A>::dedup_by_key::<F, K> ]( vec: &mut Vec<T, A>, key: F, ) ensures vec_dedup_by_key_result(old(vec)@, key, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::drain
// status: generated-new-real-relation-spec
// family: vec-iterator-adaptor-state
// source: alloc/src/vec/mod.rs:2985
// signature: pub fn drain<R>(&mut self, range: R) -> Drain<'_, T, A> where R: RangeBounds<usize>,
// requires: see executable declaration
// ensures: vec_drain_created(old(vec)@, range, drain, final(vec)@),
// shared_helpers: vec_range_bounds_valid;vec_range_start;vec_range_end;vec_drain_created
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-adaptor-state-boundary; unknown_review_reason=Iterator/adaptor values expose modeled remaining sequences but keep opaque lifetime/drop state.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__drain/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__drain/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__drain/det_harness.rs
// target_binding_result: target alloc::vec::Vec::drain bound from inventory at alloc/src/vec/mod.rs:2985
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <R>; where R: RangeBounds<usize>
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>[ Vec::<T, A>::drain::<R> ]( vec: &mut Vec<T, A>, range: R, ) -> (drain: Drain<'_, T, A>) requires vec_range_bounds_valid(old(vec)@, range), ensures vec_drain_created(old(vec)@, range, drain, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::extend_from_within
// status: generated-new-real-relation-spec
// family: vec-sequence-mutation
// source: alloc/src/vec/mod.rs:3597
// signature: pub fn extend_from_within<R>(&mut self, src: R) where R: RangeBounds<usize>,
// requires: see executable declaration
// ensures: vec_extend_from_within_result(old(vec)@, src, final(vec)@),
// shared_helpers: vec_range_bounds_valid;vec_range_start;vec_range_end;vec_extend_from_within_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extend_from_within/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extend_from_within/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extend_from_within/det_harness.rs
// target_binding_result: target alloc::vec::Vec::extend_from_within bound from inventory at alloc/src/vec/mod.rs:3597
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <R>; where R: RangeBounds<usize>
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T: core::clone::Clone, A: core::alloc::Allocator, R: core::ops::RangeBounds<usize>>[ Vec::<T, A>::extend_from_within::<R> ]( vec: &mut Vec<T, A>, src: R, ) requires vec_range_bounds_valid(old(vec)@, src), ensures vec_extend_from_within_result(old(vec)@, src, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::extract_if
// status: generated-new-real-relation-spec
// family: vec-iterator-adaptor-state
// source: alloc/src/vec/mod.rs:4224
// signature: pub fn extract_if<F, R>(&mut self, range: R, filter: F) -> ExtractIf<'_, T, F, A> where F: FnMut(&mut T) -> bool, R: RangeBounds<usize>,
// requires: see executable declaration
// ensures: vec_extract_if_created(old(vec)@, range, filter, iter, final(vec)@),
// shared_helpers: vec_range_bounds_valid;vec_range_start;vec_range_end;vec_extract_if_created
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-adaptor-state-boundary; unknown_review_reason=Iterator/adaptor values expose modeled remaining sequences but keep opaque lifetime/drop state.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extract_if/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extract_if/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__extract_if/det_harness.rs
// target_binding_result: target alloc::vec::Vec::extract_if bound from inventory at alloc/src/vec/mod.rs:4224
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F, R>; where F: FnMut(&mut T) -> bool, R: RangeBounds<usize>
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> bool, R: core::ops::RangeBounds<usize>>[ Vec::<T, A>::extract_if::<F, R> ]( vec: &mut Vec<T, A>, range: R, filter: F, ) -> (iter: ExtractIf<'_, T, F, A>) requires vec_range_bounds_valid(old(vec)@, range), ensures vec_extract_if_created(old(vec)@, range, filter, iter, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::from_raw_parts
// status: generated-new-real-relation-spec
// family: vec-raw-parts-pointer-provenance
// source: alloc/src/vec/mod.rs:642
// signature: pub const unsafe fn from_raw_parts(ptr: *mut T, length: usize, capacity: usize) -> Self
// requires: see executable declaration
// ensures: vec@ == vec_raw_parts_initialized_seq::<T>(ptr, length), vec.spec_capacity() == capacity as nat,
// shared_helpers: CapacitySpec::spec_capacity;vec_raw_parts_domain;vec_raw_parts_initialized_seq;vec_raw_parts_storage_ptr
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/targeted-from-raw-parts-20260811T1518Z/alloc__vec__Vec__from_raw_parts/result.json; synthetic=verification/evidence/vec_feedback_determinism/targeted-from-raw-parts-20260811T1518Z/alloc__vec__Vec__from_raw_parts/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/targeted-from-raw-parts-20260811T1518Z/alloc__vec__Vec__from_raw_parts/det_harness.rs
// target_binding_result: target alloc::vec::Vec::from_raw_parts bound from inventory at alloc/src/vec/mod.rs:642
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T>[ Vec::<T>::from_raw_parts ]( ptr: *mut T, length: usize, capacity: usize, ) -> (vec: Vec<T>) requires vec_raw_parts_domain::<T>(ptr, length, capacity), ensures vec@ == vec_raw_parts_initialized_seq::<T>(ptr, length), vec.spec_capacity() == capacity as nat, ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::insert_mut
// status: generated-new-real-relation-spec
// family: vec-sequence-mutation
// source: alloc/src/vec/mod.rs:2340
// signature: pub fn insert_mut(&mut self, index: usize, element: T) -> &mut T
// requires: see executable declaration
// ensures: *ret == element, final(vec)@ == old(vec)@.insert(index as int, *final(ret)),
// shared_helpers: Seq/View old/final relation
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=unsupported_mut_ref_return; R0=unsupported; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__insert_mut/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__insert_mut/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__insert_mut/det_harness.rs
// target_binding_result: target alloc::vec::Vec::insert_mut bound from inventory at alloc/src/vec/mod.rs:2340
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::insert_mut ]( vec: &mut Vec<T, A>, index: usize, element: T, ) -> (ret: &mut T) requires index <= old(vec)@.len(), ensures *ret == element, final(vec)@ == old(vec)@.insert(index as int, *final(ret)), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::into_boxed_slice
// status: generated-new-real-relation-spec
// family: vec-slice-boxed-slice-conversion
// source: alloc/src/vec/mod.rs:1731
// signature: pub fn into_boxed_slice(mut self) -> Box<[T], A>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: boxed_slice_view::<T, A>(ret) == vec@, boxed_slice_capacity::<T, A>(ret) == vec@.len(),
// shared_helpers: boxed_slice_view;boxed_slice_capacity
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=conversion-allocation-boundary; unknown_review_reason=Conversion preserves logical sequence while allocation identity/lifetime provenance remains boundary state.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_boxed_slice/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_boxed_slice/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_boxed_slice/det_harness.rs
// target_binding_result: target alloc::vec::Vec::into_boxed_slice bound from inventory at alloc/src/vec/mod.rs:1731
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::into_boxed_slice ]( vec: Vec<T, A>, ) -> (ret: alloc::boxed::Box<[T], A>) ensures boxed_slice_view::<T, A>(ret) == vec@, boxed_slice_capacity::<T, A>(ret) == vec@.len(), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::into_flattened
// status: generated-new-real-relation-spec
// family: vec-sequence-mutation
// source: alloc/src/vec/mod.rs:3633
// signature: pub fn into_flattened(self) -> Vec<T, A>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ == flatten_array_vec::<T, N>(vec@), ret@.len() == vec@.len() * N,
// shared_helpers: flatten_array_vec;array_value_view
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_flattened/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_flattened/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_flattened/det_harness.rs
// target_binding_result: target alloc::vec::Vec::into_flattened bound from inventory at alloc/src/vec/mod.rs:3633
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, const N: usize>[ Vec::<[T; N], A>::into_flattened ]( vec: Vec<[T; N], A>, ) -> (ret: Vec<T, A>) ensures ret@ == flatten_array_vec::<T, N>(vec@), ret@.len() == vec@.len() * N, ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::into_raw_parts
// status: generated-new-real-relation-spec
// family: vec-raw-parts-pointer-provenance
// source: alloc/src/vec/mod.rs:840
// signature: pub const fn into_raw_parts(self) -> (*mut T, usize, usize)
// requires: none beyond documented Rust panic/unsafe domains
// ensures: parts.1 == vec@.len(), parts.2 as nat == vec.spec_capacity(), vec_raw_parts_round_trip(vec@, vec.spec_capacity(), parts.0, parts.1, parts.2),
// shared_helpers: CapacitySpec::spec_capacity;vec_raw_parts_round_trip
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_raw_parts/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_raw_parts/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__into_raw_parts/det_harness.rs
// target_binding_result: target alloc::vec::Vec::into_raw_parts bound from inventory at alloc/src/vec/mod.rs:840
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T>[ Vec::<T>::into_raw_parts ]( vec: Vec<T>, ) -> (parts: (*mut T, usize, usize)) ensures parts.1 == vec@.len(), parts.2 as nat == vec.spec_capacity(), vec_raw_parts_round_trip(vec@, vec.spec_capacity(), parts.0, parts.1, parts.2), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::leak
// status: generated-new-real-relation-spec
// family: vec-slice-boxed-slice-conversion
// source: alloc/src/vec/mod.rs:3224
// signature: pub fn leak<'a>(self) -> &'a mut [T] where A: 'a,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ == vec@, final(ret)@.len() == vec@.len(),
// shared_helpers: Seq/View old/final relation
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=unsupported_mut_ref_return; R0=unsupported; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__leak/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__leak/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__leak/det_harness.rs
// target_binding_result: target alloc::vec::Vec::leak bound from inventory at alloc/src/vec/mod.rs:3224
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <'a>; where A: 'a
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<'a, T, A: core::alloc::Allocator + 'a>[ Vec::<T, A>::leak ]( vec: Vec<T, A>, ) -> (ret: &'a mut [T]) ensures ret@ == vec@, final(ret)@.len() == vec@.len(), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::pop_if
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:2880
// signature: pub fn pop_if(&mut self, predicate: impl FnOnce(&mut T) -> bool) -> Option<T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_pop_if_result(old(vec)@, predicate, ret, final(vec)@),
// shared_helpers: vec_pop_if_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__pop_if/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__pop_if/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__pop_if/det_harness.rs
// target_binding_result: target alloc::vec::Vec::pop_if bound from inventory at alloc/src/vec/mod.rs:2880
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, P: core::ops::FnOnce(&mut T) -> bool>[ Vec::<T, A>::pop_if ]( vec: &mut Vec<T, A>, predicate: P, ) -> (ret: Option<T>) ensures vec_pop_if_result(old(vec)@, predicate, ret, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::push_mut
// status: generated-new-real-relation-spec
// family: vec-sequence-mutation
// source: alloc/src/vec/mod.rs:1033
// signature: pub fn push_mut(&mut self, value: T) -> &mut T
// requires: none beyond documented Rust panic/unsafe domains
// ensures: *ret == value, final(vec)@ == old(vec)@.push(*final(ret)),
// shared_helpers: Seq/View old/final relation
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=unsupported_mut_ref_return; R0=unsupported; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__push_mut/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__push_mut/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__push_mut/det_harness.rs
// target_binding_result: target alloc::vec::Vec::push_mut bound from inventory at alloc/src/vec/mod.rs:1033
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::push_mut ]( vec: &mut Vec<T, A>, value: T, ) -> (ret: &mut T) ensures *ret == value, final(vec)@ == old(vec)@.push(*final(ret)), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::resize_with
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:3182
// signature: pub fn resize_with<F>(&mut self, new_len: usize, f: F) where F: FnMut() -> T,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: new_len <= old(vec)@.len() ==> final(vec)@ == old(vec)@.subrange(0, new_len as int), new_len > old(vec)@.len() ==> vec_resize_with_result(old(vec)@, new_len, f, final(vec)@),
// shared_helpers: vec_resize_with_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__resize_with/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__resize_with/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__resize_with/det_harness.rs
// target_binding_result: target alloc::vec::Vec::resize_with bound from inventory at alloc/src/vec/mod.rs:3182
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F>; where F: FnMut() -> T
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut() -> T>[ Vec::<T, A>::resize_with::<F> ]( vec: &mut Vec<T, A>, new_len: usize, f: F, ) ensures new_len <= old(vec)@.len() ==> final(vec)@ == old(vec)@.subrange(0, new_len as int), new_len > old(vec)@.len() ==> vec_resize_with_result(old(vec)@, new_len, f, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::retain
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:2488
// signature: pub fn retain<F>(&mut self, mut f: F) where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_retain_result(old(vec)@, f, final(vec)@),
// shared_helpers: vec_retain_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain/det_harness.rs
// target_binding_result: target alloc::vec::Vec::retain bound from inventory at alloc/src/vec/mod.rs:2488
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F>; where F: FnMut(&T) -> bool
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&T) -> bool>[ Vec::<T, A>::retain::<F> ]( vec: &mut Vec<T, A>, f: F, ) ensures vec_retain_result(old(vec)@, f, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::retain_mut
// status: generated-new-real-relation-spec
// family: vec-callback-trace-mutation
// source: alloc/src/vec/mod.rs:2514
// signature: pub fn retain_mut<F>(&mut self, mut f: F) where F: FnMut(&mut T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: vec_retain_mut_result(old(vec)@, f, final(vec)@),
// shared_helpers: vec_retain_mut_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=callback-trace-boundary; unknown_review_reason=FnMut/FnOnce or Clone effects are modeled by ordered source callback traces, preserving relational outcomes.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain_mut/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain_mut/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__retain_mut/det_harness.rs
// target_binding_result: target alloc::vec::Vec::retain_mut bound from inventory at alloc/src/vec/mod.rs:2514
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: <F>; where F: FnMut(&mut T) -> bool
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator, F: core::ops::FnMut(&mut T) -> bool>[ Vec::<T, A>::retain_mut::<F> ]( vec: &mut Vec<T, A>, f: F, ) ensures vec_retain_mut_result(old(vec)@, f, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::set_len
// status: generated-new-real-relation-spec
// family: vec-raw-parts-pointer-provenance
// source: alloc/src/vec/mod.rs:2224
// signature: pub unsafe fn set_len(&mut self, new_len: usize)
// requires: see executable declaration
// ensures: final(vec)@.len() == new_len, vec_set_len_result(old(vec)@, old(vec).spec_capacity(), new_len, final(vec)@),
// shared_helpers: CapacitySpec::spec_capacity;vec_set_len_domain;vec_set_len_result
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=Pointer address, provenance, and allocation layout are not uniquely recoverable from the Vec Seq view.; verus_rc=1; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__set_len/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__set_len/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__set_len/det_harness.rs
// target_binding_result: target alloc::vec::Vec::set_len bound from inventory at alloc/src/vec/mod.rs:2224
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::set_len ]( vec: &mut Vec<T, A>, new_len: usize, ) requires vec_set_len_domain(old(vec)@, old(vec).spec_capacity(), new_len), ensures final(vec)@.len() == new_len, vec_set_len_result(old(vec)@, old(vec).spec_capacity(), new_len, final(vec)@), ;
// END VEC_SPEC
// BEGIN VEC_SPEC target=alloc::vec::Vec::spare_capacity_mut
// status: generated-new-real-relation-spec
// family: vec-spare-capacity-maybeuninit-storage
// source: alloc/src/vec/mod.rs:3262
// signature: pub fn spare_capacity_mut(&mut self) -> &mut [MaybeUninit<T>]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@.len() + old(vec)@.len() == old(vec).spec_capacity(), vec_spare_capacity_relation(old(vec)@, old(vec).spec_capacity(), ret@), final(vec)@ == old(vec)@,
// shared_helpers: CapacitySpec::spec_capacity;vec_spare_capacity_relation
// typecheck_result: verus-typecheck: pass; rc=0; command=/usr/bin/timeout 110s /home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/vec_all_contracts_batch.rs --no-verify; harness=verification/harnesses/vec_all_contracts_batch.rs; stdout=verification/evidence/vec_all_contracts_batch.verus.stdout; stderr=verification/evidence/vec_all_contracts_batch.verus.stderr
// determinism_result: feedback-pipeline determinism: status=unsupported_mut_ref_return; R0=unsupported; evidence=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__spare_capacity_mut/result.json; synthetic=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__spare_capacity_mut/synthetic_spec.rs; harness=verification/evidence/vec_feedback_determinism/all-20260811T1447Z-module-first/alloc__vec__Vec__spare_capacity_mut/det_harness.rs
// target_binding_result: target alloc::vec::Vec::spare_capacity_mut bound from inventory at alloc/src/vec/mod.rs:3262
// signature_shape_result: signature mirrored from inventory row and copied Rust 1.96 source declaration
// generic_bounds_result: none
// reviewer_notes: Generated executable Vec assume_specification; feedback-pipeline determinism result recorded honestly.
// contract_text: pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::spare_capacity_mut ]( vec: &mut Vec<T, A>, ) -> (ret: &mut [core::mem::MaybeUninit<T>]) ensures ret@.len() + old(vec)@.len() == old(vec).spec_capacity(), vec_spare_capacity_relation(old(vec)@, old(vec).spec_capacity(), ret@), final(vec)@ == old(vec)@, ;
// END VEC_SPEC
