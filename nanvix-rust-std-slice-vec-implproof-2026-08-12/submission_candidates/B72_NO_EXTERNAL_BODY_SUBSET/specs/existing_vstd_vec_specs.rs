// Exact existing-vstd alloc::vec contracts selected for B72.



verus! {

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::capacity ](
    v: &Vec<T, A>,
) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;

pub assume_specification<T, A: core::alloc::Allocator> [ <Vec<T, A>>::is_empty ](
    v: &Vec<T, A>,
) -> (res: bool)
    ensures res <==> v@.len() == 0,
;

#[verifier::when_used_as_spec(spec_vec_len)]
pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::len ](
    vec: &Vec<T, A>,
) -> (len: usize)
    ensures
        len == spec_vec_len(vec),
    no_unwind
;

pub assume_specification<T>[ Vec::<T>::new ]() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::reserve ](
    vec: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::shrink_to ](
    v: &mut Vec<T, A>,
    min_capacity: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::shrink_to_fit ](
    v: &mut Vec<T, A>,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification<T, A: core::alloc::Allocator + core::clone::Clone>[ Vec::<T, A>::split_off ](
    vec: &mut Vec<T, A>,
    at: usize,
) -> (return_value: Vec<T, A>)
    requires
        at <= old(vec)@.len(),
    ensures
        final(vec)@ == old(vec)@.subrange(0, at as int),
        return_value@ == old(vec)@.subrange(at as int, old(vec)@.len() as int),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::truncate ](
    vec: &mut Vec<T, A>,
    len: usize,
)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::try_reserve ](
    vec: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::try_reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;

pub assume_specification<T>[ Vec::<T>::with_capacity ](capacity: usize) -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
;

} // verus!
