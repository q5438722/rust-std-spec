#![cfg(not(no_global_oom_handling))]

use std::borrow::Cow;
use vstd::prelude::*;

#[path = "../../../specs/cow/observation.rs"]
pub mod observation;
use observation::{CowContents, CowObservation};

verus! {

pub fn from_array<'a, T: Clone, const N: usize>(s: &'a [T; N]) -> (result: Cow<'a, [T]>)
    ensures
        CowObservation::view(&result) == CowContents::Borrowed(s@),
{
    Cow::Borrowed(s as &[_])
}

}
