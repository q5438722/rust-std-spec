pub const fn is_unspecified(&self) -> bool {
        match self {
            IpAddr::V4(ip) => ip.is_unspecified(),
            IpAddr::V6(ip) => ip.is_unspecified(),
        }
    }
