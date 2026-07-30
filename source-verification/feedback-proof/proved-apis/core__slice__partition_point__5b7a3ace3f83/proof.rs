#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::Ordering;
use core::cmp::Ordering::{Equal, Greater, Less};
use core::hint;
use core::result::Result;
use core::slice::SliceIndex;
use vstd::prelude::*;
use vstd::slice::spec_slice_get;

verus! {

pub assume_specification[
    <Ordering as PartialEq<Ordering>>::eq
](left: &Ordering, right: &Ordering) -> (result: bool)
    ensures
        result == (*left == *right),
;

pub assume_specification<T, I>[ <[T]>::get_unchecked::<I> ](
    slice: &[T],
    index: I,
) -> (output: &<I as SliceIndex<[T]>>::Output)
where
    I: SliceIndex<[T]>,
    requires
        spec_slice_get(slice, index).is_some(),
    ensures
        spec_slice_get(slice, index) == Some(output),
;

pub assume_specification<T>[ core::hint::select_unpredictable::<T> ](
    condition: bool,
    true_val: T,
    false_val: T,
) -> (result: T)
    ensures
        result == if condition { true_val } else { false_val },
;

pub assume_specification[ core::hint::assert_unchecked ](cond: bool)
    requires
        cond,
;

pub assume_specification<T, E, F>[ Result::<T, E>::unwrap_or_else ](
    result: Result<T, E>,
    op: F,
) -> (res: T)
where
    F: FnOnce(E) -> T,
    requires
        result is Err ==> op.requires((result->Err_0,)),
    ensures
        result is Ok ==> res == result->Ok_0,
        result is Err ==> op.ensures((result->Err_0,), res),
;

pub fn source_slice_partition_point<T, P>(
    slice: &[T],
    mut pred: P,
) -> (ret: usize)
where
    P: FnMut(&T) -> bool,
    requires
        forall|i: int| 0 <= i < slice@.len() ==> {
            &&& #[trigger] pred.requires((&slice@[i],))
            &&& exists|outcome: bool|
                #[trigger] pred.ensures((&slice@[i],), outcome)
        },
        forall|i: int, first: bool, second: bool|
            #![trigger pred.ensures((&slice@[i],), first),
                       pred.ensures((&slice@[i],), second)]
            0 <= i < slice@.len()
            && pred.ensures((&slice@[i],), first)
            && pred.ensures((&slice@[i],), second) ==>
                first == second,
        forall|i: int, j: int, left: bool, right: bool|
            #![trigger pred.ensures((&slice@[i],), left),
                       pred.ensures((&slice@[j],), right)]
            0 <= i < j < slice@.len()
            && pred.ensures((&slice@[i],), left)
            && pred.ensures((&slice@[j],), right) ==>
                (right ==> left),
    ensures
        (ret as int) <= slice@.len(),
        ret > 0 ==> pred.ensures((&slice@[(ret - 1) as int],), true),
        (ret as int) < slice@.len() ==>
            pred.ensures((&slice@[ret as int],), false),
{
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    let ghost initial_pred = pred;
    proof {
        assert forall|i: int| 0 <= i < slice@.len() implies {
            &&& #[trigger] initial_pred.requires((&slice@[i],))
            &&& exists|outcome: bool|
                #[trigger] initial_pred.ensures((&slice@[i],), outcome)
        } by {
            assert(pred == initial_pred);
            assert(initial_pred.requires((&slice@[i],)));
            assert(exists|outcome: bool|
                #[trigger] initial_pred.ensures((&slice@[i],), outcome));
        }
        assert forall|i: int, first: bool, second: bool|
            #![trigger initial_pred.ensures((&slice@[i],), first),
                       initial_pred.ensures((&slice@[i],), second)]
            0 <= i < slice@.len()
            && initial_pred.ensures((&slice@[i],), first)
            && initial_pred.ensures((&slice@[i],), second) implies
                first == second by {
            assert(pred == initial_pred);
            assert(pred.ensures((&slice@[i],), first));
            assert(pred.ensures((&slice@[i],), second));
        }
        assert forall|i: int, j: int, left: bool, right: bool|
            #![trigger initial_pred.ensures((&slice@[i],), left),
                       initial_pred.ensures((&slice@[j],), right)]
            0 <= i < j < slice@.len()
            && initial_pred.ensures((&slice@[i],), left)
            && initial_pred.ensures((&slice@[j],), right) implies
                (!right || left) by {
            assert(pred == initial_pred);
            assert(pred.ensures((&slice@[i],), left));
            assert(pred.ensures((&slice@[j],), right));
        }
    }
    // Inline Rust 1.96's binary_search_by and beta-reduce its comparator closure.
    let mut size = slice.len();
    let search_result = if size == 0 {
        Result::Err(0)
    } else {
        let mut base = 0usize;

        while size > 1
            invariant
                0 < size,
                base + size <= slice@.len(),
                pred == initial_pred,
                forall|i: int| 0 <= i < base as int ==>
                    initial_pred.ensures((&slice@[i],), true),
                forall|i: int| base + size <= i < slice@.len() ==>
                    initial_pred.ensures((&slice@[i],), false),
                forall|i: int| 0 <= i < slice@.len() ==> {
                    &&& #[trigger] initial_pred.requires((&slice@[i],))
                    &&& exists|outcome: bool|
                        #[trigger] initial_pred.ensures((&slice@[i],), outcome)
                },
                forall|i: int, first: bool, second: bool|
                    #![trigger initial_pred.ensures((&slice@[i],), first),
                               initial_pred.ensures((&slice@[i],), second)]
                    0 <= i < slice@.len()
                    && initial_pred.ensures((&slice@[i],), first)
                    && initial_pred.ensures((&slice@[i],), second) ==>
                        first == second,
                forall|i: int, j: int, left: bool, right: bool|
                    #![trigger initial_pred.ensures((&slice@[i],), left),
                               initial_pred.ensures((&slice@[j],), right)]
                    0 <= i < j < slice@.len()
                    && initial_pred.ensures((&slice@[i],), left)
                    && initial_pred.ensures((&slice@[j],), right) ==>
                        (right ==> left),
            decreases size,
        {
            let ghost old_base = base;
            let ghost old_size = size;
            let half = size / 2;
            proof {
                assert(0 < half < old_size);
                assert((base as int) + (half as int) < slice@.len());
                assert(slice@.len() == slice.len());
                assert((base as int) + (half as int) <= usize::MAX as int);
            }
            let mid = base + half;
            proof {
                assert(mid < slice@.len());
                assert(spec_slice_get(slice, mid).is_some());
            }
            let element = unsafe { slice.get_unchecked(mid) };
            proof {
                assert(spec_slice_get(slice, mid) == Some(element));
                assert(element == &slice@[mid as int]);
                assert(initial_pred.requires((&slice@[mid as int],)));
                assert(pred == initial_pred);
                assert(pred.requires((element,)));
            }
            let outcome = pred(element);
            let cmp = if outcome { Less } else { Greater };
            proof {
                assert(pred == initial_pred);
                assert(pred.ensures((element,), outcome));
                assert(initial_pred.ensures((element,), outcome));
                assert(initial_pred.ensures(
                    (&slice@[mid as int],),
                    outcome,
                ));
            }

            let cmp_is_greater = cmp == Greater;
            let next_base =
                hint::select_unpredictable(cmp_is_greater, base, mid);
            proof {
                assert(
                    next_base
                        == if cmp_is_greater { old_base } else { mid }
                );
            }
            base = next_base;
            size -= half;

            proof {
                assert(size == old_size - half);
                assert(half <= old_size - half <= half + 1);
                if outcome {
                    assert(cmp == Less);
                    assert(!cmp_is_greater);
                    assert(base == mid);
                } else {
                    assert(cmp == Greater);
                    assert(cmp_is_greater);
                    assert(base == old_base);
                }
                assert(base == (if !outcome { old_base } else { mid }));
                assert(base + size <= old_base + old_size);

                if outcome {
                    assert forall|i: int| 0 <= i < base as int implies
                        initial_pred.ensures((&slice@[i],), true) by {
                        if i < old_base as int {
                            assert(initial_pred.ensures((&slice@[i],), true));
                        } else {
                            assert(old_base as int <= i < mid as int);
                            assert(0 <= i < slice@.len());
                            assert(initial_pred.requires((&slice@[i],)));
                            assert(exists|left: bool|
                                #[trigger] initial_pred.ensures(
                                    (&slice@[i],),
                                    left,
                                ));
                            let left = choose|left: bool|
                                #[trigger] initial_pred.ensures(
                                    (&slice@[i],),
                                    left,
                                );
                            assert(initial_pred.ensures((&slice@[i],), left));
                            assert(initial_pred.ensures(
                                (&slice@[mid as int],),
                                outcome,
                            ));
                            assert(outcome ==> left);
                            assert(left);
                            assert(left == true);
                        }
                    }
                } else {
                    assert forall|i: int|
                        base + size <= i < slice@.len() implies
                            initial_pred.ensures((&slice@[i],), false) by {
                        if old_base + old_size <= i {
                            assert(initial_pred.ensures((&slice@[i],), false));
                        } else {
                            assert(mid as int <= i);
                            if i == mid as int {
                                assert(initial_pred.ensures(
                                    (&slice@[mid as int],),
                                    outcome,
                                ));
                                assert(outcome == false);
                            } else {
                                assert((mid as int) < i && i < slice@.len());
                                assert(0 <= i < slice@.len());
                                assert(initial_pred.requires((&slice@[i],)));
                                assert(exists|right: bool|
                                    #[trigger] initial_pred.ensures(
                                        (&slice@[i],),
                                        right,
                                    ));
                                let right = choose|right: bool|
                                    #[trigger] initial_pred.ensures(
                                        (&slice@[i],),
                                        right,
                                    );
                                assert(initial_pred.ensures(
                                    (&slice@[i],),
                                    right,
                                ));
                                assert(initial_pred.ensures(
                                    (&slice@[mid as int],),
                                    outcome,
                                ));
                                assert(right ==> outcome);
                                assert(!right);
                                assert(right == false);
                            }
                        }
                    }
                }
            }
        }

        proof {
            assert(size == 1);
            assert(base < slice@.len());
            assert(spec_slice_get(slice, base).is_some());
        }
        let element = unsafe { slice.get_unchecked(base) };
        proof {
            assert(spec_slice_get(slice, base) == Some(element));
            assert(element == &slice@[base as int]);
            assert(initial_pred.requires((&slice@[base as int],)));
            assert(pred == initial_pred);
            assert(pred.requires((element,)));
        }
        let outcome = pred(element);
        let cmp = if outcome { Less } else { Greater };
        proof {
            assert(pred == initial_pred);
            assert(pred.ensures((element,), outcome));
            assert(initial_pred.ensures((element,), outcome));
            assert(initial_pred.ensures(
                (&slice@[base as int],),
                outcome,
            ));
            assert(cmp != Equal);
        }

        let cmp_is_equal = cmp == Equal;
        if cmp_is_equal {
            proof {
                assert(false);
            }
            unsafe { hint::assert_unchecked(base < slice.len()) };
            Result::Ok(base)
        } else {
            let cmp_is_less = cmp == Less;
            let result = base + cmp_is_less as usize;
            proof {
                if outcome {
                    assert(cmp == Less);
                    assert(cmp_is_less);
                    assert(cmp_is_less as usize == 1usize);
                    assert(result == base + 1usize);
                } else {
                    assert(cmp == Greater);
                    assert(!cmp_is_less);
                    assert(cmp_is_less as usize == 0usize);
                    assert(result == base);
                }
                assert(
                    (result as int)
                        == (if outcome { (base as int) + 1 } else { base as int })
                );
                assert(result <= slice@.len());
            }
            unsafe { hint::assert_unchecked(result <= slice.len()) };
            proof {
                if outcome {
                    if (result as int) < slice@.len() {
                        assert(base + size <= result as int);
                    }
                } else {
                    if result > 0 {
                        assert(((result - 1) as int) < (base as int));
                    }
                }
            }
            Result::Err(result)
        }
    };

    proof {
        assert(search_result is Err);
        let index = search_result->Err_0;
        assert((index as int) <= slice@.len());
        if index > 0 {
            assert(initial_pred.ensures(
                (&slice@[(index - 1) as int],),
                true,
            ));
        }
        if (index as int) < slice@.len() {
            assert(initial_pred.ensures(
                (&slice@[index as int],),
                false,
            ));
        }
    }

    let identity = |i: usize| -> (out: usize)
        ensures
            out == i,
    {
        i
    };
    let ret = search_result.unwrap_or_else(identity);
    proof {
        let index = search_result->Err_0;
        assert(ret == index);
        assert((ret as int) <= slice@.len());
        if ret > 0 {
            assert(initial_pred.ensures(
                (&slice@[(ret - 1) as int],),
                true,
            ));
            assert(pred == initial_pred);
            assert(pred.ensures((&slice@[(ret - 1) as int],), true));
        }
        if (ret as int) < slice@.len() {
            assert(initial_pred.ensures((&slice@[ret as int],), false));
            assert(pred == initial_pred);
            assert(pred.ensures((&slice@[ret as int],), false));
        }
    }
    ret
}

} // verus!

fn main() {}