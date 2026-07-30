pub fn new_uninit() -> Box<mem::MaybeUninit<T>> {
        // This is the same as `Self::new_uninit_in(Global)`, but manually inlined (just like
        // `Box::new`).

        // SAFETY:
        // - If `allocate` succeeds, the returned pointer exactly matches what `Box` needs.
        unsafe { mem::transmute(box_new_uninit(<T as SizedTypeProperties>::LAYOUT)) }
    }
