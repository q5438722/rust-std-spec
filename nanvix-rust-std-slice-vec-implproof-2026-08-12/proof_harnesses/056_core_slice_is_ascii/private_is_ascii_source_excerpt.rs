/// Chunk size for SSE2 vectorized ASCII checking (4x 16-byte loads).
#[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
const SSE2_CHUNK_SIZE: usize = 64;

#[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
#[inline]
fn is_ascii_sse2(bytes: &[u8]) -> bool {
    use crate::arch::x86_64::{__m128i, _mm_loadu_si128, _mm_movemask_epi8, _mm_or_si128};

    let (chunks, rest) = bytes.as_chunks::<SSE2_CHUNK_SIZE>();

    for chunk in chunks {
        let ptr = chunk.as_ptr();
        // SAFETY: chunk is 64 bytes. SSE2 is baseline on x86_64.
        let mask = unsafe {
            let a1 = _mm_loadu_si128(ptr as *const __m128i);
            let a2 = _mm_loadu_si128(ptr.add(16) as *const __m128i);
            let b1 = _mm_loadu_si128(ptr.add(32) as *const __m128i);
            let b2 = _mm_loadu_si128(ptr.add(48) as *const __m128i);
            // OR all chunks - if any byte has high bit set, combined will too.
            let combined = _mm_or_si128(_mm_or_si128(a1, a2), _mm_or_si128(b1, b2));
            // Create a mask from the MSBs of each byte.
            // If any byte is >= 128, its MSB is 1, so the mask will be non-zero.
            _mm_movemask_epi8(combined)
        };
        if mask != 0 {
            return false;
        }
    }

    // Handle remaining bytes
    rest.iter().all(|b| b.is_ascii())
}

/// ASCII test optimized to use the `pmovmskb` instruction on `x86-64`.
///
/// Uses explicit SSE2 intrinsics to prevent LLVM from auto-vectorizing with
/// broken AVX-512 code that extracts mask bits one-by-one.
#[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
#[inline]
#[rustc_allow_const_fn_unstable(const_eval_select)]
const fn is_ascii(bytes: &[u8]) -> bool {
    const USIZE_SIZE: usize = size_of::<usize>();
    const NONASCII_MASK: usize = usize::MAX / 255 * 0x80;

    const_eval_select!(
        @capture { bytes: &[u8] } -> bool:
        if const {
            is_ascii_simple(bytes)
        } else {
            // For small inputs, use usize-at-a-time processing to avoid SSE2 call overhead.
            if bytes.len() < SSE2_CHUNK_SIZE {
                let chunks = bytes.chunks_exact(USIZE_SIZE);
                let remainder = chunks.remainder();
                for chunk in chunks {
                    let word = usize::from_ne_bytes(chunk.try_into().unwrap());
                    if (word & NONASCII_MASK) != 0 {
                        return false;
                    }
                }
                return remainder.iter().all(|b| b.is_ascii());
            }

            is_ascii_sse2(bytes)
        }
    )
}
