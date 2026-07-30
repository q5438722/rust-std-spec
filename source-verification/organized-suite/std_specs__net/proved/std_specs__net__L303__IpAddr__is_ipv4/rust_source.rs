pub const fn is_ipv4(&self) -> bool {
        matches!(self, IpAddr::V4(_))
    }
