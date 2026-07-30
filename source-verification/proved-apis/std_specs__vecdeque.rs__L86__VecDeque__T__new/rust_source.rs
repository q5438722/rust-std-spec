pub const fn new() -> VecDeque<T> {
        // FIXME(const-hack): This should just be `VecDeque::new_in(Global)` once that hits stable.
        VecDeque { head: 0, len: 0, buf: RawVec::new() }
    }
