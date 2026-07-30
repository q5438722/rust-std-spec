#![feature(slice_range)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{Range, RangeBounds, RangeTo};
use vstd::prelude::*;
use vstd::std_specs::range::{
    slice_range_end, slice_range_start, slice_range_valid,
};
use vstd::std_specs::slice::*;

verus! {

pub assume_specification<R: RangeBounds<usize>>[ core::slice::range::<R> ](
    range: R,
    bounds: RangeTo<usize>,
) -> (result: Range<usize>)
    requires
        slice_range_valid(&range, bounds.end as nat),
    ensures
        result.start as int == slice_range_start(&range),
        result.end as int == slice_range_end(&range, bounds.end as nat),
;

pub open spec fn copy_state<T>(
    current: Seq<T>,
    original: Seq<T>,
    src_start: int,
    dest: int,
    copied_from: int,
    copied_to: int,
) -> bool {
    &&& current.len() == original.len()
    &&& forall|j: int| 0 <= j < original.len() ==> current[j] == if
        dest + copied_from <= j < dest + copied_to
    {
        original[src_start + (j - dest)]
    } else {
        original[j]
    }
}

proof fn lemma_forward_step<T>(
    current: Seq<T>,
    original: Seq<T>,
    src_start: int,
    dest: int,
    count: int,
    i: int,
)
    requires
        0 <= i < count,
        0 <= src_start,
        src_start + count <= original.len(),
        0 <= dest,
        dest + count <= original.len(),
        copy_state(current, original, src_start, dest, 0, i),
    ensures
        copy_state(
            current.update(dest + i, original[src_start + i]),
            original,
            src_start,
            dest,
            0,
            i + 1,
        ),
{
    assert forall|j: int| 0 <= j < original.len() implies
        #[trigger] current.update(dest + i, original[src_start + i])[j] == if
            dest <= j < dest + i + 1
        {
            original[src_start + (j - dest)]
        } else {
            original[j]
        }
    by {
        if j == dest + i {
            assert(src_start + (j - dest) == src_start + i);
        } else {
            assert(current.update(dest + i, original[src_start + i])[j] == current[j]);
            if dest <= j < dest + i + 1 {
                assert(j < dest + i);
            }
        }
    }
}

proof fn lemma_backward_step<T>(
    current: Seq<T>,
    original: Seq<T>,
    src_start: int,
    dest: int,
    count: int,
    i: int,
)
    requires
        0 < i <= count,
        0 <= src_start,
        src_start + count <= original.len(),
        0 <= dest,
        dest + count <= original.len(),
        copy_state(current, original, src_start, dest, i, count),
    ensures
        copy_state(
            current.update(dest + i - 1, original[src_start + i - 1]),
            original,
            src_start,
            dest,
            i - 1,
            count,
        ),
{
    assert forall|j: int| 0 <= j < original.len() implies
        #[trigger] current.update(dest + i - 1, original[src_start + i - 1])[j] == if
            dest + i - 1 <= j < dest + count
        {
            original[src_start + (j - dest)]
        } else {
            original[j]
        }
    by {
        if j == dest + i - 1 {
            assert(src_start + (j - dest) == src_start + i - 1);
        } else {
            assert(
                current.update(dest + i - 1, original[src_start + i - 1])[j]
                    == current[j]
            );
            if dest + i - 1 <= j < dest + count {
                assert(dest + i <= j);
            }
        }
    }
}

proof fn lemma_copy_state_is_result<T>(
    current: Seq<T>,
    original: Seq<T>,
    src_start: int,
    src_end: int,
    dest: int,
)
    requires
        0 <= src_start <= src_end <= original.len(),
        0 <= dest,
        dest + (src_end - src_start) <= original.len(),
        copy_state(
            current,
            original,
            src_start,
            dest,
            0,
            src_end - src_start,
        ),
    ensures
        current == copy_within_result(original, src_start, src_end, dest),
{
    assert(current =~= copy_within_result(original, src_start, src_end, dest)) by {
        assert forall|j: int| 0 <= j < current.len() implies
            #[trigger] current[j]
                == copy_within_result(original, src_start, src_end, dest)[j]
        by {
            if dest <= j < dest + (src_end - src_start) {
            } else {
            }
        }
    }
}

#[track_caller]
fn source_slice_copy_within<T: Copy, R: RangeBounds<usize>>(
    slice: &mut [T],
    src: R,
    dest: usize,
)
    requires
        slice_range_valid(&src, old(slice)@.len()),
        (dest as int) + (slice_range_end(&src, old(slice)@.len())
            - slice_range_start(&src)) <= old(slice)@.len(),
    ensures
        final(slice)@ == copy_within_result(
            old(slice)@,
            slice_range_start(&src),
            slice_range_end(&src, old(slice)@.len()),
            dest as int,
        ),
{
    let ghost original = slice@;
    let ghost spec_src_start = slice_range_start(&src);
    let ghost spec_src_end = slice_range_end(&src, slice@.len());

    let normalized = core::slice::range(src, ..slice.len());
    let src_start = normalized.start;
    let src_end = normalized.end;
    let count = src_end - src_start;
    if dest > slice.len() - count {
        assert(false);
        vstd::vpanic!("dest is out of bounds");
    }

    assert(src_start + count == src_end);
    assert(src_end <= slice.len());
    assert(dest + count <= slice.len());

    // `ptr::copy` is memmove; execute its overlap-safe directional cases directly.
    if dest <= src_start {
        let mut i: usize = 0;
        while i < count
            invariant
                slice@.len() == original.len(),
                src_start as int == spec_src_start,
                src_end as int == spec_src_end,
                src_start + count == src_end,
                src_end <= slice.len(),
                dest + count <= slice.len(),
                dest <= src_start,
                i <= count,
                copy_state(
                    slice@,
                    original,
                    src_start as int,
                    dest as int,
                    0,
                    i as int,
                ),
            decreases
                count - i,
        {
            let src_index = src_start + i;
            let dest_index = dest + i;
            assert(slice@[src_index as int] == original[src_index as int]) by {
                assert(!(
                    (dest as int) <= (src_index as int)
                        && (src_index as int) < (dest as int) + (i as int)
                ));
            }
            let value = slice[src_index];
            let ghost before = slice@;
            slice[dest_index] = value;
            proof {
                lemma_forward_step(
                    before,
                    original,
                    src_start as int,
                    dest as int,
                    count as int,
                    i as int,
                );
                assert(slice@ == before.update(dest_index as int, value));
            }
            i += 1;
        }
    } else {
        let mut i = count;
        while i > 0
            invariant
                slice@.len() == original.len(),
                src_start as int == spec_src_start,
                src_end as int == spec_src_end,
                src_start + count == src_end,
                src_end <= slice.len(),
                dest + count <= slice.len(),
                src_start < dest,
                i <= count,
                copy_state(
                    slice@,
                    original,
                    src_start as int,
                    dest as int,
                    i as int,
                    count as int,
                ),
            decreases
                i,
        {
            let next = i - 1;
            let src_index = src_start + next;
            let dest_index = dest + next;
            assert(slice@[src_index as int] == original[src_index as int]) by {
                assert(src_index < dest_index);
                assert(src_index < dest + i);
            }
            let value = slice[src_index];
            let ghost before = slice@;
            slice[dest_index] = value;
            proof {
                lemma_backward_step(
                    before,
                    original,
                    src_start as int,
                    dest as int,
                    count as int,
                    i as int,
                );
                assert(slice@ == before.update(dest_index as int, value));
            }
            i = next;
        }
    }

    proof {
        lemma_copy_state_is_result(
            slice@,
            original,
            src_start as int,
            src_end as int,
            dest as int,
        );
    }
}

} // verus!

fn main() {}