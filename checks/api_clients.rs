#![feature(allocator_api)]
#[path = "../slice_mod.rs"]
pub mod slice_mod;
#[path = "../slice_non_mod.rs"]
pub mod slice_non_mod;
#[path = "../slice_shared.rs"]
pub mod slice_shared;
#[path = "../vec_mod.rs"]
pub mod vec_mod;
#[path = "../vec_non_mod.rs"]
pub mod vec_non_mod;
pub mod slice_specs {
    pub use super::slice_shared::*;
}
pub mod vec_specs {}

pub mod slice_base {
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T>() -> (result: &'a [T])
    ensures
        result@ =~= Seq::<T>::empty(),
{
    <&'a [T] as Default>::default()
}

pub fn binding_1<'a, T>() -> (result: &'a mut [T])
    ensures
        result@ =~= Seq::<T>::empty(),
{
    <&'a mut [T] as Default>::default()
}

pub fn binding_2<'a, T>(slice: &'a mut [T]) -> (result: IterMut<'a, T>)
    ensures
        IteratorSpec::remaining(&result).len() == old(slice)@.len() == final(slice)@.len(),
        forall|i: int|
            0 <= i < old(slice)@.len() ==> *IteratorSpec::remaining(&result)[i] == old(slice)@[i],
        forall|i: int|
            0 <= i < old(slice)@.len() ==> *final(IteratorSpec::remaining(&result)[i])
                == final(slice)@[i],
{
    <&'a mut [T] as IntoIterator>::into_iter(slice)
}

pub fn binding_3<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        match result {
            None => slice@.len() == 0,
            Some((last, init)) => {
                &&& slice@.len() > 0
                &&& *last == slice@[slice@.len() - 1]
                &&& init@ == slice@.subrange(0, slice@.len() - 1)
            },
        },
{
    <[T]>::split_last(slice)
}

pub fn binding_4<T>(slice: &mut [T]) -> (result: Option<(&mut T, &mut [T])>)
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
{
    <[T]>::split_last_mut(slice)
}

pub fn binding_5<T>(slice: &[T], mid: usize) -> (result: (&[T], &[T]))
    requires
        mid <= slice@.len(),
    ensures
        result.0@ == slice@.subrange(0, mid as int),
        result.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    unsafe { <[T]>::split_at_unchecked(slice, mid) }
}

pub fn binding_6<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)
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
{
    <[T]>::split_off_first(slice)
}

pub fn binding_7<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)
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
{
    <[T]>::split_off_last(slice)
}

