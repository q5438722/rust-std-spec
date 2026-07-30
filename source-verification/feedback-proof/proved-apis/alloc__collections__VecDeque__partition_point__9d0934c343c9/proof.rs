#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::vec_deque::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, P>[
    <[T]>::partition_point::<P>
](
    slice: &[T],
    pred: P,
) -> (result: usize)
where
    P: FnMut(&T) -> bool,
    requires
        forall|i: int| 0 <= i < slice@.len() ==> {
            &&& #[trigger] pred.requires((slice@.as_ref()[i],))
            &&& exists|outcome: bool|
                #[trigger] pred.ensures((slice@.as_ref()[i],), outcome)
        },
        forall|i: int, j: int, left: bool, right: bool|
            0 <= i <= j < slice@.len()
            && #[trigger] pred.ensures((slice@.as_ref()[i],), left)
            && #[trigger] pred.ensures((slice@.as_ref()[j],), right)
                ==> (right ==> left),
    ensures
        (result as int) <= slice@.len(),
        forall|i: int, outcome: bool|
            0 <= i < slice@.len()
            && #[trigger] pred.ensures((slice@.as_ref()[i],), outcome)
                ==> (outcome <==> i < result as int),
;

pub fn source_vecdeque_partition_point<T, A: Allocator, P>(
    v: &VecDeque<T, A>,
    mut pred: P,
) -> (result: usize)
where
    P: FnMut(&T) -> bool,
    requires
        forall|i: int| 0 <= i < v@.len() ==> {
            &&& #[trigger] pred.requires((v@.as_ref()[i],))
            &&& exists|outcome: bool|
                #[trigger] pred.ensures((v@.as_ref()[i],), outcome)
        },
        forall|i: int, j: int, left: bool, right: bool|
            0 <= i <= j < v@.len()
            && #[trigger] pred.ensures((v@.as_ref()[i],), left)
            && #[trigger] pred.ensures((v@.as_ref()[j],), right)
                ==> (right ==> left),
    ensures
        (result as int) <= v@.len(),
        forall|i: int, outcome: bool|
            0 <= i < v@.len()
            && #[trigger] pred.ensures((v@.as_ref()[i],), outcome)
                ==> (outcome <==> i < result as int),
{
    let (front, back) = v.as_slices();
    proof {
        vstd::slice::axiom_spec_len(front);
        vstd::slice::axiom_spec_len(back);
        vstd::std_specs::vecdeque::axiom_spec_len(v);

        assert(v@.len() == front@.len() + back@.len());

        assert forall|i: int| 0 <= i < front@.len() implies
            front@.as_ref()[i] == v@.as_ref()[i] by {
            assert((front@ + back@)[i] == front@[i]);
        }

        assert forall|i: int| 0 <= i < back@.len() implies
            back@.as_ref()[i] == v@.as_ref()[front@.len() + i] by {
            assert((front@ + back@)[front@.len() + i] == back@[i]);
        }

        assert forall|i: int| 0 <= i < front@.len() implies {
            &&& #[trigger] pred.requires((front@.as_ref()[i],))
            &&& exists|outcome: bool|
                #[trigger] pred.ensures((front@.as_ref()[i],), outcome)
        } by {
            assert(front@.as_ref()[i] == v@.as_ref()[i]);
            assert(0 <= i < v@.len());
            assert(pred.requires((v@.as_ref()[i],)));
            assert(exists|outcome: bool|
                #[trigger] pred.ensures((v@.as_ref()[i],), outcome));
        }

        assert forall|i: int, j: int, left: bool, right: bool|
            0 <= i <= j < front@.len()
            && #[trigger] pred.ensures((front@.as_ref()[i],), left)
            && #[trigger] pred.ensures((front@.as_ref()[j],), right)
                implies (!right || left) by {
            assert(front@.as_ref()[i] == v@.as_ref()[i]);
            assert(front@.as_ref()[j] == v@.as_ref()[j]);
            assert(0 <= i <= j < v@.len());
            assert(pred.ensures((v@.as_ref()[i],), left));
            assert(pred.ensures((v@.as_ref()[j],), right));
        }

        assert forall|i: int| 0 <= i < back@.len() implies {
            &&& #[trigger] pred.requires((back@.as_ref()[i],))
            &&& exists|outcome: bool|
                #[trigger] pred.ensures((back@.as_ref()[i],), outcome)
        } by {
            let k = front@.len() + i;
            assert(back@.as_ref()[i] == v@.as_ref()[k]);
            assert(0 <= k < v@.len());
            assert(pred.requires((v@.as_ref()[k],)));
            assert(exists|outcome: bool|
                #[trigger] pred.ensures((v@.as_ref()[k],), outcome));
        }

        assert forall|i: int, j: int, left: bool, right: bool|
            0 <= i <= j < back@.len()
            && #[trigger] pred.ensures((back@.as_ref()[i],), left)
            && #[trigger] pred.ensures((back@.as_ref()[j],), right)
                implies (!right || left) by {
            let ki = front@.len() + i;
            let kj = front@.len() + j;
            assert(back@.as_ref()[i] == v@.as_ref()[ki]);
            assert(back@.as_ref()[j] == v@.as_ref()[kj]);
            assert(0 <= ki <= kj < v@.len());
            assert(pred.ensures((v@.as_ref()[ki],), left));
            assert(pred.ensures((v@.as_ref()[kj],), right));
        }
    }

    let first = back.first();
    let mapped = match first {
        Some(value) => {
            proof {
                assert(back@.len() > 0);
                assert(value == back@.as_ref()[0]);
                assert(pred.requires((back@.as_ref()[0],)));
            }
            Some(pred(value))
        },
        None => None,
    };

    if let Some(true) = mapped {
        proof {
            assert(back@.len() > 0);
            assert(pred.ensures((back@.as_ref()[0],), true));
        }
        let back_result = back.partition_point(pred);
        let front_len = front.len();
        proof {
            assert((back_result as int) <= back@.len());
            assert((front_len as int) == front@.len());
            assert((front_len as int) + (back_result as int) <= v@.len());
            assert(pred.ensures((back@.as_ref()[0],), true));

            assert forall|i: int, outcome: bool|
                0 <= i < v@.len()
                && #[trigger] pred.ensures((v@.as_ref()[i],), outcome)
                    implies (
                        outcome
                            <==> i < (back_result as int) + (front_len as int)
                    ) by {
                if i < front@.len() {
                    assert(front@.as_ref()[i] == v@.as_ref()[i]);
                    assert(
                        back@.as_ref()[0]
                            == v@.as_ref()[front@.len() as int]
                    );
                    assert(
                        pred.ensures(
                            (v@.as_ref()[front@.len() as int],),
                            true,
                        )
                    );
                    assert(0 <= i <= front@.len() < v@.len());
                    assert(true ==> outcome);
                    assert(outcome);
                    assert(
                        i < (back_result as int) + (front_len as int)
                    );
                } else {
                    let j = i - front@.len();
                    assert(0 <= j < back@.len());
                    assert(back@.as_ref()[j] == v@.as_ref()[i]);
                    assert(
                        pred.ensures((back@.as_ref()[j],), outcome)
                    );
                    assert(outcome <==> j < back_result as int);
                    assert(
                        (j < back_result as int)
                            <==> i
                                < (back_result as int)
                                    + (front_len as int)
                    );
                }
            }
        }
        back_result + front_len
    } else {
        let front_result = front.partition_point(pred);
        proof {
            assert((front_result as int) <= front@.len());
            assert((front_result as int) <= v@.len());

            if back@.len() > 0 {
                assert(mapped == Some(false));
                assert(pred.ensures((back@.as_ref()[0],), false));
            }

            assert forall|i: int, outcome: bool|
                0 <= i < v@.len()
                && #[trigger] pred.ensures((v@.as_ref()[i],), outcome)
                    implies (outcome <==> i < front_result as int) by {
                if i < front@.len() {
                    assert(front@.as_ref()[i] == v@.as_ref()[i]);
                    assert(
                        pred.ensures((front@.as_ref()[i],), outcome)
                    );
                    assert(outcome <==> i < front_result as int);
                } else {
                    let j = i - front@.len();
                    assert(0 <= j < back@.len());
                    assert(back@.len() > 0);
                    assert(
                        back@.as_ref()[0]
                            == v@.as_ref()[front@.len() as int]
                    );
                    assert(
                        pred.ensures(
                            (v@.as_ref()[front@.len() as int],),
                            false,
                        )
                    );
                    assert(0 <= front@.len() <= i < v@.len());
                    assert(outcome ==> false);
                    assert(!outcome);
                    assert(front_result as int <= i);
                }
            }
        }
        front_result
    }
}

} // verus!

fn main() {}