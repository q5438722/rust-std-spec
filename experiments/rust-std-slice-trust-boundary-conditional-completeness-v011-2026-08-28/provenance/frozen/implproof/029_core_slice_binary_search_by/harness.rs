#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::binary_search_by
// Source: core/src/slice/mod.rs:2970-3022
// Source item sha256: 8a7ce9ee452f424a23a87b3d92b45c675e3d2b4a27c219bfe45f14f1832a42b3
// Dependency manifest: proof_manifests/029_core_slice_binary_search_by/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub uninterp spec fn fnmut_ordering_observed<F, T>(
    f: F,
    value: T,
) -> core::cmp::Ordering;

pub open spec fn slice_binary_search_by_ordered<F, T>(seq: Seq<T>, f: F) -> bool {
    forall|i: int, j: int| #![auto] 0 <= i <= j < seq.len()
        ==> ordering_rank(fnmut_ordering_observed(f, seq[i]))
            <= ordering_rank(fnmut_ordering_observed(f, seq[j]))
}

pub open spec fn slice_binary_search_by_equal_at<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && fnmut_ordering_observed(f, seq[index as int]) == core::cmp::Ordering::Equal
}

pub open spec fn slice_binary_search_by_insertion_point<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| #![auto] 0 <= j < index as int
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Less
        && forall|j: int| #![auto] index as int <= j < seq.len()
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_by_result<F, T>(
    seq: Seq<T>,
    f: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_binary_search_by_ordered(seq, f) ==> match result {
        core::result::Result::Ok(index) => slice_binary_search_by_equal_at(seq, f, index),
        core::result::Result::Err(index) => slice_binary_search_by_insertion_point(seq, f, index),
    }
}

pub open spec fn binary_search_prefix_less<F, T>(seq: Seq<T>, f: F, end: int) -> bool {
    forall|j: int| #![auto] 0 <= j < end
        ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Less
}

pub open spec fn binary_search_suffix_greater<F, T>(seq: Seq<T>, f: F, start: int) -> bool {
    forall|j: int| #![auto] start <= j < seq.len()
        ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Greater
}

pub open spec fn binary_search_window_has_equal<F, T>(
    seq: Seq<T>,
    f: F,
    start: int,
    end: int,
) -> bool {
    exists|j: int| #![auto] start <= j < end
        && fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Equal
}

