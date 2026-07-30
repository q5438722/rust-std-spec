pub fn new(x: T) -> Self {
        // This is `Box::new_uninit` but inlined to avoid build time regressions.
        let ptr = box_new_uninit(<T as SizedTypeProperties>::LAYOUT) as *mut T;
        // Nothing below can panic so we do not have to worry about deallocating `ptr`.
        // SAFETY: we just allocated the box to store `x`.
        unsafe { core::intrinsics::write_via_move(ptr, x) };
        // SAFETY: we just initialized `b`.
        unsafe { mem::transmute(ptr) }
    }
