use super::slice_shared::{ascii_whitespace, lowercase_byte, uppercase_byte};
use core::slice::*;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::slice::into_iter_elts;

verus! {

pub assume_specification<'a, T>[ <&'a [T] as Default>::default ]() -> (result: &'a [T])
    ensures
        result@ =~= Seq::<T>::empty(),
;

pub assume_specification<'a, T>[ <&'a mut [T] as Default>::default ]() -> (result: &'a mut [T])
    ensures
        result@ =~= Seq::<T>::empty(),
;

pub assume_specification<T>[ <[T]>::split_last ](slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        match result {
            None => slice@.len() == 0,
            Some((last, init)) => {
                &&& slice@.len() > 0
                &&& *last == slice@[slice@.len() - 1]
                &&& init@ == slice@.subrange(0, slice@.len() - 1)
            },
        },
;

pub assume_specification<T>[ <[T]>::split_last_mut ](slice: &mut [T]) -> (result: Option<
    (&mut T, &mut [T]),
>)
    ensures
        match result {
            None => old(slice)@.len() == 0 && final(slice)@ =~= seq![],
            Some((last, init)) => {
                &&& old(slice)@.len() > 0
                &&& *last == old(slice)@[old(slice)@.len() - 1]
                &&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1)
                &&& final(init)@.len() == init@.len()
                &&& final(slice)@ =~= final(init)@ + seq![*final(last)]
            },
        },
    no_unwind
;

pub assume_specification<T>[ <[T]>::split_at_unchecked ](slice: &[T], mid: usize) -> (result: (
    &[T],
    &[T],
))
    requires
        mid <= slice@.len(),
    ensures
        result.0@ == slice@.subrange(0, mid as int),
        result.1@ == slice@.subrange(mid as int, slice@.len() as int),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first ](slice: &mut &'a [T]) -> (result: Option<
    &'a T,
>)
    ensures
        match result {
            None => (*old(slice))@.len() == 0 && (*final(slice))@ =~= (*old(slice))@,
            Some(value) => {
                &&& (*old(slice))@.len() > 0
                &&& *value == (*old(slice))@[0]
                &&& (*final(slice))@ =~= (*old(slice))@.subrange(1, (*old(slice))@.len() as int)
            },
        },
    no_unwind
;

pub assume_specification<'a, T>[ <[T]>::split_off_last ](slice: &mut &'a [T]) -> (result: Option<
    &'a T,
>)
    ensures
        match result {
            None => (*old(slice))@.len() == 0 && (*final(slice))@ =~= (*old(slice))@,
            Some(value) => {
                &&& (*old(slice))@.len() > 0
                &&& *value == (*old(slice))@[(*old(slice))@.len() - 1]
                &&& (*final(slice))@ =~= (*old(slice))@.subrange(0, (*old(slice))@.len() - 1)
            },
        },
    no_unwind
;

pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ](slice: &mut &'a mut [T]) -> (result:
    Option<&'a mut T>)
    ensures
        match result {
            None => {
                &&& (*old(slice))@.len() == 0
                &&& (*final(slice))@ =~= seq![]
                &&& final(*old(slice))@ =~= seq![]
            },
            Some(value) => {
                &&& (*old(slice))@.len() > 0
                &&& *value == (*old(slice))@[0]
                &&& (*final(slice))@ == (*old(slice))@.subrange(1, (*old(slice))@.len() as int)
                &&& final(*final(slice))@.len() == (*final(slice))@.len()
                &&& final(*old(slice))@ =~= seq![*final(value)] + final(*final(slice))@
            },
        },
    no_unwind
;

pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ](slice: &mut &'a mut [T]) -> (result:
    Option<&'a mut T>)
    ensures
        match result {
            None => {
                &&& (*old(slice))@.len() == 0
                &&& (*final(slice))@ =~= seq![]
                &&& final(*old(slice))@ =~= seq![]
            },
            Some(value) => {
                &&& (*old(slice))@.len() > 0
                &&& *value == (*old(slice))@[(*old(slice))@.len() - 1]
                &&& (*final(slice))@ == (*old(slice))@.subrange(0, (*old(slice))@.len() - 1)
                &&& final(*final(slice))@.len() == (*final(slice))@.len()
                &&& final(*old(slice))@ =~= final(*final(slice))@ + seq![*final(value)]
            },
        },
    no_unwind
;

pub assume_specification[ <GetDisjointMutError as Clone>::clone ](
    value: &GetDisjointMutError,
) -> (result: GetDisjointMutError)
    ensures
        result == *value,
;

pub assume_specification[ <GetDisjointMutError as PartialEq>::eq ](
    value: &GetDisjointMutError,
    other: &GetDisjointMutError,
) -> (result: bool)
    ensures
        result == (*value == *other),
;

} // verus!
pub mod splits {
    use super::super::slice_shared::splits_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::split ](
    slice: &'a [T],
    pred: P,
) -> (out: Split<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out): (Seq<T>, P, bool, Option<usize>, State<T, P>) = (
                slice@,
                pred,
                false,
                None,
                out.state(),
            );
            out == State { v, pred, finished: inclusive && v.len() == 0, count }
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::split_mut ](
    slice: &'a mut [T],
    pred: P,
) -> (out: SplitMut<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out, owner_final, field_final): (
                Seq<T>,
                P,
                bool,
                Option<usize>,
                State<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, false, None, out.state(), final(slice)@, out.field_final());
            ({
                let (v, pred, inclusive, count, out): (
                    Seq<T>,
                    P,
                    bool,
                    Option<usize>,
                    State<T, P>,
                ) = (v, pred, inclusive, count, out);
                out == State { v, pred, finished: inclusive && v.len() == 0, count }
            }) && owner_final == field_final
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::split_inclusive ](
    slice: &'a [T],
    pred: P,
) -> (out: SplitInclusive<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out): (Seq<T>, P, bool, Option<usize>, State<T, P>) = (
                slice@,
                pred,
                true,
                None,
                out.state(),
            );
            out == State { v, pred, finished: inclusive && v.len() == 0, count }
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::split_inclusive_mut ](
    slice: &'a mut [T],
    pred: P,
) -> (out: SplitInclusiveMut<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out, owner_final, field_final): (
                Seq<T>,
                P,
                bool,
                Option<usize>,
                State<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, true, None, out.state(), final(slice)@, out.field_final());
            ({
                let (v, pred, inclusive, count, out): (
                    Seq<T>,
                    P,
                    bool,
                    Option<usize>,
                    State<T, P>,
                ) = (v, pred, inclusive, count, out);
                out == State { v, pred, finished: inclusive && v.len() == 0, count }
            }) && owner_final == field_final
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::rsplit ](
    slice: &'a [T],
    pred: P,
) -> (out: RSplit<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out): (Seq<T>, P, bool, Option<usize>, State<T, P>) = (
                slice@,
                pred,
                false,
                None,
                out.state(),
            );
            out == State { v, pred, finished: inclusive && v.len() == 0, count }
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::rsplit_mut ](
    slice: &'a mut [T],
    pred: P,
) -> (out: RSplitMut<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out, owner_final, field_final): (
                Seq<T>,
                P,
                bool,
                Option<usize>,
                State<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, false, None, out.state(), final(slice)@, out.field_final());
            ({
                let (v, pred, inclusive, count, out): (
                    Seq<T>,
                    P,
                    bool,
                    Option<usize>,
                    State<T, P>,
                ) = (v, pred, inclusive, count, out);
                out == State { v, pred, finished: inclusive && v.len() == 0, count }
            }) && owner_final == field_final
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::splitn ](
    slice: &'a [T],
    n: usize,
    pred: P,
) -> (out: SplitN<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out): (Seq<T>, P, bool, Option<usize>, State<T, P>) = (
                slice@,
                pred,
                false,
                Some(n),
                out.state(),
            );
            out == State { v, pred, finished: inclusive && v.len() == 0, count }
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::splitn_mut ](
    slice: &'a mut [T],
    n: usize,
    pred: P,
) -> (out: SplitNMut<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out, owner_final, field_final): (
                Seq<T>,
                P,
                bool,
                Option<usize>,
                State<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, false, Some(n), out.state(), final(slice)@, out.field_final());
            ({
                let (v, pred, inclusive, count, out): (
                    Seq<T>,
                    P,
                    bool,
                    Option<usize>,
                    State<T, P>,
                ) = (v, pred, inclusive, count, out);
                out == State { v, pred, finished: inclusive && v.len() == 0, count }
            }) && owner_final == field_final
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::rsplitn ](
    slice: &'a [T],
    n: usize,
    pred: P,
) -> (out: RSplitN<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out): (Seq<T>, P, bool, Option<usize>, State<T, P>) = (
                slice@,
                pred,
                false,
                Some(n),
                out.state(),
            );
            out == State { v, pred, finished: inclusive && v.len() == 0, count }
        }),
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <[T]>::rsplitn_mut ](
    slice: &'a mut [T],
    n: usize,
    pred: P,
) -> (out: RSplitNMut<'a, T, P>)
    ensures
        ({
            let (v, pred, inclusive, count, out, owner_final, field_final): (
                Seq<T>,
                P,
                bool,
                Option<usize>,
                State<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, false, Some(n), out.state(), final(slice)@, out.field_final());
            ({
                let (v, pred, inclusive, count, out): (
                    Seq<T>,
                    P,
                    bool,
                    Option<usize>,
                    State<T, P>,
                ) = (v, pred, inclusive, count, out);
                out == State { v, pred, finished: inclusive && v.len() == 0, count }
            }) && owner_final == field_final
        }),
;

} // verus!
}

pub mod chunk_by {
    use super::super::slice_shared::chunk_by_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T, P: FnMut(&T, &T) -> bool>[ <[T]>::chunk_by ](
    slice: &'a [T],
    pred: P,
) -> (result: ChunkBy<'a, T, P>)
    ensures
        ({
            let (slice, predicate, result): (Seq<T>, P, Current<T, P>) = (
                slice@,
                pred,
                result.state(),
            );
            result.slice == slice && result.predicate == predicate
        }),
;

pub assume_specification<'a, T, P: FnMut(&T, &T) -> bool>[ <[T]>::chunk_by_mut ](
    slice: &'a mut [T],
    pred: P,
) -> (result: ChunkByMut<'a, T, P>)
    ensures
        ({
            let (slice, predicate, result, owner_final, field_final): (
                Seq<T>,
                P,
                Current<T, P>,
                Seq<T>,
                Seq<T>,
            ) = (old(slice)@, pred, result.state(), final(slice)@, result.future_slice());
            ({
                let (slice, predicate, result): (Seq<T>, P, Current<T, P>) = (
                    slice,
                    predicate,
                    result,
                );
                result.slice == slice && result.predicate == predicate
            }) && owner_final == field_final
        }),
;

} // verus!
}
