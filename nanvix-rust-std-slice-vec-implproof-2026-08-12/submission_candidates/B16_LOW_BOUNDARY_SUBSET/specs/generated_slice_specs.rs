// Generated-contract submission subset for 16 core::slice targets.

include!("slice_shared_vocabulary.rs");

verus! {

pub assume_specification<T>[ <[T]>::split_first ](
    slice: &[T],
) -> (ret: Option<(&T, &[T])>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == slice@[0]
            && ret.unwrap().1@ == slice@.subrange(1, slice@.len() as int),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@,
                (*final(slice_ref))@,
                *ret.unwrap(),
            ),
;

pub assume_specification<T>[ <[T]>::split_last ](
    slice: &[T],
) -> (ret: Option<(&T, &[T])>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == slice@[(slice@.len() - 1) as int]
            && ret.unwrap().1@ == slice@.subrange(0, (slice@.len() - 1) as int),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@,
                (*final(slice_ref))@,
                *ret.unwrap(),
            ),
;

pub assume_specification<T>[ <[T]>::split_first_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == old(slice)@[0]
            && ret.unwrap().1@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            && final(slice)@ == seq![*final(ret.unwrap().0)] + final(ret.unwrap().1)@,
;

pub assume_specification<T>[ <[T]>::split_last_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == old(slice)@[(old(slice)@.len() - 1) as int]
            && ret.unwrap().1@ == old(slice)@.subrange(0, (old(slice)@.len() - 1) as int)
            && final(slice)@ == final(ret.unwrap().1)@ + seq![*final(ret.unwrap().0)],
;

pub assume_specification<'a, T>[ <[T]>::chunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).chunk_size
            == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(
            slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter)
        ),
;

pub assume_specification<'a, T>[ <[T]>::rchunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).chunk_size
            == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(
            slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter)
        ),
;

pub assume_specification[ <[u8]>::trim_ascii_start ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_start_result(slice@, ret),
;

pub assume_specification[ <[u8]>::trim_ascii_end ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_end_result(slice@, ret),
;

pub assume_specification[ <[u8]>::make_ascii_lowercase ](
    slice: &mut [u8],
)
    ensures
        final(slice)@ == ascii_lower_seq(old(slice)@),
;

pub assume_specification[ <[u8]>::make_ascii_uppercase ](
    slice: &mut [u8],
)
    ensures
        final(slice)@ == ascii_upper_seq(old(slice)@),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@,
                (*final(slice_ref))@,
                *ret.unwrap(),
            )
            && (seq![*final(ret.unwrap())] + (*final(slice_ref))@).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@,
                (*final(slice_ref))@,
                *ret.unwrap(),
            )
            && ((*final(slice_ref))@ + seq![*final(ret.unwrap())]).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a, T>[ core::slice::ChunksExact::<'a, T>::remainder ](
    iter: &core::slice::ChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).remainder,
        ret@.len()
            < slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::RChunksExact::<'a, T>::remainder ](
    iter: &core::slice::RChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).remainder,
        ret@.len()
            < slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).chunk_size,
;

} // verus!
