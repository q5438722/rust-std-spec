pub const fn new() -> Self {
        LinkedList { head: None, tail: None, len: 0, alloc: Global, marker: PhantomData }
    }
