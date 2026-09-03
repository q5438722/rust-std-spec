#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Experiment-local strengthened proof for the N=2, length=3 representative.

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;
use vstd::seq_lib::*;

verus! {

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub open spec fn flatten_array_chunks<T, const N: usize>(chunks: Seq<[T; N]>) -> Seq<T> {
    if N == 0 {
        Seq::empty()
    } else {
        Seq::new(chunks.len() * (N as nat), |i: int|
            array_value_view::<T, N>(chunks[i / (N as int)])[i % (N as int)])
    }
}

pub open spec fn slice_array_chunks_partition<T, const N: usize>(
    seq: Seq<T>,
    chunks: Seq<[T; N]>,
    remainder: Seq<T>,
) -> bool {
    N != 0 && (remainder.len() as int) < N
        && flatten_array_chunks::<T, N>(chunks) + remainder == seq
}

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

pub open spec fn split_at_mut_unchecked_result<T>(
    source: Seq<T>,
    mid: usize,
    left: Seq<T>,
    right: Seq<T>,
    final_source: Seq<T>,
    final_left: Seq<T>,
    final_right: Seq<T>,
) -> bool {
    left == source.subrange(0, mid as int)
        && right == source.subrange(mid as int, source.len() as int)
        && final_source == final_left + final_right
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub mod ub_checks {
    use super::*;

    pub fn assert_unsafe_precondition(mid: usize, len: usize)
        requires
            mid <= len,
    {
    }
}

pub fn rust_1_96_slice_as_mut_ptr_cast<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    let len = slice.len();
    let ptr = core::ptr::null_mut::<T>().with_addr(len);
    proof {
        assert(old(slice)@.len() == len as nat);
    }
    ptr
}

pub fn as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    rust_1_96_slice_as_mut_ptr_cast(slice)
}

pub unsafe fn unchecked_sub(len: usize, mid: usize) -> (ret: usize)
    requires
        mid <= len,
    ensures
        ret as int == len as int - mid as int,
{
    len - mid
}

#[verifier::external_body]
pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    ensures
        ret@.len() == len,
        slice_start_mut_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_split_at_mut_unchecked_raw_parts<'a, T>(
    slice: &'a mut [T],
    ptr: *mut T,
    mid: usize,
    len: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
        mid <= len,
        len == old(slice)@.len(),
        slice_start_mut_ptr(old(slice)@, ptr),
    ensures
        split_at_mut_unchecked_result(
            old(slice)@,
            mid,
            ret.0@,
            ret.1@,
            final(slice)@,
            final(ret.0)@,
            final(ret.1)@,
        ),
        final(ret.0)@.len() == ret.0@.len(),
        final(ret.1)@.len() == ret.1@.len(),
{
    unsafe {
        (
            from_raw_parts_mut(ptr, mid),
            from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid)),
        )
    }
}

pub unsafe fn split_at_mut_unchecked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
        final(ret.0)@.len() == ret.0@.len(),
        final(ret.1)@.len() == ret.1@.len(),
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
        assert((mid as int) <= source.len());
        assert(mid <= len);
    }
    let ptr = as_mut_ptr(slice);
    ub_checks::assert_unsafe_precondition(mid, len);
    unsafe { rust_1_96_split_at_mut_unchecked_raw_parts(slice, ptr, mid, len) }
}

#[verifier::external_body]
pub unsafe fn as_chunks_unchecked_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: &'a mut [[T; N]])
    requires
        N != 0,
        old(slice)@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
        final(ret)@.len() == ret@.len(),
{
    unsafe { slice.as_chunks_unchecked_mut() }
}

proof fn lemma_flatten_chunk_two<T>(chunks: Seq<[T; 2]>, chunk: int)
    requires
        0 <= chunk < chunks.len(),
    ensures
        array_value_view::<T, 2>(chunks[chunk])
            == flatten_array_chunks::<T, 2>(chunks).subrange(chunk * 2, (chunk + 1) * 2),
{
    reveal(flatten_array_chunks);
    assert_seqs_equal!(
        array_value_view::<T, 2>(chunks[chunk])
            == flatten_array_chunks::<T, 2>(chunks).subrange(chunk * 2, (chunk + 1) * 2),
        index => {
            assert(0 <= index < 2);
            assert((chunk * 2 + index) / 2 == chunk);
            assert((chunk * 2 + index) % 2 == index);
        }
    );
}

