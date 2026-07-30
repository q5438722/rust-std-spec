#![allow(dead_code)]

use core::cmp::Ordering;
use core::convert::Infallible;
use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

fn source_ordering_is_eq(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Equal,
{
    match ordering {
        Ordering::Equal => true,
        _ => false,
    }
}

fn source_ordering_is_ne(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Equal),
{
    match ordering {
        Ordering::Equal => false,
        _ => true,
    }
}

fn source_ordering_is_lt(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Less,
{
    match ordering {
        Ordering::Less => true,
        _ => false,
    }
}

fn source_ordering_is_gt(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Greater,
{
    match ordering {
        Ordering::Greater => true,
        _ => false,
    }
}

fn source_ordering_is_le(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Greater),
{
    match ordering {
        Ordering::Greater => false,
        _ => true,
    }
}

fn source_ordering_is_ge(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Less),
{
    match ordering {
        Ordering::Less => false,
        _ => true,
    }
}

fn source_ordering_reverse(ordering: Ordering) -> (result: Ordering)
    ensures
        result == match ordering {
            Ordering::Less => Ordering::Greater,
            Ordering::Equal => Ordering::Equal,
            Ordering::Greater => Ordering::Less,
        },
{
    match ordering {
        Ordering::Less => Ordering::Greater,
        Ordering::Equal => Ordering::Equal,
        Ordering::Greater => Ordering::Less,
    }
}

fn source_ordering_then(ordering: Ordering, other: Ordering) -> (result: Ordering)
    ensures
        result == if ordering is Equal {
            other
        } else {
            ordering
        },
{
    match ordering {
        Ordering::Equal => other,
        _ => ordering,
    }
}

fn source_control_flow_is_break<B, C>(value: &ControlFlow<B, C>) -> (result: bool)
    ensures
        result <==> value is Break,
{
    match *value {
        ControlFlow::Break(_) => true,
        ControlFlow::Continue(_) => false,
    }
}

fn source_control_flow_is_continue<B, C>(value: &ControlFlow<B, C>) -> (result: bool)
    ensures
        result <==> value is Continue,
{
    match *value {
        ControlFlow::Break(_) => false,
        ControlFlow::Continue(_) => true,
    }
}

fn source_control_flow_break_value<B, C>(value: ControlFlow<B, C>) -> (result: Option<B>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Some(b),
            ControlFlow::Continue(_) => None,
        },
{
    match value {
        ControlFlow::Continue(..) => None,
        ControlFlow::Break(value) => Some(value),
    }
}

fn source_control_flow_continue_value<B, C>(value: ControlFlow<B, C>) -> (result: Option<C>)
    ensures
        result == match value {
            ControlFlow::Break(_) => None,
            ControlFlow::Continue(c) => Some(c),
        },
{
    match value {
        ControlFlow::Continue(value) => Some(value),
        ControlFlow::Break(..) => None,
    }
}

fn source_control_flow_break_ok<B, C>(value: ControlFlow<B, C>) -> (result: Result<B, C>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Ok(b),
            ControlFlow::Continue(c) => Err(c),
        },
{
    match value {
        ControlFlow::Continue(value) => Err(value),
        ControlFlow::Break(value) => Ok(value),
    }
}

fn source_control_flow_continue_ok<B, C>(value: ControlFlow<B, C>) -> (result: Result<C, B>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Err(b),
            ControlFlow::Continue(c) => Ok(c),
        },
{
    match value {
        ControlFlow::Continue(value) => Ok(value),
        ControlFlow::Break(value) => Err(value),
    }
}

fn source_result_branch<T, E>(
    value: Result<T, E>,
) -> (result: ControlFlow<Result<Infallible, E>, T>)
    ensures
        result == match value {
            Ok(value) => ControlFlow::Continue(value),
            Err(error) => ControlFlow::Break(Err(error)),
        },
{
    match value {
        Ok(value) => ControlFlow::Continue(value),
        Err(error) => ControlFlow::Break(Err(error)),
    }
}

fn source_option_branch<T>(
    value: Option<T>,
) -> (result: ControlFlow<Option<Infallible>, T>)
    ensures
        result == match value {
            Some(value) => ControlFlow::Continue(value),
            None => ControlFlow::Break(None),
        },
{
    match value {
        Some(value) => ControlFlow::Continue(value),
        None => ControlFlow::Break(None),
    }
}

} // verus!

fn main() {}
