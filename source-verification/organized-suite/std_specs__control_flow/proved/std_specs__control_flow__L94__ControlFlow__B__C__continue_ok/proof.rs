#![allow(dead_code)]

use core::cmp::Ordering;
use core::convert::Infallible;
use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

fn ordering_is_eq_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Equal,
{
    match ordering {
        Ordering::Equal => true,
        _ => false,
    }
}

fn ordering_is_ne_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Equal),
{
    match ordering {
        Ordering::Equal => false,
        _ => true,
    }
}

fn ordering_is_lt_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Less,
{
    match ordering {
        Ordering::Less => true,
        _ => false,
    }
}

fn ordering_is_gt_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Greater,
{
    match ordering {
        Ordering::Greater => true,
        _ => false,
    }
}

fn ordering_is_le_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Greater),
{
    match ordering {
        Ordering::Greater => false,
        _ => true,
    }
}

fn ordering_is_ge_proof(ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Less),
{
    match ordering {
        Ordering::Less => false,
        _ => true,
    }
}

fn ordering_reverse_proof(ordering: Ordering) -> (result: Ordering)
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

fn ordering_then_proof(ordering: Ordering, other: Ordering) -> (result: Ordering)
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

fn control_flow_is_break_proof<B, C>(value: &ControlFlow<B, C>) -> (result: bool)
    ensures
        result <==> value is Break,
{
    match *value {
        ControlFlow::Break(_) => true,
        ControlFlow::Continue(_) => false,
    }
}

fn control_flow_is_continue_proof<B, C>(value: &ControlFlow<B, C>) -> (result: bool)
    ensures
        result <==> value is Continue,
{
    match *value {
        ControlFlow::Break(_) => false,
        ControlFlow::Continue(_) => true,
    }
}

fn control_flow_break_value_proof<B, C>(value: ControlFlow<B, C>) -> (result: Option<B>)
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

fn control_flow_continue_value_proof<B, C>(value: ControlFlow<B, C>) -> (result: Option<C>)
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

fn control_flow_break_ok_proof<B, C>(value: ControlFlow<B, C>) -> (result: Result<B, C>)
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

fn control_flow_continue_ok_proof<B, C>(value: ControlFlow<B, C>) -> (result: Result<C, B>)
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

fn result_branch_proof<T, E>(
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

fn option_branch_proof<T>(
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
