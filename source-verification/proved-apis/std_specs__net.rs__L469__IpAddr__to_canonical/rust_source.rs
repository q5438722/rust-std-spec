pub const fn to_canonical(&self) -> IpAddr {
        match self {
            IpAddr::V4(_) => *self,
            IpAddr::V6(v6) => v6.to_canonical(),
        }
    }
