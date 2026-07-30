pub const fn is_eq(self) -> bool {
        // All the `is_*` methods are implemented as comparisons against zero
        // to follow how clang's libcxx implements their equivalents in
        // <https://github.com/llvm/llvm-project/blob/60486292b79885b7800b082754153202bef5b1f0/libcxx/include/__compare/is_eq.h#L23-L28>

        self.as_raw() == 0
    }