proof fn lemma_concat_subranges<T>(left: Seq<T>, right: Seq<T>)
    ensures
        (left + right).subrange(0, left.len() as int) == left,
        (left + right).subrange(left.len() as int, (left + right).len() as int) == right,
{
    assert_seqs_equal!((left + right).subrange(0, left.len() as int) == left);
    assert_seqs_equal!(
        (left + right).subrange(left.len() as int, (left + right).len() as int) == right
    );
}

pub fn as_chunks_mut_n2_len3<'a, T>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [[T; 2]], &'a mut [T]))
    requires
        old(slice)@.len() == 3,
    ensures
        slice_array_chunks_partition::<T, 2>(old(slice)@, ret.0@, ret.1@),
        ret.0@.len() == old(slice)@.len() / 2nat,
        ret.1@.len() == old(slice)@.len() % 2nat,
        forall|chunk: int| #![auto] 0 <= chunk < ret.0@.len() ==>
            array_value_view::<T, 2>(ret.0@[chunk])
                == old(slice)@.subrange(chunk * 2, (chunk + 1) * 2),
        ret.1@ == old(slice)@.subrange((ret.0@.len() * 2nat) as int, old(slice)@.len() as int),
        final(ret.0)@.len() == ret.0@.len(),
        final(ret.1)@.len() == ret.1@.len(),
        final(slice)@ == flatten_array_chunks::<T, 2>(final(ret.0)@) + final(ret.1)@,
        forall|chunk: int| #![auto] 0 <= chunk < final(ret.0)@.len() ==>
            array_value_view::<T, 2>(final(ret.0)@[chunk])
                == final(slice)@.subrange(chunk * 2, (chunk + 1) * 2),
        final(ret.1)@ == final(slice)@.subrange(
            (final(ret.0)@.len() * 2nat) as int,
            final(slice)@.len() as int,
        ),
{
    assert(2usize != 0);
    let ghost source = slice@;
    let len = slice.len();
    assert(len == 3);
    let len_rounded_down = len / 2 * 2;
    assert(len_rounded_down == 2);
    assert(split_point_in_range::<T>(source, len_rounded_down));
    let (multiple_of_n, remainder) =
        unsafe { split_at_mut_unchecked(slice, len_rounded_down) };
    let ghost chunk_source = multiple_of_n@;
    assert(chunk_source == source.subrange(0, 2));
    assert(remainder@ == source.subrange(2, 3));
    assert(chunk_source.len() == 2);
    proof {
        source.lemma_split_at(2);
        assert(chunk_source + remainder@ == source);
    }
    let array_slice = unsafe { as_chunks_unchecked_mut::<T, 2>(multiple_of_n) };
    proof {
        reveal(flatten_array_chunks);
        assert(flatten_array_chunks::<T, 2>(array_slice@) == chunk_source);
        assert(flatten_array_chunks::<T, 2>(array_slice@) + remainder@ == source);
        assert(flatten_array_chunks::<T, 2>(array_slice@).len() == array_slice@.len() * 2);
        assert(array_slice@.len() == 1);
        assert(array_slice@.len() == source.len() / 2nat);
        assert(remainder@.len() == 1);
        assert(remainder@.len() == source.len() % 2nat);
        lemma_flatten_chunk_two(array_slice@, 0);
        assert forall|chunk: int| #![auto] 0 <= chunk < array_slice@.len() implies
            array_value_view::<T, 2>(array_slice@[chunk])
                == source.subrange(chunk * 2, (chunk + 1) * 2) by {
            assert(chunk == 0);
            lemma_flatten_chunk_two(array_slice@, chunk);
            assert(chunk_source.subrange(0, 2) == source.subrange(0, 2));
        }
        reveal(slice_array_chunks_partition);
        assert(slice_array_chunks_partition::<T, 2>(source, array_slice@, remainder@));

        assert(final(array_slice)@.len() == array_slice@.len());
        assert(final(remainder)@.len() == remainder@.len());
        let ghost final_combined =
            flatten_array_chunks::<T, 2>(final(array_slice)@) + final(remainder)@;
        lemma_concat_subranges(
            flatten_array_chunks::<T, 2>(final(array_slice)@),
            final(remainder)@,
        );
        assert forall|chunk: int| #![auto] 0 <= chunk < final(array_slice)@.len() implies
            array_value_view::<T, 2>(final(array_slice)@[chunk])
                == final_combined.subrange(chunk * 2, (chunk + 1) * 2) by {
            assert(chunk == 0);
            lemma_flatten_chunk_two(final(array_slice)@, chunk);
        }
        assert(final(array_slice)@.len() * 2nat == 2nat);
        assert(final(remainder)@ == final_combined.subrange(2, final_combined.len() as int));
    }
    (array_slice, remainder)
}

}
