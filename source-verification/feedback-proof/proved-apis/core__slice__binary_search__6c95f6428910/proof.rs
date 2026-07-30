#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;
use vstd::std_specs::cmp::{OrdSpec, PartialEqSpec, PartialOrdSpec};

verus! {

pub assume_specification<'a, T, F>[ <[T]>::binary_search_by ](
    slice: &'a [T],
    f: F,
) -> (result: core::result::Result<usize, usize>)
where
    F: FnMut(&'a T) -> Ordering,
    requires
        forall|i: int| 0 <= i < slice@.len() ==>
            #[trigger] f.requires((slice@.as_ref()[i],)),
        forall|i: int, left: Ordering, right: Ordering|
            0 <= i < slice@.len()
            && f.ensures((slice@.as_ref()[i],), left)
            && f.ensures((slice@.as_ref()[i],), right) ==>
                left == right,
        forall|i: int, j: int, left: Ordering, right: Ordering|
            0 <= i < j < slice@.len()
            && f.ensures((slice@.as_ref()[i],), left)
            && f.ensures((slice@.as_ref()[j],), right) ==>
                left == Ordering::Less
                || right == Ordering::Greater
                || left == right,
    ensures
        match result {
            core::result::Result::Ok(index) => {
                &&& (index as int) < slice@.len()
                &&& f.ensures((slice@.as_ref()[index as int],), Ordering::Equal)
                &&& forall|i: int| #![auto]
                    i > index as int && slice@.len() > i ==>
                        f.ensures((slice@.as_ref()[i],), Ordering::Greater)
            },
            core::result::Result::Err(index) => {
                &&& (index as int) <= slice@.len()
                &&& forall|i: int| #![auto]
                    i >= 0 && index as int > i ==>
                        f.ensures((slice@.as_ref()[i],), Ordering::Less)
                &&& forall|i: int| #![auto]
                    i >= index as int && slice@.len() > i ==>
                        f.ensures((slice@.as_ref()[i],), Ordering::Greater)
            },
        },
;

proof fn lemma_cmp_monotone<T: core::cmp::Ord>(left: T, right: T, x: T)
    requires
        vstd::laws_cmp::obeys_cmp::<T>(),
        left.cmp_spec(&right) != Ordering::Greater,
    ensures
        left.cmp_spec(&x) == Ordering::Less
            || right.cmp_spec(&x) == Ordering::Greater
            || left.cmp_spec(&x) == right.cmp_spec(&x),
{
    reveal(vstd::laws_cmp::obeys_cmp_ord);
    reveal(vstd::laws_cmp::obeys_partial_cmp_spec_properties);
    reveal(vstd::laws_eq::obeys_eq_spec_properties);

    let l = left.cmp_spec(&x);
    let r = right.cmp_spec(&x);
    let lr = left.cmp_spec(&right);

    assert(left.partial_cmp_spec(&x) == Some(l));
    assert(right.partial_cmp_spec(&x) == Some(r));
    assert(left.partial_cmp_spec(&right) == Some(lr));

    if l == Ordering::Less {
        assert(l == Ordering::Less);
    } else if r == Ordering::Greater {
        assert(r == Ordering::Greater);
    } else if l == r {
        assert(l == r);
    } else {
        assert(l == Ordering::Equal || l == Ordering::Greater);
        assert(r == Ordering::Less || r == Ordering::Equal);
        if l == Ordering::Greater {
            if r == Ordering::Less {
                assert(x.partial_cmp_spec(&right) == Some(Ordering::Greater));
                assert(left.partial_cmp_spec(&right) == Some(Ordering::Greater));
                assert(lr == Ordering::Greater);
                assert(false);
            } else {
                assert(r == Ordering::Equal);
                assert(right.eq_spec(&x));
                assert(x.eq_spec(&right));
                assert(lr == Ordering::Less || lr == Ordering::Equal);
                if lr == Ordering::Less {
                    assert(x.partial_cmp_spec(&left) == Some(Ordering::Less));
                    assert(x.partial_cmp_spec(&right) == Some(Ordering::Less));
                    assert(x.partial_cmp_spec(&right) == Some(Ordering::Equal));
                    assert(false);
                } else {
                    assert(lr == Ordering::Equal);
                    assert(left.eq_spec(&right));
                    assert(left.eq_spec(&x));
                    assert(left.partial_cmp_spec(&x) == Some(Ordering::Equal));
                    assert(false);
                }
            }
        } else {
            assert(l == Ordering::Equal);
            assert(r == Ordering::Less);
            assert(lr == Ordering::Less || lr == Ordering::Equal);
            if lr == Ordering::Less {
                assert(left.partial_cmp_spec(&x) == Some(Ordering::Less));
                assert(false);
            } else {
                assert(lr == Ordering::Equal);
                assert(left.eq_spec(&right));
                assert(right.eq_spec(&left));
                assert(left.eq_spec(&x));
                assert(right.eq_spec(&x));
                assert(right.partial_cmp_spec(&x) == Some(Ordering::Equal));
                assert(false);
            }
        }
    }
}

pub fn source_binary_search<T: core::cmp::Ord>(
    slice: &[T],
    x: &T,
) -> (result: core::result::Result<usize, usize>)
    requires
        vstd::laws_cmp::obeys_cmp::<T>(),
        vstd::relations::sorted_by(
            slice@,
            |left: T, right: T| left.cmp_spec(&right) != Ordering::Greater,
        ),
    ensures
        match result {
            core::result::Result::Ok(index) => {
                &&& slice@.len() > index
                &&& slice@[index as int].cmp_spec(x) == Ordering::Equal
                &&& forall|i: int| #![auto] i > index as int && slice@.len() > i ==>
                    slice@[i].cmp_spec(x) == Ordering::Greater
            },
            core::result::Result::Err(index) => {
                &&& slice@.len() >= index
                &&& forall|i: int| #![auto] i >= 0 && index as int > i ==>
                    slice@[i].cmp_spec(x) == Ordering::Less
                &&& forall|i: int| #![auto] i >= index as int && slice@.len() > i ==>
                    slice@[i].cmp_spec(x) == Ordering::Greater
            },
        },
{
    proof {
        reveal(vstd::laws_cmp::obeys_cmp_ord);
        reveal(vstd::relations::sorted_by);
    }

    let f = |p: &T| -> (r: Ordering)
        ensures
            r == p.cmp_spec(x),
    {
        p.cmp(x)
    };

    proof {
        reveal(vstd::relations::sorted_by);

        assert forall|p: &T| #[trigger] f.requires((p,)) by {
            assert(f.requires((p,)));
        }
        assert forall|p: &T, r: Ordering| #[trigger] f.ensures((p,), r) implies
            r == p.cmp_spec(x) by {
            assert(r == p.cmp_spec(x));
        }

        assert forall|i: int| 0 <= i < slice@.len() implies
            #[trigger] f.requires((slice@.as_ref()[i],)) by {
            assert(f.requires((slice@.as_ref()[i],)));
        }

        assert forall|i: int, left: Ordering, right: Ordering|
            0 <= i < slice@.len()
            && f.ensures((slice@.as_ref()[i],), left)
            && f.ensures((slice@.as_ref()[i],), right) implies
                left == right by {
            assert(left == (*slice@.as_ref()[i]).cmp_spec(x));
            assert(right == (*slice@.as_ref()[i]).cmp_spec(x));
        }

        assert forall|i: int, j: int, left: Ordering, right: Ordering|
            0 <= i < j < slice@.len()
            && f.ensures((slice@.as_ref()[i],), left)
            && f.ensures((slice@.as_ref()[j],), right) implies
                left == Ordering::Less
                || right == Ordering::Greater
                || left == right by {
            assert(left == (*slice@.as_ref()[i]).cmp_spec(x));
            assert(right == (*slice@.as_ref()[j]).cmp_spec(x));
            assert((|a: T, b: T| a.cmp_spec(&b) != Ordering::Greater)(
                slice@[i],
                slice@[j],
            ));
            assert(slice@[i].cmp_spec(&slice@[j]) != Ordering::Greater);
            lemma_cmp_monotone(slice@[i], slice@[j], *x);
        }
    }

    let result = slice.binary_search_by(f);
    proof {
        match result {
            core::result::Result::Ok(index) => {
                assert((*slice@.as_ref()[index as int]).cmp_spec(x) == Ordering::Equal);
                assert(slice@[index as int].cmp_spec(x) == Ordering::Equal);
                assert forall|i: int| i > index as int && slice@.len() > i implies
                    slice@[i].cmp_spec(x) == Ordering::Greater by {
                    assert((*slice@.as_ref()[i]).cmp_spec(x) == Ordering::Greater);
                }
            },
            core::result::Result::Err(index) => {
                assert forall|i: int| i >= 0 && index as int > i implies
                    slice@[i].cmp_spec(x) == Ordering::Less by {
                    assert((*slice@.as_ref()[i]).cmp_spec(x) == Ordering::Less);
                }
                assert forall|i: int| i >= index as int && slice@.len() > i implies
                    slice@[i].cmp_spec(x) == Ordering::Greater by {
                    assert((*slice@.as_ref()[i]).cmp_spec(x) == Ordering::Greater);
                }
            },
        }
    }
    result
}

} // verus!

fn main() {}