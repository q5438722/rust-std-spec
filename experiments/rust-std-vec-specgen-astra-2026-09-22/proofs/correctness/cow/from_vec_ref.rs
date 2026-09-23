#![cfg(not(no_global_oom_handling))]

use std::borrow::Cow;
use vstd::prelude::*;

#[path = "../../../specs/cow/observation.rs"]
pub mod observation;
use observation::{CowContents, CowObservation};

verus! {

pub fn from_vec_ref<'a, T: Clone>(v: &'a Vec<T>) -> (result: Cow<'a, [T]>)
    ensures
        CowObservation::view(&result) == CowContents::Borrowed(v@),
{
    Cow::Borrowed(v.as_slice())
}

}