pub fn binding_8<'a, T>(slice: &mut &'a mut [T]) -> (result: Option<&'a mut T>)
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
{
    <[T]>::split_off_first_mut(slice)
}

pub fn binding_9<'a, T>(slice: &mut &'a mut [T]) -> (result: Option<&'a mut T>)
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
{
    <[T]>::split_off_last_mut(slice)
}

pub fn binding_10(slice: &mut [u8])
    ensures
        final(slice)@ =~= old(slice)@.map_values(|byte: u8| uppercase_byte(byte)),
{
    <[u8]>::make_ascii_uppercase(slice)
}

pub fn binding_11(slice: &mut [u8])
    ensures
        final(slice)@ =~= old(slice)@.map_values(|byte: u8| lowercase_byte(byte)),
{
    <[u8]>::make_ascii_lowercase(slice)
}

pub fn binding_12(slice: &[u8], other: &[u8]) -> (result: bool)
    ensures
        result == (slice@.len() == other@.len() && forall|i: int|
            0 <= i < slice@.len() ==> lowercase_byte(#[trigger] slice@[i]) == lowercase_byte(
                other@[i],
            )),
{
    <[u8]>::eq_ignore_ascii_case(slice, other)
}

pub fn binding_13(slice: &[u8]) -> (result: &[u8])
    ensures
        ({
            let cut = slice@.len() - result@.len();
            &&& result@.len() <= slice@.len()
            &&& result@ == slice@.subrange(cut, slice@.len() as int)
            &&& forall|i: int| 0 <= i < cut ==> ascii_whitespace(#[trigger] slice@[i])
            &&& result@.len() > 0 ==> !ascii_whitespace(result@[0])
        }),
{
    <[u8]>::trim_ascii_start(slice)
}

pub fn binding_14(slice: &[u8]) -> (result: &[u8])
    ensures
        result@.len() <= slice@.len(),
        result@ == slice@.subrange(0, result@.len() as int),
        forall|i: int| result@.len() <= i < slice@.len() ==> ascii_whitespace(#[trigger] slice@[i]),
        result@.len() > 0 ==> !ascii_whitespace(result@[result@.len() - 1]),
{
    <[u8]>::trim_ascii_end(slice)
}

pub fn binding_15(slice: &[u8]) -> (result: &[u8])
    ensures
        exists|start: int|
            #![trigger slice@.subrange(start, start + result@.len())]
            {
                let end = start + result@.len();
                &&& 0 <= start
                &&& end <= slice@.len()
                &&& result@ == slice@.subrange(start, end)
                &&& forall|i: int| 0 <= i < start ==> ascii_whitespace(#[trigger] slice@[i])
                &&& forall|i: int|
                    end <= i < slice@.len() ==> ascii_whitespace(#[trigger] slice@[i])
                &&& start < slice@.len() ==> !ascii_whitespace(slice@[start])
                &&& result@.len() > 0 ==> !ascii_whitespace(result@[result@.len() - 1])
            },
{
    <[u8]>::trim_ascii(slice)
}

pub fn binding_16(value: &GetDisjointMutError) -> (result: GetDisjointMutError)
    ensures
        result == *value,
{
    <GetDisjointMutError as Clone>::clone(value)
}

pub fn binding_17(value: &GetDisjointMutError, other: &GetDisjointMutError) -> (result: bool)
    ensures
        result == (*value == *other),
{
    <GetDisjointMutError as PartialEq>::eq(value, other)
}

pub fn binding_18<'a, T>() -> (result: Iter<'a, T>)
    ensures
        IteratorSpec::remaining(&result) =~= Seq::<&'a T>::empty(),
        into_iter_elts(result) == IteratorSpec::remaining(&result).unref(),
{
    <Iter<'a, T> as Default>::default()
}

pub fn binding_19<'a, T>() -> (result: IterMut<'a, T>)
    ensures
        IteratorSpec::remaining(&result) =~= Seq::<&'a mut T>::empty(),
{
    <IterMut<'a, T> as Default>::default()
}

pub fn binding_20<'a, T>(iter: Iter<'a, T>) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
{
    <Iter<'a, T> as Iterator>::count(iter)
}

pub fn binding_21<'a, T>(iter: IterMut<'a, T>) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
{
    <IterMut<'a, T> as Iterator>::count(iter)
}

pub fn binding_22<'a, T>(iter: &Iter<'a, T>) -> (result: (usize, Option<usize>))
    ensures
        result.0 == IteratorSpec::remaining(iter).len(),
        result.1 == Some(result.0),
{
    <Iter<'a, T> as Iterator>::size_hint(iter)
}

pub fn binding_23<'a, T>(iter: &IterMut<'a, T>) -> (result: (usize, Option<usize>))
    ensures
        result.0 == IteratorSpec::remaining(iter).len(),
        result.1 == Some(result.0),
{
    <IterMut<'a, T> as Iterator>::size_hint(iter)
}

