use super::slice_shared::{ascii_whitespace, lowercase_byte, uppercase_byte};
use core::slice::*;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::slice::into_iter_elts;

verus! {

pub assume_specification<'a, T>[ <&'a mut [T] as IntoIterator>::into_iter ](
    slice: &'a mut [T],
) -> (result: IterMut<'a, T>)
    ensures
        IteratorSpec::remaining(&result).len() == old(slice)@.len() == final(slice)@.len(),
        forall|i: int|
            0 <= i < old(slice)@.len() ==> *IteratorSpec::remaining(&result)[i] == old(slice)@[i],
        forall|i: int|
            0 <= i < old(slice)@.len() ==> *final(IteratorSpec::remaining(&result)[i])
                == final(slice)@[i],
;

pub assume_specification[ <[u8]>::make_ascii_uppercase ](slice: &mut [u8])
    ensures
        final(slice)@ =~= old(slice)@.map_values(|byte: u8| uppercase_byte(byte)),
;

pub assume_specification[ <[u8]>::make_ascii_lowercase ](slice: &mut [u8])
    ensures
        final(slice)@ =~= old(slice)@.map_values(|byte: u8| lowercase_byte(byte)),
;

pub assume_specification[ <[u8]>::eq_ignore_ascii_case ](slice: &[u8], other: &[u8]) -> (result:
    bool)
    ensures
        result == (slice@.len() == other@.len() && forall|i: int|
            0 <= i < slice@.len() ==> lowercase_byte(#[trigger] slice@[i]) == lowercase_byte(
                other@[i],
            )),
;

pub assume_specification[ <[u8]>::trim_ascii_start ](slice: &[u8]) -> (result: &[u8])
    ensures
        ({
            let cut = slice@.len() - result@.len();
            &&& result@.len() <= slice@.len()
            &&& result@ == slice@.subrange(cut, slice@.len() as int)
            &&& forall|i: int| 0 <= i < cut ==> ascii_whitespace(#[trigger] slice@[i])
            &&& result@.len() > 0 ==> !ascii_whitespace(result@[0])
        }),
;

pub assume_specification[ <[u8]>::trim_ascii_end ](slice: &[u8]) -> (result: &[u8])
    ensures
        result@.len() <= slice@.len(),
        result@ == slice@.subrange(0, result@.len() as int),
        forall|i: int| result@.len() <= i < slice@.len() ==> ascii_whitespace(#[trigger] slice@[i]),
        result@.len() > 0 ==> !ascii_whitespace(result@[result@.len() - 1]),
;

pub assume_specification[ <[u8]>::trim_ascii ](slice: &[u8]) -> (result: &[u8])
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
;

pub assume_specification<'a, T>[ <Iter<'a, T> as Default>::default ]() -> (result: Iter<'a, T>)
    ensures
        IteratorSpec::remaining(&result) =~= Seq::<&'a T>::empty(),
        into_iter_elts(result) == IteratorSpec::remaining(&result).unref(),
;

pub assume_specification<'a, T>[ <IterMut<'a, T> as Default>::default ]() -> (result: IterMut<
    'a,
    T,
>)
    ensures
        IteratorSpec::remaining(&result) =~= Seq::<&'a mut T>::empty(),
;

pub assume_specification<'a, T>[ <Iter<'a, T> as Iterator>::count ](iter: Iter<'a, T>) -> (result:
    usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
;

pub assume_specification<'a, T>[ <IterMut<'a, T> as Iterator>::count ](
    iter: IterMut<'a, T>,
) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
;

pub assume_specification<'a, T>[ <Iter<'a, T> as Iterator>::size_hint ](
    iter: &Iter<'a, T>,
) -> (result: (usize, Option<usize>))
    ensures
        result.0 == IteratorSpec::remaining(iter).len(),
        result.1 == Some(result.0),
;

pub assume_specification<'a, T>[ <IterMut<'a, T> as Iterator>::size_hint ](
    iter: &IterMut<'a, T>,
) -> (result: (usize, Option<usize>))
    ensures
        result.0 == IteratorSpec::remaining(iter).len(),
        result.1 == Some(result.0),
;

pub assume_specification<'a, T>[ <Iter<'a, T> as Iterator>::last ](iter: Iter<'a, T>) -> (result:
    Option<&'a T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
;

pub assume_specification<'a, T>[ <IterMut<'a, T> as Iterator>::last ](
    iter: IterMut<'a, T>,
) -> (result: Option<&'a mut T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
;

} // verus!
pub mod ascii {
    use super::super::slice_shared::ascii_model::*;
    use core::slice::*;
    use state::Parts;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification[ <[u8]>::escape_ascii ](bytes: &[u8]) -> (result: EscapeAscii<'_>)
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
;

pub assume_specification<'a>[ <EscapeAscii<'a> as Iterator>::next ](
    iter: &mut EscapeAscii<'a>,
) -> (result: Option<u8>)
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
;

pub assume_specification<'a>[ <EscapeAscii<'a> as DoubleEndedIterator>::next_back ](
    iter: &mut EscapeAscii<'a>,
) -> (result: Option<u8>)
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
;

pub assume_specification<'a>[ <EscapeAscii<'a> as Iterator>::last ](
    iter: EscapeAscii<'a>,
) -> (result: Option<u8>)
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
;

pub assume_specification<'a>[ <EscapeAscii<'a> as Iterator>::size_hint ](
    iter: &EscapeAscii<'a>,
) -> (result: (usize, Option<usize>))
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
;

} // verus!
}

