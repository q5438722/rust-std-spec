#![feature(allocator_api, const_heap)]

pub mod vec {
    pub mod borrowed;
    pub mod owned_conversions;
    pub mod reused_basic;
    pub mod with_capacity;
}

pub mod cow {
    #![cfg(not(no_global_oom_handling))]
    pub mod observation;
    pub mod conversions;
}
