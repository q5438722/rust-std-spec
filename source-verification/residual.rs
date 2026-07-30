#![allow(dead_code)]

use core::convert::{From, Infallible};
use vstd::prelude::*;
use vstd::std_specs::convert::FromSpec;

verus! {

axiom fn infallible_is_uninhabited(value: Infallible)
    ensures
        false
;

fn source_option_from_residual<T>(
    residual: Option<Infallible>,
) -> (result: Option<T>)
    ensures
        residual.is_none(),
        result.is_none(),
{
    match residual {
        None => None,
        Some(value) => {
            proof {
                infallible_is_uninhabited(value);
            }
            None
        },
    }
}

#[verifier::exec_allows_no_decreases_clause]
fn source_result_from_residual<T, E, F: From<E> + FromSpec<E>>(
    residual: Result<Infallible, E>,
) -> (result: Result<T, F>)
    requires
        F::obeys_from_spec(),
    ensures
        match (residual, result) {
            (Err(error), Err(converted)) => converted == F::from_spec(error),
            _ => false,
        },
{
    match residual {
        Err(error) => Err(F::from(error)),
        Ok(value) => {
            proof {
                infallible_is_uninhabited(value);
            }
            loop {}
        },
    }
}

} // verus!

fn main() {}
