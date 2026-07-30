pub const fn is_ipv6(&self) -> bool {
        matches!(*self, SocketAddr::V6(_))
    }
