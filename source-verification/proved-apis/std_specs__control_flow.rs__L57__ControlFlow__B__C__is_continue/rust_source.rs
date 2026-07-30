pub const fn is_continue(&self) -> bool {
        matches!(*self, ControlFlow::Continue(_))
    }
