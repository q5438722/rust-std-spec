    pub const fn as_mut_ptr(&mut self) -> *mut T {
        self as *mut [T] as *mut T
    }
