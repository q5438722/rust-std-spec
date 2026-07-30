pub const fn to_canonical(&self) -> IpAddr {
        if let Some(mapped) = self.to_ipv4_mapped() {
            return IpAddr::V4(mapped);
        }
        IpAddr::V6(*self)
    }
