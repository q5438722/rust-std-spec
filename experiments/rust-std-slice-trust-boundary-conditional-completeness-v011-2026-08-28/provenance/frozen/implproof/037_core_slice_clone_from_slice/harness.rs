#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::clone_from_slice
// Source: core/src/slice/mod.rs:4254-4259 and private CloneFromSpec impls at 5588-5628
// Source item sha256: 0dfc2e8b8b0a5319d883279e62986e9055b56d6ac6ba773cc4f6b9887423819b
// Dependency manifest: proof_manifests/037_core_slice_clone_from_slice/dependency_assumption_manifest.json
//
// The target now executes the Rust 1.96 default CloneFromSpec shape: equal-length
// source prefix, idx loop, and per-element clone_from. The retained boundary is
// only the lower Clone::clone_from element effect; the TrivialClone copy
// specialization remains an equivalent source-backed lower copy path.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_cloned_from<T>(src: Seq<T>, dst: Seq<T>) -> bool {
    dst == src
}

pub open spec fn slice_prefix_cloned_from<T>(dst: Seq<T>, src: Seq<T>, count: int) -> bool {
    dst.len() == src.len()
        && 0 <= count <= src.len()
        && forall|i: int| #![auto] 0 <= i < count ==> dst[i] == src[i]
}

proof fn slice_prefix_update_next<T>(
    before: Seq<T>,
    after: Seq<T>,
    src: Seq<T>,
    idx: int,
)
    requires
        slice_prefix_cloned_from(before, src, idx),
        after == before.update(idx, src[idx]),
        0 <= idx < src.len(),
    ensures
        slice_prefix_cloned_from(after, src, idx + 1),
{
    assert(after.len() == before.len());
    assert forall|i: int| 0 <= i < idx + 1 implies after[i] == src[i] by {
        if i == idx {
            assert(after[i] == src[i]);
        } else {
            assert(0 <= i < idx);
            assert(before[i] == src[i]);
            assert(after[i] == before[i]);
        }
    }
}

proof fn slice_complete_prefix_cloned_from<T>(dst: Seq<T>, src: Seq<T>)
    requires
        slice_prefix_cloned_from(dst, src, src.len() as int),
    ensures
        slice_cloned_from(src, dst),
{
    assert(dst =~= src);
}

#[verifier::external_body]
pub fn rust_1_96_clone_from_at<T: Clone>(dst: &mut [T], src: &[T], idx: usize)
    requires
        old(dst)@.len() == src@.len(),
        idx < src@.len(),
    ensures
        final(dst)@.len() == old(dst)@.len(),
        final(dst)@ == old(dst)@.update(idx as int, src@[idx as int]),
{
    dst[idx].clone_from(&src[idx]);
}

pub fn rust_1_96_equal_len_source_prefix<'b, T>(
    src: &'b [T],
    len: usize,
) -> (ret: &'b [T])
    requires
        len as nat == src@.len(),
    ensures
        ret@ == src@,
        ret@.len() == len as nat,
{
    proof {
        assert(len <= src.len());
    }
    let (ret, _empty_suffix) = src.split_at(len);
    proof {
        assert(len as int == src@.len());
        assert(ret@ == src@.subrange(0, len as int));
        assert(ret@ =~= src@);
    }
    ret
}

pub fn spec_clone_from<T: Clone>(dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        slice_cloned_from(src@, final(dst)@),
{
    let ghost source = src@;
    let len = dst.len();
    let src = rust_1_96_equal_len_source_prefix(src, len);
    proof {
        assert(src@ == source);
        assert(len as nat == source.len());
    }

    let mut idx = 0;
    while idx < dst.len()
        invariant
            dst@.len() == source.len(),
            src@ == source,
            len as nat == source.len(),
            idx <= len,
            slice_prefix_cloned_from(dst@, source, idx as int),
        decreases len - idx
    {
        proof {
            assert(idx < source.len());
        }
        let ghost before = dst@;
        rust_1_96_clone_from_at(dst, src, idx);
        proof {
            slice_prefix_update_next::<T>(before, dst@, source, idx as int);
        }
        idx = idx + 1;
    }

    proof {
        assert(idx == len);
        slice_complete_prefix_cloned_from::<T>(dst@, source);
    }
}

pub fn clone_from_slice<T: Clone>(dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        slice_cloned_from(src@, final(dst)@),
{
    spec_clone_from(dst, src);
}

}