pub fn binding_24<'a, T>(iter: Iter<'a, T>) -> (result: Option<&'a T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
{
    <Iter<'a, T> as Iterator>::last(iter)
}

pub fn binding_25<'a, T>(iter: IterMut<'a, T>) -> (result: Option<&'a mut T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
{
    <IterMut<'a, T> as Iterator>::last(iter)
}

} // verus!
}
pub mod slice_ascii {
    use super::slice_specs::ascii_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use state::Parts;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0(bytes: &[u8]) -> (result: EscapeAscii<'_>)
    ensures
        ({
            let (bytes, result): (Seq<u8>, EscapeAscii<'_>) = (bytes@, result);
            ({
                let (bytes, after, remaining, lawful, terminates, has_metric): (
                    Seq<u8>,
                    Parts,
                    Seq<u8>,
                    bool,
                    bool,
                    bool,
                ) = (
                    bytes,
                    parts::view(result),
                    IteratorSpec::remaining(&result),
                    IteratorSpec::obeys_prophetic_iter_laws(&result),
                    IteratorSpec::will_return_none(&result),
                    IteratorSpec::decrease(&result) is Some,
                );
                &&& ({
                    let (bytes, after): (Seq<u8>, Parts) = (bytes, after);
                    after == state::initial(bytes)
                })
                &&& ({
                    let (bytes, remaining, lawful, terminates, has_metric): (
                        Seq<u8>,
                        Seq<u8>,
                        bool,
                        bool,
                        bool,
                    ) = (bytes, remaining, lawful, terminates, has_metric);
                    remaining == values::escaped(bytes) && lawful && terminates && has_metric
                })
            })
        }),
{
    <[u8]>::escape_ascii(bytes)
}

pub fn binding_1<'a>(iter: &mut EscapeAscii<'a>) -> (result: Option<u8>)
    ensures
        ({
            let (before, after, result): (Parts, Parts, Option<u8>) = (
                parts::view(*old(iter)),
                parts::view(*final(iter)),
                result,
            );
            &&& after == state::front_parts(before)
            &&& ({
                let (before, after, result): (Seq<u8>, Seq<u8>, Option<u8>) = (
                    state::contents(before),
                    state::contents(after),
                    result,
                );
                if before.len() == 0 {
                    result == None && after == before
                } else {
                    result == Some(before[0]) && after == before.drop_first()
                }
            })
        }),
{
    <EscapeAscii<'a> as Iterator>::next(iter)
}

pub fn binding_2<'a>(iter: &mut EscapeAscii<'a>) -> (result: Option<u8>)
    ensures
        ({
            let (before, after, result): (Parts, Parts, Option<u8>) = (
                parts::view(*old(iter)),
                parts::view(*final(iter)),
                result,
            );
            &&& after == state::back_parts(before)
            &&& ({
                let (before, after, result): (Seq<u8>, Seq<u8>, Option<u8>) = (
                    state::contents(before),
                    state::contents(after),
                    result,
                );
                if before.len() == 0 {
                    result == None && after == before
                } else {
                    result == Some(before.last()) && after == before.drop_last()
                }
            })
        }),
{
    <EscapeAscii<'a> as DoubleEndedIterator>::next_back(iter)
}

pub fn binding_3<'a>(iter: EscapeAscii<'a>) -> (result: Option<u8>)
    ensures
        ({
            let (before, remaining, result): (Parts, Seq<u8>, Option<u8>) = (
                parts::view(iter),
                IteratorSpec::remaining(&iter),
                result,
            );
            &&& remaining == state::contents(before)
            &&& ({
                let (before, result): (Parts, Option<u8>) = (before, result);
                ({
                    let (before, result): (Seq<u8>, Option<u8>) = (state::contents(before), result);
                    result == if before.len() == 0 {
                        None
                    } else {
                        Some(before.last())
                    }
                })
            })
            &&& ({
                let (before, result): (Seq<u8>, Option<u8>) = (remaining, result);
                result == if before.len() == 0 {
                    None
                } else {
                    Some(before.last())
                }
            })
        }),
{
    <EscapeAscii<'a> as Iterator>::last(iter)
}

pub fn binding_4<'a>(iter: &EscapeAscii<'a>) -> (result: (usize, Option<usize>))
    ensures
        ({
            let (before, remaining, result): (Parts, Seq<u8>, (usize, Option<usize>)) = (
                parts::view(*iter),
                IteratorSpec::remaining(iter),
                result,
            );
            &&& remaining == state::contents(before)
            &&& ({
                let (before, result): (Parts, (usize, Option<usize>)) = (before, result);
                result == values::hint_from_parts(before.0, before.1, before.2)
            })
            &&& ({
                let (remaining, result): (Seq<u8>, (usize, Option<usize>)) = (remaining, result);
                &&& result.0 <= remaining.len()
                &&& match result.1 {
                    Some(upper) => result.0 == upper && upper == remaining.len(),
                    None => result.0 < remaining.len(),
                }
            })
        }),
{
    <EscapeAscii<'a> as Iterator>::size_hint(iter)
}

} // verus!
}
pub mod slice_splits {
    use super::slice_specs::splits_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T, P: FnMut(&T) -> bool>(slice: &'a [T], pred: P) -> (out: Split<'a, T, P>)
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
{
    <[T]>::split(slice, pred)
}

pub fn binding_1<'a, T, P: FnMut(&T) -> bool>(slice: &'a mut [T], pred: P) -> (out: SplitMut<
    'a,
    T,
    P,
>)
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
{
    <[T]>::split_mut(slice, pred)
}

pub fn binding_2<'a, T, P: FnMut(&T) -> bool>(slice: &'a [T], pred: P) -> (out: SplitInclusive<
    'a,
    T,
    P,
>)
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
{
    <[T]>::split_inclusive(slice, pred)
}

pub fn binding_3<'a, T, P: FnMut(&T) -> bool>(slice: &'a mut [T], pred: P) -> (out:
    SplitInclusiveMut<'a, T, P>)
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
{
    <[T]>::split_inclusive_mut(slice, pred)
}

pub fn binding_4<'a, T, P: FnMut(&T) -> bool>(slice: &'a [T], pred: P) -> (out: RSplit<'a, T, P>)
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
{
    <[T]>::rsplit(slice, pred)
}

pub fn binding_5<'a, T, P: FnMut(&T) -> bool>(slice: &'a mut [T], pred: P) -> (out: RSplitMut<
    'a,
    T,
    P,
>)
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
{
    <[T]>::rsplit_mut(slice, pred)
}

pub fn binding_6<'a, T, P: FnMut(&T) -> bool>(slice: &'a [T], n: usize, pred: P) -> (out: SplitN<
    'a,
    T,
    P,
>)
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
{
    <[T]>::splitn(slice, n, pred)
}

