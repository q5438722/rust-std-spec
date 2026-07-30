pub const fn is_char_boundary(&self, index: usize) -> bool {
        // 0 is always ok.
        // Test for 0 explicitly so that it can optimize out the check
        // easily and skip reading string data for that case.
        // Note that optimizing `self.get(..index)` relies on this.
        if index == 0 {
            return true;
        }

        if index >= self.len() {
            // For `true` we have two options:
            //
            // - index == self.len()
            //   Empty strings are valid, so return true
            // - index > self.len()
            //   In this case return false
            //
            // The check is placed exactly here, because it improves generated
            // code on higher opt-levels. See PR #84751 for more details.
            index == self.len()
        } else {
            self.as_bytes()[index].is_utf8_char_boundary()
        }
    }
