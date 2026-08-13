#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_off
// Source: core/src/slice/mod.rs:4906-4925
// Source item sha256: fb19cd4b355c594bef6afbe10c0e9b9fc58e5aca2904b0b2038c4bf72df4768a
// Dependency manifest: proof_manifests/099_core_slice_split_off/dependency_assumption_manifest.json

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

pub fn split_off<'a, T>(
    slice_ref: &mut &'a [T],
    range: OneSidedRangeSpec,
) -> (ret: Option<&'a [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@,
            (*final(slice_ref))@,
            ret.unwrap()@,
        ),
{
    let split = split_point_of(range);
    if split.is_none() {
        return None;
    }
    let (direction, split_index) = split.unwrap();
    if split_index > (*slice_ref).len() {
        return None;
    }
    let ghost source = (*slice_ref)@;
    let (front, back) = (*slice_ref).split_at(split_index);
    proof {
        source.lemma_split_at(split_index as int);
        assert(front@ =~= source.subrange(0, split_index as int));
        assert(back@ =~= source.subrange(split_index as int, source.len() as int));
        assert(front@ + back@ =~= source);
    }
    match direction {
        Direction::Front => {
            *slice_ref = back;
            proof {
                assert((*slice_ref)@ == back@);
                assert(front@ + (*slice_ref)@ =~= source);
            }
            Some(front)
        },
        Direction::Back => {
            *slice_ref = front;
            proof {
                assert((*slice_ref)@ == front@);
                assert((*slice_ref)@ + back@ =~= source);
            }
            Some(back)
        },
    }
}

}
