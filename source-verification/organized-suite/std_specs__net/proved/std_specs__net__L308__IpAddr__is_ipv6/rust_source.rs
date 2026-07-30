pub const fn is_ipv6(&self) -> bool {
        matches!(self, IpAddr::V6(_))
    }