pub fn binding_7<'a, T, P: FnMut(&T) -> bool>(slice: &'a mut [T], n: usize, pred: P) -> (out:
    SplitNMut<'a, T, P>)
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
{
    <[T]>::splitn_mut(slice, n, pred)
}

pub fn binding_8<'a, T, P: FnMut(&T) -> bool>(slice: &'a [T], n: usize, pred: P) -> (out: RSplitN<
    'a,
    T,
    P,
>)
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
{
    <[T]>::rsplitn(slice, n, pred)
}

pub fn binding_9<'a, T, P: FnMut(&T) -> bool>(slice: &'a mut [T], n: usize, pred: P) -> (out:
    RSplitNMut<'a, T, P>)
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
{
    <[T]>::rsplitn_mut(slice, n, pred)
}

pub fn binding_10<'a, T, P: FnMut(&T) -> bool>(iter: &SplitInclusive<'a, T, P>) -> (out: (
    usize,
    Option<usize>,
))
    ensures
        ({
            let (s, inclusive, result): (State<T, P>, bool, (usize, Option<usize>)) = (
                iter.state(),
                true,
                out,
            );
            let hint = ({
                let (s, inclusive): (State<T, P>, bool) = (s, inclusive);
                if s.finished {
                    (0, Some(0))
                } else if inclusive {
                    (
                        1,
                        Some(
                            if s.v.len() == 0 {
                                1
                            } else {
                                s.v.len() as usize
                            },
                        ),
                    )
                } else {
                    // Normal-return observation of len + 1. Checked overflow cannot return;
                    // an unchecked usize addition wraps. The source safety proof is separate.
                    (
                        1,
                        Some(
                            if s.v.len() == usize::MAX {
                                0
                            } else {
                                (s.v.len() + 1) as usize
                            },
                        ),
                    )
                }
            });
            result == match s.count {
                None => hint,
                Some(count) => (
                    if count < hint.0 {
                        count
                    } else {
                        hint.0
                    },
                    Some(
                        match hint.1 {
                            None => count,
                            Some(upper) => if count < upper {
                                count
                            } else {
                                upper
                            },
                        },
                    ),
                ),
            }
        }),
{
    <SplitInclusive<'a, T, P> as Iterator>::size_hint(iter)
}

pub fn binding_11<'a, T, P: FnMut(&T) -> bool>(iter: &SplitInclusiveMut<'a, T, P>) -> (out: (
    usize,
    Option<usize>,
))
    ensures
        ({
            let (s, inclusive, result): (State<T, P>, bool, (usize, Option<usize>)) = (
                iter.state(),
                true,
                out,
            );
            let hint = ({
                let (s, inclusive): (State<T, P>, bool) = (s, inclusive);
                if s.finished {
                    (0, Some(0))
                } else if inclusive {
                    (
                        1,
                        Some(
                            if s.v.len() == 0 {
                                1
                            } else {
                                s.v.len() as usize
                            },
                        ),
                    )
                } else {
                    // Normal-return observation of len + 1. Checked overflow cannot return;
                    // an unchecked usize addition wraps. The source safety proof is separate.
                    (
                        1,
                        Some(
                            if s.v.len() == usize::MAX {
                                0
                            } else {
                                (s.v.len() + 1) as usize
                            },
                        ),
                    )
                }
            });
            result == match s.count {
                None => hint,
                Some(count) => (
                    if count < hint.0 {
                        count
                    } else {
                        hint.0
                    },
                    Some(
                        match hint.1 {
                            None => count,
                            Some(upper) => if count < upper {
                                count
                            } else {
                                upper
                            },
                        },
                    ),
                ),
            }
        }),
{
    <SplitInclusiveMut<'a, T, P> as Iterator>::size_hint(iter)
}

} // verus!
}
pub mod slice_chunk_by {
    use super::slice_specs::chunk_by_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T, P: FnMut(&T, &T) -> bool>(slice: &'a [T], pred: P) -> (result: ChunkBy<
    'a,
    T,
    P,
>)
    ensures
        ({
            let (slice, predicate, result): (Seq<T>, P, Current<T, P>) = (
                slice@,
                pred,
                result.state(),
            );
            result.slice == slice && result.predicate == predicate
        }),
{
    <[T]>::chunk_by(slice, pred)
}

pub fn binding_1<'a, T, P: FnMut(&T, &T) -> bool>(slice: &'a mut [T], pred: P) -> (result:
    ChunkByMut<'a, T, P>)
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
{
    <[T]>::chunk_by_mut(slice, pred)
}

pub fn binding_2<'a, T: 'a, P: FnMut(&T, &T) -> bool>(iter: &ChunkBy<'a, T, P>) -> (result: (
    usize,
    Option<usize>,
))
    ensures
        ({
            let (state, result): (Current<T, P>, (usize, Option<usize>)) = (iter.state(), result);
            result == if state.slice.len() == 0 {
                (0usize, Some(0usize))
            } else {
                (1usize, Some(state.slice.len() as usize))
            }
        }),
{
    <ChunkBy<'a, T, P> as Iterator>::size_hint(iter)
}

