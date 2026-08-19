// Generated alloc::vec contracts selected for B72.

include!("vec_shared_vocabulary.rs");

verus! {

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

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::into_boxed_slice ](
    vec: Vec<T, A>,
) -> (ret: alloc::boxed::Box<[T], A>)
    ensures
        boxed_slice_view::<T, A>(ret) == vec@,
        boxed_slice_capacity::<T, A>(ret) == vec@.len(),
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

} // verus!