pub mod splits {
    use super::super::slice_shared::splits_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <SplitInclusive<
    'a,
    T,
    P,
> as Iterator>::size_hint ](iter: &SplitInclusive<'a, T, P>) -> (out: (usize, Option<usize>))
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
;

pub assume_specification<'a, T, P: FnMut(&T) -> bool>[ <SplitInclusiveMut<
    'a,
    T,
    P,
> as Iterator>::size_hint ](iter: &SplitInclusiveMut<'a, T, P>) -> (out: (usize, Option<usize>))
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
;

} // verus!
}

pub mod chunk_by {
    use super::super::slice_shared::chunk_by_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T: 'a, P: FnMut(&T, &T) -> bool>[ <ChunkBy<
    'a,
    T,
    P,
> as Iterator>::size_hint ](iter: &ChunkBy<'a, T, P>) -> (result: (usize, Option<usize>))
    ensures
        ({
            let (state, result): (Current<T, P>, (usize, Option<usize>)) = (iter.state(), result);
            result == if state.slice.len() == 0 {
                (0usize, Some(0usize))
            } else {
                (1usize, Some(state.slice.len() as usize))
            }
        }),
;

pub assume_specification<'a, T: 'a, P: FnMut(&T, &T) -> bool>[ <ChunkByMut<
    'a,
    T,
    P,
> as Iterator>::size_hint ](iter: &ChunkByMut<'a, T, P>) -> (result: (usize, Option<usize>))
    ensures
        ({
            let (state, result): (Current<T, P>, (usize, Option<usize>)) = (iter.state(), result);
            result == if state.slice.len() == 0 {
                (0usize, Some(0usize))
            } else {
                (1usize, Some(state.slice.len() as usize))
            }
        }),
;

} // verus!
}

pub mod chunks {
    use super::super::slice_shared::chunks_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T>[ <Chunks<'a, T> as Clone>::clone ](iter: &Chunks<'a, T>) -> (result:
    Chunks<'a, T>)
    ensures
        result == *iter,
;

pub assume_specification<'a, T>[ <ChunksExact<'a, T> as Clone>::clone ](
    iter: &ChunksExact<'a, T>,
) -> (result: ChunksExact<'a, T>)
    ensures
        result == *iter,
;

pub assume_specification<'a, T>[ <ChunksExact<'a, T>>::remainder ](
    iter: &ChunksExact<'a, T>,
) -> (result: &'a [T])
    ensures
        ({
            let (before, item): (State<T>, Seq<T>) = (iter.state(), result@);
            item == before.rem
        }),
;

pub assume_specification<'a, T>[ <RChunks<'a, T> as Clone>::clone ](
    iter: &RChunks<'a, T>,
) -> (result: RChunks<'a, T>)
    ensures
        result == *iter,
;

pub assume_specification<'a, T>[ <RChunksExact<'a, T> as Clone>::clone ](
    iter: &RChunksExact<'a, T>,
) -> (result: RChunksExact<'a, T>)
    ensures
        result == *iter,
;

pub assume_specification<'a, T>[ <RChunksExact<'a, T>>::remainder ](
    iter: &RChunksExact<'a, T>,
) -> (result: &'a [T])
    ensures
        ({
            let (before, item): (State<T>, Seq<T>) = (iter.state(), result@);
            item == before.rem
        }),
;

} // verus!
}

pub mod arrays {
    use super::super::slice_shared::arrays_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T, const N: usize>[ <ArrayWindows<'a, T, N> as Clone>::clone ](
    iter: &ArrayWindows<'a, T, N>,
) -> (result: ArrayWindows<'a, T, N>)
    ensures
        result == *iter,
        result.remaining() == iter.remaining(),
        result.obeys_prophetic_iter_laws() == iter.obeys_prophetic_iter_laws(),
        result.will_return_none() == iter.will_return_none(),
        result.decrease() == iter.decrease(),
;

} // verus!
}

pub mod windows {
    use super::super::slice_shared::windows_model::*;
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

pub assume_specification<'a, T>[ <Windows<'a, T> as Clone>::clone ](
    iter: &Windows<'a, T>,
) -> (result: Windows<'a, T>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as Iterator>::next ](
    iter: &mut Windows<'a, T>,
) -> (result: Option<&'a [T]>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as Iterator>::nth ](
    iter: &mut Windows<'a, T>,
    n: usize,
) -> (result: Option<<Windows<'a, T> as Iterator>::Item>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as DoubleEndedIterator>::next_back ](
    iter: &mut Windows<'a, T>,
) -> (result: Option<<Windows<'a, T> as Iterator>::Item>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as DoubleEndedIterator>::nth_back ](
    iter: &mut Windows<'a, T>,
    n: usize,
) -> (result: Option<<Windows<'a, T> as Iterator>::Item>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as Iterator>::count ](
    iter: Windows<'a, T>,
) -> (result: usize)
    ensures
        ({
            let (state, items): (State<T>, Seq<&'a [T]>) = (iter@, IteratorSpec::remaining(&iter));
            valid(state) && items == remaining(state)
        }),
        ({
            let (before, result): (State<T>, usize) = (iter@, result);
            result == values(before).len()
        }),
;

pub assume_specification<'a, T>[ <Windows<'a, T> as Iterator>::last ](
    iter: Windows<'a, T>,
) -> (result: Option<<Windows<'a, T> as Iterator>::Item>)
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
;

pub assume_specification<'a, T>[ <Windows<'a, T> as Iterator>::size_hint ](
    iter: &Windows<'a, T>,
) -> (result: (usize, Option<usize>))
    ensures
        ({
            let (state, items): (State<T>, Seq<&'a [T]>) = (iter@, IteratorSpec::remaining(iter));
            valid(state) && items == remaining(state)
        }),
        ({
            let (before, result): (State<T>, (usize, Option<usize>)) = (iter@, result);
            result.0 == values(before).len() && result.1 == Some(result.0)
        }),
;

} // verus!
}
