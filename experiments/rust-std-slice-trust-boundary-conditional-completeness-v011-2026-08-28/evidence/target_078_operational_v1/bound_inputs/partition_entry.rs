pub(crate) fn partition<T, F>(v: &mut [T], pivot: usize, is_less: &mut F) -> usize
where
    F: FnMut(&T, &T) -> bool,
{
    let len = v.len();

    // Allows for panic-free code-gen by proving this property to the compiler.
    if len == 0 {
        return 0;
    }

    if pivot >= len {
        intrinsics::abort();
    }

    // SAFETY: We checked that `pivot` is in-bounds.
    unsafe {
        // Place the pivot at the beginning of slice.
        v.swap_unchecked(0, pivot);
    }
    let (pivot, v_without_pivot) = v.split_at_mut(1);

    // Assuming that Rust generates noalias LLVM IR we can be sure that a partition function
    // signature of the form `(v: &mut [T], pivot: &T)` guarantees that pivot and v can't alias.
    // Having this guarantee is crucial for optimizations. It's possible to copy the pivot value
    // into a stack value, but this creates issues for types with interior mutability mandating
    // a drop guard.
    let pivot = &mut pivot[0];

    // This construct is used to limit the LLVM IR generated, which saves large amounts of
    // compile-time by only instantiating the code that is needed. Idea by Frank Steffahn.
    let num_lt = (const { inst_partition::<T, F>() })(v_without_pivot, pivot, is_less);

    if num_lt >= len {
        intrinsics::abort();
    }

    // SAFETY: We checked that `num_lt` is in-bounds.
    unsafe {
        // Place the pivot between the two partitions.
        v.swap_unchecked(0, num_lt);
    }

    num_lt
}