pub open spec fn binary_search_prefix_or_equal_window<F, T>(
    seq: Seq<T>,
    f: F,
    base: int,
    size: int,
) -> bool {
    binary_search_prefix_less(seq, f, base)
        || binary_search_window_has_equal(seq, f, base, base + size)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_sliceindex_get_unchecked_ref<'a, T>(
    slice: &'a [T],
    index: usize,
) -> (ret: &'a T)
    requires
        index < slice@.len(),
    ensures
        *ret == slice@[index as int],
{
    loop {
    }
}

pub unsafe fn get_unchecked<'a, T>(slice: &'a [T], index: usize) -> (ret: &'a T)
    requires
        index < slice@.len(),
    ensures
        *ret == slice@[index as int],
{
    unsafe { rust_1_96_sliceindex_get_unchecked_ref(slice, index) }
}

#[verifier::external_body]
pub fn rust_1_96_fnmut_ordering_observe<'a, T, F>(
    f: &mut F,
    value: &'a T,
    Ghost(observed): Ghost<core::cmp::Ordering>,
) -> (ret: core::cmp::Ordering)
    where
        F: FnMut(&'a T) -> core::cmp::Ordering,
    ensures
        ret == observed,
{
    f(value)
}

pub mod hint {
    use vstd::prelude::*;

    pub fn select_unpredictable(cond: bool, true_val: usize, false_val: usize) -> (ret: usize)
        ensures
            cond ==> ret == true_val,
            !cond ==> ret == false_val,
            ret == if cond { true_val } else { false_val },
    {
        if cond {
            true_val
        } else {
            false_val
        }
    }

    pub unsafe fn assert_unchecked(cond: bool)
        requires
            cond,
        ensures
            cond,
    {
    }
}

pub proof fn ordered_prefix_le_is_less<F, T>(seq: Seq<T>, f: F, i: int, base: usize)
    requires
        slice_binary_search_by_ordered(seq, f),
        0 <= i < base as int,
        base < seq.len(),
        fnmut_ordering_observed(f, seq[base as int]) == core::cmp::Ordering::Less,
    ensures
        fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Less,
{
    assert(ordering_rank(fnmut_ordering_observed(f, seq[i]))
        <= ordering_rank(fnmut_ordering_observed(f, seq[base as int])));
    assert(ordering_rank(fnmut_ordering_observed(f, seq[i])) <= -1);
    assert(fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Less) by {
        match fnmut_ordering_observed(f, seq[i]) {
            core::cmp::Ordering::Less => {},
            core::cmp::Ordering::Equal => {},
            core::cmp::Ordering::Greater => {},
        }
    }
}

pub proof fn ordered_suffix_ge_is_greater<F, T>(seq: Seq<T>, f: F, base: usize, i: int)
    requires
        slice_binary_search_by_ordered(seq, f),
        base < seq.len(),
        base as int <= i < seq.len(),
        fnmut_ordering_observed(f, seq[base as int]) == core::cmp::Ordering::Greater,
    ensures
        fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Greater,
{
    assert(ordering_rank(fnmut_ordering_observed(f, seq[base as int]))
        <= ordering_rank(fnmut_ordering_observed(f, seq[i])));
    assert(1 <= ordering_rank(fnmut_ordering_observed(f, seq[i])));
    assert(fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Greater) by {
        match fnmut_ordering_observed(f, seq[i]) {
            core::cmp::Ordering::Less => {},
            core::cmp::Ordering::Equal => {},
            core::cmp::Ordering::Greater => {},
        }
    }
}

pub proof fn ordered_equal_before_greater<F, T>(
    seq: Seq<T>,
    f: F,
    equal_index: int,
    greater_index: usize,
)
    requires
        slice_binary_search_by_ordered(seq, f),
        0 <= equal_index < seq.len(),
        greater_index < seq.len(),
        fnmut_ordering_observed(f, seq[equal_index]) == core::cmp::Ordering::Equal,
        fnmut_ordering_observed(f, seq[greater_index as int]) == core::cmp::Ordering::Greater,
    ensures
        equal_index < greater_index as int,
{
    if (greater_index as int) <= equal_index {
        assert(ordering_rank(fnmut_ordering_observed(f, seq[greater_index as int]))
            <= ordering_rank(fnmut_ordering_observed(f, seq[equal_index])));
        assert(false);
    }
}

pub proof fn rust_1_96_binary_search_by_loop_result<F, T>(
    seq: Seq<T>,
    f: F,
    result: core::result::Result<usize, usize>,
)
    requires
        match result {
            core::result::Result::Ok(index) => index < seq.len(),
            core::result::Result::Err(index) => index <= seq.len(),
        },
        slice_binary_search_by_ordered(seq, f) ==> match result {
            core::result::Result::Ok(index) => slice_binary_search_by_equal_at(seq, f, index),
            core::result::Result::Err(index) => {
                slice_binary_search_by_insertion_point(seq, f, index)
            },
        },
    ensures
        slice_binary_search_by_result(seq, f, result),
{
}

pub fn binary_search_by<'a, T, F>(
    slice: &'a [T],
    f: F,
) -> (result: core::result::Result<usize, usize>)
    where
        F: FnMut(&'a T) -> core::cmp::Ordering,
    ensures
        slice_binary_search_by_result(slice@, f, result),
{
    let ghost callback = f;
    let mut f = f;
    let mut size = slice.len();
    if size == 0 {
        let result = core::result::Result::Err(0usize);
        proof {
            assert(slice_binary_search_by_ordered(slice@, callback)
                ==> slice_binary_search_by_insertion_point(slice@, callback, 0usize)) by {
                if slice_binary_search_by_ordered(slice@, callback) {
                    assert forall|j: int| #![auto] 0 <= j < 0 implies fnmut_ordering_observed(
                        callback,
                        slice@[j],
                    ) == core::cmp::Ordering::Less by {
                        assert(false);
                    }
                    assert forall|j: int| #![auto] 0 <= j < slice@.len() implies fnmut_ordering_observed(
                        callback,
                        slice@[j],
                    ) == core::cmp::Ordering::Greater by {
                        assert(false);
                    }
                }
            }
            rust_1_96_binary_search_by_loop_result(slice@, callback, result);
        }
        return result;
    }
    let mut base = 0usize;
    proof {
        assert(binary_search_prefix_less(slice@, callback, 0)) by {
            assert forall|j: int| #![auto] 0 <= j < 0 implies fnmut_ordering_observed(
                callback,
                slice@[j],
            ) == core::cmp::Ordering::Less by {
                assert(false);
            }
        }
        assert(binary_search_prefix_or_equal_window(slice@, callback, 0, size as int));
        assert(binary_search_suffix_greater(slice@, callback, slice@.len() as int)) by {
            assert forall|j: int| #![auto] (slice@.len() as int) <= j < slice@.len() implies fnmut_ordering_observed(
                callback,
                slice@[j],
            ) == core::cmp::Ordering::Greater by {
                assert(false);
            }
        }
    }

    while size > 1
        invariant
            slice@.len() == slice.len(),
            0 < size,
            base < slice@.len(),
            base + size <= slice@.len(),
            slice_binary_search_by_ordered(slice@, callback) ==>
                binary_search_prefix_or_equal_window(slice@, callback, base as int, size as int),
            slice_binary_search_by_ordered(slice@, callback) ==>
                binary_search_suffix_greater(
                    slice@,
                    callback,
                    (base as int) + (size as int),
                ),
        decreases size
    {
        let ghost old_base = base;
        let ghost old_size = size;
        let half = size / 2;
        proof {
            assert(0 < half);
            assert(half < size);
            assert(half <= size - half);
            assert(slice@.len() == slice.len());
            assert(slice@.len() <= usize::MAX as int);
            assert((base as int) + (half as int) <= (base as int) + (size as int));
            assert((base as int) + (size as int) <= usize::MAX as int);
            assert((base as int) + (half as int) <= usize::MAX as int);
        }
        let mid = base + half;
        proof {
            assert(mid < base + size);
            assert(mid < slice@.len());
        }

        let value = unsafe { get_unchecked(slice, mid) };
        let ghost observed = fnmut_ordering_observed(callback, slice@[mid as int]);
        let cmp = rust_1_96_fnmut_ordering_observe(
            &mut f,
            value,
            Ghost(observed),
        );

        proof {
            assert(old_base == base);
            assert(old_size == size);
            assert((old_base as int) + (old_size as int) <= slice@.len());
            assert((old_base as int) + (half as int) == mid as int);
            assert((old_base as int) + ((old_size - half) as int)
                == (old_base as int) + (old_size as int) - (half as int));
        }
        match cmp {
            core::cmp::Ordering::Greater => {
                let new_base = hint::select_unpredictable(true, base, mid);
                proof {
                    assert(cmp == observed);
                    assert(observed == core::cmp::Ordering::Greater) by {
                        match observed {
                            core::cmp::Ordering::Less => {},
                            core::cmp::Ordering::Equal => {},
                            core::cmp::Ordering::Greater => {},
                        }
                    }
                    assert(new_base == base);
                    assert(new_base == old_base);
                    assert(fnmut_ordering_observed(callback, slice@[mid as int])
                        == core::cmp::Ordering::Greater);
                    assert((old_base as int) + ((old_size - half) as int)
                        == (old_base as int) + (old_size as int) - (half as int));
                    assert((old_base as int) + (half as int) == mid as int);
                    assert(half <= old_size - half);
                    assert((old_base as int) + (old_size as int) <= slice@.len());
                }
                proof {
                if slice_binary_search_by_ordered(slice@, callback) {
                    assert(binary_search_suffix_greater(
                        slice@,
                        callback,
                        (old_base as int) + ((old_size - half) as int),
                    )) by {
                        assert forall|j: int| #![auto]
                            (old_base as int) + ((old_size - half) as int) <= j < slice@.len()
                            implies fnmut_ordering_observed(callback, slice@[j])
                                == core::cmp::Ordering::Greater
                        by {
                            assert((mid as int) <= j);
                            ordered_suffix_ge_is_greater(slice@, callback, mid, j);
                        }
                    }
                    assert(binary_search_prefix_or_equal_window(
                        slice@,
                        callback,
                        old_base as int,
                        (old_size - half) as int,
                    )) by {
                        if binary_search_prefix_less(slice@, callback, old_base as int) {
                            assert(binary_search_prefix_less(slice@, callback, old_base as int));
                        } else {
                            assert(binary_search_window_has_equal(
                                slice@,
                                callback,
                                old_base as int,
                                (old_base as int) + (old_size as int),
                            ));
                            let equal_index = choose|j: int| #![auto] (old_base as int) <= j
                                < (old_base as int) + (old_size as int)
                                && fnmut_ordering_observed(callback, slice@[j])
                                    == core::cmp::Ordering::Equal;
                            assert((old_base as int) <= equal_index
                                < (old_base as int) + (old_size as int));
                            assert(fnmut_ordering_observed(callback, slice@[equal_index])
                                == core::cmp::Ordering::Equal);
                            ordered_equal_before_greater(slice@, callback, equal_index, mid);
                            assert(equal_index < mid as int);
                            assert(mid as int
                                <= (old_base as int) + ((old_size - half) as int));
                            assert(binary_search_window_has_equal(
                                slice@,
                                callback,
                                old_base as int,
                                (old_base as int) + ((old_size - half) as int),
                            )) by {
                                assert((old_base as int) <= equal_index
                                    < (old_base as int) + ((old_size - half) as int));
                            }
                        }
                    }
                }
                }
                base = new_base;
            },
            core::cmp::Ordering::Less => {
                let new_base = hint::select_unpredictable(false, base, mid);
                proof {
                    assert(cmp == observed);
                    assert(observed == core::cmp::Ordering::Less) by {
                        match observed {
                            core::cmp::Ordering::Less => {},
                            core::cmp::Ordering::Equal => {},
                            core::cmp::Ordering::Greater => {},
                        }
                    }
                    assert(new_base == mid);
                    assert(fnmut_ordering_observed(callback, slice@[mid as int])
                        == core::cmp::Ordering::Less);
                }
                proof {
                if slice_binary_search_by_ordered(slice@, callback) {
                    assert(binary_search_suffix_greater(
                        slice@,
                        callback,
                        (old_base as int) + (old_size as int),
                    ));
                    assert(binary_search_prefix_or_equal_window(
                        slice@,
                        callback,
                        mid as int,
                        (old_size - half) as int,
                    )) by {
                        assert(binary_search_prefix_less(slice@, callback, mid as int)) by {
                            assert forall|j: int| #![auto] 0 <= j < mid as int implies
                                fnmut_ordering_observed(callback, slice@[j])
                                    == core::cmp::Ordering::Less
                            by {
                                ordered_prefix_le_is_less(slice@, callback, j, mid);
                            }
                        }
                    }
                }
                }
                base = new_base;
            },
            core::cmp::Ordering::Equal => {
                let new_base = hint::select_unpredictable(false, base, mid);
                proof {
                    assert(cmp == observed);
                    assert(observed == core::cmp::Ordering::Equal) by {
                        match observed {
                            core::cmp::Ordering::Less => {},
                            core::cmp::Ordering::Equal => {},
                            core::cmp::Ordering::Greater => {},
                        }
                    }
                    assert(new_base == mid);
                    assert(fnmut_ordering_observed(callback, slice@[mid as int])
                        == core::cmp::Ordering::Equal);
                }
                proof {
                if slice_binary_search_by_ordered(slice@, callback) {
                    assert(binary_search_suffix_greater(
                        slice@,
                        callback,
                        (old_base as int) + (old_size as int),
                    ));
                    assert(binary_search_prefix_or_equal_window(
                        slice@,
                        callback,
                        mid as int,
                        (old_size - half) as int,
                    )) by {
                        assert(binary_search_window_has_equal(
                            slice@,
                            callback,
                            mid as int,
                            (old_base as int) + (old_size as int),
                        )) by {
                            assert((mid as int) < (old_base as int) + (old_size as int));
                            assert(fnmut_ordering_observed(callback, slice@[mid as int])
                                == core::cmp::Ordering::Equal);
                        }
                    }
                }
                }
                base = new_base;
            },
        }
        size -= half;
    }

    let value = unsafe { get_unchecked(slice, base) };
    let ghost observed = fnmut_ordering_observed(callback, slice@[base as int]);
    let cmp = rust_1_96_fnmut_ordering_observe(
        &mut f,
        value,
        Ghost(observed),
    );
    match cmp {
        core::cmp::Ordering::Equal => {
            unsafe { hint::assert_unchecked(base < slice.len()) };
            let result = core::result::Result::Ok(base);
            proof {
                assert(cmp == observed);
                assert(observed == core::cmp::Ordering::Equal) by {
                    match observed {
                        core::cmp::Ordering::Less => {},
                        core::cmp::Ordering::Equal => {},
                        core::cmp::Ordering::Greater => {},
                    }
                }
                assert(fnmut_ordering_observed(callback, slice@[base as int])
                    == core::cmp::Ordering::Equal);
                assert(slice_binary_search_by_equal_at(slice@, callback, base));
                assert(slice_binary_search_by_ordered(slice@, callback)
                    ==> slice_binary_search_by_equal_at(slice@, callback, base));
                rust_1_96_binary_search_by_loop_result(slice@, callback, result);
            }
            result
        },
        core::cmp::Ordering::Less => {
            let result_index = base + 1usize;
            proof {
                assert(base < slice@.len());
                assert(slice@.len() == slice.len());
                assert(slice@.len() <= usize::MAX as int);
                assert((base as int) + 1 <= slice@.len());
                assert((base as int) + 1 <= usize::MAX as int);
                assert(result_index <= slice@.len());
            }
            unsafe { hint::assert_unchecked(result_index <= slice.len()) };
            let result = core::result::Result::Err(result_index);
            proof {
                assert(cmp == observed);
                assert(observed == core::cmp::Ordering::Less) by {
                    match observed {
                        core::cmp::Ordering::Less => {},
                        core::cmp::Ordering::Equal => {},
                        core::cmp::Ordering::Greater => {},
                    }
                }
                assert(fnmut_ordering_observed(callback, slice@[base as int])
                    == core::cmp::Ordering::Less);
                assert(size == 1);
                assert(slice_binary_search_by_ordered(slice@, callback)
                    ==> slice_binary_search_by_insertion_point(slice@, callback, result_index)) by {
                    if slice_binary_search_by_ordered(slice@, callback) {
                        assert(result_index == base + 1);
                        assert(binary_search_suffix_greater(
                            slice@,
                            callback,
                            result_index as int,
                        ));
                        assert forall|j: int| #![auto] 0 <= j < result_index as int implies
                            fnmut_ordering_observed(callback, slice@[j])
                                == core::cmp::Ordering::Less
                        by {
                            if j < base as int {
                                ordered_prefix_le_is_less(slice@, callback, j, base);
                            } else {
                                assert(j == base as int);
                                assert(fnmut_ordering_observed(callback, slice@[base as int])
                                    == core::cmp::Ordering::Less);
                            }
                        }
                    }
                }
                rust_1_96_binary_search_by_loop_result(slice@, callback, result);
            }
            result
        },
        core::cmp::Ordering::Greater => {
            let result_index = base;
            proof {
                assert(result_index <= slice@.len());
            }
            unsafe { hint::assert_unchecked(result_index <= slice.len()) };
            let result = core::result::Result::Err(result_index);
            proof {
                assert(cmp == observed);
                assert(observed == core::cmp::Ordering::Greater) by {
                    match observed {
                        core::cmp::Ordering::Less => {},
                        core::cmp::Ordering::Equal => {},
                        core::cmp::Ordering::Greater => {},
                    }
                }
                assert(fnmut_ordering_observed(callback, slice@[base as int])
                    == core::cmp::Ordering::Greater);
                assert(size == 1);
                assert(slice_binary_search_by_ordered(slice@, callback)
                    ==> slice_binary_search_by_insertion_point(slice@, callback, result_index)) by {
                    if slice_binary_search_by_ordered(slice@, callback) {
                        assert(result_index == base);
                        if !binary_search_prefix_less(slice@, callback, base as int) {
                            assert(binary_search_window_has_equal(
                                slice@,
                                callback,
                                base as int,
                                (base as int) + (size as int),
                            ));
                            let equal_index = choose|j: int| #![auto] (base as int) <= j
                                < (base as int) + (size as int)
                                && fnmut_ordering_observed(callback, slice@[j])
                                    == core::cmp::Ordering::Equal;
                            assert((base as int) <= equal_index < (base as int) + 1);
                            assert(equal_index == base as int);
                            assert(fnmut_ordering_observed(callback, slice@[base as int])
                                == core::cmp::Ordering::Equal);
                            assert(false);
                        }
                        assert(binary_search_prefix_less(slice@, callback, base as int));
                        assert forall|j: int| #![auto] (base as int) <= j < slice@.len() implies
                            fnmut_ordering_observed(callback, slice@[j])
                                == core::cmp::Ordering::Greater
                        by {
                            ordered_suffix_ge_is_greater(slice@, callback, base, j);
                        }
                    }
                }
                rust_1_96_binary_search_by_loop_result(slice@, callback, result);
            }
            result
        },
    }
}

}
