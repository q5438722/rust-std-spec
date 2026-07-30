pub const fn then(self, other: Ordering) -> Ordering {
        match self {
            Equal => other,
            _ => self,
        }
    }
