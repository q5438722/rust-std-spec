#![feature(allocator_api, const_heap, const_trait_impl)]

#[path = "../../../specs/vec/with_capacity.rs"]
pub mod with_capacity_source;

#[cfg(not(no_global_oom_handling))]
pub use with_capacity_source::with_capacity;
