#![feature(allocator_api, slice_index_methods)]

#[path = "../../../specs/vec/index.rs"]
pub mod vec_index;

pub use vec_index::index_source;
