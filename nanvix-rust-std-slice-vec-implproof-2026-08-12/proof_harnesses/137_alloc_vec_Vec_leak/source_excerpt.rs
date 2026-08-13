    pub fn leak<'a>(self) -> &'a mut [T]
    where
        A: 'a,
    {
        let mut me = ManuallyDrop::new(self);
        unsafe { slice::from_raw_parts_mut(me.as_mut_ptr(), me.len) }
    }
