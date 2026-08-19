// Generated core::slice contracts selected for B72.

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

pub assume_specification<T>[ <[T]>::split_last ](
    slice: &[T],
) -> (ret: Option<(&T, &[T])>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == slice@[(slice@.len() - 1) as int]
            && ret.unwrap().1@ == slice@.subrange(0, (slice@.len() - 1) as int),
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

pub assume_specification<'a, T>[ <[T]>::iter_mut ](
    slice: &'a mut [T],
) -> (iter: core::slice::IterMut<'a, T>)
    ensures
        slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining == old(slice)@,
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T>[ <[T]>::chunks ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::Chunks<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::chunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter)),
;

pub assume_specification<'a, T>[ <[T]>::rchunks ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunks<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::rchunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter)),
;

pub assume_specification<'a, T>[ <[T]>::windows ](
    slice: &'a [T],
    size: usize,
) -> (iter: core::slice::Windows<'a, T>)
    requires
        size != 0,
    ensures
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).chunk_size == size as int,
        !slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T, const N: usize>[ <[T]>::array_windows::<N> ](
    slice: &'a [T],
) -> (iter: core::slice::ArrayWindows<'a, T, N>)
    requires
        N != 0,
    ensures
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).chunk_size == N as int,
        !slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ core::slice::ChunksExact::<'a, T>::remainder ](
    iter: &core::slice::ChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::ChunksExactMut::<'a, T>::into_remainder ](
    iter: core::slice::ChunksExactMut<'a, T>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::RChunksExact::<'a, T>::remainder ](
    iter: &core::slice::RChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::RChunksExactMut::<'a, T>::into_remainder ](
    iter: core::slice::RChunksExactMut<'a, T>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ <[T]>::chunks_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remaining == old(slice)@,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::chunks_exact_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksExactMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter)),
;

pub assume_specification<'a, T>[ <[T]>::rchunks_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remaining == old(slice)@,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remainder == Seq::empty(),
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::rchunks_exact_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksExactMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).yielded_prefix == Seq::empty(),
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter)),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::Split<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::Split<'a, T, F>, F, T>(
            iter, slice@, pred, false, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::SplitMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_inclusive::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::SplitInclusive<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitInclusive<'a, T, F>, F, T>(
            iter, slice@, pred, true, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[
    <[T]>::split_inclusive_mut::<F>
](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::SplitInclusiveMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitInclusiveMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, true, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn::<F> ](
    slice: &'a [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::SplitN<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitN<'a, T, F>, F, T>(
            iter, slice@, pred, false, false, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn_mut::<F> ](
    slice: &'a mut [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::SplitNMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitNMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, false, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::RSplit<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplit<'a, T, F>, F, T>(
            iter, slice@, pred, false, true, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::RSplitMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, true, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn::<F> ](
    slice: &'a [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::RSplitN<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitN<'a, T, F>, F, T>(
            iter, slice@, pred, false, true, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn_mut::<F> ](
    slice: &'a mut [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::RSplitNMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitNMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, true, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::ChunkBy<'a, T, F>)
    ensures
        slice_adjacent_chunk_view::<core::slice::ChunkBy<'a, T, F>, F, T>(iter, slice@, pred),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::ChunkByMut<'a, T, F>)
    ensures
        slice_adjacent_chunk_view::<core::slice::ChunkByMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred,
        ),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[ <[T]>::split_off::<R> ](
    slice_ref: &mut &'a [T],
    range: R,
) -> (ret: Option<&'a [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@,
        ),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[
    <[T]>::split_off_mut::<R>
](
    slice_ref: &mut &'a mut [T],
    range: R,
) -> (ret: Option<&'a mut [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@,
        ),
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, final(ret.unwrap())@,
        ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            )
            && (seq![*final(ret.unwrap())] + (*final(slice_ref))@).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            )
            && ((*final(slice_ref))@ + seq![*final(ret.unwrap())]).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a>[ <[u8]>::utf8_chunks ](
    slice: &'a [u8],
) -> (iter: core::str::Utf8Chunks<'a>)
    ensures
        utf8_chunk_partition::<core::str::Utf8Chunks<'a>>(iter, slice@),
;

pub assume_specification<T>[ <[T]>::as_mut_ptr ](
    slice: &mut [T],
) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
;

pub assume_specification<T>[ <[T]>::as_ptr ](
    slice: &[T],
) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
;

pub assume_specification[ <[u8]>::eq_ignore_ascii_case ](
    slice: &[u8],
    other: &[u8],
) -> (ret: bool)
    ensures
        ret <==> ascii_eq_ignore_case(slice@, other@),
;

pub assume_specification<'a>[ <[u8]>::escape_ascii ](
    slice: &'a [u8],
) -> (iter: core::slice::EscapeAscii<'a>)
    ensures
        slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).source == slice@,
        slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).remaining
            == ascii_escape_seq(slice@),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I>[ <[T]>::get_mut::<I> ](
    slice: &mut [T],
    index: I,
) -> (ret: Option<&mut <I as core::slice::SliceIndex<[T]>>::Output>)
    where I: core::slice::SliceIndex<[T]>
    ensures
        ret.is_some() ==> slice_index_in_range(old(slice)@, index)
            && slice_index_mut_frame(old(slice)@, index, final(slice)@),
        ret.is_none() ==> !slice_index_in_range(old(slice)@, index)
            && final(slice)@ == old(slice)@,
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

pub assume_specification[ <[u8]>::trim_ascii ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_source_body_result(slice@, ret),
;

pub assume_specification[ <[u8]>::trim_ascii_end ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_end_result(slice@, ret),
;

pub assume_specification[ <[u8]>::trim_ascii_start ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_start_result(slice@, ret),
;

} // verus!
