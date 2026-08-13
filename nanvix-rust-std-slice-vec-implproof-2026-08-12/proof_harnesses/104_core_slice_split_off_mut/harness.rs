#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_off_mut
// Source: core/src/slice/mod.rs:4972-4991
// Source item sha256: e1678d19e42198d5c9fc2b61a072aa4dbc114905a60b0f55a3b44bfe37429d46
// Dependency manifest: proof_manifests/104_core_slice_split_off_mut/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub enum OneSidedRangeBound {
    StartInclusive,
    End,
    EndInclusive,
}

pub struct OneSidedRangeSpec {
    pub bound: OneSidedRangeBound,
    pub index: usize,
}

impl OneSidedRangeSpec {
    pub fn bound(self) -> (ret: (OneSidedRangeBound, usize))
        ensures ret.1 == self.index,
    {
        (self.bound, self.index)
    }
}

pub enum Direction {
    Front,
    Back,
}

pub open spec fn slice_split_off_partition<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    removed: Seq<T>,
) -> bool {
    removed + remaining == source || remaining + removed == source
}

fn split_point_of(range: OneSidedRangeSpec) -> (ret: Option<(Direction, usize)>)
{
    match range.bound() {
        (OneSidedRangeBound::StartInclusive, i) => Some((Direction::Back, i)),
        (OneSidedRangeBound::End, i) => Some((Direction::Front, i)),
        (OneSidedRangeBound::EndInclusive, i) => {
            match i.checked_add(1) {
                Some(j) => Some((Direction::Front, j)),
                None => None,
            }
        },
    }
}

pub fn split_off_mut<'a, T>(
    slice_ref: &mut &'a mut [T],
    range: OneSidedRangeSpec,
) -> (ret: Option<&'a mut [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@,
            (*final(slice_ref))@,
            ret.unwrap()@,
        ),
{
    let ghost source = (*slice_ref)@;
    let split = split_point_of(range);
    if split.is_none() {
        proof {
            assert((*slice_ref)@ == source);
        }
        return None;
    }
    let (direction, split_index) = split.unwrap();
    if split_index > (*slice_ref).len() {
        proof {
            assert((*slice_ref)@ == source);
        }
        return None;
    }

    let mut replacement: &'a mut [T] = &mut [];
    core::mem::swap(slice_ref, &mut replacement);
    let slice = replacement;
    proof {
        assert(slice@ == source);
    }

    let ghost replaced = slice@;
    let (front, back) = slice.split_at_mut(split_index);
    proof {
        assert(replaced == source);
        source.lemma_split_at(split_index as int);
        assert(front@ =~= source.subrange(0, split_index as int));
        assert(back@ =~= source.subrange(split_index as int, source.len() as int));
        assert(front@ + back@ =~= source);
    }
    match direction {
        Direction::Front => {
            let ghost removed = front@;
            let ghost remaining = back@;
            *slice_ref = back;
            proof {
                assert((*slice_ref)@ == remaining);
                assert(removed + (*slice_ref)@ =~= source);
                assert(slice_split_off_partition::<T>(source, (*slice_ref)@, removed));
            }
            Some(front)
        },
        Direction::Back => {
            let ghost removed = back@;
            let ghost remaining = front@;
            *slice_ref = front;
            proof {
                assert((*slice_ref)@ == remaining);
                assert((*slice_ref)@ + removed =~= source);
                assert(slice_split_off_partition::<T>(source, (*slice_ref)@, removed));
            }
            Some(back)
        },
    }
}

}
