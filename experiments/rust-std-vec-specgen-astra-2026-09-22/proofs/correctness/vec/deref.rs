#![feature(allocator_api)]

#[path = "../../../specs/vec/reused_basic.rs"]
pub mod reused_basic;

pub use reused_basic::deref;
