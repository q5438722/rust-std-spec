use vstd::prelude::*;

verus! {

pub open spec fn len_post<T>(slice: &[T], result: usize) -> bool {
    result == slice@.len()
}

pub open spec fn is_empty_post<T>(slice: &[T], result: bool) -> bool {
    result <==> slice@.len() == 0
}

pub open spec fn first_post<T>(slice: &[T], result: Option<&T>) -> bool {
    match result {
        None => slice@.len() == 0,
        Some(first) => slice@.len() > 0 && *first == slice@[0],
    }
}

pub open spec fn split_first_post<T>(slice: &[T], result: Option<(&T, &[T])>) -> bool {
    match result {
        None => slice@.len() == 0,
        Some((first, tail)) => {
            &&& slice@.len() > 0
            &&& *first == slice@[0]
            &&& tail@ == slice@.subrange(1, slice@.len() as int)
        },
    }
}

pub open spec fn split_last_post<T>(slice: &[T], result: Option<(&T, &[T])>) -> bool {
    match result {
        None => slice@.len() == 0,
        Some((last, init)) => {
            &&& slice@.len() > 0
            &&& *last == slice@[slice@.len() - 1]
            &&& init@ == slice@.subrange(0, slice@.len() - 1)
        },
    }
}

pub open spec fn last_post<T>(slice: &[T], result: Option<&T>) -> bool {
    match result {
        None => slice@.len() == 0,
        Some(last) => slice@.len() > 0 && *last == slice@[slice@.len() - 1],
    }
}

}
