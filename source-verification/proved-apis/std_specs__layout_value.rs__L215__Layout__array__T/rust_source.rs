pub const fn array<T>(n: usize) -> Result<Self, LayoutError> {
        // Reduce the amount of code we need to monomorphize per `T`.
        return inner(T::LAYOUT, n);

        #[inline]
        const fn inner(element_layout: Layout, n: usize) -> Result<Layout, LayoutError> {
            let Layout { size: element_size, align: alignment } = element_layout;

            // We need to check two things about the size:
            //  - That the total size won't overflow a `usize`, and
            //  - That the total size still fits in an `isize`.
            // By using division we can check them both with a single threshold.
            // That'd usually be a bad idea, but thankfully here the element size
            // and alignment are constants, so the compiler will fold all of it.
            if element_size != 0 && n > Layout::max_size_for_alignment(alignment) / element_size {
                return Err(LayoutError);
            }

            // SAFETY: We just checked that we won't overflow `usize` when we multiply.
            // This is a useless hint inside this function, but after inlining this helps
            // deduplicate checks for whether the overall capacity is zero (e.g., in RawVec's
            // allocation path) before/after this multiplication.
            let array_size = unsafe { unchecked_mul(element_size, n) };

            // SAFETY: We just checked above that the `array_size` will not
            // exceed `isize::MAX` even when rounded up to the alignment.
            // And `Alignment` guarantees it's a power of two.
            unsafe { Ok(Layout::from_size_alignment_unchecked(array_size, alignment)) }
        }
    }
