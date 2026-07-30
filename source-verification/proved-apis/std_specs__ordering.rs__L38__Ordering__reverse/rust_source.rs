pub const fn reverse(self) -> Ordering {
        match self {
            Less => Greater,
            Equal => Equal,
            Greater => Less,
        }
    }
