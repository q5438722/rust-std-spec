pub const fn is_ipv4(&self) -> bool {
        matches!(*self, SocketAddr::V4(_))
    }
