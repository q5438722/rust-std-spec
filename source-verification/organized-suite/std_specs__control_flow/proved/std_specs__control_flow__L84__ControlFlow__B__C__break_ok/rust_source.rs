pub const fn break_ok(self) -> Result<B, C> {
        match self {
            ControlFlow::Continue(c) => Err(c),
            ControlFlow::Break(b) => Ok(b),
        }
    }
