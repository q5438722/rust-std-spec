pub const fn break_value(self) -> Option<B>
    where
        Self: [const] Destruct,
    {
        match self {
            ControlFlow::Continue(..) => None,
            ControlFlow::Break(x) => Some(x),
        }
    }