pub fn binding_3<'a, T: 'a, P: FnMut(&T, &T) -> bool>(iter: &ChunkByMut<'a, T, P>) -> (result: (
    usize,
    Option<usize>,
))
    ensures
        ({
            let (state, result): (Current<T, P>, (usize, Option<usize>)) = (iter.state(), result);
            result == if state.slice.len() == 0 {
                (0usize, Some(0usize))
            } else {
                (1usize, Some(state.slice.len() as usize))
            }
        }),
{
    <ChunkByMut<'a, T, P> as Iterator>::size_hint(iter)
}

} // verus!
}
pub mod slice_chunks {
    use super::slice_specs::chunks_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T>(iter: &Chunks<'a, T>) -> (result: Chunks<'a, T>)
    ensures
        result == *iter,
{
    <Chunks<'a, T> as Clone>::clone(iter)
}

pub fn binding_1<'a, T>(iter: &ChunksExact<'a, T>) -> (result: ChunksExact<'a, T>)
    ensures
        result == *iter,
{
    <ChunksExact<'a, T> as Clone>::clone(iter)
}

pub fn binding_2<'a, T>(iter: &ChunksExact<'a, T>) -> (result: &'a [T])
    ensures
        ({
            let (before, item): (State<T>, Seq<T>) = (iter.state(), result@);
            item == before.rem
        }),
{
    <ChunksExact<'a, T>>::remainder(iter)
}

pub fn binding_3<'a, T>(iter: &RChunks<'a, T>) -> (result: RChunks<'a, T>)
    ensures
        result == *iter,
{
    <RChunks<'a, T> as Clone>::clone(iter)
}

pub fn binding_4<'a, T>(iter: &RChunksExact<'a, T>) -> (result: RChunksExact<'a, T>)
    ensures
        result == *iter,
{
    <RChunksExact<'a, T> as Clone>::clone(iter)
}

pub fn binding_5<'a, T>(iter: &RChunksExact<'a, T>) -> (result: &'a [T])
    ensures
        ({
            let (before, item): (State<T>, Seq<T>) = (iter.state(), result@);
            item == before.rem
        }),
{
    <RChunksExact<'a, T>>::remainder(iter)
}

} // verus!
}
pub mod slice_arrays {
    use super::slice_specs::arrays_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T, const N: usize>(iter: &ArrayWindows<'a, T, N>) -> (result: ArrayWindows<
    'a,
    T,
    N,
>)
    ensures
        result == *iter,
        result.remaining() == iter.remaining(),
        result.obeys_prophetic_iter_laws() == iter.obeys_prophetic_iter_laws(),
        result.will_return_none() == iter.will_return_none(),
        result.decrease() == iter.decrease(),
{
    <ArrayWindows<'a, T, N> as Clone>::clone(iter)
}

} // verus!
}
pub mod slice_windows {
    use super::slice_specs::windows_model::*;
    use super::slice_specs::*;
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::slice::into_iter_elts;
    verus! {

pub fn binding_0<'a, T>(iter: &Windows<'a, T>) -> (result: Windows<'a, T>)
    ensures
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                iter@,
                IteratorSpec::remaining(iter),
                IteratorSpec::obeys_prophetic_iter_laws(iter),
                IteratorSpec::will_return_none(iter),
                IteratorSpec::decrease(iter),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                result@,
                IteratorSpec::remaining(&result),
                IteratorSpec::obeys_prophetic_iter_laws(&result),
                IteratorSpec::will_return_none(&result),
                IteratorSpec::decrease(&result),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (before, result): (State<T>, State<T>) = (iter@, result@);
            result.v == before.v && result.width == before.width
        }),
        result.remaining() == iter.remaining(),
{
    <Windows<'a, T> as Clone>::clone(iter)
}

