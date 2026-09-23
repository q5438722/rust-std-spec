#![feature(allocator_api)]

pub mod vec {
    pub mod borrowed;
}

#[cfg(not(no_global_oom_handling))]
pub mod cow {
    pub mod observation;
    pub mod conversions;
}
