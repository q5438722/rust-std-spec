pub const fn expect(self, msg: &str) -> T {
        match self {
            Some(val) => val,
            None => expect_failed(msg),
        }
    }