pub fn binding_1<'a, T>(iter: &mut Windows<'a, T>) -> (result: Option<&'a [T]>)
    ensures
        valid(old(iter)@),
        valid(final(iter)@),
        ({
            let (before, after, result): (State<T>, State<T>, Option<Seq<T>>) = (
                old(iter)@,
                final(iter)@,
                option_values(result),
            );
            after.width == before.width && if before.width > before.v.len() {
                result == None && after.v == before.v
            } else {
                result == Some(before.v.subrange(0, before.width as int)) && after.v
                    == before.v.subrange(1, before.v.len() as int)
            }
        }),
{
    <Windows<'a, T> as Iterator>::next(iter)
}

pub fn binding_2<'a, T>(iter: &mut Windows<'a, T>, n: usize) -> (result: Option<
    <Windows<'a, T> as Iterator>::Item,
>)
    ensures
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                old(iter)@,
                IteratorSpec::remaining(old(iter)),
                IteratorSpec::obeys_prophetic_iter_laws(old(iter)),
                IteratorSpec::will_return_none(old(iter)),
                IteratorSpec::decrease(old(iter)),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                final(iter)@,
                IteratorSpec::remaining(final(iter)),
                IteratorSpec::obeys_prophetic_iter_laws(final(iter)),
                IteratorSpec::will_return_none(final(iter)),
                IteratorSpec::decrease(final(iter)),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (before, n, after, result): (State<T>, usize, State<T>, Option<Seq<T>>) = (
                old(iter)@,
                n,
                final(iter)@,
                option_values(result),
            );
            after.width == before.width && if n < values(before).len() {
                result == Some(before.v.subrange(n as int, n as int + before.width)) && after.v
                    == before.v.subrange(n as int + 1, before.v.len() as int)
            } else {
                result == None && after.v == Seq::<T>::empty()
            }
        }),
{
    <Windows<'a, T> as Iterator>::nth(iter, n)
}

pub fn binding_3<'a, T>(iter: &mut Windows<'a, T>) -> (result: Option<
    <Windows<'a, T> as Iterator>::Item,
>)
    ensures
        valid(old(iter)@),
        valid(final(iter)@),
        ({
            let (before, after, result): (State<T>, State<T>, Option<Seq<T>>) = (
                old(iter)@,
                final(iter)@,
                option_values(result),
            );
            ({
                let (before, n, after, result): (State<T>, usize, State<T>, Option<Seq<T>>) = (
                    before,
                    0,
                    after,
                    result,
                );
                after.width == before.width && if n < values(before).len() {
                    let end = before.v.len() - n;
                    result == Some(before.v.subrange(end - before.width, end)) && after.v
                        == before.v.subrange(0, end - 1)
                } else {
                    result == None && after.v == Seq::<T>::empty()
                }
            })
        }),
{
    <Windows<'a, T> as DoubleEndedIterator>::next_back(iter)
}

pub fn binding_4<'a, T>(iter: &mut Windows<'a, T>, n: usize) -> (result: Option<
    <Windows<'a, T> as Iterator>::Item,
>)
    ensures
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                old(iter)@,
                IteratorSpec::remaining(old(iter)),
                IteratorSpec::obeys_prophetic_iter_laws(old(iter)),
                IteratorSpec::will_return_none(old(iter)),
                IteratorSpec::decrease(old(iter)),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (state, items, obeys, terminates, metric): (
                State<T>,
                Seq<&'a [T]>,
                bool,
                bool,
                Option<nat>,
            ) = (
                final(iter)@,
                IteratorSpec::remaining(final(iter)),
                IteratorSpec::obeys_prophetic_iter_laws(final(iter)),
                IteratorSpec::will_return_none(final(iter)),
                IteratorSpec::decrease(final(iter)),
            );
            &&& valid(state)
            &&& items == remaining(state)
            &&& obeys
            &&& terminates
            &&& metric is Some
        }),
        ({
            let (before, n, after, result): (State<T>, usize, State<T>, Option<Seq<T>>) = (
                old(iter)@,
                n,
                final(iter)@,
                option_values(result),
            );
            after.width == before.width && if n < values(before).len() {
                let end = before.v.len() - n;
                result == Some(before.v.subrange(end - before.width, end)) && after.v
                    == before.v.subrange(0, end - 1)
            } else {
                result == None && after.v == Seq::<T>::empty()
            }
        }),
{
    <Windows<'a, T> as DoubleEndedIterator>::nth_back(iter, n)
}

