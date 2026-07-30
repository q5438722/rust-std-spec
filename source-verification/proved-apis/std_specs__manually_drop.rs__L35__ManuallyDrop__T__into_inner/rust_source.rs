pub const fn into_inner(slot: ManuallyDrop<T>) -> T {
        // Cannot use `MaybeDangling::into_inner` as that does not yet have the desired semantics.
        // SAFETY: We know this is a valid `T`. `slot` will not be dropped.
        unsafe { (&raw const slot).cast::<T>().read() }
    }
