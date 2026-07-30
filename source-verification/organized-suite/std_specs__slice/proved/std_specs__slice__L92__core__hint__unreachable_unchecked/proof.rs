#![feature(const_eval_select)]
#![feature(core_intrinsics)]
#![feature(fmt_arguments_from_str)]
#![feature(panic_internals)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unexpected_cfgs)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

pub assume_specification[core::intrinsics::unreachable]() -> !
    requires
        false,
;

#[cfg(not(verus_keep_ghost))]
#[inline]
const fn check_language_ub_proof() -> bool {
    #[inline]
    fn runtime() -> bool {
        !cfg!(miri)
    }

    #[inline]
    const fn compiletime() -> bool {
        false
    }

    core::intrinsics::const_eval_select((), compiletime, runtime)
        && core::intrinsics::ub_checks()
}

#[cfg(verus_keep_ghost)]
#[inline]
const fn check_language_ub_proof() -> bool
    requires
        false,
{
    false
}

#[cfg(not(verus_keep_ghost))]
#[rustc_no_mir_inline]
#[inline]
#[rustc_nounwind]
#[track_caller]
const fn precondition_check() {
    if !false {
        let msg = concat!(
            "unsafe precondition(s) violated: ",
            "hint::unreachable_unchecked must never be reached",
            "\n\nThis indicates a bug in the program. This Undefined Behavior check is optional, and cannot be relied on for safety."
        );
        core::panicking::panic_nounwind_fmt(
            core::fmt::Arguments::from_str(msg),
            false,
        );
    }
}

#[cfg(verus_keep_ghost)]
#[inline]
#[track_caller]
const fn precondition_check()
    requires
        false,
{
    unsafe { core::intrinsics::unreachable() }
}

#[inline]
#[track_caller]
pub const unsafe fn unreachable_unchecked_proof() -> !
    requires
        false,
{
    if check_language_ub_proof() {
        precondition_check();
    }
    unsafe { core::intrinsics::unreachable() }
}

} // verus!

fn main() {}