#![allow(unused_imports, dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification[ <[u8]>::trim_ascii_start ](slice: &[u8]) -> (ret: &[u8])
    ensures
        slice@.len() >= ret@.len(),
        ret@ == slice@.subrange(
            slice@.len() as int - ret@.len() as int,
            slice@.len() as int,
        ),
        forall|i: int|
            i >= 0 && slice@.len() as int - ret@.len() as int > i ==> (
                slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                    || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
            ),
        ret@.len() > 0 ==> !(
            slice@[slice@.len() as int - ret@.len() as int] == 0x09u8
                || slice@[slice@.len() as int - ret@.len() as int] == 0x0au8
                || slice@[slice@.len() as int - ret@.len() as int] == 0x0cu8
                || slice@[slice@.len() as int - ret@.len() as int] == 0x0du8
                || slice@[slice@.len() as int - ret@.len() as int] == 0x20u8
        ),
;

pub assume_specification[ <[u8]>::trim_ascii_end ](slice: &[u8]) -> (ret: &[u8])
    ensures
        slice@.len() >= ret@.len(),
        ret@ == slice@.subrange(0, ret@.len() as int),
        forall|i: int| i >= ret@.len() && slice@.len() > i ==> (
            slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
        ),
        ret@.len() > 0 ==> !(
            slice@[ret@.len() - 1] == 0x09u8 || slice@[ret@.len() - 1] == 0x0au8
                || slice@[ret@.len() - 1] == 0x0cu8
                || slice@[ret@.len() - 1] == 0x0du8
                || slice@[ret@.len() - 1] == 0x20u8
        ),
;

pub fn source_trim_ascii(slice: &[u8]) -> (ret: &[u8])
    ensures
        exists|start: int, end: int|
            start >= 0
            && end >= start
            && slice@.len() >= end
            && (forall|i: int| (i >= 0 && start > i) ==> (
                slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                    || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
            ))
            && (start == slice@.len() || !(
                slice@[start] == 0x09u8 || slice@[start] == 0x0au8
                    || slice@[start] == 0x0cu8 || slice@[start] == 0x0du8
                    || slice@[start] == 0x20u8
            ))
            && (forall|i: int| (i >= end && slice@.len() > i) ==> (
                slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                    || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
            ))
            && (end == start || !(
                slice@[end - 1] == 0x09u8 || slice@[end - 1] == 0x0au8
                    || slice@[end - 1] == 0x0cu8 || slice@[end - 1] == 0x0du8
                    || slice@[end - 1] == 0x20u8
            ))
            && ret@ == slice@.subrange(start, end),
{
    let start_trimmed = slice.trim_ascii_start();
    let ret = start_trimmed.trim_ascii_end();
    proof {
        let start = slice@.len() as int - start_trimmed@.len() as int;
        let end = start + ret@.len();

        assert(start_trimmed@.len() == slice@.len() - start);
        assert(end >= start);
        assert(slice@.len() >= end);

        assert forall|i: int| i >= end && slice@.len() > i implies
            slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
        by {
            let j = i - start;
            assert(j >= ret@.len());
            assert(start_trimmed@.len() > j);
            assert(start_trimmed@[j] == slice@[i]);
        }

        assert(end == start || !(
            slice@[end - 1] == 0x09u8 || slice@[end - 1] == 0x0au8
                || slice@[end - 1] == 0x0cu8 || slice@[end - 1] == 0x0du8
                || slice@[end - 1] == 0x20u8
        )) by {
            if end != start {
                assert(ret@.len() > 0);
                assert(start_trimmed@[ret@.len() - 1] == slice@[end - 1]);
            }
        }

        assert(ret@ == slice@.subrange(start, end));
        assert(exists|start0: int, end0: int|
            start0 == start && end0 == end
            && start0 >= 0
            && end0 >= start0
            && slice@.len() >= end0
            && (forall|i: int| (i >= 0 && start0 > i) ==> (
                slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                    || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
            ))
            && (start0 == slice@.len() || !(
                slice@[start0] == 0x09u8 || slice@[start0] == 0x0au8
                    || slice@[start0] == 0x0cu8 || slice@[start0] == 0x0du8
                    || slice@[start0] == 0x20u8
            ))
            && (forall|i: int| (i >= end0 && slice@.len() > i) ==> (
                slice@[i] == 0x09u8 || slice@[i] == 0x0au8 || slice@[i] == 0x0cu8
                    || slice@[i] == 0x0du8 || slice@[i] == 0x20u8
            ))
            && (end0 == start0 || !(
                slice@[end0 - 1] == 0x09u8 || slice@[end0 - 1] == 0x0au8
                    || slice@[end0 - 1] == 0x0cu8 || slice@[end0 - 1] == 0x0du8
                    || slice@[end0 - 1] == 0x20u8
            ))
            && ret@ == slice@.subrange(start0, end0)
        );
    }
    ret
}

}

fn main() {}