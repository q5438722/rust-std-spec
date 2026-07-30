pub const fn is_break(&self) -> bool {
        matches!(*self, ControlFlow::Break(_))
    }
