pub const fn new_in(alloc: A) -> Self {
        Vec { buf: RawVec::new_in(alloc), len: 0 }
    }