pub fn binding_5<'a, T>(iter: Windows<'a, T>) -> (result: usize)
    ensures
        ({
            let (state, items): (State<T>, Seq<&'a [T]>) = (iter@, IteratorSpec::remaining(&iter));
            valid(state) && items == remaining(state)
        }),
        ({
            let (before, result): (State<T>, usize) = (iter@, result);
            result == values(before).len()
        }),
{
    <Windows<'a, T> as Iterator>::count(iter)
}

pub fn binding_6<'a, T>(iter: Windows<'a, T>) -> (result: Option<
    <Windows<'a, T> as Iterator>::Item,
>)
    ensures
        ({
            let (state, items): (State<T>, Seq<&'a [T]>) = (iter@, IteratorSpec::remaining(&iter));
            valid(state) && items == remaining(state)
        }),
        ({
            let (before, result): (State<T>, Option<Seq<T>>) = (iter@, option_values(result));
            if before.width > before.v.len() {
                result == None
            } else {
                result == Some(
                    before.v.subrange(before.v.len() - before.width, before.v.len() as int),
                )
            }
        }),
{
    <Windows<'a, T> as Iterator>::last(iter)
}

pub fn binding_7<'a, T>(iter: &Windows<'a, T>) -> (result: (usize, Option<usize>))
    ensures
        ({
            let (state, items): (State<T>, Seq<&'a [T]>) = (iter@, IteratorSpec::remaining(iter));
            valid(state) && items == remaining(state)
        }),
        ({
            let (before, result): (State<T>, (usize, Option<usize>)) = (iter@, result);
            result.0 == values(before).len() && result.1 == Some(result.0)
        }),
{
    <Windows<'a, T> as Iterator>::size_hint(iter)
}

} // verus!
}
pub mod vec_base {
    use core::alloc::Allocator;
    use core::slice::*;
    use std::borrow::Cow;
    use std::vec::IntoIter;
    use vstd::prelude::*;
    use vstd::std_specs::cmp::PartialEqSpec;
    use vstd::std_specs::iter::IteratorSpec;
    use vstd::std_specs::vec::into_iter_elts;
    verus! {

pub fn binding_0<'a, T: Clone>(slice: &'a [T]) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == slice@,
            Cow::Owned(_) => false,
        },
{
    <Cow<'a, [T]> as From<&'a [T]>>::from(slice)
}

pub fn binding_1<'a, T: Clone, const N: usize>(array: &'a [T; N]) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == array@,
            Cow::Owned(_) => false,
        },
{
    <Cow<'a, [T]> as From<&'a [T; N]>>::from(array)
}

pub fn binding_2<'a, T: Clone>(vec: Vec<T>) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(_) => false,
            Cow::Owned(contents) => contents@ == vec@,
        },
{
    <Cow<'a, [T]> as From<Vec<T>>>::from(vec)
}

pub fn binding_3<'a, T: Clone>(vec: &'a Vec<T>) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == vec@,
            Cow::Owned(_) => false,
        },
{
    <Cow<'a, [T]> as From<&'a Vec<T>>>::from(vec)
}

pub fn binding_4<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>) -> (iter: <&'a mut Vec<
    T,
    A,
> as IntoIterator>::IntoIter)
    ensures
        IteratorSpec::remaining(&iter).len() == old(vec)@.len() == final(vec)@.len(),
        forall|i: int|
            #![trigger IteratorSpec::remaining(&iter)[i]]
            0 <= i < old(vec)@.len() ==> *IteratorSpec::remaining(&iter)[i] == old(vec)@[i],
        forall|i: int|
            #![trigger IteratorSpec::remaining(&iter)[i]]
            #![trigger final(vec)@[i]]
            0 <= i < old(vec)@.len() ==> *final(IteratorSpec::remaining(&iter)[i])
                == final(vec)@[i],
        IteratorSpec::decrease(&iter) is Some,
{
    <&'a mut Vec<T, A> as IntoIterator>::into_iter(vec)
}

pub fn binding_5<'a, T, A: Allocator>(vec: &'a Vec<T, A>) -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
{
    <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref(vec)
}

pub fn binding_6<'a, T, A: Allocator>(vec: &'a Vec<T, A>) -> (result: &'a [T])
    ensures
        result@ == vec@,
{
    <Vec<T, A> as AsRef<[T]>>::as_ref(vec)
}

pub fn binding_7<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        *final(result) == *final(vec),
{
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut(vec)
}

pub fn binding_8<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>) -> (result: &'a mut [T])
    ensures
        result@ == old(vec)@,
        final(result)@ == final(vec)@,
{
    <Vec<T, A> as AsMut<[T]>>::as_mut(vec)
}

pub fn binding_9<T, const N: usize>(array: [T; N]) -> (result: Vec<T>)
    ensures
        result@ == array@,
{
    <Vec<T> as From<[T; N]>>::from(array)
}

pub fn binding_10<T, A: Allocator>(slice: Box<[T], A>) -> (result: Vec<T, A>)
    ensures
        result@ == slice@,
{
    <Vec<T, A> as From<Box<[T], A>>>::from(slice)
}

pub fn binding_11<T, A: Allocator + Default>() -> (iter: IntoIter<T, A>)
    ensures
        IteratorSpec::remaining(&iter) == Seq::<T>::empty(),
        IteratorSpec::decrease(&iter) is Some,
        into_iter_elts(iter) == IteratorSpec::remaining(&iter),
{
    <IntoIter<T, A> as Default>::default()
}

pub fn binding_12<T, A: Allocator>(iter: IntoIter<T, A>) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
{
    <IntoIter<T, A> as Iterator>::count(iter)
}

pub fn binding_13<T, A: Allocator>(iter: IntoIter<T, A>) -> (result: Option<T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
{
    <IntoIter<T, A> as Iterator>::last(iter)
}

pub fn binding_14<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &Vec<T, A>,
    right: &&[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&[U]>>::eq(left, right)
}

pub fn binding_15<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &Vec<T, A>,
    right: &&[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&[U]>>::ne(left, right)
}

pub fn binding_16<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &Vec<T, A>,
    right: &&mut [U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = old(*right)@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&mut [U]>>::eq(left, right)
}

pub fn binding_17<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &Vec<T, A>,
    right: &&mut [U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = old(*right)@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&mut [U]>>::ne(left, right)
}

pub fn binding_18<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &&'spec0 [T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <&'spec0 [T] as PartialEq<Vec<U, A>>>::eq(left, right)
}

pub fn binding_19<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &&'spec0 [T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <&'spec0 [T] as PartialEq<Vec<U, A>>>::ne(left, right)
}

