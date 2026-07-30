pub fn new(value: T) -> Rc<T> {
        // There is an implicit weak pointer owned by all the strong
        // pointers, which ensures that the weak destructor never frees
        // the allocation while the strong destructor is running, even
        // if the weak pointer is stored inside the strong one.
        unsafe {
            Self::from_inner(
                Box::leak(Box::new(RcInner { strong: Cell::new(1), weak: Cell::new(1), value }))
                    .into(),
            )
        }
    }
