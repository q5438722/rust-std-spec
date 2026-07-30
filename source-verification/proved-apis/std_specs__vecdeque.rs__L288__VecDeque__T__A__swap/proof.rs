#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::as_mut_slices ](
    v: &mut VecDeque<T, A>,
) -> (result: (&mut [T], &mut [T]))
    ensures
        result.0@ + result.1@ == old(v)@,
        final(v)@ == final(result.0)@ + final(result.1)@,
;

fn swap_in_slice<T>(slice: &mut [T], i: usize, j: usize)
    requires
        i < old(slice)@.len(),
        j < old(slice)@.len(),
    ensures
        final(slice)@ == old(slice)@.update(i as int, old(slice)@[j as int]).update(
            j as int,
            old(slice)@[i as int],
        ),
{
    if i < j {
        let ghost before = slice@;
        let (left, right) = slice.split_at_mut(j);
        core::mem::swap(&mut left[i], &mut right[0]);
        proof {
            assert(slice@ == before.update(i as int, before[j as int]).update(
                j as int,
                before[i as int],
            ));
        }
    } else if j < i {
        let ghost before = slice@;
        let (left, right) = slice.split_at_mut(i);
        core::mem::swap(&mut left[j], &mut right[0]);
        proof {
            assert(slice@ == before.update(j as int, before[i as int]).update(
                i as int,
                before[j as int],
            ));
        }
    }
}

proof fn lemma_swap_first_part<T>(a: Seq<T>, b: Seq<T>, i: int, j: int)
    requires
        0 <= i < a.len(),
        0 <= j < a.len(),
    ensures
        a.update(i, a[j]).update(j, a[i]) + b
            == (a + b).update(i, (a + b)[j]).update(j, (a + b)[i]),
{
    assert_seqs_equal!(
        a.update(i, a[j]).update(j, a[i]) + b,
        (a + b).update(i, (a + b)[j]).update(j, (a + b)[i])
    );
}

proof fn lemma_swap_second_part<T>(a: Seq<T>, b: Seq<T>, i: int, j: int)
    requires
        0 <= i < b.len(),
        0 <= j < b.len(),
    ensures
        a + b.update(i, b[j]).update(j, b[i])
            == (a + b).update(
                a.len() + i,
                (a + b)[a.len() + j],
            ).update(
                a.len() + j,
                (a + b)[a.len() + i],
            ),
{
    assert_seqs_equal!(
        a + b.update(i, b[j]).update(j, b[i]),
        (a + b).update(
            a.len() + i,
            (a + b)[a.len() + j],
        ).update(
            a.len() + j,
            (a + b)[a.len() + i],
        )
    );
}

proof fn lemma_swap_across_parts<T>(a: Seq<T>, b: Seq<T>, i: int, j: int)
    requires
        0 <= i < a.len(),
        0 <= j < b.len(),
    ensures
        a.update(i, b[j]) + b.update(j, a[i])
            == (a + b).update(
                i,
                (a + b)[a.len() + j],
            ).update(
                a.len() + j,
                (a + b)[i],
            ),
{
    assert_seqs_equal!(
        a.update(i, b[j]) + b.update(j, a[i]),
        (a + b).update(
            i,
            (a + b)[a.len() + j],
        ).update(
            a.len() + j,
            (a + b)[i],
        )
    );
}

fn swap_in_two_slices<T>(
    first: &mut [T],
    second: &mut [T],
    i: usize,
    j: usize,
)
    requires
        i < old(first)@.len() + old(second)@.len(),
        j < old(first)@.len() + old(second)@.len(),
    ensures
        final(first)@ + final(second)@
            == (old(first)@ + old(second)@).update(
                i as int,
                (old(first)@ + old(second)@)[j as int],
            ).update(
                j as int,
                (old(first)@ + old(second)@)[i as int],
            ),
{
    let ghost old_first = first@;
    let ghost old_second = second@;
    let first_len = first.len();

    if i < first_len {
        if j < first_len {
            swap_in_slice(first, i, j);
            proof {
                lemma_swap_first_part(old_first, old_second, i as int, j as int);
            }
        } else {
            let second_j = j - first_len;
            core::mem::swap(&mut first[i], &mut second[second_j]);
            proof {
                lemma_swap_across_parts(
                    old_first,
                    old_second,
                    i as int,
                    second_j as int,
                );
            }
        }
    } else {
        let second_i = i - first_len;
        if j < first_len {
            core::mem::swap(&mut second[second_i], &mut first[j]);
            proof {
                lemma_swap_across_parts(
                    old_first,
                    old_second,
                    j as int,
                    second_i as int,
                );
            }
        } else {
            let second_j = j - first_len;
            swap_in_slice(second, second_i, second_j);
            proof {
                lemma_swap_second_part(
                    old_first,
                    old_second,
                    second_i as int,
                    second_j as int,
                );
            }
        }
    }
}

fn source_vecdeque_swap<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    i: usize,
    j: usize,
)
    requires
        i < old(v)@.len(),
        j < old(v)@.len(),
    ensures
        final(v)@ == old(v)@.update(i as int, old(v)@[j as int]).update(
            j as int,
            old(v)@[i as int],
        ),
{
    if i >= v.len() {
        assert(false);
        vstd::vpanic!("assertion failed: i < self.len()");
    }
    if j >= v.len() {
        assert(false);
        vstd::vpanic!("assertion failed: j < self.len()");
    }

    let (first, second) = v.as_mut_slices();
    swap_in_two_slices(first, second, i, j);
}

} // verus!

fn main() {}