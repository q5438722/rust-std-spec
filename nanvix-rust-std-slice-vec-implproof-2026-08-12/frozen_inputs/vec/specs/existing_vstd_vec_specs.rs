// Exact existing-vstd alloc::vec contracts copied into the isolated Vec workspace.

include!("vec_shared_vocabulary.rs");

verus! {

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::append ](
    vec: &mut Vec<T, A>,
    other: &mut Vec<T, A>,
)
    ensures
        final(vec)@ == old(vec)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
;

#[doc(hidden)]
pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_mut_slice ](
    vec: &mut Vec<T, A>,
) -> (slice: &mut [T])
    ensures
        slice@ == old(vec)@,
        final(slice)@ == final(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::as_slice ](
    vec: &Vec<T, A>,
) -> (slice: &[T])
    ensures
        slice@ == vec@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::capacity ](
    v: &Vec<T, A>,
) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::clear ](vec: &mut Vec<T, A>)
    ensures
        final(vec).view() == Seq::<T>::empty(),
;

pub assume_specification<T: core::clone::Clone, A: core::alloc::Allocator>[ Vec::<T, A>::extend_from_slice ](
    vec: &mut Vec<T, A>,
    other: &[T],
)
    ensures
        final(vec)@.len() == old(vec)@.len() + other@.len(),
        forall|i: int|
            #![trigger final(vec)@[i]]
            0 <= i < final(vec)@.len() ==> if i < old(vec)@.len() {
                final(vec)@[i] == old(vec)@[i]
            } else {
                cloned::<T>(other@[i - old(vec)@.len()], final(vec)@[i])
            },
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::insert ](
    vec: &mut Vec<T, A>,
    i: usize,
    element: T,
)
    requires
        i <= old(vec).len(),
    ensures
        final(vec)@ == old(vec)@.insert(i as int, element),
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

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::pop ](
    vec: &mut Vec<T, A>,
) -> (value: Option<T>)
    ensures
        old(vec)@.len() > 0 ==> value == Some(old(vec)@[old(vec)@.len() - 1])
            && final(vec)@ == old(vec)@.subrange(0, old(vec)@.len() - 1),
        old(vec)@.len() == 0 ==> value == None::<T> && final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::push ](
    vec: &mut Vec<T, A>,
    value: T,
)
    ensures
        final(vec)@ == old(vec)@.push(value),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::remove ](
    vec: &mut Vec<T, A>,
    i: usize,
) -> (element: T)
    requires
        i < old(vec).len(),
    ensures
        element == old(vec)[i as int],
        final(vec)@ == old(vec)@.remove(i as int),
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::reserve ](
    vec: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(vec)@ == old(vec)@,
;

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;

pub assume_specification<T: core::clone::Clone, A: core::alloc::Allocator>[ Vec::<T, A>::resize ](
    vec: &mut Vec<T, A>,
    len: usize,
    value: T,
)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> {
            &&& final(vec)@.len() == len
            &&& final(vec)@.subrange(0, old(vec).len() as int) == old(vec)@
            &&& forall|i| #![all_triggers] old(vec).len() <= i < len ==> cloned::<T>(value, final(vec)@[i])
        },
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

pub assume_specification<T, A: core::alloc::Allocator>[ Vec::<T, A>::swap_remove ](
    vec: &mut Vec<T, A>,
    i: usize,
) -> (element: T)
    requires
        i < old(vec).len(),
    ensures
        element == old(vec)[i as int],
        final(vec)@ == old(vec)@.update(i as int, old(vec)@.last()).drop_last(),
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
