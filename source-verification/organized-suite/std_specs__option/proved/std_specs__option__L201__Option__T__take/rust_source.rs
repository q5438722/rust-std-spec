pub const fn take(&mut self) -> Option<T> {
        // FIXME(const-hack) replace `mem::replace` by `mem::take` when the latter is const ready
        mem::replace(self, None)
    }
