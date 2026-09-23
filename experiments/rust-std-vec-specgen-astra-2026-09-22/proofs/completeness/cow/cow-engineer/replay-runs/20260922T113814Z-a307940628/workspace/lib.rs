#![feature(allocator_api)]

pub mod vec {
    pub mod borrowed;
}

pub mod cow {
    #![cfg(not(no_global_oom_handling))]
    pub mod observation;
    pub mod conversions;
}
