#![feature(allocator_api)]

use std::alloc::Global;
use vstd::prelude::*;

verus! {

pub fn global() -> Global {
    Global
}

}
