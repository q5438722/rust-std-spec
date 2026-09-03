/// }
/// ```
///
/// ### FFI: Handling null pointers
///
/// In languages such as C++, pointers to empty collections are not guaranteed to be non-null.
/// When accepting such pointers, they have to be checked for null-ness to avoid undefined
/// behavior.
///
/// ```
/// use std::slice;
///
/// /// Sum the elements of an FFI slice.
/// ///
/// /// # Safety
/// ///
/// /// If ptr is not NULL, it must be correctly aligned and
/// /// point to `len` initialized items of type `f32`.
/// unsafe extern "C" fn sum_slice(ptr: *const f32, len: usize) -> f32 {
///     let data = if ptr.is_null() {
///         // `len` is assumed to be 0.
///         &[]
///     } else {
///         // SAFETY: see function docstring.
///         unsafe { slice::from_raw_parts(ptr, len) }
///     };
///     data.into_iter().sum()
/// }
///
/// // This could be the result of C++'s std::vector::data():
/// let ptr = std::ptr::null();
/// // And this could be std::vector::size():
/// let len = 0;
/// assert_eq!(unsafe { sum_slice(ptr, len) }, 0.0);
/// ```
///
/// [valid]: ptr#safety
/// [`NonNull::dangling()`]: ptr::NonNull::dangling
#[inline]
#[stable(feature = "rust1", since = "1.0.0")]
#[rustc_const_stable(feature = "const_slice_from_raw_parts", since = "1.64.0")]
#[must_use]
#[rustc_diagnostic_item = "slice_from_raw_parts"]
#[track_caller]
pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T] {
    // SAFETY: the caller must uphold the safety contract for `from_raw_parts`.
    unsafe {
        ub_checks::assert_unsafe_precondition!(
            check_language_ub,
            "slice::from_raw_parts requires the pointer to be aligned and non-null, and the total size of the slice not to exceed `isize::MAX`",
            (
                data: *mut () = data as *mut (),
                size: usize = size_of::<T>(),
                align: usize = align_of::<T>(),
                len: usize = len,
            ) =>
            ub_checks::maybe_is_aligned_and_not_null(data, align, false)
                && ub_checks::is_valid_allocation_size(size, len)
        );
        &*ptr::slice_from_raw_parts(data, len)
    }
}
