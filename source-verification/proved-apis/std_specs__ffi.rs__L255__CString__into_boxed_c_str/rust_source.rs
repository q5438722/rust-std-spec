pub fn into_boxed_c_str(self) -> Box<CStr> {
        unsafe { Box::from_raw(Box::into_raw(self.into_inner()) as *mut CStr) }
    }
