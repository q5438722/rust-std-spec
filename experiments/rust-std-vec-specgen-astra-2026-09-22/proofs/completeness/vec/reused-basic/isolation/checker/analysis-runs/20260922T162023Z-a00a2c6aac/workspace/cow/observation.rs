#![cfg(not(no_global_oom_handling))]

use std::borrow::Cow;
use vstd::prelude::*;

verus! {

#[verifier::ext_equal]
pub enum CowContents<T> {
    Borrowed(Seq<T>),
    Owned(Seq<T>),
}

pub trait CowObservation<T> {
    spec fn view(&self) -> CowContents<T>;
}

impl<'a, T: Clone> CowObservation<T> for Cow<'a, [T]> {
    open spec fn view(&self) -> CowContents<T> {
        match self {
            Cow::Borrowed(s) => CowContents::Borrowed(s@),
            Cow::Owned(v) => CowContents::Owned(v@),
        }
    }
}

}
