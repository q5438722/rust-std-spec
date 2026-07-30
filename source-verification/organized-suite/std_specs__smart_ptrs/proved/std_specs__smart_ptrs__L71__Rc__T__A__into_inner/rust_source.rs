pub fn into_inner(this: Self) -> Option<T> {
        Rc::try_unwrap(this).ok()
    }
