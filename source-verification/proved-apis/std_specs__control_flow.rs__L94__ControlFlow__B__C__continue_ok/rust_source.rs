pub const fn continue_ok(self) -> Result<C, B> {
        match self {
            ControlFlow::Continue(c) => Ok(c),
            ControlFlow::Break(b) => Err(b),
        }
    }
