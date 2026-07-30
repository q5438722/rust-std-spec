pub fn into_bytes_with_nul(self) -> Vec<u8> {
        self.into_inner().into_vec()
    }