pub fn binding_20<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &&'spec0 mut [T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = old(*left)@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <&'spec0 mut [T] as PartialEq<Vec<U, A>>>::eq(left, right)
}

pub fn binding_21<'spec0, T: PartialEq<U>, U, A: Allocator>(
    left: &&'spec0 mut [T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = old(*left)@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <&'spec0 mut [T] as PartialEq<Vec<U, A>>>::ne(left, right)
}

pub fn binding_22<T: PartialEq<U>, U, A: Allocator>(left: &Vec<T, A>, right: &[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<[U]>>::eq(left, right)
}

pub fn binding_23<T: PartialEq<U>, U, A: Allocator>(left: &Vec<T, A>, right: &[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<[U]>>::ne(left, right)
}

pub fn binding_24<T: PartialEq<U>, U, A: Allocator>(left: &[T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <[T] as PartialEq<Vec<U, A>>>::eq(left, right)
}

pub fn binding_25<T: PartialEq<U>, U, A: Allocator>(left: &[T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <[T] as PartialEq<Vec<U, A>>>::ne(left, right)
}

pub fn binding_26<'spec0, T: PartialEq<U> + Clone, U, A: Allocator>(
    left: &Cow<'spec0, [T]>,
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec0, [T]> as PartialEq<Vec<U, A>>>::eq(left, right)
}

pub fn binding_27<'spec0, T: PartialEq<U> + Clone, U, A: Allocator>(
    left: &Cow<'spec0, [T]>,
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec0, [T]> as PartialEq<Vec<U, A>>>::ne(left, right)
}

pub fn binding_28<'spec0, 'spec1, T: PartialEq<U> + Clone, U>(
    left: &Cow<'spec1, [T]>,
    right: &&[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec1, [T]> as PartialEq<&[U]>>::eq(left, right)
}

pub fn binding_29<'spec0, 'spec1, T: PartialEq<U> + Clone, U>(
    left: &Cow<'spec1, [T]>,
    right: &&[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec1, [T]> as PartialEq<&[U]>>::ne(left, right)
}

pub fn binding_30<'spec0, 'spec1, T: PartialEq<U> + Clone, U>(
    left: &Cow<'spec1, [T]>,
    right: &&mut [U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = old(*right)@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec1, [T]> as PartialEq<&mut [U]>>::eq(left, right)
}

pub fn binding_31<'spec0, 'spec1, T: PartialEq<U> + Clone, U>(
    left: &Cow<'spec1, [T]>,
    right: &&mut [U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = old(*right)@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Cow<'spec1, [T]> as PartialEq<&mut [U]>>::ne(left, right)
}

pub fn binding_32<T: PartialEq<U>, U, A: Allocator, const N: usize>(
    left: &Vec<T, A>,
    right: &[U; N],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<[U; N]>>::eq(left, right)
}

pub fn binding_33<T: PartialEq<U>, U, A: Allocator, const N: usize>(
    left: &Vec<T, A>,
    right: &[U; N],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<[U; N]>>::ne(left, right)
}

pub fn binding_34<'spec0, T: PartialEq<U>, U, A: Allocator, const N: usize>(
    left: &Vec<T, A>,
    right: &&[U; N],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&[U; N]>>::eq(left, right)
}

pub fn binding_35<'spec0, T: PartialEq<U>, U, A: Allocator, const N: usize>(
    left: &Vec<T, A>,
    right: &&[U; N],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
{
    <Vec<T, A> as PartialEq<&[U; N]>>::ne(left, right)
}

} // verus!
}
