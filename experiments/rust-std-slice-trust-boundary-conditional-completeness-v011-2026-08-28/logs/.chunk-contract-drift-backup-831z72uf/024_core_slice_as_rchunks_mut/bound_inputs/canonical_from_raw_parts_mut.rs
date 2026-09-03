/// Performs the same functionality as [`from_raw_parts`], except that a
/// mutable slice is returned.
///
/// # Safety
///
/// Behavior is undefined if any of the following conditions are violated:
///
/// * `data` must be non-null, [valid] for both reads and writes for `len * size_of::<T>()` many bytes,
///   and it must be properly aligned. This means in particular:
///
///     * The entire memory range of this slice must be contained within a single allocation!
///       Slices can never span across multiple allocations.
///     * `data` must be non-null and aligned even for zero-length slices or slices of ZSTs. One
///       reason for this is that enum layout optimizations may rely on references
///       (including slices of any length) being aligned and non-null to distinguish
///       them from other data. You can obtain a pointer that is usable as `data`
///       for zero-length slices using [`NonNull::dangling()`].
///
/// * `data` must point to `len` consecutive properly initialized values of type `T`.
///
/// * The memory referenced by the returned slice must not be accessed through any other pointer
///   (not derived from the return value) for the duration of lifetime `'a`.
///   Both read and write accesses are forbidden.
///
/// * The total size `len * size_of::<T>()` of the slice must be no larger than `isize::MAX`,
///   and adding that size to `data` must not "wrap around" the address space.
///   See the safety documentation of [`pointer::offset`].
///
/// [valid]: ptr#safety
/// [`NonNull::dangling()`]: ptr::NonNull::dangling
#[inline]
#[stable(feature = "rust1", since = "1.0.0")]
#[rustc_const_stable(feature = "const_slice_from_raw_parts_mut", since = "1.83.0")]
#[must_use]
#[rustc_diagnostic_item = "slice_from_raw_parts_mut"]
#[track_caller]
pub const unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> &'a mut [T] {
    // SAFETY: the caller must uphold the safety contract for `from_raw_parts_mut`.
    unsafe {
        ub_checks::assert_unsafe_precondition!(
            check_language_ub,
            "slice::from_raw_parts_mut requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`",
            (
                data: *mut () = data as *mut (),
                size: usize = size_of::<T>(),
                align: usize = align_of::<T>(),
                len: usize = len,
            ) =>
            ub_checks::maybe_is_aligned_and_not_null(data, align, false)
                && ub_checks::is_valid_allocation_size(size, len)
        );
        &mut *ptr::slice_from_raw_parts_mut(data, len)
    }
}
