pub const fn continue_value(self) -> Option<C>
    where
        Self: [const] Destruct,
    {
        match self {
            ControlFlow::Continue(x) => Some(x),
            ControlFlow::Break(..) => None,
        }
    }
