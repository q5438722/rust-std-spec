pub const fn from_bytes_until_nul(bytes: &[u8]) -> Result<&CStr, FromBytesUntilNulError> {
        let nul_pos = memchr::memchr(0, bytes);
        match nul_pos {
            Some(nul_pos) => {
                // FIXME(const-hack) replace with range index
                // SAFETY: nul_pos + 1 <= bytes.len()
                let subslice = unsafe { crate::slice::from_raw_parts(bytes.as_ptr(), nul_pos + 1) };
                // SAFETY: We know there is a nul byte at nul_pos, so this slice
                // (ending at the nul byte) is a well-formed C string.
                Ok(unsafe { CStr::from_bytes_with_nul_unchecked(subslice) })
            }
            None => Err(FromBytesUntilNulError(())),
        }
    }
